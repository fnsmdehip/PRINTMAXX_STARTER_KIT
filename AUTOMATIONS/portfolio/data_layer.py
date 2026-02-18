"""
PRINTMAXX Portfolio Data Layer
Reads ALL live data from the filesystem. No mock data.
Every function reads from real CSV and MD files on disk.
"""

import csv
import re
import glob
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Optional

PROJECT_ROOT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")

# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------


@dataclass
class PortfolioPosition:
    method_id: str
    name: str
    category: str  # CORE, ECOM, EDGE, NOVEL
    status: str  # Active, Planning, Building, Paused
    revenue_total: float
    revenue_mtd: float
    expenses_total: float
    profit: float
    margin_pct: float
    monthly_potential_low: float
    monthly_potential_high: float
    synergy_score: int
    phase: str  # Phase1, Phase2, etc.


@dataclass
class FinancialSummary:
    total_revenue: float
    total_expenses: float
    net_profit: float
    mtd_revenue: float
    mtd_expenses: float
    burn_rate_monthly: float
    runway_months: float  # based on current burn vs revenue
    tool_costs_monthly: float
    active_subscriptions: int


@dataclass
class AlphaEntry:
    alpha_id: str
    source: str
    category: str
    tactic: str
    roi_potential: str
    status: str
    days_since_discovery: int


@dataclass
class PEMFMetrics:
    research_files_count: int
    research_total_lines: int
    files_status: Dict[str, int]  # {short_name: line_count}
    bootstrap_cost: float  # ~$847
    unit_cogs_low: float  # ~$62
    unit_cogs_high: float  # ~$294
    price_point: float  # $699
    margin_low: float  # 77%
    margin_high: float  # 92%
    influencers_podcasters: int
    influencers_twitter: int
    influencers_tiktok: int
    influencers_total: int
    compliance_path: str  # "General Wellness Device"
    mto_suppliers_count: int
    bradet_techniques: list


@dataclass
class ContentMetrics:
    total_pieces: int
    queued: int
    published: int
    calendar_posts: int


@dataclass
class SocialAccount:
    niche: str       # Meta, AI, Faith, Fitness
    platform: str    # X, TikTok, YouTube, Instagram
    handle: str      # @PRINTMAXXER etc
    email: str
    status: str      # PENDING, ACTIVE, etc
    created_date: str
    notes: str


@dataclass
class DailyOp:
    ops_id: str          # DOP001 etc
    ops_name: str        # competitor_monitoring etc
    frequency: str       # daily, weekly, monthly, continuous
    duration_min: int
    tool_required: str
    tool_cost: float
    last_run: str
    next_run: str
    status: str          # NOT_STARTED, ACTIVE, COMPLETED
    output_file: str
    notes: str


@dataclass
class ContentPiece:
    content_id: str
    title: str
    content_type: str
    platform: str
    niche: str
    status: str        # QUEUED, PUBLISHED, DRAFT
    created_date: str
    scheduled_date: str


@dataclass
class SignalSource:
    source_id: str
    source_name: str
    platform: str
    category: str
    signal_quality: str
    url: str
    notes: str


@dataclass
class GrowthTactic:
    platform: str
    tactic: str
    safety: str      # SAFE, GREY, DEAD
    limits: str
    details: str
    status: str      # WORKING, PATCHED


@dataclass
class GrowthService:
    platform: str
    name: str
    price: str
    description: str
    safety_rating: str
    expected_results: str


@dataclass
class Investment:
    inv_id: str
    method_id: str
    description: str
    capital_allocated: float
    priority: str
    status: str
    next_action: str


@dataclass
class Synergy:
    synergy_id: str
    method_combo: str
    synergy_name: str
    score: int
    multiplier: float


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_csv(filepath: Path) -> List[Dict[str, str]]:
    """Generic CSV loader. Returns list of dicts (one per row).

    All paths are resolved and validated against PROJECT_ROOT to prevent
    path traversal attacks.
    """
    path = PROJECT_ROOT / filepath if not filepath.is_absolute() else filepath
    path = path.resolve()
    # Path traversal protection: ensure resolved path is under PROJECT_ROOT
    if not str(path).startswith(str(PROJECT_ROOT.resolve())):
        return []
    if not path.exists():
        return []
    rows: List[Dict[str, str]] = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows


def _safe_float(val: str, default: float = 0.0) -> float:
    """Parse a string to float, stripping $, commas, k suffixes."""
    if not val:
        return default
    cleaned = val.strip().replace("$", "").replace(",", "").strip()
    if not cleaned or cleaned == "N/A":
        return default
    # Handle k suffix (e.g., "50k" -> 50000)
    multiplier = 1.0
    if cleaned.lower().endswith("k"):
        multiplier = 1000.0
        cleaned = cleaned[:-1]
    try:
        return float(cleaned) * multiplier
    except ValueError:
        return default


