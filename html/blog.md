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
  <p><strong>Featured series: <a href="{{ '/blog/series/local-first-ai-and-agent-operations/' | relative_url }}">Local First AI and Agent Operations</a>.</strong> Follow the main engineering story in Technology, or step into the separate Hands-On companions when you want runnable code and exercises.</p>
</aside>

{% assign general_blog_page = site.pages | where: "url", "/blog/general/" | first %}
{% assign pa_blog_page = site.pages | where: "url", "/blog/parental-alienation/" | first %}
{% assign technology_blog_page = site.pages | where: "url", "/blog/technology/" | first %}
{% assign series_blog_page = site.pages | where: "url", "/blog/series/" | first %}
{% assign hands_on_blog_page = site.pages | where: "url", "/blog/hands-on/" | first %}

<div class="blog-section-grid">
  <section class="blog-section-card">
    <h2><a href="{{ '/blog/general/' | relative_url }}">General</a></h2>
    <p>{{ general_blog_page.excerpt }}</p>
    <a class="button-link" href="{{ '/blog/general/' | relative_url }}">Read General Posts</a>
  </section>

  <section class="blog-section-card">
    <h2><a href="{{ '/blog/parental-alienation/' | relative_url }}">Parental Alienation</a></h2>
    <p>{{ pa_blog_page.excerpt }}</p>
    <a class="button-link" href="{{ '/blog/parental-alienation/' | relative_url }}">Read Parental Alienation Posts</a>
  </section>

  <section class="blog-section-card">
    <h2><a href="{{ '/blog/technology/' | relative_url }}">Technology</a></h2>
    <p>{{ technology_blog_page.excerpt }}</p>
    <a class="button-link" href="{{ '/blog/technology/' | relative_url }}">Read Technology Posts</a>
  </section>

  <section class="blog-section-card">
    <h2><a href="{{ '/blog/series/' | relative_url }}">Series</a></h2>
    <p>{{ series_blog_page.excerpt }}</p>
    <a class="button-link" href="{{ '/blog/series/' | relative_url }}">Browse Series</a>
  </section>

  <section class="blog-section-card">
    <h2><a href="{{ '/blog/hands-on/' | relative_url }}">Hands-On</a></h2>
    <p>{{ hands_on_blog_page.excerpt }}</p>
    <a class="button-link" href="{{ '/blog/hands-on/' | relative_url }}">Read Hands-On Posts</a>
  </section>
</div>

## [Browse by Topic]({{ '/topics/' | relative_url }})

Use the [Topics index]({{ '/topics/' | relative_url }}) to explore tags and cross-project themes spanning site posts and project blogs.

## [Recent from General]({{ '/blog/general/' | relative_url }})

{% include blog_list.html section="general" limit=3 hide_heading=true %}

## [Recent from Parental Alienation]({{ '/blog/parental-alienation/' | relative_url }})

{% include blog_list.html section="parental-alienation" limit=3 hide_heading=true %}

## [Recent from Technology]({{ '/blog/technology/' | relative_url }})

{% include blog_list.html section="technology" limit=3 hide_heading=true %}

## [Recent from Hands-On]({{ '/blog/hands-on/' | relative_url }})

{% include blog_list.html section="hands-on" limit=3 hide_heading=true %}
