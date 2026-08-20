# Hands-On 9A: Model-Free TTS Bridge Lab

This lab demonstrates an OpenAI-compatible TTS compatibility boundary without loading a model or using a real voice. It generates a short tone WAV and an invented matching transcript in a temporary directory, starts a fake speech upstream and a teaching bridge on ephemeral loopback ports, runs the acceptance cases, and removes the temporary material during cleanup.

## Safety and Scope

The generated tone is not speech and does not represent a person. The aliases `narrator` and `guide` are invented. The lab uses no network provider, credential, production path, private sample, model, GPU, or external dependency. It tests request and operational behavior, not voice-cloning quality.

## Run

```bash
python run_lab.py
python -m unittest -v test_lab.py
```

Both commands should exit zero. The runner prints a bounded result table containing status codes and Boolean checks. It never prints input text, audio bytes, temporary paths, or a voice sample.

## What the Lab Proves

The complete run checks that:

- bridge and upstream health are separate;
- a case-insensitive neutral alias selects generated audio and its matching transcript;
- the alias is replaced by the reference pair before the fake upstream sees the request;
- an OGG request is explicitly delivered as WAV;
- the returned bytes match the generated tone;
- the bridge's operational event contains a redaction marker rather than the invented input text;
- invalid input returns 400;
- an upstream timeout returns 502;
- bridge health remains 200 after the upstream has stopped while the next speech request returns 502;
- both servers stop and the temporary reference directory is removed.

## What the Lab Does Not Prove

The lab does not test a TTS model, voice similarity, speaker identity, consent, inference quality, GPU behavior, production latency, remote networking, launchd, or automatic restart. The teaching bridge is deliberately small and is not a drop-in replacement for the current LLM-Ops-Kit bridge.

## Files

| File | Purpose |
| --- | --- |
| `tts_bridge_lab.py` | Fake upstream, teaching bridge, alias resolution, format normalization, generated tone, and managed server helpers |
| `run_lab.py` | Complete acceptance sequence and bounded report |
| `test_lab.py` | Five regression tests, including the full contract, redaction leak rejection, and response-header line-break removal |
| `requirements.txt` | Confirms that the lab uses only the Python standard library |

## Cleanup

The runner stops both loopback servers in a `finally` block. Its `TemporaryDirectory` owns the tone and transcript and removes them after the server cleanup completes. If the process is interrupted, no persistent configuration or production service has been modified; the operating system can remove any abandoned temporary directory through its normal temporary-file lifecycle.
