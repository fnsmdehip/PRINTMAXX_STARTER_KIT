#!/usr/bin/env python3
"""
backup_manager.py - Auto-backup critical files with versioning

Creates timestamped backups of LEDGER, FINANCIALS, and config files.
Manages backup retention and provides restore capability.

Usage:
    python3 backup_manager.py --backup
    python3 backup_manager.py --backup --targets ledger,financials
    python3 backup_manager.py --list
    python3 backup_manager.py --restore 2026-02-01_143000
    python3 backup_manager.py --cleanup --keep 10

Example:
    # Create backup of all critical files
    python3 backup_manager.py --backup

    # List existing backups
    python3 backup_manager.py --list

    # Keep only last 10 backups
    python3 backup_manager.py --cleanup --keep 10
"""

import argparse
import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
BACKUP_DIR = PROJECT_DIR / "AUTOMATIONS" / "backups"
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "backup_manager.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Backup targets
BACKUP_TARGETS = {
    "ledger": PROJECT_DIR / "LEDGER",
    "financials": PROJECT_DIR / "FINANCIALS",
    "config": PROJECT_DIR / ".claude",
    "ops": PROJECT_DIR / "OPS",
}


def create_backup(targets=None):
    """Create a timestamped backup."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup_path = BACKUP_DIR / timestamp

    if targets is None:
        targets = list(BACKUP_TARGETS.keys())
    else:
        targets = [t.strip() for t in targets]

    total_files = 0
    total_size = 0

    for target_name in targets:
        source = BACKUP_TARGETS.get(target_name)
        if not source or not source.exists():
            logger.warning(f"Backup target not found: {target_name} ({source})")
            continue

        dest = backup_path / target_name

        if source.is_dir():
            # Copy directory, skip large/unnecessary files
            for root, dirs, files in os.walk(source):
                # Skip unwanted directories
                dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__", ".next")]

                rel_root = Path(root).relative_to(source)
                dest_root = dest / rel_root
                dest_root.mkdir(parents=True, exist_ok=True)

                for f in files:
                    if f.endswith((".csv", ".md", ".json", ".py", ".ts", ".tsx", ".yml", ".yaml")):
                        src_file = Path(root) / f
                        dst_file = dest_root / f
                        shutil.copy2(src_file, dst_file)
                        total_files += 1
                        total_size += src_file.stat().st_size
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest / source.name)
            total_files += 1
            total_size += source.stat().st_size

    logger.info(
        f"Backup created: {backup_path.name} "
        f"({total_files} files, {total_size / 1024:.0f} KB)"
    )
    return backup_path


def list_backups():
    """List all existing backups."""
    backups = sorted(BACKUP_DIR.iterdir(), reverse=True)
    backups = [b for b in backups if b.is_dir()]

    if not backups:
        print("No backups found.")
        return

    print(f"\n{'=' * 60}")
    print("  BACKUP INVENTORY")
    print(f"{'=' * 60}")

    total_size = 0
    for backup in backups:
        # Calculate size
        size = sum(f.stat().st_size for f in backup.rglob("*") if f.is_file())
        file_count = sum(1 for f in backup.rglob("*") if f.is_file())
        total_size += size

        # Get targets
        targets = [d.name for d in backup.iterdir() if d.is_dir()]

        print(
            f"  {backup.name}  |  "
            f"{file_count:>4} files  |  "
            f"{size / 1024:>7.0f} KB  |  "
            f"Targets: {', '.join(targets)}"
        )

    print(f"\n  Total Backups: {len(backups)}")
    print(f"  Total Size: {total_size / 1024 / 1024:.1f} MB")
    print(f"{'=' * 60}")


def restore_backup(backup_name):
    """Restore from a backup."""
    backup_path = BACKUP_DIR / backup_name

    if not backup_path.exists():
        logger.error(f"Backup not found: {backup_name}")
        return False

    # Create a pre-restore backup first
    logger.info("Creating pre-restore backup...")
    create_backup()

    # Restore each target
    for target_dir in backup_path.iterdir():
        if not target_dir.is_dir():
            continue

        target_name = target_dir.name
        dest = BACKUP_TARGETS.get(target_name)
        if not dest:
            logger.warning(f"Unknown restore target: {target_name}")
            continue

        restored = 0
        for root, dirs, files in os.walk(target_dir):
            rel_root = Path(root).relative_to(target_dir)
            dest_root = dest / rel_root
            dest_root.mkdir(parents=True, exist_ok=True)

            for f in files:
                src = Path(root) / f
                dst = dest_root / f
                shutil.copy2(src, dst)
                restored += 1

        logger.info(f"Restored {target_name}: {restored} files")

    logger.info(f"Restore complete from: {backup_name}")
    return True


def cleanup_backups(keep=10):
    """Remove old backups, keeping the most recent N."""
    backups = sorted(
        [b for b in BACKUP_DIR.iterdir() if b.is_dir()],
        key=lambda x: x.name,
        reverse=True,
    )

    if len(backups) <= keep:
        logger.info(f"Only {len(backups)} backups exist, nothing to clean up")
        return

    to_remove = backups[keep:]
    freed = 0

    for backup in to_remove:
        size = sum(f.stat().st_size for f in backup.rglob("*") if f.is_file())
        freed += size
        shutil.rmtree(backup)
        logger.info(f"Removed: {backup.name}")

    logger.info(f"Cleaned up {len(to_remove)} backups, freed {freed / 1024:.0f} KB")


def main():
    parser = argparse.ArgumentParser(
        description="Manage backups of critical PRINTMAXX files"
    )
    parser.add_argument("--backup", action="store_true", help="Create a new backup")
    parser.add_argument(
        "--targets",
        type=str,
        default=None,
        help="Comma-separated backup targets (ledger,financials,config,ops)",
    )
    parser.add_argument("--list", action="store_true", help="List existing backups")
    parser.add_argument("--restore", type=str, default=None, help="Restore from backup name")
    parser.add_argument("--cleanup", action="store_true", help="Remove old backups")
    parser.add_argument("--keep", type=int, default=10, help="Backups to keep (default: 10)")
    args = parser.parse_args()

    if args.backup:
        targets = args.targets.split(",") if args.targets else None
        create_backup(targets)
    elif args.list:
        list_backups()
    elif args.restore:
        restore_backup(args.restore)
    elif args.cleanup:
        cleanup_backups(args.keep)
    else:
        list_backups()


if __name__ == "__main__":
    main()
