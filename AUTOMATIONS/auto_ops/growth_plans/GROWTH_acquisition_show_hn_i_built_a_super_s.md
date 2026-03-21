# Growth Plan: [ACQUISITION] Show HN: I built a super simple email reminder

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo

---

## Tactics

1. Post our clone on Show HN after launch — free HN traffic spike, engineers are buyers
2. Comment on original Show HN thread linking our version as 'extended/monetized fork'
3. SEO: 'free email reminder tool', 'remindme bot alternative', 'set email reminder online' — all low-competition longtail
4. ProductHunt launch queued for email reminder app — category: Productivity
5. Cross-link from SoberStreak, FocusLock, PrayerLock landing pages (same user: habit/reminder audience)
6. Reddit r/productivity, r/lifehacks, r/sideproject post: 'Built a dead-simple email reminder in a weekend'

## Budget Tier Strategies

### FREE
Show HN post, HN comment engagement on original thread, Reddit organic posts, longtail SEO targeting 'remindme alternative' and 'free email reminder scheduler', cross-link from existing 47 live apps, surge.sh deploy with sitemap

### LOW
$10-20/mo Reddit ads on r/productivity targeting 'reminder app' keyword, Resend free tier (3K emails/mo) covers early users at zero cost

### MID
$50-100/mo Google Ads on 'email reminder tool free' + 'schedule email reminder' — low CPC niche, direct buyer intent

## Daily Actions

- [ ] Enhance existing hn_ph_scraper (already in AUTOMATIONS/) to filter 'Show HN: I built' posts with 50+ upvotes and single-purpose utility signals
- [ ] Score each candidate: GitHub stars <500 (low competition), tool type = utility/productivity, build complexity LOW (single file or <500 lines), existing SaaS price >$5/mo (monetization gap exists)
- [ ] Append top 3 weekly candidates to AUTOMATIONS/agent/autonomy/app_factory_priority_queue.json with clone_spec JSON
- [ ] For THIS entry specifically: build email-reminder micro-SaaS using Resend API + SQLite + minimal HTML form — deploy to surge.sh as email-reminder.surge.sh
- [ ] Wire Stripe Payment Link ($3/mo Pro: unlimited reminders vs 5 free) via payment_integrator.py --wire-app
- [ ] Generate SEO landing page targeting 'free email reminder', 'remindme bot alternative', 'schedule email reminder online'
- [ ] Generate 3 tweets + 1 Show HN-style thread: 'I cloned the HN email reminder bot and added X' — route to CONTENT/social/posting_queue/

## Tooling

```json
{
  "browser": "playwright (HN scraping)",
  "email": "Resend free tier (3K/mo) \u2014 swap for Sendgrid if volume grows",
  "content": "content_factory",
  "payments": "Stripe Payment Link \u2014 $3/mo Pro tier, wire via payment_integrator.py"
}
```
