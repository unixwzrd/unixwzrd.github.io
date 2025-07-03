# frozen_string_literal: true

module Jekyll
  class CasePreservingPermalinks < Jekyll::Generator
    safe true
    priority :high

    def generate(site)
      # Process all posts that are in project directories
      site.posts.docs.each do |doc|
        # Check if this post is in a project directory
        # Path format: projects/ProjectName/_posts/filename.md
        path_parts = doc.relative_path.split('/')
        if path_parts.length >= 3 && path_parts[0] == 'projects' && path_parts[2] == '_posts'
          project_name = path_parts[1] # This preserves the original case

          # Set the project_name in the document's data
          doc.data['project_name'] = project_name

          # Generate the permalink with preserved case
          date = doc.date
          title = doc.data['title'] || doc.basename_without_ext
          title_slug = title.downcase.gsub(/[^a-z0-9]+/, '-').gsub(/^-+|-+$/, '')

          permalink = "/projects/#{project_name}/#{date.strftime('%Y')}/#{date.strftime('%m')}/#{date.strftime('%d')}/#{title_slug}/"
          doc.data['permalink'] = permalink
        end
      end
    end
  end
end 