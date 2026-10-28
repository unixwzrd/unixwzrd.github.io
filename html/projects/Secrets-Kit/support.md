---
layout: page
title: "Secrets Kit help and problem reporting"
permalink: /projects/Secrets-Kit/support/
published: true
secrets_kit_product: true
product_nav_order: 70
nav_title: Help & Support
hide_banner_image: true
excerpt: "Report a Secrets Kit bug, ask a question in the project forum, or contact us privately."
---

{% include secrets-kit/navigation.html %}

## Report a problem

Use [Secrets Kit GitHub Issues]({{ seckit_release.issues_url }}) for reproducible bugs. Search for an existing report first; if there is no matching issue, [open a new issue]({{ seckit_release.new_issue_url }}). A GitHub account is required to post.

Include enough detail to reproduce the problem:

- Your Secrets Kit version, operating system, and processor architecture.
- The command or action, with credentials and identifying details removed.
- What you expected and what happened instead.
- The exact sanitized error and the steps that reproduce it.
- Whether the problem affects local use, peer synchronization, RSS enrollment, or an agent integration.

Do not include secret values, private keys, recovery codes, credential files, raw environment dumps, or payment receipts. Share the smallest useful sanitized excerpt rather than a full diagnostic archive.

## Questions and feature ideas

Use [Secrets Kit Discussions]({{ seckit_release.discussions_url }}) for setup questions, feature requests, release updates, and ideas. Public discussion helps other users find the answer later. You can also watch the project on GitHub for release announcements.

## Security concerns or sensitive account details

Please [contact us privately]({{ '/contact/' | relative_url }}) before posting a suspected vulnerability, account information, or material that could expose someone’s credentials. Mention Secrets Kit in your message and describe the issue without sending secret values. We can agree on an appropriate way to share further details.

## Installation or migration assistance

For hands-on configuration, migration, or deployment work, [ask about professional setup assistance]({{ '/collaborate/professionals/' | relative_url }}). This is separate from public bug reporting and the optional RSS subscription.

## Support and billing expectations

Project Issues and Discussions provide the public reporting routes; sensitive account, security and billing questions belong in private contact. Support response times and service-availability commitments are not yet set. See the [staged RSS service terms]({{ '/projects/Secrets-Kit/policies/#service-terms' | relative_url }}) for cancellation, quantity changes, refunds and the terms still to be confirmed. {% unless seckit_release.production_release_ready %}Installation and production subscriptions remain closed.{% endunless %}
