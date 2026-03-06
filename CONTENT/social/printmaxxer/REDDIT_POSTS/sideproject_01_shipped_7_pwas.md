---
subreddit: r/SideProject
title: "I built 7 PWAs in 3 weeks as a solo dev. here's what actually worked and what was a waste of time."
flair: Show & Tell
scheduled_date: 2026-03-10
---

been lurking here for months. figured it was time to share what I actually shipped instead of just planning forever.

over the past 3 weeks I built and deployed 7 progressive web apps. all single-developer. all using the same base stack. none of them are making money yet, but all of them are live and installable.

here's the stack for every single one:

- vanilla HTML/CSS/JS (no frameworks)
- service worker for offline support
- manifest.json for installability
- hosted on surge.sh (free tier)
- total hosting cost: $0

the apps cover 3 niches: faith/spirituality, fitness tracking, and productivity tools. I picked these because they have clear daily-use patterns which matters for retention on PWAs.

what actually worked:

1. **single-file architecture** - each app is one HTML file with inline CSS and JS. sounds insane but it means zero build step, instant deploy, and the entire app loads in one request. largest app is 47KB.

2. **offline-first design** - service workers cache everything. users can use the app on a plane. this is the one feature that consistently surprises people during testing.

3. **installable from browser** - no app store review process. no $99/year developer account. user taps "add to home screen" and it looks native. icon on home screen, splash screen, fullscreen mode.

4. **template reuse** - after the first app, each subsequent app took about 40% less time because I built a boilerplate with the service worker registration, manifest template, and base styles.

what was a waste of time:

1. **overdesigning before building** - first app took 5 days. last app took 1.5 days. the difference was I stopped making Figma mockups and just built in-browser.

2. **worrying about the "right" framework** - vanilla JS works fine for single-purpose apps. I spent a week evaluating React vs Svelte vs Solid before realizing none of them were necessary for what I was building.

3. **analytics before users** - I integrated 3 different analytics tools before having a single user. should have shipped first, measured later.

biggest lesson: PWAs are genuinely underrated for side projects. zero distribution cost, works on every platform, no app store gatekeeping. the tradeoff is you lose push notifications on iOS (partially fixed now) and some native APIs.

happy to answer questions about the stack or the process. not trying to sell anything here, just sharing because the side project community helped me get started and I want to give back.
