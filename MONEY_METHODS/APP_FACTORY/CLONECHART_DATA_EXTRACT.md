# CloneChart.io Data Extract

**Date Extracted:** 2026-02-10
**Source:** https://clonechart.io/ (data gathered via web search snippets - direct page fetch was blocked)
**Last Site Update:** February 09, 2026 at 10:20 AM UTC
**Database Size:** 12,000+ iOS apps (previously listed as 9,000+, expanded)

---

## EXTRACTION METHOD NOTE

WebFetch and curl were both permission-blocked during this session. All data below was extracted from web search engine snippets, cached metadata, and indexed page content. This represents partial data from what the full site contains. To get the COMPLETE dataset (all 12,000+ apps), the site needs to be scraped directly via browser or curl.

**To complete extraction, run:**
```bash
curl -sL "https://clonechart.io/" | python3 -c "import sys; print(sys.stdin.read())" > /tmp/clonechart_raw.html
curl -sL "https://clonechart.io/chart/browse?show=1000" > /tmp/clonechart_browse.html
```

---

## Platform Overview

- **Tagline:** "Discover Top Grossing iOS Apps to Clone"
- **Target Audience:** "Vibe coders" (AI-assisted app developers)
- **Core Features:**
  - AI-generated clone prompts for each app
  - Revenue estimates per app
  - Tech analysis / tech stack breakdown
  - Clone difficulty ratings
  - Daily data updates
  - Browse/filter by category
  - Save apps for later cloning

---

## URL Structure

| Page | URL |
|------|-----|
| Homepage (Top Grossing) | `https://clonechart.io/` |
| Browse (1000 apps view) | `https://clonechart.io/chart/browse?show=1000` |
| Browse (other quantities) | `?show=100`, `?show=250`, `?show=500` |
| Likely app detail pattern | `https://clonechart.io/app/{app-id}` or `/chart/{app-id}` (unconfirmed) |

---

## Clone Difficulty Ratings

| Rating | Icon | Meaning |
|--------|------|---------|
| Easy to Clone | Green circle | Simple app, replicable with AI tools |
| Medium | Yellow circle | Moderate complexity |
| Hard (Avoid) | Red circle | Complex, not worth cloning |

---

## App Categories (24 Categories Confirmed)

1. Finance
2. Productivity
3. Health & Fitness
4. Lifestyle
5. Utilities
6. Business
7. Education
8. Entertainment
9. Food & Drink
10. Shopping
11. Travel
12. Social Networking
13. Photo & Video
14. Music
15. News
16. Sports
17. Weather
18. Books
19. Medical
20. Navigation
21. Reference
22. Games
23. Graphics & Design
24. Developer Tools

---

## App Pricing Models Tracked

- Free (with In-App Purchases)
- Paid ($1.99, $2.99, $6.99, etc.) with or without In-App Purchases
- Subscription-based

---

## Specific App Data Extracted (From Search Snippets)

### Top Revenue Apps (Confirmed from snippets)

| App | Category | Developer | Rating | Est. Revenue | Price Model |
|-----|----------|-----------|--------|-------------|-------------|
| ChatGPT | Productivity | OpenAI | - | $9.0M | Free + IAP |
| Minecraft | Games | Mojang | - | $5.6M | Paid + IAP |
| Google (Photo & Video app) | Photo & Video | Google | 4.8 | $804K | Free + IAP |
| Meta app | Social Networking | Meta Platforms, Inc. | 4.5 | $307K | Free + IAP |
| OxbowSoft Finance App | Finance | OxbowSoft LLC | 4.7 | $173K | Free + IAP |
| Valenyr Finance App | Finance | Valenyr Information Technology Consultants FZCO | 4.7 | $172K | Free + IAP |
| Tantsissa Health App | Health & Fitness | Tantsissa | 4.7 | $150K | Free + IAP |
| ANI Trading / Penny Trade Alert | Finance | - | 4.2 | - | Free + IAP |
| Vivid Stock Market Alerts | Finance | - | 4.3 | - | Free + IAP |

### Finance Category (181 apps confirmed in category)

Confirmed apps in Finance category:
- OxbowSoft LLC app (4.7 stars, $173K est. revenue, Free + IAP)
- Valenyr Information Technology Consultants FZCO app (4.7 stars, $172K est. revenue, Free + IAP)
- ANI Trading Real Time Stocks Options Crypto (4.2 stars)
- Penny Trade Alert & Signal Advisory
- Vivid Stock Market Alerts Stocks & Options Trading Signals & Crypto Forex Signal for Swing Trader (4.3 stars)

---

## How Clone Prompts Work

Based on search data, the platform:
1. Lists each app with its metadata (name, developer, rating, revenue, pricing)
2. Has a "Clone" button on each app listing
3. Clicking generates an AI prompt designed for vibe coding tools
4. Prompts are compatible with AI coding assistants (Claude, ChatGPT, Cursor, etc.)
5. Prompts include tech analysis of the original app
6. Users can save apps to a list for later cloning

---

## Recommended Development Tools (Listed on Site)

The site recommends these tools for building clones:
- **Railway** - Backend hosting/deployment
- **Supabase** - Database & auth (open-source Firebase alternative)
- **Vercel** - Frontend hosting/deployment
- **Firebase** - Google's BaaS platform

---

## Pricing Information

**NOT CONFIRMED from search data.** No specific pricing tiers, free vs paid plans, or subscription costs were visible in any search snippets. The site may be:
- Free to browse with limited features
- Freemium (free browse, paid for clone prompts)
- Fully paid subscription

**Action needed:** Visit site directly to confirm pricing model.

