#!/usr/bin/env python3
"""
Fix Internal Links Script

Fixes internal link and permalink case sensitivity issues that will break on GitHub Pages.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import argparse

def fix_permalink_case_issues():
    """Fix permalink case sensitivity issues."""

    permalink_fixes = [
        # Fix project permalinks to match expected paths
        {
            'file': 'html/projects/LogGPT.md',
            'old_permalink': '/projects/LogGPT/',
            'new_permalink': '/LogGPT/'
        },
        {
            'file': 'html/projects/Case-Analytics.md',
            'old_permalink': '/projects/Case-Analytics/',
            'new_permalink': '/Case-Analytics/'
        },
        {
            'file': 'html/projects/UnicodeFix.md',
            'old_permalink': '/projects/UnicodeFix/',
            'new_permalink': '/UnicodeFix/'
        },
        {
            'file': 'html/projects/text-generation-webui-macos.md',
            'old_permalink': '/projects/text-generation-webui-macos/',
            'new_permalink': '/text-generation-webui-macos/'
        },
        {
            'file': 'html/projects/oobabooga-macOS.md',
            'old_permalink': '/projects/oobabooga-macOS/',
            'new_permalink': '/oobabooga-macOS/'
        },
        {
            'file': 'html/projects/TorchDevice.md',
            'old_permalink': '/projects/TorchDevice/',
            'new_permalink': '/TorchDevice/'
        },
        {
            'file': 'html/projects/venvutil.md',
            'old_permalink': '/projects/venvutil/',
            'new_permalink': '/venvutil/'
        },
        # Fix other permalink issues
        {
            'file': 'html/resources/emergency-resources.md',
            'old_permalink': '/resources/emergency-resources/',
            'new_permalink': '/emergency-resources/'
        },
        {
            'file': 'html/about/resume.md',
            'old_permalink': '/about/resume/',
            'new_permalink': '/resume/'
        },
        {
            'file': 'html/about/sullivan-michael-creds.md',
            'old_permalink': '/about/credentials/',
            'new_permalink': '/sullivan-michael-creds/'
        },
        {
            'file': 'html/collaborate/professionals.md',
            'old_permalink': '/collaborate/professionals/',
            'new_permalink': '/professionals/'
        },
        {
            'file': 'html/collaborate/community.md',
            'old_permalink': '/collaborate/community/',
            'new_permalink': '/community/'
        },
        {
            'file': 'html/hidden/sitemap.md',
            'old_permalink': '/hidden/sitemap/',
            'new_permalink': '/sitemap/'
        }
    ]

    for fix in permalink_fixes:
        if os.path.exists(fix['file']):
            print(f"🔧 Fixing permalink in {fix['file']}: {fix['old_permalink']} → {fix['new_permalink']}")

            with open(fix['file'], 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace permalink in front matter
            if f"permalink: {fix['old_permalink']}" in content:
                content = content.replace(f"permalink: {fix['old_permalink']}", f"permalink: {fix['new_permalink']}")

                with open(fix['file'], 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ Fixed permalink")
            else:
                print(f"   ⚠️ Permalink not found in {fix['file']}")
        else:
            print(f"   ❌ File not found: {fix['file']}")

def fix_internal_link_issues():
    """Fix internal link case sensitivity and path issues."""

    link_fixes = [
        # Fix missing trailing slashes
        {
            'old': '/contact',
            'new': '/contact/',
            'files': [
                'html/resources.md',
                'html/about.md',
                'html/projects/Case-Analytics.md',
                'html/projects/venvutil.md',
                'html/resources/emergency-resources.md',
                'html/about/resume.md',
                'html/collaborate/professionals.md',
                'html/collaborate/community.md'
            ]
        },
        {
            'old': '/resources',
            'new': '/resources/',
            'files': [
                'html/contact.md',
                'html/collaborate/community.md'
            ]
        },
        {
            'old': '/projects',
            'new': '/projects/',
            'files': [
                'html/collaborate/community.md'
            ]
        },
        # Fix specific path issues
        {
            'old': '/about/sullivan-michael-creds',
            'new': '/about/credentials/',
            'files': [
                'html/about/resume.md'
            ]
        },
        {
            'old': '/assets/documents/SullivanMichael_IT_AI_ML_Unix_52050111.pdf',
            'new': '/assets/documents/SullivanMichael_IT_AI_ML_Unix_52050111.pdf',
            'files': [
                'html/about/resume.md'
            ]
        },
        # Fix blog post permalink
        {
            'old': 'permalink: /blog/',
            'new': 'permalink: /2024/09/27/Building-This-Site-With-AI/',
            'files': [
                'html/_posts/2024-09-27-Building-This-Site-With-AI.md'
            ]
        }
    ]

    for fix in link_fixes:
        for file_path in fix['files']:
            if os.path.exists(file_path):
                print(f"🔧 Fixing internal link in {file_path}: {fix['old']} → {fix['new']}")

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if fix['old'] in content:
                    content = content.replace(fix['old'], fix['new'])

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"   ✅ Fixed in {file_path}")
                else:
                    print(f"   ⚠️ Link not found in {file_path}")
            else:
                print(f"   ❌ File not found: {file_path}")

def fix_missing_assets():
    """Fix missing asset references."""

    # Check if the default OG image exists
    og_image_path = 'html/assets/images/default-og-image.png'
    if not os.path.exists(og_image_path):
        print(f"⚠️ Missing asset: {og_image_path}")
        # Create a placeholder or copy from another image
        if os.path.exists('html/assets/images/No_Image_for_Project.png'):
            import shutil
            shutil.copy('html/assets/images/No_Image_for_Project.png', og_image_path)
            print(f"   ✅ Created placeholder from existing image")

    # Check if the PDF document exists
    pdf_path = 'html/assets/documents/SullivanMichael_IT_AI_ML_Unix_52050111.pdf'
    if not os.path.exists(pdf_path):
        print(f"⚠️ Missing asset: {pdf_path}")
        print(f"   Please ensure the PDF file exists at this location")

def validate_fixes():
    """Validate that the fixes resolved the issues."""

    print("\n🔍 Validating fixes...")

    # Run the permalink validation script again
    import subprocess
    result = subprocess.run(['python3', 'utils/bin/validate_permalink_consistency.py'],
                          capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ All permalink and internal link issues resolved!")
    else:
        print("⚠️ Some issues may remain:")
        print(result.stdout)

def main():
    parser = argparse.ArgumentParser(description='Fix internal link and permalink case sensitivity issues')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed without making changes')
    parser.add_argument('--validate-only', action='store_true', help='Only validate current state')

    args = parser.parse_args()

    print("🔍 Internal Links and Permalinks Analysis")
    print("=" * 50)

    if args.validate_only:
        validate_fixes()
        return

    if args.dry_run:
        print("🔍 DRY RUN - No changes will be made")
        print("\nWould fix the following issues:")
        print("1. Project permalinks to match expected paths")
        print("2. Missing trailing slashes in internal links")
        print("3. Incorrect asset references")
        print("4. Blog post permalink consistency")
        return

    print(f"\n🔧 Starting internal link and permalink fixes...")

    # Fix permalink case issues
    fix_permalink_case_issues()

    # Fix internal link issues
    fix_internal_link_issues()

    # Fix missing assets
    fix_missing_assets()

    # Validate the fixes
    validate_fixes()

    print(f"\n✅ Internal link and permalink fixes completed!")
    print(f"\n📋 Summary:")
    print(f"   - Fixed project permalinks to match expected paths")
    print(f"   - Added missing trailing slashes to internal links")
    print(f"   - Fixed asset references")
    print(f"   - Corrected blog post permalinks")
    print(f"\n⚠️ Note: These fixes ensure compatibility with GitHub Pages")
    print(f"   where case sensitivity matters for file paths.")

if __name__ == "__main__":
    main() 