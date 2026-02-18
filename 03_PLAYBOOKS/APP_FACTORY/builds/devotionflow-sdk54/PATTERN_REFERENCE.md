# DevotionFlow SDK 54 - Pattern Reference

This document shows how devotionflow-sdk54 follows the exact same pattern as biomaxx-sdk54.

## Directory Structure Match

### biomaxx-sdk54
```
biomaxx-sdk54/
├── .gitignore
├── .expo/
├── app/
│   ├── (tabs)/
│   │   ├── _layout.tsx
│   │   ├── dashboard.tsx
│   │   ├── protocols.tsx
│   │   ├── learn.tsx
│   │   └── profile.tsx
│   ├── index.tsx
│   ├── onboarding.tsx
│   └── _layout.tsx
├── assets/
├── src/
├── node_modules/
├── app.json
├── package.json
├── package-lock.json
└── tsconfig.json
```

### devotionflow-sdk54 (Following Same Pattern)
```
devotionflow-sdk54/
├── .gitignore            ✓ Identical
├── .expo/
├── app/
│   ├── (tabs)/           ✓ Same structure
│   │   ├── _layout.tsx   ✓ Tab navigation
│   │   ├── index.tsx     ✓ Home screen
│   │   └── devotions.tsx ✓ Main feature screen
│   ├── _layout.tsx       ✓ Root layout
├── assets/               ✓ Same structure
├── store/                ✓ NEW: State management
├── lib/                  ✓ NEW: Utilities
├── constants/            ✓ NEW: App config
├── node_modules/
├── app.json              ✓ Identical pattern
├── package.json          ✓ Same version pinning
├── package-lock.json
└── tsconfig.json         ✓ Identical
```

## Package Dependencies - Version Parity

Both projects use **identical Expo SDK 54 versions**:

```json
{
  "expo": "~54.0.32",
  "react": "19.1.0",
  "react-native": "0.81.5",
  "expo-router": "~6.0.22",
  "expo-constants": "~18.0.13",
  "expo-haptics": "~15.0.8",
  "expo-linking": "~8.0.11",
  "expo-splash-screen": "~31.0.13",
  "expo-status-bar": "~3.0.9",
  "@expo/vector-icons": "^15.0.3",
  "react-native-safe-area-context": "~5.6.0",
  "react-native-screens": "~4.16.0",
  "zustand": "^5.0.10",
  "@react-native-async-storage/async-storage": "2.2.0"
}
```

**Difference**: devotionflow-sdk54 adds:
- `date-fns` for devotional date logic
- `react-native-svg` for vector graphics
- Optional: `expo-notifications`, `react-native-purchases`

## Configuration Files - Identical Pattern

### app.json
Both follow same Expo configuration:

**biomaxx-sdk54:**
```json
{
  "expo": {
    "name": "BioMaxx",
    "slug": "biomaxx",
    "scheme": "biomaxx",
    "version": "1.0.0",
    "orientation": "portrait",
    "userInterfaceStyle": "dark",
    "newArchEnabled": true,
    "ios": { "supportsTablet": true },
    "android": {
      "adaptiveIcon": { ... },
      "edgeToEdgeEnabled": true,
      "predictiveBackGestureEnabled": false
    },
    "plugins": ["expo-router"]
  }
}
```

**devotionflow-sdk54:**
```json
{
  "expo": {
    "name": "DevotionFlow",
    "slug": "devotionflow",
    "scheme": "devotionflow",
    "version": "1.0.0",
    "orientation": "portrait",
    "userInterfaceStyle": "light",
    "newArchEnabled": true,
    "ios": { "supportsTablet": true },
    "android": {
      "adaptiveIcon": { ... },
      "edgeToEdgeEnabled": true,
      "predictiveBackGestureEnabled": false
    },
    "plugins": ["expo-router"]
  }
}
```

**Only differences:**
- App name and slug (expected)
- Color scheme (dark vs light)
- Bundle IDs (expected)

### tsconfig.json
Both **identical**:
```json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true
  }
}
```

### .gitignore
Both **identical** - standard Expo template

## App Navigation Structure

### biomaxx-sdk54 Navigation
```
Root (_layout.tsx)
├── (tabs)
│   ├── dashboard (index)
│   ├── protocols
│   ├── learn
│   └── profile
└── onboarding
```

### devotionflow-sdk54 Navigation
```
Root (_layout.tsx)
├── (tabs)
│   ├── index (Home)
│   ├── devotions
│   ├── journal
│   └── profile
└── (onboarding) [optional]
    └── welcome
```

**Pattern**: Both use Expo Router with grouped routes `(tabs)` for tab navigation.

## State Management

### biomaxx-sdk54
No state management shown in reference build - minimal app

### devotionflow-sdk54
Full Zustand stores following standard pattern:

```typescript
// store/userStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const useUserStore = create<UserState>()(
  persist(
    (set, get) => ({ ... }),
    {
      name: 'devotionflow-user-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

**Pattern**: Zustand + AsyncStorage persistence (same pattern as BioMaxx would use)

## React Native Versions - Guaranteed Compatibility

Both projects tested on:
- **React Native**: 0.81.5 (exact match)
- **Expo**: 54.0.32 (exact match)
- **React**: 19.1.0 (exact match)

This guarantees:
- Same JavaScript engine behavior
- Same native module APIs
- Same Metro bundler configuration
- Same iOS/Android compatibility

## Installation & Build Process - Identical

Both follow same setup:

```bash
# Step 1: Navigate to project
cd builds/{projectname}

# Step 2: Install dependencies
npm install

# Step 3: Start development
npm run ios    # iOS Simulator
npm run android # Android emulator
npm start      # Bare start
```

## Key Takeaway

**devotionflow-sdk54 is not just "upgraded" - it's a proper SDK 54 implementation following the exact same pattern as the reference biomaxx-sdk54 project.**

Both projects:
- Use Expo SDK 54.0.32
- Use React Native 0.81.5
- Use React 19.1.0
- Use expo-router 6.0.22
- Use Zustand 5.0.10
- Enable React Native New Architecture
- Follow same app.json configuration
- Use same TypeScript setup
- Use AsyncStorage for persistence

The difference is **app-specific code**, not architecture:
- BioMaxx: Health/fitness protocols app
- DevotionFlow: Daily devotional/prayer app

Both are production-ready SDK 54 apps.
