---
short_url: "https://unixwzrd.ai/s/ac9e64bf66/"
short_link_basis: "/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-11-05-proofreading-a-blog-by-listening-to-it.md"
layout: post
title: "Proofreading a Blog by Listening to It"
date: 2026-11-05 08:00:00 -0600
categories: [technology]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "I can read a draft three times and still miss the sentence that sounds wrong. Listening to the rendered post gives me another way to edit it."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: 7
series_order: 70
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_previous_title: "Diagrams and Source Code That Behave Like Editorial Content"
series_previous_url: /technology/2026/10/29/diagrams-and-source-code-that-behave-like-editorial-content/
series_next_title: "Checks, Repairs, and the Gates Before Deployment"
image: /assets/images/blog/jekyll-site-tooling/post-07-listening-proofread-hero.png
---

I was proofreading a blog post and thought it would be useful if the page could read a paragraph back to me. I already had local text-to-speech, so why not select some text, press Play, and listen? Then I wanted Pause. And Stop. And Restart. Before long I was thinking about saving an MP3 too. I wrote about that tangent in [Scope Creep Has Never Been This Easy]({{ '/s/7037a514e9/' | relative_url }}). The original job was still to finish the article.

The idea was useful because I can read a draft three times and still miss a sentence that sounds wrong. My eyes know what I meant to write, so they glide over a repeated phrase or fill in a missing turn in the argument. When I hear the post, I cannot skip over it quite so easily. A paragraph that looked tidy on the page suddenly takes too long to get to its point. A switch from “I” to “we” stands out. So does a bit of language that might be technically accurate but does not sound like me. I still read the Markdown and the rendered page. Listening gives me another pass, then I go back and edit the source myself.

<!--more-->

## Listen to the Page People Will Read

The input is the rendered Jekyll post, not a raw Markdown file. That matters on this site. A post can contain Liquid includes, a diagram, a source-code disclosure, a series link, and all the other furniture around the article. If I sent the page's entire text to speech, the useful sentence would be buried under navigation, URLs, code, and buttons.

The proofreader starts with the rendered post body. It keeps the title, headings, paragraphs, list items, blockquotes, readable link labels, and the words in inline code. It drops page furniture, figure images and controls, tables, full code blocks, source disclosures, media, and raw link addresses. A caption written as a regular article paragraph can still be read. A link labeled “Graphviz source-build guide” can be spoken as those words; spelling out its web address would not help me hear the sentence. The cleanup also smooths characters that sound awkward in speech, such as underscores and arrows. It is a reading copy of the article, not a substitute for the exact technical text on the page.

The Python command makes that boundary easy to inspect before any voice is involved. With the local review server running and the repository's Python dependencies available, I can ask what it would read:

```bash
python3 utils/bin/article_tts.py http://localhost:4000/technology/2026/11/05/proofreading-a-blog-by-listening-to-it/ --dry-run
```

That prints the extracted prose and the size of each proposed chunk without contacting the speech engine. I use it when a post has a new kind of include or an odd bit of formatting. If the extractor swallowed a paragraph or started reading a code listing, I want to find that before listening. The browser player has its own JavaScript extraction path with the same editorial aim, so a dry run is a check of the command-line path, not a byte-for-byte preview of every browser request.

## Keep the Listening Pass Under My Control

On a development build, the post layout adds a small Listen control at the bottom of the browser. It is not part of the production page. If I select a sentence and press Play, the player reads that selection. If I place the cursor inside the article, it can start there and continue to the end. With no selection or article cursor, Play starts with the whole post. Restart returns to the title; Pause, Play, and Stop let me work through a passage without losing my place.

That small amount of control is useful because editing by ear is rarely one uninterrupted performance. I stop at the awkward sentence, change it, rebuild or refresh the preview, and listen again. Sometimes I need the whole piece to judge its rhythm. Sometimes one paragraph is enough. The player chooses its reading target when I press Play, rather than forcing every check to begin at the top.

