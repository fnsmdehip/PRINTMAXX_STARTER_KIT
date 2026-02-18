# Meta Ads Playbook (Facebook + Instagram)

**Last Updated:** 2026-01-23
**Status:** Ready for implementation post-revenue

---

## Quick Start Checklist

- [ ] Business Manager account created
- [ ] Ad account added
- [ ] Pixel installed on landing page
- [ ] Payment method added
- [ ] First campaign drafted

---

## When to Use Meta Ads

**Start Meta Ads when:**
- Organic growth plateaus at ~$10k MRR
- Have at least 3 proven ad creatives
- $500+ monthly ad budget available
- Clear CPA target defined

**Don't start if:**
- No organic traction yet (ads won't fix bad product)
- Budget under $300/month (not enough for testing)
- No landing page optimized for conversions

---

## Account Setup

### 1. Business Manager

```
1. Go to business.facebook.com
2. Create Business Manager
3. Add ad account
4. Add payment method
5. Verify domain
6. Install pixel
```

### 2. Pixel Installation

**For Next.js (PRINTMAXX site):**

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

### 3. Conversion Events

Track these events:
- `Lead` - Form submission
- `AddToCart` - Clicked pricing
- `InitiateCheckout` - Started checkout
- `Purchase` - Completed purchase
- `ViewContent` - Viewed key pages

---

## Campaign Structure

### Advantage+ Campaigns (Recommended 2026)

Meta's AI-optimized campaigns outperform manual targeting for most use cases.

```
Campaign: Advantage+ App Campaigns
├── Budget: $100/day minimum
├── Objective: App Installs OR Conversions
├── Cost Cap: Target CPI (e.g., $2.00)
└── Creatives: 10+ variants (AI optimizes)
```

### Manual Campaign Structure

```
Campaign: [Niche] - [Objective] - [Date]
├── Ad Set 1: Broad Interests
│   ├── Ad 1: UGC Video
│   ├── Ad 2: Static Image
│   └── Ad 3: Carousel
├── Ad Set 2: Lookalike (Email List)
│   ├── Ad 1: UGC Video
│   ├── Ad 2: Static Image
│   └── Ad 3: Carousel
└── Ad Set 3: Retargeting
    ├── Ad 1: Testimonial Video
    ├── Ad 2: Feature Breakdown
    └── Ad 3: Urgency CTA
```

---

## Budget Guidelines

| Phase | Daily Budget | Duration | Goal |
|-------|-------------|----------|------|
| Testing | $20-50/day | 7-14 days | Find winning creative |
| Validation | $50-100/day | 14-30 days | Confirm CPA |
| Scaling | $100-500/day | Ongoing | Scale winners |

**Minimum viable test:** $500 total ($20/day x 25 days)

---

## Creative Guidelines

### Video Ads (Best performing)

**Structure:**
- 0-3s: Hook (pattern interrupt or bold claim)
- 3-10s: Problem statement
- 10-25s: Solution/product demo
- 25-30s: CTA

**Specs:**
- 9:16 for Stories/Reels
- 1:1 for Feed
- Under 30 seconds
- Captions required (85% watch muted)

### UGC Video Formula

```
HOOK (0-3s):
"I was wasting 4 hours a day scrolling until I found this..."

PROBLEM (3-10s):
"My screen time was out of control. I tried everything."

SOLUTION (10-25s):
"Then I found [App]. It locks my phone until I [unlock action].
Now I'm averaging 2 hours less screen time per day."

CTA (25-30s):
"Link in bio. Free to download."
```

### Static Image Specs

- 1080x1080 (Feed)
- 1080x1920 (Stories)
- High contrast
- One clear message
- Face if possible (3x engagement)

---

## Targeting by Niche

### Faith Niche (PrayerLock)

**Interests:**
- Christianity, Bible, Prayer
- Christian music, Worship
- Church, Ministry
- Specific denominations (Catholic, Baptist, etc.)

**Lookalikes:**
- Email list (prioritize)
- App installers
- Website visitors (90 days)

### Fitness Niche (WalkToUnlock)

**Interests:**
- Fitness, Health
- Walking, Running, Hiking
- Fitbit, Apple Watch
- Weight loss, Healthy lifestyle

### Student Niche (StudyLock)

**Interests:**
- College students, University
- Study, Homework, GPA
- SAT, ACT, GMAT
- Specific schools/programs

---

## Optimization Checklist

### Daily (first 7 days)

- [ ] Check spend vs budget
- [ ] Review CPA by ad set
- [ ] Check frequency (keep under 3)
- [ ] Note top performing creative

### Weekly

- [ ] Kill ad sets with CPA 2x target
- [ ] Duplicate winning ad sets
- [ ] Add new creative variants
- [ ] Update exclusions

### Monthly

- [ ] Refresh all creatives
- [ ] Update lookalike audiences
- [ ] Review attribution window
- [ ] Calculate true ROAS

---

## Key Metrics

| Metric | Target | Kill If |
|--------|--------|---------|
| CTR (Link) | >1% | <0.5% after 3 days |
| CPC | <$1.00 | >$2.00 |
| CPM | <$15 | >$30 |
| CPA | Varies | 2x target |
| ROAS | >2x | <1x after 14 days |

---

## Common Mistakes

1. **Testing too few creatives** - Need 5-10 minimum
2. **Killing too early** - Wait for 50 conversions before decisions
3. **Ignoring frequency** - >3 means audience fatigue
4. **No retargeting** - Always run retarget campaigns
5. **Wrong objective** - Use conversions, not traffic

---

## FB Ads Library Research

Use FB Ads Library to find winning ads:

```
1. Go to facebook.com/ads/library
2. Search: "app" "download" [niche keywords]
3. Filter: Active ads, All dates
4. Sort by: Running longest (proven winners)
5. Save: Screenshots of hooks, CTAs, visuals
```

**Search terms for our niches:**
- "prayer app" "Christian app" "Bible daily"
- "screen time" "phone addiction" "digital detox"
- "study app" "focus timer" "pomodoro"
- "fitness tracker" "step counter" "walking app"

---

## Integration with RevenueCat

Track app install to subscription:

1. Pass FBCLID to app on install
2. Send RevenueCat events back to Meta
3. Optimize for subscription (not just install)
4. Use 7-day click attribution

---

## Budget Allocation by Phase

### Phase 1: Testing ($500)

- 50% UGC videos
- 30% Static images
- 20% Carousels

### Phase 2: Scaling ($2000/mo)

- 70% Winning creative variants
- 20% New creative tests
- 10% Retargeting

### Phase 3: Growth ($5000+/mo)

- 60% Advantage+ campaigns
- 25% Manual campaigns (niche targeting)
- 15% Retargeting

---

## Resources

- FB Ads Library: facebook.com/ads/library
- Meta Business Help: facebook.com/business/help
- Ad specs: facebook.com/business/ads-guide
