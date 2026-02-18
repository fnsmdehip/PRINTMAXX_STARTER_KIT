---
name: review-alpha
description: Review pending alpha entries and integrate approved findings into master files.
model: sonnet
---

# Alpha Review Workflow

Review staged alpha findings and integrate into the system.

## Process

1. Read LEDGER/ALPHA_STAGING.csv
2. Filter for status = PENDING_REVIEW
3. For each entry:
   - Evaluate using criteria from OPS/prompts/skills/daily-alpha-research.md
   - Mark APPROVED or REJECTED
   - If APPROVED: Add actionable_steps and integrate into appropriate master file:
     - APP_FACTORY_METHODS.csv for new playbooks
     - MARKETING_CHANNELS_MASTER.csv for new channels
     - WINNING_CONTENT_STRUCTURES.csv for content formats
     - TOOLS_SERVICES_MASTER.csv for new tools
4. Update ALPHA_STAGING.csv with decisions

## Approval Criteria

- Actionable within $200-$500 budget
- Has proof of working (numbers, testimonials)
- Not already in our playbook
- Aligns with 3 niches or PRINTMAXXER meta-brand

## Output

Summary of:
- Entries reviewed
- Approved vs rejected
- Files updated
- New methods/channels/tools added
