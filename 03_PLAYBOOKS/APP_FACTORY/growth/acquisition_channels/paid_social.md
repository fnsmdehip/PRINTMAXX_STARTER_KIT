# Paid social: ad strategy for mobile apps

Paid social is fuel. It works when your product-market fit is proven. It fails when you're trying to buy your way to product-market fit.

---

## Prerequisites before spending

Before you spend $1 on ads:

1. **Organic traction** - People use and retain without ads
2. **Clear unit economics** - LTV > CAC target
3. **Tracking setup** - Attribution working correctly
4. **Creative assets** - Video and static ads ready
5. **Landing experience** - App Store optimized

If retention is bad, ads just accelerate failure.

---

## Platform selection

### Platform comparison

| Platform | CPM | Best Audience | Creative Type | Minimum Budget |
|----------|-----|---------------|---------------|----------------|
| Meta (FB/IG) | $5-15 | 25-55, broad | Video, UGC | $50/day |
| TikTok | $3-10 | 18-35, discovery | Video, native | $50/day |
| Google UAC | $2-8 | High intent | Mixed, auto | $30/day |
| Apple Search | $1-5 | Highest intent | Text + screenshots | $25/day |
| Snapchat | $2-8 | 13-24 | Video, AR | $50/day |

### Start with

**Limited budget ($500-2000/month):**
1. Apple Search Ads (highest intent)
2. Meta with narrow targeting

**Moderate budget ($2000-10000/month):**
1. Meta as primary
2. TikTok for younger audiences
3. Google UAC for broad reach

**Scale budget ($10000+/month):**
All platforms, optimized by CPA

---

## Campaign structure

### Meta (Facebook/Instagram)

```
Campaign Level: App Installs objective
  └── Ad Set 1: Lookalike - Purchasers
        └── Ad 1: UGC video
        └── Ad 2: Demo video
        └── Ad 3: Static carousel
  └── Ad Set 2: Lookalike - Day 7 retained
        └── (same ads, different audience)
  └── Ad Set 3: Interest targeting
        └── (same ads, different audience)
```

**Settings:**
- Optimization: App installs (start), then App events (purchase/trial)
- Attribution: 7-day click, 1-day view
- Placement: Automatic (let Meta optimize)

### TikTok

```
Campaign: App Installs
  └── Ad Group 1: Broad targeting
        └── Spark Ad 1: Native UGC
        └── Spark Ad 2: Influencer content
        └── Standard Ad: Product demo
  └── Ad Group 2: Interest targeting
        └── (same ads)
```

**Settings:**
- Optimization: Install (start), then Purchase/Trial
- Bidding: Lowest cost (start), then Cost cap
- Creative: Spark Ads perform best

### Google UAC

```
Campaign: App - Install volume
  Assets:
    - 5 headlines
    - 5 descriptions
    - 5 videos (YouTube, landscape, portrait)
    - 5 images
    - HTML5 playable (if applicable)
```

**Settings:**
- Target CPI: Start at 2x organic CPI, optimize down
- Location: Start specific, expand
- Let Google's AI optimize placements

### Apple Search Ads

```
Campaign: Brand
  └── Ad Group: Brand terms
        └── Keyword: [your app name]
        └── Keyword: [common misspellings]

Campaign: Category
  └── Ad Group: Category terms
        └── Keyword: "meditation app"
        └── Keyword: "daily meditation"

Campaign: Competitor
  └── Ad Group: Competitor names
        └── Keyword: [competitor 1 name]
        └── Keyword: [competitor 2 name]
```

**Settings:**
- Match type: Exact for control, Broad for discovery
- CPA goal: Set based on LTV
- Search Match: Separate campaign for discovery

---

## Creative strategy

### Ad types that work for apps

| Type | Description | When to Use |
|------|-------------|-------------|
| UGC | Real user testimonial | Social proof, trust |
| Demo | Screen recording + voiceover | Feature explanation |
| Problem-solution | Pain point + app solving it | Awareness |
| Before/after | Transformation story | Results-focused apps |
| Tutorial | "How to do X with app" | Education |
| Founder story | Personal connection | Smaller apps |

### Creative framework

**Hook (0-3 seconds):**
Stop the scroll. Options:
- Bold statement: "I deleted all my other fitness apps"
- Question: "Why do 90% of habits fail?"
- Shocking stat: "I saved 2 hours a day with one app"
- Visual hook: Transformation, unusual visual

**Body (3-15 seconds):**
- Show the app solving the problem
- 2-3 key features max
- Real app footage, not mockups

**CTA (last 2-3 seconds):**
- Clear instruction: "Download free"
- Urgency if real: "7-day trial ends Friday"
- Benefit reminder: "Start sleeping better tonight"

### Creative testing

**Structure:**
- 3-5 ad concepts per ad set
- Test hooks first (biggest impact)
- Winner gets variations
- Refresh every 2-4 weeks

**Testing priorities:**
1. Hook (first 3 seconds)
2. Message angle (pain vs benefit)
3. Format (UGC vs demo)
4. Length (15s vs 30s vs 60s)
5. CTA

---

## Audience targeting

### Meta audiences

**Lookalike audiences (best):**
1. Purchasers/subscribers (1-3%)
2. Day 7 retained users (1-3%)
3. Activated users (3-5%)
4. Website visitors (5-10%)

