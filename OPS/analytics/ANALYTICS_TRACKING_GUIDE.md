# Analytics and Tracking Guide - PRINTMAXX Properties

Comprehensive guide for analytics implementation across apps, web, and social properties.

---

## Tool Comparison Matrix

### Web Analytics

| Tool | Price | Privacy | Best For | Limitations |
|------|-------|---------|----------|-------------|
| **Google Analytics 4** | Free | Low | Full-featured, free | Cookie consent required, data sampling at scale |
| **Plausible** | $9/mo | High | Privacy-focused, simple | No user-level data |
| **Fathom** | $14/mo | High | Privacy + custom events | Limited segmentation |
| **PostHog** | Free-$450/mo | Medium | Product analytics + session replay | Self-hosted complexity |
| **Simple Analytics** | $9/mo | High | Ultra-simple, EU-hosted | Very basic features |

**PRINTMAXX Recommendation:**
- **Primary:** GA4 (free, most features)
- **Secondary:** Plausible ($9/mo) for privacy-conscious audiences
- **When scaling:** PostHog for product analytics

### Product Analytics

| Tool | Price | Strength | Best For |
|------|-------|----------|----------|
| **Mixpanel** | Free-$25/mo | Event analytics, funnels | Tracking feature adoption |
| **Amplitude** | Free-$61/mo | Retention, cohort analysis | Understanding user behavior |
| **PostHog** | Free-$450/mo | Session replay + analytics | Debugging + insights |
| **Heap** | Custom | Auto-capture everything | Retroactive analysis |

**Feature Comparison:**

| Feature | Mixpanel | Amplitude | PostHog |
|---------|----------|-----------|---------|
| Event tracking | Yes | Yes | Yes |
| Funnel analysis | Yes | Yes | Yes |
| Retention cohorts | Yes | Yes (best) | Yes |
| Session replay | No | Yes (add-on) | Yes |
| Feature flags | No | Yes | Yes |
| A/B testing | No | Yes | Yes |
| Self-hostable | No | No | Yes |
| Free tier | 1M events/mo | 10M events/mo | 1M events/mo |

**PRINTMAXX Recommendation:** Mixpanel free tier for apps. Amplitude if heavy retention focus.

### Mobile Analytics

| Tool | Price | Specialty | Integration |
|------|-------|-----------|-------------|
| **Firebase Analytics** | Free | Full suite, Google ecosystem | Native + React Native |
| **Mixpanel** | Free-$25/mo | Event analytics | SDK available |
| **Amplitude** | Free-$61/mo | Retention analysis | SDK available |
| **AppsFlyer** | Free-$0.06/install | Attribution | SDK available |

**PRINTMAXX Recommendation:**
- **Free path:** Firebase Analytics + RevenueCat
- **Growth path:** Add Mixpanel for event depth

### Attribution Platforms

| Tool | Price | Best For | Features |
|------|-------|----------|----------|
| **AppsFlyer** | Free-$0.06/install | Mobile attribution | Deep linking, fraud prevention |
| **Adjust** | $500+/mo | Enterprise mobile | Privacy-focused, strong fraud |
| **Branch** | Free-$500/mo | Deep linking + attribution | Universal links |
| **Singular** | Custom | Multi-channel attribution | Marketing analytics |

**PRINTMAXX Recommendation:** AppsFlyer free tier (10K attributions/mo) to start.

---

## Implementation Guide

### 1. Next.js Web Analytics (GA4 + Privacy-First)

**File: `/lib/analytics.ts`**

