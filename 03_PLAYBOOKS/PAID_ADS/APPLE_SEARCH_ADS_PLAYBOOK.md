# Apple Search Ads Playbook

**Last Updated:** 2026-01-23
**Status:** Ready for implementation at app launch

---

## Quick Start Checklist

- [ ] App live on App Store
- [ ] Apple Search Ads account created
- [ ] Payment method added
- [ ] Keywords researched
- [ ] First campaign launched

---

## Why Apple Search Ads First

**For apps, Apple Search Ads should be your FIRST paid channel:**

1. **Highest intent** - Users actively searching
2. **70% of App Store visits** - Come from search
3. **65% of downloads** - Happen right after search
4. **Best attribution** - Direct conversion tracking
5. **Lower CPI** - Typically $1-3 for good apps

---

## Account Setup

### 1. Create Account

```
1. Go to searchads.apple.com
2. Sign in with Apple Developer account
3. Accept terms
4. Add payment method
5. Set daily budget cap
```

### 2. Campaign Types

| Type | Best For | Effort |
|------|----------|--------|
| Search Results | Primary conversions | Medium |
| Search Tab | Discovery/awareness | Low |
| Today Tab | Brand awareness | High budget |
| Product Pages | Retargeting | Low |

**Start with:** Search Results only

---

## Keyword Strategy

### Keyword Types

| Type | Example | CPI | Volume |
|------|---------|-----|--------|
| Brand | "prayerlock" | Low | Low |
| Competitor | "opal app" | High | Medium |
| Category | "screen time blocker" | Medium | High |
| Long-tail | "christian prayer timer app" | Low | Low |

### Keyword Research

**Tools:**
- Apple Search Ads (built-in suggestions)
- AppTweak
- Sensor Tower
- Mobile Action

**Process:**
1. List 10 seed keywords
2. Get Apple's suggestions
3. Add competitor names
4. Add long-tail variations
5. Group by theme

### Keywords by App

**PrayerLock:**
```
Brand: prayerlock, prayer lock
Competitor: opal, one sec, screenzen
Category: prayer app, christian app, bible daily, morning devotional
Feature: screen time prayer, phone lock prayer, christian phone blocker
Long-tail: lock phone until pray, morning prayer reminder app
```

**WalkToUnlock:**
```
Brand: walktounlock, walk to unlock
Competitor: opal, stepbet, sweatcoin
Category: walking app, step counter, fitness tracker
Feature: phone lock walking, exercise phone lock
Long-tail: make yourself walk to use phone, gamified walking app
```

**StudyLock:**
```
Brand: studylock, study lock
Competitor: forest app, flora, opal
Category: study app, focus timer, pomodoro app
Feature: lock phone study, distraction blocker students
Long-tail: lock phone until homework done, study focus app college
```

---

## Campaign Structure

### Recommended Structure

```
Account
├── Campaign: [App] - Brand
│   └── Ad Group: Brand terms
│       └── Keywords: brand variations
├── Campaign: [App] - Competitor
│   └── Ad Group: Competitor names
│       └── Keywords: competitor apps
├── Campaign: [App] - Category
│   └── Ad Group: Category terms
│       └── Keywords: generic category
└── Campaign: [App] - Discovery
    └── Ad Group: Search Match
        └── Auto keywords (Apple AI)
```

### Match Types

| Match Type | Behavior | Use For |
|------------|----------|---------|
| Exact | Only that keyword | Brand, proven keywords |
| Broad | Variations and related | Discovery, new keywords |

**Strategy:**
1. Start with Broad match for discovery
2. Add Exact match for winners
3. Negative out irrelevant terms

---

## Budget Guidelines

### Starting Budget

| Campaign Type | Daily Budget | CPI Target |
|--------------|--------------|------------|
| Brand | $10/day | <$1.00 |
| Competitor | $20/day | <$3.00 |
| Category | $30/day | <$2.00 |
| Discovery | $20/day | <$2.50 |

**Total starting:** $80/day = $2,400/month

### Scaling

Once you find keywords with CPI under target:
1. Increase bid by 10-20%
2. Increase daily budget
3. Add to Exact match campaign
4. Create Custom Product Page

---

## Custom Product Pages

Apple allows 35 custom product pages per app. Use them.

### How to Create

