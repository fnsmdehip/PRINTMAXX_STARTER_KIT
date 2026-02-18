# PromptVault SDK 54 Upgrade

This is the Expo SDK 54 version of PromptVault, built with modern React Native patterns.

## Upgrade Summary

**SDK 54 Improvements:**
- React 19.1.0 (up from 18.2.0)
- React Native 0.81.5 (up from 0.73.6)
- Expo Router 6.0.22 (replaces @react-navigation)
- New Architecture enabled (`newArchEnabled: true`)
- Zustand 5.0.10 (up from 4.4.7)
- Simplified navigation with file-based routing

## Key Differences from Original

### Navigation
**Old (React Navigation):**
- Used `@react-navigation/bottom-tabs` and `@react-navigation/native-stack`
- Manual navigation configuration in `RootNavigator.tsx`

**New (Expo Router):**
- File-based routing in `app/` directory
- Automatic tab navigation with `(tabs)` directory
- Simpler, more maintainable structure

### File Structure
```
app/
├── _layout.tsx           # Root layout with Stack
├── index.tsx             # Initial route handler
├── onboarding.tsx        # Onboarding screen
└── (tabs)/              # Tab navigation group
    ├── _layout.tsx      # Tab layout config
    ├── home.tsx
    ├── favorites.tsx
    ├── improve.tsx
    └── settings.tsx
```

### Dependencies Removed
- `@react-navigation/native` (3 packages)
- `@react-navigation/bottom-tabs`
- `@react-navigation/native-stack`
- `react-native-safe-area-context` (built into expo-router)
- `expo-font` (removed from plugins)

### Dependencies Added/Updated
- `expo-router@~6.0.22`
- `react@19.1.0`
- `react-native@0.81.5`
- `zustand@^5.0.10`

## Setup Instructions

### 1. Install Dependencies
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds/promptvault-sdk54
npm install
```

### 2. Copy Assets (Manual)
The assets directory needs image files from the original:
```bash
cp -r ../promptvault/assets/* ./assets/
```

The following files are needed:
- `assets/icon.png`
- `assets/splash.png`
- `assets/adaptive-icon.png`
- `assets/favicon.png`

### 3. Verify Structure
```bash
npm list expo react react-native
```

Expected versions:
- expo: 54.0.32
- react: 19.1.0
- react-native: 0.81.5
- zustand: 5.0.10

### 4. Test on iOS Simulator
```bash
npm run ios
```

### 5. Test on Android Emulator
```bash
npm run android
```

## Store Management

All state management uses Zustand v5 with persist middleware:

- **usePromptStore**: Prompt data, filtering, searching
- **useFavoriteStore**: Favorite prompt IDs (persisted to AsyncStorage)
- **useSubscriptionStore**: Pro subscription state, trial status (persisted)
- **useOnboardingStore**: Onboarding preferences, completion status (persisted)

## Important Upgrade Notes

### React 19 Compatibility
- All screens use React 19 patterns
- No changes needed to existing component code
- Event handlers work as before

### New Architecture
- Enabled via `newArchEnabled: true` in app.json
- Better performance on newer iOS/Android devices
- Backwards compatible

### Onboarding Flow
- Uses `useOnboardingStore` instead of AsyncStorage directly
- Redirect logic in `app/index.tsx` checks state
- Automatic routing to onboarding on first launch

### SafeAreaView
- Expo Router handles safe area automatically in `_layout.tsx`
- Individual screens don't need to import SafeAreaProvider

## Migration Checklist

- [x] Create SDK 54 directory structure
- [x] Update package.json with SDK 54 dependencies
- [x] Migrate to Expo Router file-based routing
- [x] Create app/ directory with layout files
- [x] Implement store-based onboarding state
- [x] Copy all source files (screens, components, stores, services)
- [x] Copy prompt data
- [ ] Copy image assets manually
- [ ] Run `npm install`
- [ ] Test on iOS Simulator
- [ ] Test on Android Emulator
- [ ] Verify all features work (search, favorites, settings, etc.)

## Common Issues & Solutions

### Issue: "Module not found: expo-router"
**Solution:** Run `npm install` to install dependencies

### Issue: App crashes on startup
**Solution:** Check that `assets/` directory exists with required image files

### Issue: Navigation not working
**Solution:** Verify `app/` directory structure matches the file paths in screens

### Issue: Store state not persisting
**Solution:** Ensure AsyncStorage has permissions (Android: add to AndroidManifest.xml)

## Performance Notes

SDK 54 provides:
- Faster JavaScript execution (React 19)
- Improved native module loading
- Better memory management with New Architecture
- Smaller bundle size (~15% reduction in some cases)

## Next Steps

1. Copy assets from promptvault to promptvault-sdk54
2. Run `npm install`
3. Launch iOS Simulator with `npm run ios`
4. Verify all screens load and navigate correctly
5. Test key features:
   - Search functionality
   - Category filtering
   - Favorites saving/loading
   - Onboarding flow
   - Settings persistence

## References

- Expo Router docs: https://docs.expo.dev/routing/introduction/
- React 19 migration: https://react.dev/blog/2024/12/19/react-19
- Zustand v5: https://github.com/pmndrs/zustand/releases/tag/v5.0.0
