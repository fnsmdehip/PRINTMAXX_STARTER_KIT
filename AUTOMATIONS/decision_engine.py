#!/usr/bin/env python3
"""
PRINTMAXX Decision Engine — Closed-Loop Autonomous Business Agent

Replaces the old "scan → CSV → nothing" pattern with:
scan → analyze → decide → act → log → learn

Runs as a persistent daemon. Each cycle:
1. Reads all data sources (CSVs, logs, output dirs)
2. Scores opportunities using configurable thresholds
3. Takes action (generate listings, draft responses, create content, deploy)
4. Logs every decision with reasoning for audit trail
5. Updates progress trackers

Uses Claude Agent SDK when LLM judgment is needed.
Falls back to rule-based decisions for simple threshold checks.

Usage:
  python3 AUTOMATIONS/decision_engine.py --cycle          # Run one decision cycle
  python3 AUTOMATIONS/decision_engine.py --daemon         # Run continuously (every 30min)
  python3 AUTOMATIONS/decision_engine.py --status         # Show pipeline status
  python3 AUTOMATIONS/decision_engine.py --dry-run        # Show what would happen without acting
  python3 AUTOMATIONS/decision_engine.py --fix-broken     # Diagnose and fix broken cron jobs
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# === SAFETY ===
PROJECT_ROOT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
DECISION_LOG = PROJECT_ROOT / "AUTOMATIONS" / "logs" / "decision_engine.log"
DECISION_LEDGER = PROJECT_ROOT / "LEDGER" / "DECISIONS.csv"
OUTPUT_DIR = PROJECT_ROOT / "ralph" / "loops" / "spreadsheet_buildout" / "output"

def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root")
    return resolved

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    with open(DECISION_LOG, "a") as f:
        f.write(line + "\n")

def log_decision(source, action, reasoning, outcome="PENDING"):
    """Append to decisions ledger for full audit trail."""
    safe_path(DECISION_LEDGER)
    row = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "action": action,
        "reasoning": reasoning,
        "outcome": outcome,
    }
    exists = DECISION_LEDGER.exists()
    with open(DECISION_LEDGER, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=row.keys())
        if not exists:
            w.writeheader()
        w.writerow(row)


# === DATA READERS ===

def read_csv_tail(filepath, n=50):
    """Read last N rows of a CSV file."""
    p = safe_path(filepath)
    if not p.exists():
        return []
    rows = []
    with open(p, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            if len(rows) > n * 2:
                rows = rows[-n:]
    return rows[-n:]

def count_csv_rows(filepath):
    p = safe_path(filepath)
    if not p.exists():
        return 0
    with open(p, "r") as f:
        return sum(1 for _ in f) - 1  # minus header


# === DECISION MODULES ===

class FreelancePipeline:
    """Process freelance demand scan results into actionable responses."""

    SOURCE = PROJECT_ROOT / "LEDGER" / "FREELANCE_DEMAND_SCAN.csv"
    OUTPUT = PROJECT_ROOT / "CONTENT" / "freelance_responses"

    def analyze(self, dry_run=False):
        rows = read_csv_tail(self.SOURCE, 100)
        if not rows:
            log("Freelance: No data found")
            return []

        actions = []
        for row in rows:
            score = float(row.get("score", row.get("relevance_score", 0)) or 0)
            title = row.get("title", row.get("post_title", "unknown"))
            url = row.get("url", row.get("post_url", ""))
            subreddit = row.get("subreddit", "unknown")
            processed = row.get("processed", row.get("response_generated", ""))

            if score >= 60 and not processed:
                action = {
                    "type": "freelance_response",
                    "title": title,
                    "url": url,
                    "subreddit": subreddit,
                    "score": score,
                    "reasoning": f"Score {score} >= 60 threshold. Subreddit: {subreddit}",
                }
                actions.append(action)

        hot = [a for a in actions if a["score"] >= 80]
        warm = [a for a in actions if 60 <= a["score"] < 80]

        log(f"Freelance: {len(hot)} HOT, {len(warm)} WARM opportunities from last 100 rows")

        if not dry_run and (hot or warm):
            self._generate_responses(hot[:5] + warm[:3])

        return actions

    def _generate_responses(self, opportunities):
        """Generate draft responses for top opportunities."""
        self.OUTPUT.mkdir(parents=True, exist_ok=True)

        for opp in opportunities:
            # Check if response already exists
            slug = opp["title"][:50].replace(" ", "_").replace("/", "_")
            outfile = self.OUTPUT / f"response_{slug}_{datetime.now().strftime('%Y%m%d')}.md"
            if outfile.exists():
                continue

            content = f"""# Freelance Response Draft
