#!/usr/bin/env python3
"""
PRINTMAXX Automation: VC/AI Funding Lead Scraper

Scrapes TechCrunch, Crunchbase News, and PitchBook RSS feeds for newly funded
AI startups. Extracts company name, funding stage/amount, founder emails, company
size, and tech stack for the PRINTMAXX cold outbound pipeline.

AI startups with fresh capital have budget, urgency, and a mandate to build fast —
prime targets for automation, dev, and content services.

Secondary purpose: converts funding news into short engagement content pieces
about AI/VC trends for PRINTMAXX social and marketing channels.

Usage:
    python vc_ai_funding_lead_scraper.py --run
    python vc_ai_funding_lead_scraper.py --status
    python vc_ai_funding_lead_scraper.py --dry-run
"""

import argparse
import csv
import json
import logging
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: import shared utilities or define fallbacks
# ---------------------------------------------------------------------------
try:
    from _common import (  # type: ignore[import]
        PROJECT,
        capture_skill_from_result,
        recall_skills_for_task,
        safe_path,
    )
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path):
        """Return resolved Path; raise ValueError if outside PROJECT."""
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(PROJECT)
        except ValueError as exc:
            raise ValueError(
                f"Unsafe path '{resolved}' is outside PROJECT root '{PROJECT}'"
            ) from exc
        return resolved

    def recall_skills_for_task(task_name):  # noqa: D401
        return {}

    def capture_skill_from_result(task_name, result):
        return result


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_FILE        = AUTOMATIONS_DIR / "logs" / "vc_ai_funding_lead_scraper.log"
DATA_DIR        = AUTOMATIONS_DIR / "data" / "vc_ai_leads"
LEADS_CSV       = DATA_DIR / "leads.csv"
CONTENT_JSON    = DATA_DIR / "ai_vc_content.json"
STATUS_FILE     = DATA_DIR / "last_run_status.json"

# ---------------------------------------------------------------------------
# Logging — always append, stdout only during --dry-run
# ---------------------------------------------------------------------------

def setup_logging(dry_run=False):
    log_path = safe_path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("vc_ai_funding_lead_scraper")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    fh = logging.FileHandler(str(log_path), mode="a", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    if dry_run:
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmt)
        logger.addHandler(sh)

    return logger


# ---------------------------------------------------------------------------
# Network helpers — urllib only, no third-party deps
# ---------------------------------------------------------------------------

_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

_DEFAULT_HEADERS = {
    "User-Agent": _USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def fetch_url(url, timeout=15, retries=2):
    """Fetch URL body as a string; returns None on any failure."""
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=_DEFAULT_HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                charset = "utf-8"
                ct = resp.headers.get("Content-Type", "")
                m = re.search(r"charset=([\w-]+)", ct)
                if m:
                    charset = m.group(1)
                return resp.read().decode(charset, errors="replace")
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 503) and attempt < retries:
                time.sleep(3 * (attempt + 1))
                continue
            return None
        except (urllib.error.URLError, OSError):
            if attempt < retries:
                time.sleep(2)
                continue
            return None
    return None


def check_network():
    """Return True if we can reach the internet (used for pre-flight check)."""
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "4", "-o", "/dev/null",
             "-w", "%{http_code}", "https://techcrunch.com/robots.txt"],
            capture_output=True, text=True, timeout=8,
        )
        return result.returncode == 0 and result.stdout.strip().startswith("2")
    except Exception:
        return False


# ---------------------------------------------------------------------------
# RSS / XML helpers
# ---------------------------------------------------------------------------

def fetch_rss(url):
    """Parse an RSS/Atom feed; return list of {title, link, pubdate, summary}."""
    body = fetch_url(url)
    if not body:
        return []

    items = []
    raw_items = re.split(r"<(?:item|entry)[\s>]", body, flags=re.IGNORECASE)[1:]
    for raw in raw_items:
        title   = _xml_text(raw, "title")
        link    = _xml_text(raw, "link") or _xml_attr(raw, "link", "href")
        pubdate = _xml_text(raw, r"(?:pubDate|published|updated)")
        summary = _xml_text(raw, r"(?:description|summary|content:encoded)")
        if title and link:
            items.append({
                "title":   _strip_html(title).strip(),
                "link":    link.strip(),
                "pubdate": pubdate.strip() if pubdate else "",
                "summary": _strip_html(summary or "").strip()[:800],
            })
    return items


