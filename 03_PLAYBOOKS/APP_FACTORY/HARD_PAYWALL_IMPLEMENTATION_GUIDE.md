# Hard Paywall Implementation Guide

**Created:** 2026-02-01
**Source Alpha:** ALPHA465 (8x revenue), ALPHA032 (animated paywall 2.9x), ALPHA035 (+17% personalization), ALPHA034 (44.1% annual retention)
**Apps:** biomaxx, PrayerLock, WalkToUnlock, StudyLock

---

## Executive Summary

Hard paywalls during onboarding generate **8x more revenue** than freemium models. 80% of users who complete onboarding convert to paid during the trial. The key: excellent first-run experience combined with strategic paywall placement.

**The Formula:**
```
Excellent Onboarding (3-4 screens)
→ Value Demonstration
→ Paywall (animated, personalized, annual highlighted)
→ 7-day trial
→ Post-trial onboarding
= 8x revenue vs freemium
```

---

## Core Principles

### 1. No Free Tier
Users on free tiers never hit the 14-day usage threshold needed for retention. They churn without experiencing value. Hard paywall forces commitment, increases perceived value, and filters for serious users.

### 2. Trial Placement
Paywall appears at the END of onboarding, not the beginning. Users must:
- See the app's value proposition (screens 1-4)
- Personalize their experience (name, goals)
- Understand the problem being solved
- THEN hit paywall with context

### 3. Annual Pricing Highlighted
Annual plans have 44.1% retention vs 17% for monthly. Present annual as the default choice with monthly as fallback. Use savings messaging ("$2.99/mo vs $9.99/mo - save 70%").

### 4. Animated Paywall
Static paywalls convert at 1x. Animated paywalls (smooth transitions, progress indicators, benefit reveals) convert at 2.9x. Worth the extra development time.

---

## Per-App Implementation

### biomaxx (Supplement Tracker)

**Onboarding Flow (6 screens):**

**Screen 1: Personalized Welcome**
```
[User's First Name], welcome to BioMaxx

Track what works. Drop what doesn't.
Your $2,400/yr supplement stack deserves data.

[Continue Button]
```
- Use name personalization (+17% conversion per ALPHA035)
- Consequence-first hook ($2,400/yr number anchors value)
- Simple, clean design
- No skip option

**Screen 2: Protocol Selection**
```
What are you optimizing for?

[Selectable Cards]
☀️ Energy & Focus
💪 Muscle & Recovery
🧘 Sleep & Stress
🧠 Cognition & Memory
❤️ Longevity & Vitality

Select all that apply

[Continue Button]
```
- Multi-select allowed (most users select 2-3)
- Builds engagement before paywall
- Data used to personalize dashboard

**Screen 3: Stack Size**
```
How many supplements do you take daily?

[Slider: 1 - 20+]
Currently taking: [X] supplements

That's $[calculated]/month
Let's figure out which ones are worth it.

[Continue Button]
```
- Interactive slider (engagement)
- Real-time cost calculation based on average $12/supplement
- Anchors the problem ("worth it?")

**Screen 4: Problem Framing**
```
Here's the truth:

Half your stack might be doing nothing.
You're spending $2,400/year blind.

BioMaxx gives you data.
Track. Correlate. Optimize.

[See How It Works Button]
```
- No engagement required (just read)
- Sets up the value proposition
- "See How It Works" button leads to paywall

**Screen 5: Animated Paywall** ⭐ CRITICAL
```
[Top: Progress bar showing "Step 5 of 6"]

[Animated benefit cards sliding in one by one]

📊 Track unlimited supplements
📈 Automatic correlation analysis
🔔 Smart reminder system
📱 Multi-protocol stacking
📤 Export your data anytime

[Pricing Cards - Annual Highlighted]

┌─────────────────────┐  ┌─────────────────────┐
│   MOST POPULAR      │  │                     │
│                     │  │                     │
│   Annual            │  │   Monthly           │
│   $35.99/year       │  │   $9.99/month       │
│   ($2.99/month)     │  │                     │
│                     │  │                     │
│   Save 70%          │  │                     │
│   [START 7-DAY      │  │   [START 7-DAY      │
│    FREE TRIAL]      │  │    FREE TRIAL]      │
└─────────────────────┘  └─────────────────────┘

✓ Cancel anytime during trial
✓ Full access for 7 days
✓ No charge until [Date]

[Small text: Restore Purchase]
```

