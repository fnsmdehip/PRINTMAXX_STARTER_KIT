# DISPATCH HANDOFF — April 24, 2026
# Paste this into a fresh Claude Code session (Opus 4.7, max effort, max context)

You are resuming work on PRINTMAXX after a ~1 week gap. Laptop was OFF. Read CLAUDE.md and SOUL.md first per session start rules, but here's the pre-digested state so you don't burn context re-discovering it.

---

## SYSTEM STATE (verified this session)

| Component | Status |
|-----------|--------|
| Revenue | **$0 — Day 65+** |
| Loop Closer (4 loops) | ALL OK (restored this session) |
| Capital Genesis Ranker | Current — 8,899 methods, last ran Apr 15 |
| Decision Engine | Ran today — 17 freelance leads, 87 READY ops |
| Control Panel | RUNNING on :9999 |
| Master Ops Bridge | Working — 14 sheets, 2,157 rows, openpyxl IS installed |
| CEO Agent | Lock CLEARED (was stuck since Mar 28). Ready to run. |
| Cron | 120 lines active, 7 intentionally disabled |
| Alpha Corpus | 19,520 entries |
| Morning Pipeline | FIRED this session (missed while laptop off) |
| Stale files | KPI_DASHBOARD (29d), DAILY_TACTICAL_PLAN (30d), ACTIONABLE_QUEUE (30d), SESSION_LOG (38d), CURRENT_STATUS (43d) |

## ALREADY COMPLETED THIS DISPATCH SESSION

1. CEO agent stale lock removed (was blocking L0 orchestrator since Mar 28)
2. Decision engine cycle ran — surfaced 17 freelance leads, 56 ecom arb, 813 P0 methods
3. Morning pipeline fired (DAG, auto-approve, actionable aggregator, daily digest, system health)
4. INFRA_AUDIT.md written (317 lines — full L0-L6 audit, Capital Genesis review)
5. MOBILE_CONTROL_PLAYBOOK.md written (250+ lines — 7 remote control options ranked)
6. DISPATCH_STATUS.md written (system state snapshot)
7. AI_ART_VENTURE_PLAYBOOK.md written (legal framework, monetization stack, DM guardrails, ComfyUI setup)
8. AI Art Venture install script: MONEY_METHODS/AI_ART_VENTURE/install_now.sh (ready to run)
9. TruthScope spec refinement analyzed, cnsnt spec refinement started (partial)
10. All 150+ deployed surge.sh URLs cataloged

## EXECUTE NOW — Priority Order

### P0: INSTALL COMFYUI + GENERATE TEST IMAGE
```bash
bash MONEY_METHODS/AI_ART_VENTURE/install_now.sh
```
If that script has issues, do it manually:
```bash
cd ~/Documents && git clone https://github.com/comfyanonymous/ComfyUI.git 2>/dev/null
cd ~/Documents/ComfyUI
pip3 install torch torchvision torchaudio --break-system-packages
pip3 install -r requirements.txt --break-system-packages
cd custom_nodes && git clone https://github.com/ltdrdata/ComfyUI-Manager.git 2>/dev/null && cd ..
python3 main.py --force-fp16
```
Then download PonyDiffusionV6XL from CivitAI into models/checkpoints/.
Generate a test image. User wants to SEE it work.

### P1: RUN ALL SCRAPERS (backfill the offline week)
```bash
python3 AUTOMATIONS/twitter_alpha_scraper.py --all --days 14
python3 AUTOMATIONS/background_reddit_scraper.py --scrape
python3 AUTOMATIONS/method_discovery_crawler.py --crawl
python3 AUTOMATIONS/alpha_auto_processor.py --process-new
```
**BOOKMARK FILTER**: Add permanent filter to twitter_alpha_scraper.py — user's Brave bookmarks contain personal content (NSFW + political from both sides for anti-echo-chamber). ONLY process business/revenue/tech/monetization alpha. Skip everything else silently. Don't log skipped personal content. Add this as both a comment block and actual filtering logic.

### P2: FIRE UP AUTONOMOUS SYSTEMS
```bash
python3 AUTOMATIONS/venture_autonomy.py --run-all
python3 AUTOMATIONS/ceo_agent.py --dag
python3 AUTOMATIONS/loop_closer.py --cycle
python3 AUTOMATIONS/rbi_loop.py --full
```

