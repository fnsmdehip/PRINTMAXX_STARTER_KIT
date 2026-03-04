#!/usr/bin/env python3
"""
PRINTMAXX App Clone/Rebrand Pipeline
======================================
Identifies app clone opportunities across regions, languages, demographics,
and niches. Generates asset prompts (Nano Banana / ImageFX) and prepares
rebrand packages.

The factory model: find apps doing well in one market, clone/rebrand for
underserved markets. Same core, different skin.

Usage:
    python3 AUTOMATIONS/app_clone_pipeline.py --scan              # scan for opportunities
    python3 AUTOMATIONS/app_clone_pipeline.py --generate APPNAME  # generate rebrand package
    python3 AUTOMATIONS/app_clone_pipeline.py --status            # show pipeline stats
    python3 AUTOMATIONS/app_clone_pipeline.py --assets APPNAME    # generate asset prompts
    python3 AUTOMATIONS/app_clone_pipeline.py --matrix            # show full opportunity matrix

Cron:
    0 6 * * 1 cd $BASE && $PYTHON AUTOMATIONS/app_clone_pipeline.py --scan >> AUTOMATIONS/logs/app_clone.log 2>&1
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
APP_FACTORY = PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY"
CLONE_CSV = PROJECT_ROOT / "LEDGER" / "APP_CLONE_OPPORTUNITIES.csv"
OUTPUT_DIR = APP_FACTORY / "clone_packages"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, file=sys.stderr)
    safe_path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_DIR / "app_clone.log"), "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Clone dimensions
# ---------------------------------------------------------------------------
LANGUAGES = {
    "ar": {"name": "Arabic", "rtl": True, "markets": ["SA", "AE", "EG", "QA", "KW"],
            "app_store_demand": "HIGH", "competition": "LOW"},
    "es": {"name": "Spanish", "rtl": False, "markets": ["MX", "ES", "CO", "AR", "CL"],
            "app_store_demand": "HIGH", "competition": "MEDIUM"},
    "hi": {"name": "Hindi", "rtl": False, "markets": ["IN"],
            "app_store_demand": "VERY HIGH", "competition": "LOW"},
    "pt": {"name": "Portuguese", "rtl": False, "markets": ["BR", "PT"],
            "app_store_demand": "HIGH", "competition": "LOW"},
    "id": {"name": "Indonesian", "rtl": False, "markets": ["ID"],
            "app_store_demand": "HIGH", "competition": "VERY LOW"},
    "tr": {"name": "Turkish", "rtl": False, "markets": ["TR"],
            "app_store_demand": "MEDIUM", "competition": "LOW"},
    "ur": {"name": "Urdu", "rtl": True, "markets": ["PK"],
            "app_store_demand": "MEDIUM", "competition": "VERY LOW"},
    "fr": {"name": "French", "rtl": False, "markets": ["FR", "CA", "SN", "CI"],
            "app_store_demand": "MEDIUM", "competition": "MEDIUM"},
    "de": {"name": "German", "rtl": False, "markets": ["DE", "AT", "CH"],
            "app_store_demand": "MEDIUM", "competition": "MEDIUM"},
}

DEMOGRAPHICS = {
    "women": {"label": "Women-focused", "name_suffix": "Her", "color_palette": "soft pinks, lavender, rose gold",
              "icon_style": "elegant, feminine, minimal"},
    "teens": {"label": "Teen/Gen-Z", "name_suffix": "Z", "color_palette": "neon, gradient, dark mode",
              "icon_style": "bold, playful, Memphis design"},
    "seniors": {"label": "Senior-friendly", "name_suffix": "Plus", "color_palette": "high contrast, large text, blue",
                "icon_style": "simple, clear, accessible"},
    "students": {"label": "Student-focused", "name_suffix": "Study", "color_palette": "vibrant, academic, green",
                 "icon_style": "notebook, pen, graduation cap"},
    "professionals": {"label": "Professional", "name_suffix": "Pro", "color_palette": "navy, charcoal, gold accent",
                      "icon_style": "clean, corporate, sophisticated"},
    "faith": {"label": "Faith-based", "name_suffix": "Selah", "color_palette": "gold, white, deep blue",
              "icon_style": "sacred geometry, crescent/cross/om, peaceful"},
}

# Our existing apps that can be cloned
OUR_APPS = {
    "ramadan-tracker": {
        "category": "Lifestyle/Religion",
        "core_features": ["prayer times", "quran tracker", "fasting timer", "dhikr counter"],
        "current_languages": ["en", "ar"],
        "demographics": ["faith"],
        "clone_potential": {
            "languages": ["ur", "id", "tr", "fr"],
            "demographics": ["women", "seniors"],
            "niche_variants": [
                {"name": "LentTracker", "niche": "Catholic Lent", "features": ["40 day counter", "sacrifice tracker", "daily readings"]},
                {"name": "ShabbatMode", "niche": "Jewish Shabbat", "features": ["candle times", "torah portion", "meal planner"]},
            ],
        },
    },
    "focuslock": {
        "category": "Productivity",
        "core_features": ["app blocking", "focus timer", "usage stats", "streak tracking"],
        "current_languages": ["en"],
        "demographics": ["general"],
        "clone_potential": {
            "languages": ["es", "hi", "pt", "de", "fr"],
            "demographics": ["students", "professionals", "teens"],
            "niche_variants": [
                {"name": "StudyLock", "niche": "Students", "features": ["class schedule", "exam countdown", "study groups"]},
                {"name": "DeepWork", "niche": "Remote workers", "features": ["meeting blocker", "slack silencer", "pomodoro"]},
            ],
        },
    },
    "habitforge": {
        "category": "Health & Fitness",
        "core_features": ["habit tracking", "streaks", "reminders", "stats"],
        "current_languages": ["en"],
        "demographics": ["general"],
        "clone_potential": {
            "languages": ["es", "hi", "ar", "pt", "id", "tr"],
            "demographics": ["women", "teens", "seniors", "faith"],
            "niche_variants": [
                {"name": "SunnahTracker", "niche": "Islamic habits", "features": ["sunnah checklist", "adhkar counter", "fasting log"]},
                {"name": "GlowUp", "niche": "Women's wellness", "features": ["skincare routine", "cycle tracking", "water intake"]},
                {"name": "ElderFit", "niche": "Senior health", "features": ["medication reminders", "walk tracker", "large buttons"]},
            ],
        },
    },
    "mealmaxx": {
        "category": "Food & Drink",
        "core_features": ["meal planning", "calorie tracking", "grocery lists", "macros"],
        "current_languages": ["en"],
        "demographics": ["general"],
        "clone_potential": {
            "languages": ["es", "hi", "ar", "pt"],
            "demographics": ["women", "students", "faith"],
            "niche_variants": [
                {"name": "HalalBites", "niche": "Halal food", "features": ["halal restaurant finder", "halal certification check", "ramadan meal plans"]},
                {"name": "BudgetBites", "niche": "Student meals", "features": ["under $5 recipes", "dorm cooking", "meal prep"]},
            ],
        },
    },
    "sleepmaxx": {
        "category": "Health & Fitness",
        "core_features": ["sleep tracking", "bedtime reminders", "sleep sounds", "analytics"],
        "current_languages": ["en"],
        "demographics": ["general"],
        "clone_potential": {
            "languages": ["es", "hi", "pt", "de", "fr", "ar"],
            "demographics": ["women", "seniors", "teens"],
            "niche_variants": [
                {"name": "DreamJournal", "niche": "Lucid dreaming", "features": ["dream log", "reality checks", "sleep stages"]},
                {"name": "NapMaxx", "niche": "Power nappers", "features": ["smart nap timer", "caffeine calculator", "alertness tracking"]},
            ],
        },
    },
    "walktounlock": {
        "category": "Health & Fitness",
        "core_features": ["step counting", "phone locking", "rewards", "challenges"],
        "current_languages": ["en"],
        "demographics": ["general"],
        "clone_potential": {
            "languages": ["es", "hi", "pt", "id", "tr"],
            "demographics": ["teens", "seniors", "students"],
            "niche_variants": [
                {"name": "RunToUnlock", "niche": "Runners", "features": ["distance goals", "pace tracking", "route maps"]},
                {"name": "StepsForCharity", "niche": "Charity walking", "features": ["donate per step", "team challenges", "leaderboards"]},
            ],
        },
    },
}


# ---------------------------------------------------------------------------
# Opportunity scanning
# ---------------------------------------------------------------------------
def scan_opportunities() -> list[dict]:
    """Generate the full opportunity matrix."""
    opportunities = []
    opp_id = 1

    for app_name, app in OUR_APPS.items():
        clone_pot = app.get("clone_potential", {})

        # Language clones
        for lang_code in clone_pot.get("languages", []):
            lang = LANGUAGES.get(lang_code, {})
            score = 0
            if lang.get("app_store_demand") == "VERY HIGH":
                score += 40
            elif lang.get("app_store_demand") == "HIGH":
                score += 30
            elif lang.get("app_store_demand") == "MEDIUM":
                score += 20

            if lang.get("competition") == "VERY LOW":
                score += 30
            elif lang.get("competition") == "LOW":
                score += 25
            elif lang.get("competition") == "MEDIUM":
                score += 15

            # RTL bonus (harder to do, less competition)
            if lang.get("rtl"):
                score += 10

            opportunities.append({
                "opp_id": f"CLONE{opp_id:03d}",
                "base_app": app_name,
                "clone_type": "LANGUAGE",
                "target": f"{lang.get('name', lang_code)} ({', '.join(lang.get('markets', []))})",
                "new_name": f"{app_name.replace('-', '').title()} {lang.get('name', '')}",
                "score": min(score, 100),
                "effort": "MEDIUM" if lang.get("rtl") else "LOW",
                "status": "IDENTIFIED",
                "notes": f"Demand: {lang.get('app_store_demand')}, Competition: {lang.get('competition')}",
            })
            opp_id += 1

        # Demographic clones
        for demo_key in clone_pot.get("demographics", []):
            demo = DEMOGRAPHICS.get(demo_key, {})
            score = 60  # Demographics always score well
            opportunities.append({
                "opp_id": f"CLONE{opp_id:03d}",
                "base_app": app_name,
                "clone_type": "DEMOGRAPHIC",
                "target": demo.get("label", demo_key),
                "new_name": f"{app_name.replace('-', '').title()}{demo.get('name_suffix', '')}",
                "score": score,
                "effort": "LOW",
                "status": "IDENTIFIED",
                "notes": f"Palette: {demo.get('color_palette')}, Icon: {demo.get('icon_style')}",
            })
            opp_id += 1

        # Niche variant clones
        for variant in clone_pot.get("niche_variants", []):
            score = 70  # Niche variants score highest
            opportunities.append({
                "opp_id": f"CLONE{opp_id:03d}",
                "base_app": app_name,
                "clone_type": "NICHE_VARIANT",
                "target": variant.get("niche", ""),
                "new_name": variant.get("name", ""),
                "score": score,
                "effort": "MEDIUM",
                "status": "IDENTIFIED",
                "notes": f"Features: {', '.join(variant.get('features', []))}",
            })
            opp_id += 1

    # Sort by score
    opportunities.sort(key=lambda x: x["score"], reverse=True)
    return opportunities


def save_opportunities(opps: list[dict]) -> None:
    """Save opportunities to CSV."""
    safe_path(CLONE_CSV.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = ["opp_id", "base_app", "clone_type", "target", "new_name", "score", "effort", "status", "notes"]
    with open(safe_path(CLONE_CSV), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for opp in opps:
            writer.writerow(opp)
    log(f"Saved {len(opps)} clone opportunities to {CLONE_CSV}")


# ---------------------------------------------------------------------------
# Asset generation prompts
# ---------------------------------------------------------------------------
def generate_asset_prompts(app_name: str) -> str:
    """Generate Nano Banana / ImageFX prompts for an app."""
    app = OUR_APPS.get(app_name)
    if not app:
        return f"ERROR: App '{app_name}' not found. Available: {', '.join(OUR_APPS.keys())}"

    prompts = []
    prompts.append(f"# Asset Generation Prompts for {app_name}\n")
    prompts.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    clone_pot = app.get("clone_potential", {})

    # Base app icon
    prompts.append("## Base App Icon (1024x1024)")
    prompts.append(f"**Nano Banana prompt:**")
    prompts.append(f"A modern, minimal app icon for a {app['category'].lower()} app. ")
    prompts.append(f"Features: {', '.join(app['core_features'][:3])}. ")
    prompts.append("3D rendered, gradient background, single focal element, no text, ")
    prompts.append("professional quality, App Store ready, rounded corners.\n")

    # Demographic variants
    for demo_key in clone_pot.get("demographics", []):
        demo = DEMOGRAPHICS.get(demo_key, {})
        prompts.append(f"## {demo.get('label', demo_key)} Variant Icon")
        prompts.append(f"**Nano Banana prompt:**")
        prompts.append(f"A modern app icon for a {demo.get('label', '').lower()} {app['category'].lower()} app. ")
        prompts.append(f"Color palette: {demo.get('color_palette', 'modern gradient')}. ")
        prompts.append(f"Style: {demo.get('icon_style', 'clean, minimal')}. ")
        prompts.append("1024x1024, 3D rendered, no text, App Store ready, rounded corners.\n")

    # Language/region variants
    for lang_code in clone_pot.get("languages", []):
        lang = LANGUAGES.get(lang_code, {})
        prompts.append(f"## {lang.get('name', lang_code)} Market Variant Icon")
        prompts.append(f"**Nano Banana prompt:**")
        prompts.append(f"A modern app icon for the {', '.join(lang.get('markets', []))} market. ")
        prompts.append(f"{app['category'].lower()} app with cultural elements appropriate for {lang.get('name', '')} speakers. ")
        prompts.append("Professional, modern, 1024x1024, 3D rendered, no text, rounded corners.\n")

    # Niche variant icons
    for variant in clone_pot.get("niche_variants", []):
        prompts.append(f"## {variant.get('name', 'Variant')} Icon ({variant.get('niche', '')})")
        prompts.append(f"**Nano Banana prompt:**")
        prompts.append(f"A modern app icon for '{variant.get('name', '')}' - a {variant.get('niche', '').lower()} app. ")
        prompts.append(f"Core concept: {', '.join(variant.get('features', [])[:2])}. ")
        prompts.append("Unique, recognizable, 1024x1024, 3D rendered, no text, App Store ready.\n")

    # Screenshot templates
    prompts.append("## App Store Screenshots (6.5\" and 5.5\")")
    prompts.append("**For each variant, generate 5 screenshot backgrounds:**")
    prompts.append("1. Hero shot - main feature with gradient background")
    prompts.append("2. Feature showcase - 3 key features with icons")
    prompts.append("3. Before/after or progress visualization")
    prompts.append("4. Social proof / stats display")
    prompts.append("5. CTA - 'Start your journey' with app preview\n")

    return "\n".join(prompts)


# ---------------------------------------------------------------------------
# Rebrand package generation
# ---------------------------------------------------------------------------
def generate_rebrand_package(app_name: str) -> None:
    """Generate a full rebrand package for an app."""
    app = OUR_APPS.get(app_name)
    if not app:
        log(f"ERROR: App '{app_name}' not found.")
        return

    safe_path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    pkg_dir = safe_path(OUTPUT_DIR / app_name)
    pkg_dir.mkdir(parents=True, exist_ok=True)

    # Generate asset prompts
    prompts = generate_asset_prompts(app_name)
    with open(pkg_dir / "ASSET_PROMPTS.md", "w") as f:
        f.write(prompts)

    # Generate rebrand checklist
    clone_pot = app.get("clone_potential", {})
    checklist = []
    checklist.append(f"# Rebrand Checklist: {app_name}\n")
    checklist.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    total_variants = (
        len(clone_pot.get("languages", [])) +
        len(clone_pot.get("demographics", [])) +
        len(clone_pot.get("niche_variants", []))
    )
    checklist.append(f"**Total variants possible: {total_variants}**\n")

    checklist.append("## Per-Variant Checklist\n")
    checklist.append("For each clone variant, complete these steps:\n")
    checklist.append("- [ ] Choose new app name (check App Store availability)")
    checklist.append("- [ ] Generate app icon (use ASSET_PROMPTS.md)")
    checklist.append("- [ ] Update color scheme and branding")
    checklist.append("- [ ] Translate/adapt all UI strings")
    checklist.append("- [ ] Update App Store metadata (title, subtitle, keywords, description)")
    checklist.append("- [ ] Generate App Store screenshots (5 per device size)")
    checklist.append("- [ ] Update privacy policy URL")
    checklist.append("- [ ] Create new Apple Developer bundle ID")
    checklist.append("- [ ] Test on device/simulator")
    checklist.append("- [ ] Submit to App Store Review")
    checklist.append("- [ ] Set up ASO tracking for new keywords\n")

    checklist.append("## Language Variants\n")
    for lang_code in clone_pot.get("languages", []):
        lang = LANGUAGES.get(lang_code, {})
        checklist.append(f"### {lang.get('name', lang_code)} ({', '.join(lang.get('markets', []))})")
        checklist.append(f"- Demand: {lang.get('app_store_demand', 'Unknown')}")
        checklist.append(f"- Competition: {lang.get('competition', 'Unknown')}")
        checklist.append(f"- RTL support needed: {'Yes' if lang.get('rtl') else 'No'}")
        checklist.append(f"- Status: NOT STARTED\n")

    checklist.append("## Demographic Variants\n")
    for demo_key in clone_pot.get("demographics", []):
        demo = DEMOGRAPHICS.get(demo_key, {})
        checklist.append(f"### {demo.get('label', demo_key)}")
        checklist.append(f"- Name suffix: {demo.get('name_suffix', '')}")
        checklist.append(f"- Color palette: {demo.get('color_palette', '')}")
        checklist.append(f"- Icon style: {demo.get('icon_style', '')}")
        checklist.append(f"- Status: NOT STARTED\n")

    checklist.append("## Niche Variants\n")
    for variant in clone_pot.get("niche_variants", []):
        checklist.append(f"### {variant.get('name', 'Variant')} ({variant.get('niche', '')})")
        checklist.append(f"- Features: {', '.join(variant.get('features', []))}")
        checklist.append(f"- Status: NOT STARTED\n")

    with open(pkg_dir / "REBRAND_CHECKLIST.md", "w") as f:
        f.write("\n".join(checklist))

    log(f"Generated rebrand package for {app_name} at {pkg_dir}")
    log(f"  - ASSET_PROMPTS.md ({len(prompts)} chars)")
    log(f"  - REBRAND_CHECKLIST.md ({total_variants} variants)")


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
def show_matrix(opps: list[dict]) -> None:
    """Show the full opportunity matrix."""
    print("\n--- App Clone Opportunity Matrix ---\n")
    print(f"{'ID':<10} {'Base App':<18} {'Type':<15} {'Target':<30} {'New Name':<25} {'Score':<6} {'Effort':<8}")
    print("-" * 115)
    for opp in opps:
        print(f"{opp['opp_id']:<10} {opp['base_app']:<18} {opp['clone_type']:<15} "
              f"{opp['target'][:28]:<30} {opp['new_name'][:23]:<25} {opp['score']:<6} {opp['effort']:<8}")

    # Summary
    by_type = {}
    for opp in opps:
        t = opp["clone_type"]
        by_type[t] = by_type.get(t, 0) + 1
    print(f"\n  Total: {len(opps)} opportunities")
    for t, count in by_type.items():
        print(f"    {t}: {count}")

    avg_score = sum(int(o["score"]) for o in opps) / len(opps) if opps else 0
    print(f"  Average score: {avg_score:.0f}/100")
    print(f"  Top 5 by score:")
    sorted_opps = sorted(opps, key=lambda x: int(x["score"]), reverse=True)
    for opp in sorted_opps[:5]:
        print(f"    {opp['opp_id']} {opp['new_name']} ({opp['target']}) - {opp['score']}/100")
    print()


def show_status() -> None:
    """Show pipeline status."""
    print("--- App Clone Pipeline Status ---\n")

    # Apps available
    print(f"  Base apps available: {len(OUR_APPS)}")
    for name in OUR_APPS:
        clone_pot = OUR_APPS[name].get("clone_potential", {})
        variants = (
            len(clone_pot.get("languages", [])) +
            len(clone_pot.get("demographics", [])) +
            len(clone_pot.get("niche_variants", []))
        )
        print(f"    {name}: {variants} clone variants possible")

    # Languages
    print(f"\n  Languages supported: {len(LANGUAGES)}")
    for code, lang in LANGUAGES.items():
        print(f"    {code}: {lang['name']} (demand: {lang['app_store_demand']}, competition: {lang['competition']})")

    # Demographics
    print(f"\n  Demographic targets: {len(DEMOGRAPHICS)}")
    for key, demo in DEMOGRAPHICS.items():
        print(f"    {key}: {demo['label']}")

    # Existing clone CSV
    if CLONE_CSV.exists():
        with open(CLONE_CSV) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        print(f"\n  Clone opportunities CSV: {len(rows)} entries")
    else:
        print(f"\n  Clone opportunities CSV: Not generated yet (run --scan)")

    # Packages
    if OUTPUT_DIR.exists():
        packages = [d for d in OUTPUT_DIR.iterdir() if d.is_dir()]
        print(f"  Rebrand packages generated: {len(packages)}")
        for pkg in packages:
            print(f"    {pkg.name}/")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="App Clone/Rebrand Pipeline")
    parser.add_argument("--scan", action="store_true", help="Scan for clone opportunities")
    parser.add_argument("--generate", type=str, help="Generate rebrand package for APP_NAME")
    parser.add_argument("--assets", type=str, help="Generate asset prompts for APP_NAME")
    parser.add_argument("--matrix", action="store_true", help="Show full opportunity matrix")
    parser.add_argument("--status", action="store_true", help="Show pipeline status")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.scan:
        log("Scanning clone opportunities...")
        opps = scan_opportunities()
        save_opportunities(opps)
        show_matrix(opps)
        log(f"Scan complete: {len(opps)} opportunities identified")
        return

    if args.matrix:
        opps = scan_opportunities()
        show_matrix(opps)
        return

    if args.generate:
        generate_rebrand_package(args.generate)
        return

    if args.assets:
        prompts = generate_asset_prompts(args.assets)
        print(prompts)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
