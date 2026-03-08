# Reddit Distribution Cycle 8 - March 8, 2026

Status: READY_TO_POST
Generated: 2026-03-08

---

## POST 1: r/SideProject

**Title:** i built 22 PWAs in 35 days with $0 hosting. here's what i learned about shipping fast

**Flair:** Show and Tell

**Best time:** Tuesday or Wednesday, 9-11 AM EST

**Body:**

35 days ago i decided to stop planning and just build. one app per day, some days two. all progressive web apps, all hosted free on surge.sh.

here's the stack for every single one:

- vanilla HTML/CSS/JS (no frameworks)
- service worker for offline support
- manifest.json for installability
- surge.sh for hosting ($0/mo, unlimited projects)
- total build time per app: 2-6 hours

what i built:

- 7 streak/habit trackers for different niches (scripture reading, fitness, meditation, coding)
- cold email ROI calculator
- subject line grader
- sleep quality tracker
- moon sighting tracker for ramadan
- prayer time app (55KB total, works offline)
- daily planner tools
- a few more i'm forgetting

what actually worked:

1. **templates compound.** after the first 3 apps, i had a base template. apps 4-22 took half the time. same service worker pattern, same manifest structure, same deployment script. `surge ./dist appname.surge.sh` and it's live in 8 seconds.

2. **PWAs are underrated for MVPs.** no app store review. no $99/yr apple developer fee. no 30% cut. users install from the browser. works on every phone. 55KB vs 50MB+ for a react native app doing the same thing.

3. **scope creep is the real killer.** the apps that shipped fast had exactly one feature. the ones that took longest were the ones where i thought "oh it would be cool if it also did X." it never needs to also do X. not in v1.

4. **nobody cares about your tech stack.** i spent zero time on architecture decisions. no state management debates. no build tools. just files that work. the prayer time app is literally one HTML file with inline CSS and JS. users don't care. it loads in 200ms and does the thing.

what didn't work:

- building 22 apps before validating any of them. i have 22 deployed apps and $0 revenue. should have built 3 and spent the other 32 days on distribution.
- no analytics on any of them at launch. couldn't tell you which ones get traffic.
- didn't collect emails on most of them. free tool with no capture = pure charity.

the honest truth: shipping fast feels productive but it's not the same as building a business. i got really good at building and really bad at selling. working on fixing that now.

happy to share the code structure or the base template if anyone wants to skip the first 3 apps of learning curve. the pattern is dead simple once you see it.

---

## POST 2: r/webdev

**Title:** PWAs are criminally underrated. i replaced 6 native app ideas with 55KB progressive web apps

**Flair:** Discussion

**Best time:** Monday or Wednesday, 10 AM - 12 PM EST

**Body:**

i keep seeing people reach for react native or flutter when they have a simple app idea. i built 22 PWAs in the past month and i'm convinced most apps don't need to be native.

real numbers from one of them (a prayer time tracker called PrayerLock):

- total size: 55KB
- loads in under 200ms on 3G
- works fully offline (service worker caches everything)
- installable on both iOS and Android via "add to home screen"
- no app store, no review process, no $99/yr fee, no 30% revenue cut
- deployed in 8 seconds via `surge ./dist prayerlock.surge.sh`

the stack is embarrassingly simple:

```
index.html      - single page app
sw.js           - service worker (precache + offline fallback)
manifest.json   - PWA manifest (name, icons, theme color)
style.css       - styles
app.js          - logic
```

no webpack. no vite. no bundler. no node_modules. just files.

what PWAs can do now that people don't realize:

- **offline mode** (service workers). full functionality with no connection.
- **push notifications** (web push API). works on android, mostly works on iOS 16.4+.
- **install prompt** (beforeinstallprompt event). native-feeling install flow.
- **background sync** (background sync API). queue actions while offline, sync when back.
- **file system access** (file system access API, chromium). read/write local files.
- **camera/mic** (mediaDevices API). works fine for basic capture.

what PWAs still can't do well:

- bluetooth/NFC (limited support)
- anything requiring app store discoverability (ASO is real)
- complex background processing on iOS (apple still throttles this)
- iOS push notifications still feels janky
- no access to HealthKit, Core Motion, or platform-specific sensors

