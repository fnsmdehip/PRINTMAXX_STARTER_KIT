# RevenueCat Deep Dive

Advanced guide for maximizing subscription revenue with RevenueCat. Goes beyond basic setup into paywall psychology, A/B testing frameworks, analytics interpretation, and optimization playbooks.

**Prerequisites:** Read REVENUECAT_INTEGRATION_GUIDE.md first for basic setup.

---

## Table of Contents

1. [Setup Best Practices](#1-setup-best-practices)
2. [Paywall Psychology and Strategy](#2-paywall-psychology-and-strategy)
3. [A/B Testing Framework](#3-ab-testing-framework)
4. [Analytics Deep Dive](#4-analytics-deep-dive)
5. [Pricing Optimization](#5-pricing-optimization)
6. [Trial Conversion Tactics](#6-trial-conversion-tactics)
7. [Churn Reduction Playbook](#7-churn-reduction-playbook)
8. [App-Specific Strategies](#8-app-specific-strategies)
9. [Advanced Code Patterns](#9-advanced-code-patterns)
10. [Revenue Forecasting](#10-revenue-forecasting)

---

## 1. Setup Best Practices

### SDK Configuration for Maximum Reliability

```typescript
// src/services/purchases.ts - Production-ready configuration

import Purchases, {
  LOG_LEVEL,
  CustomerInfo,
  PurchasesOffering,
  PurchasesPackage,
  PURCHASES_ERROR_CODE,
} from 'react-native-purchases';
import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_KEYS = {
  ios: process.env.REVENUECAT_IOS_KEY || 'appl_XXXXXXXXXX',
  android: process.env.REVENUECAT_ANDROID_KEY || 'goog_XXXXXXXXXX',
};

const ENTITLEMENT_ID = 'premium';

// Cache offerings to reduce API calls
let cachedOfferings: PurchasesOffering | null = null;
let offeringsLastFetched: number = 0;
const OFFERINGS_CACHE_TTL = 5 * 60 * 1000; // 5 minutes

export async function initializePurchases(): Promise<void> {
  // Only enable debug logging in development
  if (__DEV__) {
    Purchases.setLogLevel(LOG_LEVEL.DEBUG);
  } else {
    Purchases.setLogLevel(LOG_LEVEL.ERROR);
  }

  const apiKey = Platform.OS === 'ios' ? API_KEYS.ios : API_KEYS.android;

  await Purchases.configure({
    apiKey,
    appUserID: null, // Let RevenueCat generate anonymous ID initially
    observerMode: false,
    useAmazon: false,
  });

  // Set user attributes for segmentation
  await setUserAttributes();
}

async function setUserAttributes(): Promise<void> {
  try {
    // Track install date for cohort analysis
    const installDate = await AsyncStorage.getItem('install_date');
    if (!installDate) {
      const today = new Date().toISOString().split('T')[0];
      await AsyncStorage.setItem('install_date', today);
      await Purchases.setAttributes({ install_date: today });
    }

    // Track app version for debugging
    const appVersion = require('../../package.json').version;
    await Purchases.setAttributes({ app_version: appVersion });

    // Track platform for cross-platform analysis
    await Purchases.setAttributes({ platform: Platform.OS });
  } catch (error) {
    console.error('Error setting user attributes:', error);
  }
}
```

### Offering Configuration Strategy

RevenueCat Offerings let you remotely configure products without app updates.

**Recommended Offering Structure:**

```
Project: PRINTMAXX Apps
  |
  +-- App: PrayerLock
  |     |
  |     +-- Entitlement: premium
  |     |
  |     +-- Offerings:
  |           |
  |           +-- default (current)
  |           |     +-- $rc_monthly -> prayerlock_monthly_999
  |           |     +-- $rc_annual -> prayerlock_annual_4999
  |           |
  |           +-- high_price (A/B test)
  |           |     +-- $rc_monthly -> prayerlock_monthly_1299
  |           |     +-- $rc_annual -> prayerlock_annual_6999
  |           |
  |           +-- trial_emphasis (A/B test)
  |                 +-- $rc_monthly -> prayerlock_monthly_999 (7-day trial)
  |                 +-- $rc_annual -> prayerlock_annual_4999 (14-day trial)
```

**Why This Structure:**

1. **Single entitlement** (`premium`) across all products simplifies code
2. **Multiple offerings** enable remote A/B testing without app updates
3. **Standard package identifiers** (`$rc_monthly`, `$rc_annual`) allow generic paywall code
4. **Separate offerings per test** give clean data

### Product ID Naming Convention

```
{app}_{duration}_{price_cents}[_{variant}]

Examples:
prayerlock_monthly_999          # Standard monthly $9.99
prayerlock_annual_4999          # Standard annual $49.99
prayerlock_monthly_1299_v2      # Price test monthly $12.99
prayerlock_annual_6999_v2       # Price test annual $69.99
prayerlock_annual_4999_14trial  # 14-day trial variant
```

---

## 2. Paywall Psychology and Strategy

### The 3-Second Rule

Users decide whether to read your paywall in 3 seconds. Optimize for:

1. **Headline clarity** - What they get in 5 words or less
2. **Visual hierarchy** - Eye goes to price or value first
3. **Friction reduction** - One clear next action

### Paywall Anatomy (High-Converting Structure)

```
+------------------------------------------+
|                                          |
|  [X Close]                               |
|                                          |
|         [App Icon or Hero Image]         |
|                                          |
|      "Unlock Your Full Potential"        |  <- Benefit headline
|        Subtitle with social proof        |
|                                          |
|  +------------------------------------+  |
|  |  ANNUAL (Best Value)    [Selected] |  |  <- Default to annual
|  |  $49.99/year  ($4.17/mo)           |  |
|  |  Save 58%                          |  |
|  +------------------------------------+  |
|  +------------------------------------+  |
|  |  MONTHLY                           |  |
|  |  $9.99/month                       |  |
|  +------------------------------------+  |
|                                          |
|  [Feature 1] ..........................  |
|  [Feature 2] ..........................  |
|  [Feature 3] ..........................  |  <- 3-5 features max
|  [Feature 4] ..........................  |
|                                          |
|  +------------------------------------+  |
|  |                                    |  |
|  |   Start 7-Day Free Trial           |  |  <- Action-focused CTA
|  |                                    |  |
|  +------------------------------------+  |
|                                          |
|  Then $49.99/year. Cancel anytime.       |  <- Trust builder
|                                          |
|         Restore Purchases                |
|                                          |
|  Terms  |  Privacy  |  Manage Sub        |  <- Required links
|                                          |
+------------------------------------------+
```

### Paywall Timing Strategies

**When to show the paywall:**

| Trigger | Conversion Rate | Best For |
|---------|-----------------|----------|
| After onboarding | 5-10% | Simple apps with obvious value |
| After first value moment | 10-15% | Apps where user must experience value |
| Feature gate | 15-25% | Feature-rich apps |
| Session-based (3rd open) | 8-12% | Habit apps |
| Soft prompt then hard | 12-18% | Complex apps |

**PrayerLock recommended flow:**

```
1. Onboarding (3 screens)
2. First morning lock (free, 5 min)
3. User completes lock successfully
4. Show "congrats" screen with upgrade prompt (soft)
5. If dismissed, allow 2 more free sessions
6. On 4th session, show paywall (harder)
7. Feature gates for premium content
```

### Hard vs Soft Paywalls

**Hard Paywall:** Blocks all usage until purchase
- Higher ARPU
- Lower installs
- Best for: utility apps where core function is the product

**Soft Paywall:** Allows limited free usage
- Higher installs
- Lower conversion rate but higher volume
- Best for: content apps, habit apps, apps with network effects

**Recommended by app:**

| App | Paywall Type | Free Tier |
|-----|--------------|-----------|
| PrayerLock | Semi-hard | 3 sessions, then paywall |
| WalkToUnlock | Hard | None - core feature is premium |
| StudyLock | Soft | Basic blocking, premium for schedules |

### Psychological Triggers

**1. Anchoring:**
Show annual price first (higher number anchors perception).
Then show monthly as "expensive" by comparison.

```typescript
// Calculate and show savings
const annualPrice = annualPackage.product.price;
const monthlyPrice = monthlyPackage.product.price;
const monthlyEquivalent = annualPrice / 12;
const savingsPercent = Math.round(((monthlyPrice - monthlyEquivalent) / monthlyPrice) * 100);

// Display: "Save 58%" on annual option
```

**2. Loss Aversion:**
Frame the trial as "yours" that they'll "lose."

```typescript
// Bad: "Start free trial"
// Good: "Claim your 7 free days"
// Better: "Your 7 free days are waiting"
```

**3. Social Proof:**
Numbers work. Use what you have.

```typescript
// Early stage (no real numbers)
"Join thousands of users" // Vague but not false

// Mid stage
"10,000+ downloads" // Verifiable from App Store

// Growth stage
"50,000 prayers completed this week" // Specific, impressive
```

**4. Scarcity/Urgency:**
Use sparingly and honestly.

```typescript
// Legitimate urgency
"Introductory pricing - lock in this rate"
"7 days left in launch sale"

// Avoid fake urgency
"Only 3 spots left!" // Unless actually true
```

---

## 3. A/B Testing Framework

### RevenueCat Experiments Setup

RevenueCat handles experiment assignment automatically via Offerings.

**Setting up an experiment:**

1. **Create variant offerings** in RevenueCat dashboard
2. **Go to Experiments** tab
3. **Create new experiment:**
   - Name: "Annual Price Test Q1 2026"
   - Control: `default` offering
   - Variant: `high_price` offering
   - Traffic split: 50/50
   - Primary metric: Trial Conversion Rate
4. **Start experiment**

**Code requires no changes:**

```typescript
// RevenueCat returns the assigned offering automatically
const offerings = await Purchases.getOfferings();
const assignedOffering = offerings.current; // User's test variant

// Your paywall renders the offering - no conditional logic needed
```

### What to A/B Test (Priority Order)

**High Impact (Test First):**

1. **Price points** - 20-30% revenue impact possible
2. **Trial length** - 10-20% conversion impact
3. **Annual vs monthly default** - 30-50% LTV impact

**Medium Impact:**

4. **Paywall headline** - 5-15% conversion impact
5. **Feature list** - 5-10% conversion impact
6. **CTA button text** - 3-8% conversion impact

**Lower Impact (Test Later):**

7. **Color scheme**
8. **Icon/imagery**
9. **Legal text placement**

### A/B Test Tracking Code

```typescript
// Track which offering variant user saw
import analytics from '@segment/analytics-react-native';

export async function trackPaywallView(): Promise<void> {
  const offerings = await Purchases.getOfferings();
  const currentOffering = offerings.current;

  analytics.track('Paywall Viewed', {
    offering_id: currentOffering?.identifier || 'none',
    packages: currentOffering?.availablePackages.map(p => ({
      identifier: p.identifier,
      price: p.product.price,
      currency: p.product.currencyCode,
    })),
  });
}

export async function trackPurchaseAttempt(
  packageId: string,
  success: boolean,
  errorCode?: string
): Promise<void> {
  const offerings = await Purchases.getOfferings();

  analytics.track('Purchase Attempted', {
    offering_id: offerings.current?.identifier,
    package_id: packageId,
    success,
    error_code: errorCode,
  });
}
```

### Statistical Significance Calculator

Don't stop tests too early. Use this framework:

```typescript
// Minimum sample size calculator
function calculateMinSampleSize(
  baseConversionRate: number, // e.g., 0.10 for 10%
  minimumDetectableEffect: number, // e.g., 0.20 for 20% lift
  significance: number = 0.05, // 95% confidence
  power: number = 0.80 // 80% power
): number {
  const alpha = significance;
  const beta = 1 - power;

  // Z-scores
  const zAlpha = 1.96; // For 95% confidence
  const zBeta = 0.84; // For 80% power

  const p1 = baseConversionRate;
  const p2 = baseConversionRate * (1 + minimumDetectableEffect);
  const pBar = (p1 + p2) / 2;

  const n = Math.pow(
    zAlpha * Math.sqrt(2 * pBar * (1 - pBar)) +
    zBeta * Math.sqrt(p1 * (1 - p1) + p2 * (1 - p2)),
    2
  ) / Math.pow(p1 - p2, 2);

  return Math.ceil(n);
}

// Example: 10% baseline conversion, want to detect 20% lift
// Need ~3,800 users per variant (7,600 total) for statistical significance
const sampleSize = calculateMinSampleSize(0.10, 0.20);
```

### Test Duration Guidelines

| Baseline Conversion | Minimum Effect | Users per Variant | At 500 installs/day |
|---------------------|----------------|-------------------|---------------------|
| 10% | 20% lift | 3,800 | 15 days |
| 10% | 30% lift | 1,700 | 7 days |
| 15% | 20% lift | 2,200 | 9 days |
| 15% | 30% lift | 1,000 | 4 days |

**Rules:**
- Run test for minimum 2 weeks (capture weekend effects)
- Don't peek and stop early
- Don't change mid-test
- Document everything

---

## 4. Analytics Deep Dive

### Key Metrics Definitions

**Acquisition Metrics:**

| Metric | Definition | Target |
|--------|------------|--------|
| Install to Trial Start | Users who start trial / Total installs | >25% |
| Paywall View Rate | Paywall views / Active users | 50-80% |
| Trial Start Rate | Trials started / Paywall views | >30% |

**Conversion Metrics:**

| Metric | Definition | Target |
|--------|------------|--------|
| Trial Conversion | Paid after trial / Trial starts | >15% |
| Direct Conversion | Paid without trial / Paywall views | >5% |
| Overall Conversion | All paid / All installs | >3% |

**Retention Metrics:**

| Metric | Definition | Target |
|--------|------------|--------|
| Monthly Churn | Cancelled / Active at month start | <8% |
| Renewal Rate | Renewed / Up for renewal | >85% |
| Annual Retention | Still active after 12 months | >50% |

**Revenue Metrics:**

| Metric | Definition | Target |
|--------|------------|--------|
| MRR | Monthly Recurring Revenue | Growing >10%/mo |
| ARPU | Revenue / Active users | $3-8/mo |
| LTV | Total revenue per customer lifetime | >$30 |
| LTV:CAC | Lifetime value : Acquisition cost | >3:1 |

### RevenueCat Dashboard Navigation

**Charts to monitor daily:**

1. **MRR** - Overall health
2. **Active Subscriptions** - Growth trend
3. **Churn** - Early warning of problems

**Charts to monitor weekly:**

4. **Trial Conversion by Cohort** - Onboarding effectiveness
5. **Revenue by Product** - Which tier performing best
6. **Revenue by Country** - Localization opportunities

**Charts to monitor monthly:**

7. **Realized LTV** - Long-term value
8. **Cohort Analysis** - Retention trends
9. **Refund Rate** - Product quality

### Custom Analytics Implementation

```typescript
// src/services/analytics.ts

interface SubscriptionEvent {
  event_type: string;
  user_id: string;
  product_id: string;
  price: number;
  currency: string;
  offering_id?: string;
  trial_length?: number;
  country?: string;
  timestamp: string;
}

class SubscriptionAnalytics {
  private events: SubscriptionEvent[] = [];

  async trackTrialStart(
    userId: string,
    packageInfo: PurchasesPackage,
    offeringId: string
  ): Promise<void> {
    const event: SubscriptionEvent = {
      event_type: 'trial_start',
      user_id: userId,
      product_id: packageInfo.product.identifier,
      price: packageInfo.product.price,
      currency: packageInfo.product.currencyCode,
      offering_id: offeringId,
      trial_length: packageInfo.product.introPrice?.periodNumberOfUnits,
      country: packageInfo.product.priceString.includes('$') ? 'US' : 'OTHER',
      timestamp: new Date().toISOString(),
    };

    this.events.push(event);
    await this.sendToBackend(event);
  }

  async trackConversion(
    userId: string,
    fromTrial: boolean,
    packageInfo: PurchasesPackage
  ): Promise<void> {
    const event: SubscriptionEvent = {
      event_type: fromTrial ? 'trial_conversion' : 'direct_purchase',
      user_id: userId,
      product_id: packageInfo.product.identifier,
      price: packageInfo.product.price,
      currency: packageInfo.product.currencyCode,
      timestamp: new Date().toISOString(),
    };

    await this.sendToBackend(event);
  }

  async trackChurn(userId: string, reason?: string): Promise<void> {
    const event: SubscriptionEvent = {
      event_type: 'churn',
      user_id: userId,
      product_id: '',
      price: 0,
      currency: '',
      timestamp: new Date().toISOString(),
    };

    await this.sendToBackend(event);
  }

  private async sendToBackend(event: SubscriptionEvent): Promise<void> {
    // Send to your analytics backend
    // This could be Mixpanel, Amplitude, or custom backend
    try {
      await fetch('https://your-api.com/analytics/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(event),
      });
    } catch (error) {
      console.error('Analytics send failed:', error);
      // Queue for retry
      await AsyncStorage.setItem(
        `pending_event_${Date.now()}`,
        JSON.stringify(event)
      );
    }
  }
}

export const subscriptionAnalytics = new SubscriptionAnalytics();
```

### Funnel Analysis Template

Track these events in order to identify drop-off points:

```
1. app_open
2. onboarding_start
3. onboarding_complete
4. first_value_action (e.g., first_prayer_completed)
5. paywall_view
6. paywall_product_select (which product)
7. paywall_purchase_tap
8. purchase_start (StoreKit flow begins)
9. purchase_complete OR purchase_cancelled OR purchase_error
10. premium_feature_used
```

**Example funnel analysis:**

```
Step                    Users    Conversion
-----------------------------------------
app_open               10,000    100%
onboarding_complete     8,500     85%  <- 15% drop, normal
first_value_action      6,000     60%  <- Need better onboarding
paywall_view            4,000     40%  <- OK
paywall_purchase_tap    1,200     12%  <- Paywall needs work
purchase_complete         800      8%  <- Payment friction normal
```

---

## 5. Pricing Optimization

### Price Point Framework

**Willingness-to-pay research methods:**

1. **Van Westendorp Price Sensitivity Meter**
   - Survey users: "At what price would you consider this too cheap? A bargain? Getting expensive? Too expensive?"
   - Plot responses to find optimal price range

2. **Competitor Analysis**
   - List 5-10 competitors
   - Record their monthly and annual prices
   - Position at median or slightly above if differentiated

3. **A/B Test Price Points**
   - Test +20% and -20% from baseline
   - Measure conversion AND revenue (not just conversion)

### PRINTMAXX App Pricing Analysis

Based on competitor research and market positioning:

**PrayerLock (Prayer + Screen Blocking):**

Competitors:
- Hallow: $12.99/mo, $59.99/yr
- Pray.com: $9.99/mo, $49.99/yr
- Abide: $14.99/mo, $69.99/yr

Recommendation: $9.99/mo, $49.99/yr (mid-market, mass appeal)

**WalkToUnlock (Fitness + Screen Blocking):**

Competitors:
- Alarmy: $4.99/mo, $24.99/yr
- One Sec: $6.99/mo, $29.99/yr
- Opal: $9.99/mo, $49.99/yr

Recommendation: $7.99/mo, $39.99/yr (competitive with clear value)

**StudyLock (Study Focus):**

Competitors:
- Forest: $1.99 one-time (old model)
- Flora: $4.99/mo
- Tide Focus: $3.99/mo

Recommendation: $6.99/mo, $34.99/yr (higher than average, more features)

### Annual Discount Strategy

Annual discounts affect LTV significantly:

| Annual Discount | Monthly Equiv | LTV Impact | Conversion Impact |
|-----------------|---------------|------------|-------------------|
| 17% (10 months) | High | +40% LTV | -5% conversion |
| 33% (8 months) | Medium | +20% LTV | Baseline |
| 50% (6 months) | Low | -10% LTV | +10% conversion |
| 58% (5 months) | Very Low | -20% LTV | +15% conversion |

**Recommendation:** 50-58% discount on annual. The extra conversions typically outweigh the per-user LTV loss.

### Price Localization

RevenueCat automatically localizes pricing, but consider:

1. **Emerging markets:** Consider 40-60% lower pricing
   - India, Brazil, Indonesia, Philippines
   - Lower price, higher volume

2. **Premium markets:** Can be 10-20% higher
   - Switzerland, Norway, Australia
   - Users expect higher prices

```typescript
// Check country for analytics/segmentation
const getCountryFromPrice = (priceString: string): string => {
  if (priceString.includes('$')) return 'USD';
  if (priceString.includes('€')) return 'EUR';
  if (priceString.includes('£')) return 'GBP';
  if (priceString.includes('¥')) return 'JPY/CNY';
  if (priceString.includes('₹')) return 'INR';
  return 'OTHER';
};
```

---

## 6. Trial Conversion Tactics

### Trial Length Optimization

| Trial Length | Conversion Rate | Best For |
|--------------|-----------------|----------|
| 3 days | 12-18% | Instant value apps (screen blockers) |
| 7 days | 15-22% | Habit apps (trackers, productivity) |
| 14 days | 18-25% | Content apps (devotionals, courses) |
| 30 days | 20-30% | Complex apps (need time to learn) |

**Rule of thumb:** Trial should be long enough to experience value 3+ times.

### Trial Engagement Sequence

Users who engage during trial convert 3x better. Push engagement:

**Day 0 (Trial Start):**
- Welcome push notification
- In-app guide to premium features
- Set up core feature (e.g., first prayer time)

**Day 1:**
- Reminder to use core feature
- Highlight a premium feature they haven't tried

**Day 3:**
- Progress celebration ("You've prayed 3 days in a row!")
- Social proof ("Join 10,000+ users who upgraded")

**Day 5 (If 7-day trial):**
- Urgency: "2 days left in your trial"
- Feature highlight: "Have you tried [premium feature]?"

**Day 6:**
- Final reminder: "Last day of premium access"
- Simplified upgrade path (one-tap purchase)

### Push Notification Templates

```typescript
// Trial engagement notifications

const TRIAL_NOTIFICATIONS = {
  day0: {
    title: "Welcome to PrayerLock Pro! 🙏",
    body: "Your 7-day premium trial has started. Set up your first prayer time to make the most of it.",
    action: "open_setup"
  },
  day1: {
    title: "Your streak is safe",
    body: "Premium feature: Streak Freezes protect your progress. You have 2 freezes available.",
    action: "open_premium_features"
  },
  day3: {
    title: "3 days strong! 🎉",
    body: "You've prayed every day this trial. Keep this momentum with unlimited access.",
    action: "open_paywall"
  },
  day5: {
    title: "2 days left in trial",
    body: "Don't lose access to extended prayer times and family accountability.",
    action: "open_paywall"
  },
  day6: {
    title: "Trial ends tomorrow",
    body: "Lock in your annual rate now: $49.99/year ($4.17/month).",
    action: "open_paywall"
  }
};
```

### Trial Extension Strategy

If conversion is low, consider extending trials for engaged users:

```typescript
// Extend trial for engaged users who didn't convert
async function offerTrialExtension(userId: string): Promise<void> {
  const customerInfo = await Purchases.getCustomerInfo();

  // Check if trial expired and user was engaged
  const wasEngaged = await checkUserEngagement(userId);
  const trialExpired = !customerInfo.entitlements.active['premium'];

  if (trialExpired && wasEngaged) {
    // Offer 3-day extension via promotional offer
    // Requires setting up Promotional Offers in App Store Connect
    await showExtensionOffer();
  }
}
```

---

## 7. Churn Reduction Playbook

### Understanding Churn Types

**Voluntary Churn (User chose to cancel):**
- Poor product-market fit
- Price too high
- Found alternative
- No longer needs product

**Involuntary Churn (Payment failed):**
- Card expired
- Insufficient funds
- Card declined
- Account issues

### Voluntary Churn Prevention

**1. Exit Survey:**
Show survey when user cancels (before they complete cancellation):

```typescript
// Cancellation flow interception
const CANCELLATION_REASONS = [
  { id: 'too_expensive', label: "It's too expensive" },
  { id: 'not_using', label: "I'm not using it enough" },
  { id: 'missing_features', label: "Missing features I need" },
  { id: 'found_alternative', label: "Found a better alternative" },
  { id: 'temporary', label: "Just need a break" },
  { id: 'other', label: "Other reason" },
];

// Based on reason, offer retention:
const RETENTION_OFFERS = {
  too_expensive: {
    type: 'discount',
    offer: '50% off next 3 months',
    code: 'STAYWITHUS50'
  },
  not_using: {
    type: 'engagement',
    offer: 'Let us help you get more value',
    action: 'schedule_call'
  },
  temporary: {
    type: 'pause',
    offer: 'Pause for 1-3 months instead',
    action: 'pause_subscription'
  }
};
```

**2. Win-back Campaigns:**
Email sequence for cancelled users:

- Day 1: "We're sorry to see you go" (no ask)
- Day 7: "What we've improved" (feature updates)
- Day 14: "Come back offer: 50% off" (discount)
- Day 30: "Final offer: 60% off annual" (bigger discount)

**3. Feature Usage Analysis:**
Users who churn often show warning signs:

```typescript
// Churn risk scoring
interface ChurnRiskFactors {
  dayssinceLastOpen: number;
  featureUsageDecline: boolean;
  supportTickets: number;
  missedPayments: number;
}

function calculateChurnRisk(factors: ChurnRiskFactors): 'low' | 'medium' | 'high' {
  let score = 0;

  if (factors.dayssinceLastOpen > 7) score += 2;
  if (factors.dayssinceLastOpen > 14) score += 3;
  if (factors.featureUsageDecline) score += 2;
  if (factors.supportTickets > 2) score += 1;
  if (factors.missedPayments > 0) score += 3;

  if (score >= 5) return 'high';
  if (score >= 3) return 'medium';
  return 'low';
}
```

### Involuntary Churn Recovery (Dunning)

RevenueCat has built-in grace periods and retry logic. Supplement with:

**1. Payment Failed Email Sequence:**

```
Day 0: "Oops! Your payment didn't go through"
- Friendly tone
- Link to update payment method

Day 3: "Still having trouble?"
- Offer help
- Explain what happens if not resolved

Day 7: "Last chance to keep your access"
- Urgency
- Clear CTA to update payment
```

**2. Grace Period Strategy:**

Configure in App Store Connect:
- Billing retry period: 16 days (Apple manages)
- Grace period: 16 days (user keeps access while retrying)

```typescript
// Check billing issue state
async function checkBillingStatus(customerInfo: CustomerInfo): Promise<void> {
  const entitlement = customerInfo.entitlements.active['premium'];

  if (entitlement?.billingIssueDetectedAt) {
    // Show banner in app
    showBillingIssueBanner();
  }
}
```

### Churn Analysis Dashboard

Track these segments:

| Segment | Definition | Action |
|---------|------------|--------|
| Trial Churned | Started trial, didn't convert | Improve trial experience |
| Month 1 Churned | Paid once, cancelled | Improve onboarding |
| Month 3-6 Churned | Loyal then left | Check for patterns |
| Annual Churned | Didn't renew annual | Win-back 60 days before |
| Involuntary Churned | Payment failed | Dunning sequence |

---

## 8. App-Specific Strategies

### PrayerLock Strategy

**Positioning:** Faith-based productivity tool with screen blocking

**Pricing:**
- Monthly: $9.99
- Annual: $49.99 (58% savings)
- Trial: 7 days

**Paywall Timing:**
1. After successful first prayer session (value delivered)
2. When trying to access 30+ minute sessions (feature gate)
3. When accessing family accountability (feature gate)

**Premium Features to Gate:**
- Extended sessions (30, 60 min)
- Family accountability
- Custom prayer prompts
- Streak freezes
- Ad-free experience

**Conversion Optimization:**
- Lead with "family accountability" (emotional value)
- Show streak protection prominently
- Use faith-specific language ("deepen your prayer life")

```typescript
// PrayerLock-specific paywall copy
const PRAYERLOCK_PAYWALL = {
  headline: "Deepen Your Prayer Life",
  subheadline: "Join 10,000+ believers in daily prayer",
  features: [
    { title: "Extended Prayer Times", desc: "30 and 60 minute sessions" },
    { title: "Family Accountability", desc: "See your family's streaks" },
    { title: "Custom Prompts", desc: "Create your daily focus" },
    { title: "Streak Protection", desc: "Life happens. 2 freezes/month" },
  ],
  cta: "Start Your Journey",
  trial_text: "7 days free, then $49.99/year",
};
```

### WalkToUnlock Strategy

**Positioning:** Get-up-and-move screen blocker for fitness-minded users

**Pricing:**
- Monthly: $7.99
- Annual: $39.99 (58% savings)
- Trial: 3 days (quick value demonstration)

**Paywall Timing:**
1. After install (hard paywall, core feature is premium)
2. Alternative: After demonstrating the blocking works (soft version)

**Premium Features:**
- All screen blocking functionality
- Step goal customization
- Schedule settings
- Health app integration
- Unlimited devices

**Conversion Optimization:**
- Emphasize health benefits
- Show "time saved from phone" stats
- Use fitness/movement language

```typescript
// WalkToUnlock-specific paywall copy
const WALKTOUNLOCK_PAYWALL = {
  headline: "Break the Phone Habit",
  subheadline: "Get moving before you start scrolling",
  features: [
    { title: "Morning Walk Lock", desc: "Complete steps to unlock" },
    { title: "Custom Goals", desc: "Set your own step targets" },
    { title: "Smart Scheduling", desc: "Only lock when you choose" },
    { title: "Health Integration", desc: "Syncs with Apple Health" },
  ],
  cta: "Start Walking",
  trial_text: "3 days free, then $39.99/year",
};
```

### StudyLock Strategy

**Positioning:** Focus tool for students and knowledge workers

**Pricing:**
- Monthly: $6.99
- Annual: $34.99 (58% savings)
- Trial: 7 days (needs time to prove value)

**Paywall Timing:**
1. After first successful study session
2. When accessing app blocking (feature gate)
3. When accessing schedule features (feature gate)

**Premium Features:**
- App/website blocking
- Study schedules
- Focus statistics
- Break reminders
- Study groups

**Conversion Optimization:**
- Target students with academic language
- Show productivity stats
- Emphasize "study smarter, not harder"
- Consider student discount (verify .edu email)

```typescript
// StudyLock-specific paywall copy
const STUDYLOCK_PAYWALL = {
  headline: "Ace Your Studies",
  subheadline: "Distraction-free focus when you need it",
  features: [
    { title: "App Blocking", desc: "Block distracting apps" },
    { title: "Study Schedules", desc: "Automated focus sessions" },
    { title: "Progress Stats", desc: "Track your focus time" },
    { title: "Smart Breaks", desc: "Pomodoro-style reminders" },
  ],
  cta: "Start Focusing",
  trial_text: "7 days free, then $34.99/year",
};
```

---

## 9. Advanced Code Patterns

### Promotional Offers (App Store)

For win-back and retention campaigns:

```typescript
// Promotional offers require signature generation on your backend
import Purchases from 'react-native-purchases';

interface PromoOffer {
  identifier: string;
  keyIdentifier: string;
  nonce: string;
  signature: string;
  timestamp: number;
}

async function purchaseWithPromoOffer(
  packageToPurchase: PurchasesPackage,
  promoOffer: PromoOffer
): Promise<void> {
  try {
    const { customerInfo } = await Purchases.purchasePackage(
      packageToPurchase,
      null, // No upgrade/downgrade
      promoOffer // Promotional offer
    );

    if (customerInfo.entitlements.active['premium']) {
      // Success
    }
  } catch (error) {
    console.error('Promo purchase failed:', error);
  }
}

// Backend endpoint to generate signature
// POST /api/generate-promo-signature
// Returns: PromoOffer object
```

### Subscription Management Screen

Required by App Store guidelines:

```typescript
// src/screens/ManageSubscriptionScreen.tsx

import React from 'react';
import { View, Text, TouchableOpacity, Linking, Alert } from 'react-native';
import Purchases, { CustomerInfo } from 'react-native-purchases';

export function ManageSubscriptionScreen() {
  const [customerInfo, setCustomerInfo] = React.useState<CustomerInfo | null>(null);

  React.useEffect(() => {
    Purchases.getCustomerInfo().then(setCustomerInfo);
  }, []);

  const activeEntitlement = customerInfo?.entitlements.active['premium'];

  const openManageSubscriptions = () => {
    // Opens App Store subscription management
    Linking.openURL('https://apps.apple.com/account/subscriptions');
  };

  const handleRestore = async () => {
    try {
      const info = await Purchases.restorePurchases();
      setCustomerInfo(info);

      if (info.entitlements.active['premium']) {
        Alert.alert('Success', 'Your subscription has been restored.');
      } else {
        Alert.alert('No Subscription Found', 'No active subscription was found for this account.');
      }
    } catch (error) {
      Alert.alert('Error', 'Unable to restore purchases. Please try again.');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Subscription</Text>

      {activeEntitlement ? (
        <View>
          <Text style={styles.status}>Status: Active</Text>
          <Text style={styles.detail}>
            Product: {activeEntitlement.productIdentifier}
          </Text>
          <Text style={styles.detail}>
            Renews: {activeEntitlement.expirationDate
              ? new Date(activeEntitlement.expirationDate).toLocaleDateString()
              : 'Never'}
          </Text>

          {activeEntitlement.willRenew ? (
            <Text style={styles.detail}>Auto-renewal: On</Text>
          ) : (
            <Text style={styles.warning}>
              Your subscription will expire on {new Date(activeEntitlement.expirationDate!).toLocaleDateString()}
            </Text>
          )}
        </View>
      ) : (
        <Text style={styles.status}>No active subscription</Text>
      )}

      <TouchableOpacity
        style={styles.button}
        onPress={openManageSubscriptions}
      >
        <Text style={styles.buttonText}>Manage Subscription</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.linkButton}
        onPress={handleRestore}
      >
        <Text style={styles.linkText}>Restore Purchases</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.linkButton}
        onPress={() => Linking.openURL('https://yourapp.com/terms')}
      >
        <Text style={styles.linkText}>Terms of Service</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.linkButton}
        onPress={() => Linking.openURL('https://yourapp.com/privacy')}
      >
        <Text style={styles.linkText}>Privacy Policy</Text>
      </TouchableOpacity>
    </View>
  );
}
```

### Offline Support

Handle offline scenarios gracefully:

```typescript
// src/hooks/useOfflineAwarePremium.ts

import { useState, useEffect } from 'react';
import NetInfo from '@react-native-community/netinfo';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Purchases, { CustomerInfo } from 'react-native-purchases';

const PREMIUM_CACHE_KEY = 'cached_premium_status';
const CACHE_EXPIRY_KEY = 'premium_cache_expiry';
const CACHE_DURATION = 7 * 24 * 60 * 60 * 1000; // 7 days

export function useOfflineAwarePremium() {
  const [isPremium, setIsPremium] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isOffline, setIsOffline] = useState(false);

  useEffect(() => {
    const checkPremiumStatus = async () => {
      const netState = await NetInfo.fetch();
      setIsOffline(!netState.isConnected);

      if (netState.isConnected) {
        // Online: fetch from RevenueCat
        try {
          const customerInfo = await Purchases.getCustomerInfo();
          const premium = customerInfo.entitlements.active['premium'] !== undefined;
          setIsPremium(premium);

          // Cache the result
          await AsyncStorage.setItem(PREMIUM_CACHE_KEY, JSON.stringify(premium));
          await AsyncStorage.setItem(CACHE_EXPIRY_KEY, String(Date.now() + CACHE_DURATION));
        } catch (error) {
          // Fall back to cache on error
          await loadFromCache();
        }
      } else {
        // Offline: use cache
        await loadFromCache();
      }

      setIsLoading(false);
    };

    const loadFromCache = async () => {
      const cached = await AsyncStorage.getItem(PREMIUM_CACHE_KEY);
      const expiry = await AsyncStorage.getItem(CACHE_EXPIRY_KEY);

      if (cached && expiry && Date.now() < Number(expiry)) {
        setIsPremium(JSON.parse(cached));
      } else {
        // Cache expired or not available, default to false
        setIsPremium(false);
      }
    };

    checkPremiumStatus();

    // Listen for network changes
    const unsubscribe = NetInfo.addEventListener(state => {
      if (state.isConnected && isOffline) {
        // Came back online, refresh status
        checkPremiumStatus();
      }
      setIsOffline(!state.isConnected);
    });

    return () => unsubscribe();
  }, []);

  return { isPremium, isLoading, isOffline };
}
```

### Error Handling Best Practices

```typescript
// src/utils/purchaseErrors.ts

import { PURCHASES_ERROR_CODE, PurchasesError } from 'react-native-purchases';

interface ErrorHandlingResult {
  userMessage: string;
  shouldRetry: boolean;
  logLevel: 'info' | 'warn' | 'error';
}

export function handlePurchaseError(error: PurchasesError): ErrorHandlingResult {
  switch (error.code) {
    case PURCHASES_ERROR_CODE.PURCHASE_CANCELLED_ERROR:
      return {
        userMessage: '', // Don't show message for cancellation
        shouldRetry: false,
        logLevel: 'info',
      };

    case PURCHASES_ERROR_CODE.PURCHASE_NOT_ALLOWED_ERROR:
      return {
        userMessage: 'Purchases are not allowed on this device. Please check your device settings.',
        shouldRetry: false,
        logLevel: 'warn',
      };

    case PURCHASES_ERROR_CODE.PURCHASE_INVALID_ERROR:
      return {
        userMessage: 'This purchase is not available. Please try again later.',
        shouldRetry: true,
        logLevel: 'error',
      };

    case PURCHASES_ERROR_CODE.PRODUCT_NOT_AVAILABLE_FOR_PURCHASE_ERROR:
      return {
        userMessage: 'This subscription is not available in your region.',
        shouldRetry: false,
        logLevel: 'warn',
      };

    case PURCHASES_ERROR_CODE.NETWORK_ERROR:
      return {
        userMessage: 'Network error. Please check your connection and try again.',
        shouldRetry: true,
        logLevel: 'warn',
      };

    case PURCHASES_ERROR_CODE.RECEIPT_ALREADY_IN_USE_ERROR:
      return {
        userMessage: 'This subscription is already active on another account.',
        shouldRetry: false,
        logLevel: 'warn',
      };

    case PURCHASES_ERROR_CODE.UNKNOWN_ERROR:
    default:
      return {
        userMessage: 'Something went wrong. Please try again.',
        shouldRetry: true,
        logLevel: 'error',
      };
  }
}
```

---

## 10. Revenue Forecasting

### MRR Projection Model

```typescript
// Simple MRR projection based on current metrics

interface MRRProjectionInputs {
  currentMRR: number;
  monthlyInstalls: number;
  installToTrialRate: number;
  trialConversionRate: number;
  monthlyChurnRate: number;
  averageRevenuePerUser: number;
}

interface MRRProjection {
  month: number;
  newMRR: number;
  churnedMRR: number;
  netMRR: number;
  totalMRR: number;
  totalSubscribers: number;
}

function projectMRR(inputs: MRRProjectionInputs, months: number): MRRProjection[] {
  const projections: MRRProjection[] = [];
  let currentMRR = inputs.currentMRR;
  let totalSubscribers = currentMRR / inputs.averageRevenuePerUser;

  for (let month = 1; month <= months; month++) {
    // New subscribers this month
    const trials = inputs.monthlyInstalls * inputs.installToTrialRate;
    const conversions = trials * inputs.trialConversionRate;
    const newMRR = conversions * inputs.averageRevenuePerUser;

    // Churned subscribers this month
    const churnedSubscribers = totalSubscribers * inputs.monthlyChurnRate;
    const churnedMRR = churnedSubscribers * inputs.averageRevenuePerUser;

    // Net change
    const netMRR = newMRR - churnedMRR;
    currentMRR += netMRR;
    totalSubscribers += conversions - churnedSubscribers;

    projections.push({
      month,
      newMRR: Math.round(newMRR),
      churnedMRR: Math.round(churnedMRR),
      netMRR: Math.round(netMRR),
      totalMRR: Math.round(currentMRR),
      totalSubscribers: Math.round(totalSubscribers),
    });
  }

  return projections;
}

// Example usage:
const projection = projectMRR({
  currentMRR: 0,
  monthlyInstalls: 5000,
  installToTrialRate: 0.25,
  trialConversionRate: 0.15,
  monthlyChurnRate: 0.08,
  averageRevenuePerUser: 8.33, // $49.99/yr / 6 months avg lifetime
}, 12);

// Output: 12-month projection with MRR growth
```

### LTV Calculation

```typescript
// Customer Lifetime Value calculation

interface LTVInputs {
  averageMonthlyRevenue: number;
  monthlyChurnRate: number;
  grossMargin: number; // After app store cut (0.70 for 30% cut)
}

function calculateLTV(inputs: LTVInputs): number {
  // LTV = (ARPU * Gross Margin) / Churn Rate
  const ltv = (inputs.averageMonthlyRevenue * inputs.grossMargin) / inputs.monthlyChurnRate;
  return Math.round(ltv * 100) / 100;
}

// Example:
const ltv = calculateLTV({
  averageMonthlyRevenue: 8.33, // $49.99/yr = $4.17/mo
  monthlyChurnRate: 0.08,
  grossMargin: 0.70, // After Apple's 30%
});

// LTV = ($4.17 * 0.70) / 0.08 = $36.49

// For CAC comparison:
// LTV:CAC ratio should be > 3:1
// If LTV is $36.49, max CAC is ~$12
```

### Breakeven Analysis

```typescript
interface BreakevenInputs {
  fixedCosts: number; // Monthly (hosting, tools, etc.)
  variableCostPerSubscriber: number; // Support, etc.
  averageRevenuePerSubscriber: number;
  grossMargin: number;
}

function calculateBreakeven(inputs: BreakevenInputs): number {
  // Subscribers needed to break even
  const contributionMargin =
    (inputs.averageRevenuePerSubscriber * inputs.grossMargin) -
    inputs.variableCostPerSubscriber;

  const breakevenSubscribers = inputs.fixedCosts / contributionMargin;
  return Math.ceil(breakevenSubscribers);
}

// Example:
const breakeven = calculateBreakeven({
  fixedCosts: 500, // $500/mo for hosting, RevenueCat, etc.
  variableCostPerSubscriber: 0.10, // Support costs
  averageRevenuePerSubscriber: 4.17, // $49.99/yr / 12
  grossMargin: 0.70,
});

// Need ~180 subscribers to break even on monthly costs
```

---

## Quick Reference Tables

### RevenueCat Plan Comparison

| Feature | Free | Starter | Pro | Scale |
|---------|------|---------|-----|-------|
| Price | $0 | $0 | $99/mo | Custom |
| MTR Limit | $2.5k | $2.5k | $25k | Unlimited |
| Revenue Fee | 0% | 0% | 0% | 0% |
| A/B Testing | No | Basic | Advanced | Advanced |
| Targeting | No | No | Yes | Yes |
| Charts | Basic | Full | Full | Full |
| Support | Community | Email | Priority | Dedicated |

For PRINTMAXX apps: Start with Free, move to Starter at $2.5k MTR, Pro at $25k MTR.

### Product Configuration Summary

| App | Monthly | Annual | Trial | Entitlement |
|-----|---------|--------|-------|-------------|
| PrayerLock | $9.99 | $49.99 | 7 days | premium |
| WalkToUnlock | $7.99 | $39.99 | 3 days | premium |
| StudyLock | $6.99 | $34.99 | 7 days | premium |

### Key Metrics Targets

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Trial Start Rate | >25% | <15% |
| Trial Conversion | >15% | <8% |
| Monthly Churn | <8% | >12% |
| LTV | >$30 | <$15 |
| LTV:CAC | >3:1 | <2:1 |

---

## Checklist: RevenueCat Optimization

### Initial Setup
- [ ] SDK configured with proper log levels
- [ ] User attributes set for segmentation
- [ ] Offerings created for all pricing tiers
- [ ] A/B test offerings created
- [ ] Entitlements linked to all products

### Paywall Optimization
- [ ] Paywall shows within first 3 sessions
- [ ] Annual plan highlighted as default
- [ ] Savings percentage displayed
- [ ] Trial length prominent in CTA
- [ ] Social proof included
- [ ] Features list shows clear value

### Analytics
- [ ] Funnel events tracked
- [ ] A/B test tracking implemented
- [ ] Dashboard configured with key charts
- [ ] Alerts set for churn spikes
- [ ] Weekly metrics review scheduled

### Testing
- [ ] All purchase flows tested in sandbox
- [ ] Trial start and conversion tested
- [ ] Restore purchases works
- [ ] Offline behavior verified
- [ ] Error states handled gracefully

### Go-Live
- [ ] Production API keys configured
- [ ] Debug logging disabled
- [ ] Webhooks configured (if using backend)
- [ ] Privacy policy updated
- [ ] App Store description includes subscription terms

---

Created: 2026-01-25
