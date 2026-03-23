# Reprocess-on-Discovery Rule (ALWAYS active)

## The Problem This Solves

New resources (playbooks, guides, products, tools, research docs) were added to the system without reprocessing Capital Genesis scoring, KPI tracking, or the actionable queue. A method with no playbook might score 6.0, but with a ready-to-use playbook it should score 7.5+ (lower effort = higher composite). The system was making decisions on stale scores.

## When to Trigger Reprocessing

Reprocess the scoring pipeline when ANY of these happen:

1. **New playbook/guide created** — a method now has execution instructions that didn't exist before
2. **New digital product created** — a method now has a sellable asset (increases revenue_potential)
3. **New automation script created** — a method now has higher automation_potential
4. **New research doc created** — a method now has better intelligence (reduces risk scores)
5. **Resource Manifest updated** — any addition to `OPS/RESOURCE_MANIFEST.md`
6. **New money method discovered** — via alpha pipeline or manual entry
7. **Existing method enhanced** — playbook expanded, new integrations wired

## Reprocessing Steps (ALL mandatory)

```bash
# 1. Rescore all methods with updated context
python3 AUTOMATIONS/capital_genesis_ranker.py --rank --report

# 2. Regenerate the priority stack
# (capital_genesis_ranker.py writes to OPS/CAPITAL_GENESIS_PRIORITY_STACK.md)

# 3. Check if P0/P1 methods changed
# Compare new priority stack to previous — surface any promotions/demotions

# 4. Update actionable queue if priorities shifted
python3 AUTOMATIONS/actionable_aggregator.py
```

## Why This Matters

Capital Genesis scores on 7 dimensions. Two of them are directly affected by resource discovery:

- **speed_to_revenue** — having a playbook means faster execution, higher speed score
- **automation_potential** — having an automation script means higher automation score

A third is indirectly affected:
- **downside_risk** — having research/compliance docs means lower risk, higher score

Without reprocessing, the ranker makes decisions on stale data. Methods that should be P0 stay at P2. Methods with new playbooks don't get the scoring boost they deserve.

## Anti-Patterns This Rule Kills

- Adding 200+ resources to a manifest without rerunning Capital Genesis
- Creating playbooks for methods without updating their scores
- Building automation scripts without updating automation_potential scores
- Discovering new tools/products without checking if they affect the priority stack
- Any session that touches `OPS/RESOURCE_MANIFEST.md` without running `capital_genesis_ranker.py --rank`

## Automation

The nightly cron already runs `capital_genesis_ranker.py` at 5:30 AM. But that only catches changes from the previous day. When doing a major resource discovery (like adding 200+ items), the ranker MUST be run immediately in-session, not deferred to cron.

## Session Checklist

At session end, before updating task tracker, ask:
1. Did I create or discover any new resources this session?
2. If yes, did I update `OPS/RESOURCE_MANIFEST.md`?
3. If yes, did I rerun `capital_genesis_ranker.py --rank`?
4. If any of these are "no" — DO IT NOW before session end.
