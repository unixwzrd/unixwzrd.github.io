#!/usr/bin/env ruby
# frozen_string_literal: true

# Rebuilds or injects `short_url` in post front matter from the same rules as
# html/_plugins/01_short_link_injector.rb (SHA256(short_link_origin + source path under html/)).
#
# Usage (from repo root):
#   bundle exec ruby scripts/backfill_short_url_front_matter.rb
#   bundle exec ruby scripts/backfill_short_url_front_matter.rb --dry-run
#   bundle exec ruby scripts/backfill_short_url_front_matter.rb --staged
#   bundle exec ruby scripts/backfill_short_url_front_matter.rb --check --staged
#   bundle exec ruby scripts/backfill_short_url_front_matter.rb html/_posts/foo.md ...
#
# Requires: bundle install (Jekyll and deps).

require "bundler/setup"
require "digest"
require "fileutils"
require "jekyll"
require "open3"
require "pathname"
require "set"

ROOT = File.expand_path("..", __dir__)
SOURCE = File.join(ROOT, "html")
DEST_SCRATCH = File.join(ROOT, ".jekyll_shortlink_backfill_dest")

def usage!
  warn <<~MSG
    usage: #{$PROGRAM_NAME} [--dry-run] [--check] [--staged] [path...]

      (no args)     update short_url for every post that needs it
      path...       only touch those files (paths relative to repo root, e.g. html/_posts/x.md)
      --staged      same as passing `git diff --cached --name-only` paths (pre-commit)
      --check       do not write; exit 1 if any targeted post has wrong/missing short_url
      --dry-run     print actions only
  MSG
  exit 64
end

def parse_argv(argv)
  opts = { dry_run: false, check: false, staged: false }
  paths = []
  argv.each do |a|
    case a
    when "--dry-run" then opts[:dry_run] = true
    when "--check" then opts[:check] = true
    when "--staged" then opts[:staged] = true
    when "--help", "-h" then usage!
    when /^-/
      warn "unknown option: #{a}"
      usage!
    else
      paths << a
    end
  end
  [opts, paths]
end

def git_staged_paths(root)
  out, status = Open3.capture2("git", "-C", root, "diff", "--cached", "--name-only", "--diff-filter=ACM")
  return [] unless status.success?

  out.lines.map(&:chomp).reject(&:empty?)
end

# Map repo-relative path to Jekyll source-relative path under html/.
def to_doc_relative(repo_path)
  p = repo_path.to_s.tr("\\", "/")
  return nil unless p.end_with?(".md")

  if p.start_with?("html/")
    rel = p.delete_prefix("html/")
    return rel if File.file?(File.join(SOURCE, rel))
  end
  if File.file?(File.join(ROOT, p))
    rel = Pathname.new(File.join(ROOT, p)).relative_path_from(Pathname.new(SOURCE)).to_s
    return rel if rel.end_with?(".md") && !rel.start_with?("..")
  end
  nil
end

def short_url_for(doc, origin)
  origin = origin.to_s.chomp("/")
  path = ShortLinkInjector.short_link_basis_path(doc)
  code = Digest::SHA256.hexdigest("#{origin}#{path}")[0, 10]
  "#{origin}/s/#{code}/"
end

def upsert_short_url_front_matter(content, url)
  line = "short_url: #{url.inspect}"
  if content.match(/^short_url:\s*/m)
    content.sub(/^short_url:\s*[^\r\n]*/, line)
  else
    content.sub(/\A(---\r?\n)/, "\\1#{line}\n")
  end
end

opts, path_args = parse_argv(ARGV)
if opts[:staged] && path_args.any?
  warn "#{$PROGRAM_NAME}: use either --staged or explicit paths, not both"
  exit 64
end
filter_rels =
  if opts[:staged]
    git_staged_paths(ROOT).filter_map { |p| to_doc_relative(p) }.to_set
  elsif path_args.any?
    path_args.filter_map { |p| to_doc_relative(p) }.to_set
  else
    nil
  end

Dir.chdir(ROOT) do
  FileUtils.rm_rf(DEST_SCRATCH)
  FileUtils.mkdir_p(DEST_SCRATCH)

  config = Jekyll.configuration(
    "source" => SOURCE,
    "destination" => DEST_SCRATCH,
    "incremental" => false,
    # Include future-dated posts so scheduled publishes get short_url updates.
    "future" => true,
    # Main _config.yml lives in repo root, not under html/
    "config" => File.join(ROOT, "_config.yml"),
  )

  site = Jekyll::Site.new(config)
  site.reset
  site.read
  ProjectPostPermalink.apply_to_site!(site)

  origin = config.fetch("short_link_origin", "https://unixwzrd.ai").to_s.chomp("/")

  code_to_rel = {}
  site.posts.docs.each do |doc|
    path = ShortLinkInjector.short_link_basis_path(doc)
    code = Digest::SHA256.hexdigest("#{origin}#{path}")[0, 10]
    rel = doc.relative_path
    if code_to_rel.key?(code) && code_to_rel[code] != rel
      warn "short_link: hash collision for /s/#{code}/ between #{code_to_rel[code]} and #{rel}"
      exit 1
    end
    code_to_rel[code] = rel
  end

  docs =
    if filter_rels
      if filter_rels.empty?
        []
      else
        site.posts.docs.select { |doc| filter_rels.include?(doc.relative_path) }
      end
    else
      site.posts.docs
    end

  mismatch = false

  docs.each do |doc|
    rel = doc.relative_path
    abs = File.join(SOURCE, rel)
    unless File.file?(abs)
      warn "skip missing #{abs}"
      next
    end

    url = short_url_for(doc, origin)
    raw = File.read(abs, encoding: "UTF-8")
    new_raw = upsert_short_url_front_matter(raw, url)

    if opts[:check]
      if new_raw != raw
        warn "short_url out of date: #{rel} (expected #{url})"
        mismatch = true
      end
      next
    end

    next if new_raw == raw

    if opts[:dry_run]
      puts "#{rel} -> #{url}"
    else
      File.write(abs, new_raw)
      puts "updated #{rel}"
    end
  end

  exit 1 if mismatch
end

