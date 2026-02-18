# Google App Campaigns Playbook

**Last Updated:** 2026-01-23
**Status:** Ready for implementation post-launch

---

## Quick Start Checklist

- [ ] Google Ads account created
- [ ] App linked from Play Console
- [ ] Firebase SDK installed (Android)
- [ ] Conversion tracking set up
- [ ] First campaign drafted

---

## When to Use Google App Campaigns

**Best for:**
- Android app installs
- Cross-platform reach (YouTube, Search, Play Store, Display)
- Larger budgets ($50+/day)
- Apps with broad appeal

**Start when:**
- App Store Ads running profitably
- Budget $1500+/month for Google
- Have 10+ creative assets ready

---

## Campaign Types

### App Campaigns for Installs (ACi)

Primary campaign type. Google AI optimizes for installs.

### App Campaigns for Engagement (ACe)

Re-engage existing users. Requires Firebase events.

### App Campaigns for Pre-Registration

Android only. Build waitlist before launch.

**Start with:** App Campaigns for Installs

---

## Account Setup

### 1. Link App

```
1. Google Ads > Tools > Linked accounts
2. Link Google Play (Android)
3. Link Firebase
4. Verify app appears
```

### 2. Conversion Tracking

**Events to track:**
- `first_open` - App opened first time
- `in_app_purchase` - Any purchase
- `subscription_start` - Started subscription
- `subscription_renew` - Renewed subscription

### 3. Firebase Setup

```javascript
// React Native with Firebase
import analytics from '@react-native-firebase/analytics';

// Track subscription
await analytics().logEvent('subscription_start', {
  plan: 'annual',
  price: 29.99,
  currency: 'USD'
});
```

---

## Campaign Structure

Google App Campaigns are fully automated. You provide:
1. Budget
2. Target CPI/CPA
3. Creative assets
4. Target locations

Google handles:
- Bidding
- Placements
- Audience targeting
- Creative combinations

```
Campaign: [App] - Installs - [Date]
├── Budget: $100/day
├── Target CPI: $2.00
├── Locations: US, CA, UK, AU
└── Assets:
    ├── Text: 5 headlines + 5 descriptions
    ├── Images: 20 images (various sizes)
    ├── Videos: 3-5 videos (portrait + landscape)
    └── HTML5: Optional playable ads
```

---

## Creative Assets

### Text Assets

**Headlines (5 required, 30 char max):**
```
1. Lock Your Phone to Pray
2. Build a Prayer Habit
3. Faith-Based Focus Timer
4. Start Your Day Right
5. Free Christian App
```

**Descriptions (5 required, 90 char max):**
```
1. Lock your phone until you complete your morning prayer. Build streaks.
2. Join 100,000+ Christians building daily prayer habits with PrayerLock.
3. Stop scrolling. Start praying. Lock your screen until you connect with God.
4. Transform your morning routine. Free download, premium features available.
5. The app that helped me pray consistently for the first time in years.
```

### Image Assets

| Size | Use | Quantity |
|------|-----|----------|
| 1200x628 | YouTube, Display | 5+ |
| 1200x1200 | Display, Discovery | 5+ |
| 300x250 | Display | 3+ |
| 320x50 | Banner | 3+ |
| 480x320 | App install | 3+ |

**Tips:**
- Include app icon in images
- Show app UI/screenshots
- Use faces when possible
- High contrast text
- Clear value prop

### Video Assets

| Format | Duration | Use |
|--------|----------|-----|
| Portrait (9:16) | 15-30s | YouTube Shorts, TikTok-style |
| Landscape (16:9) | 15-30s | YouTube pre-roll |
| Square (1:1) | 15-30s | Feed placements |

**Video formula:**
```
0-3s: Hook (problem or result)
3-15s: Show app in use
15-25s: Social proof or benefit
25-30s: CTA + app icon
```

---

## Budget Guidelines

### Minimum Viable

| Phase | Daily Budget | Duration |
|-------|-------------|----------|
| Learning | $50/day | 14 days |
| Optimization | $100/day | 30 days |
| Scaling | $200+/day | Ongoing |

**Warning:** Google needs volume to optimize. Under $50/day may not exit learning.

### Target CPI by Category

