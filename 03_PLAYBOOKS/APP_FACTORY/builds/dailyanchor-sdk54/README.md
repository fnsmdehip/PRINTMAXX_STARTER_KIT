# DailyAnchor - SDK 54 Upgrade

DailyAnchor is a spiritual companion app built with Expo SDK 54, React Native 0.81.5, and React 19.

## Upgrades from Original Version

This is the Expo SDK 54 version of DailyAnchor with the following updates:

- **Expo SDK**: Upgraded from ~51.0.0 to ~54.0.32
- **React**: Upgraded from 18.2.0 to 19.1.0
- **React Native**: Upgraded from 0.74.0 to 0.81.5
- **expo-router**: Upgraded from ~3.5.0 to ~6.0.22
- **Zustand**: Upgraded from ^4.4.7 to ^5.0.10
- **New Architecture**: Enabled with `newArchEnabled: true`

## Tech Stack

- **Frontend Framework**: React Native with Expo
- **Routing**: expo-router 6.x
- **State Management**: Zustand 5.x
- **Storage**: AsyncStorage 2.2.0
- **Utilities**: date-fns for date manipulation

## Project Structure

```
dailyanchor-sdk54/
├── app/                           # Expo Router app directory
│   ├── (tabs)/                   # Tab-based navigation
│   │   ├── index.tsx             # Today's screen
│   │   ├── journal.tsx           # Journal entries
│   │   ├── progress.tsx          # Progress tracking
│   │   ├── settings.tsx          # User settings
│   │   └── _layout.tsx           # Tab layout
│   ├── _layout.tsx               # Root layout
│   ├── onboarding.tsx            # Onboarding flow
│   ├── paywall.tsx               # Premium subscription
│   ├── privacy.tsx               # Privacy policy
│   └── terms.tsx                 # Terms of service
├── src/
│   ├── components/               # React components
│   │   ├── common/              # Reusable UI components
│   │   ├── habits/              # Habit-related components
│   │   ├── journal/             # Journal components
│   │   ├── streaks/             # Streak display
│   │   └── paywall/             # Premium paywall
│   ├── store/                    # Zustand state management
│   │   ├── habitStore.ts        # Habit state
│   │   ├── journalStore.ts      # Journal state
│   │   ├── settingsStore.ts     # Settings state
│   │   └── verseStore.ts        # Daily verse state
│   ├── types/                    # TypeScript type definitions
│   ├── utils/                    # Utility functions
│   │   ├── constants.ts         # App constants
│   │   └── dateUtils.ts         # Date manipulation
│   ├── hooks/                    # Custom React hooks
│   └── services/                 # External services
├── assets/                       # App assets (icons, images)
├── package.json                  # Dependencies
├── app.json                      # Expo configuration
├── tsconfig.json                 # TypeScript config
└── babel.config.js               # Babel configuration
```

## Getting Started

### Install Dependencies

```bash
npm install
```

### Run on iOS

```bash
npm run ios
```

### Run on Android

```bash
npm run android
```

### Run on Web

```bash
npm run web
```

## Key Features

- Daily devotional verses with Bible API integration
- Habit tracking with streak counters
- Gratitude journaling
- User settings and preferences
- Premium features with paywall
- Onboarding flow
- Local data persistence with AsyncStorage

## State Management

All state is managed with Zustand stores located in `src/store/`:

- **settingsStore**: User preferences and app settings
- **habitStore**: Habit data and completion tracking
- **journalStore**: Journal entries
- **verseStore**: Daily Bible verses (cached)

## Notable Changes from Original

1. **New Architecture Enabled**: The app uses React Native's New Architecture for better performance
2. **React 19**: Latest React features and improvements
3. **Modern Zustand**: Version 5 with improved TypeScript support
4. **Updated expo-router**: Version 6 with better routing capabilities

## Building for Production

### iOS

```bash
# Using EAS (Expo Application Services)
eas build --platform ios
```

### Android

```bash
# Using EAS
eas build --platform android
```

## Notes

- Date-fns is used for all date manipulation operations
- The Bible API is used for daily verse fetching with caching
- All user data is stored locally on device via AsyncStorage
- RevenueCat API keys need to be configured for premium features

## Environment Variables

Create a `.env` file with the following:

```
REVENUECAT_IOS_API_KEY=your_key_here
REVENUECAT_ANDROID_API_KEY=your_key_here
```

## Support

For more information about Expo SDK 54, visit: https://docs.expo.dev/
