---
short_link_basis: "/_posts/2026-08-23-memory-is-a-governance-problem-not-just-a-vector-database.md"
short_url: "https://unixwzrd.ai/s/857d25f9d2/"
layout: post
title: "Memory Is a Governance Problem, Not Just a Vector Database"
date: 2026-08-23 08:00:00 -0500
categories: [technology]
tags: [ai, agent-operations, ai-agents, memory, knowledge-management, governance, local-first, privacy, retrieval, macos]
image: /assets/images/blog/agent-optimization/post-03-memory-governance-hero.png
excerpt: "A relevant memory from the wrong context is not a better result; it is a disclosure. I moved authorization ahead of ranking and kept durable authority separate from disposable retrieval state."
series: "Local First AI and Agent Operations"
series_part: 3
series_order: 30
series_total: 14
series_url: /blog/series/local-first-ai-and-agent-operations/
series_previous_title: "Deterministic First: Building a Knowledge Intake Pipeline"
series_previous_url: /technology/2026/08/19/deterministic-first-building-a-knowledge-intake-pipeline/
series_next_title: "The Agent Memory and Optimization Tool Landscape"
series_next_url: /technology/2026/08/25/the-agent-memory-and-optimization-tool-landscape/
series_next_date: 2026-08-25 10:00:00 -0500
series_companion_title: "Hands-On: Build a Fail-Closed Memory Router"
series_companion_url: /hands-on/2026/08/25/hands-on-build-a-fail-closed-memory-router/
series_companion_date: 2026-08-25 08:00:00 -0500
published: true
---

When I first added persistent memory to an agent, the attractive part was the retrieval. A question arrived, the system embedded it, nearby memories came back, and the agent appeared to remember something from an earlier session. That is an impressive demonstration, but it is not yet an operational memory system. The difficult question is not whether a memory is relevant. It is whether this conversation, with these participants and this purpose, is allowed to receive it.

That distinction became impossible for me to ignore once the same agent began moving among private conversations, technical work, general operations, and material that was still waiting for human review. Similarity search has no instinct for those boundaries. It can find the wrong thing extremely well. A highly relevant answer from the wrong project or private context is not a better retrieval result; it is a disclosure.

The conclusion I came to was simple, although the implementation is not: memory is a governance problem with a search component. The vector database matters, but it belongs behind authority, review, classification, provenance, and access decisions rather than standing in for them.

<!--more-->

## Keep the Authority Somewhere a Human Can Read

I treat the reviewed knowledge vault as the durable authority. It holds ordinary documents with explicit metadata and a history that I can inspect without depending on an embedding model, a retrieval library, or the current shape of a database. The memory engine is derived state. Its chunks, vectors, facts, summaries, links, and indexes exist to make approved material useful to an agent, but I must be able to discard and rebuild them from the authority.

In my setup, that authority is Main Vault, an Obsidian Vault synchronized through iCloud across my operator devices and a dedicated agent account. LLM-Wiki is the structured Markdown knowledge area inside it, while the broader Vault also carries review queues, selected operational reports, and other working material. Obsidian makes that authority navigable and editable; iCloud transports copies between devices. Neither decides whether an item has been reviewed or whether an agent may retrieve it, and synchronized files still require ordinary locking and conflict discipline.

The complete Vault can be an explicitly configured document surface for an agent, but filesystem access is not blanket ownership. The agent may own and maintain the managed LLM-Wiki area while write permissions, review requirements, sensitive paths, and retrieval eligibility continue to govern the rest of Main Vault.

Each managed note carries the relevant state in YAML Front Matter. A sanitized entry might begin:

```yaml
---
classification: confidential
review_state: approved
mnemosyne: exclude
source_id: document:example-source
source_hash: sha256:example-content-hash
related:
  - "[[Example System]]"
---
```

This is deliberately not one `approved` Boolean. Classification describes sensitivity, `review_state` records the human review decision, and `mnemosyne` controls whether the note is eligible for the derived retrieval system. An approved note can therefore remain durable, linked, and visible in Obsidian without being injected into an agent conversation. Front Matter only records the decision; deterministic scanners and the retrieval policy must validate and enforce it.

That boundary sounds like routine data engineering until something changes. Suppose I correct a document, restrict its audience, or decide it should no longer be available to an agent. If the vector store has become the only practical copy, I no longer have a clean answer to “what must be removed?” One source may have produced several chunks, an embedding for each chunk, extracted facts, graph links, cached search results, and a consolidated summary. Deleting one row that happens to contain familiar text does not prove that the information is gone.

This is why I now think of provenance as part of deletion rather than an optional audit feature. Every derivative needs a path back to its source, and every derivative made from several sources needs the complete source set. Correction, restriction, and deletion begin at the authority, then propagate through the derived graph. Re-indexing is not a disaster when the derived store is genuinely disposable; it is the expected repair mechanism.

