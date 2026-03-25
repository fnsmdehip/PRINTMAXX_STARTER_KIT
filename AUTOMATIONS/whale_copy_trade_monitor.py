#!/usr/bin/env python3
"""
PRINTMAXX Automation: Whale Copy-Trade Monitor
Monitors hypurrscan.io and on-chain perps analytics APIs for whale copy-trade
events (large position opens >$1M that mirror another tracked wallet), extracts
key metrics (size, asset, P&L), generates engagement content, and routes to the
posting queue.
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: try importing from _common, fall back to local definitions
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path: Path) -> Path:
        """Validate that *path* resolves inside PROJECT; raise ValueError otherwise."""
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(PROJECT.resolve())
        except ValueError:
            raise ValueError(
                f"Path '{resolved}' escapes PROJECT root '{PROJECT}'. Refusing to proceed."
            )
        return resolved

    def recall_skills_for_task(task: str) -> list:
        return []

    def capture_skill_from_result(result: dict) -> None:
        pass


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_FILE = AUTOMATIONS_DIR / "logs" / "whale_copy_trade_monitor.log"
QUEUE_DIR = AUTOMATIONS_DIR / "queue"
STATE_FILE = AUTOMATIONS_DIR / "state" / "whale_copy_trade_state.json"
EVENTS_CSV = AUTOMATIONS_DIR / "data" / "whale_copy_trade_events.csv"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCRIPT_NAME = "whale_copy_trade_monitor"
MIN_POSITION_USD = 1_000_000          # $1M threshold
HYPURRSCAN_API = "https://hypurrscan.io/api"
# Tracked "originator" wallets whose trades trigger copy-trade detection
TRACKED_WALLETS: list[str] = [
    "0xRuneKek",   # placeholder – replace with real checksummed addresses
]
# Time window (seconds) within which a mirroring trade is considered a copy
COPY_WINDOW_SECONDS = 300

CSV_HEADERS = [
    "event_id", "detected_at", "copier_wallet", "originator_wallet",
    "asset", "direction", "size_contracts", "size_usd", "entry_price",
    "pnl_usd", "pnl_pct", "status", "posted",
]

# ---------------------------------------------------------------------------
# Logging setup  (must run before any logger usage)
# ---------------------------------------------------------------------------

def _setup_logging() -> logging.Logger:
    safe_path(LOG_FILE.parent).mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(SCRIPT_NAME)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(safe_path(LOG_FILE), mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%SZ")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(fmt)
        logger.addHandler(sh)
    return logger


log = _setup_logging()

# ---------------------------------------------------------------------------
# Directory bootstrap
# ---------------------------------------------------------------------------

def _ensure_dirs() -> None:
    for d in [
        AUTOMATIONS_DIR / "logs",
        AUTOMATIONS_DIR / "queue",
        AUTOMATIONS_DIR / "state",
        AUTOMATIONS_DIR / "data",
    ]:
        safe_path(d).mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

def _load_state() -> dict:
    try:
        p = safe_path(STATE_FILE)
        if p.exists():
            with open(p, "r", encoding="utf-8") as fh:
                return json.load(fh)
    except Exception as exc:
        log.warning("Could not load state: %s", exc)
    return {"last_run": None, "seen_event_ids": [], "posted_event_ids": []}


def _save_state(state: dict) -> None:
    try:
        p = safe_path(STATE_FILE)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2)
    except Exception as exc:
        log.error("Could not save state: %s", exc)


# ---------------------------------------------------------------------------
# CSV event log
# ---------------------------------------------------------------------------

def _append_events_csv(events: list[dict]) -> None:
    if not events:
        return
    try:
        p = safe_path(EVENTS_CSV)
        write_header = not p.exists()
        with open(p, "a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=CSV_HEADERS, extrasaction="ignore")
            if write_header:
                writer.writeheader()
            for ev in events:
                writer.writerow({k: ev.get(k, "") for k in CSV_HEADERS})
        log.debug("Appended %d event(s) to CSV.", len(events))
    except Exception as exc:
        log.error("CSV append failed: %s", exc)


# ---------------------------------------------------------------------------
# HTTP helper (stdlib only)
# ---------------------------------------------------------------------------

def _fetch_json(url: str, timeout: int = 20) -> dict | list | None:
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "PRINTMAXX-WhaleCopyMonitor/1.0",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        log.warning("HTTP %s fetching %s: %s", exc.code, url, exc.reason)
    except urllib.error.URLError as exc:
        log.warning("URL error fetching %s: %s", url, exc.reason)
    except json.JSONDecodeError as exc:
        log.warning("JSON decode error from %s: %s", url, exc)
    except Exception as exc:
        log.error("Unexpected error fetching %s: %s", url, exc)
    return None


# ---------------------------------------------------------------------------
# API wrappers
# ---------------------------------------------------------------------------

def _fetch_recent_positions() -> list[dict]:
    """
    Fetch recent large perpetuals positions from hypurrscan.io.
    Returns a list of raw position dicts.
    """
    url = f"{HYPURRSCAN_API}/positions/recent?min_usd={MIN_POSITION_USD}&limit=200"
    data = _fetch_json(url)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "positions" in data:
        return data["positions"]
    log.warning("Unexpected positions payload structure.")
    return []


def _fetch_wallet_positions(wallet: str) -> list[dict]:
    """Fetch recent positions for a specific tracked wallet."""
    url = f"{HYPURRSCAN_API}/wallet/{wallet}/positions?limit=50"
    data = _fetch_json(url)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "positions" in data:
        return data["positions"]
    return []


# ---------------------------------------------------------------------------
# Copy-trade detection logic
# ---------------------------------------------------------------------------

def _parse_ts(ts_str: str) -> datetime | None:
    """Parse ISO-8601 or epoch timestamp string to aware UTC datetime."""
    if not ts_str:
        return None
    try:
        # epoch int/float as string
        return datetime.fromtimestamp(float(ts_str), tz=timezone.utc)
    except (ValueError, TypeError):
        pass
    try:
        ts_str = ts_str.rstrip("Z")
        return datetime.fromisoformat(ts_str).replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _position_size_usd(pos: dict) -> float:
    """Best-effort USD size extraction from a position dict."""
    for key in ("size_usd", "notional_usd", "value_usd", "usd_size"):
        if key in pos:
            try:
                return float(pos[key])
            except (TypeError, ValueError):
                pass
    # fallback: contracts * price
    try:
        return float(pos.get("size", 0)) * float(pos.get("entry_price", 0))
    except (TypeError, ValueError):
        return 0.0


def _detect_copy_trades(
    all_positions: list[dict],
    originator_positions: dict[str, list[dict]],
    already_seen: set[str],
) -> list[dict]:
    """
    Identify positions in *all_positions* that:
      - Are opened within COPY_WINDOW_SECONDS of a tracked wallet's position
      - Match the same asset and direction
      - Exceed MIN_POSITION_USD
      - Have not been seen before
    """
    now = datetime.now(tz=timezone.utc)
    events: list[dict] = []

    for pos in all_positions:
        wallet = str(pos.get("wallet", pos.get("address", ""))).lower()
        if not wallet or wallet in [w.lower() for w in TRACKED_WALLETS]:
            continue

        size_usd = _position_size_usd(pos)
        if size_usd < MIN_POSITION_USD:
            continue

        pos_ts = _parse_ts(str(pos.get("opened_at", pos.get("timestamp", ""))))
        if pos_ts is None:
            continue

        asset = str(pos.get("asset", pos.get("market", "UNKNOWN"))).upper()
        direction = str(pos.get("direction", pos.get("side", "LONG"))).upper()

        for orig_wallet, orig_positions in originator_positions.items():
            for orig_pos in orig_positions:
                orig_asset = str(orig_pos.get("asset", orig_pos.get("market", ""))).upper()
                orig_direction = str(orig_pos.get("direction", orig_pos.get("side", ""))).upper()

                if orig_asset != asset or orig_direction != direction:
                    continue

                orig_ts = _parse_ts(str(orig_pos.get("opened_at", orig_pos.get("timestamp", ""))))
                if orig_ts is None:
                    continue

                delta = abs((pos_ts - orig_ts).total_seconds())
                if delta > COPY_WINDOW_SECONDS:
                    continue

                # Build a stable event ID
                event_id = (
                    f"{wallet[:10]}_{orig_wallet[:10]}_{asset}_{direction}_"
                    f"{int(pos_ts.timestamp())}"
                )
                if event_id in already_seen:
                    continue

                pnl_usd = 0.0
                pnl_pct = 0.0
                status = "OPEN"
                try:
                    pnl_usd = float(pos.get("pnl_usd", pos.get("unrealized_pnl", 0)))
                    if size_usd:
                        pnl_pct = round(pnl_usd / size_usd * 100, 2)
                    if pos.get("closed_at") or pos.get("is_closed"):
                        status = "CLOSED"
                except (TypeError, ValueError):
                    pass

                event: dict = {
                    "event_id": event_id,
                    "detected_at": now.isoformat(),
                    "copier_wallet": wallet,
                    "originator_wallet": orig_wallet,
                    "asset": asset,
                    "direction": direction,
                    "size_contracts": pos.get("size", ""),
                    "size_usd": round(size_usd, 2),
                    "entry_price": pos.get("entry_price", ""),
                    "pnl_usd": round(pnl_usd, 2),
                    "pnl_pct": pnl_pct,
                    "status": status,
                    "posted": False,
                    # extra context for content generation
                    "_copy_delta_seconds": round(delta, 1),
                    "_orig_size_usd": _position_size_usd(orig_pos),
                }
                events.append(event)
                log.info(
                    "Copy-trade detected: %s copied %s on %s %s $%.0f",
                    wallet[:12], orig_wallet[:12], direction, asset, size_usd,
                )

    return events


# ---------------------------------------------------------------------------
# Content generation
# ---------------------------------------------------------------------------

def _shorten_wallet(wallet: str) -> str:
    """Return a short display form of a wallet address."""
    if len(wallet) > 10:
        return f"{wallet[:6]}...{wallet[-4:]}"
    return wallet


def _format_usd(amount: float) -> str:
    """Format a dollar amount with M/K suffix."""
    abs_amt = abs(amount)
    if abs_amt >= 1_000_000:
        return f"${abs_amt / 1_000_000:.2f}M"
    if abs_amt >= 1_000:
        return f"${abs_amt / 1_000:.1f}K"
    return f"${abs_amt:.0f}"


def _generate_post(event: dict) -> str:
    """
    Generate an engagement-optimised social post for a copy-trade event.
    Mirrors the style shown in the method context.
    """
    copier = _shorten_wallet(event["copier_wallet"])
    orig = _shorten_wallet(event["originator_wallet"])
    asset = event["asset"]
    direction = event["direction"].upper()
    size_usd = _format_usd(float(event["size_usd"]))
    size_contracts = event.get("size_contracts", "")
    entry = event.get("entry_price", "")
    pnl_usd = float(event.get("pnl_usd", 0))
    pnl_pct = float(event.get("pnl_pct", 0))
    status = event.get("status", "OPEN")

    direction_word = "long" if direction == "LONG" else "short"
    dir_emoji = "📈" if direction == "LONG" else "📉"

    lines = [
        f"🐋 A whale ({copier}) copied {orig}'s trades and went {direction_word} on #{asset}! {dir_emoji}",
        "",
        f"He opened {direction_word}s on {size_contracts} #{asset} ({size_usd}).",
    ]

    if status == "CLOSED":
        pnl_sign = "+" if pnl_usd >= 0 else ""
        pnl_emoji = "💰" if pnl_usd >= 0 else "🔴"
        lines.append("")
        lines.append(
            f"Trade is now CLOSED — P&L: {pnl_sign}{_format_usd(pnl_usd)} "
            f"({pnl_sign}{pnl_pct:.1f}%) {pnl_emoji}"
        )
    elif pnl_usd != 0:
        pnl_sign = "+" if pnl_usd >= 0 else ""
        lines.append(
            f"Unrealised P&L: {pnl_sign}{_format_usd(pnl_usd)} ({pnl_sign}{pnl_pct:.1f}%)"
        )

    if entry:
        lines.append(f"Entry: {entry}")

    lines += [
        "",
        "Copy-trade or conviction play? 🤔",
        "",
        "#Crypto #Perps #WhaleAlert #CopyTrade",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Queue writer
# ---------------------------------------------------------------------------

def _write_to_queue(post_text: str, event: dict, dry_run: bool) -> Path | None:
    """Write a post payload JSON to the posting queue directory."""
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"whale_copy_{event['event_id'][:30]}_{ts}.json"
    payload = {
        "script": SCRIPT_NAME,
        "queued_at": datetime.now(tz=timezone.utc).isoformat(),
        "event_id": event["event_id"],
        "post_text": post_text,
        "metadata": {
            "copier": event["copier_wallet"],
            "originator": event["originator_wallet"],
            "asset": event["asset"],
            "direction": event["direction"],
            "size_usd": event["size_usd"],
            "pnl_usd": event["pnl_usd"],
            "status": event["status"],
        },
        "dry_run": dry_run,
    }
    dest = safe_path(QUEUE_DIR / filename)
    try:
        with open(dest, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        log.info("Queued post -> %s", dest.name)
        return dest
    except Exception as exc:
        log.error("Failed to write queue file %s: %s", dest, exc)
        return None


# ---------------------------------------------------------------------------
# Status report
# ---------------------------------------------------------------------------

def _show_status() -> None:
    state = _load_state()
    print(f"Last run     : {state.get('last_run', 'never')}")
    print(f"Events seen  : {len(state.get('seen_event_ids', []))}")
    print(f"Events posted: {len(state.get('posted_event_ids', []))}")

    queued = list(safe_path(QUEUE_DIR).glob("whale_copy_*.json")) if safe_path(QUEUE_DIR).exists() else []
    print(f"Queue files  : {len(queued)}")

    log_path = safe_path(LOG_FILE)
    if log_path.exists():
        size_kb = log_path.stat().st_size // 1024
        print(f"Log file     : {log_path} ({size_kb} KB)")
    else:
        print("Log file     : not yet created")

    if safe_path(EVENTS_CSV).exists():
        with open(safe_path(EVENTS_CSV), "r", encoding="utf-8") as fh:
            rows = sum(1 for _ in fh) - 1  # subtract header
        print(f"CSV records  : {rows}")


# ---------------------------------------------------------------------------
# Core run
# ---------------------------------------------------------------------------

def run(dry_run: bool = False) -> None:
    log.info("=== %s starting (dry_run=%s) ===", SCRIPT_NAME, dry_run)
    _ensure_dirs()

    # Recall skills for task context (no-op if _common not available)
    skills = recall_skills_for_task("whale copy-trade detection perps analytics")
    if skills:
        log.debug("Skills recalled: %s", skills)

    state = _load_state()
    seen_ids: set[str] = set(state.get("seen_event_ids", []))
    posted_ids: set[str] = set(state.get("posted_event_ids", []))

    # 1. Fetch all recent large positions
    log.info("Fetching recent large positions (>$%s)…", _format_usd(MIN_POSITION_USD))
    all_positions = _fetch_recent_positions()
    log.info("Fetched %d candidate positions.", len(all_positions))

    # 2. Fetch originator positions for each tracked wallet
    originator_positions: dict[str, list[dict]] = {}
    for wallet in TRACKED_WALLETS:
        log.info("Fetching positions for tracked wallet %s…", wallet[:14])
        positions = _fetch_wallet_positions(wallet)
        originator_positions[wallet] = positions
        log.debug("  -> %d positions for %s", len(positions), wallet[:14])

    # 3. Detect copy-trades
    new_events = _detect_copy_trades(all_positions, originator_positions, seen_ids)
    log.info("Detected %d new copy-trade event(s).", len(new_events))

    if not new_events:
        log.info("Nothing new to post.")
    else:
        # 4. Persist events to CSV
        _append_events_csv(new_events)

        for event in new_events:
            seen_ids.add(event["event_id"])

            # 5. Generate post content
            post_text = _generate_post(event)
            log.debug("Generated post for event %s:\n%s", event["event_id"], post_text)

            # 6. Route to posting queue
            if not dry_run:
                queued_path = _write_to_queue(post_text, event, dry_run=False)
                if queued_path:
                    event["posted"] = True
                    posted_ids.add(event["event_id"])
            else:
                log.info("[DRY-RUN] Would queue post:\n%s", post_text)
                event["posted"] = False

            # 7. Capture skill from result (no-op if _common not available)
            capture_skill_from_result(event)

    # 8. Persist updated state
    state["last_run"] = datetime.now(tz=timezone.utc).isoformat()
    state["seen_event_ids"] = list(seen_ids)
    state["posted_event_ids"] = list(posted_ids)
    _save_state(state)

    log.info("=== %s finished ===", SCRIPT_NAME)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: Monitor whale copy-trade events on perps markets.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute the monitor and route any new events to the posting queue.",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print current state, queue depth, and log info, then exit.",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Run detection and generate posts but do NOT write to the queue.",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        if args.status:
            _show_status()
        elif args.run:
            run(dry_run=False)
        elif args.dry_run:
            run(dry_run=True)
    except KeyboardInterrupt:
        log.info("Interrupted by user.")
        sys.exit(0)
    except Exception as exc:
        log.exception("Unhandled exception in main: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()