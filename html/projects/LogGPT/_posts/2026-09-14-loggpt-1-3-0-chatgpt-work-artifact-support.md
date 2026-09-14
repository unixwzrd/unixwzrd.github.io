---
permalink_slug: "loggpt-1-3-0-chatgpt-work-artifact-support"
short_link_basis: "/projects/LogGPT/_posts/2026-09-14-loggpt-1-3-0-chatgpt-work-artifact-support.md"
short_url: "https://unixwzrd.ai/s/fc2100d255/"
layout: post
title: "LogGPT 1.3.0 Adds Artifact Support for ChatGPT Work"
date: 2026-09-14
category: LogGPT
tags: [loggpt-plus, chatgpt, app-store, safari-extension, data-portability, artifacts]
content_type: update
excerpt: "LogGPT 1.3.0 adds discovery and preservation of generated images, workspace-linked files, and uploaded attachments from ChatGPT Work conversations."
image: /assets/images/projects/LogGPT/LogGPT-Plus.png
published: true
---

**LogGPT 1.3.0** is the next update to LogGPT and adds artifact support for **ChatGPT Work** conversations. It follows yesterday’s 1.2.1 usability release, making this one of the quickest LogGPT version turnarounds so far.

[Get LogGPT from the Mac App Store](https://apps.apple.com/us/app/loggpt/id6743342693?mt=12)

Version 1.2.1 added visible artifact counts, file-by-file progress, ZIP creation status, and safe cancellation. All of those improvements remain in 1.3.0. The version bump reflects a more substantial compatibility change underneath them: ChatGPT Work represents generated and uploaded files differently from ordinary ChatGPT conversations.

## Supporting a Different Conversation Structure

LogGPT already understood the artifact references used in standard ChatGPT conversations. ChatGPT Work introduced additional structures that required new discovery and download handling, including:

- Generated images represented as image asset pointers
- Generated files linked from ChatGPT Work sandbox storage
- Uploaded attachments recorded through Work conversation metadata

LogGPT 1.3.0 recognizes these forms, classifies the artifacts as generated or uploaded, and includes the available files in the same portable LogGPT Plus archive.

This is why the release moved from 1.2.1 to 1.3.0 rather than becoming another patch update. The visible workflow remains familiar, but the conversation and artifact structures LogGPT can interpret have expanded substantially.

## The Archive Format Remains Familiar

ChatGPT Work compatibility changes how LogGPT discovers source artifacts; it does not require a different workflow after export. LogGPT Plus still produces one ZIP containing the conversation JSON, the selected generated or uploaded files, and `artifact-manifest.json`.

The progress interface added in 1.2.1 also applies to ChatGPT Work exports. Before collection begins, LogGPT Plus reports the available artifact counts. During a large export, it shows the current filename and overall progress, and you can cancel without producing a partial browser download.

## Still Works with Extract Chat

The resulting ZIP remains compatible with [Extract Chat](/projects/extract-chat/). Extract Chat can unpack the archive locally and create Markdown, HTML, or both, with references to the generated and uploaded files preserved alongside the conversation.

That keeps the workflow straightforward: LogGPT captures the authenticated conversation and artifacts from Safari, and Extract Chat turns the portable archive into a readable local collection.

## Availability

LogGPT 1.3.0 is now in Apple’s review process. Version 1.2.1 remains the current public release until Apple releases the update. If you get LogGPT now, the App Store will provide version 1.3.0 when it becomes available. Existing owners receive the update at no additional charge, and LogGPT supports Family Sharing.

Your chats remain under your control: LogGPT has no accounts, analytics, telemetry, or developer-operated processing service.
