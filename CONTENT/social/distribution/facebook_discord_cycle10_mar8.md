# Facebook Groups + Discord Distribution — Cycle 10, 2026-03-08
# Status: PENDING_REVIEW
# Total: 6 Facebook group posts + 4 Discord posts
# Assets: tools hub, cold email stack, local biz demos, ADHD streak, Ramadan apps, PageScorer

---

## Pre-publish checklist (run before posting each)

- [ ] Zero em dashes
- [ ] Zero banned AI vocabulary (leverage, utilize, comprehensive, robust, innovative, seamless, game-changer, empower, unlock, delve, revolutionary, streamlined, foster)
- [ ] No "It's not just X, it's Y" constructions
- [ ] No promotional adjectives
- [ ] Consequence-first hook
- [ ] Specific numbers present
- [ ] Would @pipelineabuser post this
- [ ] First sentence delivers value, not setup
- [ ] Lowercase energy maintained throughout

---

# FACEBOOK GROUP POSTS

---

## FB POST 1 — Solopreneur / Indie Hacker groups
Target groups: Indie Hackers, Solopreneurs United, One Person Business, Build In Public Community
Tone: build-in-public transparency, peer sharing, slight flex but mostly just showing work
Screenshot: browser with printmaxx-tools.surge.sh open showing the grid of 46 tool cards

---

built 258 sites in 35 days as a solo dev. here's what actually happened.

i'm on day 35 of a solo building sprint. no team, no funding, no audience when i started. just claude code and a bad habit of not sleeping.

the breakdown:
- 22 PWA apps (streak trackers, productivity tools, cold email tools)
- 19 local business demo sites
- 46 free tools on a single hub page
- 13 comparison landing pages
- the rest are marketing pages, lead magnets, calculators

what i learned that nobody tells you:

1. deploying is harder than building. i spent more time on surge.sh configs than actual code. the unsexy work is where everything breaks.

2. the first 20 sites taught me nothing. site 21-50 is where patterns clicked. by site 100 i had templates that took 15 minutes each.

3. nobody cares about your site until you put it where people already are. i had tools live for 2 weeks with zero traffic because i never shared them anywhere.

4. PWAs are underrated for solo devs. no app store review, no $99/yr apple tax, works offline, installable. i ship updates in 30 seconds.

5. 258 sites and $0 revenue so far. being honest. distribution is the bottleneck, not building. i have more products than i have people who know they exist.

the tools hub has 46 free things i built: calculators, audit tools, planners, graders. all free, no signup required.

printmaxx-tools.surge.sh

if you're building solo, what's your biggest bottleneck right now? genuinely curious. mine is clearly distribution.

---

## FB POST 2 — Cold Email / Sales groups
Target groups: Cold Email Mastery, B2B Sales Strategies, Lead Generation Tactics, Email Outreach Pros
Tone: practitioner sharing findings, cost-conscious, anti-tool-bloat
Screenshot: side-by-side showing paid tools vs free alternatives with monthly costs crossed out

---

i was paying $97/mo for instantly + $29/mo for a subject line tool + $19/mo for an ROI calculator spreadsheet template. $145/mo before sending a single email.

then i built free versions of all three. took a weekend.

here's what i replaced:

1. cold email sending + warmup: coldmaxx (coldmaxx-app.surge.sh)
tracks sequences, handles follow-ups, warmup scheduling. not as feature-rich as instantly but covers 80% of what solopreneurs actually need. free.

2. subject line testing: subject line grader (subject-line-grader-pm.surge.sh)
scores your subject lines on length, spam trigger words, personalization, curiosity factor. gives you a score out of 100 with specific fixes. free.

3. ROI calculator: cold email ROI calculator (cold-email-roi-calculator.surge.sh)
plug in your list size, open rate, reply rate, close rate, deal size. tells you expected revenue per campaign. helps you decide if a list is worth emailing before you burn it. free.

total monthly cost now: $0.

the tradeoff is real though. these don't have deliverability monitoring, team collaboration, or CRM integrations. if you're a 1-2 person operation sending under 500 emails/day, they work fine. if you're running a 10-person SDR team, you still need the paid tools.

