---
short_link_basis: "/_posts/series/local-first-ai-and-agent-operations/2026-09-06-from-shell-scripts-to-an-operator-ready-llm-ops-kit.md"
short_url: "https://unixwzrd.ai/s/c6d5e3ed95/"
layout: post
title: "From Shell Scripts to an Operator-Ready LLM-Ops-Kit"
date: 2026-09-06 10:00:00 -0500
categories: [technology]
tags: [ai, agent-operations, ai-agents, llm-ops-kit, local-first, ai-operations, devops, macos, ssh, textual]
image: /assets/images/blog/agent-optimization/post-08-operator-ready-llm-ops-kit-hero.png
excerpt: "The shell scripts worked, but they could not explain the system. I turned that useful experiment into a small control plane with one configuration model, inspectable plans, typed lifecycle boundaries, and recovery."
series: "Local First AI and Agent Operations"
series_part: 8
series_order: 80
series_total: 14
series_url: /blog/series/local-first-ai-and-agent-operations/
series_previous_title: "Multimodal Context Hygiene with a Jinja Chat Template"
series_previous_url: /technology/2026/09/02/multimodal-context-hygiene-with-a-jinja-chat-template/
series_next_title: "Voice Cloning Across Hosts: Making TTS Operational"
series_next_url: /technology/2026/09/08/voice-cloning-across-hosts-making-tts-operational/
series_next_date: 2026-09-08 10:00:00 -0500
published: true
---

I had accumulated plenty of shell scripts that worked, which was part of the problem. One knew how to start a model, another knew which Python environment belonged to a bridge, and a deployment script could copy a working tree to another host. With the right commands in the right order, I could restart most of the stack. As long as I was sitting at the same terminal with recent history in front of me, I could usually remember how all the pieces fit together.

That was not an operator interface. The scripts could perform actions, but they could not consistently answer the questions that mattered after something changed: Which configuration was authoritative? Which component depended on this endpoint? Was the process running but unhealthy, or was it intentionally stopped? Which runtime was actually serving traffic? If an update failed on the second host, what exactly had changed on the first one, and how would I put it back?

The proof of concept had done its job by showing that the services could operate together. I did not want to turn every experimental script into a permanent compatibility layer, though. I wanted to keep the useful behavior and put it behind a small control plane with one configuration model, inspectable plans, typed lifecycle boundaries, and recovery that did not depend on what I happened to remember from the last terminal session.

<!--more-->

## Configuration Needed an Owner

The old arrangement mixed shell variables, environment files, service wrappers, host assumptions, and repository state. Even I could not always explain which value would win without tracing the startup path. It might come from a global shell file, a model-specific file, an interactive environment, or whichever copy of the repository happened to be on that host.

LLM-Ops-Kit now puts that answer in canonical schema-version-two JSON. I can follow the precedence from top to bottom, with each later layer allowed to replace the value above it. The final CLI override lasts for only that invocation:

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-08-configuration-precedence.svg"
   alt="Configuration precedence flows from shipped defaults through global configuration, a referenced profile, and a role-filtered host snapshot to a temporary CLI override. The later layers determine the effective configuration."
   variant="series" %}

There is one desired-state authority. Mutable configuration lives there, while deployed commands read checksummed desired-state revisions selected through `current-config`. The installed LLM-Ops-Kit runtime is a separate rollback domain selected through the immutable release's `current` and `previous` links. Trusted control hosts receive the complete secret-free catalog they need for global status and dependency planning. Component hosts receive role-filtered snapshots containing only the profiles needed for their work. Secret values are not part of either snapshot; configuration carries references such as `env:EXAMPLE_TOKEN`, not the token itself.

I deliberately kept local interface preferences outside that authority. A Textual theme or refresh interval belongs to the operator's terminal, not to the desired state of a model host. It sounds like a minor distinction until changing a color theme changes a configuration hash and suddenly several machines appear to have drifted.

The configuration model also gave names to concepts that had been blurred together:

