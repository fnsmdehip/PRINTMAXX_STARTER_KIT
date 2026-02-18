#!/usr/bin/env python3
"""
PRINTMAXX RBI (RESEARCH-BASED IMPROVEMENT) SYSTEM
===================================================
Perpetual improvement engine. Runs daily/weekly/monthly.
Audits all ops, scores performance, identifies improvements,
suggests new ops, and self-improves.

Usage:
    python3 scripts/rbi_audit.py daily     # Daily ops audit
    python3 scripts/rbi_audit.py weekly    # Weekly deep analysis
    python3 scripts/rbi_audit.py monthly   # Monthly strategic review
    python3 scripts/rbi_audit.py full      # Run everything
"""

import os, sys, csv, json, glob
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter

BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / 'LEDGER'
OPS = BASE / 'OPS'
MEGA = LEDGER / 'MEGA_SHEET'
FINANCIALS = BASE / 'FINANCIALS'
OUTPUT_DIR = LEDGER / 'RBI_AUDITS'

NOW = datetime.now()
TODAY = NOW.strftime('%Y-%m-%d')

def read_csv_safe(path, max_rows=None):
    rows = []
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            for i, row in enumerate(csv.DictReader(f)):
                rows.append(row)
                if max_rows and i >= max_rows:
                    break
    except Exception:
        pass
    return rows

def count_files_modified(directory, hours=24):
    count = 0
    cutoff = NOW - timedelta(hours=hours)
    try:
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
            for f in files:
                fp = os.path.join(root, f)
                try:
                    if datetime.fromtimestamp(os.path.getmtime(fp)) > cutoff:
                        count += 1
                except:
                    pass
    except:
        pass
    return count

# ============================================================
# DAILY AUDIT
# ============================================================
def daily_audit():
    report = []
    report.append(f"# RBI DAILY AUDIT — {NOW.strftime('%A, %B %d, %Y %H:%M')}\n")

    # 1. Alpha pipeline health
    report.append("## 1. ALPHA PIPELINE HEALTH\n")
    alpha = read_csv_safe(LEDGER / 'ALPHA_STAGING.csv')
    if alpha:
        status_counts = Counter(a.get('status', 'UNKNOWN').upper() for a in alpha)
        report.append(f"Total alpha entries: {len(alpha)}")
        for status, count in status_counts.most_common():
            report.append(f"  {status}: {count}")

        # ROI distribution
        roi_counts = Counter(a.get('roi_potential', 'UNKNOWN').upper() for a in alpha)
        report.append(f"\nROI distribution:")
        for roi, count in roi_counts.most_common():
            report.append(f"  {roi}: {count}")

        # Category distribution
        cat_counts = Counter(a.get('category', 'UNKNOWN') for a in alpha)
        report.append(f"\nTop categories:")
        for cat, count in cat_counts.most_common(10):
            report.append(f"  {cat}: {count}")

        # Actionable items
        high_pending = [a for a in alpha if a.get('roi_potential', '').upper() in ('HIGHEST', 'HIGH') and a.get('status', '').upper() == 'PENDING_REVIEW']
        if high_pending:
            report.append(f"\nHIGH/HIGHEST ROI pending review: {len(high_pending)}")
            report.append("ACTION: Review these first. Run: /review-alpha")
    report.append("")

    # 2. Method performance (from MEGA_SHEET)
    report.append("## 2. MONEY METHOD STATUS\n")
    methods = read_csv_safe(MEGA / 'TAB1_MONEY_METHODS_MASTER.csv')
    if methods:
        status_counts = Counter(m.get('status', 'UNKNOWN') for m in methods)
        report.append(f"Total methods: {len(methods)}")
        for s, c in status_counts.most_common():
            report.append(f"  {s}: {c}")

        active = [m for m in methods if m.get('status', '').lower() in ('active', 'Active')]
        report.append(f"\nActive methods: {len(active)}")
        for m in active:
            report.append(f"  {m.get('method_id', '?')}: {m.get('method_name', '?')} (${m.get('monthly_potential_low', '?')}-{m.get('monthly_potential_high', '?')}/mo)")
    report.append("")

    # 3. Content pipeline
    report.append("## 3. CONTENT PIPELINE\n")
    content = read_csv_safe(MEGA / 'TAB5_CONTENT_MASTER.csv')
    if content:
        status_counts = Counter(c.get('Status', c.get('status', 'UNKNOWN')).upper() for c in content)
        report.append(f"Total content pieces: {len(content)}")
        for s, c in status_counts.most_common():
            report.append(f"  {s}: {c}")

        platform_counts = Counter(c.get('Platform', c.get('platform', 'UNKNOWN')) for c in content)
        report.append(f"\nContent by platform:")
        for p, c in platform_counts.most_common():
            if p:
                report.append(f"  {p}: {c}")
    report.append("")

    # 4. Filesystem activity
    report.append("## 4. SYSTEM ACTIVITY (24H)\n")
    areas = {
        'AUTOMATIONS': BASE / 'AUTOMATIONS',
        'OPS': BASE / 'OPS',
        'LEDGER': BASE / 'LEDGER',
        'CONTENT': BASE / 'CONTENT',
        'MONEY_METHODS': BASE / 'MONEY_METHODS',
        'scripts': BASE / 'scripts',
    }
    for name, path in areas.items():
        count = count_files_modified(path, 24)
        report.append(f"  {name}: {count} files modified")
    report.append("")

    # 5. Tool utilization
    report.append("## 5. TOOL UTILIZATION\n")
    tools = read_csv_safe(LEDGER / 'TOOLS_SERVICES_MASTER.csv')
    if tools:
        tier_counts = Counter(t.get('budget_tier', t.get('tier', 'UNKNOWN')) for t in tools)
        active_tools = [t for t in tools if t.get('status', '').upper() == 'ACTIVE']
        report.append(f"Total tools: {len(tools)}")
        report.append(f"Active tools: {len(active_tools)}")
        for tier, count in tier_counts.most_common():
            report.append(f"  {tier}: {count}")
    report.append("")

    # 6. Recommendations
    report.append("## 6. RBI RECOMMENDATIONS\n")
    recommendations = []

    if alpha:
        pending = len([a for a in alpha if a.get('status', '').upper() == 'PENDING_REVIEW'])
        if pending > 100:
            recommendations.append(f"CRITICAL: {pending} alpha entries pending. Batch review needed. Use automated screening.")
        elif pending > 50:
            recommendations.append(f"IMPORTANT: {pending} alpha pending review. Schedule 30-min review session.")

    if methods:
        planning = [m for m in methods if m.get('status', '').lower() == 'planning']
        if len(planning) > 20:
            recommendations.append(f"OPPORTUNITY: {len(planning)} methods in 'Planning' status. Convert top 3 to 'Active' this week.")

    if content:
        queued = len([c for c in content if c.get('Status', c.get('status', '')).upper() == 'QUEUED'])
        posted = len([c for c in content if c.get('Status', c.get('status', '')).upper() == 'POSTED'])
        if queued > 100 and posted < 50:
            recommendations.append(f"EXECUTION GAP: {queued} content pieces queued but only {posted} posted. Start publishing.")

    if not recommendations:
        recommendations.append("System operating normally. Focus on execution of P1 priority ops.")

    for r in recommendations:
        report.append(f"- {r}")
    report.append("")

    return '\n'.join(report)

