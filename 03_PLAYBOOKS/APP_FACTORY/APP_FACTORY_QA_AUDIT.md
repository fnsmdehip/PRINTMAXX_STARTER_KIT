# APP_FACTORY QA Audit Report

**Generated:** 2026-01-25
**Total Apps Audited:** 27 app builds
**Products Directory:** 10 items (PRDs + specs)

---

## Executive Summary

| Status | Count | Percentage |
|--------|-------|------------|
| SHIP-READY (85%+) | 3 | 11% |
| NEAR-COMPLETE (70-84%) | 5 | 19% |
| IN-PROGRESS (40-69%) | 8 | 30% |
| EARLY STAGE (<40%) | 11 | 40% |

**Top Priority for Ship:** biomaxx-sdk54, stepunlock-sdk54, glowmaxx-sdk54

---

## Tier 1: Ship-Ready Apps (85%+ Complete)

### 1. biomaxx-sdk54

| Attribute | Status |
|-----------|--------|
| **Completion** | 90% |
| **Priority** | P0 - SHIP NOW |
| **Niche** | Biohacking/Longevity |

**File Structure:**
- package.json: YES (expo ~54.0.32, react 19.1.0)
- app.json: YES (configured)
- App routing: YES (expo-router with tabs layout)
- Screens: dashboard.tsx, learn.tsx, profile.tsx, onboarding.tsx

**Source Files Present:**
- app/_layout.tsx
- app/index.tsx
- app/onboarding.tsx
- app/(tabs)/_layout.tsx, dashboard.tsx, learn.tsx, profile.tsx
- src/components/ProtocolRing.tsx, ProtocolCard.tsx, AffiliateRecommendation.tsx, StreakBadge.tsx
- src/stores/userStore.ts, protocolStore.ts, subscriptionStore.ts

**Code Quality:**
- TypeScript: Clean, proper typing
- State Management: Zustand stores properly structured
- UI: Professional dashboard with longevity score, protocol rings, tips
- Navigation: Expo Router with proper tab layout

**Monetization:**
- Paywall UI: PRESENT (upgrade CTA, premium content gating)
- RevenueCat package.json: MISSING (needs react-native-purchases)
- Affiliate Component: PRESENT (AffiliateRecommendation.tsx)

**Missing for Ship:**
- [ ] Add react-native-purchases to package.json
- [ ] Configure RevenueCat API key
- [ ] Generate proper app icon (not placeholder)
- [ ] Test in iOS Simulator
- [ ] App Store screenshots

**Next Steps:**
1. `npm install react-native-purchases`
2. Add RevenueCat initialization to _layout.tsx
3. Generate 1024x1024 app icon via Gemini
4. iOS Simulator test
5. App Store Connect submission

---

### 2. stepunlock-sdk54

| Attribute | Status |
|-----------|--------|
| **Completion** | 85% |
| **Priority** | P0 - SHIP NOW |
| **Niche** | Fitness/Step Goals |

**File Structure:**
- package.json: YES (expo ~54.0.32, react-native-purchases ^9.7.1)
- app.json: YES
- Navigation: Expo Router with tabs

**Source Files Present:**
- app/_layout.tsx, index.tsx, onboarding.tsx, paywall.tsx, emergency-unlock.tsx, privacy-policy.tsx, terms.tsx
- app/(tabs)/_layout.tsx, index.tsx, progress.tsx, settings.tsx
- src/screens/HomeScreen.tsx, OnboardingScreen.tsx, ProgressScreen.tsx, PaywallScreen.tsx, SettingsScreen.tsx, EmergencyUnlockScreen.tsx
- src/components/ProgressRing.tsx, GoalSelector.tsx, AppSelector.tsx, StreakBadge.tsx, CalendarView.tsx, Button.tsx

**Code Quality:**
- TypeScript: Clean
- RevenueCat: FULLY INTEGRATED (react-native-purchases in deps, PaywallScreen with getOfferings, purchaseSubscription, restorePurchases)
- State: Zustand
- UI: Professional paywall with plan selection, features list

