---
short_url: "https://unixwzrd.ai/s/9807a49a51/"
layout: post
title: "Hands-On: Build an Idempotent Intake Manifest"
date: 2026-08-21 08:00:00 -0500
categories: [hands-on]
tags: [ai, agent-optimization, agent-workflows, python, sqlite, deterministic-systems, local-first, knowledge-management]
image: /assets/images/blog/agent-optimization/post-02a-idempotent-manifest-hero.png
excerpt: "A first import is easy. I built and tested a bounded Python and SQLite manifest that keeps source identity and history intact across reruns, changes, disappearance, and restoration."
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

While writing [Deterministic First: Building a Knowledge Intake Pipeline](/technology/2026/08/19/deterministic-first-building-a-knowledge-intake-pipeline/), I kept coming back to the same problem: a successful first import does not prove very much. Plenty of scripts can create a row once. I wanted to know what happened when I ran the script again, changed a file, removed it, and then put it back. If the inventory could not explain each of those events without producing duplicates or pretending stale data was still current, I was not ready to build anything else on top of it.

That led me to a small standard-library Python utility backed by SQLite. It scans one deliberately bounded directory tree, records deterministic source identities, preserves the history of missing files, migrates the earlier teaching schema, and reports what it did as JSON. I stopped it there on purpose. It does not summarize a document, classify it, approve it, or decide whether an agent may retrieve it. I want those later decisions to remain visible instead of disappearing inside an importer that tries to do everything.

<!--more-->

## Start With the Contract

I started with one row for every allowlisted Markdown or text file. There is nothing particularly glamorous in the record, but every field answers a question I know I will have to ask later:

| Field | What it tells me |
| --- | --- |
| `source_id` | A stable identity derived from source type and canonical path |
| `source_path` | Where the source authority was observed |
| `content_sha256` | Whether the bytes actually changed |
| `size_bytes`, `mtime_ns` | Observed metadata, refreshed even when content is unchanged |
| `extractor_version` | Which inventory contract evaluated the source |
| `processing_state` | Whether downstream processing must reconsider it |
| `availability_state` | Whether the source is currently `present` or retained as `missing` |
| `discovered_at` | When the manifest first observed the source |
| `content_changed_at` | When its content or extractor contract last changed |
| `updated_at`, `last_seen_at` | When manifest state changed and when a completed scan last saw it |

I tied identity to the source type and canonical path because those are the facts this little utility can actually prove. If I rename a file, the old path becomes missing and the new path becomes a new source. That may be less clever than guessing that the two files are the same thing, but it is also auditable. In a larger system I would record a known move explicitly or use a stronger identifier supplied by the source system.

Once I wrote those rules down, the control flow became almost boring, which is exactly what I wanted. One transaction selects eligible files beneath the configured root, fingerprints each stable read, compares it with the previous state, reconciles missing records within that same root, checks SQLite integrity, and only then commits.

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-02a-manifest-scan.svg"
   alt="Manifest scan flow from a bounded source root through allowlisted selection, stable fingerprinting, prior-record comparison, missing-source reconciliation, integrity checking, commit or rollback, and JSON output."
   variant="series" %}

I did not want the convenience of a recursive scan to turn into accidental access to an entire home directory. Hidden paths, non-text suffixes, and file or directory symlinks that could escape the root are excluded. The utility also stats each selected file before and after hashing it. If the file changes during the read, the scan fails and rolls back instead of committing a fingerprint assembled from two different versions.

## Read or Download the Complete Files

I am including both complete files because sample code is much more useful when the reader can run the same checks I ran. The on-page source viewer and download links use the same public assets, so there is no second hand-maintained copy waiting to drift away from the article. The first disclosure contains the utility, and the second contains its eight-canary acceptance suite.

{% include source_code.html source="/assets/code/agent-optimization/intake_manifest.py" language="python" title="intake_manifest.py" %}

{% include source_code.html source="/assets/code/agent-optimization/test_intake_manifest.py" language="python" title="test_intake_manifest.py" %}

## Run a Clean End-to-End Scan

I use a disposable tree under `/tmp` so I can repeat the exercise from a known starting point. Download both files into it and create one small Markdown source:

```bash
rm -rf /tmp/intake-demo
mkdir -p /tmp/intake-demo/sources

curl -fsSLo /tmp/intake-demo/intake_manifest.py \
  https://unixwzrd.ai/assets/code/agent-optimization/intake_manifest.py
curl -fsSLo /tmp/intake-demo/test_intake_manifest.py \
  https://unixwzrd.ai/assets/code/agent-optimization/test_intake_manifest.py

printf '%s\n' '# First note' 'A source with enough text to fingerprint.' \
  > /tmp/intake-demo/sources/first.md

python3 /tmp/intake-demo/intake_manifest.py \
  /tmp/intake-demo/sources \
  --db /tmp/intake-demo/manifest.db
```

The first result is not exciting, and that is good:

```json
{
  "changed": 0,
  "extractor_version": "intake-manifest-v2",
  "missing": 0,
  "new": 1,
  "restored": 0,
  "schema_version": 2,
  "unchanged": 0
}
```

When I run the same command again, it reports `new: 0` and `unchanged: 1`. The program still reads and hashes the file, so I am not claiming that modification time provides a shortcut around the scan. What I am claiming is narrower and easier to verify: an ordinary rerun does not invent another identity or reset work unnecessarily.

