# Module 4: Monetization — Stripe, Paywalls, and Your First Dollar

## What You'll Have After This Module

A working payment system in your app. Users can pay you money. That's the whole point of everything else you've built.

## Why Stripe and Nothing Else

Stripe charges 2.9% + $0.30 per transaction. On a $5/month subscription, you keep $4.56. On a $50 one-time payment, you keep $48.25.

Don't use Gumroad for in-app payments (10% fee). Don't use PayPal (dispute nightmares). Don't use Paddle unless you're selling to the EU and need them to handle VAT.

Stripe is the answer. Every time. Create your account at dashboard.stripe.com.

## Architecture: Client-Only vs. Client + Serverless

### Client-Only (Stripe Payment Links)

This is the fastest path. No backend code at all.

1. Go to Stripe Dashboard > Payment Links
2. Create a link for your product ($5/month subscription or $10 one-time)
3. Customize the checkout page (add your logo, description)
4. Copy the link
5. Put it behind your paywall button

```javascript
// In your app
document.getElementById('upgrade-btn').addEventListener('click', () => {
  window.location.href = 'https://buy.stripe.com/your-payment-link';
});
```

After payment, Stripe redirects to your success URL. Add `?session_id={CHECKOUT_SESSION_ID}` to the redirect URL to verify payment.

**Pros:** 5 minutes to implement. Zero backend.
**Cons:** Can't customize the checkout flow. Limited to Stripe's hosted page.

### Client + Serverless (Full Control)

For more control, use Stripe Checkout with a serverless function. This is what you'll use for most real products.

Create a Netlify function at `netlify/functions/create-checkout.js`:

```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method not allowed' };
  }

  const { priceId } = JSON.parse(event.body);

  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    mode: 'subscription', // or 'payment' for one-time
    success_url: `${process.env.URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.URL}/`,
  });

  return {
    statusCode: 200,
    body: JSON.stringify({ url: session.url }),
  };
};
```

Set your environment variable in Netlify: Site Settings > Environment Variables > Add `STRIPE_SECRET_KEY`.

Frontend call:

```javascript
async function startCheckout() {
  const response = await fetch('/.netlify/functions/create-checkout', {
    method: 'POST',
    body: JSON.stringify({ priceId: 'price_1234567890' }),
  });
  const { url } = await response.json();
  window.location.href = url;
}
```

The `priceId` comes from your Stripe Dashboard > Products > Create Product > Copy the price ID (starts with `price_`).

## Paywall Strategies That Actually Convert

### Strategy 1: Freemium with Feature Gating

Free users get 3 habits. Paid users get unlimited.

```javascript
const MAX_FREE_HABITS = 3;
const isPaid = localStorage.getItem('paid_status') === 'true';

function canAddHabit() {
  const habits = getHabits();
  if (habits.length >= MAX_FREE_HABITS && !isPaid) {
    showUpgradeModal();
    return false;
  }
  return true;
}
```

The upgrade modal should show:
- What they get (unlimited habits, data export, custom colors)
- Social proof ("Join 200+ users building better habits")
- Price anchoring ("Less than a coffee per month")
- A clear CTA button that triggers `startCheckout()`

### Strategy 2: Free Trial with Time Limit

Full access for 7 days. Then paywall.

```javascript
function checkTrialStatus() {
  const installDate = localStorage.getItem('install_date');
  if (!installDate) {
    localStorage.setItem('install_date', Date.now().toString());
    return 'active';
  }

  const daysSinceInstall = (Date.now() - parseInt(installDate)) / (1000 * 60 * 60 * 24);
  const isPaid = localStorage.getItem('paid_status') === 'true';

  if (daysSinceInstall > 7 && !isPaid) {
    return 'expired';
  }
  return 'active';
}
```

When the trial expires, don't lock them out completely. Let them see their data but not add new entries. Loss aversion is your best conversion tool — they've already built streaks, they don't want to lose them.

### Strategy 3: One-Time Purchase (Lifetime Access)

Best for tools that don't have recurring costs. Charge $15-50 once.

This is the simplest model. No subscription management, no churn tracking, no dunning emails. User pays once, gets full access forever.

