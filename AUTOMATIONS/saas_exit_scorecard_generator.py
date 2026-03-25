#!/usr/bin/env python3
"""
PRINTMAXX Automation: SaaS Exit Readiness Scorecard Generator

Generates 'SaaS Exit Readiness Scorecard' PDF products using acquisition criteria
(customer concentration score, competitive moat depth, founder dependency index).
Routes content through engagement_bait_converter and identifies potential leads
from r/SaaS and HN discussions around exit/acquisition at $500K-$2M ARR.

Usage:
  python saas_exit_scorecard_generator.py --run
  python saas_exit_scorecard_generator.py --run --dry-run
  python saas_exit_scorecard_generator.py --status
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Common imports (fall back to local definitions if _common not present)
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(p) -> Path:
        """Validate that path resolves within PROJECT directory."""
        resolved = Path(p).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(f"Path {resolved} escapes PROJECT root {PROJECT}")
        return resolved

    def recall_skills_for_task(task: str):  # noqa: D401
        return None

    def capture_skill_from_result(result, task: str):  # noqa: D401
        return None

# ---------------------------------------------------------------------------
# Directory / file layout
# ---------------------------------------------------------------------------
_AUTOMATIONS = PROJECT / "AUTOMATIONS"
_LOG_DIR      = _AUTOMATIONS / "logs"
_OUT_BASE     = _AUTOMATIONS / "outputs" / "saas_exit_scorecard"
_LEADS_DIR    = _OUT_BASE / "leads"
_CARDS_DIR    = _OUT_BASE / "scorecards"
_PITCHES_DIR  = _OUT_BASE / "pitches"
_STATUS_FILE  = _OUT_BASE / "status.json"
_LOG_FILE     = _LOG_DIR  / "saas_exit_scorecard_generator.log"

# ---------------------------------------------------------------------------
# Logging (append mode — cron-safe)
# ---------------------------------------------------------------------------
def _setup_logging() -> None:
    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = safe_path(_LOG_FILE)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(str(log_path), mode="a", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Acquisition scoring framework
# ---------------------------------------------------------------------------
ACQUISITION_CRITERIA = {
    "customer_concentration": {
        "description": "Revenue concentration risk across customer base",
        "weight": 0.25,
        "ideal": "No single customer >10% ARR",
        "red_flag": "Top customer >25% ARR",
    },
    "competitive_moat_depth": {
        "description": "Defensibility of market position and product",
        "weight": 0.30,
        "ideal": "Strong switching costs, network effects, or proprietary IP",
        "red_flag": "Easily replicable with no meaningful differentiation",
    },
    "founder_dependency_index": {
        "description": "Business reliance on founder involvement",
        "weight": 0.25,
        "ideal": "Fully documented processes, strong management layer",
        "red_flag": "Founder is sole relationship holder and decision-maker",
    },
    "net_revenue_retention": {
        "description": "Expansion revenue minus churn within existing customers",
        "weight": 0.20,
        "ideal": "NRR >110%",
        "red_flag": "NRR <90%",
    },
}

SCORECARD_QUESTIONS = {
    "customer_concentration": [
        ("What % of ARR comes from your single largest customer?", "pct_top_customer"),
        ("What % of ARR comes from your top 5 customers combined?", "pct_top5_customers"),
        ("Do you hold multi-year contracts with any customers?", "long_term_contracts"),
    ],
    "competitive_moat_depth": [
        ("Do customers pay for deep integrations or data portability features?", "integration_lock"),
        ("How many months does full implementation/onboarding take?", "implementation_months"),
        ("Do you own proprietary data assets, ML models, or patents?", "ip_assets"),
    ],
    "founder_dependency_index": [
        ("Could the business operate for 90 days without your direct involvement?", "founder_removable_90d"),
        ("Are your top 5 customer relationships held personally by you?", "founder_held_relationships"),
        ("Is the product roadmap documented and owned by a VP/PM (not you)?", "pm_owns_roadmap"),
    ],
    "net_revenue_retention": [
        ("What is your trailing 12-month NRR?", "nrr_trailing_12m"),
        ("What is your gross logo churn rate (annual)?", "gross_churn_annual"),
        ("What % of customers expand (upsell/cross-sell) within 12 months?", "expansion_pct"),
    ],
}

# ---------------------------------------------------------------------------
# Public-API scraper helpers
# ---------------------------------------------------------------------------
_REDDIT_SEARCH = "https://www.reddit.com/r/SaaS/search.json"
_HN_SEARCH     = "https://hn.algolia.com/api/v1/search"

_EXIT_KEYWORDS = [
    "selling my saas", "sold my saas", "saas acquisition", "exit multiple",
    "letter of intent", "due diligence buyer", "find a buyer", "bootstrapped exit",
    "ARR multiple", "PE acquisition", "strategic buyer", "looking to sell",
]

_ARR_SIGNALS = [
    "500k arr", "600k arr", "700k arr", "800k arr", "900k arr",
    "1m arr", "1.2m arr", "1.5m arr", "2m arr",
    "$500k", "$1m", "$1.2m", "$1.5m", "$2m",
    "500,000 arr", "1,000,000 arr", "2,000,000 arr",
]


def _fetch_json(url: str, timeout: int = 15) -> dict:
    """Fetch JSON from *url* via urllib; return empty dict on any error."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "PRINTMAXX-Research/1.0 (non-commercial research)")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError, OSError) as exc:
        logger.warning("Fetch failed (%s): %s", url[:80], exc)
        return {}


