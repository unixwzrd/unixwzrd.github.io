#!/usr/bin/env python3
"""Tests for the synthetic inference benchmark comparator."""

from __future__ import annotations

import copy
import json
import math
import unittest
from pathlib import Path

from benchmark_compare import SchemaError, compare_bundles, load_bundle, render_json, render_markdown, render_tsv, validate_bundle


ROOT = Path(__file__).resolve().parent


class ComparatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.baseline = load_bundle(ROOT / "fixtures" / "baseline.json")
        self.candidate = load_bundle(ROOT / "fixtures" / "candidate-optimization.json")

    def changed(self, section: str, field: str, value: object) -> dict:
        bundle = copy.deepcopy(self.candidate)
        bundle[section][field] = value
        return bundle

    def test_optimization_and_repeatability(self) -> None:
        result = compare_bundles(self.baseline, self.candidate)
        self.assertEqual((result.classification, result.experiment_kind), ("comparable", "optimization"))
        repeat = self.changed("identity", "source_fingerprint", self.baseline["identity"]["source_fingerprint"])
        self.assertEqual(compare_bundles(self.baseline, repeat).experiment_kind, "repeatability")

    def test_identity_mismatches_are_ineligible(self) -> None:
        cases = {
            "artifact_fingerprint": "6" * 64,
            "workload_fingerprint": "7" * 64,
            "warm_cold": "cold",
            "profiled": True,
            "context_tokens": 8192,
            "sampling_fingerprint": "8" * 64,
        }
        for field, value in cases.items():
            with self.subTest(field=field):
                result = compare_bundles(self.baseline, self.changed("identity", field, value))
                self.assertEqual(result.classification, "ineligible")
                self.assertIn(field, result.reasons)
                self.assertFalse(result.metrics)

    def test_engine_label_may_differ_when_contract_matches(self) -> None:
        result = compare_bundles(self.baseline, self.changed("identity", "engine", "engine-b"))
        self.assertEqual(result.classification, "comparable")

    def test_matching_profiled_runs_remain_ineligible(self) -> None:
        baseline = copy.deepcopy(self.baseline)
        candidate = copy.deepcopy(self.candidate)
        baseline["identity"]["profiled"] = True
        candidate["identity"]["profiled"] = True
        result = compare_bundles(baseline, candidate)
        self.assertEqual(result.classification, "ineligible")
        self.assertIn("profiled_runs_excluded", result.reasons)

    def test_correctness_failure_or_hash_drift_blocks_metrics(self) -> None:
        for field, value in (("passed", False), ("normalized_output_hash", "9" * 64)):
            with self.subTest(field=field):
                result = compare_bundles(self.baseline, self.changed("correctness", field, value))
                self.assertEqual(result.classification, "correctness_failed")
                self.assertFalse(result.metrics)

    def test_closed_schema_rejects_unknown_missing_and_bad_types(self) -> None:
        unknown = self.changed("identity", "engine", "engine-a")
        unknown["identity"]["hostname"] = "private-host"
        missing = copy.deepcopy(self.candidate)
        del missing["identity"]["artifact_fingerprint"]
        boolean = self.changed("identity", "memory_gb", True)
        wrong_version_type = copy.deepcopy(self.candidate)
        wrong_version_type["schema_version"] = 1.0
        nonfinite = copy.deepcopy(self.candidate)
        nonfinite["observations"][0]["ttft_ms"] = math.inf
        for bundle in (unknown, missing, boolean, wrong_version_type, nonfinite):
            with self.assertRaises(SchemaError):
                validate_bundle(bundle)

    def test_medians_and_direction_aware_outcomes(self) -> None:
        rows = {row["metric"]: row for row in compare_bundles(self.baseline, self.candidate).metrics}
        self.assertEqual(rows["ttft_ms"]["baseline_median"], 210.0)
        self.assertEqual(rows["ttft_ms"]["outcome"], "improved")
        self.assertEqual(rows["decode_tokens_per_s"]["outcome"], "improved")
        self.assertEqual(rows["peak_wired_mb"]["outcome"], "improved")

    def test_zero_baseline_percentage_is_none(self) -> None:
        baseline = copy.deepcopy(self.baseline)
        candidate = copy.deepcopy(self.candidate)
        for bundle in (baseline, candidate):
            for row in bundle["observations"]:
                row["ttft_ms"] = 0.0
        row = next(row for row in compare_bundles(baseline, candidate).metrics if row["metric"] == "ttft_ms")
        self.assertIsNone(row["percentage_delta"])

    def test_projections_are_deterministic_and_bounded(self) -> None:
        result = compare_bundles(self.baseline, self.candidate)
        projections = (render_json(result), render_tsv(result), render_markdown(result))
        self.assertEqual(projections, (render_json(result), render_tsv(result), render_markdown(result)))
        self.assertEqual(json.loads(projections[0])["classification"], "comparable")
        joined = "".join(projections).lower()
        for forbidden in ('"prompt":', '"completion":', '"output_text":', "private-host"):
            self.assertNotIn(forbidden, joined)


if __name__ == "__main__":
    unittest.main()