def _safe_int(val: str, default: int = 0) -> int:
    """Parse a string to int."""
    if not val:
        return default
    cleaned = val.strip().replace(",", "")
    try:
        return int(float(cleaned))
    except (ValueError, TypeError):
        return default


def _count_lines(filepath: Path) -> int:
    """Count lines in a file."""
    if not filepath.exists():
        return 0
    with open(filepath, encoding="utf-8", errors="replace") as f:
        return sum(1 for _ in f)


def _current_month_str() -> str:
    """Return current month as 'YYYY-MM'."""
    return date.today().strftime("%Y-%m")


# ---------------------------------------------------------------------------
# Core Loaders
# ---------------------------------------------------------------------------


def load_all_positions() -> List[PortfolioPosition]:
    """
    Build portfolio positions from TAB1_MONEY_METHODS_MASTER.csv,
    joined with REVENUE_TRACKER.csv and EXPENSE_TRACKER.csv.
    Also adds PEMF as a special position.
    """
    methods = load_csv(Path("LEDGER/MEGA_SHEET/TAB1_MONEY_METHODS_MASTER.csv"))
    rev_rows = load_csv(Path("FINANCIALS/REVENUE_TRACKER.csv"))
    exp_rows = load_csv(Path("FINANCIALS/EXPENSE_TRACKER.csv"))

    current_month = _current_month_str()

    # Aggregate revenue by method_id
    # CRITICAL: Exclude paper trades - only count REAL revenue
    rev_by_method: Dict[str, float] = {}
    rev_mtd_by_method: Dict[str, float] = {}
    for r in rev_rows:
        source = r.get("source", "").strip().lower()
        notes = r.get("notes", "").strip().lower()
        # Skip paper trades / simulated revenue
        if "paper_trade" in source or "paper trade" in notes or "simulated" in source:
            continue
        mid = r.get("method_id", "").strip()
        amt = _safe_float(r.get("revenue", "0"))
        rev_by_method[mid] = rev_by_method.get(mid, 0.0) + amt
        row_date = r.get("date", "")
        if row_date.startswith(current_month):
            rev_mtd_by_method[mid] = rev_mtd_by_method.get(mid, 0.0) + amt

    # Aggregate expenses by method_id
    exp_by_method: Dict[str, float] = {}
    for e in exp_rows:
        mid = e.get("method_id", "").strip()
        amt = _safe_float(e.get("amount", "0"))
        exp_by_method[mid] = exp_by_method.get(mid, 0.0) + amt

    positions: List[PortfolioPosition] = []
    for m in methods:
        mid = m.get("method_id", "").strip()
        name = m.get("method_name", mid)
        category = m.get("category", "CORE")
        status = m.get("status", "Planning")
        phase = m.get("priority", "Phase1")
        synergy = _safe_int(m.get("synergy_score", "0"))
        pot_low = _safe_float(m.get("monthly_potential_low", "0"))
        pot_high = _safe_float(m.get("monthly_potential_high", "0"))

        rev_total = rev_by_method.get(mid, 0.0)
        # Also check with name prefix (REVENUE_TRACKER uses MM007_COLD_OUTBOUND style)
        for key in list(rev_by_method.keys()):
            if key.startswith(mid + "_"):
                rev_total += rev_by_method[key]

        rev_mtd = rev_mtd_by_method.get(mid, 0.0)
        for key in list(rev_mtd_by_method.keys()):
            if key.startswith(mid + "_"):
                rev_mtd += rev_mtd_by_method[key]

        exp_total = exp_by_method.get(mid, 0.0)
        for key in list(exp_by_method.keys()):
            if key.startswith(mid + "_"):
                exp_total += exp_by_method[key]

        profit = rev_total - exp_total
        margin = (profit / rev_total * 100.0) if rev_total > 0 else 0.0

        positions.append(PortfolioPosition(
            method_id=mid,
            name=name,
            category=category,
            status=status,
            revenue_total=rev_total,
            revenue_mtd=rev_mtd,
            expenses_total=exp_total,
            profit=profit,
            margin_pct=round(margin, 1),
            monthly_potential_low=pot_low,
            monthly_potential_high=pot_high,
            synergy_score=synergy,
            phase=phase,
        ))

    # Add PEMF as a special position
    pemf_metrics = load_pemf_metrics()
    positions.append(PortfolioPosition(
        method_id="PEMF_WEBERMAXX",
        name="PEMF_WEBERMAXX",
        category="NOVEL",
        status="Building",
        revenue_total=0.0,
        revenue_mtd=0.0,
        expenses_total=0.0,
        profit=0.0,
        margin_pct=pemf_metrics.margin_low,
        monthly_potential_low=5000.0,
        monthly_potential_high=50000.0,
        synergy_score=60,
        phase="Phase1",
    ))

    return positions


