require "uri"

module NormalizeInternalLinks
  FILE_LIKE_PATH = /\.[a-zA-Z0-9]+$/
  INTERNAL_HREF = /(href=)(['"])(\/[^'"]*)\2/i

  module_function

  def normalize_target(raw_target)
    return raw_target if raw_target.nil? || raw_target.empty?
    return raw_target if raw_target.start_with?("//")

    path, fragment = raw_target.split("#", 2)
    path, query = path.split("?", 2)

    return raw_target unless canonical_directory_path?(path)

    normalized = "#{path}/"
    normalized += "?#{query}" if query && !query.empty?
    normalized += "##{fragment}" if fragment && !fragment.empty?
    normalized
  end

  def canonical_directory_path?(path)
    return false if path.nil? || path.empty? || path == "/"
    return false unless path.start_with?("/")
    return false if path.end_with?("/")
    return false if path.start_with?("/assets/")
    return false if ["/feed.xml", "/sitemap.xml", "/robots.txt", "/redirects.json"].include?(path)

    leaf = path.split("/").last
    return false if leaf.nil? || leaf.empty?
    return false if leaf.match?(FILE_LIKE_PATH)

    true
  end

  def normalize_output!(document)
    return unless document.output_ext == ".html"
    return if document.output.nil? || document.output.empty?

    document.output = document.output.gsub(INTERNAL_HREF) do
      prefix = Regexp.last_match(1)
      quote = Regexp.last_match(2)
      target = Regexp.last_match(3)
      "#{prefix}#{quote}#{normalize_target(target)}#{quote}"
    end
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_render do |document|
  NormalizeInternalLinks.normalize_output!(document)
end
