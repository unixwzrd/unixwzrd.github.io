#!/usr/bin/env python3
"""Tests for the rendered article TTS helper."""

from __future__ import annotations

import http.server
import io
import json
import shutil
import tempfile
import threading
import unittest
import wave
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import requests

from utils.bin.article_tts import (
    BrowserRelayConfig,
    BrowserRelayServer,
    DEFAULT_BROWSER_ORIGINS,
    chunk_blocks,
    extract_article,
    join_audio,
    main,
    make_browser_relay_handler,
    speech_endpoint,
    synthesize_chunk,
)

SAMPLE_HTML = """
<!doctype html>
<html>
  <body>
    <header><h1 class="post-title">A Useful Test</h1></header>
    <div class="post-content e-content">
      <aside class="series-context">Part nine. Previous article.</aside>
      <p>This paragraph keeps <a href="https://example.invalid/private">useful linked words</a> but never reads the URL.</p>
      <h2>Working Boundary</h2>
      <p>Inline <code>Dashboard</code>, <code>reference_id</code>, and <code>restart_policy=never</code> remain readable.</p>
      <p>A raw link such as <a href="https://example.invalid/raw">https://example.invalid/raw</a> is not spoken.</p>
      <figure><img src="diagram.svg" alt="A very long diagram description"><figcaption>Open the diagram.</figcaption></figure>
      <table><tr><td>Table material should not be spoken.</td></tr></table>
      <pre><code>print("code should not be spoken")</code></pre>
      <details><summary>View source</summary><p>Source disclosure should not be spoken.</p></details>
      <blockquote><p>A quoted paragraph remains article prose.</p></blockquote>
      <nav class="series-navigation">Next article.</nav>
      <section class="post-engagement"><p>Support this work.</p></section>
    </div>
  </body>
</html>
"""


class ExtractArticleTests(unittest.TestCase):
    def test_keeps_article_prose_without_special_blocks_or_urls(self) -> None:
        article = extract_article(SAMPLE_HTML)
        text = article.text

        self.assertIn("A Useful Test.", text)
        self.assertIn("useful linked words", text)
        self.assertIn("Working Boundary.", text)
        self.assertIn("Inline Dashboard, reference id, and restart policy equals never remain readable.", text)
        self.assertIn("A raw link such as is not spoken.", text)
        self.assertIn("A quoted paragraph remains article prose.", text)
        self.assertNotIn("https://", text)
        self.assertNotIn("diagram description", text)
        self.assertNotIn("Table material", text)
        self.assertNotIn("code should", text)
        self.assertNotIn("Source disclosure", text)
        self.assertNotIn("Next article", text)
        self.assertNotIn("Support this work", text)
        self.assertNotIn("<", text)

    def test_can_omit_title(self) -> None:
        article = extract_article(SAMPLE_HTML, include_title=False)
        self.assertNotIn("A Useful Test", article.text)

    def test_missing_article_selector_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "article selector not found"):
            extract_article("<p>no article wrapper</p>")


class ChunkArticleTests(unittest.TestCase):
    def test_packs_blocks_and_respects_limit(self) -> None:
        blocks = (
            "First sentence introduces the article. " * 4,
            "Second sentence develops the example. " * 4,
            "Third sentence finishes the example. " * 4,
        )
        chunks = chunk_blocks(blocks, max_chars=200)

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 200 for chunk in chunks))
        self.assertEqual(" ".join(" ".join(chunks).split()), " ".join(" ".join(blocks).split()))

    def test_rejects_unreasonably_small_chunk_limit(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 200"):
            chunk_blocks(["Text."], max_chars=100)


class SpeechEndpointTests(unittest.TestCase):
    def test_builds_endpoint_from_root_or_v1(self) -> None:
        self.assertEqual(speech_endpoint("http://127.0.0.1:11440"), "http://127.0.0.1:11440/v1/audio/speech")
        self.assertEqual(speech_endpoint("http://127.0.0.1:11440/v1"), "http://127.0.0.1:11440/v1/audio/speech")

    def test_preserves_full_endpoint(self) -> None:
        endpoint = "http://127.0.0.1:11440/v1/audio/speech"
        self.assertEqual(speech_endpoint(endpoint), endpoint)

    def test_rejects_non_http_endpoint(self) -> None:
        with self.assertRaisesRegex(ValueError, "absolute HTTP"):
            speech_endpoint("localhost:11440")


def tiny_wav() -> bytes:
    output = io.BytesIO()
    with wave.open(output, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        wav_file.writeframes(b"\x00\x00" * 160)
    return output.getvalue()


class FakeAudioResponse:
    def __init__(self) -> None:
        self.status_code = 200
        self.headers = {"Content-Type": "audio/wav"}
        self.content = tiny_wav()
        self.text = ""


class FakeSession:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object], float]] = []

    def post(self, endpoint: str, *, json: dict[str, object], timeout: float) -> FakeAudioResponse:
        self.calls.append((endpoint, json, timeout))
        return FakeAudioResponse()


class FakePageResponse:
    text = SAMPLE_HTML

    def raise_for_status(self) -> None:
        return None


class FakePageSession:
    def __init__(self) -> None:
        self.headers: dict[str, str] = {}

    def get(self, _url: str, *, timeout: float) -> FakePageResponse:
        self.timeout = timeout
        return FakePageResponse()


