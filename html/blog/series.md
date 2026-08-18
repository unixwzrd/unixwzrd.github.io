---
layout: page
title: "Series"
permalink: /blog/series/
excerpt: "Long-form article series that follow an engineering problem across design, implementation, measurement, and operations."
image: /assets/images/default-og-image.png
---

Long-form collections that follow one engineering thread across multiple articles, with their reading order and Hands-On companions kept together.

{% assign series_pages = site.pages | where: "series_landing", true | sort: "series_order" %}

<div class="blog-section-grid">
  {% for series_page in series_pages %}
  <section class="blog-section-card">
    <h2><a href="{{ series_page.url | relative_url }}">{{ series_page.title }}</a></h2>
    <p>{{ series_page.excerpt }}</p>
    <a class="button-link" href="{{ series_page.url | relative_url }}">View Series</a>
  </section>
  {% endfor %}
</div>
