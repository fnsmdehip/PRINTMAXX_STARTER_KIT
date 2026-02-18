---
task_id: CONTENT-002
test_command: "python3 -c \"import os; files = os.listdir('CONTENT/social/news/'); assert len(files) >= 30, f'Only {len(files)} files'\""
max_iterations: 15
completion_signal: "NEWS_BATCH_COMPLETE"
---

# Task: Generate 30 news-format posts for X

## Context
- Read .claude/rules/copy-style.md for voice
- Read .ralph/guardrails.md for constraints
- Output to CONTENT/social/news/
- Create directory if needed: `mkdir -p CONTENT/social/news/`

## Post Formats

### Format 1: Breaking News (10 posts)
```
BREAKING: [Headline in <10 words]

[Key detail 1]
[Key detail 2]

Source: [placeholder]
```

### Format 2: Thread Starters (10 posts)
```
[Hook statement that makes you want to read more]

A thread on [topic]:

1/
```

### Format 3: Data/Stats Posts (10 posts)
```
[Surprising statistic]

What this means:
- [Implication 1]
- [Implication 2]
- [Implication 3]
```

## Topic Areas (Mix)
- Tech/AI developments
- Business/startup news
- Internet culture
- Economy/markets
- Social trends

## Success Criteria
1. [ ] 30 posts written to CONTENT/social/news/
2. [ ] 10 breaking, 10 threads, 10 data posts
3. [ ] Each post < 280 chars (except threads which have 1/ marker)
4. [ ] No em dashes
5. [ ] No promotional language
6. [ ] Files named: news_001.md through news_030.md

## File Format
```markdown
---
type: news
platform: x
format: breaking | thread | data
topic: tech | business | culture | economy | social
generated_date: 2026-01-22
char_count: [number]
---

[Post content here]
```

## Quality Checks
- Does it sound like a legitimate news account?
- Is there specific information (numbers, names)?
- Would people RT this for information value?

## When complete
Output: <promise>NEWS_BATCH_COMPLETE</promise>
