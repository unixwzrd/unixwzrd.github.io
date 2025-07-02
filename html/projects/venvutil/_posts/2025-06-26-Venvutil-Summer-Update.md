---
image: /projects/venvutil/images/Herding-Cats-and-Virtual-Environments.png
title: "VenvUtil Update: Smarter Shell-Based Python Environment Management"
layout: post
redirect_from:
  - /projects/venvutil/2025/06/26/Venvutil-Summer-Update/
date: "2025-06-25"
category: venvutil
tags: [update, virtualenv, conda, devtools]
draft: false
published: true
excerpt: "The VenvUtil shell toolkit is evolving fast: improved command logging, smarter environment rollbacks, easier cloning, and real-world robustness for anyone working in Python on macOS or Linux."
---

Python environment chaos-everyone's been there. Broken builds, mismatched dependencies, mysterious bugs after a 'quick' pip install… and then you realize your environment is borked and your rollback is, well, 🤷.

That's why I built **VenvUtil**: to make managing and recovering Python environments as painless (and transparent) as possible-right in the shell.

## What *Actually* Is VenvUtil?

VenvUtil isn't just a set of wrappers-**it's a full-featured shell library and command-line toolkit** for working with Python virtual environments at scale, especially for anyone juggling machine learning, scientific, or reproducible workflows.

- **4,500+ lines of portable shell code**: POSIX-compliant, modular, and battle-tested for the weirdest edge cases.
- **Comprehensive command logging**: Every environment-altering command (install, uninstall, clone, remove, update, etc.) gets a forensic-grade audit trail:
    - Full command line, with env vars
    - Venv name (even for clones, removals, or deletes by path)
    - User, host, working directory, Python version, and timestamp
    - Package "freeze" snapshot before/after
    - Persistent logs-**even after env deletion**
- **Snapshotted rollbacks**: Any time you run a destructive command, you get an instant rollback point-just restore the previous freeze file.
- **Handles *all* the odd cases**: Whether you clone by path, remove by name, or clean up after a failed install, VenvUtil logs it all and keeps it readable.
- **Pluggable for other package managers**: It's not just `pip` and `conda`-we're working on native support for other Python package managers that are Conda-venv compatible (e.g. `mamba`, `micromamba`, `pixi`, `poetry` with conda plugins, and more).
- **Shell utilities you can actually reuse**: The included libraries (POSIX error handling, argument parsing, etc.) can be used in your own scripts, not just VenvUtil.
- **Does not depend on `brew`-works on stock macOS, Linux, and more.**

---

## Bonus Utilities: Go Beyond Virtualenv

VenvUtil ships with extras that make modern Python dev (especially for AI/ML) much less painful:
- **`genmd`**: Wrap your project's source files, scripts, and notebooks in Markdown-bundled with a visual file tree. Makes it trivial to prep AI ingestion or context-sharing with LLMs.
- **`extract-chat`**: Convert OpenAI JSON chat logs to Markdown or HTML, so you can keep "memory" between AI sessions (or just make your prompt history readable).
- **`venvutil diff` (`vdiff`)**: Compare package lists across environments or at points in time.
- **`lenv`**: List all your Conda environments, with metadata, creation dates, and paths-highlighting which is active and which are stale.

There's a lot under the hood. If you want robust shell tools for Python, you can use VenvUtil's libraries in your own automation scripts.

<div style="text-align: center">
<img src="/projects/venvutil/images/Ordering_Venvs.png" alt="Order From Chaos">
</div>

## Example: Audit, Clone, Roll Back - Tale of Two Logs

The logs are well formatted for CI/CD pipelines, development shops, and QA groups for keeping track of changes to the environment, down to who, what and when. This allows for virtual environments to be recreated consistently across environments, as well as helping to figure out what changes made something go wrong.

### Main Global VenvUtil Log
This is the master log file with all Pip and Conda "potentially destructive" commands logged.

```
# 2025-06-25 13:42:05 - python-3.11-website:  conda remove --all -n test-environment -y
# 2025-06-25 13:43:22 - python-3.11-website:  conda create --clone python-3.11-website -n python-3.11-website -y
# 2025-06-25 14:07:08 - test-environment:  conda create --clone python-3.10-PA-dev -n test-environment -y
# 2025-06-25 14:07:08 - python-3.10-PA-dev:  conda create --clone python-3.10-PA-dev -n test-environment -y
# 2025-06-25 14:09:08 - test-environment:  pip install lorem
# 2025-06-25 14:10:45 - test-environment:  pip uninstall lorem
# 2025-06-25 14:13:47 - test-environment:  conda remove --all -n test-environment -y
# 2025-06-25 14:14:13 - python-3.10-PA-dev:  conda remove --all -n test-environment -y
```

