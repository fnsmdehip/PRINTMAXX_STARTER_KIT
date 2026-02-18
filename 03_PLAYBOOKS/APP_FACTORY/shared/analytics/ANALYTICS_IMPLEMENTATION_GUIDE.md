# Analytics Implementation Guide

Production-ready analytics for React Native apps. This guide covers event tracking, funnel setup, dashboard configuration, and KPI definitions.

## Quick start

```tsx
// App.tsx
import { AnalyticsProvider } from './shared/analytics';

const analyticsConfig = {
  providers: {
    mixpanel: { apiKey: process.env.MIXPANEL_TOKEN },
    posthog: { apiKey: process.env.POSTHOG_KEY },
    firebase: {},
    revenuecat: { apiKey: process.env.REVENUECAT_KEY },
  },
  debug: __DEV__,
  sessionTimeout: 30 * 60 * 1000, // 30 minutes
};

export default function App() {
  return (
    <AnalyticsProvider config={analyticsConfig}>
      <YourApp />
    </AnalyticsProvider>
  );
}
```

```tsx
// Any component
import { useAnalytics } from './shared/analytics';

function FeatureScreen() {
  const { track, trackScreen } = useAnalytics();

  useEffect(() => {
    trackScreen('FeatureScreen');
  }, []);

  const handleAction = async () => {
    await track('feature_used', {
      feature_name: 'export',
      usage_count: 1,
    });
  };

  return <Button onPress={handleAction}>Export</Button>;
}
```

---

## Events by app type

### Utility app (one-time use)

Focus on activation and feature discovery.

**Critical events:**
- `onboarding_completed` - Did they finish setup?
- `feature_used` - Are they using core features?
- `paywall_viewed` - Did they see the upgrade option?
- `purchase_completed` - Did they convert?

**Recommended funnels:**
1. Install -> Onboarding Complete -> First Feature Use -> Purchase
2. Paywall View -> Product Select -> Purchase Complete

### Habit/daily use app

Focus on retention and engagement loops.

**Critical events:**
- `session_started` - Daily active tracking
- `streak_achieved` / `streak_broken` - Habit formation
- `notification_opened` - Re-engagement effectiveness
- `milestone_reached` - Progress tracking

**Recommended funnels:**
1. Day 1 Active -> Day 7 Active -> Day 30 Active
2. Notification Sent -> Opened -> Session Started

### Content/creation app

Focus on content creation flow and sharing.

**Critical events:**
- `content_created` - Core value delivery
- `content_saved` - Commitment signal
- `content_shared` - Viral loop
- `feature_completed` - Task completion

**Recommended funnels:**
1. Screen View -> Content Started -> Content Saved -> Shared
2. Template Selected -> Customized -> Exported

### Subscription app

Focus on trial conversion and retention.

**Critical events:**
- `trial_started` - Free trial begins
- `purchase_completed` - Conversion
- `subscription_renewed` - Retention
- `subscription_cancelled` - Churn signal

**Recommended funnels:**
1. Paywall View -> Trial Start -> Trial End -> Purchase
2. Active User -> Cancellation -> Win-back Attempt

---

## Funnel setup guide

### Mixpanel funnels

```javascript
// Mixpanel funnel definition
const onboardingFunnel = {
  name: 'Onboarding Completion',
  steps: [
    { event: 'onboarding_started' },
    { event: 'onboarding_screen_viewed', where: 'screen_index == 0' },
    { event: 'onboarding_screen_viewed', where: 'screen_index == 1' },
    { event: 'permission_granted', where: 'permission_type == "notifications"' },
    { event: 'onboarding_completed' },
  ],
  conversionWindow: 7 * 24, // 7 days in hours
};

const purchaseFunnel = {
  name: 'Purchase Conversion',
  steps: [
    { event: 'paywall_viewed' },
    { event: 'product_selected' },
    { event: 'purchase_initiated' },
    { event: 'purchase_completed' },
  ],
  conversionWindow: 24, // 24 hours
};
```

### PostHog funnels

```javascript
// PostHog funnel via API
const createFunnel = {
  name: 'Activation Funnel',
  filters: {
    events: [
      { id: 'session_started', type: 'events' },
      { id: 'feature_used', type: 'events' },
      { id: 'content_created', type: 'events' },
    ],
    funnel_window_days: 7,
    breakdown_type: 'person',
    breakdown: 'platform',
  },
};
```

### Key funnel metrics

