# frozen_string_literal: true

require "pathname"
require "rouge"

module Jekyll
  module SourceCodeFilter
    def source_code_highlight(source_url, language = "text")
      site = @context.registers[:site]
      source_root = Pathname.new(site.source).realpath
      allowed_root = source_root.join("assets", "code").realpath
      relative_path = source_url.to_s.sub(%r{\A/+}, "")
      source_path = source_root.join(relative_path).realpath

      unless source_path.to_s.start_with?("#{allowed_root}#{File::SEPARATOR}")
        raise Jekyll::Errors::FatalException,
              "source_code_highlight may only read files below /assets/code/"
      end

      lexer = Rouge::Lexer.find_fancy(language.to_s, source_path.to_s) || Rouge::Lexers::PlainText
      Rouge::Formatters::HTML.new.format(lexer.lex(source_path.read))
    rescue Errno::ENOENT
      raise Jekyll::Errors::FatalException,
            "source_code_highlight file not found: #{source_url}"
    end
  end
end

Liquid::Template.register_filter(Jekyll::SourceCodeFilter)