## Post: {opp['title']}
## URL: {opp['url']}
## Subreddit: r/{opp['subreddit']}
## Score: {opp['score']}
## Generated: {datetime.now().isoformat()}

---

### Response Template

Hi! I specialize in exactly this type of work.

**What I'd deliver:**
- [Specific deliverable matching their ask]
- Timeline: [realistic estimate]
- Includes: [bonus value-add]

**Relevant experience:**
- [Similar project with specific outcome]
- [Tool/tech stack match]

Happy to discuss scope and timeline. DM me or check my portfolio at [link].

---

### Notes for Human Review
- Customize the deliverable to match EXACTLY what they asked for
- Add specific portfolio piece URL
- Check r/{opp['subreddit']} rules for self-promotion
- Status: PENDING_REVIEW
"""
            safe_path(outfile)
            outfile.write_text(content)
            log(f"Freelance: Generated response draft for '{opp['title'][:40]}...'")
            log_decision("freelance_demand", f"draft_response:{slug}", opp["reasoning"])


class EcomArbPipeline:
    """Process ecom arbitrage opportunities into listing drafts."""

    SOURCE = PROJECT_ROOT / "LEDGER" / "ECOM_ARB_OPPORTUNITIES.csv"
    OUTPUT = PROJECT_ROOT / "CONTENT" / "ecom_listings"

    def analyze(self, dry_run=False):
        rows = read_csv_tail(self.SOURCE, 100)
        if not rows:
            log("Ecom Arb: No data found")
            return []

        actions = []
        for row in rows:
            margin = float(row.get("margin_pct", row.get("margin", 0)) or 0)
            action_flag = row.get("action", row.get("recommendation", "")).upper()
            product = row.get("product", row.get("product_name", "unknown"))
            source_price = row.get("source_price", row.get("buy_price", "?"))
            sell_price = row.get("sell_price", row.get("target_price", "?"))

            if margin >= 25 or "LIST" in action_flag:
                actions.append({
                    "type": "ecom_listing",
                    "product": product,
                    "margin": margin,
                    "source_price": source_price,
                    "sell_price": sell_price,
                    "reasoning": f"Margin {margin}% >= 25% threshold, action={action_flag}",
                })

        log(f"Ecom Arb: {len(actions)} listable products from last 100 rows")

        if not dry_run and actions:
            self._generate_listings(actions[:10])

        return actions

    def _generate_listings(self, products):
        """Generate marketplace listing drafts."""
        self.OUTPUT.mkdir(parents=True, exist_ok=True)

        for prod in products:
            slug = prod["product"][:40].replace(" ", "_").replace("/", "_")
            outfile = self.OUTPUT / f"listing_{slug}_{datetime.now().strftime('%Y%m%d')}.md"
            if outfile.exists():
                continue

            content = f"""# Ecom Listing Draft
## Product: {prod['product']}
## Source Price: {prod['source_price']}
## Sell Price: {prod['sell_price']}
## Margin: {prod['margin']}%
## Generated: {datetime.now().isoformat()}

---

### FB Marketplace Listing

**Title:** {prod['product']}
**Price:** ${prod['sell_price']}
**Category:** [Auto-detect]
**Condition:** New
**Description:**
Brand new, ships fast. Message me for bulk pricing.

### eBay Listing

**Title:** {prod['product']} - Fast Free Shipping
**Price:** ${prod['sell_price']}
**Shipping:** Free (built into price)

---

