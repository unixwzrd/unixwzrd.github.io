---
short_link_basis: "/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-16-hands-on-keep-a-one-page-publication-record.md"
short_url: "https://unixwzrd.ai/s/7ce22fa4d1/"
layout: post
title: "Hands-On: Keep a One-Page Publication Record"
date: 2026-10-16 08:05:00 -0500
categories: [hands-on]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "Copy a compact publication record and follow an invented series post from local review to the public page and reader-response routes."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: "10A"
series_order: 105
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_companion_of: 10
series_previous_title: "Closing the Publishing Loop Without Pretending It Is a CMS"
series_previous_url: /technology/2026/10/16/closing-the-publishing-loop-without-pretending-it-is-a-cms/
image: /assets/images/blog/jekyll-site-tooling/post-10-publishing-loop-hero.png
---

The [main article]({{ page.series_previous_url | relative_url }}) ends with a human decision: when is a page ready to push? I use tools to answer pieces of that question, but the evidence can be scattered across a preview, a diff, a Pages run, and a public URL. This exercise puts the important bits on one page.

Download the [publication record template]({{ '/assets/code/jekyll-site-tooling/post-10a/publication-record-template.md' | relative_url }}) and make a copy for an article on your own site. It is Markdown with placeholders. It does not run this repository's hooks, rebuild a site, send an email, or publish anything.

<!--more-->

## Start With an Invented Post

Imagine you are adding the third article in a series about a small weather station. Its source is a Markdown file under your series posts, and its intended public route is a dated article URL. Put those two paths in the record first. Then record the series order, the previous article's URL, and any stable short link or old route you have promised readers.

This is where I often catch an identity mistake. A title is editorial. A source filename is a repository detail. A canonical URL is a public promise. If one changes, write down which of the others should stay put. On this site, short links are under our own domain and can keep pointing to the right destination when naming changes.

## Record What You Actually Looked At

Open the local article and check the page rather than just its Markdown: heading, series navigation, diagram, alt text, code download, and contact/footer links. If the article uses a future date, note that the local preview includes it but a normal production build may not. Listen to the rendered prose if your site has a suitable TTS path; mark it as an editorial review, not a technical gate.

Now write down the checks you ran and whether any tool changed source files. If it did, inspect those files before you mark the review complete. Leave the publish decision blank until a person has read the final page. A checked box that means “I ran a script” is not the same as a checked box that means “I approve these changes.”

## Cross the Deployment Boundary

After a deliberate commit and push, add the Pages run or equivalent deployment reference. Wait for that job to finish, then request the public route. Check an important image or download and follow the short or legacy URL all the way to its *destination*. A redirect ending at the home page can look healthy by status alone.

Finally, note the reader-response routes. On this site, the public option is a Giscus discussion, and the private option is the contact page's mail-client draft. You can inspect that those links are present without creating a test discussion or sending a test message. The publication record should say what you checked, not imply that someone has commented or emailed you.

The template is deliberately plain. Replace its example prompts with your own paths and checks, or delete fields that do not apply. If a failure turns up later, this page gives you a place to start without pretending that every check ran automatically.

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-10a/publication-record-template.md" language="markdown" title="publication-record-template.md" %}

## Current State

You have a reusable record that keeps source identity, editorial approval, deployment evidence, public checks, and response paths together. Filling it out is a human exercise; no checkbox changes the website.

## Next Work

Use one copy for a real post, and remove any field that never helps you diagnose a publishing mistake. Keep the record small enough that you will actually use it.
