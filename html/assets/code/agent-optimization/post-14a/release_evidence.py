#!/usr/bin/env python3
"""Validate an invented release-evidence packet without external side effects."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


READY = "EVIDENCE PACKET READY FOR REVIEW"
NOT_READY = "EVIDENCE PACKET NOT READY"

TOP_FIELDS = {
    "schema_version",
    "packet_id",
    "evaluation_time",
    "max_evidence_age_days",
    "artifact",
    "publication_observation",
    "required_gates",
    "evidence",
    "claims",
}
ARTIFACT_FIELDS = {
    "name",
    "version",
    "release_tag",
    "source_commit",
    "archive_sha256",
    "manifest_sha256",
}
PUBLICATION_FIELDS = {"state", "tag", "observed_at", "evidence_ref"}
GATE_FIELDS = {"gate_id", "required"}
EVIDENCE_FIELDS = {
    "evidence_id",
    "gate_id",
    "artifact_version",
    "source_commit",
    "archive_sha256",
    "manifest_sha256",
    "observed_at",
    "result",
    "architectures",
}
CLAIM_FIELDS = {"acceptance", "approval", "approval_evidence_ref"}

PUBLICATION_STATES = {"none", "draft", "prerelease", "release"}
EVIDENCE_RESULTS = {"pass", "fail", "incomplete"}
ACCEPTANCE_CLAIMS = {"incomplete", "complete"}
APPROVAL_CLAIMS = {"unobserved", "approved"}
SYMBOL = re.compile(r"^[a-z0-9][a-z0-9._-]{0,79}$")
VERSION = re.compile(r"^[0-9]+(?:\.[0-9]+){1,3}(?:[a-z][0-9]+)?$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
PRIVATE_PATTERNS = (
    re.compile(r"(?:^|\s)/(?:Users|home|private|var|Volumes)/"),
    re.compile(r"(?:^|\s)~/"),
    re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    re.compile(r"\b(?:https?|ssh)://", re.IGNORECASE),
    re.compile(r"\b(?:token|password|secret|api[_-]?key)\s*[:=]", re.IGNORECASE),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)


class PacketError(Exception):
    """Bounded validation failure that never includes rejected input."""

    def __init__(self, code: str, field: str):
        super().__init__(code)
        self.code = code
        self.field = field


def _object(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PacketError("E_TYPE", field)
    return value


def _list(value: Any, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise PacketError("E_TYPE", field)
    return value


def _string(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise PacketError("E_TYPE", field)
    for pattern in PRIVATE_PATTERNS:
        if pattern.search(value):
            raise PacketError("E_PRIVATE", field)
    return value


def _symbol(value: Any, field: str) -> str:
    text = _string(value, field)
    if not SYMBOL.fullmatch(text):
        raise PacketError("E_SYMBOL", field)
    return text


def _closed(obj: dict[str, Any], allowed: set[str], field: str) -> None:
    if set(obj) != allowed:
        raise PacketError("E_FIELDS", field)


def _timestamp(value: Any, field: str) -> datetime:
    text = _string(value, field)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PacketError("E_TIME", field) from exc
    if parsed.tzinfo is None:
        raise PacketError("E_TIME", field)
    return parsed.astimezone(timezone.utc)


def _unique(values: list[str], field: str) -> None:
    if len(values) != len(set(values)):
        raise PacketError("E_DUPLICATE", field)


def validate_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic review summary or raise PacketError."""

    original = copy.deepcopy(packet)
    _closed(packet, TOP_FIELDS, "packet")
    if packet["schema_version"] != 1 or isinstance(packet["schema_version"], bool):
        raise PacketError("E_SCHEMA", "schema_version")

    packet_id = _symbol(packet["packet_id"], "packet_id")
    evaluation_time = _timestamp(packet["evaluation_time"], "evaluation_time")
    max_age = packet["max_evidence_age_days"]
    if isinstance(max_age, bool) or not isinstance(max_age, int) or not 1 <= max_age <= 3650:
        raise PacketError("E_RANGE", "max_evidence_age_days")

    artifact = _object(packet["artifact"], "artifact")
    _closed(artifact, ARTIFACT_FIELDS, "artifact")
    artifact_name = _symbol(artifact["name"], "artifact.name")
    artifact_version = _string(artifact["version"], "artifact.version")
    if not VERSION.fullmatch(artifact_version):
        raise PacketError("E_VERSION", "artifact.version")
    release_tag = _symbol(artifact["release_tag"], "artifact.release_tag")
    source_commit = _string(artifact["source_commit"], "artifact.source_commit")
    archive_sha = _string(artifact["archive_sha256"], "artifact.archive_sha256")
    manifest_sha = _string(artifact["manifest_sha256"], "artifact.manifest_sha256")
    if not HEX40.fullmatch(source_commit):
        raise PacketError("E_DIGEST", "artifact.source_commit")
    if not HEX64.fullmatch(archive_sha) or not HEX64.fullmatch(manifest_sha):
        raise PacketError("E_DIGEST", "artifact")

    publication = _object(packet["publication_observation"], "publication_observation")
    _closed(publication, PUBLICATION_FIELDS, "publication_observation")
    publication_state = _string(publication["state"], "publication_observation.state")
    if publication_state not in PUBLICATION_STATES:
        raise PacketError("E_VALUE", "publication_observation.state")
    publication_tag = _symbol(publication["tag"], "publication_observation.tag")
    if publication_tag != release_tag:
        raise PacketError("E_TAG", "publication_observation.tag")
    publication_time = _timestamp(publication["observed_at"], "publication_observation.observed_at")
    publication_ref = _symbol(publication["evidence_ref"], "publication_observation.evidence_ref")
    if publication_time > evaluation_time:
        raise PacketError("E_TIME_ORDER", "publication_observation.observed_at")

    gates_raw = _list(packet["required_gates"], "required_gates")
    if not gates_raw:
        raise PacketError("E_EMPTY", "required_gates")
    gates: list[tuple[str, bool]] = []
    for index, raw in enumerate(gates_raw):
        gate = _object(raw, f"required_gates[{index}]")
        _closed(gate, GATE_FIELDS, f"required_gates[{index}]")
        gate_id = _symbol(gate["gate_id"], f"required_gates[{index}].gate_id")
        if not isinstance(gate["required"], bool):
            raise PacketError("E_TYPE", f"required_gates[{index}].required")
        gates.append((gate_id, gate["required"]))
    gate_ids = [gate_id for gate_id, _ in gates]
    _unique(gate_ids, "required_gates.gate_id")
    required_gate_ids = {gate_id for gate_id, required in gates if required}
    if not required_gate_ids:
        raise PacketError("E_REQUIRED_GATE", "required_gates")

    evidence_raw = _list(packet["evidence"], "evidence")
    evidence_by_id: dict[str, dict[str, Any]] = {}
    evidence_by_gate: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(evidence_raw):
        item = _object(raw, f"evidence[{index}]")
        _closed(item, EVIDENCE_FIELDS, f"evidence[{index}]")
        evidence_id = _symbol(item["evidence_id"], f"evidence[{index}].evidence_id")
        gate_id = _symbol(item["gate_id"], f"evidence[{index}].gate_id")
        if evidence_id in evidence_by_id or gate_id in evidence_by_gate:
            raise PacketError("E_DUPLICATE", "evidence")
        if gate_id not in set(gate_ids):
            raise PacketError("E_GATE", f"evidence[{index}].gate_id")
        item_version = _string(item["artifact_version"], f"evidence[{index}].artifact_version")
        item_commit = _string(item["source_commit"], f"evidence[{index}].source_commit")
        item_archive = _string(item["archive_sha256"], f"evidence[{index}].archive_sha256")
        item_manifest = _string(item["manifest_sha256"], f"evidence[{index}].manifest_sha256")
        if (item_version, item_commit, item_archive, item_manifest) != (
            artifact_version,
            source_commit,
            archive_sha,
            manifest_sha,
        ):
            raise PacketError("E_IDENTITY", f"evidence[{index}]")
        observed_at = _timestamp(item["observed_at"], f"evidence[{index}].observed_at")
        if observed_at > evaluation_time:
            raise PacketError("E_TIME_ORDER", f"evidence[{index}].observed_at")
        if evaluation_time - observed_at > timedelta(days=max_age):
            raise PacketError("E_STALE", f"evidence[{index}].observed_at")
        result = _string(item["result"], f"evidence[{index}].result")
        if result not in EVIDENCE_RESULTS:
            raise PacketError("E_VALUE", f"evidence[{index}].result")
        architectures_raw = _list(item["architectures"], f"evidence[{index}].architectures")
        architectures = [
            _symbol(value, f"evidence[{index}].architectures") for value in architectures_raw
        ]
        if result == "pass" and not architectures:
            raise PacketError("E_EVIDENCE", f"evidence[{index}].architectures")
        _unique(architectures, f"evidence[{index}].architectures")
        normalized = dict(item)
        normalized["observed_at"] = observed_at
        evidence_by_id[evidence_id] = normalized
        evidence_by_gate[gate_id] = normalized

    if publication_ref not in evidence_by_id:
        raise PacketError("E_REFERENCE", "publication_observation.evidence_ref")
    if publication_state in {"prerelease", "release"}:
        publication_item = evidence_by_id[publication_ref]
        if publication_item["gate_id"] != "release-metadata" or publication_item["result"] != "pass":
            raise PacketError("E_PUBLICATION", "publication_observation.evidence_ref")

    if required_gate_ids - set(evidence_by_gate):
        raise PacketError("E_MISSING_GATE", "evidence")

    claims = _object(packet["claims"], "claims")
    _closed(claims, CLAIM_FIELDS, "claims")
    acceptance = _string(claims["acceptance"], "claims.acceptance")
    approval = _string(claims["approval"], "claims.approval")
    if acceptance not in ACCEPTANCE_CLAIMS or approval not in APPROVAL_CLAIMS:
        raise PacketError("E_VALUE", "claims")
    approval_ref = claims["approval_evidence_ref"]
    if approval_ref is not None:
        approval_ref = _symbol(approval_ref, "claims.approval_evidence_ref")

    required_results = [evidence_by_gate[gate_id]["result"] for gate_id in sorted(required_gate_ids)]
    all_required_pass = all(result == "pass" for result in required_results)
    if acceptance == "complete" and not all_required_pass:
        raise PacketError("E_ACCEPTANCE_CLAIM", "claims.acceptance")
    if approval == "approved":
        if approval_ref is None or approval_ref not in evidence_by_id:
            raise PacketError("E_APPROVAL_CLAIM", "claims.approval")
        approval_item = evidence_by_id[approval_ref]
        if approval_item["gate_id"] != "release-approval" or approval_item["result"] != "pass":
            raise PacketError("E_APPROVAL_CLAIM", "claims.approval")
    elif approval_ref is not None:
        raise PacketError("E_APPROVAL_CLAIM", "claims.approval_evidence_ref")

    if packet != original:
        raise PacketError("E_MUTATION", "packet")

    passed = sum(1 for gate_id in required_gate_ids if evidence_by_gate[gate_id]["result"] == "pass")
    incomplete = sum(
        1 for gate_id in required_gate_ids if evidence_by_gate[gate_id]["result"] == "incomplete"
    )
    failed = sum(1 for gate_id in required_gate_ids if evidence_by_gate[gate_id]["result"] == "fail")
    return {
        "decision": READY,
        "packet_id": packet_id,
        "artifact": artifact_name,
        "artifact_version": artifact_version,
        "publication_observation": publication_state,
        "acceptance_claim": acceptance,
        "approval_claim": approval,
        "required_gates": len(required_gate_ids),
        "passed_gates": passed,
        "incomplete_gates": incomplete,
        "failed_gates": failed,
        "release_ready_inferred": False,
        "approval_inferred": False,
        "next_gate": "human review of the identity-bound evidence packet",
    }


