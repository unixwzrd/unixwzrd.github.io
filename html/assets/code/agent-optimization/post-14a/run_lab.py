#!/usr/bin/env python3
"""Run the fixed acceptance cases for the release-evidence teaching package."""

from __future__ import annotations

import json
from pathlib import Path

from release_evidence import PacketError, READY, validate_packet


ROOT = Path(__file__).resolve().parent


def load(name: str) -> dict:
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


def expect_ready(name: str) -> dict:
    result = validate_packet(load(name))
    assert result["decision"] == READY
    return result


def expect_error(name: str, code: str) -> None:
    expect_packet_error(load(name), code)


def expect_packet_error(packet: dict, code: str) -> None:
    try:
        validate_packet(packet)
    except PacketError as error:
        assert error.code == code, (error.code, code)
    else:
        raise AssertionError(f"packet unexpectedly passed instead of {code}")


def main() -> int:
    result = expect_ready("review-ready.json")
    conditions = [
        ("ready decision", result["decision"] == READY),
        ("publication observed", result["publication_observation"] == "prerelease"),
        ("acceptance remains incomplete", result["acceptance_claim"] == "incomplete"),
        ("approval remains unobserved", result["approval_claim"] == "unobserved"),
        ("four required gates", result["required_gates"] == 4),
        ("two passed gates", result["passed_gates"] == 2),
        ("two incomplete gates", result["incomplete_gates"] == 2),
        ("no failed gates", result["failed_gates"] == 0),
        ("no inferred release readiness", result["release_ready_inferred"] is False),
        ("no inferred approval", result["approval_inferred"] is False),
    ]
    for fixture, code in (
        ("missing-gate.json", "E_MISSING_GATE"),
        ("identity-mismatch.json", "E_IDENTITY"),
        ("manifest-mismatch.json", "E_IDENTITY"),
        ("stale-evidence.json", "E_STALE"),
        ("unsupported-approval.json", "E_APPROVAL_CLAIM"),
    ):
        expect_error(fixture, code)
        conditions.append((f"{fixture} rejected as {code}", True))

    no_required = load("review-ready.json")
    for gate in no_required["required_gates"]:
        gate["required"] = False
    expect_packet_error(no_required, "E_REQUIRED_GATE")
    conditions.append(("an all-optional contract is rejected", True))

    wrong_publication_gate = load("review-ready.json")
    wrong_publication_gate["publication_observation"]["evidence_ref"] = "archive-check"
    expect_packet_error(wrong_publication_gate, "E_PUBLICATION")
    conditions.append(("publication must cite release metadata", True))

    wrong_tag = load("review-ready.json")
    wrong_tag["publication_observation"]["tag"] = "1.4.0b4"
    expect_packet_error(wrong_tag, "E_TAG")
    conditions.append(("publication tag matches artifact identity", True))

    exact_age = load("review-ready.json")
    exact_age["evidence"][1]["observed_at"] = "2026-08-21T12:00:00Z"
    assert validate_packet(exact_age)["decision"] == READY
    conditions.append(("exact evidence-age boundary passes", True))

    over_age = load("review-ready.json")
    over_age["evidence"][1]["observed_at"] = "2026-08-21T11:59:59Z"
    expect_packet_error(over_age, "E_STALE")
    conditions.append(("one second over evidence age is stale", True))

    second = expect_ready("review-ready.json")
    conditions.extend(
        [
            ("deterministic decision", second == result),
            ("artifact identity retained", result["artifact_version"] == "1.4.0b3"),
            ("human review is next", result["next_gate"].startswith("human review")),
            ("publication is supplied evidence", result["publication_observation"] != "none"),
            ("success does not equal approval", result["approval_claim"] != "approved"),
            ("success does not equal complete acceptance", result["acceptance_claim"] != "complete"),
        ]
    )
    passed = 0
    for label, ok in conditions:
        if not ok:
            raise AssertionError(label)
        passed += 1
        print(f"PASS {label}")
    print(f"PASS {passed} of {len(conditions)} conditions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
