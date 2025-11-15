module DtsSiteUrl
  DESIRED_URL = "https://unixwzrd.ai".freeze

  Jekyll::Hooks.register :site, :after_init do |site|
    env = ENV["JEKYLL_ENV"].to_s
    next unless env == "production"

    current = site.config["url"].to_s
    needs_override =
      current.empty? ||
      current.include?("localhost") ||
      current.include?("0.0.0.0") ||
      current.include?("127.0.0.1")

    if needs_override
      Jekyll.logger.info("site.url", "Overriding '#{current}' with '#{DESIRED_URL}' for production build")
      site.config["url"] = DESIRED_URL
    end
  end
end

