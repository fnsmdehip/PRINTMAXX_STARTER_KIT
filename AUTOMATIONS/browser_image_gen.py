#!/usr/bin/env python3
"""
Browser-based image generation via Gemini/ImageFX.

Extracts Chrome cookies, injects into Playwright Chromium, navigates to
gemini.google.com, generates images from prompts, downloads results.

No API key or billing needed. Uses your logged-in Chrome Google session.

Usage:
    python3 AUTOMATIONS/browser_image_gen.py                    # Generate all pending assets
    python3 AUTOMATIONS/browser_image_gen.py --max 5            # Generate up to 5 images
    python3 AUTOMATIONS/browser_image_gen.py --visible          # Show browser window
    python3 AUTOMATIONS/browser_image_gen.py --prompt "a cat"   # Single prompt test
"""

import argparse
import asyncio
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
AUTOMATIONS = BASE / "AUTOMATIONS"
APP_FACTORY = BASE / "MONEY_METHODS" / "APP_FACTORY"
ASSET_OUTPUT = APP_FACTORY / "generated_assets"
LOGS = AUTOMATIONS / "logs"
TODAY = datetime.now().strftime("%Y-%m-%d")

CHROME_USER_DATA = Path.home() / "Library" / "Application Support" / "Google" / "Chrome"
CHROME_KEY_FILE = AUTOMATIONS / ".chrome_cookie_key"

# Ensure dirs
ASSET_OUTPUT.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOGS / f"browser_image_gen_{TODAY}.log"

try:
    from Crypto.Cipher import AES
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def extract_chrome_cookies(domain_filter=".google.com"):
    """Extract and decrypt cookies from Chrome's cookie database."""
    if not HAS_CRYPTO:
        log("ERROR: pycryptodome not installed. pip3 install pycryptodome")
        return []

    cookie_db = CHROME_USER_DATA / "Default" / "Cookies"
    if not cookie_db.exists():
        log(f"ERROR: Chrome cookie DB not found at {cookie_db}")
        return []

    # Get decryption key from Keychain (or cache)
    keychain_pass = None
    if CHROME_KEY_FILE.exists():
        keychain_pass = CHROME_KEY_FILE.read_text().strip()

    if not keychain_pass:
        try:
            result = subprocess.run(
                ["security", "find-generic-password", "-s", "Chrome Safe Storage", "-w"],
                capture_output=True, text=True, timeout=15
            )
            keychain_pass = result.stdout.strip()
            if keychain_pass:
                CHROME_KEY_FILE.write_text(keychain_pass)
        except Exception as e:
            log(f"ERROR: Keychain access failed: {e}")
            return []

    if not keychain_pass:
        log("ERROR: Could not get Chrome Safe Storage key from Keychain")
        return []

    aes_key = hashlib.pbkdf2_hmac('sha1', keychain_pass.encode('utf-8'), b'saltysalt', 1003, dklen=16)

    # Copy DB to avoid locking issues
    temp_db = tempfile.mktemp(suffix=".db", prefix="chrome_cookies_")
    shutil.copy2(str(cookie_db), temp_db)
    journal = str(cookie_db) + "-journal"
    if Path(journal).exists():
        shutil.copy2(journal, temp_db + "-journal")

    cookies = []
    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        # Get all google-related cookies for auth
        cursor.execute(
            "SELECT host_key, name, path, encrypted_value, is_secure, is_httponly, "
            "expires_utc, samesite FROM cookies WHERE host_key LIKE ?",
            (f"%{domain_filter.lstrip('.')}%",),
        )

        for row in cursor.fetchall():
            host_key, name, path, encrypted_value, is_secure, is_httponly, expires_utc, samesite = row
            value = ""
            if encrypted_value and encrypted_value[:3] == b'v10':
                iv = b' ' * 16
                enc_data = encrypted_value[3:]
                if len(enc_data) % 16 != 0:
                    enc_data += b'\x00' * (16 - len(enc_data) % 16)
                try:
                    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
                    decrypted = cipher.decrypt(enc_data)
                    pad_len = decrypted[-1]
                    if 0 < pad_len <= 16:
                        decrypted = decrypted[:-pad_len]
                    else:
                        decrypted = decrypted.rstrip(b'\x00')
                    if len(decrypted) > 32:
                        value = decrypted[32:].decode('utf-8', errors='replace')
                    else:
                        value = decrypted.decode('utf-8', errors='replace')
                except Exception:
                    continue

            value = value.strip('\x00').strip()
            if not value:
                continue

            if expires_utc and expires_utc > 0:
                epoch_start = datetime(1601, 1, 1, tzinfo=timezone.utc)
                expires = (epoch_start + timedelta(microseconds=expires_utc)).timestamp()
            else:
                expires = -1

            if samesite in (-1, 0):
                ss = "None" if is_secure else "Lax"
            elif samesite == 1:
                ss = "Lax"
            else:
                ss = "Strict"

            cookie = {
                "name": name, "value": value, "domain": host_key,
                "path": path, "secure": bool(is_secure),
                "httpOnly": bool(is_httponly), "sameSite": ss,
            }
            if expires > 0:
                cookie["expires"] = expires
            cookies.append(cookie)

        conn.close()
    finally:
        Path(temp_db).unlink(missing_ok=True)
        Path(temp_db + "-journal").unlink(missing_ok=True)

    return cookies