```typescript
// Unified analytics layer
type AnalyticsProvider = 'ga4' | 'plausible' | 'posthog';

interface TrackEvent {
  name: string;
  properties?: Record<string, string | number | boolean>;
}

// Environment-based provider selection
const PROVIDER: AnalyticsProvider = (process.env.NEXT_PUBLIC_ANALYTICS_PROVIDER as AnalyticsProvider) || 'ga4';

// GA4 tracking
export const GA_TRACKING_ID = process.env.NEXT_PUBLIC_GA_ID;

export const pageview = (url: string) => {
  if (PROVIDER === 'ga4' && typeof window !== 'undefined' && window.gtag) {
    window.gtag('config', GA_TRACKING_ID, {
      page_path: url,
    });
  }

  if (PROVIDER === 'plausible' && typeof window !== 'undefined' && window.plausible) {
    // Plausible auto-tracks pageviews
  }
};

export const trackEvent = ({ name, properties }: TrackEvent) => {
  // GA4
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', name, properties);
  }

  // Plausible
  if (typeof window !== 'undefined' && window.plausible) {
    window.plausible(name, { props: properties });
  }

  // PostHog
  if (typeof window !== 'undefined' && window.posthog) {
    window.posthog.capture(name, properties);
  }
};

// Conversion tracking
export const trackConversion = (conversionType: string, value?: number) => {
  trackEvent({
    name: conversionType,
    properties: {
      conversion_type: conversionType,
      value: value || 0,
    },
  });

  // Meta Pixel
  if (typeof window !== 'undefined' && window.fbq) {
    window.fbq('track', conversionType, { value, currency: 'USD' });
  }
};
```

**File: `/app/layout.tsx`**

```tsx
import Script from 'next/script';
import { GA_TRACKING_ID } from '@/lib/analytics';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        {/* GA4 */}
        {GA_TRACKING_ID && (
          <>
            <Script
              src={`https://www.googletagmanager.com/gtag/js?id=${GA_TRACKING_ID}`}
              strategy="afterInteractive"
            />
            <Script id="google-analytics" strategy="afterInteractive">
              {`
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('config', '${GA_TRACKING_ID}', {
                  anonymize_ip: true,
                  cookie_flags: 'SameSite=None;Secure'
                });
              `}
            </Script>
          </>
        )}

        {/* Plausible (privacy-focused alternative) */}
        {process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN && (
          <Script
            defer
            data-domain={process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN}
            src="https://plausible.io/js/script.js"
          />
        )}
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### 2. React Native App Analytics

**File: `/src/lib/analytics.ts`**

```typescript
import analytics from '@react-native-firebase/analytics';
import Purchases from 'react-native-purchases';

// Event names following standard taxonomy
export const Events = {
  // Onboarding
  ONBOARDING_START: 'onboarding_start',
  ONBOARDING_STEP: 'onboarding_step',
  ONBOARDING_COMPLETE: 'onboarding_complete',

  // Core Features
  FEATURE_USED: 'feature_used',
  SESSION_START: 'session_start',
  SESSION_END: 'session_end',

  // Monetization
  PAYWALL_VIEW: 'paywall_view',
  PURCHASE_START: 'purchase_start',
  PURCHASE_COMPLETE: 'purchase_complete',
  PURCHASE_CANCEL: 'purchase_cancel',

  // Engagement
  SHARE: 'share',
  NOTIFICATION_OPEN: 'notification_open',
  DEEP_LINK_OPEN: 'deep_link_open',
} as const;

// User properties
export const setUserProperties = async (props: {
  plan_type?: 'free' | 'premium';
  signup_source?: string;
  app_version?: string;
}) => {
  await analytics().setUserProperties(props);
};

// Screen tracking
export const trackScreen = async (screenName: string, screenClass?: string) => {
  await analytics().logScreenView({
    screen_name: screenName,
    screen_class: screenClass || screenName,
  });
};

// Event tracking
export const trackEvent = async (
  eventName: string,
  params?: Record<string, string | number | boolean>
) => {
  await analytics().logEvent(eventName, params);
};

// Onboarding tracking
export const trackOnboarding = {
  start: () => trackEvent(Events.ONBOARDING_START),
  step: (stepNumber: number, stepName: string) =>
    trackEvent(Events.ONBOARDING_STEP, { step: stepNumber, step_name: stepName }),
  complete: (totalSteps: number) =>
    trackEvent(Events.ONBOARDING_COMPLETE, { total_steps: totalSteps }),
};

// Feature usage tracking
export const trackFeature = async (
  featureName: string,
  duration?: number,
  metadata?: Record<string, any>
) => {
  await trackEvent(Events.FEATURE_USED, {
    feature_name: featureName,
    duration_seconds: duration || 0,
    ...metadata,
  });
};

// Monetization tracking
export const trackMonetization = {
  paywallView: (trigger: string, productIds: string[]) =>
    trackEvent(Events.PAYWALL_VIEW, {
      trigger,
      products_shown: productIds.join(','),
    }),

  purchaseStart: (productId: string, price: number) =>
    trackEvent(Events.PURCHASE_START, {
      product_id: productId,
      price,
    }),

  purchaseComplete: (productId: string, price: number, transactionId: string) =>
    trackEvent(Events.PURCHASE_COMPLETE, {
      product_id: productId,
      price,
      transaction_id: transactionId,
    }),

  purchaseCancel: (productId: string, reason?: string) =>
    trackEvent(Events.PURCHASE_CANCEL, {
      product_id: productId,
      cancel_reason: reason || 'unknown',
    }),
};
```

