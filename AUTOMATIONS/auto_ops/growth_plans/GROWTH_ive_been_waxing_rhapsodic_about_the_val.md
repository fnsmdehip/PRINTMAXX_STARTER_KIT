# Growth Plan: I've been waxing rhapsodic about the value of an AI writing 

**Created:** 2026-03-21 12:40
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $80-300/mo

---

## Tactics

1. Reply to @every post with niche-specific example to intercept their audience
2. Post 3-tweet thread: 'AI writes generic slop. Here is the exact framework I use to make it sound like me' — link to Gumroad
3. Share the framework skeleton for free on Twitter; sell the complete niche-specific version
4. Cross-post to r/SaaS, r/Entrepreneur, Indie Hackers with value-first angle — no direct sell in post
5. Run engagement_bait_converter.py on this method to extract 3 hook posts

## Budget Tier Strategies

### FREE
Thread on Twitter showing the style guide framework with real before/after examples. Reply to @every to tap their readership. Seed Indie Hackers with value post referencing the free framework + paid complete version.

### LOW
$20 boost on best-performing tweet to founder/writer audience. DM 10 newsletter writers offering free guide in exchange for honest review or mention.

### MID
$100-150 to 5 micro-influencer newsletter writers (5K-20K lists) for a mention — free guide as the offer, Gumroad link in their issue.

## Daily Actions

- [ ] Add 'ai_style_guide' product type to micro_info_product_builder.py with template sections: voice definition, prompt library, tone rules, before/after rewrites
- [ ] Run 5 parallel claude -p calls to generate niche variants: SaaS, ecom, newsletter, coach, agency
- [ ] Review outputs, package as structured PDFs
- [ ] Queue on Gumroad at $27-47 each when account is live (16 drafts already pending — add these to batch)
- [ ] Run engagement_bait_converter.py on this method to generate 3 Twitter hooks
- [ ] Reply to @every post with concrete example to intercept their audience

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "claude -p + engagement_bait_converter.py + content_repurposer.py"
}
```
