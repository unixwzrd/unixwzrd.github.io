---
title: "Policies"
layout: page
menu_item: Policies
permalink: /Policies/
image: /assets/images/default-og-image.png
excerpt: ""
---

## Distributed Thinking Systems LLC Policies

### Privacy Policies

- [Website Privacy Policy](/Policies/General_Privacy/)
- [LogGPT Privacy Policy](/Policies/Privacy_LogGPT_for_Safari/)

{% assign seckit_policy_page = site.pages | where: 'url', '/projects/Secrets-Kit/policies/' | first %}
{% if seckit_policy_page %}
### Secrets Kit and Remote Secret Sync (RSS)

- [Secrets Kit client privacy](/projects/Secrets-Kit/policies/#client-privacy)
- [Remote Secret Sync privacy, metadata and retention](/projects/Secrets-Kit/policies/#remote-secrets-sync-privacy)
- [RSS service terms, cancellation and refunds](/projects/Secrets-Kit/policies/#service-terms)
- [Secrets Kit client MIT License](/projects/Secrets-Kit/policies/#client-license)

{% endif %}

### Terms of Service
- [Website Terms of Service](/Policies/General_ToS/)
- [LogGPT MIT License](https://github.com/unixwzrd/LogGPT/blob/main/LICENSE)

{% assign extract_chat_privacy = site.pages | where: 'url', '/Policies/Privacy_Extract_Chat/' | first %}
{% assign extract_chat_terms = site.pages | where: 'url', '/Policies/Terms_Extract_Chat/' | first %}
{% if extract_chat_privacy and extract_chat_terms %}
### Extract Chat

Extract Chat is a separate application for converting local conversation exports. Its privacy policy and terms are separate from LogGPT's.

- [Extract Chat Privacy Policy](/Policies/Privacy_Extract_Chat/)
- [Extract Chat Terms of Use and MIT License](/Policies/Terms_Extract_Chat/)

{% endif %}




