# Growth Plan: Getting hit by a return scammer and don’t know what to do

**Created:** 2026-03-21 12:40
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $200-600/mo

---

## Tactics

1. Comment on return fraud threads with actionable free advice — builds authority, drives guide sales
2. Create 'Return Fraud Recovery Checklist' as free PDF lead magnet, gate behind email signup
3. Post weekly return fraud case study on r/Flipping as value content (no direct sell)
4. Target eBay/Mercari/Amazon seller Facebook groups with the same content
5. Build SEO page: 'what to do when buyer returns wrong item / empty box scam'

## Budget Tier Strategies

### FREE
Daily scrape of return fraud threads, empathetic comment replies linking free checklist, cross-post guide as native Reddit value post once/week, SEO landing page deployed to surge.sh

### LOW
$20-30 Reddit promoted post targeting r/Flipping and r/Ebay subscribers, boost best-performing organic post

### MID
Sponsor Flipper newsletter or YouTube channel, retarget checklist downloaders with guide upsell via Facebook pixel

## Daily Actions

- [ ] Run subagent to generate 'Return Fraud Protection Guide for Resellers' (20-page PDF, cover: empty box scams, wrong item returns, chargeback fraud, platform dispute templates)
- [ ] Create Gumroad listing at $17-27 (paste-ready listing in DIGITAL_PRODUCTS/ready_to_sell/)
- [ ] Deploy free checklist lead magnet as surge.sh landing page with email capture
- [ ] Wire return_fraud_pain_scraper.py: daily scrape of 4 subreddits, qualify threads, generate + queue comments
- [ ] Add cron 0 8 * * * for daily scrape cycle
- [ ] Route 3 social posts from best thread insights via engagement_bait_converter.py

## Tooling

```json
{
  "browser": "Playwright + Brave cookies (existing scraper infra)",
  "email": "Custom cold email script \u2014 capture emails via checklist gate",
  "content": "claude -p for comment generation + guide content, engagement_bait_converter.py for social posts"
}
```
