# Daily Briefing Template — Automated Morning Report

**Generated:** {DATE} {TIME}
**Report type:** Morning briefing (6:00-7:00 AM delivery)
**Generation command:** `python3 AUTOMATIONS/daily_briefing.py --generate`

---

## HOW TO USE THIS TEMPLATE

This file is the FORMAT for the auto-generated daily brief.
To make it live: build `AUTOMATIONS/daily_briefing.py` that pulls live data and fills each `{VARIABLE}` block.

Variables to pull:
- `{DATE}` → datetime.now()
- Revenue stats → LEDGER/FINANCIALS/ CSVs
- Alpha queue → LEDGER/ALPHA_STAGING.csv count of PENDING_REVIEW
- Content status → CONTENT/social/ file count
- Cron status → `crontab -l | grep -v '^#' | wc -l`
- System health → LEDGER/SYSTEM_HEALTH.json

---

# PRINTMAXX DAILY BRIEF — {DAY_OF_WEEK} {DATE}

---

## 1. REVENUE SNAPSHOT

| Metric | Today | Yesterday | 7-Day Avg | 30-Day Total |
|--------|-------|-----------|-----------|--------------|
| Total Revenue | ${TODAY_REVENUE} | ${YESTERDAY_REVENUE} | ${7D_AVG} | ${30D_TOTAL} |
| Gumroad | ${GUMROAD_TODAY} | — | ${GUMROAD_7D} | ${GUMROAD_30D} |
| Affiliate | ${AFFILIATE_TODAY} | — | ${AFFILIATE_7D} | ${AFFILIATE_30D} |
| Apps/PWA | ${APP_TODAY} | — | ${APP_7D} | ${APP_30D} |
| Services | ${SERVICES_TODAY} | — | ${SERVICES_7D} | ${SERVICES_30D} |

**MRR Tracker:** ${CURRENT_MRR} / $8,000 target ({MRR_PERCENT}% of 90-day goal)

---

## 2. ALPHA QUEUE

**Pending review:** {ALPHA_PENDING_COUNT} entries
**Auto-approved overnight:** {ALPHA_AUTO_APPROVED}
**High-priority (score >0.8):** {ALPHA_HIGH_PRIORITY}

Top 3 pending entries to review:
1. [{ALPHA1_ID}] {ALPHA1_SUMMARY} — Source: {ALPHA1_SOURCE} — Score: {ALPHA1_SCORE}
2. [{ALPHA2_ID}] {ALPHA2_SUMMARY} — Source: {ALPHA2_SOURCE} — Score: {ALPHA2_SCORE}
3. [{ALPHA3_ID}] {ALPHA3_SUMMARY} — Source: {ALPHA3_SOURCE} — Score: {ALPHA3_SCORE}

**Action:** Run `/review-alpha` or `python3 AUTOMATIONS/alpha_auto_processor.py --process-new`

---

## 3. CONTENT STATUS

| Platform | Scheduled | Posted Today | In Queue |
|----------|-----------|--------------|----------|
| X/Twitter | {X_SCHEDULED} | {X_POSTED} | {X_QUEUE} |
| Instagram | {IG_SCHEDULED} | {IG_POSTED} | {IG_QUEUE} |
| TikTok | {TT_SCHEDULED} | {TT_POSTED} | {TT_QUEUE} |
| YouTube | {YT_SCHEDULED} | {YT_POSTED} | {YT_QUEUE} |
| Newsletter | — | {NL_SENT} | {NL_QUEUE} |

**Content in PENDING_REVIEW:** {CONTENT_PENDING} files in CONTENT/social/

---

## 4. SYSTEM STATUS

| System | Status | Last Run | Next Run |
|--------|--------|----------|----------|
| Twitter scraper | {TWITTER_STATUS} | {TWITTER_LAST} | {TWITTER_NEXT} |
| Reddit scraper | {REDDIT_STATUS} | {REDDIT_LAST} | {REDDIT_NEXT} |
| Alpha processor | {ALPHA_STATUS} | {ALPHA_LAST} | {ALPHA_NEXT} |
| Daily research | {RESEARCH_STATUS} | {RESEARCH_LAST} | {RESEARCH_NEXT} |
| Guardian backup | {BACKUP_STATUS} | {BACKUP_LAST} | {BACKUP_NEXT} |
| Cron jobs active | {CRON_COUNT} | — | — |

**System health:** {SYSTEM_HEALTH_SCORE}/100
**Disk usage:** {DISK_USAGE}GB / {DISK_TOTAL}GB ({DISK_PERCENT}%)

---

## 5. ACTIVE VENTURES STATUS

