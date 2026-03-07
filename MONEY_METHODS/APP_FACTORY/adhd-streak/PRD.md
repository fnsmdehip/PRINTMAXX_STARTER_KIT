# ADHD-Streak — Product Requirements Document

**Date:** 2026-03-07
**Category:** Health & Fitness / Productivity
**Target keyword:** "ADHD habit tracker" (rapidly rising, very low competition)
**Build time:** 1 session
**Deploy target:** adhd-streak.surge.sh

---

## The Gap

Habit trackers are built for neurotypical brains. They punish missing a day with a full streak reset.
ADHD brains can't sustain perfect daily execution — dopamine system is dysregulated, time blindness is real.
r/ADHD (1.2M members) has hundreds of posts: "I hate how my streak reset after one day and I quit entirely."

No top-10 habit tracker is ADHD-first. Forest, Habitica, Streaks — all neurotypical models.

---

## Target User

- ADHD-diagnosed adults (18-35 primary)
- ADHD-suspected but undiagnosed ("late-diagnosed ADHD" = viral search term)
- Parents tracking habits for ADHD kids
- Search terms: "ADHD habit tracker", "ADHD planner app", "ADHD routine", "ADHD productivity"

---

## Core Differentiators

### 1. Flex Streaks (no hard resets)
- Daily habit: miss 1 day = "stumble" (streak paused, not reset). Miss 2 = reset.
- Weekly habit (3x/wk): miss the goal by 1 = stumble. Miss 2 weeks = reset.
- Shows "Flex Streak" in purple, stumbles in amber. Never shows zero for one bad day.

### 2. Body Double Timer
- 25-min focus session with ambient background sounds
- "Working alongside 847 other ADHDers right now" (social proof even if static)
- Completion logs automatically to selected habit

### 3. Variable Dopamine Rewards
- Random celebration animations on check-in (not every time = variable ratio = dopamine spike)
- Celebration styles: confetti, stars, fire, streak milestone badges
- "Hyperfocus unlocked" special badge for completing 3+ habits in one day

### 4. Habit Frequency = Flexible
- Options: daily, 5x/week, 3x/week, 2x/week, weekly
- No more "I set it to daily and failed" — match the goal to real capacity

---

## Screens

1. **Home** — Habit list with one-tap check-in, streak counts, today's progress bar
2. **Add Habit** — Name, emoji, frequency, color (4 steps max)
3. **Body Double** — Focus timer, ambient sounds selector, habit auto-log on complete
4. **Stats** — Per-habit calendar heatmap, completion %, stumble count
5. **Settings** — Pro upgrade, notification toggle, theme

---

## Monetization

- **Free:** 3 habits, basic streaks, body double (limited)
- **Pro ($3.99/mo or $29.99/yr):** Unlimited habits, full body double + ambient sounds, calendar heatmap, stumble insurance (2 stumbles/month don't count), widgets spec
- **Affiliate links:**
  - Focusmate (body doubling service) — affiliate program available
  - Sunsama (ADHD-friendly daily planner) — affiliate
  - "ADHD Skills" Notion template on Gumroad ($9 — our own product)

---

## ASO Keywords

Primary: ADHD habit tracker, ADHD planner, ADHD productivity, ADHD routine builder
Secondary: habit tracker ADHD, streak tracker, flexible habit tracker, neurodivergent planner
Long-tail: habit tracker that doesn't reset, ADHD streak, ADHD daily routine app

---

## Success Metrics

- 100 PWA installs in 30 days (organic, Reddit r/ADHD post)
- 5% conversion to Pro email waitlist
- 3 affiliate clicks/day
- Target: $200/mo within 60 days