The text is split into paragraph-aware chunks before the browser asks for speech. It tries to keep sentences together and only breaks a long piece more aggressively when it has to. The player sends one chunk to a loopback relay, receives a complete WAV response, and plays that buffered audio in the browser while preparing the next chunk. That feels continuous enough for proofreading, but it is not byte-level audio streaming. The relay keeps the configured TTS bridge and voice out of the page JavaScript, accepts the local development origin, and does not write this browser-playback audio to disk.

That relay is only the website end of the path. In my setup, it forwards speech requests to the TTS Bridge managed by LLM-Ops-Kit. The bridge gives the site a stable speech interface and maps my configured voice to a registered reference; my patched MLX-Audio engine does the actual synthesis. I had to patch MLX-Audio to get voice cloning working properly, but Jekyll does not need to know about models or reference files. I went into the bridge, engine, and reference checks in [Voice Cloning Across Hosts: Making TTS Operational]({{ '/s/cff8a7634b/' | relative_url }}). For this editing pass, what matters is that the audio comes back to the page so I can hear the sentence and fix it.

{% include blog_diagram.html
   src="/assets/images/blog/jekyll-site-tooling/post-07-listening-loop.svg"
   alt="The rendered Jekyll article is reduced to readable prose, divided into speech chunks, passed through a loopback relay to a configured TTS bridge, and played in the browser. The author revises the source and previews it again."
   caption="The listening loop starts with the rendered article and ends with another edit to the source."
   variant="series" %}

The editable Graphviz source is available below if you want to inspect the exact figure input. The SVG above is the reviewed output; a PNG companion is retained with it.

{% include source_code.html source="/assets/code/jekyll-site-tooling/post-07/listening-loop.dot" language="text" title="listening-loop.dot" %}

## Browser Details That Actually Matter

Safari needed some care here. Browsers can refuse audio that starts only after an asynchronous speech request, because the user's button gesture is already over by then. The player primes audio during that gesture and uses a native audio element for Safari. Other supported browsers use Web Audio buffers. I am interested in the editing experience, but if the first Play click silently fails, the editing tool is not much use.

There is one operational step I have to remember: the browser relay is a separate process. With `TTS_BRIDGE_URL` and `TTS_BRIDGE_VOICE` set in my local environment, I start the helper in another terminal and leave it running while I edit:

```bash
utils/bin/article-tts --browser-server
```

Jekyll serves the page; that helper listens on local port 11441 and passes the browser's speech requests to the configured bridge. The Jekyll startup script does not start or stop it. If the relay is not running, the player says the TTS helper is unavailable instead of pretending the article is playing. I do not need to put a private endpoint, voice alias, or model path in the published post to describe that boundary.

Listening is especially good at catching the things a syntax or link check cannot judge. I hear when two paragraphs make the same point. I hear when a long sentence buries the useful part. I hear when the first-person voice drifts into a generic explanation. Then I decide what to cut or rewrite. No test can make that editorial call for me.

## Proofreading Audio Is Not Published Narration

The browser listening pass is temporary. Its audio is there to help me edit this version of the page. Readers do not get a recording just because I pressed Play while proofreading, and the development player is not injected into production builds.

There is a separate workflow for a post I want to publish with an MP3. That workflow checks whether the narration matches the cleaned article and its public narration profile, generates a retained file when needed, and leaves the post's `audio` front matter for an explicit editorial decision. A changed private voice or model needs an intentional profile change; the public manifest cannot discover that on its own. I will give the retained-file and freshness details their own companion rather than turn this listening story into an audio-release manual.

## Current State

I can inspect the reading copy without speech, or listen to a selected passage, the text from my cursor, or the whole rendered post in the local browser. The page furniture stays out of that pass, and the audio does not become a public artifact by accident. When I hear a problem, I change the article and listen again. That is the useful loop.

## Next Work

The next main article moves from editorial review to the checks before a commit and deployment. A sentence can sound right and still have a broken link, bad metadata, or a route that does not build. Part 8 follows the checks we actually run and the places where a human still has to decide whether the site is ready.
