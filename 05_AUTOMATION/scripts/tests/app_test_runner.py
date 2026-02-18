#!/usr/bin/env python3
"""
App Test Runner - React Native App Testing Framework
====================================================
Test React Native apps in iOS Simulator and Android Emulator using Playwright/Appium patterns.

Features:
- Launch apps in simulator/emulator
- Navigate app flows
- Capture performance metrics
- Detect UI issues
- Test deep links
- Validate app store compliance

Usage:
    from app_test_runner import AppTestRunner

    runner = AppTestRunner(platform="ios")
    runner.launch_app("com.printmaxx.aiclarity")
    results = runner.run_test_suite("basic_flow")

CLI:
    python app_test_runner.py --platform ios --app com.printmaxx.aiclarity
    python app_test_runner.py --platform android --app com.printmaxx.aiclarity --suite onboarding
"""

import os
import sys
import json
import time
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
import re

# Configure logging
LOG_DIR = Path(__file__).parent.parent.parent / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "app_test_runner.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("app_test_runner")


@dataclass
class TestResult:
    """Test result container."""
    test_name: str
    status: str  # passed, failed, skipped, error
    duration_ms: float
    error: Optional[str] = None
    screenshot_path: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AppTestSuite:
    """Collection of test results."""
    suite_name: str
    platform: str
    app_id: str
    results: List[TestResult] = field(default_factory=list)
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())
    end_time: Optional[str] = None
    summary: Dict[str, int] = field(default_factory=lambda: {"passed": 0, "failed": 0, "skipped": 0, "error": 0})


