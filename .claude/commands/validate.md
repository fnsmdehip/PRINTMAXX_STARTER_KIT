---
name: validate
description: Validate content, code, and compliance across the project.
model: sonnet
---

# Validation Suite

Run comprehensive validation across PRINTMAXX systems.

## Checks

### Content Validation
- All truth pages have required frontmatter
- Copy follows .claude/rules/copy-style.md (no AI vocab, no em dashes)
- FTC disclosures present where required
- SEO meta tags present

### Code Validation
- TypeScript compiles without errors
- No exposed credentials in code
- Bundle size within targets (.claude/rules/performance.md)

### LEDGER Validation
- All CSVs have valid headers
- No orphaned references
- Status fields are valid values

### Compliance Check
- COMPLIANCE_LOG.csv up to date
- No fake testimonials
- Affiliate disclosures in place

## Output

Validation report with:
- Pass/fail per category
- Specific issues found
- Recommended fixes
