# Cross-platform distribution content, 2026-03-09
# Status: PENDING_REVIEW
# Accounts: @PRINTMAXXER / general distribution
# Platforms: dev.to, LinkedIn, Indie Hackers, Quora
# Voice: PRINTMAXXER weighted aggregate (copy-style.md compliant)

---

## Pre-publish checklist (verified before save)

- [x] Zero em dashes
- [x] Zero banned AI vocabulary
- [x] No "It's not just X, it's Y" constructions
- [x] No vague attributions without links
- [x] No promotional adjectives
- [x] Sentence case headings
- [x] Direct statements (not hedged)
- [x] Consequence-first hooks
- [x] Exact numbers where possible
- [x] Would @pipelineabuser post this? Yes
- [x] First sentence delivers value
- [x] Passes lowercase lol energy test

---

---
# 1. DEV.TO ARTICLE
---

**Title:** Building 10 PWAs with Claude Code: what I learned

**Tags:** #webdev #pwa #javascript #productivity

**Cover image:** [surge deploy screenshot showing 267 deploys]

---

I shipped 10 PWAs in 30 days using Claude Code. total infrastructure cost: $0. here's the architecture breakdown and what I'd do differently.

---

## why PWA over native

app store fees are 30%. review times are 7-14 days. a PWA ships in minutes and runs on every device.

the tradeoff: no app store discovery. you own distribution completely. for solopreneur tools where you're driving traffic anyway, that's fine.

FocusLock, PrayerLock, and PageScorer are all PWAs. none of them required a developer account, a $99/year Apple fee, or a week waiting for review.

---

## the architecture I landed on

every app follows the same 4-file pattern:

```
app/
  index.html        # full app, single file
  manifest.json     # PWA metadata
  sw.js             # service worker
  icon-192.png      # minimum viable icon
```

that's it. no build step. no node_modules. no webpack config. the whole thing deploys with `surge` in under 10 seconds.

average bundle size across the 10 apps: 47KB. smallest is FocusLock at 23KB. largest is PageScorer at 61KB. all under 100KB, which means instant load on 3G.

---

## the manifest.json

this is where PWA installability comes from. without it, browsers won't offer the "add to home screen" prompt.

```json
{
  "name": "FocusLock",
  "short_name": "FocusLock",
  "description": "25-minute focus timer with site blocking",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0a0a0a",
  "theme_color": "#6366f1",
  "icons": [
    {
      "src": "icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

3 things that trip people up here:

1. `display: "standalone"` is what makes it feel like a native app. without this you get browser chrome.
2. `purpose: "any maskable"` on the 192 icon prevents Android from cropping your icon into a circle badly.
3. the `start_url` must be a path that actually resolves on your server. if you deploy to surge.sh with a subdomain, `/` is fine.

---

## service worker registration

the service worker is what gives you offline capability. for most of these apps, the offline story is simple: cache everything on install, serve from cache first.

register it in your HTML before the closing `</body>` tag:

```html
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
      .then(reg => console.log('SW registered:', reg.scope))
      .catch(err => console.log('SW failed:', err));
  }
</script>
```

and the service worker itself for a simple cache-first strategy:

```javascript
const CACHE_NAME = 'focuslock-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icon-192.png',
  '/icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      )
    )
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(cached => cached || fetch(event.request))
  );
});
```

that `self.skipWaiting()` call matters. without it, users who have the old version installed won't see updates until they close and reopen the app. for productivity apps where you're pushing bug fixes, that's annoying.

---

## how Claude Code handled this at scale

the pattern I found that worked: one master prompt per app type, then Claude handles all 4 files simultaneously.

for PrayerLock specifically, the prompt was about 400 words: described the prayer tracking behavior, the offline requirement, the color scheme, and the data model (local storage only, no server calls). Claude returned working code in 1 pass about 70% of the time. the remaining 30% needed 1-2 iterations on edge cases.

the biggest win: Claude generates consistent service worker patterns. i stopped writing service workers by hand after app 2.

---

## what broke

3 things failed repeatedly:

**1. iOS Safari and service workers.** iOS 16.4+ supports PWA install, but older versions don't register service workers at all. PrayerLock had to degrade gracefully, showing a banner that said "for offline use, open in Chrome" on older iOS.

**2. the manifest scope.** if you deploy to `myapp.surge.sh` and your manifest has `"scope": "/"`, it works. if you accidentally set `"scope": "/app/"` but your `start_url` is `/`, browsers reject the manifest silently. cost me 2 hours on PageScorer.

**3. icon dimensions.** lighthouse is strict. if your 512px icon isn't actually 512x512 (even by 1 pixel), you lose the installability audit. script now checks dimensions before deploy.

---

## the deploy pipeline

```bash
# deploy all apps
for app in focuslock prayerlock pagescorer; do
  cd apps/$app
  surge . $app-web.surge.sh
  cd ../..
