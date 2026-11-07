---
layout: post
title: "Secrets-Kit 2.0.2 Released — Local Credentials, Free LAN Sync, Optional Remote Sync"
date: 2026-11-07 13:27:24 -0600
category: Secrets-Kit
content_type: update
permalink_slug: "secrets-kit-2-0-2-general-availability"
short_link_basis: "/projects/Secrets-Kit/_posts/2026-11-07-secrets-kit-2-0-2-general-availability.md"
short_url: "https://unixwzrd.ai/s/24c32740c2/"
tags: [secrets-management, local-first, security, developer-tools, ai-agents, open-source]
image: /assets/images/projects/Secrets-Kit-Banner.png
excerpt: "Distributed Thinking Systems releases Secrets Kit 2.0.2: a free local-first secrets client, free encrypted LAN synchronization, and optional Remote Secrets Sync at $5 per node per month."
published: true
---

Distributed Thinking Systems is announcing the general availability of **Secrets Kit 2.0.2**. The [public stable release](https://github.com/unixwzrd/Secrets-Kit/releases/tag/v2.0.2) brings together local credential storage, selected application access, and encrypted peer-to-peer synchronization. The client is free and open source, and synchronization between authorized peers on the same local network is free too. Optional **Remote Secrets Sync (RSS)** connects enrolled peers across networks when direct communication is unavailable.

<div class="home-actions">
  <a class="home-button home-button--primary" href="https://github.com/unixwzrd/Secrets-Kit/releases/download/v2.0.2/install.sh">Download Secrets-Kit 2.0.2</a>
  <a class="home-button" href="/projects/Secrets-Kit/get-started/">Get Started</a>
</div>

The download is the free client’s `install.sh` installer. Get Started covers supported platforms and installation instructions.

Version 2.0.2 is a substantial re-architecture of Secrets Kit, not simply an update to its earlier Keychain-based workflow. Encrypted SQLite provides the normal new-store and synchronization path, with independent local storage keys on each peer. macOS Keychain remains a supported backend; existing Keychain records do not automatically become synchronized SQLite records.

<!--more-->

## Free local storage and LAN synchronization

Secrets Kit keeps API keys, tokens, and passwords on your machines. Applications and scripts can receive selected credentials through `seckit run`, rather than keeping copies in shell scripts or project configuration files. That works for database clients, scheduled jobs, development tools, and agents; it is not an agent-only product. Hermes integration is available, but neither Hermes nor an AI service is required to use the client.

Authorized peers on the same LAN segment can synchronize through the free peer-to-peer client, with unlimited LAN connections and no hosted subscription. Local credential access does not depend on a hosted vault. Each peer retains its own storage protection, and discovering another machine does not grant it permission to receive secrets.

## Remote Secrets Sync when your machines are on different networks

RSS is an optional paid service for authorized peers that cannot communicate directly across network boundaries. It carries synchronization payloads encrypted for their destination. **Your private encryption keys stay with you. We do not receive them, and RSS cannot decrypt your synchronized secret payloads.** Local access and authorized LAN synchronization remain available independently of RSS.

Subscription enrollment is open and **does not require an invitation or access code**. Follow the installed client's documented checkout and enrollment workflow; purchasing capacity and authorizing a peer are separate steps.

RSS costs **US$5 per node per month, with a two-node minimum of US$10/month**. Each additional enrolled node adds US$5/month. For billing, a node is an RSS-enrolled Secrets Kit identity associated with an operating-system user—not each application or agent using that identity. Separate enrolled user identities on one physical machine can count separately. The [pricing page](/projects/Secrets-Kit/pricing/) explains capacity, examples, and subscription management.

Synchronization messages are handled transiently in memory, rather than retained as a cloud copy of your secret store. Account and operational metadata have separate retention rules. An optional encrypted peer-invitation mailbox is a different feature and is not currently configured in production. Our [Security & Privacy overview](/projects/Secrets-Kit/security/) and [service policies](/projects/Secrets-Kit/policies/#remote-secrets-sync-privacy) describe those distinctions and the operating-system limitations.

## Protect the credential—and choose what receives it

Secrets Kit reduces the need for scattered credential copies; it does not make the receiving process trustworthy. An application supplied with a credential receives its plaintext value and can log, expose, or transmit it. Agents with sufficient system access can do the same. Optional policy-scoped MCP access also requires an explicit decision about whether a value may enter model context.

Synchronization is not a backup. Changes and deletions can propagate, so local keys, recovery material, and tested backups remain important. Start with a disposable credential and verify application access and peer authorization before moving an existing workflow.

## Install the public release

Secrets Kit 2.0.2 is available for macOS and supported glibc-based Linux systems. Begin with [Get Started](/projects/Secrets-Kit/get-started/), follow the [versioned installation guide](https://github.com/unixwzrd/Secrets-Kit/blob/v2.0.2/docs/INSTALL.md), or download the installer from the [stable v2.0.2 release](https://github.com/unixwzrd/Secrets-Kit/releases/tag/v2.0.2). The release includes the managed installer; GitHub's source-code archives are not the customer installation path.

The [product overview](/projects/Secrets-Kit/) explains the local-first workflow, [Guides](/projects/Secrets-Kit/guides/) cover everyday tasks, and [Pricing](/projects/Secrets-Kit/pricing/) explains when paid RSS is useful. You can begin with one local application and add LAN peers without subscribing to anything. Add RSS only when you need the cross-network connection.
