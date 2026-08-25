---
layout: page
title: "Topics and Article Types"
permalink: /topics/
excerpt: "Browse the controlled topic vocabulary and article types used across Distributed Thinking Systems posts and project blogs."
image: /assets/images/default-og-image.png
---

Browse the site by recurring themes instead of by section or project. Topics pull together both standard blog posts and project blog entries. Article types describe what a post is—such as a release or introduction—without treating publication status as a subject tag.

## Topics Index

{% for topic_group in site.data.tag_taxonomy.groups %}
### {{ topic_group.label }}

<div class="topics-cloud" aria-label="{{ topic_group.label }} topics">
  {% for topic in site.data.tag_taxonomy.tags %}
    {% if topic.group == topic_group.id %}
      {% assign tag_posts = site.tags[topic.id] %}
      {% if tag_posts and tag_posts.size > 0 %}
        <a class="topic-chip" href="#topic-{{ topic.id | slugify }}">{{ topic.label }} <span>{{ tag_posts | size }}</span></a>
      {% endif %}
    {% endif %}
  {% endfor %}
</div>
{% endfor %}

## Browse by Article Type

<div class="topics-cloud" aria-label="Article types">
  {% for article_type in site.data.tag_taxonomy.content_types %}
    {% assign type_posts = site.posts | where: "content_type", article_type.id %}
    {% if type_posts.size > 0 %}
      <a class="topic-chip" href="#type-{{ article_type.id | slugify }}">{{ article_type.label }} <span>{{ type_posts | size }}</span></a>
    {% endif %}
  {% endfor %}
</div>

## Topic Listings

{% for topic_group in site.data.tag_taxonomy.groups %}
{% for topic in site.data.tag_taxonomy.tags %}
{% if topic.group == topic_group.id %}
{% assign tag_posts = site.tags[topic.id] %}
{% if tag_posts and tag_posts.size > 0 %}
{% assign tag_posts = tag_posts | sort: 'date' | reverse %}
{% for alias in topic.aliases %}<span id="topic-{{ alias | slugify }}" class="topic-alias-anchor" aria-hidden="true"></span>{% endfor %}
<section class="topic-listing" id="topic-{{ topic.id | slugify }}">
  <h2>{{ topic.label }}</h2>
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
    </li>
    {% endfor %}
  </ul>
</section>
{% endif %}
{% endif %}
{% endfor %}
{% endfor %}

## Article Type Listings

{% for article_type in site.data.tag_taxonomy.content_types %}
{% assign type_posts = site.posts | where: "content_type", article_type.id | sort: 'date' | reverse %}
{% if type_posts.size > 0 %}
{% for source_tag in article_type.source_tags %}<span id="topic-{{ source_tag | slugify }}" class="topic-alias-anchor" aria-hidden="true"></span>{% endfor %}
<section class="topic-listing" id="type-{{ article_type.id | slugify }}">
  <h2>{{ article_type.label }}</h2>
  <p class="topic-count">{{ type_posts | size }} post{% if type_posts.size != 1 %}s{% endif %}</p>
  <ul class="post-list">
    {% for post in type_posts %}
    <li>
      <h3><a class="post-link" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h3>
      <span class="post-meta">{{ post.date | date: "%B %-d, %Y" }}</span>
    </li>
    {% endfor %}
  </ul>
</section>
{% endif %}
{% endfor %}