### 3. RevenueCat Integration

**File: `/src/lib/purchases.ts`**

```typescript
import Purchases, { CustomerInfo, PurchasesPackage } from 'react-native-purchases';
import { trackMonetization } from './analytics';

const REVENUECAT_API_KEY = process.env.REVENUECAT_API_KEY!;

export const initPurchases = async () => {
  Purchases.setDebugLogsEnabled(__DEV__);
  await Purchases.configure({ apiKey: REVENUECAT_API_KEY });
};

export const getOfferings = async () => {
  try {
    const offerings = await Purchases.getOfferings();
    return offerings.current;
  } catch (error) {
    console.error('Error fetching offerings:', error);
    return null;
  }
};

export const purchasePackage = async (pkg: PurchasesPackage) => {
  try {
    trackMonetization.purchaseStart(
      pkg.product.identifier,
      pkg.product.price
    );

    const { customerInfo } = await Purchases.purchasePackage(pkg);

    trackMonetization.purchaseComplete(
      pkg.product.identifier,
      pkg.product.price,
      customerInfo.originalAppUserId
    );

    return { success: true, customerInfo };
  } catch (error: any) {
    if (!error.userCancelled) {
      trackMonetization.purchaseCancel(
        pkg.product.identifier,
        error.message
      );
    }
    return { success: false, error };
  }
};

export const checkSubscriptionStatus = async (): Promise<{
  isSubscribed: boolean;
  expirationDate?: Date;
}> => {
  const customerInfo = await Purchases.getCustomerInfo();
  const entitlement = customerInfo.entitlements.active['premium'];

  return {
    isSubscribed: !!entitlement,
    expirationDate: entitlement?.expirationDate
      ? new Date(entitlement.expirationDate)
      : undefined,
  };
};
```

---

## Event Taxonomy

### Standard Event Naming Convention

**Format:** `{category}_{action}` (snake_case, lowercase)

| Category | Actions | Example |
|----------|---------|---------|
| onboarding | start, step, complete, skip | `onboarding_complete` |
| screen | view | `screen_view` |
| feature | used, started, completed | `feature_used` |
| paywall | view, dismiss | `paywall_view` |
| purchase | start, complete, cancel, restore | `purchase_complete` |
| subscription | start_trial, convert, cancel, renew | `subscription_convert` |
| content | view, scroll, complete | `content_complete` |
| share | click, complete | `share_complete` |
| notification | receive, open, dismiss | `notification_open` |
| error | occur | `error_occur` |

### Event Properties Schema

**User Properties (set once per user):**
```json
{
  "user_id": "string (hashed)",
  "signup_date": "ISO date",
  "signup_source": "organic|paid|referral",
  "plan_type": "free|premium",
  "app_version": "1.0.0",
  "device_type": "phone|tablet",
  "os_version": "iOS 17.0"
}
```

**Event Properties (per event):**
```json
{
  "event_timestamp": "ISO datetime",
  "session_id": "uuid",
  "screen_name": "current screen",
  "feature_name": "specific feature",
  "duration_seconds": "number",
  "success": "boolean",
  "error_code": "string (if applicable)"
}
```

### PRINTMAXX App Events

**PrayerLock Events:**
```typescript
const PrayerLockEvents = {
  // Onboarding
  'onboarding_start': {},
  'onboarding_step': { step: number, step_name: string },
  'onboarding_complete': { total_steps: number },

  // Timer
  'timer_start': { duration: number, mode: 'focus' | 'break' },
  'timer_complete': { duration: number, mode: string },
  'timer_cancel': { time_remaining: number },

  // Scripture
  'scripture_view': { verse_id: string },
  'scripture_save': { verse_id: string },
  'scripture_share': { verse_id: string },

  // Streak
  'streak_check': { current_streak: number },
  'streak_milestone': { milestone: number },

  // Paywall
  'paywall_view': { trigger: string },
  'paywall_dismiss': {},
  'purchase_start': { product_id: string },
  'purchase_complete': { product_id: string, price: number },
};
```

