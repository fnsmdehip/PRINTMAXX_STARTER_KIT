# Growth Plan: MIT repo: Lissy93/dashy (24290 stars, Vue)

**Created:** 2026-03-21 12:40
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $150-600/mo

---

## Tactics

1. Post config screenshots to r/selfhosted (200K) and r/homelab (500K) — these communities actively seek curated setups
2. Comment in Dashy GitHub Discussions and Issues offering pre-built config packs (24K star community = warm audience)
3. Twitter thread: 'I built the ultimate solopreneur command center using open-source Dashy — free config inside'
4. SEO targets: 'dashy config template', 'self-hosted dashboard for solopreneurs', 'homelab dashboard setup'
5. Submit to AlternativeTo under Notion/Monday dashboard alternatives
6. Product Hunt launch: 'Solopreneur Command Center — pre-configured Dashy dashboard for indie hackers'

## Budget Tier Strategies

### FREE
Post to r/selfhosted + r/homelab with screenshots, comment in Dashy GitHub Discussions, Twitter screenshot thread, AlternativeTo listing, Hacker News Show HN post

### LOW
$20 Reddit promoted post in r/selfhosted + r/homelab; $15 Product Hunt boost on launch day

### MID
$100 micro-influencer in homelab/self-hosting niche (2-5K followers) for config showcase review; $50 targeted Twitter ads to self-hosted + indie hacker interest audiences

## Daily Actions

- [ ] Clone lissy93/dashy into MONEY_METHODS/APP_FACTORY/builds/dashy-command-center/
- [ ] Run dashy_template_factory.py to generate 5 niche YAML configs with curated widgets per persona
- [ ] npm run build with indie-hacker.yml as default; deploy to dashy-demo.surge.sh
- [ ] playwright screenshot each niche config for listing assets
- [ ] Package each config as zip + README → Gumroad listing at $19/pack or $49 all-5-bundle
- [ ] Create $297 EAS tier: 'Custom Dashy Dashboard Setup' (30-min scoping + deploy + config)
- [ ] Write SEO landing page targeting 'self-hosted solopreneur dashboard' longtail keywords
- [ ] Add weekly cron to check upstream Dashy releases and auto-notify if configs need updates

## Tooling

```json
{
  "browser": "playwright (demo deployment testing + screenshot generation)",
  "email": "none",
  "content": "content_factory (screenshot-to-post pipeline for r/selfhosted posts)"
}
```
