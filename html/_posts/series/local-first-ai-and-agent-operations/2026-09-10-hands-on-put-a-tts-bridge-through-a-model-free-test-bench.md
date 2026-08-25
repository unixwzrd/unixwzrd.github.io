---
short_link_basis: "/_posts/series/local-first-ai-and-agent-operations/2026-09-10-hands-on-put-a-tts-bridge-through-a-model-free-test-bench.md"
short_url: "https://unixwzrd.ai/s/9153038fbc/"
layout: post
title: "Hands-On: Put a TTS Bridge Through a Model-Free Test Bench"
date: 2026-09-10 08:00:00 -0500
categories: [hands-on]
tags: [ai, agent-operations, ai-agents, tts, python, testing, openai-compatible, local-first, privacy]
image: /assets/images/blog/agent-optimization/post-09-voice-cloning-operations-hero.png
excerpt: "Build a model-free TTS test bench with bounded capability and registry metadata, opaque registered references, a legacy compatibility path, layered health, redacted events, and deterministic cleanup."
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

In the [main Part 9 article]({{ page.series_previous_url | relative_url }}), I separated the speech API an agent sees from the engine that generates audio and owns its references. This lab gives you a safe way to exercise that boundary without installing a model, borrowing somebody's voice, or pointing a client at a network provider.

I built the exercise to prove the operational contract, not to create a toy voice-cloning demo. It generates a short tone WAV and an invented transcript, starts a fake OpenAI-compatible speech engine and a small teaching bridge on ephemeral loopback ports, and walks through both successful requests and the failures I care about. When it finishes, both servers stop and the temporary material disappears with them.

The preferred path uses an opaque registered-reference ID. One synthetic path pair remains so the older compatibility contract is visible and testable. The tone is not speech and does not represent a person. Nothing in the package measures voice similarity, speaker identity, model quality, GPU behavior, or production latency.

Moving from this lab to a real engine means replacing the generated tone with a recording you have the right to use. That can be your own voice, purpose-made synthetic material, or a recording whose speaker gave explicit permission. If the model is transcript-conditioned, you also need to write down exactly what was said and keep that transcript with the recording when you register it. Some supported models use audio alone, so check the contract for the model you chose instead of copying the Qwen requirements blindly. The lab deliberately gives you neither a real voice nor a transcript to reuse.

<!--more-->

## What You Will Build and Verify

The package contains a teaching bridge, a fake upstream, a complete runner, seven regression tests, a README, and an intentionally empty dependency declaration. Everything runs on the Python standard library.

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-09a-model-free-tts-lab.svg"
   alt="The model-free lab generates temporary tone and transcript material, starts a teaching bridge and fake upstream with capability and registry APIs, reuses a bounded metadata cache, checks an opaque registered reference, retains one legacy path-pair case, fails closed after an unavailable-registry refresh and on an unsupported control, tests transport failures, verifies redaction, and cleans up."
   variant="series" %}

| Check | Required result |
| --- | --- |
| Metadata discovery | The bridge caches capability data plus registry reachability and count for a bounded interval |
| Alias source | The bridge exposes its configured aliases and does not retain the registry's reference IDs |
| Preferred alias | Case-insensitive `NARRATOR` becomes one opaque `reference_id` |
| Boundary check | No audio or transcript path crosses the bridge for the registered alias |
| Legacy compatibility | `guide` selects the generated audio and transcript path pair |
| Validation failures | An unavailable registry refresh returns 502 and an unsupported instruction returns 422, both before synthesis |
| Format compatibility | An OGG request is explicitly delivered as WAV |
| Operational events | Input and reference details are replaced with redaction markers |
| Split health | Bridge health remains 200 after the upstream stops, while synthesis returns 502 |
| Cleanup | Both server threads stop and the temporary directory is removed |

## Step 1: Put the Lab in an Isolated Directory

Copy the five companion files into an empty working directory:

