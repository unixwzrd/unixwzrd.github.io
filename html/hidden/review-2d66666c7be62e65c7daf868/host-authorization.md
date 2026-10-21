---
layout: review
title: "Mnemosyne Optional Host-Local Authorization Binding"
permalink: /hidden/review-2d66666c7be62e65c7daf868/host-authorization/
unlisted: true
search_exclude: true
sitemap: false
list_exclude: true
short_link: false
review_index: /hidden/review-2d66666c7be62e65c7daf868/
review_date: "2026-10-21"
review_note: "Peer-review snapshot. Links between the five included documents are retained; internal supporting references outside the packet are omitted. Example identifiers are generalized where needed. Each document retains its own design and qualification status."
---

# Mnemosyne Optional Host-Local Authorization Binding

**Status:** Partial isolated development, October 21, 2026. The operator subsequently authorized implementation after the initial design. The H1 checkpoint (internal supporting reference; not included in this packet) qualifies owner-only profile metadata/history; H2 (internal supporting reference; not included in this packet) qualifies a scoped facade over a trusted host authentication callback. The full principal/grant/audience authority and actual authenticated frontend bindings below remain proposed, not installed APIs or commands. No protected activation, migration, deployment or upstream submission is authorized.

**Baseline:** Qualified downstream core/SDK `2d1502b5210ad43d4566000499192f4172aa0e6f`, followed by owner-profile/history prerequisite `b70cf2d`. Existing legacy behavior remains unchanged. The upstream CLA hold remains in force.

