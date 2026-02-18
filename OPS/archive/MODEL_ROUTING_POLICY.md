# MODEL ROUTING POLICY (PrintMaxx) — Haiku vs Sonnet vs Opus

Purpose: maximize throughput per dollar and prevent agents from wasting time by using the wrong model.

---

## One-line rule
- **Haiku = clerical / formatting / packaging**
- **Sonnet = 90% execution (code + bulk generation)**
- **Opus = conversion-critical + compliance-critical + final gates**

If you’re not the right model for the job: **STOP** and ask the operator to switch models.

---

## STOP CHECK (agents must run this before doing any work)
**If your current model is not appropriate for the assigned task, do NOT proceed.**
Instead output:

1) **Current model:** <Haiku/Sonnet/Opus/Unknown>
2) **Assigned task:** <1 sentence>
3) **Mismatch reason:** <1 sentence>
4) **Correct model:** <Haiku/Sonnet/Opus>
5) **What to do next:** “Switch me to <model> and re-run with the same prompt.”

---

## Task → Model mapping

### Use OPUS for (high leverage, low volume)
- Offer + positioning (“money sentence”, tiers, pricing)
- Compliance-critical language (FTC, affiliate disclosures, claims)
- Cold email angles (core framing, persuasion, objection handling)
- Final polish on top 3–10 Truth Pages
- Kill/scale thresholds for email ops automation (guardrails)
- Any “final decision” that affects revenue or risk

### Use SONNET for (factory work)
- Code + repo changes (Next.js, Playwright, cron, connectors)
- Bulk content generation (25–200 pages/posts at a time)
- Lead magnet implementation after spec exists
- GEO execution (template pages, interlinking, schema)
- Data cleaning + analysis that requires scripting

### Use HAIKU for (clerical / packaging)
- CSV edits, column reshaping, renaming, formatting
- Turning notes into structured tables/checklists
- Doc cleanup, dedupe, tightening prose
- Creating placeholders / boilerplate docs
- Copying content into “ready-to-upload” layouts

---

## “Gold Spec then Factory” workflow
Best practice:

1) **Opus writes the Gold Spec** (what to build + the exact outputs)
2) **Sonnet implements at scale**
3) **Haiku packages + cleans + exports**

This prevents expensive models doing grunt work.

---

## Anti-loop guardrails (mandatory)
- Max **8 steps** per run
- If a failure repeats **twice** → STOP and write `OPS/logs/BLOCKED.md`
- Don’t edit the same file more than **2 times** in a single run
- Every run must output **at least one artifact** (file) or STOP

---

## Example “model mismatch” cases
- Haiku asked to build a Next.js site → STOP (needs Sonnet)
- Sonnet asked to write final compliance/offer copy → STOP (needs Opus)
- Opus asked to generate 200 long-tail pages → STOP (needs Sonnet)
