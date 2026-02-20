# PRINTMAXX System Architecture
## Unified Reference for ALL Agents (Claude, Codex, Kimi, MiniMax, or any LLM)

**Version:** 1.1.0
**Created:** 2026-02-19
**Last Updated:** 2026-02-19
**Auto-updater:** `python3 AUTOMATIONS/update_system_architecture.py`

---

## 1. System Overview (30-Second Orientation)

PRINTMAXX is an AI-powered solopreneur revenue system that runs 46+ money methods in parallel across 5 niches (tech, faith, fitness, memes, findom). The system uses autonomous agents, 197 automation scripts, and a 3-layer memory architecture to execute research, content generation, lead qualification, and product shipping with minimal human intervention.

**Current state** (from HEARTBEAT.md):
- Leads: 96,200/1,454,245 analyzed | 9,123 hot | 52,491 warm | 230,506 pipeline
- Revenue: $0 total | 2 entries
- Content: 5 CSVs ready | 287 pending QA
- Apps: 6 built | 6/6 live (OPS/DEPLOYMENT_URLS.md)
- Alpha: 417 pending review
- Accounts: 0/48 active (BLOCKER: need platform signups)
- Scripts: 195 automation scripts
- Blocker: Account creation → `OPS/ACCOUNT_CREATION_NOW.md`
- Cron: 226-line crontab (v2), ~56 active jobs

### Architecture Diagram

```
+====================================================================+
|                        PRINTMAXX SYSTEM                            |
+====================================================================+
|                                                                    |
|  SOURCES                     AUTONOMOUS ENGINE                     |
|  --------                    ----------------                      |
|  Twitter (116 accts)  -+                                           |
|  Reddit  (41 subs)    -+-->  SCRAPERS --> ALPHA_STAGING.csv        |
|  Telegram (26 ch)     -+       |              |                    |
|  GitHub MIT repos     -+       |         ALPHA PROCESSOR           |
|  App Store / ASO      -+       |        /      |      \            |
|  Product Hunt         -+       |   APPROVED  BAIT   REJECTED      |
|  HN / RSS feeds       -+       |      |       |                   |
|                                |      v       v                    |
|  MASTER_OPS.xlsx               |   LEDGER/  CONTENT/               |
|       |                        |                                   |
|       v                        |                                   |
|  META_PLANNER -------> TASK_QUEUE.jsonl                            |
|                             |                                      |
|                             v                                      |
|                    AUTONOMOUS SUPERVISOR                            |
|                             |                                      |
|                             v                                      |
|              OPENCLAW HYBRID ENGINE (openclaw_hybrid.py)            |
|              MemoryIntegratedRunner.execute(task)                   |
|                             |                                      |
|                +-- HealthAwareScheduler (pre-flight)                |
|                +-- Pre-task: read heartbeat + active-tasks          |
|                +-- Checkpoint thread (60s daemon)                   |
|                |                                                   |
|                v                                                   |
|           ClosedLoopExecutor                                       |
|            /              \                                        |
|     SCRIPT PATH       LLM PATH                                    |
|    (subprocess +     (gpt-5.3-codex                                |
|     3 retries +       -> Kimi 2.5                                  |
|     error cats)       -> MiniMax)                                  |
|            \              /                                        |
|             EXECUTE + LOG                                          |
|                   |                                                |
|       +-- Post-task: heartbeat + daily log + active-tasks          |
|       +-- AdaptiveRetryEngine -> retry_learnings.jsonl             |
|                   |                                                |
|                   v                                                |
|             MEMORY MANAGER                                         |
|            /      |       \                                        |
|     HEARTBEAT  DAILY LOG  THEMATIC                                 |
|     (<20 lines) (append)  (LEDGER/)                                |
|                                                                    |
|  LEADS (1.45M)                                                     |
|       |                                                            |
|       v                                                            |
|  QUALIFIER (website scoring 0-100)                                 |
|       |                                                            |
|   HOT / WARM                                                      |
|       |                                                            |
|       v                                                            |
|  COLD EMAILS --> PIPELINE TRACKER                                  |
|                                                                    |
+====================================================================+
```

---

## 2. Autonomous Execution Engine

### 2.1 Supervisor Daemon

**File:** `AUTOMATIONS/autonomous_supervisor.py`
**Run:** `caffeinate -s python3 AUTOMATIONS/autonomous_supervisor.py`

Main loop:

```
startup
  --> acquire lock file (.autonomous_supervisor.lock)
  --> load config (AUTONOMOUS_WORKER_CONFIG.yaml)
  --> memory refresh (memory_manager.py --full)
  --> cost cap check (daily_cost.json)
  --> system health check (via HealthAwareScheduler)
  --> daily digest (at 10 PM)
  --> get next task from TASK_QUEUE.jsonl (by priority, dependencies met, PENDING status)
  --> delegate to MemoryIntegratedRunner.execute(task)
  --> log result
  --> loop (poll every 300s)
```

**Execution delegation:** The supervisor no longer calls `run_script_directly()` or `spawn_agent_session()` directly. Instead, it delegates all task execution to `MemoryIntegratedRunner.execute()` from `openclaw_hybrid.py`. The runner handles both script and LLM paths internally, along with pre-flight health checks, crash recovery, adaptive retries, and memory writes.

**Dual execution mode (handled inside MemoryIntegratedRunner):**

| Path | When | How | Cost |
|------|------|-----|------|
| Script path | Task has `execution.type: "script"` | `ClosedLoopExecutor` runs `subprocess.run()` with up to 3 categorized retries | $0 (no LLM) unless fallback triggers |
| LLM path | Task has `execution.type: "llm"` | Prompt sent to `gpt-5.3-codex` -> Kimi -> MiniMax backend chain | Per-token cost |

