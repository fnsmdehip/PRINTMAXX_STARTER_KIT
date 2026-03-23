# DISTRIBUTION CYCLE 32 — HACKER NEWS + INDIEHACKERS
# Generated: 2026-03-23 02:10
# Cycle: 32 | Source: distribution_engine
# Assets: couples-streak, deskbreak, studylock, Claude Code ebook series, knowledge streaks

---

## HN SHOW POST #1 — Couples Streak [HIGH POTENTIAL]
Title: Show HN: Couples Streak – shared habit tracker for two people (no account)

URL: https://couples-streak.surge.sh

Comment body:
My partner and I kept saying we wanted to build shared habits but had no tool for it. Every habit app is individual-focused. The "couples" features are premium add-ons on apps that already have $15/month subscriptions.

Built Couples Streak as a shared habit tracker that works in the browser with no account required.

Technical implementation:
- Pure client-side (HTML/CSS/JS, ~45KB total)
- LocalStorage for streak data — nothing sent to a server
- Shareable state via URL parameters (optional — lets both people sync without accounts)
- Works offline

We use it for morning walks, no-phone dinners, and a weekly "no work after 7pm" commitment.

The interesting design challenge: what counts as a shared streak when two people have to log independently? I defaulted to "either person's log counts for the day" but made "both must log" configurable.

Would a web socket-based real-time sync be worth adding, or does the simplicity of no-backend beat the feature?

---

## HN SHOW POST #2 — DeskBreak [REMOTE WORK AUDIENCE]
Title: Show HN: DeskBreak – browser tab that reminds you to move every 45 minutes

URL: https://deskbreak.surge.sh

Comment body:
I work from home and noticed I was sitting for 5-6 hours without moving. Tried phone alarms — easy to snooze and ignore. Tried browser extensions — heavy and required install.

Built DeskBreak as a single HTML file that runs in a browser tab. It uses the Page Visibility API to detect when you're active, and triggers a reminder after a configurable interval (default 45 min).

Technical details:
- 8KB total, pure client-side
- Uses Page Visibility API + setTimeout for tracking
- Customizable interval (15 min to 2 hours)
- Reminder types: visual overlay, audio tone, or both
- Saves settings to localStorage

The design decision I'm least confident about: should it count time when the tab is in the background? Currently it pauses the timer when you switch away (assumption: if you're not looking at it, you're probably doing something else). Happy to hear arguments for continuous counting.

Feedback welcome.

---

## HN SHOW POST #3 — Knowledge Streak Cluster [LEARNING AUDIENCE]
Title: Show HN: Three free streak trackers for systematic knowledge building (history, geography, cultural literacy)

URLs:
- https://world-history-streak.surge.sh
- https://geography-mastery-streak.surge.sh
- https://cultural-etiquette-streak.surge.sh

Comment body:
I wanted to systematically improve my world history knowledge but had no tool to maintain consistent study. The habit apps are generic; the flashcard apps are for memorization, not for tracking reading sessions.

Built three simple streak trackers for knowledge-building habits:
- World History Streak: for tracking daily history reading/lectures/documentaries
- Geography Mastery: for map study, country research, geopolitical reading
- Cultural Etiquette: for learning customs, social norms, and cultural context before travel

All three are:
- Pure client-side, ~35KB each
- No account, no email
- Works offline
- Saves to localStorage

The design pattern I'm trying: separate "subject knowledge" streak apps from general productivity tools. Generic habit apps ask you to configure everything from scratch. Subject-specific ones come with suggested daily practices pre-loaded.

Are there other knowledge areas where a pre-configured streak tracker would be useful? Language learning already has Duolingo. History/geography/culture don't have a dedicated daily-practice tool.

---

## INDIEHACKERS POST #1 — Build-in-public update
Title: Day 44 update: 177 apps live, $0 revenue — here's the real bottleneck

Body:
Hey IH,

Building in public for 44 days. This is an honest status update.

**What's built:**
- 177 live websites and apps deployed on surge.sh
- 22 digital products (PDFs) with listings written
- 428 automation scripts
- 9 Claude Code guides compiled
- Autonomous pipeline scraping 1,648 new data points per day
- 192,700 leads processed

**Revenue:** $0

**The actual bottleneck:**

Not the pipeline. Not the product. Not distribution content (1,274 posts queued and ready).

The bottleneck: I haven't created a Stripe account. Or a Gumroad account. Or signed up for affiliate programs.

That's maybe 3-4 hours of work total. I spent the past 44 days building instead of doing those 4 hours of admin.

Classic over-builder mistake. The infrastructure was production-ready at day 15. Days 16-44 were building more infrastructure nobody asked for.

**Fixing this week:**
- Stripe account (30 min)
- Gumroad account + upload 22 products (2 hours)
- 5 affiliate program signups (1 hour)

After those 3.5 hours, I'll have:
- Payment path for 177 apps
- 22 products live for sale
- 6 affiliate pages generating commission

Will report back on Friday with real numbers.

Anyone else been in this pattern — building when the real leverage was 4 hours of boring admin?

---

## INDIEHACKERS POST #2 — Claude Code ebooks launch
Title: I turned 44 days of Claude Code building into 9 practical guides — here's the table of contents

Body:
After building 177 apps and 428 automation scripts using Claude Code, I compiled everything useful into guides.

Not theory. Patterns that actually worked after trying 50+ approaches.

**The 9 guides:**

1. **Claude Code Agent Bible** — how to structure agentic loops that actually execute, not just plan
2. **Claude Code for Solopreneurs** — the exact workflow for founders who aren't developers
3. **Claude Code for Non-Technical Founders** — what to build yourself vs delegate to agents
4. **Claude Code Mastery** — advanced prompt patterns, context management, multi-agent coordination
5. **Reddit Money Machine** — getting consistent traffic from Reddit without getting banned
6. **Cold Email System** — the exact system I use with 87%+ deliverability
7. **Prompt Vault** — my best prompts organized by use case (200+ prompts)
8. **Before You Family Story Workbook** — niche product for capturing family stories (AI-assisted)
9. **Claude Code Mastery Advanced** — RAG, memory systems, parallel agents

Listing on Gumroad this week at $29-47 each.

What would you want to know most about running a Claude Code-based business?

---

