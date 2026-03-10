---
layout: project
title: "LLM Ops Kit"
category: LLM-Ops-Kit
permalink: /projects/LLM-Ops-Kit/
image: /assets/images/projects/LLM-Ops-Kit/LLM-OPS-Kit-banner.png
excerpt: "Operational toolkit for running, deploying, debugging, and maintaining self-hosted AI stacks across hosts."
---

## Operational Tooling for Self-Hosted AI Systems

**LLM-Ops-Kit** is the operator layer behind a practical local AI stack. It brings together service wrappers, model profiles, deployment helpers, bridge services, observability tooling, and runtime maintenance into one coherent toolkit.

It started around a local OpenClaw deployment, but the tooling is broader than that. If you are running models across multiple hosts, juggling local bridges and remote inference servers, or trying to make a self-hosted stack reproducible instead of fragile, this project is built for that kind of work.

## What It Does

LLM-Ops-Kit focuses on the parts of local AI work that usually get left to ad hoc shell history:

- Start, stop, restart, and inspect core services from a consistent command surface
- Manage model profiles for chat, embeddings, and TTS
- Route requests through local bridge and proxy services when needed
- Sync runtime assets across hosts without depending on one checked-out source tree
- Keep logs and runtime state under control with built-in maintenance and retention
- Make request and prompt behavior visible enough to debug what the model is actually seeing
- Provide streamlined ChatML and Jinja template options, including lower-context-friendly variants for smaller or more constrained machines

## Why It Exists

Most self-hosted AI stacks work fine right up until they need to survive:

- a host migration
- stale runtime state
- mismatched ports
- a wrapper lying about health
- a prompt template that is not doing what you think it is
- a model that behaves differently once tool use or TTS is involved
- an API that claims compatibility while quietly behaving differently in practice

LLM-Ops-Kit exists to close that gap between "it runs on my machine" and "I can operate this stack reliably."

## Current Focus

The current toolkit centers on:

- Qwen-based local and remote inference
- `llama.cpp` model hosting
- MLX Audio TTS with OpenAI-compatible bridge routing
- OpenClaw gateway operations and debugging
- cross-host deployment and installed-runtime workflows
- streamlined Jinja/ChatML template control for tool use and lower-context deployments

One of the biggest practical wins so far has been local TTS and voice cloning. Replacing hosted TTS for day-to-day agent use can cut costs dramatically, especially when you want frequent spoken responses without handing every request to a premium external service.

## Highlights

- Installed-runtime-first design under `~/.llm-ops/current`
- Consistent wrappers for gateway, TTS, bridges, and model servers
- Runtime status and health visibility
- Built-in log rotation and backup pruning
- Real-world debugging tools for prompt and request inspection
- Template variants that let the same stack behave better on smaller context budgets

## Project Status

The toolkit is already being used to operate a live self-hosted stack, and it is improving through direct operational pain points rather than synthetic examples.

That includes real debugging work around OpenAI-compatible request handling, bridge behavior, prompt-template selection, and the kind of subtle interoperability problems that only show up once everything is wired together end to end.

This project is early, but it is real, tested in production-like conditions, and moving quickly.

If you are building or maintaining a serious local AI environment, this is the kind of tooling that saves hours of avoidable troubleshooting.

Stay tuned for updates below as the project evolves.
