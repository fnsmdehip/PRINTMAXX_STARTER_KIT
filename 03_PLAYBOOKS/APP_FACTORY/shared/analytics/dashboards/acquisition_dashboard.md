# Acquisition Dashboard

Metrics and queries for tracking user acquisition performance.

---

## Key metrics

| Metric | Target | Alert |
|--------|--------|-------|
| Daily installs | Varies by spend | < 50% of avg |
| Onboarding completion | > 70% | < 50% |
| CAC | < LTV/3 | > LTV/2 |
| Install to D1 active | > 40% | < 25% |

---

## Dashboard sections

### 1. Install volume

**Chart type:** Line chart (daily) + Bar chart (by source)

**Metrics:**
- Total installs (today, 7d, 30d)
- Installs by source (organic, paid, referral)
- Install trend vs previous period

**Mixpanel query:**

```javascript
// Installs over time
{
  event: 'onboarding_started',
  from_date: '-30d',
  to_date: 'today',
  type: 'general',
  unit: 'day',
  breakdowns: [{ property: 'source', type: 'event' }]
}
```

**SQL:**

```sql
SELECT
  DATE(timestamp) as date,
  properties->>'source' as source,
  COUNT(DISTINCT user_id) as installs
FROM events
WHERE event_name = 'onboarding_started'
  AND timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(timestamp), properties->>'source'
ORDER BY date, source;
```

---

### 2. Onboarding funnel

**Chart type:** Funnel visualization

**Steps:**
1. Onboarding started
2. Screen 1 viewed
3. Screen 2 viewed
4. Permissions granted
5. Onboarding completed

**Mixpanel funnel:**

```javascript
{
  name: 'Onboarding Funnel',
  steps: [
    { event: 'onboarding_started' },
    { event: 'onboarding_screen_viewed', filters: { screen_index: 0 } },
    { event: 'onboarding_screen_viewed', filters: { screen_index: 1 } },
    { event: 'permission_granted' },
    { event: 'onboarding_completed' }
  ],
  conversionWindow: 24 * 7, // 7 days
  groupBy: 'platform'
}
```

**SQL:**

```sql
WITH steps AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'onboarding_started' THEN 1 ELSE 0 END) as s1,
    MAX(CASE WHEN event_name = 'onboarding_screen_viewed'
      AND (properties->>'screen_index')::int = 0 THEN 1 ELSE 0 END) as s2,
    MAX(CASE WHEN event_name = 'onboarding_screen_viewed'
      AND (properties->>'screen_index')::int = 1 THEN 1 ELSE 0 END) as s3,
    MAX(CASE WHEN event_name = 'permission_granted' THEN 1 ELSE 0 END) as s4,
    MAX(CASE WHEN event_name = 'onboarding_completed' THEN 1 ELSE 0 END) as s5
  FROM events
  WHERE timestamp >= CURRENT_DATE - INTERVAL '7 days'
  GROUP BY user_id
)
SELECT
  'Started' as step, SUM(s1) as users, 100.0 as pct
FROM steps
UNION ALL
SELECT 'Screen 1', SUM(s2), ROUND(100.0 * SUM(s2) / NULLIF(SUM(s1), 0), 1) FROM steps
UNION ALL
SELECT 'Screen 2', SUM(s3), ROUND(100.0 * SUM(s3) / NULLIF(SUM(s1), 0), 1) FROM steps
UNION ALL
SELECT 'Permissions', SUM(s4), ROUND(100.0 * SUM(s4) / NULLIF(SUM(s1), 0), 1) FROM steps
UNION ALL
SELECT 'Completed', SUM(s5), ROUND(100.0 * SUM(s5) / NULLIF(SUM(s1), 0), 1) FROM steps;
```

---

### 3. Source performance

**Chart type:** Table with sparklines

**Columns:**
- Source name
- Install count
- Onboarding completion %
- D1 retention %
- Cost (if available)
- CAC

**SQL:**

```sql
WITH source_metrics AS (
  SELECT
    properties->>'source' as source,
    COUNT(DISTINCT CASE WHEN event_name = 'onboarding_started'
      THEN user_id END) as installs,
    COUNT(DISTINCT CASE WHEN event_name = 'onboarding_completed'
      THEN user_id END) as completed,
    COUNT(DISTINCT CASE WHEN event_name = 'session_started'
      AND DATE(timestamp) > DATE(first_seen.first_date)
      THEN user_id END) as d1_active
  FROM events
  LEFT JOIN (
    SELECT user_id, MIN(DATE(timestamp)) as first_date
    FROM events WHERE event_name = 'onboarding_started'
    GROUP BY user_id
  ) first_seen USING (user_id)
  WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY properties->>'source'
)
SELECT
  source,
  installs,
  ROUND(100.0 * completed / NULLIF(installs, 0), 1) as completion_pct,
  ROUND(100.0 * d1_active / NULLIF(installs, 0), 1) as d1_retention_pct
FROM source_metrics
ORDER BY installs DESC;
```

