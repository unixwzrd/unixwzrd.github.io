---
short_link_basis: "/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-11-12-hands-on-build-a-small-prepublication-check-runner.md"
short_url: "https://unixwzrd.ai/s/463aca228b/"
layout: post
title: "Hands-On: Build a Small Prepublication Check Runner"
date: 2026-10-11 11:30:00 -0500
categories: [hands-on]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "Run three small gates against an invented article, break one input at a time, and watch the runner stop without touching a real Jekyll checkout."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: "8A"
series_order: 85
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_companion_of: 8
series_previous_title: "Checks, Repairs, and the Gates Before Deployment"
series_previous_url: /technology/2026/10/11/checks-repairs-and-the-gates-before-deployment/
series_next_title: "Monitoring a Static Site After Deployment"
image: /assets/images/blog/jekyll-site-tooling/post-08-checks-and-gates-hero.png
redirect_from:
  - /hands-on/2026/11/12/hands-on-build-a-small-prepublication-check-runner/
---

The [main article]({{ page.series_previous_url | relative_url }}) describes the real site's checks, including a few that repair files or rebuild output. This lab is much smaller. It creates an invented article and runs three gates against it: required title, local link, and image path. You can see where a failure stops the sequence without fetching project data or running anything against this repository's posts.

The [Python source]({{ '/assets/code/jekyll-site-tooling/post-08a/preflight_lab.py' | relative_url }}) is the file you run. It needs Python 3.9 or newer and no extra packages. It refuses to use an output path that already exists; choose a fresh directory for each scenario.

<!--more-->

## Start with a Clean Fixture

From a checkout of this site, run:

```bash
python3 html/assets/code/jekyll-site-tooling/post-08a/preflight_lab.py --root /tmp/jekyll-preflight-clean --scenario clean
```

If you are reading the published article without the repository, download the source file above as `preflight_lab.py` and run `python3 preflight_lab.py` with the same options. Choose a different unused output path if the example already exists on your machine.

The runner writes `index.md`, `about.md`, and a tiny SVG under the chosen directory. It then reports PASS for front matter, local links, and image paths. The fixture remains there for inspection. There is no Jekyll build in this lab.

## Break One Gate at a Time

Use a new output directory for each run:

```bash
python3 html/assets/code/jekyll-site-tooling/post-08a/preflight_lab.py --root /tmp/jekyll-preflight-title --scenario missing-title
python3 html/assets/code/jekyll-site-tooling/post-08a/preflight_lab.py --root /tmp/jekyll-preflight-link --scenario broken-link
python3 html/assets/code/jekyll-site-tooling/post-08a/preflight_lab.py --root /tmp/jekyll-preflight-image --scenario missing-image
```

Each broken run exits with status 1. The missing-title case stops at the first gate. The broken-link case passes front matter and stops at the second. The missing-image case reaches the third. Open the generated `index.md` files to see exactly what changed. The runner leaves them alone after reporting the failure.

Want to see the shell stop on the first failure too? Run a scenario in an `if` block and inspect its status:

```bash
if python3 html/assets/code/jekyll-site-tooling/post-08a/preflight_lab.py --root /tmp/jekyll-preflight-repeat --scenario broken-link; then
  echo "Ready for the next step"
else
  echo "Stop and inspect the fixture"
fi
```

This is not a drop-in replacement for the site's Ruby short-link checks, Liquid build, HTMLProofer, or GitHub Pages workflow. It shows the smaller idea behind a gate: give each check one clear job, fail visibly, and do not quietly repair the input during an inspection. The real site's checks are more complicated, and some of them deliberately change files; I review those changes before I decide to publish.

The complete source is here if you want to adapt the exercise:

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-08a/preflight_lab.py" language="python" title="preflight_lab.py" %}
