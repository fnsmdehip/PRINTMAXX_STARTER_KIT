#!/usr/bin/env python3
"""
Session Manager
===============
Manages browser sessions for persistent logins across automation runs.

Features:
- Save and load Playwright browser state
- Organize sessions by account
- Session validation and health checks
- Backup and restore functionality
- Session expiry handling

Usage:
    from session_manager import SessionManager

    manager = SessionManager()

    # Save a session
    manager.save_session("x_faith_main", context)

    # Load a session
    session_path = manager.get_session_path("x_faith_main")

    # List all sessions
    sessions = manager.list_sessions()
"""

import os
import sys
import json
import shutil
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
import hashlib

try:
    from playwright.sync_api import sync_playwright, BrowserContext
except ImportError:
    BrowserContext = Any  # Type hint fallback


# Configure logging
LOG_DIR = Path(__file__).parent.parent.parent / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "session_manager.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("session_manager")


# Default paths
SESSIONS_DIR = Path(__file__).parent.parent.parent / "AUTOMATIONS" / "sessions"
BACKUPS_DIR = SESSIONS_DIR / "backups"
METADATA_FILE = SESSIONS_DIR / "session_metadata.json"


class SessionManager:
    """Manage browser sessions for automation."""

    def __init__(self, sessions_dir: str = None):
        """
        Initialize the session manager.

        Args:
            sessions_dir: Directory to store sessions (default: AUTOMATIONS/sessions)
        """
        self.sessions_dir = Path(sessions_dir) if sessions_dir else SESSIONS_DIR
        self.backups_dir = self.sessions_dir / "backups"
        self.metadata_file = self.sessions_dir / "session_metadata.json"

        # Ensure directories exist
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.backups_dir.mkdir(parents=True, exist_ok=True)

        # Load metadata
        self.metadata = self._load_metadata()

        logger.info(f"Session manager initialized: {self.sessions_dir}")

    def _load_metadata(self) -> Dict[str, Any]:
        """Load session metadata from file."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading metadata: {e}")
        return {"sessions": {}}

    def _save_metadata(self) -> None:
        """Save session metadata to file."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")

    def get_session_path(self, account_id: str) -> str:
        """
        Get the path to a session file for an account.

        Args:
            account_id: The account identifier

        Returns:
            Full path to the session file
        """
        return str(self.sessions_dir / f"{account_id}.json")

    def session_exists(self, account_id: str) -> bool:
        """Check if a session exists for an account."""
        return Path(self.get_session_path(account_id)).exists()

    def save_session(
        self,
        account_id: str,
        context: BrowserContext,
        platform: str = "",
        notes: str = ""
    ) -> bool:
        """
        Save a browser session state.

        Args:
            account_id: The account identifier
            context: Playwright browser context to save
            platform: Platform name (optional)
            notes: Additional notes (optional)

        Returns:
            True if successful
        """
        try:
            session_path = self.get_session_path(account_id)

            # Backup existing session if present
            if Path(session_path).exists():
                self._backup_session(account_id)

            # Save the session state
            context.storage_state(path=session_path)

            # Update metadata
            self.metadata["sessions"][account_id] = {
                "path": session_path,
                "platform": platform,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "notes": notes,
                "checksum": self._calculate_checksum(session_path)
            }
            self._save_metadata()

            logger.info(f"Session saved for {account_id}")
            return True

        except Exception as e:
            logger.error(f"Error saving session for {account_id}: {e}")
            return False

    def save_session_from_file(
        self,
        account_id: str,
        source_path: str,
        platform: str = "",
        notes: str = ""
    ) -> bool:
        """
        Save a session from an existing file.

        Args:
            account_id: The account identifier
            source_path: Path to the existing session file
            platform: Platform name
            notes: Additional notes

        Returns:
            True if successful
        """
        try:
            if not Path(source_path).exists():
                logger.error(f"Source session not found: {source_path}")
                return False

            session_path = self.get_session_path(account_id)

            # Backup existing if present
            if Path(session_path).exists():
                self._backup_session(account_id)

            # Copy the file
            shutil.copy2(source_path, session_path)

            # Update metadata
            self.metadata["sessions"][account_id] = {
                "path": session_path,
                "platform": platform,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "notes": notes,
                "checksum": self._calculate_checksum(session_path)
            }
            self._save_metadata()

            logger.info(f"Session imported for {account_id}")
            return True

        except Exception as e:
            logger.error(f"Error importing session: {e}")
            return False

    def load_session(self, account_id: str) -> Optional[Dict[str, Any]]:
        """
        Load session data for an account.

        Args:
            account_id: The account identifier

        Returns:
            Session storage state dict, or None if not found
        """
        session_path = self.get_session_path(account_id)

        if not Path(session_path).exists():
            logger.warning(f"Session not found for {account_id}")
            return None

        try:
            with open(session_path, 'r') as f:
                session_data = json.load(f)

            # Update last accessed time
            if account_id in self.metadata["sessions"]:
                self.metadata["sessions"][account_id]["last_accessed"] = datetime.now().isoformat()
                self._save_metadata()

            logger.info(f"Session loaded for {account_id}")
            return session_data

        except Exception as e:
            logger.error(f"Error loading session for {account_id}: {e}")
            return None

    def _backup_session(self, account_id: str) -> bool:
        """Create a backup of an existing session."""
        try:
            session_path = Path(self.get_session_path(account_id))
            if not session_path.exists():
                return False

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backups_dir / f"{account_id}_{timestamp}.json"

            shutil.copy2(session_path, backup_path)
            logger.info(f"Session backed up: {backup_path}")

            # Clean old backups (keep last 5)
            self._cleanup_backups(account_id)

            return True

        except Exception as e:
            logger.error(f"Error backing up session: {e}")
            return False

    def _cleanup_backups(self, account_id: str, keep: int = 5) -> None:
        """Remove old backups, keeping only the most recent ones."""
        try:
            backups = sorted(
                self.backups_dir.glob(f"{account_id}_*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )

            for old_backup in backups[keep:]:
                old_backup.unlink()
                logger.info(f"Removed old backup: {old_backup}")

        except Exception as e:
            logger.error(f"Error cleaning backups: {e}")

    def restore_backup(self, account_id: str, backup_index: int = 0) -> bool:
        """
        Restore a session from backup.

        Args:
            account_id: The account identifier
            backup_index: Index of backup to restore (0 = most recent)

        Returns:
            True if successful
        """
        try:
            backups = sorted(
                self.backups_dir.glob(f"{account_id}_*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )

            if backup_index >= len(backups):
                logger.error(f"Backup index {backup_index} not found")
                return False

            backup_path = backups[backup_index]
            session_path = self.get_session_path(account_id)

            shutil.copy2(backup_path, session_path)

            # Update metadata
            if account_id in self.metadata["sessions"]:
                self.metadata["sessions"][account_id]["restored_from"] = str(backup_path)
                self.metadata["sessions"][account_id]["updated_at"] = datetime.now().isoformat()
                self._save_metadata()

            logger.info(f"Session restored from {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False

    def delete_session(self, account_id: str, backup: bool = True) -> bool:
        """
        Delete a session.

        Args:
            account_id: The account identifier
            backup: Create backup before deleting

        Returns:
            True if successful
        """
        try:
            session_path = Path(self.get_session_path(account_id))

            if not session_path.exists():
                logger.warning(f"Session not found: {account_id}")
                return False

            if backup:
                self._backup_session(account_id)

            session_path.unlink()

            if account_id in self.metadata["sessions"]:
                del self.metadata["sessions"][account_id]
                self._save_metadata()

            logger.info(f"Session deleted: {account_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting session: {e}")
            return False

    def _calculate_checksum(self, file_path: str) -> str:
        """Calculate MD5 checksum of a file."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""

    def validate_session(self, account_id: str) -> Dict[str, Any]:
        """
        Validate a session's integrity and freshness.

        Args:
            account_id: The account identifier

        Returns:
            Validation result with status and details
        """
        result = {
            "account_id": account_id,
            "valid": False,
            "exists": False,
            "checksum_ok": False,
            "expired": True,
            "details": ""
        }

        session_path = Path(self.get_session_path(account_id))

        if not session_path.exists():
            result["details"] = "Session file not found"
            return result

        result["exists"] = True

        # Check metadata
        meta = self.metadata["sessions"].get(account_id, {})

        # Verify checksum
        if meta.get("checksum"):
            current_checksum = self._calculate_checksum(str(session_path))
            result["checksum_ok"] = (current_checksum == meta["checksum"])
            if not result["checksum_ok"]:
                result["details"] = "Checksum mismatch (file modified externally)"

        # Check age
        try:
            updated_at = meta.get("updated_at")
            if updated_at:
                updated = datetime.fromisoformat(updated_at)
                age = datetime.now() - updated
                # Consider expired after 7 days
                result["expired"] = age > timedelta(days=7)
                if result["expired"]:
                    result["details"] = f"Session expired (age: {age.days} days)"
            else:
                # Check file modification time
                mtime = datetime.fromtimestamp(session_path.stat().st_mtime)
                age = datetime.now() - mtime
                result["expired"] = age > timedelta(days=7)

        except Exception as e:
            result["details"] = f"Error checking age: {e}"

        # Overall validity
        result["valid"] = result["exists"] and not result["expired"]
        if result["valid"] and not result["details"]:
            result["details"] = "Session is valid"

        return result

    def list_sessions(self) -> List[Dict[str, Any]]:
        """
        List all available sessions with metadata.

        Returns:
            List of session info dictionaries
        """
        sessions = []

        for session_file in self.sessions_dir.glob("*.json"):
            if session_file.name == "session_metadata.json":
                continue

            account_id = session_file.stem
            meta = self.metadata["sessions"].get(account_id, {})

            validation = self.validate_session(account_id)

            sessions.append({
                "account_id": account_id,
                "platform": meta.get("platform", "unknown"),
                "created_at": meta.get("created_at", "unknown"),
                "updated_at": meta.get("updated_at", "unknown"),
                "last_accessed": meta.get("last_accessed"),
                "valid": validation["valid"],
                "expired": validation["expired"],
                "notes": meta.get("notes", ""),
                "file_size": session_file.stat().st_size
            })

        return sessions

    def list_backups(self, account_id: str = None) -> List[Dict[str, Any]]:
        """
        List available backups.

        Args:
            account_id: Filter by account (optional)

        Returns:
            List of backup info dictionaries
        """
        backups = []

        pattern = f"{account_id}_*.json" if account_id else "*.json"

        for backup_file in sorted(self.backups_dir.glob(pattern), reverse=True):
            parts = backup_file.stem.rsplit("_", 2)
            if len(parts) >= 3:
                acc_id = parts[0]
                timestamp = f"{parts[1]}_{parts[2]}"
            else:
                acc_id = parts[0]
                timestamp = "unknown"

            backups.append({
                "account_id": acc_id,
                "timestamp": timestamp,
                "path": str(backup_file),
                "file_size": backup_file.stat().st_size
            })

        return backups

    def export_session(self, account_id: str, output_path: str) -> bool:
        """
        Export a session to a specified path.

        Args:
            account_id: The account identifier
            output_path: Where to export the session

        Returns:
            True if successful
        """
        try:
            session_path = Path(self.get_session_path(account_id))

            if not session_path.exists():
                logger.error(f"Session not found: {account_id}")
                return False

            shutil.copy2(session_path, output_path)
            logger.info(f"Session exported to: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error exporting session: {e}")
            return False

    def import_session(
        self,
        account_id: str,
        input_path: str,
        platform: str = "",
        overwrite: bool = False
    ) -> bool:
        """
        Import a session from a file.

        Args:
            account_id: The account identifier to save as
            input_path: Path to the session file to import
            platform: Platform name
            overwrite: Overwrite existing session

        Returns:
            True if successful
        """
        if self.session_exists(account_id) and not overwrite:
            logger.error(f"Session already exists: {account_id}. Use overwrite=True")
            return False

        return self.save_session_from_file(account_id, input_path, platform)

    def get_session_info(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed info about a session."""
        if not self.session_exists(account_id):
            return None

        session_path = Path(self.get_session_path(account_id))
        meta = self.metadata["sessions"].get(account_id, {})
        validation = self.validate_session(account_id)

        # Get cookie count from session
        cookie_count = 0
        try:
            with open(session_path, 'r') as f:
                data = json.load(f)
                cookie_count = len(data.get("cookies", []))
        except:
            pass

        return {
            "account_id": account_id,
            "path": str(session_path),
            "platform": meta.get("platform", "unknown"),
            "created_at": meta.get("created_at"),
            "updated_at": meta.get("updated_at"),
            "last_accessed": meta.get("last_accessed"),
            "notes": meta.get("notes", ""),
            "file_size": session_path.stat().st_size,
            "cookie_count": cookie_count,
            "validation": validation,
            "backups": len(list(self.backups_dir.glob(f"{account_id}_*.json")))
        }


# CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Session Manager")
    parser.add_argument("--list", "-l", action="store_true", help="List all sessions")
    parser.add_argument("--info", help="Get info for specific account")
    parser.add_argument("--validate", help="Validate a session")
    parser.add_argument("--delete", help="Delete a session")
    parser.add_argument("--no-backup", action="store_true", help="Don't backup when deleting")
    parser.add_argument("--restore", help="Restore a backup for account")
    parser.add_argument("--backup-index", type=int, default=0, help="Backup index to restore")
    parser.add_argument("--list-backups", action="store_true", help="List backups")
    parser.add_argument("--export", nargs=2, metavar=("ACCOUNT", "PATH"), help="Export session")
    parser.add_argument("--import", nargs=2, metavar=("PATH", "ACCOUNT"), dest="import_session",
                        help="Import session")
    parser.add_argument("--platform", help="Platform for imported session")
    parser.add_argument("--dir", help="Custom sessions directory")

    args = parser.parse_args()

    manager = SessionManager(sessions_dir=args.dir)

    if args.list:
        sessions = manager.list_sessions()
        print(f"\nSessions ({len(sessions)}):")
        print("-" * 70)
        for s in sessions:
            status = "OK" if s["valid"] else "EXPIRED" if s["expired"] else "INVALID"
            print(f"  [{status:7}] {s['account_id']:25} {s['platform']:12} "
                  f"({s['file_size']/1024:.1f}KB)")

    elif args.info:
        info = manager.get_session_info(args.info)
        if info:
            print(f"\nSession Info: {args.info}")
            print("-" * 50)
            for key, value in info.items():
                if key != "validation":
                    print(f"  {key}: {value}")
            print(f"\n  Validation:")
            for key, value in info["validation"].items():
                print(f"    {key}: {value}")
        else:
            print(f"Session not found: {args.info}")

    elif args.validate:
        result = manager.validate_session(args.validate)
        print(f"\nValidation for {args.validate}:")
        for key, value in result.items():
            print(f"  {key}: {value}")

    elif args.delete:
        success = manager.delete_session(args.delete, backup=not args.no_backup)
        print(f"Delete {'successful' if success else 'failed'}")

    elif args.restore:
        success = manager.restore_backup(args.restore, args.backup_index)
        print(f"Restore {'successful' if success else 'failed'}")

    elif args.list_backups:
        backups = manager.list_backups()
        print(f"\nBackups ({len(backups)}):")
        print("-" * 60)
        for b in backups:
            print(f"  {b['account_id']:25} {b['timestamp']} ({b['file_size']/1024:.1f}KB)")

    elif args.export:
        account, path = args.export
        success = manager.export_session(account, path)
        print(f"Export {'successful' if success else 'failed'}")

    elif args.import_session:
        path, account = args.import_session
        success = manager.import_session(account, path, platform=args.platform or "")
        print(f"Import {'successful' if success else 'failed'}")

    else:
        parser.print_help()