```text
README.md
requirements.txt
run_lab.py
test_lab.py
tts_bridge_lab.py
```

Download the [complete five-file Hands-On 9A package]({{ '/assets/code/agent-optimization/post-09a/hands-on-09a-model-free-tts-bridge-lab.zip' | relative_url }}). Every file is also available below through the site's standard collapsed source viewer.

{% include source_code.html source="/assets/code/agent-optimization/post-09a/README.md" language="markdown" title="README.md" %}

{% include source_code.html source="/assets/code/agent-optimization/post-09a/requirements.txt" language="text" title="requirements.txt" %}

{% include source_code.html source="/assets/code/agent-optimization/post-09a/run_lab.py" language="python" title="run_lab.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-09a/test_lab.py" language="python" title="test_lab.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-09a/tts_bridge_lab.py" language="python" title="tts_bridge_lab.py" %}

There is nothing to install. Check that your Python is recent enough and confirm that the dependency file contains no package requirements:

```bash
python3 --version
sed -n '1,20p' requirements.txt
```

The code uses standard-library modules such as `http.server`, `urllib`, `tempfile`, `wave`, and `unittest`.

## Step 2: Read the Safety Boundary

The runner creates everything under a new `TemporaryDirectory`. The generated WAV is a low-amplitude tone lasting a fraction of a second. Its transcript says only that it is invented. Both services bind to `127.0.0.1` on ports selected by the operating system.

The lab does not read your TTS configuration, scan a samples directory, inherit a provider token, or contact a remote service. It also does not use launchd or LLM-Ops-Kit. That keeps the exercise focused on the request and observation boundary.

## Step 3: Run the Complete Acceptance Sequence

Run the bounded report first:

```bash
python3 run_lab.py
```

The command should exit zero. I deliberately keep exact temporary paths, ephemeral ports, the reference ID, and invented inputs out of the 23-condition report. The useful portion looks like this:

```text
bridge_health                              200
upstream_health                            200
speech_status                              200
audio_matches_generated_tone               True
requested_format                           ogg
delivered_format                           wav
registered_alias_uses_opaque_id            True
registered_request_omits_paths             True
metadata_cache_reused                      True
legacy_compatibility_status                200
legacy_pair_selected                       True
registry_unavailable_status                502
registry_failure_precedes_synthesis        True
unsupported_control_status                 422
control_failure_precedes_synthesis         True
input_redacted_in_events                   True
references_redacted_in_events              True
invalid_input_status                       400
timeout_status                             502
bridge_health_after_upstream_stop          200
request_status_after_upstream_stop         502
temporary_reference_directory_removed      True
servers_stopped                            True
```

This is a deterministic contract report, not a benchmark. It contains status codes, selected-format names, and Boolean comparisons. It does not print audio bytes, request text, reference details, temporary paths, or event payloads.

## Step 4: Follow the Preferred Registered Alias

The teaching bridge receives an in-memory alias map with two deliberately different contracts:

```python
voice_map = {
    "narrator": {"reference_id": "ref_lab_narrator"},
    "guide": {"sample": "narrator.wav", "ref_text": "narrator.txt"},
}
```

The first entry is the preferred form. The configured alias supplies the invented identifier. The fake registry returns a record, but the teaching bridge retains only registry reachability and count rather than copying its IDs. When the request uses `NARRATOR`, the bridge removes the alias and forwards only the configured opaque identifier with the target request. The fake engine, like the production engine, remains authoritative for whether that ID is valid.

The runner calls bridge health first, which forces a metadata refresh. The next two synthesis requests reuse the resulting capability and registry metadata instead of performing another discovery round trip. The production cache is bounded to 30 seconds; the lab verifies reuse without sleeping for that interval.

The identifier is visible in the source because it is a synthetic fixture. The product redacts reference content and paths; an opaque ID may remain for operational correlation, but it must stay out of public evidence. I made the lab stricter and redacted the ID from its events too. The string itself is unimportant. What matters is that neither the client nor the bridge needs to know the engine's filesystem layout.

