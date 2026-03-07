# HN Show Posts + Tweet Storms — 2026-03-07
# Status: APPROVED (quality gate cycle 6)
# Account: @PRINTMAXXER
# Assets: surge.sh PWA portfolio + 77-site deployment
# Pre-publish: zero em dashes, zero banned vocab, consequence-first, exact numbers

---

## SHOW HN POSTS

---

### Show HN #1 — 13 streak-tracking PWAs for niche communities ($0 hosting)

**Title:**
Show HN: I built 13 streak-tracking PWAs for niche communities (all live, $0/mo hosting)

**Body:**
I got tired of paying for infrastructure on side projects that might never make money. So I stripped everything out.

13 apps. All streak trackers. Each one targets a different micro-community: Quran readers, Torah learners, Sikh practitioners, Catholics, Mormons, Lutherans, Anglicans, meditators, runners, coders, artists. All live on surge.sh right now.

Tech: vanilla JS, Web App Manifest, Service Worker with cache-first strategy, localStorage for state, IndexedDB for streak history. No backend. No database. No server. The whole thing runs in the browser.

The tradeoff is obvious: no cross-device sync, no push notifications on iOS (PWA limitation), no accounts. I made that call deliberately. The target user opens the app once a day on the same phone. They don't need an account. They need a streak counter that works offline.

Deploying 13 apps took about 4 minutes total. One bash loop, one surge token, 13 subdomains.

I'm curious if anyone else has pushed the no-backend PWA approach this far, and what the actual adoption ceiling looks like before the offline-only constraint kills retention.

**Word count:** 178

---

### Show HN #2 — SiteScore free website analyzer

**Title:**
Show HN: SiteScore – audit any website in 10 seconds, free, no signup

**Body:**
I built this because I kept paying for Lighthouse-adjacent tools that wrapped the same free APIs I could hit directly.

SiteScore aggregates 4 free public data sources into one score: Google PageSpeed Insights API (performance + CWVs), SSL Labs API (cert grade), SecurityHeaders.io (header audit), and Mozilla Observatory (security score). No backend. The browser calls the APIs directly. No data leaves to my server because there is no server. Static HTML + vanilla JS on surge.sh.

The result is a single 0-100 score with a breakdown by category. Takes 8-12 seconds depending on API response times.

Honest limitations: SSL Labs can queue for 30-60s on uncached domains. SecurityHeaders rate-limits at 10 req/hr per IP. For personal use it's fine. For CI/CD pipelines it breaks fast.

The broader point is API arbitrage: most "premium" site audit tools charge $50-200/mo for something you can build in a weekend by gluing free public APIs together. The value they add is mostly UI.

sitescore-app.surge.sh

**Word count:** 185

---

### Show HN #3 — PrayerLock 55KB PWA

**Title:**
Show HN: PrayerLock – 55KB PWA that intercepts your phone before you scroll

**Body:**
The app is 55KB total. No dependencies. No framework. No tracking. No analytics. No backend.

The concept: when you open your phone, PrayerLock fires a prayer prompt before you get to your feed. It uses the Page Visibility API to detect when the tab regains focus, then surfaces a short prayer or scripture. You pray, you dismiss, you continue. Or you don't. No guilt loop.

It's a PWA so it installs to your home screen on Android in 2 taps (iOS requires the manual "Add to Home Screen" step, which kills casual adoption but the target user is motivated enough to do it). Offline-capable via Service Worker. Works with zero signal.

I made it deliberately small. The production build is one HTML file, one CSS file, one JS file. The whole thing fits in a single HTTP request if you inline it.

The constraint that produced the 55KB target: I wanted it to load on a 3G connection before the user changed their mind.

prayerlock-app.surge.sh

**Word count:** 172

---
---

## TWEET STORMS

---

### Storm 1 — "I mass-deployed 77 websites for $0. here's how."

**1/7**
I deployed 77 websites last week.

hosting cost: $0
time to deploy all 77: under 20 minutes

here's exactly how.

---

**2/7**
surge.sh is the answer most people skip over.

static site hosting. free tier is unlimited projects. custom subdomains. deploys in seconds from CLI.

`surge ./my-site my-site.surge.sh`

that's the whole deploy command.

---

**3/7**
I wrote one bash loop.

```
for dir in sites/*/; do
  name=$(basename "$dir")
  surge "$dir" "${name}.surge.sh"
done
```

77 folders. 77 deploys. one loop. 18 minutes.

no Vercel. no Netlify. no AWS. no credit card.

---

**4/7**
the template system is what makes 77 sites possible.

one base HTML template. swap the title, the color, the niche keyword. write it to a folder. repeat.

python script. 40 lines. generates a new site in 0.3 seconds.

i have 131 more assets ready to deploy the same way.

---

**5/7**
"but how do you manage 77 sites"

you don't manage them. that's the point.

static HTML doesn't go down. doesn't need updates. doesn't need patches. doesn't need a sysadmin.

set it. leave it. let it compound.

---

**6/7**
the full stack for $0/month:

- surge.sh (hosting)
- vanilla JS (no npm, no build step)
- Service Workers (offline capability)
- localStorage (data persistence)
- GitHub (version control, free)

zero SaaS subscriptions. zero recurring cost.

---

**7/7**
77 live sites. $0 hosting. 20 minutes of work.

the only thing stopping you from doing the same is overthinking the stack.

surge.sh + bash loop + one template. that's it.

what's your current monthly hosting bill? #buildinpublic

---
---

### Storm 2 — "I built 13 apps in 48 hours. each one targets a different micro-niche."

**1/6**
I built 13 apps in 48 hours.

