# PRINTMAXX Daily Ops Playbook
**Last updated:** 2026-02-05
**Based on:** System Audit Feb 5 2026

---

## Session Start (5 min)
1. Read `OPS/SESSION_HANDOFF_FEB5_2026.md` for current context
2. Run `python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary` (check system health)
3. Check `OPS/SYSTEM_AUDIT_FEB5_2026.md` section "CRITICAL ISSUES" for known blockers
4. Check `06_OPERATIONS/setup/HUMAN_INFRA_CHECKLIST.md` for tasks requiring human action

---

## Research Block (30-60 min)
**Use these working tools:**
- Swarm system: `ralph/.swarm/` (produces real alpha, tested Feb 5)
- Alpha screener: `python3 AUTOMATIONS/alpha_screening.py --pending` (9/11 quant tools work)
- Niche meta detector: `python3 AUTOMATIONS/niche_meta_detector.py`
- Platform monitor: `python3 AUTOMATIONS/platform_meta_monitor.py`

**Data sources:**
- High-signal accounts: `LEDGER/HIGH_SIGNAL_SOURCES.csv` (81+ accounts)
- Research subreddits: `LEDGER/RESEARCH_SUBREDDITS.csv` (41 subreddits)

**Output protocol:**
- New findings → `LEDGER/ALPHA_STAGING.csv` (status: PENDING_REVIEW)
- Before appending: run through alpha_screening to avoid duplicates
- Reference `LEDGER/CROSS_POLLINATION_MATRIX.csv` for method synergies

---

## Build Block (Main Session)
1. Pick highest-priority task from sprint
2. Use parallel agents for independent work (PARALLELRALPHMAXX mode)
3. Write to disk immediately (filesystem = memory)
4. Reference cross-pollination matrix for synergies
5. Check `MONEY_METHODS/INDEX.md` for method context before starting

---

## Session End (5 min)
1. Update `OPS/SESSION_HANDOFF_FEB5_2026.md` with what was accomplished
2. Log new files created to relevant LEDGER/INDEX entries
3. Flag any blockers needing human action to HUMAN_INFRA_CHECKLIST.md
4. Run `git status` to see uncommitted changes

---

## Proactive Checklist (Run Weekly)
- [ ] Scan 5+ high-signal sources for new alpha
- [ ] Check `LEDGER/ACTIVE_INVESTMENTS.csv` for overdue actions
- [ ] Run `python3 AUTOMATIONS/alpha_screening.py --pending` batch
- [ ] Update financial trackers if new revenue/expense data
- [ ] Verify no CSV corruption in ALPHA_STAGING.csv (check line count + sample rows)
- [ ] Check that all appended alphas have properly quoted multi-line fields
- [ ] Run `python3 AUTOMATIONS/niche_meta_detector.py` for trend shifts
- [ ] Run `python3 AUTOMATIONS/platform_meta_monitor.py` for algorithm changes
- [ ] Check `LEDGER/CROSS_POLLINATION_MATRIX.csv` for new synergy stacks
- [ ] Review `06_OPERATIONS/setup/HUMAN_INFRA_CHECKLIST.md` for unblocked human tasks

---

## Known Broken Systems (DO NOT USE)
| System | Status | Why |
|--------|--------|-----|
| Individual ralph loops (17 total) | BROKEN | `--max-tokens` flag doesn't exist in claude CLI |
| Mega ralph loop | NOT BUILT | Directory is stub, no prompt.md or run.sh |
| revenue_projector.py | BROKEN | ValueError on string-to-float parsing |
| method_performance_analyzer.py | BROKEN | ValueError on `$99` parsing |
| ALPHA_STAGING.csv | 63% CORRUPTED | Multi-line unescaped content, 146 duplicate IDs, 199 duplicate URLs |

---

## Working Automation Quick Reference
| Tool | Command | Purpose |
|------|---------|---------|
| **Quant terminal** | `python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary` | System health check |
| **Alpha screener** | `python3 AUTOMATIONS/alpha_screening.py --pending` | Score pending entries (0-100, deploy ≥70) |
| **Paper trader** | `python3 AUTOMATIONS/paper_trade.py --list` | Test methods with $0-100 budget |
| **Ops dashboard** | `python3 AUTOMATIONS/ops_dashboard.py` | Track 53 daily/weekly/monthly ops |
| **Swarm research** | See `ralph/.swarm/` directory | Primary working research system |

---

## Reality Check (Updated Feb 5)
- **Real alpha entries:** ~1,288 unique valid (not 3,908 claimed)
- **Apps shipped:** 0 (not 27)
- **Social posts published:** 0 (not 1,008)
- **Commercial revenue:** $0
- **Quant tools working:** 9/11 (2 broken, documented above)
- **Research quality:** Excellent (swarm system works)
- **Code quality:** Good (what exists is well-written)
- **Shipping quality:** Zero (no products in customer hands)

---

## Highest ROI Actions (In Priority Order)
1. **Ship one product (today):** Gumroad PDF compilation = 2 hours, possible same-day revenue
2. **Slim CLAUDE.md (this week):** Cuts context tax from 33% to 11%, saves 43K tokens/message
3. **Fix ALPHA_STAGING.csv (this week):** Write repair script for 63% corruption
4. **Fix 2 broken quant scripts (30 min):** revenue_projector.py + method_performance_analyzer.py
5. **Clean directory structure (this week):** Delete node_modules bloat (22GB) + legacy directories

---

## When Stuck
1. Check `OPS/CRITICAL_PATH_DOCS.md` for dependency chains
2. Search `OPS/SYSTEM_AUDIT_FEB5_2026.md` for known issues
3. Verify tool is in "Working Automation" table above
4. If automation is broken, use manual equivalent
5. Log blockers to SESSION_HANDOFF for next agent

---