| Object | What it means |
| --- | --- |
| Service template | A reviewed, versioned schema for fields, lifecycle ownership, endpoints, probes, timeouts, logs, and allowed actions |
| Reusable profile | Settings for one kind of service, such as a model runtime or passive proxy |
| Component | A profile placed on a particular host with identity, ownership, tags, dependencies, and desired lifecycle |
| Endpoint connection | A typed consumer-to-provider reference that can infer a lifecycle dependency |
| Stack | A named operational grouping of components, not a new process manager |
| Runtime release | The immutable LLM-Ops-Kit code and application-owned Python environment selected on a host |

That separation made guided configuration possible without creating a second configuration language. The CLI and Textual Service Catalog both consume the same JSON Schema field records. Hidden advanced values remain in the candidate document, invalid fields fail before replacement, and every mutation is shown as an equivalent `llmops` command.

## From a Template to a Small Topology

For the article walkthrough, I would never point configuration commands at a real authority tree. The safe starting point is an isolated root with invented hosts and no usable production address:

```bash
LAB_ROOT="$PWD/llmops-part8-lab"
export LLMOPS_CONFIG_HOME="$LAB_ROOT/config"
export LLMOPS_AUTHORITY_CONFIG_HOME="$LAB_ROOT/config"
export LLMOPS_DATA_HOME="$LAB_ROOT/data"
export LLMOPS_STATE_HOME="$LAB_ROOT/state"
export LLMOPS_CACHE_HOME="$LAB_ROOT/cache"

llmops init --preset local-lan \
  --user operator \
  --model-host model-node.invalid \
  --agent-host agent-node.invalid
```

The `.invalid` names are deliberate. This is synthetic desired state, not a deployment recipe pretending to have discovered two machines. LLM-Ops-Kit loads configured inventory, validates it, and can actively probe known targets. It does not scan the network for unknown hosts, infer an unconfigured topology, provision software, or move a service merely because a host field changed.

Before creating anything, I inspect the reviewed contracts:

```bash
llmops template show llama-cpp
llmops template fields llama-cpp
llmops template show model-proxy
llmops template fields model-proxy
```

The two complete input files are deliberately unusable as services. The model path is absent, the hostnames cannot resolve, and the listeners use distinct synthetic ports:

`lab-chat.json`:

```json
{
  "schema_version": 2,
  "template_id": "llama-cpp",
  "name": "lab-chat",
  "type": "llm",
  "model_path": "/tmp/llmops-part8-lab/no-model.gguf",
  "runtime": {"host": "127.0.0.1", "port": 18080},
  "llama": {"ctx_size": 4096, "gpu_layers": 0},
  "server": {"cache_prompt": true, "extra_flags": []}
}
```

`lab-proxy.json`:

```json
{
  "schema_version": 2,
  "template_id": "model-proxy",
  "name": "lab-proxy",
  "runtime": {
    "listen_host": "127.0.0.1",
    "listen_port": 18081,
    "upstream_host": "model-node.invalid",
    "upstream_port": 18080
  },
  "logging": {"show_reasoning": false}
}
```

I use `--plan` first because I want to see the typed changes and authority hash before anything moves. Only after that looks right do I repeat the command with `--apply --yes`. Components follow the same two-stage sequence and remain disabled when added, so saving a topology does not quietly start a process.

```bash
llmops profile create lab-chat \
  --template llama-cpp --values lab-chat.json --plan
llmops profile create lab-chat \
  --template llama-cpp --values lab-chat.json --apply --yes

llmops component add lab-chat \
  --template llama-cpp --profile lab-chat \
  --stack starter --host model-host --plan
llmops component add lab-chat \
  --template llama-cpp --profile lab-chat \
  --stack starter --host model-host --apply --yes

llmops profile create lab-proxy \
  --template model-proxy --values lab-proxy.json --plan
llmops profile create lab-proxy \
  --template model-proxy --values lab-proxy.json --apply --yes

llmops component add lab-proxy \
  --template model-proxy --profile lab-proxy \
  --stack starter --host agent-host \
  --connect upstream=starter:lab-chat@openai --plan
llmops component add lab-proxy \
  --template model-proxy --profile lab-proxy \
  --stack starter --host agent-host \
  --connect upstream=starter:lab-chat@openai --apply --yes
```