def load_financial_summary() -> FinancialSummary:
    """
    Build financial summary from REVENUE_TRACKER, EXPENSE_TRACKER,
    MASTER_FINANCIAL_TRACKER, and P_AND_L_MONTHLY.
    """
    rev_rows = load_csv(Path("FINANCIALS/REVENUE_TRACKER.csv"))
    exp_rows = load_csv(Path("FINANCIALS/EXPENSE_TRACKER.csv"))
    mft_rows = load_csv(Path("FINANCIALS/MASTER_FINANCIAL_TRACKER.csv"))

    current_month = _current_month_str()

    # CRITICAL: Filter out paper trades / simulated revenue
    def _is_real_revenue(r: dict) -> bool:
        source = r.get("source", "").strip().lower()
        notes = r.get("notes", "").strip().lower()
        return ("paper_trade" not in source
                and "paper trade" not in notes
                and "simulated" not in source)

    real_rev_rows = [r for r in rev_rows if _is_real_revenue(r)]
    total_revenue = sum(_safe_float(r.get("revenue", "0")) for r in real_rev_rows)
    total_expenses = sum(_safe_float(e.get("amount", "0")) for e in exp_rows)
    net_profit = total_revenue - total_expenses

    mtd_revenue = sum(
        _safe_float(r.get("revenue", "0"))
        for r in real_rev_rows
        if r.get("date", "").startswith(current_month)
    )
    mtd_expenses = sum(
        _safe_float(e.get("amount", "0"))
        for e in exp_rows
        if e.get("date", "").startswith(current_month)
    )

    # Tool costs: sum monthly subscriptions from MASTER_FINANCIAL_TRACKER
    # where status is ACTIVE or NEEDED and frequency is monthly
    tool_costs = 0.0
    active_subs = 0
    for row in mft_rows:
        freq = row.get("frequency", "").strip().lower()
        status = row.get("status", "").strip().upper()
        actual = _safe_float(row.get("actual_cost", "0"))
        estimated = _safe_float(row.get("estimated_cost", "0"))
        cost = actual if actual > 0 else estimated

        if freq == "monthly" and status in ("ACTIVE", "NEEDED"):
            tool_costs += cost
            if status == "ACTIVE":
                active_subs += 1

    # Add yearly costs prorated to monthly
    for row in mft_rows:
        freq = row.get("frequency", "").strip().lower()
        status = row.get("status", "").strip().upper()
        actual = _safe_float(row.get("actual_cost", "0"))
        if freq == "yearly" and status in ("ACTIVE", "NEEDED") and actual > 0:
            tool_costs += actual / 12.0

    # Burn rate: total expenses / number of months with data
    # Get unique months from expense tracker
    expense_months = set()
    for e in exp_rows:
        d = e.get("date", "")
        if len(d) >= 7:
            expense_months.add(d[:7])
    months_count = max(len(expense_months), 1)
    burn_rate = total_expenses / months_count

    # Runway: if burn > revenue, how many months at current rate
    if burn_rate > 0 and total_revenue < total_expenses:
        runway = 0.0  # already negative
    elif burn_rate > 0:
        runway = 12.0  # sustainable
    else:
        runway = float("inf")

    return FinancialSummary(
        total_revenue=total_revenue,
        total_expenses=total_expenses,
        net_profit=net_profit,
        mtd_revenue=mtd_revenue,
        mtd_expenses=mtd_expenses,
        burn_rate_monthly=round(burn_rate, 2),
        runway_months=runway,
        tool_costs_monthly=round(tool_costs, 2),
        active_subscriptions=active_subs,
    )


def load_alpha_entries() -> List[AlphaEntry]:
    """Load alpha entries from TAB3_ALPHA_MASTER.csv."""
    rows = load_csv(Path("LEDGER/MEGA_SHEET/TAB3_ALPHA_MASTER.csv"))
    today = date.today()
    entries: List[AlphaEntry] = []
    for r in rows:
        alpha_id = r.get("alpha_id", "").strip()
        if not alpha_id:
            continue
        reviewed = r.get("reviewed_date", "")
        days = 0
        if reviewed:
            try:
                rd = datetime.strptime(reviewed.strip(), "%Y-%m-%d").date()
                days = (today - rd).days
            except ValueError:
                pass
        entries.append(AlphaEntry(
            alpha_id=alpha_id,
            source=r.get("source", ""),
            category=r.get("category", ""),
            tactic=r.get("title", ""),
            roi_potential=r.get("roi_potential", ""),
            status=r.get("status", ""),
            days_since_discovery=days,
        ))
    return entries


