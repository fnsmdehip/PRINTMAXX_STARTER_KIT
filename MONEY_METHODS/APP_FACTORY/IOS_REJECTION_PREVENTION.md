# iOS App Store rejection prevention guide

**Last updated:** 2026-02-10
**Stack:** PWA + Capacitor.js + RevenueCat + Stripe (web fallback)
**Rejection rate context:** Apple rejects ~25% of all submissions (~1.93M apps in 2024). You will get rejected. This doc makes sure you only get rejected once.

---

## The numbers you need to know

- 25% of all app submissions get rejected
- 40%+ of unresolved rejections are Guideline 2.1 (App Completeness)
- 15% of rejections are privacy violations (and growing)
- Average review time: 24-48 hours
- Resubmission review: usually faster if you respond quickly and actually fix the issue
- Apple now uses AI-assisted reviews alongside human reviewers

---

## 1. Guideline 4.2 - Minimum functionality (THE #1 KILLER FOR PWA APPS)

**Apple guideline number:** 4.2, 4.2.2

**What triggers it:**
- App is just a website wrapped in a WebView
- App doesn't do anything a mobile browser can't do
- No native device features used (no haptics, no notifications, no camera, no local storage beyond cookies)
- App could be replaced by a bookmark to a website
- Apple calls these "web clippings" and explicitly bans them under 4.2.2

**How to prevent it (Capacitor.js specific):**

You need to use at minimum 3 native Capacitor plugins that a website cannot replicate:

1. **Haptics** (`@capacitor/haptics`) - Add tactile feedback on key actions (button presses, completions, errors). This is the easiest win.
2. **Push Notifications** (`@capacitor/push-notifications`) - Even if you only send weekly reminders. Native push = not a website.
3. **Local Notifications** (`@capacitor/local-notifications`) - Scheduled reminders, streak notifications, daily check-ins.
4. **Status Bar** (`@capacitor/status-bar`) - Control the native status bar color/style. Small but signals native.
5. **App** (`@capacitor/app`) - Handle app state changes, deep links, back button behavior.
6. **Preferences** (`@capacitor/preferences`) - Native key-value storage (not just localStorage).
7. **Share** (`@capacitor/share`) - Native share sheet integration.

**The minimum bar (Feb 2026):**

Apple doesn't care about your framework. They care about user experience. Your app must:
- Look and feel like a native iOS app (not a website on a phone)
- Use iOS-standard navigation patterns (tab bar, navigation stack, swipe gestures)
- Use at least 2-3 native device capabilities
- Have offline functionality (PWAs already have this, but make it obvious)
- Load instantly (no white screen, no web-style loading spinners)

**What passed in 2021 won't pass in 2026.** The bar is higher now.

