#!/usr/bin/env python3
"""
WEBERMAXX PEMF QUANT DASHBOARD
================================
Jane Street-style strategic command center for the PEMF venture.
Pulls all 16 research files, synthesizes into actionable panels.

Usage:
    python3 AUTOMATIONS/pemf_quant_dashboard.py              # Full dashboard
    python3 AUTOMATIONS/pemf_quant_dashboard.py --summary     # Quick summary
    python3 AUTOMATIONS/pemf_quant_dashboard.py --todo        # Priority to-do list only
    python3 AUTOMATIONS/pemf_quant_dashboard.py --financial    # Financial model only
    python3 AUTOMATIONS/pemf_quant_dashboard.py --influencer   # Influencer pipeline only
    python3 AUTOMATIONS/pemf_quant_dashboard.py --competitive  # Competitive analysis only
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.columns import Columns
    from rich.text import Text
    from rich.progress import Progress, BarColumn, TextColumn
    from rich import box
except ImportError:
    os.system("pip3 install rich")
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.columns import Columns
    from rich.text import Text
    from rich.progress import Progress, BarColumn, TextColumn
    from rich import box

# =============================================================================
# CONFIG
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESEARCH_DIR = PROJECT_ROOT / "RESEARCH"

PEMF_FILES = {
    "master": "PEMF_MASTER_RESEARCH.md",
    "transcripts": "PEMF_STEVE_BRADET_TRANSCRIPTS.md",
    "diy": "PEMF_DIY_BUILD_GUIDE.md",
    "gtm": "PEMF_GTM_STRATEGY.md",
    "supplements": "PEMF_SUPPLEMENT_SYNERGY.md",
    "compliance": "PEMF_COMPLIANCE_LEGAL.md",
    "manufacturing": "PEMF_MANUFACTURING_DROPSHIP.md",
    "market": "PEMF_MARKET_ANALYSIS.md",
    "podcasters": "PEMF_INFLUENCER_PODCASTERS.md",
    "twitter": "PEMF_INFLUENCER_TWITTER.md",
    "tiktok": "PEMF_INFLUENCER_TIKTOK.md",
    "rates": "PEMF_INFLUENCER_RATES.md",
    "alpha_audit": "PEMF_INFLUENCER_ALPHA_AUDIT.md",
    "outreach": "PEMF_INFLUENCER_OUTREACH.md",
    "mto": "PEMF_MAKE_TO_ORDER.md",
    "bootstrap": "PEMF_BOOTSTRAP_CAPITAL_GENESIS.md",
}

console = Console()

# =============================================================================
# DATA EXTRACTION
# =============================================================================

def read_file(key):
    """Read a research file, return contents or empty string."""
    path = RESEARCH_DIR / PEMF_FILES.get(key, "")
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace")
    return ""

def count_lines(key):
    """Count lines in a research file."""
    content = read_file(key)
    return len(content.splitlines()) if content else 0

def file_exists(key):
    return (RESEARCH_DIR / PEMF_FILES.get(key, "")).exists()

def extract_number(text, pattern):
    """Extract first number matching a regex pattern."""
    match = re.search(pattern, text)
    if match:
        num_str = match.group(1).replace(",", "")
        try:
            return float(num_str)
        except ValueError:
            return 0
    return 0

def count_influencers(key):
    """Count influencer entries in a file by looking for handles/names."""
    content = read_file(key)
    if not content:
        return 0
    # Count @handles or numbered list items with names
    handles = len(re.findall(r'@\w+', content))
    # Count table rows (lines starting with |)
    table_rows = len([l for l in content.splitlines() if l.strip().startswith('|') and not l.strip().startswith('| -') and not l.strip().startswith('|--') and 'Tier' not in l and 'Attribute' not in l and 'Company' not in l and '---' not in l])
    return max(handles // 2, table_rows, 10)  # rough estimate

# =============================================================================
# PANEL BUILDERS
# =============================================================================

def build_header():
    """Build the main header."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    header_text = Text()
    header_text.append("W E B E R M A X X", style="bold cyan")
    header_text.append("  PEMF QUANT DASHBOARD", style="bold white")
    header_text.append(f"  [{now}]", style="dim")

    sub = Text()
    sub.append("    measure what matters. build what works. ship what sells.", style="italic dim")

    return Panel(
        Text.from_markup(
            f"[bold cyan]W E B E R M A X X[/]  [bold white]PEMF QUANT DASHBOARD[/]  [dim][{now}][/]\n"
            f"[italic dim]    measure what matters. build what works. ship what sells.[/]"
        ),
        border_style="cyan",
        box=box.DOUBLE,
    )