def _xml_text(blob, tag):
    m = re.search(
        rf"<{tag}[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</{tag}>",
        blob,
        re.IGNORECASE | re.DOTALL,
    )
    return m.group(1) if m else ""


def _xml_attr(blob, tag, attr):
    m = re.search(
        rf'<{tag}[^>]+{attr}=["\']([^"\']+)["\']',
        blob,
        re.IGNORECASE,
    )
    return m.group(1) if m else ""


def _strip_html(text):
    text = re.sub(r"<[^>]+>", " ", text)
    for entity, char in (
        ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
        ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " "),
    ):
        text = text.replace(entity, char)
    return re.sub(r"\s+", " ", text)


# ---------------------------------------------------------------------------
# Signal filters
# ---------------------------------------------------------------------------

_FUNDING_RE = re.compile(
    r"\b(?:raises?|raised|funding|funded|secures?|secured|"
    r"seed|series [a-e]|pre-seed|pre-series|round|"
    r"venture|backed|investment|capital|"
    r"\$[\d]+(?:\.\d+)?(?:\s*million|\s*billion)?)\b",
    re.IGNORECASE,
)

_AI_RE = re.compile(
    r"\b(?:ai\b|artificial intelligence|machine learning|ml\b|"
    r"llm|large language model|generative|genai|gen-ai|"
    r"deep learning|neural|nlp|computer vision|autonomous|"
    r"automation|chatbot|copilot|foundation model)\b",
    re.IGNORECASE,
)

_STAGE_RE = re.compile(
    r"\b(pre-seed|seed|series [a-e]|pre-series [a-e]|growth|late[- ]stage)\b",
    re.IGNORECASE,
)

_AMOUNT_RE = re.compile(
    r"\$\s*([\d,]+(?:\.\d+)?)\s*(million|billion|[MBK])\b",
    re.IGNORECASE,
)

_EMAIL_RE = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)

_TECH_KEYWORDS = [
    "python", "javascript", "typescript", "react", "next.js", "node",
    "aws", "gcp", "azure", "kubernetes", "docker", "terraform",
    "pytorch", "tensorflow", "openai", "langchain", "hugging face",
    "postgres", "mongodb", "redis", "kafka", "spark",
    "rust", "go", "java", "c++", "scala",
]

_EMAIL_SKIP = (
    "example.com", "sentry.io", "wix.com", "noreply", "no-reply",
    "donotreply", "webmaster", "postmaster", "mailer", "bounce",
    ".png@", ".jpg@", ".gif@",
)


def is_ai_funding_article(title, summary):
    text = f"{title} {summary}"
    return bool(_FUNDING_RE.search(text) and _AI_RE.search(text))


def extract_funding_stage(text):
    m = _STAGE_RE.search(text)
    return m.group(1).title() if m else "Unknown"


def extract_funding_amount(text):
    m = _AMOUNT_RE.search(text)
    if not m:
        return ""
    num, unit = m.group(1), m.group(2).lower()
    if unit in ("m", "million"):   return f"${num}M"
    if unit in ("b", "billion"):   return f"${num}B"
    if unit == "k":                return f"${num}K"
    return f"${num}{unit.upper()}"


def extract_tech_stack(text):
    tl = text.lower()
    return [kw for kw in _TECH_KEYWORDS if kw in tl]


def extract_company_size(text):
    m = re.search(
        r"(\d+)\s*(?:employees?|people|team members?|staff)\b",
        text, re.IGNORECASE,
    )
    if m:
        n = int(m.group(1))
        if n < 10:  return "1-10"
        if n < 50:  return "11-50"
        if n < 200: return "51-200"
        if n < 500: return "201-500"
        return "500+"
    return "Unknown"


