"""
PRINTMAXX Test Suite
====================
Comprehensive testing framework for automation scripts.

Modules:
- app_test_runner: Test React Native apps in simulator/emulator
- screenshot_generator: Generate App Store screenshots
- crash_detector: Monitor apps for crashes
- test_x_poster: X/Twitter posting tests
- test_ig_poster: Instagram posting tests
- test_proxy_rotation: Proxy rotation tests
"""

from pathlib import Path

# Test suite version
__version__ = "1.0.0"

# Test directories
TEST_DIR = Path(__file__).parent
OUTPUT_DIR = TEST_DIR / "test_output"
OUTPUT_DIR.mkdir(exist_ok=True)
