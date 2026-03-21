# Growth Plan: Package existing stack as client service. Write 1-page deliv

**Created:** 2026-03-20 18:09
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $999-5000/mo

---

## Tactics

1. Lead with proof: 47 deployed apps, 337 automation scripts, 17K analyzed leads as social proof in cold emails
2. Reverse-engineer prospect's stack via public job postings and tech stack detectors before emailing
3. Cross-pollinate: every client engagement generates case study content for printmaxxer Twitter + thread
4. Reply-bait on Twitter about agency results to generate inbound alongside outbound
5. Stack LinkedIn connection requests 24h before cold email for multi-touch

## Budget Tier Strategies

### FREE
Cold email from custom scripts, Twitter proof-of-work threads, LinkedIn warm-up connections, reply-engagement on SaaS founder tweets, case studies from free tier delivery

### LOW
$0-50/mo: Buy custom domain for cold email sender reputation, Mailgun transactional tier for deliverability tracking

### MID
$50-200/mo: LinkedIn Sales Navigator for lead enrichment, Calendly Pro for call booking automation, retargeting ads on warm leads who opened emails

## Daily Actions

- [ ] 1. Audit existing stack and generate deliverables menu with 3 pricing tiers (Starter/Growth/Scale)
- [ ] 2. Filter 50 ICP-matched B2B SaaS founders from 17K hot leads (seed-SeriesA, 10-500 employees, automation pain signals)
- [ ] 3. Research each lead's public tech stack, recent hiring, and pain points
- [ ] 4. Craft 3-email cold sequence per lead with personalized hooks referencing their specific gaps
- [ ] 5. Send initial batch (10/day to protect sender reputation), log all to OUTREACH_PIPELINE.csv
- [ ] 6. Daily cron checks replies, scores buying intent, routes warm leads for human call booking
- [ ] 7. Follow-up sequence: Day 3 (value-add), Day 7 (case study), Day 14 (breakup email)
- [ ] 8. First client closed → deliver using existing stack → document as case study → feed back into cold email proof
- [ ] 9. Scale: increase send volume to 20/day after sender reputation established, expand ICP criteria

## Tooling

```json
{
  "browser": "none",
  "email": "custom SMTP + python smtplib",
  "content": "content_factory for case studies"
}
```
