---
layout: post
title: "UnicodeFix - Wolf Edition v1.2.0 (It Solves Problems.) Now with API support."
image: /assets/images/projects/UnicodeFix/Wolf-Edition.png
date: 2026-01-14
category: UnicodeFix
tags:
 - unicode
 - python
 - ai
 - text-cleaning
 - detection
 - forensics
 - metrics
 - devtools
 - ci
 - github-actions
 - open-source
excerpt: "UnicodeFix isn't just a CLI. It's Winston Wolf for your text pipelines: clean it, audit it, score it, ship it."
published: true
---

## UnicodeFix - Wolf Edition v1.2.0

You ever paste text into a file and *immediately* know something's wrong?

Not "logic wrong."
Not "syntax wrong."
More like... **crime scene wrong**.

The file *looks* fine. But your linter screams. Your CI fails. Your professor narrows their eyes. Your YAML config collapses like a cheap folding chair. And you're sitting there thinking:

> "It's just text. Why does it feel like this text has... fingerprints?"

That's the entire reason UnicodeFix exists.

This release is what happens when a simple Unicode scrubber grows into something bigger:

- part **cleanup crew**
- part **forensics unit**
- part **workflow upgrade**
- and yes... part "please stop sprinkling invisible gremlins in my code."

If UnicodeFix were a character, it's not just Jules and Vincent doing a chaotic drive-by on your source files.

It's **Jules** and **Vincent**... plus **Winston Wolf** - *while Jimmy makes coffee with lots of cream and lots of sugar.*

It solves problems.

---

## The Problem You Can't See (But CI Can)

A lot of Unicode trouble isn't dramatic.

It's not a glowing glyph with lightning bolts.

It's the tiny stuff:

- invisible whitespace that changes indentation
- zero-width characters that break diffs
- curly quotes that look like ASCII but aren't
- ellipses that sneak into config or code comments
- bidirectional controls that can literally alter how text is displayed (yes, really)

This can come from LLMs... but it doesn't have to.

Unicode garbage shows up in:

- chat apps
- web pages
- PDFs
- Office docs
- transcript generators
- iMessage exports
- "copy code" buttons
- log pipelines
- *other people*

UnicodeFix doesn't clean the PDF directly, obviously.

It cleans what you *extract* from it.

That distinction matters - because it's where the *real power* is:

> Instead of writing Unicode normalization logic into 17 different scripts, you keep one "cleanup brain" in one library.

---

## Two Modes: Cleaner + Auditor (AKA: Body Work + Forensics)

UnicodeFix has always been able to clean text.

Wolf Edition makes it explicit:

- **Clean mode**: remove Unicode quirks, normalize typographic junk, fix whitespace.
- **Audit mode** (`--report`): scan text and tell you what you're dealing with.

In other words:

- Clean mode is the cleanup crew with the bleach.
- Audit mode is CSI Las Vegas with a clipboard and a flashlight.

Same tool. Two moods.

---

## The CLI Is Nice... But the API Is the Secret Weapon

A lot of people treat UnicodeFix like a command:

```bash
cleanup-text draft.md
```

But the API is where it quietly becomes a *serious dev tool*.

Because the minute you're doing extraction of any kind...

- parsing a DB dump
- converting HTML
- exporting chat logs
- processing transcript text
- cleaning OCR output
- streaming decoded tokens from a local model

...you want normalization *inside* the pipeline.

Not as an afterthought.

---

## Tutorial: Drop UnicodeFix Into Any Extraction Pipeline

Here's the trick:

1) extract the text
2) normalize it *once*
3) every downstream tool stays sane

### Step 1 - The boundary function (use this everywhere)

```python
from __future__ import annotations

from unicodefix.transforms import clean_text, handle_newlines


def normalize_extracted_text(raw: str) -> str:
 """
 Your 'Winston Wolf' function:
 call this right after extraction from PDF/html/chat/db/logs/etc.
 """
 cleaned = clean_text(raw)
 return handle_newlines(cleaned)
```

