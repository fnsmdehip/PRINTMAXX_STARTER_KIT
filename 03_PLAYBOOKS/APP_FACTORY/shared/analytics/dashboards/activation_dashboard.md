# Activation Dashboard

Metrics and queries for tracking user activation and aha moment achievement.

---

## Key metrics

| Metric | Target | Alert |
|--------|--------|-------|
| Activation rate | > 40% | < 25% |
| Time to activate | < 24 hours | > 48 hours |
| Feature discovery | > 3 features | < 2 features |
| First value time | < 5 minutes | > 15 minutes |

---

## Define your aha moment

The activation event varies by app type. Configure based on your core value:

| App Type | Aha Moment Event | Properties |
|----------|------------------|------------|
| Content creator | `content_created` | content_type, completed |
| Habit tracker | `streak_achieved` | streak_count >= 3 |
| Utility | `feature_completed` | feature_name = core |
| Social | `content_shared` | share_destination |

---

## Dashboard sections

### 1. Activation rate

**Chart type:** Line chart with trend

**Metrics:**
- Daily activation rate (activated / new users)
- Cumulative activation by cohort day
- Activation rate by platform

**Mixpanel query:**

```javascript
{
  event: 'feature_completed',
  from_date: '-30d',
  type: 'unique',
  where: 'properties["feature_name"] == "core_feature"',
  divided_by: {
    event: 'onboarding_completed',
    type: 'unique'
  }
}
```

**SQL:**

```sql
WITH cohorts AS (
  SELECT
    user_id,
    DATE(MIN(timestamp)) as cohort_date
  FROM events
  WHERE event_name = 'onboarding_completed'
    AND timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY user_id
),
activated AS (
  SELECT DISTINCT user_id
  FROM events
  WHERE event_name = 'feature_completed'
    AND properties->>'feature_name' = 'core_feature'
)
SELECT
  c.cohort_date,
  COUNT(DISTINCT c.user_id) as new_users,
  COUNT(DISTINCT a.user_id) as activated,
  ROUND(100.0 * COUNT(DISTINCT a.user_id) / NULLIF(COUNT(DISTINCT c.user_id), 0), 1) as activation_rate
FROM cohorts c
LEFT JOIN activated a USING (user_id)
GROUP BY c.cohort_date
ORDER BY c.cohort_date;
```

---

### 2. Time to activation

**Chart type:** Histogram + Line chart (median over time)

**Buckets:**
- < 1 minute
- 1-5 minutes
- 5-30 minutes
- 30m - 1 hour
- 1-24 hours
- 1-7 days
- Never activated

**SQL:**

```sql
WITH activation_times AS (
  SELECT
    e.user_id,
    MIN(CASE WHEN event_name = 'onboarding_completed' THEN timestamp END) as started,
    MIN(CASE WHEN event_name = 'feature_completed'
      AND properties->>'feature_name' = 'core_feature' THEN timestamp END) as activated
  FROM events e
  WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY e.user_id
)
SELECT
  CASE
    WHEN activated IS NULL THEN 'Never'
    WHEN EXTRACT(EPOCH FROM (activated - started)) < 60 THEN '< 1m'
    WHEN EXTRACT(EPOCH FROM (activated - started)) < 300 THEN '1-5m'
    WHEN EXTRACT(EPOCH FROM (activated - started)) < 1800 THEN '5-30m'
    WHEN EXTRACT(EPOCH FROM (activated - started)) < 3600 THEN '30m-1h'
    WHEN EXTRACT(EPOCH FROM (activated - started)) < 86400 THEN '1-24h'
    ELSE '1-7d'
  END as time_bucket,
  COUNT(*) as users,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) as pct
FROM activation_times
WHERE started IS NOT NULL
GROUP BY 1
ORDER BY
  CASE time_bucket
    WHEN '< 1m' THEN 1
    WHEN '1-5m' THEN 2
    WHEN '5-30m' THEN 3
    WHEN '30m-1h' THEN 4
    WHEN '1-24h' THEN 5
    WHEN '1-7d' THEN 6
    ELSE 7
  END;
```

---

### 3. Feature discovery

**Chart type:** Horizontal bar chart

**Metrics:**
- % of new users who discovered each feature
- Avg features discovered per user
- Feature discovery sequence

**SQL:**

