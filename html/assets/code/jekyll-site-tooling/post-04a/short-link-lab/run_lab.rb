#!/usr/bin/env ruby
# frozen_string_literal: true

# Tiny stand-ins let the unchanged site module run without Jekyll gems.
module Jekyll
  class QuietLogger
    def error(*)
    end
  end

  def self.logger
    @logger ||= QuietLogger.new
  end

  module Errors
    class FatalException < StandardError; end
  end
end

require_relative "source/01_short_link_injector"

Post = Struct.new(:relative_path, :data)
PostCollection = Struct.new(:docs)
Site = Struct.new(:config, :posts, :pages)

ORIGIN = "https://site.example"
ORIGINAL_PATH = "_posts/2026-10-15-example.md"
MOVED_PATH = "_posts/series/example/2026-10-15-example.md"
FROZEN_BASIS = "/_posts/2026-10-15-example.md"

def inject(post)
  site = Site.new({ "short_link_origin" => ORIGIN }, PostCollection.new([post]), [])
  ShortLinkInjector.inject!(site)
  post.data.fetch("short_url")
end

def check(condition, label)
  raise "FAIL #{label}" unless condition

  puts "PASS #{label}"
end

before = Post.new(ORIGINAL_PATH, { "short_link_basis" => FROZEN_BASIS })
after = Post.new(MOVED_PATH, { "short_link_basis" => FROZEN_BASIS })
original_url = inject(before)
moved_url = inject(after)
check(original_url == moved_url && before.data.fetch("redirect_from") == after.data.fetch("redirect_from"), "frozen basis survives source move")

fallback_before = inject(Post.new(ORIGINAL_PATH, {}))
fallback_after = inject(Post.new(MOVED_PATH, {}))
check(fallback_before != fallback_after, "source-path fallback changes after move")

wrong = Post.new(MOVED_PATH, { "short_link_basis" => FROZEN_BASIS, "short_url" => "#{ORIGIN}/s/0000000000/" })
begin
  inject(wrong)
  raise "FAIL mismatched declared short_url was accepted"
rescue Jekyll::Errors::FatalException => error
  check(error.message.include?("short_url front matter does not match"), "mismatched declared short_url is rejected")
end

puts "Invented stable URL: #{original_url}"
