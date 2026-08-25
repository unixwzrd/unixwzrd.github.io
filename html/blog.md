---
layout: page
title: "Distributed Thinking Systems Blog"
menu_item: Blog
permalink: /blog/
show_support: true
image: /assets/images/default-og-image.png
excerpt: "Writing on local-first AI, secure automation, developer tooling, parental alienation, and sensitive workflow analysis."
---

A structured writing hub for local-first AI, secure automation, developer tooling, family-law analysis, and project updates.

For related project work, start with [Secrets Kit](/projects/Secrets-Kit/), [LLM Ops Kit](/projects/LLM-Ops-Kit/), and [Case Analytics](/projects/Case-Analytics/).

<aside class="series-context" aria-label="Featured technical series">
  <p><strong>Featured series: <a href="{{ '/blog/series/local-first-ai-and-agent-operations/' | relative_url }}">Local First AI and Agent Operations</a>.</strong> Browse the engineering story and its Hands-On companions together in the Series section.</p>
</aside>

<div class="blog-section-grid">
  {% for blog_section in site.data.blog_sections.sections %}
    {% if blog_section.visible %}
      {% assign blog_section_page = site.pages | where: "url", blog_section.url | first %}
      <section class="blog-section-card">
        <h2><a href="{{ blog_section.url | relative_url }}">{{ blog_section.title }}</a></h2>
        <p>{{ blog_section_page.excerpt | default: blog_section.description }}</p>
        <a class="button-link" href="{{ blog_section.url | relative_url }}">{{ blog_section.button_label }}</a>
      </section>
    {% endif %}
  {% endfor %}
</div>

## [Browse by Topic]({{ '/topics/' | relative_url }})

Use the [Topics index]({{ '/topics/' | relative_url }}) to explore tags and cross-project themes spanning site posts and project blogs.

{% for blog_section in site.data.blog_sections.sections %}
  {% if blog_section.visible %}
## [Recent from {{ blog_section.title }}]({{ blog_section.url | relative_url }})

{% include blog_list.html section=blog_section.section additional_category=blog_section.additional_category additional_category_primary_only=blog_section.additional_category_primary_only series=blog_section.series exclude_series=blog_section.exclude_series limit=3 hide_heading=true %}
  {% endif %}
{% endfor %}