def load_asset_prompts():
    """Load prompts from the asset generation prompts file."""
    prompts_file = APP_FACTORY / "APP_ASSET_GENERATION_PROMPTS.md"
    if not prompts_file.exists():
        return {}

    content = prompts_file.read_text()
    prompts = {}
    current_app = None
    current_section = None
    current_prompt = []
    in_code_block = False

    for line in content.splitlines():
        if line.startswith("## APP "):
            m = re.search(r"## APP \d+: (\w+)", line)
            if m:
                current_app = m.group(1).lower()
                prompts[current_app] = {}
        elif current_app and line.startswith("**") and "Variant" in line:
            if current_prompt and current_section:
                prompts[current_app][current_section] = "\n".join(current_prompt).strip()
            current_section = re.sub(r'[^a-z0-9_]', '_', line.lower().strip('*').strip())[:60]
            current_prompt = []
        elif line.strip() == "```":
            in_code_block = not in_code_block
        elif in_code_block and current_app and current_section:
            if not line.startswith("Platform:") and not line.startswith("Resolution:"):
                current_prompt.append(line)

    if current_prompt and current_app and current_section:
        prompts[current_app][current_section] = "\n".join(current_prompt).strip()

    return prompts


def get_pending_prompts(max_images=10):
    """Get prompts that haven't been generated today."""
    prompts = load_asset_prompts()
    pending = []

    for app_name, variants in prompts.items():
        app_dir = ASSET_OUTPUT / app_name
        app_dir.mkdir(parents=True, exist_ok=True)

        for variant_name, prompt_text in variants.items():
            if len(pending) >= max_images:
                return pending
            if not prompt_text or len(prompt_text) < 20:
                continue

            output_file = app_dir / f"{variant_name}_{TODAY}.png"
            if output_file.exists():
                continue

            # Extract just the main prompt line (strip metadata)
            clean_prompt = ""
            for line in prompt_text.splitlines():
                if line.startswith("Prompt:"):
                    clean_prompt = line.replace("Prompt:", "").strip().strip('"')
                    break
            if not clean_prompt:
                # Use first substantial line
                for line in prompt_text.splitlines():
                    line = line.strip()
                    if len(line) > 30 and not line.startswith("Negative") and not line.startswith("Style") and not line.startswith("Colors"):
                        clean_prompt = line.strip('"')
                        break
            if not clean_prompt:
                clean_prompt = prompt_text.splitlines()[0].strip('"')

            pending.append({
                "app": app_name,
                "variant": variant_name,
                "prompt": clean_prompt,
                "output": str(output_file),
            })

    return pending


