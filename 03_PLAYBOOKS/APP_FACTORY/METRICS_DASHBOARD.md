# App Metrics Dashboard

What to track, benchmark targets, and how to interpret data for all PRINTMAXX apps.

---

## Metrics Overview

### Acquisition Metrics
How users find and download your app.

### Activation Metrics
How users start using your app.

### Revenue Metrics
How you make money.

### Retention Metrics
How users stick around.

### Referral Metrics
How users spread the word.

---

## Acquisition Metrics

### Downloads

| Metric | Definition | Benchmark | Source |
|--------|------------|-----------|--------|
| Total downloads | Cumulative installs | Varies by niche | App Store Connect / Play Console |
| Daily downloads | Installs per day | 100+ launch week | App Store Connect |
| Downloads by source | Organic vs paid vs referral | 70% organic goal | Attribution tracking |

### App Store Performance

| Metric | Definition | Benchmark | Source |
|--------|------------|-----------|--------|
| Impressions | Times app appeared in search | Growth indicator | ASC/PC |
| Product page views | Clicked to your page | 3-5% of impressions | ASC/PC |
| Conversion rate | Downloads / page views | 25-40% | ASC/PC |
| Keyword rankings | Position for target keywords | Top 10 | AppTweak/ASO tool |

### Paid Acquisition

| Metric | Definition | Benchmark | Source |
|--------|------------|-----------|--------|
| Cost Per Install (CPI) | Ad spend / installs | $0.50-3 | Ad platforms |
| Click-Through Rate (CTR) | Clicks / impressions | 1-3% | Ad platforms |
| Cost Per Mille (CPM) | Cost per 1000 impressions | $4-15 | Ad platforms |

---

## Activation Metrics

### Onboarding

| Metric | Definition | Benchmark | Source |
|--------|------------|-----------|--------|
| Onboarding completion | Finished onboarding / downloads | 70%+ | Mixpanel |
| Time to first value | Time from download to core action | <5 minutes | Mixpanel |
| First session length | Time in first session | 3-5 minutes | Mixpanel |

### Trial Performance

| Metric | Definition | Benchmark | Source |
|--------|------------|-----------|--------|
| Trial start rate | Trials started / downloads | 60%+ | RevenueCat |
| Trial completion rate | Completed trial / started trial | 50%+ | RevenueCat |
| Trial to paid | Converted / trials ended | 8-15% | RevenueCat |

### Feature Adoption

| Metric | Definition | Benchmark | Source |
|--------|------------|-----------|--------|
| Core feature usage | % using main feature | 80%+ | Mixpanel |
| Secondary feature usage | % using other features | 40%+ | Mixpanel |
| Feature stickiness | Users returning to feature | Daily use | Mixpanel |

---

## Revenue Metrics

### Primary Revenue

| Metric | Definition | Benchmark | Source |
|--------|------------|-----------|--------|
| Monthly Recurring Revenue (MRR) | Monthly subscription revenue | Growth target | RevenueCat |
| Annual Recurring Revenue (ARR) | MRR x 12 | $100K+ goal | RevenueCat |
| Average Revenue Per User (ARPU) | Total revenue / active users | $2-5/month | RevenueCat |
| Lifetime Value (LTV) | Total revenue from a user | $25-50 | RevenueCat |

### Subscription Metrics

| Metric | Definition | Benchmark | Source |
|--------|------------|-----------|--------|
| New subscriptions | New paying users | Growth indicator | RevenueCat |
| Monthly vs Annual split | % choosing each plan | 30/70 annual preferred | RevenueCat |
| Subscription churn | Cancellations / total subs | <8% monthly | RevenueCat |
| Renewal rate | Renewed / up for renewal | 75%+ | RevenueCat |

### Unit Economics

| Metric | Definition | Benchmark | Source |
|--------|------------|-----------|--------|
| Customer Acquisition Cost (CAC) | Cost to acquire paying user | <$10 | Calculated |
| LTV/CAC ratio | Lifetime value / acquisition cost | 3:1+ | Calculated |
| Payback period | Months to recoup CAC | <3 months | Calculated |

---

## Retention Metrics

### Cohort Retention

| Day | Good | Great | Excellent |
|-----|------|-------|-----------|
| Day 1 | 35% | 45% | 55%+ |
| Day 7 | 20% | 30% | 40%+ |
| Day 30 | 12% | 18% | 25%+ |
| Day 90 | 8% | 12% | 18%+ |

### Engagement

| Metric | Definition | Benchmark | Source |
|--------|------------|-----------|--------|
| Daily Active Users (DAU) | Users active per day | Growth indicator | Mixpanel |
| Monthly Active Users (MAU) | Users active per month | Growth indicator | Mixpanel |
| DAU/MAU ratio | Daily / monthly actives | 20-30% = good | Mixpanel |
| Sessions per user | Average sessions per day | 1.5-3 | Mixpanel |
| Session length | Average time in app | 5-15 min | Mixpanel |

### Churn

| Metric | Definition | Benchmark | Source |
|--------|------------|-----------|--------|
| User churn | Inactive users / total | <10% monthly | Mixpanel |
| Revenue churn | Lost MRR / total MRR | <5% monthly | RevenueCat |
| Net churn | Revenue churn - expansion | Negative is ideal | RevenueCat |

---

## App-Specific Metrics

### StepUnlock

| Metric | Definition | Benchmark |
|--------|------------|-----------|
| Daily step goal completion | % hitting goal | 70%+ |
| Average daily steps | Steps per user | 6,000+ |
| Streak length | Consecutive days | 10+ avg |
| Emergency unlock rate | % using emergency | <5% |
| Screen time reduction | Self-reported | 30%+ |

