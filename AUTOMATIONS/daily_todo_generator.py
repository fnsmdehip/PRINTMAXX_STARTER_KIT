#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Daily TODO Generator
================================
Auto-generates a prioritized daily TODO report by scanning:
1. Overnight scraper results (what new data came in)
2. ALPHA_STAGING.csv (pending review items)
3. Lead CSVs (new leads to contact)
4. App deployment status
5. Content ready to publish
6. Revenue tracking gaps

Outputs: OPS/DAILY_TODO_[date].md

Run: python3 AUTOMATIONS/daily_todo_generator.py
Cron: 8:30 AM daily (after overnight scrapers finish)
"""

import csv
import os
import json
from datetime import datetime, date, timedelta
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent
LEDGER = BASE_DIR / "LEDGER"
AUTOMATIONS = BASE_DIR / "AUTOMATIONS"
LEADS_DIR = AUTOMATIONS / "leads"
LOGS_DIR = AUTOMATIONS / "logs"
OPS = BASE_DIR / "OPS"
CONTENT = BASE_DIR / "CONTENT"
APP_OUTPUT = BASE_DIR / "ralph" / "loops" / "app_factory" / "output"

TODAY = date.today().isoformat()

def count_csv_rows(filepath, date_filter=None):
    """Count rows in CSV, optionally filtering by date column"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if date_filter:
                rows = [r for r in rows if date_filter in str(r.get('date', r.get('discovered_date', r.get('created_date', ''))))]
            return len(rows)
    except Exception:
        return 0