### P3: UPDATE STALE FILES
These are all 30+ days stale and need regeneration:
- `OPS/KPI_DASHBOARD.md` — regenerate from current data
- `OPS/DAILY_TACTICAL_PLAN.md` — regenerate
- `OPS/ACTIONABLE_QUEUE.md` — regenerate
- `OPS/CURRENT_STATUS.md` — rewrite with current state
- `OPS/SESSION_LOG.md` — add entry for this session
- `OPS/PRINTMAXX_SYSTEM_MAP.md` — update with any changes (23 days stale)

### P4: APP SPEC REFINEMENT
Apply TruthScope refined spec standard to cnsnt (consent app) and all other apps:
- Full edge case handling
- QA hardening
- Production-quality one-shot-buildable specification
- Follow patterns in CLAUDE.md rules (app-factory-pipeline.md)
- Apps: cnsnt (priority), Scripture Streak, NutriSnap, Pocket Alexandria

### P5: PREVENT LAPTOP SLEEP
```bash
caffeinate -dims &
```
Or install the launchd plist from MOBILE_CONTROL_PLAYBOOK.md to make it permanent.

### P6: MOBILE REMOTE CONTROL SETUP
User wants to control PRINTMAXX from iPhone. Fastest path:
1. Enable RustDesk screen recording: System Settings > Privacy & Security > Screen Recording > enable RustDesk
2. OR: Tailscale login (`/opt/homebrew/bin/tailscale login`) + expose control panel on Tailscale IP
3. Details in MOBILE_CONTROL_PLAYBOOK.md at project root

### P7: AI ART VENTURE — FULL SETUP
Read MONEY_METHODS/AI_ART_VENTURE/AI_ART_VENTURE_PLAYBOOK.md for full plan.
Key points:
- ComfyUI local gen on 64GB Mac (PonyDiffusionXL for anime/art characters)
- Monetize via Twitter + Fansly + Patreon + Throne + Cash App
- All content clearly labeled "AI-generated digital characters"
- DM agent with HARD guardrails: zero tolerance for minors/illegal content, auto-block + auto-report
- Batch generate 10-20 images per session, post 3-5x daily on Twitter
- Legal protection framework in the playbook (read it)

### P8: GOOGLE DRIVE BACKUP
Set up rclone or gdrive CLI to push ledgers and critical docs to Google Drive for phone access.

## KEY FILES TO READ FIRST
- `CLAUDE.md` (root, points to `.claude/CLAUDE.md`)
- `.claude/CLAUDE.md` — 33 rules, session start/end protocol
- `AUTOMATIONS/SOUL.md` — behavioral directives
- `OPS/PERSISTENT_TASK_TRACKER.md` — current task state
- `OPS/HEARTBEAT.md` — system heartbeat
- `INFRA_AUDIT.md` — full infrastructure audit from this session
- `MOBILE_CONTROL_PLAYBOOK.md` — remote control options
- `MONEY_METHODS/AI_ART_VENTURE/AI_ART_VENTURE_PLAYBOOK.md` — AI art venture

## HUMAN BLOCKERS (user will handle separately)
These are the ONLY things preventing revenue:
| Action | Time | Unlocks |
|--------|------|---------|
| Gumroad account | 45 min | 13 products at $7-97 each |
| Surge.sh login fix | 5 min | 136 site updates + SEO |
| Fiverr/Upwork profiles | 20 min | Freelance arbitrage |
| Affiliate signups | 30 min | 6 supplement pages |
| Tailscale iPhone login | 5 min | Mobile dashboard |
| X multi-account stack | varies | 15+ content ops |

## RULES REMINDER (from CLAUDE.md)
1. SHIP NOW — deploy before building new
2. NO ORPHANS — every doc needs a consumer
4. AUTONOMOUS — don't ask permission, execute
10. PARALLEL BY DEFAULT — 5 items = 5 agents
17. NO DEAD CODE — test immediately, wire to caller
18. API-KEY OVER OAUTH — all `claude -p` calls use --api-key
21. RBI OVER BUILDING — research, backtest, then implement
22. ZERO FAKES — no stubs, no mocks
29. NEVER DEFER — complete in this session
31. ZERO SIMULATED DATA — real sensors only

## SESSION END CHECKLIST
1. Update OPS/PERSISTENT_TASK_TRACKER.md
2. Update OPS/SESSION_LOG.md
3. Generate content (Rule 9: 3 tweets + 1 thread minimum)
4. If architecture changed: update OPS/PRINTMAXX_SYSTEM_MAP.md
5. If new resources created: update OPS/RESOURCE_MANIFEST.md + rerun capital_genesis_ranker.py --rank

---
*Generated by Dispatch session, April 24, 2026*
*Paste into Claude Code with Opus 4.7 + max effort + max context*
