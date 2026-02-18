# Ralph Task: Fitness Niche Content Batch

Generate social content for the Fitness niche.

---

## Context
- Read `.claude/rules/copy-style.md` for content rules
- Read `.ralph/guardrails.md` before starting
- Output to `CONTENT/social/fitness/`
- Voice: Direct, no-BS, results-focused

## Success Criteria

### Social Posts (30 total)
1. [ ] 10 workout tips (specific, actionable)
2. [ ] 10 nutrition/habit posts with numbers
3. [ ] 10 motivation posts (real talk, not toxic positivity)
4. [ ] All posts saved as individual .md files
5. [ ] No em dashes in any post
6. [ ] No banned AI vocabulary
7. [ ] Each post has specific number or timeframe

### Thread Scripts (5 total)
8. [ ] "The 3-hour physique: my actual routine" thread
9. [ ] "5 exercises you're doing wrong (and fixes)" thread
10. [ ] "What 6 months of consistency actually looks like" thread
11. [ ] "The gym bro advice that's actually wrong" thread
12. [ ] "How I stay consistent when motivation disappears" thread
13. [ ] Each thread 5-7 tweets
14. [ ] Threads saved to `CONTENT/threads/fitness/`

### Video Scripts (5 total)
15. [ ] 30-second form check script
16. [ ] 60-second "one exercise you need" script
17. [ ] 30-second meal prep tip
18. [ ] 60-second myth buster
19. [ ] 30-second challenge/CTA
20. [ ] Scripts saved to `CONTENT/video_scripts/fitness/`

## Constraints
- No dangerous advice (injury risk)
- No unrealistic transformations
- Honest about timelines
- No supplement pushing without disclosure
- Accessible to beginners

## After Completion
- Update `.ralph/progress.md`
- Log any errors to `.ralph/errors.log`
- Add new guardrails if patterns discovered

---

test_command: "find CONTENT/social/fitness -name '*.md' | wc -l"
expected_output: "30"
