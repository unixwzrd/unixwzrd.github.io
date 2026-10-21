---
layout: review
title: "RFC Draft: Optional Policy-Aware Memory And External Source Integrity"
permalink: /hidden/review-2d66666c7be62e65c7daf868/rfc/
unlisted: true
search_exclude: true
sitemap: false
list_exclude: true
short_link: false
review_index: /hidden/review-2d66666c7be62e65c7daf868/
review_date: "2026-10-21"
review_note: "Peer-review snapshot. Links between the five included documents are retained; internal supporting references outside the packet are omitted. Example identifiers are generalized where needed. Each document retains its own design and qualification status."
---

# RFC Draft: Optional Policy-Aware Memory And External Source Integrity

**Status:** Local discussion draft. Not submitted, accepted or released. No upstream RFC number assigned.

**Proposer:** unixwzrd

**Related:** [RFC 0002, modality providers](https://github.com/mnemosyne-oss/mnemosyne/blob/main/docs/rfc/0002-modality-providers.md), [RFC 0003, media moments](https://github.com/mnemosyne-oss/mnemosyne/blob/main/docs/rfc/0003-media-moments.md), [RFC 0004, archive boundary](https://github.com/mnemosyne-oss/mnemosyne/blob/main/docs/rfc/0004-archive-boundary.md). Verify upstream paths and related issue overlap before submission. Existing issues #828, #1132 and #1208 are adjacent work to reconcile, not assumed duplicates or approvals.

## Summary

We want to extend Mnemosyne's existing banks, ownership controls, source references and native retrieval paths, not introduce another memory engine or a document archive. Two independently useful changes are proposed: exact, externally stored source evidence with bounded indexing; and optional record-level policy enforcement for deployments that need more than bank separation. Neither should require a cloud service, a new gateway, a particular classification scheme or changes to an unconfigured installation.

The distinction matters. A bank says which store a request may reach. Policy says which records that conversation may use, for which purpose and destination. An agent may have broader privileges in a different conversation; those privileges must not enter a shared conversation's candidates, ranking, tool results or model context. Filtering the final answer is too late.

We are requesting architectural direction before proposing a public API or migration contract as final. Downstream prototypes and synthetic qualification exist to make the discussion concrete. They do not establish protected-mode readiness or ask maintainers to accept an entire stacked branch.

## 1. Fit With Existing Architecture

| Existing mechanism | Proposed extension | Not proposed |
| --- | --- | --- |
| Named banks and separate SQLite databases | Preserve bank routing; add indexed record eligibility within an explicitly prepared domain | Collapse private/shared banks or infer permission from a bank name |
| Ownership/provider identity and agent adapters | Bind authenticated participants, bank, purpose and actual destination to a fresh request context | Trust model arguments, chat titles or session labels as authority |
| BEAM, native vector/FTS, direct records and graph | Admit authorized candidates before content/vector consumption and ranking | Retrieve a privileged pool and filter it afterward |
| Media assets, moments and ContentResolver | Bind exact byte/extraction revisions and verify explicitly requested expansion | Archive full documents or fetch sources during ordinary recall |
| Lifecycle plugins | Declare supported protected behavior and authorize their inputs/destinations | Treat optional notification hooks or swallowed plugin exceptions as an enforcement boundary |

Trusted in-process plugins and code owning the SQLite connection are not sandboxed by this proposal. A deployment must not claim protected operation while unsupported adapters, plugins, ordinary entry points or maintenance paths can bypass it.

## 2. External Source Integrity

Original documents, images and other heavy files remain in an archive, filesystem or other source service. Mnemosyne retains opaque source/revision/span identities, verification metadata, bounded excerpts, associations and derived indexes. Existing asset IDs and references remain readable; corrected extractions create explicit lineage rather than silently replacing the evidence behind an old citation.

A logical source can have multiple physical occurrences. Relocation does not change the expected byte revision. Explicit expansion reauthorizes, opens once, hashes the actual returned bytes and compares them with the expected revision. A HEAD response, ETag or old verification record is not proof of current bytes. Missing, changed, offline, unsupported and over-budget results remain distinguishable without silently serving another version. Ordinary recall does no source I/O.

Indexing needs explicit aggregate retention limits across aliases, revisions and retries, not just a per-chunk cap. Full-source lexical search cannot be implemented by hiding the original in FTS content or a sidecar. If a backend cannot provide a promised coverage mode within the agreed retention contract, it must report that limitation. The downstream candidate uses conservative bounded excerpts; these are proposed defaults, not upstream-approved recall-quality optima.

Updates should be idempotent and resumable. A failed import preserves the previous usable generation. Embedding reuse binds exact excerpt bytes, source/sharing domain, model/artifact identity, dimensions and preprocessing. It must not reuse private vectors across permission domains merely because text hashes match. A persisted completion flag without the required artifacts and lineage is not a usable index.

## 3. Optional Access Context And Policy

Unconfigured legacy mode keeps its current behavior. Preparing metadata is not activation. Protected mode, when eventually exposed, must be explicit, persistent and impossible to disable merely by omitting configuration or selecting an older ordinary client.

A trusted host derives the effective context from all applicable participants. It contains a deployment-defined policy/version, classification ceiling, required compartments, audiences, purpose, allowed banks/projects, destination and current identity/epoch information. The intersection of participant permissions is the ceiling; the agent's independent privileges do not widen it. Unknown participants, incomplete mappings, stale authority and unsupported paths refuse.

The engine must authorize candidate generation and subsequent use across direct lookup, vector, FTS, graph, reranking, evidence expansion and model/tool/provider delivery. Project membership records relevance, not permission. Denied records must not consume a result budget or reach a scorer. Diagnostics, logs and why-not-recalled tools need their own disclosure contract; counts, names or error messages can reveal a record without returning its body.

The policy vocabulary belongs to the deployment. No government classification labels, mandatory policy server or external identity service is required. For deployments defining `unclassified`, an absent classification with no stricter inheritance may normalize to that exact label with a recorded defaulted origin. This grants no audience, owner or purpose access. Invalid explicit labels do not default, and stricter inherited restrictions remain effective. Previewable migration and unresolved legacy metadata need a separate accepted contract; this RFC does not authorize automatic backfill.

## 4. Derivatives And Revocation

Derived memories take the highest source classification, the union of required compartments/overlays, and the intersection of allowed audiences/purposes. Empty intersections remain denied. Current single-owner/single-tenant metadata cannot safely represent every multi-owner combination; an unsupported combination must refuse rather than choose an owner or drop a tenant requirement.

Lineage must be durable and traversable. Creating a derivative's binding and exact supporting edges should be atomic. Correction, deletion or revocation quarantines affected descendants before they are eligible for retrieval, even while regeneration is pending. No implicit unquarantine or declassification is proposed. Independently authorized replacement evidence is required to regenerate a usable derivative.

The downstream lifecycle candidate adds indexed quarantine and a monotonic store epoch to the optional prepared catalog. Trusted grants bind that epoch, and explicit reads recheck authority before candidate consumption and release. A caller's old SQLite snapshot is not a source of fresh authority. The host must obtain current epoch state independently. These are cooperative checkpoints, not a claim that blocked I/O can be interrupted or that data already emitted can be retracted.

Cache entries, evidence handles, queued provider calls, streams, exports, synchronization and maintenance must obey the same lineage/epoch restrictions. They are not qualified simply because direct recall is. An earlier metadata-only prototype marker made older explicit policy readers refuse but could not block ordinary legacy SQLite clients. The later operator-approved downstream design qualifies an opt-in encrypted snapshot representation and separate current-artifact authority; an actual unchanged old native client refuses the encrypted artifact. This is evidence for the design discussion, not a decision that upstream must use this storage mechanism or a production activation claim.

The bounded owner implementation publishes immutable encrypted bytes before advancing a separately pinned persisted authority using exact-predecessor compare-and-swap. Missing/damaged current files never select an older generation. Old-memory restoration cannot restore that independent authority; uncertain COMMIT outcomes are inspected using durable operation receipts. Co-restoring both authority and memory is not detectable by markers inside those backups: a surviving trusted freshness anchor is required, or access must refuse. Host identity/grant authority likewise has to remain independently current after restore; a self-consistent old host snapshot is not fresh merely because its internal epochs agree.

This candidate uses the existing optional cryptography dependency, whole-buffer owner snapshots and explicit 64 MiB database/90 MiB envelope admission limits, not an encrypted VFS or an arbitrary-scale replacement engine. Plaintext lives only in trusted owner RAM during protected opening; raw key/connection owners are not sandboxed. Larger stores, key lifecycle, real filesystem recovery and supported adapter wiring require their own accepted design/qualification. No existing store is automatically converted or given new permissions.

The downstream prototype now includes payload-free evidence leases with explicit fresh scope/epoch checks and exact native reload before reuse. These are discussion evidence for a cooperative integration boundary, not automatic interception of external caches or provider streams. Resolving a lease cannot retract plaintext already copied elsewhere or replace the final authorization gate in a delivery adapter.

## 5. Interfaces And Contribution Boundaries

The downstream prototype separates contracts (`AccessContext`, policy definitions and capability declarations), prepared indexed metadata, explicit readers/writers, source verification/expansion, bounded indexing and lifecycle operations. These names are discussion material, not a request to freeze the current public API.

The reference protected host bridge consumes one fresh atomic authenticated roster/grant snapshot and computes all-participant intersections explicitly. Classification ceilings take the lowest grant; owner/tenant, compartment/audience, purpose, bank/project, operation and destination permissions cannot be widened by an agent's broader independent scope. Bank-wide permission must be explicit for every participant, not inferred from an empty project selection. Snapshot/global host epochs must be authoritative, not copied from chat labels or cached model claims. A fixed read/evidence dispatcher rejects scope/callback overrides and unsupported operations without calling legacy handlers. This is an optional host contract, not a new identity provider or proof that a deployed CLI/MCP/Hermes frontend implements it.

Compact evidence delivery reuses authorized leases and existing supplemental-pack grouping. It preserves verbatim bounded prefixes and exact reference metadata, counts the complete serialized output with an explicitly pinned trusted local tokenizer, reports omissions and reauthorizes after all packing/tokenizer work. Native connection/data/schema/total-change fences reject observed live updates across each whole lease batch; they do not make a later external callback atomic. No original source fetch, generated summary or deployed-model quality claim is implied by synthetic budget tests.

Source-integrity work can be useful without policy adoption. Policy core work should not require the entire importer stack. Adapter integration follows core enforcement, and protected activation follows cross-path acceptance rather than leading it. A supported-path declaration is not a certification. Unsupported protected operations must be visibly refused.

We propose separate logical contributions: qualification fixtures; source revisions and resolver integrity; bounded resumable indexing; policy contracts/storage; explicit native access; derivative lifecycle; adapter parity/activation; and compact evidence recall. Downstream corrective commits are folded into the contribution they repair. There is no requirement to merge a long dependent chain in one decision.

## 6. Validation And Cost

Use synthetic principals, sources, compartments and high-ranked denied canaries in disposable stores. Cover actual host/provider A/B/A dispatch, native float32/int8 and lexical paths, mixed participants, direct IDs, source expansion, graph, plugins, caches, maintenance, export/restore and provider delivery. Zero unauthorized intermediate disclosure is a release gate; an untested path is not a successful denial.

Each schema change needs upgrade, interruption, recovery and old-client refusal tests. Record exact source/artifact identities, interpreter/dependency versions, skipped or unsupported surfaces, installed-package checks and independent review. A unit test, selected suite or metadata-only helper does not establish deployed protected operation.

Compare each runtime change with the preceding accepted checkpoint under identical bounded workloads. Retain raw latency samples, p95, throughput, memory/index growth, embedding calls, injected tokens and authorized recall quality where applicable. A provisional 10% overhead target must be reviewed against the baseline; no formal budget or semantic-quality result is claimed here. Shared-host microsecond tail variation is reported, not attributed to an unchanged path or averaged away.

## 7. Decisions Requested

1. Are these boundaries consistent with the existing bank, ownership, media/resolver and layered-memory roadmap? Which existing issues should own the work?
2. Where should trusted context, current epochs and adapter capability checks live in the supported API?
3. What protected-store representation can make older ordinary clients refuse access, and how should revocation-safe restore work without a mandatory external service?
4. Which initial retrieval/maintenance/plugin surfaces should be supported, and which should explicitly refuse until qualified?
5. Are bounded retained content and explicit unsupported full-source search acceptable, and where should the retention/coverage contract be defined?
6. How should versioning, schema numbering and changelog entries be assigned to independently mergeable contributions? Downstream prototype versions are not proposed upstream release identities.

## 8. Non-Goals And Publication State

No full-document archive, automatic profile promotion, replacement task canvas, mandatory REST gateway, cloud service, new container framework or live bank migration is included. Existing originals, banks, private histories, embedding identities and service configuration remain unchanged.

This is an unsubmitted local RFC draft. Upstream's contributor guide requires early discussion and architectural decisions for storage/API changes. The operator's CLA clarification inquiry [#1214](https://github.com/mnemosyne-oss/mnemosyne/issues/1214) remains a separate administrative discussion; its lack of a reply is not acceptance. Technical issue/RFC/PR submission and CLA agreement require the operator's explicit decision. The administrative note here is removed or updated in the final submitted version once that gate is resolved.

## 9. Remaining Host Integration Decision

**October 21 decision:** The operator selected an optional host-local binding with explicit operator-managed grants. The [companion design](/hidden/review-2d66666c7be62e65c7daf868/host-authorization/) now resolves that direction without adding a mandatory service or changing runtime behavior. The questions below become its implementation/qualification obligations, not a renewed request to choose between a local and existing external authority. Exact schema/backend and actual frontend hooks remain proposed; approval to design is not protected activation or deployment.

The operator-approved storage/restore design is implemented and locally qualified through final core/SDK candidate `2d1502b`, together with the explicit complete-participant reference host. That closes the missing ordinary-SQLite downgrade boundary for the encrypted owner artifact; it does not make every existing endpoint protected. Independently current authority must survive memory restoration. Co-restoring both authority and memory cannot establish freshness without a surviving trusted anchor; missing freshness must refuse.

Bounded source tracing of the actual CLI, MCP and Hermes entrypoints found authentication/attribution in applicable modes and useful routing fields, but no complete current participant-permission snapshot matching the new host contract. Exact sources, pins and unknowns are recorded in the source-interface inventory (internal supporting reference; not included in this packet). Additional uninspected authority services or wrappers may exist; the report does not establish their absence. An author ID, token name, session label, chat title or bank selector is not a complete audience or memory grant.

Before implementing real protected frontend activation, agree on these boundaries:

1. Which existing host authority supplies the complete applicable conversation audience and current per-principal grants as one authenticated atomic snapshot? Include participants who can receive the model output, not just message authors. Unknown or unsupported audience discovery must refuse, not become single-user access.
2. Which provider/adapter and output hooks carry the opaque authenticated request and actual destination through recall, tool execution, prompt/provider submission and delivery? Define cancellation on membership/grant/route changes, including queued and streaming output. The reference library's callback is not automatically those hooks.
3. Which independent host epoch/restore anchor survives the chosen backup and recovery domain, and who owns key/current-generation recovery? Cached grants or an old restored authorization database cannot authorize themselves.
4. Which initial endpoint operations are supported and which are explicitly blocked, including writes, derivatives, graph, maintenance, persona, export/sync and administrative operations? Qualify the exact enabled interfaces with denied canaries before exposing activation.

This is a consequential integration decision rather than a new regression in the qualified core. No mandatory identity service, permissive fallback, foreign Hermes protocol change or default activation is chosen implicitly. A conforming application can use the tested Python host/SDK today with its own explicit trusted authority; legacy behavior remains unchanged. Real frontend activation, migration and deployment remain open, alongside timing confidentiality, deployed-tokenizer/semantic quality and scale acceptance. Upstream technical publication remains held pending the separate CLA decision.
