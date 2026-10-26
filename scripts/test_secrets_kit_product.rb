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
  SLUGS = %w[get-started guides remote-sync pricing compare security support].freeze
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
      "posts" => [], "data" => { "github_projects" => { "projects" => [] }, "secrets_kit" => release },
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
    end
    root = PRODUCTION.pages.find { |page| page.url == PREFIX }
    assert_equal "secrets-kit", root.data["product_hub"]
  end

  def test_navigation_only_links_loaded_destinations_in_editorial_order
    pages = PREVIEW.pages.select { |page| page.data["secrets_kit_product"] }.map { |page| page.to_liquid.to_h.merge("published" => false) }
    doc = navigation(pages, { "url" => "#{PREFIX}pricing/" })
    assert_equal [PREFIX] + SLUGS.map { |slug| "#{PREFIX}#{slug}/" } + ["#{PREFIX}#updates"], doc.css("nav a").map { |link| link["href"] }
    assert_equal ["Pricing"], doc.css('[aria-current="page"]').map(&:text)
    assert_includes doc.text, "coming soon"

    partial = navigation(pages.reject { |page| page["url"] == "#{PREFIX}compare/" })
    assert_empty partial.css('a[href$="/compare/"]')
    absent = navigation([])
    assert_equal [PREFIX], absent.css("nav a").map { |link| link["href"] }
    assert_empty absent.css("aside")

    published = pages.map { |page| page.to_h.merge("published" => true) }
    ready = PRODUCTION.data.fetch("secrets_kit").merge("release_tag" => "v9.8.7", "production_release_ready" => true)
    assert_empty navigation(published, {}, release: ready).css("aside")
  end

  def test_one_release_setting_updates_all_product_documentation_links
    pages = PREVIEW.pages.select { |page| page.data["secrets_kit_product"] }.map(&:to_liquid)
    release = PRODUCTION.data.fetch("secrets_kit").merge("release_tag" => "v9.8.7", "production_release_ready" => true)
    SLUGS.each do |slug|
      source = File.read(File.join(ROOT, "html/projects/Secrets-Kit/#{slug}.md")).split(/^---\s*$\n?/, 3).last
      html = render(source, pages: pages, release: release)
      links = html.scan(%r{https://github\.com/unixwzrd/Secrets-Kit/(?:blob|tree|releases/tag)/[^\s<>"\)]+})
      assert_operator links.length, :>, 0, slug unless %w[compare support].include?(slug)
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
          assert_empty doc.css("textarea, button[data-seckit-copy]")
          SLUGS.each do |slug|
            page = document(directory, "#{PREFIX}#{slug}/")
            assert_empty page.css('a[href*="github.com/unixwzrd/Secrets-Kit/releases/tag/"], a[href*="github.com/unixwzrd/Secrets-Kit/releases/download/"], a[href*="github.com/unixwzrd/Secrets-Kit/tree/v2.0.2"]'), slug
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
      assert_operator overview.to_html.index("data-seckit-product"), :<, overview.to_html.index('id="updates"')
      refute_includes overview.at_css(".project-description").text, "Version 1 is available"
      SLUGS.each do |slug|
        route = "#{PREFIX}#{slug}/"
        doc = document(directory, route)
        assert_equal 1, doc.css("h1").length, route
        assert_equal SLUGS.length + 2, doc.css(".seckit-nav a").length, route
        assert_equal 1, doc.css('.seckit-nav [aria-current="page"]').length, route
        assert doc.at_css(".seckit-nav a[href='#{PREFIX}']"), route
        assert overview.at_css(".seckit-nav a[href='#{route}']"), route
      end
      pricing = document(directory, "#{PREFIX}pricing/").at_css(".page-content").text
      ["$5", "$10", "$15", "$25", "does not lower the subscription quantity"].each { |text| assert_includes pricing, text }
      started = document(directory, "#{PREFIX}get-started/")
      if PREVIEW.data.fetch("secrets_kit")["production_release_ready"]
        assert started.at_css("#seckit-setup-prompt[readonly]")
        assert started.at_css("button[data-seckit-copy][hidden]")
      else
        assert started.at_css("#release-status")
        assert_empty started.css("textarea, button[data-seckit-copy]")
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
    end
  end

  if ENV["SECKIT_PRODUCTION_SITE"] && ENV["SECKIT_BASELINE_SITE"]
    def test_production_project_is_unchanged_from_baseline
      return if PRODUCTION.pages.any? { |page| page.data["secrets_kit_product"] }

      assert_equal normalized_project(document(ENV.fetch("SECKIT_BASELINE_SITE"))), normalized_project(document(ENV.fetch("SECKIT_PRODUCTION_SITE")))
    end
  end
end