Store the purchase status after successful checkout:

```javascript
// On your success page
const urlParams = new URLSearchParams(window.location.search);
const sessionId = urlParams.get('session_id');

if (sessionId) {
  // Verify with your serverless function
  const response = await fetch(`/.netlify/functions/verify-payment?session_id=${sessionId}`);
  const { paid } = await response.json();

  if (paid) {
    localStorage.setItem('paid_status', 'true');
    localStorage.setItem('purchase_date', Date.now().toString());
  }
}
```

The verification function:

```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async (event) => {
  const { session_id } = event.queryStringParameters;

  const session = await stripe.checkout.sessions.retrieve(session_id);

  return {
    statusCode: 200,
    body: JSON.stringify({ paid: session.payment_status === 'paid' }),
  };
};
```

## Pricing: What to Actually Charge

For PWAs and simple tools:

| Model | Price Point | Works When |
|-------|-------------|------------|
| One-time | $9 - $29 | Tool solves a one-time problem or has no server costs |
| Monthly | $3 - $9/month | Tool provides ongoing value (tracking, analytics, daily use) |
| Annual | $29 - $79/year | Offer 2 months free vs monthly to incentivize annual |
| Lifetime | $29 - $99 | You want cash upfront and don't want to manage subscriptions |

Rules:
- Never price below $5 for a one-time purchase. You'll attract complainers and refund requests.
- Always offer annual pricing alongside monthly. 30-40% of users will choose annual.
- Test pricing. Start at $9/month. If conversion rate is above 5%, raise to $12. Keep raising until conversion drops below 2%.

## Handling Payments Without a Database

For simple apps, you don't need a database to track who's paid. Here's the pattern:

1. User pays via Stripe Checkout
2. Stripe redirects to your success page with a session ID
3. Your serverless function verifies the session with Stripe
4. You set `paid_status` in localStorage

**The weakness:** Users can clear localStorage and lose their purchase status. Two solutions:

**Solution A: Stripe Customer Portal.** Let users manage their own subscription and re-verify their status:

```javascript
// Link to Stripe's hosted customer portal
const portalSession = await stripe.billingPortal.sessions.create({
  customer: customerId,
  return_url: 'https://myapp.com/settings',
});
```

**Solution B: License keys.** After purchase, generate a unique key, email it to the user, and store it in localStorage. If they clear storage, they re-enter the key. Use a serverless function to validate keys against a simple JSON file or KV store.

**Solution C: Supabase (when you're ready for a database).** Supabase gives you a Postgres database + auth for free (up to 50K monthly active users). When your app grows past localStorage, this is the next step.

## Revenue Tracking

Don't rely on Stripe's dashboard alone. Create a simple revenue tracking system:

```javascript
// In your admin/settings
async function getRevenue() {
  const response = await fetch('/.netlify/functions/revenue-stats');
  const { mrr, totalCustomers, churnRate } = await response.json();

  document.getElementById('mrr').textContent = `$${mrr}`;
  document.getElementById('customers').textContent = totalCustomers;
  document.getElementById('churn').textContent = `${churnRate}%`;
}
```

The metrics that matter:
- **MRR** (Monthly Recurring Revenue): How much you make per month from subscriptions
- **Churn rate**: What percentage of subscribers cancel per month (below 5% is good, below 3% is great)
- **LTV** (Lifetime Value): Average revenue per customer over their lifetime. If LTV > $50, you can afford to spend on acquisition.
- **Conversion rate**: Free users who become paid users. 2-5% is normal. Above 5% means you should raise prices.

## Stripe Test Mode

Before going live, test everything in Stripe's test mode. Use these test card numbers:

- `4242 4242 4242 4242` — successful payment
- `4000 0000 0000 0002` — declined card
- `4000 0000 0000 3220` — requires 3D Secure

Any future expiry date and any 3-digit CVC will work.

Toggle between test and live mode by switching your API keys. Test keys start with `sk_test_`, live keys start with `sk_live_`.

Go live only after you've tested: successful payment, failed payment, subscription cancellation, and the paywall correctly gating features.

Next module: Building a portfolio of 10+ apps and knowing which ones to kill, which ones to double down on.
