// Run with a development preview open in a named Playwright CLI session:
// playwright-cli run-code --filename scripts/check_local_reader_browser.js
// Speech and audio output are mocked: no speech backend is contacted.
async (page) => {
  const base = new URL(page.url()).origin;
  const requests = [];
  await page.route("**/*", async route => {
    const url = new URL(route.request().url());
    if (url.origin === base) return route.continue();
    if (url.pathname === "/v1/audio/speech") {
      requests.push(route.request().postDataJSON().input);
      return route.fulfill({ status: 200, contentType: "audio/wav", body: Buffer.from([0]) });
    }
    return route.abort();
  });
  await page.addInitScript(() => {
    window.readerTestHold = false;
    window.AudioContext = class {
      state = "running";
      destination = {};
      resume() { this.state = "running"; return Promise.resolve(); }
      suspend() { this.state = "suspended"; return Promise.resolve(); }
      createBuffer() { return {}; }
      decodeAudioData() { return Promise.resolve({}); }
      createBufferSource() {
        const events = {};
        return {
          connect() {}, disconnect() {}, stop() {},
          addEventListener(name, callback) { events[name] = callback; },
          start() { if (!window.readerTestHold) setTimeout(() => events.ended?.(), 10); },
        };
      }
    };
  });
  const routes = [
    "/",
    "/technology/2026/10/19/tuning-codex-subagents-for-the-work-they-actually-do/",
    "/projects/Secrets-Kit/",
    "/projects/Secrets-Kit/security/",
    "/projects/Secrets-Kit/pricing/",
    "/projects/Secrets-Kit/2026/10/28/secrets-kit-2-0-2-local-secrets-peer-to-peer-sync/",
    "/hidden/review-2d66666c7be62e65c7daf868/",
  ];
  const results = [];
  for (const path of routes) {
    requests.length = 0;
    const response = await page.goto(base + path);
    if (response.status() !== 200) throw new Error(`HTTP ${response.status()}: ${path}`);
    const player = page.locator(".article-tts-player");
    await player.waitFor();
    if (await player.count() !== 1) throw new Error(`Duplicate player: ${path}`);
    if (await page.locator('script[src*="article-tts-player.js"]').count() !== 1) throw new Error(`Duplicate script: ${path}`);
    await player.locator('[data-action="restart"]').click();
    await player.locator('[role="status"]').filter({ hasText: "Finished." }).waitFor();
    const text = requests.join("\n");
    if (!text.trim()) throw new Error(`No reading text: ${path}`);
    for (const unwanted of ["Support This Work", "Subscribe via RSS", "Join the Discussion", "Join Our Mission"]) {
      if (text.includes(unwanted)) throw new Error(`Page furniture spoken (${unwanted}): ${path}`);
    }
    if (path === "/projects/Secrets-Kit/" && text.includes("Coming Soon: Secrets Kit 2.0.2")) throw new Error("Update listing was spoken");
    results.push({ path, chunks: requests.length, characters: text.length });
  }

  // Selection, caret, controls, and duplicate-initialization checks on a product page.
  await page.goto(base + "/projects/Secrets-Kit/security/");
  await page.locator(".article-tts-player").waitFor();
  const content = page.locator("article.page .page-content > p").first();
  const expected = (await content.textContent()).trim();
  await content.evaluate(node => {
    const range = document.createRange();
    range.selectNodeContents(node);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
  });
  requests.length = 0;
  await page.locator('[data-action="play"]').click();
  await page.locator('.article-tts-player [role="status"]').filter({ hasText: "Finished." }).waitFor();
  if (requests.join(" ") !== expected) throw new Error("Selection did not limit reading");
  await content.evaluate(node => {
    const range = document.createRange();
    range.selectNodeContents(node);
    range.collapse(true);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    window.readerTestHold = true;
  });
  requests.length = 0;
  await page.locator('[data-action="play"]').click();
  await page.locator('.article-tts-player [role="status"]').filter({ hasText: /Playing .* from cursor/ }).waitFor();
  if (!requests[0].startsWith(expected)) throw new Error("Caret reading did not start at the chosen paragraph");
  await page.locator('[data-action="pause"]').click();
  await page.locator('[data-action="play"]').filter({ hasText: "Resume" }).waitFor();
  await page.locator('[data-action="play"]').click();
  await page.locator('[data-action="stop"]').click();
  await page.locator('.article-tts-player [role="status"]').filter({ hasText: /^Stopped\./ }).waitFor();
  await page.addScriptTag({ url: base + "/assets/js/article-tts-player.js" });
  if (await page.locator(".article-tts-player").count() !== 1) throw new Error("Repeated initialization created another player");

  for (const width of [1280, 390]) {
    await page.setViewportSize({ width, height: 900 });
    const fits = await page.locator(".article-tts-player").evaluate(node => {
      const rect = node.getBoundingClientRect();
      return rect.left >= 0 && rect.right <= innerWidth && rect.bottom <= innerHeight;
    });
    if (!fits) throw new Error(`Player exceeds viewport at ${width}px`);
  }
  return { pages: results, selection: "pass", caret: "pass", controls: "pass", duplicateGuard: "pass", viewports: [1280, 390], speech: "mocked" };
}
