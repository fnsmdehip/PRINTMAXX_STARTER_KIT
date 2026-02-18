# Pre-Launch Checklist

Everything that must be ready before you hit "release."

---

## Technical readiness

### Core app functionality

- [ ] All core features working without crashes
- [ ] Edge cases handled (no data, slow network, etc.)
- [ ] Offline mode works (if applicable)
- [ ] App launches in under 3 seconds
- [ ] Memory usage stable (no leaks)
- [ ] Battery drain acceptable

### Device testing

- [ ] Tested on iPhone 11/12 (minimum supported)
- [ ] Tested on iPhone 14/15 (latest)
- [ ] Tested on iPad (if universal app)
- [ ] Tested on Android mid-range (Pixel 5/6)
- [ ] Tested on Android flagship (Pixel 8, Samsung S24)
- [ ] Tested on older Android (API 26+)

### Network conditions

- [ ] Works on WiFi
- [ ] Works on cellular (4G/5G)
- [ ] Works on slow connection (simulate 3G)
- [ ] Works on IPv6 network (Apple requirement)
- [ ] Handles network loss gracefully
- [ ] Handles network reconnection

### Payment integration

- [ ] RevenueCat SDK integrated
- [ ] Sandbox purchases working (iOS)
- [ ] Test purchases working (Android)
- [ ] Restore purchases functional
- [ ] Subscription management working
- [ ] Paywall displays correctly
- [ ] All products configured in dashboards
- [ ] Webhook endpoints configured

### Analytics and monitoring

- [ ] Analytics SDK integrated (Mixpanel/Amplitude/PostHog)
- [ ] Key events tracked:
  - [ ] App open
  - [ ] Onboarding start/complete
  - [ ] Feature usage
  - [ ] Paywall view
  - [ ] Purchase attempt
  - [ ] Purchase success/failure
- [ ] Crash reporting enabled (Sentry/Crashlytics)
- [ ] Error logging in place
- [ ] User identification working

### Authentication (if applicable)

- [ ] Sign up flow works
- [ ] Login flow works
- [ ] Password reset works
- [ ] Social login works (Apple, Google)
- [ ] Account deletion works (required for App Store)
- [ ] Session management correct

---

## Marketing assets

### App Store (iOS)

- [ ] App icon (1024x1024, no transparency)
- [ ] Screenshots (6.5" iPhone, 5.5" iPhone)
  - [ ] At least 4 screenshots
  - [ ] Show key features
  - [ ] Include text overlays
- [ ] App preview video (optional but recommended)
  - [ ] 15-30 seconds
  - [ ] Shows app in action
  - [ ] No device frames in video itself
- [ ] App name (30 chars max, unique)
- [ ] Subtitle (30 chars max, key benefit)
- [ ] Keywords (100 chars, comma-separated)
- [ ] Description (first 3 lines crucial)
- [ ] Promotional text (170 chars, can update without review)
- [ ] What's New text
- [ ] Category and secondary category
- [ ] Age rating configured
- [ ] Privacy nutrition labels complete

### Google Play

