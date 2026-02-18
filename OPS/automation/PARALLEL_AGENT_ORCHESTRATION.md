# PRINTMAXX Parallel Agent Orchestration Plan

**Last Updated:** 2026-01-20
**Purpose:** Run multiple agents simultaneously across all PrintMaxx methods to maximize throughput

---

## Core Philosophy

**Parallel Lanes + A/B Everything.** Every method runs multiple variations simultaneously. Track. Kill losers. Scale winners.

---

## Agent Types & Capabilities

### 1. Content Generator Agent
**Domain:** Longtail pages, truth pages, social posts
**Tools:** Read, Write, Glob, Grep
**Human-in-Loop:** No (auto-generate, human reviews later)

**Daily Tasks:**
- Generate 5-10 longtail pages from GEO_LONGTAIL_SLUGS_300.csv
- Generate 10-20 social posts per niche
- Create email sequence drafts

**Run Command:**
```
Generate [N] longtail pages from LEDGER/GEO_LONGTAIL_SLUGS_300.csv following .claude/rules/copy-style.md
```

### 2. Alpha Researcher Agent
**Domain:** Tweet scraping, source monitoring, trend analysis
**Tools:** Bash (AppleScript), Read, Write
**Human-in-Loop:** No (scrape and stage, human reviews)

**Daily Tasks:**
- Run daily_alpha_extractor.py across all platforms
- Stage findings to ALPHA_STAGING.csv
- Flag high-priority opportunities

**Run Command:**
```bash
python3 AUTOMATIONS/daily_alpha_extractor.py --platform X
python3 AUTOMATIONS/daily_alpha_extractor.py --platform Reddit
```

### 3. Validator Agent
**Domain:** Code review, SEO checks, content QA
**Tools:** Read, Grep, Bash (lint commands)
**Human-in-Loop:** No (flag issues, human fixes)

**Daily Tasks:**
- Validate new content against copy-style.md
- Check SEO meta tags on generated pages
- Run lint on code changes

**Run Command:**
```
Validate all new content in CONTENT/ against .claude/rules/copy-style.md. Flag AI patterns.
```

### 4. Deployer Agent
**Domain:** Build, deploy, pre-flight checks
**Tools:** Bash, Read
**Human-in-Loop:** Yes (final deploy approval)

**Tasks:**
- Run npm build
- Pre-flight deployment checklist
- Environment variable verification

### 5. Reviewer Agent
**Domain:** PR review, content approval
**Tools:** Read, Grep
**Human-in-Loop:** Yes (approval required)

**Tasks:**
- Review generated content quality
- Check for compliance issues
- Approve for publishing

---

## Parallel Execution Matrix

### Daily Autonomous Run (Overnight/Background)

| Time | Agent 1 | Agent 2 | Agent 3 |
|------|---------|---------|---------|
| 00:00 | Alpha: X Platform | Content: 5 longtails | - |
| 00:30 | Alpha: Reddit | Content: 5 more longtails | - |
| 01:00 | Alpha: YouTube | Content: 20 social posts | Validator: Check new content |
| 01:30 | Alpha: Web tools | - | Validator: Flag issues |

### Human-Supervised Run (Daytime)

| Time | Task | Agent | Human Action |
|------|------|-------|--------------|
| 09:00 | Review ALPHA_STAGING.csv | - | Mark APPROVED/REJECTED |
| 09:30 | Review flagged content | Reviewer | Approve/Request changes |
| 10:00 | Deploy approved content | Deployer | Final approval |
| 10:30 | Manual warmup activities | - | Follow/like/reply on socials |

---

## Ralph Configuration for Overnight Runs

### Content Generation Config
```yaml
# ralph_content_gen.yaml
working_dir: /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT
max_iterations: 20
task: |
  Generate 10 longtail pages from LEDGER/GEO_LONGTAIL_SLUGS_300.csv.
  Follow .claude/rules/copy-style.md strictly.
  Update CSV with published=TRUE for each generated page.
  Save pages to CONTENT/longtail_pages/
stop_conditions:
  - "BLOCKED"
  - "ERROR"
  - "Need human input"
```

### Alpha Research Config
```yaml
# ralph_alpha_research.yaml
working_dir: /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT
max_iterations: 50
task: |
  Run python3 AUTOMATIONS/daily_alpha_extractor.py for all platforms.
  Review output and stage high-signal findings.
  Update LEDGER/ALPHA_STAGING.csv with new entries.
stop_conditions:
  - "Rate limited"
  - "Login required"
  - "No browser found"
```

---

## Workstream Assignments

### Workstream A: Content Production
**Agents:** Content Generator, Validator
**Files Owned:**
- CONTENT/longtail_pages/
- CONTENT/truth_pages/
- AUTOMATIONS/content_generation/

**Collision Prevention:**
- Claim folder before editing
- Use file locks for CSVs
- Update LEDGER immediately after generation

### Workstream B: Alpha Research
**Agents:** Alpha Researcher
**Files Owned:**
- LEDGER/ALPHA_STAGING.csv
- LEDGER/SCRAPED_TWEETS_ALPHA.csv
- LEDGER/HIGH_SIGNAL_SOURCES.csv

**Collision Prevention:**
- Append-only to staging CSV
- Use unique alpha_id with timestamp
- Don't modify approved entries

### Workstream C: Infrastructure
**Agents:** Deployer, Validator
**Files Owned:**
- LANDING/printmaxx-site/
- OPS/logs/

**Collision Prevention:**
- Only one deployer at a time
- Lock during build process
- Human approval gate

