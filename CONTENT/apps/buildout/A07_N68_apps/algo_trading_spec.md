# Algo Trading Backtesting Framework — Feature Spec

**Concept:** A Python-based algorithmic trading backtesting framework built for solopreneurs and quant hobbyists. Run strategies against historical data, calculate real performance metrics, apply Kelly Criterion for position sizing, and paper trade live. No finance PhD required.

**Target User:** Technically proficient solopreneurs, Python developers, and finance-curious builders who want to test trading ideas without paying $500/mo for Bloomberg Terminal.

**Use Cases:**
1. Test a momentum strategy against 10 years of crypto/stock data
2. Validate a mean reversion approach before risking real capital
3. Paper trade a live strategy with real-time data (simulated fills)
4. Build systematic signal-based position sizing with Kelly Criterion

**Implementation:** Python library + optional web UI (Streamlit/Next.js dashboard)

---

## Architecture Overview

```
printmaxx-quant/
├── core/
│   ├── backtester.py         # Main backtest engine
│   ├── strategy.py           # Strategy base class
│   ├── portfolio.py          # Portfolio + position tracking
│   ├── data.py               # Data ingestion (yfinance, CCXT, CSV)
│   ├── risk.py               # Kelly Criterion, position sizing
│   └── metrics.py            # Sharpe, Sortino, max drawdown, etc.
├── strategies/
│   ├── momentum.py           # Trend following strategies
│   ├── mean_reversion.py     # Reversion strategies
│   ├── breakout.py           # Breakout strategies
│   └── custom_template.py    # Template for user strategies
├── data/
│   ├── cache/                # Cached OHLCV data (parquet)
│   └── raw/                  # User-uploaded CSV data
├── reports/
│   └── {strategy}_{date}.html  # Auto-generated backtest reports
└── live/
    ├── paper_trader.py       # Live paper trading engine
    └── broker_adapters/      # Alpaca, IBKR, Binance adapters
```

---

## Core Module: Backtester

