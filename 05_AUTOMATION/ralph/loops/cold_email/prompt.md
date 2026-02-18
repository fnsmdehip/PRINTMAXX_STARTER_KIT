---
task: Generate cold email sequences for PRINTMAXX outbound
test_command: "ls /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/CONTENT/email_sequences/cold/*.md | wc -l"
---

# Task: Generate Cold Email Sequences

You are a Ralph loop iteration. Read this prompt fresh each time.

## First: Read These Files
1. `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/ralph/guardrails.md`
2. `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/.claude/rules/copy-style.md`

## Current State
Check `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/ralph/loops/cold_email/state.md`

## Your Job This Iteration
1. Read state.md for what's complete
2. Pick FIRST incomplete sequence
3. Write ONLY that sequence
4. Save to `CONTENT/email_sequences/cold/`
5. Mark complete in state.md
6. Exit

## Sequences to Write

### Sequence 1: saas_founders.md
- ICP: B2B SaaS founders $10k-100k MRR
- Pain: Need leads, struggling distribution
- 5 emails: Day 0, 3, 7, 14, 21

### Sequence 2: agency_owners.md
- ICP: Marketing/dev agencies 5-20 employees
- Pain: Client acquisition, scaling
- 5 emails

### Sequence 3: content_creators.md
- ICP: YouTubers/TikTokers 10k-100k followers
- Pain: Monetization beyond ads
- 5 emails

### Sequence 4: ecommerce_brands.md
- ICP: D2C brands $50k-500k/mo
- Pain: Rising ad costs, organic traffic
- 5 emails

### Sequence 5: coaches.md
- ICP: Business/life coaches with audience
- Pain: 1:1 to 1:many scaling
- 5 emails

## Email Format
```markdown
---
sequence: [name]
icp: [description]
pain_point: [main problem]
---

## Email 1 - Day 0
**Subject:** [under 50 chars]

[body 150-200 words max]

---

## Email 2 - Day 3
[etc.]
```

## Copy Rules
- No em dashes
- No AI vocabulary
- Specific numbers in every email
- @pipelineabuser style: direct, consequence-first
- One clear CTA per email
- Plain text only

## When All Done
If all 5 sequences complete, output: <promise>COMPLETE</promise>
