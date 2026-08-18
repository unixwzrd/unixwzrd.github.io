#!/usr/bin/env python
"""Render one sanitized fixture with the packaged Qwen media-history template."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jinja2


ROOT = Path(__file__).resolve().parent
DEFAULT_TEMPLATE = ROOT / "Qwen-3_5-media-history-template.jinja"
FIXTURES = ROOT / "fixtures.json"

EXPANSIONS = {
    "{{PNG_OLD}}": "iVBORw0KGgoPNG_OLD_CANARY" + ("A" * 5000),
    "{{PNG_NEW}}": "iVBORw0KGgoPNG_NEW_CANARY" + ("B" * 5000),
    "{{AUDIO_OLD}}": "data:audio/wav;base64,AUDIO_OLD_CANARY" + ("C" * 5000),
    "{{AUDIO_NEW}}": "data:audio/wav;base64,AUDIO_NEW_CANARY" + ("D" * 5000),
    "{{VIDEO_OLD}}": "data:video/mp4;base64,VIDEO_OLD_CANARY" + ("E" * 5000),
    "{{VIDEO_NEW}}": "data:video/mp4;base64,VIDEO_NEW_CANARY" + ("F" * 5000),
    "{{TRUNCATED_IMAGE}}": (
        "iVBORw0KGgoTRUNCATED_IMAGE_CANARY\n\n"
        "... [OUTPUT TRUNCATED - invented fixture] ...\n\n"
        + ("G" * 5000)
    ),
    "{{INCIDENTAL_SIGNATURE}}": "iVBORw0KGgoINCIDENTAL_SIGNATURE_CANARY" + ("H" * 5000),
}


def expand(value: Any) -> Any:
    if isinstance(value, str):
        for marker, replacement in EXPANSIONS.items():
            value = value.replace(marker, replacement)
        return value
    if isinstance(value, list):
        return [expand(item) for item in value]
    if isinstance(value, dict):
        return {key: expand(item) for key, item in value.items()}
    return value


def raise_exception(message: str) -> None:
    raise jinja2.TemplateError(message)


def load_template(path: Path) -> jinja2.Template:
    environment = jinja2.Environment(
        undefined=jinja2.ChainableUndefined,
        trim_blocks=False,
        lstrip_blocks=False,
        autoescape=False,
    )
    environment.globals["raise_exception"] = raise_exception
    return environment.from_string(path.read_text(encoding="utf-8"))


def render_case(case: dict[str, Any], template_path: Path = DEFAULT_TEMPLATE) -> str:
    payload = expand(case["payload"])
    template = load_template(template_path)
    return template.render(
        messages=payload["messages"],
        tools=payload.get("tools", []),
        add_generation_prompt=payload.get("add_generation_prompt", True),
        enable_thinking=payload.get("enable_thinking", True),
        add_vision_id=payload.get("add_vision_id", False),
        bos_token=payload.get("bos_token", ""),
        eos_token=payload.get("eos_token", ""),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", help="Fixture name from fixtures.json")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    args = parser.parse_args()
    cases = json.loads(FIXTURES.read_text(encoding="utf-8"))
    if args.case not in cases:
        parser.error(f"unknown fixture: {args.case}")
    try:
        print(render_case(cases[args.case], args.template))
    except jinja2.TemplateError as exc:
        print(f"TEMPLATE ERROR: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
