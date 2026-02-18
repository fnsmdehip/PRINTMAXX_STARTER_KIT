# LearnLock SDK 54

LearnLock upgraded to Expo SDK 54 with React Native 0.81.5 and React 19.1.0. A study timer app with focus blocking, streak tracking, and subscription paywall.

## Quick Start

```bash
# Install dependencies
npm install

# Start iOS Simulator
npm run ios

# Start Android Emulator
npm run android

# Start web
npm run web

# Development server with menu
npm start
```

## Features

- **Study Timer**: Customizable work/break durations
- **App Blocking**: Block distracting apps during study sessions
- **Streak Tracking**: Track daily study consistency with streaks
- **Statistics**: View weekly/monthly study patterns
- **Subscription**: Trial period + premium subscription via RevenueCat
- **Notifications**: Optional push notifications for session reminders
- **Settings**: Full customization of timers, notifications, and blocked apps

## Architecture

### State Management: Zustand v5

Three main stores manage app state:

1. **useUserStore** (`src/stores/userStore.ts`)
   - User settings (work/break durations, blocked apps)
   - Subscription state (trial, active subscription)
   - Onboarding completion

2. **useTimerStore** (`src/stores/timerStore.ts`)
   - Current timer state (idle, studying, break)
   - Session tracking for the day
   - Progress calculation

3. **useStreakStore** (`src/stores/streakStore.ts`)
   - Current streak count
   - Daily history and statistics
   - Weekly/monthly data

All stores use `AsyncStorage` for persistence.

### Navigation: expo-router v6

Tab-based navigation with modal screens:

```
app/
├── index.tsx          # Root screen (onboarding/dashboard redirect)
├── _layout.tsx        # Root stack layout
├── onboarding.tsx     # Onboarding flow
├── paywall.tsx        # Subscription paywall (modal)
├── privacy.tsx        # Privacy policy
├── terms.tsx          # Terms of service
└── (tabs)/
    ├── _layout.tsx    # Tab navigation
    ├── index.tsx      # Home (timer)
    ├── stats.tsx      # Statistics
    └── settings.tsx   # Settings
```

### Components

**Timer Components** (`src/components/timer/`)
- `TimerDisplay.tsx` - Circular timer with progress ring
- `TimerControls.tsx` - Start/pause/end buttons

**App Blocking** (`src/components/blocker/`)
- `AppSelector.tsx` - Select apps to block during study

**Common** (`src/components/common/`)
- `StreakBadge.tsx` - Display current streak

**Paywall** (`src/components/paywall/`)
- `PaywallScreen.tsx` - Subscription options

### Types

Defined in `src/types/index.ts`:

```typescript
// User settings
interface BlockedApp {
  id: string;
  name: string;
  enabled: boolean;
}

// Timer data
interface StudySession {
  id: string;
  date: string;
  startTime: number;
  endTime: number | null;
  duration: number; // seconds
  completed: boolean;
  wasInterrupted: boolean;
}

// Streak data
interface DailyStudyData {
  date: string;
  totalStudyTime: number; // seconds
  sessionsCompleted: number;
  streakMaintained: boolean;
  sessions: StudySession[];
}
```

## Configuration

### app.json

Key settings:

```json
{
  "expo": {
    "name": "LearnLock",
    "slug": "learnlock",
    "scheme": "learnlock",
    "newArchEnabled": true,
    "ios": {
      "bundleIdentifier": "com.printmaxx.learnlock",
      "infoPlist": {
        "UIBackgroundModes": ["fetch", "remote-notification"]
      }
    },
    "android": {
      "package": "com.printmaxx.learnlock",
      "edgeToEdgeEnabled": true
    }
  }
}
```

### Constants

Defined in `src/utils/constants.ts`:

```typescript
const DEFAULT_WORK_DURATION = 25; // minutes (Pomodoro)
const DEFAULT_BREAK_DURATION = 5; // minutes
const MIN_STUDY_TIME_FOR_STREAK = 600; // 10 minutes
const TRIAL_DURATION_DAYS = 3;
```

## Dependencies

### Core
- `react` 19.1.0
- `react-native` 0.81.5
- `expo` 54.0.32
- `expo-router` 6.0.22

### Storage & State
- `zustand` 5.0.10
- `@react-native-async-storage/async-storage` 2.2.0

### UI
- `@expo/vector-icons` 15.0.3
- `react-native-safe-area-context` 5.6.0
- `react-native-screens` 4.16.0

### Other
- `expo-splash-screen` 31.0.13
- `expo-status-bar` 3.0.9
- `expo-haptics` 15.0.8
- `expo-linking` 8.0.11
- `expo-constants` 18.0.13

## Development

### TypeScript

Strict mode enabled. Run type checking:

```bash
npx tsc --noEmit
```

### Debugging

Connect React DevTools to dev server. Use Zustand DevTools for store debugging.

### Testing

Manual testing on iOS Simulator and physical devices. For automation, use Detox or Appium.

## Publishing

### Prerequisites
1. Apple Developer account
2. TestFlight setup in App Store Connect
3. RevenueCat account (for subscriptions)
4. Build signing certificate and provisioning profile

### Build for iOS
```bash
npx eas build --platform ios
```

### Build for Android
```bash
npx eas build --platform android
```

See `OPS/MANUAL_SETUP_TASKS.md` for account setup details.

## Upgrades from Original LearnLock

See `UPGRADE_NOTES.md` for detailed changes.

Key improvements:
- React 19 performance enhancements
- Faster Metro bundler
- New Architecture support on Android
- Better TypeScript support
- Smaller JavaScript payload

## Troubleshooting

**App won't start:**
```bash
npm install
npx expo start --ios --clear
```

**Types not resolving:**
```bash
npx tsc --noEmit
npm install @types/react@~19.1.0 --save-dev
```

**AsyncStorage data lost:**
Check `STORAGE_KEYS` in `src/utils/constants.ts` - ensure persistent stores have correct key names.

**Simulator blank screen:**
- Try hot reloading (cmd+R)
- Restart dev server
- Nuke cache: `rm -rf .expo node_modules package-lock.json && npm install`

## Resources

- [Expo Documentation](https://docs.expo.dev)
- [expo-router Guide](https://docs.expo.dev/routing/introduction/)
- [React Native 0.81 Release Notes](https://github.com/facebook/react-native/releases)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
- [AsyncStorage Docs](https://react-native-async-storage.github.io/async-storage/)

## File Organization

```
learnlock-sdk54/
├── app/                    # expo-router routes
├── src/
│   ├── components/        # Reusable UI components
│   ├── screens/           # Full screen components
│   ├── stores/            # Zustand state management
│   ├── types/             # TypeScript type definitions
│   ├── utils/             # Helper functions & constants
│   ├── services/          # External API integration
│   ├── hooks/             # Custom React hooks
│   └── navigation/        # Navigation configuration
├── assets/                # App icons, splash screen
├── app.json              # Expo configuration
├── package.json          # Dependencies
├── tsconfig.json         # TypeScript configuration
├── babel.config.js       # Babel configuration
└── metro.config.js       # Metro bundler config
```

## Support

For issues or questions:
1. Check `UPGRADE_NOTES.md` for SDK 54 changes
2. Review `MIGRATION_GUIDE.md` for version details
3. Check original LearnLock at `/builds/learnlock/` for reference
