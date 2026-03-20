# Competitive Intel Findings, 2026-03-08 (Cycle 15)

## HIGH ALERT: Focus App Competitor Trending

Source: r/SideProject | Score: 149↑ 31💬
Post: "I built an app to blur everything except the active window so I can stop getting distracted"
URL: https://www.reddit.com/r/SideProject/comments/1ro5qyx/

**Competitive Analysis:**
- Single-feature focus app, simple value prop
- 149 upvotes on launch = strong product-market fit signal
- Directly competes with: ADHD apps, PrayerLock (distraction-blocking use case)
- Feature gap we can exploit: faith-based focus mode (PrayerLock already has this angle)
- Action: Add blur/focus feature to PrayerLock roadmap. Frame as "prayer focus mode"

**Content Angle (tweet):**
someone just shipped a focus app that blurs everything except your active window. 149 upvotes day 1.

the market for "stop me from getting distracted" is still wide open.

we built PrayerLock for the same reason. different angle. same pain.

---

## Pain Point Goldmine: 383 Posts Scraped Today

Top pain points by engagement score (80/100):
1. "Is there a tool that can both mass rename and..." (looking_for, tool gap)
2. "A Complete Beginner-Friendly Guide to Earning..." (frustrated_with, info gap)
3. "I moved to another continent to chase my ambitions..." (need_help, 43↑ 34💬)
4. "Need help with google ads and extremely weird traffic" (4↑ 26💬)

**Content angles:**
- "reddit pain points are the best product research. checked today: 383 posts. most wanted: a simple tool to mass rename files with AI. someone build this."
- "went through 383 reddit posts looking for what people actually need. surprising: the CSS grid help request had 22 comments in 2 hours. devs are desperate for basics."

---

## Schema Fix Needed (P2)
background_reddit_scraper.py writes `date_found` to `status` column → alpha_auto_processor.py finds 0 PENDING_REVIEW entries → no auto-routing.
Fix: align column order in background_reddit_scraper.py to match ALPHA_STAGING.csv headers.

