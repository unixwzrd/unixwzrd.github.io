#!/usr/bin/env python
"""Compare sanitized fixtures under the stock and media-history templates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import jinja2

from render_fixture import ROOT, render_case


STOCK_TEMPLATE = ROOT / "Qwen-3_5-stock-template.jinja"
DERIVATIVE_TEMPLATE = ROOT / "Qwen-3_5-media-history-template.jinja"
EXPECTED_RESULTS = ROOT / "expected-results.json"


def render_safely(case: Dict[str, Any], template_path: Path) -> Dict[str, Any]:
    """Render one fixture and return bounded output metadata."""
    try:
        rendered = render_case(case, template_path)
    except jinja2.TemplateError as exc:
        return {"characters": None, "error": str(exc), "rendered": None}
    return {"characters": len(rendered), "error": None, "rendered": rendered}


def inspect_case(
    name: str,
    case: Dict[str, Any],
    expected: Dict[str, Any],
) -> Dict[str, Any]:
    """Compare one fixture and verify its published marker expectations."""
    stock = render_safely(case, STOCK_TEMPLATE)
    derived = render_safely(case, DERIVATIVE_TEMPLATE)
    rendered: Optional[str] = derived["rendered"]
    required_present: List[str] = expected.get("contains", [])
    required_absent: List[str] = expected.get("absent", [])
    counts: Dict[str, int] = expected.get("counts", {})

    present_passed = 0 if rendered is None else sum(
        marker in rendered for marker in required_present
    )
    absent_passed = 0 if rendered is None else sum(
        marker not in rendered for marker in required_absent
    )
    count_passed = 0 if rendered is None else sum(
        rendered.count(marker) == count for marker, count in counts.items()
    )

    stock_characters = stock["characters"]
    derived_characters = derived["characters"]
    character_delta = None
    exact_match = False
    if stock_characters is not None and derived_characters is not None:
        character_delta = derived_characters - stock_characters
        exact_match = stock["rendered"] == derived["rendered"]

    return {
        "case": name,
        "description": case["description"],
        "expected_status": expected["status"],
        "expected_error": expected.get("error"),
        "matches_stock_required": bool(expected.get("matches_stock")),
        "stock_characters": stock_characters,
        "derived_characters": derived_characters,
        "character_delta": character_delta,
        "exact_match": exact_match,
        "stock_error": stock["error"],
        "derived_error": derived["error"],
        "present_checks": {"passed": present_passed, "total": len(required_present)},
        "absent_checks": {"passed": absent_passed, "total": len(required_absent)},
        "count_checks": {"passed": count_passed, "total": len(counts)},
        "image_placeholders": 0 if rendered is None else rendered.count("<|image_pad|>"),
        "video_placeholders": 0 if rendered is None else rendered.count("<|video_pad|>"),
    }


def inspect_fixtures(selected: Optional[str] = None) -> List[Dict[str, Any]]:
    """Inspect all fixtures, or one named fixture."""
    cases = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED_RESULTS.read_text(encoding="utf-8"))
    if selected is not None:
        if selected not in cases:
            choices = ", ".join(sorted(cases))
            raise ValueError(f"unknown fixture: {selected}; choose from: {choices}")
        names = [selected]
    else:
        names = list(cases)
    return [inspect_case(name, cases[name], expected[name]) for name in names]


def check_summary(summary: Dict[str, Any]) -> str:
    """Return a compact result label for one inspection summary."""
    if summary["expected_status"] == "error":
        expected_error = summary["expected_error"]
        errors_match = (
            expected_error is not None
            and summary["stock_error"] is not None
            and summary["derived_error"] is not None
            and expected_error in summary["stock_error"]
            and expected_error in summary["derived_error"]
        )
        return "expected error" if errors_match else "check failed"
    if summary["stock_error"] is not None or summary["derived_error"] is not None:
        return "check failed"
    checks = (
        summary["present_checks"],
        summary["absent_checks"],
        summary["count_checks"],
    )
    checks_pass = all(item["passed"] == item["total"] for item in checks)
    stock_contract_passes = (
        not summary["matches_stock_required"] or summary["exact_match"]
    )
    return "pass" if checks_pass and stock_contract_passes else "check failed"


def print_table(summaries: List[Dict[str, Any]]) -> None:
    """Print a bounded human-readable comparison table."""
    print(f"{'fixture':30} {'stock':>9} {'derived':>9} {'delta':>9} {'result':>14}")
    print(f"{'-' * 30} {'-' * 9} {'-' * 9} {'-' * 9} {'-' * 14}")
    for summary in summaries:
        stock = "error" if summary["stock_characters"] is None else str(summary["stock_characters"])
        derived = "error" if summary["derived_characters"] is None else str(summary["derived_characters"])
        delta = "n/a" if summary["character_delta"] is None else str(summary["character_delta"])
        print(
            f"{summary['case']:30} {stock:>9} {derived:>9} "
            f"{delta:>9} {check_summary(summary):>14}"
        )
    print("\nCharacter deltas describe these synthetic renders. They are not token or cost measurements.")


def main() -> int:
    """Run the fixture inspector command."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", nargs="?", help="Inspect one fixture instead of all fixtures")
    parser.add_argument("--json", action="store_true", help="Write the bounded summary as JSON")
    args = parser.parse_args()
    try:
        summaries = inspect_fixtures(args.case)
    except ValueError as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(summaries, indent=2, sort_keys=True))
    else:
        print_table(summaries)
    return 0 if all(check_summary(summary) in {"pass", "expected error"} for summary in summaries) else 1


if __name__ == "__main__":
    raise SystemExit(main())
