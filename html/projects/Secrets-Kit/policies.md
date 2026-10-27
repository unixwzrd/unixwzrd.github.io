---
layout: page
title: "Secrets Kit privacy, license and service terms"
permalink: /projects/Secrets-Kit/policies/
published: true
secrets_kit_product: true
hide_banner_image: true
product_nav_order: 80
nav_title: Policies
excerpt: "Prelaunch privacy and service information scoped to Secrets Kit and Remote Secrets Sync, with unresolved terms clearly identified."
---

{% include secrets-kit/navigation.html %}

This page applies to the **Secrets Kit client and optional Remote Secrets Sync (RSS)**. The Safari extension's [General Privacy Policy]({{ '/Policies/General_Privacy/' | relative_url }}) describes that extension, not Secrets Kit. It does not establish the data practices of this website or the hosted RSS service.

**Prelaunch disclosure:** installation and subscriptions are not open. The data paths below are supported by the reviewed development implementation and customer documentation. The service policy is not final: retention periods, the complete provider list, and the commercial decisions identified below require approval before subscriptions open. No effective date or release date is promised here.

<nav class="seckit-jumps" aria-label="Policy sections"><a href="#client-privacy">Client privacy</a><a href="#remote-secrets-sync-privacy">RSS privacy</a><a href="#retention-and-deletion">Retention &amp; deletion</a><a href="#service-terms">Service terms</a><a href="#client-license">MIT client license</a></nav>

<h2 id="client-privacy">Secrets Kit client privacy</h2>

Your configured local backend holds credentials and their service/account metadata. Local storage and identity keys remain with your operating-system user. Authorized peers can receive the records you authorize for synchronization. Applications receiving an injected credential receive plaintext and may expose it through their own behavior; an agent with command access may also inspect it. See [Security & Privacy]({{ '/projects/Secrets-Kit/security/' | relative_url }}) for those limitations.

Local/LAN use does not require an RSS subscription. Installation and updates contact distribution services for the selected software and runtime. Enabling hosted RSS, configuring an agent provider, or sending a support request introduces separate data paths; local storage is not a claim that every workflow stays entirely offline.

<h2 id="remote-secrets-sync-privacy">Remote Secrets Sync privacy</h2>

| Data path | What it handles | Boundary |
| --- | --- | --- |
| Secret synchronization | Destination-encrypted envelopes and the connection/routing information needed to forward them | RSS forwarding does not receive secret plaintext, customer private keys, or local datastore keys. Authorized receiving peers can decrypt their records. |
| Hosted access and billing | Account/subscription identifiers, billing contact/profile and invoice information, purchased quantity, entitlement and connection authorization | Service enrollment and billing-owner authority are separate from permission to receive another peer's secrets. |
| Connectivity and operational safety | Network connection information, connection/session identifiers and operational status | Encryption does not hide all metadata. A final field-by-field inventory and logging/retention limits are still awaiting approval. |
| Optional peer-invitation mailbox | Encrypted onboarding messages for a short-lived invitation | This is distinct from secret-sync forwarding. The mailbox cannot authorize a peer or decrypt the onboarding messages. Invitation expiry is not a promise that every stored copy, log or backup is erased at that instant. |
| Support | The information you choose to include in a report or private message | GitHub Issues and Discussions are public. Keep credentials, private keys, payment receipts and recovery material out of reports. |

RSS secret-sync forwarding is not a durable secret archive, message queue, or recovery service. The separate invitation mailbox means that a blanket claim that no encrypted messages are ever stored would be inaccurate. Account, authorization and billing records are also distinct from synchronization payloads.

### Service providers

The documented payment workflow uses **Stripe-hosted Checkout and the billing portal**. **GitHub** is the prepared source for release artifacts, versioned documentation and public support discussions. These describe the intended release workflow; they do not mean subscriptions or an installer are available now. Runtime/dependency downloads also contact their distribution sources during installation.

The complete approved list of hosting, networking, email/support and any monitoring providers, their processing locations, and their retention responsibilities has not yet been confirmed for the production service. We will not describe an incomplete list as the full set of providers or promise that metadata never leaves a particular jurisdiction.

<h2 id="retention-and-deletion">Retention and deletion</h2>

Local data, keys, replicas, exports and backups need their own lifecycle. Cancelling hosted forwarding does not delete your local credentials. Synchronization can propagate changes and deletions, but it is not a guarantee of immediate erasure from backups or every authorized peer. Uninstalling software, revoking a connection, cancelling a subscription and requesting account-data deletion are separate actions.

**Before subscriptions open, the service policy still needs approved retention and deletion rules** for account/billing and authorization records, connection logs and metrics, support correspondence, invitation-message storage, and backups. The implementation's invitation expiry and cleanup behavior is not a customer-facing retention commitment. We cannot currently promise an account-erasure deadline or automatic deletion after cancellation.

For a privacy or deletion question, [contact us privately]({{ '/contact/' | relative_url }}) and identify Secrets Kit or RSS. Do not send secret values. The final policy must explain what can be deleted, what must be retained, why, and for how long.

<h2 id="service-terms">Remote Secrets Sync service terms — prelaunch</h2>

The planned offer is **$5 per enrolled connection per month, minimum two connections ($10/month)**. The client remains free for local use and unlimited connections on the same LAN segment. An enrolled connection represents a registered client identity associated with an operating-system user; it is not a separate seat for each agent. [Pricing]({{ '/projects/Secrets-Kit/pricing/' | relative_url }}) explains the unit and examples.

The documented lifecycle separates the following actions:

- **Increase capacity:** use the existing subscription's billing portal, then wait for verified payment and provisioning before enrolling another connection.
- **Revoke or replace a connection:** a revoked identity cannot be restored. Its slot becomes reusable after enforcement; a replacement gets a new identity. Revocation does not lower the purchased quantity.
- **Reduce quantity:** change purchased quantity separately through the billing workflow. The final effective-date, proration/credit rules and treatment of already enrolled connections need confirmation; the two-connection minimum remains the stated offer.
- **Cancel:** use the billing portal workflow. Once cancellation makes the entitlement inactive, new hosted access is suspended and active forwarding terminates. Local credentials and free client functionality remain available. Whether cancellation takes effect immediately or at period end is not yet an approved service term.
- **Request a refund:** [contact privately]({{ '/contact/' | relative_url }}) for a billing question. Refund eligibility, time limits and any credit policy have not been approved; this page does not promise a refund or describe a no-refund rule.

### Support

Use [project Issues]({{ seckit_release.issues_url }}) for bugs, [project Discussions]({{ seckit_release.discussions_url }}) for questions, and [private contact]({{ '/contact/' | relative_url }}) for sensitive account or security matters. See [Help & Support]({{ '/projects/Secrets-Kit/support/' | relative_url }}) for the reporting checklist. No support response-time, uptime or recovery-time commitment has been approved. Hands-on setup assistance is separately scoped through the existing professional-services inquiry route.

The [website terms]({{ '/Policies/General_ToS/' | relative_url }}) govern the website. They are not a substitute for the final RSS subscription terms. The client license below does not include a hosted-service entitlement.

<h2 id="client-license">Secrets Kit client license: MIT</h2>

The following text is reproduced from the development workspace's client `LICENSE`. It licenses the client software; it does not set subscription, refund, privacy or support terms. The {% include secrets-kit/doc-link.html kind='license' label='license in the versioned release repository' %} is prepared for release activation. Integration files and bundled dependencies can have their own licenses; the Hermes skill's metadata does not change the client's MIT license.

> MIT License

> Copyright (c) 2026

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