**Script failure triggers LLM fallback.** If a script exits non-zero and all 3 per-category retry strategies are exhausted, the `ClosedLoopExecutor` escalates to an LLM agent (via the backend chain) to diagnose and fix the issue. This is the core OpenClaw pattern: deterministic first, adaptive retry, intelligent fallback.

**CLI modes:**

| Flag | Action |
|------|--------|
| `--once` | Execute single task and exit |
| `--plan` | Trigger self-planning (generate new tasks) |
| `--status` | Show queue and system status |
| `--dry-run` | Show what would execute, without running |
| `--pipeline <name>` | Run a specific scheduled pipeline |
| `--backends` | Check LLM backend availability |

### 2.2 LLM Backend Chain

**File:** `AUTOMATIONS/llm_backends.py`

Three backends in priority order. Each implements the same interface:
`generate(prompt, timeout_min) -> (return_code, output_text, duration_minutes)`

| Priority | Backend | Auth | Notes |
|----------|---------|------|-------|
| PRIMARY | Codex CLI (`gpt-5.3-codex` model, `full-auto`) | OAuth (free with ChatGPT Pro) | Full agent with tool use |
| FALLBACK 1 | Kimi 2.5 API (Moonshot AI) | API key (`KIMI_API_KEY` env) | OpenAI-compatible, cheap |
| FALLBACK 2 | MiniMax API | API key (`MINIMAX_API_KEY` env) | OpenAI-compatible, fast |

**Claude is NOT in the autonomous chain.** Claude Max is interactive-only and cannot power autonomous loops. Codex OAuth is free and unlimited with ChatGPT Pro. NO CLAUDE in the autonomous execution path.

Return codes: `0` = success, `-1` = timeout, `-2` = not found, `-3` = error.

### 2.3 OpenClaw Hybrid Engine

**File:** `AUTOMATIONS/openclaw_hybrid.py`

The OpenClaw Hybrid Engine is the core execution component that blends battle-tested autonomous patterns with the 3-layer Memento memory system. The supervisor daemon (`autonomous_supervisor.py`) delegates all task execution to `MemoryIntegratedRunner.execute()` rather than calling `run_script_directly()` or `spawn_agent_session()` directly.

**Architecture:** Five classes compose the engine, layered from bottom (error handling) to top (memory-integrated execution):

```
MemoryIntegratedRunner.execute(task)
    |
    +-- HealthAwareScheduler.check_all()     (pre-flight)
    +-- pre_task: read heartbeat + active-tasks (crash recovery)
    +-- start checkpoint thread (60s daemon)
    +-- ClosedLoopExecutor.execute(task)
    |       |
    |       +-- Script path: subprocess.run() with retry loop
    |       |       |
    |       |       +-- categorize_error() -> ErrorCategory
    |       |       +-- AdaptiveRetryEngine.generate_fix()
    |       |       +-- retry (up to 3x per-category strategies)
    |       |       +-- if all retries fail -> LLM fallback
    |       |
    |       +-- LLM path: prompt to gpt-5.3-codex / Kimi / MiniMax
    |
    +-- stop checkpoint thread
    +-- post_task: update heartbeat + daily log + clear active-tasks
```

#### 2.3.1 ClosedLoopExecutor

Script-first execution with error categorization and LLM fallback.

**Error categorization** (6 types, matched via regex on stderr/stdout):

| Category | Trigger Patterns | Example Fix (Attempt 1) |
|----------|-----------------|------------------------|
| `MISSING_DEP` | `ModuleNotFoundError`, `ImportError`, `command not found` | `pip3 install <module>` |
| `API_DOWN` | `ConnectionError`, `503`, `429`, `rate limit` | Wait 30s then retry |
| `BAD_DATA` | `JSONDecodeError`, `KeyError`, `csv.Error`, `malformed` | Retry with `--skip-errors` flag |
| `PERMISSION` | `PermissionError`, `EACCES`, `Errno 13` | `mkdir -p` output dirs |
| `TIMEOUT` | `TimeoutExpired`, `timed out`, `ETIMEDOUT` | Retry with 2x timeout |
| `UNKNOWN` | No pattern match | Blind retry with 1.5x timeout |

**Execution flow:**
1. Run script via `subprocess.run()` (initial attempt)
2. If exit code != 0, scan output for error category
3. Generate per-category fix strategy (up to 3 attempts)
4. Run fix command (prep commands like `pip install` run first, then re-run original)
5. Record success/failure to `retry_learnings.jsonl` for future reference
6. If all 3 retries fail, escalate to LLM fallback (prompt to Codex/Kimi/MiniMax)

#### 2.3.2 AdaptiveRetryEngine

Persists successful fixes to `AUTOMATIONS/logs/retry_learnings.jsonl` so future runs can skip straight to known-good fixes.

**Behavior:**
- On first retry attempt, checks the learnings cache for a previously successful fix matching the same error category and detail string
- If a cached fix exists, applies it immediately (skips generic strategies)
- After each retry (success or failure), writes the outcome to `retry_learnings.jsonl`
- Max 3 retries per error category before LLM fallback

**Per-category retry strategies (escalating):**

| Category | Attempt 1 | Attempt 2 | Attempt 3 |
|----------|-----------|-----------|-----------|
| `MISSING_DEP` | `pip3 install <module>` | Try alternative package name (e.g., `cv2` -> `opencv-python`) | `pip3 install --user --upgrade` |
| `API_DOWN` | Wait 30s + retry | Wait 60s + 2x timeout | Alternative API URL or 3x timeout |
| `BAD_DATA` | Retry with `--skip-errors` | Retry with `--force` | Retry with `STRICT_MODE=0` |
| `PERMISSION` | `mkdir -p` output dirs | Redirect to fallback output path | `chmod -R u+rw` project dir |
| `TIMEOUT` | 2x timeout | `--quick` flag + 3x timeout | 4x timeout + reduced batch/workers |
| `UNKNOWN` | Blind retry 1.5x timeout | Clean environment retry | (exhausted) |

