---
short_link_basis: "/_posts/2026-08-25-hands-on-build-a-fail-closed-memory-router.md"
short_url: "https://unixwzrd.ai/s/dde867f837/"
layout: post
title: "Hands-On: Build a Fail-Closed Memory Router"
date: 2026-08-23 08:00:00 -0500
categories: [hands-on]
tags: [ai, agent-operations, ai-agents, python, memory, security, local-first, privacy, retrieval]
image: /assets/images/blog/agent-optimization/post-03a-fail-closed-memory-router-hero.png
excerpt: "Authorization has to choose the candidate set before relevance ranking begins. This runnable Python router and its seven canaries make that ordering visible and testable."
series: "Local First AI and Agent Operations"
series_part: "3A"
series_order: 35
series_total: 14
series_url: /blog/series/local-first-ai-and-agent-operations/
series_companion_of: 3
series_previous_title: "Memory Is a Governance Problem, Not Just a Vector Database"
series_previous_url: /technology/2026/08/23/memory-is-a-governance-problem-not-just-a-vector-database/
series_next_title: "The Agent Memory and Optimization Tool Landscape"
series_next_url: /technology/2026/08/25/the-agent-memory-and-optimization-tool-landscape/
series_next_date: 2026-08-25 10:00:00 -0500
redirect_from:
  - /hands-on/2026/08/25/hands-on-build-a-fail-closed-memory-router/
published: true
---

While writing [Memory Is a Governance Problem, Not Just a Vector Database]({{ page.series_previous_url | relative_url }}), I kept returning to one failure that is easy to hide inside an otherwise impressive retrieval demo. A vector search can return a highly relevant memory from the wrong context. If the application filters that result after ranking, the user may never see it, but the protected content has already crossed the boundary: the scorer received it, and a logger, cache, trace, debugger, or later processing step may have received it too.

I wanted a small exercise that made the ordering visible in code. The result is a standard-library Python router with two disposable memory banks, a deliberately ordinary token-overlap scorer, and a canary suite built around one rule: authorization chooses the candidate set before relevance ranking begins.

The runnable utility and its test suite are included below as readable, downloadable source. They do not copy my private deployment, and they do not pretend that a two-bank router is a complete policy engine. They model the coarse boundary I use today closely enough to test its useful properties without exposing a real host, context identifier, conversation, path, or policy mapping.

Both banks sit downstream of the document authority. They receive already reviewed, retrieval-eligible projections from Main Vault and LLM-Wiki; this router does not decide whether raw notes or material still waiting for review may enter memory.

The lab has two files: `memory_router.py` contains the router and invented banks, while `test_memory_router.py` contains seven canaries. Both use the Python standard library, and every context, record, identifier, and policy in the exercise is fabricated.

<!--more-->

## Before You Start

You need Python 3 and `curl`. The walkthrough uses `/tmp/memory-router-demo` and does not connect to a model, vector database, Main Vault, LLM-Wiki, or a deployed memory service.

| Stage | What you will prove |
| --- | --- |
| Define the boundary | Three contexts resolve to explicit read and write outcomes |
| Run the same query twice | Permission changes the candidate set before relevance is calculated |
| Run the canaries | Unauthorized content never reaches the scorer |
| Exercise writes | Unknown contexts are denied while an explicit private context selects its bank |
| Read the implementation | Candidate construction, deduplication, scoring, and ranking stay in the required order |

## Step 1: Start with Three Bounded Outcomes

I began with the smallest context table that could fail closed. An unknown context can read general material but cannot write memory. A recognized general context stays in the general bank. A recognized private context can read general and private material while writing only to the private bank.

| Context | Read banks | Write bank |
| --- | --- | --- |
| Unknown | General | Denied |
| Recognized general | General | General |
| Recognized private | General and private | Private |

This is intentionally less ambitious than the policy model described in Post 3. It does not evaluate participants, classification ceilings, compartments, audiences, purposes, or policy epochs. Those controls belong in a richer authorization layer. The point of this exercise is to make one current engineering boundary small enough to read, run, and try to break.

