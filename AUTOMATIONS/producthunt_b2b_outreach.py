#!/usr/bin/env python3
"""
PRINTMAXX Automation: Product Hunt B2B Lead Scraper & Cold Email Queuer
Daily cron at 6:30 AM — scrapes PH launches, filters B2B, generates
personalized cold emails with beta offer, queues in cold_email_2026.py.
48-hour outreach window enforced; deduplication against prior outreach log.
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path: Path) -> Path:
        resolved = Path(path).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(f"Path escapes project root: {resolved}")
        return resolved

    def recall_skills_for_task(task: str) -> list:
        return []

    def capture_skill_from_result(result: dict, skill: str) -> None:
        pass


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_FILE = AUTOMATIONS_DIR / "logs" / "producthunt_b2b_outreach.log"
LEADS_FILE = PROJECT / "leads" / "producthunt_b2b_leads.csv"
OUTREACH_LOG = AUTOMATIONS_DIR / "logs" / "prior_outreach.json"
QUEUE_FILE = AUTOMATIONS_DIR / "queued_emails.json"
COLD_EMAIL_SCRIPT = PROJECT / "cold_email_2026.py"

PH_API_URL = "https://api.producthunt.com/v2/api/graphql"
PH_POSTS_TODAY_URL = "https://api.producthunt.com/v1/posts"

OUTREACH_WINDOW_HOURS = 48

B2B_KEYWORDS = [
    "b2b", "saas", "api", "enterprise", "workflow", "automation", "crm",
    "erp", "dashboard", "analytics", "integration", "productivity", "team",
    "collaboration", "hr", "payroll", "invoice", "billing", "compliance",
    "devops", "ci/cd", "monitoring", "platform", "management", "reporting",
    "pipeline", "outreach", "sales", "marketing", "seo", "email", "leads",
    "onboarding", "support", "ticketing", "helpdesk", "data", "warehouse",
    "etl", "security", "audit", "finance", "accounting", "legal", "contract",
    "procurement", "logistics", "supply chain", "scheduling", "project",
    "kanban", "agile", "scrum", "documentation", "wiki", "knowledge base",
    "internal tool", "backend", "infrastructure", "cloud", "deployment",
]

B2B_CATEGORIES = [
    "PRODUCTIVITY", "DEVELOPER_TOOLS", "SAAS", "ANALYTICS", "MARKETING",
    "SALES", "DESIGN_TOOLS", "FINANCE", "HUMAN_RESOURCES", "CUSTOMER_SERVICE",
    "SECURITY", "DEVOPS", "DATA_SCIENCE", "PROJECT_MANAGEMENT",
]

BETA_OFFER_TEMPLATE = """\
Subject: Congrats on your {name} launch on Product Hunt! 🎉

Hi {founder_name},

I just saw {name} hit Product Hunt today — congrats on the launch! {tagline_comment}

I'm reaching out from PRINTMAXX. We help B2B teams streamline their print \
and document automation workflows, and we're currently opening up beta access \
to a select group of early-stage SaaS companies.

Given what {name} is building, I think there could be a real fit — especially \
around {relevant_angle}. We'd love to offer you free beta access and work \
closely with your team to make sure it delivers value from day one.

Would you be open to a quick 15-minute call this week to explore?

Either way, congrats again on the launch — it's impressive work.

Best,
PRINTMAXX Team
"""


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    try:
        log_dir = safe_path(LOG_FILE.parent)
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = safe_path(LOG_FILE)
    except Exception:
        log_path = LOG_FILE
        log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("ph_b2b_outreach")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fh = logging.FileHandler(str(log_path), mode="a", encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(fh)

        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(sh)

    return logger


logger = setup_logging()


# ---------------------------------------------------------------------------
# Product Hunt scraping (public API v1 — no auth required for today's posts)
# ---------------------------------------------------------------------------

def fetch_todays_launches() -> list:
    """Fetch today's Product Hunt posts via the public v1 API."""
    url = f"{PH_POSTS_TODAY_URL}?days_ago=0&per_page=50"
    try:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "PRINTMAXX-AutoBot/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            posts = data.get("posts", [])
            logger.info("Fetched %d Product Hunt posts for today.", len(posts))
            return posts
    except urllib.error.HTTPError as exc:
        logger.error("HTTP error fetching PH posts: %s %s", exc.code, exc.reason)
        return []
    except urllib.error.URLError as exc:
        logger.error("URL error fetching PH posts: %s", exc.reason)
        return []
    except Exception as exc:
        logger.error("Unexpected error fetching PH posts: %s", exc)
        return []


# ---------------------------------------------------------------------------
# B2B filtering
# ---------------------------------------------------------------------------

