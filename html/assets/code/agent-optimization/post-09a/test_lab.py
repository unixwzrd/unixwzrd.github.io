#!/usr/bin/env python3
"""Regression tests for the model-free TTS Bridge lab."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from run_lab import SYNTHESIS_INPUTS, execute_lab
from tts_bridge_lab import (
    REDACTION_MARKER,
    BridgeConfig,
    build_upstream_payload,
    make_tone_wav,
    operational_events_redact_inputs,
)


class TTSBridgeLabTests(unittest.TestCase):
    def test_alias_selects_audio_and_matching_transcript(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_tone_wav(root / "narrator.wav")
            (root / "narrator.txt").write_text("Invented transcript.\n", encoding="utf-8")
            config = BridgeConfig(
                upstream_base="http://127.0.0.1:1/v1",
                samples_dir=root,
                voice_map={"narrator": {"sample": "narrator.wav"}},
            )
            outgoing, response_format, fallback = build_upstream_payload(
                {"input": "Invented text.", "voice": "NARRATOR", "response_format": "ogg"},
                config,
            )
            self.assertNotIn("voice", outgoing)
            self.assertEqual(outgoing["ref_audio"], str((root / "narrator.wav").resolve()))
            self.assertEqual(outgoing["ref_text"], str((root / "narrator.txt").resolve()))
            self.assertEqual(response_format, "wav")
            self.assertEqual(fallback, "ogg")

    def test_unknown_alias_remains_an_upstream_voice(self) -> None:
        config = BridgeConfig(
            upstream_base="http://127.0.0.1:1/v1",
            samples_dir=Path("/invented/not-used"),
            voice_map={},
        )
        outgoing, _, _ = build_upstream_payload(
            {"input": "Invented text.", "voice": "upstream-default"}, config
        )
        self.assertEqual(outgoing["voice"], "upstream-default")
        self.assertNotIn("ref_audio", outgoing)
        self.assertNotIn("ref_text", outgoing)

    def test_operational_event_redaction_rejects_every_synthesis_input(self) -> None:
        safe_event = f'upstream payload: {{"input": "{REDACTION_MARKER}"}}'
        self.assertTrue(operational_events_redact_inputs([safe_event], SYNTHESIS_INPUTS))
        for leaked_input in SYNTHESIS_INPUTS:
            with self.subTest(leaked_input=leaked_input):
                self.assertFalse(
                    operational_events_redact_inputs(
                        [safe_event, f"leaked input: {leaked_input}"], SYNTHESIS_INPUTS
                    )
                )

    def test_complete_lab_contract(self) -> None:
        report = execute_lab()
        self.assertEqual(report["bridge_health"], 200)
        self.assertEqual(report["upstream_health"], 200)
        self.assertEqual(report["speech_status"], 200)
        self.assertTrue(report["audio_matches_generated_tone"])
        self.assertEqual(report["requested_format"], "ogg")
        self.assertEqual(report["delivered_format"], "wav")
        self.assertTrue(report["alias_removed_before_upstream"])
        self.assertTrue(report["reference_audio_selected"])
        self.assertTrue(report["matching_transcript_selected"])
        self.assertTrue(report["input_redacted_in_events"])
        self.assertEqual(report["invalid_input_status"], 400)
        self.assertEqual(report["timeout_status"], 502)
        self.assertEqual(report["bridge_health_after_upstream_stop"], 200)
        self.assertEqual(report["request_status_after_upstream_stop"], 502)
        self.assertTrue(report["temporary_reference_directory_removed"])
        self.assertTrue(report["servers_stopped"])


if __name__ == "__main__":
    unittest.main()
