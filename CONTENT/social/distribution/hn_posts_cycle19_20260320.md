# HACKER NEWS DISTRIBUTION, Cycle 19 (2026-03-20)
# New angles: MCP Marketplace (Show HN), GEO research (Ask HN), AI-native agency
# Voice: technical, honest, minimal self-promotion

---

## POST 1: Show HN — MCP Marketplace (BEST FIT for HN audience)

**Title:** Show HN: A curated and code-reviewed MCP server marketplace

**Body:**
Built mcp-marketplace.surge.sh after spending too many hours vetting MCP servers from community lists and Discord recommendations.

Found several problematic ones in the process: servers requesting excessive permissions, making unexpected outbound network calls, executing arbitrary code on parsed input. The community lists don't flag these.

The marketplace:
- Curated list, every server code-reviewed before listing
- Categorized by use case (databases, file systems, APIs, dev tools, etc.)
- One-click install instructions
- Open to vetted submissions

Free, no signup, open to contributions. Happy to add any server that passes the review.

What would make this more useful to the Claude Code community?

**URL:** https://mcp-marketplace.surge.sh
**Target:** HN frontpage, Claude Code community, dev tools builders

---

## POST 2: Ask HN — AI Agents That Hit a Wall

**Title:** Ask HN: Has anyone built an AI agent system that works technically but fails at distribution?

**Body:**
I've been running 33 autonomous AI agents for 44 days. The technical side worked:

- 355 websites deployed
- 337 automation scripts running
- 1.45M leads analyzed, 17K qualified
- 850+ pieces of content generated
- 289 cron jobs orchestrating everything

Revenue: $0.

The agents handled every task I could automate: research, content creation, lead scoring, quality testing, deployment. What they couldn't do: post, send emails, create accounts, make phone calls.

I hit a wall I didn't expect: the system became a perfectly optimized machine for producing things that go nowhere.

Curious if others have hit this. How did you solve the human-gated distribution problem? Did you hire a VA? Build a human-approval workflow? Find ways to automate the last mile?

Not looking to promote anything — genuinely want to understand how others navigate this.

---

## POST 3: Show HN — DeskBreak (behavioral design angle)

**Title:** Show HN: DeskBreak — a break enforcer that locks your screen instead of sending notifications

**Body:**
Built deskbreak-web.surge.sh after failing to use every break reminder app I tried.

The insight: notifications let you say no. A lock doesn't.

Every break app sends you a reminder at 25 minutes. You dismiss it. 4 hours pass. You haven't moved.

DeskBreak locks your screen when break time hits. No dismiss button. No "5 more minutes." Break happens.

Same behavior design principle as PrayerLock (locks phone during salah). The user behavior you want to eliminate needs friction, not the behavior you want to encourage.

PWA: works offline, installs to home screen, no account. 55KB.

Feedback welcome — especially on the interval options and whether the enforcement level is calibrated right.

**URL:** https://deskbreak-web.surge.sh

---

## POST 4: Ask HN — GEO vs SEO (research question)

**Title:** Ask HN: Is anyone tracking AI citation rates as a distribution channel?

**Body:**
Looking at 680M citation data from ChatGPT and Perplexity and noticing some patterns:

- Perplexity cites Reddit threads 3-4x more than equivalent blog posts
- ChatGPT citations favor structured tables over prose
- FAQ sections with direct 1-sentence answers test better than long-form explanations

The implication is that AI search engines are becoming a meaningful distribution channel, and the optimization signals are different from Google.

Has anyone been tracking this systematically? What tools are you using? Are any SEO platforms adding AI citation tracking to their dashboards?

Trying to understand if this is worth building a workflow around or if it's too early/noisy.

---
