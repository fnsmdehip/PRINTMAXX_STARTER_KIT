# Affiliate Landing Page Copy

Complete copy for the affiliate signup page. Ready to implement in any landing page builder.

---

## Page structure

```
1. Hero section
2. Commission display
3. How it works
4. Earnings calculator
5. What we provide
6. FAQ
7. Application form
```

---

## Hero section

### Headline options

**Option A (results-focused):**
```
Earn $200-2,000/month promoting apps you actually use
```

**Option B (simplicity-focused):**
```
Get paid to share what you already love
```

**Option C (creator-focused):**
```
Turn your audience into recurring income
```

### Subheadline

```
Join [X] creators earning commission every time their audience downloads our apps. No inventory, no support tickets, no hassle.
```

### CTA button

```
Apply in 2 minutes
```

---

## Commission display

### Main commission box

```
+------------------------------------------+
|                                          |
|    Earn up to 30% commission             |
|    on every sale you refer               |
|                                          |
|    Average affiliate earns: $XXX/month   |
|    Top affiliates earn: $X,XXX/month     |
|                                          |
+------------------------------------------+
```

### Commission breakdown cards

**Card 1: Starter**
```
STARTER
20% commission
Get started immediately
- 20% first payment
- 10% recurring for 12 months
- $25 minimum payout
```

**Card 2: Pro**
```
PRO
25% commission
After 10+ sales/month
- 25% first payment
- 12% recurring for 12 months
- $10 minimum payout
- Priority support
```

**Card 3: Elite**
```
ELITE
30% commission
After 50+ sales/month
- 30% first payment
- 15% recurring for 12 months
- No minimum payout
- Weekly payments
- Direct founder access
```

---

## How it works

### Step-by-step process

```
STEP 1: Apply (2 minutes)
Fill out the form below. We review applications within 24 hours.

STEP 2: Get your link
Receive your unique affiliate link and promo code instantly after approval.

STEP 3: Share with your audience
Post about [App Name] using the swipe files and assets we provide.

STEP 4: Get paid monthly
Earn commission on every sale. Paid via PayPal on the 1st of each month.
```

### Visual flow

```
[Apply] → [Get Link] → [Share] → [Earn]
   ↓          ↓           ↓         ↓
 2 min    Instant     Your way   Monthly
```

---

## Earnings calculator

### Interactive calculator copy

```
HOW MUCH CAN YOU EARN?

Your followers: [slider or input: 1k - 500k]
Average engagement: [slider: 1% - 10%]
Posts per month: [slider: 1 - 30]

---

Estimated monthly earnings: $XXX - $X,XXX

Based on:
- XX estimated clicks
- XX estimated signups
- XX estimated paid conversions
- $X.XX average commission per sale

This is an estimate. Actual results depend on your content and audience fit.
```

### Calculator formula (for developers)

```javascript
// Conservative estimate
function calculateEarnings(followers, engagementRate, postsPerMonth) {
  const clickRate = 0.02; // 2% of engaged users click
  const signupRate = 0.30; // 30% of clicks convert to signup
  const paidRate = 0.10; // 10% of signups go paid
  const avgCommission = 2.00; // $2 per paid conversion

  const monthlyEngaged = followers * engagementRate * postsPerMonth;
  const clicks = monthlyEngaged * clickRate;
  const signups = clicks * signupRate;
  const paid = signups * paidRate;
  const earnings = paid * avgCommission;

  return {
    clicks: Math.round(clicks),
    signups: Math.round(signups),
    paid: Math.round(paid),
    earningsLow: Math.round(earnings * 0.5),
    earningsHigh: Math.round(earnings * 1.5)
  };
}
```

### Static earnings examples (alternative to calculator)

```
YOUR AUDIENCE SIZE    ESTIMATED MONTHLY EARNINGS

1,000 followers       $20 - $50
5,000 followers       $50 - $150
10,000 followers      $100 - $300
25,000 followers      $250 - $750
50,000 followers      $500 - $1,500
100,000+ followers    $1,000 - $3,000+
```

---

## What we provide

### Asset cards

**Card 1: Ready-to-post content**
```
SWIPE FILES
- 10 TikTok/Reels scripts
- 15 caption templates
- 5 email templates
- Story templates
- Hashtag lists

Copy, customize, post.
```

**Card 2: Creative assets**
```
GRAPHICS & BANNERS
- Banner ads (all sizes)
- Social media graphics
- App screenshots
- Logo files
- Brand colors

Professional designs ready to use.
```

**Card 3: Support**
```
AFFILIATE SUPPORT
- Dedicated affiliate manager
- Private Discord community
- Monthly strategy calls
- Performance insights
- Custom assets on request

We help you succeed.
```

**Card 4: Tracking**
```
REAL-TIME DASHBOARD
- Track clicks instantly
- See conversions live
- Monitor earnings
- Export reports
- UTM parameter support

Know exactly what's working.
```

---

## FAQ section

### Frequently asked questions