my honest take: if your app is basically "show data, let user interact, save state," a PWA does the job. you don't need 200MB of react native dependencies for a streak tracker.

the 55KB number isn't a flex, it's a consequence of not using frameworks. turns out HTML + CSS + vanilla JS is already pretty good at making web apps. who knew.

for people building side projects: ship the PWA first. if it gets traction and you actually need native APIs, then port it. 95% of side projects die before reaching that point anyway. don't pre-optimize for a problem you'll never have.

source: i built all 22 of these in about 35 days. the template pattern is reusable. happy to answer technical questions about the service worker setup or the deployment pipeline.

---

## POST 3: r/Entrepreneur

**Title:** day 35 building in public. 168 deployed sites, $0 revenue. here's the honest breakdown of what went wrong

**Flair:** Lessons Learned

**Best time:** Sunday or Monday, 8-10 AM EST

**Body:**

i'm going to be real because most "building in public" posts are just disguised promos. this one isn't. i genuinely messed up and i think the lesson is useful.

**the numbers (all real):**

- 168 deployed sites/landing pages (surge.sh, $0 hosting)
- 22 progressive web apps built and live
- 13 digital products created (Gumroad PDFs, calculators, toolkits)
- 283 social media posts written and queued
- 1,100+ leads scraped and organized
- 90+ automation scripts running via cron

**revenue: $0**

i'm not joking. 35 days, all of that output, zero dollars.

**what went wrong:**

1. **i confused building with selling.** building feels productive. you ship something, you get a dopamine hit. but nobody was buying because nobody knew the stuff existed. i built 13 Gumroad products and listed exactly zero of them with proper distribution. they're just sitting there.

2. **no validation loop.** i never stopped to check if anyone wanted what i was building. i just kept building the next thing because the building part was fun. classic indie hacker trap.

3. **automation before revenue.** i spent a full week building scraping and monitoring infrastructure. 90+ scripts. beautiful cron schedules. zero of it connected to anything that makes money. i automated the wrong things.

4. **quantity without focus.** 168 sites sounds impressive until you realize each one got maybe 20 minutes of attention. none of them are great. they're all mediocre. 5 great sites would have been better than 168 forgettable ones.

5. **zero outbound.** 1,100 leads sitting in a spreadsheet. i didn't email a single one. the cold email tools i built? never used them on real prospects. i built the gun, loaded it, and put it in a drawer.

**what i'm doing differently starting now:**

- killing 90% of the sites. keeping only the ones with actual search intent behind them.
- picking 3 products, listing them properly with real copy, real screenshots, real distribution.
- doing actual cold outreach instead of building more outreach tools.
- posting the 283 queued posts instead of writing 283 more.
- measuring one number: revenue. not deploys, not scripts, not sites.

**the actual lesson:** output is not outcome. the market doesn't care how much you built. it cares if you solved a problem someone will pay for. i got high on my own supply of productivity and forgot the whole point.

if you're in the building phase right now, stop and ask yourself: "when was the last time i talked to a potential customer?" if the answer is "never" or "not recently," you might be making the same mistake i did.

happy to answer questions. i'm not selling anything (clearly lol).

---

## POST 4: r/islam

**Title:** free ramadan tools - prayer time tracker, moon sighting app, daily planner. no ads, no tracking, open source

**Flair:** Ramadan

**Best time:** Friday after Jummah, 2-4 PM EST (or Saturday morning)

**Body:**

assalamu alaikum,

ramadan mubarak to everyone. i built a few free tools for ramadan and wanted to share them with the community. no ads, no data collection, no signup required.

**PrayerLock** - prayer time tracker

- tracks all 5 daily prayers + taraweeh
- works completely offline (no internet needed after first load)
- 55KB total size, loads instantly
- installable on your phone from the browser (add to home screen)
- no account needed, all data stays on your device
- prayerlock.surge.sh

**Hilal** - moon sighting tracker

- tracks moon phases throughout ramadan
- sighting reports and visibility calculations
- helps communities coordinate for eid
- hilal-app.surge.sh

**Ramadan Daily Planner**

- daily schedule with suhoor/iftar times
- quran reading tracker
- dua checklist
- printable format available
- ramadan-daily-planner.surge.sh

all three are progressive web apps. that means you can "install" them from your phone's browser and they'll work like regular apps, even offline. no app store needed.

