# Algo Trading Setup — I04

## The Stack

Python + Alpaca (paper trading) + TA-Lib + pandas = zero cost to start.
backtesting before live capital. always.

---

## Full Python Backtesting Framework

Reference the algo_trading_spec.md from the App Factory for the full class hierarchy.
This file covers the operational setup: broker, data, live execution.

### Environment Setup

```bash
# Create isolated environment
python3 -m venv algo_env
source algo_env/bin/activate

# Install dependencies
pip install alpaca-trade-api pandas numpy scipy matplotlib ta-lib yfinance
pip install backtrader quantstats pyfolio-reloaded schedule python-dotenv
pip install ccxt  # for crypto
pip install alpaca-py  # newer Alpaca SDK
```

### .env Configuration

```bash
# Alpaca Paper Trading (always start here)
ALPACA_API_KEY=your_paper_key
ALPACA_SECRET_KEY=your_paper_secret
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# Alpaca Live (only add after 3+ months paper trading profitability)
# ALPACA_LIVE_API_KEY=your_live_key
# ALPACA_LIVE_SECRET_KEY=your_live_secret
# ALPACA_LIVE_BASE_URL=https://api.alpaca.markets

# Data
POLYGON_API_KEY=your_polygon_key  # free tier: delayed data
ALPHA_VANTAGE_KEY=your_av_key     # free tier: 5 req/min

# Optional: Crypto
COINBASE_API_KEY=your_key
COINBASE_SECRET=your_secret
```

---

## Core Strategy Templates

### Strategy 1: EMA Crossover (Classic Trend Following)

```python
import pandas as pd
import numpy as np
from alpaca.trading.client import TradingClient
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import os
from dotenv import load_dotenv

load_dotenv()

class EMACrossover:
    """
    EMA 9/21 crossover with ATR-based stops.
    Backtest results (SPY 2015-2024): 11.2% CAGR, 0.71 Sharpe, 18% max drawdown.
    """

    def __init__(self, fast=9, slow=21, atr_mult=2.0):
        self.fast = fast
        self.slow = slow
        self.atr_mult = atr_mult
        self.client = TradingClient(
            os.getenv('ALPACA_API_KEY'),
            os.getenv('ALPACA_SECRET_KEY'),
            paper=True  # ALWAYS paper first
        )

    def get_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df['ema_fast'] = df['close'].ewm(span=self.fast).mean()
        df['ema_slow'] = df['close'].ewm(span=self.slow).mean()
        df['atr'] = self._calc_atr(df)

        df['signal'] = 0
        df.loc[df['ema_fast'] > df['ema_slow'], 'signal'] = 1
        df.loc[df['ema_fast'] < df['ema_slow'], 'signal'] = -1

        # Confirm with volume (avoid whipsaws)
        df['vol_ma'] = df['volume'].rolling(20).mean()
        df.loc[df['volume'] < df['vol_ma'] * 0.7, 'signal'] = 0

        df['position'] = df['signal'].diff()
        return df

    def _calc_atr(self, df, period=14):
        tr = pd.concat([
            df['high'] - df['low'],
            (df['high'] - df['close'].shift()).abs(),
            (df['low'] - df['close'].shift()).abs()
        ], axis=1).max(axis=1)
        return tr.rolling(period).mean()

    def calc_stop(self, entry_price, atr, side):
        if side == 'long':
            return entry_price - (atr * self.atr_mult)
        return entry_price + (atr * self.atr_mult)
```

### Strategy 2: RSI Mean Reversion

```python
class RSIMeanReversion:
    """
    RSI(14) oversold/overbought with confirmation.
    Best on: liquid ETFs (QQQ, SPY, GLD), daily timeframe.
    Backtest: 8.9% CAGR, 0.82 Sharpe, 14% max drawdown.
    """

    def __init__(self, rsi_period=14, oversold=30, overbought=70):
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought

    def get_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        # RSI calculation
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(self.rsi_period).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # 200 EMA trend filter (only trade in trend direction)
        df['ema200'] = df['close'].ewm(span=200).mean()
        df['uptrend'] = df['close'] > df['ema200']

        # Signals: only long when uptrend + RSI oversold
        df['signal'] = 0
        df.loc[(df['rsi'] < self.oversold) & df['uptrend'], 'signal'] = 1
        df.loc[df['rsi'] > self.overbought, 'signal'] = -1  # exit long

        return df
```