**WalkToUnlock Events:**
```typescript
const WalkToUnlockEvents = {
  // Steps
  'steps_goal_set': { goal: number },
  'steps_recorded': { count: number, source: 'healthkit' | 'manual' },
  'steps_goal_reached': { goal: number, actual: number },

  // Lock Screen
  'lock_enabled': {},
  'lock_disabled': {},
  'unlock_attempt': { steps_current: number, steps_required: number },
  'unlock_success': {},

  // Health Permissions
  'health_permission_request': {},
  'health_permission_granted': {},
  'health_permission_denied': {},
};
```

### Web Events (Landing Site)

```typescript
const WebEvents = {
  // Page Engagement
  'page_view': { page_path: string, referrer: string },
  'scroll_depth': { depth_percent: 25 | 50 | 75 | 100 },
  'time_on_page': { seconds: number },

  // Lead Capture
  'form_start': { form_name: string },
  'form_submit': { form_name: string, email_domain: string },
  'form_error': { form_name: string, error_type: string },

  // Lead Magnets
  'magnet_view': { magnet_id: string },
  'magnet_download': { magnet_id: string },

  // CTA Clicks
  'cta_click': { cta_id: string, cta_text: string, position: string },

  // Blog
  'article_start': { article_slug: string },
  'article_complete': { article_slug: string, read_time: number },
};
```

---

## Dashboard Setup

### GA4 Custom Dashboards

**Explorations to Create:**

1. **Conversion Funnel**
   - Steps: page_view > form_start > form_submit
   - Breakdown by: source/medium, device, page

2. **Content Performance**
   - Metrics: scroll_depth, time_on_page
   - Dimensions: page_path, article_slug

3. **Lead Source Analysis**
   - Metrics: form_submit count
   - Dimensions: utm_source, utm_medium, utm_campaign

### Looker Studio Dashboard Template

**Dashboard Sections:**

1. **Traffic Overview**
   - Sessions by day (line chart)
   - Users by source (pie chart)
   - Top pages by views (table)

2. **Conversion Metrics**
   - Conversion rate by source (bar chart)
   - Lead captures by day (line chart)
   - Funnel visualization

3. **Content Engagement**
   - Avg time on page by content type
   - Scroll depth distribution
   - Top performing articles

4. **Campaign Performance**
   - UTM campaign breakdown
   - Cost per lead (if tracking)
   - Conversion by content variant

### RevenueCat Dashboard

**Key Charts to Monitor:**

| Chart | Purpose | Frequency |
|-------|---------|-----------|
| MRR | Revenue health | Daily |
| Trial Conversion | Paywall effectiveness | Weekly |
| Churn Rate | Retention health | Weekly |
| LTV | Customer value | Monthly |
| Realization | Price optimization | Monthly |

---

## Privacy Compliance

### GDPR Requirements

**What You Need:**

1. **Cookie Consent Banner** (for EU users)
```tsx
// Component: CookieConsent.tsx
'use client';

import { useState, useEffect } from 'react';

export function CookieConsent() {
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem('analytics_consent');
    if (!consent) setShowBanner(true);
  }, []);

  const acceptCookies = () => {
    localStorage.setItem('analytics_consent', 'accepted');
    // Initialize analytics only after consent
    window.gtag('consent', 'update', {
      analytics_storage: 'granted',
    });
    setShowBanner(false);
  };

  const declineCookies = () => {
    localStorage.setItem('analytics_consent', 'declined');
    window.gtag('consent', 'update', {
      analytics_storage: 'denied',
    });
    setShowBanner(false);
  };

  if (!showBanner) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-gray-900 p-4 z-50">
      <div className="max-w-4xl mx-auto flex items-center justify-between">
        <p className="text-white text-sm">
          We use cookies to analyze site traffic. See our{' '}
          <a href="/privacy" className="underline">Privacy Policy</a>.
        </p>
        <div className="flex gap-2">
          <button onClick={declineCookies} className="px-4 py-2 text-white">
            Decline
          </button>
          <button onClick={acceptCookies} className="px-4 py-2 bg-white text-black rounded">
            Accept
          </button>
        </div>
      </div>
    </div>
  );
}
```