| Layer | Durable responsibility | What I should be able to do |
| --- | --- | --- |
| Main Vault and LLM-Wiki | Reviewed content, classification, review decision, retrieval eligibility, and source history | Read, correct, classify, retain, or remove material without the memory engine |
| Policy registry | Trusted context mappings and the rules used to interpret them | Explain why a context may read or write a class of memory |
| Derived memory | Chunks, vectors, facts, links, summaries, and search structures | Purge and rebuild from approved authority |
| Runtime cache | Reusable query plans or retrieved fragments | Invalidate whenever participants, policy, or source authority changes |

The distinction also keeps human review honest. A document can be useful enough to retain without being eligible for automatic retrieval. In the intake pipeline from the previous installment, classification, review state, and memory eligibility are separate decisions. Moving a note into a completed-review location does not silently promote it into the agent's prompt.

## The First Useful Boundary Was Deliberately Coarse

I did not begin by building a general policy engine. The practical first step was a pair of memory banks: one general and one private. A trusted context registry selects which bank a conversation may write and which banks it may read. An unknown context can read only the general bank and cannot write memory. A recognized general context stays in the general bank, while a recognized private context can combine private and general results.

That arrangement is intentionally conservative. The current router resolves a small set of trusted communication contexts, chooses a write bank, and tags results with their bank when it combines recall. Recorded canaries established the boundary I cared about first: general retrieval could not see private canaries, while a trusted private context could use both general and private material. The two databases also passed the recorded integrity and vector checks after rebuild work.

There is real value in a coarse control that I can understand and test. It gave me a safer interim system before attempting fine-grained authorization inside every retrieval path. It also gave me a clear failure mode: if a context is missing or ambiguous, protected writes are denied instead of being guessed from whatever conversation title happens to be visible.

The [Hands-On companion]({{ page.series_companion_url | relative_url }}#start-with-three-bounded-outcomes) reduces that boundary to three context outcomes and two invented memory banks. It is small enough to run, inspect, and deliberately try to break without copying my private configuration.

The diagram below shows that interim arrangement in its proper place. The banks are projections of reviewed authority, not authority themselves. Its solid path is the current coarse bank selection; the dashed branch is the proposed per-memory policy prefilter. Both put their authorization decision before ranking and prompt construction, but only the bank router is deployed today.

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-03-memory-governance.svg"
   alt="Memory governance flow separating durable retention from retrieval eligibility, then showing current general and private bank routing, a proposed per-memory authorization prefilter, and purge-and-rebuild handling for corrections, restrictions, and deletion."
   variant="series" %}

## A Bank Is Not a Complete Security Model

The limit became apparent almost immediately. “General” and “private” are useful boundaries, but real work rarely fits one Boolean. Public material may be safe to reuse anywhere. Confidential project material may be appropriate for one team and not another. Restricted internal analysis may concern the same project as a client-visible document while having a completely different audience. Personal material may need an owner restriction in addition to a sensitivity label.

Creating another database for every combination does not solve that problem gracefully. It moves the policy into bank names and routing code, then makes lifecycle work harder when a person's role, a project's participants, or a document's audience changes. Banks remain valuable for hard separation, such as different tenants, encryption keys, residency requirements, or a boundary that must not share storage. Routine authorization still needs more information attached to each memory.

The draft policy model I am working toward separates several questions that are easy to collapse:

| Policy input | Question it answers |
| --- | --- |
| Classification | How sensitive is this memory? |
| Compartments | Which projects, matters, teams, or other need-to-know domains are required? |
| Audience | Is this owner-only, internal, client-visible, or intended for another defined group? |
| Purpose | Is this operation allowed for the current use, rather than merely relevant to it? |
| Context | Which authenticated participants and stable work scope are involved now? |
| Epoch and policy version | Has participation or authorization changed since a prior decision was cached? |

None of those can be inferred safely from semantic similarity. A conversation title can help an operator locate a rule, but it is mutable and non-unique, so it cannot be the long-term authorization key. Runtime session IDs are not enough either because one durable work context may span several sessions and channels. The adapter needs to resolve authenticated platform claims into a stable access context that identifies the participants, work scope, classification ceiling, compartments, audience, purpose, and current policy version.

## Use the Lowest Common Denominator

Multi-participant conversations make the policy less intuitive. If two participants have different access, the conversation does not inherit the union of everything either person can see. It must use the least-authorized combination. The effective classification ceiling can be no higher than the least-authorized participant and the configured context ceiling. Required compartments must be available to the context and every applicable participant. Audience and purpose rules still have to pass.

In compact form, the decision looks more like an intersection than a similarity score:

```text
eligible(memory, context) =
    classification(memory) <= ceiling(context)
    AND required_compartments(memory) subset_of compartments(context)
    AND audience_allows(memory, context)
    AND purpose_allows(memory, context)
    AND context_is_authenticated_and_current(context)
```

