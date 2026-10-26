---
layout: page
title: "Remote Secrets Sync"
permalink: /projects/Secrets-Kit/remote-sync/
published: true
secrets_kit_product: true
hide_banner_image: true
product_nav_order: 30
nav_title: Remote Sync
image: /assets/images/projects/Secrets-Kit-Banner.png
excerpt: "Understand optional hosted forwarding for authorized Secrets Kit peers on separate networks."
---

{% include secrets-kit/navigation.html %}

Your workstation, a home server, and a remote machine do not always share a network. **Remote Secrets Sync (RSS)** gives authorized Secrets Kit peers a forwarding path when they cannot communicate directly. Here, RSS means Remote Secrets Sync; the site's blog subscription feed is a separate feature.

## Pay for connectivity when you need it

The free peer-to-peer client supports **unlimited connections on the same local area network (LAN) segment**, without a hosted subscription. Consider RSS when you need hosted forwarding across networks. Paid connection limits apply to RSS-enrolled connections; they do not cap free peer-to-peer connections on your LAN segment. RSS does not authorize unknown peers, replace your local datastore, or make every application on a machine eligible to receive credentials.

Remote Secrets Sync costs **$5 per enrolled connection per month, minimum two connections ($10/month)**. Read [Pricing]({{ '/projects/Secrets-Kit/pricing/' | relative_url }}) for the billing unit and lifecycle details.

## What travels through the relay

Secrets Kit encrypts a synchronization envelope for its destination peer before sending it. The relay forwards that encrypted envelope. It does not receive the secret plaintext, customer private keys, or local datastore encryption keys. Each receiving peer stores accepted records under its own local storage protection.

The service still processes the connection and account information needed to authenticate peers and operate forwarding. A statement about encrypted payloads is not a claim that every connection detail is hidden. See [Security & Privacy]({{ '/projects/Secrets-Kit/security/' | relative_url }}) for the boundaries.

## Primary and secondary relay failover

RSS provisions an ordered primary/secondary relay set. If an endpoint is unavailable, another authorized relay can provide a forwarding path. A secondary must have the connection’s authorization before it can accept it; failover does not bypass peer approval or subscription capacity.

Your local store and local credential use remain available when hosted forwarding is unavailable. Relay failover, cloud-region replication, and an offline cache are different features. Failover is not a promise of uninterrupted connections or a published recovery-time guarantee.

## Enrollment follows installation

{% if seckit_release.production_release_ready %}Install{% else %}When version {{ seckit_version }} and the hosted service are released, install{% endif %} the production client and verify the local workflow. Enrollment begins from the installed product:

```bash
seckit rss checkout
```

Review the quantity and price shown by the returned checkout page. Completing checkout and enrolling a connection are separate steps; follow the {% include secrets-kit/doc-link.html file='RSS_CUSTOMER_GUIDE.md' label='customer guide' %} for enrollment, ownership claim, and offline recovery codes.

A browser success page alone does not prove that a connection is enrolled or that forwarding works. Secrets Kit grants capacity after payment verification and provisioning. Save recovery information privately, then verify relay authentication and synchronization with disposable data.

## Add or replace a connection

The customer guide explains adding a peer from the enrolled billing owner's machine using the normal SSH installation workflow. The target creates its own identity. You do not copy private identity keys between machines.

When purchased capacity is full, increase the quantity on the existing subscription through the billing portal and wait for verified capacity before retrying. Creating another checkout is not the normal way to add a machine. For a replacement, revoke the old connection and enroll the new identity into the freed slot; revocation does not automatically reduce your bill.

## Check the stage that failed

- **Installed but not enrolled:** check the enrollment result and the retained receipt workflow in the customer guide.
- **Enrolled but not connected:** check daemon supervision and authenticated relay status. Saved configuration alone does not establish a live connection.
- **Connected but not synchronized:** check peer authorization, route readiness, and the disposable-record result on the receiving peer.
- **Capacity or payment problem:** inspect the existing subscription in the billing portal. Do not post payment receipts, recovery codes, or credential files in a support request.

Use [Guides]({{ '/projects/Secrets-Kit/guides/' | relative_url }}) for the reference links. For setup assistance across your own machines, [get in touch]({{ '/collaborate/professionals/' | relative_url }}).