**Animation Sequence:**
1. Screen fades in with benefit cards sliding up (0.3s delay each)
2. Pricing cards fade in after benefits (0.5s delay)
3. "MOST POPULAR" badge pulses gently
4. Annual card has subtle glow/highlight
5. Total animation: 2 seconds

**Design Notes:**
- Annual card 20% larger than monthly
- Green checkmark animation on "Save 70%"
- NO prominent "skip" or "maybe later" button
- Restore Purchase link small, bottom left
- iOS: Use StoreKit 2 for smooth purchase flow
- Android: Google Play Billing Library 5.0+

**Screen 6: Post-Purchase Onboarding**
```
[Checkmark animation]

You're all set!

Let's build your first stack.

[Add Supplement Button]
```
- Immediate value delivery
- Guides into first action (add supplement)
- Sets up daily reminder

---

### PrayerLock (Prayer Discipline App)

**Onboarding Flow (6 screens):**

**Screen 1: Personalized Welcome**
```
Welcome, [First Name]

Phone lock until you pray.
Turn distraction into discipline.

[Continue]
```
- Name personalization
- Two-line value prop
- Clean, minimal design (aligns with faith aesthetic)

**Screen 2: Prayer Goal**
```
How long do you want to pray each day?

[Selection Cards]
🕐 5 minutes  - Quick devotional
🕐 10 minutes - Standard practice
🕐 15 minutes - Deep focus
🕐 20+ minutes - Extended prayer

[Continue]
```
- Preset options (reduces decision fatigue)
- Descriptive labels (not just numbers)
- Default: 10 minutes highlighted

**Screen 3: Lock Settings**
```
When should your phone lock?

[Toggle Options]
☀️ Morning (6 AM - 9 AM)
🌙 Evening (8 PM - 10 PM)
⏰ Custom time

[Continue]
```
- Common patterns shown first
- Custom option for flexibility
- Sets up the core mechanic

**Screen 4: Problem Framing**
```
Average phone pickups: 96/day
Average prayer time: 4 minutes/day

Your phone owns your attention.
Take it back.

[See How PrayerLock Works]
```
- Specific numbers (96 pickups, 4 minutes)
- Contrast creates urgency
- Leads to paywall

**Screen 5: Animated Paywall**
```
[Progress: Step 5 of 6]

[Benefit cards]
📿 Daily prayer streaks
🔒 Phone lock enforcement
📊 Progress tracking
🙏 Devotional library
☁️ Cloud sync across devices

[Pricing - Annual Highlighted]

┌─────────────────────┐  ┌─────────────────────┐
│   MOST POPULAR      │  │                     │
│   Annual            │  │   Monthly           │
│   $29.99/year       │  │   $4.99/month       │
│   ($2.49/month)     │  │                     │
│   Save 50%          │  │                     │
│   [START 7-DAY      │  │   [START 7-DAY      │
│    FREE TRIAL]      │  │    FREE TRIAL]      │
└─────────────────────┘  └─────────────────────┘

✓ Full access for 7 days
✓ Cancel anytime
✓ No charge until [Date]
```

**Animation:**
- Benefit cards slide in from right
- Pricing cards fade in
- Annual card subtle pulse
- 2-second total animation

**Screen 6: Post-Purchase**
```
[Cross animation]

Your journey begins now.

Set your first prayer time.

[Choose Time Button]
```
- Faith-appropriate imagery (cross, not checkmark)
- Immediate action prompt
- Guides into core feature

---

### WalkToUnlock (Fitness Step Goal)

**Onboarding Flow (6 screens):**

**Screen 1: Personalized Welcome**
```
Hey [First Name] 👋

Your phone stays locked until you walk.
No steps = no scroll.

[Let's Go]
```
- Casual, energetic tone
- Clear mechanic explanation
- Action-oriented CTA