def is_b2b(post: dict) -> bool:
    """Heuristic filter: return True if post appears to be a B2B product."""
    name = (post.get("name") or "").lower()
    tagline = (post.get("tagline") or "").lower()
    description = (post.get("description") or "").lower()
    topics = [t.get("slug", "").upper() for t in (post.get("topics") or [])]

    combined_text = f"{name} {tagline} {description}"

    keyword_match = any(kw in combined_text for kw in B2B_KEYWORDS)
    category_match = any(cat in topics for cat in B2B_CATEGORIES)

    return keyword_match or category_match


def filter_b2b_launches(posts: list) -> list:
    b2b = [p for p in posts if is_b2b(p)]
    logger.info("Filtered %d B2B launches from %d total posts.", len(b2b), len(posts))
    return b2b


# ---------------------------------------------------------------------------
# 48-hour window check
# ---------------------------------------------------------------------------

def within_outreach_window(post: dict) -> bool:
    """Return True if the post was launched within the last 48 hours."""
    launched_at_str = post.get("created_at") or post.get("day")
    if not launched_at_str:
        return True  # assume eligible if no timestamp

    try:
        # PH API returns ISO 8601
        launched_at = datetime.fromisoformat(launched_at_str.replace("Z", "+00:00"))
        cutoff = datetime.now(timezone.utc) - timedelta(hours=OUTREACH_WINDOW_HOURS)
        return launched_at >= cutoff
    except Exception as exc:
        logger.warning("Could not parse launch timestamp '%s': %s", launched_at_str, exc)
        return True


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def load_prior_outreach() -> set:
    """Load set of previously contacted product IDs."""
    try:
        path = safe_path(OUTREACH_LOG)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data.get("contacted_ids", []))
    except Exception as exc:
        logger.warning("Could not load prior outreach log: %s", exc)
    return set()


def save_prior_outreach(contacted_ids: set) -> None:
    """Persist the updated set of contacted product IDs."""
    try:
        path = safe_path(OUTREACH_LOG)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = load_prior_outreach()
        merged = existing | contacted_ids
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"contacted_ids": sorted(merged)}, f, indent=2)
        logger.info("Updated prior outreach log with %d total IDs.", len(merged))
    except Exception as exc:
        logger.error("Failed to save prior outreach log: %s", exc)


def deduplicate(posts: list, prior_ids: set) -> list:
    fresh = [p for p in posts if str(p.get("id", "")) not in prior_ids]
    logger.info(
        "Deduplicated: %d new leads from %d (skipped %d already contacted).",
        len(fresh), len(posts), len(posts) - len(fresh),
    )
    return fresh


# ---------------------------------------------------------------------------
# CSV output
# ---------------------------------------------------------------------------

def write_leads_csv(posts: list, dry_run: bool = False) -> None:
    """Write B2B leads to CSV file."""
    if not posts:
        logger.info("No leads to write.")
        return

    try:
        path = safe_path(LEADS_FILE)
        path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "id", "name", "tagline", "url", "website", "created_at",
            "votes_count", "comments_count", "topics", "maker_name",
            "maker_email", "scraped_at",
        ]

        if dry_run:
            logger.info("[DRY-RUN] Would write %d leads to %s", len(posts), path)
            return

        file_exists = path.exists()
        existing_ids = set()

        if file_exists:
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_ids.add(row.get("id", ""))

        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            written = 0
            for post in posts:
                post_id = str(post.get("id", ""))
                if post_id in existing_ids:
                    continue
                topics_str = ",".join(
                    t.get("slug", "") for t in (post.get("topics") or [])
                )
                makers = post.get("makers") or []
                maker = makers[0] if makers else {}
                writer.writerow({
                    "id": post_id,
                    "name": post.get("name", ""),
                    "tagline": post.get("tagline", ""),
                    "url": post.get("discussion_url", ""),
                    "website": post.get("website", ""),
                    "created_at": post.get("created_at", ""),
                    "votes_count": post.get("votes_count", 0),
                    "comments_count": post.get("comments_count", 0),
                    "topics": topics_str,
                    "maker_name": maker.get("name", ""),
                    "maker_email": maker.get("email", ""),
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
                })
                written += 1

        logger.info("Wrote %d new leads to %s", written, path)

    except ValueError as exc:
        logger.error("Path validation error writing leads CSV: %s", exc)
    except Exception as exc:
        logger.error("Failed to write leads CSV: %s", exc)


# ---------------------------------------------------------------------------
# Email generation
# ---------------------------------------------------------------------------

