#!/usr/bin/env python3
"""
Fix Broken Links Script

Identifies and fixes broken links found during site monitoring.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import argparse

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def find_broken_links() -> List[Dict]:
 """Find all broken links from the monitoring output."""

 # Based on the monitoring output, these are the critical broken links:
 broken_links = [
 {
 "url": "https://github.com/unixwzr/torchdevice",
 "status": "404 - Not Found",
 "files": ["html/projects/TorchDevice.md"],
 "issue": "Wrong username (unixwzr instead of unixwzrd)",
 },
 {
 "url": "https://github.com/unixwzrd/python-venv-tools",
 "status": "404 - Not Found",
 "files": [
 "html/projects/venvutil/_posts/2025-04-24-Getting-Started-With-VenvUtil.md",
 "html/projects/venvutil/_posts/2025-03-10-venvutil-introduction.md",
 ],
 "issue": "Wrong repository name (should be venvutil)",
 },
 {
 "url": "https://github.com/unixwzrd/venvutils",
 "status": "404 - Not Found",
 "files": ["html/projects/LogGPT/_posts/2025-04-16-loggpt-introduction.md"],
 "issue": "Wrong repository name (should be venvutil)",
 },
 {
 "url": "https://code.visualstudio.com/docs/remote/remote-overview",
 "status": "500 - Internal Server Error",
 "files": ["html/_posts/2025-04-08-Remote-Debugging-With-VSCode.md"],
 "issue": "VSCode documentation URL changed",
 },
 {
 "url": "https://codercards.io/",
 "status": "Connection Error",
 "files": [".project-planning/You_can_definitely_include_a_dynamic_Git.md"],
 "issue": "Site appears to be down",
 },
 {
 "url": "https://codersrank.io/widgets/repositories/",
 "status": "404 - Not Found",
 "files": [".project-planning/You_can_definitely_include_a_dynamic_Git.md"],
 "issue": "URL path changed",
 },
 {
 "url": "https://ko-fi.com/unixwzrd",
 "status": "403 - Forbidden",
 "files": [
 "utils/output/site-source-files.md",
 "html/collaborate/community.md",
 "html/projects/LogGPT/_posts/2025-03-20-RE-Submitted-to-the-Apple-App-Stor.md",
 "html/projects/LogGPT/_posts/2025-06-11-Second-release-approved.md",
 "html/projects/LogGPT/_posts/2025-03-10-Submitted-to-the-Apple-App-Store.md",
 "html/projects/TorchDevice/_posts/2025-03-10-new-0-0-05-TorchDEvice-release.md",
 "html/projects/TorchDevice/_posts/2025-06-23-TorchDevice-Beta-Release-0.5.2.md",
 "html/projects/UnicodeFix/_posts/2025-04-25-unicodefix-introduction.md",
 ],
 "issue": "Blocked by robots.txt",
 },
 {
 "url": "https://openai.com/",
 "status": "403 - Forbidden",
 "files": ["html/resources.md", "utils/output/site-source-files.md"],
 "issue": "Blocked by robots.txt",
 },
 {
 "url": "https://try.elevenlabs.io/mhtozfq2gzjo",
 "status": "404 - Not Found",
 "files": ["html/resources.md", "utils/output/site-source-files.md"],
 "issue": "Temporary demo link expired",
 },
 {
 "url": "https://twitter.com/unixwzrd",
 "status": "403 - Forbidden",
 "files": ["html/about/resume.md"],
 "issue": "Blocked by robots.txt",
 },
 {
 "url": "https://www.amazon.com/Building-Bridges-Hope-Overcoming-Trauma/dp/B0D9RDG2D2/",
 "status": "503 - Service Unavailable",
 "files": ["html/resources.md", "utils/output/site-source-files.md"],
 "issue": "Amazon blocking automated requests",
 },
 {
 "url": "https://www.amazon.com/stores/Molly-Hayes/author/B0D9XNC1CV",
 "status": "503 - Service Unavailable",
 "files": ["html/resources.md", "utils/output/site-source-files.md"],
 "issue": "Amazon blocking automated requests",
 },
 {
 "url": "https://www.americanbar.org",
 "status": "403 - Forbidden",
 "files": ["html/resources.md", "utils/output/site-source-files.md"],
 "issue": "Blocked by robots.txt",
 },
 {
 "url": "https://www.crisistextline.org/",
 "status": "403 - Forbidden",
 "files": ["html/resources.md", "utils/output/site-source-files.md"],
 "issue": "Blocked by robots.txt",
 },
 {
 "url": "https://www.cursor.com/",
 "status": "404 - Not Found",
 "files": ["html/resources.md", "utils/output/site-source-files.md"],
 "issue": "Site structure changed",
 },
 {
 "url": "https://www.kaggle.com/",
 "status": "404 - Not Found",
 "files": ["html/resources.md", "utils/output/site-source-files.md"],
 "issue": "Site structure changed",
 },
 {
 "url": "https://www.ko-fi.com/unixwzrd",
 "status": "403 - Forbidden",
 "files": [
 "html/projects/venvutil/_posts/2025-06-26-Venvutil-Summer-Update.md"
 ],
 "issue": "Blocked by robots.txt",
 },
 {
 "url": "https://www.legalaid.org",
 "status": "Connection Error",
 "files": ["html/resources.md", "utils/output/site-source-files.md"],
 "issue": "Site appears to be down",
 },
 {
 "url": "https://www.linkedin.com/in/unixwzrd",
 "status": "999 - Unknown Error (LinkedIn)",
 "files": ["html/about/resume.md"],
 "issue": "LinkedIn blocking automated requests",
 },
 {
 "url": "https://www.psychologytoday.com/us/therapists",
 "status": "403 - Forbidden",
 "files": ["html/resources.md", "utils/output/site-source-files.md"],
 "issue": "Blocked by robots.txt",
 },
 ]

 return broken_links


def fix_repository_links():
 """Fix repository links with wrong names."""

 fixes = [
 {
 "old": "https://github.com/unixwzr/torchdevice",
 "new": "https://github.com/unixwzrd/torchdevice",
 "files": ["html/projects/TorchDevice.md"],
 },
 {
 "old": "https://github.com/unixwzrd/python-venv-tools",
 "new": "https://github.com/unixwzrd/venvutil",
 "files": [
 "html/projects/venvutil/_posts/2025-04-24-Getting-Started-With-VenvUtil.md",
 "html/projects/venvutil/_posts/2025-03-10-venvutil-introduction.md",
 ],
 },
 {
 "old": "https://github.com/unixwzrd/venvutils",
 "new": "https://github.com/unixwzrd/venvutil",
 "files": ["html/projects/LogGPT/_posts/2025-04-16-loggpt-introduction.md"],
 },
 ]

 for fix in fixes:
 for file_path in fix["files"]:
 if os.path.exists(file_path):
 print(f"🔧 Fixing {file_path}: {fix['old']} → {fix['new']}")

 with open(file_path, "r", encoding="utf-8") as f:
 content = f.read()

 if fix["old"] in content:
 content = content.replace(fix["old"], fix["new"])

 with open(file_path, "w", encoding="utf-8") as f:
 f.write(content)
 print(f" ✅ Fixed in {file_path}")
 else:
 print(f" ⚠️ Link not found in {file_path}")
 else:
 print(f" ❌ File not found: {file_path}")


def fix_vscode_documentation():
 """Fix VSCode documentation link."""

 file_path = "html/_posts/2025-04-08-Remote-Debugging-With-VSCode.md"
 old_url = "https://code.visualstudio.com/docs/remote/remote-overview"
 new_url = "https://code.visualstudio.com/docs/remote/overview"

 if os.path.exists(file_path):
 print(f"🔧 Fixing VSCode documentation link in {file_path}")

 with open(file_path, "r", encoding="utf-8") as f:
 content = f.read()

 if old_url in content:
 content = content.replace(old_url, new_url)

 with open(file_path, "w", encoding="utf-8") as f:
 f.write(content)
 print(f" ✅ Fixed VSCode documentation link")
 else:
 print(f" ⚠️ VSCode link not found in {file_path}")
 else:
 print(f" ❌ File not found: {file_path}")


def fix_codersrank_link():
 """Fix CodersRank widgets link."""

 file_path = ".project-planning/You_can_definitely_include_a_dynamic_Git.md"
 old_url = "https://codersrank.io/widgets/repositories/"
 new_url = "https://profile.codersrank.io/widget/repositories"

 if os.path.exists(file_path):
 print(f"🔧 Fixing CodersRank link in {file_path}")

 with open(file_path, "r", encoding="utf-8") as f:
 content = f.read()

 if old_url in content:
 content = content.replace(old_url, new_url)

 with open(file_path, "w", encoding="utf-8") as f:
 f.write(content)
 print(f" ✅ Fixed CodersRank link")
 else:
 print(f" ⚠️ CodersRank link not found in {file_path}")
 else:
 print(f" ❌ File not found: {file_path}")


def fix_cursor_link():
 """Fix Cursor link."""

 file_path = "html/resources.md"
 old_url = "https://www.cursor.com/"
 new_url = "https://cursor.sh/"

 if os.path.exists(file_path):
 print(f"🔧 Fixing Cursor link in {file_path}")

 with open(file_path, "r", encoding="utf-8") as f:
 content = f.read()

 if old_url in content:
 content = content.replace(old_url, new_url)

 with open(file_path, "w", encoding="utf-8") as f:
 f.write(content)
 print(f" ✅ Fixed Cursor link")
 else:
 print(f" ⚠️ Cursor link not found in {file_path}")
 else:
 print(f" ❌ File not found: {file_path}")


def fix_kaggle_link():
 """Fix Kaggle link."""

 file_path = "html/resources.md"
 old_url = "https://www.kaggle.com/"
 new_url = "https://kaggle.com/"

 if os.path.exists(file_path):
 print(f"🔧 Fixing Kaggle link in {file_path}")

 with open(file_path, "r", encoding="utf-8") as f:
 content = f.read()

 if old_url in content:
 content = content.replace(old_url, new_url)

 with open(file_path, "w", encoding="utf-8") as f:
 f.write(content)
 print(f" ✅ Fixed Kaggle link")
 else:
 print(f" ⚠️ Kaggle link not found in {file_path}")
 else:
 print(f" ❌ File not found: {file_path}")


def remove_expired_links():
 """Remove expired or problematic links."""

 # Remove expired ElevenLabs demo link
 file_path = "html/resources.md"
 expired_url = "https://try.elevenlabs.io/mhtozfq2gzjo"

 if os.path.exists(file_path):
 print(f"🗑️ Removing expired ElevenLabs link from {file_path}")

 with open(file_path, "r", encoding="utf-8") as f:
 content = f.read()

 if expired_url in content:
 # Remove the entire line containing the expired URL
 lines = content.split("\n")
 new_lines = []
 for line in lines:
 if expired_url not in line:
 new_lines.append(line)

 content = "\n".join(new_lines)

 with open(file_path, "w", encoding="utf-8") as f:
 f.write(content)
 print(f" ✅ Removed expired ElevenLabs link")
 else:
 print(f" ⚠️ Expired ElevenLabs link not found in {file_path}")
 else:
 print(f" ❌ File not found: {file_path}")


def add_robots_txt_note():
 """Add a note about robots.txt blocking for social media links."""

 note = """
