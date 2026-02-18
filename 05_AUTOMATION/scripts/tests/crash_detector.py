#!/usr/bin/env python3
"""
Crash Detector - Mobile App Crash Detection and Logging
========================================================
Monitor apps for crashes, ANRs, and errors during testing.

Features:
- Real-time crash detection
- iOS crash log parsing
- Android logcat monitoring
- ANR (Application Not Responding) detection
- Symbolication support
- Crash report aggregation
- Alert notifications

Usage:
    from crash_detector import CrashDetector

    detector = CrashDetector(platform="ios")
    detector.start_monitoring("com.printmaxx.aiclarity")

    # ... run tests ...

    crashes = detector.stop_monitoring()
    detector.generate_report()

CLI:
    python crash_detector.py --platform ios --app com.printmaxx.aiclarity --duration 60
    python crash_detector.py --platform android --app com.printmaxx.aiclarity --logcat
"""

import os
import sys
import json
import time
import re
import subprocess
import threading
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import signal

# Configure logging
LOG_DIR = Path(__file__).parent.parent.parent / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "crash_detector.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("crash_detector")


@dataclass
class CrashEvent:
    """Represents a crash event."""
    crash_id: str
    timestamp: str
    app_id: str
    platform: str
    crash_type: str  # crash, anr, exception, oom
    signal: Optional[str] = None
    thread: Optional[str] = None
    exception_type: Optional[str] = None
    exception_message: Optional[str] = None
    stack_trace: List[str] = field(default_factory=list)
    device_info: Dict[str, str] = field(default_factory=dict)
    raw_log: Optional[str] = None
    symbolicated: bool = False


@dataclass
class MonitoringSession:
    """Monitoring session metadata."""
    session_id: str
    app_id: str
    platform: str
    start_time: str
    end_time: Optional[str] = None
    crashes: List[CrashEvent] = field(default_factory=list)
    errors: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class IOSCrashParser:
    """Parse iOS crash logs."""

    # Common crash signals
    CRASH_SIGNALS = {
        "SIGSEGV": "Segmentation fault",
        "SIGBUS": "Bus error",
        "SIGABRT": "Abort signal",
        "SIGILL": "Illegal instruction",
        "SIGFPE": "Floating point exception",
        "SIGTRAP": "Trap",
        "EXC_BAD_ACCESS": "Bad memory access",
        "EXC_CRASH": "Abnormal termination",
        "EXC_BREAKPOINT": "Breakpoint",
    }

    def parse_crash_log(self, log_content: str, app_id: str) -> Optional[CrashEvent]:
        """Parse an iOS crash log file."""
        crash_id = f"ios_{int(time.time()*1000)}"

        crash = CrashEvent(
            crash_id=crash_id,
            timestamp=datetime.now().isoformat(),
            app_id=app_id,
            platform="ios",
            crash_type="crash",
            raw_log=log_content[:5000]  # Truncate for storage
        )

        # Parse exception type
        exception_match = re.search(r"Exception Type:\s+(\S+)", log_content)
        if exception_match:
            crash.signal = exception_match.group(1)
            crash.crash_type = self._get_crash_type(crash.signal)

        # Parse exception message
        reason_match = re.search(r"Exception Codes?:\s+(.+)", log_content)
        if reason_match:
            crash.exception_message = reason_match.group(1).strip()

        # Parse termination reason
        term_match = re.search(r"Termination Reason:\s+(.+)", log_content)
        if term_match:
            if not crash.exception_message:
                crash.exception_message = term_match.group(1).strip()

        # Parse crashed thread
        thread_match = re.search(r"Crashed Thread:\s+(\d+)", log_content)
        if thread_match:
            crash.thread = f"Thread {thread_match.group(1)}"

        # Parse stack trace for crashed thread
        crash.stack_trace = self._parse_stack_trace(log_content)

        # Parse device info
        crash.device_info = self._parse_device_info(log_content)

        return crash

    def _get_crash_type(self, signal: str) -> str:
        """Determine crash type from signal."""
        if signal in self.CRASH_SIGNALS:
            return "crash"
        if "MEMORY" in signal.upper() or "OOM" in signal.upper():
            return "oom"
        return "crash"

    def _parse_stack_trace(self, log_content: str) -> List[str]:
        """Extract stack trace from crash log."""
        frames = []

        # Find crashed thread section
        thread_section = re.search(
            r"Thread \d+ Crashed:[\s\S]*?(?=Thread \d+|\Z)",
            log_content
        )

        if thread_section:
            section_text = thread_section.group(0)
            # Parse frames: 0   MyApp  0x00000001000... functionName + offset
            frame_pattern = r"(\d+)\s+(\S+)\s+(0x[0-9a-fA-F]+)\s+(.+)"
            matches = re.finditer(frame_pattern, section_text)
            for match in matches:
                frame_num, binary, address, symbol = match.groups()
                frames.append(f"{frame_num}: {binary} {symbol.strip()}")

        return frames[:20]  # Limit to top 20 frames

    def _parse_device_info(self, log_content: str) -> Dict[str, str]:
        """Extract device information from crash log."""
        info = {}

        patterns = {
            "hardware_model": r"Hardware Model:\s+(\S+)",
            "os_version": r"OS Version:\s+(.+)",
            "code_type": r"Code Type:\s+(\S+)",
            "app_version": r"Version:\s+([^\s\(]+)",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, log_content)
            if match:
                info[key] = match.group(1).strip()

        return info


