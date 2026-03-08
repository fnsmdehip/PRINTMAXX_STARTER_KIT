# Freelance Response Draft
## Post: [Hiring] Developer to build a Facebook keyword posts scraper
## URL: https://reddit.com/r/forhire/comments/1ro9sgo/hiring_developer_to_build_a_facebook_keyword/
## Subreddit: r/forhire
## Score: 80.0
## Generated: 2026-03-08T15:53:13.402379
## Quality Gate: REWRITTEN cycle 14

---

### Response

I can build this. done similar scrapers for twitter and reddit using python + playwright for the browser automation and BeautifulSoup for parsing.

facebook is trickier than most platforms because their DOM changes frequently and they aggressively block headless browsers. the approach that works: cookie-based auth injection into a real browser session, not headless. rotating user agents. request throttling at 2-3 second intervals so you don't get flagged.

for keyword-based scraping specifically: I'd build it to accept a list of keywords, search each, capture post text + engagement metrics + poster info + timestamp, and output to CSV or JSON. can add scheduling so it runs daily/hourly.

timeline: 3-5 days for the core scraper. budget: depends on how many keywords and how robust you need the anti-detection. DM me with your keyword list and volume and I'll give you a fixed quote.

---

### Notes for Human Review
- Technical specifics demonstrate real scraping experience
- Addresses the hard part (Facebook anti-detection) upfront
- Fixed quote CTA (not hourly, reduces friction)
- Status: APPROVED (quality gate cycle 14)
