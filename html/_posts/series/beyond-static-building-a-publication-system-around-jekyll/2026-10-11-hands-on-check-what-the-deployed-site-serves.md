---
short_link_basis: "/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-11-hands-on-check-what-the-deployed-site-serves.md"
short_url: "https://unixwzrd.ai/s/5181a6f713/"
layout: post
title: "Hands-On: Check What the Deployed Site Serves"
date: 2026-10-11 15:50:00 -0500
categories: [hands-on]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "Serve an invented miniature site on loopback and see the difference between a missing asset, a successful HTTP response, and a redirect to the right page."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: "9A"
series_order: 95
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_companion_of: 9
series_previous_title: "Monitoring a Static Site After Deployment"
series_previous_url: /technology/2026/10/11/monitoring-a-static-site-after-deployment/
series_next_title: "Closing the Publishing Loop Without Pretending It Is a CMS"
image: /assets/images/blog/jekyll-site-tooling/post-09-after-deployment-hero.png
---

The [main article]({{ page.series_previous_url | relative_url }}) separates a successful Pages build from what a reader receives over HTTP. This exercise makes that gap small enough to inspect. One Python file starts an invented site on loopback, requests its pages, and reports both the final status and the destination of an old URL. It never calls the real site's monitoring tools or public host.

Download [post_deploy_lab.py]({{ '/assets/code/jekyll-site-tooling/post-09a/post_deploy_lab.py' | relative_url }}). It needs Python 3.9 or newer and no extra packages. From a checkout, run the copy under `html/assets/code`; if you downloaded the file alone, use `python3 post_deploy_lab.py` instead.

<!--more-->

## See the Healthy Case

```bash
python3 html/assets/code/jekyll-site-tooling/post-09a/post_deploy_lab.py --scenario healthy
```

The lab serves a tiny home page, an article, its image, and an old article URL that redirects to the article. It checks the page and image responses, then follows the redirect and compares the final path with the intended article path. All checks pass, and the temporary server closes before the command exits.

## Break the Asset

```bash
python3 html/assets/code/jekyll-site-tooling/post-09a/post_deploy_lab.py --scenario missing-image
```

The article still returns 200, but its image returns 404. The process exits 1. This is the kind of gap a build can miss if the deployed asset path is wrong or the uploaded artifact is incomplete.

## Make a Redirect That Looks Healthy

```bash
python3 html/assets/code/jekyll-site-tooling/post-09a/post_deploy_lab.py --scenario wrong-redirect
```

This time the old URL redirects to the home page. A client following redirects receives 200, which looks fine if status is the only assertion. The lab also checks the final path and exits 1 because `/` is not `/article/`. That is why I keep the short-link and generated-redirect checks alongside any public HTTP probe. The site's sitemap crawler follows redirects, but it does not currently assert the final destination.

Try changing the expected destination in the source and running the case again. You can see exactly which contract you have weakened. The lab is intentionally small; it is not a replacement for `site_crawl_check.py`, the repository's Ruby redirect verifiers, or a full browser review.

The complete source is here to inspect or adapt:

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-09a/post_deploy_lab.py" language="python" title="post_deploy_lab.py" %}
