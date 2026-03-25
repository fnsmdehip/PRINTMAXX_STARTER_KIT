# App Store Submission Checklist

Run EVERY item before declaring ANY iOS app "done." No exceptions. No "we'll fix it later."

## Payment Integration (Apple Guideline 3.1.1)
- [ ] `react-native-purchases` installed and importable (not mocked)
- [ ] `Purchases.configure({ apiKey })` called on app launch with REAL key from env
- [ ] `Purchases.getOfferings()` called before showing paywall
- [ ] `Purchases.purchasePackage(pkg)` called when user taps Subscribe (not setTimeout)
- [ ] `Purchases.restorePurchases()` wired to Restore button
- [ ] `Purchases.getCustomerInfo()` checked on app launch for returning subscribers
- [ ] Entitlement name matches RevenueCat dashboard ("premium")
- [ ] Pricing matches RevenueCat product configuration
- [ ] Annual plan pre-selected with savings badge (Cal AI pattern)
- [ ] Subscription auto-renewal terms displayed near Subscribe button
- [ ] "Subscriptions may be managed and auto-renewal turned off in Account Settings"

## Content Gating (Apple Guideline 2.3 — Accurate Metadata)
- [ ] Free users ACTUALLY blocked from premium features in CODE (not just UI)
- [ ] Premium check happens at the action level (download, scan, export) not just screen level
- [ ] User cannot bypass paywall by dismissing/back-navigating
- [ ] Free tier has genuine utility (not just a paywall wrapper)
- [ ] Premium features clearly differentiated in paywall

## Privacy & Permissions
- [ ] `ITSAppUsesNonExemptEncryption: false` in app.json infoPlist
- [ ] Privacy policy URL set and resolves to real page
- [ ] Terms of service URL set and resolves
- [ ] Camera permission string is specific ("NutriSnap uses your camera to photograph meals and estimate nutritional content including calories, protein, carbs, and fat")
- [ ] Face ID string is specific if used
- [ ] Notification string is specific if used
- [ ] `NSUserTrackingUsageDescription` set if using ads/analytics
- [ ] No unnecessary permissions requested

## App Identity
- [ ] App name doesn't clash with existing popular apps (search App Store)
- [ ] Bundle ID format: `com.printmaxx.[appname]`
- [ ] App Store subtitle set (30 char max)
- [ ] Primary + secondary categories set
- [ ] App review notes explaining subscription model

## Content Quality
- [ ] Zero placeholder text ("Lorem ipsum", "TODO", "Coming soon")
- [ ] Zero console.log/warn/error in production code
- [ ] Zero emoji used as icons (use Ionicons or SF Symbols)
- [ ] All screens have loading states (skeleton, not spinner)
- [ ] All screens have empty states with CTAs
- [ ] All touch targets minimum 44x44pt
- [ ] Hero numbers use thin weight (200) with tabular-nums
- [ ] Cards have subtle borders (1px rgba border + shadow)

## Build Verification
- [ ] `npx expo export --platform ios` passes with zero errors
- [ ] No TypeScript errors (`npx tsc --noEmit`)
- [ ] App launches in simulator without crash
- [ ] All 4+ tabs render correctly
- [ ] Onboarding flow completes start to finish
- [ ] Paywall renders with real pricing
- [ ] Can navigate every screen without crash

## Common Rejection Reasons to Verify Against
- [ ] 2.1 — App completeness: no crashes, no broken features
- [ ] 2.3 — Accurate metadata: descriptions match actual functionality
- [ ] 3.1.1 — IAP required: subscriptions use Apple IAP (RevenueCat wraps this)
- [ ] 3.1.2 — Subscriptions: auto-renewal terms displayed, manage button available
- [ ] 4.0 — Design: follows HIG basics, no web wrappers disguised as native
- [ ] 5.1.1 — Data collection: privacy policy covers what you collect
- [ ] 5.1.2 — Data use: only collect what's needed
- [ ] 5.2.1 — Legal: no claims app can't substantiate (medical, legal, financial advice)