## Step 5: Keep One Legacy Path Pair Honest

The `guide` alias exercises the older compatibility path. It resolves the generated WAV and matching transcript, then forwards both synthetic paths to the fake upstream. That case is intentionally labeled legacy compatibility rather than presented as the normal cross-host design.

I kept this case because existing deployments sometimes need a transition period, and removing the test would make it easy to break an explicitly supported compatibility path by accident. In a real engine, server paths must be allowlisted, and they should never become the default interface between hosts.

## Step 6: Fail Before Synthesis

The runner expires the teaching cache, makes the fake registry return an error, records how many synthesis requests the upstream has received, and calls the bridge again. The failed refresh marks discovery unreachable, the bridge returns 502, and the synthesis count does not change.

It then restores discovery and asks a Qwen-family clone request to use an explicit instruction control. The discovered capability data says that this control is incompatible with reference cloning, so the bridge returns 422 before synthesis. A changed capability revision by itself is not rejected, and the bridge does not validate reference-ID membership locally. Those decisions mirror the current production boundary rather than inventing a stricter bridge contract.

These are not cosmetic checks. They show that an unavailable discovery refresh and a capability-driven control conflict both stop before synthesis, while ID validity remains the engine's job.

## Step 7: Watch Compatibility Without Hiding It

The successful request asks for OGG. The teaching bridge knows that its fake upstream returns WAV, so it sends `response_format: wav` upstream and returns two headers:

```text
X-TTS-Bridge-Requested-Format: ogg
X-TTS-Bridge-Delivered-Format: wav
```

The lab compares the response body with the generated tone byte for byte. That proves that the bridge returned the fake upstream's media unchanged after translating the request. It says nothing about a real codec, model, or player.

## Step 8: Separate Health from Request Success

The fake upstream first delays synthesis longer than the bridge's configured `0.05` second bound. The bridge converts that transport failure into HTTP 502. The short value keeps the lab quick; it is not a production timeout recommendation.

The runner then stops the upstream. The bridge continues to answer its own health endpoint with HTTP 200 because its process and listener are healthy, but that forced health refresh marks discovery unreachable. The next speech request returns HTTP 502 because the required upstream metadata is no longer reachable.

That result is the reason I built the lab. A green bridge does not mean the synthesis path is green. You need separate observations for the bridge, discovery, engine, and a real request.

## Step 9: Check Both Redaction Boundaries

Before forwarding, the teaching bridge copies its structured payload for an operational event. It replaces the target input and any `reference_id`, `ref_audio`, or `ref_text` value with markers. The upstream still receives the invented input and required reference because it needs them to fulfill the request.

The runner verifies that none of its six invented inputs, the synthetic reference ID, or either temporary path appears in any event. This is a narrow logging check. It does not prove that every client, reverse proxy, dependency, or crash reporter has the same policy.

## Step 10: Run the Regression Tests

Run all seven tests with verbose names:

```bash
python3 -m unittest -v test_lab.py
```

The focused tests cover registered-ID forwarding, legacy pair selection, unknown upstream voices, input redaction, reference redaction, response-header line-break removal, and the complete acceptance sequence. You can also compile every Python file without running the servers:

```bash
python3 -m py_compile tts_bridge_lab.py run_lab.py test_lab.py
```

## Step 11: Map the Lab to the Managed Service

The lab deliberately keeps process supervision out of the fixture, but a production investigation cannot stop at a successful request from an interactive shell. In the deployment behind this article, LLM-Ops-Kit manages the bridge as a standalone background component through its dedicated `tts-bridge` adapter. It is not a launchd job. The bridge depends on the TTS engine, runs from the toolkit's immutable Python runtime, and uses `restart_policy=never`, so an intentional stop remains stopped.

