---
short_link_basis: "/_posts/series/local-first-ai-and-agent-operations/2026-09-20-running-multiple-agents-safely-on-one-lan.md"
short_url: "https://unixwzrd.ai/s/9945a5197f/"
layout: post
title: "Running Multiple Agents Safely on One LAN"
date: 2026-09-20 10:00:00 -0500
categories: [technology]
tags: [ai, agent-operations, local-first-ai, llm-ops-kit, macos, devops]
image: /assets/images/blog/agent-optimization/post-13-multiple-agents-lan-hero.png
excerpt: "A second account or spare machine is useful, but safe multi-agent operation requires separate evidence for process identity, configuration, ports, credentials, knowledge ownership, shared inference, and teardown."
series: "Local First AI and Agent Operations"
series_part: 13
series_order: 130
series_total: 17
series_url: /blog/series/local-first-ai-and-agent-operations/
series_previous_title: "Packaging Agent Operations as Installable Skills"
series_previous_url: /technology/2026/09/18/packaging-agent-operations-as-installable-skills/
series_next_title: "What a Prerelease Still Has to Prove"
series_next_url: /technology/2026/09/22/what-a-prerelease-still-has-to-prove/
series_next_date: 2026-09-22 10:00:00 -0500
series_companion_title: "Hands-On: Audit an Isolated Agent Testbed Before First Run"
series_companion_url: /hands-on/2026/09/20/hands-on-audit-an-isolated-agent-testbed-before-first-run/
series_companion_date: 2026-09-20 10:00:00 -0500
published: true
---

This is Part 13 of the seventeen-part Local-First Agent Operations series. In [Part 12]({{ page.series_previous_url | relative_url }}), I packaged operational judgment without turning a skill into another control plane. That raises the next question almost immediately: if I want a second agent for testing, how separate is separate enough?

My first answer was the obvious one. Give the agent another macOS account, perhaps put it on an older machine, and let it use the model server over the LAN. Different username, different home directory, different process. It looks tidy on a whiteboard.

Unfortunately, a username answers only one question. It does not tell me which configuration the process loaded, which credentials it inherited, where a home-relative log path expanded, which launchd bootstrap domain exists, which port a tunnel claimed, or who can write to the durable knowledge store. It certainly does not tell me whether uninstalling the second agent will leave the first one alone.

That is the useful problem behind this installment. I do want a second environment. I want it because a clean account and a modest machine expose assumptions that my normal development environment politely hides. I just do not want to call that environment isolated until the evidence catches up with the label.

<!--more-->

## The Spare Machine Is Supposed to Be Uncomfortable

A mature development machine is a generous accomplice. It has source checkouts, shell functions, cached packages, old virtual environments, credentials, compilers, and command-line tools accumulated over years. An installer can accidentally depend on any of them and still appear to work.

A clean account on a small macOS host is less forgiving. If the release archive needs Git, a shell profile, Conda, the system Python, or a source tree that was never part of the installation contract, the clean environment tends to say so quickly. That makes it a good place for fresh installation, repair, update, rollback, skill installation, migration, preserving uninstall, purge, and teardown tests.

It does not need to host the language model. The agent and its local control components can run on the modest node while inference comes from another machine on the LAN. That keeps the test focused on ownership and lifecycle instead of making an old computer compete with a large model.

There is already useful evidence behind this approach. An exact candidate artifact was installed under isolated Apple Silicon and Intel macOS accounts without relying on Git, system Python, Conda, shell profiles, or a source checkout. The install harness also exercises independently selected roots and the expected repair, upgrade, rollback, uninstall, migration, and purge shapes.

That is real evidence, but it is not the final answer. The current release records still leave the complete final-artifact lifecycle and protocol sequence open. Any later acceptance claim has to name the exact artifact version and digest that was tested. I cannot turn an older candidate installation into proof that the latest two-agent environment passed ports, credentials, knowledge ownership, failure containment, and teardown.

## Isolation Has Layers

The more I worked through the problem, the less useful the word *isolated* became on its own. I needed to know which boundary I meant and what observation would prove it.

{% include blog_diagram.html src="/assets/images/blog/agent-optimization/post-13-isolation-layers.svg" alt="Agent isolation is divided into execution identity, configuration authority, owned data, credentials and channels, network listeners, shared dependencies, lifecycle, failure containment, and teardown evidence gates." caption="A separate account helps, but the environment is only as separate as the weakest ownership boundary that both agents still share." variant="wide" %}

The first layer is execution identity. Which account owns the process and its files? On macOS, the answer also includes the process-manager domain. A per-user LaunchAgent normally depends on the applicable user bootstrap domain existing. Creating an account and writing a property list does not prove that the job survives the conditions I care about.

