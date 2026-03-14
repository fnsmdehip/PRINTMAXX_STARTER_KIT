# CEO Orchestrator

## Overview

A 16-phase autonomous orchestration cycle that manages a portfolio of revenue ventures using PROMOTE/KILL decision logic and multi-dimensional scoring. The CEO agent sits above all other agents, reads operational data from a master spreadsheet, scores ventures dynamically, makes strategic decisions, delegates to venture sub-agents, and protects high-performing ops with git-based failsafes. Designed to run 24/7 as a daemon with crash recovery via checkpoint-resume.

## Architecture

The CEO agent is a full orchestrator composed of several integrated subsystems:

```
CEO Agent (orchestrator)
├── GitGuard            -- auto-snapshot before changes, rollback on failure
├── XlsxIntel           -- reads ops from master xlsx dynamically
├── VentureScorer       -- multi-signal scoring (readiness + automation + synergy + revenue)
├── CEOBrain            -- strategic decisions (PROMOTE / ENHANCE / CREATE / KILL / DISCOVER)
├── VentureRunner       -- delegates to existing + dynamic venture agents
├── AuditTrail          -- regression detection, protected ops enforcement
├── CycleCheckpoint     -- atomic checkpoint writes, stale detection, resume-on-crash
├── Alpha Pipeline      -- triggers scrapers + alpha processor
├── Research Pipeline   -- daily research orchestrator (once/day)
├── Decision Engine     -- closed-loop decision processing
├── Content Generation  -- content creation + upgrade missions
├── System Health       -- health monitor + auto-fix
└── Cron Management     -- read/write/track scheduled tasks
```

**Phase-based cycle (simplified):**

1. **Wake** -- acquire lock, load state, check disk space
2. **Checkpoint check** -- resume from crash if stale checkpoint exists
3. **Git snapshot** -- commit current state before making changes
4. **Intel gather** -- query intelligence router for multi-venture briefing
5. **Score ventures** -- run VentureScorer across all ops (5 dimensions, 0-100 scale)
6. **Decide** -- CEOBrain produces PROMOTE/ENHANCE/CREATE/KILL/DISCOVER decisions
7. **Execute decisions** -- VentureRunner delegates to venture agents
8. **Alpha pipeline** -- trigger scrapers and alpha processing
9. **Research pipeline** -- run daily research orchestrator (time-gated)
10. **Content generation** -- trigger content creation (time-gated)
11. **Decision engine** -- process pending decisions from all agents
12. **System health** -- run health monitor, auto-fix broken cron/agents
13. **Venture autonomy** -- trigger self-managing venture engine
14. **Loop closer** -- execute decision loops, feedback loops, pipeline advancement
15. **Post-audit** -- regression detection, rollback if needed
16. **Report** -- save state, log decisions, update checkpoint

**Decision framework -- Portfolio theory:**

The system operates on the principle that 10 ventures at 30% individual success rate = 97% chance of at least one hit, 70% chance of 3+ hits. This drives the kill/double-down logic:

- **PROMOTE** (score > 70): Double down. Increase execution frequency, add resources, scale distribution.
- **ENHANCE** (score 40-70): Improve. Fix blockers, optimize automation, add missing pieces.
- **CREATE** (high-readiness ops not yet launched): Spin up new venture from xlsx ops data.
- **KILL** (score < 15, not protected): Sunset. Stop execution, archive state, reallocate resources.
- **DISCOVER** (every 4 hours): Hunt for entirely new opportunities from alpha pipeline.

## Required Inputs

- **Master Ops xlsx** -- spreadsheet with ALL OPS MASTER sheet (182+ ops), AUTO_STATUS_LIVE (readiness, automation scores, blockers), SYNERGY STACKS (revenue multipliers), VENTURE_AUTOMATION_MAP, PRIORITY LAUNCH rankings
- **Venture performance data** -- state files tracking cycle counts, success rates, last execution times per venture
- **Alpha intelligence** -- alpha staging CSV + intelligence catalog for the strategic briefing
- **Agent swarm reports** -- output from the 25-agent operational swarm (stored as files in a reports directory)
- **Decision logs** -- JSONL audit trail of past decisions for regression detection

## Outputs

- **PROMOTE/KILL decisions** -- structured decision records with: op_id, decision_type, score, reasoning, timestamp
- **Venture scoring** -- per-op scores across 5 dimensions: readiness (0-25), automation (0-25), signal count (0-25), revenue potential (0-15), synergy bonus (0-10)
- **Strategic directives** -- formatted markdown briefs for promoted and enhanced ops, sent to venture agents
- **Audit trail** -- JSONL logs of every decision, every cycle, every score change. Enables regression detection.
- **Checkpoint files** -- atomic JSON checkpoints with phase tracking, enabling crash recovery
- **Git snapshots** -- commits before every decision batch, enabling rollback if regression is detected
- **Status dashboard** -- full system status: cycle count, decisions made, promoted/killed ops, protected ops list, last run timestamps for all pipelines

