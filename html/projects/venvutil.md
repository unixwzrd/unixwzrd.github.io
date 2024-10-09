---
title: "venvutil"
layout: page
permalink: /projects/venvutil/
---

## venvutil

Python virtual environment management functions and script to build and manage performance, compatibility, and regression test venv builds mostly for AI - unixwzrd/venvutil

- [View on GitHub](https://github.com/unixwzrd/venvutil)

## Project Blog Entries

{% for post in site.categories.venvutil %}
  <article class="post">
    <h3><a href="{ post.url | relative_url }">{ post.title }</a></h3>
    <span class="post-date">{ post.date | date: "%B %d, %Y" }</span>
    {% assign excerpt = post.content | split: '<!--more-->' | first %}
    { excerpt | truncatewords: 50 | markdownify | process_heading }
    <a href="{ post.url | relative_url }" class="btn">Read More</a>
  </article>
{% endfor %}
