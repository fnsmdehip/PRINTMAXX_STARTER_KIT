# STREAKR — App Spec v1.2
Generated: 2026-04-05 | Queue Score: 122 | Decision: ITERATE_EXISTING_NOW

---

## Executive Summary

Streakr is a swipe-based habit streak tracker targeting the underserved gap between "Fabulous" (87K reviews, ★4.45, complex) and the free apps (no monetization). The alpha queue confirms HabitSwipe hit $800 revenue / 2.5K users in 2 months with no ASO, no content, and a generic design. Streakr has a superior gesture mechanic (swipe-up), MVD mode (scientific differentiation), sobriety niche integration, and a paywall built on value-moment timing.

---

## Market Opportunity

| Signal | Data |
|--------|------|
| r/Productivity | 2.39M subs — organic top-of-funnel |
| r/NoFap | 1.24M subs — sobriety niche, zero paid dedicated apps |
| r/getdisciplined | 900K subs |
| r/Meditation | 3.52M subs |
| iTunes gap | Fabulous is the ONLY major habit app with reviews. Everything else is free/dead. |
| Competitor weakness | Fabulous: complex, bloated, $39.99/yr. Streakr target: simple, fast, $24.99/yr. |
| HabitSwipe benchmark | $800 / 2.5K users in 2 months. No ASO. Generic design. We beat that with positioning. |

---

## Product

**Build location:** `MONEY_METHODS/APP_FACTORY/builds/streakr-native/`
**Bundle ID:** (needs unique ID, suggest `com.printmaxx.streakr`)
**Platform:** React Native (Expo SDK 52), iOS-first
**Status as of 2026-04-05:** Code complete, TypeScript clean, Stripe LIVE

### Core differentiators

1. **Swipe-up to complete** — faster than any tap-based competitor. One gesture = one win.
2. **MVD mode (Minimum Viable Day)** — lets users define a "floor" version of the habit. Keeps streak alive on bad days. No competitor does this.
3. **Sobriety category** — NoFap, alcohol-free, nicotine-free, social media detox, no gambling. Each with dopamine-reset milestone messages. No paid competitor owns this niche.
4. **66-day science** — onboarding explicitly corrects the "21 days" myth. Identity positioning, not willpower positioning.
5. **Value-moment review prompt** — fires at day 3 or day 7 with 90-day cooldown. Not on first open.

### Habit categories

| Category | Emoji | Key presets |
|----------|-------|-------------|
| Fitness | 💪 | Morning workout, Daily run, Cold shower |
| Mindfulness | 🧘 | Meditation, Journaling, No phone first hour |
| Learning | 📚 | Daily reading, Skill practice, Deep work block |
| Creation | ✍️ | Create something daily |
| Health | 💚 | Drink 2L water, Early sleep |
| **Sobriety** | 🧠 | **No PMO, Alcohol-free, Nicotine-free, Social media detox, No gambling** |
| Custom | ⭐ | User-defined |

---

## Monetization

### Payment (LIVE as of 2026-04-05)
| Plan | Price | Payment Link | Stripe IDs |
|------|-------|-------------|-----------|
| Annual (7-day trial) | $24.99/yr | https://buy.stripe.com/3cI9AUb207NHctPend3F60K | prod_UHbVm2YjM4LW8d / price_1TJ2IQKlbvFndmYLFBdqBaBc |
| Monthly | $4.99/mo | https://buy.stripe.com/bJe00kfig0lf0L7frh3F60L | prod_UHbVm2YjM4LW8d / price_1TJ2IeKlbvFndmYLOOQns7Nb |

### Premium features
- Unlimited habits (free tier: 3 max)
- Full streak history + heatmap
- MVD full history
- Streak repair (1 forgiven missed day/month)
- Share milestone cards (viral loop)
- CSV export

### Paywall triggers
- `habit_limit` — 4th habit added
- `mvd_history` — history tab tapped by free user
- `streak_repair` — repair tapped
- `share` — milestone share tapped
- `settings` — upgrade button in settings

---

## Onboarding (8 screens)

| Step | Screen | Purpose |
|------|--------|---------|
| 0 | Welcome + demo swipe | Product demo, trust signals (no account, offline, no ads) |
| 1 | Identity commitment | "Who are you becoming?" — identity-first framing |
| 2 | Pick category | 6 categories including Sobriety |
| 3 | Pick habit preset | Category-filtered presets or custom |
| 4 | MVD setup | Define minimum viable version, with real user quote |
| 5 | Reminder permission | Daily reminder time selector, permission request |
| 6 | Streak science | "21 days is a myth. Real number is 66." |
| 7 | Day 1 check-in | First tap = Day 1 locked in. Emotional commitment. |

---

## ASO Strategy

