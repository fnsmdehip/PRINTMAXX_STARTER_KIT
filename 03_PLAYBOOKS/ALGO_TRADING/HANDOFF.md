# ALGO_TRADING Handoff Document

**Last Updated:** 2026-01-26
**Status:** Deep dive research complete + Polymarket sub-method added
**Next Chat Priority:** HIGH - start implementation (paper trading accounts + Polymarket exploration)

---

## What Was Done This Session

### Session 3 (2026-01-26 - Current)

1. **Polymarket Opportunity Analysis Created**
   - Full analysis at `POLYMARKET_OPPORTUNITY_ANALYSIS.md`
   - Triggered by Twitter alpha: "$3.9M vibe coder" story
   - Sub-method ID: MM012-PM (Prediction Markets)
   - Synergy score: 90 with existing ALGO_TRADING infrastructure

2. **Key Findings:**
   - Polymarket = decentralized prediction market on Polygon (USDC)
   - Builder opportunities: trading bots, analytics, API wrappers, content
   - Legal: US users CANNOT trade (CFTC settlement) but CAN build tools
   - Alternative for US: Kalshi (CFTC-regulated)
   - Perfect overlap with existing signal scraper infrastructure

3. **Added to LEDGER:**
   - ALPHA352 in ALPHA_STAGING.csv (APPROVED)
   - Category: ALGO_TRADING
   - Status: Ready for implementation

### Session 2 (2026-01-24 - Previous)

1. **ALPHA204-205 APPROVED**
   - Updated ALPHA_STAGING.csv with approved status
   - Algo trading method fully validated

2. **Signal Infrastructure Created**
   - Added 20 FinTwit/trading sources to HIGH_SIGNAL_SOURCES.csv (SRC097-SRC116)
   - Sources include: @unusual_whales, @lookonchain, @WatcherGuru, @GlassNode, @DeItaone, @TokenUnlocks
   - Created `signals/trading_signal_scraper.py` with:
     - Signal type classification (WHALE, OPTIONS_FLOW, MACRO, ON_CHAIN, LIQUIDATION, BREAKOUT, NEWS)
     - Direction detection (BULLISH/BEARISH/NEUTRAL)
     - Asset extraction ($BTC, $ETH, tickers)
     - Number extraction (prices, percentages, amounts)
     - CSV logging to `signals/signal_log.csv`

3. **Infrastructure Validated**
   - Existing Twitter scraper is production-ready (Playwright-based)
   - Proxy support configured (Soax/Smartproxy)
   - Can adapt for trading signals in 2-3 hours

### Session 1 (2026-01-24 - Previous)

1. **Created full playbook** (`ALGO_TRADING_PLAYBOOK.md`)
   - Traditional markets: stocks, options, derivatives, commodities, metals
   - Crypto-specific section: on-chain analytics, whale tracking, MEV, exchange flows
   - Infrastructure design: data pipeline, tech stack, database schema
   - Ralph loop configurations for daily alpha scan, continuous monitoring, weekly review
   - A/B strategy versioning with auto-rollback
   - Info product angle for monetization beyond trading

2. **Added to PRINTMAXX system**
   - ALPHA204-205 in ALPHA_STAGING.csv (now APPROVED)
   - MM012 in CROSS_POLLINATION_MATRIX.csv
   - Updated MONEY_METHODS/INDEX.md with ALGO_TRADING section

3. **Documented cross-pollination**
   - Stack: Trading system + Finance expert AI persona + Finance news content + Info products
   - Synergy score: 85

---

## Key Thesis

> "the world is in denial about how much can be automated"

Claude-assisted trading with:
- Twitter signal aggregation
- Intuitive data analysis
- Backtesting on historical data
- A/B versioning of strategies
- Auto-rollback if updates degrade performance
- Ralph loops for perpetual optimization

Same applies to PE/VC due diligence, portfolio management, risk assessment.

---

## Crypto Unique Angles (Not Available in TradFi)

| Angle | Description | Tools |
|-------|-------------|-------|
| Whale tracking | Follow smart money wallets on-chain | Arkham, Nansen, Etherscan |
| Insider detection | Find wallets that received tokens pre-launch | On-chain analysis |
| MEV signals | Front-running activity reveals large pending trades | Flashbots, Eigenphi |
| Exchange flows | CEX inflow/outflow predicts price pressure | Glassnode, CryptoQuant |
| Liquidation mapping | Know where cascades will trigger | Coinglass, on-chain |
| Token unlocks | Supply shock calendar | Token Unlocks, Messari |

---

## What Needs to Be Built Next

### Phase 1: Signal Infrastructure
- [x] Twitter scraper for fintwit/crypto twitter (trading_signal_scraper.py created)
- [x] FinTwit sources added (20 accounts: SRC097-SRC116)
- [ ] Connect scraper to Playwright browser automation
- [ ] News aggregator (SEC filings, crypto news)
- [ ] On-chain data pipeline (whale wallets, exchange flows)
- [ ] Claude analysis prompts for signal interpretation

### Phase 2: Backtesting Framework
- [ ] Set up Backtrader or QuantConnect
- [ ] Historical data ingestion
- [ ] Strategy template library
- [ ] Performance metrics dashboard (Sharpe, drawdown, win rate)

### Phase 3: Paper Trading
- [ ] Alpaca account for stocks
- [ ] Testnet accounts for crypto
- [ ] A/B versioning system
- [ ] Auto-rollback triggers

