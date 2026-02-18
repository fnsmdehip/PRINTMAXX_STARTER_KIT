---
task_id: CONTENT-001
test_command: "python3 -c \"import os; files = os.listdir('CONTENT/social/memes/'); assert len(files) >= 50, f'Only {len(files)} files'\""
max_iterations: 20
completion_signal: "MEME_BATCH_COMPLETE"
---

# Task: Generate 50 meme posts for X

## Context
- Read .claude/rules/copy-style.md for voice
- Read .ralph/guardrails.md for constraints
- Output to CONTENT/social/memes/
- Create directory if needed: `mkdir -p CONTENT/social/memes/`

## Inspiration Sources
- LEDGER/comprehensive_results.csv (engagement patterns from @FearedBuck, @kirawontmiss, etc.)
- Format: Short, punchy, relatable, slightly provocative

## Post Types (Mix All)
1. **Hot takes** (15 posts) - Controversial but defensible opinions
2. **Observations** (15 posts) - "Nobody talks about..." or "It's crazy that..."
3. **Questions** (10 posts) - Engagement bait, relatable problems
4. **Self-deprecating** (10 posts) - Relatable fails and struggles

## Success Criteria
1. [ ] 50 posts written to CONTENT/social/memes/
2. [ ] Each post < 280 characters
3. [ ] No em dashes (use commas or periods)
4. [ ] No banned AI vocabulary (see guardrails)
5. [ ] Mix of all 4 post types
6. [ ] Each file named: meme_001.md through meme_050.md

## File Format
```markdown
---
type: meme
platform: x
post_type: hot_take | observation | question | self_deprecating
generated_date: 2026-01-22
char_count: [number]
---

[Post content here]
```

## Quality Checks
- Would a 22-year-old actually tweet this?
- Does it sound human, not AI?
- Is it specific, not vague?
- Would you like/RT this if you saw it?

## When complete
After all 50 files created and verified:
Output: <promise>MEME_BATCH_COMPLETE</promise>
