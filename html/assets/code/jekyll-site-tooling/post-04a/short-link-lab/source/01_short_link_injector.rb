# frozen_string_literal: true

require "digest"

# Deterministic short links: /s/<10 hex>/ merged into each eligible item's
# `redirect_from`. Posts are eligible by default; pages opt in with
# `short_link: true` (or an existing `short_url`).
# (consumed by jekyll-redirect-from). Invoked from CasePreservingPermalinks#generate
# so it always runs after permalinks are set and before JekyllRedirectFrom::Generator.
#
# Hash input: short_link_origin + `short_link_basis`. If the immutable basis is
# absent, the source path under the site root remains the compatibility fallback.
module ShortLinkInjector
  extend self

  DEFAULT_ORIGIN = "https://unixwzrd.ai".freeze

  def inject!(site)
    origin = site.config.fetch("short_link_origin", DEFAULT_ORIGIN).to_s.chomp("/")
    code_to_item = {}

    items(site).each do |item|
      path = short_link_basis_path(item)
      digest = Digest::SHA256.hexdigest("#{origin}#{path}")
      code = digest[0, 10]
      short_path = "/s/#{code}/"
      label = item_label(item)

      if code_to_item.key?(code) && code_to_item[code] != label
        Jekyll.logger.error(
          "ShortLinkInjector:",
          "collision: code #{code} for #{label} and #{code_to_item[code]}",
        )
        raise Jekyll::Errors::FatalException, "short_link: hash collision for /s/#{code}/"
      end
      code_to_item[code] = label

      expected_short_url = "#{origin}#{short_path}"
      if item.data["short_url"] && !item.data["short_url"].to_s.strip.empty?
        unless short_url_matches?(item.data["short_url"].to_s, origin, code)
          Jekyll.logger.error(
            "ShortLinkInjector:",
            "short_url mismatch in #{label}: expected #{expected_short_url}, got #{item.data['short_url']}",
          )
          raise Jekyll::Errors::FatalException, "short_url front matter does not match computed short URL"
        end
      end
      item.data["short_url"] = expected_short_url

      existing = item.data["redirect_from"]
      list =
        case existing
        when nil then []
        when Array then existing.dup
        else [existing]
        end
      list << short_path unless list.include?(short_path)
      item.data["redirect_from"] = list
    end
  end

  def items(site)
    pages = site.pages.select { |page| page_short_link_enabled?(page) }
    site.posts.docs + pages
  end

  def page_short_link_enabled?(page)
    page.data["short_link"] == true || !page.data["short_url"].to_s.strip.empty?
  end

  # @param item [Jekyll::Document, Jekyll::Page]
  # @return [String] path starting with /, no trailing slash (e.g. /_posts/foo.md)
  def short_link_basis_path(item)
    configured = item.data["short_link_basis"].to_s.strip
    return validate_basis!(configured, item) unless configured.empty?

    rel = item.relative_path.to_s.tr("\\", "/").delete_prefix("/")
    validate_basis!("/#{rel}", item)
  end

  def validate_basis!(basis, item)
    normalized = basis.to_s.tr("\\", "/")
    invalid = !normalized.start_with?("/") || normalized.end_with?("/") ||
      normalized.include?("?") || normalized.include?("#") ||
      normalized.split("/").include?("..")
    return normalized unless invalid

    label = item_label(item)
    Jekyll.logger.error "ShortLinkInjector:", "invalid short_link_basis in #{label}: #{basis.inspect}"
    raise Jekyll::Errors::FatalException, "short_link_basis must be a source-like absolute path"
  end

  def item_label(item)
    item.relative_path.to_s.tr("\\", "/")
  end

  def short_url_matches?(raw, origin, code)
    s = raw.to_s.strip.sub(%r{/+\z}, "").downcase
    expected = "#{origin}/s/#{code}".sub(%r{/+\z}, "").downcase
    s == expected
  end
end