---

## Method-Specific Agent Tasks

### App Factory Methods (AFM001-013)
| Method | Agent Task | Frequency |
|--------|------------|-----------|
| AFM001 Niche Adaptation | Research trending apps via appkittie | Weekly |
| AFM002 Termination Arbitrage | Monitor algrow.online | Daily |
| AFM011 FB Ads Library Mining | Search FB Ads Library keywords | Daily |
| AFM012 Screen Time Blockers | Monitor Opal competitors | Weekly |

### Marketing Channels (CH001-031)
| Channel | Agent Task | Frequency |
|---------|------------|-----------|
| CH001-005 Social Organic | Generate posts, schedule queue | Daily |
| CH029 Clipper Network | Stage clipper outreach templates | Weekly |
| CH030 LinkedIn Mining | Run LinkedIn search scripts | Weekly |
| CH031 FOIA Lead Gen | Research USAspending data | Monthly |

### Content Formats (CS001-025)
| Format | Agent Task | Frequency |
|--------|------------|-----------|
| CS001-010 Short Video | Generate scripts from templates | Daily |
| CS021 Relationship Bait | Create hook variations | Weekly |
| CS023 Math Framework | Generate revenue math threads | Weekly |

---

## Execution Commands

### Full Parallel Run (All Agents)
```bash
# Terminal 1: Alpha Research
python3 AUTOMATIONS/daily_alpha_extractor.py

# Terminal 2: Content Generation
claude "Generate 10 longtail pages from LEDGER/GEO_LONGTAIL_SLUGS_300.csv"

# Terminal 3: Validation
claude "Validate all content in CONTENT/ against copy-style.md"
```

### Platform-Specific Alpha Run
```bash
# X only (fastest, most signal)
python3 AUTOMATIONS/daily_alpha_extractor.py --platform X --tier HIGHEST

# Reddit only
python3 AUTOMATIONS/daily_alpha_extractor.py --platform Reddit

# All platforms
python3 AUTOMATIONS/daily_alpha_extractor.py
```

### Content Generation Batch
```bash
# Longtails
claude "Generate 25 longtail pages. Start from row 11 of GEO_LONGTAIL_SLUGS_300.csv"

# Social posts
claude "Generate 20 X posts for AI niche using CS006 and CS007 formats"

# Email sequences
claude "Generate 5-email welcome sequence for Faith niche"
```

---

## State Synchronization

### Before Any Run
```bash
# Check current state
cat LEDGER/STATUS_BOARD.md
head -20 LEDGER/MASTER_TASKS.md
wc -l LEDGER/ALPHA_STAGING.csv
```

### After Any Run
```bash
# Update handoff
# Agent automatically updates OPS/HANDOFF.md

# Create run log
# Agent creates OPS/logs/RUNLOG_[timestamp].md

# Verify no collisions
git status  # If using git
```

### Collision Detection
If two agents modify same file:
1. Later agent's changes flagged
2. Human resolves conflict
3. Merged version saved
4. Both agents notified

---

## Monitoring Dashboard

### Key Metrics to Track
| Metric | Source | Target |
|--------|--------|--------|
| Alpha staged/day | ALPHA_STAGING.csv | 5-10 |
| Content generated/day | CONTENT/ file count | 10-15 |
| Validation errors | OPS/logs/ | <5% |
| Build success rate | Deployer logs | 100% |

### Daily Health Check
```bash
# Count new alpha
grep "$(date +%Y-%m-%d)" LEDGER/ALPHA_STAGING.csv | wc -l

# Count new content
ls -la CONTENT/longtail_pages/ | grep "$(date +%Y-%m-%d)" | wc -l

# Check for errors
grep -r "ERROR\|BLOCKED" OPS/logs/
```

---

## Handoff Between Agents

### Agent A Finishes, Agent B Continues
1. Agent A updates HANDOFF.md with status
2. Agent A saves state to LEDGER/*.csv
3. Agent A creates RUNLOG with details
4. Agent B reads HANDOFF.md
5. Agent B continues from documented state

### Context Preservation
```
# In HANDOFF.md after each run:
## Last Agent: Alpha Researcher
## Completed: Scraped 23 X accounts, staged 8 findings
## Next: Review staged findings, run Reddit scan
## Files Modified: ALPHA_STAGING.csv, SCRAPED_TWEETS_ALPHA.csv
```

---

## Emergency Procedures

### Agent Stuck
1. Check OPS/logs/ for error details
2. Create BLOCKED_[topic].md with diagnosis
3. Kill stuck process
4. Resume from last known good state

### Rate Limited
1. Stop affected agent
2. Wait 15-30 minutes
3. Resume with --max flag for lower volume
4. Consider rotating proxy

### Data Corruption
1. Check git history (if using git)
2. Restore from backup CSV
3. Re-run affected agent
4. Verify data integrity

---

## Quick Reference

### Start Overnight Run
```bash
# Clone Ralph
git clone https://github.com/snarktank/ralph

# Configure
cp ralph_content_gen.yaml ralph/config.yaml

# Run
cd ralph && ./run.sh
```

### Morning Review
```bash
# Check what ran overnight
tail -100 OPS/logs/RUNLOG_*.md | head -50

# Review staged alpha
cat LEDGER/ALPHA_STAGING.csv | grep PENDING_REVIEW

# Check generated content
ls -la CONTENT/longtail_pages/
```

### Resume Interrupted Work
```
Read /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/OPS/HANDOFF.md and continue where we left off.
```
