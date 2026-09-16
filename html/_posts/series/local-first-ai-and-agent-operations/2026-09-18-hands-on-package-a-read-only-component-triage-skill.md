---
short_link_basis: "/_posts/series/local-first-ai-and-agent-operations/2026-09-18-hands-on-package-a-read-only-component-triage-skill.md"
short_url: "https://unixwzrd.ai/s/2f1f452380/"
layout: post
title: "Hands-On: Package a Read-Only Component Triage Skill"
date: 2026-09-18 10:00:00 -0500
categories: [hands-on]
tags: [ai, agent-operations, llm-ops-kit, agent-skills, testing, python]
image: /assets/images/blog/agent-optimization/post-12a-read-only-component-triage-hero.png
excerpt: "Run a model-free Python lab that validates invented operational evidence, correlates canonical plans with observed state, and renders a review packet without executing a lifecycle command."
series: "Local First AI and Agent Operations"
series_part: "12A"
series_order: 125
series_total: 14
series_url: /blog/series/local-first-ai-and-agent-operations/
series_companion_of: 12
series_previous_title: "Packaging Agent Operations as Installable Skills"
series_previous_url: /technology/2026/09/18/packaging-agent-operations-as-installable-skills/
series_next_title: "Running Multiple Agents Safely on One LAN"
series_next_url: /technology/2026/09/20/running-multiple-agents-safely-on-one-lan/
series_next_date: 2026-09-20 10:00:00 -0500
published: true
---

This is Hands-On 12A in the Local-First Agent Operations series. It accompanies [Part 12, Packaging Agent Operations as Installable Skills]({{ page.series_previous_url | relative_url }}), where I drew the ownership line between a skill and the control plane beneath it.

An operational skill ought to make a good procedure easier to repeat. It should not make it easier to slip past the operator. That is the line this lab is built to hold.

The package in this tutorial reads invented, already-sanitized evidence. It validates that evidence, compares a captured status snapshot with captured canonical plans, and produces a restart review packet. It does not connect to a live LLM-Ops-Kit installation, discover dependencies, execute a command, or change a service. **Package the triage, not the orchestrator.**

<!--more-->

{% include blog_diagram.html src="/assets/images/blog/agent-optimization/post-12a-evidence-to-decision.svg" alt="Invented captured evidence passes through closed validation, privacy and identity gates, then status and canonical-plan correlation before a packet can become ready for review. Unsafe input is rejected, incomplete or stale evidence is not ready, and a no-execution boundary separates the lab from future live adapters." caption="The lab can explain why a packet is ready, incomplete, stale, or rejected. It never crosses the execution boundary." variant="wide" %}

## 1. Start With the Boundary {#start-with-the-boundary}

There are three different claims hiding inside the phrase "read-only." The requested operation may be observational. The selected subcommand may avoid changing component lifecycle. The complete invocation path may still have side effects.

That third claim matters here because the reviewed LLM-Ops-Kit entrypoint can apply an approved runtime update before dispatching an otherwise read-only command. I cannot prove a zero-mutation lab merely by calling something named `status`. The lab therefore starts with captured fixtures and never starts a subprocess.

The package contains a short skill contract, a closed schema, one deterministic renderer, three fixtures, a golden Markdown packet, an acceptance runner, and unit tests:

