---
short_link_basis: "/_posts/2026-08-31-hands-on-build-and-test-a-passive-proxy-lab.md"
short_url: "https://unixwzrd.ai/s/8e69f0aff9/"
layout: post
title: "Hands-On: Build and Test a Passive Proxy Lab"
date: 2026-08-29 10:00:00 -0500
categories: [hands-on]
tags: [ai, agent-operations, ai-agents, python, model-proxy, observability, testing, local-first, privacy]
image: /assets/images/blog/agent-optimization/post-06-passive-model-proxy-hero.png
excerpt: "Run a passive proxy, deterministic fake model endpoint, and six privacy and byte-preservation canaries using only the Python standard library."
series: "Local First AI and Agent Operations"
series_part: "6A"
series_order: 65
series_total: 14
series_url: /blog/series/local-first-ai-and-agent-operations/
series_companion_of: 6
series_previous_title: "A Passive Model Proxy as an AI Debugging Instrument"
series_previous_url: /technology/2026/08/29/a-passive-model-proxy-as-an-ai-debugging-instrument/
series_next_title: "Multimodal Context Hygiene with a Jinja Chat Template"
redirect_from:
  - /hands-on/2026/08/31/hands-on-build-and-test-a-passive-proxy-lab/
published: true
---

The main Part 6 article explains why I use a passive model proxy as a debugging instrument. This companion gives you a small version you can run, break, and inspect without pointing it at a real model or putting private prompt content into the retained metrics.

The lab has three pieces:

- `passive_proxy_lab.py` forwards HTTP request and response bodies and writes content-free JSONL metrics.
- `fake_model_upstream.py` behaves like a tiny deterministic chat-completion endpoint.
- `test_passive_proxy_lab.py` proves the important claims with six canary tests.

All three use the Python standard library. There is no package installation step.

<!--more-->

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-06a-passive-proxy-lab.svg"
   alt="A three-terminal passive proxy lab with a deterministic fake model endpoint, an unchanged transport path, content-free JSONL metrics, and six regression canaries."
   variant="series" %}

## What This Lab Proves

The tests do not try to prove that this is a production model gateway. They prove a smaller set of properties that are easy to understand and hard to fake accidentally.

| Property | Canary |
| --- | --- |
| The request body is passive | The fake upstream must receive exactly the bytes submitted to the proxy |
| The response body is passive | The caller must receive exactly the body bytes produced by the fake upstream |
| Routine metrics are content-free | Prompt, authorization, private query, and private path-segment markers must be absent from JSONL |
| Existing evidence is restricted | A pre-created `0644` metric file must become `0600` before the append |
| Failure is bounded | An unavailable upstream returns 502 and records an exception class, not its potentially sensitive message |
| Upstream selection is deliberate | A non-loopback upstream requires explicit opt-in, and an upstream URL containing user information is rejected |

The proxy still forwards the `Authorization` header because a real upstream may require it. It never writes headers to the metrics file. That distinction is worth testing: a value can be required for transport and still be forbidden from retained operational evidence.

## Get the Companion Files

The complete files are available through the site's source viewer. You can inspect them in place before downloading anything.

{% include source_code.html source="/assets/code/agent-optimization/post-06/passive_proxy_lab.py" language="python" title="passive_proxy_lab.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-06/fake_model_upstream.py" language="python" title="fake_model_upstream.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-06/test_passive_proxy_lab.py" language="python" title="test_passive_proxy_lab.py" %}

Create a disposable working directory and download the three files:

```bash
mkdir -p /tmp/passive-proxy-lab
cd /tmp/passive-proxy-lab

curl -fsSLO https://unixwzrd.ai/assets/code/agent-optimization/post-06/passive_proxy_lab.py
curl -fsSLO https://unixwzrd.ai/assets/code/agent-optimization/post-06/fake_model_upstream.py
curl -fsSLO https://unixwzrd.ai/assets/code/agent-optimization/post-06/test_passive_proxy_lab.py
```

## Run the Regression Tests First

I prefer to begin with the executable contract before starting any servers manually:

```bash
python3 -m unittest -v test_passive_proxy_lab.py
```

The expected result is six passing tests. The suite creates temporary loopback listeners with operating-system-assigned ports, sends invented content through the proxy, checks the captured bytes, checks the returned body bytes, reads the metric record, and then removes the temporary evidence.

The privacy test deliberately sends four markers through different surfaces:

```text
private prompt text must not enter metrics
Bearer lab-secret
trace=private
private-path-marker
```

The body and header must reach the fake upstream, and the query and private path segment must remain part of the upstream request target. None may appear in the metrics file. The lab maps only a small fixed set of known endpoints to bounded values such as `chat_completions`, `responses`, `models`, and `health`; every other target becomes `other`. It never retains the arbitrary request path.

This is a useful pattern beyond this lab. If a log format is supposed to exclude content, do not verify that by reading a pleasant example. Inject markers into every sensitive surface and fail the test if any marker survives.

## Start the Fake Model Endpoint

Open one terminal in the companion directory and run:

```bash
python3 fake_model_upstream.py
```

It listens on loopback and accepts POST requests. It reads the body so the HTTP exchange completes correctly, but it does not print or retain that body. Every request receives the same invented OpenAI-compatible JSON response.

The zero token counts in that response are deliberate. This fake endpoint does not tokenize anything, so claiming a synthetic token count would make the example look more realistic at the expense of being truthful.

## Start the Passive Proxy

In a second terminal, still in the companion directory, run:

```bash
python3 passive_proxy_lab.py \
  --upstream http://127.0.0.1:18081 \
  --metrics ./passive-proxy-metrics.jsonl
```

