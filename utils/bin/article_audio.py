#!/usr/bin/env python3
"""Check and generate public MP3 narration for rendered Jekyll posts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

try:
    from .article_tts import (
        USER_AGENT,
        chunk_blocks,
        extract_article,
        join_audio,
        sha256_text,
        speech_endpoint,
        synthesize_chunk,
        write_json,
    )
except ImportError:
    from article_tts import (
        USER_AGENT,
        chunk_blocks,
        extract_article,
        join_audio,
        sha256_text,
        speech_endpoint,
        synthesize_chunk,
        write_json,
    )

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = REPOSITORY_ROOT / "utils/etc/article-audio.defaults.json"
POST_FILENAME = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.(?:md|markdown|html)$", re.IGNORECASE)


@dataclass(frozen=True)
class AudioConfig:
    site_url: str
    posts_root: Path
    assets_root: Path
    profile: str
    max_chars: int
    page_timeout: float
    tts_timeout: float


@dataclass(frozen=True)
class PostSpec:
    source_path: Path | None
    source_relative: str
    url: str
    category: str
    dated_slug: str

    def audio_path(self, config: AudioConfig) -> Path:
        return config.assets_root / self.category / f"{self.dated_slug}.mp3"

    def manifest_path(self, config: AudioConfig) -> Path:
        return config.assets_root / self.category / f"{self.dated_slug}.audio.json"

    def public_audio_url(self) -> str:
        return f"/assets/audio/blog/{self.category}/{self.dated_slug}.mp3"


@dataclass(frozen=True)
class ArticleSnapshot:
    text: str
    title: str
    chunks: tuple[str, ...]
    sha256: str


def resolve_repository_path(value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (REPOSITORY_ROOT / path).resolve()


def load_config(path: Path) -> AudioConfig:
    payload = json.loads(path.read_text(encoding="utf-8"))
    site_url = str(payload.get("site_url", "http://127.0.0.1:4000")).rstrip("/") + "/"
    return AudioConfig(
        site_url=site_url,
        posts_root=resolve_repository_path(str(payload.get("posts_root", "html/_posts"))),
        assets_root=resolve_repository_path(str(payload.get("assets_root", "html/assets/audio/blog"))),
        profile=str(payload.get("profile", "local-narration-v1")),
        max_chars=int(payload.get("max_chars", 1200)),
        page_timeout=float(payload.get("page_timeout", 20.0)),
        tts_timeout=float(payload.get("tts_timeout", 300.0)),
    )


def read_front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing YAML front matter: {path}")
    try:
        raw = text.split("\n---\n", 1)[0][4:]
    except IndexError as exc:
        raise ValueError(f"unterminated YAML front matter: {path}") from exc

    values: dict[str, str] = {}
    for line in raw.splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def first_category(raw: str) -> str:
    value = raw.strip().strip("[]")
    category = value.split(",", 1)[0].strip().strip('"\'')
    return category or "blog"


def post_spec_from_source(path: Path, config: AudioConfig) -> PostSpec | None:
    match = POST_FILENAME.match(path.name)
    if not match:
        return None
    front = read_front_matter(path)
    if front.get("published", "true").lower() == "false":
        return None

    file_year, file_month, file_day, slug = match.groups()
    date_match = re.match(r"^(\d{4})-(\d{2})-(\d{2})", front.get("date", ""))
    year, month, day = date_match.groups() if date_match else (file_year, file_month, file_day)
    category = first_category(front.get("categories", front.get("category", "blog")))
    permalink = front.get("permalink")
    route = permalink if permalink else f"/{category}/{year}/{month}/{day}/{slug}/"
    if not route.startswith("/"):
        route = "/" + route

    try:
        source_relative = path.resolve().relative_to(REPOSITORY_ROOT).as_posix()
    except ValueError:
        source_relative = path.name
    return PostSpec(
        source_path=path.resolve(),
        source_relative=source_relative,
        url=urljoin(config.site_url, route.lstrip("/")),
        category=re.sub(r"[^a-z0-9-]+", "-", category.lower()).strip("-") or "blog",
        dated_slug=f"{year}-{month}-{day}-{slug.lower()}",
    )


def discover_posts(config: AudioConfig) -> list[PostSpec]:
    posts: list[PostSpec] = []
    for path in sorted(config.posts_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".markdown", ".html"}:
            continue
        spec = post_spec_from_source(path, config)
        if spec is not None:
            posts.append(spec)
    return posts


def direct_url_spec(url: str, config: AudioConfig) -> PostSpec:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    category = re.sub(r"[^a-z0-9-]+", "-", (parts[0] if parts else "blog").lower()).strip("-") or "blog"
    leaf = parts[-1] if parts else "article"
    date_parts = parts[1:4] if len(parts) >= 5 and all(re.fullmatch(r"\d+", part) for part in parts[1:4]) else []
    dated_slug = "-".join([*date_parts, leaf]).lower() if date_parts else leaf.lower()
    dated_slug = re.sub(r"[^a-z0-9-]+", "-", dated_slug).strip("-") or "article"
    return PostSpec(None, "(URL target)", url, category, dated_slug)


def select_posts(targets: list[str], all_posts: bool, config: AudioConfig) -> list[PostSpec]:
    discovered = discover_posts(config)
    if all_posts:
        return discovered
    if not targets:
        raise ValueError("provide one or more post source paths or URLs, or use --all")

    selected: list[PostSpec] = []
    by_source = {str(post.source_path): post for post in discovered if post.source_path}
    for target in targets:
        if target.startswith(("http://", "https://")):
            matching = [post for post in discovered if post.url.rstrip("/") == target.rstrip("/")]
            selected.append(matching[0] if matching else direct_url_spec(target, config))
            continue
        source = resolve_repository_path(target)
        spec = by_source.get(str(source)) or post_spec_from_source(source, config)
        if spec is None:
            raise ValueError(f"not a publishable dated post: {target}")
        selected.append(spec)
    return selected


def fetch_snapshot(session: requests.Session, post: PostSpec, config: AudioConfig) -> ArticleSnapshot:
    response = session.get(post.url, timeout=config.page_timeout)
    response.raise_for_status()
    article = extract_article(response.text)
    chunks = tuple(chunk_blocks(article.blocks, max_chars=config.max_chars))
    return ArticleSnapshot(article.text, article.title, chunks, sha256_text(article.text))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def audio_status(post: PostSpec, snapshot: ArticleSnapshot, config: AudioConfig) -> tuple[str, str]:
    audio_path = post.audio_path(config)
    manifest_path = post.manifest_path(config)
    if not audio_path.is_file() or not manifest_path.is_file():
        return "missing", "MP3 or narration manifest is absent"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "stale", "narration manifest cannot be read"

    expected = {
        "schema_version": 1,
        "source_path": post.source_relative,
        "source_url": urlparse(post.url).path,
        "article_sha256": snapshot.sha256,
        "profile": config.profile,
        "max_chars": config.max_chars,
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            return "stale", f"{key} changed"
    if manifest.get("audio_sha256") != file_sha256(audio_path):
        return "stale", "MP3 hash does not match its manifest"
    return "current", "rendered prose and narration profile match"


def generate_audio(
    session: requests.Session,
    post: PostSpec,
    snapshot: ArticleSnapshot,
    config: AudioConfig,
    *,
    bridge: str,
    voice: str | None,
    model: str | None,
) -> None:
    endpoint = speech_endpoint(bridge)
    audio_path = post.audio_path(config)
    manifest_path = post.manifest_path(config)
    audio_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=f"article-audio-{post.dated_slug}-") as directory:
        work = Path(directory)
        chunk_paths: list[Path] = []
        for index, chunk in enumerate(snapshot.chunks, start=1):
            chunk_path = work / f"{index:04d}.wav"
            print(f"  [{index}/{len(snapshot.chunks)}] synthesizing {len(chunk)} characters")
            synthesize_chunk(session, endpoint, chunk, chunk_path, voice=voice, model=model, timeout=config.tts_timeout)
            chunk_paths.append(chunk_path)
        _, joined_mp3 = join_audio(chunk_paths, work)

        staged_audio = audio_path.with_suffix(audio_path.suffix + ".tmp")
        shutil.copyfile(joined_mp3, staged_audio)
        os.replace(staged_audio, audio_path)

    manifest: dict[str, object] = {
        "schema_version": 1,
        "source_path": post.source_relative,
        "source_url": urlparse(post.url).path,
        "title": snapshot.title,
        "article_sha256": snapshot.sha256,
        "audio_sha256": file_sha256(audio_path),
        "profile": config.profile,
        "max_chars": config.max_chars,
        "characters": len(snapshot.text),
        "chunks": len(snapshot.chunks),
        "generated_at": datetime.now(UTC).isoformat(),
    }
    staged_manifest = manifest_path.with_suffix(manifest_path.suffix + ".tmp")
    write_json(staged_manifest, manifest)
    os.replace(staged_manifest, manifest_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check or generate public MP3 narration for rendered Jekyll posts")
    parser.add_argument("targets", nargs="*", help="Post source paths or rendered article URLs")
    parser.add_argument("--all", action="store_true", help="Inspect every publishable file under the configured posts root")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Report current, missing, or stale narration without contacting TTS (default)")
    mode.add_argument("--generate", action="store_true", help="Generate missing or stale MP3 files; unchanged audio is reused")
    parser.add_argument("--force", action="store_true", help="Regenerate selected MP3 files even when their manifests are current")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH, help=f"Workflow defaults (default: {DEFAULT_CONFIG_PATH.relative_to(REPOSITORY_ROOT)})")
    parser.add_argument("--bridge", default=os.environ.get("TTS_BRIDGE_URL"), help="TTS Bridge base URL or speech endpoint (default: TTS_BRIDGE_URL)")
    parser.add_argument("--voice", default=os.environ.get("TTS_BRIDGE_VOICE"), help="Private bridge voice alias (default: TTS_BRIDGE_VOICE; never written to the public manifest)")
    parser.add_argument("--model", default=os.environ.get("TTS_BRIDGE_MODEL"), help="Optional private model override (default: TTS_BRIDGE_MODEL; never written to the public manifest)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config = load_config(args.config.expanduser().resolve())
        posts = select_posts(args.targets, args.all, config)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"article-audio: {exc}", file=sys.stderr)
        return 2

    if args.generate and not args.bridge:
        print("article-audio: --bridge or TTS_BRIDGE_URL is required with --generate", file=sys.stderr)
        return 2

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    unresolved = 0
    for post in posts:
        print(f"{post.source_relative}: {post.url}")
        try:
            snapshot = fetch_snapshot(session, post, config)
            status, reason = audio_status(post, snapshot, config)
            if args.force:
                status, reason = "stale", "forced regeneration requested"
            print(f"  {status}: {reason}")
            if status != "current" and args.generate:
                generate_audio(session, post, snapshot, config, bridge=args.bridge, voice=args.voice, model=args.model)
                status, reason = audio_status(post, snapshot, config)
                print(f"  {status}: {reason}")
                print("  front matter:")
                print(f"    audio: {post.public_audio_url()}")
            if status != "current":
                unresolved += 1
        except (OSError, requests.RequestException, RuntimeError, ValueError) as exc:
            unresolved += 1
            print(f"  error: {exc}", file=sys.stderr)

    current = len(posts) - unresolved
    print(f"article-audio: {current} current, {unresolved} missing, stale, or unavailable")
    return 1 if unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