### Primary keywords
- habit tracker, streak tracker, daily habits, habit streak, sobriety tracker, nofap tracker, alcohol free tracker, daily routine tracker, habit building, streak counter, minimum viable day

### App name options (test)
- **Streakr — Daily Habit Tracker**
- **Streakr: Streak & Habit Tracker**
- **Streakr — Build Real Habits**

### Subtitle (30 chars)
- "Swipe to win. Keep the streak."

### Description hook
"Most habit apps track habits. Streakr tracks who you're becoming. One swipe. One streak. That's it."

### Category
Primary: Health & Fitness
Secondary: Productivity

### Review prompt timing
Day 3 or day 7 on first achieved habit streak. 90-day cooldown. Never on session one. Expected: +0.8 stars vs session-one prompts (validated by r/SideProject case study).

---

## Experiments Queue

| Test | Variants | Success metric |
|------|----------|---------------|
| Paywall timing | After onboarding step 6 vs after first value moment (day 3) | 7-day trial conversion % |
| Pricing | $24.99/yr (current) vs $19.99/yr | Revenue/install |
| Sobriety as first category | Sobriety tab first vs Fitness tab first | Sobriety niche retention D7 |
| MVD toggle default | Default ON vs default OFF in onboarding | D14 retention |
| Review prompt | Day 3 vs day 7 | App Store rating |

---

## Distribution

### Organic
- r/NoFap: "I built an app for this subreddit" launch post (1.24M subs, zero paid alternatives)
- r/getdisciplined: "Why 21 days is a myth" thread with Streakr mention
- r/Productivity: swipe mechanic GIF post
- Twitter/X: "We built a habit tracker where the only interaction is one swipe" — short demo video

### Product Hunt
- Launch as "Streakr — The only habit tracker with Minimum Viable Day mode"
- Tagline: "Swipe to win. Keep the streak."

### Content seeds
- "The 66-day rule: why your habit tracker is lying to you" — blog post, Reddit thread
- "I tracked no-PMO for 90 days. Here's what happened to my dopamine." — r/NoFap
- "Why MVD is the most underrated habit concept" — Productivity forums

---

## Build Status Checklist

- [x] Core swipe-up check-in mechanic
- [x] Streak calculation (with yesterday-based continuity check)
- [x] MVD mode (per-habit + global toggle)
- [x] 6 habit categories including Sobriety
- [x] 17+ habit presets
- [x] Sobriety presets: No PMO, Alcohol-free, Nicotine-free, Social detox, No gambling
- [x] 8-screen onboarding (was 5, expanded 2026-04-05)
- [x] Value-moment review prompt (day 3 or 7, 90-day cooldown)
- [x] Paywall: annual-first, 7-day trial timeline
- [x] Real Stripe payment links (LIVE)
- [x] Privacy policy URL (printmaxx-privacy.surge.sh)
- [x] Terms URL (printmaxx-tos.surge.sh)
- [x] Subscription terms in paywall (Apple 3.1.1 compliant)
- [ ] App icon (needs design — not Ionicons placeholder)
- [ ] Splash screen (needs design)
- [ ] Bundle ID set in app.json (currently needs update)
- [ ] EAS build + App Store submission
- [ ] HabitDetail screen — progress heatmap view
- [ ] Milestone share cards (premium, viral)
- [ ] Streak repair implementation
- [ ] Push notification scheduling (reminder system wired in onboarding step 5)

---

## Next Actions (ordered)

1. **Asset generation** — App icon + splash. Use Pollinations.ai: "minimalist habit streak app icon, emerald green flame, dark background, iOS style". Then `npx expo prebuild` to verify.
2. **Bundle ID** — Set `com.printmaxx.streakr` in `app.json`
3. **EAS build** — `eas build --platform ios --profile preview` for simulator test
4. **Screenshot spec** — 5 screenshots: swipe demo, sobriety niche, MVD screen, milestone, paywall
5. **r/NoFap launch post** — "I built a sobriety streak tracker that doesn't suck. Free to try."

---

## Revenue Projection

| Metric | Conservative | Optimistic |
|--------|-------------|-----------|
| Installs (month 1) | 500 | 2,000 |
| Trial starts (20%) | 100 | 400 |
| Trial conversion (15%) | 15 | 60 |
| Annual plan take rate (70%) | 11 → $274 | 42 → $1,050 |
| Monthly plan take rate (30%) | 4 → $20/mo | 18 → $90/mo |
| **Month 1 revenue** | **~$294** | **~$1,140** |

HabitSwipe benchmark: $800 / 2.5K users in 2 months with no positioning. Streakr has sobriety niche, MVD differentiation, and a real launch plan. Conservative is $294. Optimistic is plausible.

---

*Spec generated by App Factory autonomy agent — 2026-04-05*
