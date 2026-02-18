# StudyScore (Focus Score for Students) - SDK 54

**Status:** SCAFFOLD
**Clone Source:** APP_CLONE_OPPORTUNITIES.csv #42
**Concept:** Simple focus score for students. Gamified study tracking without full app blocker.
**Inspired By:** Opal (focus score feature)
**Bundle ID:** com.printmaxx.studyscore
**Build Estimate:** 1 week
**Priority:** HIGH
**Mascot:** Owl character

---

## Concept

A gamified focus score app for students. Instead of trying to block apps (which requires native APIs and gets rejected by Apple), StudyScore takes a positive approach: track your study sessions and earn a daily Focus Score from 0-100.

The score is based on: study session duration, consistency (streak), session quality (self-rated), and distraction-free time. Students compete with themselves to beat their personal best score each day.

Think of it as a fitness tracker for studying. No blocking, no restrictions, just a satisfying number that goes up when you study well.

---

## Core Features

### MVP (Ship in 1 week)
1. **Focus Score (0-100)** - Daily composite score prominently displayed
2. **Study Timer** - Start/pause/stop with ambient sound options
3. **Session Rating** - After each session: rate focus quality 1-5
4. **Daily/Weekly Stats** - Score history, study time, session count
5. **Streak Counter** - Consecutive days with score above 50
6. **Subject Tags** - Tag sessions by subject (Math, Science, English, etc.)
7. **Onboarding** - 3 slides: concept, set daily study goal, start trial
8. **Paywall** - Monthly $3.99, Annual $24.99, 3-day trial

### Premium Features
- Unlimited subject tags (free = 3)
- Detailed analytics (best study times, score trends)
- Study group leaderboards
- Custom timer sounds
- Export study reports (PDF for parents/teachers)
- Widget showing today's score
- Pomodoro mode (25/5 intervals)

---

## Focus Score Algorithm

```
Daily Focus Score = weighted average of:
  - Study Duration (40%): minutes studied / daily goal * 100
  - Consistency (20%): streak bonus (longer streak = higher)
  - Session Quality (25%): average self-rating * 20
  - Sessions Count (15%): number of sessions / target * 100

Capped at 100. Minimum 0.
```

### Score Tiers
| Score | Label | Color |
|-------|-------|-------|
| 90-100 | Genius Mode | Gold |
| 70-89 | Focused | Green |
| 50-69 | Getting There | Blue |
| 30-49 | Warming Up | Orange |
| 0-29 | Just Starting | Gray |

---

## Tech Stack

- Expo SDK 54 / React 19 / React Native 0.81.5
- expo-router (file-based routing)
- zustand + AsyncStorage (persistence)
- expo-haptics (timer feedback)
- expo-av (ambient study sounds)
- react-native-purchases (RevenueCat)
- expo-notifications (study reminder)
- react-native-reanimated (score animations)
- react-native-svg (score gauge/charts)

---

## File Structure

```
studyscore-sdk54/
  app/
    _layout.tsx
    index.tsx
    onboarding.tsx
    paywall.tsx
    privacy-policy.tsx
    terms.tsx
    (tabs)/
      _layout.tsx
      index.tsx        # Score dashboard + quick start
      timer.tsx        # Study timer
      stats.tsx        # Analytics and history
      settings.tsx     # Settings + MoreApps
  src/
    stores/
      sessionStore.ts  # Study sessions, timer state
      scoreStore.ts    # Focus scores, streaks, history
      userStore.ts     # Settings, subscription, onboarding
    components/
      ScoreGauge.tsx   # Circular score display (0-100)
      StudyTimer.tsx   # Timer with controls
      SessionCard.tsx  # Individual session summary
      ScoreChart.tsx   # Weekly/monthly score graph
      SubjectTag.tsx   # Subject pill/tag
      StreakCounter.tsx
      MoreApps.tsx
    services/
      subscriptionService.ts
      notificationService.ts
      scoreCalculator.ts  # Focus score algorithm
    utils/
      constants.ts
      dateUtils.ts
    types/
      index.ts
```

---

## Data Model

### StudySession
```typescript
interface StudySession {
  id: string;
  date: string;           // YYYY-MM-DD
  subject: string;
  startTime: string;      // ISO
  endTime: string;        // ISO
  durationMinutes: number;
  focusRating: 1 | 2 | 3 | 4 | 5;  // self-rated
  notes?: string;
}
```

### DailyScore
```typescript
interface DailyScore {
  date: string;           // YYYY-MM-DD
  score: number;          // 0-100
  totalMinutes: number;
  sessionCount: number;
  avgFocusRating: number;
  subjects: string[];
}
```

### UserSettings
```typescript
interface UserSettings {
  dailyGoalMinutes: number;    // default: 120
  targetSessions: number;      // default: 3
  subjects: string[];          // ["Math", "Science", ...]
  studyReminderTime: string;   // "16:00"
  notificationsEnabled: boolean;
  pomodoroEnabled: boolean;
  pomodoroWorkMinutes: number; // default: 25
  pomodoroBreakMinutes: number; // default: 5
}
```

---

## Monetization

| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | 3 subjects, basic score, timer, 7-day history |
| Monthly | $3.99 | Unlimited subjects, full analytics, export, widget |
| Annual | $24.99 | Same as monthly (48% savings) |
| Trial | 3 days | Full access |

**Note:** Lower price point ($3.99 vs $4.99) targets student budget. Parents more likely to approve.

---

## Competitive Analysis

- **Opal:** $9.99/mo, full app blocker (needs Screen Time API) - expensive, complex
- **Forest:** $3.99 one-time, tree-growing focus timer (2M+ ratings) - but no score mechanic
- **Flora:** Free + IAP, similar to Forest - but no analytics
- **Gaps we exploit:** No app blocking (simpler, no Apple rejection risk), gamified score (addictive), student-specific (subject tagging), cheaper than Opal
- **Owl mascot** appeals to student demographic, fun personality

---

## Marketing Angle

- TikTok: "My focus score went from 23 to 87 in one month" (screenshot timelapse)
- Show the score gauge filling up with study sessions
- "Stop trying to block apps. Start tracking your focus instead."
- Target: StudyTok, back-to-school, exam season content
- Cross-promote from LearnLock (study lock), PrayerLock (discipline angle)

---

## Why This Works (No Native Blocking Required)

Unlike StudyLock/LearnLock that try to block apps (requires MDM or Screen Time API):
- StudyScore is POSITIVE reinforcement, not restriction
- No native APIs needed beyond timer
- No Apple rejection risk
- Works on both iOS and Android identically
- Students actually WANT to use it (gamification > punishment)

---

## Next Steps

1. [ ] Build score gauge component (circular animated)
2. [ ] Build study timer with start/pause/stop
3. [ ] Implement focus score algorithm
4. [ ] Build session store with AsyncStorage
5. [ ] Add subject tagging system
6. [ ] Add stats/analytics views
7. [ ] Add onboarding flow
8. [ ] Add paywall with RevenueCat
9. [ ] Add study reminder notification
10. [ ] Add MoreApps cross-promotion
11. [ ] Generate app icon with owl mascot (Gemini)
12. [ ] Test in iOS Simulator
13. [ ] Submit to App Store