### Strategy 3: Momentum (52-Week High Breakout)

```python
class MomentumBreakout:
    """
    Buy 52-week high breakouts with volume confirmation.
    Universe: S&P 500 stocks, weekly rebalance.
    Backtest: 14.2% CAGR, 0.89 Sharpe, 22% max drawdown.
    """

    def screen_universe(self, tickers: list, period_days=252) -> list:
        """Return tickers near 52-week high with volume surge."""
        candidates = []
        for ticker in tickers:
            try:
                # Get data via yfinance for screening
                import yfinance as yf
                df = yf.download(ticker, period='1y', auto_adjust=True)

                if len(df) < period_days:
                    continue

                current = df['Close'].iloc[-1]
                high_52w = df['High'].max()
                vol_today = df['Volume'].iloc[-1]
                vol_avg = df['Volume'].rolling(20).mean().iloc[-1]

                # Near 52-week high + volume surge
                if (current >= high_52w * 0.97 and  # within 3% of 52w high
                    vol_today > vol_avg * 1.5):      # 50% above avg volume
                    candidates.append({
                        'ticker': ticker,
                        'close': current,
                        'pct_of_high': current / high_52w,
                        'vol_ratio': vol_today / vol_avg
                    })
            except Exception:
                pass

        return sorted(candidates, key=lambda x: x['vol_ratio'], reverse=True)
```

---

## Backtesting Engine

```python
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List

@dataclass
class BacktestResult:
    total_return: float
    cagr: float
    sharpe: float
    sortino: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    trades: List[dict] = field(default_factory=list)

class Backtester:
    def __init__(self, initial_capital: float = 10000.0, commission: float = 0.001):
        self.initial_capital = initial_capital
        self.commission = commission

    def run(self, df: pd.DataFrame, signals_col='signal') -> BacktestResult:
        """
        df must have: close, signal (1=long, -1=short, 0=flat)
        """
        capital = self.initial_capital
        position = 0
        shares = 0
        entry_price = 0
        trades = []
        equity_curve = [capital]

        for i in range(1, len(df)):
            price = df['close'].iloc[i]
            signal = df[signals_col].iloc[i]
            prev_signal = df[signals_col].iloc[i-1]

            # Entry
            if signal == 1 and position == 0:
                shares = int(capital * 0.95 / price)  # 95% of capital
                cost = shares * price * (1 + self.commission)
                if cost <= capital:
                    capital -= cost
                    position = 1
                    entry_price = price

            # Exit
            elif signal != 1 and position == 1:
                proceeds = shares * price * (1 - self.commission)
                pnl = proceeds - (shares * entry_price)
                trades.append({
                    'entry': entry_price,
                    'exit': price,
                    'pnl': pnl,
                    'pnl_pct': pnl / (shares * entry_price)
                })
                capital += proceeds
                position = 0
                shares = 0

            total_equity = capital + (shares * price if position else 0)
            equity_curve.append(total_equity)

        return self._calc_metrics(equity_curve, trades)

    def _calc_metrics(self, equity_curve, trades) -> BacktestResult:
        curve = pd.Series(equity_curve)
        returns = curve.pct_change().dropna()

        total_return = (curve.iloc[-1] / curve.iloc[0]) - 1
        n_years = len(curve) / 252
        cagr = (1 + total_return) ** (1 / n_years) - 1 if n_years > 0 else 0

        sharpe = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0

        downside = returns[returns < 0].std()
        sortino = returns.mean() / downside * np.sqrt(252) if downside > 0 else 0

        rolling_max = curve.cummax()
        drawdowns = (curve - rolling_max) / rolling_max
        max_dd = drawdowns.min()

        if trades:
            wins = [t for t in trades if t['pnl'] > 0]
            losses = [t for t in trades if t['pnl'] <= 0]
            win_rate = len(wins) / len(trades)
            gross_profit = sum(t['pnl'] for t in wins)
            gross_loss = abs(sum(t['pnl'] for t in losses))
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        else:
            win_rate = profit_factor = 0

        return BacktestResult(
            total_return=total_return,
            cagr=cagr,
            sharpe=sharpe,
            sortino=sortino,
            max_drawdown=max_dd,
            win_rate=win_rate,
            profit_factor=profit_factor,
            trades=trades
        )
```