these are completely free and will stay free. i built them because i wanted simple tools that respect privacy and don't blast you with ads during worship. all data stays on your device.

there are about 19 days of ramadan left so hopefully these are still useful. if you notice any bugs or have suggestions, let me know and i'll fix them.

may Allah accept your fasting and prayers this ramadan.

---

## POST 5: r/ADHD

**Title:** i built a free habit streak app specifically designed for ADHD brains. shorter sessions, dopamine hits, no guilt mechanics

**Flair:** Tips/Suggestions

**Best time:** Tuesday or Thursday, 11 AM - 1 PM EST

**Body:**

i have ADHD and every habit tracking app i've tried makes me feel worse. here's why:

- they punish you for missing a day (your "streak" resets and you feel like garbage)
- they expect daily consistency (lol)
- the tasks are too vague ("meditate for 30 minutes" - yeah right)
- they're designed for neurotypical brains that can just... do things

so i built one that works differently.

**what's different:**

**micro-sessions instead of full commitments.** the shortest session is 2 minutes. not 30. not even 10. two minutes. because starting is the hardest part and once you start you usually keep going. but if you only do 2 minutes, that still counts.

**no streak death.** missing a day doesn't reset everything. your progress is cumulative, not fragile. a 30-day streak that breaks on day 31 shouldn't feel like failure. it's 30 days of evidence that you can do the thing.

**dopamine on purpose.** small completions trigger visible progress. colors change. counters go up. it sounds stupid but ADHD brains are literally wired to respond to immediate visual feedback. i designed around that instead of pretending willpower is enough.

**flexible scheduling.** not everything needs to happen every single day. some habits are 3x/week. some are "whenever i remember." the app doesn't judge you for setting a realistic schedule.

**no premium upsell guilt.** it's free. all features. no "upgrade to unlock streaks longer than 7 days" nonsense.

it's a progressive web app so you can install it from your browser. works on any phone, works offline, 55KB total. no account needed, all your data stays on your device.

i'm genuinely looking for feedback from other ADHD people. what features would actually help? what do existing apps get wrong? i want to make this actually useful, not just another app that sits on your home screen for 3 days.

the app is at adhd-streak.surge.sh

(if this kind of post isn't allowed here, mods please let me know and i'll remove it. just trying to share something that helped me.)

---

## POST 6: r/coldEmail

**Title:** i built a free cold email ROI calculator and subject line grader. no signup needed

**Flair:** Tool/Resource

**Best time:** Wednesday or Thursday, 10 AM - 12 PM EST

**Body:**

got tired of guessing whether a cold email campaign was worth running, so i built two free tools.

**cold email ROI calculator** (cold-email-roi-calculator.surge.sh)

plug in your numbers and it tells you if a campaign is worth it before you send a single email.

