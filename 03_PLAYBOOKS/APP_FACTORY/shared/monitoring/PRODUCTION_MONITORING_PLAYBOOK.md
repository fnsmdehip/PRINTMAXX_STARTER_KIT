# Production Monitoring Playbook

Operational guide for monitoring React Native apps in production.

## What to Monitor

### Core Health Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Crash-free sessions | >99.5% | <99% | <97% |
| Crash-free users | >99.5% | <99% | <97% |
| App startup time | <2s | >3s | >5s |
| Error rate | <0.1% | >1% | >5% |
| API success rate | >99% | <98% | <95% |

### Performance Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Screen render time | <300ms | >500ms | >1s |
| Time to interactive | <3s | >5s | >8s |
| API latency (p50) | <200ms | >500ms | >1s |
| API latency (p95) | <500ms | >1s | >3s |
| Memory usage | <200MB | >300MB | >500MB |

### Business Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Payment success rate | >98% | <95% | <90% |
| Session duration | Baseline +/-20% | -30% | -50% |
| DAU/MAU ratio | Baseline | -20% | -40% |

---

## Alert Configuration

### Sentry Alert Rules

```yaml
# Critical: App crashing
- name: Crash Rate Critical
  conditions:
    - event_frequency > 100 per hour
    - tags.severity = fatal
  actions:
    - notify: pagerduty
    - notify: slack#incidents

# High: Error spike
- name: Error Spike
  conditions:
    - event_frequency > 10x baseline
    - time_window: 15 minutes
  actions:
    - notify: slack#alerts
    - assign: on-call

# Medium: New issue
- name: New Error Type
  conditions:
    - is_first_seen: true
    - tags.severity in [error, fatal]
  actions:
    - notify: slack#errors
```

### PagerDuty Escalation

```yaml
escalation_policy:
  name: Mobile App Critical
  levels:
    - level: 1
      delay: 0 minutes
      targets:
        - type: on_call
          schedule: mobile-primary
    - level: 2
      delay: 15 minutes
      targets:
        - type: on_call
          schedule: mobile-secondary
        - type: user
          id: engineering-lead
    - level: 3
      delay: 30 minutes
      targets:
        - type: user
          id: engineering-manager
```

---

## Incident Response

### Severity Classification

| Severity | Impact | Examples |
|----------|--------|----------|
| SEV-1 | All users affected | App crash on launch, auth completely broken |
| SEV-2 | Major feature broken | Payments failing, main screen blank |
| SEV-3 | Minor feature broken | Settings not saving, image upload failing |
| SEV-4 | Cosmetic/edge case | Wrong color, rare device issue |

### Response Workflow

```
Alert Triggered
    │
    ▼
┌─────────────────┐
│ Acknowledge     │ < 5 min
│ (PagerDuty)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Assess Severity │
│ & Impact        │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│ SEV-1 │ │ SEV-2+│
│ SEV-2 │ │       │
└───┬───┘ └───┬───┘
    │         │
    ▼         ▼
┌─────────┐ ┌─────────┐
│ War Room│ │ Async   │
│ (Slack) │ │ Ticket  │
└────┬────┘ └────┬────┘
     │           │
     ▼           ▼
  Mitigate    Schedule
  & Resolve   Fix
```

### War Room Checklist

For SEV-1/SEV-2 incidents:

1. **Acknowledge** alert within 5 minutes
2. **Communicate** in #incidents channel:
   ```
   INCIDENT: [Brief description]
   SEVERITY: SEV-[1/2]
   IMPACT: [% users, specific features]
   STATUS: Investigating
   COMMANDER: [@name]
   ```
3. **Assess** using monitoring dashboards:
   - Error rate trend
   - Affected versions
   - Geographic distribution
   - User segment impact
4. **Mitigate** immediately if possible:
   - Feature flag disable
   - Backend rollback
   - Force update prompt
5. **Resolve** root cause
6. **Communicate** resolution:
   ```
   RESOLVED: [Brief description]
   DURATION: [X hours/minutes]
   ROOT CAUSE: [One sentence]
   POSTMORTEM: [Link or ETA]
   ```

---

## Runbook: Common Issues

### App Crash on Launch

**Symptoms:** Crash-free rate drops, users report unable to open app

**Diagnosis:**
```
1. Check Sentry for crash group
2. Identify:
   - Affected versions
   - Device/OS distribution
   - Recent release correlation
3. Pull crash logs and stack trace
```

**Mitigation:**
```
1. IF affects <5% users AND recent release:
   - Roll back release
   - Disable feature flags for new code

2. IF affects specific versions:
   - Force update prompt via remote config

3. IF affects specific devices:
   - Add device check, graceful degradation
```

---

### Payment Failures

**Symptoms:** Payment error rate >5%, user complaints about purchases

**Diagnosis:**
```
1. Check payment error category breakdown
2. Identify:
   - Store (iOS/Android)
   - Product IDs affected
   - Error codes
3. Check backend payment webhook status
```

