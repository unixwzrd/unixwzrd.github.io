#!/bin/bash

# Setup Site Reliability Monitoring
# Configures email settings and sets up automated monitoring

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
cd "$PROJECT_ROOT"

CONFIG_FILE="utils/etc/site_monitor_config.json"

echo "🔧 Setting up Site Reliability Monitoring..."

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Function to update config value
update_config() {
    local key="$1"
    local value="$2"
    
    # Use jq to update the JSON config
    if command -v jq &> /dev/null; then
        jq "$key = \"$value\"" "$CONFIG_FILE" > "${CONFIG_FILE}.tmp" && mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"
    else
        echo "⚠️  jq not found. Please install jq or manually update the config file."
        echo "   Key: $key, Value: $value"
    fi
}

# Get email configuration
echo "📧 Email Configuration"
echo ""
echo "For Gmail: Use an App Password (not your regular password)"
echo "1. Go to Google Account settings"
echo "2. Security > 2-Step Verification > App passwords"
echo "3. Generate a password for 'Mail'"
echo ""
read -p "Enter your email address: " email
read -s -p "Enter your email password/app password: " password
echo ""

if [ -n "$email" ] && [ -n "$password" ]; then
    update_config ".email.sender_email" "$email"
    update_config ".email.recipient_email" "$email"
    update_config ".email.sender_password" "$password"
    echo "✅ Email configuration updated"
    
    # Test email configuration
    echo "🧪 Testing email configuration..."
    if python3 -c "
import smtplib
import json
config = json.load(open('$CONFIG_FILE'))
email_config = config['email']
try:
    server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
    server.starttls()
    server.login(email_config['sender_email'], email_config['sender_password'])
    server.quit()
    print('✅ Email authentication successful')
except Exception as e:
    print(f'❌ Email authentication failed: {e}')
    exit(1)
"; then
        echo "✅ Email configuration test passed"
    else
        echo "⚠️  Email configuration test failed - check your settings"
    fi
else
    echo "⚠️  Email configuration skipped"
fi

# Make scripts executable
chmod +x utils/bin/site_reliability_monitor.py
chmod +x utils/bin/post_commit_monitor.sh
chmod +x utils/bin/periodic_monitor.sh

echo "✅ Scripts made executable"

# Test the monitoring system
echo "🧪 Testing monitoring system..."
if python3 utils/bin/site_reliability_monitor.py --mode health; then
    echo "✅ Monitoring system test passed"
else
    echo "⚠️  Monitoring system test failed (this might be expected if site is not accessible)"
fi

# Setup instructions
echo ""
echo "🎯 Setup Complete! Next steps:"
echo ""
echo "1. 📧 Email Alerts:"
echo "   - Update $CONFIG_FILE with your email settings"
echo "   - For Gmail, use an App Password (not your regular password)"
echo ""
echo "2. 🔄 Post-Commit Monitoring:"
echo "   - Add to your git hooks or CI/CD pipeline:"
echo "   - ./utils/bin/post_commit_monitor.sh"
echo ""
echo "3. ⏰ Periodic Monitoring:"
echo "   - Add to crontab for periodic checks:"
echo "   - crontab -e"
echo "   - Add: 0 */6 * * * /path/to/project/utils/bin/periodic_monitor.sh"
echo ""
echo "4. 🧪 Manual Testing:"
echo "   - Health check: python3 utils/bin/site_reliability_monitor.py --mode health"
echo "   - Post-commit: python3 utils/bin/site_reliability_monitor.py --mode post-commit"
echo "   - Periodic: python3 utils/bin/site_reliability_monitor.py --mode periodic"
echo ""
# Create log directory
mkdir -p utils/log

echo "📊 Logs will be written to: utils/log/site_monitor.log" 