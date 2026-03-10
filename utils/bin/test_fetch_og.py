#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import fetch_og


class FetchOgFallbackTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
