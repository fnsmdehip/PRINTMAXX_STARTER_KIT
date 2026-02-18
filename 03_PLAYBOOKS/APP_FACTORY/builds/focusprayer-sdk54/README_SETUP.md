# FocusPrayer SDK 54 Upgrade

This directory contains FocusPrayer upgraded to Expo SDK 54 with React Native 0.81.5 and React 19.1.0.

## What's Been Created

### Core Config Files
- ✓ `package.json` - SDK 54 dependencies configured
- ✓ `app.json` - Updated with `newArchEnabled: true` and latest config
- ✓ `tsconfig.json` - TypeScript configuration for Expo SDK 54
- ✓ `babel.config.js` - Babel preset configured
- ✓ `.gitignore` - Standard Expo ignore patterns

### Partial App Structure
- ✓ `app/_layout.tsx` - Root layout with app initialization
- ✓ `app/index.tsx` - Redirect logic
- ✓ `app/(tabs)/_layout.tsx` - Tab navigation
- ✓ `app/(tabs)/index.tsx` - Home screen (started)

### Still Needed
The remaining app screens need to be copied from the original focusprayer:
- `app/onboarding.tsx`
- `app/timer.tsx`
- `app/scripture.tsx`
- `app/paywall.tsx`
- `app/emergency-unlock.tsx`
- `app/privacy-policy.tsx`
- `app/terms.tsx`
- `app/(tabs)/stats.tsx`
- `app/(tabs)/settings.tsx`

The `src/` directory (stores, services, types, utils) - entire folder needs to be copied
The `assets/` directory - all images/icons
The `__tests__/` directory - all test files

## Quick Setup

### Option 1: Use the SETUP.sh Script
```bash
cd focusprayer-sdk54
bash SETUP.sh
```

This will copy all remaining directories from the original focusprayer app.

### Option 2: Manual Copy
```bash
cd focusprayer-sdk54

# Copy remaining app screens from original
cp -r ../focusprayer/app/onboarding.tsx ./app/
cp -r ../focusprayer/app/timer.tsx ./app/
cp -r ../focusprayer/app/scripture.tsx ./app/
cp -r ../focusprayer/app/paywall.tsx ./app/
cp -r ../focusprayer/app/emergency-unlock.tsx ./app/
cp -r ../focusprayer/app/privacy-policy.tsx ./app/
cp -r ../focusprayer/app/terms.tsx ./app/
cp -r ../focusprayer/app/\(tabs\)/stats.tsx ./app/\(tabs\)/
cp -r ../focusprayer/app/\(tabs\)/settings.tsx ./app/\(tabs\)/

# Copy src, assets, and tests
cp -r ../focusprayer/src ./
cp -r ../focusprayer/assets ./
cp -r ../focusprayer/__tests__ ./
```

### Option 3: Python Script
```bash
python3 << 'EOF'
import shutil
import os

src = "../focusprayer"
dest = "."

# Copy remaining directories
shutil.copytree(f"{src}/src", f"{dest}/src", dirs_exist_ok=True)
shutil.copytree(f"{src}/assets", f"{dest}/assets", dirs_exist_ok=True)
shutil.copytree(f"{src}/__tests__", f"{dest}/__tests__", dirs_exist_ok=True)

# Copy remaining app files
import glob
for file in glob.glob(f"{src}/app/**/*.tsx", recursive=True):
    rel = file.replace(f"{src}/", "")
    os.makedirs(os.path.dirname(f"{dest}/{rel}"), exist_ok=True)
    shutil.copy(file, f"{dest}/{rel}")

print("✓ All files copied")
EOF
```

## Installation & Running

### 1. Install Dependencies
```bash
npm install
```

### 2. Start Development Server
```bash
npm start
```

### 3. Run on iOS Simulator
```bash
npx expo start --ios
```

### 4. Run on Android Emulator
```bash
npx expo start --android
```

## Key Changes from Original (Expo SDK 51 → SDK 54)

### Package.json Updates
```diff
- "expo": "~51.0.28"
- "react": "18.2.0"
- "react-native": "0.74.0"

+ "expo": "~54.0.32"
+ "react": "19.1.0"
+ "react-native": "0.81.5"
```

### New Architecture Enabled
```json
{
  "expo": {
    "newArchEnabled": true,
    ...
  }
}
```

### Dependency Versions
All related dependencies upgraded to SDK 54 compatible versions:
- `@expo/vector-icons`: 14.0.0 → 15.0.3
- `expo-router`: 3.5.23 → 6.0.22
- `expo-haptics`: Added ~15.0.8
- `zustand`: 4.5.4 → 5.0.10

### Breaking Changes Handled
- React 19 compatible (removed React.FC in favor of inline typed functions)
- New Architecture enabled for better performance
- Updated expo-router v6 API compatibility

## Testing Checklist

After copying all files and installing, test:

- [ ] `npm install` completes successfully
- [ ] `npm start` launches without errors
- [ ] iOS Simulator opens and app loads
- [ ] Onboarding flow works
- [ ] Home screen renders without errors
- [ ] Timer screen countdown works
- [ ] Scripture screen loads daily passage
- [ ] Settings screen toggles work
- [ ] Paywall displays correctly
- [ ] Streak calculations display properly

## Common Issues

### "Cannot find module '@/stores/userStore'"
Make sure you've copied the `src/` directory with all stores, services, and utilities.

### "Module not found: assets"
Copy the `assets/` directory with all images and app icons.

### TypeScript errors
Run `tsc --noEmit` to check for type issues. Make sure `tsconfig.json` is properly configured.

## Next Steps

1. Complete the file copying (use SETUP.sh or manual copy)
2. Run `npm install`
3. Test in iOS Simulator with `npx expo start --ios`
4. If any compilation errors occur, check imports in the src/ files
5. Update navigation references if needed
6. Test all app flows before deployment

## Architecture

- **Expo SDK 54** - Latest Expo version
- **React Native 0.81.5** - Latest React Native with New Architecture support
- **React 19.1.0** - Latest React version
- **expo-router 6.0.22** - File-based routing
- **Zustand 5.0.10** - Lightweight state management
- **TypeScript** - Type safety throughout

## Notes

- The new App.json includes `newArchEnabled: true` for better performance
- Android has `edgeToEdgeEnabled: true` for immersive experience
- All Expo libraries are compatible with SDK 54
- RevenueCat integration preserved from original
- RevenueCat version may need updating - check for SDK 54 compatibility

## Reference

- Original app: `../focusprayer/`
- Reference SDK 54 build: `../biomaxx-sdk54/`

For more info on Expo SDK 54 changes, see: https://docs.expo.dev/
