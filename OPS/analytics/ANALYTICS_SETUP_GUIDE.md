# Analytics and Tracking Setup Guide

Complete guide to setting up analytics and tracking across all PRINTMAXX platforms.

---

## 1. Website Analytics

### GA4 Setup

**Step 1: Create GA4 Property**
1. Go to analytics.google.com
2. Admin > Create Property
3. Enter property name (e.g., "PRINTMAXX Site")
4. Select industry and business size
5. Choose "Web" as platform

**Step 2: Get Measurement ID**
- Format: G-XXXXXXXXXX
- Found in: Admin > Data Streams > Web > Measurement ID

**Step 3: Install in Next.js**

```typescript
// lib/analytics.ts
export const GA_TRACKING_ID = process.env.NEXT_PUBLIC_GA_ID;

export const pageview = (url: string) => {
  window.gtag('config', GA_TRACKING_ID, {
    page_path: url,
  });
};

export const event = ({ action, category, label, value }: {
  action: string;
  category: string;
  label: string;
  value?: number;
}) => {
  window.gtag('event', action, {
    event_category: category,
    event_label: label,
    value: value,
  });
};
```

**Step 4: Add Script**

In `_app.tsx` or `layout.tsx`:
```tsx
<Script
  src={`https://www.googletagmanager.com/gtag/js?id=${GA_TRACKING_ID}`}
  strategy="afterInteractive"
/>
<Script id="google-analytics" strategy="afterInteractive">
  {`
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', '${GA_TRACKING_ID}');
  `}
</Script>
```

### Key Events to Track

**Lead Capture:**
```typescript
// When email captured
trackEvent({
  action: 'lead_capture',
  category: 'conversion',
  label: 'email_signup',
  value: 5 // estimated lead value
});
```

**Lead Magnet Download:**
```typescript
trackEvent({
  action: 'download',
  category: 'lead_magnet',
  label: 'stack_generator'
});
```

**CTA Clicks:**
```typescript
trackEvent({
  action: 'click',
  category: 'cta',
  label: 'hero_get_started'
});
```

**Content Engagement:**
```typescript
trackEvent({
  action: 'scroll_depth',
  category: 'engagement',
  label: '50_percent',
  value: 50
});
```

### Conversions Setup

In GA4:
1. Admin > Events
2. Find event (e.g., lead_capture)
3. Toggle "Mark as conversion"

**Recommended Conversions:**
- lead_capture (email signups)
- download (lead magnets)
- purchase (if applicable)
- sign_up (account creation)

### UTM Strategy

**Standard Parameters:**
- `utm_source`: Where traffic comes from (twitter, google, email)
- `utm_medium`: Type of traffic (organic, cpc, email, social)
- `utm_campaign`: Campaign name (launch_jan, black_friday)
- `utm_content`: Specific content (thread_1, bio_link)
- `utm_term`: Keywords (for paid search)

**Example URLs:**
```
printmaxx.com?utm_source=twitter&utm_medium=organic&utm_campaign=content_202501&utm_content=thread_1
printmaxx.com?utm_source=newsletter&utm_medium=email&utm_campaign=welcome_sequence&utm_content=email_3
```

**UTM Tracking Sheet (LEDGER/UTM_MASTER.csv):**
```csv
short_code,full_url,source,medium,campaign,content,created,status
tw1,printmaxx.com/...?utm_...,twitter,organic,content_202501,thread_1,2025-01-15,active
```

---

## 2. App Analytics

### RevenueCat Setup

**Step 1: Create Account**
1. Go to revenuecat.com
2. Create project for each app
3. Add app platforms (iOS, Android)

**Step 2: Install SDK**

```bash
npm install react-native-purchases
```

**Step 3: Initialize**

```typescript
import Purchases from 'react-native-purchases';

// Initialize on app start
Purchases.configure({ apiKey: 'YOUR_API_KEY' });
```

**Step 4: Track Key Events**

```typescript
// Purchase event
const { customerInfo } = await Purchases.purchasePackage(package);

