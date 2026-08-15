---
short_url: "https://unixwzrd.ai/s/cd70519bcf/"
layout: post
title: "When a Local AI Stack Becomes an Operations System"
date: 2026-08-17 08:00:00 -0500
categories: [technology]
tags: [ai, agent-optimization, local-first-ai, llm-ops, macos, apple-silicon, operations, agent-workflows]
image: /assets/images/blog/agent-optimization/post-01-local-ai-operations-system-hero.png
excerpt: "The model may be running while the system around it is still broken. This is how a local-first AI experiment became an operations problem involving ownership, dependencies, readiness, recovery, and rollback."
series: "Local-First Agent Operations"
series_part: 1
---

The model was running, but the client still could not connect. A tunnel appeared to exist in the service manager, yet its forwarded socket was not ready. Another process was healthy on its own and useless as part of the route. None of those failures belonged to the model itself.

That was the moment the shape of the problem became clear. We were no longer operating one model. We were operating an embedding service, text-to-speech, a model proxy, memory and retrieval, a gateway, a dashboard, local and remote clients, and the tunnels between them. Each component could work on its own while the route a person actually depended on remained broken.

What began as a proof of concept had quietly become an operations system.

<!--more-->

## The Model Was Not the Hard Part

The environment had grown one useful piece at a time. A model runner lived on one Mac. Agent-facing services lived elsewhere. Some processes were started by hand, some by launchd, and some through project-specific wrappers. Different shells supplied different environments. Logs, state, configuration, and process ownership followed the conventions of whichever component had been added at the time.

None of those choices was unreasonable in isolation. The problem was the interaction between them.

A process could be running but not ready. A proxy could answer its own health check while its upstream model route was unavailable. A tunnel could have a launchd job but no listening socket. Restarting a model could unnecessarily disturb services that did not depend on its process identity. Starting a client-facing component could fail because an upstream dependency had been left stopped. A manual command and a service manager could both believe they owned the same process.

At that point, “Can I start it?” stopped being a useful question. We needed to know who owned each component, what had to be ready first, which check proved that it was usable rather than merely alive, and what else a restart would disturb. Every operation also needed an authoritative configuration, a reproducible plan, and a rollback path. When a route or host disappeared, the system needed to show what had been lost instead of flattening the failure into a generic red light.

Local-first does not answer those questions. It describes where data and execution should live, not how many processes or computers are involved. A local-first system can still be distributed across a trusted LAN, and it can still exhibit many of the coordination and partial-failure modes of a small distributed system.

## Why Not Make the Control Plane the Runtime?

Containers, Kubernetes, virtual machines, and hosted servers were never ruled out. They already own execution, placement, and isolation; [LLM-Ops-Kit](/projects/LLM-Ops-Kit/) can coordinate services on them through adapters and authorized transports. What we rejected was rebuilding those platforms inside the control plane.

The first environment already depended on native macOS, Apple Silicon, launchd, and local model data. Repackaging everything first would have added filesystem, GPU, ownership, and networking changes. Native processes and SSH were practical first targets, not the permanent architectural limit.

We needed one place to describe ownership, endpoints, dependencies, readiness, and operational intent. launchd should supervise its jobs, a container runtime or Kubernetes cluster should own its workloads, and a virtual machine or VPS should remain a host reached through an authorized transport. External services should remain externally owned.

That boundary keeps components visible wherever they run. LLM-Ops-Kit coordinates their service relationships; it does not execute the agent's application-level workflow or replace the platform that isolates and schedules them.

## A Control Plane, Not a New Runtime

LLM-Ops-Kit emerged as that coordination layer. Its boundary is intentionally limited: it loads configured inventory, validates it, plans operations, and operates and observes heterogeneous AI components, while native process managers and applications retain execution and isolation. It does not scan a network for unknown services or provision hosts automatically. For inventory already declared in configuration, adapters can inspect configured hosts and probe declared processes, sockets, endpoints, and runtime identities; those probes observe known targets rather than discover new ones.

The control path looks almost boring on paper. That is a feature:

![LLM-Ops-Kit control flow from CLI and Textual interfaces through the shared operation model, configured-inventory validation, dependency planning, execution, typed adapters, bidirectional local or SSH transport, and known components.](/assets/images/blog/agent-optimization/post-01-control-plane.svg)

Configuration describes hosts, components, profiles, endpoints, dependencies, and lifecycle ownership. Validation turns that configuration into a topology. The planner determines ordering and impact without mutating the system. The executor applies an approved plan through an adapter and a local or remote transport.

