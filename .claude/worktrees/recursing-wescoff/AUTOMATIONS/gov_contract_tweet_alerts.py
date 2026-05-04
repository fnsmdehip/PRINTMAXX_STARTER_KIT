#!/usr/bin/env python3

from __future__ import annotations
"""
Gov Contract Tweet Alert Generator
------------------------------------
Reads SAM.gov and gov tenders CSVs, filters for high-value / upcoming deadline
opportunities, and generates tweet-formatted alerts in Buffer-compatible CSV.

Usage:
    python3 gov_contract_tweet_alerts.py
    python3 gov_contract_tweet_alerts.py --min-value 1000000
    python3 gov_contract_tweet_alerts.py --max-tweets 30

Output: AUTOMATIONS/content_posting/gov_contract_tweets.csv
"""

import argparse
import csv
import os
import re
import sys
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAM_GOV_CSV = os.path.join(SCRIPT_DIR, "leads", "sam_gov_opportunities.csv")
TENDERS_CSV = os.path.join(SCRIPT_DIR, "leads", "gov_tenders_active.csv")
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "content_posting", "gov_contract_tweets.csv")


def parse_date(date_str):
    """Try multiple date formats and return a datetime or None."""
    if not date_str or not date_str.strip():
        return None
    date_str = date_str.strip()
    for fmt in (
        "%Y-%m-%dT%H:%M:%S+00:00",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%Y-%m-%dT%H:%M:%S",
    ):
        try:
            return datetime.strptime(date_str[:19], fmt[:fmt.count("%") * 3 + fmt.count("-") + fmt.count("T") + fmt.count(":") + 10])
        except (ValueError, IndexError):
            pass
    # Last resort: try parsing just the date portion
    try:
        return datetime.strptime(date_str[:10], "%Y-%m-%d")
    except (ValueError, IndexError):
        return None


def parse_dollar_amount(val):
    """Parse a dollar amount string into a float, or return 0."""
    if not val or not val.strip():
        return 0.0
    cleaned = re.sub(r"[^0-9.]", "", val.strip())
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def format_dollar(amount):
    """Format a dollar amount for tweets: $1.2B, $45M, $250K, $5K."""
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.1f}B"
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    if amount >= 1_000:
        return f"${amount / 1_000:.0f}K"
    if amount > 0:
        return f"${amount:,.0f}"
    return ""


def shorten_agency(agency):
    """Shorten long agency names for tweet brevity."""
    replacements = {
        "DEPT OF DEFENSE": "DoD",
        "DEPARTMENT OF DEFENSE": "DoD",
        "DEPT OF THE ARMY": "Army",
        "DEPT OF THE AIR FORCE": "Air Force",
        "DEPT OF THE NAVY": "Navy",
        "VETERANS AFFAIRS, DEPARTMENT OF": "VA",
        "Department of Veterans Affairs": "VA",
        "JUSTICE, DEPARTMENT OF": "DOJ",
        "Department of Justice": "DOJ",
        "HOMELAND SECURITY, DEPARTMENT OF": "DHS",
        "Department of Homeland Security": "DHS",
        "INTERIOR, DEPARTMENT OF THE": "DOI",
        "AGRICULTURE, DEPARTMENT OF": "USDA",
        "HEALTH AND HUMAN SERVICES, DEPARTMENT OF": "HHS",
        "Department of Health and Human Services": "HHS",
        "GENERAL SERVICES ADMINISTRATION": "GSA",
        "General Services Administration": "GSA",
        "Department of Energy": "DOE",
        "ENERGY, DEPARTMENT OF": "DOE",
        "Department of State": "State Dept",
        "STATE, DEPARTMENT OF": "State Dept",
        "Department of Transportation": "DOT",
        "TRANSPORTATION, DEPARTMENT OF": "DOT",
        "Social Security Administration": "SSA",
        "FEDERAL PRISON SYSTEM / BUREAU OF PRISONS": "BOP",
        "DEFENSE LOGISTICS AGENCY": "DLA",
        "Smithsonian Institution": "Smithsonian",
    }
    for long_name, short_name in replacements.items():
        if agency.upper().startswith(long_name.upper()) or agency == long_name:
            return short_name
    # Fallback: truncate if too long
    if len(agency) > 25:
        return agency[:22] + "..."
    return agency


