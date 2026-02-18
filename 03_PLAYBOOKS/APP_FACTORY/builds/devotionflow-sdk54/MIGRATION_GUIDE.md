# DevotionFlow SDK 54 Migration Guide

## Overview

The original DevotionFlow app has been upgraded from Expo SDK 51 to SDK 54, with React Native 0.81.5 and React 19.1.0.

## What Changed

### SDK & React Versions
- **Expo SDK**: 51 → 54
- **React Native**: 0.74.0 → 0.81.5
- **React**: 18.2.0 → 19.1.0

### Package Updates

| Package | Old | New | Notes |
|---------|-----|-----|-------|
| expo | ~51.0.0 | ~54.0.32 | Major SDK version |
| expo-router | ~3.5.0 | ~6.0.22 | Major version bump |
| expo-splash-screen | ~0.27.0 | ~31.0.13 | Major version |
| expo-constants | ~16.0.0 | ~18.0.13 | Major version |
| expo-haptics | ~13.0.0 | ~15.0.8 | Major version |
| expo-linking | ~6.3.0 | ~8.0.11 | Major version |
| expo-status-bar | ~1.12.0 | ~3.0.9 | Major version |
| react-native-safe-area-context | 4.10.0 | ~5.6.0 | Major version |
| react-native-screens | 3.31.0 | ~4.16.0 | Major version |
| zustand | ^4.5.0 | ^5.0.10 | Major version |
| @expo/vector-icons | ^14.0.0 | ^15.0.3 | Minor update |
| @react-native-async-storage/async-storage | 1.23.1 | 2.2.0 | Major update |
| date-fns | ^3.0.0 | ^3.0.0 | No change |

### Removed Dependencies
- **react-native-mmkv** - Removed, using AsyncStorage instead
- **react-native-gesture-handler** - Not needed for core functionality
- **react-native-reanimated** - Not needed for core functionality
- **react-native-notifications** - Removed, can be re-added if needed
- **react-native-purchases** - Removed, can be re-added if needed

## Code Changes

### lib/storage.ts

**Before (SDK 51 with MMKV):**
```typescript
import { MMKV } from 'react-native-mmkv';

export const storage = new MMKV({
  id: 'devotionflow-storage',
});
```

**After (SDK 54 with AsyncStorage):**
```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';

// All storage methods now async
export const localStore = {
  getString: async (key: string): Promise<string | null> => {
    return await AsyncStorage.getItem(key);
  },
  // ... etc
};
```

**Impact**: All storage calls are now async and must be awaited.

### app.json

**Key Changes:**
- Added `"newArchEnabled": true` to use React Native's new architecture
- Added `"edgeToEdgeEnabled": true` for Android
- Kept all existing configuration (icon, splash, plugins, etc.)

## Integration Notes

### Asset Files Required

Place these images in `assets/images/`:
- `icon.png` - App icon (1024x1024)
- `splash.png` - Splash screen (1024x1024)
- `adaptive-icon.png` - Android adaptive icon
- `favicon.png` - Web favicon

### Optional: Re-add Notifications

If you need push notifications, install the compatible version:

```bash
npm install expo-notifications@~15.0.0
```

Then restore `lib/notifications.ts` logic.

### Optional: Re-add RevenueCat Purchases

If you need in-app purchases:

```bash
npm install react-native-purchases@^10.0.0
```

Then update `lib/revenuecat.ts` with your API keys.

### Optional: Re-add Gesture Handler & Animations

For advanced gesture handling:

```bash
npm install react-native-gesture-handler@~2.21.0 react-native-reanimated@~4.1.0
```

## Testing Checklist

- [ ] `npm install` completes without errors
- [ ] `npm run ios` launches in iOS Simulator
- [ ] App initializes and shows splash screen
- [ ] Navigate through all tabs (Home, Devotions, Journal, Profile)
- [ ] Zustand stores persist data correctly
- [ ] No console errors or warnings
- [ ] Onboarding flow completes
- [ ] Devotional content displays properly
- [ ] Prayer journal entries can be created
- [ ] User streak tracking works

## Breaking Changes

### 1. Storage is Now Async

All storage operations must now be awaited:

```typescript
// Old (sync)
const name = localStore.getString('user_name');

// New (async)
const name = await localStore.getString('user_name');
```

### 2. Zustand 5.0 Updates

Check your store selectors if you use advanced features. Basic usage remains the same.

### 3. React 19 Updates

Functional components work the same. Props spreading and keys behavior unchanged.

## Troubleshooting

### "Module not found" Errors

Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

### Metro Bundler Issues

Reset Metro cache:
```bash
npm start -- --reset-cache
```

### iOS Build Issues

Clean Xcode build folder:
```bash
npm run ios -- --clear
```

## Resources

- [Expo SDK 54 Changelog](https://docs.expo.dev/workflow/sdk-changelog/)
- [React Native 0.81 Upgrade Guide](https://react-native.dev/)
- [Zustand 5.0 Migration](https://github.com/pmndrs/zustand/releases/tag/v5.0.0)

## Next Steps

1. Add asset files (icon, splash, etc.)
2. Configure RevenueCat API keys if needed
3. Test all app flows in iOS Simulator
4. Build and test on physical iOS devices
5. Repeat process for Android if needed
