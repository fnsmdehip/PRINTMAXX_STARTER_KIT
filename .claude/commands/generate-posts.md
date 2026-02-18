---
name: generate-posts
description: Generate social media posts across niches and platforms. Bulk creation for content farm.
model: haiku
---

# Social Post Generation

Generate social posts for the 3-niche content farm.

## Process

1. Read LEDGER/WINNING_CONTENT_STRUCTURES.csv for formats
2. Read existing posts in AUTOMATIONS/content_generation/posts/ for style
3. Generate posts following .claude/rules/copy-style.md

## Output Structure

```
AUTOMATIONS/content_generation/posts/
├── ai/
│   ├── x/post_XXX.md
│   ├── tiktok/post_XXX.md
│   └── instagram/post_XXX.md
├── faith/
│   └── [same structure]
└── fitness/
    └── [same structure]
```

## Arguments

- `--niche [ai|faith|fitness|all]` - Which niche (default: all)
- `--count N` - Posts per niche (default: 10)
- `--platform [x|tiktok|instagram|all]` - Which platform (default: all)

Example: `/generate-posts --niche ai --count 20 --platform x`
