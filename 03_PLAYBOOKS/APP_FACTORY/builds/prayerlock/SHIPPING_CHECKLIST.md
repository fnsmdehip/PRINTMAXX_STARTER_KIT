# PrayerLock - Shipping Checklist

**Current Status:** 85% complete
**Blockers:** Icons, RevenueCat integration, App Store submission
**Time to Ship:** 8-12 hours

---

## What's Done

- [x] Core prayer timer functionality
- [x] Phone locking mechanism
- [x] Basic UI/UX
- [x] Onboarding flow
- [x] Settings screens
- [x] Prayer streak tracking
- [x] Notification system

---

## What's Blocking Shipment

### BLOCKER 1: App Icons (2 hours)

**Current:** Placeholder icons or generic design
**Needed:** Professional app icon + splash screen

**Steps:**
1. Generate with Gemini AI (use prompts from `APP_FACTORY/assets/LOCK_APPS_ICON_PROMPTS_V3.md`)
2. Prompt:
   ```
   3D app icon for PrayerLock, Christian faith theme, gradient purple to gold,
   praying hands silhouette with subtle glow, rounded square iOS style,
   depth and dimension, 1024x1024, professional finish
   ```
3. Download 1024x1024 PNG
4. Generate all required sizes:
   ```bash
   # Install imagemagick if needed
   brew install imagemagick

   # Generate all iOS icon sizes
   cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/03_PLAYBOOKS/APP_FACTORY/builds/prayerlock/assets

   # From 1024x1024 source, create all sizes
   for size in 20 29 40 58 60 76 80 87 120 152 167 180 1024; do
     convert icon-1024.png -resize ${size}x${size} icon-${size}.png
   done
   ```
5. Update `app.json`:
   ```json
   {
     "expo": {
       "icon": "./assets/icon.png",
       "splash": {
         "image": "./assets/splash.png"
       }
     }
   }
   ```

### BLOCKER 2: RevenueCat Integration (3-4 hours)

**Current:** No monetization
**Needed:** Hard paywall with 3-day free trial

**Why RevenueCat:**
- Handles iOS and Android subscriptions
- Server-side receipt validation
- Analytics dashboard
- Webhook integrations

**Steps:**

**1. Create RevenueCat Account (15 min)**
1. Go to revenuecat.com
2. Sign up with email
3. Create new project: "PrayerLock"
4. Get API key from Settings

**2. Install RevenueCat SDK (10 min)**
```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/03_PLAYBOOKS/APP_FACTORY/builds/prayerlock

npx expo install react-native-purchases
```

**3. Copy Implementation Code (2 hours)**

Use code from biomaxx-sdk54 (already working):

**File 1: `services/subscriptionService.ts`**
```typescript
// Copy from /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/03_PLAYBOOKS/APP_FACTORY/builds/biomaxx-sdk54/services/subscriptionService.ts
```

**File 2: `components/Paywall.tsx`**
```typescript
// Copy from biomaxx-sdk54/components/Paywall.tsx
// Customize copy for PrayerLock:
// - "Unlock unlimited prayer tracking"
// - "Join 847 people who pray consistently"
// - "3-day free trial, cancel anytime"
```

**File 3: `hooks/usePremiumGate.ts`**
```typescript
// Copy from biomaxx-sdk54/hooks/usePremiumGate.ts
```

**4. Configure Products (30 min)**

In RevenueCat dashboard:
1. Products → New Product
2. Monthly: $4.99/month (identifier: `prayerlock_monthly`)
3. Annual: $39.99/year (identifier: `prayerlock_annual`)
4. Set up 3-day free trial on both

In App Store Connect (later):
1. In-App Purchases → Create subscriptions
2. Same identifiers as RevenueCat
3. Same pricing

**5. Add Paywall Trigger (30 min)**

Show paywall after:
- [ ] 7 days of use (free trial)
- [ ] 20 prayer sessions completed
- [ ] Trying to access premium features (custom prayers, themes, etc.)

```typescript
// In your main app component
import { usePremiumGate } from './hooks/usePremiumGate';

function PrayerScreen() {
  const { isPremium, showPaywall } = usePremiumGate();

  useEffect(() => {
    // Show paywall after 7 days
    const installDate = await AsyncStorage.getItem('installDate');
    if (!installDate) {
      await AsyncStorage.setItem('installDate', new Date().toISOString());
    } else {
      const daysSinceInstall = daysSince(new Date(installDate));
      if (daysSinceInstall >= 7 && !isPremium) {
        showPaywall();
      }
    }
  }, []);

  // Rest of component
}
```

**6. Test Purchases (30 min)**
1. Build app to simulator
2. Test paywall shows correctly
3. Test purchase flow (sandbox mode)
4. Test restore purchases
5. Test free trial countdown

