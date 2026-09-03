---
short_url: "https://unixwzrd.ai/s/2242756a12/"
short_link_basis: "/_posts/series/local-first-ai-and-agent-operations/2026-09-18-hands-on-tune-one-llama-cpp-variable-at-a-time.md"
layout: post
title: "Hands-On: Tune One llama.cpp Variable at a Time"
date: 2026-09-16 10:00:00 -0500
categories: [hands-on]
tags: [ai, agent-operations, benchmarking, testing, python, privacy]
image: /assets/images/blog/agent-optimization/post-10-apple-silicon-inference-hero.png
excerpt: "Run a model-free Python lab that checks one controlled intervention, active-path evidence, and correctness before comparing invented inference results."
series: "Local First AI and Agent Operations"
series_part: "11A"
series_order: 115
series_total: 14
series_url: /blog/series/local-first-ai-and-agent-operations/
series_companion_of: 11
series_previous_title: "Where Local Inference Performance Actually Comes From"
series_previous_url: /technology/2026/09/16/where-local-inference-performance-actually-comes-from/
series_next_title: "Packaging Agent Operations as Installable Skills"
redirect_from:
  - /hands-on/2026/09/18/hands-on-tune-one-llama-cpp-variable-at-a-time/
published: true
---

This is Hands-On 11A in the Local-First Agent Operations series. It accompanies [Part 11, Where Local Inference Performance Actually Comes From](/technology/2026/09/16/where-local-inference-performance-actually-comes-from/), where I separated operator controls from model-compatible acceleration and architecture decisions. Here I want to make the experimental discipline runnable without asking you to download my model, reproduce my machine, or trust a benchmark number I have not published.

The lab is deliberately model-free. It uses invented records to answer a less glamorous but more important question: would this pair of runs be eligible for a performance comparison at all?

<!--more-->

## What We Are Testing

The example starts with an invented runtime where speculative generation is disabled. Its candidate enables an abstract method named `candidate_method`. The name is intentionally dull. It does not imply that your llama.cpp build, your model, or any particular artifact supports the method.

The candidate is allowed to change three related pieces of configuration: the method name, an optional draft-artifact identity, and the method's arguments. Together they form one structured intervention. The target model, workload, tokenizer, template, sampling, cache, context, concurrency, batch, thread count, machine class, binary, source, and unrelated arguments remain frozen.

That distinction matters because a real separate-draft experiment cannot change only a single scalar flag. It needs a draft artifact and method arguments too. Those are dependent parts of one intervention, not three excuses to change the rest of the system.

{% include blog_diagram.html src="/assets/images/blog/agent-optimization/post-11a-one-intervention-lab.svg" alt="A fail-closed lab validates closed records, greedy sampling, frozen identity, one structured intervention, active-path evidence, correctness, and Part 10A metric projection" variant="wide" %}

*The metric projection is the last step. Most mistakes should stop the experiment before arithmetic begins.*

## Get Oriented

The companion contains ten small files, including four fixtures:

| File | What it does |
| --- | --- |
| `experiment.schema.json` | Documents the closed experiment record |
| `command-templates.txt` | Puts the baseline and candidate commands beside each other |
| `experiment_lab.py` | Validates records, classifies eligibility, invokes metric projection, and renders reports |
| `run_lab.py` | Runs the bounded invented walkthrough |
| `test_experiment_lab.py` | Exercises schema, identity, correctness, privacy, adapter, and cleanup behavior |
| `fixtures/*.json` | Supplies eligible, ineligible, and active-path-unproven examples |

The companion expects Hands-On 10A beside it because I did not want to invent another median calculator and another definition of metric direction. Part 11 owns experiment eligibility and runtime-configuration classification. Part 10A supplies only its reviewed median and direction-aware projection.

Download the [complete Hands-On 11A lab]({{ '/assets/code/agent-optimization/post-11a/hands-on-11a-one-inference-intervention.zip' | relative_url }}). The archive contains the ten lab files under `post-11a/` and the unchanged comparator under `post-10a/`. Keep those directories beside each other. You do not need to download Part 10A separately.

Every source file is available here without leaving the article:

{% include source_code.html source="/assets/code/agent-optimization/post-11a/README.md" language="markdown" title="README.md" %}