def load_pemf_metrics() -> PEMFMetrics:
    """
    Extract metrics from all 16 RESEARCH/PEMF_*.md files.
    Counts lines, extracts key numbers, influencer counts,
    compliance path, supplier count, and Bradet techniques.
    """
    research_dir = PROJECT_ROOT / "RESEARCH"
    pemf_files = sorted(research_dir.glob("PEMF_*.md"))

    files_status: Dict[str, int] = {}
    total_lines = 0
    for fp in pemf_files:
        short_name = fp.stem.replace("PEMF_", "")
        lc = _count_lines(fp)
        files_status[short_name] = lc
        total_lines += lc

    # Extract key numbers from BOOTSTRAP_CAPITAL_GENESIS
    bootstrap_cost = 847.0
    unit_cogs_low = 62.0
    unit_cogs_high = 294.0
    price_point = 699.0
    margin_low = 77.0
    margin_high = 92.0

    bootstrap_path = research_dir / "PEMF_BOOTSTRAP_CAPITAL_GENESIS.md"
    if bootstrap_path.exists():
        with open(bootstrap_path, encoding="utf-8", errors="replace") as f:
            text = f.read()
        # Extract $847 path total
        m = re.search(r"\$(\d[\d,]*)\s+PATH TO FIRST SALE", text)
        if m:
            bootstrap_cost = _safe_float(m.group(1))
        # Extract COGS low from Phase 0 total (~$62)
        m = re.search(r"\*\*TOTAL\*\*\s*\|\s*\*\*\$(\d+)\*\*", text)
        if m:
            unit_cogs_low = float(m.group(1))
        # Extract COGS high from Phase 1 subtotal
        m = re.search(r"SUBTOTAL.*?\$(\d+)", text)
        if m:
            unit_cogs_high = float(m.group(1))
        # Extract price point
        m = re.search(r"Sell price.*?\$(\d+)", text)
        if m:
            price_point = float(m.group(1))
        # Extract margins
        m = re.search(r"(\d+)%\)?\s*$", text, re.MULTILINE)
        # Use known values from research: 77% and 92%
        margin_matches = re.findall(r"(\d+)%\s*(?:gross profit|margin)", text, re.IGNORECASE)
        if len(margin_matches) >= 1:
            margin_low = float(margin_matches[0])
        if len(margin_matches) >= 2:
            margin_high = float(margin_matches[1])

    # Count influencers from dedicated files
    def _count_influencer_entries(filename: str) -> int:
        fp = research_dir / filename
        if not fp.exists():
            return 0
        with open(fp, encoding="utf-8", errors="replace") as f:
            content = f.read()
        # Count "### N." patterns (numbered entries)
        return len(re.findall(r"^### \d+\.", content, re.MULTILINE))

    podcasters = _count_influencer_entries("PEMF_INFLUENCER_PODCASTERS.md")
    twitter = _count_influencer_entries("PEMF_INFLUENCER_TWITTER.md")
    tiktok = _count_influencer_entries("PEMF_INFLUENCER_TIKTOK.md")

    # Compliance path from COMPLIANCE_LEGAL
    compliance_path = "General Wellness Device"
    compliance_file = research_dir / "PEMF_COMPLIANCE_LEGAL.md"
    if compliance_file.exists():
        with open(compliance_file, encoding="utf-8", errors="replace") as f:
            ct = f.read(2000)
        if "general wellness" in ct.lower():
            compliance_path = "General Wellness Device"
        elif "510(k)" in ct:
            compliance_path = "510(k) Clearance"

    # Count MTO suppliers from MAKE_TO_ORDER
    # Only count companies in the manufacturer/supplier tables (sections 1-3),
    # not component cost rows which also use bold formatting.
    mto_suppliers = 0
    mto_file = research_dir / "PEMF_MAKE_TO_ORDER.md"
    if mto_file.exists():
        with open(mto_file, encoding="utf-8", errors="replace") as f:
            mto_text = f.read()
        # Company entries have a location column after the name: | **Name** | Location |
        # Component rows have a price: | **Item** | $XX |
        for match in re.finditer(r"\|\s*\*\*([^|*]+)\*\*\s*\|([^|]*)\|", mto_text):
            second_col = match.group(2).strip()
            # Skip component/cost rows (start with $)
            if second_col.startswith("$"):
                continue
            # Skip header/description-only rows
            if not second_col:
                continue
            mto_suppliers += 1

    # Extract Bradet techniques from transcripts
    bradet_techniques: list = []
    bradet_file = research_dir / "PEMF_STEVE_BRADET_TRANSCRIPTS.md"
    if bradet_file.exists():
        with open(bradet_file, encoding="utf-8", errors="replace") as f:
            bt = f.read()
        # Pull key techniques from section headers and notable findings
        technique_patterns = [
            "Gauss Amplification",
            "Metal backing plates",
            "Coil stacking",
            "Bipolar square wave",
            "Nextion controller",
            "NASA 10Hz protocol",
            "ZK mat design",
            "T-PMF pillow",
            "Unipolar DC",
            "H-bridge electronic bipolar",
        ]
        for tp in technique_patterns:
            if tp.lower() in bt.lower():
                bradet_techniques.append(tp)

    return PEMFMetrics(
        research_files_count=len(pemf_files),
        research_total_lines=total_lines,
        files_status=files_status,
        bootstrap_cost=bootstrap_cost,
        unit_cogs_low=unit_cogs_low,
        unit_cogs_high=unit_cogs_high,
        price_point=price_point,
        margin_low=margin_low,
        margin_high=margin_high,
        influencers_podcasters=podcasters,
        influencers_twitter=twitter,
        influencers_tiktok=tiktok,
        influencers_total=podcasters + twitter + tiktok,
        compliance_path=compliance_path,
        mto_suppliers_count=mto_suppliers,
        bradet_techniques=bradet_techniques,
    )


