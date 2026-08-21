#!/usr/bin/env ruby
# frozen_string_literal: true

# Verifies every published project post has its frozen canonical output and
# every declared legacy project permalink has a generated redirect page.
# Run after Jekyll writes _site.

require "bundler/setup"
require "jekyll"

ROOT = File.expand_path("..", __dir__)
SOURCE = File.join(ROOT, "html")
DEST = File.expand_path(ENV.fetch("JEKYLL_DESTINATION", File.join(ROOT, "_site")), ROOT)
INCLUDE_FUTURE = ENV["JEKYLL_FUTURE"] == "true"

def output_file(path)
  File.join(DEST, path.delete_prefix("/"), "index.html")
end

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

  missing = []
  site.posts.docs.select { |doc| ProjectPostPermalink.project_post?(doc) }.each do |doc|
    canonical = doc.data.fetch("permalink")
    canonical_file = output_file(canonical)
    unless File.file?(canonical_file)
      missing << "canonical #{canonical} from html/#{doc.relative_path} missing #{canonical_file.sub("#{ROOT}/", "")}"
    end

    legacy = doc.data["legacy_project_permalink"].to_s.strip
    next if legacy.empty?

    redirect_file = output_file(legacy)
    unless File.file?(redirect_file)
      missing << "redirect #{legacy} from html/#{doc.relative_path} missing #{redirect_file.sub("#{ROOT}/", "")}"
      next
    end

    redirect_html = File.read(redirect_file, encoding: "UTF-8")
    unless redirect_html.include?(canonical)
      missing << "redirect #{legacy} does not target canonical #{canonical}"
    end
  end

  if missing.any?
    warn "Missing project permalink outputs:\n#{missing.join("\n")}"
    exit 1
  end
end
