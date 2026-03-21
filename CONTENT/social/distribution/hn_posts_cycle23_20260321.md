# Hacker News Posts — Cycle 23 — 2026-03-21

---

## POST 1 — Show HN: SEMrush vs Ahrefs comparison page I built (with free alternatives)

**URL:** semrush-vs-ahrefs.surge.sh

**Comment to post:**
I was paying $330/mo running both SEMrush and Ahrefs at the same time for about 4 months. Cut that down to one tool plus a couple free alternatives. Built this page to document what I found.

The comparison covers: keyword research quality, backlink database depth and accuracy, competitor traffic analysis, site audit features, position tracking, and pricing at each tier (including what's actually in each plan vs what's gated).

Main finding: they're not redundant. Ahrefs wins for backlink research and Link Intersect. SEMrush wins for competitor traffic analysis and audit depth. If you're a solo SEO, you almost certainly don't need both.

Free alternatives I actually tested are on the page too: Ahrefs Webmaster Tools (for your own site), GSC, Ubersuggest, Moz Free.

Built the page because every "SEMrush vs Ahrefs" article I found was either SEMrush-affiliated, Ahrefs-affiliated, or hadn't been updated since 2022.

---

## POST 2 — Show HN: Quran, Gita, and Sikh streak tracker apps — free, offline, no accounts

**URLs:**
- quran-streak-landing.surge.sh
- gita-streak-landing.surge.sh
- sikh-streak-landing.surge.sh

**Comment to post:**
I built 3 single-purpose religious practice streak trackers. Each one does exactly one thing: track whether you did your daily practice and show you the streak history.

Technical details:
- PWA (Progressive Web App) — installable on home screen, works offline after first load
- All data stored in localStorage — nothing leaves the device
- No backend, no accounts, no ads, no analytics
- Build time per app: about 3 hours each once I had the template

The design principle is the same one I applied to some fitness streak apps I built earlier: habit apps fail at the habit layer first. The more friction between "I want to log this" and "it's logged," the more likely you skip. So each app is one page, one button, one calendar view.

Works for daily Quran reading, Bhagavad Gita chapter tracking, and Sikh Nitnem practice.

Open to feedback from anyone in these communities on whether the UX matches how people actually want to track practice.

---

## POST 3 — Show HN: ColdMaxx — free cold email outreach tool

**URL:** coldmaxx.surge.sh

**Comment to post:**
The barrier for learning cold email is mostly pricing. Every real tool starts at $37-97/mo and most of that is for warmup infrastructure and deliverability features that don't matter until you're already sending at scale.

ColdMaxx is a free-to-start outreach tool with the core workflow: upload list, build sequence, track replies.

What's in it: list management, multi-step sequence builder, open/click/reply tracking, basic spam word checker.

What's missing currently: email warmup (you'd use a separate tool like Mailreach or Instantly warmup-only), advanced A/B testing, inbox rotation at 50+ account scale.

The intended user is someone who wants to send their first 500-2000 cold emails and figure out what actually works before paying $100/mo for tooling.

Stack is straightforward: standard web stack, nothing exotic. Feedback on broken features or missing functionality is useful.

---

## POST 4 — Show HN: PDFMaxx — browser-based PDF tools (merge, compress, convert)

**URL:** pdfmaxx.surge.sh

**Comment to post:**
I kept using online PDF tools that either have file size limits, require account creation, or are clearly running your files through their servers (which matters for anything sensitive).

PDFMaxx runs entirely in the browser. Merge, compress, split, convert — all handled client-side with PDF.js and pdf-lib. Files never leave your machine.

Current tools:
- Merge: combine multiple PDFs in any order
- Compress: reduce file size (lossy and lossless options)
- Split: extract pages or ranges
- Convert: PDF to images (PNG/JPG per page)
- Reorder: drag-and-drop page reordering before export

Built this primarily for my own use when preparing documents for client work. Figured the "no upload, no account, runs offline" angle was worth releasing.

Known limitation: very large PDFs (100+ MB) can be slow on lower-end hardware since it's all in-browser processing. That's a JS/WebAssembly constraint, not a fixable bug.
