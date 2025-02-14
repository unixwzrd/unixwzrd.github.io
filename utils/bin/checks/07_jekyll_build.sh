#!/usr/bin/env bash

# Description: Runs a test build of the Jekyll site with strict settings

echo "🏗️ Running test build with strict settings..."
JEKYLL_ENV=production bundle exec jekyll build --strict_front_matter --trace
exit $? 