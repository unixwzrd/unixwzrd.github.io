#!/usr/bin/env python3
"""Validate and compare synthetic inference benchmark bundles."""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any


HEX64 = re.compile(r"^[0-9a-f]{64}$")
TOP_KEYS = {"schema_version", "identity", "correctness", "observations"}
IDENTITY_TYPES = {
    "run_id": str,
    "engine": str,
    "source_fingerprint": str,
    "artifact_fingerprint": str,
    "workload_fingerprint": str,
    "machine_class": str,
    "memory_gb": int,
    "warm_cold": str,
    "profiled": bool,
    "concurrency": int,
    "batch_size": int,
    "context_tokens": int,
    "sampling_fingerprint": str,
}
CORRECTNESS_TYPES = {"passed": bool, "normalized_output_hash": str}
REQUIRED_METRICS = {
    "ttft_ms": ("lower", "ms"),
    "prompt_tokens_per_s": ("higher", "tokens/s"),
    "decode_tokens_per_s": ("higher", "tokens/s"),
    "peak_wired_mb": ("lower", "MiB"),
}
OPTIONAL_METRICS = {
    "ssd_read_bytes": ("lower", "bytes"),
    "warm_restore_latency_ms": ("lower", "ms"),
}
ALL_METRICS = REQUIRED_METRICS | OPTIONAL_METRICS
STRICT_IDENTITY_FIELDS = (
    "artifact_fingerprint",
    "workload_fingerprint",
    "machine_class",
    "memory_gb",
    "warm_cold",
    "profiled",
    "concurrency",
    "batch_size",
    "context_tokens",
    "sampling_fingerprint",
)


class SchemaError(ValueError):
    """Raised when a bundle violates the closed teaching schema."""


@dataclass(frozen=True)
class Comparison:
    classification: str
    experiment_kind: str | None
    reasons: tuple[str, ...]
    metrics: tuple[dict[str, Any], ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "classification": self.classification,
            "experiment_kind": self.experiment_kind,
            "reasons": list(self.reasons),
            "metrics": list(self.metrics),
        }


def _expect_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        unknown = sorted(actual - expected)
        raise SchemaError(f"{label} keys differ; missing={missing}, unknown={unknown}")


def _expect_type(value: Any, expected: type, label: str) -> None:
    if expected is int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise SchemaError(f"{label} must be an integer")
    elif type(value) is not expected:
        raise SchemaError(f"{label} must be {expected.__name__}")


def validate_bundle(bundle: Any) -> dict[str, Any]:
    """Return a validated bundle or raise SchemaError."""
    if not isinstance(bundle, dict):
        raise SchemaError("bundle must be an object")
    _expect_exact_keys(bundle, TOP_KEYS, "bundle")
    if type(bundle["schema_version"]) is not int or bundle["schema_version"] != 1:
        raise SchemaError("schema_version must be integer 1")

    identity = bundle["identity"]
    correctness = bundle["correctness"]
    observations = bundle["observations"]
    if not isinstance(identity, dict) or not isinstance(correctness, dict):
        raise SchemaError("identity and correctness must be objects")
    _expect_exact_keys(identity, set(IDENTITY_TYPES), "identity")
    _expect_exact_keys(correctness, set(CORRECTNESS_TYPES), "correctness")

    for key, expected in IDENTITY_TYPES.items():
        _expect_type(identity[key], expected, f"identity.{key}")
    for key, expected in CORRECTNESS_TYPES.items():
        _expect_type(correctness[key], expected, f"correctness.{key}")

    for key in ("run_id", "engine", "machine_class"):
        if not identity[key].strip():
            raise SchemaError(f"identity.{key} must not be empty")
    for key in (
        "source_fingerprint",
        "artifact_fingerprint",
        "workload_fingerprint",
        "sampling_fingerprint",
    ):
        if not HEX64.fullmatch(identity[key]):
            raise SchemaError(f"identity.{key} must be lowercase 64-hex")
    if not HEX64.fullmatch(correctness["normalized_output_hash"]):
        raise SchemaError("correctness.normalized_output_hash must be lowercase 64-hex")
    if identity["warm_cold"] not in {"warm", "cold"}:
        raise SchemaError("identity.warm_cold must be warm or cold")
    for key in ("memory_gb", "concurrency", "batch_size", "context_tokens"):
        if identity[key] <= 0:
            raise SchemaError(f"identity.{key} must be positive")

    if not isinstance(observations, list) or len(observations) < 3:
        raise SchemaError("observations must contain at least three rows")
    metric_keys: set[str] | None = None
    for index, row in enumerate(observations):
        if not isinstance(row, dict):
            raise SchemaError(f"observations[{index}] must be an object")
        keys = set(row)
        if not set(REQUIRED_METRICS).issubset(keys) or not keys.issubset(ALL_METRICS):
            raise SchemaError(f"observations[{index}] has missing or unknown metrics")
        if metric_keys is None:
            metric_keys = keys
        elif keys != metric_keys:
            raise SchemaError("every observation must contain the same metric keys")
        for key, value in row.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise SchemaError(f"observations[{index}].{key} must be numeric")
            if not math.isfinite(value) or value < 0:
                raise SchemaError(f"observations[{index}].{key} must be finite and nonnegative")
    return bundle