{% include source_code.html source="/assets/code/agent-optimization/post-11a/command-templates.txt" language="text" title="command-templates.txt" %}

{% include source_code.html source="/assets/code/agent-optimization/post-11a/experiment.schema.json" language="json" title="experiment.schema.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-11a/experiment_lab.py" language="python" title="experiment_lab.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-11a/run_lab.py" language="python" title="run_lab.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-11a/test_experiment_lab.py" language="python" title="test_experiment_lab.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-11a/fixtures/baseline.json" language="json" title="fixtures/baseline.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-11a/fixtures/candidate.json" language="json" title="fixtures/candidate.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-11a/fixtures/candidate-ineligible.json" language="json" title="fixtures/candidate-ineligible.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-11a/fixtures/candidate-unproven.json" language="json" title="fixtures/candidate-unproven.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-10a/benchmark_compare.py" language="python" title="Part 10A comparator dependency" %}

Extract the archive in a working directory, then enter the lab:

```bash
unzip hands-on-11a-one-inference-intervention.zip
cd post-11a
python --version
```

Python 3.10 or newer is sufficient; there are no third-party dependencies. From that directory, run:

```bash
python -B run_lab.py
python -B -m unittest -v test_experiment_lab.py
python -B -c 'from pathlib import Path; [compile(p.read_text(), str(p), "exec") for p in Path(".").glob("*.py")]'
```

The walkthrough should report fifteen passing conditions. The test suite should report nineteen passing tests. The compile command should return without output. None of those results says that the invented candidate is faster on real hardware. They say the teaching contract behaves as designed.

## Step 1: Begin With a Closed Record

Each record has six top-level sections: schema version, identity, intervention, active-path evidence, correctness, and repeated observations. Missing and unknown fields fail validation. A Boolean cannot sneak into an integer field simply because Python happens to treat `bool` as a subclass of `int`.

The closed shape also creates a privacy boundary. There is no field for a prompt, completion, username, hostname, IP address, model path, credential, or conversation. If somebody adds one, the validator rejects the record rather than carrying it into a report.

Open the baseline and candidate fixtures side by side. The long repeated hexadecimal strings are obviously invented fingerprints. They authenticate nothing. Their purpose is to show where a real capture process would place content identities without publishing the content itself.

## Step 2: Make the Runtime Configuration Prove Its Own Identity

The runtime configuration is a small canonical object:

```json
{
  "speculative_method": "candidate_method",
  "draft_artifact_fingerprint": "9999999999999999999999999999999999999999999999999999999999999999",
  "method_arguments": {
    "draft_tokens": 4
  }
}
```

The validator serializes that object with sorted keys and fixed separators, calculates its SHA-256 fingerprint, and compares the result with `runtime_configuration_fingerprint`. Change `draft_tokens` without updating the fingerprint and the record fails immediately.

This fingerprint is separate from source identity. That is important. Turning a runtime method off or on does not rewrite the llama.cpp source tree. Pretending the source changed would make the record say something untrue merely to fit another comparator's classification rules.

## Step 3: Require Greedy Generation for Exact Equality

This first lab requires greedy generation and a null seed. A fixed seed is not enough to make stochastic sampling identical across CPU implementations, backends, floating-point paths, and runtime revisions. If I expect exact normalized-output hashes to match, the generation contract needs to be deterministic enough for that expectation to make sense.

Try changing the candidate sampling section to this:

```json
{
  "mode": "stochastic",
  "seed": 7
}
```

The validator rejects it before comparison. A future live adapter may support stochastic evaluation, but it will need a task-specific correctness contract reviewed on its own merits. It cannot quietly reuse exact output equality and call the result deterministic.

## Step 4: Freeze Everything Outside the Intervention

The pair comparison freezes every identity field except the run ID and the runtime configuration. If the candidate changes from warm to cold, switches the KV format, uses another workload, alters concurrency, changes context, or runs under profiling, it is ineligible.

The `candidate-ineligible.json` fixture demonstrates this by changing the KV format while also enabling the speculative method. The lab returns `ineligible` and names `cache` as the reason. It emits no metric projection.

This is the part of benchmarking that saves me from my own enthusiasm. If I turn on speculation, reduce the cache, shorten the context, and change parallel slots in one run, I may get a better number. I will not know which change produced it, and I may not have performed the same work.

