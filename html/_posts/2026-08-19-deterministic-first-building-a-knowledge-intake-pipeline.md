---
short_url: "https://unixwzrd.ai/s/0fa3548506/"
layout: post
title: "Deterministic First: Building a Knowledge Intake Pipeline"
date: 2026-08-19 08:00:00 -0500
categories: [technology]
tags: [ai, agent-optimization, agent-workflows, knowledge-management, deterministic-systems, local-first, privacy, memory, macos]
image: /assets/images/blog/agent-optimization/post-02-deterministic-intake-hero.png
excerpt: "Before a model can decide what matters, the system still has to identify what exists, what changed, where it came from, and whether a human decision has already been made. I moved those jobs into a deterministic intake pipeline."
series: "Local-First Agent Operations"
series_part: 2
series_order: 20
series_total: 13
series_url: /blog/series/local-first-agent-operations/
series_previous_title: "When a Local AI Stack Becomes an Operations System"
series_previous_url: /technology/2026/08/17/when-a-local-ai-stack-becomes-an-operations-system/
series_next_title: "Memory Is a Governance Problem, Not Just a Vector Database"
series_next_url: /technology/2026/08/23/memory-is-a-governance-problem-not-just-a-vector-database/
series_next_date: 2026-08-23 08:00:00 -0500
series_companion_title: "Hands-On: Build an Idempotent Intake Manifest"
series_companion_url: /hands-on/2026/08/21/hands-on-build-an-idempotent-intake-manifest/
series_companion_date: 2026-08-21 08:00:00 -0500
published: true
---

{% assign hands_on_post = site.posts | where: "url", page.series_companion_url | first %}
{% assign hands_on_link_ready = false %}
{% if hands_on_post %}
  {% assign hands_on_link_ready = true %}
{% endif %}

At some point in almost every agent project, “have the model remember everything” starts to sound like a reasonable next step. I reached that point with a growing collection of conversations, session records, exports, notes, and operational logs. The obvious approach was to put a model in front of the pile and ask it to identify what mattered. On paper that sounded efficient; in practice, the more closely I looked at the plan, the less I trusted it.

Before a model could summarize anything, I still had to answer less glamorous questions. Which sources existed and which had changed? Were two records copies of the same source? Did a request dump count as another conversation? Could I trace a note back to its authority, and would tomorrow's run create the same candidate or another duplicate? None of these were model problems. They were inventory, identity, state, and provenance problems, and the pipeline became easier to reason about once I treated them that way.

<!--more-->

## The First Output Is an Inventory, Not a Summary

The raw material did not arrive in one neat format. Current sessions lived in an application database, older sessions existed as line-oriented exports, and documents appeared in several review locations. Some records were real dialogue; others were tool traces, automation noise, or structured request evidence that should not become a second copy of a conversation. I made the first job deliberately unambitious: find each source, assign a stable identity, fingerprint it, and record it in a manifest. At that stage, the system does not decide what anything means or create memory.

That separation matters because raw authority, manifest records, review candidates, durable knowledge, and retrieval indexes solve different problems:

| Layer | What it is responsible for | What it must not imply |
| --- | --- | --- |
| Raw source | The original session, export, or document | That every record is useful knowledge |
| Manifest | Stable identity, fingerprint, provenance, version, and processing state | That the content has been reviewed |
| Review candidate | A readable extract waiting for a person | That it may be retrieved by an agent |
| Durable filed knowledge | Material accepted and placed under normal knowledge-management rules | That it is automatically eligible for every context |
| Derived retrieval | A rebuildable index over explicitly eligible material | That it is the durable authority |

I learned to keep those layers separate because each time I blurred them, a later operation became harder to explain. Deletion became ambiguous, reruns produced duplicates, and search results appeared without a defensible path back to their source. Some of this is decidedly unglamorous bookkeeping. It is also the bookkeeping that lets me explain what the system did. The pipeline now keeps every transition visible:

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-02-knowledge-intake.svg"
   alt="Knowledge intake flow from retained raw sources through deterministic inventory, manifest records, bounded dialogue extraction, human review, durable filing, and a separate retrieval-eligibility gate."
   variant="series" %}

## Stable Identity Makes Reruns Boring