Now change the source and ask for the ordered record set:

```bash
printf '%s\n' 'A second paragraph changes the content fingerprint.' \
  >> /tmp/intake-demo/sources/first.md

python3 /tmp/intake-demo/intake_manifest.py \
  /tmp/intake-demo/sources \
  --db /tmp/intake-demo/manifest.db \
  --records
```

This time the summary reports `changed: 1`, but the `records` array still contains one row with the same `source_id`. Its `content_sha256` changes and its `processing_state` returns to `"discovered"`, which is the behavior I need before handing the source to another stage. Changing the extractor version causes the same reprocessing decision even when the file itself is unchanged; I do not want a new inventory contract masquerading as the old one.

## Preserve Disappearance and Restoration

This is where the original small example was not good enough. If a file disappeared, its old row simply survived and still looked current. Deleting the row would have hidden the opposite fact: the source had existed, and something had happened to it. The useful behavior is to retain the record while changing its availability. Move the example outside the source root and scan again:

```bash
mv /tmp/intake-demo/sources/first.md /tmp/intake-demo/first.saved

python3 /tmp/intake-demo/intake_manifest.py \
  /tmp/intake-demo/sources \
  --db /tmp/intake-demo/manifest.db \
  --records
```

The result reports `missing: 1`, and the retained row now has `availability_state: "missing"`. Nothing is silently erased and nothing stale is presented as current. Put the same file back and scan once more:

```bash
mv /tmp/intake-demo/first.saved /tmp/intake-demo/sources/first.md

python3 /tmp/intake-demo/intake_manifest.py \
  /tmp/intake-demo/sources \
  --db /tmp/intake-demo/manifest.db \
  --records
```

Now the result reports `restored: 1`. The record keeps its original identity and `content_changed_at` value because availability changed but the bytes did not. I still return its processing state to `discovered`; a downstream stage should make an explicit decision about the restored authority rather than assuming nothing important happened.

{% include blog_diagram.html
   src="/assets/images/blog/agent-optimization/post-02a-source-lifecycle.svg"
   alt="Per-source manifest lifecycle showing first discovery, unchanged and changed scans, retained missing history, and restoration without changing source identity."
   variant="series" %}

## Inspect the SQLite State

The `--records` option is convenient for scripts, but one reason I chose SQLite is that I can inspect the durable state without standing up another service:

```bash
sqlite3 -header -column /tmp/intake-demo/manifest.db \
  'SELECT source_id, availability_state, processing_state,
          size_bytes, extractor_version
     FROM sources
    ORDER BY source_path;'
```

The manifest stores canonical paths because it is local provenance state. I would not copy those paths into a public report or diagnostic bundle, and I have not used paths from my own environment in this article. If paths are sensitive in your environment, protect the database or introduce an opaque locator at the system boundary.

## Run the Canary Suite

I also do not want the reader to trust this utility simply because the example output looks reasonable. The earlier version left too much correctness as an exercise, so this version includes the acceptance tests I use to check the boundary:

```bash
cd /tmp/intake-demo
python3 -m unittest -v test_intake_manifest.py
```

The eight canaries cover the failure modes I care about at this boundary:

| Canary | Evidence it demands |
| --- | --- |
| New, unchanged, and changed | Three scans retain one stable source row |
| Missing and restored | Disappearance retains history and restoration retains identity |
| Bounded selection | Hidden, non-text, and symlinked sources remain excluded |
| Extractor upgrade | A contract-version change resets processing to `discovered` |
| Root-scoped reconciliation | Scanning one configured tree cannot mark another tree's records missing |
| Metadata refresh | Unchanged content still refreshes observed metadata |
| Transaction rollback | A failed fingerprint leaves no partial source updates |
| Schema migration | The original teaching schema upgrades without losing its row or state |

The ordering matters here. The integrity check runs before commit, so a source-read failure or failed `PRAGMA quick_check` rolls back the source changes from that invocation. Schema migration commits separately, which allows an older manifest to be upgraded even when a later source scan fails.

## Hand Off to Review Without Granting Retrieval

This is the point where it is tempting to keep adding features, and it is also where I stop. A downstream extractor can select rows in `processing_state = "discovered"`, but its output should still enter review in a fail-closed state:

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

After a person accepts the material for durable filing, retrieval eligibility remains a separate decision:

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

The important line is still `mnemosyne: "exclude"`. Filing something after review does not silently authorize an agent to retrieve it or inject it into a prompt. I retain rejected candidates too, with `review_state: "rejected"`, `mnemosyne: "exclude"`, and a decision timestamp, so the next extraction pass does not present the same material as new work.

## Current State

I am comfortable calling this utility complete for its stated job. It maintains an inspectable, transactional inventory of allowlisted local text sources and reports their lifecycle across reruns. Its JSON and SQLite contracts are suitable inputs for a separate extractor, and the included tests make that claim reproducible rather than anecdotal.

It still does not snapshot application databases, parse live session formats, classify content, remove secrets, review candidates, or populate a memory engine. Those jobs need source-specific adapters and policy decisions. Leaving them outside this program is not unfinished homework. It is how I keep one small component understandable enough to trust.

## Next Work

From here I can move into memory governance without pretending the inventory solved it: who may retrieve which durable material, where authorization has to happen, and why access control must narrow the candidate set before ranking begins. The next main installment tells that part of the story, and its own Hands-On companion will turn the ordering into a small fail-closed router with canary tests.
