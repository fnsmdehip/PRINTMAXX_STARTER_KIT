#!/usr/bin/env python3
"""
PRINTMAXX Tweet Auto-Drafter
============================
Reads approved/pending alpha entries from LEDGER/ALPHA_STAGING.csv and
auto-generates tweet drafts for multiple niche accounts using template-based
generation (no API keys required).

Accounts:
    @PRINTMAXXER  - tech/building-in-public
    @repscheme    - fitness
    @drifthour    - aesthetic/music
    @voidpilled   - esoteric
    @selahmoments - faith

Voice: consequence-first hooks, specific numbers, @pipelineabuser energy,
       lowercase casual, no AI slop vocabulary. See .claude/rules/copy-style.md

Usage:
    python3 AUTOMATIONS/tweet_auto_drafter.py                         # default: 20 entries
    python3 AUTOMATIONS/tweet_auto_drafter.py --batch 50              # process 50 entries
    python3 AUTOMATIONS/tweet_auto_drafter.py --account repscheme     # filter to one account
    python3 AUTOMATIONS/tweet_auto_drafter.py --dry-run               # print, don't save
    python3 AUTOMATIONS/tweet_auto_drafter.py --status                # show stats

Cron:
    30 7 * * * cd $BASE && python3 AUTOMATIONS/tweet_auto_drafter.py --batch 20 >> AUTOMATIONS/logs/tweet_drafter.log 2>&1
"""

from __future__ import annotations

import argparse
import csv
import os
import random
import re
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALPHA_CSV = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
OUTPUT_DIR = PROJECT_ROOT / "CONTENT" / "social" / "auto_generated"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"


def safe_path(target: Path) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, file=sys.stderr)
    safe_path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_DIR / "tweet_drafter.log"), "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Account definitions
# ---------------------------------------------------------------------------
ACCOUNTS = {
    "PRINTMAXXER": {
        "handle": "@PRINTMAXXER",
        "niche": "tech/building-in-public",
        "tone": "aggressive builder energy, specific numbers, tools named, consequence-first",
        "categories": [
            "APP_FACTORY", "TOOL_ALPHA", "GROWTH_HACK", "MONETIZATION",
            "CONTENT_FORMAT", "OUTBOUND", "SEO_GEO_ASO",
        ],
    },
    "repscheme": {
        "handle": "@repscheme",
        "niche": "fitness",
        "tone": "discipline-focused, no excuses, numbers on gains, lowercase casual",
        "categories": [
            "APP_FACTORY", "CONTENT_FORMAT", "GROWTH_HACK", "MONETIZATION",
        ],
    },
    "drifthour": {
        "handle": "@drifthour",
        "niche": "aesthetic/music",
        "tone": "atmospheric, minimal words, vibe-first, lowercase, ellipsis pauses",
        "categories": [
            "CONTENT_FORMAT", "CONTENT_FARM", "GROWTH_HACK", "TOOL_ALPHA",
        ],
    },
    "voidpilled": {
        "handle": "@voidpilled",
        "niche": "esoteric",
        "tone": "cryptic, philosophical, brief, no hedging, trust reader intelligence",
        "categories": [
            "CONTENT_FORMAT", "GROWTH_HACK", "TOOL_ALPHA", "MONETIZATION",
        ],
    },
    "selahmoments": {
        "handle": "@selahmoments",
        "niche": "faith",
        "tone": "reflective, purposeful, community-oriented, lowercase, gentle conviction",
        "categories": [
            "APP_FACTORY", "CONTENT_FORMAT", "GROWTH_HACK", "MONETIZATION",
        ],
    },
}

# ---------------------------------------------------------------------------
# Template library (per-account, per-category)
# ---------------------------------------------------------------------------
# Templates use placeholders: {tactic}, {source}, {number}, {tool}, {category}
# Each template is a list of tweet variants. The drafter picks 3-5 per entry.

