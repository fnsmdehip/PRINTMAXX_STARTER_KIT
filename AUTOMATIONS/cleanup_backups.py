#!/usr/bin/env python3
"""Clean up old backup files and archives"""

import shutil
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def cleanup_backups():
    """Remove old backup files"""
    print("Cleaning old backup files...\n")

    total_freed_mb = 0
    count = 0

    # Find all backup files
    backup_pattern = "*.backup_*"
    for backup_file in PROJECT_ROOT.rglob(backup_pattern):
        # Extract date from filename (format: backup_YYYYMMDD_HHMMSS)
        try:
            parts = backup_file.stem.split("_")
            if len(parts) >= 2:
                date_str = parts[-2]
                time_str = parts[-1]
                backup_date = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")

                # Delete if older than 7 days
                if datetime.now() - backup_date > timedelta(days=7):
                    size_mb = backup_file.stat().st_size / (1024*1024)
                    backup_file.unlink()
                    count += 1
                    total_freed_mb += size_mb
                    print(f"  Deleted {backup_file.name} ({size_mb:.2f}MB)")
        except:
            pass

    print(f"\n✓ Removed {count} old backups, freed {total_freed_mb:.1f}MB")

    # Also find old archive CSVs
    print("\nScanning for old archive CSVs...")
    for archive in PROJECT_ROOT.rglob("*_ARCHIVE_*.csv"):
        try:
            # Extract date from filename
            filename = archive.name
            if "ARCHIVE" in filename:
                # Format: NAME_ARCHIVE_YYYYMMDD.csv
                date_part = filename.split("ARCHIVE_")[1].replace(".csv", "")
                archive_date = datetime.strptime(date_part, "%Y%m%d")

                # Delete if older than 30 days
                if datetime.now() - archive_date > timedelta(days=30):
                    size_mb = archive.stat().st_size / (1024*1024)
                    archive.unlink()
                    count += 1
                    total_freed_mb += size_mb
                    print(f"  Deleted {archive.name} ({size_mb:.2f}MB)")
        except Exception as e:
            pass

    print(f"\n✓ Total cleanup: {count} files, {total_freed_mb:.1f}MB freed")
    return total_freed_mb

if __name__ == "__main__":
    cleanup_backups()