| Example | Classification fits? | Compartment and audience fit? | Retrieval decision |
| --- | ---: | ---: | --- |
| Public reference in a general technical discussion | Yes | Yes | Eligible |
| Confidential Project A note in a public discussion | No | Irrelevant after denial | Excluded |
| Confidential Project A note in a Project B discussion | Yes | No | Excluded |
| Internal Project A analysis in a client-visible Project A discussion | Yes | No | Excluded |
| Material with missing or invalid policy metadata | Unknown | Unknown | Pending and excluded |

This is also why authorization has to happen before search. If the engine performs a broad vector query and filters the results afterward, unauthorized content has already entered application memory and may already have been ranked, logged, cached, summarized, or exposed through a debugging tool. A secure implementation generates candidates only from the authorized set, then applies vector or lexical ranking. The model should never receive content that the policy layer intends to remove later.

The companion makes that ordering executable with a [recording-scorer canary]({{ page.series_companion_url | relative_url }}#prove-what-the-demonstration-claims). It checks what the scorer was allowed to see, not merely what survived into the final JSON.

The same rule must cover more than the obvious `recall()` call. Full-text search, graph queries, facts, consolidation, exports, synchronization, shared-memory tools, caches, and administrative inspection can all become alternate retrieval paths. Protecting the prompt while leaving one of those paths broad is not governance; it is a bypass.

## Promotion and Deletion Need History

The current review workflow fails closed on missing or invalid document metadata. Unclassified material remains pending and excluded. Reviewed material still needs an explicit eligibility choice before the memory projection includes it. That extra decision may look inconvenient, but it prevents a filing action from silently becoming permission to expose content in future conversations.

Promotion, reclassification, and deletion also need append-only history: who authorized the change, what policy applied, why it changed, and when the new decision became effective. A derived memory made from several sources inherits the strictest applicable restrictions unless an authorized workflow explicitly changes them. A convenient summary cannot become less restricted merely because the model left out the sentence that made the source sensitive.

Deletion is where these rules become concrete. Earlier remediation work exposed the practical danger of incomplete cascades: facts, vectors, links, annotations, or fallback rows can survive after their apparent source is forgotten. Current upstream releases have repaired several deletion paths, and the memory engine has useful targeted deletion and reindexing tools, but an upstream capability is not proof that every local derivative and integration path is covered. My acceptance test has to begin with the source graph and end by checking every representation the deployment actually uses.

For the smaller teaching boundary, the [rebuild-removal test]({{ page.series_companion_url | relative_url }}#prove-what-the-demonstration-claims) demonstrates the same principle by replacing disposable derived state and proving that removed authority is no longer searchable.

## Where I Want the Design to Go

The longer-term specification keeps banks for hard isolation but moves ordinary classification and need-to-know policy into indexed fields on each memory and derived chunk. The context policy would be compiled once for the current participant set and policy version, then applied as a secure prefilter before similarity or full-text ranking. Policy changes would invalidate affected caches, and audit records would explain allow and deny decisions without copying memory content into the audit trail.

That design is still proposed. It has not been submitted upstream, and I have not measured its performance or demonstrated zero leakage across every retrieval surface. The migration cannot be a one-way conversion performed on the working databases. It needs side-by-side stores, preserved provenance, duplicate reconciliation that keeps the stricter policy, canaries for every classification and compartment boundary, integrity checks, and a rollback path. The original banks remain available until authorization, recall quality, lifecycle behavior, and rollback all pass.

I am also deliberately avoiding legal or regulatory claims. A memory engine can provide classification, access controls, audit evidence, provenance, and fail-closed behavior. It cannot decide for an organization whether a document is privileged, whether a particular rule applies, or whether the surrounding operation is compliant. Those decisions belong to the responsible people and the policies they are authorized to set.

## Current State

At the source snapshot used for this article, LLM-Wiki inside Obsidian's Main Vault is the review-first durable authority, with explicit document classification and retrieval eligibility. The private environment also has an interim general/private Mnemosyne routing layer driven by trusted context mappings. Unknown contexts fail closed for writes, general retrieval is isolated from private memory, and trusted private retrieval can combine bank-tagged general and private results. Project records contain isolation canaries, idempotence checks, bank integrity checks, and successful rebuild evidence.

The richer per-memory model is a draft specification covering classification ceilings, compartments, audiences, purposes, context epochs, secure query prefilters, policy-aware caches, and decision audit. It is neither deployed nor publicly released, and no benchmark or compliance claim is being made for it.

## Next Work

The next engineering step is to map the policy requirements to every Mnemosyne storage and retrieval surface, then build the smallest indexed prefilter prototype that can fail closed before candidate ranking. That prototype needs cross-context leakage canaries, provenance and deletion tests, cache-invalidation tests, and measurements against the same workload without policy. Only after those results exist does it make sense to plan a reversible migration from coarse banks or prepare an upstream proposal.

For the blog series, the next installment steps back from one implementation and compares the wider memory and optimization tool landscape. The useful question is not which product advertises the largest saving; it is which combination improves a common workload without adding more disruption, privacy exposure, or operational cost than it removes.
