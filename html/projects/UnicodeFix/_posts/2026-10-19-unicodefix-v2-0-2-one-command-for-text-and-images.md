---
permalink_slug: "unicodefix-v2-0-2-one-command-for-text-and-images"
short_link_basis: "/projects/UnicodeFix/_posts/2026-10-19-unicodefix-v2-0-2-one-command-for-text-and-images.md"
short_url: "https://unixwzrd.ai/s/bb7fbf577a/"
layout: post
title: "UnicodeFix v2.0.2: One Command for Text and Images"
date: 2026-10-19
category: UnicodeFix
content_type: update
tags: [unicode, image-metadata, provenance, developer-tools, python, open-source]
excerpt: "UnicodeFix now recognizes image inputs in cleanup-text and routes them through the existing local image backend, while keeping audit, preview, and provenance safeguards intact."
image: /assets/images/projects/UnicodeFix-banner.png
published: true
---

I added `cleanup-image` in UnicodeFix 2.0.1, but there was still an unnecessary little decision at the front door: you had to choose the image command before the tool had even looked at the file. UnicodeFix can recognize the file signature itself, so I fixed that in **v2.0.2**.

`cleanup-text` now routes recognized images through the same local image backend. Text still goes through the text pipeline. One command can take a mixed set of files and report on both.

<!--more-->

## What Changed

An ordinary image cleanup now looks like this:

~~~sh
cleanup-text photo.jpg
~~~

For a supported writable image with ExifTool 12.70 or newer, that writes `photo.clean.jpg` with non-rendering metadata removed. It does not re-encode the pixels or discard ICC profiles, orientation, or color-space tags. The original stays put. If the image has recognized C2PA provenance, metadata cleanup refuses to proceed unless you explicitly request `--strip-provenance`; it will not quietly invalidate a credential and call that success.

The other modes came along for the ride:

~~~sh
cleanup-text --report --metrics --json notes.txt photo.jpg
cleanup-text --dry-run photo.jpg
cleanup-text --strip-provenance photo.jpg
~~~

The first command audits text and image files together without writing. The second previews the image cleanup. The third is an **explicit** choice to remove recognized provenance along with the metadata. `cleanup-image` is still there if you prefer the dedicated command; called without cleanup flags, it remains audit-only.

There are guardrails. Image output must be a separate file, and UnicodeFix refuses to overwrite one unless `--force` is supplied. Text-only switches such as `--unwrap-markdown`, in-place editing, and stdout output are rejected for images with an explanation instead of being silently ignored. Some recognizable image types can be audited but are not supported for writing; the [image guide](https://github.com/unixwzrd/UnicodeFix/blob/main/docs/cleanup-image.md) lists the supported cleanup formats and backend requirements.

This is a small change, but it makes the front end match what the tool already knows how to do. It is still a local, evidence-first cleaner, not a claim that removing metadata removes a pixel watermark or proves anything about who made an image. The [v2.0.2 changelog](https://github.com/unixwzrd/UnicodeFix/blob/main/CHANGELOG.md) has the full set of changes.
