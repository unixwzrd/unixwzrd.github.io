---
short_url: "https://unixwzrd.ai/s/7be6df4ff1/"
short_link_basis: "/_posts/series/local-first-ai-and-agent-operations/2026-09-22-what-a-prerelease-still-has-to-prove.md"
layout: post
title: "What a Prerelease Still Has to Prove"
date: 2026-09-22 10:00:00 -0500
categories: [technology]
tags: [ai, agent-operations, local-first-ai, llm-ops-kit, devops, testing]
image: /assets/images/blog/agent-optimization/post-14-prerelease-evidence-hero.png
excerpt: "A public prerelease, green CI, and a verified archive are useful facts, but they do not automatically prove complete runtime acceptance or release authority."
series: "Local First AI and Agent Operations"
series_part: 14
series_order: 140
series_total: 17
series_url: /blog/series/local-first-ai-and-agent-operations/
series_previous_title: "Running Multiple Agents Safely on One LAN"
series_previous_url: /technology/2026/09/20/running-multiple-agents-safely-on-one-lan/
series_next_title: "Secrets-Kit: From Local Secret Store to Governed Beta Service"
series_companion_title: "Hands-On: Build a Fail-Closed Release Evidence Ledger"
series_companion_url: /hands-on/2026/09/22/hands-on-build-a-fail-closed-release-evidence-ledger/
published: true
---

This is Part 14 of the Local-First Agent Operations series. In [Part 13]({{ page.series_previous_url | relative_url }}), I worked through what it would take to call a second agent environment isolated. This time the uncomfortable word is *released*.