but for solo founders testing cold outreach for the first time? spending $150/mo before your first reply is backwards.

links again:
- coldmaxx-app.surge.sh
- subject-line-grader-pm.surge.sh
- cold-email-roi-calculator.surge.sh

what's your current cold email stack costing you monthly?

---

## FB POST 3 — Web Dev / Freelancer groups
Target groups: Web Developers & Designers, Freelance Web Design, WordPress & Web Dev Community, Frontend Developers
Tone: generous resource sharing, peer-to-peer, portfolio reference angle
Screenshot: grid of 4-5 local biz demo sites on mobile and desktop side by side

---

i built 19 local business demo websites and i'm giving them away as free references.

background: i was pitching local businesses on web redesigns and kept hearing "show me what it would look like first." so instead of doing free mockups for every lead, i built industry-specific demos that i can point anyone to.

the demos cover:
- plumbing, hvac, electrical (trades)
- salon, barbershop, spa (beauty)
- restaurant, cafe, bakery (food)
- lawn care, landscaping (outdoor services)
- dentist, chiropractor (health)
- gym, yoga studio (fitness)
- auto repair, car detailing (automotive)

every demo has:
- mobile-first layout (because 70%+ of local searches happen on phones)
- click-to-call button above the fold
- google maps placeholder
- services section with pricing hints
- testimonial section
- booking/contact CTA

printmaxx-local-demos.surge.sh

