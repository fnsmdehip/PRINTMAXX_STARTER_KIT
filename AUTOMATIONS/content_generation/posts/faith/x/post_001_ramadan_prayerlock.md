# Post 001 — Ramadan PrayerLock

**Platform:** X (Twitter)
**Length:** Thread (4 tweets)
**Posted:** 2026-03-22
**Niche:** Faith

---

built prayerlock in 3 days. it's a prayer streak tracker + offline PWA for ramadan. 55kb. works with zero internet.

why it matters: ramadan started feb 28. 25 days left. millions of muslims tracking daily prayers. one broken streak = one person looking for a replacement.

the build was dumb simple:
- next.js pwa (built static)
- supabase for streaks (fallback to localstorage if offline)
- sunrise/sunset api for fajr times
- deploy to surge for free

cost: $0. revenue: waiting on stripe account.

the ramadan window closes may 25. if you're building anything faith-related, now is the moment. ramadan creates urgency. people will switch apps if yours works better.

currently live at prayerlock-web.surge.sh. no paid ads. just existing.
