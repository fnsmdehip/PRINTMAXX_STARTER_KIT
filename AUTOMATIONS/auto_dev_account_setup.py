#!/usr/bin/env python3
"""
Apple Developer Account Setup Automation
Generates developer assets, provisioning commands, Fastlane configs, enrollment guide.

Usage:
    python3 AUTOMATIONS/auto_dev_account_setup.py --setup
    python3 AUTOMATIONS/auto_dev_account_setup.py --icons focuslock
    python3 AUTOMATIONS/auto_dev_account_setup.py --fastlane focuslock
    python3 AUTOMATIONS/auto_dev_account_setup.py --guide
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "ralph" / "loops" / "app_factory" / "output"
SETUP_DIR = PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY" / "dev_setup"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT.resolve())):
        raise ValueError(f"BLOCKED: {resolved} is outside project root")
    return resolved


# ---------------------------------------------------------------------------
# App registry (imported from ios_release_pipeline)
# ---------------------------------------------------------------------------
APP_REGISTRY = {
    "focuslock": {
        "dir": "focuslock-web",
        "display_name": "FocusLock",
        "bundle_id": "com.printmaxx.focuslock",
    },
    "habitforge": {
        "dir": "habitforge-web",
        "display_name": "HabitForge",
        "bundle_id": "com.printmaxx.habitforge",
    },
    "mealmaxx": {
        "dir": "mealmaxx-web",
        "display_name": "MealMaxx",
        "bundle_id": "com.printmaxx.mealmaxx",
    },
    "hilal": {
        "dir": "ramadan-tracker",
        "display_name": "Hilal",
        "bundle_id": "com.printmaxx.hilal",
    },
    "sleepmaxx": {
        "dir": "sleepmaxx-web",
        "display_name": "SleepMaxx",
        "bundle_id": "com.printmaxx.sleepmaxx",
    },
    "walktounlock": {
        "dir": "walktounlock-web",
        "display_name": "WalkToUnlock",
        "bundle_id": "com.printmaxx.walktounlock",
    },
}

# ---------------------------------------------------------------------------
# Icon specifications - all sizes needed for iOS App Store
# ---------------------------------------------------------------------------
ICON_SPECS = {
    "app_store": {
        "size": (1024, 1024),
        "filename": "AppIcon-1024x1024.png",
        "purpose": "App Store listing (required, no alpha, no transparency)",
        "notes": "sRGB or Display P3 color space. No rounded corners (Apple adds them). No alpha channel.",
    },
    "iphone_180": {
        "size": (180, 180),
        "filename": "AppIcon-60@3x.png",
        "purpose": "iPhone app icon @3x (iPhone X and later)",
    },
    "iphone_120": {
        "size": (120, 120),
        "filename": "AppIcon-60@2x.png",
        "purpose": "iPhone app icon @2x",
    },
    "iphone_spotlight_120": {
        "size": (120, 120),
        "filename": "AppIcon-40@3x.png",
        "purpose": "iPhone Spotlight @3x",
    },
    "iphone_spotlight_80": {
        "size": (80, 80),
        "filename": "AppIcon-40@2x.png",
        "purpose": "iPhone Spotlight @2x",
    },
    "iphone_notification_60": {
        "size": (60, 60),
        "filename": "AppIcon-20@3x.png",
        "purpose": "iPhone Notification @3x",
    },
    "iphone_notification_40": {
        "size": (40, 40),
        "filename": "AppIcon-20@2x.png",
        "purpose": "iPhone Notification @2x",
    },
    "iphone_settings_87": {
        "size": (87, 87),
        "filename": "AppIcon-29@3x.png",
        "purpose": "iPhone Settings @3x",
    },
    "iphone_settings_58": {
        "size": (58, 58),
        "filename": "AppIcon-29@2x.png",
        "purpose": "iPhone Settings @2x",
    },
    "ipad_167": {
        "size": (167, 167),
        "filename": "AppIcon-83.5@2x.png",
        "purpose": "iPad Pro app icon @2x",
    },
    "ipad_152": {
        "size": (152, 152),
        "filename": "AppIcon-76@2x.png",
        "purpose": "iPad app icon @2x",
    },
    "ipad_76": {
        "size": (76, 76),
        "filename": "AppIcon-76@1x.png",
        "purpose": "iPad app icon @1x",
    },
}

# ---------------------------------------------------------------------------
# Launch screen specifications
# ---------------------------------------------------------------------------
LAUNCH_SCREEN_SPECS = {
    "storyboard": {
        "description": "Use LaunchScreen.storyboard (Capacitor default). Single centered logo on solid background.",
        "notes": (
            "Capacitor generates a default LaunchScreen.storyboard. "
            "Customize by editing ios/App/App/LaunchScreen.storyboard in Xcode. "
            "Use Auto Layout constraints to center your logo. "
            "Background color should match your app theme. "
            "Do NOT use a static launch image -- Apple requires storyboard since 2020."
        ),
    },
    "logo_specs": {
        "sizes": {
            "1x": (200, 200),
            "2x": (400, 400),
            "3x": (600, 600),
        },
        "format": "PNG with transparency",
        "placement": "Centered horizontally and vertically",
    },
    "background_colors": {
        "light_mode": "#FFFFFF",
        "dark_mode": "#000000",
        "note": "Match your app's primary background color",
    },
}


# ---------------------------------------------------------------------------
# Icon generation
# ---------------------------------------------------------------------------

def generate_icon_specs(app_key: str) -> None:
    """Generate icon specification files and sips resize commands."""
    app = APP_REGISTRY[app_key]
    app_dir = OUTPUT_DIR / app["dir"]

    print(f"\n{'='*60}")
    print(f"  ICON GENERATION: {app['display_name']}")
    print(f"{'='*60}\n")

    icons_dir = safe_path(app_dir / "ios_assets" / "icons")
    icons_dir.mkdir(parents=True, exist_ok=True)

    # Write icon spec JSON
    spec_file = safe_path(icons_dir / "icon_specs.json")
    spec_file.write_text(json.dumps(ICON_SPECS, indent=2, default=str))
    print(f"  [+] Written: {spec_file}")

    # Generate sips resize script (macOS built-in image tool)
    script_lines = [
        "#!/bin/bash",
        f"# Auto-generated icon resize script for {app['display_name']}",
        f"# Generated: {datetime.now().isoformat()}",
        "#",
        "# USAGE: Place your 1024x1024 source icon as 'source_icon.png'",
        f"#        in {icons_dir}/",
        "#        Then run: bash resize_icons.sh",
        "",
        "set -e",
        "",
        f'SOURCE="{icons_dir}/source_icon.png"',
        f'OUTPUT_DIR="{icons_dir}/generated"',
        "",
        'if [ ! -f "$SOURCE" ]; then',
        '    echo "ERROR: Place your 1024x1024 icon as source_icon.png in this directory"',
        "    exit 1",
        "fi",
        "",
        'mkdir -p "$OUTPUT_DIR"',
        "",
        "# Copy the 1024x1024 for App Store (no resize needed)",
        'cp "$SOURCE" "$OUTPUT_DIR/AppIcon-1024x1024.png"',
        "",
    ]

    for spec_key, spec in ICON_SPECS.items():
        if spec_key == "app_store":
            continue
        w, h = spec["size"]
        fname = spec["filename"]
        script_lines.append(f'# {spec["purpose"]}')
        script_lines.append(f'sips -z {h} {w} "$SOURCE" --out "$OUTPUT_DIR/{fname}"')
        script_lines.append("")

    script_lines.extend([
        'echo "All icons generated in $OUTPUT_DIR/"',
        'echo "Copy the generated/ folder contents into your Xcode asset catalog:"',
        f'echo "  {app_dir}/ios/App/App/Assets.xcassets/AppIcon.appiconset/"',
    ])

    script_file = safe_path(icons_dir / "resize_icons.sh")
    script_file.write_text("\n".join(script_lines))
    print(f"  [+] Written: {script_file}")

    # Generate Contents.json for Xcode asset catalog
    contents_json = generate_appicon_contents_json()
    contents_file = safe_path(icons_dir / "Contents.json")
    contents_file.write_text(json.dumps(contents_json, indent=2))
    print(f"  [+] Written: {contents_file}")

    # Print summary
    print(f"\n  Icon sizes needed:")
    for spec_key, spec in ICON_SPECS.items():
        w, h = spec["size"]
        print(f"    {w:4d}x{h:<4d}  {spec['filename']:30s}  {spec['purpose']}")

    print(f"\n  Steps:")
    print(f"    1. Create a 1024x1024 PNG icon (no alpha, no transparency)")
    print(f"    2. Save as: {icons_dir}/source_icon.png")
    print(f"    3. Run: bash {script_file}")
    print(f"    4. Copy generated/ contents to Xcode AppIcon.appiconset/")
    print(f"\n{'='*60}\n")


def generate_appicon_contents_json() -> dict:
    """Generate the Contents.json for Xcode AppIcon asset catalog."""
    images = [
        {"idiom": "universal", "platform": "ios", "size": "1024x1024",
         "filename": "AppIcon-1024x1024.png"},
        {"idiom": "iphone", "scale": "2x", "size": "60x60",
         "filename": "AppIcon-60@2x.png"},
        {"idiom": "iphone", "scale": "3x", "size": "60x60",
         "filename": "AppIcon-60@3x.png"},
        {"idiom": "iphone", "scale": "2x", "size": "40x40",
         "filename": "AppIcon-40@2x.png"},
        {"idiom": "iphone", "scale": "3x", "size": "40x40",
         "filename": "AppIcon-40@3x.png"},
        {"idiom": "iphone", "scale": "2x", "size": "20x20",
         "filename": "AppIcon-20@2x.png"},
        {"idiom": "iphone", "scale": "3x", "size": "20x20",
         "filename": "AppIcon-20@3x.png"},
        {"idiom": "iphone", "scale": "2x", "size": "29x29",
         "filename": "AppIcon-29@2x.png"},
        {"idiom": "iphone", "scale": "3x", "size": "29x29",
         "filename": "AppIcon-29@3x.png"},
        {"idiom": "ipad", "scale": "2x", "size": "83.5x83.5",
         "filename": "AppIcon-83.5@2x.png"},
        {"idiom": "ipad", "scale": "2x", "size": "76x76",
         "filename": "AppIcon-76@2x.png"},
        {"idiom": "ipad", "scale": "1x", "size": "76x76",
         "filename": "AppIcon-76@1x.png"},
    ]
    return {"images": images, "info": {"version": 1, "author": "auto_dev_account_setup"}}


# ---------------------------------------------------------------------------
# Provisioning profile commands
# ---------------------------------------------------------------------------

def generate_provisioning_commands(app_key: str) -> None:
    """Generate terminal commands for provisioning profile management."""
    app = APP_REGISTRY[app_key]

    print(f"\n{'='*60}")
    print(f"  PROVISIONING COMMANDS: {app['display_name']}")
    print(f"{'='*60}\n")

    commands = {
        "list_profiles": {
            "description": "List all installed provisioning profiles",
            "command": 'ls ~/Library/MobileDevice/Provisioning\\ Profiles/',
        },
        "decode_profile": {
            "description": "Decode a provisioning profile to read its contents",
            "command": 'security cms -D -i ~/Library/MobileDevice/Provisioning\\ Profiles/YOUR_PROFILE.mobileprovision',
        },
        "list_signing_identities": {
            "description": "List all code signing identities in keychain",
            "command": "security find-identity -v -p codesigning",
        },
        "create_cert_signing_request": {
            "description": "Create a Certificate Signing Request (CSR)",
            "command": (
                "openssl req -new -newkey rsa:2048 -nodes "
                "-keyout printmaxx_ios.key -out printmaxx_ios.csr "
                '-subj "/CN=PRINTMAXX LLC/O=PRINTMAXX LLC/C=US"'
            ),
        },
        "register_device": {
            "description": "Register a test device (get UDID from Finder or Xcode)",
            "command": 'xcrun altool --register-device --name "Test iPhone" --udid YOUR_UDID',
        },
        "xcode_auto_signing": {
            "description": "Let Xcode handle signing automatically (recommended)",
            "command": (
                f"# In Xcode: Target > Signing & Capabilities\n"
                f"#   Team: Your Apple Developer Team\n"
                f"#   Bundle Identifier: {app['bundle_id']}\n"
                f"#   Automatically manage signing: YES\n"
                f"# Xcode will create provisioning profiles automatically"
            ),
        },
    }

    for key, cmd in commands.items():
        print(f"  ## {cmd['description']}")
        for line in cmd["command"].split("\n"):
            print(f"    {line}")
        print()

    # Write commands to file
    cmd_dir = safe_path(SETUP_DIR / app_key)
    cmd_dir.mkdir(parents=True, exist_ok=True)
    cmd_file = safe_path(cmd_dir / "provisioning_commands.sh")

    lines = [
        "#!/bin/bash",
        f"# Provisioning commands for {app['display_name']}",
        f"# Bundle ID: {app['bundle_id']}",
        f"# Generated: {datetime.now().isoformat()}",
        "",
    ]
    for key, cmd in commands.items():
        lines.append(f"# --- {cmd['description']} ---")
        lines.append(f"# {cmd['command']}")
        lines.append("")

    cmd_file.write_text("\n".join(lines))
    print(f"  [+] Written: {cmd_file}")
    print(f"\n{'='*60}\n")


# ---------------------------------------------------------------------------
# Fastlane configuration
# ---------------------------------------------------------------------------

def generate_fastlane_config(app_key: str) -> None:
    """Generate Fastlane configuration files (Appfile, Fastfile, Matchfile)."""
    app = APP_REGISTRY[app_key]
    app_dir = OUTPUT_DIR / app["dir"]

    print(f"\n{'='*60}")
    print(f"  FASTLANE CONFIG: {app['display_name']}")
    print(f"{'='*60}\n")

    fastlane_dir = safe_path(app_dir / "ios" / "App" / "fastlane")
    fastlane_dir.mkdir(parents=True, exist_ok=True)

    # --- Appfile ---
    appfile_content = f"""\
