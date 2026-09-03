---
short_url: "https://unixwzrd.ai/s/5f74184fe9/"
short_link_basis: "/_posts/2026-09-02-multimodal-context-hygiene-with-a-jinja-chat-template.md"
layout: post
title: "Multimodal Context Hygiene with a Jinja Chat Template"
date: 2026-09-02 10:00:00 -0500
categories: [technology]
tags: [ai, agent-operations, ai-agents, qwen, jinja, multimodal, context-hygiene, model-proxy, hermes, local-first]
image: /assets/images/blog/agent-optimization/post-07-multimodal-context-hygiene-hero.png
excerpt: "Old textual media results can consume context long after they stop helping the model. I moved that cleanup into a tested Qwen chat template while keeping the diagnostic proxy passive."
series: "Local First AI and Agent Operations"
series_part: 7
series_order: 70
series_total: 14
series_url: /blog/series/local-first-ai-and-agent-operations/
series_previous_title: "A Passive Model Proxy as an AI Debugging Instrument"
series_previous_url: /technology/2026/08/29/a-passive-model-proxy-as-an-ai-debugging-instrument/
series_next_title: "From Shell Scripts to an Operator-Ready LLM-Ops-Kit"
series_next_url: /technology/2026/09/06/from-shell-scripts-to-an-operator-ready-llm-ops-kit/
series_next_date: 2026-09-06 10:00:00 -0500
series_companion_title: "Hands-On: Put Multimodal Context Hygiene Through a Test Bench"
series_companion_url: /hands-on/2026/09/02/hands-on-put-multimodal-context-hygiene-through-a-test-bench/
series_companion_date: 2026-09-02 10:00:00 -0500
published: true
---

{% assign hands_on_post = site.posts | where: "url", page.series_companion_url | first %}
{% assign hands_on_link_ready = false %}
{% if hands_on_post %}
  {% assign hands_on_link_ready = true %}
{% endif %}

The first time I noticed an image tool result being carried into a later prompt, the waste was hard to miss. A long textual payload remained in the conversation after the useful work was finished, and then I found another copy inside an assistant tool call that had decoded or saved the same bytes. I was asking the model to drag old media work through turns that no longer needed it.

That sort of history gets expensive quickly. Base64 expands binary data, and the rendered text still occupies context and participates in the model's attention and KV-cache work. I am deliberately not putting a percentage on the effect because it depends on the payload, tokenizer, context size, cache behavior, and runtime. I did not need a benchmark to establish the basic engineering fact that repeating thousands of characters of old encoded media is more work than leaving them out.

My first instinct was to strip the payload in the model proxy. I had just spent the [previous installment]({{ page.series_previous_url | relative_url }}) establishing the proxy as a passive diagnostic instrument, though. The moment it started rewriting requests, I could no longer trust it as evidence of what the client had sent. The filtering had to happen somewhere else, and for the Qwen route I was working with, the selected Jinja chat template was the right boundary.

<!--more-->

## The Template Is Part of the Model Interface

An OpenAI-compatible request is not yet the prompt the model consumes. It is structured input made up of messages, roles, tool definitions, tool calls, and sometimes native image or video parts. The chat template turns all of that into the model's grammar. In this case, that grammar belongs to the Qwen 3.5 family and includes the `<|im_start|>` and `<|im_end|>` turn envelope, Qwen vision placeholders, thinking layout, tool-call serialization, validation rules, and the final assistant generation boundary. Calling it a generic ChatML template would hide most of the compatibility contract I actually care about.

I kept the upstream stock template unchanged and built the media-history policy as a derivative. That gave me a real fallback instead of something I would have to reconstruct from memory, and it gave the tests a useful control: ordinary text and tool history should render identically under both templates. The proxy continues to observe the exchange without changing it, while the selected template performs the intentional transformation when the runtime constructs the prompt. If I want the proxy's diagnostic render to match what llama.cpp constructs, both paths have to reference the same file.

