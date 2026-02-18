# Launch Metrics Dashboard

What to track, when to track it, and what the numbers mean.

---

## Launch day metrics

### Primary metrics (track hourly)

| Metric | Source | Target | Alert if |
|--------|--------|--------|----------|
| Downloads | App Store Connect / Google Play | - | 0 after 2 hours |
| Revenue | RevenueCat | - | No trials after 4 hours |
| Crash rate | Sentry / Crashlytics | < 1% | > 1% |
| App Store rating | Manual check | > 4.0 | < 3.0 |

### Secondary metrics (track every 2-4 hours)

| Metric | Source | Target | Alert if |
|--------|--------|--------|----------|
| Landing page visits | Analytics | - | < 50/hour with active promo |
| Email open rate | Email platform | > 40% | < 20% |
| Email click rate | Email platform | > 10% | < 3% |
| Social engagement | Manual / dashboards | - | Zero engagement on posts |
| Trial start rate | RevenueCat | > 30% of downloads | < 10% |

### Vanity metrics (nice to track, not critical)

| Metric | Why track |
|--------|-----------|
| Social followers gained | Indicates reach |
| Press mentions | For future outreach |
| DMs received | User interest signal |
| Shares/retweets | Organic spread |

---

## Alert thresholds

### Critical (action within 15 minutes)

| Condition | Action |
|-----------|--------|
| Crash rate > 5% | Investigate immediately, consider pulling update |
| App Store "Ready for Sale" → other status | Check App Store Connect |
| Payment errors spike | Check RevenueCat, contact support |
| Landing page down | Check hosting, restore from backup |

### Warning (action within 1 hour)

| Condition | Action |
|-----------|--------|
| Crash rate 1-5% | Investigate, prioritize fix |
| Zero downloads for 1 hour | Check app store listing visibility |
| Negative review | Respond immediately |
| High email bounce rate | Check list quality |

### Monitor (review end of day)

| Condition | Action |
|-----------|--------|
| Lower than expected downloads | Review marketing, not product |
| Trial conversion below target | Plan paywall experiment |
| Specific feature errors | Add to v1.1 fix list |

---

## Success criteria

### Launch day success

| Tier | Downloads | Revenue | Rating |
|------|-----------|---------|--------|
| Great | > 500 | > $500 | > 4.5 |
| Good | 100-500 | $100-500 | 4.0-4.5 |
| Okay | 25-100 | $25-100 | 3.5-4.0 |
| Below target | < 25 | < $25 | < 3.5 |

Note: These vary wildly by app type and marketing spend. Set your own realistic targets.

### First week success

| Metric | Target |
|--------|--------|
| Day 1 retention | > 40% |
| Day 7 retention | > 20% |
| Trial conversion | > 5% |
| Organic downloads trending | Up or stable |
| Review count | > 10 |
| Average rating | > 4.0 |

### First month success

| Metric | Target |
|--------|--------|
| MRR | $500+ (adjust for your app) |
| Day 30 retention | > 10% |
| Organic growth | 20%+ of downloads |
| Churn rate | < 10% monthly |
| Customer acquisition cost | < 50% of first-year LTV |

---

## Dashboard setup

### RevenueCat dashboard

**Key views:**
- Overview (MRR, active subscribers, trials)
- Charts: Revenue over time
- Charts: Trial conversion rate
- Events: Recent transactions

**Set up alerts for:**
- Revenue drops
- Subscription failures
- Refund spikes

### Analytics dashboard (Mixpanel/Amplitude/PostHog)

**Key views:**
- Real-time active users
- Event funnel: Open → Onboarding → Trial → Purchase
- Retention cohort chart
- Top events by count

**Set up alerts for:**
- Error events spike
- Funnel drop-off increase
- Session duration drop

### App Store Connect / Google Play Console

**Key views:**
- Downloads over time
- Downloads by source
- Conversion rate (impressions → downloads)
- Reviews and ratings

**Check manually:**
- New reviews (respond to all)
- App Store status
- Keyword rankings

### Crash reporting (Sentry/Crashlytics)

**Key views:**
- Crash-free rate
- Most common crashes
- Affected user count
- Device/OS distribution

**Set up alerts for:**
- Crash rate > 1%
- New crash type affecting > 10 users

---

## Metric tracking sheet

Copy this to your tracking tool (Notion, Google Sheets, etc.):

### Launch day log

