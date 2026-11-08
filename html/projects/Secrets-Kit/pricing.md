---
layout: page
title: "Secrets Kit pricing"
permalink: /projects/Secrets-Kit/pricing/
published: true
secrets_kit_product: true
hide_banner_image: true
product_nav_order: 40
nav_title: Pricing
image: /assets/images/projects/Secrets-Kit-Banner.png
excerpt: "Use the client for free and add optional Remote Secret Sync at $5 per enrolled connection per month, minimum two."
---

{% include secrets-kit/release.html %}

The Secrets Kit peer-to-peer client is free, with **unlimited connections on the same local area network (LAN) segment**. The Remote Secret Sync offer adds hosted forwarding between authorized peers across networks.

## Choose what you need

{% if seckit_release.production_release_ready %}The free client and optional Remote Secret Sync subscription are available for {{ seckit_version }}.{% else %}These are the launch prices for Secrets Kit {{ seckit_version }}. Subscriptions are not open yet; follow [release updates]({{ seckit_updates_url }}) for availability.{% endif %}

{% include secrets-kit/offer-cards.html %}

| | Free peer-to-peer client | Remote Secret Sync |
| --- | --- | --- |
| Price | **$0** | **$5 per enrolled connection / month** |
| Minimum subscription | None | Two connections: **$10/month** |
| Local credential storage | Included | Uses the same local client |
| Selected application injection | Included | Uses the same local client |
| Supported agent interfaces | Included, with explicit configuration | Uses the same local client |
| Peer-to-peer connections on the same LAN segment | **Unlimited** | Still available through the free client |
| Hosted forwarding across networks | Not included | Included for enrolled, authorized connections |

The prices on this page are USD. Confirm the quantity, applicable taxes, and billing terms in checkout before subscribing.
The stable client and opt-in public beta use the same production RSS subscription, entitlement and enrolled devices. Installing a beta client does not require an invitation or a second subscription. Hosted RSS access requires a verified paid subscription and authorized device.

## What is an enrolled connection?

For paid Remote Secret Sync, an enrolled connection is a registered Secrets Kit identity associated with an operating-system user. Think of it as a participating Secrets Kit installation, rather than every application or agent that uses it. The purchased connection limit applies to RSS enrollment; free peer-to-peer connections on the same LAN segment are unlimited and do not require RSS enrollment.

A workstation and a remote server, each enrolled in RSS with one user identity, use two paid connections. Several agents using that same local Secrets Kit identity do not each create another subscription unit. Separate RSS-enrolled user identities on one physical computer can count separately. Supported deployment and platform constraints still apply.

| Purchased connections | Monthly base price |
| --- | --- |
| 2 | $10 |
| 3 | $15 |
| 5 | $25 |

These are base-price examples, not estimates of taxes or mid-cycle adjustments. The purchased quantity determines recurring capacity; an idle enrolled machine still occupies its slot.

## How to subscribe

Start with [Get Started]({{ '/projects/Secrets-Kit/get-started/' | relative_url }}) and verify the production client. {% if seckit_release.production_release_ready %}The subscription workflow begins with:

```bash
seckit rss checkout
```
{% else %}**Subscription enrollment is not open.** The installed client provides the checkout workflow; there is no active purchase link or subscription command to run from this page.{% endif %}

The installed product supplies the checkout link. Review it before paying, then follow the enrollment and recovery steps in the {% include secrets-kit/doc-link.html file='RSS_CUSTOMER_GUIDE.md' label='customer guide' %}. There is no separate shopping cart on this website. A successful browser return does not itself establish paid capacity or an enrolled connection.

## Manage an existing subscription

{% if seckit_release.production_release_ready %}Open the existing subscription's billing portal from the client:

```bash
seckit rss billing portal
```
{% else %}The installed client opens an existing subscription's Stripe-hosted billing portal. Production subscriptions and their billing controls are not open yet.{% endif %}

Use the portal to manage payment methods, view invoices and cancel at the end of the paid period. Self-service quantity changes are disabled for the initial GA offer. To add capacity, contact support for a change to the existing subscription; additions are prorated and invoiced. Wait for verified payment and provisioning before enrolling another connection.

### Replacing or removing a machine

Revoke the old connection using the {% include secrets-kit/doc-link.html file='RSS_CUSTOMER_GUIDE.md#add-another-device' label='documented device workflow' %}. Revocation frees a slot once enforced, and a replacement enrolls with a new connection identity. **Revoking a connection does not lower the subscription quantity.** Contact support to reduce purchased units; the two-connection minimum remains in force. A mid-cycle reduction may create a prorated account credit, not an automatic cash refund.

### Cancelling

Cancellation through the billing portal takes effect at the end of the paid period. Hosted access remains subject to the active entitlement until then; when the entitlement becomes inactive through cancellation or payment failure, new hosted access is suspended and active forwarding terminates. Refund requests are reviewed individually, subject to applicable law; no cash refund is automatic. Read the [RSS service terms]({{ '/projects/Secrets-Kit/policies/#service-terms' | relative_url }}) for details. Your local credentials and free client functionality remain available; direct synchronization still depends on authorized peers and a working direct route. Cancelling is separate from uninstalling the software or deleting local data.

## Setup and support contracts

Your RSS subscription includes help with problems in the hosted service. Priority assistance, setup, migration, agent integration and ongoing operational support can be arranged separately through a paid support contract. Choose a defined project or discuss an ongoing agreement; scope, pricing, coverage and response targets are agreed in writing.

[Explore support options]({{ '/projects/Secrets-Kit/support/#support-options' | relative_url }}) or [contact us about a maintenance contract or consulting assistance]({{ '/contact/' | relative_url }}). Contract fees are separate from the per-connection subscription.

Want to see the alternatives first? Read [Compare]({{ '/projects/Secrets-Kit/compare/' | relative_url }}), or check [Security & Privacy]({{ '/projects/Secrets-Kit/security/' | relative_url }}) before deciding where to keep your credentials.
