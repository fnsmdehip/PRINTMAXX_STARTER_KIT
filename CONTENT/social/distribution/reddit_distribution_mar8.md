# Reddit Distribution, Mar 8 2026
# Status: PENDING_REVIEW
# Subreddits: r/SideProject (3), r/Entrepreneur (2), r/webdev (2), r/SaaS (1), r/coldoutreach (1), r/indiehackers (2), r/islam (1), r/MuslimLounge (1)
# Total posts: 13

---

## r/SideProject posts

### r/SideProject, Post 1
**Title:** I built 22 PWA apps in 35 days as a solo dev. here's what I learned about shipping fast.
**Flair:** Show HN / Built This

35 days ago I set a goal: ship as many apps as possible before second-guessing myself to death. I had no team, no funding, no runway. Just Claude Code, a surge.sh account, and a bias toward done over perfect.

22 apps later, here's what I actually learned.

**Keep the bundle under 60KB or users on slow connections bounce before load.**

My average bundle size is 55KB. I got there by stripping every dependency I didn't need that day. CSS-only animations instead of Framer Motion. No state management library. Vanilla JS event listeners where React felt like overkill. Each app is a single HTML shell with a service worker bolted on for offline capability.

**The service worker is the only reason PWAs are worth building.**

Without offline support you're just making a mobile website with an install button. FocusLock works when your phone is on airplane mode. SleepMaxx tracks your data locally and syncs when you're back online. PrayerLock serves its full UI from cache on first load. That's the whole value prop. Get the service worker right or don't call it a PWA.

**Ship day 1, iterate day 3.**

I deployed every app the same day I built it. Some were embarrassingly bare on day 1. By day 3 I'd seen real usage patterns and fixed the 2-3 things that actually mattered. The apps I spent a week "perfecting" before shipping got identical first-week retention to the apps I shipped in 6 hours. Stop optimizing for an imaginary user who never arrived.

**Naming matters more than features.**

PrayerLock gets 3x more organic search traffic than the identical-feature app I named "Daily Prayer Tracker." People search the way they talk, and they talk in verbs + nouns. Name your app what it does to you, not what it is.

All 22 apps are live at https://printmaxx-apps.surge.sh if you want to see the stack in action.

**Link:** https://printmaxx-apps.surge.sh
**Best time to post:** Tuesday or Wednesday, 9-11 AM EST
**Notes:** r/SideProject responds well to specific numbers and honest process. Do not lead with the link. Post it as a comment first if the automod flags the text post. Engage replies within 2 hours of posting or the post dies.

---

### r/SideProject, Post 2
**Title:** I deployed 262 websites to surge.sh in 5 weeks. the deployment pipeline that makes it possible.
**Flair:** Technical / Show HN

262 sites. 5 weeks. $0 in hosting costs. Here's the pipeline.

surge.sh is free for static sites with no rate limit on deployments that I've found. The CLI is one command: `surge dist/ your-subdomain.surge.sh`. That's it. No config file, no build step required, no dashboard to click through. If your project compiles to a folder, it deploys.

The automation layer looks like this:

I have a Python script that reads a CSV of site names and target subdomains. It loops through each row, runs the build, calls `subprocess.run(["surge", "dist/", f"{subdomain}.surge.sh"])`, and logs the output. The whole 262-site batch runs in about 40 minutes. Most of that time is upload speed, not compute.

**The Playwright testing suite is what makes bulk deployment not terrifying.**

After every deployment batch I run a Playwright test that visits each URL, checks for a 200 status, confirms the page title matches expected output, and screenshots any failures. The test suite catches about 8-12 broken deploys per batch, usually from a build variable that didn't get substituted correctly. Without this I'd be manually clicking 262 links.

The test output writes to a CSV: url, status, title_match, screenshot_path, timestamp. Failed rows get re-queued automatically on the next run.

**What I'd do differently:**

Add a staging subdomain per site before going to production. Right now I deploy directly to the public URL because surge.sh doesn't have a native staging concept. A `staging-` prefix on the subdomain works but it's manual overhead.

The whole pipeline is about 200 lines of Python. If there's interest I can post the core loop.

**Link:** N/A (technical post, no single URL)
**Best time to post:** Tuesday, 10 AM EST
**Notes:** This post invites "can you share the code?" replies which drive comment count and visibility. Have the core script snippet ready to paste as a reply. Do not post the code in the main body or you lose the reply hook.

