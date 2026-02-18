#!/usr/bin/env python3
"""
Screenshot Generator - App Store Screenshot Automation
======================================================
Generate App Store/Play Store screenshots from mobile apps.

Features:
- Multiple device frame sizes (iPhone, iPad, Android phones/tablets)
- Automated screenshot capture at key screens
- Device frame overlays
- Text overlays for marketing
- Batch generation for multiple devices
- Export to App Store Connect specs

Usage:
    from screenshot_generator import ScreenshotGenerator

    gen = ScreenshotGenerator(platform="ios")
    gen.generate_screenshots("com.printmaxx.aiclarity", screens=[
        {"name": "home", "action": "wait"},
        {"name": "results", "deep_link": "myapp://results/123"}
    ])

CLI:
    python screenshot_generator.py --platform ios --app com.printmaxx.aiclarity
    python screenshot_generator.py --config screenshots.json
"""

import os
import sys
import json
import time
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field

# Configure logging
LOG_DIR = Path(__file__).parent.parent.parent / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "screenshot_generator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("screenshot_generator")


# App Store screenshot specifications
APPSTORE_SPECS = {
    # iPhone
    "iphone_6_7_inch": {
        "name": "iPhone 6.7 inch Display",
        "devices": ["iPhone 15 Pro Max", "iPhone 15 Plus", "iPhone 14 Pro Max"],
        "resolution": (1290, 2796),
        "ppi": 460,
        "required": True,
    },
    "iphone_6_5_inch": {
        "name": "iPhone 6.5 inch Display",
        "devices": ["iPhone 11 Pro Max", "iPhone XS Max"],
        "resolution": (1242, 2688),
        "ppi": 458,
        "required": True,
    },
    "iphone_5_5_inch": {
        "name": "iPhone 5.5 inch Display",
        "devices": ["iPhone 8 Plus", "iPhone 7 Plus"],
        "resolution": (1242, 2208),
        "ppi": 401,
        "required": True,
    },
    # iPad
    "ipad_12_9_inch": {
        "name": "iPad Pro 12.9 inch Display",
        "devices": ["iPad Pro 12.9-inch"],
        "resolution": (2048, 2732),
        "ppi": 264,
        "required": True,
    },
    "ipad_11_inch": {
        "name": "iPad Pro 11 inch Display",
        "devices": ["iPad Pro 11-inch"],
        "resolution": (1668, 2388),
        "ppi": 264,
        "required": False,
    },
}

PLAYSTORE_SPECS = {
    "phone": {
        "name": "Phone Screenshot",
        "min_resolution": (320, 320),
        "max_resolution": (3840, 3840),
        "aspect_ratios": ["16:9", "9:16"],
        "required": True,
    },
    "tablet_7_inch": {
        "name": "7-inch Tablet",
        "resolution": (1200, 1920),
        "required": False,
    },
    "tablet_10_inch": {
        "name": "10-inch Tablet",
        "resolution": (1600, 2560),
        "required": False,
    },
}


@dataclass
class ScreenshotConfig:
    """Configuration for a screenshot capture."""
    name: str
    action: str = "wait"  # wait, tap, scroll, deep_link
    deep_link: Optional[str] = None
    tap_coordinates: Optional[Tuple[int, int]] = None
    scroll_direction: Optional[str] = None
    wait_seconds: float = 2.0
    overlay_text: Optional[str] = None
    overlay_position: str = "bottom"  # top, bottom, center


@dataclass
class GeneratedScreenshot:
    """Generated screenshot metadata."""
    name: str
    device: str
    resolution: Tuple[int, int]
    path: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    overlay_applied: bool = False