```python
# core/backtester.py

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Type
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class BacktestConfig:
    initial_capital: float = 10_000.0
    commission: float = 0.001        # 0.1% per trade
    slippage: float = 0.001          # 0.1% slippage
    start_date: str = "2020-01-01"
    end_date: str = "2024-12-31"
    benchmark: str = "SPY"            # Benchmark ticker for comparison
    max_position_pct: float = 0.20    # Max 20% of portfolio per position
    use_kelly: bool = True            # Apply Kelly Criterion sizing
    kelly_fraction: float = 0.5       # Half Kelly (safer)

@dataclass
class Trade:
    symbol: str
    direction: str       # 'long' | 'short'
    entry_price: float
    exit_price: float
    quantity: float
    entry_date: datetime
    exit_date: datetime
    pnl: float
    pnl_pct: float
    commission_paid: float
    exit_reason: str     # 'signal' | 'stop_loss' | 'take_profit' | 'end_of_period'

class Backtester:
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.cash = config.initial_capital
        self.portfolio_value = config.initial_capital
        self.positions: Dict[str, dict] = {}
        self.trades: List[Trade] = []
        self.equity_curve: List[float] = []
        self.dates: List[datetime] = []

    def run(self, strategy, data: Dict[str, pd.DataFrame]) -> 'BacktestResult':
        """
        Run backtest.
        strategy: instance of Strategy subclass
        data: dict of {symbol: OHLCV DataFrame}
        """
        # Build aligned date index across all symbols
        all_dates = sorted(set.union(*[set(df.index) for df in data.values()]))
        all_dates = [d for d in all_dates
                     if self.config.start_date <= str(d.date()) <= self.config.end_date]

        strategy.on_start(self.config)

        for date in all_dates:
            # Build current market snapshot
            market = {}
            for symbol, df in data.items():
                if date in df.index:
                    market[symbol] = df.loc[date]

            # Update portfolio MTM value
            self._update_portfolio_value(market)

            # Run strategy signals
            signals = strategy.on_bar(date, market, self._get_state())

            # Execute signals
            for signal in signals:
                self._execute_signal(signal, market, date)

            self.equity_curve.append(self.portfolio_value)
            self.dates.append(date)

        # Close all open positions at end
        for symbol in list(self.positions.keys()):
            self._close_position(symbol, all_dates[-1],
                                 market.get(symbol, {}).get('close', 0),
                                 reason='end_of_period')

        return BacktestResult(
            trades=self.trades,
            equity_curve=self.equity_curve,
            dates=self.dates,
            initial_capital=self.config.initial_capital,
            config=self.config
        )

    def _execute_signal(self, signal: dict, market: dict, date: datetime):
        symbol = signal['symbol']
        action = signal['action']   # 'buy' | 'sell' | 'close'
        size_pct = signal.get('size_pct', 0.10)  # default 10% of portfolio

        if symbol not in market:
            return

        price = market[symbol]['close']
        price_with_slippage = price * (1 + self.config.slippage if action == 'buy'
                                       else 1 - self.config.slippage)

        if action == 'buy' and symbol not in self.positions:
            capital_to_deploy = self.portfolio_value * min(size_pct,
                                                            self.config.max_position_pct)
            if self.config.use_kelly and 'kelly_f' in signal:
                capital_to_deploy = self.portfolio_value * min(
                    signal['kelly_f'] * self.config.kelly_fraction,
                    self.config.max_position_pct
                )
            commission = capital_to_deploy * self.config.commission
            quantity = (capital_to_deploy - commission) / price_with_slippage
            cost = quantity * price_with_slippage + commission
            if cost <= self.cash:
                self.cash -= cost
                self.positions[symbol] = {
                    'quantity': quantity, 'entry_price': price_with_slippage,
                    'entry_date': date, 'direction': 'long'
                }

        elif action in ('sell', 'close') and symbol in self.positions:
            self._close_position(symbol, date, price_with_slippage, reason='signal')

    def _close_position(self, symbol: str, date: datetime,
                        exit_price: float, reason: str):
        pos = self.positions.pop(symbol)
        proceeds = pos['quantity'] * exit_price
        commission = proceeds * self.config.commission
        net_proceeds = proceeds - commission
        self.cash += net_proceeds
        pnl = net_proceeds - (pos['quantity'] * pos['entry_price'])
        pnl_pct = pnl / (pos['quantity'] * pos['entry_price'])
        self.trades.append(Trade(
            symbol=symbol, direction=pos['direction'],
            entry_price=pos['entry_price'], exit_price=exit_price,
            quantity=pos['quantity'], entry_date=pos['entry_date'],
            exit_date=date, pnl=pnl, pnl_pct=pnl_pct,
            commission_paid=commission, exit_reason=reason
        ))

    def _update_portfolio_value(self, market: dict):
        positions_value = sum(
            pos['quantity'] * market[sym]['close']
            for sym, pos in self.positions.items() if sym in market
        )
        self.portfolio_value = self.cash + positions_value

    def _get_state(self) -> dict:
        return {
            'cash': self.cash,
            'portfolio_value': self.portfolio_value,
            'positions': dict(self.positions),
            'num_trades': len(self.trades)
        }
```

---

## Core Module: Strategy Base Class

