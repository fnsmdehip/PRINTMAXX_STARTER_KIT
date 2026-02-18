# App Launch Checklist

## Phase 1: Pre-Development (Week -4 to -2)

### Market Research
- [ ] Identify 5+ competitor apps
- [ ] Document their pricing, reviews, features
- [ ] Find gaps/complaints in competitor reviews
- [ ] Validate demand (keyword volume, Reddit mentions)
- [ ] Define niche differentiation

### Technical Planning
- [ ] Choose tech stack (React Native, Flutter, native)
- [ ] Set up development environment
- [ ] Create GitHub repository
- [ ] Define MVP feature set (max 3 core features)
- [ ] Search for MIT-licensed repos to fork

### Business Setup
- [ ] Apple Developer Account ($99/year)
- [ ] Google Play Console ($25 one-time)
- [ ] RevenueCat account (subscription management)
- [ ] Analytics setup (Mixpanel, Amplitude, or PostHog)

---

## Phase 2: Development (Week -2 to 0)

### Core Build
- [ ] Scaffold app structure
- [ ] Implement core feature 1
- [ ] Implement core feature 2
- [ ] Implement core feature 3 (if MVP scope)
- [ ] Add onboarding flow

### Monetization Integration
- [ ] RevenueCat SDK integrated
- [ ] Subscription products created in App Store Connect
- [ ] Subscription products created in Google Play Console
- [ ] Paywall UI implemented
- [ ] Free trial configured (if applicable)

### Polish
- [ ] App icon designed (1024x1024, no text)
- [ ] Splash screen created
- [ ] Loading states for all async operations
- [ ] Error handling with user-friendly messages
- [ ] Haptic feedback on key actions

---

## Phase 3: App Store Prep (Week 0)

### iOS App Store Connect
- [ ] App name reserved
- [ ] Privacy policy URL (required)
- [ ] Support URL
- [ ] App category selected
- [ ] Age rating questionnaire completed
- [ ] 6.5" iPhone screenshots (6 required)
- [ ] 12.9" iPad screenshots (if applicable)
- [ ] App preview video (optional but recommended)
- [ ] Description written (4000 char max)
- [ ] Keywords field optimized (100 char max)
- [ ] What's New text prepared

### Google Play Console
- [ ] App name and description
- [ ] Privacy policy URL
- [ ] Feature graphic (1024x500)
- [ ] Phone screenshots (min 2)
- [ ] Tablet screenshots (if applicable)
- [ ] Short description (80 char max)
- [ ] Full description (4000 char max)
- [ ] Content rating questionnaire
- [ ] Target audience selected

### Legal
- [ ] Privacy policy page live
- [ ] Terms of service page live
- [ ] GDPR compliance (if EU users)
- [ ] CCPA compliance (if CA users)
- [ ] No copyrighted content in app

---

## Phase 4: Submission (Week 0)

### Pre-Submit Checklist
- [ ] Test on multiple device sizes
- [ ] Test in airplane mode
- [ ] Test all IAP flows
- [ ] Test restore purchases
- [ ] Remove all console.log/debug statements
- [ ] Increment version number
- [ ] Archive and upload to TestFlight
- [ ] Internal testing completed

### Submit to Review
- [ ] iOS: Submit for review
- [ ] Android: Submit for review (if ready)
- [ ] Prepare for rejection notes (common issues)
- [ ] Monitor review status daily

### Common Rejection Reasons (Avoid These)
- [ ] Guideline 4.2: Minimum functionality (app too simple)
- [ ] Guideline 3.1.1: IAP issues (using external payment)
- [ ] Guideline 2.1: App crashes or has bugs
- [ ] Guideline 5.1.1: Privacy policy missing/incomplete
- [ ] Guideline 4.3: Spam (too similar to existing app)

---

## Phase 5: Launch Day (Week 1)

### Technical
- [ ] Monitor crash reports
- [ ] Check analytics events firing
- [ ] Verify IAP transactions working
- [ ] Respond to any immediate bugs

### Marketing
- [ ] Post on Product Hunt (schedule ahead)
- [ ] Post in relevant subreddits
- [ ] Post on Twitter/X with screenshots
- [ ] Email your list (if applicable)
- [ ] Post in relevant Discord/Slack communities

### Content
- [ ] Publish App Store screenshot images to social
- [ ] Create launch announcement video (Remotion)
- [ ] Write launch blog post (for SEO)

---

## Phase 6: Post-Launch (Week 1-4)

### Growth
- [ ] Respond to all App Store reviews
- [ ] A/B test screenshots (after 500+ impressions)
- [ ] Monitor keyword rankings
- [ ] Iterate on conversion data

### Optimization
- [ ] Analyze funnel: Download → Open → Paywall → Subscribe
- [ ] Identify drop-off points
- [ ] Test paywall timing
- [ ] Test pricing

### Metrics to Track

| Metric | Target | Track In |
|--------|--------|----------|
| Downloads | 100+ first week | App Store Connect |
| Conversion Rate | 2-5% | RevenueCat |
| Day 1 Retention | 40%+ | Analytics |
| Day 7 Retention | 20%+ | Analytics |
| ARPU | $2+ | RevenueCat |

---

## Launch Week Schedule

| Day | Task |
|-----|------|
| Monday | Submit to App Store |
| Tuesday | Prepare launch content |
| Wednesday | Approval (hopefully) |
| Thursday | Launch posts, Product Hunt |
| Friday | Community engagement, reviews |
| Saturday | Monitor, fix urgent bugs |
| Sunday | Week 1 retrospective |

---

## Emergency Contacts

- Apple App Review: appstorereviewboard@apple.com
- Google Play Support: Through Play Console
- RevenueCat Support: support@revenuecat.com

---

Last updated: 2026-01-23
