# App Store Rejection & Account Ban Guide

How to avoid rejection and protect your developer accounts. Hedge fund-level risk management.

---

## The stakes

**Apple:**
- 1.93 million rejections in 2024 (25% of submissions)
- 82,000 apps removed post-launch for violations
- Account termination = all apps removed, banned from new accounts

**Google:**
- Three strikes = account termination
- Termination = all apps removed, can't create new accounts
- They track your identity across accounts (payment info, device, IP)

---

## Apple App Store rejection reasons (ranked by frequency)

### 1. App crashes and bugs (instant rejection)

**What triggers it:**
- App crashes on reviewer's device
- Features don't work
- IPv6 network issues

**How to avoid:**
- Test on REAL devices, not just simulator
- Test on older devices (iPhone 11, 12)
- Test on IPv6 networks
- Use TestFlight with 20+ beta testers before submission

### 2. App completeness (40% of rejections)

**What triggers it:**
- Placeholder text ("Lorem ipsum", "Coming soon")
- Buttons that do nothing
- Dead links in Privacy Policy or Support URLs
- Missing functionality promised in description

**How to avoid:**
- Every button must work
- Every link must be live
- Remove "coming soon" features, ship them later
- Privacy policy URL must be valid and accessible

### 3. Privacy violations

**What triggers it:**
- Requesting permissions without explaining why
- Asking for Camera/Location/Notifications on app launch
- Collecting data without disclosure
- Missing privacy nutrition labels

**How to avoid:**
- Request permissions IN CONTEXT (when user tries to use feature)
- Explain why you need each permission in the prompt
- Complete privacy nutrition labels accurately
- Link to valid privacy policy

### 4. Subscription disclosure issues

**What triggers it:**
- Price not clearly shown
- Cancellation terms hidden
- Free trial terms unclear
- Auto-renewal not disclosed

**How to avoid:**
- Show price, duration, and renewal terms on paywall
- "Cancel anytime" must be visible
- Follow Apple's subscription UI guidelines exactly
- Use RevenueCat's compliant paywall templates

### 5. Copycat apps

**What triggers it:**
- Too similar to existing popular app
- Using similar name/icon to established app
- Minimal differentiation

