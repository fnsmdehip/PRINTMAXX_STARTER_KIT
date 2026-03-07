# IndieHackers Distribution Posts
status: PENDING_REVIEW
created: 2026-03-07T06:00:00Z
cycle: distribution_engine_2

---

## Post 1 — Milestone: 77 sites, 13 apps, $0 revenue (building in public)

**Title:** I built 77 websites and 13 apps. Revenue: $0. Here's what I'm doing about it.

**Body:**

the numbers:
- 77 websites deployed on surge.sh ($0 hosting)
- 13 PWA apps (streak trackers for various niches)
- 131 digital products prepped for Gumroad/Whop/Etsy
- 6 local business demo sites for cold outreach
- 10 SaaS-style tools (site auditors, cold email tools, ROI calculators)
- 1 MCP server marketplace

total revenue generated: $0.

not because the products are bad. because I never distributed them.

I spent 3 months building. every week something new shipped. I got really good at building fast. the problem: I treated "deployed" as "done." it's not. deployed means nobody knows about it.

here's my distribution checklist I'm working through now:

1. list all 131 digital products on Gumroad (blocker: need Stripe account set up)
2. submit SiteScore and PrayerLock to Product Hunt
3. post about streak apps on r/SideProject, r/webdev, r/nocode
4. cold email local businesses using demo sites as proof
5. write LinkedIn posts about the $0 tech stack
6. submit tools to app directories (AlternativeTo, SaaSHub, BetaList)
7. launch newsletter with weekly build updates

the lesson: building is a comfort zone. distribution is the real work. I can spin up a functional app in 4 hours. getting one person to pay for it takes 2 weeks of consistent outreach.

if you're in a similar spot (tons built, nothing sold), my advice: stop building. spend the next 30 days doing nothing but distribution. list, post, email, submit. the product is done. the marketing isn't.

will update this thread with revenue as it comes in. starting from literal $0.

---

## Post 2 — Technical Deep Dive: PWA Factory Pattern

**Title:** How I template-deployed 13 PWAs in a weekend (code pattern + deploy pipeline)

**Body:**

the pattern is simple: one base template, one config per app, one build script, one deploy loop.

base template:
```
/template/
  index.html      (uses {{TITLE}}, {{COLOR}}, {{DESCRIPTION}} placeholders)
  styles.css      (CSS variables pulled from config)
  app.js          (streak logic, identical across all apps)
  sw.js           (service worker for offline)
  manifest.json   (templated with app name, icons, theme color)
```

config per app (config.json):
```json
{
  "name": "Quran Streak",
  "slug": "quran-streak",
  "color": "#1a7a4c",
  "icon": "quran.png",
  "description": "track your daily quran reading streak",
  "category": "religious"
}
```

build script (python, ~40 lines):
- reads config.json
- replaces placeholders in template files
- copies to /dist/{slug}/
- generates icons at multiple sizes

deploy loop (bash, 3 lines):
```bash
for dir in dist/*/; do
  slug=$(basename "$dir")
  surge "$dir" "${slug}-app.surge.sh"
done
```

the whole pipeline runs in under 2 minutes for all 13 apps.

why PWAs over native:
- no app store review (deploy in 30 seconds)
- no 30% platform cut
- works on every device with a browser
- offline-capable with service workers
- installable to home screen
- $0 hosting on surge.sh

the real question isn't technical. it's market: which communities actually want a streak tracker badly enough to install one? religious communities (daily scripture reading) and fitness communities (daily workout tracking) seem to have the strongest natural fit.

currently testing with ramadan-focused marketing for the quran and prayer apps. ramadan creates urgency: 30 days, 5 daily prayers, perfect streak mechanic.

---

## Post 3 — Ramadan Apps (time-sensitive)

**Title:** I built 2 Ramadan apps (PrayerLock + Hilal) and launched them the week Ramadan started

**Body:**

ramadan started feb 28. I had the apps live by feb 27.

PrayerLock: locks your phone at prayer times. not a reminder. a lock. you mark prayer complete to unlock. 55KB PWA. offline-capable.

Hilal (ramadan-tracker.surge.sh): tracks fasting days, prayer completion, quran reading progress, and charity goals for the 30 days of ramadan. shows countdown to iftar based on your location.

both are free. no accounts. no data collection. everything stores locally on-device.

the timing matters because ramadan apps have a 30-day window of relevance. after eid, usage drops. so the distribution push is happening right now.

channels I'm hitting:
- r/islam, r/MuslimLounge, r/Ramadan
- Islamic Discord servers
- Muslim Facebook groups (local masjid communities)
- Twitter Islamic tech community
- Muslim tech newsletters

the positioning: "built by a Muslim developer for personal use, sharing it free." no monetization on the apps themselves. the play is: build trust with free value, then cross-sell other tools and services later.

if you're building for a seasonal audience, the lesson is: have the product ready BEFORE the season starts, not during.
