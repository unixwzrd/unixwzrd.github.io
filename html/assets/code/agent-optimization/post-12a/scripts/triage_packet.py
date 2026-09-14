#!/usr/bin/env python3
"""Render a fixture-backed component restart review packet without execution."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
MAX_AGE_SECONDS = 600
REDACTED_COMMAND = "<redacted-by-capture-adapter>"
COMPONENT = re.compile(r"^[a-z][a-z0-9-]{0,31}:[a-z][a-z0-9-]{0,31}$")
SYMBOL = re.compile(r"^[a-z][a-z0-9-]{0,31}$")
HASH = re.compile(r"^[a-f0-9]{64}$")
UTC_TIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
UNSAFE = (
    re.compile(r"(?:^|[\s=:,(])(?:/|~/)"),
    re.compile(r"\b[a-z][a-z0-9+.-]*://", re.I),
    re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    re.compile(r"\b(?:password|token|secret|api[_-]?key)\s*[=:]", re.I),
    re.compile(r"(?:bearer\s+[a-z0-9._-]+|BEGIN [A-Z ]*PRIVATE KEY)", re.I),
)


class PacketError(ValueError):
    """Bounded rejection that never reproduces unsafe input."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


@dataclass(frozen=True)
class Packet:
    decision: str
    captured_at: str
    target: str
    target_status: dict[str, str]
    cascade_stops: tuple[str, ...]
    observed_running_impact: tuple[str, ...]
    restore_order: tuple[str, ...]
    gaps: tuple[str, ...]
    operation_argv: tuple[str, ...]


def reject(code: str, message: str) -> None:
    raise PacketError(code, message)


