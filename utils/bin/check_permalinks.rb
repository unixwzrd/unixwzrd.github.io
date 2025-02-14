#!/usr/bin/env ruby

require 'yaml'

def check_front_matter(file_path)
  errors = []
  begin
    content = File.read(file_path)
    if content.start_with?('---')
      # Extract front matter
      front_matter = content.split('---')[1]
      if front_matter
        # Add Time class to YAML safe_load
        data = YAML.safe_load(front_matter, permitted_classes: [Time])
        
        # Skip certain files
        return [] if ['home', 'default'].include?(data['layout'])
        return [] if file_path.end_with?('404.html')
        return [] if file_path.start_with?('assets/')
        return [] if ['feed.xml', 'sitemap.xml', 'redirects.json', 'robots.txt'].include?(File.basename(file_path))
        return [] if file_path.end_with?('.scss', '.css', '.map', '.liquid')
        return [] if file_path.include?('_includes/') || file_path.include?('_layouts/')
        
        # Skip blog posts (they use date-based permalinks)
        return [] if data['layout'] == 'post'
        
        # Check permalink
        if !data['permalink']
          errors << "Missing permalink"
        else
          permalink = data['permalink']
          errors << "Permalink must start with /" unless permalink.start_with?('/')
          errors << "Permalink must end with /" unless permalink.end_with?('/')
        end
      end
    end
  rescue => e
    errors << "Error parsing file: #{e.message}"
  end
  errors
end

def main
  html_dir = File.join(Dir.pwd, 'html')
  all_errors = {}

  # Find all markdown and HTML files
  files = Dir.glob("#{html_dir}/**/*.{md,html}")
  
  files.each do |file|
    relative_path = file.sub("#{html_dir}/", '')
    errors = check_front_matter(file)
    all_errors[relative_path] = errors if errors.any?
  end

  if all_errors.any?
    puts "\nPermalink Validation Errors:"
    all_errors.each do |file, errors|
      puts "\n#{file}:"
      errors.each { |error| puts "    - #{error}" }
    end
    puts "\nFound #{all_errors.length} files with permalink errors"
    exit 1
  else
    puts "No permalink errors found"
    exit 0
  end
end

main 