class AudioArtifactTests(unittest.TestCase):
    def test_saves_valid_bridge_wav_and_payload(self) -> None:
        session = FakeSession()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "chunk.wav"
            synthesize_chunk(
                session,
                "http://127.0.0.1:11440/v1/audio/speech",
                "Article prose only.",
                output,
                voice="narrator",
                model=None,
                timeout=30.0,
            )

            self.assertEqual(output.read_bytes(), tiny_wav())
            self.assertEqual(session.calls[0][1], {"input": "Article prose only.", "response_format": "wav", "voice": "narrator"})

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg is required")
    def test_joins_wav_chunks_and_creates_mp3(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory)
            first = output_dir / "0001.wav"
            second = output_dir / "0002.wav"
            first.write_bytes(tiny_wav())
            second.write_bytes(tiny_wav())

            wav_path, mp3_path = join_audio([first, second], output_dir)

            self.assertTrue(wav_path.is_file())
            self.assertTrue(mp3_path.is_file())
            self.assertGreater(wav_path.stat().st_size, len(tiny_wav()))
            self.assertGreater(mp3_path.stat().st_size, 0)


class BrowserRelayTests(unittest.TestCase):
    def test_default_origins_include_local_jekyll_and_safari_webreader(self) -> None:
        self.assertIn("http://127.0.0.1:4000", DEFAULT_BROWSER_ORIGINS)
        self.assertIn("http://localhost:4000", DEFAULT_BROWSER_ORIGINS)
        self.assertIn("safari-web-extension://*", DEFAULT_BROWSER_ORIGINS)

    def test_relays_allowed_browser_audio_without_exposing_bridge_configuration(self) -> None:
        received: list[dict[str, object]] = []

        class UpstreamHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, _format: str, *_args: object) -> None:
                return

            def do_POST(self) -> None:
                length = int(self.headers["Content-Length"])
                received.append(json.loads(self.rfile.read(length)))
                audio = tiny_wav()
                self.send_response(200)
                self.send_header("Content-Type", "audio/wav")
                self.send_header("Content-Length", str(len(audio)))
                self.end_headers()
                self.wfile.write(audio)

        upstream = BrowserRelayServer(("127.0.0.1", 0), UpstreamHandler)
        upstream_thread = threading.Thread(target=upstream.serve_forever, daemon=True)
        upstream_thread.start()
        upstream_url = f"http://127.0.0.1:{upstream.server_port}/v1/audio/speech"

        config = BrowserRelayConfig(
            endpoint=upstream_url,
            voice="review-voice",
            model=None,
            timeout=5.0,
            allowed_origins=frozenset({"http://127.0.0.1:4000", "safari-web-extension://*"}),
        )
        relay = BrowserRelayServer(("127.0.0.1", 0), make_browser_relay_handler(config))
        relay_thread = threading.Thread(target=relay.serve_forever, daemon=True)
        relay_thread.start()
        relay_url = f"http://127.0.0.1:{relay.server_port}"
        allowed_headers = {"Origin": "http://127.0.0.1:4000"}

        try:
            health = requests.get(f"{relay_url}/health", headers=allowed_headers, timeout=5)
            self.assertEqual(health.status_code, 200)
            self.assertNotIn(upstream_url, health.text)
            self.assertNotIn("review-voice", health.text)

            preflight = requests.options(
                f"{relay_url}/v1/audio/speech",
                headers={**allowed_headers, "Access-Control-Request-Private-Network": "true"},
                timeout=5,
            )
            self.assertEqual(preflight.status_code, 204)
            self.assertEqual(preflight.headers["Access-Control-Allow-Private-Network"], "true")

            response = requests.post(
                f"{relay_url}/v1/audio/speech",
                headers=allowed_headers,
                json={"input": "Only this selected paragraph."},
                timeout=5,
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, tiny_wav())
            self.assertEqual(
                received,
                [{"input": "Only this selected paragraph.", "response_format": "wav", "voice": "review-voice"}],
            )

            extension_response = requests.post(
                f"{relay_url}/v1/audio/speech",
                headers={"Origin": "safari-web-extension://personal-webreader"},
                json={"input": "Read through the extension."},
                timeout=5,
            )
            self.assertEqual(extension_response.status_code, 200)
            self.assertEqual(extension_response.headers["Access-Control-Allow-Origin"], "safari-web-extension://personal-webreader")

            denied = requests.post(
                f"{relay_url}/v1/audio/speech",
                headers={"Origin": "https://example.invalid"},
                json={"input": "Do not relay this."},
                timeout=5,
            )
            self.assertEqual(denied.status_code, 403)
            self.assertEqual(len(received), 2)
        finally:
            relay.shutdown()
            relay.server_close()
            upstream.shutdown()
            upstream.server_close()


class CliArtifactTests(unittest.TestCase):
    def test_dry_run_writes_review_artifacts_and_refuses_stale_reuse(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "review"
            with mock.patch("utils.bin.article_tts.requests.Session", return_value=FakePageSession()), redirect_stdout(
                io.StringIO()
            ):
                status = main(["http://127.0.0.1:4000/example/", "--dry-run", "--output-dir", str(output_dir)])
            self.assertEqual(status, 0)
            self.assertTrue((output_dir / "article.txt").is_file())
            self.assertTrue((output_dir / "manifest.json").is_file())
            self.assertTrue(any((output_dir / "chunks").glob("*.txt")))

            with mock.patch("utils.bin.article_tts.requests.Session", return_value=FakePageSession()), redirect_stdout(
                io.StringIO()
            ), redirect_stderr(io.StringIO()):
                stale_status = main(
                    [
                        "http://127.0.0.1:4000/example/",
                        "--dry-run",
                        "--output-dir",
                        str(output_dir),
                        "--max-chars",
                        "1000",
                    ]
                )
            self.assertEqual(stale_status, 2)


if __name__ == "__main__":
    unittest.main()
