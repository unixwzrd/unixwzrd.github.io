---
layout: page
title: "Secrets Kit privacy, license and service terms"
permalink: /projects/Secrets-Kit/policies/
published: true
secrets_kit_product: true
hide_banner_image: true
product_nav_order: 80
nav_title: Policies
excerpt: "Privacy, licensing, RSS service terms and optional support contracts for Secrets Kit."
---

{% include secrets-kit/navigation.html %}

This page applies to the **Secrets Kit client and optional Remote Secrets Sync (RSS)**. The Safari extension's [General Privacy Policy]({{ '/Policies/General_Privacy/' | relative_url }}) describes that extension, not Secrets Kit. It does not establish the data practices of this website or the hosted RSS service.

The retention rules and service providers for the hosted RSS service are described below. Separately agreed support contracts define the scope and terms of any additional paid assistance.

<nav class="seckit-jumps" aria-label="Policy sections"><a href="#client-privacy">Client privacy</a><a href="#remote-secrets-sync-privacy">RSS privacy</a><a href="#retention-and-deletion">Retention &amp; deletion</a><a href="#service-terms">Service terms</a><a href="#client-license">MIT client license</a></nav>

<h2 id="client-privacy">Secrets Kit client privacy</h2>

Your configured local backend holds credentials and their service/account metadata. Local storage and identity keys remain with your operating-system user. Authorized peers can receive the records you authorize for synchronization. Applications receiving an injected credential receive plaintext and may expose it through their own behavior; an agent with command access may also inspect it. See [Security & Privacy]({{ '/projects/Secrets-Kit/security/' | relative_url }}) for those limitations.

Local/LAN use does not require an RSS subscription. Installation and updates contact distribution services for the selected software and runtime. Enabling hosted RSS, configuring an agent provider, or sending a support request introduces separate data paths; local storage is not a claim that every workflow stays entirely offline.

<h2 id="remote-secrets-sync-privacy">Remote Secrets Sync privacy</h2>

| Data path | What it handles | Boundary |
| --- | --- | --- |
| Secret synchronization | Destination-encrypted messages temporarily held in an in-memory queue for delivery | RSS does not intentionally persist these messages to disk and cannot decrypt them. Authorized receiving peers can decrypt their records. This statement concerns message payloads, not account or operational metadata. |
| Hosted access and billing | Account/subscription identifiers, billing contact/profile and invoice information, purchased quantity, entitlement and connection authorization | Service enrollment and billing-owner authority are separate from permission to receive another peer's secrets. |
| Connectivity and operational safety | Opaque account and entitlement identifiers, public-key fingerprints, authorization state, connection limits, session/byte counters and aggregate host status | Encryption does not hide all metadata. RSS receives no customer billing contact or Stripe state. Aggregate host samples older than 397 days are pruned when new samples are recorded. |
| Optional peer invitations | Encrypted onboarding messages when that separate feature is configured | The production operator does not currently configure this persistent mailbox. Ordinary paid Checkout and enrollment do not require an invitation. |
| Support | The information you choose to include in a report or private message | GitHub Issues and Discussions are public. Keep credentials, private keys, payment receipts and recovery material out of reports. |

Encrypted messages pass through an in-memory queue for RSS delivery; they are not intentionally persisted to disk. Operating-system swap or paging can still write memory contents to disk, so this does not mean ciphertext can never reach disk. The queue is not a durable delivery archive or recovery service.

Account, authorization, billing and operational metadata follow their own retention rules. If the optional peer-invitation mailbox is enabled in another environment, its persistent storage is separate from the in-memory delivery queue.

### Service providers

**Stripe** hosts Checkout, payment processing and the billing portal. **GitHub** hosts release downloads, versioned documentation, this website through GitHub Pages, and public Issues and Discussions. Installation may also retrieve Python runtime and dependency packages from their distribution services. The local operator authority and customer database run on our Mac; the East RSS host uses the **Hostinger** network and the West RSS host uses **IONOS**. **GoDaddy** provides DNS for `unixwzrd.net`, and **Let's Encrypt** issues the public TLS certificates. Private contact uses email handled by **Proton Mail** for `info@unixwzrd.ai`; the contact form opens your own mail client rather than storing a submission on this website. These providers process the information needed for their respective services under their own policies. We do not use an external RSS monitoring service.

<h2 id="retention-and-deletion">Retention and deletion</h2>

Local data, keys, replicas, exports and backups need their own lifecycle. Cancelling hosted forwarding does not delete your local credentials. Synchronization can propagate changes and deletions, but it is not a guarantee of immediate erasure from backups or every authorized peer. Uninstalling software, revoking a connection, cancelling a subscription and requesting account-data deletion are separate actions.

