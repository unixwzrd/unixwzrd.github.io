---
short_link_basis: "/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-16-closing-the-publishing-loop-without-pretending-it-is-a-cms.md"
short_url: "https://unixwzrd.ai/s/6d384b45b7/"
layout: post
title: "Closing the Publishing Loop Without Pretending It Is a CMS"
date: 2026-10-16 08:00:00 -0500
categories: [technology]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "Three kinds of writing enter this Jekyll site, but they all need the same human decision before a push and the same public checks afterward. The reader can then respond in a discussion or through a mail-client draft."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: 10
series_order: 100
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_previous_title: "Monitoring a Static Site After Deployment"
series_previous_url: /technology/2026/10/11/monitoring-a-static-site-after-deployment/
series_companion_title: "Hands-On: Keep a One-Page Publication Record"
series_companion_url: /hands-on/2026/10/16/hands-on-keep-a-one-page-publication-record/
series_companion_date: 2026-10-16 08:05:00 -0500
image: /assets/images/blog/jekyll-site-tooling/post-10-publishing-loop-hero.png
---

I used to think the hard part was getting Jekyll to render a page. That was a while ago. Now I need to know where the page belongs, which URL should survive a move, what the build actually emitted, and whether a reader can still reach it after I push. Then, if the reader wants to say something, I need a way for that to happen without building a whole accounts-and-inbox application around a static site.

That is how this series got so large. Each irritating little publishing problem led to a tool, a Liquid include, a YAML field, or another check. The result is a better publishing system for *this* site, but it did not arrive as one grand CMS replacement. I kept fixing the thing that was driving me nuts next.

<!--more-->

## Three Ways In, One Editorial Decision

An ordinary article, a series installment, and a project update do not start in quite the same place here. A standalone post belongs to one of the site's article sections. A series post carries its order, navigation, and companion links in front matter. A project comes from the project data and layout structure, which can place it in the directory and navigation, give it a landing page, and provide a home for its own update posts. The generated starter material is a beginning, not a review or a finished announcement.

That is more than one blog with a drafts folder. YAML data decides which projects are presented, front matter gives posts their publishing identity, and Liquid layouts and includes reuse the presentation across those sections. I can change a project record or a menu setting and let the build assemble the right pages. I still have to inspect what that change did.

The three paths meet at the same question: is this particular page ready for people to read? A template can put it in the right place. It cannot tell me whether the prose sounds like me, whether a diagram explains anything, or whether a project update is accurate.

{% include blog_diagram.html
   src="/assets/images/blog/jekyll-site-tooling/post-10-publishing-loop.svg"
   alt="A standalone article, series installment, and project update converge at editorial review. Local preview and checks inform a human push decision. Pages deployment is followed by public checks, then readers can use a discussion or compose a private email."
   caption="Three content paths, shared checks, and two human decisions. Reader response starts after publication; it is not a deployment step."
   variant="series" %}

The [editable Graphviz source]({{ '/assets/code/jekyll-site-tooling/post-10/publishing-loop.dot' | relative_url }}) is available with the diagram.

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-10/publishing-loop.dot" language="text" title="publishing-loop.dot" %}

## The Local Loop Still Needs an Editor

I preview posts in the local Jekyll site, including work that has a future date or has not been published. The article is in the real post structure so I can see the actual layout, menus, series links, images, source viewers, and footer. That catches mistakes a Markdown editor cannot show. Part 2 went into the wrapper around local Jekyll; the important point here is that preview is a view of the work, not permission to publish it.

For technical pieces I keep the diagram source next to its rendered SVG and PNG, and I expose useful code as a download rather than trapping it in a screenshot. I may also listen to the rendered article through the local TTS path. Hearing a sentence twice because I accidentally wrote it twice is wonderfully annoying and surprisingly effective. None of those tools decides whether the article is good. They give me another way to notice that it is not ready yet.

Then I check the contracts I am about to put in public: tags, section, series order, canonical route, short link, redirects, and any project-specific paths. The pre-commit and site-check tools help, but some checks refresh data or repair files. I look at the changed-file list after they run. I do not treat a green command as a blanket approval of whatever it changed. Part 8 covered those boundaries in detail.

One other trap is the date. A future-dated post can look fine in my local preview and still be absent from the production Pages build. Moving a date forward does not make GitHub rebuild the site on that date, either. The push and resulting Pages run are separate events. I choose when to commit and push after the review, then check the deployment that actually happened.

## The Public Site Gets Its Own Check

Once Pages finishes, I check the served article and the things around it: its image, a source download if there is one, and any important short or old URL. An HTTP 200 from a redirect is not enough if it landed on the wrong page. The sitemap crawler and reliability monitor in Part 9 answer related but different questions, and neither becomes a scheduled safety net merely because its script exists. The public route is evidence about the public route. It is not a verdict on every page in the site.

Short links earn their keep when I share an article on X (Twitter), Bluesky, or another place where a long permalink wastes space. They are generated under my own site, so I control the redirect. If I change a page's naming later, I can preserve the short-link basis and point the old route at the new one. That is a useful kind of control to have when a series changes shape halfway through.

Social copy is still a publishing choice. There are helper scripts in the repository for social posting, but the current Pages workflow does not turn a deployment into an automatic post on every network. I want to read the public page first, write a short introduction that fits the audience, and then decide where to share it.

## Give Readers a Way Back

The site's shared engagement include gives a post a support block and a public discussion area unless I turn those off for a particular page. The discussion uses Giscus, which connects comments to GitHub Discussions. With this site's current pathname mapping, the public path matters to the discussion identity. If I rename a route, I need to think about that conversation as well as the redirect. A redirect can keep an old reader link working; it does not, by itself, promise the new path will find the same discussion.

There is also a private route. The [contact page]({{ '/contact/' | relative_url }}) has a small form that collects the message and opens a prepared email in the visitor's local mail client. The button says “Open Email Draft” because that is exactly what it does. The browser script puts the entered fields, page URL, referrer, and timestamp into the draft, with a direct email link as a fallback. The site does not receive a submission or store a lead when the button is clicked. The visitor still has to have a working mail client and choose to send the message.

I like that boundary. Public discussion can happen in a place readers can see, and a private note can arrive as ordinary mail. Neither requires me to run a comment database or build a login system. These routes can sit quietly for a while; they are there when somebody wants them. The support links are invitations too, not a measurement of whether an article was worth writing.

The [Hands-On companion]({{ page.series_companion_url | relative_url }}) has a one-page publication record you can copy for your own site. It tracks the source, URL promises, review decision, deployment, public checks, and reader-response routes. It is intentionally a small human record. I have enough automation already; I need to know what it proved.

## Current State

This site can take several kinds of content through shared layouts, metadata, local preview, focused checks, a deliberate push, Pages deployment, and public verification. Diagrams, code downloads, short links, listening tools, discussion, support, and a mail-client contact form make the result more useful than a pile of posts. The tools reduce repeated work and catch real mistakes. They do not write the article, approve the push, send the reader's email, or guarantee the public site stays healthy forever.

## Next Work

This closes the ten-part tour, not the maintenance work. I will keep adjusting the tools when a real publishing problem turns up, and I want to package the parts that can be taught or reused without pretending this particular site's assumptions belong in somebody else's repository. The next change will probably start the same way the others did: something will annoy me enough to fix it.
