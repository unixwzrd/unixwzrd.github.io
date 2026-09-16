from __future__ import annotations

import ast
import copy
import hashlib
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import isolation_preflight as preflight


ROOT = Path(__file__).resolve().parent


def fixture(name: str = "ready.json") -> dict:
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


class PreflightTests(unittest.TestCase):
    def test_ready_manifest_is_declaration_ready(self) -> None:
        result = preflight.validate_manifest(fixture())
        self.assertEqual(result["display_decision"], "MANIFEST READY FOR ISOLATED TEST")
        self.assertFalse(result["runtime_observed"])
        self.assertFalse(result["security_certified"])

    def test_ready_result_is_deterministic(self) -> None:
        first = preflight.validate_manifest(fixture())
        second = preflight.validate_manifest(fixture())
        self.assertEqual(first, second)
        self.assertEqual(preflight.render_text(first), preflight.render_text(second))

    def test_shared_root_is_not_ready(self) -> None:
        result = preflight.validate_manifest(fixture("shared-root.json"))
        self.assertIn("shared_owned_root", result["findings"])

    def test_same_host_port_collision_is_not_ready(self) -> None:
        result = preflight.validate_manifest(fixture("shared-port.json"))
        self.assertIn("same_host_port_collision", result["findings"])

    def test_shared_store_rejects_multiple_writers(self) -> None:
        result = preflight.validate_manifest(fixture("shared-vault-writers.json"))
        self.assertIn("shared_store_multiple_writers:test-vault", result["findings"])

    def test_store_rejects_duplicate_writer(self) -> None:
        raw = fixture()
        raw["authoritative_stores"][0]["writers"].append("agent-a")
        with self.assertRaisesRegex(preflight.ManifestError, "E_STORE_WRITER_DUPLICATE"):
            preflight.validate_manifest(raw)

    def test_store_rejects_duplicate_reader(self) -> None:
        raw = fixture()
        raw["authoritative_stores"][0]["readers"].append("agent-a")
        with self.assertRaisesRegex(preflight.ManifestError, "E_STORE_READER_DUPLICATE"):
            preflight.validate_manifest(raw)

    def test_readonly_store_may_have_zero_writers(self) -> None:
        result = preflight.validate_manifest(fixture())
        self.assertNotIn("readonly_store_has_writer:immutable-corpus", result["findings"])

    def test_nonshared_store_with_one_participant_is_ready(self) -> None:
        raw = fixture()
        store = raw["authoritative_stores"][0]
        store["shared"] = False
        store["readers"] = ["agent-a"]
        result = preflight.validate_manifest(raw)
        self.assertEqual(result["decision"], "manifest_ready_for_isolated_test")

    def test_nonshared_store_rejects_multiple_participants(self) -> None:
        raw = fixture()
        raw["authoritative_stores"][0]["shared"] = False
        result = preflight.validate_manifest(raw)
        self.assertIn("nonshared_store_multiple_participants:test-vault", result["findings"])

    def test_shared_store_requires_two_participants(self) -> None:
        raw = fixture()
        store = raw["authoritative_stores"][0]
        store["readers"] = ["agent-a"]
        result = preflight.validate_manifest(raw)
        self.assertIn("shared_store_insufficient_participants:test-vault", result["findings"])

    def test_shared_store_with_two_participants_is_ready(self) -> None:
        result = preflight.validate_manifest(fixture())
        self.assertNotIn("shared_store_insufficient_participants:test-vault", result["findings"])

    def test_writable_store_requires_one_declared_owner(self) -> None:
        raw = fixture()
        raw["authoritative_stores"][0]["owner"] = None
        result = preflight.validate_manifest(raw)
        self.assertIn("store_owner_mismatch:test-vault", result["findings"])

    def test_launchagent_requires_complete_bootstrap_plan(self) -> None:
        raw = fixture()
        raw["agents"][0]["process_manager"]["bootstrap_test_plan"].remove("headless")
        with self.assertRaisesRegex(preflight.ManifestError, "E_BOOTSTRAP_PLAN"):
            preflight.validate_manifest(raw)

    def test_launchagent_rejects_duplicate_bootstrap_check(self) -> None:
        raw = fixture()
        raw["agents"][0]["process_manager"]["bootstrap_test_plan"].append("login")
        with self.assertRaisesRegex(preflight.ManifestError, "E_BOOTSTRAP_DUPLICATE"):
            preflight.validate_manifest(raw)

    def test_standalone_rejects_launchagent_bootstrap_plan(self) -> None:
        raw = fixture()
        raw["agents"][1]["process_manager"]["bootstrap_test_plan"] = ["login"]
        with self.assertRaisesRegex(preflight.ManifestError, "E_BOOTSTRAP_PLAN"):
            preflight.validate_manifest(raw)

    def test_shared_credential_reference_is_not_ready(self) -> None:
        raw = fixture()
        raw["agents"][1]["credential_refs"] = list(raw["agents"][0]["credential_refs"])
        result = preflight.validate_manifest(raw)
        self.assertIn("shared_credential_reference", result["findings"])

    def test_shared_channel_reference_is_not_ready(self) -> None:
        raw = fixture()
        raw["agents"][1]["channel_refs"] = list(raw["agents"][0]["channel_refs"])
        result = preflight.validate_manifest(raw)
        self.assertIn("shared_channel_reference", result["findings"])

    def test_shared_inference_requires_all_clients(self) -> None:
        raw = fixture()
        raw["shared_inference"]["clients"] = ["agent-a", "agent-c"]
        result = preflight.validate_manifest(raw)
        self.assertIn("inference_client_set_incomplete", result["findings"])

    def test_shared_inference_rejects_duplicate_client(self) -> None:
        raw = fixture()
        raw["shared_inference"]["clients"].append("agent-a")
        with self.assertRaisesRegex(preflight.ManifestError, "E_INFERENCE_CLIENT_DUPLICATE"):
            preflight.validate_manifest(raw)

    def test_shared_inference_requires_attribution(self) -> None:
        raw = fixture()
        raw["shared_inference"]["request_identity"] = "shared"
        result = preflight.validate_manifest(raw)
        self.assertIn("inference_attribution_missing", result["findings"])

    def test_shared_inference_requires_distinct_canaries(self) -> None:
        raw = fixture()
        raw["shared_inference"]["failure_test"] = raw["shared_inference"]["contention_test"]
        result = preflight.validate_manifest(raw)
        self.assertIn("inference_canaries_not_distinct", result["findings"])

    def test_teardown_remove_and_preserve_must_not_overlap(self) -> None:
        raw = fixture()
        raw["agents"][0]["teardown"]["preserve"] = ["jobs-a"]
        with self.assertRaisesRegex(preflight.ManifestError, "E_TEARDOWN_CONFLICT"):
            preflight.validate_manifest(raw)

    def test_teardown_rejects_duplicate_remove_item(self) -> None:
        raw = fixture()
        raw["agents"][0]["teardown"]["remove"].append("jobs-a")
        with self.assertRaisesRegex(preflight.ManifestError, "E_TEARDOWN_REMOVE_DUPLICATE"):
            preflight.validate_manifest(raw)

    def test_teardown_rejects_duplicate_preserve_item(self) -> None:
        raw = fixture()
        raw["agents"][0]["teardown"]["preserve"].append("reviewed-notes-a")
        with self.assertRaisesRegex(preflight.ManifestError, "E_TEARDOWN_PRESERVE_DUPLICATE"):
            preflight.validate_manifest(raw)

    def test_unknown_field_is_rejected(self) -> None:
        raw = fixture()
        raw["agents"][0]["unexpected"] = True
        with self.assertRaisesRegex(preflight.ManifestError, "E_AGENT_FIELDS"):
            preflight.validate_manifest(raw)

    def test_boolean_port_is_rejected(self) -> None:
        raw = fixture()
        raw["agents"][0]["listeners"][0]["port"] = True
        with self.assertRaisesRegex(preflight.ManifestError, "E_PORT"):
            preflight.validate_manifest(raw)

    def test_absolute_path_is_rejected_without_echo(self) -> None:
        raw = fixture()
        raw["testbed_id"] = "/private/example"
        with self.assertRaises(preflight.ManifestError) as caught:
            preflight.validate_manifest(raw)
        self.assertNotIn("private", caught.exception.code)

    def test_uri_is_rejected_without_echo(self) -> None:
        raw = fixture()
        raw["shared_inference"]["id"] = "ssh://private.invalid"
        with self.assertRaises(preflight.ManifestError) as caught:
            preflight.validate_manifest(raw)
        self.assertNotIn("invalid", caught.exception.code)

    def test_cli_rejection_is_bounded_json(self) -> None:
        raw = fixture()
        raw["schema_version"] = True
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                status = preflight.main([str(path), "--format", "json"])
        payload = json.loads(output.getvalue())
        self.assertEqual(status, 2)
        self.assertEqual(payload["decision"], "rejected")
        self.assertFalse(payload["runtime_observed"])

    def test_runtime_source_has_no_execution_or_network_import(self) -> None:
        source = (ROOT / "isolation_preflight.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        forbidden = {"subprocess", "socket", "http", "urllib", "requests", "paramiko", "llmops_kit"}
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertFalse(imported & forbidden)

    def test_manifest_hashes_match_listed_files(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        for relative, expected in manifest["files"].items():
            actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, relative)

    def test_validation_does_not_mutate_input(self) -> None:
        raw = fixture()
        before = copy.deepcopy(raw)
        preflight.validate_manifest(raw)
        self.assertEqual(raw, before)


if __name__ == "__main__":
    unittest.main()
