# frozen_string_literal: true

module Jekyll
  class CasePreservingPermalinks < Jekyll::Generator
    safe true
    priority :high

    def generate(site)
      ProjectPostPermalink.apply_to_site!(site)
      ShortLinkInjector.inject!(site)
    end
  end
end

