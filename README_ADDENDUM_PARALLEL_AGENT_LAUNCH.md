# README ADDENDUM — PARALLEL AGENT LAUNCH (Sonnet 4.5) ✅

## Goal
Run multiple Claude Code instances in parallel to execute PrintMaxx faster **without merge conflicts or looping**.

## Non‑negotiable rules (anti‑loop / anti‑chaos)
- **One agent = one folder ownership.** No two agents edit the same folder.
- **Max 8 steps per run.** If not done, STOP and write a handoff note.
- **If blocked > 10 min** → write `OPS/logs/BLOCKED_<AGENT>.md` and stop.
- **Minimal working first.** No refactors unless required.

---

# RUN PLAN (launch these agents in parallel)

## Agent A — Site MVP (Truth pages + lead capture)
**Folder ownership:** `LANDING/printmaxx-site/`  
**Task:** Build the site skeleton and make it run locally.

**PROMPT (Agent A):**
You own only `LANDING/printmaxx-site/`.  
Implement:
1) Next.js app (TypeScript)
2) `/truth` index page (lists truth markdown files)
3) `/truth/[slug]` page renders markdown from `CONTENT/truth_pages/`
4) Homepage lead capture form that appends to `LEDGER/leads.csv`

Rules:
- Do NOT touch longtail generation.
- Do NOT touch master docs.
- Max 8 steps.
- If blocked: write `OPS/logs/BLOCKED_A.md`.

Deliverables:
- exact commands to run locally
- `OPS/logs/RUNLOG_A.md`

---

## Agent B — Longtail Page Batch Generator (25 pages only)
**Folder ownership:** `CONTENT/longtail_pages/`  
**Task:** Generate first 25 long-tail pages as markdown.

**PROMPT (Agent B):**
You own only:
- `CONTENT/longtail_pages/`
- optionally update `LEDGER/GEO_LONGTAIL_SLUGS_300.csv` notes column (do NOT reorder rows)

Generate 25 markdown pages using this template:
- Title
- Quick Answer (3–6 bullets)
- Step-by-step (6–10 steps)
- Comparison table (at least 5 rows)
- FAQ (4 Qs)
- Internal links: link back to `/truth` and 1 relevant truth page slug

Use `LEDGER/GEO_LONGTAIL_SLUGS_300.csv` as the source.
Output files into `CONTENT/longtail_pages/`.

Rules:
- Do NOT edit the site.
- Max 25 pages per run.
- If blocked: write `OPS/logs/BLOCKED_B.md`.

Deliverables:
- 25 files created
- `OPS/logs/RUNLOG_B.md`

---

## Agent C — Warmup Ops System (ledger + SOPs)
**Folder ownership:** `OPS/agents/` and `OPS/prompts/`  
**Task:** Create the warmup + account test SOPs and ledger rows.

**PROMPT (Agent C):**
You own only:
- `OPS/agents/`
- `OPS/prompts/`
- `LEDGER/` (you may CREATE new CSVs, but do NOT modify existing CSV headers)

Create:
1) `OPS/agents/WARMUP_PROTOCOL_X.md` — 7-day schedule (Day 1–7)
2) `OPS/agents/WARMUP_PROTOCOL_TIKTOK.md` — 7-day schedule
3) `LEDGER/ACCOUNT_FARM.csv` with columns:
   date_created,platform,handle,email,phone_verified,proxy_method,device_method,cohort,status,notes
4) `OPS/prompts/WARMUP_AGENT_PROMPT.txt` — a prompt I can reuse to run warmups as a checklist.

Cohorts must exist:
- A = normal browser + clean IP
- B = proxy
- C = anti-detect + proxy

Rules:
- Don’t touch site code.
- No automation scripts yet; SOP only.
- Max 8 steps.
- If blocked: write `OPS/logs/BLOCKED_C.md`.

Deliverables:
- the two SOPs
- ACCOUNT_FARM.csv
- `OPS/logs/RUNLOG_C.md`

---

## Agent D — Email + Offer Copy (minimal)
**Folder ownership:** `EMAIL/`  
**Task:** Draft the first working email sequence + offer page copy.

**PROMPT (Agent D):**
You own only `EMAIL/`.

Create:
- `EMAIL/sequence_v1.md` with:
  Welcome email
  Value email #1
  Value email #2
  Soft pitch
  Hard pitch
- `EMAIL/offer_copy_v1.md` for the $29/mo offer

Rules:
- No code changes.
- Max 8 steps.
- If blocked: write `OPS/logs/BLOCKED_D.md`.

Deliverables:
- both files
- `OPS/logs/RUNLOG_D.md`

---

# Integration step (after all agents finish)

## Agent M — Merge + sanity check
**Folder ownership:** READ-ONLY across repo except logs.  
**Task:** Verify everything is coherent + runnable.

**PROMPT (Agent M):**
Read:
- OPS/logs/RUNLOG_A.md, B, C, D
- LANDING/printmaxx-site
- EMAIL outputs
- longtail pages

Verify:
- Site starts locally
- Truth pages render
- lead capture appends to CSV
- no missing paths

Then write:
- `OPS/logs/INTEGRATION_REPORT.md`
with:
1) what’s shipped
2) what’s next
3) what to run tomorrow

Rules:
- Do not refactor code.
- Only minimal fixes if absolutely required.

---

# Stop condition / loop prevention
If any agent repeats the same error twice:
- STOP
- write BLOCKED file
- do not keep retrying

---

# Next run (tomorrow)
Once the MVP is live:
- generate 50 more longtails
- publish remaining truth pages
- begin daily posting schedule