#### 2.3.3 HealthAwareScheduler

Pre-flight checks before any task execution. If a critical check fails (disk space), the task is skipped. Non-critical issues are logged but execution proceeds.

| Check | Threshold | Severity |
|-------|-----------|----------|
| Disk space | Free disk < 1 GB | CRITICAL (task skipped) |
| Stale locks | Any `.lock` file > 2 hours old | WARNING (logged) |
| Heartbeat freshness | `HEARTBEAT.md` modified > 1 hour ago | WARNING (logged) |
| Daily cost cap | `daily_cost.json` total >= $50.00 | WARNING (logged) |

#### 2.3.4 SubAgentSpawner

Spawns focused sub-agents for complex tasks via the LLM backend chain.

Each sub-agent receives:
- **Success criteria** (specific outcome required)
- **Output format** (CSV, JSON, markdown with exact headers)
- **Time budget** (default 15 min)
- **Kill condition** (no file writes in 5 min -> kill and log)
- **Guardrails** (all files within `PROJECT_ROOT`, no destructive commands)

Sub-agents are routed through the same `gpt-5.3-codex -> Kimi -> MiniMax` backend chain. Results are logged to the daily log.

#### 2.3.5 MemoryIntegratedRunner

The top-level runner that wraps `ClosedLoopExecutor` with deep memory coupling. This is the entry point the supervisor calls: `runner.execute(task)`.

**Pre-task phase:**
- Read `HEARTBEAT.md` for system state awareness
- Check `active-tasks.md` for crash recovery (stale entries > 2x estimated time)
- Check daily log for duplicate attempts
- Write to `active-tasks.md` that this task is STARTED

**During-task phase:**
- Daemon checkpoint thread writes progress to `active-tasks.md` every 60 seconds
- If the process crashes, the next agent reads `active-tasks.md` and sees exactly what was running

**Post-task phase:**
- Update `active-tasks.md` (COMPLETED or FAILED)
- Append to today's daily log (`AUTOMATIONS/logs/daily/YYYY-MM-DD.md`)
- Write structured JSONL run log (`AUTOMATIONS/logs/autonomous/runs_YYYY-MM-DD.jsonl`)
- Trigger `memory_manager.py --heartbeat` to refresh system pulse

**CLI modes:**

| Flag | Action |
|------|--------|
| `--task-id <ID>` | Execute a specific task from the queue |
| `--health-check` | Run all 4 pre-flight health checks |
| `--crash-recovery` | Detect and report stale active-task entries |
| `--learnings` | Display retry learnings database (successes/failures) |
| `--categorize-error "<text>"` | Test error categorization against a string |

---

## 3. Memory Architecture (3-Layer "Memento" System)

Every piece of state lives in one of three layers, plus a heartbeat pulse:

```
+------------------------------------------------------------------+
|  HEARTBEAT.md  (<20 lines, pure numbers, 3-second check)         |
+------------------------------------------------------------------+
|                                                                  |
|  LAYER 1: ACTIVE STATE                                           |
|  +---------------------------+  +---------------------------+   |
|  | OPS/HEARTBEAT.md          |  | OPS/active-tasks.md       |   |
|  | System pulse: leads,      |  | Crash recovery: what's    |   |
|  | revenue, apps, alpha,     |  | running NOW. Next agent   |   |
|  | scripts, blockers         |  | reads this and picks up   |   |
|  | Update: every task cycle  |  | Update: every task start  |   |
|  +---------------------------+  +---------------------------+   |
|                                                                  |
|  LAYER 2: DAILY LOGS (append-only)                               |
|  +----------------------------------------------------------+   |
|  | AUTOMATIONS/logs/daily/YYYY-MM-DD.md                      |   |
|  | What happened today. Every script, every tool, every      |   |
|  | pipeline step logs here. End-of-day summary generated.    |   |
|  | Update: continuous (append-only, never overwritten)       |   |
|  +----------------------------------------------------------+   |
|                                                                  |
|  LAYER 3: THEMATIC MEMORY (long-term, survives weeks/months)     |
|  +---------------------------+  +---------------------------+   |
|  | LEDGER/ (CSVs)            |  | AUTOMATIONS/leads/        |   |
|  | ALPHA_STAGING.csv         |  | qualified/HOT_LEADS.csv   |   |
|  | REVENUE_STREAMS.csv       |  | qualified/WARM_LEADS.csv  |   |
|  | CROSS_POLLINATION.csv     |  | PIPELINE_TRACKER.csv      |   |
|  +---------------------------+  +---------------------------+   |
|  +----------------------------------------------------------+   |
|  | Per-venture files: OPS/VENTURE_ALPHA*.md                  |   |
|  | Financial tracking: FINANCIALS/*.csv                      |   |
|  +----------------------------------------------------------+   |
|                                                                  |
+------------------------------------------------------------------+
```

### Memory Manager

**File:** `AUTOMATIONS/memory_manager.py`

| Command | Action |
|---------|--------|
| `--heartbeat` | Rebuild HEARTBEAT.md from live data (leads, revenue, alpha, apps, scripts) |
| `--active-tasks` | Refresh active-tasks.md with current priorities |
| `--daily-summary` | Generate end-of-day summary in daily log |
| `--full` | Update all 3 layers |
| `--log "message"` | Append to today's daily log |
| `--health` | Venture health check across all 7 ventures |

### Crash Recovery Protocol

If an agent dies mid-task:
1. Next agent reads `OPS/active-tasks.md`
2. Sees what was running, which step, what remains
3. Picks up from that exact point

