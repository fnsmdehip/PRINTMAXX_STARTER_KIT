# Growth Plan: [r/indiehackers] Looking for builders who prefer "critique" 

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-100/mo indirect (audience growth and inbound DMs converting to EAS or cold outbound clients downstream)

---

## Tactics

1. Post 'I'll roast your landing page for free — drop it below' on r/indiehackers and Twitter. High reply volume, builds authority, drives inbound DMs for any service offering.
2. Use critique positioning as cold outreach opener: 'saw your site, here is one thing killing your conversion' — filters for serious builders only.
3. Mirror critique-angle threads on #buildinpublic Twitter — 'compliments are noise, critique is signal' framing resonates with that community.
4. Monitor r/indiehackers for new 'feedback wanted' / 'roast my X' threads — auto-flag as warm leads in LEDGER/INBOUND_LEADS.csv via background_reddit_scraper.py keyword filter.

## Budget Tier Strategies

### FREE
Run engagement_bait_converter.py to generate 5 critique-hook post variants. Queue top 2 in CONTENT/social/posting_queue/ for Twitter and r/indiehackers. Engage authentically in existing critique threads to build authority before posting own hooks.

### LOW
$0-50/mo: Boost a top-performing critique post as a Twitter/X promoted post targeting #indiehackers and #buildinpublic audiences. Expected CPE under $0.10.

### MID
$50-200/mo: Sponsor a dedicated critique session in an IndieHackers newsletter or Slack community. Position as the honest-feedback authority to generate warm inbound leads for EAS or cold outbound services.

## Daily Actions

- [ ] python3 AUTOMATIONS/engagement_bait_converter.py --input 'critique over compliments hook for indie hackers and builders' --count 5
- [ ] Queue top 2 output posts in CONTENT/social/posting_queue/ — label platform: twitter + reddit/indiehackers
- [ ] Add keyword filter to background_reddit_scraper.py: ['roast my', 'critique my', 'brutal feedback', 'honest feedback', 'tell me what is wrong'] on r/indiehackers — flag matches to LEDGER/INBOUND_LEADS.csv as WARM

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_multiplier.py"
}
```