```text
llmops-component-triage/
|-- SKILL.md
|-- README.md
|-- manifest.json
|-- schemas/evidence-envelope.schema.json
|-- scripts/triage_packet.py
|-- fixtures/complete.json
|-- fixtures/unobserved.json
|-- fixtures/stale.json
|-- fixtures/expected-complete.md
|-- run_lab.py
`-- test_triage_packet.py
```

The manifest declares four capabilities: reading a supplied fixture, validation, correlation, and rendering. Network, subprocess, secret access, discovery, and lifecycle execution are not capabilities of this package.

Download the [complete Hands-On 12A package]({{ '/assets/code/agent-optimization/post-12a/llmops-component-triage.zip' | relative_url }}) and its [SHA-256 checksum]({{ '/assets/code/agent-optimization/post-12a/llmops-component-triage.zip.sha256' | relative_url }}). Every source file is also available here through the site's collapsed source viewer:

{% include source_code.html source="/assets/code/agent-optimization/post-12a/README.md" language="markdown" title="README.md" %}

{% include source_code.html source="/assets/code/agent-optimization/post-12a/SKILL.md" language="markdown" title="SKILL.md" %}

{% include source_code.html source="/assets/code/agent-optimization/post-12a/manifest.json" language="json" title="manifest.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-12a/schemas/evidence-envelope.schema.json" language="json" title="schemas/evidence-envelope.schema.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-12a/scripts/triage_packet.py" language="python" title="scripts/triage_packet.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-12a/run_lab.py" language="python" title="run_lab.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-12a/test_triage_packet.py" language="python" title="test_triage_packet.py" %}

{% include source_code.html source="/assets/code/agent-optimization/post-12a/fixtures/complete.json" language="json" title="fixtures/complete.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-12a/fixtures/unobserved.json" language="json" title="fixtures/unobserved.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-12a/fixtures/stale.json" language="json" title="fixtures/stale.json" %}

{% include source_code.html source="/assets/code/agent-optimization/post-12a/fixtures/expected-complete.md" language="markdown" title="fixtures/expected-complete.md" %}

## 2. Verify and Extract the Archive

Download the reviewed archive and its checksum, then verify it before extraction:

```bash
shasum -a 256 -c llmops-component-triage.zip.sha256
mkdir triage-lab
cd triage-lab
unzip ../llmops-component-triage.zip
cd llmops-component-triage
python3 --version
```

The package requires Python 3.10 or newer and uses only the standard library. There is nothing to install with `pip`.

## 3. Read the Skill Contract

Open `SKILL.md` before the Python. It says when the skill applies, what evidence it accepts, what it refuses to infer, and where it stops. The schema and renderer live outside the prompt-facing instructions because validation should not depend on a model remembering every field or regular expression.

The central rule is simple: the skill may correlate evidence, but it may not become a second dependency planner. The captured cascade plan supplies the affected membership. The status capture supplies observations. Their intersection tells us which members inside that canonical impact were observed running at capture time.

## 4. Render the Complete Packet {#render-the-complete-packet}

Use the fixed `as-of` time so freshness does not depend on the day you run the tutorial:

```bash
python3 -B scripts/triage_packet.py fixtures/complete.json --as-of 2030-01-02T03:09:05Z --format markdown
```

The complete fixture contains a target-only plan with one proxy restart and a cascade plan that stops an invented agent, restarts the proxy, and restores the agent. The status snapshot says that both affected components were observed and running. The output can therefore say `READY FOR REVIEW` and display this argument array:

```json
["llmops", "component", "restart", "demo-stack:model-proxy", "--cascade"]
```

That is structured explanation, not shell text and not permission. The package never executes the array. It also warns that the observation may have changed and requires a separately qualified live adapter to re-plan and re-observe before any approved mutation.

## 5. Compare Markdown and JSON

The same packet is available as JSON:

```bash
python3 -B scripts/triage_packet.py fixtures/complete.json --as-of 2030-01-02T03:09:05Z --format json
```

Both formats carry the decision, target, observed target state, cascade stop set, observed running impact, restore order, evidence gaps, argument array, and `executed: false` boundary. The tests compare these facts rather than trusting two renderers that merely look similar.

## 6. Remove One Reliable Observation

Now run the unobserved fixture:

```bash
python3 -B scripts/triage_packet.py fixtures/unobserved.json --as-of 2030-01-02T03:09:05Z --format markdown
```

The captured canonical plan still includes the agent, but its observation is unreachable. That is valid but incomplete evidence. The packet reports `NOT READY`, names the gap, and suppresses the argument array. It does not turn "the planner selected it" into "I know its current state."

## 7. Let Good Evidence Go Stale

Well-formed evidence is not timeless:

```bash
python3 -B scripts/triage_packet.py fixtures/stale.json --as-of 2030-01-02T03:09:05Z --format markdown
```

This capture is older than the lab's fixed ten-minute window. It becomes `evidence_stale`, even though its schema, identities, plans, and observations remain internally consistent. Again, no argument array is offered.

## 8. Try the Rejection Tests

The unit suite mutates clean fixtures to introduce unknown fields, missing fields, mismatched hashes, duplicate observations, duplicate operations, invalid plan order, raw command strings, paths, addresses, URI authorities, credential assignments, bearer material, unsupported actions, and a boolean where the integer schema version belongs:

```bash
python3 -B -m unittest -v test_triage_packet.py
```

Rejected values are not echoed into the error packet. That detail matters because a validator that helpfully repeats a secret has already lost the privacy argument. These recognizable-form checks are defense in depth, not a promise to detect every arbitrary secret. A future capture adapter still owns sanitization before the envelope becomes model-visible.

## 9. Audit the Execution Surface {#audit-the-execution-surface}

One test parses the renderer's Python abstract syntax tree and rejects imports associated with subprocesses, sockets, HTTP, SSH, or LLM-Ops-Kit. It also checks for shell execution. The manifest separately declares the package's four allowed capabilities.

This proves a bounded property of the published teaching package. It does not prove that Python, the reader's computer, or some future collector cannot mutate anything. The claim is about these reviewed files and this fixture path.

## 10. Run the Acceptance Script

```bash
python3 -B run_lab.py
```

The acceptance runner checks fourteen end-to-end conditions. The separate unit suite currently contains twenty-seven tests. Both execute entirely in memory apart from reading the package files, and `-B` prevents Python bytecode from being written.

## 11. Clean Up

Return to the directory above the disposable lab and remove it:

```bash
cd ../..
rm -rf triage-lab
```

At the end of this walkthrough, no service has been queried, no installed control plane has run, no configuration has changed, no secret has been accessed, and no lifecycle operation has occurred.

## Current State

The reviewed package is a model-free teaching artifact over three invented captures. Its complete case produces a deterministic approval packet, its incomplete and stale cases stop short of an operation array, and its tests exercise the closed schema, privacy boundary, identity binding, plan invariants, correlation rules, and lack of an execution surface. `READY FOR REVIEW` is still only a review state.

## Next Work

A live collector would be a different artifact. It would need a pinned runtime identity, an explicit update policy, current schema negotiation, bounded transport, sanitization before model visibility, capture-time identity binding, race-aware revalidation, cancellation, timeouts, and its own side-effect tests. An executor would require another explicit approval boundary and would call the canonical operation API rather than treating this packet as shell text.
