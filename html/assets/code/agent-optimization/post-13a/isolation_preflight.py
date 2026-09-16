#!/usr/bin/env python3
"""Validate an invented multi-agent isolation manifest without live inspection."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SYMBOL = re.compile(r"^[a-z][a-z0-9-]{0,47}$")
ROOT = re.compile(r"^[a-z][a-z0-9-]{0,31}:[a-z][a-z0-9-]{0,47}$")
FORBIDDEN_TEXT = (
    re.compile(r"(?:^|[\s=:])(?:/|~/)[^\s]*"),
    re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    re.compile(r"\b[a-z][a-z0-9+.-]*://", re.IGNORECASE),
    re.compile(r"\b(?:token|password|secret|api[_-]?key)\s*[:=]", re.IGNORECASE),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
)

TOP_FIELDS = {"schema_version", "testbed_id", "agents", "authoritative_stores", "shared_inference"}
AGENT_FIELDS = {
    "id",
    "host",
    "execution_user",
    "process_manager",
    "roots",
    "credential_refs",
    "channel_refs",
    "listeners",
    "teardown",
}
PROCESS_FIELDS = {"mode", "domain", "bootstrap_test_plan"}
ROOT_FIELDS = {"config", "state", "logs", "cache", "workspace", "memory"}
LISTENER_FIELDS = {"service", "port"}
TEARDOWN_FIELDS = {"remove", "preserve"}
STORE_FIELDS = {"id", "shared", "writable", "owner", "writers", "readers", "transport"}
INFERENCE_FIELDS = {"id", "clients", "request_identity", "contention_test", "failure_test"}
BOOTSTRAP_CHECKS = {"login", "logout", "reboot", "headless"}


class ManifestError(Exception):
    """A bounded structural error which never echoes rejected input."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _object(value: Any, fields: set[str], code: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise ManifestError(code)
    return value


def _array(value: Any, code: str, *, minimum: int = 0) -> list[Any]:
    if not isinstance(value, list) or len(value) < minimum:
        raise ManifestError(code)
    return value


def _symbol(value: Any, code: str) -> str:
    if not isinstance(value, str) or not SYMBOL.fullmatch(value):
        raise ManifestError(code)
    return value


def _root(value: Any, code: str) -> str:
    if not isinstance(value, str) or not ROOT.fullmatch(value):
        raise ManifestError(code)
    return value


def _bool(value: Any, code: str) -> bool:
    if type(value) is not bool:
        raise ManifestError(code)
    return value


def _privacy_scan(value: Any) -> None:
    if isinstance(value, dict):
        for item in value.values():
            _privacy_scan(item)
    elif isinstance(value, list):
        for item in value:
            _privacy_scan(item)
    elif isinstance(value, str) and any(pattern.search(value) for pattern in FORBIDDEN_TEXT):
        raise ManifestError("E_PRIVATE_TEXT")


def _unique(values: list[str]) -> bool:
    return len(values) == len(set(values))


def _require_unique(values: list[str], code: str) -> None:
    if not _unique(values):
        raise ManifestError(code)