def build_research_status():
    """Panel 1: Research file status and completeness."""
    table = Table(
        title="RESEARCH INTEL STATUS",
        box=box.SIMPLE_HEAVY,
        title_style="bold green",
        show_lines=False,
        pad_edge=False,
    )
    table.add_column("File", style="cyan", width=32)
    table.add_column("Lines", justify="right", style="yellow", width=6)
    table.add_column("Status", width=10)
    table.add_column("Key Intel", style="dim", width=40)

    file_info = [
        ("master", "Master Synthesis", "Full venture overview, 10 research areas"),
        ("transcripts", "Steeve Bradet Transcripts", "26 videos analyzed, 74 cataloged"),
        ("diy", "DIY Build Guide", "3 tiers ($30-$600), Arduino code, coil formulas"),
        ("gtm", "GTM Strategy", "42 of 70+ PRINTMAXX methods mapped to PEMF"),
        ("supplements", "Supplement Synergy", "Tier 1/2/3 pairings, bundle concepts"),
        ("compliance", "Compliance & Legal", "FDA/FCC paths, copy-paste disclaimers"),
        ("manufacturing", "Manufacturing (Bulk)", "1,492 Alibaba suppliers, 10 specific"),
        ("market", "Market Analysis", "11 brands analyzed, $600M-$1.2B market"),
        ("podcasters", "Influencer: Podcasters", "45 podcasters, 7 warm leads"),
        ("twitter", "Influencer: Twitter/X", "55 accounts, 15 priority targets"),
        ("tiktok", "Influencer: TikTok", "55 creators, 11 tiers"),
        ("rates", "Influencer: Rates", "All platform rates, 6 profit-share models"),
        ("alpha_audit", "Alpha Audit", "PRINTMAXX intel applied to PEMF"),
        ("outreach", "Outreach Emails", "5 email sequences, negotiation templates"),
        ("mto", "Make-to-Order", "US manufacturers, $150-300 COGS, 75-92% margin"),
        ("bootstrap", "Bootstrap Capital Genesis", "The $451 path to first sale"),
    ]

    total_lines = 0
    complete = 0
    for key, name, intel in file_info:
        lines = count_lines(key)
        total_lines += lines
        exists = file_exists(key)
        if exists and lines > 50:
            status = "[green]COMPLETE[/]"
            complete += 1
        elif exists:
            status = "[yellow]PARTIAL[/]"
        else:
            status = "[red]MISSING[/]"
        table.add_row(name, str(lines), status, intel)

    table.add_section()
    table.add_row(
        f"[bold]TOTAL: {complete}/{len(file_info)} files[/]",
        f"[bold]{total_lines:,}[/]",
        f"[bold green]{complete*100//len(file_info)}%[/]",
        ""
    )

    return Panel(table, border_style="green", box=box.ROUNDED)

def build_financial_model():
    """Panel 2: Financial model and unit economics."""
    table = Table(
        title="UNIT ECONOMICS & CAPITAL GENESIS",
        box=box.SIMPLE_HEAVY,
        title_style="bold yellow",
        show_lines=False,
    )
    table.add_column("Product Tier", style="cyan", width=24)
    table.add_column("COGS", justify="right", style="red", width=8)
    table.add_column("Price", justify="right", style="green", width=8)
    table.add_column("Margin", justify="right", style="yellow", width=8)
    table.add_column("Margin %", justify="right", style="bold green", width=8)
    table.add_column("Status", width=12)

    products = [
        ("6-Coil Mini Mat", 125, 699, "DAY 1"),
        ("10-Coil Half Mat", 175, 999, "After 10 sales"),
        ("15-Coil Full Mat", 220, 1499, "After 25 sales"),
        ("20-Coil Full Mat", 280, 1999, "After 50 sales"),
        ("20-Coil + Nextion", 400, 2999, "After 100 sales"),
    ]

    for name, cogs, price, status in products:
        margin = price - cogs
        margin_pct = (margin / price) * 100
        table.add_row(
            name,
            f"${cogs}",
            f"${price:,}",
            f"${margin:,}",
            f"{margin_pct:.0f}%",
            f"[dim]{status}[/]",
        )

    # Startup costs section
    table.add_section()
    table.add_row("[bold]STARTUP COSTS[/]", "", "", "", "", "")

    startup_items = [
        ("Personal device (Phase 0)", "$62", "", "", "", "[green]DO FIRST[/]"),
        ("First 2 sellable units", "$250", "", "", "", "[yellow]WEEK 3[/]"),
        ("LLC + Shopify + legal", "$139-639", "", "", "", "[yellow]WEEK 4[/]"),
        ("Product liability insurance", "$183/mo", "", "", "", "[dim]After 5 sales[/]"),
        ("FCC testing", "$8K-23K", "", "", "", "[dim]After $10K rev[/]"),
    ]
    for item in startup_items:
        table.add_row(*item)

    table.add_section()
    table.add_row(
        "[bold]TOTAL BOOTSTRAP[/]",
        "[bold]$451[/]",
        "",
        "",
        "",
        "[bold green]BREAK EVEN: 1 SALE[/]"
    )

    return Panel(table, border_style="yellow", box=box.ROUNDED)