### BLOCKER 3: App Store Submission (2-3 hours)

**Prerequisites:**
- [ ] Apple Developer account ($99/year)
- [ ] App icons ready
- [ ] Screenshots ready (6 sizes required)
- [ ] Privacy policy page live
- [ ] App Store Connect project created

**Steps:**

**1. Apple Developer Account (5 min)**
1. developer.apple.com → Sign up
2. Pay $99/year
3. Wait for approval (usually instant, can take 24 hours)

**2. Create App in App Store Connect (30 min)**
1. appstoreconnect.apple.com
2. My Apps → + → New App
3. Fill out:
   - Name: "PrayerLock - Focus Timer"
   - Primary Language: English
   - Bundle ID: `com.printmaxx.prayerlock` (must match app.json)
   - SKU: `prayerlock`
4. Set up In-App Purchases (subscriptions)
5. Add pricing and availability

**3. Generate Screenshots (1 hour)**

**Required sizes:**
- 6.5" iPhone (1242 x 2688) - iPhone 14 Pro Max
- 5.5" iPhone (1242 x 2208) - iPhone 8 Plus
- 12.9" iPad Pro (2048 x 2732)

**How to generate:**
1. Launch app in iOS Simulator
2. Run through key screens:
   - Onboarding (first screen)
   - Prayer timer active (hero screen)
   - Streak tracking (social proof)
   - Settings (customization)
3. Take screenshots (Cmd+S in Simulator)
4. Use Screenshots.pro or similar to add device frames + text overlays

**Text overlays for screenshots:**
- "Lock your phone until you pray"
- "Track your prayer streak"
- "Join 847 consistent pray-ers"
- "3-day free trial"

**4. Upload Build (30 min)**

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/03_PLAYBOOKS/APP_FACTORY/builds/prayerlock

# Update version in app.json
# version: "1.0.0"

# Build for iOS
eas build --platform ios

