module Jekyll
  module StripImagesFilter
    def strip_images(input)
      # Remove Markdown images: ![alt](url)
      output = input.gsub(/!\[.*?\]\(.*?\)/, '')
      # Remove HTML images: <img ...>
      output = output.gsub(/<img.*?>/, '')
      output
    end
  end
end

Liquid::Template.register_filter(Jekyll::StripImagesFilter) 