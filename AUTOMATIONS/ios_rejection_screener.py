#!/usr/bin/env python3
"""
iOS App Store Rejection Screener
================================
Auto-screens iOS app projects against the top 20+ Apple App Store rejection
reasons (2025-2026 data). Catches issues BEFORE submission to avoid delays.

Research-backed rejection categories (approximate percentages from Apple data):
  1. Privacy violations (~25%)           - Missing privacy policy, PrivacyInfo.xcprivacy
  2. App completeness (Guideline 2.1, ~40% of unresolved) - Crashes, placeholders
  3. Performance issues (~14%)           - Bugs, broken features
  4. Legal issues (~5%)                  - IP violations, missing licenses
  5. Guideline 4.3 Spam (~8%)           - Duplicate/template apps
  6. Guideline 4.2 Minimum Functionality (~6%) - WebView wrappers
  7. Missing required device capabilities
  8. Incorrect or missing age ratings
  9. Subscription compliance failures
  10. Missing required screenshots
  11. Hardcoded test/debug data
  12. Missing usage description strings (NSCameraUsageDescription etc.)
  13. Incorrect bundle identifier format
  14. Missing app icon (1024x1024)
  15. Lorem ipsum / placeholder content
  16. Missing required API declarations (PrivacyInfo.xcprivacy)
  17. No restore purchases button (subscriptions)
  18. Missing terms of service / EULA for subscriptions
  19. External payment link compliance (EU DMA / US)
  20. AI data sharing without consent disclosure (Guideline 5.1.2(i), Nov 2025)

Usage:
  python3 ios_rejection_screener.py --check /path/to/MyApp.xcodeproj/..
  python3 ios_rejection_screener.py --fix /path/to/MyApp
  python3 ios_rejection_screener.py --report /path/to/MyApp
  python3 ios_rejection_screener.py --check /path/to/MyApp --output report.json

Author: PRINTMAXX Automation
"""

import argparse
import json
import os
import plistlib
import re
import sys
import glob as glob_module
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# SAFE PATH VALIDATION
# ---------------------------------------------------------------------------
PRINTMAXX_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def safe_path(path: str) -> str:
    """Ensure all file operations stay within the PRINTMAXX project folder."""
    resolved = os.path.realpath(os.path.abspath(path))
    if not resolved.startswith(os.path.realpath(PRINTMAXX_ROOT)):
        raise ValueError(
            f"SECURITY: Path '{path}' resolves outside the PRINTMAXX project folder.\n"
            f"  Resolved: {resolved}\n"
            f"  Allowed root: {PRINTMAXX_ROOT}"
        )
    return resolved


# ---------------------------------------------------------------------------
# DATA STRUCTURES
# ---------------------------------------------------------------------------

class Severity(str, Enum):
    CRITICAL = "CRITICAL"   # Will definitely cause rejection
    HIGH = "HIGH"           # Very likely to cause rejection
    MEDIUM = "MEDIUM"       # May cause rejection depending on reviewer
    LOW = "LOW"             # Best practice, unlikely to reject alone
    INFO = "INFO"           # Informational


@dataclass
class Finding:
    check_id: str
    guideline: str
    severity: Severity
    title: str
    message: str
    file_path: Optional[str] = None
    fix_instruction: str = ""
    auto_fixable: bool = False
    fixed: bool = False


@dataclass
class ScreeningReport:
    app_path: str
    timestamp: str = ""
    passed: bool = True
    total_checks: int = 0
    findings: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    def __post_init__(self):
        self.timestamp = datetime.now().isoformat()

    def add(self, finding: Finding):
        self.findings.append(finding)
        if finding.severity in (Severity.CRITICAL, Severity.HIGH):
            self.passed = False

    def to_dict(self):
        d = asdict(self)
        d["findings"] = [asdict(f) for f in self.findings]
        return d


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def find_files(root: str, pattern: str) -> list:
    """Recursively find files matching a glob pattern under root."""
    return glob_module.glob(os.path.join(root, "**", pattern), recursive=True)


def find_plist_files(root: str) -> list:
    """Find Info.plist files, excluding Pods/build dirs."""
    results = []
    for p in find_files(root, "Info.plist"):
        lower = p.lower()
        if "/pods/" not in lower and "/build/" not in lower and "/deriveddata/" not in lower:
            results.append(p)
    return results


def read_plist(path: str) -> dict:
    """Read a plist file and return its contents as a dict."""
    try:
        with open(path, "rb") as f:
            return plistlib.load(f)
    except Exception:
        # Try XML format
        try:
            with open(path, "r") as f:
                content = f.read()
            # Basic XML plist parsing fallback
            return {"_raw": content, "_parse_error": True}
        except Exception:
            return {}


def scan_source_files(root: str) -> list:
    """Get all Swift/ObjC source files excluding Pods/build."""
    extensions = ["*.swift", "*.m", "*.mm", "*.h"]
    results = []
    for ext in extensions:
        for p in find_files(root, ext):
            lower = p.lower()
            if "/pods/" not in lower and "/build/" not in lower and "/deriveddata/" not in lower:
                results.append(p)
    return results


