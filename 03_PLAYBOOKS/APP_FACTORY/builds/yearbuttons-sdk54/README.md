# YearButtons (365 Buttons) - SDK 54

**Status:** SCAFFOLD
**Clone Source:** APP_CLONE_OPPORTUNITIES.csv #28
**Concept:** One button per day for 365 days. Systems not outcomes. Viral Jan 2026.
**Bundle ID:** com.printmaxx.yearbuttons
**Build Estimate:** 1 week
**Priority:** HIGHEST

---

## Concept

A dead-simple habit tracker: 365 buttons in a grid. Press today's button when you complete your daily habit. That's it. No complex tracking, no analytics overload. Just a satisfying visual of your year filling up.

Inspired by the viral "systems not outcomes" trend on TikTok (Jan 2026). The app sells the feeling of consistency over perfection.

---

## Core Features

### MVP (Ship in 1 week)
1. **365-Button Grid** - Full year view, one button per day
2. **Daily Press** - Tap today's button, satisfying haptic + animation
3. **Streak Counter** - Current streak prominently displayed
4. **Multiple Habits** - Track up to 3 habits (free) or unlimited (premium)
5. **Year Progress** - Percentage of year completed visual
6. **Onboarding** - 3 slides: concept, choose first habit, start trial
7. **Paywall** - Monthly $4.99, Annual $29.99, 3-day trial

### Premium Features
- Unlimited habits
- Custom colors per habit
- Yearly heatmap view
- Share year-in-review image
- Streak recovery (missed 1 day grace)
- Widget for home screen

---

## Tech Stack

- Expo SDK 54 / React 19 / React Native 0.81.5
- expo-router (file-based routing)
- zustand + AsyncStorage (persistence)
- expo-haptics (button press feedback)
- react-native-purchases (RevenueCat)
- expo-notifications (daily reminder)

---

## File Structure

```
yearbuttons-sdk54/
  app/
    _layout.tsx
    index.tsx
    onboarding.tsx
    paywall.tsx
    (tabs)/
      _layout.tsx
      index.tsx        # Main 365 grid
      habits.tsx       # Habit management
      settings.tsx     # Settings + MoreApps
  src/
    stores/
      habitStore.ts
      userStore.ts
    components/
      ButtonGrid.tsx
      DayButton.tsx
      StreakCounter.tsx
      MoreApps.tsx
    services/
      subscriptionService.ts
      notificationService.ts
    utils/
      constants.ts
      dateUtils.ts
    types/
      index.ts
```

---

## Monetization

| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | 3 habits, basic grid, streak |
| Monthly | $4.99 | Unlimited habits, colors, heatmap, widget |
| Annual | $29.99 | Same as monthly (50% savings) |
| Trial | 3 days | Full access |

---

## Competitive Analysis

- **365 Buttons original:** Viral concept, unclear if app exists
- **Streaks app:** $4.99 one-time, simple habit tracker (1.7K ratings)
- **Done - Habit Tracker:** Subscription, more complex (12K ratings)
- **Gaps we exploit:** Viral trend timing, faith/wellness niche angles, mascot potential

---

## Marketing Angle

- TikTok video: "What if you just pressed one button every day for a year?"
- Show the grid filling up timelapse
- "Systems beat goals. This app proves it."
- Cross-promote from PrayerLock, BioMaxx, StepUnlock

---

## Next Steps

1. [ ] Build core button grid component
2. [ ] Add haptic feedback + animation on press
3. [ ] Build habit store with AsyncStorage
4. [ ] Add onboarding flow
5. [ ] Add paywall with RevenueCat
6. [ ] Add daily notification reminder
7. [ ] Add MoreApps cross-promotion
8. [ ] Generate app icon (Gemini)
9. [ ] Test in iOS Simulator
10. [ ] Submit to App Store