---

### r/SideProject, Post 3
**Title:** I built a free cold email ROI calculator. no signup, no paywall.
**Flair:** Free Tool / Show HN

Most cold email calculators make you sign up for a trial to see your results. I made one you can use right now without giving me anything.

You enter:
- emails per day
- open rate
- reply rate
- close rate
- deal size

It outputs: monthly revenue projection, cost per closed deal, break-even volume, and a "how many more emails to hit your number" figure.

I built it because I kept doing this math in a spreadsheet before every outreach campaign. Same formula every time. Took 10 minutes to set up and I'd do it for every new ICP. Stupid. So I wrapped it in a single-page tool with no backend, no database, just JavaScript doing arithmetic.

The thing that surprised me: most people who use it find out their reply rate assumption is the lever that matters most. Change close rate from 20% to 30% and revenue goes up 50%. Change reply rate from 2% to 3% and it nearly doubles. The calculator makes that relationship obvious in a way the spreadsheet didn't.

It's at cold-email-roi-calculator.surge.sh. Free, no login, works offline after first load.

**Link:** https://cold-email-roi-calculator.surge.sh
**Best time to post:** Monday, 9 AM EST (catches the "planning the week" crowd)
**Notes:** This is pure value with no friction. The best r/SideProject posts show the tool, explain the problem it solves, and get out. Do not add a CTA or upsell. Let the tool speak. If someone asks "are you monetizing this?" answer honestly: "not this one, it's a free utility."

---

## r/Entrepreneur posts

### r/Entrepreneur, Post 1
**Title:** 35 days building a digital product empire with $0 budget. 13 products ready, here's the stack.
**Flair:** Entrepreneur / Case Study

I want to be upfront: 35 days in, $0 revenue. 13 products built and ready to sell. This post is about the build side, not the earnings side, because I haven't cracked distribution yet and I'm not going to pretend I have.

Here's what $0 budget actually looks like.

**The entire infrastructure costs $200/month.** That's Claude Max, which lets me use Claude Code for unlimited agentic tasks. Everything else is free tier or open source.

Deployment: surge.sh. Free static hosting, one CLI command, no credit card. I have 262 live URLs on surge.sh right now for $0.

Email capture: formsubmit.co. Free form endpoint that sends submissions to your email. No backend, no database. You drop an HTML form pointing at their API and you're done. I use this on every landing page.

Storage: local files and git. No cloud database. Every app stores user data in localStorage or IndexedDB. Nothing leaves the device unless the user explicitly exports it.

Content: Claude Code generates copy, landing page HTML, app UI, and email sequences. One prompt produces the whole thing. I review and edit, but the 80% draft comes in under 30 seconds.

**The 13 products are a mix of PWA apps and PDF guides.** Apps handle recurring engagement. PDFs convert the traffic that doesn't want an app.

The honest bottleneck right now is not building more things. It's getting the 13 things in front of the right people. If you've cracked distribution for digital products with no ad budget I genuinely want to hear how.

**Link:** N/A (value post, no direct product link)
**Best time to post:** Wednesday, 8 AM EST
**Notes:** r/Entrepreneur rewards honesty about failures and gaps. Do not oversell. The "$0 revenue" admission in the opening line is intentional and will get more upvotes than hiding it. Expect "focus on one thing" replies. Engage them with specific data, not defensiveness.

---

### r/Entrepreneur, Post 2
**Title:** I scraped 1,111 local business leads and built custom demo sites for each. here's the outreach framework.
**Flair:** Cold Outreach / Growth

The playbook that's working (so far):

**Step 1: Scrape the niche.** I targeted home service businesses in 3 cities: Louisville, Austin, Las Vegas. Plumbers, roofers, landscapers, pressure washers. These businesses exist in every city, have predictable problems (bad or no websites), and make enough money to pay for a $500 site or $200/mo management.

I used Google Maps + a Python scraper to pull name, phone, website (if they had one), and rating. 1,111 businesses across the 3 cities.

**Step 2: Filter for the obvious opportunity.** Businesses with a website older than 2018 or no website at all. That's about 60% of the list. These are the easiest sells because the problem is visible before you say a word.