def read_file_safe(path: str) -> str:
    """Read file content, return empty string on failure."""
    try:
        with open(path, "r", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


def file_exists_in_project(root: str, filename: str) -> list:
    """Check if a file exists anywhere in the project."""
    return find_files(root, filename)


# ---------------------------------------------------------------------------
# CHECK FUNCTIONS
# ---------------------------------------------------------------------------

def check_privacy_policy(root: str, report: ScreeningReport):
    """Check for privacy policy URL in Info.plist or source code."""
    report.total_checks += 1

    plists = find_plist_files(root)
    privacy_url_found = False

    for plist_path in plists:
        data = read_plist(plist_path)
        if data.get("_parse_error"):
            raw = data.get("_raw", "")
            if "privacy" in raw.lower() and ("http" in raw.lower() or "url" in raw.lower()):
                privacy_url_found = True
                break
        else:
            # Check for common privacy policy keys
            for key in ["NSPrivacyPolicyURL", "privacy_policy_url", "PrivacyPolicyURL"]:
                if key in data:
                    privacy_url_found = True
                    break

    # Also scan source code for privacy policy URLs
    if not privacy_url_found:
        sources = scan_source_files(root)
        for src in sources:
            content = read_file_safe(src)
            if re.search(r"privacy.?policy", content, re.IGNORECASE) and re.search(r"https?://", content):
                privacy_url_found = True
                break

    # Check storyboards / SwiftUI for privacy references
    if not privacy_url_found:
        storyboards = find_files(root, "*.storyboard") + find_files(root, "*.xib")
        for sb in storyboards:
            content = read_file_safe(sb)
            if "privacy" in content.lower():
                privacy_url_found = True
                break

    if not privacy_url_found:
        report.add(Finding(
            check_id="PRIVACY_POLICY_URL",
            guideline="Guideline 5.1.1 - Data Collection and Storage",
            severity=Severity.CRITICAL,
            title="Missing Privacy Policy URL",
            message=(
                "No privacy policy URL detected in Info.plist or source code. "
                "Apple requires all apps that collect any user data to link to a privacy policy. "
                "This is the #1 rejection reason (~25% of all rejections)."
            ),
            fix_instruction=(
                "1. Create a privacy policy page (use a generator like freeprivacypolicy.com)\n"
                "2. Host it at a public URL\n"
                "3. Add it to App Store Connect under 'App Information' > 'Privacy Policy URL'\n"
                "4. Also add a link within the app (Settings screen or onboarding)"
            ),
            auto_fixable=False,
        ))


def check_privacy_manifest(root: str, report: ScreeningReport):
    """Check for PrivacyInfo.xcprivacy file (required since May 2024)."""
    report.total_checks += 1

    manifests = file_exists_in_project(root, "PrivacyInfo.xcprivacy")
    # Filter out Pods/build
    manifests = [m for m in manifests if "/pods/" not in m.lower() and "/build/" not in m.lower()]

    if not manifests:
        report.add(Finding(
            check_id="PRIVACY_MANIFEST",
            guideline="Privacy Manifest Requirements (May 2024+)",
            severity=Severity.CRITICAL,
            title="Missing PrivacyInfo.xcprivacy",
            message=(
                "No PrivacyInfo.xcprivacy file found. Since May 1, 2024, Apple rejects apps "
                "that don't include a privacy manifest declaring use of required-reason APIs. "
                "Required APIs include: UserDefaults, file timestamps, system boot time, "
                "disk space, and active keyboard."
            ),
            fix_instruction=(
                "1. In Xcode: File > New > File > App Privacy\n"
                "2. Name it 'PrivacyInfo.xcprivacy'\n"
                "3. Declare all required-reason API usage:\n"
                "   - NSPrivacyAccessedAPITypes: list each API category + reason codes\n"
                "   - NSPrivacyTracking: false (if you don't track)\n"
                "   - NSPrivacyTrackingDomains: [] (if none)\n"
                "   - NSPrivacyCollectedDataTypes: list data you collect\n"
                "4. See: https://developer.apple.com/documentation/bundleresources/privacy-manifest-files"
            ),
            auto_fixable=True,
        ))
    else:
        # Validate manifest contents
        for manifest_path in manifests:
            data = read_plist(manifest_path)
            if not data.get("_parse_error"):
                if "NSPrivacyAccessedAPITypes" not in data:
                    report.add(Finding(
                        check_id="PRIVACY_MANIFEST_INCOMPLETE",
                        guideline="Privacy Manifest Requirements",
                        severity=Severity.HIGH,
                        title="PrivacyInfo.xcprivacy missing API declarations",
                        message=(
                            f"File {manifest_path} exists but does not declare "
                            "NSPrivacyAccessedAPITypes. Most apps use UserDefaults at minimum."
                        ),
                        file_path=manifest_path,
                        fix_instruction=(
                            "Add NSPrivacyAccessedAPITypes array with entries for each "
                            "required-reason API your app uses (e.g., NSPrivacyAccessedAPICategoryUserDefaults)."
                        ),
                    ))


def check_app_icon(root: str, report: ScreeningReport):
    """Check for 1024x1024 app icon in asset catalog."""
    report.total_checks += 1

    # Look for AppIcon in asset catalogs
    asset_catalogs = find_files(root, "*.appiconset")
    asset_catalogs = [a for a in asset_catalogs if "/pods/" not in a.lower() and "/build/" not in a.lower()]

    if not asset_catalogs:
        # Also check for standalone icon files
        icon_files = (
            find_files(root, "AppIcon*.png") +
            find_files(root, "Icon*.png") +
            find_files(root, "app_icon*.png")
        )
        icon_files = [i for i in icon_files if "/pods/" not in i.lower() and "/build/" not in i.lower()]

        if not icon_files:
            report.add(Finding(
                check_id="APP_ICON_MISSING",
                guideline="Guideline 2.1 - App Completeness",
                severity=Severity.CRITICAL,
                title="No App Icon Found",
                message="No AppIcon asset catalog or icon PNG files found. Apple requires a 1024x1024 app icon.",
                fix_instruction=(
                    "1. Create a 1024x1024 PNG icon (no alpha/transparency)\n"
                    "2. In Xcode: Assets.xcassets > AppIcon\n"
                    "3. Drag your icon into the 'App Store' slot (1024x1024)\n"
                    "4. Xcode 15+ auto-generates other sizes from the single 1024 icon"
                ),
                auto_fixable=False,
            ))
    else:
        # Check Contents.json for 1024x1024
        for appiconset in asset_catalogs:
            contents_json = os.path.join(appiconset, "Contents.json")
            if os.path.exists(contents_json):
                try:
                    with open(contents_json) as f:
                        contents = json.load(f)
                    images = contents.get("images", [])
                    has_1024 = any(
                        img.get("size") == "1024x1024" and img.get("filename")
                        for img in images
                    )
                    if not has_1024:
                        report.add(Finding(
                            check_id="APP_ICON_NO_1024",
                            guideline="Guideline 2.1 - App Completeness",
                            severity=Severity.CRITICAL,
                            title="Missing 1024x1024 App Store Icon",
                            message=f"AppIcon set at {appiconset} has no 1024x1024 icon assigned.",
                            file_path=contents_json,
                            fix_instruction="Add a 1024x1024 PNG (no transparency) to the AppIcon asset catalog.",
                        ))
                except (json.JSONDecodeError, IOError):
                    pass

            # Validate icon dimensions if possible
            try:
                import struct
                png_files = glob_module.glob(os.path.join(appiconset, "*.png"))
                for png in png_files:
                    with open(png, "rb") as f:
                        header = f.read(24)
                    if len(header) >= 24 and header[:8] == b'\x89PNG\r\n\x1a\n':
                        w = struct.unpack(">I", header[16:20])[0]
                        h = struct.unpack(">I", header[20:24])[0]
                        if w == 1024 and h == 1024:
                            # Check for alpha channel (transparency)
                            # PNG color type is at byte 25
                            with open(png, "rb") as f:
                                f.read(25)
                                color_type = struct.unpack("B", f.read(1))[0]
                            if color_type in (4, 6):  # grayscale+alpha or RGBA
                                report.add(Finding(
                                    check_id="APP_ICON_ALPHA",
                                    guideline="Guideline 2.1 - App Completeness",
                                    severity=Severity.HIGH,
                                    title="App Icon May Have Transparency",
                                    message=(
                                        f"Icon {png} appears to have an alpha channel. "
                                        "Apple rejects icons with transparency."
                                    ),
                                    file_path=png,
                                    fix_instruction="Re-export the icon as RGB PNG without alpha channel.",
                                ))
            except Exception:
                pass


def check_placeholder_content(root: str, report: ScreeningReport):
    """Scan for lorem ipsum, placeholder text, and test data."""
    report.total_checks += 1

    placeholder_patterns = [
        (r"\blorem\s+ipsum\b", "Lorem ipsum placeholder text"),
        (r"\bplaceholder\b", "Placeholder text"),
        (r"\bTODO\b", "TODO marker (may indicate incomplete feature)"),
        (r"\bFIXME\b", "FIXME marker (indicates known issue)"),
        (r"\btest@test\.com\b", "Test email address"),
        (r"\btest@example\.com\b", "Test email address"),
        (r"\b(xxx|XXXX)\b", "Placeholder XXX text"),
        (r"\bhello\s+world\b", "Hello World placeholder"),
        (r"\bfoo\s*bar\b", "Foobar test text"),
        (r"\b192\.168\.\d+\.\d+\b", "Local IP address (hardcoded)"),
        (r"\blocalhost\b", "Localhost reference"),
        (r"https?://example\.com", "Example.com URL"),
        (r"\bapi[_-]?key\s*[:=]\s*['\"](?:test|demo|sample|your)", "Hardcoded test API key"),
    ]

    sources = scan_source_files(root)
    # Also check storyboards, XIBs, strings files
    sources += find_files(root, "*.storyboard")
    sources += find_files(root, "*.xib")
    sources += find_files(root, "*.strings")
    sources = [s for s in sources if "/pods/" not in s.lower() and "/build/" not in s.lower()]

    found_placeholders = []
    for src in sources:
        content = read_file_safe(src)
        for pattern, desc in placeholder_patterns:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                # Get line numbers
                lines = content[:matches[0].start()].count("\n") + 1
                found_placeholders.append((src, desc, lines, len(matches)))

    if found_placeholders:
        details = "\n".join(
            f"  - {os.path.basename(f)}: {desc} (line ~{line}, {count} occurrence(s))"
            for f, desc, line, count in found_placeholders[:15]
        )
        severity = Severity.CRITICAL if any(
            "lorem ipsum" in desc.lower() or "test email" in desc.lower()
            for _, desc, _, _ in found_placeholders
        ) else Severity.MEDIUM

        report.add(Finding(
            check_id="PLACEHOLDER_CONTENT",
            guideline="Guideline 2.1 - App Completeness",
            severity=severity,
            title="Placeholder / Test Content Detected",
            message=f"Found {len(found_placeholders)} file(s) with placeholder content:\n{details}",
            fix_instruction=(
                "Remove or replace all placeholder text before submission:\n"
                "- Replace lorem ipsum with real content\n"
                "- Remove TODO/FIXME comments or resolve them\n"
                "- Replace test emails/URLs with production values\n"
                "- Remove localhost/local IP references\n"
                "- Remove hardcoded test API keys"
            ),
        ))


def check_info_plist_keys(root: str, report: ScreeningReport):
    """Check Info.plist for required keys based on API usage."""
    report.total_checks += 1

    plists = find_plist_files(root)
    sources = scan_source_files(root)

    # Map of framework usage patterns -> required Info.plist keys
    usage_descriptions = {
        "NSCameraUsageDescription": {
            "patterns": [r"\bAVCapture", r"UIImagePickerController.*\.camera", r"\.camera\b",
                         r"AVFoundation", r"captureSession"],
            "label": "Camera",
        },
        "NSPhotoLibraryUsageDescription": {
            "patterns": [r"PHPhoto", r"UIImagePickerController", r"\.photoLibrary",
                         r"PHAsset", r"PHPickerViewController"],
            "label": "Photo Library",
        },
        "NSMicrophoneUsageDescription": {
            "patterns": [r"AVAudioRecorder", r"AVAudioSession.*\.record", r"microphone",
                         r"AVCaptureDevice.*audio"],
            "label": "Microphone",
        },
        "NSLocationWhenInUseUsageDescription": {
            "patterns": [r"CLLocationManager", r"requestWhenInUseAuthorization",
                         r"locationManager", r"CoreLocation"],
            "label": "Location (When In Use)",
        },
        "NSLocationAlwaysUsageDescription": {
            "patterns": [r"requestAlwaysAuthorization", r"allowsBackgroundLocationUpdates"],
            "label": "Location (Always)",
        },
        "NSContactsUsageDescription": {
            "patterns": [r"CNContact", r"ABAddressBook", r"Contacts\.framework"],
            "label": "Contacts",
        },
        "NSCalendarsUsageDescription": {
            "patterns": [r"EKEventStore", r"EventKit"],
            "label": "Calendar",
        },
        "NSBluetoothAlwaysUsageDescription": {
            "patterns": [r"CBCentralManager", r"CBPeripheralManager", r"CoreBluetooth"],
            "label": "Bluetooth",
        },
        "NSFaceIDUsageDescription": {
            "patterns": [r"LAContext", r"biometryType.*\.faceID", r"evaluatePolicy"],
            "label": "Face ID",
        },
        "NSSpeechRecognitionUsageDescription": {
            "patterns": [r"SFSpeechRecognizer", r"Speech\.framework"],
            "label": "Speech Recognition",
        },
        "NSMotionUsageDescription": {
            "patterns": [r"CMMotionManager", r"CoreMotion"],
            "label": "Motion/Fitness",
        },
        "NSHealthShareUsageDescription": {
            "patterns": [r"HKHealthStore", r"HealthKit"],
            "label": "HealthKit",
        },
        "NSAppleMusicUsageDescription": {
            "patterns": [r"MPMediaLibrary", r"MusicKit"],
            "label": "Apple Music/Media Library",
        },
    }

    # Scan all source code
    all_source_content = ""
    for src in sources:
        all_source_content += read_file_safe(src) + "\n"

    # Check each plist
    for plist_path in plists:
        data = read_plist(plist_path)
        if data.get("_parse_error"):
            raw = data.get("_raw", "")
            for key, info in usage_descriptions.items():
                for pattern in info["patterns"]:
                    if re.search(pattern, all_source_content, re.IGNORECASE):
                        if key not in raw:
                            report.add(Finding(
                                check_id=f"MISSING_USAGE_DESC_{key}",
                                guideline="Guideline 5.1.1 - Data Collection and Storage",
                                severity=Severity.CRITICAL,
                                title=f"Missing {info['label']} Usage Description",
                                message=(
                                    f"Code uses {info['label']} APIs but Info.plist is missing {key}. "
                                    "Apple will crash the app on launch without this key."
                                ),
                                file_path=plist_path,
                                fix_instruction=f"Add '{key}' to Info.plist with a human-readable description of WHY your app needs {info['label']} access.",
                                auto_fixable=False,
                            ))
                        break
        else:
            for key, info in usage_descriptions.items():
                api_used = False
                for pattern in info["patterns"]:
                    if re.search(pattern, all_source_content, re.IGNORECASE):
                        api_used = True
                        break
                if api_used and key not in data:
                    report.add(Finding(
                        check_id=f"MISSING_USAGE_DESC_{key}",
                        guideline="Guideline 5.1.1 - Data Collection and Storage",
                        severity=Severity.CRITICAL,
                        title=f"Missing {info['label']} Usage Description",
                        message=(
                            f"Code uses {info['label']} APIs but Info.plist is missing '{key}'. "
                            "The app will crash on launch when requesting permission."
                        ),
                        file_path=plist_path,
                        fix_instruction=f"Add '{key}' to Info.plist with a user-facing explanation of why your app needs {info['label']} access.",
                        auto_fixable=False,
                    ))

            # Check for empty usage descriptions
            for key in data:
                if key.startswith("NS") and key.endswith("UsageDescription"):
                    val = data[key]
                    if isinstance(val, str) and len(val.strip()) < 10:
                        report.add(Finding(
                            check_id=f"SHORT_USAGE_DESC_{key}",
                            guideline="Guideline 5.1.1 - Data Collection and Storage",
                            severity=Severity.HIGH,
                            title=f"Usage Description Too Short: {key}",
                            message=(
                                f"'{key}' is '{val}'. Apple requires meaningful descriptions "
                                "explaining WHY the app needs this permission."
                            ),
                            file_path=plist_path,
                            fix_instruction=f"Replace with a clear sentence: e.g., 'This app uses your camera to scan documents.'",
                        ))


def check_minimum_functionality(root: str, report: ScreeningReport):
    """Check if the app is more than a webview wrapper (Guideline 4.2)."""
    report.total_checks += 1

    sources = scan_source_files(root)
    all_source = ""
    swift_file_count = 0
    for src in sources:
        content = read_file_safe(src)
        all_source += content + "\n"
        if src.endswith(".swift"):
            swift_file_count += 1

    # Detect webview-only patterns
    webview_patterns = [
        r"WKWebView", r"UIWebView", r"SFSafariViewController",
        r"WebView\b", r"webView\.load",
    ]
    native_patterns = [
        r"UITableView", r"UICollectionView", r"SwiftUI",
        r"NavigationView", r"TabView", r"List\s*\{",
        r"UINavigationController", r"UITabBarController",
        r"CoreData", r"Realm", r"UserNotifications",
        r"UNUserNotificationCenter", r"MapKit", r"MKMapView",
        r"AVFoundation", r"HealthKit", r"ARKit", r"CoreML",
        r"StoreKit", r"SKPaymentQueue", r"GameKit",
        r"UIViewController\b.*\bclass\b",
        r"struct\s+\w+\s*:\s*View\b",
    ]

    webview_count = sum(1 for p in webview_patterns if re.search(p, all_source))
    native_count = sum(1 for p in native_patterns if re.search(p, all_source))

    if webview_count > 0 and native_count < 3 and swift_file_count < 5:
        report.add(Finding(
            check_id="MINIMUM_FUNCTIONALITY",
            guideline="Guideline 4.2 - Minimum Functionality",
            severity=Severity.CRITICAL,
            title="App May Be a WebView Wrapper",
            message=(
                f"Detected {webview_count} webview pattern(s) but only {native_count} native "
                f"UI pattern(s) across {swift_file_count} Swift files. Apple rejects apps that "
                "are essentially repackaged websites without native integration."
            ),
            fix_instruction=(
                "To avoid 4.2 rejection, add native features:\n"
                "- Native navigation (tab bar, navigation controller)\n"
                "- Push notifications\n"
                "- Offline support / cached content\n"
                "- Native settings screen\n"
                "- At least 3 distinct screens with unique content\n"
                "- Integration with iOS features (widgets, Siri shortcuts, etc.)"
            ),
        ))


def check_minimum_screens(root: str, report: ScreeningReport):
    """Check that the app has at least 3 screens of unique content."""
    report.total_checks += 1

    sources = scan_source_files(root)
    storyboards = [s for s in find_files(root, "*.storyboard")
                   if "/pods/" not in s.lower() and "/build/" not in s.lower()]

    # Count view controllers / SwiftUI views
    vc_count = 0
    swiftui_view_count = 0

    for src in sources:
        if not src.endswith(".swift"):
            continue
        content = read_file_safe(src)
        # UIKit VCs
        vc_count += len(re.findall(r"class\s+\w+\s*:\s*(?:UI)?(?:View|Table|Collection|Navigation|Tab)Controller", content))
        # SwiftUI views
        swiftui_view_count += len(re.findall(r"struct\s+\w+\s*:\s*View\b", content))

    # Count storyboard scenes
    storyboard_scenes = 0
    for sb in storyboards:
        content = read_file_safe(sb)
        storyboard_scenes += len(re.findall(r"<scene\b", content))

    total_screens = max(vc_count + swiftui_view_count, storyboard_scenes)

    if total_screens < 3:
        report.add(Finding(
            check_id="MINIMUM_SCREENS",
            guideline="Guideline 4.2 - Minimum Functionality",
            severity=Severity.HIGH,
            title=f"Only {total_screens} Screen(s) Detected",
            message=(
                f"Found {vc_count} UIKit VCs, {swiftui_view_count} SwiftUI views, "
                f"{storyboard_scenes} storyboard scenes. Apple generally expects apps to have "
                "at least 3 distinct screens with meaningful content."
            ),
            fix_instruction=(
                "Add more screens to demonstrate app value:\n"
                "- Settings/Preferences screen\n"
                "- About/Help screen\n"
                "- Onboarding flow (2-3 screens)\n"
                "- Content detail views"
            ),
        ))


def check_subscription_compliance(root: str, report: ScreeningReport):
    """Check subscription/IAP compliance (restore, terms, etc.)."""
    report.total_checks += 1

    sources = scan_source_files(root)
    all_source = ""
    for src in sources:
        all_source += read_file_safe(src) + "\n"

    has_iap = bool(re.search(r"StoreKit|SKPayment|SKProduct|Product\.products|purchase\(|\.purchase\b", all_source))
    has_subscription = bool(re.search(
        r"subscription|auto.?renew|recurring|SKPaymentQueue|Product\.SubscriptionInfo",
        all_source, re.IGNORECASE
    ))

    if not has_iap and not has_subscription:
        return  # No IAP, skip

    # Check for restore purchases
    has_restore = bool(re.search(
        r"restoreCompletedTransactions|AppStore\.sync|restore.*purchase|Transaction\.currentEntitlements",
        all_source, re.IGNORECASE
    ))

    if not has_restore:
        report.add(Finding(
            check_id="SUBSCRIPTION_RESTORE",
            guideline="Guideline 3.1.1 - In-App Purchase (Restore)",
            severity=Severity.CRITICAL,
            title="No Restore Purchases Mechanism",
            message=(
                "App uses in-app purchases/subscriptions but no restore mechanism detected. "
                "Apple REQUIRES a 'Restore Purchases' button for all apps with non-consumable "
                "IAPs or subscriptions."
            ),
            fix_instruction=(
                "Add a 'Restore Purchases' button that calls:\n"
                "  - StoreKit 1: SKPaymentQueue.default().restoreCompletedTransactions()\n"
                "  - StoreKit 2: for await result in Transaction.currentEntitlements { ... }\n"
                "  - Or: try await AppStore.sync()\n"
                "Place the button in Settings or on the paywall/purchase screen."
            ),
        ))

    if has_subscription:
        # Check for terms of service / EULA
        has_terms = bool(re.search(
            r"terms.?of.?(?:service|use)|eula|end.?user.?license|subscription.?terms",
            all_source, re.IGNORECASE
        ))
        if not has_terms:
            report.add(Finding(
                check_id="SUBSCRIPTION_TERMS",
                guideline="Guideline 3.1.2 - Subscriptions (Terms)",
                severity=Severity.HIGH,
                title="Missing Subscription Terms / EULA",
                message=(
                    "App appears to offer subscriptions but no Terms of Service or EULA "
                    "reference found. Apple requires that subscription apps clearly display "
                    "terms, pricing, and renewal information."
                ),
                fix_instruction=(
                    "On your paywall/purchase screen, include:\n"
                    "- Link to Terms of Service\n"
                    "- Link to Privacy Policy\n"
                    "- Subscription price and period (e.g., '$4.99/month')\n"
                    "- Auto-renewal disclosure\n"
                    "- How to cancel"
                ),
            ))

        # Check for price display
        has_price_display = bool(re.search(
            r"displayPrice|localizedPrice|priceFormatted|\.price\b.*display",
            all_source, re.IGNORECASE
        ))
        if not has_price_display:
            report.add(Finding(
                check_id="SUBSCRIPTION_PRICE_DISPLAY",
                guideline="Guideline 3.1.2 - Subscriptions (Price)",
                severity=Severity.MEDIUM,
                title="Subscription Price May Not Be Displayed",
                message="Could not detect dynamic price display from StoreKit. Ensure prices are fetched from StoreKit, not hardcoded.",
                fix_instruction="Use Product.displayPrice from StoreKit 2 (or SKProduct.localizedPrice) to show prices.",
            ))


def check_hardcoded_test_data(root: str, report: ScreeningReport):
    """Check for hardcoded test/debug data that should not ship."""
    report.total_checks += 1

    sources = scan_source_files(root)
    issues = []

    test_patterns = [
        (r"#if\s+DEBUG[\s\S]*?#endif", None),  # Skip DEBUG blocks (acceptable)
        (r'(?:let|var)\s+\w*(?:test|mock|fake|dummy)\w*\s*[:=]', "Test/mock variable"),
        (r'(?:baseURL|apiURL|endpoint)\s*=\s*["\']https?://(?:localhost|127\.0\.0\.1|staging|dev\.)', "Non-production URL"),
        (r'(?:password|secret|token|apikey)\s*[:=]\s*["\'][a-zA-Z0-9]{8,}["\']', "Hardcoded credential"),
        (r'print\s*\(', None),  # Too many false positives
        (r'NSLog\s*\(', "NSLog statement (remove for production)"),
        (r'debugPrint\s*\(', "debugPrint statement"),
    ]

    for src in sources:
        content = read_file_safe(src)
        for pattern, desc in test_patterns:
            if desc is None:
                continue
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            for m in matches:
                line = content[:m.start()].count("\n") + 1
                # Skip if inside a DEBUG block
                preceding = content[:m.start()]
                debug_opens = len(re.findall(r"#if\s+DEBUG", preceding))
                debug_closes = len(re.findall(r"#endif", preceding))
                if debug_opens > debug_closes:
                    continue
                issues.append((src, desc, line))

    if issues:
        details = "\n".join(
            f"  - {os.path.basename(f)}:{line} - {desc}"
            for f, desc, line in issues[:10]
        )
        report.add(Finding(
            check_id="HARDCODED_TEST_DATA",
            guideline="Guideline 2.1 - App Completeness",
            severity=Severity.HIGH,
            title="Hardcoded Test/Debug Data Detected",
            message=f"Found {len(issues)} instance(s) of test data outside #if DEBUG blocks:\n{details}",
            fix_instruction=(
                "1. Wrap debug-only code in #if DEBUG / #endif\n"
                "2. Use environment variables or config files for URLs\n"
                "3. Remove hardcoded credentials (use Keychain or server-side)\n"
                "4. Remove NSLog/debugPrint or wrap in #if DEBUG"
            ),
        ))


def check_screenshots(root: str, report: ScreeningReport):
    """Check for required App Store screenshots."""
    report.total_checks += 1

    screenshot_dirs = (
        find_files(root, "screenshots") +
        find_files(root, "Screenshots") +
        find_files(root, "AppStoreScreenshots") +
        find_files(root, "Fastlane") +
        find_files(root, "fastlane")
    )

    # Required screenshot sizes (points)
    required_sizes = {
        "6.7 inch (iPhone 15 Pro Max)": "1290x2796",
        "6.5 inch (iPhone 15 Plus)": "1284x2778",
        "5.5 inch (iPhone 8 Plus)": "1242x2208",
        "12.9 inch iPad Pro": "2048x2732",
    }

    screenshot_dir_found = False
    for d in screenshot_dirs:
        if os.path.isdir(d):
            screenshot_dir_found = True
            break

    # Also check fastlane/screenshots
    fastlane_screenshots = find_files(root, "Snapfile")
    if fastlane_screenshots:
        screenshot_dir_found = True

    if not screenshot_dir_found:
        report.add(Finding(
            check_id="SCREENSHOTS_MISSING",
            guideline="App Store Connect Requirements",
            severity=Severity.MEDIUM,
            title="No Screenshots Directory Found",
            message=(
                "Could not find a screenshots directory in the project. "
                "App Store Connect requires screenshots for at least these sizes:\n"
                + "\n".join(f"  - {name}: {size}" for name, size in required_sizes.items())
            ),
            fix_instruction=(
                "1. Create screenshots for each required device size\n"
                "2. Minimum 1, maximum 10 screenshots per size\n"
                "3. Consider using fastlane snapshot for automated screenshots\n"
                "4. Store in a 'screenshots/' directory or configure in fastlane"
            ),
        ))


def check_bundle_identifier(root: str, report: ScreeningReport):
    """Check bundle identifier format."""
    report.total_checks += 1

    plists = find_plist_files(root)
    for plist_path in plists:
        data = read_plist(plist_path)
        if data.get("_parse_error"):
            continue
        bundle_id = data.get("CFBundleIdentifier", "")
        if bundle_id and not bundle_id.startswith("$("):
            if not re.match(r"^[a-zA-Z][a-zA-Z0-9\-\.]*\.[a-zA-Z][a-zA-Z0-9\-\.]*$", bundle_id):
                report.add(Finding(
                    check_id="BUNDLE_ID_FORMAT",
                    guideline="Guideline 2.1 - App Completeness",
                    severity=Severity.HIGH,
                    title="Invalid Bundle Identifier Format",
                    message=f"Bundle identifier '{bundle_id}' may not be in reverse-domain format (e.g., com.company.appname).",
                    file_path=plist_path,
                    fix_instruction="Use reverse-domain notation: com.yourcompany.yourappname",
                ))

            if "example" in bundle_id.lower() or "test" in bundle_id.lower():
                report.add(Finding(
                    check_id="BUNDLE_ID_TEST",
                    guideline="Guideline 2.1 - App Completeness",
                    severity=Severity.HIGH,
                    title="Bundle Identifier Contains Test/Example",
                    message=f"Bundle identifier '{bundle_id}' contains 'test' or 'example'.",
                    file_path=plist_path,
                    fix_instruction="Change to your actual bundle identifier before submission.",
                ))


def check_spam_indicators(root: str, report: ScreeningReport):
    """Check for Guideline 4.3 spam indicators."""
    report.total_checks += 1

    plists = find_plist_files(root)
    sources = scan_source_files(root)

    # Check for template app indicators
    template_indicators = []
    all_source = ""
    for src in sources:
        all_source += read_file_safe(src)

    # Common template frameworks / boilerplate markers
    template_patterns = [
        (r"Created with Starter Template", "Template marker in source"),
        (r"Starter Kit.*Template", "Starter kit template reference"),
        (r"white.?label", "White-label reference"),
        (r"reskin", "Reskin reference"),
        (r"app.?clone", "App clone reference"),
    ]

    for pattern, desc in template_patterns:
        if re.search(pattern, all_source, re.IGNORECASE):
            template_indicators.append(desc)

    if template_indicators:
        report.add(Finding(
            check_id="SPAM_TEMPLATE_MARKERS",
            guideline="Guideline 4.3 - Spam",
            severity=Severity.HIGH,
            title="Template / Clone App Indicators Found",
            message=(
                f"Found {len(template_indicators)} template/clone indicator(s):\n"
                + "\n".join(f"  - {t}" for t in template_indicators) +
                "\n\nApple's November 2025 update specifically targets clone apps (4.1(c)). "
                "Submitting template apps or white-label clones is a top rejection trigger."
            ),
            fix_instruction=(
                "1. Remove ALL template/boilerplate markers from source code\n"
                "2. Ensure unique branding (icon, name, design language)\n"
                "3. Add substantial unique functionality beyond the template\n"
                "4. If you have similar apps, consider merging into one with in-app purchase variations\n"
                "5. Do NOT use another developer's icon, brand, or product name (Guideline 4.1(c))"
            ),
        ))


def check_age_rating(root: str, report: ScreeningReport):
    """Check age rating questionnaire requirements (updated Jan 2026)."""
    report.total_checks += 1

    # This is mostly an App Store Connect check, but we can flag source-level issues
    sources = scan_source_files(root)
    all_source = ""
    for src in sources:
        all_source += read_file_safe(src) + "\n"

    concerns = []
    if re.search(r"alcohol|beer|wine|liquor|spirits", all_source, re.IGNORECASE):
        concerns.append("Alcohol references detected - ensure age rating reflects this")
    if re.search(r"gambling|casino|slot|betting|wager", all_source, re.IGNORECASE):
        concerns.append("Gambling references detected - requires 17+ age rating")
    if re.search(r"violence|blood|gore|weapon|kill|shoot", all_source, re.IGNORECASE):
        concerns.append("Violence references detected - adjust age rating accordingly")
    if re.search(r"UserGeneratedContent|UGC|user.?generated", all_source, re.IGNORECASE):
        concerns.append(
            "User-generated content detected - must provide content reporting mechanism "
            "and age restriction based on verified/declared age (Nov 2025 update)"
        )

    if concerns:
        report.add(Finding(
            check_id="AGE_RATING_CONTENT",
            guideline="Guideline 1.1 - Age Ratings (Updated Jan 2026)",
            severity=Severity.MEDIUM,
            title="Age Rating Review Needed",
            message=(
                "Content flags that may affect your age rating:\n"
                + "\n".join(f"  - {c}" for c in concerns) +
                "\n\nAs of January 31, 2026, a NEW age rating questionnaire is required. "
                "New age brackets: 13+, 16+, 18+ (added July 2025)."
            ),
            fix_instruction=(
                "1. Complete the new age rating questionnaire in App Store Connect\n"
                "2. Be honest about content - misrepresentation causes rejection\n"
                "3. For UGC apps: add content reporting + age verification mechanisms\n"
                "4. New categories: 13+, 16+, 18+ available since July 2025"
            ),
        ))


def check_ai_data_sharing(root: str, report: ScreeningReport):
    """Check for AI data sharing compliance (Guideline 5.1.2(i), Nov 2025)."""
    report.total_checks += 1

    sources = scan_source_files(root)
    all_source = ""
    for src in sources:
        all_source += read_file_safe(src) + "\n"

    ai_patterns = [
        r"openai\.com", r"api\.anthropic", r"generativelanguage\.googleapis",
        r"ChatGPT", r"GPT-?4", r"Claude", r"Gemini",
        r"huggingface", r"replicate\.com", r"together\.ai",
        r"stability\.ai", r"midjourney",
    ]

    ai_services_found = []
    for pattern in ai_patterns:
        if re.search(pattern, all_source, re.IGNORECASE):
            ai_services_found.append(pattern.replace("\\", ""))

    if ai_services_found:
        # Check for consent mechanism
        has_consent = bool(re.search(
            r"consent|permission|opt.?in|agree|accept|disclosure|modal.*ai|ai.*modal",
            all_source, re.IGNORECASE
        ))
        if not has_consent:
            report.add(Finding(
                check_id="AI_DATA_SHARING_CONSENT",
                guideline="Guideline 5.1.2(i) - Third-Party AI Data Sharing (Nov 2025)",
                severity=Severity.CRITICAL,
                title="Missing AI Data Sharing Consent",
                message=(
                    f"App appears to use third-party AI services ({', '.join(ai_services_found[:5])}) "
                    "but no consent mechanism detected. As of November 2025, Apple requires:\n"
                    "  1. A consent modal BEFORE sharing personal data with third-party AI\n"
                    "  2. Modal must specify the AI provider name\n"
                    "  3. Modal must list data types being shared\n"
                    "  4. User must explicitly opt in"
                ),
                fix_instruction=(
                    "1. Add a consent dialog before any AI API call that sends user data\n"
                    "2. Specify: 'Your data will be sent to [Provider Name]'\n"
                    "3. List data types: 'Including: text input, photos, etc.'\n"
                    "4. Provide Accept/Decline buttons\n"
                    "5. Store consent state and allow withdrawal\n"
                    "6. Update privacy policy to cover third-party AI data sharing"
                ),
            ))


def check_external_payment_compliance(root: str, report: ScreeningReport):
    """Check external payment link compliance (EU DMA / US changes)."""
    report.total_checks += 1

    sources = scan_source_files(root)
    all_source = ""
    for src in sources:
        all_source += read_file_safe(src) + "\n"

    external_payment_patterns = [
        r"ExternalPurchaseLink", r"StoreKitExternalPurchase",
        r"external.*payment", r"external.*purchase",
        r"stripe\.com", r"paypal\.com", r"checkout\.stripe",
    ]

    has_external = any(re.search(p, all_source, re.IGNORECASE) for p in external_payment_patterns)

    if has_external:
        has_entitlement = bool(re.search(
            r"StoreKit External Purchase Link|com\.apple\.developer\.storekit\.external-purchase-link",
            all_source, re.IGNORECASE
        ))
        entitlement_files = find_files(root, "*.entitlements")
        for ef in entitlement_files:
            content = read_file_safe(ef)
            if "external-purchase" in content.lower():
                has_entitlement = True

        if not has_entitlement:
            report.add(Finding(
                check_id="EXTERNAL_PAYMENT_ENTITLEMENT",
                guideline="External Payment Links (EU DMA / US Storefront)",
                severity=Severity.HIGH,
                title="External Payment Without Required Entitlement",
                message=(
                    "App references external payment/purchase mechanisms but the "
                    "StoreKit External Purchase Link entitlement was not detected. "
                    "As of 2025, US apps can link to external payments without the entitlement, "
                    "but EU apps must use StoreKit External Purchase Link APIs with Apple's "
                    "disclosure sheet."
                ),
                fix_instruction=(
                    "For US storefront:\n"
                    "  - External links are now allowed without entitlement (April 2025 ruling)\n"
                    "  - Still cannot use anti-steering language\n"
                    "For EU storefront:\n"
                    "  - Must use StoreKit External Purchase Link Entitlement\n"
                    "  - Must display Apple's system disclosure sheet\n"
                    "  - Subject to initial acquisition fee (2%) and store services fee\n"
                    "  - Apply at developer.apple.com"
                ),
            ))


def check_version_and_build(root: str, report: ScreeningReport):
    """Check version and build number are set."""
    report.total_checks += 1

    plists = find_plist_files(root)
    for plist_path in plists:
        data = read_plist(plist_path)
        if data.get("_parse_error"):
            continue

        version = data.get("CFBundleShortVersionString", "")
        build = data.get("CFBundleVersion", "")

        if not version or version == "$(MARKETING_VERSION)":
            pass  # Xcode handles this
        elif not re.match(r"^\d+\.\d+(\.\d+)?$", version):
            report.add(Finding(
                check_id="VERSION_FORMAT",
                guideline="Guideline 2.1 - App Completeness",
                severity=Severity.MEDIUM,
                title=f"Version Format Issue: '{version}'",
                message="Version should be in X.Y or X.Y.Z format.",
                file_path=plist_path,
                fix_instruction="Set CFBundleShortVersionString to format like '1.0.0'.",
            ))


def check_transport_security(root: str, report: ScreeningReport):
    """Check App Transport Security settings."""
    report.total_checks += 1

    plists = find_plist_files(root)
    for plist_path in plists:
        data = read_plist(plist_path)
        if data.get("_parse_error"):
            raw = data.get("_raw", "")
            if "NSAllowsArbitraryLoads" in raw and "true" in raw.lower():
                report.add(Finding(
                    check_id="ATS_DISABLED",
                    guideline="Guideline 2.1 - Performance / Security",
                    severity=Severity.HIGH,
                    title="App Transport Security Disabled",
                    message="NSAllowsArbitraryLoads is true. Apple may reject apps that disable ATS without justification.",
                    file_path=plist_path,
                    fix_instruction=(
                        "1. Use HTTPS for all network requests\n"
                        "2. If you must allow HTTP for specific domains, use NSExceptionDomains instead\n"
                        "3. You may need to provide justification during review"
                    ),
                ))
        else:
            ats = data.get("NSAppTransportSecurity", {})
            if isinstance(ats, dict) and ats.get("NSAllowsArbitraryLoads"):
                report.add(Finding(
                    check_id="ATS_DISABLED",
                    guideline="Guideline 2.1 - Performance / Security",
                    severity=Severity.HIGH,
                    title="App Transport Security Disabled",
                    message="NSAllowsArbitraryLoads is true in Info.plist. Apple may reject without justification.",
                    file_path=plist_path,
                    fix_instruction=(
                        "1. Use HTTPS for all connections\n"
                        "2. Use NSExceptionDomains for specific HTTP-only servers\n"
                        "3. Provide justification in App Review notes if ATS exception is truly needed"
                    ),
                ))


def check_sdk_and_deployment_target(root: str, report: ScreeningReport):
    """Check for outdated deployment targets / SDK requirements."""
    report.total_checks += 1

    # Check project.pbxproj for deployment target
    pbxprojs = find_files(root, "project.pbxproj")
    pbxprojs = [p for p in pbxprojs if "/pods/" not in p.lower()]

    for pbx in pbxprojs:
        content = read_file_safe(pbx)
        targets = re.findall(r"IPHONEOS_DEPLOYMENT_TARGET\s*=\s*(\d+\.?\d*)", content)
        for target in targets:
            try:
                version = float(target)
                if version < 16.0:
                    report.add(Finding(
                        check_id="DEPLOYMENT_TARGET_OLD",
                        guideline="Technical Requirements (2026)",
                        severity=Severity.MEDIUM,
                        title=f"Low Deployment Target: iOS {target}",
                        message=(
                            f"Deployment target is iOS {target}. While not rejected for this alone, "
                            "Apple recommends supporting recent iOS versions. Starting April 28, 2026, "
                            "apps must be built with iOS 26 SDK."
                        ),
                        file_path=pbx,
                        fix_instruction="Consider raising minimum deployment target to iOS 16.0 or later.",
                    ))
                    break
            except ValueError:
                pass


# ---------------------------------------------------------------------------
# AUTO-FIX FUNCTIONS
# ---------------------------------------------------------------------------

def fix_create_privacy_manifest(root: str) -> str:
    """Create a basic PrivacyInfo.xcprivacy template."""
    manifest_content = {
        "NSPrivacyTracking": False,
        "NSPrivacyTrackingDomains": [],
        "NSPrivacyCollectedDataTypes": [],
        "NSPrivacyAccessedAPITypes": [
            {
                "NSPrivacyAccessedAPIType": "NSPrivacyAccessedAPICategoryUserDefaults",
                "NSPrivacyAccessedAPITypeReasons": ["CA92.1"],
            }
        ],
    }

    # Find the most likely target directory
    xcodeprojs = find_files(root, "*.xcodeproj")
    if xcodeprojs:
        target_dir = os.path.dirname(xcodeprojs[0])
    else:
        # Look for an existing Info.plist to place near it
        plists = find_plist_files(root)
        if plists:
            target_dir = os.path.dirname(plists[0])
        else:
            target_dir = root

    # Validate safe path
    target_path = safe_path(os.path.join(target_dir, "PrivacyInfo.xcprivacy"))

    with open(target_path, "wb") as f:
        plistlib.dump(manifest_content, f)

    return f"Created PrivacyInfo.xcprivacy at {target_path}"


def apply_fixes(root: str, report: ScreeningReport) -> list:
    """Apply auto-fixes for findings that support it."""
    fixes_applied = []

    for finding in report.findings:
        if not finding.auto_fixable or finding.fixed:
            continue

        try:
            if finding.check_id == "PRIVACY_MANIFEST":
                msg = fix_create_privacy_manifest(root)
                finding.fixed = True
                fixes_applied.append(msg)
        except Exception as e:
            fixes_applied.append(f"FAILED to fix {finding.check_id}: {e}")

    return fixes_applied


# ---------------------------------------------------------------------------
# REPORT GENERATION
# ---------------------------------------------------------------------------

def print_report(report: ScreeningReport, verbose: bool = True):
    """Print a formatted report to stdout."""
    # Header
    print("\n" + "=" * 72)
    print("  iOS APP STORE REJECTION SCREENER - REPORT")
    print("=" * 72)
    print(f"  App Path:  {report.app_path}")
    print(f"  Timestamp: {report.timestamp}")
    print(f"  Checks:    {report.total_checks}")
    print(f"  Findings:  {len(report.findings)}")
    print("=" * 72)

    # Tally by severity
    severity_counts = {}
    for f in report.findings:
        severity_counts[f.severity] = severity_counts.get(f.severity, 0) + 1

    print("\n  SEVERITY SUMMARY:")
    for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]:
        count = severity_counts.get(sev, 0)
        marker = "XX" if sev == Severity.CRITICAL and count > 0 else \
                 "!!" if sev == Severity.HIGH and count > 0 else \
                 "--"
        print(f"    [{marker}] {sev.value:10s}: {count}")

    # Overall verdict
    print("\n  " + "-" * 68)
    if report.passed:
        print("  VERDICT: PASS - No critical/high issues found.")
        print("  (Review MEDIUM/LOW findings before submission for best results.)")
    else:
        crit = severity_counts.get(Severity.CRITICAL, 0)
        high = severity_counts.get(Severity.HIGH, 0)
        print(f"  VERDICT: FAIL - {crit} critical, {high} high severity issue(s) found.")
        print("  FIX THESE BEFORE SUBMITTING or your app WILL be rejected.")
    print("  " + "-" * 68)

    # Detailed findings
    if verbose and report.findings:
        print("\n  DETAILED FINDINGS:")
        print("  " + "-" * 68)
        for i, f in enumerate(report.findings, 1):
            status = "[FIXED]" if f.fixed else f"[{f.severity.value}]"
            print(f"\n  {i}. {status} {f.title}")
            print(f"     Guideline: {f.guideline}")
            print(f"     Check ID:  {f.check_id}")
            if f.file_path:
                print(f"     File:      {f.file_path}")
            # Word-wrap message
            for line in f.message.split("\n"):
                print(f"     {line}")
            if f.fix_instruction:
                print(f"     FIX:")
                for line in f.fix_instruction.split("\n"):
                    print(f"       {line}")

    # Apple guidelines reference
    print("\n  " + "=" * 68)
    print("  REFERENCE: Key Apple Guidelines (2025-2026)")
    print("  " + "-" * 68)
    print("  - Review Guidelines: https://developer.apple.com/app-store/review/guidelines/")
    print("  - Privacy Manifests:  https://developer.apple.com/documentation/bundleresources/privacy-manifest-files")
    print("  - Age Rating Changes: New questionnaire required Jan 31, 2026")
    print("  - SDK Requirement:    iOS 26 SDK required from April 28, 2026")
    print("  - AI Data Sharing:    Guideline 5.1.2(i) - consent modal required (Nov 2025)")
    print("  - Clone App Rules:    Guideline 4.1(c) updated Nov 2025")
    print("  - EU DMA / US:        External payment links now allowed (US) / regulated (EU)")
    print("  " + "=" * 68 + "\n")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def run_all_checks(root: str) -> ScreeningReport:
    """Run all screening checks against the app directory."""
    report = ScreeningReport(app_path=root)

    checks = [
        check_privacy_policy,
        check_privacy_manifest,
        check_app_icon,
        check_placeholder_content,
        check_info_plist_keys,
        check_minimum_functionality,
        check_minimum_screens,
        check_subscription_compliance,
        check_hardcoded_test_data,
        check_screenshots,
        check_bundle_identifier,
        check_spam_indicators,
        check_age_rating,
        check_ai_data_sharing,
        check_external_payment_compliance,
        check_version_and_build,
        check_transport_security,
        check_sdk_and_deployment_target,
    ]

    for check_fn in checks:
        try:
            check_fn(root, report)
        except Exception as e:
            report.add(Finding(
                check_id=f"CHECK_ERROR_{check_fn.__name__}",
                guideline="Internal",
                severity=Severity.INFO,
                title=f"Check '{check_fn.__name__}' encountered an error",
                message=str(e),
            ))

    # Summary
    report.summary = {
        "total_checks": report.total_checks,
        "total_findings": len(report.findings),
        "critical": sum(1 for f in report.findings if f.severity == Severity.CRITICAL),
        "high": sum(1 for f in report.findings if f.severity == Severity.HIGH),
        "medium": sum(1 for f in report.findings if f.severity == Severity.MEDIUM),
        "low": sum(1 for f in report.findings if f.severity == Severity.LOW),
        "info": sum(1 for f in report.findings if f.severity == Severity.INFO),
        "passed": report.passed,
        "auto_fixable": sum(1 for f in report.findings if f.auto_fixable),
    }

    return report


