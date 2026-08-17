#!/usr/bin/env python3
"""Canary tests for the Post 3 fail-closed memory router."""

from __future__ import annotations

import unittest

from memory_router import Memory, MemoryRouter, example_router


class MemoryRouterTests(unittest.TestCase):
    def test_unknown_context_cannot_write(self) -> None:
        result = example_router().remember(
            "unrecognized-room", Memory("new", "Do not store this.", "source")
        )
        self.assertEqual(
            result,
            {
                "stored": False,
                "reason": "context_memory_write_denied",
                "context_id": "default",
            },
        )

    def test_general_context_cannot_retrieve_private_canary(self) -> None:
        results = example_router().recall("general-room", "cedar lantern")
        self.assertNotIn("private-canary", {result.memory_id for result in results})
        self.assertEqual({result.bank for result in results}, {"general"})

    def test_unknown_context_can_only_read_general(self) -> None:
        results = example_router().recall("unrecognized-room", "private canary")
        self.assertEqual({result.bank for result in results}, {"general"})

    def test_private_context_merges_and_tags_banks(self) -> None:
        results = example_router().recall("private-room", "rollback evidence")
        self.assertEqual({result.bank for result in results}, {"general", "private"})
        self.assertTrue(all(result.source_id for result in results))

    def test_private_duplicate_wins_before_score_sort(self) -> None:
        duplicate = "The same reviewed memory appears in both projections."
        router = MemoryRouter(
            {
                "private-room": {
                    "read_banks": ["general", "private"],
                    "write_bank": "private",
                }
            },
            {
                "general": [Memory("general-copy", duplicate, "general-source")],
                "private": [Memory("private-copy", duplicate, "private-source")],
            },
        )
        results = router.recall("private-room", "reviewed memory")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].bank, "private")
        self.assertEqual(results[0].memory_id, "private-copy")

    def test_unauthorized_candidates_never_reach_scorer(self) -> None:
        scored: list[str] = []

        def recording_scorer(query: str, content: str) -> float:
            scored.append(content)
            return 1.0

        baseline = example_router()
        router = MemoryRouter(baseline.contexts, baseline.banks, recording_scorer)
        router.recall("general-room", "anything")
        self.assertTrue(scored)
        self.assertFalse(any("cedar-lantern" in content for content in scored))

    def test_rebuild_removes_memory_absent_from_authority(self) -> None:
        router = example_router()
        self.assertIn(
            "private-canary",
            {result.memory_id for result in router.recall("private-room", "cedar")},
        )
        router.replace_bank("private", [])
        self.assertNotIn(
            "private-canary",
            {result.memory_id for result in router.recall("private-room", "cedar")},
        )


if __name__ == "__main__":
    unittest.main()
