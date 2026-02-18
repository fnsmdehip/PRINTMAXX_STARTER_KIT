# Ralph Task: Cold Email Sequences

Generate cold email sequences for 5 ICPs.

---

## Context
- Read `.claude/rules/copy-style.md` for content rules
- Read `ralph/guardrails.md` before starting
- Output to `CONTENT/email_sequences/cold/`
- @pipelineabuser style: direct, specific numbers, no fluff

## Success Criteria

### Sequence 1: SaaS Founders (saas_founders.md)
1. [ ] ICP: B2B SaaS founders $10k-100k MRR
2. [ ] 5 emails (Day 0, 3, 7, 14, 21)
3. [ ] Subject lines under 50 chars
4. [ ] Body 150-200 words max
5. [ ] Clear CTA each email

### Sequence 2: Agency Owners (agency_owners.md)
6. [ ] ICP: Marketing/dev agencies 5-20 employees
7. [ ] 5 emails with timing
8. [ ] Pain: client acquisition, scaling
9. [ ] Offer: AI automation

### Sequence 3: Content Creators (content_creators.md)
10. [ ] ICP: YouTubers/TikTokers 10k-100k followers
11. [ ] 5 emails with timing
12. [ ] Pain: monetization, time
13. [ ] Offer: content repurposing

### Sequence 4: E-commerce Brands (ecommerce_brands.md)
14. [ ] ICP: D2C brands $50k-500k/mo
15. [ ] 5 emails with timing
16. [ ] Pain: ad costs, organic traffic
17. [ ] Offer: UGC and content marketing

### Sequence 5: Coaches/Consultants (coaches.md)
18. [ ] ICP: Business/life coaches with audience
19. [ ] 5 emails with timing
20. [ ] Pain: 1:1 to 1:many scaling
21. [ ] Offer: info product creation

### Completion
22. [ ] SEQUENCES_COMPLETE.md created
23. [ ] All 5 sequences in folder

## Email Format

```markdown
---
sequence: [name]
icp: [description]
pain_point: [main problem]
offer: [what we're offering]
---

## Email 1 - Day 0 (Initial Outreach)
**Subject:** [subject line]

[body copy]

---
```

## Constraints
- No em dashes
- No AI vocabulary
- Specific numbers in every email
- Plain text format
- One ask per email

## After Completion
- Update `ralph/progress.md`

---

test_command: "ls CONTENT/email_sequences/cold/*.md | wc -l"
expected_output: "6"
