const searchRoot = document.querySelector("[data-search-page]");
const searchInput = document.querySelector("[data-search-input]");
const searchResults = document.querySelector("[data-search-results]");
const searchStatus = document.querySelector("[data-search-status]");

if (searchRoot && searchInput && searchResults && searchStatus) {
  const url = new URL(window.location.href);
  const initialQuery = url.searchParams.get("q") || "";
  const botPattern = /(bot|crawler|spider|slurp|bingpreview|facebookexternalhit|linkedinbot|embedly|quora link preview|pinterest|whatsapp|slackbot|discordbot|applebot|petalbot|ahrefsbot|semrushbot|mj12bot|googlebot|bingbot)/i;
  const visitorType = botPattern.test(navigator.userAgent || "") ? "bot" : "browser";
  let pagefindModulePromise = null;
  let lastQuery = "";
  let activeSearchToken = 0;

  const normalizeText = (value) => (value || "").replace(/\s+/g, " ").trim();

  const trackEvent = (name, payload) => {
    if (typeof window.gtag !== "function") {
      return;
    }
    window.gtag("event", name, payload);
  };

  const setStatus = (message) => {
    searchStatus.textContent = message;
  };

  const updateQueryString = (query) => {
    const nextUrl = new URL(window.location.href);
    if (query) {
      nextUrl.searchParams.set("q", query);
    } else {
      nextUrl.searchParams.delete("q");
    }
    window.history.replaceState({}, "", nextUrl);
  };

  const loadPagefind = async () => {
    if (!pagefindModulePromise) {
      pagefindModulePromise = import("/pagefind/pagefind.js");
    }
    return pagefindModulePromise;
  };

  const resultCountBucket = (count) => {
    if (count === 0) return "0";
    if (count <= 3) return "1-3";
    if (count <= 10) return "4-10";
    return "11+";
  };

  const renderResults = async (query, results) => {
    const fragment = document.createDocumentFragment();

    for (const result of results) {
      const data = await result.data();
      const item = document.createElement("article");
      const title = normalizeText(data.meta?.title || data.url || result.url);
      const href = data.url || result.url || "#";
      const excerpt = data.excerpt || data.meta?.description || "";
      const resultUrl = document.createElement("a");
      const titleLink = document.createElement("a");
      const heading = document.createElement("h2");
      const pathLabel = normalizeText(href.replace(window.location.origin, ""));
      const excerptNode = document.createElement("p");

      item.className = "search-result";
      item.dataset.resultUrl = href;
      item.dataset.searchTerm = query;

      heading.className = "search-result-title";
      titleLink.href = href;
      titleLink.textContent = title;
      titleLink.setAttribute("data-search-result-link", "");
      heading.appendChild(titleLink);

      resultUrl.className = "search-result-url";
      resultUrl.href = href;
      resultUrl.textContent = pathLabel;
      resultUrl.setAttribute("data-search-result-link", "");

      excerptNode.className = "search-result-excerpt";
      excerptNode.innerHTML = excerpt;

      item.appendChild(heading);
      item.appendChild(resultUrl);
      item.appendChild(excerptNode);
      fragment.appendChild(item);
    }

    searchResults.replaceChildren(fragment);
  };

  const showEmptyState = (message) => {
    const empty = document.createElement("div");
    empty.className = "search-empty";
    empty.textContent = message;
    searchResults.replaceChildren(empty);
  };

  const performSearch = async (query) => {
    const trimmed = normalizeText(query);
    const token = activeSearchToken + 1;
    activeSearchToken = token;
    updateQueryString(trimmed);

    if (!trimmed) {
      lastQuery = "";
      searchResults.replaceChildren();
      setStatus("Search blog posts, projects, and key site pages, or browse tags on the Topics page.");
      return;
    }

    setStatus(`Searching for "${trimmed}"...`);

    try {
      const pagefind = await loadPagefind();
      const search = await pagefind.search(trimmed);
      const results = search?.results || [];

      if (token !== activeSearchToken) {
        return;
      }

      lastQuery = trimmed;
      trackEvent("site_search", {
        search_term: trimmed,
        result_count: results.length,
        result_count_bucket: resultCountBucket(results.length),
        visitor_type: visitorType
      });

      if (!results.length) {
        showEmptyState(`No results found for "${trimmed}".`);
        setStatus(`No results found for "${trimmed}".`);
        trackEvent("site_search_zero_results", {
          search_term: trimmed,
          visitor_type: visitorType
        });
        return;
      }

      await renderResults(trimmed, results);
      setStatus(`${results.length} result${results.length === 1 ? "" : "s"} for "${trimmed}".`);
    } catch (error) {
      console.error("Search failed", error);
      showEmptyState("Search is temporarily unavailable.");
      setStatus("Search is temporarily unavailable.");
    }
  };

  let debounceTimer = null;
  const debouncedSearch = (query) => {
    window.clearTimeout(debounceTimer);
    debounceTimer = window.setTimeout(() => {
      performSearch(query);
    }, 180);
  };

  searchResults.addEventListener("click", (event) => {
    const link = event.target.closest("[data-search-result-link]");
    const card = event.target.closest(".search-result");
    if (!link || !card || !lastQuery) {
      return;
    }

    trackEvent("site_search_result_click", {
      search_term: lastQuery,
      result_url: card.dataset.resultUrl || link.href,
      visitor_type: visitorType
    });
  });

  searchInput.addEventListener("input", (event) => {
    debouncedSearch(event.target.value);
  });

  searchInput.value = initialQuery;
  if (initialQuery) {
    performSearch(initialQuery);
  } else {
    setStatus("Search blog posts, projects, and key site pages, or browse tags on the Topics page.");
  }
}
