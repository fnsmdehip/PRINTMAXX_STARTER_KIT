# Growth Plan:  asked a guy at a hotel bar what he does"i sell the same pdf

**Created:** 2026-03-20 18:10
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $200-2000/mo

---

## Tactics

1. Free chapter/preview as lead magnet on landing pages we already have
2. Monthly update changelog posted as Twitter thread (Rule 9 content)
3. Reddit posts in niche subreddits showing before/after page count growth
4. Cross-sell from existing 47 deployed apps — upgrade CTA to subscription PDF
5. Testimonial-style posts: subscribers screenshot their growing PDF page count

## Budget Tier Strategies

### FREE
Lead magnet preview chapters on existing 47 surge.sh sites, Twitter threads from each monthly update, Reddit posts in relevant subreddits showing value-add, cross-promote from app factory landing pages

### LOW
$10-30/mo boosted tweets on update announcements, Product Hunt launch for each new PDF subscription product

### MID
$50-150/mo targeted ads to niche audiences (e.g. Claude Code users for our solopreneur PDF, faith communities for devotional PDFs)

## Daily Actions

- [ ] 1. Select top 3 existing PDF products from DIGITAL_PRODUCTS/ready_to_sell/ with highest niche demand
- [ ] 2. Build recurring_pdf_subscription_engine.py: reads base PDF, generates 3-4 update pages via Claude, merges into master, versions it
- [ ] 3. Wire Stripe subscription products ($9-19/mo tiers) via payment_integrator.py for each selected PDF
- [ ] 4. Create free preview chapter landing pages on existing surge.sh infrastructure
- [ ] 5. Add cron (1st of month 8AM) to auto-run the update DAG pipeline
- [ ] 6. Generate launch content: 3 tweets + 1 thread per PDF subscription product (Rule 9)
- [ ] 7. Add subscriber count and MRR tracking to KPI_DASHBOARD.md
- [ ] 8. After month 1: measure churn, adjust update frequency and page count based on retention data

## Tooling

```json
{
  "browser": "none",
  "email": "custom_stripe_webhook_emailer",
  "content": "claude_p_page_generator"
}
```