**Checklist:**
- [ ] 3+ Capacitor native plugins integrated and functional
- [ ] No visible WebView artifacts (no pull-to-refresh bounce unless intentional, no URL bar, no web-style scrolling)
- [ ] Native iOS navigation patterns (no hamburger menus as primary nav)
- [ ] Haptic feedback on at least 5 key interactions
- [ ] Push or local notifications configured
- [ ] Offline mode works (service worker caching)
- [ ] App loads in under 1 second (no white flash)
- [ ] No hover states (hover doesn't exist on mobile)

---

## 2. Guideline 2.1 - App completeness (40% of all rejections)

**Apple guideline number:** 2.1

**What triggers it:**
- App crashes on launch or during review
- Placeholder content ("Lorem ipsum", "Coming soon", empty screens)
- Broken links or buttons that do nothing
- Missing features promised in description
- Login required but no demo account provided
- Backend server is down during review

**How to prevent it:**
- Test on a REAL device, not just simulator. Simulators miss memory issues, orientation bugs, and performance problems.
- Remove ALL placeholder content. Every screen must be production-ready.
- Every button must do something. If a feature isn't ready, remove the button entirely.
- If your app has login, provide demo credentials in the App Review Notes field.
- Keep your backend server running 24/7 during review period. Apple reviews at unpredictable hours.

**Checklist:**
- [ ] Tested on physical iPhone (not just simulator)
- [ ] Zero crashes in 30 minutes of usage
- [ ] No placeholder text or images anywhere
- [ ] Every button and link is functional
- [ ] Demo account credentials in Review Notes (if app has login)
- [ ] Backend/API servers confirmed running
- [ ] App works on current iOS version AND one version back
- [ ] No console errors in production build

---

## 3. Guideline 5.1.1 - Privacy policy and data collection

**Apple guideline number:** 5.1.1, 5.1.2

**What triggers it:**
- No privacy policy URL provided
- Privacy policy URL is dead (404)
- Privacy policy doesn't match what the app actually does
- Privacy Nutrition Label in App Store Connect doesn't match actual data collection
- Requesting permissions without clear explanation
- Generic permission strings ("App would like to access your camera" without explaining why)

**How to prevent it:**

Your privacy policy MUST include:
1. What data you collect (be specific, not "we may collect")
2. How you collect it (SDK, user input, automatic)
3. What you use it for (each data type mapped to purpose)
4. Third parties who receive data (analytics, ad networks, RevenueCat)
5. Data retention and deletion policy
6. How users can request data deletion
7. How users can revoke consent
8. Contact information for privacy questions

**For Capacitor.js PWA apps that store data locally:**
- Still need a privacy policy even if you collect nothing
- State clearly: "All data is stored locally on your device"
- If using RevenueCat: disclose that purchase data goes through RevenueCat
- If using any analytics (even privacy-focused ones like Plausible): disclose it

**Permission strings must be specific:**
- BAD: "This app needs camera access"
- GOOD: "PrayerLock uses your camera to scan QR codes for group prayer sessions"

**Checklist:**
- [ ] Privacy policy URL is live and accessible (test the URL)
- [ ] Privacy policy covers all 8 items listed above
- [ ] App Store Connect Privacy Nutrition Label matches actual behavior
- [ ] All permission request strings explain specific usage
- [ ] Terms of Service URL is live
- [ ] Privacy policy mentions all third-party SDKs (RevenueCat, analytics, etc.)

---

## 4. Guideline 3.1.1 - In-app purchase / subscriptions

**Apple guideline number:** 3.1.1, 3.1.2

**What triggers it:**
- Selling digital content or features outside Apple IAP
- No "Restore Purchases" button
- Subscription terms not clearly disclosed before purchase
- Auto-renewal not disclosed in app description
- Missing subscription management link
- Paywall appears before user sees any value

**Current rules (Feb 2026):**

The Epic v. Apple ruling (April 2025) changed things for the US App Store:
- You CAN include one external payment link in US apps
- You still MUST also offer Apple IAP alongside external payment
- The Dec 2025 appeals court ruled Apple can charge a "reasonable commission" on external link purchases
- For non-US storefronts: Apple IAP is still mandatory for all digital goods

**How to prevent rejection:**

1. Always offer Apple IAP as a payment option (even if you also have Stripe web checkout)
2. "Restore Purchases" button must be visible in Settings
3. Subscription auto-renewal terms must appear:
   - In the App Store description
   - On the paywall screen before purchase
   - In the app Settings
4. Include clear cancel instructions
5. Link to Apple's subscription management page from Settings
6. Don't gate the entire app behind a paywall on first launch. Let users see value first.

**RevenueCat + Capacitor.js setup:**
- Use `@revenuecat/purchases-capacitor` for IAP
- Use `@revenuecat/purchases-capacitor-ui` for paywalls
- Configure products in both App Store Connect AND RevenueCat dashboard
- Test with sandbox accounts before submission
- Verify restore purchases works on a clean install

**Checklist:**
- [ ] Apple IAP configured in App Store Connect
- [ ] RevenueCat SDK integrated and tested
- [ ] "Restore Purchases" button visible and functional
- [ ] Subscription terms disclosed on paywall screen
- [ ] Auto-renewal disclosure in App Store description
- [ ] Cancel instructions in app
- [ ] Subscription management link in Settings
- [ ] Users can access core app before hitting paywall
- [ ] Sandbox purchase tested end-to-end
- [ ] Restore purchases tested on fresh install

---

## 5. Guideline 2.3 - Accurate metadata

**Apple guideline number:** 2.3, 2.3.3, 2.3.7

**What triggers it:**
- Screenshots don't match actual app UI
- Screenshots show only splash screen or login page
- Description promises features that don't exist
- Keywords stuffed with competitor names or irrelevant terms
- App name contains price information
- Using another developer's brand name or icon

**How to prevent it:**

Screenshots:
- Must show the app IN USE (not splash screen, not login page)
- Must accurately represent the current build (don't show v2 mockups for v1)
- Minimum 3 screenshots, recommended 6 for full story
- Use real app screens, not Figma mockups with different UI
- Device frames are fine but the app content must be real

Description:
- Only describe features that exist in the current build
- Don't mention "coming soon" features
- Include subscription pricing and terms
- Don't stuff with keywords that aren't relevant

Keywords (100 character limit):
- Relevant terms only
- No competitor brand names
- No generic terms that don't describe your app
- Separate with commas, no spaces after commas
- Don't repeat words already in your app name

**2026 update:** You cannot use another developer's icon, brand, or product name in your app's icon or name without their approval.

**Checklist:**
- [ ] All 6 screenshots show app in active use
- [ ] Screenshots match the actual submitted build
- [ ] No splash screens or login pages as screenshots
- [ ] Description only mentions features that exist
- [ ] No competitor names in keywords
- [ ] Keywords under 100 characters
- [ ] App name doesn't contain pricing info
- [ ] No other developer's brand in app name or icon

---

## 6. Guideline 4.3 - Spam / app duplication

**Apple guideline number:** 4.3, 4.3(a)

**What triggers it:**
- Multiple apps from same developer with near-identical functionality
- App is a template/clone with minimal customization
- App provides same features as existing apps with only content/language variation
- Same binary submitted with different metadata

**This is critical for the PRINTMAXX app factory model** where we build multiple "Lock" apps (PrayerLock, WalkToUnlock, StudyLock, FocusLock). Each MUST be genuinely different.

**How to differentiate:**
1. Each app must have a unique core mechanic (prayer tracking vs step counting vs study timers vs pomodoro)
2. Different UI themes, not just color swaps (different layouts, different information architecture)
3. Different feature sets beyond the lock mechanism
4. Different target audiences with audience-specific content
5. Use different developer accounts if building similar category apps (risky but some do it)
6. Different onboarding flows tailored to each audience

**What Apple looks for:**
- Different binary (not just reskinned)
- Different metadata (description, keywords, screenshots)
- Different core value proposition
- Meaningful feature differences

**If rejected for 4.3:**
- Book a one-on-one App Review consultation through "Meet with Apple" weekly events
- Apple's rejection messages are vague. The consultation lets you get specific guidance.

**Checklist:**
- [ ] App has genuinely unique core functionality
- [ ] UI is not a color-swap of another app you submitted
- [ ] Feature set is meaningfully different from your other apps
- [ ] Description clearly explains what makes this app unique
- [ ] Onboarding is tailored to this app's specific audience
- [ ] Screenshots show unique features, not shared ones

---

## 7. Guideline 5.1.2 - App Tracking Transparency (ATT)

**Apple guideline number:** 5.1.2

**What triggers it:**
- Tracking users across apps/websites without ATT prompt
- Generic ATT prompt text ("tracking for ads")
- ATT prompt interrupts critical user flow (shown immediately on launch)
- Not disclosing specific data recipients

**Current requirements (2026):**
- ATT prompt required if you track users across apps/websites for advertising
- Prompt must use non-technical language (8th grade reading level)
- Must specify actual partners, not just "advertising partners"
- Must present balanced visual hierarchy between accept and reject
- If ATT opt-in rate is below 30%, expect 58% advertising revenue loss

**For most PRINTMAXX apps (no ads, no cross-app tracking):**
- You probably don't need ATT at all
- RevenueCat doesn't require ATT
- If you add analytics (Mixpanel, Amplitude), check if they trigger ATT
- Privacy-focused analytics (Plausible, PostHog self-hosted) typically don't require ATT

**If you DO need ATT:**
- Don't show it on first launch
- Show it after the user has experienced value
- Explain the benefit to the user (personalized experience, relevant content)
- Use specific partner names in the prompt

**Checklist:**
- [ ] Determined whether ATT is needed (probably not for subscription apps without ads)
- [ ] If using ads: ATT prompt implemented with specific partner names
- [ ] ATT prompt doesn't appear on first launch
- [ ] ATT prompt uses plain language
- [ ] If not using ATT: confirmed no SDKs are tracking across apps

---

## 8. Guideline 4.0 - Design (UI quality)

**Apple guideline number:** 4.0, 4.1, 4.2

**What triggers it:**
- Spelling and grammar errors in the app
- Broken layouts or overlapping elements
- Images that don't scale properly
- Animation glitches
- Non-standard UI that confuses users
- App looks like it was built in a weekend (because it was, but it shouldn't look like it)

**How to prevent it:**
- Follow Apple Human Interface Guidelines for navigation, typography, and interaction patterns
- Use standard iOS UI components (tab bar, navigation bar, action sheets)
- Test on multiple screen sizes (iPhone SE through iPhone 15 Pro Max)
- Fix every visual bug, even minor ones. Apple reviewers notice.
- No web-style patterns on mobile (no hover tooltips, no right-click menus, no horizontal scrollbars)

**For Capacitor.js apps specifically:**
- Disable rubber-band bounce scrolling where it doesn't make sense
- Hide the status bar during splash, show it after
- Match the keyboard appearance to your app's color scheme
- Use `safe-area-inset` CSS properties for notch/Dynamic Island
- Don't use browser-style back buttons (use native nav patterns)

**Checklist:**
- [ ] Zero spelling/grammar errors (run a spell checker)
- [ ] Tested on iPhone SE, iPhone 14, iPhone 15 Pro Max screen sizes
- [ ] No overlapping elements on any screen size
- [ ] All images scale properly
- [ ] No broken animations
- [ ] Standard iOS navigation patterns used
- [ ] Safe area insets respected (notch, Dynamic Island, home indicator)
- [ ] No web-only UI patterns (hover states, horizontal scroll, etc.)

---

## 9. Health and medical claims (for health/fitness apps)

**Apple guideline number:** 1.4, 1.4.1

**What triggers it:**
- Claiming the app can diagnose, treat, or cure conditions
- Using words like "cure", "fix", "treat", "diagnose"
- Medical claims without professional backing
- Health data handling without proper disclosure

**How to prevent it:**
- Use language like "track", "monitor", "support", "help manage"
- Attribute all health recommendations to published researchers with citations
- Include disclaimer: "Not a substitute for professional medical advice"
- If integrating HealthKit: additional privacy requirements apply

**Checklist:**
- [ ] No "cure/fix/treat/diagnose" language anywhere in app or description
- [ ] All health claims attributed to named researchers
- [ ] Medical disclaimer included in app and description
- [ ] HealthKit privacy requirements met (if applicable)

---

## 10. Age rating and content (2026 changes)

**Apple guideline number:** Various

**What triggers it:**
- Incorrect age rating for content
- Not completing new age-rating questionnaire (required since Jan 31, 2026)
- Creator apps without age restriction mechanisms

**2026 changes:**
- Apple replaced 4+ and 9+ ratings with granular 13+, 16+, 18+ structure
- Starting Jan 31, 2026: new age-rating questionnaire required for all new submissions
- Starting April 28, 2026: apps must be built with iOS 26 SDK
- Creator apps must have age verification mechanism
- If app uses AI services: consent modal required specifying provider and data types before any personal data is shared

**Checklist:**
- [ ] New age-rating questionnaire completed in App Store Connect
- [ ] Age rating matches actual content
- [ ] Built with iOS 26 SDK (required from April 2026)
- [ ] AI consent modal implemented if using external AI services
- [ ] Creator app age restriction implemented if applicable

---

## 11. App review notes strategy

**This is free insurance against rejection. Use it.**

Your App Review Notes should include:

1. **Testing instructions** - Step by step, assume the reviewer has never seen your app
2. **Demo account** - If login required, provide credentials. If no login, say "No login required"
3. **Feature walkthrough** - Point out 3-5 key features and where to find them
4. **Subscription details** - Pricing, trial period, how to test
5. **Privacy explanation** - What data you collect (or don't)
6. **Health disclaimers** - If health app, state your compliance
7. **Why this isn't a website** - For Capacitor apps, proactively list the native features you use

**Example for a Capacitor PWA:**

```
NATIVE FEATURES (this is not a web wrapper):
1. Push notifications for daily reminders (@capacitor/push-notifications)
2. Haptic feedback on all key interactions (@capacitor/haptics)
3. Local notifications for streak reminders (@capacitor/local-notifications)
4. Native share sheet integration (@capacitor/share)
5. Offline mode with full functionality (service worker + @capacitor/preferences)
6. App state management and deep linking (@capacitor/app)

All data stored locally on device. No cloud backend required for core functionality.
```

If a reviewer can't figure out your app in 2 minutes, they'll flag it. Make their job easy.

**Checklist:**
- [ ] Review notes written with step-by-step testing instructions
- [ ] Demo credentials included (if applicable)
- [ ] Native features explicitly listed (for Capacitor apps)
- [ ] Subscription details clearly stated
- [ ] Privacy stance explained

---

## 12. External payment links (US only, post-Epic ruling)

**Apple guideline number:** 3.1.1 (modified for US)

**Current state (Feb 2026):**
- Epic v. Apple ruling (April 30, 2025): banned Apple from charging commission on external purchases
- Dec 2025 appeals court: Apple CAN charge a "reasonable commission" on external link purchases
- US App Store only: you can include buttons/links to external checkout
- No External Link Account entitlement required for US storefront
- You CANNOT remove Apple IAP entirely (must offer both)
- Apple cannot restrict the design or placement of external payment links

**Strategy for PRINTMAXX apps:**
- Offer Apple IAP as primary (simpler, higher trust, better conversion on iOS)
- Add Stripe web checkout link for power users who want to avoid Apple's cut
- RevenueCat handles both Apple IAP and Stripe seamlessly
- Track which payment method converts better and optimize

**Checklist:**
- [ ] Apple IAP configured as primary payment method
- [ ] External payment link (Stripe) added for US users (optional)
- [ ] Both payment methods tested end-to-end
- [ ] Clear disclosure that both options are available

---

## Rejection response protocol

When (not if) you get rejected:

1. **Read the rejection reason carefully.** It references specific guideline numbers. Look them up.
2. **Don't resubmit the same binary.** Apple tracks this and it wastes everyone's time.
3. **Fix the actual issue.** Make meaningful changes.
4. **Reply in App Store Connect** by clicking "Reply to App Review." The specialist assigned knows your app.
5. **Write a short "what changed / where to test" note.** Don't write an essay.
6. **Resubmit quickly.** Fast turnaround shows responsiveness.
7. **If still stuck:** Book a one-on-one App Review consultation at developer.apple.com/contact/app-store (weekly "Meet with Apple" events).
8. **If you believe the rejection is wrong:** File an appeal through the App Review Board.

**Typical rejection-to-approval cycle:** 3-7 days if you respond promptly.

---

## Master pre-submission checklist

Run through this entire list before clicking "Submit for Review."

### App completeness
- [ ] Zero crashes in 30 min testing on real device
- [ ] No placeholder content anywhere
- [ ] Every button/link functional
- [ ] Works offline (for PWA apps)
- [ ] Backend servers running (if applicable)

### Native feel (Capacitor-specific)
- [ ] 3+ native Capacitor plugins integrated
- [ ] Haptic feedback on key interactions
- [ ] No web artifacts (rubber banding, URL bar, web spinners)
- [ ] Native navigation patterns (no hamburger-only nav)
- [ ] Safe area insets respected
- [ ] No hover states in CSS

### Privacy and data
- [ ] Privacy policy URL live and complete
- [ ] Terms of Service URL live
- [ ] Privacy Nutrition Label accurate in App Store Connect
- [ ] Permission strings explain specific usage
- [ ] New age-rating questionnaire completed

### Monetization
- [ ] Apple IAP configured and tested
- [ ] "Restore Purchases" visible and functional
- [ ] Subscription terms on paywall screen
- [ ] Auto-renewal disclosure in App Store description
- [ ] Free trial tested in sandbox

### Metadata
- [ ] 6 screenshots showing app in use (not splash/login)
- [ ] Screenshots match actual build
- [ ] Description only claims existing features
- [ ] Keywords relevant, under 100 chars, no competitor names
- [ ] App name clean (no pricing, no competitor brands)

### Review preparation
- [ ] Review notes with testing instructions
- [ ] Demo account credentials (if login required)
- [ ] Native features listed in review notes
- [ ] Health disclaimers included (if health app)

### Design quality
- [ ] Spell-checked all text
- [ ] Tested on 3+ screen sizes
- [ ] No overlapping elements
- [ ] Animations smooth (60fps)
- [ ] Standard iOS patterns followed

### Automated compliance scan (RevylAI Greenlight)
- [ ] `greenlight preflight /path/to/project` run with zero FAIL results
- [ ] `greenlight preflight . --ipa build.ipa` run with zero FAIL results (if IPA built)
- [ ] All WARN results reviewed and fixed or documented
- [ ] JSON report saved for audit trail

---

## Automated rejection prevention: RevylAI Greenlight (MANDATORY)

Manual checklists catch most issues, but code-level patterns are easy to miss -- especially private API usage buried in third-party SDKs, missing privacy manifest entries, and hardcoded secrets. RevylAI Greenlight (`https://github.com/RevylAI/greenlight`) automates the detection of 30+ rejection-causing patterns.

**What Greenlight scans (mapped to rejection guidelines above):**

| Greenlight Check | Maps to Guideline | What It Catches |
|-----------------|-------------------|-----------------|
| Metadata scan | 2.1, 2.3 | Missing Info.plist keys, invalid bundle ID format, missing privacy policy URL, missing icons |
| Code pattern scan | 2.5.1, 3.1.1, 4.2 | Private API usage (IOKit, WebKit internals), hardcoded API keys/secrets, non-IAP payment SDKs, dynamic code loading (dlopen, NSClassFromString), JIT compilation |
| Privacy scan | 5.1.1, 5.1.2 | Missing PrivacyInfo.xcprivacy, undeclared Required Reason APIs (UserDefaults, DiskSpace, FileTimestamp, SystemBootTime), tracking SDKs without ATT |
| IPA binary scan | 2.1, 4.0 | Missing app icons in binary, missing launch storyboard, oversized IPA, architecture issues |

**How to use it:**

```bash
# Install
pip install greenlight-appstore

# Scan project directory (catches metadata + code + privacy issues before build)
greenlight preflight /path/to/ios/project

# Scan with built IPA (adds binary analysis)
greenlight preflight /path/to/ios/project --ipa build/App.ipa --format json

# PRINTMAXX portfolio scan (all 6 apps at once)
python3 AUTOMATIONS/greenlight_checker.py --all
python3 AUTOMATIONS/greenlight_checker.py --app ramadan-tracker
```

**When to run:**
1. After completing development (before TestFlight) -- catches code and metadata issues early
2. After building IPA (before submission) -- catches binary-level issues
3. After any dependency update -- new SDKs may introduce private API usage or tracking

**Integration with our quality gates:**
- Gate 2 (Build review): `greenlight preflight` must pass with zero FAIL results
- Gate 3 (Submission review): `greenlight preflight --ipa` must pass with zero FAIL results
- See `APP_QUALITY_STANDARDS.md` Section 9 and `IOS_SUBMISSION_PROCESS.md` Section 3.10

**This tool exists because:** Apple uses automated scanning during review. Running the same kind of scan before submission means you catch what Apple's scanner will catch -- before they reject you and cost you 3-7 days.

---

## Sources

Research compiled from:
- [Apple App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [NextNative - App Store Review Guidelines 2025](https://nextnative.dev/blog/app-store-review-guidelines)
- [Twinr - Apple App Store Rejection Reasons 2025](https://twinr.dev/blogs/apple-app-store-rejection-reasons-2025/)
- [BetaDrop - Top 10 iOS App Rejection Reasons 2026](https://betadrop.app/blog/ios-app-rejection-reasons-2026)
- [Adapty - App Store Review Guidelines 2026 Checklist](https://adapty.io/blog/how-to-pass-app-store-review/)
- [RevenueCat - Ultimate Guide to App Store Rejections](https://www.revenuecat.com/blog/growth/the-ultimate-guide-to-app-store-rejections/)
- [RevenueCat - Apple Anti-Steering Ruling](https://www.revenuecat.com/blog/growth/apple-anti-steering-ruling-monetization-strategy/)
- [MacRumors - Apple External Payment Link Fees](https://www.macrumors.com/2025/12/11/apple-app-store-fees-external-payment-links/)
- [Capacitor.js Documentation](https://capacitorjs.com/docs)
- [Ionic Forum - Guideline 4.2 Rejections](https://forum.ionicframework.com/t/app-store-rejection-4-2-design-minimum-functionality-my-first-after-2-years-of-ionic/200908)
- [Apple Developer Forums - Guideline 4.2](https://developer.apple.com/forums/thread/806726)
- [Business of Apps - ATT Opt-In Rates 2026](https://www.businessofapps.com/data/att-opt-in-rates/)
