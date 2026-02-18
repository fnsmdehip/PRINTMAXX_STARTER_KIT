# TikTok Ads Playbook

**Last Updated:** 2026-01-23
**Status:** Ready for implementation post-revenue

---

## Quick Start Checklist

- [ ] TikTok Business Center account
- [ ] Ad account created
- [ ] Pixel installed
- [ ] Payment method added
- [ ] First Spark Ad test ready

---

## When to Use TikTok Ads

**Best for:**
- App installs (especially fitness, productivity)
- Gen Z/Millennial audiences
- Products with strong visual hook
- UGC-style content

**Start when:**
- Have 5+ organic TikToks performing well
- Budget minimum $500/month
- Clear CPI target defined

---

## Account Setup

### 1. Business Center

```
1. Go to ads.tiktok.com
2. Create Business Center
3. Create Ad Account
4. Add payment method
5. Install pixel
```

### 2. Pixel Installation

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

---

## Campaign Types

### 1. Spark Ads (Recommended)

Boost organic creator content. Lower CPM, higher engagement.

**How it works:**
1. Creator posts organically
2. You request Spark Ad authorization
3. Boost their content with your budget
4. Keeps engagement on original post

**Best for:**
- UGC from creators
- Your own viral organic posts
- Authentic-looking content

### 2. In-Feed Ads

Standard ads in For You feed.

**Specs:**
- 9:16 ratio (required)
- 5-60 seconds (15-30 optimal)
- Sound on by default
- Captions recommended

### 3. TopView

First ad user sees when opening app.

**Cost:** High ($50k+ minimum)
**Use:** Brand awareness at scale

---

## Campaign Structure

```
Campaign: [App] - App Install - [Date]
├── Ad Group 1: Broad (no targeting)
│   ├── Ad 1: UGC Testimonial
│   ├── Ad 2: Problem/Solution
│   └── Ad 3: How-To Demo
├── Ad Group 2: Interest Targeting
│   ├── Ad 1: UGC Testimonial
│   ├── Ad 2: Problem/Solution
│   └── Ad 3: How-To Demo
└── Ad Group 3: Spark Ads (boosted organic)
    ├── Spark Ad 1: Top organic post
    ├── Spark Ad 2: Creator UGC
    └── Spark Ad 3: Influencer content
```

---

## Budget Guidelines

| Phase | Daily Budget | Duration | Notes |
|-------|-------------|----------|-------|
| Testing | $50/day min | 7 days | TikTok needs volume |
| Learning | $100/day | 14 days | Exit learning phase |
| Scaling | $200-500/day | Ongoing | Scale winners only |

**Minimum campaign budget:** $500 (required by TikTok)

---

## Creative Guidelines

### TikTok Ad Formula

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

### What Works on TikTok

1. **Native-looking content** - Not polished ads
2. **Sound on** - Use trending sounds when possible
3. **Text overlays** - Large, readable
4. **Quick cuts** - 2-3 second scenes max
5. **Hook in 0.5 seconds** - Instant pattern interrupt

### What Fails

- Corporate/polished look
- Slow intros
- No text overlays
- Horizontal video
- Generic stock footage

---

## Targeting by Niche

### Fitness (WalkToUnlock)

**Interests:**
- Fitness & Wellness
- Running, Walking, Outdoor activities
- Wearable tech
- Health apps

**Behaviors:**
- App downloaders (Health & Fitness)
- In-app purchasers

### Faith (PrayerLock)

**Interests:**
- Religion & Spirituality
- Christianity, Bible
- Self-improvement
- Meditation

### Students (StudyLock)

**Interests:**
- Education
- College, University
- Study tips
- Productivity

**Demographics:**
- 18-24 age
- Students

---

## Spark Ads Setup

### Getting Authorization

1. Creator posts organically
2. Creator goes to Settings > Creator Tools > TikTok Creator Marketplace
3. Creator enables authorization
4. Creator provides authorization code
5. You add code in Ads Manager

### Finding Creators

1. Search hashtags in your niche
2. Look for 10K-100K followers (micro-influencers)
3. DM with Spark Ad proposal
4. Offer flat fee + performance bonus

**Outreach template:**

```
Hey [Name]!

Love your content about [topic]. We built [App] that does [thing].

Would you be interested in a paid partnership? We'd send you the app free + $150 for a video + bonus if it performs well.

Let me know if you're open to it!
```

---

## Optimization

### Learning Phase

TikTok needs 50 conversions in 7 days to exit learning phase.

**If stuck in learning:**
- Increase budget
- Broaden targeting
- Add more creatives
- Combine ad groups

### Key Metrics

| Metric | Target | Kill If |
|--------|--------|---------|
| CTR | >1% | <0.5% |
| CPC | <$0.50 | >$1.00 |
| CPM | <$10 | >$25 |
| CPI (install) | <$2.00 | >$5.00 |
| CVR | >2% | <0.5% |

### Weekly Optimization

1. Kill ad groups with CPI 2x target
2. Duplicate winners with 20% budget increase
3. Add 2-3 new creatives
4. Test new hooks on top performers

---

## Creative Testing Framework

### Hook Testing

Create 5 versions of same ad with different hooks:

1. **Question hook:** "Why is everyone deleting Instagram?"
2. **POV hook:** "POV: You finally have time for hobbies"
3. **Shock hook:** "This app made my husband talk to me again"
4. **Social proof:** "2M people have quit scrolling with this"
5. **Result hook:** "I got 3 hours of my life back daily"

### Body Testing

Once winning hook found, test:
- Demo style (screen record vs lifestyle)
- Length (15s vs 30s vs 60s)
- Music (trending vs no music)
- Creator (different faces)

---

## Integration

### TikTok Shop

If promoting physical products, integrate TikTok Shop:
- Direct checkout in-app
- Affiliate links for creators
- Shop tab on profile

### Events API

Send server-side events for better attribution:

```javascript
// Send purchase event
await fetch('https://business-api.tiktok.com/open_api/v1.3/pixel/track/', {
  method: 'POST',
  headers: {
    'Access-Token': 'YOUR_ACCESS_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    pixel_code: 'YOUR_PIXEL_ID',
    event: 'CompletePayment',
    event_id: 'unique_event_id',
    timestamp: Date.now(),
    context: {
      user: { external_id: 'user_id' }
    },
    properties: {
      currency: 'USD',
      value: 9.99
    }
  })
});
```

---

## Competitor Research

### TikTok Creative Center

1. Go to ads.tiktok.com/business/creativecenter
2. Search competitor apps
3. Filter by: Top ads, Last 30 days
4. Study: Hooks, visuals, CTAs

**Search terms:**
- "screen time app"
- "prayer app" "Christian app"
- "study timer" "focus app"
- "fitness tracker" "walking app"

---

## Budget Allocation

### Phase 1: Testing ($1000)

- 60% Spark Ads (boost organic)
- 30% In-Feed (own creatives)
- 10% Creator partnerships

### Phase 2: Scaling ($3000/mo)

- 50% Spark Ads
- 30% Top performers (in-feed)
- 20% New creative tests

---

## Common Mistakes

1. **Polished content** - TikTok rewards native feel
2. **Slow hooks** - Need pattern interrupt in 0.5s
3. **No sound** - TikTok is sound-on platform
4. **Small budget** - $20/day won't exit learning
5. **Ignoring Spark Ads** - Best performing format

---

## Resources

- TikTok Creative Center: ads.tiktok.com/business/creativecenter
- TikTok Ads Manager: ads.tiktok.com
- TikTok Pixel Helper: Chrome extension