## Step 5: Prove the Intended Path Was Active

Successful startup is not active-path evidence. The candidate declares an expected marker, records the observed marker, and retains a method-specific counter. These markers are sanitized symbolic identifiers such as `candidate_method_selected`, not raw log lines, paths, model names, or commands. The validator limits them to short lowercase letters, numbers, and underscores. A live adapter may derive an identifier from private evidence, but the private evidence does not belong in the portable record. In the invented fixture, the expected and observed markers match and the accepted-draft-token counter is positive.

The `candidate-unproven.json` fixture leaves the observed marker empty, sets the path state to `unknown`, and records no accepted tokens. Its terminal classification is `active_path_unproven`. Again, there is no speed comparison.

Different mechanisms will expose different evidence. A prompt-cache experiment wants an eligible identity and a confirmed hit. A KV-cache-format experiment wants the observed effective format. A speculative method wants a selected-path marker and acceptance evidence. The schema should not pretend those counters are interchangeable, but every intervention still needs a positive answer to the same question: did the runtime actually exercise what I intended to test?

## Step 6: Put Correctness Before Projection

The baseline and candidate both have to pass correctness, and their normalized-output hashes have to match under the greedy contract. Change the candidate hash or set `passed` to false and the result becomes `correctness_failed`. Metrics remain empty.

Only after schema, identity, intervention, active-path, and correctness checks pass does the versioned adapter call the Hands-On 10A comparator. Both transformed records retain the same source fingerprint, so Part 10A sees them as repeatability-shaped inputs. Part 11 does not misuse that classification. It takes only the median and direction-aware metric rows, then emits its own explicit `runtime_configuration_optimization` classification with both configuration fingerprints, the intervention contract, and active-path evidence preserved.

That separation is a little more work than changing a source hash. It is also honest.

## Step 7: Read the Invented Report Carefully

The eligible fixture produces JSON and Markdown projections in a temporary directory. Both reports contain the terminal classification, experiment kind, projection contract, both configuration fingerprints, intervention kind, phase, reviewed dependent paths, sanitized baseline and candidate configuration values, complete active-path marker and counter evidence, and median metric rows.

The invented report shows improved decode throughput alongside regressions in the other three metrics. Those numbers demonstrate report behavior, not a real performance result. They say nothing about speculative decoding, llama.cpp, MLX, Apple Silicon, or any model.

The walkthrough prints its checks and deletes its temporary reports. To read the Markdown report itself, run this from `post-11a/`; it prints the report without writing a file:

```bash
python -B -c 'from experiment_lab import load_record, compare_records, render_markdown; print(render_markdown(compare_records(load_record("fixtures/baseline.json"), load_record("fixtures/candidate.json"))))'
```

When `run_lab.py` leaves its temporary-directory block, it verifies that the report directory no longer exists. These commands do not leave an interpreter cache, start a server, call a provider, or modify operator configuration.

## Mapping the Lab to a Real Experiment

The command templates show how a later operator-owned adapter might express the baseline and candidate. Every path and value remains a placeholder. Before using a real model, I would need to qualify the artifact and license, capture the effective command rather than the intended command, define the runtime markers, retain machine and contention state, and decide which normalized correctness contract applies to the workload.

I would also keep the experiments separate. Embedded MTP off versus on is one pair. Prompt-cache cold versus warm is another. A KV-cache representation change is another. N-gram speculation, context length, and concurrency each get their own pair. The one-intervention rule is not there to make benchmarking tedious. It is what gives the result a cause I can defend.

## Current State

The model-free companion contains a closed schema, canonical runtime-configuration fingerprints, greedy exact-output correctness, structured intervention dependencies, sanitized active-path identifiers, terminal fail-closed classifications, a versioned Part 10A projection adapter, four invented fixtures, a fifteen-condition walkthrough, and nineteen tests. It runs with the Python standard library and performs no model, service, network, or persistent-cache operation.

## Next Work

The next useful addition would be a separately reviewed adapter for an operator-owned runtime. That means choosing and qualifying a model, capturing what actually ran, and deciding which correctness checks the workload needs. Until then, this lab deliberately stops at invented records. It gives me a place to test the rules before I trust them with a real performance claim.