done
```

267 deployments across 10 apps in 30 days. surge costs $0 on the free tier for static sites. the only cost is your time.

---

## what I'd do differently

offline-first from day 1, not as an afterthought. FocusLock shipped without proper offline support and had to be patched 3 times. PrayerLock was designed offline-first and has had 0 service worker issues.

also: build the manifest checker into the deploy script, not as a post-deploy audit. catching the icon dimension problem before deploy would have saved a combined 4 hours across 3 apps.

the PWA approach was the right call. $0 infrastructure, ships in minutes, works on every device. the distribution problem is real but that's a marketing problem, not a technical one.

---

---
# 2. LINKEDIN POST
---

**Title:** The $0 app factory

**Character count target:** 200-300 words

---

I built 10 apps this month.

infrastructure cost: $0.
app store fees: $0.
review time: 0 days.

the apps are PWAs (progressive web apps). they install on your home screen, work offline, and run on every device. no App Store. no Google Play. no 30% fee on every transaction.

267 deployments. surge.sh handles hosting for free on static sites. the only tool cost is Claude Code on the Max plan, which I was already paying for other work.

the apps: FocusLock (focus timer), PrayerLock (prayer tracker), PageScorer (page analysis), plus 7 others across productivity and wellness niches.

what I learned: the technical bar for a PWA is genuinely low. manifest.json, a service worker, one HTML file. average bundle size was 47KB. the whole pattern fits in 4 files.

the hard part is distribution. PWAs don't show up in app store search. you own distribution entirely. that means SEO, content, cold outreach, and community. none of which I've figured out yet since the apps shipped 30 days ago and revenue is $0.

but the infrastructure is in place. 10 apps across real niches, $0 carrying cost, ready to market.

if you're building solo: skip the app store. build a PWA. ship it on surge.sh. figure out distribution after you have something real.

what are you building?

---

---
# 3. INDIE HACKERS POST
---

**Title:** Month 1 update: 10 PWAs, 267 deploys, $0 revenue

**Format:** Honest update post

---

i'm going to be straight with you.

10 apps shipped. 267 total deployments. $0 revenue. one month in.

here's what actually happened.

---

**what went right**

shipping speed was genuinely fast. the PWA architecture (manifest + service worker + single HTML file) meant each app went from idea to deployed in 4-6 hours. FocusLock, PrayerLock, and PageScorer all deployed on the same day i decided to build them.

surge.sh is free for static sites. that's not a typo. i'm running 10 live apps with 0 infrastructure cost. the only recurring cost is Claude Code on the Max plan at $200/mo, which i'd be paying regardless.

the offline-first approach paid off. PrayerLock had 0 service worker issues because i designed it offline-first from the start. apps that weren't designed that way needed patches.

---

**what went wrong**

distribution. completely. 100%.

i spent 30 days building and 0 days on distribution. the apps exist. nobody knows they exist. i don't have Twitter accounts set up for most niches. i haven't submitted to any directories. i haven't done a single piece of outreach.

this is the classic indie hacker mistake and i made it anyway. build, build, build, ship to silence.

the secondary problem: no clear monetization before shipping. FocusLock is free with no paywall. i need to retrofit a $3/month subscription onto an app that people already expect to be free. that's a harder sell than launching paid from day 1.

---

**what's next**

directory submissions for all 10 apps this week.

setting up proper social accounts across the niches (productivity, faith, wellness) and starting to post about the apps.

adding a paywall to at least 3 apps before the end of this month. PrayerLock is the most obvious candidate: faith apps convert well on subscriptions.

i'm also looking for distribution partners. if you run a newsletter in productivity, faith, or wellness and want to feature a free tool, DM me. the apps are genuinely useful and completely free right now.

---

**the honest question**

i have working apps. the technical work is done. but i've never successfully cracked distribution as a solo builder.

specifically: for PWAs that aren't in app stores, what's your best distribution channel? directories? SEO? community posts? i'm starting from 0 followers on every relevant account.

apps if you want to try them:
- focuslock-web.surge.sh (focus timer)
- prayerlock-web.surge.sh (prayer tracker)
- pagescorer-web.surge.sh (page analysis tool)

feedback welcome. brutal honesty preferred.

---

---
# 4. QUORA ANSWER TEMPLATES
---

## Template A: "What are the best free productivity apps?"

**Answer:**

FocusLock is worth trying if you do focused work sessions.

it's a 25-minute focus timer that runs as a PWA, meaning it installs on your home screen and works offline. no App Store required. focuslock-web.surge.sh

the design is minimal on purpose: start timer, work for 25 minutes, take a break. it tracks your sessions locally so you can see how many focused hours you actually logged this week.

free. no login. no account. works on iOS and Android through the browser.

the other tools in the category worth knowing: Forest (app, freemium), Be Focused (iOS, free tier), and Toggl Track if you need time logging vs. just focus sessions. FocusLock is simpler than all of them, which is either a feature or a bug depending on what you need.

---

## Template B: "How do I build a PWA?"

**Answer:**

a PWA is 4 files. that's it.

here's the minimum viable setup:

**1. manifest.json** (tells browsers it's installable)

```json
{
  "name": "Your App Name",
  "short_name": "AppName",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
```

**2. sw.js** (service worker for offline support)

```javascript
const CACHE = 'app-v1';
const FILES = ['/', '/index.html', '/manifest.json'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(FILES))
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request))
  );
});
```

**3. register the service worker in your HTML**

```html
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js');
  }
