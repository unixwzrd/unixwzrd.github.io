---
short_url: "https://unixwzrd.ai/s/9807a49a51/"
layout: post
title: "Hands-On: Build an Idempotent Intake Manifest"
date: 2026-08-21 08:00:00 -0500
categories: [hands-on]
tags: [ai, agent-optimization, agent-workflows, python, sqlite, deterministic-systems, local-first, knowledge-management]
image: /assets/images/blog/agent-optimization/post-02a-idempotent-manifest-hero.png
excerpt: "A small Python and SQLite exercise for giving local sources stable identities, detecting real changes, and proving that ordinary reruns do not create duplicate records."
series: "Local-First Agent Operations"
series_part: "2A"
series_order: 25
series_total: 13
series_url: /blog/series/local-first-agent-operations/
series_companion_of: 2
series_previous_title: "Deterministic First: Building a Knowledge Intake Pipeline"
series_previous_url: /technology/2026/08/19/deterministic-first-building-a-knowledge-intake-pipeline/
series_next_title: "Memory Is a Governance Problem, Not Just a Vector Database"
published: true
---

While writing [Deterministic First: Building a Knowledge Intake Pipeline](/technology/2026/08/19/deterministic-first-building-a-knowledge-intake-pipeline/), I wanted a small example that showed the idea without dragging the entire private workflow along with it. The result is a local manifest that gives text sources stable identities, content fingerprints, provenance, and explicit change states. I deliberately stopped before document summaries, embeddings, review notes, and retrieval decisions because each belongs to a later lifecycle stage. The only promise this example needs to keep is that I can run discovery again without creating a second record for an unchanged source.

<!--more-->

## Start With a Small Contract

I kept the example to the Python standard library and SQLite so there is very little machinery to distract from the contract. The runnable `intake_manifest.py` file scans Markdown and text files below a directory while recording:

| Field | Purpose |
| --- | --- |
| `source_id` | Stable identity derived from the source kind and canonical path |
| `source_path` | Provenance needed to find the authority again |
| `content_sha256` | Content fingerprint used to detect a real change |
| `size_bytes` | Useful inspection metadata, not source identity |
| `mtime_ns` | Recorded provenance, not trusted as proof that content is unchanged |
| `extractor_version` | Version of the inventory contract that produced the record |
| `processing_state` | The next explicit lifecycle state |

The complete file is available here without sending it straight to the browser's download handler. Expand the disclosure to read it on the page; use the clearly labeled download button only when you want a local copy.

{% include source_code.html source="/assets/code/agent-optimization/intake_manifest.py" language="python" title="intake_manifest.py" %}

## Run the Example

Create a disposable source directory outside this repository:

```bash
mkdir -p /tmp/intake-demo/sources
printf '%s\n' '# First note' 'A source with enough text to fingerprint.' \
  > /tmp/intake-demo/sources/first.md

curl -fsSLO \
  https://unixwzrd.ai/assets/code/agent-optimization/intake_manifest.py

python3 intake_manifest.py \
  /tmp/intake-demo/sources \
  --db /tmp/intake-demo/manifest.db
```

The first run should report one new source. When I run the same command again, it reports one unchanged source. The file is still read and hashed, so this example makes no modification-time fast-path claim; it proves stable durable effects rather than zero-cost scanning.

Now change the source and run it a third time:

```bash
printf '%s\n' 'A second paragraph changes the content fingerprint.' \
  >> /tmp/intake-demo/sources/first.md

python3 intake_manifest.py \
  /tmp/intake-demo/sources \
  --db /tmp/intake-demo/manifest.db
```

The third run should report one changed source. It updates the existing manifest row and returns the processing state to `discovered` instead of inventing a second source identity. Changing the example's `VERSION` produces the same reprocessing outcome even when the content hash is unchanged, because I do not want a new inventory contract to masquerade as the old one.

## Inspect the Contract

I chose SQLite partly because it makes the state visible without requiring another service:

```bash
sqlite3 -header -column /tmp/intake-demo/manifest.db \
  'SELECT source_id, processing_state, size_bytes, extractor_version FROM sources;'
```

The manifest retains the full path for local provenance, but I would not copy that path into a public report. If paths are sensitive in your environment, use a protected locator or an opaque mapping and keep the manifest out of logs and public documentation.

## See the Review Boundary in Front Matter

The example script intentionally stops at inventory. The next boundary becomes much easier to understand once the state is sitting in the note instead of being described only in prose, so a newly extracted conversation enters a review-oriented Wiki location with front matter like this sanitized example:

```yaml
---
classification: "unclassified"
review_state: "pending"
mnemosyne: "exclude"
source_id: "src_example"
source_hash: "example-sha256"
classification_policy: "[[Wiki/Policies/Document Classification Policy]]"
related:
---
```

That is a fail-closed state. The note has provenance, but nobody has classified or approved it and no retrieval system should ingest it. After review, a note can be accepted for durable filing while remaining excluded from retrieval:

```yaml
---
classification: "public"
review_state: "approved"
mnemosyne: "exclude"
source_id: "src_example"
source_hash: "example-sha256"
classification_policy: "[[Wiki/Policies/Document Classification Policy]]"
related:
  - "[[Wiki/Concepts/Example Topic]]"
---
```

The important line is still `mnemosyne: "exclude"`. Approval and filing do not silently authorize retrieval. A rejected extract records a different durable decision:

```yaml
---
classification: "unclassified"
review_state: "rejected"
mnemosyne: "exclude"
source_id: "src_example"
source_hash: "example-sha256"
classification_policy: "[[Wiki/Policies/Document Classification Policy]]"
discarded_at: "YYYY-MM-DDTHH:MM:SSZ"
related:
---
```

The rejected note remains historical evidence that the source was considered. Keeping that state is what prevents the next extraction run from presenting the same candidate as new work. These examples show the intake mechanics only; the policy for deciding classifications and retrieval eligibility belongs to the next installment.

## Keep the Next Stage Separate

From here, a production pipeline could select rows in `processing_state = 'discovered'`, normalize them, and update that state transactionally. I would put candidate records in a separate table with their own stable identity, source reference, extraction version, review state, and content hash rather than turning `sources` into a bucket for summaries, embeddings, classifications, and retrieval flags. That separation is what lets me answer four different questions later:

1. What was the original authority?
2. What did deterministic extraction produce?
3. What did a person approve or reject?
4. What may a particular retrieval context use?

The same separation makes derived indexes disposable. If I change an embedding model or chunking strategy, I can rebuild the index from explicitly eligible durable content instead of treating old vectors as authority.

## Production Hardening Checklist

The example is intentionally small, and I would not point it at real agent data without hardening it first. At a minimum, I would:

- Open application databases read-only and use their supported snapshot behavior.
- Add schema migrations instead of modifying tables implicitly.
- Use transactions and an integrity check around manifest updates.
- Bound each run and expose counts for discovered, changed, unchanged, skipped, and failed sources.
- Define explicit source types and allowlists; do not recursively ingest an entire home directory.
- Exclude request dumps, tool payloads, credentials, caches, and generated indexes before extraction.
- Keep review candidates excluded from retrieval by default.
- Preserve rejection history so a discarded candidate does not reappear on the next run.
- Test identical reruns, content changes, extractor upgrades, filename collisions, malformed input, interruption, and recovery.

I wrote this as a teaching artifact, not a drop-in knowledge product. The useful part is not the amount of code; it is the boundary the code establishes. Inventory can be deterministic, inspectable, and boring before any model is invited to interpret the content.