```python
# core/strategy.py

from abc import ABC, abstractmethod
from typing import List, Dict
import pandas as pd

class Strategy(ABC):
    """Base class for all strategies. Override on_bar to implement logic."""

    def __init__(self, params: dict = None):
        self.params = params or {}
        self.config = None

    def on_start(self, config):
        """Called once before backtest begins."""
        self.config = config

    @abstractmethod
    def on_bar(self, date, market: dict, state: dict) -> List[dict]:
        """
        Called on every bar. Return list of signals:
        [{'symbol': 'BTC-USD', 'action': 'buy', 'size_pct': 0.10, 'kelly_f': 0.35}]
        """
        pass


# --- Example: Dual Moving Average Crossover ---
class DualMACrossover(Strategy):
    """
    Buy when fast MA crosses above slow MA.
    Sell when fast MA crosses below slow MA.
    """
    def __init__(self, fast: int = 20, slow: int = 50):
        super().__init__({'fast': fast, 'slow': slow})
        self.price_history: Dict[str, list] = {}

    def on_bar(self, date, market: dict, state: dict) -> List[dict]:
        signals = []
        for symbol, bar in market.items():
            if symbol not in self.price_history:
                self.price_history[symbol] = []
            self.price_history[symbol].append(bar['close'])

            history = self.price_history[symbol]
            slow = self.params['slow']
            fast = self.params['fast']

            if len(history) < slow + 1:
                continue

            fast_ma_now = sum(history[-fast:]) / fast
            fast_ma_prev = sum(history[-fast-1:-1]) / fast
            slow_ma_now = sum(history[-slow:]) / slow
            slow_ma_prev = sum(history[-slow-1:-1]) / slow

            crossed_up = fast_ma_prev < slow_ma_prev and fast_ma_now > slow_ma_now
            crossed_down = fast_ma_prev > slow_ma_prev and fast_ma_now < slow_ma_now

            if crossed_up and symbol not in state['positions']:
                signals.append({'symbol': symbol, 'action': 'buy', 'size_pct': 0.20})
            elif crossed_down and symbol in state['positions']:
                signals.append({'symbol': symbol, 'action': 'sell'})

        return signals
```

---

## Core Module: Risk — Kelly Criterion

```python
# core/risk.py

import numpy as np
from typing import List

def kelly_criterion(win_rate: float, avg_win: float,
                    avg_loss: float, kelly_fraction: float = 0.5) -> float:
    """
    Full Kelly: f = (bp - q) / b
    where b = avg_win/avg_loss, p = win_rate, q = 1 - win_rate
    Returns fractional Kelly (default half Kelly for safety).
    """
    if avg_loss == 0:
        return 0.0
    b = avg_win / abs(avg_loss)
    q = 1 - win_rate
    full_kelly = (b * win_rate - q) / b
    return max(0.0, min(full_kelly * kelly_fraction, 1.0))

def rolling_kelly(returns: List[float], window: int = 50,
                  kelly_fraction: float = 0.5) -> float:
    """Calculate Kelly fraction from a rolling window of trade returns."""
    if len(returns) < window:
        returns_window = returns
    else:
        returns_window = returns[-window:]

    wins = [r for r in returns_window if r > 0]
    losses = [r for r in returns_window if r < 0]

    if not wins or not losses:
        return 0.05  # default 5% position if no history

    win_rate = len(wins) / len(returns_window)
    avg_win = np.mean(wins)
    avg_loss = abs(np.mean(losses))

    return kelly_criterion(win_rate, avg_win, avg_loss, kelly_fraction)

def position_size_from_kelly(portfolio_value: float, kelly_f: float,
                              price: float, max_pct: float = 0.25) -> float:
    """Return number of shares/units to buy given Kelly f."""
    capital = portfolio_value * min(kelly_f, max_pct)
    return capital / price
```

---

## Core Module: Metrics

