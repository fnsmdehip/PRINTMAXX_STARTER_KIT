#!/usr/bin/env python3
"""
Auto Freelance Responder — Scan → Generate Response → Post → Track
=====================================================================
Finds hot freelance jobs from scanner output, generates personalized
responses, and auto-posts to Reddit / queues bids for Upwork/Fiverr.

The edge: Claude Max ($200/mo) lets you vibe-code deliverables in 15-60 min.
95%+ margin on every project. This script finds and responds to jobs
automatically so you never miss a hot opportunity.

Usage:
    python3 AUTOMATIONS/auto_freelance_responder.py --scan-and-respond
    python3 AUTOMATIONS/auto_freelance_responder.py --dry-run
    python3 AUTOMATIONS/auto_freelance_responder.py --status
    python3 AUTOMATIONS/auto_freelance_responder.py --generate-samples
    python3 AUTOMATIONS/auto_freelance_responder.py --post-pending
    python3 AUTOMATIONS/auto_freelance_responder.py --cron

Cron entry (every 2 hours, 15 min after scanner):
    15 */2 * * * cd $BASE && $PYTHON AUTOMATIONS/auto_freelance_responder.py --cron >> AUTOMATIONS/logs/auto_responder.log 2>&1
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from hashlib import md5

# ── Paths ────────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent
AUTOMATIONS = BASE / "AUTOMATIONS"
LEDGER = BASE / "LEDGER"
RESPONSES_DIR = AUTOMATIONS / "freelance_responses_auto"
TEMPLATES_DIR = AUTOMATIONS / "freelance_response_templates"
LOGS_DIR = AUTOMATIONS / "logs"
RESPONSE_LOG = RESPONSES_DIR / "response_log.csv"
SCAN_CSV = LEDGER / "FREELANCE_DEMAND_SCAN.csv"
PIPELINE_CSV = LEDGER / "FREELANCE_PIPELINE_ACTIVE.csv"
CREDENTIALS_FILE = BASE / "SECRETS" / "CREDENTIALS.env"

# ── Config ───────────────────────────────────────────────────────────────────
MIN_SCORE = 50          # minimum score to auto-respond
MAX_AGE_HOURS = 24      # don't respond to posts older than this
MAX_RESPONSES_PER_RUN = 5   # rate limit responses per cron run
RESPONSE_COOLDOWN_HOURS = 4  # don't re-respond to same subreddit within N hours

# ── Services we can deliver with Claude Max ──────────────────────────────────
VIBE_CODE_SERVICES = {
    "website": {
        "name": "Website / Landing Page",
        "delivery": "24-48h",
        "price_floor": 99,
        "portfolio": [
            "https://dental-motion.surge.sh",
            "https://realtor-motion.surge.sh",
            "https://restaurant-motion.surge.sh",
            "https://printmaxx-portfolio.surge.sh",
        ],
        # Keep outbound copy strictly truthful: never claim volume metrics unless verified.
        "pitch_angle": "i build modern, responsive sites and can share a quick sample mockup for your niche",
        "sample_type": "personalized landing page mockup",
    },
    "automation": {
        "name": "Automation / Scripts / Bots",
        "delivery": "12-24h",
        "price_floor": 79,
        "portfolio": [],
        "pitch_angle": "i build automation workflows (Python + cron, APIs, data pipelines) and can ship a working script + README fast",
        "sample_type": "working script demo",
    },
    "data_entry": {
        "name": "Data Entry / Research / VA Work",
        "delivery": "same day",
        "price_floor": 15,
        "portfolio": [],
        "pitch_angle": "i use AI-assisted workflows to move fast while keeping accuracy high (happy to do a small sample first)",
        "sample_type": "sample data extraction",
    },
    "logo": {
        "name": "Logo / Graphic Design",
        "delivery": "24h",
        "price_floor": 50,
        "portfolio": [],
        "pitch_angle": "i do logo design with AI-assisted workflows. 3-5 concepts in 24h, unlimited revisions included",
        "sample_type": "3 logo concept mockups",
    },
    "social_media": {
        "name": "Social Media Management",
        "delivery": "ongoing",
        "price_floor": 200,
        "portfolio": [],
        "pitch_angle": "i can set up a content pipeline + calendar and provide a 7-day plan + sample posts in your tone",
        "sample_type": "7-day content calendar + 5 sample posts",
    },
    "presentation": {
        "name": "Presentation / Pitch Deck",
        "delivery": "24-48h",
        "price_floor": 75,
        "portfolio": [],
        "pitch_angle": "clean, modern decks. no template garbage. designed from scratch based on your brand and story",
        "sample_type": "3-slide preview",
    },
    "scraper": {
        "name": "Web Scraper / Data Extraction",
        "delivery": "12-24h",
        "price_floor": 79,
        "portfolio": [
            "https://sitescore-app.surge.sh",
            "https://printmaxx-analyzer.surge.sh",
        ],
        "pitch_angle": "i build scrapers that can run on a schedule and deliver code + sample output quickly",
        "sample_type": "working scraper with sample output",
    },
}


def load_scan_results():
    """Load latest freelance demand scan results."""
    if not SCAN_CSV.exists():
        return []
    results = []
    with open(SCAN_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                score = int(row.get("score", 0))
                age_h = float(row.get("age_hours", 999))
                if score >= MIN_SCORE and age_h <= MAX_AGE_HOURS:
                    results.append(row)
            except (ValueError, TypeError):
                continue
    return sorted(results, key=lambda x: int(x.get("score", 0)), reverse=True)


def load_response_log():
    """Load previously sent responses to avoid duplicates."""
    if not RESPONSE_LOG.exists():
        return set()
    sent = set()
    with open(RESPONSE_LOG, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sent.add(row.get("post_id", ""))
    return sent


def get_post_id(row):
    """Generate unique ID for a post."""
    title = row.get("title", "")
    source = row.get("source", "")
    return md5(f"{source}:{title}".encode()).hexdigest()[:12]


def match_services(row):
    """Match a job post to our deliverable services."""
    services_str = row.get("services", "")
    title = row.get("title", "").lower()
    matched = []
    for svc_key, svc in VIBE_CODE_SERVICES.items():
        if svc_key in services_str:
            matched.append(svc_key)
        elif any(kw in title for kw in [svc_key, svc["name"].lower().split("/")[0].strip()]):
            matched.append(svc_key)
    return matched if matched else ["website"]  # default to website


def generate_response(row, services):
    """Generate a personalized response for a Reddit post."""
    title = row.get("title", "")
    budget = row.get("budget", "N/A")
    source = row.get("source", "")
    score = row.get("score", "?")
    age = row.get("age_hours", "?")

    primary_svc = services[0]
    svc = VIBE_CODE_SERVICES[primary_svc]

    # build portfolio links
    portfolio_links = ""
    if svc["portfolio"]:
        portfolio_links = "\n".join([f"  - {url}" for url in svc["portfolio"][:3]])
        portfolio_links = f"\n\nhere are a few live examples of my work:\n{portfolio_links}"

    # price positioning: undercut budget by 10-20% if stated, or use our floor
    price_note = ""
    if budget and budget != "N/A":
        try:
            budget_num = int(re.sub(r'[^\d]', '', str(budget)))
            our_price = max(svc["price_floor"], int(budget_num * 0.85))
            price_note = f"\n\ni can do this for ${our_price}. delivery in {svc['delivery']}."
        except ValueError:
            price_note = f"\n\npricing depends on scope. typically {svc['delivery']} delivery."
    else:
        price_note = f"\n\npricing depends on scope. typically {svc['delivery']} delivery."

    # the response (following copy-style rules - no AI slop, no chatbot artifacts)
    response = f"""hey, {svc['pitch_angle']}.{portfolio_links}{price_note}

