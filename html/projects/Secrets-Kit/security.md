---
layout: page
title: "Secrets Kit security and privacy"
permalink: /projects/Secrets-Kit/security/
published: true
secrets_kit_product: true
hide_banner_image: true
product_nav_order: 60
nav_title: Security & Privacy
image: /assets/images/projects/Secrets-Kit-Banner.png
excerpt: "Understand local storage, application access, encrypted synchronization, relay visibility, and recovery responsibilities."
---

{% include secrets-kit/navigation.html %}

Secrets Kit helps you keep credentials in a deliberate local workflow. Understanding where plaintext becomes available is more useful than a blanket promise that a key can never leak.

## Where are my credentials stored?

The configured local backend stores your credentials. Secrets Kit supports macOS Keychain and encrypted SQLite; the normal new-store setup uses encrypted SQLite. Storage keys and identity material live under the operating-system user's control. Peer synchronization is associated with the supported SQLite workflow; do not assume that selecting Keychain automatically makes Keychain items synchronized records.

Local storage protection is separate from transport encryption. A destination-encrypted synchronization envelope does not remove the need to protect the local user account, datastore, and keys. The {% include secrets-kit/doc-link.html file='SECURITY_MODEL.md' label='security model' %} documents those boundaries in more detail.

## Can an application or agent see a secret?

**A process receiving an injected credential receives its plaintext value.** With `seckit run`, selected credentials become environment variables in the child process. The application can use them, log them, or pass them to its own children. A compromised user account or process remains a risk.

That does not require pasting values into a conversation. An agent can help configure a process without receiving its credentials as chat text. But do not assume that an agent with arbitrary command execution is technically prevented from inspecting its environment.

The optional **Model Context Protocol (MCP)** interface is read-only and policy-scoped. Read-only means it does not provide write operations; approved retrieval can still disclose a value to a model. Keep retrieval denied unless you intentionally authorize exact names. The {% include secrets-kit/doc-link.html kind='hermes' label='Hermes integration' %} distinguishes process access from model-visible retrieval.

## What can another machine receive?

Peers require explicit authorization. Finding a machine on a network does not make it trusted. For supported encrypted SQLite synchronization, the sending peer encrypts an envelope for the destination, and the receiver protects accepted records using its own local storage key. Do not copy a local datastore key to another peer.

Decide which peers you trust before joining them. Synchronization is not a substitute for backups: changes and deletions can propagate. Test backup and recovery separately using the documented workflow.

## What does Remote Secrets Sync see?

Remote Secrets Sync forwards destination-encrypted envelopes. It does not receive secret plaintext, customer private keys, or local datastore encryption keys. It is a transport service rather than the authority for the contents of your local store.

Operating the service requires account, payment, connection, and authorization information. Encrypted payloads do not imply anonymous connections or zero metadata. This page does not claim that Secrets Kit is an independently audited zero-knowledge service, a hardware security module, or a compliance system. See the {% include secrets-kit/doc-link.html file='RSS_CUSTOMER_GUIDE.md' label='RSS customer guide' %} for enrollment and identity handling.

## Are keys escrowed or split between services?

Each peer keeps its own local storage and identity keys. To synchronize a record, the sender protects it for the destination peer; the receiver stores it under its own local storage key. RSS relays do not receive those keys. This is per-peer encryption and destination wrapping, not a threshold split-key scheme or a hosted escrow of customer datastore keys.

Hosted-account recovery codes restore billing-owner authority. They do not reconstruct your local secret store or replace lost datastore keys. Backups, local key recovery, and hosted account recovery need separate consideration.

## What do I need to preserve for recovery?

Protect your local store, keys, exports, and backups according to the documented recovery workflow. Keep them out of source repositories and broadly shared directories. An encrypted backup is only useful if you also retain the information needed to restore it.

For hosted-account ownership, save the account information and one-time recovery codes offline when the product provides them. Billing-owner recovery, replacing a revoked connection, and recovering local secret data are different operations. A recovered account does not restore a revoked device identity or bypass purchased capacity.

## What happens if I cancel?

Hosted forwarding stops when the service entitlement becomes inactive. The free peer-to-peer client and local credentials remain under your control, including unlimited connections on the same local area network (LAN) segment. Peers still require authorization and a working network route. Review [Pricing]({{ '/projects/Secrets-Kit/pricing/' | relative_url }}) for paid RSS quantity changes and replacement connections; uninstalling the client does not itself cancel a subscription.

## What should I share when asking for help?

Share the installed version, operating system, command, and sanitized error. Do not share secret values, raw environment dumps, credential files, private keys, recovery codes, or unredacted exports. Use disposable data when demonstrating a problem.

Start with [Guides]({{ '/projects/Secrets-Kit/guides/' | relative_url }}) for troubleshooting references. A successful installation check verifies installation; assess access and recovery separately for your workload.
