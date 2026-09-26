---
short_url: "https://unixwzrd.ai/s/05935819b6/"
short_link_basis: "/_posts/2026-10-08-hands-on-find-the-limits-of-a-jekyll-metadata-check.md"
layout: post
title: "Hands-On: Find the Limits of a Jekyll Metadata Check"
date: 2026-10-08 10:00:00 -0500
categories: [hands-on]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "Run the site's taxonomy plugin against invented posts and see both the bad metadata it rejects and the mistake a successful build still lets through."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: "3A"
series_order: 35
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_companion_of: 3
series_previous_title: "Building the Site from Shared Layouts, Includes, and Data"
series_previous_url: /technology/2026/10/08/building-the-site-from-shared-layouts-includes-and-data/
series_next_title: "Stable URLs in a Repository That Keeps Moving"
series_next_url: /technology/2026/10/15/stable-urls-in-a-repository-that-keeps-moving/
series_next_date: 2026-10-15 08:00:00 -0500
image: /assets/images/blog/jekyll-site-tooling/post-03-shared-layouts-hero.png
---

I have a lot of fields at the top of a post now. It would be nice if "Jekyll build complete" meant I got every one of them right. It doesn't. The site's strict taxonomy check has a specific job, and I need to know where that job ends.

The [Part 3 article]({{ page.series_previous_url | relative_url }}) follows one project page through layouts, includes, and data. This companion puts a few invented posts through the site's current tag-taxonomy plugin. Some fail exactly as they should. One has a missing series order and passes. That pass is the point of the exercise.

<!--more-->

## Use the Real Check on Invented Material

The lab includes a frozen, unchanged copy of `html/_plugins/03_tag_taxonomy_validator.rb` from this site, a small invented tag taxonomy, and seven invented post cases. It does not copy the site's real project catalog or posts. Each case gets its own Jekyll build under the lab's `out/` directory; the runner checks both the exit status and the expected error text.

The site plugin checks canonical tags and optional `content_type` values for posts under `_posts`. It skips actual `_drafts` paths during draft-inclusive preview. It does not require every field that layouts and series pages use. The lab tests that boundary with the plugin itself rather than with a new lookalike validator.

Download the [complete taxonomy lab]({{ '/assets/code/jekyll-site-tooling/post-03a/jekyll-taxonomy-lab.zip' | relative_url }}) and its [SHA-256 checksum]({{ '/assets/code/jekyll-site-tooling/post-03a/jekyll-taxonomy-lab.zip.sha256' | relative_url }}). The README, runner, small taxonomy, and plugin snapshot are available to read or download separately:

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-03a/taxonomy-lab/README.md" language="markdown" title="README.md" %}

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-03a/taxonomy-lab/run_lab.sh" language="bash" title="run_lab.sh" %}

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-03a/taxonomy-lab/site/_data/tag_taxonomy.yml" language="yaml" title="tag_taxonomy.yml" %}

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-03a/taxonomy-lab/site/_plugins/03_tag_taxonomy_validator.rb" language="ruby" title="03_tag_taxonomy_validator.rb" %}

## Run the Cases

The package needs Ruby, Bundler, and Jekyll 4.3-compatible gems. Put the archive and checksum in one directory, then verify and extract it:

```bash
shasum -a 256 -c jekyll-taxonomy-lab.zip.sha256
unzip jekyll-taxonomy-lab.zip
cd taxonomy-lab
bundle install
./run_lab.sh
```

You should see seven `PASS` lines. The valid post is accepted. Unknown, retired-alias, and duplicate tags are rejected, as is an unknown `content_type`. The case named `missing-series-order` is accepted even though its series metadata is incomplete. The old-tag draft is also accepted when Jekyll includes drafts, because the plugin deliberately leaves `_drafts` alone until that work moves into a publishable post tree.

The runner keeps each build log and its generated output under `out/`. Open the log for a rejected case if you want to see the exact Jekyll error. No case runs against your real site or changes a live post.

{% include blog_diagram.html
   src="/assets/images/blog/jekyll-site-tooling/post-03-metadata-contract.svg"
   alt="Authored front matter feeds layouts, discovery lists, and series views, while only tags and content type pass through the current strict taxonomy check."
   caption="The lab exercises the checked branch. The other branches still need their own review."
   variant="series" %}

## The Pass That Should Make You Pause

Take a look at `cases/missing-series-order.md`. Its tags are valid, and it has a series name, but no `series_order`. The taxonomy validator accepts it because series order is not one of its checks. The real site's series index uses that field to set reading order. This little fixture has no series index, so its successful build proves only that the taxonomy check did not catch the omission. It says nothing about where the article would appear in the real series. That is the editorial question I still need to answer.

The same gap applies to a wrong project `category`, a broken image path, or a next-article link that points somewhere else. The real site's layouts and includes will use those values, but this particular plugin will not certify them. That is why I look at the rendered page and the surrounding series after the mechanical checks pass.

There is an older front-matter utility in this repository that can add missing title, image, and excerpt fields by editing files. This lab does not run it. Nor does it run the site's short-link checks, redirect checks, pre-commit chain, or deployment workflow. The point here is to make one active validator's responsibility visible, not to rename a small lab "the publishing pipeline."

## Current State

The same taxonomy plugin this site uses rejects the invented invalid tags and content type. It allows an incomplete series entry because that field is outside its remit, and it allows an actual draft to keep an old tag while I am still working on it. I can inspect those results and the retained logs without touching my site's content.

That is a useful check with a clear boundary. I want it in the build. I also want to know when to stop asking it a question it was never written to answer.

## Next Work

Part 4 moves to another field that a successful page build can hide: the identity of a public URL. I will trace how the site keeps project-post links stable when source paths and titles change.
