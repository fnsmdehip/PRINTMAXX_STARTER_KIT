# Streakr — MVD Upgrade Spec (2026-04-07)
## Status: BUILT | Score: 122 | Market: HIGH

## Source Intelligence
- RF_006: "Minimum Viable Day" concept — 307 upvotes in r/productivity. Highest-engagement post across all scrapes.
- RF_002: HabitSwipe ($800, 2.5K users, 2 months) — swipe-based UX confirmed as differentiator
- ALPHA103106: r/NoFap (1.24M subs) + sobriety niche — zero paid dedicated streak apps

## What Was Upgraded (2026-04-07 session)

### 1. MVD Day Won Banner (RF_006 implementation)
**File:** `src/screens/TodayScreen.tsx`
**What:** Distinct intermediate win state that fires when all MVD-enabled habits are checked in, even if non-MVD habits remain incomplete.
**Why this matters:** The viral Reddit post's core insight is psychological — the day "counts" when your minimum viable version is done. The previous `allDoneToday` binary was all-or-nothing and caused guilt on partial completion days.

Logic added:
```typescript
const mvdHabits = habits.filter(h => h.mvdEnabled);
const mvdDayWon = mvdHabits.length > 0 && mvdHabits.every(h => isCheckedInToday(h)) && !allDoneToday;
```

Banner: Gold/amber styling, trophy emoji, shows "X non-negotiables done. Y bonus habits left if you want them."

### 2. Sobriety Category Added to AddHabitScreen
**File:** `src/screens/AddHabitScreen.tsx`
**What:** Added `{ label: 'Sobriety', value: 'sobriety', emoji: '🧠' }` to CATEGORIES array.
**Why:** The sobriety presets (NoFap/PMO, Alcohol-free, Nicotine-free, Social media detox, No gambling) existed in `src/constants/habits.ts` but the category chip was missing from the UI — users couldn't navigate to these presets.

## What Was Already Built (Prior Sessions)

### Swipe UX
- PanResponder swipe-up gesture (45px threshold, 40px drift max)
- Bounce-back animation on partial swipe
- Fly-up + fade animation on confirmed check-in
- Already matches HabitSwipe's differentiating interaction pattern (RF_002)

### MVD Per-Habit (Full Implementation)
- `Habit.mvdEnabled` + `Habit.mvdLabel` in types
- AddHabitScreen: toggle + text input for MVD label per habit
- Each preset in `habits.ts` has a pre-filled `mvdLabel` (e.g., "Do 5 pushups" for Morning Workout)
- MVD pill badge on habit card shows when mvdEnabled and not yet done

### Sobriety Presets (habits.ts)
- `No PMO` with NoFap-specific milestone messages (3d/7d/14d/30d/90d/180d/365d)
- `Alcohol-free`, `Nicotine-free`, `Social media detox`, `No gambling`
- Milestone messages use science-backed language (dopamine reset, lung function, etc.)

### Review Prompts (value-moment timing)
- Day 3 or Day 7 milestone only — never on first session
- 90-day cooldown gate
- iOS: `StoreReview.requestReview()` via expo-store-review

### Payment
- Stripe payment links via `app.json` extra config
- Free limit: 3 habits max
- Premium: unlimited habits + streak repair

## Compile Status
- `npx tsc --noEmit` → CLEAN (0 errors) on both Streakr-native and SoberStreak-native

## ASO Targets
- Primary keywords: "habit tracker", "streak tracker", "daily habits app"
- Secondary: "nofap tracker", "sobriety streak", "minimum viable day"
- Category: Health & Fitness
- Price test: Free + $2.99/mo or $19.99/yr

## Next Actions (Human Required)
1. EAS Build: `eas build --platform ios --profile production` (requires Apple Developer account)
2. App Store Connect: Create listing with ASO-optimized description
3. Screenshot set: 6 screens (Today, MVD Won state, Paywall, Sobriety presets, Habit Detail, Settings)

## Revenue Projection
- Month 1: 100 downloads → 5% convert = 5 premium × $2.99 = $15/mo (baseline)
- Month 3: Cross-post "built for myself" narrative on r/productivity, r/NoFap, r/habits → 500+ downloads → $75/mo
- Month 6 at scale: 2K downloads/mo × 5% × $2.99 = $300/mo
