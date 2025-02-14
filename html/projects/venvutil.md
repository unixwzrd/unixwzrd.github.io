---
layout: project
title: "venvutil"
category: venvutil
permalink: /projects/venvutil/
---

## venvutil

Python virtual environment management functions and script to build and manage performance, compatibility, and regression test venv builds mostly for AI - unixwzrd/venvutil

<!-- Placeholder for additional user supplied information >
## This is some optional additional information on venvutil

Some additional information as a placeholder for additional project information we can edit to appear on the page as well, in front of the blog entries.
<!-- Placeholder for additional user supplied information -->

* [View on GitHub](https://github.com/unixwzrd/venvutil){: target="_blank" rel="noopener noreferrer"}

## Project Blog Entries

{% for post in site.categories.venvutil %}
<article class="post">
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
    {% assign excerpt = post.content | split: '<!--more-->' | first %}
    {{ excerpt | truncatewords: 50 | markdownify }}
    <a href="{{ post.url | relative_url }}" class="btn">Read More</a>
</article>
{% endfor %}

{% include join_us.html %}

{% include getintouch.html %}
