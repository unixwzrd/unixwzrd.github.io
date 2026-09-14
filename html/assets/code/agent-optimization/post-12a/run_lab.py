from __future__ import annotations

import json
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from triage_packet import build_packet, load, render_json, render_markdown  # noqa: E402

AS_OF = "2030-01-02T03:09:05Z"


def main() -> int:
    complete = build_packet(load(ROOT / "fixtures" / "complete.json"), as_of=AS_OF)
    unobserved = build_packet(load(ROOT / "fixtures" / "unobserved.json"), as_of=AS_OF)
    stale = build_packet(load(ROOT / "fixtures" / "stale.json"), as_of=AS_OF)
    manifest = json.loads((ROOT / "manifest.json").read_text())
    manifest_valid = all(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected for relative, expected in manifest["files"].items())
    checks = {
        "complete evidence is ready for review": complete.decision == "ready_for_review",
        "complete Markdown matches the golden file": render_markdown(complete) == (ROOT / "fixtures" / "expected-complete.md").read_text(),
        "JSON preserves the review decision": json.loads(render_json(complete))["decision"] == "ready_for_review",
        "target-only and cascade facts remain distinct": complete.cascade_stops == ("demo-stack:agent",),
        "only observed running cascade members are reported": complete.observed_running_impact == ("demo-stack:agent",),
        "the operation is a closed argument array": complete.operation_argv == ("llmops", "component", "restart", "demo-stack:model-proxy", "--cascade"),
        "unobserved impact is not ready": unobserved.decision == "evidence_incomplete",
        "incomplete evidence suppresses the operation array": not unobserved.operation_argv,
        "stale evidence is not ready": stale.decision == "evidence_stale",
        "stale evidence suppresses the operation array": not stale.operation_argv,
        "manifest checksums match package files": manifest_valid,
        "manifest capability boundary is closed": manifest["capabilities"] == ["read_fixture", "validate", "correlate", "render"],
        "rendering creates no output directory": not (ROOT / "output").exists(),
        "Python bytecode is absent": not any(ROOT.rglob("__pycache__")) and not any(ROOT.rglob("*.pyc")),
    }
    for label, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'}: {label}")
    print(f"{sum(checks.values())}/{len(checks)} conditions passed")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