**Screen 2: Step Goal**
```
Daily step goal?

[Selection Cards with Icons]
🚶 3,000 steps  - Getting started
🏃 5,000 steps  - Active lifestyle
🔥 7,500 steps  - Health optimized
💪 10,000 steps - Athlete mode

[Continue]
```
- Icons add personality
- Descriptive labels frame identity
- Default: 7,500 (science-backed for mortality reduction)

**Screen 3: Lock Schedule**
```
When does the lock activate?

[Toggle Options]
📱 All day (hardcore mode)
🌅 Mornings only
🌆 Evenings only
⚙️ Custom schedule

[Continue]
```
- "Hardcore mode" gamifies the challenge
- Flexibility prevents abandonment
- Sets expectations

**Screen 4: Problem Framing**
```
Average daily steps: 3,000
Recommended: 7,500

That gap = 20 lbs gained per year.

Friction is the feature.

[See How It Works]
```
- Specific consequence (20 lbs/year)
- Data from JAMA 2019 study
- "Friction is the feature" = contrarian positioning

**Screen 5: Animated Paywall**
```
[Progress: Step 5 of 6]

[Benefit cards]
👟 Automatic step tracking
🔒 Progressive unlock system
📊 Weekly progress reports
🏆 Streak challenges
💪 Health integration

[Pricing - Annual Highlighted]

┌─────────────────────┐  ┌─────────────────────┐
│   MOST POPULAR      │  │                     │
│   Annual            │  │   Monthly           │
│   $24.99/year       │  │   $3.99/month       │
│   ($2.08/month)     │  │                     │
│   Save 48%          │  │                     │
│   [START 7-DAY      │  │   [START 7-DAY      │
│    FREE TRIAL]      │  │    FREE TRIAL]      │
└─────────────────────┘  └─────────────────────┘

✓ 7 days free
✓ Cancel anytime
✓ No charge until [Date]
```

**Animation:**
- Benefits slide up from bottom
- Pricing cards zoom in slightly
- Annual card glow effect
- 2-second animation

**Screen 6: Post-Purchase**
```
[Shoe icon animation]

Let's get moving.

Take your first 100 steps.

[Start Walking Button]
```
- Immediate activation
- Small first step (100 steps = 1 minute walk)
- Gamified

---

### StudyLock (Study Discipline App)

**Onboarding Flow (6 screens):**

**Screen 1: Personalized Welcome**
```
Welcome, [First Name]

Phone locked until you study.
Focus earned, not given.

[Start]
```
- Academic/professional tone
- Clear value prop
- Name personalization

**Screen 2: Study Goal**
```
Daily study time?

[Selection Cards]
📚 30 minutes  - Quick review
📖 60 minutes  - Standard session
🎓 90 minutes  - Deep work
🔬 120+ minutes - Grind mode

[Continue]
```
- Time-based goals
- Descriptive labels
- Default: 60 minutes

**Screen 3: Lock Settings**
```
When should your phone lock?

[Toggle Options]
🌅 Morning study block
🌆 Evening study block
📅 Exam prep mode (all day)
⚙️ Custom schedule

[Continue]
```
- "Exam prep mode" for high-stakes periods
- Flexibility for different routines

**Screen 4: Problem Framing**
```
Distractions kill focus.

Average deep work session: 12 minutes.
Potential with focus: 90+ minutes.

Your phone is the leash.

[See How StudyLock Works]
```
- 12 vs 90 minute contrast
- "Phone is the leash" = powerful metaphor
- Sets up paywall

**Screen 5: Animated Paywall**
```
[Progress: Step 5 of 6]

[Benefit cards]
⏱️ Pomodoro timer built-in
🔒 App blocking during sessions
📊 Study time analytics
🎯 Subject tracking
☁️ Cross-device sync

[Pricing - Annual Highlighted]

┌─────────────────────┐  ┌─────────────────────┐
│   BEST VALUE        │  │                     │
│   Annual            │  │   Monthly           │
│   $29.99/year       │  │   $4.99/month       │
│   ($2.49/month)     │  │                     │
│   Save 50%          │  │                     │
│   [START 7-DAY      │  │   [START 7-DAY      │
│    FREE TRIAL]      │  │    FREE TRIAL]      │
└─────────────────────┘  └─────────────────────┘

✓ Full access for 7 days
✓ No charge until [Date]
✓ Cancel anytime
```

