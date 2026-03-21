# Growth Plan: I made a Tinder like app that you can discover and star repo

**Created:** 2026-03-20 18:09
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo

---

## Tactics

1. Post to r/SideProject, r/webdev, r/github, r/programming with 'I built this' framing
2. Cross-post to HN Show HN for developer audience
3. Tweet build thread from tech account showing swipe UX in action (screen recording GIF)
4. Submit to Product Hunt as developer tool
5. Template the swipe UI so we can launch Tinder-for-MCP-servers, Tinder-for-AI-tools as fast follows

## Budget Tier Strategies

### FREE
Reddit Show posts across 4 dev subreddits, HN Show HN, Twitter build thread with screen recording, GitHub repo with demo link in README, Product Hunt launch

### LOW
$10-30 Reddit promoted post targeting r/programming, dev newsletter sponsorship swap

### MID
$50-100 targeted dev Twitter ads, ProductHunt featured launch slot, indie hacker community sponsorship

## Daily Actions

- [ ] Build reusable swipe-card PWA template using existing app factory base (HTML/CSS/JS, no framework)
- [ ] Wire GitHub API (unauthenticated: 60 req/hr, sufficient for daily refresh of ~50 trending repos)
- [ ] Daily cron scrapes GitHub trending + topics API, outputs swipe_cards.json
- [ ] PWA loads JSON, renders swipe UI with repo name, description, stars, language, screenshot
- [ ] Swipe right = star (localStorage initially, Firebase sync for accounts later)
- [ ] Deploy to surge.sh as repo-swipe.surge.sh
- [ ] Clone template for 2-3 variants: mcp-swipe (MCP servers), tool-swipe (AI tools), project-swipe (indie projects)
- [ ] Distribute via Reddit/HN/Twitter build threads

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory for launch posts and build threads"
}
```
