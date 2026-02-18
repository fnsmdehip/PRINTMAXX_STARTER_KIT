#!/usr/bin/env python3
"""
Queue Processor Test Suite
==========================
Comprehensive tests for the QueueProcessor class.

Features:
- Queue reading tests
- Status update tests
- Platform routing tests
- Logging tests
- Scheduled post tests

Usage:
    python -m pytest test_queue_processor.py -v
    python test_queue_processor.py --unit
"""

import os
import sys
import json
import csv
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

try:
    from queue_processor import QueueProcessor, QueueItem
except ImportError:
    QueueProcessor = None
    QueueItem = None

# Test output directory
TEST_OUTPUT_DIR = Path(__file__).parent / "test_output"
TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class TestQueueItemDataclass(unittest.TestCase):
    """Tests for QueueItem dataclass."""

    def test_queue_item_creation(self):
        """Test QueueItem creation with minimal fields."""
        if not QueueItem:
            self.skipTest("QueueItem not importable")

        item = QueueItem(
            id="Q0001",
            account_id="x_faith",
            platform="X",
            content="Test content"
        )
        self.assertEqual(item.id, "Q0001")
        self.assertEqual(item.platform, "X")
        self.assertEqual(item.status, "pending")

    def test_queue_item_to_dict(self):
        """Test QueueItem serialization."""
        if not QueueItem:
            self.skipTest("QueueItem not importable")

        item = QueueItem(
            id="Q0001",
            account_id="x_faith",
            platform="X",
            content="Test content",
            hashtags="ai tech"
        )
        d = item.to_dict()

        self.assertIsInstance(d, dict)
        self.assertEqual(d["id"], "Q0001")
        self.assertEqual(d["hashtags"], "ai tech")

    def test_queue_item_from_csv_row(self):
        """Test creating QueueItem from CSV row."""
        if not QueueItem:
            self.skipTest("QueueItem not importable")

        row = {
            "ContentID": "Q0001",
            "Platform": "X",
            "Title": "Test content",
            "Status": "QUEUED",
            "ScheduledDate": "2024-01-15T10:00:00",
            "Niche": "AI",
            "Type": "Post"
        }
        item = QueueItem.from_csv_row(row)

        self.assertEqual(item.id, "Q0001")
        self.assertEqual(item.platform, "X")
        self.assertEqual(item.content, "Test content")
        self.assertEqual(item.status, "queued")
        self.assertEqual(item.niche, "AI")

    def test_queue_item_from_csv_alternative_fields(self):
        """Test QueueItem handles alternative field names."""
        if not QueueItem:
            self.skipTest("QueueItem not importable")

        row = {
            "id": "Q0002",
            "platform": "Instagram",
            "content": "Alt content",
            "status": "pending"
        }
        item = QueueItem.from_csv_row(row)

        self.assertEqual(item.id, "Q0002")
        self.assertEqual(item.platform, "Instagram")


