# PRINTMAXX Overnight Process Guide

## The System

When you go to bed, PRINTMAXX keeps working. Three layers of automation run while you sleep.

---

## Layer 1: Cron Jobs (Always Running)

These run on schedule regardless of Claude Code sessions:

| Schedule | Script | What It Does |
|----------|--------|-------------|
| Daily 6:00 AM | `daily_twitter_scraper.py` | Scrapes 92 high-signal Twitter accounts |
| Daily 6:15 AM | `daily_reddit_scraper.py` | Scrapes 41 tracked subreddits |
| Daily 2:00 AM | `overnight_master_runner.sh` | Runs ALL 30+ scrapers/analyzers in sequence |
| Every 30 min (midnight-8am) | `auto_resume_monitor.sh` | Checks if overnight run was interrupted, auto-resumes |
| Weekly Mon 3:00 AM | `platform_rpm_tracking.py` | Tracks RPM/CPM rates across platforms |
| Weekly Mon 3:30 AM | `creator_program_monitoring.py` | Monitors creator monetization programs |
| Weekly Mon 4:00 AM | `aso_keyword_research.py` | App Store keyword research |

### Setup Cron

```bash
crontab -e
# Paste the cron entries from AUTOMATIONS/crontab_printmaxx.txt
```

### Check Cron Health

```bash
# See what's scheduled
crontab -l

# Check overnight log
tail -50 AUTOMATIONS/logs/overnight_$(date +%Y-%m-%d).log

# Check status
cat AUTOMATIONS/logs/overnight_status_$(date +%Y-%m-%d).json | python3 -m json.tool
```

---

## Layer 2: Ralph Overnight Loop (Claude Code Autonomous)

Launches Claude Code in autonomous ralph loop mode. Each iteration:
1. Reads progress file to know what previous iterations did
2. Picks highest-value task (alpha vetting, content gen, scraper runs)
3. Executes for ~15 min
4. Writes results to `ralph/overnight_progress.md`
5. Exits and restarts fresh (no context bloat)

### Launch Before Bed

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
bash AUTOMATIONS/ralph_overnight_loop.sh 5 60
# 5 iterations, 60s between each
```

### Check Morning Progress

```bash
cat ralph/overnight_progress.md
tail -100 AUTOMATIONS/logs/ralph_overnight_$(date +%Y-%m-%d).log
```

---

## Layer 3: Background Agents (In-Session)

When you trigger agents before bed, they run until:
- They complete
- They hit token limits (resets 7 PM daily)
- Claude Code session ends

These are the agents launched during interactive sessions that continue working.

---

## Token Limit Handling

**Problem:** Claude Max has daily token limits. If hit during overnight, work stops.

**Solution:** The auto-resume monitor detects interruption and:
1. Checks if overnight runner completed (grep for "COMPLETE" in log)
2. If interrupted, restarts the runner from scratch (scripts are idempotent)
3. If Claude session died, pure Python scrapers still run via cron

**Token Reset:** Happens at 7 PM daily. If limit hit before then:
- Cron Python scripts continue (they don't use Claude tokens)
- Claude-dependent tasks wait for reset
- Auto-resume monitor triggers finishing run after 7 PM

**Prevention:**
- Ralph loop has max 5 iterations by default
- Each iteration has 15 min timeout
- Overnight runner has per-script timeouts
- Most scrapers are pure Python (no Claude tokens needed)

---

## Morning Checklist

When you wake up:

```bash
# 1. Check overnight results
cat AUTOMATIONS/logs/overnight_status_$(date +%Y-%m-%d).json

# 2. Check ralph progress
cat ralph/overnight_progress.md

# 3. Count new leads
ls -la AUTOMATIONS/leads/

# 4. Count new alpha
grep "$(date +%Y-%m-%d)" LEDGER/ALPHA_STAGING.csv | wc -l

# 5. Check for errors
grep "FAILED\|ERROR" AUTOMATIONS/logs/overnight_$(date +%Y-%m-%d).log

# 6. Or just run the quant terminal
python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Cron not running | `crontab -l` to verify entries exist |
| Script permission denied | `chmod +x AUTOMATIONS/*.sh` |
| Python not found | Use full path: `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3` |
| Playwright not working | Cron scripts use `requests` not Playwright (no browser needed) |
| Token limit hit | Wait for 7 PM reset, cron Python scripts continue regardless |
| Lock file stuck | `rm /tmp/printmaxx_auto_resume.lock` |

---

## File Locations

| File | Purpose |
|------|---------|
| `AUTOMATIONS/overnight_master_runner.sh` | Runs all 30+ scripts |
| `AUTOMATIONS/auto_resume_monitor.sh` | Detects interruption, auto-resumes |
| `AUTOMATIONS/ralph_overnight_loop.sh` | Ralph loop for Claude autonomous work |
| `AUTOMATIONS/crontab_printmaxx.txt` | All cron entries to install |
| `AUTOMATIONS/logs/overnight_*.log` | Daily run logs |
| `AUTOMATIONS/logs/overnight_status_*.json` | Script-by-script status |
| `AUTOMATIONS/logs/auto_resume.log` | Resume monitor log |
| `ralph/overnight_progress.md` | Ralph loop iteration progress |