| Category | Target CPI | Typical Range |
|----------|------------|---------------|
| Health & Fitness | $2.00 | $1-4 |
| Productivity | $1.50 | $0.50-3 |
| Lifestyle | $1.00 | $0.50-2 |
| Education | $2.50 | $1-5 |

---

## Optimization

### What You Can Control

1. **Budget** - Increase for winners
2. **Target CPI** - Adjust based on results
3. **Creative assets** - Add/remove
4. **Locations** - Expand or restrict
5. **Device targeting** - Android version, device type

### What Google Controls

- Bidding
- Placements
- Audience selection
- Creative combinations
- Time of day

### Weekly Optimization

1. **Check conversion rate by asset:**
   - Remove underperforming images/videos
   - Add new variants of winners

2. **Review placement performance:**
   - Google shows where ads appeared
   - Can't exclude, but can adjust strategy

3. **Adjust target CPI:**
   - If under target: Lower CPI, same budget
   - If over target: Raise CPI or pause

---

## Key Metrics

| Metric | Target | Kill Campaign If |
|--------|--------|------------------|
| CPI | <$2.00 | >$5.00 after 14 days |
| CVR (install) | >15% | <5% |
| Day 7 retention | >10% | <5% |
| CPA (subscription) | <$20 | >$50 |

### Tracking Funnel

```
Impressions → Clicks → Installs → Day 1 → Day 7 → Trial → Subscription
```

---

## Asset Best Practices

### Images That Work

1. **App UI screenshots** - Show the product
2. **Before/after** - Transformation
3. **Face + phone** - Person using app
4. **Icon + headline** - Simple and clear
5. **Social proof** - Star rating, user count

### Images That Fail

- Generic stock photos
- Too much text
- Low contrast
- No app connection
- Cluttered design

### Video That Works

1. **Problem-solution** - Show pain then relief
2. **Demo** - Screen recording with voiceover
3. **Testimonial** - UGC style
4. **Results** - Numbers and proof

---

## Android-Specific Considerations

### Play Store Listing Optimization

Google uses your Play Store listing for ads:
- Title (30 chars)
- Short description (80 chars)
- Screenshots (up to 8)
- Feature graphic
- Video

**Optimize Play Store first, then run ads.**

### Pre-Registration Campaigns

For apps not yet launched:

1. Set up pre-registration in Play Console
2. Create App Campaign for Pre-Registration
3. Budget $20-50/day
4. Collect signups
5. Launch notification goes to all pre-registered users

---

## Integration

### Firebase + Google Ads

```javascript
// Track key events for optimization
analytics().logEvent('level_complete', {
  level: 7,
  score: 1234
});

analytics().logEvent('spend_virtual_currency', {
  value: 10,
  virtual_currency_name: 'coins'
});

analytics().logPurchase({
  currency: 'USD',
  value: 29.99,
  items: [{ item_name: 'Annual Subscription' }]
});
```

### RevenueCat + Google Ads

1. Enable Google Ads attribution in RevenueCat
2. Send purchase events to Google
3. Optimize campaigns for subscription, not install

---

## Budget Allocation

### Phase 1: Launch ($1500/month)

- 70% App Campaigns for Installs
- 20% Search Ads (competitor keywords)
- 10% YouTube (awareness)

### Phase 2: Scale ($5000/month)

- 60% App Campaigns (optimized)
- 25% App Campaigns for Engagement (re-engagement)
- 15% YouTube (brand building)

---

## Common Mistakes

1. **Under-funding** - $10/day won't optimize
2. **Few creative assets** - Need 20+ for combinations
3. **Optimizing too early** - Wait 14 days minimum
4. **Ignoring Play Store** - Listing affects ad performance
5. **Install-only focus** - Optimize for revenue events

---

## When to Pause

Pause campaign if:
- CPI 2x target after 14 days
- No subscriptions after 500 installs
- Day 1 retention under 20%
- Creative fatigue (rising CPI over 4 weeks)

---

## Resources

- Google App Campaigns: ads.google.com/home/campaigns/app-campaigns
- Firebase Analytics: firebase.google.com/docs/analytics
- Play Console: play.google.com/console
- Asset specs: support.google.com/google-ads/answer/9893845