**Configurable vocabulary:** The operator selected one generic model with domain-configurable levels, access rules and user/administrator terminology. Government/military labels are one familiar example, not a hard-coded default. Use the [profile configuration guide](/hidden/review-2d66666c7be62e65c7daf868/policy-profiles/) and canonical [regulatory overlays](/hidden/review-12caba0b6046f6338c842cd2/#regulatory-and-professional-overlays). HIPAA, legal confidentiality and other applicable duties remain independent controls, not extra ranks or automatic government designations. Configuration authority does not grant content access. This terminology update does not implement or activate a profile.

## Executive Summary

Add an optional host-local authority that turns explicit operator-managed identities, conversation audiences, grants and routes into the complete fresh `HostPolicySnapshot` already consumed by the protected reference adapter. It is an extension at the host boundary, not another memory engine, a mandatory policy server, an identity guesser or a claim that current Hermes/MCP/CLI installations already enforce policy.

The first implementation should use one bounded local metadata authority with serialized administrative updates, an explicit trusted frontend integration, and independent restore-freshness evidence. It must reuse the existing indexed enforcement, encrypted owner repository and audited read SDK. Protected requests without complete identity, audience, current authority or qualified provider/output hooks refuse before memory access. Legacy requests cannot be used as a fallback for a protected route.

The operator manages permissions; authenticated transports establish which registered identities and actual output audience apply. Registering a name is not authenticating a request. An agent's broader privileges elsewhere never widen a conversation's effective permissions. Changing audiences or grants cancels the old turn and requires a clean authorized model context, not merely a new recall filter.

### Index

- [Scope and trust](#scope-and-trust)
- [Architecture and existing interfaces](#architecture-and-existing-interfaces)
- [Authority records and operator workflow](#authority-records-and-operator-workflow)
- [Authenticated requests and complete audiences](#authenticated-requests-and-complete-audiences)
- [Snapshot and epoch protocol](#snapshot-and-epoch-protocol)
- [Provider, output and history gates](#provider-output-and-history-gates)
- [Frontend bindings](#frontend-bindings)
- [Restore and interruption](#restore-and-interruption)
- [Compatibility and supported surfaces](#compatibility-and-supported-surfaces)
- [Qualification and performance](#qualification-and-performance)
- [Implementation slices and remaining gates](#implementation-slices-and-remaining-gates)

## Scope And Trust

Protect supported memory-derived candidates, tools, prompts and outputs from exceeding the current conversation's authority. Keep original documents outside Mnemosyne; this authority stores only bounded identity, policy, routing, revision and audit metadata. No transcript, document, embedding, source excerpt, prompt or secret value belongs in its grant records.

The administrator, trusted host integration, raw key/SQLite owner and code executing with those capabilities remain trusted. A malicious filesystem administrator or arbitrary same-owner Python process is outside this library's sandbox guarantees. An administrative capability is separate from an ordinary conversation principal: giving a person memory access must not silently grant permission to edit grants or read the decision journal.

Model-controlled shell, Python, filesystem and debugging tools must not possess those owner capabilities. If an agent can run unrestricted code as the authority/key owner or inspect the trusted host's memory, it can bypass this API; more SQL checks do not fix that. Such a profile cannot claim an enforcing boundary against that tool use. Use an existing qualified tool sandbox, distinct owner identity or equivalent capability separation, or leave the profile unsupported. This design does not silently introduce a daemon or claim process isolation that is absent.

No automatic host/user discovery, trust-on-first-message, title parsing, agent-written grants, wildcard permissions, executable configuration callbacks, plaintext fallback or cloud dependency is introduced. External identity providers can later implement the same boundary; they are not required. A remote memory caller needs an explicitly authenticated host binding; a local filesystem alias or SSH connection alone does not authenticate everyone who will receive its answer.

## Architecture And Existing Interfaces

{% include blog_diagram.html src="/hidden/review-2d66666c7be62e65c7daf868/diagrams/host-01.svg" alt="Architecture And Existing Interfaces - policy flow diagram" %}

<details markdown="1">
<summary>Diagram source</summary>

```text
flowchart TD
    O[Operator administrative capability] --> P[Validate and preview explicit metadata changes]
    P --> A[Host-local authority and current epoch]
    W[Independent restore-freshness witness] --> A
    T[Trusted authenticated frontend] --> R[Opaque request and complete audience binding]
    R --> S[Fresh atomic host snapshot]
    A --> S
    S --> H[Existing ProtectedHostAdapter]
    H --> M[Current encrypted owner repository and indexed reads]
    M --> E[Authorized evidence only]
    E --> G[Fresh prompt and provider admission]
    G --> L[Approved provider and bound model context]
    L --> D[Fresh output admission to exact audience]
    A -. Epoch changes cancel old work .-> G
    A -. Epoch changes cancel old work .-> D
```

</details>

Existing contracts at the frozen baseline are `ParticipantGrant`, `HostPolicySnapshot`, `ProtectedHostAdapter(load_snapshot=..., resolve_store=...)`, `ProtectedSession`, `SnapshotAuthority` and `ProtectedRepository`. Their source is not changed by this design. The new binding implements the two explicit host callbacks; it does not bypass the reader or construct a legacy `BeamMemory` on protected artifacts.

The source-interface inventory (internal supporting reference; not included in this packet) found useful attribution/authentication/routing at the traced entrypoints, but not the complete current authorization snapshot. A future adapter must supply that missing contract rather than reinterpret existing titles, author fields or session selectors. This observation is pinned source evidence, not a claim about every possible upstream plugin or current deployed transport.

### Proposed Logical Interfaces

| Proposed interface | Responsibility | Explicitly not authority |
| --- | --- | --- |
| `LocalHostAuthority` | Read current bounded identity/grant/route metadata; serialize exact-predecessor administrative updates | A model tool, grant-file import on read or a permissive default configuration |
| `RequestAdmission` | Issue a process-owned opaque handle after trusted frontend authentication and exact audience/route admission | A caller-supplied context dictionary, chat label or arbitrary bearer string |
| `load_snapshot(handle)` | Reauthenticate the admitted handle, read fresh metadata and return the existing exact `HostPolicySnapshot` type or refuse | A cached permission result, model argument or independent agent privilege |
| `resolve_store(store_id)` | Resolve one host-selected registered owner repository and decision journal | A tool path, environment-selected bank or filesystem search |
| `TurnBinding` | Bind current authority/roster/route and authorized history/evidence to one model context | Permission to reuse previous higher-privilege provider state |
| Provider/output admission | Recheck the turn binding and actual destination before each supported submission/release | A receipt that grants indefinite access or authorizes another route |

These are design responsibilities, not promises to expose all names as public classes. Keep transport and provider integrations narrow; do not build a general RPC service merely to pass an in-process capability.

## Authority Records And Operator Workflow

Use one host-local metadata database in an explicitly provisioned private root, separate from memory artifacts, publication authority and content-bearing backups. Proposed root/database permissions are owner-only, with canonical identity checks and no symlink-following provisioning. The real filesystem and durability behavior require qualification; different directory names do not by themselves create independent restore domains.

| Record | Required content and invariant |
| --- | --- |
| Authority header | Schema/contract version, pinned random authority ID, current generation, policy digest and recovery state; no implicit initialization during reads |
| Policy definition | Exact namespace/ID/version and configured ordered level IDs matching the memory domain; separate user/admin labels and explicit mappings for legacy/custom vocabularies; invalid or unknown values refuse |
| Principal registration | Stable opaque principal ID, kind, enabled state and explicit trusted issuer/subject mapping; display names are non-authoritative |
| Participant grant | Explicit bank/project, owner/tenant, compartment/audience, purpose, operation, destination and classification ceilings; empty sets grant nothing; bank-wide access defaults false |
| Conversation audience binding | Trusted frontend/conversation identity, complete applicable principal roster, explicit audience/route revision, purpose, exact allowed store/domain and supported delivery contract |
| Store registration | Exact store ID, domain, bank, owner-registry key and required protected capability/version; no content or key value |
| Destination registration | Exact logical endpoint, recipient/audience semantics, approved provider/output route and capability version; secrets belong in the existing host credential mechanism |
| Update receipt | Unique operation ID, predecessor/current generation, canonical metadata digest and content-free result; retry inspection is not authorization |

For each selected regulatory/professional overlay, authority administration must record applicability, controlling jurisdiction/source/version, supported actions and required current attestations. Patient/matter scope, purpose, consent or other disclosure authority, ethical-wall exclusions and provider approvals remain separate from clearance. A chat/persona label, a high tier, an `overlays` string or an administrator's generic provider approval does not satisfy those predicates. Unsupported overlay/operation combinations refuse. Keep actual government designations distinct from organizational analogues; this host is not authorized for actual classified processing by using familiar names.

The proposed metadata digest covers a deterministic encoding of the active contract version, authority identity/generation, policy, principals, grants, audience/route bindings and store registry. It excludes its own digest field, inactive preparations and receipt history to avoid recursive hashes and prevent an uncommitted proposal from changing the active-state identity. Define canonical byte encoding and exact bounds in H-A, including Unicode, ordering, unknown/duplicate fields and tombstones; neither hashing the SQLite file nor file mtimes defines this logical digest. The authority contains sensitive identifiers even though it holds no memory text.

Use strict structured import/export with bounded record counts and sizes, duplicate/unknown-key refusal and exact type validation. A proposed first implementation should cap each request roster and each grant label set at the existing 256-entry contract limit; aggregate principal/route/update limits must be fixed and overflow-tested in its own reviewed schema before coding. Exhaustion refuses rather than evicting revocation state or resetting the epoch. No user-controlled SQL, module import, shell callback or expression evaluator is allowed.

The operator workflow is validate, preview, apply against an exact predecessor, inspect receipt. Preview shows the resulting effective permissions for selected synthetic contexts, affected routes, invalidated turns, backup/restore obligations and unsupported surfaces. Expanding access is never hidden in an unrelated configuration save. Administrative writes require an authenticated administrative host capability, not a grant embedded in a conversation. No actual CLI syntax or configuration key is introduced in this design.

Initial provisioning creates an empty denied authority; it does not manufacture a privileged default person or infer a participant from an OS username. Grants and issuer mappings are explicit separate administrative changes. Importing a proposal never applies it automatically. Source identities and policy classification remain separate: missing record classification can normalize to `unclassified` only under the already reviewed vocabulary/inheritance rules, and never creates a participant grant or public access. No record backfill or migration is included.

Configuration, grant administration, approval, sensitive-metadata inspection, audit review and content access are separately scoped capabilities, with configurable role names. A configuration administrator receives no implicit plaintext, filename, history or raw-key access. Prevent self-elevation through direct grants, controlled identities/groups, level ordering, rule/route substitution, delegation or changes to the approval policy. A single operator may explicitly hold several roles; no universal admin flag supplies them automatically. Raw platform/key-owner powers remain a different trust boundary, not a configuration entitlement. These administration constraints are implementation requirements, not new qualified capabilities.

### Synthetic Permission Example

This is a human-readable grant projection, not executable configuration. The same explicit store, owner, purpose and route must be authorized for all applicable participants.

| Field | `person:example` | `agent:example` | Effective shared request |
| --- | --- | --- | --- |
| Classification ceiling under organizational reference profile | `confidential` | `top_secret` | `confidential` |
| Allowed projects | `project:notes` | `project:notes`, `project:private` | `project:notes` only |
| Owners | `owner:example` | `owner:example`, `owner:other` | `owner:example` only |
| Purpose | `assist` | `assist`, `research` | `assist` only |
| Destination | `route:private-example` | `route:private-example`, `route:other` | `route:private-example` only |
| Bank-wide access | false | true | false; a nonempty shared project selection is required |

The agent's private-project memory must not be retrieved for internal reasoning in this shared request. Removing the shared project, adding an unmapped participant or selecting the other route refuses; the host does not shrink the declared audience to make the request succeed. The familiar reference tiers do not create patient/matter access or public-release permission, and they do not silently replace existing policy vocabularies.

## Authenticated Requests And Complete Audiences

Identity proof comes from the trusted frontend, not from the model or a newly asserted grant. Bind exact issuer/subject pairs to registered principals only after the frontend validates its authentication. An OS account or MCP token can establish the caller under a qualified binding; neither establishes the full downstream conversation audience on its own. An operator-entered subject mapping still needs actual request authentication and replay/session checks.

The complete applicable roster includes the human and agent principals whose participation is relevant to the policy, including silent members who can receive the output. Forwarding, shared links, relay destinations, multi-device/shared sessions and group membership must be represented by the frontend's delivery contract. Providers and other data processors also require explicit destination/provider authorization; choosing a model does not grant it permission to receive private data. They cannot be silently omitted merely because they are not message authors.

A fixed private route can use an explicitly registered static roster only if the frontend enforces that exact audience, provides a current route/recipient-set revision and invalidates the binding whenever the route or its access ACL changes. Operator enumeration alone is insufficient for an unbounded group or a route whose membership cannot be verified. A transport with unknown or expanding audiences is unsupported for protected plaintext.

Handles are issued only by trusted ingress, are process-owned, short-lived, scoped to one request/turn and rejected in another process, session, route or authority generation. They are not passed in model arguments, persisted into message history or logged. Ordinary tool arguments can select only narrower approved operations/projects, never principals, permission ceilings, bank ownership or egress callbacks. Initial cross-process handle serialization is unsupported; adding it later requires a separate authenticated replay-resistant protocol, not pickling the Python object.

## Snapshot And Epoch Protocol

Keep the host authorization generation `H` distinct from memory publication generation `M` and memory lifecycle epoch `L`. A stable revision/digest identifies the exact policy and audience. Timestamps, conversation titles, source hashes and a matching old snapshot are not freshness evidence.

1. Validate the opaque ingress handle, its configured process-monotonic lifetime and the trusted frontend's current audience/route assertion. Acquire fresh restore-freshness evidence for the configured authority identity; unavailable or uncertain freshness refuses. Initial grant expiry is explicit revocation/disabled state, not a wall-clock freshness heuristic; time-based grant scheduling is unsupported until separately specified.
2. Read the authority header, exact policy, principal states, all selected grants, roster and route from one short committed metadata snapshot. Refuse missing, duplicate, disabled, ambiguous or incomplete registrations. Each materialized `ParticipantGrant.authority_epoch` is `H` because it was read under that current authoritative revision; it is not refreshed by relabeling a cached old grant.
3. End that metadata read transaction. Resolve the registered current owner checkpoint and `L` through the existing independent publication authority. Recheck current host/witness and frontend revisions from a new read; refuse any change. This is checked composition across separate authorities, not a claimed distributed atomic transaction.
4. Construct the existing exact `AccessContext`, `PolicyDefinition`, `ParticipantGrant` tuple and `HostPolicySnapshot`. Include the complete roster, host issuer, current `H`, actual bank/store/domain/destination, explicit purpose/project selection and independently current `L`. Reuse `effective()` for intersection; add no wildcard, union or agent-privilege fallback.
5. Run the existing guarded SDK. Each callback invocation reads current authority again; it must not inherit a caller's old SQLite transaction. Changed `H`, `M`, `L`, audience, route or policy invalidates the handle and the whole old turn, even if a later change happens to restore equal-looking permissions.

The proposed first implementation uses a single conservative host generation: any authorization/identity/route change increments `H`, invalidating all outstanding bindings for that authority. Per-route optimization can follow profiling and separate proof; correctness does not depend on targeted invalidation messages arriving. Deleting and recreating a principal/route does not reuse a prior identity or generation. Overflow and lost generation state refuse.

Administrative changes use an exact-predecessor serialized metadata transaction, unique operation receipt and strict validation of the complete result. Never use read-uncommitted mode, shared mutable grant dictionaries or a long-lived read transaction as current authority. SQLite permits old readers to retain snapshots after another connection commits; a fresh verification therefore requires ending the previous read transaction, not another SELECT in it. See [SQLite isolation](https://sqlite.org/isolation.html). The proposed implementation must separately qualify its admitted journal/synchronous settings and filesystem; [SQLite atomic commit](https://sqlite.org/atomiccommit.html) is not evidence of a cross-file or backup-freshness guarantee.

## Provider, Output And History Gates

The library callback is not automatically Hermes prompt assembly, SDK submission or network delivery. Each enabled host must implement the following checkpoints and prove that untrusted code cannot bypass them on a protected route.

| Boundary | Required action |
| --- | --- |
| Ingress and turn creation | Authenticate actual route/audience and bind fresh authority before any memory, persona, prefetch or history loading |
| Memory candidate/tool execution | Pass the opaque request separately from model arguments; use the existing indexed protected APIs and fixed refusals |
| History/persona/cache assembly | Audience narrowing requires a clean security/model context, not in-place sanitization; admit only independently authorized provenance-bearing inputs into it, and refuse if the host cannot isolate old state |
| Prompt assembly | Attach exact authorized evidence/context lineage to the turn; no broader independent-agent recall, fallback memory file or hidden tool preload |
| Provider submission | Recheck current authority, full turn provenance, approved provider identity and actual route immediately before a supported SDK submission; check retries and background jobs too |
| Provider output and tools | Bind tool calls/results, generated output and summaries to the originating turn's restrictions; do not treat generated text as automatically public |
| Streaming/nonstreaming egress | Recheck before each supported chunk or full-body release to the exact current audience; close/drain cooperative producers on invalidation |
| Persistence, reports and handoffs | Preserve strict provenance/restrictions or refuse unsupported persistence; logs/coordination journals cannot receive private payload by default |

A participant, grant, purpose, policy or route change cancels queued work and invalidates leases, memory results, prompts, pending retries, provider sessions and caches tied to the old turn. Audience narrowing requires a new clean security/model context; the conservative default starts one whenever a new person/agent joins. Do not continue or attempt to sanitize the existing privileged model context: the provider may already have seen that material. New inputs must be independently authorized, not a replay of the old transcript, hidden state, tool outputs, persona/prelude or conversation summary. If the application cannot establish that boundary, refuse. Output filtering cannot repair earlier prompt contamination. Broader permissions also require a new admitted turn, never retroactive permission to reuse an old handle.

The transition must also fence old-epoch deliveries and preserve old transcript/attachment/history visibility restrictions. A new model context alone cannot protect old messages exposed by the frontend. Prefer a separate conversation when adding the new audience would otherwise expose the previous thread; incapable frontends must refuse that protected transition. Continuity is optional: use only a current authorized release artifact or rebuild from independently authorized evidence in the fresh context. Model-generated sanitization of the old privileged session is not an automatic declassification/release decision. If no safe summary is available, start with no summary. No historical transcript is deleted or automatically reclassified by this rule.

Ordinary transcripts and externally supplied documents may lack provenance. This memory extension cannot certify arbitrary existing chat history or police deliberate retyping by the operator. Protected-route acceptance must either prove the relevant history/other-input contract or exclude those paths; it must not silently mark all historical text unclassified. Conversation-history storage and retention changes require their own scoped acceptance, not automatic private-history copying.

Define admission as the final supported local gate before a synchronous handoff or bounded transport release. Administrative commits and that admission must have a tested ordering; no authority lock or SQLite transaction is held while waiting for inference or network I/O. A later revocation cannot retract already submitted prompts, emitted bytes or uninterruptible external work. Cancellation signals provide promptness, not authority; fresh gates remain necessary after process loss, delayed notifications or subscriber disconnect. Do not claim linearizable revocation across arbitrary callbacks or remote providers. A provider/transport whose queued submissions or stream chunks cannot be gated and cancelled within its declared contract remains unsupported.

## Frontend Bindings

### Hermes

Keep the existing legacy provider contract working for legacy routes. A protected route requires explicit capability negotiation between trusted gateway/desktop ingress, turn/prompt assembly, `MemoryManager`, the Mnemosyne provider, tool/prelude execution, provider submission and actual delivery. No unknown keyword can be silently dropped into the old path. Missing hooks/capability versions fail that protected route before content is read.

Pass the opaque authenticated request via a dedicated trusted host channel, not a tool field, title or plain `session_id`. Background prefetch and copied ContextVars must preserve the binding and revalidate it at execution time; A/B/A interleaving must not share a mutable provider/grant cache. The traced `chat_id`/`channel_id` mismatch must be resolved by an explicit tested route mapping, not assumed equivalence. Single `turn_author` metadata is attribution, not a complete roster.

Protected automatic sync/write, persona/ordinary memory preload, cron/heartbeat recall, scripted preludes, retained provider context and asynchronous delivery remain blocked until individually supported. Disabling one read callback does not prove those paths cannot bypass the boundary. An authorization failure cannot degrade to ordinary memory or an agent-wide bank. The first release can remain read-only for protected memory while ordinary authorized nonmemory chat behavior is separately defined; any reused private context still requires the history/provider gates above.

### MCP

Require an authenticated client identity plus an explicitly registered calling-application audience/route binding. Multi-token attribution is useful but not complete authorization; a bearer token's owner is not necessarily the sole reader of the final answer. A model cannot nominate a lower-privilege-looking audience or switch the bank/route through arguments. An authenticated calling application's current audience assertion must use an explicitly trusted host channel; do not add a generic signed-JSON scheme without its own issuer, key and replay contract.

Initially refuse protected operations for shared anonymous tokens, unbound stdio callers, unknown caller applications or missing current downstream audience proof. This does not disable those modes for legacy stores. A source-level synthetic MCP test is not acceptance of the actual HTTP/stdio dispatch, cancellation or output path.

### CLI

Separate administrator metadata inspection/change from protected plaintext retrieval. Administrative identity is explicitly provisioned and authenticated by the qualified local binding; a username or `--principal` string is not proof. A protected read additionally needs a registered invocation/recipient contract and actual output destination. Piping to an arbitrary command/file is not automatically the same approved audience as an interactive terminal. Initial unsupported redirected/plaintext routes refuse rather than writing and warning afterward. No new parser flags or CLI implementation are supplied here.

## Restore And Interruption

Protect three independent authorities: current encrypted-memory publication, host authorization state, and evidence that those authorities have not themselves been rolled back. Use a proposed restore witness with pinned authority/realm identity, strictly increasing generation, exact committed metadata digest, and serialized compare-and-advance semantics. A static ID, signature, secret key or file mtime authenticates neither recency nor nonrollback by itself.

The host-local deployment must identify a witness/recovery root that survives the supported memory and authority restores. It can be locally operated; no mandatory online/cloud service is introduced. Merely placing another database in another directory is insufficient. A witness backend and its real restore domain must be qualified before activation. Complete machine/witness co-restoration is not detectable purely from those restored bytes; require an independently surviving anchor or explicit administrative recovery that fences the old realm. Lost or uncertain witness state denies protected access, not silent reprovisioning.

Proposed authority-update protocol:

1. Validate the exact predecessor and write a durable prepared change plus operation ID/digest, without exposing its grants as active. Serialize administrative changes so a second writer cannot prepare a competing successor.
2. Advance the independent witness to the exact prepared successor using compare-and-advance. Readers refuse while the database and witness select different generations/digests. They never elect a winner by timestamp or grant generosity.
3. Finalize the exact witnessed successor locally and issue invalidations. Only a matching committed database/witness pair is readable. Notification failure does not restore old authorization.
4. After uncertainty, inspect the durable receipt, witness and prepared state. A matching prepared successor may be finalized; an unwitnessed proposal cannot grant access. Missing witnessed bytes, conflicting operation IDs or ambiguous witness advancement keep the authority fenced for explicit recovery. No blind retry, old-grant fallback or epoch decrement is allowed.

Implementation must define this state machine and every crash edge before coding; the existing `SnapshotAuthority` API is not a ready-made host-grant witness. No atomic transaction across database/witness/memory files is claimed. A revocation is reported complete only after its witnessed successor is active; failures are visible, not reported as successfully revoked. Reads during a prepared mismatch fail closed. Same-user administrators remain trusted; this protocol is not hardware attestation.

| Failure | Required result |
| --- | --- |
| Old memory restored, memory publication authority current | Existing encrypted owner boundary refuses the wrong/missing generation; no prior artifact fallback |
| Old grant database restored, witness current | Refuse mismatched generation/digest before memory decryption |
| Missing database, witness or registered authority identity | Refuse; no read-triggered provisioning or authority reconstruction from memory/config |
| Crash before witness advancement | Prior matching committed state remains usable only if preparation/recovery rules prove it current; pending proposal grants nothing |
| Crash after witness advancement, before finalization | Fence reads; reconcile only the exact durable prepared successor or remain denied |
| Lost COMMIT/witness acknowledgment | Inspect exact receipts/current state; do not report failure as proof nothing committed and do not replay blindly |
| Both database and witness restored together | No freshness claim without another surviving trusted anchor; recovery/activation remains fenced |
| Restored configuration omits the binding | Protected store/route capability requirement still refuses; no legacy reopening |

Keys remain in the existing approved host credential mechanism, referenced by logical identity only. This design adds no secret-value editor, key export, plaintext fallback or automatic rotation. Full-machine restore, key loss/compromise and cross-host authority replacement require an explicit reviewed recovery procedure and separate evidence.

## Compatibility And Supported Surfaces

Legacy stores and unconfigured installations keep their current behavior. Provisioning this authority never converts, reclassifies, grants access to or reindexes an existing bank. A protected store and host route must persist their capability requirements, and missing/older clients must refuse; changing a default config field cannot downgrade them. The storage-level old-client refusal is necessary but does not erase cached plaintext outside that storage.

Initial protected frontend scope should be the already qualified read/evidence operations with explicit capability declarations and exact-artifact transport acceptance. Generic writes, ingestion, derivatives, consolidation, graph, export/sync, maintenance, persona, administrative/debug content access and nonconforming source resolvers remain blocked. The lower-level owner APIs and explicit source-expansion seam are separate capabilities, not permission to route arbitrary frontend calls to them. Compact and stream use require their own provider/output binding; labels such as read-only cannot substitute for that evidence.

Denials at public boundaries use stable content-free refusal and do not disclose whether a record, principal, private route or bank exists. Record allow/deny metadata using the qualified audit contract; grant administration uses a separately authorized sensitive journal. Do not log request handles, bearer credentials, raw claims, filenames, queries, prompts or payloads. Timing and count confidentiality require their own measurements; this design makes no constant-time claim.

## Qualification And Performance

All complete scenarios below remain **planned or partial** for this binding. H1 supplies narrowly qualified owner metadata/witness interruption evidence; it does not complete any full host/transport scenario. Subsequent scoped facade results are recorded separately in the contribution ledger. Existing core tests are predecessor evidence, not blanket passes for these new host/transport/witness behaviors. Use synthetic participants, disposable authorities and denied canaries; no production data, provider call or real key is needed for initial implementation.

| ID | Required scenario | Primary gate |
| --- | --- | --- |
| H01 | Empty/unconfigured binding; missing/invalid grants; unsupported schema; no permissive provisioning | V1, V3, V7 |
| H02 | Authenticate registered issuer/subject; forged tool principal/token name/title/session label refuses before lookup | V1, V4 |
| H03 | Complete shared roster including silent recipients; unknown/duplicate/missing participant refuses | V1, V4 |
| H04 | Broader agent with narrower human; bank/project/owner/tenant/compartment/audience/purpose/route intersections | V1, V2 |
| H05 | Empty project selection never implies all projects; explicit all-participant bank-wide permission | V1, V2 |
| H06 | Fixed private route verifies actual recipients/ACL; group expansion and redirects invalidate old handle | V4, V6 |
| H07 | Fresh snapshot reads; injected concurrent administrative commit, caller transaction, stale reader and ABA changes | V1, V6 |
| H08 | Separate current H/M/L composition; mismatched domain/store/publication/epoch refuses before decode/output | V2, V7 |
| H09 | Actual Hermes gateway/provider/tool/prelude/background A/B/A dispatch; inspect nontarget stores and model inputs | V2, V3, V4 |
| H10 | Actual MCP HTTP/stdio and CLI direct/redirected paths; identity, audience and output bindings, unsupported refusals | V3, V4 |
| H11 | High-ranked denied native FTS/vector/hybrid/direct/source candidates never reach scorers or provider payload | V2, V9 |
| H12 | Permission/audience/route/purpose change before and during prefetch, prompt assembly, provider queue and retry | V2, V6 |
| H13 | Revocation during chunk waits, EOF, cancellation, tool round and final-body delivery; producer cleanup | V3, V6 |
| H14 | Narrowed audience requires clean security/model context or refusal, no in-place sanitization; fence old deliveries/history exposure and admit only independently authorized continuity; T01-T06 | V2, V3, V5, V6 |
| H15 | Every blocked write/graph/maintenance/export/sync/admin/persona path refuses with no legacy fallback | V3, V5, V7 |
| H16 | Restore old memory, authority, config, witness or all together; unavailable surviving anchor stays fenced | V7 |
| H17 | Inject failure at every prepare/witness/finalize edge; lost acknowledgments, competing writers, exact receipt recovery | V6, V7 |
| H18 | Capacity/overflow, malformed structured imports, unknown fields, alias/symlink/root replacement and permission errors | V1, V7 |
| H19 | Content-free public errors/audit; separately authorized administration; check counts/names/metadata and timing gaps | V8 |
| H20 | Exact-artifact install without checkout; old clients, missing hooks and capability version mismatch refuse | V3, V7 |
| H21 | Legacy regression and unchanged 1024-dimensional embedding identity; no migration or provider fallback | B7, V9 |
| H22 | Repeatable fixed-baseline cost, recall oracles and denial coverage across every enabled boundary | V10 |
| H23 | Model-controlled shell/Python/file/debug tools cannot obtain raw owner keys, authority mutation or decrypted handles; incapable profiles stay unsupported | V2, V3, V7 |

For each implementation slice, compare the exact predecessor under identical bounded workloads before integration. Measure complete request p50/p95, throughput, peak process/native memory where available, authority read/SQLite-call counts, cancellation latency, audit/witness writes, permission-update contention and index growth. Include 1/2/8/32/256-participant synthetic rosters, denied/high-rank canaries, direct and native 1024-dimensional recall, one/eight-chunk streams and compact evidence with a fixed explicit tokenizer. Treat absent semantic-quality or timing-threat-model evidence as open, not passing.

Do not cache permissions, current epochs, witness results or complete host snapshots between enforcement checkpoints to hit a budget. Immutable policy parsing and safe prepared-query reuse can be profiled separately. Metadata work should scale with the bounded roster, not with all memory records; keep authorization in indexed candidate generation. The initial coarse global H may cancel unrelated turns on any edit; record this explicit simplicity/performance tradeoff before proposing finer-grained invalidation.

The existing original-baseline and final core cost columns remain in the performance report (internal supporting reference; not included in this packet). No performance result is claimed for this design. Any overhead budget remains provisional until its real bindings and workload are measured.

## Implementation Slices And Remaining Gates

| Slice | Bounded implementation | Must precede the next slice |
| --- | --- | --- |
| H-A: Authority and restore state machine | Strict metadata schema, explicit admin capability, serialized preview/CAS/receipts, witness interface and disposable recovery backend | Freeze exact schemas/limits, recovery semantics and H01/H07/H16-H19; no activation |
| H-B: Trusted ingress and snapshot loader | Explicit issuer mappings, complete enforced audience/route binding, opaque handles and existing host callbacks | H02-H08 with real authenticated host fixture; no model-argument authority |
| H-C: Frontend/provider/output lifecycle | Narrow capability-negotiated Hermes hooks plus explicitly supported MCP/CLI bindings; clean contexts and cancellation | Actual H09-H15, including unsupported-path refusals and inspected provider inputs |
| H-D: Candidate qualification | Exact artifacts, legacy/interpreter suites, restoration evidence, API/operator docs and measured costs | H20-H22 plus complete applicable V/A/B evidence before recommending activation |

These are logical review slices, not new PRs already opened or a reason to bundle the whole branch against upstream main. Keep storage/core changes independently reviewable. The operator has approved this design direction, not the proposed schema as a final public API or deployment. Exact schema/backend contracts, foreign Hermes hook changes and eventual activation must satisfy the applicable review gates; subsequent authorization to implement does not make those designs qualified or deployed.

The reference-profile G01-G10 scenarios in the canonical specification are additional planned proofs, not passes for H01-H23. They cover classification/clearance terminology, independent need-to-know and regulatory overlays, actual provider/recipient controls and safe legacy mappings. Before coding any regulatory evaluator, freeze its exact supported profile/actions and acceptance evidence; the host-local authority by itself does not implement HIPAA, legal-ethics or other jurisdictional decision rules.

Additional planned administration proofs require a configuration-only principal who can change only permitted settings while denied content, grant escalation, audit-content access and recovery/key operations remain denied; test indirect/aliased self-elevation and semantic-versus-display changes. These checks do not treat arbitrary trusted owner code as sandboxed. The operator subsequently authorized implementation after documentation; that permits isolated development and qualification, not live activation, deployment or upstream submission.

## References

- [Canonical policy specification](/hidden/review-12caba0b6046f6338c842cd2/) and [V1-V10 status](/hidden/review-2d66666c7be62e65c7daf868/validation/).
- Qualified core ledger (internal supporting reference; not included in this packet), [local RFC](/hidden/review-2d66666c7be62e65c7daf868/rfc/) and upstream submission hold (internal supporting reference; not included in this packet).
- Existing host API (internal supporting reference; not included in this packet), owner/restore contract (internal supporting reference; not included in this packet), guarded SDK (internal supporting reference; not included in this packet) and complete synthetic example (internal supporting reference; not included in this packet), all at frozen `2d1502b`.
