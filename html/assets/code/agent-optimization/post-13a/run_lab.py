#!/usr/bin/env python3
"""Run the fixed, model-free isolation preflight walkthrough."""

from __future__ import annotations

import json
from pathlib import Path

from isolation_preflight import validate_manifest


ROOT = Path(__file__).resolve().parent
CASES = {
    "ready.json": ("manifest_ready_for_isolated_test", []),
    "shared-root.json": ("not_ready", ["shared_owned_root"]),
    "shared-port.json": ("not_ready", ["same_host_port_collision"]),
    "shared-vault-writers.json": (
        "not_ready",
        ["shared_store_multiple_writers:test-vault", "store_owner_mismatch:test-vault"],
    ),
}


def main() -> int:
    passed = 0
    for filename, (decision, required_findings) in CASES.items():
        raw = json.loads((ROOT / "fixtures" / filename).read_text(encoding="utf-8"))
        result = validate_manifest(raw)
        checks = [
            result["decision"] == decision,
            all(item in result["findings"] for item in required_findings),
            result["runtime_observed"] is False,
            result["security_certified"] is False,
        ]
        if not all(checks):
            print(f"FAIL {filename}")
            return 1
        passed += len(checks)
        print(f"PASS {filename}: {result['display_decision']}")
    print(f"PASS {passed} of {len(CASES) * 4} conditions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