The local operator retains current and inactive customer accounts, subscription and invoice summaries, entitlement and device-authorization history, accounting aggregates and payload-free audit records **indefinitely until deliberate operator deletion**. Cancellation or device revocation changes access; neither automatically erases those records. The relay databases likewise retain authorization and accounting records until operator deletion. Aggregate RSS host-status samples in the operator database are removed once older than **397 days** when new samples are recorded. Destination-encrypted sync messages are held only in a transient in-memory relay queue for delivery, not a durable message archive; operating-system swap may still write memory to disk.

The East RSS system journal is configured for a maximum of seven days, subject to earlier size-based rotation; West has no configured fixed journal retention period. Protected recovery backups and private support email have no Secrets Kit automatic deletion deadline and remain until operator or provider deletion. The production operator does not currently enable the optional persistent invitation mailbox. There is no automatic account-erasure deadline after cancellation. A deletion request requires individual review, including any records that must remain for billing, security or recovery; deletion from another authorized peer, a provider, or an existing backup is not immediate or guaranteed.

For a privacy or deletion question, [contact us privately]({{ '/contact/' | relative_url }}) and identify Secrets Kit or RSS. Do not send secret values.

<h2 id="service-terms">Remote Secrets Sync service terms</h2>

The launch offer is **$5 per enrolled connection per month, minimum two connections ($10/month)**. The client remains free for local use and unlimited connections on the same LAN segment. An enrolled connection represents a registered client identity associated with an operating-system user; it is not a separate seat for each agent. [Pricing]({{ '/projects/Secrets-Kit/pricing/' | relative_url }}) explains the unit and examples.
The stable and opt-in public beta clients share one production RSS service and subscription. A paying customer may install either channel without a separate invitation, account, subscription or enrollment. Verified payment establishes the entitlement; only enrolled and authorized devices may use hosted forwarding. Applicable taxes are charged separately once collection obligations are confirmed; automatic Stripe Tax collection is not enabled for the initial offer.

Manage your connections and subscription separately:

- **Increase capacity:** contact support to add units to the existing subscription. Additions are prorated and invoiced; wait for verified payment and provisioning before enrolling another connection. Self-service portal quantity changes are disabled.
- **Revoke or replace a connection:** a revoked identity cannot be restored. Its slot becomes reusable after enforcement; a replacement gets a new identity. Revocation does not lower the purchased quantity.
- **Reduce quantity:** contact support to change purchased capacity, subject to the two-connection minimum. A mid-cycle reduction may create a prorated account credit. There is no automatic cash refund; hosted access remains limited to paid capacity.
- **Cancel:** use the billing portal workflow. Cancellation takes effect at the end of the paid period. Once the entitlement becomes inactive, new hosted access is suspended and active forwarding terminates. Local credentials and free client functionality remain available.
- **Request a refund:** [contact privately]({{ '/contact/' | relative_url }}) with the billing details. Requests are reviewed individually, subject to applicable law; a refund is not automatic.

### Support

Public bug reports and community questions are welcome for the free client. An RSS subscription includes help with problems in the hosted service, including connection enrollment, hosted forwarding and subscription access. We investigate reported service problems and work to resolve them.

Priority assistance, hands-on configuration, migration, agent integration and ongoing operational support can be arranged through a **separate paid support contract**. Contracts can cover a defined piece of work or ongoing support. Scope, fees, coverage hours, response targets, contacts and exclusions are agreed in writing before the contract begins. An RSS connection subscription does not itself include priority support or a service-level agreement.

See [Help & Support]({{ '/projects/Secrets-Kit/support/#support-options' | relative_url }}) for the support options and reporting routes, or [ask about a support contract]({{ '/collaborate/professionals/' | relative_url }}). Sensitive account or security matters belong in [private contact]({{ '/contact/' | relative_url }}).

The [website terms]({{ '/Policies/General_ToS/' | relative_url }}) govern the website; the RSS service terms above describe the hosted subscription. The client license below does not include a hosted-service entitlement.

<h2 id="client-license">Secrets Kit client license: MIT</h2>

The MIT License below covers the Secrets Kit client. It licenses the client software; it does not set subscription, refund, privacy or support terms. See also the {% include secrets-kit/doc-link.html kind='license' label='license in the versioned release repository' %}. Integration files and bundled dependencies can carry separate licenses.

> MIT License

> Copyright (c) 2026

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