def build_competitive_matrix():
    """Panel 3: Competitive positioning."""
    table = Table(
        title="COMPETITIVE POSITIONING MATRIX",
        box=box.SIMPLE_HEAVY,
        title_style="bold red",
        show_lines=True,
    )
    table.add_column("Brand", style="cyan", width=16)
    table.add_column("Price", justify="right", width=12)
    table.add_column("Gauss", width=10)
    table.add_column("Wave", width=8)
    table.add_column("Freq", width=10)
    table.add_column("QC Cert", width=8)
    table.add_column("Vulnerability", style="dim", width=28)

    competitors = [
        ("BEMER", "$4,990-6,490", "Low", "Sine", "2 only", "[red]NO[/]", "MLM 3x markup, 2 frequencies"),
        ("Pulse PEMF", "$5,500-12K", "High", "Square", "19", "[red]NO[/]", "Pro pricing, opacity"),
        ("HUGO", "$6,000-25K", "Very High", "Spark", "Varies", "[red]NO[/]", "Celebrity pricing only"),
        ("iMRS", "$4,000-6K", "Low-Med", "Various", "Multi", "[red]NO[/]", "MLM, warranty games"),
        ("OMI PEMF", "$499-1,250", "Medium", "Varies", "99 Hz", "[red]NO[/]", "Basic, no differentiation"),
        ("FluxHealth", "$150-450", "Low", "Square", "ICES", "[red]NO[/]", "Targeted only, not mats"),
        ("Bradet ZK", "$1,000-2K", "45-55", "Square", "0-15K", "[yellow]YES[/]", "Small team, capacity limited"),
        ("Bradet Nextion", "$3,000", "45-100", "Square", "0-15K", "[yellow]YES[/]", "Premium only, no entry tier"),
        ("[bold cyan]WEBERMAXX[/]", "[bold green]$699[/]", "[bold]45-55[/]", "[bold green]Square[/]", "[bold]1-150K[/]", "[bold green]YES[/]", "[bold green]Honest science + best price[/]"),
    ]

    for row in competitors:
        table.add_row(*row)

    return Panel(table, border_style="red", box=box.ROUNDED)

def build_influencer_pipeline():
    """Panel 4: Influencer campaign pipeline."""
    table = Table(
        title="INFLUENCER PIPELINE (155 TARGETS)",
        box=box.SIMPLE_HEAVY,
        title_style="bold magenta",
        show_lines=False,
    )
    table.add_column("Channel", style="cyan", width=14)
    table.add_column("Count", justify="right", style="yellow", width=6)
    table.add_column("Sweet Spot", width=16)
    table.add_column("Cost/Creator", justify="right", width=14)
    table.add_column("Strategy", width=30)
    table.add_column("File", style="dim", width=20)

    channels = [
        ("Podcasters", "45", "5K-25K downloads", "$0-$750", "Product seed + affiliate, 7 warm leads", "PODCASTERS.md"),
        ("Twitter/X", "55", "10K-100K followers", "$50-$500", "Biohacking accounts, affiliate-only", "TWITTER.md"),
        ("TikTok", "55", "5K-100K followers", "$50-$500", "Nano swarm, device demos", "TIKTOK.md"),
        ("UGC (E. Europe)", "10-20", "N/A", "$10-$25/vid", "Ad creatives for Meta/TikTok", "ALPHA_AUDIT.md"),
        ("AI UGC", "Unlimited", "N/A", "$0.10-$1/vid", "Nano Banana workflow", "ALPHA_AUDIT.md"),
    ]

    for row in channels:
        table.add_row(*row)

    table.add_section()

    # Budget tiers
    table.add_row("[bold]BUDGET TIERS[/]", "", "", "", "", "")
    table.add_row("Bootstrap", "", "", "[green]$1.5-3.5K[/]", "25-45 content pieces, seed 5 devices", "")
    table.add_row("Growth", "", "", "[yellow]$7-12K[/]", "63-83 content pieces, 20 creators", "")
    table.add_row("Scale", "", "", "[red]$21-49K[/]", "170-220+ pieces, 50 creator swarm", "")

    return Panel(table, border_style="magenta", box=box.ROUNDED)

