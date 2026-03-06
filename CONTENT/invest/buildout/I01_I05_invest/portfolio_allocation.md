# Portfolio Allocation Framework — I05

## Core Philosophy

diversification is for people who don't know what they're doing. concentration is for conviction.
but conviction without risk management = ruin.

the framework: Kelly Criterion to size positions, hard stop rules to protect the downside.

---

## Kelly Criterion Applied

**Full Kelly formula:**
```
f* = (bp - q) / b

where:
  b = net odds received (win amount / loss amount)
  p = probability of winning
  q = 1 - p (probability of losing)
  f* = fraction of capital to risk
```

**Worked example:**
- Stock setup: 60% chance of 30% gain, 40% chance of 20% loss
- b = 0.30 / 0.20 = 1.5
- p = 0.60, q = 0.40
- f* = (1.5 × 0.60 - 0.40) / 1.5 = (0.90 - 0.40) / 1.5 = 0.50 / 1.5 = **33%**

**But never use full Kelly.** Use half-Kelly or quarter-Kelly:
- Full Kelly: mathematically optimal but devastating drawdowns
- Half Kelly (16.5%): smoother equity curve, ~75% of full Kelly returns
- Quarter Kelly (8.25%): conservative, recommended for most situations

**Practical rule:** if you're not 100% certain of your edge, use 25% Kelly or less.

---

## Asset Class Allocation

### Baseline Portfolio (Solopreneur with $10K-50K liquid)

This assumes primary income from business ops, portfolio is reserve + growth.

| Asset Class | Allocation | Purpose | Instruments |
|-------------|-----------|---------|-------------|
| Emergency reserve | 20% | 6-month runway, liquid | HYSA at 4.5%+ (Marcus, Ally) |
| Index funds (passive) | 30% | long-term compound | VTI, QQQ, VOO |
| Business reinvestment | 25% | highest IRR, what we know | ads, tools, content |
| Active speculation | 15% | asymmetric upside | individual stocks, crypto |
| Alts (domains, accounts) | 10% | non-correlated returns | domain flipping, account flips |

**Total: 100%**

### When Revenue Hits $5K+/Mo

| Asset Class | Allocation | Change |
|-------------|-----------|--------|
| Emergency reserve | 15% | reduced (stable income) |
| Index funds | 35% | increased |
| Business reinvestment | 20% | optimized |
| Active speculation | 20% | increased |
| Alts | 10% | maintained |

### When Revenue Hits $20K+/Mo

| Asset Class | Allocation | Change |
|-------------|-----------|--------|
| Emergency reserve | 10% | lower threshold |
| Index funds | 40% | majority to passive |
| Business reinvestment | 15% | selective only |
| Active speculation | 25% | meaningful position |
| Real estate / private | 10% | add this tier |

---

## Position Sizing Rules

### Individual Stock Positions

