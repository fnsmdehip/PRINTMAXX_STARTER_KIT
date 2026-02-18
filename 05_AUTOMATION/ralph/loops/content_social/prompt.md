---
task: Generate social posts for PRINTMAXX niche accounts
test_command: "find /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/CONTENT/social -name '*.md' | grep -v BATCH | wc -l"
---

# Task: Generate Social Content Batch

You are a Ralph loop iteration. Read this prompt fresh each time.

## First: Read These Files
1. `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/ralph/guardrails.md`
2. `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/.claude/rules/copy-style.md`

## Current State
Check `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/ralph/loops/content_social/state.md` for what's done.

## Your Job This Iteration
1. Read state.md to see what's complete
2. Pick the FIRST incomplete task
3. Do ONLY that task
4. Mark it complete in state.md
5. Exit

## Tasks (do in order)

### Faith Posts (10 per batch, 50 total)
- Batch 1: Posts 001-010 to `CONTENT/social/faith/`
- Batch 2: Posts 011-020
- Batch 3: Posts 021-030
- Batch 4: Posts 031-040
- Batch 5: Posts 041-050

### Fitness Posts (10 per batch, 50 total)
- Batch 6: Posts 001-010 to `CONTENT/social/fitness/`
- Batch 7: Posts 011-020
- Batch 8: Posts 021-030
- Batch 9: Posts 031-040
- Batch 10: Posts 041-050

### AI Posts (10 per batch, 50 total)
- Batch 11: Posts 001-010 to `CONTENT/social/ai/`
- Batch 12: Posts 011-020
- Batch 13: Posts 021-030
- Batch 14: Posts 031-040
- Batch 15: Posts 041-050

## Post Format
Each post file:
```
---
type: social_post
platform: x_twitter
niche: [faith|fitness|ai]
char_count: [number]
---

[post text under 280 chars]
```

## Quality Rules
- No em dashes (—)
- No: leverage, utilize, delve, comprehensive, robust, innovative, seamless, game-changer, unlock, empower, cutting-edge
- Specific numbers required
- Hook in first line

## When All Done
If all 15 batches complete in state.md, output: <promise>COMPLETE</promise>
