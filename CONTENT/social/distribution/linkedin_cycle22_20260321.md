# LinkedIn Posts — Cycle 22 — 2026-03-21

---

## POST 1: Fitness Streak Apps — Builder Angle

I shipped 5 fitness habit tracker apps in 48 hours.

No accounts. No subscriptions. No ads.

Each one does exactly one thing:
- Pushup Streak: log daily reps + visual streak
- Plank Streak: timer + streak
- Yoga Streak: daily practice tracker
- Cycling Streak: daily ride tracker
- HIIT Streak: daily session logger

Here's what I learned shipping fast:

**1. Friction is the enemy of habits.** Every signup screen is an 8-15% drop in retention. Remove the login entirely and you're ahead of most apps.

**2. Single-purpose wins on mobile.** When someone opens a habit app, they want to log one thing and leave. Multi-feature apps fight against this.

**3. Web apps ship in hours, iOS apps ship in weeks.** For testing market demand, web-first beats native every time.

All 5 are live as free web apps. Building the native iOS versions for the ones that get traction.

What habit tracking approaches have you seen actually work for your teams or audience?

---

## POST 2: Tools — The Overthinking Problem

We over-engineer tools.

Invoice generator: most freelancers need 4 fields and a PDF download.

Prompt library: most developers need search, tags, and a share link.

Study tracker: most students need a timer, a subject label, and a streak counter.

I built all three.

No accounts. Free. Each one does its one job well.

The trap is adding features to justify charging. But free + focused + frictionless is a legitimate strategy — especially when your monetization comes from the attention and trust you build, not the product itself.

invoiceforge.surge.sh | promptvault.surge.sh | studylock.surge.sh

What's a tool you use weekly that does way more than you need?

---

## POST 3: Framer vs Webflow — For Founders and Builders

If you're building a landing page for your product, this matters:

**Framer:**
- Build a beautiful landing page in 2-4 hours
- Free tier that lets you publish immediately
- AI-native: generate full sections in seconds
- Better for indie builders and SaaS marketing pages

**Webflow:**
- More control over the underlying code
- Better for complex client sites with CMS needs
- $23+/month before you publish anything
- Steeper learning curve

My honest take after building in both:

If you're a founder testing a new product → use Framer. Ship in hours, not days.

If you're a web designer building for clients with ongoing content needs → use Webflow.

The decision comes down to: are you testing demand (Framer) or building infrastructure (Webflow)?

Full comparison: framer-vs-webflow.surge.sh

---

## POST 4: Claude Code vs OpenCode — For Engineering Leaders

OpenCode launched today (685 HN points). It's an open-source AI coding agent that competes with Claude Code.

Why this matters for engineering leaders:

**OpenCode's case:**
- Model-agnostic: use GPT-4, Gemini, or local Llama
- Open-source: your team can audit, fork, and customize
- Community-driven contributions

**Claude Code's case:**
- Deep Anthropic integration (Opus reasoning models)
- MCP server ecosystem built in
- Better for teams already in the Anthropic stack

This isn't a vs. fight — they serve different teams. But if your org is running AI coding tools at scale, knowing the tradeoffs matters now before you're locked in.

Full breakdown: claude-code-vs-opencode.surge.sh
