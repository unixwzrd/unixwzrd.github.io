---
layout: home
title: "Distributed Thinking Systems"
menu_item: Home
permalink: /
excerpt: "Distributed Thinking Systems helps professionals and small teams run local AI, secure automation, and practical systems for sensitive work."
image: "/assets/images/default-og-image.png"
hide_home_title: true
hide_content_footer: true
---

<div class="home-banner">
  <img src="{{ page.image | relative_url }}" alt="Distributed Thinking Systems LLC — AI systems, developer tooling, and automation" width="1536" height="512" fetchpriority="high" decoding="async">
</div>

<section class="home-hero" aria-labelledby="home-heading">
  {% if site.data.secrets_kit.production_release_ready == false %}
  <aside class="seckit-notice" aria-label="Secrets Kit announcement">
    <strong>Coming soon: Secrets Kit {{ site.data.secrets_kit.release_tag | remove_first: 'v' | escape }}</strong>
    <p>Free peer-to-peer secrets management, unlimited connections on the same LAN segment, and optional remote sync. Final testing is underway. <a href="{{ '/projects/Secrets-Kit/' | relative_url }}">Meet Secrets Kit →</a></p>
  </aside>
  {% endif %}
  <p class="home-kicker">Local-first software &amp; systems engineering</p>
  <h1 id="home-heading">Practical tools.<br>Local control.</h1>
  <p class="home-lead">Keep your AI conversations, credentials, and working files useful—and under your control.</p>
  <p>Distributed Thinking Systems builds local-first software and automation for developers, independent professionals, and small teams. Explore the tools, follow the engineering, or get help making a sensitive workflow work on your own systems.</p>
  <div class="home-actions">
    <a class="home-button home-button--primary" href="#featured-tools">Explore the tools</a>
    <a class="home-button" href="{{ '/blog/' | relative_url }}">Read the engineering</a>
    <a class="home-text-link" href="{{ '/collaborate/professionals/' | relative_url }}">Work with us →</a>
  </div>
</section>

<section class="home-section" aria-labelledby="featured-tools">
  <div class="home-section-heading">
    <h2 id="featured-tools">Tools worth a closer look</h2>
    <p>Different jobs, a shared approach: local processing, portable files, and deliberate handling of sensitive information.</p>
  </div>
  <div class="home-project-grid">
    {% for featured in site.data.homepage.featured_projects %}
      {% assign project = site.data.github_projects.projects | where: 'name', featured.name | first %}
      {% if project and project.visibility == 'public' %}
      <article class="home-project-card" data-home-project="{{ project.name | escape }}">
        <a class="home-project-image" href="{{ project.page_url | relative_url }}" tabindex="-1" aria-hidden="true">
          <img src="{{ project.banner_image_url | default: project.image_url | relative_url }}" alt="" loading="lazy" width="640" height="360">
        </a>
        <div class="home-project-copy">
          <p class="home-label">{{ featured.label | escape }}</p>
          <h3><a href="{{ project.page_url | relative_url }}">{{ project.title | escape }}</a></h3>
          <p>{{ featured.summary | escape }}</p>
          <a class="home-card-action" href="{{ project.page_url | relative_url }}">{{ featured.action | escape }} →</a>
        </div>
      </article>
      {% endif %}
    {% endfor %}
  </div>
  <div class="home-more-tools">
    <h3>More of the toolkit</h3>
    <ul>
      {% for featured in site.data.homepage.more_projects %}
        {% assign project = site.data.github_projects.projects | where: 'name', featured.name | first %}
        {% if project and project.visibility == 'public' %}
        <li><a href="{{ project.page_url | relative_url }}">{{ project.title | escape }}</a> — {{ featured.summary | escape }}</li>
        {% endif %}
      {% endfor %}
    </ul>
    <p><a href="{{ '/projects/' | relative_url }}">Browse all projects →</a></p>
  </div>
</section>

<section class="home-section" aria-labelledby="home-services">
  <h2 id="home-services">When the pieces need to work together</h2>
  <p>A useful tool is only part of a working system. Distributed Thinking Systems also provides hands-on integration, automation, and troubleshooting for local AI and sensitive workflows.</p>
  <div class="home-capabilities">
    <div>
      <h3>Local AI &amp; agents</h3>
      <p>Model runtimes, agent workflows, and document processing fitted to your hardware and the data you need to handle.</p>
    </div>
    <div>
      <h3>Secure automation</h3>
      <p>Shell tools and service workflows that make credential handling explicit and reduce unnecessary copies of sensitive data.</p>
    </div>
    <div>
      <h3>Systems engineering</h3>
      <p>Unix, Linux, and macOS integration, diagnostics, and developer infrastructure—with attention to how it will be operated and maintained.</p>
    </div>
  </div>
  <p><a href="{{ '/collaborate/professionals/' | relative_url }}">Explore professional services</a> or <a href="{{ '/contact/' | relative_url }}">bring a specific problem</a>.</p>
</section>

<section class="home-section" aria-labelledby="home-writing">
  <h2 id="home-writing">Follow the engineering</h2>
  <p>The writing covers implementation, experiments, failures, and the decisions behind the tools—not just release announcements. Read a <a href="{{ '/blog/series/' | relative_url }}">complete series</a>, try a <a href="{{ '/blog/hands-on/' | relative_url }}">Hands-On tutorial</a>, or start with a recent post.</p>
  {% include discovery_post_list.html limit=4 %}
  <p><a href="{{ '/blog/all/' | relative_url }}">Browse every post →</a></p>
  <p>Want to talk through an article or share what you are building? <a href="https://www.reddit.com/r/unixwzrd/">Join the conversation at r/unixwzrd →</a></p>
</section>

<section class="home-section home-research" aria-labelledby="home-research">
  <h2 id="home-research">Research with a human purpose</h2>
  <p>Some of this work grew from the difficulty of organizing sensitive communications and family-law records. <a href="{{ '/projects/Case-Analytics/' | relative_url }}">Case Analytics</a> and <a href="{{ '/projects/PA-Awareness-1/' | relative_url }}">parental alienation research</a> remain part of that longer-term effort. The aim is to support careful review and preserve context, not to turn an AI output into a finding about a family.</p>
  <p>For research participation or project contributions, see <a href="{{ '/collaborate/community/' | relative_url }}">community collaboration</a>. For background on the company and its work, visit <a href="{{ '/about/' | relative_url }}">About Us</a>.</p>
</section>