**Animation:**
- Benefit cards fade in sequentially
- Pricing cards slide in from sides
- Annual card highlight pulse
- 2-second total

**Screen 6: Post-Purchase**
```
[Book icon animation]

Time to focus.

Start your first study session.

[Begin Studying Button]
```
- Immediate activation
- Guides into first session
- Clean, minimal

---

## RevenueCat Configuration

### Setup Steps

**1. Create RevenueCat Account**
- URL: https://app.revenuecat.com/signup
- Free tier: up to $2,500 MRR
- Then 1% of revenue + $0.01 per transaction

**2. Create Projects (One Per App)**
```
Project 1: biomaxx
Project 2: PrayerLock
Project 3: WalkToUnlock
Project 4: StudyLock
```

**3. Configure Products for Each App**

**biomaxx:**
```
Product ID: biomaxx_annual
Price: $35.99/year
Free Trial: 7 days
Display Name: "Annual Plan"
Description: "Full access to all features"

Product ID: biomaxx_monthly
Price: $9.99/month
Free Trial: 7 days
Display Name: "Monthly Plan"
Description: "Full access, billed monthly"
```

**PrayerLock:**
```
Product ID: prayerlock_annual
Price: $29.99/year
Free Trial: 7 days
Display Name: "Annual Plan"
Description: "Full prayer toolkit"

Product ID: prayerlock_monthly
Price: $4.99/month
Free Trial: 7 days
Display Name: "Monthly Plan"
Description: "Full access, billed monthly"
```

**WalkToUnlock:**
```
Product ID: walktounlock_annual
Price: $24.99/year
Free Trial: 7 days
Display Name: "Annual Plan"
Description: "Unlimited step tracking"

Product ID: walktounlock_monthly
Price: $3.99/month
Free Trial: 7 days
Display Name: "Monthly Plan"
Description: "Billed monthly"
```

**StudyLock:**
```
Product ID: studylock_annual
Price: $29.99/year
Free Trial: 7 days
Display Name: "Annual Plan"
Description: "Full focus toolkit"

Product ID: studylock_monthly
Price: $4.99/month
Free Trial: 7 days
Display Name: "Monthly Plan"
Description: "Billed monthly"
```

**4. Create Entitlements**

For each app, create one entitlement:
```
Entitlement ID: premium
Attached Products: [app_annual, app_monthly]
```

This allows checking `Purchases.shared.customerInfo.entitlements["premium"]?.isActive` regardless of which product they bought.

**5. Offerings Configuration**

Create a default offering for each app:
```
Offering ID: default
Packages:
  - annual (identifier: $rc_annual)
  - monthly (identifier: $rc_monthly)
```

---

## Code Implementation

### React Native Setup

**1. Install RevenueCat SDK**
```bash
npm install react-native-purchases
npx pod-install # iOS only
```

**2. Configure in App.tsx (or index.js)**
```typescript
import Purchases from 'react-native-purchases';

// In your app initialization
async function initializeRevenueCat() {
  if (Platform.OS === 'ios') {
    await Purchases.configure({
      apiKey: 'YOUR_IOS_API_KEY',
      appUserID: null // Let RevenueCat generate anonymous ID
    });
  } else if (Platform.OS === 'android') {
    await Purchases.configure({
      apiKey: 'YOUR_ANDROID_API_KEY',
      appUserID: null
    });
  }
}
```

**3. Paywall Screen Component**

