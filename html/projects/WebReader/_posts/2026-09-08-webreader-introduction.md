---
short_link_basis: "/projects/WebReader/_posts/2026-09-08-webreader-introduction.md"
short_url: "https://unixwzrd.ai/s/9de0be2ea2/"
permalink_slug: "webreader-introduction"
layout: post
title: "Introducing WebReader for Safari: Listen to the Web Through Your Own TTS"
date: 2026-09-08
category: WebReader
content_type: introduction
tags: [tts, local-first, macos, developer-tools]
excerpt: "WebReader for Safari turns selected text or complete Safari articles into temporary speech through a local TTS system that remains under your control."
image: /assets/images/projects/WebReader/webreader-banner.png
published: true
---

I did not set out to build another browser extension. I was proofreading a long technical article by listening to it through my local text-to-speech system, and the spoken version immediately exposed things I had stopped seeing on the page. A stray change from "I" to "we" sounded obvious. So did stiff paragraphs, repeated phrases, and sentences that looked acceptable but became exhausting when read aloud.

<!--more-->

The first helper worked only on my own site. That solved the immediate problem, but it also made the limitation hard to ignore. I read documentation, project pages, news, and long-form articles in the same browser. I wanted to select a passage on any of those pages, press Play, and hear it through the TTS system I was already operating.

That small detour became **WebReader for Safari**.

## The Useful Part Is the Boundary

WebReader for Safari is not a speech engine. It is the browser-facing part of a local speech pipeline.

The Safari extension finds the article, strips away the usual page furniture, and decides what should be read. Selected text wins. If I have not selected anything, I can place the cursor in the article and continue from there. If neither applies, WebReader for Safari reads the detected article from the beginning.

The extension sends that text to a loopback-only relay, which passes it to the TTS Bridge managed by [LLM-Ops-Kit](/projects/LLM-Ops-Kit/). The bridge calls the speech engine configured behind it. That gives the browser one stable local interface without baking a particular model, provider, voice, or private deployment into the extension.

The ordinary playback path does not create an audio library behind my back. Synthesized audio stays in memory and disappears when playback is finished. Saving a narrated article can be a separate, explicit workflow later; it should not be an accidental side effect of pressing Play.

## Reading the Article, Not the Website

Getting audio back from a TTS endpoint was the easy part. Deciding what to send was more interesting.

Web pages contain menus, buttons, advertisements, forms, comments, related stories, and enough footer material to turn a five-minute article into a recital of somebody's entire navigation system. WebReader for Safari uses Mozilla Readability to identify the main article and then applies additional filtering before it sends anything to speech.

That filtering is intentionally practical rather than magical. If I select text, WebReader for Safari reads exactly that passage. If I ask for the article, it tries to give me the title and prose while leaving the machinery of the page alone.

## A Small Player That Stays Out of the Way

Pressing the Safari toolbar button adds a compact player to the current page. It has Restart, Play, Pause, Stop, and Hide controls. Restart returns to the detected title, while Play respects a selection or cursor position when one is available.

Safari also introduced a useful engineering wrinkle. Some sites use a Content Security Policy that blocks the usual `blob:` media path even when the relay has returned perfectly valid audio. WebReader for Safari detects that case and falls back to decoded, in-memory Web Audio playback. The page's policy remains in force, and the reader still gets to speak.

## Local First Does Not Mean One Giant Program

The source repository contains the extension, generated Safari wrapper, local relay, tests, icons, and its pinned Readability library. It does not copy [LLM-Ops-Kit](/projects/LLM-Ops-Kit/) into the tree or bundle a TTS model.

The supported runtime does depend on [LLM-Ops-Kit](https://github.com/unixwzrd/LLM-Ops-Kit) for the managed TTS Bridge. The actual speech engine, models, voices, and any authorized voice-reference material remain separately owned. I prefer that arrangement because each part has a job I can explain, test, replace, and operate without pretending the whole chain is one application.

## Current State

WebReader for Safari currently supports selected-text playback, cursor-aware starts, complete-article reading, temporary in-memory audio, active-tab permission, and the restrictive-site playback fallback in Safari. It is a working personal tool and an early public project, not a claim that every page on the web has suddenly become well-structured.

## Next Work

The immediate work is mostly about making the reader more comfortable to use across a wider range of real pages while keeping the interface small. Provider configuration and saved narration are natural directions, but they should preserve the boundary that made the first version useful: the browser chooses and plays clean text, while the speech and operations layers remain replaceable services.

The source and setup instructions are available in the [WebReader for Safari repository](https://github.com/unixwzrd/WebReader). The [WebReader for Safari project page](/projects/WebReader/) will collect future updates.