// Check subscription status
const customerInfo = await Purchases.getCustomerInfo();
const isPremium = customerInfo.entitlements.active['premium'] !== undefined;
```

**Key Metrics in Dashboard:**
- MRR (Monthly Recurring Revenue)
- Active Subscribers
- Trial Conversion Rate
- Churn Rate
- LTV (Lifetime Value)

### Firebase Analytics

**Step 1: Add Firebase**

```bash
npm install @react-native-firebase/app @react-native-firebase/analytics
```

**Step 2: Track Events**

```typescript
import analytics from '@react-native-firebase/analytics';

// Screen view
await analytics().logScreenView({
  screen_name: 'HomeScreen',
  screen_class: 'HomeScreen',
});

// Custom events
await analytics().logEvent('feature_used', {
  feature_name: 'timer',
  duration: 25
});

// User properties
await analytics().setUserProperties({
  plan_type: 'premium',
  signup_source: 'organic'
});
```

**Standard Events to Track:**

```typescript
// Onboarding
analytics().logEvent('onboarding_start');
analytics().logEvent('onboarding_step', { step: 1, step_name: 'welcome' });
analytics().logEvent('onboarding_complete');

// Feature usage
analytics().logEvent('timer_started', { duration: 25, mode: 'focus' });
analytics().logEvent('timer_completed', { duration: 25, mode: 'focus' });

