---
layout: page
title: "Search"
permalink: /search/
excerpt: "Search core pages, blog posts, and project content across Distributed Thinking Systems."
hide_banner_image: true
search_page: true
search_exclude: true
sitemap: false
---

<section class="search-page" data-search-page>
  <p class="search-page-intro">
    Search across core pages, blog posts, project pages, and project blog entries.
  </p>

  <div class="search-controls">
    <label class="search-label" for="site-search-input">Search</label>
    <input
      class="search-input"
      id="site-search-input"
      name="q"
      type="search"
      autocomplete="off"
      placeholder="Search projects, posts, and topics"
      data-search-input>
  </div>

  <div class="search-status" data-search-status aria-live="polite"></div>
  <div class="search-results" data-search-results></div>
</section>
