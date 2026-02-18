# Algo Trading Deep Dive: Signal Sources, Platforms, and Automation

**Last Updated:** 2026-01-25
**Status:** Research Complete - Ready for Implementation
**Capital Requirement:** $1k-100k+ depending on strategy
**Risk Level:** HIGH (trading losses possible)

---

## Table of Contents

1. [Signal Source Comparison](#signal-source-comparison)
2. [Trading Platform Recommendations](#trading-platform-recommendations)
3. [Automation Workflow](#automation-workflow)
4. [Risk Management](#risk-management)
5. [Getting Started Steps](#getting-started-steps)
6. [Strategy Templates](#strategy-templates)

---

## Signal Source Comparison

### Options Flow Tools

| Tool | Monthly Cost | Best For | Data Quality | API Access |
|------|-------------|----------|--------------|------------|
| **Unusual Whales** | $40-150 | Retail traders, options flow | HIGH | Yes (premium) |
| **Cheddar Flow** | $99-299 | Professional options flow | HIGHEST | Yes |
| **FlowAlgo** | $79-199 | Real-time options alerts | HIGH | Limited |
| **BlackBoxStocks** | $79-999 | Scanner + options flow | MEDIUM | No |
| **Market Chameleon** | $69-199 | Options analytics | HIGH | Yes |

**Recommendation:** Start with Unusual Whales ($40/mo tier). Best signal-to-noise ratio for the price. Upgrade to Cheddar Flow if you're profitable and need faster data.

**What to Watch:**
- Unusual call sweeps (bullish)
- Unusual put sweeps (bearish)
- Dark pool prints (institutional activity)
- Gamma exposure levels
- Open interest changes
- IV rank anomalies

### Crypto Whale Tracking

| Tool | Monthly Cost | Best For | Chains Covered | Speed |
|------|-------------|----------|----------------|-------|
| **Arkham Intelligence** | Free-$500 | Entity identification | ETH, BTC, SOL | Real-time |
| **Nansen** | $150-1500 | Smart money labels | 15+ chains | Real-time |
| **Lookonchain** | Free (Twitter) | Breaking whale moves | Major chains | 5-15 min |
| **Whale Alert** | Free (Twitter) | Large transfers | BTC, ETH | 1-5 min |
| **DeBank** | Free | Wallet tracking | EVM chains | Near real-time |
| **Etherscan/Solscan** | Free | Raw on-chain data | Single chain | Immediate |

**Recommendation:**
- **Free tier:** Lookonchain + Whale Alert Twitter + DeBank
- **Paid:** Arkham ($0 to start) for entity labeling, upgrade to Nansen if doing serious on-chain analysis

**Key Whale Tracking Strategies:**

1. **Exchange Flow Analysis**
   ```
   CEX Inflow (tokens to exchange) = Sell pressure coming
   CEX Outflow (tokens from exchange) = Accumulation signal
   Large stablecoin inflow to DEX = Buying incoming
   ```

2. **Smart Money Following**
   - Identify wallets with consistent profits
   - Track their new token entries
   - Note: 15-30 min delay is still alpha

3. **Insider Detection**
   - Find wallets that received tokens before public sale
   - Track their sell patterns as exit signals
   - Cross-reference with team wallet labels

### Social Sentiment Tools

| Tool | Monthly Cost | Best For | Data Sources | Accuracy |
|------|-------------|----------|--------------|----------|
| **LunarCrush** | Free-$150 | Crypto social metrics | Twitter, Reddit | MEDIUM |
| **Santiment** | $49-299 | On-chain + social | Multiple | HIGH |
| **The TIE** | Enterprise | Institutional sentiment | News, social | HIGHEST |
| **Stocktwits** | Free | Stock retail sentiment | App users | LOW-MEDIUM |
| **Reddit API** | Free | WallStreetBets, etc. | Reddit | MEDIUM |

**Recommendation:**
- Crypto: Santiment for combined on-chain + social
- Stocks: Build custom Reddit/Stocktwits scraper (more alpha than paid tools)

**Sentiment Indicators to Track:**
- Volume of mentions (spikes = attention)
- Sentiment polarity (bullish/bearish ratio)
- Influencer activity (when big accounts talk)
- FUD detection (coordinated negative campaigns)

### Technical Alert Tools

| Tool | Monthly Cost | Best For | Alert Types | Integrations |
|------|-------------|----------|-------------|--------------|
| **TradingView** | $0-60 | Multi-asset charting | Price, indicator, pattern | Webhooks |
| **Thinkorswim** | Free w/ TDA | Options charting | Price, scanner | Limited |
| **TC2000** | $10-90 | Stock scanning | Custom conditions | Alerts only |
| **Coinigy** | $19-99 | Crypto charting | Price, volume | Webhooks |

**Recommendation:** TradingView Pro ($15/mo) for webhooks + multi-chart. Essential for automation.

**High-Value TradingView Alerts:**
- Support/resistance breaks
- Volume spikes (3x average)
- RSI divergences
- MACD crossovers
- Bollinger Band squeezes

### News-Based Signal Sources

| Source | Cost | Speed | Coverage | API |
|--------|------|-------|----------|-----|
| **@DeItaone (Twitter)** | Free | Fastest | Headlines | No |
| **@zerohedge** | Free | Fast | Macro/markets | No |
| **@WatcherGuru** | Free | Fast | Crypto news | No |
| **Benzinga Pro** | $79-177 | Fast | Stocks | Yes |
| **NewsAPI.org** | Free-$449 | Medium | General | Yes |
| **SEC EDGAR** | Free | Official | Filings | Yes |

**Recommendation:**
- Twitter accounts for breaking news (free)
- Benzinga Pro if trading news actively
- SEC EDGAR API for filings (earnings, 13F, 8-K)

### On-Chain Data (Crypto Specific)

| Tool | Monthly Cost | Best For | Data Types | Latency |
|------|-------------|----------|------------|---------|
| **Glassnode** | $39-799 | Bitcoin analytics | UTXO, supply | 1hr+ |
| **CryptoQuant** | $49-199 | Exchange flows | CEX data | 15min |
| **Dune Analytics** | Free-$350 | Custom queries | All EVM | Varies |
| **The Graph** | Pay per query | Protocol data | DeFi | Real-time |
| **Token Terminal** | Free-$325 | Fundamentals | Revenue, TVL | Daily |
| **Coinglass** | Free-$50 | Derivatives | Funding, OI, liquidations | Real-time |

**Recommendation:**
- **Free:** Coinglass (derivatives) + Dune (custom queries)
- **Paid:** CryptoQuant for exchange flow signals

**On-Chain Metrics That Matter:**

| Metric | Bullish | Bearish |
|--------|---------|---------|
| Exchange balance | Decreasing | Increasing |
| Funding rate | Negative (contrarian) | Extreme positive |
| Open interest | Rising with price | Rising against price |
| MVRV Z-Score | Below 0 | Above 7 |
| Stablecoin supply ratio | Increasing | Decreasing |
| NVT ratio | Low | High |

---

## Trading Platform Recommendations

### Stock Trading Platforms

| Platform | Commissions | API Quality | Paper Trading | Best For |
|----------|-------------|-------------|---------------|----------|
| **Alpaca** | $0 | Excellent | Yes (free) | Algo trading |
| **Interactive Brokers** | $0-low | Excellent | Yes | Full market access |
| **TD Ameritrade** | $0 | Good | Yes | Options, scanning |
| **Tradier** | $0-35/mo | Good | Yes | API-first |
| **Robinhood** | $0 | Limited | No | Don't use for algo |

**Recommendation: Alpaca for Stocks**

**Why Alpaca:**
- Commission-free stocks and ETFs
- Excellent REST + WebSocket API
- Paper trading with real market data
- Easy authentication (API key only)
- Good documentation
- Python SDK available

**Alpaca Setup:**
```python
import alpaca_trade_api as tradeapi

api = tradeapi.REST(
    key_id='YOUR_API_KEY',
    secret_key='YOUR_SECRET_KEY',
    base_url='https://paper-api.alpaca.markets'  # Paper trading
)

# Get account info
account = api.get_account()
print(f"Buying power: ${account.buying_power}")

# Submit order
api.submit_order(
    symbol='SPY',
    qty=10,
    side='buy',
    type='market',
    time_in_force='day'
)
```

### Crypto Trading Platforms

| Platform | Fees | API Quality | US Available | Best For |
|----------|------|-------------|--------------|----------|
| **Coinbase Advanced** | 0.05-0.6% | Good | Yes | US compliant |
| **Binance** | 0.1% | Excellent | No (US)* | International |
| **Kraken** | 0.16-0.26% | Good | Yes | Pro traders |
| **FTX** | N/A | N/A | No | Bankrupt |
| **Bybit** | 0.1% | Good | No (US) | Derivatives |
| **Hyperliquid** | 0.02-0.05% | Good | ? | Perps |

*Binance.US has limited features

**Recommendation: Coinbase Advanced (US) or Binance (non-US)**

**Coinbase Advanced Setup:**
```python
from coinbase.rest import RESTClient

client = RESTClient(api_key="YOUR_KEY", api_secret="YOUR_SECRET")

# Get account balance
accounts = client.get_accounts()

# Place order
order = client.create_order(
    product_id="BTC-USD",
    side="BUY",
    order_configuration={
        "market_market_ioc": {
            "quote_size": "100.00"  # $100 market buy
        }
    }
)
```

### DEX Aggregators (Crypto)

| Platform | Chains | Best Rates | API | Use Case |
|----------|--------|------------|-----|----------|
| **1inch** | 10+ | Excellent | Yes | Best execution |
| **Paraswap** | 5+ | Good | Yes | Gas efficient |
| **0x** | 5+ | Good | Yes | DEX aggregation |
| **Jupiter** | Solana | Best on SOL | Yes | Solana swaps |
| **CowSwap** | ETH | MEV protected | Yes | No sandwiching |

**Recommendation:**
- Ethereum: CowSwap (MEV protection) or 1inch (best rates)
- Solana: Jupiter

---

## Automation Workflow

### Architecture Overview

```
                    SIGNAL SOURCES
                         |
    +--------+--------+--+--+--------+--------+
    |        |        |     |        |        |
 Twitter   Options  Whale  News   On-Chain  Technical
  Feeds     Flow    Alerts Feeds    Data     Alerts
    |        |        |     |        |        |
    +--------+--------+--+--+--------+--------+
                         |
                   SIGNAL AGGREGATOR
                    (Python/n8n)
                         |
              +----------+----------+
              |                     |
         FILTERING              ANALYSIS
     (Signal quality,         (Claude API,
      deduplication)         pattern matching)
              |                     |
              +----------+----------+
                         |
                  DECISION ENGINE
                 (Strategy rules)
                         |
              +----------+----------+
              |          |          |
           PAPER     BACKTEST    LIVE
          TRADING    COMPARE    TRADING
              |          |          |
              +----------+----------+
                         |
                    EXECUTION
                  (Alpaca/Coinbase)
                         |
                   MONITORING
              (P&L, risk, alerts)
```

### Python Trading Bot Framework

**Directory Structure:**
```
trading_bot/
├── config/
│   ├── settings.py
│   └── credentials.py (gitignored)
├── signals/
│   ├── twitter_scraper.py
│   ├── options_flow.py
│   ├── whale_tracker.py
│   └── aggregator.py
├── analysis/
│   ├── claude_analyzer.py
│   └── pattern_detector.py
├── strategy/
│   ├── base_strategy.py
│   ├── momentum.py
│   └── mean_reversion.py
├── execution/
│   ├── alpaca_executor.py
│   ├── coinbase_executor.py
│   └── paper_trader.py
├── risk/
│   ├── position_sizer.py
│   └── risk_manager.py
├── monitoring/
│   ├── pnl_tracker.py
│   └── alerter.py
├── backtesting/
│   ├── backtrader_engine.py
│   └── results/
└── main.py
```

**Signal Aggregator Example:**
```python
# signals/aggregator.py

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import asyncio

@dataclass
class Signal:
    source: str
    signal_type: str  # WHALE, OPTIONS, NEWS, TECHNICAL
    asset: str
    direction: str  # BULLISH, BEARISH, NEUTRAL
    confidence: float  # 0-1
    timestamp: datetime
    raw_data: dict

class SignalAggregator:
    def __init__(self):
        self.signals: List[Signal] = []
        self.sources = []

    async def collect_signals(self, lookback_minutes: int = 60) -> List[Signal]:
        """Collect signals from all sources."""
        tasks = [
            self.get_twitter_signals(),
            self.get_options_flow(),
            self.get_whale_alerts(),
            self.get_technical_alerts(),
        ]
        results = await asyncio.gather(*tasks)

        all_signals = []
        for signal_list in results:
            all_signals.extend(signal_list)

        # Deduplicate and sort by timestamp
        return self.deduplicate(all_signals)

    def aggregate_by_asset(self, signals: List[Signal]) -> dict:
        """Group signals by asset and calculate aggregate sentiment."""
        by_asset = {}

        for signal in signals:
            if signal.asset not in by_asset:
                by_asset[signal.asset] = {
                    'bullish_signals': 0,
                    'bearish_signals': 0,
                    'total_confidence': 0,
                    'signals': []
                }

            asset_data = by_asset[signal.asset]
            asset_data['signals'].append(signal)

            if signal.direction == 'BULLISH':
                asset_data['bullish_signals'] += signal.confidence
            elif signal.direction == 'BEARISH':
                asset_data['bearish_signals'] += signal.confidence

            asset_data['total_confidence'] += signal.confidence

        return by_asset
```

**Strategy Base Class:**
```python
# strategy/base_strategy.py

from abc import ABC, abstractmethod
from typing import Optional
from signals.aggregator import Signal

class BaseStrategy(ABC):
    def __init__(self, config: dict):
        self.config = config
        self.positions = {}

    @abstractmethod
    def evaluate(self, signals: list) -> Optional[dict]:
        """
        Evaluate signals and return trade decision.
        Returns: {'action': 'BUY'|'SELL'|'HOLD', 'asset': str, 'size': float}
        """
        pass

    @abstractmethod
    def get_position_size(self, asset: str, account_value: float) -> float:
        """Calculate position size based on risk rules."""
        pass

    def validate_risk(self, trade: dict, account: dict) -> bool:
        """Validate trade against risk limits."""
        max_position_pct = self.config.get('max_position_pct', 0.05)
        max_position_value = account['equity'] * max_position_pct

        if trade['size'] * trade.get('price', 100) > max_position_value:
            return False
        return True
```

### n8n/Make Automation (No-Code Option)

**Workflow: Twitter Signal to Discord Alert**

```
[Twitter Trigger]
      |
      v
[Filter: Contains $BTC or $ETH]
      |
      v
[Claude API: Classify signal]
      |
      v
[IF: Confidence > 0.7]
      |
      v
[Discord Webhook: Send alert]
      |
      v
[Google Sheets: Log signal]
```

**n8n Nodes Required:**
1. Twitter Trigger (polling or API)
2. IF node (filter conditions)
3. HTTP Request (Claude API)
4. Discord node
5. Google Sheets node

### Webhook Integration (TradingView to Execution)

**TradingView Alert Setup:**
```
// Alert message format
{
  "action": "{{strategy.order.action}}",
  "ticker": "{{ticker}}",
  "price": "{{close}}",
  "time": "{{time}}",
  "strategy": "breakout_v1"
}
```

**Webhook Receiver (FastAPI):**
```python
from fastapi import FastAPI, Request
import alpaca_trade_api as tradeapi

app = FastAPI()
api = tradeapi.REST(API_KEY, SECRET_KEY, paper=True)

@app.post("/webhook/tradingview")
async def handle_tv_alert(request: Request):
    data = await request.json()

    # Validate secret (basic auth)
    if data.get('secret') != WEBHOOK_SECRET:
        return {"error": "Unauthorized"}

    # Execute trade
    if data['action'] == 'buy':
        api.submit_order(
            symbol=data['ticker'],
            qty=calculate_qty(data['ticker']),
            side='buy',
            type='market',
            time_in_force='day'
        )

    return {"status": "executed", "action": data['action']}
```

### Alert Systems

**Telegram Bot for Alerts:**
```python
import telegram
from telegram import Bot

bot = Bot(token="YOUR_BOT_TOKEN")
CHAT_ID = "YOUR_CHAT_ID"

async def send_alert(message: str, urgency: str = "normal"):
    """Send trading alert to Telegram."""
    emoji = {"high": "🚨", "normal": "📊", "low": "ℹ️"}
    formatted = f"{emoji.get(urgency, '')} {message}"

    await bot.send_message(
        chat_id=CHAT_ID,
        text=formatted,
        parse_mode='Markdown'
    )

# Usage
await send_alert("$BTC whale moved 5,000 BTC to Binance", urgency="high")
```

**Discord Webhook:**
```python
import requests

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/..."

def send_discord_alert(content: str, embed: dict = None):
    payload = {"content": content}
    if embed:
        payload["embeds"] = [embed]

    requests.post(DISCORD_WEBHOOK, json=payload)

# Rich embed for trade signals
send_discord_alert("", embed={
    "title": "🐋 Whale Alert",
    "description": "5,000 BTC moved from Binance",
    "color": 0xFF0000,
    "fields": [
        {"name": "Asset", "value": "BTC", "inline": True},
        {"name": "Direction", "value": "Bearish", "inline": True},
        {"name": "Confidence", "value": "High", "inline": True}
    ]
})
```

---

## Backtesting Platforms

### Platform Comparison

| Platform | Language | Data | Live Trading | Cost | Best For |
|----------|----------|------|--------------|------|----------|
| **QuantConnect** | Python/C# | Included | Yes | Free-$8-80/mo | Full workflow |
| **Backtrader** | Python | BYOD | Manual | Free | Flexibility |
| **Zipline** | Python | BYOD | No | Free | Research |
| **VectorBT** | Python | BYOD | No | Free | Fast backtests |
| **Freqtrade** | Python | BYOD | Yes (crypto) | Free | Crypto bots |
| **TradingView** | Pine | Included | Via broker | $0-60 | Visual testing |

**Recommendation:**
- **Starting out:** QuantConnect (free tier, data included)
- **Custom strategies:** Backtrader (most flexible)
- **Crypto only:** Freqtrade (full crypto bot framework)

### QuantConnect Setup

```python
# QuantConnect algorithm template
class MyAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2023, 1, 1)
        self.SetEndDate(2024, 1, 1)
        self.SetCash(100000)

        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol

        # Indicators
        self.sma_fast = self.SMA(self.spy, 10)
        self.sma_slow = self.SMA(self.spy, 50)

    def OnData(self, data):
        if not self.sma_fast.IsReady:
            return

        # Simple crossover strategy
        if self.sma_fast.Current.Value > self.sma_slow.Current.Value:
            if not self.Portfolio.Invested:
                self.SetHoldings(self.spy, 1.0)
        else:
            if self.Portfolio.Invested:
                self.Liquidate(self.spy)
```

### Backtrader Example

```python
import backtrader as bt

class SignalStrategy(bt.Strategy):
    params = (
        ('fast_period', 10),
        ('slow_period', 50),
        ('risk_pct', 0.02),
    )

    def __init__(self):
        self.sma_fast = bt.indicators.SMA(period=self.p.fast_period)
        self.sma_slow = bt.indicators.SMA(period=self.p.slow_period)
        self.crossover = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)

    def next(self):
        if self.crossover > 0:
            size = self.broker.getcash() * self.p.risk_pct / self.data.close[0]
            self.buy(size=int(size))
        elif self.crossover < 0:
            self.close()

# Run backtest
cerebro = bt.Cerebro()
cerebro.addstrategy(SignalStrategy)
cerebro.broker.setcash(100000)

# Add data
data = bt.feeds.YahooFinanceData(dataname='SPY', fromdate=datetime(2023,1,1))
cerebro.adddata(data)

# Run
results = cerebro.run()
cerebro.plot()
```

### Performance Metrics to Track

| Metric | Target | Red Flag |
|--------|--------|----------|
| **Sharpe Ratio** | > 1.5 | < 0.5 |
| **Max Drawdown** | < 20% | > 30% |
| **Win Rate** | > 50% | < 40% |
| **Profit Factor** | > 1.5 | < 1.0 |
| **Recovery Factor** | > 3 | < 1 |
| **Avg Win/Avg Loss** | > 1.5 | < 1.0 |
| **Trades per Month** | 5-50 | > 200 (overtrading) |

---

## Risk Management

### Position Sizing Rules

**Fixed Percentage Risk:**
```python
def calculate_position_size(
    account_value: float,
    risk_per_trade: float = 0.02,  # 2% max risk
    entry_price: float,
    stop_loss_price: float
) -> float:
    """
    Calculate position size based on fixed percentage risk.
    """
    risk_amount = account_value * risk_per_trade
    risk_per_share = abs(entry_price - stop_loss_price)

    if risk_per_share == 0:
        return 0

    shares = risk_amount / risk_per_share
    return int(shares)

# Example: $100k account, buy at $150, stop at $145
# Risk: $2,000 (2% of $100k)
# Shares: $2,000 / $5 = 400 shares
# Position: $60,000 (60% of account) BUT only risking $2,000
```

**Kelly Criterion (Advanced):**
```python
def kelly_position_size(
    win_rate: float,  # Historical win rate (0-1)
    avg_win: float,   # Average winning trade
    avg_loss: float,  # Average losing trade
    kelly_fraction: float = 0.5  # Use half-Kelly for safety
) -> float:
    """
    Calculate Kelly-optimal position size.
    """
    if avg_loss == 0:
        return 0

    win_loss_ratio = avg_win / avg_loss
    kelly = win_rate - ((1 - win_rate) / win_loss_ratio)

    # Apply fractional Kelly for safety
    return max(0, kelly * kelly_fraction)

# Example: 55% win rate, avg win $200, avg loss $100
# Full Kelly: 0.55 - (0.45 / 2) = 0.325 (32.5% of portfolio)
# Half Kelly: 0.1625 (16.25% of portfolio)
```

### Daily Loss Limits

```python
class RiskManager:
    def __init__(self, max_daily_loss_pct: float = 0.03):
        self.max_daily_loss_pct = max_daily_loss_pct
        self.starting_equity = None
        self.trading_halted = False

    def check_daily_loss(self, current_equity: float) -> bool:
        """Returns True if trading should stop."""
        if self.starting_equity is None:
            self.starting_equity = current_equity
            return False

        daily_pnl_pct = (current_equity - self.starting_equity) / self.starting_equity

        if daily_pnl_pct <= -self.max_daily_loss_pct:
            self.trading_halted = True
            return True

        return False
```

### Drawdown Limits

| Drawdown Level | Action |
|----------------|--------|
| 5% | Review recent trades |
| 10% | Reduce position sizes by 50% |
| 15% | Stop new trades, review strategy |
| 20% | Pause trading, full audit |
| 25% | Stop all trading, reassess |

### Correlation Risk

```python
def check_correlation_risk(positions: dict, max_correlation: float = 0.7) -> bool:
    """
    Check if positions are too correlated.
    Returns True if risk is acceptable.
    """
    # Get correlation matrix
    tickers = list(positions.keys())

    # Simplified: check for obvious correlations
    # Tech stocks (AAPL, MSFT, GOOG) correlate highly
    # Crypto (BTC, ETH, SOL) correlate highly

    tech_exposure = sum(positions.get(t, 0) for t in ['AAPL', 'MSFT', 'GOOG', 'NVDA', 'META'])
    crypto_exposure = sum(positions.get(t, 0) for t in ['BTC', 'ETH', 'SOL'])

    total_exposure = sum(positions.values())

    if tech_exposure / total_exposure > 0.6:
        return False  # Too concentrated in tech
    if crypto_exposure / total_exposure > 0.4:
        return False  # Too concentrated in crypto

    return True
```

### Stop-Loss Automation

```python
class StopLossManager:
    def __init__(self):
        self.stops = {}  # {symbol: {'type': 'fixed'|'trailing', 'price': float}}

    def set_stop(self, symbol: str, entry: float, stop_type: str = 'fixed',
                 stop_pct: float = 0.05):
        """Set stop-loss for position."""
        if stop_type == 'fixed':
            self.stops[symbol] = {
                'type': 'fixed',
                'price': entry * (1 - stop_pct)
            }
        elif stop_type == 'trailing':
            self.stops[symbol] = {
                'type': 'trailing',
                'price': entry * (1 - stop_pct),
                'trail_pct': stop_pct
            }

    def update_trailing_stops(self, current_prices: dict):
        """Update trailing stops with new high prices."""
        for symbol, stop_data in self.stops.items():
            if stop_data['type'] == 'trailing':
                current = current_prices.get(symbol, 0)
                new_stop = current * (1 - stop_data['trail_pct'])
                if new_stop > stop_data['price']:
                    stop_data['price'] = new_stop

    def check_stops(self, current_prices: dict) -> list:
        """Check if any stops are triggered. Returns list of symbols to close."""
        triggered = []
        for symbol, stop_data in self.stops.items():
            current = current_prices.get(symbol, float('inf'))
            if current <= stop_data['price']:
                triggered.append(symbol)
        return triggered
```

### Legal Disclaimers (Required)

**On All Content:**
```
DISCLAIMER: This content is for educational purposes only and does not
constitute financial advice. Trading involves substantial risk of loss.
Past performance does not guarantee future results. Never trade with
money you cannot afford to lose. Consult a licensed financial advisor
before making investment decisions.
```

**For Info Products:**
- Include disclaimer on every page
- No specific return guarantees
- Paper trade for minimum 4 weeks recommendation
- "Results may vary" on any case studies

---

## Getting Started Steps

### Week 1: Foundation

**Day 1-2: Accounts**
- [ ] Create Alpaca paper trading account
- [ ] Create Coinbase Advanced account (crypto)
- [ ] Set up TradingView free account
- [ ] Create Discord server for alerts

**Day 3-4: Signal Sources**
- [ ] Follow trading Twitter accounts (see HIGH_SIGNAL_SOURCES.csv)
- [ ] Set up Unusual Whales free tier
- [ ] Set up Coinglass for derivatives data
- [ ] Create DeBank watchlist for whale wallets

**Day 5-7: Infrastructure**
- [ ] Set up Python environment
- [ ] Install trading libraries: `pip install alpaca-trade-api backtrader ccxt`
- [ ] Clone/create trading bot directory structure
- [ ] Test Alpaca paper trading API

### Week 2: Signal Collection

**Day 1-3: Twitter Pipeline**
- [ ] Set up trading signal scraper (trading_signal_scraper.py)
- [ ] Configure Playwright for Twitter scraping
- [ ] Test signal parsing and classification
- [ ] Connect to signal log CSV

**Day 4-5: Webhook Alerts**
- [ ] Set up TradingView webhooks
- [ ] Create webhook receiver (FastAPI)
- [ ] Test TradingView -> Local pipeline
- [ ] Set up Telegram/Discord alerts

**Day 6-7: Data Storage**
- [ ] Set up PostgreSQL or SQLite
- [ ] Create tables (signals, trades, performance)
- [ ] Test data logging
- [ ] Create basic dashboard

### Week 3: Strategy Development

**Day 1-3: Backtesting**
- [ ] Set up QuantConnect account
- [ ] Or configure Backtrader locally
- [ ] Download historical data
- [ ] Implement first simple strategy

**Day 4-5: Strategy Refinement**
- [ ] Backtest multiple parameter sets
- [ ] Calculate performance metrics
- [ ] Document strategy rules clearly
- [ ] Identify edge (why would this work?)

**Day 6-7: Risk Framework**
- [ ] Implement position sizing
- [ ] Implement stop-loss logic
- [ ] Set daily loss limits
- [ ] Create risk management checklist

### Week 4: Paper Trading

**Day 1-7: Live Paper Testing**
- [ ] Deploy to paper trading
- [ ] Run for full week
- [ ] Track every trade with rationale
- [ ] Compare to backtest expectations
- [ ] Note any execution issues

**End of Week 4:**
- [ ] Calculate paper trading metrics
- [ ] Document differences from backtest
- [ ] Decide: continue paper or investigate issues
- [ ] Create optimization list

### Weeks 5-8: Extended Paper Trading

- [ ] Run for minimum 4 weeks
- [ ] Weekly performance reviews
- [ ] A/B test strategy variations
- [ ] Refine based on results
- [ ] Build confidence before live

### Week 9+: Small Live (If Profitable)

- [ ] Start with 10% of intended capital
- [ ] Strict position limits (even smaller)
- [ ] Daily review first month
- [ ] Scale gradually if profitable
- [ ] Never exceed risk limits

---

## Strategy Templates

### Template 1: Whale Following (Crypto)

**Edge:** Smart money (known profitable wallets) moves before retail.

**Signals:**
- Whale wallet accumulation (Arkham/Nansen)
- Exchange outflow spikes
- Stablecoin movement to DEX

**Rules:**
```python
def whale_following_strategy(signals: list) -> dict:
    for signal in signals:
        if signal.type == 'WHALE' and signal.direction == 'BULLISH':
            if signal.amount_usd > 1_000_000:  # >$1M move
                if signal.asset in ['BTC', 'ETH', 'SOL']:
                    return {
                        'action': 'BUY',
                        'asset': signal.asset,
                        'size': 0.05,  # 5% of portfolio
                        'stop_loss': 0.05,  # 5% stop
                        'take_profit': 0.15  # 15% target
                    }
    return {'action': 'HOLD'}
```

### Template 2: Options Flow Following (Stocks)

**Edge:** Unusual options activity often precedes price moves.

**Signals:**
- Unusual call sweeps (bullish)
- Unusual put sweeps (bearish)
- Dark pool prints

**Rules:**
```python
def options_flow_strategy(signals: list) -> dict:
    for signal in signals:
        if signal.type == 'OPTIONS_FLOW':
            # Large call sweep with short expiry = conviction
            if signal.option_type == 'CALL' and signal.premium > 100_000:
                if signal.days_to_expiry < 30:  # Near-term = conviction
                    return {
                        'action': 'BUY',
                        'asset': signal.underlying,
                        'size': 0.03,
                        'stop_loss': 0.03,
                        'take_profit': 0.10,
                        'time_limit': signal.days_to_expiry - 5  # Exit before expiry
                    }
    return {'action': 'HOLD'}
```

### Template 3: News Sentiment (Multi-Asset)

**Edge:** First mover on breaking news.

**Signals:**
- @DeItaone headlines
- SEC filings (8-K, 13F)
- Crypto news (@WatcherGuru)

**Rules:**
```python
def news_sentiment_strategy(signals: list) -> dict:
    for signal in signals:
        if signal.type == 'NEWS' and signal.freshness < 300:  # <5 min old
            sentiment = analyze_sentiment(signal.content)  # Claude API

            if sentiment.score > 0.7 and sentiment.confidence > 0.8:
                return {
                    'action': 'BUY',
                    'asset': signal.asset,
                    'size': 0.02,  # Smaller size for news trades
                    'stop_loss': 0.03,
                    'time_limit': 60  # Exit within 1 hour
                }
            elif sentiment.score < -0.7 and sentiment.confidence > 0.8:
                return {
                    'action': 'SELL',  # Or short if available
                    'asset': signal.asset,
                    'size': 0.02,
                    'stop_loss': 0.03,
                    'time_limit': 60
                }
    return {'action': 'HOLD'}
```

### Template 4: Mean Reversion (Technical)

**Edge:** Oversold/overbought conditions tend to revert.

**Signals:**
- RSI extremes (<30 or >70)
- Bollinger Band touches
- Volume divergence

**Rules:**
```python
def mean_reversion_strategy(data: dict) -> dict:
    rsi = data['rsi']
    bb_lower = data['bb_lower']
    bb_upper = data['bb_upper']
    price = data['close']
    volume = data['volume']
    avg_volume = data['avg_volume']

    # Oversold bounce
    if rsi < 30 and price < bb_lower and volume > avg_volume * 1.5:
        return {
            'action': 'BUY',
            'size': 0.03,
            'stop_loss': price * 0.97,  # Below recent low
            'take_profit': bb_middle  # Target middle band
        }

    # Overbought fade
    if rsi > 70 and price > bb_upper and volume > avg_volume * 1.5:
        return {
            'action': 'SELL',
            'size': 0.03,
            'stop_loss': price * 1.03,
            'take_profit': bb_middle
        }

    return {'action': 'HOLD'}
```

---

## Monitoring & Optimization

### Daily Checklist

**Morning (Pre-Market):**
- [ ] Check overnight signals
- [ ] Review open positions
- [ ] Check economic calendar
- [ ] Verify system running
- [ ] Check account balances

**During Session:**
- [ ] Monitor P&L
- [ ] Check stop-losses
- [ ] Watch for new signals
- [ ] Note unusual activity

**End of Day:**
- [ ] Log all trades
- [ ] Calculate daily P&L
- [ ] Update performance tracker
- [ ] Identify any issues

### Weekly Review

```markdown
## Week [N] Performance Review

### Metrics
- Total P&L: $X (X%)
- Win Rate: X%
- Sharpe (weekly): X
- Max Drawdown: X%
- Trades Taken: X

### What Worked
- [Strategy/signal that worked well]

### What Didn't Work
- [Strategy/signal that underperformed]

### Signals Missed
- [Opportunities not captured]

### Adjustments for Next Week
- [ ] [Specific adjustment 1]
- [ ] [Specific adjustment 2]
```

### Ralph Loop for Continuous Optimization

**Location:** `ralph/loops/algo_trading/`

```yaml
# prompt.md
schedule: "0 6 * * 1-5"  # 6 AM weekdays

tasks:
  - name: daily_signal_scan
    actions:
      - Scrape trading Twitter accounts
      - Parse signals to signal_log.csv
      - Analyze overnight moves

  - name: performance_check
    actions:
      - Calculate weekly performance
      - Compare to backtest baseline
      - Flag if degradation >10%

  - name: strategy_audit
    actions:
      - Review recent trade outcomes
      - Identify pattern in losses
      - Suggest parameter adjustments
```

---

## Info Product Monetization

### Product Ladder

| Tier | Product | Price | Content |
|------|---------|-------|---------|
| Free | Lead Magnet | $0 | "5 Signals That Predicted..." PDF |
| Entry | Starter Kit | $47 | Signal sources + basic setup |
| Core | Trading System | $197 | Full framework + templates |
| Premium | + Weekly Signals | $297 | System + weekly digest |
| DWY | Setup Service | $997 | 4 calls + custom setup |

### Lead Magnet Ideas

1. "5 Twitter Signals That Predicted Major Market Moves"
2. "The Whale Watching Checklist"
3. "Options Flow Decoder Cheat Sheet"
4. "Crypto On-Chain Signals Quick Reference"

### Content for Core Product

1. Signal source setup guides
2. Python bot templates
3. Risk management spreadsheet
4. Strategy backtesting notebooks
5. Weekly office hours access

---

## Resources & Links

### APIs
- Alpaca: https://alpaca.markets/docs/
- Coinbase: https://docs.cloud.coinbase.com/
- TradingView: https://www.tradingview.com/rest-api-spec/
- Polygon: https://polygon.io/docs/

### Backtesting
- QuantConnect: https://www.quantconnect.com/docs/
- Backtrader: https://www.backtrader.com/docu/
- Freqtrade: https://www.freqtrade.io/en/stable/

### Data
- Unusual Whales: https://unusualwhales.com/
- Glassnode: https://studio.glassnode.com/
- Coinglass: https://www.coinglass.com/
- Arkham: https://platform.arkhamintelligence.com/

### Learning
- QuantStart: https://www.quantstart.com/articles/
- Algorithmic Trading (Ernest Chan)
- Trading Evolved (Andreas Clenow)

---

## Compliance Checklist

- [ ] Include "not financial advice" on all content
- [ ] Include "past performance" disclaimer
- [ ] Never guarantee specific returns
- [ ] Paper trade minimum 4 weeks before recommending live
- [ ] Don't manage other people's money (requires registration)
- [ ] Consult lawyer before scaling

---

**Next Steps:**
1. Set up paper trading accounts (Alpaca + Coinbase)
2. Configure signal sources (Twitter + Unusual Whales)
3. Run trading_signal_scraper.py
4. Build first backtest
5. Document everything

---

*Last Updated: 2026-01-25*
*Status: Research complete, ready for implementation*