If the account will run headless, I need to observe what happens before login, after logout, after reboot, and when no interactive GUI session remains. A reviewed standalone process manager or another native service domain may be a better fit when a persistent per-user bootstrap context is unavailable. LLM-Ops-Kit can route an operation under a declared execution user, but the operating system still owns whether that user and process domain are viable.

The next layers are configuration and data ownership. Each agent needs its own configuration authority, state, logs, cache, workspace, and memory database. Home directories help, but absolute paths, inherited environment variables, shared mount points, and old compatibility links can reconnect two supposedly independent environments.

Credentials and communication channels need the same treatment. A clean test should use dedicated, least-privilege canaries for each agent. A negative test can prove that Agent A's canary is unavailable to Agent B without attempting to read another agent's real secret or operate a production identity. I do not need to poke at live credentials to learn whether the boundary was designed correctly.

## Process Identity Is Not a Decorative Field

The current control-plane tests capture an important wrinkle. If a component is declared under another execution user on the same physical machine, the control path uses the configured SSH route rather than quietly running the caller's local wrappers. Home-relative log paths are resolved against the execution user's home. Status reports execution identity separately from component identity.

Those controls stop the operator's environment from impersonating the target by accident. They still do not prove the owner of every child process or file. The acceptance report has to bind the declared component, process-manager domain, observed process owner, and owned filesystem roots. If one disagrees, a running main process is not enough.

## Ports Need Owners Too

Two agents on one host will often want the same familiar ports. Gateways, dashboards, proxies, speech bridges, callback listeners, and SSH tunnels all compete in the same socket namespace unless I separate them deliberately.

I keep a small port ledger for that reason. Each listener has a component owner, host, execution identity, bind scope, transport direction, and teardown rule.

| Listener question | Why I need the answer |
| --- | --- |
| Which component owns it? | A listening socket without an owner cannot be governed or removed safely. |
| Which account starts it? | The port may be unique while the process identity is still wrong. |
| Where does it bind? | Loopback, a LAN interface, and all interfaces expose very different surfaces. |
| Is it a service or tunnel? | A local tunnel may hide the remote destination behind an ordinary loopback port. |
| What removes it? | Teardown must remove the job and verify that the socket disappeared. |

The topology validator already rejects a tested same-host nested-runtime port conflict. A validator can only reason about ports represented in its configuration, however. An undeclared helper, stale tunnel, or manually started debug server remains an operating-system observation problem.

## Shared Inference Is Shared Fate

The clean testbed becomes practical because both agents can use one remote model server. It also creates a common-mode dependency.

{% include blog_diagram.html src="/assets/images/blog/agent-optimization/post-13-shared-inference.svg" alt="Two agent environments have separate execution identities, roots, ports, credentials, and writable stores, while both send attributable requests to one remote inference service that has shared queue, memory, cache, and latency capacity." caption="The agents can own separate private state and still interfere through a shared queue, memory budget, cache budget, or failure domain." variant="wide" %}

Endpoint availability is only the most obvious coupling. Two clients may contend for queue capacity, inference slots, memory, cache budget, rate limits, and latency. If the server cannot attribute requests to a client, I may see a slowdown without being able to explain which workload caused it.

Where the interface supports it, I want a symbolic per-client request identity and attributable logs or metrics. Then I can run each agent alone, run them together, and introduce a controlled endpoint failure. The record should show what each client observed.

Shared compute and cache capacity are not the same thing as shared conversation state. Contention does not prove prompt leakage, and I will not claim cross-request leakage without evidence. The honest statement is narrower: the clients can influence one another's performance and availability through shared resources even when their private roots are separate.

## A Synchronized Vault Is Not a Lock Manager

The knowledge boundary is where I am least willing to improvise. An earlier workspace audit found runtime files, raw sessions, logs, databases, durable notes, procedures, and synchronized material living under one broad ownership idea. It worked until I needed to explain which copy was authoritative and which process was allowed to change it.

For an initial two-agent test, I will not let both agents write to the same iCloud-backed Obsidian Vault. A synchronized view moves bytes between devices. It does not provide transactions, authorization, merge policy, or a guarantee that a reader saw one complete synchronization point.

The rule I want is precise. Every shared authoritative store has at most one writer. Every writable authoritative store has exactly one declared owner. A read-only replica or immutable input may correctly have no writer at all.

One agent can own a disposable test Vault while the other consumes a read-only copy. Both can read an immutable corpus. An independent Git clone can test explicit review and merge behavior without making the production knowledge store the experiment. I will not point two agents at the same writable synchronized tree and hope file synchronization invents a concurrency model for me.

The publisher's broader Main Vault and its LLM-Wiki material are not part of the public example. The portable lesson is ownership: synchronization is transport, not authority.

## One Operation Model, Different Agents

An agent-neutral control model makes the test more interesting. Hermes is the deployed client context in this series, but the component, endpoint, lifecycle, status, log, memory, and benchmark interfaces do not have to belong to Hermes. Another implementation, including OpenClaw, could be described through those same boundaries.

