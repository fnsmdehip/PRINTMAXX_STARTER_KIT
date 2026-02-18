#!/usr/bin/env python3
"""
Session Manager Test Suite
==========================
Comprehensive tests for the SessionManager class.

Features:
- Session save/load tests
- Expiry checking tests
- Backup/restore tests
- Validation tests
- Export/import tests

Usage:
    python -m pytest test_session_manager.py -v
    python test_session_manager.py --unit
"""

import os
import sys
import json
import tempfile
import shutil
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

try:
    from session_manager import SessionManager
except ImportError:
    SessionManager = None

# Test output directory
TEST_OUTPUT_DIR = Path(__file__).parent / "test_output" / "sessions"
TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class TestSessionManagerInit(unittest.TestCase):
    """Tests for SessionManager initialization."""

    def test_init_with_defaults(self):
        """Test manager initialization with defaults."""
        if not SessionManager:
            self.skipTest("SessionManager not importable")

        manager = SessionManager()
        self.assertIsNotNone(manager.sessions_dir)
        self.assertIsNotNone(manager.backups_dir)

    def test_init_with_custom_dir(self):
        """Test manager with custom sessions directory."""
        if not SessionManager:
            self.skipTest("SessionManager not importable")

        custom_dir = str(TEST_OUTPUT_DIR / "custom_sessions")
        manager = SessionManager(sessions_dir=custom_dir)

        self.assertEqual(str(manager.sessions_dir), custom_dir)
        self.assertTrue(manager.sessions_dir.exists())

        # Clean up
        shutil.rmtree(custom_dir, ignore_errors=True)

    def test_init_creates_directories(self):
        """Test manager creates required directories."""
        if not SessionManager:
            self.skipTest("SessionManager not importable")

        custom_dir = str(TEST_OUTPUT_DIR / "new_sessions")
        if Path(custom_dir).exists():
            shutil.rmtree(custom_dir)

        manager = SessionManager(sessions_dir=custom_dir)

        self.assertTrue(manager.sessions_dir.exists())
        self.assertTrue(manager.backups_dir.exists())

        # Clean up
        shutil.rmtree(custom_dir, ignore_errors=True)

    def test_init_loads_metadata(self):
        """Test manager loads existing metadata."""
        if not SessionManager:
            self.skipTest("SessionManager not importable")

        # Create metadata file first
        custom_dir = TEST_OUTPUT_DIR / "meta_sessions"
        custom_dir.mkdir(parents=True, exist_ok=True)
        metadata_file = custom_dir / "session_metadata.json"

        metadata = {
            "sessions": {
                "test_account": {
                    "path": "/path/to/session.json",
                    "platform": "X",
                    "created_at": "2024-01-01T00:00:00"
                }
            }
        }
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f)

        manager = SessionManager(sessions_dir=str(custom_dir))

        self.assertIn("test_account", manager.metadata["sessions"])

        # Clean up
        shutil.rmtree(custom_dir, ignore_errors=True)


class TestSessionManagerPaths(unittest.TestCase):
    """Tests for session path methods."""

    def setUp(self):
        """Set up test manager."""
        if not SessionManager:
            self.skipTest("SessionManager not importable")

        self.test_dir = TEST_OUTPUT_DIR / "path_tests"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.manager = SessionManager(sessions_dir=str(self.test_dir))

    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_get_session_path(self):
        """Test getting session path."""
        path = self.manager.get_session_path("x_faith_main")

        self.assertTrue(path.endswith(".json"))
        self.assertIn("x_faith_main", path)

    def test_session_exists_false(self):
        """Test session_exists returns False for nonexistent."""
        self.assertFalse(self.manager.session_exists("nonexistent"))

    def test_session_exists_true(self):
        """Test session_exists returns True for existing."""
        # Create a session file
        session_path = self.manager.get_session_path("test_account")
        with open(session_path, 'w') as f:
            json.dump({"cookies": []}, f)

        self.assertTrue(self.manager.session_exists("test_account"))


