# HN + Product Hunt distribution, cycle 6
# Generated: 2026-03-07
# STATUS: PENDING_REVIEW (all posts)

---

## HACKER NEWS SHOW HN POSTS

---

### Show HN 1: SiteScore

**Title:** Show HN: SiteScore, a free website audit that runs entirely in your browser

**Body:**

I needed a fast way to check a site's performance and SEO basics before client calls. Every tool I found wanted my email, wanted to run on their servers, or took 2 minutes to return results.

So I built SiteScore. It runs 100% client-side. Your browser fetches the page, analyzes the DOM, and scores it on 5 dimensions: performance, SEO, accessibility, security headers, and mobile readiness. No backend. No data leaves your machine. Results in about 10 seconds.

The tradeoff: since there's no server component, I can't measure TTFB, server response times, or do multi-geography testing. Everything is based on what the DOM and network requests tell me from your browser. For a quick pre-call sanity check, that's enough. For a full audit, you still need Lighthouse or WebPageTest.

Built with vanilla JS. Total page weight is under 80KB. Works offline after first load.

https://sitescore-free.surge.sh

**First comment (maker's comment):**

Maker here. I'm an indie dev building small tools to support a consulting pipeline. The thesis: give away useful free tools, let them drive inbound leads for paid work.

The scoring algorithm weighs 23 checks across 5 categories. Some examples: missing meta descriptions, images without alt text, no HTTPS redirect, viewport not set, render-blocking scripts in the head. Each check has a weight based on how much it actually matters (missing H1 is weighted higher than missing Open Graph tags, for instance).

Honest limitations: cross-origin restrictions mean I can't analyze third-party script performance. The performance score is really a "front-end hygiene" score, not a true speed metric. I'm considering adding a small optional backend for the server-side checks, but the whole appeal is "no signup, no tracking, just paste a URL."

Source is messy but I'll clean it up and open source if there's interest. Ask me anything about the scoring weights or the client-side approach in the comments.

---

### Show HN 2: Streak Factory

**Title:** Show HN: I generated 28 habit-tracking PWAs from one HTML template

**Body:**

I built one HTML template for daily habit tracking. Then I used CSS variable injection and a build script to generate 28 niche-specific PWAs from it. Each one targets a different audience: Catholic daily prayer, Quran reading streaks, fitness tracking, coding practice, meditation, journaling, language learning, and about 20 more.

The technical approach is simple. One base HTML file. One service worker. One manifest template. A JSON config per app defines: app name, color scheme (CSS custom properties), streak labels, default habits, and icon. Build script reads the config, injects the variables, outputs a deployable PWA directory. Each app is under 60KB, works offline, and stores data in localStorage.

I wanted to test whether template-based app generation is a real distribution strategy or just a clever hack that goes nowhere. 28 apps gives me 28 chances to rank for niche long-tail keywords instead of competing in the "habit tracker" bloodbath with apps that have 10,000+ reviews.

No framework. No React. No build toolchain beyond a Python script that does string replacement. Each PWA passes Lighthouse PWA audit with 100.

https://printmaxx-apps.surge.sh

**First comment (maker's comment):**

Maker here. Some numbers on the approach:

- 1 template, 28 outputs. Adding a new niche takes about 15 minutes (write config JSON, pick colors, choose default habits).
- Each app: ~55KB total (HTML + CSS + JS + manifest + service worker). No external dependencies.
- localStorage persistence means zero server costs. The entire portfolio runs on free static hosting.
- 0 frameworks. The template is vanilla HTML/CSS/JS. Service worker handles offline caching.

The question I'm testing: in a world of 500 generic habit trackers, does "habit tracker for Lutherans" or "habit tracker for artists" actually convert better because the user feels like it was built for them? Even though under the hood it's the same app with different colors and labels.

The niche targeting is the product strategy, not the code. The code is intentionally boring.

Tradeoffs: localStorage means data doesn't sync across devices. No cloud backup. If you clear browser data, your streaks are gone. I could add optional sync but that adds complexity and hosting costs that kill the free model.

If anyone has experience with template-based app distribution, I'd be curious what worked and what didn't.

---

### Show HN 3: InvoiceForge

**Title:** Show HN: InvoiceForge, free invoice generator with zero data collection

**Body:**

I got tired of invoice tools that want you to create an account before generating a single PDF. InvoiceForge generates invoices client-side. Fill in the fields, hit generate, get a PDF. Nothing touches a server.

The PDF generation uses jsPDF. Your data stays in your browser tab. Close the tab and the data is gone (unless you save the PDF first, obviously). No cookies, no analytics, no tracking pixels.

It handles the basics: line items with quantity and rate, tax calculation, due dates, payment terms, your logo (loaded as base64 from a local file picker, never uploaded). The output looks professional enough for freelance work and small business invoicing.

What it doesn't do: recurring invoices, payment integration, client management, invoice tracking. If you need those, you need FreshBooks or Wave. This is for the "I need one invoice right now" use case.

https://invoiceforge-app.surge.sh

**First comment (maker's comment):**

Maker here. Built this because I send maybe 3-4 invoices a month and couldn't justify paying for invoicing software. Google Docs templates work but they're slow and formatting breaks constantly.

Technical details: jsPDF for PDF generation, vanilla JS for the form logic, CSS grid for the invoice layout preview. Total page weight is about 90KB including the jsPDF library. Works offline after first load thanks to a service worker.

One thing I learned: PDF generation in the browser is surprisingly annoying. Font rendering, line wrapping, and table alignment all behave differently than they do in CSS. I spent more time on the PDF output matching the on-screen preview than on any other part of the project.

The privacy angle is genuine, not a marketing gimmick. If you're invoicing clients, that data includes names, addresses, amounts, and bank details. I don't want that responsibility and you shouldn't have to trust a random free tool with it.

---

### Show HN 4: ColdMaxx

**Title:** Show HN: ColdMaxx, free cold email toolkit with a subject line scoring algorithm

**Body:**

ColdMaxx is a browser-based toolkit for cold email. The main feature is a subject line scorer that rates your subject line against patterns from open rate data. It checks length, word choice, personalization tokens, spam trigger words, and question vs. statement format.

The scoring is based on published cold email benchmarks (Woodpecker, Lemlist, and Hunter.io have all published open rate data by subject line characteristics). I aggregated the patterns into a weighted scoring model. It's not ML, it's a rule-based system with about 40 checks. Transparent and deterministic, so you can see exactly why your subject line scored the way it did.

Also includes: 12 cold email templates organized by use case (agency pitch, SaaS demo request, freelancer intro, partnership proposal), a deliverability checklist, and a spam word reference. All static content, no backend.

The thesis: I'm testing whether giving away a useful free tool generates consulting leads better than cold outreach itself. Using cold email tools to sell cold email services is the kind of recursion that either works great or is deeply ironic.

https://coldmaxx-app.surge.sh

**First comment (maker's comment):**

Maker here. The scoring algorithm breaks down like this:

- Length: 3-5 words score highest (35-45 char range based on Woodpecker data showing 36% avg open rate)
- Personalization: {{firstName}} or {{company}} tokens add points
- Spam triggers: "free," "guaranteed," "act now" etc. subtract points (list of ~80 words from spam filter databases)
- Question format: slight bonus (questions show 10-20% higher open rates in most benchmarks)
- All caps words: penalty
- RE:/FW: prefix: penalty (deceptive, hurts trust long-term even if it boosts initial opens)

The weights are tunable. I'm planning to add an A/B comparison mode where you paste two subject lines and it tells you which one should perform better and why.

Honest limitation: open rate benchmarks vary wildly by industry, list quality, and sending domain reputation. A "perfect" subject line means nothing if your domain is on a blacklist. The tool is useful for catching obvious mistakes, not for guaranteeing results.

---

## PRODUCT HUNT LAUNCH DRAFTS

---

### Launch 1: SiteScore

**Tagline:** Free website audit in 10 seconds. No signup needed.

**Description (260 chars):**
Paste any URL. Get scored on performance, SEO, accessibility, security, and mobile readiness. Runs in your browser. No account, no data collection, no backend. Built for quick checks before client calls. Under 80KB total.

**First comment from maker:**
Built this because every audit tool I tried wanted my email first. SiteScore runs entirely in your browser. Paste a URL, get a score across 5 dimensions in about 10 seconds. 23 individual checks with transparent weights. No server, no tracking, no cookies. Your data never leaves your machine. The tradeoff is I can't test server-side metrics like TTFB without a backend, but for a fast sanity check it does the job. Free, no strings.

**5 key features:**
1. 10-second audit across 5 categories (performance, SEO, accessibility, security, mobile)
2. 23 weighted checks with transparent scoring, you can see why you got each score
3. 100% client-side, no data transmitted, no account needed
4. Works offline after first visit (service worker cached)
5. Under 80KB total page weight, loads instantly on any connection

**Pricing:** Free

**Categories:** Developer Tools, Productivity, SEO

**STATUS:** PENDING_REVIEW

---

### Launch 2: The Streak Factory

**Tagline:** 28 habit-tracking apps. Pick your niche. Start today.

**Description (260 chars):**
One template, 28 niche habit trackers. Catholic, Buddhist, fitness, coding, meditation, journaling, and 22 more. Each app is a PWA under 60KB. Works offline. No account needed. Data stays on your device in localStorage.

**First comment from maker:**
I built one habit tracker template and generated 28 niche-specific apps from it. Instead of competing in the "habit tracker" category against apps with 50K reviews, each version targets a specific community: Catholic daily prayer, Quran reading, coding practice, art streaks, fitness logging. Under the hood it's the same app with different colors, labels, and default habits. Each one is under 60KB, works offline, and stores everything in localStorage. Zero server costs. The bet: people pick the app that feels like it was built for them, even if the code is identical.

**5 key features:**
1. 28 niche-specific habit trackers from one template (religious, health, creative, learning)
2. Each app is a PWA, works offline, installable on any device
3. Under 60KB per app, loads instantly, no framework bloat
4. Data stored in localStorage, never transmitted, no account needed
5. Add a new niche in 15 minutes (JSON config, color scheme, default habits)

**Pricing:** Free

**Categories:** Productivity, Health and Fitness

**STATUS:** PENDING_REVIEW

---

### Launch 3: PrayerLock

**Tagline:** Block distractions during prayer times. Free PWA.

**Description (260 chars):**
PrayerLock shows your next prayer time and blocks distracting apps during salah. Location-based prayer time calculation. Works offline. Free PWA, 55KB. Ramadan is March 1-30 this year, built this for the community.

**First comment from maker:**
Built PrayerLock because I saw Muslim friends manually setting Do Not Disturb 5 times a day. The app calculates prayer times based on your location, shows countdown to the next one, and activates a focus mode that blocks notifications during prayer. It's a 55KB PWA that works offline after first load. No account, no data collection. Prayer time calculation uses standard astronomical formulas (angle-based methods, supports multiple calculation conventions used in different regions). Ramadan started March 1st and runs through the 30th. Over a billion people are fasting and praying extra this month. If this helps even a few hundred people stay focused during salah, it was worth building. Free, no ads, no premium tier.

**5 key features:**
1. Automatic prayer time calculation based on your location (supports multiple calculation methods)
2. Focus mode blocks distractions during prayer windows
3. Countdown timer to next prayer with notification alerts
4. 55KB PWA, works offline, installable on any phone
5. Free with no ads, no account needed, no data collection

**Pricing:** Free

**Categories:** Productivity, Health and Fitness

**STATUS:** PENDING_REVIEW

---

## Distribution notes

- HN posts: submit between 8-10am ET on weekday mornings for best visibility
- HN: space posts 3-5 days apart, don't submit multiple in the same day
- HN: SiteScore and InvoiceForge are strongest candidates (HN loves privacy-first tools)
- HN: Streak Factory has the most interesting technical discussion angle (template-based generation)
- PH: launch Tuesday-Thursday for best traffic, avoid Fridays and weekends
- PH: PrayerLock is time-sensitive (Ramadan ends ~March 30), launch within 5 days
- PH: ask 5-10 people to upvote and leave genuine comments within first hour
- Cross-post HN links to relevant Twitter threads for compound distribution
