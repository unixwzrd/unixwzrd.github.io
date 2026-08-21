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
    configured_slug = doc.data["permalink_slug"].to_s.strip
    if configured_slug.empty?
      raise Jekyll::Errors::FatalException,
        "project post #{doc.relative_path} is missing immutable permalink_slug front matter"
    end

    title_slug = title_slugify(configured_slug)
    if configured_slug != title_slug
      raise Jekyll::Errors::FatalException,
        "project post #{doc.relative_path} has non-normalized permalink_slug #{configured_slug.inspect}; expected #{title_slug.inspect}"
    end

    "/projects/#{project_name}/#{date.strftime('%Y')}/#{date.strftime('%m')}/#{date.strftime('%d')}/#{title_slug}/"
  end

  def apply_to_site!(site)
    site.posts.docs.each do |doc|
      next unless project_post?(doc)

      path_parts = doc.relative_path.split("/")
      project_name = path_parts[1]
      doc.data["project_name"] = project_name
      doc.data["permalink"] = permalink_for_project_post(doc)
      add_legacy_redirect!(doc)
    end
  end

  def add_legacy_redirect!(doc)
    legacy = doc.data["legacy_project_permalink"].to_s.strip
    return if legacy.empty?

    unless legacy.start_with?("/") && legacy.end_with?("/")
      raise Jekyll::Errors::FatalException,
        "project post #{doc.relative_path} has invalid legacy_project_permalink #{legacy.inspect}"
    end

    redirects =
      case doc.data["redirect_from"]
      when nil then []
      when Array then doc.data["redirect_from"].dup
      else [doc.data["redirect_from"]]
      end
    redirects << legacy unless redirects.include?(legacy)
    doc.data["redirect_from"] = redirects
  end

  # Same slug rules as Jekyll-compatible "title from string" (matches previous CasePreserving behavior).
  def title_slugify(title)
    title.to_s.downcase.gsub(/[^a-z0-9]+/, "-").gsub(/^-+|-+$/, "")
  end
end
