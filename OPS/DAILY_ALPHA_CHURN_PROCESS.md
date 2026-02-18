# Daily Alpha Churn Process

**Purpose:** Convert approved alpha into daily revenue actions. Stop hoarding research. Start executing.
**Owner:** Run automatically at session start + as a ralph loop overnight.
**Metric:** Alpha Utilization Rate (target: 80% of APPROVED utilized within 14 days)

---

## The Problem This Solves

835 alpha entries collected. 163 approved. Near zero converted to ops. $0 revenue from research.

The pipeline is: COLLECT -> REVIEW -> APPROVE -> ... -> nothing.

This process adds the missing steps: APPROVE -> PRIORITIZE -> TASK -> EXECUTE -> TRACK -> REVENUE.

---

## Daily Process (Run Every Session Start)

### Step 1: Scan Approved + Not Utilized (2 minutes)

```bash
# Scan ALPHA_STAGING.csv for APPROVED entries without utilization
# Look for entries where utilization_status is NOT_UTILIZED or empty
grep "APPROVED" LEDGER/ALPHA_STAGING.csv | grep -v "UTILIZED\|IN_PROGRESS\|REVENUE_GENERATED"
```

Priority order for selection:
1. HIGHEST ROI + APPROVED + NOT_UTILIZED (pick from these first)
2. HIGH ROI + APPROVED + NOT_UTILIZED
3. Any APPROVED + NOT_UTILIZED

### Step 2: Pick Top 3 Alpha for Today (1 minute)

Select 3 alpha entries based on:
- ROI potential (HIGHEST first)
- Effort level (LOW effort first for quick wins)
- Dependencies (can we start TODAY without waiting for anything?)
- Revenue proximity (how many steps to first dollar?)

**Selection matrix:**

| Priority | ROI | Effort | Dependencies | Pick? |
|----------|-----|--------|-------------|-------|
| 1st | HIGHEST | LOW | None | ALWAYS |
| 2nd | HIGHEST | MEDIUM | None | YES |
| 3rd | HIGH | LOW | None | YES |
| 4th | HIGHEST | LOW | 1 blocker | MAYBE (if blocker is quick) |
| Skip | Any | HIGH | Multiple | NO (backlog) |

### Step 3: Convert Alpha to Daily Tasks (5 minutes per alpha)

For each selected alpha, create a concrete task:

**Task format:**
```
TASK: [Specific action verb] [Specific deliverable]
ALPHA: [Alpha ID]
TIME_ESTIMATE: [30min / 1hr / 2hr / 4hr]
DONE_WHEN: [Specific measurable outcome]
FIRST_STEP: [The literal first thing to do]
```

**Examples:**

```
TASK: Set up Visualping monitoring for 20 competitor pages
ALPHA: ALPHA319
TIME_ESTIMATE: 1hr
DONE_WHEN: 20 competitor URLs added to Visualping with email alerts configured
FIRST_STEP: Go to visualping.io and create free account

TASK: Purchase 3 cold email domains and start warmup
ALPHA: ALPHA282, ALPHA285
TIME_ESTIMATE: 2hr
DONE_WHEN: 3 domains purchased, DNS configured, warmup tool connected
FIRST_STEP: Go to Namecheap and buy 3 domains similar to main brand

TASK: Generate first AI persona with Leonardo.ai
ALPHA: ALPHA222, ALPHA231
TIME_ESTIMATE: 2hr
DONE_WHEN: 10 consistent character images generated, reference sheet saved
FIRST_STEP: Subscribe to Leonardo.ai ($12/mo) and generate base character
```

### Step 4: Execute Tasks (bulk of day)

Do the tasks. Ship. Don't plan more.

### Step 5: Update Utilization Status (2 minutes)

After executing, update ALPHA_STAGING.csv:
- Change `utilization_status` from `NOT_UTILIZED` to `IN_PROGRESS` or `UTILIZED`
- Add `utilization_date` with today's date
- Add `utilization_notes` with what was done

### Step 6: Log Daily Alpha Churn (1 minute)

Append to `LEDGER/ALPHA_CHURN_LOG.csv`:

```csv
date,alpha_ids_attempted,alpha_ids_completed,tasks_created,tasks_completed,revenue_generated,notes
2026-02-10,"ALPHA319,ALPHA282,ALPHA222",ALPHA319,3,1,0,Visualping set up. Domains purchased but warmup pending.
```

---

## Weekly Alpha Utilization Report (Run Every Monday)

### Metrics to Track

