# Ralph Task: Email Sequences for All Niches

Generate ready-to-load email sequences.

---

## Context
- Read `.claude/rules/copy-style.md` for content rules
- Read `.ralph/guardrails.md` before starting
- Read existing sequences in `MONEY_METHODS/COLD_OUTBOUND/sequences/` for format
- Output to `CONTENT/email_sequences/`
- Voice: Direct, personal, value-first

## Success Criteria

### Welcome Sequences (3 total, 7 emails each)
1. [ ] Faith welcome sequence (7 emails)
2. [ ] Fitness welcome sequence (7 emails)
3. [ ] AI/Productivity welcome sequence (7 emails)
4. [ ] Each email has: subject, preview text, body, CTA
5. [ ] Day 1: Immediate value delivery
6. [ ] Day 2-3: Story/credibility
7. [ ] Day 4-5: Problem agitation
8. [ ] Day 6-7: Soft pitch

### Launch Sequences (3 total, 5 emails each)
9. [ ] Info product launch sequence (5 emails)
10. [ ] App launch sequence (5 emails)
11. [ ] Service launch sequence (5 emails)
12. [ ] Email 1: Announcement + early bird
13. [ ] Email 2: Value/benefits
14. [ ] Email 3: Social proof
15. [ ] Email 4: Urgency
16. [ ] Email 5: Last chance

### Cold Outreach (5 sequences, 5 emails each)
17. [ ] Agency services cold sequence
18. [ ] SaaS demo cold sequence
19. [ ] Consulting cold sequence
20. [ ] Partnership cold sequence
21. [ ] Podcast guest pitch sequence
22. [ ] Each sequence follows 5-touch pattern
23. [ ] Subject lines A/B variants included

### Nurture Sequences (3 total, 4 emails each)
24. [ ] Weekly value email template
25. [ ] Case study email template
26. [ ] Behind-the-scenes email template

## Format Per Email
```markdown
# [Sequence Name] - Email [N]

**Subject:** [Primary subject line]
**Subject B:** [A/B test variant]
**Preview:** [Preview text < 90 chars]
**Send timing:** [Day X after trigger]

---

[Email body]

---

**CTA:** [What action to take]
**Link:** [Where CTA goes]
```

## Constraints
- No spam triggers (FREE!!!, Act Now, etc.)
- Personal tone (I/you, not we/our)
- Mobile-friendly (short paragraphs)
- One CTA per email
- Value before pitch

## After Completion
- Update `.ralph/progress.md`
- Log any errors to `.ralph/errors.log`
- Add new guardrails if patterns discovered

---

test_command: "find CONTENT/email_sequences -name '*.md' | wc -l"
expected_output: "14"
