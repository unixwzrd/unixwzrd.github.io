---
short_url: "https://unixwzrd.ai/s/6e4099c398/"
short_link_basis: "/_posts/series/local-first-ai-and-agent-operations/2026-09-16-where-local-inference-performance-actually-comes-from.md"
layout: post
title: "Where Local Inference Performance Actually Comes From"
date: 2026-09-16 10:00:00 -0500
categories: [technology]
tags: [ai, agent-operations, local-first-ai, apple-silicon, mlx, benchmarking]
image: /assets/images/blog/agent-optimization/post-10-apple-silicon-inference-hero.png
excerpt: "Cache size, quantization, draft models, and MTP solve different problems. Part 11 separates the tuning decisions and the evidence each one needs."
series: "Local First AI and Agent Operations"
series_part: 11
series_order: 110
series_total: 14
series_url: /blog/series/local-first-ai-and-agent-operations/
series_previous_title: "Squeezing More Inference from Apple Silicon: llama.cpp Today, MLXForge Later"
series_previous_url: /technology/2026/09/12/squeezing-more-inference-from-apple-silicon-llama-cpp-today-mlxforge-later/
series_next_title: "Packaging Agent Operations as Installable Skills"
series_companion_title: "Hands-On: Tune One llama.cpp Variable at a Time"
series_companion_url: /hands-on/2026/09/16/hands-on-tune-one-llama-cpp-variable-at-a-time/
series_companion_date: 2026-09-16 10:00:00 -0500
published: true
---

This is Part 11 of the fourteen-part Local-First Agent Operations series. In [Part 10](/technology/2026/09/12/squeezing-more-inference-from-apple-silicon-llama-cpp-today-mlxforge-later/), I broke inference latency into phases and put a fail-closed comparison contract around the results. That gave me a much better answer to the question, "Where is the time going?" It did not answer the next question, which was, "What should I touch?"

That second question is where performance work gets interesting, and where it can get expensive in a hurry. A trace may show that prompt processing dominates a request, but shrinking the context can throw away information the agent needs. A smaller quantization may fit comfortably in memory and quietly damage the work I actually care about. A speculative path may produce impressive decode numbers while consuming enough memory to make the rest of the machine miserable.

I eventually stopped treating tuning as a bag of command-line flags. The more useful approach was to ask where a performance decision lives, what must already be true before I can use it, and what evidence would tell me that it helped rather than merely ran.

<!--more-->

*Status updated September 2, 2026: Qwen3.8 is in production use. The earlier Qwen3.6 MTP example remains historical evidence, and no controlled MTP speedup is claimed here.*

## Three Places a Performance Decision Lives

The first distinction I needed was not between fast and slow. It was between changes I could make as an operator, changes that required a compatible model and runtime, and changes that belonged to model design or conversion. Those layers interact, but they are not interchangeable.

{% include blog_diagram.html src="/assets/images/blog/agent-optimization/post-11-performance-layers.svg" alt="Three layers of inference performance decisions: operator and runtime controls, compatible acceleration paths, and architecture conversion or training choices" variant="wide" %}

*The first useful question is not which flag to change, but which layer owns the proposed change.*

| Decision layer                         | Examples                                                                                                                   | What has to be true                                                                                                                    |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Operator and runtime                   | Context, batch shape, parallel slots, thread and device placement, weight choice, KV-cache format and limits, prompt reuse | The engine and artifact already support the setting, and the resulting work remains comparable                                         |
| Compatible acceleration path           | Separate draft model, embedded MTP heads, EAGLE-style drafting, n-gram or lookup speculation                               | The model and runtime expose a compatible path, the path is observably active, and the target still verifies the result                |
| Architecture, conversion, and training | MTP training, Engram conditional memory, model geometry, conversion and quantization recipes                               | The capability exists in the artifact or conversion pipeline and survives load, generation, correctness, and save/reload qualification |

