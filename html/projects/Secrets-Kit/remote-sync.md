---
layout: page
title: "Remote Secret Sync (RSS)"
permalink: /projects/Secrets-Kit/remote-sync/
published: true
secrets_kit_product: true
hide_banner_image: true
product_nav_order: 30
nav_title: RSS
image: /assets/images/projects/Secrets-Kit-Banner.png
excerpt: "Understand optional hosted forwarding for authorized Secrets Kit peers on separate networks."
---

{% include secrets-kit/release.html %}

Your workstation, a home server, and a remote machine do not always share a network. **Remote Secret Sync (RSS)** gives authorized Secrets Kit peers a forwarding path when they cannot communicate directly. Here, RSS means Remote Secret Sync; the site's blog subscription feed is a separate feature.

## Pay for connectivity when you need it

The free peer-to-peer client supports **unlimited connections on the same local area network (LAN) segment**, without a hosted subscription. Consider RSS when you need hosted forwarding across networks. Paid connection limits apply to RSS-enrolled connections; they do not cap free peer-to-peer connections on your LAN segment. RSS does not authorize unknown peers, replace your local datastore, or make every application on a machine eligible to receive credentials.

{% if seckit_release.production_release_ready %}Pricing is{% else %}Launch pricing is{% endif %} **$5 per enrolled connection per month, minimum two connections ($10/month)**. Read [Pricing]({{ '/projects/Secrets-Kit/pricing/' | relative_url }}) for the billing unit and lifecycle details.

## What travels through RSS {#what-travels-through-the-relay}

Secrets Kit encrypts a synchronization envelope for its destination peer before sending it. RSS forwards that encrypted envelope. It does not receive the secret plaintext, customer private keys, or local datastore encryption keys. Each receiving peer stores accepted records under its own local storage protection.

The service still processes the connection and account information needed to authenticate peers and operate forwarding. A statement about encrypted payloads is not a claim that every connection detail is hidden. See [Security & Privacy]({{ '/projects/Secrets-Kit/security/' | relative_url }}) for the boundaries.

Read the published [RSS privacy and retention summary]({{ '/projects/Secrets-Kit/policies/#remote-secrets-sync-privacy' | relative_url }}) and [service terms]({{ '/projects/Secrets-Kit/policies/#service-terms' | relative_url }}) for provider disclosures, retention, billing and cancellation.

## Primary and secondary RSS failover {#primary-and-secondary-relay-failover}

RSS provisions an ordered primary/secondary endpoint set. If an endpoint is unavailable, another authorized RSS endpoint can provide a forwarding path. A secondary must have the connection's authorization before it can accept it; failover does not bypass peer approval or subscription capacity.

Your local store and local credential use remain available when RSS is unavailable. RSS failover, cloud-region replication, and an offline cache are different features. Failover is not a promise of uninterrupted connections or a published recovery-time guarantee.

## Enrollment follows installation

The subscription workflow starts with an installed production client and a verified local workflow. {% if seckit_release.production_release_ready %}Enrollment begins from the installed product:

```bash
seckit rss checkout
```
{% else %}Enrollment and subscriptions are not open. The client checkout instructions will appear with the approved release.{% endif %}

Review the quantity and price shown by the returned checkout page. Completing checkout and enrolling a connection are separate steps; follow the {% include secrets-kit/doc-link.html file='RSS_CUSTOMER_GUIDE.md' label='customer guide' %} for enrollment, ownership claim, and offline recovery codes.

A browser success page alone does not prove that a connection is enrolled or that synchronization works. Secrets Kit grants capacity after payment verification and provisioning. Save recovery information privately, then verify RSS authentication and synchronization with disposable data.

## Add or replace a connection {#add-or-replace-a-connection}

From the enrolled billing owner's machine, check the registered connections and add a new host through the supported SSH workflow:

```bash
seckit rss devices list
seckit install user@host
```

The target creates its own RSS identity; do not copy private identity keys between machines. The optional non-SSH peer-invitation mailbox is not enabled in production. Peer invitations are separate from the retired beta Checkout invitations, and ordinary paid Checkout needs no invitation. The {% include secrets-kit/doc-link.html file='RSS_CUSTOMER_GUIDE.md#add-another-device' label='customer guide' %} covers enrollment and billing-owner recovery.

When purchased capacity is full, the billing owner runs `seckit rss billing units N` on an enrolled machine, reviews Stripe's adjustment and new monthly total, and explicitly confirms. Portal quantity changes remain disabled. Wait for verified payment and the new entitlement capacity before enrolling another connection. Creating another Checkout is not the normal way to add a machine.

To remove or replace a connection, choose its ID from `seckit rss devices list`, then run `seckit rss devices revoke CONNECTION_ID` on the billing owner's machine and confirm the prompt. Wait until both RSS endpoints enforce revocation; a `pending_enforcement` result does not release the slot yet. A different host with a new RSS identity can then enroll in the freed slot using `seckit install user@host`, without another payment. Revocation does not automatically reduce your bill; use `seckit rss billing units N` separately if you also want fewer paid connections.

**Re-adding a previously revoked profile:** reinstalling on that same user profile preserves its revoked RSS identity and does not enroll it again. The current client has no supported self-service command to replace that profile's RSS identity while preserving its local data. Do not delete its credentials or local store to force enrollment; [contact support privately]({{ '/contact/' | relative_url }}) for help. A normal reinstall of an *unrevoked* profile preserves its existing enrollment.

## Check the stage that failed

- **Installed but not enrolled:** check the enrollment result and the retained receipt workflow in the customer guide.
- **Enrolled but not connected:** check daemon supervision and authenticated RSS status. Saved configuration alone does not establish a live connection.
- **Connected but not synchronized:** check peer authorization, route readiness, and the disposable-record result on the receiving peer.
- **Capacity or payment problem:** inspect the existing subscription in the billing portal. Do not post payment receipts, recovery codes, or credential files in a support request.

Use [Guides]({{ '/projects/Secrets-Kit/guides/' | relative_url }}) for the reference links. For setup assistance across your own machines, [get in touch]({{ '/collaborate/professionals/' | relative_url }}).

