---
layout: post
title: "LogGPT: NEW 1.0.6 - Fixed issue with loading"
date: 2025-06-21
category: LogGPT
tags: [LogGPT, ChatGPT export, privacy, Safari extension, Apple App Store, AI tools, JSON, macOS]
excerpt: "Just as Apple approved the second release of LogGPT, OpenAI quietly changed the Document Object Model (DOM) on ChatGPT's site-breaking the download button injection."
image: /projects/LogGPT/images/Icon-512-download.png
published: true
---

Just as Apple approved the second release of LogGPT, OpenAI quietly changed the Document Object Model (DOM) on ChatGPT's site-breaking the download button injection.

[Get LogGPT on the Mac App Store](https://apps.apple.com/us/app/loggpt/id6743342693?mt=12)

### What's New
With this update, the download icon now shows up in the right place, even after UI refreshes or dynamic changes. For those following the saga: Apple's review team sent it back once (mentioning OpenAI and ChatGPT in the description = forbidden fruit), and then took their time reviewing it during WWDC. Now it's resubmitted and I'm waiting on the green light-shouldn't be long.

This release is mostly about fixing the DOM change, but I also took the opportunity to clean up the code:
- Refactored button creation and event handler logic (better performance, less fragility)
- Download button handler moved to its own function, avoiding redundant event bindings
- Injection is now focused on pure DOM manipulation-no more accidental duplication
- Button stays persistent, even as ChatGPT's UI dances around

As for the Safari extension lifecycle: unfortunately, the Safari API doesn't allow deactivation events to cleanly unload JavaScript from the extension. It's not ideal, but at least now, reactivating the extension doesn't spin up multiple instances, and you can always reload the window for a clean slate.

You can grab the new version from the [LogGPT GitHub repo](https://github.com/unixwzrd/LogGPT) or (soon) directly from the App Store. If you already have it, an update will be pushed out once Apple gives the final approval.

### Bonus
LogGPT pairs nicely with my command-line Python Virtual Environment Utilities for AI/ML workflows. With [`venvutil`](https://github.com/unixwzrd/venvutil), you can extract your ChatGPT logs as Markdown, move between contexts, or migrate sessions when you hit limits or want to swap models. The tool has an easy installer (`./setup.sh`) - just clone, cd, and run.

Here's the prompt I use to reconstitute ChatGPT context after hitting session limits (meta, I know):

{% include wrap_codeblock.html %}
```markdown
# Context Move Instructions

Our conversation exceeded the length restrictions. I am uploading our previous conversation so we can continue with the same context. Please **review and internally reconstruct the discussion** but **do not summarize back to me** unless requested. Read teh files carefully as I will reference items from them conversation in the future, so make sure you have an understanding of everything.

The files are in markdown format, numbered sequentially and contain overlapping content (512 Bytes) to ensure continuity. Pay special attention to the **last file**, as it contains our most recent exchanges. If any chunks are missing or unclear, let me know.

There are 7 total conversation files in Markdown format. Since I can only upload **10 files at a time**, I will inform you when all batches are uploaded. Please reply with **"Received. Ready for next batch."** after you have had a chance to review and summarize the batch internally until I confirm all uploads are complete.

Once all files are uploaded, I will provide your initial instructions, and we will resume working together. At that time, we will discuss your **memory of our previous conversation** to ensure alignment before moving forward.
```

Be sure to change the file count, overlap and anything else that is needed to make it work for your use case.