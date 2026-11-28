#!/usr/bin/env python3
"""
Quick File Watcher Test

Simple manual test to verify file watcher functionality.
"""

import os
import sys
import time
import subprocess
from pathlib import Path


def test_basic_functionality():
    """Test basic file watcher functionality."""
    print("🧪 Testing basic file watcher functionality...")

    # Test 1: Check if file watcher starts
    print("1. Testing file watcher startup...")
    try:
        process = subprocess.Popen(
            [sys.executable, "utils/bin/file_watcher.py", "--target-dir", "html"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        time.sleep(2)

        if process.poll() is None:
            print("   ✅ File watcher started successfully")
            process.terminate()
            process.wait()
        else:
            stdout, stderr = process.communicate()
            print(f"   ❌ File watcher failed to start: {stderr}")
            return False

    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

    # Test 2: Check Jekyll service help
    print("2. Testing Jekyll service integration...")
    try:
        result = subprocess.run(
            ["./utils/bin/jekyll-service", "--help"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )

        if result.returncode == 0 and "-j, --jekyll-only" in result.stdout:
            print("   ✅ Jekyll service shows new flags")
        else:
            print("   ❌ Jekyll service help failed")
            return False

    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

    # Test 3: Check watchers directory
    print("3. Testing watchers directory...")
    watchers_dir = Path("utils/bin/watchers")
    if watchers_dir.exists():
        scripts = list(watchers_dir.glob("*.py"))
        print(f"   ✅ Found {len(scripts)} watcher scripts")
        for script in scripts:
            print(f"      - {script.name}")
    else:
        print("   ❌ Watchers directory not found")
        return False

    print("✅ All basic tests passed!")
    return True


def test_watcher_script():
    """Test creating and running a watcher script."""
    print("\n🧪 Testing watcher script creation and execution...")

    # Create a test watcher script
    test_script = Path("utils/bin/watchers/quick_test_watcher.py")
    script_content = """#!/usr/bin/env python3
import sys
print(f"Quick test watcher executed for {sys.argv[1]}")
"""

    with open(test_script, "w") as f:
        f.write(script_content)

    os.chmod(test_script, 0o755)
    print("   ✅ Created test watcher script")

    # Test running it directly
    try:
        result = subprocess.run(
            [sys.executable, str(test_script), "test_file.md", "modified"],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0 and "Quick test watcher executed" in result.stdout:
            print("   ✅ Test watcher script executed correctly")
        else:
            print(f"   ❌ Test watcher script failed: {result.stderr}")
            test_script.unlink()
            return False

    except Exception as e:
        print(f"   ❌ Exception: {e}")
        test_script.unlink()
        return False

    # Clean up
    test_script.unlink()
    print("   ✅ Cleaned up test script")

    print("✅ Watcher script test passed!")
    return True


def main():
    print("🚀 Quick File Watcher Test")
    print("=" * 40)

    success = True

    if not test_basic_functionality():
        success = False

    if not test_watcher_script():
        success = False

    print("\n" + "=" * 40)
    if success:
        print("🎉 All quick tests passed! File watcher system appears to be working.")
        print(
            "You can now run the full test suite with: python utils/bin/diagnostics/test_file_watcher.py"
        )
    else:
        print("💥 Some tests failed. Please check the issues above.")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

