# SaaS Products Unit Economics

## MRR Projections (Solopreneur SaaS)

### Month 1-12 Growth Model

**Conservative Scenario (Organic only, no prior audience)**

| Month | New Customers | Churned | Active | MRR | Notes |
|-------|---------------|---------|--------|-----|-------|
| 1 | 5 | 0 | 5 | $145 | Launch to small list |
| 2 | 8 | 1 | 12 | $348 | Word of mouth |
| 3 | 12 | 1 | 23 | $667 | SEO starting |
| 4 | 15 | 2 | 36 | $1,044 | First $1K MRR |
| 5 | 18 | 3 | 51 | $1,479 | |
| 6 | 22 | 4 | 69 | $2,001 | $2K milestone |
| 7 | 25 | 5 | 89 | $2,581 | |
| 8 | 28 | 6 | 111 | $3,219 | |
| 9 | 32 | 8 | 135 | $3,915 | |
| 10 | 35 | 9 | 161 | $4,669 | |
| 11 | 38 | 11 | 188 | $5,452 | |
| 12 | 42 | 13 | 217 | $6,293 | $6K+ MRR |

**Assumptions:**
- Price: $29/mo
- Churn: 7% monthly
- Organic growth only
- Starting with ~500 email list

### Optimistic Scenario (Product-led growth, viral mechanics)

| Month | New Customers | Churned | Active | MRR |
|-------|---------------|---------|--------|-----|
| 1 | 20 | 0 | 20 | $580 |
| 2 | 35 | 1 | 54 | $1,566 |
| 3 | 50 | 3 | 101 | $2,929 |
| 4 | 70 | 5 | 166 | $4,814 |
| 5 | 90 | 8 | 248 | $7,192 |
| 6 | 110 | 12 | 346 | $10,034 |

**Requires:** Strong product-market fit, viral loop, existing audience

---

## Pricing Analysis

### Common SaaS Price Points

| Tier | Price | Best For | Conv Rate |
|------|-------|----------|-----------|
| Hobby | $9-19/mo | Side projects, testing | 3-5% |
| Starter | $29-49/mo | Small business, freelancers | 2-3% |
| Pro | $79-149/mo | Growing businesses | 1-2% |
| Business | $199-499/mo | Teams, agencies | 0.5-1% |

### Solopreneur Sweet Spots

**$29/mo** - Most common for solopreneur SaaS
- Low friction
- Impulse subscription range
- $348/yr feels reasonable
- Easy to justify ROI

**$49/mo** - Premium positioning
- Higher quality expectation
- Better customers (less support)
- Faster path to $10K MRR
- Need stronger value prop

**$99/mo** - Prosumer/SMB
- Requires more features
- Sales conversations likely
- Higher LTV but harder acquisition

---

## Churn Rate Analysis

### Industry Benchmarks

| Churn Rate | Rating | What It Means |
|------------|--------|---------------|
| >10%/mo | Critical | Product problem or wrong market |
| 7-10%/mo | Poor | Need to improve onboarding |
| 5-7%/mo | Average | Typical for solopreneur SaaS |
| 3-5%/mo | Good | Strong product-market fit |
| <3%/mo | Excellent | Category leader status |

### Churn Impact on Revenue

**Starting with 100 customers at $29/mo:**

| Monthly Churn | Year 1 Revenue | Remaining Customers |
|---------------|----------------|---------------------|
| 3% | $28,800 | 69 |
| 5% | $26,400 | 54 |
| 7% | $24,200 | 42 |
| 10% | $21,500 | 28 |

**Key insight:** Reducing churn from 7% to 5% adds $2,200/year per 100 starting customers

### Churn Reduction Strategies

| Strategy | Impact | Cost |
|----------|--------|------|
| Onboarding emails | -1-2% churn | Time only |
| In-app guidance | -1-2% churn | Dev time |
| Annual discount | -2-3% churn | 15-20% discount |
| Customer success calls | -2-4% churn | Time intensive |

---

## CAC Payback Period

### Formula

```
CAC Payback = CAC / (ARPU x Gross Margin)

Example:
- CAC: $100
- ARPU: $29/mo
- Gross Margin: 80%

Payback = $100 / ($29 x 0.80) = 4.3 months
```

### Benchmarks

| Payback Period | Rating | Action |
|----------------|--------|--------|
| <3 months | Excellent | Scale aggressively |
| 3-6 months | Good | Scale carefully |
| 6-12 months | Acceptable | Optimize CAC |
| >12 months | Poor | Fix unit economics first |

