---
task: Generate landing page copy for PRINTMAXX apps
test_command: "find /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds -name 'LANDING_COPY.md' | wc -l"
---

# Task: Generate App Landing Page Copy

You are a Ralph loop iteration. Read this prompt fresh each time.

## First: Read These Files
1. `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/ralph/guardrails.md`
2. `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/.claude/rules/copy-style.md`

## Current State
Check `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/ralph/loops/landing_copy/state.md`

## Your Job This Iteration
1. Read state.md
2. Pick FIRST incomplete app
3. Write LANDING_COPY.md for that app
4. Save to app's build folder
5. Mark complete in state.md
6. Exit

## Apps to Write Copy For

### App 1: PrayerLock
- Path: `MONEY_METHODS/APP_FACTORY/builds/prayerlock/LANDING_COPY.md`
- Concept: Lock phone until prayer complete
- Niche: Faith/Christian productivity

### App 2: StepUnlock
- Path: `MONEY_METHODS/APP_FACTORY/builds/stepunlock/LANDING_COPY.md`
- Concept: Lock phone until steps walked
- Niche: Fitness/walking motivation

### App 3: LearnLock
- Path: `MONEY_METHODS/APP_FACTORY/builds/learnlock-sdk54/LANDING_COPY.md`
- Concept: Lock distracting apps during study
- Niche: Students/productivity

### App 4: BioMaxx
- Path: `MONEY_METHODS/APP_FACTORY/builds/biomaxx-sdk54/LANDING_COPY.md`
- Concept: Biohacking habits tracker
- Niche: Health optimization

### App 5: GlowMaxx
- Path: `MONEY_METHODS/APP_FACTORY/builds/glowmaxx-sdk54/LANDING_COPY.md`
- Concept: Skincare routine tracker
- Niche: Women's beauty/wellness

### App 6: DevotionFlow
- Path: `MONEY_METHODS/APP_FACTORY/builds/devotionflow-sdk54/LANDING_COPY.md`
- Concept: Daily devotional + journaling
- Niche: Faith/spiritual growth

## Copy Structure Required
```markdown
## Hero Section
- **Headline:** [under 10 words]
- **Subheadline:** [who + what, under 20 words]
- **CTA:** [action verb + outcome]

## Problem Section
- Pain 1
- Pain 2
- Pain 3

## Solution Section
- Step 1
- Step 2
- Step 3

## Features Section
- 5 feature bullets with benefits

## Pricing Section
- Free tier
- Premium: $X.99/mo

## FAQ Section
- 5 Q&As

## Final CTA
```

## Copy Rules
- No em dashes
- No AI vocabulary
- Specific numbers
- Sentence case headings
- @levelsio/@tdinh_me indie hacker tone

## When All Done
If all 6 apps complete, output: <promise>COMPLETE</promise>
