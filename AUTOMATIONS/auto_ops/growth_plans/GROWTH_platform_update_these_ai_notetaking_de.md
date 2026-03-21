# Growth Plan: [PLATFORM UPDATE] These AI notetaking devices can help you r

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo affiliate (Amazon Associates 3-4% on $100-400 devices, direct brand affiliate programs at 10-20%)

---

## Tactics

1. Post comparison thread on r/productivity, r/remotework, r/entrepreneur with genuine device breakdown — link to page in comments
2. Twitter thread: 'I tested 5 AI notetakers so you don't have to' — real spec comparison, link in bio
3. Target 'vs' longtail keywords: Plaud Note vs Otter, Friend AI vs Limitless Pendant (high commercial intent, low competition)
4. Add page to existing surge.sh sitemap sweep so it gets indexed alongside 47 live sites
5. Cross-link from existing comparison pages (email-tools, invoice-tools) in a 'related tools' footer

## Budget Tier Strategies

### FREE
SEO via longtail keyword targeting, Reddit authentic posts in productivity subreddits, Twitter comparison thread, internal cross-links from 47 live surge sites

### LOW
$0-50/mo — Pinterest comparison pins (devices side-by-side visual), boost Reddit post with $5 promoted post if organic traction confirmed

### MID
$50-200/mo — YouTube Shorts voiceover comparison video using existing auto-clip pipeline, retarget visitors with Google display ads

## Daily Actions

- [ ] Copy MONEY_METHODS/APP_FACTORY/builds/email-tools-compared/index.html as template
- [ ] Run playwright scrape on top 5-6 AI notetaker device pages for specs/pricing
- [ ] Generate comparison table + FAQ via claude -p with copy-style.md injection
- [ ] Wire Amazon Associates links for each device (use existing AMAZON_ASSOCIATE_ID from .env)
- [ ] Deploy to ai-notetakers-compared.surge.sh
- [ ] Add cron entry: weekly Monday 8 AM to re-scrape prices and refresh page
- [ ] Post Reddit thread in r/productivity + r/remotework same day as deploy

## Tooling

```json
{
  "browser": "playwright MCP for product page scraping",
  "email": "none",
  "content": "claude -p for comparison content, existing comparison page HTML template from APP_FACTORY/builds/"
}
```
