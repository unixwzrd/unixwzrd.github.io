Jekyll::Hooks.register :pages, :pre_render do |page|
  # Skip validation for certain layouts if needed
  return if ['home', 'default'].include?(page.data['layout'])

  # Check if permalink is present and properly formatted
  if !page.data['permalink']
    Jekyll.logger.error "Permalink Error:", "Missing permalink in #{page.path}"
    raise "Missing permalink in #{page.path}"
  end

  # Ensure permalink starts with /
  if !page.data['permalink'].start_with?('/')
    Jekyll.logger.error "Permalink Error:", "Permalink must start with / in #{page.path}"
    raise "Permalink must start with / in #{page.path}"
  end

  # Ensure permalink ends with /
  if !page.data['permalink'].end_with?('/')
    Jekyll.logger.error "Permalink Error:", "Permalink must end with / in #{page.path}"
    raise "Permalink must end with / in #{page.path}"
  end
end 