**Interest audiences:**
Combine 2-3 related interests:
- App category (fitness, meditation)
- Behavior (active lifestyle, wellness)
- Related apps (competitor users)

**Broad targeting:**
Let Meta's AI find users. Works at scale.

### TikTok audiences

**Lookalike:**
Same as Meta, but 1% works best

**Interest:**
- Category interests
- Video interaction categories
- Creator audiences

### Exclusions

Always exclude:
- Existing users (device IDs)
- Past purchasers
- Website visitors who installed

---

## Bidding and budget

### Bidding strategies

| Strategy | When to Use | Risk |
|----------|-------------|------|
| Lowest cost | Learning phase | Can overspend |
| Cost cap | Efficiency target | Volume limited |
| Bid cap | Strict CPA target | Volume very limited |

### Budget allocation

**Phase 1: Learning ($500-1000)**
- Test 3-5 audiences
- 3-5 creatives per audience
- $20-50/day per ad set
- Goal: Find winning combinations

**Phase 2: Validation ($1000-3000)**
- Scale winning ad sets
- Kill losers (CPA > 2x target)
- $50-100/day per winner
- Goal: Confirm CPA at scale

**Phase 3: Scale ($3000+)**
- Increase budget 20% every 3 days
- Expand audiences (higher % lookalikes)
- Add platforms
- Goal: Volume at target CPA

### Budget pacing

- Never increase more than 20% at once
- Let ad sets exit learning phase (50 conversions)
- Weekend performance often differs from weekday

---

## Attribution and tracking

### Setup checklist

- [ ] Meta Pixel + SDK installed
- [ ] TikTok Pixel + SDK installed
- [ ] Google Firebase linked
- [ ] Apple Search Ads attribution
- [ ] MMP installed (AppsFlyer, Adjust, Branch)
- [ ] Server-side events if applicable

### Key events to track

| Event | Description | Use For |
|-------|-------------|---------|
| Install | App downloaded | CPI optimization |
| Activation | First value action | Quality signal |
| Trial start | Started free trial | Subscription apps |
| Purchase | First payment | ROAS optimization |
| Day 7 retention | Active after 7 days | LTV prediction |

### Attribution windows

- **Standard:** 7-day click, 1-day view
- **iOS 14.5+:** Use SKAdNetwork, expect delays
- **Compare:** Platform reported vs MMP vs backend

---

## Optimization workflow

### Daily (5 min)

- Check spend vs budget
- Flag any anomalies
- Pause clear losers (3x CPA, enough spend)

### Weekly (30 min)

- Review CPA by ad set and creative
- Pause underperformers
- Scale winners (20% budget increase)
- Review creative fatigue (CTR declining)
- Launch new tests

### Monthly (2 hours)

- Full channel review
- LTV by source analysis
- Creative audit and refresh
- Budget reallocation
- New platform testing

### Optimization rules

**Kill if:**
- CPA > 2x target after $100 spend
- CTR < 0.5% after 10K impressions
- No installs after $50 spend

**Scale if:**
- CPA < target for 3 consecutive days
- CTR > 1.5%
- Consistent volume

---

## Platform-specific tactics

### Meta

1. Use Advantage+ campaigns for broad reach
2. Dynamic creative optimization for variations
3. Test Reels placement specifically
4. Catalog ads for multiple app features
5. Run engagement campaigns to build social proof

### TikTok

1. Spark Ads always (use organic content as ads)
2. Work with creators for authentic content
3. Follow trends with your spin
4. Test Interactive Add-ons
5. Use TikTok Creative Center for research

### Apple Search Ads

1. Bid aggressively on brand terms
2. Use Search Match for keyword discovery
3. Custom product pages per ad group
4. Negative keywords to reduce waste
5. Daypart bidding if patterns emerge

---

## Budget allocation by stage

### Pre-PMF ($500/month)

Don't run ads yet. Focus on organic.

### Early traction ($500-2000/month)

| Channel | Allocation | Goal |
|---------|------------|------|
| Apple Search Ads | 60% | High-intent installs |
| Meta | 40% | Test audiences |

### Growth ($2000-10000/month)

| Channel | Allocation | Goal |
|---------|------------|------|
| Meta | 50% | Scale |
| Apple Search Ads | 25% | Maintain |
| TikTok/Google | 25% | Test |

### Scale ($10000+/month)

Optimize by CPA, not channel. Allocate to what works.

---

## Common mistakes

1. **Spending before PMF** - Ads amplify, not create, demand
2. **No creative testing** - Same ad until it dies
3. **Wrong optimization event** - Optimizing installs, not revenue
4. **Ignoring iOS attribution** - SKAdNetwork requires patience
5. **Scaling too fast** - Kills learning, spikes CPA
6. **No exclusions** - Paying to reach existing users
7. **Chasing vanity metrics** - CTR without CPA focus

---

## Implementation checklist

### Setup (Week 1)

- [ ] Install all pixels and SDKs
- [ ] Set up MMP if needed
- [ ] Create conversion events
- [ ] Build initial audiences
- [ ] Produce 5+ creative assets

### Launch (Week 2)

- [ ] Start with lowest risk (Apple Search Ads)
- [ ] Launch Meta tests ($20/day per ad set)
- [ ] Set up daily monitoring
- [ ] Define success metrics

### Optimize (Week 3+)

- [ ] Review performance weekly
- [ ] Kill losers, scale winners
- [ ] Refresh creative bi-weekly
- [ ] Expand to new platforms as budget allows