| Funnel | Target Conversion | Alert Threshold |
|--------|-------------------|-----------------|
| Onboarding | > 70% | < 50% |
| Activation (D1) | > 40% | < 25% |
| Trial to Paid | > 20% | < 10% |
| Paywall to Purchase | > 5% | < 2% |
| Notification to Session | > 15% | < 8% |

---

## Dashboard templates

### Executive dashboard

**Metrics to display:**

1. **DAU/WAU/MAU** - Active user counts
2. **Revenue** - MRR, ARR, new MRR, churned MRR
3. **Conversion rate** - Trial to paid
4. **Retention** - D1, D7, D30 curves
5. **Acquisition** - Installs by source

### Product dashboard

**Metrics to display:**

1. **Feature adoption** - % users using each feature
2. **Session metrics** - Duration, depth, frequency
3. **Onboarding completion** - Step-by-step drop-off
4. **Error rates** - By type and screen
5. **User flows** - Common paths through app

### Growth dashboard

**Metrics to display:**

1. **Acquisition funnel** - Install to activation
2. **Referral metrics** - K-factor, viral coefficient
3. **Notification performance** - Open rates, conversion
4. **Paywall performance** - View to purchase by variant
5. **Cohort retention** - By acquisition source

---

## KPI definitions

### Acquisition KPIs

| Metric | Definition | Calculation |
|--------|------------|-------------|
| **CAC** | Customer Acquisition Cost | Total ad spend / New customers |
| **Install Rate** | Store page to install | Installs / Store impressions |
| **Onboarding Rate** | Install to onboarding complete | Onboarding completed / Installs |

### Activation KPIs

| Metric | Definition | Calculation |
|--------|------------|-------------|
| **Activation Rate** | New users hitting aha moment | Activated users / New users |
| **Time to Activate** | Hours from install to activation | Avg(activation_time - install_time) |
| **D1 Retention** | Users returning day after install | D1 active / D0 installs |

### Retention KPIs

| Metric | Definition | Calculation |
|--------|------------|-------------|
| **D7 Retention** | Users active 7 days post-install | D7 active / D0 installs |
| **D30 Retention** | Users active 30 days post-install | D30 active / D0 installs |
| **WAU/MAU** | Stickiness ratio | Weekly active / Monthly active |
| **Churn Rate** | Users who stopped using app | Churned users / Active users |

### Revenue KPIs

| Metric | Definition | Calculation |
|--------|------------|-------------|
| **MRR** | Monthly Recurring Revenue | Sum of monthly subscriptions |
| **ARPU** | Average Revenue Per User | Total revenue / Total users |
| **ARPPU** | Avg Revenue Per Paying User | Total revenue / Paying users |
| **LTV** | Lifetime Value | ARPU * Avg customer lifespan |
| **Trial Conversion** | Free trial to paid | Paid conversions / Trial starts |
| **Renewal Rate** | Subscribers who renew | Renewals / Expiring subscriptions |

---

## Alert configurations

### Critical alerts (immediate notification)

```javascript
const criticalAlerts = [
  {
    name: 'Purchase failures spike',
    metric: 'purchase_failed',
    condition: 'count > 10 in 1 hour',
    channels: ['slack', 'pagerduty'],
  },
  {
    name: 'Crash rate increase',
    metric: 'crash_detected',
    condition: 'rate > 1% of sessions',
    channels: ['slack', 'pagerduty'],
  },
  {
    name: 'Revenue drop',
    metric: 'daily_revenue',
    condition: '< 50% of 7-day avg',
    channels: ['slack', 'email'],
  },
];
```

### Warning alerts (daily digest)

```javascript
const warningAlerts = [
  {
    name: 'Onboarding drop-off',
    metric: 'onboarding_completed / onboarding_started',
    condition: '< 60%',
  },
  {
    name: 'Trial conversion decline',
    metric: 'trial_conversion_rate',
    condition: '< 15%',
  },
  {
    name: 'D1 retention decline',
    metric: 'd1_retention',
    condition: '< 30%',
  },
  {
    name: 'Notification opt-out spike',
    metric: 'permission_denied (notifications)',
    condition: '> 50% of requests',
  },
];
```

---

## Implementation checklist

### Phase 1: Core events (Week 1)

- [ ] Install AnalyticsProvider at app root
- [ ] Add session tracking (automatic)
- [ ] Add screen view tracking (each screen)
- [ ] Add onboarding events
- [ ] Add error tracking

### Phase 2: Conversion events (Week 2)