The boundary is not perfectly clean. Choosing a different quantized artifact is an operator action, but producing that artifact belongs to conversion. Enabling MTP may look like a runtime option, but it does nothing useful unless the artifact contains the required heads and the runtime knows how to exercise them. The important part is that my evidence obligation changes when I cross layers.

## Start With the Working Set

Most of the practical tuning decisions I make begin with memory, but even the word memory hides several different things. Model weights are one part of the working set. The KV cache is another. Runtime buffers, draft state, compiled graphs, other loaded models, the operating system, and every other application on the machine still want their share.

Weight quantization reduces the representation used for the model parameters. KV-cache quantization changes the representation of attention state created while processing the current sequence. Those are different objects with different lifetimes and different risks. A weight format that works well for one model geometry does not automatically tell me which KV representation to use, and a smaller KV cache does not make the weights smaller.

Context length matters because the live attention state grows as more tokens are retained. Parallel slots can multiply that pressure. A rotating or bounded cache can stop growth, but it does so by deciding which earlier state no longer remains available to the model. That is a continuity and correctness decision as much as a capacity decision. If an agent forgets the instruction that made its answer safe, I do not get to call the run optimized because it used less memory.

This is why I do not have a universal recommendation for bit width, context, or cache size. I can say that a candidate fits, loads, and runs. I still have to test whether it preserves the output contract and improves the phase that was actually slow.

## A Prompt Cache Is Not the KV Cache

The terminology gets muddy because several useful mechanisms contain the word cache, while the agent system also has durable memory. I keep four concepts separate:

| State                   | Purpose                                                                      | Reuse boundary                                                                                       |
| ----------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Live KV cache           | Attention state for tokens already processed in an active sequence           | The current model execution and its exact sequence state                                             |
| Prompt or prefix cache  | Reusable computed state for an identical eligible prefix                     | Exact model, tokenizer, template, prefix bytes or tokens, adapters, media identity, and cache layout |
| Persisted session state | Saved execution state intended to resume later                               | All prompt-cache identity plus compatible runtime and serialization versions                         |
| Agent memory            | Durable facts, notes, decisions, and provenance selected for later retrieval | Knowledge-governance and authorization policy, not an inference-cache identity                       |

A reusable prefix can save work when many requests begin the same way. It can also restore the wrong state if its identity is too weak. Text tokens alone may not distinguish two multimodal requests. A template revision can change the effective prompt without changing the visible user text. An adapter, tokenizer, model revision, or policy change can make an old cache ineligible even when the beginning of the conversation looks familiar.

That makes prompt reuse an invalidation problem before it becomes a performance feature. The same lesson applies more strongly to persisted sessions. If I cannot explain why restored state belongs to this exact request, a cache miss is the safer result.

Agent memory is a different layer entirely. LLM-Wiki, the Main Vault, and derived retrieval systems retain durable knowledge for later selection. They do not replace the attention state the inference engine needs for the tokens in front of it. Calling both things memory does not make them substitutable.

## Drafting Tokens Without Trusting Them

Speculative decoding is easier to understand when I stop describing it as a shortcut and describe it as proposal followed by verification. A cheaper path proposes several likely tokens. The target model evaluates those proposals together. Accepted tokens advance the sequence, rejected proposals are discarded, and the target remains authoritative.

{% include blog_diagram.html src="/assets/images/blog/agent-optimization/post-11-speculative-verification.svg" alt="A separate draft model, embedded MTP heads, or n-gram lookup proposes tokens which the target model verifies before accepted tokens advance the sequence" variant="wide" %}

<center>*Drafting can come from several places, but proposal is never the same thing as acceptance.*</center>

A conventional speculative setup uses a smaller draft model. That model has its own weights, cache, compute cost, and compatibility requirements. Embedded multi-token prediction, or MTP, can use additional prediction heads retained with the target artifact as a self-drafting path when the runtime supports it. Draftless methods such as n-gram lookup search patterns already present in the token history and do not load another model at all.

