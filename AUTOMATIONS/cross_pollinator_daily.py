#!/usr/bin/env python3
"""
CROSS-POLLINATOR DAILY BRIDGE
Wires new daily intelligence into downstream ventures.
Called by cross_pollinator_v2.py or standalone.

New connections added 2026-04-01:
  1. New Opportunities → Cold Outreach Angles (OPP files → outreach email context)
  2. New Digital Products (PDFs) → Posting Queue (awareness posts for new products)
  3. New Affiliate Pages → Affiliate Distribute Targets (new pages need traffic)
  4. New Opportunities (DIGITAL_PRODUCTS type) → Product Creation Queue
  5. Reddit scrapes → Alpha Staging pipeline (today's unprocessed entries)

Run: python3 AUTOMATIONS/cross_pollinator_daily.py --cycle
"""

import csv
import json
import re
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT_ROOT / "AUTOMATIONS"
LEDGER = PROJECT_ROOT / "LEDGER"
CONTENT = PROJECT_ROOT / "CONTENT" / "social"
OPP_DIR = AUTOMATIONS / "agent" / "swarm" / "opportunities"
REPORTS = AUTOMATIONS / "agent" / "swarm" / "reports"
POSTING_QUEUE = CONTENT / "posting_queue"
OUTBOUND = AUTOMATIONS / "leads" / "auto_outbound_cold_outreach_engine_9569"
AUTO_STATE = AUTOMATIONS / "agent" / "autonomy"
LANDING = PROJECT_ROOT / "LANDING"
DIGITAL_PRODUCTS = PROJECT_ROOT / "DIGITAL_PRODUCTS" / "ready_to_sell" / "pdfs"
ALPHA_STAGING = LEDGER / "ALPHA_STAGING.csv"
REDDIT_OUTPUT = AUTOMATIONS / "reddit_scraper_output"

NOW = datetime.now()
TODAY = NOW.strftime("%Y%m%d")
TIMESTAMP = NOW.strftime("%Y-%m-%dT%H:%M:%S")

results = {}
total_wired = 0


def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} outside project root")
    return resolved


def wire_new_opportunities_to_outreach_angles():
    """Connection 1: New OPP files from today → Cold Outreach Angles context."""
    global total_wired
    angles_path = safe_path(OUTBOUND / "opportunity_angles.json")

    # Load existing angles
    existing = []
    if angles_path.exists():
        try:
            existing = json.loads(angles_path.read_text(encoding="utf-8"))
        except Exception:
            existing = []

    existing_ids = {a.get("opp_id") for a in existing if isinstance(a, dict)}

    # Read all OPP files and extract high-score ones
    new_angles = []
    if OPP_DIR.exists():
        for opp_file in sorted(OPP_DIR.glob("OPP_*.md")):
            opp_id = opp_file.stem
            if opp_id in existing_ids:
                continue

            content = opp_file.read_text(encoding="utf-8", errors="ignore")

            # Extract score
            score_match = re.search(r"\*\*Score:\s*([\d.]+)/10\*\*", content)
            score = float(score_match.group(1)) if score_match else 0.0

            if score < 7.5:
                continue  # Only wire high-score opportunities to outreach

            # Extract category
            cat_match = re.search(r"\*\*Category:\s*([^*]+)\*\*", content)
            category = cat_match.group(1).strip() if cat_match else "UNKNOWN"

            # Extract "What" section as the angle
            what_match = re.search(r"## What\s*\n+(.*?)(?=\n##|\Z)", content, re.DOTALL)
            what_text = what_match.group(1).strip()[:300] if what_match else content[:200]

            new_angles.append({
                "opp_id": opp_id,
                "score": score,
                "category": category,
                "angle": what_text,
                "source_file": str(opp_file.name),
                "added_at": TIMESTAMP,
            })

    if new_angles:
        all_angles = existing + new_angles
        angles_path.write_text(json.dumps(all_angles, indent=2))
        results["New Opportunities → Outreach Angles"] = {
            "status": "OK",
            "items_wired": len(new_angles),
            "total_in_file": len(all_angles),
        }
        total_wired += len(new_angles)
    else:
        results["New Opportunities → Outreach Angles"] = {
            "status": "OK",
            "items_wired": 0,
            "note": "deduped, no new high-score opps",
        }
    print(f"  [{'+'  if new_angles else '-'}] New Opportunities → Outreach Angles: {len(new_angles)} (OK)")