**Monetization:**
- RevenueCat: YES (package.json + service implementation)
- Paywall: YES (monthly/annual plans with "Best value" badge)
- Legal: YES (Terms, Privacy Policy screens)

**Missing for Ship:**
- [ ] Generate proper app icon
- [ ] Test RevenueCat purchase flow
- [ ] iOS Simulator test
- [ ] App Store screenshots
- [ ] Configure RevenueCat project ID

**Next Steps:**
1. Generate 1024x1024 app icon
2. Test in iOS Simulator
3. Configure RevenueCat dashboard
4. Submit to App Store

---

### 3. glowmaxx-sdk54

| Attribute | Status |
|-----------|--------|
| **Completion** | 85% |
| **Priority** | P1 |
| **Niche** | Women's Skincare/Beauty |

**File Structure:**
- package.json: YES (expo ~54.0.32, react-native-purchases ^9.7.1, expo-camera, expo-image-picker)
- app.json: YES
- Navigation: Expo Router tabs

**Source Files Present:**
- app/_layout.tsx, index.tsx, onboarding.tsx, paywall.tsx
- app/(tabs)/_layout.tsx, routines.tsx, progress.tsx, learn.tsx

**Code Quality:**
- TypeScript: Clean
- RevenueCat: IN DEPS (react-native-purchases)
- Camera integration: Ready (expo-camera, expo-image-picker)

**Monetization:**
- RevenueCat: YES (in dependencies)
- Paywall screen: YES

**Missing for Ship:**
- [ ] App icon
- [ ] Full paywall service implementation
- [ ] iOS Simulator test

---

## Tier 2: Near-Complete Apps (70-84%)

### 4. learnlock-sdk54

| Attribute | Status |
|-----------|--------|
| **Completion** | 75% |
| **Priority** | P1 |
| **Niche** | Students/Focus |

**File Structure:**
- package.json: YES (expo ~54.0.32, slider, gesture handler)
- app.json: YES
- Navigation: Expo Router

**Source Files Present:**
- src/components/timer/, stats/, blocker/, common/, paywall/
- src/screens/HomeScreen.tsx, StatsScreen.tsx, OnboardingScreen.tsx, PrivacyPolicyScreen.tsx, TermsScreen.tsx
- app/(tabs)/index.tsx, stats.tsx, settings.tsx
- app/onboarding.tsx, paywall.tsx, privacy.tsx, terms.tsx

**Monetization:**
- Paywall Component: YES (src/components/paywall/PaywallScreen.tsx)
- RevenueCat: MISSING from package.json

**Missing for Ship:**
- [ ] Add react-native-purchases
- [ ] App icon
- [ ] RevenueCat integration
- [ ] iOS Simulator test

---

### 5. prayerlock (Legacy)

| Attribute | Status |
|-----------|--------|
| **Completion** | 80% |
| **Priority** | P1 |
| **Niche** | Faith/Prayer |

**File Structure:**
- package.json: YES (expo ~52.0.23, older SDK)
- app.json: YES
- Navigation: React Navigation stack

**Source Files Present:**
- src/screens/PaywallScreen.tsx (full implementation with LinearGradient, plan selection)
- src/components/Button.tsx
- src/constants/Colors.ts
- src/utils/storage.ts (setPremiumStatus)

**Code Quality:**
- Paywall: COMPLETE (7-day trial, monthly/yearly plans, feature comparison)
- UI: Professional with gradient header, plan cards, feature list
- Legal: Complete (Terms, Privacy links)

**Monetization:**
- Paywall UI: COMPLETE
- RevenueCat: STUB only (simulates purchase for demo)
- NOTE: Uses setPremiumStatus for local storage, needs real RevenueCat

**Missing for Ship:**
- [ ] Upgrade to SDK 54
- [ ] Add real RevenueCat integration
- [ ] App icon
- [ ] Convert to Expo Router (optional)