These methods share a verification idea, but their costs are different. A draft model may be cheap per token and expensive to keep resident. An n-gram method may be almost free when a workload repeats long sequences and useless when the next text is novel. MTP heads may avoid a separate full draft model while still requiring model-specific runtime support and additional state.

The [active-path checks in Hands-On 11A](/hands-on/2026/09/16/hands-on-tune-one-llama-cpp-variable-at-a-time/#step-5-prove-the-intended-path-was-active) make the distinction between enabled and exercised visible in a small example.

The useful number is not simply how many tokens were proposed. Acceptance has to be weighed against drafting cost, target verification cost, cache management, memory pressure, sampling behavior, and the latency the client actually experiences. An active path can be slower. A disabled path can leave misleading configuration behind. This is why Part 10's run identity and phase measurements still govern the result.

## The Historical MTP Run Taught Me What Counts as Evidence

I have one retained Qwen3.6-family llama.cpp run that gives me a useful, bounded example. The runtime reported that it created an embedded MTP draft context against the target model itself. Later timing records contained nonzero accepted draft-token counts, and no separate draft artifact had been supplied.

That is much stronger evidence than a filename containing `MTP`, or a configuration field that says the feature should be enabled. It shows that the runtime selected the self-drafting path and that at least some proposed tokens were accepted. It still does not tell me that the path improved performance because that run was not a controlled MTP-off versus MTP-on comparison.

I now use Qwen3.8 in production. The earlier review caught a disagreement between the intended model selection and retained runtime settings, but that snapshot is not a description of what I am running today. The lesson still matters: I need to record what actually ran. Production use establishes that the model is doing useful work; it does not, by itself, establish which speculative path is active or how much that path helps.

This is the sort of bookkeeping that can feel annoyingly administrative when I want to test a model. It is also what prevents me from publishing a beautiful result for a process I did not actually run.

## MTP and Engram Are Not Two More Cache Flags

The MTP research begins at training time. Instead of training only one next-token objective at each position, the method adds heads that predict several future tokens from a shared model trunk. A compatible inference runtime may later use retained heads to propose more than one token, but that does not turn MTP into a feature I can bolt onto any arbitrary checkpoint after download.

The performance and quality results in the MTP paper belong to the models and experiments reported there. They are a reason to investigate the technique, not a benchmark result for my machine. My historical run establishes observed use of one embedded path. It does not inherit the paper's speed claims.

Engram conditional memory lives even farther from an operator toggle. It introduces learned lookup memory over token patterns as another sparsity axis in the model architecture. It is not LLM-Wiki, an Obsidian vault, Mnemosyne, a vector database, a prompt cache, or a KV cache. It belongs in this discussion because it demonstrates how easily the word memory can blur a model-design technique into an agent-operations feature that it is not.

If a capability changes how a model was designed or trained, I treat it as part of the artifact's identity. The runtime may expose it, but the runtime did not invent it.

## Conversion Is Part of the Performance Story

Conversion sits between model design and runtime operation. It decides how weights, metadata, tokenizer files, templates, quantization information, and architecture-specific geometry arrive in the artifact I will actually load. A conversion that produces smaller files but damages tensor layout or loses required metadata has not optimized the model. It has produced a different, possibly broken artifact.

This is one reason MLXForge is becoming a larger project than a file-format utility. The implemented work includes multiple conversion lanes, direct GGUF-to-MLX conversion, metadata and geometry handling, and bounded Qwen-family load and generation probes. The newer work also exercises served generation and profiling, including checks that distinguish a profiled server from an ordinary timing run. That is meaningful engineering progress, but M9 as a whole remains unaccepted. GGUF is a container, not a model architecture, so loading the container does not eliminate the need to map and qualify the geometry it contains.

The larger runtime changes remain unfinished. M10 covers a unified kernel scheduler, admission, cancellation, and batching. M11 covers memory ownership, residency, and runtime caches. M12 adds warm/cold backing state and session persistence. The complete external-MTP path belongs to M13. A draft-only loader and a weight-inventory probe do not yet constitute draft forward execution, target-and-draft pairing, speculative verification, cache rewind, parity qualification, or acceptance-rate metrics.

I want MLXForge to become the place where conversion provenance and model-specific acceleration can be qualified together. For now, the honest description is that the conversion foundation exists, the larger milestone remains under review, and the runtime acceleration path is still being designed and built.

## Let the Bottleneck Choose the First Experiment

Once I know which phase is slow, I can choose the first family of variables worth testing. The map is deliberately conservative. It does not promise that the first experiment will win. It only keeps me from changing five unrelated things and then inventing a story about the result.

{% include blog_diagram.html src="/assets/images/blog/agent-optimization/post-11-bottleneck-first-experiment.svg" alt="Measured cold load, prefill, decode, memory pressure, and concurrency bottlenecks leading to separate first experiment families" variant="wide" %}

*A measured phase narrows the first experiment. It does not choose a universal setting.*

For the local MTP question, the next benchmark is quite small. I start by recording the effective runtime configuration, then freeze the binary, artifact, prompt and template bytes, workload, sampling, context, slot count, cache formats, threads, repetitions, and machine conditions. On an artifact and runtime qualified for embedded MTP, the baseline disables it and the candidate enables only that path. Both retain correctness, time to first token, prompt and decode throughput, end-to-end latency, memory, active-path evidence, and draft acceptance.

Prompt-cache behavior is a different experiment, with cold and warm observations kept separate. KV-cache representation is another experiment because it changes memory behavior and may affect output. N-gram speculation, context changes, and concurrency changes each get their own comparison. If correctness fails, memory pressure changes the workload, or the end-to-end metric gets worse, I stop. I do not average the failure into a nicer conclusion.

[Hands-On 11A](/hands-on/2026/09/16/hands-on-tune-one-llama-cpp-variable-at-a-time/) turns that discipline into a model-neutral lab. It captures identities, command templates, active-path evidence, and stop conditions, then feeds invented result bundles through the fail-closed comparator from Hands-On 10A. The private local model and local benchmark values are not part of the teaching artifact. Start with [the runnable package](/hands-on/2026/09/16/hands-on-tune-one-llama-cpp-variable-at-a-time/#get-oriented), or jump to [the identity checks](/hands-on/2026/09/16/hands-on-tune-one-llama-cpp-variable-at-a-time/#step-4-freeze-everything-outside-the-intervention) and [report interpretation](/hands-on/2026/09/16/hands-on-tune-one-llama-cpp-variable-at-a-time/#step-7-read-the-invented-report-carefully).

## Current State

Qwen3.8 is the model I use in production. The retained Qwen3.6-family run proves that embedded MTP was selected and exercised in that earlier run, but it does not prove a speedup or establish the active path of the newer model. Those are separate questions, and I do not want a working deployment to become an accidental benchmark claim.

Upstream llama.cpp and MLX-LM provide useful reference implementations for speculative generation and cache behavior. MLXForge's current records include conversion, metadata, geometry, model probes, served-generation regression work, and profiling corrections. M9 is still under qualification. The unified scheduler, memory manager and runtime cache, warm/cold persistence, and complete external-MTP path remain unfinished milestones. I am not publishing private timing results or treating these development checks as a qualified performance comparison.

## Next Work

The next performance question is what the active runtime is doing and whether a controlled change improves the work I care about. After qualifying the artifact and its supported speculative path, I can compare that path disabled and enabled on the same workload. Prompt reuse and KV-cache representation will remain separate experiments, and every result will pass the Part 10 identity and correctness contract before it earns a performance conclusion.

Part 12 will move back up the stack and examine how these operational patterns can be packaged as installable, reviewable agent skills rather than left as private procedures.
