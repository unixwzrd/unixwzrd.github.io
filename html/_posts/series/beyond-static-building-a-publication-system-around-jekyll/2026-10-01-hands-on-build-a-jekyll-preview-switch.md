---
short_url: "https://unixwzrd.ai/s/ae4932cc7d/"
short_link_basis: "/_posts/2026-10-01-hands-on-build-a-jekyll-preview-switch.md"
layout: post
title: "Hands-On: Build a Jekyll Preview Switch"
date: 2026-10-01 10:00:00 -0500
categories: [hands-on]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "Build one small Jekyll fixture in current and review modes, then prove which posts each mode includes without touching your site server."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: "2A"
series_order: 25
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_companion_of: 2
series_previous_title: "A Local Jekyll Server I Can Actually Operate"
series_previous_url: /technology/2026/10/01/a-local-jekyll-server-i-can-actually-operate/
series_next_title: "Building the Site from Shared Layouts, Includes, and Data"
series_next_url: /technology/2026/10/08/building-the-site-from-shared-layouts-includes-and-data/
series_next_date: 2026-10-08 08:00:00 -0500
image: /assets/images/blog/jekyll-site-tooling/post-02-local-preview-hero.png
---

The main [Part 2 article]({{ page.series_previous_url | relative_url }}) explains why I want two local views: one for the material I am editing and one for the content that should be visible today. My site's `jekyll-site` command makes that choice when it starts the local server. Here is the smallest version of the same content switch I could make useful. It uses an invented Jekyll site with four posts and writes two separate builds, so there is no reason to start or stop your real site server.

The interesting result is not a clever shell script. It is being able to say exactly which material each mode includes and then check that claim against the generated HTML.

<!--more-->

## The Boundary of This Exercise

The package contains a tiny Jekyll site, a `preview.sh` wrapper, and a `verify.sh` check. The fixture has one ordinary post, one far-future post, one Markdown draft, and one post marked `published: false`. Each has a distinct marker. The wrapper builds either `current` or `review` into a fixed directory beneath the lab.

This is a build-only exercise. It does not serve a port, manage a PID, refresh project metadata, run Pagefind, or copy any of my site's plugins and layouts. Those are responsibilities of the real site wrapper. The lab isolates the content-selection decision that the two wrappers have in common.

Download the [complete preview lab]({{ '/assets/code/jekyll-site-tooling/post-02a/jekyll-preview-lab.zip' | relative_url }}) and its [SHA-256 checksum]({{ '/assets/code/jekyll-site-tooling/post-02a/jekyll-preview-lab.zip.sha256' | relative_url }}). The two scripts and README are also readable here:

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-02a/preview-lab/README.md" language="markdown" title="README.md" %}

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-02a/preview-lab/preview.sh" language="bash" title="preview.sh" %}

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-02a/preview-lab/verify.sh" language="bash" title="verify.sh" %}

## Run Both Views

The lab needs Ruby, Bundler, and the Jekyll gems declared in its Gemfile. After downloading the archive and checksum to one directory, verify the archive, extract it, and work inside its own folder:

```bash
shasum -a 256 -c jekyll-preview-lab.zip.sha256
unzip jekyll-preview-lab.zip
cd preview-lab
bundle install
./preview.sh current
./preview.sh review
./verify.sh
```

`current` omits the extra inclusion flags. `review` supplies `--future --drafts --unpublished`. The wrapper uses `jekyll build` for both modes and writes to `out/current/` and `out/review/`. It never selects a path outside the extracted lab.

The expected result is `PASS: current has one post; review has all four`. You can open either generated `index.html` in a browser or inspect the markers directly. The current index should contain only `CURRENT-POST-MARKER`; the review index should also contain the future, draft, and unpublished markers.

## Map the Lab Back to My Site

Here is the exact point of contact with the way I operate the site. In `utils/bin/jekyll-site`, the normal `start` path eventually runs a development `jekyll serve` with `--future --drafts --unpublished`. Passing `--current` removes those three flags. The lab's `review` and `current` builds exercise that same inclusion choice against four invented posts. You can inspect both `serve_flags` assignments in the site's wrapper without running it:

```bash
rg -n 'serve_flags=|JEKYLL_ENV=production|JEKYLL_ENV=development|run_pagefind_index' utils/bin/jekyll-site
```

The rest of our command matters just as much operationally. Before either serve mode, `jekyll-site start` can refresh project OpenGraph data, then clears generated output, runs a production Jekyll build, and makes a Pagefind index. Only then does it launch the development server and write its PID file. `start -n` skips the metadata refresh, but still builds, indexes, and starts the server. `restart` also stops the old process and skips refresh by default. The lab does none of those things, and it does not set `JEKYLL_ENV` to imitate either stage. Its two HTML outputs demonstrate content inclusion only.

This explains a practical surprise: a future post can appear in the local review browser while the Pagefind index was built from the earlier production-stage output. I do not treat finding that post in the page as proof that local search has indexed it. The lab lets you see the selection difference directly; the real workflow still needs separate checks for search and the final built site.

{% include blog_diagram.html
   src="/assets/images/blog/jekyll-site-tooling/post-02-preview-path.svg"
   alt="The real site wrapper first prepares a build and search index, then starts a development server whose review mode includes future, draft, and unpublished posts while current mode omits those flags."
   caption="This lab isolates the content switch at the right; it does not reproduce the full site wrapper."
   variant="series" %}

## Change One Thing and Check Again

Edit the invented future post's date to a date in the past, then run `./verify.sh` again. The check should fail because its expectation is now wrong: that marker belongs in the current view too. This is a useful failure. The script is making a claim about content selection, not merely checking that Jekyll exited zero.

Restore the future date and rerun the check. Then try `./preview.sh other` to see the wrapper reject an unknown mode before building anything. The script deliberately has only two accepted choices and fixed output destinations.

If you adapt this pattern for a real site, decide where the generated output goes and what a build or restart does beyond Jekyll itself. My site's wrapper, for example, can refresh project data and replace its generated output before it serves. That is why I would not lift this teaching script into production unchanged.

## Current State

The fixture gives a repeatable way to see the difference between a current-content build and a review-inclusive build. The verification checks the generated HTML for the expected posts. It proves that bounded behavior for this invented fixture under the Jekyll version you run; it does not prove the behavior of a different site's layouts, plugins, or deployment.

## Next Work

Part 3 moves from selecting content into rendering it. I will follow the site's layout hierarchy and the Liquid includes that let one project definition appear in several places without repeating the same page structure.
