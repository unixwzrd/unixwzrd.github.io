Jekyll::Hooks.register :pages, :pre_render do |page|
  # Initialize errors array if it doesn't exist
  Jekyll.instance_variable_set(:@permalink_errors, []) unless Jekyll.instance_variable_defined?(:@permalink_errors)
  errors = Jekyll.instance_variable_get(:@permalink_errors)

  # Skip validation for certain layouts, special pages, and system files
  next if ['home', 'default', 'redirect'].include?(page.data['layout'])
  next if page.name == '404.html' || page.path == '404.html' || page.path.end_with?('/404.html')  # Skip 404.html completely
  next if page.path.start_with?('assets/')
  next if ['feed.xml', 'sitemap.xml', 'redirects.json', 'robots.txt'].include?(page.name)
  next if page.path.end_with?('.scss', '.css', '.map', '.liquid', '.xml')
  next if page.path.include?('_includes/') || page.path.include?('_layouts/') || page.path.include?('_archives/')
  next if page.path.include?('_posts/') # Skip blog posts as they use date-based permalinks

  # Collect all errors for this page
  page_errors = []

  # Check if permalink is present
  if !page.data['permalink']
    page_errors << "Missing permalink"
  else
    # Validate permalink format
    if !page.data['permalink'].start_with?('/')
      page_errors << "Permalink must start with /"
    end
    if !page.data['permalink'].end_with?('/')
      page_errors << "Permalink must end with /"
    end
  end

  # If there are any errors for this page, add them to the main errors list
  if !page_errors.empty?
    errors << "#{page.path}:\n    - #{page_errors.join("\n    - ")}"
  end
end

Jekyll::Hooks.register :site, :post_write do |site|
  errors = Jekyll.instance_variable_get(:@permalink_errors)
  if errors && !errors.empty?
    Jekyll.logger.error "Permalink Validation Errors:", "\n#{errors.join("\n")}"
    Jekyll.logger.error "\nFound #{errors.length} files with permalink errors"
    Jekyll.logger.error "Please fix these issues and try again"
    raise "Build failed due to permalink validation errors"
  end
end
