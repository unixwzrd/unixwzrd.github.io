#!/usr/bin/env ruby
# frozen_string_literal: true

# Offline only: render templates and execute their inline JS in Node's VM.
# ATTRIBUTION_SITE=/tmp/build ATTRIBUTION_BASELINE=/tmp/before bundle exec ruby scripts/test_short_link_attribution.rb
require "bundler/setup"
require "jekyll"
require "minitest/autorun"
require "nokogiri"
require "json"
require "open3"
require "uri"

class ShortLinkAttributionTest < Minitest::Test
  ROOT = File.expand_path("..", __dir__)
  VM = <<~'JS'
    const vm = require("node:vm");
    const fs = require("node:fs");
    const input = JSON.parse(fs.readFileSync(0, "utf8"));
    const current = new URL(input.location);
    const redirects = [];
    const sandbox = {
      URL, URLSearchParams, Date,
      navigator: {userAgent: "Offline attribution regression test"},
      document: {referrer: input.referrer || "", addEventListener() {}},
      location: {
        href: current.href, search: current.search, hash: current.hash,
        hostname: current.hostname, pathname: current.pathname, origin: current.origin,
        replace(value) { redirects.push(value); }
      }
    };
    sandbox.window = sandbox;
    vm.runInNewContext(input.script, sandbox, {timeout: 1000});
    console.log(JSON.stringify({redirects, commands: (sandbox.dataLayer || []).map(item => Array.from(item))}));
  JS

  def execute(html, location: "https://unixwzrd.ai/example/?utm_source=qa", referrer: "https://referral.example/")
    scripts = Nokogiri::HTML(html).css("script:not([src])").map(&:text).join("\n")
    output, error, status = Open3.capture3("node", "-e", VM, stdin_data: JSON.generate(script: scripts, location: location, referrer: referrer))
    assert status.success?, error
    JSON.parse(output)
  end

  def redirect(target)
    template = File.read(File.join(ROOT, "html/_layouts/redirect.html")).split(/^---\s*$\n?/, 3).last
    Liquid::Template.parse(template).render!("page" => { "redirect" => { "to" => target } })
  end

  def assert_one_page_view(result)
    configs = result.fetch("commands").select { |command| command[0] == "config" }
    manual = result.fetch("commands").select { |command| command[0..1] == ["event", "page_view"] }
    assert_equal 1, configs.length
    assert_equal 1, configs.count { |command| command.fetch(2, {})["send_page_view"] != false } + manual.length
    assert_equal 1, result.fetch("commands").count { |command| command[0..1] == ["event", "page_context"] }
  end

  def test_redirect_preserves_raw_parameters_and_fragments_without_changing_mapping
    target = "https://unixwzrd.ai/destination/"
    query = "?utm_source=qa&utm_medium=social&utm_campaign=one%2Btwo&x=a&x=b+two&empty=&gclid=synthetic"
    html = redirect(target)
    result = execute(html, location: "https://unixwzrd.ai/s/abc/#{query}#section")
    assert_equal [target + query + "#section"], result.fetch("redirects")
    assert_empty result.fetch("commands")
    doc = Nokogiri::HTML(html)
    assert_equal target, doc.at_css('link[rel="canonical"]')["href"]
    assert_equal target, doc.at_css("a")["href"]
    assert_equal "0; url=#{target}", doc.at_css('meta[http-equiv="refresh"]')["content"]
    assert_equal "noindex", doc.at_css('meta[name="robots"]')["content"]
    assert_empty doc.css("script[src]")
  end

  def test_redirect_retains_configured_query_and_fragment
    target = "https://unixwzrd.ai/destination/?fixed=1#configured"
    result = execute(redirect(target), location: "https://unixwzrd.ai/s/abc/?x=2&x=3#incoming")
    assert_equal ["https://unixwzrd.ai/destination/?fixed=1&x=2&x=3#configured"], result.fetch("redirects")
    assert_equal [target], execute(redirect(target), location: "https://unixwzrd.ai/s/abc/").fetch("redirects")
  end

  def test_redirect_never_interpolates_incoming_parameters_into_html
    query = "?utm_content=%3C%2Fscript%3E%3Cscript%3Ebad()%3C%2Fscript%3E&empty="
    target = "https://unixwzrd.ai/destination/"
    assert_equal [target + query], execute(redirect(target), location: "https://unixwzrd.ai/s/abc/" + query).fetch("redirects")
  end

  def test_each_template_has_one_page_view_and_preserves_context_events
    source = File.read(File.join(ROOT, "html/_includes/google-analytics.html"))
    [%w[post /technology/example/], %w[project /projects/Example/], %w[page /projects/Example/], %w[home /], %w[page /404.html]].each do |layout, url|
      page = { "layout" => layout, "url" => url, "title" => "Audit", "category" => "technology", "tags" => ["ai"], "permalink" => url }
      html = Liquid::Template.parse(source).render!("page" => page, "site" => { "title" => "Audit", "google_analytics" => "G-OFFLINE-TEST" })
      result = execute(html)
      assert_one_page_view(result)
      config = result.fetch("commands").find { |command| command[0] == "config" }
      assert_equal "https://unixwzrd.ai/example/?utm_source=qa", config[2]["page_location"]
      assert_equal(layout == "post" || (layout == "page" && url.start_with?("/projects/")), config[2]["send_page_view"] == false)
    end
  end

  def test_analytics_title_is_a_safe_javascript_string
    title = "A title's \"quotes\", newline\n& </script><script>bad()</script>"
    source = File.read(File.join(ROOT, "html/_includes/google-analytics.html"))
    html = Liquid::Template.parse(source).render!("page" => { "layout" => "post", "title" => title }, "site" => { "google_analytics" => "G-OFFLINE-TEST" })
    result = execute(html)
    assert_one_page_view(result)
    config = result.fetch("commands").find { |command| command[0] == "config" }
    assert_equal title, config[2]["page_title"]
  end

  if ENV["ATTRIBUTION_SITE"]
    def test_generated_redirect_and_analytics_outputs
      site = File.expand_path(ENV.fetch("ATTRIBUTION_SITE"))
      redirects = JSON.parse(File.read(File.join(site, "redirects.json")))
      if ENV["ATTRIBUTION_BASELINE"]
        original = JSON.parse(File.read(File.join(ENV.fetch("ATTRIBUTION_BASELINE"), "redirects.json")))
        assert_equal original, redirects, "Existing redirect mappings changed"
      end
      redirects.each do |from, target|
        relative = from.delete_prefix("/")
        path = [File.join(site, relative, "index.html"), File.join(site, relative)].find { |candidate| File.file?(candidate) }
        refute_nil path, "Missing redirect output: #{from}"

        doc = Nokogiri::HTML(File.read(path))
        next unless doc.at_css('meta[http-equiv="refresh"]') # Case-only aliases may share a file on macOS.

        assert_equal target, doc.at_css('link[rel="canonical"]')["href"], from
        assert_equal "noindex", doc.at_css('meta[name="robots"]')["content"], from
        assert_empty doc.css('script[src*="googletagmanager"]'), from
        result = execute(doc.to_html, location: "https://unixwzrd.ai#{from}?utm_source=qa#section")
        expected = URI.parse(target)
        expected.query = [expected.query, "utm_source=qa"].compact.join("&")
        expected.fragment ||= "section"
        assert_equal [expected.to_s], result.fetch("redirects"), from
      end
      Dir.glob("#{site}/**/*.html").each do |path|
        doc = Nokogiri::HTML(File.read(path))
        next unless doc.at_css('script[src*="googletagmanager.com/gtag/js"]')

        inline = doc.css("script:not([src])").select { |script| script.text.include?("gtag('config'") }.map(&:to_html).join
        assert_one_page_view(execute(inline))
      end
    end
  end
end