def wire_new_pdfs_to_posting_queue():
    """Connection 2: New PDFs in DIGITAL_PRODUCTS → Posting Queue content stubs."""
    global total_wired
    registry_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "pdf_posting_registry.json")

    # Load existing registry
    existing_pdfs = set()
    if registry_path.exists():
        try:
            existing_pdfs = set(json.loads(registry_path.read_text(encoding="utf-8")))
        except Exception:
            existing_pdfs = set()

    new_posts = []
    new_pdf_ids = []

    if DIGITAL_PRODUCTS.exists():
        for pdf in sorted(DIGITAL_PRODUCTS.glob("*.pdf")):
            pdf_name = pdf.stem
            if pdf_name in existing_pdfs:
                continue

            # Parse the number prefix (e.g., "14_CLAUDE_CODE_AGENT_BIBLE")
            match = re.match(r"^(\d+)_(.+)$", pdf_name)
            if not match:
                continue

            num = int(match.group(1))
            slug = match.group(2)
            title = slug.replace("_", " ").title()

            # Generate a simple hook tweet for the product
            hook = _generate_product_hook(num, title)

            post_filename = f"{TODAY}_product_amplify_{num}.md"
            post_path = safe_path(POSTING_QUEUE / post_filename)

            if not post_path.exists():
                post_path.write_text(
                    f"# Product Amplify: {title}\n\n"
                    f"Platform: X/Twitter\n"
                    f"Format: Single tweet\n"
                    f"Status: READY TO POST\n\n"
                    f"---\n\n"
                    f"{hook}\n\n"
                    f"---\n\n"
                    f"Product: {title}\n"
                    f"Source: DIGITAL_PRODUCTS/ready_to_sell/pdfs/{pdf.name}\n"
                    f"Generated: {TIMESTAMP}\n",
                    encoding="utf-8",
                )
                new_posts.append(post_filename)

            new_pdf_ids.append(pdf_name)

    if new_pdf_ids:
        updated_registry = list(existing_pdfs | set(new_pdf_ids))
        registry_path.write_text(json.dumps(updated_registry, indent=2))

    results["New PDFs → Posting Queue"] = {
        "status": "OK",
        "items_wired": len(new_posts),
        "posts_created": new_posts[:5],
    }
    if new_posts:
        total_wired += len(new_posts)
    print(f"  [{'+'  if new_posts else '-'}] New PDFs → Posting Queue: {len(new_posts)} (OK)")


def _generate_product_hook(num: int, title: str) -> str:
    hooks = {
        "CLAUDE CODE AGENT BIBLE": "I built 50+ automated agents in 90 days. Every pattern, every prompt, every system.\n\nNow it's a PDF. The Claude Code Agent Bible.\n\nFree for the first 48 hours.",
        "CLAUDE CODE FOR SOLOPRENEURS": "Solopreneurs who know Claude Code are building in 1 day what used to take a developer a week.\n\nHere's the exact playbook.",
        "CLAUDE CODE FOR NONTECHNICAL FOUNDERS": "You don't need to code.\n\nYou need to know how to DIRECT code.\n\nThis PDF teaches non-technical founders how to ship with Claude Code.",
        "CLAUDE CODE FOR CONTENT CREATORS": "Content creators using Claude Code are automating:\n- Article drafts\n- SEO research\n- Social scheduling\n- Email sequences\n\nFull system inside.",
        "BEFORE YOU FAMILY STORY WORKBOOK": "Your grandparents have stories you'll never hear unless you ask NOW.\n\nThis workbook makes the conversation easy.",
        "REDDIT MONEY MACHINE": "Reddit has $0 → $3K/month case studies posted every week.\n\nMost people scroll past them.\n\nThis PDF teaches you to extract the systems.",
        "CLAUDE CODE MASTERY": "I went from zero to shipping 8 apps in 30 days using only Claude Code.\n\nHere's the exact method.",
        "COLD EMAIL SYSTEM": "Cold email still works. The people who say it doesn't are sending generic AI slop.\n\nHere's a system that gets 15-40% reply rates.",
        "PROMPT VAULT": "I collected 200+ high-signal prompts from indie hackers, solopreneurs, and agency owners.\n\nAll in one vault.",
    }
    # Match by key substring
    for key, hook in hooks.items():
        if key in title.upper():
            return hook
    return f"New resource: {title}\n\nCovering what most people skip when building online income systems."


