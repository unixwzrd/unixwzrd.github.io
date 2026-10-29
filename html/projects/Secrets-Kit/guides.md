---
layout: page
title: "Secrets Kit user guides"
permalink: /projects/Secrets-Kit/guides/
published: true
secrets_kit_product: true
hide_banner_image: true
product_nav_order: 20
nav_title: Guides
image: /assets/images/projects/Secrets-Kit-Banner.png
excerpt: "Find the next task: store a credential, run an application, configure an agent, connect a peer, or recover your setup."
---

{% include secrets-kit/navigation.html %}

{% if seckit_release.production_release_ready != true %}
## Plan your first workflow

The version {{ seckit_version }} user guides and agent integration will accompany the release. While final testing finishes, here is where to start:

| Your goal | What to explore now |
| --- | --- |
| Keep credentials on your own machines | [Local storage and access boundaries]({{ '/projects/Secrets-Kit/security/' | relative_url }}) |
| Connect workstations on one LAN segment | [The free peer-to-peer client]({{ '/projects/Secrets-Kit/' | relative_url }}) — unlimited connections on the same segment |
| Connect authorized peers across networks | [Remote Secrets Sync and relay failover]({{ '/projects/Secrets-Kit/remote-sync/' | relative_url }}) |
| Let Hermes help with installation | [Agent-assisted setup preview]({{ '/projects/Secrets-Kit/get-started/' | relative_url }}) |
| Compare custody, recovery, and service dependence | [The feature comparison and wider landscape]({{ '/projects/Secrets-Kit/compare/' | relative_url }}) |
| Ask a question or report a tester problem | [Help & Support]({{ '/projects/Secrets-Kit/support/' | relative_url }}) |

Follow [Blog & Updates]({{ seckit_updates_url }}) for release updates. Detailed installation and command references will become active here when the production release is available.
{% else %}


Pick the task you need. The links below follow the production release selected for this site, so its commands, integration, and documentation stay together. Start with [Get Started]({{ '/projects/Secrets-Kit/get-started/' | relative_url }}) if this is your first installation.

## Store and use credentials

| I want to… | Start here | What to check |
| --- | --- | --- |
| Add a credential | [Usage]({{ seckit_docs_url }}USAGE.md) | Choose a service, account, and name. Supply values through the documented input path, without pasting real values into an agent transcript. |
| Give an application selected credentials | [Application examples]({{ seckit_docs_url }}EXAMPLES.md) | Use `seckit run` with the intended scope and names. Confirm the application uses that source without printing values. |
| Avoid repeating the same scope | [Defaults]({{ seckit_docs_url }}DEFAULTS.md) | Review configured defaults before running a command in another project. |
| Find a command or option | [CLI reference]({{ seckit_docs_url }}CLI_REFERENCE.md) | Use the reference for your installed version. |

A service and account let you keep the same name, such as `API_TOKEN`, in separate scopes. Choose names that make the intended use clear. A process receives the selected plaintext values in its environment, so its logging and child-process behavior still matter.

## Configure an agent

For Hermes, give your agent the [integration URL]({{ seckit_hermes_url }}) and ask it to follow the instructions there. [Get Started]({{ '/projects/Secrets-Kit/get-started/#have-your-agent-help' | relative_url }}) provides the short handoff. Preserve the existing agent configuration and `.env` file until you explicitly approve a cutover. A successful request using an old environment fallback does not establish that the integration is reading Secrets Kit.

For other applications and agents, read [Integrations]({{ seckit_docs_url }}INTEGRATIONS.md). General command-line compatibility is different from a verified agent-specific integration. Optional MCP access is read-only and policy-scoped; permission to retrieve a value into model context requires its own decision.

## Connect another machine

Authorize the peer before expecting synchronization. The free peer-to-peer client provides unlimited connections on the same local area network (LAN) segment, without a hosted subscription. For machines on separate networks, [Remote Sync]({{ '/projects/Secrets-Kit/remote-sync/' | relative_url }}) explains the optional hosted service and links to the [customer workflow]({{ seckit_docs_url }}RSS_CUSTOMER_GUIDE.md).

The [installation guide]({{ seckit_docs_url }}INSTALL.md#remote-install) covers remote installation over SSH. Installation, authorization, and a working synchronization route are separate checks. First verify with a disposable value, and never send another machine your local datastore encryption key to make synchronization work.

## Update, back up, recover, or leave

| Task | Reference | Before you start |
| --- | --- | --- |
| Update an existing installation | [Upgrade]({{ seckit_docs_url }}INSTALL.md#upgrade) | Keep your existing store and identity. Check the version and approved channel; do not initialize or enroll again as part of an ordinary update. |
| Make a backup or transfer records | [Workflows]({{ seckit_docs_url }}WORKFLOWS.md) and [CLI reference]({{ seckit_docs_url }}CLI_REFERENCE.md) | Review the export format and encryption options. Treat exports and recovery material as sensitive. Test recovery with disposable data first. |
| Recover hosted-account ownership | [RSS recovery]({{ seckit_docs_url }}RSS_CUSTOMER_GUIDE.md#revocation-and-recovery) | You need the saved account information and an offline recovery code. Recovery does not restore a revoked connection. |
| Replace a machine or change paid capacity | [Pricing]({{ '/projects/Secrets-Kit/pricing/' | relative_url }}) | Revocation frees a slot; reducing the subscription quantity is a separate billing action. |
| Uninstall | [CLI reference]({{ seckit_docs_url }}CLI_REFERENCE.md) | Review the state-preservation and explicit deletion options for your version. Uninstalling software and cancelling a subscription are separate actions. |

## When something fails

Start with the [installation troubleshooting guide]({{ seckit_docs_url }}INSTALL.md#troubleshooting). A healthy local installation, a healthy daemon, peer authorization, relay authentication, and successful synchronization establish different things. Check the stage that failed before repeating setup or buying another connection.

When asking for help, include the installed version, platform, command, and sanitized error. Leave out secret values, environment dumps, credential files, private keys, and recovery codes. For hands-on help, [ask about setup assistance]({{ '/collaborate/professionals/' | relative_url }}).

{% endif %}