# Appfile - {app['display_name']}
# Generated: {datetime.now().isoformat()}

app_identifier("{app['bundle_id']}")
apple_id("YOUR_APPLE_ID@email.com")      # Your Apple Developer email
team_id("XXXXXXXXXX")                     # Your Apple Developer Team ID
itc_team_id("XXXXXXXXXX")                 # Your App Store Connect Team ID

# For multiple targets:
# for_platform :ios do
#   app_identifier("{app['bundle_id']}")
# end
"""
    appfile = safe_path(fastlane_dir / "Appfile")
    appfile.write_text(appfile_content)
    print(f"  [+] Written: {appfile}")

    # --- Fastfile ---
    fastfile_content = f"""\
# Fastfile - {app['display_name']}
# Generated: {datetime.now().isoformat()}

default_platform(:ios)

platform :ios do

  desc "Build and run tests"
  lane :test do
    scan(
      workspace: "App.xcworkspace",
      scheme: "App",
      clean: true,
      devices: ["iPhone 16 Pro"]
    )
  end

  desc "Build for TestFlight (beta)"
  lane :beta do
    # Ensure clean git status
    # ensure_git_status_clean

    # Increment build number
    increment_build_number(
      xcodeproj: "App.xcodeproj"
    )

    # Build the app
    build_app(
      workspace: "App.xcworkspace",
      scheme: "App",
      configuration: "Release",
      export_method: "app-store",
      export_options: {{
        provisioningProfiles: {{
          "{app['bundle_id']}" => "match AppStore {app['bundle_id']}"
        }}
      }}
    )

    # Upload to TestFlight
    upload_to_testflight(
      skip_waiting_for_build_processing: true,
      apple_id: "YOUR_APP_APPLE_ID"       # App-specific Apple ID from App Store Connect
    )

    # Notify
    puts "Beta build uploaded to TestFlight for {app['display_name']}"
  end

  desc "Deploy to App Store"
  lane :release do
    # Ensure clean git status
    # ensure_git_status_clean

    # Increment build number
    increment_build_number(
      xcodeproj: "App.xcodeproj"
    )

    # Build the app
    build_app(
      workspace: "App.xcworkspace",
      scheme: "App",
      configuration: "Release",
      export_method: "app-store",
      export_options: {{
        provisioningProfiles: {{
          "{app['bundle_id']}" => "match AppStore {app['bundle_id']}"
        }}
      }}
    )

    # Upload to App Store Connect
    deliver(
      submit_for_review: false,
      automatic_release: false,
      force: true,
      skip_screenshots: true,
      skip_metadata: false,
      metadata_path: "./fastlane/metadata"
    )

    puts "Release build uploaded for {app['display_name']}"
  end

  desc "Download and install certificates via match"
  lane :certificates do
    match(type: "development")
    match(type: "appstore")
  end

  desc "Take App Store screenshots"
  lane :screenshots do
    capture_screenshots(
      workspace: "App.xcworkspace",
      scheme: "App",
      devices: [
        "iPhone 16 Pro Max",
        "iPhone 16 Plus",
        "iPhone 14 Pro Max",
        "iPhone 8 Plus"
      ],
      languages: ["en-US", "es-ES", "pt-BR"],
      clear_previous_screenshots: true,
      output_directory: "./fastlane/screenshots"
    )
  end

