#!/usr/bin/env python3
"""
PRINTMAXX SEO Competitor Analyzer
---------------------------------
Compares a hot lead against all other businesses in the same category + city/state.
Generates competitive insights for cold email injection.

IMPORTANT: total_score in the CSV is a LEAD QUALITY score (higher = worse website
= better sales prospect). The WEBSITE QUALITY score shown to prospects is derived
from design_score + seo_score + aio_score (out of 75). We normalize to 0-100 for
the email snippets.

Usage:
    python3 seo_competitor_analyzer.py --top 5
    python3 seo_competitor_analyzer.py --lead-id UUID
    python3 seo_competitor_analyzer.py --industry dentist --city "New York" --state NY
    python3 seo_competitor_analyzer.py --summary
    python3 seo_competitor_analyzer.py --export /path/to/output.csv
"""

import argparse
import csv
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEADS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "leads" / "qualified"
HOT_LEADS_CSV = LEADS_DIR / "HOT_LEADS_QUALIFIED.csv"
ANALYZED_CSV = LEADS_DIR / "ANALYZED_LEADS.csv"
OUTPUT_DIR = PROJECT_ROOT / "AUTOMATIONS" / "leads" / "competitor_reports"

# Industry groupings: treat related categories as same competitive pool
INDUSTRY_GROUPS = {
    "dental": ["dentist", "cosmetic_dentist", "general_dentistry", "orthodontist", "pediatric_dentist", "dentistry_schools"],
    "legal": ["lawyer", "civil_rights_lawyers", "appellate_practice_lawyers"],
    "beauty": ["hair_salon", "beauty_salon", "nail_salon"],
}

CATEGORY_TO_GROUP = {}
for group, cats in INDUSTRY_GROUPS.items():
    for cat in cats:
        CATEGORY_TO_GROUP[cat] = group

# Pain signal -> human-readable label (what the TARGET is missing)
PAIN_LABELS = {
    "NO_SSL": "no SSL certificate (browsers show 'Not Secure')",
    "NO_MOBILE_VIEWPORT": "not mobile-friendly (60%+ of searches are mobile)",
    "OLD:table_layout": "outdated table-based layout from the 2000s",
    "OLD:font_tags": "deprecated HTML font tags",
    "OLD:frames": "uses HTML frames (obsolete since 2010)",
    "OLD:inline_styles_heavy": "heavy inline CSS (poor maintainability)",
    "SEO_MISSING:has_title": "missing page title tag",
    "SEO_MISSING:has_meta_desc": "missing meta description (Google shows random text instead)",
    "SEO_MISSING:has_h1": "missing H1 heading (confuses search engines)",
    "SEO_MISSING:has_h2": "missing H2 subheadings",
    "SEO_MISSING:has_schema": "no schema markup (invisible to Google rich results)",
    "SEO_MISSING:has_og_tags": "no Open Graph tags (broken previews on social media)",
    "SEO_MISSING:has_canonical": "no canonical URL (duplicate content risk)",
    "SEO_MISSING:has_sitemap_ref": "no sitemap (Google can't index all your pages)",
    "SEO_MISSING:has_robots_meta": "no robots meta tag",
    "SEO_MISSING:has_alt_tags": "missing image alt tags (hurts SEO and accessibility)",
    "AIO_MISSING:has_faq": "no FAQ section (missing AI Overview opportunity)",
    "AIO_MISSING:has_qa_schema": "no Q&A schema",
    "AIO_MISSING:has_howto_schema": "no HowTo schema",
    "AIO_MISSING:has_local_business_schema": "no LocalBusiness schema (hurts Google Maps ranking)",
}

# What the competitor HAS that the target is missing
COMPETITOR_HAS_LABELS = {
    "NO_SSL": "SSL certificate (secure padlock in browser)",
    "NO_MOBILE_VIEWPORT": "mobile-friendly responsive design",
    "SEO_MISSING:has_meta_desc": "optimized meta descriptions",
    "SEO_MISSING:has_h1": "proper H1 heading structure",
    "SEO_MISSING:has_schema": "schema markup for Google rich results",
    "SEO_MISSING:has_og_tags": "Open Graph tags for social sharing",
    "SEO_MISSING:has_alt_tags": "image alt tags for SEO",
    "SEO_MISSING:has_sitemap_ref": "XML sitemap for full indexing",
    "AIO_MISSING:has_faq": "FAQ section (shows up in AI Overviews)",
    "AIO_MISSING:has_local_business_schema": "LocalBusiness schema for Google Maps",
}