def wire_new_affiliate_pages_to_distribute_targets():
    """Connection 3: New affiliate landing pages → Affiliate Distribute Targets."""
    global total_wired
    targets_path = safe_path(AUTO_STATE / "affiliate_distribute_targets.json")

    existing_targets = []
    existing_urls = set()
    if targets_path.exists():
        try:
            existing_targets = json.loads(targets_path.read_text(encoding="utf-8"))
            existing_urls = {t.get("url") for t in existing_targets if isinstance(t, dict)}
        except Exception:
            pass

    affiliate_pages_dir = LANDING / "affiliate-pages"
    new_targets = []

    if affiliate_pages_dir.exists():
        for page_dir in sorted(affiliate_pages_dir.iterdir()):
            if not page_dir.is_dir():
                continue
            index = page_dir / "index.html"
            if not index.exists():
                continue

            # Derive surge URL from dir name
            slug = page_dir.name
            url = f"https://{slug}.surge.sh"

            if url in existing_urls:
                continue

            # Extract niche from slug
            niche = slug.replace("-", " ").replace("best ", "").replace("supplement", "").replace("men over", "men 50+").strip()

            new_targets.append({
                "url": url,
                "slug": slug,
                "niche": niche,
                "type": "affiliate_landing",
                "added_at": TIMESTAMP,
                "content_needed": True,
                "distribution_channels": ["twitter", "reddit", "pinterest"],
            })
            existing_urls.add(url)

    if new_targets:
        all_targets = existing_targets + new_targets
        targets_path.write_text(json.dumps(all_targets, indent=2))
        results["New Affiliate Pages → Distribute Targets"] = {
            "status": "OK",
            "items_wired": len(new_targets),
            "pages": [t["slug"] for t in new_targets],
        }
        total_wired += len(new_targets)
    else:
        results["New Affiliate Pages → Distribute Targets"] = {
            "status": "OK",
            "items_wired": 0,
            "note": "deduped, all pages already in targets",
        }
    print(f"  [{'+'  if new_targets else '-'}] New Affiliate Pages → Distribute Targets: {len(new_targets)} (OK)")


