# Growth Plan:  you don’t realise how early you are so many people are miss

**Created:** 2026-03-20 18:10
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. SEO longtail pages targeting 'best X for Y' buyer-intent keywords with affiliate links
2. Reddit value-posts in relevant subreddits with subtle tool recommendations
3. Cross-pollinate: every app landing page gets a 'tools we use' affiliate section
4. Repurpose comparison articles into Twitter threads and TikTok scripts
5. Engagement warming on affiliate-heavy niches before posting affiliate content

## Budget Tier Strategies

### FREE
AI-generated SEO articles on surge.sh landing pages, Reddit organic posts, Twitter threads with affiliate CTAs, cross-link from existing 47 deployed sites

### LOW
$0-50/mo: Upgrade surge to Plus for custom domains and robots.txt, boosted pins on Pinterest for affiliate reviews

### MID
$50-200/mo: Micro-influencer seeding of comparison articles, paid Reddit promoted posts in buyer-intent subreddits

## Daily Actions

- [ ] 1. Scan existing LEDGER/APP_CLONE_OPPORTUNITIES.csv and LEDGER/TOOLS_SERVICES_MASTER.csv for products with affiliate programs accepting free signups
- [ ] 2. Create ai_organic_affiliate_engine.py that uses claude -p to batch-generate 'best X vs Y' comparison articles optimized for buyer-intent longtail keywords
- [ ] 3. Wire into existing generate-longtail skill to produce SEO affiliate pages at scale
- [ ] 4. Add affiliate CTA sections to existing 47 deployed landing pages (cross-pollination)
- [ ] 5. Queue social snippets from each article to CONTENT/social/posting_queue/ with affiliate links
- [ ] 6. Add cron at 7 AM daily to generate 3 new affiliate content pieces
- [ ] 7. BLOCKER: Human must sign up for affiliate programs (already tracked in PERSISTENT_TASK_TRACKER as P0)

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + generate_longtail + engagement_bait_converter"
}
```
