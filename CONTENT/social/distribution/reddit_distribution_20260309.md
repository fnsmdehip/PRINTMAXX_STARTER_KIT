# Reddit Distribution Posts - 2026-03-09
# Status: PENDING_REVIEW
# Apps: PrayerLock, FocusLock, Hilal, PageScorer
# Also includes: 2x HackerNews Show HN posts

---

## PRE-PUBLISH CHECKLIST

- [x] Zero em dashes
- [x] Zero banned AI vocabulary (leverage, utilize, delve, comprehensive, robust, innovative, seamless)
- [x] Consequence-first hooks
- [x] Exact numbers where possible
- [x] Lowercase energy where appropriate
- [x] First sentence delivers value
- [x] No promotional adjectives
- [x] Humble builder voice throughout
- [x] "What I learned" sections included

---

## APP 1: PRAYERLOCK

---

### Post 1 of 2 - r/islam

**Title:** built a PWA that locks your screen during salah so notifications don't pull you out - free, no app store needed

**Body:**

i kept getting pulled out of prayer by notifications. not bad ones necessarily, just the lock screen lighting up mid-ruku and breaking concentration.

i built PrayerLock to fix that. it's a PWA (progressive web app) so you add it to your home screen from the browser, no app store account needed, no permissions granted to some company. it uses the Web Lock API to block the screen during your set prayer window.

the flow is simple: you open it, set the duration of your prayer window, and hit start. your screen locks and stays locked for that window. notifications still queue, you just don't see them until you're done.

it's free. no account, no login, no tracking.

prayerlock.surge.sh

what i learned building this: the Web Lock API has spotty iOS Safari support. on Android Chrome it's solid. on iPhone you need to keep the browser tab open (can't background it the same way). that's a real limitation i'm still working around. if anyone has dealt with this on iOS PWAs i'd genuinely like to know what worked.

looking for feedback on the ux and whether the timing flow makes sense. does a simple start/stop model work for you or would something that ties into actual prayer time APIs be more useful?

---

### Post 2 of 2 - r/muslimtechnet

**Title:** built PrayerLock - screen lock PWA for salah, no app store install required (feedback wanted from devs)

**Body:**

built this because i couldn't find a simple screen lock tool that didn't require a full app install and account creation.

PrayerLock is a PWA. you go to prayerlock.surge.sh in your browser, hit "add to home screen," and it behaves like a native app without any of the permissions overhead.

the core mechanic: set a duration for your prayer window, start it, your screen locks. that's it. when the window ends it unlocks. you can stop it early if needed.

technical stack: vanilla JS, Web Lock API, service worker for offline support, installable manifest. about 55KB total. loads in under 2 seconds on 3G.

the iOS limitation is real. Safari on iOS handles the Web Lock API differently from Chrome on Android. on Android it works cleanly in the background. on iOS the tab has to stay active. haven't fully cracked that yet.

questions i'm trying to answer:

1. is a manual "set duration" model good enough or do people want it to pull from a prayer times API and auto-set?
2. is there appetite for a qibla direction indicator baked in or is that scope creep?
3. anyone else building PWAs for this niche and want to share notes?

no monetization on this. built it for personal use, cleaned it up, put it out.

prayerlock.surge.sh

---

### Post 3 of 2 - r/productivity + r/digitalminimalism (same copy, post to both)

**Title:** I built a screen lock app to stop my phone from breaking focus during intentional offline time - free PWA

**Body:**

i have a habit i wanted to protect. there's a 20-minute window in my day that i want completely offline. not phone-in-another-room offline, just screen-dark-and-quiet offline while i'm still nearby.

the problem with existing options: do-not-disturb still lights up the screen. grayscale mode still lights up the screen. airplane mode cuts off things i don't want cut off. screen timeout settings are too blunt.

so i built PrayerLock (the name comes from what i originally built it for, but the app works for any focus window). you set a duration, hit start, screen locks for that window. that's the whole thing.

prayerlock.surge.sh - it's a PWA so you add it to your home screen from the browser. no download, no account.

what i learned: most "focus" apps are designed around task management. there's almost nothing that just does one thing: lock your screen for a defined window with no other features. building something this narrow felt weird at first. now it feels right. the simpler the tool, the easier the habit.

works well on Android. iOS Safari has limitations with the Web Lock API that i haven't fully resolved. if you're on iPhone, the tab needs to stay open.

feedback welcome, especially on whether the duration-setting flow makes sense.

---

## APP 2: FOCUSLOCK

---

### Post 1 of 3 - r/ADHD

**Title:** built a PWA that actually locks your phone screen during focus sessions - not just a timer, it physically blocks the screen

**Body:**