### Phase 4: Live Trading (After Validation)
- [ ] Position sizing limits
- [ ] Stop-loss automation
- [ ] Daily/weekly review ralph loops
- [ ] Alert system for anomalies

### Phase 5: Info Products
- [ ] Lead magnet: "5 Twitter Signals That Predicted Market Moves"
- [ ] Core product: "Algo Trading Starter Kit" ($97)
- [ ] Premium: Strategy framework + weekly signals ($297)
- [ ] DWY: Custom system setup ($997)

---

## Technical Stack Summary

| Component | Recommended Tool | Alternative |
|-----------|------------------|-------------|
| Twitter data | Twitter API v2, Nitter scrape | Apify |
| Stock execution | Alpaca | IBKR |
| Crypto execution | Coinbase, Binance | DEX aggregators |
| On-chain data | Dune Analytics | The Graph |
| Whale tracking | Arkham | Nansen, custom |
| Backtesting | Backtrader | QuantConnect, Zipline |
| Database | PostgreSQL | TimescaleDB |
| Monitoring | Grafana | Custom dashboards |
| Alerts | Telegram bots | Discord webhooks |

---

## Risk Management Rules (NON-NEGOTIABLE)

1. **Position sizing:** Max 2-5% per trade
2. **Daily loss limit:** Stop trading at -X%
3. **Drawdown limits:**
   - 10% monthly → reduce position sizes 50%
   - 20% monthly → pause trading, review
   - 30% → stop, full audit
4. **No leverage until profitable for 3+ months**
5. **Paper trade minimum 4 weeks before live**
6. **Crypto-specific:** Never hold significant on CEX, use hardware wallets

---

## Cross-Pollination Stack

```
ALGO_TRADING (MM012)
    ↓ generates insights
AI_INFLUENCER/NICHE_EXPERTS (AI001)
    ↓ builds authority from insights
CONTENT_FARM/FINANCE_NEWS (CF008)
    ↓ amplifies reach
INFO_PRODUCTS (MM002)
    ↓ monetizes audience
Signal subscriptions (recurring revenue)
```

---

## Files in This Folder

```
ALGO_TRADING/
├── ALGO_TRADING_PLAYBOOK.md       # Full playbook (created)
├── ALGO_TRADING_DEEP_DIVE.md      # Comprehensive research guide (NEW 2026-01-25)
├── CLAUDE_CODE_TRADING_BOTS.md    # Claude Code trading bot dev (NEW 2026-01-26 - ALPHA358)
├── POLYMARKET_OPPORTUNITY_ANALYSIS.md  # Prediction markets sub-method (NEW 2026-01-26)
├── HANDOFF.md                      # This file
├── signals/
│   ├── trading_signal_scraper.py  # Signal scraper
│   ├── signal_log.csv             # Signal output (created on first run)
│   └── logs/                      # Scraper logs
├── strategies/                     # TODO: Strategy templates
├── backtests/                      # TODO: Backtest results
└── info_products/                  # TODO: Product content
```

---

## Questions for Next Session

1. **Capital allocation:** How much to allocate to trading vs info products?
2. **Market focus:** Start with stocks, crypto, or both?
3. **Timeline:** When to target first paper trades?
4. **Tools:** Which paid tools to prioritize (Nansen expensive but high signal)?

---

## Related PRINTMAXX Files

- `LEDGER/ALPHA_STAGING.csv` - ALPHA204-205 for algo trading
- `LEDGER/CROSS_POLLINATION_MATRIX.csv` - MM012 entry
- `MONEY_METHODS/INDEX.md` - ALGO_TRADING section
- `OPS/SWARM_PROMOTION_PLAYBOOK.md` - For distribution of info products

---

## Immediate Next Actions

1. **Set up Alpaca paper account** for stocks
2. **Set up Coinbase Advanced** for crypto
3. **Configure TradingView webhooks** for alerts
4. **Run trading_signal_scraper.py** with real Twitter data
5. **Build first backtest** using QuantConnect or Backtrader
6. **Draft lead magnet content** for info product funnel

### Polymarket-Specific Next Actions

7. **Review Polymarket API docs** (https://docs.polymarket.com)
8. **Set up Polygon wallet** + fund with test USDC
9. **Make 5 small trades manually** to learn platform mechanics
10. **Adapt signal scraper for news** relevant to prediction markets
11. **Identify 10 markets** with potential mispricing
12. **Start Twitter content** documenting prediction market journey

**Deep Dive Research Complete:** See `ALGO_TRADING_DEEP_DIVE.md` for:
- Signal source comparison (Unusual Whales, Arkham, Nansen, etc.)
- Platform recommendations (Alpaca, Coinbase, DEX aggregators)
- Full automation workflow with code templates
- Backtesting platform comparison (QuantConnect vs Backtrader vs Freqtrade)
- Risk management framework
- 4-week getting started timeline
- Strategy templates (whale following, options flow, news sentiment)

---

## Session Notes

User insight: "the world is in denial of this and in meantime before elons UHI theory or whatever happens this is true alpha. also selling such info is true alpha."

Key differentiation from typical quant:
- Claude for intuitive analysis, not just statistical
- Twitter/social signals as leading indicators
- Crypto on-chain transparency as unique edge
- Info product monetization parallel to trading
- Ralph loops for perpetual optimization

This is a high-conviction play. The infrastructure exists. The edge is execution speed and intelligence of the system.

---

Last Updated: 2026-01-24