class ScreenshotGenerator:
    """Generate App Store screenshots."""

    def __init__(self, platform: str = "ios"):
        """
        Initialize screenshot generator.

        Args:
            platform: 'ios' or 'android'
        """
        self.platform = platform.lower()
        self.output_dir = Path(__file__).parent.parent / "app_store_screenshots"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Import controller from app_test_runner
        from app_test_runner import SimulatorController, EmulatorController

        if self.platform == "ios":
            self.controller = SimulatorController()
            self.specs = APPSTORE_SPECS
        elif self.platform == "android":
            self.controller = EmulatorController()
            self.specs = PLAYSTORE_SPECS
        else:
            raise ValueError(f"Unknown platform: {platform}")

        self.generated: List[GeneratedScreenshot] = []
        logger.info(f"Screenshot generator initialized for {platform}")

    def _get_available_devices(self) -> List[Dict[str, str]]:
        """Get list of available simulator/emulator devices."""
        return self.controller.list_devices()

    def _find_device_for_spec(self, spec_name: str) -> Optional[str]:
        """Find a device matching the spec."""
        spec = self.specs.get(spec_name, {})
        target_devices = spec.get("devices", [])
        available = self._get_available_devices()

        for target in target_devices:
            for device in available:
                if target.lower() in device.get("name", "").lower():
                    return device.get("udid") or device.get("id")
        return None

    def _capture_screenshot(self, name: str, device_spec: str = None) -> Optional[str]:
        """Capture a single screenshot."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if device_spec:
            filename = f"{name}_{device_spec}_{timestamp}.png"
        else:
            filename = f"{name}_{timestamp}.png"

        output_path = str(self.output_dir / filename)

        if self.controller.take_screenshot(output_path):
            return output_path
        return None

    def _execute_action(self, config: ScreenshotConfig) -> None:
        """Execute the action before taking screenshot."""
        if config.action == "wait":
            time.sleep(config.wait_seconds)

        elif config.action == "deep_link" and config.deep_link:
            self.controller.open_url(config.deep_link)
            time.sleep(config.wait_seconds)

        elif config.action == "tap" and config.tap_coordinates:
            # For iOS, use simctl tap (limited support)
            # For Android, use adb input tap
            x, y = config.tap_coordinates
            if self.platform == "android":
                device_id = self.controller.device_id
                if device_id:
                    subprocess.run(
                        ["adb", "-s", device_id, "shell", "input", "tap", str(x), str(y)],
                        capture_output=True
                    )
            time.sleep(config.wait_seconds)

        elif config.action == "scroll" and config.scroll_direction:
            # Scroll simulation
            if self.platform == "android":
                device_id = self.controller.device_id
                if device_id:
                    if config.scroll_direction == "down":
                        subprocess.run(
                            ["adb", "-s", device_id, "shell", "input", "swipe",
                             "500", "1500", "500", "500", "300"],
                            capture_output=True
                        )
                    elif config.scroll_direction == "up":
                        subprocess.run(
                            ["adb", "-s", device_id, "shell", "input", "swipe",
                             "500", "500", "500", "1500", "300"],
                            capture_output=True
                        )
            time.sleep(config.wait_seconds)

    def generate_screenshot(
        self,
        app_id: str,
        config: ScreenshotConfig,
        device_spec: str = None
    ) -> Optional[GeneratedScreenshot]:
        """
        Generate a single screenshot.

        Args:
            app_id: App bundle ID or package name
            config: Screenshot configuration
            device_spec: Optional device specification name
        """
        # Execute action
        self._execute_action(config)

        # Capture screenshot
        path = self._capture_screenshot(config.name, device_spec)
        if not path:
            logger.error(f"Failed to capture screenshot: {config.name}")
            return None

        # Get resolution
        resolution = self._get_image_resolution(path)

        screenshot = GeneratedScreenshot(
            name=config.name,
            device=device_spec or "default",
            resolution=resolution,
            path=path
        )

        # Apply overlay if specified
        if config.overlay_text:
            self._apply_overlay(path, config.overlay_text, config.overlay_position)
            screenshot.overlay_applied = True

        self.generated.append(screenshot)
        logger.info(f"Generated screenshot: {config.name} -> {path}")

        return screenshot

    def _get_image_resolution(self, image_path: str) -> Tuple[int, int]:
        """Get image resolution using sips (macOS) or identify."""
        try:
            # Try sips on macOS
            result = subprocess.run(
                ["sips", "-g", "pixelWidth", "-g", "pixelHeight", image_path],
                capture_output=True,
                text=True
            )
            output = result.stdout
            width = int(output.split("pixelWidth:")[1].split()[0])
            height = int(output.split("pixelHeight:")[1].split()[0])
            return (width, height)
        except:
            pass

        try:
            # Try ImageMagick identify
            result = subprocess.run(
                ["identify", "-format", "%wx%h", image_path],
                capture_output=True,
                text=True
            )
            parts = result.stdout.strip().split("x")
            return (int(parts[0]), int(parts[1]))
        except:
            pass

        return (0, 0)

    def _apply_overlay(self, image_path: str, text: str, position: str) -> bool:
        """Apply text overlay to screenshot."""
        try:
            # Use ImageMagick if available
            gravity = {
                "top": "North",
                "bottom": "South",
                "center": "Center"
            }.get(position, "South")

            output_path = image_path.replace(".png", "_overlay.png")

            subprocess.run([
                "convert", image_path,
                "-gravity", gravity,
                "-pointsize", "60",
                "-fill", "white",
                "-stroke", "black",
                "-strokewidth", "2",
                "-annotate", "+0+50", text,
                output_path
            ], capture_output=True, check=True)

            # Replace original with overlay version
            os.replace(output_path, image_path)
            logger.info(f"Applied overlay to: {image_path}")
            return True

        except FileNotFoundError:
            logger.warning("ImageMagick not installed - skipping overlay")
            return False
        except Exception as e:
            logger.error(f"Failed to apply overlay: {e}")
            return False

    def generate_screenshots(
        self,
        app_id: str,
        screens: List[Dict[str, Any]],
        device_specs: List[str] = None
    ) -> List[GeneratedScreenshot]:
        """
        Generate screenshots for multiple screens.

        Args:
            app_id: App bundle ID or package name
            screens: List of screen configurations
            device_specs: List of device specifications to capture for

        Returns:
            List of generated screenshots
        """
        # Convert dicts to ScreenshotConfig objects
        configs = []
        for screen in screens:
            configs.append(ScreenshotConfig(**screen))

        # Use default device specs if not specified
        if device_specs is None:
            device_specs = [None]  # Use current device

        results = []

        # Launch app first
        self.controller.launch_app(app_id)
        time.sleep(3)

        for spec in device_specs:
            logger.info(f"Generating screenshots for spec: {spec or 'default'}")

            for config in configs:
                result = self.generate_screenshot(app_id, config, spec)
                if result:
                    results.append(result)
                time.sleep(1)

            # Relaunch app for next device if switching
            if len(device_specs) > 1:
                self.controller.terminate_app(app_id)
                time.sleep(1)
                self.controller.launch_app(app_id)
                time.sleep(3)

        return results

    def generate_for_all_required_specs(
        self,
        app_id: str,
        screens: List[Dict[str, Any]]
    ) -> Dict[str, List[GeneratedScreenshot]]:
        """
        Generate screenshots for all required App Store specs.

        Args:
            app_id: App bundle ID or package name
            screens: List of screen configurations

        Returns:
            Dict mapping spec name to list of screenshots
        """
        results = {}

        for spec_name, spec in self.specs.items():
            if not spec.get("required", False):
                continue

            logger.info(f"Generating for spec: {spec_name}")

            # Find matching device
            device_id = self._find_device_for_spec(spec_name)
            if not device_id:
                logger.warning(f"No device found for spec: {spec_name}")
                continue

            # Boot device if needed (iOS)
            if self.platform == "ios":
                self.controller.boot_device(device_id)
                time.sleep(2)

            # Generate screenshots
            screenshots = self.generate_screenshots(app_id, screens, [spec_name])
            results[spec_name] = screenshots

        return results

    def export_manifest(self, output_path: str = None) -> str:
        """Export screenshot manifest for upload."""
        if output_path is None:
            output_path = str(self.output_dir / "manifest.json")

        manifest = {
            "platform": self.platform,
            "generated_at": datetime.now().isoformat(),
            "screenshots": []
        }

        for screenshot in self.generated:
            manifest["screenshots"].append({
                "name": screenshot.name,
                "device": screenshot.device,
                "resolution": screenshot.resolution,
                "path": screenshot.path,
                "timestamp": screenshot.timestamp,
                "overlay_applied": screenshot.overlay_applied
            })

        with open(output_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        logger.info(f"Manifest exported: {output_path}")
        return output_path

    def validate_screenshots(self) -> Dict[str, Any]:
        """Validate generated screenshots against store requirements."""
        validation = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "coverage": {}
        }

        # Check each required spec
        for spec_name, spec in self.specs.items():
            if not spec.get("required", False):
                continue

            matching = [s for s in self.generated if s.device == spec_name]
            if not matching:
                validation["coverage"][spec_name] = "missing"
                if spec.get("required"):
                    validation["errors"].append(f"Missing required screenshots for: {spec_name}")
                    validation["valid"] = False
            else:
                validation["coverage"][spec_name] = len(matching)

                # Check resolution
                required_res = spec.get("resolution")
                if required_res:
                    for screenshot in matching:
                        if screenshot.resolution != required_res:
                            validation["warnings"].append(
                                f"{screenshot.name}: Resolution {screenshot.resolution} "
                                f"doesn't match required {required_res}"
                            )

        return validation


# CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="App Store Screenshot Generator")
    parser.add_argument("--platform", "-p", choices=["ios", "android"], default="ios",
                        help="Target platform")
    parser.add_argument("--app", "-a", help="App bundle ID or package name")
    parser.add_argument("--config", "-c", help="JSON config file with screen definitions")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--all-specs", action="store_true",
                        help="Generate for all required App Store specs")
    parser.add_argument("--validate", action="store_true",
                        help="Validate generated screenshots")

    args = parser.parse_args()

    generator = ScreenshotGenerator(platform=args.platform)

    if args.output:
        generator.output_dir = Path(args.output)
        generator.output_dir.mkdir(parents=True, exist_ok=True)

    # Load screen definitions
    if args.config:
        with open(args.config, 'r') as f:
            config_data = json.load(f)
        screens = config_data.get("screens", [])
        app_id = config_data.get("app_id") or args.app
    else:
        # Default screens
        screens = [
            {"name": "home", "action": "wait", "wait_seconds": 3},
            {"name": "feature_1", "action": "scroll", "scroll_direction": "down"},
        ]
        app_id = args.app

    if not app_id:
        print("Error: App ID required (--app or in config file)")
        sys.exit(1)

    # Generate screenshots
    if args.all_specs:
        results = generator.generate_for_all_required_specs(app_id, screens)
        print(f"\nGenerated screenshots for {len(results)} device specs")
    else:
        results = generator.generate_screenshots(app_id, screens)
        print(f"\nGenerated {len(results)} screenshots")

    # Export manifest
    manifest_path = generator.export_manifest()
    print(f"Manifest: {manifest_path}")

    # Validate if requested
    if args.validate:
        validation = generator.validate_screenshots()
        print(f"\nValidation:")
        print(f"  Valid: {validation['valid']}")
        if validation['warnings']:
            print(f"  Warnings: {len(validation['warnings'])}")
            for w in validation['warnings'][:5]:
                print(f"    - {w}")
        if validation['errors']:
            print(f"  Errors: {len(validation['errors'])}")
            for e in validation['errors']:
                print(f"    - {e}")

    print(f"\nScreenshots saved to: {generator.output_dir}")
