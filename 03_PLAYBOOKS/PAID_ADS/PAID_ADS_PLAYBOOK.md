# Paid Ads Playbook

**Created:** 2026-01-23
**Purpose:** Paid acquisition for app installs, info products, lead gen
**Budget:** Start small ($50-100/day), scale winners

---

## Alpha from Extracted Tweets

### 1. FB Ads Library Product Research (@xivy0k)
**Source:** ALPHA_AUDIT_2026-01-20.md

Search FB Ads Library for these keywords to find winning products:
- Ebook, Digital Download, Instant PDF
- Printable, Template, Guide, Course
- Planner, Editable, Tracker
- Worksheets, Cheat Sheet

**Logic:** If they're paying for ads, they're making money. Clone what works.

**URL:** https://www.facebook.com/ads/library

### 2. Bidcap Meta Ads Strategy (@CEOLandshark)
**Source:** ALPHA_STAGING.csv

Set budget caps on Meta ads to control spend while testing. Prevents runaway costs during learning phase.

### 3. Organic → Paid Pipeline (@lottsnomad)
**Source:** WINNING_CONTENT_STRUCTURES.csv

Framework:
1. Post same video idea with 10 different hooks on TikTok organic
2. See which hook gets traction (free testing)
3. Take winning hook → run as paid ad
4. Scale winners only

**Key insight:** TikTok organic = free hook testing. Validate before spending.

### 4. UGC Campaign Formula (@alexcooldev)
**Source:** SCRAPED_TWEETS_ALPHA.csv

"Build the app. Post daily. Use UGC campaigns. Market more than you build."

Ratio: More marketing than building. UGC scales better than polished content.

---

## Platform Playbooks

### Meta (Facebook/Instagram)

**Best for:**
- App installs (iOS/Android)
- Info product sales
- Lead gen for services

**Ad Types:**
1. **UGC Style** - Native looking, not polished
2. **Hook-Problem-Demo** - 30 sec format
3. **Testimonial Mashup** - Multiple quick testimonials

**Targeting:**
- Lookalike audiences from email list
- Interest stacking (combine 3-5 related interests)
- Retargeting website visitors

**Budget:**
- Testing: $20-50/day per ad set
- Scaling: $100-500/day on winners

**Metrics to Track:**
- CPM (Cost per 1000 impressions): Target <$15
- CTR (Click-through rate): Target >1.5%
- CPI (Cost per install): Target <$2 for apps
- ROAS (Return on ad spend): Target >2x

### TikTok Ads

**Best for:**
- App installs (younger demos)
- UGC-style content
- Viral potential

**Ad Types:**
1. **Spark Ads** - Boost organic posts that perform
2. **In-Feed Native** - Looks like regular content
3. **TopView** - Premium placement (expensive)

**Creative Guidelines:**
- First 2 seconds = hook or scroll
- Vertical video only (9:16)
- Use trending sounds
- Look native, not polished

**Budget:**
- Minimum: $50/day per campaign
- Testing: $100-200/day
- Scaling: $500+/day

### Google Ads

**Best for:**
- App Store search ads (ASA alternative)
- Intent-based keywords
- Retargeting

**Campaign Types:**
1. **App Campaigns** - Automated for installs
2. **Search** - Keyword targeting
3. **Display** - Retargeting

---

## UGC Sourcing

### Cheap UGC Sources (from Alpha)
- @dansugcmodels - $3-20/video roster
- @franci__ugc - UGC sourcing tactics
- Fiverr UGC creators - $10-30/video
- Billo - $99/video average
- Insense - Marketplace for UGC

### UGC Brief Template

```markdown
# UGC Brief: [Product Name]

## Hook Options (pick one)
1. "I was struggling with [problem]..."
2. "I never thought I'd [outcome]..."
3. "Okay but why did no one tell me about this?"

## Script (30 seconds)
- 0-3s: Hook (must stop scroll)
- 3-10s: Problem/struggle
- 10-20s: Discovery + demo
- 20-27s: Result/transformation
- 27-30s: CTA

## Deliverables
- 3 variations (different hooks)
- Raw footage + edited version
- Vertical 9:16 format
- Good lighting, authentic setting

## Don't
- Sound scripted
- Use professional lighting
- Look like an ad
```

---

## Testing Framework

### Phase 1: Creative Testing ($100-300)

1. Create 5 different hooks for same product
2. Run each as separate ad
3. $20/day per ad for 3 days
4. Kill losers (CTR <1%, CPM >$20)
5. Scale winners

### Phase 2: Audience Testing ($200-500)

1. Take winning creative
2. Test 5 different audiences
3. Compare CPI across audiences
4. Double down on best performers

### Phase 3: Scale ($500+/day)

1. Increase budget 20% every 2-3 days
2. Monitor for fatigue (CTR drops)
3. Refresh creative every 2-4 weeks
4. Build lookalike audiences from converters

---

## Budget Allocation by Method

| Method | Platform | Daily Budget | CPA Target |
|--------|----------|--------------|------------|
| APP_FACTORY | TikTok + Meta | $100-300 | <$2 CPI |
| INFO_PRODUCTS | Meta + Google | $50-200 | <$50 CPA |
| COLD_OUTBOUND | LinkedIn | $50-100 | <$20 CPL |
| AI_INFLUENCER | TikTok | $20-50 | Profile follows |

---

## Tracking Setup

### Required:
- [ ] Meta Pixel installed
- [ ] TikTok Pixel installed
- [ ] Google Analytics 4
- [ ] Conversion events defined
- [ ] UTM parameters on all links

### Attribution:
- Use unique landing pages per platform
- Track: Click → Lead → Customer → LTV
- Calculate true ROAS including all costs

---

## Compliance Checklist

- [ ] "Ad" or "Sponsored" label visible
- [ ] AI disclosure if using synthetic content
- [ ] Affiliate disclosure if promoting products
- [ ] No misleading income claims
- [ ] Testimonials are real and substantiated
- [ ] Landing page matches ad claims

---

## Quick Start (First $100)

1. Pick one winning organic post
2. Turn into Spark Ad on TikTok ($50)
3. Run for 3 days
4. If CPI <$3, scale
5. If CPI >$5, try different hook
6. Parallel test on Meta ($50)
7. Compare results
8. Scale winner platform

---

## Resources

- FB Ads Library: https://www.facebook.com/ads/library
- TikTok Creative Center: https://ads.tiktok.com/business/creativecenter
- Foreplay.co - Ad swipe file tool
- AdSpy - Competitor ad research

---

## Files in This Folder

```
MONEY_METHODS/PAID_ADS/
├── PAID_ADS_PLAYBOOK.md (this file)
├── meta/
│   └── (Meta campaign assets)
├── tiktok/
│   └── (TikTok campaign assets)
├── google/
│   └── (Google campaign assets)
├── research/
│   └── (Competitor ad screenshots)
└── creatives/
    └── (UGC videos, images)
```
