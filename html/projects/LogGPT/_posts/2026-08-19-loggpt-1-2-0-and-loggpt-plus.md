---
permalink_slug: "loggpt-1-2-0-and-loggpt-plus"
legacy_project_permalink: "/projects/LogGPT/2026/08/19/loggpt-1-2-0-and-loggpt-plus-preserve-conversations-and-artifacts/"
short_link_basis: "/projects/LogGPT/_posts/2026-08-19-loggpt-1-2-0-and-loggpt-plus.md"
short_url: "https://unixwzrd.ai/s/39e7b3ae47/"
layout: post
title: "LogGPT 1.2.0 and LogGPT Plus: Preserve Conversations and Artifacts"
date: 2026-08-19
category: LogGPT
tags: [loggpt-plus, app-store, safari-extension, privacy, chatgpt, data-portability, artifacts, macos]
content_type: release
excerpt: "LogGPT 1.2.0 introduces LogGPT Plus, a permanent upgrade that can preserve a ChatGPT conversation and its generated or uploaded artifacts together in one ZIP archive."
image: /assets/images/projects/LogGPT/LogGPT-Plus.png
published: true
---

I am pleased to announce **LogGPT 1.2.0** and the new **LogGPT Plus** upgrade for Safari. LogGPT still provides the straightforward, privacy-focused JSON export it was built for, while Plus can now preserve the files associated with a ChatGPT conversation as part of the same local archive.

[Get or update LogGPT on the Mac App Store](https://apps.apple.com/us/app/loggpt/id6743342693?mt=12)

Existing users can update LogGPT and use the in app purchase to add LogGPT Plus to their account.

## LogGPT Remains Simple

The standard LogGPT workflow has not changed: click the export button in a ChatGPT conversation and LogGPT downloads the conversation as structured JSON. Basic export remains JSON-only and does not require the Plus upgrade.

Everything continues to run through the Safari extension. LogGPT has no user accounts, analytics, telemetry, or purchase server, and it does not send your conversations to an external service.

## What LogGPT Plus Adds

LogGPT Plus is a permanent in-app purchase available from the existing LogGPT App Store listing. When exporting a conversation, Plus lets you choose which related artifacts to preserve:

- **Generated Content** created during the conversation
- **Uploaded Content** that you supplied to the conversation
- **Both** generated and uploaded content

The result is one ZIP archive containing the conversation JSON, the selected artifacts, and an `artifact-manifest.json` file that describes what was found and downloaded.

The archive keeps generated, uploaded, and derived files organized separately. The manifest records useful preservation details such as file identifiers, detected and declared media types, sizes, hashes, source information, and download status. Images, vector graphics, audio, video, documents, spreadsheets, archives, and other binary files can be retained without converting them to another format.

## Useful Even When One File Fails

An artifact failure does not discard the rest of the export. LogGPT Plus saves the conversation and any files it successfully downloaded, then records failures or skipped items in the manifest. That makes the archive useful while still leaving an auditable account of anything that could not be preserved.

If both artifact categories are turned off, Plus downloads JSON only, just like the standard workflow.

## A Portable Starting Point

The ZIP is intended as a durable capture package rather than a rendered document. [Extract Chat](/projects/extract-chat/) can process these exports offline and produce Markdown or HTML that refers to the preserved local files. This separation keeps capture focused, makes the original data easier to retain, and lets you choose how to render or analyze it later.

LogGPT 1.2.0 is available from the [same Mac App Store listing](https://apps.apple.com/us/app/loggpt/id6743342693?mt=12). Existing users can update LogGPT there, and the source remains available in the [LogGPT GitHub repository](https://github.com/unixwzrd/LogGPT).
