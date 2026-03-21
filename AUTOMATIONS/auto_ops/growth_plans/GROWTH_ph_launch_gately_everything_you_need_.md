# Growth Plan: [PH LAUNCH] Gately: Everything you need to build your own me

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo via affiliate commissions on comparison page traffic

---

## Tactics

1. Post 'Gately vs [competitor]' comparison content — captures high-intent search traffic from people already evaluating tools
2. Reply to Gately's PH launch comments with value-add insight — founder audience, warm impressions
3. Target Gately upvoters on Twitter (public PH voter lists) with relevant cold DM about complementary tools
4. Build SEO page: 'best membership site platforms 2026' — affiliate link farm with Gately + Memberful + Memberstack

## Budget Tier Strategies

### FREE
PH comment engagement + Twitter replies to maker + organic SEO comparison page via surge.sh deployment

### LOW
$0-50/mo — boost comparison post on Twitter, seed Reddit r/SaaS and r/indiehackers with 'I tested 5 membership tools' post linking to our page

### MID
$50-200/mo — affiliate traffic via SEMrush-style keyword targeting on 'membership site builder' longtails using our existing landing page infrastructure

## Daily Actions

- [ ] Wire ph_membership_monitor.py to scrape PH /memberships and /community daily at 7 AM
- [ ] Score launches: upvotes threshold routing (>200 → EAS leads, 50-200 → content, <50 → discard)
- [ ] Auto-extract affiliate program links from each tool's homepage
- [ ] Pipe content seeds to engagement_bait_converter.py for 3 post variants per tool
- [ ] Deploy 'best membership platforms 2026' SEO page to surge.sh with affiliate links
- [ ] Add cron entry + test run immediately to confirm output artifacts exist

## Tooling

```json
{
  "browser": "Playwright MCP (PH scraping)",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
