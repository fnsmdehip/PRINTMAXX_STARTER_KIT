---
task: Research competitors for PRINTMAXX app categories
test_command: "ls /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/research/*.md | wc -l"
---

# Task: Competitor Research

You are a Ralph loop iteration. Read this prompt fresh each time.

## First: Read
1. `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/ralph/guardrails.md`

## Current State
Check `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/ralph/loops/competitor_research/state.md`

## Your Job This Iteration
1. Read state.md
2. Pick FIRST incomplete category
3. Research competitors using web search
4. Write research file
5. Mark complete in state.md
6. Exit

## Categories to Research

### Category 1: screen_time_competitors.md
Research: Opal, One Sec, Freedom, Forest, BePresent
- Revenue estimates
- Pricing
- Key features
- Gaps to exploit
Save to: `MONEY_METHODS/APP_FACTORY/research/`

### Category 2: prayer_app_competitors.md
Research: Hallow, Pray.com, Abide, Glorify, Click To Pray
- Revenue estimates
- Subscription models
- Feature comparison

### Category 3: fitness_app_competitors.md
Research: StepBet, Sweatcoin, Charity Miles, Paceline, Achievement
- Business models
- Gamification mechanics
- User counts

### Category 4: study_app_competitors.md
Research: Forest, Flora, Flipd, Cold Turkey, LeechBlock
- Target audiences
- Pricing strategies
- Feature gaps

### Category 5: womens_health_competitors.md
Research: Flo, Clue, Natural Cycles, Glow, Period Tracker
- Revenue and users
- Privacy approaches
- Monetization

## File Format
```markdown
---
category: [name]
researched_date: 2026-01-24
our_app: [which PRINTMAXX app]
---

## Market Overview
- TAM
- Trends

## Competitor Analysis

### 1. [App Name]
- **Revenue:** $X/mo
- **Pricing:** Free / $X.99
- **Rating:** X.X stars
- **Features:** [list]
- **Weakness:** [gap]

## Opportunity Analysis
- Market gaps
- Differentiation strategy
```

## Research Rules
- Use web search for current data
- Specific numbers required
- Focus on actionable gaps

## When All Done
If all 5 categories complete, output: <promise>COMPLETE</promise>
