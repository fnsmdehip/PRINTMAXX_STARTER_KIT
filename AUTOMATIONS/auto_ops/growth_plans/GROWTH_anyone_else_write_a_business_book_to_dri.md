# Growth Plan: Anyone else write a business book to drive traffic to the Sa

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo indirect (email list growth → app installs → downstream revenue)

---

## Tactics

1. Post each guide chapter as Twitter/X thread with lead magnet CTA at end
2. Upload full guide to Scribd, SlideShare, Academia.edu for passive SEO backlinks
3. Post guide to relevant subreddits as 'free resource' — r/SaaS, r/entrepreneur, r/indiehackers
4. Repurpose chapters via content_multiplier.py into 5-10 SEO blog posts per guide
5. Gate guide download behind email capture — feeds cold email pipeline

## Budget Tier Strategies

### FREE
Distribute via Scribd/SlideShare/Reddit, repurpose chapters as blog posts and Twitter threads via content_multiplier.py, post to relevant subreddits with genuine value framing

### LOW
$10-30/mo: Boost top-performing Reddit posts with Reddit promoted posts, promote guide landing page via Twitter ads targeting SaaS/founder audiences

### MID
$50-150/mo: Sponsor relevant newsletters with free guide offer as lead gen, run targeted LinkedIn content ads to B2B niche if applicable

## Daily Actions

- [ ] For each live app niche (prayer, sobriety, focus, invoice, etc.), use claude -p to generate 20-30 page 'ultimate guide' PDF — e.g. 'Ultimate Guide to Building a Prayer Habit'
- [ ] Create simple landing page per guide with email capture (surge.sh, reuse existing templates)
- [ ] Feed captured emails into cold email pipeline via eas_lead_pipeline.py or outreach scripts
- [ ] Run content_multiplier.py on guide chapters to produce 5-10 SEO blog posts per guide
- [ ] Post blog posts to app marketing pages (LANDING/app-marketing-pages/) for SEO
- [ ] Route guide chapters to engagement_bait_converter.py for 3+ Twitter posts per guide
- [ ] Upload guide PDFs to Scribd/SlideShare for passive backlinks
- [ ] Schedule via cron: weekly guide generation Monday 7 AM, picks next niche in queue

## Tooling

```json
{
  "browser": "none",
  "email": "cold email pipeline (captured leads)",
  "content": "content_multiplier.py + engagement_bait_converter.py"
}
```