This is boring code.

Boring is good.

Boring means it works at 2:00 AM, with CI screaming at you, while someone's asking why the release tag didn't build.

---

## Real Example: iMessage / Chat Export Recovery

This is one of my favorite use-cases because it's so "non-AI."

You extract iMessage text (or other chat logs) from a database.

You get:

- odd non-breaking spaces
- weird line ending styles
- invisible marks
- formatting junk you never typed

You could handle it everywhere...

Or you do this once:

```python
from unicodefix.transforms import clean_text, handle_newlines

def normalize_chat_text(message: str) -> str:
 return handle_newlines(clean_text(message))
```

Now every exporter, formatter, report generator, and PDF builder in your pipeline benefits automatically.

That's the "one brain / many scripts" win.

---

## Audit Mode: Counting the Mess Before You Clean It

Here's where Wolf Edition gets fun.

Audit mode will scan text and report anomalies like:

- zero-width spaces
- smart quotes
- Unicode separators and NBSP variants
- bidi controls
- trailing whitespace lines
- missing final newline
- replacement characters (U+FFFD)

Run it like this:

```bash
cleanup-text --report notes.md
```

Want machine-friendly output?

```bash
cleanup-text --report --json notes.md
```

Now you can treat Unicode weirdness like lint.

Which is the entire point.

---

## Metrics Mode: "Is This Text... Suspicious?"

Now let's talk about the professor angle - because yes, UnicodeFix can play both sides.

Wolf Edition added **semantic metrics** (optional):

- entropy
- ascii ratio
- repetition ratio
- sentence-length variability ("burstiness")
- stopword ratio
- and a heuristic "AI score"

To enable it:

```bash
cleanup-text --report --metrics essay.md
```

This installs NLTK resources (tokenizers etc) via the optional extra:

```bash
pip install unicodefix[nlp]
```

### Important note

This is not a magical "AI detector."

It's a dashboard.

It's the difference between:

- "this *feels* AI-generated"
- and "here are measurable signals that explain why it feels that way"

And yes: professors love that kind of thing.

So do reviewers.

So do paranoid devs.

So do people who are tired of Unicode daemons in production.

---

## CI/CD: The Clock Is Ticking (And Wolf Doesn't Have Time for Excuses)

UnicodeFix is tested in GitHub Actions across:

- Ubuntu Linux
- macOS
- Python 3.9, 3.10, 3.11, 3.12

That matters because Unicode problems are often platform-flavored.

Different terminals, different default encodings, different newline behavior, different tools.

This pipeline doesn't just test Python unit tests - it runs integration tests and newline preservation checks too.

That last part is huge.

Because stripping or rewriting newlines is one of those "quiet disasters" that doesn't show up until you've destroyed a file and a human has to untangle it.

UnicodeFix does the opposite:

> clean the mess, preserve the structure.

---

## The Joke That's Also True

There's a scene in *Pulp Fiction* where Winston Wolf calmly walks into chaos and basically says:

> "If you do what I say, when I say it, we're gonna be okay."

UnicodeFix does that for text.

You've got invisible debris everywhere:

- little bits of ZWSP
- pools of NBSP
- splashes of bidi controls
- curly quotes pretending to be innocent civilians

UnicodeFix is the guy who shows up with:

- cleaning products
- metrics
- a report
- a plan

And yes:

- It's a floor wax.
- It's a dessert topping.
- It's a cleaner *and* an auditor.

---

## Get It / Support It

Repo + issues + discussions:

- https://github.com/unixwzrd/UnicodeFix

Support the work (coffee fuels commits):

- [Patreon](https://patreon.com/unixwzrd)
- [Ko-fi](https://ko-fi.com/unixwzrd)
- [Buy Me a Coffee](https://buymeacoffee.com/unixwzrd)

Bug reports welcome. PRs welcome. New glyph sightings especially welcome.

This project evolves because people keep finding new ways for text to become cursed.

UnicodeFix is how we un-curse it.

* - Mia & the unixwzrd*
