# Growth Plan: <!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8

**Created:** 2026-03-20 23:12
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $0/mo

---

## Tactics

1. Fix orphan_doc_scanner to skip binary/code files — only stage markdown/text/CSV as alpha
2. Add pre-filter: if method field starts with '<' or '{' or contains DOCTYPE, auto-reject before staging

## Budget Tier Strategies

### FREE
Add HTML/code content filter to orphan_doc_scanner.py — 10-line fix, prevents repeated false positives

### LOW
N/A

### MID
N/A

## Daily Actions

- [ ] Add content-type filter to orphan_doc_scanner.py: skip files ending in .html, .css, .js, .json
- [ ] Add method field validator in auto_approve.py: if method starts with '<' or '<!', set quality_score=1 and skip
- [ ] Add PreToolUse hook in settings.json to block staging of entries where method contains 'DOCTYPE' or '<html'

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "none"
}
```
