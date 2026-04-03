# Universal Paywall Framework — Integration Guide

**File:** `MONEY_METHODS/APP_FACTORY/paywall/paywall.js`
**Impact:** 45 apps currently have zero monetization. Each integration = ~30 min work.

---

## What it does

- 7-day free trial (auto-starts on first visit, localStorage-based)
- Hard paywall on premium feature access after trial expires
- Annual-first display (BEST VALUE badge, higher LTV)
- Review prompt at configurable milestones (7/30/90/365 days)
- Zero backend — everything in localStorage
- Stripe payment links (no server required)

## Quick Integration (30 min per app)

### Step 1 — Add the script tag
In your `index.html` `<head>`:
```html
<script src="/paywall.js"></script>
```
Or if hosting remotely:
```html
<script src="https://printmaxx-paywall.surge.sh/paywall.js"></script>
```

### Step 2 — Initialize with your config
Anywhere in your app JS (after DOM ready):
```js
const pw = Paywall.init({
  appId: 'soberstreak',          // unique key per app (no spaces)
  appName: 'SoberStreak',
  trialDays: 7,
  annualUrl: 'https://buy.stripe.com/YOUR_ANNUAL_LINK',
  monthlyUrl: 'https://buy.stripe.com/YOUR_MONTHLY_LINK',
  annualPrice: '$19.99/yr',
  monthlyPrice: '$2.99/mo',
  annualLabel: 'Best value — save 44%',
  icon: '🔓',                    // modal header emoji
  tagline: 'Unlock all features',
  features: [
    'Track 5 habits simultaneously',
    'Data export (CSV)',
    'Custom milestone messages',
    'No upgrade prompts',
  ],
  premiumFeatures: ['multi-habit', 'export', 'custom-milestones'],
  reviewUrl: 'https://soberstreak.surge.sh/',
  reviewMilestones: [7, 30, 90, 365],
});
```

### Step 3 — Gate features
```js
// Before any premium action:
if (!pw.gate('multi-habit')) return; // shows paywall + returns false if not allowed

// Or check directly:
if (!pw.isAllowed()) {
  pw.showModal();
  return;
}
```

### Step 4 — Trigger review prompts at milestones
```js
// Call this whenever a streak milestone is reached:
pw.markMilestone(state.streak); // fires review modal at 7, 30, 90, 365 days
```

### Step 5 — Handle upgrade callback (optional)
```js
pw.onUpgrade(() => {
  // e.g. track event, show confirmation
  console.log('User clicked upgrade');
});
```

---

## Stripe Setup (per app, ~10 min)

For each app that needs payment links:

```bash
# 1. Create product (one-time)
curl -s -X POST https://api.stripe.com/v1/products \
  -u "$STRIPE_SECRET_KEY:" \
  -d "name=AppName Pro Annual" \
  -d "metadata[app]=appid"

# 2. Create annual price
curl -s -X POST https://api.stripe.com/v1/prices \
  -u "$STRIPE_SECRET_KEY:" \
  -d "product=prod_XXX" \
  -d "unit_amount=1999" \
  -d "currency=usd" \
  -d "recurring[interval]=year"

# 3. Create annual payment link
curl -s -X POST https://api.stripe.com/v1/payment_links \
  -u "$STRIPE_SECRET_KEY:" \
  -d "line_items[0][price]=price_XXX" \
  -d "line_items[0][quantity]=1"

# Repeat steps 2-3 for monthly ($299, interval=month)
```

---

## App Monetization Queue (45 apps need wiring)

Priority order (largest audience niches first):

| App | Niche | Monthly Price | Annual Price | Status |
|-----|-------|--------------|--------------|--------|
| runningstreak | r/running 4.19M | $1.99/mo | $14.99/yr | NEEDS STRIPE |
| yoga-streak | r/yoga 3.31M | $1.99/mo | $14.99/yr | NEEDS STRIPE |
| hiit-streak | r/hiit 4.72M | $1.99/mo | $14.99/yr | NEEDS STRIPE |
| pushup-streak | r/fitness 4.72M | $1.99/mo | $14.99/yr | NEEDS STRIPE |
| plank-streak | r/fitness 4.72M | $1.99/mo | $14.99/yr | NEEDS STRIPE |
| meditation-streak-landing | r/Meditation 3.52M | $2.99/mo | $19.99/yr | NEEDS STRIPE |
| cycling-streak | r/cycling 1.45M | $1.99/mo | $14.99/yr | NEEDS STRIPE |
| breathwork-streak | r/breathwork | $1.99/mo | $14.99/yr | NEEDS STRIPE |
| water-streak | r/fitness | $0.99/mo | $7.99/yr | NEEDS STRIPE |
| gratitude-streak | r/gratitude | $1.99/mo | $14.99/yr | NEEDS STRIPE |
| studylock | r/studying | $2.99/mo | $19.99/yr | NEEDS STRIPE |
| walktounlock-web | productivity | $1.99/mo | $14.99/yr | NEEDS STRIPE |
| streakr | habits 122 score | $4.99/mo | $29.99/yr | HAS STRIPE |
| soberstreak | r/NoFap 1.24M | $2.99/mo | $19.99/yr | HAS STRIPE ✓ |

---

## Pricing Strategy

- **Fitness streaks:** $1.99/mo / $14.99/yr (low barrier, volume play)
- **Health/wellness:** $2.99/mo / $19.99/yr (standard tier)
- **Productivity:** $4.99/mo / $29.99/yr (higher willingness to pay)
- Always show annual first with BEST VALUE badge
- Soft launch at lower price, test up

## Trial Notes

- 7-day trial starts on FIRST VISIT (no opt-in required)
- User sees trial countdown in paywall modal
- After 7 days: premium features show paywall on access attempt
- Free tier always includes core functionality (streak tracking, basic heatmap)
- Premium gates: multiple habits, data export, advanced analytics, no prompts

## Revenue Projections (conservative)

| Scenario | Apps | Avg users/app | Conv rate | Avg price | MRR |
|----------|------|--------------|-----------|-----------|-----|
| Conservative | 10 | 50 | 3% | $2/mo | $30 |
| Base | 20 | 200 | 5% | $2/mo | $400 |
| Optimistic | 45 | 500 | 8% | $2.50/mo | $4,500 |

The framework costs zero to add. Every unmonetized app is leaving money on the table.
