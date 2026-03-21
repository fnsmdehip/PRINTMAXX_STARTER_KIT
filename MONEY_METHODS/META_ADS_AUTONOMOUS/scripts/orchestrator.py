#!/usr/bin/env python3
"""
Meta Ads Autonomous Orchestrator

Runs the full 6-step autonomous ad management loop:
  1. Health check (read campaigns, score performance)
  2. Fatigue detection (frequency > 3.5 = cooked)
  3. Auto-pause bleeders + budget shift to winners
  4. Copy generation from winning patterns
  5. Ad upload (new creative to Meta)
  6. Morning brief (Telegram/Slack delivery)

Usage:
  python3 orchestrator.py                  # Full loop
  python3 orchestrator.py --step health    # Single step
  python3 orchestrator.py --dry-run        # Read-only mode

Cron (daily 6AM):
  0 6 * * * cd /path/to/META_ADS_AUTONOMOUS && python3 scripts/orchestrator.py >> logs/orchestrator.log 2>&1

Requires:
  - social-cli installed (npm i -g social-cli)
  - Meta Marketing API credentials in config/credentials.env
  - ANTHROPIC_API_KEY or GROQ_API_KEY for copy generation
"""

import json
import csv
import os
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = LOGS_DIR / "health_reports"

def load_config():
    with open(CONFIG_DIR / "targets.json") as f:
        return json.load(f)

def load_env():
    env_file = CONFIG_DIR / "credentials.env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, val = line.partition("=")
            if key and val and key not in os.environ:
                os.environ[key] = val

