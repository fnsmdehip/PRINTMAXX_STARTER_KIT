# Master Ops Loop - Codebase Patterns & Reference

This document helps a fresh Claude context understand the codebase structure relevant to this loop's 8 tasks.

---

## Key Scripts

### scripts/builders/build_master_ops_v2.py
- Generates `PRINTMAXX_MASTER_OPS.xlsx` using openpyxl
- 150+ ops across 10 themed sheets (dark Bloomberg aesthetic)
- Requires `openpyxl` Python package
- Run from project root: `python3 scripts/builders/build_master_ops_v2.py`
- Output lands in project root as `PRINTMAXX_MASTER_OPS.xlsx`

### scripts/self_test.py
- Validates operational readiness for all money methods
- Scores each op 0-100 across: Infrastructure, Accounts, Revenue, Freshness
- Usage: `python3 scripts/self_test.py --json` for machine-readable output
- Usage: `python3 scripts/self_test.py --op MM007` for single op test
- Reads from: LEDGER/ACCOUNTS.csv, FINANCIALS/REVENUE_TRACKER.csv, MONEY_METHODS/
- Outputs to: LEDGER/SELF_TEST_RESULTS/

### scripts/revenue_intake.py
- CLI for logging and summarizing revenue
- Usage: `python3 scripts/revenue_intake.py summary` for revenue summary
- Usage: `python3 scripts/revenue_intake.py dashboard` for visual dashboard
- Reads/writes: FINANCIALS/REVENUE_TRACKER.csv
- Maps method IDs via LEDGER/MEGA_SHEET/TAB1_MONEY_METHODS_MASTER.csv

---

## LEDGER Directory (Source of Truth)

All tracking data lives in CSV files here. Agent reads from LEDGER, never writes directly to XLSX.

### Core CSVs Used By This Loop

| File | Purpose | Key Columns |
|------|---------|-------------|
| `LEDGER/ALPHA_STAGING.csv` | All alpha entries (pending + approved + rejected) | alpha_id, source, category, status, roi_potential, tactic_summary |
| `LEDGER/ACCOUNTS.csv` | All platform accounts and their states | platform, username, status, proxy_required, anti_detect_profile |
| `LEDGER/CROSS_POLLINATION_MATRIX.csv` | Method-to-method synergy scores | method_a, method_b, synergy_score, stack_description |
| `LEDGER/MEGA_SHEET/TAB1_MONEY_METHODS_MASTER.csv` | All 68+ money methods | method_id, method_name, category, status, revenue_potential |
| `LEDGER/MEGA_SHEET/TAB4_TOOLS_CHANNELS_MASTER.csv` | Tools, marketing channels, MCP servers | tool_name, category, cost, status, tier |
| `LEDGER/MEGA_SHEET/TAB7_SOURCES_ACCOUNTS.csv` | High signal sources, social accounts | source_name, platform, tier, signal_quality |

### Financial CSVs

| File | Purpose | Key Columns |
|------|---------|-------------|
| `FINANCIALS/REVENUE_TRACKER.csv` | All revenue by method | date, method_id, method_name, revenue, expenses, profit, source |
| `FINANCIALS/EXPENSE_TRACKER.csv` | All expenses | date, category, amount, description, tax_deductible |
| `FINANCIALS/P_AND_L_MONTHLY.csv` | Monthly profit/loss | month, revenue, expenses, profit |

---

## Output Locations

This loop writes to these locations:

| Output | Path | Format |
|--------|------|--------|
| Loop progress (append-only) | `ralph/loops/master_ops/.ralph/progress.md` | Markdown with task sections |
| Task state | `ralph/loops/master_ops/prd.json` | JSON with passes: true/false |
| Alpha sync log | `ralph/loops/master_ops/.ralph/alpha_sync_log.csv` | CSV: date, alpha_id, mapped_op, summary |
| Account sync summary | `ralph/loops/master_ops/.ralph/accounts_sync.md` | Markdown summary |
| Cross-pollination findings | `ralph/loops/master_ops/.ralph/cross_pollination_findings.md` | Markdown analysis |
| Revenue sync summary | `ralph/loops/master_ops/.ralph/revenue_sync.md` | Markdown summary |
| Priority rankings | `ralph/loops/master_ops/.ralph/priority_rankings.md` | Ranked list with scores |
| Infra inventory | `ralph/loops/master_ops/.ralph/infra_inventory.md` | Categorized tool list |
| Generated content | `ralph/loops/master_ops/output/generated_content.md` | Content pieces, PENDING_REVIEW |

---

## Agent Team Pattern (For T8 or Parallel Work)

If a task benefits from spawning subagents:

```
1. TeamCreate (team_name, description)
2. TaskCreate (subject, description, activeForm) - for each subtask
3. Task tool (spawn agents with team_name + name)
4. TaskUpdate (assign tasks to agents via owner)
5. Agents work, mark tasks completed via TaskUpdate
6. SendMessage for coordination
7. TeamDelete when done
```

This loop does NOT typically need teams - tasks are sequential and one-per-iteration. But T8 (content generation) could use parallel agents if generating many content pieces.

---

## Copy Style Rules (For T8 Content Generation)

All generated content MUST follow `.claude/rules/copy-style.md`:
- No em dashes
- No AI vocabulary (leverage, utilize, delve, comprehensive, robust, innovative, seamless)
- Consequence-first hooks
- Exact numbers always
- Lowercase energy, @pipelineabuser voice (50% weight)
- Would @pipelineabuser actually post this? If no, rewrite.

Example good post:
```
ran self-test on 47 ops. 12 scored above 70 (launch-ready). 8 scored below 30 (need infra).
the gap between "ready" and "not ready" is almost always one thing: a warmed account.
```

Example bad post:
```
We've completed a comprehensive operational readiness assessment across our portfolio of money methods, revealing innovative insights about launch preparedness.
```

---

## Method ID Convention

- `MM001`-`MM069`: Core money methods (cold outbound, apps, content farms, etc.)
- `CF001`-`CF013`: Content farm sub-methods
- `AI001`-`AI008`: AI influencer sub-methods
- `SWARM001`: Swarm/agent method
- `N001`-`N033`: Niche IDs

---

## File Modification Rules

1. **LEDGER CSVs:** Read freely. Write only by appending rows (never overwrite headers or existing data).
2. **FINANCIALS CSVs:** Read freely. Write only through revenue_intake.py or by careful append.
3. **prd.json:** Read and rewrite (update passes field only).
4. **progress.md:** APPEND ONLY. Never truncate or overwrite.
5. **Output files in .ralph/:** Can create new or overwrite (these are ephemeral summaries).
6. **Output content:** Write to `ralph/loops/master_ops/output/` directory.

---

## Error Handling

Common issues and fixes:

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: openpyxl` | `pip3 install openpyxl` |
| `FileNotFoundError: ACCOUNTS.csv` | Log warning, create stub CSV with headers |
| `csv.Error: line contains NULL byte` | Skip malformed line, log line number |
| `self_test.py returns non-zero` | Try without `--json` flag, parse text output |
| `REVENUE_TRACKER.csv empty` | Log $0 revenue, continue (pre-revenue is normal) |
| `prd.json parse error` | Rewrite from scratch with current task states from progress.md |
