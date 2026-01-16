#!/usr/bin/env python3
"""
General File Watcher

Monitors files for changes and automatically runs scripts in the watchers directory.
Each watcher script should be executable and can define its own file patterns and actions.

Usage:
 python utils/bin/file_watcher.py [--target-dir DIR] [--watchers-dir DIR]
"""

import argparse
import os
import sys
import time
import subprocess
import logging
import signal
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set up logging
logging.basicConfig(
 level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


def signal_handler(signum, frame):
 """Handle termination signals gracefully."""
 logger.info(f"\n🛑 Received signal {signum}, stopping watcher...")
 sys.exit(0)


class FileWatcherHandler(FileSystemEventHandler):
 """Handle file system events and run appropriate watchers."""

 def __init__(self, target_dir, watchers_dir):
 self.target_dir = target_dir
 self.watchers_dir = watchers_dir
 self.last_events = {} # Track last event time for debouncing
 self.watcher_scripts = set() # Track current watcher scripts
 self._load_watcher_scripts()

 def _load_watcher_scripts(self):
 """Load the list of available watcher scripts."""
 watchers_path = Path(self.watchers_dir)
 if watchers_path.exists():
 self.watcher_scripts = {
 script.name
 for script in watchers_path.glob("*.py")
 if not script.name.startswith("_")
 }
 else:
 self.watcher_scripts = set()

 def on_modified(self, event):
 if event.is_directory:
 return
 self._handle_event(event, "modified")

 def on_created(self, event):
 if event.is_directory:
 return
 self._handle_event(event, "created")

 def on_deleted(self, event):
 if event.is_directory:
 return
 self._handle_event(event, "deleted")

 def _handle_event(self, event, event_type):
 """Handle a file system event."""
 file_path = event.src_path

 # Check if this is a change in the watchers directory
 if self.watchers_dir in file_path:
 self._handle_watcher_change(event, event_type)
 return

 # Get relative path from target directory
 try:
 rel_path = os.path.relpath(file_path, self.target_dir)
 except ValueError:
 return

 logger.info(f"📝 File {event_type}: {rel_path}")

 # Run all watcher scripts
 self._run_watchers(file_path, event_type)

 def _handle_watcher_change(self, event, event_type):
 """Handle changes in the watchers directory."""
 file_name = Path(event.src_path).name

 if (
 event_type == "created"
 and file_name.endswith(".py")
 and not file_name.startswith("_")
 ):
 logger.info(f"🆕 New watcher script detected: {file_name}")
 self._load_watcher_scripts()
 elif event_type == "deleted" and file_name.endswith(".py"):
 logger.info(f"🗑️ Watcher script removed: {file_name}")
 self._load_watcher_scripts()
 elif (
 event_type == "modified"
 and file_name.endswith(".py")
 and not file_name.startswith("_")
 ):
 logger.info(f"🔄 Watcher script modified: {file_name}")
 self._load_watcher_scripts()

 def _run_watchers(self, file_path, event_type):
 """Run all watcher scripts for the given file."""
 watchers_path = Path(self.watchers_dir)

 if not watchers_path.exists():
 return

 # Use the cached list of watcher scripts
 for script_name in self.watcher_scripts:
 script_file = watchers_path / script_name

 if not script_file.exists():
 continue # Script was removed, skip it

 # Check debounce
 current_time = time.time()
 event_key = f"{script_name}:{file_path}"

 if event_key in self.last_events:
 if (
 current_time - self.last_events[event_key] < 1.0
 ): # 1 second debounce
 continue
 self.last_events[event_key] = current_time

 # Run the watcher script
 try:
 env = os.environ.copy()
 env["WATCHER_FILE"] = file_path
 env["WATCHER_EVENT"] = event_type
 env["WATCHER_NAME"] = script_file.stem

 result = subprocess.run(
 [sys.executable, str(script_file), file_path, event_type],
 capture_output=True,
 text=True,
 env=env,
 cwd=os.getcwd(),
 )

 if result.returncode == 0:
 if result.stdout.strip():
 logger.info(f"✅ {script_file.stem}: {result.stdout.strip()}")
 else:
 logger.error(f"❌ {script_file.stem}: {result.stderr.strip()}")

 except Exception as e:
 logger.error(f"❌ {script_file.stem}: Failed to run - {e}")


def main():
 # Set up signal handlers for graceful shutdown
 signal.signal(signal.SIGTERM, signal_handler)
 signal.signal(signal.SIGINT, signal_handler)

 parser = argparse.ArgumentParser(
 description="Watch files and run watcher scripts automatically"
 )
 parser.add_argument(
 "--target-dir", default="html", help="Directory to watch (default: html)"
 )
 parser.add_argument(
 "--watchers-dir",
 default="utils/bin/watchers",
 help="Directory containing watcher scripts (default: utils/bin/watchers)",
 )
 parser.add_argument(
 "--list-watchers", action="store_true", help="List available watchers and exit"
 )

 args = parser.parse_args()

 # Validate paths
 target_path = Path(args.target_dir)
 if not target_path.exists():
 logger.error(f"❌ Target directory does not exist: {args.target_dir}")
 sys.exit(1)

 watchers_path = Path(args.watchers_dir)
 if not watchers_path.exists():
 logger.warning(f"⚠️ Watchers directory does not exist: {args.watchers_dir}")
 logger.info("Creating watchers directory...")
 watchers_path.mkdir(parents=True, exist_ok=True)

 # List watchers if requested
 if args.list_watchers:
 watchers = list(watchers_path.glob("*.py"))
 if not watchers:
 print("No watchers found.")
 else:
 print("Available watchers:")
 for watcher in watchers:
 if not watcher.name.startswith("_"):
 print(f" - {watcher.stem}")
 return

 logger.info("🔍 Starting file watcher...")
 logger.info(f" Target directory: {args.target_dir}")
 logger.info(f" Watchers directory: {args.watchers_dir}")
 logger.info(" Press Ctrl+C to stop")

 # Set up the event handler and observer
 event_handler = FileWatcherHandler(args.target_dir, args.watchers_dir)
 observer = Observer()

 # Watch both the target directory and the watchers directory
 observer.schedule(event_handler, args.target_dir, recursive=True)
 observer.schedule(event_handler, args.watchers_dir, recursive=False)

 try:
 observer.start()
 logger.info("✅ Watcher started successfully")

 # Keep the script running
 while True:
 time.sleep(1)

 except KeyboardInterrupt:
 logger.info("\n🛑 Stopping watcher...")
 observer.stop()

 observer.join()
 logger.info("✅ Watcher stopped")


if __name__ == "__main__":
 main()