class TestSessionManagerSave(unittest.TestCase):
    """Tests for saving sessions."""

    def setUp(self):
        """Set up test manager."""
        if not SessionManager:
            self.skipTest("SessionManager not importable")

        self.test_dir = TEST_OUTPUT_DIR / "save_tests"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.manager = SessionManager(sessions_dir=str(self.test_dir))

    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_save_session_from_context(self):
        """Test saving session from browser context."""
        mock_context = MagicMock()
        mock_context.storage_state.return_value = None

        result = self.manager.save_session(
            "test_account",
            mock_context,
            platform="X",
            notes="Test session"
        )

        self.assertTrue(result)
        mock_context.storage_state.assert_called_once()

        # Check metadata updated
        self.assertIn("test_account", self.manager.metadata["sessions"])
        self.assertEqual(self.manager.metadata["sessions"]["test_account"]["platform"], "X")

    def test_save_session_from_file(self):
        """Test saving session from existing file."""
        # Create source file
        source_path = self.test_dir / "source_session.json"
        with open(source_path, 'w') as f:
            json.dump({"cookies": [{"name": "test"}]}, f)

        result = self.manager.save_session_from_file(
            "imported_account",
            str(source_path),
            platform="Instagram"
        )

        self.assertTrue(result)
        self.assertTrue(self.manager.session_exists("imported_account"))

    def test_save_session_creates_backup(self):
        """Test saving existing session creates backup."""
        # Create initial session
        session_path = self.manager.get_session_path("backup_test")
        with open(session_path, 'w') as f:
            json.dump({"cookies": [{"name": "original"}]}, f)

        # Update metadata
        self.manager.metadata["sessions"]["backup_test"] = {
            "path": session_path,
            "platform": "X",
            "created_at": datetime.now().isoformat()
        }

        # Save new session (should backup old one)
        mock_context = MagicMock()
        self.manager.save_session("backup_test", mock_context)

        # Check backup was created
        backups = list(self.manager.backups_dir.glob("backup_test_*.json"))
        self.assertGreaterEqual(len(backups), 1)


class TestSessionManagerLoad(unittest.TestCase):
    """Tests for loading sessions."""

    def setUp(self):
        """Set up test manager."""
        if not SessionManager:
            self.skipTest("SessionManager not importable")

        self.test_dir = TEST_OUTPUT_DIR / "load_tests"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.manager = SessionManager(sessions_dir=str(self.test_dir))

    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_load_session_nonexistent(self):
        """Test loading nonexistent session returns None."""
        result = self.manager.load_session("nonexistent")
        self.assertIsNone(result)

    def test_load_session_existing(self):
        """Test loading existing session."""
        # Create session file
        session_path = self.manager.get_session_path("test_account")
        session_data = {
            "cookies": [{"name": "auth", "value": "token123"}],
            "origins": []
        }
        with open(session_path, 'w') as f:
            json.dump(session_data, f)

        # Update metadata
        self.manager.metadata["sessions"]["test_account"] = {
            "path": session_path,
            "created_at": datetime.now().isoformat()
        }

        result = self.manager.load_session("test_account")

        self.assertIsNotNone(result)
        self.assertEqual(result["cookies"][0]["name"], "auth")

    def test_load_session_updates_last_accessed(self):
        """Test loading updates last_accessed in metadata."""
        # Create session
        session_path = self.manager.get_session_path("access_test")
        with open(session_path, 'w') as f:
            json.dump({"cookies": []}, f)

        self.manager.metadata["sessions"]["access_test"] = {
            "path": session_path,
            "created_at": datetime.now().isoformat()
        }

        self.manager.load_session("access_test")

        self.assertIn("last_accessed", self.manager.metadata["sessions"]["access_test"])