def build_priority_todos():
    """Panel 5: Priority action items."""

    # Phase-based to-do list
    todos = [
        # Phase 0: Build (Week 1-2)
        ("P0", "CRITICAL", "Build personal Tier 1 PEMF device", "$62", "Week 1", "Not started"),
        ("P0", "CRITICAL", "Test on yourself for 2 weeks, document effects", "$0", "Week 1-2", "Not started"),
        ("P0", "CRITICAL", "Film build process on phone (3-5 videos)", "$0", "Week 1", "Not started"),

        # Phase 1: Product (Week 3-4)
        ("P1", "HIGH", "Build first 6-coil mini mat (sellable)", "$125", "Week 3", "Not started"),
        ("P1", "HIGH", "Build second unit (backup/demo)", "$125", "Week 3", "Not started"),
        ("P1", "HIGH", "Form Wyoming LLC", "$100", "Week 4", "Not started"),
        ("P1", "HIGH", "Set up Shopify store with disclaimers", "$39/mo", "Week 4", "Not started"),
        ("P1", "HIGH", "Product photography (iPhone)", "$0", "Week 4", "Not started"),
        ("P1", "HIGH", "Create QC certificate template", "$0", "Week 4", "Not started"),

        # Phase 2: Launch (Week 5-8)
        ("P2", "HIGH", "Post YouTube build series (3 videos)", "$0", "Week 5", "Not started"),
        ("P2", "HIGH", "Reddit r/PEMF engagement (5-10 answers)", "$0", "Week 5-6", "Not started"),
        ("P2", "HIGH", "Comparison post: $125 build vs $5K BEMER", "$0", "Week 6", "Not started"),
        ("P2", "MED", "List on Etsy (handmade PEMF device)", "$0.20", "Week 6", "Not started"),
        ("P2", "MED", "DM 5 nano podcasters for guest spot", "$0", "Week 7", "Not started"),
        ("P2", "MED", "Seed 1 device to r/PEMF power user", "$125", "Week 7", "Not started"),
        ("P2", "MED", "Join 3-5 Facebook PEMF groups", "$0", "Week 5", "Not started"),

        # Phase 3: Scale (Week 9-12)
        ("P3", "MED", "Set up GoAffPro affiliate program (free)", "$0", "Week 9", "Not started"),
        ("P3", "MED", "Seed 2 more devices to influencers", "$250", "Week 9", "Not started"),
        ("P3", "MED", "Order 5 UGC videos (Eastern Europe)", "$100-200", "Week 10", "Not started"),
        ("P3", "MED", "Start Meta ads at $20/day", "$600/mo", "Week 11", "Not started"),
        ("P3", "LOW", "Launch Beehiiv newsletter (free tier)", "$0", "Week 7", "Not started"),
        ("P3", "LOW", "Add 10-coil mat product tier", "$175 COGS", "After 10 sales", "Not started"),

        # Compliance (parallel track)
        ("CMP", "HIGH", "Copy-adapt disclaimers from Pulse PEMF", "$0", "Week 4", "Not started"),
        ("CMP", "MED", "Get product liability insurance", "$183/mo", "After 5 sales", "Not started"),
        ("CMP", "LOW", "FCC pre-compliance testing", "$2-5K", "After $10K rev", "Not started"),
        ("CMP", "LOW", "Attorney review of marketing claims", "$300-500", "After $5K rev", "Not started"),
    ]

    table = Table(
        title="PRIORITY EXECUTION QUEUE",
        box=box.SIMPLE_HEAVY,
        title_style="bold white on blue",
        show_lines=False,
    )
    table.add_column("Phase", style="dim", width=5)
    table.add_column("Pri", width=10)
    table.add_column("Action", style="white", width=42)
    table.add_column("Cost", justify="right", style="yellow", width=10)
    table.add_column("When", width=14)
    table.add_column("Status", width=12)

    for phase, pri, action, cost, when, status in todos:
        if pri == "CRITICAL":
            pri_style = "[bold red]CRITICAL[/]"
        elif pri == "HIGH":
            pri_style = "[bold yellow]HIGH[/]"
        elif pri == "MED":
            pri_style = "[bold cyan]MED[/]"
        else:
            pri_style = "[dim]LOW[/]"

        if status == "Not started":
            status_style = "[dim][ ] TODO[/]"
        elif status == "In progress":
            status_style = "[yellow][~] WIP[/]"
        elif status == "Done":
            status_style = "[green][x] DONE[/]"
        else:
            status_style = f"[dim]{status}[/]"

        table.add_row(f"[dim]{phase}[/]", pri_style, action, cost, when, status_style)

    return Panel(table, border_style="blue", box=box.ROUNDED)