end
"""
    fastfile = safe_path(fastlane_dir / "Fastfile")
    fastfile.write_text(fastfile_content)
    print(f"  [+] Written: {fastfile}")

    # --- Matchfile ---
    matchfile_content = f"""\
# Matchfile - {app['display_name']}
# Generated: {datetime.now().isoformat()}
#
# match manages your provisioning profiles and certificates
# See: https://docs.fastlane.tools/actions/match/

git_url("https://github.com/YOUR_ORG/ios-certificates.git")  # Private repo for certs

storage_mode("git")

type("appstore")    # Can be: development, adhoc, appstore, enterprise

app_identifier(["{app['bundle_id']}"])

username("YOUR_APPLE_ID@email.com")

team_id("XXXXXXXXXX")

# Optional: Use Apple's cloud-managed signing
# storage_mode("google_cloud")
# google_cloud_bucket_name("your-bucket")
"""
    matchfile = safe_path(fastlane_dir / "Matchfile")
    matchfile.write_text(matchfile_content)
    print(f"  [+] Written: {matchfile}")

    # --- Gemfile ---
    gemfile_content = """\
source "https://rubygems.org"

gem "fastlane"

# Optional plugins
# gem "fastlane-plugin-firebase_app_distribution"
"""
    gemfile = safe_path(fastlane_dir.parent / "Gemfile")
    gemfile.write_text(gemfile_content)
    print(f"  [+] Written: {gemfile}")

    # Print usage instructions
    print(f"\n  Fastlane commands for {app['display_name']}:")
    print(f"    cd {app_dir}/ios/App")
    print(f"    bundle install                    # Install Fastlane")
    print(f"    bundle exec fastlane certificates # Download signing certs")
    print(f"    bundle exec fastlane beta         # Build + upload to TestFlight")
    print(f"    bundle exec fastlane release      # Build + upload to App Store")
    print(f"    bundle exec fastlane screenshots  # Capture App Store screenshots")

    print(f"\n  Before first run, update these placeholders:")
    print(f"    - YOUR_APPLE_ID@email.com   (your Apple Developer email)")
    print(f"    - XXXXXXXXXX                (your Team ID from developer.apple.com)")
    print(f"    - YOUR_APP_APPLE_ID         (app-specific ID from App Store Connect)")
    print(f"    - git_url in Matchfile      (private repo for certificates)")

    print(f"\n{'='*60}\n")


# ---------------------------------------------------------------------------
# Full setup
# ---------------------------------------------------------------------------

def run_full_setup() -> None:
    """Run full developer account setup for all apps."""
    print(f"\n{'='*60}")
    print("  FULL DEVELOPER ACCOUNT SETUP")
    print(f"{'='*60}\n")

    SETUP_DIR.mkdir(parents=True, exist_ok=True)

    # Check for Xcode
    print("  Checking prerequisites...")
    try:
        result = subprocess.run(
            ["xcodebuild", "-version"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            version = result.stdout.strip().split("\n")[0]
            print(f"  [+] Xcode: {version}")
        else:
            print("  [!] Xcode not found or not configured. Install from App Store.")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("  [!] xcodebuild not available. Install Xcode and command line tools.")

    # Check for Fastlane
    try:
        result = subprocess.run(
            ["fastlane", "--version"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            print(f"  [+] Fastlane: installed")
        else:
            print("  [!] Fastlane not found. Install: brew install fastlane")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("  [!] Fastlane not found. Install: brew install fastlane")

    # Check for Node/npm
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            print(f"  [+] Node.js: {result.stdout.strip()}")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("  [!] Node.js not found. Install: brew install node")

    # Check for CocoaPods
    try:
        result = subprocess.run(
            ["pod", "--version"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            print(f"  [+] CocoaPods: {result.stdout.strip()}")
        else:
            print("  [!] CocoaPods not found. Install: sudo gem install cocoapods")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("  [!] CocoaPods not found. Install: sudo gem install cocoapods")

    print()

    # Generate assets for all apps
    for app_key in APP_REGISTRY:
        generate_icon_specs(app_key)

    print("  Setup complete. Next: run --fastlane <app> for each app.\n")


# ---------------------------------------------------------------------------
# Enrollment guide
# ---------------------------------------------------------------------------

def print_enrollment_guide() -> None:
    """Print step-by-step Apple Developer enrollment guide."""
    print(f"\n{'='*60}")
    print("  APPLE DEVELOPER PROGRAM ENROLLMENT GUIDE")
    print(f"  Cost: $99/year")
    print(f"  URL:  https://developer.apple.com/programs/enroll/")
    print(f"{'='*60}\n")

    steps = [
        {
            "title": "Create or verify your Apple ID",
            "details": [
                "Go to: https://appleid.apple.com/",
                "Use a dedicated business email (not personal Gmail)",
                "Enable two-factor authentication (REQUIRED for developer program)",
                "Verify your phone number and email",
            ],
        },
        {
            "title": "Decide: Individual or Organization enrollment",
            "details": [
                "INDIVIDUAL ($99/year):",
                "  - Your legal name appears as seller on App Store",
                "  - Faster approval (usually 24-48 hours)",
                "  - Good for: solo developers, starting out",
                "",
                "ORGANIZATION ($99/year):",
                "  - Company name appears as seller on App Store",
                "  - Requires D-U-N-S number (free but takes 5-14 business days)",
                "  - Requires legal entity (LLC, Corp, etc.)",
                "  - Good for: professional appearance, multiple team members",
                "",
                "RECOMMENDATION: Start as Individual. Convert to Organization later.",
            ],
        },
        {
            "title": "Get a D-U-N-S number (Organization only)",
            "details": [
                "Go to: https://developer.apple.com/enroll/duns-lookup/",
                "Search for your company. If not found, request a free D-U-N-S number.",
                "Dun & Bradstreet will contact you within 5-14 business days.",
                "You need: legal business name, address, phone number, EIN/Tax ID",
                "SKIP this step if enrolling as Individual.",
            ],
        },
        {
            "title": "Start enrollment",
            "details": [
                "Go to: https://developer.apple.com/programs/enroll/",
                "Sign in with your Apple ID",
                "Select Individual or Organization",
                "Fill in your legal information exactly as it appears on government ID",
                "For Individual: Apple may require identity verification via iPhone or iPad",
            ],
        },
        {
            "title": "Pay the $99 annual fee",
            "details": [
                "Apple accepts credit/debit cards",
                "Payment is non-refundable",
                "Membership auto-renews annually (can cancel in settings)",
                "After payment, account activation takes up to 48 hours",
            ],
        },
        {
            "title": "Enroll in Apple Small Business Program (saves 15%)",
            "details": [
                "URL: https://developer.apple.com/programs/small-business/",
                "If your app revenue is under $1M/year, you qualify",
                "Commission drops from 30% to 15% on all App Store revenue",
                "Must be enrolled BEFORE your first sale to get the lower rate",
                "Re-qualifies annually based on previous year revenue",
            ],
        },
        {
            "title": "Set up App Store Connect",
            "details": [
                "Go to: https://appstoreconnect.apple.com/",
                "Accept the latest agreements (Paid Apps, Free Apps)",
                "Set up banking information for revenue payments",
                "Set up tax forms (W-9 for US developers)",
                "Create your first app listing (you can save as draft)",
            ],
        },
        {
            "title": "Create App Store Connect API key",
            "details": [
                "Go to: App Store Connect > Users and Access > Keys",
                "Generate an API key with Admin role",
                "Download the .p8 file (you can only download it ONCE)",
                "Save the Key ID and Issuer ID",
                "Store the .p8 file securely (needed for altool and Fastlane)",
                "NEVER commit the .p8 file to git",
            ],
        },
        {
            "title": "Configure Xcode signing",
            "details": [
                "Open Xcode > Settings > Accounts",
                "Add your Apple ID",
                "Your team should appear automatically",
                "Xcode will manage signing certificates and provisioning profiles",
                "For each app: set Automatically manage signing = YES",
            ],
        },
        {
            "title": "Create sandbox tester account",
            "details": [
                "App Store Connect > Users and Access > Sandbox Testers",
                "Create a new sandbox tester with a unique email",
                "On your test iPhone: Settings > App Store > Sandbox Account",
                "Sign in with the sandbox tester credentials",
                "This allows testing in-app purchases without real charges",
            ],
        },
    ]

    for i, step in enumerate(steps, 1):
        print(f"  STEP {i}: {step['title']}")
        print(f"  {'─'*50}")
        for detail in step["details"]:
            print(f"    {detail}")
        print()

    print(f"  TIMELINE ESTIMATE:")
    print(f"    Individual enrollment: 1-2 days")
    print(f"    Organization enrollment: 2-3 weeks (D-U-N-S delay)")
    print(f"    First app submission: 1-2 weeks after enrollment")
    print(f"    First app review: 24-48 hours (up to 1 week for first submission)")
    print(f"\n{'='*60}\n")

    # Save guide to file
    guide_file = safe_path(SETUP_DIR / "enrollment_guide.txt")
    SETUP_DIR.mkdir(parents=True, exist_ok=True)
    lines = []
    for i, step in enumerate(steps, 1):
        lines.append(f"STEP {i}: {step['title']}")
        for detail in step["details"]:
            lines.append(f"  {detail}")
        lines.append("")
    guide_file.write_text("\n".join(lines))
    print(f"  [+] Guide saved: {guide_file}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def resolve_app_key(name: str) -> Optional[str]:
    clean = name.lower().replace("-", "").replace("_", "").replace(" ", "")
    for key in APP_REGISTRY:
        if key == clean or key.startswith(clean) or clean in key:
            return key
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apple Developer Account Setup Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s --setup                Full setup (check prereqs + generate all icons)
  %(prog)s --icons focuslock      Generate icon specs and resize script
  %(prog)s --fastlane focuslock   Generate Fastlane config files
  %(prog)s --provisioning focuslock  Generate provisioning profile commands
  %(prog)s --guide                Print Apple Developer enrollment guide
  %(prog)s --all APP              Generate icons + fastlane + provisioning for APP
""",
    )

    parser.add_argument("--setup", action="store_true",
                        help="Full setup: check prerequisites, generate all icon specs")
    parser.add_argument("--icons", metavar="APP",
                        help="Generate icon specs and resize script for APP")
    parser.add_argument("--fastlane", metavar="APP",
                        help="Generate Fastlane configuration files for APP")
    parser.add_argument("--provisioning", metavar="APP",
                        help="Generate provisioning profile commands for APP")
    parser.add_argument("--guide", action="store_true",
                        help="Print Apple Developer enrollment guide ($99/year)")
    parser.add_argument("--all", metavar="APP",
                        help="Generate everything (icons + fastlane + provisioning) for APP")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    if args.setup:
        run_full_setup()

    if args.guide:
        print_enrollment_guide()

    if args.icons:
        app_key = resolve_app_key(args.icons)
        if not app_key:
            print(f"Unknown app: {args.icons}")
            print(f"Available: {', '.join(APP_REGISTRY.keys())}")
            sys.exit(1)
        generate_icon_specs(app_key)

    if args.fastlane:
        app_key = resolve_app_key(args.fastlane)
        if not app_key:
            print(f"Unknown app: {args.fastlane}")
            sys.exit(1)
        generate_fastlane_config(app_key)

    if args.provisioning:
        app_key = resolve_app_key(args.provisioning)
        if not app_key:
            print(f"Unknown app: {args.provisioning}")
            sys.exit(1)
        generate_provisioning_commands(app_key)

    if args.all:
        app_key = resolve_app_key(args.all)
        if not app_key:
            print(f"Unknown app: {args.all}")
            sys.exit(1)
        generate_icon_specs(app_key)
        generate_fastlane_config(app_key)
        generate_provisioning_commands(app_key)


if __name__ == "__main__":
    main()
