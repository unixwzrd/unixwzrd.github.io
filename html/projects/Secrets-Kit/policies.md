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

Retention periods, the full service-provider list and the billing details marked below will be confirmed before RSS subscriptions open. Separately agreed support contracts define the scope and terms of any additional paid assistance.

<nav class="seckit-jumps" aria-label="Policy sections"><a href="#client-privacy">Client privacy</a><a href="#remote-secrets-sync-privacy">RSS privacy</a><a href="#retention-and-deletion">Retention &amp; deletion</a><a href="#service-terms">Service terms</a><a href="#client-license">MIT client license</a></nav>

<h2 id="client-privacy">Secrets Kit client privacy</h2>

Your configured local backend holds credentials and their service/account metadata. Local storage and identity keys remain with your operating-system user. Authorized peers can receive the records you authorize for synchronization. Applications receiving an injected credential receive plaintext and may expose it through their own behavior; an agent with command access may also inspect it. See [Security & Privacy]({{ '/projects/Secrets-Kit/security/' | relative_url }}) for those limitations.

Local/LAN use does not require an RSS subscription. Installation and updates contact distribution services for the selected software and runtime. Enabling hosted RSS, configuring an agent provider, or sending a support request introduces separate data paths; local storage is not a claim that every workflow stays entirely offline.

<h2 id="remote-secrets-sync-privacy">Remote Secrets Sync privacy</h2>

| Data path | What it handles | Boundary |
| --- | --- | --- |
| Secret synchronization | Destination-encrypted messages temporarily held in an in-memory queue for delivery | RSS does not intentionally persist these messages to disk and cannot decrypt them. Authorized receiving peers can decrypt their records. This statement concerns message payloads, not account or operational metadata. |
| Hosted access and billing | Account/subscription identifiers, billing contact/profile and invoice information, purchased quantity, entitlement and connection authorization | Service enrollment and billing-owner authority are separate from permission to receive another peer's secrets. |
| Connectivity and operational safety | Network connection information, connection/session identifiers and operational status | Encryption does not hide all metadata. The exact metadata fields, logging limits and retention periods are still to be confirmed. |
| Optional peer invitations | Encrypted onboarding messages for a short-lived invitation, held in separate persistent storage | This exchange is separate from the in-memory delivery queue. It cannot authorize a peer or decrypt the onboarding messages. Invitation expiry does not establish when stored copies or backups are erased. |
| Support | The information you choose to include in a report or private message | GitHub Issues and Discussions are public. Keep credentials, private keys, payment receipts and recovery material out of reports. |

Encrypted messages pass through an in-memory queue for RSS delivery; they are not intentionally persisted to disk. Operating-system swap or paging can still write memory contents to disk, so this does not mean ciphertext can never reach disk. The queue is not a durable delivery archive or recovery service.

Account, authorization, billing and operational metadata follow their own retention rules. The separate optional peer-invitation exchange uses persistent storage for encrypted onboarding messages; the in-memory delivery statement does not apply to that exchange.

### Service providers

Payments will use **Stripe-hosted Checkout and the billing portal**. Release downloads and versioned documentation will be available on **GitHub**, alongside public support discussions. Installation also downloads runtime and dependency files from their distribution services.

The full list of hosting, networking, email/support and monitoring providers, their processing locations and their retention responsibilities is still to be confirmed before RSS subscriptions open.

<h2 id="retention-and-deletion">Retention and deletion</h2>

Local data, keys, replicas, exports and backups need their own lifecycle. Cancelling hosted forwarding does not delete your local credentials. Synchronization can propagate changes and deletions, but it is not a guarantee of immediate erasure from backups or every authorized peer. Uninstalling software, revoking a connection, cancelling a subscription and requesting account-data deletion are separate actions.

**Retention and deletion rules are still to be confirmed before subscriptions open** for account/billing and authorization records, connection logs and metrics, support correspondence, invitation-message storage, and backups. An expired invitation cannot be used, but expiry does not establish when every stored copy or backup is erased. Account-erasure deadlines and any automatic deletion after cancellation are still to be confirmed.

For a privacy or deletion question, [contact us privately]({{ '/contact/' | relative_url }}) and identify Secrets Kit or RSS. Do not send secret values.

<h2 id="service-terms">Remote Secrets Sync service terms</h2>

The launch offer is **$5 per enrolled connection per month, minimum two connections ($10/month)**. The client remains free for local use and unlimited connections on the same LAN segment. An enrolled connection represents a registered client identity associated with an operating-system user; it is not a separate seat for each agent. [Pricing]({{ '/projects/Secrets-Kit/pricing/' | relative_url }}) explains the unit and examples.

Manage your connections and subscription separately:

- **Increase capacity:** use the existing subscription's billing portal, then wait for verified payment and provisioning before enrolling another connection.
- **Revoke or replace a connection:** a revoked identity cannot be restored. Its slot becomes reusable after enforcement; a replacement gets a new identity. Revocation does not lower the purchased quantity.
- **Reduce quantity:** change purchased quantity separately through the billing workflow. The final effective-date, proration/credit rules and treatment of already enrolled connections need confirmation; the two-connection minimum remains the stated offer.
- **Cancel:** use the billing portal workflow. Once cancellation makes the entitlement inactive, new hosted access is suspended and active forwarding terminates. Local credentials and free client functionality remain available. Whether cancellation takes effect immediately or at period end is still to be confirmed before subscriptions open.
- **Request a refund:** [contact privately]({{ '/contact/' | relative_url }}) for a billing question. Refund eligibility, time limits and any credit policy are still to be confirmed before subscriptions open.

### Support

Public bug reports and community questions are welcome for the free client. An RSS subscription includes help with problems in the hosted service, including connection enrollment, hosted forwarding and subscription access. We investigate reported service problems and work to resolve them.

Priority assistance, hands-on configuration, migration, agent integration and ongoing operational support can be arranged through a **separate paid support contract**. Contracts can cover a defined piece of work or ongoing support. Scope, fees, coverage hours, response targets, contacts and exclusions are agreed in writing before the contract begins. An RSS connection subscription does not itself include priority support or a service-level agreement.

See [Help & Support]({{ '/projects/Secrets-Kit/support/#support-options' | relative_url }}) for the support options and reporting routes, or [ask about a support contract]({{ '/collaborate/professionals/' | relative_url }}). Sensitive account or security matters belong in [private contact]({{ '/contact/' | relative_url }}).

The [website terms]({{ '/Policies/General_ToS/' | relative_url }}) govern the website. They are not a substitute for the final RSS subscription terms. The client license below does not include a hosted-service entitlement.

<h2 id="client-license">Secrets Kit client license: MIT</h2>

The MIT License below covers the Secrets Kit client. It licenses the client software; it does not set subscription, refund, privacy or support terms. The {% include secrets-kit/doc-link.html kind='license' label='license in the versioned release repository' %} will be available with the release. Integration files and bundled dependencies can carry separate licenses.

> MIT License

> Copyright (c) 2026

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
