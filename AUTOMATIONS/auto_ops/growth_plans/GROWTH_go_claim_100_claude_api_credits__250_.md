# Growth Plan: Go Claim $100 Claude API credits + $250 Stripe credits

here

**Created:** 2026-03-21 12:40
**Venture:** RESEARCH
**Budget Tier:** FREE
**Revenue Est:** $0/mo direct | $350 one-time cost savings + ongoing credit stacking potential

---

## Tactics

1. Monitor Lovable, Vercel, Netlify, AWS Activate, Stripe Atlas, and Anthropic partner pages weekly for new credit offers
2. Stack credits across multiple dev platforms to reduce API/infra burn rate to near-zero in Phase 0
3. Check if Lovable has referral program — each referral may unlock additional credits
4. Cross-reference with YC Startup School deals page (free tier available to non-YC founders) for Stripe/AWS/Anthropic credits

## Budget Tier Strategies

### FREE
Claim all available partner credits across Lovable, Vercel, AWS Activate, Heroku, Anthropic Console — reduces monthly infra cost by $200-500

### LOW
N/A — this is a cost-reduction method, not a paid acquisition channel

### MID
N/A

## Daily Actions

- [ ] HUMAN NOW: Open lovable.dev → dashboard → Offers section → claim Claude $100 credit (paste Anthropic Org ID from console.anthropic.com/settings) + claim Stripe $250
- [ ] BUILD: dev_credit_offer_scanner.py — weekly Playwright scrape of Lovable offers page + known partner credit pages, diff against last scan, alert to OPS/HUMAN_ACTIONS.md if new offer detected
- [ ] CRON: Add weekly Monday 9 AM scan — `python3 AUTOMATIONS/dev_credit_offer_scanner.py --scan`
- [ ] TRACK: Log claimed credits in LEDGER/ACTIVE_INVESTMENTS.csv with expiry dates so cron alerts before expiration

## Tooling

```json
{
  "browser": "playwright (check offer pages weekly)",
  "email": "none",
  "content": "none"
}
```
