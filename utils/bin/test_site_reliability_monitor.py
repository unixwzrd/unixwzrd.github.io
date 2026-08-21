#!/usr/bin/env python3

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("site_reliability_monitor.py")
SPEC = importlib.util.spec_from_file_location("site_reliability_monitor", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
SiteReliabilityMonitor = MODULE.SiteReliabilityMonitor


class SiteReliabilityMonitorDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.monitor = SiteReliabilityMonitor.__new__(SiteReliabilityMonitor)
        self.monitor.verbose = False

    def test_redirect_paths_include_existing_and_legacy_values(self):
        paths = self.monitor._redirect_paths_from_front_matter(
            {
                "redirect_from": ["/old-case/", "/s/abc123/"],
                "legacy_project_permalink": "/former-title/",
            }
        )
        self.assertEqual(paths, ["/old-case/", "/s/abc123/", "/former-title/"])

    def test_project_discovery_uses_frozen_slug_and_checks_legacy_redirect(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            post_dir = root / "html/projects/Example/_posts"
            post_dir.mkdir(parents=True)
            (post_dir / "2026-08-21-source-filename.md").write_text(
                """---
title: A Completely Different Title
date: 2026-08-20
permalink_slug: frozen-source-route
legacy_project_permalink: /projects/Example/2026/08/20/a-completely-different-title/
---
Body
""",
                encoding="utf-8",
            )

            original_directory = Path.cwd()
            try:
                os.chdir(root)
                pages = self.monitor._discover_critical_pages()
            finally:
                os.chdir(original_directory)

        self.assertIn(
            "/projects/Example/2026/08/20/frozen-source-route/", pages
        )
        self.assertIn(
            "/projects/Example/2026/08/20/a-completely-different-title/", pages
        )


if __name__ == "__main__":
    unittest.main()