### CAC by Channel for SaaS

| Channel | Typical CAC | Payback (at $29/mo) |
|---------|-------------|---------------------|
| Organic SEO | $20-50 | 1-2 months |
| Content marketing | $30-80 | 1-3 months |
| Paid social | $80-200 | 3-9 months |
| Google Ads | $100-300 | 4-13 months |
| Cold email | $50-150 | 2-6 months |

---

## LTV:CAC Ratio

### Formula

```
LTV = ARPU x Gross Margin / Monthly Churn Rate

Example:
- ARPU: $29
- Gross margin: 80%
- Churn: 5%

LTV = $29 x 0.80 / 0.05 = $464
```

### Target Ratios

| LTV:CAC | Rating | Meaning |
|---------|--------|---------|
| <1:1 | Failing | Losing money on every customer |
| 1:1-2:1 | Poor | Barely sustainable |
| 3:1 | Target | Healthy SaaS economics |
| 4:1+ | Excellent | Can invest more in growth |
| >5:1 | Consider | May be underinvesting in growth |

### Example Scenarios

| ARPU | Churn | LTV | Max CAC (3:1) |
|------|-------|-----|---------------|
| $29 | 5% | $464 | $155 |
| $29 | 7% | $331 | $110 |
| $49 | 5% | $784 | $261 |
| $49 | 7% | $560 | $187 |
| $99 | 5% | $1,584 | $528 |

---

## Infrastructure Costs

### Solopreneur SaaS Stack (Bootstrap Phase)

| Item | Cost/Month | Notes |
|------|------------|-------|
| Vercel (hosting) | $0-20 | Free tier works to ~100K requests |
| Database (Supabase) | $0-25 | Free tier works to 500MB |
| Auth (Clerk/Auth0) | $0-25 | Free tier works to 5K users |
| Email (Resend) | $0-20 | Free tier: 3K emails/mo |
| Analytics (Plausible) | $9 | Privacy-focused |
| Error tracking (Sentry) | $0-26 | Free tier adequate |
| **Total** | $9-146 | |

### Growth Phase ($5K+ MRR)

| Item | Cost/Month | Notes |
|------|------------|-------|
| Vercel Pro | $20 | More bandwidth |
| Database Pro | $25-50 | More storage, backups |
| Auth paid tier | $25-50 | More users |
| Email scaling | $20-100 | Transactional + marketing |
| Monitoring | $50-100 | Better observability |
| Support tools | $50-100 | Help desk, docs |
| **Total** | $190-420 | |

### Gross Margin Calculation

```
Gross Margin = (Revenue - COGS) / Revenue

At $5K MRR with $300 infrastructure:
Gross Margin = ($5,000 - $300) / $5,000 = 94%

Target: >80% gross margin for SaaS
```

---

## Key Metrics to Track

### Weekly

- New signups
- Trial-to-paid conversion
- Active users / Total users
- Feature usage

### Monthly

- MRR
- Net MRR growth (new - churn - downgrades + upgrades)
- Churn rate
- CAC by channel
- LTV:CAC ratio

### Quarterly

- Gross margin trend
- Payback period trend
- Customer segments analysis
- Pricing effectiveness

---

## Break-Even Analysis

### Fixed Costs Assumption

| Item | Monthly |
|------|---------|
| Infrastructure | $100 |
| Tools | $50 |
| Domain/misc | $20 |
| **Total Fixed** | $170 |

### Break-Even Customers

```
Break-Even = Fixed Costs / (ARPU x Gross Margin)

At $29/mo, 80% margin:
Break-Even = $170 / ($29 x 0.80) = 8 customers
```

**You need 8 paying customers to cover costs.**

### Path to $10K MRR

| Price Point | Customers Needed | Time (Conservative) |
|-------------|------------------|---------------------|
| $29/mo | 345 | 12-18 months |
| $49/mo | 205 | 10-14 months |
| $99/mo | 102 | 8-12 months |

---

## Action Items

1. **Price at $29/mo minimum** - $9-19 rarely works for solopreneurs
2. **Target <7% monthly churn** - Invest in onboarding
3. **Keep infra under $200/mo** - Until $5K MRR
4. **Offer annual at 2 months free** - Reduces churn, improves cash flow
5. **Track LTV:CAC weekly** - Your north star metric
