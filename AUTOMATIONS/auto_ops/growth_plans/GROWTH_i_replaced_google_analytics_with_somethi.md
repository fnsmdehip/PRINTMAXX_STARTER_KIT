# Growth Plan: I replaced Google Analytics with something that actually sho

**Created:** 2026-03-20 18:09
**Venture:** RESEARCH
**Budget Tier:** FREE
**Revenue Est:** $0/mo direct (infrastructure optimization — value unlocks when revenue starts, prevents scaling wrong channel)

---

## Tactics

1. UTM-tag every outbound link in social posts and cold emails
2. Add ?ref= param to all cross-site links between our 47+ properties for internal attribution

## Budget Tier Strategies

### FREE
Custom JS snippet on all landing pages logs referrer + UTM to localStorage, beacon to local endpoint. Python script aggregates weekly. No GA, no paid tool.

### LOW
$0-10/mo: Umami self-hosted (OSS, Docker) for real-time dashboard if local JSONL gets unwieldy

### MID
$50/mo: PostHog free tier (1M events/mo) for full funnel analysis once revenue exceeds $500/mo

## Daily Actions

- [ ] Create revenue_attribution_tracker.py that generates a <200 byte JS snippet logging referrer, UTM params, and payment-link click events
- [ ] Batch-inject snippet into all HTML files under LANDING/ and MONEY_METHODS/APP_FACTORY/builds/ via Python string replace
- [ ] Create weekly cron (Monday 7 AM) that aggregates click data into LEDGER/REVENUE_ATTRIBUTION.csv
- [ ] Add UTM params to all outbound links in CONTENT/social/posting_queue/ templates

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "none"
}
```