class AndroidLogcatParser:
    """Parse Android logcat output for crashes."""

    # Fatal exception patterns
    FATAL_PATTERNS = [
        r"FATAL EXCEPTION",
        r"java\.lang\.\w+Exception",
        r"AndroidRuntime.*E.*FATAL",
        r"Caused by:",
        r"ANR in",
    ]

    def __init__(self):
        self.current_crash: Optional[CrashEvent] = None
        self.crash_buffer: List[str] = []
        self.in_crash_block = False

    def parse_line(self, line: str, app_id: str) -> Optional[CrashEvent]:
        """Parse a single logcat line."""
        # Check for new crash start
        for pattern in self.FATAL_PATTERNS:
            if re.search(pattern, line):
                if self.in_crash_block and self.current_crash:
                    # Finish previous crash
                    completed = self._finalize_crash()
                    self._start_new_crash(line, app_id)
                    return completed
                else:
                    self._start_new_crash(line, app_id)
                    return None

        # If in crash block, accumulate lines
        if self.in_crash_block:
            self.crash_buffer.append(line)

            # Check for stack trace end
            if self._is_crash_end(line):
                return self._finalize_crash()

        return None

    def _start_new_crash(self, line: str, app_id: str) -> None:
        """Start tracking a new crash."""
        crash_id = f"android_{int(time.time()*1000)}"

        self.current_crash = CrashEvent(
            crash_id=crash_id,
            timestamp=datetime.now().isoformat(),
            app_id=app_id,
            platform="android",
            crash_type="crash"
        )

        # Detect ANR
        if "ANR in" in line:
            self.current_crash.crash_type = "anr"
            anr_match = re.search(r"ANR in (\S+)", line)
            if anr_match:
                self.current_crash.exception_type = "ANR"
                self.current_crash.exception_message = f"Application Not Responding: {anr_match.group(1)}"

        # Detect exception type
        exception_match = re.search(r"([\w\.]+Exception):\s*(.+)?", line)
        if exception_match:
            self.current_crash.exception_type = exception_match.group(1)
            self.current_crash.exception_message = exception_match.group(2) or ""

        self.crash_buffer = [line]
        self.in_crash_block = True

    def _finalize_crash(self) -> Optional[CrashEvent]:
        """Finalize current crash event."""
        if not self.current_crash:
            return None

        # Parse stack trace from buffer
        stack_trace = []
        for line in self.crash_buffer:
            if "\tat " in line:
                # Java stack frame
                frame = line.strip()
                if frame.startswith("at "):
                    frame = frame[3:]
                stack_trace.append(frame)

        self.current_crash.stack_trace = stack_trace[:20]
        self.current_crash.raw_log = "\n".join(self.crash_buffer[:100])

        crash = self.current_crash
        self.current_crash = None
        self.crash_buffer = []
        self.in_crash_block = False

        return crash

    def _is_crash_end(self, line: str) -> bool:
        """Check if line indicates end of crash block."""
        # End markers
        end_markers = [
            "--- end of stack trace ---",
            "System.exit called",
            "Shutting down VM",
        ]
        return any(marker in line for marker in end_markers)