I went into this article expecting to write about the work remaining before LLM-Ops-Kit had anything public. That premise lasted until I compared the release checklist with the repository. The checklist still named `0.9.0b41`. GitHub already had a [public `0.9.0b49` prerelease](https://github.com/unixwzrd/LLM-Ops-Kit/releases/tag/0.9.0b49), complete with a tag, archive, manifest, checksums, and green CI.

That did not mean the checklist was useless, and it did not mean the prerelease was fully accepted. It meant I had three different records moving at different speeds, and I had been trying to read them as one.

The distinction matters because a prerelease can be perfectly real while its broader runtime acceptance remains incomplete. The artifact exists. People can download it. The source and archive identities are public. None of those facts automatically proves the complete installation, lifecycle, failure, recovery, and removal matrix I would want before wider beta adoption or a stable release.

<!--more-->

## I Needed Three Ledgers, Not One Percentage

Release conversations have a habit of collapsing into a percentage. The project is eighty percent done, ninety percent tested, nearly ready, or one checklist away. Those numbers feel precise until I ask what the denominator contains and which artifact the tests actually exercised.

I found it more useful to keep three ledgers.

The capability ledger records what the source implements. The exact-artifact acceptance ledger records what has been exercised against one version, source commit, archive digest, architecture, and time. The authorization and publication ledger records observable release facts such as tags, manifests, checksums, CI, and public assets. If approval evidence is not in the reviewed sources, that absence stays visible rather than being reconstructed from the fact that publication occurred.

{% include blog_diagram.html src="/assets/images/blog/agent-optimization/post-14-three-evidence-ledgers.svg" alt="One exact artifact identity connects separately to a capability ledger, an incomplete exact-artifact acceptance ledger, and an authorization and publication ledger containing an observed public prerelease with unknown approval provenance." caption="The ledgers share an artifact identity, but they do not advance in lockstep. A public prerelease can coexist with incomplete runtime acceptance." variant="wide" %}

The exact identity at the center is not decoration. For `0.9.0b49`, the annotated tag resolves to source commit `dbf5604b7e2281186b2e4893fd8eee7b3c12c422`. The release manifest records that same commit and says the source was clean. The archive SHA-256 is `94002a285844f15df8fe0c7212ef41fda03614a3018720739033edd42fc309f0`. The [tag CI](https://github.com/unixwzrd/LLM-Ops-Kit/actions/runs/34220164329) and [identical-tree merged-main CI](https://github.com/unixwzrd/LLM-Ops-Kit/actions/runs/34220164665) both completed successfully, and the release page reports a 237-test precheck.

Those are strong, useful facts. They establish which source produced the release, which archive is under discussion, and which CI runs belong to it. They do not establish every runtime behavior listed in an older manual acceptance document.

## The Control Plane Is Not Waiting for Its First Useful Feature

LLM-Ops-Kit is well past the shell-script experiment that started this story. It has an application-owned Python environment, immutable versioned releases, checksum verification, normal and minimal installations, repair, update, rollback, uninstall and purge paths, versioned adapters, and separate lifecycle, health, condition, and observability signals.

The control library sits under both the CLI and Textual interface. It understands configured inventory, dependency plans, remote operations, desired-state authority, configuration reconciliation, service templates, product history, logs, and component-specific ownership. Later revisions added concurrent dependency-safe startup and shutdown waves while retaining readiness gates, startup rollback, and best-effort shutdown behavior.

That implementation surface belongs in the capability ledger. It explains why the prerelease is interesting and why I have used the toolkit in a real environment. It does not move an unchecked runtime gate into the pass column.

The same rule applies to earlier testing. The project records isolated archive installation under Apple Silicon and Intel macOS accounts, installed-wheel Textual checks, coordinated update failure cases, reconciliation and conflict refusal, matching topology and catalog identity, historical rollback and cold-start work, and clean rejection of unsupported Linux installation before mutation. I can describe that evidence as historical or bounded. I cannot attribute it to `b49` unless the retained record names the `b49` source or archive identity.

## Evidence Expires at the Artifact Boundary

This is where release work becomes less glamorous than feature work. A new candidate may change only a few lines, but the affected evidence still has to follow it. The amount of repetition depends on the change, not on how tired I am of running the tests.

The gap between `b41` and `b49` is a good example. The later entries include lifecycle behavior, best-effort shutdown, live progress, streaming changes, manifest-update behavior, TTS reference handling, log inspection, configuration editing, update behavior, and runtime provenance. Version movement is normal. Letting the old candidate's acceptance record silently attach itself to the new archive is not.

I do not need to throw away every earlier result. A test can remain useful design evidence, regression context, or proof that a mechanism once worked. I do need to stop calling it exact-artifact acceptance when the identity does not match.

For this prerelease, the release record currently proves more than I first thought and less than a casual reading might imply:

| Ledger | What the reviewed evidence supports | What it does not support |
| --- | --- | --- |
| Capability | The implemented installer, control library, adapters, configuration model, CLI, TUI, logging, update, reconciliation, and lifecycle surfaces | That every path passed against the public archive |
| Exact-artifact acceptance | Clean source identity, archive and manifest identity, matching release commit, reported precheck, and green CI | The complete normal/minimal installation, lifecycle, remote-failure, protocol, recovery, teardown, and observation matrix |
| Authorization and publication | An observable public GitHub prerelease with tag and assets | The unrecorded approval decision or readiness for a wider beta audience or stable release |

The September program record makes the remaining boundary explicit: the local environment was aligned with `0.9.0b49`, but live acceptance was still pending in that update window. Local use is valuable operational evidence. It is not a substitute for a reconciled release packet.

## What the Prerelease Still Has to Prove

The unfinished work is easier to understand when grouped by the claim each gate protects.

Artifact gates bind the source commit, clean manifest, archive checksum, member layout, dependency wheelhouse, and privacy exclusions. The public assets give this work a solid starting identity. The remaining archive-content and installation claims still need their own retained evidence rather than an inference from the presence of a manifest.

Installation gates exercise the same archive through normal and minimal installation under isolated Apple Silicon and Intel accounts. They verify the application-owned runtime, immutable selection, command behavior, optional Textual dependency boundary, initialization, and imported-reference handling without borrowing Git, Conda, a shell profile, or a source checkout from the maintainer's workstation.

Lifecycle gates repeat repair, upgrade, rollback, preserving uninstall, reinstall, and purge. A purge has to remove what the toolkit owns without wandering into models, agent data, unrelated logs, or source defaults. The most dangerous installer is not the one that refuses to run. It is the one that works until cleanup decides ownership is broader than the documentation said.

Control-surface gates compare CLI and Textual behavior for status, logs, plans, configuration edits, dependent-impact refusal, confirmation, cancellation, and transactional failure. A polished interface is not useful if it silently performs a different operation from the command it displays.

Distributed gates cover remote update, older-peer bootstrap, interrupted transfer, apply failure, rollback, configuration reconciliation, drift refusal, and identity convergence. Full-stack gates then exercise chat, embeddings, proxy rendering, speech, bridge, gateway, dashboard, tunnel, and client recovery as separate observations. A healthy process is not automatically a healthy route, and a recovered tunnel is not proof that every client session reconnected.

Finally, the evidence has to survive the observation period. Backup hashes, prior runtimes, raw records, and the final report need to remain available long enough for someone else to explain a pass or a failure. A green terminal that disappears with its scrollback is not a release record.

## A Roadmap Is Not a Release Checklist

One of the easiest ways to never release software is to turn every interesting future idea into a current blocker. LLM-Ops-Kit still has worthwhile work around optional host and executable discovery, broader product-specific schemas, recovery policies, stack mutation, corrective suggestions, a proxy exchange browser, a live operational skill, a WebUI, relocation, component-native updates, and eventual Linux support.

Those items do not all belong in the `b49` acceptance matrix. They become blockers only when the release contract promises them. The opposite mistake is just as bad: treating unfinished lifecycle and data-preservation tests as optional because the maintainer can run the program today.

MLXForge and Secrets-Kit make this boundary especially important. They are independently governed products with their own artifacts, evidence, and release decisions. A future MLXForge engine adapter or Secrets-Kit provider belongs on the integration roadmap. Neither should be smuggled into the LLM-Ops-Kit prerelease as an implied dependency or used to hold this release open indefinitely.

## I Want the Failures Before the Users Find Them

The negative cases are the part of the release matrix I trust most. An unreachable peer should stop before changing another host. An interrupted transfer should leave the selected runtime alone. A later-host apply failure should produce bounded rollback evidence. Stale authority should be refused rather than merged. An active-dependent stop should require an explicit cascade or force decision.

The same thinking applies lower in the stack. A running process with failed readiness must remain running and degraded, not magically become stopped. An intentionally unobservable component should remain authority-only rather than unreachable. Tunnel loss, listener recovery, and client reconnection need separate observations. Partial startup should preserve the reason it rolled back, while best-effort shutdown should attempt the remaining components and collect every failure.

These cases are not pessimism. They are how I keep the release story from being written entirely by the happy path.

## A Small Lab for the Evidence Boundary

The [Hands-On 14A companion, *Build a Fail-Closed Release Evidence Ledger*]({{ page.series_companion_url | relative_url }}), turns the three-ledger distinction into a model-free Python lab. It uses invented artifact identities and evidence references, then rejects missing gates, duplicate records, stale evidence, identity mismatches, and unsupported approval claims.

The clean fixture deliberately records a public prerelease while installation and lifecycle evidence remain incomplete. Its successful terminal state is `EVIDENCE PACKET READY FOR REVIEW`. It never infers `RELEASE READY`, `APPROVED`, or `PUBLISHED`, and it performs no build, installation, network request, Git action, CI query, signing, upload, approval, or publication.

That may sound strict for a teaching package. It is strict because the words are the lesson. A coherent packet can be ready for human review even when the artifact is not ready for wider adoption.

## Current State

LLM-Ops-Kit `0.9.0b49` is a public GitHub prerelease tied to an annotated source commit, a clean per-file manifest, a verified archive digest, a reported 237-test precheck, and successful tag and merged-main CI. The project also has substantial implemented capability, bounded earlier acceptance results, and a locally recorded `b49` runtime.

The reviewed sources do not establish complete `b49` normal and minimal installation, repair, upgrade, rollback, preserving uninstall, purge, remote-failure, full-protocol, recovery, cold-cycle, teardown, or observation-period acceptance. They also do not contain the approval record behind the existing public prerelease. I can report the publication event without inventing its governance history.

## Next Work

The next useful step is not another feature. It is refreshing the release audit and manual acceptance documents around the existing `b49` source commit and archive digest, running the remaining identity-bound gates, retaining the results, and reconciling one report that says exactly what passed, failed, or remains unobserved.

After that, the project can make a separate decision about wider beta adoption or a stable release. Part 15 will move to Secrets-Kit, but it will start with the same discipline: current source, exact artifact, retained qualification evidence, and a clear separation between infrastructure that exists and availability that has actually been authorized.