Inspect the managed component through the control plane rather than inferring its configuration from a shell environment. Substitute your own qualified component ID:

```bash
llmops component status demo-speech:tts-bridge
llmops config effective component demo-speech:tts-bridge
llmops component logs demo-speech:tts-bridge --list
llmops component logs demo-speech:tts-bridge --channel service --lines 200
```

The effective configuration should make the ownership boundary visible: the bridge belongs on the inference host beside the engine, listens on its client-facing address, and reaches the engine over loopback. The selected configuration revision, component host, execution user, dependency, interpreter, listener, upstream, health target, and log channel should agree. Do not treat an old mutable tree on a non-authority host as current configuration; inspect the authority-selected effective revision.

Then test the protocol in layers. A bridge may legitimately return 404 for an API route it does not implement, so use its actual contract rather than a generic model-server probe:

```text
GET  /health
GET  /v1/audio/voices
POST /v1/audio/speech
```

Run those checks first from an authorized operator context, then repeat the speech request through the real client process. Here, `Dashboard` means the Hermes Agent Dashboard, not a generic web dashboard. That second check matters on macOS because NECP can deny Local Network access to a Dashboard running as a LaunchAgent even when the same URL works under `curl` in a terminal. NECP is the macOS network-policy subsystem involved in enforcing [Local Network privacy](https://developer.apple.com/documentation/technotes/tn3179-understanding-local-network-privacy) decisions. In that failure mode, the client sees `No route to host`, the bridge records no matching request, and macOS unified logs point back to the client process. Other LAN services may still work because they run in different process and privacy contexts.

The repair is not to move the bridge back or weaken its API. Correct the client process's Local Network and applicable network-filter permission, or move that client into a reviewed lifecycle context that has the required access. After changing supervision, recheck the component driver, process owner, logs, health, voice discovery, and one real synthesis request. A stack restart is not acceptance by itself: verify every required component returned to `running/healthy`, and restart a missed client or tunnel explicitly while treating the incomplete stack operation as a control-plane defect to fix.

## Cleanup and End State

You should not have to clean up after a successful run. `run_lab.py` stops the fake upstream and bridge in a `finally` block, then the temporary directory removes the generated tone and transcript. The final two report lines verify both conditions instead of asking you to trust that cleanup happened.

If you interrupt the process, it still has no authority to modify a production service or configuration. An abandoned temporary directory contains only a generated tone and invented transcript and can be removed through the operating system's normal temporary-file lifecycle.

## What This Lab Cannot Prove

The lab does not load a TTS model, clone a voice, evaluate similarity, measure inference speed, exercise a GPU, test a remote network, validate launchd or another process supervisor, or prove automatic recovery. The operational mapping above is a production diagnostic checklist, not evidence produced by the model-free fixture. The lab does not enforce ownership or consent, and it does not establish that a production bridge supports every third-party provider.

I left those things out on purpose. The useful result is a small executable model of the preferred registered-reference boundary, its legacy compatibility path, and its discovery failures, all without requiring sensitive or expensive material.

## Current State

The five-file companion runs with the Python standard library. Its complete 23-condition acceptance runner exits zero, all seven regression tests pass, and all Python files compile. The generated media and transcript are temporary, synthetic, and removed during cleanup. No model, GPU, credential, remote provider, real voice, or private path is used.

## Next Work

The next technical step belongs in product acceptance, not this teaching fixture. That means repeating the bridge and TTS protocol checks against the final artifact from both the operator context and the actual client runtime, exercising cold start and outage behavior, confirming stack operations restore every managed process, performing human listening review separately, and testing rollback with authorized material kept inside the inference service boundary.

The proposed restart policy from Part 9 is not part of this lab. It needs its own implementation, desired-state contract, bounded retry tests, explicit-stop test, discovery gating, restart counters, and exhausted-budget evidence before a future Hands-On exercise can present it as runnable behavior.
