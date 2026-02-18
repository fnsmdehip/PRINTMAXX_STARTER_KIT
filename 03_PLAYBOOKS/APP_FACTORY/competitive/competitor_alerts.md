# Competitor Alerts & Monitoring

**Last Updated:** 2026-01-21
**Purpose:** Systematic tracking of competitor moves with response playbooks

---

## What to Monitor

### 1. App Store Changes (Weekly)

| Signal | Where to Check | Priority |
|--------|----------------|----------|
| Rank changes (+/- 20 positions) | App Store / Sensor Tower | High |
| Rating changes (+/- 0.2) | App Store | Medium |
| Review velocity (spike/drop) | AppFollow / App Store | Medium |
| New version releases | App Store | High |
| Screenshot/description changes | App Store | Medium |
| Pricing changes | App Store / website | Critical |

### 2. Product Changes (Weekly)

| Signal | Where to Check | Priority |
|--------|----------------|----------|
| New feature launches | App release notes | High |
| UI/UX redesigns | Download and test | High |
| Removed features | Release notes / reviews | Medium |
| New subscription tiers | App Store / website | Critical |
| Partnership announcements | PR / social media | Medium |

### 3. Marketing Activity (Weekly)

| Signal | Where to Check | Priority |
|--------|----------------|----------|
| New ad campaigns | Facebook Ad Library | High |
| Influencer partnerships | Social media | Medium |
| PR/media coverage | Google News | Medium |
| Social media activity | Twitter/IG/TikTok | Low |
| Email campaigns | Subscribe to lists | Medium |
| Content marketing | Blogs / YouTube | Low |

### 4. Business Signals (Monthly)

| Signal | Where to Check | Priority |
|--------|----------------|----------|
| Funding announcements | Crunchbase / TechCrunch | High |
| Leadership changes | LinkedIn / PR | Medium |
| Acquisition rumors | Tech news | Medium |
| Layoffs/hiring | LinkedIn / news | Medium |
| Revenue estimates | Sensor Tower / app stores | Medium |

---

## Alert Triggers

### Critical Alerts (Respond within 24 hours)

**Trigger:** Competitor drops price by >30%
**Detection:** Weekly price check
**Response:**
1. Assess if temporary (promo) or permanent
2. If permanent, review our pricing strategy
3. Prepare messaging for users asking about it
4. Consider response promotion if needed

**Trigger:** Competitor launches feature we planned
**Detection:** App update monitoring
**Response:**
1. Review their implementation
2. Identify what they missed
3. Adjust our feature to differentiate
4. Accelerate launch if possible
5. Position as "we did it better"

**Trigger:** Major negative PR for competitor
**Detection:** Google Alerts / news monitoring
**Response:**
1. DO NOT attack directly (tacky)
2. Subtly emphasize our strengths in that area
3. Prepare for potential influx of switching users
4. Consider targeted content addressing concern

**Trigger:** New well-funded competitor enters market
**Detection:** Crunchbase alerts / tech news
**Response:**
1. Analyze their positioning
2. Identify our defensive advantages
3. Consider accelerating key differentiators
4. Monitor their launch strategy

### High Priority Alerts (Respond within 1 week)

**Trigger:** Competitor gains 20+ ranking positions
**Detection:** Weekly tracking
**Response:**
1. Investigate cause (feature? marketing? ASO?)
2. Learn from what's working
3. Adjust our strategy if needed

**Trigger:** Competitor review sentiment shifts significantly
**Detection:** Review monitoring
**Response:**
1. Identify what changed
2. If positive: learn from it
3. If negative: opportunity to capitalize

**Trigger:** Competitor secures major partnership
**Detection:** PR monitoring
**Response:**
1. Assess impact on market
2. Identify alternative partnerships
3. Consider counter-positioning

### Medium Priority Alerts (Review monthly)

- New marketing campaigns
- Minor feature updates
- Social media activity changes
- Content marketing shifts
- Hiring patterns

---

## Monitoring Tools

### Free Tools
| Tool | Purpose | Setup |
|------|---------|-------|
| Google Alerts | PR monitoring | Set up for each competitor name |
| App Store (manual) | Rankings, reviews | Weekly manual check |
| Facebook Ad Library | Ad monitoring | Search competitor names |
| Twitter lists | Social monitoring | Create private list |
| Wayback Machine | Historical changes | Check quarterly |

