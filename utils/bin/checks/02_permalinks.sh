#!/usr/bin/env bash

# Run permalink validator
echo "🔍 Checking permalinks..."
./utils/bin/check_permalinks.rb
exit $? 