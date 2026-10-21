---
layout: review
title: "Policy-Aware Agentic Memory: Peer Review Packet"
permalink: /hidden/review-2d66666c7be62e65c7daf868/
unlisted: true
search_exclude: true
sitemap: false
list_exclude: true
short_link: false
review_index: /hidden/review-2d66666c7be62e65c7daf868/
review_date: "2026-10-21"
review_note: "Working documents shared for peer review. This packet is unlisted, not access-controlled. It describes downstream design and partially qualified implementation, not upstream approval or deployed protection."
---

# Policy-Aware Agentic Memory: Peer Review Packet

This packet brings together five working documents about extending agentic memory with need-to-know access, document classification, participant permissions, source integrity, and explicit authorization boundaries. The initial implementation target is Mnemosyne, while the requirements model is intended to remain product-neutral.

The **[Policy-Aware Agentic Memory Requirements and Specification](/hidden/review-12caba0b6046f6338c842cd2/)** is the canonical requirements document. The RFC provides orientation, the domain-profile guide explains the model through examples, the host-local design examines the proposed trust boundary, and the validation checklist distinguishes qualified work from partial or missing coverage. None replaces the specification.

## Suggested Reading Order

| Order | Document | Review purpose |
| --- | --- | --- |
| 1 | [RFC: Optional Policy-Aware Memory and External Source Integrity](/hidden/review-2d66666c7be62e65c7daf868/rfc/) | Short orientation: what is being extended, how it fits Mnemosyne, and what remains outside scope. |
| 2 | [Configuring Domain Policy Profiles](/hidden/review-2d66666c7be62e65c7daf868/policy-profiles/) | Understand the model through diagrams and government, healthcare, legal, financial, and personal examples. Review classification versus authorization, administrator separation, external documents, and conversation changes. |
| 3 | [Policy-Aware Agentic Memory Requirements and Specification](/hidden/review-12caba0b6046f6338c842cd2/) | Review the requirements: threat model, information model, authorization, retrieval boundaries, inheritance, revocation, compatibility, and acceptance criteria. |
| 4 | [Optional Host-Local Authorization Binding](/hidden/review-2d66666c7be62e65c7daf868/host-authorization/) | Examine authenticated identities, complete audiences, grants, epochs, provider/output/history gates, and restore protection. Particularly relevant to security architects. |
| 5 | [Policy Enforcement Validation Checklist](/hidden/review-2d66666c7be62e65c7daf868/validation/) | Challenge the release gates and inspect what is qualified, partial, or still missing. Requirements and passing unit tests must not be mistaken for complete protection. |

## A Shorter First Pass

For a limited-time review, read documents **1-2**, then the specification's [Threat Model](/hidden/review-12caba0b6046f6338c842cd2/#threat-model) and [Authorization Decision](/hidden/review-12caba0b6046f6338c842cd2/#authorization-decision) sections. Implementation reviewers should read all five, including the qualification limits and open decisions.

Each document has a collapsible **On this page** index. Diagrams are static images with expandable source text; click a diagram or its full-size link to use the site's zoom/pan viewer. Reading the documents and inline diagrams needs no JavaScript or external diagram service. The **Review packet and reading order** link returns here from any document.

## Review Brief

> Please identify missing threats, ambiguous authorization rules, bypass paths, and impractical operational requirements. Pay particular attention to participant-permission intersections, privileged context leakage, administrative self-elevation, revocation and in-flight responses, external-source classification, restore/downgrade behavior, and domain-specific restrictions that cannot safely be represented by a sensitivity level alone. Distinguish objections to the requirements from gaps in the current implementation.

Useful feedback identifies the document and section, the failure or ambiguity, an example or counterexample, and whether it concerns a requirement, a proposed design, or evidence still needed from an implementation. Synthetic examples are preferable to private records, credentials, or live permission changes.

## Status and Scope of This Packet

These are snapshots of the five selected documents as of **October 21, 2026**. Their original status notices, exact qualification scopes, open questions, and upstream-submission boundaries are retained. Downstream implementation or a qualified checkpoint does not imply upstream acceptance, complete cross-path protection, regulatory certification, or deployment.

Links among the five documents have been rewritten for this packet. Internal operational ledgers, private development paths, raw evidence artifacts, and supporting documents outside the packet are not included; their references are identified as omitted rather than presented as working links. Example participant/channel identifiers are generalized where needed. The original working documents remain unchanged.

The packet is excluded from the site's navigation, search index, feeds, and sitemaps, but it is still publicly accessible to anyone with its URL. Please keep sharing within the intended peer-review group. This is a document review packet, not a project launch or an upstream submission.
