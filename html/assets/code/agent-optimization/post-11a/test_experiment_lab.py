#!/usr/bin/env python3
"""Tests for the model-neutral Hands-On 11A companion."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from experiment_lab import SchemaError, compare_records, configuration_fingerprint, load_record, render_json, render_markdown, validate_record


ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"


class ExperimentLabTests(unittest.TestCase):
    def setUp(self) -> None:
        self.baseline = load_record(FIXTURES / "baseline.json")
        self.candidate = load_record(FIXTURES / "candidate.json")

    def test_eligible_structured_intervention(self) -> None:
        result = compare_records(self.baseline, self.candidate)
        self.assertEqual(result.classification, "comparable")
        self.assertEqual(result.experiment_kind, "runtime_configuration_optimization")
        self.assertEqual(result.projection_contract, "part-10a-v1-metric-projection")
        self.assertTrue(result.metrics)

    def test_stochastic_sampling_rejected_even_with_seed(self) -> None:
        changed = copy.deepcopy(self.candidate)
        changed["identity"]["sampling"] = {"mode": "stochastic", "seed": 7}
        with self.assertRaises(SchemaError):
            validate_record(changed)

    def test_unknown_field_rejected(self) -> None:
        changed = copy.deepcopy(self.candidate)
        changed["identity"]["hostname"] = "not accepted"
        with self.assertRaises(SchemaError):
            validate_record(changed)

    def test_missing_identity_rejected(self) -> None:
        changed = copy.deepcopy(self.candidate)
        del changed["identity"]["binary_fingerprint"]
        with self.assertRaises(SchemaError):
            validate_record(changed)

    def test_boolean_numeric_rejected(self) -> None:
        changed = copy.deepcopy(self.candidate)
        changed["identity"]["threads"] = True
        with self.assertRaises(SchemaError):
            validate_record(changed)

    def test_canonical_configuration_fingerprint_required(self) -> None:
        changed = copy.deepcopy(self.candidate)
        changed["identity"]["runtime_configuration"]["method_arguments"]["draft_tokens"] = 5
        with self.assertRaises(SchemaError):
            validate_record(changed)
        changed["identity"]["runtime_configuration_fingerprint"] = configuration_fingerprint(changed["identity"]["runtime_configuration"])
        validate_record(changed)

    def test_unrelated_change_rejected(self) -> None:
        changed = copy.deepcopy(self.candidate)
        changed["identity"]["cache"]["kv_format"] = "invented-q8"
        result = compare_records(self.baseline, changed)
        self.assertEqual(result.classification, "ineligible")
        self.assertIn("cache", result.reasons)

    def test_reviewed_dependent_fields_accepted(self) -> None:
        config = self.candidate["identity"]["runtime_configuration"]
        self.assertEqual(config["speculative_method"], "candidate_method")
        self.assertIsNotNone(config["draft_artifact_fingerprint"])
        self.assertGreater(config["method_arguments"]["draft_tokens"], 0)
        self.assertEqual(compare_records(self.baseline, self.candidate).classification, "comparable")

    def test_warm_cold_mismatch_rejected(self) -> None:
        changed = copy.deepcopy(self.candidate)
        changed["identity"]["warm_cold"] = "cold"
        result = compare_records(self.baseline, changed)
        self.assertEqual(result.classification, "ineligible")
        self.assertIn("warm_cold", result.reasons)

    def test_profiled_pair_rejected(self) -> None:
        baseline = copy.deepcopy(self.baseline)
        candidate = copy.deepcopy(self.candidate)
        baseline["identity"]["profiled"] = True
        candidate["identity"]["profiled"] = True
        result = compare_records(baseline, candidate)
        self.assertEqual(result.classification, "ineligible")
        self.assertIn("profiled_runs_excluded", result.reasons)

    def test_active_path_unknown_rejected(self) -> None:
        changed = copy.deepcopy(self.candidate)
        changed["active_path"]["status"] = "unknown"
        changed["active_path"]["observed_marker"] = ""
        result = compare_records(self.baseline, changed)
        self.assertEqual(result.classification, "active_path_unproven")
        self.assertFalse(result.metrics)

    def test_correctness_failure_blocks_metrics(self) -> None:
        changed = copy.deepcopy(self.candidate)
        changed["correctness"]["passed"] = False
        result = compare_records(self.baseline, changed)
        self.assertEqual(result.classification, "correctness_failed")
        self.assertFalse(result.metrics)

    def test_output_drift_blocks_metrics(self) -> None:
        changed = copy.deepcopy(self.candidate)
        changed["correctness"]["normalized_output_hash"] = "f" * 64
        result = compare_records(self.baseline, changed)
        self.assertEqual(result.classification, "correctness_failed")
        self.assertIn("normalized_output_hash_mismatch", result.reasons)

    def test_report_preserves_contract_evidence(self) -> None:
        result = compare_records(self.baseline, self.candidate)
        json_report = render_json(result)
        markdown_report = render_markdown(result)
        payload = json.loads(json_report)
        self.assertEqual(payload, result.as_dict())
        self.assertIn(result.baseline_configuration_fingerprint, json_report)
        self.assertIn(result.candidate_configuration_fingerprint, markdown_report)
        expected_values = (
            result.classification,
            result.experiment_kind,
            result.projection_contract,
            result.intervention["kind"],
            result.intervention["phase"],
            *result.intervention["reviewed_dependent_paths"],
            result.intervention_change["baseline"]["speculative_method"],
            result.intervention_change["candidate"]["speculative_method"],
            result.intervention_change["candidate"]["draft_artifact_fingerprint"],
            result.active_path["status"],
            result.active_path["expected_marker"],
            result.active_path["observed_marker"],
            result.active_path["counter_name"],
            str(result.active_path["counter_value"]),
        )
        for value in expected_values:
            self.assertIn(str(value), json_report)
            self.assertIn(str(value), markdown_report)
        for side, record in (("baseline", self.baseline), ("candidate", self.candidate)):
            configuration = record["identity"]["runtime_configuration"]
            fingerprint = record["identity"]["runtime_configuration_fingerprint"]
            self.assertEqual(payload["intervention_change"][side], configuration)
            self.assertEqual(payload[f"{side}_configuration_fingerprint"], fingerprint)
            expected_lines = (
                f"{side.title()} configuration: `{fingerprint}`",
                f"{side.title()} method: `{configuration['speculative_method']}`",
                f"{side.title()} draft identity: `{configuration['draft_artifact_fingerprint'] or 'none'}`",
                f"{side.title()} method arguments: `{json.dumps(configuration['method_arguments'], sort_keys=True, separators=(',', ':'))}`",
            )
            for line in expected_lines:
                self.assertIn(line, markdown_report.splitlines())

    def test_unsafe_method_rejected_before_report(self) -> None:
        for side in ("baseline", "candidate"):
            with self.subTest(side=side):
                baseline = copy.deepcopy(self.baseline)
                candidate = copy.deepcopy(self.candidate)
                identity = (baseline if side == "baseline" else candidate)["identity"]
                identity["runtime_configuration"]["speculative_method"] = "../private/runtime.log"
                identity["runtime_configuration_fingerprint"] = configuration_fingerprint(identity["runtime_configuration"])
                with self.assertRaisesRegex(SchemaError, "speculative_method must be none or candidate_method"):
                    compare_records(baseline, candidate)

    def test_method_vocabulary_matches_schema(self) -> None:
        schema = json.loads((ROOT / "experiment.schema.json").read_text(encoding="utf-8"))
        methods = schema["$defs"]["runtimeConfiguration"]["properties"]["speculative_method"]["enum"]
        self.assertEqual(methods, ["none", "candidate_method"])
        for method in (*methods, "unreviewed_method", "", None, []):
            with self.subTest(method=method):
                changed = copy.deepcopy(self.candidate)
                identity = changed["identity"]
                identity["runtime_configuration"]["speculative_method"] = method
                identity["runtime_configuration_fingerprint"] = configuration_fingerprint(identity["runtime_configuration"])
                if method in methods:
                    validate_record(changed)
                else:
                    with self.assertRaises(SchemaError):
                        validate_record(changed)

    def test_unsafe_marker_rejected(self) -> None:
        changed = copy.deepcopy(self.candidate)
        changed["active_path"]["observed_marker"] = "../private/runtime.log"
        with self.assertRaises(SchemaError):
            validate_record(changed)

    def test_command_template_matches_greedy_schema(self) -> None:
        commands = (ROOT / "command-templates.txt").read_text(encoding="utf-8")
        schema = json.loads((ROOT / "experiment.schema.json").read_text(encoding="utf-8"))
        self.assertNotIn("--seed", commands)
        self.assertEqual(commands.count("--temp 0"), 2)
        sampling = schema["$defs"]["sampling"]["properties"]
        self.assertEqual(sampling["mode"]["const"], "greedy")
        self.assertEqual(sampling["seed"]["type"], "null")

    def test_temporary_report_cleanup(self) -> None:
        result = compare_records(self.baseline, self.candidate)
        with tempfile.TemporaryDirectory(prefix="post-11a-test-") as temporary:
            directory = Path(temporary)
            (directory / "report.json").write_text(render_json(result), encoding="utf-8")
            self.assertTrue((directory / "report.json").is_file())
        self.assertFalse(directory.exists())


if __name__ == "__main__":
    unittest.main()