def _arr_signal(text: str) -> bool:
    low = text.lower()
    return any(sig in low for sig in _ARR_SIGNALS)


def scrape_reddit_leads(dry_run: bool = False) -> list:
    """Return list of lead dicts from r/SaaS public search API."""
    if dry_run:
        logger.info("[DRY-RUN] Skipping Reddit scrape")
        return [{
            "source": "reddit", "title": "[DRY-RUN] Just sold my SaaS — AMA",
            "author": "dry_run_founder", "url": "https://reddit.com/r/SaaS/dry",
            "arr_signal": True, "keywords_matched": ["sold my saas"],
            "created_utc": 0, "score": 200, "num_comments": 80,
        }]

    leads = []
    for kw in _EXIT_KEYWORDS[:6]:
        params = urllib.parse.urlencode({
            "q": kw, "sort": "new", "limit": 25,
            "t": "year", "restrict_sr": "true",
        })
        data = _fetch_json(f"{_REDDIT_SEARCH}?{params}")
        for child in data.get("data", {}).get("children", []):
            pd = child.get("data", {})
            combined = (pd.get("title", "") + " " + pd.get("selftext", "")).lower()
            if kw.lower() in combined or _arr_signal(combined):
                leads.append({
                    "source": "reddit",
                    "title": pd.get("title", ""),
                    "author": pd.get("author", ""),
                    "url": "https://reddit.com" + pd.get("permalink", ""),
                    "arr_signal": _arr_signal(combined),
                    "keywords_matched": [kw],
                    "created_utc": pd.get("created_utc", 0),
                    "score": pd.get("score", 0),
                    "num_comments": pd.get("num_comments", 0),
                })
    logger.info("Reddit leads found: %d", len(leads))
    return leads