### Action Required
- Status: PENDING_REVIEW
- Need: Platform accounts (FB Marketplace, eBay)
- Blocker: Account creation (see OPS/ACCOUNT_CREATION_NOW.md)
"""
            safe_path(outfile)
            outfile.write_text(content)
            log(f"Ecom: Generated listing for '{prod['product'][:30]}...' ({prod['margin']}% margin)")
            log_decision("ecom_arb", f"listing_draft:{slug}", prod["reasoning"])


class AlphaPipeline:
    """Process alpha staging entries into actionable content or strategy updates."""

    SOURCE = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
    BACKTEST = PROJECT_ROOT / "LEDGER" / "BACKTESTS" / "BACKTEST_RESULTS.csv"
    OUTPUT = PROJECT_ROOT / "CONTENT" / "alpha_actions"

    def analyze(self, dry_run=False):
        # Check backtest results for SCALE verdicts
        bt_rows = read_csv_tail(self.BACKTEST, 200)
        scale = [r for r in bt_rows if r.get("verdict", "").upper() == "SCALE"]
        paper = [r for r in bt_rows if r.get("verdict", "").upper() == "PAPER_TRADE"]

        log(f"Alpha: {len(scale)} SCALE, {len(paper)} PAPER_TRADE from backtest results")

        if not dry_run and scale:
            self._escalate_scale_items(scale)

        return {"scale": len(scale), "paper_trade": len(paper)}

    def _escalate_scale_items(self, items):
        """Create action items for SCALE-worthy alpha."""
        self.OUTPUT.mkdir(parents=True, exist_ok=True)

        for item in items[:5]:
            method = item.get("method", item.get("alpha_id", "unknown"))
            outfile = self.OUTPUT / f"scale_{method}_{datetime.now().strftime('%Y%m%d')}.md"
            if outfile.exists():
                continue

            content = f"""# SCALE ALERT — {method}
## Verdict: SCALE (backtest passed)
## Generated: {datetime.now().isoformat()}

---

### What This Means
The alpha screening system backtested this method and it passed the SCALE threshold.
This means it should be actively deployed, not just tracked.

### Source Data
{json.dumps(item, indent=2, default=str)}

