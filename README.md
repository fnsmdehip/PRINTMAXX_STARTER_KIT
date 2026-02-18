# PRINTMAXX Starter Kit (Local Repo)

Date: 2026-01-18

This folder is designed to be opened directly in **Cursor / VS Code / Claude Code / OpenCode**.
Your agent reads **MASTER_DOC/PRINTMAXX_MASTER_OPERATING_SYSTEM.md** and executes the To-Do list.

---

## 0) What’s inside

- `MASTER_DOC/PRINTMAXX_MASTER_OPERATING_SYSTEM.md` — single source of truth (To-Dos + stack + guardrails)
- `LEDGER/` — CSVs that control queues + tracking
  - `GEO_PROMPTS_200.csv`
  - `GEO_TRUTH_PAGES_10.csv`
  - `GEO_LONGTAIL_SLUGS_300.csv`
  - `FUNNEL_METRICS.csv` (tracking)
  - `leads.csv` (captures)
- `CONTENT/truth_pages/` — 10 Truth Pages in markdown
- `OPS/prompts/` — copy/paste prompts for agents
- `AUTOMATIONS/` — placeholders for Playwright + cron jobs

---

## 1) Your one job: run the agent using the prompt below

## Model routing (IMPORTANT)
Before any agent starts work, it must read:
- `OPS/MODEL_ROUTING_POLICY.md`

If the agent is on the wrong model for the task, it must **STOP immediately** and tell you what model to switch to.


### If using Claude Code / Cowork / OpenCode (recommended)
Copy/paste this prompt:

**PROMPT (RUN-01):**
You are my PrintMaxx execution agent.
Repo root is this folder.

Read:
1) MASTER_DOC/PRINTMAXX_MASTER_OPERATING_SYSTEM.md
2) LEDGER/*.csv
3) CONTENT/truth_pages/*.md

Goal: ship the MVP and start compounding distribution.

Rules:
- Do NOT loop. Max 8 steps per run.
- If blocked, write OPS/logs/BLOCKED.md with:
  (a) what failed
  (b) why
  (c) exact next manual step
- Work in small diffs. Keep everything runnable.
- Prefer deterministic automation (Playwright + cron) over flaky UI agents.

Tasks (in order):
1) Create a Next.js site under LANDING/printmaxx-site that renders truth pages:
   - /truth index
   - /truth/[slug] markdown rendering
2) Create a homepage with a lead capture form that appends to LEDGER/leads.csv
3) Create /magnet/stack-generator (simple form -> outputs a workflow plan)
4) Generate the first 25 long-tail pages into CONTENT/longtail_pages/ using LEDGER/GEO_LONGTAIL_SLUGS_300.csv
5) Update LEDGER/GEO_TRUTH_PAGES_10.csv and LEDGER/GEO_LONGTAIL_SLUGS_300.csv with published flags + last_updated

Deliverables:
- Running site locally (include commands)
- Files created/changed
- Short run log in OPS/logs/RUNLOG.md

---

## 2) How to run locally (Mac)

From repo root:
- `cd LANDING/printmaxx-site`
- `npm install`
- `npm run dev`

---

## 3) If you want to start posting today (no excuses)

Post 1x/day on X + 10 replies/day.
CTA: “Reply STACK and I’ll send the workflow generator.”

---

## 4) Safety / compliance baseline (non-negotiable)
- Affiliate disclosures: clear and simple near links (“affiliate link”).
- Don’t make fake testimonials.
- Don’t claim results you can’t substantiate.

---

## 5) Next run (RUN-02)
After RUN-01 ships the site, run the agent again with:
“Continue from OPS/logs/RUNLOG.md. Next: publish remaining Truth Pages + generate 50 more long-tails + draft newsletter sequence.”

