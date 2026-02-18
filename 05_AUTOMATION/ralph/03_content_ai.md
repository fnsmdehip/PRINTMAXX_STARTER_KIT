# Ralph Task: AI/Productivity Niche Content Batch

Generate social content for the AI/Productivity niche.

---

## Context
- Read `.claude/rules/copy-style.md` for content rules
- Read `.ralph/guardrails.md` before starting
- Output to `CONTENT/social/ai/`
- Voice: Technical but accessible, @levelsio style

## Success Criteria

### Social Posts (30 total)
1. [ ] 10 AI tool tips (specific tools, specific uses)
2. [ ] 10 productivity hacks with time saved
3. [ ] 10 automation wins (what I automated, results)
4. [ ] All posts saved as individual .md files
5. [ ] No em dashes in any post
6. [ ] No banned AI vocabulary
7. [ ] Each post mentions specific tool or number

### Thread Scripts (5 total)
8. [ ] "My $0 tech stack that makes $X/month" thread
9. [ ] "5 AI tools that replaced my VA" thread
10. [ ] "How I automated my content posting (3 hours setup)" thread
11. [ ] "The prompt engineering tricks nobody talks about" thread
12. [ ] "What running AI agents overnight actually looks like" thread
13. [ ] Each thread 5-7 tweets
14. [ ] Threads saved to `CONTENT/threads/ai/`

### Video Scripts (5 total)
15. [ ] 30-second tool demo script
16. [ ] 60-second "before/after automation" script
17. [ ] 30-second prompt tip
18. [ ] 60-second workflow breakdown
19. [ ] 30-second results showcase
20. [ ] Scripts saved to `CONTENT/video_scripts/ai/`

## Constraints
- Specific tools, not vague "AI"
- Real results with numbers
- Acknowledge limitations
- No hype ("revolutionary", "game-changing")
- Accessible to non-technical audience

## After Completion
- Update `.ralph/progress.md`
- Log any errors to `.ralph/errors.log`
- Add new guardrails if patterns discovered

---

test_command: "find CONTENT/social/ai -name '*.md' | wc -l"
expected_output: "30"
