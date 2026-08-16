---
layout: page
title: "Local-First Agent Operations"
permalink: /blog/series/local-first-agent-operations/
excerpt: "A planned 13-part engineering series about making a local-first agent environment measurable, recoverable, governable, and easier to operate."
image: /assets/images/blog/agent-optimization/post-01-local-ai-operations-system-hero.png
---

This planned 13-part series follows the work of turning a local-first collection of models, agents, services, memory, and developer tools into an environment I can inspect, recover, and improve without hiding the hard parts behind another layer of automation.

The main installments appear in [Technology](/blog/technology/). Runnable companion articles appear in [Hands-On](/blog/hands-on/). Each post stands on its own, while the links at the top and bottom preserve the larger engineering story.

## Published and Scheduled Articles

{% assign agent_operations_posts = site.posts | where: "series", "Local-First Agent Operations" | sort: "date" %}

<ol class="series-index">
{% for post in agent_operations_posts %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <span class="post-meta">Part {{ post.series_part }} · {{ post.date | date: "%B %-d, %Y" }} · {{ post.categories | first | replace: '-', ' ' | capitalize }}</span>
  </li>
{% endfor %}
</ol>

## Coming Later

The remaining installments cover governed memory retrieval, the optimization-tool landscape, measuring token reduction without damaging agent behavior, passive model-proxy instrumentation, multimodal context hygiene, operator-ready packaging, cross-host voice services, Apple Silicon inference, installable skills, safe multi-agent operation on one LAN, and an honest public-release readiness assessment.