# Niche-specific customer terms
CUSTOMER_TERMS = {
    "dental": "patients",
    "legal": "clients",
    "beauty": "clients",
    "real_estate_agent": "home buyers",
    "chiropractor": "patients",
    "veterinarian": "pet owners",
    "spanish_restaurant": "customers",
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
@dataclass
class Lead:
    id: str
    name: str
    category: str
    phone: str
    email: str
    website: str
    domain: str
    city: str
    state: str
    lat: float
    lon: float
    total_score: int       # Lead quality score (higher = worse website = better prospect)
    design_score: int      # 0-25: website design quality
    seo_score: int         # 0-25: SEO quality
    aio_score: int         # 0-25: AI Overview readiness
    pain_signals: list = field(default_factory=list)
    ssl_valid: str = ""
    mobile_friendly: str = ""
    cms_detected: str = ""
    response_time_ms: int = 0
    is_hot: bool = False

    @property
    def website_score(self) -> int:
        """Website quality score 0-100 (higher = better website).
        Derived from design + seo + aio (each 0-25, total 0-75), normalized to 0-100."""
        raw = self.design_score + self.seo_score + self.aio_score
        return round(raw * 100 / 75)

    @property
    def pain_count(self) -> int:
        return len(self.pain_signals)


@dataclass
class CompetitorReport:
    target: Lead
    competitors: list                  # list of Lead, sorted by website_score desc
    same_city_count: int
    same_state_count: int
    city_rank: int                     # 1 = worst website in city (most pain)
    city_rank_total: int               # total in city
    state_rank: int
    state_rank_total: int
    city_avg_website_score: float
    state_avg_website_score: float
    best_competitor: Optional[Lead]    # competitor with highest website_score
    advantages_over_target: list       # things best competitor has that target lacks
    email_snippet: str = ""


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------
def _safe_int(val, default=0):
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def _safe_float(val, default=0.0):
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def parse_lead(row: dict, is_hot: bool = False) -> Lead:
    pain = row.get("pain_signals", "")
    pain_list = [p.strip() for p in pain.split("|") if p.strip()] if pain else []

    return Lead(
        id=row.get("id", ""),
        name=row.get("name", ""),
        category=row.get("category", ""),
        phone=row.get("phone", ""),
        email=row.get("email", ""),
        website=row.get("website", ""),
        domain=row.get("domain", ""),
        city=row.get("city", ""),
        state=row.get("state", ""),
        lat=_safe_float(row.get("lat")),
        lon=_safe_float(row.get("lon")),
        total_score=_safe_int(row.get("total_score")),
        design_score=_safe_int(row.get("design_score")),
        seo_score=_safe_int(row.get("seo_score")),
        aio_score=_safe_int(row.get("aio_score")),
        pain_signals=pain_list,
        ssl_valid=row.get("ssl_valid", ""),
        mobile_friendly=row.get("mobile_friendly", ""),
        cms_detected=row.get("cms_detected", ""),
        response_time_ms=_safe_int(row.get("response_time_ms")),
        is_hot=is_hot,
    )


def load_all_leads() -> tuple[list[Lead], list[Lead]]:
    """Load hot leads and all analyzed leads."""
    hot_leads = []
    if HOT_LEADS_CSV.exists():
        with open(HOT_LEADS_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                hot_leads.append(parse_lead(row, is_hot=True))

    all_leads = []
    if ANALYZED_CSV.exists():
        with open(ANALYZED_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                all_leads.append(parse_lead(row))

    return hot_leads, all_leads


def haversine_miles(lat1, lon1, lat2, lon2) -> float:
    """Distance in miles between two lat/lon points."""
    R = 3959
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


# ---------------------------------------------------------------------------
# Indexing
# ---------------------------------------------------------------------------
def build_indexes(all_leads: list[Lead]) -> dict:
    """Build city+category and state+category indexes."""
    city_cat = defaultdict(list)
    state_cat = defaultdict(list)

    for lead in all_leads:
        group = CATEGORY_TO_GROUP.get(lead.category, lead.category)
        city_key = (lead.city.lower().strip(), lead.state.upper().strip(), group)
        state_key = (lead.state.upper().strip(), group)
        city_cat[city_key].append(lead)
        state_cat[state_key].append(lead)

    return {"city": city_cat, "state": state_cat}


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def analyze_lead(target: Lead, indexes: dict, nearby_radius_miles: float = 30.0) -> CompetitorReport:
    """Generate competitive analysis for a single lead."""
    group = CATEGORY_TO_GROUP.get(target.category, target.category)
    city_key = (target.city.lower().strip(), target.state.upper().strip(), group)
    state_key = (target.state.upper().strip(), group)

    city_comps = [l for l in indexes["city"].get(city_key, []) if l.id != target.id]
    state_comps = [l for l in indexes["state"].get(state_key, []) if l.id != target.id]

    # Expand to nearby cities if too few local competitors
    if len(city_comps) < 3 and target.lat != 0 and target.lon != 0:
        city_ids = {c.id for c in city_comps}
        for lead in state_comps:
            if lead.id != target.id and lead.id not in city_ids:
                if lead.lat != 0 and lead.lon != 0:
                    dist = haversine_miles(target.lat, target.lon, lead.lat, lead.lon)
                    if dist <= nearby_radius_miles:
                        city_comps.append(lead)
                        city_ids.add(lead.id)

    # Sort by WEBSITE QUALITY (higher = better website), not lead score
    city_sorted = sorted(city_comps, key=lambda l: l.website_score, reverse=True)
    state_sorted = sorted(state_comps, key=lambda l: l.website_score, reverse=True)

    # City rank: how many local competitors have a BETTER website than target
    # Rank 1 = best website in city, Rank N = worst
    city_better = sum(1 for c in city_comps if c.website_score > target.website_score)
    city_rank = city_better + 1
    city_total = len(city_comps) + 1

    state_better = sum(1 for c in state_comps if c.website_score > target.website_score)
    state_rank = state_better + 1
    state_total = len(state_comps) + 1

    # Averages (website quality)
    city_ws = [c.website_score for c in city_comps]
    state_ws = [c.website_score for c in state_comps]
    city_avg = sum(city_ws) / len(city_ws) if city_ws else 0
    state_avg = sum(state_ws) / len(state_ws) if state_ws else 0

    # Best competitor = highest website quality score in city (or state fallback)
    best_comp = city_sorted[0] if city_sorted else (state_sorted[0] if state_sorted else None)

    # Advantages: pain signals target has that best competitor does NOT
    advantages = []
    if best_comp:
        target_pains = set(target.pain_signals)
        best_pains = set(best_comp.pain_signals)
        for pain in target_pains:
            if pain not in best_pains and pain in COMPETITOR_HAS_LABELS:
                advantages.append(COMPETITOR_HAS_LABELS[pain])

    report = CompetitorReport(
        target=target,
        competitors=city_sorted[:10],
        same_city_count=city_total,
        same_state_count=state_total,
        city_rank=city_rank,
        city_rank_total=city_total,
        state_rank=state_rank,
        state_rank_total=state_total,
        city_avg_website_score=round(city_avg, 1),
        state_avg_website_score=round(state_avg, 1),
        best_competitor=best_comp,
        advantages_over_target=advantages,
    )

    report.email_snippet = generate_email_snippet(report)
    return report


def _group_label(category: str) -> str:
    labels = {
        "dentist": "dental practice",
        "cosmetic_dentist": "dental practice",
        "general_dentistry": "dental practice",
        "orthodontist": "dental practice",
        "pediatric_dentist": "dental practice",
        "lawyer": "law firm",
        "civil_rights_lawyers": "law firm",
        "appellate_practice_lawyers": "law firm",
        "hair_salon": "salon",
        "beauty_salon": "salon",
        "nail_salon": "salon",
        "real_estate_agent": "real estate agency",
        "chiropractor": "chiropractic practice",
        "veterinarian": "veterinary clinic",
        "spanish_restaurant": "restaurant",
    }
    return labels.get(category, category.replace("_", " "))


def _customer_term(category: str) -> str:
    group = CATEGORY_TO_GROUP.get(category, category)
    return CUSTOMER_TERMS.get(group, CUSTOMER_TERMS.get(category, "customers"))


def _get_critical_pains(pain_signals: list) -> list:
    """Return human-readable critical pain points in priority order."""
    critical_order = [
        "NO_SSL",
        "NO_MOBILE_VIEWPORT",
        "SEO_MISSING:has_meta_desc",
        "SEO_MISSING:has_schema",
        "SEO_MISSING:has_alt_tags",
        "AIO_MISSING:has_faq",
        "AIO_MISSING:has_local_business_schema",
        "SEO_MISSING:has_h1",
        "SEO_MISSING:has_og_tags",
        "SEO_MISSING:has_sitemap_ref",
        "OLD:table_layout",
        "OLD:font_tags",
        "OLD:frames",
    ]
    pain_set = set(pain_signals)
    return [PAIN_LABELS[p] for p in critical_order if p in pain_set and p in PAIN_LABELS]


def generate_email_snippet(report: CompetitorReport) -> str:
    """Generate a cold-email-ready competitive insight paragraph."""
    t = report.target
    bc = report.best_competitor
    ws = t.website_score
    cust = _customer_term(t.category)
    gl = _group_label(t.category)

    lines = []

    # Opening: how many competitors analyzed, your score
    if report.same_city_count > 2:
        lines.append(
            f"I analyzed {report.same_city_count} {gl} websites in {t.city}, {t.state}."
        )
        lines.append(
            f"Your site ({t.domain}) scored {ws}/100 on web presence."
        )
        if report.city_avg_website_score > ws:
            lines.append(
                f"The local average is {report.city_avg_website_score:.0f}/100."
            )
            lines.append(
                f"You rank #{report.city_rank} out of {report.city_rank_total}."
            )
        elif report.city_rank > 1:
            lines.append(
                f"You rank #{report.city_rank} out of {report.city_rank_total} locally."
            )
    else:
        lines.append(
            f"I analyzed {gl} websites across {t.state}."
        )
        lines.append(
            f"Your site ({t.domain}) scored {ws}/100 on web presence."
        )
        if report.state_avg_website_score > ws:
            lines.append(
                f"State average: {report.state_avg_website_score:.0f}/100."
            )

    # Best competitor comparison
    if bc and bc.website_score > ws:
        gap = bc.website_score - ws
        lines.append(
            f"Your top local competitor ({bc.name}) scores {bc.website_score}/100, {gap} points ahead."
        )
        if report.advantages_over_target:
            adv_str = ", ".join(report.advantages_over_target[:3])
            lines.append(f"They have {adv_str}. You don't.")

    # Key pain points (max 3 for email brevity)
    key_pains = _get_critical_pains(t.pain_signals)
    if key_pains:
        lines.append(f"Biggest issues: {key_pains[0]}")
        if len(key_pains) > 1:
            lines[-1] += f", {key_pains[1]}"
        lines[-1] += "."

    # Consequence framing
    if t.seo_score <= 10:
        lines.append(
            f"When {cust} search Google for a {gl.rstrip(' practice').rstrip(' agency').rstrip(' clinic')} in {t.city}, your site isn't showing up."
        )
    if t.aio_score <= 10:
        lines.append(
            f"When {cust} ask ChatGPT or Google AI for recommendations, you're invisible."
        )

    return " ".join(lines)


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
def _wrap_print(text: str, indent: int = 2, width: int = 76):
    """Word-wrap and print text with indentation."""
    prefix = " " * indent
    words = text.split()
    line = prefix
    for word in words:
        if len(line) + len(word) + 1 > width:
            print(line)
            line = prefix + word
        else:
            line += (" " + word) if len(line) > indent else word
    if line.strip():
        print(line)


def print_report(report: CompetitorReport, verbose: bool = True):
    """Print a competitive analysis report to stdout."""
    t = report.target
    bc = report.best_competitor

    print("=" * 78)
    print(f"  COMPETITIVE ANALYSIS: {t.name}")
    print(f"  {t.domain} | {t.city}, {t.state} | {t.category}")
    print("=" * 78)

    # Score card (website quality scores, not lead quality)
    bc_ws = bc.website_score if bc else "-"
    bc_d = bc.design_score if bc else "-"
    bc_s = bc.seo_score if bc else "-"
    bc_a = bc.aio_score if bc else "-"

    print(f"\n  WEBSITE QUALITY SCORES")
    print(f"  {'Metric':<22} {'You':>6} {'City Avg':>10} {'Best Comp':>10}")
    print(f"  {'-'*22} {'-'*6} {'-'*10} {'-'*10}")
    print(f"  {'Web Presence (/100)':<22} {t.website_score:>6} {report.city_avg_website_score:>10.0f} {bc_ws!s:>10}")
    print(f"  {'Design (/25)':<22} {t.design_score:>6} {'':>10} {bc_d!s:>10}")
    print(f"  {'SEO (/25)':<22} {t.seo_score:>6} {'':>10} {bc_s!s:>10}")
    print(f"  {'AI Readiness (/25)':<22} {t.aio_score:>6} {'':>10} {bc_a!s:>10}")

    # Rankings (lower rank = better website, higher rank = worse)
    print(f"\n  LOCAL RANKING")
    print(f"  City:  #{report.city_rank} of {report.city_rank_total} in {t.city}, {t.state}")
    print(f"  State: #{report.state_rank} of {report.state_rank_total} in {t.state}")
    if report.city_rank > report.city_rank_total * 0.5:
        pct = round((report.city_rank / report.city_rank_total) * 100)
        print(f"  -> Bottom {pct}% in your city. {_customer_term(t.category).title()} searching online are finding competitors first.")

    # Best competitor detail
    if bc:
        print(f"\n  TOP LOCAL COMPETITOR")
        print(f"  {bc.name} ({bc.domain})")
        print(f"  Web presence: {bc.website_score}/100 | Design: {bc.design_score}/25 | SEO: {bc.seo_score}/25 | AI: {bc.aio_score}/25")
        if report.advantages_over_target:
            print(f"  They have (you don't):")
            for adv in report.advantages_over_target[:6]:
                print(f"    + {adv}")

    # Pain points
    key_pains = _get_critical_pains(t.pain_signals)
    if key_pains:
        print(f"\n  YOUR CRITICAL ISSUES ({len(key_pains)} found)")
        for i, pain in enumerate(key_pains[:8], 1):
            print(f"  {i}. {pain}")

    # City competitors table
    if verbose and report.competitors:
        print(f"\n  LOCAL COMPETITORS ({t.city}, {t.state})")
        print(f"  {'#':<4} {'Name':<32} {'Score':>6} {'Design':>7} {'SEO':>5} {'AI':>4} {'SSL':>5} {'Mobile':>7}")
        print(f"  {'-'*4} {'-'*32} {'-'*6} {'-'*7} {'-'*5} {'-'*4} {'-'*5} {'-'*7}")
        for i, c in enumerate(report.competitors[:10], 1):
            name_trunc = c.name[:30] + ".." if len(c.name) > 32 else c.name
            ssl = "YES" if "NO_SSL" not in c.pain_signals else "NO"
            mob = "YES" if "NO_MOBILE_VIEWPORT" not in c.pain_signals else "NO"
            print(f"  {i:<4} {name_trunc:<32} {c.website_score:>6} {c.design_score:>7} {c.seo_score:>5} {c.aio_score:>4} {ssl:>5} {mob:>7}")

    # Email snippet
    print(f"\n  COLD EMAIL SNIPPET")
    print(f"  {'-' * 72}")
    _wrap_print(report.email_snippet, indent=2, width=74)
    print(f"  {'-' * 72}")
    print()


def print_summary(hot_leads: list, all_leads: list, indexes: dict):
    """Print aggregate summary stats."""
    print("=" * 62)
    print("  PRINTMAXX SEO COMPETITOR ANALYZER — SUMMARY")
    print("=" * 62)
    print(f"\n  Data:")
    print(f"    Hot leads (bad websites, great prospects): {len(hot_leads):,}")
    print(f"    Total analyzed businesses:                 {len(all_leads):,}")

    # Industry breakdown
    cat_counts = defaultdict(int)
    for l in all_leads:
        group = CATEGORY_TO_GROUP.get(l.category, l.category)
        cat_counts[group] += 1
    print(f"\n  Industries ({len(cat_counts)}):")
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f"    {cat:<25} {count:>6} businesses")

    # Top competitive cities
    city_counts = defaultdict(int)
    for l in all_leads:
        city_counts[(l.city, l.state)] += 1
    top_cities = sorted(city_counts.items(), key=lambda x: -x[1])[:10]
    print(f"\n  Most competitive markets:")
    for (city, state), count in top_cities:
        print(f"    {city}, {state:<5} {count:>5} businesses")

    # Website quality distribution of hot leads
    if hot_leads:
        ws_scores = [l.website_score for l in hot_leads]
        avg_ws = sum(ws_scores) / len(ws_scores)
        print(f"\n  Hot lead website quality:")
        print(f"    Average website score: {avg_ws:.0f}/100 (lower = worse site = better prospect)")
        print(f"    Worst website:  {min(ws_scores)}/100")
        print(f"    Best website:   {max(ws_scores)}/100")

        no_ssl = sum(1 for l in hot_leads if "NO_SSL" in l.pain_signals)
        no_mobile = sum(1 for l in hot_leads if "NO_MOBILE_VIEWPORT" in l.pain_signals)
        no_schema = sum(1 for l in hot_leads if "SEO_MISSING:has_schema" in l.pain_signals)
        no_faq = sum(1 for l in hot_leads if "AIO_MISSING:has_faq" in l.pain_signals)
        print(f"\n  Pain signal prevalence (hot leads):")
        print(f"    No SSL:            {no_ssl:>5} ({no_ssl*100//len(hot_leads)}%)")
        print(f"    Not mobile:        {no_mobile:>5} ({no_mobile*100//len(hot_leads)}%)")
        print(f"    No schema markup:  {no_schema:>5} ({no_schema*100//len(hot_leads)}%)")
        print(f"    No FAQ section:    {no_faq:>5} ({no_faq*100//len(hot_leads)}%)")

    print()


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
def export_reports(reports: list[CompetitorReport], filepath: str):
    """Export competitive reports to CSV."""
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    fieldnames = [
        "lead_id", "name", "email", "domain", "category", "city", "state",
        "website_score", "design_score", "seo_score", "aio_score",
        "city_rank", "city_total", "city_avg_score",
        "state_rank", "state_total", "state_avg_score",
        "best_competitor_name", "best_competitor_domain", "best_competitor_score",
        "advantages_they_have", "critical_pains", "email_snippet",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in reports:
            bc = r.best_competitor
            writer.writerow({
                "lead_id": r.target.id,
                "name": r.target.name,
                "email": r.target.email,
                "domain": r.target.domain,
                "category": r.target.category,
                "city": r.target.city,
                "state": r.target.state,
                "website_score": r.target.website_score,
                "design_score": r.target.design_score,
                "seo_score": r.target.seo_score,
                "aio_score": r.target.aio_score,
                "city_rank": r.city_rank,
                "city_total": r.city_rank_total,
                "city_avg_score": r.city_avg_website_score,
                "state_rank": r.state_rank,
                "state_total": r.state_rank_total,
                "state_avg_score": r.state_avg_website_score,
                "best_competitor_name": bc.name if bc else "",
                "best_competitor_domain": bc.domain if bc else "",
                "best_competitor_score": bc.website_score if bc else "",
                "advantages_they_have": " | ".join(r.advantages_over_target[:5]),
                "critical_pains": " | ".join(_get_critical_pains(r.target.pain_signals)[:5]),
                "email_snippet": r.email_snippet,
            })

    print(f"  Exported {len(reports)} reports to {filepath}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX SEO Competitor Analyzer - compare leads against local competitors"
    )
    parser.add_argument("--lead-id", help="Analyze a specific lead by UUID")
    parser.add_argument("--top", type=int, help="Analyze top N hot leads (by lead quality desc)")
    parser.add_argument("--industry", help="Filter by industry/category (e.g. dentist, lawyer, real_estate_agent)")
    parser.add_argument("--city", help="Filter by city name")
    parser.add_argument("--state", help="Filter by state abbreviation (e.g. CA, NY)")
    parser.add_argument("--export", help="Export results to CSV file path")
    parser.add_argument("--summary", action="store_true", help="Print aggregate summary stats")
    parser.add_argument("--brief", action="store_true", help="Brief output (email snippet only)")
    parser.add_argument("--all-hot", action="store_true", help="Analyze ALL hot leads")

    args = parser.parse_args()

    print("  Loading leads data...")
    hot_leads, all_leads = load_all_leads()
    print(f"  Loaded {len(hot_leads):,} hot leads, {len(all_leads):,} analyzed leads")

    if not all_leads:
        print("  ERROR: No analyzed leads found. Check ANALYZED_LEADS.csv.")
        sys.exit(1)

    indexes = build_indexes(all_leads)

    if args.summary:
        print_summary(hot_leads, all_leads, indexes)
        return

    # Select targets
    targets = []

    if args.lead_id:
        match = [l for l in all_leads if l.id == args.lead_id]
        if not match:
            match = [l for l in hot_leads if l.id == args.lead_id]
        if not match:
            print(f"  ERROR: Lead ID {args.lead_id} not found.")
            sys.exit(1)
        targets = match[:1]

    elif args.top:
        pool = hot_leads
        if args.industry:
            group = CATEGORY_TO_GROUP.get(args.industry, args.industry)
            pool = [l for l in pool if CATEGORY_TO_GROUP.get(l.category, l.category) == group or l.category == args.industry]
        if args.city:
            pool = [l for l in pool if l.city.lower() == args.city.lower()]
        if args.state:
            pool = [l for l in pool if l.state.upper() == args.state.upper()]
        pool = sorted(pool, key=lambda l: l.total_score, reverse=True)
        targets = pool[:args.top]

    elif args.industry or args.city or args.state:
        pool = hot_leads if hot_leads else all_leads
        if args.industry:
            group = CATEGORY_TO_GROUP.get(args.industry, args.industry)
            pool = [l for l in pool if CATEGORY_TO_GROUP.get(l.category, l.category) == group or l.category == args.industry]
        if args.city:
            pool = [l for l in pool if l.city.lower() == args.city.lower()]
        if args.state:
            pool = [l for l in pool if l.state.upper() == args.state.upper()]
        pool = sorted(pool, key=lambda l: l.total_score, reverse=True)
        targets = pool[:20]

    elif args.all_hot:
        targets = hot_leads

    else:
        targets = sorted(hot_leads, key=lambda l: l.total_score, reverse=True)[:5]

    if not targets:
        print("  No leads matched the filter criteria.")
        sys.exit(0)

    print(f"  Analyzing {len(targets)} lead(s)...\n")

    reports = []
    for target in targets:
        report = analyze_lead(target, indexes)
        reports.append(report)
        if args.brief:
            print(f"  [{target.name}] ({target.domain}) - Web score: {target.website_score}/100")
            print(f"  Rank: #{report.city_rank}/{report.city_rank_total} in {target.city} | #{report.state_rank}/{report.state_rank_total} in {target.state}")
            print(f"  Snippet: {report.email_snippet}")
            print()
        else:
            print_report(report, verbose=True)

    if args.export:
        export_reports(reports, args.export)
    elif args.all_hot:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_path = OUTPUT_DIR / f"competitor_reports_{ts}.csv"
        export_reports(reports, str(default_path))

    print(f"  Analyzed {len(reports)} lead(s). Done.")
    if not args.export and not args.all_hot:
        print(f"  Tip: --export FILE.csv to save | --all-hot for all {len(hot_leads)} hot leads | --summary for stats")


if __name__ == "__main__":
    main()
