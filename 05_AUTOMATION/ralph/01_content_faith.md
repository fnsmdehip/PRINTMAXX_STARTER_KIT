# Ralph Task: Faith Niche Content Batch

Generate social content for the Faith niche.

---

## Context
- Read `.claude/rules/copy-style.md` for content rules
- Read `.ralph/guardrails.md` before starting
- Output to `CONTENT/social/faith/`
- Voice: Encouraging, practical, specific

## Success Criteria

### Social Posts (30 total)
1. [ ] 10 morning devotional hooks (< 280 chars each)
2. [ ] 10 encouragement posts with specific examples
3. [ ] 10 practical faith tips (actionable, not preachy)
4. [ ] All posts saved as individual .md files
5. [ ] No em dashes in any post
6. [ ] No banned AI vocabulary
7. [ ] Each post has hook in first line

### Thread Scripts (5 total)
8. [ ] "5 ways to start your morning with intention" thread
9. [ ] "What I learned from 30 days of daily prayer" thread
10. [ ] "The simple habit that changed my perspective" thread
11. [ ] "Why community matters more than motivation" thread
12. [ ] "How to find peace when everything feels chaotic" thread
13. [ ] Each thread 5-7 tweets
14. [ ] Threads saved to `CONTENT/threads/faith/`

### Video Scripts (5 total)
15. [ ] 30-second devotional script
16. [ ] 60-second "one thing" encouragement
17. [ ] 30-second morning routine tip
18. [ ] 60-second story/testimony format
19. [ ] 30-second call-to-action closer
20. [ ] Scripts saved to `CONTENT/video_scripts/faith/`

## Constraints
- No prosperity gospel vibes
- Encouraging, not guilt-inducing
- Specific examples over generic advice
- Inclusive language (not denomination-specific)
- FTC compliant if mentioning products

## After Completion
- Update `.ralph/progress.md`
- Log any errors to `.ralph/errors.log`
- Add new guardrails if patterns discovered

---

test_command: "find CONTENT/social/faith -name '*.md' | wc -l"
expected_output: "30"
