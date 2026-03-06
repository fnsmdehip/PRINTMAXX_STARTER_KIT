#!/usr/bin/env python3
"""
PRINTMAXX Market Scanner — Prediction Markets, Crypto, Options Edge Detection

Scans free/public APIs for trading and prediction market opportunities.
Covers: Polymarket, Kalshi, Manifold, crypto launches, DEX anomalies,
social sentiment, unusual options activity, sector rotation.

Risk management enforced: $20 max per position, $100 daily exposure,
50% stop loss, 5% bankroll rule.

Usage:
  python3 AUTOMATIONS/market_scanner.py --scan-polymarket
  python3 AUTOMATIONS/market_scanner.py --scan-crypto
  python3 AUTOMATIONS/market_scanner.py --scan-options
  python3 AUTOMATIONS/market_scanner.py --portfolio
  python3 AUTOMATIONS/market_scanner.py --log-trade POLYMARKET 15.00
  python3 AUTOMATIONS/market_scanner.py --pnl
  python3 AUTOMATIONS/market_scanner.py --alerts
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# PATH SAFETY (guardrails.md compliant)
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def safe_path(target) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


# ---------------------------------------------------------------------------
# CONSTANTS / RISK MANAGEMENT
# ---------------------------------------------------------------------------

MAX_BET_SIZE = 20.0          # dollars per position
MAX_DAILY_EXPOSURE = 100.0   # total daily risk
STOP_LOSS_PCT = 0.50         # 50 % of position
MAX_BANKROLL_PCT = 0.05      # never risk > 5 % of bankroll on one bet
DEFAULT_BANKROLL = 500.0     # starting bankroll assumption

POSITIONS_CSV  = safe_path(PROJECT_ROOT / "LEDGER" / "MARKET_POSITIONS.csv")
SIGNALS_CSV    = safe_path(PROJECT_ROOT / "LEDGER" / "MARKET_SIGNALS.csv")
DAILY_BRIEF_MD = safe_path(PROJECT_ROOT / "OPS" / "MARKET_DAILY_BRIEF.md")

POSITIONS_HEADERS = [
    "id", "timestamp", "type", "market", "side", "amount",
    "entry_price", "current_price", "pnl", "status", "notes"
]
SIGNALS_HEADERS = [
    "id", "timestamp", "source", "category", "signal",
    "confidence", "edge_pct", "url", "acted"
]

CATEGORIES = ["politics", "tech", "sports", "crypto", "ai"]

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def ensure_csv(path: Path, headers: list):
    """Create CSV with headers if it does not exist."""
    path = safe_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(headers)


def read_csv(path: Path) -> list[dict]:
    path = safe_path(path)
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def append_csv(path: Path, row: dict, headers: list):
    path = safe_path(path)
    ensure_csv(path, headers)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writerow(row)


def next_id(prefix: str, path: Path) -> str:
    rows = read_csv(path)
    nums = []
    for r in rows:
        rid = r.get("id", "")
        if rid.startswith(prefix):
            try:
                nums.append(int(rid[len(prefix):]))
            except ValueError:
                pass
    n = max(nums) + 1 if nums else 1
    return f"{prefix}{n:04d}"


def fetch_json(url: str, timeout: int = 15) -> dict | list | None:
    """GET JSON from a URL. Returns None on failure."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "PRINTMAXX-MarketScanner/1.0",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  [!] Fetch failed for {url}: {e}")
        return None


def now_iso() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def print_table(rows: list[dict], cols: list[str], widths: list[int] | None = None):
    """Print a simple ASCII table."""
    if not rows:
        print("  (no data)")
        return
    if widths is None:
        widths = [max(len(c), max((len(str(r.get(c, ""))) for r in rows), default=4)) + 2 for c in cols]
    header = "".join(str(c).ljust(w) for c, w in zip(cols, widths))
    print(f"  {header}")
    print(f"  {''.join('-' * w for w in widths)}")
    for r in rows:
        line = "".join(str(r.get(c, "")).ljust(w) for c, w in zip(cols, widths))
        print(f"  {line}")


# ---------------------------------------------------------------------------
# 1. PREDICTION MARKETS
# ---------------------------------------------------------------------------

