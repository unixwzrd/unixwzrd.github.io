---
title: "TorchDevice"
layout: page
permalink: /projects/TorchDevice/
---

## TorchDevice

Module contains class TorchDevice abstracting CUDA/MPS/CPU, intercepting, and redirecting calls to the available device to assist in porting code from CUDA to MPS. - unixwzrd/TorchDevice

- [View on GitHub](https://github.com/unixwzrd/TorchDevice)

## Project Blog Entries

{% for post in site.categories.TorchDevice %}
  <article class="post">
    <h3><a href="{ post.url | relative_url }">{ post.title }</a></h3>
    <span class="post-date">{ post.date | date: "%B %d, %Y" }</span>
    {% assign excerpt = post.content | split: '<!--more-->' | first %}
    { excerpt | truncatewords: 50 | markdownify | process_heading }
    <a href="{ post.url | relative_url }" class="btn">Read More</a>
  </article>
{% endfor %}
