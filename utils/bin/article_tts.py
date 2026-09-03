#!/usr/bin/env python3
"""Extract a rendered Jekyll article and send its prose to a TTS bridge."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import http.server
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from socketserver import ThreadingMixIn
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, Tag

DEFAULT_SELECTOR = ".post-content.e-content"
DEFAULT_MAX_CHARS = 1200
DEFAULT_BROWSER_PORT = 11441
DEFAULT_BROWSER_ORIGINS = (
    "http://127.0.0.1:4000",
    "http://localhost:4000",
    "safari-web-extension://*",
)
MAX_BROWSER_REQUEST_BYTES = 64 * 1024
MAX_BROWSER_INPUT_CHARS = 5000
USER_AGENT = "unixwzrd-article-tts/1.0"
BLOCK_TAGS = {"h2", "h3", "h4", "p", "li", "blockquote"}
REMOVE_SELECTORS = (
    "aside",
    "nav",
    "figure",
    "table",
    "pre",
    "details",
    "script",
    "style",
    "noscript",
    "audio",
    "video",
    "button",
    "form",
    ".series-context",
    ".series-navigation",
    ".post-engagement",
    ".content-footer",
    ".support-section",
    ".post-comments",
    ".blog-diagram",
    "[aria-hidden='true']",
)
SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9'\"])")
WHITESPACE = re.compile(r"\s+")
SPACE_BEFORE_PUNCTUATION = re.compile(r"\s+([,.;:!?])")
SPACE_AFTER_OPENING_PUNCTUATION = re.compile(r"([(\[])\s+")
SPACE_BEFORE_CLOSING_PUNCTUATION = re.compile(r"\s+([)\]])")
SAFE_SLUG = re.compile(r"[^A-Za-z0-9._-]+")


@dataclass(frozen=True)
class ExtractedArticle:
    title: str
    blocks: tuple[str, ...]

    @property
    def text(self) -> str:
        return "\n\n".join(self.blocks).strip() + "\n"


@dataclass(frozen=True)
class BrowserRelayConfig:
    endpoint: str
    voice: str | None
    model: str | None
    timeout: float
    allowed_origins: frozenset[str]


def clean_spoken_text(value: str) -> str:
    """Normalize rendered text without turning punctuation into spoken markup."""
    text = unicodedata.normalize("NFKC", value)
    replacements = {
        "\u00a0": " ",
        "\u200b": "",
        "\u200c": "",
        "\u200d": "",
        "\ufeff": "",
        "&": " and ",
        "→": " ",
        "←": " ",
        "↔": " ",
        "•": " ",
        "_": " ",
        "/": " ",
        "=": " equals ",
        "+": " plus ",
        "|": " ",
        "`": "",
        "*": "",
    }
    for source, replacement in replacements.items():
        text = text.replace(source, replacement)
    text = WHITESPACE.sub(" ", text).strip()
    text = SPACE_BEFORE_PUNCTUATION.sub(r"\1", text)
    text = SPACE_AFTER_OPENING_PUNCTUATION.sub(r"\1", text)
    return SPACE_BEFORE_CLOSING_PUNCTUATION.sub(r"\1", text)


def _is_nested_block(node: Tag, root: Tag) -> bool:
    parent = node.parent
    while isinstance(parent, Tag) and parent is not root:
        if parent.name in BLOCK_TAGS:
            return True
        parent = parent.parent
    return False


def extract_article(html: str, selector: str = DEFAULT_SELECTOR, include_title: bool = True) -> ExtractedArticle:
    """Extract readable prose from the rendered article body."""
    soup = BeautifulSoup(html, "html.parser")
    root = soup.select_one(selector)
    if root is None:
        raise ValueError(f"article selector not found: {selector}")

    title_node = soup.select_one(".post-title") or soup.find("h1")
    title = clean_spoken_text(title_node.get_text(" ", strip=True)) if title_node else "Article"

    for remove_selector in REMOVE_SELECTORS:
        for node in root.select(remove_selector):
            node.decompose()

    for image in root.find_all("img"):
        image.decompose()
    for link in root.find_all("a"):
        visible = link.get_text(" ", strip=True)
        href = str(link.get("href", "")).strip()
        if visible.startswith(("http://", "https://", "www.")) or visible == href:
            link.decompose()
        else:
            link.unwrap()
    for line_break in root.find_all("br"):
        line_break.replace_with(" ")

    blocks: list[str] = []
    if include_title and title:
        blocks.append(title.rstrip(".!?") + ".")

    for node in root.find_all(tuple(BLOCK_TAGS)):
        if _is_nested_block(node, root):
            continue
        text = clean_spoken_text(node.get_text(" ", strip=True))
        if not text:
            continue
        if node.name in {"h2", "h3", "h4"} and text[-1:] not in ".!?":
            text += "."
        if not blocks or blocks[-1] != text:
            blocks.append(text)

    if not blocks:
        raise ValueError("article body contained no readable prose")
    return ExtractedArticle(title=title, blocks=tuple(blocks))


def _split_long_text(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    sentences = SENTENCE_BOUNDARY.split(text)
    pieces: list[str] = []
    current = ""
    for sentence in sentences:
        if len(sentence) > max_chars:
            if current:
                pieces.append(current)
                current = ""
            words = sentence.split()
            word_piece = ""
            for word in words:
                candidate = f"{word_piece} {word}".strip()
                if word_piece and len(candidate) > max_chars:
                    pieces.append(word_piece)
                    word_piece = word
                else:
                    word_piece = candidate
            if word_piece:
                pieces.append(word_piece)
            continue

        candidate = f"{current} {sentence}".strip()
        if current and len(candidate) > max_chars:
            pieces.append(current)
            current = sentence
        else:
            current = candidate
    if current:
        pieces.append(current)
    return pieces


def chunk_blocks(blocks: tuple[str, ...] | list[str], max_chars: int = DEFAULT_MAX_CHARS) -> list[str]:
    """Pack article blocks without splitting a sentence unless it is oversized."""
    if max_chars < 200:
        raise ValueError("max_chars must be at least 200")

    chunks: list[str] = []
    current = ""
    for block in blocks:
        for piece in _split_long_text(block, max_chars):
            candidate = f"{current}\n\n{piece}".strip()
            if current and len(candidate) > max_chars:
                chunks.append(current)
                current = piece
            else:
                current = candidate
    if current:
        chunks.append(current)
    return chunks


def speech_endpoint(bridge_url: str) -> str:
    value = bridge_url.rstrip("/")
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("bridge URL must be an absolute HTTP or HTTPS URL")
    if parsed.path.endswith("/v1/audio/speech") or parsed.path.endswith("/audio/speech"):
        return value
    if parsed.path.endswith("/v1"):
        return value + "/audio/speech"
    return value + "/v1/audio/speech"


def safe_slug(url: str) -> str:
    parsed = urlparse(url)
    candidate = Path(parsed.path.rstrip("/")).name or "article"
    slug = SAFE_SLUG.sub("-", candidate).strip("-.")
    return slug or "article"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_json(path: Path, payload: dict[str, object]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def synthesize_chunk(
    session: requests.Session,
    endpoint: str,
    text: str,
    output_path: Path,
    *,
    voice: str | None,
    model: str | None,
    timeout: float,
) -> None:
    payload: dict[str, object] = {"input": text, "response_format": "wav"}
    if voice:
        payload["voice"] = voice
    if model:
        payload["model"] = model

    response = session.post(endpoint, json=payload, timeout=timeout)
    if response.status_code >= 400:
        bounded = response.text[:500].replace("\n", " ")
        raise RuntimeError(f"TTS request failed with HTTP {response.status_code}: {bounded}")
    content_type = response.headers.get("Content-Type", "").lower()
    if "json" in content_type:
        raise RuntimeError(f"TTS response was JSON rather than audio: {response.text[:500]}")
    if not response.content.startswith(b"RIFF") or response.content[8:12] != b"WAVE":
        raise RuntimeError(f"TTS response was not a WAV file (Content-Type: {content_type or 'unknown'})")

    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary.write_bytes(response.content)
    temporary.replace(output_path)


def make_browser_relay_handler(config: BrowserRelayConfig) -> type[http.server.BaseHTTPRequestHandler]:
    """Create a loopback relay handler without exposing bridge configuration."""

    class BrowserRelayHandler(http.server.BaseHTTPRequestHandler):
        server_version = "ArticleTTSRelay/1.0"

        def log_message(self, format_string: str, *args: object) -> None:
            sys.stderr.write("article-tts relay: " + format_string % args + "\n")

        def _origin_allowed(self) -> bool:
            origin = self.headers.get("Origin", "")
            return any(fnmatch.fnmatchcase(origin, pattern) for pattern in config.allowed_origins)

        def _cors_headers(self) -> None:
            origin = self.headers.get("Origin", "")
            if any(fnmatch.fnmatchcase(origin, pattern) for pattern in config.allowed_origins):
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Vary", "Origin")
            if self.headers.get("Access-Control-Request-Private-Network", "").lower() == "true":
                self.send_header("Access-Control-Allow-Private-Network", "true")

        def _send_json(self, status: int, payload: dict[str, object]) -> None:
            body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
            self.send_response(status)
            self._cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def do_OPTIONS(self) -> None:
            if self.path not in {"/health", "/v1/audio/speech"}:
                self.send_error(404)
                return
            if not self._origin_allowed():
                self.send_error(403)
                return
            self.send_response(204)
            self._cors_headers()
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Max-Age", "600")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()

        def do_GET(self) -> None:
            if self.path != "/health":
                self.send_error(404)
                return
            if not self._origin_allowed():
                self.send_error(403)
                return
            self._send_json(200, {"status": "ok", "service": "article-tts-browser-relay"})

        def do_POST(self) -> None:
            if self.path != "/v1/audio/speech":
                self.send_error(404)
                return
            if not self._origin_allowed():
                self.send_error(403)
                return

            try:
                content_length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self._send_json(400, {"error": "invalid Content-Length"})
                return
            if content_length < 1 or content_length > MAX_BROWSER_REQUEST_BYTES:
                self._send_json(413, {"error": "request body is empty or too large"})
                return

            try:
                request_payload = json.loads(self.rfile.read(content_length))
            except (json.JSONDecodeError, UnicodeDecodeError):
                self._send_json(400, {"error": "request body must be JSON"})
                return
            text = request_payload.get("input") if isinstance(request_payload, dict) else None
            if not isinstance(text, str) or not text.strip():
                self._send_json(400, {"error": "input must be a non-empty string"})
                return
            if len(text) > MAX_BROWSER_INPUT_CHARS:
                self._send_json(413, {"error": f"input exceeds {MAX_BROWSER_INPUT_CHARS} characters"})
                return

            payload: dict[str, object] = {"input": text, "response_format": "wav"}
            if config.voice:
                payload["voice"] = config.voice
            if config.model:
                payload["model"] = config.model

            try:
                response = requests.post(config.endpoint, json=payload, timeout=config.timeout)
                response.raise_for_status()
            except requests.RequestException as exc:
                self.log_error("bridge request failed for %d characters: %s", len(text), exc)
                self._send_json(502, {"error": "TTS Bridge request failed"})
                return

            content_type = response.headers.get("Content-Type", "audio/wav")
            if "json" in content_type.lower() or not response.content:
                self.log_error("bridge returned non-audio data for %d characters", len(text))
                self._send_json(502, {"error": "TTS Bridge did not return audio"})
                return

            self.send_response(200)
            self._cors_headers()
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(response.content)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            try:
                self.wfile.write(response.content)
            except (BrokenPipeError, ConnectionResetError):
                self.log_message("browser stopped playback after %d characters", len(text))

    return BrowserRelayHandler


class BrowserRelayServer(ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


def run_browser_server(
    bridge_url: str,
    *,
    voice: str | None,
    model: str | None,
    timeout: float,
    listen_host: str,
    listen_port: int,
    allowed_origins: tuple[str, ...],
) -> None:
    if listen_host not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("browser relay must listen on a loopback address")
    config = BrowserRelayConfig(
        endpoint=speech_endpoint(bridge_url),
        voice=voice,
        model=model,
        timeout=timeout,
        allowed_origins=frozenset(origin.rstrip("/") for origin in allowed_origins),
    )
    server = BrowserRelayServer((listen_host, listen_port), make_browser_relay_handler(config))
    print(f"Article TTS browser relay listening on http://{listen_host}:{server.server_port}")
    print("Allowed origins: " + ", ".join(sorted(config.allowed_origins)))
    print("Audio is relayed from memory and is not written to disk. Press Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def ffmpeg_concat_entry(path: Path) -> str:
    escaped = str(path.resolve()).replace("'", "'\\''")
    return f"file '{escaped}'"


def join_audio(chunk_paths: list[Path], output_dir: Path) -> tuple[Path, Path]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required to join article audio")

    concat_path = output_dir / "concat.txt"
    concat_path.write_text("\n".join(ffmpeg_concat_entry(path) for path in chunk_paths) + "\n", encoding="utf-8")
    wav_path = output_dir / "article.wav"
    mp3_path = output_dir / "article.mp3"

    subprocess.run(
        [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_path), "-c:a", "pcm_s16le", str(wav_path)],
        check=True,
    )
    subprocess.run(
        [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(wav_path), "-vn", "-ac", "1", "-b:a", "96k", str(mp3_path)],
        check=True,
    )
    return wav_path, mp3_path


def print_dry_run(article: ExtractedArticle, chunks: list[str]) -> None:
    print(article.text.rstrip())
    print(f"\nExtracted {len(article.text)} characters into {len(chunks)} chunk(s).")
    for index, chunk in enumerate(chunks, start=1):
        print(f"  {index:03d}: {len(chunk)} characters")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read the prose of a rendered Jekyll post through a TTS Bridge")
    parser.add_argument("url", nargs="?", help="Rendered local or remote article URL")
    parser.add_argument("--bridge", default=os.environ.get("TTS_BRIDGE_URL"), help="TTS Bridge base URL or speech endpoint (default: TTS_BRIDGE_URL)")
    parser.add_argument("--voice", default=os.environ.get("TTS_BRIDGE_VOICE"), help="Configured bridge voice alias (default: TTS_BRIDGE_VOICE)")
    parser.add_argument("--model", default=None, help="Optional model override")
    parser.add_argument("--selector", default=DEFAULT_SELECTOR, help=f"Article-body CSS selector (default: {DEFAULT_SELECTOR})")
    parser.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS, help=f"Maximum characters per speech request (default: {DEFAULT_MAX_CHARS})")
    parser.add_argument("--page-timeout", type=float, default=20.0, help="Rendered-page request timeout in seconds")
    parser.add_argument("--tts-timeout", type=float, default=300.0, help="Per-chunk TTS request timeout in seconds")
    parser.add_argument("--output-dir", type=Path, help="Artifact directory; default is a new system temporary directory")
    parser.add_argument("--dry-run", action="store_true", help="Print extracted prose and chunk sizes without calling TTS")
    parser.add_argument("--play", action="store_true", help="Play each completed WAV chunk with afplay")
    parser.add_argument("--no-title", action="store_true", help="Do not speak the article title")
    parser.add_argument("--browser-server", action="store_true", help="Run the loopback relay used by the development-only post player")
    parser.add_argument("--listen-host", default="127.0.0.1", help="Browser relay listen address; loopback only (default: 127.0.0.1)")
    parser.add_argument("--listen-port", type=int, default=DEFAULT_BROWSER_PORT, help=f"Browser relay listen port (default: {DEFAULT_BROWSER_PORT})")
    parser.add_argument("--allow-origin", action="append", help="Allowed browser origin pattern; may be repeated (defaults to local Jekyll and Safari WebReader origins)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.browser_server:
        if not args.bridge:
            print("article-tts: --bridge or TTS_BRIDGE_URL is required for --browser-server", file=sys.stderr)
            return 2
        try:
            run_browser_server(
                args.bridge,
                voice=args.voice,
                model=args.model,
                timeout=args.tts_timeout,
                listen_host=args.listen_host,
                listen_port=args.listen_port,
                allowed_origins=tuple(args.allow_origin or DEFAULT_BROWSER_ORIGINS),
            )
        except (OSError, ValueError) as exc:
            print(f"article-tts: {exc}", file=sys.stderr)
            return 1
        return 0
    if not args.url:
        print("article-tts: an article URL is required unless --browser-server is used", file=sys.stderr)
        return 2

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    try:
        page_response = session.get(args.url, timeout=args.page_timeout)
        page_response.raise_for_status()
        article = extract_article(page_response.text, selector=args.selector, include_title=not args.no_title)
        chunks = chunk_blocks(article.blocks, max_chars=args.max_chars)
    except (requests.RequestException, ValueError) as exc:
        print(f"article-tts: {exc}", file=sys.stderr)
        return 1

    if args.dry_run and args.output_dir is None:
        print_dry_run(article, chunks)
        return 0
    if not args.dry_run and not args.bridge:
        print("article-tts: --bridge or TTS_BRIDGE_URL is required unless --dry-run is used", file=sys.stderr)
        return 2

    output_dir = args.output_dir
    if output_dir is None:
        output_dir = Path(tempfile.mkdtemp(prefix=f"article-tts-{safe_slug(args.url)}-"))
    output_dir = output_dir.expanduser().resolve()
    chunk_records: list[dict[str, object]] = []
    for index, chunk in enumerate(chunks, start=1):
        text_name = f"{index:04d}.txt"
        audio_name = f"{index:04d}.wav"
        chunk_records.append(
            {
                "index": index,
                "characters": len(chunk),
                "sha256": sha256_text(chunk),
                "text_file": f"chunks/{text_name}",
                "audio_file": f"chunks/{audio_name}",
                "complete": False,
            }
        )

    manifest: dict[str, object] = {
        "schema_version": 1,
        "source_url": args.url,
        "title": article.title,
        "selector": args.selector,
        "article_sha256": sha256_text(article.text),
        "max_chars": args.max_chars,
        "voice": args.voice or "bridge-default",
        "model": args.model or "bridge-default",
        "chunks": chunk_records,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    chunks_dir = output_dir / "chunks"
    manifest_path = output_dir / "manifest.json"
    if manifest_path.is_file():
        try:
            existing_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"article-tts: cannot read existing manifest: {exc}", file=sys.stderr)
            return 2
        identity_fields = ("schema_version", "source_url", "article_sha256", "max_chars", "voice", "model")
        identity_matches = all(existing_manifest.get(field) == manifest.get(field) for field in identity_fields)
        existing_hashes = [record.get("sha256") for record in existing_manifest.get("chunks", [])]
        current_hashes = [record["sha256"] for record in chunk_records]
        if not identity_matches or existing_hashes != current_hashes:
            print("article-tts: output directory contains artifacts for different article text or synthesis settings", file=sys.stderr)
            print("Choose a new --output-dir to avoid reusing stale audio.", file=sys.stderr)
            return 2
    elif any(output_dir.iterdir()):
        print("article-tts: output directory is not empty and has no compatible manifest", file=sys.stderr)
        return 2

    chunks_dir.mkdir(exist_ok=True)
    article_path = output_dir / "article.txt"
    article_path.write_text(article.text, encoding="utf-8")
    for index, chunk in enumerate(chunks, start=1):
        (chunks_dir / f"{index:04d}.txt").write_text(chunk.rstrip() + "\n", encoding="utf-8")
        chunk_records[index - 1]["complete"] = (chunks_dir / f"{index:04d}.wav").is_file()
    write_json(manifest_path, manifest)

    if args.dry_run:
        print_dry_run(article, chunks)
        print(f"Artifacts: {output_dir}")
        return 0

    try:
        endpoint = speech_endpoint(args.bridge)
        player = shutil.which("afplay") if args.play else None
        if args.play and player is None:
            raise RuntimeError("afplay was not found")

        audio_paths: list[Path] = []
        for index, (chunk, record) in enumerate(zip(chunks, chunk_records, strict=True), start=1):
            audio_path = output_dir / str(record["audio_file"])
            audio_paths.append(audio_path)
            if audio_path.is_file():
                print(f"[{index}/{len(chunks)}] reusing {audio_path.name}")
            else:
                print(f"[{index}/{len(chunks)}] synthesizing {len(chunk)} characters")
                synthesize_chunk(session, endpoint, chunk, audio_path, voice=args.voice, model=args.model, timeout=args.tts_timeout)
                record["complete"] = True
                write_json(manifest_path, manifest)
            if player:
                subprocess.run([player, str(audio_path)], check=True)

        wav_path, mp3_path = join_audio(audio_paths, output_dir)
    except (requests.RequestException, RuntimeError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"article-tts: {exc}", file=sys.stderr)
        print(f"Partial artifacts: {output_dir}", file=sys.stderr)
        return 1

    manifest["joined_wav"] = wav_path.name
    manifest["joined_mp3"] = mp3_path.name
    write_json(manifest_path, manifest)
    print(f"WAV: {wav_path}")
    print(f"MP3: {mp3_path}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
