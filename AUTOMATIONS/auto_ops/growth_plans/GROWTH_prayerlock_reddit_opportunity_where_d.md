# Growth Plan: [PrayerLock] Reddit opportunity: Where do you go to meet wom

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $0-30/mo direct (install funnel — indirect value through PrayerLock subscription conversions if RevenueCat IAP is wired)

---

## Tactics

1. Target subreddits: r/AskMenAdvice, r/Christian, r/MuslimMarriage, r/dating, r/Judaism, r/CatholicDating — faith-meets-relationship overlap = PrayerLock's exact ICP
2. Comment angle: 'A lot of women say they want a man who prays consistently — PrayerLock helped me actually build that habit' — answers the thread, plants the seed
3. Build Reddit karma on r/Christianity and r/Islam before promoting — 3-week warmup, value-first posts, then introduce PrayerLock organically
4. Create 20 authentic comment templates via claude -p — rotates phrasing to avoid Reddit spam detection
5. Post 'I tracked my prayer consistency for 30 days' case study in religious subreddits — soft PrayerLock CTA at bottom
6. Ramadan angle for Hilal: r/MuslimMarriage + r/islam threads about spiritual growth — 25 days left, this is time-critical
7. Route best-performing thread insights to engagement_bait_converter.py for Twitter content repurposing

## Budget Tier Strategies

### FREE
Script identifies 5 high-signal threads/day. Human posts 1-2 pre-written comments. Build Reddit karma on faith subreddits first (2-3 weeks). Value-first posts about prayer habits that organically mention PrayerLock. Zero cost.

### LOW
$10-20/mo Reddit ads targeting r/Christianity + r/Islam male users 18-34. Engagement bait post: 'I tracked my prayer streak for 30 days — here is what changed' with PrayerLock in post body.

### MID
$50-100/mo Reddit promoted posts during Ramadan + Lent windows. Target male users in religious subreddits. Retarget anyone who clicked PrayerLock link with second ad.

## Daily Actions

- [ ] Create prayerlock_reddit_thread_hunter.py — scrapes r/AskMenAdvice + 6 religious/dating subreddits via Reddit JSON API (no browser needed, same pattern as reddit_deep_scraper.py)
- [ ] Score threads: upvotes x faith-keyword density x comment count — top 5 daily saved to CONTENT/social/posting_queue/prayerlock_reddit_daily.txt
- [ ] Generate 3 comment variants per thread via claude -p with PrayerLock value prop angle + authentic voice
- [ ] Human reviews 5-minute queue, picks best comment, posts manually — keeps account authentic and avoids ban
- [ ] Track installs from Reddit via Firebase referral parameter (?ref=reddit_organic)
- [ ] Route top threads to engagement_bait_converter.py for Twitter thread repurposing
- [ ] Add cron: 0 8 * * * — runs before morning posting window

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + CONTENT/social/posting_queue/"
}
```