That does not make the agents equivalent or produce a comparison result. A fair comparison needs the same task corpus, model and sampling controls, tool permissions, starting memory, network conditions, stop rules, correctness checks, repeated runs, and run identity. Prompt and completion accounting must be captured rather than estimated.

Prompt overhead is measurable. It is not a verdict by itself. An agent may spend more tokens on a tool contract and avoid a costly mistake, or spend fewer tokens while omitting context required for a correct result. I want equivalent tasks and retained evidence before I say one architecture is more efficient, reliable, or capable than another.

For now, that comparison remains proposed. The second environment is first an acceptance testbed, not a product tournament.

## The Matrix I Want to Pass

This is the matrix I expect to keep beside the machine. Each gate proves a different claim.

| Gate | Evidence required before moving on |
| --- | --- |
| Install | The exact version and digest install without source checkout, shell profile, Conda, or system-Python dependence. |
| Identity | Processes and owned files resolve to the intended account and viable process-manager domain, including login, logout, reboot, and headless behavior where applicable. |
| Configuration | Each process loads the expected authority and cannot fall back to another agent's roots. |
| Network | Every listener and tunnel has a unique owner, intended bind scope, and verified teardown. |
| Credentials and channels | Dedicated least-privilege canaries prove each agent can use only its assigned references. |
| Durable data | Each writable authority has one owner, each shared authority has at most one writer, and read-only consumers make no transactional-read claim. |
| Shared inference | Requests are attributable where supported, and contention, endpoint failure, and recovery are exercised separately. |
| Lifecycle | Start, readiness, repair, update, rollback, restart, preserving uninstall, purge, and recovery use the same exact artifact. |
| Failure containment | Failure of one agent, transport, or shared endpoint does not corrupt the other agent's owned state. |
| Teardown | Jobs, processes, sockets, credentials, and toolkit-owned roots disappear while explicitly preserved user data remains. |

{% include blog_diagram.html src="/assets/images/blog/agent-optimization/post-13-acceptance-gates.svg" alt="A manifest preflight checks the declared install, identity, configuration, network, credentials, data, shared inference, lifecycle, failure containment, and teardown plan before the separate live evidence phase can begin." caption="A clean declaration is permission to begin testing. It is not evidence that the environment already passed." variant="wide" %}

Teardown belongs in the design before installation. If I cannot name the jobs, sockets, runtime roots, and credentials the second agent owns, or the user data that must survive, a purge test is just deletion with optimistic documentation.

## A Hands-On Preflight Before First Run

The companion, [Hands-On 13A: Audit an Isolated Agent Testbed Before First Run]({{ page.series_companion_url | relative_url }}), turns the declaration portion of this matrix into a small standard-library lab. It begins with the [boundary the lab refuses to cross]({{ page.series_companion_url | relative_url }}#start-with-the-boundary), then uses an invented two-agent manifest and deliberately broken fixtures for a shared root, a same-host port collision, and two writers on one shared test Vault.

The result wording matters. A clean file produces `MANIFEST READY FOR ISOLATED TEST`. It does not produce `isolated`, `secure`, or `approved`. The program opens no network path, starts no process, inspects no credential, writes no Vault, and invokes no installed control plane. It catches contradictions before provisioning, then stops where live evidence must begin.

It makes a sloppy plan fail early without pretending that a JSON file can certify the machine. Readers who want to get straight to the practical checks can run the [ready case]({{ page.series_companion_url | relative_url }}#run-the-ready-case) and then the [complete fixed walkthrough]({{ page.series_companion_url | relative_url }}#run-the-fixed-walkthrough).

## Current State

The current evidence supports isolated candidate installation on Apple Silicon and Intel accounts, independently selected installation roots, cross-user control routing under a declared execution user, execution-user-aware log paths, role-filtered secret-free snapshots, and a tested same-host port-conflict case. The current offline qualification record also identifies the installed LLM-Ops-Kit version, while leaving live acceptance pending.

The complete second-agent environment has not yet passed the full matrix. Process ownership across bootstrap conditions, unique live ports, negative credential and channel canaries, synchronized knowledge ownership, shared-inference contention, failure containment, final-artifact lifecycle repetition, and teardown still need one retained acceptance record tied to the exact tested artifact.

## Next Work

The next step is to freeze the artifact under test, record its version and digest, and run the matrix on isolated Apple Silicon and Intel accounts. The evidence package needs to remain sanitized while retaining enough identity, timing, lifecycle, port, and ownership information to explain every pass or failure.

Only after that will a second agent become useful for neutral implementation comparison. At that point I can give Hermes and another client equivalent tasks, capture prompt overhead and runtime behavior, and discuss the differences from measurements instead of preference. Part 14 places this unfinished acceptance work beside the remaining release gates rather than pretending that a long checklist is already a release.