I wanted rerunning intake to be boring. The inventory derives a stable identifier from each source, computes a content fingerprint, and records the extractor version and provenance needed by later stages. When the fingerprint and relevant version have not changed, the pipeline does not normalize the source again or create another candidate.{% if hands_on_link_ready %} The hands-on follow-up shows the [small SQLite record contract behind that manifest]({{ page.series_companion_url | relative_url }}#start-with-a-small-contract).{% endif %}

That does not mean the scan avoids every read. It still fingerprints file sources and reads session messages to calculate their fingerprint; modification time remains provenance rather than a shortcut. Stable source-derived suffixes also prevent two similar extracts from colliding without exposing a real session identifier, and a regression test keeps that behavior from disappearing.

### The Rerun Test

The quickest way I found to expose a weak intake design was simply to run it again. My acceptance check asks what survives three ordinary operator actions:

| Operator action | Expected durable result |
| --- | --- |
| Run inventory twice without changing a source | The source is fingerprinted again, but no second normalization or candidate is created |
| Refresh a pending note after changing only its formatter | The note changes in place while its candidate identity and review state remain stable |
| Move a managed candidate to `Discard`, then run extraction again | The rejection remains recorded and the candidate does not return |

Those checks tell me more than a successful first import. The first run proves that the pipeline can create data; later runs show whether it respects existing data and human decisions. The Hands-On companion pulls this boundary into a standard-library Python and SQLite example, then stops at inventory because extraction, review, and retrieval have different failure modes.{% if hands_on_link_ready %} You can [run that new/unchanged/changed exercise here]({{ page.series_companion_url | relative_url }}#run-the-example).{% endif %}

## Extract Dialogue Without Asking What It Means

Once the inventory was dependable, I could produce readable review notes without asking a model what a conversation meant. The extractor keeps active user and assistant turns, drops tool roles, session metadata, request payloads, and credential-shaped material, and rejects empty or one-sided exchanges. It preserves the structure and provenance needed for review, then places the result in the queue as unclassified, pending, and excluded from retrieval. These filters are reproducible heuristics, not proof that every sensitive value has been caught, so they do not replace human privacy judgment.

## Why the Model Moved Later

My earlier design allowed bounded model-assisted extraction. It was safer than an unbounded bulk import, but when an output looked wrong I still had to ask whether the source, prompt, model, or rerun behavior caused it. That was too much uncertainty for an inventory job. The current path keeps discovery, filtering, identity, provenance, and review-state transitions deterministic. Models may help later with summaries, links, or synthesis, but those outputs remain proposals behind their own acceptance and policy gates. I use the model where interpretation adds value, not where ordinary code gives me a stronger contract.

## Move Deterministic Work Out of the Agent Loop

That rule applies to scheduling as well as intake. An early scheduler created an agent turn for every maintenance job, so log rotation, health probes, Wiki statistics and lint, source discovery, and validation could spend provider tokens or occupy a local model without using language understanding. Deterministic maintenance could even fail merely because the model endpoint was unavailable.

I moved that work into ordinary scripts supervised by `launchd`; cron or systemd timers provide the same boundary elsewhere. Runs record a lock, timeout, revision, exit state, and machine-readable result. The model consumes the output later only when interpretation adds value, such as proposing links or writing a consolidated report. The recurring audit question is simple: *Is this scheduled task making a judgment, or running a command that should have been a script?* Moving the second category out of heartbeats reduces hosted-model cost, avoids unnecessary local CPU and GPU work, and makes failures reproducible.

A future `deterministic-scheduler` skill could classify a task and generate a reviewed script and scheduler plan with ownership, an evidence contract, and rollback. It should not install scheduler entries without approval.

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-02-deterministic-scheduler.svg"
   alt="Scheduled work is divided before execution: deterministic jobs run as supervised scripts and produce machine-readable evidence, while language-model work passes through health and policy gates and remains subject to human review."
   variant="wide" %}

## LLM-Wiki Is the Filing System

The name comes from [Andrej Karpathy's original LLM Wiki idea file](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), not from a product or a canonical folder layout. The pattern has three conceptual layers: immutable raw sources; an LLM-owned collection of interlinked Markdown summaries, entities, concepts, comparisons, overviews, and syntheses; and a co-evolved schema, such as `AGENTS.md`, that teaches the agent how to ingest, query, and maintain the Wiki. Within that managed area, `index.md` is the content-oriented catalog, while `log.md` is the append-only operational history. The exact directory structure and conventions are deliberately left to each deployment.

I use that pattern as LLM-Wiki, one managed knowledge area inside a broader Obsidian Vault called Main Vault. The rest of the Vault holds review queues, selected operational material, documents, and working notes that do not need to become Wiki entries. Everything remains readable without a retrieval engine. iCloud synchronizes the Vault across my operator devices and a dedicated agent account, but it is transport rather than authority or concurrency control. Jobs still need bounded writes and locking, and multiple agents should not edit the same synchronized file concurrently.

I can share the whole Main Vault with an agent as an explicitly configured document surface without pretending that the agent owns every note it can see. Write ownership, review gates, sensitive paths, and retrieval eligibility remain policy-controlled. Karpathy's useful rule that the LLM owns the Wiki applies to the managed LLM-Wiki area in this deployment, not automatically to every adjacent document in Main Vault.

YAML Front Matter gives deterministic tools a machine-readable description of each entry while leaving the document useful in Obsidian. A sanitized review candidate can begin like this:

```yaml
---
classification: unclassified
review_state: pending
mnemosyne: exclude
source_id: conversation:example-source
source_hash: sha256:example-content-hash
related: []
---
```

Those fields are independent on purpose. Human approval does not silently grant retrieval. Front Matter records metadata; deterministic scanners and policy-aware adapters enforce its meaning. The Hands-On companion develops the same contract with complete pending, approved-but-excluded, and rejected examples.

## The Queue Is a Safety Boundary

I first treated the review directories as organization. They became a safety boundary once each location represented a different decision. `Pending Review` is readable but unclassified and excluded from retrieval. `Completed Review` means a person retained the material for curation; it still does not mean “put this in memory.” A useful document can remain in the Vault without being suitable for automatic injection.

`Discard` means rejected, not erased. The manifest keeps the rejection and prevents the same unchanged source from returning on the next run. Pending notes can also be refreshed in place after a formatting change without losing identity or review state. If a file cannot be resolved to one candidate unambiguously, the job leaves it for a person rather than guessing.

Review and retrieval answer different questions, and I do not want a directory move silently answering both:

| State | Human decision | Retrieval consequence |
| --- | --- | --- |
| `Pending Review` | No decision yet | Excluded |
| `Completed Review` | Reviewed and retained for curation | Still requires an explicit eligibility decision |
| `Discard` | Rejected | Excluded, with rejection history retained |
| Durable filed knowledge | Accepted under normal knowledge rules | Eligible only when policy explicitly permits it |

Treating those as two axes prevents a convenient filing action from silently becoming authorization to inject content into an agent conversation.{% if hands_on_link_ready %} That distinction is easier to see in the note than in a state diagram, so the tutorial walks through [sanitized front matter for pending, approved-but-still-excluded, and rejected candidates]({{ page.series_companion_url | relative_url }}#see-the-review-boundary-in-front-matter). Classification, `review_state`, and `mnemosyne` remain independent because approval must not silently grant retrieval. It then keeps the same boundary visible in [the next-stage design]({{ page.series_companion_url | relative_url }}#keep-the-next-stage-separate) rather than cramming source, review, and retrieval state into one table.{% endif %}

## Bounded Work Creates Useful Backpressure

The production workflow inventories periodically and processes candidates in bounded nightly batches. I am keeping the exact schedule and batch size private; the important point is that the limit controls runtime and keeps automation from filling the queue faster than I can review it. A growing queue is useful evidence that the batch is too large, the filters are too permissive, or review cannot keep up.

Small batches also exposed filename and formatting defects before a historical import buried them beneath thousands of plausible notes. They taught me not to confuse a successful job with fresh coverage: an oldest-first process can exit cleanly while recent material remains untouched. I still need waiting age, newest source processed, inflow, and throughput, with scheduler capacity reserved separately for catch-up and currency when both matter.

## Preserve Evidence Without Turning It Into Knowledge

I applied the same discipline to logs. Raw rolling logs stay outside LLM-Wiki; an archive job copies each active log to a source-date path and only then truncates the active file in place. That preserves evidence while allowing human-readable reports to use the date of the underlying data.

An earlier workflow filed selected rotated operational logs in Main Vault, and being able to read that history from any Obsidian device was genuinely useful. I kept the useful part with a narrower boundary: summaries, indexes, and explicitly approved or sanitized operational archives may live in the Vault's Operations area. Raw prompt logs, request bodies, credentials, and high-volume rolling output stay outside the synchronized knowledge tree. The Vault can carry portable operational history without becoming an uncontrolled second copy of every private log.

The rule I keep coming back to is to retain the authority, record its provenance, and derive only what the next stage needs. A report is not a raw log, a review note is not a session database, and a retrieval index is not a vault. Treating them as interchangeable may be convenient for the first import, but it makes every later correction harder.

## What Deterministic First Does Not Solve

I do not want deterministic intake to carry claims it has not earned. It does not decide who is authorized to retrieve a memory. It records review state, fails closed on unresolved material, and excludes candidates by default while the richer policy model remains separate work. Nor does it promise perfect cross-source deduplication, detection of every secret, or zero-cost rescanning. Stable identity and content hashes prevent repeated effects for the same source; semantic equivalence and a modification-time fast path are different problems. This is not a released ingestion product either. It is a private implementation whose design was useful enough to document and turn into a small teaching example.{% if hands_on_link_ready %} Before adapting that example to real agent data, use the [production-hardening checklist]({{ page.series_companion_url | relative_url }}#production-hardening-checklist) as a starting point rather than treating the demonstration as a finished importer.{% endif %}

## Current State

At the source snapshot used for this article, LLM-Wiki inside Main Vault is the human-readable document authority, with iCloud providing synchronization rather than retrieval policy. The private environment has deterministic inventory, stable source IDs and fingerprints, manifest-backed state, model-free dialogue extraction, bounded batches, retained rejection history, pending-note refresh, and source-date archival. Deterministic maintenance runs as supervised scripts rather than agent heartbeats. Focused regressions cover reruns, dialogue filtering, Markdown preservation, collision avoidance, refresh, discard idempotence, reviewed approval, privacy-safe linking, and copy-and-truncate archival. No public intake or scheduler artifact has been released.

## Next Work

The pipeline is useful now, but there is still work I am deliberately leaving for later. A modification-time fast path may eventually reduce the cost of inventory, but I do not want it to weaken content-hash verification or idempotence. Model-assisted summaries and link suggestions can also be evaluated after the human-review boundary rather than being pulled back into intake.

The next installment takes up the harder question this pipeline intentionally leaves open, because reviewed does not mean universally safe. Once knowledge has been reviewed, the system still has to decide whether a particular conversation is actually authorized to retrieve it. That is a policy problem, and putting it off until after similarity search is already too late.