---

### 6. studylock (Legacy)

| Attribute | Status |
|-----------|--------|
| **Completion** | 70% |
| **Priority** | P2 |
| **Niche** | Students/Focus |

**File Structure:**
- package.json: YES
- app.json: YES
- Navigation: Expo Router

**Source Files:**
- app/paywall.tsx (re-exports from src/screens/PaywallScreen)
- Minimal screen structure

**Missing for Ship:**
- [ ] Upgrade to SDK 54
- [ ] Complete screen implementations
- [ ] RevenueCat integration
- [ ] App icon

---

### 7. walktounlock (Legacy)

| Attribute | Status |
|-----------|--------|
| **Completion** | 70% |
| **Priority** | P2 |
| **Niche** | Fitness/Steps |

**File Structure:**
- package.json: YES
- app.json: YES
- App.tsx: YES (basic structure)

**Missing for Ship:**
- [ ] Upgrade to SDK 54
- [ ] Complete health integration
- [ ] RevenueCat
- [ ] App icon

---

### 8. prayerlock-sdk54

| Attribute | Status |
|-----------|--------|
| **Completion** | 70% |
| **Priority** | P1 |
| **Niche** | Faith/Prayer |

**File Structure:**
- package.json: YES (expo ~54.0.32, expo-notifications)
- Limited source files visible

**Missing for Ship:**
- [ ] Complete screen implementations from legacy prayerlock
- [ ] RevenueCat integration
- [ ] App icon

---

## Tier 3: In-Progress Apps (40-69%)

### 9. devotionflow-sdk54 (50%)

- Has: package.json, basic app structure, tab navigation
- Missing: Full screen implementations, RevenueCat, icon

### 10. focusprayer-sdk54 (50%)

- Has: package.json, basic routing
- Missing: Full screens, monetization, icon

### 11. promptvault-sdk54 (50%)

- Has: package.json, basic structure
- Missing: AI integration, monetization, icon

### 12. dailyanchor-sdk54 (45%)

- Has: package.json, basic structure
- Missing: Full implementation

### 13. pelvicpro-sdk54 (45%)

- Has: package.json, basic structure
- Niche: Women's Health
- Missing: Full implementation, icon

### 14-16. biomaxx, glowmaxx, devotionflow (Legacy) (40-50%)

- Older SDK versions
- Consider deprecating in favor of -sdk54 versions

---

## Tier 4: Early Stage Apps (<40%)

### 17-27. Various Legacy Builds

Apps that are early stage or should be deprecated:
- learnlock (use learnlock-sdk54)
- focusprayer (use focusprayer-sdk54)
- promptvault (use promptvault-sdk54)
- dailyanchor (use dailyanchor-sdk54)
- pelvicpro (use pelvicpro-sdk54)
- stepunlock (use stepunlock-sdk54)

---

## Products Directory (PRDs and Specs)

Location: `/MONEY_METHODS/APP_FACTORY/products/`

| Item | Type |
|------|------|
| PRAYERLOCK_PRD.md | Product Requirements |
| STUDYLOCK_PRD.md | Product Requirements |
| WALKTOUNLOCK_PRD.md | Product Requirements |
| dailyanchor/ | Product folder |
| dailydevotion/ | Product folder |
| femfit/ | Product folder |
| prayerlock/ | Product folder |
| promptvault/ | Product folder |
| studylock/ | Product folder |
| walktounlock/ | Product folder |

---

## RevenueCat Integration Status

| App | Has Dependency | Has Service Code | Status |
|-----|----------------|------------------|--------|
| stepunlock-sdk54 | YES | YES | READY |
| glowmaxx-sdk54 | YES | PARTIAL | NEEDS SERVICE |
| biomaxx-sdk54 | NO | NO | ADD DEP |
| learnlock-sdk54 | NO | HAS PAYWALL UI | ADD DEP |
| prayerlock | NO | STUB ONLY | ADD DEP |
| prayerlock-sdk54 | NO | NO | ADD DEP |
| Others | NO | NO | ADD DEP |

