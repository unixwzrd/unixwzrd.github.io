---
layout: post
title: "UnicodeFix v1.2.1: Smoother Installs, Cleaner Reports, Less Weirdness"
image: /assets/images/projects/UnicodeFix/Wolf-Edition-Enhancements.png
date: 2026-03-06
category: UnicodeFix
tags: [unicode, python, text-cleaning, ai, developer-tools, open-source]
excerpt: "UnicodeFix v1.2.1 makes the tool easier to install, easier to trust, and much less likely to surprise you with confusing reports or rough edges."
published: true
---

## UnicodeFix v1.2.1: The "Smooth the Edges" Release

Not every release needs fireworks.

Some releases need to do something quieter, and honestly more useful:
**remove friction.**

UnicodeFix v1.2.1 is that kind of release.

This update is about making the tool feel better in real use:

- easier to install
- easier to understand
- less confusing when you ask for metrics
- more honest in how it reports what it found

In other words: less "why is it doing that?" and more "yes, that is exactly what I wanted."

---

## First: Installation Finally Got Less Annoying

One of the big cleanup jobs in this release was the install path.

Before, UnicodeFix had a few too many ways to get itself onto a system.
That usually sounds flexible until you're the person trying to figure out which path is the *real* one.

v1.2.1 tightens that up.

Now the project uses **`pyproject.toml` as the single source of truth** for dependencies, and `setup.sh` acts like a sane bootstrap script instead of a side quest.

That means:

- no split-brain dependency story between `requirements.txt` and package metadata
- a cleaner path for contributors and regular users alike
- better alignment between local installs, docs, and CI

It also behaves more politely with Python environments now.
If you're already inside Conda, UnicodeFix should act like a good guest and install there instead of wandering off and building a surprise environment on its own.

That sounds small.
If you've ever lost ten minutes to "which Python did this install into?" you know it is not small.

---

## The Hyphen Fix That Should Have Been There Already

This release also fixes one of those maddening Unicode details that only becomes obvious after it breaks something important.

UnicodeFix now normalizes additional dash and hyphen variants, including the **non-breaking hyphen** (`U+2011`).

That matters because these characters are sneaky.
To a human reader they often look perfectly normal.
To a terminal, linter, parser, or diff tool, they are very much *not* normal.

So if you've ever had text that looked clean but still behaved strangely, this is exactly the kind of thing that causes it.

Now UnicodeFix catches more of those cases by default.

---

## Metrics Now Behave Like a Person Thought About Them

The `--metrics` feature got one of the most practical improvements in the entire release.

Before, the behavior around metrics could feel a little too clever in the wrong way.
You might ask for metrics and get output that wasn't quite what you expected.
Or ask for cleaned output and wonder why the reporting behavior changed.

v1.2.1 makes that much clearer:

- `cleanup-text --metrics file.txt` gives you a report
- if you explicitly ask for cleaned output with `-o` or `-t`, UnicodeFix still writes the cleaned file
- and now the report is emitted as a **side report**, so you can see what happened without losing the clean output you asked for

That is a much better contract.

You say what you want.
The tool does that.
And it doesn't make you decode its mood afterward.

---

## Reports Are More Honest Now

This is my favorite kind of fix: the kind that makes a tool more trustworthy.

UnicodeFix's scanner/reporting logic now does a better job separating what is merely **informational** from what is actually an **anomaly**.

A good example is quote counting.

This release splits quote-like characters into more useful categories, so the tool can distinguish between:

- normal ASCII quote characters
- Unicode quote-like characters that may actually be suspicious or worth cleaning

That means if you clean a file and run it back through the tool, you are less likely to get a misleading "something is still wrong" vibe just because the file contains ordinary apostrophes or quotation marks.

That is a subtle change, but it matters a lot.
If a report tool overstates the problem, people stop trusting the report.

This release pushes UnicodeFix in the opposite direction:
**fewer false alarms, clearer signal.**

---

## A Quiet But Important Python Compatibility Fix

UnicodeFix now behaves better across Python versions too.

There was a compatibility issue around `tomllib`, which is available in newer Python versions but not older ones like 3.9 and 3.10.
That got cleaned up by falling back to `tomli` where needed.

The result:

- smoother installs on older supported Python versions
- better CI coverage
- fewer "works on my machine" moments

And yes, the CI matrix was expanded too, because if you're going to claim support, you should actually test it.

---

## Who This Release Is Really For

This update helps a few different kinds of people.

### If you're technical

You get:

- a cleaner packaging story
- better CI behavior
- saner metrics/report interactions
- more accurate anomaly reporting
- fewer environment surprises

### If you're not especially technical

You get something just as valuable:

- install it more easily
- run it with less confusion
- trust the output more quickly
- spend less time wondering whether the weirdness is your fault

That is one of my favorite things about this release.
It improves the developer experience **without** making the tool more intimidating.

---

## A Nice Example of What "Polish" Really Means

People talk about polish like it's decorative.

It usually isn't.

Most of the time, polish is just this:

> removing the little moments where software makes you stop and ask, "wait... what?"

UnicodeFix v1.2.1 does a lot of that.

It doesn't reinvent the project.
It makes the project feel more deliberate.

And for a tool that exists to clean up tiny hidden problems, that feels exactly right.

---

## Try It

If you've already been using UnicodeFix, this is a very easy upgrade to appreciate.

If you haven't used it yet, this is a nice release to start with.

Use it when:

- pasted text starts acting cursed
- your docs look normal but diff weirdly
- CI starts complaining about characters nobody can see
- you want a fast sanity check on whether a file is carrying invisible baggage

UnicodeFix is still the same basic idea:
clean the text, remove the gremlins, move on with your life.

This release just makes that whole experience smoother.

---

## In Short

UnicodeFix v1.2.1 brings:

- a unified install path
- better Conda/env behavior
- improved Unicode hyphen handling
- cleaner metrics/report behavior
- more accurate quote/anomaly reporting
- stronger Python compatibility and CI coverage

Not flashy.
Very useful.
Exactly the kind of release you want in a tool that lives in your daily workflow.

---

## Get It / Support It

Repo, issues, and discussions:

- https://github.com/unixwzrd/UnicodeFix

UnicodeFix is used pretty widely now, which is great.
What it has not done particularly well is pay for the time it takes to keep improving it.

This project keeps moving because people use it, report weird edge-cases, open issues, send patches, and occasionally throw a little fuel on the fire so more of that work can happen.

If UnicodeFix has saved you time, cleaned up a mess, helped your workflow, or spared you one of those invisible-character debugging sessions that steals an afternoon, support is appreciated.

Support the work:

- [Patreon](https://patreon.com/unixwzrd)
- [Ko-fi](https://ko-fi.com/unixwzrd)
- [Buy Me a Coffee](https://buymeacoffee.com/unixwzrd)

Bug reports welcome. PRs welcome. New glyph sightings especially welcome.

This project evolves because people keep finding new ways for text to become cursed.

UnicodeFix is how we un-curse it.

* - Mia & the unixwzrd*