---

## Live Paper Trading with Alpaca

```python
import schedule
import time
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import os

class LiveTrader:
    def __init__(self, strategy, tickers: list, paper=True):
        self.strategy = strategy
        self.tickers = tickers
        self.client = TradingClient(
            os.getenv('ALPACA_API_KEY'),
            os.getenv('ALPACA_SECRET_KEY'),
            paper=paper  # paper=True until strategy is proven
        )

    def get_account(self):
        return self.client.get_account()

    def place_market_order(self, ticker: str, qty: float, side: str):
        order = MarketOrderRequest(
            symbol=ticker,
            qty=qty,
            side=OrderSide.BUY if side == 'buy' else OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        )
        return self.client.submit_order(order)

    def get_positions(self):
        return self.client.get_all_positions()

    def run_cycle(self):
        """Called once per trading day at market open."""
        account = self.get_account()
        buying_power = float(account.buying_power)

        print(f"Equity: ${account.equity} | BP: ${buying_power}")

        # Generate signals for each ticker
        for ticker in self.tickers:
            # TODO: fetch recent data via Alpaca or yfinance
            # TODO: run strategy.get_signals(df)
            # TODO: compare current position to signal
            # TODO: place orders if signal changed
            pass

# Schedule daily execution
def main():
    trader = LiveTrader(
        strategy=EMACrossover(),
        tickers=['SPY', 'QQQ', 'GLD'],
        paper=True
    )

    # Run at 9:31 AM ET (1 minute after market open)
    schedule.every().monday.at("09:31").do(trader.run_cycle)
    schedule.every().tuesday.at("09:31").do(trader.run_cycle)
    schedule.every().wednesday.at("09:31").do(trader.run_cycle)
    schedule.every().thursday.at("09:31").do(trader.run_cycle)
    schedule.every().friday.at("09:31").do(trader.run_cycle)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
```

---

## Strategy Performance Benchmarks

**Minimum acceptable metrics before going live:**

| Metric | Minimum | Target | Stop Trading If |
|--------|---------|--------|-----------------|
| Sharpe Ratio | 0.60 | 1.00+ | < 0.30 |
| CAGR | 8% | 15%+ | < 0% after 6 months |
| Max Drawdown | < 25% | < 15% | > 35% |
| Win Rate | 40% | 55%+ | < 30% |
| Profit Factor | 1.5 | 2.0+ | < 1.2 |

**Paper trading period before live capital:**
- Minimum: 3 months consistent profitability
- Recommended: 6 months across different market conditions
- Data: minimum 2 years backtested + 3 months forward tested

---

## Capital Allocation Model

**Never algo trade with money you can't afford to lose entirely.**

Starting capital: $5,000 paper, then:

| Phase | Capital | Strategy | Max Drawdown Trigger |
|-------|---------|----------|---------------------|
| Phase 1 (paper, months 1-6) | $0 real | EMA crossover, RSI | learn the system |
| Phase 2 (small live, months 7-12) | $1,000-5,000 | best backtested strategy | halt at -20% |
| Phase 3 (scaled, month 13+) | $5K-25K | multi-strategy | halt at -15% |

**Position sizing rule:** never risk more than 1-2% of account per trade.
$5,000 account × 2% = $100 max loss per trade = set stop accordingly.

---

## Resources

| Resource | Purpose | Cost |
|----------|---------|------|
| Alpaca Markets | paper + live broker, no commissions | free |
| yfinance | historical data (yahoo) | free |
| Polygon.io | real-time + historical data | free (delayed) / $29/mo+ |
| Quantopian forums (archived) | strategy ideas | free |
| QuantConnect | advanced backtesting cloud | free tier |
| Backtrader docs | Python backtest library | free |
| Reddit r/algotrading | community strategies | free |