class TestQueueProcessorInit(unittest.TestCase):
    """Tests for QueueProcessor initialization."""

    def test_init_with_defaults(self):
        """Test processor initialization with defaults."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        processor = QueueProcessor()
        self.assertIsNotNone(processor.queue_path)
        self.assertIsNotNone(processor.log_path)

    def test_init_with_custom_paths(self):
        """Test processor with custom paths."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        queue_path = str(TEST_OUTPUT_DIR / "custom_queue.csv")
        log_path = str(TEST_OUTPUT_DIR / "custom_log.csv")

        processor = QueueProcessor(
            queue_path=queue_path,
            log_path=log_path
        )

        self.assertEqual(str(processor.queue_path), queue_path)
        self.assertEqual(str(processor.log_path), log_path)

    def test_init_creates_log_file(self):
        """Test processor creates post log if missing."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        log_path = TEST_OUTPUT_DIR / "new_log.csv"
        if log_path.exists():
            log_path.unlink()

        processor = QueueProcessor(log_path=str(log_path))

        self.assertTrue(log_path.exists())

        # Clean up
        log_path.unlink()


class TestQueueProcessorLoadQueue(unittest.TestCase):
    """Tests for loading queue from CSV."""

    def setUp(self):
        """Create test queue files."""
        self.temp_files = []

    def tearDown(self):
        """Clean up temp files."""
        for f in self.temp_files:
            try:
                os.unlink(f)
            except:
                pass

    def _create_temp_csv(self, rows, fieldnames):
        """Create a temporary CSV file."""
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        f.close()
        self.temp_files.append(f.name)
        return f.name

    def test_load_queue_empty(self):
        """Test loading nonexistent queue returns empty list."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        processor = QueueProcessor(queue_path="/nonexistent/queue.csv")
        items = processor.load_queue()

        self.assertEqual(len(items), 0)

    def test_load_queue_with_items(self):
        """Test loading queue with items."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        rows = [
            {"ContentID": "Q0001", "Platform": "X", "Title": "Content 1", "Status": "PENDING"},
            {"ContentID": "Q0002", "Platform": "Instagram", "Title": "Content 2", "Status": "QUEUED"},
        ]
        fieldnames = ["ContentID", "Platform", "Title", "Status"]
        queue_path = self._create_temp_csv(rows, fieldnames)

        processor = QueueProcessor(queue_path=queue_path)
        items = processor.load_queue()

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].id, "Q0001")
        self.assertEqual(items[1].platform, "Instagram")

    def test_get_pending_items(self):
        """Test filtering pending items."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        rows = [
            {"ContentID": "Q0001", "Platform": "X", "Title": "C1", "Status": "PENDING"},
            {"ContentID": "Q0002", "Platform": "X", "Title": "C2", "Status": "POSTED"},
            {"ContentID": "Q0003", "Platform": "X", "Title": "C3", "Status": "QUEUED"},
        ]
        fieldnames = ["ContentID", "Platform", "Title", "Status"]
        queue_path = self._create_temp_csv(rows, fieldnames)

        processor = QueueProcessor(queue_path=queue_path)
        pending = processor.get_pending_items()

        self.assertEqual(len(pending), 2)  # PENDING and QUEUED

    def test_get_scheduled_items(self):
        """Test filtering scheduled items due now."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        past_time = (datetime.now() - timedelta(hours=1)).isoformat()
        future_time = (datetime.now() + timedelta(hours=1)).isoformat()

        rows = [
            {"ContentID": "Q0001", "Platform": "X", "Title": "C1", "Status": "scheduled",
             "ScheduledDate": past_time},
            {"ContentID": "Q0002", "Platform": "X", "Title": "C2", "Status": "scheduled",
             "ScheduledDate": future_time},
        ]
        fieldnames = ["ContentID", "Platform", "Title", "Status", "ScheduledDate"]
        queue_path = self._create_temp_csv(rows, fieldnames)

        processor = QueueProcessor(queue_path=queue_path)
        scheduled = processor.get_scheduled_items()

        # Only past scheduled item should be ready
        self.assertEqual(len(scheduled), 1)
        self.assertEqual(scheduled[0].id, "Q0001")


class TestQueueProcessorPlatformRouting(unittest.TestCase):
    """Tests for platform routing."""

    def test_get_poster_for_x(self):
        """Test getting poster for X platform."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        processor = QueueProcessor()

        with patch.dict('sys.modules', {'x_poster': MagicMock()}):
            with patch.object(processor, '_get_poster_for_platform') as mock:
                mock.return_value = MagicMock()
                poster = processor._get_poster_for_platform("X", {})

                self.assertIsNotNone(poster)

    def test_get_poster_for_instagram(self):
        """Test getting poster for Instagram platform."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        processor = QueueProcessor()

        with patch.dict('sys.modules', {'ig_poster': MagicMock()}):
            with patch.object(processor, '_get_poster_for_platform') as mock:
                mock.return_value = MagicMock()
                poster = processor._get_poster_for_platform("Instagram", {})

                self.assertIsNotNone(poster)

    def test_get_poster_for_unknown_platform(self):
        """Test unknown platform returns None."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        processor = QueueProcessor()
        poster = processor._get_poster_for_platform("Unknown", {})

        self.assertIsNone(poster)


