#!/usr/bin/env python3
"""Tests for the retained article-audio workflow."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from utils.bin.article_audio import AudioConfig, ArticleSnapshot, audio_status, discover_posts, generate_audio, post_spec_from_source


class ArticleAudioPostTests(unittest.TestCase):
    def config(self, root: Path) -> AudioConfig:
        return AudioConfig(
            site_url="http://127.0.0.1:4000/",
            posts_root=root / "posts",
            assets_root=root / "assets",
            profile="test-profile-v1",
            max_chars=1200,
            page_timeout=20.0,
            tts_timeout=300.0,
        )

    def test_uses_front_matter_date_and_category_for_route(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self.config(root)
            post = config.posts_root / "general" / "2026-01-20-example-post.md"
            post.parent.mkdir(parents=True)
            post.write_text(
                "---\nlayout: post\ndate: 2025-12-31 10:00:00 -0600\ncategories: [general]\n---\n\nBody.\n",
                encoding="utf-8",
            )

            spec = post_spec_from_source(post, config)

            self.assertIsNotNone(spec)
            assert spec is not None
            self.assertEqual(spec.url, "http://127.0.0.1:4000/general/2025/12/31/example-post/")
            self.assertEqual(spec.public_audio_url(), "/assets/audio/blog/general/2025-12-31-example-post.mp3")

    def test_discovers_only_publishable_dated_posts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self.config(root)
            config.posts_root.mkdir(parents=True)
            (config.posts_root / "2026-01-01-live.md").write_text(
                "---\nlayout: post\ndate: 2026-01-01\ncategories: [technology]\n---\n\nLive.\n",
                encoding="utf-8",
            )
            (config.posts_root / "2026-01-02-hidden.md").write_text(
                "---\nlayout: post\ndate: 2026-01-02\ncategories: [technology]\npublished: false\n---\n\nHidden.\n",
                encoding="utf-8",
            )
            (config.posts_root / "2026-01-01-social-posts.txt").write_text("not a post", encoding="utf-8")

            posts = discover_posts(config)

            self.assertEqual([post.dated_slug for post in posts], ["2026-01-01-live"])

    def test_status_detects_current_stale_and_tampered_audio(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self.config(root)
            source = config.posts_root / "2026-01-01-example.md"
            source.parent.mkdir(parents=True)
            source.write_text(
                "---\nlayout: post\ndate: 2026-01-01\ncategories: [technology]\n---\n\nExample.\n",
                encoding="utf-8",
            )
            post = post_spec_from_source(source, config)
            assert post is not None
            snapshot = ArticleSnapshot("Example.\n", "Example", ("Example.",), "article-hash")

            self.assertEqual(audio_status(post, snapshot, config)[0], "missing")
            audio = post.audio_path(config)
            manifest = post.manifest_path(config)
            audio.parent.mkdir(parents=True)
            audio.write_bytes(b"mp3-data")
            payload = {
                "schema_version": 1,
                "source_path": post.source_relative,
                "source_url": "/technology/2026/01/01/example/",
                "article_sha256": snapshot.sha256,
                "audio_sha256": __import__("hashlib").sha256(b"mp3-data").hexdigest(),
                "profile": config.profile,
                "max_chars": config.max_chars,
            }
            manifest.write_text(json.dumps(payload), encoding="utf-8")

            self.assertEqual(audio_status(post, snapshot, config)[0], "current")
            changed = ArticleSnapshot(snapshot.text, snapshot.title, snapshot.chunks, "changed-hash")
            self.assertEqual(audio_status(post, changed, config), ("stale", "article_sha256 changed"))
            audio.write_bytes(b"tampered")
            self.assertEqual(audio_status(post, snapshot, config), ("stale", "MP3 hash does not match its manifest"))

    def test_generation_keeps_private_voice_and_model_out_of_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self.config(root)
            source = config.posts_root / "2026-01-01-example.md"
            source.parent.mkdir(parents=True)
            source.write_text(
                "---\nlayout: post\ndate: 2026-01-01\ncategories: [technology]\n---\n\nExample.\n",
                encoding="utf-8",
            )
            post = post_spec_from_source(source, config)
            assert post is not None
            snapshot = ArticleSnapshot("Example.\n", "Example", ("Example.",), "article-hash")

            def fake_synthesize(_session, _endpoint, _text, output, **_kwargs):
                output.write_bytes(b"wav")

            def fake_join(_chunks, output_dir):
                wav = output_dir / "article.wav"
                mp3 = output_dir / "article.mp3"
                wav.write_bytes(b"wav")
                mp3.write_bytes(b"mp3")
                return wav, mp3

            with mock.patch("utils.bin.article_audio.synthesize_chunk", side_effect=fake_synthesize), mock.patch(
                "utils.bin.article_audio.join_audio", side_effect=fake_join
            ):
                generate_audio(
                    object(),
                    post,
                    snapshot,
                    config,
                    bridge="http://127.0.0.1:11440/v1",
                    voice="private-voice-name",
                    model="private-model-name",
                )

            manifest = json.loads(post.manifest_path(config).read_text(encoding="utf-8"))
            self.assertNotIn("voice", manifest)
            self.assertNotIn("model", manifest)
            self.assertNotIn("private-voice-name", json.dumps(manifest))
            self.assertNotIn("private-model-name", json.dumps(manifest))
            self.assertEqual(audio_status(post, snapshot, config)[0], "current")


if __name__ == "__main__":
    unittest.main()
