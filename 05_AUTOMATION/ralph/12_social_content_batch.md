# Ralph Task: Social Content Batch Generation

Generate 150 social posts across 3 niches (50 each).

---

## Context
- Read `.claude/rules/copy-style.md` for content rules
- Read `ralph/guardrails.md` before starting
- Output to `CONTENT/social/{niche}/`
- Each post under 280 chars
- Individual .md files numbered 001-050 per niche

## Success Criteria

### Faith Niche (50 posts)
1. [ ] 10 morning devotional prompts saved to `CONTENT/social/faith/`
2. [ ] 10 prayer reminders with specific timing
3. [ ] 10 faith-based productivity tips
4. [ ] 10 scripture application posts
5. [ ] 10 encouragement for busy believers
6. [ ] All files named 001.md through 050.md with frontmatter

### Fitness Niche (50 posts)
7. [ ] 10 quick workout tips with specific reps saved to `CONTENT/social/fitness/`
8. [ ] 10 nutrition hacks with exact numbers
9. [ ] 10 recovery and sleep posts
10. [ ] 10 mindset posts
11. [ ] 10 progress tracking motivation
12. [ ] All files named 001.md through 050.md with frontmatter

### AI/Productivity Niche (50 posts)
13. [ ] 10 AI tool recommendations saved to `CONTENT/social/ai/`
14. [ ] 10 automation wins with time saved metrics
15. [ ] 10 solopreneur revenue/growth tactics
16. [ ] 10 Claude/ChatGPT workflow tips
17. [ ] 10 build in public style updates
18. [ ] All files named 001.md through 050.md with frontmatter

### Completion
19. [ ] BATCH_COMPLETE.md created in each niche folder
20. [ ] Total 150 posts generated

## File Format

```markdown
---
type: social_post
platform: x_twitter
niche: [faith|fitness|ai_productivity]
generated_date: 2026-01-24
char_count: [actual count]
---

[post content here]
```

## Constraints
- No em dashes (—)
- No AI vocabulary: leverage, utilize, delve, comprehensive, robust, innovative, seamless, game-changer, unlock, empower, cutting-edge
- Specific numbers over vague claims
- Hook in first line
- Under 280 characters each

## After Completion
- Update `ralph/progress.md` with batch count
- Create BATCH_COMPLETE.md in each folder

---

test_command: "find CONTENT/social -name '*.md' | grep -v BATCH | wc -l"
expected_output: "150"
