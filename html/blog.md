---
layout: blog
title: Distributed Thinking Systems Blog
menu_item: Blog
permalink: /blog/
---

Welcome to the Distributed Thinking Systems blog! Here, we dive into the cutting-edge world of artificial intelligence, distributed computing, and tech innovation. Whether you’re looking for the latest breakthroughs in AI research, project updates, or deep technical explorations, you’ll find it all here.

Stay connected for insights and articles from Michael Sullivan, sharing over 30 years of experience in technology and innovation. Our posts cover everything from real-world AI applications to thought-provoking takes on the future of tech. We’re excited to share our journey with you!

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a> - {{ post.date | date: "%B %d, %Y" }}
    </li>
  {% endfor %}
</ul>


{% include GetInTouch.html %}