### Next Actions
1. Review the method details above
2. Check if required accounts/tools exist
3. Deploy if ready, or add to OPS/PERSISTENT_TASK_TRACKER.md
4. Status: PENDING_REVIEW
"""
            safe_path(outfile)
            outfile.write_text(content)
            log(f"Alpha: Escalated SCALE item '{method}'")
            log_decision("alpha_screening", f"scale_escalation:{method}",
                        f"Backtest verdict=SCALE, auto-escalated for review")


class ContentIntegrationPipeline:
    """Move ralph loop output into proper content directories and deployment pipeline."""

    def analyze(self, dry_run=False):
        if not OUTPUT_DIR.exists():
            log("Content Integration: No spreadsheet buildout output found")
            return {}

        dirs = [d for d in OUTPUT_DIR.iterdir() if d.is_dir()]
        total_files = sum(1 for d in dirs for _ in d.rglob("*") if _.is_file())

        # Check what's already been integrated
        integrated_marker = OUTPUT_DIR / ".integrated"
        already_done = set()
        if integrated_marker.exists():
            already_done = set(integrated_marker.read_text().strip().split("\n"))

        new_dirs = [d for d in dirs if d.name not in already_done]

        log(f"Content Integration: {len(dirs)} output dirs, {len(new_dirs)} not yet integrated, {total_files} total files")

        if not dry_run and new_dirs:
            self._integrate_outputs(new_dirs, integrated_marker, already_done)

        return {"total_dirs": len(dirs), "new": len(new_dirs), "files": total_files}

    def _integrate_outputs(self, dirs, marker_file, already_done):
        """Copy relevant outputs to proper content directories."""
        content_base = PROJECT_ROOT / "CONTENT"

        mapping = {
            "C": "social",        # Content ops → social content
            "E": "ecom",          # Ecom → ecom content
            "D": "digital",       # Digital products
            "S": "services",      # Services
            "A": "apps",          # Apps
            "P": "personas",      # Personas
            "I": "invest",        # Investment
            "M": "community",     # Community
            "F": "affiliate",     # Affiliate
            "G": "growth",        # Growth
            "N": "growth",        # N-series → growth
        }

        integrated = list(already_done)

        for d in dirs:
            # Determine category from dir name prefix
            prefix = d.name[0].upper()
            category = mapping.get(prefix, "misc")
            target = content_base / category / "buildout" / d.name

            if target.exists():
                integrated.append(d.name)
                continue

            target.mkdir(parents=True, exist_ok=True)

            # Copy files (not move — keep originals)
            import shutil
            for f in d.rglob("*"):
                if f.is_file():
                    dest = target / f.relative_to(d)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    safe_path(dest)
                    shutil.copy2(f, dest)

            log(f"Content Integration: Integrated {d.name} → CONTENT/{category}/buildout/{d.name}")
            log_decision("content_integration", f"integrated:{d.name}",
                        f"Moved {sum(1 for _ in d.rglob('*') if _.is_file())} files to content pipeline")
            integrated.append(d.name)

        safe_path(marker_file)
        marker_file.write_text("\n".join(integrated))


class BrokenCronFixer:
    """Diagnose and fix broken cron jobs."""

    KNOWN_ISSUES = {
        "sam_gov_monitor.py": {
            "symptom": "HTTP 404 on every keyword",
            "fix": "Need SAM_GOV_API_KEY env var. Get free key at https://api.data.gov/signup/",
            "severity": "LOW",  # Gov contracts are long-term play
        },
        "hashtag_audio_tracking.py": {
            "symptom": "brotli decode error on Brave search, subreddit 403/404",
            "fix": "Install brotli: pip3 install brotli. Fix subreddit names (r/TikTokTrending doesn't exist)",
            "severity": "MEDIUM",
        },
        "trend_aggregator.py": {
            "symptom": "5 of 6 daily runs produce 0 signals",
            "fix": "Rate limiting. Reduce frequency from every 4h to every 8h. Add retry with backoff.",
            "severity": "MEDIUM",
        },
        "platform_algo_detection.py": {
            "symptom": "Brave search fails with brotli error",
            "fix": "Same brotli fix. Install: pip3 install brotli",
            "severity": "LOW",
        },
    }

    def diagnose(self):
        log("=== BROKEN CRON DIAGNOSIS ===")
        fixes = []

        for script, info in self.KNOWN_ISSUES.items():
            log(f"  {script}: {info['symptom']}")
            log(f"    Fix: {info['fix']}")
            log(f"    Severity: {info['severity']}")
            fixes.append(info)

        return fixes

    def fix(self, dry_run=False):
        fixes_applied = []

        # Fix 1: Install brotli
        if not dry_run:
            try:
                import brotli
                log("brotli already installed")
            except ImportError:
                log("Installing brotli for Brave search fix...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "brotli"],
                    capture_output=True, text=True, timeout=60
                )
                if result.returncode == 0:
                    log("brotli installed successfully")
                    fixes_applied.append("brotli_install")
                else:
                    log(f"brotli install failed: {result.stderr[:200]}", "ERROR")

        return fixes_applied


class CronOptimizer:
    """Analyze and optimize cron schedule."""

    def analyze(self):
        """Check which action scripts exist but aren't in cron."""
        missing_from_cron = []

        action_scripts = [
            ("auto_freelance_responder.py", "Responds to hot freelance posts", "*/3"),
            ("arb_listing_generator.py", "Generates listings from arb opportunities", "*/4"),
            ("trend_to_listing.py", "Converts trends to product listings", "*/6"),
            ("ecom_autopilot.py", "Auto-manages ecom pipeline", "*/4"),
        ]

        for script, desc, freq in action_scripts:
            path = PROJECT_ROOT / "AUTOMATIONS" / script
            if path.exists():
                # Check if it's in active crontab
                result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
                if script not in result.stdout:
                    missing_from_cron.append({
                        "script": script,
                        "description": desc,
                        "suggested_frequency": freq,
                        "exists": True,
                    })
                    log(f"Cron gap: {script} exists but NOT in crontab ({desc})")

        return missing_from_cron


# === MAIN ENGINE ===

def run_cycle(dry_run=False):
    """Run one full decision cycle across all pipelines."""
    log("=" * 60)
    log(f"DECISION ENGINE CYCLE START {'(DRY RUN)' if dry_run else ''}")
    log("=" * 60)

    results = {}

    # Run all pipelines
    pipelines = [
        ("freelance", FreelancePipeline()),
        ("ecom_arb", EcomArbPipeline()),
        ("alpha", AlphaPipeline()),
        ("content_integration", ContentIntegrationPipeline()),
    ]

    for name, pipeline in pipelines:
        try:
            results[name] = pipeline.analyze(dry_run=dry_run)
        except Exception as e:
            log(f"{name}: ERROR — {e}", "ERROR")
            results[name] = {"error": str(e)}

    # Summary
    log("=" * 60)
    log("CYCLE COMPLETE — SUMMARY")
    for name, result in results.items():
        log(f"  {name}: {result}")
    log("=" * 60)

    return results


