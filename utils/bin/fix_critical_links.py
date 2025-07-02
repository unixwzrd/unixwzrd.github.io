#!/usr/bin/env python3
"""
Fix Critical Internal Links Script

Fixes ONLY the most critical internal link and permalink issues that will break the site on GitHub Pages.
Focuses on project permalinks and missing trailing slashes first.
"""

import os
import re
import sys
from pathlib import Path

def fix_project_permalinks():
    """Fix the most critical project permalink issues."""

    print("🔧 Fixing critical project permalinks...")

    project_fixes = [
        {
            'file': 'html/projects/LogGPT.md',
            'old': 'permalink: /projects/LogGPT/',
            'new': 'permalink: /LogGPT/'
        },
        {
            'file': 'html/projects/Case-Analytics.md',
            'old': 'permalink: /projects/Case-Analytics/',
            'new': 'permalink: /Case-Analytics/'
        },
        {
            'file': 'html/projects/UnicodeFix.md',
            'old': 'permalink: /projects/UnicodeFix/',
            'new': 'permalink: /UnicodeFix/'
        },
        {
            'file': 'html/projects/text-generation-webui-macos.md',
            'old': 'permalink: /projects/text-generation-webui-macos/',
            'new': 'permalink: /text-generation-webui-macos/'
        },
        {
            'file': 'html/projects/oobabooga-macOS.md',
            'old': 'permalink: /projects/oobabooga-macOS/',
            'new': 'permalink: /oobabooga-macOS/'
        },
        {
            'file': 'html/projects/TorchDevice.md',
            'old': 'permalink: /projects/TorchDevice/',
            'new': 'permalink: /TorchDevice/'
        },
        {
            'file': 'html/projects/venvutil.md',
            'old': 'permalink: /projects/venvutil/',
            'new': 'permalink: /venvutil/'
        }
    ]

    fixed_count = 0
    for fix in project_fixes:
        if os.path.exists(fix['file']):
            print(f"   Checking {fix['file']}...")

            with open(fix['file'], 'r', encoding='utf-8') as f:
                content = f.read()

            if fix['old'] in content:
                content = content.replace(fix['old'], fix['new'])

                with open(fix['file'], 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ Fixed: {fix['old']} → {fix['new']}")
                fixed_count += 1
            else:
                print(f"   ⚠️ Permalink not found in {fix['file']}")
        else:
            print(f"   ❌ File not found: {fix['file']}")

    print(f"   📊 Fixed {fixed_count} project permalinks")
    return fixed_count

def fix_missing_trailing_slashes():
    """Fix missing trailing slashes in internal links."""

    print("\n🔧 Fixing missing trailing slashes...")

    slash_fixes = [
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
        }
    ]

    fixed_count = 0
    for fix in slash_fixes:
        for file_path in fix['files']:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if fix['old'] in content:
                    content = content.replace(fix['old'], fix['new'])

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"   ✅ Fixed {fix['old']} → {fix['new']} in {file_path}")
                    fixed_count += 1
            else:
                print(f"   ❌ File not found: {file_path}")

    print(f"   📊 Fixed {fixed_count} missing trailing slash issues")
    return fixed_count

def create_missing_assets():
    """Create or fix missing asset references."""

    print("\n🔧 Checking missing assets...")

    # Check default OG image
    og_image_path = 'html/assets/images/default-og-image.png'
    if not os.path.exists(og_image_path):
        print(f"   ⚠️ Missing: {og_image_path}")
        # Try to create from existing image
        if os.path.exists('html/assets/images/No_Image_for_Project.png'):
            import shutil
            shutil.copy('html/assets/images/No_Image_for_Project.png', og_image_path)
            print(f"   ✅ Created placeholder from existing image")
        else:
            print(f"   ❌ No suitable replacement image found")

    # Check PDF document
    pdf_path = 'html/assets/documents/SullivanMichael_IT_AI_ML_Unix_52050111.pdf'
    if not os.path.exists(pdf_path):
        print(f"   ⚠️ Missing: {pdf_path}")
        print(f"   📝 Please ensure this PDF file exists")

def validate_critical_fixes():
    """Validate that the critical fixes resolved the main issues."""

    print("\n🔍 Validating critical fixes...")

    # Run the permalink validation script
    import subprocess
    result = subprocess.run(['python3', 'utils/bin/validate_permalink_consistency.py'],
                          capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ All critical permalink and internal link issues resolved!")
        return True
    else:
        print("⚠️ Some critical issues may remain:")
        # Count remaining issues
        lines = result.stdout.split('\n')
        critical_issues = [line for line in lines if '❌' in line and ('projects/' in line or 'contact' in line or 'resources' in line)]
        print(f"   📊 {len(critical_issues)} critical issues remaining")
        return False

def main():
    print("🔍 Critical Internal Links Fix")
    print("=" * 40)
    print("Focusing on issues that will break the site on GitHub Pages")
    print()

    # Step 1: Fix project permalinks
    project_fixes = fix_project_permalinks()

    # Step 2: Fix missing trailing slashes
    slash_fixes = fix_missing_trailing_slashes()

    # Step 3: Check missing assets
    create_missing_assets()

    # Step 4: Validate fixes
    success = validate_critical_fixes()

    print(f"\n📋 Summary:")
    print(f"   - Fixed {project_fixes} project permalinks")
    print(f"   - Fixed {slash_fixes} missing trailing slash issues")
    print(f"   - Checked missing assets")

    if success:
        print(f"\n✅ Critical fixes completed successfully!")
        print(f"   The site should now work properly on GitHub Pages")
    else:
        print(f"\n⚠️ Some critical issues may remain")
        print(f"   Check the validation output above for details")

    print(f"\n📝 Note: Secondary permalink issues have been documented")
    print(f"   in .project-planning/tmp/critical-link-fixes.md for later review")

if __name__ == "__main__":
    main() 