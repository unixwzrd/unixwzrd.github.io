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
excerpt: "Use the client for free and add optional Remote Secrets Sync at $5 per enrolled connection per month, minimum two."
---

{% include secrets-kit/navigation.html %}

The Secrets Kit peer-to-peer client is free, with **unlimited connections on the same local area network (LAN) segment**. Pay for Remote Secrets Sync when you need hosted forwarding between authorized peers across networks.

## Choose what you need

{% if seckit_release.production_release_ready %}The free client and optional Remote Secrets Sync subscription are available for {{ seckit_version }}.{% else %}These are the planned prices for the {{ seckit_version }} launch. Subscriptions are not open yet; release availability will be announced in [project Discussions]({{ seckit_release.discussions_url }}).{% endif %}

| | Free peer-to-peer client | Remote Secrets Sync |
| --- | --- | --- |
| Price | **$0** | **$5 per enrolled connection / month** |
| Minimum subscription | None | Two connections: **$10/month** |
| Local credential storage | Included | Uses the same local client |
| Selected application injection | Included | Uses the same local client |
| Supported agent interfaces | Included, with explicit configuration | Uses the same local client |
| Peer-to-peer connections on the same LAN segment | **Unlimited** | Still available through the free client |
| Hosted forwarding across networks | Not included | Included for enrolled, authorized connections |

The prices on this page are USD. Confirm the quantity, applicable taxes, and billing terms in checkout before subscribing.

## What is an enrolled connection?

For paid Remote Secrets Sync, an enrolled connection is a registered Secrets Kit identity associated with an operating-system user. Think of it as a participating Secrets Kit installation, rather than every application or agent that uses it. The purchased connection limit applies to RSS enrollment; free peer-to-peer connections on the same LAN segment are unlimited and do not require RSS enrollment.

A workstation and a remote server, each enrolled in RSS with one user identity, use two paid connections. Several agents using that same local Secrets Kit identity do not each create another subscription unit. Separate RSS-enrolled user identities on one physical computer can count separately. Supported deployment and platform constraints still apply.

| Purchased connections | Monthly base price |
| --- | --- |
| 2 | $10 |
| 3 | $15 |
| 5 | $25 |

These are base-price examples, not estimates of taxes or mid-cycle adjustments. The purchased quantity determines recurring capacity; an idle enrolled machine still occupies its slot.

## How to subscribe

{% if seckit_release.production_release_ready %}Start{% else %}Once {{ seckit_version }} and the service are released, start{% endif %} with [Get Started]({{ '/projects/Secrets-Kit/get-started/' | relative_url }}) and verify the production client. The subscription workflow begins with:

```bash
seckit rss checkout
```

The installed product supplies the checkout link. Review it before paying, then follow the enrollment and recovery steps in the {% include secrets-kit/doc-link.html file='RSS_CUSTOMER_GUIDE.md' label='customer guide' %}. There is no separate shopping cart on this website. A successful browser return does not itself establish paid capacity or an enrolled connection.

## Manage an existing subscription

Open the existing subscription's billing portal from the client:

```bash
seckit rss billing portal
```

Use it to review the available billing controls and quantity changes. If you need more capacity, change the quantity on that subscription and wait for verified payment and provisioning before adding another connection.

### Replacing or removing a machine

Revoke the old connection using the {% include secrets-kit/doc-link.html file='RSS_CUSTOMER_GUIDE.md#add-another-device' label='documented device workflow' %}. Revocation frees a slot once enforced, and a replacement enrolls with a new connection identity. **Revoking a connection does not lower the subscription quantity.** Reduce the purchased quantity separately in the billing portal if you want a lower recurring charge.

### Cancelling

Review the cancellation terms and effective date in the billing portal. When the entitlement becomes inactive through cancellation or payment failure, hosted forwarding stops according to the service lifecycle. Your local credentials and free client functionality remain available; direct synchronization still depends on authorized peers and a working direct route. Cancelling is separate from uninstalling the software or deleting local data.

## Need help getting set up?

[Ask about setup or migration assistance]({{ '/collaborate/professionals/' | relative_url }}). We can discuss the work your environment needs before agreeing a price. This is separate from the connection subscription and does not imply an enterprise support contract or an availability guarantee.

Want to see the alternatives first? Read [Compare]({{ '/projects/Secrets-Kit/compare/' | relative_url }}), or check [Security & Privacy]({{ '/projects/Secrets-Kit/security/' | relative_url }}) before deciding where to keep your credentials.
