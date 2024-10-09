---
title: "TokenSecure"
layout: page
permalink: /projects/TokenSecure/
---

## TokenSecure

A safer way to store access tokens in an encrypted file and access them in your scripts without relying on environment files which could be accidentally be uploaded into a public repository. - unix...

- [View on GitHub](https://github.com/unixwzrd/TokenSecure)

## Project Blog Entries

{% for post in site.categories.TokenSecure %}
  <article class="post">
    <h3><a href="{ post.url | relative_url }">{ post.title }</a></h3>
    <span class="post-date">{ post.date | date: "%B %d, %Y" }</span>
    {% assign excerpt = post.content | split: '<!--more-->' | first %}
    { excerpt | truncatewords: 50 | markdownify | process_heading }
    <a href="{ post.url | relative_url }" class="btn">Read More</a>
  </article>
{% endfor %}
