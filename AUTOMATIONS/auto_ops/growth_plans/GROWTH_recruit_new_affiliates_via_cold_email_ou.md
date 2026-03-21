# Growth Plan: recruit new affiliates via cold email outreach

**Created:** 2026-03-20 13:50
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo

---

## Tactics

1. Scrape competitor affiliate pages for their existing affiliates and poach them with better commission rates
2. Monitor r/Affiliatemarketing for people asking 'what should I promote' and DM/reply with our program
3. Create affiliate resource kit (banners, copy, landing page links) so recruits convert faster

## Budget Tier Strategies

### FREE
Cold email via custom SMTP, scrape Reddit/Twitter for prospects, reply engagement in affiliate subreddits, create affiliate signup page on existing surge.sh infrastructure

### LOW
$0-50/mo: Use Instantly free tier for email warmup, create dedicated affiliate landing page with tracking links

### MID
$50-200/mo: Run micro-targeted ads on Reddit/Twitter to affiliate marketers, offer signup bonuses

## Daily Actions

- [ ] Reuse existing cold email patterns from eas_lead_pipeline.py and procedural memory
- [ ] Build affiliate_recruiter_cold_outreach.py with scrape→qualify→email pipeline
- [ ] Create affiliate program page listing commission rates (30-50%) for our products
- [ ] Schedule weekly cron (Monday 7 AM) to scrape new prospects and send batch
- [ ] Track replies and affiliate signups in affiliate_performance.json
- [ ] Feed successful email templates back into procedural memory

## Tooling

```json
{
  "browser": "none",
  "email": "custom SMTP cold email script (reuse eas_lead_pipeline patterns)",
  "content": "claude -p for personalized email generation"
}
```