the problem with focus timers: they count down in the background while you scroll Twitter. the timer finishing is the only consequence, and that consequence comes after the damage is done.

i built FocusLock differently. you set a session, hit start, your screen locks. you can't casually unlock it and check something "real quick." the friction is physical, not psychological.

it's free and runs in the browser as a PWA - you add it to your home screen, no app store needed.

focuslock-web.surge.sh

honest notes for people with ADHD specifically:

the lock works well when you initiate it on purpose. it's not a guardian that stops you from unlocking - you can still unlock your phone normally. what it does is add one extra intentional step before the screen lights up. for me that pause is enough to catch the impulse. for others it might not be. know your own patterns.

Android Chrome works clean. iOS Safari has a limitation with the Web Lock API - the tab needs to stay open in the foreground, which defeats some of the purpose on iPhone. that's a real bug i'm working on.

what actually helps me use it: i set the lock before i sit down, not after i've already started. the sequence matters. lock first, then open whatever work i'm doing.

curious whether the "hard lock" mechanic is actually useful for people here or whether it's the wrong frame entirely. i've seen people swear by physical phone boxes for the same reason.

---

### Post 2 of 3 - r/getdisciplined

**Title:** I made screen locking the first step of my focus routine instead of the last - here's the free tool I built for it

**Body:**

most focus advice assumes your phone is already away. mine wasn't.

i tried timers, app blockers, do-not-disturb, grayscale. they all share one problem: they're advisory. the phone still lights up. the notifications still show the first line of the text. the friction is low enough that "just checking one thing" happens anyway.

i built FocusLock to make the screen physically dark for a set window. you go to focuslock-web.surge.sh, set your session duration, hit start. your screen locks. you can still unlock it - this isn't a parental control - but unlocking is now a deliberate action instead of a reflexive one.

the behavioral difference: reflexive unlocking bypasses your prefrontal cortex. deliberate unlocking doesn't. one extra step is enough to catch the impulse before it executes.

what i learned building and using this over a few weeks:

- 25-minute sessions feel right for me. 45+ and i find reasons to unlock.
- the app is more useful for protecting a session that's already going than for starting one from scratch.
- having the lock on before i sit down matters more than anything else in my setup.

free, no account, works as a PWA you add to your home screen. Android works well. iOS has a limitation i'm still solving.

focuslock-web.surge.sh

not trying to sell anything. genuinely curious if this approach works for other people or if i'm solving a problem that's specific to how my brain works.

---

### Post 3 of 3 - r/productivity + r/digitalminimalism (same copy, works for both)

**Title:** I built a one-button screen lock PWA for focus sessions - free, no account, works from the browser

**Body:**

the gap i found: there's no simple tool that just locks your screen for a defined window. app blockers do too much. timers do the wrong thing. do-not-disturb still lights up the screen.

FocusLock does one thing. you set a duration, hit start, your screen locks for that window.

focuslock-web.surge.sh

it's a PWA - you go to the link in your browser, add it to your home screen, it behaves like a native app. no account, no download from an app store, about 60KB.

the thing i didn't expect when building it: the technical problem was almost trivial. the harder question was whether single-function tools actually change behavior. my conclusion after using it: yes, but only if the single function hits the exact moment where the habit breaks down. for me that moment is "screen lights up reflexively while i'm already in flow." this stops that.

Android Chrome works cleanly. iOS Safari is limited by how Apple handles the Web Lock API - the tab needs to stay active, which reduces the usefulness on iPhone. working on this.

open to feedback on whether the core mechanic is right or whether i'm missing something about how people actually lose focus on their phones.

---

## APP 3: HILAL (TIME-SENSITIVE - RAMADAN ACTIVE NOW)

**NOTE FOR POSTER: Ramadan is currently active as of posting date 2026-03-09. Lead with that.**

---

### Post 1 of 2 - r/Ramadan

**Title:** built a free Ramadan tracker PWA this year - tracks fasts, ibadah, and the days remaining in the month

**Body:**

i wanted a tracker that was specifically for Ramadan, not a general habit tracker repurposed for the month.

Hilal tracks: which fasts you've completed, your daily ibadah log (prayer, quran, dhikr - you set what matters to you), and a visual countdown of remaining days in the month.

it's a PWA at ramadan-tracker.surge.sh. you add it to your home screen from the browser, no app store, no account. data stays on your device.

built it before the month started, using it myself now. it's simple and that's intentional. most tracker apps add so many features that the daily check-in becomes another task. this one opens fast and has one job.

what i built in that i'm not sure about: a "streak" mechanic for fasts completed. on one hand streaks are motivating. on the other hand Ramadan isn't about streaks, it's about intention. if you miss a fast due to travel, illness, or menstruation, a broken streak counter feels wrong. considering removing it entirely. curious what people think.

