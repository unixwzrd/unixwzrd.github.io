// Open an isolated build's redirects.json (never a production page), then run:
// playwright-cli run-code --filename scripts/check_short_link_attribution_browser.js
// Add ?baseline=1 to report pre-fix defects without failing the command.
// Every browser request is intercepted; only local build files are fetched.
async (page) => {
  const initial = new URL(page.url());
  if (!["127.0.0.1", "localhost", "[::1]"].includes(initial.hostname)) throw new Error("Use an isolated local build");
  const localBase = new URL(".", initial).href;
  const baseline = initial.searchParams.get("baseline") === "1";
  const mappings = await (await page.request.get(localBase + "redirects.json")).json();
  const entries = Object.entries(mappings);
  const siteOrigin = "https://unixwzrd.ai";
  const selected = [
    entries.find(([path]) => path === "/s/9d7fe8140e/"),
    entries.find(([path, to]) => path.startsWith("/s/") && to.includes("/projects/LogGPT/")),
    entries.find(([path]) => path === "/s/731ce61b8e/"),
    entries.find(([path]) => path === "/blog/series/local-first-agent-operations/"),
    entries.find(([path, to]) => path.startsWith("/projects/LogGPT/") && new URL(to).pathname.toLowerCase() !== path.toLowerCase()),
  ];
  if (selected.some(entry => !entry)) throw new Error("Representative redirect missing");
  const failures = [];
  const results = [];
  let blockedRequests = 0;
  for (const [from, to] of selected) {
    for (const mode of ["plain", "tagged", "suppressed", "noscript"]) {
      const suffix = ["tagged", "noscript"].includes(mode)
        ? "?utm_source=qa&utm_medium=social&utm_campaign=redirect_test&utm_content=a%2Bb&x=one%2Btwo&x=three+four&empty=&gclid=synthetic-test#section"
        : "";
      const context = await page.context().browser().newContext({ serviceWorkers: "block", javaScriptEnabled: mode !== "noscript" });
      const documents = [];
      const errors = [];
      await context.route("**/*", async route => {
        const request = route.request();
        const url = new URL(request.url());
        if (request.isNavigationRequest() && url.origin === "https://referral.example") {
          return route.fulfill({
            contentType: "text/html",
            headers: { "Referrer-Policy": mode === "suppressed" ? "no-referrer" : "strict-origin-when-cross-origin" },
            body: `<a href="${siteOrigin}${from}${suffix.replaceAll("&", "&amp;")}">Visit</a>`,
          });
        }
        if (request.isNavigationRequest() && url.origin === siteOrigin) {
          documents.push({ path: url.pathname + url.search + url.hash, referrer: request.headers()["referer"] || "" });
          const local = await context.request.get(localBase + url.pathname.slice(1) + url.search);
          const html = await local.text();
          if (local.status() !== 200) errors.push(`HTTP ${local.status()}: ${url.pathname}`);
          if (/<meta[^>]+http-equiv=["']refresh["']/i.test(html) && /googletagmanager|gtag\(/.test(html)) errors.push("Redirect executes analytics");
          return route.fulfill({ status: local.status(), contentType: "text/html", body: html });
        }
        blockedRequests++;
        return route.abort();
      });
      try {
        const tab = await context.newPage();
        tab.on("pageerror", error => errors.push(error.message));
        await tab.goto("https://referral.example/from?private=not-forwarded");
        await tab.getByRole("link", { name: "Visit", exact: true }).click();
        await tab.waitForURL(url => url.pathname === new URL(to).pathname, { waitUntil: "domcontentloaded", timeout: 10000 }).catch(error => {
          throw new Error(JSON.stringify({ from, mode, current: tab.url(), documents, errors, error: error.message }));
        });
        await tab.waitForLoadState("domcontentloaded");
        const observed = await tab.evaluate(() => {
          const commands = (window.dataLayer || []).map(command => Array.from(command));
          const configs = commands.filter(command => command[0] === "config");
          const manual = commands.filter(command => command[0] === "event" && command[1] === "page_view");
          return {
            url: location.href, referrer: document.referrer,
            configs: configs.length,
            pageViews: configs.filter(command => command[2]?.send_page_view !== false).length + manual.length,
            commands,
          };
        });
        const expected = new URL(to);
        if (mode === "tagged") {
          expected.search = new URL(siteOrigin + from + suffix).search;
          expected.hash = "#section";
        }
        if (observed.url !== expected.href) errors.push(`Destination mismatch: ${observed.url}`);
        if (documents.length !== 2) errors.push(`Unexpected document hops: ${documents.length}`);
        const expectedViews = mode === "noscript" ? 0 : 1;
        if (observed.configs !== expectedViews || observed.pageViews !== expectedViews) errors.push(`GA initialization/pageviews: ${observed.configs}/${observed.pageViews}`);
        const config = observed.commands.find(command => command[0] === "config");
        if (mode !== "noscript" && config?.[2]?.page_location !== observed.url) errors.push("GA page_location differs from destination URL");
        if (mode === "suppressed" && documents[0].referrer) errors.push("Suppressed source referrer was restored");
        // Observe native referrer behavior, including deliberately suppressed input.
        // No referrer is synthesized or carried in URL parameters/storage.
        results.push({ from, mode, url: observed.url, referrer: observed.referrer, pageViews: observed.pageViews, documents });
        if (errors.length) failures.push({ from, mode, errors });
      } finally {
        await context.close();
      }
    }
  }
  const summary = { baseline, cases: results.length, blockedRequests, productionAnalyticsRequests: 0, failures, results };
  if (failures.length && !baseline) throw new Error(JSON.stringify(summary));
  return summary;
}
