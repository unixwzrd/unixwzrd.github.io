---
short_url: "https://unixwzrd.ai/s/472134b8b4/"
short_link_basis: "/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-22-hands-on-follow-a-project-through-the-catalog.md"
layout: post
title: "Hands-On: Follow a Project Through the Catalog"
date: 2026-10-22 10:00:00 -0500
categories: [hands-on]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "Run an offline copy of the project generator on three invented repositories and inspect the data and scaffolding it produces."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: "5A"
series_order: 55
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_companion_of: 5
series_previous_title: "From a YAML Project Catalog to a Project Publishing System"
series_previous_url: /technology/2026/10/22/from-a-yaml-project-catalog-to-a-project-publishing-system/
series_next_title: "Diagrams and Source Code That Behave Like Editorial Content"
image: /assets/images/blog/jekyll-site-tooling/post-05-project-catalog-hero.png
---

I can describe the project catalog all day, but I find it easier to understand once I can see what a single refresh writes. This lab runs a frozen copy of the current project generator against three invented repositories. It keeps the experiment out of the real site and replaces GitHub requests and image rendering with local stand-ins.

The [Part 5 article]({{ page.series_previous_url | relative_url }}) follows the whole publishing path. Here I am testing a smaller claim: project order survives generation, my overrides win where I supply them, visibility changes the generated fields, and a new project gets starter files. The menu and page still need a Jekyll build; this Python run does not render them.

<!--more-->

## Run the Invented Catalog

Download the [project catalog lab]({{ '/assets/code/jekyll-site-tooling/post-05a/project-catalog-lab.zip' | relative_url }}) and its [SHA-256 checksum]({{ '/assets/code/jekyll-site-tooling/post-05a/project-catalog-lab.zip.sha256' | relative_url }}). The runner uses Python 3 plus the generator's existing `requests`, `PyYAML`, and `beautifulsoup4` dependencies. It writes only into a temporary directory and removes that directory when it finishes.

You can inspect the instructions and runner first:

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-05a/project-catalog-lab/README.md" language="markdown" title="README.md" %}

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-05a/project-catalog-lab/run_lab.py" language="python" title="run_lab.py" %}

With the ZIP and checksum in one directory:

```bash
shasum -a 256 -c project-catalog-lab.zip.sha256
unzip project-catalog-lab.zip
cd project-catalog-lab
python3 run_lab.py
python3 run_lab.py --reorder
python3 run_lab.py --show-hidden
```

In the first run, Example Tool has both a fetched description and a manual description. Look for the manual one in the printed result. Quiet Tool has no fetched metadata and is marked private; it gets a page but no repository URL in its generated entry. Hidden Tool is marked `none`; it remains in generated data so the site's Liquid views can filter it.

Now compare the two variations. `--reorder` moves Quiet Tool ahead of Example Tool in the invented input, and the printed generated order changes with it. `--show-hidden` changes Hidden Tool's visibility to public; its generated entry gains a repository URL. The runner checks each result before printing `PASS`. The commands do not edit this site's YAML or render its menus, but they let you change the same inputs those later views consume.

{% include blog_diagram.html
   src="/assets/images/blog/jekyll-site-tooling/post-05-publishing-paths.svg"
   alt="The lab exercises the ordered repository input through the project generator and generated data, including first-page scaffolding; it does not exercise the separate Blog sections path or rendered Liquid menus."
   caption="This run exercises the project-generator branch. The reader-facing menus are the next build's job."
   variant="series" %}

## Read the Result Carefully

The runner also checks for Example Tool's landing page, draft template, and draft-marked starter introduction. Those files show what the generator *starts*. They do not make the introduction ready to publish. I would still review the words, image, route, tags, and any private detail before treating it as an actual project announcement.

The lab stubs the network and card renderer on purpose, so it does not prove GitHub availability, image rendering, or the final HTML. It does execute the current generator's project-entry and scaffolding code. If its assertions pass, they support those particular behaviors on the frozen snapshot included in the archive.

## Next Work

The generated card and page give a project a place to start. Part 6 looks at how diagrams and source files inside an article become useful editorial material rather than a pile of attachments.