use cases for other freelancers:
1. show clients what "modern" looks like vs their 2018 squarespace site
2. use as starter templates for your own builds (inspect the source, it's all vanilla html/css)
3. reference for layout patterns that work for service businesses

these are free. no attribution needed. if you're a freelancer pitching local businesses, feel free to use these in your proposals. saves you the "but what would it actually look like" conversation.

what industries am i missing? i'll build more if there's demand.

---

## FB POST 4 — ADHD / Productivity groups
Target groups: ADHD Adults Support, Productivity & ADHD, ADHD Life Hacks, Neurodivergent Professionals
Tone: empathetic, personal, zero condescension, built-by-someone-who-gets-it energy
Screenshot: phone mockup showing the ADHD streak app with a 12-day streak and the calendar view

---

i have ADHD and every habit tracker i tried made me feel worse.

the pattern was always the same: download app, set up 14 habits because i'm optimistic on day 1, track for 3 days, miss a day, see the broken streak, feel like garbage, delete the app.

so i built one that works differently.

adhd-streak.surge.sh

here's what makes it different from the 200 habit trackers on the app store:

1. one habit at a time. not 14. you pick one thing and that's it. the interface won't let you add more until you've kept a streak for 7 days. forced simplicity.

2. no account creation. this was important to me. the moment an app asks me to create an account, i close it. this saves everything to your phone locally.

3. no ads. no notifications. no push alerts. no "you haven't logged in today!" guilt messages. you open it when you remember. if you forget, it's there when you come back.

4. works offline. it's a PWA, so you install it to your home screen and it works without internet. i use it on airplane mode when i need to focus.

5. the streak display is visual. a calendar with colored dots. my brain needs to see the chain to care about not breaking it. numbers alone don't motivate me.

6. it's 55KB total. loads instantly. no waiting, no loading screen, no splash page.

i built this for myself first. shared it with a few friends who also have ADHD and they asked me to make it public. so here it is.

it's completely free. no premium tier, no "unlock 3 more habits for $4.99." what you see is what you get.

if you try it, i'd love to know: does the one-habit-at-a-time constraint help or would you want the option to add more? trying to figure out if that's a feature or a limitation.

adhd-streak.surge.sh

---

## FB POST 5 — Muslim / Ramadan groups (URGENT, 19 days left)
Target groups: Muslim Community USA, Ramadan Mubarak 2026, Muslim Professionals Network, Islam & Daily Life, American Muslims, Muslim Parents
Tone: community member sharing a gift, zero promotion, warm and genuine, salam opener
Screenshot: phone showing hilal app with fasting tracker and progress rings for the month

---

assalamu alaikum everyone. ramadan mubarak.

i built 3 free apps for ramadan and wanted to share them with the community before we're too deep into the month. we have about 19 days left inshaAllah.

1. hilal (hilal-app.surge.sh)
ramadan companion app. tracks fasting days, prayer completion, quran reading progress, and sadaqah for the month. shows your progress visually so you can see how your ramadan is going at a glance.

2. prayerlock (prayerlock-app.surge.sh)
prayer times based on your location + a completion tracker. mark each salah as you pray it. keeps a streak going so you can see consistency over the month. the idea is simple: don't break the chain.

3. quran streak (quran-streak-app.surge.sh)
daily quran reading tracker. set your goal (1 page, 1 juz, whatever works for you) and mark each day you read. visual calendar shows your progress.

important things about all 3:
- completely free. no premium version, no ads, no upsells
- no account needed. your data stays on your phone
- works offline (they're PWAs, install to your home screen)
- no data collection. i don't track you, sell your info, or even have a server
- built with respect for the deen. no music, no unnecessary images

i built these because the ramadan apps on the app store either cost money, show ads between prayers (astaghfirullah), or require you to create an account and give your email.

you shouldn't need to give your email to track your ibadah.

if these help even one person stay consistent this ramadan, alhamdulillah that's enough.

please share with family and friends if you find them useful. JazakAllahu khairan.

---

## FB POST 6 — Small Business Owner groups
Target groups: Small Business Owners USA, Local Business Marketing Tips, Entrepreneurs & Small Business, Main Street Business Network
Tone: direct offer, slightly provocative opening, practitioner not agency
Screenshot: before/after comparison of a dated business site vs one of the modern demos

---

i pulled up 50 local business websites last week. 38 of them looked like they were built in 2016 and never touched again.

the patterns are always the same:
- stock photo of a handshake as the hero image
- phone number hidden in the footer
- "welcome to our website" as the headline
- takes 6+ seconds to load on mobile
- not mobile-friendly at all (you have to pinch and zoom)

meanwhile their competitor down the street has a clean site with click-to-call, online booking, and loads in 2 seconds. guess who gets the call.

i built demo sites for 19 different local business types to show what "modern" actually looks like:

printmaxx-local-demos.surge.sh

trades (plumbing, hvac, electrical, roofing)
beauty (salon, barbershop, spa)
food (restaurant, cafe, bakery)
health (dentist, chiropractor)
fitness (gym, yoga studio)
auto (repair shop, detailing)
outdoor (lawn care, landscaping)

every demo has:
- mobile-first design (because 76% of "near me" searches happen on phones)
- click-to-call button that's actually visible
- google maps section
- services with transparent pricing
- booking/contact form above the fold

if your business site is in the "2016 and never touched" category, two options:

1. browse the demos for free and use them as a reference for what to ask your web person to build
2. DM me. i'll look at your current site and tell you honestly whether it needs a refresh or if it's fine. no charge for the opinion.

the sites are at printmaxx-local-demos.surge.sh and the full services page is at printmaxx-services.surge.sh

what industry is your business in? curious which demos would be most useful.

---

# DISCORD SERVER POSTS

---

## DISCORD POST 1 — r/webdev Discord (#share-your-project or #tools)
Server: Reactiflux / The Coding Den / Webdev & Webdesign
Channel: #show-your-work or #tools-and-resources

---

built a free website audit tool if anyone wants to test it.

**pagescorer** (pagescorer.surge.sh)

paste any URL and it gives you scores across 5 categories:
- performance (load time, asset size, render blocking resources)
- SEO (meta tags, heading structure, alt text, canonical URLs)
- accessibility (contrast ratios, ARIA labels, keyboard nav)
- security (HTTPS, headers, mixed content)
- mobile (viewport, tap targets, responsive images)

runs client-side. no backend, no account, no data stored.

i built it because lighthouse is great but overkill for quick audits. sometimes i just want to paste a URL and see "your meta description is missing" without waiting for a full 30-second analysis.

it's not a lighthouse replacement. it's more like a quick triage tool when you're reviewing a client site or checking your own stuff.

open source, free, no catch. feedback on scoring accuracy would be useful. especially the performance scoring, that's the hardest to get right without a real backend.

pagescorer.surge.sh

---

## DISCORD POST 2 — IndieHackers Discord (#milestones or #build-in-public)
Server: Indie Hackers
Channel: #milestones or #build-in-public

---

day 35 build-in-public update.

numbers:
- 258 sites deployed on surge.sh
- 22 PWA apps (streak trackers, tools, calculators)
- 46 free tools on one hub page
- 13 comparison landing pages (X vs Y format)
- 19 local business demo sites
- $0 revenue

the honest version: i built too much and sold too little. classic indie hacker trap.

what's working:
- PWAs are the move for solo devs. no app store review, no fees, instant deploys. my apps are 30-80KB each.
- comparison pages are starting to get organic search impressions. "coldmaxx vs instantly" type stuff.
- local business demos are the closest to actual revenue. business owners can see exactly what they'd get.

what's not working:
- zero distribution for the first 2 weeks. i just built and deployed into the void.
- too many products, not enough depth on any single one.
- no email list until week 3. left money on the table.

current stack: claude code for everything, surge.sh for hosting ($0), vanilla html/css/js for most sites, next.js for the main site.

hub with all 46 free tools: printmaxx-tools.surge.sh

the plan for next 30 days: stop building, start distributing. the code is done. the marketing is not.

anyone else stuck in build-more-ship-less mode? how did you break out of it?

---

## DISCORD POST 3 — Claude Code / AI Tooling Discord (#showcase or #projects)
Server: Claude Code Community / AI Dev Tools / Anthropic Discord
Channel: #showcase or #projects

---

built a side-by-side comparison of cursor vs claude code for solo dev workflows.

cursor-vs-claudecode.surge.sh

not a hot take post. it's a structured breakdown of both tools across actual categories:
- speed of iteration (how fast you go from idea to deployed)
- context window handling (how each deals with large codebases)
- file editing (inline vs agent-style)
- debugging workflows
- cost at different usage levels
- terminal integration

the context: i've shipped 258 sites in 35 days using claude code almost exclusively. ran cursor for about a week before switching. the comparison page covers what made me switch and where cursor still wins.

spoiler: claude code wins on speed of deployment and autonomy (the ralph loop pattern is unbeatable for overnight batch work). cursor wins on visual diff review and when you need tight IDE integration.

also built similar comparison pages for:
- instantly vs lemlist (cold email tools)
- convertkit vs beehiiv (newsletters)
- pagescorer vs gtmetrix (site audit)
- sleepmaxx vs sleep cycle (sleep tracking)

all at printmaxx-comparisons.surge.sh

the comparison page format itself is interesting for SEO. "X vs Y" queries have high purchase intent and most results are either reddit threads or affiliate blog spam. a clean, honest comparison page fills a real gap.

---

## DISCORD POST 4 — Productivity / ADHD Discord (#tools or #apps)
Server: ADHD Discord / Productivity Server / Self Improvement Discord
Channel: #tools, #apps, or #resources

---

made a few free streak/habit apps. sharing in case they're useful.

**adhd streak** (adhd-streak.surge.sh)
built specifically for ADHD brains. one habit at a time. no account. no notifications. no guilt mechanics. just a visual calendar where you mark each day. the constraint of only tracking one thing at a time is intentional. every other habit app lets you add 15 habits on day 1, which is a setup for failure.

**other streak apps** (same format, different focus):
- fitness-streak-app.surge.sh (workout consistency)
- reading-streak-app.surge.sh (daily reading)
- meditation-streak-app.surge.sh (meditation practice)
- coding-streak-app.surge.sh (daily coding)
- journal-streak-app.surge.sh (journaling)

all of them:
- free, no premium tier
- no account creation (data saved locally on your device)
- work offline (PWAs, install to home screen)
- under 60KB each (load instantly)
- no ads, no tracking, no data collection

the design philosophy is "don't break the chain" from the seinfeld productivity method. the visual streak on a calendar creates enough motivation to keep going without needing points, badges, leaderboards, or any of that gamification stuff that stops working after a week.

if anyone tries the ADHD one specifically, i'd love feedback on the one-habit constraint. some people love it, some want 2-3 habits max. trying to figure out the right limit.
