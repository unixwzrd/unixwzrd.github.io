---
short_link_basis: "/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-11-monitoring-a-static-site-after-deployment.md"
short_url: "https://unixwzrd.ai/s/ffb5439ba2/"
layout: post
title: "Monitoring a Static Site After Deployment"
date: 2026-10-11 15:45:00 -0500
categories: [technology]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "The Pages job can finish cleanly while a public route, image, or redirect still needs attention. Here is what my served-site crawler and monitoring tools actually check."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: 9
series_order: 90
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_previous_title: "Checks, Repairs, and the Gates Before Deployment"
series_previous_url: /technology/2026/10/11/checks-repairs-and-the-gates-before-deployment/
series_companion_title: "Hands-On: Check What the Deployed Site Serves"
series_companion_url: /hands-on/2026/10/11/hands-on-check-what-the-deployed-site-serves/
series_companion_date: 2026-10-11 15:50:00 -0500
series_next_title: "Closing the Publishing Loop Without Pretending It Is a CMS"
series_next_url: /technology/2026/10/16/closing-the-publishing-loop-without-pretending-it-is-a-cms/
series_next_date: 2026-10-16 08:00:00 -0500
image: /assets/images/blog/jekyll-site-tooling/post-09-after-deployment-hero.png
---

The [last article]({{ page.series_previous_url | relative_url }}) stopped at the deployment gate. On October 11, the Pages workflow for the latest series push [completed successfully](https://github.com/unixwzrd/unixwzrd.github.io/actions/runs/38173106123), and the public Part 8 page returned HTTP 200 when I checked it. Good. That tells me the build and deployment finished and that one page answered one request. It does not tell me whether every old short link still reaches the right article, whether an image is missing, or whether an outside source I linked last month has disappeared.

That is the uncomfortable bit about a static site. There may be no application process to keep alive, but the published result still has moving parts: hosting, DNS, redirects, linked assets, and other people's websites. Once the page leaves my build directory, I need to look at what a reader actually receives.

<!--more-->

## Ask the Served Site, Not Just the Source Tree

The most direct utility here is `utils/bin/site_crawl_check.py`. It fetches the site's `sitemap.xml`, checks each same-host page listed there, then follows the same-host links and images it finds in those pages. It reports a failed fetch with the source page that exposed it. The script takes an explicit base URL, so I can point it at the public site when I choose to run a live check:

```bash
python3 utils/bin/site_crawl_check.py --base-url https://unixwzrd.ai
```

That is a real HTTP check, not another reading of Markdown. If an image path has the wrong case, or a link points to a route Pages did not emit, the response is the evidence. It also has a sensible boundary: the crawler stays on the supplied host. It does not audit third-party pages or images, and it does not recursively parse every page reached through a link unless that page is in the sitemap. A clean report means the requests it made succeeded, not that every possible route on the site was exercised.

Redirects need an extra question. The crawler follows them and accepts the final response if it is below HTTP 400. That catches a redirect ending in a 404. It does not verify *where* a successful redirect lands. An old article URL that quietly ends up on the home page can return 200 and still be wrong. I keep the source and generated redirect checks from Part 8 for the URL contract, and I spot-check important public redirects after deployment. Status and destination are different assertions.

{% include blog_diagram.html
   src="/assets/images/blog/jekyll-site-tooling/post-09-observation-boundaries.svg"
   alt="A deployed site is observed through a served-site sitemap crawler and a separate source-derived reliability monitor. Both produce evidence for a human investigation; neither is shown as an automatic Pages gate."
   caption="The build and the public site answer different questions. Monitoring only happens when something invokes it."
   variant="series" %}

The editable [Graphviz source]({{ '/assets/code/jekyll-site-tooling/post-09/observation-boundaries.dot' | relative_url }}) is available with the diagram.

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-09/observation-boundaries.dot" language="text" title="observation-boundaries.dot" %}

## The Larger Monitor Has a Different View

The repository also has `utils/bin/site_reliability_monitor.py`. It starts with site availability, checks a list of critical pages, probes images on those pages, and checks external links extracted from Markdown source. It can keep link metrics in its local configuration and send email through configured SMTP settings in post-commit or periodic modes. The `site` mode skips external links for a quicker pass. These are useful pieces, but they are not the same thing as crawling the rendered site.

Its critical-page list combines configured paths with paths it derives from the checkout. The discovery covers top-level pages and project posts, including their legacy redirects. It does not discover the nested series posts as a complete set. It can also encounter source for a page that has not been published yet. The two current unit tests exercise project-route and redirect discovery; they do not prove a successful remote sweep or an alert arriving in an inbox. Even constructing the monitor can save an updated local configuration, and the external-link pass writes metrics. I treat a run as an operational action, not a read-only audit.

The names in that directory can overpromise if I read them too quickly. The monitor's `check_links` setting controls its external Markdown-link check. It does not turn `run_health_checks` into a rendered internal-link crawl. The separate sitemap crawler does that narrower served-site job. There is also a page-management helper whose missing-page and removal commands call methods the monitor class does not currently provide. I am not going to tell readers they have an automatic missing-page cleanup system when that path cannot run as advertised.

## A Script Is Not a Schedule

There are shell wrappers for periodic checks and post-commit checks, plus a script that can install crontab entries. Those are ways to invoke monitoring. The Pages workflow in this repository does not call either monitor or the crawler, and it has no scheduled health-check job. The existence of `periodic_monitor.sh` tells me what would run *if* a schedule called it; it does not tell me that a schedule is active, or that mail delivery is configured and working.

The distinction is especially sharp in post-commit mode. Some of the older guide text says it waits for deployment. The current method calls the health checks immediately. A local commit is not the moment GitHub Pages finishes publishing, and the shell wrapper does not wait for that workflow either. If I want to verify a release, I first wait for the Pages deployment result, then check the public routes and their destinations. Calling the monitor immediately after a commit could inspect the previous deployment and label it with the new commit hash.

I keep logs and notifications in the same category: evidence only if the job actually ran and the message actually arrived. The monitoring code has file logging and SMTP paths, but I cannot infer either a reliable schedule or successful notification from configuration alone. A failed outside link also needs judgment. It might be a removed page, a rate limit, a temporary outage, or a site that blocks automated requests. I do not rewrite an article because one probe got an unhelpful response.

## Try the Public-Side Question Locally

The [Hands-On companion]({{ page.series_companion_url | relative_url }}) serves invented pages on loopback and tests three cases: healthy output, a missing image, and an old URL that redirects to the wrong page. It uses only Python's standard library. The third case is deliberate: a status-only check sees HTTP 200, while a destination check sees the mistake. Nothing in the exercise touches this site's monitor configuration, email settings, or public host.

## Current State

I have two useful but separate tools: a served-site sitemap crawler for public pages and their same-host links and images, and a source-aware monitor for selected pages, images, and Markdown external links. The repository also has invocation and scheduling scripts. They do not become an active safety net merely by existing in `utils/bin`, and neither tool is part of the current Pages deployment job. The limits matter because a clean build, a clean crawl, and a correct redirect are three different claims.

## Next Work

The final installment will put these checks back into the full publishing loop: deciding what to write, previewing and proofreading it, reviewing what the tools changed, choosing when to push, and checking what readers can reach afterward. I want that loop to be dependable without pretending the site has become a CMS that makes editorial decisions for me.
