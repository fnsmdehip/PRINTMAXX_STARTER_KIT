# PrayerLock

**Pray First, Phone Second**

A faith-based screen time blocker that helps Christians start their day with prayer before accessing their phone.

## Quick Start

```bash
# Install dependencies
npm install

# Start development
npx expo start

# Run on iOS Simulator
npx expo start --ios

# Run on Android Emulator
npx expo start --android
```

## Features

### MVP (Current)
- Morning lock screen with daily verse
- Prayer timer (5/10/15/30 min options)
- Streak tracking
- Emergency unlock with shame counter
- Settings (lock time, duration, notifications)
- Paywall with RevenueCat placeholder

### Coming Soon (Pro)
- Extended prayer times (30/60 min)
- Family accountability
- Custom prayer prompts
- Streak freezes
- Audio prayers

## Project Structure

```
prayerlock/
├── App.tsx                 # Entry point
├── app.json               # Expo config
├── package.json           # Dependencies
├── tsconfig.json          # TypeScript config
├── assets/                # App icons and splash
└── src/
    ├── components/        # Reusable UI components
    │   ├── Button.tsx
    │   ├── VerseCard.tsx
    │   ├── StatCard.tsx
    │   ├── CircularProgress.tsx
    │   └── DurationPicker.tsx
    ├── constants/         # App constants
    │   ├── colors.ts
    │   └── index.ts
    ├── context/           # React Context
    │   └── AppContext.tsx
    ├── data/              # Static data
    │   └── verses.json    # 30 Bible verses
    ├── hooks/             # Custom hooks
    │   └── useTimer.ts
    ├── navigation/        # React Navigation setup
    │   └── index.tsx
    ├── screens/           # App screens
    │   ├── LockScreen.tsx
    │   ├── TimerScreen.tsx
    │   ├── HomeScreen.tsx
    │   ├── SettingsScreen.tsx
    │   └── PaywallScreen.tsx
    └── utils/             # Helper functions
        └── storage.ts     # AsyncStorage helpers
```

## Tech Stack

- React Native + Expo SDK 52
- TypeScript
- React Navigation 6
- AsyncStorage (local persistence)
- Expo Haptics (vibration feedback)
- Expo Linear Gradient (UI)
- react-native-svg (timer circle)

## Required Assets

Before building, add these to `/assets`:
- `icon.png` (1024x1024) - App icon
- `splash.png` (1242x2436) - Splash screen
- `adaptive-icon.png` (1024x1024) - Android adaptive icon
- `favicon.png` (32x32) - Web favicon

## RevenueCat Integration

The paywall is set up for RevenueCat integration. To enable:

1. Create a RevenueCat account
2. Add your app products
3. Install the SDK: `npm install react-native-purchases`
4. Initialize in App.tsx with your API key
5. Update PaywallScreen.tsx to use RevenueCat purchase methods

## App Store Submission

### iOS
1. Generate assets with proper sizes
2. Fill out App Store Connect metadata
3. Submit for TestFlight review

### Android
1. Create keystore for signing
2. Build AAB: `eas build --platform android`
3. Upload to Google Play Console

## ASO Keywords
- prayer app
- morning devotion
- christian screen time
- phone detox faith
- daily bible verse
- prayer timer
- christian productivity

## License

Proprietary - All rights reserved
