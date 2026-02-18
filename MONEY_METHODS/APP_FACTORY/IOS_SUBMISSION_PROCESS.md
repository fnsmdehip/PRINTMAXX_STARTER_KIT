# iOS App Store submission process

**Last updated:** 2026-02-12
**Stack:** PWA (Next.js/React) + Capacitor.js + RevenueCat + Stripe (web fallback)
**Purpose:** Step-by-step submission process that leaves nothing to chance. Every item is checkable (yes/no). Every requirement references a real Apple guideline number.

**Context:** Apple reviewed 7.77M submissions in 2024 and rejected ~25% of them. Average review time is 24-48 hours, but first submissions can take up to 1 week. Every rejection costs you 3-7 days minimum. Do this right the first time.

---

## Phase 1: Pre-build checklist (before writing any code)

Complete every item before opening your IDE. Skipping this phase causes the most expensive rework.

### 1.1 App name and legal

- [ ] **App name search on App Store** -- search App Store Connect and live App Store for exact name conflicts
- [ ] **Trademark search on USPTO.gov** -- search TESS database (tmsearch.uspto.gov) for your exact app name in Class 009 (software) and Class 042 (SaaS)
- [ ] **Domain availability check** -- check if [appname].com or [appname].app is available (needed for support URL and privacy policy hosting)
- [ ] **Social handle availability** -- check @[appname] on X, Instagram, TikTok (not blocking but useful for marketing)
- [ ] **Name does not contain** -- price info (Guideline 2.3.7), another developer's brand name (Guideline 2.3.1, updated Nov 2025), generic Apple terms like "iPhone" or "iPad" (Guideline 2.3.1)
- [ ] **Name is under 30 characters** (App Store Connect limit)
- [ ] **Subtitle is under 30 characters** (App Store Connect limit)

### 1.2 Category selection

Pick your primary and secondary categories now. This affects which reviewers see your app and what competition you face.

| App type | Recommended primary | Recommended secondary |
|----------|--------------------|-----------------------|
| Prayer/faith | Lifestyle | Health & Fitness |
| Habit tracker | Health & Fitness | Productivity |
| Sleep tracker | Health & Fitness | Lifestyle |
| Focus timer | Productivity | Education |
| Walking/fitness | Health & Fitness | Lifestyle |
| Meal tracker | Food & Drink | Health & Fitness |
| Fasting app | Health & Fitness | Lifestyle |

- [ ] **Primary category selected**
- [ ] **Secondary category selected**
- [ ] **Category matches actual app functionality** (Guideline 2.3.3 -- wrong category = rejection)

### 1.3 Revenue model decision

Decide before building. Your architecture depends on this.

- [ ] **Revenue model chosen** -- subscription / freemium / one-time purchase / ads + subscription hybrid
- [ ] **Pricing tiers defined** -- weekly, monthly, annual prices using Apple's standard pricing tiers (you cannot set custom prices like $4.37; must use $4.99, $3.99, etc.)
- [ ] **Free trial length decided** -- minimum 3 days, recommended 7 days (trials under 4 days convert 30% worse)
- [ ] **Apple Small Business Program enrolled** -- if under $1M/year revenue, enroll for 15% commission instead of 30% (developer.apple.com/programs/small-business/)
- [ ] **RevenueCat account created** at app.revenuecat.com
- [ ] **Stripe account created** (for web fallback / external payment link in US)

### 1.4 Required native features list

Apple rejects PWA wrappers that don't use native device capabilities (Guideline 4.2, 4.2.2). You must integrate a minimum of 3 Capacitor native plugins.

- [ ] **3+ Capacitor native plugins planned from this list:**
  - `@capacitor/haptics` -- tactile feedback on button presses, completions, errors
  - `@capacitor/push-notifications` -- remote push notifications
  - `@capacitor/local-notifications` -- scheduled reminders, streaks, daily check-ins
  - `@capacitor/status-bar` -- native status bar color/style control
  - `@capacitor/app` -- app state changes, deep links, back button handling
  - `@capacitor/preferences` -- native key-value storage (not just localStorage)
  - `@capacitor/share` -- native share sheet integration
  - `@capacitor/camera` -- if your app needs photo input
  - `@capacitor/keyboard` -- keyboard appearance control
  - `@capacitor/motion` -- accelerometer/gyroscope access
- [ ] **Plugins written down in a list** -- you will reference these in your App Review Notes

### 1.5 Privacy and legal URLs

These must be live before you can submit. Prepare them now.

- [ ] **Privacy policy URL planned** -- must be hosted on HTTPS (not a Google Doc, Apple flags those)
  - Free hosting options: GitHub Pages, Vercel, Netlify, your own domain
  - Generator options: Termly.io (free tier), Iubenda ($27/year), PrivacyPolicies.com
- [ ] **Terms of Service URL planned** -- can be a simple page, must be on HTTPS
- [ ] **Support URL planned** -- can be an email address page, a contact form, or a FAQ page
- [ ] **Support email address decided** -- appears on your App Store listing

### 1.6 Age rating pre-determination

Apple overhauled age ratings in July 2025. New categories: 4+, 9+, 13+, 16+, 18+ (the old 12+ and 17+ are gone). You must answer the new age rating questionnaire.

| App content | Likely rating | Notes |
|-------------|---------------|-------|
| No sensitive content, no UGC | 4+ | Most utility/tracker apps |
| Mild themes, infrequent mature content | 9+ | Faith apps with fasting (mild health) |
| Medical/wellness topics, moderate themes | 13+ | Health trackers, fasting apps |
| Frequent intense themes, unrestricted web access | 16+ | Apps with AI chat, web browsing |
| Explicit content | 18+ | Adult content (separate account) |

- [ ] **Expected age rating determined**
- [ ] **New age rating questionnaire questions reviewed** -- covers: in-app controls, capabilities, medical/wellness topics, violent themes (deadline was Jan 31, 2026 -- must be answered for all apps)

### 1.7 Developer account readiness

- [ ] **Apple Developer Program membership active** ($99/year at developer.apple.com/programs/)
- [ ] **Developer account in good standing** (no recent flags or suspensions)
- [ ] **App Store Connect access confirmed** (appstoreconnect.apple.com)
- [ ] **Latest Xcode installed** (required: Xcode 16+ for current submissions; Xcode with iOS 26 SDK required from April 28, 2026)
- [ ] **Physical iPhone available for testing** (not just Simulator -- Simulator misses memory issues, orientation bugs, performance problems)
- [ ] **Apple sandbox tester account created** (Settings > App Store > Sandbox Account on test device)

