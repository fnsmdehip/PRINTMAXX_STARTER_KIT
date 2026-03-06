#!/usr/bin/env python3
"""
PRINTMAXX Autonomous Production Factory

The missing execution layer. This script ACTUALLY CREATES output:
- Generates app assets via Gemini API (Nano Banana = gemini-2.5-flash)
- Deploys apps to surge.sh
- Generates ecom listings from arb scan data
- Produces content from alpha/trends
- Creates daily PRODUCTION_REPORT.md with visible proof

Usage:
    python3 AUTOMATIONS/autonomous_factory.py --full           # Run entire factory
    python3 AUTOMATIONS/autonomous_factory.py --assets         # Generate images via Gemini API (falls back to browser)
    python3 AUTOMATIONS/autonomous_factory.py --browser-assets # Generate via Chrome/ImageFX (no API needed, free)
    python3 AUTOMATIONS/autonomous_factory.py --collect-assets # Collect browser-downloaded images into asset dirs
    python3 AUTOMATIONS/autonomous_factory.py --deploy         # Deploy apps to surge.sh
    python3 AUTOMATIONS/autonomous_factory.py --listings       # Generate ecom listings
    python3 AUTOMATIONS/autonomous_factory.py --content        # Produce content from pipeline
    python3 AUTOMATIONS/autonomous_factory.py --report         # Generate production report
    python3 AUTOMATIONS/autonomous_factory.py --status         # Quick factory status
"""

import csv
import json
import os
import re
import subprocess
import sys
import time
import base64
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# === PATHS ===
BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "LEDGER"
OPS = BASE / "OPS"
PRODUCTS = BASE / "PRODUCTS"
CONTENT = BASE / "CONTENT"
AUTOMATIONS = BASE / "AUTOMATIONS"
APP_FACTORY = BASE / "MONEY_METHODS" / "APP_FACTORY"
BUILDS = APP_FACTORY / "builds"
SECRETS = BASE / "SECRETS"
LOGS = AUTOMATIONS / "logs"
ASSET_OUTPUT = APP_FACTORY / "generated_assets"
REPORT_DIR = OPS / "production_reports"