The proxy listens on a separate loopback port and forwards to the fake endpoint. Both listener and upstream default to local-only behavior. Before every append, the metrics writer verifies that the destination is a regular file and enforces mode `0600`, including when a permissive file already exists. A symbolic-link target is rejected where the platform provides the standard no-follow open flag.

The proxy accepts GET, POST, PUT, PATCH, DELETE, and OPTIONS for experimentation. It filters a fixed set of common hop-by-hop headers, sets the upstream Host and Content-Length values, and otherwise leaves end-to-end headers available to the upstream. It does not parse additional header names nominated by an incoming `Connection` header, which is one reason this remains a teaching artifact. Request and response bodies are handled as bytes. They are not decoded, normalized, reformatted, or rendered.

The upstream URL must include an explicit host and port and may not contain user information, a query, or a fragment. Remote hosts also require `--allow-remote-upstream`. Rejecting user information prevents a startup status line from reproducing embedded credentials.

## Send an Invented Chat Request

Use a third terminal to send a request through the proxy:

```bash
curl --silent --show-error \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer invented-lab-token' \
  --data '{"messages":[{"role":"user","content":"Explain why passive observation matters."}]}' \
  'http://127.0.0.1:18080/v1/chat/completions?session=invented'
```

You should receive the deterministic response from the fake endpoint. The proxy did not generate that response and did not parse it before returning it.

Now inspect the operational record:

```bash
tail -n 1 passive-proxy-metrics.jsonl | python3 -m json.tool
```

The exact timestamp, request ID, byte counts, and duration will differ. The shape should resemble this sanitized example:

```json
{
    "duration_ms": 1.234,
    "error_class": null,
    "method": "POST",
    "request_bytes": 88,
    "request_id": "generated-lab-identifier",
    "response_bytes": 251,
    "route_class": "chat_completions",
    "status": 200,
    "ts": "generated UTC timestamp"
}
```

Notice what is missing. There is no arbitrary request path, and there are no headers, token values, query parameters, request bodies, prompt fragments, replies, or client addresses. The route class and byte counts are useful for trend monitoring, but they cannot reconstruct the content.

You can check the canaries directly:

```bash
if grep -Eq 'invented-lab-token|session=invented|passive observation matters' passive-proxy-metrics.jsonl; then
  echo 'privacy canary failed'
else
  echo 'privacy canaries absent from metrics'
fi
```

## Force an Upstream Failure

Stop the fake endpoint with Control-C, leave the proxy running, and send the request again. The proxy should return a short 502 response containing a generated request ID. Its metric record will have status `502` and an `error_class`, but it will not record the exception message or upstream address.

This is not enough error reporting for a production operator. It is the right amount for this lab because it demonstrates the boundary: routine metrics can identify the class and correlation point while detailed incident evidence remains a separate, more sensitive channel.

Restart the fake endpoint and the next request should succeed. That gives you a quick way to watch the status transition without changing the proxy configuration.

## Try Three Useful Experiments

First, change whitespace inside the JSON body and rerun the byte-preservation test. A proxy that parses and reserializes JSON may preserve meaning while changing bytes. This lab's contract is stricter, so the upstream capture must match the original body exactly.

Second, add more canaries. Put an invented secret in a header, a query parameter, a variable path segment, and a nested message. Then extend the test assertion before changing the proxy. This turns the privacy rule into a regression boundary rather than a comment future code can ignore.

Third, add a `Content-Encoding` or unusual content type and observe that the proxy does not need to understand the payload to forward its bytes. Be careful not to mistake this for complete HTTP compliance. The lab buffers complete bodies and does not implement chunked request streaming.

## What I Would Add Before Real Use

I would not place this teaching proxy on a shared network. A production component needs streaming request and response handling, bounded body sizes, TLS policy, authentication, concurrency limits, timeouts suited to model workloads, structured diagnostic retention, rotation, health checks, service supervision, and careful handling of disconnects and partial responses.

It also needs separate evidence modes. Content-free operational metrics can have one access and retention policy. Raw requests, rendered prompts, model reasoning, tool calls, and responses need a much stricter policy. Combining both into one convenient log makes it too easy for a routine monitoring tool to become a private-conversation archive.

The production LLM-Ops-Kit proxy covers substantially more of that operational surface, including streaming diagnostics, rendered prompt inspection, correlation, cancellation classification, wrapper-managed operations, and timed numbered diagnostic-log rotation. That rotation renames the active file and changes its inode, so monitoring readers must reopen the active filename. This lab is here so readers can understand and test the core invariant without copying private configuration or deploying a full stack.

## Current State

The proxy lab, fake upstream, and six regression tests pass with the system Python 3 interpreter in the private publication workspace. The tests verify exact request and response body preservation, bounded route classification, prompt, header, query, and path-segment marker exclusion, `0600` enforcement for new and pre-existing metric files, sanitized upstream failure, credential-bearing upstream rejection, and explicit remote-upstream opt-in.

The package is presented as a teaching artifact and is not represented as production-ready. It passed the documented technical checks before appearing here.

## Next Work

A useful follow-up exercise would add streaming SSE fixtures while preserving the same content canaries and exact transport assertions. That belongs in a later revision only after the buffered teaching boundary remains clear.

For now, the important result is already executable: the proxy can observe sizes, timing, status, and failure class while leaving the request and response bodies alone and keeping their contents out of its routine metric record.

That is the habit I want readers to take away from the exercise. Write the boundary down, put canaries on both sides of it, and make the test fail before a future convenience quietly turns observation into mutation or routine metrics into a content archive.
