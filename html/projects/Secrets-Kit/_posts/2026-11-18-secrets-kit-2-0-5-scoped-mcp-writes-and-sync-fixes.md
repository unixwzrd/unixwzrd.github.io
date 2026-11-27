---
layout: post
title: "Secrets-Kit 2.0.5 Released - Scoped MCP Writes, Sync Fixes, and Credential Export"
date: 2026-11-18 14:33:00 -0600
category: Secrets-Kit
content_type: update
release_version: "2.0.5"
release_status: released
permalink_slug: "secrets-kit-2-0-5-scoped-mcp-writes-and-sync-fixes"
short_link_basis: "/projects/Secrets-Kit/_posts/2026-11-18-secrets-kit-2-0-5-scoped-mcp-writes-and-sync-fixes.md"
short_url: "https://unixwzrd.ai/s/d756241670/"
tags: [secrets-management, local-first, security, developer-tools, ai-agents, open-source]
image: /assets/images/projects/Secrets-Kit-Banner.png
excerpt: "Secrets Kit 2.0.5 improves peer synchronization, hardens installed runtimes, adds opt-in scoped MCP writes and protected dotenv export, and makes preserving credentials during uninstall clearer."
published: true
---

**Secrets Kit 2.0.5 is available**, with improvements to peer synchronization, agent access, runtime isolation, and credential export. This release makes it easier to bring a new peer into an existing setup, give an agent precisely bounded write permissions when needed, and move selected credentials into another application without treating migration as an all-or-nothing exercise.

The free local-first client and free LAN synchronization remain the foundation. **Remote Secret Sync (RSS)** is still optional for authorized peers across networks; these client updates do not introduce a requirement to subscribe.

<!--more-->

[Product Overview](/projects/Secrets-Kit/) · [Get Started](/projects/Secrets-Kit/get-started/) · [Download Installer Script](https://github.com/unixwzrd/Secrets-Kit/releases/download/v2.0.5/install.sh)

## More reliable synchronization when a peer joins

We've corrected a case where a newly joined peer could remain unable to synchronize after other peers had accumulated updates. Pending endpoint history is now delivered to each authorized peer in transaction order, including when a later update has already been retried. The practical benefit is that joining a device should not leave it stuck behind history that other peers have already processed.

Peer authorization remains separate from discovery and synchronization. Finding a machine does not authorize it to receive credentials, and these fixes do not turn synchronization into a backup. Changes and deletions can propagate; keep recovery material and test your backups separately.

## Agent writes are optional, explicit, and scoped

**MCP access remains read-only by default.** Version 2 policies can explicitly permit creation, revision-checked updates, and revision-checked deletion for exact credential names within one owner-approved service and account. This is not a general grant for an agent to manage every credential in the store.

We've also tightened metadata listing so it remains within the configured service/account scope, including when another service uses the same credential name. The Hermes MCP launcher is pinned to its owner-approved policy, with checks that the policy, import scope, and credential allowlist agree. These boundaries belong in enforced configuration, not just instructions asking the agent to behave itself.

Value retrieval remains a separate decision. Keep it denied unless you deliberately want a credential returned to the model. **A credential supplied as a create or update tool argument is visible to the MCP host and may be visible to its agent or model.** Scoped MCP permissions are not a sandbox for other processes running under the same Unix account. The [v2.0.5 integration guide](https://github.com/unixwzrd/Secrets-Kit/blob/v2.0.5/docs/INTEGRATIONS.md#hermes-mcp-access) explains the policy and access boundaries.

{% include blog_diagram.html
   src="/assets/images/blog/secrets-kit/2026-11-18/scoped-mcp-writes.svg"
   alt="An owner-controlled policy selects read-only defaults or optional exact-name writes in one service and account. The agent host connects over stdio to seckit-mcp, which enforces the policy before using the local Unix domain socket to reach the daemon."
   caption="Read-only is the default; write grants require explicit owner approval. Policy enforcement stays in seckit-mcp, not the daemon. Write values may reach the model, and these grants do not isolate other processes using the same Unix account."
%}

## A cleaner runtime for the CLI and Hermes integration

The installed CLI, MCP server, and Hermes helpers are now isolated from inherited Python, Conda, native-loader, and OpenSSL environment settings. The Hermes launcher selects its runtime from the installed user location rather than accepting a caller-supplied runtime path. The integration's installer controller and verifier have also been updated for current release artifacts and daemon-health checks.

That reduces interference from whichever development environment happens to be active in a terminal. It does not make a compromised account safe or prevent an application from exposing a credential after receiving it.

## Export selected credentials and keep control of your exit

For applications that require `.env` files, Secrets Kit can now export selected stored credential values into a protected dotenv file. The command refuses values it cannot preserve in that format. The existing placeholder export remains available; exporting actual values is an explicit choice, not a new default.

**A dotenv export contains plaintext credentials.** Protect the file, keep it out of version control and shared locations, and verify the receiving application's actual loader before switching over. A successful export alone does not establish that the application will interpret every value correctly. Our updated human and agent instructions cover selected export, checking the replacement application, and uninstalling one host without discarding the original credentials prematurely.

Local uninstall now asks for confirmation by default. The `--yes` option is available for approved automation, but it does not bypass ownership, receipt, path, or active-service checks. The credential store and keys remain by default. Uninstalling a local client **does not cancel an RSS subscription or revoke enrolled devices**; those are separate actions.

## Clearer RSS device-replacement status

The client now distinguishes revocation that is still awaiting RSS enforcement from a slot that is ready for a replacement device. That distinction matters when changing devices: requesting revocation is not the same as having the released slot ready to reuse.

RSS pricing remains **US$5 per paid node slot per month, with a two-slot minimum of US$10/month**. Local use and authorized LAN synchronization are free. Purchasing capacity, enrolling a device, and authorizing a peer remain separate steps; see [Pricing](/projects/Secrets-Kit/pricing/) and the [RSS overview](/projects/Secrets-Kit/remote-sync/) for the workflow and service boundaries.

## Upgrade to the public stable release

Existing installations can use the documented preserving upgrade path:

```bash
seckit upgrade --check
seckit upgrade
```

For a new installation, use [Get Started](/projects/Secrets-Kit/get-started/) or the installer attached to the [public v2.0.5 release](https://github.com/unixwzrd/Secrets-Kit/releases/tag/v2.0.5). GitHub's source-code archives are not the customer installer. The [versioned installation guide](https://github.com/unixwzrd/Secrets-Kit/blob/v2.0.5/docs/INSTALL.md) and [changelog](https://github.com/unixwzrd/Secrets-Kit/blob/v2.0.5/CHANGELOG.md) provide the detailed instructions and release record.

If you encounter a problem, [contact us](/contact/) or [open a project issue](https://github.com/unixwzrd/Secrets-Kit/issues), keeping credentials and recovery material out of public reports. For deployment, migration, integrations, or ongoing maintenance, Distributed Thinking Systems also offers consulting and maintenance engagements under a separately agreed scope.