def validate_manifest(raw: Any) -> dict[str, Any]:
    manifest = _object(raw, TOP_FIELDS, "E_TOP_LEVEL")
    if manifest["schema_version"] != 1 or type(manifest["schema_version"]) is not int:
        raise ManifestError("E_SCHEMA_VERSION")
    _symbol(manifest["testbed_id"], "E_TESTBED_ID")
    _privacy_scan(manifest)

    agents = _array(manifest["agents"], "E_AGENTS", minimum=2)
    agent_ids: list[str] = []
    users: list[str] = []
    domains: list[str] = []
    roots: list[str] = []
    credential_refs: list[str] = []
    channel_refs: list[str] = []
    listeners: list[tuple[str, int]] = []

    for index, value in enumerate(agents):
        agent = _object(value, AGENT_FIELDS, "E_AGENT_FIELDS")
        agent_id = _symbol(agent["id"], "E_AGENT_ID")
        host = _symbol(agent["host"], "E_HOST")
        user = _symbol(agent["execution_user"], "E_EXECUTION_USER")
        agent_ids.append(agent_id)
        users.append(f"{host}:{user}")

        process = _object(agent["process_manager"], PROCESS_FIELDS, "E_PROCESS_MANAGER")
        mode = process["mode"]
        if mode not in {"launchagent", "standalone"}:
            raise ManifestError("E_PROCESS_MODE")
        domain = _symbol(process["domain"], "E_PROCESS_DOMAIN")
        domains.append(f"{host}:{domain}")
        checks = [_symbol(item, "E_BOOTSTRAP_CHECK") for item in _array(process["bootstrap_test_plan"], "E_BOOTSTRAP_PLAN")]
        _require_unique(checks, "E_BOOTSTRAP_DUPLICATE")
        if mode == "launchagent" and set(checks) != BOOTSTRAP_CHECKS:
            raise ManifestError("E_BOOTSTRAP_PLAN")
        if mode == "standalone" and checks:
            raise ManifestError("E_BOOTSTRAP_PLAN")

        root_map = _object(agent["roots"], ROOT_FIELDS, "E_ROOT_FIELDS")
        agent_roots = [_root(root_map[name], "E_ROOT_VALUE") for name in sorted(ROOT_FIELDS)]
        if not _unique(agent_roots):
            raise ManifestError("E_ROOT_COLLISION_LOCAL")
        roots.extend(agent_roots)

        credentials = [_symbol(item, "E_CREDENTIAL_REF") for item in _array(agent["credential_refs"], "E_CREDENTIAL_REFS", minimum=1)]
        channels = [_symbol(item, "E_CHANNEL_REF") for item in _array(agent["channel_refs"], "E_CHANNEL_REFS", minimum=1)]
        if not _unique(credentials) or not _unique(channels):
            raise ManifestError("E_IDENTITY_REF_DUPLICATE")
        credential_refs.extend(credentials)
        channel_refs.extend(channels)

        for item in _array(agent["listeners"], "E_LISTENERS", minimum=1):
            listener = _object(item, LISTENER_FIELDS, "E_LISTENER_FIELDS")
            _symbol(listener["service"], "E_SERVICE")
            port = listener["port"]
            if type(port) is not int or not 1024 <= port <= 65535:
                raise ManifestError("E_PORT")
            listeners.append((host, port))

        teardown = _object(agent["teardown"], TEARDOWN_FIELDS, "E_TEARDOWN_FIELDS")
        remove = [_symbol(item, "E_TEARDOWN_REMOVE") for item in _array(teardown["remove"], "E_TEARDOWN_REMOVE", minimum=1)]
        preserve = [_symbol(item, "E_TEARDOWN_PRESERVE") for item in _array(teardown["preserve"], "E_TEARDOWN_PRESERVE", minimum=1)]
        _require_unique(remove, "E_TEARDOWN_REMOVE_DUPLICATE")
        _require_unique(preserve, "E_TEARDOWN_PRESERVE_DUPLICATE")
        if set(remove) & set(preserve):
            raise ManifestError("E_TEARDOWN_CONFLICT")

    findings: list[str] = []
    if not _unique(agent_ids):
        findings.append("duplicate_agent_identity")
    if not _unique(users):
        findings.append("shared_execution_user")
    if not _unique(domains):
        findings.append("shared_process_domain")
    if not _unique(roots):
        findings.append("shared_owned_root")
    if not _unique(credential_refs):
        findings.append("shared_credential_reference")
    if not _unique(channel_refs):
        findings.append("shared_channel_reference")
    if not _unique([f"{host}:{port}" for host, port in listeners]):
        findings.append("same_host_port_collision")

    stores = _array(manifest["authoritative_stores"], "E_STORES", minimum=1)
    store_ids: list[str] = []
    known_agents = set(agent_ids)
    for value in stores:
        store = _object(value, STORE_FIELDS, "E_STORE_FIELDS")
        store_id = _symbol(store["id"], "E_STORE_ID")
        store_ids.append(store_id)
        shared = _bool(store["shared"], "E_STORE_SHARED")
        writable = _bool(store["writable"], "E_STORE_WRITABLE")
        owner = store["owner"]
        if owner is not None:
            owner = _symbol(owner, "E_STORE_OWNER")
        writers = [_symbol(item, "E_STORE_WRITER") for item in _array(store["writers"], "E_STORE_WRITERS")]
        readers = [_symbol(item, "E_STORE_READER") for item in _array(store["readers"], "E_STORE_READERS")]
        _require_unique(writers, "E_STORE_WRITER_DUPLICATE")
        _require_unique(readers, "E_STORE_READER_DUPLICATE")
        transport = store["transport"]
        if transport is not None:
            _symbol(transport, "E_STORE_TRANSPORT")
        if not set(writers + readers).issubset(known_agents):
            raise ManifestError("E_STORE_AGENT")
        if writable and (owner not in known_agents or writers != [owner]):
            findings.append(f"store_owner_mismatch:{store_id}")
        if not writable and (owner is not None or writers):
            findings.append(f"readonly_store_has_writer:{store_id}")
        if shared and len(writers) > 1:
            findings.append(f"shared_store_multiple_writers:{store_id}")
        if shared and transport is None:
            findings.append(f"shared_store_transport_missing:{store_id}")
        participants = ({owner} if owner is not None else set()) | set(writers) | set(readers)
        if shared and len(participants) < 2:
            findings.append(f"shared_store_insufficient_participants:{store_id}")
        if not shared and len(participants) > 1:
            findings.append(f"nonshared_store_multiple_participants:{store_id}")
    if not _unique(store_ids):
        findings.append("duplicate_store_identity")

    inference = _object(manifest["shared_inference"], INFERENCE_FIELDS, "E_INFERENCE_FIELDS")
    _symbol(inference["id"], "E_INFERENCE_ID")
    clients = [_symbol(item, "E_INFERENCE_CLIENT") for item in _array(inference["clients"], "E_INFERENCE_CLIENTS", minimum=2)]
    _require_unique(clients, "E_INFERENCE_CLIENT_DUPLICATE")
    if set(clients) != known_agents:
        findings.append("inference_client_set_incomplete")
    if inference["request_identity"] != "per-client":
        findings.append("inference_attribution_missing")
    for name in ("contention_test", "failure_test"):
        if not isinstance(inference[name], str) or not SYMBOL.fullmatch(inference[name]):
            raise ManifestError("E_INFERENCE_TEST")
    if inference["contention_test"] == inference["failure_test"]:
        findings.append("inference_canaries_not_distinct")

    return {
        "schema_version": 1,
        "testbed_id": manifest["testbed_id"],
        "decision": "manifest_ready_for_isolated_test" if not findings else "not_ready",
        "display_decision": "MANIFEST READY FOR ISOLATED TEST" if not findings else "NOT READY",
        "agent_count": len(agents),
        "shared_inference": inference["id"],
        "findings": sorted(findings),
        "runtime_observed": False,
        "security_certified": False,
    }