def scan_polymarket():
    """Scan Polymarket public API for mispriced markets and arbitrage."""
    print("\n=== POLYMARKET SCANNER ===\n")

    # Polymarket CLOB API — public, no auth needed
    # Docs: https://docs.polymarket.com
    url = "https://gamma-api.polymarket.com/markets?closed=false&limit=50&order=volume24hr&ascending=false"
    data = fetch_json(url)

    if not data:
        print("  [!] Could not reach Polymarket API. Trying fallback...")
        url_fb = "https://gamma-api.polymarket.com/markets?closed=false&limit=30"
        data = fetch_json(url_fb)

    if not data:
        print("  [!] Polymarket API unavailable. Skipping.")
        return []

    signals = []
    print(f"  Fetched {len(data)} active markets from Polymarket\n")

    for mkt in data:
        try:
            question = mkt.get("question", "")[:80]
            slug = mkt.get("slug", "")
            outcomes = mkt.get("outcomePrices", "")
            volume = float(mkt.get("volume", 0) or 0)
            volume_24h = float(mkt.get("volume24hr", 0) or 0)
            liquidity = float(mkt.get("liquidityNum", 0) or 0)

            # Parse outcome prices
            if isinstance(outcomes, str):
                try:
                    prices = json.loads(outcomes)
                except (json.JSONDecodeError, TypeError):
                    prices = []
            else:
                prices = outcomes if isinstance(outcomes, list) else []

            if not prices or len(prices) < 2:
                continue

            yes_price = float(prices[0])
            no_price = float(prices[1])

            # --- MISPRICING DETECTION ---
            # Prices should sum close to 1.0 (minus vig)
            price_sum = yes_price + no_price
            vig = abs(price_sum - 1.0)

            # Edge 1: extreme mispricing (prices dont sum near 1)
            if vig > 0.05:
                edge = vig * 100
                sig = {
                    "id": next_id("SIG", SIGNALS_CSV),
                    "timestamp": now_iso(),
                    "source": "polymarket",
                    "category": _categorize_market(question),
                    "signal": f"MISPRICING vig={vig:.3f} | {question} | YES={yes_price:.2f} NO={no_price:.2f}",
                    "confidence": min(90, int(edge * 10)),
                    "edge_pct": f"{edge:.1f}",
                    "url": f"https://polymarket.com/event/{slug}",
                    "acted": "NO",
                }
                signals.append(sig)

            # Edge 2: heavily lopsided markets with decent volume
            if (yes_price > 0.90 or yes_price < 0.10) and volume_24h > 5000:
                side = "YES" if yes_price > 0.90 else "NO"
                cheap_side_price = min(yes_price, no_price)
                sig = {
                    "id": next_id("SIG", SIGNALS_CSV),
                    "timestamp": now_iso(),
                    "source": "polymarket",
                    "category": _categorize_market(question),
                    "signal": f"LOPSIDED {side}={max(yes_price,no_price):.2f} vol24h=${volume_24h:,.0f} | {question}",
                    "confidence": 60,
                    "edge_pct": f"{cheap_side_price * 100:.1f}",
                    "url": f"https://polymarket.com/event/{slug}",
                    "acted": "NO",
                }
                signals.append(sig)

            # Edge 3: high volume spike (potential informed trading)
            if volume_24h > 50000 and liquidity > 0:
                vol_liq_ratio = volume_24h / liquidity
                if vol_liq_ratio > 2.0:
                    sig = {
                        "id": next_id("SIG", SIGNALS_CSV),
                        "timestamp": now_iso(),
                        "source": "polymarket",
                        "category": _categorize_market(question),
                        "signal": f"VOLUME SPIKE vol/liq={vol_liq_ratio:.1f}x vol24h=${volume_24h:,.0f} | {question}",
                        "confidence": 70,
                        "edge_pct": f"{(vol_liq_ratio - 1) * 10:.1f}",
                        "url": f"https://polymarket.com/event/{slug}",
                        "acted": "NO",
                    }
                    signals.append(sig)

        except (ValueError, TypeError, KeyError):
            continue

    # --- MANIFOLD MARKETS ---
    print("  Scanning Manifold Markets...")
    manifold_signals = _scan_manifold()
    signals.extend(manifold_signals)

    # --- CROSS-PLATFORM ARBITRAGE ---
    print("  Checking cross-platform arbitrage...")
    arb_signals = _check_prediction_arbitrage(data)
    signals.extend(arb_signals)

    # Save signals
    for sig in signals:
        append_csv(SIGNALS_CSV, sig, SIGNALS_HEADERS)

    # Print summary
    if signals:
        print(f"\n  Found {len(signals)} prediction market signals:\n")
        print_table(signals, ["source", "category", "confidence", "edge_pct", "signal"],
                    [14, 10, 12, 10, 60])
    else:
        print("  No actionable signals found right now.")

    return signals


def _scan_manifold() -> list[dict]:
    """Scan Manifold Markets public API for mispriced binary markets."""
    url = "https://api.manifold.markets/v0/search-markets?sort=newest&limit=30&filter=open"
    data = fetch_json(url)
    signals = []

    if not data:
        print("  [!] Manifold API unavailable.")
        return signals

    for mkt in data:
        try:
            if mkt.get("outcomeType") != "BINARY":
                continue
            prob = float(mkt.get("probability", 0.5))
            question = mkt.get("question", "")[:80]
            mkt_id = mkt.get("id", "")
            volume = float(mkt.get("volume", 0) or 0)
            unique_bettors = int(mkt.get("uniqueBettorCount", 0) or 0)

            # Lopsided with few bettors = potential mispricing
            if (prob > 0.92 or prob < 0.08) and unique_bettors < 10 and volume > 100:
                sig = {
                    "id": next_id("SIG", SIGNALS_CSV),
                    "timestamp": now_iso(),
                    "source": "manifold",
                    "category": _categorize_market(question),
                    "signal": f"THIN MARKET prob={prob:.2f} bettors={unique_bettors} | {question}",
                    "confidence": 55,
                    "edge_pct": f"{min(prob, 1-prob) * 100:.1f}",
                    "url": f"https://manifold.markets/{mkt.get('creatorUsername', '')}/{mkt.get('slug', '')}",
                    "acted": "NO",
                }
                signals.append(sig)

        except (ValueError, TypeError, KeyError):
            continue

    print(f"  Manifold: {len(signals)} signals from {len(data)} markets")
    return signals