**Every long-running operation MUST:** write to active-tasks.md before starting, update at each step, clear on completion.

---

## 4. Task Queue and Pipeline System

### 4.1 Task Queue

**File:** `OPS/AUTONOMOUS_TASK_QUEUE.jsonl` (JSONL format, one task per line)

**Current state:** 33 tasks (as of 2026-02-19)

**Task schema:**

```json
{
  "id": "AUTO_20260219_research_twitter_scrape",
  "category": "research",
  "priority": 1,
  "risk_level": "LOW",
  "description": "Scrape 116+ high-signal Twitter accounts via Brave cookies",
  "success_criteria": "New tweets extracted, alpha entries appended",
  "estimated_minutes": 30,
  "output_path": "OPS/autonomous_output/2026-02-19/research/",
  "status": "PENDING",
  "created_at": "2026-02-19T17:54:47",
  "dependencies": [],
  "pipeline": "research",
  "execution": {
    "type": "script",
    "script": "twitter_alpha_scraper.py",
    "flags": "--all",
    "command": "python3 AUTOMATIONS/twitter_alpha_scraper.py --all"
  }
}
```

**Status lifecycle:** `PENDING` -> `RUNNING` -> `DONE` | `FAILED` | `BLOCKED`

### 4.2 Workflow Wirer

**File:** `AUTOMATIONS/workflow_wirer.py`

Defines 29 pipelines with 33+ tasks (auto-generated daily). Scans all automation scripts and cron jobs, then generates task queue entries.

| Pipeline | Schedule | Steps | Description |
|----------|----------|-------|-------------|
| `research` | 05:00 | 6 | Twitter scrape, Reddit scrape, research orchestrator, unified alpha, pain points, alpha processing |
| `content` | 08:00 | 1 | Generate tweets + threads from approved alpha (LLM task) |
| `competitor` | 07:00 | 2 | Competitor monitor (19 apps), App Store tracker (36 apps) |
| `leads` | 03:00 | 1 | Closed-loop pipeline (qualify, email, track) |
| `ecom` | 09:00 | 3 | Ecom arb scan, trend scan, trend-to-listing |
| `freelance` | -- | 2 | Freelance demand scan, freelance pipeline |
| `compliance` | 08:45 | 2 | Compliance deadlines, content compliance scan |
| `telegram` | 09:15 | 1 | Telegram community monitor (26 channels) |
| `health` | -- | 2 | System health check, memory refresh |
| `overnight` | 22:00 | 1 | Overnight build (LLM task, picks highest-priority pending) |
| `retrospective` | 22:30 | 1 | Review logs, extract learnings (LLM task) |
| `app_ideation` | -- | 1 | Full trend scan + gap analysis + scoring |
| `venture_tracking` | -- | 1 | Score all methods 0-100, recommend actions |

**CLI:**

| Flag | Action |
|------|--------|
| `--scan` | Show what would be wired |
| `--wire` | Write tasks to queue |
| `--status` | Current wiring status |
| `--daily` | Generate full daily task set |
| `--dry-run` | Preview without writing |

### 4.3 Meta Planner

**File:** `AUTOMATIONS/meta_planner.py`

Reads MASTER_OPS.xlsx (150+ ops, 12 sheets), identifies which ops have automation coverage and which do not, then generates LLM-native tasks for gaps.

| Flag | Action |
|------|--------|
| `--meta-plan` | Full meta plan from MASTER_OPS |
| `--nav-context` | Compact folder navigation for agent prompts |
| `--wire-all` | Wire all unautomated ops into queue |
| `--status` | Coverage report: X/150 ops automated |
| `--gaps` | Show ops with no script coverage |

---

## 5. Configuration

### 5.1 Worker Config

**File:** `OPS/AUTONOMOUS_WORKER_CONFIG.yaml`

| Section | Key Settings |
|---------|-------------|
| **Cost limits** | $5/run cap, $50/day cap |
| **Time limits** | 120 min/run cap, 30 min/task cap |
| **Supervisor** | 300s poll interval, 6h self-plan interval, 1 concurrent run |
| **Schedule** | research 05:00, content AM 08:00, midday 12:00, content PM 17:00, overnight 22:00, retro 22:30 |
| **Backends** | codex (PRIMARY, gpt-5.3-codex, full-auto, OAuth) -> kimi 2.5 -> minimax. NO Claude |
| **Guardrails** | See Section 8 below |
| **Alerts** | Telegram on: task_completed, task_failed, human_needed, cost_warning, agent_timeout, daily_digest, system_health |
| **Git sync** | Every 6h, auto_pull=true, auto_push=false |
| **Task categories** | research (P1), content (P2), analysis (P3), building (P4), maintenance (P5), self_improvement (P6) |
| **Logging** | AUTOMATIONS/logs/autonomous/, 30-day retention, INFO level |

### 5.2 Backend Config

| Setting | Source | Default |
|---------|--------|---------|
| `codex_model` | YAML | `gpt-5.3-codex` |
| `codex_approval_mode` | YAML | `full-auto` |
| `kimi_api_key` | `KIMI_API_KEY` env or YAML | (empty) |
| `kimi_model` | YAML | `kimi-k2-0711-chat` |
| `minimax_api_key` | `MINIMAX_API_KEY` env or YAML | (empty) |
| `minimax_model` | YAML | `MiniMax-Text-01` |

---

## 6. Key Automation Scripts (Top 30)

