# DevotionFlow SDK 54

DevotionFlow app upgraded to Expo SDK 54 with React Native 0.81.5 and React 19.1.0.

## Quick Start

```bash
cd devotionflow-sdk54
npm install
npm run ios  # Launch in iOS Simulator
```

## Project Structure

- **app/** - Expo Router screens and layouts
- **store/** - Zustand state management stores
- **lib/** - Utility functions (storage, notifications, RevenueCat)
- **constants/** - Theme, devotions content, paywall config
- **assets/** - Images and app assets

## Key Upgrades from Original DevotionFlow

- Expo SDK: 51 → 54
- React Native: 0.74.0 → 0.81.5
- React: 18.2.0 → 19.1.0
- expo-router: 3.5.0 → 6.0.22
- expo-notifications: 0.28.0 → 18.0.6
- zustand: 4.5.0 → 5.0.10
- Removed react-native-mmkv (use AsyncStorage instead)
- Updated all expo-* packages to compatible versions

## Config Changes

- **app.json**: Updated for SDK 54, enabled `newArchEnabled`
- **package.json**: All dependencies updated to SDK 54 compatible versions
- **lib/storage.ts**: Simplified to use AsyncStorage only (MMKV removed)

## Testing

1. Run `npm install` to verify all dependencies resolve
2. Launch with `npm run ios` for iOS Simulator testing
3. Check screens render correctly (Tabs, Home, Devotions, Journal, Profile)
4. Verify navigation works between routes

## Notes

- Place asset files (icon.png, splash.png, adaptive-icon.png) in `assets/images/`
- RevenueCat API keys need to be configured in `lib/revenuecat.ts`
- Notification permissions are handled in the onboarding flow
- All Zustand stores persist using AsyncStorage