def shorten_title(title, max_len=100):
    """Shorten a title, removing common prefixes and noise."""
    # Remove common prefixes and bracketed tags
    title = re.sub(r"^\[.*?\]\s*", "", title)
    for prefix in (
        "RFI ",
        "Sources Sought Notice ",
        "IGF::OT::IGF ",
        "IGF::CL,CT::IGF ",
        "TAS::89 0240::TAS ",
    ):
        if title.startswith(prefix):
            title = title[len(prefix):]
    # Remove solicitation numbers embedded in titles
    title = re.sub(r"\b[A-Z0-9]{5,}-\d{2,}-[A-Z0-9-]+\b", "", title).strip()
    # Remove leading/trailing punctuation
    title = title.strip(" -:,")
    if len(title) > max_len:
        title = title[:max_len - 3].rsplit(" ", 1)[0] + "..."
    return title


def load_sam_gov():
    """Load SAM.gov opportunities CSV."""
    records = []
    if not os.path.exists(SAM_GOV_CSV):
        print(f"  SAM.gov CSV not found: {SAM_GOV_CSV}")
        return records
    with open(SAM_GOV_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "source": "SAM.gov",
                "title": row.get("title", ""),
                "agency": row.get("agency", ""),
                "sub_agency": row.get("sub_agency", ""),
                "deadline": row.get("response_deadline", ""),
                "posted_date": row.get("posted_date", ""),
                "amount": 0.0,  # SAM.gov search results don't have dollar amounts
                "set_aside": row.get("set_aside_description", ""),
                "notice_type": row.get("opportunity_type", ""),
                "location": row.get("place_of_performance_state", ""),
                "url": row.get("sam_gov_link", ""),
                "naics": row.get("naics_code", ""),
                "category": "",
            })
    print(f"  Loaded {len(records)} SAM.gov opportunities")
    return records


