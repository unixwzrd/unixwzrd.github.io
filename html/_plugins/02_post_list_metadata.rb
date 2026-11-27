# frozen_string_literal: true

# Sets `list_date` and `list_sort_key` on each post for discovery-list sorting.
# Discovery lists always use the original publication date, never an edit or
# release-notice date. Series indexes, tag pages, and permalinks are unaffected.
#
# list_sort_key is a zero-padded inverted epoch string so Liquid's `sort` filter
# (lexicographic) yields newest-first when sorted ascending.
module PostListMetadata
  LIST_SORT_EPOCH_MAX = 9_999_999_999_999

  module_function

  def apply!(site)
    site.posts.docs.each do |post|
      apply_to_post!(post)
    end
  end

  def apply_to_post!(post)
    list_date = list_date_for(post)
    post.data["list_date"] = list_date
    post.data["list_sort_key"] = list_sort_key_for(post, list_date)
  end

  def list_date_for(doc)
    coerce_time(doc.data["date"] || doc.date)
  end

  def list_sort_key_for(doc, list_date)
    time = coerce_time(list_date)
    return format("%013d", LIST_SORT_EPOCH_MAX) unless time

    seq = doc.data["sequence"]
    seq = seq.nil? ? 500 : seq.to_i
    composite = (time.to_i * 1000) + (1000 - seq)
    inverted = LIST_SORT_EPOCH_MAX - composite
    format("%013d", inverted)
  end

  def coerce_time(value)
    return nil if value.nil?

    return value.to_time if value.respond_to?(:to_time)

    Time.parse(value.to_s)
  rescue ArgumentError
    nil
  end
end

module Jekyll
  class PostListMetadataGenerator < Jekyll::Generator
    safe true
    priority :lowest

    def generate(site)
      PostListMetadata.apply!(site)
    end
  end
end

