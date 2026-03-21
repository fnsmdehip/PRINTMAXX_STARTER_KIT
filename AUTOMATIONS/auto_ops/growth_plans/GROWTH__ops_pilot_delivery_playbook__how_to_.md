# Growth Plan: # Ops Pilot Delivery Playbook  **How to deliver a Back-Offic

**Created:** 2026-03-20 18:10
**Venture:** EAS
**Budget Tier:** FREE
**Revenue Est:** $2000-5000/mo

---

## Tactics

1. Cold email prospects who posted ops/data-entry jobs in last 14 days (highest intent signal)
2. Post case studies on r/smallbusiness and r/automation showing before/after of pilot deliveries
3. Cross-pollinate with existing EAS leads — ops pilot is a lower-commitment entry point than full EAS
4. Reply to Twitter/HN threads about 'hiring is hard' with automation-first framing

## Budget Tier Strategies

### FREE
Job board scraping for intent signals, cold email via custom scripts, Reddit/HN content marketing, cross-sell to existing EAS pipeline leads

### LOW
$20-30/mo for LinkedIn Sales Navigator basic to find decision-makers at qualified companies

### MID
$100-150/mo for Instantly.ai warm email infrastructure if cold volume exceeds 50/day

## Daily Actions

- [ ] Wire orphan doc content into EAS venture as ops_pilot_playbook.md delivery template
- [ ] Extend eas_lead_pipeline.py with job-board scraping module targeting ops/data-entry postings
- [ ] Create cold email template variant specific to ops pilot offer (10-day fixed price framing)
- [ ] Add prospect scoring criteria: company size, industry, number of ops roles, tech signals
- [ ] Schedule MWF cron to scrape and queue new prospects
- [ ] Add ops_pilot as entry-level offering in EAS pricing ladder (pilot → retainer → full automation)
- [ ] Reuse procedural memory objection-handling and proposal-writing skills for outreach personalization

## Tooling

```json
{
  "browser": "playwright for job board scraping",
  "email": "custom cold email scripts (eas_lead_pipeline.py already exists)",
  "content": "content_factory for case study generation"
}
```
