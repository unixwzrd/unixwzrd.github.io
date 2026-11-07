---
permalink_slug: "secrets-kit-2-0-2-local-secrets-peer-to-peer-sync"
short_link_basis: "/projects/Secrets-Kit/_posts/2026-10-28-secrets-kit-2-0-2-local-secrets-peer-to-peer-sync.md"
short_url: "https://unixwzrd.ai/s/48b996c9bb/"
layout: post
title: "Secrets Kit 2.0.2 — Local Secrets, Encrypted Peer-to-Peer Sync"
date: 2026-10-28
category: Secrets-Kit
content_type: update
tags: [secrets-management, local-first, security, developer-tools, ai-agents, open-source]
excerpt: "Secrets Kit 2.0.2 is available with encrypted local SQLite storage, free LAN peer-to-peer synchronization, selected application access, and optional Remote Secrets Sync across networks."
image: /assets/images/projects/Secrets-Kit-Banner.png
published: true
---

**Update November 7, 2026: Secrets Kit 2.0.2 is available.** The release combines encrypted SQLite storage, authorized peer-to-peer synchronization, and optional remote connectivity: keep credentials on your devices and provide selected values to the applications that need them.

The free client supports unlimited peer-to-peer connections on the same local area network segment. There is no hosted vault to retrieve your credentials from, and local credential use does not depend on a cloud service. Optional **Remote Secrets Sync (RSS)** connects authorized peers across networks when direct connectivity is unavailable.

Download the [stable v2.0.2 release](https://github.com/unixwzrd/Secrets-Kit/releases/tag/v2.0.2) or follow [Get Started](/projects/Secrets-Kit/get-started/). Production RSS subscriptions use the same account and infrastructure for stable and opt-in beta clients; paying customers do not need invitations.

<!--more-->

## A Local Store Built for Multiple Machines

Earlier releases centered on macOS Keychain. Version 2.0.2 makes **encrypted SQLite** the normal new-store workflow and the foundation for synchronization on macOS and Linux. Keychain remains a supported macOS backend, but its items do not automatically become synchronized SQLite records.

Each peer keeps its own local storage key. The sender protects a synchronization record for its authorized destination; the receiver decrypts the envelope and stores accepted records under its own local protection. Your machines do not share one datastore encryption key.

Discovering a machine does not authorize it to receive credentials. An RSS subscription does not grant access to another peer's secrets either.

## Credentials for Applications, Not Just Agents

Secrets Kit works with database clients, scheduled jobs, deployment scripts, and applications that accept credentials through environment variables. With credentials already stored, `seckit run` supplies selected values to the child process rather than embedding them in scripts or command-line arguments:

~~~sh
seckit run --service postgres --account development --names PGPASSWORD -- psql -h localhost -U app -d appdb
seckit run --service redis --account development --names REDISCLI_AUTH -- redis-cli -h localhost PING
~~~

These illustrate the workflow, not installation instructions. Programs requiring password files still need their documented file interface; Secrets Kit does not rewrite their configuration automatically.

Agents can use the same process-launch approach. Hermes integration and optional policy-scoped, read-only MCP access provide additional paths, but neither is required. Retrieving a value into model context remains a separate permission decision.

**A process receiving a credential receives plaintext.** It can log it, expose its environment, or pass it onward. An agent with sufficient command access can inspect or leak it too. Secrets Kit reduces credential sprawl; it cannot make an application trustworthy or protect a compromised account.

## Free Peer-to-Peer Synchronization on Your LAN

Authorized workstations and servers on the same LAN segment synchronize directly without a hosted subscription. Records stay in local stores, with synchronization envelopes encrypted for their destination. A home server or lab does not need RSS for everyday local access.

{% include blog_diagram.html
   src="/assets/images/blog/secrets-kit/2026-10-28/local-store-and-lan-sync.svg"
   alt="Encrypted local stores and application credentials on two authorized Secrets Kit LAN peers"
   caption="Local storage and application access remain on each peer. Free LAN synchronization does not require Remote Secrets Sync." %}

Synchronization is not a backup: changes and deletions can propagate. Protect local keys, backups, and recovery procedures separately.

## Remote Secrets Sync When Networks Get in the Way

Home, office, lab, and VPS systems do not always have a usable direct route. RSS connects those systems using synchronization envelopes already encrypted for the destination peer. **Your private encryption keys stay with you. We do not receive them, and RSS cannot decrypt your synchronized secret payloads.** Only the authorized destination peer decrypts those payloads and stores accepted records under its own local storage key.

{% include blog_diagram.html
   src="/assets/images/blog/secrets-kit/2026-10-28/remote-sync-boundary.svg"
   alt="Remote Secrets Sync forwards destination-encrypted envelopes without decrypting their secret payload"
   caption="The destination-encrypted payload remains protected throughout RSS delivery. Transport encryption is separate from payload encryption; private encryption and local storage keys remain with the peers." %}

RSS handles secret synchronization messages transiently in memory, rather than keeping a cloud copy of your secret store. It does not intentionally persist these encrypted payloads to disk. Account and operational metadata and the separate encrypted invitation exchange have their own storage rules; the [security overview](/projects/Secrets-Kit/security/) and [privacy summary](/projects/Secrets-Kit/policies/#remote-secrets-sync-privacy) cover those distinctions, including operating-system paging limitations.

An ordered primary/secondary RSS endpoint set provides connection failover. Cross-network synchronization through RSS requires service availability, but an RSS outage does not remove your local credentials or stop local credential use and authorized LAN synchronization.

### Pay for Remote Connectivity, Not Every Agent

Launch pricing is **US$5 per RSS-enrolled connection per month**, with a two-connection minimum of **US$10/month**. Each additional enrolled connection adds US$5/month. Free LAN peer-to-peer connections remain unlimited.

An enrolled connection is a registered Secrets Kit identity associated with an operating-system user—not each application or agent. A workstation and a server with one enrolled identity each use two connections; separate enrolled users on one machine can count separately. See [Pricing](/projects/Secrets-Kit/pricing/).

## Get Started

The stable client and documentation are published for macOS and Linux. Further integrations and capabilities are planned separately.

Explore the [product overview](/projects/Secrets-Kit/), [setup instructions](/projects/Secrets-Kit/get-started/), and [feature comparison](/projects/Secrets-Kit/). The result is local custody, explicit access, and optional remote connectivity without a cloud-hosted secret vault.
