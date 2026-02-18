# LAUNCH OVERNIGHT MEGA RALPH LOOP

**Status:** READY FOR LAUNCH
**Model:** Opus (maximum quality)
**Mode:** Autonomous (no human approval needed)
**Guardrails:** Project folder only, Chrome MCP for scraping, no Bash

---

## Quick Launch (Recommended)

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph
./run_mega.sh 7  # Run for 7 days = 147 iterations
```

This launches in background with `nohup` - terminal can close, loop keeps running.

---

## What It Does

### Day Cycle (21 iterations per day)

| Iterations | Phase | What Happens |
|------------|-------|--------------|
| 1-3 | DAILY_RESEARCH | Scan Twitter, Reddit, Product Hunt, web for alpha. Append to ALPHA_STAGING.csv |
| 4 | REFLECTION | Synthesize findings, update priorities, identify highest ROI opportunities |
| 5-10 | CONTENT_GENERATION | Social posts, email sequences, landing copy, longtail pages |
| 11-15 | EXECUTION | App builds, automation scripts, SEO/ASO optimization |
| 16-20 | INTELLIGENCE | Competitor monitoring, platform changes, deep alpha hunting |
| 21 | CHECKPOINT | Summarize day, flag items for human review, plan next day |

### Outputs Per Day

- **Research:** 10-20 new alpha entries in ALPHA_STAGING.csv
- **Content:** 30-50 social posts, 3-5 email sequences, 2-3 landing pages
- **Execution:** 5-10 app tasks, 2-3 automation scripts, SEO/ASO updates
- **Intelligence:** Competitor updates, risk radar, cross-pollination discoveries

### Full 7-Day Run = 147 Iterations

- **Alpha discovered:** 70-140 entries
- **Content generated:** 210-350 social posts, 21-35 email sequences, 14-21 landing pages
- **Apps improved:** 35-70 tasks across all apps
- **Automation built:** 14-21 scripts
- **Intelligence reports:** 35+ competitor/platform/tool analyses

---

## Monitor Progress

### Live log (see what's happening now)
```bash
tail -f /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/logs/mega_*.log
```

### Progress file (current state)
```bash
cat /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/mega/.ralph/progress.md
```

### Activity log (what's been done)
```bash
tail -100 /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/mega/.ralph/activity.log
```

### Errors (if any)
```bash
cat /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/mega/.ralph/errors.log
```

### Master tracker (all tasks)
```bash
head -50 /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/LEDGER/MEGA_RALPH_TRACKER.csv
```

### Checkpoints (human review items)
```bash
ls /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/mega/checkpoints/
cat /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/mega/checkpoints/PENDING_*.md
```

### Research output
```bash
ls /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/mega/output/
```

---

## Stop the Loop

```bash
# Find the PID
cat /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/mega/.ralph/mega.pid

# Kill it
kill [PID]

# Or just kill all ralph processes
pkill -f "mega"
```

---

## Guardrails (What It Can't Do)

**Blocked operations:**
- Delete any files
- Run bash commands (no terminal access)
- Access files outside project folder
- Make purchases
- Create accounts
- Publish content (flags for human review)

**What it flags for human approval:**
- Tools/services to buy → `checkpoints/PENDING_PURCHASES.md`
- Content ready to publish → `checkpoints/PENDING_PUBLISH.md`
- Accounts to create → `checkpoints/PENDING_ACCOUNTS.md`
- High-risk tactics → `checkpoints/PENDING_HIGH_RISK.md`

**It continues working on non-blocked tasks while waiting for human approval.**

---

## Launch Options

### Short test run (1 day = 21 iterations, ~3-4 hours)
```bash
./run_mega.sh 1
```

### Overnight (3 days = 63 iterations, default)
```bash
./run_mega.sh 3
```

### Weekend (7 days = 147 iterations)
```bash
./run_mega.sh 7
```

### Full week work sprint (10 days = 210 iterations)
```bash
./run_mega.sh 10
```

---

## What To Expect

### Hour 1 (Iterations 1-6)
- Scanning high-signal Twitter accounts
- Web research across 10 categories
- First alpha entries appear in ALPHA_STAGING.csv
- REFLECTION phase synthesizes findings

### Hours 2-4 (Iterations 7-21)
- Content generation begins (social posts, emails, landing pages)
- App development tasks executing
- Intelligence gathering (competitors, platforms, tools)
- Day 1 checkpoint summary created

### Day 2+
- Loop continues 24/7
- Each day builds on previous findings
- Priorities auto-recalculate daily (REFLECTION phase)
- Quality improves as guardrails.md accumulates learnings

### After 7 Days
- 100+ alpha entries discovered
- 300+ content pieces generated
- 50+ app/automation tasks completed
- 40+ intelligence reports
- Full checkpoint review queue for human

---

## Recovery From Crashes

The loop is crash-resistant:
- State saved after EVERY iteration
- `.ralph/progress.md` tracks current position
- Can resume from last completed task
- Lost iterations just skip, next iteration continues
- All outputs written to disk immediately (nothing in memory)

If terminal crashes:
1. Check `.ralph/progress.md` for last completed iteration
2. Relaunch with `./run_mega.sh [days]`
3. Loop reads state and continues where it left off

---

## Opus Token Usage

**Per iteration estimate:** 5K-15K tokens (input + output)

**Per day (21 iterations):** 105K-315K tokens

**7-day run (147 iterations):** 735K-2.2M tokens

**Your Claude Max limit:** 500K context window, high rate limits

The loop sleeps 10 seconds between iterations to respect rate limits.

If you hit limits, the loop will:
- Log the error to `.ralph/errors.log`
- Continue to next iteration after cooldown
- Human can check errors and adjust days if needed

---

## Human Review Workflow

### Daily (5 minutes)
1. Check `checkpoints/` folder for pending items
2. Approve/reject flagged purchases, content, tactics
3. Mark status: PENDING → APPROVED or REJECTED

### Weekly (30 minutes)
1. Review `LEDGER/ALPHA_STAGING.csv` - approve best findings via `/review-alpha`
2. Check `MEGA_RALPH_TRACKER.csv` - see what's been done
3. Read checkpoint summaries - plan next week priorities

### After full run (1 hour)
1. Review all checkpoints
2. Approve content for publishing
3. Integrate approved alpha into master files
4. Launch next 7-day run with updated priorities

---

## Safety Notes

**This loop is designed to run unattended overnight.**

It will NOT:
- Spend money
- Create accounts
- Publish content
- Delete files
- Access system outside project folder
- Run destructive commands

It WILL:
- Scan the web aggressively for alpha
- Generate lots of content (drafts, not published)
- Build and improve apps
- Write automation scripts
- Flag items needing human judgment

**All outputs are DRAFTS until human approval.**

---

## Launch NOW

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph
./run_mega.sh 7  # Let it run overnight for 7 days
```

Then close terminal. Loop keeps running.

Check back in the morning. Review checkpoints. Approve wins. Repeat.

**This is the PRINTMAXX way: Ship while you sleep.**
