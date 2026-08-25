# frozen_string_literal: true

require "set"

module Jekyll
  class TagTaxonomyValidator < Generator
    safe true
    priority :highest

    def generate(site)
      taxonomy = site.data["tag_taxonomy"]
      raise Errors::FatalException, "tag taxonomy: missing _data/tag_taxonomy.yml" unless taxonomy

      groups = Array(taxonomy["groups"])
      tags = Array(taxonomy["tags"])
      content_types = Array(taxonomy["content_types"])

      group_ids = unique_ids!(groups, "group")
      tag_ids = unique_ids!(tags, "tag")
      content_type_ids = unique_ids!(content_types, "content type")
      aliases = {}

      tags.each do |tag|
        group = tag["group"].to_s
        unless group_ids.include?(group)
          raise Errors::FatalException,
            "tag taxonomy: #{tag['id'].inspect} references unknown group #{group.inspect}"
        end

        Array(tag["aliases"]).each do |alias_id|
          register_alias!(aliases, tag_ids, alias_id, tag.fetch("id"))
        end
      end

      content_types.each do |content_type|
        Array(content_type["source_tags"]).each do |source_tag|
          register_alias!(aliases, tag_ids, source_tag, "content_type:#{content_type.fetch('id')}")
        end
      end

      errors = []
      site.posts.docs.each do |post|
        label = post.relative_path
        post_tags = Array(post.data["tags"]).map(&:to_s)

        duplicate_tags = post_tags.group_by(&:itself).select { |_tag, values| values.size > 1 }.keys
        errors << "#{label}: duplicate tags #{duplicate_tags.join(', ')}" if duplicate_tags.any?

        post_tags.each do |tag|
          next if tag_ids.include?(tag)

          if aliases.key?(tag)
            errors << "#{label}: tag #{tag.inspect} is an alias; use #{aliases.fetch(tag).inspect}"
          else
            errors << "#{label}: unknown tag #{tag.inspect}; add it to _data/tag_taxonomy.yml first"
          end
        end

        content_type = post.data["content_type"].to_s
        if !content_type.empty? && !content_type_ids.include?(content_type)
          errors << "#{label}: unknown content_type #{content_type.inspect}"
        end
      end

      return if errors.empty?

      errors.each { |error| Jekyll.logger.error "TagTaxonomy:", error }
      raise Errors::FatalException, "tag taxonomy validation failed with #{errors.size} error(s)"
    end

    private

    def unique_ids!(entries, kind)
      ids = entries.map { |entry| entry["id"].to_s }
      missing = ids.count(&:empty?)
      duplicates = ids.group_by(&:itself).select { |_id, values| values.size > 1 }.keys

      raise Errors::FatalException, "tag taxonomy: #{missing} #{kind}(s) missing an id" if missing.positive?
      unless duplicates.empty?
        raise Errors::FatalException, "tag taxonomy: duplicate #{kind} ids: #{duplicates.join(', ')}"
      end

      ids.to_set
    end

    def register_alias!(aliases, canonical_ids, alias_id, target)
      alias_id = alias_id.to_s
      if alias_id.empty? || canonical_ids.include?(alias_id)
        raise Errors::FatalException, "tag taxonomy: invalid alias #{alias_id.inspect} for #{target.inspect}"
      end
      if aliases.key?(alias_id) && aliases[alias_id] != target
        raise Errors::FatalException,
          "tag taxonomy: alias #{alias_id.inspect} maps to both #{aliases[alias_id].inspect} and #{target.inspect}"
      end

      aliases[alias_id] = target
    end
  end
end
