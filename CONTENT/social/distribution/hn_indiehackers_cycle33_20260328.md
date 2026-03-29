# DISTRIBUTION CYCLE 33 — HACKER NEWS + INDIEHACKERS
# Generated: 2026-03-28
# Cycle: 33 | Source: distribution_engine
# Assets: Claude Code ebooks, tools cluster, autonomous agent system

---

## HN POST 1 — Show HN: Free browser-based prayer tracker (no account, offline-capable)
**Type:** Show HN
**Asset:** prayerlock-web.surge.sh
**Best time:** March 28-29 (Eid timing — relevant to HN Muslim community)

**Title:** Show HN: PrayerLock – A browser-based Islamic prayer tracker with no accounts or downloads

**Body:**
PrayerLock is a simple prayer tracker I built for Ramadan: https://prayerlock-web.surge.sh

No account required, works offline, tracks your 5 daily salah and streak. Built with vanilla JS and localStorage, 55KB total.

Technical notes for HN:
- Pure client-side, no server
- LocalStorage for persistence
- Service worker for offline capability
- Designed to work on mobile browser without installation

Also built a Hilal/Eid tracker: https://ramadan-tracker.surge.sh

Both free, open to feedback. Particularly interested in: should I add export/backup, and is there a prayer time API integration that would be genuinely useful vs. over-engineered?

---

## HN POST 2 — Show HN: 47 free web tools built with Claude Code (ROI calc, PDF tools, stack comparison)
**Type:** Show HN
**Asset:** Tool cluster
**Best time:** March 30-31

**Title:** Show HN: 47 browser-based productivity tools I built in 44 days using Claude Code

**Body:**
I've been experimenting with using Claude Code to rapidly build web tools. 47 apps deployed in 44 days, all free, no accounts.

A few worth sharing:

**ROI Calculator:** https://roicalc.surge.sh
Plug in cost, expected revenue, timeline. Tells you payback period and if the investment makes sense.

**PDF Tools:** https://pdfmaxx.surge.sh
Merge/split/compress in browser. Nothing uploaded to a server.

**Stack Comparison:** https://stackmaxx.surge.sh
Compare tech stacks by use case based on real-world data.

**Cold Email Reference:** https://coldmaxx.surge.sh
Subject lines and sequence templates organized by use case.

**Prospect Research:** https://prospectmaxx.surge.sh
For B2B outbound.

Technical notes:
- All vanilla HTML/CSS/JS + React for the more complex ones
- Deployed to surge.sh (free tier)
- No backend, no database, everything client-side

What I learned: the bottleneck with AI-assisted development isn't the AI — it's spec quality. Vague prompt = vague app. A 2-page task spec outperforms "build me a tool that does X."

The architecture I settled on: Claude gets one task file per session, writes to filesystem, git after each working unit. Prevents the context drift problem.

Happy to discuss the architecture, the surge.sh limitations (CDN robots.txt issue with free tier is annoying), or the tooling setup.

---

## HN POST 3 — Ask HN: How do you structure Claude Code for long-running autonomous agents?
**Type:** Ask HN
**Asset:** Brand / Claude Code expertise
**Best time:** March 31

**Title:** Ask HN: What's your architecture for Claude Code agents that run unattended for hours?

**Body:**
I've been running Claude Code-based automation agents on cron for 44 days. The system has 33 agents, 524 scripts, and processes ~1.4M leads.

The biggest problems I've solved:
1. Context window management: agents write to files, return 1-line summaries
2. Auth failures: --api-key flag required for cron contexts (OAuth tokens expire silently)
3. Script orphaning: every script needs a named caller before it gets written

But I'm still struggling with:
- Stuck agent detection (how to tell if an agent hung vs. is just processing)
- Consistent output format across agents that weren't designed together
- Cost management when parallel agents hit the same task from different entry points

What architectures are people using for long-running Claude Code agents? Particularly curious about how others handle failure recovery.

---

## INDIEHACKERS POST 1 — Product teardown angle
**Type:** Milestone / honest post
**Asset:** General brand + tools
**Best time:** March 29-30

**Title:** Day 44 of building in public: 47 apps, 16 products, $0 revenue. Here's the honest breakdown.

**Body:**
I set a goal 44 days ago: build an autonomous revenue system using AI. Here's where I actually am.

**What's live:**
- 47 web apps deployed (streak trackers, productivity tools, comparison pages, AI tools)
- 16 digital products written and packaged (guides, playbooks, ebooks)
- 33 AI agents running daily (scrapers, analyzers, content generators)
- 192,700 leads qualified from 1.45M scraped
- 524 automation scripts

**Revenue: $0**

**Why:** I built the products. I didn't create the accounts to sell them. No Gumroad, no Stripe, no platform accounts.

This is the most useful lesson I can share: the product is never the blocker. The activation is.

I kept telling myself "I'll set up the accounts when the product is ready." 44 days later: 16 products ready, 0 accounts.

**What's different now:**
Accounts are being created. The first digital product goes live this week.

**What I'd tell someone starting today:**
1. Create your Gumroad/Stripe on day 1, before you build anything
2. Launch publicly from day 1, even if it's just a waitlist
3. Build one thing to $100 before building a second thing
4. Every build session should produce 3 tweets and 1 thread — content before code

The system works. The operator was the bottleneck.

Tools I built that are free for the community to use: roicalc.surge.sh, pdfmaxx.surge.sh, stackmaxx.surge.sh

---

## INDIEHACKERS POST 2 — Technical resource angle
**Type:** Value / tutorial
**Asset:** Claude Code Agent Bible ebook
**Best time:** March 31 - April 1

**Title:** The 5 things that killed my Claude Code automation system (and how I fixed each one)

**Body:**
After 44 days and 524 automation scripts, here are the failure modes that cost me the most time:

**1. OAuth tokens expiring silently**
Every `claude -p` call in a cron or background script needs `--api-key $ANTHROPIC_API_KEY`. OAuth tokens expire after hours/days and fail silently with no log output. Costs you days of automation dead-time before you notice.

**2. Scripts with no caller**
I hit 524 scripts. Most of them are called by nothing. Pure dead weight. The rule I wish I'd had from day 1: before writing a script, name the cron entry or caller that will run it.

**3. Context window filling with tool results**
Claude starts contradicting itself around 60% context usage. The fix: subagents write to files, return 1-line summaries to the main agent. Never dump large tool results into the main conversation.

**4. Building infrastructure before validating revenue path**
I built 33 agents to process leads before creating the Gumroad account to sell to them. RBI (Research, Backtest, Implement) before building anything.

**5. Parallel agents hitting permission blocks**
Background agents with `run_in_background: true` get file write permissions auto-denied in some contexts. Use foreground agents for anything that needs to write files.

I wrote a full breakdown of my Claude Code architecture in a guide called the Claude Code Agent Bible. DM me "bible" if you want a copy.

---

## DEVTO/MEDIUM POST — Technical article
**Asset:** Claude Code expertise / tools
**Best time:** April 1-3

**Title:** How I Deployed 47 Web Apps in 44 Days Using Claude Code (Architecture + Lessons)

**Outline:**
1. The setup: Claude Code + surge.sh + cron
2. The task spec pattern that actually works
3. The 5 failure modes and their fixes
4. Tool examples: roicalc.surge.sh, pdfmaxx.surge.sh, etc.
5. What I'd do differently
6. The $0 problem: infrastructure vs activation

**Target:** dev.to (primary), Medium (cross-post), Hashnode
**SEO angle:** "claude code automation", "deploy apps with AI", "ai-assisted development"
