# Pre-commit Check System

## Overview

The pre-commit check system ensures code quality and consistency by running a series of validations before each commit. It's implemented through `utils/bin/check_site.sh` and its associated check scripts.

## Location

- Main script: `utils/bin/check_site.sh`
- Check scripts: `utils/bin/checks/*.sh`

## Dependencies

- Bash shell
- Ruby environment (for Jekyll)
- Python 3.x
- Required Python packages (see requirements.txt)

## Available Checks

### 1. Environment Check (01_environment.sh)

Validates the development environment:

```bash
# Run environment check only
./utils/bin/check_site.sh --run 01_environment
```

- Verifies Ruby/Jekyll installation
- Checks Python dependencies
- Validates environment variables

### 2. Permalink Validation (02_permalinks.sh)

Ensures consistent URL structure:

```bash
# Run permalink check only
./utils/bin/check_site.sh --run 02_permalinks
```

- Validates permalink format
- Checks for missing permalinks
- Ensures unique URLs

### 4. Link Checker (04_link_checker.sh)

Validates internal links and identifies orphaned pages:

```bash
# Run link check only
./utils/bin/check_site.sh --run 04_link_checker
```

- Checks for broken internal links
- Identifies orphaned pages
- Handles URL-encoded characters (spaces, special chars)
  - Automatically decodes %20 and other encoded characters
  - Properly verifies paths with spaces and special characters
- Reports external links for review

### Implementation Details

The link checker uses a URL decoding function:

```bash
urldecode() {
    local url_encoded="${1//+/ }"
    printf '%b' "${url_encoded//%/\\x}"
}
```

This function is called before checking file paths:

```bash
# Decode URL-encoded characters
decoded_target=$(urldecode "$target")

# Remove trailing slash and add potential extensions
base_target=${decoded_target%/}
```

[Additional checks documented similarly...]

### 5. Built-Site Link Verification (05_site_link_checker.sh)

Runs [HTMLProofer](https://github.com/gjtorikian/html-proofer) against the generated `_site/` output:

```bash
# Requires a prior `bundle exec jekyll build`
./utils/bin/checks/05_site_link_checker.sh
```

- Detects real 404s and missing fragment IDs in the rendered site (e.g., forward/backward references)
- Ignores external URLs to keep the check fast/offline
- Also available via `./utils/bin/jekyll-site build -c`, which triggers the same check immediately after a build

## Usage

### Basic Usage

```bash
# Run all checks
./utils/bin/check_site.sh

# Run specific checks
./utils/bin/check_site.sh --run check1,check2

# Skip specific checks
./utils/bin/check_site.sh --skip check1,check2

# List available checks
./utils/bin/check_site.sh --list
```

### Integration with Git

The checks are automatically run by the pre-commit hook:

```bash
.git/hooks/pre-commit
```

### Common Issues and Solutions

1. **Jekyll Build Fails**
   - Check Jekyll configuration
   - Verify front matter format
   - Look for Liquid syntax errors

2. **Permalink Validation Fails**
   - Ensure permalinks start and end with /
   - Check for duplicate permalinks
   - Verify permalink format

3. **Link Validation Fails**
   - Check for typos in link URLs
   - Verify files exist at the linked paths
   - For links with spaces or special characters, ensure proper URL encoding
   - Check for case sensitivity issues in file paths
   - If using special characters in filenames, test the link checker manually

4. **Environment Check Fails**
   - Update Ruby gems
   - Install missing Python packages
   - Check environment variables

## Adding New Checks

1. Create new check script in `utils/bin/checks/`
2. Name format: `NN_descriptive_name.sh`
3. Add description comment
4. Implement check logic
5. Return 0 for success, non-zero for failure

Example:

```bash
#!/usr/bin/env bash
# Description: Checks for required files

set -e
echo "Checking required files..."
# Check logic here
exit 0
```

## Configuration

- Check order determined by filename prefix
- Individual checks can be configured in their scripts
- Global settings in check_site.sh

## Future Enhancements

- Add performance checks
- Implement parallel check execution
- Add more detailed reporting
- Create check dependencies system
