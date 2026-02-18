# DevotionFlow

A faith/devotional app built with Expo SDK 51 and React Native.

## Features

- **Daily Devotionals**: Fresh content every day with Scripture, reflection, and prayer
- **Prayer Journal**: Track your prayers and mark them as answered
- **Bible Verse of the Day**: Curated Scripture to start your morning
- **Streak Tracking**: Build consistent devotional habits
- **Daily Reminders**: Customizable notification times
- **RevenueCat Integration**: Subscription management ready

## Tech Stack

- **Framework**: Expo SDK 51 (React Native 0.74)
- **Navigation**: Expo Router 3.5
- **State**: Zustand with persistence
- **Storage**: MMKV + AsyncStorage
- **Payments**: RevenueCat (react-native-purchases)
- **Styling**: StyleSheet with custom theme

## Getting Started

### Prerequisites

- Node.js 18+
- Expo CLI
- iOS Simulator or Android Emulator (or physical device)

### Installation

```bash
cd devotionflow
npm install
```

### Running the App

```bash
# Start development server
npx expo start

# Run on iOS
npx expo start --ios

# Run on Android
npx expo start --android
```

## Project Structure

```
devotionflow/
├── app/                    # Expo Router screens
│   ├── (onboarding)/       # Onboarding flow
│   │   ├── welcome.tsx
│   │   ├── faith-background.tsx
│   │   ├── notifications.tsx
│   │   └── paywall.tsx
│   ├── (tabs)/             # Main tab navigation
│   │   ├── index.tsx       # Home
│   │   ├── devotions.tsx   # Devotion library
│   │   ├── journal.tsx     # Prayer journal
│   │   └── profile.tsx     # Settings/profile
│   ├── devotion/[id].tsx   # Devotion detail
│   ├── paywall.tsx         # Subscription modal
│   ├── privacy.tsx         # Privacy policy
│   └── terms.tsx           # Terms of service
├── components/             # Reusable components
│   └── ui/                 # Basic UI components
├── constants/              # App configuration
│   ├── theme.ts            # Colors, spacing, typography
│   ├── paywall.ts          # Subscription config
│   └── devotions.ts        # Devotional content
├── lib/                    # Utilities
│   ├── storage.ts          # MMKV storage
│   ├── revenuecat.ts       # Subscription logic
│   └── notifications.ts    # Push notifications
├── store/                  # Zustand stores
│   ├── userStore.ts        # User state & streaks
│   └── journalStore.ts     # Prayer entries
└── assets/                 # Images and fonts
```

## Configuration

### Bundle ID

- iOS: `com.printmaxx.devotionflow`
- Android: `com.printmaxx.devotionflow`

### RevenueCat Setup

1. Create products in App Store Connect / Google Play Console
2. Add products to RevenueCat dashboard
3. Update API keys in `lib/revenuecat.ts`
4. Configure entitlement ID: `premium`

### Product IDs

- Weekly: `devotionflow_weekly_499` ($4.99/week)
- Annual: `devotionflow_annual_3999` ($39.99/year)

## Monetization

- 7-day free trial on weekly plan
- Soft paywall after onboarding
- Hard paywall after trial expires or 5 devotions

## Assets Required

Before building, add these assets to `assets/images/`:

- `icon.png` (1024x1024) - App icon
- `splash.png` (1284x2778) - Splash screen
- `adaptive-icon.png` (1024x1024) - Android adaptive icon
- `notification-icon.png` (96x96) - Notification icon

Use warm cream/brown tones (#F5F0E8, #8B7355) to match the theme.

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

## Color Theme

- Primary: `#8B7355` (Warm brown)
- Secondary: `#D4A574` (Soft gold)
- Accent: `#6B8E7B` (Sage green)
- Background: `#F5F0E8` (Warm cream)
- Prayer: `#7B6BA5` (Soft purple)
- Verse: `#5C7A8A` (Calm blue)

## License

Private - PRINTMAXX
