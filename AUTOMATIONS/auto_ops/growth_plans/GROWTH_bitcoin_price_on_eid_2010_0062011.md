# Growth Plan: Bitcoin Price on Eid 

2010: $0.06
2011: $3
2012: $5
2013: $

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo direct (affiliate crypto exchange clicks) + audience building for Hilal/PrayerLock cross-sell

---

## Tactics

1. Post NOW during Ramadan — Muslim crypto Twitter is primed for this exact content, high share velocity
2. Tag WatcherGuru original post as QT with added angle (Hilal app cross-promo)
3. Expand template to Eid al-Adha, Ramadan start, Laylat al-Qadr — 4 posts per year per coin
4. Replicate format for ETH, SOL — '3 coins on Eid every year' triple-data post
5. Cross-post in r/islam + r/Bitcoin + r/CryptoCurrency during Eid countdown
6. Pin to Hilal app Twitter account as social proof that crypto + faith audience exists
7. Automate for ALL major religious holidays: Christmas, Diwali, Chinese New Year, Hanukkah — 8 niches x 15 years = 120 viral posts
8. Create 'Save this for next Eid' CTA to drive bookmarks (boosts algo reach)
9. Wire into PrayerLock/Hilal promotion — faith audience already engaged

## Budget Tier Strategies

### FREE
Post from @printmaxxer during Ramadan peak hours (7-9 PM EST), QT the original WatcherGuru post, cross-post to faith subreddits, use engagement_bait_converter.py to generate 5 platform variants per post. Expand to all 8 religious calendars automatically.

### LOW
$0-50/mo: Boost 1 top-performing post per week on Twitter ($5-10/boost) during Ramadan window. Target: Muslim crypto accounts, Islamic finance hashtags.

### MID
$50-200/mo: Sponsor placement in 2-3 Muslim crypto Telegram groups (50K+ members). Wire affiliate link to crypto exchange with Sharia-compliant trading option.

## Daily Actions

- [ ] pip3 install hijri-converter requests — both free, no API key needed
- [ ] Build religious_calendar_btc_content.py: calculate Eid al-Fitr dates 2010-2026 via hijri-converter, fetch BTC close price on each date from CoinGecko /history endpoint, format as 3 variants (thread, single tweet, IG caption)
- [ ] Extend to 8 calendars: Eid x2, Ramadan start, Christmas, Diwali, Chinese New Year, Hanukkah, Vesak — same script, config-driven
- [ ] Pipe output to CONTENT/social/posting_queue/ as time-stamped files
- [ ] Run immediately for Ramadan 2026 content (time-critical, 25 days left)
- [ ] Add to cron 0 7 * * * to auto-generate for upcoming holidays
- [ ] Wire Hilal app URL into post CTA — 'Track Ramadan with Hilal: [url]'

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py",
  "data": "CoinGecko free API (historical OHLC, no key needed) + hijri-converter PyPI package for Islamic calendar dates"
}
```