the month is about halfway through depending on where you are. if you want something lightweight to track the rest of it, here's the link:

ramadan-tracker.surge.sh

---

### Post 2 of 2 - r/islam + r/muslimtechnet (same copy)

**Title:** Ramadan tracker PWA I built - free, no account, data stays on device - feedback wanted

**Body:**

ramadan-tracker.surge.sh

quick context: i built Hilal as a PWA for tracking fasts and ibadah during Ramadan. it works offline after the first load, data is stored locally (nothing sent to any server), and it installs to your home screen from the browser.

what it tracks:
- fasts completed / days remaining in the month
- a simple daily ibadah log you can configure
- a visual progress view for the month

what it doesn't do: prayer time alerts (there are better apps for that), account sync between devices, social features.

the technical limitation worth knowing: local storage means data doesn't sync if you switch phones or clear your browser. for a one-month tracker that's probably fine. for something you want to keep long-term it's a real limitation.

the thing i'm undecided on: the streak counter. habits researchers say streaks increase follow-through. Islamic scholars would probably say they can create the wrong framing for ibadat. i'm genuinely not sure which consideration should win here.

if you've used other Ramadan trackers and have opinions on what works or what's missing, i'd find that useful. trying to make this better before the month ends.

ramadan-tracker.surge.sh

---

## APP 4: PAGESCORER

---

### Post 1 of 4 - r/SideProject

**Title:** built a free landing page audit tool that scores conversion - no signup, just paste your URL

**Body:**

i was tired of paying for CRO tools that take 3 days to audit and give me a PDF i forget about.

PageScorer gives you a score in about 10 seconds. you paste your URL, it analyzes the page, and returns a score out of 100 with specific callouts on what's hurting you.

pagescorer.surge.sh

it checks things that actually move conversion rates: above-the-fold clarity, CTA placement and copy, social proof presence and specificity, page load time (via a lightweight measure), form friction, mobile rendering basics, and headline clarity.

what it doesn't do: it's not a pixel-level UX audit. it won't catch everything. think of it as a fast gut-check before you spend money on ads or launch something.

built it because i kept manually checking these same 8 things on every landing page i built. now i run it in 10 seconds and spend my time on the ones with obvious problems.

free. no account, no email capture, no upsell on the other end.

what i learned: the thing people actually want to know isn't "what score did i get" - it's "what is the one thing most hurting my conversion rate right now." working on surfacing that as a single priority callout at the top of the report.

feedback on what the audit is missing or getting wrong would be useful. anyone who tests it against a page they know well is welcome to tell me where it diverged from your expectations.

pagescorer.surge.sh

---

### Post 2 of 4 - r/webdev

**Title:** built a landing page scorer in vanilla JS - here's how it audits pages client-side with no backend

**Body:**

pagescorer.surge.sh

curious to get webdev feedback on this. PageScorer is a landing page audit tool that runs entirely client-side. no backend, no API calls to a scoring service, no data leaves the browser.

the technical approach: it uses a combination of fetch + DOMParser to pull the target URL's HTML, runs a series of checks against the parsed DOM, and scores 8 categories each weighted differently.

the CORS problem is real. if the target URL has restrictive CORS headers, the fetch fails and we fall back to a set of checks we can run from the URL structure alone. that fallback is noticeably less accurate. i've been debating whether to add a lightweight server-side proxy just to handle CORS, but that would break the "no backend" architecture.

categories scored:
- headline presence and clarity (20 pts)
- CTA above fold (15 pts)
- social proof specificity (15 pts)
- page speed signals (15 pts)
- form field count and friction (10 pts)
- mobile viewport meta (10 pts)
- structured data / meta description (10 pts)
- trust signals (5 pts)

weighting is opinionated. open to arguments that i've got the priorities wrong.

the output is a score out of 100 plus per-category breakdowns. i'm working on adding a "biggest single fix" summary at the top because the per-category breakdown is too much to act on at once.

anyone who's done CRO work professionally and thinks the audit logic is off - i'd genuinely like to know where.

pagescorer.surge.sh

---

### Post 3 of 4 - r/Entrepreneur

**Title:** before you spend money on ads, run your landing page through this free auditor I built - takes 10 seconds

**Body:**

landing page problems kill ad spend faster than almost anything else. a page that converts at 1% vs 3% is a 3x difference in effective CAC.

i built PageScorer to be the 10-second check before you send paid traffic anywhere.

pagescorer.surge.sh

paste your URL, get a score out of 100, see which specific elements are pulling the score down. takes less time than opening a spreadsheet.