| Venture | Stage | Last Action | Revenue | Priority |
|---------|-------|-------------|---------|----------|
| MCP Marketplace | {MCP_STAGE} | {MCP_LAST} | ${MCP_REV} | {MCP_PRIORITY} |
| PrayerLock PWA | {PL_STAGE} | {PL_LAST} | ${PL_REV} | {PL_PRIORITY} |
| Cold Outbound | {CO_STAGE} | {CO_LAST} | ${CO_REV} | {CO_PRIORITY} |
| App Factory | {AF_STAGE} | {AF_LAST} | ${AF_REV} | {AF_PRIORITY} |
| Newsletter | {NL_STAGE} | {NL_LAST} | ${NL_REV} | {NL_PRIORITY} |

---

## 6. TASKS FOR TODAY

**Auto-generated from PERSISTENT_TASK_TRACKER.md — high priority items:**

1. {TASK1}
2. {TASK2}
3. {TASK3}
4. {TASK4}
5. {TASK5}

**Blockers identified:**
- {BLOCKER1} (priority: {BLOCKER1_PRIORITY})
- {BLOCKER2} (priority: {BLOCKER2_PRIORITY})

---

## 7. OVERNIGHT ACTIVITY SUMMARY

**Ralph loops run:** {RALPH_LOOPS_COUNT}
**Files created overnight:** {FILES_CREATED}
**Commits made:** {GIT_COMMITS}
**Cron executions:** {CRON_EXECUTIONS}

**Notable completions:**
{OVERNIGHT_COMPLETIONS}

---

## 8. MARKET INTELLIGENCE

**Trending topics in your niches (last 24h):**
- Solopreneur: {SOLOPRENEUR_TREND}
- Faith/Ramadan: {FAITH_TREND}
- AI tools: {AI_TREND}

**Competitor moves:**
{COMPETITOR_INTEL}

---

## 9. KEY METRICS TRACKER (30-day view)

```
Revenue per day (last 30 days):
Day  1: ${D1}  ████
Day  2: ${D2}  ████████
...
Day 30: ${D30} ████████████████

Trend: {REVENUE_TREND}
Projected month-end: ${PROJECTED_MONTH_END}
```

---

## 10. TODAY'S FOCUS

Based on venture scoring and revenue trajectory:

**Top priority:** {TOP_PRIORITY_ACTION}
**Expected outcome:** {EXPECTED_OUTCOME}
**Time required:** {TIME_REQUIRED}

**Do NOT spend time on:**
- {AVOID1}
- {AVOID2}

---

## QUICK COMMANDS

```bash
# Review alpha
python3 AUTOMATIONS/alpha_auto_processor.py --process-new

# Check system health
python3 AUTOMATIONS/system_health_monitor.py --quick

# Run all scrapers
python3 AUTOMATIONS/twitter_alpha_scraper.py --all &
python3 AUTOMATIONS/background_reddit_scraper.py --scrape &

# Check venture status
python3 AUTOMATIONS/venture_performance_tracker.py --recommend

# Generate content
/generate-posts
```

---

*Generated by AUTOMATIONS/daily_briefing.py at {GENERATION_TIME}*
*Next briefing: Tomorrow at 6:00 AM*
*To disable: `crontab -e` and remove briefing entry*

---

## BRIEFING GENERATOR SCRIPT STUB

```python
# AUTOMATIONS/daily_briefing.py
# python3 AUTOMATIONS/daily_briefing.py --generate

import json
import csv
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def get_alpha_queue_stats():
    staging_file = BASE_DIR / 'LEDGER' / 'ALPHA_STAGING.csv'
    pending = 0
    auto_approved = 0
    with open(staging_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('status') == 'PENDING_REVIEW':
                pending += 1
            elif row.get('status') == 'AUTO_APPROVED':
                if row.get('date_processed', '')[:10] == datetime.now().strftime('%Y-%m-%d'):
                    auto_approved += 1
    return pending, auto_approved

def get_system_health():
    health_file = BASE_DIR / 'LEDGER' / 'SYSTEM_HEALTH.json'
    with open(health_file) as f:
        return json.load(f)

def generate_briefing():
    template_file = BASE_DIR / 'ralph' / 'loops' / 'spreadsheet_buildout' / 'output' / 'G01_G15_growth' / 'daily_briefing_template.md'
    output_file = BASE_DIR / 'OPS' / 'DAILY_BRIEFING.md'

    pending, auto_approved = get_alpha_queue_stats()
    health = get_system_health()

    # Load template and fill variables
    with open(template_file) as f:
        template = f.read()

    now = datetime.now()
    filled = template.replace('{DATE}', now.strftime('%Y-%m-%d'))
    filled = filled.replace('{TIME}', now.strftime('%H:%M'))
    filled = filled.replace('{DAY_OF_WEEK}', now.strftime('%A').upper())
    filled = filled.replace('{ALPHA_PENDING_COUNT}', str(pending))
    filled = filled.replace('{ALPHA_AUTO_APPROVED}', str(auto_approved))
    # ... add remaining replacements

    with open(output_file, 'w') as f:
        f.write(filled)

    print(f"Briefing generated: {output_file}")

if __name__ == '__main__':
    generate_briefing()
```

**Cron entry:** `0 6 * * * python3 /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/daily_briefing.py --generate`
