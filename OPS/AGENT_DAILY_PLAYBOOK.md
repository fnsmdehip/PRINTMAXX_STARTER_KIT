# Agent Daily Playbook

**This is THE guide for any new Claude agent session. Read it. Do what it says. No re-explaining needed.**

---

## Step 1: Orient (10 seconds)

```bash
python3 AUTOMATIONS/daily_agent_runner.py --status
```

This shows: priorities, blockers, recent files, account status, next action. If this script doesn't exist or errors, read `OPS/SESSION_HANDOFF_FEB12_2026.md` instead.

## Step 2: Check what's printing

```bash
python3 AUTOMATIONS/venture_performance_tracker.py --recommend
```

- Score >70 = DOUBLE_DOWN (scale it)
- Score 20-70 = MAINTAIN (keep running)
- Score <20 = KILL (stop wasting time)

## Step 3: Execute top priority

### Decision tree:

**Are accounts created?** Check `LEDGER/ACCOUNTS.csv`
- NO → Read `OPS/ACCOUNT_CREATION_NOW.md`, prompt user to create accounts NOW
- YES → Continue below

**Are products listed?** Check if Gumroad/Fiverr/Etsy have products
- NO → Copy-paste from ready listings (see "Ready-to-list" below)
- YES → Continue below

**Is content posted?** Check social accounts
- NO → Upload Buffer CSVs from `AUTOMATIONS/content_posting/`
- YES → Continue below

**Is anything converting?**
- NO → Run A/B tests: `python3 scripts/experiment_runner.py recommend`
- YES → Double down on winners, kill losers

### Ready-to-list assets (copy-paste ready):

| Platform | File | Count |
|----------|------|-------|
| Gumroad | `PRODUCTS/GUMROAD_READY_LISTINGS.md` | 10 products |
| Fiverr | `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md` | 10 gigs |
| Upwork | `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md` | 5 profiles |
| Etsy | `PRODUCTS/ECOM_LISTINGS_READY/ETSY_LISTINGS_COMPLETE.md` | Full listings |
| Buffer | `AUTOMATIONS/content_posting/` | 12 CSVs, 1,278 posts |
| Substack | `CONTENT/substack_posts/SUBSTACK_NOTES_50.csv` | 50 notes |
| Medium | `CONTENT/medium_articles/` | Articles ready |

### Time-sensitive items:
- **Ramadan app** - Feb 28 start. Deploy NOW: `ralph/loops/app_factory/output/ramadan-tracker/`
- **Cold email sequences** - `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv`

## Step 4: Research & RBI (background)

```bash
python3 AUTOMATIONS/daily_nocost_rbi_scanner.py --next-actions
```

Always scan for new zero-cost opportunities. New alpha → `LEDGER/ALPHA_STAGING.csv`

## Step 5: Content squeeze (MANDATORY)

Every session generates minimum:
- 3 tweets
- 1 thread
- Save to `CONTENT/social/` as PENDING_REVIEW
- Voice: `.claude/rules/copy-style.md` (consequence-first, specific numbers, no AI slop)

## Step 6: Log learnings

```bash
python3 AUTOMATIONS/daily_agent_runner.py --learning "what worked and what didn't"
```

---

## Quick decision trees

### "What should I build next?"
1. `python3 AUTOMATIONS/venture_performance_tracker.py --recommend`
2. DOUBLE_DOWN items exist? → Scale those
3. No clear winner? → `OPS/FIRST_PRINCIPLES_OPPORTUNITY_MATRIX.md`
4. Default: list products on platforms (accounts are bottleneck)

### "Something isn't working"
1. Account blocker? → `OPS/ACCOUNT_CREATION_NOW.md`
2. Tech issue? → Try fallback chain, log to `OPS/logs/BLOCKED_[topic].md`
3. Method dead? → `python3 AUTOMATIONS/venture_performance_tracker.py --score METHOD_ID`

### "User hasn't said anything"
Keep building. Priority order:
1. Deploy ready apps
2. List ready products
3. Generate and post content
4. Run clipping automation pipeline
5. Distribute ecom across platforms
6. Research new alpha
7. Optimize existing methods

### "I need to automate something"
1. Check `AUTOMATIONS/` for existing scripts
2. Check `AUTOMATIONS/auto_list_products.py` for browser automation
3. Check `AUTOMATIONS/clip_automation_pipeline.py` for clipping
4. Check `AUTOMATIONS/ecom_distributor.py` for multi-platform distribution

---

## Key files

| Need | File |
|------|------|
| Orientation | `python3 AUTOMATIONS/daily_agent_runner.py --status` |
| What's printing | `python3 AUTOMATIONS/venture_performance_tracker.py --recommend` |
| Account setup | `OPS/ACCOUNT_CREATION_NOW.md` |
| Copy style | `.claude/rules/copy-style.md` |
| All listings | `PRODUCTS/GUMROAD_READY_LISTINGS.md` + `PRODUCTS/FREELANCE_LISTINGS_READY/` |
| Session handoff | `OPS/SESSION_HANDOFF_FEB12_2026.md` |
| Master nav | `.claude/CLAUDE.md` |
| Clipping pipeline | `AUTOMATIONS/clip_automation_pipeline.py` |
| Ecom distribution | `AUTOMATIONS/ecom_distributor.py` |
| Quant terminal | `python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary` |

---

## The rule

This system is self-running. You don't need the user to explain what to do. Read the status, execute the top priority, log what you learned. The learning loop makes priorities better over time. Bias toward action. Ship first, document second.