class CrashDetector:
    """Main crash detection and monitoring class."""

    def __init__(self, platform: str = "ios"):
        """
        Initialize crash detector.

        Args:
            platform: 'ios' or 'android'
        """
        self.platform = platform.lower()
        self.output_dir = Path(__file__).parent.parent / "crash_reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.session: Optional[MonitoringSession] = None
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._callbacks: List[Callable[[CrashEvent], None]] = []

        if self.platform == "ios":
            self.parser = IOSCrashParser()
        elif self.platform == "android":
            self.parser = AndroidLogcatParser()
        else:
            raise ValueError(f"Unknown platform: {platform}")

        logger.info(f"Crash detector initialized for {platform}")

    def add_callback(self, callback: Callable[[CrashEvent], None]) -> None:
        """Add a callback for crash events."""
        self._callbacks.append(callback)

    def _notify_callbacks(self, crash: CrashEvent) -> None:
        """Notify all registered callbacks."""
        for callback in self._callbacks:
            try:
                callback(crash)
            except Exception as e:
                logger.error(f"Callback error: {e}")

    def start_monitoring(self, app_id: str) -> str:
        """
        Start monitoring for crashes.

        Args:
            app_id: App bundle ID or package name

        Returns:
            Session ID
        """
        session_id = f"session_{int(time.time()*1000)}"

        self.session = MonitoringSession(
            session_id=session_id,
            app_id=app_id,
            platform=self.platform,
            start_time=datetime.now().isoformat()
        )

        self._monitoring = True

        if self.platform == "ios":
            self._monitor_thread = threading.Thread(
                target=self._monitor_ios_crashes,
                args=(app_id,),
                daemon=True
            )
        else:
            self._monitor_thread = threading.Thread(
                target=self._monitor_android_crashes,
                args=(app_id,),
                daemon=True
            )

        self._monitor_thread.start()
        logger.info(f"Started monitoring session: {session_id}")

        return session_id

    def stop_monitoring(self) -> List[CrashEvent]:
        """
        Stop monitoring and return collected crashes.

        Returns:
            List of crash events
        """
        self._monitoring = False

        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)

        if self.session:
            self.session.end_time = datetime.now().isoformat()

        logger.info(f"Stopped monitoring. Crashes detected: {len(self.session.crashes) if self.session else 0}")

        return self.session.crashes if self.session else []

    def _monitor_ios_crashes(self, app_id: str) -> None:
        """Monitor iOS crash logs."""
        # Watch for new crash logs
        crash_log_dir = Path.home() / "Library/Logs/DiagnosticReports"

        if not crash_log_dir.exists():
            logger.warning(f"Crash log directory not found: {crash_log_dir}")
            return

        # Get list of existing crash logs to ignore
        existing_logs = set(crash_log_dir.glob("*.crash"))
        existing_logs.update(crash_log_dir.glob("*.ips"))

        while self._monitoring:
            try:
                # Check for new crash logs
                current_logs = set(crash_log_dir.glob("*.crash"))
                current_logs.update(crash_log_dir.glob("*.ips"))

                new_logs = current_logs - existing_logs

                for log_path in new_logs:
                    try:
                        content = log_path.read_text()

                        # Check if crash is for our app
                        if app_id in content or app_id.split(".")[-1] in content:
                            crash = self.parser.parse_crash_log(content, app_id)
                            if crash:
                                self.session.crashes.append(crash)
                                self._notify_callbacks(crash)
                                logger.warning(f"Crash detected: {crash.crash_id}")

                        existing_logs.add(log_path)

                    except Exception as e:
                        logger.error(f"Error parsing crash log {log_path}: {e}")

                time.sleep(1)

            except Exception as e:
                logger.error(f"Error monitoring iOS crashes: {e}")
                time.sleep(5)

    def _monitor_android_crashes(self, app_id: str) -> None:
        """Monitor Android logcat for crashes."""
        try:
            # Clear logcat buffer first
            subprocess.run(["adb", "logcat", "-c"], capture_output=True)

            # Start logcat process
            process = subprocess.Popen(
                ["adb", "logcat", "-v", "threadtime", "*:E"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            while self._monitoring:
                line = process.stdout.readline()
                if not line:
                    time.sleep(0.1)
                    continue

                # Filter for our app
                if app_id in line or "AndroidRuntime" in line:
                    crash = self.parser.parse_line(line, app_id)
                    if crash:
                        self.session.crashes.append(crash)
                        self._notify_callbacks(crash)
                        logger.warning(f"Crash detected: {crash.crash_id}")

            process.terminate()

        except FileNotFoundError:
            logger.error("adb not found - Android crash monitoring disabled")
        except Exception as e:
            logger.error(f"Error monitoring Android crashes: {e}")

    def check_for_crash_now(self, app_id: str) -> Optional[CrashEvent]:
        """
        Check for recent crashes (polling method).

        Args:
            app_id: App bundle ID or package name

        Returns:
            Most recent crash if found
        """
        if self.platform == "ios":
            return self._check_ios_recent_crash(app_id)
        else:
            return self._check_android_recent_crash(app_id)

    def _check_ios_recent_crash(self, app_id: str) -> Optional[CrashEvent]:
        """Check for recent iOS crash."""
        crash_log_dir = Path.home() / "Library/Logs/DiagnosticReports"
        if not crash_log_dir.exists():
            return None

        # Get most recent crash log
        crash_files = list(crash_log_dir.glob("*.crash"))
        crash_files.extend(crash_log_dir.glob("*.ips"))

        if not crash_files:
            return None

        most_recent = max(crash_files, key=lambda p: p.stat().st_mtime)

        # Check if recent (last 60 seconds)
        if time.time() - most_recent.stat().st_mtime > 60:
            return None

        content = most_recent.read_text()
        if app_id in content or app_id.split(".")[-1] in content:
            return self.parser.parse_crash_log(content, app_id)

        return None

    def _check_android_recent_crash(self, app_id: str) -> Optional[CrashEvent]:
        """Check for recent Android crash in logcat."""
        try:
            result = subprocess.run(
                ["adb", "logcat", "-d", "-t", "100", "*:E"],
                capture_output=True,
                text=True,
                timeout=10
            )

            for line in result.stdout.split("\n"):
                if app_id in line or "AndroidRuntime" in line:
                    crash = self.parser.parse_line(line, app_id)
                    if crash:
                        return crash

            return None

        except Exception as e:
            logger.error(f"Error checking Android crashes: {e}")
            return None

    def generate_report(self, output_path: str = None) -> str:
        """
        Generate crash report.

        Args:
            output_path: Optional output file path

        Returns:
            Report file path
        """
        if not self.session:
            logger.warning("No monitoring session to report")
            return ""

        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = str(self.output_dir / f"crash_report_{timestamp}.json")

        # Aggregate crashes by type
        by_type = defaultdict(list)
        for crash in self.session.crashes:
            by_type[crash.crash_type].append(crash)

        # Generate summary
        report = {
            "session": {
                "session_id": self.session.session_id,
                "app_id": self.session.app_id,
                "platform": self.session.platform,
                "start_time": self.session.start_time,
                "end_time": self.session.end_time,
            },
            "summary": {
                "total_crashes": len(self.session.crashes),
                "by_type": {k: len(v) for k, v in by_type.items()},
            },
            "crashes": [asdict(c) for c in self.session.crashes],
            "warnings": self.session.warnings,
        }

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Crash report saved: {output_path}")
        return output_path

    def get_crash_summary(self) -> Dict[str, Any]:
        """Get a quick summary of detected crashes."""
        if not self.session:
            return {"crashes": 0, "anrs": 0, "ooms": 0}

        summary = {
            "crashes": 0,
            "anrs": 0,
            "ooms": 0,
            "exceptions": defaultdict(int)
        }

        for crash in self.session.crashes:
            if crash.crash_type == "anr":
                summary["anrs"] += 1
            elif crash.crash_type == "oom":
                summary["ooms"] += 1
            else:
                summary["crashes"] += 1

            if crash.exception_type:
                summary["exceptions"][crash.exception_type] += 1

        summary["exceptions"] = dict(summary["exceptions"])
        return summary


# CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Crash Detector")
    parser.add_argument("--platform", "-p", choices=["ios", "android"], default="ios",
                        help="Target platform")
    parser.add_argument("--app", "-a", required=True, help="App bundle ID or package name")
    parser.add_argument("--duration", "-d", type=int, default=60,
                        help="Monitoring duration in seconds")
    parser.add_argument("--output", "-o", help="Output report path")
    parser.add_argument("--check-now", action="store_true",
                        help="Check for recent crash and exit")

    args = parser.parse_args()

    detector = CrashDetector(platform=args.platform)

    # Add simple callback to print crashes
    def on_crash(crash: CrashEvent):
        print(f"\n[CRASH DETECTED] {crash.crash_type.upper()}")
        print(f"  Exception: {crash.exception_type}")
        print(f"  Message: {crash.exception_message}")
        if crash.stack_trace:
            print(f"  Stack trace (first 3 frames):")
            for frame in crash.stack_trace[:3]:
                print(f"    {frame}")

    detector.add_callback(on_crash)

    if args.check_now:
        # Just check for recent crash
        crash = detector.check_for_crash_now(args.app)
        if crash:
            print(f"Recent crash found: {crash.crash_id}")
            print(f"  Type: {crash.crash_type}")
            print(f"  Exception: {crash.exception_type}")
            sys.exit(1)
        else:
            print("No recent crashes found")
            sys.exit(0)

    # Start monitoring
    print(f"Starting crash monitoring for {args.app}")
    print(f"Duration: {args.duration} seconds")
    print("-" * 40)

    session_id = detector.start_monitoring(args.app)

    try:
        # Wait for duration
        for i in range(args.duration):
            time.sleep(1)
            if i % 10 == 0:
                summary = detector.get_crash_summary()
                print(f"[{i}s] Crashes: {summary['crashes']}, ANRs: {summary['anrs']}")

    except KeyboardInterrupt:
        print("\nStopping monitoring...")

    # Stop and report
    crashes = detector.stop_monitoring()

    print(f"\n{'=' * 40}")
    print(f"Monitoring complete")
    print(f"Total crashes detected: {len(crashes)}")

    # Generate report
    report_path = detector.generate_report(args.output)
    print(f"Report: {report_path}")

    # Summary
    summary = detector.get_crash_summary()
    print(f"\nSummary:")
    print(f"  Crashes: {summary['crashes']}")
    print(f"  ANRs: {summary['anrs']}")
    print(f"  OOMs: {summary['ooms']}")

    if summary['exceptions']:
        print(f"  Exception types:")
        for exc_type, count in summary['exceptions'].items():
            print(f"    {exc_type}: {count}")

    sys.exit(1 if crashes else 0)