```sql
WITH new_users AS (
  SELECT DISTINCT user_id
  FROM events
  WHERE event_name = 'onboarding_completed'
    AND timestamp >= CURRENT_DATE - INTERVAL '30 days'
),
feature_usage AS (
  SELECT
    user_id,
    properties->>'feature_name' as feature,
    MIN(timestamp) as first_use
  FROM events
  WHERE event_name = 'feature_used'
    AND timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY user_id, properties->>'feature_name'
)
SELECT
  feature,
  COUNT(DISTINCT f.user_id) as users,
  ROUND(100.0 * COUNT(DISTINCT f.user_id) / (SELECT COUNT(*) FROM new_users), 1) as discovery_rate
FROM feature_usage f
JOIN new_users n USING (user_id)
GROUP BY feature
ORDER BY users DESC;
```

---

### 4. Activation funnel by segment

**Chart type:** Multi-funnel comparison

**Segments:**
- By platform (iOS vs Android)
- By acquisition source
- By onboarding path
- By first feature used

**SQL:**

```sql
WITH user_segments AS (
  SELECT
    user_id,
    MAX(properties->>'platform') as platform,
    MAX(properties->>'source') as source
  FROM events
  WHERE event_name = 'onboarding_started'
    AND timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY user_id
),
activation_status AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'onboarding_completed' THEN 1 ELSE 0 END) as onboarded,
    MAX(CASE WHEN event_name = 'feature_used' THEN 1 ELSE 0 END) as used_feature,
    MAX(CASE WHEN event_name = 'feature_completed' THEN 1 ELSE 0 END) as activated
  FROM events
  WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY user_id
)
SELECT
  s.platform,
  COUNT(DISTINCT s.user_id) as users,
  ROUND(100.0 * SUM(a.onboarded) / COUNT(*), 1) as onboarded_pct,
  ROUND(100.0 * SUM(a.used_feature) / COUNT(*), 1) as used_feature_pct,
  ROUND(100.0 * SUM(a.activated) / COUNT(*), 1) as activated_pct
FROM user_segments s
JOIN activation_status a USING (user_id)
GROUP BY s.platform;
```

---

### 5. Drop-off analysis

**Chart type:** Sankey diagram or funnel with reasons

**Stages:**
1. Onboarding complete
2. First screen view (post-onboarding)
3. First interaction
4. First feature use
5. Feature completion (activation)

**SQL:**

```sql
WITH user_journey AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'onboarding_completed' THEN 1 ELSE 0 END) as step1,
    MAX(CASE WHEN event_name = 'screen_viewed' THEN 1 ELSE 0 END) as step2,
    MAX(CASE WHEN event_name IN ('feature_used', 'content_created', 'search_performed')
      THEN 1 ELSE 0 END) as step3,
    MAX(CASE WHEN event_name = 'feature_used' THEN 1 ELSE 0 END) as step4,
    MAX(CASE WHEN event_name = 'feature_completed' THEN 1 ELSE 0 END) as step5
  FROM events
  WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY user_id
)
SELECT
  'Onboarded' as stage, SUM(step1) as users,
  NULL as dropped, NULL as drop_rate
FROM user_journey WHERE step1 = 1
UNION ALL
SELECT
  'Viewed app',
  SUM(CASE WHEN step1 = 1 AND step2 = 1 THEN 1 ELSE 0 END),
  SUM(CASE WHEN step1 = 1 AND step2 = 0 THEN 1 ELSE 0 END),
  ROUND(100.0 * SUM(CASE WHEN step1 = 1 AND step2 = 0 THEN 1 ELSE 0 END) /
    NULLIF(SUM(step1), 0), 1)
FROM user_journey
UNION ALL
SELECT
  'First interaction',
  SUM(CASE WHEN step2 = 1 AND step3 = 1 THEN 1 ELSE 0 END),
  SUM(CASE WHEN step2 = 1 AND step3 = 0 THEN 1 ELSE 0 END),
  ROUND(100.0 * SUM(CASE WHEN step2 = 1 AND step3 = 0 THEN 1 ELSE 0 END) /
    NULLIF(SUM(step2), 0), 1)
FROM user_journey
UNION ALL
SELECT
  'Used feature',
  SUM(CASE WHEN step3 = 1 AND step4 = 1 THEN 1 ELSE 0 END),
  SUM(CASE WHEN step3 = 1 AND step4 = 0 THEN 1 ELSE 0 END),
  ROUND(100.0 * SUM(CASE WHEN step3 = 1 AND step4 = 0 THEN 1 ELSE 0 END) /
    NULLIF(SUM(step3), 0), 1)
FROM user_journey
UNION ALL
SELECT
  'Activated',
  SUM(CASE WHEN step4 = 1 AND step5 = 1 THEN 1 ELSE 0 END),
  SUM(CASE WHEN step4 = 1 AND step5 = 0 THEN 1 ELSE 0 END),
  ROUND(100.0 * SUM(CASE WHEN step4 = 1 AND step5 = 0 THEN 1 ELSE 0 END) /
    NULLIF(SUM(step4), 0), 1)
FROM user_journey;
```

