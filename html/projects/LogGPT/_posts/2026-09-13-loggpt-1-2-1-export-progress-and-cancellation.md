---
permalink_slug: "loggpt-1-2-1-export-progress-and-cancellation"
short_link_basis: "/projects/LogGPT/_posts/2026-09-13-loggpt-1-2-1-export-progress-and-cancellation.md"
short_url: "https://unixwzrd.ai/s/b3b9b2f23f/"
layout: post
title: "LogGPT 1.2.1 Makes Large Artifact Exports Easier to Follow and Cancel"
date: 2026-09-13
category: LogGPT
tags: [loggpt-plus, app-store, safari-extension, data-portability, artifacts, macos]
content_type: update
excerpt: "LogGPT 1.2.1 adds artifact counts, visible file-by-file progress, safe cancellation, and clearer feedback while Plus prepares a conversation archive."
image: /assets/images/projects/LogGPT/LogGPT-Plus.png
published: true
---

**LogGPT 1.2.1** is a usability-focused follow-up to the artifact-preservation features introduced in LogGPT 1.2.0. The update makes large LogGPT Plus exports easier to understand while they are running—and gives you a safe way to stop one when it is taking longer than expected.

Version 1.2.1 has been submitted to Apple and is currently in App Store review.

[Get LogGPT from the Mac App Store](https://apps.apple.com/us/app/loggpt/id6743342693?mt=12)

You do not need to wait for the review to finish before getting LogGPT. The current release remains available from the same listing, and the App Store will offer the 1.2.1 update after Apple approves it. Existing owners receive the update at no additional charge, and LogGPT supports Family Sharing.

## Know What the Conversation Contains

When LogGPT Plus examines a conversation, the export choices now show the total number of artifacts and separate counts for generated and uploaded content. That makes the size of the export visible before collection begins and helps explain why a conversation with many files may take longer to package.

![LogGPT Plus export dialog showing 139 total artifacts, including separate generated and uploaded counts](/assets/images/projects/LogGPT/loggpt-plus-artifact-selection.png)

You can still choose generated content, uploaded content, both categories, or a standalone JSON export. Saved preferences can skip this selection dialog, but they no longer hide the progress of the export itself.

## Follow Each File as It Is Collected

After the export starts, LogGPT Plus displays the current phase, the number of artifacts collected, the filename being processed, and a progress bar based on the complete artifact count. ZIP creation also reports progress instead of leaving a long-running download without feedback.

![LogGPT Plus collecting artifact 22 of 139 with the current filename, progress bar, and Cancel button](/assets/images/projects/LogGPT/loggpt-plus-export-progress.png)

This is especially useful for conversations containing many uploaded documents, generated files, images, or other artifacts. You can see that LogGPT is still working, which file it is handling, and how much of the collection remains.

## Cancel Without Leaving a Partial Download

The new Cancel button can stop conversation retrieval, artifact collection, or ZIP creation. LogGPT does not start the browser download until the archive is complete, so cancelling an unfinished export does not leave behind a partial ZIP. Version 1.2.1 also prevents a second export from starting while one is already being prepared.

Partial artifact availability remains a separate case: if an individual artifact cannot be retrieved but the export continues, LogGPT Plus preserves everything it successfully collected and records unavailable or skipped items in `artifact-manifest.json`.

## From Capture to Readable Markdown and HTML

The ZIP produced by LogGPT Plus works directly with [Extract Chat](/projects/extract-chat/). Extract Chat can safely unpack the archive, organize its generated and uploaded artifacts, and create Markdown, HTML, or both with references to the local files in the extracted directory.

That division remains useful: LogGPT captures the authenticated conversation and its associated files in Safari, while Extract Chat processes the resulting archive locally. I am exploring ways to make that handoff easier in the future—possibly through a native application, a droplet-style workflow, or tighter integration—but no particular form has been chosen yet.

LogGPT 1.2.1 is awaiting Apple’s approval. You can [get the current version from the Mac App Store now](https://apps.apple.com/us/app/loggpt/id6743342693?mt=12) and receive the update from the same listing once it is released.
