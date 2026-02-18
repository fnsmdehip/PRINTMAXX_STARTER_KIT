# Paid Ads Deep Dive: App Marketing Channels & Strategies

**Last Updated:** 2026-01-25
**Purpose:** Comprehensive guide to paid acquisition for app installs
**Budget Range:** $500/mo (testing) to $10k+/mo (scaling)

---

## Table of Contents

1. [Channel Comparison Matrix](#channel-comparison-matrix)
2. [Meta (Facebook/Instagram)](#meta-facebookinstagram)
3. [Apple Search Ads](#apple-search-ads)
4. [Google App Campaigns](#google-app-campaigns)
5. [TikTok Ads](#tiktok-ads)
6. [Alternative Channels](#alternative-channels)
7. [CPI Benchmarks by Category](#cpi-benchmarks-by-category)
8. [Budget Allocation Strategy](#budget-allocation-strategy)
9. [Creative Templates & Frameworks](#creative-templates--frameworks)
10. [Tracking & Attribution Setup](#tracking--attribution-setup)
11. [Optimization Playbook](#optimization-playbook)
12. [iOS ATT Impact & Mitigation](#ios-att-impact--mitigation)

---

## Channel Comparison Matrix

### Quick Decision Table

| Channel | Min Budget | Typical CPI | Best For | Effort Level |
|---------|-----------|-------------|----------|--------------|
| **Apple Search Ads** | $500/mo | $1-3 | iOS apps, high-intent users | Low |
| **Meta Ads** | $500/mo | $1-4 | Broad reach, retargeting | Medium |
| **Google UAC** | $1,500/mo | $1-5 | Android, cross-platform reach | Low |
| **TikTok Ads** | $500/mo | $1-3 | Gen Z/Millennial, viral potential | High |
| **Reddit Ads** | $200/mo | $2-6 | Niche communities, tech users | Medium |
| **Twitter/X Ads** | $300/mo | $3-8 | Tech, crypto, news audiences | Medium |
| **Snapchat Ads** | $500/mo | $1-4 | Gen Z, AR features | Medium |
| **Unity/ironSource** | $1,000/mo | $0.50-3 | Gaming apps, rewarded installs | Low |

### Channel Selection Framework

```
START HERE
    |
    v
Is your app iOS-only?
    |
    YES --> Start with Apple Search Ads
    |         (highest intent, best attribution)
    |
    NO --> Is budget under $1,000/mo?
              |
              YES --> Apple Search Ads + TikTok Spark Ads
              |
              NO --> Full channel mix (see budget allocation)
```

---

## Meta (Facebook/Instagram)

### Overview

**Strengths:**
- Largest reach (3.7B users across Meta platforms)
- Advanced targeting and lookalike audiences
- Advantage+ AI optimization
- Strong retargeting capabilities

**Weaknesses:**
- iOS ATT significantly impacted attribution
- CPMs increasing year-over-year
- Creative fatigue happens quickly
- Requires constant creative refresh

### Campaign Types for Apps

| Campaign Type | Objective | Best For |
|--------------|-----------|----------|
| **Advantage+ App** | App Installs | Primary acquisition |
| **Manual App** | App Installs | Specific audience testing |
| **Engagement** | App Events | Re-engagement, upsell |
| **Sales** | In-App Purchases | Revenue optimization |

### Advantage+ App Campaigns (Recommended 2026)

Meta's AI-optimized campaigns outperform manual targeting for most use cases now.

**Setup:**
```
Campaign: Advantage+ App Campaign
├── Objective: App Installs OR App Events
├── Budget: $100/day minimum for learning
├── Cost Cap: Target CPI (e.g., $2.00)
├── Locations: Tier 1 (US, CA, UK, AU)
├── Placements: Advantage+ (let AI optimize)
└── Creatives: 10+ variants minimum
```

**Key Settings:**
- Enable Advantage+ placements (AI finds best)
- Set cost cap at target CPI
- Use Advantage+ creative (auto-optimize images/videos)
- Run minimum 7 days before judging

### Manual Campaign Structure

Use when you need specific audience testing:

```
Campaign: [App] - Manual - [Audience] - [Date]
├── Ad Set 1: Interest Stack A
│   ├── Interests: [3-5 related interests]
│   ├── Budget: $25/day
│   └── Ads: 3-5 creatives
├── Ad Set 2: Lookalike (Email/Purchasers)
│   ├── Lookalike: 1-3% of source
│   ├── Budget: $25/day
│   └── Ads: 3-5 creatives
└── Ad Set 3: Retargeting (Website/App)
    ├── Audience: 30-180 day visitors
    ├── Budget: $15/day
    └── Ads: 3-5 creatives
```

### Targeting Options

**Interest Targeting (by niche):**

| Niche | Interest Stack |
|-------|---------------|
| Faith | Christianity, Bible, Prayer, Worship, Church |
| Fitness | Fitness, Running, Walking, Wearables, Wellness |
| Productivity | Productivity, Time Management, Focus, Pomodoro |
| Students | College, University, Study, GPA, SAT/ACT |
| Women's Wellness | Women's health, Self-care, Mindfulness |

**Lookalike Audiences (ranked by quality):**
1. Subscribers/Purchasers (best)
2. Trial starters
3. App installers (7-30 day)
4. Email list
5. Website visitors (engaged)
6. Video viewers (50%+ watched)

### Budget Guidelines

| Phase | Daily Budget | Duration | Goal |
|-------|-------------|----------|------|
| Testing | $50-100/day | 7-14 days | Find winning creative |
| Validation | $100-200/day | 14-30 days | Confirm CPA at scale |
| Scaling | $200-1000/day | Ongoing | Scale winners |

**Minimum viable test:** $700-1,000 total

### Key Metrics

| Metric | Target | Kill If |
|--------|--------|---------|
| CTR (Link) | >1% | <0.5% after 3 days |
| CPC | <$1.00 | >$2.00 |
| CPM | <$15 | >$30 |
| CPI | <$2.00 | >$5.00 after 7 days |
| ROAS | >2x | <1x after 14 days |

---

## Apple Search Ads

### Overview

**Strengths:**
- Highest intent users (actively searching)
- 70% of App Store visits come from search
- 65% of downloads happen after search
- Best attribution (direct iOS integration)
- Typically lowest CPI for quality installs

**Weaknesses:**
- iOS only
- Limited creative control
- Competitive bidding on popular keywords
- No video ads

### Why ASA Should Be Your First Channel

For any iOS app, Apple Search Ads should be your FIRST paid channel:

1. **Intent** - Users actively searching for your category
2. **Attribution** - Perfect tracking (no ATT issues)
3. **Efficiency** - Often $1-3 CPI for good apps
4. **Learning** - Discover what keywords convert

### Campaign Types

| Type | Best For | Budget | Effort |
|------|----------|--------|--------|
| Search Results | Primary conversions | 70% of budget | Medium |
| Search Tab | Discovery/awareness | 20% of budget | Low |
| Today Tab | Brand awareness | High budget only | Low |
| Product Pages | Browse retargeting | 10% of budget | Low |

### Keyword Strategy

**Keyword Categories:**

| Type | Example | CPI | Volume | Priority |
|------|---------|-----|--------|----------|
| Brand | "prayerlock" | $0.50-1 | Low | Defensive |
| Competitor | "opal app" | $2-5 | Medium | Opportunistic |
| Category | "screen time blocker" | $1-3 | High | Primary |
| Long-tail | "christian prayer timer app" | $0.50-2 | Low | Efficient |

**Keyword Research Process:**
1. List 10 seed keywords (your features)
2. Use Apple's built-in suggestions
3. Add competitor brand names
4. Add long-tail variations
5. Group by theme into campaigns

### Campaign Structure

```
Account
├── Campaign: [App] - Brand
│   └── Keywords: brand variations (Exact match)
├── Campaign: [App] - Competitor
│   └── Keywords: competitor names (Broad match)
├── Campaign: [App] - Category
│   └── Keywords: category terms (Broad + Exact)
└── Campaign: [App] - Discovery
    └── Search Match enabled (Apple AI)
```

### Match Types

| Match Type | Behavior | Use For |
|------------|----------|---------|
| Exact | Only that keyword | Brand, proven winners |
| Broad | Variations and related | Discovery, testing |

**Strategy:**
1. Start with Broad match for discovery
2. Mine Search Terms report weekly
3. Move winners to Exact match
4. Negative out irrelevant terms

### Custom Product Pages

Apple allows 35 custom product pages per app. Use them for keyword-specific landing experiences.

**Example:**
- "prayer app" search → Custom Page A (prayer-focused screenshots)
- "screen time blocker" search → Custom Page B (lock screen screenshots)

### Budget Guidelines

| Campaign Type | Daily Budget | CPI Target |
|--------------|--------------|------------|
| Brand | $10-20/day | <$1.00 |
| Competitor | $20-40/day | <$3.00 |
| Category | $30-60/day | <$2.00 |
| Discovery | $20-30/day | <$2.50 |

**Starting budget:** $80-150/day = $2,400-4,500/month

### Key Metrics

| Metric | Target | Action If Off |
|--------|--------|---------------|
| TTR (Tap-Through Rate) | >5% | Improve screenshots/metadata |
| CVR (Conversion Rate) | >30% | Improve app store page |
| CPI | <$2.00 | Lower bids, refine keywords |
| CPA (subscription) | <$10 | Optimize app onboarding |

---

## Google App Campaigns

### Overview

**Strengths:**
- Cross-platform reach (Search, YouTube, Display, Play Store)
- Fully automated optimization
- Great for Android
- Pre-registration campaigns (Android)

**Weaknesses:**
- Requires higher budget ($50+/day minimum)
- Limited control over placements
- Black box optimization
- Slower learning than other channels

### Campaign Types

| Type | Purpose | Min Budget |
|------|---------|-----------|
| App Campaigns for Installs (ACi) | Primary acquisition | $50/day |
| App Campaigns for Engagement (ACe) | Re-engagement | $30/day |
| App Campaigns for Pre-Registration | Android pre-launch | $20/day |

### How Google UAC Works

Google controls everything except:
- Budget
- Target CPI/CPA
- Creative assets
- Geographic targeting
- Device targeting

You provide assets, Google handles:
- Bidding
- Placements
- Audience targeting
- Creative combinations
- Time of day

### Asset Requirements

**Text Assets:**

| Asset | Count | Max Length |
|-------|-------|------------|
| Headlines | 5 required | 30 chars |
| Descriptions | 5 required | 90 chars |

**Image Assets:**

| Size | Use | Min Quantity |
|------|-----|--------------|
| 1200x628 | YouTube, Display | 5 |
| 1200x1200 | Display, Discovery | 5 |
| 300x250 | Display | 3 |
| 320x50 | Banner | 3 |
| 480x320 | App install | 3 |

**Video Assets:**

| Format | Duration | Use |
|--------|----------|-----|
| Portrait (9:16) | 15-30s | YouTube Shorts |
| Landscape (16:9) | 15-30s | YouTube pre-roll |
| Square (1:1) | 15-30s | Feed placements |

### Budget Guidelines

| Phase | Daily Budget | Duration |
|-------|-------------|----------|
| Learning | $50-100/day | 14 days |
| Optimization | $100-200/day | 30 days |
| Scaling | $200-500/day | Ongoing |

**Warning:** Under $50/day may never exit learning phase.

### Target CPI by Category

| Category | Target CPI | Typical Range |
|----------|------------|---------------|
| Health & Fitness | $2.00 | $1-4 |
| Productivity | $1.50 | $0.50-3 |
| Lifestyle | $1.00 | $0.50-2 |
| Education | $2.50 | $1-5 |
| Games | $1.00 | $0.50-2 |
| Finance | $3.00 | $2-6 |

### Key Metrics

| Metric | Target | Kill Campaign If |
|--------|--------|------------------|
| CPI | <$2.00 | >$5.00 after 14 days |
| CVR (install) | >15% | <5% |
| Day 7 retention | >10% | <5% |
| CPA (subscription) | <$20 | >$50 |

---

## TikTok Ads

### Overview

**Strengths:**
- Lowest CPMs in 2026
- Native UGC format performs best
- Gen Z/Millennial reach
- Spark Ads (boost organic)
- TikTok Shop integration

**Weaknesses:**
- Requires TikTok-native creative
- 50 conversions needed to exit learning
- $50/day minimum per ad group
- Attribution challenges

### Campaign Types

| Type | Best For | CPM |
|------|----------|-----|
| Spark Ads | UGC, organic boost | Lowest |
| In-Feed | Custom creatives | Medium |
| TopView | Brand awareness | High ($50k+) |

### Spark Ads (Recommended)

Boost organic creator content. Best performing format.

**How it works:**
1. Creator posts organically
2. You request Spark Ad authorization
3. Boost their content with your budget
4. Engagement stays on original post

**Finding creators:**
1. Search niche hashtags
2. Look for 10K-100K followers (micro-influencers)
3. DM with Spark Ad proposal
4. Offer flat fee + performance bonus

### Creative Requirements

**TikTok Ad Formula:**
```
HOOK (0-1s):
Start mid-action. No intro. Pattern interrupt.
"POV: You finally deleted Instagram"
"This app just saved my marriage"

BODY (1-10s):
Show don't tell. Quick cuts. Native feel.
- Screen recording of app
- Before/after transformation
- Day-in-the-life usage

CTA (10-15s):
Simple, direct.
"Link in bio"
"Try it free"
```

**What works:**
- Native-looking content (not polished)
- Sound on (use trending sounds)
- Text overlays (large, readable)
- Quick cuts (2-3 second scenes max)
- Hook in 0.5 seconds

**What fails:**
- Corporate/polished look
- Slow intros
- Horizontal video
- Generic stock footage

### Budget Guidelines

| Phase | Daily Budget | Duration |
|-------|-------------|----------|
| Testing | $50/day min | 7 days |
| Learning | $100/day | 14 days |
| Scaling | $200-500/day | Ongoing |

**Minimum campaign budget:** $500 (TikTok requirement)

### Key Metrics

| Metric | Target | Kill If |
|--------|--------|---------|
| CTR | >1% | <0.5% |
| CPC | <$0.50 | >$1.00 |
| CPM | <$10 | >$25 |
| CPI | <$2.00 | >$5.00 |
| CVR | >2% | <0.5% |

---

## Alternative Channels

### Reddit Ads

**Best for:** Tech products, niche communities, B2B apps

**Targeting:**
- Subreddit targeting (most valuable)
- Interest targeting
- Lookalike audiences

**Budget:** $200-500/mo minimum

**CPI range:** $2-6

**Tips:**
- Target specific subreddits (not broad interests)
- Native-feeling creative (looks like Reddit post)
- Avoid salesy language
- Test promoted posts vs display
- r/productivity, r/adhd, r/getdisciplined for focus apps
- r/fitness, r/running for fitness apps
- r/Christianity for faith apps

**Creative format:**
- Text-heavy, native look
- Authentic testimonial style
- AMA-style engagement
- Before/after results

### Twitter/X Ads

**Best for:** Tech, crypto, news, finance apps

**Campaign types:**
- App Install campaigns
- Website Traffic (to app store)
- Engagement (build following first)

**Budget:** $300-1,000/mo minimum

**CPI range:** $3-8

**Tips:**
- Target followers of relevant accounts
- Keyword targeting for real-time intent
- Use Video + Cards for best performance
- Conversational ads for engagement

### Snapchat Ads

**Best for:** Gen Z apps, AR features, casual games

**Campaign types:**
- App Install
- App Re-engagement

**Budget:** $500/mo minimum

**CPI range:** $1-4

**Strengths:**
- AR Lens ads (interactive)
- Younger demographic
- Lower competition than TikTok
- Good for games

**Tips:**
- Vertical video only
- First 2 seconds critical
- Sound-off design
- AR Lenses for engagement

### Programmatic (Unity/ironSource)

**Best for:** Gaming apps, rewarded installs, high volume

**Networks:**
- Unity Ads
- ironSource (now Unity)
- AppLovin
- Vungle
- AdColony

**Budget:** $1,000/mo minimum

**CPI range:** $0.50-3

**Ad formats:**
- Rewarded video (best quality)
- Interstitial video
- Playable ads (for games)
- Banner (lowest quality)

**Tips:**
- Rewarded video = highest quality users
- Start with Unity + ironSource
- Optimize by network performance
- Cap frequency per user
- Test playable ads for games

### Influencer Marketing (Not Traditional Paid)

**Platforms:**
- TikTok Creator Marketplace
- Instagram branded content
- YouTube sponsorships
- Micro-influencer networks

**Pricing models:**
- Flat fee ($50-500 for micro, $1k-50k for macro)
- CPI-based ($1-5 per install guaranteed)
- Revenue share
- Free product + affiliate

**Best practices:**
- Micro-influencers (10K-100K) often better ROI
- Authentic integration > scripted read
- Track with unique promo codes
- Test 10+ creators before scaling
- Negotiate performance bonuses

---

## CPI Benchmarks by Category

### Global CPI Averages (2025-2026)

| Category | iOS CPI | Android CPI |
|----------|---------|-------------|
| Games (Casual) | $1.50-3 | $0.50-1.50 |
| Games (Mid-core) | $3-7 | $1.50-4 |
| Games (Hardcore) | $5-15 | $2-8 |
| Health & Fitness | $2-5 | $1-3 |
| Productivity | $1.50-4 | $0.75-2.50 |
| Education | $2-6 | $1-4 |
| Finance | $3-10 | $1.50-5 |
| Shopping | $1-3 | $0.50-2 |
| Social | $2-6 | $1-3 |
| Entertainment | $1.50-4 | $0.75-2.50 |
| Lifestyle | $1-3 | $0.50-2 |
| Dating | $3-10 | $1.50-5 |

### CPI by Geography

| Region | Multiplier vs US |
|--------|-----------------|
| US | 1.0x (baseline) |
| UK | 0.9x |
| Canada | 0.85x |
| Australia | 0.9x |
| Germany | 0.8x |
| France | 0.75x |
| Japan | 1.2x |
| South Korea | 0.9x |
| Brazil | 0.3x |
| India | 0.1x |
| Southeast Asia | 0.2x |

### CPI by Channel

| Channel | Avg CPI | Quality |
|---------|---------|---------|
| Apple Search Ads | $1-3 | Highest |
| Meta (iOS) | $2-5 | High |
| Meta (Android) | $1-3 | High |
| Google UAC | $1-4 | Medium-High |
| TikTok | $1-3 | Medium |
| Snapchat | $1-4 | Medium |
| Unity/ironSource | $0.50-2 | Medium |
| Reddit | $2-6 | Medium |
| Twitter/X | $3-8 | Medium |

---

## Budget Allocation Strategy

### Starting Budget ($500-1,000/month)

Focus on highest-intent channels first.

```
Apple Search Ads: 60% ($300-600)
├── Category keywords: 40%
├── Competitor keywords: 30%
├── Brand protection: 20%
└── Discovery: 10%

TikTok Spark Ads: 30% ($150-300)
└── Boost top 3 organic posts

Testing Reserve: 10% ($50-100)
└── New creative/channel tests
```

### Growth Budget ($1,000-3,000/month)

Add Meta for scale and retargeting.

```
Apple Search Ads: 40% ($400-1,200)
├── Proven keywords scaled
└── Custom product pages

Meta Ads: 35% ($350-1,050)
├── Advantage+ App: 60%
├── Lookalike campaigns: 25%
└── Retargeting: 15%

TikTok Ads: 15% ($150-450)
├── Spark Ads: 70%
└── In-Feed tests: 30%

Testing Reserve: 10% ($100-300)
└── Reddit, Twitter, Snap tests
```

### Scale Budget ($3,000-10,000/month)

Full channel diversification.

```
Apple Search Ads: 30% ($900-3,000)
├── All keyword campaigns
├── Today Tab tests
└── Product Page Browse

Meta Ads: 30% ($900-3,000)
├── Advantage+ scaled
├── Manual campaigns (niche)
└── Re-engagement

Google UAC: 20% ($600-2,000)
├── App Campaigns for Installs
├── YouTube
└── Pre-registration (Android)

TikTok Ads: 10% ($300-1,000)
├── Spark Ads scaled
├── In-Feed winners
└── Creator partnerships

Alternative Channels: 10% ($300-1,000)
├── Reddit (niche targeting)
├── Snapchat (Gen Z)
├── Influencer tests
└── Programmatic
```

### Budget Reallocation Rules

**Weekly review:**
1. Calculate CPI/CPA per channel
2. Reallocate from worst to best performer
3. Max 20% reallocation per week
4. Keep minimum viable budget per channel

**Kill criteria:**
- CPI 2x target for 14+ days
- No conversions after $500 spend
- CTR <0.5% after 7 days
- Creative fatigue (CPI rising 3+ weeks)

---

## Creative Templates & Frameworks

### UGC Video Template (Best Performer)

```
HOOK (0-3s):
"I was wasting 4 hours a day scrolling until I found this..."

OPTIONS:
- "I never thought I'd [outcome] until..."
- "Okay but why did no one tell me about this?"
- "POV: You finally [desired state]"
- "This app just [big claim]"

PROBLEM (3-10s):
"My screen time was out of control. I tried everything.
App limits didn't work. Willpower wasn't enough."

SOLUTION (10-25s):
"Then I found [App]. [Show app in use]
It locks my phone until I [unlock action].
[Show result/streak/progress]
Now I'm averaging 2 hours less screen time per day."

CTA (25-30s):
"Link in bio. Free to download."
OR
"Click below to try it free."
```

### UGC Brief Template

Send this to creators:

```markdown
# UGC Brief: [App Name]

## Hook Options (pick one)
1. "I was struggling with [problem]..."
2. "I never thought I'd [outcome]..."
3. "Okay but why did no one tell me about this?"
4. "This changed everything for me..."
5. "POV: You finally [desired state]"

## Script Structure (30 seconds)
- 0-3s: Hook (must stop scroll)
- 3-10s: Problem/struggle (relatable)
- 10-20s: Discovery + demo (show app)
- 20-27s: Result/transformation (specific numbers)
- 27-30s: CTA (simple, direct)

## Deliverables
- 3 variations (different hooks)
- Raw footage + edited version
- Vertical 9:16 format
- Good lighting, authentic setting (not studio)

## Don'ts
- Don't sound scripted
- Don't use professional lighting
- Don't look like an ad
- Don't mention pricing
- Don't oversell/be too enthusiastic

## Dos
- Be natural, like talking to a friend
- Show real app on your phone
- Include specific numbers/results
- Record in natural environment
- Show your face (builds trust)
```

### Static Image Templates

**Template 1: Problem/Solution**
```
[Top third: Relatable problem visual]
[Middle: App screenshot]
[Bottom: "Download free" CTA]
```

**Template 2: Social Proof**
```
[Star rating: 4.9 stars]
[User count: "500,000+ users"]
[Screenshot of app]
[Quote: "Finally an app that works"]
```

**Template 3: Before/After**
```
[Left side: Screen time 6+ hours]
[Right side: Screen time 2 hours]
[Arrow or divide between]
[CTA at bottom]
```

**Template 4: Feature Callout**
```
[App screenshot]
[3 feature callouts with icons]
[Download CTA]
```

### Hook Testing Framework

Test 5+ hooks for every creative concept:

| Hook Type | Example | Best For |
|-----------|---------|----------|
| Question | "Why is everyone deleting Instagram?" | Curiosity |
| POV | "POV: You finally have time for hobbies" | Aspiration |
| Shock | "This app made my husband talk to me again" | Attention |
| Social Proof | "2M people have quit scrolling with this" | Trust |
| Result | "I got 3 hours of my life back daily" | Outcome |
| Challenge | "You can't last a week with this app" | Engagement |
| Confession | "I was addicted to my phone. Here's what helped." | Relatability |

---

## Tracking & Attribution Setup

### Required Tracking Stack

| Tool | Purpose | Priority |
|------|---------|----------|
| Meta Pixel | Facebook/Instagram attribution | Required |
| TikTok Pixel | TikTok attribution | Required |
| Google Firebase | Google UAC, analytics | Required |
| AppsFlyer/Adjust | Multi-touch attribution | Recommended |
| RevenueCat | Subscription attribution | Required |

### Meta Pixel Installation (Next.js)

```javascript
// app/layout.tsx
import Script from 'next/script'

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <Script id="fb-pixel" strategy="afterInteractive">
          {`
            !function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');
            fbq('init', 'YOUR_PIXEL_ID');
            fbq('track', 'PageView');
          `}
        </Script>
      </head>
      <body>{children}</body>
    </html>
  )
}
```

### TikTok Pixel Installation

```javascript
// app/layout.tsx
<Script id="tiktok-pixel" strategy="afterInteractive">
  {`
    !function (w, d, t) {
      w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];
      ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie"];
      ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};
      for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);
      ttq.instance=function(t){for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e};
      ttq.load=function(e,n){var i="https://analytics.tiktok.com/i18n/pixel/events.js";
      ttq._i=ttq._i||{},ttq._i[e]=[],ttq._i[e]._u=i,ttq._t=ttq._t||{},ttq._t[e]=+new Date,ttq._o=ttq._o||{},ttq._o[e]=n||{};
      var o=document.createElement("script");o.type="text/javascript",o.async=!0,o.src=i+"?sdkid="+e+"&lib="+t;
      var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(o,a)};
      ttq.load('YOUR_PIXEL_ID');
      ttq.page();
    }(window, document, 'ttq');
  `}
</Script>
```

### Conversion Events to Track

| Event | When to Fire | Priority |
|-------|--------------|----------|
| PageView | Page load | Required |
| ViewContent | Key page viewed | Required |
| Lead | Form submission | Required |
| AddToCart | Clicked pricing | Recommended |
| InitiateCheckout | Started checkout | Required |
| Purchase | Completed purchase | Required |
| Subscribe | Started subscription | Required |

### Apple Search Ads Attribution (iOS)

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

### UTM Parameter Strategy

Use consistent UTM parameters across all campaigns:

```
?utm_source=[platform]
&utm_medium=[campaign_type]
&utm_campaign=[campaign_name]
&utm_content=[ad_name]
&utm_term=[keyword_or_audience]
```

**Examples:**
```
?utm_source=facebook&utm_medium=cpc&utm_campaign=prayerlock_app_install&utm_content=ugc_testimonial_v1
?utm_source=apple&utm_medium=asa&utm_campaign=category_keywords&utm_term=prayer_app
?utm_source=tiktok&utm_medium=spark&utm_campaign=creator_boost&utm_content=sarah_testimonial
```

### RevenueCat Integration

RevenueCat automatically captures attribution from:
- Apple Search Ads
- Facebook Ads (via SKAdNetwork)
- Google Ads (via Firebase)

**Enable in RevenueCat dashboard:**
1. Go to Project Settings > Integrations
2. Enable Apple Search Ads Attribution
3. Enable Google Attribution
4. View in Analytics > Attribution

---

## Optimization Playbook

### Daily Checklist (First 14 Days)

- [ ] Check spend vs budget (all channels)
- [ ] Review CPI/CPA by campaign
- [ ] Check frequency (Meta: keep under 3)
- [ ] Note top performing creative
- [ ] Kill any ads with 0 conversions after $100 spend

### Weekly Optimization

**Week 1-2: Creative Testing**

1. Launch 5-10 creative variants
2. Run each with equal budget
3. After $50-100 per creative:
   - Kill: CTR <0.5%, CPI 2x target
   - Scale: Top 2-3 performers
4. Create 2-3 variations of winners

**Week 3-4: Audience/Channel Testing**

1. Take winning creatives
2. Test across:
   - Different audiences (Meta)
   - Different keywords (ASA)
   - Different ad groups (TikTok)
3. Identify best audience x creative combos
4. Reallocate budget to winners

**Monthly Optimization**

1. **Creative refresh** - All creatives fatigue. Add 3-5 new variants monthly.
2. **Audience expansion** - Test new lookalike sources, interest stacks
3. **Channel rebalancing** - Shift budget based on CPA trends
4. **Landing page tests** - A/B test app store page, custom product pages
5. **LTV analysis** - Calculate true ROAS including all costs

### Scaling Rules

**When to scale:**
- CPI consistently under target for 7+ days
- 50+ conversions (statistical significance)
- Frequency <2 (Meta)
- Creative not showing fatigue

**How to scale:**
1. Increase budget 20% every 2-3 days
2. Never increase more than 50% at once
3. Monitor CPI closely during scale
4. Have backup creatives ready

**When to pause/kill:**
- CPI 2x target for 7+ days
- No conversions after $500 spend
- Frequency >5 (Meta)
- CPI rising for 3+ consecutive weeks

### Optimization Decision Tree

```
CPI over target?
├── YES → Check creative performance
│   ├── All creatives failing → Test new creative concepts
│   └── Some winning → Kill losers, scale winners
│
└── NO → Check scale opportunity
    ├── Frequency <2, stable CPI → Scale 20%
    └── Frequency >3 or rising CPI → Expand to new audience
```

### A/B Testing Framework

**What to test (priority order):**

1. **Hook** (highest impact)
   - Test 5 hooks, same body
   - Winner by CTR

2. **Creative format**
   - UGC vs polished
   - Video vs static
   - Winner by CPI

3. **Audience**
   - Interest vs lookalike
   - Different lookalike sources
   - Winner by CPA

4. **Landing page**
   - Custom product pages (ASA)
   - Different app store screenshots
   - Winner by CVR

5. **Offer**
   - Free trial vs discount
   - Annual vs monthly first
   - Winner by LTV

---

## iOS ATT Impact & Mitigation

### What Changed

iOS 14.5+ App Tracking Transparency (ATT) requires user opt-in for tracking.

**Impact:**
- 20-40% of iOS users opt in
- Attribution windows shortened
- Lookalike audience quality decreased
- CPIs increased 20-50% initially

### Mitigation Strategies

**1. Embrace SKAdNetwork (SKAN)**
- Apple's privacy-preserving attribution
- Works for install attribution
- Limited conversion value data
- 24-48 hour delay

**2. Prioritize Apple Search Ads**
- Unaffected by ATT (first-party data)
- Perfect attribution
- Often most efficient iOS channel now

**3. Use Probabilistic Modeling**
- MMPs (Adjust, AppsFlyer) offer modeled attribution
- Not 100% accurate but directionally useful
- Better than flying blind

**4. Focus on Android**
- Android not affected
- Lower CPIs, better attribution
- Consider Android-first strategy

**5. Server-Side Events**
- Conversions API (Meta)
- Events API (TikTok)
- Better match rates than client-side

**6. Creative-Based Optimization**
- Focus on creative testing (not audience)
- Use Advantage+ campaigns (AI optimization)
- Broad targeting often outperforms now

**7. First-Party Data**
- Build email lists
- In-app surveys for acquisition source
- Incentivize email collection

### Post-ATT Channel Priority

| Channel | ATT Impact | Recommendation |
|---------|------------|----------------|
| Apple Search Ads | None | Increase spend |
| Meta (Advantage+) | High | Use broad, trust AI |
| Meta (Manual) | Very High | Test vs Advantage+ |
| Google UAC | Medium | Good alternative |
| TikTok | Medium | Spark Ads help |
| Programmatic | Low | Consider increase |

---

## Quick Reference: Platform Links

| Platform | Ads Manager | Help/Docs |
|----------|-------------|-----------|
| Meta | business.facebook.com | facebook.com/business/help |
| Apple Search Ads | searchads.apple.com | searchads.apple.com/help |
| Google Ads | ads.google.com | support.google.com/google-ads |
| TikTok | ads.tiktok.com | ads.tiktok.com/help |
| Reddit | ads.reddit.com | advertising.reddithelp.com |
| Snapchat | ads.snapchat.com | businesshelp.snapchat.com |
| Twitter/X | ads.twitter.com | business.twitter.com/help |

## Research Tools

| Tool | Purpose | URL |
|------|---------|-----|
| FB Ads Library | Competitor ad research | facebook.com/ads/library |
| TikTok Creative Center | TikTok ad inspiration | ads.tiktok.com/business/creativecenter |
| Foreplay | Ad swipe file | foreplay.co |
| AdSpy | Competitive intelligence | adspy.com |
| Sensor Tower | App intelligence | sensortower.com |
| AppTweak | ASO + ASA research | apptweak.com |

---

## Files in This Folder

```
MONEY_METHODS/PAID_ADS/
├── PAID_ADS_DEEP_DIVE.md (this file)
├── PAID_ADS_PLAYBOOK.md (original quick start)
├── META_ADS_PLAYBOOK.md (Meta deep dive)
├── APPLE_SEARCH_ADS_PLAYBOOK.md (ASA deep dive)
├── GOOGLE_APP_CAMPAIGNS_PLAYBOOK.md (Google deep dive)
├── TIKTOK_ADS_PLAYBOOK.md (TikTok deep dive)
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

---

Last updated: 2026-01-25
