# Prediction Market Arbitrage Playbook

**OP_ID:** I06 (proposed)
**Revenue Range:** $500-$50K/mo (high variance)
**Automation Level:** Medium-High (scanner automated, execution manual)
**Phase:** 2 (requires capital + knowledge)
**Risk Level:** HIGH (speculative, variance)
**Status:** NEW

---

## What This Is

Exploit pricing inefficiencies between prediction markets (Polymarket, Kalshi, PredictIt, Metaculus, Manifold) and between prediction markets and real-world probability estimates.

three types of edge:
1. **Cross-platform arbitrage** - same event, different prices across platforms. buy low, sell high.
2. **Information edge** - you know something the market hasn't priced in yet. news scraping + fast execution.
3. **Market making** - provide liquidity on wide spreads. collect the bid-ask spread.

the edge: Claude Code can build scrapers that monitor prices across all platforms simultaneously. when spreads exceed threshold, alert instantly. most participants are manual traders checking one platform at a time.

---

## Market Reality (2026)

- Polymarket: $3B+ total volume in 2025. Peaked at $450M/month during US elections.
- Kalshi: CFTC-regulated, approved for event contracts. Growing fast. US-legal.
- PredictIt: Capped at $850/contract. Being wound down but still active.
- Manifold Markets: Play-money but real signal value for calibration.
- Total prediction market volume globally: estimated $8B+ in 2025.

**Key facts:**
- Polymarket is crypto-based (USDC on Polygon). Non-US residents can trade directly. US = grey area.
- Kalshi is the only CFTC-regulated prediction market. US-legal. KYC required.
- Cross-platform spreads of 3-8% exist regularly on identical events.
- During breaking news, spreads can hit 15-25% for minutes before markets sync.

**Regulatory note:** Prediction markets are evolving legally. Kalshi is regulated. Polymarket operates from outside US. Always check current legal status in your jurisdiction before trading.

---

## Revenue Model

### Strategy 1: Cross-Platform Arbitrage ($200-$5K/mo)
- Monitor same events across Polymarket, Kalshi, PredictIt
- When spread exceeds 4% (after fees): buy YES on cheap platform, buy NO on expensive platform
- Guaranteed profit regardless of outcome
- **Edge requirement:** Speed. Spreads close in minutes.
- **Capital needed:** $500-$5K per position

### Strategy 2: News-Based Trading ($500-$20K/mo)
- Monitor breaking news faster than the market
- Claude Code scraper monitors 50+ news sources. when relevant event detected, check if prediction market has adjusted.
- **Edge requirement:** Information speed + interpretation quality
- **Capital needed:** $1K-$10K per position

### Strategy 3: Market Making ($300-$10K/mo)
- Provide liquidity on markets with wide bid-ask spreads
- Post limit orders on both sides, collect the spread
- **Edge requirement:** Capital efficiency + patience
- **Capital needed:** $2K-$20K deployed

### Strategy 4: Calendar Arbitrage ($200-$2K/mo)
- Events with known resolution dates
- Calculate time-value and probability gaps vs market price
- **Edge requirement:** Better probabilistic reasoning than crowd

### Strategy 5: Educational Content ($500-$3K/mo passive)
- Document strategies, sell course/newsletter
- **No capital needed. Low risk.**

---

## Platform Comparison

| Platform | Real Money | Fees | Limits | KYC | Settlement |
|----------|-----------|------|--------|-----|-----------|
| **Kalshi** | Yes | 1-7% | No cap (event-dependent) | Yes (US) | USD wire/ACH |
| **Polymarket** | Yes (crypto) | 0% (gas fees only) | No cap | Yes | USDC on Polygon |
| **PredictIt** | Yes | 5% profit + 10% withdrawal | $850/contract | Yes (US) | USD |
| **Manifold** | No (play money) | 0% | No cap | No | Mana (play currency) |

---

## The Arbitrage Scanner (Build This)

### Architecture
```
NEWS MONITOR (50+ sources)
    |
    v
EVENT MATCHER (maps events to markets)
    |
    v
PRICE SCRAPER (all platforms, every 60 seconds)
    |
    v
SPREAD CALCULATOR (accounting for fees)
    |
    v
ALERT ENGINE (Slack/email/SMS when spread > threshold)
    |
    v
EXECUTION TRACKER (log trades, P&L, resolution)
```

### Data Sources for News Edge
- Twitter API (breaking news accounts)
- Associated Press API, Reuters API
- Government press releases (whitehouse.gov, sec.gov, fda.gov)
- Google News Alerts
- Reddit (r/polymarket, r/kalshi for sentiment)
- Discord servers (prediction market communities)