def render_text(result: dict[str, Any]) -> str:
    lines = [
        result["display_decision"],
        f"Testbed: {result['testbed_id']}",
        f"Declared agents: {result['agent_count']}",
        f"Shared inference dependency: {result['shared_inference']}",
    ]
    if result["findings"]:
        lines.append("Findings:")
        lines.extend(f"- {item}" for item in result["findings"])
    else:
        lines.append("Declaration conflicts: none")
    lines.extend(
        [
            "Runtime observed: no",
            "Security certified: no",
            "Next gate: inspect the declared environment with separately reviewed tools.",
        ]
    )
    return "\n".join(lines) + "\n"


def load_manifest(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ManifestError("E_INPUT") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        result = validate_manifest(load_manifest(args.manifest))
    except ManifestError as exc:
        result = {"decision": "rejected", "error": exc.code, "runtime_observed": False, "security_certified": False}
        print(json.dumps(result, sort_keys=True) if args.format == "json" else f"REJECTED\nError: {exc.code}\n")
        return 2
    print(json.dumps(result, indent=2, sort_keys=True) if args.format == "json" else render_text(result), end="" if args.format == "text" else "\n")
    return 0 if result["decision"] == "manifest_ready_for_isolated_test" else 1


if __name__ == "__main__":
    sys.exit(main())