```typescript
import React, { useEffect, useState } from 'react';
import { View, Text, TouchableOpacity, ActivityIndicator, Animated } from 'react-native';
import Purchases from 'react-native-purchases';

export function PaywallScreen({ onComplete }: { onComplete: () => void }) {
  const [offerings, setOfferings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [purchasing, setPurchasing] = useState(false);

  // Animation values
  const fadeAnim = useState(new Animated.Value(0))[0];
  const slideAnim = useState(new Animated.Value(50))[0];

  useEffect(() => {
    fetchOfferings();

    // Animate on mount
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 500,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 500,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  async function fetchOfferings() {
    try {
      const offerings = await Purchases.getOfferings();
      if (offerings.current !== null) {
        setOfferings(offerings.current);
      }
    } catch (e) {
      console.error('Error fetching offerings:', e);
    } finally {
      setLoading(false);
    }
  }

  async function purchasePackage(packageToPurchase) {
    setPurchasing(true);
    try {
      const { customerInfo } = await Purchases.purchasePackage(packageToPurchase);

      // Check if they now have premium entitlement
      if (customerInfo.entitlements.active['premium']) {
        onComplete();
      }
    } catch (e) {
      if (!e.userCancelled) {
        console.error('Error purchasing:', e);
        alert('Purchase failed. Please try again.');
      }
    } finally {
      setPurchasing(false);
    }
  }

  if (loading) {
    return <ActivityIndicator size="large" />;
  }

  const annualPackage = offerings?.availablePackages.find(p => p.identifier === '$rc_annual');
  const monthlyPackage = offerings?.availablePackages.find(p => p.identifier === '$rc_monthly');

  // Calculate savings
  const annualMonthlyPrice = annualPackage ? (annualPackage.product.price / 12).toFixed(2) : 0;
  const monthlySavings = monthlyPackage && annualPackage
    ? Math.round(((monthlyPackage.product.price * 12 - annualPackage.product.price) / (monthlyPackage.product.price * 12)) * 100)
    : 0;

  return (
    <View style={styles.container}>
      {/* Progress indicator */}
      <Text style={styles.progress}>Step 5 of 6</Text>

      {/* Animated benefits */}
      <Animated.View style={{
        opacity: fadeAnim,
        transform: [{ translateY: slideAnim }]
      }}>
        <View style={styles.benefits}>
          <BenefitItem icon="📊" text="Track unlimited supplements" delay={0} />
          <BenefitItem icon="📈" text="Automatic correlation analysis" delay={100} />
          <BenefitItem icon="🔔" text="Smart reminder system" delay={200} />
          <BenefitItem icon="📱" text="Multi-protocol stacking" delay={300} />
          <BenefitItem icon="📤" text="Export your data anytime" delay={400} />
        </View>
      </Animated.View>

      {/* Pricing cards */}
      <View style={styles.pricingContainer}>
        {/* Annual (highlighted) */}
        <TouchableOpacity
          style={[styles.pricingCard, styles.pricingCardHighlighted]}
          onPress={() => purchasePackage(annualPackage)}
          disabled={purchasing}
        >
          <View style={styles.badge}>
            <Text style={styles.badgeText}>MOST POPULAR</Text>
          </View>
          <Text style={styles.planName}>Annual</Text>
          <Text style={styles.price}>{annualPackage?.product.priceString}/year</Text>
          <Text style={styles.perMonth}>(${annualMonthlyPrice}/month)</Text>
          <Text style={styles.savings}>Save {monthlySavings}%</Text>
          <Text style={styles.cta}>
            {purchasing ? 'Processing...' : 'START 7-DAY FREE TRIAL'}
          </Text>
        </TouchableOpacity>

        {/* Monthly */}
        <TouchableOpacity
          style={styles.pricingCard}
          onPress={() => purchasePackage(monthlyPackage)}
          disabled={purchasing}
        >
          <Text style={styles.planName}>Monthly</Text>
          <Text style={styles.price}>{monthlyPackage?.product.priceString}/month</Text>
          <Text style={styles.cta}>
            {purchasing ? 'Processing...' : 'START 7-DAY FREE TRIAL'}
          </Text>
        </TouchableOpacity>
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>✓ Cancel anytime during trial</Text>
        <Text style={styles.footerText}>✓ Full access for 7 days</Text>
        <Text style={styles.footerText}>✓ No charge until {getTrialEndDate()}</Text>
      </View>

      {/* Restore purchases (small, bottom left) */}
      <TouchableOpacity
        style={styles.restore}
        onPress={async () => {
          try {
            const customerInfo = await Purchases.restorePurchases();
            if (customerInfo.entitlements.active['premium']) {
              onComplete();
            } else {
              alert('No active subscription found.');
            }
          } catch (e) {
            console.error('Error restoring:', e);
          }
        }}
      >
        <Text style={styles.restoreText}>Restore Purchase</Text>
      </TouchableOpacity>
    </View>
  );
}

function BenefitItem({ icon, text, delay }) {
  const slideAnim = useState(new Animated.Value(30))[0];
  const fadeAnim = useState(new Animated.Value(0))[0];

  useEffect(() => {
    setTimeout(() => {
      Animated.parallel([
        Animated.timing(slideAnim, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 300,
          useNativeDriver: true,
        }),
      ]).start();
    }, delay);
  }, []);

  return (
    <Animated.View style={{
      flexDirection: 'row',
      alignItems: 'center',
      marginVertical: 8,
      opacity: fadeAnim,
      transform: [{ translateX: slideAnim }]
    }}>
      <Text style={{ fontSize: 24, marginRight: 12 }}>{icon}</Text>
      <Text style={{ fontSize: 16 }}>{text}</Text>
    </Animated.View>
  );
}

function getTrialEndDate() {
  const date = new Date();
  date.setDate(date.getDate() + 7);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}
```