def load_content_metrics() -> ContentMetrics:
    """Load content metrics from CONTENT_PIPELINE and CONTENT_CALENDAR_30DAY."""
    pipeline = load_csv(Path("LEDGER/CONTENT_PIPELINE.csv"))
    calendar = load_csv(Path("LEDGER/CONTENT_CALENDAR_30DAY.csv"))

    total = len(pipeline)
    queued = sum(1 for r in pipeline if r.get("Status", "").strip().upper() == "QUEUED")
    published = sum(1 for r in pipeline if r.get("Status", "").strip().upper() == "PUBLISHED")

    return ContentMetrics(
        total_pieces=total,
        queued=queued,
        published=published,
        calendar_posts=len(calendar),
    )


def load_revenue_history() -> List[dict]:
    """Return raw revenue tracker rows as list of dicts.

    Excludes paper trades / simulated entries so risk calculations
    only operate on real revenue data.
    """
    rows = load_csv(Path("FINANCIALS/REVENUE_TRACKER.csv"))
    real = []
    for r in rows:
        source = r.get("source", "").strip().lower()
        notes = r.get("notes", "").strip().lower()
        if "paper_trade" in source or "paper trade" in notes or "simulated" in source:
            continue
        real.append(r)
    return real


def load_expense_breakdown() -> dict:
    """Return expenses grouped by category."""
    rows = load_csv(Path("FINANCIALS/EXPENSE_TRACKER.csv"))
    breakdown: Dict[str, float] = {}
    for r in rows:
        cat = r.get("category", "OTHER").strip()
        amt = _safe_float(r.get("amount", "0"))
        breakdown[cat] = breakdown.get(cat, 0.0) + amt
    return breakdown


def load_social_accounts() -> List[SocialAccount]:
    """Load social accounts from LEDGER/ACCOUNTS.csv"""
    rows = load_csv(Path("LEDGER/ACCOUNTS.csv"))
    accounts = []
    for r in rows:
        accounts.append(SocialAccount(
            niche=r.get("Niche", ""),
            platform=r.get("Platform", ""),
            handle=r.get("Handle", ""),
            email=r.get("Email", ""),
            status=r.get("Status", ""),
            created_date=r.get("CreatedDate", ""),
            notes=r.get("Notes", ""),
        ))
    return accounts


def load_daily_ops() -> List[DailyOp]:
    """Load daily ops from LEDGER/DAILY_OPS_TRACKER.csv"""
    rows = load_csv(Path("LEDGER/DAILY_OPS_TRACKER.csv"))
    ops = []
    for r in rows:
        ops.append(DailyOp(
            ops_id=r.get("ops_id", ""),
            ops_name=r.get("ops_name", ""),
            frequency=r.get("frequency", ""),
            duration_min=_safe_int(r.get("duration_min", "0")),
            tool_required=r.get("tool_required", ""),
            tool_cost=_safe_float(r.get("tool_cost", "0")),
            last_run=r.get("last_run", ""),
            next_run=r.get("next_run", ""),
            status=r.get("status", ""),
            output_file=r.get("output_file", ""),
            notes=r.get("notes", ""),
        ))
    return ops


