---
layout: project
title: "chatgpt-chatlog-export"
category: chatgpt-chatlog-export
permalink: /projects/chatgpt-chatlog-export/
---

## chatgpt-chatlog-export

ChatGPT - Chat Log Export, a lightweight method of exporting entire ChatGPT conversations in JSON format. - unixwzrd/chatgpt-chatlog-export

<!-- Placeholder for additional user supplied information >
## This is some optional additional information on chatgpt-chatlog-export

Some additional information as a placeholder for additional project information we can edit to appear on the page as well, in front of the blog entries.
<!-- Placeholder for additional user supplied information -->

* [View on GitHub](https://github.com/unixwzrd/chatgpt-chatlog-export){: target="_blank" rel="noopener noreferrer"}

## Project Blog Entries

{% for post in site.categories.chatgpt-chatlog-export %}
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
