# Claude Cowork Integration Plan

**Created:** 2026-02-27
**Status:** READY TO IMPLEMENT
**Current setup:** 57+ cron entries via printmaxx_cron.sh + Ralph loops + Claude Code CLI

---

## TL;DR

Cron stays for data pipelines. Ralph stays for overnight Claude work. Add Cowork for 5 new daytime AI synthesis tasks. Nothing moves from Layer 1.

**Decision matrix for any new task:**
- Python/bash + overnight → CRON
- Needs Claude + writes code → RALPH LOOP (Claude Code)
- Needs Claude + daytime + produces document → COWORK SCHEDULED TASK

---

## Feature Comparison

| Feature | Cron (launchd) | Ralph Loops (Claude Code) | Cowork Scheduled Tasks |
|---------|---------------|--------------------------|----------------------|
| Runs overnight | YES (launchd wakes Mac) | YES (terminal stays open) | NO (needs Desktop app open) |
| Needs AI reasoning | NO | YES | YES |
| Writes code/scripts | NO | YES | YES (sandboxed VM) |
| Runs Python scripts | YES | YES | YES (limited) |
| Cost | $0 | Claude Max subscription | Claude Max subscription |
| Sandboxing | None (full system access) | Project guardrails.py | Linux VM (strongest) |
| Scheduling | crontab syntax (flexible) | Manual/cron-triggered | UI-based (daily/weekly/custom) |
| Parallel execution | Unlimited | ~5-10 concurrent | Unknown limit |
| Failure recovery | Log + retry in cron | Agent handles | Auto-retry unclear |
| Can access internet | YES | YES | YES (sandboxed) |
| Can push to git | YES | YES | YES (mount project folder) |

---

## What Stays as Cron (ALL of Layer 1)

Every one of the 57+ cron entries stays. These are Python/bash scripts that don't need AI reasoning:

**Data Pipelines (every 2-4h):**
- `ecom_arb_engine.py` — scrapes product prices
- `freelance_demand_scanner.py` — scans Reddit/Upwork
- `trend_aggregator.py` — aggregates trend signals
- `browser_scraper_daily.py` — Reddit JSON API scraping
- `twitter_alpha_scraper.py` — Twitter bookmark extraction

**Daily Operations (fixed times):**
- `daily_agent_runner.py` — 6 AM status check
- `auto_content_poster.py` — every 2h posting
- `build_enhanced_master_ops.py` — daily spreadsheet rebuild
- `ship_captain.py` — shipping pipeline
- `perpetual_ship_engine.sh` — auto-backup at 9 PM
- `heartbeat_updater.py` — every 30 min system pulse

**Weekly:**
- `backup_system.py --full` — Sunday 3 AM
- Winner reports, engagement analysis

**Why these stay:** They're pure data processing. No Claude reasoning needed. Cron via launchd runs even when you're asleep. Moving them to Cowork would make them LESS reliable.

---

## What Stays as Ralph Loops (Layer 2)

Ralph loops = iterative Claude Code sessions that read files, reason, write code, repeat.

**Keep these as Ralph:**
- `ralph_overnight_loop.sh` — overnight alpha extraction + content generation
- `run_parallel_loops.sh` — parallel research loops
- Any task that needs Claude to write/modify code
- Any task that runs overnight

**Upgrade:** Add `-w` flag (git worktree isolation) to all Ralph loops for safer parallel iterations:
```bash
# Before
claude-code --task "extract alpha from bookmarks"
# After
claude-code --task "extract alpha from bookmarks" -w
```

---

## New Cowork Scheduled Tasks (Layer 3)

These 5 tasks need Claude reasoning but are daytime activities that produce documents, not code:

### 1. Morning Intelligence Brief (Daily, 9 AM)
**What:** Synthesize overnight logs into a 1-page actionable briefing
**Reads:** logs/, HEARTBEAT.md, LEDGER/ changes, git diff since last brief
**Writes:** OPS/DAILY_BRIEF_{date}.md
**Why Cowork:** Needs AI reasoning to prioritize and synthesize. Not mechanical.

### 2. Weekly Strategy Narrative (Monday, 10 AM)
**What:** Turn week's data into "here's what to do about it" memo
**Reads:** All daily briefs, revenue tracker, alpha staging, task tracker
**Writes:** OPS/WEEKLY_STRATEGY_{date}.md
**Why Cowork:** Strategic synthesis, not data processing

### 3. Compliance Triage (Thursday, 11 AM)
**What:** Prioritize the 285+ CRITICAL compliance issues by revenue risk
**Reads:** NSFW compliance checklist, content QA queue, escalation logs
**Writes:** OPS/COMPLIANCE_TRIAGE_{date}.md
**Why Cowork:** Needs judgment to rank by risk/impact

