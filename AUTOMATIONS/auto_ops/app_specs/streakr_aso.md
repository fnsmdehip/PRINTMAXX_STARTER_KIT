# Streakr — ASO Package
**Generated:** 2026-04-04 | **Category:** Health & Fitness (primary), Productivity (alt)
**Bundle ID:** com.printmaxx.streakr | **Price:** Free (Subscription)

---

## App Name (30 chars max)
`Streakr: Habit Streak Tracker`

## Subtitle (30 chars max)
`Build streaks. Keep them alive.`

## Category
Primary: **Health & Fitness**
Secondary: **Productivity**

---

## Keywords (100 chars max — comma separated, no spaces after commas)
`habit,streak,tracker,daily,routine,challenge,minimum,viable,swipe,consistency,goal,check,day`

**Keyword rationale:**
- `habit` — 2.5M+ searches/mo on App Store
- `streak` — HabitSwipe, Streaks app dominate. We can rank #3-5 with reviews.
- `minimum viable` — zero apps own this term despite 307 upvotes on the concept
- `swipe` — differentiates vs generic habit apps, low competition
- `consistency` — high intent, low comp
- `challenge` — taps into "30 day challenge" search cluster

**Long-tail angles to own:**
- "swipe to complete habits"
- "minimum viable day tracker"
- "3 habit limit tracker"
- "simple streak counter no fluff"

---

## Description (4000 chars max)

### Short description (for preview / first 255 chars):
Streakr tracks your habits with one swipe. Set your Minimum Viable Day — the smallest version of each habit that still counts. Then swipe to complete. No fluff, no coaching, no guilt trips.

### Full description:

**Your habits. One swipe. Every day.**

Streakr is the simplest habit tracker you'll actually use. No daily coaching lectures. No gamification overload. Just your habits, a swipe, and a growing streak.

**What makes Streakr different:**

🔥 **Swipe to complete** — Tinder-style habit cards. Left to skip, right to log. One motion per habit.

📐 **Minimum Viable Day (MVD)** — Define the smallest version of a habit that still counts. On hard days, the minimum is enough. Streaks survive. Progress continues.

📅 **Streak history** — 30-day calendar heatmap per habit. See your consistency patterns at a glance.

🔔 **Daily reminder** — One notification at your chosen time. That's it.

🔒 **100% local** — Your habits stay on your device. No account required. No syncing to our servers. No privacy surprises.

**Built for people who hate habit apps:**

Most habit apps add so much friction that the app itself becomes the obstacle. Streakr removes everything except the one thing that matters: did you do it today?

Three free habits. Unlimited with Streakr Pro.

**Streakr Pro includes:**
- Unlimited habits
- Full MVD history
- Streak repair (miss a day but honor the effort)
- Milestone share cards

Try Pro free for 7 days. Cancel anytime.

---

**Common habits tracked in Streakr:**
Exercise, meditation, reading, journaling, cold shower, no alcohol, study, practice, hydration, walking, gratitude, coding, stretching, language learning, prayer, fasting, sleep schedule, and more.

---

## Screenshots Spec (6.5" iPhone — 1290×2796)

### Screen 1 — Hook
**Headline:** "One swipe. One win."
**Subtext:** "The habit tracker you'll actually open."
**Visual:** Card stack with "Morning Walk" at top, green swipe arrow, 14-day streak indicator

### Screen 2 — MVD Feature
**Headline:** "Define your minimum. Never break the chain."
**Subtext:** "On bad days, the minimum counts. Streaks survive."
**Visual:** MVD setup screen with "Full workout" vs "20 pushups" slider, "Both count" badge

### Screen 3 — Swipe UX
**Headline:** "Swipe to win. Or skip without shame."
**Subtext:** "No pop-ups, no nag screens. Just cards."
**Visual:** Animated swipe right on "Journaling" card → green checkmark

### Screen 4 — Calendar Heatmap
**Headline:** "See exactly where you show up."
**Subtext:** "30-day heatmap per habit. Green means done."
**Visual:** April calendar with 22/30 green cells

### Screen 5 — Privacy
**Headline:** "Your habits. Your phone. Nobody else's business."
**Subtext:** "No account. No cloud sync. 100% local storage."
**Visual:** Lock icon, "0 servers", "0 sign-ups" badges

### Screen 6 — Paywall
**Headline:** "7 days free. Then decide."
**Subtext:** "Most people pay less than $2.50/month annually."
**Visual:** Pricing comparison, "Annual $24.99/yr" highlighted

---

## Review Prompt Timing

Based on RF_005 alpha (score 125): +0.8 stars from timing change.

**Trigger conditions (StorReviewRequestAPI):**
- Day 3 OR Day 7 streak on any habit (whichever comes first)
- 2.5 second delay after milestone celebration animation completes
- 90-day cooldown after request
- `hasReviewedApp` guard: never prompt after user has tapped "Rate" once

**DO NOT prompt:**
- On first session open
- Immediately after paywall (Stripe webhook moment)
- During a habit card swipe animation

---

## Pricing Tests (A/B sequence)

**Test 1 (launch):** Annual $24.99/yr vs Monthly $4.99/mo
**Test 2 (30d):** Annual $19.99 vs Annual $24.99 (check churn difference)
**Test 3 (60d):** Weekly $1.99/wk A/B vs no weekly tier

**Hypothesis:** Annual-first display with 7-day trial will drive 3-4x more annual conversions vs monthly-first, per HabitSwipe conversion data.

---

## Competitor Gaps (from queue intel)

| App | Gap Streakr Fills |
|-----|-------------------|
| Fabulous | Way too complex, coaching overhead, no swipe |
| Streaks | No MVD, no swipe, no category presets |
| HabitSwipe | No iOS-native (web app), no trial, no free tier |
| Habitica | Gamification overkill, no minimalist mode |
| Done | No swipe, no MVD, paid upfront |

---

## Stripe Payment Links (HUMAN ACTION NEEDED)

Create in Stripe Dashboard → Payment Links:
1. `streakr-annual` — Recurring $24.99/yr, 7-day free trial, description: "Streakr Pro Annual"
2. `streakr-monthly` — Recurring $4.99/mo, no trial (or 3-day trial), description: "Streakr Pro Monthly"

Replace placeholder URLs in `src/screens/PaywallScreen.tsx:18-19`:
```
const STRIPE_ANNUAL = 'https://buy.stripe.com/REAL_ANNUAL_LINK';
const STRIPE_MONTHLY = 'https://buy.stripe.com/REAL_MONTHLY_LINK';
```

---

## Launch Sequence (post Stripe links)

1. `npx expo prebuild --platform ios` (clean native build)
2. `npx expo run:ios` (Simulator test — verify swipe, paywall, review prompt)
3. Screenshot all 6 screens in Simulator
4. `eas build --platform ios --profile production`
5. Submit to TestFlight
6. Post to r/SideProject, r/passive_income (same narrative as HabitSwipe post)
