# Growth Plan: I built 8 email automations for my 322-user app  in one week

**Created:** 2026-03-20 18:35
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. Embed email capture popup on all 47 surge.sh apps with exit-intent trigger
2. Use app usage data as personalization attributes (streak count, last active, features used)
3. Cross-promote between app email lists (scripture-streak users get meditation-streak pitch)
4. A/B test subject lines using Claude -p for generation, pick winner after 50 sends
5. Referral sequence: users who hit 7-day streak get 'share with a friend' email with unique link
6. Win-back sequence fires after 3 days inactive with personalized 'you had X streak going'

## Budget Tier Strategies

### FREE
Brevo free tier (300 emails/day = 9K/mo), Firebase attribute sync via cron, Claude -p for copy generation, cross-app list cross-pollination, exit-intent popups on all apps

### LOW
$0-30/mo: Brevo Starter plan (20K emails/mo) if we exceed free tier, custom domain for sender reputation

### MID
$50-100/mo: Brevo Business for A/B testing + send time optimization + advanced segmentation

## Daily Actions

- [ ] Create Brevo account (HUMAN BLOCKER: 5 min signup)
- [ ] Build email_automation_engine.py: Brevo API wrapper for sequence CRUD, contact sync, attribute management
- [ ] Add minimal email capture form (name + email) to all 47 deployed apps via shared JS snippet
- [ ] Define 20+ contact attributes from app usage data (streak_count, last_active, app_name, days_since_signup, features_used, premium_status)
- [ ] Build Firebase-to-Brevo sync script, cron every 4 hours
- [ ] Create 8 sequence templates with Claude -p generated copy, personalized with {{attribute}} merge tags
- [ ] Deploy sequences in Brevo, wire triggers (signup=onboarding, 3d_inactive=winback, 7d_streak=referral)
- [ ] Add KPI tracking: daily open rate, CTR, conversion per sequence
- [ ] A/B test subject lines weekly, auto-promote winners

## Tooling

```json
{
  "browser": "none",
  "email": "Brevo free tier (300/day)",
  "content": "claude -p for email copy generation"
}
```