---

### 6. Session depth before activation

**Chart type:** Box plot or distribution

**Metrics:**
- Sessions before activation
- Screens viewed before activation
- Actions taken before activation

**SQL:**

```sql
WITH activation_session AS (
  SELECT
    user_id,
    MIN(CASE WHEN event_name = 'feature_completed' THEN session_id END) as activation_session
  FROM events e
  JOIN (
    SELECT user_id, session_id, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY MIN(timestamp)) as session_num
    FROM events
    GROUP BY user_id, session_id
  ) s USING (user_id, session_id)
  WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY user_id
),
session_counts AS (
  SELECT
    e.user_id,
    COUNT(DISTINCT e.session_id) as sessions_before,
    COUNT(DISTINCT CASE WHEN event_name = 'screen_viewed' THEN e.timestamp END) as screens,
    COUNT(*) as total_events
  FROM events e
  JOIN activation_session a USING (user_id)
  WHERE e.timestamp < (
    SELECT MIN(timestamp) FROM events e2
    WHERE e2.user_id = e.user_id AND e2.event_name = 'feature_completed'
  )
  GROUP BY e.user_id
)
SELECT
  CASE
    WHEN sessions_before = 1 THEN '1 session'
    WHEN sessions_before <= 3 THEN '2-3 sessions'
    WHEN sessions_before <= 5 THEN '4-5 sessions'
    ELSE '6+ sessions'
  END as sessions_bucket,
  COUNT(*) as users,
  ROUND(AVG(screens), 1) as avg_screens,
  ROUND(AVG(total_events), 1) as avg_events
FROM session_counts
GROUP BY 1
ORDER BY MIN(sessions_before);
```

---

## Alerts

### Critical

| Alert | Condition | Action |
|-------|-----------|--------|
| Activation crash | Rate drops > 20% day-over-day | Check for bugs, crashes |
| Time to activate spike | Median > 2x baseline | Review UX flow |

### Warning

| Alert | Condition | Action |
|-------|-----------|--------|
| Feature adoption drop | < 30% trying core feature | Add nudges, improve discoverability |
| Platform disparity | iOS/Android diff > 20% | Platform-specific investigation |

---

## PostHog insight config

```json
{
  "name": "Activation Analysis",
  "panels": [
    {
      "id": "activation_rate",
      "type": "trends",
      "events": [
        {"id": "feature_completed", "math": "unique_users"}
      ],
      "compare": true,
      "compare_to": "-7d"
    },
    {
      "id": "activation_funnel",
      "type": "funnels",
      "events": [
        {"id": "onboarding_completed"},
        {"id": "screen_viewed"},
        {"id": "feature_used"},
        {"id": "feature_completed"}
      ],
      "funnel_viz_type": "steps"
    },
    {
      "id": "features",
      "type": "trends",
      "events": [{"id": "feature_used"}],
      "breakdown": "feature_name",
      "display": "ActionsBarValue"
    }
  ]
}
```

---

## Cohort analysis

Track activation rate by install week:

```sql
WITH weekly_cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('week', MIN(timestamp)) as cohort_week
  FROM events
  WHERE event_name = 'onboarding_completed'
  GROUP BY user_id
),
activated AS (
  SELECT DISTINCT user_id, 1 as activated
  FROM events
  WHERE event_name = 'feature_completed'
)
SELECT
  cohort_week,
  COUNT(DISTINCT c.user_id) as cohort_size,
  COUNT(DISTINCT a.user_id) as activated,
  ROUND(100.0 * COUNT(DISTINCT a.user_id) / COUNT(DISTINCT c.user_id), 1) as activation_rate
FROM weekly_cohorts c
LEFT JOIN activated a USING (user_id)
GROUP BY cohort_week
ORDER BY cohort_week DESC
LIMIT 12;
```

---

## Refresh schedule

- Real-time: Activation events (for debugging)
- Hourly: Activation rate, funnel drop-offs
- Daily: Time to activate, feature discovery
- Weekly: Cohort activation analysis