### FocusPrayer

| Metric | Definition | Benchmark |
|--------|------------|-----------|
| Devotion completion rate | % completing daily | 75%+ |
| Average prayer time | Minutes per session | 8+ min |
| Scripture read rate | % reading daily verse | 85%+ |
| Streak length | Consecutive days | 12+ avg |
| Church pilot enrollment | Churches active | 10+ |

### DailyAnchor

| Metric | Definition | Benchmark |
|--------|------------|-----------|
| Habit completion rate | Habits checked / total | 60%+ |
| Gratitude entries | % journaling daily | 70%+ |
| Average habits tracked | Habits per user | 4+ |
| Streak length | Consecutive days | 15+ avg |
| Template adoption | % using templates | 80%+ |

### DevotionFlow

| Metric | Definition | Benchmark |
|--------|------------|-----------|
| Habit completion rate | Habits checked / total | 60%+ |
| Template usage | % using pre-built | 85%+ |
| Streak celebrations | Hitting milestones | Engagement lift |
| Daily verse views | % viewing verse | 90%+ |

### LearnLock

| Metric | Definition | Benchmark |
|--------|------------|-----------|
| Session completion | % completing timer | 80%+ |
| Average session length | Minutes per session | 35+ min |
| Daily study time | Total minutes/day | 120+ min |
| Streak length | Consecutive days | 8+ avg |
| University pilots | Schools active | 5+ |

---

## Dashboard Setup

### Tools Stack

| Tool | Purpose | Cost |
|------|---------|------|
| RevenueCat | Revenue, subscriptions | Free to start |
| Mixpanel | User behavior, retention | Free to 1M events |
| Sentry | Crash reporting | Free tier available |
| App Store Connect | iOS metrics | Free |
| Google Play Console | Android metrics | Free |

### RevenueCat Dashboard

Track:
- MRR/ARR
- New subscriptions
- Churn rate
- Trial conversions
- Revenue by product

### Mixpanel Dashboard

Track:
- Daily/Monthly active users
- Retention cohorts
- Feature usage
- Funnel completion
- User segments

### Custom Spreadsheet Dashboard

Build a weekly tracker with:
- Downloads (by source)
- Trials started
- Conversions
- MRR
- Retention (D1, D7, D30)
- Key feature usage
- App Store rating

---

## Alert Thresholds

### Red Alerts (Immediate Action)

| Metric | Threshold | Action |
|--------|-----------|--------|
| Crash rate | >1% | Stop releases, fix |
| Day 1 retention | <30% | Review onboarding |
| Trial to paid | <5% | Review paywall |
| App Store rating | <4.0 | Address reviews |
| Daily downloads | -50% | Investigate |

### Yellow Alerts (Monitor Closely)

| Metric | Threshold | Action |
|--------|-----------|--------|
| Day 7 retention | <20% | Test engagement |
| CAC | >$5 | Review ads |
| Churn | >10% | Survey churned users |
| Feature adoption | <50% | Improve discoverability |

### Green Indicators (Scale)

| Metric | Threshold | Action |
|--------|-----------|--------|
| Trial to paid | >12% | Increase acquisition |
| LTV/CAC | >4:1 | Scale paid |
| Day 30 retention | >20% | Add features |
| Referral rate | >5% | Invest in referral |

---

## Reporting Cadence

### Daily (Automated)

- Downloads
- Revenue
- Crash rate
- Active users

### Weekly (Manual Review)

- Week-over-week trends
- Retention cohorts
- Conversion funnels
- Channel performance
- Bug reports

### Monthly (Deep Dive)

- Full metrics review
- User interviews
- Competitor analysis
- Feature prioritization
- Pricing review

---

## Benchmarks by App Type

### Screen Time / Blocking Apps (StepUnlock, FocusPrayer, LearnLock)

| Metric | Benchmark |
|--------|-----------|
| Day 1 retention | 45%+ |
| Day 7 retention | 28%+ |
| Day 30 retention | 18%+ |
| Trial to paid | 10%+ |
| Monthly churn | <7% |

### Habit Tracking Apps (DailyAnchor, DevotionFlow)

| Metric | Benchmark |
|--------|-----------|
| Day 1 retention | 40%+ |
| Day 7 retention | 25%+ |
| Day 30 retention | 15%+ |
| Trial to paid | 8%+ |
| Monthly churn | <8% |

---

## Data-Driven Decisions

### If trial to paid is low (<8%)

1. Review paywall design
2. A/B test pricing
3. Extend trial length
4. Add more value to premium
5. Improve trial experience

### If Day 1 retention is low (<35%)

1. Simplify onboarding
2. Speed up time to value
3. Reduce permissions asks
4. Improve first session
5. Add progress indicators

### If churn is high (>10%)

1. Survey churned users
2. Improve core loop
3. Add engagement features
4. Better push notifications
5. Re-engagement campaigns

### If CAC is high (>$3)

1. Improve creative
2. Narrow targeting
3. Shift to cheaper channels
4. Increase organic efforts
5. Improve conversion rate

---

## Metric Formulas

**LTV Calculation:**
```
LTV = ARPU x Average Customer Lifespan
LTV = (Monthly ARPU) / (Monthly Churn Rate)
```

**CAC Calculation:**
```
CAC = Total Marketing Spend / New Customers
```

**LTV/CAC Ratio:**
```
Ratio = LTV / CAC
Target: 3:1 or higher
```

**Payback Period:**
```
Payback = CAC / Monthly ARPU
Target: <3 months
```

**Retention Rate:**
```
Retention = (Users at end - New users) / Users at start
```

---

Created: 2026-01-21