| # | Script | Purpose |
|---|--------|---------|
| 1 | `autonomous_supervisor.py` | 24/7 daemon: reads queue, delegates to MemoryIntegratedRunner, enforces guardrails |
| 2 | `openclaw_hybrid.py` | OpenClaw Hybrid Engine: ClosedLoopExecutor, AdaptiveRetryEngine, HealthAwareScheduler, SubAgentSpawner, MemoryIntegratedRunner |
| 3 | `llm_backends.py` | Multi-provider LLM router: gpt-5.3-codex -> Kimi 2.5 -> MiniMax |
| 4 | `memory_manager.py` | 3-layer memory: heartbeat + active tasks + daily logs |
| 5 | `workflow_wirer.py` | Generates task queue entries from 12 pipelines, 33+ tasks |
| 6 | `meta_planner.py` | Reads MASTER_OPS.xlsx, identifies gaps, generates tasks |
| 7 | `closed_loop_pipeline.py` | Lead qualification -> cold email -> pipeline tracker loop |
| 8 | `intelligent_lead_qualifier.py` | 2.87M lead qualification with website scoring 0-100 |
| 9 | `twitter_alpha_scraper.py` | Scrape 116+ Twitter accounts via Brave cookies |
| 10 | `background_reddit_scraper.py` | Reddit JSON API scraper across 41 subreddits |
| 11 | `daily_research_orchestrator.py` | Master orchestrator: 5 scrapers + HN + PH, dedup, score 0-100 |
| 12 | `alpha_auto_processor.py` | Route processed alpha to ventures/OPS/cron/archive |
| 13 | `alpha_review_bot.py` | Auto-process PENDING_REVIEW alpha backlog |
| 14 | `generate_cold_emails.py` | Auto-match demos, generate personalized 3-email sequences |
| 15 | `email_sender.py` | SMTP sender with rate limiting and dry-run mode |
| 16 | `website_signal_scorer.py` | Score websites 0-100 on 15 signals (design, SEO, activity) |
| 17 | `ecom_arb_engine.py` | Amazon/eBay price scraping, AliExpress sourcing, profit calc |
| 18 | `trend_aggregator.py` | Google Trends + Reddit + PH viral trend detection |
| 19 | `freelance_demand_scanner.py` | Scan 9 Reddit subreddits for active hiring posts |
| 20 | `system_health_monitor.py` | 14-point health check: GREEN/AMBER/RED per checkpoint |
| 21 | `compliance_scanner.py` | FTC/CAN-SPAM/PII/income claim scanning of all content |
| 22 | `compliance_deadline_tracker.py` | Track 21 regulatory deadlines, RSS scanning |
| 23 | `telegram_community_monitor.py` | Monitor 26 public Telegram channels, 8 niches |
| 24 | `reddit_pain_point_miner.py` | Extract buying intent from 25 subreddits |
| 25 | `unified_alpha_monitor.py` | 350+ sources: Reddit + GitHub MIT + ASO + competitors |
| 26 | `content_multiplier.py` | One piece of content -> multiple platform variants |
| 27 | `refresh_dashboard.py` | Bloomberg-style pipeline dashboard with Chart.js |
| 28 | `personalize_demos.py` | Map 30+ biz categories to 6 templates, generate demos |
| 29 | `venture_performance_tracker.py` | Score all methods 0-100, KILL/MAINTAIN/DOUBLE_DOWN |
| 30 | `daily_agent_runner.py` | Auto-orient any new agent session in 10 seconds |
| 31 | `trend_to_listing.py` | Trend -> POD/Gumroad/Etsy/social listings pipeline |

**Total automation scripts:** 200 Python files in `AUTOMATIONS/`

---

## 7. Data Flow Diagram

### 7.1 Alpha Intelligence Pipeline

```
SOURCES (350+ total)
  Twitter (116 accts, Brave cookies)
  Reddit  (41 subreddits, JSON API)
  Telegram (26 channels, 8 niches)
  GitHub (MIT repos, trending)
  App Store / Product Hunt / HN
      |
      v
SCRAPERS (run daily 05:00-06:30)
  twitter_alpha_scraper.py ----+
  background_reddit_scraper.py-+
  daily_research_orchestrator.py-+-> LEDGER/ALPHA_STAGING.csv
  unified_alpha_monitor.py ----+    (status: PENDING_REVIEW)
  telegram_community_monitor.py+
  reddit_pain_point_miner.py --+
      |
      v
ALPHA PROCESSOR (alpha_auto_processor.py, 06:30)
      |
      +-> APPROVED ---------> Integrate to LEDGER/ + OPS/ + venture files
      +-> ENGAGEMENT_BAIT --> CONTENT/ queue for niche accounts
      +-> REPURPOSE_ONLY ---> Reference material
      +-> REJECTED ---------> Archive
      +-> COMPLIANCE_RISK --> Flag for review
```

### 7.2 Lead Qualification Pipeline

```
RAW LEADS (2.87M from bulk CSV)
      |
      v
PRE-FILTER (intelligent_lead_qualifier.py)
  Deduplicate, domain normalize, industry score
      |
      v
1,454,245 unique domains (PREFILTERED_LEADS.csv)
      |
      v
WEBSITE ANALYSIS (website_signal_scorer.py)
  HTTP + HTML check, design age, SEO, AIO/GIO, activity
  Score 0-100 per site
      |
      v
QUALIFIED LEADS
  HOT (score >= 65):    9,123 --> HOT_LEADS_QUALIFIED.csv
  WARM (score 45-64):  52,491 --> WARM_LEADS_QUALIFIED.csv
  COLD (score < 45):   -----> archive
      |
      v
COLD EMAIL GENERATION (generate_cold_emails.py)
  Match to live demo URLs (surge.sh)
  Personalized 3-email sequences
      |
      v
PIPELINE TRACKER (230,506 in pipeline)
  QUEUED -> SENT -> OPENED -> REPLIED -> BOOKED -> CLOSED
```

### 7.3 Autonomous Execution Flow

