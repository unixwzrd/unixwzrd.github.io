# Testing Guide

This guide covers testing procedures for the file watcher system and Jekyll service integration.

## Quick Test

For a fast verification that everything is working:

```bash
python utils/bin/quick_test.py
```

This runs basic functionality tests:
- File watcher startup
- Jekyll service integration
- Watcher script execution
- Directory structure verification

## Full Test Suite

For comprehensive testing:

```bash
python utils/bin/test_file_watcher.py [--verbose]
```

The full test suite covers:
- File watcher startup and shutdown
- Dynamic watcher script reloading
- Watcher script execution
- Jekyll service integration
- Error handling with broken scripts

## Manual Testing

### 1. Test Jekyll Service Integration

```bash
# Start both Jekyll and watcher
./utils/bin/jekyll-service start

# Start only Jekyll
./utils/bin/jekyll-service start -j

# Start only watcher
./utils/bin/jekyll-service start -w

# Stop both
./utils/bin/jekyll-service stop

# Stop only Jekyll
./utils/bin/jekyll-service stop -j

# Stop only watcher
./utils/bin/jekyll-service stop -w
```

### 2. Test File Watcher Functionality

```bash
# Start watcher
./utils/bin/jekyll-service start -w

# Create a test file with image path
echo '![Test Image](test_image.png)' > html/test_file.md

# Check if it was processed (should show absolute URL)
cat html/test_file.md

# Clean up
rm html/test_file.md
```

### 3. Test Dynamic Script Loading

```bash
# Start watcher
./utils/bin/jekyll-service start -w

# Create a new watcher script
cat > utils/bin/watchers/test_script.py << 'EOF'
#!/usr/bin/env python3
import sys
print(f"New script loaded for {sys.argv[1]}")
EOF

chmod +x utils/bin/watchers/test_script.py

# The watcher should detect and load the new script automatically
# Check logs for "New watcher script detected" message

# Clean up
rm utils/bin/watchers/test_script.py
```

## Test Results Interpretation

### ✅ Success Indicators

- File watcher starts without errors
- Jekyll service shows new `-j` and `-w` flags in help
- Watcher scripts execute when files change
- New scripts are detected and loaded automatically
- Error handling works (broken scripts don't crash the watcher)

### ❌ Failure Indicators

- File watcher fails to start
- Jekyll service doesn't recognize new flags
- Watcher scripts don't execute
- New scripts aren't detected
- Watcher crashes when encountering errors

## Troubleshooting

### Common Issues

1. **File watcher won't start**
   - Check if target directory exists
   - Verify Python dependencies are installed
   - Check file permissions

2. **Watcher scripts not executing**
   - Ensure scripts are executable (`chmod +x`)
   - Check script syntax
   - Verify scripts are in `utils/bin/watchers/` directory

3. **Jekyll service integration issues**
   - Verify script is executable
   - Check environment variables
   - Ensure PID files are writable

### Debug Mode

Run tests with verbose output:

```bash
python utils/bin/test_file_watcher.py --verbose
```

This shows detailed test messages and helps identify specific issues.

## Continuous Testing

The file watcher system includes built-in error handling and logging. Monitor the logs during development to ensure everything continues working correctly.

For automated testing in CI/CD pipelines, use the quick test script as it provides fast feedback without extensive setup. 