# GitHub Actions Setup Guide

This guide explains how to set up GitHub Actions for automated site health monitoring with GitHub's built-in notifications.

## Overview

The GitHub Actions workflow provides:
- **Periodic health checks** every 6 hours
- **Post-commit verification** after deployments
- **GitHub Issues** created automatically on failures
- **Manual triggering** for testing
- **No SMTP configuration required** - uses GitHub's built-in notifications

## Setup Steps

### 1. Enable GitHub Actions

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Actions** → **General**
3. Ensure "Allow all actions and reusable workflows" is selected
4. Save the settings

### 2. Configure GitHub Notifications

GitHub will automatically send email notifications to repository members when:
- Workflows fail
- Issues are created
- Pull requests are opened

To configure your notification preferences:

1. Go to **Settings** → **Notifications**
2. Configure email notifications for:
   - **Issues**: When issues are opened or commented on
   - **Actions**: When workflows fail
   - **Repository**: When you're mentioned or assigned

### 3. Test the Setup

1. Go to **Actions** tab in your repository
2. Select **Site Health Check** workflow
3. Click **Run workflow** → **Run workflow**
4. Monitor the execution

## Workflow Features

### Periodic Health Checks
- Runs every 6 hours automatically
- Checks site availability, critical pages, images, and links
- Creates GitHub Issues on failures
- Prevents duplicate issues (only creates one per 24 hours)

### Post-Commit Verification
- Triggers after pushes to main branch
- Waits 15 minutes for deployment
- Verifies site health after changes
- Creates GitHub Issues on failures

### Manual Testing
- Can be triggered manually via GitHub UI
- Useful for testing configuration changes
- Creates issues on failures

## How Notifications Work

### GitHub Issues
When health checks fail, the workflow automatically creates GitHub Issues with:
- Detailed error information
- Links to workflow logs
- Step-by-step troubleshooting instructions
- Appropriate labels for filtering

### Email Notifications
GitHub automatically sends email notifications to repository members when:
- Issues are created
- Workflows fail
- You're mentioned in issues

### Issue Labels
The workflow uses these labels for easy filtering:
- `site-health` - General site health issues
- `deployment` - Post-commit verification issues
- `automated` - Issues created by automation
- `bug` - Problems that need fixing

## Benefits of This Approach

### Simplicity
- **No SMTP configuration** required
- **No secrets to manage**
- **No external dependencies**
- **Works out of the box**

### Reliability
- **GitHub's infrastructure** handles notifications
- **No email delivery issues**
- **Automatic retry on failures**
- **Built-in spam protection**

### Integration
- **Issues integrate with GitHub's workflow**
- **Can assign issues to team members**
- **Track resolution progress**
- **Link to pull requests and commits**

## Troubleshooting

### Common Issues

1. **Workflow Not Running**
   - Check if Actions are enabled in repository settings
   - Verify the workflow file is in `.github/workflows/`
   - Check GitHub Actions logs for errors

2. **No Notifications**
   - Check your GitHub notification settings
   - Verify you're a repository member
   - Check if notifications are enabled for the repository

3. **Issues Not Created**
   - Check workflow permissions
   - Verify the workflow has access to create issues
   - Check GitHub Actions logs for errors

### Manual Testing

You can test the health check locally:

```bash
# Test the monitoring system
python3 utils/bin/site_reliability_monitor.py --mode health

# Test post-commit verification
python3 utils/bin/site_reliability_monitor.py --mode post-commit
```

## Monitoring and Maintenance

### Viewing Results
- Check **Actions** tab for workflow runs
- Check **Issues** tab for health problems
- Download logs as artifacts
- Monitor email notifications from GitHub

### Managing Issues
- **Close issues** when problems are resolved
- **Add comments** with resolution details
- **Assign issues** to team members
- **Use labels** for organization

### Updating Configuration
- Modify workflow file for new features
- Test changes with manual workflow runs
- Update issue templates if needed

## Integration with Local Monitoring

The GitHub Actions workflow complements your local monitoring:

- **Local**: Real-time development monitoring with email alerts
- **GitHub Actions**: Production deployment verification with GitHub Issues
- **Both**: Comprehensive coverage of your site health

This provides redundancy and ensures issues are caught whether you're actively developing or not.

## Cost Considerations

- GitHub Actions provides 2,000 minutes/month for free
- Each health check uses ~2-3 minutes
- Monitor usage in **Settings** → **Billing**
- No additional costs for notifications or issues 