The order matters more than the scorer:

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-03a-fail-closed-memory-router.svg"
   alt="Fail-closed memory routing flow in which a context policy selects authorized general or private banks before candidate construction, deduplication, scoring, and bank-tagged results."
   variant="series" %}

The scorer sits to the right of the authorization boundary. An unauthorized private record is not a low-ranked candidate, a discarded result, or a redacted object. It is never a candidate at all.

## Step 2: Get the Complete Lab

Both disclosures use the same public files as their download actions, so the source shown in the article cannot drift away from the runnable copy.

{% include source_code.html source="/assets/code/agent-optimization/memory_router.py" language="python" title="memory_router.py" %}

{% include source_code.html source="/assets/code/agent-optimization/test_memory_router.py" language="python" title="test_memory_router.py" %}

## Step 3: Run the Boundary in Both Directions

Create a disposable working directory and download both files:

```bash
mkdir -p /tmp/memory-router-demo
cd /tmp/memory-router-demo

curl -fsSLO https://unixwzrd.ai/assets/code/agent-optimization/memory_router.py
curl -fsSLO https://unixwzrd.ai/assets/code/agent-optimization/test_memory_router.py
```

Query the private canary through the unknown-context path:

```bash
python3 memory_router.py unknown "cedar lantern"
```

The command may return low-scoring general memories because this toy scorer reports the best eligible records even when their token overlap is weak. What it cannot return is `private-canary`. More importantly, the private record never reaches the scoring function.

Now run the same words through the invented trusted-private context:

```bash
python3 memory_router.py private-room "cedar lantern"
```

The private canary becomes eligible, and every result retains its source-bank tag. Combining two authorized projections should not erase provenance merely because their records appear in one ranked list. That bank tag is not a complete source graph, but it keeps the example honest about where each result came from.

This pair of commands is useful because it separates relevance from permission without changing the query. The words are identical. Only the resolved context changes, and that decision changes which records exist from the scorer’s point of view.

## Step 4: Run the Canary Suite

The example includes seven canaries rather than relying on two attractive command outputs. Run them from the same disposable directory:

```bash
python3 -m unittest -v test_memory_router.py
```

| Canary | Boundary it establishes |
| --- | --- |
| Unknown write refusal | A missing context cannot silently select a protected write destination |
| General/private isolation | A general query cannot retrieve the private canary |
| Unknown-context fallback | An unrecognized context reads only the general bank |
| Trusted merged recall | A private context receives tagged results from both permitted banks |
| Deterministic duplicate handling | When identical content exists in both projections, the private copy wins |
| Pre-ranking exclusion | Private content never reaches the scorer during a general query |
| Rebuild removal | Replacing disposable derived state removes material no longer present in authority |

The pre-ranking canary is the one I care about most. It supplies a recording scorer, performs a general-context recall, and then inspects everything the scorer was allowed to see. A design that searches both banks and removes private results afterward cannot pass that test, even if its final JSON looks perfect.

The rebuild test protects a different part of the contract. These banks are derived projections, not durable authority. When approved authority changes, replacing a bank from that authority must remove records that no longer belong there. A deletion that changes the source but leaves the old derived candidate searchable is not a completed deletion.

## Step 5: Exercise the Write Boundary

The command-line interface demonstrates recall, so use a short Python invocation to exercise the write decision directly:

```bash
python3 - <<'PY'
from memory_router import Memory, example_router

router = example_router()
candidate = Memory("lab-note", "An invented lab memory.", "lab-source")
print(router.remember("unknown", candidate))
print(router.remember("private-room", candidate))
PY
```

The first result should contain `"stored": False` and `"reason": "context_memory_write_denied"`. The second should contain `"stored": True` and `"bank": "private"`. The difference comes from an explicit context policy, not a title guess or a relevance score.

## Step 6: Read the Security Ordering in the Code

The `recall()` method resolves a context policy, validates its declared bank names, and constructs candidates only from the authorized set. Private records are considered before general records when both banks are permitted, so normalized duplicate content keeps the more restricted copy. Only then does the router call the scorer, sort the results, and apply the requested limit.

In simplified form, the path looks like this:

