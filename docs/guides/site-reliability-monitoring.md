# Site Reliability Monitoring System

## Overview

The Site Reliability Monitoring System provides automated health checks, deployment verification, and alerting for the Jekyll website. It eliminates the need for manual page-by-page checking and provides proactive monitoring with intelligent output formatting and smart defaults.

## Features

### 🏥 **Comprehensive Health Checks**
- **Site Availability**: Verifies the main site is accessible
- **Critical Pages**: Checks all important pages load correctly
- **Response Times**: Monitors page load performance
- **Image Verification**: Detects broken images (with smart 404 page handling)
- **Link Validation**: Ensures internal links work
- **External Link Validation**: Ensures all external references are valid and accessible
- **Early Exit Logic**: Stops checking if site is down to avoid timeouts
- **Summary Counts**: Shows totals for pages, images, and links checked

### 🚀 **Post-Commit Verification**
- **Automatic Deployment Check**: Runs after commits with configurable delay
- **Email Alerts**: Notifies you of deployment success/failure
- **Issue Reporting**: Detailed breakdown of any problems found

### ⏰ **Periodic Monitoring**
- **Scheduled Checks**: Runs automatically at configurable intervals
- **Proactive Alerts**: Catches issues before users report them
- **Performance Tracking**: Monitors response times over time

### 📧 **Email Alerting**
- **Success Notifications**: Confirms deployments worked correctly
- **Issue Alerts**: Detailed reports of problems found
- **Configurable**: Supports Gmail and other SMTP providers

### 🎯 **Smart Output Formatting**
- **Summary Mode**: Shows counts and failures only (default)
- **Verbose Mode**: Shows all checked items with `-V` flag
- **Clear Status Indicators**: ✅ for success, ❌ for failures, 🐌 for slow responses
- **Final Summary**: Warm fuzzy feeling when all checks pass

## Quick Start

### 1. Initial Setup

```bash
# Run the setup script
./utils/bin/setup_site_monitoring.sh
```

This will:
- Configure email settings
- Make scripts executable
- Test the monitoring system
- Provide setup instructions

### 2. Configure Email Alerts

Edit `utils/etc/site_monitor_config.json`:

```json
{
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your-email@gmail.com",
        "sender_password": "your-app-password",
        "recipient_email": "your-email@gmail.com"
    }
}
```

**For Gmail**: Use an App Password, not your regular password.

### 3. Manual Testing

```bash
# Test health checks (summary mode)
python3 utils/bin/site_reliability_monitor.py --mode health

# Test health checks (verbose mode)
python3 utils/bin/site_reliability_monitor.py --mode health -V

# Test against local development server
python3 utils/bin/site_reliability_monitor.py --mode health --local

# Test post-commit verification (waits 10 minutes)
python3 utils/bin/site_reliability_monitor.py --mode post-commit

# Test periodic monitoring
python3 utils/bin/site_reliability_monitor.py --mode periodic
```

## Output Examples

### Summary Mode (Default)
```
🏥 Starting comprehensive health checks...
✅ Site is accessible: 200
🔍 Checking critical pages...
✅ 44 pages checked and passed.
🖼️ Checking images on critical pages...
✅ 44 images checked and passed.
🔗 Checking internal links...
🎉 All health checks passed! Your site is healthy and ready for visitors.
```

### Verbose Mode (-V)
```
🏥 Starting comprehensive health checks...
✅ Site is accessible: 200
🔍 Checking critical pages...
✅ http://localhost:4000/: 0.00s
✅ http://localhost:4000/blog/: 0.00s
✅ http://localhost:4000/projects/: 0.00s
✅ 44 pages checked and passed.
🖼️ Checking images on critical pages...
✅ http://localhost:4000/: images OK
✅ http://localhost:4000/blog/: images OK
✅ 44 images checked and passed.
🔗 Checking internal links...
🎉 All health checks passed! Your site is healthy and ready for visitors.
```

### With Failures
```
🏥 Starting comprehensive health checks...
✅ Site is accessible: 200
🔍 Checking critical pages...
❌ http://localhost:4000/missing-page/: HTTP 404
✅ 43 pages checked and passed.
❌ 1 page failed out of 44 checked:
  - http://localhost:4000/missing-page/ (HTTP error)
🖼️ Checking images on critical pages...
✅ 44 images checked and passed.
🔗 Checking internal links...
⚠️ Health checks completed with 1 issues
Please review and fix the issues listed above.
```

## Automation Setup

### Post-Commit Monitoring

