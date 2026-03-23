# PRINTMAXX Scheduled Tasks & Automation Framework

## Overview

Three layers of automated execution, from lightweight cron to intelligent AI agents running throughout the day.

---

## Layer 1: Cron (Already Running, 57+ Jobs)

Existing cron infrastructure handles time-based automation. Runs regardless of whether Claude is active.

**Install/verify:** `crontab -l | wc -l` (should show 57+ entries)
**Crontab file:** `AUTOMATIONS/crontab_printmaxx_v2.txt`

### Key daily schedule:
| Time | Script | What it does |
|------|--------|-------------|
| 3:00 AM | closed_loop_pipeline.py | Lead qualification + cold email generation |
| 4:00 AM | import_sourcing_scanner.py | US customs factory intel |
| 5:00 AM | memory_manager.py --full | Refresh all 3 memory layers |
| 5:30 AM | twitter_alpha_scraper.py | Scrape 89+ high-signal Twitter accounts |
| 5:45 AM | unified_alpha_monitor.py | 350+ sources: Reddit + GitHub + ASO + competitors |
| 6:00 AM | alpha_review_bot.py | Clear PENDING_REVIEW backlog |
| 6:30 AM | alpha_auto_processor.py | Route alpha to ventures/OPS/cron/archive |
| 6:30 AM | reddit_pain_point_miner.py | 25 subreddits buying intent extraction |
| 7:00 AM | competitor_monitor.py | 19 apps, 6 niches, iTunes API |
| 7:30 AM | system_health_monitor.py | 14-point health check |
| 8:00 AM | memory_manager.py --heartbeat | Update HEARTBEAT.md for morning check |
| 8:30 AM | compliance_scanner.py | FTC/CAN-SPAM content audit |
| 8:45 AM | compliance_deadline_tracker.py | 21 regulatory deadline alerts |
| 9:15 AM | telegram_community_monitor.py | 26 channels, 8 niches, signal scoring |

### P0 gaps to add:
```
# Tweet auto-drafter (generate daily tweet batches)
30 7 * * * cd $BASE && $PYTHON AUTOMATIONS/tweet_auto_drafter.py --batch 10 >> AUTOMATIONS/logs/tweet_drafter.log 2>&1

# Quote tweet scanner (scan latest scrape for quote opportunities)
0 8 * * * cd $BASE && $PYTHON AUTOMATIONS/quote_tweet_scanner.py --min-likes 200 >> AUTOMATIONS/logs/quote_scanner.log 2>&1

# Content trend pipeline (find top posts, generate own versions)
0 */2 * * * cd $BASE && $PYTHON AUTOMATIONS/content_trend_pipeline.py --scan --generate >> AUTOMATIONS/logs/content_trends.log 2>&1

# Niche meta detector (live trend data)
15 7 * * * cd $BASE && $PYTHON AUTOMATIONS/niche_meta_detector.py >> AUTOMATIONS/logs/niche_meta.log 2>&1
```

---

## Layer 2: Claude Cowork Scheduled Tasks (NEW, Feb 25, 2026)

Claude Desktop's Cowork feature now supports recurring scheduled tasks. These run within Claude Desktop when the app is open.

### Setup
1. Open Claude Desktop app
2. Open Cowork mode
3. Type `/schedule` to create a new scheduled task
4. Or click "Scheduled" in sidebar > "+ New task"

### Recommended Cowork Scheduled Tasks

**Daily Morning Briefing (7:00 AM, Weekdays)**
```
Read OPS/HEARTBEAT.md, check AUTOMATIONS/logs/ for overnight results,
scan LEDGER/ALPHA_STAGING.csv for new PENDING_REVIEW entries, check
OPS/active-tasks.md for crashed tasks. Generate a 20-line morning briefing
summarizing: new alpha count, lead pipeline status, content ready to post,
any errors in logs, top 3 priorities for today. Save to OPS/DAILY_BRIEFING_TODAY.md.
```