The typed `upstream` connection is more than documentation. Because the proxy template declares that endpoint as required, the connection adds a lifecycle dependency on the chat component unless the template explicitly opts out. The reader does not have to remember to add a matching `depends_on` entry elsewhere, and the planner does not have to guess from a URL.

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-08-template-profile-component.svg"
   alt="A reviewed service template generates reusable profiles, profiles are placed as disabled components on invented hosts, and a typed upstream endpoint creates a provider-to-consumer lifecycle dependency."
   variant="series" %}

This is the point where I stop the synthetic mutation. I can inspect the saved objects and inferred edge without reconciling the snapshot to another host, enabling either component, or starting a service. The configuration plans are the ones reviewed above; I do not request a lifecycle start plan for a component that is still disabled:

```bash
llmops doctor
llmops config effective component starter:lab-chat
llmops config effective component starter:lab-proxy
llmops component details starter:lab-proxy
llmops topology show --component starter:lab-proxy
llmops status --all --json
```

`doctor --probe` belongs after the inventory names real, authorized targets. Static validation can still reject missing profiles, unknown hosts, dependency cycles, ambiguous references, embedded secrets, unsupported drivers, and known port conflicts while the example remains safely inert.

## A Plan Is a Durable Explanation

Most shell operations were really a command followed by a collection of assumptions in my head. The control-plane version has to explain itself: ordered steps, dependency impact, target host, execution identity, timeout, and the equivalent CLI command all belong in the validated plan.

Starting a component includes any missing upstream dependencies. Restarting one component affects only that target by default. Stopping a provider with active dependents is refused until the operator chooses force or cascade behavior. A stack starts in dependency order and stops in the exact reverse of the selected start order. Externally owned services and tool components remain visible in stack status but are not mutated as a side effect.

The executor also keeps track of what it changed. If a multi-component start fails readiness halfway through, cleanup stops only the components started by that invocation. A service that was already running before the plan began is left alone. Repeating a successful operation should converge on the same state rather than manufacture extra work.

Long operations do not belong to the lifetime of a terminal window. The Textual interface dispatches an accepted plan to a detached, short-lived worker and persists an operation record with progress, bounded output, errors, and result. Closing the TUI does not cancel a model startup, and the worker does not become a resident privileged daemon.

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-08-control-and-observation.svg"
   alt="CLI and Textual use the same validation, planner, executor, typed adapters, and local or restricted SSH transport, while operation records, status, and reviewed log channels return through the shared control library."
   variant="series" %}

## Remote Control Is Not Remote Shell

Once I started operating across several hosts, I needed to draw another line. A trusted peer can ask a configured host for status, run doctor, or request an approved component or stack operation. It uses the configured SSH route and the target's absolute installed `llmops` path, so success does not depend on an interactive login shell choosing the right Python environment by accident.

That permission is intentionally narrower than arbitrary SSH command execution. Alternate configuration roots and general shell commands are rejected. Authentication remains operator-provisioned, and the shared catalog does not distribute private keys or secret values. If a component belongs to a desktop login domain that a peer is not authorized to inspect, the result is `authority-only`, not a fabricated outage.

Status had to become more precise for that distinction to work:

| Field | Question it answers |
| --- | --- |
| Lifecycle | Is the component running, stopped, disabled, or unknown? |
| Health | Is the configured readiness or health contract healthy, degraded, unhealthy, unknown, or not applicable? |
| Condition | Does the operator need to act, or is the state intentionally down or unobserved? |
| Observability | Was the target observed, intentionally authority-only, or unreachable through an authorized route? |
| Desired and observed runtime | Is the live process using the immutable release selected by configuration? |
| Execution identity | Which configured account owns lifecycle operations, independent of the operator invoking the command? |

A proxy can therefore be `running`, `degraded`, and `attention` when its upstream model is unavailable. An intentionally stopped component can be `stopped`, desired `stopped`, and `down` without becoming an error. A peer-restricted desktop component is `unknown` and `unobserved`, which says nothing about whether the owning account would find it healthy.

