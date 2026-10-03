---
permalink_slug: "loggpt-1-3-2-safari-conversation-switching-fix"
short_link_basis: "/projects/LogGPT/_posts/2026-10-03-loggpt-1-3-2-safari-conversation-switching-fix.md"
short_url: "https://unixwzrd.ai/s/c6c0f02119/"
layout: post
title: "LogGPT 1.3.2 Fixes a Safari Freeze When Switching Conversations"
date: 2026-10-03
category: LogGPT
tags: [chatgpt, safari-extension, app-store, macos]
content_type: update
excerpt: "LogGPT 1.3.2 fixes a button-reconciliation race that could freeze Safari when switching ChatGPT conversations."
image: /assets/images/projects/LogGPT/LogGPT-Plus.png
published: true
---

ChatGPT changed its conversation title bar, so [LogGPT 1.3.1](/projects/LogGPT/2026/10/01/loggpt-1-3-1-download-button-compatibility/) had to adjust where it placed the download button. That fix brought the button back, but it also exposed a race in LogGPT's button handling that could freeze Safari when you switched conversations. **LogGPT 1.3.2 fixes that.**

The extension now ignores hidden conversation headers and won't treat its own download button as the place to insert the button again. It also groups page changes so it only reconciles the button once per animation frame, with a bounded check for conversation changes that don't trigger a visible page mutation. The result is that the download button should stay available as you move between conversations, without needing to reload the page or getting Safari stuck in the process.

This is a stability update; the LogGPT and LogGPT Plus export workflows have not changed. Version 1.3.2 has been submitted to Apple. If you already own LogGPT, the App Store will provide the update at no additional charge when Apple makes it available.

[Get LogGPT from the Mac App Store](https://apps.apple.com/us/app/loggpt/id6743342693?mt=12).
