#!/usr/bin/env python3
"""
PRINTMAXX Telegram Community Monitor — Signal Extraction from Public Channels
==============================================================================
Monitors public Telegram channels and groups for alpha signals, trending
topics, product opportunities, and competitor activity. Uses t.me/s/ public
preview (no API key needed for public channels).

Sources: OPS/TELEGRAM_COMMUNITIES_ALL_NICHES.md (33 niche communities planned)
         OPS/SIGNAL_ACCOUNT_DIRECTORY.md (Telegram signal channels)

Usage:
    python3 telegram_community_monitor.py --scan          # Full scan all channels
    python3 telegram_community_monitor.py --scan --niche ai   # Scan specific niche
    python3 telegram_community_monitor.py --status        # Show monitoring scope
    python3 telegram_community_monitor.py --digest        # Generate OPS/ digest
    python3 telegram_community_monitor.py --trending      # Show trending topics
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

try:
    import requests
except ImportError:
    requests = None

# --- Paths ---
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
LEDGER_DIR = BASE_DIR / "LEDGER"
OPS_DIR = BASE_DIR / "OPS"
LOG_DIR = SCRIPT_DIR / "logs"
ALPHA_CSV = LEDGER_DIR / "ALPHA_STAGING.csv"
TELEGRAM_CSV = LEDGER_DIR / "TELEGRAM_SIGNALS.csv"

# --- Colors ---
G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"; B = "\033[94m"
M = "\033[95m"; C = "\033[96m"; W = "\033[97m"; D = "\033[0m"; BOLD = "\033[1m"

# ============================================================
# MONITORED TELEGRAM CHANNELS (Public Channels)
# ============================================================
# Format: channel_handle (without @), niche category, description

CHANNELS = {
    "ai_tools": {
        "description": "AI Tools & Automation",
        "channels": [
            ("aiaboratory", "AI lab tools and research"),
            ("aikitech", "AI tech news and tools"),
            ("chatgpt_prompts_official", "ChatGPT prompts and techniques"),
            ("aitooltracker", "Daily AI tool discoveries"),
        ],
    },
    "crypto_defi": {
        "description": "Crypto & DeFi Alpha",
        "channels": [
            ("whale_alert", "Large crypto transactions"),
            ("cryptonews_official", "Crypto market news"),
            ("defipulse", "DeFi protocol tracking"),
            ("maboroshilab", "Meme coin alpha"),
        ],
    },
    "indie_hackers": {
        "description": "Indie Hackers & Solopreneur",
        "channels": [
            ("indiehackernews", "Indie hacker launches and revenue"),
            ("buildinpublic", "Build-in-public updates"),
            ("saas_weekly", "SaaS metrics and insights"),
        ],
    },
    "ecom_dropship": {
        "description": "Ecommerce & Dropshipping",
        "channels": [
            ("ecomtrends", "Ecom product trends"),
            ("aliexpresstrending", "AliExpress trending products"),
            ("shopifytips", "Shopify tips and tactics"),
        ],
    },
    "marketing_growth": {
        "description": "Marketing & Growth Hacking",
        "channels": [
            ("growth_hacking_channel", "Growth hacking tactics"),
            ("seochannel", "SEO strategies and updates"),
            ("contentmarketingtips", "Content marketing insights"),
        ],
    },
    "freelance": {
        "description": "Freelance & Remote Work",
        "channels": [
            ("remotejobschannel", "Remote job opportunities"),
            ("freelancejobs", "Freelance gig postings"),
            ("upworkinsider", "Upwork tips and strategies"),
        ],
    },
    "dev_tools": {
        "description": "Developer Tools & Open Source",
        "channels": [
            ("github_trending_repos", "Trending GitHub repos"),
            ("devtoolsdaily", "Developer tool discoveries"),
            ("python_daily", "Python tips and packages"),
        ],
    },
    "faith_wellness": {
        "description": "Faith & Wellness (Niche Apps)",
        "channels": [
            ("islamicreminders", "Islamic content and reminders"),
            ("productivityhacks", "Productivity methods and tools"),
            ("biohacking", "Biohacking and wellness"),
        ],
    },
}

# Signal keywords that indicate high-value alpha
SIGNAL_KEYWORDS = {
    "revenue": {
        "weight": 90,
        "patterns": [
            r'\$[\d,]+(?:k|K|/mo|/month|MRR|ARR)',
            r'(?:revenue|income|profit|making|earned)\s*(?:of\s+)?\$[\d,]+',
            r'(?:6|7|8)\s*(?:-|\s)?figure',
        ],
    },
    "product_launch": {
        "weight": 80,
        "patterns": [
            r'(?:just\s+)?launch(?:ed|ing)',
            r'(?:now\s+)?live\s+on',
            r'shipped\s+(?:my|our|the)',
            r'product\s+hunt',
        ],
    },
    "opportunity": {
        "weight": 85,
        "patterns": [
            r'(?:arbitrage|arb)\s+(?:opportunity|window)',
            r'underpriced|mispriced|untapped',
            r'(?:nobody|no\s+one)\s+(?:is\s+)?(?:doing|building|selling)',
            r'gap\s+in\s+(?:the\s+)?market',
        ],
    },
    "tool_alpha": {
        "weight": 70,
        "patterns": [
            r'(?:free|open\s*source)\s+(?:tool|alternative)',
            r'(?:better|cheaper)\s+(?:than|alternative)',
            r'(?:new|just\s+)?released',
            r'MIT\s+licen[sc]e',
        ],
    },
    "growth_hack": {
        "weight": 75,
        "patterns": [
            r'(?:growth|marketing)\s+(?:hack|trick|strategy)',
            r'(?:went\s+)?viral',
            r'(?:\d+[KkMm]\+?)\s+(?:views|followers|subscribers|downloads)',
            r'conversion\s+rate',
        ],
    },
    "hiring_demand": {
        "weight": 65,
        "patterns": [
            r'(?:looking\s+for|hiring|need)\s+(?:a\s+)?(?:developer|designer|freelancer|VA)',
            r'(?:willing\s+to\s+)?pay\s+\$[\d,]+',
            r'budget\s*(?::|is)\s*\$[\d,]+',
        ],
    },
}


def fetch_telegram_channel(handle, max_messages=20):
    """Fetch recent messages from a public Telegram channel via t.me/s/ preview."""
    if not requests:
        return []

    url = f"https://t.me/s/{handle}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return []

        html = resp.text
        messages = []

        # Extract message blocks from t.me/s/ public preview
        # Each message is in a div with class "tgme_widget_message_wrap"
        msg_blocks = re.findall(
            r'<div class="tgme_widget_message_wrap[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>',
            html, re.DOTALL
        )

        if not msg_blocks:
            # Fallback: try to get text content from message bubbles
            msg_blocks = re.findall(
                r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>',
                html, re.DOTALL
            )

        for block in msg_blocks[:max_messages]:
            # Extract text content
            text = re.sub(r'<[^>]+>', ' ', block)
            text = re.sub(r'\s+', ' ', text).strip()

            if len(text) < 10:
                continue

            # Extract views
            views_m = re.search(r'([\d.]+[KkMm]?)\s*(?:views?|👁)', block)
            views = views_m.group(1) if views_m else "0"

            # Extract date
            date_m = re.search(r'datetime="(\d{4}-\d{2}-\d{2})', block)
            msg_date = date_m.group(1) if date_m else datetime.now().strftime("%Y-%m-%d")

            messages.append({
                "text": text[:500],
                "views": views,
                "date": msg_date,
                "handle": handle,
            })

        return messages

    except Exception as e:
        return []


def match_signals(text):
    """Match text against signal keyword patterns. Returns list of (category, weight) matches."""
    matches = []
    text_lower = text.lower()
    for category, config in SIGNAL_KEYWORDS.items():
        for pattern in config["patterns"]:
            if re.search(pattern, text_lower):
                matches.append((category, config["weight"]))
                break  # one match per category is enough
    return matches


def score_message(msg, signal_matches):
    """Score a message 0-100 based on signal matches and engagement."""
    if not signal_matches:
        return 0

    base_score = max(w for _, w in signal_matches)

    # Engagement multiplier from views
    views_str = msg.get("views", "0")
    try:
        if "K" in views_str.upper():
            views = float(views_str.upper().replace("K", "")) * 1000
        elif "M" in views_str.upper():
            views = float(views_str.upper().replace("M", "")) * 1000000
        else:
            views = float(views_str)
    except (ValueError, TypeError):
        views = 0

    if views > 10000:
        base_score = min(100, base_score + 10)
    elif views > 1000:
        base_score = min(100, base_score + 5)

    # Multiple signal bonus
    if len(signal_matches) >= 3:
        base_score = min(100, base_score + 10)
    elif len(signal_matches) >= 2:
        base_score = min(100, base_score + 5)

    return base_score


def content_hash(text):
    """Generate dedup hash for message content."""
    normalized = re.sub(r'\s+', ' ', text.lower().strip())[:200]
    return hashlib.md5(normalized.encode()).hexdigest()[:12]


def scan_channels(niche_filter=None):
    """Scan all monitored Telegram channels for signals."""
    if not requests:
        print(f"{R}ERROR: requests library required. pip3 install requests{D}")
        return []

    today = datetime.now()
    all_signals = []
    total_messages = 0
    total_channels = 0
    failed_channels = 0

    # Load existing hashes for dedup
    existing_hashes = set()
    if TELEGRAM_CSV.exists():
        try:
            with open(TELEGRAM_CSV, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    h = row.get("content_hash", "")
                    if h:
                        existing_hashes.add(h)
        except Exception:
            pass

    print(f"\n{BOLD}{W}{'='*70}")
    print(f"  TELEGRAM COMMUNITY MONITOR — Signal Scan")
    print(f"  {today.strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*70}{D}\n")

    niches_to_scan = CHANNELS.items()
    if niche_filter:
        niche_filter_lower = niche_filter.lower()
        niches_to_scan = [(k, v) for k, v in CHANNELS.items()
                          if niche_filter_lower in k.lower() or niche_filter_lower in v["description"].lower()]
        if not niches_to_scan:
            print(f"{R}No niches matching '{niche_filter}'. Available: {', '.join(CHANNELS.keys())}{D}")
            return []

    for niche_key, niche_data in niches_to_scan:
        print(f"\n{BOLD}{B}  [{niche_key.upper()}] {niche_data['description']}{D}")
        print(f"  {'-'*60}")

        for handle, description in niche_data["channels"]:
            total_channels += 1
            messages = fetch_telegram_channel(handle)

            if not messages:
                print(f"  {Y}[@{handle}]{D} — no messages (private or empty)")
                failed_channels += 1
                continue

            channel_signals = 0
            for msg in messages:
                total_messages += 1
                signal_matches = match_signals(msg["text"])

                if signal_matches:
                    score = score_message(msg, signal_matches)
                    if score >= 50:
                        ch = content_hash(msg["text"])
                        if ch in existing_hashes:
                            continue
                        existing_hashes.add(ch)

                        signal = {
                            "date": msg["date"],
                            "niche": niche_key,
                            "channel": f"@{handle}",
                            "text": msg["text"][:300],
                            "views": msg["views"],
                            "score": score,
                            "signals": [s[0] for s in signal_matches],
                            "content_hash": ch,
                        }
                        all_signals.append(signal)
                        channel_signals += 1

            status = G if channel_signals > 0 else W
            print(f"  {status}[@{handle}]{D} — {len(messages)} msgs, {channel_signals} signals")

            # Rate limit: be polite to Telegram
            time.sleep(1.5)

    # Summary
    print(f"\n{BOLD}{W}  SCAN SUMMARY{D}")
    print(f"  {'-'*60}")
    print(f"  Channels scanned: {total_channels} ({failed_channels} private/empty)")
    print(f"  Total messages: {total_messages}")
    print(f"  Signals found: {G}{len(all_signals)}{D}")

    if all_signals:
        # Save to CSV
        save_signals_csv(all_signals)

        # Show top signals
        top = sorted(all_signals, key=lambda s: s["score"], reverse=True)[:10]
        print(f"\n{BOLD}{Y}  TOP SIGNALS:{D}\n")
        for i, sig in enumerate(top, 1):
            sig_labels = ", ".join(sig["signals"])
            print(f"  {i}. [{sig['score']}/100] {sig['channel']} ({sig['niche']})")
            print(f"     Signals: {sig_labels}")
            print(f"     {sig['text'][:120]}")
            print()

        # Append high-value to ALPHA_STAGING
        appended = append_to_alpha(all_signals)
        if appended > 0:
            print(f"  {G}Appended {appended} high-value signals to ALPHA_STAGING.csv{D}")

    return all_signals


def save_signals_csv(signals):
    """Save/append signals to TELEGRAM_SIGNALS.csv."""
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)

    file_exists = TELEGRAM_CSV.exists()
    with open(TELEGRAM_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "date", "niche", "channel", "text", "views",
                "score", "signals", "content_hash"
            ])
        for sig in signals:
            writer.writerow([
                sig["date"], sig["niche"], sig["channel"],
                sig["text"], sig["views"], sig["score"],
                "|".join(sig["signals"]), sig["content_hash"]
            ])

    print(f"  {G}Saved {len(signals)} signals to {TELEGRAM_CSV}{D}")


def append_to_alpha(signals, threshold=75):
    """Append high-scoring signals to ALPHA_STAGING.csv."""
    if not ALPHA_CSV.exists():
        return 0

    high_value = [s for s in signals if s["score"] >= threshold]
    if not high_value:
        return 0

    # Get next ALPHA ID
    existing_ids = set()
    try:
        with open(ALPHA_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                aid = row.get("alpha_id", "")
                m = re.match(r'ALPHA(\d+)', aid)
                if m:
                    existing_ids.add(int(m.group(1)))
    except Exception:
        pass

    next_id = max(existing_ids, default=10000) + 1
    appended = 0

    try:
        with open(ALPHA_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            for sig in high_value:
                alpha_id = f"ALPHA{next_id}"
                next_id += 1
                category = "TOOL_ALPHA" if "tool_alpha" in sig["signals"] else \
                           "MONETIZATION" if "revenue" in sig["signals"] else \
                           "GROWTH_HACK" if "growth_hack" in sig["signals"] else \
                           "EMERGING_OPPORTUNITY"
                writer.writerow([
                    alpha_id,
                    f"Telegram {sig['channel']}",
                    f"https://t.me/s/{sig['channel'].lstrip('@')}",
                    category,
                    sig["text"][:200],
                    "HIGH" if sig["score"] >= 85 else "MEDIUM",
                    "IMMEDIATE" if sig["score"] >= 85 else "SOON",
                    "PENDING_REVIEW",
                    "",
                    sig["niche"].upper(),
                    sig["score"],
                    f"Telegram signal: {', '.join(sig['signals'])}. Views: {sig['views']}",
                    "None",
                    "N/A",
                    "N/A",
                    sig["text"][:150],
                    "None",
                    datetime.now().strftime("%Y-%m-%d"),
                ])
                appended += 1
    except Exception as e:
        print(f"  {R}Error appending to ALPHA_STAGING: {e}{D}")

    return appended


def generate_digest(signals=None):
    """Generate Telegram monitoring digest."""
    today = datetime.now()
    digest_path = OPS_DIR / f"TELEGRAM_SIGNAL_DIGEST_{today.strftime('%Y_%m_%d')}.md"

    # Load signals from CSV if not provided
    if signals is None:
        signals = []
        if TELEGRAM_CSV.exists():
            try:
                with open(TELEGRAM_CSV, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get("date", "") == today.strftime("%Y-%m-%d"):
                            signals.append(row)
            except Exception:
                pass

    lines = [
        f"# Telegram Signal Digest",
        f"",
        f"Generated: {today.strftime('%Y-%m-%d %H:%M:%S')}",
        f"",
        f"Total signals today: {len(signals)}",
        f"Channels monitored: {sum(len(v['channels']) for v in CHANNELS.values())}",
        f"Niches covered: {len(CHANNELS)}",
        f"",
        f"---",
        f"",
    ]

    if signals:
        # Group by niche
        by_niche = {}
        for sig in signals:
            niche = sig.get("niche", "unknown")
            by_niche.setdefault(niche, []).append(sig)

        for niche, sigs in sorted(by_niche.items()):
            desc = CHANNELS.get(niche, {}).get("description", niche)
            lines.append(f"## {desc} ({len(sigs)} signals)")
            lines.append("")
            for sig in sorted(sigs, key=lambda s: -int(s.get("score", 0))):
                score = sig.get("score", 0)
                channel = sig.get("channel", "?")
                text = sig.get("text", "")[:150]
                signal_types = sig.get("signals", "")
                lines.append(f"- **[{score}/100]** {channel}: {text}")
                lines.append(f"  Signals: {signal_types}")
                lines.append("")

    # Niche coverage
    lines.append(f"## Monitoring Coverage")
    lines.append("")
    lines.append(f"| Niche | Channels | Description |")
    lines.append(f"|-------|----------|-------------|")
    for niche_key, niche_data in CHANNELS.items():
        channels = ", ".join(f"@{h}" for h, _ in niche_data["channels"])
        lines.append(f"| {niche_key} | {len(niche_data['channels'])} | {niche_data['description']} |")

    content = "\n".join(lines)
    with open(digest_path, 'w') as f:
        f.write(content)

    print(f"  {G}Digest saved to {digest_path}{D}")
    return digest_path


def show_trending():
    """Show trending topics from recent Telegram signals."""
    if not TELEGRAM_CSV.exists():
        print(f"{Y}No signals data yet. Run --scan first.{D}")
        return

    all_words = Counter()
    signal_counts = Counter()

    with open(TELEGRAM_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row.get("text", "").lower()
            # Extract meaningful words (3+ chars, not common)
            words = re.findall(r'\b[a-z]{3,}\b', text)
            stopwords = {"the", "and", "for", "that", "this", "with", "are", "you",
                         "have", "from", "was", "not", "but", "they", "can", "has",
                         "been", "will", "more", "one", "all", "would", "there", "what",
                         "about", "which", "when", "your", "how", "get", "just", "its"}
            words = [w for w in words if w not in stopwords]
            all_words.update(words)

            sigs = row.get("signals", "").split("|")
            signal_counts.update(sigs)

    print(f"\n{BOLD}{W}  TRENDING TOPICS (from Telegram signals){D}\n")
    print(f"  Top Keywords:")
    for word, count in all_words.most_common(20):
        bar = "█" * min(count, 30)
        print(f"  {word:20s} {count:3d} {G}{bar}{D}")

    print(f"\n  Signal Distribution:")
    for sig, count in signal_counts.most_common():
        if sig:
            print(f"  {sig:20s} {count:3d}")


def show_status():
    """Show monitoring scope status."""
    total_channels = sum(len(v["channels"]) for v in CHANNELS.values())
    total_niches = len(CHANNELS)

    print(f"\n{BOLD}{W}  TELEGRAM COMMUNITY MONITOR — Status{D}")
    print(f"  {'-'*50}")
    print(f"  Niches: {total_niches}")
    print(f"  Channels: {total_channels}")
    print(f"  Signal categories: {len(SIGNAL_KEYWORDS)}")
    print()

    for niche_key, niche_data in CHANNELS.items():
        channels = ", ".join(f"@{h}" for h, _ in niche_data["channels"])
        print(f"  {B}{niche_key}{D}: {niche_data['description']}")
        print(f"    Channels: {channels}")
        print()

    # CSV stats
    if TELEGRAM_CSV.exists():
        try:
            with open(TELEGRAM_CSV, 'r') as f:
                rows = sum(1 for _ in f) - 1
            print(f"  Total signals collected: {G}{rows}{D}")
        except Exception:
            pass

    print(f"\n  Signal keywords tracked:")
    for cat, config in SIGNAL_KEYWORDS.items():
        print(f"    {cat}: weight {config['weight']}, {len(config['patterns'])} patterns")


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Telegram Community Monitor")
    parser.add_argument("--scan", action="store_true", help="Scan all channels for signals")
    parser.add_argument("--niche", type=str, help="Filter scan to specific niche")
    parser.add_argument("--status", action="store_true", help="Show monitoring scope")
    parser.add_argument("--digest", action="store_true", help="Generate OPS/ digest")
    parser.add_argument("--trending", action="store_true", help="Show trending topics")

    args = parser.parse_args()

    if not any([args.scan, args.status, args.digest, args.trending]):
        args.status = True

    if args.status:
        show_status()

    if args.scan:
        signals = scan_channels(niche_filter=args.niche)
        if signals:
            generate_digest(signals)

    if args.digest:
        generate_digest()

    if args.trending:
        show_trending()


if __name__ == "__main__":
    main()