**4. Check Subscription Status**

```typescript
// In your app's main screen or App.tsx
useEffect(() => {
  checkSubscriptionStatus();
}, []);

async function checkSubscriptionStatus() {
  try {
    const customerInfo = await Purchases.getCustomerInfo();

    if (customerInfo.entitlements.active['premium']) {
      // User has premium access
      // Allow full app functionality
    } else {
      // User is not subscribed
      // Show paywall or limited features
    }
  } catch (e) {
    console.error('Error checking subscription:', e);
  }
}
```

**5. Listen for Subscription Changes**

```typescript
useEffect(() => {
  const listener = Purchases.addCustomerInfoUpdateListener((info) => {
    // Called when subscription status changes
    if (info.entitlements.active['premium']) {
      // User just subscribed
      // Update app state
    } else {
      // User's subscription expired
      // Show paywall again
    }
  });

  return () => {
    listener.remove();
  };
}, []);
```

---

## A/B Testing Plan

### Test 1: Annual vs Monthly Default (Week 1-2)

**Variant A:** Annual highlighted, monthly secondary
**Variant B:** Both equal prominence
**Metric:** % choosing annual
**Success:** >65% annual selection

### Test 2: Trial Length (Week 3-4)

**Variant A:** 7-day trial
**Variant B:** 14-day trial
**Metric:** Trial-to-paid conversion rate
**Success:** >38% conversion (industry benchmark: 25%)

### Test 3: Paywall Placement (Week 5-6)

**Variant A:** End of onboarding (screen 5 of 6)
**Variant B:** After first value delivery (post onboarding)
**Metric:** Conversion rate
**Success:** End of onboarding should win based on ALPHA465

### Test 4: Personalization (Week 7-8)

**Variant A:** "Welcome, [Name]" throughout
**Variant B:** No personalization
**Metric:** Conversion rate
**Success:** +17% lift per ALPHA035

### Test 5: Price Points (Week 9-10)

**biomaxx Test:**
- Variant A: $35.99/year
- Variant B: $29.99/year
- Variant C: $39.99/year
**Metric:** Revenue per install (not just conversion rate)

Run same test for other 3 apps with different price points.

---

## Success Metrics

### Primary KPIs

| Metric | Target | Current (Freemium) | Hard Paywall Goal |
|--------|--------|-------------------|-------------------|
| Trial start rate | 50%+ | N/A | 50% of onboarding completions |
| Trial-to-paid conversion | 38%+ | N/A | Industry: 25%, us: 38%+ |
| Annual vs monthly mix | 65%+ annual | N/A | 65% choose annual |
| LTV per user | $25+ | $3 (freemium) | $25+ (8x increase) |
| Churn rate (monthly) | <5% | 83% | <5% |
| Churn rate (annual) | <10% | N/A | <10% after year 1 |

### Secondary KPIs

- Paywall screen time: <30 seconds average
- Purchase flow abandonment: <20%
- Restore purchase attempts: <5% of users
- Refund requests: <3% of purchases
- App Store rating impact: maintain 4.5+ stars

---

## Implementation Checklist

