# Growth Plan: In 1893, a printer pinned a style guide to the wall so Oxfor

**Created:** 2026-03-21 12:40
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $50-150/mo

---

## Tactics

1. Post the Oxford compositor story as a thread hook — historical analogy converts well on X
2. Quote-tweet @kplikethebird's post with our own take + link to the Gumroad product
3. Drop in r/ChatGPT, r/LocalLLaMA, r/PromptEngineering — style guide advice posts perform well there
4. Add to PRINTMAXX's own .claude/reference/copy-style.md — immediate internal value

## Budget Tier Strategies

### FREE
Post the historical hook story on X. Engage in AI Twitter threads about prompt consistency. Submit to r/PromptEngineering. Use engagement_bait_converter.py to generate 3 post variants from the Oxford compositor angle.

### LOW
$0-50/mo: Boost the best-performing tweet. Pin to profile. Add to a newsletter issue.

### MID
$50-200/mo: Sponsor a small AI newsletter. Bundle with other prompt packs.

## Daily Actions

- [ ] Run engagement_bait_converter.py with the Oxford compositor angle — extract 3 tweet variants (hook: '1893 Oxford printer → your LLM needs this too')
- [ ] Create ai_style_guide_generator.py: CLI takes --brand, --niche, --tone, --forbidden-words, outputs a system prompt block + markdown style guide
- [ ] Generate a sample output for PRINTMAXX itself and drop it in .claude/reference/copy-style.md
- [ ] Create a Gumroad listing: 'AI Style Guide Template Pack' ($19) — 5 pre-built style guides (SaaS, ecom, newsletter, app store, cold email) + the generator script
- [ ] Add listing to GUMROAD_UPLOAD_NOW.md queue

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
