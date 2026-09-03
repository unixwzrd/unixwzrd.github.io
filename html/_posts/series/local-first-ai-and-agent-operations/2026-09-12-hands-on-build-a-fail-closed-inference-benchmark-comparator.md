---
short_url: "https://unixwzrd.ai/s/93a01b62c9/"
short_link_basis: "/_posts/series/local-first-ai-and-agent-operations/2026-09-14-hands-on-build-a-fail-closed-inference-benchmark-comparator.md"
layout: post
title: "Hands-On: Build a Fail-Closed Inference Benchmark Comparator"
date: 2026-09-12 10:00:00 -0500
categories: [hands-on]
tags: [ai, agent-operations, benchmarking, testing, python, privacy]
image: /assets/images/blog/agent-optimization/post-10-apple-silicon-inference-hero.png
excerpt: "Build a standard-library benchmark comparator that rejects incompatible runs and correctness drift before calculating median, direction-aware performance deltas."
series: "Local First AI and Agent Operations"
series_part: "10A"
series_order: 105
series_total: 14
series_url: /blog/series/local-first-ai-and-agent-operations/
series_companion_of: 10
series_previous_title: "Squeezing More Inference from Apple Silicon: llama.cpp Today, MLXForge Later"
series_previous_url: /technology/2026/09/12/squeezing-more-inference-from-apple-silicon-llama-cpp-today-mlxforge-later/
series_next_title: "Where Local Inference Performance Actually Comes From"
series_next_url: /technology/2026/09/16/where-local-inference-performance-actually-comes-from/
series_next_date: 2026-09-16 10:00:00 -0500
redirect_from:
  - /hands-on/2026/09/14/hands-on-build-a-fail-closed-inference-benchmark-comparator/
published: true
---

This lab accompanies [Part 10: Squeezing More Inference from Apple Silicon: llama.cpp Today, MLXForge Later]({{ page.series_previous_url | relative_url }}). The main article explains why a performance comparison needs identity and correctness before arithmetic. Here, we are going to make that rule executable.

I deliberately kept this lab away from a real inference engine. It uses invented JSON fixtures and the Python standard library. You do not need MLXForge, a model, a GPU, Apple Silicon, a provider account, or a network connection. Nothing in the synthetic results says how fast any real machine or engine is.

What the lab does prove is narrower and more useful: it can reject an invalid document, distinguish a repeatability run from an optimization run, stop an incompatible comparison, block a speed conclusion after correctness drift, calculate median direction-aware deltas, and render the same bounded result as JSON, TSV, and Markdown.

<!--more-->

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-10a-comparator-flow.svg"
   alt="Synthetic benchmark bundles pass through closed-schema validation, identity compatibility, correctness, median aggregation, direction-aware deltas, and bounded reports; failures stop without a speed conclusion."
   variant="wide" %}

## What You Will Build

The companion contains exactly eight files:

```text
README.md
benchmark_compare.py
run_lab.py
test_lab.py
fixtures/baseline.json
fixtures/candidate-optimization.json
fixtures/candidate-ineligible.json
requirements.txt
```

`benchmark_compare.py` owns validation, eligibility, aggregation, and report rendering. `run_lab.py` performs the bounded walkthrough and removes its temporary reports. `test_lab.py` exercises the failure boundaries. The three fixtures are invented and small enough to inspect by eye. `requirements.txt` documents that there are no third-party dependencies.

Download the [complete eight-file Hands-On 10A package]({{ '/assets/code/agent-optimization/post-10a/hands-on-10a-fail-closed-inference-comparator.zip' | relative_url }}). Every file is also available below through the site's standard collapsed source viewer.

{% include source_code.html source="/assets/code/agent-optimization/post-10a/README.md" language="markdown" title="README.md" %}

{% include source_code.html source="/assets/code/agent-optimization/post-10a/benchmark_compare.py" language="python" title="benchmark_compare.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-10a/run_lab.py" language="python" title="run_lab.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-10a/test_lab.py" language="python" title="test_lab.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-10a/requirements.txt" language="text" title="requirements.txt" %}