each one targets a different community that has almost zero apps built for them.

they're all live right now.

---

**2/6**
the niche list:

Quran streak tracker. Torah. Sikh. Catholic. Mormon. Lutheran. Anglican. Evangelical. Orthodox. Buddhist. Gita.

then secular: coding streak. fitness streak. meditation streak. art streak.

communities with millions of members. apps built for them: basically none.

---

**3/6**
the approach: streak mechanic + PWA + no backend.

streak mechanics are the highest-retention feature in consumer apps. duolingo built a $6B company on one mechanic.

i copied the mechanic. i targeted communities they don't serve.

---

**4/6**
PWA means no app store gatekeeping.

no $99/yr Apple developer account to start. no review process. no 30% cut on in-app purchases until you're ready.

install to home screen. works offline. pushes to production in 4 minutes.

---

**5/6**
why 13 apps instead of 1?

because one of them will hit. i don't know which one yet.

the bet is diversification across niches, not perfection in one.

13 at-bats costs the same time as 1 well-polished miss.

---

**6/6**
13 apps. 48 hours. $0 infrastructure.

all live. all indexed. all waiting for someone to care.

which niche should i build next? drop it below and i'll ship it this week.

---
---

### Storm 3 — "the $0/month indie hacker stack nobody talks about"

**1/7**
everyone talks about their $100/mo Vercel bill.

mine is $0.

not because i'm cheap. because the stack i use doesn't need it.

here's the whole thing.

---

**2/7**
hosting: surge.sh

free. unlimited projects. custom domains. deploys from CLI in one command. no cold starts. no edge functions you don't need. just static files on a CDN.

most solopreneur apps don't need a server. they need to stop pretending they do.

---

**3/7**
frontend: vanilla JS

no React. no Next.js. no npm. no build step. no 300MB node_modules folder.

one HTML file. one CSS file. one JS file.

loads in under 1 second on 3G. works offline via Service Worker. installs to home screen as a PWA.

---

**4/7**
data layer: localStorage + IndexedDB

for a streak tracker, a habit app, a timer, a prayer reminder: you don't need a database.

the user's phone IS the database.

zero GDPR headaches. zero breach liability. zero monthly cost.

---

**5/7**
the tradeoff is real and i'm not hiding it.

no cross-device sync. no server-side analytics. no push notifications on iOS.

if your app needs those things, pay for the server. but most apps people build don't need them. they add them because it feels more "real."

---

**6/7**
the $0 stack in full:

- surge.sh: hosting
- vanilla JS: frontend
- Service Worker: offline + caching
- localStorage: user data
- GitHub Actions: optional CI

monthly cost: $0
deploy time: 4 minutes
apps live right now: 77

---

**7/7**
the $100/mo Vercel bill is optional.

most people pay it because they copy the stack from tutorials, not because their app needs it.

what's your monthly hosting cost right now?

if it's above $0 i want to know what you're running that actually needs it.

---
---

### Storm 4 — "I have 131 products ready to list and $0 revenue. here's the plan."

**1/7**
i have 131 products ready to list.

current revenue: $0.

not a failure story. a distribution problem.

here's what i'm doing about it.

---

**2/7**
the breakdown of 131 products:

- 77 deployed websites
- 13 PWA apps
- 20 digital products for Etsy (printables, templates)
- 15 KDP listings (low-content books)
- 8 Whop community products
- 10 Fiverr service listings
- 13 Gumroad digital downloads
- remaining: Redbubble + TeePublic designs

built in ~3 months. $0 in sales.

---

**3/7**
the honest diagnosis:

i've been building. not distributing.

131 products sitting in draft or half-listed is not a portfolio. it's a backlog.

the next 30 days is distribution only. no new builds.

---

**4/7**
platform priority order based on time-to-first-dollar:

1. Gumroad (13 products, direct traffic, lowest friction)
2. Etsy (20 products, search-driven, passive after listing)
3. Fiverr (10 listings, active demand already exists)
4. KDP (15 books, 60-90 day lag before indexing)
5. Whop (8 products, needs community distribution first)

---

**5/7**
what i'm NOT doing:

not building a new app.
not redesigning anything.
not optimizing copy i haven't tested.
not waiting until things are "perfect."

listing is the product now.

---

**6/7**
the math if even 10% converts at $9:

131 products x 10% listed and selling = 13 products
13 x $9 avg = $117/mo

not life-changing. but proof the system works. then i scale what wins.

---

**7/7**
131 products. $0 revenue. day 1 of distribution sprint.

i'm posting the results here regardless of outcome.

which platform should i list on first? Gumroad or Etsy?

vote below. i'll do whichever wins today. #buildinpublic

---

## PRE-PUBLISH QA

- [x] Zero em dashes
- [x] Zero banned AI vocabulary (no leverage, utilize, delve, comprehensive, robust, innovative, seamless)
- [x] Consequence-first hooks on all 7 openers
- [x] Exact numbers throughout (77 sites, 13 apps, 48 hours, 55KB, 131 products, $0, $9, $117)
- [x] Would @pipelineabuser post this: yes
- [x] Lowercase energy: yes
- [x] First sentence delivers value: yes
- [x] One hashtag max on final tweet per storm: yes (#buildinpublic)
- [x] No hashtags in body tweets: yes
- [x] HN bodies are 150-200 words: yes (178, 185, 172)
- [x] No "Thread:" prefix: yes
- [x] No exclamation points: yes
- [x] No em-dash abuse: yes
- [x] Tool names, not generic terms: yes (surge.sh, localStorage, IndexedDB, Service Worker, Gumroad, Etsy)
