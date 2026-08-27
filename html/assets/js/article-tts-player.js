(() => {
  "use strict";

  const article = document.querySelector(".post-content.e-content");
  if (!article || !("AudioContext" in window || "webkitAudioContext" in window)) {
    return;
  }

  const relayUrl = window.localStorage.getItem("articleTtsRelayUrl") || "http://127.0.0.1:11441";
  const maxChunkCharacters = 900;
  const removedSelectors = [
    "aside",
    "nav",
    "figure",
    "table",
    "pre",
    "details",
    "script",
    "style",
    "noscript",
    "audio",
    "video",
    "button",
    "form",
    ".series-context",
    ".series-navigation",
    ".post-engagement",
    ".content-footer",
    ".support-section",
    ".post-comments",
    ".blog-diagram",
    "[aria-hidden='true']",
  ];

  const player = document.createElement("section");
  player.className = "article-tts-player";
  player.setAttribute("aria-label", "Article text-to-speech player");
  player.innerHTML = `
    <span class="article-tts-player__label">Listen</span>
    <button type="button" class="article-tts-player__button" data-action="restart" title="Restart from the beginning of the article">Restart</button>
    <button type="button" class="article-tts-player__button" data-action="play">Play</button>
    <button type="button" class="article-tts-player__button" data-action="pause" disabled>Pause</button>
    <button type="button" class="article-tts-player__button" data-action="stop" disabled>Stop</button>
    <span class="article-tts-player__status" role="status" aria-live="polite">Select text, place the cursor, or play the whole post.</span>
  `;
  document.body.append(player);
  document.body.classList.add("article-tts-enabled");

  const restartButton = player.querySelector('[data-action="restart"]');
  const playButton = player.querySelector('[data-action="play"]');
  const pauseButton = player.querySelector('[data-action="pause"]');
  const stopButton = player.querySelector('[data-action="stop"]');
  const status = player.querySelector(".article-tts-player__status");
  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  const usesNativeAudio = /Safari/i.test(navigator.userAgent) && !/(Chrome|Chromium|CriOS|Edg|OPR|FxiOS)/i.test(navigator.userAgent);
  const nativeAudio = usesNativeAudio ? document.createElement("audio") : null;
  const silentWav = "data:audio/wav;base64,UklGRsQAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";

  if (nativeAudio) {
    nativeAudio.hidden = true;
    nativeAudio.preload = "auto";
    nativeAudio.setAttribute("playsinline", "");
    nativeAudio.setAttribute("aria-hidden", "true");
    document.body.append(nativeAudio);
  }

  let audioContext = null;
  let activeSource = null;
  let activeObjectUrl = null;
  let objectUrls = new Set();
  let sessionId = 0;
  let chunks = [];
  let currentIndex = 0;
  let paused = false;
  let stopped = true;
  let pendingBuffer = null;
  let bufferPromises = new Map();
  let controllers = new Set();
  let queuedReadingTarget = null;
  let lastArticleCaret = null;
  let playbackScope = "article";

  function setStatus(message) {
    status.textContent = message;
  }

  function setControls({ playing = false, isPaused = false } = {}) {
    playButton.textContent = isPaused ? "Resume" : "Play";
    playButton.disabled = playing && !isPaused;
    pauseButton.disabled = !playing || isPaused;
    stopButton.disabled = !playing;
  }

  function ensureAudioContext() {
    if (!audioContext || audioContext.state === "closed") {
      audioContext = new AudioContextClass();
    }
    return audioContext;
  }

  function primeAudioOutput() {
    if (usesNativeAudio) {
      if (!nativeAudio.getAttribute("src") || nativeAudio.src.startsWith("data:")) {
        nativeAudio.src = silentWav;
      }
      nativeAudio.play().catch(() => {});
      return;
    }

    const context = ensureAudioContext();
    context.resume().catch(() => {});

    // Safari may refuse a source started after the asynchronous TTS request
    // unless audio was first touched during the user's button gesture.
    const source = context.createBufferSource();
    source.buffer = context.createBuffer(1, 1, context.sampleRate);
    source.connect(context.destination);
    source.start(0);
    source.addEventListener("ended", () => source.disconnect(), { once: true });
  }

  function cleanText(value) {
    return value
      .normalize("NFKC")
      .replace(/[\u200B-\u200D\uFEFF]/g, "")
      .replace(/&/g, " and ")
      .replace(/[→←↔•_|`*]/g, " ")
      .replace(/\//g, " ")
      .replace(/=/g, " equals ")
      .replace(/\+/g, " plus ")
      .replace(/\s+/g, " ")
      .replace(/\s+([,.;:!?])/g, "$1")
      .replace(/([(\[])\s+/g, "$1")
      .replace(/\s+([)\]])/g, "$1")
      .trim();
  }

  function rangeContainer(range) {
    return range.commonAncestorContainer.nodeType === Node.ELEMENT_NODE
      ? range.commonAncestorContainer
      : range.commonAncestorContainer.parentElement;
  }

  function currentArticleRange() {
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) {
      return null;
    }
    const range = selection.getRangeAt(0);
    const container = rangeContainer(range);
    if (!container || !article.contains(container)) {
      return null;
    }
    return range.cloneRange();
  }

  function readableTextFromFragment(fragment, includeTitle = false) {
    fragment.querySelectorAll(removedSelectors.join(",")).forEach((node) => node.remove());
    fragment.querySelectorAll("img").forEach((node) => node.remove());
    fragment.querySelectorAll("a").forEach((link) => {
      const visible = link.textContent.trim();
      const href = (link.getAttribute("href") || "").trim();
      if (/^(https?:\/\/|www\.)/i.test(visible) || visible === href) {
        link.remove();
      } else {
        link.replaceWith(...link.childNodes);
      }
    });

    const blocks = [];
    if (includeTitle) {
      const title = cleanText(document.querySelector(".post-title")?.textContent || "");
      if (title) {
        blocks.push(/[.!?]$/.test(title) ? title : `${title}.`);
      }
    }
    const blockSelector = "h2, h3, h4, p, li, blockquote";
    fragment.querySelectorAll(blockSelector).forEach((node) => {
      const parentBlock = node.parentElement?.closest(blockSelector);
      if (parentBlock && fragment.contains(parentBlock)) {
        return;
      }
      let text = cleanText(node.textContent);
      if (!text) {
        return;
      }
      if (/^H[2-4]$/.test(node.tagName) && !/[.!?]$/.test(text)) {
        text += ".";
      }
      if (blocks.at(-1) !== text) {
        blocks.push(text);
      }
    });
    if (blocks.length === 0) {
      const fallback = cleanText(fragment.textContent || "");
      if (fallback) {
        blocks.push(fallback);
      }
    }
    return blocks.join("\n\n");
  }

  function wholeArticleText() {
    return readableTextFromFragment(article.cloneNode(true), true);
  }

  function textFromCaret(range) {
    const readingRange = range.cloneRange();
    try {
      readingRange.setEnd(article, article.childNodes.length);
    } catch (_error) {
      return "";
    }
    return readableTextFromFragment(readingRange.cloneContents());
  }

  function readingTarget() {
    const selection = window.getSelection();
    const range = currentArticleRange();
    if (range && selection && !selection.isCollapsed) {
      return { text: cleanText(selection.toString()), scope: "selection" };
    }
    if (range?.collapsed) {
      lastArticleCaret = range.cloneRange();
      return { text: textFromCaret(range), scope: "cursor" };
    }
    if (lastArticleCaret) {
      return { text: textFromCaret(lastArticleCaret), scope: "cursor" };
    }
    return { text: wholeArticleText(), scope: "article" };
  }

  function splitLongText(text) {
    if (text.length <= maxChunkCharacters) {
      return [text];
    }
    const sentences = text.match(/[^.!?]+[.!?]+(?:["')\]]+)?|[^.!?]+$/g) || [text];
    const pieces = [];
    let current = "";
    for (const rawSentence of sentences) {
      const sentence = rawSentence.trim();
      const candidate = `${current} ${sentence}`.trim();
      if (current && candidate.length > maxChunkCharacters) {
        pieces.push(current);
        current = sentence;
      } else {
        current = candidate;
      }
      while (current.length > maxChunkCharacters) {
        let boundary = current.lastIndexOf(" ", maxChunkCharacters);
        if (boundary < 1) {
          boundary = maxChunkCharacters;
        }
        pieces.push(current.slice(0, boundary).trim());
        current = current.slice(boundary).trim();
      }
    }
    if (current) {
      pieces.push(current);
    }
    return pieces;
  }

  function makeChunks(text) {
    const result = [];
    let current = "";
    for (const paragraph of text.split(/\n{2,}/).map(cleanText).filter(Boolean)) {
      for (const piece of splitLongText(paragraph)) {
        const candidate = `${current}\n\n${piece}`.trim();
        if (current && candidate.length > maxChunkCharacters) {
          result.push(current);
          current = piece;
        } else {
          current = candidate;
        }
      }
    }
    if (current) {
      result.push(current);
    }
    return result;
  }

  async function loadBuffer(index, expectedSession) {
    if (bufferPromises.has(index)) {
      return bufferPromises.get(index);
    }
    const promise = (async () => {
      const controller = new AbortController();
      controllers.add(controller);
      try {
        const response = await fetch(`${relayUrl}/v1/audio/speech`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ input: chunks[index] }),
          cache: "no-store",
          signal: controller.signal,
        });
        if (!response.ok) {
          throw new Error(`relay returned HTTP ${response.status}`);
        }
        if (usesNativeAudio) {
          const blob = await response.blob();
          if (expectedSession !== sessionId) {
            return null;
          }
          const url = URL.createObjectURL(blob);
          objectUrls.add(url);
          return { url };
        }

        const bytes = await response.arrayBuffer();
        if (expectedSession !== sessionId) {
          return null;
        }
        try {
          return await audioContext.decodeAudioData(bytes);
        } catch (error) {
          throw new Error("browser could not decode the returned audio", { cause: error });
        }
      } finally {
        controllers.delete(controller);
      }
    })();
    bufferPromises.set(index, promise);
    return promise;
  }

  async function playCurrent(expectedSession) {
    if (expectedSession !== sessionId || stopped || paused) {
      return;
    }
    if (currentIndex >= chunks.length) {
      stopped = true;
      setControls();
      setStatus("Finished.");
      return;
    }

    try {
      setStatus(`Preparing ${currentIndex + 1} of ${chunks.length}...`);
      pendingBuffer = await loadBuffer(currentIndex, expectedSession);
      if (!pendingBuffer || expectedSession !== sessionId || stopped) {
        return;
      }
      if (paused) {
        setStatus(`Paused at ${currentIndex + 1} of ${chunks.length}.`);
        return;
      }

      const chunkEnded = () => {
        if (expectedSession !== sessionId || stopped) {
          return;
        }
        if (activeObjectUrl) {
          URL.revokeObjectURL(activeObjectUrl);
          objectUrls.delete(activeObjectUrl);
          activeObjectUrl = null;
        }
        activeSource = null;
        pendingBuffer = null;
        currentIndex += 1;
        playCurrent(expectedSession);
      };

      if (usesNativeAudio) {
        activeObjectUrl = pendingBuffer.url;
        activeSource = nativeAudio;
        nativeAudio.src = activeObjectUrl;
        nativeAudio.currentTime = 0;
        nativeAudio.addEventListener("ended", chunkEnded, { once: true });
        await nativeAudio.play();
      } else {
        if (audioContext.state !== "running") {
          await audioContext.resume();
        }
        activeSource = audioContext.createBufferSource();
        activeSource.buffer = pendingBuffer;
        activeSource.connect(audioContext.destination);
        activeSource.addEventListener("ended", chunkEnded, { once: true });
        activeSource.start();
      }
      setStatus(`Playing ${currentIndex + 1} of ${chunks.length} from ${playbackScope}.`);
      if (currentIndex + 1 < chunks.length) {
        loadBuffer(currentIndex + 1, expectedSession).catch(() => {});
      }
    } catch (error) {
      if (error.name === "AbortError" || expectedSession !== sessionId) {
        return;
      }
      stopped = true;
      setControls();
      if (error.message.includes("decode the returned audio")) {
        setStatus("The helper returned audio, but the browser could not decode it.");
      } else {
        setStatus("TTS helper unavailable. Start utils/bin/article-tts --browser-server.");
      }
      console.error("Article TTS playback failed:", error);
    }
  }

  async function startOrResume(forcedTarget = null) {
    if (!forcedTarget && paused && !stopped) {
      paused = false;
      if (usesNativeAudio) {
        await nativeAudio.play();
      } else {
        await audioContext.resume();
      }
      setControls({ playing: true });
      if (activeSource) {
        setStatus(`Playing ${currentIndex + 1} of ${chunks.length} from ${playbackScope}.`);
      } else {
        playCurrent(sessionId);
      }
      return;
    }

    stopPlayback(false);
    const target = forcedTarget || queuedReadingTarget || readingTarget();
    queuedReadingTarget = null;
    chunks = makeChunks(target.text);
    if (chunks.length === 0) {
      setStatus("No readable article text was found.");
      return;
    }

    if (!usesNativeAudio) {
      ensureAudioContext();
      await audioContext.resume();
    }
    sessionId += 1;
    currentIndex = 0;
    stopped = false;
    paused = false;
    playbackScope = target.scope;
    bufferPromises = new Map();
    setControls({ playing: true });
    playCurrent(sessionId);
  }

  async function pausePlayback() {
    if (stopped || paused) {
      return;
    }
    paused = true;
    if (usesNativeAudio) {
      nativeAudio.pause();
    } else {
      await audioContext?.suspend();
    }
    setControls({ playing: true, isPaused: true });
    setStatus(`Paused at ${currentIndex + 1} of ${chunks.length}.`);
  }

  function stopPlayback(showStatus = true) {
    sessionId += 1;
    stopped = true;
    paused = false;
    controllers.forEach((controller) => controller.abort());
    controllers.clear();
    if (usesNativeAudio) {
      nativeAudio.pause();
      nativeAudio.removeAttribute("src");
      nativeAudio.load();
      activeSource = null;
    } else if (activeSource) {
      try {
        activeSource.stop();
      } catch (_error) {
        // The source may already have ended.
      }
      activeSource.disconnect();
      activeSource = null;
    }
    objectUrls.forEach((url) => URL.revokeObjectURL(url));
    objectUrls.clear();
    activeObjectUrl = null;
    pendingBuffer = null;
    bufferPromises.clear();
    chunks = [];
    currentIndex = 0;
    if (audioContext) {
      if (showStatus) {
        audioContext.suspend().catch(() => {});
      }
    }
    setControls();
    if (showStatus) {
      setStatus("Stopped. Select text, place the cursor, or play the whole post.");
    }
  }

  article.addEventListener("pointerup", (event) => {
    const selection = window.getSelection();
    const range = currentArticleRange();
    if (range?.collapsed && selection?.isCollapsed) {
      lastArticleCaret = range.cloneRange();
      return;
    }
    if (selection && !selection.isCollapsed) {
      return;
    }

    let pointerRange = null;
    if (document.caretPositionFromPoint) {
      const position = document.caretPositionFromPoint(event.clientX, event.clientY);
      if (position) {
        pointerRange = document.createRange();
        pointerRange.setStart(position.offsetNode, position.offset);
        pointerRange.collapse(true);
      }
    } else if (document.caretRangeFromPoint) {
      pointerRange = document.caretRangeFromPoint(event.clientX, event.clientY);
    }
    const container = pointerRange ? rangeContainer(pointerRange) : null;
    if (container && article.contains(container)) {
      lastArticleCaret = pointerRange.cloneRange();
    }
  });
  playButton.addEventListener("pointerdown", () => {
    queuedReadingTarget = readingTarget();
    primeAudioOutput();
  });
  playButton.addEventListener("click", () => {
    primeAudioOutput();
    startOrResume().catch((error) => {
      setControls();
      setStatus("The browser could not start audio playback.");
      console.error("Article TTS start failed:", error);
    });
  });
  restartButton.addEventListener("pointerdown", () => {
    primeAudioOutput();
  });
  restartButton.addEventListener("click", () => {
    primeAudioOutput();
    startOrResume({ text: wholeArticleText(), scope: "beginning" }).catch((error) => {
      setControls();
      setStatus("The browser could not restart audio playback.");
      console.error("Article TTS restart failed:", error);
    });
  });
  pauseButton.addEventListener("click", () => pausePlayback());
  stopButton.addEventListener("click", () => stopPlayback());
  window.addEventListener("pagehide", () => {
    stopPlayback(false);
    audioContext?.close().catch(() => {});
    audioContext = null;
  });
})();