```
MASTER_OPS.xlsx (150+ ops, 12 sheets)
      |
      v
META_PLANNER (meta_planner.py)
  Identify unautomated ops, generate tasks
      |
      v
TASK_QUEUE.jsonl (33 tasks, JSONL)
      |
      v
AUTONOMOUS SUPERVISOR (autonomous_supervisor.py)
  Poll every 300s | Check cost caps | Check dependencies
      |
      v
OPENCLAW HYBRID ENGINE (openclaw_hybrid.py)
  MemoryIntegratedRunner.execute(task)
      |
      +-- HEALTH CHECK (HealthAwareScheduler)
      |     Disk >1GB | Stale locks >2h | Heartbeat fresh | Cost <$50
      |
      +-- PRE-TASK: read heartbeat + active-tasks (crash recovery)
      |     Start checkpoint thread (write progress every 60s)
      |
      +-- CLOSED-LOOP EXECUTOR:
      |     |
      |     +-- SCRIPT PATH: subprocess.run() + 3 categorized retries
      |     |     Error categories: MISSING_DEP, API_DOWN, BAD_DATA,
      |     |                       PERMISSION, TIMEOUT, UNKNOWN
      |     |     Cost: $0 | Speed: Fast | Reliability: High
      |     |
      |     +-- LLM PATH: prompt to gpt-5.3-codex / Kimi 2.5 / MiniMax
      |     |     Cost: per-token | Speed: Varies | Capability: Broad
      |     |
      |     +-- FALLBACK: All 3 retries exhausted -> LLM diagnoses + fixes
      |     |
      |     +-- AdaptiveRetryEngine: record outcome to retry_learnings.jsonl
      |
      +-- POST-TASK: update heartbeat + daily log + JSONL run log
      |     Clear active-tasks entry | Stop checkpoint thread
      |
      v
RESULT -> AUTOMATIONS/logs/autonomous/runs_YYYY-MM-DD.jsonl
       -> AUTOMATIONS/logs/daily/YYYY-MM-DD.md
       -> OPS/HEARTBEAT.md (refreshed)
       -> OPS/active-tasks.md (cleared)
       -> Task status: DONE | FAILED
       -> Telegram alert (if configured)
```

---

## 8. Guardrails and Safety

### 8.1 Blocked Actions (NEVER executed by autonomous agents)

```
git push, npm publish, pip publish, payment, stripe, paypal,
account creation, password, credential, ssh-keygen,
rm -rf /, sudo rm, diskutil, mkfs
```

### 8.2 Escalation Triggers (allowed but alert sent)

```
deploy, publish, send email, post to twitter, post to social,
purchase, create account, modify .env, modify SECRETS
```

### 8.3 Path Restrictions

**Allowed write paths:**
```
AUTOMATIONS/, OPS/, LEDGER/, CONTENT/, MONEY_METHODS/,
PRODUCTS/, DIGITAL_PRODUCTS/, builds/, output/, ralph/, scripts/
```

**Protected files (NEVER modified by autonomous agents):**
```
CLAUDE.md, SECRETS/, FINANCIALS/, .env, .claude/rules/,
package.json, package-lock.json
```

### 8.4 Operational Safety

| Safeguard | Mechanism |
|-----------|-----------|
| Cost cap per run | $5.00 max |
| Cost cap daily | $50.00 max |
| Time cap per run | 120 minutes |
| Time cap per task | 30 minutes |
| Lock files | `.autonomous_supervisor.lock` prevents double-runs |
| All operations | Must stay within project root |
| Append-only logs | Logs are never deleted |
| Path validation | Every write checks `PROJECT_ROOT` prefix |
| Backup system | Incremental nightly + full weekly to `~/PRINTMAXX_BACKUPS/` |

---

## 9. Cron Schedule (Current)

**File:** `AUTOMATIONS/crontab_printmaxx_v2.txt` (226 lines, ~56 active jobs)

### Daily Schedule

| Time | Script | Purpose |
|------|--------|---------|
| 01:00 | `perpetual_ship_engine.sh layer1` | Pre-overnight data gathering |
| 02:00 | `overnight_master_runner.sh` | All scrapers + analyzers |
| 03:00 | `closed_loop_pipeline.py --cycles 5` | Lead qualification (10,000 leads/night) |
| 04:00 | `import_sourcing_scanner.py --daily` | Factory sourcing intel |
| 04:30 | `refresh_dashboard.py` | Bloomberg-style dashboard refresh |
| 05:00 | `memory_manager.py --full` | Refresh all memory layers |
| 05:30 | `twitter_alpha_scraper.py --all` | Twitter scrape (116 accounts) |
| 05:45 | `unified_alpha_monitor.py --full` | 350+ source alpha monitor |
| 06:00 | `daily_twitter_scraper.py` | Twitter signal accounts |
| 06:30 | `reddit_pain_point_miner.py --scan` | Reddit buying intent extraction |
| 06:30 | `daily_research_pipeline.py --full` | Scrape -> extract -> filter -> repurpose |
| 07:00 | `competitor_monitor.py --scan` | 19 apps, 6 niches, iTunes API |
| 07:30 | `system_health_monitor.py --check` | 14-point health check |
| 08:00 | `memory_manager.py --heartbeat` | Morning heartbeat update |
| 08:30 | `daily_todo_generator.py` | Generate prioritized daily TODO |
| 08:30 | `compliance_scanner.py --audit-all` | Content compliance scan |
| 08:45 | `compliance_deadline_tracker.py --check` | Regulatory deadline check |
| 09:00 | `daily_agent_runner.py --status` | Session handoff state snapshot |
| 09:15 | `telegram_community_monitor.py --scan` | Telegram signal monitoring |
| 10:00 | `seo_competitor_analyzer.py --summary` | SEO competitor analysis |
| 22:00 | `overnight_master_runner.sh` | Longer builds and features |
| 23:59 | `memory_manager.py --daily-summary` | End-of-day summary |

