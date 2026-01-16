#!/usr/bin/env python3
"""
Page Monitoring Management Script

Manages pages in the site reliability monitoring system:
- List missing pages
- Remove pages from monitoring
- Review page removal alerts
"""

import argparse
import json
from pathlib import Path
import sys
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.bin.site_reliability_monitor import SiteReliabilityMonitor


def list_missing_pages():
 """List all missing pages and their status."""
 monitor = SiteReliabilityMonitor()
 missing_data = monitor.list_missing_pages()

 print("📋 Missing Pages Report")
 print("=" * 50)

 if not missing_data["missing_pages"]:
 print("✅ No missing pages found!")
 return

 print(f"Found {len(missing_data['missing_pages'])} missing pages:\n")

 for page, data in missing_data["missing_pages"].items():
 first_detected = datetime.fromisoformat(data["first_detected"])
 last_detected = datetime.fromisoformat(data["last_detected"])
 days_missing = (datetime.now() - first_detected).days

 print(f"🔴 {page}")
 print(f" First detected: {first_detected.strftime('%Y-%m-%d %H:%M:%S')}")
 print(f" Last detected: {last_detected.strftime('%Y-%m-%d %H:%M:%S')}")
 print(f" Days missing: {days_missing}")
 print(f" Failure count: {data['failure_count']}")
 print(f" Status codes: {data['status_codes']}")

 # Check if page should be considered for removal
 if days_missing >= 7 or data["failure_count"] >= 10:
 print(
 f" ⚠️ CONSIDER REMOVAL: Missing for {days_missing} days or {data['failure_count']} failures"
 )
 print()


def list_removed_pages():
 """List pages that have been removed from monitoring."""
 monitor = SiteReliabilityMonitor()
 missing_data = monitor.list_missing_pages()

 print("🗑️ Removed Pages History")
 print("=" * 50)

 if not missing_data["removed_pages"]:
 print("No pages have been removed from monitoring.")
 return

 print(f"Found {len(missing_data['removed_pages'])} removed pages:\n")

 for removed in missing_data["removed_pages"]:
 removed_at = datetime.fromisoformat(removed["removed_at"])
 missing_data = removed["missing_data"]
 first_detected = datetime.fromisoformat(missing_data["first_detected"])
 days_missing = (removed_at - first_detected).days

 print(f"🔴 {removed['page']}")
 print(f" Removed: {removed_at.strftime('%Y-%m-%d %H:%M:%S')}")
 print(f" Was missing for: {days_missing} days")
 print(f" Total failures: {missing_data['failure_count']}")
 print()


def check_removal_alerts():
 """Check for page removal alerts."""
 alert_file = Path("utils/etc/page_removal_alert.json")

 if not alert_file.exists():
 print("✅ No page removal alerts found.")
 return

 try:
 with open(alert_file, "r") as f:
 alert_data = json.load(f)

 print("🚨 Page Removal Alert")
 print("=" * 50)
 print(f"Alert created: {alert_data['timestamp']}")
 print(f"Action required: {alert_data['action_required']}")
 print()

 print("Pages recommended for removal:")
 for page in alert_data["pages_to_remove"]:
 data = alert_data["missing_pages_data"][page]
 first_detected = datetime.fromisoformat(data["first_detected"])
 days_missing = (datetime.now() - first_detected).days

 print(f" - {page}")
 print(f" Missing for: {days_missing} days")
 print(f" Failure count: {data['failure_count']}")
 print(f" Latest status: {data['status_codes'][-1]}")
 print()

 print("To remove these pages, run:")
 print(
 f"python3 utils/bin/manage_monitoring_pages.py remove {' '.join(alert_data['pages_to_remove'])}"
 )

 except Exception as e:
 print(f"❌ Error reading alert file: {e}")


def remove_pages(pages_to_remove, confirm=False):
 """Remove pages from monitoring."""
 monitor = SiteReliabilityMonitor()

 if not confirm:
 print("⚠️ Page removal requires confirmation!")
 print(f"Pages to remove: {pages_to_remove}")
 print()
 print("To confirm removal, run with --confirm flag:")
 print(
 f"python3 utils/bin/manage_monitoring_pages.py remove {' '.join(pages_to_remove)} --confirm"
 )
 return False

 print(f"🗑️ Removing {len(pages_to_remove)} pages from monitoring...")

 success = monitor.remove_pages_from_monitoring(pages_to_remove, confirm=True)

 if success:
 print("✅ Pages removed successfully!")

 # Clear the alert file if it exists
 alert_file = Path("utils/etc/page_removal_alert.json")
 if alert_file.exists():
 alert_file.unlink()
 print("✅ Cleared page removal alert.")
 else:
 print("❌ Failed to remove pages.")

 return success


def list_monitored_pages():
 """List all currently monitored pages."""
 monitor = SiteReliabilityMonitor()

 print("📋 Currently Monitored Pages")
 print("=" * 50)

 pages = monitor.config["health_checks"]["critical_pages"]
 print(f"Total pages: {len(pages)}\n")

 for i, page in enumerate(pages, 1):
 print(f"{i:2d}. {page}")


def main():
 parser = argparse.ArgumentParser(description="Manage Site Monitoring Pages")
 parser.add_argument(
 "action",
 choices=["list", "missing", "removed", "alerts", "remove"],
 help="Action to perform",
 )
 parser.add_argument("pages", nargs="*", help="Pages to remove (for remove action)")
 parser.add_argument("--confirm", action="store_true", help="Confirm page removal")
 parser.add_argument(
 "--config",
 default="utils/etc/site_monitor_config.json",
 help="Configuration file path",
 )

 args = parser.parse_args()

 if args.action == "list":
 list_monitored_pages()
 elif args.action == "missing":
 list_missing_pages()
 elif args.action == "removed":
 list_removed_pages()
 elif args.action == "alerts":
 check_removal_alerts()
 elif args.action == "remove":
 if not args.pages:
 print("❌ No pages specified for removal.")
 print(
 "Usage: python3 utils/bin/manage_monitoring_pages.py remove page1 page2 --confirm"
 )
 sys.exit(1)
 remove_pages(args.pages, args.confirm)


if __name__ == "__main__":
 main()
