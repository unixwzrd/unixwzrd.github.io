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

Choose the manual route or let an agent help. **Hermes is optional**; the client also works with applications, scripts, and other agents.

<nav class="seckit-jumps" aria-label="Setup sections"><a href="#have-your-agent-help">Agent-assisted setup</a><a href="#install-it-yourself">Manual setup</a><a href="#compatibility">Compatibility &amp; prerequisites</a><a href="#license">Client license</a></nav>

{% unless seckit_release.production_release_ready %}
<p id="release-status">These pages describe the upcoming {{ seckit_version }} release. Installation and subscriptions are not open. Existing testers should continue using their supplied test instructions.</p>
{% endunless %}

## Have your agent help

{% unless seckit_release.production_release_ready %}When the release is available, give{% else %}Give{% endunless %} your agent the official GitHub instructions and ask it to follow them. Hermes has an integration guide; another agent can use the general installation guide.

{% if seckit_release.production_release_ready %}

The [Hermes integration]({{ seckit_hermes_url }}) keeps installation, configuration, and verification together.

<div class="seckit-prompt">
<label for="seckit-setup-prompt"><strong>Give this to your agent</strong></label>
<textarea id="seckit-setup-prompt" rows="3" readonly spellcheck="false">Read {{ seckit_hermes_url }} and follow the instructions to install and configure Secrets Kit for Hermes.</textarea>
<p><button class="seckit-copy" type="button" data-seckit-copy="seckit-setup-prompt" hidden>Copy installation request</button> <span id="seckit-copy-status" role="status" aria-live="polite"></span></p>
<noscript><p>Select the installation request above and copy it into your agent.</p></noscript>
</div>
<script src="{{ '/assets/js/secrets-kit-setup.js' | relative_url }}" defer></script>

For another agent, use the [GitHub installation instructions]({{ seckit_readme_url }}).
{% else %}

The {% include secrets-kit/doc-link.html kind='hermes' label='Hermes integration' %} and {% include secrets-kit/doc-link.html file='INSTALL.md' label='general installation guide' %} are not public installation links yet. Setup instructions will be available with the release.
{% endif %}

Preserve existing data, agent configuration, and `.env` files. Choose explicitly which credentials to import or make available. Installing the client, migrating credentials, allowing agent access, and enrolling in paid RSS are separate decisions. Model-visible retrieval through the optional Model Context Protocol interface needs its own permission.

## Install it yourself

No agent is needed. The manual route uses the release's single-file `install.sh`: download it from the official release page, review the installation guide, and run it as the operating-system user who will use Secrets Kit. A repository source archive is not the installer. The installer provisions its own runtime and verifies its embedded application assets; obtain it from the trusted release link.

{% if seckit_release.production_release_ready %}

Open the [Secrets Kit {{ seckit_version }} release]({{ seckit_download_url }}) and follow the [installation guide]({{ seckit_docs_url }}INSTALL.md). After installation, open a new terminal and check:

```bash
seckit --version
seckit doctor --install-check
```

The version should match the selected release. Use a disposable credential to verify application access and peer synchronization without displaying its value. An installation check alone does not establish that an agent is reading Secrets Kit.
{% else %}

**The {{ seckit_version }} installer is forthcoming.** The {% include secrets-kit/doc-link.html file='INSTALL.md' label='manual installation guide' %} will be available with the release. You can [follow release updates]({{ seckit_updates_url }}) while testing continues.
{% endif %}

<h2 id="compatibility">Planned platform support</h2>

{% unless seckit_release.compatibility.approved_for_202 %}
Final compatibility, including minimum versions, will be confirmed before the {{ seckit_version }} release.
{% endunless %}

| Operating system | Planned version support | Architecture |
| --- | --- | --- |
{% for target in seckit_release.compatibility.targets %}| {{ target.system }} | {{ target.version }} | {{ target.architecture }} |
{% endfor %}

Windows and Linux ARM are not included in the planned customer installer support.

Installer prerequisites:

- Bash, standard platform utilities, and `curl` or `wget`.
- Network access for the first installation, including runtime and dependency downloads.
- Installation under the intended operating-system user; the normal per-user route does not use `sudo`.
- **No preinstalled Python, UV, Git, or development checkout is required.** The installer provisions Python 3.12. Custom development installation routes can have different requirements.

Background synchronization on Linux uses the user's service manager. Running while that user is logged out may require administrator-enabled user lingering. Confirm this for the target environment before relying on unattended operation.

<h2 id="license">Client license</h2>

The Secrets Kit client is licensed under the **MIT License**. Read the [applicable client license]({{ '/projects/Secrets-Kit/policies/#client-license' | relative_url }}). The {% include secrets-kit/doc-link.html kind='license' label='versioned repository license' %} will accompany the release. The optional hosted RSS subscription has separate [service terms]({{ '/projects/Secrets-Kit/policies/#service-terms' | relative_url }}); the client license does not promise hosted service or support.

## Choose what comes next

Explore [Guides]({{ '/projects/Secrets-Kit/guides/' | relative_url }}), [Remote Sync]({{ '/projects/Secrets-Kit/remote-sync/' | relative_url }}), [planned pricing]({{ '/projects/Secrets-Kit/pricing/' | relative_url }}), and [Security & Privacy]({{ '/projects/Secrets-Kit/security/' | relative_url }}). Use [Help & Support]({{ '/projects/Secrets-Kit/support/' | relative_url }}) for questions and sanitized problem reports.
