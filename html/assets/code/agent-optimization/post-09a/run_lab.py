#!/usr/bin/env python3
"""Run the complete model-free TTS Bridge lab."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any
from urllib import error, request

from tts_bridge_lab import (
    BridgeConfig,
    FakeUpstreamState,
    make_bridge,
    make_fake_upstream,
    make_tone_wav,
    operational_events_redact_inputs,
)


SYNTHESIS_INPUTS = (
    "Invented lab sentence.",
    "Invented timeout case.",
    "Invented unavailable-upstream case.",
)


def get_json(url: str) -> tuple[int, dict[str, Any]]:
    try:
        with request.urlopen(url, timeout=2) as response:
            return response.status, json.loads(response.read().decode())
    except error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode())


def post_json(url: str, value: dict[str, Any]) -> tuple[int, bytes, dict[str, str]]:
    req = request.Request(
        url,
        data=json.dumps(value).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=2) as response:
            return response.status, response.read(), dict(response.headers.items())
    except error.HTTPError as exc:
        return exc.code, exc.read(), dict(exc.headers.items())


def execute_lab() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="tts-bridge-lab-") as tmp:
        root = Path(tmp)
        samples = root / "references"
        samples.mkdir()
        tone_path = samples / "narrator.wav"
        transcript_path = samples / "narrator.txt"
        tone_bytes = make_tone_wav(tone_path)
        transcript_path.write_text("This is an invented matching transcript.\n", encoding="utf-8")

        upstream_state = FakeUpstreamState(audio_bytes=tone_bytes)
        upstream = make_fake_upstream(upstream_state)
        config = BridgeConfig(
            upstream_base=f"http://127.0.0.1:{upstream.port}/v1",
            samples_dir=samples,
            voice_map={
                "narrator": {"sample": tone_path.name},
                "guide": {"sample": tone_path.name, "ref_text": transcript_path.name},
            },
            timeout_seconds=0.05,
        )
        bridge = make_bridge(config)
        upstream.start()
        bridge.start()

        bridge_url = f"http://127.0.0.1:{bridge.port}"
        upstream_url = f"http://127.0.0.1:{upstream.port}"
        try:
            bridge_health, _ = get_json(bridge_url + "/health")
            upstream_health, _ = get_json(upstream_url + "/health")
            speech_status, speech_body, headers = post_json(
                bridge_url + "/v1/audio/speech",
                {
                    "input": SYNTHESIS_INPUTS[0],
                    "voice": "NARRATOR",
                    "response_format": "ogg",
                },
            )
            forwarded = upstream_state.received[-1]
            invalid_status, _, _ = post_json(
                bridge_url + "/v1/audio/speech", {"voice": "narrator"}
            )

            upstream_state.delay_seconds = 0.15
            timeout_status, _, _ = post_json(
                bridge_url + "/v1/audio/speech",
                {"input": SYNTHESIS_INPUTS[1], "voice": "guide"},
            )
            upstream_state.delay_seconds = 0.0

            upstream.stop()
            bridge_after_upstream_stop, _ = get_json(bridge_url + "/health")
            unavailable_status, _, _ = post_json(
                bridge_url + "/v1/audio/speech",
                {"input": SYNTHESIS_INPUTS[2], "voice": "guide"},
            )

            report = {
                "bridge_health": bridge_health,
                "upstream_health": upstream_health,
                "speech_status": speech_status,
                "audio_matches_generated_tone": speech_body == tone_bytes,
                "requested_format": headers.get("X-TTS-Bridge-Requested-Format"),
                "delivered_format": headers.get("X-TTS-Bridge-Delivered-Format"),
                "alias_removed_before_upstream": "voice" not in forwarded,
                "reference_audio_selected": forwarded.get("ref_audio") == str(tone_path.resolve()),
                "matching_transcript_selected": forwarded.get("ref_text")
                == str(transcript_path.resolve()),
                "input_redacted_in_events": operational_events_redact_inputs(
                    config.events, SYNTHESIS_INPUTS
                ),
                "invalid_input_status": invalid_status,
                "timeout_status": timeout_status,
                "bridge_health_after_upstream_stop": bridge_after_upstream_stop,
                "request_status_after_upstream_stop": unavailable_status,
            }
        finally:
            if upstream.thread.is_alive():
                upstream.stop()
            bridge.stop()

    report["temporary_reference_directory_removed"] = not root.exists()
    report["servers_stopped"] = not upstream.thread.is_alive() and not bridge.thread.is_alive()
    return report


def main() -> int:
    report = execute_lab()
    print("Model-free TTS Bridge lab")
    print("=" * 58)
    for key, value in report.items():
        print(f"{key:42} {value}")
    required = {
        "bridge_health": 200,
        "upstream_health": 200,
        "speech_status": 200,
        "audio_matches_generated_tone": True,
        "requested_format": "ogg",
        "delivered_format": "wav",
        "alias_removed_before_upstream": True,
        "reference_audio_selected": True,
        "matching_transcript_selected": True,
        "input_redacted_in_events": True,
        "invalid_input_status": 400,
        "timeout_status": 502,
        "bridge_health_after_upstream_stop": 200,
        "request_status_after_upstream_stop": 502,
        "temporary_reference_directory_removed": True,
        "servers_stopped": True,
    }
    return 0 if all(report.get(key) == expected for key, expected in required.items()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
