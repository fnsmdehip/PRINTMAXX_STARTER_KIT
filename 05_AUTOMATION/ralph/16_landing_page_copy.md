# Ralph Task: Landing Page Copy

Generate landing page copy for all PRINTMAXX apps.

---

## Context
- Read `.claude/rules/copy-style.md` for content rules
- Read `ralph/guardrails.md` before starting
- Output LANDING_COPY.md to each app's build folder
- Indie hacker tone: @levelsio, @tdinh_me style

## Success Criteria

### PrayerLock
1. [ ] LANDING_COPY.md in `MONEY_METHODS/APP_FACTORY/builds/prayerlock/`
2. [ ] Hero: headline under 10 words
3. [ ] 3 pain points
4. [ ] 3 simple steps
5. [ ] 5 feature bullets
6. [ ] Pricing section
7. [ ] 5 FAQs

### StepUnlock/WalkToUnlock
8. [ ] LANDING_COPY.md in `MONEY_METHODS/APP_FACTORY/builds/stepunlock/`
9. [ ] All sections complete

### LearnLock/StudyLock
10. [ ] LANDING_COPY.md in `MONEY_METHODS/APP_FACTORY/builds/learnlock-sdk54/`
11. [ ] All sections complete

### BioMaxx
12. [ ] LANDING_COPY.md in `MONEY_METHODS/APP_FACTORY/builds/biomaxx-sdk54/`
13. [ ] All sections complete

### GlowMaxx
14. [ ] LANDING_COPY.md in `MONEY_METHODS/APP_FACTORY/builds/glowmaxx-sdk54/`
15. [ ] All sections complete

### DevotionFlow
16. [ ] LANDING_COPY.md in `MONEY_METHODS/APP_FACTORY/builds/devotionflow-sdk54/`
17. [ ] All sections complete

### Completion
18. [ ] LANDING_COPY_COMPLETE.md in builds folder
19. [ ] All 6 apps have landing copy

## Copy Structure

```markdown
## Hero Section
- **Headline:** [under 10 words]
- **Subheadline:** [who + what, under 20 words]
- **CTA Button:** [action verb + outcome]

## Problem Section
- Pain 1 [specific]
- Pain 2 [specific]
- Pain 3 [specific]

## Solution Section
- Step 1: [how it works]
- Step 2: [how it works]
- Step 3: [how it works]

## Features Section
- Feature 1 + benefit
- Feature 2 + benefit
- Feature 3 + benefit
- Feature 4 + benefit
- Feature 5 + benefit

## Pricing Section
- Free tier
- Premium: $X.99/mo or $XX.99/yr

## FAQ Section
- Q1 + A1
- Q2 + A2
- Q3 + A3
- Q4 + A4
- Q5 + A5

## Final CTA
[urgency + clear action]
```

## Constraints
- No em dashes
- No AI vocabulary
- Specific numbers
- Sentence case headings
- Direct, confident tone

## After Completion
- Update `ralph/progress.md`

---

test_command: "find MONEY_METHODS/APP_FACTORY/builds -name 'LANDING_COPY.md' | wc -l"
expected_output: "6"
