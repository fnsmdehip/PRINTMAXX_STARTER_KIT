#!/usr/bin/env python3
"""
PRINTMAXX Alpha Research Runner
================================

Reads RESEARCH TASKS created by the alpha_auto_processor and runs web searches
to enrich them. Uses Reddit JSON API and source URL metadata extraction to find
competitive data, market signals, and related discussions.

The alpha_auto_processor (Route C) writes RESEARCH TASK entries to
ALPHA_STAGING.csv with status CONVERTED_TO_RESEARCH and generates cron entries
in AUTOMATIONS/auto_generated_cron_entries.txt.

This script picks up those entries, runs enrichment research, and writes
results to LEDGER/ALPHA_RESEARCH_RESULTS.csv.

Usage:
    python3 AUTOMATIONS/alpha_research_runner.py --scan              # Find entries needing research
    python3 AUTOMATIONS/alpha_research_runner.py --run               # Run research (default batch 10)
    python3 AUTOMATIONS/alpha_research_runner.py --run --batch-size 5 # Process 5 entries
    python3 AUTOMATIONS/alpha_research_runner.py --status            # Show research stats
    python3 AUTOMATIONS/alpha_research_runner.py --dry-run           # Preview without writing
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import ssl
import sys
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALPHA_CSV = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
RESEARCH_RESULTS_CSV = PROJECT_ROOT / "LEDGER" / "ALPHA_RESEARCH_RESULTS.csv"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
LOG_FILE = LOG_DIR / "alpha_research.log"

RESULTS_FIELDNAMES = [
    "alpha_id",
    "original_tactic",
    "research_query",
    "findings_summary",
    "reddit_discussions_found",
    "source_metadata",
    "enrichment_date",
    "research_status",
]

# Reddit API rate limit: 2 seconds between requests
REDDIT_RATE_LIMIT_SECONDS = 2

# Keywords that signal an entry is research-worthy even without explicit
# RESEARCH status (tools, competitors, market data)
RESEARCH_TRIGGER_KEYWORDS = [
    "competitor", "market", "tool", "platform", "pricing",
    "alternative", "compare", "benchmark", "trend", "emerging",
    "monitor", "track", "scan", "scrape", "analyze",
    "saas", "app store", "revenue", "growth", "churn",
    "api", "integration", "framework", "library", "sdk",
    "niche", "opportunity", "demand", "supply", "gap",
]

# User-Agent for HTTP requests (Reddit requires a meaningful UA)
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36 "
    "PRINTMAXX-Research/1.0"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def today_str() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")


def log(msg: str) -> None:
    """Append to log file and print to stderr."""
    ts = now_iso()
    line = f"[{ts}] {msg}"
    print(line, file=sys.stderr)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def safe_path(target: Path) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def truncate(text: str, max_len: int = 500) -> str:
    """Truncate text to max_len, adding ... if truncated."""
    text = text.strip()
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def clean_text(text: str) -> str:
    """Strip HTML entities and excessive whitespace."""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_search_query(row: dict) -> str:
    """
    Build a search query string from an alpha entry.
    Extracts the most meaningful terms from tactic, category, and extracted_method.
    """
    parts = []

    tactic = str(row.get("tactic", "")).strip()
    extracted_method = str(row.get("extracted_method", "")).strip()
    category = str(row.get("category", "")).strip()

    # Prefer extracted_method if available (it is typically concise)
    if extracted_method and len(extracted_method) > 5:
        parts.append(extracted_method)
    elif tactic:
        # Take the first meaningful sentence from the tactic
        sentences = re.split(r"[.!?\n]", tactic)
        for s in sentences:
            s = s.strip()
            if len(s) > 10:
                parts.append(s[:120])
                break

    # Add category as context
    if category:
        cat_clean = category.replace("_", " ").lower()
        parts.append(cat_clean)

    query = " ".join(parts)
    # Remove special characters that break URL encoding
    query = re.sub(r"[^\w\s\-/]", " ", query)
    query = re.sub(r"\s+", " ", query).strip()

    # Cap at 100 chars for search queries
    if len(query) > 100:
        query = query[:100].rsplit(" ", 1)[0]

    return query


# ---------------------------------------------------------------------------
# HTTP helpers (stdlib only)
# ---------------------------------------------------------------------------

def _create_ssl_context() -> ssl.SSLContext:
    """Create an SSL context that skips verification for flaky certs."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _http_get(url: str, timeout: int = 15) -> tuple[int, str, dict]:
    """
    Perform an HTTP GET request using urllib.

    Returns: (status_code, body_text, response_headers_dict)
    Raises no exceptions -- returns (-1, error_message, {}) on failure.
    """
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", USER_AGENT)
        req.add_header("Accept", "application/json, text/html, */*")

        ctx = _create_ssl_context()
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="replace")
            headers = dict(resp.headers)
            return (status, body, headers)
    except urllib.error.HTTPError as e:
        return (e.code, f"HTTPError: {e.code} {e.reason}", {})
    except urllib.error.URLError as e:
        return (-1, f"URLError: {e.reason}", {})
    except Exception as e:
        return (-1, f"Error: {type(e).__name__}: {e}", {})


