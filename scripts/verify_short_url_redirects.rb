#!/usr/bin/env ruby
# frozen_string_literal: true

# Verifies _site/s/<code>/index.html exists for each published eligible item.
# Run after `jekyll build` (without --future). Future-dated posts are excluded
# because Jekyll does not emit them or their redirects until publish day.
#
# Usage (from repo root):
#   bundle exec ruby scripts/verify_short_url_redirects.rb
#   JEKYLL_DESTINATION=/tmp/site JEKYLL_FUTURE=true bundle exec ruby scripts/verify_short_url_redirects.rb

require "bundler/setup"
require "digest"
require "fileutils"
require "jekyll"

ROOT = File.expand_path("..", __dir__)
SOURCE = File.join(ROOT, "html")
DEST = File.expand_path(ENV.fetch("JEKYLL_DESTINATION", File.join(ROOT, "_site")), ROOT)
INCLUDE_FUTURE = ENV["JEKYLL_FUTURE"] == "true"

Dir.chdir(ROOT) do
  config = Jekyll.configuration(
    "source" => SOURCE,
    "destination" => DEST,
    "future" => INCLUDE_FUTURE,
    "config" => File.join(ROOT, "_config.yml"),
  )

  site = Jekyll::Site.new(config)
  site.reset
  site.read
  ProjectPostPermalink.apply_to_site!(site)

  origin = site.config.fetch("short_link_origin", "https://unixwzrd.ai").to_s.chomp("/")
  missing = []

  ShortLinkInjector.items(site).each do |doc|
    raw = doc.data["short_url"]
    next if raw.nil? || raw.to_s.strip.empty?

    path = ShortLinkInjector.short_link_basis_path(doc)
    code = Digest::SHA256.hexdigest("#{origin}#{path}")[0, 10]
    redirect = File.join(DEST, "s", code, "index.html")
    url = "#{origin}/s/#{code}/"

    next if File.file?(redirect)

    rel = "html/#{doc.relative_path}"
    missing << "#{url} from #{rel} missing #{redirect.sub("#{ROOT}/", "")}"
  end

  if missing.any?
    warn "Missing generated short URL redirects:\n#{missing.join("\n")}"
    exit 1
  end
end