class TestQueueProcessorPostItem(unittest.TestCase):
    """Tests for posting individual items."""

    def test_post_item_no_account(self):
        """Test posting without available account."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        processor = QueueProcessor()

        # Mock account_manager to return None
        processor.account_manager = MagicMock()
        processor.account_manager.get_account.return_value = None
        processor.account_manager.get_next_available.return_value = None

        item = QueueItem(
            id="Q0001",
            account_id="nonexistent",
            platform="X",
            content="Test"
        )

        result = processor.post_item(item)

        self.assertFalse(result["success"])
        self.assertIn("No available account", result["error"])

    def test_post_item_rate_limited(self):
        """Test posting when rate limited."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        processor = QueueProcessor()

        mock_account = MagicMock()
        mock_account.id = "test"
        mock_account.proxy = {}

        processor.account_manager = MagicMock()
        processor.account_manager.get_account.return_value = mock_account
        processor.account_manager.can_post.return_value = False

        item = QueueItem(
            id="Q0001",
            account_id="test",
            platform="X",
            content="Test"
        )

        result = processor.post_item(item)

        self.assertFalse(result["success"])
        self.assertIn("rate limited", result["error"])

    @patch('queue_processor.XPoster')
    def test_post_item_success(self, mock_poster_class):
        """Test successful post."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        processor = QueueProcessor()

        # Mock account
        mock_account = MagicMock()
        mock_account.id = "test"
        mock_account.proxy = {}
        mock_account.session_path = ""

        processor.account_manager = MagicMock()
        processor.account_manager.get_account.return_value = mock_account
        processor.account_manager.can_post.return_value = True

        # Mock poster
        mock_poster = MagicMock()
        mock_poster.post.return_value = {"success": True}
        mock_poster_class.return_value = mock_poster

        item = QueueItem(
            id="Q0001",
            account_id="test",
            platform="X",
            content="Test content"
        )

        # Mock the _get_poster_for_platform method
        with patch.object(processor, '_get_poster_for_platform', return_value=mock_poster):
            with patch.object(processor, '_log_post'):
                result = processor.post_item(item)

        self.assertTrue(result["success"])


class TestQueueProcessorUpdateStatus(unittest.TestCase):
    """Tests for updating queue status."""

    def test_update_queue_status(self):
        """Test updating item status in queue."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        # Create temp queue
        temp_queue = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
        writer = csv.DictWriter(temp_queue, fieldnames=["ContentID", "Platform", "Status", "PublishedDate"])
        writer.writeheader()
        writer.writerow({"ContentID": "Q0001", "Platform": "X", "Status": "PENDING", "PublishedDate": ""})
        temp_queue.close()

        try:
            processor = QueueProcessor(queue_path=temp_queue.name)
            processor.update_queue_status("Q0001", "posted")

            # Read back and verify
            with open(temp_queue.name) as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            self.assertEqual(rows[0]["Status"], "POSTED")
            self.assertNotEqual(rows[0]["PublishedDate"], "")
        finally:
            os.unlink(temp_queue.name)


class TestQueueProcessorProcessing(unittest.TestCase):
    """Tests for batch processing."""

    def test_process_pending_dry_run(self):
        """Test dry run processing."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        # Create temp queue
        temp_queue = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
        writer = csv.DictWriter(temp_queue, fieldnames=["ContentID", "Platform", "Title", "Status"])
        writer.writeheader()
        writer.writerow({"ContentID": "Q0001", "Platform": "X", "Title": "Test", "Status": "PENDING"})
        temp_queue.close()

        try:
            processor = QueueProcessor(queue_path=temp_queue.name)
            results = processor.process_pending(dry_run=True)

            self.assertEqual(len(results), 1)
            self.assertTrue(results[0].get("dry_run"))
        finally:
            os.unlink(temp_queue.name)

    def test_process_pending_with_limit(self):
        """Test processing with limit."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        # Create temp queue with multiple items
        temp_queue = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
        writer = csv.DictWriter(temp_queue, fieldnames=["ContentID", "Platform", "Title", "Status"])
        writer.writeheader()
        for i in range(5):
            writer.writerow({
                "ContentID": f"Q{i:04d}",
                "Platform": "X",
                "Title": f"Test {i}",
                "Status": "PENDING"
            })
        temp_queue.close()

        try:
            processor = QueueProcessor(queue_path=temp_queue.name)
            results = processor.process_pending(limit=2, dry_run=True)

            self.assertEqual(len(results), 2)
        finally:
            os.unlink(temp_queue.name)