TEMPLATES = {
    "PRINTMAXXER": {
        "TOOL_ALPHA": [
            "found {tool}. {tactic_short}. it's borderline illegal how much this saves you.",
            "just wired {tool} into the stack. {tactic_short}. stop overthinking it, just set it up.",
            "{tactic_short}. been using {tool} for a week. already saved {number} hours.",
            "the tool nobody talks about: {tool}. {tactic_short}. zero excuses left.",
            "if you're not using {tool} you're leaving money on the table. {tactic_short}.",
        ],
        "APP_FACTORY": [
            "analyzed {number} apps doing $100k+/mo. {tactic_short}. the pattern is obvious.",
            "{tactic_short}. built this in one session. ship it, measure it, iterate.",
            "the app factory playbook: {tactic_short}. clone what works, rebrand for your niche.",
            "just shipped another app. {tactic_short}. stop planning, start deploying.",
            "every app making money does this: {tactic_short}. not complicated. just do it.",
        ],
        "GROWTH_HACK": [
            "{tactic_short}. tried it yesterday. results in {number} hours.",
            "growth hack that actually works: {tactic_short}. no gimmicks.",
            "stop buying followers. {tactic_short}. real growth, real numbers.",
            "{tactic_short}. this is the kind of stuff that compounds. just start.",
            "most people won't do this: {tactic_short}. that's why it works.",
        ],
        "MONETIZATION": [
            "{tactic_short}. the math works out to {number}/mo if you execute.",
            "revenue hack: {tactic_short}. not theory. real numbers from real builders.",
            "stop making $0. {tactic_short}. the first dollar is the hardest. then it compounds.",
            "{tactic_short}. stack this with 2-3 other methods and you're printing.",
            "the revenue play nobody talks about: {tactic_short}. works at any scale.",
        ],
        "CONTENT_FORMAT": [
            "{tactic_short}. this content format gets {number}x more engagement.",
            "content that converts: {tactic_short}. stop posting generic advice.",
            "tested this format: {tactic_short}. engagement went up, followers went up, revenue went up.",
            "{tactic_short}. the algo rewards this right now. window won't last forever.",
            "if your content isn't doing this: {tactic_short}. you're invisible.",
        ],
        "OUTBOUND": [
            "cold outreach update: {tactic_short}. reply rates doubled.",
            "{tactic_short}. sent {number} emails. this framework converts.",
            "outbound hack: {tactic_short}. stop spraying and praying.",
            "the cold email framework: {tactic_short}. specific, personal, short.",
            "{tactic_short}. outbound is still the fastest path to revenue. period.",
        ],
        "SEO_GEO_ASO": [
            "seo play: {tactic_short}. organic traffic in {number} days.",
            "{tactic_short}. programmatic pages + this = free traffic forever.",
            "aso trick: {tactic_short}. rank higher, spend less on ads.",
            "{tactic_short}. seo is not dead. you're just doing it wrong.",
            "the seo move: {tactic_short}. set it up once, collect traffic forever.",
        ],
    },
    "repscheme": {
        "_default": [
            "the discipline is the same whether it's reps or revenue. {tactic_short}.",
            "grind doesn't care about your feelings. {tactic_short}. just show up.",
            "{tactic_short}. same energy as hitting a PR. consistent effort, real results.",
            "no shortcuts. {tactic_short}. put in the work and the numbers follow.",
            "your excuses don't burn calories. {tactic_short}. start today.",
            "the body keeps score and so does the algorithm. {tactic_short}.",
            "{tactic_short}. apply this like progressive overload. small gains compound.",
        ],
    },
    "drifthour": {
        "_default": [
            "{tactic_short}... let that sit for a moment.",
            "the aesthetic of doing the work quietly... {tactic_short}.",
            "{tactic_short}. there's beauty in the process.",
            "late night session... {tactic_short}. the vibe is right.",
            "found something worth sharing... {tactic_short}.",
            "{tactic_short}... curate your inputs, curate your outputs.",
            "the drift... {tactic_short}. trust the process.",
        ],
    },
    "voidpilled": {
        "_default": [
            "{tactic_short}. the simulation rewards those who see the pattern.",
            "they don't want you to know this: {tactic_short}.",
            "{tactic_short}. information asymmetry is the real currency.",
            "the matrix has a backdoor. {tactic_short}.",
            "most are asleep. {tactic_short}. those who see, profit.",
            "{tactic_short}. reality is programmable if you know the inputs.",
            "esoteric alpha: {tactic_short}. hide in plain sight.",
        ],
    },
    "selahmoments": {
        "_default": [
            "stewardship means using every tool available. {tactic_short}.",
            "{tactic_short}. building with purpose, not just profit.",
            "provision comes in unexpected forms. {tactic_short}.",
            "the work of your hands matters. {tactic_short}. do it with excellence.",
            "{tactic_short}. create value for your community and the rest follows.",
            "faith without works... {tactic_short}. put the effort in.",
            "{tactic_short}. serve others well and the resources come.",
        ],
    },
}


# ---------------------------------------------------------------------------
# Alpha reader
# ---------------------------------------------------------------------------
def read_alpha_entries(batch_size: int = 20) -> list[dict]:
    """Read APPROVED or PENDING_REVIEW entries from ALPHA_STAGING.csv."""
    entries = []
    csv_path = safe_path(ALPHA_CSV)
    if not csv_path.exists():
        log(f"ALPHA_STAGING.csv not found at {csv_path}")
        return entries

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = (row.get("status") or "").strip().upper()
            if status in ("APPROVED", "PENDING_REVIEW"):
                entries.append(row)
            if len(entries) >= batch_size:
                break
    return entries


