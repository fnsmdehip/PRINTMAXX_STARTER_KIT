# Early warning signals

Identify users about to churn before they leave. Early intervention converts 15-25% of at-risk users.

---

## Signal categories

### Category 1: Activity decline

These signals indicate decreasing engagement before full churn.

| Signal | How to detect | Risk level | Time to churn |
|--------|---------------|------------|---------------|
| Session frequency drop | 50%+ fewer sessions week-over-week | High | 7-14 days |
| Session duration drop | 50%+ shorter sessions | Medium | 10-20 days |
| Core actions declining | Fewer core actions per session | Medium | 14-21 days |
| Feature exploration stopped | No new features used in 14 days | Low | 21-30 days |

**Detection query example:**
```sql
SELECT user_id
FROM user_activity
WHERE sessions_last_7_days < sessions_7_14_days_ago * 0.5
  AND sessions_last_7_days > 0
```

---

### Category 2: Engagement quality

Quality of engagement matters more than quantity.

| Signal | How to detect | Risk level | Time to churn |
|--------|---------------|------------|---------------|
| Bounce rate increasing | Opens app, leaves in <30 sec | High | 5-10 days |
| No core actions | Opens but doesn't complete value action | High | 7-14 days |
| Passive vs active | Only consumes, doesn't interact | Medium | 14-21 days |
| Shallow engagement | Views home screen only | High | 7-14 days |

**Detection query example:**
```sql
SELECT user_id
FROM sessions
WHERE session_duration < 30
  AND date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY user_id
HAVING COUNT(*) > 3
```

---

### Category 3: Behavioral changes

Sudden changes in behavior patterns signal risk.

| Signal | How to detect | Risk level | Time to churn |
|--------|---------------|------------|---------------|
| Time of use shifted | Regular time abandoned | Medium | 14-21 days |
| Device changed | New device, old habits lost | Medium | 10-14 days |
| Streak broken | Maintained streak, now lost | High | 3-7 days |
| Notification disabled | Previously enabled, now off | Critical | 5-10 days |

**Detection query example:**
```sql
SELECT user_id
FROM user_settings_history
WHERE setting = 'notifications_enabled'
  AND new_value = false
  AND old_value = true
  AND changed_at >= CURRENT_DATE - INTERVAL '7 days'
```

---

### Category 4: Technical friction

Technical issues cause preventable churn.

| Signal | How to detect | Risk level | Time to churn |
|--------|---------------|------------|---------------|
| App crashes | Crashlytics reports for user | Critical | 3-7 days |
| Error encounters | API errors, failed actions | High | 5-10 days |
| Slow performance | Load times >3 seconds | Medium | 14-21 days |
| Sync failures | Data sync errors | High | 7-14 days |

**Detection:**
```
Monitor Crashlytics/Sentry for:
- Users with 2+ crashes in 7 days
- Users with 5+ API errors in 7 days
- Users with session timeouts
```

---

### Category 5: Subscription signals

For premium users, subscription behavior predicts churn.

| Signal | How to detect | Risk level | Time to churn |
|--------|---------------|------------|---------------|
| Billing issue | Payment failed | Critical | 0-3 days |
| Cancellation initiated | Started cancel flow | Critical | 0-7 days |
| Downgrade inquiry | Viewed pricing, on premium | High | 7-14 days |
| Usage below tier | Premium but uses like free | High | 14-30 days |

---

## Composite risk scoring

### Engagement score calculation

```
Score components (0-100 total):

Activity (30 points max):
- Sessions in last 7 days: 0-15 points
- Core actions in last 7 days: 0-15 points

Quality (30 points max):
- Average session duration: 0-15 points
- Features used: 0-15 points

Consistency (20 points max):
- Active days out of last 7: 0-10 points
- Streak length: 0-10 points

Platform (20 points max):
- Notifications enabled: 0-10 points
- Premium status: 0-10 points
```

### Risk thresholds

| Score | Risk level | Action |
|-------|------------|--------|
| 0-20 | Critical | Immediate intervention |
| 21-40 | High | Proactive outreach within 24h |
| 41-60 | Medium | Monitor closely, soft outreach |
| 61-80 | Low | Standard nurture sequence |
| 81-100 | Minimal | Power user treatment |

