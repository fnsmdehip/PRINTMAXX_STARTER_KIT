# Growth Plan: [PH LAUNCH] Cursor Glass: Unified agent workspace with seaml

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $150-500/mo

---

## Tactics

1. Post congratulatory reply on PH launch page to build visibility with founder + their audience
2. Monitor Cursor Glass Twitter mentions to find developers complaining about gaps — position our stack as complementary
3. Scrape PH upvoters (they are early adopters in agent/AI space) as secondary outreach list
4. Track 'Cursor Glass alternatives' search intent — SEO page opportunity
5. Cross-reference PH makers with HN 'Show HN' posts for double-signal warm leads

## Budget Tier Strategies

### FREE
PH API scrape + Twitter mention monitor via existing twitter_alpha_scraper.py + personalized cold email via custom script. Zero cost.

### LOW
$0-50/mo: Apollo.io free tier for email enrichment on top PH makers. Instantly warmup on outreach domain.

### MID
$50-200/mo: Hunter.io for bulk email find on maker companies. Smartlead for sequenced follow-ups.

## Daily Actions

- [ ] Wire ph_agent_workspace_lead_scraper.py to hit PH API at 6:30 AM daily — filter by 'developer-tools/ai/agents' tags
- [ ] Append qualified leads to LEDGER/INBOUND_LEADS.csv with source=PH and launch_date for 48h window tracking
- [ ] Route to existing chain_14_ph_launches_today handoff chain — already handles PH→outreach pattern
- [ ] Generate 3 content posts from each notable PH launch via engagement_bait_converter.py (reaction content performs well)
- [ ] Add 'agentic IDE' and 'agent workspace' as tracked keywords in competitive intel scraper

## Tooling

```json
{
  "browser": "playwright (PH profile scraping)",
  "email": "custom cold email script (existing in AUTOMATIONS/)",
  "content": "engagement_bait_converter.py for PH-watching posts"
}
```
