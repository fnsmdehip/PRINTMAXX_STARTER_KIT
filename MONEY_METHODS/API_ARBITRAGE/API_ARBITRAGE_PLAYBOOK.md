# API Arbitrage Products Playbook

**OP_ID:** N54 + D09 (combined)
**Revenue Range:** $500-$10K/mo
**Automation Level:** High (build once, runs on autopilot)
**Phase:** 1 (launch fast, iterate)
**Status:** NEW

---

## What This Is

Wrap free or cheap APIs into paid products with better UX, simpler onboarding, and niche-specific features. non-technical users will pay $10-$50/mo to NOT deal with API documentation, authentication, rate limits, and JSON responses.

the edge: most APIs are built for developers. 99% of business users can't use them. you're the translation layer between raw API and usable product. Claude Code builds the wrapper in hours. the API provider handles all the hard infra.

this is the modern version of buying wholesale and selling retail. the "wholesale" is a free API. the "retail" is a $29/mo SaaS with a nice UI.

---

## Market Reality (2026)

- RapidAPI: 40K+ APIs listed. Most have free tiers that cover significant usage.
- OpenAI API cost: $0.001-$0.03 per request. Sell access for $0.10-$1.00 equivalent in a paid wrapper. 10-100x markup.
- Companies pay Clearbit $99-$999/mo for data enrichment. The same data is available free via Hunter.io free tier + LinkedIn scraping + Google search.
- Weather API: free from OpenWeatherMap. Companies pay $49-$499/mo for "weather intelligence platforms" that wrap the same data with dashboards.
- Google Maps API: $0.005-$0.01 per request. "Store locator" SaaS products charge $29-$99/mo for a widget that makes 100 API calls/day.

**Key insight:** the value isn't the data. the value is NOT HAVING TO THINK ABOUT THE DATA. a dashboard that shows "your competitors changed their prices today" is worth $49/mo even if the underlying API call costs $0.001.

---

## Revenue Model

### Tier 1: Single API Wrappers ($9-$29/mo SaaS)
- One API, one use case, beautiful UI
- Examples: "Track your competitors' pricing," "Monitor your brand mentions"
- Build time: 4-8 hours with Claude Code
- **Target: 20-100 users = $180-$2.9K/mo**

### Tier 2: Multi-API Aggregators ($29-$79/mo SaaS)
- Combine 3-5 APIs into one dashboard
- Examples: "Complete competitor intelligence" (pricing + social mentions + job postings + tech stack)
- Build time: 20-40 hours
- **Target: 10-50 users = $290-$3.95K/mo**

### Tier 3: API-Powered Tools ($49-$199/mo or one-time $97-$497)
- Full application built on APIs
- Examples: "AI email writer that pulls your brand voice from your website"
- Build time: 40-80 hours
- **Target: 10-30 users = $490-$5.97K/mo**

### Tier 4: White-Label API Products ($500-$2K/mo B2B)
- Sell API-powered features to businesses who embed in their own products
- Build time: 40-80 hours
- **Target: 2-5 B2B clients = $1K-$10K/mo**

---

## The 15 Most Profitable API Arbitrage Opportunities

### Category 1: Data Enrichment (Highest Margin)

**1. Company Intelligence API -> "Competitor Tracker" SaaS ($29/mo)**
- Free APIs: Clearbit (limited free), Hunter.io (25 free/mo), BuiltWith (limited free)
- Wrap into: dashboard that tracks competitors' tech stack, employee count, social presence
- Sell to: SaaS companies, marketing agencies
- Cost per user: ~$0.50/mo in API calls
- **Margin: 97%**

**2. LinkedIn Data -> "Lead Enrichment Tool" ($19/mo)**
- Source: Proxycurl API (free tier: 10 credits/mo, paid: $0.01/request)
- Wrap into: Upload CSV of names/companies, get back enriched data
- Sell to: Sales teams, recruiters
- Cost per user: ~$2/mo in API calls
- **Margin: 89%**

**3. Domain Intelligence -> "Website Analyzer" ($9/mo)**
- Free APIs: WHOIS, BuiltWith (limited), PageSpeed Insights, SecurityTrails (free tier)
- Wrap into: Enter any URL, get full report (tech stack, performance, SEO score, security)
- Sell to: Agencies, freelancers, SEO professionals
- Cost per user: ~$0.10/mo
- **Margin: 99%**

### Category 2: AI Wrappers (Fastest to Build)

**4. Claude/GPT API -> Niche AI Tool ($14.99/mo)**
- Cost: Claude API ~$0.003/request (Haiku) to $0.075 (Opus)
- Wrap into: "AI [Industry] Assistant" with pre-loaded industry knowledge
- Examples: "AI Legal Brief Writer," "AI Real Estate Description Generator," "AI Restaurant Menu Creator"
- Cost per user: ~$1-$5/mo in API calls
- **Margin: 70-93%**

**5. Claude API + Scraper -> "AI Research Assistant" ($29/mo)**
- Scrape target URL/document + Claude summarization
- Sell to: Consultants, VCs, analysts
- Cost per user: ~$3/mo
- **Margin: 90%**