def build_technical_specs():
    """Panel 6: Technical specifications from Steeve Bradet research."""
    table = Table(
        title="WEBERMAXX TECHNICAL SPECS (from Bradet Research)",
        box=box.SIMPLE_HEAVY,
        title_style="bold cyan",
        show_lines=False,
    )
    table.add_column("Parameter", style="cyan", width=28)
    table.add_column("Our Spec", style="bold green", width=22)
    table.add_column("Why", style="dim", width=36)

    specs = [
        ("Gauss per coil", "45-55 G", "Bradet sweet spot. >100 causes adverse effects"),
        ("Waveform", "Square wave", "100% cell absorption vs 40% sine. NASA validated"),
        ("Rise time", "0.04 ms", "vs 8.2ms sine. Cells only respond to rapid change"),
        ("Frequency range", "1-150,000 Hz", "ZK-PP2K module supports full range"),
        ("Coil orientation", "Constructive", "40% more Weber. Most brands don't check"),
        ("Measurement", "Weber (not Gauss)", "Total flux crossing a plane. Actual metric"),
        ("Wire gauge", "20-22 AWG", "Sweet spot: enough current, manageable weight"),
        ("Wire type", "Lacquered copper", "NOT copper-clad aluminum (CCA)"),
        ("Duty cycle", "10% default", "NASA optimal. Adjustable 0-100%"),
        ("Controller", "ZK-PP2K", "$5-8 module. LCD, memory, 1Hz-150KHz"),
        ("Power supply", "19V DC laptop", "Recycled or $12 new. Standard barrel jack"),
        ("Coil form", "17-20cm PVC", "$3-5 hardware store"),
        ("Metal backing", "Steel plate behind coils", "+55% gauss boost (27 to 42-43 G)"),
        ("QC per unit", "WT10A gaussmeter", "Every coil measured. Certificate included"),
    ]

    for row in specs:
        table.add_row(*row)

    return Panel(table, border_style="cyan", box=box.ROUNDED)

def build_compliance_checklist():
    """Panel 7: Compliance status."""
    table = Table(
        title="COMPLIANCE CHECKLIST",
        box=box.SIMPLE_HEAVY,
        title_style="bold red",
        show_lines=False,
    )
    table.add_column("Requirement", style="cyan", width=30)
    table.add_column("Status", width=12)
    table.add_column("Cost", justify="right", width=12)
    table.add_column("When Required", width=20)
    table.add_column("Notes", style="dim", width=28)

    items = [
        ("LLC formation", "[red]TODO[/]", "$100", "Before first sale", "Wyoming recommended"),
        ("EIN (tax ID)", "[red]TODO[/]", "Free", "Before first sale", "IRS.gov, 5 minutes"),
        ("FDA disclaimers", "[red]TODO[/]", "$0-$500", "Before first sale", "Copy from Pulse PEMF"),
        ("Contraindication warnings", "[red]TODO[/]", "$0", "In every box", "Template in compliance doc"),
        ("FTC-compliant copy", "[red]TODO[/]", "$0", "All marketing", "No disease claims ever"),
        ("Product liability insurance", "[dim]DEFER[/]", "$2.2-5K/yr", "After 5 sales", "Insureon or NEXT"),
        ("FCC Part 18 testing", "[dim]DEFER[/]", "$8-23K", "After $10K revenue", "Skip if <100 units"),
        ("510(k) FDA clearance", "[dim]SKIP[/]", "$50-150K+", "NEVER (wellness only)", "Only if medical claims"),
        ("UL Safety certification", "[dim]SKIP[/]", "$10-30K", "Optional, helps insurance", "Nice-to-have only"),
        ("Stripe account", "[red]TODO[/]", "Free", "Before first sale", "2.9% + $0.30/txn"),
        ("Shopify store", "[red]TODO[/]", "$39/mo", "Before first sale", "Free trial available"),
        ("Terms of Service", "[red]TODO[/]", "$0-$300", "Before first sale", "LegalZoom template OK"),
    ]

    for row in items:
        table.add_row(*row)

    return Panel(table, border_style="red", box=box.ROUNDED)