```python
policy = self.policy_for(context_key)
allowed = {str(bank) for bank in policy.get("read_banks", ["general"])}

bank_order = [bank for bank in ("private", "general") if bank in allowed]
candidates = [
    (bank, memory)
    for bank in bank_order
    for memory in self.banks[bank]
]

# Deduplicate eligible candidates, then score and rank them.
```

The example uses token overlap because it keeps the exercise portable and makes the security test easy to instrument. Replacing `token_score()` with vector similarity does not change the contract. The vector index, database predicate, or application query must still restrict the candidate population before distance calculation returns protected content to the ranking layer.

The write side follows the same fail-closed posture. `policy_for()` returns a default policy for an unknown context, and that policy selects no write bank. The router reports the refusal as an ordinary structured result rather than guessing a destination from a mutable title or silently dropping the request.

## Step 7: Compare the Coarse Router with a Fine-Grained Store

Two banks are useful for teaching and for coarse hard boundaries, but they do not express all of the decisions a real memory system may need. The future design in Post 3 attaches classification, compartments, audience, purpose, policy version, and stable access context to individual memories and their derivatives. A database capable of enforcing that policy might preserve an ordering like this:

```sql
SELECT id, content
FROM memories
WHERE classification_rank <= :context_ceiling
  AND required_compartments_are_available = TRUE
  AND audience_allowed = TRUE
  AND purpose_allowed = TRUE
ORDER BY vector_distance(embedding, :query_embedding)
LIMIT :limit;
```

That SQL is illustrative pseudocode. It is not the schema of the current router, a deployed Mnemosyne query, or a benchmarked implementation. Its purpose is to keep the authorization predicate visibly ahead of vector ranking.

A production design must also apply an equivalent boundary to full-text search, graph traversal, fact stores, consolidation, exports, caches, administrative tools, and every other path that can reveal memory. Protecting the primary `recall()` method while leaving a secondary inspection path broad only moves the disclosure.

## Before Adapting the Example

The small router earns exactly the claims covered by its canaries. Before I would let a similar design handle real material, I would expect the surrounding system to provide the following controls:

| Area | Additional control |
| --- | --- |
| Context authority | Authenticated platform claims mapped to stable access-context identifiers |
| Policy integrity | Schema validation and fail-closed handling for missing, stale, or invalid metadata |
| Hard isolation | Separate storage or cryptographic boundaries for tenant, residency, or key separation |
| Lifecycle | Transactional promotion, reclassification, deletion, and rebuild operations |
| Evidence | Append-only decisions that record policy and provenance without copying protected content into logs |
| Caching | Keys that include participants, purpose, authorization epoch, and policy version |
| Leakage testing | Canaries on every retrieval and administrative surface |
| Migration | Side-by-side rollout, integrity checks, preserved authority, and tested rollback |

This is also why I resist calling the example a security or compliance solution. It demonstrates a narrow control with executable evidence. The larger result still depends on authentication, policy administration, storage boundaries, lifecycle coverage, observability, and the behavior of every integration around it.

## What You Should Have at the End

You should now have two query results produced from identical words but different authorized candidate sets, seven passing canaries, and an explicit write refusal for the unknown context. Together those checks establish more than a final filtered result: protected content stayed outside the scorer in the first place.

When you are finished, remove only the disposable directory created for this lab:

```bash
rm -rf /tmp/memory-router-demo
```

## Current State

The companion currently contains a standard-library Python router, two invented disposable banks, three context outcomes, bank-tagged results, deterministic private-first duplicate handling, replacement of a bank from authority, and seven passing canary tests. The current private system uses a related coarse general/private routing boundary, but the names, identifiers, policies, records, and topology in this exercise are fabricated.

The richer per-memory policy model remains proposed. This exercise does not implement classification ceilings, compartments, participant intersections, audiences, purposes, policy-aware caches, or authorization across every Mnemosyne retrieval surface.

## Next Work

The next useful extension is not a more sophisticated scorer. It is a small indexed prefilter prototype with invented classification and compartment data, plus recording canaries that prove excluded content never reaches vector ranking, full-text search, caches, exports, or administrative inspection. Any migration from coarse banks should remain side by side and reversible until those boundaries, lifecycle operations, and rollback all pass.