2. **GA4 Consent Mode Setup**
```javascript
// Add before GA4 script
gtag('consent', 'default', {
  'analytics_storage': 'denied',
  'ad_storage': 'denied',
  'wait_for_update': 500
});
```

3. **Required Documentation**
   - Privacy Policy (link in footer)
   - Cookie Policy (explain what you track)
   - Data retention policy (GA4 default: 14 months)

### CCPA Requirements (California)

1. **Do Not Sell Link**
   - Add "Do Not Sell My Personal Information" link in footer
   - Implement opt-out mechanism

2. **Privacy Rights**
   - Right to know what data is collected
   - Right to delete data
   - Right to opt-out of sale

### App Store Privacy Requirements

**iOS App Privacy Labels**

Must disclose:
- Data types collected
- How data is linked to user
- Whether data is used for tracking

**Categories for PRINTMAXX apps:**

| Data Type | Linked to User | Used for Tracking |
|-----------|----------------|-------------------|
| Usage Data | Yes | No |
| Diagnostics | No | No |
| Purchases | Yes | No |

### Privacy-First Alternative Stack

If privacy compliance is primary concern:

| Layer | Tool | Why |
|-------|------|-----|
| Web Analytics | Plausible | No cookies, GDPR-compliant |
| App Analytics | Firebase (anonymized) | Google ecosystem, configurable |
| Product Analytics | PostHog (self-hosted) | Full data control |
| Attribution | First-party UTMs only | No third-party tracking |

**Cost:** ~$9/mo (Plausible) vs $0 (GA4)
**Compliance:** No cookie banner needed with Plausible

---

## Attribution Setup

### UTM Parameter Strategy

**Standard Parameters:**
```
utm_source    = where traffic originates (twitter, google, email)
utm_medium    = marketing medium (organic, cpc, email, social)
utm_campaign  = campaign identifier (launch_jan26, welcome_seq)
utm_content   = specific content piece (thread_1, bio_link, cta_hero)
utm_term      = paid search keywords (optional)
```

**PRINTMAXX UTM Template:**

| Source | Medium | Campaign Format | Content Format |
|--------|--------|-----------------|----------------|
| twitter | organic | {initiative}_{yyyymm} | thread_{n}, bio, reply |
| tiktok | organic | {initiative}_{yyyymm} | video_{n}, bio |
| email | email | {sequence}_{position} | cta_{position} |
| google | cpc | {offer}_{yyyymm} | ad_{variant} |
| producthunt | referral | launch_{date} | listing |

**Example URLs:**
```
https://printmaxx.com?utm_source=twitter&utm_medium=organic&utm_campaign=content_202601&utm_content=thread_1
https://printmaxx.com?utm_source=email&utm_medium=email&utm_campaign=welcome_3&utm_content=cta_main
```

### App Attribution (AppsFlyer Setup)

**Install SDK:**
```bash
npm install react-native-appsflyer
```

**Initialize:**
```typescript
import appsFlyer from 'react-native-appsflyer';

const initAppsFlyer = () => {
  appsFlyer.initSdk({
    devKey: 'YOUR_DEV_KEY',
    isDebug: __DEV__,
    appId: 'YOUR_APP_ID', // iOS only
    onInstallConversionDataListener: true,
  });
};

// Track in-app events
appsFlyer.logEvent('af_subscribe', {
  af_revenue: 9.99,
  af_currency: 'USD',
  af_content_id: 'premium_monthly',
});
```

**Key Events for Attribution:**
```typescript
const AttributionEvents = {
  // Standard AppsFlyer events
  'af_complete_registration': {},
  'af_subscribe': { af_revenue: number, af_currency: string },
  'af_start_trial': {},
  'af_purchase': { af_revenue: number, af_content_id: string },
};
```

### Deep Linking for Attribution

**Branch.io Setup (if using):**
```typescript
import branch from 'react-native-branch';

// Handle deep link
branch.subscribe(({ error, params }) => {
  if (params['+clicked_branch_link']) {
    // User came from Branch link
    const campaign = params['campaign'];
    const source = params['channel'];
    trackEvent('deep_link_open', { campaign, source });
  }
});
```