class TestSessionManagerBackup(unittest.TestCase):
    """Tests for backup functionality."""

    def setUp(self):
        """Set up test manager."""
        if not SessionManager:
            self.skipTest("SessionManager not importable")

        self.test_dir = TEST_OUTPUT_DIR / "backup_tests"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.manager = SessionManager(sessions_dir=str(self.test_dir))

    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_backup_session(self):
        """Test creating a backup."""
        # Create session
        session_path = self.manager.get_session_path("backup_me")
        with open(session_path, 'w') as f:
            json.dump({"cookies": [{"name": "original"}]}, f)

        result = self.manager._backup_session("backup_me")

        self.assertTrue(result)
        backups = list(self.manager.backups_dir.glob("backup_me_*.json"))
        self.assertEqual(len(backups), 1)

    def test_backup_nonexistent_returns_false(self):
        """Test backup of nonexistent session returns False."""
        result = self.manager._backup_session("nonexistent")
        self.assertFalse(result)

    def test_cleanup_old_backups(self):
        """Test cleanup keeps only recent backups."""
        # Create multiple backups
        for i in range(10):
            backup_path = self.manager.backups_dir / f"cleanup_test_2024010{i}_120000.json"
            with open(backup_path, 'w') as f:
                json.dump({}, f)

        self.manager._cleanup_backups("cleanup_test", keep=3)

        backups = list(self.manager.backups_dir.glob("cleanup_test_*.json"))
        self.assertEqual(len(backups), 3)

    def test_restore_backup(self):
        """Test restoring from backup."""
        # Create session
        session_path = self.manager.get_session_path("restore_test")
        with open(session_path, 'w') as f:
            json.dump({"cookies": [{"name": "current"}]}, f)

        # Create backup with different content
        backup_path = self.manager.backups_dir / "restore_test_20240115_120000.json"
        with open(backup_path, 'w') as f:
            json.dump({"cookies": [{"name": "backup"}]}, f)

        # Update metadata
        self.manager.metadata["sessions"]["restore_test"] = {"path": session_path}

        result = self.manager.restore_backup("restore_test", backup_index=0)

        self.assertTrue(result)

        # Verify restored content
        with open(session_path) as f:
            restored = json.load(f)
        self.assertEqual(restored["cookies"][0]["name"], "backup")

    def test_list_backups(self):
        """Test listing backups."""
        # Create backups
        for acc in ["acc1", "acc2"]:
            for i in range(2):
                backup_path = self.manager.backups_dir / f"{acc}_2024010{i}_120000.json"
                with open(backup_path, 'w') as f:
                    json.dump({}, f)

        all_backups = self.manager.list_backups()
        self.assertEqual(len(all_backups), 4)

        acc1_backups = self.manager.list_backups("acc1")
        self.assertEqual(len(acc1_backups), 2)


class TestSessionManagerValidation(unittest.TestCase):
    """Tests for session validation."""

    def setUp(self):
        """Set up test manager."""
        if not SessionManager:
            self.skipTest("SessionManager not importable")

        self.test_dir = TEST_OUTPUT_DIR / "validate_tests"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.manager = SessionManager(sessions_dir=str(self.test_dir))

    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_validate_nonexistent_session(self):
        """Test validating nonexistent session."""
        result = self.manager.validate_session("nonexistent")

        self.assertFalse(result["valid"])
        self.assertFalse(result["exists"])

    def test_validate_fresh_session(self):
        """Test validating fresh session."""
        # Create session
        session_path = self.manager.get_session_path("fresh_session")
        with open(session_path, 'w') as f:
            json.dump({"cookies": []}, f)

        # Update metadata with recent date
        self.manager.metadata["sessions"]["fresh_session"] = {
            "path": session_path,
            "updated_at": datetime.now().isoformat(),
            "checksum": self.manager._calculate_checksum(session_path)
        }

        result = self.manager.validate_session("fresh_session")

        self.assertTrue(result["valid"])
        self.assertTrue(result["exists"])
        self.assertFalse(result["expired"])

    def test_validate_expired_session(self):
        """Test validating expired session."""
        # Create session
        session_path = self.manager.get_session_path("old_session")
        with open(session_path, 'w') as f:
            json.dump({"cookies": []}, f)

        # Update metadata with old date
        old_date = (datetime.now() - timedelta(days=10)).isoformat()
        self.manager.metadata["sessions"]["old_session"] = {
            "path": session_path,
            "updated_at": old_date,
            "checksum": self.manager._calculate_checksum(session_path)
        }

        result = self.manager.validate_session("old_session")

        self.assertTrue(result["expired"])
        self.assertFalse(result["valid"])

    def test_validate_checksum_mismatch(self):
        """Test validating session with checksum mismatch."""
        # Create session
        session_path = self.manager.get_session_path("modified_session")
        with open(session_path, 'w') as f:
            json.dump({"cookies": []}, f)

        # Store wrong checksum
        self.manager.metadata["sessions"]["modified_session"] = {
            "path": session_path,
            "updated_at": datetime.now().isoformat(),
            "checksum": "wrong_checksum_value"
        }

        result = self.manager.validate_session("modified_session")

        self.assertFalse(result["checksum_ok"])


