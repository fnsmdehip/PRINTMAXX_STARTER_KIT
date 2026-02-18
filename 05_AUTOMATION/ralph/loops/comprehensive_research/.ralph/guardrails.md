# Comprehensive Research Guardrails

Learned constraints from failed iterations.

---

## General Rules

### Always check for duplicates before adding
- **Trigger:** Adding to any LEDGER CSV
- **Instruction:** `grep "unique_identifier" LEDGER/FILE.csv` first
- **Reason:** Avoid duplicate entries

### Append, never overwrite
- **Trigger:** Writing to CSV files
- **Instruction:** Use `>> file.csv` not `> file.csv`
- **Reason:** Preserve existing data

### Write immediately, don't accumulate
- **Trigger:** Finding research results
- **Instruction:** Write to disk after each finding, not batch at end
- **Reason:** Data persists even if iteration fails

### Require proof
- **Trigger:** Evaluating any finding
- **Instruction:** Must have revenue numbers, GitHub stars, engagement proof, or case study
- **Reason:** Actionable insights only, no speculation

---

## File-Specific Rules

### LEDGER/NICHES.csv
- Must have monetization_proof column filled
- applicable_methods must map to existing method IDs
- niche_id increments from last entry (N021+)

### LEDGER/MONEY_METHODS_TRACKER.csv
- method_id increments from MM017+
- revenue_model required
- proof_url required

### LEDGER/CROSS_POLLINATION_MATRIX.csv
- synergy_score must be 85+ to add
- mechanism column must explain WHY synergy exists
- implementation_sequence required

### LEDGER/ALPHA_STAGING.csv
- status always APPROVED (auto-approved research findings)
- roi_potential required (HIGHEST/HIGH/MEDIUM/LOW)
- category must be valid category name

---

## Error Recovery

### If web search fails
- Try alternative search engines
- Check for rate limiting
- Log to errors.log and move to next category

### If file doesn't exist
- Check LEDGER_INDEX.md for correct path
- Create file with proper headers if truly missing
- Log to errors.log

### If CSV malformed
- Read file first to check format
- Use Python csv module for safety
- Don't write if uncertain

---

*Add new guardrails as failures occur during loop runs*
