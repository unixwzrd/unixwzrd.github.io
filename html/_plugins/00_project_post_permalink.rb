# frozen_string_literal: true

# Shared rules for project-scoped posts under html/projects/<Name>/_posts/.
# Loaded first (00_ prefix) for CasePreservingPermalinks and backfill_short_url_front_matter.rb
module ProjectPostPermalink
  module_function

  def project_post?(doc_or_relative_path)
    parts =
      if doc_or_relative_path.respond_to?(:relative_path)
        doc_or_relative_path.relative_path.split("/")
      else
        doc_or_relative_path.to_s.split("/")
      end
    parts.length >= 3 && parts[0] == "projects" && parts[2] == "_posts"
  end

  # @param doc [Jekyll::Document] post document
  # @return [String, nil] permalink path with leading/trailing slashes, or nil if not a project post
  def permalink_for_project_post(doc)
    return nil unless project_post?(doc)

    path_parts = doc.relative_path.split("/")
    project_name = path_parts[1]
    date = doc.date
    title = doc.data["title"] || doc.basename_without_ext
    slug_source = doc.data["slug"].to_s.strip
    slug_source = title if slug_source.empty?
    title_slug = title_slugify(slug_source)

    "/projects/#{project_name}/#{date.strftime('%Y')}/#{date.strftime('%m')}/#{date.strftime('%d')}/#{title_slug}/"
  end

  def apply_to_site!(site)
    site.posts.docs.each do |doc|
      next unless project_post?(doc)

      path_parts = doc.relative_path.split("/")
      project_name = path_parts[1]
      doc.data["project_name"] = project_name
      doc.data["permalink"] = permalink_for_project_post(doc)
    end
  end

  # Same slug rules as Jekyll-compatible "title from string" (matches previous CasePreserving behavior).
  def title_slugify(title)
    title.to_s.downcase.gsub(/[^a-z0-9]+/, "-").gsub(/^-+|-+$/, "")
  end
end