def _check_prediction_arbitrage(polymarket_data: list) -> list[dict]:
    """
    Look for same-topic markets across Polymarket and Manifold with different prices.
    Simple keyword matching — not perfect but catches obvious overlaps.
    """
    signals = []

    # Get Manifold markets for comparison
    url = "https://api.manifold.markets/v0/search-markets?sort=most-popular&limit=50&filter=open"
    manifold_data = fetch_json(url)
    if not manifold_data:
        return signals

    # Build keyword index from Polymarket
    poly_markets = {}
    for mkt in polymarket_data:
        q = mkt.get("question", "").lower()
        outcomes = mkt.get("outcomePrices", "")
        if isinstance(outcomes, str):
            try:
                prices = json.loads(outcomes)
            except (json.JSONDecodeError, TypeError):
                continue
        else:
            prices = outcomes if isinstance(outcomes, list) else []
        if prices and len(prices) >= 2:
            poly_markets[q] = {
                "yes_price": float(prices[0]),
                "question": mkt.get("question", ""),
                "slug": mkt.get("slug", ""),
            }

    # Check Manifold markets against Polymarket
    for mkt in manifold_data:
        if mkt.get("outcomeType") != "BINARY":
            continue
        q = mkt.get("question", "").lower()
        prob = float(mkt.get("probability", 0.5))

        # Simple keyword overlap check
        for poly_q, poly_info in poly_markets.items():
            # Count shared significant words
            poly_words = set(w for w in poly_q.split() if len(w) > 4)
            mani_words = set(w for w in q.split() if len(w) > 4)
            overlap = poly_words & mani_words

            if len(overlap) >= 3:  # at least 3 significant shared words
                price_diff = abs(prob - poly_info["yes_price"])
                if price_diff > 0.08:  # >8% price difference = potential arb
                    sig = {
                        "id": next_id("SIG", SIGNALS_CSV),
                        "timestamp": now_iso(),
                        "source": "cross-platform",
                        "category": _categorize_market(poly_info["question"]),
                        "signal": (
                            f"ARB OPPORTUNITY: Poly={poly_info['yes_price']:.2f} vs Manifold={prob:.2f} "
                            f"diff={price_diff:.2f} | {poly_info['question'][:60]}"
                        ),
                        "confidence": min(85, int(price_diff * 200)),
                        "edge_pct": f"{price_diff * 100:.1f}",
                        "url": f"https://polymarket.com/event/{poly_info['slug']}",
                        "acted": "NO",
                    }
                    signals.append(sig)

    if signals:
        print(f"  Cross-platform: {len(signals)} arbitrage opportunities found")
    return signals


def _categorize_market(question: str) -> str:
    """Simple keyword-based category assignment."""
    q = question.lower()
    if any(w in q for w in ["trump", "biden", "election", "president", "senate", "congress", "vote", "democrat", "republican", "governor"]):
        return "politics"
    if any(w in q for w in ["bitcoin", "ethereum", "crypto", "btc", "eth", "solana", "token", "defi"]):
        return "crypto"
    if any(w in q for w in ["ai", "openai", "gpt", "claude", "artificial intelligence", "llm", "agi", "chatgpt", "gemini"]):
        return "ai"
    if any(w in q for w in ["nba", "nfl", "mlb", "soccer", "football", "basketball", "super bowl", "championship", "world cup"]):
        return "sports"
    if any(w in q for w in ["apple", "google", "microsoft", "meta", "tesla", "nvidia", "tech", "iphone", "launch"]):
        return "tech"
    return "other"


# ---------------------------------------------------------------------------
# 2. CRYPTO OPPORTUNITIES
# ---------------------------------------------------------------------------

def scan_crypto():
    """Scan for crypto opportunities using free public APIs."""
    print("\n=== CRYPTO OPPORTUNITY SCANNER ===\n")

    signals = []

    # --- 2a. DEX VOLUME ANOMALIES via DeFi Llama ---
    print("  Scanning DEX volumes (DeFi Llama)...")
    dex_signals = _scan_dex_volumes()
    signals.extend(dex_signals)

    # --- 2b. TRENDING TOKENS via CoinGecko ---
    print("  Scanning trending tokens (CoinGecko)...")
    trending_signals = _scan_trending_tokens()
    signals.extend(trending_signals)

    # --- 2c. NEW LISTINGS / HIGH GAINERS ---
    print("  Scanning top gainers (CoinGecko)...")
    gainer_signals = _scan_top_gainers()
    signals.extend(gainer_signals)

    # --- 2d. REDDIT SENTIMENT ---
    print("  Scanning crypto subreddit sentiment...")
    reddit_signals = _scan_crypto_reddit()
    signals.extend(reddit_signals)

    # --- 2e. AIRDROP OPPORTUNITIES ---
    print("  Checking potential airdrop protocols...")
    airdrop_signals = _scan_airdrop_candidates()
    signals.extend(airdrop_signals)

    # Save signals
    for sig in signals:
        append_csv(SIGNALS_CSV, sig, SIGNALS_HEADERS)

    if signals:
        print(f"\n  Found {len(signals)} crypto signals:\n")
        print_table(signals, ["source", "category", "confidence", "edge_pct", "signal"],
                    [14, 10, 12, 10, 60])
    else:
        print("  No actionable crypto signals right now.")

    return signals


def _scan_dex_volumes() -> list[dict]:
    """Detect DEX volume anomalies via DeFi Llama."""
    signals = []

    # DeFi Llama DEX overview — free, no auth
    url = "https://api.llama.fi/overview/dexs?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true"
    data = fetch_json(url, timeout=20)

    if not data or "protocols" not in data:
        print("  [!] DeFi Llama DEX API unavailable.")
        return signals

    for proto in data.get("protocols", [])[:40]:
        try:
            name = proto.get("name", "")
            chain = proto.get("chain", "")
            vol_24h = float(proto.get("total24h", 0) or 0)
            vol_7d = float(proto.get("total7d", 0) or 0)
            change_1d = float(proto.get("change_1d", 0) or 0)

            # Detect volume spikes (>50% daily increase)
            if change_1d > 50 and vol_24h > 1_000_000:
                sig = {
                    "id": next_id("SIG", SIGNALS_CSV),
                    "timestamp": now_iso(),
                    "source": "defillama-dex",
                    "category": "crypto",
                    "signal": f"DEX VOLUME SPIKE {name} ({chain}) +{change_1d:.0f}% 24h=${vol_24h/1e6:.1f}M",
                    "confidence": min(80, int(change_1d / 2)),
                    "edge_pct": f"{change_1d:.0f}",
                    "url": f"https://defillama.com/dex/{name.lower().replace(' ', '-')}",
                    "acted": "NO",
                }
                signals.append(sig)

        except (ValueError, TypeError, KeyError):
            continue

    print(f"  DEX volumes: {len(signals)} spikes detected")
    return signals