def main():
    parser = argparse.ArgumentParser(
        description="iOS App Store Rejection Screener - Checks for common rejection patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 ios_rejection_screener.py --check /path/to/MyApp\n"
            "  python3 ios_rejection_screener.py --fix /path/to/MyApp\n"
            "  python3 ios_rejection_screener.py --report /path/to/MyApp --output report.json\n"
        ),
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", metavar="PATH", help="Check app directory for rejection issues")
    group.add_argument("--fix", metavar="PATH", help="Auto-fix what can be fixed, then report")
    group.add_argument("--report", metavar="PATH", help="Generate full report (same as --check with --output)")

    parser.add_argument("--output", metavar="FILE", help="Save JSON report to file (must be within project)")
    parser.add_argument("--quiet", action="store_true", help="Only show PASS/FAIL and critical issues")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of formatted text")

    args = parser.parse_args()

    # Determine the app path
    app_path = args.check or args.fix or args.report

    # Validate paths
    try:
        app_path = safe_path(app_path)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(app_path):
        print(f"ERROR: '{app_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Run checks
    report = run_all_checks(app_path)

    # Apply fixes if requested
    if args.fix:
        fixes = apply_fixes(app_path, report)
        if fixes:
            print("\nAUTO-FIXES APPLIED:")
            for fix_msg in fixes:
                print(f"  + {fix_msg}")
            # Re-run checks after fixes
            report = run_all_checks(app_path)

    # Output
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, default=str))
    else:
        print_report(report, verbose=not args.quiet)

    # Save JSON report if requested
    if args.output:
        try:
            output_path = safe_path(args.output)
            with open(output_path, "w") as f:
                json.dump(report.to_dict(), f, indent=2, default=str)
            print(f"\nJSON report saved to: {output_path}")
        except ValueError as e:
            print(f"ERROR: Cannot save report: {e}", file=sys.stderr)

    # Exit code
    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
