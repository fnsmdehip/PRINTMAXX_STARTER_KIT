---
subreddit: r/webdev
title: "single-file PWAs: why I stopped using frameworks for small web apps and went back to vanilla HTML"
flair: Discussion
scheduled_date: 2026-03-13
---

I want to share an approach I've been using that goes against current best practices but has been working really well for a specific use case.

**the approach: one HTML file = one complete app.**

inline CSS. inline JS. service worker registered from the same origin. manifest.json as the only separate file. total file count per app: 3 (index.html, sw.js, manifest.json).

**why:**

I build small, single-purpose tools. a prayer time calculator. a workout interval timer. a daily focus tracker. these apps do one thing. they don't need routing. they don't need state management libraries. they don't need a build step.

**the performance numbers speak for themselves:**

| metric | framework approach | single-file approach |
|--------|-------------------|---------------------|
| total bundle | 180KB+ (React minimal) | 23-47KB |
| time to interactive | 1.8s (3G) | 0.4s (3G) |
| lighthouse perf | 82-91 | 98-100 |
| build time | 12-30s | 0s (no build step) |
| deploy time | 45s (with CI) | 2s (surge ./dist) |

**the service worker pattern I use:**

```javascript
// sw.js - total: 28 lines
const CACHE = 'app-v1';
const ASSETS = ['/', '/index.html', '/manifest.json'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request))
  );
});
```

cache-first strategy. entire app available offline after first load. no workbox, no service worker library. 28 lines.

**where this approach fails:**

- multi-page apps with complex routing: use a framework
- apps with shared state across components: use a framework
- team projects where multiple devs touch the same code: use a framework
- apps that need server-side rendering for SEO: use Next/Nuxt/etc

this is specifically for small, client-side, single-purpose tools where the total JS is under ~5KB.

**the installability factor:**

adding manifest.json makes these installable as PWAs. users tap "add to home screen" and get:
- app icon on home screen
- splash screen on launch
- runs in standalone mode (no browser chrome)
- works offline

for the user, it feels native. for me, it took 15 minutes to add to an existing web page.

**development workflow:**

1. write HTML in VS Code
2. open in browser with live server extension
3. test on phone via local network IP
4. deploy with `surge ./` (2 seconds)
5. test installability on phone
6. done

no `npm install`. no webpack config. no dependency updates. no node_modules folder taking 847MB.

I've shipped 7 apps this way. the approach won't scale to complex applications but for the "I need a small tool that works everywhere" use case, it's hard to beat.

curious if anyone else has gone back to vanilla for small projects or if I'm an outlier here. also open to criticism of this approach because I know it has limitations I might be blind to.