def exact_keys(value: Any, required: set[str], *, where: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != required:
        reject("E_SCHEMA", f"{where} has missing or unknown fields")
    return value


def reject_unsafe(value: Any) -> None:
    if isinstance(value, dict):
        for item in value.values():
            reject_unsafe(item)
    elif isinstance(value, list):
        for item in value:
            reject_unsafe(item)
    elif isinstance(value, str) and value != REDACTED_COMMAND:
        if any(pattern.search(value) for pattern in UNSAFE):
            reject("E_PRIVACY", "unsafe string rejected")


def parse_time(value: str) -> datetime:
    if not isinstance(value, str) or not UTC_TIME.fullmatch(value):
        reject("E_TIME", "capture time must be RFC 3339 UTC")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        reject("E_TIME", "capture time is not a valid calendar value")


def validate(envelope: Any) -> dict[str, Any]:
    root = exact_keys(envelope, {"schema_version", "capture", "request", "status", "target_plan", "cascade_plan"}, where="envelope")
    if type(root["schema_version"]) is not int or root["schema_version"] != SCHEMA_VERSION:
        reject("E_VERSION", "unsupported evidence schema")
    capture = exact_keys(root["capture"], {"captured_at", "toolkit_version", "config_hash", "catalog_hash"}, where="capture")
    parse_time(capture["captured_at"])
    if not isinstance(capture["toolkit_version"], str) or not SYMBOL.fullmatch(capture["toolkit_version"]):
        reject("E_IDENTITY", "invalid toolkit identity")
    if not isinstance(capture["config_hash"], str) or not isinstance(capture["catalog_hash"], str) or not HASH.fullmatch(capture["config_hash"]) or not HASH.fullmatch(capture["catalog_hash"]):
        reject("E_IDENTITY", "invalid authority identity")
    request = exact_keys(root["request"], {"component", "action", "cascade"}, where="request")
    if not isinstance(request["component"], str) or not COMPONENT.fullmatch(request["component"]) or not isinstance(request["action"], str) or request["action"] != "restart" or request["cascade"] is not True:
        reject("E_REQUEST", "unsupported request")
    if not isinstance(root["status"], list) or not isinstance(root["target_plan"], list) or not isinstance(root["cascade_plan"], list):
        reject("E_SCHEMA", "capture arrays are required")
    reject_unsafe(root)
    return root


def validate_status(rows: list[Any], capture: dict[str, str]) -> dict[str, dict[str, str]]:
    required = {"lifecycle", "desired_lifecycle", "health", "condition", "observability", "component", "host", "execution_user", "driver", "component_version", "toolkit_version", "config_hash", "catalog_hash", "error"}
    allowed_lifecycle = {"running", "stopped", "unknown"}
    allowed_desired = {"running", "stopped"}
    allowed_health = {"healthy", "unhealthy", "unknown", "not-applicable"}
    allowed_observability = {"observed", "unreachable", "unobserved"}
    found: dict[str, dict[str, str]] = {}
    for raw in rows:
        row = exact_keys(raw, required, where="status row")
        string_fields = ("lifecycle", "desired_lifecycle", "health", "condition", "observability", "component", "host", "execution_user", "driver", "component_version", "toolkit_version", "config_hash", "catalog_hash", "error")
        if any(not isinstance(row[field], str) for field in string_fields):
            reject("E_STATUS", "status fields have invalid JSON types")
        component = row["component"]
        if not COMPONENT.fullmatch(component) or component in found:
            reject("E_STATUS", "invalid or duplicate component observation")
        if not SYMBOL.fullmatch(row["host"]) or not SYMBOL.fullmatch(row["execution_user"]) or not SYMBOL.fullmatch(row["driver"]):
            reject("E_STATUS", "invalid symbolic status identity")
        if row["lifecycle"] not in allowed_lifecycle or row["health"] not in allowed_health or row["observability"] not in allowed_observability:
            reject("E_STATUS", "invalid status vocabulary")
        if row["desired_lifecycle"] not in allowed_desired:
            reject("E_STATUS", "invalid desired lifecycle")
        if not SYMBOL.fullmatch(row["condition"]) or not SYMBOL.fullmatch(row["component_version"]):
            reject("E_STATUS", "invalid symbolic status value")
        if not isinstance(row["error"], str) or (row["error"] and not SYMBOL.fullmatch(row["error"])):
            reject("E_STATUS", "invalid sanitized error code")
        if len(row["error"]) > 80:
            reject("E_STATUS", "sanitized error code is too long")
        if any(row[key] != capture[key] for key in ("toolkit_version", "config_hash", "catalog_hash")):
            reject("E_IDENTITY", "status and envelope identities differ")
        found[component] = row
    return found


def validate_plan(rows: list[Any]) -> list[dict[str, str]]:
    required = {"component", "host", "driver", "action", "command"}
    result: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for raw in rows:
        row = exact_keys(raw, required, where="plan row")
        if any(not isinstance(row[field], str) for field in required):
            reject("E_PLAN", "plan fields have invalid JSON types")
        if not COMPONENT.fullmatch(row["component"]) or not SYMBOL.fullmatch(row["host"]) or not SYMBOL.fullmatch(row["driver"]):
            reject("E_PLAN", "invalid symbolic plan identity")
        if row["action"] not in {"stop", "restart", "start"} or row["command"] != REDACTED_COMMAND:
            reject("E_PLAN", "invalid plan operation")
        identity = (row["component"], row["action"])
        if identity in seen:
            reject("E_PLAN", "duplicate plan operation")
        seen.add(identity)
        result.append(row)
    return result


def build_packet(envelope: Any, *, as_of: str) -> Packet:
    root = validate(envelope)
    capture = root["capture"]
    captured_at = parse_time(capture["captured_at"])
    now = parse_time(as_of)
    if now < captured_at:
        reject("E_TIME", "as-of time precedes capture")
    status = validate_status(root["status"], capture)
    target_plan = validate_plan(root["target_plan"])
    cascade = validate_plan(root["cascade_plan"])
    target = root["request"]["component"]
    if [(row["component"], row["action"]) for row in target_plan] != [(target, "restart")]:
        reject("E_PLAN", "target plan must contain one target restart")
    restart_positions = [index for index, row in enumerate(cascade) if row["action"] == "restart"]
    if len(restart_positions) != 1 or cascade[restart_positions[0]]["component"] != target:
        reject("E_PLAN", "cascade must contain one target restart")
    pivot = restart_positions[0]
    if any(row["action"] != "stop" for row in cascade[:pivot]) or any(row["action"] != "start" for row in cascade[pivot + 1:]):
        reject("E_PLAN", "cascade phases are out of order")
    stops = tuple(row["component"] for row in cascade[:pivot])
    restores = tuple(row["component"] for row in cascade[pivot + 1:])
    if restores != tuple(reversed(stops)) or target in stops:
        reject("E_PLAN", "cascade membership is inconsistent")
    target_identity = (target_plan[0]["component"], target_plan[0]["host"], target_plan[0]["driver"])
    cascade_target_identity = (cascade[pivot]["component"], cascade[pivot]["host"], cascade[pivot]["driver"])
    if target_identity != cascade_target_identity:
        reject("E_PLAN", "target plan identities disagree")
    for row in (*target_plan, *cascade):
        observation = status.get(row["component"])
        if observation is not None and (row["host"], row["driver"]) != (observation["host"], observation["driver"]):
            reject("E_PLAN", "plan and status identities disagree")
    gaps: list[str] = []
    for component in (target, *stops):
        row = status.get(component)
        if row is None:
            gaps.append(f"missing observation: {component}")
        elif row["observability"] != "observed" or row["lifecycle"] == "unknown":
            gaps.append(f"incomplete observation: {component}")
    stale = (now - captured_at).total_seconds() > MAX_AGE_SECONDS
    decision = "evidence_stale" if stale else "evidence_incomplete" if gaps else "ready_for_review"
    observed = tuple(component for component in stops if status.get(component, {}).get("lifecycle") == "running" and status.get(component, {}).get("observability") == "observed")
    operation = ("llmops", "component", "restart", target, "--cascade") if decision == "ready_for_review" else ()
    target_row = status.get(target, {})
    return Packet(decision, capture["captured_at"], target, {key: str(target_row.get(key, "unknown")) for key in ("lifecycle", "health", "observability")}, stops, observed, restores, tuple(gaps), operation)


def render_markdown(packet: Packet) -> str:
    label = "READY FOR REVIEW" if packet.decision == "ready_for_review" else "NOT READY"
    lines = ["# Component Restart Review", "", f"Decision: {label}", f"Evidence state: {packet.decision}", f"Evidence captured: {packet.captured_at.replace('T', ' ').replace('Z', ' UTC')}", f"Target: {packet.target}", "Requested scope: cascade restart", "", "## Observed target", "", f"- Lifecycle: {packet.target_status['lifecycle']}", f"- Health: {packet.target_status['health']}", f"- Observability: {packet.target_status['observability']}", "", "## Canonical impact", "", f"- Target-only plan: restart {packet.target}", f"- Cascade stop set: {', '.join(packet.cascade_stops) or 'none'}", f"- Observed running components within cascade impact: {', '.join(packet.observed_running_impact) or 'none'}", f"- Restore order: {', '.join(packet.restore_order) or 'none'}"]
    if packet.gaps:
        lines += ["", "## Evidence gaps", ""] + [f"- {gap}" for gap in packet.gaps]
    if packet.operation_argv:
        lines += ["", "## Equivalent CLI argument array", "", json.dumps(list(packet.operation_argv))]
    lines += ["", "## Approval boundary", "", f"No command was executed. Captured status may have changed since {packet.captured_at.replace('T', ' ').replace('Z', ' UTC')}. Re-plan and re-observe through a separately qualified live adapter before any approved mutation.", ""]
    return "\n".join(lines)


def render_json(packet: Packet) -> str:
    return json.dumps({"decision": packet.decision, "captured_at": packet.captured_at, "target": packet.target, "target_status": packet.target_status, "cascade_stop_set": list(packet.cascade_stops), "observed_running_impact": list(packet.observed_running_impact), "restore_order": list(packet.restore_order), "evidence_gaps": list(packet.gaps), "operation_argv": list(packet.operation_argv), "executed": False}, indent=2, sort_keys=True) + "\n"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()
    try:
        packet = build_packet(load(args.fixture), as_of=args.as_of)
    except (OSError, json.JSONDecodeError, PacketError) as exc:
        if isinstance(exc, PacketError):
            print(json.dumps({"decision": "input_rejected", "error_code": exc.code, "message": exc.message}, sort_keys=True))
        else:
            print(json.dumps({"decision": "input_rejected", "error_code": "E_INPUT", "message": "fixture could not be read"}, sort_keys=True))
        return 2
    print(render_markdown(packet) if args.format == "markdown" else render_json(packet), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