- [ ] Add paywall view events
- [ ] Add purchase events
- [ ] Add trial events
- [ ] Connect RevenueCat

### Phase 3: Retention events (Week 3)

- [ ] Add streak tracking
- [ ] Add milestone events
- [ ] Add notification events
- [ ] Add feature usage events

### Phase 4: Dashboards (Week 4)

- [ ] Create Mixpanel/PostHog dashboards
- [ ] Configure alerts
- [ ] Set up weekly reports
- [ ] Document KPI targets

---

## SQL query templates

### Daily active users

```sql
SELECT
  DATE(timestamp) as date,
  COUNT(DISTINCT user_id) as dau
FROM events
WHERE event_name = 'session_started'
  AND timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(timestamp)
ORDER BY date;
```

### Onboarding funnel

```sql
WITH funnel AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'onboarding_started' THEN 1 ELSE 0 END) as step1,
    MAX(CASE WHEN event_name = 'permission_granted' THEN 1 ELSE 0 END) as step2,
    MAX(CASE WHEN event_name = 'onboarding_completed' THEN 1 ELSE 0 END) as step3
  FROM events
  WHERE timestamp >= CURRENT_DATE - INTERVAL '7 days'
  GROUP BY user_id
)
SELECT
  SUM(step1) as started,
  SUM(step2) as permissions,
  SUM(step3) as completed,
  ROUND(100.0 * SUM(step3) / NULLIF(SUM(step1), 0), 2) as conversion_rate
FROM funnel;
```

### Revenue by cohort

```sql
WITH cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('week', MIN(timestamp)) as cohort_week
  FROM events
  WHERE event_name = 'session_started'
  GROUP BY user_id
)
SELECT
  c.cohort_week,
  COUNT(DISTINCT c.user_id) as users,
  SUM(p.price) as revenue,
  ROUND(SUM(p.price) / COUNT(DISTINCT c.user_id), 2) as arpu
FROM cohorts c
LEFT JOIN events p ON c.user_id = p.user_id
  AND p.event_name = 'purchase_completed'
GROUP BY c.cohort_week
ORDER BY c.cohort_week;
```

### Retention curve

```sql
WITH first_seen AS (
  SELECT
    user_id,
    DATE(MIN(timestamp)) as first_date
  FROM events
  WHERE event_name = 'session_started'
  GROUP BY user_id
),
activity AS (
  SELECT
    f.user_id,
    f.first_date,
    DATE(e.timestamp) - f.first_date as days_since_first
  FROM first_seen f
  JOIN events e ON f.user_id = e.user_id
  WHERE e.event_name = 'session_started'
)
SELECT
  days_since_first as day,
  COUNT(DISTINCT user_id) as retained_users,
  ROUND(100.0 * COUNT(DISTINCT user_id) /
    (SELECT COUNT(DISTINCT user_id) FROM first_seen), 2) as retention_rate
FROM activity
WHERE days_since_first <= 30
GROUP BY days_since_first
ORDER BY days_since_first;
```

---

## Best practices

### Event naming

- Use snake_case for event names
- Use past tense for completed actions (`purchase_completed` not `purchase`)
- Be specific (`content_created` not `create`)
- Keep consistent across platforms

### Property naming

- Use snake_case for property names
- Use primitive types where possible (string, number, boolean)
- Avoid nested objects
- Keep property values under 100 characters

### Performance

- Batch events where possible
- Flush on app background
- Don't block UI on analytics
- Implement exponential backoff for retries

### Privacy

- Never track PII without consent
- Implement opt-out functionality
- Respect ATT (App Tracking Transparency)
- Document data retention policies

---

## Troubleshooting

### Events not appearing

1. Check API keys are correct
2. Verify network connectivity
3. Check debug mode is enabled
4. Verify event names match schema
5. Check for initialization errors

### Duplicate events

1. Check for multiple provider instances
2. Verify session management
3. Check component re-render behavior
4. Review event deduplication logic

### Missing user properties

1. Verify identify called before track
2. Check property name length limits
3. Verify value type compatibility
4. Check for async timing issues

---

## Resources

- [Mixpanel React Native SDK](https://developer.mixpanel.com/docs/react-native)
- [PostHog React Native SDK](https://posthog.com/docs/libraries/react-native)
- [Firebase Analytics RN](https://rnfirebase.io/analytics/usage)
- [RevenueCat SDK](https://docs.revenuecat.com/docs/reactnative)