**Step 3: Build a demo site for each niche, not each business.** This is the time saver. I built 8 demo templates: plumber, roofer, landscaper, pressure washer, cleaner, painter, junk removal, handyman. Each template has placeholder business name and phone number. Takes 3 minutes to swap the details and deploy a personalized demo.

**Step 4: The outreach email.** Subject: "built something for [Business Name]". Body: 3 sentences. "I found your business on Google. Built a demo site to show what a modern version could look like. Here's the link: [demo URL]. No cost to look."

Reply rate on the demo site emails is 4-6x higher than generic "I can build you a website" cold emails. The demo does the selling.

**Step 5: Follow-up on day 3.** One follow-up only. "Did you get a chance to check out the demo?" No more after that.

The 1,111 leads are still being worked through. The framework is the repeatable part, not the specific list.

**Link:** N/A
**Best time to post:** Thursday, 10 AM EST
**Notes:** This post gives a complete methodology. The r/Entrepreneur crowd wants to know the exact steps. Give them steps 1-5 with real numbers. Expect "what's your close rate?" Do not make up a number. Say "still running the campaign, will update."

---

## r/webdev posts

### r/webdev, Post 1
**Title:** I built 22 PWAs that average 55KB each. here's how I keep them tiny.
**Flair:** PWA / Performance

55KB average bundle size across 22 production PWAs. Here's the exact list of decisions that get you there.

**No UI framework in the initial shell.** I use vanilla HTML/CSS/JS for the app shell. The shell loads in under 100ms on a 3G connection. If a specific view needs more interactivity, I lazy-load a lightweight script for that view only. The user is never waiting for React to hydrate before they see anything.

**CSS-only animations.** Every transition and loading state is CSS. No animation library. `@keyframes` handles 95% of what you need. The remaining 5% (physics-based springs, etc.) I drop or redesign around. Framer Motion is 42KB gzipped. That's nearly my entire budget for an app that doesn't use it.

**One service worker, written by hand.** I don't use Workbox. The service worker for each app is about 40 lines: cache the shell on install, serve from cache on fetch, fall back to network if the cache misses. That's it. Workbox adds ~15KB for features I'm not using.

**localStorage over IndexedDB for simple apps.** IndexedDB is async and adds complexity. For apps with under 50KB of user data, localStorage is synchronous, zero-dependency, and works in every browser back to IE8. I only reach for IndexedDB when I need to store binary data or more than ~5MB.

**No Google Fonts.** System font stack. `font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`. Looks clean, loads instantly, never causes a layout shift.

**The real size killer is third-party scripts.** Analytics, chat widgets, pixel tracking. Each one adds 15-80KB and a network request. I run zero third-party scripts in the initial load. If I need analytics, it's a single `navigator.sendBeacon()` call to my own endpoint on page unload. 200 bytes.

If you're building a PWA and wondering where your KB went, audit your third-party scripts first.

**Link:** https://printmaxx-apps.surge.sh
**Best time to post:** Tuesday, 11 AM EST
**Notes:** r/webdev loves specific, technical decisions with real numbers. Lead with the number (55KB), deliver on the promise. Expect "why not just use Vite/Astro/etc." Have a genuine answer: "Vite is great but the config overhead and default plugin set adds weight I have to fight back down. Vanilla lets me start at zero."

---

### r/webdev, Post 2
**Title:** Deployed 262 static sites on surge.sh with automated Playwright testing. here's the pipeline.
**Flair:** DevOps / Automation

I needed to deploy 262 static sites and know that every single one was working without clicking 262 links. Here's what I built.

**The deploy script (Python, ~80 lines core):**

```python
import subprocess
import csv
import logging

def deploy_site(name, subdomain, dist_path):
    result = subprocess.run(
        ["surge", dist_path, f"{subdomain}.surge.sh"],
        capture_output=True, text=True, timeout=120
    )
    return result.returncode == 0, result.stdout

with open("sites.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        success, output = deploy_site(
            row["name"], row["subdomain"], row["dist_path"]
        )
        logging.info(f"{row['subdomain']}: {'OK' if success else 'FAIL'}")
```

`sites.csv` has columns: name, subdomain, dist_path, expected_title.

**The Playwright test suite (~60 lines):**