**How to avoid:**
- Niche differentiation (faith version, women's version, etc.)
- Unique mascot/branding
- Different feature set
- Unique name (check App Store first)

### 6. Metadata issues

**What triggers it:**
- Screenshots don't match app
- Description mentions other platforms
- Keyword stuffing
- Mentioning price in description

**How to avoid:**
- Screenshots must be current app version
- Don't mention "also on Android"
- Don't stuff keywords
- Don't mention price (App Store shows it)

---

## Google Play rejection reasons

### 1. Policy violations

**Common violations:**
- Deceptive behavior (misleading functionality)
- Malware/spyware behavior
- Data collection without consent
- Intellectual property infringement

### 2. Content policy

**What gets rejected:**
- Hate speech, violence, adult content
- Gambling without proper licensing
- Impersonation of other apps/brands

### 3. Technical issues

**What gets rejected:**
- Crashes
- ANR (App Not Responding) issues
- Battery drain
- Excessive permissions

---

## Account termination triggers (AVOID AT ALL COSTS)

### Apple account termination

**Instant termination:**
- Malware/spyware
- Fraud (fake reviews, manipulating rankings)
- Repeated guideline violations
- Submitting multiple similar "spam" apps

**How Apple tracks you:**
- Developer account info
- Payment methods
- Device IDs used for development
- IP addresses

### Google account termination

**Termination triggers:**
- Three strikes (rejections/removals)
- Egregious single violation
- Association with terminated account
- Attempting to create new account after termination

**How Google tracks you:**
- Payment info across Google services
- Device fingerprints
- IP addresses
- Behavioral patterns

---

## Risk mitigation strategy (hedge fund approach)

### Account isolation

**Don't:**
- Use same payment method for multiple dev accounts
- Develop from same devices/IPs for different accounts
- Link accounts in any way

**Do:**
- Separate LLC for each "brand" of apps
- Separate bank accounts/cards
- Different devices for different accounts
- VPN/proxy for account management (carefully)

### Pre-submission checklist

```markdown
## Before every submission

### Functionality
- [ ] App launches without crash
- [ ] All buttons work
- [ ] All links work (Privacy, Support, ToS)
- [ ] Tested on real device (not simulator)
- [ ] Tested on older device (iPhone 11/12)
- [ ] Tested on IPv6 network

### Content
- [ ] No placeholder text
- [ ] No "coming soon" features
- [ ] No offensive content
- [ ] No copyrighted content without license

### Privacy
- [ ] Permissions requested in context
- [ ] Privacy policy URL works
- [ ] Privacy nutrition labels complete
- [ ] Data collection disclosed

### Subscriptions (if applicable)
- [ ] Price clearly displayed
- [ ] Duration clearly displayed
- [ ] Cancellation terms visible
- [ ] Auto-renewal disclosed
- [ ] Free trial terms clear

### Metadata
- [ ] Screenshots current and accurate
- [ ] Description matches functionality
- [ ] No keyword stuffing
- [ ] No price mentioned in description
- [ ] No competitor names mentioned

### Differentiation
- [ ] App name unique (searched App Store)
- [ ] Icon distinctive
- [ ] Not a copy of existing app
- [ ] Clear niche/value proposition
```

### Response to rejection

**Do:**
- Read rejection reason carefully
- Fix EXACTLY what they mentioned
- Respond politely in Resolution Center
- Ask for clarification if unclear

**Don't:**
- Argue with reviewers
- Resubmit without fixing issues
- Try to sneak past the same violation
- Create new account to avoid rejection

---

## Automated submission with Fastlane

Use [Fastlane](https://fastlane.tools/) to automate submissions and reduce human error.

### Setup

```bash
# Install
brew install fastlane

# Initialize in project
cd your-app
fastlane init
```

### Fastfile for iOS

```ruby
default_platform(:ios)

platform :ios do
  desc "Submit to App Store"
  lane :release do
    # Increment build number
    increment_build_number

    # Build
    build_app(
      scheme: "YourApp",
      export_method: "app-store"
    )

    # Upload to App Store Connect
    upload_to_app_store(
      skip_screenshots: true,
      skip_metadata: false,
      submit_for_review: false,  # Set true for auto-submit
      automatic_release: false
    )
  end

  desc "Submit to TestFlight"
  lane :beta do
    increment_build_number
    build_app(scheme: "YourApp")
    upload_to_testflight
  end
end
```

### Fastfile for Android

```ruby
default_platform(:android)

platform :android do
  desc "Deploy to Google Play"
  lane :release do
    gradle(task: "clean assembleRelease")
    upload_to_play_store(
      track: "production",
      release_status: "draft"  # Review before going live
    )
  end

  desc "Deploy to internal testing"
  lane :beta do
    gradle(task: "clean assembleRelease")
    upload_to_play_store(track: "internal")
  end
end
```

### CI/CD integration

```yaml
# GitHub Actions example
name: Release iOS

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.0'
      - run: bundle install
      - run: bundle exec fastlane release
        env:
          APP_STORE_CONNECT_API_KEY: ${{ secrets.APP_STORE_KEY }}
```

---

## Bulk testing strategy

### Before submission testing matrix

| Device | OS Version | Network | Test |
|--------|------------|---------|------|
| iPhone 15 Pro | iOS 18 | WiFi | Full flow |
| iPhone 12 | iOS 17 | LTE | Full flow |
| iPhone 11 | iOS 16 | IPv6 | Launch + core |
| Pixel 7 | Android 14 | WiFi | Full flow |
| Samsung A52 | Android 12 | LTE | Full flow |

### Automated testing

```bash
# iOS UI testing
xcodebuild test -scheme YourApp -destination 'platform=iOS Simulator,name=iPhone 15'

# Android UI testing
./gradlew connectedAndroidTest
```

### TestFlight strategy

1. Internal testing (team): 5-10 testers, catch obvious bugs
2. External testing (beta): 20-50 testers, catch edge cases
3. Wait for 48 hours of feedback before App Store submission

---

## Recovery from rejection

### Single rejection

1. Read Resolution Center message carefully
2. Fix the specific issue mentioned
3. Add explanation in "Notes for reviewer" about what you fixed
4. Resubmit

### Multiple rejections (same issue)

1. Request phone call with App Review
2. Explain your implementation
3. Ask for specific guidance
4. Document everything

### Account warning

1. Stop all submissions immediately
2. Audit all apps for violations
3. Fix issues proactively
4. Consider removing risky apps voluntarily

---

## Sources

- [BetaDrop - Top 10 iOS App Rejection Reasons 2026](https://betadrop.app/blog/ios-app-rejection-reasons-2026)
- [Adapty - App Store Rejection Reasons](https://adapty.io/blog/app-store-rejection/)
- [OneMobile - Common App Store Rejections](https://onemobile.ai/common-app-store-rejections-and-how-to-avoid-them/)
- [Google Play Enforcement Process](https://support.google.com/googleplay/android-developer/answer/9899234)
- [Fastlane Documentation](https://docs.fastlane.tools/)

---

Created: 2026-01-21
