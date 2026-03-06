#!/usr/bin/env python3
"""
iOS Release Pipeline - Automated PWA-to-App-Store submission
Wraps PWAs with Capacitor, generates metadata, builds, validates, uploads.

Usage:
    python3 AUTOMATIONS/ios_release_pipeline.py --app focuslock --all-steps
    python3 AUTOMATIONS/ios_release_pipeline.py --all --wrap-only
    python3 AUTOMATIONS/ios_release_pipeline.py --app sleepmaxx --validate-only
    python3 AUTOMATIONS/ios_release_pipeline.py --app mealmaxx --metadata-only
    python3 AUTOMATIONS/ios_release_pipeline.py --status
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "ralph" / "loops" / "app_factory" / "output"
BUILDS_DIR = PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY" / "builds"
PIPELINE_LOG = BUILDS_DIR / "pipeline_log.json"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT.resolve())):
        raise ValueError(f"BLOCKED: {resolved} is outside project root")
    return resolved


# ---------------------------------------------------------------------------
# App registry - single source of truth matching wrap_and_submit_all.sh
# ---------------------------------------------------------------------------
APP_REGISTRY = {
    "focuslock": {
        "dir": "focuslock-web",
        "display_name": "FocusLock",
        "bundle_id": "com.printmaxx.focuslock",
        "primary_category": "Productivity",
        "secondary_category": "Education",
        "subtitle": "Block Distractions, Build Focus",
        "description": (
            "FocusLock helps you stay focused by blocking distracting apps "
            "and websites during work sessions. Set a timer, lock your phone, "
            "and get real work done. Pomodoro mode, focus stats, ambient sounds, "
            "and streak tracking keep you on track every day.\n\n"
            "Features:\n"
            "- App and website blocking during focus sessions\n"
            "- Pomodoro timer with auto-cycling\n"
            "- Ambient sound mixer (rain, cafe, white noise)\n"
            "- Daily and weekly focus statistics\n"
            "- Streak tracking with visual heatmap\n"
            "- Haptic feedback on session milestones\n"
            "- Dark mode support\n"
            "- Native notifications for session reminders"
        ),
        "keywords": "focus,timer,pomodoro,block,distraction,productivity,study,work,screen,time",
        "promotional_text": "Stay focused. Block distractions. Build streaks.",
        "age_rating": "4+",
    },
    "habitforge": {
        "dir": "habitforge-web",
        "display_name": "HabitForge",
        "bundle_id": "com.printmaxx.habitforge",
        "primary_category": "Health & Fitness",
        "secondary_category": "Productivity",
        "subtitle": "Build Habits That Actually Stick",
        "description": (
            "HabitForge makes building daily habits simple and visual. "
            "Track your streaks with a GitHub-style heatmap, set custom "
            "reminders, and build consistency one day at a time.\n\n"
            "Features:\n"
            "- Unlimited habit tracking\n"
            "- GitHub-style heatmap visualization\n"
            "- Streak tracking with personal records\n"
            "- Custom reminder schedules per habit\n"
            "- Detailed statistics and progress charts\n"
            "- Haptic feedback on completions\n"
            "- Dark mode support\n"
            "- Data export to CSV"
        ),
        "keywords": "habit,tracker,streak,routine,daily,goals,heatmap,discipline,morning,consistency",
        "promotional_text": "Track habits. Build streaks. See your progress.",
        "age_rating": "4+",
    },
    "mealmaxx": {
        "dir": "mealmaxx-web",
        "display_name": "MealMaxx",
        "bundle_id": "com.printmaxx.mealmaxx",
        "primary_category": "Food & Drink",
        "secondary_category": "Health & Fitness",
        "subtitle": "Meal Prep Made Dead Simple",
        "description": (
            "MealMaxx takes the guesswork out of meal planning. "
            "Pick your goals, get weekly meal plans, auto-generate grocery "
            "lists, and track your macros without logging every bite.\n\n"
            "Features:\n"
            "- Weekly meal plan generator\n"
            "- Auto grocery list from meal plans\n"
            "- Macro and calorie tracking\n"
            "- Recipe library with prep time estimates\n"
            "- Dietary preference filters (keto, vegan, halal, etc.)\n"
            "- Shopping list sharing\n"
            "- Dark mode support\n"
            "- Offline access to saved plans"
        ),
        "keywords": "meal,prep,plan,grocery,list,macros,calories,recipe,diet,nutrition",
        "promotional_text": "Plan meals. Auto grocery lists. Hit your macros.",
        "age_rating": "4+",
    },
    "hilal": {
        "dir": "ramadan-tracker",
        "display_name": "Hilal",
        "bundle_id": "com.printmaxx.hilal",
        "primary_category": "Lifestyle",
        "secondary_category": "Health & Fitness",
        "subtitle": "Ramadan Tracker and Prayer Times",
        "description": (
            "Hilal is your companion for Ramadan and beyond. Accurate prayer "
            "times, fasting tracker, Quran reading progress, and daily duas "
            "keep you connected throughout the holy month.\n\n"
            "Features:\n"
            "- Accurate prayer times based on location\n"
            "- Suhoor and Iftar countdown timers\n"
            "- Fasting day tracker with streak\n"
            "- Quran reading progress tracker\n"
            "- Daily dua reminders\n"
            "- Qibla compass\n"
            "- Dark mode support\n"
            "- Notification reminders for prayer and fasting"
        ),
        "keywords": "ramadan,prayer,times,fasting,islam,quran,dua,iftar,suhoor,muslim",
        "promotional_text": "Prayer times. Fasting tracker. Ramadan companion.",
        "age_rating": "4+",
    },
    "sleepmaxx": {
        "dir": "sleepmaxx-web",
        "display_name": "SleepMaxx",
        "bundle_id": "com.printmaxx.sleepmaxx",
        "primary_category": "Health & Fitness",
        "secondary_category": "Lifestyle",
        "subtitle": "Better Sleep Starts Tonight",
        "description": (
            "SleepMaxx helps you build a better sleep routine by tracking "
            "your sleep inputs, not just outputs. Log caffeine timing, "
            "screen time, room temperature, and evening habits to find "
            "what actually improves your sleep.\n\n"
            "Features:\n"
            "- Sleep input tracking (caffeine, screens, exercise, meals)\n"
            "- Sleep quality scoring based on your habits\n"
            "- Bedtime and wake time reminders\n"
            "- Sleep sounds (rain, white noise, brown noise)\n"
            "- Weekly sleep reports with insights\n"
            "- Haptic alarm option\n"
            "- Dark mode with true black OLED support\n"
            "- Data export for health tracking"
        ),
        "keywords": "sleep,tracker,insomnia,bedtime,routine,sounds,alarm,rest,night,quality",
        "promotional_text": "Track what matters. Sleep better tonight.",
        "age_rating": "4+",
    },
    "walktounlock": {
        "dir": "walktounlock-web",
        "display_name": "WalkToUnlock",
        "bundle_id": "com.printmaxx.walktounlock",
        "primary_category": "Health & Fitness",
        "secondary_category": "Lifestyle",
        "subtitle": "Walk More. Earn Rewards.",
        "description": (
            "WalkToUnlock motivates you to walk more by locking premium "
            "content behind step goals. Hit your daily steps to unlock "
            "rewards, build streaks, and compete with friends.\n\n"
            "Features:\n"
            "- Step-gated reward system\n"
            "- Daily step goal tracking\n"
            "- Walking streak tracker\n"
            "- Route history and distance maps\n"
            "- Weekly and monthly walking stats\n"
            "- Haptic celebrations on goal completion\n"
            "- Dark mode support\n"
            "- Push notifications for daily motivation"
        ),
        "keywords": "walk,steps,pedometer,fitness,walking,health,exercise,motivation,streak,rewards",
        "promotional_text": "Walk to unlock rewards. Build your streak.",
        "age_rating": "4+",
    },
}

# ---------------------------------------------------------------------------
# Screenshot size specs - all required device sizes for App Store Connect
# ---------------------------------------------------------------------------
SCREENSHOT_SPECS = {
    "iPhone_6.9": {
        "label": "iPhone 16 Pro Max (6.9-inch)",
        "size": (1320, 2868),
        "required": True,
        "devices": ["iPhone 16 Pro Max"],
    },
    "iPhone_6.7": {
        "label": "iPhone 16 Plus / 15 Plus / 14 Pro Max (6.7-inch)",
        "size": (1290, 2796),
        "required": True,
        "devices": ["iPhone 16 Plus", "iPhone 15 Plus", "iPhone 14 Pro Max"],
    },
    "iPhone_6.5": {
        "label": "iPhone 14 Plus / 13 Pro Max / 11 Pro Max (6.5-inch)",
        "size": (1284, 2778),
        "required": True,
        "devices": ["iPhone 14 Plus", "iPhone 13 Pro Max", "iPhone 11 Pro Max"],
    },
    "iPhone_5.5": {
        "label": "iPhone 8 Plus (5.5-inch)",
        "size": (1242, 2208),
        "required": False,
        "devices": ["iPhone 8 Plus", "iPhone 7 Plus"],
    },
    "iPad_Pro_13": {
        "label": "iPad Pro 13-inch (6th gen)",
        "size": (2064, 2752),
        "required": False,
        "devices": ["iPad Pro 13-inch"],
    },
    "iPad_Pro_12_9": {
        "label": "iPad Pro 12.9-inch (2nd gen)",
        "size": (2048, 2732),
        "required": False,
        "devices": ["iPad Pro 12.9-inch (2nd gen)"],
    },
}

# ---------------------------------------------------------------------------
# PrivacyInfo.xcprivacy template
# ---------------------------------------------------------------------------
PRIVACY_INFO_TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyTracking</key>
    <false/>
    <key>NSPrivacyTrackingDomains</key>
    <array/>
    <key>NSPrivacyCollectedDataTypes</key>
    <array>
        <dict>
            <key>NSPrivacyCollectedDataType</key>
            <string>NSPrivacyCollectedDataTypeDeviceID</string>
            <key>NSPrivacyCollectedDataTypeLinked</key>
            <false/>
            <key>NSPrivacyCollectedDataTypeTracking</key>
            <false/>
            <key>NSPrivacyCollectedDataTypePurposes</key>
            <array>
                <string>NSPrivacyCollectedDataTypePurposeAppFunctionality</string>
            </array>
        </dict>
    </array>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>CA92.1</string>
            </array>
        </dict>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategorySystemBootTime</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>35F9.1</string>
            </array>
        </dict>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryDiskSpace</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>E174.1</string>
            </array>
        </dict>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>C617.1</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    prefix = {"INFO": "[*]", "OK": "[+]", "WARN": "[!]", "ERR": "[-]", "STEP": "[>]"}
    print(f"  {prefix.get(level, '[*]')} {ts} {msg}")


def run_cmd(cmd: list[str], cwd: Optional[Path] = None, check: bool = True,
            timeout: int = 300, capture: bool = True) -> subprocess.CompletedProcess:
    """Run a subprocess command with safety checks."""
    log(f"Running: {' '.join(cmd[:6])}{'...' if len(cmd) > 6 else ''}")
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=capture,
            text=True,
            timeout=timeout,
            check=check,
        )
        return result
    except subprocess.TimeoutExpired:
        log(f"Command timed out after {timeout}s", "ERR")
        raise
    except subprocess.CalledProcessError as e:
        log(f"Command failed (exit {e.returncode}): {e.stderr[:200] if e.stderr else 'no stderr'}", "ERR")
        raise


def load_pipeline_log() -> dict:
    if PIPELINE_LOG.exists():
        return json.loads(PIPELINE_LOG.read_text())
    return {"runs": [], "apps": {}}


def save_pipeline_log(data: dict) -> None:
    safe_path(PIPELINE_LOG)
    PIPELINE_LOG.parent.mkdir(parents=True, exist_ok=True)
    PIPELINE_LOG.write_text(json.dumps(data, indent=2, default=str))


def get_app_dir(app_key: str) -> Path:
    app = APP_REGISTRY[app_key]
    return OUTPUT_DIR / app["dir"]


# ---------------------------------------------------------------------------
# Pipeline steps
# ---------------------------------------------------------------------------

def step_wrap_capacitor(app_key: str) -> bool:
    """Wrap PWA with Capacitor and add iOS platform."""
    app = APP_REGISTRY[app_key]
    app_dir = get_app_dir(app_key)

    log(f"Wrapping {app['display_name']} with Capacitor", "STEP")

    if not app_dir.exists():
        log(f"App directory not found: {app_dir}", "ERR")
        return False

    # Init npm if needed
    pkg_json = app_dir / "package.json"
    if not pkg_json.exists():
        log("Initializing package.json")
        run_cmd(["npm", "init", "-y"], cwd=app_dir)

    # Install Capacitor
    node_modules = app_dir / "node_modules" / "@capacitor"
    if not node_modules.exists():
        log("Installing Capacitor core + cli + ios")
        run_cmd(
            ["npm", "install", "@capacitor/core", "@capacitor/cli", "@capacitor/ios"],
            cwd=app_dir,
            timeout=120,
        )

    # Init Capacitor config
    cap_config = app_dir / "capacitor.config.json"
    cap_config_ts = app_dir / "capacitor.config.ts"
    if not cap_config.exists() and not cap_config_ts.exists():
        log("Initializing Capacitor project")
        config = {
            "appId": app["bundle_id"],
            "appName": app["display_name"],
            "webDir": ".",
            "server": {"androidScheme": "https"},
            "ios": {
                "contentInset": "automatic",
                "allowsLinkPreview": False,
                "scrollEnabled": True,
            },
        }
        safe_path(cap_config)
        cap_config.write_text(json.dumps(config, indent=2))

    # Add iOS platform
    ios_dir = app_dir / "ios"
    if not ios_dir.exists():
        log("Adding iOS platform")
        run_cmd(["npx", "cap", "add", "ios"], cwd=app_dir, timeout=120)

    # Copy web assets to iOS
    log("Copying web assets to iOS project")
    run_cmd(["npx", "cap", "copy", "ios"], cwd=app_dir, timeout=60)

    # Sync native plugins
    log("Syncing native plugins")
    run_cmd(["npx", "cap", "sync", "ios"], cwd=app_dir, timeout=120)

    log(f"Capacitor wrap complete for {app['display_name']}", "OK")
    return True


def step_generate_privacy_info(app_key: str) -> bool:
    """Generate PrivacyInfo.xcprivacy in the iOS project."""
    app = APP_REGISTRY[app_key]
    app_dir = get_app_dir(app_key)
    ios_app_dir = app_dir / "ios" / "App" / "App"

    log(f"Generating PrivacyInfo.xcprivacy for {app['display_name']}", "STEP")

    if not ios_app_dir.exists():
        log(f"iOS App directory not found. Run --wrap first: {ios_app_dir}", "ERR")
        return False

    privacy_file = ios_app_dir / "PrivacyInfo.xcprivacy"
    safe_path(privacy_file)
    privacy_file.write_text(PRIVACY_INFO_TEMPLATE)
    log(f"Written: {privacy_file}", "OK")

    # Also place one at the project root for CocoaPods/SPM
    root_privacy = app_dir / "ios" / "App" / "PrivacyInfo.xcprivacy"
    safe_path(root_privacy)
    root_privacy.write_text(PRIVACY_INFO_TEMPLATE)
    log(f"Written: {root_privacy}", "OK")

    return True


def step_generate_metadata(app_key: str) -> bool:
    """Generate App Store metadata JSON for the app."""
    app = APP_REGISTRY[app_key]
    app_dir = get_app_dir(app_key)

    log(f"Generating App Store metadata for {app['display_name']}", "STEP")

    metadata = {
        "app_name": app["display_name"],
        "bundle_id": app["bundle_id"],
        "subtitle": app["subtitle"],
        "description": app["description"],
        "keywords": app["keywords"],
        "promotional_text": app["promotional_text"],
        "primary_category": app["primary_category"],
        "secondary_category": app["secondary_category"],
        "age_rating": app["age_rating"],
        "copyright": f"(c) {datetime.now().year} PRINTMAXX LLC",
        "support_url": f"https://{app_key}.printmaxx.io/support",
        "privacy_url": f"https://{app_key}.printmaxx.io/privacy",
        "marketing_url": f"https://{app_key}.printmaxx.io",
        "screenshots_required": {},
        "review_notes": (
            f"{app['display_name']} is a native iOS application built with Capacitor. "
            "It uses the following native plugins: @capacitor/haptics for tactile feedback, "
            "@capacitor/local-notifications for scheduled reminders, "
            "@capacitor/preferences for native key-value storage, "
            "@capacitor/app for app state management and deep links, "
            "@capacitor/status-bar for native status bar control. "
            "All core functionality works offline."
        ),
        "generated_at": datetime.now().isoformat(),
    }

    # Add screenshot specs
    for spec_key, spec in SCREENSHOT_SPECS.items():
        metadata["screenshots_required"][spec_key] = {
            "label": spec["label"],
            "width": spec["size"][0],
            "height": spec["size"][1],
            "required": spec["required"],
            "count": "3-10 screenshots",
            "format": "PNG or JPEG, no alpha, sRGB",
        }

    # Write metadata
    metadata_dir = app_dir / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    metadata_file = safe_path(metadata_dir / "app_store_metadata.json")
    metadata_file.write_text(json.dumps(metadata, indent=2))
    log(f"Written: {metadata_file}", "OK")

    # Write plain-text description file for copy-paste into App Store Connect
    desc_file = safe_path(metadata_dir / "description.txt")
    desc_file.write_text(app["description"])
    log(f"Written: {desc_file}", "OK")

    # Write keywords file
    kw_file = safe_path(metadata_dir / "keywords.txt")
    kw_file.write_text(app["keywords"])
    log(f"Written: {kw_file}", "OK")

    return True


def step_generate_screenshot_specs(app_key: str) -> bool:
    """Generate screenshot size specification document."""
    app = APP_REGISTRY[app_key]
    app_dir = get_app_dir(app_key)

    log(f"Generating screenshot specs for {app['display_name']}", "STEP")

    metadata_dir = app_dir / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Screenshot Specifications - {app['display_name']}",
        f"# Generated: {datetime.now().isoformat()}",
        "",
        "# Required screenshots: minimum 3, maximum 10 per device size",
        "# Format: PNG or JPEG, sRGB color space, no alpha channel",
        "# App Store Connect accepts portrait and landscape orientations",
        "",
    ]

    for spec_key, spec in SCREENSHOT_SPECS.items():
        w, h = spec["size"]
        req = "REQUIRED" if spec["required"] else "OPTIONAL"
        lines.append(f"## {spec['label']} [{req}]")
        lines.append(f"   Portrait:  {w} x {h} px")
        lines.append(f"   Landscape: {h} x {w} px")
        lines.append(f"   Devices:   {', '.join(spec['devices'])}")
        lines.append("")

    lines.extend([
        "# Simulator screenshot commands:",
        "# xcrun simctl io booted screenshot screenshot.png",
        "",
        "# Recommended screenshot content (in order):",
        "# 1. Hero shot - main feature in action",
        "# 2. Key feature #1 with callout text",
        "# 3. Key feature #2 with callout text",
        "# 4. Settings / customization screen",
        "# 5. Dark mode variant",
        "# 6. Widget / notification preview (if applicable)",
    ])

    spec_file = safe_path(metadata_dir / "screenshot_specs.txt")
    spec_file.write_text("\n".join(lines))
    log(f"Written: {spec_file}", "OK")

    return True


def step_xcode_archive(app_key: str) -> bool:
    """Build Xcode archive for distribution."""
    app = APP_REGISTRY[app_key]
    app_dir = get_app_dir(app_key)
    ios_dir = app_dir / "ios" / "App"
    workspace = ios_dir / "App.xcworkspace"

    log(f"Archiving {app['display_name']} with xcodebuild", "STEP")

    if not workspace.exists():
        # Fall back to xcodeproj
        xcodeproj = ios_dir / "App.xcodeproj"
        if not xcodeproj.exists():
            log(f"No Xcode workspace or project found at {ios_dir}", "ERR")
            return False

    archive_dir = safe_path(BUILDS_DIR / app_key)
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"{app['display_name']}.xcarchive"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Determine build source
    if workspace.exists():
        src_args = ["-workspace", str(workspace)]
    else:
        src_args = ["-project", str(ios_dir / "App.xcodeproj")]

    archive_cmd = [
        "xcodebuild",
        *src_args,
        "-scheme", "App",
        "-configuration", "Release",
        "-sdk", "iphoneos",
        "-destination", "generic/platform=iOS",
        "-archivePath", str(archive_path),
        "archive",
        "DEVELOPMENT_TEAM=XXXXXXXXXX",  # Replace with your team ID
        f"PRODUCT_BUNDLE_IDENTIFIER={app['bundle_id']}",
        "CODE_SIGN_STYLE=Automatic",
    ]

    log("Running xcodebuild archive (this may take several minutes)...")
    try:
        result = run_cmd(archive_cmd, cwd=ios_dir, timeout=600, capture=True)
        log(f"Archive created: {archive_path}", "OK")
    except subprocess.CalledProcessError as e:
        log("xcodebuild archive failed. Check Xcode project configuration.", "ERR")
        # Write error log for debugging
        err_log = safe_path(archive_dir / f"archive_error_{ts}.log")
        err_log.write_text(f"STDOUT:\n{e.stdout or ''}\n\nSTDERR:\n{e.stderr or ''}")
        log(f"Error log: {err_log}", "ERR")
        return False

    # Export IPA
    export_options_plist = safe_path(archive_dir / "ExportOptions.plist")
    export_options_content = f"""\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store-connect</string>
    <key>teamID</key>
    <string>XXXXXXXXXX</string>
    <key>signingStyle</key>
    <string>automatic</string>
    <key>uploadBitcode</key>
    <false/>
    <key>uploadSymbols</key>
    <true/>
    <key>destination</key>
    <string>upload</string>