def check_overnight_results():
    """Check what overnight scrapers produced"""
    results = []
    status_file = LOGS_DIR / f"overnight_status_{TODAY}.json"
    log_file = LOGS_DIR / f"overnight_{TODAY}.log"

    if status_file.exists():
        try:
            with open(status_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and line != '[]':
                        try:
                            entry = json.loads(line)
                            results.append(entry)
                        except json.JSONDecodeError:
                            pass
        except Exception:
            pass

    success = sum(1 for r in results if r.get('status') == 'SUCCESS')
    failed = sum(1 for r in results if r.get('status') == 'FAILED')
    timeout = sum(1 for r in results if r.get('status') == 'TIMEOUT')

    return {
        'ran': len(results) > 0,
        'success': success,
        'failed': failed,
        'timeout': timeout,
        'details': results
    }

def check_pending_alpha():
    """Count pending alpha entries"""
    alpha_file = LEDGER / "ALPHA_STAGING.csv"
    if not alpha_file.exists():
        return {'total': 0, 'pending': 0, 'approved': 0, 'today': 0}

    with open(alpha_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    pending = sum(1 for r in rows if r.get('status', '').strip() == 'PENDING_REVIEW')
    approved = sum(1 for r in rows if r.get('status', '').strip() == 'APPROVED')
    today_new = sum(1 for r in rows if TODAY in str(r.get('discovered_date', r.get('date', ''))))

    return {'total': len(rows), 'pending': pending, 'approved': approved, 'today': today_new}

def check_new_leads():
    """Check for new lead data"""
    lead_info = []
    if LEADS_DIR.exists():
        for f in LEADS_DIR.glob("*.csv"):
            mod_time = datetime.fromtimestamp(f.stat().st_mtime)
            if (datetime.now() - mod_time).days < 1:
                rows = count_csv_rows(f)
                lead_info.append({
                    'file': f.name,
                    'rows': rows,
                    'size': f.stat().st_size,
                    'updated': mod_time.strftime('%H:%M')
                })
    return lead_info

def check_app_status():
    """Check PWA app deployment status"""
    apps = []
    if APP_OUTPUT.exists():
        for app_dir in APP_OUTPUT.iterdir():
            if app_dir.is_dir():
                has_index = (app_dir / "index.html").exists()
                has_vercel = (app_dir / "vercel.json").exists()
                has_manifest = (app_dir / "manifest.json").exists()
                has_sw = (app_dir / "sw.js").exists()

                # Check if deployed (look for .vercel dir or deployment URL)
                deployed = (app_dir / ".vercel").exists()

                apps.append({
                    'name': app_dir.name,
                    'has_index': has_index,
                    'has_vercel': has_vercel,
                    'has_manifest': has_manifest,
                    'pwa_ready': has_index and has_manifest and has_sw,
                    'deployed': deployed
                })
    return apps

def check_content_ready():
    """Check content ready to publish"""
    ready = []

    # Check Buffer CSVs
    posting_dir = AUTOMATIONS / "content_posting"
    if posting_dir.exists():
        for f in posting_dir.glob("*.csv"):
            rows = count_csv_rows(f)
            if rows > 0:
                ready.append(f"Buffer CSV: {f.name} ({rows} posts)")

    # Check content dirs
    for subdir in ['social', 'medium_articles', 'substack_posts', 'email_sequences']:
        content_path = CONTENT / subdir
        if content_path.exists():
            files = list(content_path.rglob("*.md"))
            if files:
                ready.append(f"{subdir}: {len(files)} files")

    return ready

def check_revenue_status():
    """Check revenue tracking"""
    rev_file = BASE_DIR / "FINANCIALS" / "REVENUE_TRACKER.csv"
    if rev_file.exists():
        rows = count_csv_rows(rev_file)
        return {'tracked': True, 'entries': rows}
    return {'tracked': False, 'entries': 0}

def check_human_blockers():
    """Check for things that need human action"""
    blockers = []

    # Check if Vercel is logged in
    vercel_dir = Path.home() / ".vercel"
    if not vercel_dir.exists():
        blockers.append("Vercel login needed: `vercel login` (blocks all app deployments)")

    # Check for pending purchases
    checkpoints_dir = BASE_DIR / "ralph" / "loops" / "mega" / "checkpoints"
    if checkpoints_dir.exists():
        for f in checkpoints_dir.glob("PENDING_*"):
            blockers.append(f"Review: {f.name}")

    # Check if social accounts created
    accounts_file = LEDGER / "ACCOUNTS.csv"
    if accounts_file.exists():
        pending = count_csv_rows(accounts_file)  # All are PENDING
        if pending > 0:
            blockers.append(f"{pending} social accounts still need manual creation")

    return blockers

def generate_report():
    """Generate the full daily TODO report"""
    overnight = check_overnight_results()
    alpha = check_pending_alpha()
    leads = check_new_leads()
    apps = check_app_status()
    content = check_content_ready()
    revenue = check_revenue_status()
    blockers = check_human_blockers()

    report = f"""# PRINTMAXX Daily TODO - {TODAY}
*Auto-generated at {datetime.now().strftime('%H:%M')}*

## Overnight Results
"""

    if overnight['ran']:
        report += f"""
| Metric | Count |
|--------|-------|
| Scripts ran | {overnight['success'] + overnight['failed'] + overnight['timeout']} |
| Succeeded | {overnight['success']} |
| Failed | {overnight['failed']} |
| Timed out | {overnight['timeout']} |
"""
    else:
        report += "\nNo overnight run detected. Check cron: `crontab -l`\n"

    report += f"""
## Priority 1: Human Blockers (Do These First)

"""
    if blockers:
        for b in blockers:
            report += f"- [ ] {b}\n"
    else:
        report += "No blockers. Everything automated is running.\n"

    report += f"""
## Priority 2: Alpha Review ({alpha['pending']} pending)

- Total alpha: {alpha['total']}
- Pending review: {alpha['pending']}
- Approved: {alpha['approved']}
- New today: {alpha['today']}

"""
    if alpha['pending'] > 0:
        report += f"- [ ] Review alpha: `python3 AUTOMATIONS/alpha_screening.py --pending`\n"
        report += f"- [ ] Or run `/review-alpha` in Claude Code\n"

    report += f"""
## Priority 3: New Leads ({sum(l['rows'] for l in leads)} across {len(leads)} files)

"""
    if leads:
        report += "| File | Rows | Updated |\n|------|------|---------|\n"
        for l in sorted(leads, key=lambda x: x['rows'], reverse=True):
            report += f"| {l['file']} | {l['rows']} | {l['updated']} |\n"
        report += "\n- [ ] Review top leads and start outreach\n"
        report += "- [ ] Run mass outreach: `python3 AUTOMATIONS/mass_outreach.py`\n"
    else:
        report += "No new leads today. Check scraper logs.\n"

    report += f"""
## Priority 4: App Deployments ({sum(1 for a in apps if a['deployed'])}/{len(apps)} deployed)

"""
    if apps:
        report += "| App | PWA Ready | Deployed |\n|-----|-----------|----------|\n"
        for a in apps:
            pwa = "YES" if a['pwa_ready'] else "NO"
            dep = "YES" if a['deployed'] else "NO"
            report += f"| {a['name']} | {pwa} | {dep} |\n"

        undeployed = [a for a in apps if not a['deployed'] and a['pwa_ready']]
        if undeployed:
            report += f"\n- [ ] Deploy {len(undeployed)} apps: need `vercel login` first\n"
            for a in undeployed:
                report += f"  - `cd ralph/loops/app_factory/output/{a['name']} && vercel deploy --prod`\n"

    report += f"""
## Priority 5: Content to Publish ({len(content)} batches ready)

"""
    if content:
        for c in content:
            report += f"- [ ] {c}\n"
    else:
        report += "No content batches found.\n"

    report += f"""
## Priority 6: Revenue Status

- Tracking active: {'YES' if revenue['tracked'] else 'NO'}
- Revenue entries: {revenue['entries']}
- Current MRR: $0 (pre-launch)

---

## Quick Commands

```bash
# Check overnight log
tail -50 AUTOMATIONS/logs/overnight_$(date +%Y-%m-%d).log

# Run quant terminal
python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary

# Screen alpha
python3 AUTOMATIONS/alpha_screening.py --pending

# Run lead scraper
python3 AUTOMATIONS/savvy_lead_scraper.py --city "Austin" --category "dentist"

# Deploy apps (after vercel login)
for app in ralph/loops/app_factory/output/*/; do cd "$app" && vercel deploy --prod && cd -; done
```

## Next Session Priorities

1. Deploy Ramadan Tracker (Ramadan starts Feb 28 - 18 DAYS LEFT)
2. Create social media accounts (40 pending)
3. Upload 130 tweets to Buffer
4. List products on Gumroad
5. Start cold email outreach with new leads
"""

    output_path = OPS / f"DAILY_TODO_{TODAY.replace('-', '_')}.md"
    with open(output_path, 'w') as f:
        f.write(report)

    print(f"Daily TODO generated: {output_path}")
    print(f"  Blockers: {len(blockers)}")
    print(f"  Alpha pending: {alpha['pending']}")
    print(f"  New leads: {sum(l['rows'] for l in leads)}")
    print(f"  Apps ready: {sum(1 for a in apps if a['pwa_ready'])}/{len(apps)}")
    print(f"  Content batches: {len(content)}")

    return str(output_path)

if __name__ == "__main__":
    generate_report()