### 4. Alpha-to-OPS Routing (Daily, 10:30 AM)
**What:** Route new alpha entries to the right playbook/method
**Reads:** LEDGER/ALPHA_STAGING.csv (new entries), 03_PLAYBOOKS/INDEX.md
**Writes:** Updates routing in alpha entries, creates venture files
**Why Cowork:** Strategic routing decisions, not mechanical copy

### 5. Content QA Voice Check (Sunday, 2 PM)
**What:** Review queued social posts against copy-style.md voice guidelines
**Reads:** OPS/CONTENT_QA_QUEUE/, .claude/rules/copy-style.md
**Writes:** Approved/rejected status in QA queue
**Why Cowork:** Voice judgment, needs AI to match tone profiles

---

## Cowork Setup Steps

1. **Open Claude Desktop app** (required for Cowork)
2. **Mount ONLY the PRINTMAXX folder** — matches guardrails.md
3. Create each scheduled task via Cowork UI:
   - Name: e.g., "Morning Intelligence Brief"
   - Schedule: Daily at 9 AM (or whatever)
   - Prompt: Include exact file paths to read and write
   - Permissions: Read + Write within project folder only

---

## Claude Code 2.x Features to Use NOW

### Agent Teams (Experimental)
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```
Formalizes the 11+ parallel agents into structured teams with task lists and coordination. We already use this (printmaxx-reboot team).

### Git Worktree Isolation
```bash
claude-code --task "task" -w
```
Each agent gets its own worktree. Prevents file conflicts when running 5+ agents in parallel. Use this for ALL future Ralph loops.

### Automatic Memory
Claude Code now has built-in memory at `~/.claude/projects/`. Test it alongside the existing file-based memory system (PERSISTENT_TASK_TRACKER.md). Don't remove the file-based system yet — it's proven.

### WorktreeCreate/WorktreeRemove Hooks
Auto-run guardrails.py validation when new worktrees are created:
```json
// .claude/settings.json
{
  "hooks": {
    "WorktreeCreate": "python3 AUTOMATIONS/guardrails.py --test",
    "WorktreeRemove": "echo 'Worktree cleaned up'"
  }
}
```

### /teleport
Handoff sessions between devices. Useful if you switch from Mac to iPad.

---

## OpenClaw Status: DEAD, DO NOT USE

Your instinct to stop using OpenClaw was correct:
- 386 malicious ClawHub packages discovered
- Port 18789 exposed to internet by default
- Plaintext credential leakage
- Ban wave from Anthropic
- Multiple CVEs and security advisories (Aikido, Cisco)

**Current architecture (official CLI + cron + guardrails.py) is the correct one.** No changes needed.

---

## claude-code-scheduler Plugin: SKIP

The `jshchnz/claude-code-scheduler` GitHub plugin is for people who don't know cron syntax. You have `printmaxx_cron.sh` with 57 working entries. No value in adding another scheduling layer.

---

## Hybrid Architecture Summary

```
Layer 1: CRON (launchd)
├── Data pipelines (scraping, aggregation, posting)
├── Daily ops (spreadsheet builds, backups, heartbeat)
├── Runs 24/7 including overnight
└── 57+ entries, ALL STAY

Layer 2: RALPH LOOPS (Claude Code CLI)
├── Overnight alpha extraction
├── Code generation tasks
├── Complex multi-file operations
├── Upgrade: add -w flag for worktree isolation
└── Keep ralph_overnight_loop.sh as-is

Layer 3: COWORK SCHEDULED TASKS (NEW)
├── Morning intelligence brief (daily 9 AM)
├── Weekly strategy narrative (Monday 10 AM)
├── Compliance triage (Thursday 11 AM)
├── Alpha-to-OPS routing (daily 10:30 AM)
├── Content QA voice check (Sunday 2 PM)
└── ONLY runs when Mac is awake + Desktop app open
```

**Rule: Nothing moves DOWN a layer. Layer 3 is additive only.**

---

## Migration Checklist

- [ ] Enable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in shell profile
- [ ] Add `-w` flag to all Ralph loop scripts
- [ ] Set up 5 Cowork scheduled tasks (when Desktop app is available)
- [ ] Test Cowork scheduled task #1 (morning brief) manually first
- [ ] Verify Cowork only mounts PRINTMAXX folder (sandbox security)
- [ ] Keep file-based memory (PERSISTENT_TASK_TRACKER.md) alongside auto-memory
- [ ] Remove any OpenClaw references from scripts/docs
