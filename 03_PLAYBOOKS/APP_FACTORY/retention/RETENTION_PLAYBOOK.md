# Retention playbook

Retention is the only metric that matters. A 5% improvement in D30 retention beats a 50% increase in installs.

---

## Retention benchmarks by app type

### Day 1 retention (D1)

| App type | Poor | Average | Good | Excellent |
|----------|------|---------|------|-----------|
| Faith/devotional | <30% | 30-40% | 40-50% | >50% |
| Fitness/workout | <25% | 25-35% | 35-45% | >45% |
| Productivity/focus | <20% | 20-30% | 30-40% | >40% |

### Day 7 retention (D7)

| App type | Poor | Average | Good | Excellent |
|----------|------|---------|------|-----------|
| Faith/devotional | <15% | 15-22% | 22-30% | >30% |
| Fitness/workout | <12% | 12-18% | 18-25% | >25% |
| Productivity/focus | <10% | 10-15% | 15-22% | >22% |

### Day 30 retention (D30)

| App type | Poor | Average | Good | Excellent |
|----------|------|---------|------|-----------|
| Faith/devotional | <8% | 8-12% | 12-18% | >18% |
| Fitness/workout | <5% | 5-10% | 10-15% | >15% |
| Productivity/focus | <4% | 4-8% | 8-12% | >12% |

### Day 90 retention (D90)

| App type | Poor | Average | Good | Excellent |
|----------|------|---------|------|-----------|
| Faith/devotional | <4% | 4-7% | 7-10% | >10% |
| Fitness/workout | <2% | 2-5% | 5-8% | >8% |
| Productivity/focus | <2% | 2-4% | 4-7% | >7% |

---

## Cohort analysis setup

### Weekly cohorts

Track users by install week, not by calendar date. This reveals trends over time.

**Firebase setup:**
```
Events to track:
- first_open (automatic)
- session_start (automatic)
- core_action_completed (custom)
- feature_used_[name] (custom)
- subscription_started (custom)
```

### Cohort table structure

| Install week | Users | D1 | D7 | D14 | D30 | D60 | D90 |
|--------------|-------|----|----|-----|-----|-----|-----|
| W1 Jan 2026 | 1,234 | 38% | 18% | 12% | 8% | 5% | 3% |
| W2 Jan 2026 | 1,456 | 41% | 21% | 14% | 9% | - | - |
| W3 Jan 2026 | 1,678 | 39% | 19% | - | - | - | - |

### Key analysis questions

1. Which cohorts perform best? (Correlate with marketing channel)
2. Where is the biggest drop? (D1-D7 vs D7-D30)
3. Are newer cohorts improving? (Product changes working?)
4. What do retained users have in common? (Activation events)

---

## Churn prediction signals

### High-risk behaviors (predict churn 7+ days before)

| Signal | Risk level | Action trigger |
|--------|------------|----------------|
| No session in 3 days | Medium | Send push: "We miss you" |
| No core action in 5 days | High | Send push + email combo |
| Disabled notifications | High | In-app prompt to re-enable |
| Never completed onboarding | Critical | Onboarding reminder sequence |
| Used app <2 min on D1 | High | Send value reminder D2 |
| No second session | Critical | D1 re-engagement push |

### Engagement scoring model

Score users 0-100 based on weighted factors:

```
Engagement score =
  (sessions_last_7d * 5) +
  (core_actions_last_7d * 10) +
  (streak_length * 2) +
  (features_used * 3) +
  (notifications_enabled * 15) +
  (premium_user * 20)
```

**Score thresholds:**
- 0-20: Critical risk, immediate intervention
- 21-40: High risk, proactive outreach
- 41-60: Medium risk, monitor closely
- 61-80: Engaged, standard nurture
- 81-100: Power user, request reviews/referrals

---

## Re-engagement triggers

### Push notification triggers

| Trigger condition | Timing | Message type |
|-------------------|--------|--------------|
| No open in 24h | 9am local | Streak reminder |
| No open in 48h | 9am local | Miss-you message |
| No open in 72h | 9am local | Value reminder |
| No open in 7d | 9am local | What's new |
| No open in 14d | 9am local | Special offer |
| No open in 30d | 9am local | Win-back incentive |

### Email triggers

| Trigger condition | Delay | Email type |
|-------------------|-------|------------|
| No D2 session | 36h after install | "Getting started" tips |
| No D4 session | 4 days after install | Feature highlight |
| No D7 session | 7 days after install | Social proof + value |
| No D14 session | 14 days after install | "We miss you" |
| No D30 session | 30 days after install | Win-back offer |

### In-app triggers

| User state | Trigger | Action |
|------------|---------|--------|
| Returns after 3+ days | On app open | Welcome back modal |
| About to lose streak | 2h before midnight | Streak save notification |
| Completed milestone | On achievement | Celebration animation |
| Used new feature | After first use | Feature benefit tooltip |

---

## Retention levers by impact

### High impact (focus here first)

1. **Onboarding completion** - Users who finish onboarding retain 2.5x better
2. **Day 1 core action** - Users who complete core action on D1 retain 3x better
3. **Push notification opt-in** - Users with notifications retain 2x better
4. **Streak formation** - Users who build 7-day streak retain 4x better

### Medium impact

5. **Personalization** - Customized content increases D30 by 15-25%
6. **Social features** - Users with friends retain 1.5x better
7. **Content freshness** - New content weekly increases return visits 20%

### Lower impact (nice to have)

8. **UI polish** - Marginal retention gains, better conversion
9. **Load time** - Only matters if >3s
10. **Dark mode** - Requested often, minimal retention impact

---

## Retention emergency protocol

### If D1 drops >5% week-over-week

1. Check for app crashes (Firebase Crashlytics)
2. Check onboarding funnel for new friction
3. Check for bad reviews mentioning specific issues
4. Check if marketing channel mix changed
5. Run A/B test reverting recent changes

### If D7 drops >3% week-over-week

1. Analyze activated vs non-activated users
2. Check push notification delivery rates
3. Review content freshness schedule
4. Check competitor launches
5. Survey recent churned users

### If D30 drops >2% week-over-week

1. Deep cohort analysis by acquisition source
2. Review subscription pricing/value perception
3. Check for engagement score drift
4. Analyze feature usage patterns
5. Run NPS survey to long-term users

---

## Quick wins checklist

- [ ] Push notifications enabled by default (with clear value prop)
- [ ] Core action achievable in <60 seconds on D1
- [ ] Progress saved across sessions
- [ ] Streak mechanic implemented
- [ ] Re-engagement push sequence active
- [ ] Welcome back modal for returning users
- [ ] Milestone celebrations with share prompts
- [ ] Daily reminder notification at optimal time
- [ ] Onboarding <5 screens
- [ ] Value delivered before asking for anything

---

## Retention math

### Retention drives LTV

```
D30 10% -> LTV $2.50
D30 15% -> LTV $4.00
D30 20% -> LTV $6.00

Every 5% D30 improvement = ~$1.50 LTV gain
```

### Payback period calculation

```
CAC = $1.50 (average paid install)
ARPU = $0.15/month (blended)

At D30 10%: Payback = 10 months
At D30 15%: Payback = 6.7 months
At D30 20%: Payback = 5 months
```

### The retention cliff

Most churn happens D0-D1. Fix this first.

```
Typical decay curve:
D0 -> D1: -60% (biggest loss)
D1 -> D7: -50%
D7 -> D30: -40%
D30 -> D90: -50%
```

Focus 80% of retention effort on D0-D7. This is where users decide if your app is habit or delete.