| Metric | Target | How to Calculate |
|--------|--------|-----------------|
| **Alpha Utilization Rate** | 80% within 14 days | (UTILIZED + IN_PROGRESS + REVENUE_GENERATED) / APPROVED |
| **Days to Utilization** | < 14 days | avg(utilization_date - approved_date) |
| **Revenue per Alpha** | > $0 for 20% of utilized | sum(revenue from utilized alpha) / count(utilized) |
| **Daily Churn Rate** | 3+ per day | avg(alpha_ids_completed per day) |
| **Pending Backlog** | Decreasing | count(APPROVED + NOT_UTILIZED) |
| **ENGAGEMENT_BAIT Conversion** | 5+ posts/day | count(EB entries converted to posts today) |

### Report Format

```
ALPHA UTILIZATION REPORT - Week of [DATE]

APPROVED INVENTORY: [X] total
  UTILIZED:           [X] ([X]%)
  IN_PROGRESS:        [X] ([X]%)
  NOT_UTILIZED:       [X] ([X]%) <-- this number should shrink
  REVENUE_GENERATED:  [X] ([X]%)

ENGAGEMENT_BAIT INVENTORY: [X] total
  CONVERTED_TO_POSTS: [X] ([X]%)
  UNUSED:             [X] ([X]%) <-- this number should shrink

THIS WEEK:
  Alpha churned: [X]
  Tasks created: [X]
  Tasks completed: [X]
  Revenue from alpha: $[X]

TOP 3 ALPHA NOT YET UTILIZED (oldest APPROVED):
  1. ALPHA[XXX] - [tactic] - approved [date] - [X] days idle
  2. ALPHA[XXX] - [tactic] - approved [date] - [X] days idle
  3. ALPHA[XXX] - [tactic] - approved [date] - [X] days idle
```

---

## Ralph Loop Integration

### Loop: alpha_churn (run daily, 3 iterations per day)

**Prompt template for ralph loop:**

```markdown
# Alpha Churn Loop

You are an execution agent. Your job is to convert approved alpha into actionable tasks.

## Your Process

1. Read LEDGER/ALPHA_STAGING.csv
2. Find all APPROVED entries where utilization_status is NOT_UTILIZED or empty
3. Sort by roi_potential (HIGHEST first), then effort_level (LOW first)
4. For the top entry:
   a. Create a specific, executable task
   b. If the task can be done by an AI agent (research, content creation, code generation): DO IT NOW
   c. If the task requires human action (purchases, account creation, publishing): Write to ralph/loops/mega/checkpoints/PENDING_ALPHA_TASKS.md
   d. Update utilization_status in the CSV
5. Append to LEDGER/ALPHA_CHURN_LOG.csv

## What You Can Do Without Human

- Generate content from ENGAGEMENT_BAIT entries
- Create email templates from OUTBOUND alpha
- Build landing page drafts from APP_FACTORY alpha
- Write cold outreach scripts
- Create GEO-optimized content from SEO alpha
- Draft social media posts
- Build automation workflow specs
- Generate product descriptions
- Create pitch decks / service proposals

## What Needs Human

- Purchases over $50
- Account creation (requires email/phone)
- Publishing (human reviews first)
- Domain purchases
- Tool subscriptions
- Sending actual emails
```

### Loop config (add to ralph/loops/alpha_churn/):

```
PROMPT.md: [above prompt]
prd.json: {
  "tasks": [
    {"id": "churn-001", "title": "Convert top 3 HIGHEST ROI alpha to tasks", "passes": false},
    {"id": "churn-002", "title": "Generate 5 social posts from ENGAGEMENT_BAIT entries", "passes": false},
    {"id": "churn-003", "title": "Create email template from OUTBOUND alpha", "passes": false},
    {"id": "churn-004", "title": "Draft landing page from APP_FACTORY alpha", "passes": false},
    {"id": "churn-005", "title": "Build GEO content from SEO alpha", "passes": false},
    {"id": "churn-006", "title": "Update utilization tracking and generate report", "passes": false}
  ]
}
```

---

## Engagement Bait Conversion Pipeline

169 ENGAGEMENT_BAIT entries are content gold sitting unused.

### Daily conversion target: 5 entries -> 15+ posts

For each ENGAGEMENT_BAIT entry:
1. Extract the hook / key claim
2. Rewrite in PRINTMAXXER voice (follow `.claude/rules/copy-style.md`)
3. Create 3 variants:
   - Twitter/X post (consequence-first, specific numbers)
   - Instagram caption (hook + value + CTA)
   - TikTok script (3-sec hook + problem + solution + CTA)
