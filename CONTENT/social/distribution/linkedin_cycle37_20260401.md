# LinkedIn Distribution — Cycle 37 — 2026-04-01

---

## POST 1 — TruthScope thought leadership

**Title / Hook:** I built an app marketed as a "physiological stress analyzer" because "lie detector" would have been technically accurate but scientifically irresponsible.

Here's the distinction that actually matters for anyone building health or biometric products:

**The science:**
Modern iPhones can measure contact PPG (photoplethysmography) via the rear camera and flashlight with >99.6% accuracy vs ECG gold standard. From that signal you extract HRV metrics — RMSSD, LF/HF ratio — the same cardiovascular channels a clinical polygraph measures.

When someone lies, sympathetic activation typically raises HR 5-15 BPM and drops HRV. Real, measurable signal.

**The limitation:**
Anxiety produces identical signals. Fear, embarrassment, caffeine, and exercise produce identical signals. The hardware measures arousal, not deception. Deception is a subset of arousal under specific conditions.

**The product decision:**
Shipping as "lie detector" would have driven 10x more installs. The framing is irresistible. It would also be misleading about a health metric people might actually misuse.

Shipped as "TruthScope — Physiological Stress Analyzer."

The lesson for product builders: the most defensible long-term position is accurate marketing, even when accurate marketing is less compelling than the alternative.

Especially for biometric/health apps where misrepresentation has real downstream consequences.

---

## POST 2 — Solopreneur systems post

**I built 398 live web apps and 22 digital products with 1 person and 33 autonomous agents.**

The revenue after 57 days: $0.

This isn't a failure story. It's a specific type of bottleneck I want to name clearly because I see other builders hit it.

The system generates, deploys, analyzes, and distributes autonomously. 33 agents running daily batch processing. 1,454,245 leads analyzed. 529 automation scripts.

The blocker: Stripe account (10 min). Gumroad account (30 min). Amazon Associates signup (15 min).

I've been "about to" create these accounts for 3 weeks.

This is what I'm calling automation dysmorphia: when you've automated 95% of your workflow, the remaining 5% of human-required tasks feel disproportionately disruptive. The context switch cost feels high. So you keep deferring trivial tasks that are actually P0 revenue blockers.

The recognition is useful. The 45 minutes of account creation would have unlocked the revenue pipeline weeks ago.

What's the equivalent in your workflow — the obvious thing you keep deferring?

---

## POST 3 — Claude Code authority post

**9 Claude Code guides, ready to sell, blocked by a 10-minute account creation.**

For anyone in the Claude Code / AI developer tools space — I've been deep in agentic development for the past 57 days. What I've built:

1. Claude Code Agent Bible — multi-agent system design patterns
2. Claude Code for Solopreneurs — full-stack build workflow
3. Claude Code for Non-Technical Founders — ship product without engineering background
4. Claude Code for Content Creators — automated content operations
5. Claude Code Mastery — advanced patterns and edge cases
6. Cold Email System — Claude-powered outreach automation
7. Reddit Money Machine — systematic community distribution
8. Prompt Vault — 400+ tested prompts organized by use case

Each one is the distillation of building 398 apps and running 33 agents.

They're in limbo until I get the Gumroad account live. If any of these look useful for your team or audience, comment and I'll send directly.

The irony of an AI automation expert having an account-creation bottleneck is not lost on me.

---

## POST 4 — B2B / agency angle

**The website builder decision tree most agencies get wrong:**

After deploying 398 sites, here's what I actually use and why:

STATIC CONTENT (landing pages, docs, demos):
surge.sh — 5-second deploy, $0 cost, unlimited traffic. No reason to pay for Webflow when you don't need a CMS.

CMS-DRIVEN (blog + landing + marketing):
Webflow — worth the premium only when you have non-developer editors updating content regularly.

DESIGN-FORWARD (agency portfolios, product launches):
Framer — best-in-class visual output, but vendor lock-in is real and export is messy.

The mistake I see consistently: agencies defaulting to Webflow for clients who just need static HTML. The $39/mo CMS plan is fine for large clients. It's overkill for 80% of SMB sites.

Full comparison with decision tree criteria: website-builders-compared.surge.sh

What's the builder your team defaults to and why?