**Content Quality Audit (9:00 AM, Daily)**
```
Scan CONTENT/social/ for any files modified in last 24 hours. Check each
against .claude/rules/copy-style.md voice guidelines. Flag any that fail
the @pipelineabuser energy test. Check for banned AI vocabulary, em dashes,
hedge stacking. Save audit to OPS/CONTENT_QA_QUEUE/daily_audit.md.
```

**Alpha Processing Sweep (11:00 AM, Daily)**
```
Check LEDGER/ALPHA_STAGING.csv for PENDING_REVIEW entries. Process up to
50 entries using .claude/rules/alpha-review.md criteria. Route APPROVED
entries to appropriate LEDGER CSVs. Generate content from top 5 approved
entries (3 tweets + 1 thread per Zero Waste Protocol). Save content to
CONTENT/social/auto_generated/.
```

**Competitor + Trend Snapshot (2:00 PM, Weekdays)**
```
Run a quick scan of top 10 competitors from AUTOMATIONS/competitor_monitor.py
output. Check Google Trends for our 5 niche keywords. Check latest
LEDGER/TREND_SIGNALS.csv entries. Identify any breaking trends or competitor
moves. Save snapshot to OPS/TREND_SNAPSHOTS/.
```

**Session Prep (6:00 PM, Daily)**
```
Prepare for evening work session. Update OPS/HEARTBEAT.md with latest
numbers. Check all cron job logs for errors. Create OPS/EVENING_PRIORITIES.md
with top 5 things to work on tonight ranked by revenue impact.
```

**Weekly Self-Audit (Monday 8:00 AM)**
```
Run full audit: check all 57+ cron jobs ran successfully last week.
Count new alpha entries, content generated, leads qualified. Check venture
performance scores. Identify any stale alpha (>30 days old). Check
compliance deadlines approaching. Generate OPS/WEEKLY_SELF_AUDIT.md.
```

**Weekly Security Scan (Sunday 3:00 AM)**
```
Scan all Python scripts in AUTOMATIONS/ for: hardcoded credentials,
missing safe_path() validation, files writing outside PROJECT_ROOT.
Check SECRETS/ directory permissions. Verify .gitignore includes all
sensitive files. Save to OPS/SECURITY_SCAN_WEEKLY.md.
```

### Cowork Limitations
- Requires Claude Desktop to be open and computer awake
- Skips tasks if app is closed at scheduled time (runs next time app opens)
- Better for intelligent/adaptive tasks than rigid automation
- Use Layer 1 (cron) for must-run-exactly-on-time tasks
- Use Layer 2 (Cowork) for tasks that benefit from AI reasoning

---

## Layer 3: Claude Code Headless + runCLAUDErun (NEW)

For tasks that need Claude Code's full tool access on a schedule.

### Option A: runCLAUDErun (macOS Native Scheduler)
Download from https://runclauderun.com/
- Native macOS app for scheduling Claude Code tasks
- GUI for setting up recurring prompts
- No cron configuration needed
- Good for: code reviews, security audits, test runs

### Option B: Claude Code Headless via Cron
```
# Example: Daily security audit at 4 AM
0 4 * * * claude -p "Read OPS/HEARTBEAT.md and check AUTOMATIONS/logs/. If any RED items, create OPS/URGENT_ALERT.md." >> /tmp/claude-security-audit.log 2>&1

# Example: Weekly alpha deep-dive (Sunday 6 AM)
0 6 * * 0 claude -p "Process all PENDING_REVIEW entries in ALPHA_STAGING.csv. Generate content per Zero Waste Protocol." >> /tmp/claude-alpha-weekly.log 2>&1
```

### Option C: GitHub Actions with Claude Code Action
For tasks that should run even if laptop is off:
```yaml
name: Daily PRINTMAXX Automation
on:
  schedule:
    - cron: '0 12 * * *'  # Noon UTC = 7 AM EST
jobs:
  daily-automation:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          prompt: "Run daily alpha processing and content generation pipeline"
```

