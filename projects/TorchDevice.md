---
layout: project
title: "TorchDevice"
category: TorchDevice
---

## TorchDevice

Module contains class TorchDevice abstracting CUDA/MPS/CPU, intercepting, and redirecting calls to the available device to assist in porting code from CUDA to MPS. - unixwzrd/TorchDevice

<!-- Placeholder for additional user supplied information >
## This is some optional additional information on TorchDevice

Some additional information as a placeholder for additional project information we can edit to appear on the page as well, in front of the blog entries.
<!-- Placeholder for additional user supplied information -->

* [View on GitHub](https://github.com/unixwzrd/TorchDevice){{:target="_blank" rel="noopener noreferrer"}}

## Project Blog Entries

{% for post in site.categories.TorchDevice %}
<article class="post">
    <h3><a href="{{{ post.url | relative_url }}}">{{{ post.title }}}</a></h3>
    <span class="post-date">{{{ post.date | date: "%B %d, %Y" }}}</span>
    {% assign excerpt = post.content | split: '<!--more-->' | first %}
    {{{ excerpt | truncatewords: 50 | markdownify }}}
    <a href="{{{ post.url | relative_url }}}" class="btn">Read More</a>
</article>
{% endfor %}

{% include join_us.html %}

{% include getintouch.html %}
