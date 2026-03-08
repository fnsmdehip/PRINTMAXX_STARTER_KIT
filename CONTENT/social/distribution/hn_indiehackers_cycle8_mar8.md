# HN + IndieHackers distribution - cycle 8 - march 8 2026

status: PENDING_REVIEW
platform: hackernews, indiehackers
created: 2026-03-08

---

## HACKER NEWS POST 1

**Title:** Show HN: PageScorer - Free website audit tool, no signup required

**URL:** https://pagescorer.surge.sh

**Comment (post immediately after submitting):**

I kept paying $15/mo for GTmetrix Pro to run Lighthouse audits on client sites. felt dumb when i realized all of that can run client-side.

PageScorer runs performance, SEO, and accessibility checks entirely in your browser. no backend. no tracking. no account. open the page, paste a URL, get results.

the whole thing is vanilla JS. no framework, no build step. runs Lighthouse-style scoring with the same metrics (LCP, CLS, FID) but without sending your URLs to anyone's server.

technical details:

- all computation happens in the browser via the Performance API and DOM analysis
- zero network requests after initial page load (no analytics, no telemetry)
- works offline once loaded (it's a PWA, 47KB total)
- scoring algorithm mirrors Lighthouse v11 weights
- outputs a shareable report as a static HTML file

i built this because the free tiers on GTmetrix and PageSpeed Insights rate-limit you after 5-10 checks. if you're auditing 30+ pages for a client, that gets annoying fast.

source is readable (view-source, no minification). happy to answer questions about the scoring methodology.

---

## HACKER NEWS POST 2

**Title:** Show HN: I built 16 streak-tracking PWAs for niche communities (55KB each, $0 hosting)

**URL:** https://printmaxx-apps.surge.sh

**Comment (post immediately after submitting):**

i built a base template for streak/habit tracking PWAs and used it to ship 16 apps targeting specific communities. each one is under 55KB, works offline, and costs $0/mo to host.

the apps cover religious text reading (quran, torah, gita, scripture), fitness, coding, journaling, meditation, reading, art, and language learning. each has content specific to that community instead of being a generic habit tracker.

technical approach:

- base template: HTML + vanilla JS + CSS. no framework. the template is ~40KB
- customization per app: content arrays (streak messages, daily prompts), color themes, icons, onboarding copy
- storage: localStorage only. no backend, no database, no accounts
- deployment: surge.sh static hosting. `surge ./app-dir appname.surge.sh` and done
- PWA: service worker for offline, manifest for install prompt. all apps are installable to home screen
- total time from template to deployed app: about 20 minutes per variant

the tradeoff is obvious: no sync across devices, no social features, no cloud backup. for a simple daily streak tracker, i think that's fine. most people use these on one phone.

hosting cost breakdown: surge.sh free tier gives unlimited projects with custom subdomains. 16 apps * $0 = $0/mo. the only ongoing cost is the domain if you want a custom one.

what i learned: niche communities respond better to "quran streak tracker" than "habit tracker with quran mode." the specificity is the feature.

---

## HACKER NEWS POST 3

**Title:** Show HN: ColdMaxx - Free cold email management tool (no monthly fee)

**URL:** https://coldmaxx-app.surge.sh

**Comment (post immediately after submitting):**

i was paying $30/mo for Instantly to manage cold email campaigns. most of what i used was: save templates, track which prospects i emailed, schedule follow-ups. that's a spreadsheet with extra steps.

ColdMaxx does those three things as a PWA. runs in your browser. everything stored in localStorage. no backend, no monthly fee.

what it does:

- campaign management: create campaigns, add prospects, track status (sent, replied, bounced, meeting booked)
- template library: save and reuse email templates with variable placeholders ({firstName}, {company}, etc.)
- follow-up scheduling: set follow-up dates, get a daily view of what needs to go out
- basic analytics: reply rates, open tracking (if you use a pixel service), conversion by campaign

what it does NOT do:

- actually send emails (you still use Gmail/Outlook/SMTP)
- warm up inboxes
- provide lead databases
- A/B test at scale

the target user is someone sending 10-50 cold emails per day manually who wants to stay organized without paying for a full platform. if you're doing 500+ emails/day with automated sequences, you need Instantly or Smartlead.

it's a PWA (installable, works offline) built with vanilla JS. about 62KB total. all data stays in your browser.

i'm not pretending this replaces the paid tools for power users. it replaces the "i track prospects in a Google Sheet" workflow for people who don't need automated sending.

---

## INDIEHACKERS POST 1

**Title:** 35 days, 168 deployed sites, $0 revenue. here's why building is the easy part

**Body:**

i've been going hard on a solo portfolio strategy for 35 days now. here's where i am:

- 22 apps built and deployed (all PWAs, $0 hosting)
- 13 digital products created (PDF guides, templates, toolkits)
- 168 sites live across surge.sh
- 364 tweets written, scheduled, and... not posted
- 1,111 leads scraped and organized
- $0 revenue

the math on paper looks great. 22 apps, if even 2 get traction at $5/mo, that's $10/mo. 13 products on Gumroad at $9 each, sell 1 per week, $36/mo. it adds up fast. on paper.

the problem is i never flipped the switch from building to selling.

building is dopamine. you write code, something appears on screen, you deploy it, you feel productive. i can build a new PWA in 2 hours. i can write a new landing page in 45 minutes. i can generate 50 tweets in 20 minutes.

selling is anxiety. posting content means people might ignore it. listing a product means someone might say it sucks. sending a cold email means someone might not reply. so instead of doing those things, i built another app.

here's my ratio: 35 days of building, 0 days of selling. i have a content queue with 364 posts and haven't posted a single one.

if i could start over, i'd spend day 1 selling something, even if it was ugly and half-broken. sell first, build the thing people actually want second.

what i'm changing now:

1. posting the queued content starting today (literally just hitting publish on what already exists)
2. listing the 13 products on Gumroad this week (they're done, just not listed)
3. no new apps until the existing 22 are actually marketed
4. measuring days by "things sold" not "things built"

what's your build-to-sell ratio? curious if anyone else has this problem or if i'm uniquely dumb about this.

---

## INDIEHACKERS POST 2

**Title:** the PWA portfolio strategy: why i'm betting on 22 small apps instead of 1 big one

**Body:**

most indie hacker advice says pick one idea and go deep. i went the opposite direction. i built 22 small PWAs in 35 days and deployed all of them for $0/mo.

here's the thesis:

if each app has a 10% chance of getting meaningful traction (100+ monthly users), then:
- 1 app = 10% chance of a hit
- 5 apps = 41% chance of at least 1 hit
- 10 apps = 65% chance
- 22 apps = 90% chance

that's basic probability, not optimism. the key is keeping marginal cost near zero so failed apps don't hurt.

how i keep costs at $0:

- stack: HTML, CSS, vanilla JS. no framework, no build tools, no dependencies
- hosting: surge.sh free tier (unlimited static sites)
- backend: none. localStorage for all data persistence
- auth: none. no accounts, no databases
- size: each app is 40-65KB total. loads in under 1 second on 3G

the apps cover different niches: religious streak trackers (quran, torah, gita, scripture variants for 12+ denominations), fitness tracking, cold email management, website auditing, sleep tracking, meal planning, focus timers.

each app took 1-3 hours to build using a shared base template. the template handles PWA setup (service worker, manifest, install prompt, offline support). i just swap in the content, colors, and niche-specific features.

tradeoffs i'm accepting:

- no cross-device sync (localStorage only)
- no social features
- can't do server-side processing
- each app is simple by design (1-2 core features)
- no app store presence (PWAs only, web distribution)

the portfolio approach also compounds with content. 22 apps = 22 different niches to write about. 22 subreddits to contribute to. 22 comparison pages to rank for. 22 angles for cold outreach.

biggest risk: spreading too thin and none of them getting enough attention. i'm testing a strategy where i rotate marketing focus weekly. week 1 = push the sleep tracker. week 2 = push the cold email tool. track which one gets the best response and double down.

current numbers: 22 apps deployed, 168 total sites (includes landing pages and comparison pages), 0 revenue. i'm at the "now sell something" phase.

anyone else running a portfolio strategy instead of going all-in on one product? curious about your experience.

---

## POSTING NOTES

HN posting strategy:
- post Show HN items between 8-10am EST (peak HN traffic)
- post the URL submission, then immediately add your descriptive comment
- don't self-promote in the comment. be technical and honest about tradeoffs
- respond to every comment within the first 2 hours
- if someone finds a bug, fix it live and reply with "fixed, thanks"

IndieHackers posting strategy:
- post between 9-11am EST
- use lowercase titles (matches the platform vibe)
- be honest about failures. IH readers hate fake success stories
- end with a question to drive comments
- cross-post to IH Twitter account and tag @IndieHackers

Priority order:
1. IH Post 1 (the honest failure narrative, highest engagement potential)
2. HN Post 2 (PWA portfolio, most technically interesting)
3. HN Post 1 (PageScorer, clear Show HN format)
4. IH Post 2 (portfolio strategy, builds on post 1)
5. HN Post 3 (ColdMaxx, niche but solid)

don't post all 5 on the same day. spread across 3-4 days. never more than 1 HN submission per day (you'll get flagged).
