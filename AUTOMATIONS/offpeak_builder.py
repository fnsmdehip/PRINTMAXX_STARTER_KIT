#!/usr/bin/env python3
"""OFFPEAK BUILDER — Uses 2x window to BUILD and REFINE finished assets.

NOT another meta-agent. This script actually produces deployable outputs:
- Refines existing content from draft → ship-ready
- Builds app store listings from existing app code
- Packages Gumroad products from raw files
- Converts alpha intelligence into finished products
- Generates cold email sequences from lead data
- Creates landing page copy from existing templates

Uses claude -p with agentic prompts. Each run produces TANGIBLE output.

Usage:
  python3 AUTOMATIONS/offpeak_builder.py --refine-content    # Polish draft content
  python3 AUTOMATIONS/offpeak_builder.py --build-products     # Package Gumroad products
  python3 AUTOMATIONS/offpeak_builder.py --alpha-to-assets    # Convert alpha → products
  python3 AUTOMATIONS/offpeak_builder.py --refine-apps        # Polish app code + listings
  python3 AUTOMATIONS/offpeak_builder.py --outreach-ready     # Build ready-to-send sequences
  python3 AUTOMATIONS/offpeak_builder.py --landing-polish     # Fix/improve landing pages
  python3 AUTOMATIONS/offpeak_builder.py --full-cycle         # Run ALL builders
"""
from __future__ import annotations
import argparse, json, subprocess, sys, os
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
AUTO = PROJECT / "AUTOMATIONS"
LOGS = AUTO / "logs"
LOGS.mkdir(exist_ok=True)

# Use smart model routing
MODEL_OPUS = "claude-opus-4-6"
MODEL_SONNET = "claude-sonnet-4-6"

def _load_json(p, default=None):
    try: return json.loads(Path(p).read_text())
    except: return default or {}

def _run_claude(prompt: str, model: str = MODEL_SONNET, label: str = "builder", timeout: int = 900) -> bool:
    """Run claude -p with a prompt. Returns True if successful."""
    log_file = LOGS / f"offpeak_{label}_{datetime.now().strftime('%Y%m%d_%H%M')}.log"
    cmd = f'cd "{PROJECT}" && claude -p "{prompt}" --dangerously-skip-permissions --model {model} >> "{log_file}" 2>&1'
    print(f"  [{label}] Launching with {model}...")
    try:
        r = subprocess.run(cmd, shell=True, timeout=timeout, capture_output=True, text=True)
        print(f"  [{label}] {'OK' if r.returncode == 0 else 'FAILED'} (log: {log_file.name})")
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  [{label}] Timed out after {timeout}s")
        return False
    except Exception as e:
        print(f"  [{label}] Error: {e}")
        return False


def _get_soul_voice() -> str:
    """Get SOUL + voice model injection for prompts."""
    soul = ""
    try:
        soul = (AUTO / "SOUL.md").read_text()[:1500]
    except: pass
    voice = ""
    try:
        from _common import get_voice_model
        voice = get_voice_model()
    except: pass
    return f"{soul}\n\n{voice}" if voice else soul


def refine_content():
    """Take draft content and make it ship-ready."""
    print("\n=== REFINE CONTENT ===")
    soul = _get_soul_voice()

    prompt = f"""You are the PRINTMAXX content refiner. Your job: take DRAFT content and make it SHIP-READY.

{soul}

TASK:
1. Read CONTENT/social/posting_queue/ — find all .txt files
2. For each file, score it 1-10 on:
   - Hook strength (first line grabs attention?)
   - Specificity (has real numbers, tools, methods?)
   - Voice match (lowercase, direct, no AI slop?)
   - Actionability (reader knows what to do after?)
3. Files scoring < 7: REWRITE them in place following copy-style.md rules
4. Files scoring 7+: Leave them, they're ready
5. Generate 10 NEW posts based on the best-performing patterns you see
6. Save new posts to CONTENT/social/posting_queue/refined_batch_{date}.txt
7. Write a summary: how many refined, how many new, quality scores

RULES:
- Read .claude/rules/copy-style.md FIRST — follow it exactly
- No em dashes, no AI vocabulary, consequence-first hooks
- Specific numbers > vague claims
- Would @pipelineabuser post this? If no, rewrite.
- All files stay in project root
"""
    _run_claude(prompt.replace('"', '\\"'), MODEL_SONNET, "refine_content")


