# Growth Plan: SPX Dealer Premiums - Volland

Dealer Premium (SPX) is a sna

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-150/mo

---

## Tactics

1. Post during market open (9:30 AM ET) when 0DTE options discussion peaks on fintwit
2. Reply to @financialjuice, @SpotGamma, @OptionsFlow posts to capture their existing audience
3. Use specific CBOE daily numbers (free public endpoint) to add credibility — beats vague takes
4. Thread structure: explain dealer positioning concept → today's setup → implied market implication → engagement CTA
5. Quote-tweet SPX move events with dealer flow context — algorithm treats QTs as high-signal engagement

## Budget Tier Strategies

### FREE
Post fintwit content at market open via CONTENT/social/posting_queue/, reply to top options flow accounts, pull free CBOE SPX stats daily (cboe.com/us/equities/market_statistics), engage 0DTE subreddits (r/options, r/wallstreetbets) with educational content

### LOW
$0-50/mo — schedule via Buffer CSV import once account created, $5-10 Twitter boost on top-performing threads, unusual_whales free tier for supplemental flow data

### MID
$50-200/mo — unusual_whales paid tier for proprietary flow credibility, targeted follow campaigns against fintwit accounts, brokerage affiliate links (Tastytrade $100-200/funded account, Webull $50-100/signup)

## Daily Actions

- [ ] Run engagement_bait_converter.py with this entry — generates 3 fintwit hooks: (1) specific-number hook on dealer net premium, (2) contrarian 0DTE take, (3) educational thread on dealer hedging mechanics
- [ ] Pull free CBOE daily SPX options stats from cboe.com/us/equities/market_statistics — no auth, scrape-safe
- [ ] Inject daily CBOE numbers into hook templates for credibility
- [ ] Queue 3 posts to CONTENT/social/posting_queue/ scheduled Mon-Fri 9:30 AM ET
- [ ] If engagement >2% CTR after 2 weeks, wire brokerage affiliate links (Tastytrade, Webull) into content

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