# ============================================================
# WEEKLY ANALYSIS
# ============================================================
def weekly_analysis():
    report = []
    report.append(f"# RBI WEEKLY DEEP ANALYSIS — Week of {TODAY}\n")

    # 1. Cross-pollination opportunities
    report.append("## 1. CROSS-POLLINATION SCAN\n")
    cross = read_csv_safe(LEDGER / 'CROSS_POLLINATION_MATRIX.csv')
    if cross:
        high_synergy = [c for c in cross if float(c.get('synergy_score', 0) or 0) > 2.0]
        report.append(f"Total stacks tracked: {len(cross)}")
        report.append(f"High synergy (>2.0x): {len(high_synergy)}")
        if high_synergy:
            report.append("Top synergy pairs:")
            for s in sorted(high_synergy, key=lambda x: float(x.get('synergy_score', 0) or 0), reverse=True)[:5]:
                report.append(f"  {s.get('method_1', '?')} × {s.get('method_2', '?')} = {s.get('synergy_score', '?')}x multiplier")
    report.append("")

    # 2. Revenue analysis
    report.append("## 2. REVENUE ANALYSIS\n")
    rev = read_csv_safe(FINANCIALS / 'REVENUE_TRACKER.csv')
    if rev:
        report.append(f"Total revenue entries: {len(rev)}")
        method_rev = defaultdict(float)
        for r in rev:
            try:
                method_rev[r.get('method', 'UNKNOWN')] += float(r.get('amount', 0) or 0)
            except:
                pass
        if method_rev:
            report.append("Revenue by method:")
            for method, amount in sorted(method_rev.items(), key=lambda x: x[1], reverse=True):
                report.append(f"  {method}: ${amount:.2f}")
    else:
        report.append("No revenue tracked yet. PRIORITY: Launch first revenue-generating op.")
    report.append("")

    # 3. Experiment scorecard
    report.append("## 3. EXPERIMENT SCORECARD\n")
    exp = read_csv_safe(MEGA / 'TAB9_EXPERIMENTS_METRICS.csv')
    if exp:
        active = [e for e in exp if e.get('status', '').upper() == 'ACTIVE']
        concluded = [e for e in exp if e.get('status', '').upper() == 'CONCLUDED']
        report.append(f"Active experiments: {len(active)}")
        report.append(f"Concluded experiments: {len(concluded)}")
        if not active:
            report.append("WARNING: No active experiments. Launch 2-3 A/B tests this week.")
    report.append("")

    # 4. Source quality ranking
    report.append("## 4. SIGNAL SOURCE QUALITY\n")
    sources = read_csv_safe(MEGA / 'TAB7_SOURCES_ACCOUNTS.csv')
    if sources:
        highest = [s for s in sources if s.get('signal_quality', '').upper() == 'HIGHEST']
        report.append(f"Total sources: {len(sources)}")
        report.append(f"HIGHEST quality: {len(highest)}")
    report.append("")

    return '\n'.join(report)

