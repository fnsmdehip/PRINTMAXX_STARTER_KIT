# Growth Plan: Turkish mobile app studio printing $900k/month 

with only 3

**Created:** 2026-03-20 13:50
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $500-3000/mo

---

## Tactics

1. ASO keyword stuffing: target long-tail AI queries (ai search assistant, ai document scanner, ai chat helper) where competition is lower than generic terms
2. Subscription pricing psychology: free tier with 3 queries/day, $4.99/week or $29.99/year — weekly pricing converts higher on impulse installs
3. Localization blitz: translate app listing to 15+ languages for zero-competition international keywords (Turkish studio's edge)
4. Review velocity: in-app review prompt after 3rd successful use (high-satisfaction moment), target 4.7+ stars
5. Cross-promote between our own AI wrapper apps (scanner users see chatbot ad, search users see scanner)
6. Content marketing: TikTok/YouTube Shorts showing the app solving real problems (screen recordings with voiceover)

## Budget Tier Strategies

### FREE
ASO optimization, cross-promotion between own apps, organic TikTok/Shorts content showing app in use, Reddit posts in r/apps r/productivity, in-app review prompts, localization to 15 languages via Claude translation

### LOW
$0-50/mo: Apple Search Ads on exact-match branded competitor keywords (Perplexity, ChatGPT alternatives), targeted Reddit/Twitter ads for AI tool seekers

### MID
$50-200/mo: Apple Search Ads broad campaigns on utility keywords, micro-influencer app reviews on YouTube (5-10K subscriber channels), ProductHunt launch for each app

## Daily Actions

- [ ] 1. Run ai_wrapper_app_scanner.py to identify top 20 grossing simple AI utility apps and their exact keyword/pricing strategies
- [ ] 2. Build 3 AI wrapper apps using existing app factory Capacitor templates: (a) AI Search (OpenRouter/Claude API wrapper), (b) Doc Scanner (camera + OCR + Claude summarize), (c) AI Chat (Claude API with persona presets)
- [ ] 3. Implement freemium subscription model: 3 free uses/day, $4.99/week or $29.99/year unlock
- [ ] 4. ASO optimize all 3 listings with Claude-generated localized descriptions in 15 languages
- [ ] 5. Submit to App Store (requires existing Apple Developer account — already have from scripture-streak apps)
- [ ] 6. Set up weekly cron to monitor competitor rankings and rotate ASO keywords
- [ ] 7. Generate 10 TikTok/Shorts scripts per app showing real use cases for organic distribution
- [ ] 8. Cross-promote across existing 47 deployed apps via in-app banners

## Tooling

```json
{
  "browser": "playwright for App Store scraping",
  "email": "none",
  "content": "content_factory for app marketing posts"
}
```
