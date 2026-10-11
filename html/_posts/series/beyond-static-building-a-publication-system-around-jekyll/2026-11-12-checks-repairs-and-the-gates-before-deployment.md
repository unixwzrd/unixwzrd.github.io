---
short_link_basis: "/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-11-12-checks-repairs-and-the-gates-before-deployment.md"
short_url: "https://unixwzrd.ai/s/661f384344/"
layout: post
title: "Checks, Repairs, and the Gates Before Deployment"
date: 2026-10-11 11:15:00 -0500
categories: [technology]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "A successful Jekyll build is useful, but it is not my entire publishing decision. Here is what the local checks, commit hook, and Pages workflow actually do."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: 8
series_order: 80
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_previous_title: "Proofreading a Blog by Listening to It"
series_previous_url: /technology/2026/10/11/proofreading-a-blog-by-listening-to-it/
series_companion_title: "Hands-On: Build a Small Prepublication Check Runner"
series_companion_url: /hands-on/2026/10/11/hands-on-build-a-small-prepublication-check-runner/
series_companion_date: 2026-10-11 11:30:00 -0500
series_next_title: "Monitoring a Static Site After Deployment"
image: /assets/images/blog/jekyll-site-tooling/post-08-checks-and-gates-hero.png
redirect_from:
  - /technology/2026/11/12/checks-repairs-and-the-gates-before-deployment/
---

I can finish an article, listen to it, fix the sentence that sounds wrong, and still ship a broken link. Jekyll might build the page perfectly well. That does not mean the short URL points where I expect, the image path has the right case, or the project data in the generated site is the version I meant to publish.

That is why this site has accumulated so many checks. Some came from a specific failure. Others came from being tired of finding the failure only after a push. At this point there are enough scripts in `utils/bin` that it is tempting to say “the pipeline checks everything.” It doesn't. Some checks only warn, some repair files, and the GitHub Pages job runs a narrower set than my local machine. I need to know which gate I am actually standing at.

<!--more-->

## The Small Checks Catch Different Mistakes

The numbered scripts under `utils/bin/checks` cover environment dependencies, permalinks, Jekyll doctor, source links, generated-site links, external links, large files, a strict build, required files, Liquid syntax, front matter, navigation, image paths, and text cleanup. The runner, `utils/bin/check_site.sh`, calls the matching shell scripts in filename order and stops when one exits unsuccessfully. It accepts `--list`, `--run`, and `--skip` for a narrower pass.

I like having a quick way to ask one question while I am editing. A short-link check is a different question from whether the complete site builds. The Ruby short-link tools verify the front-matter identity and generated redirects; the taxonomy checker asks whether I used canonical tags. A production build is still needed to see what Liquid and the plugins actually produce. None of these checks decides whether the article is clear, whether a diagram tells the truth, or whether I meant to publish it today.

For a quick inventory or one focused gate, the runner accepts an extensionless check name:

```bash
./utils/bin/check_site.sh --list
./utils/bin/check_site.sh --run 03_jekyll_doctor
```

That second command invokes Jekyll doctor in the current checkout. On my case-insensitive macOS filesystem it reports URLs that differ only by case and exits 1; its wrapper treats that as a warning unless `STRICT_JEKYLL_DOCTOR=1` is set. So “the runner passed” still requires reading what it printed.

Some names in the numbered directory sound stronger than their implementation. The Liquid syntax step searches files for a `for` without an `endfor`, or an `if` without an `endif`, prints warnings, and exits successfully. The navigation step also warns and returns success. I would not treat either as a parser or as a deployment blocker. The real Jekyll build does more useful work on Liquid, but a successful build still does not read the article for me.

{% include blog_diagram.html
   src="/assets/images/blog/jekyll-site-tooling/post-08-check-boundaries.svg"
   alt="Article source goes through focused checks, the local numbered suite, review of changed files and rendered output, a human push decision, the Pages workflow, and deployment. A repair path returns from review to source."
   caption="Each gate answers a different question; review and the push decision remain mine."
   variant="series" %}

The editable [Graphviz source]({{ '/assets/code/jekyll-site-tooling/post-08/check-boundaries.dot' | relative_url }}) is available if you want to change the flow for your own site.

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-08/check-boundaries.dot" language="text" title="check-boundaries.dot" %}

