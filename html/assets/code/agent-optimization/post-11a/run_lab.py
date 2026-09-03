#!/usr/bin/env python3
"""Run the bounded, invented Hands-On 11A experiment lab."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from experiment_lab import SchemaError, compare_records, configuration_fingerprint, load_record, render_json, render_markdown, validate_record


ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"


def main() -> int:
    baseline = load_record(FIXTURES / "baseline.json")
    candidate = load_record(FIXTURES / "candidate.json")
    ineligible = load_record(FIXTURES / "candidate-ineligible.json")
    unproven = load_record(FIXTURES / "candidate-unproven.json")
    accepted = compare_records(baseline, candidate)
    rejected = compare_records(baseline, ineligible)
    path_unknown = compare_records(baseline, unproven)

    correctness = copy.deepcopy(candidate)
    correctness["correctness"]["passed"] = False
    correctness_result = compare_records(baseline, correctness)
    stochastic = copy.deepcopy(candidate)
    stochastic["identity"]["sampling"] = {"mode": "stochastic", "seed": 7}

    try:
        validate_record(stochastic)
        stochastic_rejected = False
    except SchemaError:
        stochastic_rejected = True

    with tempfile.TemporaryDirectory(prefix="post-11a-lab-") as temporary:
        report_dir = Path(temporary)
        json_report = render_json(accepted)
        markdown_report = render_markdown(accepted)
        (report_dir / "comparison.json").write_text(json_report, encoding="utf-8")
        (report_dir / "comparison.md").write_text(markdown_report, encoding="utf-8")
        json_payload = json.loads(json_report)
        parity_values = (
            accepted.classification,
            accepted.experiment_kind,
            accepted.projection_contract,
            accepted.intervention["kind"],
            accepted.intervention["phase"],
            *accepted.intervention["reviewed_dependent_paths"],
            accepted.intervention_change["baseline"]["speculative_method"],
            accepted.intervention_change["candidate"]["speculative_method"],
            accepted.intervention_change["candidate"]["draft_artifact_fingerprint"],
            accepted.active_path["status"],
            accepted.active_path["expected_marker"],
            accepted.active_path["observed_marker"],
            accepted.active_path["counter_name"],
            str(accepted.active_path["counter_value"]),
        )
        report_agreement = json_payload == accepted.as_dict() and all(str(value) in markdown_report for value in parity_values)
        for side, record in (("baseline", baseline), ("candidate", candidate)):
            configuration = record["identity"]["runtime_configuration"]
            fingerprint = record["identity"]["runtime_configuration_fingerprint"]
            expected_lines = (
                f"{side.title()} configuration: `{fingerprint}`",
                f"{side.title()} method: `{configuration['speculative_method']}`",
                f"{side.title()} draft identity: `{configuration['draft_artifact_fingerprint'] or 'none'}`",
                f"{side.title()} method arguments: `{json.dumps(configuration['method_arguments'], sort_keys=True, separators=(',', ':'))}`",
            )
            report_agreement = (
                report_agreement
                and json_payload["intervention_change"][side] == configuration
                and json_payload[f"{side}_configuration_fingerprint"] == fingerprint
                and all(line in markdown_report.splitlines() for line in expected_lines)
            )

    command_templates = (ROOT / "command-templates.txt").read_text(encoding="utf-8")
    schema = json.loads((ROOT / "experiment.schema.json").read_text(encoding="utf-8"))
    command_contract_matches = (
        "--seed" not in command_templates
        and command_templates.count("--temp 0") == 2
        and schema["$defs"]["sampling"]["properties"]["mode"]["const"] == "greedy"
        and schema["$defs"]["sampling"]["properties"]["seed"]["type"] == "null"
    )

    unsafe_marker = copy.deepcopy(candidate)
    unsafe_marker["active_path"]["observed_marker"] = "../private/runtime.log"
    try:
        validate_record(unsafe_marker)
        unsafe_marker_rejected = False
    except SchemaError:
        unsafe_marker_rejected = True

    unsafe_method = copy.deepcopy(candidate)
    identity = unsafe_method["identity"]
    identity["runtime_configuration"]["speculative_method"] = "../private/runtime.log"
    identity["runtime_configuration_fingerprint"] = configuration_fingerprint(identity["runtime_configuration"])
    try:
        compare_records(baseline, unsafe_method)
        unsafe_method_rejected = False
    except SchemaError:
        unsafe_method_rejected = True

    checks = {
        "eligible_one_intervention": accepted.classification == "comparable",
        "runtime_optimization_classified_by_part11": accepted.experiment_kind == "runtime_configuration_optimization",
        "part10a_projection_versioned": accepted.projection_contract == "part-10a-v1-metric-projection",
        "configuration_fingerprints_preserved": bool(accepted.baseline_configuration_fingerprint and accepted.candidate_configuration_fingerprint),
        "active_path_preserved": accepted.active_path["status"] == "confirmed" and accepted.active_path["counter_value"] > 0,
        "unrelated_cache_change_rejected": rejected.classification == "ineligible" and "cache" in rejected.reasons,
        "unknown_active_path_rejected": path_unknown.classification == "active_path_unproven" and not path_unknown.metrics,
        "correctness_blocks_projection": correctness_result.classification == "correctness_failed" and not correctness_result.metrics,
        "stochastic_sampling_rejected": stochastic_rejected,
        "reports_agree": report_agreement,
        "command_template_matches_greedy_schema": command_contract_matches,
        "unsafe_marker_rejected": unsafe_marker_rejected,
        "unsafe_method_rejected_before_report": unsafe_method_rejected,
        "privacy_fields_absent": _privacy_check(baseline, candidate, ineligible, unproven, accepted.as_dict()),
        "cleanup_complete": not report_dir.exists(),
    }
    print(json.dumps({"conditions": checks, "passed": sum(checks.values()), "total": len(checks), "ok": all(checks.values())}, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


def _privacy_check(*values: object) -> bool:
    text = json.dumps(values, sort_keys=True).lower()
    forbidden = ('"prompt"', '"completion"', '"output_text"', '"hostname"', '"user"', '"ip_address"', '"model_path"', '"credential"')
    return not any(term in text for term in forbidden)


if __name__ == "__main__":
    raise SystemExit(main())
