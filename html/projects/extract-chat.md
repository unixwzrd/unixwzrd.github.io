---
layout: project
title: "Extract Chat"
category: extract-chat
image: /assets/images/projects/extract-chat-banner.png
permalink: /projects/extract-chat/
excerpt: "Extract Chat turns downloaded ChatGPT or OpenAI conversation JSON into readable Markdown or HTML, preserves the useful structure, and makes it practical to archive, publish, or chunk conversations for downstream AI workflows."
---

If you have ever exported a ChatGPT conversation and then opened the JSON only to realize it was technically useful but not exactly human-friendly, `extract-chat` is the tool meant to fix that.

It takes raw ChatGPT or OpenAI conversation exports and turns them into something you can actually work with. Instead of a pile of structured data that mostly makes sense to a machine, you get readable Markdown, clean HTML, and output that is much easier to archive, review, publish, or reuse in other AI workflows.

What makes it especially useful is that it does not just flatten everything into plain text and call it a day. It preserves the structure that matters. References and citations stay intact. Hidden tool activity can still be surfaced. Longer conversations can be broken into chunks that are easier to feed into embeddings, retrieval workflows, or agent systems.

This makes `extract-chat` a natural companion to [LogGPT](/projects/LogGPT/). [LogGPT](/projects/LogGPT/) gives you the exported conversation JSON, including an easy App Store path for Safari users, and `extract-chat` turns that exported conversation into something worth keeping. Together they form a much more practical workflow for anyone who wants local control over their AI conversation history.

If your ChatGPT sessions are more than disposable chat, if they contain research, writing, debugging, analysis, or context you may need again later, `extract-chat` helps turn that history into something readable, portable, and genuinely reusable.

For code, usage, and installation details, see the project repository:

[View extract-chat on GitHub](https://github.com/unixwzrd/extract-chat)
