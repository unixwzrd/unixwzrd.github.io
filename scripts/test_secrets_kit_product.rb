#!/usr/bin/env ruby
# frozen_string_literal: true

# Verify publication filtering and the opt-in product hub. Optional rendered checks:
# SECKIT_PRODUCTION_SITE=/tmp/production SECKIT_PREVIEW_SITE=/tmp/preview \
# SECKIT_BASELINE_SITE=/tmp/before bundle exec ruby scripts/test_secrets_kit_product.rb
require "bundler/setup"
require "jekyll"
require "minitest/autorun"
require "nokogiri"
require "tmpdir"
require "fileutils"

class SecretsKitProductTest < Minitest::Test
  ROOT = File.expand_path("..", __dir__)
  PREFIX = "/projects/Secrets-Kit/"
  SLUGS = %w[get-started guides remote-sync pricing compare security credential-risks support policies].freeze
  NAV_SLUGS = %w[compare pricing credential-risks guides security support remote-sync get-started].freeze
  TEMP = Dir.mktmpdir("seckit-product-tests-")
  Minitest.after_run { FileUtils.remove_entry(TEMP) }

  def self.read_site(unpublished: false)
    site = Jekyll::Site.new(Jekyll.configuration(
      "config" => File.join(ROOT, "_config.yml"),
      "source" => File.join(ROOT, "html"),
      "destination" => File.join(TEMP, unpublished ? "preview" : "production"),
      "disable_disk_cache" => true,
      "unpublished" => unpublished,
      "quiet" => true,
    ))
    site.read
    site
  end

  PRODUCTION = read_site
  PREVIEW = read_site(unpublished: true)

  def render(template, pages:, page: {}, content: "LEGACY_LANDING_CONTENT", release: PRODUCTION.data.fetch("secrets_kit"))
    site = {
      "url" => "https://unixwzrd.ai", "baseurl" => "", "pages" => pages,
      "posts" => [], "data" => { "github_projects" => { "projects" => [] }, "secrets_kit" => release, "secrets_kit_threats" => PRODUCTION.data.fetch("secrets_kit_threats"), "secrets_kit_competitors" => PRODUCTION.data.fetch("secrets_kit_competitors") },
      "giscus" => { "enabled" => false },
    }
    Liquid::Template.parse(template).render!(
      { "site" => site, "page" => page.merge("comments" => false, "show_support" => false), "content" => content },
      registers: { site: PREVIEW }, strict_filters: true,
    )
  end

  def navigation(pages, page = {}, release: PRODUCTION.data.fetch("secrets_kit"))
    Nokogiri::HTML.fragment(render("{% include secrets-kit/navigation.html %}", pages: pages, page: page, release: release))
  end

  def test_product_pages_publish_together_and_follow_the_declared_state
    pages = PREVIEW.pages.select { |page| page.data["secrets_kit_product"] }
    assert_equal SLUGS.map { |slug| "#{PREFIX}#{slug}/" }.sort, pages.map(&:url).sort
    states = pages.map { |page| page.data["published"] }.uniq
    assert_equal 1, states.length, "Publish or unpublish the product pages together"
    assert_includes [true, false], states.first
    expected = states.first ? pages.map(&:url).sort : []
    assert_equal expected, PRODUCTION.pages.select { |page| page.data["secrets_kit_product"] }.map(&:url).sort
    if states.first
      release = PRODUCTION.data.fetch("secrets_kit")
      assert_match(/\Av\d+\.\d+\.\d+\z/, release["release_tag"].to_s)
      assert_includes [true, false], release["production_release_ready"]
      if release["production_release_ready"]
        assert_equal true, release.fetch("compatibility").fetch("approved_for_202"), "Approve the production support matrix first"
        assert_equal true, release.fetch("service_policies_approved"), "Approve service policies before opening subscriptions"
        refute_empty release.fetch("release_announcement_url"), "Choose the actual release announcement destination"
      end
    end
    root = PRODUCTION.pages.find { |page| page.url == PREFIX }
    assert_equal "secrets-kit", root.data["product_hub"]
  end

  def test_navigation_only_links_loaded_destinations_in_editorial_order
    pages = PREVIEW.pages.select { |page| page.data["secrets_kit_product"] }.map { |page| page.to_liquid.to_h.merge("published" => false) }
    doc = navigation(pages, { "url" => "#{PREFIX}pricing/" })
    assert_equal [PREFIX] + %w[compare pricing credential-risks guides security].map { |slug| "#{PREFIX}#{slug}/" } + [PRODUCTION.data.fetch("secrets_kit").fetch("repository_url")] + %w[support remote-sync].map { |slug| "#{PREFIX}#{slug}/" } + ["#{PREFIX}#updates", "#{PREFIX}get-started/"], doc.css("nav a").map { |link| link["href"] }
    assert_equal ["Pricing"], doc.css('[aria-current="page"]').map(&:text)
    action = PRODUCTION.data.fetch("secrets_kit")["production_release_ready"] ? "Get Started" : "Explore 2.0.2"
    assert_equal ["Overview", "Compare", "Pricing", "Research", "Guides", "Security", "GitHub", action], doc.css('.seckit-nav-links > a').map(&:text)
    assert_equal ["Help", "RSS", "Updates"], doc.css('.seckit-nav-menu a').map(&:text)
    assert_equal "Secrets Kit pages", doc.at_css('.seckit-nav-pages > summary').text
    assert_nil doc.at_css('.seckit-nav-pages')["open"], "Native disclosure remains usable before JavaScript"
    research = navigation(pages, { "url" => "#{PREFIX}credential-risks/" })
    assert_equal ["Research"], research.css('[aria-current="page"]').map(&:text)
    assert_empty research.css('[aria-current="location"]')
    assert_empty doc.css('a[href$="/policies/"]'), "Policies belong in the footer"
    if PRODUCTION.data.fetch("secrets_kit")["production_release_ready"]
      assert_equal "Launch preview", doc.at_css('.seckit-notice strong').text
      assert_empty doc.css('.seckit-notice a')
    else
      assert_includes doc.text, "coming soon"
      assert_equal "#{PREFIX}#updates", doc.at_css('.seckit-notice a')["href"]
    end

    partial = navigation(pages.reject { |page| page["url"] == "#{PREFIX}compare/" })
    assert_empty partial.css('a[href$="/compare/"]')
    policy_index = File.read(File.join(ROOT, "html/Policies.md")).split(/^---\s*$\n?/, 3).last
    refute_includes render(policy_index, pages: []), "#{PREFIX}policies/#client-privacy"
    assert_includes render(policy_index, pages: pages), "#{PREFIX}policies/#client-privacy"
    absent = navigation([])
    assert_equal [PREFIX], absent.css("nav a").map { |link| link["href"] }
    assert_empty absent.css("aside")

    published = pages.map { |page| page.to_h.merge("published" => true) }
    ready = PRODUCTION.data.fetch("secrets_kit").merge("release_tag" => "v9.8.7", "production_release_ready" => true)
    assert_empty navigation(published, {}, release: ready).css("aside")
  end

  def test_one_release_setting_updates_all_product_documentation_links
    pages = PREVIEW.pages.select { |page| page.data["secrets_kit_product"] }.map(&:to_liquid)
    release = PRODUCTION.data.fetch("secrets_kit").merge("release_tag" => "v9.8.7", "production_release_ready" => true,
      "release_announcement_url" => "https://github.com/unixwzrd/Secrets-Kit/releases/tag/v9.8.7")
    SLUGS.each do |slug|
      source = File.read(File.join(ROOT, "html/projects/Secrets-Kit/#{slug}.md")).split(/^---\s*$\n?/, 3).last
      html = render(source, pages: pages, release: release)
      links = html.scan(%r{https://github\.com/unixwzrd/Secrets-Kit/(?:blob|tree|releases/tag)/[^\s<>"\)]+})
      assert_operator links.length, :>, 0, slug unless %w[compare support credential-risks].include?(slug)
      links.each { |url| assert_includes url, "/v9.8.7", "#{slug}: #{url}" }
      refute_match(/v2\.0\.1b\d+|releases\/latest/, html, slug)
    end
    source = File.read(File.join(ROOT, "html/projects/Secrets-Kit/get-started.md")).split(/^---\s*$\n?/, 3).last
    ready = Nokogiri::HTML.fragment(render(source, pages: pages, release: release))
    prompt = ready.at_css("#seckit-setup-prompt")
    assert prompt
    assert_operator prompt.text.length, :<, 250
    assert_equal 1, prompt.text.scan("https://").length
    assert_includes prompt.text, "/tree/v9.8.7/integrations/hermes/"
    pending = Nokogiri::HTML.fragment(render(source, pages: pages, release: release.merge("release_tag" => nil, "production_release_ready" => false)))
    assert pending.at_css("#release-status")
    assert_empty pending.css("textarea, button[data-seckit-copy]")
    refute_includes pending.to_html, "/tree/main/integrations/hermes/"
    refute_includes pending.to_html, "/releases/tag/"
  end

  def test_forthcoming_documents_are_text_and_activate_only_at_the_shared_release
    pages = PREVIEW.pages.select { |page| page.data["secrets_kit_product"] }.map(&:to_liquid)
    template = "{% include secrets-kit/release.html %}{% include secrets-kit/doc-link.html file='SECURITY_MODEL.md' label='security model' %}{% include secrets-kit/doc-link.html file='RSS_CUSTOMER_GUIDE.md#add-another-device' label='device workflow' %}{% include secrets-kit/doc-link.html kind='hermes' label='Hermes integration' %}{% include secrets-kit/doc-link.html kind='license' label='client license' %}"
    pending_release = PRODUCTION.data.fetch("secrets_kit").merge("production_release_ready" => false)
    pending = Nokogiri::HTML.fragment(render(template, pages: pages, release: pending_release))
    assert_empty pending.css("a"), "An unavailable document must not look like a functional link"
    assert_equal 4, pending.css('[data-seckit-unavailable="release-document"]').length
    pending.css("span").each { |span| assert_includes span.text, "forthcoming with 2.0.2" }
    ready = PRODUCTION.data.fetch("secrets_kit").merge("production_release_ready" => true, "release_tag" => "v9.8.7", "release_announcement_url" => "https://example.com/launch")
    links = Nokogiri::HTML.fragment(render(template, pages: pages, release: ready)).css("a").map { |a| a["href"] }
    assert_equal ["blob/v9.8.7/docs/SECURITY_MODEL.md", "blob/v9.8.7/docs/RSS_CUSTOMER_GUIDE.md#add-another-device", "tree/v9.8.7/integrations/hermes/install-secrets-kit-for-hermes", "blob/v9.8.7/LICENSE"].map { |path| "https://github.com/unixwzrd/Secrets-Kit/#{path}" }, links
    updates = render("{% include secrets-kit/release.html %}{{ seckit_updates_url }}", pages: pages, release: ready)
    assert_includes updates, "https://example.com/launch"
  end

  def test_product_hub_requires_opt_in_and_loaded_get_started_page
    template = File.read(File.join(ROOT, "html/_layouts/project.html"))
    pages = PREVIEW.pages.select { |page| page.data["secrets_kit_product"] }.map(&:to_liquid)
    root = { "product_hub" => "secrets-kit", "category" => "Secrets-Kit", "url" => PREFIX }
    [[], pages.reject { |page| page["url"] == "#{PREFIX}get-started/" }].each do |loaded|
      html = render(template, pages: loaded, page: root)
      assert_includes html, "LEGACY_LANDING_CONTENT"
      refute_includes html, "data-seckit-product"
      assert_operator html.index("blog-list-container"), :<, html.index("project-description")
    end
    [root.reject { |key, _value| key == "product_hub" }, root.merge("category" => "Other")].each do |page|
      assert_includes render(template, pages: pages, page: page), "LEGACY_LANDING_CONTENT"
    end
    preview = render(template, pages: pages, page: root)
    refute_includes preview, "LEGACY_LANDING_CONTENT"
    assert_operator preview.index("data-seckit-product"), :<, preview.index('id="updates"')
    hub = Nokogiri::HTML.fragment(preview)
    callout = hub.at_css('.seckit-risk-callout')
    assert callout
    assert_equal "#{PREFIX}credential-risks/#credential-risk", callout.at_css('a')['href']
    research = PRODUCTION.data.fetch("secrets_kit_threats")
    assert_includes callout.text, research.fetch("public_code").fetch("display")
    assert_includes callout.text, research.fetch("public_code").fetch("year").to_s
    assert_includes callout.text, research.fetch("business_impact").fetch("identity_breach").fetch("median_display")
    september = research.fetch("stolen_material").fetch("months").find { |month| month.fetch("period") == "2026-09" }
    assert_includes callout.text, "#{(september.fetch('distinct_pairs') / 1_000_000.0).round(1)} million"
    assert_includes callout.text, "Distinct username/password pairs indexed in #{september.fetch('label')} stealer logs."
    assert_equal "A small secret can carry a large business risk.", callout.at_css('h2').text
    assert_equal 3, callout.css('dt').length
    assert_equal ["Read the research →"], callout.css('a').map(&:text)
    assert callout.at_css('a.home-button'), "Research is a button styled link"
    assert_empty callout.css('.seckit-comparison-footnote')

    refute Nokogiri::HTML.fragment(render(template, pages: pages.reject { |page| page["url"] == "#{PREFIX}credential-risks/" }, page: root)).at_css('.seckit-risk-callout'), "Only advertise an available research page"
    assert_equal %w[seckit-promise seckit-risk-heading seckit-use-cases seckit-offer seckit-next], hub.css('.seckit-product > section').map { |section| section["aria-labelledby"] }
    hero = hub.at_css('.seckit-hero')
    assert_empty hero.css('a, button'), "Explore belongs in the navigation, not the hero"
    assert_empty hero.css('.seckit-source')
    source = hub.at_css('.seckit-offer-cards .seckit-card:first-child .seckit-source')
    assert_includes source.text, "Free, open-source client."
    assert_equal PRODUCTION.data.fetch("secrets_kit").fetch("repository_url"), source.at_css('a')["href"]
    assert_equal %w[seckit-hero-heading seckit-hero-art seckit-hero-intro], hero.at_css('.seckit-hero-grid').element_children.map { |node| node["class"] }
    assert_equal 3, hub.css('.seckit-workflow-steps li').length
    assert_empty hub.css('.seckit-workflow figcaption, .seckit-workflow code')
    assert_empty hub.css('#seckit-how-it-works')
    assert_equal "Blog & Updates", Nokogiri::HTML.fragment(preview).at_css("#updates h2").text
  end

  def test_comparison_matrix_has_accessible_product_columns_and_complete_feature_rows
    source = File.read(File.join(ROOT, "html/projects/Secrets-Kit/compare.md")).split(/^---\s*$\n?/, 3).last
    pages = PREVIEW.pages.select { |page| page.data["secrets_kit_product"] }.map(&:to_liquid)
    doc = Nokogiri::HTML.fragment(render(source, pages: pages))
    matrix = doc.at_css("table.seckit-matrix")
    assert matrix
    assert_equal 6, matrix.css('thead th[scope="col"]').length
    assert_equal ["Secrets Kit", "Bitwarden", "Doppler", "Infisical", "AWS"], matrix.css("thead a").map(&:text)
    assert_equal 5, matrix.css("tbody").length
    matrix.css("tbody").each do |group|
      assert_equal 1, group.css('th[scope="rowgroup"]').length
      group.css("tr:not(.seckit-matrix-group)").each do |row|
        assert_equal 1, row.css('th[scope="row"]').length
        assert_equal 5, row.css("td").length
        assert row.at_css("td:first-of-type.seckit-featured")
      end
    end
    future = matrix.css('td a[href="#seckit-future-enhancements"]')
    assert_equal ["Organization administration", "Organization audit logs", "Automatic secret rotation"], future.map { |link| link.ancestors("tr").first.at_css('th[scope="row"]').text }
    future.each { |link| assert link.ancestors("td").first.at_css('.seckit-cross[aria-label="Not included"]') }
    assert_includes doc.at_css('#seckit-future-enhancements').text, "Planned enhancements, not included in Secrets Kit 2.0.2."
    assert_includes doc.at_css('#seckit-future-enhancements').text, "Scope and release timing may change."
    assert matrix.at_css("caption")
    assert doc.at_css('.seckit-matrix-frame[tabindex="0"][aria-describedby]')
    matrix.css('[role="img"]').each { |mark| refute_empty mark["aria-label"] }
    assert_equal ["✓", "×", "—"].sort, matrix.css('[role="img"]').map(&:text).uniq.sort
  end

  def test_competitor_landscape_has_primary_sources_and_architecture_coverage
    landscape = PREVIEW.data.fetch("secrets_kit_competitors")
    products = landscape.fetch("products")
    assert_operator products.length, :>=, 25
    assert_equal products.length, products.map { |entry| entry.fetch("id") }.uniq.length
    categories = landscape.fetch("categories").map { |entry| entry.fetch("id") }
    fields = %w[status storage custody splitting transfer dependency resilience runtime pricing]
    products.each do |entry|
      assert_includes categories, entry.fetch("category"), entry.fetch("name")
      fields.each { |field| refute_empty entry.fetch(field), "#{entry.fetch('name')}: #{field}" }
      refute_empty entry.fetch("sources"), entry.fetch("name")
      entry.fetch("sources").each { |source| assert_match(%r{\Ahttps://}, source.fetch("url")) }
    end
    assert products.find { |entry| entry["id"] == "envkey" }.fetch("status").include?("shutdown")
    assert products.find { |entry| entry["id"] == "envmanager-oss" }.fetch("status").include?("Experimental")
  end

  def test_comparison_reference_material_is_collapsed_without_removing_sources_or_anchors
    source = File.read(File.join(ROOT, "html/projects/Secrets-Kit/compare.md")).split(/^---\s*$\n?/, 3).last
    converted = PREVIEW.find_converter_instance(Jekyll::Converters::Markdown).convert(render(source, pages: []))
    doc = Nokogiri::HTML.fragment(converted)
    assert_equal 2, doc.css("table.seckit-matrix").length
    doc.css("table.seckit-matrix").each do |table|
      assert_empty table.ancestors("details")
      assert table.at_css("col.seckit-featured-column")
    end
    %w[seckit-workflow-notes seckit-architecture-notes].each do |id|
      section = doc.at_css("div##{id}")
      assert section, id
      assert_empty section.ancestors("details")
      assert_empty section.css("details, summary")
    end
    %w[seckit-product-catalog comparison-sources].each do |id|
      details = doc.at_css("details##{id}")
      assert details, id
      refute details.key?("open"), id
    end
    catalog = doc.at_css("#seckit-product-catalog")
    assert_equal PRODUCTION.data.fetch("secrets_kit_competitors").fetch("products").length, catalog.css("[data-competitor]").length
    %w[seckit-workflow-fit seckit-custody-heading seckit-landscape-heading].each { |id| assert doc.at_css("##{id}") }
    assert doc.at_css('#comparison-sources a[href="https://www.doppler.com/pricing"]')
  end

  def test_ga_announcement_is_publishable_and_separate_from_the_prerelease_article
    basename = "2026-11-07-secrets-kit-2-0-2-general-availability.md"
    announcement = PRODUCTION.posts.docs.find { |post| File.basename(post.path) == basename }
    assert announcement
    assert_equal true, announcement.data["published"]
    refute announcement.data["list_exclude"]
    refute announcement.data["search_exclude"]
    refute_equal false, announcement.data["sitemap"]
    assert_equal "Secrets-Kit 2.0.2 Released — Local Credentials, Free LAN Sync, Optional Remote Secret Sync", announcement.data["title"]
    assert_includes announcement.content, "US$5 per node per month"
    assert_includes announcement.content, "two-node minimum of US$10/month"
    assert_includes announcement.content, "/blob/v2.0.2/docs/INSTALL.md"
    assert_includes announcement.content, "does not require an invitation or access code"
    opening = Nokogiri::HTML.fragment(announcement.content.split("<!--more-->").first)
    download = opening.at_css(".home-actions a.home-button--primary")
    assert_equal "Download Secrets-Kit 2.0.2", download.text
    assert_equal "https://github.com/unixwzrd/Secrets-Kit/releases/download/v2.0.2/install.sh", download["href"]
    assert opening.at_css('.home-actions a[href="/projects/Secrets-Kit/get-started/"]')
    prerelease = PRODUCTION.posts.docs.find { |post| File.basename(post.path) == "2026-10-28-secrets-kit-2-0-2-local-secrets-peer-to-peer-sync.md" }
    assert prerelease
    assert_includes prerelease.data["title"], "Coming Soon"
    assert_includes prerelease.content, "this is a pre-announcement, not general availability"
  end

  def test_current_product_naming_support_routes_and_legacy_anchors
    sources = Dir[File.join(ROOT, "html/_includes/secrets-kit/*.html")] + SLUGS.map { |slug| File.join(ROOT, "html/projects/Secrets-Kit/#{slug}.md") }
    sources.each do |path|
      text = File.read(path)
      refute_match(/Remote Secrets Sync|Remote Sync/, text, path)
      refute_match(/\brelays?\b/i, text.gsub(/\{#[^}]+\}/, ""), path)
    end
    remote = File.read(File.join(ROOT, "html/projects/Secrets-Kit/remote-sync.md"))
    assert_includes remote, "nav_title: RSS"
    assert_includes remote, "{#what-travels-through-the-relay}"
    assert_includes remote, "{#primary-and-secondary-relay-failover}"
    security = File.read(File.join(ROOT, "html/projects/Secrets-Kit/security.md"))
    assert_includes security, "{#what-does-remote-secrets-sync-see}"
    %w[overview support].each do |name|
      text = File.read(File.join(ROOT, "html/_includes/secrets-kit/#{name}.html"))
      assert_includes text, "maintenance contract"
      assert_match(/consulting/i, text)
      assert_includes text, "'/contact/' | relative_url"
      assert_match(/separately.*RSS subscription|RSS subscription.*maintenance contract/, text)
    end
  end

  def test_threat_statistics_keep_sources_periods_and_calculations_explicit
    research = PRODUCTION.data.fetch("secrets_kit_threats")
    sources = research.fetch("sources")
    sources.each_value { |source| assert_match(%r{\Ahttps://}, source.fetch("url")) }
    code = research.fetch("public_code")
    series = code.fetch("annual_series")
    assert_equal series.map { |point| point.fetch("year") }.sort, series.map { |point| point.fetch("year") }
    series.each { |point| assert_operator point.fetch("millions"), :<=, code.fetch("annual_series_max_millions") }
    months = research.fetch("stolen_material").fetch("months")
    assert_equal months.map { |month| month.fetch("period") }.sort, months.map { |month| month.fetch("period") }
    assert_equal months.length, months.map { |month| month.fetch("period") }.uniq.length
    months.each do |month|
      assert sources.key?(month.fetch("source"))
      if month.fetch("status") == "published"
        assert_equal month.fetch("distinct_pairs"), month.fetch("pairs_display").delete(",").to_i
        assert_equal month.fetch("machines"), month.fetch("machines_display").delete(",").to_i
        assert_operator month.fetch("credential_records"), :>=, month.fetch("distinct_pairs")
      else
        assert_equal "unavailable", month.fetch("status")
        assert_nil month.fetch("distinct_pairs"), "Missing months must not become zero observations"
        assert_nil month.fetch("machines")
      end
    end
    abuse = research.fetch("credential_abuse")
    assert_includes 0..100, abuse.fetch("percent")
    assert_equal abuse.fetch("cohort_size"), abuse.fetch("cohort_display").delete(",").to_i
    doc = Nokogiri::HTML.fragment(render("{% include secrets-kit/threat-context.html %}", pages: []))
    assert doc.at_css("#credential-risk")
    %w[seckit-threat-trend-title seckit-loss-trend-title seckit-monthly-trend-title].each do |id|
      caption = doc.at_css("figcaption##{id}")
      assert caption.at_css("h3"), "Chart title must use the shared subsection heading: #{id}"
      assert caption.parent["aria-labelledby"] == id
    end
    assert_equal series.length, doc.at_css("#seckit-threat-trend-title").parent.css(".seckit-threat-bars li").length
    monthly = format("%.1f", code.fetch("approximate_count").to_f / 12 / 1_000_000)
    daily = (code.fetch("approximate_count").to_f / code.fetch("days_in_year")).round(-3).to_s.reverse.gsub(/(\d{3})(?=\d)/, '\\1,').reverse
    assert_includes doc.text, "#{monthly} million detections per month"
    assert_includes doc.text, "#{daily} per day"
    assert_includes doc.text, "not a trend in global theft"
    assert_includes doc.text, "does not mean zero exposure"
    monthly_chart = doc.at_css("#seckit-monthly-trend-title").parent
    assert_equal months.length, monthly_chart.css("li").length
    assert_equal months.count { |month| month["status"] == "published" }, monthly_chart.css(".seckit-threat-track").length
    assert_equal months.count { |month| month["status"] == "unavailable" }, monthly_chart.css(".seckit-threat-unavailable").length
    impact = research.fetch("business_impact")
    cost = impact.fetch("identity_breach")
    assert_equal cost.fetch("median_usd"), cost.fetch("median_display").delete("$, ").to_i
    assert_operator cost.fetch("mean_usd"), :>, cost.fetch("median_usd")
    losses = impact.fetch("bec").fetch("annual_series")
    assert_equal losses.map { |row| row.fetch("year") }.sort, losses.map { |row| row.fetch("year") }
    assert_equal losses.length, doc.at_css("#seckit-loss-trend-title").parent.css("li").length
    yoy = (100.0 * (losses.last.fetch("loss_usd") - losses[-2].fetch("loss_usd")) / losses[-2].fetch("loss_usd")).round(1)
    assert_includes doc.text, "#{yoy}% above #{losses[-2].fetch('year')}"
    example = impact.fetch("staff_time_example")
    assert_equal example.fetch("people") * example.fetch("hours_per_person") * example.fetch("hourly_cost_usd"), example.fetch("cost_display").delete("$, ").to_i
    assert doc.at_css("[data-seckit-cost-planner][hidden]")
    assert doc.at_css("[data-seckit-cost-example]")
    calculator = doc.at_css('section.seckit-cost-planner[aria-labelledby="credential-response-cost"]')
    assert calculator
    assert_equal "Instant response-cost calculator", calculator.at_css("h3").text
    assert_empty calculator.ancestors("details")
    assert_empty calculator.css("summary")
    assert_equal 3, doc.css(".seckit-agent-chain li").length
    assert_includes doc.text, "not a reported criminal campaign"

    sources.each_value { |source| assert doc.css("a").any? { |a| a["href"] == source.fetch("url") }, source.fetch("title") }
  end

  def document(directory, route = PREFIX)
    Nokogiri::HTML(File.read(File.join(directory, route.delete_prefix("/"), "index.html")))
  end

  def normalized_project(doc)
    node = doc.at_css("article.project").dup
    node.traverse { |child| child.remove if child.text? && child.text.strip.empty? }
    node.to_html
  end

  if ENV["SECKIT_PRODUCTION_SITE"]
    def test_rendered_production_matches_declared_publication_state
      directory = ENV.fetch("SECKIT_PRODUCTION_SITE")
      routes = SLUGS.map { |slug| "#{PREFIX}#{slug}/" }
      if PRODUCTION.pages.any? { |page| page.data["secrets_kit_product"] }
        routes.each { |route| assert File.file?(File.join(directory, route, "index.html")), route }
        assert document(directory).at_css("[data-seckit-product]")
        unless PRODUCTION.data.fetch("secrets_kit")["production_release_ready"]
          doc = document(directory, "#{PREFIX}get-started/")
          assert_includes doc.text, "coming soon"
    assert_equal "#{PREFIX}#updates", doc.at_css('.seckit-notice a')["href"]
          assert_empty doc.css("textarea, button[data-seckit-copy]")
          SLUGS.each do |slug|
            page = document(directory, "#{PREFIX}#{slug}/")
            assert_empty page.css('a[href*="github.com/unixwzrd/Secrets-Kit/releases/tag/"], a[href*="github.com/unixwzrd/Secrets-Kit/releases/download/"], a[href*="github.com/unixwzrd/Secrets-Kit/tree/v2.0.2"], a[href*="github.com/unixwzrd/Secrets-Kit/blob/v2.0.2"]'), slug
          end
        end
        return
      end
      routes.each { |route| refute File.exist?(File.join(directory, route, "index.html")), route }
      Dir.glob(File.join(directory, "**/*.{html,xml,json}")).each do |path|
        text = File.read(path)
        routes.each { |route| refute_includes text, route, path }
        refute_includes text, "per enrolled connection / month", path
      end
      doc = document(directory)
      assert_empty doc.css("[data-seckit-product], .seckit-nav, #updates")
      assert_includes doc.at_css(".project-description").text, "coming soon"
    end
  end

  if ENV["SECKIT_PRODUCTION_SITE"] && ENV["SECKIT_PREVIEW_SITE"]
    def test_rendered_preview_has_navigation_prices_prompt_and_unchanged_blog_links
      directory = ENV.fetch("SECKIT_PREVIEW_SITE")
      overview = document(directory)
      assert_equal 1, overview.css("h1").length
      assert overview.at_css("[data-seckit-product]")
      assert_empty overview.css(".post-toc"), "Landing page should not acquire a contents widget"
      assert_operator overview.to_html.index("data-seckit-product"), :<, overview.to_html.index('id="updates"')
      refute_includes overview.at_css(".project-description").text, "Version 1 is available"
      SLUGS.each do |slug|
        route = "#{PREFIX}#{slug}/"
        doc = document(directory, route)
        assert_equal 1, doc.css("h1").length, route
        assert_equal 1, doc.css(".seckit-nav").length, route
        assert_equal 1, doc.css(".post-toc").length, route
        assert_equal 1, doc.css(".seckit-subpage-hero img").length, route
        assert_empty doc.css(".page-header .page-banner-image"), route
        shared = doc.at_css(".seckit-subpage-header")
        assert shared, route
        assert_equal %w[seckit-nav seckit-subpage-hero post-toc], shared.element_children.select { |node| %w[nav div details].include?(node.name) }.map { |node| node["class"] }, route
        refute doc.at_css(".post-toc").key?("open"), route
        assert_equal "/assets/images/projects/Secrets-Kit-Banner.png", doc.at_css(".seckit-subpage-hero img")["src"]
        assert_empty doc.css(".seckit-jumps"), route
        assert_empty doc.at_css('article.seckit-product-page').css('h1[style], h2[style], h3[style], p[style]'), route
        assert_operator doc.to_html.index('class="seckit-nav"'), :<, doc.to_html.index('class="post-toc"'), route
        doc.css(".post-toc a").each { |link| assert doc.at_css("[id='#{link['href'].delete_prefix('#')}']"), link["href"] }
        assert_equal NAV_SLUGS.length + 3, doc.css(".seckit-nav a").length, route
        expected_current = slug == "policies" ? 0 : 1
        assert_equal expected_current, doc.css('.seckit-nav [aria-current]').length, route
        assert doc.at_css(".seckit-nav a[href='#{PREFIX}']"), route
        assert overview.at_css("a[href='#{route}'], a[href^='#{route}#']"), route
      end
      security = document(directory, "#{PREFIX}security/")
      research = document(directory, "#{PREFIX}credential-risks/")
      assert_empty security.css('.seckit-threat-context'), "Practical security answers must lead"
      assert research.at_css('.seckit-threat-context')
      assert_equal "credential-risk", research.at_css(".page-content h2")["id"]
      headings = research.css(".page-content h2[id]").map { |heading| heading["id"] }
      assert_operator headings.index("where-do-secrets-turn-up"), :<, headings.index("agentic-credential-risk")
      assert research.at_css('.post-toc a[href="#credential-response-cost"]')
      assert_equal 1, research.css(".seckit-agentic-risk").length
      assert research.at_css(".seckit-agentic-risk.seckit-risk-callout")
      assert_equal 3, research.css(".seckit-agent-chain li").length
      refute_includes research.text, "Explore the upcoming client"
      callout = security.at_css('[aria-labelledby="agent-workflow-credential-risk"]')
      assert callout
      assert callout.at_css('a[href="/projects/Secrets-Kit/credential-risks/#agentic-credential-risk"]')
      %w[metr_hugging_face hugging_face_incident].each do |key|
        url = PREVIEW.data.fetch("secrets_kit_threats").fetch("sources").fetch(key).fetch("url")
        assert callout.at_css("a[href='#{url}']")
        assert research.at_css(".seckit-agentic-risk .home-actions a[href='#{url}']")
      end
      assert_includes research.text, "historical Codecov incident of 2021"
      assert_includes research.text, "initial account tokens and the later production secrets were different exposures"
      %w[credential-risk business-impact recent-credential-reports agentic-credential-risk].each do |anchor|
        assert security.at_css("##{anchor} a[href='#{PREFIX}credential-risks/##{anchor}']"), anchor
        assert research.at_css("##{anchor}"), anchor
      end
      assert overview.at_css('.seckit-support--compact')
      policy = document(directory, "#{PREFIX}policies/")
      %w[client-privacy remote-secrets-sync-privacy retention-and-deletion service-terms client-license].each { |anchor| assert policy.at_css("##{anchor}") }
      assert_includes policy.text, "in-memory queue"
      assert_includes policy.text, "persistent storage is separate from the in-memory delivery queue"
      assert_includes policy.text, "does not currently configure this persistent mailbox"
      assert_includes policy.text, "swap or paging"
      assert_includes policy.text, "MIT License"
      refute_empty document(directory, "#{PREFIX}security/").css('a[href$="/policies/#remote-secrets-sync-privacy"]')
      pricing = document(directory, "#{PREFIX}pricing/").at_css(".page-content").text
      ["$5", "$10", "$15", "$25", "does not lower the subscription quantity"].each { |text| assert_includes pricing, text }
      started = document(directory, "#{PREFIX}get-started/")
      if PREVIEW.data.fetch("secrets_kit")["production_release_ready"]
        assert started.at_css("#seckit-setup-prompt[readonly]")
        assert started.at_css("button[data-seckit-copy][hidden]")
      else
        assert started.at_css("#release-status")
        assert_empty started.css("textarea, button[data-seckit-copy]")
        assert_empty started.css('a[href$="#release-status"]')
        assert started.at_css("#compatibility")
        assert_includes started.at_css("#compatibility").text, "Supported platforms"
        refute_includes started.text, "Planned platform support"
        assert_includes started.text, "Linux (glibc)"
        assert_includes started.text, "ARM64 (aarch64)"
        refute_includes started.text, "Windows and Linux ARM are not supported"
        assert_includes started.text, "Hermes is optional"
        assert_empty document(directory, "#{PREFIX}pricing/").css("pre code")
        assert_empty document(directory, "#{PREFIX}remote-sync/").css("pre code")
      end
      if PREVIEW.data.fetch("secrets_kit")["production_release_ready"]
        assert started.at_css("#have-your-agent-help")
        assert started.at_css("#install-it-yourself")
      end
      production = document(ENV.fetch("SECKIT_PRODUCTION_SITE"))
      assert_equal production.css(".post-link").map { |link| link["href"] }, overview.css("#updates .post-link").map { |link| link["href"] }
      %w[get-started guides remote-sync pricing compare security support].each do |slug|
        doc = document(directory, "#{PREFIX}#{slug}/")
        assert doc.at_css('.seckit-support a[href="https://github.com/unixwzrd/Secrets-Kit/issues"]'), slug
        assert doc.at_css('.seckit-support a[href="https://github.com/unixwzrd/Secrets-Kit/discussions"]'), slug
      end
      comparison = document(directory, "#{PREFIX}compare/")
      assert_equal PREVIEW.data.fetch("secrets_kit_competitors").fetch("products").length, comparison.css("[data-competitor]").length
      launch_url = "#{PREFIX}2026/11/07/secrets-kit-2-0-2-general-availability/"
      assert_equal launch_url, overview.at_css("#updates .post-link")["href"]
      home = document(directory, "/")
      assert_equal launch_url, home.at_css('[aria-labelledby="home-writing"] .post-link')["href"]
      note = home.at_css(".home-hero > .home-release-announcement")
      assert note
      assert_includes note["class"].split, "home-lead"
      assert_equal "home-actions", note.next_element["class"]
      assert_equal [PREFIX, "https://github.com/unixwzrd/Secrets-Kit/releases/tag/v2.0.2"], note.css("a").map { |link| link["href"] }
      assert_equal 3, home.css(".home-project-card").length
    end
  end

  if ENV["SECKIT_PRODUCTION_SITE"] && ENV["SECKIT_BASELINE_SITE"]
    def test_production_project_is_unchanged_from_baseline
      return if PRODUCTION.pages.any? { |page| page.data["secrets_kit_product"] }

      assert_equal normalized_project(document(ENV.fetch("SECKIT_BASELINE_SITE"))), normalized_project(document(ENV.fetch("SECKIT_PRODUCTION_SITE")))
    end
  end
end