---

### 4. Permission acceptance

**Chart type:** Stacked bar chart

**Metrics by permission type:**
- Notifications: granted/denied %
- Tracking (ATT): granted/denied %
- Camera: granted/denied %
- Photos: granted/denied %

**SQL:**

```sql
SELECT
  properties->>'permission_type' as permission,
  COUNT(CASE WHEN event_name = 'permission_granted' THEN 1 END) as granted,
  COUNT(CASE WHEN event_name = 'permission_denied' THEN 1 END) as denied,
  ROUND(100.0 * COUNT(CASE WHEN event_name = 'permission_granted' THEN 1 END) /
    NULLIF(COUNT(*), 0), 1) as grant_rate
FROM events
WHERE event_name IN ('permission_granted', 'permission_denied')
  AND timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY properties->>'permission_type';
```

---

### 5. Time to complete onboarding

**Chart type:** Histogram

**Buckets:**
- < 30 seconds
- 30s - 1 minute
- 1-2 minutes
- 2-5 minutes
- 5+ minutes
- Abandoned

**SQL:**

```sql
WITH completion_times AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'onboarding_started' THEN timestamp END) as started,
    MAX(CASE WHEN event_name = 'onboarding_completed' THEN timestamp END) as completed
  FROM events
  WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY user_id
)
SELECT
  CASE
    WHEN completed IS NULL THEN 'Abandoned'
    WHEN EXTRACT(EPOCH FROM (completed - started)) < 30 THEN '< 30s'
    WHEN EXTRACT(EPOCH FROM (completed - started)) < 60 THEN '30s - 1m'
    WHEN EXTRACT(EPOCH FROM (completed - started)) < 120 THEN '1-2m'
    WHEN EXTRACT(EPOCH FROM (completed - started)) < 300 THEN '2-5m'
    ELSE '5m+'
  END as time_bucket,
  COUNT(*) as users,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) as pct
FROM completion_times
GROUP BY 1
ORDER BY
  CASE time_bucket
    WHEN '< 30s' THEN 1
    WHEN '30s - 1m' THEN 2
    WHEN '1-2m' THEN 3
    WHEN '2-5m' THEN 4
    WHEN '5m+' THEN 5
    ELSE 6
  END;
```

---

### 6. Geographic distribution

**Chart type:** World map heat map + Table

**Metrics by country:**
- Install count
- Onboarding completion %
- Revenue potential

**SQL:**

```sql
SELECT
  properties->>'country' as country,
  COUNT(DISTINCT user_id) as installs,
  ROUND(100.0 * COUNT(DISTINCT CASE WHEN event_name = 'onboarding_completed'
    THEN user_id END) / NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'onboarding_started'
    THEN user_id END), 0), 1) as completion_rate
FROM events
WHERE event_name IN ('onboarding_started', 'onboarding_completed')
  AND timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY properties->>'country'
ORDER BY installs DESC
LIMIT 20;
```

---

## Alerts

### Critical

| Alert | Condition | Action |
|-------|-----------|--------|
| Install drop | < 50% of 7d avg | Check attribution, app store |
| Onboarding failure | < 40% completion | Review UX, check for crashes |

### Warning

| Alert | Condition | Action |
|-------|-----------|--------|
| Permission decline | > 60% denied | Review permission prompts |
| Source quality drop | D1 < 20% for source | Adjust targeting |

---

## PostHog insight config

```json
{
  "name": "Acquisition Overview",
  "panels": [
    {
      "id": "installs",
      "type": "trends",
      "events": [{"id": "onboarding_started"}],
      "display": "ActionsLineGraph",
      "interval": "day"
    },
    {
      "id": "onboarding_funnel",
      "type": "funnels",
      "events": [
        {"id": "onboarding_started"},
        {"id": "onboarding_completed"}
      ],
      "breakdown": "platform"
    },
    {
      "id": "sources",
      "type": "trends",
      "events": [{"id": "onboarding_started"}],
      "breakdown": "source",
      "display": "ActionsBarValue"
    }
  ]
}
```

---

## Refresh schedule

- Real-time: Install count, active onboarding
- Hourly: Funnel completion rates
- Daily: Source performance, geographic data
- Weekly: Cohort quality analysis
