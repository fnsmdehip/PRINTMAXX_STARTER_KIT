# Growth Plan:  curious on what the best methods of earnings affiliate inco

**Created:** 2026-03-20 18:09
**Venture:** MONETIZE
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo

---

## Tactics

1. SEO longtail pages targeting 'best X vs Y' buyer-intent keywords
2. Cross-pollinate affiliate links into existing 47 deployed sites
3. Reddit value posts in r/affiliatemarketing r/passive_income with soft CTAs
4. Programmatic affiliate comparison pages at scale via generate-longtail skill

## Budget Tier Strategies

### FREE
Programmatic SEO comparison pages, embed affiliate links in existing 47 sites, Reddit/forum value posts with affiliate CTAs, email list affiliate recommendations

### LOW
$0-50/mo: Pinterest pins linking to affiliate pages, boosted social posts on top performers

### MID
$50-200/mo: Paid search on high-intent 'best X alternative' keywords, micro-influencer affiliate content seeding

## Daily Actions

- [ ] 1. Scan existing LEDGER/AFFILIATE files and OPS/AFFILIATE_OPPORTUNITIES_MAR08.md for current state
- [ ] 2. Build affiliate_income_optimizer.py that scrapes top digital product affiliate programs (SaaS tools, course platforms, AI tools) filtering for free signup + 20%+ commission
- [ ] 3. Cross-reference with existing affiliate-pages in LANDING/affiliate-pages/ to avoid duplication
- [ ] 4. Generate new comparison/review landing pages using content_multiplier for top 10 programs
- [ ] 5. Embed affiliate links into existing 47 deployed sites where contextually relevant
- [ ] 6. Queue social content promoting affiliate pages via posting_queue
- [ ] 7. Wire into existing chain_recruit_new_affiliates_via_cold_email_ou for affiliate manager relationship building
- [ ] 8. BLOCKER: Human must sign up for affiliate programs (already tracked in PERSISTENT_TASK_TRACKER)
- [ ] 9. Schedule weekly cron to refresh program data and generate new pages for trending products

## Tooling

```json
{
  "browser": "playwright for program signup verification",
  "email": "cold email scripts for affiliate manager outreach",
  "content": "content_multiplier + generate-longtail for comparison pages"
}
```