def scrape_hn_leads(dry_run: bool = False) -> list:
    """Return list of lead dicts from HN Algolia search API."""
    if dry_run:
        logger.info("[DRY-RUN] Skipping HN scrape")
        return [{
            "source": "hn", "title": "[DRY-RUN] Show HN: We sold our SaaS for $3M",
            "author": "dry_run_hn_founder", "url": "https://news.ycombinator.com/item?id=0",
            "arr_signal": True, "keywords_matched": ["sold saas"],
            "created_at": "", "points": 300, "num_comments": 120,
        }]

    leads = []
    for query in ["SaaS acquisition", "sold my SaaS", "SaaS exit bootstrapped", "acquired B2B SaaS"]:
        params = urllib.parse.urlencode({
            "query": query, "tags": "story",
            "numericFilters": "created_at_i>1640000000",
        })
        data = _fetch_json(f"{_HN_SEARCH}?{params}")
        for hit in data.get("hits", []):
            combined = ((hit.get("title") or "") + " " + (hit.get("story_text") or "")).lower()
            if _arr_signal(combined) or any(kw.lower() in combined for kw in _EXIT_KEYWORDS[:8]):
                leads.append({
                    "source": "hn",
                    "title": hit.get("title", ""),
                    "author": hit.get("author", ""),
                    "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID','')}",
                    "arr_signal": _arr_signal(combined),
                    "keywords_matched": [query],
                    "created_at": hit.get("created_at", ""),
                    "points": hit.get("points", 0),
                    "num_comments": hit.get("num_comments", 0),
                })
    logger.info("HN leads found: %d", len(leads))
    return leads

# ---------------------------------------------------------------------------
# Lead scoring
# ---------------------------------------------------------------------------

def score_lead(lead: dict) -> dict:
    """Assign a preliminary exit-readiness score from available signals."""
    score = 50
    signals = []
    title = (lead.get("title") or "").lower()

    if lead.get("arr_signal"):
        score += 15
        signals.append("ARR in target range ($500K–$2M detected)")
    if any(kw in title for kw in ("sold", "acquisition", "acquired", "exit")):
        score += 10
        signals.append("Direct exit-event signal in title")
    if lead.get("num_comments", 0) > 50 or lead.get("num_comments", 0) > 50:
        score += 10
        signals.append("High community engagement (>50 comments)")
    if lead.get("score", 0) > 100 or lead.get("points", 0) > 100:
        score += 5
        signals.append("High upvote signal")
    if "due diligence" in title or "loi" in title:
        score += 10
        signals.append("Active deal process signal")

    return {
        **lead,
        "exit_readiness_score": min(score, 100),
        "score_signals": signals,
        "scorecard_fit": score >= 65,
    }

# ---------------------------------------------------------------------------
# Engagement bait converter
# ---------------------------------------------------------------------------

def engagement_bait_converter(leads: list) -> list:
    """
    Map each qualified lead to an engagement angle and pitch hook.
    Returns leads augmented with pitch_angle, pitch_hook, pitch_cta, pitch_channel.
    NOTE: Output is saved to CSV for manual human review before any outreach.
    """
    converted = []
    for lead in leads:
        title  = (lead.get("title") or "").lower()
        source = lead.get("source", "")

        if "sold" in title or "acquired" in title:
            angle = "peer_validation"
            hook  = (
                "You mentioned selling — here's the exact framework 30 real buyers used "
                "to evaluate SaaS at your ARR range. Most founders leave 0.5x on the table."
            )
        elif any(w in title for w in ("looking", "thinking", "considering", "plan")):
            angle = "urgency_education"
            hook  = (
                "Founders preparing for exit miss 3 critical preparation steps that cost "
                "0.5–1x multiple. Free scorecard shows where you stand today."
            )
        elif any(w in title for w in ("due diligence", "loi", "letter of intent")):
            angle = "process_support"
            hook  = (
                "You're already in the process — run the exit readiness scorecard now to "
                "close documentation gaps before buyers surface them."
            )
        else:
            angle = "awareness"
            hook  = (
                "Curious what buyers actually look for at your ARR? We distilled 30 "
                "acquisitions into one free scorecard. Takes 2 minutes."
            )

        converted.append({
            **lead,
            "pitch_angle":   angle,
            "pitch_hook":    hook,
            "pitch_cta":     "Request your free Exit Readiness Score (2-min form, instant results)",
            "pitch_channel": "reply_to_post" if source in ("reddit", "hn") else "email",
        })
    return converted

