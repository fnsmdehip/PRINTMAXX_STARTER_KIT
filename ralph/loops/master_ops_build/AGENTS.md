# Master Ops Build — Agent Codebase Reference

## Key Files

| File | Purpose |
|------|---------|
| `scripts/builders/build_master_ops_v2.py` | Generates PRINTMAXX_MASTER_OPS.xlsx (11 sheets) |
| `scripts/builders/build_ops_playbook.py` | Original 16-op playbook builder (data source) |
| `scripts/builders/build_ops_addendum.py` | OP17-OP22 addendum (data source) |
| `scripts/self_test.py` | Scores ops 0-100 (GREEN/YELLOW/RED) |
| `scripts/revenue_intake.py` | Revenue tracking CLI |
| `scripts/experiment_runner.py` | A/B test lifecycle manager |
| `scripts/account_tracker.py` | Account lifecycle + warmup |

## LEDGER Source of Truth

| CSV | Schema |
|-----|--------|
| `LEDGER/ALPHA_STAGING.csv` | alpha_id,source,category,status,roi_potential,... |
| `LEDGER/ACCOUNTS.csv` | platform,handle,status,warmup_day,... |
| `LEDGER/CROSS_POLLINATION_MATRIX.csv` | method_a,method_b,synergy_score,... |
| `FINANCIALS/REVENUE_TRACKER.csv` | date,amount,method,platform,... |
| `LEDGER/AB_TESTS_MASTER.csv` | test_id,test_name,status,variant_a,variant_b,... |

## Agent Team Pattern

```python
# 1. Create team
TeamCreate(team_name="master-ops-t2")

# 2. Create tasks for the team
TaskCreate(subject="Scan alpha staging", ...)
TaskCreate(subject="Update tech stack", ...)

# 3. Spawn agents with team_name
Task(subagent_type="general-purpose", team_name="master-ops-t2", name="alpha-scanner", ...)
Task(subagent_type="general-purpose", team_name="master-ops-t2", name="tech-updater", ...)

# 4. Agents work autonomously, update task status
# 5. When all done:
TeamDelete()
```

## Copy Style

ALL content follows `.claude/rules/copy-style.md`:
- No em dashes
- No AI vocabulary (leverage, utilize, delve, comprehensive, robust)
- Consequence-first hooks
- Specific numbers always
- @pipelineabuser energy (50% weight)

## Method ID Conventions

- C01-C20: Content ops
- E01-E10: Ecommerce ops
- D01-D12: Digital product ops
- S01-S18: Service/freelance ops
- A01-A12: App/SaaS ops
- P01-P12: AI persona ops
- I01-I05: Investment/trading ops
- M01-M06: Community/membership ops
- F01-F05: Affiliate ops
- G01-G15: Growth/infrastructure ops
- OP01-OP22: Deep playbook ops (detailed instructions)

## Output Locations

- XLSX: `PRINTMAXX_MASTER_OPS.xlsx` (project root)
- Content: `ralph/loops/master_ops_build/output/`
- Progress: `ralph/loops/master_ops_build/.ralph/progress.md`
- Logs: `ralph/logs/master_ops_build_*.log`
