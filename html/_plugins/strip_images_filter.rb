module Jekyll
  module StripImagesFilter
    def strip_images(input)
      # Remove Markdown images: ![alt](url)
      output = input.gsub(/!\[.*?\]\(.*?\)/, '')
      # Remove HTML images: <img ...>
      output = output.gsub(/<img.*?>/, '')
      # Remove Markdown links: [text](url) - keep just the text
      output = output.gsub(/\[([^\]]+)\]\([^)]+\)/, '\1')
      # Remove HTML links: <a href="...">text</a> - keep just the text
      output = output.gsub(/<a[^>]*>(.*?)<\/a>/, '\1')
      output
    end
  end
end

Liquid::Template.register_filter(Jekyll::StripImagesFilter) 