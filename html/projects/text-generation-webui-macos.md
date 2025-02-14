---
layout: project
title: "text-generation-webui-macos"
category: text-generation-webui-macos
---

## text-generation-webui-macos

A macOS version of the oobabooga gradio web UI for running Large Language Models like LLaMA, llama.cpp, GPT-J, Pythia, OPT, and GALACTICA. - unixwzrd/text-generation-webui-macos

<!-- Placeholder for additional user supplied information >
## This is some optional additional information on text-generation-webui-macos

Some additional information as a placeholder for additional project information we can edit to appear on the page as well, in front of the blog entries.
<!-- Placeholder for additional user supplied information -->

* [View on GitHub](https://github.com/unixwzrd/text-generation-webui-macos){: target="_blank" rel="noopener noreferrer"}

## Project Blog Entries

{% for post in site.categories.text-generation-webui-macos %}
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
