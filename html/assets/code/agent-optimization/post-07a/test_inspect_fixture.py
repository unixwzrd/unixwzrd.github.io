#!/usr/bin/env python
from __future__ import annotations

import unittest

from inspect_fixture import check_summary, inspect_fixtures
from render_fixture import render_case


class FixtureInspectorTests(unittest.TestCase):
    def test_all_packaged_fixtures_satisfy_their_contracts(self) -> None:
        summaries = inspect_fixtures()
        self.assertEqual(len(summaries), 7)
        self.assertTrue(
            all(check_summary(summary) in {"pass", "expected error"} for summary in summaries)
        )

    def test_ordinary_history_matches_stock_exactly(self) -> None:
        summary = inspect_fixtures("ordinary_text_tool_history")[0]
        self.assertTrue(summary["exact_match"])
        self.assertEqual(summary["character_delta"], 0)

    def test_required_stock_match_cannot_report_pass_when_render_differs(self) -> None:
        summary = inspect_fixtures("ordinary_text_tool_history")[0]
        summary["exact_match"] = False
        self.assertEqual(check_summary(summary), "check failed")

    def test_textual_image_history_is_removed(self) -> None:
        summary = inspect_fixtures("textual_image_exchanges")[0]
        self.assertLess(summary["character_delta"], 0)
        self.assertEqual(summary["absent_checks"]["passed"], summary["absent_checks"]["total"])

    def test_native_media_keeps_qwen_placeholders(self) -> None:
        summary = inspect_fixtures("native_structured_media")[0]
        self.assertEqual(summary["image_placeholders"], 1)
        self.assertEqual(summary["video_placeholders"], 1)

    def test_malformed_ordering_reports_the_template_error(self) -> None:
        summary = inspect_fixtures("malformed_ordering")[0]
        self.assertEqual(check_summary(summary), "expected error")
        self.assertIn("System message must be at the beginning.", summary["stock_error"])
        self.assertIn("System message must be at the beginning.", summary["derived_error"])

    def test_declared_error_requires_matching_stock_and_derived_failures(self) -> None:
        summary = inspect_fixtures("malformed_ordering")[0]
        summary["stock_error"] = None
        summary["derived_error"] = "Unrelated template failure"
        self.assertEqual(check_summary(summary), "check failed")

    def test_textual_media_threshold_is_strictly_greater_than_4096(self) -> None:
        prefix = '{"images":["iVBORw0KGgoTHRESHOLD_CANARY'
        suffix = '"]}'

        def threshold_case(length: int) -> dict:
            content = prefix + ("A" * (length - len(prefix) - len(suffix))) + suffix
            return {
                "payload": {
                    "messages": [
                        {"role": "user", "content": "Create an invented image."},
                        {
                            "role": "assistant",
                            "content": "threshold image call",
                            "tool_calls": [
                                {
                                    "type": "function",
                                    "function": {
                                        "name": "terminal",
                                        "arguments": {
                                            "command": "generate invented image"
                                        },
                                    },
                                }
                            ],
                        },
                        {"role": "tool", "content": content},
                        {"role": "user", "content": "Continue."},
                    ],
                    "tools": [],
                    "add_generation_prompt": True,
                }
            }

        self.assertIn("THRESHOLD_CANARY", render_case(threshold_case(4096)))
        self.assertNotIn("THRESHOLD_CANARY", render_case(threshold_case(4097)))


if __name__ == "__main__":
    unittest.main()
