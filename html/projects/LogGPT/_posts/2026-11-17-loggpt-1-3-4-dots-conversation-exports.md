---
layout: post
title: "LogGPT 1.3.4 Adds Dots Exports and Clearer Download Filenames"
date: 2026-11-17
category: LogGPT
content_type: update
permalink_slug: "loggpt-1-3-4-dots-conversation-exports"
short_link_basis: "/projects/LogGPT/_posts/2026-11-17-loggpt-1-3-4-dots-conversation-exports.md"
short_url: "https://unixwzrd.ai/s/13f5ab2484/"
tags: [chatgpt, safari-extension, app-store, macos, data-portability]
image: /assets/images/projects/LogGPT/LogGPT-Plus.png
excerpt: "LogGPT 1.3.4 adds Dots main-timeline exports, available direct attachments with Plus, and source-labeled filenames. Available on the Mac App Store."
published: true
update_notice_title: "Version 1.3.5 update - November 18, 2026"
update_notice: "LogGPT 1.3.5 restores the Dots download control after another header change and adds downloads from the Safari toolbar popup. Plus bundles now use the ZIP-compatible `.lgpt` extension. [Read the 1.3.5 announcement](/projects/LogGPT/2026/11/18/loggpt-1-3-5-toolbar-downloads-and-lgpt-archives/). The original 1.3.4 announcement is preserved below."
---

**LogGPT 1.3.4 is available on the Mac App Store.** We've added Dots conversation exports alongside the existing ChatGPT and ChatGPT Work support, giving you another way to keep a local copy of your work. Downloads are easier to identify, too, with source labels added to filenames when LogGPT recognizes where the conversation came from. All existing LogGPT owners, whether Basic or Plus, receive this app update at no additional charge.

<!--more-->

[Get LogGPT on the Mac App Store](https://apps.apple.com/us/app/loggpt/id6743342693?mt=12).

## Export the Dots timeline and its attachments

Version 1.3.4 adds a LogGPT download button beside the Dots conversation actions menu. It can export the main conversation timeline as JSON, or use LogGPT Plus to package that timeline and its directly attached available files together in a ZIP. For longer histories, LogGPT shows message collection progress and lets you cancel while retrieval is underway.

**Dots exports include the main timeline and directly attached available files only. Linked task histories and nested reply histories are not included.** That distinction matters when deciding what an export preserves: a file attached to the timeline and a separate history linked from it are not the same thing.

## Tell downloads apart at a glance

When LogGPT recognizes the conversation source, exported filenames carry one of these postfixes:

| Conversation source | Filename postfix |
| --- | --- |
| ChatGPT | `-chat` |
| ChatGPT Work | `-work` |
| Dots | `-dot` |
| Source not recognized | No source postfix |

If LogGPT cannot determine the source, the filename keeps the familiar format: the chat name with its start and end dates. No source postfix is added.

Those labels make a mixed download folder easier to follow without opening each archive to work out where it came from. The update also retains the checkbox visibility fixes introduced in [LogGPT 1.3.3](/projects/LogGPT/2026/11/16/loggpt-1-3-3-checkbox-visibility-fix/), covering the Plus export dialog and Basic upgrade notice.

## A free app update, with more to archive through Plus

LogGPT Basic gives you a structured JSON copy of the conversation, including the new Dots main-timeline export. That's useful for keeping your own record, processing the conversation locally, or carrying project context into another workflow rather than starting from scratch.

**LogGPT Plus keeps the supporting files with the conversation in one portable ZIP.** For ChatGPT and ChatGPT Work, you can choose available generated content, uploaded content, or both. For Dots, Plus includes directly attached available files from the main timeline. If your work involves documents, images, code, or research material, saving the discussion is only part of the job: you also want the files it refers to when you return to that project.

We built Plus for that next step, so you can keep the conversation and its available files together rather than download and organize them separately. It's an optional, one-time in-app purchase, not a subscription. Basic owners can upgrade from within LogGPT whenever they want artifact archiving; existing Plus owners are already covered and do not need to purchase it again for Dots support.

[Get LogGPT on the Mac App Store](https://apps.apple.com/us/app/loggpt/id6743342693?mt=12), then add Plus from within the app if you'd like to keep the files alongside your conversations.


