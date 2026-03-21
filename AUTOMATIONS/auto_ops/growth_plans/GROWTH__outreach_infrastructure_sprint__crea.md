# Growth Plan: # Outreach Infrastructure Sprint  **Created:** 2026-02-19 **

**Created:** 2026-03-20 18:10
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo

---

## Tactics

1. Warm 3 email domains simultaneously (Google Workspace $6/mo each) to 3x send capacity
2. A/B test subject lines across lead segments — kill losers at <10% open rate after 200 sends
3. Cross-pollinate: positive reply leads also get added to social warm-touch list (Twitter follow + engage before email)
4. Use demo sites as social proof anchors in email signatures — 6 live sites = credibility
5. Reply-chain seeding: first email asks question, second email provides value, third email pitches

## Budget Tier Strategies

### FREE
Custom SMTP via email_sender.py, manual warmup by sending 5-10/day for 2 weeks, use existing 6 demo sites as proof, organic LinkedIn connection requests to same leads

### LOW
$18/mo for 3 Google Workspace accounts for domain warmup, rotate sending across accounts to stay under spam thresholds

### MID
$50-100/mo for Instantly account to handle warmup + deliverability + auto-rotation across the 51 pre-formatted CSVs

## Daily Actions

- [ ] 1. Verify all referenced assets exist: HOT_LEADS_QUALIFIED.csv, cold_emails_ready.csv, email_sender.py, response_tracker.py, 6 demo site URLs
- [ ] 2. Dedupe hot leads against existing OUTBOUND venture leads and OUTREACH_PIPELINE.csv to avoid double-sending
- [ ] 3. Merge verified leads into OUTBOUND venture state with priority scoring
- [ ] 4. Wire email_sender.py and response_tracker.py into the existing chain_recruit_new_affiliates_via_cold_email_ou handoff chain
- [ ] 5. Add cron entry: weekdays 8 AM, send batch of 50 emails (configurable, starts at 5/day during warmup)
- [ ] 6. Wire response_tracker.py output into INBOUND_LEADS.csv for positive replies
- [ ] 7. HUMAN BLOCKER: Create 3 email sending accounts + begin 14-day warmup (5→10→20→50/day ramp)
- [ ] 8. Add KPI tracking row to KPI_DASHBOARD.md: send count, open rate, reply rate, positive reply count

## Tooling

```json
{
  "browser": "none",
  "email": "email_sender.py (custom) \u2192 Instantly when budget allows",
  "content": "cold_emails_ready.csv (13,221 pre-generated)"
}
```
