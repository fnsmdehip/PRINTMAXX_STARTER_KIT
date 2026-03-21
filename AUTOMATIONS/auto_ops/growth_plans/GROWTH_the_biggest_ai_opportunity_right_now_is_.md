# Growth Plan: the biggest AI opportunity right now is mid-market companies

**Created:** 2026-03-20 13:50
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $2000-5000/mo

---

## Tactics

1. Cold email founders directly with specific workflow pain points pulled from their own job postings (hyper-personalization)
2. LinkedIn content: post AI audit case studies targeting mid-market ops managers
3. Reddit /r/smallbusiness /r/entrepreneur posts about manual workflow hell with subtle CTA
4. Reply to mid-market founders complaining about manual processes on Twitter with free audit offer
5. Partner with fractional CTOs who serve mid-market — they see the pain but cant build the AI solution

## Budget Tier Strategies

### FREE
Cold email from scraped leads, LinkedIn organic posts about AI workflow audits, Twitter reply engagement to mid-market founder complaints, Reddit value posts in r/smallbusiness r/SaaS r/entrepreneur

### LOW
$20-50/mo for LinkedIn Sales Navigator basic to find ops/founder contacts at target companies, email warmup service

### MID
$100-200/mo for Apollo.io or similar B2B contact enrichment to get direct founder emails at scale + sponsored LinkedIn posts targeting mid-market ops directors

## Daily Actions

- [ ] 1. Build midmarket_ai_audit_scanner.py — scrapes Indeed/LinkedIn for companies posting manual-workflow roles in $5M-$50M band
- [ ] 2. Add AI-readiness scoring: legacy tech stack (BuiltWith), manual job density, no AI vendor detected, revenue band confirmation
- [ ] 3. Wire proposal generator: takes company pain signals from job posts, generates 1-page AI workflow audit offer
- [ ] 4. Connect to existing cold outbound pipeline (eas_lead_pipeline.py) for email delivery
- [ ] 5. Use procedural memory objection handling for follow-up sequences
- [ ] 6. Cron at 6:30 AM weekdays, feed qualified leads to outbound queue
- [ ] 7. Track: leads scraped, proposals sent, replies received, audits booked

## Tooling

```json
{
  "browser": "playwright for job board scraping",
  "email": "custom cold email scripts (existing outbound infra)",
  "content": "claude -p for proposal generation and personalization"
}
```
