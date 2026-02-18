# FocusPrayer SDK 54 Upgrade - Checklist

## Pre-Setup Checklist

- [ ] Located in correct directory: `focusprayer-sdk54/`
- [ ] Verified source `focusprayer/` directory exists nearby
- [ ] Have Python 3 installed (`python3 --version`)
- [ ] Have Node.js/npm installed (`npm --version`)
- [ ] Have Xcode installed for iOS testing (`xcode-select --version`)
- [ ] Have time for initial setup (~10-15 minutes)

## Setup Execution Checklist

### Option A: Python Script (Recommended)
- [ ] Run: `python3 complete_setup.py`
- [ ] All directories copied successfully
- [ ] No error messages in output
- [ ] Output shows: "✓ Setup Complete!"

### Option B: Bash Script
- [ ] Run: `bash SETUP.sh`
- [ ] All directories copied successfully
- [ ] Script completed without errors

### Option C: Manual Copy
- [ ] Copied `src/` directory
- [ ] Copied `assets/` directory
- [ ] Copied `__tests__/` directory
- [ ] Copied all app screens to `app/`
- [ ] Copied tab screens to `app/(tabs)/`

## Verification Checklist (After Setup Script)

### Directory Structure
- [ ] `src/stores/` contains userStore.ts, devotionStore.ts
- [ ] `src/services/` contains subscription, blocker, bible services
- [ ] `src/types/` contains index.ts
- [ ] `src/utils/` contains constants.ts, dateUtils.ts
- [ ] `assets/` contains icon.png, splash.png, etc.
- [ ] `__tests__/` directory exists with test files
- [ ] `app/` contains all screen files

### App Screen Files
- [ ] `app/_layout.tsx` - Root layout ✓ (pre-created)
- [ ] `app/index.tsx` - Index/redirect ✓ (pre-created)
- [ ] `app/onboarding.tsx` - Onboarding screen
- [ ] `app/timer.tsx` - Prayer timer screen
- [ ] `app/scripture.tsx` - Scripture reading screen
- [ ] `app/paywall.tsx` - Subscription paywall
- [ ] `app/emergency-unlock.tsx` - Emergency unlock modal
- [ ] `app/privacy-policy.tsx` - Privacy policy screen
- [ ] `app/terms.tsx` - Terms of service screen
- [ ] `app/(tabs)/_layout.tsx` - Tab navigation ✓ (pre-created)
- [ ] `app/(tabs)/index.tsx` - Home tab
- [ ] `app/(tabs)/stats.tsx` - Stats/calendar tab
- [ ] `app/(tabs)/settings.tsx` - Settings tab

### Configuration Files
- [ ] `package.json` - ✓ (pre-created with SDK 54 deps)
- [ ] `app.json` - ✓ (pre-created with newArchEnabled)
- [ ] `tsconfig.json` - ✓ (pre-created)
- [ ] `babel.config.js` - ✓ (pre-created)
- [ ] `.gitignore` - ✓ (pre-created)

## Installation Checklist

### npm install
```bash
npm install
```
- [ ] Command completes without errors
- [ ] `node_modules/` directory created
- [ ] `package-lock.json` generated
- [ ] No peer dependency warnings
- [ ] No vulnerability warnings (or low-severity only)

### Dependency Versions (Verify)
```bash
npm ls expo react react-native expo-router zustand
```
- [ ] `expo@~54.0.32` or compatible
- [ ] `react@19.1.0` or compatible
- [ ] `react-native@0.81.5` or compatible
- [ ] `expo-router@~6.0.22` or compatible
- [ ] `zustand@^5.0.10` or compatible

## Pre-Test Checklist

### Environment Setup
- [ ] iOS Simulator installed and working
- [ ] Android Emulator available (optional)
- [ ] `npx expo` command works
- [ ] Current directory is `focusprayer-sdk54/`

### Start Dev Server
```bash
npx expo start --ios
```
- [ ] Metro bundler starts without errors
- [ ] Shows "To open the app in the browser, press 'w' in the terminal."
- [ ] iOS Simulator launches automatically
- [ ] App starts loading in simulator

## Functionality Testing Checklist

### App Launch
- [ ] App opens without crashing
- [ ] Loading screen displays
- [ ] No red error screens
- [ ] Navigation works

### Onboarding (First Time Only)
- [ ] Welcome screen displays with FocusPrayer branding
- [ ] Can select apps to block
- [ ] Can set prayer duration
- [ ] Can grant blocking permissions
- [ ] Completes successfully

### Home Tab
- [ ] Displays current streak number
- [ ] Shows devotion status
- [ ] "Start Devotion" button visible
- [ ] Trial days display correctly
- [ ] Streak warning shows when at risk

