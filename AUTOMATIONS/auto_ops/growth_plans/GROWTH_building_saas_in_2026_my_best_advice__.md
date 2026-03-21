# Growth Plan: Building SaaS in 2026? My best advice * Offer Google login. 

**Created:** 2026-03-20 18:35
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $0-100/mo

---

## Tactics

1. Add Google OAuth to all apps to reduce signup friction (stated: most users won't bother without it)
2. Implement streak-based retention loops in all streak apps (retention 25x cheaper than acquisition)
3. Add share/referral buttons to all apps for organic viral loops
4. 80/20 rule: dedicate 4x more time to marketing existing apps vs building new ones

## Budget Tier Strategies

### FREE
Google OAuth via Firebase Auth (already have Firebase MCP), share buttons, OG meta tags, streak push notifications, referral program with vanity URLs

### LOW
$0-50/mo: targeted Reddit/Twitter posts about each app weekly, ProductHunt launches for top 5 apps

### MID
$50-200/mo: retargeting ads for users who visited but didn't sign up, email re-engagement drip sequences

## Daily Actions

- [ ] Build dag_runner script that crawls OPS/DEPLOYMENT_URLS.md for all live app URLs
- [ ] For each app: fetch HTML, check for Google sign-in button, Stripe/payment link, retention elements (notifications, streak UI, email capture), marketing elements (OG tags, share buttons, referral link)
- [ ] Generate compliance scorecard CSV in LEDGER/APP_SAAS_COMPLIANCE.csv
- [ ] Route top-priority fixes (missing payment links first, then OAuth, then retention) to app_factory_autopilot queue
- [ ] Schedule weekly Monday 7 AM cron to re-audit and track improvement over time
- [ ] Generate 3 tweets from audit findings (Rule 9): 'audited 47 apps against SaaS best practices, here is what I found'

## Tooling

```json
{
  "browser": "playwright_mcp for app auditing",
  "email": "none",
  "content": "content_factory for marketing posts per app"
}
```
