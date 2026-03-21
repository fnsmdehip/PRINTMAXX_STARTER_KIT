# Growth Plan: [r/entrepreneur] Customer data for tailored notifications

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $0-30/mo direct (retention lift on existing apps improves IAP conversion marginally at current user scale)

---

## Tactics

1. Segment by streak milestone (3/7/14/30 days) — congratulation notifications drive social shares
2. Dormant re-engagement: users inactive 48h get personalized 'Your streak is at risk' push
3. Paywall proximity trigger: users who opened premium feature 3x without upgrading get limited-time offer notification
4. Time-of-day personalization: send at user's historical peak engagement hour (stored in Firebase user doc)

## Budget Tier Strategies

### FREE
Firebase FCM (free unlimited push) + segment logic in Python script + Claude-generated notification copy variants

### LOW
$0-20/mo — OneSignal free tier for A/B testing notification copy, track which variant drives more upgrades

### MID
$50-100/mo — Braze or Customer.io for advanced behavioral triggers if user base exceeds 10K

## Daily Actions

- [ ] Read Firebase Firestore user collection — extract last_open, streak_count, subscription_tier, notification_opt_in
- [ ] Segment into buckets: dormant (>48h), streak_at_risk (>20h no check-in), upgrade_candidate (3+ premium feature views), active (send nothing — don't spam engaged users)
- [ ] Generate notification copy per segment using claude -p with app-specific context
- [ ] Send via Firebase Admin SDK FCM — batch by segment, throttle to 200/min
- [ ] Write delivery log to Firebase — track open_rate, conversion per segment for next-cycle optimization

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "claude -p for notification copy generation",
  "backend": "Firebase Firestore + FCM"
}
```
