---
layout: page
title: "Topics"
permalink: /topics/
excerpt: "Browse topics, tags, and cross-project themes across Distributed Thinking Systems posts and project blogs."
image: /assets/images/default-og-image.png
---

Browse the site by recurring themes instead of by section or project. Topics pull together both standard blog posts and project blog entries.

## Blog Sections

<div class="topics-section-grid">
  <a class="topic-card" href="{{ '/blog/general/' | relative_url }}">
    <strong>General</strong>
    <span>{{ site.categories.general | size }} posts</span>
  </a>
  <a class="topic-card" href="{{ '/blog/parental-alienation/' | relative_url }}">
    <strong>Parental Alienation</strong>
    <span>{{ site.categories.parental-alienation | size }} posts</span>
  </a>
  <a class="topic-card" href="{{ '/blog/technology/' | relative_url }}">
    <strong>Technology</strong>
    <span>{{ site.categories.technology | size }} posts</span>
  </a>
</div>

## Topics Index

<div class="topics-cloud">
  {% assign sorted_tags = site.tags | sort %}
  {% for tag in sorted_tags %}
    {% assign tag_name = tag[0] %}
    {% assign tag_posts = tag[1] %}
    <a class="topic-chip" href="#topic-{{ tag_name | slugify }}">{{ tag_name }} <span>{{ tag_posts | size }}</span></a>
  {% endfor %}
</div>

## Topic Listings

{% for tag in sorted_tags %}
  {% assign tag_name = tag[0] %}
  {% assign tag_posts = tag[1] | sort: 'date' | reverse %}
  <section class="topic-listing" id="topic-{{ tag_name | slugify }}">
    <h2>{{ tag_name }}</h2>
    <p class="topic-count">{{ tag_posts | size }} post{% if tag_posts.size != 1 %}s{% endif %}</p>
    <ul class="post-list">
      {% for post in tag_posts %}
        <li>
          <h3><a class="post-link" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h3>
          <span class="post-meta">{{ post.date | date: "%B %-d, %Y" }}</span>
          {% if post.category %}
            <span class="topic-meta-label">{{ post.category }}</span>
          {% elsif post.categories %}
            <span class="topic-meta-label">{{ post.categories | first }}</span>
          {% endif %}
          <div class="post-excerpt">
            {% if post.excerpt %}
              {{ post.excerpt | strip_images | markdownify | process_heading }}
            {% else %}
              {{ post.content | strip_images | truncatewords: site.excerpt_word_limit | markdownify | process_heading }}
            {% endif %}
          </div>
        </li>
      {% endfor %}
    </ul>
  </section>
{% endfor %}