**Pre-Launch:**
- [ ] RevenueCat account created
- [ ] All 4 app projects configured in RevenueCat
- [ ] Products created (annual + monthly for each app)
- [ ] Entitlements configured
- [ ] SDK integrated into all 4 apps
- [ ] Paywall screens designed and implemented
- [ ] Animations tested on real devices
- [ ] Purchase flow tested with sandbox accounts
- [ ] Restore purchase functionality tested
- [ ] Error handling implemented
- [ ] Analytics events configured (paywall_viewed, trial_started, purchase_completed)

**Launch Week:**
- [ ] Monitor trial start rate hourly
- [ ] Monitor trial-to-paid conversion daily
- [ ] Check for purchase errors in logs
- [ ] Monitor App Store reviews for paywall feedback
- [ ] Track revenue in RevenueCat dashboard
- [ ] Compare to freemium baseline (if available)

**Week 2+:**
- [ ] Begin A/B testing (annual vs monthly prominence)
- [ ] Analyze drop-off points in paywall flow
- [ ] Iterate on copy if conversion < 38%
- [ ] Test different price points
- [ ] Collect qualitative feedback

---

## Legal & Compliance

### App Store Requirements

**iOS:**
- Use StoreKit 2 for purchases (required for iOS 15+)
- Clearly state trial terms
- "No charge until [date]" must be accurate
- Cancel button must be present (in Settings → Subscriptions)
- Offer Codes supported (optional but recommended)

**Android:**
- Use Google Play Billing Library 5.0+
- Trial terms clearly stated
- "No charge until [date]" accurate
- Cancellation in Google Play subscriptions

### FTC Compliance

- Trial terms must be clear BEFORE purchase
- No hidden fees
- No negative option billing (must be opt-in)
- Cancellation must be as easy as signing up
- If you claim "Save 70%", show the math

---

## Troubleshooting

### Common Issues

**Issue: "Purchase Failed" error**
- Check: Sandbox accounts configured correctly?
- Check: Products live in App Store Connect?
- Check: RevenueCat API keys correct?

**Issue: Low trial start rate (<30%)**
- Test: Move paywall earlier in onboarding
- Test: Reduce friction (fewer screens before paywall)
- Test: Improve value demonstration in onboarding

**Issue: Low trial-to-paid conversion (<25%)**
- Check: Are users experiencing value during trial?
- Check: Reminder emails sent before trial ends?
- Test: Extend trial to 14 days
- Test: Add in-app reminder on day 5

**Issue: High annual-to-monthly cancels**
- Check: Is annual price too high?
- Test: Lower annual price
- Test: Add monthly reminder emails with value props

---

## Revenue Projections (8x Multiplier)

Assuming 1,000 downloads per app per month:

**Freemium Model (baseline):**
```
1,000 downloads
× 5% paid conversion
= 50 paid users
× $3 average LTV
= $150 revenue/month
```

**Hard Paywall Model (8x):**
```
1,000 downloads
× 70% onboarding completion
= 700 onboarding completes
× 50% trial start rate
= 350 trials
× 38% trial-to-paid conversion
= 133 paid users
× 65% annual, 35% monthly
= 86 annual + 47 monthly
× $35.99 annual + $9.99 monthly
= $3,095 + $469 = $3,564 first month revenue

Then:
Month 2-12: +$469/month (new monthly subs)
Month 13+: Annual renewals at 44.1% retention = $1,365/year recurring
```

**Per-app projections (conservative):**
- Month 1: $3,500
- Month 3: $4,500
- Month 6: $6,000
- Month 12: $10,000

**All 4 apps combined:**
- Month 1: $14,000
- Month 3: $18,000
- Month 6: $24,000
- Month 12: $40,000

This assumes steady 1,000 downloads/month. With ASO + paid ads, 10K+ downloads/month possible.

---

## Next Steps

1. **Implement paywall screens** in all 4 apps (use code template above)
2. **Configure RevenueCat** (30 minutes per app)
3. **Test purchase flows** with sandbox accounts
4. **Submit to App Store** with hard paywall in place
5. **Monitor metrics** daily for first 2 weeks
6. **Iterate based on data** (target: 38%+ trial-to-paid)

**Timeline:**
- Day 1-2: Implement paywalls
- Day 3-4: Test and QA
- Day 5: Submit to stores
- Day 12-14: Approved and live
- Week 3: First A/B test
- Week 5: Optimize based on data

**This is the 8x revenue lever. Ship it first.**