---

## Phase 2: Build standards (during development)

These standards apply throughout the entire build. Don't try to bolt them on at the end.

### 2.1 Native plugin integration checklist

Every Capacitor app must integrate these to pass Guideline 4.2:

**Mandatory (include in every app):**

- [ ] `@capacitor/haptics` installed and integrated
  - [ ] `ImpactStyle.Light` on every primary button tap
  - [ ] `ImpactStyle.Medium` on toggle switch state changes
  - [ ] `NotificationType.Success` on achievements/milestones
  - [ ] `NotificationType.Error` on form validation failures
  - [ ] `ImpactStyle.Heavy` on long press / context menu
  - [ ] Minimum 5 distinct interactions have haptic feedback
- [ ] `@capacitor/local-notifications` installed and integrated
  - [ ] At least 1 scheduled notification type (daily reminder, streak alert, etc.)
  - [ ] Permission request with specific usage string (not generic)
- [ ] `@capacitor/preferences` installed and integrated
  - [ ] User settings stored in native Preferences, not just localStorage
  - [ ] App state persists across kills/restarts via Preferences
- [ ] `@capacitor/app` installed and integrated
  - [ ] App state change listeners (foreground/background transitions)
  - [ ] Deep link handling configured (even if not used yet, register the handler)
  - [ ] Back button behavior handled (no browser-style back)
- [ ] `@capacitor/status-bar` installed and integrated
  - [ ] Status bar style matches app theme (light/dark)
  - [ ] Status bar hidden during splash, shown after

**Recommended (include at least 1):**

- [ ] `@capacitor/push-notifications` -- remote push via APNs
- [ ] `@capacitor/share` -- native share sheet
- [ ] `@capacitor/camera` -- if app needs photo input
- [ ] `@capacitor/keyboard` -- keyboard appearance control

### 2.2 iOS Human Interface Guidelines compliance

Reference: developer.apple.com/design/human-interface-guidelines/

