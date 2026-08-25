#!/usr/bin/env ruby
# frozen_string_literal: true

require "yaml"

root = File.expand_path("..", __dir__)
taxonomy_path = File.join(root, "html", "_data", "tag_taxonomy.yml")
taxonomy = YAML.safe_load_file(taxonomy_path)
settings = taxonomy.fetch("settings", {})
tags = taxonomy.fetch("tags")

puts "Canonical blog tags"
puts "Recommended per post: #{settings.fetch('recommended_min_tags', 2)}-#{settings.fetch('recommended_max_tags', 6)}"

taxonomy.fetch("groups").each do |group|
  puts "\n#{group.fetch('label')}"
  tags.select { |tag| tag.fetch("group") == group.fetch("id") }.each do |tag|
    puts "  #{tag.fetch('id')}"
  end
end

puts "\nArticle types (use content_type, not tags)"
taxonomy.fetch("content_types").each do |content_type|
  puts "  #{content_type.fetch('id')}"
end
