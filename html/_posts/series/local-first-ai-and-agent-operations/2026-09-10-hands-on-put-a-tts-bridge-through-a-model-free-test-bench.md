---
short_link_basis: "/_posts/series/local-first-ai-and-agent-operations/2026-09-10-hands-on-put-a-tts-bridge-through-a-model-free-test-bench.md"
short_url: "https://unixwzrd.ai/s/9153038fbc/"
layout: post
title: "Hands-On: Put a TTS Bridge Through a Model-Free Test Bench"
date: 2026-09-10 08:00:00 -0500
categories: [hands-on]
tags: [ai, agent-optimization, agent-workflows, tts, python, testing, openai-compatible, local-first, privacy]
image: /assets/images/blog/agent-optimization/post-09-voice-cloning-operations-hero.png
excerpt: "Build a model-free TTS test bench with a fake OpenAI-compatible upstream, generated tone audio, neutral aliases, layered health checks, bounded timeouts, redacted operational events, and deterministic cleanup."
series: "Local First AI and Agent Operations"
series_part: "9A"
series_order: 95
series_total: 13
series_url: /blog/series/local-first-ai-and-agent-operations/
series_companion_of: 9
series_previous_title: "Voice Cloning Across Hosts: Making TTS Operational"
series_previous_url: /technology/2026/09/08/voice-cloning-across-hosts-making-tts-operational/
series_next_title: "Squeezing More Inference from Apple Silicon with MLXForge"
published: true
---

The [main Part 9 article]({{ page.series_previous_url | relative_url }}) separates an agent-facing speech API from the engine that actually generates audio. This lab lets you test that boundary without installing a model, borrowing somebody's voice, or pointing a client at a network provider.

I wanted the exercise to prove the operational contract rather than create a toy voice-cloning demo. It generates a short tone WAV, writes an invented matching transcript, starts a fake OpenAI-compatible speech upstream and a small teaching bridge on ephemeral loopback ports, and then checks the happy path and the failures I care about. When it finishes, both servers stop and the temporary reference material is removed.

The tone is not speech and does not represent a person. The aliases `narrator` and `guide` are invented. Nothing in the package measures voice similarity, speaker identity, model quality, GPU behavior, or production latency.

<!--more-->

## What You Will Build and Verify

The package contains a teaching bridge, fake upstream, complete runner, four regression tests, README, and an empty dependency declaration because the lab uses only the Python standard library.

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-09a-model-free-tts-lab.svg"
   alt="The model-free lab generates temporary tone and transcript material, starts a teaching bridge and fake upstream, runs happy-path and failure cases, checks health and operational-event redaction boundaries, and cleans up both servers and temporary files."
   variant="series" %}

The complete run checks these behaviors:

| Check | Required result |
| --- | --- |
| Bridge health | HTTP 200 while the teaching bridge is running |
| Upstream health | HTTP 200 while the fake upstream is running |
| Neutral alias | Case-insensitive `NARRATOR` selects the generated audio and transcript pair |
| Upstream request | The configured pair replaces the alias before the fake upstream sees the payload |
| Format compatibility | An OGG request is explicitly delivered as WAV |
| Returned media | Response bytes match the generated tone exactly |
| Operational log | Contains `<redacted input text>` and none of the three invented synthesis inputs |
| Invalid input | Missing `input` returns HTTP 400 |
| Bounded timeout | A deliberately slow upstream returns HTTP 502 |
| Split health | Bridge health remains HTTP 200 after the upstream stops, while the next speech request returns HTTP 502 |
| Cleanup | Both server threads stop and the temporary reference directory is removed |

## Step 1: Put the Lab in an Isolated Directory

Copy the five companion files into an empty working directory:

```text
README.md
requirements.txt
run_lab.py
test_lab.py
tts_bridge_lab.py
```

The publication package provides the same files as individual source disclosures and as one archive. The archive is the convenient path; the disclosures make the implementation reviewable without forcing a browser download.

Download the [complete five-file Hands-On 9A package]({{ '/assets/code/agent-optimization/post-09a/hands-on-09a-model-free-tts-bridge-lab.zip' | relative_url }}). Every file is also available below through the site's standard collapsed source viewer.

{% include source_code.html source="/assets/code/agent-optimization/post-09a/README.md" language="markdown" title="README.md" %}

{% include source_code.html source="/assets/code/agent-optimization/post-09a/requirements.txt" language="text" title="requirements.txt" %}

{% include source_code.html source="/assets/code/agent-optimization/post-09a/run_lab.py" language="python" title="run_lab.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-09a/test_lab.py" language="python" title="test_lab.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-09a/tts_bridge_lab.py" language="python" title="tts_bridge_lab.py" %}

There is no install step. Confirm that your Python is recent enough and that the dependency file contains no package requirements:

```bash
python --version
sed -n '1,20p' requirements.txt
```

The current drafting environment uses Python 3.12. The code depends only on standard-library modules such as `http.server`, `urllib`, `tempfile`, `wave`, and `unittest`.

## Step 2: Read the Safety Boundary Before Running It

The runner creates everything under a new `TemporaryDirectory`. The generated WAV is a low-amplitude tone lasting a fraction of a second. Its sidecar transcript says only that it is invented. The services bind to `127.0.0.1` on ports selected by the operating system, and the fake upstream returns the same generated bytes it receives from the lab fixture.

The lab does not read your TTS configuration, scan a samples directory, inherit a provider token, or contact a remote service. It also does not use launchd or LLM-Ops-Kit. That keeps the experiment focused on the request and observation boundary.

