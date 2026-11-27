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
require "yaml"
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

  def test_project_help_only_routes_configured_public_projects_and_respects_ancillary_page_context
    projects = [
      { "name" => "Example", "title" => "Example Tool", "repo_url" => "https://github.com/owner/example", "visibility" => "public" },
      { "name" => "Private", "repo_url" => "https://github.com/owner/private", "visibility" => "private" },
      { "name" => "Hidden", "repo_url" => "https://github.com/owner/hidden", "visibility" => "none" },
      { "name" => "Unconfigured", "repo_url" => "https://github.com/owner/unconfigured", "visibility" => "public" },
    ]
    site = { "data" => { "github_projects" => { "projects" => projects }, "project_help" => { "Example" => { "guide_url" => "/guide/", "guide_label" => "Read the guide", "prominent_guide" => true }, "Private" => {}, "Hidden" => {} } } }
    page = { "support_project" => "Example", "url" => "/guide/", "layout" => "page" }
    doc = Nokogiri::HTML.fragment(render_include("project_help.html", page: page, site: site))
    assert_equal 1, doc.css("#project-help").length
    assert doc.at_css('a[href="https://github.com/owner/example/issues"]')
    assert doc.at_css('a[href="https://github.com/owner/example/issues/new/choose"]')
    assert doc.at_css('a[href="/contact/#private-inquiries"]')
    assert_empty doc.css('a[href="/guide/"]'), "Do not link a guide to itself"
    %w[Private Hidden Unconfigured Missing].each do |name|
      assert_empty render_include("project_help.html", page: { "category" => name }, site: site).strip
    end
    header = Nokogiri::HTML.fragment(render_include("project_help.html", parameters: "position='header'", page: { "category" => "Example", "layout" => "project" }, site: site))
    assert header.at_css('.project-help--prominent h2 a[href="/guide/"]')
    picker = Nokogiri::HTML.fragment(render_include("project_help_picker.html", site: site))
    assert_equal ["Example"], picker.css("li[data-project-name]").map { |item| item["data-project-name"] }
    assert picker.at_css("[data-project-help-filter]").key?("hidden")
    assert picker.at_css('a[href="https://github.com/owner/example/issues/new/choose"]'), "The unenhanced page must retain usable links"
    assert_empty picker.css("form"), "The selector must not submit inquiry information"
  end

  def test_project_picker_only_filters_existing_links_and_does_not_collect_contact_data
    source = File.read(File.join(ROOT, "html/assets/js/project-help.js"))
    harness = <<~JS
      const vm = require('node:vm');
      const rows = ['LogGPT', 'UnicodeFix'].map(name => ({dataset:{projectName:name},hidden:false}));
      const filter = {hidden:true};
      const select = {value:'',addEventListener(type, handler){if(type!=='change')throw Error(type);this.change=handler;}};
      const picker = {
        querySelector(selector){if(selector==='[data-project-help-filter]')return filter;if(selector==='#project-help-select')return select;throw Error('Unexpected field access: '+selector);},
        querySelectorAll(selector){if(selector!=='[data-project-name]')throw Error(selector);return rows;}
      };
      for(const present of [false,true]){
        const document={addEventListener(type,handler){if(type!=='DOMContentLoaded')throw Error(type);handler();},querySelector(selector){if(selector!=='[data-project-help-picker]')throw Error(selector);return present?picker:null;}};
        const context={document};
        for(const key of ['fetch','localStorage','location'])Object.defineProperty(context,key,{get(){throw Error('Unexpected side effect: '+key);}});
        vm.runInNewContext(#{source.to_json},context);
      }
      if(filter.hidden||rows.some(row=>row.hidden))throw Error('Initial links missing');
      select.value='LogGPT';select.change();
      if(rows[0].hidden||!rows[1].hidden)throw Error('Wrong project selected');
      select.value='';select.change();
      if(rows.some(row=>row.hidden))throw Error('Could not restore all projects');
    JS
    output, status = Open3.capture2e("node", "-e", harness)
    assert status.success?, output
  end

  def test_shared_github_issue_forms_and_review_packages_have_valid_required_fields_and_private_routes
    files = Dir.glob(File.join(ROOT, ".github/ISSUE_TEMPLATE/*.yml")) + Dir.glob(File.join(ROOT, "docs/templates/project-issue-forms/**/*.yml"), File::FNM_DOTMATCH)
    assert_equal 11, files.length
    files.each do |path|
      form = YAML.safe_load(File.read(path))
      if File.basename(path) == "config.yml"
        assert_equal true, form.fetch("blank_issues_enabled")
        assert form.fetch("contact_links").any? { |link| link["url"] == "https://unixwzrd.ai/contact/#private-inquiries" }
        form.fetch("contact_links").each { |link| assert_equal "https://unixwzrd.ai", URI.parse(link.fetch("url")).then { |url| "#{url.scheme}://#{url.host}" } }
        next
      end
      refute_empty form.fetch("name")
      refute_empty form.fetch("description")
      fields = form.fetch("body")
      ids = fields.filter_map { |field| field["id"] }
      assert_equal ids.uniq, ids
      fields.each do |field|
        assert_includes %w[markdown input textarea dropdown checkboxes], field.fetch("type")
        next if field["type"] == "markdown"
        assert_match(/\A[a-z][a-z0-9-]*\z/, field.fetch("id"))
        refute_empty field.fetch("attributes").fetch("label")
      end
      assert fields.any? { |field| field["type"] == "checkboxes" && field.fetch("attributes").fetch("options").any? { |option| option["required"] == true } }
      assert_includes fields.select { |field| field["type"] == "markdown" }.map { |field| field.dig("attributes", "value") }.join, "https://unixwzrd.ai/contact/#private-inquiries"
      refute form.key?("assignees")
      refute form.key?("labels"), "Do not depend on labels that may not exist in another repository"
    end
    assert File.file?(File.join(ROOT, "docs/templates/project-issue-forms/code-analytics/.github/ISSUE_TEMPLATE/feature_request.yml"))
    refute File.exist?(File.join(ROOT, "docs/templates/project-issue-forms/code-analytics/.github/ISSUE_TEMPLATE/bug_report.yml")), "Preserve the existing Code Analysis bug form"
  end

  ReleasePost = Struct.new(:data, :date, :relative_path, :url)
  ReleaseSite = Struct.new(:posts, :pages, :data, :time)

  def release_post(name, date: "2026-11-18", project: "Example", **data)
    ReleasePost.new(
      { "title" => name, "content_type" => "update" }.merge(data.transform_keys(&:to_s)),
      Time.parse(date), "projects/#{project}/_posts/#{name}.md", "/projects/#{project}/#{name}/",
    )
  end

  def release_site(posts)
    ReleaseSite.new(
      Struct.new(:docs).new(posts),
      %w[Example Other].map { |name| Struct.new(:url).new("/projects/#{name}/") },
      {}, Time.parse("2026-11-26"),
    )
  end

  def test_discovery_order_uses_publication_dates_even_with_later_edits_and_notices
    old = release_post("old", date: "2026-08-19", last_modified_at: "2026-11-25", update_notice: "Substantial revision")
    latest = release_post("latest", date: "2026-11-18")
    [old, latest].each { |doc| PostListMetadata.apply_to_post!(doc) }
    assert_equal old.date, old.data["list_date"]
    assert_equal [latest, old], [old, latest].sort_by { |doc| doc.data.fetch("list_sort_key") }
    first = release_post("first", sequence: 1)
    second = release_post("second", sequence: 2)
    [first, second].each { |doc| PostListMetadata.apply_to_post!(doc) }
    assert_equal [first, second], [second, first].sort_by { |doc| doc.data.fetch("list_sort_key") }
  end

  def test_updated_badges_require_real_editorial_notice_and_modified_date
    no_date = post("old", "date" => "2026-08-19", "update_notice" => "Editorial note")
    assert_empty Nokogiri::HTML.fragment(render_include("post_list_meta.html", parameters: "post=page", page: no_date)).css(".post-updated-badge")
    edited = no_date.merge("modified_date" => "2026-11-25")
    badge = Nokogiri::HTML.fragment(render_include("post_list_meta.html", parameters: "post=page", page: edited)).at_css(".post-updated-badge time")
    assert badge["datetime"].start_with?("2026-11-25")
    automatic = edited.reject { |key, _| key == "update_notice" }.merge("newer_release" => { "version" => "2.0" })
    assert_empty Nokogiri::HTML.fragment(render_include("post_list_meta.html", parameters: "post=page", page: automatic)).css(".post-updated-badge")
  end

  def test_release_notices_use_only_explicit_public_releases_and_stay_within_the_product
    old = release_post("old", date: "2026-08-19", update_notice: "A real editorial correction", release_version: "1.0")
    current = release_post("current", release_version: "2.0", release_status: "released", excerpt: "A useful maintenance release.")
    rejected = [
      release_post("preview", date: "2026-11-20", release_version: "3.0", release_status: "preview"),
      release_post("unpublished", date: "2026-11-21", release_version: "4.0", release_status: "released", published: false),
      release_post("future", date: "2027-01-01", release_version: "5.0", release_status: "released"),
      release_post("_drafts/draft", date: "2026-11-22", release_version: "6.0", release_status: "released"),
      release_post("draft-flag", date: "2026-11-22", release_version: "6.1", release_status: "released", draft: true),
      release_post("social-posts", date: "2026-11-23", release_version: "7.0", release_status: "released"),
      release_post("excluded", date: "2026-11-24", release_version: "8.0", release_status: "released", list_exclude: true),
      release_post("case-study", date: "2026-11-25", content_type: "case-study"),
      release_post("unqualified", date: "2026-11-25", release_version: "9.0"),
    ]
    other = release_post("other-release", project: "Other", release_version: "99.0", release_status: "released")
    opted_out = release_post("opt-out", date: "2026-08-18", release_notice: false)
    story = release_post("story", date: "2026-08-18", content_type: nil)
    same_version = release_post("same-version", date: "2026-08-18", release_version: "2.0")
    site = release_site([old, current, other, opted_out, story, same_version, *rejected])
    ProductReleaseNotices.apply!(site)
    notice = old.data.fetch("newer_release")
    assert_equal "2.0", notice["version"]
    assert_equal current.url, notice["url"]
    assert_equal "/projects/Example/", notice["overview_url"]
    assert_equal current.date, notice["date"]
    assert_equal "A real editorial correction", old.data["update_notice"]
    [current, other, opted_out, story, same_version, *rejected].each { |doc| refute doc.data.key?("newer_release"), doc.relative_path }
    rendered = Nokogiri::HTML.fragment(render_include("product_release_notice.html", page: old.data))
    assert_equal 1, rendered.css("aside.post-update-notice[role='note']").length
    assert_equal ["/projects/Example/", current.url], rendered.css("a").map { |link| link["href"] }

    # A subsequent release updates old notices without editing any older post.
    next_release = release_post("next", date: "2026-11-25", release_version: "2.1", release_status: "released")
    site.posts.docs << next_release
    ProductReleaseNotices.apply!(site)
    assert_equal "2.1", old.data.fetch("newer_release")["version"]
    assert_equal "2.1", current.data.fetch("newer_release")["version"]
    refute next_release.data.key?("newer_release")
    site.posts.docs.each { |doc| doc.data.delete("release_status") }
    ProductReleaseNotices.apply!(site)
    assert site.posts.docs.none? { |doc| doc.data.key?("newer_release") }, "Withdrawn releases must not leave stale notices"
  end

  def test_release_notices_skip_hidden_products_and_missing_overviews
    old = release_post("old", date: "2026-08-19")
    current = release_post("current", release_version: "2.0", release_status: "released")
    site = release_site([old, current])
    site.pages.clear
    ProductReleaseNotices.apply!(site)
    refute old.data.key?("newer_release")
    site.pages << Struct.new(:url).new("/projects/Example/")
    site.data["github_projects"] = { "projects" => [{ "name" => "Example", "visibility" => "none" }] }
    ProductReleaseNotices.apply!(site)
    refute old.data.key?("newer_release")
  end

  def test_local_reader_include_is_localhost_only_in_every_build_and_supports_page_opt_out
    assert_equal true, SITE.config.fetch("defaults").first.fetch("values").fetch("local_reader")
    %w[development production test].each do |environment|
      doc = Nokogiri::HTML.fragment(render_include("local_reader.html", environment: environment))
      assert_equal 1, doc.css("script[data-local-reader-loader]").length
      assert_empty doc.css("script[src]")
      assert_empty Nokogiri::HTML.fragment(render_include("local_reader.html", environment: environment, page: { "local_reader" => false })).css("script")
      loader = doc.at_css("script").text
      harness = <<~JS
        const vm = require('node:vm');
        const source = #{loader.to_json};
        for (const hostname of ['localhost', '127.0.0.1', '[::1]', 'unixwzrd.ai', 'www.unixwzrd.ai', 'localhost.example.com', '127.0.0.1.example.com', 'example.com', '']) {
          const scripts = [];
          const context = { window: { location: { hostname } }, document: {
            querySelector: () => scripts.length ? scripts[0] : null,
            createElement: () => ({ dataset: {} }),
            body: { append: script => scripts.push(script) },
          }};
          vm.runInNewContext(source, context);
          vm.runInNewContext(source, context);
          const local = ['localhost', '127.0.0.1', '[::1]'].includes(hostname);
          if (scripts.length !== (local ? 1 : 0)) throw Error(`Incorrect loader count: ${hostname}`);
          if (local && (!scripts[0].src.startsWith('/assets/js/article-tts-player.js?v=') || !scripts[0].defer)) throw Error('Incorrect player asset');
        }
      JS
      output, status = Open3.capture2e("node", "-e", harness)
      assert status.success?, output
    end
    %w[default review].each do |layout|
      source = File.read(File.join(ROOT, "html/_layouts/#{layout}.html"))
      assert_equal 1, source.scan("include local_reader.html").length
      assert_includes source, "data-local-reader-content"
    end
    refute_includes File.read(File.join(ROOT, "html/_layouts/post.html")), "article-tts-player.js"
  end

  def filtered_titles(parameters, posts, projects = [])
    template = "{% include filter_discovery_posts.html #{parameters} %}{{ discovery_posts | map: 'title' | join: '|' }}"
    Liquid::Template.parse(template).render!(
      { "site" => { "posts" => posts, "data" => { "github_projects" => { "projects" => projects } } } },
      registers: { site: SITE }, strict_filters: true,
    ).strip
  end

  def test_local_reader_player_returns_before_reading_browser_state_on_public_hosts
    source = File.read(File.join(ROOT, "html/assets/js/article-tts-player.js"))
    harness = <<~JS
      const vm = require('node:vm');
      for (const hostname of ['unixwzrd.ai', 'www.unixwzrd.ai', 'localhost.example.com', '127.0.0.1.example.com']) {
        const window = { location: { hostname } };
        Object.defineProperty(window, 'localStorage', { get() { throw Error('Public page accessed local storage'); } });
        const context = { window };
        Object.defineProperty(context, 'document', { get() { throw Error('Public page initialized the player'); } });
        vm.runInNewContext(#{source.to_json}, context);
      }
    JS
    output, status = Open3.capture2e("node", "-e", harness)
    assert status.success?, output
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
    assert_equal "Review <example> - Review copy", doc.at_css("title").text
    assert_equal "noindex, nofollow, noarchive", doc.at_css('meta[name="robots"]')["content"]
    assert_equal "no-referrer", doc.at_css('meta[name="referrer"]')["content"]
    assert_equal "all", doc.at_css("[data-unlisted-review]")["data-pagefind-ignore"]
    assert_equal "Draft <not accepted>", doc.at_css("aside p:last-of-type").text
    assert_equal 1, doc.css("h1").length
    assert_empty doc.css("script:not([data-local-reader-loader]), footer, [data-pagefind-body], .support-section, .post-comments")
    assert_equal 1, doc.css("script[data-local-reader-loader]").length
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
    assigns["page"]["review_index"] = "/hidden/packet/"
    with_packet = Nokogiri::HTML(Liquid::Template.parse(source).render!(assigns, registers: { site: SITE }, strict_filters: true))
    assert_equal "/hidden/packet/", with_packet.at_css('[aria-label="Review packet"] a')["href"]
    assert_equal "/hidden/packet/", with_packet.at_css("[data-unlisted-review]")["data-review-packet"]
    assigns["page"]["url"] = "/hidden/packet/"
    packet_index = Nokogiri::HTML(Liquid::Template.parse(source).render!(assigns, registers: { site: SITE }, strict_filters: true))
    assert_empty packet_index.css('[aria-label="Review packet"]')
  end

  def test_review_diagrams_use_the_standard_viewer_without_inline_scripts
    src = "/hidden/example/diagrams/policy.svg"
    title = "Policy & authorization"
    html = render_include("blog_diagram.html", parameters: "src=page.diagram alt=page.diagram_title", page: { "diagram" => src, "diagram_title" => title })
    doc = Nokogiri::HTML.fragment(html)
    assert_equal src, doc.at_css("img")["src"]
    assert_equal title, doc.at_css("img")["alt"]
    assert_equal 2, doc.css("a").length
    doc.css("a").each do |link|
      url = URI.parse(link["href"])
      assert_equal "/diagram-viewer/", url.path
      assert_equal({ "src" => src, "title" => title }, URI.decode_www_form(url.query).to_h)
      assert_equal "_blank", link["target"]
    end
    assert_empty doc.css("script")
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
    release = YAML.safe_load(File.read(File.join(ROOT, "html/_data/secrets_kit.yml")))
    assert_includes actual, "Secrets Kit #{release.fetch('product_version')} is available"
    assert_includes actual, "optional paid Remote Secret Sync"
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
    collaborate_children = settings.fetch("collaborate.md").fetch("children")
    collaborate_links = doc.css(".nav-dropdown-collaborate .nav-dropdown-item")
    assert_equal collaborate_children.map { |child| child.fetch("label") }, collaborate_links.map(&:text)
    assert_equal collaborate_children.map { |child| child.fetch("url") }, collaborate_links.map { |link| link["href"] }
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
    RELEASE_SOURCE = Jekyll::Site.new(ReaderExperienceTest::SITE.config.merge(
      "destination" => File.join(ReaderExperienceTest::TEMP, "release-source"),
    )).tap(&:read)
    PILOTS = %w[
      technology/2025/04/08/Remote-Debugging-With-VSCode
      technology/2026/08/23/memory-is-a-governance-problem-not-just-a-vector-database
    ].freeze

    def document(path)
      Nokogiri::HTML(File.read(File.join(ROOT, path, "index.html")))
    end

    # Read expected targets from published source metadata, not the generated
    # notice. Adding a release must not require updating hardcoded test versions.
    def latest_release_for(project)
      RELEASE_SOURCE.posts.docs.select do |post|
        post.relative_path.start_with?("projects/#{project}/_posts/") &&
          post.data["release_status"] == "released" && post.data["release_version"] &&
          post.data["published"] != false && !post.data["list_exclude"] &&
          !post.draft? && post.date <= RELEASE_SOURCE.time
      end.max_by(&:date)
    end

    def release_url(post)
      ProjectPostPermalink.permalink_for_project_post(post)
    end

    def test_loggpt_120_points_readers_to_current_information_without_changing_legacy_urls
      path = "projects/LogGPT/2026/08/19/loggpt-1-2-0-and-loggpt-plus"
      page = document(path)
      notice = page.at_css(".post-update-notice")
      refute_nil notice
      release = latest_release_for("LogGPT")
      version = release.data.fetch("release_version")
      assert_equal "Version #{version} update · #{release.date.strftime('%B %-d, %Y')}", notice.at_css(".post-update-notice__title").text
      assert_equal [
        "/projects/LogGPT/",
        release_url(release),
      ], notice.css("a").to_a.last(2).map { |link| link["href"] }
      assert_includes notice.text, "Read the #{version} release announcement"
      assert_includes notice.text, "original announcement and its publication date are preserved"
      assert page.at_css(".dt-published")["datetime"].start_with?("2026-08-19")
      assert_nil page.at_css(".dt-modified"), "An automatic release pointer is not an editorial revision"
      assert_includes page.at_css("h1").text, "LogGPT 1.2.0 and LogGPT Plus"
      assert_includes page.at_css(".post-content").text, "I am pleased to announce LogGPT 1.2.0"
      assert_operator page.to_html.index('class="post-update-notice"'), :<, page.to_html.index('class="post-banner-image"')
      destination = "https://unixwzrd.ai/#{path}/"
      assert_equal destination, page.at_css('link[rel="canonical"]')["href"]
      ["s/39e7b3ae47", "#{path}-preserve-conversations-and-artifacts"].each do |redirect|
        assert_equal destination, document(redirect).at_css('link[rel="canonical"]')["href"]
      end
    end

    def test_project_posts_sort_by_publication_and_share_automatic_release_notices
      overview = document("projects/LogGPT")
      dates = overview.css(".post-list > li .post-meta > time:first-child").map { |time| Time.parse(time["datetime"]) }
      refute_empty dates
      assert_equal dates.sort.reverse, dates
      %w[2026/11/16/loggpt-1-3-3-checkbox-visibility-fix 2026/11/17/loggpt-1-3-4-dots-conversation-exports].each do |path|
        notices = document("projects/LogGPT/#{path}").css(".post-update-notice")
        assert_equal 1, notices.length
        assert_includes notices.first.css("a").map { |link| link["href"] }, release_url(latest_release_for("LogGPT"))
      end
      assert_empty document(release_url(latest_release_for("LogGPT")).delete_prefix("/")).css("aside[aria-label='Newer product release']")
      secrets = document("projects/Secrets-Kit/2026/10/28/secrets-kit-2-0-2-local-secrets-peer-to-peer-sync")
      assert_equal 1, secrets.css(".post-update-notice").length
      assert secrets.at_css('.post-update-notice a[href="/projects/Secrets-Kit/"]')
      assert_includes secrets.css(".post-update-notice a").map { |link| link["href"] }, release_url(latest_release_for("Secrets-Kit"))
      assert_includes secrets.at_css("h1").text, "Coming Soon"
      assert_includes secrets.at_css(".post-content").text, "pre-announcement, not general availability"
      unicode = document("projects/UnicodeFix/2026/10/19/unicodefix-v2-0-2-one-command-for-text-and-images")
      assert_includes unicode.css(".post-update-notice a").map { |link| link["href"] }, release_url(latest_release_for("UnicodeFix"))
      assert_empty document("projects/LogGPT/2026/10/15/when-codex-turned-to-loggpt").css("aside[aria-label='Newer product release']")
      {
        "projects/extract-chat/2026/08/24/extract-chat-v0-6-0-loggpt-plus-archive-support" => "extract-chat",
        "projects/TorchDevice/2025/03/05/new-0-0-05-torchdevice-release" => "TorchDevice",
      }.each do |old_path, project|
        notice = document(old_path).at_css("aside[aria-label='Newer product release']")
        refute_nil notice, old_path
        assert_includes notice.css("a").map { |link| link["href"] }, release_url(latest_release_for(project))
      end
      preview = document("projects/extract-chat/2026/11/20/extract-chat-1-0-0-native-macos-app")
      preview_date = Time.parse(preview.at_css(".dt-published")["datetime"])
      if latest_release_for("extract-chat").date <= preview_date
        assert_empty preview.css("aside[aria-label='Newer product release']"), "The newer Mac App Store preview must not point backwards or supersede a shipped release"
      else
        assert_includes preview.css(".post-update-notice a").map { |link| link["href"] }, release_url(latest_release_for("extract-chat"))
      end
    end

    def test_artex_repository_update_preserves_original_dates_urls_and_attribution_limits
      path = "technology/2026/11/18/artex-ai-attacks-and-the-november-outages"
      page = document(path)
      notice = page.at_css(".post-update-notice")
      refute_nil notice
      assert notice.at_css("a[href='https://github.com/BaaRai/ARTEX']")
      assert notice.at_css("a[href='https://blog.talosintelligence.com/artex-and-beyond/']")
      ["English-language translation and continuation", "July 2026", "not run or audited", "not evidence connecting the November outages"].each do |text|
        assert_includes notice.text, text
      end
      assert page.at_css(".dt-published")["datetime"].start_with?("2026-11-18")
      assert page.at_css(".dt-modified")["datetime"].start_with?("2026-11-23")
      assert_includes page.at_css(".post-content").text, "outage inventory retains its November 18 research cutoff"
      content = page.at_css(".post-content")
      %w[a-working-framework-is-not-the-same-as-a-vetted-fork the-testing-tool-can-itself-be-the-supply-chain-compromise].each do |id|
        assert content.at_css("h2[id='#{id}']"), id
      end
      %w[https://badbyte.io/artex-backdoor-docker-image/ https://asec.ahnlab.com/en/95845/ https://github.com/BaaRai/ARTEX/pull/128].each do |url|
        assert content.at_css("a[href='#{url}']"), url
      end
      ["Pulls are not unique installations", "inside the container", "not evidence that BaaRai", "not an independent audit"].each do |text|
        assert_includes content.text, text
      end
      assert_equal "#a-working-framework-is-not-the-same-as-a-vetted-fork", notice.at_css('a[href^="#"]')["href"]
      destination = "https://unixwzrd.ai/#{path}/"
      assert_equal destination, page.at_css('link[rel="canonical"]')["href"]
      assert_equal destination, document("s/33594dffe3").at_css('link[rel="canonical"]')["href"]
    end

    def test_extract_chat_100_announcement_preserves_availability_scope_and_short_link
      path = "projects/extract-chat/2026/11/20/extract-chat-1-0-0-native-macos-app"
      page = document(path)
      content = page.at_css(".post-content")
      assert_equal ["Extract Chat 1.0.0 Brings Conversation Archives to the Mac"], page.css("h1").map { |heading| heading.text.strip }
      ["available soon on the Mac App Store", "Apple silicon", "macOS 14", ".lgpt", "Hermes Desktop", "View CSS", "Save As", "Choose CSS", "Install CLI", "Original input archive"].each do |text|
        assert_includes content.text.downcase, text.downcase
      end
      assert content.at_css("a[href='/projects/extract-chat/macos/']")
      assert content.at_css("a[href='https://github.com/unixwzrd/extract-chat/tree/v1.0.0']")
      assert_equal 2, content.css("figure.project-screenshot img").length
      refute_match(/available now on the (?:Mac )?App Store|approved by Apple/i, content.text)
      destination = "https://unixwzrd.ai/#{path}/"
      assert_equal destination, page.at_css('link[rel="canonical"]')["href"]
      redirect = document("s/43ec12ca50")
      assert_equal destination, redirect.at_css('link[rel="canonical"]')["href"]
      assert_equal "/#{path}/", document("projects/extract-chat").at_css(".post-link")["href"]
      refute File.exist?(File.join(ROOT, "projects/extract-chat/_drafts/2026-11-20-extract-chat-1-0-0-social-posts.txt"))
    end

    def test_loggpt_mobile_guide_is_discoverable_and_uses_shared_navigation_and_screenshot_styles
      path = "projects/LogGPT/ios-guide"
      guide = document(path)
      assert_equal ["LogGPT User Guide for iPhone and iPad"], guide.css("h1").map { |heading| heading.text.strip }
      assert_equal "https://unixwzrd.ai/#{path}/", guide.at_css('link[rel="canonical"]')["href"]
      breadcrumbs = guide.at_css('nav[aria-label="Breadcrumb navigation"]')
      assert_equal ["/", "/projects/", "/projects/LogGPT/"], breadcrumbs.css("a").map { |link| link["href"] }
      assert_equal "LogGPT User Guide for iPhone and iPad", breadcrumbs.at_css('[aria-current="page"]').text.strip
      assert_empty document("projects").css(".projects-list a[href='/#{path}/']"), "The manual is not a peer project"
      assert_empty guide.css(".nav-dropdown-projects a[href='/#{path}/']"), "Keep the manual out of the top-level project catalog"
      assert_empty document("projects/LogGPT").css(".post-list .post-link[href='/#{path}/']"), "The manual is not a blog post"
      overview = document("projects/LogGPT")
      callout = overview.at_css(".page-header .project-help--prominent")
      assert callout.at_css("h2 a[href='/#{path}/']"), "The guide must be prominent directly below the project title"
      assert callout.at_css('a[href="https://github.com/unixwzrd/LogGPT/issues/new/choose"]'), "Ordinary support must go directly to the GitHub chooser"
      assert_operator overview.to_html.index('class="contact-card project-help project-help--prominent"'), :<, overview.to_html.index('class="page-banner-image"')
      content = guide.at_css("article.page > .page-content")
      assert content.at_css("a[href='/projects/LogGPT/']"), "Keep a route back to the product overview"
      toc = content.css("details.post-toc")
      assert_equal 1, toc.length
      refute toc.first.key?("open"), "The shared On this page index must start collapsed"
      sections = content.css("h2[id]").map { |heading| "##{heading['id']}" }
      assert_equal 8, sections.length
      assert_equal sections, toc.first.css("nav a").map { |link| link["href"] }
      images = content.css("figure.project-screenshot img")
      assert_equal 35, images.length
      stylesheet = File.read(File.join(ROOT, "assets/css/style.css"))
      screenshot_styles = stylesheet[/\.loggpt-guide-screenshots img\s*\{([^}]+)\}/, 1]
      refute_nil screenshot_styles, "Keep the border scoped to the manual's screenshots"
      assert_match(/border:\s*1px\s+solid\s+#fff(?:fff)?\s*;/, screenshot_styles)
      assert_match(/box-sizing:\s*border-box/, screenshot_styles)
      images.each do |image|
        assert image["src"].start_with?("/assets/images/projects/LogGPT/ios-guide/")
        assert File.file?(File.join(ROOT, image["src"])), image["src"]
        assert_equal image["src"], image.parent["href"], "Each screenshot must open its full-resolution source"
        refute_empty image["alt"]
        assert_operator image["width"].to_i, :>, 0
        assert_operator image["height"].to_i, :>, 0
        assert_equal "lazy", image["loading"]
        assert_equal "async", image["decoding"]
        refute_empty image.ancestors("figure").first.at_css("figcaption").text.strip
      end
      phone_examples = content.css("details:not(.post-toc)")
      assert_equal 6, phone_examples.length
      phone_examples.each do |example|
        assert_includes example.at_css("summary").text, "iPhone"
        refute_nil example.at_css('img[src*="/ios-guide/iphone/"]'), "Retain the expandable iPhone instructions"
        refute example.key?("open")
      end
      assert_equal 17, images.count { |image| image["src"].include?("/iphone/") }
      ["Basic", "one-time upgrade", "Generated Content", "Uploaded Content", "Set Default Folder", "Discard Export", "Restore purchases"].each do |text|
        assert_includes content.text, text
      end
      assert_empty content.css("script, iframe")
      assert_empty guide.css(".page-store-link"), "Do not add a mobile install claim before availability is confirmed"
    end

    def test_product_help_routes_to_each_products_own_repository_and_preserves_private_contact
      contact = document("contact")
      picker = contact.at_css("#product-help")
      refute_nil picker
      assert contact.at_css("#private-inquiries #contact-form")
      assert_operator contact.to_html.index('id="product-help"'), :<, contact.to_html.index('id="contact-form"')
      names = YAML.safe_load(File.read(File.join(ReaderExperienceTest::ROOT, "html/_data/project_help.yml"))).keys
      assert_equal names.sort, picker.css("[data-project-name]").map { |row| row["data-project-name"] }.sort
      catalog = YAML.safe_load(File.read(File.join(ReaderExperienceTest::ROOT, "html/_data/github_projects.yml"))).fetch("projects")
      names.each do |name|
        repo = catalog.find { |project| project["name"] == name }.fetch("repo_url")
        row = picker.at_css("[data-project-name='#{name}']")
        assert row.at_css("a[href='#{repo}/issues']"), name
        assert row.at_css("a[href='#{repo}/issues/new/choose']"), name
        product = document("projects/#{name}")
        assert product.at_css(".content-footer a[href='#{repo}/issues']"), name
      end
      guide = document("projects/LogGPT/ios-guide")
      assert_equal 1, guide.css("#project-help").length
      assert guide.at_css('#project-help a[href="https://github.com/unixwzrd/LogGPT/issues/new/choose"]')
      assert guide.at_css('#project-help a[href="/contact/#private-inquiries"]')
      assert_includes guide.at_css("#project-help").text, "GitHub is our product support tracking system"
      assert_includes guide.at_css("#project-help").text, "setup and usage questions"
      assert_includes guide.at_css("#project-help").text, "ordinary product support is tracked through GitHub issues"
      assert_includes contact.at_css("#private-inquiries").text, "Email is not a separate product support queue"
      assert_empty guide.css(".get-in-touch-section"), "Project help must replace the generic email-first footer"
      article = document("projects/LogGPT/2026/11/18/loggpt-1-3-5-toolbar-downloads-and-lgpt-archives")
      assert article.at_css('#project-help a[href="https://github.com/unixwzrd/LogGPT/issues/new/choose"]')
      assert_empty document("projects/TorchDevice").css("#project-help"), "Do not advertise support for unconfigured legacy projects"
    end

    def test_extract_chat_macos_walkthrough_has_linked_screenshots_and_accurate_scope
      overview = document("projects/extract-chat")
      assert overview.at_css(".project-intro a[href='/projects/extract-chat/macos/']"), "Keep the walkthrough discoverable before project updates"
      page = document("projects/extract-chat/macos")
      assert_equal ["Extract Chat for macOS"], page.css("h1").map { |heading| heading.text.strip }
      assert_equal "https://unixwzrd.ai/projects/extract-chat/macos/", page.at_css('link[rel="canonical"]')["href"]
      content = page.at_css("article.page .page-content")
      assert content.at_css("a[href='/projects/extract-chat/']")
      %w[conversion artifacts transcript hermes batch].each do |name|
        src = "/assets/images/projects/extract-chat/macos-#{name}.webp"
        image = content.at_css("figure.project-screenshot img[src='#{src}']")
        refute_nil image, name
        refute_empty image["alt"]
        assert_equal "lazy", image["loading"]
        assert_equal ["2560", "1600"], [image["width"], image["height"]]
        assert File.file?(File.join(ROOT, src)), src
        link = image.parent
        assert_equal src, link["href"]
        assert_equal "_blank", link["target"]
        assert_includes link["rel"].split, "noopener"
        assert_includes link["rel"].split, "noreferrer"
      end
      assert_equal 5, content.css("figure.project-screenshot").length
      ["Apple silicon", "macOS 14", "App Store review", "View CSS", "Save As", "Choose CSS", "not Markdown", "Original input files are not modified"].each do |text|
        assert_includes content.text, text
      end
      assert_empty content.css("script, iframe, button")
    end

    def test_extract_chat_policies_are_public_and_linked_from_the_index_and_product
      index = document("Policies")
      product = document("projects/extract-chat")
      policies = {
        "Privacy_Extract_Chat" => ["Extract Chat Privacy Policy", "Terms_Extract_Chat"],
        "Terms_Extract_Chat" => ["Extract Chat Terms of Use", "Privacy_Extract_Chat"],
      }
      policies.each do |name, (title, counterpart)|
        page = document("Policies/#{name}")
        assert_equal title, page.at_css("h1").text.strip
        content = page.at_css("article.page .page-content")
        assert_includes content.text, "Effective Date: November 20, 2026"
        refute_match(/Draft for review|not yet published|effective date will be added/i, content.text)
        assert content.at_css("a[href='/Policies/#{counterpart}/']")
        assert_equal "https://unixwzrd.ai/Policies/#{name}/", page.at_css('link[rel="canonical"]')["href"]
        [index, product].each { |source| assert source.at_css("a[href='/Policies/#{name}/']"), name }
      end
    end

    def test_unlisted_reviews_have_no_inbound_listing_links_or_tracking
      files = Dir.glob("#{ROOT}/**/*.html")
      reviews = files.select { |path| File.read(path).include?("data-unlisted-review") }
      packets = reviews.to_h do |path|
        doc = Nokogiri::HTML(File.read(path))
        [path, doc.at_css("[data-unlisted-review]")["data-review-packet"].to_s]
      end
      reviews.each do |path|
        doc = Nokogiri::HTML(File.read(path))
        url = URI.parse(doc.at_css('link[rel="canonical"]')["href"]).path
        assert_includes doc.at_css('meta[name="robots"]')["content"], "noindex"
        assert_equal "no-referrer", doc.at_css('meta[name="referrer"]')["content"]
        assert_empty doc.css("script:not([data-local-reader-loader]), [data-pagefind-body], .support-section, .post-comments")
        assert_equal 1, doc.css("script[data-local-reader-loader]").length
        doc.css('img[src$=".svg"]').each do |image|
          figure = image.ancestors("figure.blog-diagram").first
          refute_nil figure, "review diagram bypasses standard component: #{image['src']}"
          links = figure.css("a").map { |link| URI.parse(link["href"]) }
          assert_equal 2, links.size
          links.each do |link|
            assert_equal "/diagram-viewer/", link.path
            assert_equal image["src"], URI.decode_www_form(link.query).to_h["src"]
          end
        end
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
        packet = packets.fetch(path)
        if !packet.empty? && packet != url
          assert_equal [packet], doc.css('[aria-label="Review packet"] a').map { |link| link["href"] }
        end
        files.reject { |other| other == path || (!packet.empty? && packets[other] == packet) }.each do |other|
          refute_includes File.read(other), url, "unlisted review linked from #{other}"
        end
        %w[sitemap.xml feed.xml redirects.json].each do |name|
          refute_includes File.read(File.join(ROOT, name)), url, name
        end
      end
    end

    def test_diagram_viewer_is_unindexed_and_does_not_load_tracking
      doc = document("diagram-viewer")
      assert_equal "false", doc.at_css("#diagram-image")["draggable"]
      assert_includes doc.at_css('meta[name="robots"]')["content"], "noindex"
      assert_equal "no-referrer", doc.at_css('meta[name="referrer"]')["content"]
      assert_empty doc.css("script[src]")
      refute_includes doc.to_html, "googletagmanager"
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

    def test_secrets_kit_offers_the_stable_release_after_ga
      body = document("projects/Secrets-Kit").at_css(".project-description").text
      assert_includes body, "Get Started"
      refute_includes body, "coming soon"
      setup = document("projects/Secrets-Kit/get-started")
      release = YAML.safe_load(File.read(File.expand_path("../html/_data/secrets_kit.yml", __dir__)))
      assert setup.at_css("a[href='#{release.fetch('repository_url')}/releases/tag/#{release.fetch('release_tag')}']")
      assert_nil setup.at_css('#release-status')
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






