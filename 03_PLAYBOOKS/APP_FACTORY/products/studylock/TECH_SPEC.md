# StudyLock - Technical Specification

---

## Stack Overview

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Framework | React Native | Cross-platform, reuses PrayerLock/WalkToUnlock code |
| Language | TypeScript | Type safety |
| State | Zustand | Lightweight state management with persistence |
| Storage | AsyncStorage | Local persistence for settings and history |
| Subscriptions | RevenueCat | Handles subscriptions and trials |
| Analytics | Mixpanel | Free tier sufficient |
| Push | Firebase Cloud Messaging | Free, reliable |
| Timer | react-native-background-timer | Background timer support |

---

## Architecture

```
+----------------------------------------------------------+
|                     StudyLock App                         |
+----------------------------------------------------------+
|  Screens                                                  |
|  +----------+ +----------+ +----------+ +----------+      |
|  | Onboard  | |   Home   | |  Stats   | | Settings |      |
|  +----------+ +----------+ +----------+ +----------+      |
+----------------------------------------------------------+
|  Core Services                                            |
|  +--------------+ +---------------+ +--------------+      |
|  | TimerService | | BlockerService| | StreakService|      |
|  +--------------+ +---------------+ +--------------+      |
+----------------------------------------------------------+
|  State Management (Zustand)                               |
|  +-----------+ +------------+ +-----------+               |
|  | timerStore| | streakStore| | userStore |               |
|  +-----------+ +------------+ +-----------+               |
+----------------------------------------------------------+
|  External                                                 |
|  +----------+ +----------+                                |
|  |RevenueCat| | Firebase |                                |
|  +----------+ +----------+                                |
+----------------------------------------------------------+
```

---

## Data Models

### User Settings
```typescript
interface UserSettings {
  workDuration: number;        // 5-60 minutes
  breakDuration: number;       // 1-15 minutes
  blockedApps: BlockedApp[];
  notificationsEnabled: boolean;
  soundEnabled: boolean;
  vibrationEnabled: boolean;
  hasCompletedOnboarding: boolean;
  trialStartDate: string | null;
}
```

### Timer State
```typescript
type TimerState = 'idle' | 'studying' | 'break' | 'paused';

interface TimerData {
  state: TimerState;
  remainingSeconds: number;
  totalSeconds: number;
  sessionStartTime: number | null;
  currentSessionType: 'work' | 'break';
}
```

### Study Session
```typescript
interface StudySession {
  id: string;
  date: string;              // YYYY-MM-DD
  startTime: number;         // timestamp
  endTime: number | null;
  duration: number;          // seconds
  completed: boolean;
  wasInterrupted: boolean;
}
```

### Streak Data
```typescript
interface StreakData {
  currentStreak: number;
  longestStreak: number;
  totalDaysStudied: number;
  totalStudyHours: number;
  completedDates: string[];
  lastStudyDate: string | null;
}
```

---

## File Structure

```
studylock/
├── App.tsx                    # App entry point
├── app.json                   # Expo config
├── package.json
├── tsconfig.json
├── babel.config.js
├── metro.config.js
└── src/
    ├── types/
    │   └── index.ts           # TypeScript interfaces
    ├── utils/
    │   ├── constants.ts       # Config, colors, presets
    │   └── dateUtils.ts       # Date formatting helpers
    ├── stores/
    │   ├── timerStore.ts      # Pomodoro timer state
    │   ├── streakStore.ts     # Streak and history
    │   └── userStore.ts       # Settings and subscription
    ├── hooks/
    │   └── useTimer.ts        # Timer hook with background support
    ├── components/
    │   ├── timer/
    │   │   ├── TimerDisplay.tsx
    │   │   └── TimerControls.tsx
    │   ├── stats/
    │   │   ├── DailyStats.tsx
    │   │   └── WeeklyChart.tsx
    │   ├── paywall/
    │   │   └── PaywallScreen.tsx
    │   ├── blocker/
    │   │   └── AppSelector.tsx
    │   └── common/
    │       └── StreakBadge.tsx
    ├── screens/
    │   ├── HomeScreen.tsx
    │   ├── StatsScreen.tsx
    │   └── SettingsScreen.tsx
    └── navigation/
        └── AppNavigator.tsx
```

---

## Timer Implementation

### State Machine

```
         +-------+
         | idle  |<---------+
         +-------+          |
              |             |
        startSession()      |
              |             |
              v             |
         +---------+        |
    +--->| studying|        |
    |    +---------+        |
    |         |             |
    |   pause() |           |
    |         v             |
    |    +--------+         |
    +----|paused  |         |
resume() +--------+         |
              |             |
        endSession()        |
              |             |
              v             |
         +-------+          |
         | break |----------+
         +-------+     skipBreak()
              |
        (timer ends)
              |
              v
         +-------+
         | idle  |
         +-------+
```

### Background Timer Logic

```typescript
// When app goes to background:
1. Save current timestamp
2. Stop interval timer

// When app returns to foreground:
1. Calculate elapsed time
2. Subtract from remaining time
3. If time <= 0, complete session
4. Else, resume timer with new remaining time
```

---

## App Blocking Implementation

### iOS (FamilyControls / Screen Time API)
- Requires Apple Family Sharing approval
- Uses `DeviceActivityMonitor` for blocking
- Shield overlay on blocked apps