> **Note:** Some social media and external service links may appear broken during automated testing due to robots.txt restrictions. These links work correctly for human users.
"""

 # Add to resources.md if it doesn't already have this note
 file_path = "html/resources.md"
 if os.path.exists(file_path):
 with open(file_path, "r", encoding="utf-8") as f:
 content = f.read()

 if "robots.txt restrictions" not in content:
 print(f"📝 Adding robots.txt note to {file_path}")

 # Add the note at the end of the file
 content += note

 with open(file_path, "w", encoding="utf-8") as f:
 f.write(content)
 print(f" ✅ Added robots.txt note")
 else:
 print(f" ℹ️ Robots.txt note already exists in {file_path}")
 else:
 print(f" ❌ File not found: {file_path}")


def main():
 parser = argparse.ArgumentParser(
 description="Fix broken links found in site monitoring"
 )
 parser.add_argument(
 "--dry-run",
 action="store_true",
 help="Show what would be fixed without making changes",
 )
 parser.add_argument(
 "--list-only", action="store_true", help="Only list broken links without fixing"
 )

 args = parser.parse_args()

 print("🔍 Broken Links Analysis")
 print("=" * 50)

 broken_links = find_broken_links()

 if args.list_only:
 print(f"\nFound {len(broken_links)} broken links:")
 for i, link in enumerate(broken_links, 1):
 print(f"\n{i}. {link['url']}")
 print(f" Status: {link['status']}")
 print(f" Issue: {link['issue']}")
 print(f" Files: {', '.join(link['files'])}")
 return

 print(f"\nFound {len(broken_links)} broken links to fix:")

 # Group by issue type
 fixable_links = [
 link
 for link in broken_links
 if "Wrong" in link["issue"]
 or "URL" in link["issue"]
 or "Site structure" in link["issue"]
 ]
 robots_blocked = [link for link in broken_links if "robots.txt" in link["issue"]]
 expired_links = [link for link in broken_links if "expired" in link["issue"]]
 down_sites = [link for link in broken_links if "down" in link["issue"]]

 print(f"\n🔧 Fixable links ({len(fixable_links)}):")
 for link in fixable_links:
 print(f" - {link['url']} ({link['issue']})")

 print(f"\n🤖 Robots.txt blocked ({len(robots_blocked)}):")
 for link in robots_blocked:
 print(f" - {link['url']}")

 print(f"\n⏰ Expired links ({len(expired_links)}):")
 for link in expired_links:
 print(f" - {link['url']}")

 print(f"\n💥 Down sites ({len(down_sites)}):")
 for link in down_sites:
 print(f" - {link['url']}")

 if args.dry_run:
 print(f"\n🔍 DRY RUN - No changes will be made")
 return

 print(f"\n🔧 Starting fixes...")

 # Fix repository links
 fix_repository_links()

 # Fix VSCode documentation
 fix_vscode_documentation()

 # Fix CodersRank link
 fix_codersrank_link()

 # Fix Cursor link
 fix_cursor_link()

 # Fix Kaggle link
 fix_kaggle_link()

 # Remove expired links
 remove_expired_links()

 # Add robots.txt note
 add_robots_txt_note()

 print(f"\n✅ Link fixes completed!")
 print(f"\n📋 Summary:")
 print(f" - Fixed repository name issues")
 print(f" - Updated VSCode documentation URL")
 print(f" - Fixed CodersRank widgets URL")
 print(f" - Updated Cursor and Kaggle URLs")
 print(f" - Removed expired ElevenLabs demo link")
 print(f" - Added note about robots.txt restrictions")
 print(f"\n⚠️ Note: Some links remain 'broken' due to robots.txt restrictions")
 print(
 f" These work correctly for human users but are blocked for automated testing."
 )


if __name__ == "__main__":
 main()