| Time | Downloads | Revenue | Trials | Crashes | Reviews | Notes |
|------|-----------|---------|--------|---------|---------|-------|
| T+0 | | | | | | |
| T+1h | | | | | | |
| T+2h | | | | | | |
| T+4h | | | | | | |
| T+6h | | | | | | |
| T+8h | | | | | | |
| T+12h | | | | | | |
| T+24h | | | | | | |

### Week 1 daily log

| Day | Downloads | Revenue | Trials | D1 Ret. | Reviews | Rating |
|-----|-----------|---------|--------|---------|---------|--------|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |
| 6 | | | | | | |
| 7 | | | | | | |

### Month 1 weekly log

| Week | Downloads | Revenue | MRR | Churn | D7 Ret. | CAC |
|------|-----------|---------|-----|-------|---------|-----|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |

---

## Calculating key metrics

### Trial conversion rate

```
Trial Conversion = (Paid Conversions / Trial Starts) x 100

Example: 50 paid / 500 trials = 10%
```

### Day N retention

```
Day N Retention = (Users active on Day N / Users who started on Day 0) x 100

Example: 200 active on Day 7 / 1000 started = 20%
```

### Customer acquisition cost (CAC)

```
CAC = Total Marketing Spend / New Customers

Example: $500 ads / 50 customers = $10 CAC
```

### Lifetime value (LTV)

```
Simple LTV = Average Revenue Per User x Average Customer Lifespan

Subscription LTV = Monthly Price x (1 / Monthly Churn Rate)

Example: $10/month x (1 / 0.05) = $200 LTV
```

### Payback period

```
Payback = CAC / Monthly Revenue Per User

Example: $10 CAC / $2 monthly = 5 months
```

---

## Benchmarks by app type

### Consumer subscription apps

| Metric | Average | Good | Great |
|--------|---------|------|-------|
| Trial conversion | 2-5% | 5-10% | > 10% |
| Day 1 retention | 25-35% | 35-50% | > 50% |
| Day 7 retention | 10-15% | 15-25% | > 25% |
| Day 30 retention | 5-10% | 10-15% | > 15% |
| Monthly churn | 5-10% | 3-5% | < 3% |

### Productivity apps

| Metric | Average | Good | Great |
|--------|---------|------|-------|
| Trial conversion | 5-10% | 10-20% | > 20% |
| Day 1 retention | 30-40% | 40-55% | > 55% |
| Day 7 retention | 15-25% | 25-35% | > 35% |
| Day 30 retention | 10-15% | 15-25% | > 25% |
| Monthly churn | 3-7% | 2-3% | < 2% |

### One-time purchase apps

| Metric | Average | Good | Great |
|--------|---------|------|-------|
| Conversion rate | 0.5-2% | 2-5% | > 5% |
| Day 1 retention | 20-30% | 30-45% | > 45% |
| Review rate | 1-3% | 3-5% | > 5% |

---

## What to do with the data

### If downloads are low

1. Check app store listing visibility
2. Review screenshots and description
3. Increase marketing activity
4. Check if targeting is correct

### If trial conversion is low

1. Review onboarding flow
2. Check time-to-value (too long?)
3. Test different paywall designs
4. Review pricing

### If retention is low

1. Check Day 1 experience
2. Review core value proposition
3. Add engagement features (notifications, streaks)
4. Interview churned users

### If revenue is low despite good trials

1. Test pricing (might be too low)
2. Review paywall messaging
3. Check for payment friction
4. Test annual vs monthly emphasis

---

## Reporting template

### Daily report (for launch week)

```
[App Name] Day [X] Report

Downloads: [N] (+X% vs yesterday)
Revenue: $[N] (+$X vs yesterday)
Trials: [N]
Conversions: [N] ([X]% conversion rate)

Reviews: [N] new ([X] star average)
Crashes: [N] ([X]% crash rate)

Wins:
- [Positive thing]

Issues:
- [Problem and fix]

Tomorrow:
- [Plan]
```

### Weekly report

```
[App Name] Week [X] Report

Total downloads: [N]
Total revenue: $[N]
MRR: $[N]
Active users: [N]

Key metrics:
- Trial conversion: [X]%
- Day 7 retention: [X]%
- CAC: $[X]
- LTV estimate: $[X]

Top performing channel: [Channel]
Worst performing channel: [Channel]

Top feedback themes:
1. [Theme]
2. [Theme]
3. [Theme]

Actions for next week:
1. [Action]
2. [Action]
3. [Action]
```

---

Created: 2026-01-21
