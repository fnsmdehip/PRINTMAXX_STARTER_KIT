# DreamBoard (Vision Board App) - SDK 54

**Status:** SCAFFOLD
**Clone Source:** APP_CLONE_OPPORTUNITIES.csv #27
**Concept:** Daily check-ins + vision boards. Accountability trend Jan 2026.
**Bundle ID:** com.printmaxx.dreamboard
**Build Estimate:** 1 week
**Priority:** HIGH
**Mascot:** Star character

---

## Concept

A vision board app that combines digital vision boards with daily check-ins. Users create boards with goals, images, and affirmations, then check in daily to rate progress and stay accountable. The accountability angle is trending hard in Jan 2026 (same wave as YearButtons "systems not outcomes" trend).

Not just a static Pinterest-style board. The daily check-in mechanic creates habit loops and gives users a reason to open the app every day.

---

## Core Features

### MVP (Ship in 1 week)
1. **Vision Board Builder** - Drag-and-drop grid of goals with images, text, colors
2. **Daily Check-In** - Rate each goal 1-5, journal prompt, streak tracking
3. **Goal Categories** - Health, Career, Finance, Relationships, Personal Growth
4. **Progress Timeline** - See check-in history per goal over time
5. **Streak Counter** - Current check-in streak prominently displayed
6. **Onboarding** - 3 slides: concept, create first board, start trial
7. **Paywall** - Monthly $4.99, Annual $29.99, 3-day trial

### Premium Features
- Unlimited boards (free = 1 board)
- Custom backgrounds and themes
- Photo upload for goal images
- Weekly/monthly progress reports
- Share board as image
- Affirmation reminders
- Widget showing today's focus goal

---

## Tech Stack

- Expo SDK 54 / React 19 / React Native 0.81.5
- expo-router (file-based routing)
- zustand + AsyncStorage (persistence)
- expo-haptics (check-in feedback)
- expo-image-picker (goal photos)
- react-native-purchases (RevenueCat)
- expo-notifications (daily check-in reminder)
- react-native-reanimated (board animations)

---

## File Structure

```
dreamboard-sdk54/
  app/
    _layout.tsx
    index.tsx
    onboarding.tsx
    paywall.tsx
    privacy-policy.tsx
    terms.tsx
    (tabs)/
      _layout.tsx
      index.tsx        # Main vision board view
      checkin.tsx       # Daily check-in flow
      progress.tsx      # Progress timeline
      settings.tsx      # Settings + MoreApps
  src/
    stores/
      boardStore.ts    # Vision boards, goals, images
      checkinStore.ts  # Daily check-in data, streaks
      userStore.ts     # Settings, subscription, onboarding
    components/
      BoardGrid.tsx    # Vision board layout
      GoalCard.tsx     # Individual goal tile
      CheckInForm.tsx  # Daily rating + journal
      StreakCounter.tsx
      ProgressChart.tsx
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

## Data Model

### Board
```typescript
interface Board {
  id: string;
  name: string;
  goals: Goal[];
  background: string;  // color or image URI
  createdAt: string;
  updatedAt: string;
}
```

### Goal
```typescript
interface Goal {
  id: string;
  boardId: string;
  title: string;
  category: 'health' | 'career' | 'finance' | 'relationships' | 'personal';
  imageUri?: string;
  color: string;
  affirmation?: string;
  position: { row: number; col: number };
  createdAt: string;
}
```

### CheckIn
```typescript
interface CheckIn {
  id: string;
  date: string;  // YYYY-MM-DD
  ratings: Record<string, number>;  // goalId -> 1-5
  journalEntry?: string;
  mood?: 'great' | 'good' | 'okay' | 'tough';
}
```

---

## Monetization

| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | 1 board, 5 goals max, basic check-in |
| Monthly | $4.99 | Unlimited boards, photos, reports, widget |
| Annual | $29.99 | Same as monthly (50% savings) |
| Trial | 3 days | Full access |

---

## Competitive Analysis

- **Vision Board apps on App Store:** Most are static image collage makers ($2.99-$9.99)
- **Accountability apps:** Day One (journal), Streaks (habits), but none combine vision board + daily check-in
- **Gap we exploit:** Accountability trend + vision board = daily active use (not set-and-forget)
- **Star mascot** differentiates from minimalist competitors

---

## Marketing Angle

- TikTok video: "I manifested my dream life with this app" (vision board timelapse)
- Show the daily check-in streak building up
- "Vision boards work. But only if you look at them every day. This app makes you."
- Cross-promote from PrayerLock (faith goal setting), BioMaxx (health goals)

---

## Next Steps

1. [ ] Build vision board grid component
2. [ ] Add goal card with category colors
3. [ ] Build daily check-in flow with ratings
4. [ ] Build board store with AsyncStorage
5. [ ] Add progress timeline view
6. [ ] Add onboarding flow
7. [ ] Add paywall with RevenueCat
8. [ ] Add daily check-in notification
9. [ ] Add MoreApps cross-promotion
10. [ ] Generate app icon with star mascot (Gemini)
11. [ ] Test in iOS Simulator
12. [ ] Submit to App Store