# ---------------------------------------------------------------------------
# Reddit search
# ---------------------------------------------------------------------------

def search_reddit(query: str, limit: int = 10) -> list[dict]:
    """
    Search Reddit via the public JSON API.

    Returns a list of dicts with keys: title, subreddit, score, num_comments,
    url, selftext_snippet, created_utc.
    """
    encoded = urllib.parse.quote_plus(query)
    url = f"https://www.reddit.com/search.json?q={encoded}&limit={limit}&sort=relevance&t=year"

    log(f"  Reddit search: {query[:80]}")
    status, body, _ = _http_get(url, timeout=20)

    if status != 200:
        log(f"  Reddit search failed: status={status}, body={body[:200]}")
        return []

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        log("  Reddit search: failed to parse JSON")
        return []

    results = []
    children = data.get("data", {}).get("children", [])
    for child in children:
        d = child.get("data", {})
        selftext = clean_text(str(d.get("selftext", "")))
        results.append({
            "title": clean_text(str(d.get("title", ""))),
            "subreddit": str(d.get("subreddit", "")),
            "score": int(d.get("score", 0)),
            "num_comments": int(d.get("num_comments", 0)),
            "url": f"https://reddit.com{d.get('permalink', '')}",
            "selftext_snippet": truncate(selftext, 200),
            "created_utc": int(d.get("created_utc", 0)),
        })

    return results


def summarize_reddit_results(results: list[dict]) -> tuple[str, str]:
    """
    Summarize Reddit search results into two strings:
    - findings_summary: key takeaways
    - discussions_found: compact listing of top posts
    """
    if not results:
        return ("No Reddit discussions found", "0 discussions")

    # Sort by score descending
    results.sort(key=lambda r: r["score"], reverse=True)

    # Build discussions listing
    discussion_lines = []
    for i, r in enumerate(results[:5], 1):
        discussion_lines.append(
            f"[{i}] r/{r['subreddit']} | {r['score']}pts {r['num_comments']}comments | {r['title'][:80]}"
        )
    discussions_str = "; ".join(discussion_lines)

    # Build findings summary
    total_score = sum(r["score"] for r in results)
    total_comments = sum(r["num_comments"] for r in results)
    top_subreddits = list({r["subreddit"] for r in results[:5]})

    summary_parts = [
        f"Found {len(results)} related discussions",
        f"total engagement: {total_score} upvotes / {total_comments} comments",
        f"top subreddits: {', '.join(top_subreddits[:5])}",
    ]

    # Extract key themes from top 3 results
    if results:
        top_titles = [r["title"][:60] for r in results[:3]]
        summary_parts.append(f"top topics: {' | '.join(top_titles)}")

    # Check for high-signal discussions
    high_signal = [r for r in results if r["score"] > 100 or r["num_comments"] > 50]
    if high_signal:
        summary_parts.append(
            f"{len(high_signal)} high-signal thread(s) (100+ upvotes or 50+ comments)"
        )

    findings = ". ".join(summary_parts)
    return (truncate(findings, 800), truncate(discussions_str, 500))