**Mitigation:**
```
1. IF store outage:
   - Show maintenance message
   - Monitor store status page

2. IF backend issue:
   - Check RevenueCat/backend status
   - Roll back backend changes

3. IF client issue:
   - Disable affected purchase flow
   - Release hotfix
```

---

### Slow Performance

**Symptoms:** Startup time >5s, screen renders >1s, user complaints

**Diagnosis:**
```
1. Check performance dashboard trends
2. Identify:
   - Affected screens
   - Recent code changes
   - Device/OS distribution
3. Profile with React DevTools or native profiler
```

**Mitigation:**
```
1. IF specific screen:
   - Lazy load heavy components
   - Memoize expensive calculations
   - Defer non-critical data fetching

2. IF global:
   - Review recent changes for performance impact
   - Check for memory leaks
   - Reduce bundle size
```

---

### Authentication Issues

**Symptoms:** Login failures >10%, session drops, unauthorized errors

**Diagnosis:**
```
1. Check auth error breakdown
2. Identify:
   - OAuth provider status
   - Token expiration patterns
   - Backend auth service status
3. Test auth flow manually
```

**Mitigation:**
```
1. IF provider outage:
   - Show provider status message
   - Enable backup auth method

2. IF token issues:
   - Force token refresh
   - Clear cached tokens

3. IF backend issue:
   - Roll back auth service changes
   - Enable maintenance mode
```

---

## Post-Mortem Template

After SEV-1/SEV-2 incidents, complete within 48 hours:

```markdown
# Incident Post-Mortem: [Title]

**Date:** YYYY-MM-DD
**Duration:** X hours Y minutes
**Severity:** SEV-[1/2]
**Author:** @name

## Summary

One paragraph describing what happened and impact.

## Impact

- Users affected: X (Y%)
- Sessions affected: X
- Revenue impact: $X (estimated)
- Brand/trust impact: [Low/Medium/High]

## Timeline

| Time (UTC) | Event |
|------------|-------|
| HH:MM | Alert triggered |
| HH:MM | Acknowledged by @name |
| HH:MM | Root cause identified |
| HH:MM | Mitigation deployed |
| HH:MM | Incident resolved |

## Root Cause

Detailed technical explanation of what caused the incident.

## Resolution

What was done to fix the immediate issue.

## Prevention

### What went well
- Item 1
- Item 2

### What could be improved
- Item 1
- Item 2

### Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Add test coverage for X | @name | YYYY-MM-DD | Pending |
| Improve alert threshold | @name | YYYY-MM-DD | Pending |
| Document runbook for Y | @name | YYYY-MM-DD | Pending |

## Lessons Learned

Key takeaways for the team.
```

---

## Daily Operations

### Morning Check (5 min)

```
1. Check crash-free rate (should be >99%)
2. Review new error types from last 24h
3. Check payment success rate
4. Review any overnight alerts
```

### Weekly Review (30 min)

```
1. Error trend analysis
   - New errors introduced
   - Error rate by release
   - Top 10 errors by volume

2. Performance review
   - Startup time trend
   - Screen render times
   - API latency percentiles

3. User impact review
   - Users affected by errors
   - Support tickets correlation
   - App store reviews

4. Action items from incidents
   - Review pending action items
   - Prioritize for sprint
```

### Release Monitoring

After each release:

```
Day 1: Monitor hourly
- Crash-free rate vs baseline
- Error rate vs baseline
- New error types

Day 2-3: Monitor daily
- Performance metrics
- User feedback
- Support tickets

Day 7: Release retrospective
- Document any issues
- Update monitoring thresholds
- Plan improvements
```

---

## Dashboard Views

### Executive Dashboard

Shows high-level health for stakeholders:
- Crash-free rate (7-day rolling)
- Error rate (7-day rolling)
- App rating (App Store + Play Store)
- Active users trend

### Engineering Dashboard

Shows detailed technical metrics:
- Errors by category
- Performance percentiles
- Release comparison
- Device/OS breakdown

### On-Call Dashboard

Shows immediate health status:
- Real-time error rate
- Active incidents
- Recent alerts
- Quick links to runbooks

---

## Tools Quick Reference

| Tool | Purpose | URL |
|------|---------|-----|
| Sentry | Crash/error tracking | sentry.io |
| PagerDuty | On-call alerts | pagerduty.com |
| Slack | Incident communication | #incidents, #alerts |
| Grafana | Metrics dashboards | Internal |
| App Store Connect | iOS metrics | appstoreconnect.apple.com |
| Play Console | Android metrics | play.google.com/console |

---

## Contacts

| Role | Contact |
|------|---------|
| On-call primary | Check PagerDuty schedule |
| On-call secondary | Check PagerDuty schedule |
| Engineering lead | @lead |
| Product manager | @pm |
| Support escalation | @support-lead |
