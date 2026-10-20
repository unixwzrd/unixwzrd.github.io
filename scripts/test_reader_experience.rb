#!/usr/bin/env ruby
# frozen_string_literal: true

# Focused source/fixture tests. Does not build, refresh metadata, or contact APIs.
# Run: bundle exec ruby scripts/test_reader_experience.rb
require "bundler/setup"
require "jekyll"
require "minitest/autorun"
require "tmpdir"
require "nokogiri"
require "open3"
require "uri"
require_relative "../html/_plugins/article_toc_filter"

class ReaderExperienceTest < Minitest::Test
  ROOT = File.expand_path("..", __dir__)
  TEMP = Dir.mktmpdir("reader-experience-tests-")
  SITE = Jekyll::Site.new(Jekyll.configuration(
    "config" => File.join(ROOT, "_config.yml"),
    "source" => File.join(ROOT, "html"),
    "destination" => File.join(TEMP, "site"),
    "cache_dir" => File.join(TEMP, "cache"),
    "disable_disk_cache" => true,
    "quiet" => true,
  ))

  def render_include(name, page: {}, parameters: "", site: {}, environment: "production")
    defaults = {
      "url" => "https://unixwzrd.ai", "baseurl" => "", "posts" => [],
      "data" => { "github_projects" => { "projects" => [] } },
      "giscus" => { "enabled" => true, "repo" => "owner/repo", "repo_id" => "repo-identity", "category" => "Announcements", "category_id" => "category-identity", "mapping" => "pathname" },
    }
    Liquid::Template.parse("{% include #{name} #{parameters} %}").render!(
      { "page" => page, "site" => defaults.merge(site), "jekyll" => { "environment" => environment } },
      registers: { site: SITE }, strict_filters: true,
    )
  end

  def post(title, extra = {})
    { "title" => title, "path" => "_posts/#{title}.md", "url" => "/#{title}/", "categories" => ["technology"] }.merge(extra)
  end

  def filtered_titles(parameters, posts, projects = [])
    template = "{% include filter_discovery_posts.html #{parameters} %}{{ discovery_posts | map: 'title' | join: '|' }}"
    Liquid::Template.parse(template).render!(
      { "site" => { "posts" => posts, "data" => { "github_projects" => { "projects" => projects } } } },
      registers: { site: SITE }, strict_filters: true,
    ).strip
  end

  def test_review_layout_is_unindexed_and_has_no_tracking_or_public_page_furniture
    source = File.read(File.join(ROOT, "html/_layouts/review.html")).split(/^---\s*$\n?/, 3).last
    assigns = {
      "page" => { "title" => "Review <example>", "url" => "/hidden/example/", "review_date" => "2026-10-20", "review_note" => "Draft <not accepted>" },
      "site" => { "url" => "https://unixwzrd.ai", "baseurl" => "" },
      "content" => '<h1 id="example">Example</h1><h2 id="one">One</h2><h3 id="child">Child</h3>',
    }
    html = Liquid::Template.parse(source).render!(
      assigns,
      registers: { site: SITE }, strict_filters: true,
    )
    doc = Nokogiri::HTML(html)
    assert_equal "Review <example> — Review copy", doc.at_css("title").text
    assert_equal "noindex, nofollow, noarchive", doc.at_css('meta[name="robots"]')["content"]
    assert_equal "no-referrer", doc.at_css('meta[name="referrer"]')["content"]
    assert_equal "all", doc.at_css("[data-unlisted-review]")["data-pagefind-ignore"]
    assert_equal "Draft <not accepted>", doc.at_css("aside p:last-of-type").text
    assert_equal 1, doc.css("h1").length
    assert_empty doc.css("script, footer, [data-pagefind-body], .support-section, .post-comments")
    assert_equal 1, doc.css("nav").length
    assert_equal %w[#one #child], doc.css(".post-toc a").map { |link| link["href"] }
    assert_equal "On this page", doc.at_css(".post-toc summary").text
    refute doc.at_css(".post-toc").key?("open")
    assert_includes doc.at_css(".post-content").previous_element["class"], "post-toc"

    assigns["page"]["toc"] = false
    without_toc = Liquid::Template.parse(source).render!(assigns, registers: { site: SITE }, strict_filters: true)
    assert_empty Nokogiri::HTML(without_toc).css(".post-toc")
    assigns["page"].delete("toc")
    assigns["content"] = "<p>No section headings.</p>"
    without_headings = Liquid::Template.parse(source).render!(assigns, registers: { site: SITE }, strict_filters: true)
    assert_empty Nokogiri::HTML(without_headings).css(".post-toc")
  end

  def test_toc_uses_existing_ids_and_nests_h3_without_mutating_content
    html = '<h2 id="one">One &amp; <code>two</code></h2><h3 id="child">Child</h3><h2 id="last">Last</h2>'
    original = html.dup
    result = Object.new.extend(Jekyll::ArticleTocFilter).article_toc(html)
    doc = Nokogiri::HTML.fragment(result)
    assert_equal original, html
    assert_equal %w[#one #child #last], doc.css("a").map { |a| a["href"] }
    assert_equal "One & two", doc.at_css("a").text
    assert_equal 2, doc.css("nav > ul > li").length
    assert_equal 1, doc.css("nav > ul > li > ul > li").length
    assert_equal "all", doc.at_css("details")["data-pagefind-ignore"]
    refute doc.at_css("details").key?("open")
  end

  def test_toc_defaults_cover_regular_and_project_posts_and_respect_opt_out
    { "posts" => "_posts/technology/2026-10-18-example.md", "project_posts" => "_project_posts/2026-10-18-example.md" }.each do |collection, path|
      document = Jekyll::Document.new(File.join(SITE.source, path), site: SITE, collection: SITE.collections.fetch(collection))
      document.content = '<h2 id="example">Example</h2>'
      assert_equal true, document.data["toc"], path
      Jekyll::Hooks.trigger(:documents, :post_convert, document)
      assert_includes document.data["article_toc"], 'href="#example"'
      document.data["toc"] = false
      Jekyll::Hooks.trigger(:documents, :post_convert, document)
      assert_nil document.data["article_toc"]
      document.data["toc"] = true
      document.content = "<p>A short announcement without headings.</p>"
      Jekyll::Hooks.trigger(:documents, :post_convert, document)
      assert_equal "", document.data["article_toc"]
    end
    assert_nil SITE.frontmatter_defaults.find("projects/LogGPT.md", :pages, "toc")
  end

  def test_homepage_selections_are_unique_public_projects_with_landing_pages
    selections = YAML.safe_load(File.read(File.join(ROOT, "html/_data/homepage.yml")))
    catalog = YAML.safe_load(File.read(File.join(ROOT, "html/_data/github_projects.yml"))).fetch("projects")
    names = selections.values.flatten.map { |item| item.fetch("name") }
    assert_equal names.uniq, names
    names.each do |name|
      project = catalog.find { |item| item["name"] == name }
      refute_nil project, name
      assert_equal "public", project["visibility"], name
      assert_match %r{\A/projects/[^/]+/\z}, project["page_url"], name
    end
  end

  def test_secrets_kit_catalog_status_matches_its_persistent_override
    catalog = YAML.safe_load(File.read(File.join(ROOT, "html/_data/github_projects.yml"))).fetch("projects")
    sources = YAML.safe_load(File.read(File.join(ROOT, "html/_data/repos.yml"))).fetch("repositories")
    actual = catalog.find { |project| project["name"] == "Secrets-Kit" }.fetch("description")
    override = sources.find { |project| project["name"] == "Secrets-Kit" }.fetch("overrides").fetch("description")
    assert_equal override, actual
    assert_includes actual, "Version 1 is available"
    assert_includes actual, "version 2 is in limited-access beta"
    refute_match(/public beta/i, actual)
  end

  def test_navigation_uses_configured_order_labels_and_existing_catalog_filters
    paths = SITE.config.fetch("header_pages")
    settings = SITE.config.fetch("header_navigation").transform_values(&:dup)
    pages = paths.map { |path| { "path" => path, "url" => "/#{path.delete_suffix('.md')}/", "title" => "Default #{path}", "menu_item" => path.delete_suffix('.md') } }
    data = {
      "github_projects" => { "projects" => [{ "title" => "Visible", "page_url" => "/projects/Visible/", "visibility" => "public" }, { "title" => "Private", "page_url" => "/projects/Private/", "visibility" => "private" }, { "title" => "Hidden", "page_url" => "/projects/Hidden/", "visibility" => "none" }] },
      "blog_sections" => { "sections" => [{ "title" => "Technology", "url" => "/blog/technology/", "visible" => true }, { "title" => "General", "url" => "/blog/general/", "visible" => false }] },
    }
    site = { "header_pages" => paths, "header_navigation" => settings, "pages" => pages, "data" => data }
    links = ".trigger > a.page-link, .trigger > .nav-dropdown > .nav-dropdown-trigger-row > a"
    doc = Nokogiri::HTML.fragment(render_include("navigation.html", site: site))
    assert_equal paths.map { |path| settings.fetch(path).fetch("label") }, doc.css(links).map(&:text)
    assert_equal ["All Projects", "Visible", "Private"], doc.css(".nav-dropdown-projects .nav-dropdown-item").map(&:text)
    assert_equal ["Blog Home", "All Posts", "Technology", "Topics"], doc.css(".nav-dropdown-blogs .nav-dropdown-item").map(&:text)
    assert_equal ["Professional Services", "Community Collaboration"], doc.css(".nav-dropdown-collaborate .nav-dropdown-item").map(&:text)
    ids = doc.css("[id]").map { |node| node["id"] }
    assert_equal ids.uniq, ids
    settings.fetch(paths.last)["label"] = "Find & read"
    reversed = Nokogiri::HTML.fragment(render_include("navigation.html", site: site.merge("header_pages" => paths.reverse)))
    assert_equal "Find & read", reversed.css(links).first.text
    assert_equal paths.reverse.map { |path| settings.fetch(path).fetch("label") }, reversed.css(links).map(&:text)
    (paths + SITE.config.fetch("footer_pages")).each { |path| assert File.file?(File.join(SITE.source, path)), path }
  end

  def test_toc_excludes_unanchored_headings_and_embedded_furniture
    html = '<h2>No ID</h2><details><h2 id="hidden">Hidden</h2></details><blockquote><h2 id="quote">Quote</h2></blockquote><h3 id="standalone">Standalone</h3>'
    doc = Nokogiri::HTML.fragment(Object.new.extend(Jekyll::ArticleTocFilter).article_toc(html))
    assert_equal ["#standalone"], doc.css("a").map { |a| a["href"] }
    assert_equal "", Object.new.extend(Jekyll::ArticleTocFilter).article_toc('<p>No headings</p>')
    hostile = '<h2 id="&quot; onclick=&quot;bad">&lt;script&gt; &amp; text</h2>'
    safe = Nokogiri::HTML.fragment(Object.new.extend(Jekyll::ArticleTocFilter).article_toc(hostile))
    refute safe.at_css("a").key?("onclick")
    assert_empty safe.css("script")
  end

  def test_layout_safely_omits_unavailable_prepared_toc_under_strict_filters
    layout = File.read(File.join(ROOT, "html/_layouts/post.html"))
    slot = layout[/\{% if page.toc == true %\}.*?\{% endif %\}/m]
    refute_nil slot
    template = Liquid::Template.parse(slot)
    assert_equal "", template.render!({ "page" => { "toc" => true } }, strict_filters: true)
    prepared = '<details class="post-toc">Prepared</details>'
    assert_equal prepared, template.render!({ "page" => { "toc" => true, "article_toc" => prepared } }, strict_filters: true)
    assert_equal "", template.render!({ "page" => { "toc" => false, "article_toc" => prepared } }, strict_filters: true)
  end

  def test_series_listing_spans_series_but_preserves_exclusions
    posts = [post("local", "series" => "Local First"), post("jekyll", "series" => "Beyond Static"), post("standalone"), post("empty", "series" => " "), post("draft", "series" => "Local First", "draft" => true), post("unpublished", "series" => "Beyond Static", "published" => false), post("hidden", "series" => "Beyond Static", "list_exclude" => true), post("social-posts", "series" => "Beyond Static"), post("project", "series" => "Beyond Static", "category" => "Invisible")]
    assert_equal "local|jekyll", filtered_titles("series_only=true", posts, [{ "name" => "Invisible", "visibility" => "none" }])
    assert_equal "jekyll", filtered_titles('series="Beyond Static"', posts.first(3))
    assert_equal "standalone|empty", filtered_titles('section="technology" exclude_series=true', posts.first(4))
  end

  def test_hands_on_allows_series_companions
    posts = [post("companion", "series" => "Beyond Static", "categories" => ["hands-on"]), post("standalone", "categories" => ["hands-on"]), post("tech")]
    assert_equal "companion|standalone", filtered_titles('section="hands-on"', posts)
    config = YAML.safe_load(File.read(File.join(ROOT, "html/_data/blog_sections.yml")))
    sections = config.fetch("sections")
    assert_equal true, sections.find { |s| s["id"] == "series" }["series_only"]
    refute sections.find { |s| s["id"] == "hands-on" }["exclude_series"]
    assert sections.find { |s| s["id"] == "technology" }["exclude_series"]
  end

  def test_engagement_order_prompt_and_mapping
    doc = Nokogiri::HTML.fragment(render_include("engagement.html", page: { "discussion_prompt" => "A **specific** question?" }))
    elements = doc.children.select(&:element?)
    assert_equal ["section", "p", "hr", "section"], elements.map(&:name)
    assert_equal 1, doc.css(".support-section").length
    assert_equal 1, doc.css(".post-comments strong").length
    assert_includes doc.at_css(".post-comments").text, "Comments for this post live in GitHub Discussions."
    assert_equal "pathname", doc.at_css('script[src="https://giscus.app/client.js"]')["data-mapping"]
    assert_equal "owner/repo", doc.at_css("script")["data-repo"]
    assert_equal "repo-identity", doc.at_css("script")["data-repo-id"]
    assert_equal "Announcements", doc.at_css("script")["data-category"]
    assert_equal "category-identity", doc.at_css("script")["data-category-id"]
    assert_equal "preferred_color_scheme", doc.at_css("script")["data-theme"]
    assert_equal "https://unixwzrd.ai/feed.xml", doc.at_css(".feed-subscribe a")["href"]
  end

  def test_engagement_disable_flags_and_fallback
    doc = Nokogiri::HTML.fragment(render_include("engagement.html"))
    assert_includes doc.at_css(".post-comments").text, "Comments for this post live in GitHub Discussions."
    no_comments = Nokogiri::HTML.fragment(render_include("engagement.html", page: { "comments" => false, "discussion_prompt" => "Hidden prompt" }))
    assert_empty no_comments.css(".post-comments, .giscus, script")
    refute_includes no_comments.text, "Hidden prompt"
    no_support = Nokogiri::HTML.fragment(render_include("engagement.html", page: { "show_support" => false }))
    assert_empty no_support.css(".support-section, hr")
    neither = Nokogiri::HTML.fragment(render_include("engagement.html", page: { "comments" => false, "show_support" => false }))
    assert_equal ["p"], neither.children.select(&:element?).map(&:name)
    disabled = Nokogiri::HTML.fragment(render_include("engagement.html", site: { "giscus" => { "enabled" => false } }))
    assert_empty disabled.css(".post-comments, .giscus, script")
  end

  def test_disqus_fallback_keeps_production_and_comment_guards
    settings = { "giscus" => { "enabled" => false }, "disqus" => { "shortname" => "example-only" } }
    page = { "discussion_prompt" => "A specific question?" }
    production = Nokogiri::HTML.fragment(render_include("engagement.html", page: page, site: settings))
    assert production.at_css("#disqus_thread")
    assert_includes production.text, "A specific question?"
    development = render_include("engagement.html", page: page, site: settings, environment: "development")
    refute_includes development, "disqus_thread"
    refute_includes development, "A specific question?"
    disabled = render_include("engagement.html", page: page.merge("comments" => false), site: settings)
    refute_includes disabled, "disqus_thread"
    refute_includes disabled, "A specific question?"
  end

  def test_github_buttons_require_a_public_project_and_nonempty_repository
    [{ "visibility" => "public", "repo_url" => "https://github.com/example/project", "expected" => 1 },
     { "visibility" => "private", "repo_url" => "https://github.com/example/project", "expected" => 0 },
     { "visibility" => "none", "repo_url" => "https://github.com/example/project", "expected" => 0 },
     { "visibility" => "public", "expected" => 0 },
     { "visibility" => "public", "repo_url" => "  ", "expected" => 0 }].each do |settings|
      project = { "name" => "Example", "title" => "Example", "description" => "A project", "image_url" => "/example.png" }.merge(settings)
      site = { "data" => { "github_projects" => { "projects" => [project] } } }
      listing = render_include("projects_list.html", parameters: "visibility=page.visibility", page: project, site: site)
      layout = Liquid::Template.parse(File.read(File.join(ROOT, "html/_layouts/project.html"))).render!(
        { "site" => site, "page" => { "category" => "Example", "comments" => false, "show_support" => false }, "jekyll" => { "environment" => "production" } },
        registers: { site: SITE }, strict_filters: true,
      )
      [listing, layout].each do |html|
        links = Nokogiri::HTML.fragment(html).css("a.github-link")
        assert_equal settings["expected"], links.length, settings.inspect
        links.each { |link| assert_equal project["repo_url"], link["href"] }
      end
    end
  end

  def test_permalink_checker_excludes_asset_labs_but_not_real_pages
    Dir.mktmpdir("permalink-check-", TEMP) do |directory|
      FileUtils.mkdir_p(File.join(directory, "html/assets/example-lab/site"))
      File.write(File.join(directory, "html/assets/example-lab/site/index.md"), "---\nlayout: page\n---\nExample fixture\n")
      command = [RbConfig.ruby, File.join(ROOT, "utils/bin/checks/check_permalinks.rb")]
      output, error, status = Open3.capture3(*command, chdir: directory)
      assert status.success?, output + error
      page = File.join(directory, "html/about.md")
      File.write(page, "---\nlayout: page\n---\nReal page\n")
      output, error, status = Open3.capture3(*command, chdir: directory)
      refute status.success?, output + error
      assert_includes output, "about.md"
      assert_includes output, "Missing permalink"
      refute_includes output, "example-lab"
      File.write(page, "---\nlayout: page\npermalink: /about/\n---\nReal page\n")
      output, error, status = Open3.capture3(*command, chdir: directory)
      assert status.success?, output + error
    end
  end
end

# Optional integration checks against an already-built site. No build is run.
# READER_SITE=/tmp/site READER_BASELINE=/tmp/head-site bundle exec ruby scripts/test_reader_experience.rb
if ENV["READER_SITE"]
  class RenderedReaderExperienceTest < Minitest::Test
    ROOT = File.expand_path(ENV.fetch("READER_SITE"))
    PILOTS = %w[
      technology/2025/04/08/Remote-Debugging-With-VSCode
      technology/2026/08/23/memory-is-a-governance-problem-not-just-a-vector-database
    ].freeze

    def document(path)
      Nokogiri::HTML(File.read(File.join(ROOT, path, "index.html")))
    end

    def test_unlisted_reviews_have_no_inbound_listing_links_or_tracking
      files = Dir.glob("#{ROOT}/**/*.html")
      reviews = files.select { |path| File.read(path).include?("data-unlisted-review") }
      reviews.each do |path|
        doc = Nokogiri::HTML(File.read(path))
        url = URI.parse(doc.at_css('link[rel="canonical"]')["href"]).path
        assert_includes doc.at_css('meta[name="robots"]')["content"], "noindex"
        assert_equal "no-referrer", doc.at_css('meta[name="referrer"]')["content"]
        assert_empty doc.css("script, [data-pagefind-body], .support-section, .post-comments")
        headings = doc.css(".post-content h2[id], .post-content h3[id]")
        if headings.any?
          assert_equal 1, doc.css(".post-toc").length
          assert_equal headings.map { |heading| "##{heading['id']}" }, doc.css(".post-toc a").map { |link| link["href"] }
          assert_includes doc.at_css(".post-content").previous_element["class"], "post-toc"
        end
        doc.css('a[href^="#"]').each do |link|
          fragment = link["href"].delete_prefix("#")
          assert doc.css("[id]").any? { |node| node["id"] == fragment }, link["href"]
        end
        files.reject { |other| other == path }.each do |other|
          refute_includes File.read(other), url, "unlisted review linked from #{other}"
        end
        %w[sitemap.xml feed.xml redirects.json].each do |name|
          refute_includes File.read(File.join(ROOT, name)), url, name
        end
      end
    end

    def test_toc_pilots_and_existing_fragments
      PILOTS.each do |path|
        doc = document(path)
        assert_equal 1, doc.css(".post-toc").length
        doc.css(".post-toc a").each { |a| assert doc.at_css(".post-content").css("[id]").any? { |h| "##{h['id']}" == a["href"] }, a["href"] }
        if ENV["READER_BASELINE"]
          original = Nokogiri::HTML(File.read(File.join(ENV.fetch("READER_BASELINE"), path, "index.html")))
          assert_equal original.css(".post-content h2, .post-content h3").map { |h| h["id"] }, doc.css(".post-content h2, .post-content h3").map { |h| h["id"] }
          assert_equal original.at_css('link[rel="canonical"]')["href"], doc.at_css('link[rel="canonical"]')["href"]
        end
      end
      assert_equal 1, document("projects/LogGPT/2026/10/15/when-codex-turned-to-loggpt").css(".post-toc").length
    end

    def test_all_rendered_blog_posts_have_contents_when_headings_exist
      source_site = Jekyll::Site.new(ReaderExperienceTest::SITE.config)
      source_site.read
      ProjectPostPermalink.apply_to_site!(source_site)
      opt_outs = source_site.collections.values.flat_map(&:docs).select { |post| post.data["toc"] == false }.map { |post| post.destination(ROOT) }
      posts = 0
      with_contents = 0
      Dir.glob("#{ROOT}/**/*.html").each do |path|
        doc = Nokogiri::HTML(File.read(path))
        next unless doc.at_css("article.post .post-content")

        posts += 1
        headings = doc.css(".post-content h2[id], .post-content h3[id]").reject do |heading|
          heading.ancestors.any? { |node| %w[details blockquote nav figure].include?(node.name) || %w[series-context series-navigation].include?(node["class"]) }
        end
        toc = doc.css(".post-toc")
        hidden = headings.empty? || opt_outs.include?(path)
        assert_equal hidden ? 0 : 1, toc.length, path
        next if hidden

        with_contents += 1
        assert_equal headings.map { |heading| "##{heading['id']}" }, toc.css("a").map { |a| a["href"] }, path
        refute toc.first.key?("open"), path
      end
      assert_operator posts, :>, 20
      assert_operator with_contents, :>, 10
    end

    def test_project_intro_is_only_in_opted_in_projects_and_precedes_history
      projects = Dir.glob("#{ROOT}/projects/*/index.html").select { |path| File.read(path).include?('class="project-intro"') }
      assert_equal %w[LogGPT code-analytics extract-chat localops-ui-kit], projects.map { |p| File.basename(File.dirname(p)) }.sort
      projects.each do |path|
        doc = Nokogiri::HTML(File.read(path))
        order = doc.at_css(".project-content").element_children.map { |node| node["class"] }
        assert_operator order.index("project-intro"), :<, order.index("blog-list-container")
        assert_operator order.index("blog-list-container"), :<, order.index("project-description")
      end
    end

    def test_homepage_uses_editorial_order_without_beta_recruitment
      doc = document("")
      configuration = YAML.safe_load(File.read(File.join(ReaderExperienceTest::ROOT, "html/_data/homepage.yml")))
      assert_equal configuration.fetch("featured_projects").map { |project| project.fetch("name") }, doc.css("[data-home-project]").map { |card| card["data-home-project"] }
      assert_equal 1, doc.css("h1").length
      assert_equal 1, doc.css(".site-header").length
      assert_equal 1, doc.css(".site-footer").length
      assert_equal "/assets/images/default-og-image.png", doc.at_css(".home-banner img")["src"]
      assert_equal "1536", doc.at_css(".home-banner img")["width"]
      assert_equal "512", doc.at_css(".home-banner img")["height"]
      assert_equal "home-hero", doc.at_css(".home-banner").next_element["class"]
      assert_empty doc.css(".home .content-footer")
      assert_equal "https://unixwzrd.ai/", doc.at_css('link[rel="canonical"]')["href"]
      assert_empty doc.css(".home-beta")
      refute_match(/\bbeta\b|share testing feedback|help test secrets kit/i, doc.at_css(".home").text)
      assert_empty doc.css('.home a[href*="#availability"]')
      assert_equal "Explore Secrets Kit →", doc.at_css('[data-home-project="Secrets-Kit"] .home-card-action').text
      assert_equal 4, doc.css("#home-writing + p + .post-list > li").length
      %w[venvutil TorchDevice Case-Analytics PA-Awareness-1].each do |name|
        refute_includes doc.css("[data-home-project]").map { |card| card["data-home-project"] }, name
      end
      assert doc.at_css('a[href="/projects/Case-Analytics/"]')
      assert doc.at_css('a[href="/projects/PA-Awareness-1/"]')
    end

    def test_rendered_navigation_and_secondary_faq_routes
      config = ReaderExperienceTest::SITE.config
      expected = config.fetch("header_pages").map { |path| config.fetch("header_navigation").fetch(path).fetch("label") }
      selector = ".site-nav .trigger > a.page-link, .site-nav .trigger > .nav-dropdown > .nav-dropdown-trigger-row > a"
      Dir.glob("#{ROOT}/**/*.html").each do |path|
        doc = Nokogiri::HTML(File.read(path))
        next unless doc.at_css(".site-header")

        assert_equal expected, doc.css(selector).map(&:text), path
        assert_equal ["/faq/"], doc.css(".footer-navigation a").map { |a| a["href"] }, path
      end
      %w[about collaborate/professionals].each do |path|
        assert document(path).at_css('.post-content a[href="/faq/"], .page-content a[href="/faq/"]'), path
      end
    end

    def test_secrets_kit_distinguishes_available_v1_and_restricted_v2
      body = document("projects/Secrets-Kit").at_css(".project-description").text
      assert_includes body, "Version 1 is available"
      assert_includes body, "Version 2 is in limited-access beta"
      assert_includes body, "access restricted to authorized testers"
      assert_includes body, "Windows compatibility has not yet been tested"
      refute_match(/public beta|no stable production release yet/i, body)
      refute_match(/\bbeta\b/i, document("").at_css(".home").text)
    end

    def test_no_duplicate_support_and_discussion_precedes_support
      Dir.glob("#{ROOT}/**/*.html").each do |path|
        doc = Nokogiri::HTML(File.read(path))
        assert_operator doc.css(".support-section").length, :<=, 1, path
        comments = doc.at_css(".post-comments")
        support = doc.at_css(".support-section")
        next unless comments && support

        siblings = comments.parent.element_children
        assert_operator siblings.index(comments), :<, siblings.index(support), path
        rss = siblings.find { |node| node["class"] == "feed-subscribe" }
        assert rss, path
        assert_operator siblings.index(comments), :<, siblings.index(rss), path
        assert_operator siblings.index(rss), :<, siblings.index(support), path
      end
    end

    def test_stylesheet_is_compiled_with_one_custom_pass
      css = File.read(File.join(ROOT, "assets/css/style.css"))
      assert_includes css, "--site-code-surface: #f6f8fa"
      assert_includes css, "--site-code-surface: #0d1117"
      assert_equal 1, css.scan(/^\.post-toc summary \{/).length
      refute File.exist?(File.join(ROOT, "assets/css/style.scss"))
    end

    def test_legacy_companion_fragments_are_preserved_alongside_current_headings
      {
        "hands-on/2026/08/19/hands-on-build-an-idempotent-intake-manifest" => {
          "start-with-the-contract" => "step-1-define-the-manifest-contract",
          "run-a-clean-end-to-end-scan" => "step-3-run-a-clean-end-to-end-scan",
          "hand-off-to-review-without-granting-retrieval" => "step-7-hand-off-to-review-without-granting-retrieval",
        },
        "hands-on/2026/08/23/hands-on-build-a-fail-closed-memory-router" => {
          "start-with-three-bounded-outcomes" => "step-1-start-with-three-bounded-outcomes",
          "prove-what-the-demonstration-claims" => "step-4-run-the-canary-suite",
        },
      }.each do |path, anchors|
        doc = document(path)
        anchors.each do |legacy, current|
          targets = doc.css("[id]").select { |node| node["id"] == legacy }
          assert_equal 1, targets.length, "#{path}##{legacy}"
          assert_equal current, targets.first.next_element&.[]("id"), legacy
        end
      end
    end

    def test_nonpublic_project_pages_have_no_empty_github_buttons
      %w[mlx-harmony oobabooga-macOS text-generation-webui-macos].each do |project|
        assert_empty document("projects/#{project}").css("a.github-link"), project
      end
      Dir.glob("#{ROOT}/**/*.html").each do |path|
        doc = Nokogiri::HTML(File.read(path))
        doc.css("a.github-link").each { |a| refute_empty a["href"].to_s.strip, path }
      end
    end

    if ENV["READER_BASELINE"]
      def test_original_outputs_and_discussion_identities_are_preserved
        baseline = File.expand_path(ENV.fetch("READER_BASELINE"))
        identity = lambda do |doc|
          script = doc.at_css('script[src="https://giscus.app/client.js"]')
          [doc.at_css('link[rel="canonical"]')&.[]("href"), script&.attributes&.select { |key, _| %w[data-repo data-repo-id data-category data-category-id data-mapping].include?(key) }&.transform_values(&:value)]
        end
        Dir.glob("#{baseline}/**/*.html").each do |old_path|
          relative = old_path.delete_prefix("#{baseline}/")
          current = File.join(ROOT, relative)
          assert File.file?(current), relative
          assert_equal identity.call(Nokogiri::HTML(File.read(old_path))), identity.call(Nokogiri::HTML(File.read(current))), relative
        end
      end
    end
  end
end