### Paid Tools (When Budget Allows)
| Tool | Purpose | Cost |
|------|---------|------|
| Sensor Tower | Rankings, downloads, revenue | $$$$ |
| AppFollow | Review monitoring, ASO | $$ |
| SimilarWeb | Traffic analysis | $$$ |
| SpyFu/SEMrush | Keyword tracking | $$ |
| AppTweak | ASO competitor analysis | $$ |

### DIY Solutions
| Tool | Purpose | How |
|------|---------|-----|
| competitor_review_mining.py | Review analysis | Run weekly |
| Spreadsheet tracking | Manual monitoring | Update weekly |
| Screenshot archive | Visual changes | Monthly captures |

---

## Response Playbooks

### Playbook: Price War

**Situation:** Competitor significantly undercuts our price

**Do Not:**
- Panic-match price immediately
- Publicly criticize competitor pricing
- Devalue your own product

**Do:**
1. Verify it's permanent (not promo)
2. Analyze their sustainable price point
3. Emphasize value over price in messaging
4. Consider time-limited competitive offer
5. Focus on features/quality they lack

### Playbook: Feature Copy

**Situation:** Competitor launches feature similar to ours

**Do Not:**
- Accuse of copying (even if true)
- Abandon the feature
- Rush inferior version

**Do:**
1. Note publicly we had it first (subtly)
2. Identify their implementation weaknesses
3. Double down on making ours better
4. Find next differentiating feature
5. Celebrate the validation

### Playbook: Negative PR Opportunity

**Situation:** Competitor faces backlash (privacy, outage, etc.)

**Do Not:**
- Directly attack or mock
- Make comparisons explicitly
- Seem opportunistic

**Do:**
1. Create content about our approach (proactive, not reactive)
2. Emphasize relevant strengths in marketing
3. Be ready for increased trials
4. Let users make the comparison themselves

### Playbook: New Entrant

**Situation:** Well-funded new competitor launches

**Do Not:**
- Assume they'll fail
- Ignore their positioning
- Compete on their strengths

**Do:**
1. Analyze their target segment
2. Identify overlap with our users
3. Reinforce our unique positioning
4. Accelerate community building (moat)
5. Consider partnership vs. competition

### Playbook: Celebrity/Influencer Partnership

**Situation:** Competitor lands major influencer deal

**Do Not:**
- Try to outspend (we can't)
- Dismiss influencer marketing
- Copy their exact approach

**Do:**
1. Focus on micro-influencers (more ROI)
2. Emphasize authentic community
3. User testimonials over celebrity
4. Find underserved influencer niches

---

## Competitive Intelligence Calendar

### Weekly (Every Monday)
- [ ] Check App Store rankings for all competitors
- [ ] Review new app versions released
- [ ] Scan competitor social media highlights
- [ ] Update COMPETITOR_TRACKING.csv
- [ ] Note any alerts triggered

### Monthly (First of Month)
- [ ] Run competitor_review_mining.py
- [ ] Full competitive feature audit
- [ ] Review pricing across all competitors
- [ ] Check for new entrants in space
- [ ] Update keyword rankings
- [ ] Review and respond to any patterns

### Quarterly (Jan/Apr/Jul/Oct)
- [ ] Full competitive strategy review
- [ ] Update all competitor analysis docs
- [ ] Screenshot competitor apps (archive)
- [ ] Review win/loss patterns
- [ ] Adjust positioning if needed
- [ ] Plan next quarter differentiators

---

## Alert Distribution

### Who Gets What

| Alert Type | Notify |
|------------|--------|
| Critical (pricing, major launch) | Founder immediately |
| High (rankings, sentiment) | Weekly summary |
| Medium (marketing, content) | Monthly review |
| Low (social, minor) | Quarterly review |

### Alert Format

```
COMPETITOR ALERT: [PRIORITY]

Competitor: [Name]
Signal: [What happened]
Source: [Where detected]
Date: [When]

Impact Assessment:
[Brief analysis of what this means]

Recommended Response:
[Specific actions to take]

Timeline: [When to respond by]
```

---

## Historical Patterns to Watch

### Seasonal
- January: Fitness apps surge (New Year resolutions)
- Lent/Easter: Faith apps increase
- Back to school: Productivity apps rise
- BFCM: Everyone discounts

### Cyclical
- App Store algorithm changes
- iOS major version releases
- Platform policy updates
- Economic conditions (subscription fatigue)

### Competitor-Specific
- Hallow: Major releases around Catholic calendar
- Strava: Updates before marathon seasons
- Forest: Student-focused timing
