---
layout: page
title: "Get started with Secrets Kit"
permalink: /projects/Secrets-Kit/get-started/
published: true
secrets_kit_product: true
hide_banner_image: true
product_nav_order: 10
nav_title: Get Started
image: /assets/images/projects/Secrets-Kit-Banner.png
excerpt: "Give your agent the GitHub installation URL, or follow the production installation guide yourself."
---

{% include secrets-kit/navigation.html %}

{% if seckit_release.production_release_ready != true %}
<section id="release-status" class="seckit-release-status" aria-labelledby="seckit-release-title">
  <p class="home-kicker">The next release</p>
  <h2 id="seckit-release-title">Secrets Kit {{ seckit_version }} is coming soon.</h2>
  <p>Final testing is underway. The release brings free, unlimited peer-to-peer connections on the same LAN segment, selected credential access for applications and agents, and optional Remote Secrets Sync across networks.</p>
  <p>The production installer and hosted subscription are not available yet. We’ll link the release here when it is ready.</p>
  <div class="home-actions"><a class="home-button home-button--primary" href="{{ seckit_release.discussions_url }}">Follow release updates</a><a class="home-button" href="{{ '/projects/Secrets-Kit/compare/' | relative_url }}">Compare features</a></div>
</section>

## One URL for your agent

When {{ seckit_version }} is released, give Hermes the GitHub integration URL and ask it to follow the instructions there. Installation, verification, and integration details will live with that release in the repository. You won’t need a long setup prompt or a separate development checkout.

## Explore while we finish testing

Read [how Remote Secrets Sync works]({{ '/projects/Secrets-Kit/remote-sync/' | relative_url }}), review the [planned launch pricing]({{ '/projects/Secrets-Kit/pricing/' | relative_url }}), or compare [storage, key custody, and server dependence]({{ '/projects/Secrets-Kit/compare/' | relative_url }}). [Security & Privacy]({{ '/projects/Secrets-Kit/security/' | relative_url }}) explains the trust boundaries.

Existing testers should continue using their supplied test instructions. Report problems through [project Issues]({{ seckit_release.issues_url }}), ask questions in [project Discussions]({{ seckit_release.discussions_url }}), or use [Help & Support]({{ '/projects/Secrets-Kit/support/' | relative_url }}) to choose a private route.
{% else %}

The free peer-to-peer client supports unlimited connections on the same local area network (LAN) segment. Install it yourself, or let your agent follow the instructions on GitHub.

## Have your agent help

For Hermes, the [Secrets Kit integration on GitHub]({{ seckit_hermes_url }}) contains the installation and configuration instructions. Give your agent that URL and ask it to follow the instructions there.

<div class="seckit-prompt">
<label for="seckit-setup-prompt"><strong>Give this to your agent</strong></label>
<textarea id="seckit-setup-prompt" rows="3" readonly spellcheck="false">Read {{ seckit_hermes_url }} and follow the instructions to install and configure Secrets Kit for Hermes.</textarea>
<p><button class="seckit-copy" type="button" data-seckit-copy="seckit-setup-prompt" hidden>Copy installation request</button> <span id="seckit-copy-status" role="status" aria-live="polite"></span></p>
<noscript><p>Select the installation request above and copy it into your agent.</p></noscript>
</div>
<script src="{{ '/assets/js/secrets-kit-setup.js' | relative_url }}" defer></script>

For another agent, start with the [GitHub installation instructions]({{ seckit_readme_url }}). The Hermes-specific configuration belongs in the Hermes integration. Choose which credentials to make available during setup; installation and paid Remote Secrets Sync enrollment are separate choices.

## Install it yourself

Open the [Secrets Kit production release {{ seckit_release.release_tag }} on GitHub]({{ seckit_download_url }}) and follow the [installation instructions]({{ seckit_docs_url }}INSTALL.md). The release installer includes its verification and provisions its own runtime.

Use a supported macOS or Linux system and install as the operating-system user who will run your applications or agent. You do not need to set up Python, Git, or a development checkout first. Existing users should follow the guide's upgrade instructions to preserve their installation and data.

## Check your installation

Open a new terminal after installation, then run:

```bash
seckit --version
seckit doctor --install-check
```

The version should match the production release you selected, and the installation check should succeed. The GitHub guide covers troubleshooting and verification; there is no need to copy those instructions into an agent conversation.

## Choose what comes next

Use [Guides]({{ '/projects/Secrets-Kit/guides/' | relative_url }}) for everyday tasks and [Security & Privacy]({{ '/projects/Secrets-Kit/security/' | relative_url }}) for access choices. LAN peer-to-peer use is free. Read [Remote Sync]({{ '/projects/Secrets-Kit/remote-sync/' | relative_url }}) and [Pricing]({{ '/projects/Secrets-Kit/pricing/' | relative_url }}) if you need hosted connectivity across networks. For hands-on help, [ask about setup assistance]({{ '/collaborate/professionals/' | relative_url }}).
{% endif %}
