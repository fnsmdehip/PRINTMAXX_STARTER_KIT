# Onboarding Metrics Guide

Track these metrics to optimize onboarding flows across all 7 apps.

---

## Core Funnel Metrics

### 1. Screen Completion Rate

**What:** Percentage of users who complete each screen and move to the next.

**Formula:**
```
Screen N Completion Rate = (Users reaching Screen N+1) / (Users reaching Screen N) * 100
```

**Benchmark targets by screen type:**

| Screen Type | Target | Acceptable | Poor |
|-------------|--------|------------|------|
| Welcome/intro | > 95% | 90-95% | < 90% |
| Goal/preference selection | > 90% | 85-90% | < 85% |
| Permission request | > 75% | 65-75% | < 65% |
| Paywall (hard) | > 60% | 50-60% | < 50% |
| Paywall (soft) | > 85% | 75-85% | < 75% |
| First action/tutorial | > 80% | 70-80% | < 70% |

### 2. Onboarding Completion Rate

**What:** Percentage of users who complete the entire onboarding flow.

**Formula:**
```
Onboarding Completion Rate = (Users completing final screen) / (Users starting onboarding) * 100
```

**Benchmark targets by app type:**

| App Type | Target | Acceptable | Poor |
|----------|--------|------------|------|
| Hard paywall (PrayerLock, WalkToUnlock, StudyLock, FemFit) | > 55% | 45-55% | < 45% |
| Soft paywall (PromptVault, DailyAnchor, DailyDevotion) | > 75% | 65-75% | < 65% |

### 3. Time to Complete Onboarding

**What:** Average time users spend in the onboarding flow.

**Benchmark targets:**

| Screens | Target | Too Fast | Too Slow |
|---------|--------|----------|----------|
| 4 screens | 90-150 sec | < 60 sec | > 240 sec |
| 5 screens | 120-180 sec | < 90 sec | > 300 sec |
| 6 screens | 150-210 sec | < 120 sec | > 360 sec |

**Why too fast is bad:** Users skipping without reading.
**Why too slow is bad:** Friction causing abandonment.

---

## Conversion Metrics

### 4. Trial Start Rate

**What:** Percentage of users who start a free trial.

**Formula:**
```
Trial Start Rate = (Users starting trial) / (Users reaching paywall) * 100
```

**Benchmark targets:**

| Paywall Type | Target | Acceptable | Poor |
|--------------|--------|------------|------|
| Hard paywall (3-day trial) | > 65% | 55-65% | < 55% |
| Hard paywall (7-day trial) | > 70% | 60-70% | < 60% |
| Soft paywall | > 25% | 15-25% | < 15% |

### 5. Trial to Paid Conversion

**What:** Percentage of trial users who convert to paid.

**Formula:**
```
Trial to Paid = (Paid subscribers from trial) / (Trial starts) * 100
```

**Benchmark targets by app:**

| App | Target | Acceptable | Poor |
|-----|--------|------------|------|
| PrayerLock | > 15% | 12-15% | < 12% |
| WalkToUnlock | > 12% | 10-12% | < 10% |
| StudyLock | > 10% | 8-10% | < 8% |
| FemFit | > 12% | 10-12% | < 10% |
| PromptVault | > 25% | 20-25% | < 20% |
| DailyAnchor | > 8% | 6-8% | < 6% |
| DailyDevotion | > 8% | 6-8% | < 6% |

### 6. Overall Conversion Rate

**What:** Percentage of all onboarding users who become paid subscribers.

**Formula:**
```
Overall Conversion = (Paid subscribers) / (Users starting onboarding) * 100
```

**Benchmark targets:**

| Model | Target | Acceptable | Poor |
|-------|--------|------------|------|
| Hard paywall apps | > 8% | 5-8% | < 5% |
| Freemium apps | > 3% | 2-3% | < 2% |

---

## Engagement Metrics

### 7. First Action Completion

**What:** Percentage of users who complete the first core action after onboarding.

**First actions by app:**

| App | First Action | Target |
|-----|--------------|--------|
| PrayerLock | Complete first prayer session | > 70% |
| WalkToUnlock | Hit first step goal | > 40% |
| StudyLock | Complete first study session | > 65% |
| PromptVault | Copy first prompt | > 80% |
| DailyAnchor | Check off first habit | > 75% |
| FemFit | Complete first workout | > 55% |
| DailyDevotion | Mark first verse as read | > 70% |

### 8. Day 1 Retention

**What:** Percentage of users who return on the day after onboarding.

**Formula:**
```
Day 1 Retention = (Users active on Day 1) / (Users completing onboarding on Day 0) * 100
```

**Benchmark targets:**

| App Type | Target | Acceptable | Poor |
|----------|--------|------------|------|
| Blocker apps (PrayerLock, WalkToUnlock, StudyLock) | > 60% | 50-60% | < 50% |
| Habit apps (DailyAnchor, DailyDevotion) | > 55% | 45-55% | < 45% |
| Tool apps (PromptVault, FemFit) | > 45% | 35-45% | < 35% |

### 9. Day 7 Retention

**What:** Percentage of users active 7 days after onboarding.

**Benchmark targets:**