def generate_email(post: dict) -> dict:
    """Generate a personalized cold email for a B2B Product Hunt launch."""
    name = post.get("name", "your product")
    tagline = post.get("tagline", "")
    makers = post.get("makers") or []
    maker = makers[0] if makers else {}
    founder_name = maker.get("name", "Founder") or "Founder"
    if " " in founder_name:
        founder_name = founder_name.split()[0]

    tagline_comment = (
        f'"{tagline}" sounds like exactly the kind of solution the market needs.'
        if tagline else
        "What you're building sounds genuinely exciting."
    )

    topics = [t.get("slug", "").lower() for t in (post.get("topics") or [])]
    if any(t in topics for t in ["developer-tools", "devops", "api"]):
        relevant_angle = "developer tooling and integration workflows"
    elif any(t in topics for t in ["marketing", "sales", "seo"]):
        relevant_angle = "go-to-market collateral and print automation"
    elif any(t in topics for t in ["productivity", "project-management"]):
        relevant_angle = "internal document workflows and team coordination"
    else:
        relevant_angle = "document and communication workflows"

    body = BETA_OFFER_TEMPLATE.format(
        name=name,
        founder_name=founder_name,
        tagline_comment=tagline_comment,
        relevant_angle=relevant_angle,
    )

    subject_line = f"Congrats on your {name} launch on Product Hunt!"

    return {
        "to_name": maker.get("name", ""),
        "to_email": maker.get("email", ""),
        "product_name": name,
        "product_url": post.get("discussion_url", ""),
        "subject": subject_line,
        "body": body,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "producthunt",
        "post_id": str(post.get("id", "")),
    }


# ---------------------------------------------------------------------------
# Queue emails into cold_email_2026.py pipeline
# ---------------------------------------------------------------------------

