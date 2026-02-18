# PRINTMAXX AUTONOMOUS AGENT SYSTEM — MASTER OPERATIONS DOCUMENT

**Version:** 1.1
**Date:** 2026-02-17 (updated with CODEX.md 2026-02-16 refresh)
**Author:** Claude Opus 4.6 (synthesized from full system analysis)
**Purpose:** Self-looping LLM automation system with intelligent routing, remote worker isolation, and $200/mo budget targeting $30K/mo equivalent output.

---

## TABLE OF CONTENTS

1. [Architecture Overview](#1-architecture-overview)
2. [Node Topology: M1 Control + M2 Worker](#2-node-topology)
3. [Intelligent Model Routing Engine](#3-intelligent-model-routing-engine)
4. [Budget Optimization: $200 → $30K Equivalent](#4-budget-optimization)
5. [Self-Looping Agent Architecture (ClawdBot Model)](#5-self-looping-agent-architecture)
6. [CODEX.md vs CLAUDE.md Analysis + Hybrid System](#6-codex-vs-claude-analysis)
7. [Agent Context Navigation Protocol](#7-agent-context-navigation-protocol)
8. [Existing Ops Integration (All 150+ Ops)](#8-existing-ops-integration)
9. [New Ops Discovery (Deep Research Findings)](#9-new-ops-discovery)
10. [Cron Orchestration & Runtime Loop](#10-cron-orchestration)
11. [Guardrails & Safety Architecture](#11-guardrails-safety)
12. [Implementation Roadmap](#12-implementation-roadmap)

---

## 1. ARCHITECTURE OVERVIEW

```
                    PRINTMAXX AUTONOMOUS AGENT SYSTEM
                    =================================

    [M1 MacBook - CONTROL NODE]              [M2 MacBook - WORKER NODE]
    64GB RAM | Main machine                   16GB RAM | Sandbox
    ================================          ================================
    | Claude Code (Max Plan $100)  |          | Tart VM (Ephemeral)          |
    | - Session orchestrator       |   SSH    | - Agent execution sandbox    |
    | - Approval gates             |--------->| - Cron jobs                  |
    | - Code review                |   Tart   | - Browser automation         |
    | - Strategy decisions         |   Exec   | - Scraper fleet              |
    |                              |          | - Email pipeline             |
    | OpenRouter API Client        |          | - Content generation         |
    | - Kimi K2.5 ($0.50/$2.80)   |          |                              |
    | - MiniMax M2.5 ($0.30/$1.20)|          | Local LLMs (Ollama)          |
    | - DeepSeek V3.2 ($0.24/$0.38|          | - qwen2.5:7b (FREE)         |
    | - DeepSeek R1 (FREE tier)   |          | - llama3.1:8b (FREE)        |
    | - Llama 3.3 70B (FREE tier) |          | - phi4 (FREE)               |
    |                              |          |                              |
    | Codex CLI (ChatGPT $20 sub) |          | ship_captain.py (runtime)    |
    | - codex exec "<prompt>"      |          | stack_governor.py (routing)  |
    | - o4-mini / GPT-5.3-Codex   |          | memory_manager.py (3-layer)  |
    | - Free tier usage            |          | closed_loop_pipeline.py      |
    |                              |          |                              |
    | Meta Vision Audit Corpus     |          | Qwen3-TTS Voice Stack        |
    | - full_context_swarm_dump.py |          | - qwen3_tts_longform.py      |
    | - meta_vision_swarm_audit.py |          | - approved_script_voice.py   |
    | - master_ops_enhancer.py     |          | - Voice render queue         |
    | - master_ops_executor.py     |          | - output/qwen_tts/           |
    ================================          ================================
                |                                          |
                |         [OpenRouter API]                 |
                |         $0.24-$2.80/M tokens             |
                |         30+ models available              |
                +------------------------------------------+
                                    |
                          [HEARTBEAT.md]
                          [active-tasks.md]
                          [LEDGER/*.csv]
                          (Shared filesystem via SSH/rsync)
```

### Core Design Principles

1. **Budget-first routing**: Every LLM call goes through `stack_governor.py` which picks the cheapest model capable of the task
2. **Isolation by default**: Worker node runs inside Tart VM. If it blows up, destroy and recreate in seconds
3. **Self-looping**: Ship captain runs on 30-min cron. Heartbeat checks. Auto-resume on crash via `active-tasks.md`
4. **Human gates only for**: payments, account creation, publishing, compliance, and destructive actions
5. **Portfolio approach**: Run ALL 150+ ops in parallel. Kill losers, double winners. Jane Street model.

---

## 2. NODE TOPOLOGY

### M1 MacBook (Control Node — 64GB RAM)

**Role:** Coding, approvals, supervision, strategy. NEVER executes critical revenue actions.

**What runs here:**
- Claude Code sessions (interactive coding, architecture, review)
- Codex CLI scripted prompts (free tier, high-level reasoning)
- SSH tunnel management to M2
- Approval queue review (`OPS/HUMAN_LOOP_QUEUE.md`)
- Dashboard monitoring (`output/dashboard/index.html`)
- Git operations (commit, push, PR review)

**What does NOT run here:**
- Live email sends
- App deployments
- Browser automation against platforms
- Scraper fleets
- Cron job execution

### M2 MacBook (Worker Node — 16GB RAM)

**Role:** Sandbox execution machine. All live actions happen here.

**What runs here:**
- Tart VM with ephemeral macOS/Linux guest
- Ollama with local models (qwen2.5:7b, llama3.1:8b, phi4)
- Cron fleet (57+ active jobs)
- Ship captain runtime loop
- Browser automation (Playwright, headless Chrome)
- Email pipeline (warmup, sends)
- Scraper fleet (Reddit, Twitter, freelance, ecom)
- Content generation pipeline
- Build/deploy operations (surge.sh, Vercel)

**Isolation Setup (Tart VM):**

```bash
# One-time setup on M2
brew install cirruslabs/cli/tart

# Create ephemeral worker VM
tart create --from-ipsw latest printmaxx-worker
tart run printmaxx-worker &

# SSH into VM from M1
ssh admin@$(tart ip printmaxx-worker)

# For maximum isolation: use tart exec (no network needed)
tart exec printmaxx-worker -- bash -c "cd /path/to/project && python3 AUTOMATIONS/ship_captain.py"

# Destroy and recreate for clean slate
tart delete printmaxx-worker
tart clone printmaxx-base printmaxx-worker
```

**Network Isolation:**
- VM gets its own network namespace
- Only outbound HTTPS allowed (for API calls, deployments)
- No inbound access from internet
- SSH access only from M1's IP

**Filesystem Isolation:**
- Project folder shared via Tart shared directories or rsync
- VM cannot access M1's filesystem
- VM cannot access M2's host filesystem outside shared dir
- Guardrails Python module validates all paths inside VM

### Node Communication Protocol

```
M1 (Control) ----SSH----> M2 (Worker) ----tart exec----> VM (Sandbox)
     |                         |                              |
     | 1. Push task to         | 2. Ship captain picks        | 3. Executes inside
     |    active-tasks.md      |    up task from queue         |    isolated VM
     |                         |                              |
     | 4. Read results from    | 3. Results written to        | 3. Writes to shared
     |    LEDGER/ + output/    |    shared filesystem         |    filesystem
     |                         |                              |
     | 5. Review in            |                              |
     |    HUMAN_LOOP_QUEUE.md  |                              |
```

**Config file:** `OPS/NODE_ROLE.json`
```json
{
  "role": "worker",  // or "control"
  "updated_at": "2026-02-17",
  "notes": "Set via scripts/set_node_role.py"
}
```

---

## 3. INTELLIGENT MODEL ROUTING ENGINE

### The Routing Table

Every LLM call in the system goes through `AUTOMATIONS/stack_governor.py` which reads `OPS/STACK_POLICY.json` and picks the optimal model based on task type and budget.

| Task Type | Model Priority (try in order) | Cost/M Tokens | When to Use |
|-----------|------------------------------|---------------|-------------|
| **Bulk content generation** | Local qwen2.5:7b → DeepSeek V3.2 → MiniMax M2.5 | $0 → $0.24/$0.38 → $0.30/$1.20 | Tweets, social posts, product descriptions, SEO pages |
| **Content quality** | MiniMax M2.5 → Kimi K2.5 → DeepSeek R1 | $0.30/$1.20 → $0.50/$2.80 → $0.55/$2.19 | Newsletter copy, cold emails, landing pages |
| **Code generation** | Codex CLI (free) → Claude Sonnet 4.5 → DeepSeek V3.2 | $0 → $3/$15 → $0.24/$0.38 | Scripts, app code, automation code |
| **Reasoning/strategy** | Codex CLI (free o4-mini) → DeepSeek R1 → Claude Opus 4.6 | $0 → $0.55/$2.19 → $15/$75 | Architecture, business strategy, complex analysis |
| **Visual/multimodal** | Kimi K2.5 → Claude Sonnet 4.5 | $0.50/$2.80 → $3/$15 | Screenshot analysis, UI review, image-based tasks |
| **Long context (>100K)** | Kimi K2.5 (262K) → MiniMax M1 (1M) | $0.50/$2.80 → $0.43/$1.93 | Full codebase review, massive document analysis |
| **Prototyping/testing** | DeepSeek R1 FREE → Llama 3.3 FREE → DeepSeek V3.1 FREE | $0 | Testing pipelines, prompt iteration, dry runs |

### Model Pricing Reference (Feb 2026)

| Model | Provider | Input $/M | Output $/M | Context | Best For |
|-------|----------|-----------|------------|---------|----------|
| **qwen2.5:7b** | Local (Ollama) | $0 | $0 | 32K | Bulk transforms, simple tasks |
| **llama3.1:8b** | Local (Ollama) | $0 | $0 | 128K | Classification, formatting |
| **phi4** | Local (Ollama) | $0 | $0 | 16K | Quick reasoning |
| **DeepSeek V3.2** | OpenRouter | $0.24 | $0.38 | 128K | Best price/quality ratio |
| **DeepSeek R1** | OpenRouter FREE | $0 | $0 | 128K | Reasoning (free tier) |
| **DeepSeek V3.1** | OpenRouter FREE | $0 | $0 | 128K | Chat (free tier) |
| **Llama 3.3 70B** | OpenRouter FREE | $0 | $0 | 128K | General (free tier) |
| **MiniMax M2.5** | OpenRouter | $0.30 | $1.20 | 204K | Cheapest frontier model |
| **Kimi K2.5** | OpenRouter | $0.50 | $2.80 | 262K | Visual coding, multimodal |
| **MiniMax M1** | OpenRouter | $0.43 | $1.93 | 1M | Ultra-long context |
| **Claude Sonnet 4.5** | Anthropic | $3 | $15 | 200K | Premium code generation |
| **Claude Opus 4.6** | Claude Max sub | included | included | 200K | Strategy, complex reasoning |
| **Codex CLI (o4-mini)** | ChatGPT $20 sub | $0* | $0* | varies | Code tasks (free with sub) |

*Free with ChatGPT subscription, subject to rolling 5-hour window limits.

### Routing Logic (stack_governor.py)

```python
def route_task(task_type: str, complexity: int, budget_remaining: float) -> str:
    """Pick cheapest model that can handle the task."""

    # Always try free/local first
    if task_type in ["bulk_content", "formatting", "classification"]:
        if ollama_available():
            return "local:qwen2.5:7b"

    # Free OpenRouter tier for prototyping
    if task_type == "prototype" or budget_remaining < 5.0:
        return "openrouter:deepseek/deepseek-r1:free"

    # Budget routing
    if task_type == "content_generation":
        if complexity < 3:
            return "openrouter:deepseek/deepseek-chat-v3.2"  # $0.24/$0.38
        elif complexity < 7:
            return "openrouter:minimax/minimax-m2.5"  # $0.30/$1.20
        else:
            return "openrouter:moonshotai/kimi-k2.5"  # $0.50/$2.80

    if task_type == "code_generation":
        # Try Codex CLI first (free with ChatGPT sub)
        if codex_cli_available() and within_rate_limit():
            return "codex:o4-mini"
        return "openrouter:deepseek/deepseek-chat-v3.2"

    if task_type == "reasoning":
        if codex_cli_available():
            return "codex:o4-mini"
        return "openrouter:deepseek/deepseek-r1"

    if task_type == "visual":
        return "openrouter:moonshotai/kimi-k2.5"

    # Fallback
    return "openrouter:deepseek/deepseek-chat-v3.2"
```

### Codex CLI Integration (Free Tier Strategy)

The ChatGPT $20 subscription includes Codex CLI access. This is the legitimate way to script prompts against your subscription.

```bash
# Non-interactive scripted prompt
codex exec "Analyze this CSV and suggest top 5 optimization targets" < data.csv

# Pipe output to file
codex exec "Generate 10 cold email subject lines for dental practices" > subjects.txt

# JSON output for script consumption
codex exec --json "Rate these app names 1-10 for the fitness niche" | jq '.rating'

# Check remaining usage in rolling window
codex exec "/status"
```

**Rate limit strategy:**
- 5-hour rolling window shared between local and cloud tasks
- Use for HIGH-VALUE tasks only (complex reasoning, code architecture)
- A single prompt can consume ~7% of weekly Plus tier limits
- Batch similar requests into single prompts
- Reserve for tasks where DeepSeek/Kimi quality isn't sufficient

**Cron integration:**
```bash
# 6 AM - Use Codex for daily strategic analysis
0 6 * * * cd $BASE && codex exec "$(cat OPS/DAILY_STRATEGIC_PROMPT.md)" > OPS/DAILY_STRATEGY_$(date +%Y_%m_%d).md 2>/dev/null || echo "Codex limit hit, skipping"

# Fallback: if Codex fails (rate limited), use DeepSeek R1
0 6 * * * cd $BASE && python3 AUTOMATIONS/daily_strategic_analysis.py --model deepseek-r1
```

---

## 4. BUDGET OPTIMIZATION: $200 → $30K EQUIVALENT

### Budget Allocation

| Category | Monthly Budget | What You Get | Equivalent API Cost |
|----------|---------------|--------------|---------------------|
| **Claude Max plan** | $100/mo | 240-480h Sonnet + 24-40h Opus per week | ~$8,000-$15,000 |
| **ChatGPT Plus** | $20/mo | Codex CLI free tier + 150 GPT-4o msgs/3h | ~$2,000-$4,000 |
| **OpenRouter API** | $80/mo | ~100M tokens at DeepSeek V3.2 rates | ~$3,000-$5,000 |
| **Local models (Ollama)** | $0/mo | Unlimited qwen2.5:7b + llama3.1:8b | ~$2,000-$3,000 |
| **Free tiers** | $0/mo | DeepSeek R1 + Llama 3.3 + DeepSeek V3.1 | ~$1,000-$2,000 |
| **TOTAL** | **$200/mo** | | **~$16,000-$29,000** |

### Token Math

At $80/mo on OpenRouter with weighted model usage:

| Model | % of Budget | Monthly Spend | Tokens Generated |
|-------|-------------|---------------|------------------|
| DeepSeek V3.2 | 40% | $32 | ~84M input + 84M output |
| MiniMax M2.5 | 25% | $20 | ~44M input + 16M output |
| DeepSeek R1 (free) | 15% | $0 (+ $12 paid) | ~22M input + 7M output |
| Kimi K2.5 | 10% | $8 | ~16M input + 3M output |
| Free tiers | 10% | $0 (+ $8 overflow) | ~20M+ tokens |

**Conservative estimate:** 250M+ tokens/month from API alone, plus unlimited local and Claude Max usage.

### Maximizing Claude Max ($100/mo)

Claude Max gives 240-480h of Sonnet and 24-40h of Opus per week. At max usage:

- **Sonnet hours:** 480h/week x 4 weeks = 1,920 hours/month
- **Opus hours:** 40h/week x 4 weeks = 160 hours/month
- Use Claude Code in `--print` mode for batch operations (Ralph loops)
- Use `--dangerously-skip-permissions` for autonomous overnight runs

**Key insight:** Claude Max is the single most cost-effective resource. Maximize usage of weekly Sonnet/Opus hours through Ralph loops and parallel subagents.

### Cost Optimization Tactics

1. **Local first, always:** Run qwen2.5:7b for all classification, formatting, simple transforms
2. **Free tiers for prototyping:** Use DeepSeek R1 free tier for testing prompts before spending on paid models
3. **Batch operations:** Combine 10 small tasks into 1 large prompt (saves per-request overhead)
4. **Cache system prompts:** Kimi K2.5 cached input is only $0.10/M (vs $0.50/M uncached) — reuse system prompts
5. **Output minimization:** Configure models to return minimal JSON/CSV, not verbose explanations
6. **Context window management:** Use 7B local for tasks under 32K tokens, save 262K Kimi for when you need it
7. **Codex CLI for premium tasks:** Free o4-mini reasoning for complex analysis, saves $50+/mo in API costs
8. **Weekly quota tracking:** Script that monitors OpenRouter spend and pauses non-critical tasks when approaching soft cap

---

## 5. SELF-LOOPING AGENT ARCHITECTURE (ClawdBot Model)

### What OpenClaw/ClawdBot Does (and what we replicate)

OpenClaw (147K GitHub stars) is a self-looping autonomous agent with:
- Background daemon with heartbeat loop (every 30 min)
- Persistent markdown memory on disk
- Messaging platform as UI (WhatsApp, Telegram, Slack)
- MIT-licensed, local-first
- Skills ecosystem (5,705+ community skills)

**Our system replicates this pattern using existing PRINTMAXX infrastructure:**

### The PRINTMAXX Loop (OpenClaw-equivalent)

```
                    PRINTMAXX AUTONOMOUS LOOP
                    =========================

    +-----------+     +-----------+     +-----------+
    | HEARTBEAT |---->| SHIP      |---->| EXECUTE   |
    | CHECK     |     | CAPTAIN   |     | TASKS     |
    | (30 min)  |     | (router)  |     | (workers) |
    +-----------+     +-----------+     +-----------+
         ^                                    |
         |            +-----------+           |
         +------------| MEMORY    |<----------+
                      | UPDATE    |
                      | (3-layer) |
                      +-----------+
```

**Layer 1: Heartbeat (every 30 min)**
```bash
# crontab entry
*/30 * * * * cd $BASE && python3 AUTOMATIONS/ship_captain.py --tick
```

Ship captain reads:
1. `OPS/HEARTBEAT.md` — system pulse (<20 lines)
2. `OPS/active-tasks.md` — crash recovery (what was running)
3. `OPS/HUMAN_LOOP_QUEUE.md` — pending approvals
4. `OPS/HUMAN_APPROVALS.csv` — approved actions

**Layer 2: Task Router (ship_captain.py)**
```python
def tick():
    """Single iteration of the autonomous loop."""
    # 1. Read system state
    heartbeat = read_heartbeat()
    active = read_active_tasks()
    approvals = read_approvals()

    # 2. Check for crashed tasks (resume)
    if active.has_interrupted_tasks():
        resume_task(active.latest_interrupted)
        return

    # 3. Check approval queue
    if approvals.has_new_approvals():
        execute_approved(approvals.latest)
        return

    # 4. Route to highest-priority lane
    lanes = load_lane_config()  # from CLAWWORK_SIDECAR_POLICY.json
    for lane in sorted(lanes, key=lambda l: l.priority, reverse=True):
        if lane.has_work() and not lane.is_blocked():
            execute_lane(lane, max_tasks=3)
            break

    # 5. Update memory
    update_heartbeat()
    update_active_tasks()
    log_daily(f"tick complete at {now()}")
```

**Layer 3: Lane Workers**

Each "lane" is an automation pipeline (from CLAWWORK_SIDECAR_POLICY.json):

| Lane | Priority | Win Rate | Value/Win | Blocker |
|------|----------|----------|-----------|---------|
| freelance_arbitrage | 100 | 8% | $225 | FIVERR_UPWORK_ACCOUNT |
| gumroad_listings | 95 | 22% | $19 | GUMROAD_ACCOUNT |
| cold_outreach_warmup | 90 | 2% | $300 | EMAIL_INFRA |
| rbi_intent_sniping | 80 | 3% | $180 | X_MULTI_ACCOUNT_STACK |

**Layer 4: Memory Architecture (3-layer OpenClaw pattern)**

| Layer | File | Update Freq | Purpose |
|-------|------|-------------|---------|
| Pulse | `OPS/HEARTBEAT.md` | Every tick | <20 lines, pure numbers |
| Crash Recovery | `OPS/active-tasks.md` | Every task start/end | What's running NOW |
| Transaction Log | `AUTOMATIONS/logs/daily/YYYY-MM-DD.md` | Continuous | Append-only daily log |

### Ralph Loop Integration

Ralph loops are the autonomous Claude Code iteration system. They complement the ship captain by handling complex, multi-step work:

```bash
# Ralph loop (overnight autonomous work)
while :; do
  cat PROMPT.md | claude --dangerously-skip-permissions --print

  # Check for completion
  if grep -q "COMPLETE" progress.txt; then
    break
  fi

  sleep 2
done
```

**Ralph Loop Factory:** `AUTOMATIONS/ralph_loop_factory.py` (947 lines) generates loop configurations for ANY of the 150+ ops.

**Parallel Ralph Execution:**
```bash
# Launch 5 concurrent ralph loops on different ops
for loop in s02 s03 s04 c01 e03; do
  cd ralph/loops/$loop && bash run.sh &
done
```

### ClawWork Sidecar (Autonomous Evaluation Agent)

The ClawWork sidecar evaluates which lanes to prioritize based on expected value:

```
Expected Value per Run = Win Rate x Value per Win x Quality Factor
```

| Lane | EV/Run | Monthly Runs | Monthly EV |
|------|--------|-------------|------------|
| freelance_arbitrage | $225 x 0.08 x 0.75 = $13.50 | 720 | $9,720 |
| gumroad_listings | $19 x 0.22 x 0.90 = $3.76 | 720 | $2,710 |
| cold_outreach | $300 x 0.02 x 0.70 = $4.20 | 720 | $3,024 |
| rbi_intent | $180 x 0.03 x 0.70 = $3.78 | 720 | $2,722 |

**Total monthly EV (if all lanes unblocked):** ~$18,176

---

## 6. CODEX.md vs CLAUDE.md ANALYSIS + HYBRID SYSTEM

### CODEX.md (Lean, Control/Worker, Ship Captain) — 2026-02-16 Refresh

**Strengths:**
- Clean ~150-line contract. Agent reads it in 10 seconds.
- Explicit node role separation (control vs worker)
- Clear guardrails hierarchy (human approval gates)
- Budget-first routing via STACK_POLICY.json
- Structured agent navigation order (7 levels, expanded in Feb 16 refresh)
- Swarm audit commands for system maintenance
- **NEW: Operator intent defaults** — universal expansion, `etc` adjacency expansion, execute-first behavior, no hand-holding mode, portfolio expansion
- **NEW: ClawWork sidecar controls** — lane evaluation, sidecar run tracking, minimal sidecar plan
- **NEW: Local Qwen3-TTS voice stack** — longform rendering, approved script queue, voice render runs ledger
- **NEW: Full-context audit corpus** — Meta Vision docs, file inventory CSV, swarm dump/audit tools
- **NEW: Master Ops intelligent execution layer** — enhancer + executor scripts, 7 enhanced sheets driving automation (PRIORITY_AUTOMATION_EXEC, ETC_EXPANSION_QUEUE, DEEP_PLAYBOOK_INDEX, ALPHA_THESIS_INDEX, VENTURE_AUTOMATION_MAP)
- **NEW: Secure minimal cron** — hardened crontab + installer script

**Weaknesses:**
- No institutional memory (no session logs, no nav maps)
- No proactive execution directives (relies on operator intent defaults instead)
- Doesn't encode the "ship now, plan later" philosophy directly
- Missing all the operational playbooks and asset locations
- Assumes agent already knows the codebase

**Best for:** Codex CLI (which has limited context and needs concise instructions), ship_captain.py autonomous loops, and any short-context model agent

### CLAUDE.md (Comprehensive, Ralph Loops, 3-Layer Memory)

**Strengths:**
- Massive institutional memory (200+ "Where is..." entries, 100+ "I want to..." routes)
- Session logs dating back weeks (continuity between agents)
- Encoded execution philosophy ("ship now", "no AI slop", factory mode)
- Copy style enforcement with weighted voice system
- Detailed financial tracking integration
- Browser automation fallback chains
- Compliance and safety protocols

**Weaknesses:**
- Massive size causes context pressure (thousands of lines)
- Repetitive directives (same instruction stated 5+ ways)
- Historical cruft (status from weeks ago still in file)
- Session logs consume context without aiding new tasks
- "Never stop building" conflicts with quality gates

**Best for:** Claude Code (which has large context and benefits from comprehensive memory)

### HYBRID SYSTEM: Dual-Layer Agent Contract

The optimal system uses BOTH approaches:

```
AGENT ENTRY POINT
=================

Codex CLI / OpenCode / Short-context models:
  → Read CODEX.md (151 lines, 10-second orientation)
  → Read OPS/HUMAN_LOOP_QUEUE.md (blockers)
  → Read OPS/HEARTBEAT.md (system pulse)
  → Execute via STACK_POLICY.json routing

Claude Code / Long-context sessions:
  → Read CODEX.md FIRST (contract)
  → Read .claude/CLAUDE.md (deep memory)
  → Read OPS/PERSISTENT_TASK_TRACKER.md (all tasks)
  → Full execution with institutional memory

Ship Captain (autonomous loop):
  → Read CODEX.md only (lean contract)
  → Read STACK_POLICY.json (routing)
  → Read active-tasks.md (crash recovery)
  → Execute lanes per CLAWWORK_SIDECAR_POLICY.json
```

**Key innovation:** CODEX.md is the ALWAYS-READ contract. CLAUDE.md is the DEEP-DIVE memory. No agent reads CLAUDE.md without first reading CODEX.md. This keeps lean agents fast while giving rich agents full context.

### CODEX.md Operator Intent Defaults (Critical for Agent Behavior)

The Feb 16 refresh added persistent operator intent defaults that ALL agents must follow:

1. **Universal expansion default**: Every task expands to maximum aligned execution set. Explicit examples are minimum scope, not final scope.
2. **`etc` adjacency expansion**: When examples are given (e.g. "eBay, Etsy, Redbubble"), treat as seed set and auto-expand to full comparable opportunity surface.
3. **Execute-first behavior**: Default to implementation, not instructions. Only pause for compliance, payment, KYC, or destructive actions.
4. **No hand-holding mode**: Infer obvious next steps. If blocked, create unblock artifacts and keep other lanes running.
5. **Portfolio expansion**: Continuously scan for additional monetizable channels. Maintain an "opportunity frontier" list.
6. **Master Ops `etc` execution**: Treat the enhanced spreadsheet as a live expansion surface. Update `ETC_EXPANSION_QUEUE` on each enhancement run.

These defaults are the CODEX equivalent of CLAUDE.md's "ship now, factory mode, above and beyond" directives — but encoded as lean rules rather than paragraphs.

### Recommended CODEX.md Updates (Still Pending)

Add to CODEX.md:
1. Model routing table (which model for which task type)
2. OpenRouter API endpoint and key location
3. M2 worker SSH connection details
4. Tart VM management commands

### Recommended CLAUDE.md Cleanup

Reduce CLAUDE.md by:
1. Move session logs older than 7 days to `OPS/SESSION_ARCHIVE/`
2. Deduplicate repeated directives (ship now, factory mode, etc.) into single canonical versions
3. Move "Where is..." table to `OPS/NAV_MAP.md` (referenced from CLAUDE.md, not inline)
4. Move copy-style rules to `.claude/rules/copy-style.md` (already exists, remove inline version)

---

## 7. AGENT CONTEXT NAVIGATION PROTOCOL

### For ANY Agent Entering the System

This matches CODEX.md's Agent Navigation (2026-02-16 Refresh) with added context for each level:

```
LEVEL 0: IDENTITY (1 second)
  Read: OPS/NODE_ROLE.json
  → Am I control or worker?

LEVEL 1: CONTRACT (10 seconds)
  Read: CODEX.md
  → Guardrails, routing, operator intent defaults, non-negotiables

LEVEL 2: GATES & BLOCKERS (10 seconds)
  Read: OPS/HUMAN_LOOP_QUEUE.md
  Read: OPS/HUMAN_APPROVALS.csv
  Read: OPS/NODE_ROLE.json
  → What's approved? What's blocked? What actions can this node take?

LEVEL 3: RUNTIME HEALTH (5 seconds)
  Read: OPS/STACK_HEARTBEAT.md
  Read: OPS/HUMAN_EXECUTION_BRIEF.md
  Read: output/cron_fleet/latest.md
  → System pulse, what's running, lane outputs

LEVEL 4: CLAWWORK SIDECAR (10 seconds)
  Read: OPS/CLAWWORK_SIDECAR_POLICY.json
  Read: OPS/CLAWWORK_MINIMAL_SIDECAR_PLAN.md
  Read: output/clawwork_sidecar/latest.md
  Read: LEDGER/CLAWWORK_SIDECAR_RUNS.csv
  → Lane evaluation, expected value, run history

LEVEL 5: LOCAL VOICE STACK — Qwen3-TTS (5 seconds, if voice tasks queued)
  Read: OPS/QWEN3_TTS_LOCAL_STACK.md
  Read: OPS/VOICEOVER_APPROVED_QUEUE.csv
  Read: LEDGER/VOICE_RENDER_RUNS.csv
  → Approved scripts, render queue, output at output/qwen_tts/
  Execute: bash scripts/approved_voice_runner.sh --max-jobs 2

LEVEL 6: AUDIT CORPUS + META VISION (30 seconds, for audit/synthesis tasks only)
  Read: AUDIT/META_VISION.md (historical baseline)
  Read: AUDIT/META_VISION_2026_02_16.md (swarm metrics sweep)
  Read: AUDIT/META_VISION_2026_02_17_AUTOMATION.md (automation upgrade pass)
  Read: AUDIT/META_VISION_FULL_CONTEXT_2026_02_16.md (raw-corpus-linked)
  Read: AUDIT/META_VISION_2026_02_16_FILE_INVENTORY.csv (full file/folder inventory)
  → System-wide audit state, file inventory, cross-document patterns

LEVEL 7: MASTER OPS EXECUTION LAYER (varies)
  Read: PRINTMAXX_MASTER_OPS_ENHANCED_2026-02-17.xlsx (or extracted CSVs)
  Execute: python3 AUTOMATIONS/master_ops_executor.py --top 12 --max-per-lane 3
  → Prioritized ops from enhanced sheets:
    PRIORITY_AUTOMATION_EXEC, ETC_EXPANSION_QUEUE,
    DEEP_PLAYBOOK_INDEX, ALPHA_THESIS_INDEX, VENTURE_AUTOMATION_MAP

LEVEL 8: DEEP MEMORY (30 seconds, Claude Code only)
  Read: .claude/CLAUDE.md
  → Full institutional context, nav maps, session history

LEVEL 9: TASK ROUTING (10 seconds)
  Read: OPS/PERSISTENT_TASK_TRACKER.md
  Read: OPS/active-tasks.md (crash recovery)
  → What needs doing? Was something interrupted? Resume it.
```

**Agent type determines max level:**

| Agent Type | Max Level | Skip Levels |
|------------|-----------|-------------|
| ship_captain.py (cron) | 4 | 5, 6, 8 |
| Ralph loop (autonomous) | 7 | 5, 6, 8 |
| Codex CLI (scripted) | 4 | 5, 6, 7, 8 |
| Local qwen2.5:7b | 2 | 3-8 |
| Voice sidecar | 5 | 3, 4, 6, 7, 8 |
| Claude Code (interactive) | 9 | none |
| Swarm audit agent | 6 | 5, 7, 8 |
| Master ops executor | 7 | 5, 6, 8 |

### Context Budget Strategy

| Agent Type | Context Budget | Strategy |
|------------|---------------|----------|
| Codex CLI | ~128K tokens | CODEX.md + HEARTBEAT + specific task file only |
| Local qwen2.5:7b | 32K tokens | Single task prompt + CSV data only |
| DeepSeek V3.2 | 128K tokens | CODEX.md + lane-specific files + output template |
| Kimi K2.5 | 262K tokens | Full codebase review, visual analysis |
| MiniMax M1 | 1M tokens | Entire project in context (for audit/synthesis) |
| Claude Code | 200K tokens | Full CLAUDE.md + CODEX.md + task files |

**Rule:** Never feed a cheap model more context than it needs. CODEX.md for orientation. Task-specific files for execution. CLAUDE.md only for Claude Code sessions.

---

## 8. EXISTING OPS INTEGRATION (ALL 150+ OPS)

### By Automation Lane (from VENTURE_AUTOMATION_MAP)

**PRIORITY LAUNCH (17 ventures, ready to execute):**

| ID | Venture | Lane | Score | Signal Count | Command |
|----|---------|------|-------|--------------|---------|
| C01 | TikTok Content Farm | rbi_intent_sniping | 67 | 487 | `python3 AUTOMATIONS/clawdbot_rbi_engine.py --tick` |
| S01 | Freelance Arbitrage | freelance_arbitrage | 55 | 109 | `python3 AUTOMATIONS/freelance_demand_scanner.py --hourly` |
| N68 | Ramadan PWA | app_factory | 48 | 15 | `python3 AUTOMATIONS/app_packager.py --write` |
| P11 | CashApp/Crypto Bio | app_factory | 48 | 15 | `python3 AUTOMATIONS/app_packager.py --write` |
| D01 | Gumroad Portfolio | gumroad_listings | 47 | 5 | `python3 AUTOMATIONS/gumroad_autolist_packager.py --write` |
| S05 | Bland AI Voice | cold_outreach | 43 | 339 | `python3 AUTOMATIONS/email_sender.py --preview` |
| C12 | Email Sequence Machine | cold_outreach | 43 | 339 | `python3 AUTOMATIONS/email_sender.py --preview` |

**LLM ALPHA THESIS (37 opportunities with edge duration 6-48 months):**

Top opportunities by edge duration:
1. App factory (24-36 month window)
2. Cold email personalization (18-36 months)
3. Ecomm product scouting (12-24 months)
4. Micro-SaaS portfolio (24-36 months)
5. AI companion apps (24-36 months)

**SYNERGY STACKS (26 packages with 3.8x-8.7x revenue multipliers):**

Top 5 synergies:
1. Portfolio Apps + Paywall Optimization: 8.7x multiplier
2. AI Findom Multiplatform: 8.0x
3. Course + Community + AI Expert: 7.5x
4. Content Arbitrage Engine: 6.5x (one piece → 5 platforms → 50 revenue events/day)
5. Freelance + Productized Service: 5.2x

### Human Blockers (9 pending approvals)

| Blocker Key | Blocks | How to Unblock |
|-------------|--------|---------------|
| X_MULTI_ACCOUNT_STACK | TikTok Farm, SEO content, X growth | Create X accounts, warmup 3-5 days |
| FIVERR_UPWORK_ACCOUNT | Freelance arbitrage | Create accounts per OPS/FIVERR_LAUNCH_CHECKLIST.md |
| STORE_ACCOUNT_AND_PAYMENT | Ramadan PWA, CashApp Bio | Apple dev account + Stripe |
| GUMROAD_ACCOUNT | Gumroad portfolio, Notion products | 10-min signup at gumroad.com |
| EMAIL_INFRA | Bland AI, Email sequences | Domain + warmup + CAN-SPAM setup |

---

## 9. NEW OPS DISCOVERY (DEEP RESEARCH FINDINGS)

### New Ops NOT Already in the System

These were identified through deep research and cross-referencing against ALL 150+ existing ops:

**TIER 1: High-Confidence, Immediate Revenue Potential**

| # | Op | Revenue Model | Monthly Potential | Why It's Missing |
|---|-----|--------------|-------------------|-----------------|
| 1 | **OpenRouter Model Arbitrage** | Resell cheap API access with markup | $500-$5K | Direct API resale - buy at $0.24/M, sell at $1/M via wrapper |
| 2 | **CrewAI/AutoGPT Agent-as-a-Service** | Build and sell autonomous agents | $2K-$15K | AI agent services exist but not framed as CrewAI builds |
| 3 | **Codex CLI Automation Consulting** | Sell Codex CLI automation setups | $1K-$5K | New tool (Feb 2026), first-mover window |
| 4 | **Tart VM Sandbox-as-a-Service** | Sell isolated dev environments | $500-$3K | Apple Silicon VM management for agencies |
| 5 | **OpenClaw Skill Development** | Build and sell OpenClaw skills on ClawHub | $200-$2K | 5,705 skills in registry, marketplace growing |
| 6 | **LLM Router/Gateway SaaS** | Build OpenRouter-like routing for enterprises | $2K-$20K | Enterprises need multi-model routing |

**TIER 2: Medium-Confidence, Requires Testing**

| # | Op | Revenue Model | Monthly Potential | Edge |
|---|-----|--------------|-------------------|------|
| 7 | **AI Voice Cloning Narration** | Audiobook/podcast narration service | $1K-$8K | Qwen3-TTS local stack BUILT + approved queue + voice sidecar cron |
| 8 | **Ephemeral VM Testing Farms** | Sell clean browser environments for testers | $500-$3K | Tart VMs + Dolphin Anty infrastructure |
| 9 | **MCP Server Development** | Build Model Context Protocol servers | $2K-$10K | 13-day window already elapsed, still early |
| 10 | **AI Compliance Audit Service** | Scan content for FTC/CAN-SPAM violations | $1K-$5K | compliance_scanner.py already built |
| 11 | **Programmatic SEO Factory** | Generate 600+ page sites for local keywords | $500-$3K | programmatic_seo.py already built, needs Vercel migration |
| 12 | **Ralph Loop Templates Marketplace** | Sell pre-built autonomous loop configs | $200-$1K | Unique IP, ralph_loop_factory.py exists |

**TIER 3: Experimental/Long-Shot**

| # | Op | Revenue Model | Why Interesting |
|---|-----|--------------|-----------------|
| 13 | **AI Agent Benchmark Testing** | Test and rank AI agents for enterprises | Growing market, SWE-bench model |
| 14 | **Cross-Model Prompt Optimization** | Optimize prompts across models for clients | Deep knowledge of model-specific strengths |
| 15 | **Autonomous Market Making (Prediction Markets)** | Bot-driven Polymarket/Kalshi trading | prediction_market_arb_playbook.md exists |
| 16 | **AI-Generated Course Factory** | Mass-produce niche courses via CrewAI pipelines | info_product_ops_strategy.md exists |
| 17 | **Browser Fingerprint Testing Service** | Test anti-detect browser effectiveness | PROXY_ANTIDETECT_VPN_WIRING_GUIDE.md exists |
| 18 | **Multi-Model A/B Testing Service** | Compare model outputs for enterprises | stack_governor.py routing logic |

### Tools & Frameworks to Integrate

| Tool | GitHub Stars | What It Does | Integration Point |
|------|-------------|-------------|------------------|
| **OpenClaw** | 147K | Heartbeat-based autonomous agent | Replace/augment ship_captain.py |
| **CrewAI** | 20K+ | Multi-agent business workflows | Agent team orchestration for complex ops |
| **AutoGPT Forge** | 182K | Build custom autonomous agents | Template for new lane workers |
| **Aider** | ~20K | Terminal AI pair programming | Code generation in Ralph loops |
| **OpenHands** | ~15K | Autonomous software engineering | Complex app building |
| **Tart** | ~5K | Apple Silicon VM management | M2 worker isolation |

---

## 10. CRON ORCHESTRATION & RUNTIME LOOP

### Master Cron Schedule

```
# ============================================
# PRINTMAXX MASTER CRON (Worker Node / M2)
# ============================================

# TIER 0: System Health (every 30 min)
*/30 * * * * cd $BASE && python3 AUTOMATIONS/ship_captain.py --tick
*/30 0-8 * * * cd $BASE && python3 AUTOMATIONS/auto_resume_monitor.sh

# TIER 1: Morning Cycle (5-9 AM)
0 5 * * * cd $BASE && python3 AUTOMATIONS/memory_manager.py --full
30 5 * * * cd $BASE && python3 AUTOMATIONS/twitter_alpha_scraper.py --all
45 5 * * * cd $BASE && python3 AUTOMATIONS/unified_alpha_monitor.py --full
0 6 * * * cd $BASE && ./printmaxx_cron.sh morning
0 6 * * * cd $BASE && codex exec "$(cat OPS/DAILY_STRATEGIC_PROMPT.md)" > OPS/DAILY_STRATEGY_$(date +%Y_%m_%d).md 2>/dev/null || true
15 6 * * * cd $BASE && python3 AUTOMATIONS/background_reddit_scraper.py --scrape
30 6 * * * cd $BASE && python3 AUTOMATIONS/daily_research_pipeline.py --full
0 7 * * * cd $BASE && python3 AUTOMATIONS/system_health_monitor.py --check
45 8 * * * cd $BASE && python3 AUTOMATIONS/compliance_deadline_tracker.py --check
0 9 * * * cd $BASE && ./printmaxx_cron.sh outreach
15 9 * * * cd $BASE && python3 AUTOMATIONS/telegram_community_monitor.py --scan

# TIER 2: Continuous Scanning
0 */2 * * * cd $BASE && python3 AUTOMATIONS/ecom_arb_engine.py --scan --top 8
0 */3 * * * cd $BASE && python3 AUTOMATIONS/freelance_demand_scanner.py --scan
0 */4 * * * cd $BASE && python3 AUTOMATIONS/trend_aggregator.py --scan
0 */6 * * * cd $BASE && python3 AUTOMATIONS/alpha_screening.py --pending

# TIER 3: Evening & Overnight
0 18 * * * cd $BASE && ./printmaxx_cron.sh digest
0 21 * * * cd $BASE && ./printmaxx_cron.sh backup
0 22 * * * cd $BASE && ./printmaxx_cron.sh overnight
0 3 * * * cd $BASE && python3 AUTOMATIONS/closed_loop_pipeline.py --cycles 5 --batch 2000

# TIER 4: Weekly
0 3 * * 1 cd $BASE && ./printmaxx_cron.sh weekly
0 4 * * 1 cd $BASE && python3 scripts/strategic_rbi_engine.py full

# TIER 5: Monthly
0 3 1 * * cd $BASE && ./printmaxx_cron.sh monthly

# TIER 6: Voice Sidecar (Qwen3-TTS)
0 10 * * * cd $BASE && bash scripts/approved_voice_runner.sh --max-jobs 2 --max-blocks-per-source 1
0 14 * * * cd $BASE && python3 AUTOMATIONS/approved_script_voice_runner.py --dry-run >> AUTOMATIONS/logs/voice_sidecar.log

# TIER 7: Swarm Audit (Weekly)
0 2 * * 0 cd $BASE && python3 AUTOMATIONS/meta_vision_swarm_audit.py --write --tag $(date +%Y_%m_%d)
0 3 * * 0 cd $BASE && python3 AUTOMATIONS/master_ops_enhancer.py
```

**Secure Minimal Cron:** CODEX.md specifies `AUTOMATIONS/crontab_secure_minimal.txt` as the hardened production crontab. Install via `scripts/install_secure_cron.sh`. The master schedule above is the full development cron. For production worker nodes, use the secure minimal version which strips research/scraping jobs and only retains revenue-critical lanes.

### Runtime Loop Flow

```
Every 30 minutes (ship_captain.py --tick):
  1. Read HEARTBEAT.md
  2. Check active-tasks.md for interrupted work
  3. Check HUMAN_APPROVALS.csv for newly approved actions
  4. Route to highest-priority unblocked lane
  5. Execute up to 3 tasks per lane
  6. Update HEARTBEAT.md + active-tasks.md
  7. Log to daily log
  8. Check budget remaining (STACK_POLICY.json caps)
  9. If budget exceeded, pause non-free operations

Every morning (printmaxx_cron.sh morning):
  1. Alpha sync from overnight scrapers
  2. RBI daily audit
  3. Memory layer refresh
  4. Generate daily TODO

Every evening (printmaxx_cron.sh digest):
  1. Yield summary (what was accomplished)
  2. Revenue check
  3. Next-day priority setting

Overnight (Ralph loops):
  1. Launch parallel Ralph loops on highest-EV ops
  2. Content generation across all niches
  3. Lead qualification pipeline (closed-loop)
  4. Alpha research and screening
```

---

## 11. GUARDRAILS & SAFETY ARCHITECTURE

### Blast Radius Controls

| Action | Allowed On | Blocked On | Approval Required? |
|--------|-----------|-----------|-------------------|
| File read/write | Worker VM only | Control node | No (within project) |
| API calls | Both nodes | - | No |
| Email sends | Worker VM only | Control node | Yes (EMAIL_INFRA) |
| App deploys | Worker VM only | Control node | Yes (DEPLOY_APPS) |
| Static deploys | Worker VM only | Control node | Yes (DEPLOY_STATIC_SITES) |
| Git push | Both nodes | - | No (non-destructive) |
| Payment actions | Neither (human only) | Both nodes | Always |
| Account creation | Neither (human only) | Both nodes | Always |
| Destructive git ops | Neither | Both nodes | Human only |

### Worker VM Safety

1. **Ephemeral VMs**: Destroy and recreate after risky operations
2. **No host filesystem access**: VM can only see shared project directory
3. **Network restrictions**: Outbound HTTPS only, no inbound
4. **Resource limits**: CPU/RAM caps in Tart config prevent runaway processes
5. **PID tracking**: active-tasks.md tracks all running processes for manual kill

### Budget Safety

```json
// OPS/STACK_POLICY.json
{
  "budget": {
    "monthly_cap_usd": 200,
    "soft_cap_usd": 150,    // Warning at $150
    "hard_pause_cap_usd": 190,  // Pause non-critical at $190
    "daily_target_usd": 6.5,
    "premium_token_share_max_percent": 15  // Max 15% on expensive models
  }
}
```

When approaching caps:
- At $150: Log warning, reduce non-critical scanning frequency
- At $190: Pause all paid API calls except active revenue-generating tasks
- At $200: Only free tiers and local models

### Data Protection

- `SECRETS/` directory is gitignored
- Credentials never in source code
- API keys in environment variables only
- Guardrails Python module validates all file operations
- Backup runs nightly to `~/PRINTMAXX_BACKUPS/` (outside project)

---

## 12. IMPLEMENTATION ROADMAP

### Phase 1: Foundation (Day 1-2)

**On M2 Worker:**
```bash
# 1. Install Tart
brew install cirruslabs/cli/tart

# 2. Create base VM
tart create --from-ipsw latest printmaxx-base

# 3. Install Ollama in VM
tart exec printmaxx-base -- bash -c "curl -fsSL https://ollama.com/install.sh | sh"
tart exec printmaxx-base -- bash -c "ollama pull qwen2.5:7b && ollama pull llama3.1:8b && ollama pull phi4"

# 4. Clone project into VM shared directory
tart exec printmaxx-base -- bash -c "git clone <repo> /workspace/PRINTMAXX_STARTER_KITttttt"

# 5. Install Python dependencies
tart exec printmaxx-base -- bash -c "cd /workspace/PRINTMAXX_STARTER_KITttttt && pip3 install -r requirements.txt"

# 6. Save base VM snapshot
tart stop printmaxx-base
```

**On M1 Control:**
```bash
# 1. Set up SSH key for M2 access
ssh-keygen -t ed25519 -f ~/.ssh/printmaxx_m2
ssh-copy-id -i ~/.ssh/printmaxx_m2.pub user@m2-ip

# 2. Install Codex CLI
npm install -g @openai/codex

# 3. Configure OpenRouter API key
echo "OPENROUTER_API_KEY=sk-or-..." >> ~/Documents/p/PRINTMAXX_STARTER_KITttttt/SECRETS/CREDENTIALS.env
```

### Phase 2: Model Routing (Day 2-3)

1. Update `AUTOMATIONS/stack_governor.py` with new routing table
2. Update `OPS/STACK_POLICY.json` with new model defaults
3. Create `AUTOMATIONS/openrouter_client.py` for unified API access
4. Create `AUTOMATIONS/codex_cli_wrapper.py` for scripted Codex prompts
5. Test routing logic: each task type hits correct model

### Phase 3: Autonomous Loop (Day 3-5)

1. Update `AUTOMATIONS/ship_captain.py` with new tick logic
2. Wire `CLAWWORK_SIDECAR_POLICY.json` lane evaluation
3. Install cron schedule on M2 worker VM
4. Test full loop: heartbeat → route → execute → log → heartbeat
5. Run overnight test (5 Ralph loops in parallel)

### Phase 4: Human Approval Unblocking (Day 5-7)

Priority order (from PRIORITY_AUTOMATION_EXEC):
1. Create Gumroad account (10 min) → unblocks D01
2. Create Fiverr account (15 min) → unblocks S01
3. Create X accounts (5 min) → unblocks C01
4. Set up email infrastructure → unblocks S05, C12
5. Apple dev account → unblocks N68, P11

### Phase 5: Scale (Week 2+)

1. Deploy all 17 PRIORITY_LAUNCH ventures
2. Expand to LLM_ALPHA_THESIS experiments
3. Add synergy stacks (highest multiplier first)
4. Weekly venture performance reviews (KILL/MAINTAIN/DOUBLE_DOWN)
5. Monthly budget rebalancing

---

## APPENDIX A: Quick Reference Commands

```bash
# System health check
python3 AUTOMATIONS/system_health_monitor.py --quick

# Ship captain manual tick
python3 AUTOMATIONS/ship_captain.py --tick

# Memory refresh
python3 AUTOMATIONS/memory_manager.py --full

# Venture performance
python3 AUTOMATIONS/venture_performance_tracker.py --recommend

# Budget check
python3 AUTOMATIONS/stack_governor.py --budget

# Start parallel Ralph loops
cd ralph && bash run_parallel_loops.sh

# Codex CLI strategic analysis
codex exec "$(cat OPS/DAILY_STRATEGIC_PROMPT.md)" > OPS/DAILY_STRATEGY.md

# OpenRouter model test
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek/deepseek-chat-v3.2","messages":[{"role":"user","content":"test"}]}'

# --- SWARM AUDIT COMMANDS (from CODEX.md) ---

# Full-content corpus rebuild (10 workers, compressed shards, deduped)
python3 AUTOMATIONS/full_context_swarm_dump.py --write --workers 10 --chunk-chars 5000 --max-records-per-shard 2500 --compress-shards --dedupe-content

# Metrics/meta sweep (tagged by date)
python3 AUTOMATIONS/meta_vision_swarm_audit.py --write --tag 2026_02_17

# Master Ops workbook enhancement (adds 7 automation sheets)
python3 AUTOMATIONS/master_ops_enhancer.py

# Master Ops execution planning (safe, top 12 ops, max 3 per lane)
python3 AUTOMATIONS/master_ops_executor.py --top 12 --max-per-lane 3

# --- VOICE STACK COMMANDS (Qwen3-TTS) ---

# Local Qwen3-TTS setup (first run downloads model)
bash scripts/setup_qwen3_tts_local.sh
DOWNLOAD_MODEL=1 bash scripts/setup_qwen3_tts_local.sh

# Longform voice render
bash scripts/qwen3_tts_longform.sh --text-file <path_to_script_txt> --speaker aiden --language English --out output/qwen_tts/longform.wav

# Approved-script voice sidecar (dry run)
python3 AUTOMATIONS/approved_script_voice_runner.py --dry-run

# Approved-script voice sidecar (live, max 2 concurrent jobs)
bash scripts/approved_voice_runner.sh --max-jobs 2 --max-blocks-per-source 1

# --- SECURE CRON ---

# Install hardened minimal cron (production worker)
bash scripts/install_secure_cron.sh
```

## APPENDIX B: File Index for This System

| File | Purpose |
|------|---------|
| `OPS/PRINTMAXX_CLAWDBOT_SYSTEM_OPS.md` | THIS DOCUMENT — master system ops |
| `CODEX.md` | Lean agent contract (always read first) |
| `.claude/CLAUDE.md` | Deep institutional memory |
| `OPS/STACK_POLICY.json` | Model routing and budget config |
| `OPS/NODE_ROLE.json` | Control vs worker node identity |
| `OPS/CLAWWORK_SIDECAR_POLICY.json` | Lane evaluation and priorities |
| `OPS/HUMAN_LOOP_QUEUE.md` | Pending human approvals |
| `OPS/HUMAN_APPROVALS.csv` | Approved actions |
| `OPS/HEARTBEAT.md` | System pulse (<20 lines) |
| `OPS/active-tasks.md` | Crash recovery state |
| `AUTOMATIONS/ship_captain.py` | Primary runtime loop |
| `AUTOMATIONS/stack_governor.py` | Model routing engine |
| `AUTOMATIONS/memory_manager.py` | 3-layer memory management |
| `AUTOMATIONS/ralph_loop_factory.py` | Generate Ralph loops for any op |
| `AUTOMATIONS/closed_loop_pipeline.py` | Lead→email→track automation |
| `printmaxx_cron.sh` | Master cron orchestrator |
| **--- NEW (CODEX.md 2026-02-16 Refresh) ---** | |
| `OPS/CLAWWORK_MINIMAL_SIDECAR_PLAN.md` | Minimal sidecar execution plan |
| `output/clawwork_sidecar/latest.md` | Latest sidecar run output |
| `LEDGER/CLAWWORK_SIDECAR_RUNS.csv` | Sidecar run history/metrics |
| `OPS/QWEN3_TTS_LOCAL_STACK.md` | Local voice stack setup guide |
| `scripts/setup_qwen3_tts_local.sh` | Qwen3-TTS install/setup |
| `scripts/qwen3_tts_longform.sh` | Longform voice rendering |
| `scripts/approved_voice_runner.sh` | Approved script voice sidecar |
| `AUTOMATIONS/qwen3_tts_longform.py` | Python longform TTS engine |
| `AUTOMATIONS/approved_script_voice_runner.py` | Voice render queue processor |
| `OPS/VOICEOVER_APPROVED_QUEUE.csv` | Scripts approved for voice render |
| `LEDGER/VOICE_RENDER_RUNS.csv` | Voice render run history |
| `output/qwen_tts/` | Voice render output directory |
| `AUDIT/META_VISION.md` | Historical baseline audit |
| `AUDIT/META_VISION_2026_02_16.md` | Swarm metrics sweep |
| `AUDIT/META_VISION_2026_02_17_AUTOMATION.md` | Automation upgrade pass |
| `AUDIT/META_VISION_FULL_CONTEXT_2026_02_16.md` | Raw-corpus-linked audit |
| `AUDIT/META_VISION_2026_02_16_FILE_INVENTORY.csv` | Full file/folder inventory |
| `AUTOMATIONS/full_context_swarm_dump.py` | Corpus rebuild with compression |
| `AUTOMATIONS/meta_vision_swarm_audit.py` | Metrics/meta sweep tool |
| `AUTOMATIONS/master_ops_enhancer.py` | Enhance master ops spreadsheet |
| `AUTOMATIONS/master_ops_executor.py` | Execute top-priority ops from spreadsheet |
| `AUTOMATIONS/crontab_secure_minimal.txt` | Hardened production crontab |
| `scripts/install_secure_cron.sh` | Secure cron installer |
| `OPS/STACK_HEARTBEAT.md` | Stack-level heartbeat status |
| `OPS/HUMAN_EXECUTION_BRIEF.md` | Human execution brief |
| `output/cron_fleet/latest.md` | Latest cron fleet output |

---

*This document synthesizes analysis from: 19 spreadsheet tabs (PRINTMAXX_MASTER_OPS_ENHANCED), CODEX.md (2026-02-16 refresh with operator intent defaults, ClawWork sidecar, Qwen3-TTS voice stack, Meta Vision audit corpus, Master Ops execution layer, secure cron), CLAUDE.md, STACK_POLICY.json, NODE_ROLE.json, CLAWWORK_SIDECAR_POLICY.json, 77+ automation scripts, 96+ OPS files, deep web research on Kimi K2.5/MiniMax/OpenRouter/OpenClaw/CrewAI/AutoGPT/Tart/Codex CLI pricing and architecture.*
