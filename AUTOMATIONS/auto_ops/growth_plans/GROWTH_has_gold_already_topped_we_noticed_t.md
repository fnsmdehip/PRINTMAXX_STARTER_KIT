# Growth Plan: Has #gold already topped? 

We noticed two whales have taken

**Created:** 2026-03-20 18:35
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Quote-tweet Lookonchain and similar on-chain analysts with our own take
2. Post whale alerts as reply-bait threads during high-volume crypto hours (US market open, Asia evening)

## Budget Tier Strategies

### FREE
Organic crypto Twitter threads timed to whale movements; QT major on-chain accounts; use whale data as reply-bait under trending $GOLD $XAUT cashtags

### LOW
$0-20/mo for Etherscan Pro API if free tier rate-limits hit

### MID
N/A — not worth paid scaling until crypto audience >2K followers

## Daily Actions

- [ ] Add Etherscan/Arkham free-tier API polling for known whale wallets (0x8C08, 0xdfcA) targeting XAUT and PAXG transfers
- [ ] Format large movements (>$1M) into tweet-ready threads with profit/loss context
- [ ] Queue formatted threads to CONTENT/social/posting_queue/ via engagement_bait_converter.py
- [ ] Schedule cron 7 AM + 7 PM to catch overnight and daytime whale activity
- [ ] Tag output with #gold #XAUT #PAXG cashtags for discoverability

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