dm me if you want to see a quick sample before committing. i can put something together in a few hours so you know exactly what you're getting."""

    return response.strip()


def generate_sample_spec(row, services):
    """Generate a spec for building a free sample deliverable."""
    primary_svc = services[0]
    svc = VIBE_CODE_SERVICES[primary_svc]
    title = row.get("title", "")
    budget = row.get("budget", "N/A")

    spec = {
        "job_title": title,
        "service": svc["name"],
        "sample_type": svc["sample_type"],
        "budget": budget,
        "approach": f"build {svc['sample_type']} using Claude Max. should take 15-60 min.",
        "delivery_plan": f"1. build sample ({svc['sample_type']})\n2. reply with sample + price\n3. follow up via DM with full portfolio\n4. deliver final in {svc['delivery']}",
    }
    return spec


def save_response(row, response, services, status="PENDING"):
    """Save generated response to file and log."""
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)

    post_id = get_post_id(row)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"{timestamp}_{post_id}.md"
    filepath = RESPONSES_DIR / filename

    title = row.get("title", "")
    source = row.get("source", "")
    budget = row.get("budget", "N/A")
    score = row.get("score", "?")
    url = row.get("url", "")

    content = f"""# Auto-Generated Freelance Response
**Post:** {title}
**Source:** {source}
**Score:** {score}
**Budget:** {budget}
**URL:** {url}
**Generated:** {datetime.now().isoformat()}
**Status:** {status}
**Services:** {', '.join(services)}

---

## RESPONSE (copy-paste ready)

{response}

---

## SAMPLE DELIVERABLE SPEC

{json.dumps(generate_sample_spec(row, services), indent=2)}

---

## FOLLOW-UP DM

hey, i left a comment on your post about {services[0]}. wanted to follow up directly.

i put together a quick sample based on your requirements. take a look and let me know if the direction works for you.

if you want to move forward, i can have the full deliverable ready in {VIBE_CODE_SERVICES[services[0]]['delivery']}.
"""

    filepath.write_text(content)

    # log it
    log_exists = RESPONSE_LOG.exists()
    with open(RESPONSE_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        if not log_exists:
            writer.writerow(["timestamp", "post_id", "title", "source", "score", "budget", "services", "status", "file"])
        writer.writerow([
            datetime.now().isoformat(),
            post_id,
            title[:80],
            source,
            score,
            budget,
            "|".join(services),
            status,
            str(filepath.relative_to(BASE)),
        ])

    return filepath


def post_to_reddit(row, response):
    """Post response to Reddit. Requires REDDIT_* credentials in CREDENTIALS.env."""
    creds = load_credentials()
    if not creds.get("REDDIT_USERNAME") or not creds.get("REDDIT_PASSWORD"):
        return False, "no reddit credentials configured"

    # Reddit API auth
    client_id = creds.get("REDDIT_CLIENT_ID", "")
    client_secret = creds.get("REDDIT_CLIENT_SECRET", "")
    username = creds.get("REDDIT_USERNAME", "")
    password = creds.get("REDDIT_PASSWORD", "")

    if not client_id or not client_secret:
        return False, "missing REDDIT_CLIENT_ID or REDDIT_CLIENT_SECRET in CREDENTIALS.env"

    try:
        # get auth token
        auth_data = f"grant_type=password&username={username}&password={password}".encode()
        auth_req = urllib.request.Request(
            "https://www.reddit.com/api/v1/access_token",
            data=auth_data,
            method="POST",
        )
        auth_req.add_header("User-Agent", "PrintmaxxFreelanceBot/1.0")

        import base64
        credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        auth_req.add_header("Authorization", f"Basic {credentials}")

        with urllib.request.urlopen(auth_req, timeout=15) as resp:
            token_data = json.loads(resp.read().decode())
            access_token = token_data.get("access_token")

        if not access_token:
            return False, "failed to get reddit auth token"

        # extract post ID from URL
        url = row.get("url", "")
        post_id_match = re.search(r'/comments/([a-z0-9]+)/', url)
        if not post_id_match:
            return False, f"can't extract post ID from URL: {url}"

        reddit_post_id = post_id_match.group(1)

        # post comment
        comment_data = f"api_type=json&thing_id=t3_{reddit_post_id}&text={urllib.parse.quote(response)}".encode()
        comment_req = urllib.request.Request(
            "https://oauth.reddit.com/api/comment",
            data=comment_data,
            method="POST",
        )
        comment_req.add_header("User-Agent", "PrintmaxxFreelanceBot/1.0")
        comment_req.add_header("Authorization", f"bearer {access_token}")

        with urllib.request.urlopen(comment_req, timeout=15) as resp:
            result = json.loads(resp.read().decode())

        errors = result.get("json", {}).get("errors", [])
        if errors:
            return False, f"reddit API errors: {errors}"

        return True, "posted successfully"

    except Exception as e:
        return False, f"reddit post failed: {str(e)}"


def load_credentials():
    """Load credentials from CREDENTIALS.env."""
    creds = {}
    if CREDENTIALS_FILE.exists():
        with open(CREDENTIALS_FILE) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    creds[key.strip()] = val.strip().strip('"').strip("'")
    return creds


def scan_and_respond(dry_run=False, max_responses=MAX_RESPONSES_PER_RUN):
    """Main pipeline: scan results → generate responses → post (or dry-run)."""
    results = load_scan_results()
    if not results:
        print("  no hot opportunities found in latest scan.")
        return 0

    already_sent = load_response_log()
    responses_generated = 0

    print(f"\n  found {len(results)} opportunities scoring {MIN_SCORE}+ and under {MAX_AGE_HOURS}h old")
    print(f"  already responded to {len(already_sent)} posts")
    print(f"  mode: {'DRY RUN (no posting)' if dry_run else 'LIVE (will post if credentials exist)'}")
    print()

    for row in results:
        if responses_generated >= max_responses:
            print(f"  rate limit: generated {max_responses} responses this run. remaining queued for next run.")
            break

        post_id = get_post_id(row)
        if post_id in already_sent:
            continue

        services = match_services(row)
        response = generate_response(row, services)

        title = row.get("title", "")[:60]
        source = row.get("source", "")
        score = row.get("score", "?")
        budget = row.get("budget", "N/A")

        print(f"  [{score}] {source}: {title}")
        print(f"       services: {', '.join(services)} | budget: {budget}")

        if dry_run:
            filepath = save_response(row, response, services, status="DRY_RUN")
            print(f"       saved: {filepath.name}")
        else:
            # try posting to reddit
            posted, msg = post_to_reddit(row, response)
            if posted:
                filepath = save_response(row, response, services, status="POSTED")
                print(f"       POSTED to Reddit")
            else:
                filepath = save_response(row, response, services, status="PENDING")
                print(f"       saved as PENDING ({msg})")

        responses_generated += 1
        print()

    return responses_generated


def show_status():
    """Show pipeline status."""
    print("\n" + "=" * 60)
    print("  FREELANCE AUTO-RESPONDER STATUS")
    print("=" * 60)

    # scan data
    results = load_scan_results()
    print(f"\n  hot opportunities (score {MIN_SCORE}+, <{MAX_AGE_HOURS}h): {len(results)}")

    # response log
    already_sent = load_response_log()
    print(f"  responses generated: {len(already_sent)}")

    # pending responses
    if RESPONSES_DIR.exists():
        pending = list(RESPONSES_DIR.glob("*.md"))
        print(f"  response files: {len(pending)}")

    # credentials check
    creds = load_credentials()
    reddit_ready = bool(creds.get("REDDIT_USERNAME") and creds.get("REDDIT_CLIENT_ID"))
    upwork_ready = bool(creds.get("UPWORK_USERNAME"))
    fiverr_ready = bool(creds.get("FIVERR_USERNAME"))

    print(f"\n  platform readiness:")
    print(f"    reddit:  {'READY' if reddit_ready else 'NEEDS CREDENTIALS'}")
    print(f"    upwork:  {'READY' if upwork_ready else 'NEEDS ACCOUNT'}")
    print(f"    fiverr:  {'READY' if fiverr_ready else 'NEEDS ACCOUNT'}")

    # vibe code services
    print(f"\n  services we can deliver ({len(VIBE_CODE_SERVICES)}):")
    for key, svc in VIBE_CODE_SERVICES.items():
        print(f"    {key:15s} ${svc['price_floor']:>4}+  {svc['delivery']:>8}  {len(svc['portfolio'])} portfolio items")

    # top opportunities
    if results:
        print(f"\n  top 5 hot opportunities:")
        for r in results[:5]:
            title = r.get("title", "")[:50]
            score = r.get("score", "?")
            budget = r.get("budget", "N/A")
            source = r.get("source", "")
            age = r.get("age_hours", "?")
            post_id = get_post_id(r)
            already = " [RESPONDED]" if post_id in already_sent else ""
            print(f"    [{score}] {source}: {title}... ${budget} ({age}h){already}")

    print()


def generate_sample_deliverables():
    """Generate sample deliverable specs for top opportunities."""
    results = load_scan_results()
    if not results:
        print("  no opportunities to generate samples for.")
        return

    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    specs_file = RESPONSES_DIR / f"sample_specs_{datetime.now().strftime('%Y%m%d')}.json"
    specs = []

    print(f"\n  generating sample deliverable specs for top {min(5, len(results))} opportunities:\n")

    for row in results[:5]:
        services = match_services(row)
        spec = generate_sample_spec(row, services)
        specs.append(spec)
        print(f"  {spec['job_title'][:50]}")
        print(f"    service: {spec['service']}")
        print(f"    sample: {spec['sample_type']}")
        print(f"    approach: {spec['approach']}")
        print()

    with open(specs_file, "w") as f:
        json.dump(specs, f, indent=2)
    print(f"  specs saved: {specs_file.name}")


def cron_run():
    """Cron mode: scan + respond (dry-run if no credentials)."""
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    creds = load_credentials()
    has_reddit = bool(creds.get("REDDIT_USERNAME") and creds.get("REDDIT_CLIENT_ID"))

    count = scan_and_respond(dry_run=not has_reddit)
    # one-line log for cron
    print(f"{timestamp} | responses: {count} | mode: {'live' if has_reddit else 'dry-run'}")


def main():
    parser = argparse.ArgumentParser(description="Auto Freelance Responder")
    parser.add_argument("--scan-and-respond", action="store_true", help="scan + generate + post responses")
    parser.add_argument("--dry-run", action="store_true", help="scan + generate responses without posting")
    parser.add_argument("--status", action="store_true", help="show pipeline status")
    parser.add_argument("--generate-samples", action="store_true", help="generate sample deliverable specs")
    parser.add_argument("--post-pending", action="store_true", help="post pending responses that have credentials now")
    parser.add_argument("--cron", action="store_true", help="cron mode: auto dry-run or live based on credentials")
    parser.add_argument("--max", type=int, default=MAX_RESPONSES_PER_RUN, help="max responses per run")

    args = parser.parse_args()

    os.chdir(str(BASE))

    print()
    print("=" * 60)
    print("  PRINTMAXX AUTO FREELANCE RESPONDER")
    print(f"  {len(VIBE_CODE_SERVICES)} vibe-codeable services | Claude Max edge")
    print("=" * 60)

    if args.status:
        show_status()
    elif args.generate_samples:
        generate_sample_deliverables()
    elif args.dry_run:
        count = scan_and_respond(dry_run=True, max_responses=args.max)
        print(f"  total: {count} responses generated (dry-run)")
    elif args.scan_and_respond:
        count = scan_and_respond(dry_run=False, max_responses=args.max)
        print(f"  total: {count} responses generated")
    elif args.post_pending:
        # TODO: iterate pending responses and post them
        print("  posting pending responses...")
        print("  (requires Reddit/Upwork/Fiverr credentials in SECRETS/CREDENTIALS.env)")
    elif args.cron:
        cron_run()
    else:
        show_status()


if __name__ == "__main__":
    main()