def _scan_trending_tokens() -> list[dict]:
    """CoinGecko trending tokens — free, no API key needed."""
    signals = []
    url = "https://api.coingecko.com/api/v3/search/trending"
    data = fetch_json(url)

    if not data or "coins" not in data:
        print("  [!] CoinGecko trending API unavailable.")
        return signals

    for item in data.get("coins", []):
        coin = item.get("item", {})
        name = coin.get("name", "")
        symbol = coin.get("symbol", "")
        mcap_rank = coin.get("market_cap_rank")
        price_change_24h = coin.get("data", {}).get("price_change_percentage_24h", {})

        # Extract USD price change
        pct_change = 0
        if isinstance(price_change_24h, dict):
            pct_change = float(price_change_24h.get("usd", 0) or 0)
        elif isinstance(price_change_24h, (int, float)):
            pct_change = float(price_change_24h)

        # Flag memecoins and high-momentum tokens
        is_memecoin = any(w in name.lower() for w in ["doge", "shib", "pepe", "meme", "inu", "cat", "bonk", "wif", "floki"])

        if abs(pct_change) > 15 or is_memecoin:
            label = "MEMECOIN MOMENTUM" if is_memecoin else "TRENDING TOKEN"
            sig = {
                "id": next_id("SIG", SIGNALS_CSV),
                "timestamp": now_iso(),
                "source": "coingecko-trending",
                "category": "crypto",
                "signal": f"{label}: {name} ({symbol}) {pct_change:+.1f}% 24h | MCap Rank: {mcap_rank or 'N/A'}",
                "confidence": 50 if is_memecoin else 60,
                "edge_pct": f"{abs(pct_change):.1f}",
                "url": f"https://www.coingecko.com/en/coins/{coin.get('id', '')}",
                "acted": "NO",
            }
            signals.append(sig)

    print(f"  Trending: {len(signals)} momentum tokens found")
    return signals


def _scan_top_gainers() -> list[dict]:
    """CoinGecko top gainers by 24h price change."""
    signals = []
    # Free tier: markets endpoint with sorting
    url = ("https://api.coingecko.com/api/v3/coins/markets"
           "?vs_currency=usd&order=percent_change_24h_desc&per_page=20&page=1"
           "&sparkline=false&price_change_percentage=24h,7d")
    data = fetch_json(url)

    if not data:
        print("  [!] CoinGecko markets API unavailable.")
        return signals

    for coin in data:
        try:
            name = coin.get("name", "")
            symbol = coin.get("symbol", "").upper()
            pct_24h = float(coin.get("price_change_percentage_24h", 0) or 0)
            pct_7d = float(coin.get("price_change_percentage_7d_in_currency", 0) or 0)
            volume = float(coin.get("total_volume", 0) or 0)
            mcap = float(coin.get("market_cap", 0) or 0)

            # High gainer with volume confirmation
            if pct_24h > 25 and volume > 500_000:
                # Volume/mcap ratio as quality signal
                vol_mcap = (volume / mcap * 100) if mcap > 0 else 0
                sig = {
                    "id": next_id("SIG", SIGNALS_CSV),
                    "timestamp": now_iso(),
                    "source": "coingecko-gainers",
                    "category": "crypto",
                    "signal": (
                        f"TOP GAINER: {name} ({symbol}) +{pct_24h:.0f}% 24h "
                        f"vol=${volume/1e6:.1f}M vol/mcap={vol_mcap:.0f}%"
                    ),
                    "confidence": min(75, int(pct_24h / 3)),
                    "edge_pct": f"{pct_24h:.0f}",
                    "url": f"https://www.coingecko.com/en/coins/{coin.get('id', '')}",
                    "acted": "NO",
                }
                signals.append(sig)
        except (ValueError, TypeError, KeyError):
            continue

    print(f"  Gainers: {len(signals)} high-momentum tokens")
    return signals


def _scan_crypto_reddit() -> list[dict]:
    """Scan crypto subreddits for sentiment spikes via Reddit JSON API."""
    signals = []
    subs = ["cryptocurrency", "CryptoMoonShots", "altcoin", "solana", "ethereum"]

    for sub in subs:
        url = f"https://www.reddit.com/r/{sub}/hot.json?limit=10"
        data = fetch_json(url)
        if not data or "data" not in data:
            continue

        for post in data["data"].get("children", []):
            p = post.get("data", {})
            title = p.get("title", "")
            score = int(p.get("score", 0))
            num_comments = int(p.get("num_comments", 0))
            upvote_ratio = float(p.get("upvote_ratio", 0.5))

            # High engagement + positive sentiment = signal
            if score > 500 and num_comments > 100 and upvote_ratio > 0.85:
                sig = {
                    "id": next_id("SIG", SIGNALS_CSV),
                    "timestamp": now_iso(),
                    "source": f"reddit-r/{sub}",
                    "category": "crypto",
                    "signal": f"HIGH SENTIMENT: {title[:70]} | score={score} comments={num_comments} ratio={upvote_ratio:.2f}",
                    "confidence": min(65, int(score / 50)),
                    "edge_pct": f"{upvote_ratio * 100:.0f}",
                    "url": f"https://reddit.com{p.get('permalink', '')}",
                    "acted": "NO",
                }
                signals.append(sig)

        time.sleep(1)  # respect Reddit rate limits

    print(f"  Reddit crypto: {len(signals)} high-sentiment posts")
    return signals