### Periodic

| Schedule | Script | Purpose |
|----------|--------|---------|
| Every 2h | `ecom_arb_engine.py --scan` | Ecom arb price monitoring |
| Every 3h | `freelance_demand_scanner.py --scan` | Freelance demand scan |
| Every 4h | `trend_aggregator.py --scan` | Trend detection |
| Every 4h | `venture_performance_tracker.py --recommend` | Venture scoring |
| Hourly | `trend_to_listing.py --hourly` | Trend-to-listing pipeline |
| Mon 06:00 | `compliance_deadline_tracker.py --scan` | Weekly regulation scan |
| Mon 06:00 | `trend_scanner.py --full` | Weekly trend deep scan |
| Sun 06:00 | `seo_competitor_analyzer.py --top 50` | Weekly full SEO analysis |

---

## 10. Agent Onboarding (How to Use This Document)

**For any new agent (Claude, Codex, Kimi, MiniMax, or future LLMs):**

### Step 1: Read HEARTBEAT (3 seconds)
```bash
cat OPS/HEARTBEAT.md
```
Pure numbers. Tells you: leads, revenue, apps, alpha, scripts, blockers.

### Step 2: Read Active Tasks (crash recovery)
```bash
cat OPS/active-tasks.md
```
If a previous agent crashed, this tells you what was running and where to pick up.

### Step 3: Read This Document (5 minutes)
You are reading it now. Understand the architecture, memory layers, and execution engine.

### Step 4: Run Memory Manager
```bash
python3 AUTOMATIONS/memory_manager.py --full
```
Refreshes all 3 memory layers with current data.

### Step 5: Check Task Queue
```bash
cat OPS/AUTONOMOUS_TASK_QUEUE.jsonl | python3 -c "import sys,json; [print(json.loads(l).get('id','?'), json.loads(l).get('status','?'), json.loads(l).get('priority','?')) for l in sys.stdin if l.strip()]"
```
Or simply read the file. Look for `PENDING` tasks.

### Step 6: Execute Top Priority
Pick the highest-priority PENDING task with met dependencies. Execute it. Log the result.

### Quick Reference Commands

| Need | Command |
|------|---------|
| System pulse | `cat OPS/HEARTBEAT.md` |
| What's running | `cat OPS/active-tasks.md` |
| Full memory refresh | `python3 AUTOMATIONS/memory_manager.py --full` |
| Auto-orient (10 seconds) | `python3 AUTOMATIONS/daily_agent_runner.py --status` |
| Agent playbook | `cat OPS/AGENT_DAILY_PLAYBOOK.md` |
| Venture health | `python3 AUTOMATIONS/venture_performance_tracker.py --recommend` |
| System health | `python3 AUTOMATIONS/system_health_monitor.py --quick` |
| Pipeline status | `python3 AUTOMATIONS/closed_loop_pipeline.py --status` |
| Copy style rules | `cat .claude/rules/copy-style.md` |

---

## 11. Key File Locations

### Configuration

| File | Purpose |
|------|---------|
| `OPS/AUTONOMOUS_WORKER_CONFIG.yaml` | All tunable settings for the supervisor daemon |
| `OPS/AUTONOMOUS_TASK_QUEUE.jsonl` | Task queue (JSONL, one task per line) |
| `OPS/WORKFLOW_WIRING_REGISTRY.json` | Pipeline wiring registry |
| `AUTOMATIONS/openclaw_hybrid.py` | OpenClaw Hybrid Engine (ClosedLoopExecutor, AdaptiveRetryEngine, HealthAwareScheduler, SubAgentSpawner, MemoryIntegratedRunner) |
| `AUTOMATIONS/crontab_printmaxx_v2.txt` | Cron schedule (226 lines) |
| `.claude/CLAUDE.md` | Claude-specific agent instructions |
| `CODEX.md` | Codex-specific agent instructions |
| `OPS/WORKER_BASE_PROMPT.md` | Base prompt for autonomous worker agents |
| `OPS/SELF_PLANNING_PROMPT.md` | Self-planning prompt for task generation |

### Data (Source of Truth)

| File | Purpose |
|------|---------|
| `LEDGER/ALPHA_STAGING.csv` | All alpha entries (PENDING_REVIEW, APPROVED, etc.) |
| `LEDGER/MEGA_SHEET/` | 10 consolidated CSVs (2,512 rows) |
| `FINANCIALS/REVENUE_TRACKER.csv` | Revenue by method |
| `AUTOMATIONS/leads/qualified/` | HOT, WARM, ANALYZED, PREFILTERED leads |
| `AUTOMATIONS/outreach/PIPELINE_TRACKER.csv` | Cold email pipeline |
| `PRINTMAXX_MASTER_OPS.xlsx` | 150+ ops across 12 sheets |

### Memory

| File | Purpose |
|------|---------|
| `OPS/HEARTBEAT.md` | System pulse (<20 lines) |
| `OPS/active-tasks.md` | Crash recovery (written every 60s by checkpoint thread) |
| `AUTOMATIONS/logs/daily/YYYY-MM-DD.md` | Today's append-only log |
| `AUTOMATIONS/logs/retry_learnings.jsonl` | Adaptive retry learnings (successful fixes persisted for future runs) |
| `AUTOMATIONS/logs/autonomous/runs_YYYY-MM-DD.jsonl` | Structured JSONL run logs from OpenClaw Hybrid Engine |
| `LEDGER/RBI_STRATEGIC/LEARNINGS.jsonl` | Persistent learnings database |

### Outputs