inputs:
- list size
- estimated open rate
- estimated reply rate
- estimated close rate
- deal value
- cost per lead (if you're buying lists)
- tool costs (lemlist, instantly, smartlead, whatever)

outputs:
- projected revenue
- cost per acquisition
- ROI percentage
- break-even point

example calculation: 1,000 leads, 45% open rate, 3% reply rate, 10% close rate, $2,000 deal value = 3 closed deals = $6,000 revenue. if your tools cost $100/mo and leads cost $0.05 each ($50), your ROI is 9,700%. now you know if it's worth running before you burn the list.

the tool also shows you where the biggest leverage point is. like if bumping your reply rate from 3% to 5% doubles your revenue, maybe spend time on copy instead of buying more leads.

**subject line grader** (subject-line-grader-pm.surge.sh)

paste in your subject line and it scores it on:
- length (sweet spot is 28-50 characters)
- spam trigger words
- personalization tokens
- curiosity/specificity balance
- mobile preview truncation (will it get cut off on phones?)

it's not AI-powered or anything fancy. just pattern matching against what actually works based on published benchmarks. open rates drop 10-15% when subject lines exceed 60 characters. the tool flags that stuff.

both tools are free, no signup, no email capture. just use them. built as PWAs so they work offline too if you want to install them.

looking for feedback from people who actually send cold email. what calculations or checks would you add? i want to make these actually useful for daily workflow.

---

## POST 7: r/IndieHackers (or indiehackers.com)

**Title:** month 1 building a portfolio of micro-tools. 168 sites, 22 apps, 13 digital products. $0 revenue. lessons learned

**Flair:** Article

**Best time:** Monday or Tuesday, 9-11 AM EST

**Body:**

i'm going to share the real numbers because i think the failure is more interesting than the plan.

**what i built in 35 days:**

- 22 progressive web apps (PWAs, all free hosting on surge.sh)
- 13 digital products (Gumroad PDFs, calculators, toolkits)
- 168 landing pages and microsites
- 90+ automation scripts (scrapers, content generators, monitoring)
- 1,100+ leads scraped and organized
- 283 social media posts written and queued

**the stack:**

- PWAs: vanilla HTML/CSS/JS, no frameworks. average app is 55-200KB.
- hosting: surge.sh (free, unlimited projects, SSL included)
- products: Gumroad (free until you sell something)
- automation: python + cron jobs
- total monthly cost: $0 (just my time)

**revenue: $0**

i know.

**here's what i learned:**

**1. the portfolio strategy has a critical flaw.**

the idea was "build 20 small things, one of them will work." the problem is none of them work if you don't distribute any of them. i was so focused on building the next thing that i never went back and actually marketed the last thing. each app got about 20 minutes of distribution attention. that's not enough.

**2. PWAs are perfect for micro-tools.**

this part actually worked. the build cycle for a new PWA from template is about 2-4 hours. deploy is 8 seconds. no app store review, no hosting costs, works offline, installable. for MVPs and free tools this is the best stack i've found.

**3. automation is a trap if you don't have revenue.**

i built 90+ scripts. scrapers, content generators, competitive monitoring, lead enrichment. beautiful infrastructure. zero of it generates revenue. i automated the interesting parts and ignored the boring parts (listing products, writing sales pages, doing outreach).

**4. digital products are the fastest path to first dollar.**

of everything i built, the 13 Gumroad products are closest to revenue. they're done. they just need listing and distribution. i should have focused there from day 1 instead of building 22 apps.

**5. "building in public" is accountability theater if nobody's watching.**

i wrote 283 posts and queued them up. posted maybe 15. the build-in-public strategy requires the "in public" part. i was building in private and planning to go public. different thing entirely.

**what i'm doing in month 2:**

- picking the top 3 products and doing proper launches
- actually posting the 283 queued posts
- sending cold emails to the 1,100 leads
- killing the apps that have zero search intent behind them
- tracking one metric: revenue

the honest truth about indie hacking that nobody talks about: the building is the easy part. i can build all day. the selling, the marketing, the putting yourself out there part, that's what's hard. and that's the part that actually matters.

if you're reading this and you have a bunch of stuff built but nothing sold, you're not alone. but also, we should probably both stop building and start selling.

---

## POSTING NOTES

**General Reddit rules to follow:**
- Wait at least 24-48 hours between posts across subreddits
- Don't post more than 2-3 per week total
- Respond to every single comment within the first 2 hours
- Never link to your own stuff in the first comment. wait for someone to ask
- If the post gets traction, add an edit with the link people are requesting

**Subreddit-specific:**
- r/islam: be genuinely respectful. this is not a marketing channel. you're serving the community.
- r/ADHD: be real about having ADHD. don't position yourself as someone with a solution. position as someone with the same problem who built something that might help.
- r/coldEmail: these people know their stuff. don't oversimplify. show real numbers.
- r/Entrepreneur: vulnerability wins. the $0 revenue number is the hook, not the app count.
- r/SideProject and r/webdev: technical detail matters. show code structure, real file sizes, real deployment commands.

**Order of posting (space these out over 2 weeks):**
1. r/Entrepreneur (strongest narrative, test the vulnerability angle)
2. r/islam (time sensitive, ramadan ending)
3. r/SideProject (technical + story combo)
4. r/coldEmail (value-first, specific tools)
5. r/ADHD (needs most careful tone)
6. r/webdev (pure technical, good for weekday)
7. r/IndieHackers (similar to entrepreneur, save for last)

**Engagement protocol:**
- Reply to every comment within first 2 hours (critical for algorithm)
- Ask follow-up questions to genuine commenters
- If someone asks for a link, provide it in a reply (not as an edit to the post)
- If someone criticizes, agree with the valid parts. don't get defensive.
- Upvote everyone who engages with your post
