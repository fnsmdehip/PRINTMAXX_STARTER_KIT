# PrayerLock

Block distracting apps until you complete your morning devotion.

## Overview

PrayerLock is a screen time blocker for Christians. Selected apps stay locked until you complete your daily prayer time and scripture reading.

Core features:
- App blocking (requires native module setup)
- Prayer timer with guided prompts
- Daily scripture reading from bible-api.com
- Streak tracking
- Hard paywall ($9.99/mo or $49.99/yr)

## Project Structure

```
prayerlock/
├── src/
│   ├── screens/          # All app screens
│   │   ├── OnboardingScreen.tsx
│   │   ├── HomeScreen.tsx
│   │   ├── TimerScreen.tsx
│   │   ├── ScriptureScreen.tsx
│   │   ├── StatsScreen.tsx
│   │   ├── SettingsScreen.tsx
│   │   ├── PaywallScreen.tsx
│   │   └── EmergencyUnlockScreen.tsx
│   ├── services/         # Business logic
│   │   ├── bibleService.ts
│   │   ├── blockerService.ts
│   │   ├── streakService.ts
│   │   └── subscriptionService.ts
│   ├── stores/           # Zustand state
│   │   ├── userStore.ts
│   │   └── devotionStore.ts
│   ├── types/            # TypeScript types
│   └── utils/            # Utilities
├── __tests__/            # Unit tests
├── App.tsx               # Root component
└── package.json
```

## Quick Start

```bash
# Install dependencies
npm install

# iOS
cd ios && pod install && cd ..
npm run ios

# Android
npm run android

# Run tests
npm test
```

## Tech Stack

- React Native 0.73
- TypeScript
- Zustand (state management)
- React Navigation
- AsyncStorage (persistence)
- RevenueCat (subscriptions)

## What's Implemented

- Full UI for all screens
- Zustand stores for state management
- Bible API integration (bible-api.com)
- Streak calculation logic
- Trial management
- Paywall with subscription options
- Emergency unlock flow

## What Needs Manual Setup

1. **Native modules** - iOS Screen Time API and Android UsageStats
2. **RevenueCat** - API keys and product setup
3. **Firebase** - Push notifications (optional)
4. **App Store** - Listings and screenshots

See SUBMISSION_CHECKLIST.md for full details.

## Key Files

| File | Purpose |
|------|---------|
| `src/stores/devotionStore.ts` | Session and streak state |
| `src/stores/userStore.ts` | Settings and subscription |
| `src/services/bibleService.ts` | 365 daily passages |
| `src/services/blockerService.ts` | Native module interface |
| `src/utils/constants.ts` | All config values |

## Customization

### Change prayer duration options
Edit `src/screens/OnboardingScreen.tsx` line with `durations` array.

### Change default blocked apps
Edit `src/utils/constants.ts` - `COMMON_SOCIAL_APPS` array.

### Change subscription pricing
Edit `src/utils/constants.ts` and update in RevenueCat dashboard.

### Add more daily passages
Edit `src/services/bibleService.ts` - `DAILY_PASSAGES` array.

## License

Proprietary. Part of the PRINTMAXX App Factory.