---

## Common Missing Items Across All Apps

### Critical (Blocking Ship)

1. **App Icons** - No apps have proper 1024x1024 icons generated
2. **RevenueCat API Keys** - Not configured in any app
3. **iOS Simulator Testing** - No evidence of recent testing

### Important (Should Fix)

1. **Consistent RevenueCat Integration** - Only stepunlock-sdk54 has full integration
2. **Privacy Policy URLs** - Need real URLs, not placeholders
3. **Terms of Service URLs** - Need real URLs
4. **App Store Screenshots** - None generated

### Nice to Have

1. **Splash screens** - Most use default Expo splash
2. **App Store descriptions** - Not drafted
3. **Keywords/ASO** - Not researched

---

## Recommended Ship Order

### Week 1: Ship These
1. **biomaxx-sdk54** - Just needs RevenueCat dep + icon
2. **stepunlock-sdk54** - Already has RevenueCat, needs icon + testing

### Week 2: Ship These
3. **glowmaxx-sdk54** - Needs service implementation + icon
4. **learnlock-sdk54** - Needs RevenueCat + icon

### Week 3: Ship These
5. **prayerlock-sdk54** - Needs completion from legacy
6. **devotionflow-sdk54** - Complete implementation

---

## Action Items Summary

### Immediate (Today)

| Task | App | Est. Time |
|------|-----|-----------|
| Add react-native-purchases | biomaxx-sdk54 | 5 min |
| Generate app icon | biomaxx-sdk54 | 15 min |
| iOS Simulator test | biomaxx-sdk54 | 30 min |
| Generate app icon | stepunlock-sdk54 | 15 min |
| iOS Simulator test | stepunlock-sdk54 | 30 min |

### This Week

| Task | Apps | Est. Time |
|------|------|-----------|
| RevenueCat dashboard setup | All | 2 hours |
| Generate all app icons | 6 priority apps | 1.5 hours |
| Complete RevenueCat services | glowmaxx, learnlock | 2 hours |
| App Store Connect setup | First 2 apps | 1 hour |

### Deprecation Candidates

The following legacy builds should be archived in favor of SDK54 versions:
- biomaxx (use biomaxx-sdk54)
- glowmaxx (use glowmaxx-sdk54)
- learnlock (use learnlock-sdk54)
- stepunlock (use stepunlock-sdk54)
- focusprayer (use focusprayer-sdk54)
- devotionflow (use devotionflow-sdk54)
- promptvault (use promptvault-sdk54)
- dailyanchor (use dailyanchor-sdk54)
- pelvicpro (use pelvicpro-sdk54)

---

## Technical Notes

### SDK Versions

| SDK | React Native | React | Status |
|-----|--------------|-------|--------|
| Expo 54 | 0.81.5 | 19.1.0 | CURRENT |
| Expo 52 | 0.76.x | 18.x | LEGACY |

### Dependencies to Add for All Apps

```json
{
  "react-native-purchases": "^9.7.1",
  "expo-haptics": "~15.0.8",
  "expo-notifications": "~0.32.16"
}
```

### RevenueCat Service Template

Location: `/stepunlock-sdk54/src/services/subscriptionService.ts`

This can be copied to other apps as the standard RevenueCat integration template.

---

## Conclusion

The APP_FACTORY has 27 app builds with 3 apps (biomaxx-sdk54, stepunlock-sdk54, glowmaxx-sdk54) at 85%+ completion and ready to ship within days. The main blockers are:

1. App icons (can be generated with Gemini in 15 min each)
2. RevenueCat dependency addition (5 min each)
3. iOS Simulator testing (30 min each)

**Estimated time to ship first 2 apps: 4 hours total work.**

Priority should be given to SDK54 versions. Legacy builds should be deprecated to reduce maintenance burden.