### Android (UsageStats + Accessibility)
- Request USAGE_STATS_PERMISSION
- Use AccessibilityService to detect app launches
- Show overlay when blocked app detected
- Redirect to StudyLock

### Simplified MVP Approach
For MVP, use "honor system" blocking:
1. Show list of apps to user
2. During session, display motivational overlay
3. Log when user leaves app during session
4. Shame user in stats if they left during session

Real blocking can be added post-MVP after App Store approval process is understood.

---

## Streak Calculation

```typescript
// A day counts toward streak if:
// totalStudyTime >= 25 minutes (MIN_STUDY_TIME_FOR_STREAK)

// Streak breaks if:
// - Current date is not today AND not yesterday
// - No study session recorded for yesterday

function calculateStreak(completedDates: string[]): number {
  // Sort dates descending
  // Check if most recent is today or yesterday
  // Count consecutive days backward
}
```

---

## Paywall Strategy

### Trial Flow
```
1. User completes onboarding
2. Trial starts (7 days)
3. Full app access during trial
4. Day 6: Push notification reminder
5. Day 7: Trial expires
6. Hard paywall on app launch
```

### RevenueCat Integration
```typescript
// Initialize on app start
Purchases.configure({ apiKey: REVENUECAT_API_KEY });

// Check subscription status
const customerInfo = await Purchases.getCustomerInfo();
const isActive = customerInfo.entitlements.active['premium'];

// Make purchase
const { customerInfo } = await Purchases.purchasePackage(package);
```

---

## Push Notifications

### Notification Types

| Type | Trigger | Message |
|------|---------|---------|
| Session Complete | Timer ends | "Great work! You completed a 25-minute session." |
| Break Ending | Break timer | "Break's over! Ready for another session?" |
| Streak Reminder | 8pm daily | "Don't break your streak! Study for 25 min today." |
| Streak Milestone | Streak = 7, 30, 100 | "Amazing! You've studied for 7 days straight!" |
| Trial Ending | Trial day 6 | "Your free trial ends tomorrow. Subscribe to continue." |

### Implementation
```typescript
// Request permissions
await Notifications.requestPermissionsAsync();

// Schedule local notification
await Notifications.scheduleNotificationAsync({
  content: {
    title: "Streak Reminder",
    body: "Don't break your streak! Study for 25 min today.",
  },
  trigger: {
    hour: 20,
    minute: 0,
    repeats: true,
  },
});
```

---

## Performance Targets

| Metric | Target |
|--------|--------|
| App launch | < 2s |
| Timer accuracy | < 1s drift per hour |
| Background resume | < 500ms |
| Battery impact | < 2% daily |
| Storage usage | < 20MB |

---

## Security Considerations

### Data Privacy
- All data stored locally (no server)
- No PII collected
- Study history stays on device

### Subscription Validation
- RevenueCat handles server-side validation
- Offline grace period: 7 days
- Receipt validation on app launch

### Anti-Bypass
- Emergency unlock requires exact phrase match
- All bypasses logged in history
- Bypass resets streak (shame)

---

## Testing Strategy

### Unit Tests
- Streak calculation
- Timer state machine
- Date utilities
- Progress calculations

### Integration Tests
- Subscription flow
- Timer background behavior
- Storage persistence

### Manual Testing
- Real devices (iOS + Android)
- Background behavior
- Push notifications
- Paywall flow
- Emergency unlock

---

## Deployment

### App Store
- Category: Education or Productivity
- Keywords: study, focus, pomodoro, timer, block apps, student
- Privacy nutrition label: No data collected
- Age rating: 4+

### Google Play
- Category: Education
- Similar keywords
- Privacy policy required
- Target SDK: 34

---

## Cost Estimate

| Item | Monthly Cost |
|------|--------------|
| RevenueCat | Free (until $2.5k MRR) |
| Firebase | Free tier |
| Mixpanel | Free tier |
| Apple Developer | $8.25 |
| Google Play | $2.08 |
| **Total** | ~$10/mo |

---

## Code Sharing Opportunities

### Reusable from PrayerLock/WalkToUnlock
- Paywall screen (customize copy)
- Streak tracking logic
- Settings screen structure
- Emergency unlock flow
- Date utilities
- Subscription service

### Potential Shared Library
```
shared/
├── components/
│   ├── StreakBadge.tsx
│   ├── PaywallTemplate.tsx
│   └── SettingsRow.tsx
├── services/
│   ├── subscriptionService.ts
│   └── analyticsService.ts
└── utils/
    ├── dateUtils.ts
    └── streakUtils.ts
```

---

## MVP Checklist

- [x] Pomodoro timer (25/5 default, customizable)
- [x] Timer display with progress ring
- [x] Play/pause/end controls
- [x] Break timer
- [x] Streak tracking
- [x] Daily/weekly stats
- [x] Weekly chart
- [x] App selector UI
- [x] Hard paywall with 7-day trial
- [x] Settings screen
- [x] Emergency unlock
- [x] Onboarding flow
- [ ] Push notifications (integrate Firebase)
- [ ] RevenueCat integration (add API keys)
- [ ] Real app blocking (post-MVP)
- [ ] App Store submission

---

## Next Steps

1. Add Firebase for push notifications
2. Integrate RevenueCat with real product IDs
3. Create app icons and splash screens
4. Write App Store description
5. TestFlight beta testing
6. Submit to App Store
7. Create TikTok content for launch
