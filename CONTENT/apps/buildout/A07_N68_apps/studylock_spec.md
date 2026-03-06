# StudyLock — Feature Spec

**Concept:** A study accountability app that locks your phone's other apps until you complete a timed study session. Think FocusLock meets Pomodoro meets social accountability.

**Target User:** Students (16-25), test preppers (LSAT/MCAT/bar exam), self-learners grinding skills.

**Category:** Education / Productivity
**Platform:** iOS first, Android follow
**Pricing:** Free 3 sessions/day → $4.99/mo StudyLock Pro
**Revenue Target:** $2,500/mo at 500 paid subs — achievable at 25K downloads with 2% conversion

---

## Core Differentiator

FocusLock + Pomodoro + streak system. Not just blocking — gamified study sessions with XP, levels, and optional friend accountability. The lock mechanism makes it sticky. The streaks make it addictive.

---

## MVP Features (v1.0)

### 1. Study Session Engine
- Session types: Pomodoro (25/5), Short Focus (15/3), Deep Work (90/20), Custom
- App blocker: iOS Screen Time API locks selected apps during session
- Break enforcement: can't skip break (prevents burnout, improves retention)
- Background audio: lo-fi presets, brown noise, rain, white noise (ElevenLabs-generated ambience)
- Session notes: quick text field to log what you studied

### 2. Lock Mechanism
- iOS: Screen Time API (MDM profile approach for true locking)
- Android: Accessibility Service + UsageStatsManager
- Emergency exit: 3 taps → 60-second countdown → session marked as broken (shame mechanic)
- Allowlist: phone calls, emergency contacts, specified apps always allowed

### 3. Streak & XP System
| Action | XP |
|---|---|
| Complete Pomodoro | +10 XP |
| Complete Deep Work | +30 XP |
| Maintain daily streak | +15 XP bonus |
| Zero breaks skipped | +5 XP bonus |
| New subject unlocked | +20 XP |
| Weekly goal hit | +50 XP |

**Levels:** Rookie → Focused → Scholar → Grinder → Legend → StudyLock Elite (100+ day streak)

**Streaks:** Daily streak resets at midnight. 7-day streak = badge. 30-day = Pro trial unlock.

### 4. Subject Tracking
- Up to 8 subjects (Pro: unlimited)
- Time logged per subject per day/week/month
- Color-coded cards with study goal per subject (e.g., "Math — goal 2h/day")
- Progress bar per subject

### 5. Stats Dashboard
- Daily/weekly/monthly heatmap (GitHub-style)
- Total study hours lifetime
- Subject breakdown pie chart
- Productivity score (sessions completed / sessions started)
- Best streak, current streak

---

## Pro Features ($4.99/mo or $29.99/yr)

### Advanced Locking
- Full device lockdown (no app exceptions except emergency)
- Website blocking via VPN profile (blocks distractions at DNS level)
- Scheduled auto-sessions ("Lock me in Mon-Fri 9am-12pm")
- Recurring session templates

### Social Accountability
- Accountability partner: share streak with 1 friend — they get notified if you break
- Group study rooms: 2-8 people studying simultaneously (no chat, just presence indicators)
- Public profile + leaderboard (opt-in)
- Study challenges: "Complete 20 Pomodoros this week" community goals

### Advanced Analytics
- Focus score trending over 90 days
- Optimal study time detection (AI-analyzed based on completion rate)
- Subject balance recommendations
- Export to CSV for tracking

### Customization
- Custom session lengths
- Custom break activities (e.g., "do 10 pushups" prompt during break)
- Themes: Dark, Forest, Paper, Midnight, Space
- Custom ambient sounds upload

---

## Technical Architecture

