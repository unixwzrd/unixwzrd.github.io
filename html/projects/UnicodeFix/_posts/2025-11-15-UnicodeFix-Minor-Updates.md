---
layout: post
title: "UnicodeFix Levels Up: Metrics, Forensics, and Bracket Discipline"
image: /assets/images/projects/UnicodeFix/LevelsUp.png
date: 2025-11-15
category: UnicodeFix
tags:
  - unicode
  - python
  - ai
  - text-cleaning
  - detection
  - open-source
  - shortcuts
  - devtools
  - ai-watermarks
  - anti-cheat
  - codex
  - analytics
  - forensics
  - brackets
excerpt: "UnicodeFix grew a dashboard in your terminal: reports, metrics, and stricter Unicode discipline - same exorcism, more forensics."
published: true
---

## UnicodeFix Grew a Brain

Last time I wrote about UnicodeFix, it was in full CodExorcism mode:
burn the smart quotes, banish zero-width daemons, normalize ellipses, and make Codex's Unicode gremlins someone else's problem.

Since then, the tool did what all good exorcists eventually do:
it learned to **take notes on the hauntings.**

The current release line is:

> **UnicodeFix - CodExorcism Edition+ v1.1.3**

Same mission (wipe AI breadcrumbs and Unicode trash), but now it can **analyze** what it just cleaned - and tell you how weird your text looked before the ritual.

---

## From "Just Clean It" to "Show Me the Crime Scene"

The big change is that UnicodeFix is no longer just a firehose; it's also a **forensics report**.

You still have the classic "make this text not suck" workflows:

```bash
# Filter mode (STDIN → STDOUT)
cat draft.md | cleanup-text > draft.clean.md

# Batch clean
cleanup-text *.txt

# In-place, with temp file safety
cleanup-text -t important.txt
```

But now there's a whole analysis layer bolted on top:

```bash
# Human-readable audit
cleanup-text --report notes.md

# JSON report (for scripts/CI)
cleanup-text --report --json notes.md

# Add experimental semantic metrics
cleanup-text --report --json --metrics essay.md
```

### What the Metrics Do (and Don't Do)

Turn on `--metrics` and UnicodeFix will attach a **metrics block** to the report:

- Entropy / diversity
- ASCII vs Unicode ratios
- Repetition patterns
- A heuristic "AI-likeness" score

This is **not** a magical AI-detector. It's a **dashboard**:

- "Why does this look machine-generated?"
- "Why is this file full of weird Unicode when the rest of the repo isn't?"
- "Why did my CI suddenly start yelling at me?"

Pair it with:

- `--metrics-help` for a friendly legend (and ↑/↓ hints)
- `--exit-zero` to keep CI/pre-commit runs informative without breaking your flow
- `--threshold` when you *do* want to fail the pipeline if things get too spooky

Example:

```bash
# Warn, don't break commits
cleanup-text --report --metrics --exit-zero src/**/*.py

# Fail CI if anomalies cross your line in the sand
cleanup-text --report --threshold 1 docs/**/*.md
```

---

## Unicode Discipline: Fullwidth Brackets & Friends

The 2025-11-15 update (v1.1.3) did a little Unicode housekeeping too:

- **Fullwidth square brackets** `[]` now fold to ASCII `[]` **by default**
  - keeps tables, code blocks, and terminal output aligned
- If you're doing something visual/typographic and you *want* the fullwidth flavor:

```bash
cleanup-text --keep-fullwidth-brackets manuscript.md
```

The dagger `†` (e.g., for footnote markers) is left alone.
We're exorcising daemons, not your typography.

There's also a small helper for **display-only folding** if you want to keep your source text intact but render it in ASCII for terminals:

- `unicodefix.transforms.fold_for_terminal_display(text)`

Use it when you want clean-looking logs without mutating the original content.

---

## Test Harness: Less Ceremony, More Coverage

The test suite grew up too.

Instead of a thicket of bespoke scripts, there's now a single entry point:

```bash
tests/test_all.sh
```

What it does:

- Builds its run list automatically from `data/`
- Exercises all the main scenarios:
  - default clean
  - invisible-preserving (`-i`)
  - no-newline (`-n`)
  - custom output (`-o`)
  - in-place (`-t` / `-t -p`)
  - STDIN/STDOUT filter mode
- Drops **diffs** and **word-count comparisons** into `test_output/<scenario>/`

Binary fixtures are sensibly skipped in STDIN/STDOUT mode so the run doesn't explode on UTF-8 decoding.

Cleanup is one command away:

```bash
tests/test_all.sh clean
```

If you're wiring UnicodeFix into CI, this harness is basically your paranoia button: push it before you publish, push it before you grade, push it before you merge PRs that smell like AI copy-paste.

---

## Install / Upgrade in 60 Seconds

The installer path also got cleaned up and clarified.

Fresh install:

```bash
git clone https://github.com/unixwzrd/UnicodeFix.git
cd UnicodeFix

./setup.sh               # creates a venv and installs dependencies

# Standard usage
pip install .

# Dev/editable mode
pip install -e .

# With optional NLP metrics support
pip install .[nlp]
```

The README and `setup.sh` now actually explain what just happened, how to activate the env, and how to get from "clone repo" to "cleanup-text on PATH" without spelunking.

---

## Real-World Use Cases (Now With Forensics)

### Students

- Clean AI-assisted code before handing it in
- Run `--report --metrics` on your own work to understand **why** it looks suspicious
- Use `--exit-zero` so your local checks warn you without blocking the compile/push cycle

### Devs

- Put `cleanup-text --report --threshold N` into CI to catch sketchy Unicode in PRs
- Run `cleanup-text -t` on config files, docs, and scripts cloned from random Gists
- Keep logs / emails / release notes looking hand-typed instead of LLM-sprayed

### Writers / Bloggers

- Use `-Q` and `-D` to **keep** smart quotes and em dashes where you actually want them
- Let UnicodeFix handle the invisible junk, weird spaces, and stray AI fingerprints
- Run `--report` on drafts to see where editors/LLMs have been "helpful" behind your back

---

## TL;DR

Since the last CodExorcism post, UnicodeFix:

- **Added analytics**: `--report`, `--json`, `--metrics`, `--metrics-help`, `--threshold`, `--exit-zero`
- **Slimmed and hardened the test suite**: `tests/test_all.sh` drives everything from `data/`
- **Tightened Unicode behavior**: default folding for fullwidth square brackets with an escape hatch flag
- **Polished the installer and docs** so the path from "clone" to "clean" is straightforward

Same attitude, sharper tools.

If you're already using UnicodeFix, pull the latest and run your usual workflows with `--report` once - it's weirdly satisfying to watch your own files get roasted in the terminal.

If you're new:

- Repo: <https://github.com/unixwzrd/UnicodeFix>
- Shortcut, tests, docs, and screenshots are all in there.

The Unicode arms race isn't slowing down.
At least your side has better metrics now.
