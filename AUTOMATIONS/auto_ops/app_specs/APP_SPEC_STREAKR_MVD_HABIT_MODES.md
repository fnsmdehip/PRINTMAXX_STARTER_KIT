# Streakr — Minimum Viable Day + Multi-Habit Mode Spec

**Priority queue score:** 122 (ITERATE_EXISTING_NOW)
**Source signals:**
- HabitSwipe $800 revenue, 2.5K users in 2 months (verified alpha)
- Minimum Viable Day: 307 upvotes on r/SideProject
- Fabulous competitor gap: 87K reviews, ★4.45 — only major habit app below 4.5 stars
- NoFap/sobriety already built as standalone (SoberStreak) — Streakr serves different users: general habit builders

**Decision:** Streakr should NOT duplicate SoberStreak. Position Streakr as the "positive habit builder" (Streakr = build streaks) while SoberStreak is the "breaking bad habits" app. They serve different intent queries.

---

## Feature 1: Minimum Viable Day (MVD) Mode

### What it is
The "Minimum Viable Day" concept went viral (307 upvotes): define the absolute minimum version of each habit that still counts as completing it. Instead of "30-minute workout" the MVD is "put on gym shoes and do 1 pushup." The streak counts as long as the MVD is met.

### Why it converts
- Removes the "I didn't do my full routine so I'll skip entirely" failure mode
- Builds consistent habit identity over perfect execution
- Differentiation from Fabulous (which has rigid routines that trigger perfectionism)

### Implementation
```
HabitConfig {
  name: string           // "Morning workout"
  fullGoal: string       // "30-minute workout"
  mvd: string            // "Put on gym shoes. Do 1 pushup."
  mvdEmoji: string       // "👟"
  streak: number
  checkInMode: 'full' | 'mvd' | null  // today's log
}
```

Check-in flow:
1. User taps "Check In" for a habit
2. App asks: "Full goal or MVD today?"
   - **Full goal** → Green checkmark, +1 full day count
   - **MVD** → Teal checkmark, +1 streak (doesn't break), increments mvdDays counter
   - **Skip** → Streak breaks
3. Stats show: `streak: 14 (11 full, 3 MVD)`

### ASO Impact
Keyword: "minimum viable day app" — no dedicated apps. Could own this keyword.

---

## Feature 2: Multi-Mode Habit Types

Current Streakr (web landing page only) needs native screens. Build with these 6 habit modes:

| Mode | Target Niche | Community | Pricing Signal |
|------|-------------|-----------|----------------|
| `focus` | Deep Work / Focus blocks | r/productivity 3M | $2.99 |
| `fitness` | Daily movement | r/fitness 10M | $1.99 |
| `reading` | Daily reading | r/books 23M | $1.99 |
| `meditation` | Daily meditation | r/meditation 3.5M | $2.99 |
| `journal` | Daily journaling | r/journaling 500K | $1.99 |
| `learning` | Skill practice | r/learnprogramming 6M | $2.99 |

Each mode has:
- Mode-specific daily prompts (not generic)
- Mode-specific milestone messages
- MVD presets per mode (pre-filled, user can edit)

---

## Feature 3: 7-Day Trial Paywall Framework

Alpha signal: "7-day trial = 5x conversion lift (2% to 11%)."

Current Streakr has no paywall. Implement:

```
Free tier:
  - 1 habit (any mode)
  - Basic streak counter
  - Check-in reminder

Premium ($19.99/yr, 7-day trial):
  - Unlimited habits
  - MVD mode
  - Milestone celebrations
  - Habit insights (which day of week you most often skip)
  - Export data
```

Paywall trigger: After user creates 2nd habit, show paywall.
NOT on launch, NOT during onboarding.

---

## Onboarding (12 screens, Cal AI model)

1. Welcome — "Build the habits that build you"
2. Choose first habit + mode
3. Set your goal (full goal)
4. Set your MVD — "What's the minimum that still counts?"
5. Why does this habit matter? (anchors motivation)
6. Schedule: When do you want to do this?
7. Reminder time
8. Streak milestone preview (Day 7, 30, 100)
9. "Streakr doesn't judge MVD days. Done is done." — key differentiator screen
10. Stats preview (mock 30-day view)
11. Paywall (7-day trial, annual-first)
12. Completion — "Your first streak starts today"

---

## Build Priority

**Phase 1 (this cycle):** Core native app shell
- Today screen: shows habit list + check-in buttons
- MVD check-in flow (the key differentiator)
- Storage service (local-first)
- Basic onboarding (12 screens)

**Phase 2 (next cycle):** Paywall + notifications
- 7-day trial paywall after 2nd habit
- Push notifications
- ASO screenshots

**Phase 3:** Insights
- Weekly analytics
- Habit skip pattern detection

---

## Differentiation vs Fabulous (★4.45, 87K reviews)

Fabulous weakness: "Too rigid, heavy paywall, feel guilty when I miss" (top complaint pattern)

Streakr positioning: "Streakr doesn't demand perfection. Define your minimum. Show up anyway. The streak is yours."

This is a genuine, testable product difference — not marketing copy.

---

## Pricing (validated)
- Annual: $19.99 / year (7-day free trial) — position above HabitSwipe
- Monthly: $4.99 / month
- No weekly plan (habit app users have longer intent horizon)

## Files to Create
- `MONEY_METHODS/APP_FACTORY/builds/streakr-native/` — full Expo app
- Target: next 12h cycle

## ASO Keywords
- habit streak tracker
- daily habit app
- minimum viable day
- streak counter habits
- habit builder app ios
- daily routine tracker
- streak motivation app
