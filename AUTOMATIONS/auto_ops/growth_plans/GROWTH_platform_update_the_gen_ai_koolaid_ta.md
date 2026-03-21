# Growth Plan: [PLATFORM UPDATE] The gen AI Kool-Aid tastes like eugenics

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-100/mo

---

## Tactics

1. Post contrarian 'AI pragmatist vs AI critic' content to ride TheVerge/documentary media coverage wave
2. Create thread: 'What AI critics get right — and what they miss for solopreneurs shipping real products'
3. Quote-tweet or respond to mainstream AI criticism accounts with specific, data-backed counter — controversy drives replies
4. Use 'eugenics' angle as a hook in post title, then pivot to practical solopreneur AI use — bait + substance combo
5. Engage with AI ethics/skeptic community to build credibility as nuanced voice, not pure hype

## Budget Tier Strategies

### FREE
Organic: 1 nuanced AI-criticism take per week; engage AI skeptic accounts; thread format to maximize saves/reshares; use controversy framing in first line

### LOW
$0-50/mo: boost top-performing AI controversy post to tech/solopreneur audiences; seed to r/singularity, r/slatestarcodex, HN Show threads

### MID
$50-200/mo: promote 'AI reality check for builders' content to build differentiated authority vs pure-hype accounts

## Daily Actions

- [ ] Run: python3 AUTOMATIONS/engagement_bait_converter.py — pass TheVerge article as context signal
- [ ] Generate 3 post variants: (1) agree-with-nuance ('AI critics are right about X but wrong about Y'), (2) pragmatist rebuttal ('I ship real products with AI, here is what the documentary misses'), (3) hot-take hook ('The gen AI Kool-Aid criticism is 40% right — here is the 60% they are ignoring')
- [ ] Add all 3 to CONTENT/social/posting_queue/ for next scheduled cycle
- [ ] Monitor engagement at 24h and 48h — flag any post exceeding 2x baseline for boosting

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
