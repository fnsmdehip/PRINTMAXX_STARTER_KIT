# PromptVault SDK 54 Setup Guide

## Overview

PromptVault SDK 54 is a complete upgrade of the PromptVault app to use modern Expo SDK 54, Expo Router, and React 19. The original app used @react-navigation; this version uses the modern file-based Expo Router approach.

## What Was Upgraded

### Technology Stack
| Component | Old | New |
|-----------|-----|-----|
| Expo | ~50.0.0 | ~54.0.32 |
| React | 18.2.0 | 19.1.0 |
| React Native | 0.73.6 | 0.81.5 |
| Navigation | @react-navigation | expo-router 6.0.22 |
| Zustand | 4.4.7 | 5.0.10 |
| New Architecture | false | true |

### Key Improvements
1. **File-based routing** - No more manual navigator configuration
2. **React 19** - Latest features and performance improvements
3. **New Architecture** - Enabled for better performance
4. **Simpler structure** - Less boilerplate, more maintainable
5. **Better async handling** - Zustand v5 with improved persistence

## Quick Start

### Step 1: Install Dependencies
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds/promptvault-sdk54
npm install
```

**Expected output:**
```
added 500+ packages
up to date, audited 501 packages in 30s
```

### Step 2: Copy Assets (IMPORTANT)
The image assets need to be copied from the original PromptVault:

```bash
# Copy all image files
cp ../promptvault/assets/* ./assets/

# Verify files exist
ls -la assets/
```

**Required files:**
- `assets/icon.png` (App home screen icon)
- `assets/splash.png` (Splash screen on launch)
- `assets/adaptive-icon.png` (Android adaptive icon)
- `assets/favicon.png` (Web favicon)

### Step 3: Verify Installation
```bash
# Check that Expo CLI recognizes the app
npx expo --version

# Check package versions
npm list expo react react-native zustand
```

### Step 4: Launch on iOS Simulator
```bash
npm run ios
```

This will:
1. Start the Expo dev server
2. Automatically open iOS Simulator
3. Load the PromptVault app

**Expected:** Onboarding screen appears (first launch)

### Step 5: Launch on Android Emulator
```bash
npm run android
```

## App Structure

### Entry Points

**`app/_layout.tsx`** - Root layout
- Configures Stack navigation
- Manages StatusBar
- Handles splash screen

**`app/index.tsx`** - App initialization
- Checks onboarding status
- Redirects to onboarding or home
- Shows loading state while checking

### Tab Navigation

**`app/(tabs)/_layout.tsx`** - Tab configuration
- Defines 4 tabs: Home, Favorites, Improve, Settings
- Configures tab bar styling
- Sets active/inactive colors

**`app/(tabs)/home.tsx`** - Library tab
- Browse all prompts
- Search and filter
- Create custom prompts

**`app/(tabs)/favorites.tsx`** - Favorites tab
- View saved prompts
- Quick access to most used
- Managed by Zustand store

**`app/(tabs)/improve.tsx`** - Improvement tool
- Enhance prompt quality
- AI-powered suggestions

**`app/(tabs)/settings.tsx`** - Settings tab
- Subscription management
- Privacy/Terms
- About & feedback

### Screens (in `src/screens/`)

These are reusable screen components that render in the app/ routes:

- **HomeScreen** - Main library interface
- **FavoritesScreen** - Saved prompts
- **ImproveScreen** - Enhancement tool
- **SettingsScreen** - User preferences
- **PromptDetailScreen** - Full prompt view (modal)
- **OnboardingScreen** - First-time setup
- **PrivacyPolicyScreen** - Legal info
- **TermsScreen** - Terms of service

### Components (in `src/components/`)

- **PromptCard** - Individual prompt display
- **SearchBar** - Search input
- **CategoryChip** - Category filter buttons
- **CreatePromptModal** - Add custom prompt dialog
- **Paywall** - Subscription UI
- **AdBanner** - Ad display for free users
- **Toast** - Notification messages

### State Management (in `src/stores/`)

All state uses Zustand with AsyncStorage persistence:

**usePromptStore** - Prompt data
- All available prompts
- User-created prompts
- Search query & results
- Selected category filter
- Methods: setSearchQuery, setSelectedCategory, addUserPrompt

**useFavoriteStore** - Favorites
- List of favorited prompt IDs
- Persisted to AsyncStorage
- Methods: toggleFavorite, isFavorite, addFavorite, removeFavorite

**useSubscriptionStore** - Subscription state
- Pro/free tier status
- Trial active status
- Expiration dates
- Methods: startTrial, upgradeToPro, restorePurchases

**useOnboardingStore** - Onboarding
- Onboarding completion status
- User preferences (use cases, experience level)
- Persisted to AsyncStorage
- Methods: completeOnboarding, setExperience, getPreferredCategories

## Key Differences from Original

### Navigation

**Before (React Navigation):**
```typescript
// Manual stack + tab configuration
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function RootNavigator() {
  // Manual config...
}
```

**Now (Expo Router):**
```
app/
├── _layout.tsx      # <Stack />
├── index.tsx        # Home route
├── onboarding.tsx   # Onboarding route
└── (tabs)/          # Tab group
    ├── _layout.tsx  # <Tabs />
    ├── home.tsx
    ├── favorites.tsx
    └── settings.tsx
```

### Onboarding

**Before:**
```typescript
// Manual AsyncStorage management
const [onboarding, setOnboarding] = useState(false);
useEffect(() => {
  AsyncStorage.getItem('promptvault_onboarding').then(...)
}, [])
```

**Now:**
```typescript
// Zustand store with automatic persistence
const onboarding = useOnboardingStore(s => s.onboardingCompleted);
// Automatically loads from AsyncStorage on app start
```

## Testing the App

### Test Onboarding
1. Launch the app
2. First time: Onboarding screen appears
3. Select use cases and experience level
4. Click "Get Started"
5. Should navigate to Home tab

### Test Search
1. Go to Home tab
2. Type in search bar
3. Verify prompts filter in real-time

### Test Favorites
1. On any prompt card, tap heart icon
2. Go to Favorites tab
3. Verify prompt appears
4. Tap heart again to remove

### Test Settings
1. Go to Settings tab
2. Verify subscription section shows
3. Tap privacy/terms links
4. Go back (should work)

### Test Persistence
1. Add favorites
2. Close app completely
3. Reopen app
4. Verify favorites still there (AsyncStorage persistence)

## Troubleshooting

### Issue: "Module not found: expo-router"
```
Error: Cannot find module 'expo-router'
```
**Solution:**
```bash
npm install
npm list expo-router  # Should show ~6.0.22
```

### Issue: "Cannot find module '../src/screens/HomeScreen'"
**Solution:** Verify file exists:
```bash
ls src/screens/HomeScreen.tsx
```

### Issue: App crashes on startup
**Check:**
1. Assets directory exists: `ls -la assets/`
2. Required image files present
3. No TypeScript errors: `npm run type-check` (if available)

### Issue: Favorites not persisting
**Check:**
1. AsyncStorage has permission to write (Android)
2. App hasn't been cleared of data (iOS Settings > PromptVault > Clear)
3. Zustand store is properly initialized

### Issue: Onboarding screen appears every time
**Check:**
1. Storage is working: `await AsyncStorage.getItem('promptvault_onboarding')`
2. `useOnboardingStore.completeOnboarding()` was called
3. AsyncStorage isn't being cleared by system

## Dependencies

### Core Dependencies
```json
{
  "expo": "~54.0.32",
  "expo-router": "~6.0.22",
  "expo-splash-screen": "~31.0.13",
  "expo-status-bar": "~3.0.9",
  "react": "19.1.0",
  "react-native": "0.81.5",
  "zustand": "^5.0.10"
}
```

### UI & Navigation
```json
{
  "@expo/vector-icons": "^15.0.3",
  "react-native-safe-area-context": "~5.6.0",
  "react-native-screens": "~4.16.0"
}
```

### Storage
```json
{
  "@react-native-async-storage/async-storage": "2.2.0"
}
```

### Search & Utilities
```json
{
  "fuse.js": "^7.0.0"
}
```

## Next Steps

1. **Run app locally** - Verify all screens load correctly
2. **Test core features** - Search, favorites, onboarding
3. **Check console** - Look for warnings/errors
4. **Profile performance** - Use Expo DevTools
5. **Prepare for distribution**:
   - Update app icon (replace `assets/icon.png`)
   - Update splash screen
   - Configure app.json with correct bundle IDs
   - Test on physical devices

## Development Workflow

### Hot Reload
Changes to files automatically reload:
- TypeScript changes auto-reload
- Avoid full restart for most edits
- Clear cache if issues: Press `c` in dev terminal

### Debug
```bash
# Open DevTools
# Press Shift+D in Terminal
# Select "Open debugger"
```

### Build Locally
```bash
# For review before shipping
eas build --local --platform ios
eas build --local --platform android
```

## Resources

- **Expo Router docs**: https://docs.expo.dev/routing/introduction/
- **React 19**: https://react.dev/blog/2024/12/19/react-19
- **Zustand**: https://github.com/pmndrs/zustand
- **SDK 54 changelog**: https://expo.dev/changelog

## Support

If you encounter issues:
1. Check this guide's Troubleshooting section
2. Review `SDK54_UPGRADE.md` for migration details
3. Clear cache: `npm cache clean --force && rm -rf node_modules`
4. Reinstall: `npm install`
5. Clear app cache: `expo start -c`