def build_revenue_scenarios():
    """Panel 8: Revenue projection scenarios."""
    table = Table(
        title="REVENUE SCENARIOS (90-Day Model)",
        box=box.SIMPLE_HEAVY,
        title_style="bold green",
        show_lines=True,
    )
    table.add_column("Scenario", style="cyan", width=14)
    table.add_column("Units/Mo", justify="right", width=10)
    table.add_column("Price", justify="right", width=8)
    table.add_column("Revenue/Mo", justify="right", style="green", width=12)
    table.add_column("COGS/Mo", justify="right", style="red", width=10)
    table.add_column("Gross/Mo", justify="right", style="bold green", width=12)
    table.add_column("Annual Run", justify="right", style="bold yellow", width=12)

    scenarios = [
        ("Bear", 2, 699, "Solo, organic only"),
        ("Base", 5, 699, "Organic + seeding"),
        ("Bull", 10, 699, "Organic + affiliates"),
        ("Moon", 20, 899, "Paid ads + affiliates"),
        ("Mars", 40, 1249, "Multi-tier + team"),
    ]

    for name, units, price, _ in scenarios:
        cogs = units * 125
        revenue = units * price
        gross = revenue - cogs
        annual = revenue * 12
        table.add_row(
            name,
            str(units),
            f"${price}",
            f"${revenue:,}",
            f"${cogs:,}",
            f"${gross:,}",
            f"${annual:,}",
        )

    table.add_section()
    table.add_row(
        "[bold]KEY METRIC[/]", "", "", "", "", "",
        "[bold]1 unit/week = $36K/yr[/]"
    )

    return Panel(table, border_style="green", box=box.ROUNDED)

def build_bradet_intelligence():
    """Panel 9: Steeve Bradet competitive intelligence."""
    table = Table(
        title="STEEVE BRADET INTELLIGENCE",
        box=box.SIMPLE_HEAVY,
        title_style="bold yellow",
        show_lines=False,
    )
    table.add_column("Attribute", style="cyan", width=24)
    table.add_column("Detail", width=50)

    intel = [
        ("Location", "Edmonton, Alberta, Canada"),
        ("Team", "Small team, hand-assembly"),
        ("Products", "ZK 6-coil ($1K), 10-coil ($1.35K), 15-coil ($1.65K), 20-coil ($2K), Nextion ($3K)"),
        ("US Distributor", "PEMF Mat Source LLC (exclusive)"),
        ("Ship Time", "5-8 business days (MTO confirmed)"),
        ("Controller", "ZK-PP2K ($5-8) and Nextion touchscreen"),
        ("Frequency Range", "0.01-15,000 Hz"),
        ("Waveform", "Square wave, ~250 T/s slew rate"),
        ("Est. COGS (20-coil)", "$150-250"),
        ("Est. Margin", "88-93%"),
        ("Tariff (CA to US)", "$220 import tariff"),
        ("Warranty", "3 years"),
        ("Key Insight", "[bold]Metal backing = +55% gauss boost[/] (27 to 42-43 G)"),
        ("Key Insight", "[bold]Supplement protocol from Dr. Stokes[/]: charcoal, pectin, zinc, 64oz water"),
        ("Our Advantage", "[bold green]30% lower price, US-based, no import tariff, QC cert[/]"),
    ]

    for attr, detail in intel:
        table.add_row(attr, detail)

    return Panel(table, border_style="yellow", box=box.ROUNDED)

