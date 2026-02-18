# GlowMaxx SDK 54 Setup Checklist

## Pre-Setup Verification ✅

- [x] Directory created: glowmaxx-sdk54/
- [x] package.json with SDK 54 dependencies
- [x] app.json with proper configuration
- [x] tsconfig.json configured
- [x] .gitignore set up
- [x] All app screens created (9 screens)
- [x] Root layout with splash screen
- [x] Onboarding flow
- [x] Tab navigation setup
- [x] Types and constants defined

## Setup Steps

### Step 1: Run Migration Script
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds/glowmaxx-sdk54
chmod +x COMPLETE_MIGRATION.sh
./COMPLETE_MIGRATION.sh
```

Expected output:
- src/stores/ copied
- src/components/ copied
- src/services/ copied
- src/data/ copied
- Assets copied
- Config files copied
- npm install completes

### Step 2: Verify Installation
```bash
npm list expo
npm list react-native
npm list expo-router
```

Should show:
- expo@54.0.32
- react-native@0.81.5
- expo-router@6.0.22

### Step 3: Start Development Server
```bash
npx expo start --ios
```

Watch for output:
- "Expo Go ready at http://localhost:..."
- No TypeScript errors
- No import errors

### Step 4: Open iOS Simulator
- Press `i` when prompted
- Wait for simulator to launch
- App should load with splash screen

## Functional Testing

### Onboarding Flow
- [ ] Splash screen displays (2 seconds)
- [ ] First onboarding screen shows
- [ ] Can navigate through 4 onboarding steps
- [ ] Skip button works
- [ ] Gender selection screen appears
- [ ] Gender selection works
- [ ] Redirects to home after selecting gender

### Main App
- [ ] Home tab loads with daily progress
- [ ] Water tracker works
- [ ] Mewing timer responds to taps
- [ ] Routines tab shows list
- [ ] Progress tab shows photo interface
- [ ] Learn tab shows guides
- [ ] Settings tab shows all options

### Tab Navigation
- [ ] All 5 tabs appear in tab bar
- [ ] Icons display correctly
- [ ] Labels display correctly
- [ ] Switching tabs doesn't crash
- [ ] Active tab styling works

### Navigation
- [ ] Home → Routines → Home works
- [ ] Tapping routine opens routine-player
- [ ] Back button returns correctly
- [ ] Deep linking works (if configured)

### Settings
- [ ] Can toggle notifications
- [ ] Can change daily goals
- [ ] Changes persist on app restart
- [ ] Can access Privacy Policy
- [ ] Can access Terms of Service

### Permissions
- [ ] Camera permission prompt works
- [ ] Photo library permission prompt works
- [ ] Notification permission prompt works
- [ ] Can deny and re-enable permissions

## Performance Metrics

After startup, check:
- [ ] No console errors (terminal output)
- [ ] No TypeScript warnings
- [ ] App responds quickly to taps
- [ ] Smooth 60fps scrolling
- [ ] Tab switching is instant

## File Structure Verification

After setup, verify:
```
glowmaxx-sdk54/
├── node_modules/              # npm packages installed
├── app/                        # 9 screen files ✓
├── src/
│   ├── stores/                 # 3+ Zustand stores
│   ├── components/             # UI components
│   ├── services/               # RevenueCat, notifications
│   ├── data/                   # Exercises, guides
│   ├── types/
│   │   └── index.ts           # ✓
│   └── utils/
│       ├── constants.ts       # ✓
│       └── dateUtils.ts       # From migration
├── assets/                     # App icons, splash
├── .expo/                      # Expo cache
├── node_modules/              # Installed deps
├── package.json               # ✓
├── app.json                   # ✓
└── tsconfig.json              # ✓
```

## Troubleshooting Quick Fixes

**App crashes on startup:**
- [ ] Run: `npm install` again
- [ ] Clear cache: `npx expo start --clear`
- [ ] Delete node_modules and reinstall

**TypeScript errors:**
- [ ] Check src/stores/ was copied
- [ ] Run: `npx tsc --noEmit`
- [ ] Verify import paths are correct

**Simulator shows blank screen:**
- [ ] Check for errors in terminal
- [ ] Press `r` to reload
- [ ] Press `shift+r` for hard reload

**Permissions not working:**
- [ ] Check iOS permissions in Settings → GlowMaxx
- [ ] Revoke and request again
- [ ] Restart simulator

## Deployment Readiness

When ready for TestFlight/Release, verify:
- [ ] All tests pass
- [ ] No console errors
- [ ] No TypeScript errors
- [ ] Bundle size acceptable
- [ ] Performance targets met
- [ ] All features tested on device

## Sign-Off

When all checks pass:
1. Move glowmaxx-sdk54 to production path
2. Update build references if needed
3. Coordinate with team for TestFlight submission
4. Archive for version control

## Success Indicators

✅ Setup is complete when:
1. App launches without errors
2. Onboarding flow completes
3. All tabs navigate correctly
4. Settings persist
5. No console errors after 2 minutes of use
