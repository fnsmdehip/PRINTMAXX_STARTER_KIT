#!/usr/bin/env python3
"""
PRINTMAXX DAILY MORNING BRIEFING GENERATOR
===========================================
Scans ALL ledgers, logs, ops, automations, and financials.
Generates a prioritized "HUMAN ACTION REQUIRED" report.
Run via cron at 5:00 AM daily or on-demand.

Usage:
    python3 scripts/daily_briefing.py              # Full briefing
    python3 scripts/daily_briefing.py --quick       # Quick summary only
    python3 scripts/daily_briefing.py --json        # JSON output for TUI
"""

import os, sys, csv, json, glob
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / 'LEDGER'
OPS = BASE / 'OPS'
LOGS = BASE / 'logs'
FINANCIALS = BASE / 'FINANCIALS'
AUTOMATIONS = BASE / 'AUTOMATIONS'
MEGA = LEDGER / 'MEGA_SHEET'
OUTPUT_DIR = LEDGER / 'DAILY_BRIEFINGS'

NOW = datetime.now()
TODAY = NOW.strftime('%Y-%m-%d')
YESTERDAY = (NOW - timedelta(days=1)).strftime('%Y-%m-%d')

def read_csv_safe(path, max_rows=None):
    rows = []
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                rows.append(row)
                if max_rows and i >= max_rows:
                    break
    except Exception:
        pass
    return rows

def file_modified_today(path):
    try:
        mtime = datetime.fromtimestamp(os.path.getmtime(path))
        return mtime.date() == NOW.date()
    except Exception:
        return False

def file_modified_recently(path, hours=24):
    try:
        mtime = datetime.fromtimestamp(os.path.getmtime(path))
        return (NOW - mtime).total_seconds() < hours * 3600
    except Exception:
        return False

# ============================================================
# 1. AUTOMATION STATUS
# ============================================================
def check_automations():
    results = {'status': 'UNKNOWN', 'details': [], 'actions': []}

    # Check AUTOMATION_RESULTS.csv
    auto_results = read_csv_safe(LEDGER / 'AUTOMATION_RESULTS.csv')
    if auto_results:
        latest = auto_results[-1]
        results['latest_run'] = latest.get('timestamp', 'unknown')
        results['alpha_extracted'] = latest.get('alpha_extracted', '0')
        results['content_generated'] = latest.get('content_generated', '0')

        # Check if ran today
        ts = latest.get('timestamp', '')
        if TODAY in ts:
            results['status'] = 'GREEN'
            results['details'].append(f"Last run: {ts}")
            results['details'].append(f"Alpha extracted: {latest.get('alpha_extracted', '0')}")
            results['details'].append(f"Content generated: {latest.get('content_generated', '0')}")
        elif YESTERDAY in ts:
            results['status'] = 'YELLOW'
            results['details'].append(f"Last run was YESTERDAY: {ts}")
            results['actions'].append("MANUAL: Check why morning cron didn't fire. Run: ./printmaxx_cron.sh morning_sync")
        else:
            results['status'] = 'RED'
            results['details'].append(f"Last run: {ts} (STALE)")
            results['actions'].append("CRITICAL: Automations haven't run recently. Check launchd: launchctl list | grep printmaxx")
    else:
        results['status'] = 'RED'
        results['details'].append("No AUTOMATION_RESULTS.csv found")
        results['actions'].append("CRITICAL: Run ./printmaxx_cron.sh to initialize automation tracking")

    # Check log files
    recent_logs = []
    if LOGS.exists():
        for log in sorted(LOGS.glob('*.log'), key=os.path.getmtime, reverse=True)[:5]:
            if file_modified_recently(log, 24):
                size = os.path.getsize(log)
                recent_logs.append(f"{log.name} ({size} bytes)")
                # Check for errors in log
                try:
                    with open(log, 'r', errors='replace') as f:
                        content = f.read()
                        error_count = content.lower().count('error')
                        if error_count > 5:
                            results['actions'].append(f"WARNING: {log.name} has {error_count} errors. Review: tail -50 logs/{log.name}")
                except Exception:
                    pass
    results['recent_logs'] = recent_logs

    return results

