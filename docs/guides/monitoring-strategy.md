# Site Monitoring Strategy

## Check Frequency Guidelines

### 🚀 **Post-Commit Monitoring** (Recommended: Always)
- **When**: After every commit/push
- **Delay**: 15 minutes (configurable)
- **Purpose**: Verify deployment success
- **Email**: Always (success or failure)
- **Why**: Catches deployment issues immediately

### ⏰ **Periodic Monitoring** (Recommended: 6-12 hours)
- **When**: Scheduled intervals (crontab)
- **Frequency**: Every 6-12 hours
- **Purpose**: Catch issues between deployments
- **Email**: Only on failure
- **Why**: Proactive monitoring without spam

### 🏥 **Manual Health Checks** (As needed)
- **When**: Manual testing, troubleshooting
- **Purpose**: Immediate verification
- **Email**: Never
- **Why**: Quick feedback during development

## Avoiding Over-Checking

### ❌ **Don't Run During:**
- **File system changes** (handled by file watcher)
- **Pre-commit checks** (different purpose)
- **Development builds** (unnecessary overhead)

### ✅ **Do Run During:**
- **Post-deployment** (critical)
- **Scheduled intervals** (proactive)
- **Manual verification** (troubleshooting)

## Recommended Setup

### 1. **Post-Commit Hook**
```bash
# In your CI/CD or git hook
./utils/bin/post_commit_monitor.sh
```

### 2. **Periodic Monitoring**
```bash
# Add to crontab (every 6 hours)
0 */6 * * * /path/to/project/utils/bin/periodic_monitor.sh

# Or daily at 9 AM
0 9 * * * /path/to/project/utils/bin/periodic_monitor.sh
```

### 3. **Manual Testing**
```bash
# Quick health check
python3 utils/bin/site_reliability_monitor.py --mode health
```

## Check Overlap Analysis

| Check Type | Frequency | Purpose | Email | Overlap Risk |
|------------|-----------|---------|-------|--------------|
| File Watcher | Real-time | Development fixes | No | Low |
| Pre-commit | Per commit | Pre-deployment | No | Low |
| Post-commit | Per deployment | Deployment verification | Yes | Low |
| Periodic | 6-12 hours | Ongoing monitoring | On failure | Low |

## Optimization Recommendations

### **For Active Development:**
- **Post-commit**: Always (15-minute delay)
- **Periodic**: Every 12 hours
- **Manual**: As needed

### **For Stable Sites:**
- **Post-commit**: Always (15-minute delay)
- **Periodic**: Daily at 9 AM
- **Manual**: Monthly or on issues

### **For High-Traffic Sites:**
- **Post-commit**: Always (15-minute delay)
- **Periodic**: Every 6 hours
- **Manual**: Weekly health checks

## Resource Considerations

### **Network Impact:**
- **Post-commit**: ~10 requests per deployment
- **Periodic**: ~10 requests every 6-12 hours
- **Total**: ~50-100 requests per day

### **Email Volume:**
- **Success emails**: 1 per deployment
- **Failure emails**: Only when issues found
- **Estimated**: 1-5 emails per day

### **Log Volume:**
- **File size**: ~1-5 MB per month
- **Rotation**: Consider log rotation for long-term use

## Troubleshooting Over-Checking

### **Symptoms:**
- Too many emails
- Slow development workflow
- High resource usage

### **Solutions:**
1. **Reduce periodic frequency** (12 hours instead of 6)
2. **Disable email on success** (modify config)
3. **Use manual checks only** for development
4. **Implement log rotation** for long-term use

## Best Practices

### **1. Start Conservative**
- Begin with post-commit only
- Add periodic monitoring gradually
- Monitor email volume and adjust

### **2. Configure Appropriately**
- Set realistic response time thresholds
- Include only truly critical pages
- Use appropriate check delays

### **3. Monitor the Monitor**
- Check log files periodically
- Verify email delivery
- Test the system monthly

### **4. Scale as Needed**
- Increase frequency for critical sites
- Decrease frequency for stable sites
- Adjust based on actual issues found

---

This strategy ensures comprehensive monitoring without overwhelming your workflow or inbox. 