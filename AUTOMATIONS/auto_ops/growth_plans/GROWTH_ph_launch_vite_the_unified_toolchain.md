# Growth Plan: [PH LAUNCH] Vite+: The Unified Toolchain for the Web

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $300-600/mo

---

## Tactics

1. Scrape PH daily at 7 AM — new launches go live overnight, 48h window is peak outreach time
2. Filter by categories: Developer Tools, SaaS, Productivity, Web Dev — these founders buy services
3. Extract founder Twitter/LinkedIn from PH maker profiles — direct DM has higher open rate than cold email
4. Use Playwright MCP to grab maker emails from PH profiles where listed
5. Cross-reference with existing lead database to avoid duplicate outreach
6. Generate personalized first lines referencing their specific PH launch in outreach

## Budget Tier Strategies

### FREE
Scrape PH JSON API (no auth needed for public data), extract maker profiles, send cold emails via custom script, personalize with Claude -p one-liner referencing launch

### LOW
$0-50/mo — upgrade to PH API token for higher rate limits, use Apollo free tier for email enrichment on founders without listed emails

### MID
$50-200/mo — Instantly or Smartlead for warmed sending infrastructure, higher volume outreach to all 10-20 daily PH launches

## Daily Actions

- [ ] Wire ph_launch_monitor.py to hit PH public API daily at 7 AM and pull all launches from prior 24h
- [ ] Score each launch: B2B keywords in description (+2), pricing page exists (+2), team < 5 (+1), dev-tool category (+1) — threshold 4+ to qualify
- [ ] Extract maker name, Twitter handle, email (if listed) from PH maker profiles via Playwright MCP
- [ ] Deduplicate against existing LEDGER/INBOUND_LEADS.csv
- [ ] Append qualified leads to outreach queue with personalized first-line using Claude -p referencing their PH launch
- [ ] Route into existing chain_14_ph_launches_today__high_quality_b2b_ for 48h follow-up sequence

## Tooling

```json
{
  "browser": "Playwright MCP for maker profile extraction",
  "email": "custom cold email scripts (Phase 0), Instantly when funded",
  "content": "none \u2014 pure outbound play"
}
```
