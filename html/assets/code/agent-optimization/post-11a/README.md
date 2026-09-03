# Hands-On 11A Companion: One Inference Intervention at a Time

This model-neutral Python 3.10+ lab validates an invented runtime-configuration experiment without downloading or running a model. It requires greedy sampling for exact normalized-output equality, proves that only one structured intervention changed, requires method-specific active-path evidence, and reuses the Hands-On 10A comparator only for median and direction-aware metric projection.

All model, machine, fingerprint, marker, and metric values are invented. They are not llama.cpp, MLX, Apple Silicon, or MLXForge benchmark results.

The teaching schema accepts only `none` and `candidate_method` as method names. Both validators enforce that vocabulary before a comparison can produce a report, including a rejected comparison. Adding a real method requires a separately reviewed schema change; raw runtime strings do not belong in this field.

## Files

| File | Purpose |
| --- | --- |
| `experiment.schema.json` | Human-readable closed JSON Schema for the teaching record |
| `command-templates.txt` | Baseline and candidate templates with one visible structured intervention |
| `experiment_lab.py` | Exact validator, eligibility classifier, versioned Part 10A projection adapter, and report rendering |
| `run_lab.py` | Bounded walkthrough using four invented fixtures and temporary reports |
| `test_experiment_lab.py` | Focused schema, identity, intervention, correctness, privacy, adapter, and cleanup tests |
| `fixtures/*.json` | Invented eligible, ineligible, and active-path-unproven records |

The companion expects the reviewed Hands-On 10A directory beside this directory. It imports `../post-10a/benchmark_compare.py` at runtime and does not alter that accepted schema or its source-fingerprint classification.

## Run the Lab

```bash
python -B run_lab.py
python -B -m unittest -v test_experiment_lab.py
python -B -c 'from pathlib import Path; [compile(p.read_text(), str(p), "exec") for p in Path(".").glob("*.py")]'
```

The lab creates reports only inside a temporary directory and verifies that the directory is removed. It starts no service, opens no network connection, creates no cache, and modifies no operator configuration.

## What the Contract Enforces

The target artifact, source, binary, tokenizer, template, workload, greedy sampling, cache, context, concurrency, batch, threads, machine class, warm/cold state, profiling state, and unrelated arguments remain frozen. The runtime configuration has its own canonical fingerprint. The reviewed `speculative_method` intervention may change only its method, optional draft-artifact identity, and method arguments.

The candidate must confirm the expected active-path marker and record a positive invented acceptance counter. Markers are short sanitized symbolic identifiers, not raw log text, paths, model names, or command lines. Missing, inactive, contradictory, unknown, or unsafe marker evidence emits no metric projection. Correctness failure or exact normalized-output drift emits `correctness_failed`. Other identity drift emits `ineligible`.

The Part 11 validator owns the `runtime_configuration_optimization` classification. The Part 10A adapter supplies only the already-reviewed median and direction-aware metric projection. It never changes the source fingerprint to manufacture an optimization classification.

## Current State

This is original model-free teaching code with invented fixtures. The walkthrough checks 15 conditions, and the test suite contains 19 tests. It does not establish compatibility or performance for a real model or runtime.

## Next Work

A separately reviewed live adapter could capture records from an operator-owned model and runtime. Any stochastic sampling mode needs a task-specific correctness contract and is intentionally rejected here.