def run_social_cli(cmd_args):
    """Run a social-cli command and return parsed JSON output."""
    try:
        result = subprocess.run(
            ["social-cli"] + cmd_args,
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            print(f"  [WARN] social-cli error: {result.stderr.strip()}")
            return None
        return json.loads(result.stdout) if result.stdout.strip() else None
    except FileNotFoundError:
        print("  [ERROR] social-cli not found. Install: npm i -g social-cli")
        return None
    except json.JSONDecodeError:
        return {"raw": result.stdout}

def step_health_check(config):
    """Step 1: Pull campaign data, answer the 5 daily questions."""
    print("\n[Step 1] Health Check")
    account_id = os.environ.get("META_AD_ACCOUNT_ID", "")
    if not account_id:
        print("  [SKIP] No META_AD_ACCOUNT_ID configured")
        return None

    data = run_social_cli(["meta", "campaigns", "--account", account_id, "--format", "json"])
    if not data:
        print("  [SKIP] Could not fetch campaign data")
        return None

    report = {
        "timestamp": datetime.now().isoformat(),
        "account_id": account_id,
        "campaigns": data if isinstance(data, list) else [data],
    }

    report_path = REPORTS_DIR / f"health_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"  Saved health report: {report_path.name}")
    return report

def step_fatigue_detection(config, health_report):
    """Step 2: Check frequency per ad, flag anything > threshold."""
    print("\n[Step 2] Fatigue Detection")
    threshold = config["global_defaults"]["frequency_fatigue_threshold"]
    fatigued = []

    if not health_report or "campaigns" not in health_report:
        print("  [SKIP] No campaign data")
        return fatigued

    for campaign in health_report.get("campaigns", []):
        ads = campaign.get("ads", [])
        for ad in ads:
            freq = ad.get("frequency", 0)
            if freq > threshold:
                fatigued.append({
                    "campaign_id": campaign.get("id", ""),
                    "ad_id": ad.get("id", ""),
                    "ad_name": ad.get("name", ""),
                    "frequency": freq,
                    "ctr": ad.get("ctr", 0),
                    "cpa": ad.get("cpa", 0),
                })

    if fatigued:
        print(f"  Found {len(fatigued)} fatigued ads (freq > {threshold})")
        with open(LOGS_DIR / "fatigue_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            for ad in fatigued:
                writer.writerow([
                    datetime.now().isoformat(),
                    ad["campaign_id"], ad["ad_id"], ad["ad_name"],
                    ad["frequency"], ad["ctr"], ad["cpa"], "flagged"
                ])
    else:
        print("  No fatigue detected")

    return fatigued

def step_auto_pause_and_shift(config, health_report, dry_run=False):
    """Step 3: Pause bleeders, shift budget to winners."""
    print("\n[Step 3] Auto-Pause + Budget Shift")
    kill_mult = config["global_defaults"]["cpa_kill_multiplier"]
    actions = []

    if not health_report:
        print("  [SKIP] No campaign data")
        return actions

    for campaign in health_report.get("campaigns", []):
        cid = campaign.get("id", "")
        cpa = campaign.get("cpa", 0)
        venture = campaign.get("venture", "")
        venture_config = config["ventures"].get(venture, {})
        target_cpa = venture_config.get("target_cpa", config["global_defaults"].get("default_target_cpa", 10))

        if cpa > target_cpa * kill_mult:
            action = f"PAUSE campaign {cid} (CPA ${cpa:.2f} > {kill_mult}x target ${target_cpa:.2f})"
            print(f"  {action}")
            if not dry_run:
                run_social_cli(["meta", "campaign", "pause", "--id", cid])
            actions.append(("pause", cid, "", f"CPA {cpa} > {kill_mult}x target {target_cpa}", cpa, "executed" if not dry_run else "dry_run"))

    if actions:
        with open(LOGS_DIR / "actions_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            for a in actions:
                writer.writerow([datetime.now().isoformat()] + list(a))
    else:
        print("  No bleeders found")

    return actions

def step_copy_generation(config, health_report, dry_run=False):
    """Step 4: Analyze winners, generate copy variations."""
    print("\n[Step 4] Copy Generation")
    if dry_run:
        print("  [DRY RUN] Skipping copy generation")
        return []
    print("  [TODO] Requires Claude/Groq API integration for copy generation")
    return []

def step_ad_upload(config, dry_run=False):
    """Step 5: Upload queued ads to Meta."""
    print("\n[Step 5] Ad Upload")
    queue_path = LOGS_DIR / "copy_queue.json"
    with open(queue_path) as f:
        queue = json.load(f)

    if not queue:
        print("  No ads in queue")
        return

    if dry_run:
        print(f"  [DRY RUN] Would upload {len(queue)} ads")
        return

    print(f"  [TODO] Upload {len(queue)} ads via social-cli")

def step_morning_brief(config, health_report, fatigued, actions):
    """Step 6: Compile and deliver brief."""
    print("\n[Step 6] Morning Brief")
    brief_lines = [
        f"Meta Ads Brief: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Campaigns checked: {len(health_report.get('campaigns', [])) if health_report else 0}",
        f"Fatigued ads: {len(fatigued)}",
        f"Actions taken: {len(actions)}",
    ]
    for line in brief_lines:
        print(f"  {line}")

    # Telegram delivery
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if bot_token and chat_id:
        import urllib.request
        msg = "\n".join(brief_lines)
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = json.dumps({"chat_id": chat_id, "text": msg}).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req, timeout=10)
            print("  Brief sent to Telegram")
        except Exception as e:
            print(f"  [WARN] Telegram send failed: {e}")
    else:
        print("  [SKIP] No Telegram credentials configured")

def main():
    load_env()
    config = load_config()
    dry_run = "--dry-run" in sys.argv
    single_step = None
    if "--step" in sys.argv:
        idx = sys.argv.index("--step")
        single_step = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None

    if dry_run:
        print("=== DRY RUN MODE (no write actions) ===")

    print(f"=== Meta Ads Autonomous Loop: {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")

    health_report = None
    fatigued = []
    actions = []

    if not single_step or single_step == "health":
        health_report = step_health_check(config)
    if not single_step or single_step == "fatigue":
        fatigued = step_fatigue_detection(config, health_report)
    if not single_step or single_step == "pause":
        actions = step_auto_pause_and_shift(config, health_report, dry_run)
    if not single_step or single_step == "copy":
        step_copy_generation(config, health_report, dry_run)
    if not single_step or single_step == "upload":
        step_ad_upload(config, dry_run)
    if not single_step or single_step == "brief":
        step_morning_brief(config, health_report, fatigued, actions)

    print("\n=== Loop complete ===")

if __name__ == "__main__":
    main()
