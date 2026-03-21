# Growth Plan: MIT repo: brufdev/many-notes (928 stars, PHP)

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $100-400/mo

---

## Tactics

1. Post in r/selfhosted and r/productivity as 'I found this open-source notes app with 928 stars' — drives organic installs and brand awareness
2. Submit to awesome-selfhosted GitHub list for passive backlinks
3. Create 'Notion is $16/mo — here's a $0 self-hosted alternative' thread on Twitter/X
4. List hosted version on Product Hunt as 'Many Notes Cloud — privacy-first notes without the Notion price'

## Budget Tier Strategies

### FREE
Post in r/selfhosted, r/productivity, r/privacy — self-hosted community actively seeks these tools. Submit to alternativeto.net, saashub.com. SEO landing page for 'self-hosted notes', 'open source notion alternative'. Cross-post to HN Show HN.

### LOW
$20 Reddit promoted post in r/privacy or r/selfhosted targeting the anti-Notion crowd. $20 for a PH launch boost via engagement warming.

### MID
$50-100 on micro-influencer in productivity/PKM niche (Zettelkasten, second brain community) to mention the hosted tier.

## Daily Actions

- [ ] Run subagents in parallel: audit repo features + scrape GitHub issues for pain points + check competitor pricing
- [ ] Fork repo, apply branding patch, add Stripe payment link as 7-day trial gate
- [ ] Generate Railway deploy config, push to Railway free tier (PHP supported)
- [ ] Build surge.sh landing page targeting 'self-hosted notes app', 'open source notion alternative', 'private notes no cloud'
- [ ] Submit to alternativeto.net, saashub.com, Product Hunt
- [ ] Run engagement_bait_converter.py on 'Notion costs $16/mo, this PHP app is free to self-host but I'll host it for $9/mo' angle
- [ ] Add KPI entry: weekly trial-to-paid conversion check

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py \u2014 convert 'self-hosted notes vs Notion cost' angle into 3 tweets + 1 thread"
}
```
