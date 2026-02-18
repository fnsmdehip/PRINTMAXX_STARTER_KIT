# Affiliate Program Setup Guide

Complete technical and operational setup for running your own affiliate program.

---

## Platform options

### Budget tier (free to $50/mo)

| Platform | Cost | Best for | Pros | Cons |
|----------|------|----------|------|------|
| **Rewardful** | Free-$29/mo | Stripe users | Direct Stripe integration, simple setup | Limited features on free tier |
| **FirstPromoter** | $49/mo | SaaS apps | Good dashboard, Stripe/Paddle support | Minimum $49/mo |
| **Custom (manual)** | Free | <20 affiliates | Full control, no fees | Time-intensive, error-prone |

### Growth tier ($50-200/mo)

| Platform | Cost | Best for | Pros | Cons |
|----------|------|----------|------|------|
| **Tapfiliate** | $89/mo | Multi-product | Flexible commission rules, good API | Setup complexity |
| **Refersion** | $99/mo | E-commerce | Shopify integration, influencer tools | Higher minimums |
| **LeadDyno** | $49/mo | Simple programs | Easy setup, email integrations | Limited advanced features |

### Scale tier ($200+/mo)

| Platform | Cost | Best for | Pros | Cons |
|----------|------|----------|------|------|
| **PartnerStack** | Custom | B2B SaaS | Full partner management, marketplace | Enterprise pricing |
| **Impact** | Custom | Large programs | Industry standard, fraud protection | Complex, expensive |
| **CJ Affiliate** | Custom | High volume | Huge affiliate network | High fees, slow approval |

### Recommendation by stage

**Pre-revenue to $5k MRR:** Rewardful free tier + PayPal manual payouts
**$5k-20k MRR:** Rewardful paid or FirstPromoter
**$20k+ MRR:** Tapfiliate or PartnerStack

---

## Commission structures

### One-time commission

Best for: Lifetime deals, high-priced products, physical goods

```
Example: 20% of first payment

Customer pays $99 → Affiliate earns $19.80
Customer pays $49 → Affiliate earns $9.80
```

Pros: Simple, predictable costs
Cons: Less incentive for affiliates long-term

### Recurring commission

Best for: Subscriptions, SaaS, membership products

```
Example: 20% recurring for 12 months

Customer pays $9.99/mo → Affiliate earns $2/mo for 12 months
Total potential: $24 per customer
```

Pros: Affiliates motivated to promote quality
Cons: Higher total payout, accounting complexity

### Tiered commission

Best for: Incentivizing volume

```
Tier 1 (0-9 sales/mo): 20%
Tier 2 (10-49 sales/mo): 25%
Tier 3 (50+ sales/mo): 30%
```

Pros: Rewards top performers
Cons: Complexity, potential disputes

### Hybrid commission

Best for: Balancing acquisition and retention

```
First payment: 30%
Months 2-12: 15%
Month 13+: 10%
```

Pros: Incentivizes both acquisition and quality referrals
Cons: Tracking complexity

### Our recommended structure

For apps with $9.99/mo subscription:

| Tier | Sales/month | First payment | Recurring (12 mo) | Max per customer |
|------|-------------|---------------|-------------------|------------------|
| Starter | 0-9 | 20% ($2) | 10% ($1/mo) | $14 |
| Pro | 10-49 | 25% ($2.50) | 12% ($1.20/mo) | $16.90 |
| Elite | 50+ | 30% ($3) | 15% ($1.50/mo) | $21 |

---

## Cookie duration

Cookie = how long after clicking affiliate link the referral counts

### Standard durations

| Duration | Use case | Example |
|----------|----------|---------|
| **24 hours** | Impulse purchases | Amazon |
| **30 days** | Standard SaaS | Most programs |
| **60 days** | Considered purchases | B2B software |
| **90 days** | Long sales cycles | Enterprise, courses |
| **Lifetime** | First-touch attribution | High-trust affiliates |

### Recommended: 30-day cookie with 90-day attribution window

```
First click: Cookie set for 30 days
If customer returns within 30 days: Cookie refreshes
If customer purchases within 90 days of any click: Affiliate credited
```

Why 30/90 split:
- 30 days prevents affiliate squatting
- 90 days captures delayed conversions
- Balances affiliate fairness with business protection

### Technical implementation

**Rewardful (recommended):**
```javascript
// Add to your site
<script>(function(w,r){w._rwq=r;w[r]=w[r]||function(){(w[r].q=w[r].q||[]).push(arguments)}})(window,'rewardful');</script>
<script async src='https://r.wdfl.co/rw.js' data-rewardful='YOUR_API_KEY'></script>
```

**Cookie structure:**
```javascript
{
  "affiliate_id": "aff_12345",
  "first_click": "2026-01-15T10:30:00Z",
  "last_click": "2026-01-21T14:22:00Z",
  "source": "tiktok",
  "campaign": "winter_launch"
}
```

---

## Payment terms

### Payment schedule

| Frequency | Best for | Pros | Cons |
|-----------|----------|------|------|
| Weekly | Top performers | High affiliate satisfaction | Admin overhead |
| Bi-weekly | Growth stage | Balance of speed and efficiency | Moderate overhead |
| Monthly | Standard | Simple, aligns with billing | Affiliates wait longer |

Recommended: Monthly for all, weekly for Elite tier

### Payment thresholds

```
Starter tier: $25 minimum payout
Pro tier: $10 minimum payout
Elite tier: No minimum
```

Why thresholds:
- Reduces payment processing costs
- Prevents micro-payouts
- Keeps affiliates engaged (working toward threshold)

