# DISTRIBUTION CYCLE 34 — HACKER NEWS + INDIEHACKERS
# Generated: 2026-03-29
# Cycle: 34 | Source: distribution_engine

---

## HACKER NEWS POST 1 — Show HN [HIGH PRIORITY]
**Asset:** claude-code-vs-opencode.surge.sh
**Type:** Show HN — timely comparison page

**Title:** Show HN: Claude Code vs OpenCode – honest comparison after OpenCode's HN #1

**Body:**
With OpenCode hitting #1 on HN this week, I put together an honest technical comparison for people trying to decide between them.

The summary: Claude Code wins for MCP-heavy agentic workflows. OpenCode wins for budget-conscious devs who want model flexibility.

The thing most comparisons miss: Claude Code's native MCP support means 100+ live integrations (Stripe, GitHub, databases, browser automation). OpenCode doesn't have this yet. For pure code editing tasks, the gap narrows significantly.

Neither is "dead." They serve different use cases.

https://claude-code-vs-opencode.surge.sh

I included a cost calculator and decision tree. Feedback on the framing appreciated.

---

## HACKER NEWS POST 2 — Show HN
**Asset:** cnsnt-web.surge.sh
**Type:** Show HN — privacy tool

**Title:** Show HN: cnsnt – local-first consent manager, AES-256 encrypted, zero server

**Body:**
Built cnsnt because every consent management tool I evaluated either cost $99+/mo or stored your consent records on their servers (which defeats the purpose for sensitive documents).

https://cnsnt-web.surge.sh

What it does:
- Creates consent records locally using AES-256-GCM + PBKDF2 key derivation
- Stores everything in browser IndexedDB — nothing leaves your device
- 11 built-in templates: GDPR, biometric, data processing, NDAs, research consent
- Generates signed audit-trail exports with HMAC integrity verification
- Cloud backup (encrypted before upload) via optional integration

Use case: legal/medical practices, researchers handling IRB consent, small businesses with GDPR requirements who can't afford enterprise tools.

Tech stack: React + Vite + Web Crypto API. No backend. The encryption logic is auditable.

Free for individuals. Feedback welcome before I add team features.

---

## HACKER NEWS POST 3 — Ask HN
**Asset:** Organic community / brand build
**Type:** Ask HN — genuine question for engagement

**Title:** Ask HN: How do you distribute side projects when you have no audience?

**Body:**
I've shipped 47 PWA apps and tools in 44 days (tracker: https://builders-ledger.surge.sh). Revenue: $0.

The technical side works. Distribution is the bottleneck.

I've tried: Reddit value posts (12K organic visitors, no conversions), HN Show HN (minor spikes, short-lived), cold email to founders (2.3% reply rate), Twitter (@printmaxxer, ~200 followers), SEO landing pages (ranking for some longtails, no traffic yet).

The consistent pattern: traffic isn't the problem. Conversion is.

Has anyone found a distribution channel that converts well for free tools / PWA apps? Not looking for "post on social media" advice — specifically interested in channels where the user has buying intent vs. just browsing.

---

## INDIEHACKERS POST 1 — Milestone post
**Asset:** builders-ledger.surge.sh + overall portfolio
**Type:** Milestone / transparency post

**Title:** Day 44: 47 apps live, $0 revenue — sharing everything I know about what's broken

**Body:**
44 days into building. 47 PWA apps and tools deployed. 500+ automation scripts running. 192,000 leads analyzed. $0 in revenue.

This isn't a failure post. It's an honesty post.

What I built works. What I haven't cracked is the last 10%: payment accounts, affiliate signups, getting things in front of buyers instead of browsers.

The blockers are embarrassingly human: creating a Gumroad account takes 15 minutes and I haven't done it. Connecting Stripe to 20 apps takes an afternoon. These are not technical problems.

What I learned in 44 days:

**Automation scales production, not distribution.** Having 500 scripts doesn't get you to $1. You still need to be in front of a human who will pay.

**The YC advice is right.** Don't sell AI access for $50/mo. Sell finished work for $5,000. The margin in the gap is real.

**$0 revenue doesn't mean 0 traction.** 12K organic Reddit visitors. Multiple tools ranking on page 1 for longtail keywords. 7 apps with real daily users. The audience exists. The checkout doesn't.

Tracking everything publicly: https://builders-ledger.surge.sh

What's your hardest distribution bottleneck right now?

---

## INDIEHACKERS POST 2 — Product showcase
**Asset:** claude-code-vs-opencode.surge.sh
**Type:** Tool showcase + discussion

**Title:** Built a comparison page for the Claude Code vs OpenCode debate — sharing the findings

**Body:**
The OpenCode launch triggered a bunch of comparisons that were either "both are great!" nothing-takes or "Claude Code is dead" hot takes.

I built a more structured comparison: https://claude-code-vs-opencode.surge.sh

Key finding that most comparisons miss: the MCP gap. OpenCode doesn't support MCP natively. Claude Code has 100+ MCP servers. For anyone building agentic workflows (not just code editing), this is a meaningful difference.

For pure code editing tasks on a budget, OpenCode is excellent and free.

For automated multi-agent systems that need to call live APIs, Claude Code still has the edge.

The page has a decision tree, cost calculator, and use-case breakdown.

IH audience would find this useful — lots of people here picking AI coding tools for side projects.

---

## POSTING SCHEDULE
- HN Post 1 (Claude Code vs OpenCode): POST MARCH 29 — trending, time-sensitive
- IH Post 1 (Day 44 milestone): POST MARCH 30 — best performing type for IH
- HN Post 2 (cnsnt Show HN): POST APRIL 1
- IH Post 2 (OpenCode comparison): POST APRIL 2
- HN Post 3 (Ask HN distribution): POST APRIL 3 — schedule for weekday morning 9 AM EST