// Monetization
analytics().logEvent('paywall_view', { trigger: 'feature_gate' });
analytics().logEvent('purchase_started', { product_id: 'premium_monthly' });
analytics().logEvent('purchase_complete', { product_id: 'premium_monthly', value: 9.99 });
```

### Funnel Analysis Setup

**Essential Funnels:**

**Onboarding Funnel:**
1. app_open (first_open)
2. onboarding_step_1
3. onboarding_step_2
4. onboarding_complete
5. first_feature_use

**Subscription Funnel:**
1. paywall_view
2. product_selected
3. purchase_started
4. purchase_complete

**Engagement Funnel:**
1. session_start
2. core_feature_used
3. session_end (with engagement time)

---

## 3. Social Analytics

### Platform-Native Analytics

**Twitter/X Analytics:**
- Access: analytics.twitter.com
- Key metrics: Impressions, engagement rate, link clicks, profile visits
- Export: CSV download available

**TikTok Analytics:**
- Access: Creator tools in app or tiktok.com/analytics
- Key metrics: Views, watch time, shares, profile views
- Requires 100+ followers for full access

**Instagram Analytics:**
- Access: Professional dashboard in app
- Key metrics: Reach, impressions, saves, shares, profile visits
- Requires Business or Creator account

**YouTube Analytics:**
- Access: studio.youtube.com
- Key metrics: Watch time, CTR, retention, subscribers gained
- Most detailed native analytics

### Metrics That Matter Per Platform

| Platform | Primary Metric | Secondary | Ignore |
|----------|---------------|-----------|--------|
| Twitter/X | Link clicks | Replies, quotes | Impressions |
| TikTok | Watch time % | Shares, saves | Views alone |
| Instagram | Saves | Shares, DMs | Likes |
| YouTube | Watch time | CTR | Subscriber count |
| LinkedIn | Comments | Shares | Views |

**Why These Metrics:**
- **Link clicks** = actual traffic driven
- **Watch time %** = content quality signal
- **Saves** = high-intent engagement
- **Comments** = community building
- Views and likes are vanity metrics

### Third-Party Tools

**Free Options:**
| Tool | Best For | Limitations |
|------|----------|-------------|
| Buffer Analytics | Multi-platform overview | Basic metrics only |
| Creator Studio | Facebook/Instagram | Platform-locked |
| TweetDeck | Twitter monitoring | No historical data |
| Hootsuite Free | Scheduling + basic stats | 2 accounts max |

**Paid Options:**
| Tool | Price | Best For |
|------|-------|----------|
| Sprout Social | $249/mo | Agency-level reporting |
| Hootsuite Pro | $99/mo | Multi-account management |
| Hypefury | $29/mo | Twitter growth + analytics |
| Shield | $15/mo | LinkedIn analytics |

**Recommendation for Bootstrap:**
1. Start with native analytics (free)
2. Add Hypefury for Twitter if primary channel ($29/mo)
3. Use Buffer free tier for scheduling
4. Graduate to Sprout Social when revenue supports it

### Reporting Cadence

**Daily (5 min):**
- Check notifications and replies
- Note any viral content
- Track link clicks from posts

**Weekly (30 min):**
- Export key metrics to tracking sheet
- Identify top performing content
- Note content types that worked
- Plan next week's content angles

**Monthly (1 hour):**
- Full platform review
- Follower growth trends
- Engagement rate trends
- Content pillar performance
- Adjust strategy based on data

---

## 4. Email Analytics

### Key Metrics to Track

| Metric | Formula | What It Tells You |
|--------|---------|-------------------|
| Open Rate | Opens / Delivered | Subject line effectiveness |
| Click Rate | Clicks / Delivered | Content relevance |
| CTOR | Clicks / Opens | Email content quality |
| Unsubscribe Rate | Unsubs / Delivered | List-message fit |
| Bounce Rate | Bounces / Sent | List health |
| Spam Rate | Spam reports / Delivered | Sender reputation |
| Reply Rate | Replies / Delivered | Engagement quality |

### Benchmarks by Email Type

| Email Type | Open Rate | Click Rate | CTOR |
|------------|-----------|------------|------|
| Welcome email | 50-60% | 15-25% | 30-40% |
| Newsletter | 20-30% | 2-5% | 10-15% |
| Product update | 25-35% | 5-10% | 15-25% |
| Promotional | 15-25% | 1-3% | 5-10% |
| Re-engagement | 10-15% | 1-2% | 5-10% |
| Transactional | 60-80% | 10-20% | 15-25% |

### A/B Testing Setup

**What to Test (Priority Order):**
1. Subject lines (highest impact)
2. Send time
3. From name
4. Preview text
5. CTA button text
6. Email length
7. Personalization

**A/B Test Tracking (LEDGER/EMAIL_AB_TESTS.csv):**
```csv
test_id,date,test_type,variant_a,variant_b,metric,result_a,result_b,winner,significance,learnings
001,2025-01-20,subject,5 ways to automate,I saved 10 hours,open_rate,24%,31%,B,95%,Specific outcomes beat lists
```

### List Health Metrics

**Monitor Monthly:**
| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Bounce rate | <2% | 2-5% | >5% |
| Unsubscribe rate | <0.5% | 0.5-1% | >1% |
| Spam complaints | <0.1% | 0.1-0.3% | >0.3% |
| List growth rate | >5% | 0-5% | Negative |
| Inactive rate (90d) | <20% | 20-40% | >40% |

---

## 5. Attribution

### Multi-Touch Attribution Basics

**Attribution Models:**

| Model | How It Works | Best For |
|-------|--------------|----------|
| Last Click | 100% credit to final touchpoint | Direct response campaigns |
| First Click | 100% credit to first touchpoint | Understanding discovery |
| Linear | Equal credit to all touchpoints | Balanced view |
| Time Decay | More credit to recent touchpoints | Long sales cycles |
| Position Based | 40% first, 20% middle, 40% last | Balanced with emphasis |

**For Bootstrap Operations:**
Start with last-click attribution. It's simple and directionally correct. Graduate to multi-touch when you have enough data.

### UTM Strategy (Detailed)

**Naming Conventions:**

```
# Source values
google, bing, facebook, instagram, twitter, linkedin, tiktok, youtube
reddit, producthunt, newsletter, podcast, partner_[name]

# Medium values
organic, cpc, cpm, email, social, referral, affiliate, pr

# Campaign values
[initiative]_[date]_[variant]
Examples: launch_202501, black_friday_2025, blog_post_automation

