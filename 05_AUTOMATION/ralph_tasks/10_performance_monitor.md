# Ralph Task: Performance Monitor

Track metrics, A/B test results, and optimize based on data. Run daily/weekly.

---

## Context

Read these files:
- `LEDGER/FUNNEL_METRICS.csv` - Current metrics
- `LEDGER/CONTENT_QUEUE.csv` - Content performance
- `LEDGER/ALPHA_STAGING.csv` - New tactics to try
- `LEDGER/HIGH_SIGNAL_SOURCES.csv` - Sources to monitor

Output to:
- `OPS/reports/[DATE]_performance.md`
- `LEDGER/AB_TEST_LOG.csv`
- `LEDGER/OPTIMIZATION_QUEUE.csv`

---

## Success Criteria

### Step 1: Gather metrics

1. [ ] Pull revenue data (RevenueCat if accessible via API)
2. [ ] Pull content performance (engagement rates)
3. [ ] Pull ad performance (if accessible)
4. [ ] Calculate key KPIs:
    - MRR / ARR
    - Trial conversion rate
    - Churn rate
    - CAC by channel
    - LTV

### Step 2: Compare to benchmarks

5. [ ] Compare to previous period
6. [ ] Compare to targets in FUNNEL_METRICS.csv
7. [ ] Flag anything >20% off target
8. [ ] Identify top performers and underperformers

### Step 3: A/B test analysis

9. [ ] Check running A/B tests
10. [ ] Calculate statistical significance
11. [ ] Recommend winner or continue test
12. [ ] Log results to AB_TEST_LOG.csv

### Step 4: Optimization recommendations

13. [ ] For each underperforming metric, propose fix
14. [ ] Prioritize by impact and effort
15. [ ] Add to OPTIMIZATION_QUEUE.csv
16. [ ] Create specific action items

### Step 5: Competitive monitoring

17. [ ] Check competitor apps (App Store updates, pricing changes)
18. [ ] Check competitor social (new content formats)
19. [ ] Note any tactics to test

### Step 6: Source monitoring

20. [ ] Scan HIGH_SIGNAL_SOURCES.csv accounts
21. [ ] Extract new tactics/tools
22. [ ] Add to ALPHA_STAGING.csv if valuable
23. [ ] Flag anything for immediate implementation

### Step 7: Generate report

24. [ ] Create daily/weekly performance report
25. [ ] Highlight wins
26. [ ] Highlight concerns
27. [ ] List action items

---

## Report Template

```markdown
# Performance Report - [DATE]

## Summary
- MRR: $X (↑/↓ Y% vs last period)
- New users: X
- Conversion rate: X%
- Churn: X%

## Wins
1. [Win with context and numbers]
2. [Win]

## Concerns
1. [Concern with diagnosis and proposed fix]
2. [Concern]

## A/B Tests
| Test | Status | Winner | Next steps |
|------|--------|--------|------------|
| Paywall copy | Complete | Variant B | Roll out |
| Price test | Running | Inconclusive | Continue 1 week |

## Optimizations Implemented
- [What was changed and result]

## Optimizations Queued
1. [Priority 1 optimization]
2. [Priority 2 optimization]

## Competitive Intel
- [Competitor did X, consider Y]

## Alpha Finds
- [New tactic found, added to staging]

## Action Items
- [ ] [Specific action]
- [ ] [Specific action]
```

---

## A/B Test Log Format

```csv
test_id,app,test_type,variant_a,variant_b,start_date,end_date,sample_a,sample_b,metric,result_a,result_b,winner,confidence,notes
1,prayerlock,paywall_copy,Original,Urgency,2026-01-15,2026-01-22,500,500,conversion,12%,18%,B,95%,Roll out B
```

---

## Optimization Queue Format

```csv
id,app,area,issue,proposed_fix,expected_impact,effort,priority,status,assigned_date
1,prayerlock,onboarding,50% drop at step 3,Simplify form,+10% completion,LOW,P1,queued,2026-01-21
```

---

## Metrics to track

### Revenue metrics
- MRR (Monthly Recurring Revenue)
- ARR (Annual Recurring Revenue)
- ARPU (Average Revenue Per User)
- LTV (Lifetime Value)

### Acquisition metrics
- Downloads by source
- Cost per install (CPI)
- App Store conversion rate
- Landing page conversion rate

### Activation metrics
- Onboarding completion rate
- Time to first value
- Trial start rate

### Retention metrics
- Day 1, 7, 30 retention
- Weekly/monthly active users
- Churn rate
- Feature usage

### Content metrics
- Views/impressions
- Engagement rate
- Click-through rate
- Follower growth

---

## Statistical significance calculator

For A/B tests, use this threshold:
- 95% confidence = statistically significant
- <95% = continue test or increase sample

Quick calculation:
- Sample size needed: ~1000 per variant for 5% baseline, 20% lift detection
- Duration: Usually 1-2 weeks minimum

---

## Monitoring sources

### Forums/communities to check
- r/SideProject
- r/startups
- r/Entrepreneur
- IndieHackers
- Product Hunt
- Hacker News

### Twitter accounts (from HIGH_SIGNAL_SOURCES)
- @levelsio (indie tactics)
- @dannypostmaa (growth experiments)
- @tdinh_me (technical marketing)
- @Hightrafficsite (SEO/traffic)

### Grey hat forums (carefully)
- BlackHatWorld (filter for legal tactics)
- GrowthHackers
- Warrior Forum

---

## Frequency

| Task | Frequency | Notes |
|------|-----------|-------|
| Revenue check | Daily | Quick glance |
| Content performance | Daily | What's working |
| A/B test check | Daily | Monitor progress |
| Full analysis | Weekly | Deep dive |
| Competitive intel | Weekly | What are they doing |
| Source scan | Daily | Part of /daily-research |

---

## Integration with daily research

This task should run in coordination with `ralph_tasks/00_daily_alpha_research.md`:

1. Daily research finds new tactics
2. This task evaluates current performance
3. Cross-reference: Which new tactics address current underperformance?
4. Prioritize implementations

---

## Guardrails

### Do NOT:
- Access live production data without permission
- Make changes without logging
- Skip statistical significance
- Ignore compliance in optimizations

### Always:
- Document everything
- Use data to drive decisions
- Flag urgent issues immediately
- Maintain historical records

---

## After Completion

1. Save report to `OPS/reports/[DATE]_performance.md`
2. Update `LEDGER/AB_TEST_LOG.csv`
3. Update `LEDGER/OPTIMIZATION_QUEUE.csv`
4. Update `.ralph/progress.md`

---

test_command: "ls OPS/reports/*_performance.md | wc -l"