**Q: Who can join?**
```
Anyone with an audience in fitness, faith, productivity, or self-improvement niches. We accept creators of all sizes, from 1k to 1M+ followers.
```

**Q: How do I get paid?**
```
Monthly via PayPal on the 1st. Minimum payout is $25 for Starter tier. We also support Wise for international affiliates.
```

**Q: When do I get my affiliate link?**
```
Immediately after approval. Most applications are reviewed within 24 hours.
```

**Q: How long does the cookie last?**
```
30 days. If someone clicks your link and purchases within 30 days, you get credit.
```

**Q: Can I promote on multiple platforms?**
```
Yes. Use your link on TikTok, Instagram, YouTube, Twitter, email, blog, or anywhere else. We track all conversions.
```

**Q: Do I need to disclose the affiliate relationship?**
```
Yes. FTC requires disclosure. We provide exact language to use. It's simple: just add "#ad" or "affiliate link" to your posts.
```

**Q: What if my referral requests a refund?**
```
Commissions are adjusted if a customer refunds within 30 days. After 30 days, your commission is locked.
```

**Q: Can I use paid ads?**
```
Yes, but not for branded search terms (our app name). Display, social, and content ads are allowed.
```

**Q: Is there a minimum sales requirement?**
```
No minimums. Promote as much or as little as you want. We keep your account active indefinitely.
```

**Q: How do I get to higher commission tiers?**
```
Automatic. Hit 10 sales in a month → Pro tier. Hit 50 sales → Elite tier. Tier resets monthly based on performance.
```

---

## Application form

### Form fields

```
BECOME AN AFFILIATE

Name *
[text input]

Email *
[email input]

Primary platform *
[dropdown: TikTok, Instagram, YouTube, Twitter/X, Blog, Podcast, Email list, Other]

Your handle/URL *
[text input]
(e.g., @yourhandle or yoursite.com)

Follower/subscriber count *
[dropdown: Under 1k, 1k-5k, 5k-10k, 10k-50k, 50k-100k, 100k+]

Your niche *
[dropdown: Fitness, Faith/Spirituality, Productivity, Self-improvement, Tech/AI, Other]

How will you promote [App Name]? *
[textarea]
(Brief description of your content strategy)

PayPal email for payments *
[email input]

[ ] I agree to the affiliate terms and FTC disclosure requirements *

[APPLY NOW]
```

### Form validation messages

```
Name: "Please enter your name"
Email: "Please enter a valid email address"
Platform: "Please select your primary platform"
Handle: "Please enter your social handle or website URL"
Followers: "Please select your follower count"
Niche: "Please select your niche"
Strategy: "Please describe how you'll promote (minimum 20 characters)"
PayPal: "Please enter your PayPal email for payments"
Terms: "Please agree to the affiliate terms"
```

### Success message

```
APPLICATION SUBMITTED

Thanks for applying to the [App Name] affiliate program.

What happens next:
1. We'll review your application within 24 hours
2. You'll receive an email with your unique link and assets
3. Start sharing and earning immediately

Check your email (including spam folder) for our welcome message.

Questions? Email affiliates@[yourdomain].com
```

---

## Social proof section (optional)

### Testimonials from affiliates

**Testimonial 1:**
```
"Made $847 my first month just from TikTok. The swipe files made it easy to get started."
- @sarahfitness, 23k followers
```

**Testimonial 2:**
```
"Best affiliate program I've worked with. Fast payments, great support, and my audience actually loves the app."
- @dailydevotions, 45k followers
```

**Testimonial 3:**
```
"Started as a side thing, now it's $2k/month recurring. The 12-month commission structure is a game changer."
- @productivityhacks, 12k followers
```

### Stats bar

```
[500+]           [$XXX,XXX]        [30 days]        [24 hours]
Affiliates       Paid out          Cookie duration  Approval time
```

---

## SEO metadata

### Title tag
```
Become an Affiliate | Earn 20-30% Commission | [App Name]
```

### Meta description
```
Join the [App Name] affiliate program. Earn 20-30% commission on every sale. Get paid monthly. Free swipe files and assets included. Apply in 2 minutes.
```

### Open Graph

```
og:title: Earn $200-2,000/month as a [App Name] Affiliate
og:description: Join 500+ creators earning recurring commission. 30-day cookie, monthly payments, free content assets.
og:image: [affiliate-og-image.png]
og:url: https://yourapp.com/affiliates
```

---

## Design notes

### Color scheme
- Primary CTA: Brand primary color
- Commission cards: Gradient or distinct colors per tier
- Background: Light with subtle patterns
- Text: High contrast for readability

### Layout
- Mobile-first design
- Above-fold: Hero + main CTA
- Calculator: Interactive, prominent
- Form: Clean, minimal fields
- Trust elements: Testimonials near CTA

### Animations
- Commission cards: Hover effect
- Calculator: Real-time number updates
- Form: Progress indicator
- Success: Confetti or checkmark animation

---

Created: 2026-01-21