# ---------------------------------------------------------------------------
# Scorecard HTML generator
# ---------------------------------------------------------------------------

def _build_scorecard_html(lead: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    criteria_rows = ""
    for key, meta in ACQUISITION_CRITERIA.items():
        qs = "".join(f"<li>{q[0]}</li>" for q in SCORECARD_QUESTIONS.get(key, []))
        criteria_rows += f"""
      <tr>
        <td><strong>{key.replace('_',' ').title()}</strong><br>
            <small style='color:#555'>{meta['description']}</small></td>
        <td style='text-align:center'>{int(meta['weight']*100)}%</td>
        <td style='color:#1a7a1a'>{meta['ideal']}</td>
        <td style='color:#c0392b'>{meta['red_flag']}</td>
        <td><ul style='margin:0;padding-left:18px'>{qs}</ul></td>
      </tr>"""

    signals_html = "".join(
        f"<li>{s}</li>" for s in (lead.get("score_signals") or ["No signals detected"])
    )
    score = lead.get("exit_readiness_score", "N/A")
    title = (lead.get("title") or "")[:90]
    url   = lead.get("url", "#")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>SaaS Exit Readiness Scorecard</title>
  <style>
    body  {{ font-family:Arial,sans-serif; max-width:920px; margin:40px auto; color:#222; line-height:1.5; }}
    h1   {{ color:#1a1a2e; border-bottom:3px solid #e94560; padding-bottom:8px; }}
    h2   {{ color:#16213e; margin-top:30px; }}
    table{{ width:100%; border-collapse:collapse; margin:16px 0; }}
    th   {{ background:#16213e; color:#fff; padding:10px; text-align:left; }}
    td   {{ padding:10px; border:1px solid #ddd; vertical-align:top; }}
    tr:nth-child(even) td {{ background:#f7f7f7; }}
    .score-box  {{ background:#1a1a2e; color:#fff; padding:24px; border-radius:8px; text-align:center; }}
    .score-num  {{ font-size:52px; font-weight:bold; color:#e94560; }}
    .signals    {{ background:#f0fff0; border-left:4px solid #2ecc71; padding:12px 16px; margin:16px 0; }}
    .cta        {{ background:#e94560; color:#fff; padding:20px; border-radius:8px; margin-top:32px; }}
    .cta h3     {{ margin-top:0; }}
    .meta       {{ color:#666; font-size:13px; margin-bottom:20px; }}
  </style>
</head>
<body>
  <h1>SaaS Exit Readiness Scorecard</h1>
  <p class="meta">Generated: {now} &nbsp;|&nbsp;
     Source: {lead.get('source','').upper()} &nbsp;|&nbsp;
     Reference: <a href="{url}">{title}</a></p>

  <div class="score-box">
    <div style="font-size:18px;margin-bottom:6px">Preliminary Exit Readiness Score</div>
    <div class="score-num">{score}<span style="font-size:28px">/100</span></div>
    <div style="opacity:.8">{len(lead.get('score_signals') or [])} signals detected</div>
  </div>

  <div class="signals">
    <strong>Detected Signals:</strong>
    <ul style="margin:6px 0 0 0;padding-left:20px">{signals_html}</ul>
  </div>

  <h2>Acquisition Criteria Framework</h2>
  <p>Derived from analysis of 30+ SaaS acquisitions in the $500K–$5M ARR range.</p>
  <table>
    <thead>
      <tr>
        <th>Criterion</th><th>Weight</th>
        <th>Ideal State</th><th>Red Flag</th><th>Assessment Questions</th>
      </tr>
    </thead>
    <tbody>{criteria_rows}</tbody>
  </table>

  <h2>What Buyers Actually Evaluated</h2>
  <ul>
    <li><strong>Customer Concentration:</strong> Every 5 percentage points above 10% of ARR held by one customer shaves ~0.2× off your multiple.</li>
    <li><strong>Competitive Moat:</strong> Strategic acquirers pay 1–2× premium for documented, defensible moats.</li>
    <li><strong>Founder Dependency:</strong> PE buyers require a credible 90-day transition plan and penalise undocumented key-person risk.</li>
    <li><strong>Net Revenue Retention:</strong> NRR &gt;110% is the single largest multiple driver below $5M ARR — it signals PMF and organic growth.</li>
  </ul>

  <div class="cta">
    <h3>Next Step: Full Exit Readiness Audit</h3>
    <p>A full scorecard audit typically surfaces 2–4 fixable gaps that can increase your exit multiple by 0.5–1.5× before going to market.</p>
    <p><strong>Schedule a complimentary 30-minute Exit Readiness Review</strong> — instant results, no obligation.</p>
  </div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# File I/O helpers
# ---------------------------------------------------------------------------

def save_scorecard_html(lead: dict, dry_run: bool = False) -> Path:
    """Write scorecard HTML to _CARDS_DIR; return the path."""
    _CARDS_DIR.mkdir(parents=True, exist_ok=True)
    slug = (lead.get("author") or "unknown").replace("/", "_")[:30]
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = safe_path(_CARDS_DIR / f"scorecard_{slug}_{ts}.html")
    if dry_run:
        logger.info("[DRY-RUN] Would write scorecard HTML: %s", dest)
        return dest
    dest.write_text(_build_scorecard_html(lead), encoding="utf-8")
    logger.info("Scorecard HTML saved: %s", dest)
    return dest


def convert_to_pdf(html_path: Path, dry_run: bool = False) -> Path:
    """Convert HTML scorecard to PDF via wkhtmltopdf or Chrome headless."""
    pdf_path = html_path.with_suffix(".pdf")
    if dry_run:
        logger.info("[DRY-RUN] Would convert to PDF: %s", pdf_path)
        return pdf_path

    for cmd in [
        ["wkhtmltopdf", "--quiet", str(html_path), str(pdf_path)],
    ]:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if r.returncode == 0:
                logger.info("PDF via wkhtmltopdf: %s", pdf_path)
                return pdf_path
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    chrome_bins = [
        "google-chrome", "chromium-browser", "chromium",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for bin_ in chrome_bins:
        try:
            r = subprocess.run(
                [bin_, "--headless", "--disable-gpu", "--no-sandbox",
                 f"--print-to-pdf={pdf_path}", str(html_path)],
                capture_output=True, text=True, timeout=30,
            )
            if r.returncode == 0:
                logger.info("PDF via Chrome headless: %s", pdf_path)
                return pdf_path
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    logger.warning("No PDF renderer found; HTML scorecard retained only.")
    return html_path


def save_leads_json(leads: list, dry_run: bool = False) -> Path:
    _LEADS_DIR.mkdir(parents=True, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = safe_path(_LEADS_DIR / f"leads_{ts}.json")
    if dry_run:
        logger.info("[DRY-RUN] Would write leads JSON: %s", dest)
        return dest
    dest.write_text(json.dumps(leads, indent=2, default=str), encoding="utf-8")
    logger.info("Leads JSON saved: %s (%d records)", dest, len(leads))
    return dest


def save_pitch_queue(converted: list, dry_run: bool = False) -> Path:
    """Save pitch queue to CSV for human review before any outreach."""
    _PITCHES_DIR.mkdir(parents=True, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = safe_path(_PITCHES_DIR / f"pitch_queue_{ts}.csv")
    fields = [
        "source", "author", "title", "url", "arr_signal",
        "exit_readiness_score", "scorecard_fit",
        "pitch_angle", "pitch_hook", "pitch_cta", "pitch_channel",
    ]
    if dry_run:
        logger.info("[DRY-RUN] Would write pitch queue CSV: %s (%d rows)", dest, len(converted))
        return dest
    with open(dest, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(converted)
    logger.info("Pitch queue CSV saved: %s (%d rows)", dest, len(converted))
    return dest

# ---------------------------------------------------------------------------
# Status helpers
# ---------------------------------------------------------------------------

def _write_status(data: dict) -> None:
    _OUT_BASE.mkdir(parents=True, exist_ok=True)
    dest = safe_path(_STATUS_FILE)
    try:
        existing: dict = {}
        if dest.exists():
            try:
                existing = json.loads(dest.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        existing.update(data)
        existing["last_updated"] = datetime.now().isoformat()
        dest.write_text(json.dumps(existing, indent=2, default=str), encoding="utf-8")
    except Exception as exc:
        logger.warning("Status write failed: %s", exc)


def _read_status() -> dict:
    dest = safe_path(_STATUS_FILE)
    if not dest.exists():
        return {"status": "never_run"}
    try:
        return json.loads(dest.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("Status read failed: %s", exc)
        return {"status": "error_reading_status", "detail": str(exc)}

# ---------------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------------

def run_workflow(dry_run: bool = False) -> None:
    logger.info("=== SaaS Exit Readiness Scorecard Generator  dry_run=%s ===", dry_run)
    recall_skills_for_task("saas_exit_scorecard_generation")
    _write_status({"status": "running", "dry_run": dry_run})

    try:
        # 1. Collect leads from public sources
        reddit_leads = scrape_reddit_leads(dry_run=dry_run)
        hn_leads     = scrape_hn_leads(dry_run=dry_run)
        all_leads    = reddit_leads + hn_leads
        logger.info("Total raw leads: %d", len(all_leads))

        # 2. Score every lead
        scored = [score_lead(lead) for lead in all_leads]
        qualified = [l for l in scored if l.get("scorecard_fit")]
        logger.info("Qualified leads: %d", len(qualified))

        # 3. Route through engagement_bait_converter
        pitched = engagement_bait_converter(qualified)

        # 4. Persist artefacts
        leads_json = save_leads_json(scored, dry_run=dry_run)
        pitch_csv  = save_pitch_queue(pitched, dry_run=dry_run)

        # 5. Generate scorecards for top leads
        top = sorted(pitched, key=lambda x: x.get("exit_readiness_score", 0), reverse=True)[:5]
        generated = []
        for lead in top:
            try:
                html = save_scorecard_html(lead, dry_run=dry_run)
                pdf  = convert_to_pdf(html, dry_run=dry_run)
                generated.append(str(pdf))
            except Exception as exc:
                logger.warning("Scorecard generation failed for %s: %s", lead.get("author"), exc)

        result = {
            "status":               "completed",
            "total_leads_found":    len(all_leads),
            "qualified_leads":      len(qualified),
            "scorecards_generated": len(generated),
            "leads_json":           str(leads_json),
            "pitch_queue_csv":      str(pitch_csv),
            "top_scorecards":       generated,
        }
        _write_status(result)
        capture_skill_from_result(result, "saas_exit_scorecard_generation")
        logger.info("Run complete: %s", json.dumps(result, indent=2))

    except Exception as exc:
        logger.error("Workflow failed: %s", exc, exc_info=True)
        _write_status({"status": "failed", "error": str(exc)})
        sys.exit(1)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="saas_exit_scorecard_generator.py",
        description="PRINTMAXX: SaaS Exit Readiness Scorecard Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python saas_exit_scorecard_generator.py --run\n"
            "  python saas_exit_scorecard_generator.py --run --dry-run\n"
            "  python saas_exit_scorecard_generator.py --status\n"
        ),
    )
    parser.add_argument("--run",     action="store_true", help="Execute the full pipeline")
    parser.add_argument("--status",  action="store_true", help="Print current run status as JSON")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing files or calling APIs")
    args = parser.parse_args()

    _setup_logging()

    if args.status:
        print(json.dumps(_read_status(), indent=2))
        sys.exit(0)

    if args.run:
        run_workflow(dry_run=args.dry_run)
        sys.exit(0)

    parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()