def queue_emails(emails: list, dry_run: bool = False) -> None:
    """Append generated emails to the queue file and invoke the pipeline."""
    if not emails:
        logger.info("No emails to queue.")
        return

    try:
        queue_path = safe_path(QUEUE_FILE)
        queue_path.parent.mkdir(parents=True, exist_ok=True)

        existing = []
        if queue_path.exists():
            with open(queue_path, "r", encoding="utf-8") as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = []

        if dry_run:
            logger.info("[DRY-RUN] Would queue %d emails to %s", len(emails), queue_path)
            for email in emails:
                logger.info(
                    "[DRY-RUN]   -> %s <%s>: %s",
                    email.get("to_name"), email.get("to_email"), email.get("subject"),
                )
            return

        combined = existing + emails
        with open(queue_path, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2)

        logger.info("Queued %d emails (total in queue: %d).", len(emails), len(combined))

        # Invoke the cold_email_2026.py pipeline if it exists
        pipeline = safe_path(COLD_EMAIL_SCRIPT)
        if pipeline.exists():
            try:
                result = subprocess.run(
                    [sys.executable, str(pipeline), "--process-queue", str(queue_path)],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if result.returncode == 0:
                    logger.info("cold_email_2026.py pipeline completed successfully.")
                    if result.stdout.strip():
                        logger.info("Pipeline stdout: %s", result.stdout.strip())
                else:
                    logger.error(
                        "cold_email_2026.py exited with code %d. stderr: %s",
                        result.returncode, result.stderr.strip(),
                    )
            except subprocess.TimeoutExpired:
                logger.error("cold_email_2026.py pipeline timed out after 120s.")
            except Exception as exc:
                logger.error("Failed to invoke cold_email_2026.py: %s", exc)
        else:
            logger.warning(
                "cold_email_2026.py not found at %s — emails queued but pipeline not run.",
                pipeline,
            )

    except ValueError as exc:
        logger.error("Path validation error queuing emails: %s", exc)
    except Exception as exc:
        logger.error("Failed to queue emails: %s", exc)


# ---------------------------------------------------------------------------
# Status report
# ---------------------------------------------------------------------------

def print_status() -> None:
    """Print current status of leads file, outreach log, and email queue."""
    print("\n=== PRINTMAXX Product Hunt B2B Outreach Status ===\n")

    # Leads CSV
    try:
        leads_path = safe_path(LEADS_FILE)
        if leads_path.exists():
            with open(leads_path, "r", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            print(f"Leads CSV:        {leads_path}")
            print(f"  Total leads:    {len(rows)}")
            if rows:
                recent = sorted(rows, key=lambda r: r.get("scraped_at", ""), reverse=True)[:3]
                print("  Recent leads:")
                for r in recent:
                    print(f"    - {r.get('name', 'N/A')} ({r.get('created_at', 'N/A')})")
        else:
            print(f"Leads CSV:        {leads_path} [NOT FOUND]")
    except Exception as exc:
        print(f"Leads CSV:        ERROR — {exc}")

    print()

    # Prior outreach log
    try:
        prior_ids = load_prior_outreach()
        print(f"Prior outreach:   {len(prior_ids)} products already contacted")
    except Exception as exc:
        print(f"Prior outreach:   ERROR — {exc}")

    print()

    # Email queue
    try:
        queue_path = safe_path(QUEUE_FILE)
        if queue_path.exists():
            with open(queue_path, "r", encoding="utf-8") as f:
                queue = json.load(f)
            print(f"Email queue:      {queue_path}")
            print(f"  Queued emails:  {len(queue)}")
        else:
            print(f"Email queue:      {queue_path} [EMPTY / NOT FOUND]")
    except Exception as exc:
        print(f"Email queue:      ERROR — {exc}")

    print()

    # Log file
    try:
        log_path = safe_path(LOG_FILE)
        if log_path.exists():
            size_kb = log_path.stat().st_size / 1024
            print(f"Log file:         {log_path} ({size_kb:.1f} KB)")
        else:
            print(f"Log file:         {log_path} [NOT FOUND]")
    except Exception as exc:
        print(f"Log file:         ERROR — {exc}")

    print()


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(dry_run: bool = False) -> int:
    """
    Full pipeline:
    1. Fetch today's PH launches
    2. Filter B2B
    3. Enforce 48h window
    4. Deduplicate
    5. Write leads CSV
    6. Generate and queue emails
    Returns count of new leads processed.
    """
    recall_skills_for_task("product_hunt_b2b_outreach")

    logger.info("=== PRINTMAXX PH B2B Outreach pipeline START%s ===",
                " [DRY-RUN]" if dry_run else "")

    # Step 1: Fetch
    posts = fetch_todays_launches()
    if not posts:
        logger.warning("No posts fetched. Exiting pipeline.")
        return 0

    # Step 2: B2B filter
    b2b_posts = filter_b2b_launches(posts)
    if not b2b_posts:
        logger.info("No B2B posts found today.")
        return 0

    # Step 3: 48h window
    in_window = [p for p in b2b_posts if within_outreach_window(p)]
    skipped_window = len(b2b_posts) - len(in_window)
    if skipped_window:
        logger.info("Skipped %d posts outside 48h outreach window.", skipped_window)
    if not in_window:
        logger.info("All B2B posts are outside the 48h window.")
        return 0

    # Step 4: Deduplicate
    prior_ids = load_prior_outreach()
    new_posts = deduplicate(in_window, prior_ids)
    if not new_posts:
        logger.info("All leads already contacted. Nothing to do.")
        return 0

    # Step 5: Write leads CSV
    write_leads_csv(new_posts, dry_run=dry_run)

    # Step 6: Generate and queue emails
    emails = []
    for post in new_posts:
        try:
            email = generate_email(post)
            emails.append(email)
            logger.info(
                "Generated email for: %s (id=%s)",
                post.get("name", "N/A"), post.get("id", "N/A"),
            )
        except Exception as exc:
            logger.error("Failed to generate email for post %s: %s", post.get("id"), exc)

    queue_emails(emails, dry_run=dry_run)

    # Persist contacted IDs
    if not dry_run:
        new_ids = {str(p.get("id", "")) for p in new_posts}
        save_prior_outreach(new_ids)
        result_summary = {
            "run_at": datetime.now(timezone.utc).isoformat(),
            "posts_fetched": len(posts),
            "b2b_filtered": len(b2b_posts),
            "in_window": len(in_window),
            "new_leads": len(new_posts),
            "emails_queued": len(emails),
        }
        capture_skill_from_result(result_summary, "product_hunt_b2b_outreach")

    logger.info(
        "=== Pipeline COMPLETE: %d new leads, %d emails queued ===",
        len(new_posts), len(emails),
    )
    return len(new_posts)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: Product Hunt B2B Lead Scraper & Cold Email Queuer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --run           # Run the full pipeline\n"
            "  %(prog)s --dry-run       # Simulate without writing files\n"
            "  %(prog)s --status        # Show current pipeline status\n"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Run the full PH B2B scrape and email queue pipeline.",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate pipeline execution without writing files or queuing emails.",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print current status of leads, outreach log, and email queue.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.status:
            print_status()
            sys.exit(0)

        elif args.dry_run:
            count = run_pipeline(dry_run=True)
            logger.info("[DRY-RUN] Would have processed %d new leads.", count)
            sys.exit(0)

        elif args.run:
            count = run_pipeline(dry_run=False)
            sys.exit(0 if count >= 0 else 1)

    except KeyboardInterrupt:
        logger.warning("Interrupted by user.")
        sys.exit(130)
    except Exception as exc:
        logger.error("Fatal error in main: %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()