# ============================================================
# MONTHLY STRATEGIC
# ============================================================
def monthly_strategic():
    report = []
    report.append(f"# RBI MONTHLY STRATEGIC REVIEW — {NOW.strftime('%B %Y')}\n")

    report.append("## 1. PORTFOLIO REBALANCING\n")
    methods = read_csv_safe(MEGA / 'TAB1_MONEY_METHODS_MASTER.csv')
    if methods:
        # Score each method
        for m in methods:
            try:
                low = float(m.get('monthly_potential_low', '0').replace('$', '').replace('k', '000').replace(',', '') or 0)
                high = float(m.get('monthly_potential_high', '0').replace('$', '').replace('k', '000').replace(',', '') or 0)
                auto = m.get('automation_level', 'Low')
                auto_score = {'High': 3, 'Medium': 2, 'Low': 1}.get(auto, 1)
                m['_score'] = ((low + high) / 2) * auto_score
            except:
                m['_score'] = 0

        top = sorted(methods, key=lambda x: x['_score'], reverse=True)[:10]
        report.append("Top 10 methods by (revenue potential × automation level):")
        for i, m in enumerate(top, 1):
            report.append(f"  {i}. {m.get('method_name', '?')}: ${m.get('monthly_potential_low', '?')}-{m.get('monthly_potential_high', '?')}/mo, {m.get('automation_level', '?')} auto, status: {m.get('status', '?')}")

        # Identify underallocated
        high_pot_inactive = [m for m in top[:20] if m.get('status', '').lower() in ('planning', 'new')]
        if high_pot_inactive:
            report.append(f"\nUNDERALLOCATED: {len(high_pot_inactive)} high-potential methods not yet active:")
            for m in high_pot_inactive[:5]:
                report.append(f"  {m.get('method_name', '?')}: ${m.get('monthly_potential_low', '?')}-{m.get('monthly_potential_high', '?')}/mo")
    report.append("")

    report.append("## 2. NEW OP IDENTIFICATION\n")
    report.append("First principles scan for new ops:")
    report.append("- Check trending topics on social platforms for unserved niches")
    report.append("- Review recent alpha for patterns suggesting new revenue streams")
    report.append("- Audit competitor launches for replicable models")
    report.append("- Check for new free-tier tools that enable new ops")
    report.append("- Review technological shifts (new APIs, platforms, algorithms)")
    report.append("")

    return '\n'.join(report)

# ============================================================
# MAIN
# ============================================================
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'daily'

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if mode == 'daily':
        report = daily_audit()
    elif mode == 'weekly':
        report = daily_audit() + '\n---\n\n' + weekly_analysis()
    elif mode == 'monthly':
        report = daily_audit() + '\n---\n\n' + weekly_analysis() + '\n---\n\n' + monthly_strategic()
    elif mode == 'full':
        report = daily_audit() + '\n---\n\n' + weekly_analysis() + '\n---\n\n' + monthly_strategic()
    else:
        print(f"Unknown mode: {mode}. Use: daily, weekly, monthly, full")
        sys.exit(1)

    output_file = OUTPUT_DIR / f'RBI_AUDIT_{TODAY}_{mode}.md'
    with open(output_file, 'w') as f:
        f.write(report)

    print(report)
    print(f"\nSaved to: {output_file}")

if __name__ == '__main__':
    main()