## Logs and Drift Follow the Same Authority

Log access used to mean knowing a path on the correct machine. That knowledge now belongs to the reviewed service template. A component exposes named channels, and the shared log resolver combines the template with effective configuration to identify the host, execution user, path or provider unit, availability, and bounds. CLI and TUI select from those same records. Neither accepts an arbitrary path disguised as a convenience option.

Desired-state reconciliation follows a similarly conservative rule. The authority renders complete secret-free snapshots for trusted controllers and role-filtered snapshots for component hosts. Each revision carries per-file hashes. If the selected target revision matches, the plan is a no-op. If the target is unreachable, invalid, or independently edited, apply is refused. LLM-Ops-Kit does not attempt to merge two writable authorities and call the result consensus.

For the small trusted LAN I operate, that is enough. One authority, explicit hashes, visible conflicts, and a retained previous revision are much easier to reason about than a distributed configuration system whose failure modes would be larger than the services it manages.

## The Release Could Not Depend on the Repository

Repository synchronization was useful while I was experimenting because the repository doubled as the delivery mechanism. The downside was that a runtime could depend on ignored files, source-tree wrappers, a developer Python, or the state of a checkout that was never intended to be an installation.

The beta distribution replaced that with checksummed, repository-free artifacts. A standalone bootstrap verifies the selected release, bootstraps UV when necessary, installs a managed CPython and locked application environment, and selects the immutable release only after verification. Normal installation includes Textual; `--minimal` leaves it out while preserving the CLI. No Git checkout, system Python, Conda activation, or shell-profile modification is required.

Updates use the same separation of concerns. A plan does not download or mutate anything. Multi-host apply preflights every selected host, stages the same verified archive, applies sequentially, and verifies runtime and configuration identity. If a later host fails, hosts changed by that invocation are rolled back and the mixed-version result is reported. Local rollback exchanges `current` and `previous`; it does not reconstruct the old runtime from a working directory. Configuration and operational state live outside those immutable releases, so runtime rollback does not erase the operator's desired state or an agent's data.

That is why the old repository sync, runtime legacy shell reads, embedded Python shell blocks, ignored wrappers, and agent-specific privilege paths were removed instead of kept indefinitely as compatibility shims. A one-way migration can classify the old inputs, preview the result, convert likely secret literals into references, and refuse unknown material. Once migration is accepted, runtime commands read canonical JSON only. The old source remains a backup during acceptance, not a second configuration system waiting to disagree with the first one.

## Current State

LLM-Ops-Kit now has the application-owned UV-managed Python runtime, schema-driven CLI and Textual configuration, reviewed templates, reusable profiles, endpoint-derived dependencies, typed adapters, non-mutating plans, idempotent lifecycle operations, restricted SSH control, role-filtered reconciliation, independent status fields, host-qualified logs, immutable releases, and rollback described here. The current engineering record includes source, installed-wheel, clean-archive, failure-injection, reconciliation, and bounded private multi-host acceptance evidence.

It is still a macOS beta candidate, not a publicly released cross-platform operations product. The final artifact still needs the remaining repair, upgrade, rollback, uninstall, purge, complete lifecycle, and protocol repetitions recorded in the current TODO. Publication also remains behind explicit maintainer approval and green macOS CI. Linux and systemd support are experimental and are not claimed by this article.

## Next Work

The remaining usability work is no longer the vague task of “own Python” or “add guided configuration.” Those pieces now exist. What remains is more specific: optional discovery of unknown hosts and executables, broader product-specific schema coverage, safer stack membership editing, deterministic corrective suggestions, an agent-neutral operational skill, and an optional loopback WebUI that consumes the same control library instead of inventing another executor.

I also want the release gates to remain boring and explicit. Final-artifact checks, a clean rollback, protocol acceptance, and an approved prerelease are more valuable than adding another clever compatibility path. The lesson from the scripts was not that shell is bad. It was that once several hosts, runtimes, users, dependencies, and recovery paths are involved, the operator needs a durable explanation of what the system intends to do before it does it.