def wire_digital_product_opps_to_product_queue():
    """Connection 4: DIGITAL_PRODUCTS category opportunities → Product creation queue."""
    global total_wired
    queue_path = safe_path(AUTO_STATE / "product_creation_queue.json")

    existing_queue = []
    existing_ids = set()
    if queue_path.exists():
        try:
            existing_queue = json.loads(queue_path.read_text(encoding="utf-8"))
            existing_ids = {q.get("opp_id") for q in existing_queue if isinstance(q, dict)}
        except Exception:
            pass

    new_items = []
    if OPP_DIR.exists():
        for opp_file in sorted(OPP_DIR.glob("OPP_*.md")):
            opp_id = opp_file.stem
            if opp_id in existing_ids:
                continue

            content = opp_file.read_text(encoding="utf-8", errors="ignore")

            # Only DIGITAL_PRODUCTS or SAAS/PRODUCT category
            cat_match = re.search(r"\*\*Category:\s*([^*]+)\*\*", content)
            category = cat_match.group(1).strip() if cat_match else ""

            if not any(c in category.upper() for c in ["DIGITAL_PRODUCTS", "PRODUCT", "TEMPLATE", "COURSE"]):
                continue

            score_match = re.search(r"\*\*Score:\s*([\d.]+)/10\*\*", content)
            score = float(score_match.group(1)) if score_match else 0.0

            if score < 7.0:
                continue

            # Extract speed
            speed_match = re.search(r"\*\*Speed:\s*([^*]+)\*\*", content)
            speed = speed_match.group(1).strip() if speed_match else "unknown"

            # Extract what section title
            title_match = re.search(r"^# OPP_\d+[a-z]?:\s*(.+)$", content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else opp_id

            new_items.append({
                "opp_id": opp_id,
                "title": title,
                "score": score,
                "category": category,
                "speed": speed,
                "status": "QUEUED",
                "added_at": TIMESTAMP,
            })
            existing_ids.add(opp_id)

    if new_items:
        all_items = existing_queue + new_items
        queue_path.write_text(json.dumps(all_items, indent=2))
        results["Digital Product Opps → Product Creation Queue"] = {
            "status": "OK",
            "items_wired": len(new_items),
            "examples": [i["title"][:60] for i in new_items[:3]],
        }
        total_wired += len(new_items)
    else:
        results["Digital Product Opps → Product Creation Queue"] = {
            "status": "OK",
            "items_wired": 0,
            "note": "deduped",
        }
    print(f"  [{'+'  if new_items else '-'}] Digital Product Opps → Product Queue: {len(new_items)} (OK)")


def wire_reddit_to_alpha_staging():
    """Connection 5: Today's Reddit scrapes → ALPHA_STAGING.csv."""
    global total_wired

    # Read existing alpha IDs to dedup
    existing_ids = set()
    if ALPHA_STAGING.exists():
        try:
            with open(ALPHA_STAGING, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_ids.add(row.get("alpha_id", ""))
        except Exception:
            pass

    new_entries = []
    if REDDIT_OUTPUT.exists():
        for reddit_file in sorted(REDDIT_OUTPUT.glob("reddit_*.json")):
            try:
                data = json.loads(reddit_file.read_text(encoding="utf-8"))
                posts = data if isinstance(data, list) else data.get("posts", [])
                for post in posts:
                    aid = post.get("alpha_id", "")
                    if not aid or aid in existing_ids:
                        continue
                    new_entries.append({
                        "alpha_id": aid,
                        "source": post.get("source", "reddit"),
                        "source_url": post.get("source_url", ""),
                        "title": post.get("title", post.get("content", ""))[:200],
                        "content": post.get("content", "")[:500],
                        "score": post.get("score", 0),
                        "status": "PENDING_REVIEW",
                        "added_at": TIMESTAMP,
                    })
                    existing_ids.add(aid)
            except Exception:
                continue

    if new_entries and ALPHA_STAGING.exists():
        # Append to CSV
        with open(ALPHA_STAGING, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["alpha_id", "source", "source_url", "title", "content",
                            "score", "status", "added_at"],
                extrasaction="ignore",
            )
            for entry in new_entries:
                writer.writerow(entry)
        results["Reddit Scrapes → Alpha Staging"] = {
            "status": "OK",
            "items_wired": len(new_entries),
        }
        total_wired += len(new_entries)
    else:
        results["Reddit Scrapes → Alpha Staging"] = {
            "status": "OK",
            "items_wired": 0,
            "note": "deduped or no alpha staging file",
        }
    print(f"  [{'+'  if new_entries else '-'}] Reddit Scrapes → Alpha Staging: {len(new_entries)} (OK)")


def run_cycle():
    print("=" * 65)
    print("  CROSS-POLLINATOR DAILY — NEW CONNECTIONS")
    print(f"  Time: {TIMESTAMP}")
    print("=" * 65)
    print()
    print("--- WIRING NEW CONNECTIONS ---")

    wire_new_opportunities_to_outreach_angles()
    wire_new_pdfs_to_posting_queue()
    wire_new_affiliate_pages_to_distribute_targets()
    wire_digital_product_opps_to_product_queue()
    wire_reddit_to_alpha_staging()

    print()
    print(f"Total items wired (new connections): {total_wired}")

    # Write to cross pollinator log
    log_path = safe_path(AUTOMATIONS / "agent" / "swarm" / "cross_pollinator_log.jsonl")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": TIMESTAMP,
            "agent": "cross_pollinator_daily",
            "total_wired": total_wired,
            "connections": results,
        }) + "\n")

    return total_wired, results


if __name__ == "__main__":
    run_cycle()
