---
layout: project
title: "Secrets Kit"
category: Secrets-Kit
permalink: /projects/Secrets-Kit/
excerpt: "Secrets Kit version 1 is available for local secrets management. Version 2 is in limited-access beta, with macOS/Linux support and peer-to-peer replication."
image: /assets/images/projects/Secrets-Kit-Banner.png
---

Designed for local AI workflows, developer tooling, and shell-driven systems that still rely on environment variables.

Secrets Kit is a local-first secrets CLI that stores credentials locally and passes selected values to a child process with `seckit run` when that process actually needs them. This helps keep API keys and tokens out of `.env` files, copied commands, and startup scripts. The available version 1 provides the basic local secrets workflow on macOS.

Version 2 is currently in limited-access beta. It supports macOS and Linux, with Keychain or encrypted SQLite storage and authenticated encrypted peer-to-peer replication. Optional RSS forwarding connects peers across networks, and a policy-scoped, read-only MCP interface supports tools that need it. Ordinary command-line use does not depend on MCP or a hosted service.

None of that makes it a guarantee against compromise. A child process can still expose values through its own environment, logs, or behavior, and Secrets Kit cannot protect a machine or account that is already compromised. It is a local operator tool, not a hosted vault or a substitute for reviewing the systems that receive your secrets.

What it does offer is a more deliberate workflow than leaving credentials in source trees or shell history. Start with local storage and selected injection; use version 2's peer replication only when you need it and understand the trust boundary.

## Availability

**Version 1 is available** for basic local secrets management. See the [published releases](https://github.com/unixwzrd/Secrets-Kit/releases) for version-specific release information.

**Version 2 is in limited-access beta**, with access restricted to authorized testers. Its general release will follow completion of beta testing and review of the remaining feedback. Windows compatibility has not yet been tested, so Windows is not currently listed as supported.

If you plan to use it with valuable credentials, read the [project's safety and installation guidance](https://github.com/unixwzrd/Secrets-Kit) and test the workflow with disposable values first.

## Related Work

- [LLM Ops Kit](/projects/LLM-Ops-Kit/) uses the same local-first operating philosophy for self-hosted AI stacks.
- [Professional Services](/collaborate/professionals/) covers consulting for secure automation, local AI setup, and developer infrastructure.

[View Secrets Kit on GitHub](https://github.com/unixwzrd/Secrets-Kit)