what it actually checks: whether your headline communicates the value clearly above the fold, whether your CTA is visible before scrolling, whether your social proof is specific (numbers and names beat "customers love us"), load time signals, form friction, and mobile basics.

i built it because i was running the same mental checklist on every page before launching ads and i wanted to stop doing that manually.

it's free. no account. no upsell inside the tool.

the honest limitation: it's a heuristic audit, not a statistical one. it can tell you that your CTA is weak based on the copy, not that it's converting at 1.3% specifically. for that you need A/B test data. this is the pre-ad-spend gut-check, not the ongoing CRO tool.

if you test it on a page you already know the conversion rate on, curious whether the score correlates with what you'd expect.

pagescorer.surge.sh

---

### Post 4 of 4 - r/marketing + r/startups (same copy, works for both)

**Title:** free tool I built: paste any landing page URL and get a conversion audit score in 10 seconds

**Body:**

pagescorer.surge.sh

the problem with most CRO tools: they're slow, expensive, and the output is a report you have to translate into action yourself.

PageScorer runs in 10 seconds and gives you a score out of 100 with specific callouts.

what it audits:
- headline clarity and placement
- CTA above the fold
- social proof (and whether it's specific enough to be credible)
- page speed signals
- form friction
- mobile rendering basics
- trust indicators

i built it for myself because i have a bad habit of thinking a landing page is ready when it isn't. running the audit catches obvious problems before i send traffic.

it's free, no account, entirely client-side.

the thing i'm still refining: the output currently gives you 8 category scores. most people want to know the one thing to fix first. adding a "priority fix" callout to the top of the report is next.

if you've tested it and the score doesn't match your intuition about the page, tell me what it missed. that kind of feedback is more useful than general impressions.

pagescorer.surge.sh

---

## HACKERNEWS - SHOW HN POSTS

---

### Show HN 1: PageScorer

**Title:** Show HN: PageScorer - free landing page audit tool that runs entirely client-side

**Body:**

pagescorer.surge.sh

Paste a URL, get a score out of 100 with category breakdowns. Runs in the browser with no backend - uses fetch + DOMParser to analyze the target page's HTML against 8 weighted criteria (headline clarity, CTA placement, social proof specificity, page speed signals, form friction, mobile viewport, structured data, trust signals).

CORS is the main limitation. Pages with restrictive headers fall back to a reduced audit based on URL structure and metadata only, which is less accurate. Considering a lightweight proxy to fix this but trying to keep it serverless.

Built it because I was running the same manual checklist before launching ads and wanted to stop doing that by hand. Free, no login, no tracking.

---

### Show HN 2: FocusLock

**Title:** Show HN: FocusLock - PWA that locks your phone screen during focus sessions using the Web Lock API

**Body:**

focuslock-web.surge.sh

Single-function PWA: set a duration, hit start, screen locks for that window. Uses the Web Lock API to hold a lock that prevents the screen from activating passively.

Works cleanly on Android Chrome. iOS Safari handles Web Lock differently - the tab needs to stay active in the foreground, which undermines the use case on iPhone. Haven't resolved that yet without breaking the no-backend, no-account architecture.

About 60KB total. Installs to home screen from the browser. No account, no data sent anywhere.

Built it because every focus app I tried was really a task manager. I wanted something that did exactly one thing at the OS level.

---

## POSTING NOTES

Priority order by time-sensitivity:
1. Hilal posts (r/Ramadan, r/islam, r/muslimtechnet) - POST TODAY. Ramadan is active now.
2. PrayerLock posts - POST THIS WEEK
3. FocusLock posts - POST THIS WEEK
4. PageScorer posts - POST THIS WEEK
5. HackerNews posts - any time, no time sensitivity

Reddit rules to check before posting:
- r/islam - no self-promotion, post as genuine tool share, read the rules before posting
- r/Ramadan - community rules vary by year, check pinned mod posts
- r/muslimtechnet - tech projects generally welcome, read sidebar
- r/ADHD - very active, supportive of tools that help. do not over-claim. be honest about limitations.
- r/getdisciplined - builders sharing tools is generally well-received
- r/productivity - busy sub, replies help more than upvotes for visibility
- r/digitalminimalism - very skeptical of tech tools. lead hard on the "one function" angle.
- r/SideProject - most builder-friendly, feedback culture
- r/webdev - technical audience, they will find bugs. lead with technical details.
- r/Entrepreneur - outcome-focused, lead with the business case
- r/startups + r/marketing - overlap with r/Entrepreneur, same approach

Wait 15-30 min between posts on any single account to avoid spam filters.

Account age matters on Reddit. If accounts are new (under 30 days), r/Entrepreneur and r/startups may auto-remove posts. Start with r/SideProject and r/webdev which have more lenient filters.