</dict>
</plist>
"""
    export_options_plist.write_text(export_options_content)

    export_dir = safe_path(archive_dir / "export")
    export_dir.mkdir(parents=True, exist_ok=True)

    export_cmd = [
        "xcodebuild",
        "-exportArchive",
        "-archivePath", str(archive_path),
        "-exportPath", str(export_dir),
        "-exportOptionsPlist", str(export_options_plist),
    ]

    log("Exporting IPA from archive...")
    try:
        run_cmd(export_cmd, cwd=ios_dir, timeout=300)
        log(f"IPA exported to: {export_dir}", "OK")
    except subprocess.CalledProcessError:
        log("IPA export failed. Check signing and export options.", "ERR")
        return False

    return True


def step_validate_binary(app_key: str) -> bool:
    """Validate the IPA with App Store Connect using xcrun notarytool / altool."""
    app = APP_REGISTRY[app_key]
    archive_dir = BUILDS_DIR / app_key / "export"

    log(f"Validating {app['display_name']} binary", "STEP")

    # Find IPA
    ipa_files = list(archive_dir.glob("*.ipa")) if archive_dir.exists() else []
    if not ipa_files:
        log(f"No IPA found in {archive_dir}. Run archive step first.", "ERR")
        return False

    ipa_path = ipa_files[0]
    log(f"Found IPA: {ipa_path.name}")

    # Validate with xcrun altool
    validate_cmd = [
        "xcrun", "altool",
        "--validate-app",
        "--file", str(ipa_path),
        "--type", "ios",
        "--apiKey", "YOUR_API_KEY_ID",        # Replace with App Store Connect API key ID
        "--apiIssuer", "YOUR_ISSUER_ID",      # Replace with App Store Connect issuer ID
    ]

    log("Running xcrun altool --validate-app...")
    try:
        result = run_cmd(validate_cmd, timeout=300)
        if result.returncode == 0:
            log("Validation passed", "OK")
            return True
    except subprocess.CalledProcessError as e:
        log(f"Validation failed: {e.stderr[:300] if e.stderr else 'unknown error'}", "ERR")

    # Alternative: try with xcrun notarytool for newer Xcode
    log("Trying xcrun notarytool as fallback...")
    notary_cmd = [
        "xcrun", "notarytool", "submit",
        str(ipa_path),
        "--key", "~/.private_keys/AuthKey_YOUR_KEY.p8",
        "--key-id", "YOUR_API_KEY_ID",
        "--issuer", "YOUR_ISSUER_ID",
        "--wait",
    ]
    log(f"Notarytool command prepared (update API keys before running)", "WARN")
    log(f"  {' '.join(notary_cmd)}")

    return False


def step_upload_binary(app_key: str) -> bool:
    """Upload the validated IPA to App Store Connect."""
    app = APP_REGISTRY[app_key]
    archive_dir = BUILDS_DIR / app_key / "export"

    log(f"Uploading {app['display_name']} to App Store Connect", "STEP")

    ipa_files = list(archive_dir.glob("*.ipa")) if archive_dir.exists() else []
    if not ipa_files:
        log(f"No IPA found in {archive_dir}", "ERR")
        return False

    ipa_path = ipa_files[0]

    upload_cmd = [
        "xcrun", "altool",
        "--upload-app",
        "--file", str(ipa_path),
        "--type", "ios",
        "--apiKey", "YOUR_API_KEY_ID",
        "--apiIssuer", "YOUR_ISSUER_ID",
    ]

    log("Running xcrun altool --upload-app...")
    try:
        result = run_cmd(upload_cmd, timeout=600)
        if result.returncode == 0:
            log("Upload successful. Check App Store Connect for processing status.", "OK")
            return True
    except subprocess.CalledProcessError as e:
        log(f"Upload failed: {e.stderr[:300] if e.stderr else 'unknown error'}", "ERR")

    return False


# ---------------------------------------------------------------------------
# Pipeline orchestration
# ---------------------------------------------------------------------------

def run_pipeline(app_key: str, steps: list[str]) -> dict:
    """Run specified pipeline steps for an app."""
    app = APP_REGISTRY[app_key]
    results = {}
    start = time.time()

    print(f"\n{'='*60}")
    print(f"  iOS RELEASE PIPELINE: {app['display_name']}")
    print(f"  Bundle: {app['bundle_id']}")
    print(f"  Steps:  {', '.join(steps)}")
    print(f"{'='*60}\n")

    step_map = {
        "wrap": step_wrap_capacitor,
        "privacy": step_generate_privacy_info,
        "metadata": step_generate_metadata,
        "screenshots": step_generate_screenshot_specs,
        "archive": step_xcode_archive,
        "validate": step_validate_binary,
        "upload": step_upload_binary,
    }

    for step_name in steps:
        if step_name not in step_map:
            log(f"Unknown step: {step_name}", "WARN")
            results[step_name] = False
            continue

        try:
            ok = step_map[step_name](app_key)
            results[step_name] = ok
            if not ok and step_name in ("wrap", "archive"):
                log(f"Critical step '{step_name}' failed. Stopping pipeline.", "ERR")
                break
        except Exception as e:
            log(f"Step '{step_name}' raised exception: {e}", "ERR")
            results[step_name] = False
            break

    elapsed = time.time() - start
    passed = sum(1 for v in results.values() if v)
    total = len(results)

    print(f"\n{'='*60}")
    print(f"  PIPELINE SUMMARY: {app['display_name']}")
    print(f"  Result: {passed}/{total} steps passed")
    print(f"  Time:   {elapsed:.1f}s")
    for step_name, ok in results.items():
        status = "PASS" if ok else "FAIL"
        print(f"    {status}  {step_name}")
    print(f"{'='*60}\n")

    # Log to pipeline history
    pipeline_log = load_pipeline_log()
    run_entry = {
        "app": app_key,
        "display_name": app["display_name"],
        "steps": steps,
        "results": results,
        "elapsed_seconds": round(elapsed, 1),
        "timestamp": datetime.now().isoformat(),
    }
    pipeline_log["runs"].append(run_entry)
    pipeline_log["apps"][app_key] = {
        "last_run": datetime.now().isoformat(),
        "last_results": results,
    }
    save_pipeline_log(pipeline_log)

    return results


def show_status() -> None:
    """Show pipeline status for all apps."""
    print(f"\n{'='*60}")
    print("  iOS RELEASE PIPELINE STATUS")
    print(f"{'='*60}\n")

    # Check each app
    for app_key, app in APP_REGISTRY.items():
        app_dir = get_app_dir(app_key)
        has_dir = app_dir.exists()
        has_ios = (app_dir / "ios").exists() if has_dir else False
        has_cap = (app_dir / "capacitor.config.json").exists() if has_dir else False
        has_privacy = (app_dir / "ios" / "App" / "App" / "PrivacyInfo.xcprivacy").exists() if has_ios else False
        has_metadata = (app_dir / "metadata" / "app_store_metadata.json").exists() if has_dir else False

        status_parts = []
        if not has_dir:
            status_parts.append("NO DIR")
        else:
            status_parts.append("DIR:ok" if has_dir else "DIR:--")
            status_parts.append("CAP:ok" if has_cap else "CAP:--")
            status_parts.append("IOS:ok" if has_ios else "IOS:--")
            status_parts.append("PRV:ok" if has_privacy else "PRV:--")
            status_parts.append("META:ok" if has_metadata else "META:--")

        print(f"  {app['display_name']:15s} ({app['bundle_id']})")
        print(f"    {' | '.join(status_parts)}")

    # Check for builds
    print(f"\n  BUILDS:")
    if BUILDS_DIR.exists():
        for app_key in APP_REGISTRY:
            build_dir = BUILDS_DIR / app_key
            if build_dir.exists():
                archives = list(build_dir.glob("*.xcarchive"))
                ipas = list((build_dir / "export").glob("*.ipa")) if (build_dir / "export").exists() else []
                print(f"    {app_key}: {len(archives)} archive(s), {len(ipas)} IPA(s)")
    else:
        print("    No builds directory yet.")

    # Recent runs
    pipeline_log = load_pipeline_log()
    if pipeline_log.get("runs"):
        print(f"\n  RECENT RUNS (last 5):")
        for run in pipeline_log["runs"][-5:]:
            passed = sum(1 for v in run["results"].values() if v)
            total = len(run["results"])
            print(f"    {run['timestamp'][:16]}  {run['display_name']:15s}  {passed}/{total} passed  ({run['elapsed_seconds']}s)")

    print(f"\n{'='*60}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="iOS Release Pipeline - Automated PWA to App Store submission",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s --app focuslock --all-steps       Full pipeline for one app
  %(prog)s --all --wrap-only                 Wrap all apps with Capacitor
  %(prog)s --app sleepmaxx --validate-only   Validate existing build
  %(prog)s --app mealmaxx --metadata-only    Generate metadata only
  %(prog)s --status                          Show pipeline status
  %(prog)s --list-apps                       List registered apps
""",
    )

    # App selection
    app_group = parser.add_mutually_exclusive_group()
    app_group.add_argument("--app", type=str, help="App key (e.g. focuslock, sleepmaxx)")
    app_group.add_argument("--all", action="store_true", help="Run for all registered apps")

    # Step selection
    step_group = parser.add_mutually_exclusive_group()
    step_group.add_argument("--all-steps", action="store_true",
                            help="Run full pipeline: wrap, privacy, metadata, screenshots, archive, validate, upload")
    step_group.add_argument("--wrap-only", action="store_true",
                            help="Only wrap with Capacitor + generate privacy manifest")
    step_group.add_argument("--metadata-only", action="store_true",
                            help="Only generate App Store metadata + screenshot specs")
    step_group.add_argument("--build-only", action="store_true",
                            help="Only run xcodebuild archive + export")
    step_group.add_argument("--validate-only", action="store_true",
                            help="Only validate existing IPA")
    step_group.add_argument("--upload-only", action="store_true",
                            help="Only upload validated IPA")
    step_group.add_argument("--steps", nargs="+",
                            choices=["wrap", "privacy", "metadata", "screenshots", "archive", "validate", "upload"],
                            help="Run specific steps")

    # Info commands
    parser.add_argument("--status", action="store_true", help="Show pipeline status")
    parser.add_argument("--list-apps", action="store_true", help="List registered apps")

    args = parser.parse_args()

    # Info commands
    if args.status:
        show_status()
        return

    if args.list_apps:
        print("\nRegistered apps:")
        for key, app in APP_REGISTRY.items():
            print(f"  {key:15s}  {app['display_name']:15s}  {app['bundle_id']}")
        print()
        return

    # Determine steps
    if args.all_steps:
        steps = ["wrap", "privacy", "metadata", "screenshots", "archive", "validate", "upload"]
    elif args.wrap_only:
        steps = ["wrap", "privacy"]
    elif args.metadata_only:
        steps = ["metadata", "screenshots"]
    elif args.build_only:
        steps = ["archive"]
    elif args.validate_only:
        steps = ["validate"]
    elif args.upload_only:
        steps = ["upload"]
    elif args.steps:
        steps = args.steps
    else:
        # Default to metadata + screenshots (safe, no builds)
        steps = ["metadata", "screenshots"]

    # Determine apps
    if args.all:
        apps_to_run = list(APP_REGISTRY.keys())
    elif args.app:
        app_key = args.app.lower().replace("-", "").replace("_", "")
        # Fuzzy match
        matched = None
        for key in APP_REGISTRY:
            if key == app_key or key.startswith(app_key) or app_key in key:
                matched = key
                break
        if not matched:
            print(f"Unknown app: {args.app}")
            print(f"Available: {', '.join(APP_REGISTRY.keys())}")
            sys.exit(1)
        apps_to_run = [matched]
    else:
        parser.print_help()
        sys.exit(1)

    # Run pipeline
    all_results = {}
    for app_key in apps_to_run:
        results = run_pipeline(app_key, steps)
        all_results[app_key] = results

    # Final summary for multi-app runs
    if len(apps_to_run) > 1:
        print(f"\n{'='*60}")
        print("  MULTI-APP SUMMARY")
        print(f"{'='*60}")
        for app_key, results in all_results.items():
            passed = sum(1 for v in results.values() if v)
            total = len(results)
            status = "ALL PASS" if passed == total else f"{passed}/{total}"
            print(f"  {APP_REGISTRY[app_key]['display_name']:15s}  {status}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
