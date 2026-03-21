# Growth Plan:  most dropshippers find a winning product and have no idea w

**Created:** 2026-03-20 18:09
**Venture:** SCRAPING
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. Post 'customs data hack' thread on Twitter — high engagement bait for ecom audience
2. Cross-post supplier sourcing tips to r/dropshipping, r/FulfillmentByAmazon, r/ecommerce
3. Create free sample report as lead magnet (1 niche) to drive paid report sales
4. Reply to dropshipper complaint tweets with 'customs data is public, here is how' hook
5. SEO longtail: 'how to find real suppliers for [product]' pages linking to paid reports

## Budget Tier Strategies

### FREE
Twitter threads on customs data sourcing, Reddit posts in ecom subs, free sample report as lead magnet, reply engagement on dropshipper tweets

### LOW
$0-50/mo: Boost top-performing customs data thread on Twitter, run $20 FB ad to ecom audiences targeting the free sample report

### MID
$50-200/mo: Partner with ecom YouTubers for shoutouts, run targeted Google Ads on 'find real supplier for [product]' keywords

## Daily Actions

- [ ] 1. Build customs_supplier_intel_scraper.py — scrapes ImportYeti (free, no auth needed), USA Trade Online, Volza free tier for shipment records by HS code
- [ ] 2. Build product_trend_matcher.py — pulls trending AliExpress/Amazon products via free APIs and matches to customs consignee data
- [ ] 3. Build supplier_report_generator.py — takes matched data and generates niche PDF reports (e.g. 'Phone Accessories Real Suppliers 2026')
- [ ] 4. Generate 3 initial niche reports: phone accessories, home decor, fitness gear (highest dropship volume categories)
- [ ] 5. Create Gumroad/Whop listing for reports at $29-47 each or $97 bundle
- [ ] 6. Generate content: 3 tweets + 1 thread on customs data hack, post to r/dropshipping
- [ ] 7. Set up weekly cron (Monday 5 AM) to refresh customs data and flag new supplier matches
- [ ] 8. Cold email 50 dropshipper leads from LEDGER/INBOUND_LEADS.csv offering free sample report

## Tooling

```json
{
  "browser": "playwright for ImportYeti/Volza scraping",
  "email": "custom cold email script to dropshipper leads",
  "content": "content_factory for ecom audience threads + engagement_bait_converter"
}
```