# Ensure output dirs exist
for d in [ASSET_OUTPUT, REPORT_DIR, LOGS]:
    d.mkdir(parents=True, exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
LOG_FILE = LOGS / f"factory_{TODAY}.log"


def log(msg):
    """Append-only logging."""
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def safe_path(target):
    """Verify path is within project root."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(BASE)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {BASE}")
    return resolved


# ============================================================
# MODULE 1: ASSET GENERATION (Gemini / Nano Banana)
# ============================================================

def get_gemini_client():
    """Initialize Gemini client. Returns None if no API key."""
    try:
        from google import genai
    except ImportError:
        log("ERROR: google-genai not installed. Run: pip3 install google-genai")
        return None

    # Check for API key in multiple locations
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        env_file = SECRETS / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("GEMINI_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not api_key:
        cred_file = SECRETS / "CREDENTIALS.env"
        if cred_file.exists():
            for line in cred_file.read_text().splitlines():
                if "GEMINI" in line and "=" in line:
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not api_key:
        # Also check project root .env
        root_env = BASE / ".env"
        if root_env.exists():
            for line in root_env.read_text().splitlines():
                if line.startswith("GEMINI_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not api_key:
        log("WARNING: No GEMINI_API_KEY found. Asset generation will be skipped.")
        log("  To enable: Get free key at https://ai.google.dev then add to SECRETS/.env")
        log("  Format: GEMINI_API_KEY=your_key_here")
        return None

    try:
        client = genai.Client(api_key=api_key)
        log("Gemini client initialized (Nano Banana ready)")
        return client
    except Exception as e:
        log(f"ERROR initializing Gemini client: {e}")
        return None


def load_asset_prompts():
    """Load prompts from APP_ASSET_GENERATION_PROMPTS.md."""
    prompts_file = APP_FACTORY / "APP_ASSET_GENERATION_PROMPTS.md"
    if not prompts_file.exists():
        log("WARNING: APP_ASSET_GENERATION_PROMPTS.md not found")
        return {}

    content = prompts_file.read_text()
    prompts = {}
    current_app = None
    current_section = None
    current_prompt = []
    in_code_block = False

    for line in content.splitlines():
        # Track app sections
        if line.startswith("## APP "):
            m = re.search(r"## APP \d+: (\w+)", line)
            if m:
                current_app = m.group(1).lower()
                prompts[current_app] = {}

        # Track subsections (Icon, Splash, etc.)
        elif current_app and line.startswith("### ") and not line.startswith("### A.") and not line.startswith("### B."):
            pass

        # Track prompt variants
        elif current_app and line.startswith("**") and "Variant" in line:
            if current_prompt and current_section:
                prompts[current_app][current_section] = "\n".join(current_prompt).strip()
            current_section = re.sub(r'[^a-z0-9_]', '_', line.lower().strip('*').strip())[:60]
            current_prompt = []

        # Code blocks contain the actual prompts
        elif line.strip() == "```":
            in_code_block = not in_code_block
        elif in_code_block and current_app and current_section:
            if not line.startswith("Platform:") and not line.startswith("Resolution:"):
                current_prompt.append(line)

    # Save last prompt
    if current_prompt and current_app and current_section:
        prompts[current_app][current_section] = "\n".join(current_prompt).strip()

    return prompts


def generate_assets_browser(max_images=10):
    """Generate app assets via automated Chrome browser + Gemini web UI.

    Uses Chrome cookies for Google auth. Playwright automates Gemini to
    generate images from prompts. No API key or billing needed.
    """
    log("Launching automated browser image generation (Gemini web UI)...")
    try:
        result = subprocess.run(
            [sys.executable, str(AUTOMATIONS / "browser_image_gen.py"),
             "--max", str(max_images)],
            capture_output=True, text=True, timeout=300,
            cwd=str(BASE),
        )
        log(result.stdout)
        if result.stderr:
            log(f"STDERR: {result.stderr[-500:]}")

        # Count generated files from today
        generated = 0
        results = []
        if ASSET_OUTPUT.exists():
            for f in ASSET_OUTPUT.rglob(f"*_{TODAY}.png"):
                generated += 1
                results.append({
                    "app": f.parent.name,
                    "variant": f.stem.replace(f"_{TODAY}", ""),
                    "file": str(f.relative_to(BASE)),
                    "size_kb": f.stat().st_size // 1024,
                })

        return {
            "generated": generated,
            "results": results,
            "mode": "browser",
        }
    except subprocess.TimeoutExpired:
        log("Browser generation timed out after 5 minutes")
        return {"generated": 0, "mode": "browser", "error": "timeout"}
    except Exception as e:
        log(f"Browser generation failed: {e}")
        return {"generated": 0, "mode": "browser", "error": str(e)}


def generate_assets(client, max_images=10, browser_fallback=True):
    """Generate app assets using Gemini API with browser fallback."""
    prompts = load_asset_prompts()
    if not prompts:
        log("SKIP: No asset prompts loaded")
        return {"generated": 0, "skipped": "no_prompts"}

    # If no API client, go straight to browser mode
    if not client:
        log("No Gemini API client. Using browser-based generation (ImageFX).")
        return generate_assets_browser(max_images)

    from google import genai

    generated = 0
    errors = 0
    quota_hit = False
    results = []

    for app_name, variants in prompts.items():
        if generated >= max_images or quota_hit:
            break

        app_asset_dir = safe_path(ASSET_OUTPUT / app_name)
        app_asset_dir.mkdir(parents=True, exist_ok=True)

        for variant_name, prompt_text in variants.items():
            if generated >= max_images or quota_hit:
                break
            if not prompt_text or len(prompt_text) < 20:
                continue

            # Skip if already generated today
            output_file = app_asset_dir / f"{variant_name}_{TODAY}.png"
            if output_file.exists():
                log(f"  SKIP {app_name}/{variant_name} (already generated today)")
                continue

            log(f"  Generating: {app_name}/{variant_name}...")
            try:
                from google.genai import types
                # Try image models in order of quality (best first)
                image_models = ["gemini-2.5-flash-image", "gemini-2.0-flash-exp-image-generation"]
                response = None
                for img_model in image_models:
                    try:
                        response = client.models.generate_content(
                            model=img_model,
                            contents=[prompt_text],
                            config=types.GenerateContentConfig(
                                response_modalities=["IMAGE"],
                                image_config=types.ImageConfig(
                                    aspect_ratio="1:1",
                                ),
                            ),
                        )
                        break  # success
                    except Exception as model_err:
                        err_str = str(model_err)
                        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                            log(f"  Rate limited on {img_model}. Switching to browser mode.")
                            response = None
                            quota_hit = True
                            break
                        elif "400" in err_str or "not support" in err_str.lower():
                            log(f"  {img_model} not available, trying next...")
                            continue
                        else:
                            raise

                if quota_hit:
                    break

                # Check if response has image data
                if response and hasattr(response, 'parts') and response.parts:
                    for part in response.parts:
                        if hasattr(part, 'inline_data') and part.inline_data:
                            img_data = part.inline_data.data
                            if isinstance(img_data, str):
                                img_data = base64.b64decode(img_data)
                            safe_path(output_file)
                            with open(output_file, "wb") as f:
                                f.write(img_data)
                            generated += 1
                            results.append({
                                "app": app_name,
                                "variant": variant_name,
                                "file": str(output_file.relative_to(BASE)),
                                "size_kb": len(img_data) // 1024
                            })
                            log(f"  DONE: {output_file.name} ({len(img_data)//1024}KB)")
                            break
                    else:
                        log(f"  WARN: No image in response for {app_name}/{variant_name}")
                        errors += 1
                else:
                    log(f"  WARN: Empty response for {app_name}/{variant_name}")
                    errors += 1

                # Rate limit: 15 req/min = 4 sec between requests
                time.sleep(4)

            except Exception as e:
                log(f"  ERROR generating {app_name}/{variant_name}: {e}")
                errors += 1
                time.sleep(5)

    # If API quota was hit, fall back to browser for remaining
    if quota_hit and browser_fallback:
        log("\nAPI quota exhausted. Falling back to browser-based generation...")
        browser_result = generate_assets_browser(max_images - generated)
        return {
            "generated": generated + browser_result.get("generated", 0),
            "errors": errors,
            "results": results,
            "browser_pending": browser_result.get("pending", 0),
            "mode": "hybrid",
        }

    log(f"Asset generation complete: {generated} generated, {errors} errors")
    return {"generated": generated, "errors": errors, "results": results}


# ============================================================
# MODULE 2: APP DEPLOYMENT (surge.sh)
# ============================================================

def get_deployable_apps():
    """Find apps that can be deployed to surge.sh."""
    apps = []
    if not BUILDS.exists():
        return apps

    for app_dir in sorted(BUILDS.iterdir()):
        if not app_dir.is_dir():
            continue
        index = app_dir / "index.html"
        if index.exists():
            size = sum(f.stat().st_size for f in app_dir.rglob("*") if f.is_file())
            apps.append({
                "name": app_dir.name,
                "path": str(app_dir),
                "index_size": index.stat().st_size,
                "total_size_kb": size // 1024,
                "files": sum(1 for _ in app_dir.rglob("*") if _.is_file())
            })
    return apps


def deploy_apps(force=False):
    """Deploy all PWA builds to surge.sh."""
    apps = get_deployable_apps()
    if not apps:
        log("SKIP: No deployable apps found in builds/")
        return {"deployed": 0, "apps": []}

    # Check if surge is available
    surge_check = subprocess.run(["which", "surge"], capture_output=True, text=True)
    if surge_check.returncode != 0:
        log("SKIP: surge CLI not found. Install: npm install -g surge")
        return {"deployed": 0, "skipped": "surge_not_installed"}

    deployed = []
    skipped = []

    for app in apps:
        name = app["name"]
        # Standard surge domain
        domain = f"{name}.surge.sh"

        if not force:
            # Check if already deployed (quick HEAD request)
            check = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"https://{domain}"],
                capture_output=True, text=True, timeout=10
            )
            if check.stdout.strip() == "200":
                log(f"  SKIP {name} (already live at {domain})")
                skipped.append({"name": name, "url": f"https://{domain}", "status": "already_live"})
                continue

        log(f"  Deploying {name} to {domain}...")
        try:
            result = subprocess.run(
                ["surge", app["path"], domain],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                deployed.append({"name": name, "url": f"https://{domain}", "status": "deployed"})
                log(f"  LIVE: https://{domain}")
            else:
                log(f"  FAIL: {name} - {result.stderr[:200]}")
                skipped.append({"name": name, "status": "deploy_failed", "error": result.stderr[:200]})
        except Exception as e:
            log(f"  ERROR deploying {name}: {e}")
            skipped.append({"name": name, "status": "error", "error": str(e)})

    log(f"Deployment: {len(deployed)} deployed, {len(skipped)} skipped")
    return {"deployed": len(deployed), "skipped": len(skipped), "apps": deployed + skipped}


# ============================================================
# MODULE 3: ECOM LISTING GENERATION
# ============================================================

def generate_ecom_listings(min_margin=25, max_listings=20):
    """Generate ecom marketplace listings from arb scan data."""
    arb_csv = LEDGER / "ECOM_ARB_OPPORTUNITIES.csv"
    if not arb_csv.exists():
        log("SKIP: ECOM_ARB_OPPORTUNITIES.csv not found")
        return {"generated": 0}

    # Read opportunities
    opportunities = []
    with open(arb_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                margin = float(row.get("margin_pct", "0").replace("%", ""))
                if margin >= min_margin:
                    opportunities.append(row)
            except (ValueError, TypeError):
                continue

    # Sort by margin descending
    opportunities.sort(key=lambda x: float(x.get("margin_pct", "0").replace("%", "")), reverse=True)
    opportunities = opportunities[:max_listings]

    if not opportunities:
        log(f"SKIP: No arb opportunities with margin >= {min_margin}%")
        return {"generated": 0}

    # Generate listings
    output_dir = safe_path(PRODUCTS / "ARB_LISTINGS")
    output_dir.mkdir(parents=True, exist_ok=True)

    listings_file = safe_path(output_dir / f"ARB_LISTINGS_{TODAY}.md")
    sourcing_file = safe_path(output_dir / f"SOURCING_GUIDE_{TODAY}.md")

    listings = []
    for opp in opportunities:
        product = opp.get("product", "Unknown Product")
        category = opp.get("category", "general")
        sell_price = opp.get("sell_price", "N/A")
        source_price = opp.get("source_price", "N/A")
        margin = opp.get("margin_pct", "N/A")
        platform = opp.get("best_platform", "eBay")
        net_profit = opp.get("net_profit", "N/A")

        listing = {
            "product": product,
            "category": category,
            "sell_price": sell_price,
            "source_price": source_price,
            "margin": margin,
            "platform": platform,
            "net_profit": net_profit,
        }

        # Generate listing copy
        listing["title"] = f"{product} - Premium Quality, Fast Shipping"
        listing["description"] = (
            f"Brand new {product}. Ships within 24 hours. "
            f"Top-rated seller. Returns accepted within 30 days. "
            f"Category: {category}."
        )
        listing["tags"] = [
            category.lower(), product.split()[0].lower(),
            "fast shipping", "new", "trending"
        ]
        listings.append(listing)

    # Write listings markdown
    md_lines = [
        f"# PRINTMAXX Arb Listings - {TODAY}",
        f"\n**Generated:** {NOW}",
        f"**Products:** {len(listings)} (min margin: {min_margin}%)",
        f"\n---\n"
    ]

    for i, l in enumerate(listings, 1):
        md_lines.extend([
            f"## {i}. {l['product']}",
            f"- **Sell Price:** {l['sell_price']}",
            f"- **Source Price:** {l['source_price']}",
            f"- **Net Profit:** {l['net_profit']}",
            f"- **Margin:** {l['margin']}%",
            f"- **Best Platform:** {l['platform']}",
            f"- **Listing Title:** {l['title']}",
            f"- **Description:** {l['description']}",
            f"- **Tags:** {', '.join(l['tags'])}",
            ""
        ])

    safe_path(listings_file)
    listings_file.write_text("\n".join(md_lines))
    log(f"Generated {len(listings)} listings at {listings_file.name}")

    # Write sourcing guide
    source_lines = [
        f"# Sourcing Guide - {TODAY}",
        f"\n**Products to source:** {len(listings)}",
        f"\n| # | Product | Source Price | Sell Price | Margin | Platform |",
        f"|---|---------|-------------|-----------|--------|----------|"
    ]
    for i, l in enumerate(listings, 1):
        source_lines.append(
            f"| {i} | {l['product'][:30]} | {l['source_price']} | {l['sell_price']} | {l['margin']}% | {l['platform']} |"
        )
    source_lines.extend([
        "",
        "## Sourcing Steps",
        "1. Search AliExpress for each product name",
        "2. Filter by: 4.5+ stars, 100+ orders, ePacket/standard shipping",
        "3. Contact supplier for bulk pricing (10+ units)",
        "4. List on target platform with 15-20% markup over scan price",
        "5. Ship direct from supplier or order inventory for faster delivery"
    ])
    safe_path(sourcing_file)
    sourcing_file.write_text("\n".join(source_lines))

    return {"generated": len(listings), "file": str(listings_file.relative_to(BASE))}


# ============================================================
# MODULE 4: CONTENT PRODUCTION
# ============================================================

def produce_content():
    """Generate content from alpha pipeline and move through stages."""
    results = {
        "tweets_drafted": 0,
        "content_moved": 0,
        "alpha_converted": 0,
    }

    # 1. Count existing content by status
    content_dir = CONTENT / "social"
    pending_count = 0
    ready_count = 0
    posted_count = 0

    if content_dir.exists():
        for f in content_dir.rglob("*"):
            if f.is_file() and f.suffix in [".md", ".csv"]:
                try:
                    text = f.read_text(errors="ignore")[:5000]
                    if "PENDING_REVIEW" in text:
                        pending_count += 1
                    elif "READY_TO_POST" in text:
                        ready_count += 1
                    elif "POSTED" in text:
                        posted_count += 1
                except Exception:
                    pass

    # 2. Generate tweets from today's alpha
    alpha_csv = LEDGER / "ALPHA_STAGING.csv"
    if alpha_csv.exists():
        today_alpha = []
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        with open(alpha_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts = row.get("timestamp", "")
                status = row.get("status", "")
                if status == "APPROVED" and (TODAY in ts or yesterday in ts):
                    today_alpha.append(row)

        if today_alpha:
            tweets_file = safe_path(CONTENT / "social" / "auto_generated" / f"factory_tweets_{TODAY}.md")
            tweets_file.parent.mkdir(parents=True, exist_ok=True)

            tweet_lines = [
                f"# Factory-Generated Tweets - {TODAY}",
                f"Status: PENDING_REVIEW",
                f"Source: autonomous_factory.py from {len(today_alpha)} approved alpha entries",
                ""
            ]

            for alpha in today_alpha[:10]:  # Max 10 tweets per run
                source = alpha.get("source", "")
                summary = alpha.get("summary", alpha.get("content", ""))[:200]
                category = alpha.get("category", "GENERAL")

                # Generate tweet in PRINTMAXXER voice
                tweet = generate_tweet_from_alpha(summary, category, source)
                if tweet:
                    tweet_lines.extend([
                        f"---",
                        f"### Alpha: {alpha.get('alpha_id', 'N/A')}",
                        f"**Category:** {category}",
                        f"**Tweet:**",
                        f"```",
                        tweet,
                        f"```",
                        ""
                    ])
                    results["tweets_drafted"] += 1

            safe_path(tweets_file)
            tweets_file.write_text("\n".join(tweet_lines))
            log(f"Drafted {results['tweets_drafted']} tweets from today's alpha")

    # 3. Count content in auto_generated
    auto_dir = CONTENT / "social" / "auto_generated"
    if auto_dir.exists():
        auto_files = list(auto_dir.glob("*.md")) + list(auto_dir.glob("*.csv"))
        results["auto_generated_files"] = len(auto_files)

    # 3. Generate tweets from ecom arb finds (building-in-public content)
    arb_csv = LEDGER / "ECOM_ARB_OPPORTUNITIES.csv"
    if arb_csv.exists():
        top_arb = []
        with open(arb_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    margin = float(row.get("margin_pct", "0").replace("%", ""))
                    if margin > 40 and (TODAY in row.get("timestamp", "") or
                                        (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d") in row.get("timestamp", "")):
                        top_arb.append(row)
                except (ValueError, TypeError):
                    pass

        if top_arb:
            arb_tweets_file = safe_path(CONTENT / "social" / "auto_generated" / f"factory_arb_tweets_{TODAY}.md")
            arb_tweets_file.parent.mkdir(parents=True, exist_ok=True)
            arb_lines = [
                f"# Factory Arb Tweets - {TODAY}",
                f"Status: PENDING_REVIEW",
                f"Source: autonomous_factory.py from {len(top_arb)} high-margin finds",
                ""
            ]
            for opp in top_arb[:5]:
                product = opp.get("product", "unknown")
                margin = opp.get("margin_pct", "?")
                sell = opp.get("sell_price", "?")
                source = opp.get("source_price", "?")
                tweet = f"found a {product} selling for ${sell}. source price ${source}. that's {margin}% margin before platform fees. the arb scanner catches these every 2 hours. just need accounts to start listing."
                arb_lines.extend([
                    "---",
                    f"**Product:** {product} ({margin}% margin)",
                    "```",
                    tweet[:280],
                    "```",
                    ""
                ])
                results["tweets_drafted"] += 1

            safe_path(arb_tweets_file)
            arb_tweets_file.write_text("\n".join(arb_lines))
            log(f"Drafted {min(len(top_arb), 5)} arb tweets")

    results["pending"] = pending_count
    results["ready"] = ready_count
    results["posted"] = posted_count

    log(f"Content: {results['tweets_drafted']} new tweets, {pending_count} pending, {ready_count} ready, {posted_count} posted")
    return results


def generate_tweet_from_alpha(summary, category, source):
    """Generate a tweet in PRINTMAXXER voice from alpha summary."""
    if not summary or len(summary) < 10:
        return None

    # Simple template-based generation (no LLM needed)
    # PRINTMAXXER voice: lowercase, specific numbers, consequence-first, no fluff
    templates = {
        "APP_FACTORY": "found an app doing {summary_short}. cloning it for a different niche. the playbook works.",
        "TOOL_ALPHA": "{summary_short}. been using it for a week. saves real time.",
        "GROWTH_HACK": "{summary_short}. tested it yesterday. actually works.",
        "MONETIZATION": "{summary_short}. the math checks out.",
        "OUTBOUND": "{summary_short}. cold email still prints if you do it right.",
        "CONTENT_FORMAT": "{summary_short}. this format is printing engagement right now.",
    }

    template = templates.get(category, "{summary_short}. just found this. sharing because it's real signal.")

    # Clean and shorten summary
    summary_short = summary.strip()
    summary_short = re.sub(r'https?://\S+', '', summary_short).strip()
    summary_short = summary_short[:200]

    # Make it lowercase, casual
    tweet = template.format(summary_short=summary_short.lower())

    # Trim to 280 chars
    if len(tweet) > 280:
        tweet = tweet[:277] + "..."

    return tweet


# ============================================================
# MODULE 5: DAILY PRODUCTION REPORT (VISIBLE PROOF)
# ============================================================

def generate_production_report(asset_results=None, deploy_results=None,
                                listing_results=None, content_results=None):
    """Generate daily production report showing EXACTLY what was produced."""

    report_file = safe_path(REPORT_DIR / f"PRODUCTION_REPORT_{TODAY}.md")

    # Gather system-wide production metrics
    metrics = gather_production_metrics()

    lines = [
        f"# PRINTMAXX PRODUCTION REPORT",
        f"## {TODAY} | Generated {NOW}",
        "",
        "---",
        "",
        "## FACTORY OUTPUT TODAY",
        "",
    ]

    # Assets section
    if asset_results:
        lines.extend([
            f"### Assets Generated (Gemini/Nano Banana)",
            f"- **Images created:** {asset_results.get('generated', 0)}",
            f"- **Errors:** {asset_results.get('errors', 0)}",
        ])
        for r in asset_results.get("results", []):
            lines.append(f"  - {r['app']}/{r['variant']} ({r['size_kb']}KB)")
        lines.append("")
    else:
        lines.extend([
            "### Assets Generated",
            "- **Status:** Not run this cycle (no Gemini API key or --assets not used)",
            ""
        ])

    # Deployment section
    if deploy_results:
        lines.extend([
            f"### Apps Deployed (surge.sh)",
            f"- **Deployed:** {deploy_results.get('deployed', 0)}",
            f"- **Skipped:** {deploy_results.get('skipped', 0)}",
        ])
        for app in deploy_results.get("apps", []):
            status_emoji = "LIVE" if app.get("status") in ["deployed", "already_live"] else "FAIL"
            lines.append(f"  - [{status_emoji}] {app['name']} → {app.get('url', 'N/A')}")
        lines.append("")

    # Listings section
    if listing_results:
        lines.extend([
            f"### Ecom Listings Generated",
            f"- **Listings created:** {listing_results.get('generated', 0)}",
            f"- **File:** {listing_results.get('file', 'N/A')}",
            ""
        ])

    # Content section
    if content_results:
        lines.extend([
            f"### Content Pipeline",
            f"- **Tweets drafted today:** {content_results.get('tweets_drafted', 0)}",
            f"- **Pending review:** {content_results.get('pending', 0)}",
            f"- **Ready to post:** {content_results.get('ready', 0)}",
            f"- **Posted:** {content_results.get('posted', 0)}",
            f"- **Auto-generated files total:** {content_results.get('auto_generated_files', 0)}",
            ""
        ])

    # System-wide metrics
    lines.extend([
        "---",
        "",
        "## SYSTEM-WIDE PRODUCTION METRICS",
        "",
        f"### Scanning Layer (WORKING)",
        f"- **Ecom arb opportunities:** {metrics['ecom_total']} total, {metrics['ecom_today']} added today",
        f"- **High-margin products (>30%):** {metrics['ecom_high_margin']}",
        f"- **Freelance demand posts:** {metrics['freelance_total']} total",
        f"- **Alpha entries:** {metrics['alpha_total']} total, {metrics['alpha_pending']} pending review",
        f"- **Trend signals:** {metrics['trend_total']} total",
        "",
        f"### Production Layer (THIS FACTORY)",
        f"- **App builds available:** {metrics['app_builds']}",
        f"- **Apps deployed (surge.sh):** {metrics['apps_deployed']}",
        f"- **Arb listings generated:** {metrics['arb_listings_count']}",
        f"- **Content files generated:** {metrics['content_auto_count']}",
        f"- **Generated assets:** {metrics['asset_count']}",
        "",
        f"### Execution Layer (NEEDS HUMAN)",
        f"- **Platform accounts created:** {metrics['accounts_created']}/45+",
        f"- **Products listed on marketplaces:** {metrics['products_listed']}",
        f"- **Cold emails sent:** {metrics['emails_sent']}",
        f"- **Revenue generated:** ${metrics['revenue']}",
        "",
    ])

    # Blockers
    lines.extend([
        "---",
        "",
        "## TOP BLOCKERS",
        "",
    ])

    blockers = []
    if metrics['accounts_created'] == 0:
        blockers.append("1. **NO ACCOUNTS CREATED** — Cannot list products, send emails, or post content without platform accounts. Start: https://gumroad.com → https://fiverr.com → https://upwork.com")
    if not asset_results or asset_results.get("generated", 0) == 0:
        mode = (asset_results or {}).get("mode", "")
        if mode == "browser" or (asset_results or {}).get("browser_pending", 0) > 0:
            pending = (asset_results or {}).get("pending", 0) or (asset_results or {}).get("browser_pending", 0)
            blockers.append(f"2. **BROWSER ASSETS PENDING** — {pending} images queued for browser generation. Run: `--browser-assets` then download from ImageFX, then `--collect-assets`")
        else:
            blockers.append(f"2. **ASSET GENERATION** — Run `--browser-assets` to generate via ImageFX (free, no API billing needed) or enable billing at https://ai.google.dev for API mode")
    if metrics['emails_sent'] == 0:
        blockers.append(f"3. **ZERO EMAILS SENT** — {metrics.get('emails_ready', 0)} emails drafted but 0 sent. Need email infra (DeliverOn $23/mo or Instantly $30/mo)")
    if metrics['revenue'] == 0:
        blockers.append("4. **$0 REVENUE** — Everything is ready to sell but nothing is listed on any platform")

    if blockers:
        lines.extend(blockers)
    else:
        lines.append("No critical blockers!")

    lines.extend([
        "",
        "---",
        "",
        "## NEXT FACTORY RUN",
        f"- Scheduled: Next cron cycle or `python3 AUTOMATIONS/autonomous_factory.py --full`",
        f"- Log: AUTOMATIONS/logs/factory_{TODAY}.log",
        ""
    ])

    safe_path(report_file)
    report_file.write_text("\n".join(lines))
    log(f"Production report saved: {report_file.name}")

    # Also save a machine-readable version
    metrics_file = safe_path(REPORT_DIR / f"factory_metrics_{TODAY}.json")
    metrics["report_generated"] = NOW
    metrics["asset_results"] = asset_results or {}
    metrics["deploy_results"] = deploy_results or {}
    metrics["listing_results"] = listing_results or {}
    metrics["content_results"] = content_results or {}
    metrics_file.write_text(json.dumps(metrics, indent=2, default=str))

    return report_file


def gather_production_metrics():
    """Gather all production metrics across the system."""
    metrics = {
        "ecom_total": 0,
        "ecom_today": 0,
        "ecom_high_margin": 0,
        "freelance_total": 0,
        "alpha_total": 0,
        "alpha_pending": 0,
        "trend_total": 0,
        "app_builds": 0,
        "apps_deployed": 0,
        "arb_listings_count": 0,
        "content_auto_count": 0,
        "asset_count": 0,
        "accounts_created": 0,
        "products_listed": 0,
        "emails_sent": 0,
        "emails_ready": 0,
        "revenue": 0,
    }

    # Ecom arb
    arb_csv = LEDGER / "ECOM_ARB_OPPORTUNITIES.csv"
    if arb_csv.exists():
        with open(arb_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                metrics["ecom_total"] += 1
                if TODAY in row.get("timestamp", ""):
                    metrics["ecom_today"] += 1
                try:
                    if float(row.get("margin_pct", "0").replace("%", "")) > 30:
                        metrics["ecom_high_margin"] += 1
                except (ValueError, TypeError):
                    pass

    # Freelance demand
    fl_csv = LEDGER / "FREELANCE_DEMAND_SCAN.csv"
    if fl_csv.exists():
        with open(fl_csv, "r") as f:
            metrics["freelance_total"] = sum(1 for _ in csv.DictReader(f))

    # Alpha
    alpha_csv = LEDGER / "ALPHA_STAGING.csv"
    if alpha_csv.exists():
        with open(alpha_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                metrics["alpha_total"] += 1
                if row.get("status", "") == "PENDING_REVIEW":
                    metrics["alpha_pending"] += 1

    # Trends
    trend_csv = LEDGER / "TREND_SIGNALS.csv"
    if trend_csv.exists():
        with open(trend_csv, "r") as f:
            metrics["trend_total"] = sum(1 for _ in csv.DictReader(f))

    # App builds
    if BUILDS.exists():
        metrics["app_builds"] = sum(1 for d in BUILDS.iterdir() if d.is_dir() and (d / "index.html").exists())

    # Deployed apps (check surge.sh)
    deploy_log = OPS / "DEPLOY_LOG.md"
    if deploy_log.exists():
        text = deploy_log.read_text()
        metrics["apps_deployed"] = text.count("surge.sh")

    # Arb listings
    arb_dir = PRODUCTS / "ARB_LISTINGS"
    if arb_dir.exists():
        for f in arb_dir.glob("ARB_LISTINGS_*.md"):
            try:
                text = f.read_text()
                metrics["arb_listings_count"] += text.count("## ")
            except Exception:
                pass

    # Auto-generated content
    auto_dir = CONTENT / "social" / "auto_generated"
    if auto_dir.exists():
        metrics["content_auto_count"] = sum(1 for _ in auto_dir.iterdir() if _.is_file())

    # Generated assets
    if ASSET_OUTPUT.exists():
        metrics["asset_count"] = sum(1 for _ in ASSET_OUTPUT.rglob("*.png"))

    # Accounts (from ACCOUNTS.csv)
    accounts_csv = LEDGER / "ACCOUNTS.csv"
    if accounts_csv.exists():
        with open(accounts_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = row.get("status", "").upper()
                if status in ["ACTIVE", "CREATED", "LIVE"]:
                    metrics["accounts_created"] += 1

    # Cold emails ready
    outreach_dir = AUTOMATIONS / "outreach"
    if outreach_dir.exists():
        for f in outreach_dir.glob("*.csv"):
            try:
                with open(f, "r") as fh:
                    metrics["emails_ready"] += sum(1 for _ in csv.DictReader(fh))
            except Exception:
                pass

    # Revenue
    rev_csv = Path(BASE / "FINANCIALS" / "REVENUE_TRACKER.csv")
    if rev_csv.exists():
        with open(rev_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    amt = float(row.get("amount", "0").replace("$", "").replace(",", ""))
                    metrics["revenue"] += amt
                except (ValueError, TypeError):
                    pass

    return metrics


# ============================================================
# MODULE 6: STATUS CHECK (Quick view)
# ============================================================

def show_status():
    """Quick factory status."""
    metrics = gather_production_metrics()

    print("\n" + "=" * 60)
    print("  PRINTMAXX AUTONOMOUS FACTORY STATUS")
    print("=" * 60)

    # Scanning (GREEN = working)
    print("\n  SCANNING LAYER (data collection)")
    scanning_ok = metrics["ecom_total"] > 0 or metrics["alpha_total"] > 0
    status = "GREEN" if scanning_ok else "RED"
    print(f"  [{status}] Ecom arb:     {metrics['ecom_total']} total, {metrics['ecom_today']} today")
    print(f"  [{status}] Alpha:        {metrics['alpha_total']} total, {metrics['alpha_pending']} pending")
    print(f"  [{'GREEN' if metrics['freelance_total'] > 0 else 'RED'}] Freelance:    {metrics['freelance_total']} posts")
    print(f"  [{'GREEN' if metrics['trend_total'] > 0 else 'AMBER'}] Trends:       {metrics['trend_total']} signals")

    # Production (what this factory creates)
    print("\n  PRODUCTION LAYER (factory output)")
    print(f"  [{'GREEN' if metrics['app_builds'] > 0 else 'RED'}] App builds:   {metrics['app_builds']} ready")
    print(f"  [{'GREEN' if metrics['apps_deployed'] > 0 else 'AMBER'}] Deployed:     {metrics['apps_deployed']} live")
    print(f"  [{'GREEN' if metrics['arb_listings_count'] > 0 else 'AMBER'}] Arb listings: {metrics['arb_listings_count']} generated")
    print(f"  [{'GREEN' if metrics['content_auto_count'] > 0 else 'AMBER'}] Content:      {metrics['content_auto_count']} auto-generated")
    print(f"  [{'GREEN' if metrics['asset_count'] > 0 else 'AMBER'}] Assets:       {metrics['asset_count']} images")

    # Execution (needs human)
    print("\n  EXECUTION LAYER (needs human action)")
    print(f"  [{'GREEN' if metrics['accounts_created'] > 0 else 'RED'}] Accounts:     {metrics['accounts_created']}/45+")
    print(f"  [{'GREEN' if metrics['products_listed'] > 0 else 'RED'}] Listed:       {metrics['products_listed']} products")
    print(f"  [{'GREEN' if metrics['emails_sent'] > 0 else 'RED'}] Emails sent:  {metrics['emails_sent']}")
    print(f"  [{'GREEN' if metrics['revenue'] > 0 else 'RED'}] Revenue:      ${metrics['revenue']}")

    # Gemini API check
    has_key = bool(os.environ.get("GEMINI_API_KEY"))
    if not has_key:
        env_file = SECRETS / ".env"
        if env_file.exists():
            has_key = "GEMINI_API_KEY" in env_file.read_text()
    if not has_key:
        root_env = BASE / ".env"
        if root_env.exists():
            for line in root_env.read_text().splitlines():
                if line.startswith("GEMINI_API_KEY=") and line.split("=", 1)[1].strip():
                    has_key = True
                    break

    print(f"\n  GEMINI API:    {'CONFIGURED' if has_key else 'MISSING (get free key at https://ai.google.dev)'}")

    # Latest report
    reports = sorted(REPORT_DIR.glob("PRODUCTION_REPORT_*.md"))
    if reports:
        print(f"  Latest report: {reports[-1].name}")
    else:
        print("  Latest report: None (run --report to generate)")

    print("\n" + "=" * 60)
    print(f"  Run: python3 AUTOMATIONS/autonomous_factory.py --full")
    print("=" * 60 + "\n")

    return metrics


# ============================================================
# MAIN
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="PRINTMAXX Autonomous Production Factory")
    parser.add_argument("--full", action="store_true", help="Run entire factory")
    parser.add_argument("--assets", action="store_true", help="Generate images via Gemini")
    parser.add_argument("--deploy", action="store_true", help="Deploy apps to surge.sh")
    parser.add_argument("--listings", action="store_true", help="Generate ecom listings")
    parser.add_argument("--content", action="store_true", help="Produce content from pipeline")
    parser.add_argument("--report", action="store_true", help="Generate production report")
    parser.add_argument("--status", action="store_true", help="Quick factory status")
    parser.add_argument("--force-deploy", action="store_true", help="Force redeploy all apps")
    parser.add_argument("--max-images", type=int, default=10, help="Max images to generate per run")
    parser.add_argument("--min-margin", type=float, default=25, help="Min margin for listings")
    parser.add_argument("--browser-assets", action="store_true", help="Generate assets via Chrome/ImageFX (no API needed)")
    parser.add_argument("--collect-assets", action="store_true", help="Collect downloaded browser-generated assets from ~/Downloads")
    args = parser.parse_args()

    if not any([args.full, args.assets, args.deploy, args.listings,
                args.content, args.report, args.status, args.browser_assets,
                args.collect_assets]):
        args.status = True

    log(f"=== FACTORY RUN START: {NOW} ===")

    asset_results = None
    deploy_results = None
    listing_results = None
    content_results = None

    if args.status:
        show_status()
        return

    if args.browser_assets:
        log("\n--- BROWSER-BASED ASSET GENERATION (ImageFX) ---")
        asset_results = generate_assets_browser(max_images=args.max_images)
        if args.report or args.full:
            generate_production_report(asset_results=asset_results)
        return

    if args.full or args.assets:
        log("\n--- MODULE 1: ASSET GENERATION ---")
        client = get_gemini_client()
        asset_results = generate_assets(client, max_images=args.max_images)

    if args.full or args.deploy:
        log("\n--- MODULE 2: APP DEPLOYMENT ---")
        deploy_results = deploy_apps(force=args.force_deploy)

    if args.full or args.listings:
        log("\n--- MODULE 3: ECOM LISTINGS ---")
        listing_results = generate_ecom_listings(min_margin=args.min_margin)

    if args.full or args.content:
        log("\n--- MODULE 4: CONTENT PRODUCTION ---")
        content_results = produce_content()

    if args.full or args.report:
        log("\n--- MODULE 5: PRODUCTION REPORT ---")
        report = generate_production_report(
            asset_results=asset_results,
            deploy_results=deploy_results,
            listing_results=listing_results,
            content_results=content_results
        )
        log(f"Report: {report}")

    log(f"\n=== FACTORY RUN COMPLETE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")


if __name__ == "__main__":
    main()