</script>
```

**4. link the manifest in your `<head>`**

```html
<link rel="manifest" href="/manifest.json">
```

deploy to surge.sh (free) or Netlify (free). open in Chrome on mobile and you'll get the "add to home screen" prompt.

you can see a working example at focuslock-web.surge.sh. open source pattern, check the source in devtools.

the main gotcha: iOS Safari on older versions (pre-16.4) doesn't support PWA install. if your audience is heavy iOS, add a banner that says "open in Chrome for install." everything else works across all modern browsers.

---

## Template C: "What tools do solopreneurs use?"

**Answer:**

after 30 days of building solo, here's the actual stack (not the aspirational one):

for building: Claude Code on the Max plan ($200/mo). i built 10 apps with it in 30 days. it writes the service workers, the manifest files, and most of the UI. i write the product specs.

for hosting: surge.sh. free for static sites. `surge .` in the terminal and your app is live in 10 seconds. no config, no build pipeline required.

for page analysis: PageScorer (pagescorer-web.surge.sh). i built this myself because i wanted something that audits a page's copy and structure without 47 browser tabs open. runs as a PWA, works offline.

for focus: FocusLock (focuslock-web.surge.sh). 25-minute timer, session tracking, no ads.

for writing: Obsidian locally, no sync subscription. all notes in markdown on disk.

for email: Beehiiv free tier until a newsletter hits 2,500 subs.

the pattern: free or one-time-cost tools where possible. the only recurring spend that actually moves the needle is Claude Code. everything else is either free or cheap.

the tool stack matters less than people think. distribution matters more. but those are the actual tools.

---

# END OF CONTENT
# Status: PENDING_REVIEW
# Next action: Human review then post to each platform
# Estimated posting time: 45 minutes across all 4 platforms
