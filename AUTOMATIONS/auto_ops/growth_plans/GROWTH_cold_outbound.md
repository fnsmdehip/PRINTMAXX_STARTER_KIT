# Growth Plan: COLD_OUTBOUND

**Created:** 2026-03-20 18:09
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $500-2000/mo

---

## Tactics

1. Multi-domain warm-up: 3 domains rotating, 5 emails/day/domain ramp over 14 days
2. Signal stacking: leads with 2+ intent signals get priority (hired + raised = hot)
3. Reply-to-thread mining: scrape Reddit/HN threads where ICP complains about problem we solve
4. Referral loop: positive replies get asked for warm intros to similar companies
5. Content-to-outbound: use our CONTENT venture posts as social proof links in cold emails

## Budget Tier Strategies

### FREE
Custom SMTP via free email providers (Zoho free tier, 3 domains at ~$10/yr each from Namecheap), Hunter.io free 25 searches/mo + custom email pattern guessing, Claude Max for personalization, Reddit/HN/Crunchbase free scraping

### LOW
$0-50/mo: 1 cheap SMTP relay (Amazon SES at $0.10/1K emails), Namecheap domains for sender rotation, paid Hunter.io for 500 searches/mo

### MID
$50-200/mo: Dedicated warm-up service (Warmup Inbox $15/mo), multiple SES accounts, Apollo.io basic for enrichment, 5+ sending domains

## Daily Actions

- [ ] 1. Create intent_signal_cold_outbound.py with DAG orchestration for 4 parallel signal sources
- [ ] 2. Wire into existing chain_recruit_new_affiliates_via_cold_email_ou for sender infrastructure
- [ ] 3. Build email pattern guesser (firstname@domain, f.last@domain, etc.) to avoid paid enrichment
- [ ] 4. Create 3 cold email templates by signal type: hiring-trigger, funding-trigger, pain-point-trigger
- [ ] 5. Add claude -p personalization step that references the specific trigger event in first line
- [ ] 6. Set up Zoho free SMTP accounts on 3 domains (HUMAN: domain purchase needed ~$30 one-time)
- [ ] 7. Create warm-up schedule: 5 emails/day/domain for 14 days before real sends
- [ ] 8. Wire cron at 6:30 AM daily: scrape signals → enrich → personalize → queue for send
- [ ] 9. Add reply tracking: IMAP check on sender accounts, log to OUTREACH_PIPELINE.csv
- [ ] 10. KPI entry: daily leads scraped, emails sent, reply rate target >3%

## Tooling

```json
{
  "browser": "playwright MCP for scraping job boards and BuiltWith",
  "email": "custom Python smtplib + Zoho free SMTP (Phase 0), SES later",
  "content": "claude -p for personalization, existing content_factory for social proof assets",
  "enrichment": "hunter.io free tier + custom email pattern generator",
  "crm": "LEDGER/OUTREACH_PIPELINE.csv (existing)"
}
```
