# WEBrick 404 Handler Plugin
# Configures WEBrick to serve our custom 404.html page instead of default 404 messages

require 'webrick'

# Monkey patch WEBrick to handle missing index files properly
module WEBrick
  class HTTPServlet::FileHandler
    alias_method :original_do_GET, :do_GET
    
    def do_GET(req, res)
      # Check if this is a request for the root directory
      if req.path == "/" || req.path == ""
        # Check if index files exist
        index_files = ['index.html', 'index.md', 'index.markdown']
        index_exists = index_files.any? { |file| File.exist?(@root + "/" + file) }
        
        if !index_exists
          # Serve our custom 404 page instead of directory listing or default 404
          custom_404_path = @root + "/404.html"
          if File.exist?(custom_404_path)
            res.status = 404
            res.content_type = "text/html"
            res.body = File.read(custom_404_path)
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
  Jekyll.logger.info "WEBrick 404 handler configured - will serve custom 404.html for missing index"
end 