**6. Whisper API -> "Meeting Transcription + Action Items" ($19/mo)**
- OpenAI Whisper API: $0.006/minute
- Upload recording, get transcript + summary + action items
- Sell to: Remote teams, consultants
- Cost per user: ~$2/mo
- **Margin: 89%**

### Category 3: Content Tools (Highest Volume)

**7. Social Media APIs -> "Content Performance Tracker" ($19/mo)**
- Free APIs: Twitter API free tier, Instagram Graph API, YouTube Data API
- Track social performance across platforms in one dashboard
- Sell to: Creators, small businesses, agencies
- Cost per user: ~$0.20/mo
- **Margin: 99%**

**8. Stock Photo APIs -> "AI Image Finder" ($9/mo)**
- Free APIs: Unsplash (50 req/hr), Pexels (200/hr), Pixabay (unlimited)
- Describe what you need, AI finds best match across all free stock sites
- Sell to: Bloggers, marketers, social media managers
- Cost per user: ~$0.10/mo
- **Margin: 99%**

### Category 4: Business Tools (Highest Retention)

**9. Google Sheets API + Claude -> "Smart Spreadsheet" ($14.99/mo)**
- Google Sheets API: free
- Ask questions about spreadsheet data in plain English
- Sell to: Small business owners, analysts
- Cost per user: ~$1/mo
- **Margin: 93%**

**10. Stripe API -> "Financial Dashboard for Freelancers" ($9/mo)**
- Stripe API: free
- Connect Stripe, see revenue trends, client analytics, tax estimates
- Sell to: Freelancers, solopreneurs
- Cost per user: ~$0 (Stripe API is free)
- **Margin: ~100% minus hosting**

**11. Email Verification APIs -> "Email Cleaner" ($9/mo)**
- APIs: Hunter.io (25 free/mo), ZeroBounce (100 free), Mailgun validation
- Upload list, get back verified emails with confidence score
- Sell to: Cold emailers, marketers
- Cost per user: ~$0.50/mo
- **Margin: 94%**

### Category 5: Monitoring Tools (Best for Recurring Revenue)

**12. Price Monitoring -> "Competitor Price Tracker" ($29/mo)**
- Build scraper (Playwright) + change detection
- Monitor competitor websites for price changes, new products
- Sell to: Ecom, SaaS, agencies
- Cost per user: ~$1/mo
- **Margin: 97%**

**13. Uptime/Performance API -> "Website Monitor" ($9/mo)**
- Free alternatives: UptimeRobot (50 free monitors), StatusCake (10 free)
- Premium monitoring with AI-powered incident analysis
- Sell to: Web agencies, SaaS companies
- Cost per user: ~$0.50/mo
- **Margin: 94%**

**14. Google Alerts API + Claude -> "News Intelligence" ($19/mo)**
- Google Alerts: free. NewsAPI.org: free tier 100 requests/day.
- Track any topic, get daily AI-curated digest with analysis
- Sell to: PR firms, marketers, executives
- Cost per user: ~$0.50/mo
- **Margin: 97%**

**15. Government Data APIs -> "Grant/Contract Finder" ($29/mo)**
- SAM.gov API: free. Grants.gov API: free. USASpending API: free.
- AI-filtered government opportunity alerts matching your profile
- Already have gov contract scraping built (AUTOMATIONS/)
- Sell to: Government contractors, small businesses
- Cost per user: ~$0.50/mo
- **Margin: 98%**

---

## Tech Stack

| Layer | Tool | Cost |
|-------|------|------|
| Frontend | Next.js or Lovable.dev | $0 |
| Backend | Vercel serverless functions or Railway | $0-$5/mo |
| Database | Supabase (free tier: 500MB) | $0 |
| Auth | Supabase Auth or Clerk (free tier) | $0 |
| Payments | Stripe | 2.9% + $0.30/tx |
| API calls | Various free tiers | $0-$5/mo per product |
| **Total startup cost** | | **$0** |

---

## Build Process (Per Product)

### Phase 1: Validate (Day 1)
```
1. Identify API with free tier that solves a real problem
2. Check: who would pay for a nicer version of this?
3. Search Twitter/Reddit: are people complaining about this problem?
4. Check existing solutions: what do competitors charge?
5. If competitor charges $50+/mo and API is free: green light
```

### Phase 2: Build MVP (Day 2-3)
```
1. Claude Code: "Build a Next.js app that [wraps this API]"
2. Minimum features:
   - Sign up / sign in (Supabase Auth)
   - Connect API / enter data
   - Display results in clean dashboard
   - Export to CSV/PDF
3. Deploy on Vercel free tier
4. Add Stripe checkout ($X/mo subscription)
```

### Phase 3: Launch (Day 4-5)
```
1. ProductHunt launch
2. Reddit post in relevant subreddit
3. X thread: "I built [tool] in 3 days. It uses [free API] under the hood."
4. Hacker News "Show HN" (if technical enough)
5. List on Indie Hackers products
```

