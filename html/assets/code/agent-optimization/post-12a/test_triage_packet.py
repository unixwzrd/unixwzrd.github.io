from __future__ import annotations

import ast
import contextlib
import copy
import hashlib
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from triage_packet import PacketError, build_packet, load, main, render_json, render_markdown  # noqa: E402

AS_OF = "2030-01-02T03:09:05Z"


def audit_read_only_source(source: str) -> None:
    tree = ast.parse(source)
    forbidden_roots = {"subprocess", "socket", "requests", "urllib", "http", "paramiko", "llmops_kit"}
    forbidden_names = {"eval", "exec", "compile", "__import__"}
    filesystem_mutations = {"write_text", "write_bytes", "mkdir", "unlink", "rename", "replace", "touch", "rmdir", "symlink_to", "hardlink_to"}
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for item in node.names:
                aliases[item.asname or item.name.split(".")[0]] = item.name
                if item.name.split(".")[0] in forbidden_roots:
                    raise AssertionError("forbidden import")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.split(".")[0] in forbidden_roots or module == "os" and any(item.name in {"system", "popen"} for item in node.names):
                raise AssertionError("forbidden direct import")
            for item in node.names:
                aliases[item.asname or item.name] = f"{module}.{item.name}".strip(".")
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            name = node.func.id
            path = aliases.get(name, name)
            if name in forbidden_names or path.split(".")[0] in forbidden_roots or path in {"os.system", "os.popen"}:
                raise AssertionError("forbidden call")
        elif isinstance(node.func, ast.Attribute):
            path_receiver = isinstance(node.func.value, ast.Name) and aliases.get(node.func.value.id, node.func.value.id) == "pathlib.Path"
            path_receiver = path_receiver or isinstance(node.func.value, ast.Call) and isinstance(node.func.value.func, ast.Name) and aliases.get(node.func.value.func.id, node.func.value.func.id) == "pathlib.Path"
            if node.func.attr in filesystem_mutations and (node.func.attr != "replace" or path_receiver):
                raise AssertionError("filesystem mutation")
            parts = [node.func.attr]
            value = node.func.value
            while isinstance(value, ast.Attribute):
                parts.append(value.attr)
                value = value.value
            if isinstance(value, ast.Name):
                parts.append(aliases.get(value.id, value.id))
            path = ".".join(reversed(parts))
            if path.split(".")[0] in forbidden_roots or path in {"os.system", "os.popen"}:
                raise AssertionError("forbidden call")


