# OPP-004: Local Business Review Management Micro-SaaS

**Score:** 8.0/10 (Fit: 8, Effort: 6, ROI: 9)
**Startup Cost:** $0
**Time to First Revenue:** 2-3 weeks
**Monthly Potential:** $2,000-$10,000 (recurring)
**Competition:** Low in $29-44/mo tier (gap between free and $259/mo enterprise)

## What

Build a review aggregation + response management tool for single-location small businesses. BrightLocal charges $44/mo per location. EmbedSocial starts at $259/mo. The $29-44/mo sweet spot for local shops, restaurants, clinics is wide open.

## Why Now

- Clear pricing gap: free tools vs $44-259/mo enterprise solutions
- Single-location businesses (restaurants, dentists, salons) underserved
- We already have local_biz_website_scraper rated 95/100 by SaaS opportunity engine
- Google Business Profile API, Yelp API available
- Micro-SaaS segment growing 30% annually ($15.7B → $59.6B by 2030)
- AI response generation = killer feature competitors lack at this price point

## How

1. Next.js dashboard: aggregate Google, Yelp, Facebook reviews in one view
2. AI-powered response suggestions (Claude API for tone-matched replies)
3. Sentiment tracking + weekly email digest
4. Price at $29/mo (single location) or $19/mo annual
5. Sell via cold outreach to local businesses (our outbound stack)

## Expected ROI

- Build time: 2-3 weeks for MVP
- 50 customers at $29/mo = $1,450/mo
- 200 customers at $29/mo = $5,800/mo
- LTV at 12mo avg retention: $348/customer
- Cold outbound CAC: ~$5-15/customer (email only)

## First 3 Steps

1. Build MVP: Google review aggregation + AI response suggestions (Next.js + Claude API)
2. Deploy to Vercel, create landing page with "manage all your reviews in one place" positioning
3. Cold email 100 local businesses using existing local_biz scraper data + outbound stack

## Stack Fit

Next.js + Python + Claude API + existing local_biz_scraper + cold outbound infrastructure. All pieces exist.
