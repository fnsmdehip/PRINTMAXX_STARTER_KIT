# Reddit Posts — Compound Batch — 2026-04-01
# Status: READY TO POST

---

## REDDIT 09 — r/SideProject + r/indiehackers
**Title: I built 530 automation scripts and made $0 in 57 days. here's what went wrong.**

I've been building an autonomous revenue system as a solo developer. The architecture is genuinely impressive (not bragging, it's the problem):

- 530 Python scripts
- 33 AI agents running on cron jobs
- 388 deployed websites
- 14 finished digital products
- 22 marketplace listings ready to publish
- 192,700 scraped leads, 17,484 qualified as hot
- 251 personalized cold emails generated

Revenue: $0. For 57 consecutive days.

The diagnosis: I automated everything except the actions that require me to personally sign up for payment platforms, send the first email, and list the first product.

I'm calling it "automation dysmorphia" -- when your system is so good that building it becomes a substitute for doing the uncomfortable work that generates revenue.

The fix I'm implementing:
1. Freeze all new script creation
2. Identify the 3 actions closest to money: send cold emails (15 min), list products on Gumroad (45 min), sign up for affiliate programs (30 min)
3. Do them manually first
4. Only automate what works

Has anyone else fallen into this trap? Curious if there's a common pattern.

---

## REDDIT 10 — r/webdev + r/web_design
**Title: PSA: surge.sh free tier serves Disallow: / in robots.txt at the CDN level. your sites are invisible to Google.**

Discovered this after deploying 388 sites to surge.sh over the past 2 months.

Surge's free student plan injects `Disallow: /` into robots.txt at the CDN layer. You can't override it with your own robots.txt file. Every page on every site is blocked from search engine crawling.

This means:
- All your SEO work (meta tags, schema markup, sitemaps) does nothing
- Google will never index any page
- Your sites effectively don't exist for organic search

Options:
- Surge Plus ($13/mo) removes the restriction
- Netlify free tier has no such restriction
- Cloudflare Pages free tier has no such restriction

Check yours: `curl -s yoursite.surge.sh/robots.txt`

If you see `Disallow: /` and you didn't put it there, now you know why your site has zero organic traffic.

Figured this out after 2 months. Wanted to save someone else the time.

---

## REDDIT 11 — r/ClaudeAI + r/ChatGPTCoding
**Title: I run 33 autonomous AI agents on a 2-hour cycle. here's which ones are actually useful after 48 cycles.**

Built a swarm of 33 AI agents using Claude Code that auto-run on cron jobs. After 48 decision cycles, the "swarm brain" agent scored and rebalanced them. Results:

**S-Tier (actually essential):**
- System healer: monitors disk, memory, process health. caught 3 silent failures that would have killed the pipeline
- Data janitor: found 99.9% duplicate rows in a tracker. 2,807 of 2,810 rows were identical copies. the scraper had a merge() bug nobody noticed

**A-Tier (genuinely useful):**
- Asset deployer: tracks 388 sites, 100% critical pass rate
- Revenue tracker: clearest picture of where money leaks exist
- Playwright tester: automated QA on all deployed sites, 92.2% pass rate
- Lead machine: 10 new leads per cycle, with quality scoring and outreach drafts

**B-Tier (useful but overpowered):**
- Competitor stalker: found a free AI Bible app that invalidated my product strategy. now promoted
- Cross-pollinator: wires outputs from one agent as inputs to another. found 11 new connections this cycle

**Killed (waste of compute):**
- Opportunity scanner: redundant with gap hunter
- Content compounder: no social accounts to post on
- Trend synthesizer: nobody consumes the output

Key lesson: more agents is not better. the swarm brain spent most of its time REDUCING the fleet, not expanding it. went from 25 to 12 productive agents. the rest were generating reports nobody read.

if you're building agent swarms, build the evaluation layer first. otherwise you're running 33 agents at full cost when 12 do the actual work.

---

## REDDIT 12 — r/Entrepreneur + r/startups
**Title: Anthropic launched 13 free Claude Code courses. every paid AI education product just died.**

Anthropic (maker of Claude) launched Anthropic Academy: 13 free courses with official certificates, hosted on Skilljar and Coursera.

There's also CC for Everyone (ccforeveryone.com): free interactive Claude Code course for non-coders.

And Sahil's open source Claude Code skills at 4.8K GitHub stars.

I had 16 paid digital products about Claude Code ready to list. All educational: "how to use Claude Code for X." All now worthless.

This is a predictable pattern:
- Apple released Swift Playgrounds, killed third-party Swift courses
- Google released Android training, killed third-party Android guides
- AWS/Azure/GCP all have free cert prep, suppressing paid prep courses

The framework: never sell education about a tool. The vendor will always give it away to drive adoption.

What survives: operational products. Not "learn how to configure an AI agent" but "install this config and your agent starts working in 10 minutes."

Courses teach the tool. Operational products ARE the tool.

The vendor can commoditize knowledge about their platform. They can't commoditize your specific workflow packaged as a deployable product.

Rewriting all 16 products from educational to operational today.