# ---------------------------------------------------------------------------
# Tactic extraction helpers
# ---------------------------------------------------------------------------
def extract_tactic_short(entry: dict) -> str:
    """Pull a short tactic description from alpha entry fields."""
    # Try extracted_method first, then tactic, then reviewer_notes
    for field in ("extracted_method", "tactic", "reviewer_notes"):
        val = (entry.get(field) or "").strip()
        if val and len(val) > 10:
            # Clean up: lowercase, strip APPROVED prefix, trim
            val = re.sub(r'^APPROVED\.?\s*', '', val, flags=re.IGNORECASE)
            val = val.strip(". ")
            # Truncate to fit tweet length, break at sentence
            if len(val) > 180:
                # Find a sentence break
                cut = val[:180].rfind(".")
                if cut > 60:
                    val = val[:cut + 1]
                else:
                    val = val[:177] + "..."
            # Lowercase first char for casual voice
            if val and val[0].isupper():
                val = val[0].lower() + val[1:]
            return val
    # Fallback
    return entry.get("alpha_id", "alpha")


def extract_number(entry: dict) -> str:
    """Try to pull a specific number from the entry for templates."""
    text = " ".join([
        entry.get("extracted_method", ""),
        entry.get("tactic", ""),
        entry.get("reviewer_notes", ""),
    ])
    # Look for dollar amounts
    m = re.search(r'\$[\d,]+[kK]?(?:/(?:mo|month|day|year|week))?', text)
    if m:
        return m.group(0)
    # Look for percentages
    m = re.search(r'\d+(?:\.\d+)?%', text)
    if m:
        return m.group(0)
    # Look for plain numbers with context
    m = re.search(r'(\d{2,}[\+]?)\s*(apps?|tools?|hours?|days?|sites?|pages?|leads?|emails?|users?|downloads?)', text, re.IGNORECASE)
    if m:
        return f"{m.group(1)} {m.group(2)}"
    # Fallback generic numbers
    return random.choice(["100+", "50+", "200+", "30+", "10x"])


def extract_tool(entry: dict) -> str:
    """Try to pull a named tool from the entry."""
    text = " ".join([
        entry.get("extracted_method", ""),
        entry.get("tactic", ""),
        entry.get("source", ""),
        entry.get("reviewer_notes", ""),
    ])
    # Look for tool patterns (word.io, word.ai, word.com, etc.)
    m = re.search(r'(\w+\.(?:io|ai|com|dev|app|co|sh|so))', text, re.IGNORECASE)
    if m:
        return m.group(1)
    # Look for capitalized tool names
    m = re.search(r'\b([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?)\b', text)
    if m and m.group(1) not in ("APPROVED", "PENDING", "HIGH", "HIGHEST", "TRUE", "FALSE", "ALPHA", "The"):
        return m.group(1)
    return entry.get("source", "this tool")


# ---------------------------------------------------------------------------
# Tweet generation
# ---------------------------------------------------------------------------
def generate_tweets_for_entry(entry: dict, target_account: str | None = None) -> list[dict]:
    """Generate 3-5 tweet variants per account for a given alpha entry."""
    results = []
    alpha_id = entry.get("alpha_id", "UNKNOWN")
    category = (entry.get("category") or "GROWTH_HACK").strip().upper()
    tactic_short = extract_tactic_short(entry)
    number = extract_number(entry)
    tool = extract_tool(entry)
    source = entry.get("source", "")
    created_date = datetime.now().strftime("%Y-%m-%d")

    accounts_to_process = {}
    if target_account:
        key = target_account.upper().lstrip("@")
        if key in ACCOUNTS:
            accounts_to_process[key] = ACCOUNTS[key]
        else:
            log(f"Unknown account: {target_account}. Available: {', '.join(ACCOUNTS.keys())}")
            return results
    else:
        accounts_to_process = ACCOUNTS

    for acct_key, acct_info in accounts_to_process.items():
        # Check category relevance
        if category not in acct_info["categories"] and "_default" not in TEMPLATES.get(acct_key, {}):
            continue

        # Get templates
        acct_templates = TEMPLATES.get(acct_key, {})
        template_list = acct_templates.get(category, acct_templates.get("_default", []))
        if not template_list:
            continue

        # Pick 3-5 random templates
        count = min(random.randint(3, 5), len(template_list))
        chosen = random.sample(template_list, count)

        for template in chosen:
            tweet_text = template.format(
                tactic_short=tactic_short,
                number=number,
                tool=tool,
                source=source,
                category=category.lower().replace("_", " "),
            )
            # Clean up double spaces, trailing whitespace
            tweet_text = re.sub(r'\s+', ' ', tweet_text).strip()
            # Enforce max 280 chars
            if len(tweet_text) > 280:
                tweet_text = tweet_text[:277] + "..."

            results.append({
                "tweet_text": tweet_text,
                "source_alpha_id": alpha_id,
                "account": acct_info["handle"],
                "status": "PENDING_REVIEW",
                "created_date": created_date,
            })

    return results


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
CSV_FIELDS = ["tweet_text", "source_alpha_id", "account", "status", "created_date"]


