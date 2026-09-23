---
layout: page
title: "Beyond Static: Building a Publication System Around Jekyll"
permalink: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
short_link: true
short_link_basis: "/blog/series/beyond-static-building-a-publication-system-around-jekyll.md"
short_url: "https://unixwzrd.ai/s/9921c79b2b/"
series_landing: true
series_order: 20
show_support: true
excerpt: "A ten-part engineering series about extending a Jekyll site with project publishing, reusable Liquid templates, stable URLs, technical-article tools, validation, and monitoring."
image: /assets/images/blog/jekyll-site-tooling/post-01-publishing-workbench-hero.png
---

Jekyll still builds the site, but writing Markdown is only part of publishing it. A new project needs a place in the catalog, a card, a landing page, a blog, and a route into navigation. An article needs a stable URL, a useful place in discovery, and a way to review it before readers see it. Technical posts also bring diagrams, source files, and sometimes audio.

I added tools as those needs surfaced. Some changes are Liquid layouts and includes; others are Ruby plugins, Python generators, shell wrappers, checks, or review habits. This series follows the problems that led to them and explains where each part of the workflow begins and ends.

The main installments tell the engineering story. Optional Hands-On companions will use small, invented examples when a mechanism is worth building separately. They will appear beside the relevant installment and are not required to follow the argument.

{% assign published_series_posts = site.posts | where: "series", "Beyond Static: Building a Publication System Around Jekyll" %}
{% if published_series_posts.size > 0 %}
{% include series_index.html series="Beyond Static: Building a Publication System Around Jekyll" %}
{% else %}
The opening installment is in review. It will appear here after publication.
{% endif %}

## Across the Series

The opening article follows repeated Jekyll frustrations into a more connected publication workflow. From there I look at local preview, layout inheritance and shared Liquid includes, stable URLs, the YAML project catalog, project blogs and discovery, diagrams and source files, proofreading by listening, validation and deployment gates, monitoring, and the editorial decisions that still belong to a person.

The repository includes older experiments and utilities alongside active paths. I will distinguish implemented code, current operator use, configured automation, and historical work instead of treating every script as part of the daily publishing path.