# ============================================================
# 2. ALPHA DIGEST
# ============================================================
def check_alpha():
    results = {'pending': 0, 'approved': 0, 'total': 0, 'top_items': [], 'actions': []}

    # Check ALPHA_STAGING.csv
    alpha = read_csv_safe(LEDGER / 'ALPHA_STAGING.csv')
    if not alpha:
        # Try MEGA_SHEET TAB3
        alpha = read_csv_safe(MEGA / 'TAB3_ALPHA_MASTER.csv')

    if alpha:
        results['total'] = len(alpha)
        pending = [a for a in alpha if a.get('status', '').upper() == 'PENDING_REVIEW']
        approved = [a for a in alpha if a.get('status', '').upper() == 'APPROVED']
        results['pending'] = len(pending)
        results['approved'] = len(approved)

        # Top 5 highest ROI pending
        highest = [a for a in pending if a.get('roi_potential', '').upper() in ('HIGHEST', 'HIGH')][:5]
        for h in highest:
            results['top_items'].append({
                'id': h.get('alpha_id', '?'),
                'title': h.get('title', h.get('tactic', '?'))[:80],
                'category': h.get('category', '?'),
                'roi': h.get('roi_potential', '?'),
                'source': h.get('source', '?')
            })

        if len(pending) > 50:
            results['actions'].append(f"REVIEW: {len(pending)} alpha entries pending review. Run: /review-alpha")
        if len(pending) > 200:
            results['actions'].append(f"CRITICAL: Alpha backlog at {len(pending)}. Batch review needed urgently.")

    return results

# ============================================================
# 3. CONTENT QUEUE
# ============================================================
def check_content():
    results = {'today_posts': 0, 'queued': 0, 'gaps': [], 'actions': []}

    calendar = read_csv_safe(LEDGER / 'CONTENT_CALENDAR_30DAY.csv')
    if calendar:
        today_posts = [c for c in calendar if c.get('ScheduledDate', c.get('date', '')) == TODAY]
        queued = [c for c in calendar if c.get('Status', c.get('status', '')).upper() == 'QUEUED']
        results['today_posts'] = len(today_posts)
        results['queued'] = len(queued)

        if not today_posts:
            results['gaps'].append("No content scheduled for today!")
            results['actions'].append("MANUAL: Schedule content for today or run content generation cron")
        else:
            platforms = set(c.get('Platform', c.get('platform', '?')) for c in today_posts)
            results['platforms_today'] = list(platforms)

            # Check for manual posting needed
            manual = [c for c in today_posts if c.get('status', '').upper() != 'POSTED']
            if manual:
                results['actions'].append(f"POST: {len(manual)} pieces need manual posting today across {', '.join(platforms)}")

    return results

# ============================================================
# 4. ACCOUNT HEALTH
# ============================================================
def check_accounts():
    results = {'total': 0, 'active': 0, 'warnings': [], 'actions': []}

    health = read_csv_safe(LEDGER / 'ACCOUNT_HEALTH_DAILY.csv')
    portfolio = read_csv_safe(LEDGER / 'ACCOUNT_PORTFOLIO_MASTER.csv')

    if portfolio:
        results['total'] = len(portfolio)
        created = [a for a in portfolio if a.get('status', '').upper() != 'NOT_CREATED']
        results['active'] = len(created)
        not_created = len(portfolio) - len(created)
        if not_created > 0:
            results['actions'].append(f"SETUP: {not_created} accounts still need creation. Check ACCOUNT_PORTFOLIO_MASTER.csv")

    if health:
        for h in health:
            status = h.get('status', '').upper()
            if 'SHADOWBAN' in status or 'FLAG' in status or 'WARN' in status:
                results['warnings'].append(f"{h.get('account', '?')}: {status}")
                results['actions'].append(f"URGENT: {h.get('account', '?')} flagged as {status}. Reduce activity immediately.")

    return results

