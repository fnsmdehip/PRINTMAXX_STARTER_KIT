# RunningStreak Native — App Spec
**Decision:** BUILD_NEW | Score: 112 | Source: queue item RF_006
**Template base:** streakr-native (fork + specialize)
**Bundle ID:** com.printmaxx.runningstreak
**Category:** Health & Fitness | **Price:** Free + $19.99/yr

---

## Market Gap (verified)

- r/running: 4.19M subscribers
- iTunes scan: ZERO dedicated paid running streak apps
- Only competitor: Streaks ($5.99 one-time, generic) — not running-specific
- No swipe UX, no MVD, no running-specific data fields in any top result
- HabitSwipe = generic, no run data (distance, pace, conditions)

**Opportunity:** Own "running streak" keyword with a dedicated, running-specific app. $1.99 launch price undercuts Streaks.

---

## Core Differentiators vs Streakr

| Feature | Streakr | RunningStreak |
|---------|---------|---------------|
| Habit type | Any habit | Running ONLY |
| Data logged | Check-in | Distance + time + conditions |
| Milestones | Day 3, 7, 30 | 5K, 10K, 100K lifetime miles |
| MVD | Generic | "Run at least 1 mile" minimum |
| Leaderboard | No | Anonymous weekly leaderboard |
| Pace tracking | No | Avg pace per run |

---

## Build Approach

**Base:** Fork `streakr-native/` → replace multi-habit model with single-habit running model.

### File changes from Streakr template:

1. **`app.json`** — name: "RunningStreak", slug: "runningstreak", bundle: com.printmaxx.runningstreak, backgroundColor: "#001a00"

2. **`src/types/index.ts`** — Replace `Habit[]` with `RunEntry` model:
```typescript
interface RunEntry {
  id: string;
  date: string;         // YYYY-MM-DD
  distanceMiles: number;
  durationMinutes: number;
  paceMinPerMile: number;  // computed: duration/distance
  conditions: 'great' | 'tough' | 'minimum';  // MVD: minimum = just a mile, still counts
  notes?: string;
}
```

3. **`src/services/storage.ts`** — CRUD for RunEntry[], streak calculation: consecutive days with any run, lifetime miles aggregation

4. **`src/screens/LogRunScreen.tsx`** — Primary action screen:
   - Distance input (miles/km toggle, saved preference)
   - Duration input (stopwatch or manual entry)
   - Conditions selector (3 buttons: Great run / Tough but done / Minimum mile)
   - Auto-computes pace on blur
   - On save: check streak continuation, trigger milestone if applicable

5. **`src/screens/TodayScreen.tsx`** — Replace swipe cards with:
   - Large streak counter (days)
   - "Log Today's Run" CTA (big green button, not swipe)
   - Lifetime distance bar (toward next milestone)
   - Yesterday's run summary if exists

6. **`src/screens/StatsScreen.tsx`** — Replace HabitDetail:
   - 30-day calendar heatmap (colored by conditions: green/yellow/red)
   - Lifetime miles + personal best pace
   - Weekly mileage bar chart (7-day view)

7. **`src/screens/PaywallScreen.tsx`** — Annual $19.99/yr (cheaper than Streakr to penetrate market), monthly $2.99/mo, features:
   - Free: Streak tracking, basic log, milestone badges
   - Pro: Pace history, weekly mileage charts, CSV export, training plan templates

8. **`src/screens/OnboardingFlow.tsx`** — 6 steps (simpler than Streakr):
   - Welcome → "Why streak?" (social proof: 4M+ runners) → MVD setup ("What's your minimum mile?") → First run log → Reminder time → Go

9. **`src/constants/theme.ts`** — Dark green theme: `#001a00` bg, `#22c55e` accent, `#ffffff` text

10. **`src/constants/milestones.ts`** — Running-specific:
    - 7 days: "One Week Warrior"
    - 30 days: "Month Mile Club"
    - 50 miles logged: "50-Mile Finisher"
    - 100 miles: "Century Runner"
    - 365 days: "Yearly Runner"

---

## Build Steps (agent-executable)

```bash
# 1. Fork Streakr
cp -r MONEY_METHODS/APP_FACTORY/builds/streakr-native/ MONEY_METHODS/APP_FACTORY/builds/runningstreak-native/

# 2. Update package.json name
sed -i '' 's/"name": "streakr"/"name": "runningstreak"/' runningstreak-native/package.json

# 3. Replace app.json
# (Write new app.json per spec above)

# 4. Modify types → RunEntry model
# (Edit src/types/index.ts)

# 5. Rewrite storage service for RunEntry
# (Edit src/services/storage.ts)

# 6. Rewrite screens per spec
# (Edit src/screens/*.tsx)

# 7. Generate icon: dark green bg, white running figure
curl -sL -o assets/icon.png "https://image.pollinations.ai/prompt/minimalist%20iOS%20app%20icon%20for%20running%20streak%20tracker%2C%20very%20dark%20green%20background%2C%20simple%20white%20running%20figure%20with%20flame%20trail%2C%20clean%20flat%20design?width=1024&height=1024&nologo=true&seed=99"

# 8. TypeScript check
cd runningstreak-native && npx tsc --noEmit

# 9. Test in simulator
npx expo prebuild --platform ios && npx expo run:ios
```

---

## ASO Package

**App Name:** `RunningStreak: Daily Run Tracker`
**Subtitle:** `Log runs. Keep your streak alive.`
**Keywords:** `running,streak,daily,run,tracker,distance,pace,mile,habit,challenge,runner`
**Price test:** Annual $19.99 launch → test $24.99 at 30d if conversion >4%

---

## Review Prompt

Same logic as Streakr but adapted:
- Trigger: Day 7 streak OR 50-mile lifetime milestone
- 3s delay after milestone animation
- 90-day cooldown

---

## Stripe Products Needed (HUMAN ACTION)

1. `runningstreak-annual` — $19.99/yr, 7-day trial
2. `runningstreak-monthly` — $2.99/mo, 3-day trial

---

## Status: SPEC COMPLETE — ready for build in next cycle