| Directory | Purpose |
|-----------|---------|
| `OPS/autonomous_output/YYYY-MM-DD/` | Daily autonomous run outputs |
| `AUTOMATIONS/logs/autonomous/` | Supervisor logs |
| `CONTENT/social/auto_generated/` | Auto-generated social content |
| `output/` | Dashboard, demos, cold emails |

---

## 12. System Diagram (Complete Data Flow)

```
+===========================================================================+
|                        PRINTMAXX DATA FLOW                                |
+===========================================================================+
|                                                                           |
|  EXTERNAL SOURCES                                                         |
|  +-------+  +-------+  +--------+  +------+  +------+  +---------+      |
|  |Twitter |  |Reddit |  |Telegram|  |GitHub|  |AppSt |  |PH/HN/RS|      |
|  | 116    |  | 41    |  | 26 ch  |  | MIT  |  | ASO  |  | feeds  |      |
|  +---+----+  +---+---+  +---+----+  +--+---+  +--+---+  +----+---+      |
|      |           |           |          |         |            |          |
|      +-----+-----+-----+----+-----+----+----+----+-----+------+          |
|            |                 |                    |                        |
|            v                 v                    v                        |
|  +---------------------+  +---------------------+  +------------------+  |
|  | twitter_alpha        |  | reddit/telegram     |  | unified_alpha   |  |
|  | _scraper.py          |  | scrapers            |  | _monitor.py     |  |
|  +----------+----------+  +----------+----------+  +--------+---------+  |
|             |                        |                       |            |
|             +------------+-----------+------------+----------+            |
|                          |                                                |
|                          v                                                |
|  +-------------------------------------------------------------+        |
|  |  LEDGER/ALPHA_STAGING.csv  (status: PENDING_REVIEW)         |        |
|  +---------------------------+---------------------------------+        |
|                              |                                            |
|                              v                                            |
|  +-------------------------------------------------------------+        |
|  |  alpha_auto_processor.py  (approve / reject / route)        |        |
|  +----+------------+-------------+-------------+---------------+        |
|       |            |             |             |                          |
|       v            v             v             v                          |
|   APPROVED    ENGAGEMENT     REPURPOSE     REJECTED                      |
|       |          BAIT          ONLY            |                          |
|       v            v             |          archive                       |
|   LEDGER/      CONTENT/         |                                        |
|   OPS/         queue            |                                        |
|   ventures                      |                                        |
|                                                                           |
|  MASTER_OPS.xlsx ----> META_PLANNER ----> TASK_QUEUE.jsonl               |
|                                               |                           |
|                                               v                           |
|                                    AUTONOMOUS SUPERVISOR                  |
|                                               |                           |
|                                               v                           |
|                                OPENCLAW HYBRID ENGINE                     |
|                              MemoryIntegratedRunner                       |
|                        (health check -> pre-task memory ->                |
|                         checkpoint thread -> execute ->                    |
|                         post-task memory write)                           |
|                                    /                  \                    |
|                             script path          LLM path                 |
|                          (ClosedLoopExecutor:  (gpt-5.3-codex             |
|                           subprocess + 3       -> Kimi 2.5                |
|                           categorized retries  -> MiniMax)                |
|                           + adaptive learning)                            |
|                                    \                  /                    |
|                                     EXECUTE + LOG                         |
|                                          |                                |
|                           +--------------+--------------+                 |
|                           |              |              |                 |
|                           v              v              v                 |
|                      HEARTBEAT.md    daily log    LEDGER/                 |
|                                                                           |
|  LEADS (1.45M unique) --> QUALIFIER --> HOT/WARM --> COLD EMAILS         |
|                                                          |                |
|                                                          v                |
|                                                   PIPELINE TRACKER       |
|                                                   (230K in pipeline)      |
|                                                                           |
+===========================================================================+
```

---

## 13. Glossary

| Term | Meaning |
|------|---------|
| **Alpha** | Actionable intelligence from external sources (tactics, tools, opportunities) |
| **HEARTBEAT** | <20-line system pulse file with pure numbers |
| **OpenClaw** | Autonomous agent patterns: script-first execution, 6-type error categorization, adaptive retry with learning, LLM fallback, crash recovery. Implemented in `openclaw_hybrid.py` |
| **Pipeline** | Group of scripts that run together in sequence with dependencies |
| **Ralph loop** | `while :; do cat PROMPT.md \| claude --print ; done` autonomous iteration |
| **RBI** | Research-Based Investing pattern applied to money methods |
| **Task Queue** | JSONL file where each line is an executable task for the supervisor |
| **Venture** | A specific money method being actively pursued |
| **Wiring** | Connecting a script to the autonomous task queue so the supervisor can run it |

---

## Appendix A: Project Root Structure

```
PRINTMAXX_STARTER_KITttttt/
  .claude/            Agent config, rules, commands
  01_STRATEGY/        Strategic plans, capital genesis
  AUTOMATIONS/        197 Python scripts, cron, logs
  CONTENT/            Social content, articles, newsletters
  DIGITAL_PRODUCTS/   Gumroad listings, PDFs, micro products
  FINANCIALS/         Revenue, expenses, P&L tracking
  LANDING/            Next.js site (printmaxx-site/)
  LEDGER/             Source of truth CSVs (88 methods)
  MONEY_METHODS/      Playbooks per method (APP_FACTORY, etc.)
  OPS/                Operations, handoffs, checklists, config
  PRODUCTS/           Product listings by platform
  RESEARCH/           Research outputs
  SECRETS/            Credentials (gitignored)
  builds/             Deployed assets, SEO pages
  output/             Dashboard, demos, cold emails
  ralph/              Autonomous loop system
  scripts/            Builder scripts, utilities
```

---

*This document is the single source of truth for system architecture. Any agent reading this should be able to understand the full system in 5 minutes and begin executing tasks immediately.*

*Auto-update: `python3 AUTOMATIONS/update_system_architecture.py`*
