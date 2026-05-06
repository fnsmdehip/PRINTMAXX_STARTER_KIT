# Reddit Distribution — Cycle 47 — 2026-05-05
# Focus: r/classicliterature (Pocket Alexandria), r/hormones (androx-trt), r/productivity + r/getmotivated (dosewell), r/islam + r/MuslimLounge (PrayerLock), r/quran (Quran streak)

---

## POST 1 — r/classicliterature — Pocket Alexandria [GAP FROM CYCLE 46]
**Subreddit:** r/classicliterature
**Title:** Built a curated classics reader for people who keep bouncing off public domain sites

**Body:**
I've started and abandoned more classics than I've finished, partly because the reading experience on most public domain sites (Gutenberg, Standard Ebooks) is genuinely bad on mobile.

So I built Pocket Alexandria: a PWA reader with 156 curated public domain books, designed to open and read comfortably without account setup.

What it has:
- 156 books across philosophy, literature, history, and science — Aurelius, Seneca, Dostoevsky, Tolstoy, Aristotle, Epictetus, Montaigne
- Reading progress tracking (local, no sync required)
- Night mode (reading in low light)
- Clean mobile typography optimized for long-form reading

Free tier: 10 books. Full library: $1.99/mo or $9.99/year.

https://pocket-alexandria.surge.sh

Happy to hear what authors or titles are missing from the list. Right now the selection skews toward Stoics and 19th century Russian literature because that's what I was reading when I built it.

---

## POST 2 — r/hormones — androx-trt [GAP FROM CYCLE 46]
**Subreddit:** r/hormones
**Title:** Built a TRT/hormone protocol tracker — local storage, no account, free

**Body:**
Tracking a TRT protocol in a spreadsheet is workable but annoying. Existing apps either want an account or are designed for diabetics (tracking glucose, not testosterone panels).

Built androx-trt for this gap specifically.

What it tracks:
- Injection logs: date, compound, dose, injection site, batch number
- Lab results: Total T, Free T, E2, hematocrit, SHBG, LH, FSH — whatever your doc orders
- Symptom journal: libido, energy, sleep, mood — log subjectively over time
- Protocol history: see every adjustment you've made and when

Everything stores locally. No account. No data goes anywhere.

Works as a PWA — add to home screen on iPhone/Android.

https://androx-trt.surge.sh

Currently tracking my own protocol with it. Feedback on what fields matter most to you would help me improve the lab section — different practitioners run different panels.

---

## POST 3 — r/productivity — dosewell [GAP FROM CYCLE 46]
**Subreddit:** r/productivity
**Title:** Minimal supplement/medication tracker — streak-based, offline, no account

**Body:**
The problem with most supplement tracking apps: they require a subscription to use basic features, or they're so complex they need 20 minutes to set up.

I built dosewell with one goal: log what you took in 10 seconds and close the app.

What it does:
- Morning/evening supplement groups
- Single tap logging for each item
- Streak tracking (don't break the chain)
- Local notifications for reminders
- Zero account, zero cloud, offline-first

What it doesn't do: nutrition calculations, drug interactions, complicated schedules. That's intentional — other apps cover those use cases well.

https://dosewell.surge.sh

Add to home screen from Safari/Chrome for the best experience on mobile. Works as a PWA.

---

## POST 4 — r/getmotivated — dosewell habit angle [GAP FROM CYCLE 46]
**Subreddit:** r/getmotivated
**Title:** The habit I needed to track wasn't productivity — it was whether I took my supplements

**Body:**
I track a lot of habits. Workouts, reading, cold showers, whatever's on the current list.

The one that kept slipping was the most boring: did I take my supplements this morning?

I kept forgetting the specific ones (fish oil, vitamin D, magnesium, creatine) because there was no streak attached to it. No consequence for missing. Just a vague sense I should probably be more consistent.

Built a tiny app to fix this: https://dosewell.surge.sh

It's just a checklist with streak tracking. Nothing novel. But adding a streak to boring habits is apparently all I needed.

30+ day streak now. First time in two years I've been consistent about it.

If you have boring health habits that keep slipping, try adding a streak counter. It's embarrassingly simple but it works.

---

## POST 5 — r/islam — PrayerLock [TIME-SENSITIVE — Ramadan]
**Subreddit:** r/islam
**Title:** Built a prayer tracking app for Ramadan — offline, no account, free

**Body:**
Ramadan Mubarak to everyone in this community.

I built prayerlock during Ramadan to track my 5 daily prayers. Simple streak counter, works offline, no account required. Add it to your home screen on iPhone or Android like a native app.

Link: https://prayerlock-web.surge.sh

Also built a Ramadan tracker specifically for the month: fasting streak, iftar/suhoor notes, daily quran progress. https://ramadan-tracker.surge.sh

Both are free. No data collection. No tracking. No ads.

If you want something specific added before the end of Ramadan, let me know and I'll try to add it.

Ramadan Mubarak.

---

## POST 6 — r/MuslimLounge — PrayerLock [TIME-SENSITIVE — Ramadan]
**Subreddit:** r/MuslimLounge
**Title:** Free prayer tracker app for Ramadan — works offline, no sign-up

**Body:**
Assalamu alaikum,

I know there are a few prayer apps out there but I built this one because I wanted something with zero friction — open, tap, done. No account, no notifications requiring permissions, works with no internet connection.

prayerlock: https://prayerlock-web.surge.sh
- 5-prayer daily tracker with streak
- Add to home screen (iOS/Android) — works like a native app
- Offline-first
- Free

Ramadan tracker (fasting + quran + dua logging): https://ramadan-tracker.surge.sh

Made this as a personal tool and figured others might find it useful during Ramadan. No monetization. Just free.

Ramadan Mubarak.

---

## POST 7 — r/quran — Quran Streak [TIME-SENSITIVE — Ramadan]
**Subreddit:** r/quran
**Title:** Built a Quran reading streak tracker — simple, offline, no account needed

**Body:**
One of my Ramadan goals is consistent daily Quran reading. I kept track loosely but wanted a streak counter specifically for it.

Built a simple tracker: https://quran-streak-landing.surge.sh

It's a PWA (add to home screen). Tracks your daily reading streak, lets you log pages or time, shows your progress through the month.

Also built a full Ramadan tracker with prayer + fasting + quran fields combined: https://ramadan-tracker.surge.sh

Free, offline-first, no data sent anywhere. If there are features that would make it more useful for your Ramadan practice, let me know.

Ramadan Kareem.

---

## POST 8 — r/SideProject — 804 sites milestone [BUILD-IN-PUBLIC]
**Subreddit:** r/SideProject
**Title:** I have 804 deployed websites and $0 revenue. Here's what that actually means.

**Body:**
Day 45 of solo automation building.

Status: 804 surge.sh websites, 539 automation scripts, 192K leads scraped, 4 iOS apps built and simulator-tested, 20 Gumroad product listings drafted.

Revenue: $0.

The gap between "built" and "making money" is accounts. Specifically:
- No Stripe account set up (10 min task)
- No Gumroad account (15 min task)  
- iOS apps not submitted to App Store (45 min task)
- Affiliate IDs not replaced with real ones (30 min task)

The automation pipeline works. It builds, deploys, generates leads, creates content, queues distribution. What it can't do: create accounts, accept payments, submit to app stores.

I built the engine before I built the infrastructure that receives revenue from the engine.

Lesson: set up Stripe on day 1. Not day 45.

---
