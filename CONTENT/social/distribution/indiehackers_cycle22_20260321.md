# IndieHackers Posts — Cycle 22 — 2026-03-21

---

## POST 1: Show IH — 5 fitness streak apps shipped in 48 hours, zero backend

**Category:** Projects / Show IH

**Body:**
Shipped 5 fitness streak trackers this week. Web apps, no login, no backend, no ads.

- Pushup Streak (pushup-streak.surge.sh)
- Plank Streak (plank-streak.surge.sh)
- Yoga Streak (yoga-streak.surge.sh)
- Cycling Streak (cycling-streak.surge.sh)
- HIIT Streak (hiit-streak.surge.sh)

**The hypothesis I'm testing:** focused single-purpose apps retain better than multi-feature trackers because they remove all friction from the primary action.

**Stack:** vanilla JS, localStorage for streak data, surge.sh for hosting. Zero recurring cost.

**Next step:** wire RevenueCat to the iOS versions once I see which ones get traction on web.

What's your experience with focused vs. feature-rich for habit apps? Curious if anyone has retention data.

---

## POST 2: Show IH — Free invoice generator (no watermarks, no account)

**Body:**
Built invoiceforge.surge.sh after spending 20 minutes hunting for a free invoice generator that didn't want my email.

Four fields. PDF download. Done.

No watermark, no free tier limit, no signup.

Stack: HTML + JS + html2pdf.js. Deployed to surge in 10 minutes.

The angle: "free tool" as top-of-funnel. SEO for "free invoice generator no watermark" and similar queries. Monetization comes from trust → upsell to premium features if there's demand.

---

## POST 3: Show IH — Prompt Vault for LLM prompts

**Body:**
I kept losing my best Claude/GPT/Gemini prompts in random notes. Built a fix.

promptvault.surge.sh — save, tag, and share prompts. No account.

The real insight: the best prompts for any workflow take time to engineer. The ones you don't save are the ones you re-engineer from scratch six times.

This is basically a tagged library with a share link. Simple. Free.

Curious if anyone else has a workflow for prompt management — what am I missing?

---

## POST 4: IH Discussion — Claude Code vs OpenCode

**Category:** Discussion

**Title:** OpenCode launched today — does this change your AI coding tool choice?

**Body:**
OpenCode hit 685 HN points today. It's an open-source alternative to Claude Code — model-agnostic, runs in terminal, community-driven.

I built a comparison page after testing it: claude-code-vs-opencode.surge.sh

Two camps emerging:

**OpenCode crowd:** developers who want model flexibility, open-source auditability, and community contributions. Don't want to be locked to Anthropic.

**Claude Code crowd:** developers who want Anthropic's reasoning models (Opus), MCP server ecosystem, and deeper API integration.

I'm in the Claude Code camp currently but keep an eye on OpenCode.

Where does IH land on this? And does anyone have a strong case for one over the other that I'm missing in the comparison?
