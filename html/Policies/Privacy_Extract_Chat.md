---
title: "Extract Chat Privacy Policy"
layout: page
permalink: /Policies/Privacy_Extract_Chat/
image: /assets/images/default-og-image.png
excerpt: "How the Extract Chat macOS application handles local conversation archives, settings, diagnostics, and support requests."
published: false
---

Draft for review - not yet published. An effective date will be added before release.

## Your conversations stay under your control

Extract Chat converts conversation JSON and ZIP archives that you select into readable Markdown, HTML, and optional continuity chunks. Conversion runs locally on your Mac using the engine bundled with the app. You do not need an Extract Chat account, a Python installation, or a connection to ChatGPT to convert files you have already downloaded.

The macOS app does not send your conversations, attachments, filenames, or conversion results to us. It has no advertising, analytics, tracking, or automatic diagnostic-upload service. It does not ask for ChatGPT credentials, browser cookies, or access to your browser session.

## Files and saved settings

The app requests access to the files and folders needed for the conversion you choose. It reads the selected inputs and writes results to the location you authorize. Original input archives are not modified. Temporary working files are used during conversion and are removed when the operation finishes or cancellation completes normally. An unexpected crash or forced termination may leave temporary data behind.

The app remembers conversion settings on your Mac. It may also save macOS security-scoped bookmarks for folders and custom CSS files you select, so it can request access to those locations again. These settings and bookmarks are not sent to us.

Converted files remain where you save them until you move or delete them. Choosing an iCloud Drive, Google Drive, Dropbox, or other synchronized folder may cause that provider to upload or synchronize the files under your account and its own privacy policy. That is different from Extract Chat sending your files to us.

## Diagnostics and support

Conversion errors and schema warnings may produce local logs or reports containing filenames, paths, format details, and metadata from the input. Reports are not automatically submitted by the macOS app. Review and redact them before sharing them, especially in a public GitHub issue. The separately installed command-line tool has an explicit issue-submission option; that option is not exposed by the macOS interface.

If you contact us or choose to send a sample, we receive the information you provide and use it to answer your request or investigate the problem. Do not send credentials, session cookies, or unredacted private conversations. We do not sell support correspondence. You can ask us to delete information you supplied by contacting us; material posted publicly on GitHub is also subject to GitHub's controls and retention policies.

## Apple and external links

Apple handles App Store purchases and distribution. Apple may provide developers with sales information, usage reports, or diagnostics according to your Apple settings and Apple's policies. Extract Chat does not operate a separate payment or telemetry service.

Opening a support link or a link in an exported document uses your chosen browser or other application. Those websites and services have their own privacy policies. Exported HTML and custom CSS may contain external references; opening the output can make network requests through the viewer. Local conversion is not a guarantee that every link or resource in the resulting document is offline.

## Changes and contact

We will update this policy if the app's data handling changes. The published policy will show its effective date.

For privacy questions or requests, contact Distributed Thinking Systems LLC through our [contact page](/contact/) or email [info@unixwzrd.ai](mailto:info@unixwzrd.ai).

[Extract Chat](/projects/extract-chat/) · [Terms of Use](/Policies/Terms_Extract_Chat/)

Copyright 2026 Distributed Thinking Systems LLC.

