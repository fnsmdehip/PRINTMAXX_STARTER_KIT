# OPP-061: n8n Workflow Template Store

**Score:** 8.8/10 (Fit: 9, Effort: 4, ROI: 9)
**Startup Cost:** $0
**Time to First Revenue:** 3-5 days
**Monthly Potential:** $2,000-5,000
**Competition:** Low-Medium (3 dedicated marketplaces, few high-quality sellers)

## What

Sell pre-built n8n automation workflow templates on dedicated n8n marketplaces. One creator built 5 templates generating $3,200/mo passively (March 2026 verified). We already have 528 automation scripts — many are wrappable as n8n workflows or already are. No new build required for first batch.

## Why Now

- 3 active dedicated marketplaces: haveworkflow.com, n8nmarket.com, managen8n.com
- n8n has 9,000+ community workflows but few are polished or monetized
- Real demand: n8n community posts asking "where can I sell my workflow?" — market finding us
- Price range: $29 simple → $299+ complex industry-specific solutions (avg $89)
- Passive: once listed, zero marginal effort per sale
- Compounding: marketplace rankings improve with each sale, driving organic discovery
- Our Python/Playwright expertise translates directly — n8n wraps what we already build

## How

1. Audit AUTOMATIONS/ for scripts that are already webhook-triggered or API-sequential (n8n-izable)
2. Convert top 5 scripts to n8n JSON export format (each takes 2-3h via Claude)
3. Create seller accounts on haveworkflow.com and n8nmarket.com ($0)
4. List at $49-99 per template with clear use-case descriptions
5. Cross-post to n8n community forum + Reddit r/n8n for initial traction
6. Add Gumroad/Whop listing for same templates (multi-channel)

## Best Candidates From Our Stack

- Lead scoring + qualification pipeline (existing: lead_qualifier.py)
- Cold email sequence generator (existing: email outreach scripts)
- Reddit content scraper + repurposer (existing: reddit_deep_scraper.py)
- Daily alpha digest + newsletter formatter
- Local business review aggregator

## Expected ROI

- 5 templates at $69 avg = $345/sale bundle OR $69 each
- At 15 sales/mo across 5 templates: $1,035/mo passive
- At 30 sales/mo: $2,070/mo passive
- Proven ceiling: $3,200/mo from 5 templates (one creator, March 2026)
- Maintenance: 2h/week max (API updates, customer questions)

## First 3 Steps

1. Run `ls AUTOMATIONS/*.py | head -50` and flag top 5 most marketable scripts
2. Export each as n8n JSON workflow (Claude can translate Python logic to n8n nodes)
3. Create seller account on haveworkflow.com + n8nmarket.com, list first template by Day 3

## Stack Fit

Python/Claude expertise maps directly to n8n workflow building. We have 528 automation scripts — this is pure packaging. No new systems needed. Haveworkflow.com supports Stripe-native checkout.

## Source Signal

- Medium article (March 2026): "I Built 5 n8n Automations That Generate $3,200/Month Passively"
- n8n community: "Where can I sell my N8N workflow?" — active thread, high demand
- n8nmarket.com: active paid listings visible
