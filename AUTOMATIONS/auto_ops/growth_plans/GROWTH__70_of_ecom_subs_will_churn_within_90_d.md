# Growth Plan:  70% of ecom subs will churn within 90 days and it has nothi

**Created:** 2026-03-20 18:10
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo

---

## Tactics

1. Post the 70% churn stat as a standalone tweet — controversial data gets quote-tweets
2. Reply to ecom influencers discussing subscriptions with the churn angle
3. Cross-post to r/ecommerce, r/shopify, r/entrepreneur with 'unpopular opinion' framing
4. Use the stat as cold email opener: 'Your subscription program is probably losing 70% in 90 days — here is why'

## Budget Tier Strategies

### FREE
Organic posts across Twitter/LinkedIn/Reddit using the churn stat as engagement bait. Reply to ecom threads. QT ecom influencer posts with the contrarian data point. Cold DMs to ecom brand founders.

### LOW
$0-50/mo: Boost top-performing churn post on Twitter. Small Reddit ad in r/ecommerce.

### MID
$50-200/mo: LinkedIn sponsored post targeting ecom founders. Retarget site visitors who clicked churn content with retention guide CTA.

## Daily Actions

- [ ] 1. Run engagement_bait_converter.py with the churn stat to generate 5+ posts (Twitter thread, LinkedIn post, Reddit post, QT bait, reply bait)
- [ ] 2. Queue all generated posts to CONTENT/social/posting_queue/
- [ ] 3. Draft cold email template using churn stat as opener, targeting Shopify subscription brands
- [ ] 4. Add ecom-subscription-brands as a lead category in outreach pipeline
- [ ] 5. Create DIGITAL_PRODUCTS/ready_to_sell/ecom_retention_playbook/ outline for future product
- [ ] 6. Schedule weekly content refresh (new angle on same data) via cron

## Tooling

```json
{
  "browser": "none",
  "email": "custom cold email scripts",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