# ---------------------------------------------------------------------------
# Source URL metadata extraction
# ---------------------------------------------------------------------------

def extract_source_metadata(url: str) -> str:
    """
    Try to extract metadata from a source URL (title, description, etc.).
    Returns a summary string.
    """
    if not url or not url.startswith("http"):
        return "No source URL"

    log(f"  Fetching metadata: {url[:80]}")
    status, body, headers = _http_get(url, timeout=10)

    if status != 200:
        return f"URL unreachable (status {status})"

    metadata_parts = []

    # Extract <title>
    title_match = re.search(r"<title[^>]*>(.*?)</title>", body, re.IGNORECASE | re.DOTALL)
    if title_match:
        title = clean_text(title_match.group(1))
        metadata_parts.append(f"title: {truncate(title, 120)}")

    # Extract meta description
    desc_match = re.search(
        r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']',
        body,
        re.IGNORECASE,
    )
    if not desc_match:
        desc_match = re.search(
            r'<meta\s+[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\']',
            body,
            re.IGNORECASE,
        )
    if desc_match:
        desc = clean_text(desc_match.group(1))
        metadata_parts.append(f"description: {truncate(desc, 200)}")

    # Extract og:title and og:description as fallback
    og_title_match = re.search(
        r'<meta\s+[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']*)["\']',
        body,
        re.IGNORECASE,
    )
    if og_title_match and not title_match:
        metadata_parts.append(f"og_title: {clean_text(og_title_match.group(1))[:120]}")

    og_desc_match = re.search(
        r'<meta\s+[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']*)["\']',
        body,
        re.IGNORECASE,
    )
    if og_desc_match and not desc_match:
        metadata_parts.append(f"og_desc: {clean_text(og_desc_match.group(1))[:200]}")

    # Content-Type from headers
    content_type = headers.get("Content-Type", "")
    if content_type:
        metadata_parts.append(f"content_type: {content_type.split(';')[0].strip()}")

    # Check for GitHub-specific metadata
    if "github.com" in url.lower():
        # Try to find repo stars / description
        stars_match = re.search(
            r'<span[^>]*class="[^"]*Counter[^"]*"[^>]*>(\d[\d,.]*)</span>',
            body,
        )
        if stars_match:
            metadata_parts.append(f"github_stars: {stars_match.group(1)}")

        about_match = re.search(
            r'<p[^>]*class="[^"]*f4[^"]*"[^>]*>(.*?)</p>',
            body,
            re.DOTALL,
        )
        if about_match:
            about = clean_text(about_match.group(1))
            metadata_parts.append(f"repo_about: {truncate(about, 150)}")

    if not metadata_parts:
        return "URL reachable but no extractable metadata"

    return " | ".join(metadata_parts)


# ---------------------------------------------------------------------------
# Research entry identification
# ---------------------------------------------------------------------------

def is_research_worthy(row: dict) -> bool:
    """
    Determine if an alpha entry needs research.

    An entry is research-worthy if:
    1. Its status contains 'RESEARCH' (e.g., CONVERTED_TO_RESEARCH)
    2. Its tactic text mentions research-worthy topics (tools, competitors, etc.)
    """
    status = str(row.get("status", "")).strip().upper()

    # Direct status match
    if "RESEARCH" in status:
        return True

    # Check tactic text for research trigger keywords
    tactic = str(row.get("tactic", "")).lower()
    extracted_method = str(row.get("extracted_method", "")).lower()
    combined = f"{tactic} {extracted_method}"

    keyword_hits = sum(1 for kw in RESEARCH_TRIGGER_KEYWORDS if kw in combined)
    # Require at least 2 keyword hits to avoid false positives
    if keyword_hits >= 2:
        return True

    return False


