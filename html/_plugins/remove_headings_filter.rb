module Jekyll
    module ProcessHeadingsFilter
      def process_heading(input)
        puts "Processing input content: #{input}" # Debug input before processing
  
        # Case 1: If <h2> is followed by <p>, format accordingly with class
        processed_output = input.gsub(/<h2[^>]*>(.*?)<\/h2>\s*<p>/i, '<p class="post-excerpt"><b>\\1:</b> ')
  
        # Case 2: If <h2> is not followed by <p>, wrap <b> in a new <p> with class
        processed_output = processed_output.gsub(/<h2[^>]*>(.*?)<\/h2>/i, '<p class="post-excerpt"><b>\\1:</b></p>')
  
        puts "Processed output content: #{processed_output}" # Debug output after processing
        return processed_output
      end
    end
  end
  
  Liquid::Template.register_filter(Jekyll::ProcessHeadingsFilter)