{% include source_code.html source="/assets/code/agent-optimization/post-10a/fixtures/baseline.json" language="json" title="fixtures/baseline.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-10a/fixtures/candidate-optimization.json" language="json" title="fixtures/candidate-optimization.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-10a/fixtures/candidate-ineligible.json" language="json" title="fixtures/candidate-ineligible.json" %}

Start in a copy of the companion directory and inspect the files before running them:

```bash
find . -maxdepth 2 -type f -print | sort
python --version
```

Python 3.10 or newer is sufficient. The lab does not install anything and does not read configuration outside its directory.

## Step 1: Inspect the Closed Schema

Open `fixtures/baseline.json`. The document has four top-level fields: `schema_version`, `identity`, `correctness`, and `observations`. Unknown fields are rejected rather than ignored.

The identity block carries the conditions that determine whether the arithmetic has meaning. A model label is present for human orientation, but the artifact fingerprint is the comparison identity. The workload and sampling fingerprints represent the semantic request and generation controls without storing the prompt itself. Machine class, memory, context, concurrency, batch, warm or cold state, and profiling state describe the execution conditions.

The correctness block contains a Boolean result and a normalized output hash. This is an equality contract for the lab, not a quality score. The observations contain four metrics:

| Metric | Direction | Meaning in this lab |
| --- | --- | --- |
| `ttft_ms` | Lower is better | Time to the first token measurement point |
| `prompt_tokens_per_s` | Higher is better | Prompt prefill throughput |
| `decode_tokens_per_s` | Higher is better | Generated-token throughput |
| `peak_wired_mb` | Lower is better | Peak wired memory |

Every observation must carry the same metric set, and every fixture needs at least three observations. The comparator uses the median. Three synthetic samples do not establish statistical significance; they simply make the aggregation rule visible.

## Step 2: Run the Bounded Walkthrough

Run:

```bash
python run_lab.py
```

The runner prints one JSON object with 20 named conditions. A successful run ends with:

```json
{
  "ok": true,
  "passed": 20,
  "total": 20
}
```

The full output includes every condition rather than only the totals. That matters when the lab fails because you can see which boundary changed. The runner creates JSON, TSV, and Markdown projections inside a temporary directory, checks their agreement, and removes the directory before reporting `cleanup_complete`.

The runner does not hide a failed assertion behind a zero exit status. If any condition is false, it exits nonzero.

## Step 3: Compare an Optimization Candidate

Run the comparator directly:

```bash
python benchmark_compare.py fixtures/baseline.json fixtures/candidate-optimization.json
```

The candidate uses the same artifact, workload, sampling, machine, context, cache state, profiling state, concurrency, and batch size as the baseline. Its source fingerprint differs, so the comparator labels the experiment `optimization`.

The report shows baseline median, candidate median, absolute delta, percentage delta, expected direction, and outcome for each metric. Notice that a negative delta can be an improvement for latency or memory, while a positive delta can be an improvement for throughput. Direction belongs to the metric definition; it should not be guessed by a report viewer.

Try the other formats:

```bash
python benchmark_compare.py fixtures/baseline.json fixtures/candidate-optimization.json --format json
python benchmark_compare.py fixtures/baseline.json fixtures/candidate-optimization.json --format tsv
```

All three projections come from the same validated comparison object. The tool does not parse its own Markdown or recalculate a TSV independently.

## Step 4: Turn It into a Repeatability Check

Copy `candidate-optimization.json` to a temporary file and replace its `source_fingerprint` with the baseline source fingerprint. Leave the other identity fields alone, then compare it again.

The classification remains `comparable`, but the experiment kind changes to `repeatability`. That distinction prevents an unchanged program being advertised as a code optimization merely because normal run-to-run variation moved a median.

Do not edit the artifact or workload fingerprint for this step. Those changes describe different content, not a repeat of the same experiment.

## Step 5: Watch an Incompatible Run Stop

Now run:

```bash
python benchmark_compare.py fixtures/baseline.json fixtures/candidate-ineligible.json
```

The command exits with status 2 and reports `ineligible`. The candidate is cold while the baseline is warm. Its numbers may be interesting in a cold-start experiment, but they cannot be mixed into this warm comparison.

