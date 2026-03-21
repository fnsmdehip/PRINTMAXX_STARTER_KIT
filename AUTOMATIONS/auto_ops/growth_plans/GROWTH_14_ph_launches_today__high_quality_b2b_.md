# Growth Plan: 14 PH launches today - HIGH quality B2B leads. 48h outreach 

**Created:** 2026-03-20 18:09
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. Reply to PH launch threads with genuine congrats + subtle mention before emailing (warms the cold touch)
2. Cross-reference PH makers with Twitter — follow + engage before outreach
3. Offer free landing page audit as lead magnet (we can auto-generate via existing scripts)
4. Track which PH categories yield highest reply rates and double down
5. Use PH maker mutual connections as social proof in email

## Budget Tier Strategies

### FREE
PH API scraping + custom email composer via claude -p + manual Gmail sending. Reply to PH threads for warm touches. Cross-pollinate with Twitter engagement.

### LOW
$0-50/mo: Hunter.io paid tier for better email enrichment (150 requests/mo free may suffice). Instantly free tier for sending automation.

### MID
$50-200/mo: Instantly paid for volume sending + auto follow-ups. Apollo.io for deeper founder enrichment. A/B test subject lines at scale.

## Daily Actions

- [ ] 1. Build ph_launch_outreach_pipeline.py that scrapes PH daily launches (extend existing ph_scrape_latest.csv flow)
- [ ] 2. Add B2B qualifier: filter by category tags (SaaS, developer tools, productivity, B2B), presence of pricing page, team indicators
- [ ] 3. Add founder email extraction: scrape maker profiles for Twitter/LinkedIn/website, check website contact pages, use Hunter.io free tier
- [ ] 4. Build email composer using claude -p: congrats template + product-specific compliment + value offer (landing page audit / beta access / growth tips)
- [ ] 5. Wire into LEDGER/OUTREACH_PIPELINE.csv with status tracking and 48h follow-up scheduling
- [ ] 6. Add cron at 7 AM daily (PH launches midnight PT, gives 7h for processing before business hours)
- [ ] 7. Warm touch: auto-comment on PH launch thread before sending email (uses existing engagement patterns)
- [ ] 8. Track reply rates by PH category to optimize targeting over time

## Tooling

```json
{
  "browser": "playwright for PH scraping",
  "email": "custom cold email scripts + Gmail SMTP",
  "content": "claude -p for email personalization"
}
```