**For concentrated bets (you've done the work):**

| Conviction Level | Max Position | Exit Rule |
|----------------|-------------|-----------|
| High (deep research) | 10-15% of speculative bucket | -20% stop, scale out at +30% |
| Medium (moderate research) | 5-8% | -15% stop, scale out at +20% |
| Low (thesis not fully formed) | 2-3% | -10% stop, reassess at +15% |

**Hard rules:**
- Never more than 20% in any single position
- Never hold a losing position hoping — set stops before entry
- Scale in (3 tranches) not all-in at once
- Review every position monthly, exit if thesis changes

### Crypto Allocation

**For someone building a business (not a crypto trader):**

| Total Portfolio | Max Crypto | Breakdown |
|----------------|-----------|-----------|
| < $25K | 5-10% | BTC 60%, ETH 30%, speculation 10% |
| $25K-$100K | 10-15% | BTC 50%, ETH 30%, alt 15%, meme 5% |
| $100K+ | 10% (hard cap) | BTC 40%, ETH 30%, alts 20%, meme 10% |

**Core crypto holdings (low volatility relative to alts):**
- Bitcoin (BTC): digital gold narrative. hold 3-5 years.
- Ethereum (ETH): smart contract platform. hold 2-3 years.

**Never:**
- More than 5% of total net worth in memecoins
- Leveraged crypto positions (liquidation risk is real)
- Loans against crypto positions (saw too many wrecked in 2022)

---

## Rebalancing Protocol

### When to Rebalance

**Triggered rebalancing (better than calendar-based):**

1. Any asset class drifts more than 10% from target → rebalance within 30 days
2. Single position exceeds 20% of its bucket → trim to 15%
3. Emergency reserve drops below 3-month runway → replenish before investing
4. Business revenue drops 30%+ for 2+ months → increase reserve, cut speculation

**Calendar rebalancing (backup):**
- Review allocation every 6 months regardless of triggers
- Tax-aware: sell losers in December, take gains strategically

### Rebalancing Math Example

Starting allocation: $20,000 total
- Emergency: $4,000 (20%)
- Index funds: $6,000 (30%)
- Business: $5,000 (25%)
- Speculation: $3,000 (15%)
- Alts: $2,000 (10%)

After 6 months, index funds grew 18%, speculation grew 35%:
- Emergency: $4,000 (stays)
- Index funds: $7,080 → target $6,540 → trim $540
- Speculation: $4,050 → target $3,270 → trim $780
- Trim total: $1,320 → add to business reinvestment or alts

---

## Risk Management Rules

### The Hard Stops

These are not suggestions. pre-set these before any position.

**Individual positions:**
- Stop loss: -15% on high conviction, -10% on low conviction
- Scale out: sell 50% at +30%, let rest run with trailing stop
- Maximum hold time with no thesis progress: 6 months → reassess or exit

**Portfolio level:**
- Maximum portfolio drawdown before halting new positions: -20%
- At -20%: stop all new speculation, review all positions, wait 30 days
- At -30%: halt everything, shift 100% to cash + HYSA, investigate thesis

**Business correlation risk:**
If business revenue drops AND portfolio drops at same time:
- Raise 6 months cash immediately (even if selling at a loss)
- Your ability to weather the storm > optimizing returns

### Sequence-of-Returns Risk

Most relevant when near a major life expense (starting a company, buying equipment, etc.):

- Timeline < 6 months: 100% cash/HYSA, no speculation
- Timeline 6-18 months: max 30% in anything volatile
- Timeline 18+ months: normal allocation

---

## Tax Optimization

**Always think after-tax returns.**

**Short-term gains (< 1 year held):** taxed as ordinary income (22-37%)
**Long-term gains (> 1 year held):** taxed at 0/15/20% depending on income

**Practical rules:**
1. Hold winning positions for 12+ months whenever possible (saves 17-37% on gains)
2. Harvest losses in December to offset gains
3. Max out tax-advantaged accounts first: Roth IRA ($7K/yr 2024), Solo 401K ($69K/yr if self-employed)
4. Speculative plays = short-term bucket (accept higher tax, higher risk/reward)
5. Index funds = long-term bucket (compound tax-efficiently)

**Roth IRA strategy for solopreneurs:**
- Put speculative bets inside Roth IRA
- If they 10x, that's tax-free growth forever
- If they go to zero, you lose the contribution but not additional tax
- Backdoor Roth if income > $161K/yr (2024 limit)

---

## Business vs Investment IRR Comparison

Every dollar you invest externally competes with reinvesting in the business.

**Typical returns by category:**

| Category | Expected Annual Return | Risk | Liquidity |
|----------|----------------------|------|-----------|
| HYSA (4.5%) | 4.5% | very low | high |
| Index funds (VTI) | 8-10% historical | medium | high |
| Paid ads (positive ROI campaigns) | 50-300%+ | medium | medium |
| Cold email outbound | 200-500% ROI | low | medium |
| Algo trading (proven) | 10-20% | medium | high |
| Domain flipping | 50-200% on deployed capital | medium | low |
| Memecoin speculation | -100% to +10,000% | very high | high |

**Decision rule:** if a business investment has > 50% expected ROI, it beats every market option. prioritize business first until marginal ROI drops below 20%.

---

## Monthly Financial Review (30 min)

**Run this every 1st of month:**

1. Check total portfolio value vs last month → track equity curve
2. Verify allocation % → trigger rebalance if needed
3. Review all stop losses → adjust for trailing stops on winners
4. Calculate runway (cash + monthly burn rate)
5. Tax-lot tracking → any positions crossing 12-month threshold this month?
6. Business revenue vs. projection → is thesis still valid?
7. One question: "what's the biggest risk to my financial position right now?"

**Tracking spreadsheet columns:**
```
Date | Asset | Type | Market Value | Allocation % | Target % | Drift | Action Needed
```

---

## The 90-Day Bootstrap Allocation

Starting from zero with business income just starting:

**Month 1-3 ($0-$2K liquid):**
- 100% emergency reserve in HYSA
- 0% speculation
- All income → business tools and growth

**Month 4-6 ($2K-$5K liquid):**
- 80% emergency reserve
- 20% index funds (start dollar-cost averaging)
- 0% speculation (not yet)

**Month 7-12 ($5K-$15K liquid):**
- 30% emergency reserve (3 months covered)
- 40% index funds
- 15% business reinvestment
- 15% start speculation (small, $500-1K only)

**Month 13+ ($15K+ liquid):**
- Apply full allocation framework above
- Review and set formal investment policy statement (IPS)
