#!/usr/bin/env python3
"""Run the bounded, synthetic benchmark-comparison lab."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from benchmark_compare import SchemaError, compare_bundles, load_bundle, render_json, render_markdown, render_tsv, validate_bundle


ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"


def main() -> int:
    baseline = load_bundle(FIXTURES / "baseline.json")
    candidate = load_bundle(FIXTURES / "candidate-optimization.json")
    ineligible = load_bundle(FIXTURES / "candidate-ineligible.json")
    result = compare_bundles(baseline, candidate)
    rejected = compare_bundles(baseline, ineligible)

    correctness = copy.deepcopy(candidate)
    correctness["correctness"]["passed"] = False
    correctness_result = compare_bundles(baseline, correctness)

    unknown = copy.deepcopy(candidate)
    unknown["identity"]["hostname"] = "must-not-be-accepted"
    boolean_numeric = copy.deepcopy(candidate)
    boolean_numeric["identity"]["memory_gb"] = True

    def rejected_schema(value: dict) -> bool:
        try:
            validate_bundle(value)
        except SchemaError:
            return True
        return False

    with tempfile.TemporaryDirectory(prefix="benchmark-comparator-") as temporary:
        report_dir = Path(temporary)
        projections = {
            "json": render_json(result),
            "tsv": render_tsv(result),
            "markdown": render_markdown(result),
        }
        for extension, content in projections.items():
            (report_dir / f"comparison.{extension if extension != 'markdown' else 'md'}").write_text(content, encoding="utf-8")
        json_payload = json.loads(projections["json"])
        projection_agreement = (
            json_payload["classification"] == result.classification
            and all(result.classification in projections[name] for name in projections)
            and all((result.experiment_kind or "") in projections[name] for name in projections)
            and all(row["metric"] in projections["tsv"] and row["metric"] in projections["markdown"] for row in result.metrics)
        )

    metric_map = {row["metric"]: row for row in result.metrics}
    checks = {
        "baseline_schema_valid": True,
        "candidate_schema_valid": True,
        "artifact_identity_matches": baseline["identity"]["artifact_fingerprint"] == candidate["identity"]["artifact_fingerprint"],
        "workload_identity_matches": baseline["identity"]["workload_fingerprint"] == candidate["identity"]["workload_fingerprint"],
        "experiment_kind_is_optimization": result.experiment_kind == "optimization",
        "correctness_passes": result.classification == "comparable",
        "comparison_is_eligible": result.classification == "comparable",
        "ttft_direction_is_lower": metric_map["ttft_ms"]["direction"] == "lower",
        "decode_direction_is_higher": metric_map["decode_tokens_per_s"]["direction"] == "higher",
        "median_aggregation_used": metric_map["ttft_ms"]["baseline_median"] == 210.0,
        "incompatible_cache_state_rejected": rejected.classification == "ineligible" and "warm_cold" in rejected.reasons,
        "profiled_mismatch_rejected": _mismatch_rejected(baseline, candidate, "profiled", True),
        "incompatible_workload_rejected": _mismatch_rejected(baseline, candidate, "workload_fingerprint", "9" * 64),
        "context_mismatch_rejected": _mismatch_rejected(baseline, candidate, "context_tokens", 8192),
        "correctness_failure_blocks_speed_claim": correctness_result.classification == "correctness_failed" and not correctness_result.metrics,
        "unknown_field_rejected": rejected_schema(unknown),
        "boolean_numeric_rejected": rejected_schema(boolean_numeric),
        "json_tsv_markdown_agree": projection_agreement,
        "prompt_and_output_text_absent": _privacy_check(baseline, candidate, ineligible, projections),
        "cleanup_complete": not report_dir.exists(),
    }
    print(json.dumps({"conditions": checks, "passed": sum(checks.values()), "total": len(checks), "ok": all(checks.values())}, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


def _mismatch_rejected(baseline: dict, candidate: dict, field: str, value: object) -> bool:
    changed = copy.deepcopy(candidate)
    changed["identity"][field] = value
    result = compare_bundles(baseline, changed)
    return result.classification == "ineligible" and field in result.reasons


def _privacy_check(*values: object) -> bool:
    text = json.dumps(values, sort_keys=True).lower()
    forbidden = ('"prompt"', '"completion"', '"output_text"', '"hostname"', '"user"', '"ip_address"', '"token"')
    return not any(term in text for term in forbidden)


if __name__ == "__main__":
    raise SystemExit(main())
