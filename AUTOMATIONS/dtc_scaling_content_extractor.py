#!/usr/bin/env python3
"""
PRINTMAXX Automation System — DTC Supplement Scaling Content Extractor

TYPE: handoff
PURPOSE: Extract DTC supplement scaling playbook ($20K→$191K MRR in 7 months)
         into monetizable content assets (Twitter/X threads, LinkedIn posts,
         Instagram carousels) and cold outreach templates targeting
         supplement/wellness brands for AI-powered ad creative and ops
         automation services.

Phase 0 constraint: No ad spend available. Monetization via content authority
and direct outbound sales of AI creative + automation services.

Usage:
    python3 dtc_scaling_content_extractor.py --run
    python3 dtc_scaling_content_extractor.py --status
    python3 dtc_scaling_content_extractor.py --dry-run
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: attempt to import shared _common utilities; fall back gracefully
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(target: Path, base: Path = None) -> Path:
        """Validate that *target* resolves inside *base* (default: PROJECT)."""
        base = base or PROJECT
        try:
            resolved = Path(target).resolve()
            base_resolved = Path(base).resolve()
            resolved.relative_to(base_resolved)
            return resolved
        except ValueError:
            raise ValueError(
                f"Path traversal blocked: '{target}' is outside '{base}'"
            )

    def recall_skills_for_task(task_name: str) -> dict:
        return {"task": task_name, "skills": [], "source": "fallback"}

    def capture_skill_from_result(result: dict, skill_key: str) -> None:
        pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCRIPT_NAME = "dtc_scaling_content_extractor"
LOG_DIR = PROJECT / "AUTOMATIONS" / "logs"
LOG_FILE = LOG_DIR / f"{SCRIPT_NAME}.log"
OUTPUT_DIR = PROJECT / "AUTOMATIONS" / "outputs" / SCRIPT_NAME
STATUS_FILE = OUTPUT_DIR / "status.json"

# ---------------------------------------------------------------------------
# Logging — append mode, cron-safe (no ANSI, no interactive)
# ---------------------------------------------------------------------------
def _setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(SCRIPT_NAME)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(safe_path(LOG_FILE), mode="a", encoding="utf-8")
        fh.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                              datefmt="%Y-%m-%dT%H:%M:%S")
        )
        logger.addHandler(fh)
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(sh)
    return logger


log = _setup_logging()

# ---------------------------------------------------------------------------
# Playbook data — baked-in from the $20K→$191K MRR case study
# The brand is intentionally anonymised; the methodology is the asset.
# ---------------------------------------------------------------------------
PLAYBOOK_STEPS = [
    {
        "phase": 1,
        "month_range": "1-2",
        "title": "Offer Archaeology",
        "summary": (
            "Audited 6 months of Klaviyo data to find the 20 % of SKUs driving "
            "80 % of repeat purchases. Discontinued 3 underperformers, doubled "
            "down on hero bundle. AOV jumped from $47 to $71 inside 30 days."
        ),
        "levers": ["SKU rationalisation", "bundle architecture", "AOV lift"],
        "ai_angle": (
            "AI can scan your LTV cohorts overnight and surface the bundle "
            "configuration your data already knows — without a BI team."
        ),
        "thread_hook": (
            "Most supplement brands are accidentally shrinking their margins "
            "by carrying too many SKUs. Here's how we diagnosed the problem "
            "in 48 hours using nothing but Klaviyo export CSVs 🧵"
        ),
    },
    {
        "phase": 2,
        "month_range": "2-3",
        "title": "Creative Velocity Engine",
        "summary": (
            "Launched a UGC flywheel: 12 creators on $150 flat fee + commission. "
            "Fed raw footage into an AI editing pipeline producing 40+ ad variants "
            "per week. CTR improved 2.1x vs. studio creative within 3 weeks."
        ),
        "levers": ["UGC acquisition", "AI video editing", "creative iteration"],
        "ai_angle": (
            "AI trims, captions, and scores creative against your winning "
            "hooks automatically — your team ships 10x the variants with "
            "the same headcount."
        ),
        "thread_hook": (
            "We scaled a supplement brand's ad creative from 4 pieces/month "
            "to 40+ — without hiring a single editor. The AI pipeline we "
            "built cost less than one freelance post-production day 🧵"
        ),
    },
    {
        "phase": 3,
        "month_range": "3-4",
        "title": "Meta Funnel Architecture",
        "summary": (
            "Rebuilt campaign structure: Broad CBO at top, dynamic retargeting "
            "for add-to-cart abandoners (72-hr window), and a post-purchase "
            "upsell sequence via Messenger. ROAS moved from 1.8x to 3.4x."
        ),
        "levers": ["CBO structure", "audience architecture", "ROAS optimisation"],
        "ai_angle": (
            "AI monitors campaign performance 24/7 and auto-pauses "
            "underperforming ad sets before they burn budget — no manual "
            "babysitting required."
        ),
        "thread_hook": (
            "The supplement brand was running 23 ad sets with no coherent "
            "structure. We collapsed it into 3 campaigns and ROAS nearly "
            "doubled. Here's the exact framework 🧵"
        ),
    },
    {
        "phase": 4,
        "month_range": "4-5",
        "title": "Retention & Subscription Conversion",
        "summary": (
            "Introduced a subscribe-and-save tier at 15 % discount. Deployed "
            "a 7-email post-purchase sequence authored via LLM and A/B tested "
            "inside Klaviyo. Subscription penetration reached 34 % of new buyers."
        ),
        "levers": ["subscription model", "email automation", "LTV extension"],
        "ai_angle": (
            "AI writes, segments, and optimises your post-purchase sequences "
            "continuously — no copywriter on retainer, no agency mark-up."
        ),
        "thread_hook": (
            "34 % of first-time buyers converted to subscribers in 60 days. "
            "The only tool we used was an LLM and Klaviyo. Here's the "
            "7-email sequence that did it 🧵"
        ),
    },
    {
        "phase": 5,
        "month_range": "5-6",
        "title": "TikTok Shop Activation",
        "summary": (
            "Listed hero SKU on TikTok Shop, seeded 8 micro-creators "
            "(10K–80K followers) with affiliate links. Generated $31K GMV in "
            "first 45 days with zero paid media spend on the channel."
        ),
        "levers": ["TikTok Shop", "affiliate micro-creator", "organic GMV"],
        "ai_angle": (
            "AI identifies micro-creators with the highest engagement-to-follower "
            "ratio in your niche and drafts personalised outreach in seconds."
        ),
        "thread_hook": (
            "$31K GMV on TikTok Shop in 45 days — no ads, just 8 "
            "micro-creators and a system. Here's how we built the affiliate "
            "engine from scratch 🧵"
        ),
    },
    {
        "phase": 6,
        "month_range": "6-7",
        "title": "Ops Automation & Margin Defence",
        "summary": (
            "Automated inventory reorder alerts, 3PL exception handling, and "
            "customer support triage via AI chatbot. Support ticket volume "
            "dropped 41 %; gross margin improved 4 pp as team shed 1 FTE."
        ),
        "levers": ["ops automation", "support AI", "margin improvement"],
        "ai_angle": (
            "AI handles tier-1 support, flags inventory risk, and escalates "
            "edge cases — giving a lean team enterprise-grade operational "
            "leverage."
        ),
        "thread_hook": (
            "We cut a supplement brand's support tickets by 41 % and improved "
            "gross margin by 4 points — without firing anyone. Here's the "
            "AI ops stack we built for under $500/month 🧵"
        ),
    },
]

OUTREACH_PERSONAS = [
    {
        "persona_id": "founder_bootstrapped",
        "label": "Bootstrapped Supplement Founder",
        "pain_points": [
            "Burning cash on Meta with no clear feedback loop",
            "Creative production is slow and expensive",
            "No time to learn AI tools — need done-for-you",
        ],
        "decision_trigger": "proof of ROI in similar brand",
        "channel": "LinkedIn DM / Email",
    },
    {
        "persona_id": "brand_manager_funded",
        "label": "Brand Manager at VC-Backed Wellness Co.",
        "pain_points": [
            "Board wants efficiency gains before next round",
            "Creative team can't keep pace with testing demand",
            "Attribution is broken across Meta + TikTok",
        ],
        "decision_trigger": "case study numbers + enterprise credibility",
        "channel": "LinkedIn DM / cold email",
    },
    {
        "persona_id": "agency_owner",
        "label": "DTC Agency Owner (supplement vertical)",
        "pain_points": [
            "Margin compression from client demands",
            "Scaling delivery without headcount",
            "Differentiating against AI-native competitors",
        ],
        "decision_trigger": "white-label AI stack they can resell",
        "channel": "Twitter/X DM / Slack communities",
    },
]

OUTREACH_TEMPLATES = [
    {
        "template_id": "cold_email_founder",
        "persona_id": "founder_bootstrapped",
        "subject": "How {brand_name} could add ${mrr_lift}K MRR without more ad spend",
        "body": (
            "Hi {first_name},\n\n"
            "I came across {brand_name} while researching supplement brands "
            "doing interesting things with their creative — the {product_category} "
            "angle caught my eye.\n\n"
            "We recently helped a similar brand go from $20K to $191K MRR in "
            "7 months. The biggest lever wasn't more ad spend — it was "
            "restructuring their offer, automating creative production, and "
            "letting AI handle ops.\n\n"
            "I put together a short breakdown of what applied most directly to "
            "your situation. Worth a 15-minute call to walk through it?\n\n"
            "No pitch deck, no agency fluff — just the playbook and whether it "
            "fits.\n\n"
            "Best,\n{sender_name}\n\n"
            "P.S. If you'd rather just see the numbers first, reply and I'll "
            "send the one-pager."
        ),
        "cta": "15-minute call",
        "personalisation_fields": [
            "first_name", "brand_name", "product_category",
            "mrr_lift", "sender_name"
        ],
    },
    {
        "template_id": "cold_email_brand_manager",
        "persona_id": "brand_manager_funded",
        "subject": "AI creative ops for {brand_name} — 10x output, same headcount",
        "body": (
            "Hi {first_name},\n\n"
            "Quick question: how many ad variants is your creative team "
            "shipping per week right now?\n\n"
            "We built an AI-powered creative pipeline for a supplement brand "
            "that took them from 4 pieces/month to 40+ — without a single "
            "new hire. ROAS doubled in under 90 days.\n\n"
            "Given {brand_name}'s position in {product_category}, I think "
            "there's a direct application. Happy to share the technical "
            "breakdown if useful.\n\n"
            "15 minutes?\n\n"
            "{sender_name}"
        ),
        "cta": "15-minute call",
        "personalisation_fields": [
            "first_name", "brand_name", "product_category", "sender_name"
        ],
    },
    {
        "template_id": "twitter_dm_agency",
        "persona_id": "agency_owner",
        "subject": None,
        "body": (
            "Hey {first_name} — been following your content on scaling DTC "
            "supplement clients. We built an AI creative + ops stack that a "
            "few agencies are now white-labelling to increase margin without "
            "headcount. Thought it might be relevant. Happy to share the "
            "one-pager if you want a look?"
        ),
        "cta": "one-pager request",
        "personalisation_fields": ["first_name", "sender_name"],
    },
    {
        "template_id": "linkedin_follow_up",
        "persona_id": "founder_bootstrapped",
        "subject": "Following up — DTC supplement playbook",
        "body": (
            "Hi {first_name},\n\n"
            "Circling back on my earlier note. I know your inbox is a warzone "
            "so I'll keep it tight:\n\n"
            "• $20K → $191K MRR in 7 months\n"
            "• Core levers: offer restructure, AI creative velocity, "
            "retention automation\n"
            "• Applicable to any supplement brand doing $10K–$500K MRR\n\n"
            "If the timing is off, just say the word. If curious, a 15-minute "
            "call is all it takes to figure out if there's a fit.\n\n"
            "{sender_name}"
        ),
        "cta": "15-minute call",
        "personalisation_fields": ["first_name", "sender_name"],
    },
]

THREAD_STRUCTURE = {
    "platform": "Twitter/X",
    "format": "numbered thread",
    "optimal_length_tweets": 12,
    "hook_formula": "Bold claim + specificity + promise of method",
    "close_formula": "CTA to follow + offer of one-pager / call",
    "engagement_tactics": [
        "Ask a question at tweet 3-4 to boost reply count",
        "Drop a surprising counter-intuitive insight at tweet 7",
        "Screenshot / visual at tweet 5 if possible",
        "Restate the hook differently at the close",
    ],
}


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def build_threads() -> list[dict]:
    """Generate Twitter/X thread drafts for each playbook phase."""
    threads = []
    for step in PLAYBOOK_STEPS:
        tweets = []

        # Tweet 1 — hook
        tweets.append({
            "n": 1,
            "role": "hook",
            "text": step["thread_hook"],
        })

        # Tweet 2 — context / credibility
        tweets.append({
            "n": 2,
            "role": "context",
            "text": (
                f"Quick context: this is Phase {step['phase']} of a 7-month "
                f"sprint that took a supplement brand from $20K MRR to $191K MRR. "
                f"Month {step['month_range']}. No fluff — just what we did."
            ),
        })

        # Tweets 3-N — methodology broken into chunks
        summary_sentences = [s.strip() for s in step["summary"].split(".") if s.strip()]
        for i, sentence in enumerate(summary_sentences, start=3):
            tweets.append({
                "n": i,
                "role": "method",
                "text": sentence + ".",
            })

        # Mid-thread engagement question
        mid = len(tweets) + 1
        tweets.append({
            "n": mid,
            "role": "engagement",
            "text": (
                f"Quick question for supplement founders reading this: "
                f"which of these is your biggest bottleneck right now — "
                f"{', '.join(step['levers'][:-1])}, or {step['levers'][-1]}? "
                f"Reply below. I'll share the most relevant part of the playbook."
            ),
        })

        # AI angle tweet
        tweets.append({
            "n": mid + 1,
            "role": "ai_angle",
            "text": (
                f"The AI angle here:\n\n{step['ai_angle']}"
            ),
        })

        # Close / CTA
        tweets.append({
            "n": mid + 2,
            "role": "cta",
            "text": (
                "That's the phase breakdown. Full 7-phase playbook dropping "
                "this week.\n\nIf you want the one-pager now DM me 'PLAYBOOK' "
                "and I'll send it over.\n\nFollow for the rest of the thread series."
            ),
        })

        threads.append({
            "thread_id": f"phase_{step['phase']}_thread",
            "phase": step["phase"],
            "title": step["title"],
            "month_range": step["month_range"],
            "tweet_count": len(tweets),
            "tweets": tweets,
            "levers": step["levers"],
        })

    return threads


def build_linkedin_posts() -> list[dict]:
    """Generate LinkedIn post drafts (longer-form, professional tone)."""
    posts = []
    for step in PLAYBOOK_STEPS:
        body_lines = [
            f"Phase {step['phase']} of 7 — {step['title']} (Month {step['month_range']})",
            "",
            step["summary"],
            "",
            "The AI leverage point:",
            step["ai_angle"],
            "",
            f"Key levers: {' · '.join(step['levers'])}",
            "",
            "This is one chapter of a 7-phase playbook that took a supplement "
            "brand from $20K to $191K MRR in 7 months.",
            "",
            "Follow me for the full series. DM 'PLAYBOOK' if you want the "
            "one-pager now.",
        ]
        posts.append({
            "post_id": f"li_phase_{step['phase']}",
            "phase": step["phase"],
            "title": step["title"],
            "platform": "LinkedIn",
            "character_count": len("\n".join(body_lines)),
            "body": "\n".join(body_lines),
        })
    return posts


def build_carousel_outlines() -> list[dict]:
    """Generate Instagram / LinkedIn carousel slide outlines."""
    carousels = []
    for step in PLAYBOOK_STEPS:
        slides = [
            {"slide": 1, "type": "hook",
             "headline": step["thread_hook"].split("\n")[0],
             "sub": f"Phase {step['phase']} of 7"},
            {"slide": 2, "type": "problem",
             "headline": f"The problem at Month {step['month_range']}",
             "sub": "Before we touched anything..."},
            {"slide": 3, "type": "method",
             "headline": step["title"],
             "sub": step["summary"][:120] + "..."},
            {"slide": 4, "type": "result",
             "headline": "The result",
             "sub": step["summary"].split(".")[-2].strip() + "."},
            {"slide": 5, "type": "ai_angle",
             "headline": "How AI changes this",
             "sub": step["ai_angle"]},
            {"slide": 6, "type": "cta",
             "headline": "Want the full 7-phase playbook?",
             "sub": "DM 'PLAYBOOK' or follow for the next phase."},
        ]
        carousels.append({
            "carousel_id": f"carousel_phase_{step['phase']}",
            "phase": step["phase"],
            "title": step["title"],
            "slide_count": len(slides),
            "slides": slides,
        })
    return carousels


def build_content_calendar() -> list[dict]:
    """Return a 6-week rolling content calendar seeding all assets."""
    base_week = 1
    calendar = []
    for step in PLAYBOOK_STEPS:
        calendar.extend([
            {
                "week": base_week + step["phase"] - 1,
                "day": "Monday",
                "platform": "Twitter/X",
                "asset_id": f"phase_{step['phase']}_thread",
                "format": "thread",
                "phase": step["phase"],
            },
            {
                "week": base_week + step["phase"] - 1,
                "day": "Wednesday",
                "platform": "LinkedIn",
                "asset_id": f"li_phase_{step['phase']}",
                "format": "long-form post",
                "phase": step["phase"],
            },
            {
                "week": base_week + step["phase"] - 1,
                "day": "Friday",
                "platform": "Instagram / LinkedIn",
                "asset_id": f"carousel_phase_{step['phase']}",
                "format": "carousel",
                "phase": step["phase"],
            },
        ])
    return calendar


def build_outreach_pack() -> dict:
    """Assemble the full outreach pack (personas + templates)."""
    return {
        "personas": OUTREACH_PERSONAS,
        "templates": OUTREACH_TEMPLATES,
        "sequencing": {
            "cold_touch_1": "Day 0 — cold email or DM (personalised template)",
            "cold_touch_2": "Day 4 — follow-up with content asset link",
            "cold_touch_3": "Day 10 — value-add: share relevant thread/post",
            "cold_touch_4": "Day 17 — final ask or park",
        },
        "kpis": {
            "target_open_rate": "40%",
            "target_reply_rate": "8%",
            "target_call_book_rate": "3%",
            "weekly_outreach_volume": 50,
        },
    }


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------

def _ensure_output_dir(dry_run: bool) -> None:
    if not dry_run:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def write_json(data: object, filename: str, dry_run: bool) -> Path:
    target = OUTPUT_DIR / filename
    safe = safe_path(target)
    if dry_run:
        log.info("[DRY-RUN] Would write JSON → %s (%d bytes)",
                 safe, len(json.dumps(data)))
        return safe
    safe.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info("Wrote JSON → %s", safe)
    return safe


def write_csv(rows: list[dict], filename: str, dry_run: bool) -> Path:
    if not rows:
        log.warning("No rows to write for %s — skipping.", filename)
        return OUTPUT_DIR / filename
    target = OUTPUT_DIR / filename
    safe = safe_path(target)
    if dry_run:
        log.info("[DRY-RUN] Would write CSV → %s (%d rows)", safe, len(rows))
        return safe
    with safe.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            flat = {k: (json.dumps(v) if isinstance(v, (list, dict)) else v)
                    for k, v in row.items()}
            writer.writerow(flat)
    log.info("Wrote CSV → %s (%d rows)", safe, len(rows))
    return safe


def write_outreach_csv(pack: dict, dry_run: bool) -> Path:
    rows = []
    for tpl in pack["templates"]:
        persona = next(
            (p for p in pack["personas"] if p["persona_id"] == tpl["persona_id"]),
            {}
        )
        rows.append({
            "template_id": tpl["template_id"],
            "persona_label": persona.get("label", ""),
            "channel": persona.get("channel", ""),
            "subject": tpl.get("subject") or "",
            "body_preview": tpl["body"][:200].replace("\n", " "),
            "cta": tpl["cta"],
            "personalisation_fields": "|".join(tpl["personalisation_fields"]),
        })
    return write_csv(rows, "outreach_templates.csv", dry_run)


def write_thread_csv(threads: list[dict], dry_run: bool) -> Path:
    rows = []
    for thread in threads:
        for tweet in thread["tweets"]:
            rows.append({
                "thread_id": thread["thread_id"],
                "phase": thread["phase"],
                "title": thread["title"],
                "tweet_n": tweet["n"],
                "role": tweet["role"],
                "text": tweet["text"],
            })
    return write_csv(rows, "threads_all_tweets.csv", dry_run)


def write_calendar_csv(calendar: list[dict], dry_run: bool) -> Path:
    return write_csv(calendar, "content_calendar.csv", dry_run)


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def _load_status() -> dict:
    try:
        p = safe_path(STATUS_FILE)
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        log.warning("Could not load status file: %s", exc)
    return {}


def _save_status(status: dict, dry_run: bool) -> None:
    if dry_run:
        return
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        p = safe_path(STATUS_FILE)
        p.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as exc:
        log.error("Failed to save status: %s", exc)


def cmd_status() -> int:
    """Print last run status and list generated files."""
    status = _load_status()
    if not status:
        print("No previous run found. Execute with --run to generate assets.")
        return 0
    print(json.dumps(status, indent=2))
    return 0


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(dry_run: bool) -> int:
    """Execute the full content extraction pipeline."""
    label = "DRY-RUN" if dry_run else "RUN"
    log.info("=== PRINTMAXX DTC Content Extractor — %s ===", label)
    ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    try:
        skills = recall_skills_for_task("dtc_supplement_scaling_content_extraction")
        log.debug("Skills recalled: %s", skills)
    except Exception as exc:
        log.debug("recall_skills_for_task skipped: %s", exc)

    try:
        _ensure_output_dir(dry_run)
    except Exception as exc:
        log.error("Cannot create output directory: %s", exc)
        return 1

    generated_files = []
    errors = []

    steps = [
        ("threads", lambda: build_threads()),
        ("linkedin_posts", lambda: build_linkedin_posts()),
        ("carousels", lambda: build_carousel_outlines()),
        ("calendar", lambda: build_content_calendar()),
        ("outreach_pack", lambda: build_outreach_pack()),
    ]

    data_store = {}
    for key, builder in steps:
        try:
            log.info("Building: %s", key)
            data_store[key] = builder()
        except Exception as exc:
            log.error("Error building %s: %s", key, exc)
            errors.append({"step": key, "error": str(exc)})

    # JSON dumps
    json_exports = [
        ("threads.json", data_store.get("threads", [])),
        ("linkedin_posts.json", data_store.get("linkedin_posts", [])),
        ("carousel_outlines.json", data_store.get("carousels", [])),
        ("content_calendar.json", data_store.get("calendar", [])),
        ("outreach_pack.json", data_store.get("outreach_pack", {})),
        ("thread_structure_guide.json", THREAD_STRUCTURE),
        ("playbook_steps.json", PLAYBOOK_STEPS),
    ]
    for fname, payload in json_exports:
        try:
            p = write_json(payload, fname, dry_run)
            generated_files.append(str(p))
        except Exception as exc:
            log.error("Error writing %s: %s", fname, exc)
            errors.append({"step": fname, "error": str(exc)})

    # CSV exports
    csv_jobs = [
        ("threads", lambda: write_thread_csv(data_store.get("threads", []), dry_run)),
        ("calendar", lambda: write_calendar_csv(data_store.get("calendar", []), dry_run)),
        ("outreach", lambda: write_outreach_csv(data_store.get("outreach_pack", {}), dry_run)),
    ]
    for label_csv, writer in csv_jobs:
        try:
            p = writer()
            generated_files.append(str(p))
        except Exception as exc:
            log.error("Error in CSV export %s: %s", label_csv, exc)
            errors.append({"step": f"csv_{label_csv}", "error": str(exc)})

    status = {
        "last_run": ts,
        "mode": "dry_run" if dry_run else "live",
        "phases_extracted": len(PLAYBOOK_STEPS),
        "threads_generated": len(data_store.get("threads", [])),
        "linkedin_posts_generated": len(data_store.get("linkedin_posts", [])),
        "carousel_outlines_generated": len(data_store.get("carousels", [])),
        "outreach_templates": len(OUTREACH_TEMPLATES),
        "calendar_entries": len(data_store.get("calendar", [])),
        "files": generated_files,
        "errors": errors,
        "success": len(errors) == 0,
    }

    _save_status(status, dry_run)

    try:
        result_summary = {
            "task": "dtc_scaling_content_extraction",
            "status": status,
            "top_hooks": [s["thread_hook"][:80] for s in PLAYBOOK_STEPS],
        }
        capture_skill_from_result(result_summary, "dtc_content_extractor")
    except Exception as exc:
        log.debug("capture_skill_from_result skipped: %s", exc)

    if errors:
        log.warning("Pipeline finished with %d error(s). Review log.", len(errors))
        return 1

    log.info(
        "Pipeline complete. Threads: %d | LinkedIn posts: %d | "
        "Carousels: %d | Outreach templates: %d | Calendar entries: %d",
        len(data_store.get("threads", [])),
        len(data_store.get("linkedin_posts", [])),
        len(data_store.get("carousels", [])),
        len(OUTREACH_TEMPLATES),
        len(data_store.get("calendar", [])),
    )
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description=(
            "PRINTMAXX — DTC Supplement Scaling Content Extractor. "
            "Converts the $20K→$191K MRR playbook into threads, posts, "
            "carousels, and cold outreach templates."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute the full extraction pipeline and write output files.",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print the status of the last run.",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Simulate the pipeline without writing any files.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.status:
            sys.exit(cmd_status())
        elif args.dry_run:
            sys.exit(run_pipeline(dry_run=True))
        else:
            sys.exit(run_pipeline(dry_run=False))
    except KeyboardInterrupt:
        log.info("Interrupted by user.")
        sys.exit(130)
    except Exception as exc:
        log.critical("Unhandled exception: %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()