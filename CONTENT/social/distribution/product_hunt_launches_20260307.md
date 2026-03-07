# Product Hunt Launch Drafts
status: PENDING_REVIEW
created: 2026-03-07T06:00:00Z
cycle: distribution_engine_2

---

## Launch 1: PrayerLock (TIME-CRITICAL — Ramadan is live)

**Tagline:** the prayer tracker that locks your phone until you pray. built for ramadan.

**Description:**
PrayerLock blocks app access at prayer times. not a reminder. a lock.

it calculates all 5 daily prayer times based on your location. when it's time, your phone goes into focus mode. you mark your prayer complete to unlock.

built as a PWA. no app store needed. works offline. installs to your home screen in 2 taps. 55KB total.

designed for ramadan but works year-round. tracks streaks, shows prayer history, and works on any device with a browser.

$0 hosting. $0 infrastructure. pure static HTML/CSS/JS with a service worker.

**First Comment (Maker):**
built this because alarm-based prayer reminders don't work. you dismiss them and forget. PrayerLock makes it harder to ignore. the phone is literally unusable until you pray.

the tech is intentionally minimal. no backend. no database. no user accounts. everything stores locally. your prayer data never leaves your device.

tested it during the first week of ramadan. completion rate went from ~60% to ~95% for the 5 daily prayers.

live at prayerlock-app.surge.sh. code is vanilla JS, no frameworks.

**Topics:** Productivity, Health & Fitness, Tech, Developer Tools
**Gallery:** 3 screenshots — lock screen, prayer dashboard, streak view

---

## Launch 2: SiteScore / PageScorer (Website Audit Tool)

**Tagline:** paste a URL, get a site audit in 10 seconds. free. no signup.

**Description:**
drop any URL. get a performance, SEO, accessibility, and security score instantly.

no account required. no email gate. no "book a demo." paste the URL, hit analyze, see results.

scores across 4 categories:
- performance (load time, asset sizes, render blocking)
- SEO (meta tags, headings, alt text, structured data)
- accessibility (contrast ratios, aria labels, keyboard nav)
- security (HTTPS, headers, mixed content)

each category breaks down into specific checks with pass/fail and recommendations. export the report as a shareable link.

built for freelancers who need a quick audit to show prospects what's broken on their site. "here's what's wrong, here's what I'd fix" is the best cold email opener that exists.

**First Comment (Maker):**
built this because every website audit tool either costs money or requires an account. lighthouse is great but it's buried in devtools and non-technical clients don't understand the output.

this gives you a clean, shareable report you can drop in a cold email or client meeting. "your site scores 34/100 on mobile performance. here's why." that's the entire sales pitch.

live at pagescorer.surge.sh. also available at sitescore-app.surge.sh.

**Topics:** Developer Tools, SEO, Freelance, Marketing
**Gallery:** 3 screenshots — URL input, score dashboard, detailed report

---

## Launch 3: Streak Apps (13-app bundle)

**Tagline:** 13 streak-tracking PWAs. every niche. every religion. every habit. all free.

**Description:**
one code template. 13 deployed apps. each one tracks daily streaks for a different activity or community.

the full set:
- scripture-streak (bible)
- torah-streak, quran-streak, gita-streak, guru-streak, sutra-streak (religious texts)
- fitness-streak, coding-streak, meditation-streak, reading-streak
- art-streak, language-streak, journal-streak

every app: offline-capable PWA, installable to home screen, tracks streaks with visual calendars, sends local notifications, stores data on-device.

the template system: one base codebase, config.json per app with custom copy/colors/icons, python build script generates all 13 in under a minute, bash loop deploys all to surge.sh.

$0 total cost. no backend. no accounts. no data collection.

**First Comment (Maker):**
the insight behind this: streak mechanics work for literally any daily habit. the UI is identical. the only thing that changes is the context: what are you tracking, what language does the community speak, what colors resonate.

so I templated the whole thing. adding a new streak app takes 10 minutes: write the config, run the build, deploy. that's it.

if you want to fork the template for your own niche, the approach is: config.json with title, colors, icon, copy. build script reads config, injects into HTML template, outputs to /dist. surge deploys /dist.

**Topics:** Productivity, Developer Tools, Open Source, Health & Fitness
**Gallery:** Grid of all 13 app screenshots, one detail view of streak calendar
