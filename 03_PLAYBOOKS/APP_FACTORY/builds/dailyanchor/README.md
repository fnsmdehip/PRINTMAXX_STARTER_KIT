# DailyAnchor

A faith-based daily habit tracker and journaling app built with Expo.

## Quick Start

```bash
# Install dependencies
npm install

# Generate placeholder assets (optional, uses ImageMagick if available)
chmod +x scripts/generate-assets.sh
./scripts/generate-assets.sh

# Or manually add PNG images to assets/:
# - icon.png (1024x1024)
# - adaptive-icon.png (1024x1024)
# - splash.png (1284x2778)
# - favicon.png (32x32)

# Start the development server
npx expo start --ios
```

## Project Structure

```
dailyanchor/
├── app/                    # Expo Router pages
│   ├── _layout.tsx        # Root layout with providers
│   ├── (tabs)/            # Tab navigation group
│   │   ├── _layout.tsx    # Tab bar configuration
│   │   ├── index.tsx      # Today screen (home)
│   │   ├── journal.tsx    # Journal screen
│   │   ├── progress.tsx   # Progress/stats screen
│   │   └── settings.tsx   # Settings screen
│   ├── paywall.tsx        # Premium paywall modal
│   ├── onboarding.tsx     # Onboarding flow
│   ├── privacy.tsx        # Privacy policy
│   └── terms.tsx          # Terms of service
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── common/        # Button, Card, DailyVerse
│   │   ├── habits/        # HabitChecklist, HabitItem
│   │   ├── journal/       # JournalEntryForm, GratitudeInput
│   │   ├── paywall/       # PremiumFeatureCard, PricingOption
│   │   └── streaks/       # StreakCounter, StreakCalendar
│   ├── store/             # Zustand state management
│   ├── types/             # TypeScript interfaces
│   └── utils/             # Constants and utilities
├── assets/                # App icons and splash screen
├── app.json               # Expo configuration
└── package.json
```

## Features

- Daily devotional verses (Bible API)
- Habit tracking with streaks
- Gratitude journaling
- Progress statistics and calendar view
- Premium subscription (RevenueCat integration ready)
- Onboarding flow

## Tech Stack

- **Framework:** Expo SDK 51 (managed workflow)
- **Navigation:** Expo Router (file-based routing)
- **State:** Zustand with AsyncStorage persistence
- **UI:** React Native core components
- **Subscriptions:** RevenueCat (integration placeholder)

## Bundle ID

- iOS: `com.printmaxx.dailyanchor`
- Android: `com.printmaxx.dailyanchor`

## Scripts

```bash
npm start          # Start Expo dev server
npm run ios        # Start on iOS simulator
npm run android    # Start on Android emulator
npm run web        # Start web version
npm run typecheck  # Run TypeScript checks
npm run lint       # Run ESLint
```

## Next Steps

1. Add placeholder PNG assets to `assets/` folder
2. Run `npm install` to install dependencies
3. Run `npx expo start --ios` to launch on iOS simulator
4. Replace RevenueCat API keys in `src/utils/constants.ts`
5. Set up EAS Build for production builds