def extract_company_name(title):
    """Heuristic: company name typically precedes the funding verb."""
    m = re.match(
        r"^([A-Z][^,|]{2,45?}?)\s+(?:Raises?|Secures?|Closes?|Lands?|Gets?|Nets?|Bags?)\b",
        title,
    )
    if m:
        return m.group(1).strip()
    parts = title.split()
    return " ".join(parts[:3]) if len(parts) >= 3 else title[:40]


# ---------------------------------------------------------------------------
# Website / email discovery
# ---------------------------------------------------------------------------

def find_company_website(company_name):
    """Try a DuckDuckGo HTML search to locate the company's domain."""
    query = urllib.parse.quote_plus(f"{company_name} AI startup official website")
    url = f"https://html.duckduckgo.com/html/?q={query}"
    body = fetch_url(url, timeout=10)
    if not body:
        return None
    links = re.findall(r'<a[^>]+class="[^"]*result__url[^"]*"[^>]*>([^<]+)<', body)
    for link in links:
        link = link.strip()
        if link and "duckduckgo" not in link:
            return link if link.startswith("http") else f"https://{link}"
    return None


def scrape_contact_emails(website_url):
    """Visit homepage and /contact to harvest founder/team emails."""
    if not website_url:
        return []
    emails = set()
    pages = [
        website_url,
        website_url.rstrip("/") + "/contact",
        website_url.rstrip("/") + "/about",
    ]
    for page in pages[:2]:
        body = fetch_url(page, timeout=8)
        if body:
            for em in _EMAIL_RE.findall(body):
                if not any(skip in em.lower() for skip in _EMAIL_SKIP):
                    emails.add(em)
        time.sleep(0.5)
    return sorted(emails)[:5]


# ---------------------------------------------------------------------------
# Source scrapers
# ---------------------------------------------------------------------------

_TC_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://techcrunch.com/category/startups/feed/",
    "https://techcrunch.com/tag/funding/feed/",
]

_CB_FEEDS = [
    "https://news.crunchbase.com/feed/",
    "https://news.crunchbase.com/category/news/feed/",
    "https://news.crunchbase.com/category/venture/feed/",
]

_PB_FEEDS = [
    "https://pitchbook.com/news/rss.xml",
]


def _scrape_feeds(feeds, source_name, logger):
    results = []
    for feed_url in feeds:
        try:
            items = fetch_rss(feed_url)
            logger.debug(f"  {feed_url}: {len(items)} items")
            for item in items:
                if is_ai_funding_article(item["title"], item["summary"]):
                    results.append({**item, "source": source_name})
        except Exception as exc:
            logger.warning(f"Feed error ({feed_url}): {exc}")
    logger.info(f"{source_name}: {len(results)} relevant articles")
    return results


def scrape_techcrunch(logger):
    logger.info("Scraping TechCrunch…")
    return _scrape_feeds(_TC_FEEDS, "TechCrunch", logger)


def scrape_crunchbase(logger):
    logger.info("Scraping Crunchbase News…")
    return _scrape_feeds(_CB_FEEDS, "Crunchbase", logger)


def scrape_pitchbook(logger):
    logger.info("Scraping PitchBook…")
    return _scrape_feeds(_PB_FEEDS, "PitchBook", logger)


# ---------------------------------------------------------------------------
# Lead enrichment
# ---------------------------------------------------------------------------

def build_lead(article, dry_run, logger):
    """Enrich a raw article into a structured lead record."""
    title     = article["title"]
    summary   = article["summary"]
    full_text = f"{title} {summary}"

    company = extract_company_name(title)
    stage   = extract_funding_stage(full_text)
    amount  = extract_funding_amount(full_text)
    size    = extract_company_size(full_text)
    stack   = extract_tech_stack(full_text)

    website = ""
    emails  = []
    if not dry_run:
        try:
            website = find_company_website(company) or ""
            if website:
                emails = scrape_contact_emails(website)
                logger.debug(f"  {company}: {website} → {emails}")
        except Exception as exc:
            logger.warning(f"Enrichment error for '{company}': {exc}")
        time.sleep(1.0)

    return {
        "scraped_at":      datetime.now(timezone.utc).isoformat(),
        "source":          article.get("source", ""),
        "company_name":    company,
        "funding_stage":   stage,
        "funding_amount":  amount,
        "company_size":    size,
        "tech_stack":      "|".join(stack),
        "website":         website,
        "founder_emails":  "|".join(emails),
        "article_title":   title,
        "article_url":     article.get("link", ""),
        "article_date":    article.get("pubdate", ""),
        "article_summary": summary[:300],
    }