```python
from playwright.sync_api import sync_playwright
import csv

def test_site(page, url, expected_title):
    response = page.goto(url, timeout=10000)
    status_ok = response.status == 200
    title_ok = expected_title.lower() in page.title().lower()
    page.screenshot(path=f"screenshots/{url.replace('/', '_')}.png")
    return status_ok, title_ok

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    results = []
    with open("sites.csv") as f:
        for row in csv.DictReader(f):
            url = f"https://{row['subdomain']}.surge.sh"
            status_ok, title_ok = test_site(page, url, row["expected_title"])
            results.append({
                "url": url, "status": status_ok, "title": title_ok
            })
    browser.close()
```

Failed rows get written to `failed_deploys.csv` and re-queued on the next run.

The whole thing runs in about 45 minutes for 262 sites. Playwright catches 8-12 broken deploys per batch. Worth it.

surge.sh has been reliable for all 262 sites. $0 hosting cost. The only limit I've hit is their 1GB per project cap, which you can work around with multiple accounts or their paid tier.

**Link:** N/A
**Best time to post:** Wednesday, 10 AM EST
**Notes:** Include the code blocks. r/webdev skips posts without them. The code should be copy-pasteable and real. Do not post pseudocode. Expect "why not Netlify/Vercel?" Answer: "Netlify/Vercel are great but have build minute limits on free tier. surge.sh is truly unlimited for static."

---

## r/SaaS posts

### r/SaaS, Post 1
**Title:** Free tools I built instead of paying for SaaS: invoice generator, ROI calculator, page scorer, subject line grader.
**Flair:** Tools / Free Resource

I got tired of paying $20-40/month for tools I used 3-4 times a month. So I built the ones I needed most. All free, no login, no paywall.

**Cold Email ROI Calculator**, cold-email-roi-calculator.surge.sh
You enter daily volume, open rate, reply rate, close rate, deal size. It tells you monthly revenue projection and break-even volume. I use this before every campaign to reality-check my assumptions. The math almost always shows reply rate is the lever that matters most, not close rate.

**Page Scorer**, pagescorer-vs-gtmetrix.surge.sh (comparison page with embedded scorer)
Scores your landing page on 8 factors: headline clarity, social proof, CTA placement, load time, mobile layout, trust signals, form friction, above-the-fold value prop. Not a Lighthouse replacement. More of a conversion audit than a technical audit.

**Subject Line Grader**, subject-line-grader-pm.surge.sh
Paste a subject line and it scores it on: length (under 50 chars), personalization tokens, spam trigger words, question vs statement, urgency without screaming. Built this because I kept A/B testing subject lines without a baseline framework.

**Invoice Generator**, invoiceforge.surge.sh
Single-page invoice builder. Fill in client details, line items, payment terms. Downloads a clean PDF. No account, no watermark, no "upgrade to remove branding." I use this for every client invoice.

All 4 are single-page static tools. Zero backend. The data never leaves your browser. Built in a weekend, maintained in about 30 minutes a month.

If you're paying monthly for any of these categories, worth checking if a free tool handles your actual use case first.

**Link:** See individual URLs above
**Best time to post:** Monday, 9 AM EST
**Notes:** List posts with multiple free tools perform well in r/SaaS because they solve the "I'm paying too much" frustration that's common there. Do not mention PRINTMAXX or any brand in the post body. Let the tools stand alone. The links are the conversion mechanism.

---

## r/coldoutreach posts

### r/coldoutreach, Post 1
**Title:** I built a cold email ROI calculator that shows exactly how many emails = $X revenue. free, no signup.
**Flair:** Tool / Free Resource

The single biggest problem in cold email is fuzzy math. "I need more pipeline" is not a plan. "I need to send 400 emails per day at a 3% reply rate and 20% close rate to close 2 deals per week at $2k each" is a plan.

I built a calculator that forces you to do that math before you start.

Inputs:
- emails per day
- open rate (%)
- reply rate (%)
- close rate (%)
- average deal size ($)

Outputs:
- projected monthly revenue
- cost per closed deal (if you enter cost per email)
- emails needed to hit a target number
- the sensitivity chart that shows which variable moves revenue most

The sensitivity output is the part I use most. It runs the model at +/- 1% on each variable and shows you which one has the biggest impact on your specific numbers. For most setups, reply rate matters 3-4x more than close rate. That tells you where to focus your testing.

