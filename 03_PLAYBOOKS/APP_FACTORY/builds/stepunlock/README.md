# StepUnlock

Block distracting apps until you hit your daily step goal. No steps, no scrolling.

## What it does

StepUnlock connects to your phone's health data (HealthKit on iOS, Google Fit on Android) and blocks apps you select until you've walked enough steps. Set your goal, pick the apps to block, and the app handles the rest.

When you hit your step goal, your apps unlock automatically.

## Features

- Set daily step goals from 1,000 to 20,000 steps
- Block any apps you choose (social media, games, etc.)
- Real-time progress tracking with visual ring
- Automatic unlock when goal is reached
- Streak tracking to build the habit
- Emergency unlock for genuine emergencies (resets streak)
- Background step syncing

## Tech Stack

- Expo SDK 51 (managed workflow)
- expo-router for navigation
- TypeScript
- Zustand for state management
- HealthKit (iOS) / Google Fit (Android)
- RevenueCat for subscriptions
- react-native-svg for progress ring

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npx expo start

# Run on iOS simulator (press i)
npx expo start --ios

# Run on Android emulator (press a)
npx expo start --android

# Run tests
npm test
```

## Project Structure

```
stepunlock/
├── app/                    # Expo Router screens
│   ├── _layout.tsx         # Root layout
│   ├── index.tsx           # Entry redirect
│   ├── onboarding.tsx      # Onboarding flow
│   ├── paywall.tsx         # Subscription paywall
│   ├── emergency-unlock.tsx
│   ├── privacy-policy.tsx
│   ├── terms.tsx
│   └── (tabs)/             # Tab navigation
│       ├── _layout.tsx     # Tab layout
│       ├── index.tsx       # Home (Today)
│       ├── progress.tsx    # Progress stats
│       └── settings.tsx    # Settings
├── src/
│   ├── components/         # Reusable UI components
│   ├── services/           # Step tracking, blocking, subscriptions
│   ├── stores/             # Zustand state management
│   ├── types/              # TypeScript definitions
│   └── utils/              # Date utils, constants
├── assets/                 # App icons, splash, etc.
├── app.json                # Expo configuration
└── package.json
```

## Development Notes

### Health Data (HealthKit/Google Fit)

Health data integration requires a **development build** (not Expo Go):

```bash
# Create development build
npx expo prebuild
npx expo run:ios  # or run:android
```

In Expo Go, the app uses mock step data for testing.

### App Blocking

Real app blocking functionality requires native modules and is only available in development builds. The Expo Go version uses simulated blocking for testing.

### RevenueCat Setup

1. Create a RevenueCat account
2. Set up your app and products
3. Update API keys in `src/utils/constants.ts`:
   - `REVENUECAT_API_KEY_IOS`
   - `REVENUECAT_API_KEY_ANDROID`

## Building for Production

```bash
# Install EAS CLI
npm install -g eas-cli

# Configure EAS
eas build:configure

# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android
```

## Before Building

See SUBMISSION_CHECKLIST.md for all manual setup steps including:
- RevenueCat API keys
- HealthKit/Google Fit configuration
- App Store/Play Store setup
- Privacy policy requirements

## Assets Required

Before submitting to app stores, add these to `/assets`:
- `icon.png` (1024x1024) - App icon
- `splash.png` (1284x2778) - Splash screen
- `adaptive-icon.png` (1024x1024) - Android adaptive icon

See `assets/ASSET_INSTRUCTIONS.md` for details.

## Monetization

- 3-day free trial
- Monthly: $7.99
- Annual: $39.99 (58% savings)

Hard paywall after trial ends.

## Scripts

```bash
npm start          # Start Expo dev server
npm run ios        # Run on iOS
npm run android    # Run on Android
npm test           # Run tests
npm run lint       # Lint code
npm run typecheck  # TypeScript check
npm run prebuild   # Generate native projects
```

## License

Proprietary. Not for redistribution.
