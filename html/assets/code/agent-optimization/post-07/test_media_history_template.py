#!/usr/bin/env python
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import jinja2

from render_fixture import ROOT, render_case


UPSTREAM_SHA256 = "a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715"
STOCK_SHA256 = "d2cb9a5730cdd5f44bce3ada2dc1b0e00c6c59788b6d1c4d8d49c40a274dffb0"
DERIVATIVE_SHA256 = "162671aeaf5e2c39966816dae53e5e6f8ac0dfb97d53f34094afe74e44b2fae6"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class MediaHistoryTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
        cls.expected = json.loads((ROOT / "expected-results.json").read_text(encoding="utf-8"))

    def test_provenance_checksums(self) -> None:
        stock = (ROOT / "Qwen-3_5-stock-template.jinja").read_bytes()
        derivative = (ROOT / "Qwen-3_5-media-history-template.jinja").read_bytes()
        self.assertEqual(sha256(stock), STOCK_SHA256)
        self.assertEqual(sha256(stock.removesuffix(b"\n")), UPSTREAM_SHA256)
        self.assertEqual(sha256(derivative), DERIVATIVE_SHA256)

    def test_sanitized_fixture_contracts(self) -> None:
        for name, case in self.cases.items():
            with self.subTest(case=name):
                expected = self.expected[name]
                if expected["status"] == "error":
                    with self.assertRaisesRegex(jinja2.TemplateError, expected["error"]):
                        render_case(case)
                    continue
                rendered = render_case(case)
                for marker in expected.get("contains", []):
                    self.assertIn(marker, rendered)
                for marker in expected.get("absent", []):
                    self.assertNotIn(marker, rendered)
                for marker, count in expected.get("counts", {}).items():
                    self.assertEqual(rendered.count(marker), count)
                if expected.get("matches_stock"):
                    stock_rendered = render_case(
                        case,
                        ROOT / "Qwen-3_5-stock-template.jinja",
                    )
                    self.assertEqual(rendered, stock_rendered)

    def test_fixture_and_expectation_names_match(self) -> None:
        self.assertEqual(set(self.cases), set(self.expected))


if __name__ == "__main__":
    unittest.main()
