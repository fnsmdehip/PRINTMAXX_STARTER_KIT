# APP FACTORY - Manual Setup Handoff Checklist

**Generated:** 2026-01-21
**Status:** Ready for human setup

---

## App Portfolio Summary

| App | Niche | Status | Files | Key Feature |
|-----|-------|--------|-------|-------------|
| **StepUnlock** | Fitness | Ready | 11 screens | Blocks apps until step goal |
| **DailyAnchor** | Journaling | Ready | 10 screens | Daily affirmation journal |
| **DevotionFlow** | Faith | Ready | 15 screens | Guided devotional app |
| **FocusPrayer** | Faith | Ready | 11 screens | Prayer timer with app blocking |
| **LearnLock** | Education | Ready | 8 screens | Study time tracking |
| **PelvicPro** | Women's Health | Ready | 19 screens | Pelvic floor exercises |
| **PromptVault** | Productivity | Structure | Basic | AI prompt library |
| **GlowMaxx** | Looksmaxxing | Building | In progress | Mewing, debloating, skincare |

---

## Step 1: Apple Developer Account Setup

### Required
- [ ] Apple Developer Program membership ($99/year)
- [ ] Apple Developer account enrolled
- [ ] App Store Connect access configured

### Create App IDs (one per app)
- [ ] `com.stepunlock.app`
- [ ] `com.dailyanchor.app`
- [ ] `com.devotionflow.app`
- [ ] `com.focusprayer.app`
- [ ] `com.learnlock.app`
- [ ] `com.pelvicpro.app`
- [ ] `com.glowmaxx.app`

### Create App Store Connect Records
For each app:
- [ ] Create new app in App Store Connect
- [ ] Fill basic info (name, subtitle, description)
- [ ] Upload screenshots (use simulator + screenshot tool)
- [ ] Set age rating
- [ ] Set pricing/availability

---

## Step 2: RevenueCat Setup

### Account Setup
- [ ] Create RevenueCat account: https://app.revenuecat.com
- [ ] Create new project for PRINTMAXX apps

### For Each App, Create:
- [ ] New app in RevenueCat
- [ ] Connect to App Store Connect
- [ ] Create products:
  - `monthly_premium` - $9.99/mo
  - `annual_premium` - $49.99/yr (17% discount)
- [ ] Create offerings:
  - Default offering with monthly + annual
  - Paywall A/B test variants (if doing tests)
- [ ] Copy API keys to each app's config

### API Keys Location
Update these files with your RevenueCat public API key:
```
stepunlock/src/services/subscriptionService.ts
dailyanchor/src/services/subscriptionService.ts
devotionflow/src/services/subscriptionService.ts
focusprayer/src/services/subscriptionService.ts
learnlock/src/services/subscriptionService.ts
pelvicpro/src/services/subscriptionService.ts
glowmaxx/src/services/subscriptionService.ts
```

Look for: `REVENUECAT_PUBLIC_KEY` or similar placeholder.

---

## Step 3: Stripe Setup (Optional - Web Checkout)

If using Stripe for web-based checkout or supplementary payments:

- [ ] Create Stripe account: https://stripe.com
- [ ] Complete business verification
- [ ] Create products matching RevenueCat products
- [ ] Set up webhook to RevenueCat (for cross-platform sync)

---

## Step 4: Affiliate Links Setup

### Amazon Associates
- [ ] Join Amazon Associates: https://affiliate-program.amazon.com
- [ ] Get tracking ID
- [ ] Create links for recommended products

### ShareASale
- [ ] Join ShareASale: https://www.shareasale.com
- [ ] Apply to relevant merchant programs:
  - Christianbook.com (faith apps)
  - DaySpring (journals)
  - Health/fitness merchants

### App-Specific Affiliate Programs

**Faith Apps (DevotionFlow, FocusPrayer):**
- [ ] Hallow: https://hallow.com/affiliate
- [ ] She Reads Truth: Contact directly
- [ ] Logos/Faithlife: https://faithlife.com/affiliate

**Fitness Apps (StepUnlock, PelvicPro):**
- [ ] Amazon (fitness gear)
- [ ] Athletic supplements merchants

**Looksmaxxing (GlowMaxx):**
- [ ] Skincare affiliate programs
- [ ] Jade roller / gua sha products
- [ ] Clean water filter affiliate programs

### Update Affiliate Links in Code
Search for `AFFILIATE_LINK` placeholders in each app.

---

## Step 5: EAS Build Configuration

### One-Time Setup
```bash
# Install EAS CLI
npm install -g eas-cli

# Login
eas login
```