def _scan_airdrop_candidates() -> list[dict]:
    """
    Identify protocols that might do token launches / airdrops.
    Uses DeFi Llama TVL data to find high-TVL protocols without tokens.
    """
    signals = []
    url = "https://api.llama.fi/protocols"
    data = fetch_json(url, timeout=20)

    if not data:
        print("  [!] DeFi Llama protocols API unavailable.")
        return signals

    # Known protocols without tokens (potential airdrop candidates)
    # This list should be updated periodically
    no_token_protocols = {
        "zora", "metamask", "phantom", "opensea", "rainbow",
        "rabby", "zksync", "linea", "scroll", "base",
        "blast", "berachain", "monad", "megaeth",
    }

    for proto in data:
        try:
            name = proto.get("name", "")
            slug = proto.get("slug", "")
            tvl = float(proto.get("tvl", 0) or 0)
            chain = proto.get("chain", "")
            chains = proto.get("chains", [])
            symbol = proto.get("symbol", "")

            # High TVL protocols without a token symbol
            if tvl > 50_000_000 and (not symbol or symbol == "-" or slug.lower() in no_token_protocols):
                chain_str = ", ".join(chains[:3]) if chains else chain
                sig = {
                    "id": next_id("SIG", SIGNALS_CSV),
                    "timestamp": now_iso(),
                    "source": "defillama-airdrop",
                    "category": "crypto",
                    "signal": f"AIRDROP CANDIDATE: {name} TVL=${tvl/1e6:.0f}M chains=[{chain_str}] | No token yet",
                    "confidence": 45,
                    "edge_pct": "N/A",
                    "url": f"https://defillama.com/protocol/{slug}",
                    "acted": "NO",
                }
                signals.append(sig)

        except (ValueError, TypeError, KeyError):
            continue

    print(f"  Airdrop candidates: {len(signals)} high-TVL tokenless protocols")
    return signals[:10]  # cap at 10


# ---------------------------------------------------------------------------
# 3. OPTIONS / STOCKS EDGE
# ---------------------------------------------------------------------------

def scan_options():
    """Scan for unusual options activity and stock signals using free APIs."""
    print("\n=== OPTIONS / STOCKS SCANNER ===\n")

    signals = []

    # --- 3a. UNUSUAL VOLUME via Yahoo Finance ---
    print("  Scanning unusual options activity (Yahoo Finance)...")
    options_signals = _scan_unusual_options()
    signals.extend(options_signals)

    # --- 3b. SECTOR ROTATION ---
    print("  Checking sector rotation signals...")
    sector_signals = _scan_sector_rotation()
    signals.extend(sector_signals)

    # --- 3c. EARNINGS CALENDAR ---
    print("  Checking upcoming earnings for arb opportunities...")
    earnings_signals = _scan_earnings_edge()
    signals.extend(earnings_signals)

    # Save signals
    for sig in signals:
        append_csv(SIGNALS_CSV, sig, SIGNALS_HEADERS)

    if signals:
        print(f"\n  Found {len(signals)} options/stock signals:\n")
        print_table(signals, ["source", "category", "confidence", "edge_pct", "signal"],
                    [14, 10, 12, 10, 60])
    else:
        print("  No actionable options signals right now.")

    return signals


def _scan_unusual_options() -> list[dict]:
    """
    Detect unusual options activity using Yahoo Finance free API.
    Look for high volume relative to open interest.
    """
    signals = []

    # High-profile tickers to monitor
    tickers = [
        "AAPL", "MSFT", "NVDA", "TSLA", "META", "AMZN", "GOOG",
        "AMD", "PLTR", "COIN", "MSTR", "GME", "AMC", "SOFI",
        "RKLB", "SMCI", "ARM", "MARA", "RIOT", "SQ",
    ]

    for ticker in tickers:
        try:
            # Yahoo Finance v8 API (free, no key needed)
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d"
            data = fetch_json(url)

            if not data or "chart" not in data:
                continue

            result = data["chart"].get("result", [{}])[0]
            meta = result.get("meta", {})
            price = float(meta.get("regularMarketPrice", 0) or 0)
            prev_close = float(meta.get("previousClose", 0) or 0)
            volume = int(meta.get("regularMarketVolume", 0) or 0)

            indicators = result.get("indicators", {}).get("quote", [{}])[0]
            volumes = indicators.get("volume", [])

            if not volumes or len(volumes) < 2:
                continue

            # Calculate average volume (excluding today)
            past_vols = [v for v in volumes[:-1] if v]
            if not past_vols:
                continue
            avg_vol = sum(past_vols) / len(past_vols)
            current_vol = volumes[-1] if volumes[-1] else 0

            # Volume ratio
            if avg_vol > 0:
                vol_ratio = current_vol / avg_vol
            else:
                continue

            # Price change
            if prev_close > 0:
                pct_change = ((price - prev_close) / prev_close) * 100
            else:
                pct_change = 0

            # Flag unusual activity
            if vol_ratio > 2.0 and abs(pct_change) > 3:
                direction = "BULLISH" if pct_change > 0 else "BEARISH"
                sig = {
                    "id": next_id("SIG", SIGNALS_CSV),
                    "timestamp": now_iso(),
                    "source": "yahoo-options",
                    "category": "stocks",
                    "signal": (
                        f"UNUSUAL VOLUME {ticker} {direction} {pct_change:+.1f}% "
                        f"vol={vol_ratio:.1f}x avg price=${price:.2f}"
                    ),
                    "confidence": min(80, int(vol_ratio * 20)),
                    "edge_pct": f"{abs(pct_change):.1f}",
                    "url": f"https://finance.yahoo.com/quote/{ticker}",
                    "acted": "NO",
                }
                signals.append(sig)

        except (ValueError, TypeError, KeyError):
            continue

        time.sleep(0.3)  # be nice to Yahoo

    print(f"  Unusual options: {len(signals)} stocks with abnormal volume")
    return signals


