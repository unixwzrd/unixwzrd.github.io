#!/usr/bin/env bash

# Run permalink validator
echo "🔍 Checking permalinks..."
./utils/bin/checks/check_permalinks.rb
exit $? 