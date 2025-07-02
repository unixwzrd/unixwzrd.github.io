# Disable Directory Listing Plugin for Jekyll
# Prevents WEBrick from showing directory listings when index files are missing

require 'webrick'

# Override WEBrick's FileHandler to disable directory listings
module WEBrick
  class HTTPServlet::FileHandler
    alias_method :original_do_GET, :do_GET

    def do_GET(req, res)
      # Check if this is a request for a directory (ends with / and doesn't have a file extension)
      if req.path.end_with?('/') && !req.path.match(/\.(html|css|js|png|jpg|jpeg|gif|svg|ico|json|xml|txt|md)$/)
        # Check if index files exist
        index_files = ['index.html', 'index.md', 'index.markdown']
        index_exists = index_files.any? { |file| File.exist?(@root + req.path + file) }

        if !index_exists
          # Serve 404 page instead of directory listing
          custom_404_path = @root + "/404.html"
          if File.exist?(custom_404_path)
            res.status = 404
            res.content_type = "text/html"
            res.body = File.read(custom_404_path)
            return
          else
            # Fallback to simple 404 response
            res.status = 404
            res.content_type = "text/html"
            res.body = "<h1>404 - Page Not Found</h1><p>The requested page could not be found.</p>"
            return
          end
        end
      end

      # Call the original method for all other requests
      original_do_GET(req, res)
    rescue => e
      # If anything goes wrong, try to serve our custom 404 page
      custom_404_path = @root + "/404.html"
      if File.exist?(custom_404_path)
        res.status = 404
        res.content_type = "text/html"
        res.body = File.read(custom_404_path)
      else
        # Fallback to original error handling
        raise e
      end
    end
  end
end

# Register the plugin
Jekyll::Hooks.register :site, :post_write do |site|
  Jekyll.logger.info "Directory listing disabled - will serve 404.html for missing index files"
end 