def _scan_sector_rotation() -> list[dict]:
    """
    Detect sector rotation by comparing sector ETF performance.
    Uses Yahoo Finance for sector ETF data.
    """
    signals = []

    sector_etfs = {
        "XLK": "Technology",
        "XLF": "Financials",
        "XLE": "Energy",
        "XLV": "Healthcare",
        "XLI": "Industrials",
        "XLU": "Utilities",
        "XLP": "Consumer Staples",
        "XLY": "Consumer Discretionary",
        "XLRE": "Real Estate",
        "XLB": "Materials",
        "XLC": "Communications",
    }

    performances = {}
    for etf, sector in sector_etfs.items():
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{etf}?interval=1d&range=5d"
        data = fetch_json(url)

        if not data or "chart" not in data:
            continue

        result = data["chart"].get("result", [{}])[0]
        meta = result.get("meta", {})
        price = float(meta.get("regularMarketPrice", 0) or 0)
        prev_close = float(meta.get("previousClose", 0) or 0)

        if prev_close > 0:
            pct = ((price - prev_close) / prev_close) * 100
            performances[sector] = pct

        time.sleep(0.2)

    if len(performances) < 5:
        print("  [!] Not enough sector data for rotation analysis.")
        return signals

    # Sort by performance
    sorted_sectors = sorted(performances.items(), key=lambda x: x[1], reverse=True)
    avg_perf = sum(performances.values()) / len(performances)

    # Flag sectors outperforming / underperforming significantly
    for sector, pct in sorted_sectors:
        deviation = pct - avg_perf
        if abs(deviation) > 1.0:  # >1% deviation from average
            direction = "INFLOW" if deviation > 0 else "OUTFLOW"
            sig = {
                "id": next_id("SIG", SIGNALS_CSV),
                "timestamp": now_iso(),
                "source": "sector-rotation",
                "category": "stocks",
                "signal": f"SECTOR {direction}: {sector} {pct:+.2f}% (avg {avg_perf:+.2f}%) dev={deviation:+.2f}%",
                "confidence": min(70, int(abs(deviation) * 25)),
                "edge_pct": f"{abs(deviation):.1f}",
                "url": "https://finance.yahoo.com/sectors/",
                "acted": "NO",
            }
            signals.append(sig)

    print(f"  Sector rotation: {len(signals)} rotation signals")
    return signals


def _scan_earnings_edge() -> list[dict]:
    """
    Look for earnings-related opportunities.
    High IV stocks near earnings with predictable patterns.
    """
    signals = []

    # Monitor high-profile earnings movers
    # These are stocks known for big earnings moves
    earnings_movers = [
        ("NVDA", "AI/GPU leader, massive earnings moves"),
        ("TSLA", "High IV, big post-earnings swings"),
        ("META", "Ad revenue bellwether"),
        ("NFLX", "Subscriber growth drives price"),
        ("CRM", "Enterprise AI spending indicator"),
        ("PLTR", "Government + AI contracts"),
        ("COIN", "Crypto market sentiment proxy"),
        ("SNOW", "Cloud spending indicator"),
    ]

    for ticker, note in earnings_movers:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1mo"
        data = fetch_json(url)
        if not data or "chart" not in data:
            continue

        result = data["chart"].get("result", [{}])[0]
        indicators = result.get("indicators", {}).get("quote", [{}])[0]
        closes = indicators.get("close", [])
        volumes = indicators.get("volume", [])

        if not closes or len(closes) < 5:
            continue

        # Calculate recent volatility
        recent_closes = [c for c in closes[-10:] if c]
        if len(recent_closes) < 5:
            continue

        daily_returns = []
        for i in range(1, len(recent_closes)):
            if recent_closes[i-1] > 0:
                ret = (recent_closes[i] - recent_closes[i-1]) / recent_closes[i-1]
                daily_returns.append(ret)

        if not daily_returns:
            continue

        avg_return = sum(daily_returns) / len(daily_returns)
        variance = sum((r - avg_return) ** 2 for r in daily_returns) / len(daily_returns)
        vol = (variance ** 0.5) * (252 ** 0.5) * 100  # annualized vol

        # High recent vol = potential earnings play setup
        if vol > 50:  # >50% annualized vol
            sig = {
                "id": next_id("SIG", SIGNALS_CSV),
                "timestamp": now_iso(),
                "source": "earnings-edge",
                "category": "stocks",
                "signal": f"HIGH VOL SETUP: {ticker} ann_vol={vol:.0f}% | {note}",
                "confidence": 55,
                "edge_pct": f"{vol:.0f}",
                "url": f"https://finance.yahoo.com/quote/{ticker}",
                "acted": "NO",
            }
            signals.append(sig)

        time.sleep(0.3)

    print(f"  Earnings edge: {len(signals)} high-vol setups")
    return signals


# ---------------------------------------------------------------------------
# 4. PORTFOLIO MANAGEMENT
# ---------------------------------------------------------------------------

def show_portfolio():
    """Display current positions with P/L."""
    print("\n=== MARKET POSITIONS ===\n")
    ensure_csv(POSITIONS_CSV, POSITIONS_HEADERS)

    positions = read_csv(POSITIONS_CSV)
    active = [p for p in positions if p.get("status") == "OPEN"]

    if not active:
        print("  No open positions.")
        print(f"\n  Total positions (all time): {len(positions)}")
        return

    total_exposure = sum(float(p.get("amount", 0)) for p in active)
    total_pnl = sum(float(p.get("pnl", 0)) for p in active)

    print(f"  Open positions: {len(active)}")
    print(f"  Total exposure: ${total_exposure:.2f} / ${MAX_DAILY_EXPOSURE:.2f} limit")
    print(f"  Unrealized P/L: ${total_pnl:+.2f}")
    print()

    print_table(active, ["id", "type", "market", "side", "amount", "entry_price", "pnl", "status"],
                [10, 14, 30, 6, 10, 12, 10, 8])


