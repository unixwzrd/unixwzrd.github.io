"""Canonical-only tooling paths and test-runner safety contracts."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest
import re
import tempfile
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from utils.lib import run_tests


class ToolingLayoutTests(unittest.TestCase):
    def test_root_scripts_directory_has_been_removed(self):
        self.assertFalse((ROOT / "scripts").exists())
        self.assertFalse((ROOT / "scripts").is_symlink())

    def test_retired_python_and_manual_aliases_have_been_removed(self):
        names = ("test_article_audio.py", "test_article_tts.py", "test_fetch_og.py", "test_site_reliability_monitor.py", "test_email.py", "test_external_links.py", "test_file_watcher.py", "test_services.sh", "quick_test.py")
        for name in names:
            alias = ROOT / "utils/bin" / name
            self.assertFalse(alias.exists(), name)
            self.assertFalse(alias.is_symlink(), name)

    def test_canonical_tooling_contains_no_symlinks(self):
        for folder in ("bin", "lib", "tests"):
            for path in (ROOT / "utils" / folder).rglob("*"):
                self.assertFalse(path.is_symlink(), str(path.relative_to(ROOT)))

    def test_live_documentation_and_callers_do_not_use_retired_site_tool_paths(self):
        root_names = ("backfill_short_url_front_matter.rb", "list_tags.rb", "check_tag_taxonomy.rb", "verify_project_permalink_redirects.rb", "verify_short_url_redirects.rb", "test_check_site_environment.rb", "test_jekyll_site.rb", "test_reader_experience.rb", "test_secrets_kit_product.rb", "test_short_link_attribution.rb", "check_local_reader_browser.js", "check_reader_experience_browser.js", "check_secrets_kit_product_browser.js", "check_short_link_attribution_browser.js")
        retired = ["scripts/" + name for name in root_names]
        retired += ["utils/bin/" + name for name in ("test_article_audio.py", "test_article_tts.py", "test_fetch_og.py", "test_site_reliability_monitor.py", "test_email.py", "test_external_links.py", "test_file_watcher.py", "test_services.sh", "quick_test.py")]
        files = [ROOT / name for name in ("README.md", "TODO.md", "CHANGELOG.md", ".pre-commit-config.yaml")]
        for folder in (".github", "docs", "html", "utils/bin", "utils/lib", "utils/tests"):
            files.extend(path for path in (ROOT / folder).rglob("*") if path.suffix in (".md", ".txt", ".py", ".rb", ".sh", ".js", ".yml", ".yaml", ".html") and path.is_file() and not path.is_symlink())
        for path in files:
            # Dated review receipts retain literal historical commands under a
            # prominent migration notice; they are not operational tutorials.
            if path == ROOT / "docs/publication/jekyll-site-tooling-review.md":
                continue
            text = path.read_text()
            for old in retired:
                self.assertNotIn(old, text, f"Retired tool path in {path.relative_to(ROOT)}")

    def test_hooks_and_command_entry_points_are_portable_and_executable(self):
        for name in ("check-site", "check_site.sh", "pre-commit", "cleanup-artifacts"):
            path = ROOT / "utils/bin" / name
            self.assertFalse(path.is_symlink())
            self.assertTrue(path.stat().st_mode & 0o111)
            self.assertNotIn("/Users/mps/", path.read_text())

    def test_runner_discovers_canonical_tests_once_and_excludes_manual_diagnostics(self):
        commands = []
        def capture(command, **kwargs):
            commands.append(command)
            return subprocess.CompletedProcess(command, 0)
        with mock.patch.object(sys, "argv", ["run_tests"]), mock.patch.object(run_tests.subprocess, "run", side_effect=capture):
            self.assertEqual(0, run_tests.main())
        ruby = [Path(command[-1]) for command in commands if "ruby" in command]
        self.assertEqual(sorted((ROOT / "utils/tests/ruby").glob("test_*.rb")), ruby)
        self.assertEqual(len(ruby), len(set(ruby)))
        self.assertNotIn("diagnostics", str(commands))
        self.assertNotIn("jekyll build", str(commands))

    def test_runner_stops_on_failed_check(self):
        with mock.patch.object(sys, "argv", ["run_tests"]), mock.patch.object(run_tests.subprocess, "run", return_value=subprocess.CompletedProcess([], 7)) as run:
            self.assertEqual(7, run_tests.main())
            self.assertEqual(1, run.call_count)

    def test_catalog_links_cover_every_canonical_tool(self):
        catalog = (ROOT / "utils/README.md").read_text()
        links = set(re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", catalog))
        for folder in ("bin", "lib", "tests"):
            for path in (ROOT / "utils" / folder).rglob("*"):
                if not path.is_file() or path.is_symlink() or "__pycache__" in path.parts or path.name.startswith(".") or path.suffix == ".md":
                    continue
                relative = path.relative_to(ROOT / "utils").as_posix()
                with self.subTest(tool=relative):
                    self.assertIn(relative, links, "Every canonical tool needs a catalog entry")

    def test_monitor_regressions_import_without_local_runtime_log_directories(self):
        with tempfile.TemporaryDirectory(prefix="monitor-import-") as directory:
            script = ROOT / "utils/tests/python/test_site_reliability_monitor.py"
            result = subprocess.run([sys.executable, "-c", f"import runpy; runpy.run_path({str(script)!r}, run_name='fixture')"], cwd=directory, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertFalse((Path(directory) / "utils/log").exists())


if __name__ == "__main__":
    unittest.main()