# ============================================================
# 5. FINANCIAL CHECK
# ============================================================
def check_financials():
    results = {'revenue_today': 0, 'expenses_today': 0, 'actions': []}

    rev = read_csv_safe(FINANCIALS / 'REVENUE_TRACKER.csv')
    exp = read_csv_safe(FINANCIALS / 'EXPENSE_TRACKER.csv')

    if rev:
        today_rev = [r for r in rev if r.get('date', '') == TODAY]
        results['total_revenue_entries'] = len(rev)
        results['revenue_today'] = len(today_rev)

    if exp:
        today_exp = [e for e in exp if e.get('date', '') == TODAY]
        results['total_expense_entries'] = len(exp)
        results['expenses_today'] = len(today_exp)

        # Check for upcoming renewals
        for e in exp:
            if e.get('recurring', '').upper() == 'YES':
                next_date = e.get('next_due', '')
                if next_date and next_date <= (NOW + timedelta(days=3)).strftime('%Y-%m-%d'):
                    results['actions'].append(f"RENEWAL: {e.get('description', '?')} due {next_date} (${e.get('amount', '?')})")

    # Check P&L
    pnl = read_csv_safe(FINANCIALS / 'P_AND_L_MONTHLY.csv')
    if pnl:
        latest = pnl[-1]
        results['latest_month'] = latest.get('month', '?')
        results['net_income'] = latest.get('net_income', latest.get('profit', '?'))

    return results

# ============================================================
# 6. OPS STATUS
# ============================================================
def check_ops():
    results = {'active_ops': 0, 'recent_changes': [], 'actions': []}

    # Count ops with recent activity
    if OPS.exists():
        recent_ops = []
        for f in OPS.iterdir():
            if f.is_file() and file_modified_recently(f, 48):
                recent_ops.append(f.name)
        results['active_ops'] = len(recent_ops)
        results['recent_changes'] = recent_ops[:10]

    # Check for blocked items
    blocked = list(OPS.glob('**/BLOCKED_*.md')) if OPS.exists() else []
    if blocked:
        for b in blocked:
            results['actions'].append(f"BLOCKED: {b.name} needs resolution")

    # Check checkpoints
    checkpoints_dir = BASE / 'ralph' / 'loops' / 'mega' / 'checkpoints'
    if checkpoints_dir.exists():
        for cp_dir in checkpoints_dir.iterdir():
            if cp_dir.is_dir():
                pending = list(cp_dir.glob('*.md'))
                if pending:
                    results['actions'].append(f"CHECKPOINT: {len(pending)} items in {cp_dir.name} need human review")

    return results

# ============================================================
# 7. TOOL STATUS
# ============================================================
def check_tools():
    results = {'total': 0, 'free_tier': 0, 'approaching_limits': [], 'actions': []}

    tools = read_csv_safe(LEDGER / 'TOOLS_SERVICES_MASTER.csv')
    if tools:
        results['total'] = len(tools)
        free = [t for t in tools if t.get('budget_tier', t.get('tier', '')).upper() in ('FREE', '$0', 'TIER_0')]
        results['free_tier'] = len(free)

    return results

# ============================================================
# 8. FREELANCE PIPELINE (NEW)
# ============================================================
def check_freelance():
    results = {'active_gigs': 0, 'pending_delivery': 0, 'actions': []}

    freelance_csv = LEDGER / 'FREELANCE_PIPELINE.csv'
    if freelance_csv.exists():
        orders = read_csv_safe(freelance_csv)
        active = [o for o in orders if o.get('status', '').upper() in ('ACTIVE', 'IN_PROGRESS')]
        pending = [o for o in orders if o.get('status', '').upper() == 'PENDING_DELIVERY']
        results['active_gigs'] = len(active)
        results['pending_delivery'] = len(pending)

        for o in pending:
            deadline = o.get('deadline', '')
            if deadline and deadline <= TODAY:
                results['actions'].append(f"OVERDUE: {o.get('service', '?')} for {o.get('client', '?')} was due {deadline}")
            elif deadline and deadline <= (NOW + timedelta(days=1)).strftime('%Y-%m-%d'):
                results['actions'].append(f"DUE TOMORROW: {o.get('service', '?')} for {o.get('client', '?')}")
    else:
        results['actions'].append("SETUP: Create LEDGER/FREELANCE_PIPELINE.csv for freelance gig tracking")

    return results

# ============================================================
# 9. FILE SYSTEM HEALTH
# ============================================================
def check_filesystem():
    results = {'new_files_24h': 0, 'large_files': [], 'actions': []}

    new_count = 0
    large = []
    for root, dirs, files in os.walk(BASE):
        # Skip hidden dirs, node_modules, etc
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != '__pycache__']
        for f in files:
            fp = os.path.join(root, f)
            try:
                if file_modified_recently(fp, 24):
                    new_count += 1
                size = os.path.getsize(fp)
                if size > 10_000_000:  # 10MB
                    large.append(f"{f} ({size // 1_000_000}MB)")
            except Exception:
                pass

    results['new_files_24h'] = new_count
    results['large_files'] = large[:5]

    return results