4. Save to `AUTOMATIONS/content_posting/alpha_derived/`
5. Mark entry with `content_generated: TRUE` and date

### Example conversion:

**ENGAGEMENT_BAIT entry (ALPHA092):**
> "Gauth $1.2M/mo, Knowunity $460k/mo, Chegg $600k/mo. All AI study apps using viral slideshow format generating 50M views/mo."

**Twitter post:**
> "3 AI study apps printing $2.2M/mo combined. all using the same format: informational slideshows on TikTok. no influencers. no UGC. just organic educational content with a CTA. Gauth alone does $1.2M/mo. the study niche is wide open."

**Instagram caption:**
> "study apps are printing. Gauth: $1.2M/mo. Knowunity: $460k/mo. they all use the same viral format: informational slideshows on TikTok. no face required. replicate this in any niche."

**TikTok script:**
> "[HOOK - 3 sec] this app makes $1.2 million a month with zero influencers
> [PROBLEM] most people think you need UGC creators or paid ads to grow an app
> [SOLUTION] these study apps just post organic slideshows on TikTok. educational content. that's it.
> [CTA] comment STUDY if you want the full breakdown"

---

## PENDING_REVIEW Batch Processing

108 PENDING_REVIEW entries need review. Process in batches of 20.

### Batch review SOP:
1. Read 20 entries
2. Apply quick decision framework from `.claude/rules/alpha-review.md`
3. Update status
4. For newly APPROVED: immediately queue for alpha churn
5. For ENGAGEMENT_BAIT: immediately queue for content conversion
6. Target: clear all 108 within 5 sessions (20 per session)

---

## Schema Update for ALPHA_STAGING.csv

Add these columns:

| Column | Type | Values | Purpose |
|--------|------|--------|---------|
| `utilization_status` | string | NOT_UTILIZED, IN_PROGRESS, UTILIZED, REVENUE_GENERATED | Track whether alpha is being used |
| `utilization_date` | date | YYYY-MM-DD | When alpha was first acted on |
| `utilization_notes` | string | Free text | What was done with this alpha |
| `content_generated` | boolean | TRUE/FALSE | Whether content was created from this entry |
| `revenue_attributed` | number | Dollar amount | Revenue directly attributed to this alpha |
| `days_idle` | calculated | utilization_date - reviewed_date | How long alpha sat before use |

---

## Dashboard Integration

Add to `AUTOMATIONS/printmaxx_quant_terminal.py`:

```
ALPHA UTILIZATION PANEL:
  Total Alpha:     835
  Approved:        163 (19.5%)
  Utilized:        [X] ([X]% of approved)  <-- KEY METRIC
  Revenue:         $[X] from alpha
  Avg Days Idle:   [X] days
  Today's Churn:   [X]/3 target
  EB -> Posts:     [X]/5 target
```

---

## Critical Path: First 7 Days

| Day | Alpha to Churn | Expected Output |
|-----|---------------|-----------------|
| 1 | ALPHA319 (Visualping), ALPHA285 (subdomains), ALPHA222 (Leonardo) | Competitor monitoring live. Domains purchased. AI persona generated. |
| 2 | ALPHA282 (warmup start), ALPHA334 (self-reply), ALPHA271 (repurposing) | Email warmup started. Self-reply funnel live. Repurposing workflow drafted. |
| 3 | ALPHA296 (Nano Banana UGC), ALPHA274 (cold email strategy), ALPHA032 (animated paywall) | 10 sample UGCs created. Email templates written. Paywall spec drafted. |
| 4 | ALPHA010 (email flash sale), ALPHA263 (TikTok algo), ALPHA015 (FOIA/gov) | Beehiiv setup. First TikTok posted. FOIA request filed. |
| 5 | 10 ENGAGEMENT_BAIT -> posts, ALPHA343 (4-day SaaS), ALPHA045 (portfolio) | 30 posts queued. First SaaS validation started. Portfolio plan created. |
| 6 | ALPHA288 (Clay intent data), ALPHA008 (clipper network), ALPHA358 (trading bot) | Clay trial started. Clipper recruitment DMs sent. Bot spec drafted. |
| 7 | Review + report | Weekly utilization report. Adjust process. Celebrate any revenue. |

**By Day 7, at least 20 alpha entries should be IN_PROGRESS or UTILIZED.**
**By Day 14, target 50+.**
**By Day 30, 80% utilization rate on all APPROVED alpha.**

---

## The Rule

**No new alpha collection until utilization rate hits 50%.**

We don't need more research. We need to use what we have. 835 entries is enough alpha for 6 months of daily ops. Stop collecting. Start churning.
