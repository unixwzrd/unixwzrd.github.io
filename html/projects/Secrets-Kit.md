---
layout: project
title: "Secrets Kit"
category: Secrets-Kit
permalink: /projects/Secrets-Kit/
---

Designed for local AI workflows, developer tooling, and shell-driven systems that still rely on environment variables.

Secrets Kit is a local macOS tool for managing API keys, passwords, tokens, and other sensitive values without leaving them scattered across `.env` files, shell startup scripts, copied commands, and forgotten project directories.

Instead of leaving that material in plain text all over the machine, Secrets Kit keeps secret values in the macOS login Keychain and keeps only non-secret metadata in a local registry. When a local UI, agent runtime, script, or development stack actually needs a value, Secrets Kit can export it into the current shell at that moment instead of expecting you to keep it sitting around in a source tree or startup script.

That does not make it a perfect security solution, and it should not be treated like one. Secrets Kit is not a hosted secret manager, not a vault, not a guarantee against compromise, and not a replacement for thinking carefully about what a local session can already access. If a machine or shell session is already compromised, no wrapper script is going to magically fix that.

What it does do is give you a much better default workflow than random `.env` files and copied secrets. It helps reduce secret sprawl, makes accidental GitHub commits less likely, and raises the bar against the easy, careless forms of exposure that happen when sensitive values are left lying around in plain text.

It is also intentionally simple. Secrets Kit does not collect secret information for itself, and it does not store your keychain password. Under the hood, it is a thin wrapper around the macOS `security` command plus a local metadata and workflow layer that helps you keep track of what belongs where.

That makes it a practical fit for local agent stacks, developer tooling, web UIs, and shell-driven workflows that still need environment variables, but do not need those values living forever in source directories or login scripts.

It replaces scattered habits with a single, consistent way to handle secrets locally.

[View Secrets Kit on GitHub](https://github.com/unixwzrd/Secrets-Kit)
