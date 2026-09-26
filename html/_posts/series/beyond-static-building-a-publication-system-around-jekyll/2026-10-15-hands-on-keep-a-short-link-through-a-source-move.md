---
short_link_basis: "/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-15-hands-on-keep-a-short-link-through-a-source-move.md"
short_url: "https://unixwzrd.ai/s/d73dbf7bb9/"
layout: post
title: "Hands-On: Keep a Short Link Through a Source Move"
date: 2026-10-15 10:00:00 -0500
categories: [hands-on]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "Run the site's short-link calculation on invented posts and watch what stays fixed when a source path changes."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: "4A"
series_order: 45
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_companion_of: 4
series_previous_title: "Stable URLs in a Repository That Keeps Moving"
series_previous_url: /technology/2026/10/15/stable-urls-in-a-repository-that-keeps-moving/
series_next_title: "From a YAML Project Catalog to a Project Publishing System"
series_next_url: /technology/2026/10/22/from-a-yaml-project-catalog-to-a-project-publishing-system/
series_next_date: 2026-10-22 08:00:00 -0500
image: /assets/images/blog/jekyll-site-tooling/post-04-stable-urls-hero.png
---

I put short links into this site so I could share articles on X/Twitter, Bluesky, and other places with tight post lengths without depending on an external redirect service. I want those links under our control, including when I change how the article's page is named. If I calculate a short link from a source path and then reorganize the source, though, the same calculation gives me a different link. That is exactly what I was trying to avoid.

The [Part 4 article]({{ page.series_previous_url | relative_url }}) explains the separate identities involved. Here I want to make one piece of that behavior visible: the site's current short-link module, an invented post, and a simulated file move. The exercise is small enough to run without building this website.

<!--more-->

## Run the Module Against Invented Posts

Download the [short-link lab]({{ '/assets/code/jekyll-site-tooling/post-04a/jekyll-short-link-lab.zip' | relative_url }}) and its [SHA-256 checksum]({{ '/assets/code/jekyll-site-tooling/post-04a/jekyll-short-link-lab.zip.sha256' | relative_url }}). The archive contains an unchanged snapshot of this site's `01_short_link_injector.rb` and a Ruby runner that supplies tiny stand-ins for Jekyll post and site objects. There are no real posts, credentials, or network calls in the lab.

You can inspect the material before running it:

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-04a/short-link-lab/README.md" language="markdown" title="README.md" %}

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-04a/short-link-lab/run_lab.rb" language="ruby" title="run_lab.rb" %}

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-04a/short-link-lab/source/01_short_link_injector.rb" language="ruby" title="01_short_link_injector.rb" %}

Put the ZIP and checksum together, then run:

```bash
shasum -a 256 -c jekyll-short-link-lab.zip.sha256
unzip jekyll-short-link-lab.zip
cd short-link-lab
ruby run_lab.rb
```

The first check makes two invented posts with different `relative_path` values but the same frozen `short_link_basis`. They get the same short URL and the same `/s/` redirect path. The second check omits the basis, so moving the source changes the hash input and the code. The third declares a wrong `short_url` and checks that the module rejects it.

{% include blog_diagram.html
   src="/assets/images/blog/jekyll-site-tooling/post-04-url-contract.svg"
   alt="For project posts, a canonical URL, declared legacy redirect, and basis-derived short redirect are separate paths to the same article. This lab exercises only the short-link calculation."
   caption="This lab exercises the short-link branch, not the complete Jekyll redirect build."
   variant="series" %}

## What That Result Means

The runner uses the actual module's hash and validation logic. It does not ask Jekyll to write redirect pages. The public site still needs its normal build, its post-build redirect checks, and a look at the served result. This lab shows why I store the basis before I start moving files around; it does not certify a deployed link.

It also shows a trap in the word *deterministic*. A hash can be perfectly deterministic and still produce a new address if I change its input. The immutable input is the useful part of the design.

## Current State

With a frozen basis, the invented source move leaves the short link alone. Without it, the fallback path moves and the link changes. The module catches a declared `short_url` that disagrees with its calculation. All three cases run without modifying the website.

## Next Work

Part 5 follows the project itself from authored YAML into generated data, cards, pages, menus, and project blog lists. That is where stable routes become one part of a larger project publishing path.