The same stop occurs when artifact, workload, sampling, machine, memory, profiling, concurrency, batch, or context identity differs. Matching profiled runs also stop because profiling is diagnostic and does not belong in a throughput baseline. The report names the reason and emits no metric rows. A rejection is not a failed benchmark run. It is the comparator doing its job before a misleading conclusion escapes.

## Step 6: Prove That Correctness Blocks Speed

Copy the optimization fixture, set `correctness.passed` to `false`, and compare it with the baseline. You can also leave `passed` true and change the normalized output hash.

Either change produces `correctness_failed`, with no performance metrics in the result. The tool does not print faster numbers with a warning beneath them. I made that a terminal state because warnings are easy to quote around.

This rule is intentionally stricter than many exploratory notebooks. If you are evaluating an intentional quality change, define a different experiment and quality contract. Do not silently reuse a deterministic regression contract that the candidate no longer satisfies.

## Step 7: Break the Schema on Purpose

Add an unexpected field such as `hostname` to the identity object and run the comparator again. It fails schema validation. Then remove the field and change `memory_gb` from `32` to `true`. That also fails.

Python treats `bool` as a subclass of `int`, so a careless numeric validator will accept `true` as memory capacity. The lab rejects it explicitly. It also rejects missing fields, uppercase or malformed fingerprints, empty observations, inconsistent metric columns, negative values, and non-finite values such as infinity or NaN.

Failing closed here is not pedantry. Quietly accepting a field that one version ignores and another interprets is how evidence formats become ambiguous.

## Step 8: Run the Regression Tests

Run:

```bash
python -m unittest -v test_lab.py
python -B -m py_compile benchmark_compare.py run_lab.py test_lab.py
```

The nine tests cover optimization and repeatability classification, cross-engine labels under a matched contract, identity mismatches, exclusion of matching profiled runs, correctness drift, exact schema behavior, median and direction-aware outcomes, a zero baseline percentage, deterministic projections, and absence of prompt or output fields.

The cross-engine-label test deserves a note. The `engine` string may differ because the lab is engine-neutral. That does not relax artifact, workload, sampling, machine, or execution-state compatibility. In a real cross-format comparison, you would still need a documented equivalence contract if exact artifact identity cannot be preserved.

## Step 9: Confirm the Privacy Boundary

Search the package:

```bash
rg -n 'hostname|ip_address|api_key|bearer|customer|conversation|output_text' .
```

The test source contains some forbidden names as negative cases, but the fixtures and reports contain no real host, account, address, private path, prompt, completion, token, credential, or model-generated artifact. Fingerprints and IDs are visibly invented. They do not authenticate a real model or source revision.

The metric name `prompt_tokens_per_s` is safe because it describes a numeric measurement, not prompt content. A privacy rule that merely searches for the substring `prompt` would confuse a metric with the material the metric describes.

## Step 10: Clean Up

`run_lab.py` cleans its generated reports automatically. If you created modified fixture copies during the walkthrough, remove only those copies. Do not remove the eight companion files.

Confirm that no interpreter cache was retained:

```bash
find . -type d -name __pycache__ -print
find . -type f -name '*.pyc' -print
```

The intended result is no output. The lab starts no service, loads no model, opens no network connection, creates no persistent cache, and touches no operator configuration.

## Current State

The companion is an original standard-library teaching implementation with three invented fixtures, 20 bounded acceptance conditions, and nine unit tests. It validates an exact closed schema, distinguishes optimization from repeatability, rejects incompatible and profiled runs, requires matching normalized correctness, aggregates medians, calculates direction-aware deltas, and emits deterministic bounded projections.

Its synthetic values test comparator behavior only. They are not Apple Silicon measurements, MLXForge evidence, engine recommendations, or hardware guidance.

## Next Work

The natural extension is a small adapter that maps a privacy-reviewed export from an inference engine into this schema. That adapter should remain outside the comparator and should never scrape a private run directory indiscriminately. It needs explicit ownership of redaction, field mapping, units, token accounting, and artifact-equivalence rules.

Real benchmark publication would add frozen source identity, retained correctness evidence, repeated observations with spread, contention notes, and a reviewed disclosure package. The comparator should stay boring. Its job is to stop bad comparisons early and make the surviving arithmetic easy to inspect.