## Setup

1. **Create the agent state directory:**
   ```
   project/
   ├── AUTOMATIONS/
   │   ├── ceo_agent.py
   │   └── agent/
   │       └── ceo_agent/
   │           ├── ceo_state.json
   │           ├── decisions.jsonl
   │           ├── audit.jsonl
   │           ├── checkpoint.json
   │           └── ceo.lock
   ```

2. **Configure thresholds** at the top of the script:
   - `KILL_THRESHOLD` (default 15) -- ops below this score are eligible for kill
   - `PROTECT_THRESHOLD` (default 60) -- ops above this are protected from kill
   - `PROMOTE_THRESHOLD` (default 70) -- ops above this get doubled down
   - `MAX_CHANGES_PER_CYCLE` (default 5) -- prevents runaway mutations

3. **Set up the Master Ops xlsx** with required sheets: ALL OPS MASTER, AUTO_STATUS_LIVE, SYNERGY STACKS, VENTURE_AUTOMATION_MAP, PRIORITY LAUNCH.

4. **Wire up sub-systems** -- the CEO agent calls the intelligence router, alpha pipeline, venture autonomy engine, loop closer, and system health monitor. Each must be independently functional.

5. **Install as a daemon** (optional):
   ```bash
   python3 ceo_agent.py --daemon  # runs forever, 1-hour cycle interval
   ```
   Or run via cron for periodic execution:
   ```bash
   python3 ceo_agent.py  # single cycle
   ```

## Example Usage

Run a single CEO cycle (full orchestration):
```bash
python3 ceo_agent.py
```

View the full status dashboard:
```bash
python3 ceo_agent.py --status
```

Score all ops without executing decisions:
```bash
python3 ceo_agent.py --score
```

Preview decisions without executing:
```bash
python3 ceo_agent.py --decide
```

Protect a specific op from being killed:
```bash
python3 ceo_agent.py --protect OP_ID
```

Rollback the last CEO change batch:
```bash
python3 ceo_agent.py --rollback
```

Run the alpha pipeline only:
```bash
python3 ceo_agent.py --alpha
```

## Key Patterns

- **Checkpoint-resume** -- the CycleCheckpoint class writes atomic JSON checkpoints at each phase transition. If the process crashes, the next cycle detects the stale checkpoint (older than 2 hours) and resumes from the last completed phase. This prevents lost work and duplicate decisions.
- **Git-based failsafes** -- GitGuard commits all state before every decision batch. If the post-cycle audit detects regression (scores dropping, protected ops damaged), it performs a soft reset to the snapshot hash.
- **Multi-dimensional scoring** -- ops are scored across 5 independent dimensions (readiness, automation level, signal count, revenue potential, synergy bonus) summing to 0-100. This prevents single-factor bias in decisions.
- **Protected ops enforcement** -- ops above the protect threshold or manually protected cannot be auto-killed. This prevents the system from destroying high-value assets during a temporary score dip.
- **Adversarial challenger review** -- the CEOBrain pulls strategic intelligence from the router and intelligence catalog before making decisions. It examines "buried gold" (high-value intelligence not yet monetized) to inform DISCOVER decisions.
- **Regression detection** -- the AuditTrail compares scores across cycles. If a promoted op's score drops significantly, or if a kill decision is followed by negative outcomes, the system flags and can rollback.
- **Lock file concurrency guard** -- a filesystem lock prevents double-runs. If the CEO agent is already running, a second instance exits immediately.
- **Time-gated sub-pipelines** -- expensive operations (research, content generation, discovery) run at configured intervals (4h, 6h, 24h) rather than every cycle. The CEO tracks last-run timestamps in state and skips sub-pipelines that ran recently.
- **Max changes per cycle** -- a hard cap (default 5) prevents runaway mutations where the CEO makes too many decisions in a single pass.

## Limitations

- The VentureScorer requires openpyxl to read xlsx data. Without the master spreadsheet, scoring falls back to minimal defaults.
- Kill decisions are final within a cycle. While rollback is possible, there is no automatic "unkill" mechanism -- killed ops must be manually restored if the decision was wrong.
- The adversarial challenger review relies on the intelligence catalog being current. Stale catalog = stale strategic context.
- City rotation for local business pipeline (OpenClaw) is hardcoded. Adding new cities requires editing the source.
- The 16-phase cycle is sequential. Individual phases cannot be parallelized within a single cycle, though sub-agents can run concurrently.
- Score history retention is capped at 20 snapshots per op. Long-term trend analysis requires exporting to an external store.
- The CEO does not currently factor in financial actuals (revenue, expenses) from the financial tracker. Scoring is based on readiness and signals, not realized revenue.