---

## Key Metrics by Property

### Apps (PrayerLock, WalkToUnlock, StudyLock)

| Metric | Formula | Target | Priority |
|--------|---------|--------|----------|
| **D1 Retention** | Users active Day 1 / Installs | >40% | High |
| **D7 Retention** | Users active Day 7 / Installs | >20% | High |
| **D30 Retention** | Users active Day 30 / Installs | >10% | High |
| **Trial Start Rate** | Trial starts / Installs | >15% | High |
| **Trial Conversion** | Subscribed / Trial starts | >30% | Critical |
| **MRR** | Monthly Recurring Revenue | Track growth | Critical |
| **Churn Rate** | Cancellations / Active subs | <5%/mo | Critical |
| **LTV** | Revenue / Total customers | >$20 | Medium |
| **CAC** | Ad spend / Installs | <LTV/3 | Medium |

### Website (PRINTMAXX Landing)

| Metric | Formula | Target | Priority |
|--------|---------|--------|----------|
| **Lead Capture Rate** | Email signups / Unique visitors | >3% | Critical |
| **Bounce Rate** | Single-page sessions / Total | <60% | Medium |
| **Avg Session Duration** | Total time / Sessions | >2 min | Medium |
| **Pages per Session** | Pageviews / Sessions | >2 | Low |
| **Scroll Depth (75%)** | Scrolled 75%+ / Total | >30% | Medium |
| **CTA Click Rate** | CTA clicks / Impressions | >5% | High |

### Email

| Metric | Formula | Target | Priority |
|--------|---------|--------|----------|
| **Open Rate** | Opens / Delivered | >25% | Medium |
| **Click Rate** | Clicks / Delivered | >3% | High |
| **Unsubscribe Rate** | Unsubs / Delivered | <0.5% | High |
| **Reply Rate** | Replies / Delivered | >1% | High |
| **Revenue per Email** | Revenue / Emails sent | Track trend | High |

---

## Implementation Checklist

### Phase 1: Foundation (Week 1)

- [ ] Create GA4 property for website
- [ ] Install GA4 tracking code in Next.js
- [ ] Set up basic conversions (lead_capture, download)
- [ ] Create UTM naming convention document
- [ ] Install Firebase Analytics in app
- [ ] Configure RevenueCat for subscription tracking

### Phase 2: Events (Week 2)

- [ ] Implement all standard events per taxonomy
- [ ] Set up user properties
- [ ] Create onboarding funnel tracking
- [ ] Add paywall and purchase events
- [ ] Test all events in debug mode

### Phase 3: Dashboards (Week 3)

- [ ] Build GA4 Explorations
- [ ] Create Looker Studio dashboard
- [ ] Set up RevenueCat charts
- [ ] Create weekly metrics template
- [ ] Set up automated reports (email)

### Phase 4: Privacy (Week 4)

- [ ] Implement cookie consent banner
- [ ] Configure GA4 consent mode
- [ ] Update Privacy Policy
- [ ] Add App Store privacy labels
- [ ] Test GDPR/CCPA flows

### Phase 5: Attribution (Month 2)

- [ ] Set up AppsFlyer (if needed)
- [ ] Implement UTM tracking across all channels
- [ ] Create attribution report
- [ ] Set up deep linking (if needed)
- [ ] Track CAC by channel

---

## Quick Reference

### Event Naming

```
{category}_{action}

Categories: onboarding, screen, feature, paywall, purchase, subscription,
            content, share, notification, error

Actions: start, step, complete, skip, view, used, click, dismiss,
         open, receive, cancel, restore
```

### GA4 Key Conversions

```
lead_capture      - Email signup
download          - Lead magnet download
sign_up           - Account creation
purchase          - Any purchase
subscribe         - Subscription start
```

### RevenueCat Key Events

```
initial_purchase  - First subscription
trial_started     - Trial begins
trial_converted   - Trial to paid
expiration        - Subscription ends
renewal           - Subscription renews
```

### Privacy Checklist

```
[ ] Cookie consent banner (EU)
[ ] Do Not Sell link (California)
[ ] Privacy Policy updated
[ ] Data retention configured
[ ] App Store privacy labels
[ ] Consent mode enabled
```

---

Last updated: 2026-01-25