| App | Target | Acceptable | Poor |
|-----|--------|------------|------|
| PrayerLock | > 40% | 30-40% | < 30% |
| WalkToUnlock | > 35% | 25-35% | < 25% |
| StudyLock | > 35% | 25-35% | < 25% |
| PromptVault | > 30% | 20-30% | < 20% |
| DailyAnchor | > 40% | 30-40% | < 30% |
| FemFit | > 35% | 25-35% | < 25% |
| DailyDevotion | > 40% | 30-40% | < 30% |

---

## Permission Metrics

### 10. Notification Permission Grant Rate

**What:** Percentage of users who grant notification permission.

**Benchmark targets:**

| Timing | Target | Acceptable | Poor |
|--------|--------|------------|------|
| After value demonstrated | > 70% | 60-70% | < 60% |
| During onboarding (with context) | > 55% | 45-55% | < 45% |
| Cold ask (no context) | > 35% | 25-35% | < 25% |

### 11. Health Data Permission Grant Rate (WalkToUnlock only)

**What:** Percentage of users who grant HealthKit/Google Fit access.

**Benchmark targets:**

| Context | Target | Acceptable | Poor |
|---------|--------|------------|------|
| With privacy explanation | > 80% | 70-80% | < 70% |
| Without explanation | > 60% | 50-60% | < 50% |

### 12. Screen Time Permission Grant Rate (Blocker apps)

**What:** Percentage of users who grant screen time/accessibility access.

**Benchmark targets:**

| Context | Target | Acceptable | Poor |
|---------|--------|------------|------|
| With clear explanation | > 75% | 65-75% | < 65% |
| App cannot function without | > 85% | 75-85% | < 75% |

---

## Drop-off Analysis Metrics

### 13. Screen-by-Screen Drop-off Rate

**What:** Percentage of users who abandon at each screen.

**Formula:**
```
Drop-off Rate = (Users reaching Screen N) - (Users reaching Screen N+1) / (Users reaching Screen N) * 100
```

**Alert thresholds:**

| Screen Type | Alert if drop-off > |
|-------------|---------------------|
| Welcome | 5% |
| Preference selection | 15% |
| Permission request | 35% |
| Paywall (hard) | 50% |
| Paywall (soft) | 25% |
| Final action | 20% |

### 14. Rage Quit Rate

**What:** Users who force-close the app during onboarding.

**Formula:**
```
Rage Quit Rate = (Force closes during onboarding) / (Onboarding starts) * 100
```

**Benchmark:** Should be < 5%

### 15. Back Button Rate

**What:** Percentage of users who use back button during onboarding.

**Benchmark:** High back button usage (> 20%) indicates confusion or regret.

---

## A/B Test Metrics

### 16. Statistical Significance

**What:** Confidence level that a variant is better than control.

**Minimum requirements:**
- Sample size: 1,000 users per variant minimum
- Confidence level: 95% (p < 0.05)
- Duration: Run test for at least 7 days

### 17. Lift Percentage

**What:** Percentage improvement of variant over control.

**Formula:**
```
Lift = (Variant conversion - Control conversion) / Control conversion * 100
```

**Action thresholds:**

| Lift | Action |
|------|--------|
| > 20% lift | Ship immediately |
| 10-20% lift | Ship if statistically significant |
| 5-10% lift | Continue testing with larger sample |
| < 5% lift | Not worth shipping |

---

## Implementation Checklist

### Analytics Events to Track

```javascript
// Required events for all apps
onboarding_started
onboarding_screen_viewed (screen_name, screen_number)
onboarding_screen_completed (screen_name, time_spent)
onboarding_abandoned (screen_name, time_spent)
onboarding_completed (total_time)

// Permission events
permission_requested (type: notification|health|screentime)
permission_granted (type)
permission_denied (type)

// Paywall events
paywall_shown
paywall_trial_started
paywall_free_selected (soft paywall only)
paywall_dismissed (if dismissible)

// Selection events
preference_selected (preference_name, value)

// Post-onboarding
first_action_started
first_action_completed
```

### Dashboard Requirements

Build dashboards showing:

1. **Funnel view:** Visual flow from start to completion
2. **Screen-by-screen metrics:** Completion rate, time spent, drop-off
3. **Conversion tracking:** Trial starts, trial-to-paid, overall
4. **A/B test results:** Variant performance comparison
5. **Trend analysis:** Week-over-week changes in key metrics

### Tools Recommendation

| Purpose | Tool | Cost |
|---------|------|------|
| Analytics | Mixpanel (free tier) | Free up to 20M events/month |
| A/B testing | RevenueCat Experiments | Included with RevenueCat |
| Crash reporting | Firebase Crashlytics | Free |
| Session recording | UXCam (optional) | $99/month |

---

## Weekly Review Checklist

Every week, review:

- [ ] Overall onboarding completion rate
- [ ] Screen-by-screen drop-off rates
- [ ] Trial start rate
- [ ] Permission grant rates
- [ ] Day 1 and Day 7 retention
- [ ] Any A/B test results ready for decision
- [ ] Any screens with > 20% drop-off needing attention

---

## Quarterly Goals

Set quarterly targets for:

1. Improve onboarding completion by X%
2. Improve trial start rate by X%
3. Improve trial-to-paid by X%
4. Run X A/B tests
5. Achieve X% Day 7 retention

Track progress monthly. Adjust tactics if not on track.
