#!/usr/bin/env python3
"""
Asset Generator - Bulk image generation via Gemini (Nano Banana)

Automates asset creation by:
1. Loading prompts from PROMPT_LIBRARY.md or custom prompt lists
2. Navigating to Gemini
3. Submitting prompts and downloading results
4. Organizing outputs into structured folders

Usage:
    python asset_generator.py --app prayerlock --type icons
    python asset_generator.py --prompts custom_prompts.txt --output ./my_assets
    python asset_generator.py --batch all --dry-run
"""

import os
import sys
import time
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

try:
    from playwright.sync_api import sync_playwright, Page, Browser
except ImportError:
    print("Playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)


# ============================================================================
# Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
PROMPT_LIBRARY = PROJECT_ROOT / "MONEY_METHODS/APP_FACTORY/assets/PROMPT_LIBRARY.md"
DEFAULT_OUTPUT = PROJECT_ROOT / "MONEY_METHODS/APP_FACTORY/assets/generated"
GEMINI_URL = "https://gemini.google.com/app"

# Timing configurations (adjust based on your connection speed)
WAIT_FOR_LOGIN = 5  # seconds to wait for login check
WAIT_FOR_GENERATION = 45  # seconds to wait for image generation
WAIT_BETWEEN_PROMPTS = 3  # seconds between prompts to avoid rate limits

# App configurations
APPS = {
    "prayerlock": {
        "name": "PrayerLock",
        "colors": {"primary": "#1a1a2e", "secondary": "#4c1d95", "accent": "#d4af37"}
    },
    "walktounlock": {
        "name": "WalkToUnlock",
        "colors": {"primary": "#10b981", "secondary": "#14b8a6", "accent": "#ffffff"}
    },
    "studylock": {
        "name": "StudyLock",
        "colors": {"primary": "#3730a3", "secondary": "#1e3a5f", "accent": "#60a5fa"}
    },
    "promptvault": {
        "name": "PromptVault",
        "colors": {"primary": "#3b82f6", "secondary": "#8b5cf6", "accent": "#22d3d8"}
    },
    "dailyanchor": {
        "name": "DailyAnchor",
        "colors": {"primary": "#1e40af", "secondary": "#f97316", "accent": "#fcd34d"}
    },
    "femfit": {
        "name": "FemFit",
        "colors": {"primary": "#f472b6", "secondary": "#ec4899", "accent": "#c4b5fd"}
    },
    "dailydevotion": {
        "name": "DailyDevotion",
        "colors": {"primary": "#1e3a8a", "secondary": "#7f1d1d", "accent": "#fef3c7"}
    }
}

ASSET_TYPES = ["icons", "mascots", "screenshots", "marketing"]


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Prompt:
    """Represents a single generation prompt."""
    app: str
    asset_type: str
    variant: str
    text: str
    filename: str


@dataclass
class GenerationResult:
    """Result of a single generation attempt."""
    prompt: Prompt
    success: bool
    output_path: Optional[str]
    error: Optional[str]
    timestamp: str


# ============================================================================
# Prompt Parser
# ============================================================================

def parse_prompt_library(filepath: Path) -> dict:
    """
    Parse PROMPT_LIBRARY.md and extract prompts organized by app and type.

    Returns:
        dict: Nested structure {app: {asset_type: [prompts]}}
    """
    if not filepath.exists():
        print(f"Warning: Prompt library not found at {filepath}")
        return {}

    content = filepath.read_text()
    prompts = {}

    # Extract code blocks (prompts are in ``` blocks)
    code_block_pattern = r'```\n(.*?)```'

    current_app = None
    current_type = None
    current_variant = None

    lines = content.split('\n')
    in_code_block = False
    current_block = []

    for i, line in enumerate(lines):
        # Detect app sections
        if "### " in line and "Icon" in line:
            for app_key in APPS:
                if APPS[app_key]["name"] in line:
                    current_app = app_key
                    current_type = "icons"
                    break

        if "### " in line and "Character" in line:
            current_type = "mascots"
            # Detect which mascot
            if "Angel" in line:
                current_app = "prayerlock"
            elif "Dog" in line:
                current_app = "walktounlock"
            elif "Owl" in line:
                current_app = "studylock"
            elif "Cat" in line:
                current_app = "femfit"
            elif "Dove" in line:
                current_app = "dailydevotion"

        if "### " in line and "Template" in line:
            current_type = "screenshots"
            current_app = "generic"

        if "### " in line and ("Background" in line or "Ad" in line or "Hero" in line or "Email" in line):
            current_type = "marketing"
            current_app = "generic"

        # Detect variant names
        if line.startswith("**") and ":" in line:
            variant_match = re.match(r'\*\*(.+?)(?:\s*\(|:|\*\*)', line)
            if variant_match:
                current_variant = variant_match.group(1).lower().replace(" ", "_")

        # Track code blocks
        if line.strip() == '```':
            if in_code_block:
                # End of code block - save prompt
                if current_app and current_type and current_block:
                    prompt_text = '\n'.join(current_block).strip()
                    if prompt_text and not prompt_text.startswith(('python', 'bash', '[')):
                        if current_app not in prompts:
                            prompts[current_app] = {}
                        if current_type not in prompts[current_app]:
                            prompts[current_app][current_type] = []

                        variant = current_variant or f"v{len(prompts[current_app][current_type]) + 1}"
                        filename = f"{current_app}_{current_type[:-1]}_{variant}"

                        prompts[current_app][current_type].append(Prompt(
                            app=current_app,
                            asset_type=current_type,
                            variant=variant,
                            text=prompt_text,
                            filename=filename
                        ))

                current_block = []
                in_code_block = False
            else:
                in_code_block = True
        elif in_code_block:
            current_block.append(line)

    return prompts


def load_custom_prompts(filepath: Path) -> list:
    """Load prompts from a simple text file (one prompt per paragraph)."""
    if not filepath.exists():
        raise FileNotFoundError(f"Custom prompt file not found: {filepath}")

    content = filepath.read_text()
    paragraphs = content.split('\n\n')

    prompts = []
    for i, para in enumerate(paragraphs):
        para = para.strip()
        if para and not para.startswith('#'):
            prompts.append(Prompt(
                app="custom",
                asset_type="custom",
                variant=f"v{i+1}",
                text=para,
                filename=f"custom_asset_{i+1}"
            ))

    return prompts


# ============================================================================
# Browser Automation
# ============================================================================

class GeminiGenerator:
    """Handles browser automation for Gemini image generation."""

    def __init__(self, headless: bool = False, output_dir: Path = DEFAULT_OUTPUT):
        self.headless = headless
        self.output_dir = output_dir
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.results: list = []

    def setup(self):
        """Initialize browser and navigate to Gemini."""
        print("Starting browser...")
        self.playwright = sync_playwright().start()

        # Use persistent context to maintain login
        user_data_dir = Path.home() / ".gemini_generator_profile"
        user_data_dir.mkdir(exist_ok=True)

        self.browser = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=self.headless,
            viewport={"width": 1280, "height": 900}
        )

        self.page = self.browser.new_page()
        self.page.goto(GEMINI_URL)

        print(f"Navigated to {GEMINI_URL}")
        print("Waiting for page to load...")
        time.sleep(WAIT_FOR_LOGIN)

        # Check if logged in
        if not self._check_logged_in():
            print("\n" + "="*60)
            print("Please log in to your Google account in the browser window.")
            print("Press Enter here once you're logged in...")
            print("="*60)
            input()
            time.sleep(2)

    def _check_logged_in(self) -> bool:
        """Check if user is logged into Gemini."""
        try:
            # Look for the prompt input which only appears when logged in
            prompt_input = self.page.locator('div[contenteditable="true"]').first
            return prompt_input.is_visible(timeout=3000)
        except:
            return False

    def generate(self, prompt: Prompt) -> GenerationResult:
        """Generate a single image from a prompt."""
        timestamp = datetime.now().isoformat()

        try:
            # Find and clear the prompt input
            prompt_input = self.page.locator('div[contenteditable="true"]').first
            prompt_input.click()

            # Clear existing text
            self.page.keyboard.press("Control+a")
            self.page.keyboard.press("Backspace")

            # Type the prompt
            prompt_input.fill(prompt.text)
            time.sleep(0.5)

            # Submit
            self.page.keyboard.press("Enter")

            print(f"  Submitted prompt, waiting for generation...")

            # Wait for image generation (look for image elements in response)
            time.sleep(WAIT_FOR_GENERATION)

            # Try to find and download the generated image
            output_path = self._download_image(prompt)

            if output_path:
                return GenerationResult(
                    prompt=prompt,
                    success=True,
                    output_path=str(output_path),
                    error=None,
                    timestamp=timestamp
                )
            else:
                return GenerationResult(
                    prompt=prompt,
                    success=False,
                    output_path=None,
                    error="Could not locate generated image",
                    timestamp=timestamp
                )

        except Exception as e:
            return GenerationResult(
                prompt=prompt,
                success=False,
                output_path=None,
                error=str(e),
                timestamp=timestamp
            )

    def _download_image(self, prompt: Prompt) -> Optional[Path]:
        """Attempt to download the most recently generated image."""
        try:
            # Create output directory structure
            output_subdir = self.output_dir / prompt.app / prompt.asset_type
            output_subdir.mkdir(parents=True, exist_ok=True)

            output_path = output_subdir / f"{prompt.filename}.png"

            # Find image elements in the response
            # Gemini's UI structure may vary - these are common patterns
            image_selectors = [
                'img[src*="generated"]',
                'img[src*="blob:"]',
                'div[data-image] img',
                'img[alt*="Generated"]',
                '.response-container img',
            ]

            for selector in image_selectors:
                images = self.page.locator(selector).all()
                if images:
                    # Take the last image (most recent generation)
                    img = images[-1]

                    # Try right-click download
                    img.click(button="right")
                    time.sleep(0.5)

                    # Look for "Save image as" option
                    save_option = self.page.locator('text="Save image as"').first
                    if save_option.is_visible(timeout=2000):
                        save_option.click()
                        time.sleep(1)

                        # Handle file dialog (type filename and save)
                        self.page.keyboard.type(str(output_path))
                        self.page.keyboard.press("Enter")
                        time.sleep(2)

                        if output_path.exists():
                            return output_path

            # Alternative: screenshot the image element
            for selector in image_selectors:
                images = self.page.locator(selector).all()
                if images:
                    img = images[-1]
                    img.screenshot(path=str(output_path))
                    if output_path.exists():
                        print(f"  Saved via screenshot: {output_path}")
                        return output_path

            return None

        except Exception as e:
            print(f"  Download error: {e}")
            return None

    def batch_generate(self, prompts: list, dry_run: bool = False):
        """Generate images for a batch of prompts."""
        total = len(prompts)
        print(f"\nStarting batch generation of {total} assets...")

        if dry_run:
            print("\n[DRY RUN MODE - No actual generation]")
            for i, prompt in enumerate(prompts, 1):
                print(f"\n[{i}/{total}] Would generate:")
                print(f"  App: {prompt.app}")
                print(f"  Type: {prompt.asset_type}")
                print(f"  Variant: {prompt.variant}")
                print(f"  Filename: {prompt.filename}.png")
                print(f"  Prompt preview: {prompt.text[:100]}...")
            return

        self.setup()

        for i, prompt in enumerate(prompts, 1):
            print(f"\n[{i}/{total}] Generating: {prompt.filename}")

            result = self.generate(prompt)
            self.results.append(result)

            if result.success:
                print(f"  Success: {result.output_path}")
            else:
                print(f"  Failed: {result.error}")

            # Wait between prompts to avoid rate limiting
            if i < total:
                print(f"  Waiting {WAIT_BETWEEN_PROMPTS}s before next prompt...")
                time.sleep(WAIT_BETWEEN_PROMPTS)

        self._save_results()
        self.cleanup()

    def _save_results(self):
        """Save generation results to a log file."""
        log_path = self.output_dir / "generation_log.json"

        results_data = []
        for r in self.results:
            results_data.append({
                "app": r.prompt.app,
                "type": r.prompt.asset_type,
                "variant": r.prompt.variant,
                "filename": r.prompt.filename,
                "success": r.success,
                "output_path": r.output_path,
                "error": r.error,
                "timestamp": r.timestamp
            })

        # Append to existing log or create new
        existing = []
        if log_path.exists():
            try:
                existing = json.loads(log_path.read_text())
            except:
                pass

        existing.extend(results_data)
        log_path.write_text(json.dumps(existing, indent=2))
        print(f"\nResults logged to: {log_path}")

        # Print summary
        success = sum(1 for r in self.results if r.success)
        failed = len(self.results) - success
        print(f"\nGeneration Summary:")
        print(f"  Successful: {success}")
        print(f"  Failed: {failed}")

    def cleanup(self):
        """Close browser and cleanup."""
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()
        print("\nBrowser closed.")


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Bulk asset generation via Gemini (Nano Banana)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all icons for PrayerLock
  python asset_generator.py --app prayerlock --type icons

  # Generate mascots for all apps
  python asset_generator.py --type mascots

  # Dry run to preview what would be generated
  python asset_generator.py --batch all --dry-run

  # Use custom prompts file
  python asset_generator.py --prompts my_prompts.txt --output ./custom_assets

  # Generate everything
  python asset_generator.py --batch all
        """
    )

    parser.add_argument(
        "--app",
        choices=list(APPS.keys()) + ["all", "generic"],
        help="App to generate assets for"
    )

    parser.add_argument(
        "--type",
        choices=ASSET_TYPES + ["all"],
        help="Type of assets to generate"
    )

    parser.add_argument(
        "--batch",
        choices=["all"],
        help="Run batch generation for all apps and types"
    )

    parser.add_argument(
        "--prompts",
        type=Path,
        help="Path to custom prompts file"
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output directory (default: {DEFAULT_OUTPUT})"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be generated without actually running"
    )

    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (not recommended - need to see images)"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List available prompts from the library"
    )

    args = parser.parse_args()

    # Parse the prompt library
    library = parse_prompt_library(PROMPT_LIBRARY)

    # Handle --list
    if args.list:
        print("\nAvailable prompts in library:")
        print("="*50)
        for app, types in library.items():
            print(f"\n{APPS.get(app, {}).get('name', app.upper())}:")
            for asset_type, prompts in types.items():
                print(f"  {asset_type}: {len(prompts)} prompts")
                for p in prompts:
                    print(f"    - {p.variant}")
        return

    # Collect prompts to generate
    prompts_to_generate = []

    if args.prompts:
        # Custom prompts file
        prompts_to_generate = load_custom_prompts(args.prompts)

    elif args.batch == "all":
        # All prompts from library
        for app, types in library.items():
            for asset_type, prompts in types.items():
                prompts_to_generate.extend(prompts)

    elif args.app and args.type:
        # Specific app and type
        apps = list(APPS.keys()) if args.app == "all" else [args.app]
        types = ASSET_TYPES if args.type == "all" else [args.type]

        for app in apps:
            if app in library:
                for asset_type in types:
                    if asset_type in library[app]:
                        prompts_to_generate.extend(library[app][asset_type])

    elif args.app:
        # All types for specific app
        if args.app in library:
            for asset_type, prompts in library[args.app].items():
                prompts_to_generate.extend(prompts)

    elif args.type:
        # Specific type across all apps
        for app, types in library.items():
            if args.type in types:
                prompts_to_generate.extend(types[args.type])

    else:
        parser.print_help()
        return

    if not prompts_to_generate:
        print("No prompts found matching criteria.")
        return

    # Run generation
    generator = GeminiGenerator(
        headless=args.headless,
        output_dir=args.output
    )

    generator.batch_generate(prompts_to_generate, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