def load_tenders():
    """Load gov tenders active CSV."""
    records = []
    if not os.path.exists(TENDERS_CSV):
        print(f"  Tenders CSV not found: {TENDERS_CSV}")
        return records
    with open(TENDERS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            amount = parse_dollar_amount(row.get("award_amount", "") or row.get("budget_high", ""))
            records.append({
                "source": "USAspending",
                "title": row.get("title", ""),
                "agency": row.get("agency", ""),
                "sub_agency": row.get("sub_agency", ""),
                "deadline": row.get("deadline", ""),
                "posted_date": row.get("posted_date", ""),
                "amount": amount,
                "set_aside": row.get("set_aside_description", ""),
                "notice_type": row.get("notice_type", ""),
                "location": row.get("location", ""),
                "url": row.get("url", ""),
                "naics": row.get("naics_code", ""),
                "category": row.get("category", ""),
            })
    print(f"  Loaded {len(records)} gov tenders")
    return records


def score_opportunity(record):
    """Score an opportunity for tweet-worthiness (higher = better)."""
    score = 0

    # Dollar value scoring
    amt = record["amount"]
    if amt >= 1_000_000_000:
        score += 50
    elif amt >= 100_000_000:
        score += 40
    elif amt >= 10_000_000:
        score += 30
    elif amt >= 1_000_000:
        score += 20
    elif amt >= 100_000:
        score += 10

    # Deadline proximity (upcoming = more urgent = more tweetable)
    deadline_dt = parse_date(record["deadline"])
    if deadline_dt:
        days_until = (deadline_dt - datetime.now()).days
        if 0 < days_until <= 7:
            score += 25  # This week
        elif 7 < days_until <= 14:
            score += 15  # Next week
        elif 14 < days_until <= 30:
            score += 10  # This month

    # Small business set-aside (our audience)
    set_aside = record.get("set_aside", "")
    if set_aside and "small business" in set_aside.lower():
        score += 15
    if set_aside and ("8(a)" in set_aside or "veteran" in set_aside.lower() or "women" in set_aside.lower()):
        score += 10

    # IT / tech / software related (our niche)
    title_lower = record["title"].lower()
    tech_keywords = ["software", "IT ", "web ", "data", "cyber", "cloud", "digital", "tech", "computer", "AI ", "network"]
    for kw in tech_keywords:
        if kw.lower() in title_lower:
            score += 10
            break

    # Penalize generic/boring
    boring_keywords = ["kosher", "meats", "subsistence", "custodial", "cleaning", "mowing"]
    for kw in boring_keywords:
        if kw.lower() in title_lower:
            score -= 20

    # Recency bonus
    posted_dt = parse_date(record["posted_date"])
    if posted_dt:
        days_old = (datetime.now() - posted_dt).days
        if days_old <= 3:
            score += 10
        elif days_old <= 7:
            score += 5

    # SAM.gov active solicitations get a base boost (real bidding opportunities)
    notice_type = record.get("notice_type", "").lower()
    if "solicitation" in notice_type or "combined synopsis" in notice_type:
        score += 10

    return score


def generate_tweet(record):
    """Generate a single tweet from an opportunity record. Must be under 280 chars."""
    agency = shorten_agency(record["agency"])
    title = shorten_title(record["title"], max_len=90)
    amount_str = format_dollar(record["amount"])
    deadline_dt = parse_date(record["deadline"])
    source = record["source"]

    # Build deadline string
    deadline_str = ""
    if deadline_dt:
        days_until = (deadline_dt - datetime.now()).days
        if days_until > 0:
            deadline_str = f"Due {deadline_dt.strftime('%b %d')}"
        elif days_until == 0:
            deadline_str = "Due TODAY"
        else:
            deadline_str = f"Closed {deadline_dt.strftime('%b %d')}"

    # Build set-aside tag
    set_aside = record.get("set_aside", "")
    sa_tag = ""
    if set_aside:
        if "small business" in set_aside.lower():
            sa_tag = "SB set-aside"
        elif "8(a)" in set_aside:
            sa_tag = "8(a)"
        elif "veteran" in set_aside.lower():
            sa_tag = "SDVOSB"
        elif "women" in set_aside.lower():
            sa_tag = "WOSB"
        elif "hubzone" in set_aside.lower():
            sa_tag = "HUBZone"

    # Location
    loc = record.get("location", "")
    loc_str = f" | {loc}" if loc and len(loc) <= 3 else ""

    # Construct tweet variants based on available data
    parts = []

    if amount_str and deadline_str:
        parts.append(f"{agency}: {title}")
        parts.append(f"{amount_str} | {deadline_str}{loc_str}")
        if sa_tag:
            parts.append(sa_tag)
        parts.append("#GovContracts #FedBiz")
    elif amount_str:
        parts.append(f"{agency}: {title}")
        parts.append(f"Value: {amount_str}{loc_str}")
        if sa_tag:
            parts.append(sa_tag)
        parts.append("#GovContracts #FedBiz")
    elif deadline_str:
        parts.append(f"{agency}: {title}")
        parts.append(f"{deadline_str}{loc_str}")
        if sa_tag:
            parts.append(sa_tag)
        parts.append("#GovContracts #FedBiz")
    else:
        parts.append(f"{agency}: {title}")
        if sa_tag:
            parts.append(sa_tag)
        parts.append("#GovContracts #FedBiz")

    tweet = "\n".join(parts)

    # Ensure under 280 chars
    if len(tweet) > 280:
        # Trim title further
        title = shorten_title(record["title"], max_len=60)
        parts[0] = f"{agency}: {title}"
        tweet = "\n".join(parts)

    if len(tweet) > 280:
        # Drop hashtags
        tweet = "\n".join(parts[:-1])

    if len(tweet) > 280:
        tweet = tweet[:277] + "..."

    return tweet


def generate_schedule_dates(count, start_date=None, posts_per_day=3):
    """Generate scheduled dates for tweets, spacing them throughout the day."""
    if start_date is None:
        start_date = datetime.now() + timedelta(days=1)
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

    hours = [9, 13, 17]  # 9 AM, 1 PM, 5 PM
    dates = []
    day = 0
    idx = 0
    while len(dates) < count:
        current_date = start_date + timedelta(days=day)
        hour = hours[idx % len(hours)]
        scheduled = current_date.replace(hour=hour, minute=0)
        dates.append(scheduled.strftime("%Y-%m-%d %H:%M"))
        idx += 1
        if idx % posts_per_day == 0:
            day += 1
    return dates


def main():
    parser = argparse.ArgumentParser(description="Gov Contract Tweet Alert Generator")
    parser.add_argument("--min-value", type=float, default=0, help="Minimum dollar value filter")
    parser.add_argument("--max-tweets", type=int, default=30, help="Maximum tweets to generate")
    parser.add_argument("--output", default=OUTPUT_CSV, help="Output CSV path")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print("  PRINTMAXX Gov Contract Tweet Alert Generator")
    print(f"{'='*60}")

    # Load data
    all_records = []
    all_records.extend(load_sam_gov())
    all_records.extend(load_tenders())

    if not all_records:
        print("  No records found. Ensure CSVs exist in AUTOMATIONS/leads/")
        sys.exit(1)

    print(f"  Total records loaded: {len(all_records)}")

    # Filter by minimum value if specified
    if args.min_value > 0:
        all_records = [r for r in all_records if r["amount"] >= args.min_value]
        print(f"  After min-value filter (${args.min_value:,.0f}): {len(all_records)}")

    # Score and rank
    scored = []
    for record in all_records:
        score = score_opportunity(record)
        scored.append((score, record))

    scored.sort(key=lambda x: x[0], reverse=True)

    # Take top N
    top = scored[:args.max_tweets]
    print(f"  Generating tweets for top {len(top)} opportunities...")

    # Generate tweets
    tweets = []
    seen_titles = set()
    for score, record in top:
        title_key = record["title"][:50].lower()
        if title_key in seen_titles:
            continue
        seen_titles.add(title_key)

        tweet_text = generate_tweet(record)
        tweets.append({
            "text": tweet_text,
            "score": score,
            "source": record["source"],
            "amount": record["amount"],
        })

    # Generate schedule dates
    schedule_dates = generate_schedule_dates(len(tweets))

    # Write Buffer-compatible CSV
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "scheduled_date"])
        for i, tweet in enumerate(tweets):
            scheduled = schedule_dates[i] if i < len(schedule_dates) else ""
            writer.writerow([tweet["text"], scheduled])

    print(f"\n  Wrote {len(tweets)} tweets to: {args.output}")

    # Print preview
    print(f"\n{'='*60}")
    print("  TWEET PREVIEWS (top 5)")
    print(f"{'='*60}")
    for i, tweet in enumerate(tweets[:5], 1):
        print(f"\n  [{i}] (score: {tweet['score']}, {tweet['source']}, {format_dollar(tweet['amount']) or 'no $'})")
        print(f"  {'-'*50}")
        for line in tweet["text"].split("\n"):
            print(f"    {line}")
        print(f"    ({len(tweet['text'])} chars)")

    # Stats
    print(f"\n{'='*60}")
    print("  STATS")
    print(f"{'='*60}")
    print(f"  Total tweets generated: {len(tweets)}")
    sam_count = sum(1 for t in tweets if t["source"] == "SAM.gov")
    tender_count = sum(1 for t in tweets if t["source"] == "USAspending")
    print(f"  From SAM.gov: {sam_count}")
    print(f"  From USAspending: {tender_count}")
    high_value = sum(1 for t in tweets if t["amount"] >= 1_000_000)
    print(f"  High-value ($1M+): {high_value}")
    avg_len = sum(len(t["text"]) for t in tweets) / len(tweets) if tweets else 0
    print(f"  Avg tweet length: {avg_len:.0f} chars")
    over_280 = sum(1 for t in tweets if len(t["text"]) > 280)
    print(f"  Over 280 chars: {over_280}")
    print(f"\n  Output: {args.output}")
    print(f"  Upload to Buffer using: {os.path.join(SCRIPT_DIR, 'content_posting', 'BUFFER_UPLOAD_GUIDE.md')}")


if __name__ == "__main__":
    main()
