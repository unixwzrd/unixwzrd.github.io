---
short_link_basis: "/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-15-stable-urls-in-a-repository-that-keeps-moving.md"
short_url: "https://unixwzrd.ai/s/213165a2ee/"
layout: post
title: "Stable URLs in a Repository That Keeps Moving"
date: 2026-10-15 08:00:00 -0500
categories: [technology]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "I can reorganize the source all I want, but a link I have already given somebody needs a more deliberate kind of change."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: 4
series_order: 40
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_previous_title: "Building the Site from Shared Layouts, Includes, and Data"
series_previous_url: /technology/2026/10/08/building-the-site-from-shared-layouts-includes-and-data/
series_next_title: "From a YAML Project Catalog to a Project Publishing System"
series_next_url: /technology/2026/10/22/from-a-yaml-project-catalog-to-a-project-publishing-system/
series_next_date: 2026-10-22 08:00:00 -0500
series_companion_title: "Hands-On: Keep a Short Link Through a Source Move"
series_companion_url: /hands-on/2026/10/15/hands-on-keep-a-short-link-through-a-source-move/
series_companion_date: 2026-10-15 10:00:00 -0500
image: /assets/images/blog/jekyll-site-tooling/post-04-stable-urls-hero.png
---

I have moved a lot of files around in this repository. Organizing the source is my problem. A reader who saved a link to an article should not have to care which directory I decided to put the Markdown in this week.

I also share articles on X/Twitter, Bluesky, and other places where a post has limited room. A long URL takes space I would rather use to say something about the article. I could send those links through an external shortening service, but I wanted the short links and their redirects to live in the Jekyll site I already manage. They are our links to keep working, not a provider's links that I have to hope will keep pointing the right way.

That made the public address worth protecting. Jekyll can make a URL feel like a side effect of the source. A title changes, a filename gets cleaned up, or I put a post under a different directory, and suddenly I have to ask whether the address I already shared still works. Part 3 was about letting layouts and includes share the presentation. This is the other side of that work: giving a published page an identity that survives my housekeeping.

<!--more-->

## A Project Post Needs a Frozen Address

Project posts used to get title-derived URL paths. That was convenient until a title changed. A title is editorial text; I want to be able to improve it without making old links disappear. The current project-post plugin requires a `permalink_slug` in front matter and uses it for the final path instead of generating a slug from the current title.

Here is the small contract for an invented project post:

```yaml
title: A Better Title for Example Tool
date: 2026-10-15 08:00:00 -0500
permalink_slug: example-tool-introduction
```

If that file lives under `projects/ExampleTool/_posts/`, the plugin builds `/projects/ExampleTool/2026/10/15/example-tool-introduction/`. It rejects a missing slug or one that is not already normalized to its lowercase, hyphenated form. I can edit the title or the source filename without changing that final segment.

There is a limit I have to remember: the slug is only one piece of the route. The project directory name and the post's publication date supply the other pieces. Moving the file to a different project or changing the front-matter date would change the canonical path. I do not casually edit those values after publication either.

The changelog records the point where this became a formal rule. On August 21, 2026, the project posts gained explicit slugs, and 26 former title-based paths were kept as compatibility redirects. That is a record of the migration, not a promise that every old URL anyone might have invented is covered.

## Let the Old Path Point to the New One

When a project post has an old public path, I can declare it with `legacy_project_permalink`. The project-post plugin puts that path into `redirect_from`, and Jekyll's redirect plugin writes a redirect page pointing to the current canonical route. A current post can therefore keep its short, frozen slug while an older title-derived link still reaches it.

That old path has to be explicit. The plugin does not search the internet for links I may have shared, and it does not infer every title the article ever had. The project redirect verifier checks that a declared legacy path generated a page and that the page points at the canonical path. It is checking the build output, not pinging the deployed website.

{% include blog_diagram.html
   src="/assets/images/blog/jekyll-site-tooling/post-04-url-contract.svg"
   alt="A project post's directory, date, and frozen permalink slug form its canonical URL. A declared legacy project permalink redirects there. An immutable short-link basis and configured origin form a separate deterministic short redirect to the same page."
   caption="The source file, canonical path, old path, and short link have different jobs."
   variant="series" %}

## The Short Link Has a Different Identity

The point was to give those social posts a compact address that still belonged to this site. I did not need a hand-written list of arbitrary codes to do it. The current short-link plugin takes the configured site origin and a `short_link_basis`, hashes them with SHA-256, and uses the first ten hexadecimal characters for a `/s/` path. That path is added to `redirect_from`, so Jekyll generates the redirect to the article's current canonical URL as part of the site.

The important field is `short_link_basis`. I store a source-like path in front matter and treat it as an immutable identifier. It can keep saying where the post *started* even after the actual Markdown moves. The source organization can change; the hash input does not. If I omit the basis, the plugin falls back to the current source path. That is compatible with older material, but the short code can then change when the file moves. A stable short link needs the stored basis, not just a deterministic hash.

That control matters when I change a page's naming convention. With the basis left alone, the `/s/` link I already shared can stay the same while Jekyll builds its redirect to the page's current canonical address. If the old full-length page URL also needs to keep working, that is a separate redirect I must preserve. Owning the short link gives me the option to manage both paths here, but it does not make every old page address survive automatically.

Posts get short links by default. Pages can opt in with `short_link: true`, as this series landing page does. If a post already declares `short_url` and it disagrees with the value calculated from the basis, the build fails. The plugin also checks for a ten-character code collision among the eligible items it sees. The backfill script can write or check these front-matter fields, but I still review any edit to an identity value before accepting it.

The [Hands-On 4A companion]({{ page.series_companion_url | relative_url }}) runs a frozen copy of that plugin on invented items. It shows the same code after a source move with an explicit basis, a changed code when the fallback path moves, and the failure for a declared URL that does not match. Nothing in that lab touches a live post.

## A Green Build Is One Check, Not the Whole Story

The plugin assigns the short redirect after project-post permalinks have been set. The Pages workflow then builds the production site and runs three relevant checks: the front-matter short-link check, a check that generated short redirect files exist, and a check that project canonical and declared legacy outputs exist and line up. Those are useful, concrete checks before deployment.

They do not tell me that a reader can reach the domain from outside the build environment. They also do not decide whether changing a published date is editorially acceptable. The generated pages and their redirects have to be correct, and I still have to treat public links as commitments once I share them.

One more scope detail matters. This frozen `permalink_slug` rule is for project-scoped posts. Ordinary Technology and Hands-On series posts use their own date, category, and slug routes. I keep their publication identity stable too, but I should not claim that the project-post plugin is enforcing it for them.

## Current State

Project posts have explicit slug segments, and declared older project paths can redirect to their current canonical pages. Short links use a separate frozen basis, so a source-directory move or deliberate page-naming change does not have to change a shared `/s/` address. Those short addresses and redirects are under this site's control. The build and CI check the generated pieces that implement those promises.

That gives me room to clean up the repository without casually breaking the paths readers already have. It also makes the exceptions visible: a changed date, project directory, missing basis, or undeclared old route still needs my attention.

## Next Work

Stable links are one part of giving a project a proper home. Part 5 starts earlier in the pipeline: the YAML project catalog, generated metadata and cards, scaffolded pages, and the Liquid views that put a new project where readers can find it.
