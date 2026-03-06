---
subreddit: r/webdev
title: "offline-first web apps in 2026: the 3 patterns that actually work and the 2 that don't"
flair: Discussion
scheduled_date: 2026-03-18
---

I've been building offline-first PWAs for the past 2 months and ran into every caching pitfall you can imagine. here's what I learned so you don't have to.

**why offline-first matters more than you think:**

most web apps break completely when the network drops. even a 2-second blip during a subway ride can lose form data or show an error screen. offline-first inverts this: the app works by default, network is a bonus.

my use case: small utility apps (timers, trackers, calculators) that people use throughout the day, often in places with spotty connection.

**pattern 1: cache-first with network fallback (WORKS)**

serve everything from cache. only hit the network when cache misses. update the cache in the background for next load.

```javascript
self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request)
      .then(cached => cached || fetch(e.request)
        .then(response => {
          const clone = response.clone();
          caches.open('v1').then(c => c.put(e.request, clone));
          return response;
        })
      )
  );
});
```

pros: instant load, works offline, simple mental model.
cons: users might see stale content until background update finishes.

best for: apps where data doesn't change often (tools, references, calculators).

**pattern 2: IndexedDB for user data persistence (WORKS)**

localStorage has a 5MB limit and blocks the main thread. IndexedDB is async, handles larger datasets, and supports structured queries.

I use a thin wrapper (~40 lines) that provides get/set/delete/getAll operations. no library needed for simple use cases.

key insight: IndexedDB survives browser restarts but NOT "clear all site data." always warn users about this limitation.

real-world numbers: one of my apps stores 6 months of daily tracking data in IndexedDB. total storage used: ~200KB. well within browser limits.

**pattern 3: background sync for deferred actions (WORKS with caveats)**

user performs an action offline. app queues it in IndexedDB. when connection returns, service worker processes the queue.

the caveat: Background Sync API support is still Chrome/Edge only. Safari and Firefox need a workaround. I use a simple polling approach: check navigator.onLine every 30 seconds, process queue when true.

not elegant but it works on all browsers.

**pattern that DOESN'T work: aggressive precaching of everything**

I tried caching every asset, every route, every possible resource on first load. result: 8MB cache on a simple app. slow first load. wasted bandwidth for assets users never accessed.

better approach: cache the shell (HTML, CSS, critical JS) and lazy-cache everything else on demand.

**pattern that DOESN'T work: relying on the browser's HTTP cache**

HTTP cache is unreliable for offline scenarios. browsers evict cached resources under memory pressure. service worker caches are persistent and developer-controlled. always use service worker caches for offline-critical resources.

**the testing gap:**

Chrome DevTools has a good offline simulation mode. but it doesn't simulate the edge cases that break real apps:

- slow 2G connections (not the same as offline)
- connection that drops mid-request
- WiFi that connects but has no internet (captive portals)

I test by literally putting my phone in airplane mode, using the app for 5 minutes, then turning data back on. that catches more bugs than any simulation.

**resources that actually helped:**

- Jake Archibald's offline cookbook (still the best resource from 2016 and it holds up)
- web.dev PWA training course
- actually reading the service worker spec instead of tutorials

if you're building anything that people use on mobile, offline-first is worth the investment. the service worker pattern adds maybe 30 lines to your project and the user experience improvement is noticeable.

happy to share my service worker template or answer questions about specific offline patterns.
