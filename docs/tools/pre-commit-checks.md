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

[Additional checks documented similarly...]

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

3. **Environment Check Fails**
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