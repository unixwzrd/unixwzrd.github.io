"""Browser lifecycle tests use mocked CLI calls and temporary evidence only."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from utils.lib import browser_run


class BrowserRunTests(unittest.TestCase):
    def test_only_local_http_targets_are_accepted(self):
        for url in ("http://localhost:4000/", "http://127.0.0.1:4000/", "http://10.0.0.67:4000/", "http://xanax.local:4000/", "http://[::1]:4000/"):
            self.assertEqual(url, browser_run.local_url(url))
        for url in ("https://unixwzrd.ai/", "http://localhost.evil.example/", "http://8.8.8.8/", "file:///tmp/a", "http://user:secret@localhost/"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                browser_run.local_url(url)

    def run_fixture(self, fail=False):
        temp = tempfile.TemporaryDirectory(prefix="browser-run-fixture-")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        scripts = root / "utils/tests/browser"
        scripts.mkdir(parents=True)
        (scripts / "check_reader_experience_browser.js").write_text('async(page)=>{await page.screenshot({path:"output/playwright/example.png"});}')
        commands = []
        def run(command, **kwargs):
            commands.append(command)
            if "run-code" in command:
                source = Path(command[-1]).read_text()
                self.assertIn("route.abort()", source)
                self.assertNotIn('path:"output/playwright/', source)
                if fail:
                    return subprocess.CompletedProcess(command, 0, "### Error\nfixture failure", "")
            return subprocess.CompletedProcess(command, 0, "fixture CLI output", "")
        with mock.patch.object(browser_run.subprocess, "run", side_effect=run):
            if fail:
                with self.assertRaises(RuntimeError):
                    browser_run.run_audit("reader-experience", "http://localhost:4000/", "/fixture/cli", root=root)
                directory = next((root / "output/playwright").iterdir())
            else:
                directory = browser_run.run_audit("reader-experience", "http://localhost:4000/", "/fixture/cli", root=root)
        self.assertEqual("close", commands[-1][-1])
        self.assertFalse((directory / ".active").exists())
        return directory

    def test_success_records_completion_and_closes_owned_session(self):
        directory = self.run_fixture()
        self.assertEqual("passed", json.loads((directory / ".run.json").read_text())["status"])
        self.assertFalse((directory / ".keep").exists())

    def test_failure_is_pinned_even_when_cli_returns_zero(self):
        directory = self.run_fixture(fail=True)
        self.assertEqual("failed", json.loads((directory / ".run.json").read_text())["status"])
        self.assertTrue((directory / ".keep").exists())


if __name__ == "__main__":
    unittest.main()