### Frontend
- **iOS:** SwiftUI + WidgetKit (home screen widget showing streak + today's study time)
- **Android:** Jetpack Compose
- **Web PWA:** React + localStorage (fallback, no locking features)

### Backend (minimal)
- **Supabase:** auth + user profiles + streak sync across devices
- **Push notifications:** APNs (iOS) / FCM (Android) — streak reminders, accountability pings
- **Analytics:** PostHog self-hosted

### Screen Time Integration (iOS)
```swift
import FamilyControls
import ManagedSettings
import DeviceActivity

// Request authorization
let center = AuthorizationCenter.shared
try await center.requestAuthorization(for: .individual)

// Lock apps during session
let store = ManagedSettingsStore()
store.shield.applications = selectedApps  // Set of ApplicationToken

// Monitor session end
let schedule = DeviceActivitySchedule(
    intervalStart: DateComponents(hour: startHour, minute: startMin),
    intervalEnd: DateComponents(hour: endHour, minute: endMin),
    repeats: false
)
```

### Accessibility Service (Android)
```kotlin
class StudyLockService : AccessibilityService() {
    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        if (event?.eventType == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED) {
            val packageName = event.packageName?.toString()
            if (blockedApps.contains(packageName) && isSessionActive) {
                // Return user to StudyLock
                launchStudyLock()
            }
        }
    }
}
```

---

## Monetization Stack

| Stream | Revenue/Mo |
|---|---|
| Pro subscriptions ($4.99/mo) | Primary |
| Annual plan ($29.99/yr) | Churn reduction |
| StudyLock Elite badge (cosmetic $0.99 one-time) | Whales |
| B2B: School/tutor license ($99/mo per seat bulk) | Expansion |
| Merch: "grind differently" tee (Printful) | Brand |

**Revenue math:**
- 25K downloads: 500 paid = $2,500/mo
- 100K downloads: 2,000 paid = $10,000/mo
- Annual plan conversion target: 25% of paid users → increases LTV 3x

---

## App Store Metadata

**Title:** StudyLock — Focus & Study Timer
**Subtitle:** Block Distractions. Build Streaks.
**Keywords:** study timer, focus app, pomodoro, app blocker, productivity, student, study streak, deep work, screen time

**Description (short):**
Lock your apps. Study smarter. Build a streak you can't break.

StudyLock locks your distractions so you can focus on what actually matters. Set a session, choose what to block, and go. No willpower needed — the app does the blocking for you.

**Category:** Education (primary), Productivity (secondary)
**Rating:** 4+
**Localization priority:** EN, ES, PT-BR, KO, JA (students worldwide)

---

## Competitive Analysis

| App | Price | Locking | Streaks | Social |
|---|---|---|---|---|
| Forest | Free/$1.99 IAP | Partial (gamified) | Yes | Trees planted |
| Flora | Free/$9.99/yr | Partial | Yes | Friend rooms |
| Focus Bear | $7.99/mo | Strong (habits) | Yes | No |
| **StudyLock** | **Free/$4.99/mo** | **Full iOS Screen Time** | **XP + levels** | **Accountability partner** |

**Edge:** Full Screen Time API integration + XP gamification + lower price than Focus Bear. Forest is the incumbent — StudyLock wins on price and harder lock.

---

## Launch Plan

**Week 1-2:** Build MVP (SwiftUI, Screen Time, Pomodoro, streaks)
**Week 3:** TestFlight beta, 50 testers from Reddit (r/MCAT, r/lawschool, r/premed)
**Week 4:** App Store submission
**Week 5+:** TikTok content — "I locked my phone for 25 minutes, here's what happened"

**Reddit launch posts:**
- r/MCAT: "built an app to stop myself from checking my phone while studying"
- r/productivity: "StudyLock — actual phone locking Pomodoro timer, free to try"
- r/getdisciplined: "tired of Forest not actually blocking apps, so I built this"

**TikTok angle:** Study-with-me format. Show lock activating. Real student reaction. Hook: "This app literally won't let you open Instagram during your study session."

---

## Build Timeline

| Phase | Duration | Deliverable |
|---|---|---|
| MVP iOS | 3-4 weeks | Screen Time + Pomodoro + streaks |
| App Store launch | Week 5 | v1.0 live |
| Android port | Week 8-12 | Kotlin version |
| Pro features | Week 6-8 | Subscription + social |
| B2B module | Month 4+ | School license dashboard |

**Build cost (solo dev):**
- SwiftUI dev: self-build or $2,000 contractor (MVP)
- Supabase: free tier → $25/mo at scale
- Break-even: 5 paid subs ($25/mo) → covers Supabase
- Profitable from day 1 if self-built
