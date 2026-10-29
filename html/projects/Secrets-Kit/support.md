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

Use [Secrets Kit Discussions]({{ seckit_release.discussions_url }}) for setup questions, feature requests and ideas. Public discussion helps other users find the answer later. Follow [Blog & Updates]({{ seckit_updates_url }}) for release updates.

## Security concerns or sensitive account details

Please [contact us privately]({{ '/contact/' | relative_url }}) before posting a suspected vulnerability, account information, or material that could expose someone’s credentials. Mention Secrets Kit in your message and describe the issue without sending secret values. We can agree on an appropriate way to share further details.

## Support options

### Community help

Public bug reports and questions are welcome for the free client. Use the Issues and Discussions routes above, and share only sanitized information. Community help has no contracted response time.

### Included RSS service support

An RSS subscription includes help with connection enrollment, hosted forwarding, subscription access and other problems in the hosted service. We investigate reported service problems and work to resolve them. Use [private contact]({{ '/contact/' | relative_url }}) for account or billing details; reproducible software bugs can be reported in Issues.

### Contracted support

If you need priority assistance or work on your particular environment, [ask about a paid support contract]({{ '/collaborate/professionals/' | relative_url }}). Two arrangements are available to discuss:

- **Project assistance:** a defined setup, migration, agent integration or troubleshooting engagement, with an agreed scope and price.
- **Ongoing support:** a continuing support agreement with an agreed scope, fees, coverage hours, contacts and response targets.

The written agreement sets the support level and any service commitments. The RSS connection subscription is separate from these contracts and does not itself include priority support or a service-level agreement.

## Support and billing expectations

See the [RSS service terms]({{ '/projects/Secrets-Kit/policies/#service-terms' | relative_url }}) for cancellation, quantity changes, refunds and the terms still to be confirmed. {% unless seckit_release.production_release_ready %}Installation and production subscriptions remain closed.{% endunless %}