async def generate_images(prompts_list, visible=False):
    """Generate images using Gemini web UI with Chrome cookies."""
    if not HAS_PLAYWRIGHT:
        log("ERROR: playwright not installed. pip3 install playwright")
        return []

    log("Extracting Chrome cookies for Google auth...")
    cookies = extract_chrome_cookies(".google.com")
    if not cookies:
        log("ERROR: No Google cookies found. Make sure you're logged into Google in Chrome.")
        return []
    log(f"  Got {len(cookies)} Google cookies")

    p = await async_playwright().start()
    browser = await p.chromium.launch(
        headless=not visible,
        args=["--no-first-run", "--disable-blink-features=AutomationControlled"],
    )
    context = await browser.new_context(
        viewport={'width': 1280, 'height': 900},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    )

    # Inject cookies
    injected = 0
    for cookie in cookies:
        try:
            await context.add_cookies([cookie])
            injected += 1
        except Exception:
            pass
    log(f"  Injected {injected}/{len(cookies)} cookies")

    page = await context.new_page()
    results = []

    try:
        # Navigate to Gemini
        log("Navigating to gemini.google.com...")
        await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(4)

        # Check if logged in
        url = page.url
        if "accounts.google.com" in url or "signin" in url.lower():
            log("ERROR: Not logged into Google. Log into Google in Chrome first.")
            await browser.close()
            await p.stop()
            return []

        log("Logged into Gemini")

        for i, item in enumerate(prompts_list):
            prompt = item["prompt"]
            output_path = Path(item["output"])
            log(f"\n[{i+1}/{len(prompts_list)}] Generating: {item['app']}/{item['variant']}")
            log(f"  Prompt: {prompt[:80]}...")

            try:
                # Find the input area and type the prompt
                # Gemini uses a contenteditable div or textarea
                input_sel = 'div[contenteditable="true"], textarea[aria-label*="prompt" i], .ql-editor, div.input-area-container [contenteditable], rich-textarea [contenteditable]'

                # Wait for input to be ready
                await page.wait_for_selector(input_sel, timeout=15000)
                await asyncio.sleep(1)

                input_el = await page.query_selector(input_sel)
                if not input_el:
                    log("  ERROR: Could not find input field")
                    continue

                # Prefix with "Generate an image: " to ensure image output
                full_prompt = f"Generate an image: {prompt}"

                await input_el.click()
                await asyncio.sleep(0.5)

                # Type the prompt
                await input_el.fill("")
                await page.keyboard.type(full_prompt, delay=10)
                await asyncio.sleep(0.5)

                # Submit - press Enter or click send button
                send_btn = await page.query_selector('button[aria-label*="Send" i], button[aria-label*="submit" i], button.send-button, mat-icon[data-mat-icon-name="send"]')
                if send_btn:
                    await send_btn.click()
                else:
                    await page.keyboard.press("Enter")

                log("  Waiting for image generation (up to 60s)...")

                # Wait for image to appear in response
                # Gemini renders images as <img> tags within response containers
                image_found = False
                for attempt in range(30):  # 30 * 2s = 60s max
                    await asyncio.sleep(2)

                    # Look for generated images in the response
                    images = await page.query_selector_all('img[src*="blob:"], img[src*="lh3.googleusercontent"], img[src*="encrypted"], .response-container img, model-response img')

                    # Filter to new images (not UI elements)
                    for img in images:
                        src = await img.get_attribute("src") or ""
                        alt = await img.get_attribute("alt") or ""
                        width = await img.get_attribute("width") or ""
                        # Skip tiny UI icons
                        bounding = await img.bounding_box()
                        if bounding and bounding["width"] > 100 and bounding["height"] > 100:
                            if "blob:" in src or "lh3" in src or "encrypted" in src:
                                # Found a generated image
                                image_found = True

                                # Try to download via right-click -> save / screenshot
                                output_path.parent.mkdir(parents=True, exist_ok=True)

                                # Method 1: Screenshot the image element
                                await img.screenshot(path=str(output_path))
                                log(f"  Captured image via screenshot: {output_path.name}")

                                results.append({
                                    "app": item["app"],
                                    "variant": item["variant"],
                                    "file": str(output_path.relative_to(BASE)),
                                    "size_kb": output_path.stat().st_size // 1024,
                                })
                                break

                    if image_found:
                        break

                    # Check for error messages
                    error_els = await page.query_selector_all('.error-message, [class*="error"]')
                    for err_el in error_els:
                        err_text = await err_el.text_content()
                        if err_text and ("limit" in err_text.lower() or "error" in err_text.lower()):
                            log(f"  ERROR from Gemini: {err_text[:100]}")
                            break

                if not image_found:
                    log("  WARN: No image generated after 60s timeout")

                    # Take a debug screenshot
                    debug_path = LOGS / f"debug_gemini_{i}_{TODAY}.png"
                    await page.screenshot(path=str(debug_path))
                    log(f"  Debug screenshot saved: {debug_path.name}")

                # Start new chat for next prompt to avoid context buildup
                if i < len(prompts_list) - 1:
                    await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=20000)
                    await asyncio.sleep(3)

            except Exception as e:
                log(f"  ERROR: {e}")
                # Debug screenshot
                try:
                    debug_path = LOGS / f"debug_gemini_err_{i}_{TODAY}.png"
                    await page.screenshot(path=str(debug_path))
                except Exception:
                    pass
                continue

    finally:
        await browser.close()
        await p.stop()

    return results


async def run_single_prompt(prompt, visible=False):
    """Generate a single image from a prompt (test mode)."""
    output = ASSET_OUTPUT / f"test_{TODAY}.png"
    items = [{"app": "test", "variant": "test", "prompt": prompt, "output": str(output)}]
    results = await generate_images(items, visible=visible)
    return results


async def main():
    parser = argparse.ArgumentParser(description="Browser-based image generation via Gemini")
    parser.add_argument("--max", type=int, default=10, help="Max images to generate")
    parser.add_argument("--visible", action="store_true", help="Show browser window")
    parser.add_argument("--prompt", type=str, help="Single prompt test mode")
    parser.add_argument("--status", action="store_true", help="Show pending prompts")
    args = parser.parse_args()

    if args.status:
        pending = get_pending_prompts(max_images=999)
        print(f"\n{len(pending)} images pending generation:")
        for i, p in enumerate(pending[:20], 1):
            print(f"  {i}. {p['app']}/{p['variant']}")
        if len(pending) > 20:
            print(f"  ... and {len(pending) - 20} more")
        return

    if args.prompt:
        log(f"Single prompt test: {args.prompt[:60]}...")
        results = await run_single_prompt(args.prompt, visible=args.visible)
        if results:
            log(f"Success: {results[0]['file']}")
        else:
            log("No image generated")
        return

    # Generate pending assets
    pending = get_pending_prompts(max_images=args.max)
    if not pending:
        log("All assets already generated today")
        return

    log(f"Generating {len(pending)} images via Chrome browser...")
    results = await generate_images(pending, visible=args.visible)
    log(f"\nDone: {len(results)}/{len(pending)} images generated")

    for r in results:
        log(f"  {r['app']}/{r['variant']}: {r['file']} ({r['size_kb']}KB)")


if __name__ == "__main__":
    asyncio.run(main())