- [ ] Feature graphic (1024x500)
- [ ] App icon (512x512)
- [ ] Screenshots (phone and 7" tablet minimum)
- [ ] Short description (80 chars)
- [ ] Full description (4000 chars)
- [ ] Promo video (YouTube link, optional)
- [ ] Content rating questionnaire done
- [ ] Data safety form complete
- [ ] Category selected
- [ ] Tags selected

### Landing page assets

- [ ] Domain live and pointing to site
- [ ] SSL certificate active (https)
- [ ] Hero image or video
- [ ] App screenshots (mockups in device frames)
- [ ] Feature icons/illustrations
- [ ] Testimonial photos/avatars
- [ ] App Store badge (official Apple badge)
- [ ] Google Play badge (official Google badge)
- [ ] Social sharing image (1200x630 for OG)
- [ ] Favicon

### Social media assets

- [ ] Profile photos for all accounts
- [ ] Cover/header images
- [ ] Content templates in Canva/Figma
- [ ] Video templates
- [ ] Brand colors and fonts documented

---

## Support readiness

### Help documentation

- [ ] FAQ page or section ready
- [ ] Basic help articles (5-10 minimum):
  - [ ] Getting started
  - [ ] How to use [main feature]
  - [ ] Subscription/billing questions
  - [ ] Account/data questions
  - [ ] Troubleshooting common issues
- [ ] Help accessible from within app
- [ ] Contact support method clear

### Support systems

- [ ] Support email configured (support@domain.com)
- [ ] Email forwarding to your inbox working
- [ ] Helpdesk set up (if using: Crisp, Intercom, Zendesk)
- [ ] Canned responses ready for common questions
- [ ] Bug report template ready
- [ ] Refund request process defined

### Response plan

- [ ] Who handles support during launch?
- [ ] Response time target (< 24 hours recommended)
- [ ] Escalation path for urgent issues
- [ ] Refund policy defined and documented
- [ ] What warrants immediate action (crashes, payment issues)

---

## Legal compliance

### Required legal pages

- [ ] Privacy policy live at public URL
  - [ ] Covers data collection
  - [ ] Covers data usage
  - [ ] Covers third parties (analytics, payment)
  - [ ] Includes contact info
  - [ ] GDPR compliant (if EU users)
  - [ ] CCPA compliant (if CA users)
- [ ] Terms of service live at public URL
  - [ ] Acceptable use
  - [ ] Account termination
  - [ ] Limitation of liability
  - [ ] Dispute resolution

### App store requirements

- [ ] Privacy policy URL entered in App Store Connect
- [ ] Privacy policy URL entered in Google Play Console
- [ ] Privacy nutrition labels complete (iOS)
- [ ] Data safety form complete (Android)
- [ ] Account deletion mechanism (if accounts exist)
- [ ] Age rating accurate
- [ ] No misleading content claims

### Payment compliance

- [ ] Subscriptions clearly described
- [ ] Pricing displayed correctly
- [ ] Free trial terms clear
- [ ] Auto-renewal disclosed
- [ ] Restore purchases available
- [ ] Cancel subscription instructions accessible

### Content compliance

- [ ] No copyrighted content without license
- [ ] No trademarked names without permission
- [ ] User-generated content moderation plan (if applicable)
- [ ] Appropriate content for age rating

---

## Monitoring setup

### App performance

- [ ] Crash reporting dashboard accessible
- [ ] Error tracking dashboard accessible
- [ ] Performance monitoring enabled (if using)
- [ ] API monitoring (if applicable)

### Revenue tracking

- [ ] RevenueCat dashboard showing data
- [ ] Subscription events visible
- [ ] Revenue charts populating
- [ ] Trial conversion tracking working

### Analytics dashboards

- [ ] Real-time user tracking working
- [ ] Funnel visualization set up
- [ ] Key metrics dashboard created
- [ ] Retention cohorts configured

### Alerting

- [ ] Crash spike alerts enabled
- [ ] Error rate alerts enabled
- [ ] Revenue alerts (optional)
- [ ] Downtime alerts (if server-based)

---

## Final verification

### Test one more time

- [ ] Download TestFlight build
- [ ] Complete full user journey
- [ ] Make a purchase (sandbox)
- [ ] Check analytics received
- [ ] Force crash and verify it's reported
- [ ] Test on WiFi and cellular

### Team ready

- [ ] Everyone knows launch time
- [ ] Everyone knows their role
- [ ] Communication channels tested
- [ ] Emergency contacts shared
- [ ] Monitoring access confirmed

### Marketing queued

- [ ] Launch email drafted and scheduled
- [ ] Social posts drafted and scheduled
- [ ] Landing page ready for traffic
- [ ] Affiliate/partner notifications drafted

### Psychological readiness

- [ ] Accepted that something will break
- [ ] Plan for handling negative feedback
- [ ] Prepared to iterate quickly
- [ ] Ready to ship fixes same day if needed

---

## Go/no-go decision

Answer these before proceeding:

1. **Does the core feature work reliably?** If no, delay.
2. **Can users pay you?** If no, delay.
3. **Can you respond to support?** If no, plan coverage.
4. **Are legal requirements met?** If no, delay.
5. **Do you know if it crashes?** If no, enable monitoring first.

If all yes: Ship it.

---

## Common launch blockers

| Issue | Solution | Time needed |
|-------|----------|-------------|
| App Store rejection | See APP_STORE_REJECTION_GUIDE.md | 1-3 days |
| Payment not working | Verify RevenueCat config, sandbox mode | 1-2 hours |
| Screenshots wrong size | Use official size specs, regenerate | 30 min |
| Privacy policy missing | Use generator (Termly, iubenda) | 1 hour |
| Analytics not firing | Check SDK init, event names | 1-2 hours |
| Slow app launch | Profile startup, lazy load | 2-4 hours |

---

Created: 2026-01-21
