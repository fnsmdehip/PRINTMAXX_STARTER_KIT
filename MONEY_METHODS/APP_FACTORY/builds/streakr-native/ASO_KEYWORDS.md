# Streakr — ASO Keywords, Metadata & Launch Strategy
## Generated: 2026-04-06

---

## App Store Metadata

### App Name (30 chars max)
`Streakr: Habit & Streak Tracker`

### Subtitle (30 chars max)
`Swipe to complete. Build more.`

### Keyword Field (100 chars max — comma-separated, no spaces after commas)
`habit,streak,tracker,yoga,hiit,pushup,plank,cycling,swipe,mvd,minimum,viable,consistency,routine`

---

## Primary Keywords (high intent, validated demand)

| Keyword | Search Volume | Competition | Priority |
|---------|--------------|-------------|----------|
| habit tracker | Very High | High | P0 |
| streak tracker | High | Medium | P0 |
| daily habits | High | High | P0 |
| habit app | High | High | P0 |
| streak counter | Medium | Low | P1 |
| swipe habit | Low | Very Low | P1 (own it) |
| habit streak | Medium | Low | P1 |
| daily routine app | Medium | Medium | P1 |
| minimum viable day | Low | Very Low | P1 (own it) |
| consistency tracker | Low | Low | P2 |
| habit checker | Low | Low | P2 |
| goal tracker | High | High | P2 |

---

## Secondary Keywords (broader)

- daily goal tracker
- healthy habits
- productivity streak
- habit building
- self improvement tracker
- routine builder
- streak app ios
- habit challenge tracker
- simple habit tracker
- accountability tracker

---

## Competitor Analysis

| App | Rating | Reviews | Gap |
|-----|--------|---------|-----|
| Streaks | 4.8 | 85K | Paid upfront, no swipe UX, no MVD mode |
| Habitify | 4.5 | 22K | Complex UI, no swipe, subscription heavy |
| Fabulous | 4.7 | 120K | Coaching-heavy, not lightweight |
| HabitSwipe | ~3.8 | 120 | Cross-platform, no MVD, no milestone cards |
| Habit Tracker | 4.4 | 31K | Generic, no swipe, no local-first |

**Our gap:** Swipe-to-complete UX + Minimum Viable Day framework + local-first (no account) + free 3-habit tier

---

## App Store Description (copy-ready)

**Tagline:** One swipe. One win. Build unstoppable habits.

**Short Description (80 chars):**
Swipe to complete habits. Define your minimum viable day. No account needed.

**Full Description:**

Streakr is the fastest, most satisfying habit tracker ever built.

**Swipe up to complete.** No tapping menus, no loading spinners. One swipe = one win. Feel the streak click into place with a haptic confirmation every time.

**Define your Minimum Viable Day (MVD).** Instead of tracking 10 habits and feeling guilty, define the 3 non-negotiables that make the day count. If you hit your MVD, it's a win — no matter what else happened.

**12 habit presets. 5 categories.**
- Health: drink water, exercise, sleep 7+ hours
- Focus: deep work block, no phone first hour
- Mind: meditation, journaling, reading
- Discipline: cold shower, early rise
- Custom: anything you want to build or quit

**Built for consistency, not complexity.**
- 3 habits free, forever
- Swipe-based completion (like Tinder for habits)
- MVD mode with clear win/loss indicator
- 30-day calendar heatmap per habit
- Milestone celebrations at day 3, 7, 14, 30, 60, 90
- Smart review prompts after you hit a milestone (never on session open)
- Zero account required, 100% local storage

**Streakr Pro — $24.99/year (7-day free trial)**
- Unlimited habits
- Full streak history
- Streak repair (1 per month)
- Share milestone cards

---

## Review Prompt Strategy

**Trigger:** Fire `StoreKit.requestReview()` exactly 2s after user hits a milestone (day 3 or 7 on any habit)
**Cooldown:** 90 days between prompts
**Guard:** Never fire if `hasReviewedApp === true`
**Message context:** User is in celebration mode, at peak satisfaction
**Expected outcome:** +0.8 stars vs session-open prompts (validated by RF_005 data)

---

## Screenshot Specs (6 screens, all required)

| # | Screen | Copy | Visual Focus |
|---|--------|------|-------------|
| 1 | TodayScreen swipe | "One swipe = one win" | Swipe animation on card |
| 2 | MVD mode active | "Define your minimum viable day" | 3 non-negotiables checked |
| 3 | Milestone celebration | "7-day streak 🔥" | Confetti + milestone card |
| 4 | Heatmap detail | "Track every day. See every win." | 30-day green calendar |
| 5 | Habit picker | "12 habits. 5 categories." | Category grid selection |
| 6 | Paywall | "Try free for 7 days" | Annual plan highlighted |

Screenshot background: warm ivory (#FAF7F2), emerald accent (#2D9B6C)

---

## Pricing Strategy

| Tier | Price | Trial | Notes |
|------|-------|-------|-------|
| Free | $0 | — | 3 habits, no history, no milestone cards |
| Annual | $24.99/yr | 7 days | Primary CTA, anchored first |
| Monthly | $4.99/mo | None | Available as escape valve, not promoted |

**Anchoring rule:** Annual is always listed first, with "Most Popular" badge. Monthly is below in smaller text with "cancel anytime" copy.

**A/B test queue:**
1. $19.99 vs $24.99 annual (2 weeks each)
2. Annual trial 7-day vs 3-day (after first 50 ratings)
3. Paywall position: after first habit created vs after first swipe check-in

---

## Launch Sequence

### Day 0 (App Store submission)
- Submit with "New App" flag
- Request featured consideration via App Store Connect form
- Post on r/passive_income: "Built a swipe-to-complete habit tracker because Streaks is $5 upfront and doesn't have MVD mode"

### Day 1-3 (Reddit seeding)
- r/getdisciplined: "I stopped tracking 10 habits and defined my Minimum Viable Day instead"
- r/productivity: Link to MVD concept thread (307 upvotes on the concept — ride the wave)
- r/selfimprovement: Focus on swipe UX vs tap-heavy alternatives

### Week 1 (Review gathering)
- Day 3: first in-app review prompts fire (milestone-triggered)
- Target: 20 reviews in week 1

### Week 2+ (ASO iteration)
- Check keyword ranking for "habit tracker" and "streak counter"
- A/B test screenshots based on conversion data
- If day-7 D7 retention > 40%, start paid UA at $10/day CPM on Instagram

---

## Affiliate Integration (post-retention only)

After user reaches day 30 streak on any "health" habit:
- Show contextual recommendation: "People with 30-day workout streaks often use these" → affiliate link
- Never before day 30, never on the home screen, never interrupt-style

Target programs: Whoop (wearables), Blinkist (reading), Calm (meditation), Athletic Greens (health)
Revenue estimate: $15-40/conversion at 1-3% CVR on milestone events

---

## EAS Build Config

```json
{
  "build": {
    "preview": {
      "distribution": "internal",
      "ios": { "simulator": true }
    },
    "production": {
      "ios": {
        "autoIncrement": true
      }
    }
  }
}
```

Command: `eas build --platform ios --profile preview` (TestFlight internal)
Then: `eas submit --platform ios` (App Store Connect)