def write_account_csv(account_handle: str, tweets: list[dict], dry_run: bool = False) -> str | None:
    """Write tweets for one account to a CSV file. Returns filepath or None."""
    if not tweets:
        return None

    safe_path(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    clean_handle = account_handle.lstrip("@").lower()
    datestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tweets_{clean_handle}_{datestamp}.csv"
    filepath = safe_path(OUTPUT_DIR / filename)

    if dry_run:
        print(f"\n{'='*60}")
        print(f"  DRY RUN: {account_handle} ({len(tweets)} tweets)")
        print(f"  Would write to: {filepath}")
        print(f"{'='*60}")
        for t in tweets:
            print(f"\n  [{t['source_alpha_id']}] {t['tweet_text']}")
        return None

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(tweets)

    log(f"Wrote {len(tweets)} tweets for {account_handle} -> {filepath}")
    return str(filepath)


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
def show_status():
    """Print stats about alpha entries and existing tweet drafts."""
    # Count alpha entries by status
    status_counts = {}
    if ALPHA_CSV.exists():
        with open(ALPHA_CSV, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                s = (row.get("status") or "UNKNOWN").strip()
                status_counts[s] = status_counts.get(s, 0) + 1

    print("\n--- ALPHA_STAGING.csv Status ---")
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        print(f"  {status}: {count}")
    processable = status_counts.get("APPROVED", 0) + status_counts.get("PENDING_REVIEW", 0)
    print(f"\n  Processable (APPROVED + PENDING_REVIEW): {processable}")

    # Count existing tweet drafts
    if OUTPUT_DIR.exists():
        csv_files = list(OUTPUT_DIR.glob("tweets_*.csv"))
        total_tweets = 0
        per_account = {}
        for cf in csv_files:
            with open(cf, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total_tweets += 1
                    acct = row.get("account", "unknown")
                    per_account[acct] = per_account.get(acct, 0) + 1

        print(f"\n--- Existing Tweet Drafts ---")
        print(f"  Files: {len(csv_files)}")
        print(f"  Total tweets: {total_tweets}")
        for acct, count in sorted(per_account.items()):
            print(f"    {acct}: {count}")
    else:
        print(f"\n  No existing tweet drafts (dir doesn't exist yet)")

    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Generate tweet drafts from ALPHA_STAGING.csv entries"
    )
    parser.add_argument(
        "--batch", "-b", type=int, default=20,
        help="Number of alpha entries to process (default: 20)"
    )
    parser.add_argument(
        "--account", "-a", type=str, default=None,
        help="Filter to specific account (e.g. PRINTMAXXER, repscheme, drifthour, voidpilled, selahmoments)"
    )
    parser.add_argument(
        "--dry-run", "-d", action="store_true",
        help="Print tweets without saving to disk"
    )
    parser.add_argument(
        "--status", "-s", action="store_true",
        help="Show stats about alpha entries and existing drafts"
    )
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    log(f"Starting tweet drafter: batch={args.batch}, account={args.account}, dry_run={args.dry_run}")

    # Read alpha entries
    entries = read_alpha_entries(batch_size=args.batch)
    if not entries:
        log("No processable alpha entries found (APPROVED or PENDING_REVIEW)")
        print("No processable alpha entries found.")
        return

    log(f"Loaded {len(entries)} alpha entries")

    # Generate tweets
    all_tweets: dict[str, list[dict]] = {}
    total_generated = 0
    for entry in entries:
        tweets = generate_tweets_for_entry(entry, target_account=args.account)
        for t in tweets:
            acct = t["account"]
            if acct not in all_tweets:
                all_tweets[acct] = []
            all_tweets[acct].append(t)
            total_generated += 1

    log(f"Generated {total_generated} tweets across {len(all_tweets)} accounts")

    # Output
    files_written = []
    for acct_handle, tweets in sorted(all_tweets.items()):
        result = write_account_csv(acct_handle, tweets, dry_run=args.dry_run)
        if result:
            files_written.append(result)

    # Summary
    print(f"\n--- Tweet Drafter Summary ---")
    print(f"  Alpha entries processed: {len(entries)}")
    print(f"  Total tweets generated: {total_generated}")
    for acct, tweets in sorted(all_tweets.items()):
        print(f"    {acct}: {len(tweets)} tweets")
    if files_written:
        print(f"\n  Files written:")
        for fp in files_written:
            print(f"    {fp}")
    elif not args.dry_run:
        print(f"\n  No files written (no tweets generated)")
    print()


if __name__ == "__main__":
    main()
