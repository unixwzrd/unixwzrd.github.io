#!/usr/bin/env python3

import tempfile
import unittest
import json
from pathlib import Path
from unittest import mock

import fetch_og
import requests


class FetchOgFallbackTests(unittest.TestCase):
    def tearDown(self):
        fetch_og.REFRESH_EXISTING_IMAGES = False

    def test_format_title_preserves_llm_acronym(self):
        self.assertEqual(fetch_og.format_title("LLM-Ops-Kit"), "LLM Ops Kit")

    def test_normalize_description_strips_github_suffix(self):
        self.assertEqual(
            fetch_og.normalize_description(
                "Operational toolkit for running, deploying, and maintaining a local OpenClaw stack across hosts. - unixwzrd/LLM-Ops-Kit",
                "unixwzrd",
                "LLM-Ops-Kit",
            ),
            "Operational toolkit for running, deploying, and maintaining a local OpenClaw stack across hosts.",
        )

    def test_private_repo_without_manual_data_still_generates_scaffolding(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            (base_dir / "html/_data").mkdir(parents=True, exist_ok=True)

            repo_config = {"owner": "unixwzrd", "name": "LLM-Ops-Kit"}

            with mock.patch.object(
                fetch_og, "setup_environment", return_value=base_dir
            ), mock.patch.object(
                fetch_og, "load_repository_config", return_value=[repo_config]
            ), mock.patch.object(
                fetch_og, "fetch_github_data", return_value=None
            ), mock.patch.object(
                fetch_og, "write_projects_data", return_value=True
            ) as write_projects_data:
                fetch_og.main()

            project_page = base_dir / "html/projects/LLM-Ops-Kit.md"
            draft_template = (
                base_dir / "html/projects/LLM-Ops-Kit/_drafts/template-blog-entry.md"
            )
            intro_post_dir = base_dir / "html/projects/LLM-Ops-Kit/_posts"
            image_dir = base_dir / "html/assets/images/projects/LLM-Ops-Kit"
            gitkeep_file = image_dir / ".gitkeep"

            self.assertTrue(project_page.exists())
            self.assertTrue(draft_template.exists())
            self.assertTrue(intro_post_dir.exists())
            self.assertTrue(image_dir.exists())
            self.assertTrue(gitkeep_file.exists())

            projects = write_projects_data.call_args.args[0]
            self.assertEqual(len(projects), 1)
            self.assertEqual(projects[0]["name"], "LLM-Ops-Kit")
            self.assertEqual(projects[0]["title"], "LLM Ops Kit")
            self.assertEqual(projects[0]["description"], "Private repository: LLM-Ops-Kit")
            self.assertEqual(projects[0]["page_url"], "/projects/LLM-Ops-Kit/")
            self.assertEqual(projects[0]["visibility"], "private")

    def test_overrides_can_set_banner_image_url(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            (base_dir / "html/_data").mkdir(parents=True, exist_ok=True)

            repo_config = {
                "owner": "unixwzrd",
                "name": "LogGPT",
                "overrides": {
                    "title": "LogGPT for Safari",
                    "banner_image_url": "/assets/images/projects/LogGPT/LogGPT-banner.png",
                },
            }

            with mock.patch.object(
                fetch_og,
                "cache_image",
                return_value="/assets/images/projects/LogGPT.png",
            ):
                entry = fetch_og.create_project_entry(
                    data={
                        "description": "Export ChatGPT conversations.",
                        "image_url": "https://example.com/og-image.png",
                        "visibility": "public",
                    },
                    owner="unixwzrd",
                    name="LogGPT",
                    base_dir=base_dir,
                    repo_config=repo_config,
                )

            self.assertEqual(entry["title"], "LogGPT for Safari")
            self.assertEqual(
                entry["banner_image_url"],
                "/assets/images/projects/LogGPT/LogGPT-banner.png",
            )

    def test_create_project_entry_prefers_generated_local_card_for_public_repo(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            repo_config = {"owner": "unixwzrd", "name": "extract-chat", "overrides": {}}

            with mock.patch.object(
                fetch_og,
                "generate_project_card",
                return_value="/assets/images/projects/extract-chat.png",
            ) as generate_project_card, mock.patch.object(fetch_og, "cache_image") as cache_image:
                entry = fetch_og.create_project_entry(
                    data={
                        "description": "Export ChatGPT sessions as HTML and Markdown.",
                        "visibility": "public",
                        "stargazers_count": 12,
                        "forks_count": 3,
                        "open_issues_count": 1,
                        "language": "Python",
                    },
                    owner="unixwzrd",
                    name="extract-chat",
                    base_dir=base_dir,
                    repo_config=repo_config,
                )

            self.assertEqual(entry["image_url"], "/assets/images/projects/extract-chat.png")
            generate_project_card.assert_called_once()
            cache_image.assert_not_called()

    def test_create_project_entry_honors_manual_image_override(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            repo_config = {
                "owner": "unixwzrd",
                "name": "Example",
                "overrides": {
                    "image_url": "/assets/images/projects/manual-example.png",
                },
            }

            with mock.patch.object(
                fetch_og,
                "cache_image",
                return_value="/assets/images/projects/manual-example.png",
            ) as cache_image, mock.patch.object(fetch_og, "generate_project_card") as generate_project_card:
                entry = fetch_og.create_project_entry(
                    data={
                        "description": "Example repo.",
                        "visibility": "public",
                    },
                    owner="unixwzrd",
                    name="Example",
                    base_dir=base_dir,
                    repo_config=repo_config,
                )

            self.assertEqual(entry["image_url"], "/assets/images/projects/manual-example.png")
            cache_image.assert_called_once()
            generate_project_card.assert_not_called()

    def test_cache_image_keeps_existing_file_on_rate_limit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            image_dir = base_dir / "html/assets/images/projects"
            image_dir.mkdir(parents=True, exist_ok=True)
            cached_image = image_dir / "LogGPT.png"
            cached_image.write_bytes(b"existing-image")

            response = requests.Response()
            response.status_code = 429
            response.url = "https://opengraph.githubassets.com/example/unixwzrd/LogGPT"

            error = requests.HTTPError("429 Client Error: Too Many Requests", response=response)

            with mock.patch.object(
                fetch_og.requests, "get", return_value=response
            ), mock.patch.object(fetch_og.time, "sleep", return_value=None):
                result = fetch_og.cache_image(
                    "https://opengraph.githubassets.com/example/unixwzrd/LogGPT",
                    "LogGPT",
                    base_dir,
                )

            self.assertEqual(result, "/assets/images/projects/LogGPT.png")
            self.assertEqual(cached_image.read_bytes(), b"existing-image")

    def test_cache_image_uses_existing_file_without_refresh(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            image_dir = base_dir / "html/assets/images/projects"
            image_dir.mkdir(parents=True, exist_ok=True)
            cached_image = image_dir / "UnicodeFix.png"
            cached_image.write_bytes(b"existing-image")

            with mock.patch.object(fetch_og.requests, "get") as mock_get:
                result = fetch_og.cache_image(
                    "https://opengraph.githubassets.com/example/unixwzrd/UnicodeFix",
                    "UnicodeFix",
                    base_dir,
                )

            self.assertEqual(result, "/assets/images/projects/UnicodeFix.png")
            mock_get.assert_not_called()

    def test_generate_project_card_uses_metadata_cache_when_stats_unchanged(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            image_dir = base_dir / "html/assets/images/projects"
            image_dir.mkdir(parents=True, exist_ok=True)
            image_path = image_dir / "extract-chat.png"
            image_path.write_bytes(b"existing-image")
            meta_path = image_dir / "extract-chat.card-meta.json"
            meta = {
                "card_style_version": fetch_og.CARD_STYLE_VERSION,
                "owner": "unixwzrd",
                "name": "extract-chat",
                "title": "Extract Chat",
                "description": "Export ChatGPT sessions.",
                "language": "Python",
                "top_languages": [{"name": "Python", "share": "100%", "color": "#66d9ef"}],
                "contributors_count": 4,
                "stargazers_count": 12,
                "forks_count": 3,
                "open_issues_count": 1,
                "updated_at": "2026-04-09T00:00:00Z",
            }
            meta_path.write_text(json.dumps(meta), encoding="utf-8")

            with mock.patch.object(fetch_og.shutil, "which", return_value="/usr/local/bin/wkhtmltoimage"), mock.patch.object(
                fetch_og.subprocess, "run"
            ) as subprocess_run:
                result = fetch_og.generate_project_card(
                    {
                        "language": "Python",
                        "top_languages": [{"name": "Python", "share": "100%", "color": "#66d9ef"}],
                        "contributors_count": 4,
                        "stargazers_count": 12,
                        "forks_count": 3,
                        "open_issues_count": 1,
                        "updated_at": "2026-04-09T00:00:00Z",
                    },
                    "unixwzrd",
                    "extract-chat",
                    "Extract Chat",
                    "Export ChatGPT sessions.",
                    base_dir,
                )

            self.assertEqual(result, "/assets/images/projects/extract-chat.png")
            subprocess_run.assert_not_called()

    def test_generate_project_card_regenerates_when_stats_change(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            image_dir = base_dir / "html/assets/images/projects"
            image_dir.mkdir(parents=True, exist_ok=True)
            image_path = image_dir / "extract-chat.png"
            image_path.write_bytes(b"existing-image")
            meta_path = image_dir / "extract-chat.card-meta.json"
            meta_path.write_text(
                json.dumps(
                    {
                        "card_style_version": fetch_og.CARD_STYLE_VERSION,
                        "owner": "unixwzrd",
                        "name": "extract-chat",
                        "title": "Extract Chat",
                        "description": "Export ChatGPT sessions.",
                        "language": "Python",
                        "top_languages": [{"name": "Python", "share": "100%", "color": "#66d9ef"}],
                        "contributors_count": 4,
                        "stargazers_count": 11,
                        "forks_count": 3,
                        "open_issues_count": 1,
                        "updated_at": "2026-04-09T00:00:00Z",
                    }
                ),
                encoding="utf-8",
            )

            def fake_run(cmd, check, capture_output, text):
                Path(cmd[-1]).write_bytes(b"new-image")
                return mock.Mock(returncode=0, stderr="")

            with mock.patch.object(fetch_og.shutil, "which", return_value="/usr/local/bin/wkhtmltoimage"), mock.patch.object(
                fetch_og.subprocess, "run", side_effect=fake_run
            ) as subprocess_run:
                result = fetch_og.generate_project_card(
                    {
                        "language": "Python",
                        "top_languages": [{"name": "Python", "share": "100%", "color": "#66d9ef"}],
                        "contributors_count": 4,
                        "stargazers_count": 12,
                        "forks_count": 3,
                        "open_issues_count": 1,
                        "updated_at": "2026-04-09T00:00:00Z",
                    },
                    "unixwzrd",
                    "extract-chat",
                    "Extract Chat",
                    "Export ChatGPT sessions.",
                    base_dir,
                )

            self.assertEqual(result, "/assets/images/projects/extract-chat.png")
            subprocess_run.assert_called_once()
            self.assertEqual(image_path.read_bytes(), b"new-image")

    def test_parse_args_enables_explicit_refresh_flag(self):
        with mock.patch("sys.argv", ["fetch_og.py", "--refresh-images"]):
            args = fetch_og.parse_args()
        self.assertTrue(args.refresh_images)


if __name__ == "__main__":
    unittest.main()