### Timer Screen
- [ ] Opens when starting devotion
- [ ] Countdown timer works
- [ ] Displays prayer prompts
- [ ] Completion triggers correctly
- [ ] Vibration on completion works

### Scripture Screen
- [ ] Daily passage loads
- [ ] Can scroll through text
- [ ] Completion requirements show
- [ ] Shows time spent reading
- [ ] Completes session when requirements met

### Settings Tab
- [ ] Opens without errors
- [ ] Prayer duration adjustment works
- [ ] Toggle switches respond
- [ ] Blocked apps selector works
- [ ] Links to privacy/terms work

### Stats Tab
- [ ] Calendar displays
- [ ] Completed days highlighted
- [ ] Month navigation works
- [ ] Streak metrics display
- [ ] Statistics update correctly

### Paywall Screen
- [ ] Displays subscription options
- [ ] Plan selection works
- [ ] Pricing displays correctly
- [ ] Free trial button available (if applicable)
- [ ] Links to terms/privacy work

### Navigation
- [ ] Tab switching works smoothly
- [ ] No console errors on navigation
- [ ] Back button functions correctly
- [ ] Modal screens dismiss properly

## Build Checklist

### Development Build
- [ ] Development server stays running
- [ ] Hot reload works for code changes
- [ ] Assets load correctly
- [ ] No errors in Xcode console

### Production Build (When Ready)
- [ ] Update `version` in app.json
- [ ] Update `buildNumber` in app.json (iOS)
- [ ] Update `versionCode` in app.json (Android)
- [ ] Clear build cache: `rm -rf .expo/`
- [ ] Test production build locally

## Performance Checklist

### App Performance
- [ ] App launches within 2-3 seconds
- [ ] Transitions between screens smooth
- [ ] No memory leaks (watch Xcode Activity Monitor)
- [ ] No jank during scroll
- [ ] Network requests complete quickly

### Console/Logs
- [ ] No console errors displayed
- [ ] No console warnings
- [ ] Navigation logs clean
- [ ] No async warnings

## Troubleshooting Checklist (If Issues Occur)

### Setup Failed
- [ ] Re-run: `python3 complete_setup.py`
- [ ] Check source directory exists: `ls ../focusprayer/`
- [ ] Verify write permissions in current directory
- [ ] Try manual copy as fallback

### npm install Failed
- [ ] Clear npm cache: `npm cache clean --force`
- [ ] Delete node_modules: `rm -rf node_modules`
- [ ] Delete package-lock.json: `rm package-lock.json`
- [ ] Try again: `npm install`

### App Won't Start
- [ ] Clear Metro cache: `npx expo start --clear`
- [ ] Check for TypeScript errors: `npx tsc --noEmit`
- [ ] Check console for specific error messages
- [ ] Verify all `src/` files were copied

### Module Not Found Errors
- [ ] Verify src/ directory structure matches expected
- [ ] Check path aliases in tsconfig.json
- [ ] Verify imports use correct @/ aliases
- [ ] Clear and reinstall: `rm -rf node_modules && npm install`

## Post-Deployment Checklist (When Ready to Release)

- [ ] All testing checklist items passed
- [ ] No console errors or warnings
- [ ] Performance metrics acceptable
- [ ] Subscription system tested
- [ ] All screens tested on actual devices
- [ ] Privacy policy and terms updated
- [ ] Version number incremented
- [ ] Build artifacts ready
- [ ] TestFlight/Play Store upload configured
- [ ] Release notes prepared

## Documentation Checklist

- [ ] Read `QUICK_START.md` for overview
- [ ] Read `README_SETUP.md` for detailed instructions
- [ ] Read `UPGRADE_SUMMARY.md` for technical details
- [ ] Review changes from SDK 51 to SDK 54
- [ ] Understood new React 19 features
- [ ] Aware of New Architecture implications

## Cleanup Checklist (Optional - After Successful Build)

- [ ] Remove setup scripts (SETUP.sh, complete_setup.py)
- [ ] Remove temporary documentation
- [ ] Commit clean files to git
- [ ] Document any custom changes made
- [ ] Update project README with new SDK info

---

## Summary

### Status Before Setup
- [ ] 45% Complete (configs in place)
- [ ] Ready for file copying

### Status After Setup
- [ ] 100% Complete (all files in place)
- [ ] Ready for testing

### Status After Testing
- [ ] Ready for deployment
- [ ] Ready for TestFlight/Play Store

---

**Last Updated:** 2026-01-22
**Upgrade Status:** Ready
**Next Step:** Run `python3 complete_setup.py`
