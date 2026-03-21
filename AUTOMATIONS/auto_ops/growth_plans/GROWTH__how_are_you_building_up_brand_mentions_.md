# Growth Plan:  how are you building up brand mentions in llms? trying to c

**Created:** 2026-03-20 18:09
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo indirect via increased organic traffic from LLM referrals within 60-90 days

---

## Tactics

1. Seed Reddit answers in niche subs (r/productivity, r/islam, r/Christianity, r/getdisciplined) with genuine value + natural app mentions — Perplexity indexes Reddit heavily
2. Create comparison pages (X vs Y) for every app — LLMs love structured comparisons for recommendations
3. Add FAQ schema markup to all 47 deployed landing pages — structured data improves LLM extraction
4. Build programmatic 'best X for Y' pages targeting long-tail queries LLMs get asked
5. Post to dev.to and Medium with technical guides mentioning our tools — high-authority domains LLMs trust
6. Create GitHub repos with README files that naturally reference our products as solutions
7. Answer Quora questions in our niches — another source Perplexity crawls

## Budget Tier Strategies

### FREE
Organic Reddit/dev.to/Medium posting, FAQ schema on existing pages, GitHub presence, Quora answers. Leverage existing 47 sites for structured data. Use content_multiplier.py to generate AEO variants at scale. Query Perplexity free tier for monitoring.

### LOW
$0-50/mo: Perplexity Pro for deeper monitoring, boost key Reddit posts, Medium paid distribution for authority signals

### MID
$50-200/mo: Programmatic AEO page generation at scale (hundreds of comparison/FAQ pages), paid guest posts on high-DA sites that LLMs index, Perplexity API for automated monitoring

## Daily Actions

- [ ] 1. Build aeo_optimization_engine.py with Perplexity query scraper (playwright) — test 50 niche queries, log which sites get cited
- [ ] 2. Identify gap queries where no good answer exists for our niches (faith apps, streak apps, productivity, MCP tools)
- [ ] 3. Add FAQ schema (JSON-LD) to ALL 47 deployed landing pages via batch script — immediate low-hanging fruit
- [ ] 4. Generate 20 comparison pages (scripture-streak vs competitor, prayerlock vs hallow, etc.) — LLMs love head-to-head content
- [ ] 5. Create Reddit answer seeding schedule: 2 genuine answers/day in target subs with natural product mentions
- [ ] 6. Post 3 dev.to articles about our tools (MCP marketplace, streak app framework, autonomous agent setup)
- [ ] 7. Set up weekly Perplexity monitoring cron — query same 50 questions, track citation delta in LEDGER/AEO_METRICS.csv
- [ ] 8. Feed AEO content back into content_trend_pipeline.py for cross-platform distribution

## Tooling

```json
{
  "browser": "playwright for Perplexity/ChatGPT querying",
  "email": "none",
  "content": "content_factory + content_multiplier.py + engagement_bait_converter.py"
}
```