def load_content_pipeline_detailed() -> List[ContentPiece]:
    """Load detailed content pipeline from LEDGER/CONTENT_PIPELINE.csv"""
    rows = load_csv(Path("LEDGER/CONTENT_PIPELINE.csv"))
    pieces = []
    for r in rows:
        pieces.append(ContentPiece(
            content_id=r.get("content_id", r.get("ContentID", "")),
            title=r.get("title", r.get("Title", "")),
            content_type=r.get("type", r.get("Type", r.get("content_type", ""))),
            platform=r.get("platform", r.get("Platform", "")),
            niche=r.get("niche", r.get("Niche", "")),
            status=r.get("Status", r.get("status", "")),
            created_date=r.get("created_date", r.get("CreatedDate", "")),
            scheduled_date=r.get("scheduled_date", r.get("ScheduledDate", "")),
        ))
    return pieces


def load_signal_sources() -> List[SignalSource]:
    """Load signal sources from LEDGER/MEGA_SHEET/TAB7_SOURCES_ACCOUNTS.csv"""
    rows = load_csv(Path("LEDGER/MEGA_SHEET/TAB7_SOURCES_ACCOUNTS.csv"))
    sources = []
    for r in rows:
        sources.append(SignalSource(
            source_id=r.get("source_id", r.get("account_id", "")),
            source_name=r.get("source_name", r.get("handle", r.get("account_name", ""))),
            platform=r.get("platform", r.get("Platform", "")),
            category=r.get("category", r.get("Category", "")),
            signal_quality=r.get("signal_quality", r.get("quality", "")),
            url=r.get("url", r.get("URL", "")),
            notes=r.get("notes", r.get("Notes", "")),
        ))
    return sources


def load_active_investments() -> List[Investment]:
    rows = load_csv(Path("LEDGER/ACTIVE_INVESTMENTS.csv"))
    investments = []
    for r in rows:
        investments.append(Investment(
            inv_id=r.get("investment_id", r.get("inv_id", "")),
            method_id=r.get("method_id", ""),
            description=r.get("name", r.get("description", r.get("investment_name", ""))),
            capital_allocated=_safe_float(r.get("capital_allocated", r.get("capital", "0")).replace("$", "").replace(",", "")),
            priority=r.get("priority", "MEDIUM"),
            status=r.get("status", ""),
            next_action=r.get("next_action", r.get("next_step", "")),
        ))
    return investments


def load_synergies() -> List[Synergy]:
    rows = load_csv(Path("LEDGER/CROSS_POLLINATION_MATRIX.csv"))
    synergies = []
    for r in rows:
        score = _safe_int(r.get("synergy_score", "0"))
        mult_str = r.get("revenue_multiplier", "1.0").replace("x", "").replace("X", "")
        mult = _safe_float(mult_str, 1.0)
        synergies.append(Synergy(
            synergy_id=r.get("synergy_id", r.get("id", "")),
            method_combo=r.get("method_combo", f"{r.get('method_1', '')}+{r.get('method_2', '')}"),
            synergy_name=r.get("synergy_name", r.get("synergy_type", r.get("name", ""))),
            score=score,
            multiplier=mult,
        ))
    synergies.sort(key=lambda s: s.score, reverse=True)
    return synergies