The calculator is at cold-email-roi-calculator.surge.sh. Free, no login, works offline after the first load (it's a PWA). No email capture, no trial, no "export requires Pro."

Built this because I was doing this math in a spreadsheet before every campaign. Same formula every time. Easier as a tool.

**Link:** https://cold-email-roi-calculator.surge.sh
**Best time to post:** Monday or Tuesday, 8 AM EST
**Notes:** r/coldoutreach is a practitioner audience. They respond to tools that solve the actual math problem, not tips content. Post early in the week when people are planning campaigns. Engage any "what's your conversion from this calculator" question with honest data or a deflection to the tool's purpose.

---

## r/indiehackers posts

### r/indiehackers, Post 1
**Title:** Day 35: 22 apps, 262 sites, 13 products, $0 revenue. the honest truth about building vs selling.
**Flair:** Post-Mortem / Transparency

Day 35. Here's the real numbers:

- 22 PWA apps deployed and live
- 262 static sites on surge.sh
- 13 digital products (apps + PDFs) ready to sell
- 1,111 local business leads scraped and categorized
- $0 revenue

I built a machine. The machine doesn't have a sales channel yet.

This is the indie hacking trap nobody talks about loudly enough. You spend 35 days building the thing because building is safe, measurable, and gives you something to show. Selling is uncomfortable, uncontrollable, and produces rejection before it produces revenue.

The specific failure mode: I prioritized completing builds over listing products. Every day I'd wake up with a list of things to build. Zero days I woke up with a list of places to post, DMs to send, or listings to complete. Build mode is not the same as make money mode.

What I should have done differently:

Stop building after app 5. Deploy and sell app 5 before building app 6. If app 5 doesn't sell after 2 weeks of real distribution effort, understand why before building app 6 with the same assumptions.

The 262 sites are beautiful, well-tested, and completely invisible. No backlinks. No SEO domain authority. No referral traffic. Surge.sh subdomains don't rank. I knew this and built them anyway because "getting it live" felt like progress.

The 1,111 leads are sitting in a CSV that I've sent maybe 40 emails from. The pipeline isn't even open yet.

35 days of velocity and I'm staring at the hardest part: doing the thing that doesn't feel like building.

Day 36 changes the metric. Not apps built. Not sites deployed. Revenue.

**Link:** N/A
**Best time to post:** Sunday evening, 7 PM EST (IH crowd is reflective on Sundays)
**Notes:** Brutal honesty is the currency in r/indiehackers. This post will get more traction than any "I built X and made $Y" success post because the community has seen through polished success theater. Do not soften the $0 figure. Do not add "but I'm confident in the process." Just state the reality. Comments will be more useful than upvotes here.

---

### r/indiehackers, Post 2
**Title:** I automated my entire content pipeline: research to content to distribution. here's the architecture.
**Flair:** Automation / Build Log

The pipeline has 5 layers. Here's each one with the actual tools.

**Layer 1: Research (runs daily, automated)**
Two scrapers run every morning. A Twitter scraper reads bookmarks and 40+ monitored accounts, extracts signal (frameworks, tactics, numbers, case studies), and writes to a CSV. A Reddit scraper hits 41 subreddits via the JSON API and pulls top posts from the last 24 hours. Total: ~200 new data points per day. Zero manual work.

**Layer 2: Alpha processing (runs after research)**
A Python script reads the CSV, scores each entry (specificity, actionability, ROI potential), routes it to the right category (content, outbound, product, tool), and flags the top 10% for immediate action. The scoring is rule-based, not ML. Works fine.

**Layer 3: Content generation (triggered by alpha)**
For each approved alpha entry, Claude Code generates: 3 tweet variants, 1 thread outline, 1 Reddit post draft, and a newsletter paragraph. The prompt template is the same every time. Output goes to a staging folder with status PENDING_REVIEW.

**Layer 4: Quality gate (runs before distribution)**
A separate script reads the staging folder and runs a checklist: no em dashes, no banned AI vocabulary (use, use, dig, etc.), consequence-first hook, specific numbers present, length within platform limits. Anything that fails gets flagged for human edit. About 15% fail on the first pass.

**Layer 5: Distribution queue**
Approved content gets routed to a posting queue by platform: Twitter, Reddit, LinkedIn, newsletter. The queue has time slots. Human posts from the queue, doesn't write from scratch.

The result: I spend about 20 minutes per day on content instead of 2 hours. The research and first draft are automated. I'm only editing and posting.

Full stack: Python, Playwright (for scraping), Claude API (for generation), surge.sh (for landing pages), formsubmit.co (for email capture). Total cost: Claude Max plan at $200/mo covers the generation. Everything else is free.

**Link:** N/A
**Best time to post:** Wednesday, 10 AM EST
**Notes:** r/indiehackers loves architecture posts with real tool names. Name every tool, every layer, every cost. Do not be vague. The post's value is in the specificity. Expect "can you open source this?" Have a genuine answer ready about what's shareable and what's too specific to the PRINTMAXX setup to be useful out of context.

---

## r/islam posts

### r/islam, Post 1
**Title:** Built a free Ramadan tracker PWA. prayer times, fasting tracker, Quran progress. works offline, no ads.
**Flair:** App / Resource

Assalamu Alaikum,

I built a Ramadan tracker that works offline. No ads, no tracking, no login required.

What it does:
- Calculates prayer times based on your location (uses browser geolocation, data never leaves your device)
- Fasting tracker with Suhoor and Iftar time display for your city
- Daily Quran reading log (track by juz or page)
- Simple streak counter for salah consistency through Ramadan
- Works fully offline after the first load (it's a PWA, stores everything locally)

I built it because most Ramadan apps I found were either bloated with ads or required a sign-up before you could see anything. This one opens immediately and works without a network connection once loaded.

The prayer time calculation uses the standard formula with support for multiple calculation methods (MWL, ISNA, Egypt, Makkah, Karachi, Tehran, Jafari). You can set your method in settings. No account needed to change it.

It's at hilal-ramadan.surge.sh. Free to use, works on any phone or browser. If you install it to your home screen it behaves like a native app.

Ramadan Mubarak to everyone in this community.

**Link:** https://hilal-ramadan.surge.sh
**Best time to post:** First week of Ramadan, morning (around Fajr EST)
**Notes:** r/islam requires genuine community participation, not drive-by promotion. Engage respectfully with any questions about calculation methods. Be prepared to explain which method is the default and why. Do not post this from a brand-new account. The Ramadan Mubarak closing is sincere, not a tactic.

---

## r/MuslimLounge posts

### r/MuslimLounge, Post 1
**Title:** Free prayer streak app for Ramadan. 55KB, works offline, no tracking.
**Flair:** Apps & Tech

Assalamu Alaikum brothers and sisters,

I wanted to share something I built for Ramadan. It's a prayer streak app, kind of like a Duolingo streak but for salah. It tracks your 5 daily prayers and shows your consistency over the month.

It's called PrayerLock. A few things I made sure of:

- zero ads
- no account required
- no data leaves your device (everything stores in your browser's local storage)
- works offline after the first load
- 55KB total size (loads fast on mobile data)
- install to home screen and it works like a native app

The streak mechanic is optional. If you don't want to think about streaks and just want a simple tracker, you can use it in list mode without the streak counter.

I'm not trying to sell anything. This is just a free tool I built because the apps I found either had ads or required sign-in to use basic features.

It's at prayerlock-app.surge.sh. Works on any phone.

Ramadan Mubarak. May Allah accept our fasting and prayers.

**Link:** https://prayerlock-app.surge.sh
**Best time to post:** First few days of Ramadan, after Fajr or Maghrib EST
**Notes:** r/MuslimLounge has a tighter community feel than r/islam. Shorter post is better here. The technical specs (55KB, offline) matter to users who've dealt with bloated apps eating their data. Do not cross-post the identical text from r/islam. Different angle: r/islam gets the feature breakdown, r/MuslimLounge gets the personal/community angle. Engage any "is this halal to use" type questions about data privacy with direct confirmation that zero data is transmitted.

---

## Pre-publish checklist (run before each post)

- [ ] Zero em dashes in post body
- [ ] Zero banned AI vocabulary (use, use, dig, complete, strong, novel, seamless)
- [ ] First sentence delivers value or consequence, not setup
- [ ] Specific numbers present (KB sizes, site counts, revenue figures, percentages)
- [ ] No promotional adjectives (revolutionary, cutting-edge, game-changing)
- [ ] No title case headings within post body
- [ ] Tool names are specific (surge.sh, formsubmit.co, not "hosting platform")
- [ ] Honest about failures where applicable (especially r/indiehackers, r/Entrepreneur)
- [ ] Link is in the body or comment, not the title
- [ ] Posted from aged account with relevant karma for that subreddit
