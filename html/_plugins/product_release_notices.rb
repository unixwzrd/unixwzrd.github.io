# frozen_string_literal: true

# Release selection is explicit: never guess shipping status from a title,
# content_type, edited date, or a preview build's --unpublished/--future flags.
module ProductReleaseNotices
  module_function

  def project_for(post)
    return unless ProjectPostPermalink.project_post?(post)

    post.relative_path.split("/")[1]
  end

  def public_post?(post, site)
    post.data["published"] != false && !post.data["draft"] && !post.data["list_exclude"] &&
      !post.relative_path.split("/").include?("_drafts") &&
      !post.relative_path.include?("social-posts") && post.date <= site.time
  end

  def apply!(site)
    projects = site.posts.docs.group_by { |post| project_for(post) }
    projects.each do |project, posts|
      next unless project

      # Clear derived data on watched rebuilds, including when a release is withdrawn.
      posts.each { |post| post.data.delete("newer_release") }
      catalog = site.data.dig("github_projects", "projects") || []
      next if catalog.any? { |entry| entry["name"] == project && entry["visibility"] == "none" }

      release = posts.select do |post|
        public_post?(post, site) && post.data["release_status"] == "released" &&
          !post.data["release_version"].to_s.strip.empty?
      end.max_by { |post| [post.date, post.relative_path] }
      next unless release

      overview = "/projects/#{project}/"
      next unless site.pages.any? { |page| page.url == overview }

      details = {
        "version" => release.data["release_version"].to_s,
        "date" => release.date,
        "url" => release.url,
        "overview_url" => overview,
        "summary" => release.data["release_summary"] || release.data["excerpt"],
      }
      posts.each do |post|
        next unless public_post?(post, site) && post.date < release.date
        next if post.data["release_notice"] == false
        next unless post.data["release_version"] || post.data["release_notice"] == true ||
          %w[release update introduction].include?(post.data["content_type"])
        next if post.data["release_version"].to_s == details["version"]

        post.data["newer_release"] = details
      end
    end
  end
end

module Jekyll
  class ProductReleaseNoticesGenerator < Generator
    safe true
    priority :low

    def generate(site)
      ProductReleaseNotices.apply!(site)
    end
  end
end

