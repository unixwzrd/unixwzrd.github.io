#!/usr/bin/env ruby
# frozen_string_literal: true

# Does not start a listener, build the site, or stop an existing server.
require "bundler/setup"
require "jekyll"
require "minitest/autorun"
require "open3"
require "tmpdir"
require_relative "../html/_plugins/set_production_url"

class JekyllSiteTest < Minitest::Test
  ROOT = File.expand_path("..", __dir__)
  SCRIPT = File.join(ROOT, "utils/bin/jekyll-site")

  def test_wrapper_syntax_help_and_invalid_lan_arguments
    output, status = Open3.capture2e("bash", "-n", SCRIPT)
    assert status.success?, output
    output, status = Open3.capture2e("bash", SCRIPT, "--help")
    assert status.success?, output
    assert_includes output, "--lan HOST"
    [[], ["--current"], ["http://10.0.0.67"], ["10.0.0.67:4000"]].each do |args|
      output, status = Open3.capture2e("bash", SCRIPT, "restart", "--lan", *args)
      refute status.success?, output
      assert_includes output, "--lan requires"
      refute_includes output, "Stopping Jekyll-site"
    end
  end

  def test_preview_and_current_modes_preserve_the_requested_bind_and_public_host
    function = File.read(SCRIPT)[/^start_service\(\) \{\n.*?^\}/m]
    refute_nil function
    Dir.mktmpdir("jekyll-wrapper-test-") do |dir|
      [false, true].product(["", "10.0.0.67", "xanax.local"]).each do |current, host|
        harness = <<~BASH
          BASE_DIR="$1"
          pid_file="$2/pid"
          check_running() { return 1; }
          check_port_in_use() { return 1; }
          site_build() { :; }
          bundle() { printf 'ENV=%s URL=%s ARGS=' "$JEKYLL_ENV" "$JEKYLL_PREVIEW_URL"; printf '<%s>' "$@"; printf '\\n'; }
          #{function}
          start_service true false "$3" "$4"
          wait
        BASH
        output, status = Open3.capture2e("bash", "-c", harness, "wrapper-test", ROOT, dir, current.to_s, host)
        assert status.success?, output
        assert_includes output, "ENV=development URL=#{host.empty? ? '' : "http://#{host}:4000"} ARGS="
        assert_includes output, "<--host><#{host.empty? ? 'localhost' : '0.0.0.0'}><--port><4000>"
        %w[--future --drafts --unpublished].each do |flag|
          current ? refute_includes(output, "<#{flag}>") : assert_includes(output, "<#{flag}>")
        end
      end
    end
  end

  def test_preview_url_override_is_development_only_and_production_stays_canonical
    original = ENV.to_h.slice("JEKYLL_ENV", "JEKYLL_PREVIEW_URL")
    cases = [
      ["development", "", "http://localhost:4000", "http://localhost:4000"],
      ["development", "http://10.0.0.67:4000", "http://0.0.0.0:4000", "http://10.0.0.67:4000"],
      ["production", "http://10.0.0.67:4000", "http://0.0.0.0:4000", "https://unixwzrd.ai"],
      ["production", "http://10.0.0.67:4000", "https://unixwzrd.ai", "https://unixwzrd.ai"],
    ]
    cases.each do |environment, preview, initial, expected|
      ENV["JEKYLL_ENV"] = environment
      ENV["JEKYLL_PREVIEW_URL"] = preview
      site = Struct.new(:config).new({ "url" => initial })
      Jekyll::Hooks.trigger :site, :after_init, site
      assert_equal expected, site.config["url"]
    end
  ensure
    %w[JEKYLL_ENV JEKYLL_PREVIEW_URL].each do |name|
      original.key?(name) ? ENV[name] = original[name] : ENV.delete(name)
    end
  end
end