def build_products():
    """Package existing raw files into Gumroad-ready products."""
    print("\n=== BUILD PRODUCTS ===")

    prompt = f"""You are the PRINTMAXX product packager. Your job: turn raw files into LISTED products.

TASK:
1. Scan PRODUCTS/GUMROAD_INSTANT_UPLOAD/ — find all product folders
2. For each product:
   a. Check if it has: cover image, formatted PDF/content, pricing, description
   b. If missing ANY of those, CREATE them now
   c. Write product listing copy (title, description, price, tags) following copy-style.md
   d. Save listing copy to PRODUCTS/GUMROAD_INSTANT_UPLOAD/{{product}}/LISTING.md
3. Scan DIGITAL_PRODUCTS/ for additional products not yet packaged
4. Create a master PRODUCTS/GUMROAD_UPLOAD_QUEUE.md with:
   - Product name, price, file path, listing copy, status (READY/NEEDS_WORK)
   - Ordered by estimated revenue potential

RULES:
- Read .claude/rules/copy-style.md — product descriptions must match voice
- Prices: $7-27 for PDFs, $27-97 for tools/templates, $97-297 for courses
- No AI slop in descriptions. Direct, specific, consequence-first.
- All files stay in project root
"""
    _run_claude(prompt.replace('"', '\\"'), MODEL_SONNET, "build_products")


def alpha_to_assets():
    """Convert high-ROI alpha entries into actual products/content/tools."""
    print("\n=== ALPHA → ASSETS ===")

    prompt = f"""You are the PRINTMAXX alpha converter. Your job: turn intelligence into MONEY.

TASK:
1. Read LEDGER/ALPHA_STAGING.csv — find all APPROVED entries with ROI_POTENTIAL = HIGHEST or HIGH
2. For the top 20 entries:
   a. Categorize: can this become a (a) product, (b) content piece, (c) tool, (d) service offering?
   b. For products: create the product outline + first draft in PRODUCTS/alpha_derived/
   c. For content: write 3 social posts + 1 thread in CONTENT/social/posting_queue/alpha_content_{date}.txt
   d. For tools: create a spec + MVP code in MONEY_METHODS/APP_FACTORY/alpha_tools/
   e. For services: create an offer page draft in LANDING/alpha_services/
3. Update LEDGER/ASSET_TRACKER.csv with what was created (alpha_source, asset_type, status)
4. Write summary: X alpha entries → Y products, Z content pieces, W tools

ANTI-PATTERN: Do NOT just create a report about what COULD be done. Actually CREATE the assets.
All files stay in project root.
"""
    _run_claude(prompt.replace('"', '\\"'), MODEL_OPUS, "alpha_to_assets")


def refine_apps():
    """Polish existing app code, create store listings, improve UI."""
    print("\n=== REFINE APPS ===")

    prompt = f"""You are the PRINTMAXX app polisher. Your job: make built apps STORE-READY.

TASK:
1. Scan MONEY_METHODS/APP_FACTORY/builds/ — list all app directories
2. For each app:
   a. Check if it builds (npm install && npm run build or equivalent)
   b. Check for: app icon, screenshots, privacy policy, terms of service
   c. If missing, CREATE them:
      - App icon: create a simple SVG or describe exact spec for image gen
      - Screenshots: list what screens to capture
      - Privacy policy: generate from template
      - Terms: generate from template
   d. Create APP_STORE_LISTING.md with: name, subtitle, description, keywords, category, price
   e. Create GOOGLE_PLAY_LISTING.md with same
3. Write MONEY_METHODS/APP_FACTORY/STORE_READY_REPORT.md:
   - Which apps are ready to submit
   - Which need human action (screenshots, developer account)
   - Priority order by estimated revenue

RULES: Focus on the TOP 3 most promising apps. Don't spread thin across all of them.
All files stay in project root.
"""
    _run_claude(prompt.replace('"', '\\"'), MODEL_SONNET, "refine_apps")


