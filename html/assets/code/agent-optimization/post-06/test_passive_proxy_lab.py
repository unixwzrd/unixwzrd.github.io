#!/usr/bin/env python3
from __future__ import annotations

import json
import socket
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from passive_proxy_lab import JsonlMetrics, classify_route, make_proxy_handler, parse_upstream


class CaptureUpstream(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    received: list[dict[str, object]] = []
    response_body = b'{"ok":true,"spacing":"  preserved  "}\n'

    def log_message(self, _format: str, *_args: object) -> None:
        return

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length)
        type(self).received.append(
            {
                "authorization": self.headers.get("Authorization"),
                "body": body,
                "path": self.path,
            }
        )
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(self.response_body)))
        self.end_headers()
        self.wfile.write(self.response_body)


def start_server(handler: type[BaseHTTPRequestHandler]) -> tuple[ThreadingHTTPServer, threading.Thread]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def read_metrics(path: Path, timeout: float = 2.0) -> str:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.exists() and path.stat().st_size:
            return path.read_text(encoding="utf-8")
        time.sleep(0.01)
    raise AssertionError(f"metrics were not written within {timeout} seconds")


class PassiveProxyLabTests(unittest.TestCase):
    def setUp(self) -> None:
        CaptureUpstream.received = []

    def test_request_and_response_bodies_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_path = Path(tmpdir) / "metrics.jsonl"
            upstream, upstream_thread = start_server(CaptureUpstream)
            self.addCleanup(upstream.shutdown)
            self.addCleanup(upstream.server_close)
            self.addCleanup(upstream_thread.join, 1)

            parsed = parse_upstream(f"http://127.0.0.1:{upstream.server_port}")
            proxy_handler = make_proxy_handler(parsed, JsonlMetrics(metrics_path))
            proxy, proxy_thread = start_server(proxy_handler)
            self.addCleanup(proxy.shutdown)
            self.addCleanup(proxy.server_close)
            self.addCleanup(proxy_thread.join, 1)

            secret_marker = "private prompt text must not enter metrics"
            request_body = json.dumps(
                {"messages": [{"role": "user", "content": secret_marker}]},
                separators=(",", ":"),
            ).encode("utf-8")
            path_marker = "private-path-marker"
            request = Request(
                f"http://127.0.0.1:{proxy.server_port}/sessions/{path_marker}/messages?trace=private",
                data=request_body,
                headers={
                    "Authorization": "Bearer lab-secret",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urlopen(request, timeout=3) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.read(), CaptureUpstream.response_body)

            self.assertEqual(CaptureUpstream.received[0]["body"], request_body)
            self.assertEqual(
                CaptureUpstream.received[0]["path"],
                f"/sessions/{path_marker}/messages?trace=private",
            )
            self.assertEqual(
                CaptureUpstream.received[0]["authorization"],
                "Bearer lab-secret",
            )

            metrics_text = read_metrics(metrics_path)
            self.assertNotIn(secret_marker, metrics_text)
            self.assertNotIn("lab-secret", metrics_text)
            self.assertNotIn("trace=private", metrics_text)
            self.assertNotIn(path_marker, metrics_text)
            record = json.loads(metrics_text)
            self.assertEqual(
                set(record),
                {
                    "duration_ms",
                    "error_class",
                    "method",
                    "request_bytes",
                    "request_id",
                    "response_bytes",
                    "route_class",
                    "status",
                    "ts",
                },
            )
            self.assertEqual(record["route_class"], "other")
            self.assertEqual(record["request_bytes"], len(request_body))
            self.assertEqual(record["response_bytes"], len(CaptureUpstream.response_body))
            self.assertEqual(record["status"], 200)
            self.assertIsNone(record["error_class"])
            self.assertEqual(metrics_path.stat().st_mode & 0o777, 0o600)

    def test_route_classes_are_bounded(self) -> None:
        self.assertEqual(classify_route("/v1/chat/completions?trace=private"), "chat_completions")
        self.assertEqual(classify_route("/sessions/private-path-marker/messages"), "other")

    def test_existing_metrics_file_is_restricted_before_append(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_path = Path(tmpdir) / "metrics.jsonl"
            metrics_path.write_text("", encoding="utf-8")
            metrics_path.chmod(0o644)

            JsonlMetrics(metrics_path).write({"route_class": "health", "status": 200})

            self.assertEqual(metrics_path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(json.loads(metrics_path.read_text(encoding="utf-8"))["status"], 200)

    def test_upstream_failure_returns_502_without_logging_exception_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_path = Path(tmpdir) / "metrics.jsonl"
            unused = socket.socket()
            unused.bind(("127.0.0.1", 0))
            unused_port = unused.getsockname()[1]
            unused.close()

            parsed = parse_upstream(f"http://127.0.0.1:{unused_port}")
            proxy_handler = make_proxy_handler(parsed, JsonlMetrics(metrics_path), timeout=0.5)
            proxy, proxy_thread = start_server(proxy_handler)
            self.addCleanup(proxy.shutdown)
            self.addCleanup(proxy.server_close)
            self.addCleanup(proxy_thread.join, 1)

            request = Request(
                f"http://127.0.0.1:{proxy.server_port}/v1/models",
                data=b"sensitive failure payload",
                method="POST",
            )
            with self.assertRaises(HTTPError) as raised:
                urlopen(request, timeout=3)
            self.assertEqual(raised.exception.code, 502)

            metrics_text = read_metrics(metrics_path)
            self.assertNotIn("sensitive failure payload", metrics_text)
            self.assertNotIn(str(unused_port), metrics_text)
            record = json.loads(metrics_text)
            self.assertEqual(record["status"], 502)
            self.assertIsNotNone(record["error_class"])

    def test_remote_upstream_requires_explicit_opt_in(self) -> None:
        with self.assertRaisesRegex(ValueError, "--allow-remote-upstream"):
            parse_upstream("https://example.invalid:443")

    def test_upstream_user_information_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not include user information"):
            parse_upstream("http://invented-user:invented-secret@127.0.0.1:18081")


if __name__ == "__main__":
    unittest.main()
