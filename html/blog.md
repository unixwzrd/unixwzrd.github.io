---
title: "Distributed Thinking Systems Blog"
layout: page
menu_item: Blog
permalink: /blog/
---

Welcome to the **Distributed Thinking Systems Blog**, where we delve into topics at the intersection of **AI development**, **distributed computing**, and **technology innovations** in **Unix/Linux/macOS environments**. 

Beyond tech, we explore real-world applications of these advancements, such as addressing societal challenges like **parental alienation**. Dive into our latest articles and stay informed about our projects, research, and technical explorations.

{% for post in site.posts %}
  <article class="post">
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
    {% assign excerpt = post.content | split: '<!--more-->' | first %}
    {{ excerpt | truncatewords: 50 | markdownify | process_heading }}
    <a href="{{ post.url | relative_url }}" class="btn">Read More</a>
  </article>
{% endfor %}

{% include getintouch.html %}