---

## Setup (Week 1-2)

### Day 1-2: Platform Setup
```
1. Create Kalshi account: kalshi.com (KYC, deposit $500-$1,000)
2. Create Polymarket account: polymarket.com (MetaMask wallet, USDC on Polygon)
3. Create Manifold account: manifold.markets (paper trading)
```

### Day 3-5: Build Scanner
```
1. Build price scraper for Polymarket public API
2. Build price scraper for Kalshi public API
3. Create event matching system (manual mapping, then Claude NLP auto-match)
4. Build spread calculator accounting for fees
5. Set up alerting (Slack webhook or email via n8n)
```

### Day 6-7: Paper Trade
```
1. Paper trade for 1 week minimum
2. Validate that spreads are real and executable (not phantom liquidity)
3. Calculate actual expected return after fees, slippage, timing
```

### Week 2: Live Trading
```
1. Start small: $50-$100 per position
2. Target only cross-platform arbs with >8% spread (after fees)
3. Log every trade in LEDGER/PREDICTION_MARKET_TRADES.csv
4. Review after 20 trades
```

---

## Risk Management (Critical)

### Position Sizing
- Never more than 10% of total capital in single event
- Never more than 30% in correlated events
- Keep 30% cash reserve
- Start with 1% of target position size while learning

### Risk Limits
- Max loss per day: 5% of total capital
- Max loss per week: 10% of total capital
- If hit: stop trading for 48 hours, review

### Known Risks
| Risk | Severity | Mitigation |
|------|----------|-----------|
| Platform insolvency | HIGH | Never keep >30% on any single platform |
| Regulatory change | MEDIUM | Diversify across regulated (Kalshi) and crypto |
| Liquidity risk | MEDIUM | Only trade markets with >$100K volume |
| Execution risk | HIGH | Automate execution. Paper trade first. |
| Smart contract risk | LOW-MEDIUM | Use established markets only |

---

## Example Arbitrage Calculation

**Event:** "Will [Candidate] win [State]?"

| Platform | YES Price | NO Price | Fees |
|----------|-----------|----------|------|
| Polymarket | $0.42 | $0.58 | 0% |
| Kalshi | $0.48 | $0.53 | 7% on profit |

**Real arb threshold: spreads must exceed ~8-10% to be profitable after all fees.** This is why speed matters.

---

## Content Monetization Layer

Even if trading P&L is modest, the CONTENT is valuable:
1. X Thread: prediction market alpha series
2. Substack: $9.99/mo paid tier with trade logs
3. Gumroad: sell the scanner ($29-$49)
4. Course: "How to trade prediction markets profitably" ($97-$297)

---

## Synergy Map

| Stack With | How |
|-----------|-----|
| I04 (Algo Trading) | Same quant infrastructure |
| G10 (Quant Dashboard) | Add prediction market panel |
| CF008 (Finance News) | Finance content accounts post market analysis |
| MM015 (Newsletter) | Prediction market digest = newsletter content |

---

## Legal Considerations

- **Kalshi:** CFTC-regulated. Legal in US. 18+. KYC required.
- **Polymarket:** Operates outside US. US users: grey area.
- **Tax:** Prediction market gains are taxable. Kalshi issues 1099-B.
- **This is NOT financial advice.** Prediction markets involve risk of total loss.

---

## KPIs

| Metric | Month 1 | Month 3 | Month 6 |
|--------|---------|---------|---------|
| Capital deployed | $500-$1K | $2K-$5K | $5K-$20K |
| Trades executed | 5-10 | 20-40 | 40-80 |
| Win rate (arb) | 90%+ | 92%+ | 95%+ |
| Monthly return (arb only) | 2-5% | 3-6% | 4-8% |
| Content revenue | $0 | $100-$500 | $500-$3K |

---

## Quick Start Checklist

- [ ] Create Kalshi account (KYC, deposit $500)
- [ ] Create Polymarket wallet (USDC on Polygon, deposit $500)
- [ ] Create Manifold account (paper trading)
- [ ] Build basic price scraper for top 20 events
- [ ] Paper trade for 7 days minimum
- [ ] Build spread calculator with fee accounting
- [ ] Set up alerting for spreads > 8%
- [ ] Log all trades in LEDGER/PREDICTION_MARKET_TRADES.csv
- [ ] Start X content: prediction market alpha thread series
- [ ] Review after 20 live trades: continue, adjust, or kill