def already_researched(row: dict) -> bool:
    """Check if an entry has already been researched."""
    notes = str(row.get("reviewer_notes", ""))
    if "[RESEARCHED:" in notes:
        return True
    return False


def find_research_entries(rows: list[dict]) -> list[dict]:
    """Find all entries that need research and have not been researched yet."""
    entries = []
    for row in rows:
        if is_research_worthy(row) and not already_researched(row):
            entries.append(row)
    return entries


# ---------------------------------------------------------------------------
# CSV I/O
# ---------------------------------------------------------------------------

def read_alpha_csv() -> tuple[list[str], list[dict]]:
    """Read ALPHA_STAGING.csv, return (fieldnames, rows)."""
    target = safe_path(ALPHA_CSV)
    if not target.exists():
        log(f"ERROR: {target} not found")
        sys.exit(1)

    rows = []
    fieldnames = []
    with open(target, "r", newline="", errors="replace") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        for row in reader:
            rows.append(row)
    return fieldnames, rows


def write_alpha_csv(fieldnames: list[str], rows: list[dict]) -> None:
    """Write back the full ALPHA_STAGING.csv."""
    target = safe_path(ALPHA_CSV)
    with open(target, "w", newline="", errors="replace") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_existing_results() -> set[str]:
    """Read existing research results to avoid re-processing."""
    target = safe_path(RESEARCH_RESULTS_CSV)
    already_done = set()
    if target.exists():
        with open(target, "r", newline="", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                aid = str(row.get("alpha_id", "")).strip()
                if aid:
                    already_done.add(aid)
    return already_done


def append_research_result(result: dict) -> None:
    """Append a single research result to ALPHA_RESEARCH_RESULTS.csv."""
    target = safe_path(RESEARCH_RESULTS_CSV)
    file_exists = target.exists()

    with open(target, "a", newline="", errors="replace") as f:
        writer = csv.DictWriter(f, fieldnames=RESULTS_FIELDNAMES, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        writer.writerow(result)


# ---------------------------------------------------------------------------
# Core research pipeline
# ---------------------------------------------------------------------------

def research_single_entry(row: dict, dry_run: bool = False) -> dict:
    """
    Run research on a single alpha entry.

    Returns a result dict ready for ALPHA_RESEARCH_RESULTS.csv.
    """
    alpha_id = str(row.get("alpha_id", "UNKNOWN"))
    tactic = str(row.get("tactic", ""))
    source_url = str(row.get("source_url", "")).strip()
    enrichment_date = today_str()

    # Build search query
    query = build_search_query(row)
    if not query or len(query) < 5:
        log(f"  [{alpha_id}] Skipped: no meaningful query could be built")
        return {
            "alpha_id": alpha_id,
            "original_tactic": truncate(tactic, 300),
            "research_query": "",
            "findings_summary": "Could not build a meaningful search query",
            "reddit_discussions_found": "0 discussions",
            "source_metadata": "N/A",
            "enrichment_date": enrichment_date,
            "research_status": "SKIPPED",
        }

    log(f"  [{alpha_id}] Researching: {query[:60]}...")

    findings_summary = ""
    discussions_found = ""
    source_metadata = ""
    research_status = "COMPLETE"

    if not dry_run:
        # 1. Reddit search
        reddit_results = search_reddit(query, limit=10)
        findings_summary, discussions_found = summarize_reddit_results(reddit_results)

        # Rate limit between Reddit and source URL fetch
        time.sleep(REDDIT_RATE_LIMIT_SECONDS)

        # 2. Source URL metadata
        source_metadata = extract_source_metadata(source_url)
    else:
        findings_summary = f"[DRY RUN] Would search Reddit for: {query}"
        discussions_found = "[DRY RUN] No actual search performed"
        source_metadata = f"[DRY RUN] Would fetch: {source_url}"
        research_status = "DRY_RUN"

    result = {
        "alpha_id": alpha_id,
        "original_tactic": truncate(tactic, 300),
        "research_query": query,
        "findings_summary": findings_summary,
        "reddit_discussions_found": discussions_found,
        "source_metadata": source_metadata,
        "enrichment_date": enrichment_date,
        "research_status": research_status,
    }

    return result


def run_research(
    rows: list[dict],
    batch_size: int = 10,
    dry_run: bool = False,
) -> list[dict]:
    """
    Run research on pending entries.

    Returns list of result dicts that were processed.
    """
    # Find entries needing research
    pending = find_research_entries(rows)

    # Filter out already-processed entries from the results CSV
    already_done = read_existing_results()
    pending = [
        r for r in pending
        if str(r.get("alpha_id", "")).strip() not in already_done
    ]

    if not pending:
        log("No entries pending research")
        return []

    log(f"Found {len(pending)} entries needing research, processing batch of {batch_size}")

    # Limit to batch size
    batch = pending[:batch_size]
    results = []
    last_request_time = 0.0

    for i, row in enumerate(batch, 1):
        alpha_id = str(row.get("alpha_id", "UNKNOWN"))
        log(f"[{i}/{len(batch)}] Processing {alpha_id}")

        # Rate limit between entries (2 second minimum gap)
        elapsed = time.time() - last_request_time
        if elapsed < REDDIT_RATE_LIMIT_SECONDS and i > 1:
            wait = REDDIT_RATE_LIMIT_SECONDS - elapsed
            log(f"  Rate limiting: waiting {wait:.1f}s")
            time.sleep(wait)

        last_request_time = time.time()

        try:
            result = research_single_entry(row, dry_run=dry_run)
            results.append(result)

            # Write result to CSV immediately (not in dry run)
            if not dry_run:
                append_research_result(result)

            # Update the original row's reviewer_notes
            if not dry_run and result["research_status"] == "COMPLETE":
                existing_notes = str(row.get("reviewer_notes", "")).strip()
                research_tag = f"[RESEARCHED: {today_str()}]"
                if existing_notes:
                    row["reviewer_notes"] = f"{existing_notes} {research_tag}"
                else:
                    row["reviewer_notes"] = research_tag

            log(f"  [{alpha_id}] {result['research_status']}: {result['findings_summary'][:80]}")

        except Exception as e:
            log(f"  [{alpha_id}] ERROR: {type(e).__name__}: {e}")
            error_result = {
                "alpha_id": alpha_id,
                "original_tactic": truncate(str(row.get("tactic", "")), 300),
                "research_query": build_search_query(row),
                "findings_summary": f"Error during research: {e}",
                "reddit_discussions_found": "0 discussions",
                "source_metadata": "Error",
                "enrichment_date": today_str(),
                "research_status": "ERROR",
            }
            results.append(error_result)
            if not dry_run:
                append_research_result(error_result)

    return results


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def cmd_scan() -> None:
    """Find all entries needing research."""
    _, rows = read_alpha_csv()
    pending = find_research_entries(rows)

    # Filter out already-processed
    already_done = read_existing_results()
    pending = [
        r for r in pending
        if str(r.get("alpha_id", "")).strip() not in already_done
    ]

    print(f"\n=== ALPHA RESEARCH SCAN ===\n")
    print(f"Total alpha entries:       {len(rows)}")
    print(f"Entries needing research:  {len(pending)}")
    print(f"Already researched:        {len(already_done)}")

    if pending:
        print(f"\n--- Pending Research Entries (showing first 20) ---\n")
        for i, row in enumerate(pending[:20], 1):
            alpha_id = row.get("alpha_id", "?")
            status = row.get("status", "?")
            tactic = truncate(str(row.get("tactic", "")), 80)
            category = row.get("category", "?")
            source = row.get("source", "?")
            query = build_search_query(row)
            print(f"  {i:2d}. [{alpha_id}] ({status}) [{category}]")
            print(f"      Source: {source}")
            print(f"      Tactic: {tactic}")
            print(f"      Query:  {query[:80]}")
            print()

        if len(pending) > 20:
            print(f"  ... and {len(pending) - 20} more entries")
    else:
        print("\nNo entries pending research. All caught up.")
    print()


def cmd_status() -> None:
    """Show research statistics."""
    _, rows = read_alpha_csv()
    already_done = read_existing_results()

    # Count entries by research state
    research_status_entries = [r for r in rows if "RESEARCH" in str(r.get("status", "")).upper()]
    keyword_worthy = [
        r for r in rows
        if not "RESEARCH" in str(r.get("status", "")).upper()
        and is_research_worthy(r)
    ]
    researched = [r for r in rows if "[RESEARCHED:" in str(r.get("reviewer_notes", ""))]

    print(f"\n=== ALPHA RESEARCH STATUS ===\n")
    print(f"Total alpha entries:               {len(rows)}")
    print(f"Entries with RESEARCH status:       {len(research_status_entries)}")
    print(f"Entries with research keywords:     {len(keyword_worthy)}")
    print(f"Total research-worthy:              {len(research_status_entries) + len(keyword_worthy)}")
    print(f"Already researched (tagged):        {len(researched)}")
    print(f"Results in results CSV:             {len(already_done)}")

    # Show results breakdown if results exist
    if RESEARCH_RESULTS_CSV.exists():
        status_counts: dict[str, int] = {}
        with open(safe_path(RESEARCH_RESULTS_CSV), "r", newline="", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rs = row.get("research_status", "UNKNOWN")
                status_counts[rs] = status_counts.get(rs, 0) + 1

        if status_counts:
            print(f"\n--- Results Breakdown ---\n")
            for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
                bar = "#" * min(count, 40)
                print(f"  {status:15s} {count:>5d}  {bar}")

    # Show last few log entries
    if LOG_FILE.exists():
        print(f"\n--- Recent Log ---\n")
        try:
            lines = LOG_FILE.read_text().strip().split("\n")
            for line in lines[-5:]:
                print(f"  {line}")
        except Exception:
            print("  (could not read log)")

    print()


def cmd_run(batch_size: int = 10, dry_run: bool = False) -> None:
    """Run research on pending entries."""
    mode = "DRY RUN" if dry_run else "LIVE"
    log(f"=== Alpha Research Runner starting ({mode}) ===")

    fieldnames, rows = read_alpha_csv()
    log(f"Loaded {len(rows)} rows from ALPHA_STAGING.csv")

    results = run_research(rows, batch_size=batch_size, dry_run=dry_run)

    # Write back ALPHA_STAGING.csv with updated reviewer_notes
    if not dry_run and results:
        write_alpha_csv(fieldnames, rows)
        log("ALPHA_STAGING.csv updated with [RESEARCHED: date] tags")

    # Report
    completed = sum(1 for r in results if r["research_status"] == "COMPLETE")
    errors = sum(1 for r in results if r["research_status"] == "ERROR")
    skipped = sum(1 for r in results if r["research_status"] == "SKIPPED")
    dry_runs = sum(1 for r in results if r["research_status"] == "DRY_RUN")

    report = textwrap.dedent(f"""
    === ALPHA RESEARCH RUNNER REPORT ({mode}) ===

    Entries processed:   {len(results)}
    Completed:           {completed}
    Errors:              {errors}
    Skipped:             {skipped}
    Dry run:             {dry_runs}

    Results written to:  {RESEARCH_RESULTS_CSV}
    Log file:            {LOG_FILE}
    """)

    print(report)
    log(report.strip())
    log("=== Alpha Research Runner complete ===")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Alpha Research Runner: enrich alpha entries with web research."
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Find all entries needing research",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run research on pending entries (default batch of 10)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Number of entries to process per batch (default: 10)",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show research statistics",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without writing any changes",
    )
    args = parser.parse_args()

    # If --dry-run is passed alone (no --run), treat it as --run --dry-run
    if args.dry_run and not args.run and not args.scan and not args.status:
        args.run = True

    if args.scan:
        cmd_scan()
    elif args.status:
        cmd_status()
    elif args.run:
        cmd_run(batch_size=args.batch_size, dry_run=args.dry_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
