#!/usr/bin/env python3
"""A small content-free passive HTTP proxy lab for local experimentation.

The lab forwards request and response bodies without decoding or rewriting them.
Its JSONL metrics contain a bounded route class, sizes, timing, status, and an
error class only. It does not record request targets, headers, bodies, client
addresses, prompts, or replies.

This is an educational artifact, not a production model gateway. It intentionally
omits streaming passthrough, TLS termination, authentication, log rotation, and
service supervision.
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import stat
import threading
import time
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Type
from urllib.parse import SplitResult, urlsplit


HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}

ROUTE_CLASSES = {
    "/api/chat": "chat_completions",
    "/chat/completions": "chat_completions",
    "/v1/chat/completions": "chat_completions",
    "/v1/responses": "responses",
    "/v1/models": "models",
    "/health": "health",
    "/healthz": "health",
}

HEADER_NAME_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_upstream(value: str, *, allow_remote: bool = False) -> SplitResult:
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("upstream scheme must be http or https")
    if not parsed.hostname or parsed.port is None:
        raise ValueError("upstream must include an explicit host and port")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("upstream must not include user information")
    if parsed.query or parsed.fragment:
        raise ValueError("upstream must not include a query or fragment")
    if not allow_remote and parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("remote upstreams require --allow-remote-upstream")
    return parsed


def classify_route(request_target: str) -> str:
    """Map a request target to a bounded class without retaining path segments."""

    path = urlsplit(request_target).path.rstrip("/") or "/"
    return ROUTE_CLASSES.get(path, "other")


def safe_header_name(name: str) -> str | None:
    """Return a header name only if it is a valid RFC 9110 field name."""
    sanitized = name.replace("\r", "").replace("\n", "").replace(":", "")
    if sanitized != name:
        return None
    return sanitized if HEADER_NAME_RE.fullmatch(sanitized) else None


def safe_header_value(value: str) -> str:
    """Remove line breaks before writing a value to an HTTP response header."""
    return value.replace("\r", "").replace("\n", "")


class JsonlMetrics:
    """Append content-free records with process-local write serialization."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()

    def write(self, record: dict[str, object]) -> None:
        line = json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            if not hasattr(os, "O_NOFOLLOW") and self.path.is_symlink():
                raise ValueError("metrics path must not be a symbolic link")
            flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
            descriptor = os.open(self.path, flags, 0o600)
            try:
                if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                    raise ValueError("metrics path must be a regular file")
                os.fchmod(descriptor, 0o600)
                handle = os.fdopen(descriptor, "a", encoding="utf-8")
                descriptor = -1
                with handle:
                    handle.write(line)
                    handle.flush()
                    os.fsync(handle.fileno())
            finally:
                if descriptor >= 0:
                    os.close(descriptor)


def joined_upstream_path(upstream: SplitResult, request_target: str) -> str:
    base = upstream.path.rstrip("/")
    target = request_target if request_target.startswith("/") else f"/{request_target}"
    return f"{base}{target}" if base else target


def make_proxy_handler(
    upstream: SplitResult,
    metrics: JsonlMetrics,
    *,
    timeout: float = 30.0,
) -> Type[BaseHTTPRequestHandler]:
    """Create an isolated handler class bound to one upstream and metrics sink."""

    class PassiveProxyHandler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, _format: str, *_args: object) -> None:
            return

        def read_request_body(self) -> bytes:
            length = int(self.headers.get("Content-Length", "0") or "0")
            return self.rfile.read(length) if length > 0 else b""

        def filtered_request_headers(self, body: bytes) -> dict[str, str]:
            headers: dict[str, str] = {}
            for name, value in self.headers.items():
                lowered = name.lower()
                if lowered in HOP_BY_HOP_HEADERS or lowered in {"host", "content-length"}:
                    continue
                headers[name] = value
            headers["Host"] = upstream.netloc
            headers["Content-Length"] = str(len(body))
            return headers

        def send_upstream_response(
            self,
            status: int,
            reason: str,
            headers: list[tuple[str, str]],
            body: bytes,
        ) -> None:
            self.send_response(status, reason)
            for name, value in headers:
                lowered = name.lower()
                if lowered in HOP_BY_HOP_HEADERS or lowered == "content-length":
                    continue
                safe_name = safe_header_name(name)
                if safe_name is None:
                    continue
                self.send_header(safe_name, safe_header_value(value))
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.end_headers()
            if body:
                self.wfile.write(body)

        def send_proxy_error(self, request_id: str) -> bytes:
            body = json.dumps(
                {"error": "upstream unavailable", "request_id": request_id},
                separators=(",", ":"),
            ).encode("utf-8")
            self.send_response(502, "Bad Gateway")
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(body)
            return body

        def proxy(self) -> None:
            request_id = uuid.uuid4().hex
            started = time.monotonic()
            request_body = self.read_request_body()
            response_body = b""
            status = 502
            error_class: str | None = None
            connection: http.client.HTTPConnection | http.client.HTTPSConnection | None = None

            try:
                connection_type = (
                    http.client.HTTPSConnection
                    if upstream.scheme == "https"
                    else http.client.HTTPConnection
                )
                connection = connection_type(upstream.hostname, upstream.port, timeout=timeout)
                connection.request(
                    self.command,
                    joined_upstream_path(upstream, self.path),
                    body=request_body,
                    headers=self.filtered_request_headers(request_body),
                )
                response = connection.getresponse()
                status = response.status
                response_body = response.read()
                self.send_upstream_response(
                    response.status,
                    response.reason,
                    response.getheaders(),
                    response_body,
                )
            except Exception as exc:  # The lab records the class, never the message.
                error_class = type(exc).__name__
                response_body = self.send_proxy_error(request_id)
            finally:
                if connection is not None:
                    connection.close()
                metrics.write(
                    {
                        "duration_ms": round((time.monotonic() - started) * 1000, 3),
                        "error_class": error_class,
                        "method": self.command,
                        "request_bytes": len(request_body),
                        "request_id": request_id,
                        "response_bytes": len(response_body),
                        "route_class": classify_route(self.path),
                        "status": status,
                        "ts": utc_now(),
                    }
                )

        do_GET = proxy
        do_POST = proxy
        do_PUT = proxy
        do_PATCH = proxy
        do_DELETE = proxy
        do_OPTIONS = proxy

    return PassiveProxyHandler


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Content-free passive proxy lab")
    parser.add_argument("--listen-host", default="127.0.0.1")
    parser.add_argument("--listen-port", type=int, default=18080)
    parser.add_argument("--upstream", required=True, help="Example: http://127.0.0.1:18081")
    parser.add_argument("--metrics", type=Path, default=Path("passive-proxy-metrics.jsonl"))
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--allow-remote-upstream", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    upstream = parse_upstream(args.upstream, allow_remote=args.allow_remote_upstream)
    handler = make_proxy_handler(upstream, JsonlMetrics(args.metrics), timeout=args.timeout)
    server = ThreadingHTTPServer((args.listen_host, args.listen_port), handler)
    print(
        f"passive proxy lab listening on http://{args.listen_host}:{server.server_port} "
        f"and forwarding to {upstream.scheme}://{upstream.netloc}{upstream.path}",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