---

## Potential API Endpoints (Speculative)

Based on URL patterns and typical SaaS architecture:
- `https://clonechart.io/api/apps` - App listing API
- `https://clonechart.io/api/apps/{id}` - Individual app data
- `https://clonechart.io/api/categories` - Category listing
- `https://clonechart.io/api/clone-prompt/{id}` - Clone prompt generation
- `https://clonechart.io/chart/browse?show={count}&category={category}` - Filtered browse

**NOTE:** These are SPECULATIVE based on common patterns. None confirmed from source code inspection. Need direct page source access to verify.

---

## Data Quality Assessment

| Metric | Assessment |
|--------|-----------|
| Revenue estimates | Likely based on Sensor Tower / Appfigures / similar data providers |
| Update frequency | Daily (confirmed on site) |
| Coverage | 12,000+ iOS apps (US App Store focus) |
| Difficulty ratings | 3 tiers (Easy/Medium/Hard) - methodology unknown |
| Clone prompts | AI-generated, quality unknown |

---

## PRINTMAXX Action Items

### Immediate (Complete Extraction)
1. **Browser scrape needed:** Open clonechart.io in Chrome, use DevTools Network tab to find API endpoints
2. **Full data dump:** Once API found, pull all 12,000+ apps with revenue/difficulty data
3. **Filter for easy clones with $50K+ revenue:** These are the money targets

### Strategic Uses
1. **Cross-reference with our APP_CLONE_OPPORTUNITIES.csv** - Find overlap and new opportunities
2. **Revenue validation** - Compare their estimates against Sensor Tower / AppMagic data
3. **Clone prompt extraction** - Get the AI prompts for top 50 easy-to-clone apps with highest revenue
4. **Category analysis** - Which categories have the most "easy to clone" high-revenue apps?
5. **Niche targeting** - Filter for faith, fitness, productivity niches that align with our portfolio

### High-Priority Clone Targets (Based on Extracted Data)

Finance niche apps ($150K-$173K revenue range with 4.7 star ratings) appear to be solid clone targets. Specific opportunities:
- Stock alert / trading signal apps (multiple in $150K+ range)
- The Finance category alone has 181 tracked apps

Photo & Video apps show highest individual revenue ($804K for Google's app) but likely harder to clone.

Health & Fitness apps ($150K range, Tantsissa) align with our fitness niche (WalkToUnlock, BioMaxx).

### Competitive Intelligence
- CloneChart itself is a product worth studying - it is a "vibe coder tool" SaaS
- 12,000+ app database = significant data moat
- Daily updates = automated pipeline (likely App Store Connect API + revenue estimation model)
- This exact product model could be replicated for Android (Google Play) or for specific niches

---

## Raw Search Snippets (For Verification)

### Snippet 1 (Homepage metadata)
"CloneChart.io - 12,000+ iOS Apps, Updated Daily"
"Discover Top Grossing iOS Apps to Clone. AI-generated prompts, revenue estimates, and tech analysis for vibe coders."

### Snippet 2 (Browse page)
"CloneChart.io - 9,000+ iOS Apps, Updated Daily" (older cache, now 12,000+)
URL: clonechart.io/chart/browse?show=1000

### Snippet 3 (Finance data)
Finance category: 181 apps
- OxbowSoft LLC | 4.7 stars | $173K est. revenue | Free + In-App Purchases
- Valenyr Information Technology Consultants FZCO | 4.7 stars | $172K est. revenue | Free + IAP
- ANI Trading Real Time Stocks Options Crypto and Penny Trade Alert & Signal Advisory | 4.2 stars
- Vivid Stock Market Alerts Stocks & Options Trading Signals & Crypto Forex Signal for Swing Trader | 4.3 stars

### Snippet 4 (Top revenue)
- OpenAI (Productivity) | $9.0M estimated revenue
- Mojang (Games) | $5.6M estimated revenue

### Snippet 5 (Photo & Video / Social)
- Google (Photo & Video) | 4.8 stars | $804K estimated revenue
- Meta Platforms, Inc. (Social Networking) | 4.5 stars | $307K estimated revenue

### Snippet 6 (Health & Fitness)
- Tantsissa (Health & Fitness) | 4.7 stars | $150K estimated revenue

### Snippet 7 (Paid apps)
Some apps priced at $6.99, $2.99, $1.99 with additional in-app purchases

### Snippet 8 (Dev tools recommended)
Site recommends: Railway, Supabase, Vercel, Firebase for building clones

---

## NEXT STEPS FOR COMPLETE DATA EXTRACTION

The search-based extraction captured ~10 specific apps with data points. The full site has 12,000+ apps. To get complete data:

1. **Method 1: Browser DevTools**
   - Open clonechart.io in Chrome
   - Open Network tab
   - Browse the app list and watch for API calls
   - Copy the API endpoint and use it to pull all data

2. **Method 2: Page scrape with Playwright**
   ```python
   # Scroll through all apps on browse page and extract table data
   # clonechart.io/chart/browse?show=1000
   ```

3. **Method 3: Manual Chrome + copy-paste**
   - Open clonechart.io/chart/browse?show=1000
   - Select all visible table data
   - Copy to spreadsheet
   - Repeat for each category filter

4. **Method 4: curl (when network access available)**
   ```bash
   curl -sL "https://clonechart.io/" > /tmp/cc_home.html
   curl -sL "https://clonechart.io/chart/browse?show=1000" > /tmp/cc_browse.html
   # Parse HTML for app data
   ```

**Priority:** Method 1 (browser DevTools to find API) is fastest path to complete data.
