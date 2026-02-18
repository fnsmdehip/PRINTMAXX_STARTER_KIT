# PRD: SDK 54 App Fixes

## Introduction

Fix critical issues in SDK 54 apps identified by QA testing. Several apps have npm install failures, missing modules, and TypeScript errors that prevent them from running.

## Alpha Stack Reference

**SDK 54 Stack (per QA reports):**
- Expo 54.0.32
- React 19.1.0
- React Native 0.81.5
- Zustand 5.0.10
- expo-router 6.0.22
- newArchEnabled: true

**QA Report:** `MONEY_METHODS/APP_FACTORY/builds/SDK54_QA_REPORT.md`

**Working Examples:**
- `prayerlock-sdk54` - Clean, passes all checks
- `stepunlock-sdk54` - Clean, passes all checks

**Reference Files:**
- `.claude/CLAUDE.md` → APP_FACTORY Full Stack section
- `MONEY_METHODS/APP_FACTORY/APP_LAUNCH_FULL_STACK.md`

## Goals

- Fix npm install failures for glowmaxx, promptvault
- Fix missing module errors for devotionflow, focusprayer, learnlock
- Fix TypeScript errors in biomaxx, pelvicpro
- All apps pass `npx tsc --noEmit`
- All apps can run in iOS Simulator

## Critical Issues by App

### glowmaxx-sdk54
- **Issue:** npm install fails - expo-image-picker@~16.0.11 doesn't exist
- **Fix:** Update to expo-image-picker@~16.0.6 (latest compatible)

### promptvault-sdk54
- **Issue:** npm install fails - expo-clipboard@~8.0.13 doesn't exist
- **Fix:** Update to expo-clipboard@~7.0.1 (latest SDK 54 compatible)

### devotionflow-sdk54
- **Issue:** 20+ missing module errors (stores, constants, packages)
- **Fix:** Create missing store files, install missing packages

### focusprayer-sdk54
- **Issue:** 12 missing module errors (stores, services, utils)
- **Fix:** Create missing files based on prayerlock-sdk54 pattern

### learnlock-sdk54
- **Issue:** 30+ errors (esModuleInterop, missing packages, type issues)
- **Fix:** Update tsconfig.json, install packages, fix types

### biomaxx-sdk54
- **Issue:** 2 TypeScript errors (implicit any), missing iOS bundleIdentifier
- **Fix:** Add types, add bundleIdentifier to app.json

### pelvicpro-sdk54
- **Issue:** 3 TypeScript errors (Timeout type, implicit any)
- **Fix:** Import Timeout type from react-native, add explicit types

## User Stories

### US-001: Fix GlowMaxx npm install
**Description:** As a developer, I need GlowMaxx to install dependencies.

**Acceptance Criteria:**
- [ ] Update package.json expo-image-picker to ~16.0.6
- [ ] Run npm install successfully
- [ ] No dependency resolution errors
- [ ] Typecheck passes

### US-002: Fix PromptVault npm install
**Description:** As a developer, I need PromptVault to install dependencies.

**Acceptance Criteria:**
- [ ] Update package.json expo-clipboard to ~7.0.1
- [ ] Run npm install successfully
- [ ] No dependency resolution errors
- [ ] Typecheck passes

### US-003: Fix BioMaxx TypeScript and config
**Description:** As a developer, I need BioMaxx to pass TypeScript checks.

**Acceptance Criteria:**
- [ ] Fix implicit any errors with explicit types
- [ ] Add bundleIdentifier to app.json ios section
- [ ] Typecheck passes: `npx tsc --noEmit`

### US-004: Fix PelvicPro TypeScript errors
**Description:** As a developer, I need PelvicPro to pass TypeScript checks.

**Acceptance Criteria:**
- [ ] Import Timeout type from react-native where needed
- [ ] Fix implicit any errors
- [ ] Typecheck passes: `npx tsc --noEmit`

### US-005: Create DevotionFlow missing modules
**Description:** As a developer, I need DevotionFlow's missing stores and utilities.

**Acceptance Criteria:**
- [ ] Create missing store files based on similar app patterns
- [ ] Install any missing npm packages
- [ ] All imports resolve correctly
- [ ] Typecheck passes

### US-006: Create FocusPrayer missing modules
**Description:** As a developer, I need FocusPrayer's missing stores and services.

**Acceptance Criteria:**
- [ ] Create missing files (copy pattern from prayerlock-sdk54)
- [ ] Update imports to match file structure
- [ ] Typecheck passes

### US-007: Fix LearnLock comprehensive errors
**Description:** As a developer, I need LearnLock to build without errors.

**Acceptance Criteria:**
- [ ] Update tsconfig.json with esModuleInterop: true
- [ ] Install missing packages
- [ ] Fix type errors
- [ ] Typecheck passes

### US-008: Verify all apps in iOS Simulator
**Description:** As a QA tester, I need to confirm all fixed apps run.

**Acceptance Criteria:**
- [ ] Each fixed app launches with `npx expo start --ios`
- [ ] App displays main screen without crash
- [ ] No red screen errors
- [ ] Basic navigation works

## Technical Considerations

**Pattern Reference (Working Apps):**
- Use `prayerlock-sdk54` as reference for faith app structure
- Use `stepunlock-sdk54` as reference for fitness app structure

**Package Version Lookup:**
```bash
npm view expo-image-picker versions --json | jq '.[-10:]'
npm view expo-clipboard versions --json | jq '.[-10:]'
```

**TypeScript Config Standard:**
```json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true
  }
}
```

## Non-Goals

- No new features (just fixes)
- No UI redesigns
- No package major version upgrades beyond what's needed

## Success Metrics

- All 10 SDK 54 apps pass `npm install`
- All 10 SDK 54 apps pass `npx tsc --noEmit`
- All 10 SDK 54 apps launch in iOS Simulator
- QA report shows 10/10 apps ready