def render_text(summary: dict[str, Any]) -> str:
    lines = [
        summary["decision"],
        f"Packet: {summary['packet_id']}",
        f"Artifact: {summary['artifact']} {summary['artifact_version']}",
        f"Publication observation: {summary['publication_observation']} (supplied evidence)",
        f"Acceptance claim: {summary['acceptance_claim']}",
        f"Approval claim: {summary['approval_claim']}",
        f"Required gates: {summary['required_gates']}",
        f"Passed gates: {summary['passed_gates']}",
        f"Incomplete gates: {summary['incomplete_gates']}",
        f"Failed gates: {summary['failed_gates']}",
        "Release readiness inferred: no",
        "Approval inferred: no",
        f"Next gate: {summary['next_gate']}.",
    ]
    return "\n".join(lines)


def rejection(error: PacketError) -> dict[str, str]:
    return {"decision": NOT_READY, "error": error.code, "field": error.field}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        raw = json.loads(args.packet.read_text(encoding="utf-8"))
        packet = _object(raw, "packet")
        result = validate_packet(packet)
    except (OSError, json.JSONDecodeError):
        result = {"decision": NOT_READY, "error": "E_INPUT", "field": "packet"}
        status = 2
    except PacketError as error:
        result = rejection(error)
        status = 1
    else:
        status = 0
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    elif status == 0:
        print(render_text(result))
    else:
        print(f"{result['decision']}\nError: {result['error']}\nField: {result['field']}")
    return status


if __name__ == "__main__":
    sys.exit(main())
