# Growth Plan: https://reddit.com/r/SideProject/comments/1rvfp51/thesis_dis

**Created:** 2026-03-20 23:12
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo indirect (drives app installs, reduces CAC on streak apps by 30-40% vs paid)

---

## Tactics

1. Join servers as genuine member — answer questions in target niche for 2 weeks before any soft promotion
2. Create a dedicated #resources channel post with all PRINTMAXX app links as 'free tools for this community'
3. Use existing chain__met_a_girl_in_a_discord_server_who_said learnings — community warmth converts better than cold pitch
4. Cross-promote Discord presence on Twitter/X threads to drive server discovery
5. Target faith-based servers for Hilal, Scripture Streak, PrayerLock — Ramadan context makes this time-critical (25 days left)

## Budget Tier Strategies

### FREE
Manual server joins + value posting. Playwright scrapes Disboard for server lists. Claude generates value posts. Human posts 3x/week across top 10 servers per niche.

### LOW
$0-50/mo: Discord bot ($5/mo hosting) for automated welcome messages and resource drops in servers you own. MEE6 alternative.

### MID
$50-200/mo: Sponsored server listings on Disboard ($50+/mo). Discord Nitro boosts for your own community server to increase discoverability.

## Daily Actions

- [ ] Run discord_distribution_engine.py --discover to scrape Disboard for faith/fitness/productivity servers with >500 members
- [ ] Filter to top 20 servers per niche, save to LEDGER/DISCORD_SERVER_TARGETS.csv
- [ ] Generate value post templates per niche via claude -p, save to CONTENT/social/posting_queue/discord_*.txt
- [ ] HUMAN ACTION: Join top 5 servers per niche, post value content 3x before any app mention
- [ ] Wire UTM params (utm_source=discord&utm_medium=community) on all surge landing page links
- [ ] Cron weekly on Monday 9 AM to refresh server list and generate new value posts
- [ ] Track installs via KPI dashboard — if Discord drives >50 installs/week, escalate to MID budget tier

## Tooling

```json
{
  "browser": "playwright (Disboard scraping)",
  "email": "none",
  "content": "claude -p for value post generation, content_factory for cross-platform repurpose"
}
```
