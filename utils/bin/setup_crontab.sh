#!/bin/bash

# Setup Crontab for Scheduled Tasks
# Sets up automated tasks for log rotation, monitoring, and maintenance

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
cd "$PROJECT_ROOT"

echo "🔧 Setting up Crontab for Scheduled Tasks..."

# Create log directory if it doesn't exist
mkdir -p utils/log

# Get the full path to the project
PROJECT_PATH=$(pwd)

# Define the crontab entries
CRONTAB_ENTRIES=(
    "# Site Reliability Monitoring - Log Rotation (Daily at 2 AM)"
    "0 2 * * * cd $PROJECT_PATH && python3 utils/bin/scheduled_tasks.py --task rotate-logs >> utils/log/cron.log 2>&1"
    ""
    "# Site Reliability Monitoring - Daily Tasks (Daily at 3 AM)"
    "0 3 * * * cd $PROJECT_PATH && python3 utils/bin/scheduled_tasks.py --task daily >> utils/log/cron.log 2>&1"
    ""
    "# Site Reliability Monitoring - Weekly Tasks (Sundays at 4 AM)"
    "0 4 * * 0 cd $PROJECT_PATH && python3 utils/bin/scheduled_tasks.py --task weekly >> utils/log/cron.log 2>&1"
    ""
    "# Site Reliability Monitoring - Monthly Tasks (1st of month at 5 AM)"
    "0 5 1 * * cd $PROJECT_PATH && python3 utils/bin/scheduled_tasks.py --task monthly >> utils/log/cron.log 2>&1"
    ""
    "# Site Reliability Monitoring - Quarterly Tasks (1st of Jan, Apr, Jul, Oct at 6 AM)"
    "0 6 1 1,4,7,10 * cd $PROJECT_PATH && python3 utils/bin/scheduled_tasks.py --task quarterly >> utils/log/cron.log 2>&1"
    ""
    "# Site Health Monitoring - Every 6 hours"
    "0 */6 * * * cd $PROJECT_PATH && python3 utils/bin/site_reliability_monitor.py --mode periodic >> utils/log/cron.log 2>&1"
)

# Function to add crontab entries
setup_crontab() {
    echo "📅 Setting up crontab entries..."
    
    # Create temporary file with current crontab
    CURRENT_CRONTAB=$(mktemp)
    crontab -l 2>/dev/null > "$CURRENT_CRONTAB" || true
    
    # Check if our entries already exist
    if grep -q "Site Reliability Monitoring" "$CURRENT_CRONTAB"; then
        echo "⚠️  Crontab entries already exist. Removing old entries..."
        # Remove existing entries
        sed -i.bak '/# Site Reliability Monitoring/,/^$/d' "$CURRENT_CRONTAB"
        sed -i.bak '/^$/d' "$CURRENT_CRONTAB"  # Remove empty lines
    fi
    
    # Add new entries
    echo "" >> "$CURRENT_CRONTAB"
    for entry in "${CRONTAB_ENTRIES[@]}"; do
        echo "$entry" >> "$CURRENT_CRONTAB"
    done
    
    # Install the new crontab
    crontab "$CURRENT_CRONTAB"
    rm "$CURRENT_CRONTAB"
    
    echo "✅ Crontab entries added successfully"
}

# Function to show current crontab
show_crontab() {
    echo "📋 Current crontab entries:"
    echo ""
    crontab -l 2>/dev/null | grep -A 1 -B 1 "Site Reliability Monitoring" || echo "No monitoring entries found"
    echo ""
}

# Function to remove crontab entries
remove_crontab() {
    echo "🗑️  Removing crontab entries..."
    
    CURRENT_CRONTAB=$(mktemp)
    crontab -l 2>/dev/null > "$CURRENT_CRONTAB" || true
    
    # Remove our entries
    sed -i.bak '/# Site Reliability Monitoring/,/^$/d' "$CURRENT_CRONTAB"
    sed -i.bak '/^$/d' "$CURRENT_CRONTAB"  # Remove empty lines
    
    # Install the cleaned crontab
    crontab "$CURRENT_CRONTAB"
    rm "$CURRENT_CRONTAB"
    
    echo "✅ Crontab entries removed"
}

# Function to test scheduled tasks
test_tasks() {
    echo "🧪 Testing scheduled tasks..."
    
    echo "Testing log rotation..."
    if python3 utils/bin/scheduled_tasks.py --task rotate-logs; then
        echo "✅ Log rotation test passed"
    else
        echo "❌ Log rotation test failed"
    fi
    
    echo "Testing daily tasks..."
    if python3 utils/bin/scheduled_tasks.py --task daily; then
        echo "✅ Daily tasks test passed"
    else
        echo "❌ Daily tasks test failed"
    fi
    
    echo "Testing site monitoring..."
    if python3 utils/bin/site_reliability_monitor.py --mode health; then
        echo "✅ Site monitoring test passed"
    else
        echo "❌ Site monitoring test failed (this might be expected if site has issues)"
    fi
}

# Main script logic
case "${1:-setup}" in
    "setup")
        setup_crontab
        show_crontab
        test_tasks
        ;;
    "show")
        show_crontab
        ;;
    "remove")
        remove_crontab
        ;;
    "test")
        test_tasks
        ;;
    *)
        echo "Usage: $0 [setup|show|remove|test]"
        echo ""
        echo "Commands:"
        echo "  setup   - Set up crontab entries (default)"
        echo "  show    - Show current crontab entries"
        echo "  remove  - Remove crontab entries"
        echo "  test    - Test scheduled tasks"
        exit 1
        ;;
esac

echo ""
echo "🎯 Crontab Setup Complete!"
echo ""
echo "📅 Scheduled Tasks:"
echo "  • Log Rotation: Daily at 2 AM"
echo "  • Daily Tasks: Daily at 3 AM"
echo "  • Weekly Tasks: Sundays at 4 AM"
echo "  • Monthly Tasks: 1st of month at 5 AM"
echo "  • Quarterly Tasks: 1st of Jan, Apr, Jul, Oct at 6 AM"
echo "  • Site Health: Every 6 hours"
echo ""
echo "📊 Logs:"
echo "  • Cron logs: utils/log/cron.log"
echo "  • Site monitor: utils/log/site_monitor.log"
echo "  • Scheduled tasks: utils/log/scheduled_tasks.log"
echo ""
echo "🔧 Management:"
echo "  • View crontab: crontab -l"
echo "  • Edit crontab: crontab -e"
echo "  • Show monitoring: $0 show"
echo "  • Remove monitoring: $0 remove" 