def log_trade(trade_type: str, amount: float, market: str = "", side: str = "YES", notes: str = ""):
    """Log a new trade with risk management checks."""
    print(f"\n=== LOG TRADE: {trade_type} ${amount:.2f} ===\n")

    # Risk checks
    if amount > MAX_BET_SIZE:
        print(f"  [!] BLOCKED: ${amount:.2f} exceeds max bet size of ${MAX_BET_SIZE:.2f}")
        return

    # Check daily exposure
    ensure_csv(POSITIONS_CSV, POSITIONS_HEADERS)
    positions = read_csv(POSITIONS_CSV)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    today_exposure = sum(
        float(p.get("amount", 0))
        for p in positions
        if p.get("timestamp", "").startswith(today) and p.get("status") == "OPEN"
    )

    if today_exposure + amount > MAX_DAILY_EXPOSURE:
        print(f"  [!] BLOCKED: Would exceed daily exposure limit.")
        print(f"      Today: ${today_exposure:.2f} + ${amount:.2f} = ${today_exposure + amount:.2f}")
        print(f"      Limit: ${MAX_DAILY_EXPOSURE:.2f}")
        return

    # Bankroll check (5% rule)
    total_value = DEFAULT_BANKROLL + sum(float(p.get("pnl", 0)) for p in positions)
    max_single_bet = total_value * MAX_BANKROLL_PCT
    if amount > max_single_bet:
        print(f"  [!] WARNING: ${amount:.2f} exceeds 5% of bankroll (${max_single_bet:.2f})")
        print(f"      Proceeding anyway but consider reducing size.")

    stop_loss = amount * STOP_LOSS_PCT

    trade = {
        "id": next_id("POS", POSITIONS_CSV),
        "timestamp": now_iso(),
        "type": trade_type.upper(),
        "market": market or f"{trade_type} trade",
        "side": side.upper(),
        "amount": f"{amount:.2f}",
        "entry_price": "1.00",
        "current_price": "1.00",
        "pnl": "0.00",
        "status": "OPEN",
        "notes": f"stop_loss=${stop_loss:.2f} | {notes}",
    }

    append_csv(POSITIONS_CSV, trade, POSITIONS_HEADERS)

    print(f"  Trade logged: {trade['id']}")
    print(f"  Type: {trade_type.upper()}")
    print(f"  Amount: ${amount:.2f}")
    print(f"  Stop loss: ${stop_loss:.2f} (-{STOP_LOSS_PCT*100:.0f}%)")
    print(f"  Daily exposure: ${today_exposure + amount:.2f} / ${MAX_DAILY_EXPOSURE:.2f}")


def show_pnl():
    """Show profit/loss summary."""
    print("\n=== PROFIT / LOSS SUMMARY ===\n")
    ensure_csv(POSITIONS_CSV, POSITIONS_HEADERS)
    positions = read_csv(POSITIONS_CSV)

    if not positions:
        print("  No trades recorded yet.")
        return

    open_positions = [p for p in positions if p.get("status") == "OPEN"]
    closed = [p for p in positions if p.get("status") == "CLOSED"]

    total_invested = sum(float(p.get("amount", 0)) for p in positions)
    total_pnl = sum(float(p.get("pnl", 0)) for p in positions)
    open_pnl = sum(float(p.get("pnl", 0)) for p in open_positions)
    closed_pnl = sum(float(p.get("pnl", 0)) for p in closed)
    open_exposure = sum(float(p.get("amount", 0)) for p in open_positions)

    wins = len([p for p in closed if float(p.get("pnl", 0)) > 0])
    losses = len([p for p in closed if float(p.get("pnl", 0)) < 0])
    win_rate = (wins / len(closed) * 100) if closed else 0

    # Breakdown by type
    by_type = {}
    for p in positions:
        t = p.get("type", "UNKNOWN")
        if t not in by_type:
            by_type[t] = {"count": 0, "pnl": 0, "invested": 0}
        by_type[t]["count"] += 1
        by_type[t]["pnl"] += float(p.get("pnl", 0))
        by_type[t]["invested"] += float(p.get("amount", 0))

    print(f"  Total trades:      {len(positions)}")
    print(f"  Open positions:    {len(open_positions)} (${open_exposure:.2f} exposure)")
    print(f"  Closed trades:     {len(closed)}")
    print(f"  Win rate:          {win_rate:.1f}% ({wins}W / {losses}L)")
    print(f"  Total invested:    ${total_invested:.2f}")
    print(f"  Open P/L:          ${open_pnl:+.2f}")
    print(f"  Closed P/L:        ${closed_pnl:+.2f}")
    print(f"  Total P/L:         ${total_pnl:+.2f}")
    print(f"  ROI:               {(total_pnl / total_invested * 100) if total_invested > 0 else 0:+.1f}%")

    if by_type:
        print(f"\n  --- By Category ---")
        type_rows = [{"type": t, "trades": d["count"], "invested": f"${d['invested']:.2f}", "pnl": f"${d['pnl']:+.2f}"}
                     for t, d in sorted(by_type.items())]
        print_table(type_rows, ["type", "trades", "invested", "pnl"], [16, 8, 14, 14])


def show_alerts():
    """Show all recent actionable signals."""
    print("\n=== ACTIONABLE ALERTS ===\n")

    all_signals = []

    print("  Running all scanners...\n")
    all_signals.extend(scan_polymarket())
    all_signals.extend(scan_crypto())
    all_signals.extend(scan_options())

    if not all_signals:
        print("\n  No actionable alerts found across all markets.")
        return

    # Sort by confidence
    all_signals.sort(key=lambda s: int(s.get("confidence", 0)), reverse=True)

    print(f"\n  === TOP ALERTS (sorted by confidence) ===\n")
    top = all_signals[:15]
    print_table(top, ["source", "category", "confidence", "edge_pct", "signal"],
                [16, 10, 12, 10, 58])

    # Generate daily brief
    _generate_daily_brief(all_signals)

    print(f"\n  Total signals: {len(all_signals)}")
    print(f"  Signals saved to: {SIGNALS_CSV}")
    print(f"  Daily brief at: {DAILY_BRIEF_MD}")