def load_bundle(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        return validate_bundle(json.load(handle))


def compare_bundles(baseline: dict[str, Any], candidate: dict[str, Any]) -> Comparison:
    baseline = validate_bundle(baseline)
    candidate = validate_bundle(candidate)
    mismatches = tuple(
        field
        for field in STRICT_IDENTITY_FIELDS
        if baseline["identity"][field] != candidate["identity"][field]
    )
    baseline_keys = set(baseline["observations"][0])
    candidate_keys = set(candidate["observations"][0])
    if baseline_keys != candidate_keys:
        mismatches += ("metric_set",)
    if mismatches:
        return Comparison("ineligible", None, mismatches, ())
    if baseline["identity"]["profiled"]:
        return Comparison("ineligible", None, ("profiled_runs_excluded",), ())

    correctness_reasons: list[str] = []
    if not baseline["correctness"]["passed"]:
        correctness_reasons.append("baseline_correctness_failed")
    if not candidate["correctness"]["passed"]:
        correctness_reasons.append("candidate_correctness_failed")
    if (
        baseline["correctness"]["normalized_output_hash"]
        != candidate["correctness"]["normalized_output_hash"]
    ):
        correctness_reasons.append("normalized_output_hash_mismatch")
    if correctness_reasons:
        return Comparison("correctness_failed", None, tuple(correctness_reasons), ())

    experiment_kind = (
        "repeatability"
        if baseline["identity"]["source_fingerprint"]
        == candidate["identity"]["source_fingerprint"]
        else "optimization"
    )
    rows: list[dict[str, Any]] = []
    for name in sorted(baseline_keys):
        direction, unit = ALL_METRICS[name]
        baseline_value = statistics.median(row[name] for row in baseline["observations"])
        candidate_value = statistics.median(row[name] for row in candidate["observations"])
        delta = candidate_value - baseline_value
        percent_delta = None if baseline_value == 0 else (delta / baseline_value) * 100
        directed_delta = delta if direction == "higher" else -delta
        outcome = "unchanged" if delta == 0 else ("improved" if directed_delta > 0 else "regressed")
        rows.append(
            {
                "metric": name,
                "unit": unit,
                "direction": direction,
                "baseline_median": baseline_value,
                "candidate_median": candidate_value,
                "absolute_delta": delta,
                "percentage_delta": percent_delta,
                "outcome": outcome,
            }
        )
    return Comparison("comparable", experiment_kind, (), tuple(rows))


def render_json(result: Comparison) -> str:
    return json.dumps(result.as_dict(), indent=2, sort_keys=True) + "\n"


def render_tsv(result: Comparison) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter="\t", lineterminator="\n")
    writer.writerow(("classification", result.classification))
    writer.writerow(("experiment_kind", result.experiment_kind or ""))
    writer.writerow(("reasons", ",".join(result.reasons)))
    writer.writerow(())
    writer.writerow(("metric", "unit", "direction", "baseline_median", "candidate_median", "absolute_delta", "percentage_delta", "outcome"))
    for row in result.metrics:
        writer.writerow(row[key] if row[key] is not None else "" for key in ("metric", "unit", "direction", "baseline_median", "candidate_median", "absolute_delta", "percentage_delta", "outcome"))
    return output.getvalue()


def render_markdown(result: Comparison) -> str:
    lines = [
        f"Classification: `{result.classification}`",
        f"Experiment: `{result.experiment_kind or 'none'}`",
        f"Reasons: `{', '.join(result.reasons) if result.reasons else 'none'}`",
    ]
    if result.metrics:
        lines.extend(("", "| Metric | Unit | Direction | Baseline median | Candidate median | Delta | Percent delta | Outcome |", "| --- | --- | --- | ---: | ---: | ---: | ---: | --- |"))
        for row in result.metrics:
            percent = "n/a" if row["percentage_delta"] is None else f'{row["percentage_delta"]:.3f}%'
            lines.append(f'| {row["metric"]} | {row["unit"]} | {row["direction"]} | {row["baseline_median"]:.3f} | {row["candidate_median"]:.3f} | {row["absolute_delta"]:.3f} | {percent} | {row["outcome"]} |')
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--format", choices=("json", "tsv", "markdown"), default="markdown")
    args = parser.parse_args()
    result = compare_bundles(load_bundle(args.baseline), load_bundle(args.candidate))
    print({"json": render_json, "tsv": render_tsv, "markdown": render_markdown}[args.format](result), end="")
    return 0 if result.classification == "comparable" else 2


if __name__ == "__main__":
    raise SystemExit(main())