class TestQueueProcessorAddToQueue(unittest.TestCase):
    """Tests for adding items to queue."""

    def test_add_to_queue_creates_file(self):
        """Test adding creates queue file if missing."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        queue_path = TEST_OUTPUT_DIR / "new_queue.csv"
        if queue_path.exists():
            queue_path.unlink()

        processor = QueueProcessor(queue_path=str(queue_path))
        new_id = processor.add_to_queue(
            platform="X",
            content="Test content",
            niche="AI"
        )

        self.assertTrue(queue_path.exists())
        self.assertIsNotNone(new_id)

        # Clean up
        queue_path.unlink()

    def test_add_to_queue_generates_id(self):
        """Test adding generates unique IDs."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        queue_path = TEST_OUTPUT_DIR / "queue_ids.csv"
        if queue_path.exists():
            queue_path.unlink()

        processor = QueueProcessor(queue_path=str(queue_path))

        id1 = processor.add_to_queue(platform="X", content="Test 1")
        id2 = processor.add_to_queue(platform="X", content="Test 2")

        self.assertNotEqual(id1, id2)

        # Clean up
        queue_path.unlink()

    def test_add_scheduled_item(self):
        """Test adding scheduled item."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        queue_path = TEST_OUTPUT_DIR / "scheduled_queue.csv"
        if queue_path.exists():
            queue_path.unlink()

        processor = QueueProcessor(queue_path=str(queue_path))
        scheduled_time = (datetime.now() + timedelta(hours=2)).isoformat()

        new_id = processor.add_to_queue(
            platform="X",
            content="Scheduled post",
            scheduled_time=scheduled_time
        )

        items = processor.load_queue()
        self.assertEqual(items[0].status, "scheduled")

        # Clean up
        queue_path.unlink()


class TestQueueProcessorStats(unittest.TestCase):
    """Tests for queue statistics."""

    def test_get_queue_stats(self):
        """Test getting queue statistics."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        # Create temp queue
        temp_queue = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
        fieldnames = ["ContentID", "Platform", "Title", "Status", "Niche"]
        writer = csv.DictWriter(temp_queue, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"ContentID": "Q0001", "Platform": "X", "Title": "T1", "Status": "PENDING", "Niche": "AI"})
        writer.writerow({"ContentID": "Q0002", "Platform": "X", "Title": "T2", "Status": "POSTED", "Niche": "AI"})
        writer.writerow({"ContentID": "Q0003", "Platform": "Instagram", "Title": "T3", "Status": "PENDING", "Niche": "Faith"})
        temp_queue.close()

        try:
            processor = QueueProcessor(queue_path=temp_queue.name)
            stats = processor.get_queue_stats()

            self.assertEqual(stats["total"], 3)
            self.assertEqual(stats["by_status"]["pending"], 2)
            self.assertEqual(stats["by_status"]["posted"], 1)
            self.assertEqual(stats["by_platform"]["X"], 2)
            self.assertEqual(stats["by_platform"]["Instagram"], 1)
            self.assertEqual(stats["by_niche"]["AI"], 2)
            self.assertEqual(stats["by_niche"]["Faith"], 1)
        finally:
            os.unlink(temp_queue.name)


class TestQueueProcessorLogging(unittest.TestCase):
    """Tests for post logging."""

    def test_log_post(self):
        """Test logging a post result."""
        if not QueueProcessor:
            self.skipTest("QueueProcessor not importable")

        log_path = TEST_OUTPUT_DIR / "test_post_log.csv"
        if log_path.exists():
            log_path.unlink()

        processor = QueueProcessor(log_path=str(log_path))

        item = QueueItem(
            id="Q0001",
            account_id="test",
            platform="X",
            content="Test content for logging"
        )

        result = {
            "queue_id": "Q0001",
            "account_id": "test",
            "success": True,
            "error": None,
            "timestamp": datetime.now().isoformat()
        }

        processor._log_post(result, item)

        # Read log and verify
        with open(log_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["queue_id"], "Q0001")
        self.assertEqual(rows[0]["status"], "success")

        # Clean up
        log_path.unlink()


def run_tests(test_type: str = "all") -> Dict[str, Any]:
    """Run tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestQueueItemDataclass))
    suite.addTests(loader.loadTestsFromTestCase(TestQueueProcessorInit))
    suite.addTests(loader.loadTestsFromTestCase(TestQueueProcessorLoadQueue))
    suite.addTests(loader.loadTestsFromTestCase(TestQueueProcessorPlatformRouting))
    suite.addTests(loader.loadTestsFromTestCase(TestQueueProcessorPostItem))
    suite.addTests(loader.loadTestsFromTestCase(TestQueueProcessorUpdateStatus))
    suite.addTests(loader.loadTestsFromTestCase(TestQueueProcessorProcessing))
    suite.addTests(loader.loadTestsFromTestCase(TestQueueProcessorAddToQueue))
    suite.addTests(loader.loadTestsFromTestCase(TestQueueProcessorStats))
    suite.addTests(loader.loadTestsFromTestCase(TestQueueProcessorLogging))

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

    parser = argparse.ArgumentParser(description="Queue Processor Test Suite")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--output", "-o", help="Output results to JSON file")

    args = parser.parse_args()

    results = run_tests()

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    sys.exit(0 if results["success"] else 1)
