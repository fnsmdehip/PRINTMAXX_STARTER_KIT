# OPP-007: X/Twitter API Pay-Per-Use Micro-Tools

**Score:** 8.5/10 (Fit: 9, Effort: 8, ROI: 8)
**Startup Cost:** $5-50/mo (X API usage-based)
**Time to First Revenue:** 1-2 weeks

---

## What

Build and sell micro-tools that leverage X's new pay-per-use API pricing (launched Jan 21, 2026). The pricing shift from $200/mo flat to $5/1K reads creates an arbitrage window: tools that were too expensive for indie hackers to build are now dirt cheap to operate.

## Why

- X API went pay-per-use Jan 2026: 1K post reads = $5 (was $200/mo flat rate)
- xAI integration gives FREE AI credits from API spending — subsidized compute
- 18,217+ MCP servers on mcp.so — demand for X/Twitter integrations is proven
- Indie hackers and solopreneurs are the primary audience for cheap X tools
- Our existing Twitter scraping infrastructure (4 working scrapers) gives us domain expertise
- We already understand the X API ecosystem deeply

## How

1. **Tool 1: "X Audience Analyzer"** — Input a Twitter handle, get audience demographics, top topics, best posting times, engagement patterns. Sell as Gumroad product ($29 one-time) or SaaS ($9/mo).
2. **Tool 2: "X Thread Repurposer"** — Paste a thread URL, get it reformatted for LinkedIn, newsletter, blog post. $19 one-time on Gumroad.
3. **Tool 3: MCP Server for X Analytics** — Free MCP server that gives Claude Code users X analytics. Monetize with premium tier (advanced analytics, historical data).
4. **Distribution:** Launch on Product Hunt, Indie Hackers, MCP marketplace. Content about X API pricing changes drives organic traffic.

## Expected ROI

- Tool 1 (Audience Analyzer): 50 sales/mo x $29 = $1,450/mo
- Tool 2 (Thread Repurposer): 100 sales/mo x $19 = $1,900/mo
- Tool 3 (MCP Server): lead gen for premium → 20 users x $9/mo = $180/mo
- API costs: ~$50-100/mo at scale
- Net: $3,000-3,400/mo at moderate traction

## First 3 Steps

1. Build X Audience Analyzer MVP (Python script + simple web UI) — uses X API v2 user timeline endpoint + Claude for analysis
2. Create Gumroad listing with demo screenshots + landing page on surge.sh
3. Launch on Indie Hackers + post "X API pricing changed everything" thread on @printmaxxer

## Risk

- X API terms change frequently — build defensively
- Competition from established tools (Tweethunter, Hypefury) but they're expensive ($49+/mo)
- Usage-based costs scale with users (mitigate: caching, batch queries)

## Sources

- WeAreFounders: X API Pricing 2026 tier breakdown
- Superframeworks: X API pay-per-use indie hacker guide
- Zuplo: API monetization playbook for indie hackers