Adapters translate that shared operation contract into native lifecycle behavior; they preserve rather than conceal the ownership, readiness, and failure semantics that differ among launchd jobs, standalone processes, HTTP services, and SSH tunnels.

The implementation is deliberately ordinary. It uses conventional technologies, each with a narrow job:

| Technology | Engineering role | Boundary it preserves |
| --- | --- | --- |
| Python package and typed control library | Shared configuration, topology, planning, execution, and status model | Keeps orchestration logic out of shell wrappers and user interfaces |
| JSON and JSON Schema | Canonical desired state, typed service templates, constraints, and UI field metadata | Makes configuration validation deterministic and reviewable |
| launchd | Native supervision for managed macOS user services | Retains macOS process ownership instead of replacing it with another daemon |
| SSH | Initial transport for authorized cross-host operations | Keeps remote execution explicit and uses configured execution identities |
| Textual | On-demand terminal interface over the same control library as the CLI | Avoids a second planner or a permanently running management service |
| UV-managed Python environment | Application-owned CPython runtime and locked application environment | Avoids dependence on system Python, Conda activation, operator virtual environments, or shell startup files |
| Checksummed immutable release artifacts | Verified repository-free installation, `current` and `previous` selection, coordinated update, and rollback | Separates released code from configuration, state, logs, and model data |

Because both interfaces call the same library, neither gets to invent its own orchestration rules. The command-line interface and Textual console share the operation model, planner, executor, adapters, and configuration. An interactive action can display its equivalent `llmops` command before it changes anything, which makes the operation reviewable and reproducible.

It also keeps adapters bounded. Each adapter owns its native lifecycle and readiness contract, so the planner needs neither product-specific shell fragments nor permission to rewrite global topology.

## Components Stay Independent; Stacks Add Coordination

We kept components and stacks separate.

A component remains independently manageable. It has an owner, a host, a profile, lifecycle semantics, readiness behavior, logs, and dependencies. A stack is only a dependency group for coordinated operation. It does not turn several services into one opaque process.

In practice, starting a component starts only missing upstream dependencies, while restarting it affects only that component unless cascading behavior is explicitly requested. A stop is refused when active dependents would be disrupted unless the operator explicitly forces or cascades the action. Stack startup follows dependency order, and shutdown reverses the actual selected startup order. If a start fails partway through, cleanup stops only the components started by that invocation and leaves pre-existing services alone. Externally owned services remain visible in status but are not mutated as a side effect of stack operations.

That can feel conservative when automatic remediation is fashionable, but predictability matters more here. The control plane can help without becoming another autonomous agent with permission to improvise on the infrastructure.

Idempotence is part of the same contract. Starting an already running component should not create a duplicate. Stopping an already stopped managed job should not turn a normal state into an error. Read-only operations such as status, health, topology, drift, plans, configuration inspection, and logs should remain read-only.

## Process State Is Not Service Health

The proof of concept also exposed the weakness of a single “status” field. A process can be running while its upstream is unavailable. A component can be healthy but intentionally unobservable from the current account. A service can be stopped because the operator asked it to stop, or stopped unexpectedly because it failed. Those states should not collapse into one green or red label.

The resulting status model separates lifecycle, desired lifecycle, health, condition, observability, ownership, configuration identity, and runtime identity. The separation gives each signal one engineering question to answer:

| Signal | Question answered | Example failure it distinguishes |
| --- | --- | --- |
| Lifecycle | Is the process running or stopped? | A missing process versus a running but unusable service |
| Desired lifecycle | Is the lifecycle state intentional? | An operator-requested stop versus an unexpected exit |
| Health | Does the configured readiness contract pass? | A live process whose endpoint cannot serve requests |
| Condition | Is drift, degradation, or another issue present? | A healthy process running stale code or using stale configuration |
| Observability | Can this operator inspect the component from here? | An intentionally restricted observation route versus an unreachable host |
| Runtime identity | Is the live process using the selected immutable release? | A successful update selection whose old process has not restarted |

The difference showed up during acceptance. A tunnel initially appeared ready based on its supervisor state before its forwarded socket accepted connections. The readiness contract had to test the route that clients actually used. Similar distinctions apply to proxies, bridges, dashboards, and model endpoints.

Health checks should therefore test the narrowest useful contract. A process probe proves existence. A socket probe proves a listener. An HTTP probe proves an application response. A small end-to-end request proves a route. None automatically proves all the others.

## Desired State and Recovery Need Their Own Design

Once multiple hosts are involved, configuration distribution becomes another operational subsystem. Copying a source checkout between machines or allowing independent edits everywhere makes it difficult to answer which state is authoritative.

