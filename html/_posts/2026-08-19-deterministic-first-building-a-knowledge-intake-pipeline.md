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

The raw material did not arrive in one neat format. Current sessions lived in an application database, older sessions existed as line-oriented exports, and documents appeared in several review-oriented locations. Some records contained real dialogue between a user and an assistant. Others were tool traces, automation noise, or structured request evidence that should never have been treated as a second copy of a conversation. I made the first job of the pipeline deliberately unambitious: find those sources, assign a stable identity, fingerprint their contents, and describe them in a manifest. At that stage, the system does not decide what anything means and does not create memory.

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

I wanted rerunning intake to be boring. For each source, the inventory derives a stable identifier from its origin and computes a content fingerprint. The manifest records both, together with the extractor version and enough provenance to understand anything created later. When the fingerprint and relevant version have not changed, the pipeline avoids repeating normalization and downstream candidate work.{% if hands_on_link_ready %} The hands-on follow-up shows the [small SQLite record contract behind that manifest]({{ page.series_companion_url | relative_url }}#start-with-a-small-contract).{% endif %}

I have to be precise about where that optimization begins. The current implementation still opens and fingerprints file sources, and it still reads session messages to calculate their fingerprint. Modification time is retained as provenance; it is not a fast path that skips the scan. The idempotence is in the durable effects: unchanged sources are not normalized again and do not produce duplicate candidates. It is not yet an optimization that avoids every read.

Stable identity also fixed a more tangible problem. Two conversation extracts could land on the same date with similar titles and session suffixes, producing a filename collision even though they came from different sources. Adding a stable source-derived suffix made the names collision-resistant without publishing a real session identifier, and a regression test now keeps that behavior from quietly disappearing.

### The Rerun Test

The quickest way I found to expose a weak intake design was simply to run it again. My acceptance check asks what survives three ordinary operator actions:

| Operator action | Expected durable result |
| --- | --- |
| Run inventory twice without changing a source | The source is fingerprinted again, but no second normalization or candidate is created |
| Refresh a pending note after changing only its formatter | The note changes in place while its candidate identity and review state remain stable |
| Move a managed candidate to `Discard`, then run extraction again | The rejection remains recorded and the candidate does not return |

Those checks tell me more than a successful first import. The first run only proves that the pipeline can create data; later runs show whether it respects data and human decisions that already exist. In the Hands-On companion, *Build an Idempotent Intake Manifest*, I pull the smallest useful part into a standard-library Python example with a SQLite record contract and the same three-run exercise. It stops deliberately at inventory because extraction, review, and retrieval are different stages with different failure modes.{% if hands_on_link_ready %} You can [run that new/unchanged/changed exercise here]({{ page.series_companion_url | relative_url }}#run-the-example).{% else %} That hands-on article follows on August 21.{% endif %}

## Extract Dialogue Without Asking What It Means

Once the inventory was dependable, I could turn eligible session records into readable review notes without asking a model what the conversation meant. The extractor keeps active user and assistant turns, excludes tool roles and session metadata, rejects empty or one-sided exchanges, and applies explicit minimum-content and natural-language checks. It also drops messages matching request, tool, credential, or other payload patterns that should not be copied into a note. Structured request dumps remain evidence rather than becoming alternate conversation sources.

I kept these rules intentionally modest. They do not pretend to recognize a brilliant insight; they ask whether a record looks like a real exchange, contains enough dialogue to review, and can be rendered without obvious operational noise. The result preserves paragraphs, lists, code blocks, roles, timestamps when available, and source provenance, then enters the queue as unclassified, pending, and excluded from retrieval. String and structure filters are still heuristics, not proof that every sensitive value has been caught, so deterministic filtering improves reproducibility without replacing human privacy judgment.

## Why the Model Moved Later

My earlier design allowed bounded model-assisted extraction. I constrained the work per run, along with model calls, tokens, and elapsed time, which was safer than turning a model loose on a bulk import. The model sometimes did useful work, but it was still probabilistic behavior too early in the lifecycle. When an output looked wrong, I first had to determine whether the source was wrong, the prompt was wrong, the model had made a poor choice, or the pipeline had processed the same material twice. That is too many moving parts for what should have been an inventory job.

The current path moves model calls out of inventory and dialogue extraction. For the same source and extractor version, discovery, filtering, identity, provenance, and review-state transitions now produce the same kind of result. I can inspect what was kept, what was skipped, and why without interpreting a generated summary first. Models may still help after review by suggesting summaries, proposing links, or assisting with synthesis, but those outputs belong to later, separately governed steps and remain proposals until their own acceptance and policy gates exist. I use the model where interpretation adds value, not where ordinary code can give me a stronger contract.

## The Queue Is a Safety Boundary

I initially thought of the review directories as a convenient way to keep notes organized. They became more important once I recognized that each one represents a different decision. `Pending Review` means the extractor produced something readable, but nobody has approved its classification, usefulness, filing location, or links, so it remains excluded from retrieval. `Completed Review` means a person has reviewed and retained the material for curation; it still does not mean “put this in memory.” A note can be valuable durable documentation and still be inappropriate for automatic injection into an agent conversation.

`Discard` means rejected, not erased. When a managed candidate is moved there, the pipeline records the rejection in the manifest, marks it excluded from retrieval, rejects pending link suggestions, and retains the note as history. A later run recognizes that state and does not recreate the candidate. If the file does not contain enough identity to resolve one candidate unambiguously, the job leaves it for manual attention rather than guessing.

Retaining that history prevents a failure I did not want to keep rediscovering: I reject a low-value extract, the next scheduled run sees the unchanged raw session, and the same note returns as though the decision never happened. I do not need the automation arguing with a decision I already made. The pipeline also lets me refresh pending notes after a formatting change by re-rendering them in place while preserving candidate identity and review state, so presentation can improve without pretending that the source or the human decision is new.

Review and retrieval answer different questions, and I do not want a directory move silently answering both:

| State | Human decision | Retrieval consequence |
| --- | --- | --- |
| `Pending Review` | No decision yet | Excluded |
| `Completed Review` | Reviewed and retained for curation | Still requires an explicit eligibility decision |
| `Discard` | Rejected | Excluded, with rejection history retained |
| Durable filed knowledge | Accepted under normal knowledge rules | Eligible only when policy explicitly permits it |

Treating those as two axes prevents a convenient filing action from silently becoming authorization to inject content into an agent conversation.{% if hands_on_link_ready %} That distinction is easier to see in the note than in a state diagram, so the tutorial walks through [sanitized front matter for pending, approved-but-still-excluded, and rejected candidates]({{ page.series_companion_url | relative_url }}#see-the-review-boundary-in-front-matter). Classification, `review_state`, and `mnemosyne` remain independent because approval must not silently grant retrieval. It then keeps the same boundary visible in [the next-stage design]({{ page.series_companion_url | relative_url }}#keep-the-next-stage-separate) rather than cramming source, review, and retrieval state into one table.{% endif %}

## Bounded Work Creates Useful Backpressure

The production workflow inventories periodically and processes conversation candidates in bounded nightly batches. I am keeping the exact schedule and batch size private, but the reason for the limit is more interesting than the number. A bounded batch limits runtime, makes recovery understandable, and keeps automation from filling the review queue faster than a person can inspect it. If the pending queue grows continuously, that is useful operational evidence: the batch may be too large, the filters too permissive, or the review process unable to keep up.

An unbounded historical import would have hidden that feedback beneath a mountain of plausible-looking notes. There is no prize for generating thousands of notes that nobody has time to review. Small batches gave me room to inspect representative output, fix filename and formatting defects, refresh existing candidates safely, and only then widen the backlog run. In this case, slower turned out to be more efficient because it spent less human attention cleaning up avoidable output.

The bounded queue also taught me not to confuse process health with freshness. An oldest-first job can succeed every night while recent material remains buried behind historical backlog, so exit status alone is weak evidence. I also need the oldest waiting age, newest source processed, inflow, and throughput. If catch-up and currency both matter, the scheduler can reserve capacity for each instead of letting one workload hide the other.

## Preserve Evidence Without Turning It Into Knowledge

I applied the same discipline to logs. Raw operational logs stay outside the knowledge vault; an archive job copies each active log to a source-date path and only then truncates the active file in place. It reports that source files were not deleted, and a repeated run ignores an already empty active log. That preserves the evidence while allowing reproducible, human-readable reports to use the date of the underlying data rather than the day I happened to generate the report. It also prevents the knowledge base from becoming a second log store full of private request material.

The rule I keep coming back to is to retain the authority, record its provenance, and derive only what the next stage needs. A report is not a raw log, a review note is not a session database, and a retrieval index is not a vault. Treating them as interchangeable may be convenient for the first import, but it makes every later correction harder.

## What Deterministic First Does Not Solve

I do not want deterministic intake to carry claims it has not earned. It does not decide who is authorized to retrieve a memory. It records review state, fails closed on unresolved material, and excludes candidates by default while the richer policy model remains separate work. Nor does it promise perfect cross-source deduplication, detection of every secret, or zero-cost rescanning. Stable identity and content hashes prevent repeated effects for the same source; semantic equivalence and a modification-time fast path are different problems. This is not a released ingestion product either. It is a private implementation whose design was useful enough to document and turn into a small teaching example.{% if hands_on_link_ready %} Before adapting that example to real agent data, use the [production-hardening checklist]({{ page.series_companion_url | relative_url }}#production-hardening-checklist) as a starting point rather than treating the demonstration as a finished importer.{% endif %}

## Current State

At the source snapshot used for this article, I have deterministic source inventory, stable source IDs and content fingerprints, manifest-backed processing state, model-free dialogue extraction, bounded batches, retained rejection history, pending-note refresh, and source-date log archiving. The repository includes focused regressions for repeated inventory, dialogue filtering, Markdown preservation, filename-collision avoidance, refresh behavior, discard idempotence, reviewed approval, privacy-safe linking, and copy-and-truncate archival. Project records also show periodic inventory and bounded nightly extraction running in the private environment, including a corrected filename-collision defect and successful rerun. During technical review, the focused offline regressions for inventory, conversation extraction, knowledge review, and source-date archival passed again. No public intake artifact has been released.

## Next Work

The pipeline is useful now, but there is still work I am deliberately leaving for later. A modification-time fast path may eventually reduce the cost of inventory, but I do not want it to weaken content-hash verification or idempotence. Model-assisted summaries and link suggestions can also be evaluated after the human-review boundary rather than being pulled back into intake.

The next installment takes up the harder question this pipeline intentionally leaves open, because reviewed does not mean universally safe. Once knowledge has been reviewed, the system still has to decide whether a particular conversation is actually authorized to retrieve it. That is a policy problem, and putting it off until after similarity search is already too late.