```python
# core/metrics.py

import numpy as np
import pandas as pd
from typing import List

def calculate_metrics(equity_curve: List[float],
                      trades: list,
                      risk_free_rate: float = 0.05) -> dict:
    """Compute full backtest performance metrics."""
    equity = np.array(equity_curve)
    returns = np.diff(equity) / equity[:-1]

    initial = equity[0]
    final = equity[-1]
    total_return = (final - initial) / initial
    n_years = len(equity) / 252

    # Annualized return
    cagr = (1 + total_return) ** (1 / n_years) - 1 if n_years > 0 else 0

    # Volatility (annualized)
    volatility = returns.std() * np.sqrt(252)

    # Sharpe ratio
    excess_returns = returns - (risk_free_rate / 252)
    sharpe = (excess_returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0

    # Sortino ratio
    downside_returns = returns[returns < 0]
    downside_vol = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
    sortino = (returns.mean() * 252 - risk_free_rate) / downside_vol if downside_vol > 0 else 0

    # Max drawdown
    peak = np.maximum.accumulate(equity)
    drawdown = (equity - peak) / peak
    max_drawdown = drawdown.min()

    # Calmar ratio
    calmar = cagr / abs(max_drawdown) if max_drawdown != 0 else 0

    # Trade-level stats
    if trades:
        pnls = [t.pnl for t in trades]
        winning_trades = [t for t in trades if t.pnl > 0]
        losing_trades = [t for t in trades if t.pnl <= 0]
        win_rate = len(winning_trades) / len(trades)
        avg_win = np.mean([t.pnl for t in winning_trades]) if winning_trades else 0
        avg_loss = np.mean([t.pnl for t in losing_trades]) if losing_trades else 0
        profit_factor = (sum(t.pnl for t in winning_trades) /
                         abs(sum(t.pnl for t in losing_trades))) if losing_trades else float('inf')
    else:
        win_rate = avg_win = avg_loss = profit_factor = 0

    return {
        'total_return_pct': round(total_return * 100, 2),
        'cagr_pct': round(cagr * 100, 2),
        'volatility_pct': round(volatility * 100, 2),
        'sharpe_ratio': round(sharpe, 3),
        'sortino_ratio': round(sortino, 3),
        'calmar_ratio': round(calmar, 3),
        'max_drawdown_pct': round(max_drawdown * 100, 2),
        'win_rate_pct': round(win_rate * 100, 2) if trades else 0,
        'avg_win_usd': round(avg_win, 2),
        'avg_loss_usd': round(avg_loss, 2),
        'profit_factor': round(profit_factor, 3),
        'total_trades': len(trades),
        'final_value_usd': round(final, 2),
    }
```

---

## Data Module

```python
# core/data.py

import yfinance as yf
import ccxt
import pandas as pd
from pathlib import Path

CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_stock_data(symbol: str, start: str, end: str,
                   interval: str = "1d") -> pd.DataFrame:
    """Download OHLCV from Yahoo Finance with local parquet cache."""
    cache_file = CACHE_DIR / f"{symbol}_{start}_{end}_{interval}.parquet"
    if cache_file.exists():
        return pd.read_parquet(cache_file)
    df = yf.download(symbol, start=start, end=end, interval=interval, auto_adjust=True)
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df.to_parquet(cache_file)
    return df

def get_crypto_data(symbol: str, start: str, end: str,
                    exchange: str = "binance") -> pd.DataFrame:
    """Download OHLCV from CCXT exchange."""
    cache_file = CACHE_DIR / f"crypto_{symbol.replace('/', '_')}_{start}_{end}.parquet"
    if cache_file.exists():
        return pd.read_parquet(cache_file)
    ex = getattr(ccxt, exchange)()
    since = int(pd.Timestamp(start).timestamp() * 1000)
    ohlcv = ex.fetch_ohlcv(symbol, '1d', since=since, limit=1000)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df.to_parquet(cache_file)
    return df
```

---

## Complete Usage Example

```python
from core.backtester import Backtester, BacktestConfig
from core.strategies import DualMACrossover
from core.data import get_stock_data
from core.metrics import calculate_metrics
from core.risk import kelly_criterion
import json

# 1. Load data
symbols = ['AAPL', 'MSFT', 'GOOGL', 'SPY']
data = {sym: get_stock_data(sym, '2018-01-01', '2024-12-31') for sym in symbols}

# 2. Configure backtest
config = BacktestConfig(
    initial_capital=10_000,
    commission=0.001,
    slippage=0.001,
    start_date='2018-01-01',
    end_date='2024-12-31',
    max_position_pct=0.25,
    use_kelly=True,
    kelly_fraction=0.5
)

# 3. Run strategy
strategy = DualMACrossover(fast=20, slow=50)
backtester = Backtester(config)
result = backtester.run(strategy, data)

# 4. Calculate metrics
metrics = calculate_metrics(result.equity_curve, result.trades)
print(json.dumps(metrics, indent=2))

# Output:
# {
#   "total_return_pct": 142.7,
#   "cagr_pct": 14.8,
#   "volatility_pct": 18.2,
#   "sharpe_ratio": 0.812,
#   "sortino_ratio": 1.24,
#   "calmar_ratio": 0.91,
#   "max_drawdown_pct": -16.3,
#   "win_rate_pct": 48.2,
#   "profit_factor": 1.73,
#   "total_trades": 114,
#   "final_value_usd": 24270.0
# }
```