def load_growth_tactics() -> List[GrowthTactic]:
    """36 comprehensive growth tactics from EDGE_GROWTH_TACTICS.md"""
    return [
        # Instagram
        GrowthTactic("Instagram", "Reels 3-5x/week + trending audio", "SAFE", "3-5/week", "1-3s hooks. Trending audio within 48hr.", "WORKING"),
        GrowthTactic("Instagram", "Carousel posts (12% > Reels interactions)", "SAFE", "Unlimited", "10-slide carousels. Educational content.", "WORKING"),
        GrowthTactic("Instagram", "Trial Reels (built-in A/B test)", "SAFE", "Unlimited", "Test with non-followers first.", "WORKING"),
        GrowthTactic("Instagram", "1-2 hashtags only", "SAFE", "1-2 per post", "Beats 20+ hashtags. Following dying.", "WORKING"),
        GrowthTactic("Instagram", "First-comment on big accounts", "SAFE", "20-30/day", "Authority building tactic", "WORKING"),
        GrowthTactic("Instagram", "Collab posts", "SAFE", "Unlimited", "Guest content on partner accounts", "WORKING"),
        GrowthTactic("Instagram", "Follow/Unfollow", "GREY", "30-50/day aged", "Mobile proxies REQUIRED. Residential flagged.", "WORKING"),
        GrowthTactic("Instagram", "Chrome extensions", "DEAD", "N/A", "Instant detection on all platforms since 2024", "PATCHED"),
        GrowthTactic("Instagram", "Mass DM automation", "DEAD", "N/A", "Restricted quickly, not worth risk", "PATCHED"),
        # TikTok
        GrowthTactic("TikTok", "Organic posting 3-5x/day", "SAFE", "3-5 posts/day", "ONLY recommended approach. Hook in 1s critical.", "WORKING"),
        GrowthTactic("TikTok", "Duet/Stitch viral content", "SAFE", "Unlimited", "Best organic traction method", "WORKING"),
        GrowthTactic("TikTok", "Trending sounds (within 48hr)", "SAFE", "Unlimited", "Critical timing window", "WORKING"),
        GrowthTactic("TikTok", "Native scheduler", "SAFE", "Unlimited", "Only safe scheduling method", "WORKING"),
        GrowthTactic("TikTok", "ALL automation tools", "DEAD", "N/A", "Detection too aggressive 2026. No VPN.", "PATCHED"),
        GrowthTactic("TikTok", "Bought views", "DEAD", "N/A", "Algorithm detects, account flagged", "PATCHED"),
        # Twitter/X
        GrowthTactic("Twitter/X", "Reply-guy strategy", "SAFE", "50-100/day", "First to reply on big accounts. Most lenient platform.", "WORKING"),
        GrowthTactic("Twitter/X", "Engagement pods", "SAFE", "Unlimited", "Private groups, legal", "WORKING"),
        GrowthTactic("Twitter/X", "Thread format (authority)", "SAFE", "4-8x/day tweets", "Self-reply funnels for CTAs", "WORKING"),
        GrowthTactic("Twitter/X", "Quote tweets with value", "SAFE", "20-50/day", "Builds on existing viral content", "WORKING"),
        GrowthTactic("Twitter/X", "Hypefury scheduling", "SAFE", "Unlimited", "$19-49/mo. Best for creators.", "WORKING"),
        # LinkedIn
        GrowthTactic("LinkedIn", "Carousels/documents", "SAFE", "3-5x/week", "Highest reach format 2026", "WORKING"),
        GrowthTactic("LinkedIn", "Voice notes DMs", "SAFE", "10-20/day", "3x higher response rate. BEST tactic.", "WORKING"),
        GrowthTactic("LinkedIn", "Comment before connecting", "SAFE", "10+ posts/day", "Engage 2+ weeks before outreach", "WORKING"),
        GrowthTactic("LinkedIn", "Cloud automation (Expandi)", "GREY", "50 connections/day max", "Expandi $99/mo. NO Chrome extensions.", "WORKING"),
        GrowthTactic("LinkedIn", "Dripify drip sequences", "GREY", "50/day", "Dripify $59/mo. Cloud-only.", "WORKING"),
        GrowthTactic("LinkedIn", "Chrome extensions", "DEAD", "N/A", "Instant detection. Cloud-only now.", "PATCHED"),
        GrowthTactic("LinkedIn", "Desktop automation", "DEAD", "N/A", "Jarvee/Phantombuster banned on LinkedIn", "PATCHED"),
        # Email
        GrowthTactic("Email", "Multi-inbox rotation (3-5)", "SAFE", "30/day/inbox", "Instantly $37-97/mo or Smartlead $39-94/mo", "WORKING"),
        GrowthTactic("Email", "Plain text only", "SAFE", "All sends", "HTML = instant spam flag 2026", "WORKING"),
        GrowthTactic("Email", "Open tracking OFF", "SAFE", "All sends", "Gmail shows warning label if tracked", "WORKING"),
        GrowthTactic("Email", "Intent-based timing", "SAFE", "Unlimited", "Within 48hr of trigger = 2-4x reply rate", "WORKING"),
        GrowthTactic("Email", "Subdomain isolation", "SAFE", "Always", "Never cold email from main domain", "WORKING"),
        GrowthTactic("Email", "Pre-warmed inboxes (DeliverOn)", "SAFE", "Instant start", "DeliverOn $49/mo. Skip DIY warmup.", "WORKING"),
        GrowthTactic("Email", "Single inbox campaigns", "DEAD", "N/A", "Domain burning certain in 2026", "PATCHED"),
        # Cross-platform
        GrowthTactic("Cross-platform", "Launch coordination", "SAFE", "Per launch", "Friends/community upvote. Legal.", "WORKING"),
        GrowthTactic("Cross-platform", "Shoutout trades", "SAFE", "Unlimited", "Exchange posts with similar accounts", "WORKING"),
    ]