# Wait for build to complete (15-30 min)
# Download IPA from Expo dashboard
# Upload to App Store Connect via Transporter app
```

**5. Submit for Review (30 min)**

In App Store Connect:
1. Add screenshots
2. Write description (use listing copy from competitive analysis)
3. Add keywords: prayer, faith, christian, accountability, timer, lock, focus
4. Set age rating: 4+
5. Add privacy policy URL
6. Add support URL
7. Submit for review

**Review time:** 24-72 hours typically

---

## Pre-Launch Quality Assurance

### Functional Testing (1 hour)

**Critical flows to test:**
- [ ] Onboarding completes without crashes
- [ ] Prayer timer starts and counts correctly
- [ ] Phone locks during prayer time
- [ ] Emergency calls still work when locked
- [ ] Streak tracking increments correctly
- [ ] Notifications fire at set times
- [ ] Settings save properly
- [ ] Paywall shows after trigger
- [ ] Purchase flow completes (sandbox)
- [ ] Restore purchases works

**Test on devices:**
- [ ] iPhone 14 Pro Max (6.5" - largest)
- [ ] iPhone SE (4.7" - smallest)
- [ ] iPad Pro (tablet view)

### Copy Review (30 min)

**Check all in-app copy:**
- [ ] No em dashes
- [ ] No AI vocabulary (leverage, comprehensive, etc.)
- [ ] Consistent voice (@pipelineabuser style)
- [ ] Clear value props
- [ ] No typos

### Privacy Compliance (30 min)

**Required disclosures:**
- [ ] Privacy policy page created
- [ ] What data is collected (prayer times, streaks)
- [ ] What data is NOT collected (prayer content)
- [ ] Third-party services (RevenueCat, Firebase)
- [ ] Right to delete data

**Create privacy policy:**
1. Use generator: privacypolicies.com
2. Customize for PrayerLock
3. Host on printmaxx-site: `/privacy/prayerlock`
4. Add link to app and App Store listing

---

## Launch Day Checklist

**24 hours before launch:**
- [ ] Final build uploaded to App Store
- [ ] Screenshots finalized
- [ ] Description optimized for ASO
- [ ] RevenueCat webhooks tested
- [ ] Analytics connected (Firebase, Mixpanel, or RevenueCat)
- [ ] Support email created: support@printmaxx.com or similar
- [ ] Landing page live: printmaxx.com/prayerlock

**Launch day:**
- [ ] App goes live (usually 24-72 hours after approval)
- [ ] Post launch announcement (all social channels)
- [ ] Share in relevant communities (r/Christianity, faith subreddits)
- [ ] Email list announcement (if you have one)
- [ ] Monitor for crashes (RevenueCat dashboard, crash reports)

**First week:**
- [ ] Reply to all reviews within 24 hours
- [ ] Track metrics daily (downloads, trials, conversions)
- [ ] Monitor support emails
- [ ] Fix any critical bugs immediately
- [ ] Gather testimonials from early users

---

## Post-Launch Optimization

### Week 1: Monitor & Fix

**Metrics to track:**
| Metric | Target | Tool |
|--------|--------|------|
| Downloads | 50+ | App Store Connect |
| Trial starts | 20+ (40% of downloads) | RevenueCat |
| Trial → Paid | 3+ (15% of trials) | RevenueCat |
| Daily Active Users | 30+ | RevenueCat or Firebase |
| Crash-free rate | >99% | App Store Connect |

**If conversion < 15%:**
- Test different paywall copy
- Shorten trial period (3 days → 7 days)
- Adjust pricing ($4.99 → $2.99)

### Week 2-4: Iterate

**A/B test (using RevenueCat Experiments):**
- [ ] Annual-first vs monthly-first pricing display
- [ ] 3-day vs 7-day free trial
- [ ] Paywall timing (7 days vs 14 days)
- [ ] Price points ($4.99 vs $2.99 vs $6.99)

**Add features based on feedback:**
- [ ] Custom prayer templates
- [ ] Group accountability
- [ ] Prayer journal
- [ ] Bible verse integration
- [ ] Community challenges

---

## Revenue Projections

### Conservative (Month 1)

| Metric | Value |
|--------|-------|
| Downloads | 500 |
| Trial starts (40%) | 200 |
| Trial → Paid (15%) | 30 |
| Monthly subs | 20 ($4.99) |
| Annual subs | 10 ($39.99) |
| **MRR** | **$133** |
| **Annual revenue** | **$1,596** |

### Moderate (Month 3)

| Metric | Value |
|--------|-------|
| Downloads | 2,000 |
| Trial starts (45%) | 900 |
| Trial → Paid (20%) | 180 |
| Monthly subs | 100 ($4.99) |
| Annual subs | 80 ($39.99) |
| **MRR** | **$766** |
| **Annual revenue** | **$9,192** |

### Aggressive (Month 6)

| Metric | Value |
|--------|-------|
| Downloads | 5,000 |
| Trial starts (50%) | 2,500 |
| Trial → Paid (25%) | 625 |
| Monthly subs | 400 ($4.99) |
| Annual subs | 225 ($39.99) |
| **MRR** | **$2,746** |
| **Annual revenue** | **$32,952** |

---

## Risks & Mitigations

### Risk 1: App Store Rejection

**Common reasons:**
- Incomplete metadata
- Privacy policy issues
- Crashes during review
- In-app purchase issues

**Mitigation:**
- Test thoroughly before submission
- Clear privacy policy
- Detailed app description
- Test all purchase flows

### Risk 2: Low Conversion Rate

**If trial → paid < 10%:**
- Paywall copy needs work
- Pricing too high
- Not enough value demonstrated
- Trial period wrong length

**Fix:**
- A/B test pricing
- Improve in-app value props
- Add social proof
- Test 7-day trial

### Risk 3: High Churn

**If monthly churn > 10%:**
- App not providing enough value
- Users find workarounds
- Bugs or crashes
- Better alternatives exist

**Fix:**
- Add features users request
- Improve onboarding
- Fix bugs immediately
- Build community (Discord/Telegram)

---

## Next Apps After PrayerLock

**Once PrayerLock is live and generating revenue:**

1. **WalkToUnlock** (fitness niche)
   - Similar locking mechanism
   - Track steps, not prayers
   - Copy 80% of code from PrayerLock
   - Time to ship: 1 week

2. **StudyLock** (student niche)
   - Lock phone during study sessions
   - Pomodoro timer built-in
   - Copy 80% of code
   - Time to ship: 1 week

3. **[Niche]Lock** (template)
   - Pick any behavior to enforce
   - Copy 90% of code
   - Customize for niche
   - Time to ship: 3-5 days

**Lock App Portfolio Strategy:**
- 10 niche-specific apps
- All using same codebase
- Each targeting different audience
- Revenue compounds across portfolio

---

## Time Breakdown

| Task | Time |
|------|------|
| Generate app icons | 2 hrs |
| RevenueCat integration | 3-4 hrs |
| Testing & QA | 1 hr |
| App Store submission prep | 2 hrs |
| Build & upload | 1 hr |
| Submit for review | 30 min |
| **Total** | **9.5-10.5 hrs** |

**Then wait:** 24-72 hours for Apple review

---

**Status:** 85% complete. 8-12 hours of work to ship. Primary blocker: RevenueCat integration. Use biomaxx code as template.