### Phase 4: Iterate (Week 2+)
```
1. Check: are people signing up?
2. If yes: add features, add more API integrations
3. If no: pivot to different niche or different API
4. Add AI layer (Claude API) for analysis/insights on top of raw data
5. Build referral program (30% commission)
```

---

## The Portfolio Approach

Don't build one product. Build 5-10. each takes 2-3 days. most will fail. 1-2 will stick. those 1-2 fund everything else.

**Target portfolio:**
- Month 1: Build 3 products, launch all 3
- Month 2: Kill losers (< 5 signups), double down on winner, build 2 more
- Month 3: Optimize winner, build 2 more
- Month 6: 2-3 products generating $500-$3K/mo each

**The math:** 10 products x $500/mo average = $5K/mo. Most products cost $0/mo to run.

---

## Pricing Strategy

| User Type | Sweet Spot |
|-----------|-----------|
| Solopreneurs | $9-$14.99/mo |
| Small businesses (1-10) | $19-$49/mo |
| Agencies | $49-$99/mo |
| Enterprise | $199-$499/mo |

**Pricing rules:**
1. Annual plan at 2 months free (improves cash flow, reduces churn)
2. Free tier with usage limits (drives signups, upgrades to paid)
3. Never compete on price with enterprise tools. Compete on simplicity.
4. If API cost per user < 5% of subscription price, you're golden.

---

## Finding API Opportunities (Ongoing)

### Where to find APIs
- RapidAPI.com - 40K+ APIs with free tiers
- Public-APIs GitHub repo (github.com/public-apis/public-apis) - 1,400+ APIs
- ProgrammableWeb.com - API directory
- Any SaaS company's developer docs page

### Red flags (avoid)
- Unstable/frequently changing
- No free tier
- Rate limits too low
- Deprecated or unmaintained
- Requires business verification

### Green flags (build on these)
- Generous free tier (1K+ requests/day)
- Stable, well-documented
- Large company backing (Google, Microsoft, Stripe)
- Data that non-technical users want but can't access
- No good consumer-facing product built on it yet

---

## Example: Full Build Walk-Through

**Product:** "PriceHawk" - Competitor Price Monitor
**API:** Custom scraper (Playwright) + ChangeDetection.io API (free self-hosted)
**Target:** Ecommerce businesses
**Price:** $29/mo

**Build (8 hours):**
1. Next.js frontend with Supabase backend
2. User enters competitor URLs
3. Scraper checks daily for changes
4. Claude API analyzes changes and generates insights
5. Email alert when significant change detected
6. Dashboard shows history + trends

**Cost per user:** ~$1/mo
**Margin:** 97%
**Break-even:** 1 user

**Launch sequence:**
1. Post on r/ecommerce
2. ProductHunt launch
3. X thread showing before/after screenshots
4. Cold email 50 Shopify stores

---

## Synergy Map

| Stack With | How |
|-----------|-----|
| D12 (MCP Server Marketplace) | Build MCP servers that wrap APIs. Sell to Claude users. |
| S04 (Automation Agency) | API products upsold: "want me to integrate with your other tools?" |
| MM004 (SaaS) | Every API wrapper IS a micro-SaaS. Fastest path to MRR. |
| N37 (AI Workflow Marketplace) | API-powered workflows sold as templates. |
| D13 (AI Agent Service) | Agents that use API wrappers. Recursive value. |
| N53 (ProductHunt Launch) | Launch each product for free exposure. |

---

## Content Strategy

1. **X:** "I built [tool] in 3 days using a free API. It now makes $X/mo."
2. **Reddit:** r/SaaS, r/SideProject - "How I turned a free API into a $X/mo business"
3. **Indie Hackers:** Product launch + journey documentation
4. **ProductHunt:** Launch each product
5. **YouTube:** "Build a SaaS in 48 hours using free APIs" tutorial
6. **Medium:** "The API Arbitrage Playbook" article

---

## KPIs

| Metric | Month 1 | Month 3 | Month 6 |
|--------|---------|---------|---------|
| Products built | 3 | 6-8 | 10-12 |
| Products with revenue | 0-1 | 1-3 | 2-4 |
| Total MRR | $0-$200 | $500-$2K | $2K-$10K |
| Signups (free tier) | 20-50 | 100-300 | 500+ |
| Paid users | 0-10 | 20-60 | 50-150 |
| Churn rate | N/A | < 10%/mo | < 8%/mo |
| API cost as % of revenue | N/A | < 5% | < 3% |

---

## Quick Start Checklist

- [ ] Browse RapidAPI and Public-APIs for 5 promising APIs with free tiers
- [ ] Validate demand: search Twitter/Reddit for complaints
- [ ] Pick top 3 by: demand + ease of build + margin
- [ ] Build MVP #1 with Claude Code (Next.js + Supabase + Vercel)
- [ ] Add Stripe payments
- [ ] Launch on ProductHunt + Reddit + X
- [ ] Build MVP #2 and #3
- [ ] Kill products with < 5 signups after 2 weeks
- [ ] Double down on winner
- [ ] Document journey for content (build-in-public)
