## CRITICAL: Autonomous System Architecture (OpenClaw Battle-Tested Patterns)

**Source:** 3 weeks of running OpenClaw autonomous agents. These patterns are battle-tested, not theoretical.

### 3-Layer Memory Architecture

Every piece of state the PRINTMAXX system produces lives in one of three layers:

| Layer | File | Purpose | Update Frequency |
|-------|------|---------|------------------|
| **Active Tasks** | `OPS/active-tasks.md` | Crash recovery. What's running NOW. If agent dies mid-task, next agent reads this and picks up exactly where it left off. | Every task start/end |
| **Daily Logs** | `AUTOMATIONS/logs/daily/YYYY-MM-DD.md` | What happened today. Append-only. Every tool, every script, every pipeline step logs here. | Continuous |
| **Thematic Memory** | `LEDGER/` + `AUTOMATIONS/leads/qualified/` + per-venture files | Long-term. Revenue, leads, alpha, experiments. Survives across weeks/months. | Per transaction |

**Plus HEARTBEAT.md** — `OPS/HEARTBEAT.md` — <20 lines of pure numbers. Any new agent reads this in 3 seconds and knows the full system state. Updated by `python3 AUTOMATIONS/memory_manager.py --heartbeat`.

**Memory Manager:** `python3 AUTOMATIONS/memory_manager.py`
- `--heartbeat` — Update HEARTBEAT.md
- `--active-tasks` — Refresh active-tasks.md
- `--daily-summary` — Generate end-of-day summary
- `--log "message"` — Append to today's daily log
- `--health` — Venture health check
- `--full` — Update all 3 layers

### Crash Recovery Pattern (active-tasks.md)

The single most important pattern. If an agent dies mid-task:
1. Next agent reads `OPS/active-tasks.md`
2. Sees exactly what was running, what step it was on, what's left
3. Picks up from that exact point

**Every long-running operation MUST:**
- Write to active-tasks.md BEFORE starting
- Update active-tasks.md at each step transition
- Clear active-tasks.md on successful completion

The closed-loop pipeline (`AUTOMATIONS/closed_loop_pipeline.py`) implements this pattern. All new tools should too.

### Closed-Loop Automation (No Human Review Required)

The bottleneck isn't AI capability. It's human review speed. Build systems that close the loop automatically.

**Closed-loop pipeline:** `python3 AUTOMATIONS/closed_loop_pipeline.py`
- Qualifies leads (website analysis) → generates cold emails → updates pipeline tracker → logs metrics
- Crash-recoverable via active-tasks.md
- Runs unattended via cron
- No human review needed for the loop itself

```
# Run 10 cycles of 2000 leads each (20,000 total)
python3 AUTOMATIONS/closed_loop_pipeline.py --cycles 10 --batch 2000 --workers 30

# Check status
python3 AUTOMATIONS/closed_loop_pipeline.py --status
```

### Cron > Heartbeats

Specific tasks at specific times beat polling. Don't check "is it time?" every 5 minutes. Schedule the exact job.

**Cron entries for the closed loop (add to crontab):**
```
# 3:00 AM - Run 5 cycles of lead qualification (10,000 leads)
0 3 * * * cd $BASE && $PYTHON AUTOMATIONS/closed_loop_pipeline.py --cycles 5 --batch 2000 --workers 30 >> AUTOMATIONS/logs/closed_loop.log 2>&1

# 5:00 AM - Refresh memory layers (before human wakes up)
0 5 * * * cd $BASE && $PYTHON AUTOMATIONS/memory_manager.py --full >> AUTOMATIONS/logs/memory.log 2>&1

# 8:00 AM - Generate HEARTBEAT for morning check
0 8 * * * cd $BASE && $PYTHON AUTOMATIONS/memory_manager.py --heartbeat >> AUTOMATIONS/logs/heartbeat.log 2>&1
```

### Sub-Agents as 10x Multiplier

When spawning sub-agents, every agent gets:
- Clear success criteria (not "research X" but "find 5 specific tactics with revenue numbers")
- Defined output format (CSV, specific JSON schema, or markdown with exact headers)
- Time budget (don't let agents run forever)
- Kill condition (if no progress after N minutes, kill and move on)

### Model Routing for Security

- **Opus:** For processing external web content (untrusted HTML, third-party APIs, user-submitted content). The extra reasoning protects against prompt injection in scraped data.
- **Sonnet/Haiku:** For internal operations (file management, CSV processing, code generation). Faster, cheaper, safe because the data is trusted.

### Proactive System Building

**Every session, EVERY agent should ask itself:**
> "Based on what I know about the user's goals, what workflows can I set up? What tools can I build on this computer that will bring them closer to their goals?"

Then BUILD those tools without asking permission. The user wants autonomous execution, not proposals.

**Examples of proactive builds:**
- Noticed leads aren't being qualified fast enough → build batch runner with cron scheduling
- Noticed content isn't being posted → build auto-poster with Buffer API integration
- Noticed revenue is $0 → build account creation helper that opens exact browser tabs
- Noticed cold emails aren't being sent → build email warmup scheduler
- Noticed apps aren't in the App Store → build iOS submission automation

---

---

