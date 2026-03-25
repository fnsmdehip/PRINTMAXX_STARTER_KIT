#!/usr/bin/env python3
"""
App Store Auto-Submit Pipeline
Submits all PRINTMAXX apps to iOS App Store via EAS CLI.

Prerequisites:
- Apple Developer account ($99/yr)
- eas login (run once with Apple ID)
- RevenueCat products configured
- Privacy policy URLs live

Usage:
    python3 app_store_submit.py --status          # Check readiness of all apps
    python3 app_store_submit.py --build APP_NAME   # Build one app for submission
    python3 app_store_submit.py --submit APP_NAME  # Submit to App Store Review
    python3 app_store_submit.py --all              # Build and submit all apps
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILDS_DIR = PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY" / "builds"

# App registry — all production-ready apps
APPS = {
    "nutriai": {
        "path": BUILDS_DIR / "nutriai",
        "bundle_id": "com.printmaxx.nutriai",
        "name": "NutriAI - Calorie Tracker",
        "category": "FOOD_AND_DRINK",
        "secondary_category": "HEALTH_AND_FITNESS",
        "age_rating": "4+",
        "pricing": {"annual": "$29.99", "monthly": "$4.99"},
    },
    "scripture-streak": {
        "path": BUILDS_DIR / "scripture-streak",
        "bundle_id": "com.printmaxx.scripturestreak",
        "name": "Scripture Streak - Bible",
        "category": "LIFESTYLE",
        "secondary_category": "EDUCATION",
        "age_rating": "4+",
        "pricing": {"annual": "$19.99", "monthly": "$3.99"},
    },
    "pocket-alexandria": {
        "path": BUILDS_DIR / "pocket-alexandria",
        "bundle_id": "com.printmaxx.pocketalexandria",
        "name": "Pocket Alexandria",
        "category": "BOOKS",
        "secondary_category": "EDUCATION",
        "age_rating": "4+",
        "pricing": {"annual": "$9.99", "monthly": "$1.99"},
    },
    "cnsnt": {
        "path": BUILDS_DIR / "cnsnt",
        "bundle_id": "com.printmaxx.cnsnt",
        "name": "cnsnt - Consent Records",
        "category": "PRODUCTIVITY",
        "secondary_category": "UTILITIES",
        "age_rating": "4+",
        "pricing": {"annual": "$29.99", "monthly": "$4.99"},
    },
}

# Pre-submission checklist
CHECKLIST = [
    ("app.json exists", lambda p: (p / "app.json").exists()),
    ("bundle ID set", lambda p: _check_bundle_id(p)),
    ("privacy URL set", lambda p: _check_extra_field(p, "privacyPolicyUrl")),
    ("no console.log", lambda p: _no_console_log(p)),
    ("no placeholder text", lambda p: _no_placeholder(p)),
    ("iOS export clean", lambda p: _can_export(p)),
    ("eas.json exists", lambda p: (p / "eas.json").exists()),
]


def _check_bundle_id(path):
    try:
        config = json.loads((path / "app.json").read_text())
        return bool(config.get("expo", {}).get("ios", {}).get("bundleIdentifier"))
    except:
        return False


def _check_extra_field(path, field):
    try:
        config = json.loads((path / "app.json").read_text())
        return bool(config.get("expo", {}).get("extra", {}).get(field))
    except:
        return False


def _no_console_log(path):
    result = subprocess.run(
        f"grep -r 'console\\.log' {path}/app {path}/src --include='*.tsx' --include='*.ts' -l 2>/dev/null",
        shell=True, capture_output=True, text=True
    )
    return len(result.stdout.strip()) == 0


def _no_placeholder(path):
    result = subprocess.run(
        f"grep -ri 'lorem ipsum\\|placeholder text\\|TODO:' {path}/app {path}/src --include='*.tsx' --include='*.ts' -l 2>/dev/null",
        shell=True, capture_output=True, text=True
    )
    return len(result.stdout.strip()) == 0


def _can_export(path):
    # Check if dist/ exists from a recent export
    dist = path / "dist"
    if dist.exists():
        files = list(dist.rglob("*.hbc"))
        return len(files) > 0
    return False


def ensure_eas_json(app_path, app_config):
    """Create eas.json if it doesn't exist."""
    eas_path = app_path / "eas.json"
    if not eas_path.exists():
        eas_config = {
            "cli": {"version": ">= 16.0.0"},
            "build": {
                "development": {
                    "developmentClient": True,
                    "distribution": "internal"
                },
                "preview": {
                    "distribution": "internal"
                },
                "production": {}
            },
            "submit": {
                "production": {
                    "ios": {
                        "appleId": "",  # User fills in
                        "ascAppId": "",  # User fills in
                        "appleTeamId": ""  # User fills in
                    }
                }
            }
        }
        eas_path.write_text(json.dumps(eas_config, indent=2))
        print(f"  Created eas.json at {eas_path}")


def check_status():
    """Check readiness of all apps."""
    print("App Store Submission Readiness\n" + "=" * 50)

    for app_name, config in APPS.items():
        path = config["path"]
        print(f"\n{app_name} ({config['name']})")
        print(f"  Bundle ID: {config['bundle_id']}")
        print(f"  Path: {path}")

        all_pass = True
        for check_name, check_fn in CHECKLIST:
            try:
                passed = check_fn(path)
            except:
                passed = False
            status = "PASS" if passed else "FAIL"
            if not passed:
                all_pass = False
            print(f"  [{status}] {check_name}")

        print(f"  Overall: {'READY' if all_pass else 'NOT READY'}")

    # Check EAS login
    print(f"\nEAS CLI: ", end="")
    result = subprocess.run("eas whoami 2>&1", shell=True, capture_output=True, text=True)
    if "not logged in" in result.stdout.lower() or result.returncode != 0:
        print("NOT LOGGED IN — run: eas login")
    else:
        print(f"Logged in as {result.stdout.strip()}")

    # Check Apple Developer
    print(f"Fastlane: ", end="")
    result = subprocess.run("fastlane --version 2>&1 | head -1", shell=True, capture_output=True, text=True)
    print(result.stdout.strip())


def build_app(app_name):
    """Build app for App Store submission via EAS."""
    if app_name not in APPS:
        print(f"Unknown app: {app_name}. Available: {', '.join(APPS.keys())}")
        return False

    config = APPS[app_name]
    path = config["path"]

    ensure_eas_json(path, config)

    print(f"Building {app_name} for App Store...")
    result = subprocess.run(
        "eas build --platform ios --profile production --non-interactive",
        shell=True, cwd=str(path)
    )
    return result.returncode == 0


def submit_app(app_name):
    """Submit built app to App Store Review."""
    if app_name not in APPS:
        print(f"Unknown app: {app_name}")
        return False

    config = APPS[app_name]
    path = config["path"]

    print(f"Submitting {app_name} to App Store Review...")
    result = subprocess.run(
        "eas submit --platform ios --profile production --non-interactive",
        shell=True, cwd=str(path)
    )
    return result.returncode == 0


def submit_all():
    """Build and submit all apps."""
    for app_name in APPS:
        print(f"\n{'='*50}")
        print(f"Processing: {app_name}")
        print(f"{'='*50}")

        if build_app(app_name):
            submit_app(app_name)
        else:
            print(f"Build failed for {app_name}, skipping submit")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "--status":
        check_status()
    elif cmd == "--build" and len(sys.argv) > 2:
        build_app(sys.argv[2])
    elif cmd == "--submit" and len(sys.argv) > 2:
        submit_app(sys.argv[2])
    elif cmd == "--all":
        submit_all()
    else:
        print(__doc__)