- [ ] **Navigation uses iOS patterns** -- tab bar for top-level navigation (not hamburger menu as primary nav), navigation bar for hierarchical drill-down, swipe-back gesture enabled
- [ ] **No web-only UI patterns** -- no hover states in CSS (hover doesn't exist on touch), no horizontal scrollbars, no right-click context menus, no browser-style loading spinners, no URL bar visible
- [ ] **System fonts or intentional custom fonts** -- SF Pro is default; if custom, define full type scale (Display 34px, H1 28px, H2 22px, Body 17px, Caption 13px, Overline 11px)
- [ ] **Touch targets minimum 44x44pt** -- Apple HIG requirement, every interactive element
- [ ] **Safe area insets respected** -- notch, Dynamic Island, home indicator all accounted for via CSS `env(safe-area-inset-top)` etc.
- [ ] **Standard iOS components used** -- action sheets (not custom modals) for destructive choices, system alerts for critical messages, native-feeling toggles
- [ ] **No rubber-band bounce scrolling** where it doesn't make sense (disable on fixed views)
- [ ] **Keyboard dismissal** -- tapping outside text input dismisses keyboard
- [ ] **Pull-to-refresh** -- only on scrollable lists, with custom animation (not browser default)

### 2.3 Accessibility requirements (WCAG 2.1 AA minimum)

Guideline 4.0 -- Apple explicitly reviews for accessibility.

- [ ] **All text meets contrast ratio** -- 4.5:1 for body text, 3:1 for large text (18px+ bold or 24px+ regular)
- [ ] **VoiceOver labels on all interactive elements** -- buttons, links, inputs, toggles all have `aria-label` or `accessibilityLabel`
- [ ] **VoiceOver navigation tested** -- enable VoiceOver on test device, navigate every screen
- [ ] **Dynamic Type supported** -- text scales with system font size settings up to 200%
- [ ] **Reduce Motion respected** -- check `prefers-reduced-motion` media query, disable non-essential animations
- [ ] **No information conveyed by color alone** -- icons, labels, or patterns accompany color indicators
- [ ] **Focus indicators visible** -- focusable elements have visible focus rings for switch control users

### 2.4 Dark mode support

- [ ] **Full dark mode implementation** (not just inverted colors)
- [ ] **System preference detection** -- `prefers-color-scheme` media query respects iOS setting
- [ ] **Manual toggle in Settings screen** -- user can override system preference
- [ ] **True black (#000000) backgrounds for OLED** -- saves battery on iPhone Pro models
- [ ] **All assets work on both backgrounds** -- icons, illustrations, images tested on light and dark
- [ ] **No hardcoded colors** -- all colors use CSS custom properties or theme tokens

### 2.5 iPad support decision

- [ ] **iPad support decided** -- yes (universal) or no (iPhone only)
- [ ] If yes: layouts tested on iPad Mini (8.3"), iPad Air (10.9"), iPad Pro (12.9")
- [ ] If yes: split view and slide over work correctly
- [ ] If no: confirmed in App Store Connect that app is iPhone-only (some categories like Games have stricter iPad requirements)

### 2.6 Performance benchmarks

| Metric | Target | Hard reject if |
|--------|--------|----------------|
| App launch to interactive | < 1 second | > 3 seconds |
| Lighthouse Performance score | > 90 | < 80 |
| Lighthouse Accessibility score | > 90 | < 85 |
| First Contentful Paint | < 1.5s | > 2.5s |
| Largest Contentful Paint | < 2.5s | > 4.0s |
| Cumulative Layout Shift | < 0.1 | > 0.25 |
| Total bundle size (gzipped) | < 500KB | > 1MB |
| JavaScript bundle (gzipped) | < 300KB | > 500KB |
| Memory usage (steady state) | < 150MB | > 300MB |
| Animation frame rate | 60fps | < 30fps |
| IPA file size | < 100MB | > 200MB (affects cellular download) |

- [ ] **All performance benchmarks met**
- [ ] **No white flash on launch** -- splash screen covers the WebView load time
- [ ] **No jank during scrolling** -- profile with Safari Web Inspector on connected device
- [ ] **No memory leaks** -- profile with Instruments > Allocations on real device over 10 min session

### 2.7 Offline functionality

Guideline 4.2 -- offline capability is a strong signal that your app is not just a website.

- [ ] **Service worker caches app shell and critical assets**
- [ ] **Core features work without internet** (tracking, logging, viewing saved data)
- [ ] **Offline indicator shown** -- subtle banner, not a blocking modal
- [ ] **Queued actions sync when connection returns** (if applicable)
- [ ] **No blank screens when offline** -- every screen has an offline fallback
- [ ] **Data stored in Capacitor Preferences persists** -- not dependent on web cache

### 2.8 PrivacyInfo.xcprivacy manifest (required since May 2024)

Apple requires a privacy manifest file declaring your use of certain APIs. Capacitor apps typically need this.

- [ ] **PrivacyInfo.xcprivacy file created** in `/ios/App/`
- [ ] **Required Reasons APIs declared:**
  - `NSPrivacyAccessedAPICategoryUserDefaults` (reason: `CA92.1`) -- if using `@capacitor/preferences`
  - `NSPrivacyAccessedAPICategoryDiskSpace` (reason: `7D9E.1`) -- if checking storage
  - `NSPrivacyAccessedAPICategoryFileTimestamp` (reason: `3B52.1`) -- if accessing file metadata
  - `NSPrivacyAccessedAPICategorySystemBootTime` (reason: `35F9.1`) -- if checking uptime
- [ ] **Third-party SDK privacy manifests included** -- RevenueCat, analytics SDKs each provide their own
- [ ] **Capacitor version is 5.7.4+, 6.0.0+, or 8.0+** (older versions don't support privacy manifests)

---

## Phase 3: Pre-submission audit (the gate)

This is the quality gate. Every item must be YES before you submit. No exceptions, no "we'll fix it in the next update."

### 3.1 Screenshot requirements

As of 2025-2026, Apple requires the 6.9-inch iPhone size as the mandatory base. Apple automatically scales it for smaller devices.

**Required device sizes:**

| Device class | Dimensions (portrait) | Status |
|-------------|----------------------|--------|
| iPhone 6.9" (16 Pro Max) | 1320 x 2868 px | MANDATORY |
| iPad 13" | 2064 x 2752 px | MANDATORY (if iPad support enabled) |

**All other sizes auto-scale from the 6.9" submission.**

- [ ] **6.9" iPhone screenshots created** at exactly 1320 x 2868 pixels
- [ ] **Minimum 3 screenshots, target 6, maximum 10**
- [ ] **Screenshot 1:** Hero shot -- main app screen with headline benefit visible
- [ ] **Screenshot 2:** Core feature 1 in action
- [ ] **Screenshot 3:** Core feature 2 showing depth
- [ ] **Screenshot 4:** Progress/tracking/stats screen
- [ ] **Screenshot 5:** Settings or personalization showing polish
- [ ] **Screenshot 6:** Additional feature or social proof
- [ ] **NO screenshots of splash screen** (Guideline 2.3)
- [ ] **NO screenshots of login page** (Guideline 2.3)
- [ ] **ALL screenshots show app actively being used** (Guideline 2.3)
- [ ] **ALL screenshots match the actual submitted build exactly** (Guideline 2.3 -- mismatched screenshots = automatic rejection)
- [ ] **Format:** PNG or JPEG (PNG preferred for text clarity)
- [ ] **If iPad enabled:** 13" iPad screenshots at 2064 x 2752 px

### 3.2 App Preview video specifications

Optional but increases conversion 20-30%.

- [ ] **Duration:** 15-30 seconds (15-25 seconds recommended)
- [ ] **Resolution:** matches device screenshot dimensions (1320 x 2868 for 6.9" iPhone portrait)
- [ ] **Format:** H.264 or ProRes 422 (HQ), .mov or .mp4 container
- [ ] **File size:** under 500 MB
- [ ] **Content:** screen captures recorded on actual device only -- no live-action footage, no hands operating device, no simulated interface elements
- [ ] **Audio:** optional, but if included, no copyrighted music
- [ ] **Maximum 3 preview videos per localized listing**

### 3.3 Metadata requirements

**App Store description:**

- [ ] **Description only mentions features that exist in the current build** (Guideline 2.3)
- [ ] **No "coming soon" features mentioned** (Guideline 2.1)
- [ ] **No competitor names** (Guideline 2.3.1)
- [ ] **Subscription auto-renewal disclosure included** -- required text: "Payment will be charged to your Apple ID account at the confirmation of purchase. The subscription automatically renews unless it is canceled at least 24 hours before the end of the current period. Your account will be charged for renewal within 24 hours prior to the end of the current period. You can manage and cancel your subscriptions by going to your App Store account settings after purchase."
- [ ] **Health/medical disclaimer included** (if health app) -- "This app is not a medical device and is not intended to diagnose, treat, cure, or prevent any disease."
- [ ] **FTC affiliate disclosure included** (if affiliate links present)

**Keywords:**

- [ ] **Under 100 characters total** (hard limit)
- [ ] **Comma-separated, no spaces after commas**
- [ ] **No competitor brand names** (Guideline 2.3.7)
- [ ] **No words already in your app name** (duplicating wastes characters)
- [ ] **No generic terms** ("app," "free," "best") -- waste of keyword space
- [ ] **Include relevant niche terms** your target users actually search for

**Other metadata:**

- [ ] **Promotional text** (170 chars, can update without new build) written
- [ ] **"What's New" text** written (even for v1.0, write something like "Initial release of [app name]")
- [ ] **Copyright field** filled in (format: "2026 [Your Name or Company]")

### 3.4 Demo account for reviewers

Guideline 2.1 -- if your app requires login, you MUST provide demo credentials.

- [ ] **If login required:** demo username and password created and tested
- [ ] **Demo account has full access** to all features (including premium if subscription app)
- [ ] **Demo account credentials work right now** (test them before submitting)
- [ ] **If no login required:** noted "No login required" in review notes
- [ ] **If app requires specific hardware** (BLE device, etc.): noted in review notes with video demo

### 3.5 Privacy Nutrition Labels

App Store Connect asks a series of questions about your data practices. These labels appear on your listing. They MUST match your actual behavior (Guideline 5.1.1).

**Apple asks about these data categories:**

| Category | If you use... | Declare |
|----------|--------------|---------|
| Contact Info | User creates account with email | YES: Email Address, linked to identity |
| Health & Fitness | HealthKit data | YES: specify each data type |
| Financial Info | RevenueCat / Apple IAP | YES: Purchase History, linked to identity |
| Location | GPS features | YES: Precise or Coarse location |
| Usage Data | Any analytics (Plausible, PostHog, Mixpanel, Firebase) | YES: Product Interaction |
| Diagnostics | Crash reporting (Sentry, Crashlytics) | YES: Crash Data |
| Identifiers | Device ID for analytics | YES: Device ID |
| Browsing History | In-app browser | YES if tracking URLs visited |

- [ ] **Every third-party SDK audited** for data collection (RevenueCat, analytics, crash reporting)
- [ ] **Privacy Nutrition Labels filled out in App Store Connect** matching actual behavior
- [ ] **"Data Used to Track You" section accurate** -- only declare tracking if you actually track across apps/websites
- [ ] **"Data Linked to You" section accurate** -- if you can associate data with user identity
- [ ] **"Data Not Linked to You" section accurate** -- anonymous/aggregated data
- [ ] **If you collect NO data at all:** select "Data Not Collected" (rare for any app with analytics)

### 3.6 Data collection declarations

- [ ] **All permission request strings are specific** (Guideline 5.1.1):
  - BAD: "This app needs notification access"
  - GOOD: "[AppName] sends you daily prayer reminders at your chosen times"
- [ ] **No permissions requested that aren't used** -- if you request camera but never use it, rejection
- [ ] **Usage description strings in Info.plist** for every permission:
  - `NSCameraUsageDescription` (if camera used)
  - `NSPhotoLibraryUsageDescription` (if photo library used)
  - `NSLocationWhenInUseUsageDescription` (if location used)
  - `NSHealthShareUsageDescription` (if HealthKit reading)
  - `NSHealthUpdateUsageDescription` (if HealthKit writing)
  - `NSUserTrackingUsageDescription` (if ATT needed)
  - Each string must explain WHY the app needs this specific data

### 3.7 Third-party SDK declarations

Since Nov 2025, Apple requires disclosure of AI data sharing (Guideline 5.1.1(ix)).

- [ ] **All third-party SDKs listed** (RevenueCat, analytics, crash reporting, AI APIs)
- [ ] **If using external AI services** (OpenAI, Claude, Gemini): consent modal implemented that specifies:
  - The AI service provider name
  - What data types are shared
  - Explicit user consent before any personal data is sent
- [ ] **Each SDK's privacy manifest included** in the build

### 3.8 Encryption export compliance

HTTPS counts as encryption. Almost every app triggers this.

- [ ] **Encryption compliance questionnaire answered in App Store Connect:**
  1. "Does your app use encryption?" -- YES (if using HTTPS, which you are)
  2. "Does your app qualify for any exemptions?" -- YES, select "It uses encryption that is exempt" if ONLY using HTTPS via Apple's standard networking (URLSession/Capacitor's default HTTP client)
  3. If using custom encryption beyond HTTPS: may need a formal BIS classification
- [ ] **If exempt:** set `ITSAppUsesNonExemptEncryption` to `NO` in Info.plist (avoids being asked this on every upload)
- [ ] **If not exempt:** upload export compliance documentation (Apple reviews in ~2 business days, provides a key value for Xcode)

### 3.9 Build with correct SDK

- [ ] **Built with latest stable Xcode** (currently Xcode 16.x)
- [ ] **Targets minimum iOS 17** (supports current + one version back)
- [ ] **After April 28, 2026:** must use iOS 26 SDK (Xcode with iOS 26)
- [ ] **Capacitor version 6.0+ or 8.0+** (for privacy manifest support and latest APIs)
- [ ] **All CocoaPods / SPM dependencies up to date** (run `pod update` and resolve warnings)
- [ ] **No compiler warnings** in Release build (Apple reviewers see warning counts)
- [ ] **Archive build successful** with no errors

### 3.10 RevylAI Greenlight pre-submission scan (MANDATORY)

Run RevylAI Greenlight (`https://github.com/RevylAI/greenlight`) before every submission. This is an open-source Apple App Store compliance scanner that catches rejection-causing issues automatically. It checks metadata (Info.plist, icons, bundle ID format, privacy policy URLs), 30+ rejection-risk code patterns (private APIs, hardcoded secrets, unauthorized payment flows, dynamic code loading), privacy compliance (PrivacyInfo.xcprivacy, Required Reason APIs, tracking SDK declarations), and IPA binary analysis (icons, launch storyboards, size).

**Install once:**
```bash
pip install greenlight-appstore
# or clone and install from source:
git clone https://github.com/RevylAI/greenlight.git && cd greenlight && pip install -e .
```

**Run on every app before submission:**
```bash
# Scan project directory (pre-build)
greenlight preflight /path/to/ios/project

# Scan with IPA binary analysis (post-build)
greenlight preflight /path/to/ios/project --ipa build/App.ipa --format json

# Run on all 6 PRINTMAXX apps at once using wrapper script
python3 AUTOMATIONS/greenlight_checker.py --all
```

**What Greenlight catches that manual review misses:**
- Private API usage buried in third-party SDKs
- Hardcoded secrets in source code or plist files
- Missing PrivacyInfo.xcprivacy entries for Required Reason APIs
- Bundle ID format violations
- Missing or malformed privacy policy URLs in Info.plist
- Dynamic code loading patterns (dlopen, NSClassFromString on private classes)
- Unauthorized payment SDK usage outside Apple IAP
- Missing launch storyboards or incorrect icon sizes in IPA

**Checklist:**
- [ ] **Greenlight installed** (`greenlight --version` runs without error)
- [ ] **`greenlight preflight` run on project directory** with zero FAIL results
- [ ] **All WARN results reviewed** and either fixed or documented with justification
- [ ] **If IPA exists:** `greenlight preflight . --ipa build.ipa` run with zero FAIL results
- [ ] **JSON report saved** (`greenlight preflight . --format json > greenlight_report.json`) for audit trail
- [ ] **PRINTMAXX wrapper run:** `python3 AUTOMATIONS/greenlight_checker.py --app <appname>` passes

**If Greenlight finds FAILs:** Fix them before submitting. Every FAIL maps to a known Apple rejection reason. Submitting with known FAILs wastes 3-7 days on a guaranteed rejection.

---

## Phase 4: Submission process (step by step)

### Step 4.1: App Store Connect configuration

Do this once per app, well before you're ready to submit.

1. [ ] **Log in to App Store Connect** (appstoreconnect.apple.com)
2. [ ] **Click "My Apps" > "+" > "New App"**
3. [ ] **Fill in required fields:**
   - Platform: iOS
   - Name: your app name (must be unique across App Store)
   - Primary language: English (or your target)
   - Bundle ID: select from your provisioning profiles (matches Xcode bundle ID exactly)
   - SKU: unique identifier (can be anything, like "prayerlock-v1")
4. [ ] **Under "App Information":**
   - Primary category selected
   - Secondary category selected
   - Content rights: "This app does not contain, show, or access third-party content" (or declare if it does)
   - Age rating questionnaire completed (the new 2025-2026 questionnaire with medical/wellness questions)
5. [ ] **Under "Pricing and Availability":**
   - Price: Free (if freemium/subscription)
   - Availability: select countries (or all)
6. [ ] **Under "In-App Purchases":**
   - Create subscription group
   - Create individual subscription products (weekly, monthly, annual) with Apple's pricing tiers
   - Configure introductory offer (free trial) for each product
   - Products are "Ready to Submit" status
7. [ ] **Under "App Privacy":**
   - Privacy policy URL entered and verified accessible
   - Privacy Nutrition Label questionnaire completed

### Step 4.2: TestFlight internal testing

Never submit directly to App Store without TestFlight first.

1. [ ] **Upload build from Xcode:** Product > Archive > Distribute App > App Store Connect
2. [ ] **Wait for build processing** (usually 5-30 minutes)
3. [ ] **In App Store Connect > TestFlight tab:**
   - Build appears under "iOS Builds"
   - Status changes from "Processing" to "Ready to Test"
4. [ ] **Add internal testers** (up to 100, from your App Store Connect team)
5. [ ] **Add test information:**
   - Beta app description
   - What to test
   - Feedback email
6. [ ] **Internal testers test on real devices:**
   - [ ] Every screen loads without crash
   - [ ] Every button does something
   - [ ] Onboarding flow completes end-to-end
   - [ ] Subscription purchase works in sandbox
   - [ ] Restore purchases works on fresh install
   - [ ] Offline mode works (airplane mode test)
   - [ ] Push/local notifications fire correctly
   - [ ] Dark mode looks correct
   - [ ] Tested on iPhone SE (small screen) and iPhone Pro Max (large screen)
   - [ ] No console errors (connect Safari Web Inspector to test device)
7. [ ] **All critical bugs fixed** -- no crash bugs, no data loss bugs, no broken purchase flow

### Step 4.3: TestFlight external testing (recommended for v1.0)

External testing goes through a lightweight Apple review (usually 1-2 days). This is a rehearsal for the real review.

1. [ ] **Create external testing group** in TestFlight tab
2. [ ] **Add external testers** (up to 10,000 via email or public link)
3. [ ] **Submit for Beta App Review** -- Apple checks for:
   - App completeness (no crashes, no placeholder content)
   - Privacy policy accessible
   - Appropriate content
4. [ ] **If Beta App Review rejects:** fix the issue before submitting for App Store Review (same reviewer criteria apply)
5. [ ] **Collect feedback from external testers** -- bugs, UX issues, feature requests
6. [ ] **Fix all P0/P1 bugs** before App Store submission

### Step 4.4: Submission checklist

Run through this ENTIRE list. Every item must be YES.

**App Store Connect fields:**

- [ ] App name final
- [ ] Subtitle written (under 30 chars)
- [ ] Description complete with subscription terms and disclaimers
- [ ] Promotional text written (170 chars)
- [ ] Keywords set (under 100 chars, comma-separated)
- [ ] "What's New" text written
- [ ] Privacy policy URL live and loads in under 5 seconds
- [ ] Support URL live
- [ ] Marketing URL set (optional)
- [ ] Copyright text set
- [ ] Contact info (first name, last name, phone, email) filled in
- [ ] Category and secondary category set
- [ ] Age rating questionnaire answered (2025-2026 version)

**Screenshots and media:**

- [ ] 6 screenshots uploaded for 6.9" iPhone (1320 x 2868 px)
- [ ] All screenshots show real app, in use, matching this build
- [ ] iPad screenshots uploaded (if universal app)
- [ ] App Preview video uploaded (optional but recommended)

**Build:**

- [ ] Correct build selected (matches the TestFlight-tested build)
- [ ] Build is not expired (TestFlight builds expire after 90 days)
- [ ] Export compliance answered (or Info.plist key set)
- [ ] Content rights answered

**In-App Purchases:**

- [ ] All IAP products in "Ready to Submit" status
- [ ] Products attached to this app version
- [ ] Subscription group configured correctly
- [ ] Review screenshot uploaded for each IAP product (screenshot of what the purchase unlocks)

**Privacy:**

- [ ] Privacy Nutrition Labels completed
- [ ] All SDKs declared
- [ ] PrivacyInfo.xcprivacy included in build

### Step 4.5: Review notes for Apple reviewer

This is your chance to make the reviewer's job easy. Write thorough notes. This is NOT optional.

**Template (copy and customize):**

```
TESTING INSTRUCTIONS:
1. Open the app. You will see the onboarding flow (4 screens).
2. Complete onboarding by selecting any preferences.
3. On the paywall screen, tap "X" to dismiss (or test purchase with sandbox account).
4. The main screen shows [describe main feature].
5. Tap [specific button] to [specific action].
6. Navigate to Settings via the gear icon in [location].
7. Verify "Restore Purchases" works in Settings.

DEMO ACCOUNT:
[Not required -- no login in this app]
OR
Email: demo@example.com
Password: DemoPass123!

NATIVE FEATURES (this is not a web wrapper):
1. Haptic feedback on all key interactions (@capacitor/haptics)
2. Local notifications for daily reminders (@capacitor/local-notifications)
3. Native preferences storage (@capacitor/preferences)
4. Native share sheet integration (@capacitor/share)
5. Native status bar control (@capacitor/status-bar)
6. Offline mode with full functionality (service worker + native storage)

SUBSCRIPTION DETAILS:
- Weekly: $[X.XX]/week after 7-day free trial
- Monthly: $[X.XX]/month
- Annual: $[X.XX]/year after 7-day free trial (best value)
- All subscriptions auto-renew. Cancel anytime in iOS Settings.

PRIVACY:
- All user data stored locally on device
- No cloud backend required for core functionality
- [RevenueCat collects purchase data for subscription management]
- [Analytics provider] collects anonymized usage data
- No user tracking across apps/websites

HEALTH DISCLAIMER (if applicable):
This app is for general wellness purposes only. It is not a medical
device and is not intended to diagnose, treat, cure, or prevent
any medical condition.

AI DISCLOSURE (if applicable):
This app uses [AI service name] for [specific feature].
Users are shown a consent modal before any personal data is
shared with the AI service, per Guideline 5.1.1(ix).
```

- [ ] **Review notes written** following template above
- [ ] **Review notes tested** -- can a stranger follow these steps and use your app in 2 minutes?
- [ ] **Demo credentials verified** working right now (if applicable)

### Step 4.6: Submit

1. [ ] **Select the build** in App Store Connect
2. [ ] **Attach all IAP products** to this version
3. [ ] **Fill in App Review Information** (review notes, demo account, contact info)
4. [ ] **Choose release method:**
   - Manual release (recommended for v1.0 -- you control when it goes live)
   - Automatic release (goes live immediately when approved)
   - Phased release (for updates only, not v1.0)
5. [ ] **Click "Submit for Review"**
6. [ ] **Status changes to "Waiting for Review"**

**Expected timeline:**
- Waiting for Review: 0-24 hours
- In Review: 1-24 hours
- Most apps reviewed within 24-48 hours
- First submissions or unusual apps: up to 7 days
- Holiday periods (Dec-Jan): can be longer

7. [ ] **Monitor App Store Connect** for status changes
8. [ ] **Keep your backend server running** 24/7 during review (if applicable)
9. [ ] **Keep your phone nearby** -- Apple may call for clarification (rare but possible)

---

## Phase 5: Post-rejection recovery

You will get rejected. This is normal. What matters is how fast you recover.

### 5.1 Reading the rejection message

1. [ ] **Open the rejection in App Store Connect** Resolution Center
2. [ ] **Note the exact guideline number(s)** cited -- this tells you exactly what to fix
3. [ ] **Read the full text** -- Apple usually includes specific details about what they found

**Common rejection message patterns:**

| Guideline | Message pattern | What it means |
|-----------|----------------|---------------|
| 2.1 | "app crashed during review" / "placeholder content" | Your app has bugs or unfinished features |
| 2.3 | "screenshots do not reflect" / "metadata does not match" | Your screenshots or description are inaccurate |
| 3.1.1 | "in-app purchase" / "digital content" | You're selling digital goods outside Apple IAP |
| 4.0 / 4.2 | "minimum functionality" / "web clipping" | Your app is too simple or looks like a website |
| 4.3 | "spam" / "similar to existing apps" | Your app too closely resembles another app (possibly your own) |
| 5.1.1 | "privacy" / "data collection" / "nutrition labels" | Your privacy disclosures don't match your actual behavior |

### 5.2 The fix-and-reply process

1. [ ] **Fix the actual issue.** Don't just tweak wording -- make meaningful changes.
2. [ ] **Test the fix thoroughly** on a real device
3. [ ] **Upload a new build** to App Store Connect (new build number required)
4. [ ] **Reply in Resolution Center** -- click "Reply to App Review" (not "Submit for Review")
5. [ ] **In your reply, state clearly:**
   - What guideline was cited
   - What specific change you made to address it
   - Where in the app the reviewer can see the change
6. [ ] **Do NOT write a long essay.** Keep it to 3-5 sentences. Be direct.

**Example reply:**

```
Thank you for the review. We've addressed Guideline 4.2 by adding
the following native features:
1. Haptic feedback on all key interactions (Settings > Haptics toggle)
2. Local notifications for daily reminders (Settings > Notifications)
3. Native share sheet on the main screen (Share button, top right)
4. Offline mode with full functionality (test in airplane mode)

The new build (1.0.2) includes these changes. Please let us know
if you have any additional feedback.
```

### 5.3 Common quick fixes by rejection reason

| Rejection | Quick fix | Time to fix |
|-----------|-----------|-------------|
| 2.1 crash | Test on real device, fix the crash, upload new build | 1-4 hours |
| 2.1 placeholder | Remove "coming soon" sections, fill in real content | 1-2 hours |
| 2.3 metadata | Retake screenshots from current build, update description | 30-60 min |
| 3.1.1 IAP | Add Apple IAP via RevenueCat, remove external payment buttons | 2-8 hours |
| 4.2 minimum functionality | Add 2-3 Capacitor native plugins, add haptics, add stats screen | 4-16 hours |
| 4.3 spam | Change icon, color scheme, add unique feature, rewrite description | 4-8 hours |
| 5.1.1 privacy | Update privacy policy, fix Nutrition Labels, add permission strings | 1-4 hours |

### 5.4 Resubmission etiquette

- [ ] **Resubmit within 24-48 hours** -- fast turnaround shows responsiveness and gets you the same reviewer
- [ ] **Do NOT resubmit the same binary** without changes -- Apple tracks this and it flags your account
- [ ] **Always increment build number** (not version number, just build number: 1.0 build 2, build 3, etc.)
- [ ] **If rejected 3+ times for same reason:** book a one-on-one App Review consultation at developer.apple.com/contact/app-store ("Meet with Apple" weekly events)

### 5.5 Appeal process

If you believe the rejection is wrong:

1. [ ] Reply in Resolution Center explaining why you disagree (professional tone, cite specific guidelines)
2. [ ] If rejected again: click "Appeal" to escalate to the App Review Board
3. [ ] The App Review Board will review your appeal within 48 hours
4. [ ] If still rejected: request a phone call (final escalation -- be well-prepared with documentation)
5. [ ] If still rejected after phone call: accept the decision, make the requested changes, resubmit

### 5.6 Expedited review request

For time-sensitive situations only:

- [ ] Go to App Store Connect > your app > App Review
- [ ] Click "Contact Us" or use "Request Expedited Review"
- [ ] Valid reasons: critical bug fix for live app, time-sensitive event (Ramadan, holiday), security vulnerability patch
- [ ] Apple typically responds within 24 hours for expedited requests
- [ ] Do NOT abuse this -- save it for genuine emergencies

---

## Phase 6: Post-acceptance

### 6.1 Release strategy

**For v1.0 (new app):**

- [ ] **Use manual release** -- don't auto-release. Review everything first.
- [ ] **When approved, go to App Store Connect** and click "Release This Version"
- [ ] **App appears on App Store within 24 hours** of release

**For updates (v1.1+):**

- [ ] **Use phased release** -- rolls out gradually over 7 days:
  - Day 1: 1% of users
  - Day 2: 2%
  - Day 3: 5%
  - Day 4: 10%
  - Day 5: 20%
  - Day 6: 50%
  - Day 7: 100%
- [ ] **Monitor crash rates** at each phase -- if spikes, pause the release
- [ ] **You can pause for up to 30 days** (no limit on number of pauses)
- [ ] **You cannot roll back** -- only ship a new version that supersedes the broken one

### 6.2 First 48-hour monitoring

- [ ] **Monitor crash reports** in App Store Connect > Analytics > Crashes
- [ ] **Monitor App Store reviews** -- respond to every 1-star review within 24 hours
- [ ] **Check analytics** -- are users completing onboarding? Hitting the paywall? Starting trials?
- [ ] **Check RevenueCat dashboard** -- are subscriptions processing correctly?
- [ ] **Check Sentry/crash reporting** for any errors not caught in testing
- [ ] **Keep backend server stable** (no deploys during first 48 hours)
- [ ] **Check on different iOS versions** -- any version-specific crashes reported?

### 6.3 Rating prompt timing

Apple provides SKStoreReviewController for requesting ratings. Rules:

- [ ] **Do NOT prompt on first launch** -- user has no opinion yet
- [ ] **Prompt after a positive moment** -- completing a goal, hitting a streak, finishing a session
- [ ] **Minimum 3 app sessions before prompting** (user needs to be engaged)
- [ ] **Apple limits prompts to 3 times per 365-day period** per device
- [ ] **Never use custom rating prompts** -- Apple rejects apps that use non-system rating dialogs (Guideline 5.6.1)
- [ ] **Don't ask "Are you enjoying the app?" first** and only route happy users to the rating prompt -- Apple considers this manipulation (Guideline 5.6.1)
- [ ] **Implemented using StoreKit's native API** (or RevenueCat's rating prompt wrapper)

### 6.4 ASO optimization (post-launch)

Within the first 2 weeks after launch:

- [ ] **Monitor search ranking** for target keywords (AppFollow, Sensor Tower, or AppTweak free tier)
- [ ] **A/B test screenshots** -- App Store Connect has Product Page Optimization for custom product pages
- [ ] **Update keywords** if initial set isn't ranking (you can change keywords with each update, no review needed for keyword-only changes)
- [ ] **Localize metadata** for high-value markets (Germany, Japan, Brazil, Saudi Arabia -- if relevant to your niche)
- [ ] **Monitor competitor keywords** -- what terms are they ranking for that you're not?
- [ ] **Submit promotional text updates** (170 chars, updateable without new build) to test messaging

### 6.5 Post-launch content and marketing

- [ ] **Submit to directories:** Product Hunt, BetaList, StartupStash, AlternativeTo
- [ ] **Prepare "How I built [app name]" tweet thread** (building-in-public content)
- [ ] **Share on relevant subreddits** (r/[niche], r/SideProject, r/iOSProgramming)
- [ ] **Run Apple Search Ads** ($50-100/day test budget) -- target your exact keywords
- [ ] **Enable App Store Connect analytics** -- track impressions, product page views, conversion rate

---

## Appendix A: Capacitor-specific gotchas

These are issues specific to Capacitor.js that cause rejections or delays. Compiled from Ionic forums and developer reports.

| Issue | What happens | Fix |
|-------|-------------|-----|
| WebView bounce scroll visible | App feels like a website to reviewers | Set `overScrollMode: "never"` in capacitor.config.ts, or use CSS `-webkit-overflow-scrolling: touch` selectively |
| White flash on launch | WebView loads before content renders | Use a native splash screen plugin (`@capacitor/splash-screen`) with auto-hide after app is ready |
| Pull-to-refresh triggers browser reload | Not native behavior | Disable default pull-to-refresh in WKWebView config or use a custom implementation |
| Keyboard pushes view up weirdly | Default WebView keyboard behavior | Use `@capacitor/keyboard` plugin, set `resize: "none"` or `"ionic"`, handle manually |
| Links open in-app browser | URL bar visible = web feel | Use `@capacitor/browser` for external links (opens SFSafariViewController, looks native) |
| Console.log visible in production | Unprofessional, potential data leak | Strip all console statements from production build (use a build plugin or terser config) |
| Old cached version loads | Service worker serves stale content after update | Implement cache-busting strategy, increment service worker version |
| Status bar overlaps content | Content renders behind status bar | Use `safe-area-inset-top` padding and `@capacitor/status-bar` for overlay control |
| Scheme handling wrong | Deep links don't work | Configure custom URL scheme in capacitor.config.ts and Info.plist |
| Privacy manifest missing | Apple email warning or rejection since May 2024 | Add PrivacyInfo.xcprivacy with Required Reasons API declarations |

---

## Appendix B: The spam prevention strategy (Guideline 4.3)

For the PRINTMAXX app factory model of shipping multiple apps in similar categories.

### Differentiation requirements per app

| Element | Must be unique | Shared OK |
|---------|---------------|-----------|
| App icon | YES -- different shape, color, symbol | NO |
| App name | YES | NO |
| Color scheme | YES -- different primary palette | NO |
| Target audience | YES -- different demographic stated in description | NO |
| Core feature | YES -- different primary use case / mechanic | NO |
| Screenshots | YES -- different UI, different content shown | Layout style can be similar |
| Description | YES -- different value proposition, different keywords | NO |
| Onboarding flow | YES -- personalization questions differ | Screen count can be similar |
| Settings screen | YES -- different options relevant to app | Basic structure can be similar |
| Category | Preferred different | Same OK if genuinely differentiated |

### Submission timing

- [ ] **Maximum 2 similar-category apps per week**
- [ ] **Space submissions by 7-14 days** between apps in the same niche
- [ ] **If one is rejected for 4.3:** wait 14 days, add more differentiation, then resubmit
- [ ] **Use ONE developer account** for all apps (Apple trusts established accounts more than new ones)
- [ ] **Organize apps into logical families** -- Faith Suite, Health Suite, Productivity Suite

---

## Appendix C: Apple guideline reference numbers

Quick-reference for every guideline cited in this document.

| Guideline | Title | Summary |
|-----------|-------|---------|
| 1.1 | Objectionable Content | No offensive, insensitive, or inappropriate content |
| 1.2 | User Generated Content | If UGC visible to others: need moderation, reporting, blocking |
| 1.4 | Physical Harm | Health apps: no unsubstantiated medical claims |
| 2.1 | App Completeness | No crashes, no placeholder content, no broken features |
| 2.3 | Accurate Metadata | Screenshots, description, keywords must match actual app |
| 2.3.1 | No Misleading Names | No competitor brands, no Apple trademarks in name |
| 2.3.3 | Accurate Categories | Category must match functionality |
| 2.3.7 | No Misleading Keywords | No competitor names, no irrelevant terms |
| 2.5.1 | Use Public APIs Only | No private/undocumented Apple APIs |
| 3.1.1 | In-App Purchase | All digital goods must use Apple IAP (with noted exceptions) |
| 3.1.2 | Subscriptions | Clear terms, pricing, auto-renewal disclosure, restore button |
| 4.0 | Design Quality | Professional UI, no spelling errors, no broken layouts |
| 4.1 | Copycats | No copying another app's UI or brand |
| 4.2 | Minimum Functionality | App must do more than a website can; not a web wrapper |
| 4.2.2 | Web Clippings | Explicit ban on website-in-an-app-shell |
| 4.3 | Spam | No duplicate/reskinned apps, must be genuinely different |
| 5.1.1 | Data Collection & Storage | Privacy policy required, Nutrition Labels must be accurate |
| 5.1.2 | Data Use & Sharing | Disclose third-party data sharing, ATT if tracking |
| 5.1.1(ix) | AI Data Sharing | Consent modal required before sharing data with external AI (Nov 2025) |
| 5.6.1 | App Store Reviews | Use system rating prompt only, no manipulation |

---

## Appendix D: Timeline and cost estimate

### Timeline for first submission (realistic)

| Phase | Duration | Notes |
|-------|----------|-------|
| Phase 1: Pre-build | 1-2 hours | Name search, accounts, planning |
| Phase 2: Build | 2-14 days | Depends on app complexity |
| Phase 3: Pre-submission audit | 2-4 hours | Screenshot creation, metadata, privacy |
| Phase 4: TestFlight testing | 2-3 days | Internal testing, bug fixes |
| Phase 4: Submission | 30 minutes | Form filling in App Store Connect |
| Apple review | 1-7 days | Usually 24-48 hours |
| If rejected + fix + resubmit | 2-5 days | Per rejection cycle |
| **Total: first app from code-complete to live** | **5-14 days** | |

### Cost (minimum)

| Item | Cost | Frequency |
|------|------|-----------|
| Apple Developer Program | $99 | Annual |
| RevenueCat | $0 | Free up to $2,500/mo MTR |
| Privacy policy generator (Termly) | $0 | Free tier |
| Domain for support/privacy URLs | $10-15 | Annual |
| Sentry crash reporting | $0 | Free tier (50K events/mo) |
| Apple Search Ads (optional) | $50-100 | Per day test budget |
| **Total minimum to submit** | **$99** | **(just the dev program)** |

---

## Version history

| Date | Change | Author |
|------|--------|--------|
| 2026-02-12 | Initial version created from research + existing docs | Agent |

---

## Sources

- [Apple App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Apple Screenshot Specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/)
- [Apple App Preview Specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications/)
- [Apple Privacy Manifest Files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)
- [Apple Encryption Export Compliance](https://developer.apple.com/documentation/security/complying-with-encryption-export-regulations)
- [Apple Age Rating Updates](https://developer.apple.com/news/?id=ks775ehf)
- [Apple Phased Release](https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/)
- [Apple TestFlight Overview](https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/)
- [Apple App Privacy Details](https://developer.apple.com/app-store/app-privacy-details/)
- [App Store Review Times (Runway)](https://www.runway.team/appreviewtimes)
- [Adapty - App Store Review Checklist 2026](https://adapty.io/blog/how-to-pass-app-store-review/)
- [Adapty - App Store Screenshot Sizes 2026](https://adapty.io/blog/app-store-screenshot-sizes-dimensions/)
- [NextNative - App Store Review Guidelines 2025](https://nextnative.dev/blog/app-store-review-guidelines)
- [Twinr - Apple App Store Rejection Reasons 2025](https://twinr.dev/blogs/apple-app-store-rejection-reasons-2025/)
- [Capacitor Privacy Manifest](https://capacitorjs.com/docs/v5/ios/privacy-manifest)
- [Capgo - Apple Policy Updates for Capacitor Apps 2025](https://capgo.app/blog/apple-policy-updates-for-capacitor-apps-2025/)
- [TechCrunch - Apple AI Data Sharing Guidelines](https://techcrunch.com/2025/11/13/apples-new-app-review-guidelines-clamp-down-on-apps-sharing-personal-data-with-third-party-ai/)
- [9to5Mac - Apple Copycat App Guidelines](https://9to5mac.com/2025/11/13/apple-tightens-app-review-guidelines-to-crack-down-on-copycat-apps/)
- [RevenueCat - Apple Anti-Steering Ruling](https://www.revenuecat.com/blog/growth/apple-anti-steering-ruling-monetization-strategy/)
- [SplitMetrics - App Store Screenshots Guide](https://splitmetrics.com/blog/app-store-screenshots-aso-guide/)
- [Ionic Forum - Guideline 4.2 Rejections](https://forum.ionicframework.com/t/app-store-rejection-4-2-design-minimum-functionality-my-first-after-2-years-of-ionic/200908)