### Payment methods

| Method | Fees | Speed | Best for |
|--------|------|-------|----------|
| PayPal | 2.9% + $0.30 | Instant | US affiliates |
| Wise | 0.5-1% | 1-2 days | International |
| Bank transfer | $25-50 | 3-5 days | High-value payouts |
| Payoneer | 2% | 2 days | International creators |

Recommended stack:
- PayPal for US affiliates (most common)
- Wise for international (lowest fees)
- Bank transfer for $500+ monthly earnings

### Clawback policy

When customers refund, handle commission:

**Option A: Full clawback (strict)**
```
Customer refunds within 30 days → Full commission returned
Customer refunds after 30 days → Commission kept
```

**Option B: Partial clawback (balanced)**
```
Refund within 7 days → 100% clawback
Refund 8-30 days → 50% clawback
Refund after 30 days → No clawback
```

**Option C: Rolling reserve (advanced)**
```
Hold 20% of commissions in reserve
Release after 60 days if no chargebacks
```

Recommended: Option B for balance of fairness and protection

---

## Tracking setup

### Attribution model

**Last-click attribution** (recommended for simplicity):
- Credit goes to last affiliate link clicked before purchase
- Simple to understand and implement
- Industry standard

**First-click attribution**:
- Credit goes to first affiliate who referred the customer
- Good for content creators who drive awareness
- Harder to implement

**Multi-touch attribution** (advanced):
- Split credit among multiple affiliates
- Most accurate but complex
- Requires advanced tracking

### Tracking parameters

Standard URL structure:
```
https://yourapp.com/?ref=AFFILIATE_CODE
https://yourapp.com/?via=AFFILIATE_CODE
https://yourapp.com/r/AFFILIATE_CODE
```

Recommended parameters to track:
```
ref=AFFILIATE_CODE        (required)
source=tiktok             (platform they posted on)
campaign=winter_launch    (your campaign name)
content=video_1           (specific piece of content)
```

Full tracked URL:
```
https://yourapp.com/?ref=sarah_fit&source=tiktok&campaign=launch&content=tutorial_1
```

### Tracking implementation

**Rewardful setup:**

1. Create account at rewardful.com
2. Connect Stripe account
3. Install tracking script
4. Configure commission rules
5. Create affiliate portal link

**Manual tracking (spreadsheet backup):**

Track these fields:
```
timestamp, affiliate_id, customer_email, plan, amount, commission, source, content_url
```

Weekly reconciliation:
- Export Stripe payments
- Match to affiliate clicks
- Calculate commissions
- Update tracking sheet

### Fraud prevention

**Red flags:**
- Multiple signups from same IP
- Immediate cancellations after trial
- Credit card declines after signup
- Self-referrals
- Abnormal conversion rates (>50%)

**Prevention measures:**
- IP tracking and limits (max 5 signups per IP)
- Email domain restrictions (no temp emails)
- 7-day hold before commission locked
- Manual review for high-volume affiliates
- Chargebacks trigger automatic review

---

## Legal requirements

### Affiliate agreement essentials

Required clauses:
1. FTC disclosure requirement
2. Prohibited marketing practices
3. Commission structure and payment terms
4. Termination conditions
5. IP usage rights
6. Liability limitations

**Template location:** `/affiliate_onboarding/affiliate_agreement_template.md`

### FTC compliance

We require all affiliates to:
- Disclose affiliate relationship clearly
- Not make unsubstantiated claims
- Not use fake testimonials
- Follow platform-specific guidelines

Our documentation for compliance:
- Agreement signed with timestamp
- Disclosure policy sent via email
- Periodic compliance reminders
- Content review process

### Tax requirements

**US affiliates:**
- Collect W-9 for payments >$600/year
- Issue 1099-NEC by January 31
- Track all payments for reporting

**International affiliates:**
- Collect W-8BEN form
- No withholding if tax treaty applies
- Document country of residence

---

## Quick setup checklist

### Week 1: Foundation

- [ ] Choose tracking platform (Rewardful recommended)
- [ ] Set up Stripe/payment integration
- [ ] Define commission structure
- [ ] Create affiliate agreement
- [ ] Build affiliate signup page

### Week 2: Assets and onboarding

- [ ] Create swipe files (email, social, video)
- [ ] Build affiliate dashboard
- [ ] Write onboarding email sequence
- [ ] Create FAQ document
- [ ] Set up payment method (PayPal business)

### Week 3: Launch

- [ ] Recruit first 10 affiliates (personal outreach)
- [ ] Test full tracking flow
- [ ] Process first test payout
- [ ] Gather feedback and iterate
- [ ] Document process for scale

---

## Cost projections

### Bootstrap budget ($0-50/mo)

```
Rewardful free tier: $0
PayPal fees: 2.9% of payouts
Total monthly: ~$50 at $1k affiliate revenue
```

### Growth budget ($100-300/mo)

```
Rewardful paid: $29-49/mo
PayPal fees: 2.9% of payouts
Email tools: $20-50/mo
Total monthly: ~$200 at $5k affiliate revenue
```

### Scale budget ($500+/mo)

```
PartnerStack or Impact: $200-500/mo
Wise for international: 1% of payouts
Automation tools: $100/mo
Total monthly: ~$500 at $20k affiliate revenue
```

---

## Resources

- Rewardful docs: docs.rewardful.com
- FTC Endorsement Guides: ftc.gov/endorsement-guides
- AFFILIATE_SOURCES_MASTER.md (programs to join ourselves)
- RECRUITMENT_PLAYBOOK.md (finding affiliates)

---

Created: 2026-01-21