### Score decay detection

More important than absolute score: rate of change.

```
Alert triggers:
- Score drops >20 points in 7 days
- Score drops >10 points in 3 days
- Score crosses below 40 threshold
- Score crosses below 20 threshold
```

---

## Signal prioritization matrix

### By predictive power

| Rank | Signal | Predictive accuracy |
|------|--------|---------------------|
| 1 | Notifications disabled | 78% churn within 30 days |
| 2 | Streak broken (7+ days) | 65% churn within 30 days |
| 3 | No session in 5 days | 60% churn within 30 days |
| 4 | App crash experienced | 55% churn within 30 days |
| 5 | Session duration <30s | 50% churn within 30 days |
| 6 | Core actions stopped | 48% churn within 30 days |
| 7 | Feature usage narrowed | 35% churn within 30 days |

### By actionability

| Signal | Actionable? | Intervention |
|--------|-------------|--------------|
| Notifications disabled | Yes | Re-enable prompt |
| Streak broken | Yes | Streak recovery offer |
| No recent session | Yes | Re-engagement push |
| App crash | Maybe | Fix bug, apologize |
| Short sessions | Hard | Improve content quality |
| Billing failed | Yes | Update payment prompt |

---

## Real-time alerting setup

### Critical alerts (immediate action)

```
Alert: Critical risk user detected
Trigger: Score drops below 20 OR notification disabled

Action:
1. Flag in dashboard
2. Queue priority re-engagement
3. If premium: escalate to support
```

### Daily digest alerts

```
Morning report:
- Users who entered critical risk (last 24h): [count]
- Users who entered high risk (last 24h): [count]
- Users recovered from at-risk: [count]
- Total at-risk population: [count]

Attached: CSV of critical/high risk users for manual review
```

### Weekly trend alerts

```
Weekly analysis:
- Risk population trend (up/down %)
- Top churn reasons this week
- Intervention success rate
- Cohort retention changes
```

---

## Segment-specific signals

### New users (0-7 days)

Focus signals:
- Onboarding completion
- First core action completed
- Second session happened
- Notification permission granted

### Developing users (7-30 days)

Focus signals:
- Streak building
- Feature exploration
- Return visit frequency
- Session depth

### Established users (30+ days)

Focus signals:
- Usage pattern changes
- Engagement decline rate
- Premium conversion/retention
- Feature abandonment

---

## Data collection requirements

### Events to track

```
Required events:
- app_open (timestamp, session_id)
- app_close (timestamp, session_id, duration)
- core_action_completed (type, duration)
- feature_used (feature_name)
- notification_setting_changed (old, new)
- error_occurred (type, message)
- session_timeout (last_action)
```

### User properties to maintain

```
User properties:
- first_open_date
- last_active_date
- total_sessions
- streak_current
- streak_max
- notifications_enabled
- premium_status
- engagement_score (calculated)
- risk_level (calculated)
```

### Event processing

```
Pipeline:
1. Raw events -> BigQuery/Amplitude
2. Daily aggregation job (engagement score)
3. Risk scoring job (composite score)
4. Alert generation (threshold checks)
5. Dashboard update
```

---

## Alert response playbook

### Score drops below 20 (critical)

1. Check for technical issues (crashes, errors)
2. Review recent activity pattern
3. Send personalized re-engagement
4. If premium: notify support team
5. Track intervention response

### Notifications disabled

1. Wait 24 hours (may be temporary)
2. Send in-app prompt on next open
3. If no open: email explaining value
4. Document for cohort analysis

### Streak broken

1. Send "streak save" offer immediately
2. Lower bar for streak recovery (1 action)
3. Celebrate when streak restored
4. Monitor for repeat breaks

### No session in 5 days

1. Stage 1 re-engagement push
2. Personalized content highlight
3. If premium: special offer
4. Log and continue sequence

---

## Metrics to track

| Metric | Target | Current |
|--------|--------|---------|
| At-risk detection rate | >90% of churners flagged | - |
| False positive rate | <30% | - |
| Lead time (days before churn) | >7 days | - |
| Intervention success rate | >15% recovered | - |
| Critical alert response time | <2 hours | - |
