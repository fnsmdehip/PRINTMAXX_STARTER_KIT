# Trend Intelligence Loop Guardrails

Learned constraints from iterations. Append-only. Never delete entries.

---

## General Rules

### Always check for duplicates before adding
- **Trigger:** Adding to LEDGER/TREND_INTEL_TRACKER.csv
- **Instruction:** Read file first, check if `handle` column already has this creator
- **Reason:** Avoid duplicate entries cluttering the tracker

### Append, never overwrite
- **Trigger:** Writing to CSV files
- **Instruction:** Use `>> file.csv` not `> file.csv`
- **Reason:** Preserve existing data

### Write immediately, don't accumulate
- **Trigger:** Finding research results
- **Instruction:** Write each finding to disk individually, not batch at end
- **Reason:** Data persists even if iteration crashes

### Require proof for revenue estimates
- **Trigger:** Filling est_mrr column
- **Instruction:** Must have visible revenue proof (screenshots, public numbers, credible estimates from follower/pricing data)
- **Reason:** Speculation wastes time. Only track what we can validate.

### Cross-reference existing methods
- **Trigger:** Filling printmaxx_methods column
- **Instruction:** Check LEDGER/MONEY_METHODS_TRACKER.csv for valid method IDs
- **Reason:** Findings must map to our execution capabilities

---

## Quality Rules

### Replication score must be justified
- **Trigger:** Assigning replication_score
- **Instruction:** Score 7+ requires specific explanation of what's replicable and what infrastructure we have
- **Reason:** Prevents optimistic scoring that wastes human review time

### Minimum 2 replicable frameworks per entry
- **Trigger:** Evaluating whether to log a finding
- **Instruction:** Must identify at least 2 specific things we can copy (content format, pricing, distribution, funnel structure, etc.)
- **Reason:** Single-insight findings don't justify the tracking overhead

### Don't log creators without monetization
- **Trigger:** Finding a creator with large following but no visible income
- **Instruction:** Skip unless they're clearly building toward monetization (launching soon, building audience)
- **Reason:** We're tracking monetized trends, not just popular accounts

---

## Rate Limit Rules

### WebSearch pacing
- **Trigger:** Running multiple searches in sequence
- **Instruction:** Don't fire more than 10 searches per category. Be strategic with queries.
- **Reason:** Stay within API limits and focus on high-signal searches

### One category per iteration
- **Trigger:** Starting research
- **Instruction:** Pick ONE category from progress.md, complete it fully, then exit
- **Reason:** Ralph loop pattern - each iteration is one focused task

---

## File-Specific Rules

### LEDGER/TREND_INTEL_TRACKER.csv
- trend_id format: TREND[NNN] (three digits, zero-padded)
- date_identified: YYYY-MM-DD format
- est_mrr: Use ranges ($1K-5K, $5K-20K, $20K-100K, $100K+)
- replication_score: Integer 1-10
- printmaxx_methods: Comma-separated method IDs (no spaces)
- status: Always PENDING_REVIEW for new entries

### OPS/TREND_INTEL/analyses/*.md
- Filename format: TREND[NNN]_[handle_without_at].md
- Only create for replication_score >= 7
- Follow the template in prompt.md exactly
- Keep analysis concise (under 100 lines)

---

## Error Recovery

### If web search returns no results
- Try alternative query phrasing
- Try different search engine/approach
- Log to errors.log and move on after 3 failed attempts

### If TREND_INTEL_TRACKER.csv doesn't exist
- Create it with the header row from prompt.md
- Log the creation to activity.log

### If analysis directory doesn't exist
- Create OPS/TREND_INTEL/analyses/ directory
- Log the creation to activity.log

---

*Add new guardrails as failures occur during loop runs*