def outreach_ready():
    """Build ready-to-send cold email sequences from lead data."""
    print("\n=== OUTREACH READY ===")

    prompt = f"""You are the PRINTMAXX outreach builder. Your job: create PASTE-AND-SEND email sequences.

TASK:
1. Read AUTOMATIONS/leads/ — find all lead files (CSV, JSON, MD)
2. Categorize leads by type: SaaS founders, local businesses, freelancers, agencies
3. For each category, create a 3-email sequence:
   - Email 1: cold intro (specific problem + proof)
   - Email 2: follow-up (case study or social proof)
   - Email 3: breakup email (scarcity + final CTA)
4. Save sequences to MONEY_METHODS/OUTBOUND/email_sequences/
5. For the TOP 20 hottest leads (by score or recency):
   - Write personalized email 1 (specific to their company/situation)
   - Save to MONEY_METHODS/OUTBOUND/personalized/{{company}}_email1.txt
6. Create MONEY_METHODS/OUTBOUND/SEND_QUEUE.md:
   - Ordered list of who to email, which sequence, personalization notes

RULES:
- Read .claude/rules/copy-style.md — emails must match voice
- No "I hope this email finds you well" — direct, specific, consequence-first
- Subject lines: specific benefit in < 50 chars
- All files stay in project root
"""
    _run_claude(prompt.replace('"', '\\"'), MODEL_SONNET, "outreach_ready")


def landing_polish():
    """Fix and improve existing landing pages."""
    print("\n=== LANDING POLISH ===")

    prompt = f"""You are the PRINTMAXX landing page optimizer. Your job: make existing sites CONVERT.

TASK:
1. Check OPS/DEPLOYMENT_URLS.md — get list of deployed surge.sh sites
2. For the top 10 most important sites (revenue-generating potential):
   a. Read the source HTML/code
   b. Check for: clear headline, CTA button, social proof, mobile responsive
   c. REWRITE the copy following copy-style.md rules
   d. Add/fix: meta tags, OG images, clear CTA, email capture form
   e. If site has no monetization (no link to product/service), ADD one
3. For sites that exist in code but aren't deployed:
   a. List them in OPS/DEPLOY_QUEUE.md with deployment commands
4. Write OPS/LANDING_OPTIMIZATION_REPORT.md:
   - Sites optimized, changes made, estimated impact

RULES:
- Focus on sites that can actually make money (product pages, service pages, lead capture)
- Skip vanity/portfolio sites unless they drive traffic
- All files stay in project root
"""
    _run_claude(prompt.replace('"', '\\"'), MODEL_SONNET, "landing_polish")


def full_cycle():
    """Run ALL builders in sequence."""
    print("=" * 60)
    print("OFFPEAK BUILDER — FULL CYCLE")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    refine_content()
    build_products()
    alpha_to_assets()
    refine_apps()
    outreach_ready()
    landing_polish()

    print("\n" + "=" * 60)
    print("FULL CYCLE COMPLETE")
    print("Check AUTOMATIONS/logs/offpeak_*.log for details")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Offpeak Builder — produce REAL assets")
    parser.add_argument("--refine-content", action="store_true")
    parser.add_argument("--build-products", action="store_true")
    parser.add_argument("--alpha-to-assets", action="store_true")
    parser.add_argument("--refine-apps", action="store_true")
    parser.add_argument("--outreach-ready", action="store_true")
    parser.add_argument("--landing-polish", action="store_true")
    parser.add_argument("--full-cycle", action="store_true")
    args = parser.parse_args()

    if args.refine_content: refine_content()
    elif args.build_products: build_products()
    elif args.alpha_to_assets: alpha_to_assets()
    elif args.refine_apps: refine_apps()
    elif args.outreach_ready: outreach_ready()
    elif args.landing_polish: landing_polish()
    elif args.full_cycle: full_cycle()
    else:
        print("No action specified. Use --full-cycle or a specific builder.")
        parser.print_help()


if __name__ == "__main__":
    main()