## Step 3: Run the Complete Acceptance Sequence

Run the bounded report first:

```bash
python run_lab.py
```

The command should exit zero and print one line per acceptance condition. The exact temporary paths and ephemeral ports are deliberately absent from the report. The important portion looks like this:

```text
bridge_health                              200
upstream_health                            200
speech_status                              200
audio_matches_generated_tone               True
requested_format                           ogg
delivered_format                           wav
alias_removed_before_upstream              True
reference_audio_selected                   True
matching_transcript_selected               True
input_redacted_in_events                   True
invalid_input_status                       400
timeout_status                             502
bridge_health_after_upstream_stop          200
request_status_after_upstream_stop         502
temporary_reference_directory_removed      True
servers_stopped                            True
```

This is a deterministic contract report, not a benchmark. It contains status codes, selected-format names, and Boolean comparisons. It does not print the audio bytes, request text, reference paths, or event payloads.

## Step 4: Follow the Alias and Reference Pair

The runner creates one generated tone and one matching text sidecar, then supplies this in-memory mapping:

```python
voice_map = {
    "narrator": {"sample": "narrator.wav"},
    "guide": {"sample": "narrator.wav", "ref_text": "narrator.txt"},
}
```

When the request uses `NARRATOR`, the lookup is case-insensitive. The teaching bridge removes the alias from the upstream payload and replaces it with the resolved `ref_audio` and `ref_text` pair. The fake upstream records the structured payload so the runner can compare both paths with the files it created, but the bounded report emits only `True` or `False`.

The behavior is deliberately similar to the current bridge without pretending that this small fixture is the product. It does not prove ownership or consent. It proves that a reviewed mapping selects two files as one operational pair.

## Step 5: Watch Compatibility Without Hiding It

The speech request asks for OGG. The teaching bridge knows that its fake upstream returns WAV, so it sends `response_format: wav` upstream and returns two headers:

```text
X-TTS-Bridge-Requested-Format: ogg
X-TTS-Bridge-Delivered-Format: wav
```

That is a compatibility decision the caller can observe. The lab then compares the response body with the generated tone byte for byte. A matching result proves that the bridge returned the fake upstream's media unchanged after translating the request. It says nothing about how a real codec, model, or player would behave.

## Step 6: Separate Health from Request Success

The fake upstream first delays its response longer than the bridge's configured `0.05`-second bound. The bridge converts that transport failure into HTTP 502. The short value exists only to keep the lab quick; it is not a production timeout recommendation.

The runner then stops the upstream completely. The bridge continues to answer its own `/health` endpoint with HTTP 200 because its process and listener are still healthy. The next synthesis request returns HTTP 502 because the required upstream is gone.

That result is the central lesson of the lab. A green bridge is not a green model path. An operator needs both observations, plus a real synthesis check when validating the complete service.

## Step 7: Check the Redaction Boundary

Before forwarding, the teaching bridge copies the structured payload and replaces its `input` value with `<redacted input text>` in the operational event. The upstream still receives the invented input because it needs text to fulfill the request. The runner verifies that the event contains the marker and that none of the happy-path, timeout, or unavailable-upstream inputs appears in any operational event.

This is a narrow logging check. It does not prove that every library, reverse proxy, client, crash reporter, or upstream service has the same redaction policy. It proves only the behavior of the packaged teaching bridge.

## Step 8: Run the Regression Tests

Run all four tests with verbose names:

```bash
python -m unittest -v test_lab.py
```

The first test checks alias, paired-path, and format normalization directly. The second proves that an unknown alias remains an upstream voice rather than manufacturing a reference pair. The third injects each invented synthesis input into an operational event and confirms that every leak is rejected. The fourth reruns the complete acceptance sequence, including timeout, upstream loss, redaction, and cleanup.

You can also compile every Python file without running the network fixture:

```bash
python -m py_compile tts_bridge_lab.py run_lab.py test_lab.py
```

## Cleanup and End State

No manual cleanup is required after a successful run. `run_lab.py` stops the fake upstream and bridge in a `finally` block. The temporary directory then removes the generated tone and transcript. The final two report lines verify both conditions.

If you interrupt the process, it still has no authority to modify a production service or configuration. An abandoned temporary directory contains only a generated tone and invented transcript and can be removed through the operating system's normal temporary-file lifecycle.

## What This Lab Cannot Prove

The lab does not load a TTS model, clone a voice, evaluate similarity, measure inference speed, exercise a GPU, test a remote network, validate launchd, or prove automatic recovery. It does not make a reference path portable and does not enforce ownership or consent. It also does not establish that the production bridge is ready for every third-party provider.

Those omissions are intentional. The useful result is a small executable model of the compatibility boundary, including its failure states, without requiring sensitive or expensive material.

## Current State

The five-file companion runs with the Python standard library. Its complete acceptance runner exits zero, all four regression tests pass, and all Python files compile. The generated media and transcript are temporary, synthetic, and removed during cleanup. No model, GPU, credential, remote provider, real voice, or private path is used.

## Next Work

The next technical step belongs in the real product acceptance process: repeat bridge and TTS protocol checks against the final artifact, exercise cold start and outage behavior, and test any provider contract with operator-supplied synthetic fixtures before using authorized voice material.

The proposed restart policy from Part 9 is not part of this lab. It needs its own implementation, desired-state contract, bounded retry tests, explicit-stop test, outage gating, restart counters, and exhausted-budget evidence before a future Hands-On exercise can present it as runnable behavior.
