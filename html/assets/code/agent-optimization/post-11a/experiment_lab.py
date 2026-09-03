#!/usr/bin/env python3
"""Validate and compare invented one-intervention inference records."""

from __future__ import annotations

import importlib.util
import json
import math
import re
import sys
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from types import ModuleType
from typing import Any


HEX64 = re.compile(r"^[0-9a-f]{64}$")
MARKER_ID = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
TOP_KEYS = {"schema_version", "identity", "intervention", "active_path", "correctness", "observations"}
IDENTITY_KEYS = {
    "run_id", "engine", "source_fingerprint", "binary_fingerprint",
    "target_artifact_fingerprint", "tokenizer_fingerprint", "template_fingerprint",
    "workload_fingerprint", "sampling_fingerprint", "extra_arguments_fingerprint",
    "runtime_configuration_fingerprint", "runtime_configuration", "sampling", "cache",
    "machine_class", "memory_gb", "warm_cold", "profiled", "concurrency",
    "batch_size", "context_tokens", "threads",
}
FINGERPRINT_FIELDS = {
    "source_fingerprint", "binary_fingerprint", "target_artifact_fingerprint",
    "tokenizer_fingerprint", "template_fingerprint", "workload_fingerprint",
    "sampling_fingerprint", "extra_arguments_fingerprint", "runtime_configuration_fingerprint",
}
FROZEN_IDENTITY_FIELDS = IDENTITY_KEYS - {"run_id", "runtime_configuration_fingerprint", "runtime_configuration"}
INTERVENTION_KEYS = {"kind", "phase", "reviewed_dependent_paths"}
REVIEWED_PATHS = [
    "runtime_configuration.speculative_method",
    "runtime_configuration.draft_artifact_fingerprint",
    "runtime_configuration.method_arguments",
]
ACTIVE_PATH_KEYS = {"status", "expected_marker", "observed_marker", "counter_name", "counter_value"}
CORRECTNESS_KEYS = {"passed", "normalized_output_hash"}
METRICS = {"ttft_ms", "prompt_tokens_per_s", "decode_tokens_per_s", "peak_wired_mb"}


class SchemaError(ValueError):
    """Raised when a record violates the closed teaching schema."""


@dataclass(frozen=True)
class ExperimentComparison:
    """Terminal classification and optional Part 10A metric projection."""

    classification: str
    experiment_kind: str | None
    reasons: tuple[str, ...]
    baseline_configuration_fingerprint: str
    candidate_configuration_fingerprint: str
    intervention: dict[str, Any]
    intervention_change: dict[str, Any]
    active_path: dict[str, Any]
    projection_contract: str | None
    metrics: tuple[dict[str, Any], ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "classification": self.classification,
            "experiment_kind": self.experiment_kind,
            "reasons": list(self.reasons),
            "baseline_configuration_fingerprint": self.baseline_configuration_fingerprint,
            "candidate_configuration_fingerprint": self.candidate_configuration_fingerprint,
            "intervention": self.intervention,
            "intervention_change": self.intervention_change,
            "active_path": self.active_path,
            "projection_contract": self.projection_contract,
            "metrics": list(self.metrics),
        }


def _exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise SchemaError(f"{label} keys differ; missing={sorted(expected - actual)}, unknown={sorted(actual - expected)}")