Add to your git hooks or CI/CD pipeline:

```bash
# In your post-commit hook or CI script
./utils/bin/post_commit_monitor.sh
```

### Periodic Monitoring

Add to crontab for automatic periodic checks (recommended over launchd/systemd for simplicity and portability):

```bash
# Edit crontab
crontab -e

# Add this line for checks every 6 hours
0 */6 * * * /path/to/project/utils/bin/periodic_monitor.sh

# Or for daily checks at 9 AM
0 9 * * * /path/to/project/utils/bin/periodic_monitor.sh

# Or for checks every 12 hours (recommended for most sites)
0 */12 * * * /path/to/project/utils/bin/periodic_monitor.sh
```

## Configuration

### Critical Pages

Edit the `critical_pages` array in `utils/etc/site_monitor_config.json`:

```json
{
    "health_checks": {
        "critical_pages": [
            "/",
            "/blog/",
            "/projects/",
            "/about/",
            "/contact/",
            "/resources/",
            "/collaborate/"
        ]
    }
}
```

### Response Time Thresholds

```json
{
    "health_checks": {
        "max_response_time": 5.0
    }
}
```

### Deployment Settings

```json
{
    "deployment": {
        "check_delay_minutes": 10,
        "max_deployment_time": 15
    }
}
```

## Monitoring Modes

### Health Check Mode
```bash
python3 utils/bin/site_reliability_monitor.py --mode health
```
- Runs immediate health checks
- No email alerts
- Returns exit code 0 for success, 1 for failure

### Post-Commit Mode
```bash
python3 utils/bin/site_reliability_monitor.py --mode post-commit --commit-hash abc123
```
- Waits for deployment (configurable delay)
- Runs comprehensive health checks
- Sends email alerts with results
- Perfect for CI/CD integration

### Periodic Mode
```bash
python3 utils/bin/site_reliability_monitor.py --mode periodic
```
- Runs health checks
- Sends email alerts only if issues found
- Designed for scheduled execution

## Custom Health Checks

Add custom health check functions:

```python
def my_custom_check():
    # Your custom logic here
    return True  # or False if check fails

monitor = SiteReliabilityMonitor()
monitor.add_health_check(my_custom_check, "Custom Check Name", critical=True)
```

## Logging

All monitoring activity is logged to:
- **File**: `utils/log/site_monitor.log`
- **Console**: Real-time output during execution

Log levels:
- **INFO**: Normal operation
- **WARNING**: Non-critical issues
- **ERROR**: Critical failures

## Troubleshooting

### Email Not Sending
1. Check SMTP settings in config file
2. For Gmail, ensure you're using an App Password
3. Verify firewall/network connectivity

### False Positives
1. Adjust response time thresholds
2. Add problematic pages to exclusion list
3. Check for temporary network issues

### Monitoring Not Running
1. Verify script permissions: `chmod +x utils/bin/site_reliability_monitor.py`
2. Check Python dependencies: `pip install requests`
3. Verify config file exists and is valid JSON

## Integration with Existing Systems

### Git Hooks
Add to `.git/hooks/post-commit`:
```bash
#!/bin/bash
/path/to/project/utils/bin/post_commit_monitor.sh
```

### CI/CD Pipelines
Add to your GitHub Actions, GitLab CI, or other CI/CD:
```yaml
- name: Site Reliability Check
  run: |
    ./utils/bin/post_commit_monitor.sh
```

### Existing Pre-commit Checks
The monitoring system complements your existing pre-commit checks:
- **Pre-commit**: Catches issues before deployment
- **Post-commit**: Verifies deployment success
- **Periodic**: Ongoing health monitoring

## Benefits

### 🎯 **Proactive Issue Detection**
- Catches problems before users report them
- Monitors performance degradation
- Identifies broken links and images

### ⚡ **Automated Verification**
- No manual page checking required
- Consistent monitoring across all pages
- Detailed issue reporting

### 📊 **Performance Insights**
- Response time tracking
- Deployment success rates
- Historical health data

### 🚨 **Immediate Alerts**
- Email notifications for issues
- Detailed problem descriptions
- Quick issue resolution

## Future Enhancements

Potential improvements:
- **Dashboard**: Web interface for monitoring results
- **Metrics**: Historical performance tracking
- **Slack Integration**: Alternative to email alerts
- **Custom Checks**: Plugin system for specific needs
- **Performance Baselines**: Automatic threshold adjustment

---

This monitoring system transforms your site maintenance from reactive to proactive, ensuring your website remains reliable and performant. 