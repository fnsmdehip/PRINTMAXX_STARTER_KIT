# Growth Plan: [ACQUISITION] I screen deal flow for an early-stage syndicat

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo

---

## Tactics

1. Post 3-part thread: 'I screen 200+ decks/month. Here are the 3 reasons yours gets auto-rejected before I read page 2' — each point = one tweet
2. Quote-tweet founders sharing their deck struggles with the checklist as a reply bait anchor
3. Post checklist as a free Gumroad download ($0, email-gated) to build founder email list
4. Cross-post to r/startups, r/Entrepreneur, r/venturecapital as a value-add comment on 'how do I raise' threads
5. Build a one-page static 'Pre-Seed Deck Scorecard' on surge.sh — SEO target: 'pre-seed deck template 2026'

## Budget Tier Strategies

### FREE
Thread content via engagement_bait_converter.py → posting_queue → post 2x/week. Reddit organic comments on fundraising threads. Static scorecard page on surge.sh for SEO.

### LOW
$0-50/mo: Boost top-performing thread with $20 Twitter promotion to founder audience (target: YC alumni, AngelList users). Submit scorecard page to founder tool directories.

### MID
$50-200/mo: Sponsor a founder newsletter (e.g. Lenny's, The Hustle subset lists) with the free scorecard as lead gen. Convert list to Gumroad buyers for $29 'Deck Teardown' guide.

## Daily Actions

- [ ] Run python3 AUTOMATIONS/engagement_bait_converter.py with the 3 rejection criteria as input — outputs 3 tweets + 1 thread to CONTENT/social/posting_queue/
- [ ] Add cron entry: 0 8 * * 2,4 to post from queue via twitter_warmup_poster.py
- [ ] Build /MONEY_METHODS/APP_FACTORY/builds/preseed-scorecard/ static HTML checklist (5 questions, instant score) — deploy to surge.sh
- [ ] Add scorecard URL to posting_queue posts as CTA
- [ ] Wire scorecard page into sitemap + SEO metadata targeting 'pre-seed pitch deck checklist'

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