# Content values
[format]_[position]_[variant]
Examples: thread_1, story_cta, bio_link, email_header_v2
```

### Pixel Setup

**Meta Pixel:**

```html
<script>
  !function(f,b,e,v,n,t,s)
  {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', 'YOUR_PIXEL_ID');
  fbq('track', 'PageView');
</script>
```

Track conversions:
```javascript
// Lead capture
fbq('track', 'Lead', {
  content_name: 'Newsletter Signup',
  content_category: 'email_capture'
});

// Purchase
fbq('track', 'Purchase', {
  value: 49.00,
  currency: 'USD'
});
```

**TikTok Pixel:**
```javascript
ttq.track('SubmitForm');
ttq.track('CompleteRegistration');
```

### Cross-Platform Tracking

**Unified Tracking Layer:**

```typescript
// lib/tracking.ts
interface TrackingEvent {
  name: string;
  properties?: Record<string, any>;
}

export const trackConversion = (event: TrackingEvent) => {
  const { name, properties } = event;

  // Google Analytics
  if (window.gtag) {
    window.gtag('event', name, properties);
  }

  // Meta Pixel
  if (window.fbq) {
    window.fbq('track', name, properties);
  }

  // TikTok Pixel
  if (window.ttq) {
    window.ttq.track(name, properties);
  }
};
```

---

## 6. Reporting Templates

### Weekly Metrics Report

```markdown
# Weekly Metrics Report
**Week of:** [DATE]

## Traffic Summary
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Sessions | | | |
| Users | | | |
| New Users | | | |
| Bounce Rate | | | |

## Top Traffic Sources
1. [Source] - [Sessions] - [Conversion Rate]
2. [Source] - [Sessions] - [Conversion Rate]
3. [Source] - [Sessions] - [Conversion Rate]

## Conversions
| Goal | Completions | Rate | vs Last Week |
|------|-------------|------|--------------|
| Lead Captures | | | |
| Lead Magnet Downloads | | | |

## Social Performance
| Platform | Followers | Impressions | Engagement | Link Clicks |
|----------|-----------|-------------|------------|-------------|
| Twitter | | | | |
| TikTok | | | | |

## Key Wins
-

## Next Week Focus
-
```

### Monthly Performance Review

Full template includes:
- Executive summary
- Traffic analysis by channel
- Conversion funnel analysis
- App metrics (if applicable)
- Social media performance
- Email performance
- Experiments and tests
- Key insights
- Recommendations

---

## 7. Tools Comparison

### Website Analytics

| Tool | Price | Best For |
|------|-------|----------|
| Google Analytics 4 | Free | Most use cases |
| Plausible | $9/mo | Privacy-focused, simple |
| Fathom | $14/mo | Privacy-focused, simple |
| Mixpanel | Free-$25/mo | Product analytics |

**Recommendation:** Start with GA4 (free). Add Plausible ($9/mo) if you want privacy-friendly.

### App Analytics

| Tool | Price | Best For |
|------|-------|----------|
| Firebase Analytics | Free | Basic app analytics |
| RevenueCat | Free-$50/mo | Subscription tracking |
| Mixpanel | Free-$25/mo | Event analytics |

**Recommendation:** Firebase Analytics (free) + RevenueCat (free tier) covers 90%.

### Attribution Tools

| Tool | Price | Best For |
|------|-------|----------|
| UTM + GA4 | Free | Basic attribution |
| Triple Whale | $129/mo | E-commerce |
| Hyros | $399/mo | High-ticket |

**Recommendation:** Start with UTM tracking + GA4. Attribution tools only make sense at $50k+/mo ad spend.

---

## Quick Start Checklist

**Day 1:**
- [ ] Create GA4 property
- [ ] Install tracking code on site
- [ ] Verify tracking is working
- [ ] Set up 3-5 key conversions

**Week 1:**
- [ ] Create UTM naming convention doc
- [ ] Set up Firebase Analytics in app (if applicable)
- [ ] Configure RevenueCat (if applicable)
- [ ] Create Looker Studio dashboard

**Month 1:**
- [ ] Implement all custom events
- [ ] Set up Meta and TikTok pixels (if using paid)
- [ ] Create weekly reporting template
- [ ] Run first weekly report

**Ongoing:**
- [ ] Weekly metrics review (Monday)
- [ ] Monthly performance review (1st week)
- [ ] Continuous test and learn

---

## Metrics That Actually Matter

Stop tracking vanity metrics. Focus on these:

**Website:**
- Conversion rate by source
- Time to conversion
- Cost per lead (if paid)

**App:**
- Day 1, 7, 30 retention
- Trial to paid conversion
- Revenue per user

**Social:**
- Link clicks per post
- Profile visits to follow rate
- Content to lead conversion

**Email:**
- Revenue per subscriber
- Reply rate
- Click-to-conversion rate

Everything else is context. These are decisions.

---

Last updated: 2026-01-23
