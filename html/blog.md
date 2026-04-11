---
layout: page
title: "Distributed Thinking Systems Blog"
menu_item: Blog
permalink: /blog/
image: /assets/images/default-og-image.png
excerpt: "Explore the Distributed Thinking Systems writing index, with dedicated sections for General, Parental Alienation, and Technology."
---

A structured writing hub for updates, analysis, and essays across three editorial tracks.

{% assign general_blog_page = site.pages | where: "url", "/blog/general/" | first %}
{% assign pa_blog_page = site.pages | where: "url", "/blog/parental-alienation/" | first %}
{% assign technology_blog_page = site.pages | where: "url", "/blog/technology/" | first %}

<div class="blog-section-grid">
  <section class="blog-section-card">
    <h2><a href="{{ '/blog/general/' | relative_url }}">General</a></h2>
    <p>{{ general_blog_page.excerpt }}</p>
    <a class="button-link" href="{{ '/blog/general/' | relative_url }}">Read General Posts</a>
  </section>

  <section class="blog-section-card">
    <h2><a href="{{ '/blog/parental-alienation/' | relative_url }}">Parental Alienation</a></h2>
    <p>{{ pa_blog_page.excerpt }}</p>
    <a class="button-link" href="{{ '/blog/parental-alienation/' | relative_url }}">Read Parental Alienation Posts</a>
  </section>

  <section class="blog-section-card">
    <h2><a href="{{ '/blog/technology/' | relative_url }}">Technology</a></h2>
    <p>{{ technology_blog_page.excerpt }}</p>
    <a class="button-link" href="{{ '/blog/technology/' | relative_url }}">Read Technology Posts</a>
  </section>
</div>

## Browse by Topic

Use the [Topics index]({{ '/topics/' | relative_url }}) to explore tags and cross-project themes spanning site posts and project blogs.

## Recent from General

{% include blog_list.html section="general" limit=3 hide_heading=true %}

## Recent from Parental Alienation

{% include blog_list.html section="parental-alienation" limit=3 hide_heading=true %}

## Recent from Technology

{% include blog_list.html section="technology" limit=3 hide_heading=true %}
