# Growth Plan: Best of Passive Income: March 2026

**Created:** 2026-03-20 13:50
**Venture:** RESEARCH
**Budget Tier:** FREE
**Revenue Est:** $0/mo direct (pipeline enhancement — improves alpha quality by surfacing community-validated methods, estimated 15-25% better hit rate on extracted methods vs raw scrapes)

---

## Tactics

1. cross-post extracted methods as 'what Reddit says works' threads on Twitter
2. use community-validated methods as social proof in content
3. monitor which extracted methods get traction for doubling down

## Budget Tier Strategies

### FREE
Repurpose top Reddit methods into Twitter threads with attribution. Use extracted methods to validate or kill existing ventures. Cross-reference with HN/Twitter alpha for triangulation.

### LOW
$0-20/mo: Reddit API access if JSON endpoint gets restricted. Proxy rotation for rate limit avoidance.

### MID
$50-100/mo: Paid Reddit data provider for historical roundup access. Sentiment analysis on method discussions.

## Daily Actions

- [ ] Wire into existing reddit_deep_scraper.py with new target: r/passive_income monthly 'best of' posts
- [ ] Add method extraction logic: parse post body for numbered lists, bullet points, and top-level comments with method descriptions
- [ ] Score each extracted method against Capital Genesis criteria (speed, automation potential, cost, synergy with existing ventures)
- [ ] Auto-stage qualifying methods (score >= 6) into ALPHA_STAGING.csv with source='reddit/r/passive_income/roundup'
- [ ] Deduplicate against existing alpha entries to avoid re-processing known methods
- [ ] Add cron entry: 1st of each month at 7 AM

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory for repurposing extracted methods"
}
```