# ============================================================
# 10. EXPERIMENTS
# ============================================================
def check_experiments():
    results = {'active': 0, 'concluded': 0, 'actions': []}

    exp = read_csv_safe(MEGA / 'TAB9_EXPERIMENTS_METRICS.csv')
    if exp:
        active = [e for e in exp if e.get('status', '').upper() == 'ACTIVE']
        concluded = [e for e in exp if e.get('status', '').upper() == 'CONCLUDED']
        results['active'] = len(active)
        results['concluded'] = len(concluded)

        for e in concluded:
            if e.get('winner', ''):
                results['actions'].append(f"IMPLEMENT: Experiment '{e.get('name', '?')}' concluded. Winner: {e.get('winner', '?')}")

    return results

# ============================================================
# GENERATE BRIEFING
# ============================================================
def generate_briefing(quick=False, json_output=False):
    briefing = {
        'generated': NOW.strftime('%Y-%m-%d %H:%M:%S'),
        'sections': {}
    }

    # Run all checks
    briefing['sections']['automations'] = check_automations()
    briefing['sections']['alpha'] = check_alpha()
    briefing['sections']['content'] = check_content()
    briefing['sections']['accounts'] = check_accounts()
    briefing['sections']['financials'] = check_financials()
    briefing['sections']['ops'] = check_ops()
    briefing['sections']['tools'] = check_tools()
    briefing['sections']['freelance'] = check_freelance()
    briefing['sections']['filesystem'] = check_filesystem()
    briefing['sections']['experiments'] = check_experiments()

    # Collect ALL actions
    all_actions = []
    for section_name, section_data in briefing['sections'].items():
        for action in section_data.get('actions', []):
            priority = 'HIGH' if any(w in action for w in ['CRITICAL', 'OVERDUE', 'URGENT']) else \
                       'MEDIUM' if any(w in action for w in ['MANUAL', 'REVIEW', 'POST', 'SETUP']) else 'LOW'
            all_actions.append({
                'section': section_name.upper(),
                'action': action,
                'priority': priority
            })

    # Sort: CRITICAL first, then MANUAL, then others
    all_actions.sort(key=lambda x: {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[x['priority']])
    briefing['all_actions'] = all_actions

    if json_output:
        print(json.dumps(briefing, indent=2))
        return briefing

    # Generate markdown report
    lines = []
    lines.append(f"# PRINTMAXX DAILY BRIEFING — {NOW.strftime('%A, %B %d, %Y')}")
    lines.append(f"_Generated: {NOW.strftime('%H:%M:%S')}_\n")

    # === PRIORITY ACTIONS ===
    lines.append("## TODAY'S MANUAL ACTIONS REQUIRED\n")
    if all_actions:
        high = [a for a in all_actions if a['priority'] == 'HIGH']
        med = [a for a in all_actions if a['priority'] == 'MEDIUM']
        low = [a for a in all_actions if a['priority'] == 'LOW']

        if high:
            lines.append("### CRITICAL (Do First)\n")
            for a in high:
                lines.append(f"- [{a['section']}] {a['action']}")
            lines.append("")

        if med:
            lines.append("### IMPORTANT (Do Today)\n")
            for a in med:
                lines.append(f"- [{a['section']}] {a['action']}")
            lines.append("")

        if low:
            lines.append("### LOW PRIORITY (When Available)\n")
            for a in low:
                lines.append(f"- [{a['section']}] {a['action']}")
            lines.append("")
    else:
        lines.append("No manual actions required. All systems nominal.\n")

    lines.append(f"**Total action items: {len(all_actions)}** ({len([a for a in all_actions if a['priority']=='HIGH'])} critical, {len([a for a in all_actions if a['priority']=='MEDIUM'])} important, {len([a for a in all_actions if a['priority']=='LOW'])} low)\n")

    if quick:
        report = '\n'.join(lines)
        print(report)
        return briefing

    # === FULL SECTIONS ===
    lines.append("---\n")

    # Automations
    auto = briefing['sections']['automations']
    status_emoji = {'GREEN': 'GREEN', 'YELLOW': 'YELLOW', 'RED': 'RED'}.get(auto['status'], 'UNKNOWN')
    lines.append(f"## 1. AUTOMATION STATUS: {status_emoji}\n")
    for d in auto.get('details', []):
        lines.append(f"- {d}")
    if auto.get('recent_logs'):
        lines.append(f"\nRecent logs: {', '.join(auto['recent_logs'][:3])}")
    lines.append("")

    # Alpha
    alpha = briefing['sections']['alpha']
    lines.append(f"## 2. ALPHA DIGEST\n")
    lines.append(f"- Total entries: {alpha['total']}")
    lines.append(f"- Pending review: {alpha['pending']}")
    lines.append(f"- Approved: {alpha['approved']}")
    if alpha['top_items']:
        lines.append("\n**Top pending alpha:**")
        for item in alpha['top_items']:
            lines.append(f"- {item['id']}: {item['title']} [{item['category']}] ROI: {item['roi']}")
    lines.append("")

    # Content
    content = briefing['sections']['content']
    lines.append(f"## 3. CONTENT QUEUE\n")
    lines.append(f"- Posts scheduled today: {content['today_posts']}")
    lines.append(f"- Total queued: {content['queued']}")
    if content.get('platforms_today'):
        lines.append(f"- Platforms: {', '.join(content['platforms_today'])}")
    if content['gaps']:
        for g in content['gaps']:
            lines.append(f"- GAP: {g}")
    lines.append("")

    # Accounts
    accts = briefing['sections']['accounts']
    lines.append(f"## 4. ACCOUNT HEALTH\n")
    lines.append(f"- Total accounts: {accts['total']}")
    lines.append(f"- Active: {accts['active']}")
    if accts['warnings']:
        for w in accts['warnings']:
            lines.append(f"- WARNING: {w}")
    lines.append("")

    # Financials
    fin = briefing['sections']['financials']
    lines.append(f"## 5. FINANCIALS\n")
    lines.append(f"- Revenue entries today: {fin['revenue_today']}")
    lines.append(f"- Expense entries today: {fin['expenses_today']}")
    if fin.get('latest_month'):
        lines.append(f"- Latest P&L month: {fin['latest_month']}")
    if fin.get('net_income'):
        lines.append(f"- Net income: {fin['net_income']}")
    lines.append("")

    # Ops
    ops = briefing['sections']['ops']
    lines.append(f"## 6. OPS STATUS\n")
    lines.append(f"- Active ops (48hr): {ops['active_ops']}")
    if ops['recent_changes']:
        lines.append(f"- Recent: {', '.join(ops['recent_changes'][:5])}")
    lines.append("")

    # Tools
    tools = briefing['sections']['tools']
    lines.append(f"## 7. TOOL STATUS\n")
    lines.append(f"- Total tools: {tools['total']}")
    lines.append(f"- Free tier: {tools['free_tier']}")
    lines.append("")

    # Freelance
    fl = briefing['sections']['freelance']
    lines.append(f"## 8. FREELANCE PIPELINE\n")
    lines.append(f"- Active gigs: {fl['active_gigs']}")
    lines.append(f"- Pending delivery: {fl['pending_delivery']}")
    lines.append("")

    # Filesystem
    fs = briefing['sections']['filesystem']
    lines.append(f"## 9. FILE SYSTEM\n")
    lines.append(f"- Files modified (24hr): {fs['new_files_24h']}")
    if fs['large_files']:
        lines.append(f"- Large files (>10MB): {', '.join(fs['large_files'])}")
    lines.append("")

    # Experiments
    exp = briefing['sections']['experiments']
    lines.append(f"## 10. EXPERIMENTS\n")
    lines.append(f"- Active: {exp['active']}")
    lines.append(f"- Concluded: {exp['concluded']}")
    lines.append("")

    lines.append("---")
    lines.append(f"_PRINTMAXX Daily Briefing v1.0 | {NOW.strftime('%Y-%m-%d %H:%M:%S')}_")

    report = '\n'.join(lines)

    # Save to file
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f'DAILY_BRIEFING_{TODAY}.md'
    with open(output_file, 'w') as f:
        f.write(report)

    print(report)
    print(f"\nSaved to: {output_file}")

    return briefing

if __name__ == '__main__':
    quick = '--quick' in sys.argv
    json_out = '--json' in sys.argv
    generate_briefing(quick=quick, json_output=json_out)
