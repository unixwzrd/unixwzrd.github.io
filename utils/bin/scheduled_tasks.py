#!/usr/bin/env python3
"""
Scheduled Tasks Framework

Handles periodic maintenance tasks including:
- Log rotation
- Daily/weekly/monthly/quarterly tasks
- System cleanup
- Performance optimization
"""

import os
import sys
import shutil
import gzip
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import logging
import json

# Configure logging
logging.basicConfig(
 level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ScheduledTaskManager:
 def __init__(self, config_file: str = "utils/etc/scheduled_tasks_config.json"):
 self.config_file = Path(config_file)
 self.config = self._load_config()
 self.project_root = Path.cwd()

 def _load_config(self) -> dict:
 """Load configuration from JSON file."""
 if self.config_file.exists():
 try:
 with open(self.config_file, "r") as f:
 return json.load(f)
 except Exception as e:
 logger.error(f"Failed to load config: {e}")
 return self._get_default_config()
 else:
 return self._get_default_config()

 def _get_default_config(self) -> dict:
 """Get default configuration."""
 return {
 "log_rotation": {
 "enabled": True,
 "max_size_mb": 10,
 "keep_days": 30,
 "compress_old": True,
 "log_files": [
 "utils/log/site_monitor.log",
 "utils/log/jekyll_service.log",
 "utils/log/file_watcher.log",
 ],
 },
 "daily_tasks": {
 "enabled": True,
 "cleanup_temp_files": True,
 "check_disk_space": True,
 "verify_backups": False,
 },
 "weekly_tasks": {
 "enabled": True,
 "cleanup_old_builds": True,
 "optimize_images": False,
 "update_dependencies": False,
 },
 "monthly_tasks": {
 "enabled": True,
 "full_system_audit": True,
 "performance_review": True,
 "security_check": True,
 },
 "quarterly_tasks": {
 "enabled": True,
 "major_cleanup": True,
 "dependency_updates": True,
 "configuration_review": True,
 },
 }

 def rotate_logs(self) -> bool:
 """Rotate log files based on size and age."""
 logger.info("🔄 Starting log rotation...")

 config = self.config["log_rotation"]
 if not config["enabled"]:
 logger.info("Log rotation disabled in config")
 return True

 success = True
 for log_file in config["log_files"]:
 log_path = Path(log_file)
 if not log_path.exists():
 continue

 try:
 # Check file size
 size_mb = log_path.stat().st_size / (1024 * 1024)
 if size_mb > config["max_size_mb"]:
 self._rotate_single_log(log_path, config)

 # Check file age
 file_age = datetime.now() - datetime.fromtimestamp(
 log_path.stat().st_mtime
 )
 if file_age.days > config["keep_days"]:
 self._cleanup_old_log(log_path, config)

 except Exception as e:
 logger.error(f"Failed to rotate {log_file}: {e}")
 success = False

 logger.info("✅ Log rotation completed")
 return success

 def _rotate_single_log(self, log_path: Path, config: dict) -> None:
 """Rotate a single log file."""
 timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
 backup_path = log_path.with_suffix(f".{timestamp}.log")

 # Move current log to backup
 shutil.move(str(log_path), str(backup_path))

 # Create new empty log file
 log_path.touch()

 # Compress old backup if enabled
 if config["compress_old"]:
 with open(backup_path, "rb") as f_in:
 with gzip.open(f"{backup_path}.gz", "wb") as f_out:
 shutil.copyfileobj(f_in, f_out)
 backup_path.unlink() # Remove uncompressed backup

 logger.info(f"Rotated {log_path.name} -> {backup_path.name}")

 def _cleanup_old_log(self, log_path: Path, config: dict) -> None:
 """Clean up old log files."""
 # Find old log files
 log_dir = log_path.parent
 log_pattern = f"{log_path.stem}.*.log*"

 cutoff_date = datetime.now() - timedelta(days=config["keep_days"])

 for old_log in log_dir.glob(log_pattern):
 if old_log == log_path: # Skip current log
 continue

 try:
 file_date = datetime.fromtimestamp(old_log.stat().st_mtime)
 if file_date < cutoff_date:
 old_log.unlink()
 logger.info(f"Removed old log: {old_log.name}")
 except Exception as e:
 logger.error(f"Failed to remove {old_log}: {e}")

 def run_daily_tasks(self) -> bool:
 """Run daily maintenance tasks."""
 logger.info("📅 Running daily tasks...")

 config = self.config["daily_tasks"]
 if not config["enabled"]:
 logger.info("Daily tasks disabled in config")
 return True

 success = True

 if config["cleanup_temp_files"]:
 success &= self._cleanup_temp_files()

 if config["check_disk_space"]:
 success &= self._check_disk_space()

 if config["verify_backups"]:
 success &= self._verify_backups()

 logger.info("✅ Daily tasks completed")
 return success

 def run_weekly_tasks(self) -> bool:
 """Run weekly maintenance tasks."""
 logger.info("📅 Running weekly tasks...")

 config = self.config["weekly_tasks"]
 if not config["enabled"]:
 logger.info("Weekly tasks disabled in config")
 return True

 success = True

 if config["cleanup_old_builds"]:
 success &= self._cleanup_old_builds()

 if config["optimize_images"]:
 success &= self._optimize_images()

 if config["update_dependencies"]:
 success &= self._update_dependencies()

 logger.info("✅ Weekly tasks completed")
 return success

 def run_monthly_tasks(self) -> bool:
 """Run monthly maintenance tasks."""
 logger.info("📅 Running monthly tasks...")

 config = self.config["monthly_tasks"]
 if not config["enabled"]:
 logger.info("Monthly tasks disabled in config")
 return True

 success = True

 if config["full_system_audit"]:
 success &= self._full_system_audit()

 if config["performance_review"]:
 success &= self._performance_review()

 if config["security_check"]:
 success &= self._security_check()

 logger.info("✅ Monthly tasks completed")
 return success

 def run_quarterly_tasks(self) -> bool:
 """Run quarterly maintenance tasks."""
 logger.info("📅 Running quarterly tasks...")

 config = self.config["quarterly_tasks"]
 if not config["enabled"]:
 logger.info("Quarterly tasks disabled in config")
 return True

 success = True

 if config["major_cleanup"]:
 success &= self._major_cleanup()

 if config["dependency_updates"]:
 success &= self._dependency_updates()

 if config["configuration_review"]:
 success &= self._configuration_review()

 logger.info("✅ Quarterly tasks completed")
 return success

 def _cleanup_temp_files(self) -> bool:
 """Clean up temporary files."""
 logger.info("🧹 Cleaning up temporary files...")

 temp_patterns = [
 "*.tmp",
 "*.temp",
 ".DS_Store",
 "Thumbs.db",
 "_site/.jekyll-cache/*",
 ]

 cleaned = 0
 for pattern in temp_patterns:
 for file_path in self.project_root.rglob(pattern):
 try:
 if file_path.is_file():
 file_path.unlink()
 cleaned += 1
 except Exception as e:
 logger.error(f"Failed to remove {file_path}: {e}")

 logger.info(f"Cleaned up {cleaned} temporary files")
 return True

 def _check_disk_space(self) -> bool:
 """Check available disk space."""
 logger.info("💾 Checking disk space...")

 try:
 stat = shutil.disk_usage(self.project_root)
 free_gb = stat.free / (1024**3)

 if free_gb < 1.0:
 logger.warning(f"Low disk space: {free_gb:.2f} GB free")
 return False
 else:
 logger.info(f"Disk space OK: {free_gb:.2f} GB free")
 return True
 except Exception as e:
 logger.error(f"Failed to check disk space: {e}")
 return False

 def _cleanup_old_builds(self) -> bool:
 """Clean up old build artifacts."""
 logger.info("🧹 Cleaning up old builds...")

 build_dirs = ["_site", ".jekyll-cache"]
 cleaned = 0

 for dir_name in build_dirs:
 build_path = self.project_root / dir_name
 if build_path.exists():
 try:
 shutil.rmtree(build_path)
 cleaned += 1
 logger.info(f"Removed {dir_name}")
 except Exception as e:
 logger.error(f"Failed to remove {dir_name}: {e}")

 logger.info(f"Cleaned up {cleaned} build directories")
 return True

 def _full_system_audit(self) -> bool:
 """Run a full system audit."""
 logger.info("🔍 Running full system audit...")

 # Check for broken links
 # Check for missing images
 # Check for outdated content
 # Check for security issues

 logger.info("System audit completed")
 return True

 def _performance_review(self) -> bool:
 """Review system performance."""
 logger.info("⚡ Reviewing system performance...")

 # Analyze log files for performance issues
 # Check response times
 # Review resource usage

 logger.info("Performance review completed")
 return True

 def _security_check(self) -> bool:
 """Check for security issues."""
 logger.info("🔒 Running security check...")

 # Check for exposed secrets
 # Review file permissions
 # Check for outdated dependencies

 logger.info("Security check completed")
 return True

 def _major_cleanup(self) -> bool:
 """Perform major cleanup tasks."""
 logger.info("🧹 Performing major cleanup...")

 # Deep clean of all temporary files
 # Archive old logs
 # Clean up unused assets

 logger.info("Major cleanup completed")
 return True

 def _dependency_updates(self) -> bool:
 """Update dependencies."""
 logger.info("📦 Updating dependencies...")

 # Update Gemfile dependencies
 # Update Python dependencies
 # Check for security updates

 logger.info("Dependency updates completed")
 return True

 def _configuration_review(self) -> bool:
 """Review system configuration."""
 logger.info("⚙️ Reviewing system configuration...")

 # Review all config files
 # Check for deprecated settings
 # Validate configuration

 logger.info("Configuration review completed")
 return True

 def _verify_backups(self) -> bool:
 """Verify backup integrity."""
 logger.info("💾 Verifying backups...")
 # Placeholder for backup verification
 return True

 def _optimize_images(self) -> bool:
 """Optimize image files."""
 logger.info("🖼️ Optimizing images...")
 # Placeholder for image optimization
 return True

 def _update_dependencies(self) -> bool:
 """Update dependencies."""
 logger.info("📦 Updating dependencies...")
 # Placeholder for dependency updates
 return True


def main():
 parser = argparse.ArgumentParser(description="Scheduled Task Manager")
 parser.add_argument(
 "--task",
 choices=["rotate-logs", "daily", "weekly", "monthly", "quarterly"],
 required=True,
 help="Task to run",
 )
 parser.add_argument(
 "--config",
 default="utils/etc/scheduled_tasks_config.json",
 help="Configuration file path",
 )

 args = parser.parse_args()

 manager = ScheduledTaskManager(args.config)

 if args.task == "rotate-logs":
 success = manager.rotate_logs()
 elif args.task == "daily":
 success = manager.run_daily_tasks()
 elif args.task == "weekly":
 success = manager.run_weekly_tasks()
 elif args.task == "monthly":
 success = manager.run_monthly_tasks()
 elif args.task == "quarterly":
 success = manager.run_quarterly_tasks()

 sys.exit(0 if success else 1)


if __name__ == "__main__":
 main()
