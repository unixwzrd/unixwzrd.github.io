# frozen_string_literal: true

require "cgi"
require "nokogiri"

module Jekyll
  module ArticleTocFilter
    # Read Kramdown's IDs from rendered article HTML without modifying anchors.
    def article_toc(html)
      fragment = Nokogiri::HTML.fragment(html.to_s)
      entries = []
      parent = nil
      fragment.css("h2[id], h3[id]").each do |heading|
        next if heading["id"].strip.empty?
        next if heading.ancestors.any? { |node| %w[details blockquote nav figure].include?(node.name) }

        entry = { id: heading["id"], text: heading.text.strip, children: [] }
        if heading.name == "h3" && parent
          parent[:children] << entry
        else
          entries << entry
          parent = entry if heading.name == "h2"
        end
      end
      return "" if entries.empty?

      '<details class="post-toc" data-pagefind-ignore="all">' \
        '<summary>On this page</summary><nav aria-label="On this page">' \
        "#{article_toc_list(entries)}</nav></details>"
    end

    private

    def article_toc_list(entries)
      items = entries.map do |entry|
        children = entry[:children].empty? ? "" : article_toc_list(entry[:children])
        %(<li><a href="##{CGI.escapeHTML(entry[:id])}">#{CGI.escapeHTML(entry[:text])}</a>#{children}</li>)
      end
      "<ul>#{items.join}</ul>"
    end
  end
end

Liquid::Template.register_filter(Jekyll::ArticleTocFilter)

# Prepare navigation after Markdown conversion and before layouts are rendered.
# An older watcher without this hook simply has no prepared contents to display;
# the layout never calls an unavailable filter, even with strict_filters enabled.
Jekyll::Hooks.register :documents, :post_convert do |document|
  document.data["article_toc"] = if document.data["toc"] == true
                                   Object.new.extend(Jekyll::ArticleTocFilter).article_toc(document.content)
                                 end
end
