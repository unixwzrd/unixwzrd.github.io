// Run against an isolated site served on the current Playwright page's origin:
// playwright-cli run-code --filename scripts/check_reader_experience_browser.js
// Reads pages and writes only ignored screenshots. Never submits forms/comments.
async (page) => {
  const base = new URL(page.url()).origin;
  const routes = [
    ["home", "/"],
    ["ssh", "/technology/2025/04/08/Remote-Debugging-With-VSCode/"],
    ["memory", "/technology/2026/08/23/memory-is-a-governance-problem-not-just-a-vector-database/"],
    ["monitoring", "/technology/2026/10/11/monitoring-a-static-site-after-deployment/"],
    ["blog", "/blog/"], ["archive", "/blog/all/"],
    ["loggpt", "/projects/LogGPT/"], ["extract-chat", "/projects/extract-chat/"],
    ["search", "/search/"], ["contact", "/contact/"],
    ["case-study", "/projects/LogGPT/2026/10/15/when-codex-turned-to-loggpt/"],
  ];
  const results = [];
  const failures = [];
  let searchChecks = 0;
  let navigationChecks = 0;
  for (const scheme of ["light", "dark"]) {
    await page.emulateMedia({ colorScheme: scheme });
    for (const width of [1280, 390]) {
      await page.setViewportSize({ width, height: 900 });
      for (const [name, path] of routes) {
        const response = await page.goto(base + path, { waitUntil: "load" });
        if (!response || response.status() !== 200) throw new Error(`HTTP failure: ${path}`);
        if (name === "home") {
          for (const image of await page.locator(".home-banner img, .home-project-image img").all()) {
            await image.scrollIntoViewIfNeeded();
            await image.evaluate(image => image.decode());
          }
          const labels = await page.locator(".site-nav .trigger > a.page-link, .site-nav .trigger > .nav-dropdown > .nav-dropdown-trigger-row > a").allTextContents();
          if (labels.join("|") !== "Resources|Projects|Blog|Work With Us|About|Contact|Search") throw new Error(`Navigation order: ${labels}`);
          const mobile = await page.locator('.site-nav label[for="nav-trigger"]').isVisible();
          if (mobile) await page.locator('.site-nav label[for="nav-trigger"]').click();
          for (const menu of ["projects", "blogs", "collaborate"]) {
            const dropdown = page.locator(`.nav-dropdown-${menu}`);
            if (mobile) await dropdown.locator(".nav-dropdown-toggle").click();
            else await dropdown.locator(".nav-dropdown-link").focus();
            if (!(await dropdown.locator(".nav-dropdown-menu").isVisible())) throw new Error(`Dropdown failed: ${menu}`);
            if (mobile) await dropdown.locator(".nav-dropdown-toggle").click();
          }
          if (mobile) await page.locator('.site-nav label[for="nav-trigger"]').click();
          await page.evaluate(() => document.activeElement?.blur());
          await page.locator(".home-hero").hover();
          await page.evaluate(() => window.scrollTo(0, 0));
          navigationChecks++;
        }
        if (name === "search") {
          await page.locator("[data-search-input]").fill("LogGPT");
          await page.locator("[data-search-status]").filter({ hasText: /\d+ results? for/ }).waitFor();
          const firstResult = page.locator(".search-result a").first();
          await firstResult.waitFor();
          const href = await firstResult.getAttribute("href");
          if (new URL(href, base).origin !== base || new URL(page.url()).searchParams.get("q") !== "LogGPT") throw new Error("Search result/query URL failure");
          const target = await page.request.get(new URL(href, base).href);
          if (target.status() !== 200) throw new Error(`Search result HTTP failure: ${href}`);
          searchChecks++;
        }
        for (const summary of await page.locator(".source-code-disclosure summary").all()) {
          await summary.focus();
          await page.keyboard.press("Enter");
        }
        const result = await page.evaluate(() => {
          const canvas = document.createElement("canvas");
          canvas.width = canvas.height = 1;
          const ctx = canvas.getContext("2d", { willReadFrequently: true });
          const rgba = color => {
            ctx.clearRect(0, 0, 1, 1);
            ctx.fillStyle = color;
            ctx.fillRect(0, 0, 1, 1);
            return Array.from(ctx.getImageData(0, 0, 1, 1).data);
          };
          const composite = (top, bottom) => {
            const alpha = top[3] / 255;
            return top.slice(0, 3).map((v, i) => v * alpha + bottom[i] * (1 - alpha));
          };
          const background = el => {
            const chain = [];
            for (let node = el; node; node = node.parentElement) chain.unshift(node);
            return chain.reduce((bg, node) => composite(rgba(getComputedStyle(node).backgroundColor), bg), [255, 255, 255]);
          };
          const luminance = rgb => rgb.map(v => {
            const n = v / 255;
            return n <= 0.04045 ? n / 12.92 : ((n + 0.055) / 1.055) ** 2.4;
          }).reduce((sum, n, i) => sum + n * [0.2126, 0.7152, 0.0722][i], 0);
          const contrast = (a, b) => {
            const values = [luminance(a), luminance(b)].sort((x, y) => y - x);
            return (values[0] + 0.05) / (values[1] + 0.05);
          };
          let checked = 0;
          let controlsChecked = 0;
          const bad = [];
          for (const el of document.querySelectorAll("body *")) {
            if (el.closest('script, style, svg, iframe, [hidden], [aria-hidden="true"]')) continue;
            if (el.disabled || !el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) continue;
            const text = Array.from(el.childNodes).filter(n => n.nodeType === Node.TEXT_NODE).map(n => n.textContent).join("").trim();
            if (!text) continue;
            const style = getComputedStyle(el);
            const bg = background(el);
            const fg = composite(rgba(style.color), bg);
            const ratio = contrast(fg, bg);
            const large = parseFloat(style.fontSize) >= 24 || (parseFloat(style.fontSize) >= 18.666 && parseInt(style.fontWeight, 10) >= 700);
            const target = large ? 3 : 4.5;
            checked++;
            if (ratio < target) bad.push({ tag: el.tagName, class: el.className, text: text.slice(0, 65), color: style.color, bg, ratio: +ratio.toFixed(3), target });
          }
          for (const el of document.querySelectorAll(".contact-field input, .contact-field textarea, .contact-field select, .contact-submit, .search-input, .pagination-size select, .pagination-btn, .source-code-disclosure__actions .button-link, .home-button")) {
            if (el.disabled || !el.checkVisibility()) continue;
            const style = getComputedStyle(el);
            const adjacent = el.matches(".home-button") ? background(el.parentElement) : background(el);
            const ratio = contrast(composite(rgba(style.borderTopColor), adjacent), adjacent);
            controlsChecked++;
            if (ratio < 3) bad.push({ kind: "control-border", tag: el.tagName, class: el.className, ratio: +ratio.toFixed(3), target: 3 });
          }
          return { checked, controlsChecked, bad: bad.slice(0, 15), totalBad: bad.length, overflow: document.documentElement.scrollWidth > innerWidth + 1, background: getComputedStyle(document.body).backgroundColor };
        });
        results.push({ scheme, width, name, checked: result.checked, controlsChecked: result.controlsChecked, background: result.background });
        if (result.totalBad || result.overflow) failures.push({ scheme, width, name, ...result });
        const toc = page.locator(".post-toc");
        if (["ssh", "memory", "monitoring", "case-study"].includes(name)) {
          if (await toc.count() !== 1 || await toc.getAttribute("open") !== null) throw new Error(`TOC initial state: ${name}`);
          await toc.locator("summary").focus();
          await page.keyboard.press("Enter");
          if (await toc.getAttribute("open") === null) throw new Error(`TOC keyboard opening: ${name}`);
          const invalid = await toc.locator("a").evaluateAll(links => links.map(a => a.getAttribute("href")).filter(href => !document.getElementById(decodeURIComponent(href.slice(1)))));
          if (invalid.length) throw new Error(`Missing TOC targets: ${invalid}`);
          const anchor = await toc.locator("a").first().getAttribute("href");
          await toc.locator("a").first().click();
          if (decodeURIComponent(new URL(page.url()).hash) !== anchor) throw new Error(`TOC navigation: ${name}`);
          await toc.locator("summary").focus();
          await page.keyboard.press("Enter");
        } else if (await toc.count()) throw new Error(`Unexpected TOC: ${name}`);
        if (name === "ssh") {
          await page.locator("pre").first().scrollIntoViewIfNeeded();
          await page.screenshot({ path: `output/playwright/reader-after-${scheme}-${width}.png` });
        }
        if (name === "home") {
          if (await page.locator(".home-project-card").count() !== 3 || await page.locator("h1").count() !== 1) throw new Error("Homepage featured-card/title failure");
          if (await page.locator(".home-beta").count() || /\bbeta\b|share testing feedback|help test secrets kit/i.test(await page.locator(".home").innerText())) throw new Error("Homepage exposes beta recruitment");
          const unloaded = await page.locator(".home-project-image img").evaluateAll(images => images.filter(image => !image.complete || image.naturalWidth === 0).map(image => image.src));
          if (unloaded.length) throw new Error(`Homepage images not loaded: ${unloaded}`);
          await page.screenshot({ path: `output/playwright/homepage-${scheme}-${width}.png`, fullPage: true });
        }
        if (["loggpt", "extract-chat"].includes(name)) {
          const intro = page.locator(".project-intro");
          if (await intro.count() !== 1) throw new Error(`Missing project intro: ${name}`);
          const correctOrder = await intro.evaluate(el => {
            const siblings = Array.from(el.parentElement.children);
            return siblings.indexOf(el) < siblings.findIndex(node => node.classList.contains("blog-list-container"));
          });
          if (!correctOrder) throw new Error(`Project intro after history: ${name}`);
          await intro.scrollIntoViewIfNeeded();
          await page.screenshot({ path: `output/playwright/reader-project-${name}-${scheme}-${width}.png` });
        }
      }
    }
  }
  let noJsChecks = 0;
  for (const colorScheme of ["light", "dark"]) {
    const context = await page.context().browser().newContext({ javaScriptEnabled: false, colorScheme, viewport: { width: 390, height: 844 } });
    try {
      const tab = await context.newPage();
      for (const [, path] of routes.filter(([name]) => ["ssh", "memory"].includes(name))) {
        await tab.goto(base + path);
        const toc = tab.locator(".post-toc");
        await toc.locator("summary").focus();
        await tab.keyboard.press("Enter");
        if (await toc.getAttribute("open") === null) throw new Error("No-JS disclosure failed");
        const href = await toc.locator("a").first().getAttribute("href");
        await toc.locator("a").first().click();
        if (decodeURIComponent(new URL(tab.url()).hash) !== href) throw new Error("No-JS fragment navigation failed");
        noJsChecks++;
      }
    } finally {
      await context.close();
    }
  }
  const summary = { scenarios: results.length, noJsChecks, searchChecks, navigationChecks, textChecks: results.reduce((sum, r) => sum + r.checked, 0), controlChecks: results.reduce((sum, r) => sum + r.controlsChecked, 0), failures, results };
  if (failures.length) throw new Error(JSON.stringify(summary));
  return summary;
}