def _integer(value: Any, label: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise SchemaError(f"{label} must be an integer >= {minimum}")
    return value


def _fingerprint(value: Any, label: str) -> str:
    if not isinstance(value, str) or not HEX64.fullmatch(value):
        raise SchemaError(f"{label} must be lowercase 64-hex")
    return value


def configuration_fingerprint(configuration: dict[str, Any]) -> str:
    """Return the canonical SHA-256 fingerprint for a runtime configuration."""
    encoded = json.dumps(configuration, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()


def validate_record(value: Any) -> dict[str, Any]:
    """Return a validated experiment record or raise SchemaError."""
    if not isinstance(value, dict):
        raise SchemaError("record must be an object")
    _exact_keys(value, TOP_KEYS, "record")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise SchemaError("schema_version must be integer 1")

    identity = value["identity"]
    intervention = value["intervention"]
    active_path = value["active_path"]
    correctness = value["correctness"]
    observations = value["observations"]
    for item, label in ((identity, "identity"), (intervention, "intervention"), (active_path, "active_path"), (correctness, "correctness")):
        if not isinstance(item, dict):
            raise SchemaError(f"{label} must be an object")
    _exact_keys(identity, IDENTITY_KEYS, "identity")
    _exact_keys(intervention, INTERVENTION_KEYS, "intervention")
    _exact_keys(active_path, ACTIVE_PATH_KEYS, "active_path")
    _exact_keys(correctness, CORRECTNESS_KEYS, "correctness")

    for field in FINGERPRINT_FIELDS:
        _fingerprint(identity[field], f"identity.{field}")
    for field in ("run_id", "engine", "machine_class"):
        if not isinstance(identity[field], str) or not identity[field].strip():
            raise SchemaError(f"identity.{field} must be a nonempty string")
    for field in ("memory_gb", "concurrency", "batch_size", "context_tokens", "threads"):
        _integer(identity[field], f"identity.{field}", minimum=1)
    if type(identity["profiled"]) is not bool:
        raise SchemaError("identity.profiled must be Boolean")
    if identity["warm_cold"] not in {"warm", "cold"}:
        raise SchemaError("identity.warm_cold must be warm or cold")

    sampling = identity["sampling"]
    cache = identity["cache"]
    configuration = identity["runtime_configuration"]
    for item, label in ((sampling, "identity.sampling"), (cache, "identity.cache"), (configuration, "identity.runtime_configuration")):
        if not isinstance(item, dict):
            raise SchemaError(f"{label} must be an object")
    _exact_keys(sampling, {"mode", "seed"}, "identity.sampling")
    if sampling != {"mode": "greedy", "seed": None}:
        raise SchemaError("identity.sampling must be greedy with a null seed")
    _exact_keys(cache, {"kv_format", "prompt_cache"}, "identity.cache")
    if not isinstance(cache["kv_format"], str) or not cache["kv_format"].strip() or type(cache["prompt_cache"]) is not bool:
        raise SchemaError("identity.cache has invalid values")
    _exact_keys(configuration, {"speculative_method", "draft_artifact_fingerprint", "method_arguments"}, "identity.runtime_configuration")
    if not isinstance(configuration["speculative_method"], str) or configuration["speculative_method"] not in {"none", "candidate_method"}:
        raise SchemaError("runtime speculative_method must be none or candidate_method")
    draft_fingerprint = configuration["draft_artifact_fingerprint"]
    if draft_fingerprint is not None:
        _fingerprint(draft_fingerprint, "identity.runtime_configuration.draft_artifact_fingerprint")
    arguments = configuration["method_arguments"]
    if not isinstance(arguments, dict):
        raise SchemaError("method_arguments must be an object")
    _exact_keys(arguments, {"draft_tokens"}, "identity.runtime_configuration.method_arguments")
    _integer(arguments["draft_tokens"], "method_arguments.draft_tokens")
    if configuration_fingerprint(configuration) != identity["runtime_configuration_fingerprint"]:
        raise SchemaError("runtime_configuration_fingerprint does not match canonical configuration")

    if intervention != {"kind": "speculative_method", "phase": "decode", "reviewed_dependent_paths": REVIEWED_PATHS}:
        raise SchemaError("intervention must use the reviewed speculative_method contract")
    if active_path["status"] not in {"confirmed", "inactive", "contradictory", "unknown"}:
        raise SchemaError("active_path.status is invalid")
    for field in ("expected_marker", "observed_marker", "counter_name"):
        if not isinstance(active_path[field], str):
            raise SchemaError(f"active_path.{field} must be a string")
    if not MARKER_ID.fullmatch(active_path["expected_marker"]):
        raise SchemaError("active_path.expected_marker must be a sanitized symbolic identifier")
    if active_path["observed_marker"] and not MARKER_ID.fullmatch(active_path["observed_marker"]):
        raise SchemaError("active_path.observed_marker must be empty or a sanitized symbolic identifier")
    if active_path["counter_name"] != "accepted_draft_tokens":
        raise SchemaError("active_path marker or counter contract is invalid")
    _integer(active_path["counter_value"], "active_path.counter_value")
    if type(correctness["passed"]) is not bool:
        raise SchemaError("correctness.passed must be Boolean")
    _fingerprint(correctness["normalized_output_hash"], "correctness.normalized_output_hash")

    if not isinstance(observations, list) or len(observations) < 3:
        raise SchemaError("observations must contain at least three rows")
    for index, row in enumerate(observations):
        if not isinstance(row, dict):
            raise SchemaError(f"observations[{index}] must be an object")
        _exact_keys(row, METRICS, f"observations[{index}]")
        for name, metric in row.items():
            if isinstance(metric, bool) or not isinstance(metric, (int, float)) or not math.isfinite(metric) or metric < 0:
                raise SchemaError(f"observations[{index}].{name} must be finite and nonnegative")
    return value


def load_record(path: str | Path) -> dict[str, Any]:
    """Load and validate a JSON experiment record."""
    with Path(path).open(encoding="utf-8") as handle:
        return validate_record(json.load(handle))


def _terminal(baseline: dict[str, Any], candidate: dict[str, Any], classification: str, reasons: tuple[str, ...]) -> ExperimentComparison:
    return ExperimentComparison(
        classification=classification,
        experiment_kind=None,
        reasons=reasons,
        baseline_configuration_fingerprint=baseline["identity"]["runtime_configuration_fingerprint"],
        candidate_configuration_fingerprint=candidate["identity"]["runtime_configuration_fingerprint"],
        intervention=candidate["intervention"],
        intervention_change=_intervention_change(baseline, candidate),
        active_path=candidate["active_path"],
        projection_contract=None,
        metrics=(),
    )


def _intervention_change(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    """Return the sanitized reviewed runtime-configuration change."""
    return {
        "baseline": baseline["identity"]["runtime_configuration"],
        "candidate": candidate["identity"]["runtime_configuration"],
    }


def compare_records(baseline: dict[str, Any], candidate: dict[str, Any], *, part10a_path: Path | None = None) -> ExperimentComparison:
    """Classify one runtime intervention and project eligible metrics."""
    baseline = validate_record(baseline)
    candidate = validate_record(candidate)
    mismatches = tuple(sorted(field for field in FROZEN_IDENTITY_FIELDS if baseline["identity"][field] != candidate["identity"][field]))
    if mismatches:
        return _terminal(baseline, candidate, "ineligible", mismatches)
    if baseline["intervention"] != candidate["intervention"]:
        return _terminal(baseline, candidate, "ineligible", ("intervention_contract_mismatch",))
    if baseline["identity"]["profiled"]:
        return _terminal(baseline, candidate, "ineligible", ("profiled_runs_excluded",))
    baseline_config = baseline["identity"]["runtime_configuration"]
    candidate_config = candidate["identity"]["runtime_configuration"]
    if baseline_config["speculative_method"] != "none" or candidate_config["speculative_method"] != "candidate_method":
        return _terminal(baseline, candidate, "ineligible", ("abstract_method_transition_required",))
    if baseline["identity"]["runtime_configuration_fingerprint"] == candidate["identity"]["runtime_configuration_fingerprint"]:
        return _terminal(baseline, candidate, "ineligible", ("configuration_unchanged",))
    if baseline_config["draft_artifact_fingerprint"] is not None or baseline_config["method_arguments"]["draft_tokens"] != 0:
        return _terminal(baseline, candidate, "ineligible", ("baseline_intervention_not_disabled",))
    active = candidate["active_path"]
    if active["status"] != "confirmed" or active["expected_marker"] != active["observed_marker"] or active["counter_value"] <= 0:
        return _terminal(baseline, candidate, "active_path_unproven", ("candidate_active_path_not_confirmed",))
    baseline_active = baseline["active_path"]
    if baseline_active["status"] != "confirmed" or baseline_active["expected_marker"] != baseline_active["observed_marker"] or baseline_active["counter_value"] != 0:
        return _terminal(baseline, candidate, "active_path_unproven", ("baseline_disabled_path_not_confirmed",))
    correctness_reasons: list[str] = []
    if not baseline["correctness"]["passed"]:
        correctness_reasons.append("baseline_correctness_failed")
    if not candidate["correctness"]["passed"]:
        correctness_reasons.append("candidate_correctness_failed")
    if baseline["correctness"]["normalized_output_hash"] != candidate["correctness"]["normalized_output_hash"]:
        correctness_reasons.append("normalized_output_hash_mismatch")
    if correctness_reasons:
        return _terminal(baseline, candidate, "correctness_failed", tuple(correctness_reasons))

    metrics = _part10a_projection(baseline, candidate, part10a_path=part10a_path)
    return ExperimentComparison(
        classification="comparable",
        experiment_kind="runtime_configuration_optimization",
        reasons=(),
        baseline_configuration_fingerprint=baseline["identity"]["runtime_configuration_fingerprint"],
        candidate_configuration_fingerprint=candidate["identity"]["runtime_configuration_fingerprint"],
        intervention=candidate["intervention"],
        intervention_change=_intervention_change(baseline, candidate),
        active_path=candidate["active_path"],
        projection_contract="part-10a-v1-metric-projection",
        metrics=metrics,
    )


def _load_part10a(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("post10a_benchmark_compare", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load Part 10A comparator from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _part10a_projection(baseline: dict[str, Any], candidate: dict[str, Any], *, part10a_path: Path | None) -> tuple[dict[str, Any], ...]:
    comparator_path = part10a_path or Path(__file__).resolve().parents[1] / "post-10a" / "benchmark_compare.py"
    module = _load_part10a(comparator_path)

    def transform(record: dict[str, Any]) -> dict[str, Any]:
        identity = record["identity"]
        return {
            "schema_version": 1,
            "identity": {
                "run_id": identity["run_id"],
                "engine": identity["engine"],
                "source_fingerprint": identity["source_fingerprint"],
                "artifact_fingerprint": identity["target_artifact_fingerprint"],
                "workload_fingerprint": identity["workload_fingerprint"],
                "machine_class": identity["machine_class"],
                "memory_gb": identity["memory_gb"],
                "warm_cold": identity["warm_cold"],
                "profiled": identity["profiled"],
                "concurrency": identity["concurrency"],
                "batch_size": identity["batch_size"],
                "context_tokens": identity["context_tokens"],
                "sampling_fingerprint": identity["sampling_fingerprint"],
            },
            "correctness": record["correctness"],
            "observations": record["observations"],
        }

    result = module.compare_bundles(transform(baseline), transform(candidate))
    if result.classification != "comparable":
        raise RuntimeError(f"Part 10A metric projection rejected an eligible Part 11 pair: {result.reasons}")
    return tuple(result.metrics)


def render_json(result: ExperimentComparison) -> str:
    """Render one stable JSON report."""
    return json.dumps(result.as_dict(), indent=2, sort_keys=True) + "\n"


def render_markdown(result: ExperimentComparison) -> str:
    """Render one concise Markdown report."""
    dependent_paths = ", ".join(result.intervention.get("reviewed_dependent_paths", []))
    baseline_change = result.intervention_change.get("baseline", {})
    candidate_change = result.intervention_change.get("candidate", {})
    baseline_arguments = json.dumps(baseline_change.get("method_arguments", {}), sort_keys=True, separators=(",", ":"))
    candidate_arguments = json.dumps(candidate_change.get("method_arguments", {}), sort_keys=True, separators=(",", ":"))
    lines = [
        f"Classification: `{result.classification}`",
        f"Experiment: `{result.experiment_kind or 'none'}`",
        f"Projection: `{result.projection_contract or 'none'}`",
        f"Reasons: `{', '.join(result.reasons) if result.reasons else 'none'}`",
        f"Baseline configuration: `{result.baseline_configuration_fingerprint}`",
        f"Candidate configuration: `{result.candidate_configuration_fingerprint}`",
        f"Intervention kind: `{result.intervention.get('kind', 'unknown')}`",
        f"Intervention phase: `{result.intervention.get('phase', 'unknown')}`",
        f"Reviewed dependent paths: `{dependent_paths}`",
        f"Baseline method: `{baseline_change.get('speculative_method', 'unknown')}`",
        f"Baseline draft identity: `{baseline_change.get('draft_artifact_fingerprint') or 'none'}`",
        f"Baseline method arguments: `{baseline_arguments}`",
        f"Candidate method: `{candidate_change.get('speculative_method', 'unknown')}`",
        f"Candidate draft identity: `{candidate_change.get('draft_artifact_fingerprint') or 'none'}`",
        f"Candidate method arguments: `{candidate_arguments}`",
        f"Active-path status: `{result.active_path.get('status', 'unknown')}`",
        f"Expected marker ID: `{result.active_path.get('expected_marker', '')}`",
        f"Observed marker ID: `{result.active_path.get('observed_marker', '')}`",
        f"Counter: `{result.active_path.get('counter_name', '')}`",
        f"Counter value: `{result.active_path.get('counter_value', '')}`",
    ]
    if result.metrics:
        lines.extend(("", "| Metric | Unit | Direction | Baseline median | Candidate median | Outcome |", "| --- | --- | --- | ---: | ---: | --- |"))
        for row in result.metrics:
            lines.append(f"| {row['metric']} | {row['unit']} | {row['direction']} | {row['baseline_median']:.3f} | {row['candidate_median']:.3f} | {row['outcome']} |")
    return "\n".join(lines) + "\n"