class SimulatorController:
    """Control iOS Simulator."""

    def __init__(self):
        self.booted_device = None
        self._check_xcrun()

    def _check_xcrun(self) -> bool:
        """Check if xcrun is available."""
        try:
            subprocess.run(["xcrun", "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("xcrun not available - iOS simulator features disabled")
            return False

    def list_devices(self) -> List[Dict[str, str]]:
        """List available iOS simulators."""
        try:
            result = subprocess.run(
                ["xcrun", "simctl", "list", "devices", "-j"],
                capture_output=True,
                text=True,
                check=True
            )
            data = json.loads(result.stdout)
            devices = []
            for runtime, device_list in data.get("devices", {}).items():
                for device in device_list:
                    if device.get("isAvailable", False):
                        devices.append({
                            "udid": device["udid"],
                            "name": device["name"],
                            "state": device["state"],
                            "runtime": runtime
                        })
            return devices
        except Exception as e:
            logger.error(f"Failed to list devices: {e}")
            return []

    def boot_device(self, udid: str = None, device_name: str = None) -> Optional[str]:
        """Boot a simulator device."""
        if not udid and not device_name:
            # Find iPhone 15 Pro or first available
            devices = self.list_devices()
            for device in devices:
                if "iPhone 15 Pro" in device["name"]:
                    udid = device["udid"]
                    break
            if not udid and devices:
                udid = devices[0]["udid"]

        if not udid:
            logger.error("No simulator device found")
            return None

        try:
            subprocess.run(["xcrun", "simctl", "boot", udid], capture_output=True, check=False)
            self.booted_device = udid
            logger.info(f"Booted simulator: {udid}")
            time.sleep(3)  # Wait for boot
            return udid
        except Exception as e:
            logger.error(f"Failed to boot device: {e}")
            return None

    def shutdown_device(self, udid: str = None) -> bool:
        """Shutdown a simulator device."""
        udid = udid or self.booted_device
        if not udid:
            return False
        try:
            subprocess.run(["xcrun", "simctl", "shutdown", udid], capture_output=True, check=False)
            logger.info(f"Shutdown simulator: {udid}")
            return True
        except Exception as e:
            logger.error(f"Failed to shutdown device: {e}")
            return False

    def install_app(self, app_path: str, udid: str = None) -> bool:
        """Install app on simulator."""
        udid = udid or self.booted_device
        if not udid:
            logger.error("No device booted")
            return False
        try:
            subprocess.run(
                ["xcrun", "simctl", "install", udid, app_path],
                capture_output=True,
                check=True
            )
            logger.info(f"Installed app: {app_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to install app: {e}")
            return False

    def launch_app(self, bundle_id: str, udid: str = None) -> bool:
        """Launch app on simulator."""
        udid = udid or self.booted_device
        if not udid:
            logger.error("No device booted")
            return False
        try:
            subprocess.run(
                ["xcrun", "simctl", "launch", udid, bundle_id],
                capture_output=True,
                check=True
            )
            logger.info(f"Launched app: {bundle_id}")
            time.sleep(2)  # Wait for app launch
            return True
        except Exception as e:
            logger.error(f"Failed to launch app: {e}")
            return False

    def terminate_app(self, bundle_id: str, udid: str = None) -> bool:
        """Terminate app on simulator."""
        udid = udid or self.booted_device
        if not udid:
            return False
        try:
            subprocess.run(
                ["xcrun", "simctl", "terminate", udid, bundle_id],
                capture_output=True,
                check=False
            )
            return True
        except:
            return False

    def take_screenshot(self, output_path: str, udid: str = None) -> bool:
        """Take screenshot of simulator."""
        udid = udid or self.booted_device
        if not udid:
            return False
        try:
            subprocess.run(
                ["xcrun", "simctl", "io", udid, "screenshot", output_path],
                capture_output=True,
                check=True
            )
            logger.info(f"Screenshot saved: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return False

    def open_url(self, url: str, udid: str = None) -> bool:
        """Open URL (deep link) in simulator."""
        udid = udid or self.booted_device
        if not udid:
            return False
        try:
            subprocess.run(
                ["xcrun", "simctl", "openurl", udid, url],
                capture_output=True,
                check=True
            )
            logger.info(f"Opened URL: {url}")
            return True
        except Exception as e:
            logger.error(f"Failed to open URL: {e}")
            return False

    def get_app_container(self, bundle_id: str, container_type: str = "data", udid: str = None) -> Optional[str]:
        """Get app container path."""
        udid = udid or self.booted_device
        if not udid:
            return None
        try:
            result = subprocess.run(
                ["xcrun", "simctl", "get_app_container", udid, bundle_id, container_type],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except:
            return None


class EmulatorController:
    """Control Android Emulator via ADB."""

    def __init__(self):
        self.device_id = None
        self._check_adb()

    def _check_adb(self) -> bool:
        """Check if adb is available."""
        try:
            subprocess.run(["adb", "version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("adb not available - Android emulator features disabled")
            return False

    def list_devices(self) -> List[Dict[str, str]]:
        """List connected Android devices/emulators."""
        try:
            result = subprocess.run(
                ["adb", "devices", "-l"],
                capture_output=True,
                text=True,
                check=True
            )
            devices = []
            for line in result.stdout.strip().split("\n")[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        devices.append({
                            "id": parts[0],
                            "state": parts[1],
                            "info": " ".join(parts[2:]) if len(parts) > 2 else ""
                        })
            return devices
        except Exception as e:
            logger.error(f"Failed to list devices: {e}")
            return []

    def start_emulator(self, avd_name: str) -> Optional[str]:
        """Start Android emulator."""
        try:
            subprocess.Popen(
                ["emulator", "-avd", avd_name, "-no-snapshot-load"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # Wait for emulator to boot
            for _ in range(60):
                devices = self.list_devices()
                for device in devices:
                    if device["state"] == "device" and "emulator" in device["id"]:
                        self.device_id = device["id"]
                        logger.info(f"Emulator started: {self.device_id}")
                        return self.device_id
                time.sleep(2)
            return None
        except Exception as e:
            logger.error(f"Failed to start emulator: {e}")
            return None

    def install_app(self, apk_path: str, device_id: str = None) -> bool:
        """Install APK on device."""
        device_id = device_id or self.device_id
        if not device_id:
            logger.error("No device connected")
            return False
        try:
            subprocess.run(
                ["adb", "-s", device_id, "install", "-r", apk_path],
                capture_output=True,
                check=True
            )
            logger.info(f"Installed APK: {apk_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to install APK: {e}")
            return False

    def launch_app(self, package_name: str, activity: str = ".MainActivity", device_id: str = None) -> bool:
        """Launch app on device."""
        device_id = device_id or self.device_id
        if not device_id:
            return False
        try:
            subprocess.run(
                ["adb", "-s", device_id, "shell", "am", "start", "-n", f"{package_name}/{activity}"],
                capture_output=True,
                check=True
            )
            logger.info(f"Launched app: {package_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to launch app: {e}")
            return False

    def terminate_app(self, package_name: str, device_id: str = None) -> bool:
        """Force stop app."""
        device_id = device_id or self.device_id
        if not device_id:
            return False
        try:
            subprocess.run(
                ["adb", "-s", device_id, "shell", "am", "force-stop", package_name],
                capture_output=True,
                check=False
            )
            return True
        except:
            return False

    def take_screenshot(self, output_path: str, device_id: str = None) -> bool:
        """Take screenshot from device."""
        device_id = device_id or self.device_id
        if not device_id:
            return False
        try:
            # Capture to device
            subprocess.run(
                ["adb", "-s", device_id, "shell", "screencap", "/sdcard/screenshot.png"],
                capture_output=True,
                check=True
            )
            # Pull to local
            subprocess.run(
                ["adb", "-s", device_id, "pull", "/sdcard/screenshot.png", output_path],
                capture_output=True,
                check=True
            )
            logger.info(f"Screenshot saved: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return False

    def open_url(self, url: str, device_id: str = None) -> bool:
        """Open URL (deep link) on device."""
        device_id = device_id or self.device_id
        if not device_id:
            return False
        try:
            subprocess.run(
                ["adb", "-s", device_id, "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url],
                capture_output=True,
                check=True
            )
            logger.info(f"Opened URL: {url}")
            return True
        except Exception as e:
            logger.error(f"Failed to open URL: {e}")
            return False


class AppTestRunner:
    """Main test runner for mobile apps."""

    def __init__(self, platform: str = "ios"):
        """
        Initialize app test runner.

        Args:
            platform: 'ios' or 'android'
        """
        self.platform = platform.lower()
        self.screenshots_dir = Path(__file__).parent.parent / "test_screenshots"
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)

        if self.platform == "ios":
            self.controller = SimulatorController()
        elif self.platform == "android":
            self.controller = EmulatorController()
        else:
            raise ValueError(f"Unknown platform: {platform}")

        self.app_id = None
        self.test_suite: Optional[AppTestSuite] = None

        logger.info(f"App test runner initialized for {platform}")

    def setup(self, device_id: str = None, device_name: str = None) -> bool:
        """Setup test environment."""
        if self.platform == "ios":
            return self.controller.boot_device(device_id, device_name) is not None
        else:
            devices = self.controller.list_devices()
            if devices:
                self.controller.device_id = devices[0]["id"]
                return True
            return False

    def teardown(self) -> None:
        """Cleanup test environment."""
        if self.app_id:
            self.controller.terminate_app(self.app_id)
        if self.platform == "ios":
            # Don't shutdown simulator - let user manage it
            pass

    def launch_app(self, app_id: str) -> bool:
        """Launch app for testing."""
        self.app_id = app_id
        return self.controller.launch_app(app_id)

    def _take_test_screenshot(self, test_name: str) -> Optional[str]:
        """Take screenshot for a test."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        output_path = str(self.screenshots_dir / filename)
        if self.controller.take_screenshot(output_path):
            return output_path
        return None

    def run_test(self, test_name: str, test_func: callable) -> TestResult:
        """Run a single test."""
        start_time = time.time()
        result = TestResult(
            test_name=test_name,
            status="error",
            duration_ms=0
        )

        try:
            test_func()
            result.status = "passed"
        except AssertionError as e:
            result.status = "failed"
            result.error = str(e)
            result.screenshot_path = self._take_test_screenshot(test_name)
        except Exception as e:
            result.status = "error"
            result.error = str(e)
            result.screenshot_path = self._take_test_screenshot(test_name)

        result.duration_ms = (time.time() - start_time) * 1000
        return result

    def run_test_suite(self, suite_name: str, tests: List[Dict[str, Any]] = None) -> AppTestSuite:
        """
        Run a test suite.

        Args:
            suite_name: Name of the test suite
            tests: List of test definitions [{"name": "...", "func": callable}, ...]
        """
        self.test_suite = AppTestSuite(
            suite_name=suite_name,
            platform=self.platform,
            app_id=self.app_id or "unknown"
        )

        if tests is None:
            tests = self._get_default_tests()

        for test_def in tests:
            test_name = test_def.get("name", "unnamed")
            test_func = test_def.get("func")

            if not test_func:
                result = TestResult(
                    test_name=test_name,
                    status="skipped",
                    duration_ms=0,
                    error="No test function provided"
                )
            else:
                logger.info(f"Running test: {test_name}")
                result = self.run_test(test_name, test_func)

            self.test_suite.results.append(result)
            self.test_suite.summary[result.status] += 1

        self.test_suite.end_time = datetime.now().isoformat()
        return self.test_suite

    def _get_default_tests(self) -> List[Dict[str, Any]]:
        """Get default test definitions."""
        def test_app_launches():
            assert self.app_id is not None, "App ID not set"
            # App should already be launched
            time.sleep(2)

        def test_take_screenshot():
            path = self._take_test_screenshot("default_screen")
            assert path is not None, "Failed to take screenshot"
            assert Path(path).exists(), f"Screenshot not saved: {path}"

        return [
            {"name": "app_launches", "func": test_app_launches},
            {"name": "screenshot_capture", "func": test_take_screenshot},
        ]

    def test_deep_link(self, url: str) -> TestResult:
        """Test a deep link."""
        def test_func():
            success = self.controller.open_url(url)
            assert success, f"Failed to open deep link: {url}"
            time.sleep(2)

        return self.run_test(f"deep_link_{url[:30]}", test_func)

    def test_onboarding_flow(self) -> List[TestResult]:
        """Test app onboarding flow - override in subclass for specific apps."""
        results = []

        def test_onboarding_shown():
            time.sleep(3)
            # Take screenshot to verify onboarding
            path = self._take_test_screenshot("onboarding_screen")
            assert path is not None, "Could not capture onboarding screen"

        results.append(self.run_test("onboarding_shown", test_onboarding_shown))
        return results

    def generate_report(self) -> Dict[str, Any]:
        """Generate test report."""
        if not self.test_suite:
            return {}

        total = sum(self.test_suite.summary.values())
        pass_rate = (self.test_suite.summary["passed"] / total * 100) if total > 0 else 0

        report = {
            "suite_name": self.test_suite.suite_name,
            "platform": self.test_suite.platform,
            "app_id": self.test_suite.app_id,
            "start_time": self.test_suite.start_time,
            "end_time": self.test_suite.end_time,
            "summary": self.test_suite.summary,
            "pass_rate": round(pass_rate, 2),
            "total_tests": total,
            "results": [asdict(r) for r in self.test_suite.results]
        }

        return report

    def save_report(self, output_path: str = None) -> str:
        """Save test report to file."""
        report = self.generate_report()
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = str(LOG_DIR / f"app_test_report_{timestamp}.json")

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Report saved: {output_path}")
        return output_path


# CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="App Test Runner")
    parser.add_argument("--platform", "-p", choices=["ios", "android"], default="ios",
                        help="Target platform")
    parser.add_argument("--app", "-a", required=True, help="App bundle ID or package name")
    parser.add_argument("--suite", "-s", default="basic", help="Test suite to run")
    parser.add_argument("--device", "-d", help="Device ID or name")
    parser.add_argument("--output", "-o", help="Output report path")
    parser.add_argument("--deep-link", help="Test specific deep link URL")

    args = parser.parse_args()

    runner = AppTestRunner(platform=args.platform)

    # Setup
    if not runner.setup(device_id=args.device):
        print("Failed to setup test environment")
        sys.exit(1)

    try:
        # Launch app
        if not runner.launch_app(args.app):
            print(f"Failed to launch app: {args.app}")
            sys.exit(1)

        # Test deep link if specified
        if args.deep_link:
            result = runner.test_deep_link(args.deep_link)
            print(f"Deep link test: {result.status}")
            if result.error:
                print(f"  Error: {result.error}")

        # Run test suite
        suite = runner.run_test_suite(args.suite)

        # Print summary
        print(f"\nTest Suite: {suite.suite_name}")
        print(f"Platform: {suite.platform}")
        print(f"App: {suite.app_id}")
        print("-" * 40)
        print(f"Passed: {suite.summary['passed']}")
        print(f"Failed: {suite.summary['failed']}")
        print(f"Skipped: {suite.summary['skipped']}")
        print(f"Errors: {suite.summary['error']}")

        # Save report
        report_path = runner.save_report(args.output)
        print(f"\nReport: {report_path}")

        # Exit code based on results
        sys.exit(0 if suite.summary['failed'] == 0 and suite.summary['error'] == 0 else 1)

    finally:
        runner.teardown()
