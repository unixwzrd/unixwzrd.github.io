---
title: "oobabooga-macOS"
layout: page
permalink: /projects/oobabooga-macOS/
---

## oobabooga-macOS

Optimizing performance, building and installing packages required for oobabooga, AI and Data Science on Apple Silicon GPU. The goal is to optimize wherever possible, from the ground up. - unixwzrd/...

- [View on GitHub](https://github.com/unixwzrd/oobabooga-macOS)

## Project Blog Entries

{% for post in site.categories.oobabooga-macOS %}
  <article class="post">
    <h3><a href="{ post.url | relative_url }">{ post.title }</a></h3>
    <span class="post-date">{ post.date | date: "%B %d, %Y" }</span>
    {% assign excerpt = post.content | split: '<!--more-->' | first %}
    { excerpt | truncatewords: 50 | markdownify | process_heading }
    <a href="{ post.url | relative_url }" class="btn">Read More</a>
  </article>
{% endfor %}
