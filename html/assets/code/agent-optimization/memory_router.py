#!/usr/bin/env python3
"""Demonstrate fail-closed routing across general and private memory banks."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from typing import Callable, Iterable, Mapping


DEFAULT_POLICY = {
    "context_id": "default",
    "read_banks": ["general"],
    "write_bank": "deny",
}


@dataclass(frozen=True)
class Memory:
    memory_id: str
    content: str
    source_id: str


@dataclass(frozen=True)
class Result:
    memory_id: str
    content: str
    source_id: str
    bank: str
    score: float


def normalize(content: str) -> str:
    return " ".join(content.lower().split())


def token_score(query: str, content: str) -> float:
    query_tokens = set(re.findall(r"[a-z0-9]+", query.lower()))
    content_tokens = set(re.findall(r"[a-z0-9]+", content.lower()))
    if not query_tokens:
        return 0.0
    return len(query_tokens & content_tokens) / len(query_tokens)


class MemoryRouter:
    """Select authorized banks before calling a ranking function."""

    def __init__(
        self,
        contexts: Mapping[str, Mapping[str, object]],
        banks: Mapping[str, Iterable[Memory]] | None = None,
        scorer: Callable[[str, str], float] = token_score,
    ) -> None:
        self.contexts = {key: dict(value) for key, value in contexts.items()}
        self.banks = {
            "general": list((banks or {}).get("general", [])),
            "private": list((banks or {}).get("private", [])),
        }
        self.scorer = scorer

    def policy_for(self, context_key: str) -> dict[str, object]:
        return dict(self.contexts.get(context_key, DEFAULT_POLICY))

    def remember(self, context_key: str, memory: Memory) -> dict[str, object]:
        policy = self.policy_for(context_key)
        bank = str(policy.get("write_bank") or "deny")
        if bank == "deny":
            return {
                "stored": False,
                "reason": "context_memory_write_denied",
                "context_id": policy.get("context_id", "default"),
            }
        if bank not in self.banks:
            raise ValueError(f"policy selects unknown write bank: {bank}")
        self.banks[bank].append(memory)
        return {"stored": True, "bank": bank, "memory_id": memory.memory_id}

    def recall(self, context_key: str, query: str, limit: int = 5) -> list[Result]:
        if limit < 1:
            raise ValueError("limit must be at least 1")

        policy = self.policy_for(context_key)
        allowed = {str(bank) for bank in policy.get("read_banks", ["general"])}
        unknown = allowed - self.banks.keys()
        if unknown:
            raise ValueError(f"policy selects unknown read banks: {sorted(unknown)}")

        # Authorization happens here, before any candidate reaches the scorer.
        bank_order = [bank for bank in ("private", "general") if bank in allowed]
        candidates = [
            (bank, memory)
            for bank in bank_order
            for memory in self.banks[bank]
        ]

        combined: list[Result] = []
        seen: set[str] = set()
        for bank, memory in candidates:
            identity = normalize(memory.content)
            if not identity or identity in seen:
                continue
            seen.add(identity)
            combined.append(
                Result(
                    memory_id=memory.memory_id,
                    content=memory.content,
                    source_id=memory.source_id,
                    bank=bank,
                    score=self.scorer(query, memory.content),
                )
            )

        combined.sort(key=lambda result: (-result.score, result.memory_id))
        return combined[:limit]

    def replace_bank(self, bank: str, memories: Iterable[Memory]) -> None:
        """Replace disposable derived state from its reviewed authority."""
        if bank not in self.banks:
            raise ValueError(f"unknown bank: {bank}")
        self.banks[bank] = list(memories)


def example_router() -> MemoryRouter:
    contexts = {
        "general-room": {
            "context_id": "general-example",
            "read_banks": ["general"],
            "write_bank": "general",
        },
        "private-room": {
            "context_id": "private-example",
            "read_banks": ["general", "private"],
            "write_bank": "private",
        },
    }
    banks = {
        "general": [
            Memory("general-1", "Release checklists require rollback evidence.", "doc-1"),
            Memory("general-2", "Unknown contexts cannot write memory.", "doc-2"),
        ],
        "private": [
            Memory("private-canary", "Private canary: cedar-lantern.", "doc-3"),
            Memory("private-2", "Rollback evidence belongs with the private review.", "doc-4"),
        ],
    }
    return MemoryRouter(contexts, banks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("context", choices=["unknown", "general-room", "private-room"])
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    results = example_router().recall(args.context, args.query, args.limit)
    print(json.dumps([asdict(result) for result in results], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