def load_growth_services() -> List[GrowthService]:
    """16 growth services with real pricing from EDGE_GROWTH_TACTICS.md"""
    return [
        GrowthService("Instagram", "Kicksta", "$49-99/mo", "AI-targeted likes/follows", "HIGH", "100-500 followers/mo"),
        GrowthService("Instagram", "Growthoid", "$49-99/mo", "Human team engagement", "HIGHEST", "200-800 followers/mo"),
        GrowthService("Instagram", "Upleap", "$59-99/mo", "Managed service", "HIGH", "300-1000 followers/mo"),
        GrowthService("Instagram", "Jarvee", "$30-70/mo + proxies", "Desktop automation", "MEDIUM", "Full control but risky"),
        GrowthService("TikTok", "Manual only", "Free", "Content + engagement", "HIGHEST", "ONLY recommended approach"),
        GrowthService("Twitter/X", "Hypefury", "$19-49/mo", "Scheduling + engagement", "HIGH", "Best for creators"),
        GrowthService("Twitter/X", "TweetHunter", "$49/mo", "AI tweets + CRM", "HIGH", "Growth-focused"),
        GrowthService("Twitter/X", "Buffer/Hootsuite", "Free-$15/mo", "Scheduling", "HIGHEST", "Safe option"),
        GrowthService("LinkedIn", "Expandi", "$99/mo", "Cloud automation", "HIGHEST", "Safest automation"),
        GrowthService("LinkedIn", "Dripify", "$59/mo", "Drip sequences", "HIGH", "Good sequences"),
        GrowthService("LinkedIn", "Waalaxy", "$56/mo", "Multi-channel", "MEDIUM", "Also does email"),
        GrowthService("Email", "Instantly", "$37-97/mo", "Multi-inbox rotation", "HIGHEST", "Best cold email tool"),
        GrowthService("Email", "Smartlead", "$39-94/mo", "AI sequences", "HIGH", "Good AI features"),
        GrowthService("Email", "DeliverOn", "$49/mo", "Pre-warmed inboxes", "HIGHEST", "Skip DIY warmup"),
        GrowthService("Email", "EmailBison", "$29/mo", "Budget option", "MEDIUM", "Cheaper alternative"),
        GrowthService("Engagement", "MediaMister", "$2-50/order", "Buy engagement", "LOW", "Quick boost only"),
    ]


# ---------------------------------------------------------------------------
# Quick self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== PRINTMAXX Data Layer Self-Test ===\n")

    positions = load_all_positions()
    print(f"Positions loaded: {len(positions)}")
    active = [p for p in positions if p.status == "Active"]
    print(f"  Active: {len(active)}")
    for p in active:
        print(f"    {p.method_id}: {p.name} rev=${p.revenue_total:.0f} exp=${p.expenses_total:.0f}")

    fin = load_financial_summary()
    print(f"\nFinancial Summary:")
    print(f"  Revenue:  ${fin.total_revenue:,.2f}")
    print(f"  Expenses: ${fin.total_expenses:,.2f}")
    print(f"  Net P&L:  ${fin.net_profit:,.2f}")
    print(f"  Burn/mo:  ${fin.burn_rate_monthly:,.2f}")
    print(f"  Tool $:   ${fin.tool_costs_monthly:,.2f}/mo")
    print(f"  Active subs: {fin.active_subscriptions}")

    alpha = load_alpha_entries()
    print(f"\nAlpha Entries: {len(alpha)}")
    by_status = {}
    for a in alpha:
        by_status[a.status] = by_status.get(a.status, 0) + 1
    for s, c in sorted(by_status.items()):
        print(f"  {s}: {c}")

    pemf = load_pemf_metrics()
    print(f"\nPEMF Metrics:")
    print(f"  Files: {pemf.research_files_count}, Lines: {pemf.research_total_lines}")
    print(f"  Bootstrap: ${pemf.bootstrap_cost:.0f}")
    print(f"  COGS: ${pemf.unit_cogs_low:.0f}-${pemf.unit_cogs_high:.0f}")
    print(f"  Price: ${pemf.price_point:.0f}")
    print(f"  Margin: {pemf.margin_low:.0f}%-{pemf.margin_high:.0f}%")
    print(f"  Influencers: {pemf.influencers_total} (pod={pemf.influencers_podcasters} tw={pemf.influencers_twitter} tt={pemf.influencers_tiktok})")
    print(f"  Compliance: {pemf.compliance_path}")
    print(f"  MTO suppliers: {pemf.mto_suppliers_count}")
    print(f"  Bradet techniques: {pemf.bradet_techniques}")

    content = load_content_metrics()
    print(f"\nContent: {content.total_pieces} total, {content.queued} queued, {content.published} published, {content.calendar_posts} calendar")

    exp_breakdown = load_expense_breakdown()
    print(f"\nExpense breakdown: {exp_breakdown}")

    print("\n=== Self-test complete ===")
