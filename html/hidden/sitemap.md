---
layout: page
title: "Sitemap"
permalink: /hidden/sitemap/
image: /assets/images/default-og-image.png
excerpt: ""
---

## Sitemap

### Pages
{% for page in site.pages %}
- [{{ page.title }}]({{ page.url | relative_url }})
{% endfor %}

### Blog Posts
{% for post in site.posts %}
- [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}