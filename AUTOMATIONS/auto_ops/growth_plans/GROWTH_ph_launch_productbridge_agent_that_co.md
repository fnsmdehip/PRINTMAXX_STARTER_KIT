# Growth Plan: [PH LAUNCH] ProductBridge: Agent that collects feedback acro

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $300-900/mo

---

## Tactics

1. Comment on top 5 PH launches within first 2h of daily reset (highest visibility window before algo buries comments)
2. Post daily Twitter thread: 'Best PH launches today + what feedback infrastructure they need' — tags founders, drives follow-backs
3. Monitor PH comments for founders asking about feedback tooling or analytics — reply with direct value offer
4. Build ProductBridge clone as APP factory product using Playwright MCP to scrape Reddit/Twitter/PH/G2 — zero COGS, instant shipping
5. Reply to PH Ship (pre-launch) posts with feedback offer before they launch — highest receptivity window

## Budget Tier Strategies

### FREE
Daily PH scrape via Playwright MCP, organic comments on top launches, Twitter roundup threads tagging founders, manual DM to top 3 founders/day via existing Twitter account, PH Ship feed monitoring for pre-launch outreach

### LOW
$0-50/mo — lightweight proxy for scraping stability, basic email warming for outreach domain, PH Pro for instant launch notifications (first-mover advantage on comments)

### MID
$50-200/mo — LinkedIn Sales Nav for founder enrichment, automated follow-up sequences via custom cold email scripts, micro-influencer seeding on PH launch days

## Daily Actions

- [ ] Add ph_feedback_tool_outreach.py as a category filter layer on top of existing chain_14_ph_launches_today chain — no new chain, enhance existing
- [ ] Qualifier adds category scoring: agent/AI/feedback/multi-platform tags boost score by +2 each
- [ ] Outreach template: 'Saw [ProductName] on PH — we build cross-platform feedback pipelines. Noticed you're collecting from [X platforms]. Want one that auto-routes to your CRM + Slack?'
- [ ] Queue personalized emails to AUTOMATIONS/leads/ outreach pipeline with 48h send timer
- [ ] Generate 3-tweet roundup thread daily from ph_launches_qualified.json via engagement_bait_converter.py
- [ ] Add cron entry: 30 6 * * * ph_feedback_tool_outreach.py (post-PH daily reset at 6:30 AM)

## Tooling

```json
{
  "browser": "Playwright MCP (PH public scraping, no auth needed)",
  "email": "existing AUTOMATIONS/ cold email scripts (swap Instantly \u2192 custom sender)",
  "content": "claude -p for personalized outreach copy per launch"
}
```
