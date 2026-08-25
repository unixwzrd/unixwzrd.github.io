---
permalink_slug: "launchd-seckit-run-and-invisible-env-vars"
legacy_project_permalink: "/projects/Secrets-Kit/2026/05/04/secrets-kit-1-2-launchd-seckit-run-and-invisible-env-vars/"
short_url: "https://unixwzrd.ai/s/53370b7288/"
layout: post
slug: launchd-seckit-run-and-invisible-env-vars
title: "Secrets Kit 1.2: launchd, seckit run, and invisible env vars"
date: 2026-05-04
category: Secrets-Kit
tags: [launchd, macos, secrets-management, ai-agents, local-ops]
content_type: release
excerpt: "Version 1.2 leans into the boring superpower: run real programs - Hermes, OpenClaw, whatever - without painting secrets on the process list, and wire that story into launchd without turning your plist into a confession booth."
image: /assets/images/projects/Secrets-Kit-Banner.png
published: true
---

## Secrets Kit 1.2: launchd, invisible env vars, and why API keys shouldn't ride shotgun on argv

Feynman had a habit of boiling things down to what actually matters. If you can't explain it to a freshman, you probably don't understand it. Thompson might add: if you're explaining it while the engine is on fire, bring better tools - because adrenaline is expensive and key rotation is worse.

Secrets Kit **1.2.0** is that kind of release: less spectacle, more structural integrity. The kind where nothing flashy happens, and everything quietly stops breaking.

<!--more-->

### Here's the plot.

Most of us learned to pass API keys like contraband in a crowded room: export them in a shell, paste them into a `.env`, duplicate them into a launchd plist because "it worked once," and then pretend `ps eww` is not a thing.

Spoiler: it is. So is your shell history. So is every log line that ever captured argv when you weren't looking.

**`seckit run`** is the workaround that sounds boring until you actually watch it behave.

The parent (`seckit`) talks to Keychain, pulls the values you asked for, drops them into the **child's environment**, and hands off to your real program. The secret never becomes a command-line argument. Nothing gets pinned to the process list like it's a parade float.

Quick example, same vibe as the docs but slightly more awake with black coffee:

```bash
echo 'sk-demo-not-real' | seckit set --name OPENAI_API_KEY --stdin \
  --kind api_key --service my-agents --account launchd

seckit run --service my-agents --account launchd -- \
  python3 -c "import os; print('set' if os.getenv('OPENAI_API_KEY') else 'missing')"
```

Set defaults once and the launch line collapses into something almost offensively simple:

```bash
seckit run -- /path/to/your/actual/binary
```

That pattern is what makes **launchd** bearable. `launchd` is a fine scheduler with a weakness: it loves XML, and XML loves to leak structure the minute you stuff secrets into `EnvironmentVariables`. So don't. Make `ProgramArguments` a **wrapper**, not a vault.

### launchd without the confession booth

`launchd` is a solid scheduler with one unfortunate personality trait: it happily exposes whatever you feed it.

So don't feed it secrets.

Make `ProgramArguments` a wrapper, not a vault:

```xml
<key>ProgramArguments</key>
<array>
  <string>/usr/local/bin/seckit</string>
  <string>run</string>
  <string>--service</string>
  <string>hermes</string>
  <string>--account</string>
  <string>local</string>
  <string>--</string>
  <string>/Users/you/.venv/hermes/bin/hermes</string>
  <string>gateway</string>
  <string>start</string>
</array>
```

Same camera angle for **OpenClaw** (or any other long-running "always there" agent): **`seckit run` first**, then your usual subcommand. The plist stays boring. Boring plists age well.

### Operator candy

Shipped alongside the good manners:

- **`seckit version --json`** and **`--info`**: for scripts and humans who want to see the world as a small, honest data structure instead of squinting at four different terminal panes.
- **CI and release hygiene** that actually touches **every** Python the project claims to support - including **3.13** - so "it works on my laptop" stays a joke and not a deployment strategy.
- **Cross-host moves** stay the adult path: **`seckit export`** → encrypted artifact → **`seckit import`** on the other Mac. No fairy dust. It works in hotel Wi-Fi and in your lab.

### Cross-host reality

There's no magic sync story here, and that's intentional.

You export, you move the file, you import:

```
seckit export → encrypted artifact → seckit import
```

It works on hotel Wi-Fi. It works in a lab. It works when things are slightly broken, which is most of the time.

### The iCloud Keychain chapter (honest edition)

We've spent real time on **synchronizable Keychain** paths - native helper, entitlements, the whole song-and-dance - because "synced secrets" is a beautiful idea until the operating system decides your helper is **not** allowed to have nice things. In plain English: on a lot of macOS builds, the helper can get **`SIGKILL`** at launch (**taskgated**, **AMFI -413**, pick your villain) **even when notarization looks fine**. That's not a Python packaging tantrum; that's policy territory.

The helper gets shut down at launch:
- `SIGKILL`
- `taskgated`
- AMFI complaints

The work is **preserved in git** on branch **`preserve/icloud-backend-as-of-2026-05-05`** while we wait to hear something useful back from Apple. If the OS opens the door, you'll see that path return in a shape that doesn't waste your afternoon. Until then: **`seckit run`**, **launchd**, **export/import**. It's less science fiction and more "lunch with the laws of physics."

- `seckit run`
- launchd wrappers
- export/import

Less fantasy, more physics.

### Install / peek

```bash
pip install "git+https://github.com/unixwzrd/Secrets-Kit.git@v1.2.0"
seckit version
seckit version --info
```

Repo and deeper docs: [Secrets-Kit on GitHub](https://github.com/unixwzrd/Secrets-Kit).

---

*P.S. If you already read the gentle introduction post, this is the one where the rubber meets `launchd`. Same philosophy: fewer secrets on disk, fewer secrets in argv, fewer apologies later.*