1. App Store Connect > App > Product Page Optimization
2. Create new Custom Product Page
3. Customize screenshots/preview for keyword theme
4. Link to specific ad group

### Examples

**"prayer app" search → Custom Page A:**
- Screenshots showing prayer features
- App preview focused on morning devotional
- Subtitle emphasizing faith focus

**"screen time blocker" search → Custom Page B:**
- Screenshots showing lock screen
- App preview showing phone blocked
- Subtitle emphasizing digital wellness

---

## Optimization

### Daily Tasks

- [ ] Check spend vs budget
- [ ] Review CPI by keyword
- [ ] Add negative keywords for wasted spend
- [ ] Note any search terms with high volume

### Weekly Tasks

- [ ] Move winners from Broad to Exact
- [ ] Increase bids on profitable keywords
- [ ] Pause keywords with CPI 2x target
- [ ] Review Search Terms report

### Monthly Tasks

- [ ] Refresh custom product pages
- [ ] Add new keyword themes
- [ ] Analyze conversion to subscription
- [ ] Calculate true CAC vs LTV

---

## Key Metrics

| Metric | Target | Action If Off |
|--------|--------|---------------|
| TTR (Tap-Through Rate) | >5% | Improve screenshots/metadata |
| CVR (Conversion Rate) | >30% | Improve app store page |
| CPI | <$2.00 | Lower bids, improve targeting |
| CPA (subscription) | <$10 | Optimize onboarding |

### Conversion Funnel

```
Impressions → Taps → Downloads → Opens → Trials → Subscriptions
   100%       5%      30%        80%      20%       5%
```

---

## Search Match (Discovery)

Apple's AI finds keywords for you.

### Setup

1. Create Discovery campaign
2. Enable Search Match
3. Set conservative bids ($0.50-1.00)
4. Run for 2-4 weeks
5. Harvest winning keywords

### Mining Process

Weekly:
1. Go to Search Terms report
2. Filter by conversions
3. Export high-performing terms
4. Add to Exact match campaign
5. Negative out in Discovery

---

## Competitor Targeting

### Legal/Allowed

- Bidding on competitor brand names
- Showing ads when users search competitors
- Comparing features in screenshots (carefully)

### Strategy

1. List top 10 competitors
2. Create dedicated campaign
3. Higher bids (expect $3-5 CPI)
4. Custom product page highlighting differences
5. Track separately from other campaigns

### PrayerLock Competitors

```
opal app, one sec app, screenzen,
clearspace, flipd, forest app,
freedom app, offtime, space app
```

---

## Attribution & Tracking

### Apple Search Ads Attribution API

```swift
// iOS App - Check attribution on first launch
import AdServices

func checkAttribution() async {
    do {
        let token = try AAAttribution.attributionToken()
        // Send to your backend
        await sendToBackend(token: token)
    } catch {
        print("Attribution not available")
    }
}
```

### RevenueCat Integration

RevenueCat automatically captures Apple Search Ads attribution:
1. Enable in RevenueCat dashboard
2. View in Analytics > Attribution
3. See CPA by keyword/campaign

---

## Budget Allocation

### Phase 1: Launch ($1000/month)

- 30% Brand protection
- 40% Category keywords
- 20% Discovery (Search Match)
- 10% Competitor (conservative)

### Phase 2: Growth ($3000/month)

- 20% Brand
- 40% Proven category keywords
- 20% Competitor expansion
- 20% New keyword tests

---

## Common Mistakes

1. **No brand campaign** - Competitors will bid on your name
2. **Broad match only** - Wastes budget on irrelevant terms
3. **Ignoring Search Terms** - Missing optimization opportunities
4. **Same CPP for all** - Custom pages boost CVR
5. **Not tracking to subscription** - CPI doesn't matter, CPA does

---

## Advanced: Search Ads Advanced vs Basic

### Basic (Easy, Limited)

- Pay per install
- Apple sets bids
- Limited reporting
- Good for beginners

### Advanced (Recommended)

- Full control over bids
- Keyword-level reporting
- Custom product pages
- Search Terms mining
- Better for optimization

**Recommendation:** Start with Basic for 2 weeks, then switch to Advanced.

---

## Resources

- Apple Search Ads: searchads.apple.com
- Best Practices: searchads.apple.com/best-practices
- API Documentation: developer.apple.com/documentation/apple_search_ads
