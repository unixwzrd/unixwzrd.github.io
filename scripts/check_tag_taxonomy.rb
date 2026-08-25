#!/usr/bin/env ruby
# frozen_string_literal: true

require "bundler/setup"
require "jekyll"
require_relative "../html/_plugins/03_tag_taxonomy_validator"

root = File.expand_path("..", __dir__)
config = Jekyll.configuration(
  "source" => File.join(root, "html"),
  "destination" => File.join(root, ".jekyll_tag_taxonomy_check"),
  "config" => File.join(root, "_config.yml"),
  "future" => true,
  "quiet" => true,
)

site = Jekyll::Site.new(config)
site.reset
site.read
Jekyll::TagTaxonomyValidator.new.generate(site)

puts "tag taxonomy: #{site.posts.docs.size} published and scheduled posts valid"