class TriagePacketTests(unittest.TestCase):
    def fixture(self, name: str = "complete.json"):
        return load(ROOT / "fixtures" / name)

    def rejected(self, envelope, code: str):
        with self.assertRaises(PacketError) as caught:
            build_packet(envelope, as_of=AS_OF)
        self.assertEqual(caught.exception.code, code)

    def invoke_cli(self, envelope):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text(json.dumps(envelope))
            output = io.StringIO()
            with mock.patch.object(sys, "argv", ["triage_packet.py", str(path), "--as-of", AS_OF]), contextlib.redirect_stdout(output):
                status = main()
        return status, output.getvalue()

    def test_complete_is_ready(self):
        self.assertEqual(build_packet(self.fixture(), as_of=AS_OF).decision, "ready_for_review")

    def test_golden_markdown(self):
        packet = build_packet(self.fixture(), as_of=AS_OF)
        self.assertEqual(render_markdown(packet), (ROOT / "fixtures" / "expected-complete.md").read_text())

    def test_rendering_is_deterministic(self):
        packet = build_packet(self.fixture(), as_of=AS_OF)
        self.assertEqual(render_json(packet), render_json(packet))

    def test_json_and_markdown_agree(self):
        packet = build_packet(self.fixture(), as_of=AS_OF)
        structured = json.loads(render_json(packet))
        markdown = render_markdown(packet)
        self.assertEqual(structured["decision"], packet.decision)
        self.assertEqual(structured["captured_at"], packet.captured_at)
        self.assertEqual(structured["target"], packet.target)
        self.assertEqual(structured["target_status"], packet.target_status)
        self.assertEqual(structured["cascade_stop_set"], list(packet.cascade_stops))
        self.assertEqual(structured["observed_running_impact"], list(packet.observed_running_impact))
        self.assertEqual(structured["restore_order"], list(packet.restore_order))
        self.assertEqual(structured["evidence_gaps"], list(packet.gaps))
        self.assertEqual(structured["operation_argv"], list(packet.operation_argv))
        self.assertFalse(structured["executed"])
        for value in (packet.captured_at.replace("T", " ").replace("Z", " UTC"), packet.target, *packet.target_status.values(), *packet.cascade_stops, *packet.observed_running_impact, *packet.restore_order, json.dumps(list(packet.operation_argv))):
            self.assertIn(value, markdown)

    def test_target_plan_is_target_only(self):
        envelope = self.fixture()
        envelope["target_plan"].append(copy.deepcopy(envelope["cascade_plan"][0]))
        self.rejected(envelope, "E_PLAN")

    def test_invalid_cascade_order_is_rejected(self):
        envelope = self.fixture()
        envelope["cascade_plan"][0]["action"] = "start"
        self.rejected(envelope, "E_PLAN")

    def test_two_dependent_restore_order_is_exact_reverse(self):
        envelope = self.fixture()
        second_status = copy.deepcopy(envelope["status"][-1])
        second_status["component"] = "demo-stack:dashboard"
        envelope["status"].append(second_status)
        stop = copy.deepcopy(envelope["cascade_plan"][0])
        stop["component"] = "demo-stack:dashboard"
        start = copy.deepcopy(stop)
        start["action"] = "start"
        envelope["cascade_plan"] = [stop, envelope["cascade_plan"][0], envelope["cascade_plan"][1], envelope["cascade_plan"][2], start]
        packet = build_packet(envelope, as_of=AS_OF)
        self.assertEqual(packet.restore_order, tuple(reversed(packet.cascade_stops)))
        envelope["cascade_plan"][-2:] = list(reversed(envelope["cascade_plan"][-2:]))
        self.rejected(envelope, "E_PLAN")

    def test_impact_comes_from_cascade_membership(self):
        packet = build_packet(self.fixture(), as_of=AS_OF)
        self.assertEqual(packet.observed_running_impact, ("demo-stack:agent",))
        self.assertNotIn("demo-stack:model", packet.observed_running_impact)

    def test_unobserved_is_incomplete_and_suppresses_operation(self):
        packet = build_packet(self.fixture("unobserved.json"), as_of=AS_OF)
        self.assertEqual(packet.decision, "evidence_incomplete")
        self.assertEqual(packet.operation_argv, ())

    def test_missing_affected_status_is_incomplete(self):
        envelope = self.fixture()
        envelope["status"] = [row for row in envelope["status"] if row["component"] != "demo-stack:agent"]
        self.assertEqual(build_packet(envelope, as_of=AS_OF).decision, "evidence_incomplete")

    def test_stale_is_not_ready(self):
        packet = build_packet(self.fixture("stale.json"), as_of=AS_OF)
        self.assertEqual(packet.decision, "evidence_stale")
        self.assertEqual(packet.operation_argv, ())

    def test_mismatched_identity_is_rejected(self):
        envelope = self.fixture()
        envelope["status"][0]["config_hash"] = "c" * 64
        self.rejected(envelope, "E_IDENTITY")

    def test_plan_host_driver_and_target_identities_are_correlated(self):
        for section, index, field in (("cascade_plan", 0, "host"), ("cascade_plan", 0, "driver"), ("target_plan", 0, "host")):
            envelope = self.fixture()
            envelope[section][index][field] = "other-node" if field == "host" else "launchd"
            self.rejected(envelope, "E_PLAN")
        envelope = self.fixture()
        envelope["cascade_plan"][1]["host"] = "other-node"
        self.rejected(envelope, "E_PLAN")

    def test_unknown_field_is_rejected(self):
        envelope = self.fixture()
        envelope["request"]["extra"] = "value"
        self.rejected(envelope, "E_SCHEMA")

    def test_missing_field_is_rejected(self):
        envelope = self.fixture()
        del envelope["capture"]["catalog_hash"]
        self.rejected(envelope, "E_SCHEMA")

    def test_duplicate_observation_is_rejected(self):
        envelope = self.fixture()
        envelope["status"].append(copy.deepcopy(envelope["status"][0]))
        self.rejected(envelope, "E_STATUS")

    def test_duplicate_operation_is_rejected(self):
        envelope = self.fixture()
        envelope["cascade_plan"].insert(1, copy.deepcopy(envelope["cascade_plan"][0]))
        self.rejected(envelope, "E_PLAN")

    def test_unsafe_material_is_rejected_without_echo(self):
        for unsafe in ("/private/example", "failure path=/private/example", "https://example.invalid", "failure ftp://private.invalid", "192.0.2.10", "token=example", "secret: example", "Bearer example"):
            envelope = self.fixture()
            envelope["status"][0]["error"] = unsafe
            with self.assertRaises(PacketError) as caught:
                build_packet(envelope, as_of=AS_OF)
            self.assertEqual(caught.exception.code, "E_PRIVACY")
            self.assertNotIn(unsafe, str(caught.exception))

    def test_runtime_enforces_every_published_status_constraint(self):
        for field, value in (("desired_lifecycle", "unknown"), ("condition", "not_valid"), ("component_version", "not_valid"), ("error", "x" * 81)):
            envelope = self.fixture()
            envelope["status"][0][field] = value
            self.rejected(envelope, "E_STATUS")

    def test_malformed_json_types_and_calendar_values_are_bounded_at_cli(self):
        cases = []
        integer_hash = self.fixture()
        integer_hash["capture"]["config_hash"] = int("1" * 64)
        for row in integer_hash["status"]:
            row["config_hash"] = int("1" * 64)
        cases.append((integer_hash, "E_IDENTITY"))
        for field in ("lifecycle", "desired_lifecycle", "health", "observability"):
            envelope = self.fixture()
            envelope["status"][0][field] = ["running"]
            cases.append((envelope, "E_STATUS"))
        plan_action = self.fixture()
        plan_action["target_plan"][0]["action"] = ["restart"]
        cases.append((plan_action, "E_PLAN"))
        invalid_date = self.fixture()
        invalid_date["capture"]["captured_at"] = "2030-02-30T03:04:05Z"
        cases.append((invalid_date, "E_TIME"))
        for envelope, code in cases:
            status, output = self.invoke_cli(envelope)
            self.assertEqual(status, 2)
            self.assertEqual(json.loads(output)["error_code"], code)
            self.assertNotIn("Traceback", output)

    def test_raw_command_is_rejected(self):
        envelope = self.fixture()
        envelope["target_plan"][0]["command"] = "llmops component restart example"
        self.rejected(envelope, "E_PLAN")

    def test_unsupported_version_action_and_boolean_version_are_rejected(self):
        for value, code in ((2, "E_VERSION"), (True, "E_VERSION")):
            envelope = self.fixture()
            envelope["schema_version"] = value
            self.rejected(envelope, code)
        envelope = self.fixture()
        envelope["request"]["action"] = "stop"
        self.rejected(envelope, "E_REQUEST")

    def test_argument_array_is_closed(self):
        packet = build_packet(self.fixture(), as_of=AS_OF)
        self.assertEqual(packet.operation_argv, ("llmops", "component", "restart", "demo-stack:model-proxy", "--cascade"))

    def test_source_has_no_execution_surface(self):
        source = (ROOT / "scripts" / "triage_packet.py").read_text()
        audit_read_only_source(source)

    def test_ast_audit_rejects_direct_alias_and_filesystem_bypasses(self):
        bypasses = (
            "from subprocess import run\nrun([])\n",
            "from os import system as invoke\ninvoke('example')\n",
            "from pathlib import Path\nPath('example').write_text('value')\n",
        )
        for source in bypasses:
            with self.assertRaises(AssertionError):
                audit_read_only_source(source)

    def test_fixture_and_golden_content_has_no_private_identifier(self):
        patterns = [re.compile(r"/Users/|/home/|~/"), re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"), re.compile(r"\b(?:password|token|secret|api[_-]?key)\s*[=:]", re.I)]
        for path in [*sorted((ROOT / "fixtures").glob("*"))]:
            text = path.read_text()
            self.assertFalse(any(pattern.search(text) for pattern in patterns), path.name)

    def test_manifest_capabilities_and_checksums(self):
        manifest = json.loads((ROOT / "manifest.json").read_text())
        self.assertEqual(manifest["capabilities"], ["read_fixture", "validate", "correlate", "render"])
        self.assertIn("lifecycle_mutation", manifest["excluded_capabilities"])
        for relative, expected in manifest["files"].items():
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), expected)


if __name__ == "__main__":
    unittest.main()
