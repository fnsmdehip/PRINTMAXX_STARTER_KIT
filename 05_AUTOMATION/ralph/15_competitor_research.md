# Ralph Task: Competitor Research

Research competitors for all app categories.

---

## Context
- Use web search for current data
- Output to `MONEY_METHODS/APP_FACTORY/research/`
- Include specific revenue numbers where available
- Focus on gaps we can exploit

## Success Criteria

### Screen Time/Focus Apps (screen_time_competitors.md)
1. [ ] Research: Opal, One Sec, Freedom, Forest, BePresent
2. [ ] Revenue estimates for each
3. [ ] Pricing breakdown
4. [ ] Key features list
5. [ ] Gaps identified

### Prayer/Faith Apps (prayer_app_competitors.md)
6. [ ] Research: Hallow, Pray.com, Abide, Glorify, Click To Pray
7. [ ] Revenue estimates
8. [ ] Pricing and subscription models
9. [ ] Feature comparison
10. [ ] Positioning opportunities

### Fitness/Walking Apps (fitness_app_competitors.md)
11. [ ] Research: StepBet, Sweatcoin, Charity Miles, Paceline
12. [ ] Revenue and business models
13. [ ] Gamification mechanics
14. [ ] Weaknesses to exploit

### Study/Productivity Apps (study_app_competitors.md)
15. [ ] Research: Forest, Flora, Flipd, Cold Turkey
16. [ ] Target audience differences
17. [ ] Pricing comparison
18. [ ] Feature gaps

### Women's Health Apps (womens_health_competitors.md)
19. [ ] Research: Flo, Clue, Natural Cycles, Glow
20. [ ] Revenue and user counts
21. [ ] Privacy approaches
22. [ ] Monetization strategies

### Completion
23. [ ] RESEARCH_COMPLETE.md with key insights summary
24. [ ] All 5 research files created

## File Format

```markdown
---
category: [category name]
researched_date: 2026-01-24
our_app: [which PRINTMAXX app competes]
---

## Market Overview
- TAM size
- Growth trends

## Competitor Analysis

### 1. [App Name]
- **Revenue Estimate:** $X/mo
- **Pricing:** Free / $X.99/mo
- **Rating:** X.X stars
- **Key Features:** [list]
- **Weakness:** [gap to exploit]

## Opportunity Analysis
- Gaps in market
- Recommended differentiation
```

## Constraints
- Specific numbers required
- Source data where possible
- Focus on actionable insights

## After Completion
- Update `ralph/progress.md`

---

test_command: "ls MONEY_METHODS/APP_FACTORY/research/*.md | wc -l"
expected_output: "6"
