module Jekyll
  module EmailObfuscationFilter
    def encode_email(addr)
      addr.chars.map { |char| encode_email_char(char) }.join("")
    end

    def encode_email_char(char)
      ["&#"  + char.ord.to_s + ";", "&#x" + char.ord.to_s(16) + ";", char].sample
    end
  end
end

Liquid::Template.register_filter(Jekyll::EmailObfuscationFilter)