### For Each App
```bash
cd builds/[appname]

# Initialize EAS
eas build:configure

# Update eas.json with your Apple credentials
# Update app.json with your bundle ID

# Build for iOS
eas build --platform ios --profile production
```

### Update app.json Files
Each app needs real values for:
```json
{
  "expo": {
    "extra": {
      "eas": {
        "projectId": "YOUR_ACTUAL_EAS_PROJECT_ID"
      }
    },
    "ios": {
      "bundleIdentifier": "com.yourcompany.appname"
    }
  }
}
```

---

## Step 6: App Store Submission

### For Each App, Complete:

**1. Screenshots (required sizes)**
- [ ] 6.7" (iPhone 15 Pro Max): 1290 x 2796
- [ ] 6.5" (iPhone 11 Pro Max): 1242 x 2688
- [ ] 5.5" (iPhone 8 Plus): 1242 x 2208
- [ ] iPad Pro 12.9": 2048 x 2732

**2. App Store Listing**
- [ ] App name (30 char max)
- [ ] Subtitle (30 char max)
- [ ] Description (4000 char max)
- [ ] Keywords (100 char max, comma separated)
- [ ] Support URL
- [ ] Privacy policy URL
- [ ] Categories (primary + secondary)

**3. Review Information**
- [ ] Demo account (if needed)
- [ ] Contact info
- [ ] Notes for reviewer (explain any special features)

**4. Pricing & Availability**
- [ ] Set base country pricing
- [ ] Configure auto-renewable subscription prices
- [ ] Set availability (worldwide or specific)

---

## Step 7: Post-Launch Setup

### Analytics
- [ ] Verify RevenueCat analytics working
- [ ] Set up Mixpanel or Amplitude (optional)
- [ ] Configure App Store Connect analytics

### ASO Optimization
- [ ] Monitor keyword rankings
- [ ] Update keywords based on performance
- [ ] Request reviews from active users

### Marketing Launch
Marketing materials created in:
- `builds/[app]/marketing/cold_outreach.md`
- `builds/[app]/marketing/lead_gen.md`
- `builds/[app]/marketing/ugc_brief.md`
- `builds/[app]/marketing/affiliate_strategy.md`

---

## App-Specific Notes

### StepUnlock
- Requires HealthKit permission for step counting
- Test step tracking on real device
- Emergency unlock resets streak (intended)

### DevotionFlow
- 365 devotions included in data file
- Notification scheduling for daily reminders
- Journal entries stored locally

### FocusPrayer
- Similar to StepUnlock but for prayer
- Scripture reading component included
- Guided prayer timer

### PelvicPro
- Exercise animations/illustrations needed
- Shop tab ready for affiliate products
- Women's health claims require careful review

### GlowMaxx (In Development)
- Mewing timer with progress tracking
- Before/after photo comparison
- Debloat tracking (water, sodium, sleep)
- Gender-specific routines

---

## Files to Update Before Build

| File Pattern | Update Needed |
|-------------|---------------|
| `*/app.json` | Bundle ID, project ID, version |
| `*/src/services/subscriptionService.ts` | RevenueCat API key |
| `*/src/utils/constants.ts` | Affiliate links, URLs |
| `*/app/privacy-policy.tsx` | Your company/privacy info |
| `*/app/terms.tsx` | Your terms of service |

---

## Quick Commands Reference

```bash
# Start any app in simulator
cd builds/[appname]
npx expo start --ios

# Build for TestFlight
eas build --platform ios --profile preview

# Build for App Store
eas build --platform ios --profile production

# Submit to App Store
eas submit --platform ios
```

---

## Support Resources

- Expo docs: https://docs.expo.dev
- RevenueCat docs: https://docs.revenuecat.com
- App Store Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
- EAS Build docs: https://docs.expo.dev/build/introduction/

---

## Estimated Time to Complete

| Task | Time |
|------|------|
| Apple Developer setup | 1-2 hours |
| RevenueCat setup (all apps) | 2-3 hours |
| Affiliate programs | 1-2 hours |
| EAS build configuration | 1 hour per app |
| App Store listings | 1-2 hours per app |
| First submission | 30 min per app |
| Review wait time | 24-72 hours typically |

**Total estimated setup time:** 15-25 hours

---

## Priority Order for Submission

1. **StepUnlock** - Most complete, fitness niche proven
2. **DevotionFlow** - Faith niche, strong retention
3. **FocusPrayer** - Faith niche, app blocking angle
4. **DailyAnchor** - Journaling, broad appeal
5. **PelvicPro** - Women's health, lucrative but needs care
6. **LearnLock** - Education niche
7. **GlowMaxx** - Looksmaxxing (complete build first)

---

Good luck with the launch!