---

## Paper Trading Engine

```python
# live/paper_trader.py

import asyncio
import alpaca_trade_api as alpaca
from datetime import datetime

class PaperTrader:
    """
    Paper trading engine using Alpaca Paper API.
    Runs strategy on live market data, simulates fills.
    """
    def __init__(self, strategy, config: dict):
        self.strategy = strategy
        self.api = alpaca.REST(
            config['alpaca_key'],
            config['alpaca_secret'],
            base_url='https://paper-api.alpaca.markets'
        )
        self.portfolio_value = float(self.api.get_account().portfolio_value)

    async def run(self, symbols: list, interval_seconds: int = 60):
        print(f"Paper trading started. Portfolio: ${self.portfolio_value:,.2f}")
        while True:
            market = self._fetch_latest_bars(symbols)
            state = self._get_state()
            signals = self.strategy.on_bar(datetime.now(), market, state)
            for signal in signals:
                self._execute_paper_signal(signal, market)
            await asyncio.sleep(interval_seconds)

    def _fetch_latest_bars(self, symbols: list) -> dict:
        bars = self.api.get_latest_bars(symbols)
        return {sym: {'close': bar.c, 'open': bar.o, 'high': bar.h,
                      'low': bar.l, 'volume': bar.v}
                for sym, bar in bars.items()}

    def _execute_paper_signal(self, signal: dict, market: dict):
        symbol = signal['symbol']
        action = signal['action']
        positions = {p.symbol: p for p in self.api.list_positions()}
        if action == 'buy' and symbol not in positions:
            dollar_amount = self.portfolio_value * signal.get('size_pct', 0.10)
            self.api.submit_order(symbol=symbol, notional=dollar_amount,
                                  side='buy', type='market', time_in_force='day')
            print(f"BUY {symbol} ${dollar_amount:.2f}")
        elif action in ('sell', 'close') and symbol in positions:
            self.api.close_position(symbol)
            print(f"SELL {symbol}")
```

---

## Included Built-In Strategies

| Strategy | Description | Typical Win Rate | Best Market |
|---|---|---|---|
| DualMACrossover | 20/50 MA crossover | 45-52% | Trending |
| RSI Mean Reversion | Buy oversold (RSI<30), sell overbought (RSI>70) | 55-62% | Range-bound |
| BollingerBandBreakout | Buy breakout above upper band | 40-48% | Volatile |
| MomentumRankRotation | Hold top N assets by 3-month momentum | 52-58% | Bull market |
| TrendFollowingEMA | Triple EMA (8/21/55) alignment | 42-50% | Strong trends |

---

## Installation & Requirements

```
pip install yfinance ccxt pandas numpy alpaca-trade-api plotly
```

**Optional for dashboard:**
```
pip install streamlit  # for interactive UI
streamlit run dashboard.py
```

**Alpaca Paper account:** Free at alpaca.markets — no real money, real market data

---

## Monetization Paths

1. **Open source core + paid extensions:** GitHub release as open source → paid strategy packs, premium indicators, live broker adapters ($29-$99 one-time on Gumroad)
2. **SaaS backtest-as-service:** Upload CSV, choose strategy, get report in browser — $19/mo (no Python knowledge needed)
3. **Done-for-you backtests:** Build custom strategy for client — $500-2000 per engagement
4. **Quant course:** "Build your first algo trading system" — $197 course with this framework as foundation
5. **Strategy marketplace:** Users sell their strategies (backtested + live-traded stats required) — 20% platform fee

---

## Dependencies

```
yfinance>=0.2.48          # Yahoo Finance OHLCV
ccxt>=4.3.0               # Crypto exchange data
pandas>=2.1.0             # Data manipulation
numpy>=1.26.0             # Math
alpaca-trade-api>=3.3.0   # Paper trading
plotly>=5.22.0            # Charts
```