That separation is simple on paper and important in operation.{% if hands_on_link_ready %} The Hands-On companion makes both rendering paths visible in a [small stock-versus-derived test bench]({{ page.series_companion_url | relative_url }}#what-you-will-build-and-verify).{% endif %}

| Boundary | Responsibility |
| --- | --- |
| Agent or application | Sends OpenAI-compatible messages and tool history |
| Passive model proxy | Forwards the request and produces diagnostic views without rewriting it |
| Selected Qwen template | Applies the reviewed media-history policy while rendering the model prompt |
| Model runtime | Consumes the rendered prompt and processes native structured vision data |

## History Is Structured, Even When the Payload Is Text

My first version kept only the latest image-like payload. It proved the idea, but it was too broad in one direction and too narrow in the other. A long string containing an image signature is not automatically an image result, and deleting only the payload can leave a broken conversational exchange behind.

The current template starts with a prepass over the messages. It looks for explicit tool results whose content is a string longer than 4,096 characters and whose structure and markers identify the relevant media type. For images, the content must look like an image result and contain a PNG, JPEG, or image data-URL marker. Audio and video require their corresponding result labels and data-URL markers.

The 4,096-character threshold is only a routing gate. It is not a truncation size, a token estimate, or proof that the content is valid base64. Jinja is not a media parser, and I do not want the template pretending it validated data that it merely recognized by shape and marker. A false positive can be just as damaging as missed cleanup, so one synthetic fixture contains a long ordinary diagnostic result with an incidental PNG signature. It stays in the rendered prompt because the surrounding structure does not identify it as an image result.{% if hands_on_link_ready %} You can exercise the exact greater-than boundary at [4,096 and 4,097 characters in the lab]({{ page.series_companion_url | relative_url }}#step-7-touch-the-4096-character-boundary).{% endif %}

The prepass builds the selection policy before the normal Qwen rendering loop begins:

{% raw %}
```jinja
{%- if message.role == 'tool'
      and message.content is string
      and message.content|length > 4096 %}
    {# Classify explicit textual media results and record retention state. #}
{%- endif %}
```
{% endraw %}

That fragment is intentionally incomplete. I would rather give readers the reviewed file than turn a few selected snippets into a puzzle they have to reconstruct. The complete attributed template, stock fallback, fixtures, expected results, renderer, tests, notice, checksums, and Apache-2.0 license are available together later in this article.

## Images, Audio, and Video Do Not Share One Retention Rule

The current policy removes every textual image tool result, including the newest one. That sounds aggressive until textual history and native structured vision are treated as different things. Textual image results are often enormous, may already be truncated, and cannot reliably reconstruct a usable image for the model. Keeping the newest damaged string does not make it useful. Native structured image parts are different: the model engine handles their data separately while the template emits Qwen's vision placeholder, so those parts remain eligible.

Audio and video follow a different rule in the current policy. Older explicit textual results are removed while the latest explicit result of each type remains. This is a bounded choice based on the shapes exercised in the tested route, not a general claim that the latest media payload is always sufficient for every model or application.

The result is easier to understand as a selection flow than as a pile of string checks:

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-07-media-history-policy.svg"
   alt="Before-and-after media-history selection showing ordinary history retained, textual image exchanges removed as complete pairs, only the latest explicit textual audio and video exchanges retained, and native Qwen vision placeholders preserved."
   variant="series" %}

The important division is not simply old versus new. It is textual tool history versus native structured multimodal input, followed by a media-specific retention rule.

## Remove the Exchange, Not Just the Payload

A tool result does not exist by itself. The assistant requested the tool, the tool returned a result, and later turns may refer back to the exchange. If I remove only the result, the prompt can retain an orphaned assistant call asking for work that apparently never completed. The template therefore removes media-producing assistant calls and their associated tool results as complete exchanges. It also removes assistant calls carrying recognizable media bytes or explicitly decoding base64, along with the following results that belong to those calls. That catches the second copy that started this investigation in the first place: the image appeared as a tool result, then an assistant-side operation copied or decoded the same bytes again.

The ordering logic deserves tests because message history is not always tidy. A truncated result can still contain enough structure to identify the exchange. A malformed system message must still fail with the stock Qwen ordering error. A normal tool exchange must remain untouched. Removing context is only a win when the remaining prompt preserves the model's grammar and the application's meaning.

## What the Fixtures Actually Prove

I built the publication companion around seven invented fixtures instead of trying to sanitize a screenshot from my own environment. Each fixture generates obvious canary strings locally and contains no real prompt, conversation, model response, or media artifact.{% if hands_on_link_ready %} The Hands-On companion lets you [compare all seven fixtures without dumping their long payloads]({{ page.series_companion_url | relative_url }}#step-4-compare-all-seven-fixtures-without-dumping-the-payloads).{% endif %}

| Fixture | Evidence it provides |
| --- | --- |
| Native structured media | One image placeholder and one video placeholder remain while the invented data URL does not render as prompt text |
| Textual image exchanges | Both image results, both producing calls, and the assistant-side decode exchange are absent |
| Latest audio and video | Older explicit exchanges are absent and the latest explicit exchanges remain |
| Truncated image history | The truncation marker, image marker, and producing call are removed together |
| Incidental signature collision | A long ordinary result remains because image-result structure is absent |
| Malformed ordering | Rendering fails with the normal Qwen system-message ordering error |
| Ordinary text and tools | The derived render is byte-identical to the packaged stock render |

The companion tests also verify provenance checksums. The packaged stock fallback is byte-equivalent to the immutable upstream Qwen template after removing its single added trailing newline. The derivative carries a prominent modification notice, and the Apache-2.0 license travels with the package. These are rendering tests: they establish how the supplied template handles the supplied message shapes under the tested Jinja environment, but they do not prove output quality, token savings, latency improvement, or compatibility with an arbitrary model artifact. A generation canary still has to run against the exact model and runtime selected for deployment.

## Get the Complete Template Package

The complete package is available as [one ZIP download](/assets/code/agent-optimization/post-07/post-07-qwen-media-history-companion.zip). It contains the exact nine documented files and excludes interpreter caches and bytecode. The same files are available below through the source viewer, so you can inspect them before downloading anything.

{% include source_code.html source="/assets/code/agent-optimization/post-07/Qwen-3_5-media-history-template.jinja" language="jinja" title="Qwen-3_5-media-history-template.jinja" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07/Qwen-3_5-stock-template.jinja" language="jinja" title="Qwen-3_5-stock-template.jinja" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07/README.md" language="markdown" title="README.md" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07/fixtures.json" language="json" title="fixtures.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07/expected-results.json" language="json" title="expected-results.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07/render_fixture.py" language="python" title="render_fixture.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07/test_media_history_template.py" language="python" title="test_media_history_template.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07/NOTICE.md" language="markdown" title="NOTICE.md" %}

{% include source_code.html source="/assets/code/agent-optimization/post-07/LICENSE-APACHE-2.0.txt" language="text" title="LICENSE-APACHE-2.0.txt" %}

## A Small Change Still Needs a Rollback Path

Replacing a model's bundled chat template may look like a small configuration change, but it is not cosmetic. One missing delimiter, changed tool schema, damaged reasoning boundary, or misplaced generation marker can make a healthy model behave as though the entire serving stack is broken.

My acceptance sequence begins with rendering sanitized fixtures under both templates. Ordinary text and tool history must match the stock baseline, and the media cases must show only the intended differences. I then run bounded generation canaries for ordinary text, tool calling, native structured vision, and the media-history case that motivated the change. Only after those checks would I point the model profile at the derivative and restart the selected component through the normal plan, apply, and status path. If the passive proxy renders diagnostic prompts, it receives the same template selection so its evidence agrees with the runtime.{% if hands_on_link_ready %} The optional lab section shows [how to compare those two diagnostic renders without claiming that render-only mode proves live forwarding]({{ page.series_companion_url | relative_url }}#step-8-see-where-the-passive-model-proxy-fits).{% endif %}

Rollback is simply the stock template kept beside the derivative. Restoring that path and repeating the same canaries is faster and safer than editing the derivative under pressure, which is exactly when I am least likely to make a careful template repair. The companion README records the profile shape, restart sequence, checksums, acceptance gates, and stock rollback procedure.

Hermes continues sending its OpenAI-compatible message and tool history. It does not need a request-rewriting plugin for this policy because the selected matching Qwen runtime applies the policy during prompt rendering. The template has also worked with a matching later Qwen prompt format in my environment, but I treat that as an operational observation rather than a support claim. I would not drop this file into Llama, Mistral, Gemma, an OpenAI model, or an arbitrary ChatML-style runtime. The pruning policy can be ported, but the destination template must preserve that model's own control tokens, multimodal markers, reasoning rules, tool schema, and generation boundary. Similar-looking envelopes are not a compatibility test.

## Current State

The Qwen 3.5-family media-history derivative is implemented and covered by the current LLM-Ops-Kit regression suite. The publication companion adds an attributed derivative, stock fallback, Apache-2.0 license and notice, immutable provenance, checksums, seven synthetic fixtures, explicit expected results, a manual renderer, and self-contained tests. Its three test methods pass under Jinja 3.1.6, and the underlying production suite covers the central structured-media and passive-proxy boundaries.

There is bounded operational evidence for the matching Qwen route used in my environment and a successful Hermes history replay. That does not establish universal model compatibility or a benchmark result. The package is presented as a tested technical companion, not a generic replacement for another model's bundled template.

## Next Work

What remains is narrower and easier to name. I want an explicit final-artifact generation pass against the selected model revision, followed by repeated checks for ordinary tools, native vision, reasoning boundaries, and termination. More general tool-call reduction stays deferred because it can change semantics in ways this media-history cleanup does not.

The next main installment returns to the larger operations story: how the collection of scripts became an operator-ready LLM-Ops-Kit with typed adapters, dependency-aware plans, immutable releases, and rollback that does not depend on remembering which shell command happened to work last time.
