#!/usr/bin/env bash

# Description: Runs Jekyll doctor to check for common configuration issues

echo "🔍 Running Jekyll doctor..."
bundle exec jekyll doctor
exit $? 