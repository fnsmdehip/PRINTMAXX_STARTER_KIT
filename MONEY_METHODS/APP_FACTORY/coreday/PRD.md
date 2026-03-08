# CoreDay — Product Requirements Document

**Generated:** 2026-03-08
**Agent Cycle:** APP_FACTORY autonomy cycle
**Signal Source:** Reddit r/productivity (307 upvotes, 42 comments) + HabitSwipe $800/2mo validated

---

## Problem

Habit trackers fail because they optimize for tracking, not success. Users add 8-12 habits, miss one day, feel like failures, abandon the app.

Reddit signal (307 upvotes): *"I stopped tracking 10 habits and started defining a 'minimum viable day.' It's working better than I expected."*

The pain: no app is built around this insight. Existing apps (HabitForge, Streaks, Habitica) all encourage MORE habits.

---

## Solution

CoreDay. Pick your 3 non-negotiables. If you do all 3, it's a **Win Day**. That's it.

No 10-habit grids. No complicated scoring. No overwhelm. Just 3 things that define a successful day, tracked with a streak.

---

## Target User

- Productivity-interested 25-40yo (r/productivity, r/getdisciplined demographic)
- Burned out on complex habit trackers
- Wants something they'll actually stick with
- iOS/Android/PWA — mobile-first

---

## Core Features (v1.0)

### Free Tier
1. **Onboarding** — Set your 3 "cores" with emoji + custom name
2. **Today screen** — 3 large tap targets, one per core. Tap to complete.
3. **Win Day animation** — Satisfying celebration when all 3 are checked
4. **Streak tracker** — Days in a row with all 3 cores complete
5. **30-day calendar heatmap** — Green = Win Day, grey = not yet, dark = missed
6. **Stats** — Current streak, best streak, win% this month
7. **Reminders** — Optional daily push notification (PWA notifications)
8. **Offline-first** — Full functionality, no network needed

### Pro Tier ($2.99/mo or $9.99 one-time)
1. **4th and 5th core** — For people who want slightly more
2. **Notes per day** — Add a 1-sentence reflection to each day
3. **90-day heatmap** — Longer history view
4. **Data export** — CSV export of all log data
5. **Custom colors** — Change the accent color

---

## Monetization

- **Free**: 3 cores, 30-day history, basic stats
- **Pro**: $2.99/month via Stripe (future) or $9.99 one-time
- **MVP**: Pro gate with "coming soon" modal + email capture (validate demand before building payment)
- **Affiliate**: Link to productivity books/tools in settings (Amazon affiliate)

---

## Tech Stack

- Single-file PWA (HTML/CSS/JS + manifest.json + sw.js)
- LocalStorage for all data (no backend, zero cost)
- Surge.sh deployment (instant, free)
- Plausible analytics (privacy-first, lightweight)

---

## Quality Bar

Must match or beat top-10 in "habit tracker" category:
- Streaks app (iOS): clean, daily check-in, beautiful
- Habitica: gamified but overcomplicated
- HabitSwipe: minimal, swipe-based
- **CoreDay wins by**: being the ONLY app that tells you to track LESS

---

## Launch Plan

1. Deploy to coreday.surge.sh
2. Post to r/productivity: "I built the 'minimum viable day' concept as an app" (not promotional, show the tool)
3. Post to r/getdisciplined, r/selfimprovement
4. Twitter thread: "I built an anti-habit-tracker. Here's why" (link HabitSwipe as validation)
5. Product Hunt launch (build backlog of early users first)
6. SEO: "minimum viable day app", "3 habits per day app", "anti habit tracker"

---

## Success Metrics

- 100 users in 7 days (Reddit launch)
- 500 users in 30 days
- 10 Pro conversions at day 30 ($30-100/mo initial)
- App Store listing when PWA is validated

---

## Competitive Positioning

> "The only habit tracker that tells you to track less."

Every competitor adds features. CoreDay subtracts them. This is the angle.