### Log for a Single Venv

This is the log for a single venv, showing the full command line, the virtual environment name, the working directory, user, and host, and the package state before and after each operation.

```
# ==> 2025-06-25 14:07:08 <==
# 2025-06-25 14:07:08: Success:  conda create --clone python-3.10-PA-dev -n test-environment -y
# 2025-06-25 14:07:08: Return code: No error
# 2025-06-25 14:07:08: conda 25.3.1
# 2025-06-25 14:07:08: UID: 1002 EUID:1002) HOST: xanax.local CWD: /Users/mps/.venvutil
# 2025-06-25 14:07:08: State: /Users/unixwzrd/.venvutil/freeze/test-environment.20250625140708.txt
# ==> 2025-06-25 14:09:08 <==
# 2025-06-25 14:09:08: Success:  pip install lorem
# 2025-06-25 14:09:08: Return code: No error
# 2025-06-25 14:09:08: pip 24.2 from /Users/unixwzrd/miniconda3/envs/test-environment/lib/python3.11/site-packages/pip (python 3.11)
# 2025-06-25 14:09:08: UID: 1002 EUID:1002) HOST: xanax.local CWD: /Users/mps/.venvutil
# 2025-06-25 14:09:08: State: /Users/unixwzrd/.venvutil/freeze/test-environment.20250625140908.txt
# ==> 2025-06-25 14:10:45 <==
# 2025-06-25 14:10:45: Success:  pip uninstall lorem
# 2025-06-25 14:10:45: Return code: No error
# 2025-06-25 14:10:45: pip 24.2 from /Users/unixwzrd/miniconda3/envs/test-environment/lib/python3.11/site-packages/pip (python 3.11)
# 2025-06-25 14:10:45: UID: 1002 EUID:1002) HOST: xanax.local CWD: /Users/mps/.venvutil
# 2025-06-25 14:10:45: State: /Users/unixwzrd/.venvutil/freeze/test-environment.20250625141045.txt
# ==> 2025-06-25 14:13:47 <==
# 2025-06-25 14:13:47: Failure:  conda remove --all -n test-environment -y
# 2025-06-25 14:13:47: Return code: (EPERM: 1): Operation not permitted
# 2025-06-25 14:13:47: conda 25.3.1
# 2025-06-25 14:13:47: UID: 1002 EUID:1002) HOST: xanax.local CWD: /Users/mps/.venvutil
```

Want to know **who** nuked your venv, or **when** a dependency got updated and broke your model training run? You've got a paper trail.


## Quick Install

Clone the repo and source the wrappers:

```
git clone https://github.com/unixwzrd/venvutil
cd venvutil
bash setup.sh install
exec bash -
```

The installer adds all necessary wrappers and helpers to your shell startup, creates a default environment, and lets you use pip/conda as usual-with all the safety and audit features built in. You can also use the `venvutil` command to get help on the commands and options.

## Works Great With LogGPT

Plus there are handy tools and utilities for managing your virtual environments, converting OpenAI JSON Chat logs into Markdown and HTML, and more. The go great with the [LogGPT Safari Extension](/projects/LogGPT/) which was just released again with two weeks of updates. You can get it form the [Apple App Store](https://apps.apple.com/us/app/loggpt/id6743342693?mt=12), or get the Xcode Project from the [GitHub Repo](https://github.com/unixwzrd/LogGPT) and build it yourself, of course if you teh tools useful and hand, you can always help contribute suggestions or code, and I'll never turn down a pizza or a [cup of coffee](https://www.ko-fi.com/unixwzrd). If you'd like to support my work on an on-going basis, I have a [Patreon](https://www.patreon.com/unixwzrd) and am also available for individual on-on-one consulting or projects.

## Known Issues & Roadmap

- Some edge cases for multi-env commands (like rename or oddball -n/-p combos) are not 100% bulletproof-yet.
- Next up: a proper `vhist` reporting tool for visualizing your environment history, plus a smoother upgrade path for Python major/minor versions (with instant rollback).
- If you break something, send me a bug or PR. (Nobody has yet, but you could be the first!)

## Roadmap & Contributions

- Full support for `mamba`, `micromamba`, `pixi`, and other managers that use Conda-style envs.
- `vhist` command for timeline-style audit reports.
- Streamlined upgrades and environment migration (Python 3.12+, rollback on failure).
- Polished docs and more how-to's.

If you break something or want to contribute, open an issue or PR-be the first!

---

Built by [unixwzrd](https://unixwzrd.ai) - for devs who'd rather code than debug "dependency hell." Mia the AI assistant approves. 🐾

*If you use VenvUtil and it makes your life better (or worse), let me know! And yes-support, coffee, and ideas are always appreciated.*