## A Check That Changes the Thing It Checks

Here is the awkward part: the full numbered suite is not a read-only inspection. Its environment step may install missing Python packages. Its project-data step calls `fetch_og.py` and can stage generated YAML, pages, and images. The front-matter step inserts missing fields. The image-path step can rewrite paths and updates a local timestamp. The cleanup step can rewrite changed text files and re-stage those already in the index. The build and HTMLProofer steps also replace build output. That is useful work when I have chosen it, but it is not the command I run just to ask “what would change?”

The internal generated-site link check builds again before HTMLProofer examines `_site`; the external link check is normally skipped unless `CHECK_EXTERNAL_LINKS=1` is set. That external pass depends on the network and can run into rate limits or temporary failures. `jekyll-site -c` is another explicit way to request the generated-site HTMLProofer pass during a build. These are separate entry points with overlapping work, not one magical validator hiding behind a single name.

There is a particularly good reminder in the installed pre-commit hook. Its comment says it skips the project-data refresh, and it calls:

```bash
./utils/bin/check_site.sh --skip 05_update_project_data.sh
```

The runner removes `.sh` before it compares check names. So that argument does **not** match `05_update_project_data` in the current checkout. The refresh step is still selected. That is a real bug in the local hook contract, and it means I cannot honestly describe the hook as a non-mutating validation pass. I check the staged diff again after it runs, especially when a tool can stage something for me. A hook can stop a bad commit; it can also change the material I thought I was committing.

The repository has a separate `.pre-commit-config.yaml` with focused short-link and tag hooks. That file is configuration for the optional `pre-commit` framework. It does not prove those hooks are installed in a particular clone, and it is not the installed shell hook described above. The difference matters when somebody follows these instructions on their own checkout.

## What Happens After I Push

The GitHub Pages workflow starts on a push to `main` or a manual dispatch. It checks out the repository, installs Ruby dependencies, clears the old output and Jekyll cache, and runs a production Jekyll build. Then it checks short-link front matter and generated redirects, verifies project permalink redirects, and runs the tag taxonomy checker before uploading the built site and deploying Pages.

A future date in a post is not a deployment timer. The production build excludes that post until its date arrives, and this workflow has no scheduled rebuild. I checked on October 11: Part 3 was dated October 8, but its live URL still returned 404. The [last successful Pages run](https://github.com/unixwzrd/unixwzrd.github.io/actions/runs/37534099551) was October 6. Nothing had rebuilt the site after Part 3 became eligible. The source can be sitting on `main` while its page is still missing from Pages. I have to check the live route after the next deployment, not infer publication from Git history.

That is a useful deployment gate, but it is smaller than the local numbered suite. It does not run every `utils/bin/checks` script, and it does not crawl the live site or prove that an external page is still there. Those are different questions for the monitoring installment that follows this one. It also does not give GitHub Actions my editorial judgment. Pushing starts the workflow; it does not replace my decision to push.

For a small change, I start with the focused checks that answer the likely failure modes, build the site, and inspect the rendered page. Before committing, I look at the diff and the staged files again. If I choose the broader local suite, I treat its repairs and generated output as new changes to review, not as invisible housekeeping. After a push, I want the Pages job to succeed, and I want to know what it actually deployed. The handoff from “the command passed” to “this is the version I meant to publish” is still mine.

## Try the Gate Without Touching This Site

The [Hands-On companion]({{ page.series_companion_url | relative_url }}) gives you a small prepublication runner with invented pages and assets. You can make one gate fail, see what gets skipped, and inspect the fixture without running this repository's mutating checks or contacting a service. It is a teaching lab, not a substitute for the actual site's Ruby plugins, Jekyll build, or Pages workflow.

## Current State

This site has useful, layered defenses: Ruby checks for URL and tag contracts, a substantial local script suite, a Jekyll build, and a narrower Pages deployment job. It also has overlap, warning-only steps, repair steps, and a hook argument that misses the check it intended to skip. I would rather describe those edges plainly than sell the pipeline as a green light that means everything is fine.

The next article looks at the other side of deployment. A successful upload does not tell me whether the live pages, redirects, images, and outside links keep working tomorrow.
