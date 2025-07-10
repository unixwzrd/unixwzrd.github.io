# Troubleshooting

[← Back to Site Operations Guide](site-operations.md)

- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
    - [RVM Issues](#rvm-issues)
    - [Jekyll Build Issues](#jekyll-build-issues)
    - [Port Conflicts](#port-conflicts)
    - [OpenGraph Refresh Issues](#opengraph-refresh-issues)
  - [Service Management Issues](#service-management-issues)
    - [Server Won't Start](#server-wont-start)
    - [Server Won't Stop](#server-wont-stop)

This section covers common issues, error messages, and their solutions for both development and production environments.

## Common Issues

### RVM Issues
```bash
# If RVM not found
source ~/.rvm/scripts/rvm

# If gemset not found
rvm gemset create unixwzrd.github.io
rvm use 3.3.4@unixwzrd.github.io --default
bundle install
```

### Jekyll Build Issues
```bash
# Clear all caches
rm -rf _site/
rm -rf html/.jekyll-cache/
rm -rf html/.sass-cache/

# Rebuild
bundle exec jekyll build --trace
```

### Port Conflicts
```bash
# Check if port 4000 is in use
lsof -i :4000

# Kill process if needed
kill -9 <PID>
```

### OpenGraph Refresh Issues
```bash
# Manual OpenGraph refresh
python3 utils/bin/fetch_og.py

# Check for API rate limits or network issues
```

## Service Management Issues

### Server Won't Start
```bash
# Check if PID file exists but process is dead
rm -f utils/etc/jekyll.pid

# Restart service
./utils/bin/site-service restart
```

### Server Won't Stop
```bash
# Force kill by PID
cat utils/etc/jekyll.pid | xargs kill -9
rm -f utils/etc/jekyll.pid
``` 