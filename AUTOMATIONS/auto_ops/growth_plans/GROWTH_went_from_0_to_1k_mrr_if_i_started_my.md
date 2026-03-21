# Growth Plan: Went from $0 to $1k MRR. If I started my SaaS over, here's e

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $0 direct — selection filter improves app factory hit rate ~15-20% by killing low-retention ideas earlier

---

## Tactics

1. Ship app factory apps that solve weekly recurring loops (habit tracking, prayer, finance, health) — these already dominate our portfolio
2. In app store listings, explicitly call out the recurring use case in the subtitle (e.g. 'Daily streak tracker' not 'track your goals')
3. Use recurrence frequency as a proxy for retention — filter app ideas by 'how often does the user come back?'

## Budget Tier Strategies

### FREE
Audit existing 69 deployed apps against recurrence test — flag any that solve one-time problems for kill/pivot. Takes 1 hour.

### LOW
Add 'recurrence score' dimension to capital_genesis_ranker.py — weight daily-use apps 1.3x in composite score.

### MID
N/A — this is a selection filter, not a paid channel

## Daily Actions

- [ ] Add recurrence_score field to app_factory_priority_queue.json scoring rubric (0=one-time, 5=daily, 10=multiple/day)
- [ ] Patch app_factory_command_center.py --refresh to apply recurrence multiplier before ranking
- [ ] Retroactively flag existing 69 live apps: streaks/prayer/habit = HIGH, one-time tools = LOW
- [ ] Wire into existing chain_4day_saas_validation_vibe_coding_gemi as step 0 gate

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "none"
}
```
