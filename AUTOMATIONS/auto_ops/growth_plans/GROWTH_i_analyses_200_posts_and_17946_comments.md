# Growth Plan: I Analyses 200 posts and 17,946 comments from r/SaaS and r/E

**Created:** 2026-03-20 18:35
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo

---

## Tactics

1. Post lead gen pain point analysis as original content on r/SaaS (mirrors source format, proven engagement)
2. Reply to lead gen complaint threads with genuine value + soft link to our lead gen tools
3. Cross-post validated pain points as Twitter threads targeting #buildinpublic #indiehackers
4. Use pain point data to write comparison landing pages (our free tool vs paid alternatives)

## Budget Tier Strategies

### FREE
Reddit engagement in lead gen threads, Twitter threads from scraped insights, SEO longtail pages targeting 'free lead generation tool' variants

### LOW
$0-50/mo: Boost top-performing lead gen content thread on Twitter, sponsor one r/SaaS comment

### MID
$50-200/mo: Run lead gen comparison pages as Google Ads on long-tail keywords with low CPC

## Daily Actions

- [ ] Run reddit_deep_scraper.py targeting r/SaaS and r/Entrepreneur with 'lead generation' filter
- [ ] Cluster extracted complaints into subtopics (cold email, LinkedIn, inbound, SEO leads, paid ads leads)
- [ ] Generate 3 Twitter threads + 5 reply templates from validated pain points
- [ ] Update app_factory_priority_queue.json to boost lead-gen-adjacent apps (cold email tools, scraper tools)
- [ ] Queue generated content to CONTENT/social/posting_queue/
- [ ] Feed into existing chain_building_a_clay_alternative_for_lead_en for product development signal

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
