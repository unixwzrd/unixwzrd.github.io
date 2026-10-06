---
layout: project
title: "Secrets Kit"
category: Secrets-Kit
permalink: /projects/Secrets-Kit/
excerpt: "Secrets Kit is a local-first secrets CLI for macOS and Linux, with Keychain or encrypted SQLite storage, selected environment injection, and peer synchronization."
image: /assets/images/projects/Secrets-Kit-Banner.png
---

Designed for local AI workflows, developer tooling, and shell-driven systems that still rely on environment variables.

Secrets Kit is a local-first secrets CLI for macOS and Linux. It can store sensitive values in the macOS login Keychain or encrypted SQLite, then pass selected values to a child process with `seckit run` when that process actually needs them. This helps keep API keys and tokens out of `.env` files, copied commands, and startup scripts.

The public beta also supports authenticated encrypted peer synchronization, with optional RSS forwarding for peers across networks. There is a policy-scoped, read-only MCP interface for tools that need it, but ordinary command-line use does not depend on MCP or a hosted service.

None of that makes it a guarantee against compromise. A child process can still expose values through its own environment, logs, or behavior, and Secrets Kit cannot protect a machine or account that is already compromised. It is a local operator tool, not a hosted vault or a substitute for reviewing the systems that receive your secrets.

What it does offer is a more deliberate workflow than leaving credentials in source trees or shell history. Start with local storage and selected injection; add peer synchronization only when you need it and understand the trust boundary.

## Availability

Secrets Kit has a **public beta for macOS and Linux**; there is no stable production release yet. Use the [current public beta release and its installation instructions](https://github.com/unixwzrd/Secrets-Kit/releases) rather than an old article or a moving development branch. Private development and QA builds are separate from the public beta.

If you plan to use it with valuable credentials, read the [project's safety and installation guidance](https://github.com/unixwzrd/Secrets-Kit) and test the workflow with disposable values first.

## Related Work

- [LLM Ops Kit](/projects/LLM-Ops-Kit/) uses the same local-first operating philosophy for self-hosted AI stacks.
- [Professional Services](/collaborate/professionals/) covers consulting for secure automation, local AI setup, and developer infrastructure.

[View Secrets Kit on GitHub](https://github.com/unixwzrd/Secrets-Kit)
