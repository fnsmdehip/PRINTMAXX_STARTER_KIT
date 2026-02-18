---
name: generate-longtail
description: Generate SEO-optimized longtail pages in bulk. Use Haiku for speed.
model: haiku
---

# Longtail Page Generation

Generate longtail pages following the PRINTMAXX system.

## Process

1. Read LEDGER/GEO_LONGTAIL_SLUGS_300.csv
2. Filter for rows where published != TRUE
3. For each slug (up to N requested):
   - Generate page following .claude/rules/copy-style.md
   - Use template structure from existing CONTENT/longtail_pages/
   - Write to CONTENT/longtail_pages/[slug].md
   - Update CSV row with published=TRUE, date

## Quality Gates

- Every 10th page: Use Sonnet for quality review
- Check: No AI vocab, no em dashes, specific numbers
- Validate frontmatter format

## Arguments

- First argument: Number of pages to generate (default: 10)

Example: `/generate-longtail 25`
