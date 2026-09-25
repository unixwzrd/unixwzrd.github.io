---
short_url: "https://unixwzrd.ai/s/571cb24d83/"
short_link_basis: "/_posts/2026-10-01-a-local-jekyll-server-i-can-actually-operate.md"
layout: post
title: "A Local Jekyll Server I Can Actually Operate"
date: 2026-10-01 08:00:00 -0500
categories: [technology]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "A useful preview has to show work in progress without confusing it with the current publication. Here is what my Jekyll wrapper actually does."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: 2
series_order: 20
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_previous_title: "Jekyll, One Problem at a Time"
series_previous_url: /technology/2026/09/22/jekyll-one-problem-at-a-time/
series_next_title: "Building the Site from Shared Layouts, Includes, and Data"
image: /assets/images/blog/jekyll-site-tooling/post-02-local-preview-hero.png
---

A future-dated post can be perfectly good and still be invisible when I open the local site. That is irritating when the whole point of starting the server is to see what I am writing. But I also need to check the site without that work in progress mixed in. Those are two different questions, and I want to ask either one without rebuilding a command line from memory each time.

The first installment was about how a string of ordinary Jekyll frustrations grew into a publishing workflow. This is one of the smaller, more practical fixes: a wrapper around the local build and server. It is useful precisely because it makes the choice between an editorial view and a current-content view explicit.

<!--more-->

## Two Views, Two Questions

When I am editing next week's article, I want to see its layout, image, links, and place in the series. The normal `jekyll-site start` path serves with `--future`, `--drafts`, and `--unpublished`. That lets me review future-dated posts, Markdown drafts, and posts marked `published: false` in the local browser. It does not make any of them public.

When I want to see the site without those extra categories, I use `jekyll-site start --current`. That omits the three inclusion flags. It is a useful approximation of the content visible today, and it is a different editorial question from "does my upcoming post look right?" I can also use `--current` with `restart`.

The name needs a little care. `--current` changes which material the server includes; it does not turn that server into a production build. In both modes, the wrapper launches `jekyll serve` with `JEKYLL_ENV=development`. A current-content preview can tell me whether a scheduled post disappears from the local listing. It cannot, by itself, certify the exact production output, its canonical metadata, or a deployed page.

There is another wrinkle in the series listing itself. The shared series index intentionally filters out `_drafts` files and posts marked `published: false`. A draft can be served locally and still not appear as a normal installment on that landing page. For a scheduled article whose position I want to inspect in the series, I use a future-dated post in the post tree. That is why preview mode and a deliberate publication date matter together.

## What the Wrapper Does Before Serving

I called the command `jekyll-site`, but `start` is more than a thin alias for `bundle exec jekyll serve`. The script changes into the repository, loads its local environment, checks a PID file, and looks for a process on its configured local port. Then it builds the site before it starts the server.

That build step uses `JEKYLL_ENV=production`. It clears the existing Jekyll cache and generated site output, runs a full Jekyll build, and generates a Pagefind index from the resulting pages. By default, `start` also refreshes OpenGraph project data before the build. I can skip that refresh with `-n`, or request a fresh start when the project metadata is the thing I need to inspect. The link checker is optional with `-c`.

After all that, the wrapper starts the *development* server with the chosen preview flags. So one invocation contains two stages with different jobs: a production-style build and index preparation, followed by a local development preview. The first stage is not a promise that the later watched preview will keep the Pagefind index in step with every edit. If I am checking search behavior, I need to verify the generated index and the rendered page I am actually looking at.

{% include blog_diagram.html
   src="/assets/images/blog/jekyll-site-tooling/post-02-preview-path.svg"
   alt="The jekyll-site start command optionally refreshes project metadata, clears generated output, makes a production Jekyll build and Pagefind index, then starts a development Jekyll server. The default server includes future posts, drafts, and unpublished posts; current mode omits those flags."
   caption="One start command prepares build output, then serves one of two local content views."
   variant="series" %}

That sequence is worth understanding before treating `start` as a harmless status check. The build replaces generated output. The default refresh can update project data. If another process has the local port, the wrapper tries to terminate it, first normally and then forcibly. I use the wrapper as an operator command, not as something to run just to discover whether a page exists.

## Edit the Post, Refresh the Browser

Once the server is running, ordinary content edits do not require a fresh `jekyll-site build` or a restart. Jekyll's serve process watches the source and regenerates affected output. I edit the Markdown or a template, wait for that rebuild, and reload the page. The preview is meant to shorten that loop, not add another command to every paragraph.

There are still reasons to restart. Changing the preview mode changes the server flags. The Jekyll configuration file is not reloaded automatically by `jekyll serve`, so changes there require a restart. If I need a fresh project-data pull or a clean full build, that is a conscious operation too. The wrapper's `restart` path skips the OpenGraph refresh by default; `-r` requests it. `-n` wins if both refresh switches are supplied, which the script warns about.

The PID file is a convenience, not an all-knowing service manager. The script checks whether that PID still exists and whether its command looks like Jekyll. It also checks the local port separately. There is no public `status` subcommand in `jekyll-site` today, even though older service documentation suggests one elsewhere. I would rather describe the command that exists than promise a polished daemon interface it does not have.

## Preview Is a Review Step

The most useful thing about this setup is the separation of questions. In editorial mode I can inspect tomorrow's article in context. In current mode I can look for accidental inclusion of unfinished work. In the production build and later checks I can examine the artifact that is meant for publication. Those views overlap, but they are not interchangeable.

I also do not need a second file-watching service to get the normal edit-and-reload loop. Jekyll already watches the source while serving. There is older watcher code in this repository, but it is not part of how I operate the site now. Keeping that distinction clear prevents a historical experiment from turning into a fictional dependency in the story.

This is still a personal operator tool. It assumes the site's local environment, Ruby setup, generated-data workflow, and chosen port. That is fine for my site. The useful pattern is not the exact shell script. It is deciding which preview question I am asking, making that choice visible in the command, and knowing which steps have side effects before I run them.

## Current State

`jekyll-site` gives me a repeatable local build and preview path. A normal start includes future, draft, and unpublished content; `--current` leaves those inclusions off. Both run a development server after a separate production build and Pagefind indexing step. Ordinary edits then use Jekyll's own rebuild loop. Restarting or refreshing project metadata is an explicit choice, with consequences I can inspect.

## Next Work

A predictable preview only helps if the pages themselves are built consistently. Next I will follow a project page through Jekyll's layout hierarchy and the shared Liquid includes that keep menus, project details, and blog lists from being copied into every page.