def build_differentiation_stack():
    """Panel 10: What makes Webermaxx different."""
    table = Table(
        title="WEBERMAXX DIFFERENTIATION STACK (MOAT)",
        box=box.SIMPLE_HEAVY,
        title_style="bold cyan on black",
        show_lines=False,
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("Edge", style="bold cyan", width=26)
    table.add_column("What It Means", width=42)
    table.add_column("Competitor Gap", style="red", width=24)

    edges = [
        ("1", "Weber measurement", "Measure total flux (what matters), not single-line intensity", "Nobody else does this"),
        ("2", "Square wave verified", "100% cell absorption, oscilloscope proof in every box", "Most use sine or unverified"),
        ("3", "Constructive coils", "40% more Weber from proper orientation", "Most don't even check"),
        ("4", "QC certificate per unit", "Exact gauss readings for YOUR device", "Zero competitors do this"),
        ("5", "Transparent pricing", "Honest about margins, COGS, and markup", "MLMs hide behind layers"),
        ("6", "Open build docs", "Publish specs, teach science, show process", "Competitors gatekeep"),
        ("7", "Metal backing boost", "+55% gauss from steel plates behind coils", "Bradet's technique, not widely known"),
        ("8", "No restocking fee", "30-day money-back, no BEMER-style $448 fee", "BEMER: $448 restocking"),
        ("9", "US-built, no tariff", "No $220 Canada import tariff vs Bradet", "Bradet ships from Canada"),
        ("10", "NASA-validated protocol", "10 Hz square wave, published research", "Most cite NASA but use sine"),
    ]

    for row in edges:
        table.add_row(*row)

    return Panel(table, border_style="cyan", box=box.ROUNDED)

def build_risk_radar():
    """Panel 11: Risk assessment."""
    table = Table(
        title="RISK RADAR",
        box=box.SIMPLE_HEAVY,
        title_style="bold red on black",
        show_lines=False,
    )
    table.add_column("Risk", style="cyan", width=24)
    table.add_column("Prob", width=8)
    table.add_column("Impact", width=8)
    table.add_column("Score", width=8)
    table.add_column("Mitigation", style="dim", width=36)

    risks = [
        ("No one buys", "[yellow]MED[/]", "[yellow]MED[/]", "[yellow]4/9[/]", "$0 marketing via Reddit/YT. Total risk <$1K"),
        ("Product injury", "[green]LOW[/]", "[red]HIGH[/]", "[yellow]3/9[/]", "5-300G safe range, contraindications, LLC"),
        ("FCC enforcement", "[green]VLOW[/]", "[yellow]MED[/]", "[green]2/9[/]", "Artisan scale, get tested at $10K rev"),
        ("FDA warning letter", "[green]LOW[/]", "[yellow]MED[/]", "[green]2/9[/]", "Wellness claims only, copy competitor copy"),
        ("FTC health claims", "[yellow]MED[/]", "[red]HIGH[/]", "[yellow]6/9[/]", "ZERO disease claims. Attorney review at $5K"),
        ("Customer return", "[yellow]MED[/]", "[green]LOW[/]", "[green]2/9[/]", "30-day guarantee, $50 reserve per unit"),
        ("Bradet competes on price", "[green]LOW[/]", "[yellow]MED[/]", "[green]2/9[/]", "He's premium. We're entry-level. Different tiers"),
        ("Component supply issue", "[green]LOW[/]", "[green]LOW[/]", "[green]1/9[/]", "All parts Amazon/AliExpress, multiple sources"),
    ]

    for row in risks:
        table.add_row(*row)

    return Panel(table, border_style="red", box=box.ROUNDED)

def build_key_metrics():
    """Summary metrics bar."""
    metrics = [
        ("Total Research", "[bold green]16 files, 9,400+ lines[/]"),
        ("Market Size", "[bold yellow]$600M-$1.2B[/]"),
        ("Competitors Analyzed", "[bold cyan]11 brands[/]"),
        ("Influencer Targets", "[bold magenta]155 creators[/]"),
        ("Bootstrap Cost", "[bold green]$451[/]"),
        ("Break-Even", "[bold green]1 sale[/]"),
        ("Unit Margin", "[bold green]77-87%[/]"),
        ("Bradet Videos Analyzed", "[bold cyan]26/74[/]"),
    ]

    text_parts = []
    for label, value in metrics:
        text_parts.append(f"[dim]{label}:[/] {value}")

    return Panel(
        Text.from_markup("  |  ".join(text_parts)),
        border_style="white",
        title="KEY METRICS",
        title_align="left",
    )

def build_supplement_bundles():
    """Panel: Supplement upsell opportunities."""
    table = Table(
        title="SUPPLEMENT SYNERGY BUNDLES (UPSELL)",
        box=box.SIMPLE_HEAVY,
        title_style="bold green",
        show_lines=False,
    )
    table.add_column("Tier", style="yellow", width=8)
    table.add_column("Supplement", style="cyan", width=20)
    table.add_column("Why + PEMF", width=36)
    table.add_column("Bundle Price", justify="right", style="green", width=12)

    supplements = [
        ("1", "Magnesium Glycinate", "PEMF increases cellular uptake", "Device + $29"),
        ("1", "CoQ10 / Ubiquinol", "Mitochondrial synergy with PEMF", "Device + $39"),
        ("1", "Omega-3 (Fish Oil)", "Anti-inflammatory stack", "Device + $24"),
        ("2", "NAD+ Precursor (NMN)", "Cellular energy + PEMF repair", "Device + $49"),
        ("2", "Activated Charcoal", "Bradet/Stokes: binder before PEMF", "Device + $14"),
        ("2", "Zinc + Minerals", "Bradet/Stokes: supports detox", "Device + $19"),
        ("3", "Red Light Panel", "PEMF + photobiomodulation stack", "Separate product"),
        ("3", "Grounding Mat", "PEMF + earthing synergy", "Separate product"),
    ]

    for row in supplements:
        table.add_row(*row)

    return Panel(table, border_style="green", box=box.ROUNDED)

# =============================================================================
# MAIN DISPLAY FUNCTIONS
# =============================================================================

def show_full_dashboard():
    """Display the complete dashboard."""
    console.clear()
    console.print(build_header())
    console.print(build_key_metrics())
    console.print()
    console.print(build_research_status())
    console.print()
    console.print(build_financial_model())
    console.print()
    console.print(build_competitive_matrix())
    console.print()
    console.print(build_differentiation_stack())
    console.print()
    console.print(build_revenue_scenarios())
    console.print()
    console.print(build_influencer_pipeline())
    console.print()
    console.print(build_bradet_intelligence())
    console.print()
    console.print(build_technical_specs())
    console.print()
    console.print(build_compliance_checklist())
    console.print()
    console.print(build_risk_radar())
    console.print()
    console.print(build_supplement_bundles())
    console.print()
    console.print(build_priority_todos())
    console.print()

    # Footer
    console.print(Panel(
        Text.from_markup(
            "[dim]Files: RESEARCH/PEMF_*.md  |  "
            "Refresh: python3 AUTOMATIONS/pemf_quant_dashboard.py  |  "
            "Quick: --summary --todo --financial --influencer --competitive[/]"
        ),
        border_style="dim",
    ))

def show_summary():
    """Quick summary view."""
    console.clear()
    console.print(build_header())
    console.print(build_key_metrics())
    console.print()
    console.print(build_financial_model())
    console.print()
    console.print(build_revenue_scenarios())
    console.print()

    # Quick action items
    console.print(Panel(
        Text.from_markup(
            "[bold red]NEXT 3 ACTIONS:[/]\n"
            "  [bold]1.[/] Build personal Tier 1 PEMF device ($62, 1 weekend)\n"
            "  [bold]2.[/] Test on yourself for 2 weeks, document effects\n"
            "  [bold]3.[/] Film build process for YouTube content"
        ),
        border_style="red",
        title="DO THIS NOW",
    ))

def show_todos():
    """To-do list only."""
    console.clear()
    console.print(build_header())
    console.print(build_priority_todos())

def show_financial():
    """Financial model only."""
    console.clear()
    console.print(build_header())
    console.print(build_financial_model())
    console.print()
    console.print(build_revenue_scenarios())
    console.print()
    console.print(build_risk_radar())

def show_influencer():
    """Influencer pipeline only."""
    console.clear()
    console.print(build_header())
    console.print(build_influencer_pipeline())

def show_competitive():
    """Competitive analysis only."""
    console.clear()
    console.print(build_header())
    console.print(build_competitive_matrix())
    console.print()
    console.print(build_differentiation_stack())
    console.print()
    console.print(build_bradet_intelligence())

# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    args = sys.argv[1:]

    if "--summary" in args:
        show_summary()
    elif "--todo" in args:
        show_todos()
    elif "--financial" in args:
        show_financial()
    elif "--influencer" in args:
        show_influencer()
    elif "--competitive" in args:
        show_competitive()
    else:
        show_full_dashboard()