---

## Layer Selection Guide

| Task Type | Best Layer | Why |
|-----------|-----------|-----|
| Data scraping/API calls | Layer 1 (cron) | Needs reliability, no AI reasoning |
| Content quality review | Layer 2 (Cowork) | Benefits from AI judgment |
| Code security audit | Layer 3 (Claude Code) | Needs full tool access |
| Lead pipeline processing | Layer 1 (cron) | Must run reliably at scale |
| Strategic daily briefing | Layer 2 (Cowork) | Benefits from synthesis ability |
| Alpha processing + routing | Layer 1 + Layer 2 | Cron for processing, Cowork for quality |
| Self-audit + compliance | Layer 2 (Cowork) | Needs adaptive reasoning |
| Content generation | Layer 2 (Cowork) | Needs creative AI capability |
| Trend detection + response | Layer 1 + Layer 2 | Cron scrapes, Cowork analyzes |

---

## Full Daily Timeline (All Layers)

```
3:00 AM  [CRON] Lead qualification pipeline
4:00 AM  [CRON] Import sourcing scanner
5:00 AM  [CRON] Memory manager full refresh
5:30 AM  [CRON] Twitter alpha scraper (89+ accounts)
5:45 AM  [CRON] Unified alpha monitor (350+ sources)
6:00 AM  [CRON] Alpha review bot
6:30 AM  [CRON] Alpha auto-processor + Reddit pain miner
7:00 AM  [COWORK] Morning briefing generation
7:00 AM  [CRON] Competitor monitor (19 apps)
7:15 AM  [CRON] Niche meta detector
7:30 AM  [CRON] Tweet auto-drafter (10 tweets/day)
8:00 AM  [CRON] Quote tweet scanner + Heartbeat update
8:30 AM  [CRON] Compliance scanner
8:45 AM  [CRON] Compliance deadline tracker
9:00 AM  [COWORK] Content quality audit
9:15 AM  [CRON] Telegram community monitor
11:00 AM [COWORK] Alpha processing sweep
2:00 PM  [COWORK] Competitor + trend snapshot
6:00 PM  [COWORK] Session prep
9:15 PM  [CRON] Backup
11:59 PM [CRON] Daily summary generation
```

---

## Setup Checklist

- [ ] Verify cron is running: `crontab -l | wc -l` (should be 57+)
- [ ] Add P0 gap cron entries (tweet_auto_drafter, quote_tweet_scanner, content_trend_pipeline, niche_meta_detector)
- [ ] Install Claude Desktop if not already installed
- [ ] Set up 7 Cowork scheduled tasks (morning briefing, content audit, alpha sweep, trend snapshot, session prep, weekly audit, security scan)
- [ ] Optional: Install runCLAUDErun for additional Claude Code scheduling
- [ ] Optional: Set up GitHub Actions for cloud-based scheduling
- [ ] Test all scheduled tasks manually first
- [ ] Monitor logs for 1 week to verify everything runs correctly

---

## Monitoring

**Quick check all layers:**
```bash
# Layer 1: Check cron ran
tail -5 AUTOMATIONS/logs/*.log

# Layer 2: Check Cowork tasks
# Open Claude Desktop > Scheduled > View past runs

# Layer 3: Check Claude Code scheduled runs
tail -5 /tmp/claude-*.log
```

**Full health check:**
```bash
python3 AUTOMATIONS/system_health_monitor.py --quick
```


---

## Pending Enhancement (ALPHA1773997195, Score: 20)

**Source:** ProductHunt | **URL:** https://www.producthunt.com/products/claude-code-scheduled-tasks
**Added:** 2026-03-22T19:00:20-04:00

[PH LAUNCH] Claude Code Scheduled Tasks: Schedule recurring tasks locally and in the cloud easily

