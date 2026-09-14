---
layout: project
title: "LogGPT and LogGPT Plus for Safari"
appstore_link: https://apps.apple.com/us/app/loggpt/id6743342693?mt=12
category: LogGPT
permalink: /projects/LogGPT/
image: /assets/images/projects/LogGPT/LogGPT-Plus.png
excerpt: "LogGPT 1.3.0 exports ChatGPT and ChatGPT Work conversations as structured JSON, while LogGPT Plus preserves generated and uploaded artifacts in a portable ZIP."
---

## Local Archives for ChatGPT Conversations and Artifacts

ChatGPT conversations often contain research, troubleshooting history, writing drafts, decisions, and project context that are easy to lose inside a hosted chat interface. **LogGPT for Safari** exports complete ChatGPT conversations as structured JSON so you can keep your own archive and decide what to do with it next.

The permanent **LogGPT Plus** upgrade adds artifact preservation. It can collect generated content, uploaded content, or both and package those files with the conversation JSON and an artifact manifest in one ZIP archive. The extension runs in Safari on macOS and is available through Apple's App Store.

## Why It Matters

AI chat history becomes more useful when it is portable. Exported conversations can be reviewed, backed up, searched, converted, chunked, or reused in local-first workflows instead of remaining trapped in a browser tab.

LogGPT fits the broader Distributed Thinking Systems stack as the capture layer for ChatGPT history and associated files. [Extract Chat](/projects/extract-chat/) can process the exports offline into readable Markdown or HTML with local artifact references, and tools such as [VenvUtil](/projects/venvutil/) can help process larger archives for local AI and data workflows.

## Key Features

- **Capture complete ChatGPT sessions** as structured JSON with a single click
- **Support ChatGPT Work artifacts**, including generated images, workspace-linked files, and uploaded attachments
- **Choose generated content, uploaded content, or both** with LogGPT Plus
- **Download one portable ZIP archive** containing the JSON, selected artifacts, and an artifact manifest
- **See artifact counts and file-by-file progress** while LogGPT Plus prepares large archives
- **Cancel an unfinished export safely** without producing a partial browser download
- **Keep partial archives useful** when an individual artifact cannot be downloaded, with the failure recorded in the manifest
- **No external servers, no tracking, and full user control - runs entirely in your browser**
- **Works with local processing tools** for review, conversion, chunking, and archival workflows
- **Supports context transfer** by making it easier to split exported files and reuse selected context in a new session

## Development & Availability

LogGPT is available for **Safari on macOS** through its [App Store listing](https://apps.apple.com/us/app/loggpt/id6743342693?mt=12). Version 1.2.1 is the current public release. Version 1.3.0 is now in Apple’s review process and adds ChatGPT Work artifact support while retaining the export progress and cancellation introduced in 1.2.1. Anyone getting LogGPT now will receive version 1.3.0 through the same App Store listing when it is released. Existing owners receive the update at no additional charge, and LogGPT supports Family Sharing. Basic JSON export remains available without the upgrade; LogGPT Plus is a permanent in-app purchase. The project is also available on [GitHub](https://github.com/unixwzrd/LogGPT).

For details on **installation, usage, and technical documentation**, refer to the project's **[README](https://github.com/unixwzrd/LogGPT)**.

If you need help building local archive, conversion, or AI analysis workflows around exported chat history, [get in touch](/contact/).
