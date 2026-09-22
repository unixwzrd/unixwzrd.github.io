from __future__ import annotations

import ast
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from release_evidence import NOT_READY, PacketError, READY, main, render_text, validate_packet


ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"


def load(name: str = "review-ready.json") -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class ReleaseEvidenceTests(unittest.TestCase):
    def assert_code(self, packet: dict, code: str) -> None:
        with self.assertRaises(PacketError) as caught:
            validate_packet(packet)
        self.assertEqual(caught.exception.code, code)

    def test_ready_packet_is_review_ready(self) -> None:
        result = validate_packet(load())
        self.assertEqual(result["decision"], READY)
        self.assertEqual(result["passed_gates"], 2)
        self.assertEqual(result["incomplete_gates"], 2)
        self.assertFalse(result["release_ready_inferred"])
        self.assertFalse(result["approval_inferred"])

    def test_ready_result_is_deterministic(self) -> None:
        self.assertEqual(validate_packet(load()), validate_packet(load()))

    def test_text_never_emits_inferred_terminal_claims(self) -> None:
        text = render_text(validate_packet(load()))
        self.assertIn(READY, text)
        self.assertNotIn("RELEASE READY", text)
        self.assertNotIn("APPROVED", text)
        self.assertNotIn("PUBLISHED", text)

    def test_validation_does_not_mutate_input(self) -> None:
        packet = load()
        original = copy.deepcopy(packet)
        validate_packet(packet)
        self.assertEqual(packet, original)

    def test_missing_gate_is_rejected(self) -> None:
        self.assert_code(load("missing-gate.json"), "E_MISSING_GATE")

    def test_identity_mismatch_is_rejected(self) -> None:
        self.assert_code(load("identity-mismatch.json"), "E_IDENTITY")

    def test_manifest_mismatch_is_rejected(self) -> None:
        self.assert_code(load("manifest-mismatch.json"), "E_IDENTITY")

    def test_stale_evidence_is_rejected(self) -> None:
        self.assert_code(load("stale-evidence.json"), "E_STALE")

    def test_unsupported_approval_is_rejected(self) -> None:
        self.assert_code(load("unsupported-approval.json"), "E_APPROVAL_CLAIM")

    def test_complete_acceptance_requires_all_required_passes(self) -> None:
        packet = load()
        packet["claims"]["acceptance"] = "complete"
        self.assert_code(packet, "E_ACCEPTANCE_CLAIM")

    def test_complete_acceptance_is_declaratively_valid_when_all_pass(self) -> None:
        packet = load()
        for item in packet["evidence"]:
            item["result"] = "pass"
            item["architectures"] = ["test-architecture"]
        packet["claims"]["acceptance"] = "complete"
        result = validate_packet(packet)
        self.assertEqual(result["acceptance_claim"], "complete")
        self.assertFalse(result["release_ready_inferred"])

    def test_supported_approval_requires_matching_gate_evidence(self) -> None:
        packet = load()
        packet["evidence"].append(
            {
                "evidence_id": "approval-record",
                "gate_id": "release-approval",
                "artifact_version": packet["artifact"]["version"],
                "source_commit": packet["artifact"]["source_commit"],
                "archive_sha256": packet["artifact"]["archive_sha256"],
                "manifest_sha256": packet["artifact"]["manifest_sha256"],
                "observed_at": "2026-09-19T10:00:00Z",
                "result": "pass",
                "architectures": ["governance-record"],
            }
        )
        packet["claims"]["approval"] = "approved"
        packet["claims"]["approval_evidence_ref"] = "approval-record"
        result = validate_packet(packet)
        self.assertEqual(result["approval_claim"], "approved")
        self.assertFalse(result["approval_inferred"])

    def test_unobserved_approval_rejects_reference(self) -> None:
        packet = load()
        packet["claims"]["approval_evidence_ref"] = "public-release-record"
        self.assert_code(packet, "E_APPROVAL_CLAIM")

    def test_duplicate_gate_is_rejected(self) -> None:
        packet = load()
        packet["required_gates"].append(copy.deepcopy(packet["required_gates"][0]))
        self.assert_code(packet, "E_DUPLICATE")

    def test_duplicate_evidence_id_is_rejected(self) -> None:
        packet = load()
        duplicate = copy.deepcopy(packet["evidence"][0])
        duplicate["gate_id"] = "release-approval"
        packet["evidence"].append(duplicate)
        self.assert_code(packet, "E_DUPLICATE")

    def test_duplicate_gate_evidence_is_rejected(self) -> None:
        packet = load()
        duplicate = copy.deepcopy(packet["evidence"][0])
        duplicate["evidence_id"] = "another-record"
        packet["evidence"].append(duplicate)
        self.assert_code(packet, "E_DUPLICATE")

    def test_duplicate_architecture_is_rejected(self) -> None:
        packet = load()
        packet["evidence"][0]["architectures"] = ["public-metadata", "public-metadata"]
        self.assert_code(packet, "E_DUPLICATE")

    def test_pass_requires_architecture_or_evidence_scope(self) -> None:
        packet = load()
        packet["evidence"][0]["architectures"] = []
        self.assert_code(packet, "E_EVIDENCE")

    def test_unknown_gate_reference_is_rejected(self) -> None:
        packet = load()
        packet["evidence"][0]["gate_id"] = "unknown-gate"
        self.assert_code(packet, "E_GATE")

    def test_publication_reference_must_exist(self) -> None:
        packet = load()
        packet["publication_observation"]["evidence_ref"] = "missing-record"
        self.assert_code(packet, "E_REFERENCE")

    def test_prerelease_reference_must_pass(self) -> None:
        packet = load()
        packet["evidence"][0]["result"] = "incomplete"
        packet["evidence"][0]["architectures"] = []
        self.assert_code(packet, "E_PUBLICATION")

    def test_optional_gate_may_lack_evidence(self) -> None:
        result = validate_packet(load())
        self.assertEqual(result["required_gates"], 4)

    def test_at_least_one_gate_must_be_required(self) -> None:
        packet = load()
        for gate in packet["required_gates"]:
            gate["required"] = False
        self.assert_code(packet, "E_REQUIRED_GATE")

    def test_prerelease_reference_must_name_release_metadata(self) -> None:
        packet = load()
        packet["publication_observation"]["evidence_ref"] = "archive-check"
        self.assert_code(packet, "E_PUBLICATION")

    def test_publication_tag_must_match_artifact_release_tag(self) -> None:
        packet = load()
        packet["publication_observation"]["tag"] = "1.4.0b4"
        self.assert_code(packet, "E_TAG")

    def test_evidence_at_exact_age_boundary_passes(self) -> None:
        packet = load()
        packet["evidence"][1]["observed_at"] = "2026-08-21T12:00:00Z"
        result = validate_packet(packet)
        self.assertEqual(result["decision"], READY)

    def test_evidence_past_exact_age_boundary_is_stale(self) -> None:
        packet = load()
        packet["evidence"][1]["observed_at"] = "2026-08-21T11:59:59Z"
        self.assert_code(packet, "E_STALE")

    def test_future_evidence_is_rejected(self) -> None:
        packet = load()
        packet["evidence"][0]["observed_at"] = "2026-09-21T12:00:00Z"
        self.assert_code(packet, "E_TIME_ORDER")

    def test_future_publication_observation_is_rejected(self) -> None:
        packet = load()
        packet["publication_observation"]["observed_at"] = "2026-09-21T12:00:00Z"
        self.assert_code(packet, "E_TIME_ORDER")

    def test_invalid_calendar_time_is_rejected(self) -> None:
        packet = load()
        packet["evaluation_time"] = "2026-02-30T12:00:00Z"
        self.assert_code(packet, "E_TIME")

    def test_boolean_max_age_is_rejected(self) -> None:
        packet = load()
        packet["max_evidence_age_days"] = True
        self.assert_code(packet, "E_RANGE")

    def test_invalid_commit_is_rejected(self) -> None:
        packet = load()
        packet["artifact"]["source_commit"] = "short"
        self.assert_code(packet, "E_DIGEST")

    def test_invalid_digest_is_rejected(self) -> None:
        packet = load()
        packet["artifact"]["archive_sha256"] = "not-a-digest"
        self.assert_code(packet, "E_DIGEST")

    def test_invalid_version_is_rejected(self) -> None:
        packet = load()
        packet["artifact"]["version"] = "latest"
        self.assert_code(packet, "E_VERSION")

    def test_unknown_top_field_is_rejected(self) -> None:
        packet = load()
        packet["extra"] = "value"
        self.assert_code(packet, "E_FIELDS")

    def test_unknown_nested_field_is_rejected(self) -> None:
        packet = load()
        packet["artifact"]["path"] = "artifact"
        self.assert_code(packet, "E_FIELDS")

    def test_absolute_path_is_rejected_without_echo(self) -> None:
        packet = load()
        packet["packet_id"] = "/Users/example/private"
        with self.assertRaises(PacketError) as caught:
            validate_packet(packet)
        self.assertEqual(caught.exception.code, "E_PRIVATE")
        self.assertNotIn("Users", str(caught.exception))

    def test_ip_address_is_rejected(self) -> None:
        packet = load()
        packet["packet_id"] = "host-192.0.2.1"
        self.assert_code(packet, "E_PRIVATE")

    def test_uri_is_rejected(self) -> None:
        packet = load()
        packet["packet_id"] = "https://example.invalid/release"
        self.assert_code(packet, "E_PRIVATE")

    def test_secret_assignment_is_rejected(self) -> None:
        packet = load()
        packet["packet_id"] = "token=example"
        self.assert_code(packet, "E_PRIVATE")

    def test_runtime_source_has_no_execution_or_network_import(self) -> None:
        tree = ast.parse((ROOT / "release_evidence.py").read_text(encoding="utf-8"))
        banned = {"subprocess", "socket", "http", "urllib", "requests", "ssh", "paramiko"}
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        self.assertFalse(imports & banned)

    def test_manifest_hashes_match_listed_files(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        for relative, expected in manifest["files"].items():
            actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, relative)

    def test_cli_rejects_malformed_json_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("{", encoding="utf-8")
            self.assertEqual(main([str(path), "--format", "json"]), 2)


if __name__ == "__main__":
    unittest.main()
