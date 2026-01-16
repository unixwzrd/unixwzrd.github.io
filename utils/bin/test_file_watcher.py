#!/usr/bin/env python3
"""
File Watcher Test Suite

Comprehensive testing for the file watcher system including:
- File watcher startup and shutdown
- Dynamic watcher script reloading
- Watcher script execution
- Jekyll service integration
- Error handling

Usage:
 python utils/bin/test_file_watcher.py [--verbose]
"""

import os
import sys
import time
import tempfile
import subprocess
import threading
from pathlib import Path
import argparse
import logging

# Set up logging
logging.basicConfig(
 level=logging.INFO,
 format="%(asctime)s - %(levelname)s - %(message)s",
 datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


class FileWatcherTester:
 """Test suite for the file watcher system."""

 def __init__(self, verbose=False):
 self.verbose = verbose
 self.base_dir = Path.cwd()
 self.test_dir = self.base_dir / "test_watcher"
 self.test_file = self.base_dir / "html" / "test_file.md"
 self.watcher_script = (
 self.base_dir / "utils" / "bin" / "watchers" / "test_watcher.py"
 )
 self.results = []

 def log_test(self, test_name, passed, message=""):
 """Log test result."""
 status = "✅ PASS" if passed else "❌ FAIL"
 logger.info(f"{status} {test_name}: {message}")
 self.results.append((test_name, passed, message))

 def setup_test_environment(self):
 """Set up test environment."""
 logger.info("🔧 Setting up test environment...")

 # Create test watcher script
 test_script_content = '''#!/usr/bin/env python3
"""
Test Watcher Script

This script is used for testing the file watcher system.
It simply logs that it was executed.
"""

import os
import sys

def main():
 file_path = sys.argv[1]
 event_type = sys.argv[2]

 # Only process test files
 if not file_path.endswith('test_file.md'):
 return

 print(f"Test watcher executed for {file_path} (event: {event_type})")

if __name__ == "__main__":
 main()
'''

 self.watcher_script.parent.mkdir(parents=True, exist_ok=True)
 with open(self.watcher_script, "w") as f:
 f.write(test_script_content)

 # Make script executable
 os.chmod(self.watcher_script, 0o755)

 # Create test file
 self.test_file.parent.mkdir(parents=True, exist_ok=True)
 with open(self.test_file, "w") as f:
 f.write("# Test File\n\nThis is a test file for the file watcher.")

 logger.info("✅ Test environment setup complete")

 def cleanup_test_environment(self):
 """Clean up test environment."""
 logger.info("🧹 Cleaning up test environment...")

 # Remove test files
 if self.test_file.exists():
 self.test_file.unlink()

 if self.watcher_script.exists():
 self.watcher_script.unlink()

 logger.info("✅ Test environment cleanup complete")

 def test_file_watcher_startup(self):
 """Test that the file watcher starts correctly."""
 logger.info("🧪 Testing file watcher startup...")

 try:
 # Start file watcher in background
 process = subprocess.Popen(
 [sys.executable, "utils/bin/file_watcher.py", "--target-dir", "html"],
 stdout=subprocess.PIPE,
 stderr=subprocess.PIPE,
 text=True,
 )

 # Give it time to start
 time.sleep(2)

 # Check if process is still running
 if process.poll() is None:
 self.log_test(
 "File Watcher Startup", True, "File watcher started successfully"
 )
 process.terminate()
 process.wait()
 return True
 else:
 stdout, stderr = process.communicate()
 self.log_test(
 "File Watcher Startup", False, f"Failed to start: {stderr}"
 )
 return False

 except Exception as e:
 self.log_test("File Watcher Startup", False, f"Exception: {e}")
 return False

 def test_watcher_script_execution(self):
 """Test that watcher scripts are executed when files change."""
 logger.info("🧪 Testing watcher script execution...")

 # Start file watcher
 process = subprocess.Popen(
 [sys.executable, "utils/bin/file_watcher.py", "--target-dir", "html"],
 stdout=subprocess.PIPE,
 stderr=subprocess.PIPE,
 text=True,
 )

 try:
 # Give it time to start
 time.sleep(2)

 # Modify test file
 with open(self.test_file, "a") as f:
 f.write("\n\n# Modified content")

 # Give it time to process
 time.sleep(3)

 # Check output for watcher execution
 stdout, stderr = process.communicate()

 if "Test watcher executed" in stdout:
 self.log_test(
 "Watcher Script Execution",
 True,
 "Watcher script executed correctly",
 )
 return True
 else:
 self.log_test(
 "Watcher Script Execution",
 False,
 f"No execution detected. Output: {stdout}",
 )
 return False

 finally:
 process.terminate()
 process.wait()

 def test_dynamic_reloading(self):
 """Test that new watcher scripts are detected and loaded."""
 logger.info("🧪 Testing dynamic reloading...")

 # Start file watcher
 process = subprocess.Popen(
 [sys.executable, "utils/bin/file_watcher.py", "--target-dir", "html"],
 stdout=subprocess.PIPE,
 stderr=subprocess.PIPE,
 text=True,
 )

 try:
 # Give it time to start
 time.sleep(2)

 # Create a new watcher script
 new_watcher = (
 self.base_dir / "utils" / "bin" / "watchers" / "new_test_watcher.py"
 )
 with open(new_watcher, "w") as f:
 f.write(
 """#!/usr/bin/env python3
import sys
print(f"New watcher loaded for {sys.argv[1]}")
"""
 )

 # Give it time to detect
 time.sleep(2)

 # Check output for detection message
 stdout, stderr = process.communicate()

 if "New watcher script detected" in stdout:
 self.log_test(
 "Dynamic Reloading", True, "New watcher script detected correctly"
 )
 new_watcher.unlink() # Clean up
 return True
 else:
 self.log_test(
 "Dynamic Reloading",
 False,
 f"No detection message. Output: {stdout}",
 )
 new_watcher.unlink() # Clean up
 return False

 finally:
 process.terminate()
 process.wait()

 def test_jekyll_service_integration(self):
 """Test Jekyll service integration with file watcher."""
 logger.info("🧪 Testing Jekyll service integration...")

 try:
 # Test help command with new flags
 result = subprocess.run(
 ["./utils/bin/jekyll-service", "--help"],
 capture_output=True,
 text=True,
 cwd=self.base_dir,
 )

 if result.returncode == 0 and "-j, --jekyll-only" in result.stdout:
 self.log_test(
 "Jekyll Service Help", True, "Help command shows new flags"
 )
 else:
 self.log_test(
 "Jekyll Service Help", False, "Help command failed or missing flags"
 )
 return False

 # Test watcher-only start (should fail gracefully if no watcher running)
 result = subprocess.run(
 ["./utils/bin/jekyll-service", "start", "-w"],
 capture_output=True,
 text=True,
 cwd=self.base_dir,
 )

 # Should start watcher successfully
 if result.returncode == 0:
 self.log_test(
 "Jekyll Service Watcher Start", True, "Watcher started successfully"
 )

 # Stop watcher
 subprocess.run(
 ["./utils/bin/jekyll-service", "stop", "-w"],
 capture_output=True,
 text=True,
 cwd=self.base_dir,
 )
 else:
 self.log_test(
 "Jekyll Service Watcher Start",
 False,
 f"Failed to start watcher: {result.stderr}",
 )
 return False

 return True

 except Exception as e:
 self.log_test("Jekyll Service Integration", False, f"Exception: {e}")
 return False

 def test_error_handling(self):
 """Test error handling in watcher scripts."""
 logger.info("🧪 Testing error handling...")

 # Create a broken watcher script
 broken_watcher = (
 self.base_dir / "utils" / "bin" / "watchers" / "broken_watcher.py"
 )
 with open(broken_watcher, "w") as f:
 f.write(
 """#!/usr/bin/env python3
# This script has a syntax error
print("This will cause an error"
"""
 )

 # Start file watcher
 process = subprocess.Popen(
 [sys.executable, "utils/bin/file_watcher.py", "--target-dir", "html"],
 stdout=subprocess.PIPE,
 stderr=subprocess.PIPE,
 text=True,
 )

 try:
 # Give it time to start
 time.sleep(2)

 # Modify test file to trigger watcher
 with open(self.test_file, "a") as f:
 f.write("\n\n# Trigger broken watcher")

 # Give it time to process
 time.sleep(3)

 # Check that the watcher didn't crash
 if process.poll() is None:
 self.log_test(
 "Error Handling", True, "Watcher handled broken script gracefully"
 )
 process.terminate()
 process.wait()
 broken_watcher.unlink() # Clean up
 return True
 else:
 stdout, stderr = process.communicate()
 self.log_test("Error Handling", False, f"Watcher crashed: {stderr}")
 broken_watcher.unlink() # Clean up
 return False

 finally:
 if process.poll() is None:
 process.terminate()
 process.wait()
 broken_watcher.unlink() # Clean up

 def run_all_tests(self):
 """Run all tests and report results."""
 logger.info("🚀 Starting File Watcher Test Suite")
 logger.info("=" * 50)

 try:
 self.setup_test_environment()

 # Run tests
 tests = [
 ("File Watcher Startup", self.test_file_watcher_startup),
 ("Watcher Script Execution", self.test_watcher_script_execution),
 ("Dynamic Reloading", self.test_dynamic_reloading),
 ("Jekyll Service Integration", self.test_jekyll_service_integration),
 ("Error Handling", self.test_error_handling),
 ]

 for test_name, test_func in tests:
 logger.info(f"\n{'='*20} {test_name} {'='*20}")
 try:
 test_func()
 except Exception as e:
 self.log_test(test_name, False, f"Test exception: {e}")

 finally:
 self.cleanup_test_environment()

 # Report results
 logger.info("\n" + "=" * 50)
 logger.info("📊 TEST RESULTS SUMMARY")
 logger.info("=" * 50)

 passed = sum(1 for _, result, _ in self.results if result)
 total = len(self.results)

 for test_name, result, message in self.results:
 status = "✅ PASS" if result else "❌ FAIL"
 logger.info(f"{status} {test_name}")
 if message and self.verbose:
 logger.info(f" {message}")

 logger.info(f"\nOverall: {passed}/{total} tests passed")

 if passed == total:
 logger.info("🎉 All tests passed! File watcher system is ready.")
 return True
 else:
 logger.error("💥 Some tests failed. Please review the issues above.")
 return False


def main():
 parser = argparse.ArgumentParser(description="Test the file watcher system")
 parser.add_argument(
 "--verbose", "-v", action="store_true", help="Show detailed test messages"
 )

 args = parser.parse_args()

 tester = FileWatcherTester(verbose=args.verbose)
 success = tester.run_all_tests()

 sys.exit(0 if success else 1)


if __name__ == "__main__":
 main()