def run_daemon():
    """Run continuously, one cycle every 30 minutes."""
    log("DECISION ENGINE DAEMON STARTING — Ctrl+C to stop")
    log("Cycle interval: 30 minutes")

    while True:
        try:
            run_cycle(dry_run=False)
            log("Sleeping 30 minutes until next cycle...")
            time.sleep(1800)
        except KeyboardInterrupt:
            log("DAEMON STOPPED by user")
            break
        except Exception as e:
            log(f"CYCLE FAILED: {e} — retrying in 5 minutes", "ERROR")
            time.sleep(300)


def show_status():
    """Show current pipeline status."""
    print("=" * 60)
    print("PRINTMAXX DECISION ENGINE STATUS")
    print("=" * 60)

    # Data source sizes
    sources = {
        "Freelance Demand": PROJECT_ROOT / "LEDGER" / "FREELANCE_DEMAND_SCAN.csv",
        "Ecom Arb": PROJECT_ROOT / "LEDGER" / "ECOM_ARB_OPPORTUNITIES.csv",
        "Alpha Staging": PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv",
        "Backtest Results": PROJECT_ROOT / "LEDGER" / "BACKTESTS" / "BACKTEST_RESULTS.csv",
        "Decisions Log": DECISION_LEDGER,
    }

    print("\nDATA SOURCES:")
    for name, path in sources.items():
        count = count_csv_rows(path) if path.exists() else 0
        age = ""
        if path.exists():
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            age = f" (updated {mtime.strftime('%Y-%m-%d %H:%M')})"
        print(f"  {name}: {count:,} rows{age}")

    # Output integration status
    if OUTPUT_DIR.exists():
        dirs = [d for d in OUTPUT_DIR.iterdir() if d.is_dir()]
        marker = OUTPUT_DIR / ".integrated"
        integrated = set()
        if marker.exists():
            integrated = set(marker.read_text().strip().split("\n"))
        print(f"\nBUILDOUT OUTPUT: {len(dirs)} dirs, {len(integrated)} integrated")

    # Action outputs
    action_dirs = [
        ("Freelance Responses", PROJECT_ROOT / "CONTENT" / "freelance_responses"),
        ("Ecom Listings", PROJECT_ROOT / "CONTENT" / "ecom_listings"),
        ("Alpha Actions", PROJECT_ROOT / "CONTENT" / "alpha_actions"),
    ]

    print("\nACTION OUTPUTS:")
    for name, path in action_dirs:
        count = len(list(path.glob("*.md"))) if path.exists() else 0
        print(f"  {name}: {count} drafts")

    # Decision log
    if DECISION_LEDGER.exists():
        decisions = count_csv_rows(DECISION_LEDGER)
        print(f"\nDECISIONS LOGGED: {decisions}")

    # Broken cron diagnosis
    print("\nBROKEN CRON JOBS:")
    fixer = BrokenCronFixer()
    for script, info in fixer.KNOWN_ISSUES.items():
        print(f"  {script}: {info['symptom']} [{info['severity']}]")

    # Missing action scripts in cron
    print("\nMISSING FROM CRON (exist but not scheduled):")
    optimizer = CronOptimizer()
    missing = optimizer.analyze()
    if not missing:
        print("  All action scripts are in cron")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Decision Engine")
    parser.add_argument("--cycle", action="store_true", help="Run one decision cycle")
    parser.add_argument("--daemon", action="store_true", help="Run continuously")
    parser.add_argument("--status", action="store_true", help="Show pipeline status")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without executing")
    parser.add_argument("--fix-broken", action="store_true", help="Fix broken cron jobs")

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.fix_broken:
        fixer = BrokenCronFixer()
        fixer.diagnose()
        fixer.fix(dry_run=False)
    elif args.daemon:
        run_daemon()
    elif args.cycle or args.dry_run:
        run_cycle(dry_run=args.dry_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
