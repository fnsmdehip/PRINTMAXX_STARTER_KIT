# Growth Plan: [PH LAUNCH] Looq: Preview Files: A better Quick Look: code, 

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $200-600/mo

---

## Tactics

1. Scrape PH daily launches — filter for developer/productivity/SaaS tools with 100+ upvotes
2. Extract maker profiles: email via PH API, GitHub (check repo for contact), LinkedIn search
3. 48h outreach window is critical — founder ego is highest right after launch
4. Pitch angle: 'Saw Looq hit PH — congrats. Here is how we got X similar tool to 500 installs in 30 days'
5. Segment by tool category: dev tools, productivity, macOS-native — each needs a different pitch template
6. Add to OUTBOUND cold email sequences with personalized PH launch hook
7. Monitor maker comment threads for pain points — use as cold email openers

## Budget Tier Strategies

### FREE
PH API scrape daily launches → extract maker emails/GitHub → queue to existing cold email script → personalized 48h outreach via SMTP warmup accounts

### LOW
$0-50/mo: Apollo.io free tier for email enrichment on founders missing direct contact, 1 dedicated warmup domain for PH outreach

### MID
$50-200/mo: Instantly sequences for PH launch category (dev tools, productivity, macOS) — multi-touch 5-step sequences, reply detection, auto-pause on response

## Daily Actions

- [ ] Wire into existing chain_14_ph_launches_today__high_quality_b2b_ — this entry is the same pattern, parameterize not duplicate
- [ ] Add 'developer_tools' and 'macos_native' as target categories in ph_launch_outreach_queuer.py config
- [ ] Confirm PH scraper hits the existing daily cron at 8 AM — append Looq-type tools to qualified_leads.json
- [ ] Pull Looq maker profile now: extract GitHub (likely has email in commits), PH profile link, any listed contact
- [ ] Draft outreach: subject line 'Saw Looq launch on PH today — quick question on distribution', body references specific PH launch + concrete growth offer
- [ ] Queue to existing SMTP warmup sequence — send within 24h of this entry timestamp

## Tooling

```json
{
  "browser": "requests + PH API (no browser needed for public data)",
  "email": "custom cold email scripts (existing OUTBOUND infra)",
  "content": "none"
}
```
