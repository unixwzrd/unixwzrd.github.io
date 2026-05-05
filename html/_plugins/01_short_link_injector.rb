# frozen_string_literal: true

require "digest"

# Deterministic short links: /s/<10 hex>/ merged into each post's `redirect_from`
# (consumed by jekyll-redirect-from). Invoked from CasePreservingPermalinks#generate
# so it always runs after permalinks are set and before JekyllRedirectFrom::Generator.
#
# Hash input: short_link_origin + the post's source path under the site root
# (e.g. /projects/Foo/_posts/2026-01-01-slug.md). Edits to title, date, slug, or
# permalink do not change the code; renaming/moving the .md file does.
module ShortLinkInjector
  extend self

  DEFAULT_ORIGIN = "https://unixwzrd.ai".freeze

  def inject!(site)
    origin = site.config.fetch("short_link_origin", DEFAULT_ORIGIN).to_s.chomp("/")
    code_to_doc = {}

    site.posts.docs.each do |doc|
      path = short_link_basis_path(doc)
      digest = Digest::SHA256.hexdigest("#{origin}#{path}")
      code = digest[0, 10]
      short_path = "/s/#{code}/"

      if code_to_doc.key?(code) && code_to_doc[code] != doc.relative_path
        Jekyll.logger.error(
          "ShortLinkInjector:",
          "collision: code #{code} for #{doc.relative_path} and #{code_to_doc[code]}",
        )
        raise Jekyll::Errors::FatalException, "short_link: hash collision for /s/#{code}/"
      end
      code_to_doc[code] = doc.relative_path

      expected_short_url = "#{origin}#{short_path}"
      if doc.data["short_url"] && !doc.data["short_url"].to_s.strip.empty?
        unless short_url_matches?(doc.data["short_url"].to_s, origin, code)
          Jekyll.logger.error(
            "ShortLinkInjector:",
            "short_url mismatch in #{doc.relative_path}: expected #{expected_short_url}, got #{doc.data['short_url']}",
          )
          raise Jekyll::Errors::FatalException, "short_url front matter does not match computed short URL"
        end
      end

      existing = doc.data["redirect_from"]
      list =
        case existing
        when nil then []
        when Array then existing.dup
        else [existing]
        end
      list << short_path unless list.include?(short_path)
      doc.data["redirect_from"] = list
    end
  end

  # @param doc [Jekyll::Document]
  # @return [String] path starting with /, no trailing slash (e.g. /_posts/foo.md)
  def short_link_basis_path(doc)
    rel = doc.relative_path.to_s.tr("\\", "/").delete_prefix("/")
    "/#{rel}"
  end

  def short_url_matches?(raw, origin, code)
    s = raw.to_s.strip.sub(%r{/+\z}, "").downcase
    expected = "#{origin}/s/#{code}".sub(%r{/+\z}, "").downcase
    s == expected
  end
end

