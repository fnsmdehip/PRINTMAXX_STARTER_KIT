#!/usr/bin/env python3
"""
Complete Setup Script for focusprayer-sdk54
Copies all remaining files from the original focusprayer app
"""

import os
import shutil
import sys
from pathlib import Path

def main():
    # Get the directory paths
    script_dir = Path(__file__).parent
    src_dir = script_dir.parent / "focusprayer"
    dest_dir = script_dir

    print("=" * 60)
    print("FocusPrayer SDK 54 - Complete Setup")
    print("=" * 60)
    print()

    # Verify source directory exists
    if not src_dir.exists():
        print(f"❌ Error: Source directory not found: {src_dir}")
        print(f"   This script must be run from focusprayer-sdk54/ directory")
        sys.exit(1)

    print(f"Source:      {src_dir}")
    print(f"Destination: {dest_dir}")
    print()

    # Define directories to copy
    dirs_to_copy = [
        ("src", "src"),
        ("assets", "assets"),
        ("__tests__", "__tests__"),
    ]

    # Copy directories
    print("Copying directories...")
    for src_name, dest_name in dirs_to_copy:
        src_path = src_dir / src_name
        dest_path = dest_dir / dest_name

        if not src_path.exists():
            print(f"  ⚠ Skipped {src_name} (not found in source)")
            continue

        try:
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(src_path, dest_path)
            print(f"  ✓ Copied {src_name}/")
        except Exception as e:
            print(f"  ❌ Failed to copy {src_name}: {e}")
            sys.exit(1)

    # Copy individual app files
    print("\nCopying app screens...")
    app_files = [
        "onboarding.tsx",
        "timer.tsx",
        "scripture.tsx",
        "paywall.tsx",
        "emergency-unlock.tsx",
        "privacy-policy.tsx",
        "terms.tsx",
    ]

    for filename in app_files:
        src_file = src_dir / "app" / filename
        dest_file = dest_dir / "app" / filename

        if not src_file.exists():
            print(f"  ⚠ Skipped {filename} (not found)")
            continue

        try:
            shutil.copy2(src_file, dest_file)
            print(f"  ✓ Copied {filename}")
        except Exception as e:
            print(f"  ❌ Failed to copy {filename}: {e}")
            sys.exit(1)

    # Copy tab screens
    print("\nCopying tab screens...")
    tab_files = ["stats.tsx", "settings.tsx"]
    tabs_dest = dest_dir / "app" / "(tabs)"
    tabs_dest.mkdir(parents=True, exist_ok=True)

    for filename in tab_files:
        src_file = src_dir / "app" / "(tabs)" / filename
        dest_file = tabs_dest / filename

        if not src_file.exists():
            print(f"  ⚠ Skipped {filename} (not found)")
            continue

        try:
            shutil.copy2(src_file, dest_file)
            print(f"  ✓ Copied {filename}")
        except Exception as e:
            print(f"  ❌ Failed to copy {filename}: {e}")
            sys.exit(1)

    print()
    print("=" * 60)
    print("✓ Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. npm install")
    print("  2. npx expo start --ios")
    print()
    print("For more details, see README_SETUP.md")
    print()

if __name__ == "__main__":
    main()