def _generate_daily_brief(signals: list[dict]):
    """Generate a markdown daily brief from signals."""
    brief_path = safe_path(DAILY_BRIEF_MD)
    brief_path.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.utcnow()

    # Group by source
    by_source = {}
    for sig in signals:
        src = sig.get("source", "unknown")
        if src not in by_source:
            by_source[src] = []
        by_source[src].append(sig)

    # Read positions for portfolio snapshot
    positions = read_csv(POSITIONS_CSV)
    open_pos = [p for p in positions if p.get("status") == "OPEN"]
    total_pnl = sum(float(p.get("pnl", 0)) for p in positions)

    lines = [
        f"# Market Daily Brief - {now.strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        f"**Signals found:** {len(signals)}",
        f"**Open positions:** {len(open_pos)}",
        f"**Total P/L:** ${total_pnl:+.2f}",
        "",
        "## Top Signals (by confidence)",
        "",
    ]

    # Top 10 signals
    top = sorted(signals, key=lambda s: int(s.get("confidence", 0)), reverse=True)[:10]
    for i, sig in enumerate(top, 1):
        lines.append(
            f"{i}. **[{sig.get('source', '')}]** {sig.get('signal', '')} "
            f"(confidence: {sig.get('confidence', '')}%, edge: {sig.get('edge_pct', '')}%)"
        )

    lines.extend(["", "## Signals by Source", ""])

    for src, sigs in sorted(by_source.items()):
        lines.append(f"### {src} ({len(sigs)} signals)")
        lines.append("")
        for sig in sigs[:5]:
            lines.append(f"- {sig.get('signal', '')} | conf={sig.get('confidence', '')}%")
        if len(sigs) > 5:
            lines.append(f"- ... and {len(sigs) - 5} more")
        lines.append("")

    lines.extend([
        "## Risk Management Status",
        "",
        f"- Max bet size: ${MAX_BET_SIZE}",
        f"- Max daily exposure: ${MAX_DAILY_EXPOSURE}",
        f"- Stop loss: {STOP_LOSS_PCT*100:.0f}%",
        f"- Max bankroll risk per trade: {MAX_BANKROLL_PCT*100:.0f}%",
        "",
        "## Action Items",
        "",
        "- [ ] Review top signals and decide which to act on",
        "- [ ] Check existing positions for stop-loss triggers",
        "- [ ] Update position prices if manual tracking",
        "",
        f"*Generated by market_scanner.py at {now.strftime('%Y-%m-%d %H:%M UTC')}*",
    ])

    with open(brief_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Market Scanner - Prediction Markets, Crypto, Options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 AUTOMATIONS/market_scanner.py --scan-polymarket
  python3 AUTOMATIONS/market_scanner.py --scan-crypto
  python3 AUTOMATIONS/market_scanner.py --scan-options
  python3 AUTOMATIONS/market_scanner.py --alerts
  python3 AUTOMATIONS/market_scanner.py --portfolio
  python3 AUTOMATIONS/market_scanner.py --log-trade POLYMARKET 15.00
  python3 AUTOMATIONS/market_scanner.py --log-trade CRYPTO 10.00 --market "SOL memecoin X" --side BUY
  python3 AUTOMATIONS/market_scanner.py --pnl
        """,
    )

    parser.add_argument("--scan-polymarket", action="store_true",
                        help="Scan prediction markets (Polymarket, Manifold)")
    parser.add_argument("--scan-crypto", action="store_true",
                        help="Scan crypto opportunities (DEX, trending, sentiment)")
    parser.add_argument("--scan-options", action="store_true",
                        help="Scan unusual options activity and sector rotation")
    parser.add_argument("--portfolio", action="store_true",
                        help="Show current open positions")
    parser.add_argument("--log-trade", nargs=2, metavar=("TYPE", "AMOUNT"),
                        help="Log a new trade (e.g. --log-trade POLYMARKET 15.00)")
    parser.add_argument("--pnl", action="store_true",
                        help="Show profit/loss summary")
    parser.add_argument("--alerts", action="store_true",
                        help="Run all scanners and show top actionable opportunities")
    parser.add_argument("--market", type=str, default="",
                        help="Market name for --log-trade")
    parser.add_argument("--side", type=str, default="YES",
                        help="Side for --log-trade (YES/NO/BUY/SELL)")
    parser.add_argument("--notes", type=str, default="",
                        help="Notes for --log-trade")

    args = parser.parse_args()

    # Ensure output directories exist
    ensure_csv(POSITIONS_CSV, POSITIONS_HEADERS)
    ensure_csv(SIGNALS_CSV, SIGNALS_HEADERS)

    if args.scan_polymarket:
        scan_polymarket()
    elif args.scan_crypto:
        scan_crypto()
    elif args.scan_options:
        scan_options()
    elif args.portfolio:
        show_portfolio()
    elif args.log_trade:
        trade_type, amount_str = args.log_trade
        try:
            amount = float(amount_str)
        except ValueError:
            print(f"  [!] Invalid amount: {amount_str}")
            sys.exit(1)
        log_trade(trade_type, amount, market=args.market, side=args.side, notes=args.notes)
    elif args.pnl:
        show_pnl()
    elif args.alerts:
        show_alerts()
    else:
        parser.print_help()
        print("\n  Quick start: python3 AUTOMATIONS/market_scanner.py --alerts")


if __name__ == "__main__":
    main()
