# Growth Plan: How we automated LinkedIn lead gen using keyword triggers (w

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $300-1200/mo

---

## Tactics

1. Monitor 10 buying-signal keyword sets daily: 'tool recommendation', 'best SaaS for', 'looking for a solution', 'anyone used X', 'replacing Y with'
2. Engage in comments BEFORE the post author responds to capture top-comment visibility
3. Use native LinkedIn comment (not DM) — avoids spam classifier entirely
4. Rotate keyword sets weekly to avoid LinkedIn pattern detection
5. Build comment template library: problem-aware / solution-proof / social-proof variants
6. Cross-post best-performing comment formats as standalone LinkedIn posts for organic reach amplification

## Budget Tier Strategies

### FREE
Playwright MCP monitors 5 keyword sets on existing LinkedIn session, Claude generates comment responses, manual review queue for posting. Zero recurring cost.

### LOW
$0-50/mo — residential proxies ($29/mo SOAX) for scraping at scale without session risk; LinkedIn Sales Navigator free trial for advanced keyword filters

### MID
$50-200/mo — dedicated LinkedIn account warmup sequence, retarget commenters with sponsored posts, promote best comment threads as native ads

## Daily Actions

- [ ] Check chain_how_we_automated_linkedin_lead_gen_using — enhance with keyword-trigger DAG logic rather than creating duplicate
- [ ] Build linkedin_keyword_trigger_commenter.py: Playwright MCP scrapes LinkedIn search for buying-signal queries
- [ ] Score posts by relevance: keyword match strength, poster seniority (manager+), post recency (<48h), comment count (<10 preferred for visibility)
- [ ] Generate 3 comment variants per qualified post via claude -p: problem-aware, solution-focused, social-proof-backed
- [ ] Post at max 15 comments/day to stay under LinkedIn soft rate limit — random 8-45 min gaps between posts
- [ ] Log all outreach with post URL, comment text, timestamp to LEDGER/OUTREACH_PIPELINE.csv
- [ ] Add cron: 30 7 * * 1-5 (weekday mornings, catches overnight buying-signal posts)

## Tooling

```json
{
  "browser": "Playwright MCP (existing LinkedIn session via Brave cookies)",
  "email": "none",
  "content": "claude -p for comment generation (3 variants per post)"
}
```