class TestSessionManagerDelete(unittest.TestCase):
    """Tests for deleting sessions."""

    def setUp(self):
        """Set up test manager."""
        if not SessionManager:
            self.skipTest("SessionManager not importable")

        self.test_dir = TEST_OUTPUT_DIR / "delete_tests"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.manager = SessionManager(sessions_dir=str(self.test_dir))

    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_delete_session(self):
        """Test deleting a session."""
        # Create session
        session_path = self.manager.get_session_path("delete_me")
        with open(session_path, 'w') as f:
            json.dump({"cookies": []}, f)

        self.manager.metadata["sessions"]["delete_me"] = {"path": session_path}

        result = self.manager.delete_session("delete_me", backup=False)

        self.assertTrue(result)
        self.assertFalse(Path(session_path).exists())
        self.assertNotIn("delete_me", self.manager.metadata["sessions"])

    def test_delete_session_with_backup(self):
        """Test deleting session creates backup."""
        # Create session
        session_path = self.manager.get_session_path("delete_backup")
        with open(session_path, 'w') as f:
            json.dump({"cookies": []}, f)

        self.manager.metadata["sessions"]["delete_backup"] = {"path": session_path}

        result = self.manager.delete_session("delete_backup", backup=True)

        self.assertTrue(result)
        # Check backup was created
        backups = list(self.manager.backups_dir.glob("delete_backup_*.json"))
        self.assertGreaterEqual(len(backups), 1)

    def test_delete_nonexistent_session(self):
        """Test deleting nonexistent session returns False."""
        result = self.manager.delete_session("nonexistent")
        self.assertFalse(result)


class TestSessionManagerExportImport(unittest.TestCase):
    """Tests for export/import functionality."""

    def setUp(self):
        """Set up test manager."""
        if not SessionManager:
            self.skipTest("SessionManager not importable")

        self.test_dir = TEST_OUTPUT_DIR / "export_tests"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.manager = SessionManager(sessions_dir=str(self.test_dir))

    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_export_session(self):
        """Test exporting a session."""
        # Create session
        session_path = self.manager.get_session_path("export_me")
        with open(session_path, 'w') as f:
            json.dump({"cookies": [{"name": "export"}]}, f)

        export_path = self.test_dir / "exported.json"
        result = self.manager.export_session("export_me", str(export_path))

        self.assertTrue(result)
        self.assertTrue(export_path.exists())

        with open(export_path) as f:
            exported = json.load(f)
        self.assertEqual(exported["cookies"][0]["name"], "export")

    def test_export_nonexistent_returns_false(self):
        """Test exporting nonexistent session returns False."""
        result = self.manager.export_session("nonexistent", "/tmp/out.json")
        self.assertFalse(result)

    def test_import_session(self):
        """Test importing a session."""
        # Create source file
        source_path = self.test_dir / "source.json"
        with open(source_path, 'w') as f:
            json.dump({"cookies": [{"name": "imported"}]}, f)

        result = self.manager.import_session(
            "new_account",
            str(source_path),
            platform="X"
        )

        self.assertTrue(result)
        self.assertTrue(self.manager.session_exists("new_account"))

    def test_import_session_no_overwrite(self):
        """Test import doesn't overwrite existing by default."""
        # Create existing session
        session_path = self.manager.get_session_path("existing")
        with open(session_path, 'w') as f:
            json.dump({"cookies": []}, f)

        source_path = self.test_dir / "source.json"
        with open(source_path, 'w') as f:
            json.dump({"cookies": [{"name": "new"}]}, f)

        result = self.manager.import_session(
            "existing",
            str(source_path),
            overwrite=False
        )

        self.assertFalse(result)

    def test_import_session_overwrite(self):
        """Test import with overwrite flag."""
        # Create existing session
        session_path = self.manager.get_session_path("overwrite_me")
        with open(session_path, 'w') as f:
            json.dump({"cookies": [{"name": "old"}]}, f)

        source_path = self.test_dir / "source.json"
        with open(source_path, 'w') as f:
            json.dump({"cookies": [{"name": "new"}]}, f)

        result = self.manager.import_session(
            "overwrite_me",
            str(source_path),
            overwrite=True
        )

        self.assertTrue(result)

        # Verify content was overwritten
        with open(session_path) as f:
            content = json.load(f)
        self.assertEqual(content["cookies"][0]["name"], "new")