The current design uses one desired-state authority and immutable, checksummed configuration revisions. Trusted control hosts can receive the complete secret-free topology required for planning. Component-only hosts receive role-filtered snapshots containing only what they need. A host selects a revision atomically. If an independent edit appears, reconciliation reports drift and refuses to merge it silently.

Runtime releases follow a similar pattern. Installation selects an immutable release while retaining previous release information for rollback. Configuration and operational state live outside the release directory, so changing code does not overwrite the data needed to operate or recover the system. Coordinated remote updates stage and verify the same artifact on selected hosts, and a failed invocation can roll back hosts it already changed.

That meant leaving development-repository synchronization behind. The control surface needed reviewed artifacts and explicit desired state, not whichever files happened to be present in a checkout.

## Migration Had to Be an Acceptance Process

Installing the control plane and starting its command proved very little. The real test was whether it could operate the existing services without losing ownership, routing, or recovery.

The migration plan adopted components one at a time. Each step captured the baseline, rendered the intended action, stopped the prior owner, started the component through the new control path, ran acceptance checks, and then either retained the change or rolled it back. A component was not allowed to remain in an ambiguous halfway state.

The private operator-v1 acceptance cycle eventually exercised fresh installation, repair, update, rollback, uninstall behavior, configuration migration, independent component restarts, dependency refusal, readiness checks, and a full-stack all-down and dependency-ordered return. It also retained previous runtimes and verified recovery archives rather than deleting the old path as soon as the new one appeared to work.

The acceptance run earned its keep by finding defects. Among them were assumptions about installation paths, validation that checked the presence of a profile but not all runtime conflicts, packaging that included the wrong source set, a stop operation that was not idempotent, remote commands that selected the wrong configuration root, a graph edge case that expanded an empty subset, and a tunnel check that reported readiness too early.

This is what acceptance testing is for. Every defect marked a place where a local success signal was weaker than the operational contract.

## Reusable Lessons

Ownership was the starting point. A component should have one lifecycle owner at a time, and the control plane must know whether it manages a process or merely observes an externally managed service.

A dependency graph turned out to be more useful than a longer startup script. It supports impact planning, safe refusal, independent restarts, partial-start cleanup, and reverse-order shutdown. A linear script gives you one happy path and very little help when the path breaks.

Planning also had to stand on its own. A non-mutating plan gives both people and tools a chance to inspect scope before accepting a change. The executor can then receive an approved, typed plan instead of reconstructing intent from interface state or unvalidated shell strings.

We treated readiness as evidence, not a label. Supervisor state, process existence, a listening socket, application health, and a completed route are different checkpoints. The right one is whichever matches the promise being made.

Rollback belonged in the installation design from the beginning. Immutable artifacts, externalized state, retained prior revisions, and bounded cleanup make recovery a normal operation instead of a late emergency procedure.

The common thread was restraint. A control plane does not need to become a model engine, container scheduler, secret store, agent framework, or autonomous remediator. It needs to coordinate those systems predictably and show the operator what it knows, what it plans, and what it cannot prove.

## Current State

At the source snapshot used for this draft, LLM-Ops-Kit has the implemented control-plane architecture described here: one public `llmops` command surface, typed adapters, dependency-aware components and stacks, shared CLI and Textual interfaces, immutable releases, configuration reconciliation, remote operation over SSH, drift reporting, and rollback behavior. The repository records private multi-host operation and later isolated installation testing on both Apple Silicon and Intel macOS.

That evidence does not mean a public beta is available. The current README explicitly says that no beta has been published, and the release checklist still requires final-artifact lifecycle repetition, explicit approval to push or tag, green macOS CI, and a prerelease package with checksums and release documentation.

## Next Work

The immediate work is to repeat the complete model, embedding, speech, proxy, bridge, gateway, dashboard, tunnel, dependency, restart, and cold-start acceptance against the final artifact rather than an earlier baseline. Publication remains a separate approval gate.

Beyond that release boundary, the roadmap includes bounded recovery policies that preserve intentional stops, a network-outage acceptance fixture, more guided discovery for operators, component-native update contracts with backup and rollback, and an optional loopback interface over the same control library. Those items remain proposed or deferred; they are not part of the current operational claim.

There is more background on the [LLM-Ops-Kit project page](/projects/LLM-Ops-Kit/), including its project-specific posts. [Secrets Kit](/projects/Secrets-Kit/) handles a different part of the local-first problem: keeping runtime secrets out of topology and logs. [MLX Harmony](/projects/mlx-harmony/) is a separate experiment with MLX engines, GPT-OSS, and the Harmony prompting structure, not the model-hosting layer. That later work belongs to MLX Forge, which remains private while it clears its initial milestones.