# ---------------------------------------------------------------------------
# CSV output
# ---------------------------------------------------------------------------

_LEAD_FIELDS = [
    "scraped_at", "source", "company_name", "funding_stage",
    "funding_amount", "company_size", "tech_stack", "website",
    "founder_emails", "article_title", "article_url", "article_date",
    "article_summary",
]


def write_leads_csv(leads, logger):
    dest = safe_path(LEADS_CSV)
    dest.parent.mkdir(parents=True, exist_ok=True)
    write_header = not dest.exists() or dest.stat().st_size == 0
    with open(str(dest), "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_LEAD_FIELDS, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerows(leads)
    logger.info(f"Wrote {len(leads)} leads → {dest}")


# ---------------------------------------------------------------------------
# Content generation
# ---------------------------------------------------------------------------

def generate_content_pieces(articles):
    """Convert funding articles into engagement posts about AI/VC trends."""
    pieces = []
    stage_counts = {}

    for art in articles:
        full    = f"{art['title']} {art['summary']}"
        stage   = extract_funding_stage(full)
        amount  = extract_funding_amount(full)
        stack   = extract_tech_stack(full)
        company = extract_company_name(art["title"])
        stage_counts[stage] = stage_counts.get(stage, 0) + 1

        verb_tail = " ".join(art["title"].split()[1:])[:70]
        post = (
            f"\U0001f4b0 {company} just {verb_tail}...\n\n"
            f"Stage: {stage}  |  Amount: {amount or 'undisclosed'}\n"
            f"Tech: {', '.join(stack[:4]) if stack else 'stealth'}\n\n"
            "AI startups are eating the venture industry \u2014 and the returns, "
            "so far, are good. Fresh-funded teams need automation, dev support, "
            "and content infrastructure NOW.\n\n"
            "#AIStartups #VentureCapital #Funding #Automation #PRINTMAXX"
        )
        pieces.append({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "type":         "linkedin_post",
            "company":      company,
            "stage":        stage,
            "amount":       amount,
            "stack":        stack,
            "content":      post,
            "source_url":   art.get("link", ""),
        })

    if stage_counts:
        top = sorted(stage_counts.items(), key=lambda x: x[1], reverse=True)
        breakdown = ", ".join(f"{s} ({n})" for s, n in top[:4])
        trend_post = (
            f"AI Funding Pulse \u2014 {datetime.now().strftime('%B %Y')}\n\n"
            f"Scanned {len(articles)} AI funding announcements.\n"
            f"Stage breakdown: {breakdown}.\n\n"
            "The signal is clear: capital is flooding into AI at every stage. "
            "Newly funded teams are actively buying services. "
            "PRINTMAXX helps these teams move faster with automation, "
            "dev support, and content infrastructure.\n\n"
            "#AITrends #VCPulse #StartupFunding #PRINTMAXX"
        )
        pieces.append({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "type":         "trend_summary",
            "company":      "AGGREGATE",
            "stage":        "",
            "amount":       "",
            "stack":        [],
            "content":      trend_post,
            "source_url":   "",
        })

    return pieces


def write_content_json(pieces, logger):
    dest = safe_path(CONTENT_JSON)
    dest.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if dest.exists():
        try:
            with open(str(dest), "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, OSError):
            existing = []
    combined = (existing + pieces)[-500:]
    with open(str(dest), "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    logger.info(f"Wrote {len(pieces)} content pieces → {dest} ({len(combined)} total)")


# ---------------------------------------------------------------------------
# Status helpers
# ---------------------------------------------------------------------------

def write_status(status, logger):
    dest = safe_path(STATUS_FILE)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(str(dest), "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2)
    logger.debug(f"Status written → {dest}")


def read_status():
    try:
        p = safe_path(STATUS_FILE)
        if p.exists():
            with open(str(p), "r", encoding="utf-8") as f:
                return json.load(f)
    except (OSError, json.JSONDecodeError, ValueError):
        pass
    return {}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        prog="vc_ai_funding_lead_scraper",
        description=(
            "PRINTMAXX: scrape newly funded AI startups "
            "for cold outbound pipeline and trend content"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Run full scrape + enrich + write pipeline",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print last run status and exit",
    )
    group.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Scrape articles but skip website/email enrichment; print summary only",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    logger = setup_logging(dry_run=args.dry_run)

    if args.status:
        status = read_status()
        if not status:
            print("No previous run recorded.")
        else:
            print(json.dumps(status, indent=2))
        sys.exit(0)

    recall_skills_for_task("vc_ai_funding_lead_scraper")

    run_ts = datetime.now(timezone.utc).isoformat()
    logger.info(f"=== vc_ai_funding_lead_scraper START {run_ts} ===")

    if not args.dry_run and not check_network():
        logger.error("Network pre-flight check failed — aborting run")
        sys.exit(1)

    raw_articles = []

    try:
        raw_articles += scrape_techcrunch(logger)
    except Exception as exc:
        logger.error(f"TechCrunch scrape failed: {exc}")

    try:
        raw_articles += scrape_crunchbase(logger)
    except Exception as exc:
        logger.error(f"Crunchbase scrape failed: {exc}")

    try:
        raw_articles += scrape_pitchbook(logger)
    except Exception as exc:
        logger.error(f"PitchBook scrape failed: {exc}")

    # Deduplicate by URL
    seen = set()
    unique_articles = []
    for art in raw_articles:
        link = art.get("link", "")
        if link and link not in seen:
            seen.add(link)
            unique_articles.append(art)

    logger.info(f"Total unique AI funding articles: {len(unique_articles)}")

    leads = []
    for art in unique_articles:
        try:
            leads.append(build_lead(art, dry_run=args.dry_run, logger=logger))
        except Exception as exc:
            logger.warning(f"Lead build failed ('{art.get('title', '')}…'): {exc}")

    content_pieces = []
    try:
        content_pieces = generate_content_pieces(unique_articles)
    except Exception as exc:
        logger.error(f"Content generation failed: {exc}")

    if args.dry_run:
        print(f"\n[DRY RUN] articles={len(unique_articles)}  leads={len(leads)}  content={len(content_pieces)}")
        print(f"[DRY RUN] leads would be written to:   {LEADS_CSV}")
        print(f"[DRY RUN] content would be written to: {CONTENT_JSON}")
        if leads:
            print("\nSample leads:")
            for lead in leads[:3]:
                print(f"  {lead['company_name']:<30} {lead['funding_stage']:<12} {lead['funding_amount']}")
        if content_pieces:
            print("\nSample content piece:\n")
            print(content_pieces[0]["content"][:400] + "…")
    else:
        if leads:
            try:
                write_leads_csv(leads, logger)
            except Exception as exc:
                logger.error(f"CSV write failed: {exc}")

        if content_pieces:
            try:
                write_content_json(content_pieces, logger)
            except Exception as exc:
                logger.error(f"Content JSON write failed: {exc}")

    status = {
        "last_run":          run_ts,
        "articles_found":    len(unique_articles),
        "leads_generated":   len(leads),
        "content_pieces":    len(content_pieces),
        "dry_run":           args.dry_run,
        "sources_attempted": ["TechCrunch", "Crunchbase", "PitchBook"],
    }

    capture_skill_from_result("vc_ai_funding_lead_scraper", status)

    if not args.dry_run:
        try:
            write_status(status, logger)
        except Exception as exc:
            logger.warning(f"Status write failed: {exc}")

    logger.info(
        f"=== DONE | articles={len(unique_articles)} "
        f"leads={len(leads)} content={len(content_pieces)} ==="
    )


if __name__ == "__main__":
    main()