class TestSessionManagerList(unittest.TestCase):
    """Tests for listing sessions."""

    def setUp(self):
        """Set up test manager."""
        if not SessionManager:
            self.skipTest("SessionManager not importable")

        self.test_dir = TEST_OUTPUT_DIR / "list_tests"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.manager = SessionManager(sessions_dir=str(self.test_dir))

    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_list_sessions_empty(self):
        """Test listing empty sessions directory."""
        sessions = self.manager.list_sessions()
        self.assertEqual(len(sessions), 0)

    def test_list_sessions(self):
        """Test listing sessions."""
        # Create sessions
        for acc in ["x_faith", "ig_ai"]:
            session_path = self.manager.get_session_path(acc)
            with open(session_path, 'w') as f:
                json.dump({"cookies": []}, f)

            self.manager.metadata["sessions"][acc] = {
                "path": session_path,
                "platform": "X" if "x_" in acc else "Instagram",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }

        sessions = self.manager.list_sessions()

        self.assertEqual(len(sessions), 2)
        self.assertIn("account_id", sessions[0])
        self.assertIn("platform", sessions[0])
        self.assertIn("valid", sessions[0])

    def test_get_session_info(self):
        """Test getting detailed session info."""
        # Create session
        session_path = self.manager.get_session_path("info_test")
        with open(session_path, 'w') as f:
            json.dump({"cookies": [{"name": "a"}, {"name": "b"}]}, f)

        self.manager.metadata["sessions"]["info_test"] = {
            "path": session_path,
            "platform": "X",
            "created_at": datetime.now().isoformat(),
            "notes": "Test notes"
        }

        info = self.manager.get_session_info("info_test")

        self.assertIsNotNone(info)
        self.assertEqual(info["account_id"], "info_test")
        self.assertEqual(info["platform"], "X")
        self.assertEqual(info["cookie_count"], 2)
        self.assertEqual(info["notes"], "Test notes")

    def test_get_session_info_nonexistent(self):
        """Test getting info for nonexistent session."""
        info = self.manager.get_session_info("nonexistent")
        self.assertIsNone(info)


def run_tests(test_type: str = "all") -> Dict[str, Any]:
    """Run tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestSessionManagerInit))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionManagerPaths))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionManagerSave))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionManagerLoad))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionManagerBackup))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionManagerValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionManagerDelete))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionManagerExportImport))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionManagerList))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return {
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "success": result.wasSuccessful(),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Session Manager Test Suite")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--output", "-o", help="Output results to JSON file")

    args = parser.parse_args()

    results = run_tests()

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    sys.exit(0 if results["success"] else 1)
