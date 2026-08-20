#!/usr/bin/env python3
"""Model-free OpenAI-compatible TTS bridge teaching fixture."""

from __future__ import annotations

import io
import json
import math
import struct
import threading
import time
import wave
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib import error, request


FORMAT_FALLBACKS = {"ogg": "wav", "opus": "wav"}
REDACTION_MARKER = "<redacted input text>"


def safe_header_value(value: str) -> str:
    """Remove line breaks before writing a value to an HTTP response header."""
    return value.replace("\r", "").replace("\n", "")


def operational_events_redact_inputs(events: list[str], synthesis_inputs: tuple[str, ...]) -> bool:
    event_text = "\n".join(events)
    return REDACTION_MARKER in event_text and all(value not in event_text for value in synthesis_inputs)


def make_tone_wav(path: Path, *, seconds: float = 0.08, frequency: float = 440.0) -> bytes:
    sample_rate = 16_000
    frame_count = int(sample_rate * seconds)
    output = io.BytesIO()
    with wave.open(output, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for frame in range(frame_count):
            value = int(2_000 * math.sin(2.0 * math.pi * frequency * frame / sample_rate))
            wav_file.writeframesraw(struct.pack("<h", value))
    payload = output.getvalue()
    path.write_bytes(payload)
    return payload


@dataclass
class FakeUpstreamState:
    audio_bytes: bytes
    received: list[dict[str, Any]] = field(default_factory=list)
    delay_seconds: float = 0.0
    fail_status: int | None = None


@dataclass
class BridgeConfig:
    upstream_base: str
    samples_dir: Path
    voice_map: dict[str, dict[str, str]]
    timeout_seconds: float = 1.0
    events: list[str] = field(default_factory=list)


class ManagedServer:
    def __init__(self, server: ThreadingHTTPServer):
        self.server = server
        self.thread = threading.Thread(target=server.serve_forever, daemon=True)

    def start(self) -> None:
        self.thread.start()

    @property
    def port(self) -> int:
        return int(self.server.server_address[1])

    def stop(self) -> None:
        self.server.shutdown()
        self.thread.join(timeout=2)
        self.server.server_close()


def normalize_format(requested: str) -> tuple[str, str | None]:
    requested = (requested or "wav").lower()
    delivered = FORMAT_FALLBACKS.get(requested, requested)
    return delivered, requested if delivered != requested else None


def resolve_alias(voice: str, cfg: BridgeConfig) -> tuple[Path, Path] | None:
    entry = cfg.voice_map.get((voice or "").strip().lower())
    if entry is None:
        return None
    sample = (cfg.samples_dir / entry["sample"]).resolve()
    transcript_name = entry.get("ref_text") or sample.with_suffix(".txt").name
    transcript = (cfg.samples_dir / transcript_name).resolve()
    return sample, transcript


def build_upstream_payload(
    incoming: dict[str, Any], cfg: BridgeConfig
) -> tuple[dict[str, Any], str, str | None]:
    text = incoming.get("input")
    if not isinstance(text, str):
        raise ValueError("field 'input' must be a string")

    delivered_format, downgraded_from = normalize_format(
        str(incoming.get("response_format", "wav"))
    )
    output: dict[str, Any] = {
        "input": text,
        "response_format": delivered_format,
    }

    voice = str(incoming.get("voice", ""))
    pair = resolve_alias(voice, cfg)
    if pair is None:
        if voice:
            output["voice"] = voice
    else:
        sample, transcript = pair
        output["ref_audio"] = str(sample)
        output["ref_text"] = str(transcript)

    return output, delivered_format, downgraded_from


class FakeUpstreamHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/health", "/v1/health"):
            payload = json.dumps({"ok": True, "kind": "fake-upstream"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        if self.path not in ("/audio/speech", "/v1/audio/speech"):
            self.send_response(404)
            self.end_headers()
            return

        state: FakeUpstreamState = self.server.state  # type: ignore[attr-defined]
        length = int(self.headers.get("Content-Length", "0"))
        incoming = json.loads(self.rfile.read(length).decode("utf-8"))
        state.received.append(incoming)
        if state.delay_seconds:
            time.sleep(state.delay_seconds)
        if state.fail_status is not None:
            payload = json.dumps({"error": "invented upstream failure"}).encode()
            self.send_response(state.fail_status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        self.send_response(200)
        self.send_header("Content-Type", "audio/wav")
        self.send_header("Content-Length", str(len(state.audio_bytes)))
        self.end_headers()
        self.wfile.write(state.audio_bytes)

    def log_message(self, fmt: str, *args: object) -> None:
        return


class BridgeHandler(BaseHTTPRequestHandler):
    def _json(self, status: int, value: dict[str, Any]) -> None:
        payload = json.dumps(value).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/health", "/v1/health"):
            cfg: BridgeConfig = self.server.config  # type: ignore[attr-defined]
            self._json(
                200,
                {
                    "ok": True,
                    "kind": "teaching-bridge",
                    "upstream": cfg.upstream_base,
                    "voice_alias_count": len(cfg.voice_map),
                },
            )
            return
        self._json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path not in ("/audio/speech", "/v1/audio/speech"):
            self._json(404, {"error": "not_found"})
            return

        cfg: BridgeConfig = self.server.config  # type: ignore[attr-defined]
        length = int(self.headers.get("Content-Length", "0"))
        try:
            incoming = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(incoming, dict):
                raise ValueError("payload must be an object")
            outgoing, delivered_format, downgraded_from = build_upstream_payload(incoming, cfg)
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
            self._json(400, {"error": f"input_validation: {exc}"})
            return

        redacted = dict(outgoing)
        redacted["input"] = REDACTION_MARKER
        cfg.events.append("upstream payload: " + json.dumps(redacted, sort_keys=True))
        body = json.dumps(outgoing).encode()
        req = request.Request(
            cfg.upstream_base.rstrip("/") + "/audio/speech",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=cfg.timeout_seconds) as response:
                response_body = response.read()
                self.send_response(response.status)
                self.send_header("Content-Type", "audio/wav")
                self.send_header("Content-Length", str(len(response_body)))
                if downgraded_from:
                    self.send_header(
                        "X-TTS-Bridge-Requested-Format",
                        safe_header_value(downgraded_from),
                    )
                    self.send_header(
                        "X-TTS-Bridge-Delivered-Format",
                        safe_header_value(delivered_format),
                    )
                self.end_headers()
                self.wfile.write(response_body)
        except error.HTTPError as exc:
            self._json(exc.code, {"error": f"upstream_request: HTTP {exc.code}"})
        except Exception as exc:  # noqa: BLE001
            cfg.events.append("upstream failure: " + type(exc).__name__)
            self._json(502, {"error": "upstream_request: transport failure"})

    def log_message(self, fmt: str, *args: object) -> None:
        return


def make_fake_upstream(state: FakeUpstreamState) -> ManagedServer:
    server = ThreadingHTTPServer(("127.0.0.1", 0), FakeUpstreamHandler)
    server.state = state  # type: ignore[attr-defined]
    return ManagedServer(server)


def make_bridge(config: BridgeConfig) -> ManagedServer:
    server = ThreadingHTTPServer(("127.0.0.1", 0), BridgeHandler)
    server.config = config  # type: ignore[attr-defined]
    return ManagedServer(server)
