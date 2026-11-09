// Run with the local preview open in a named Playwright CLI session:
// playwright-cli run-code --filename scripts/check_secrets_kit_product_browser.js
// Blocks external requests; never submits forms or starts installation/billing.
async (page) => {
  const base = new URL(page.url()).origin;
  await page.route("**/*", route => new URL(route.request().url()).origin === base ? route.fallback() : route.abort());
  const slugs = ["", "compare/", "pricing/", "credential-risks/", "guides/", "security/", "get-started/", "remote-sync/", "support/", "policies/"];
  const primary = ["Overview", "Compare", "Pricing", "Research", "Guides", "Security", "GitHub", "Get Started"];
  const results = [];
  for (const scheme of ["light", "dark"]) {
    await page.emulateMedia({ colorScheme: scheme });
    for (const width of [1280, 800, 390]) {
      await page.setViewportSize({ width, height: 1000 });
      await page.goto(base + "/about/");
      const typography = await page.evaluate(() => {
        const reference = document.createElement("article");
        reference.className = "page";
        reference.style.display = "none";
        reference.innerHTML = '<h1 class="page-title">Title</h1><div class="page-content"><h2>Section</h2><h3>Subsection</h3><p>Body</p></div>';
        document.querySelector("main .wrapper").append(reference);
        const result = Object.fromEntries(["h1", "h2", "h3", "p"].map(tag => {
          const style = getComputedStyle(reference.querySelector(tag));
          return [tag, [style.fontFamily, style.fontSize, style.fontWeight, style.lineHeight]];
        }));
        reference.remove();
        return result;
      });
      await page.goto(base + "/projects/Secrets-Kit/");
      const overviewHero = await page.locator(".seckit-hero-art").evaluate(async image => {
        await image.decode();
        const rect = image.getBoundingClientRect();
        const style = getComputedStyle(image);
        return { width: rect.width, height: rect.height, aspectRatio: style.aspectRatio, objectFit: style.objectFit, borderRadius: style.borderRadius };
      });
      for (const slug of slugs) {
        const path = "/projects/Secrets-Kit/" + slug;
        const response = await page.goto(base + path);
        if (response.status() !== 200) throw Error(`HTTP ${response.status()}: ${path}`);
        const nav = page.locator(".seckit-nav");
        if (await nav.count() !== 1) throw Error(`Duplicate/missing navigation: ${path}`);
        if (await page.locator("main h1").count() !== 1) throw Error(`H1 count: ${path}`);
        if (await page.locator(".seckit-jumps").count()) throw Error(`Redundant jump links: ${path}`);
        const mismatches = await page.locator("article.seckit-product-page").evaluate((article, expected) => {
          return [...article.querySelectorAll("h1, h2, h3")].filter(node => {
            if (node.matches(".seckit-hero-heading")) return false;
            const tag = node.tagName.toLowerCase();
            const style = getComputedStyle(node);
            return JSON.stringify([style.fontFamily, style.fontSize, style.fontWeight, style.lineHeight]) !== JSON.stringify(expected[tag]);
          }).map(node => ({ tag: node.tagName, text: node.textContent.slice(0, 80) }));
        }, typography);
        if (mismatches.length) throw Error(`Product typography diverged at ${path}: ${JSON.stringify(mismatches)}`);
        const labels = await nav.locator(".seckit-nav-links > a").allTextContents();
        if (labels.map(label => label.trim()).join("|") !== primary.join("|")) throw Error(`Navigation mismatch: ${path}`);
        if ((await nav.locator(".seckit-nav-menu a").allTextContents()).join("|") !== "Help|RSS|Updates") throw Error(`More mismatch: ${path}`);
        const pages = nav.locator(".seckit-nav-pages");
        if (width < 800) {
          if (await pages.evaluate(node => node.open)) throw Error("Mobile navigation should start collapsed");
          await pages.locator(":scope > summary").click();
          if (!(await pages.evaluate(node => node.open))) throw Error("Mobile navigation did not open");
        }
        const more = nav.locator(".seckit-nav-more");
        await more.locator("summary").focus();
        await page.keyboard.press("Enter");
        if (!(await more.evaluate(node => node.open))) throw Error("More did not open with keyboard");
        await page.keyboard.press("Escape");
        if (await more.evaluate(node => node.open)) throw Error("Escape did not close More");
        const toc = page.locator(".post-toc");
        if (slug) {
          if (await toc.count() !== 1 || await toc.evaluate(node => node.open)) throw Error(`TOC state: ${path}`);
          await page.locator(".seckit-subpage-hero img").evaluate(image => image.decode());
          const header = await page.locator("article.seckit-product-page").evaluate(article => {
            const shared = article.querySelector(".seckit-subpage-header");
            const image = shared.querySelector(".seckit-subpage-hero img");
            const rect = image.getBoundingClientRect();
            const intro = article.querySelector(":scope > .page-content").firstElementChild;
            return {
              order: [...shared.children].filter(node => node.matches("nav, .seckit-subpage-hero, .post-toc")).map(node => node.tagName),
              width: rect.width, height: rect.height,
              aspectRatio: getComputedStyle(image).aspectRatio, objectFit: getComputedStyle(image).objectFit, borderRadius: getComputedStyle(image).borderRadius,
              tocGap: intro.getBoundingClientRect().top - shared.querySelector(".post-toc").getBoundingClientRect().bottom,
              genericBanner: article.querySelectorAll(".page-header .page-banner-image").length,
            };
          });
          if (header.order.join("|") !== "NAV|DIV|DETAILS" || header.genericBanner) throw Error(`Incorrect shared header order: ${path}`);
          if (Math.abs(header.width - overviewHero.width) > 1 || Math.abs(header.height - overviewHero.height) > 1 || header.aspectRatio !== overviewHero.aspectRatio || header.objectFit !== overviewHero.objectFit || header.borderRadius !== overviewHero.borderRadius) throw Error(`Hero differs from Overview: ${path} (${JSON.stringify(header)} versus ${JSON.stringify(overviewHero)})`);
          if (header.tocGap < 0 || header.tocGap > 32) throw Error(`Unexpected gap after TOC: ${path} (${header.tocGap}px)`);
          const badLinks = await toc.locator("a").evaluateAll(links => links.filter(link => !document.getElementById(decodeURIComponent(link.hash.slice(1)))).map(link => link.hash));
          if (badLinks.length) throw Error(`Broken contents links: ${badLinks}`);
          await toc.locator(":scope > summary").focus();
          await page.keyboard.press("Enter");
          if (!(await toc.evaluate(node => node.open))) throw Error("Contents did not open with keyboard");
          await page.keyboard.press("Enter");
        } else {
          if (await toc.count() || await page.locator(".seckit-subpage-hero").count()) throw Error("Overview gained a subpage header");
          await page.locator(".seckit-hero-art").evaluate(image => image.decode());
          if (await page.locator(".seckit-hero-art").count() !== 1) throw Error("Overview hero changed");
          const lead = await page.locator(".seckit-hero").evaluate(node => {
            const heading = node.querySelector(".seckit-hero-heading");
            const image = node.querySelector(".seckit-hero-art");
            const intro = node.querySelector(".seckit-hero-intro");
            return {
              headingSize: parseFloat(getComputedStyle(heading).fontSize),
              textSizes: [...intro.querySelectorAll("p")].map(p => parseFloat(getComputedStyle(p).fontSize)),
              paragraphMargins: [...intro.querySelectorAll("p")].map(p => getComputedStyle(p).margin),
              imageGap: image.getBoundingClientRect().top - heading.getBoundingClientRect().bottom,
              introGap: intro.getBoundingClientRect().top - image.getBoundingClientRect().bottom,
            };
          });
          if (lead.headingSize < parseFloat(typography.h2[1]) || lead.textSizes.some(size => size <= parseFloat(typography.p[1]))) throw Error("Overview lead text is undersized");
          if (lead.imageGap > 24 || lead.introGap > 24 || lead.paragraphMargins.some(margin => margin !== "0px")) throw Error("Overview lead spacing is inconsistent");
          await page.locator(".seckit-hero-heading").evaluate(node => window.scrollTo(0, scrollY + node.getBoundingClientRect().top - 24));
          await page.screenshot({ path: `output/playwright/seckit-overview-lead-${scheme}-${width}.png` });
        }
        if (["compare/", "security/", "credential-risks/"].includes(slug)) {
          if (width < 800) await pages.locator(":scope > summary").click();
          await page.evaluate(() => document.activeElement?.blur());
          await page.evaluate(() => window.scrollTo(0, 0));
          await page.screenshot({ path: `output/playwright/seckit-shared-${slug.replace("/", "")}-${scheme}-${width}.png` });
        }
        if (slug === "credential-risks/") {
          const incident = page.locator(".seckit-agentic-risk");
          const followsExposure = await incident.evaluate(node => {
            const numbers = document.getElementById("credential-risk");
            const exposure = document.getElementById("where-do-secrets-turn-up");
            return Boolean(numbers.compareDocumentPosition(exposure) & Node.DOCUMENT_POSITION_FOLLOWING)
              && Boolean(exposure.compareDocumentPosition(node) & Node.DOCUMENT_POSITION_FOLLOWING);
          });
          if (!followsExposure || await incident.locator(".seckit-agent-chain li").count() !== 3 || await incident.locator(".home-actions a").count() !== 2) throw Error("Research incident presentation regressed");
          const calculator = page.locator("section.seckit-cost-planner");
          if (await calculator.locator("xpath=ancestor::details").count()) throw Error("Calculator is hidden in a disclosure");
          for (const [id, value] of [["seckit-cost-people", "3"], ["seckit-cost-hours", "2"], ["seckit-cost-rate", "50"]]) await calculator.locator(`#${id}`).fill(value);
          if (await calculator.locator("output").innerText() !== "$300") throw Error("Calculator did not update immediately");
          await calculator.locator("#seckit-cost-hours").fill("-1");
          if (!(await calculator.locator("output").innerText()).includes("Enter valid values")) throw Error("Calculator accepted invalid input");
          await calculator.locator("#seckit-cost-hours").fill("2");
          await calculator.evaluate(node => window.scrollTo(0, scrollY + node.getBoundingClientRect().top - 24));
          await page.screenshot({ path: `output/playwright/seckit-calculator-${scheme}-${width}.png` });
          await incident.evaluate(node => window.scrollTo(0, scrollY + node.getBoundingClientRect().top - 24));
          await page.screenshot({ path: `output/playwright/seckit-investigation-${scheme}-${width}.png` });
        }
        if (await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) throw Error(`Page overflow: ${path} at ${width}px`);
        if (slug === "compare/") {
          const disclosures = page.locator("details.seckit-comparison-notes");
          if (await disclosures.count() !== 2 || await disclosures.evaluateAll(nodes => nodes.some(node => node.open))) throw Error("Catalog and sources are not collapsed");
          for (const id of ["seckit-workflow-notes", "seckit-architecture-notes"]) {
            if (!(await page.locator(`#${id}`).evaluate(node => node.tagName !== "DETAILS" && !node.closest("details") && !node.querySelector("summary")))) throw Error(`Guidance is still collapsible: ${id}`);
          }
          for (const frame of await page.locator(".seckit-matrix-frame").all()) {
            const columns = await frame.evaluate(node => {
              const cells = node.querySelectorAll("thead th");
              const positions = () => [...cells].slice(0, 3).map(cell => cell.getBoundingClientRect().x);
              const before = positions();
              node.scrollLeft = 350;
              const after = positions();
              return { before, after, scroll: node.scrollLeft };
            });
            if (columns.scroll < 50 || Math.abs(columns.before[0] - columns.after[0]) > 1) throw Error("Feature labels did not stay pinned");
            const featuredMoved = Math.abs(columns.before[1] - columns.after[1]);
            if (width >= 768 ? featuredMoved > 1 : featuredMoved < 50) throw Error(`Incorrect Secrets Kit column behavior at ${width}px`);
          }
          await page.locator(".seckit-matrix-frame").first().scrollIntoViewIfNeeded();
          await page.screenshot({ path: `output/playwright/seckit-ga-compare-${scheme}-${width}.png` });
          const catalog = page.locator("#seckit-product-catalog");
          await catalog.locator(":scope > summary").click();
          const total = await catalog.locator("[data-competitor]").count();
          if (!total) throw Error("Catalog is empty");
          await catalog.locator("input[type=search]").fill("Bitwarden");
          const matches = await catalog.locator("[data-competitor]:not([hidden])").count();
          if (!matches || matches >= total) throw Error("Catalog filtering failed");
          await catalog.locator("input[type=search]").fill("");
          await page.goto(base + path + "#competitor-bitwarden");
          if (!(await page.locator("#seckit-product-catalog").evaluate(node => node.open))) throw Error("Existing competitor fragment does not reveal the catalog");
          results.push({ scheme, width, catalog: total, navigation: slugs.length, tables: 2 });
        }
      }
    }
  }
  const launch = "/projects/Secrets-Kit/2026/11/09/secrets-kit-2-0-4-general-availability/";
  for (const [path, selector] of [["/", '[aria-labelledby="home-writing"] .post-link'], ["/projects/Secrets-Kit/", "#updates .post-link"]]) {
    await page.goto(base + path);
    if (await page.locator(selector).first().getAttribute("href") !== launch) throw Error(`GA announcement is not first on ${path}`);
  }
  await page.goto(base + "/");
  if (await page.locator(".home-project-card").count() !== 3) throw Error("Homepage cards changed");
  if (!(await page.locator(".home-release-announcement").evaluate(node => node.nextElementSibling.classList.contains("home-actions")))) throw Error("Homepage announcement placement changed");
  const announcementType = await page.locator(".home-release-announcement").evaluate(node => {
    const lead = node.parentElement.querySelector(".home-lead:not(.home-release-announcement)");
    return { announcement: getComputedStyle(node).fontSize, lead: getComputedStyle(lead).fontSize };
  });
  if (announcementType.announcement !== announcementType.lead) throw Error("Homepage announcement does not match lead text size");
  await page.screenshot({ path: "output/playwright/seckit-ga-homepage.png", fullPage: true });
  if ((await page.goto(base + launch)).status() !== 200) throw Error("Launch article unavailable");
  await page.locator(".post-banner-image img").evaluate(image => image.decode());
  const actionGap = await page.locator(".post-content > .home-actions").evaluate(node => node.nextElementSibling.getBoundingClientRect().top - node.getBoundingClientRect().bottom);
  if (actionGap < 20 || actionGap > 32) throw Error(`Article action spacing regressed: ${actionGap}px`);
  if (!(await page.locator(".post-content").innerText()).includes("US$5 per node per month")) throw Error("Launch pricing missing");
  await page.screenshot({ path: "output/playwright/seckit-ga-announcement-preview.png", fullPage: true });
  return { checks: results, typography: "shared site styles", launch, firstInRecentLists: true, externalRequests: "blocked" };
}

