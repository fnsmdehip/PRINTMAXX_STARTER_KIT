#!/usr/bin/env python3
"""
GROWTH STRATEGIST — Creates Detailed Growth Strategies Per Venture From Intelligence
=====================================================================================

Usage:
    python3 growth_strategist.py                    # Full strategy report (all ventures)
    python3 growth_strategist.py --venture CONTENT  # Single venture strategy
    python3 growth_strategist.py --edge             # Grey growth edge tactics only
    python3 growth_strategist.py --json             # Structured output for agents
"""
from __future__ import annotations
import argparse, csv, json, subprocess, sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

try:
    from master_ops_bridge import MasterOpsBridge
    _BRIDGE_AVAILABLE = True
except ImportError:
    _BRIDGE_AVAILABLE = False

PROJECT = Path(__file__).resolve().parent.parent
AUTO = PROJECT / "AUTOMATIONS"
REPORTS = AUTO / "agent" / "swarm" / "reports"
GROWTH_DIRS = [PROJECT / "CONTENT" / "growth" / "buildout" / "G01_G15_growth",
               PROJECT / "CONTENT" / "growth" / "buildout" / "N_series",
               PROJECT / "06_OPERATIONS" / "growth"]
INTEL_CAT = PROJECT / "OPS" / "INTELLIGENCE_CATALOG.json"
MKT_CSV = PROJECT / "LEDGER" / "MARKETING_CHANNELS_MASTER.csv"

VENTURES = ["CONTENT", "OUTBOUND", "APP_FACTORY", "LOCAL_BIZ",
            "MONETIZATION", "PRODUCT", "RESEARCH", "SCRAPING"]

VCTX = {
    "CONTENT":      ("Content creation, distribution, engagement farming", ["Twitter/X","TikTok","LinkedIn","Reddit","Newsletter","YouTube"], ["Impressions","Engagement rate","Follower growth","Link clicks","DMs received"]),
    "OUTBOUND":     ("Cold email, cold DM, lead gen, prospecting", ["Email","LinkedIn","Twitter DMs","Cold calling"], ["Emails sent","Reply rate","Meeting booked rate","Close rate","Revenue/lead"]),
    "APP_FACTORY":  ("PWA/app discovery, ASO, downloads, retention", ["App Store","Play Store","Product Hunt","HackerNews","AlternativeTo"], ["Downloads","DAU/MAU","Retention D1/D7/D30","Revenue/user","ASO rank"]),
    "LOCAL_BIZ":    ("Local business client acquisition, web design, local SEO", ["Google Business","Local SEO","Cold email","LinkedIn","Local forums"], ["Demos built","Outreach sent","Meetings booked","Clients closed","MRR"]),
    "MONETIZATION": ("Revenue channels, pricing, funnels, checkout, affiliate", ["Gumroad","Stripe","Etsy","Fiverr","Whop","Affiliate networks"], ["Revenue","Conversion rate","AOV","LTV","Churn rate"]),
    "PRODUCT":      ("Digital product creation, listing, pricing, sales", ["Gumroad","Etsy","Notion marketplace","Lemon Squeezy","Direct sales"], ["Products listed","Sales","Revenue","Reviews","Refund rate"]),
    "RESEARCH":     ("Intelligence gathering, tool discovery, alpha scanning", ["Twitter","Reddit","HackerNews","GitHub","Product Hunt"], ["Alpha entries found","Actionable insights","Tools discovered","Trends identified"]),
    "SCRAPING":     ("Data extraction, competitor monitoring, signal detection", ["Web scrapers","API monitors","RSS feeds","Alert systems"], ["Sources monitored","Data freshness","Signal quality","Action rate"]),
}

EDGE_DOCS = ["grey_hat_legal.md", "EDGE_GROWTH_TACTICS.md", "GREY_HAT_UPDATE_JAN_2026.md", "multi_account_warmup.md"]
PLAT_DOCS = {"Twitter/X": ["TWITTER_META_JANUARY_2026.md","reply_guy_strategy.md","NICHE_POSTING_STRATEGY.md"],
             "TikTok": ["PLATFORM_UPDATES_JAN_2026.md","clipper_army_sop.md"],
             "LinkedIn": ["linkedin_automation.md","DM_FUNNEL_PLAYBOOK.md"],
             "Reddit": ["medium_substack_strategy.md"], "Product Hunt": ["product_hunt_playbook.md"],
             "GitHub": ["github_trending.md"]}
DIST_DOCS = ["cross_pollination_playbook.md", "swarm_promotion.md", "build_in_public.md"]
ENG_DOCS = ["ENGAGEMENT_FARMING_TACTICS.md", "reply_guy_strategy.md", "platform_algorithm_notes.md"]

EDGE_DEFAULTS = ["Multi-account warmup (21-30 day ramp)", "Reply guy strategy (500-2000 followers/month at $0)",
                 "Clipper army SOP (10x distribution via secondary accounts)",
                 "Engagement farming (1 reply = 4x value of a like)", "Swarm promotion (4-layer coordinated launch)"]

def safe_path(t: Path) -> Path:
    r = Path(t).resolve()
    if not str(r).startswith(str(PROJECT.resolve())): raise ValueError(f"BLOCKED: {r}")
    return r

def ts() -> str: return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def log(m: str) -> None: print(f"[{ts()}] [GROWTH_STRATEGIST] {m}")

def _run_json(script: str, args: list[str]) -> list | dict:
    cmd = [sys.executable, str(AUTO / script)] + args + ["--json"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=str(PROJECT))
        if r.returncode == 0 and r.stdout.strip(): return json.loads(r.stdout)
    except Exception: pass
    return [] if "alpha" in script else {}

def read_growth_docs() -> dict[str, list[str]]:
    docs = {}
    for d in GROWTH_DIRS:
        if not d.exists(): continue
        for f in d.glob("*.md"):
            try: docs[f.name] = f.read_text(encoding="utf-8", errors="replace").split("\n")[:80]
            except Exception: pass
    return docs

def read_json_file(path: Path) -> dict:
    if not path.exists(): return {}
    try: return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception: return {}

def read_csv_rows(path: Path) -> list[dict]:
    if not path.exists(): return []
    try:
        with open(path, newline="", encoding="utf-8", errors="replace") as f:
            return list(csv.DictReader(f))
    except Exception: return []

def read_swarm_reports() -> list[str]:
    if not REPORTS.exists(): return []
    out = []
    for r in sorted(REPORTS.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)[:10]:
        try: out.append(f"--- {r.name} ---\n" + "\n".join(r.read_text(errors="replace").split("\n")[:15]))
        except Exception: pass
    return out

def _extract_actions(lines: list[str], n: int = 5) -> list[str]:
    return [ln.strip() for ln in lines if ln.strip() and
            (ln.strip()[0] in "-*" or (ln.strip()[:1].isdigit() and "." in ln.strip()[:4]))][:n]

def _section(title: str, items: list[str]) -> list[str]:
    out = [f"### {title}"]
    for i in items: out.append(f"   {i}")
    out.append("")
    return out

def _get_synergy_context(venture_type: str) -> str:
    """Get synergy and tool recommendations from Master Ops."""
    if not _BRIDGE_AVAILABLE:
        return ""
    try:
        bridge = MasterOpsBridge()
        sections = []

        # Synergy stacks
        ops = bridge.get_ops_by_category(venture_type)
        op_ids = {o.get("OP_ID") for o in ops}
        synergies = [s for s in bridge.get_synergy_stacks()
                     if any(oid in s.get("METHODS_COMBINED", "") for oid in op_ids)]

        if synergies:
            sections.append("SYNERGY OPPORTUNITIES:")
            for s in synergies[:5]:
                sections.append(f"  - {s.get('NAME')}: score {s.get('SYNERGY_SCORE')}, {s.get('REVENUE_MULTIPLIER')}x multiplier")
                sections.append(f"    Methods: {s.get('METHODS_COMBINED')}")
                sections.append(f"    {s.get('DESCRIPTION', '')[:100]}")

        # Tool recommendations
        tools = bridge.get_all_tool_stacks()
        if venture_type.upper() in ("CONTENT", "MEDIA"):
            relevant_tools = tools.get("video", [])
            if relevant_tools:
                sections.append("\nRECOMMENDED TOOLS (VIDEO/MEDIA):")
                for t in relevant_tools[:5]:
                    sections.append(f"  - {t.get('TOOL')}: {t.get('FREE_TIER', 'N/A')} free | Quality: {t.get('QUALITY', '?')}")
        elif venture_type.upper() in ("OUTBOUND", "LOCAL_BIZ", "SERVICE"):
            relevant_tools = tools.get("lead_gen", [])
            if relevant_tools:
                sections.append("\nRECOMMENDED TOOLS (LEAD GEN):")
                for t in relevant_tools[:5]:
                    sections.append(f"  - {t.get('TOOL')}: {t.get('FREE_TIER', 'N/A')} free | Automation: {t.get('AUTOMATION_LEVEL', '?')}")

        # Alpha thesis edge durations
        theses = bridge.get_alpha_by_lane(venture_type.lower())
        if theses:
            sections.append("\nALPHA EDGE ANALYSIS:")
            for t in theses[:3]:
                sections.append(f"  - {t.get('OPPORTUNITY')}")
                sections.append(f"    Edge duration: {t.get('EDGE_DURATION')} | {t.get('WHY_LLM_EDGE', '')[:80]}")

        return "\n".join(sections)
    except Exception:
        return ""


def gen_venture(venture: str, intel: dict, alpha: list, gdocs: dict,
                channels: list, edge_only: bool = False) -> str:
    focus, platforms, kpis = VCTX.get(venture, ("", [], []))
    L = [f"## {venture}", f"**Focus:** {focus}", f"**Platforms:** {', '.join(platforms)}", ""]

    if not edge_only:
        L.append("### Top 3 Growth Tactics From Intelligence")
        for i, e in enumerate(alpha[:3], 1):
            L.append(f"**{i}. [{e.get('alpha_id','?')}] (ROI: {e.get('roi_potential','?')})**")
            L.append(f"   {(e.get('tactic') or '')[:200]}")
            m = (e.get("extracted_method") or "")[:150]
            if m: L.append(f"   Method: {m}")
            L.append("")
        if not alpha: L += ["   No alpha entries found.", ""]
        if intel:
            L.append("### Intelligence Summary")
            if intel.get("brief"): L.append(intel["brief"][:500])
            L.append(f"   Sources: {len(intel.get('alpha',[]))} alpha, {len(intel.get('docs',[]))} docs, {len(intel.get('tactics',[]))} tactics")
            L.append("")

    # Grey edge tactics
    L += ["### Grey Growth Edge Tactics", "*(Medium aggression, safe but effective)*", ""]
    found = False
    for dn in EDGE_DOCS:
        if dn in gdocs:
            acts = _extract_actions(gdocs[dn])
            if acts:
                L.append(f"**From {dn}:**")
                L += [f"   {a}" for a in acts] + [""]
                found = True
    if not found:
        L += [f"   - {d}" for d in EDGE_DEFAULTS] + [""]
    if edge_only: return "\n".join(L)

    # Platform-specific
    L.append("### Platform-Specific Tactics")
    for p in platforms:
        L.append(f"**{p}:**")
        hit = False
        for dn in PLAT_DOCS.get(p, []):
            if dn in gdocs:
                for a in _extract_actions(gdocs[dn], 3): L.append(f"   {a}")
                hit = True
        if not hit: L += [f"   - Deploy {venture.lower()} assets to {p}", f"   - Create platform-native content"]
        L.append("")

    # Distribution
    L.append("### Content Distribution Plan")
    hit = False
    for dn in DIST_DOCS:
        if dn in gdocs:
            L.append(f"   - **{dn}**: {gdocs[dn][0].strip('#').strip()}")
            hit = True
    if not hit: L += ["   - One input -> 4+ output channels", "   - Build in public for 3-5x conversion", "   - 4-layer coordinated launch system"]
    L.append("")

    # Engagement
    L.append("### Engagement Farming")
    hit = False
    for dn in ENG_DOCS:
        if dn in gdocs:
            for a in _extract_actions(gdocs[dn], 3): L.append(f"   {a}")
            hit = True
    if not hit: L += ["   - Reply bait outperforms RT bait 3x", "   - 1 reply = 4x value of a like", "   - Reply guy 5-touch rule"]
    L.append("")

    # Multi-account
    L.append("### Multi-Account Strategy")
    if "multi_account_warmup.md" in gdocs:
        for a in _extract_actions(gdocs["multi_account_warmup.md"]): L.append(f"   {a}")
    else:
        L += ["   - 21-30 day warmup SOP per account", "   - Mobile proxies required", "   - Separate browser profiles", "   - Stagger posting times"]
    L.append("")

    # Master Ops synergy & tool intelligence
    synergy_ctx = _get_synergy_context(venture)
    if synergy_ctx:
        L += [f"### MASTER OPS SYNERGY & TOOLS", synergy_ctx, ""]

    # KPIs
    L += _section("KPIs", [f"- {k}" for k in kpis])

    # Marketing channels from CSV
    vl = venture.lower()
    rel = [c for c in channels if vl in (c.get("venture","") or c.get("method","") or c.get("channel","") or "").lower()][:5]
    if rel: L += _section("Active Marketing Channels", [f"- {c.get('channel', c.get('name','?'))} ({c.get('status','?')})" for c in rel])

    # Weekly actions
    L += ["### Weekly Actions",
          f"   1. `python3 AUTOMATIONS/intelligence_router.py --venture {venture} --full`",
          f"   2. `python3 AUTOMATIONS/alpha_query.py --venture {venture} --top 10`",
          f"   3. Execute top 3 tactics from alpha above",
          f"   4. Create 5+ platform-native content pieces",
          f"   5. Distribute to {', '.join(platforms[:3])}",
          f"   6. Track: {', '.join(kpis[:3])}", ""]
    return "\n".join(L)

def generate_report(ventures: list[str], edge_only: bool = False, as_json: bool = False) -> str | dict[str, Any]:
    log(f"Gathering intelligence for {len(ventures)} ventures...")
    gdocs = read_growth_docs()
    catalog = read_json_file(INTEL_CAT)
    channels = read_csv_rows(MKT_CSV)
    log(f"Loaded: {len(gdocs)} growth docs, {len(channels)} channels")

    if as_json: output = {"generated_at": ts(), "ventures": {}}
    lines = [f"# PRINTMAXX Growth Strategy Report", f"**Generated:** {ts()}",
             f"**Mode:** {'Edge Only' if edge_only else 'Full'}", f"**Ventures:** {len(ventures)}",
             f"**Sources:** {len(gdocs)} growth docs, {len(channels)} channels", "", "---", ""]

    for v in ventures:
        log(f"Strategy: {v}...")
        intel = _run_json("intelligence_router.py", ["--venture", v])
        alpha = _run_json("alpha_query.py", ["--venture", v, "--top", "15"])
        strat = gen_venture(v, intel, alpha, gdocs, channels, edge_only)
        if as_json:
            output["ventures"][v] = {
                "alpha_count": len(alpha), "intel_docs": len(intel.get("docs",[])) if isinstance(intel,dict) else 0,
                "top_tactics": [{"tactic":(e.get("tactic") or "")[:200], "roi":e.get("roi_potential","?"), "source":e.get("alpha_id","?")} for e in (alpha[:3] if isinstance(alpha,list) else [])],
                "platforms": VCTX.get(v,("",[],""))[1], "kpis": VCTX.get(v,("","",[],""))[2], "strategy_text": strat}
        else:
            lines += [strat, "---", ""]

    if as_json: return output
    buried = catalog.get("high_value_summary", catalog.get("buried_gold_summary", {}))
    if buried:
        lines.append("## Buried Gold (Intelligence Catalog)")
        for k, val in buried.items():
            lines.append(f"**{k}:** {len(val) if isinstance(val,list) else val}")
        lines.append("")
    return "\n".join(lines)

def main() -> None:
    p = argparse.ArgumentParser(description="PRINTMAXX Growth Strategist")
    p.add_argument("--venture", help=f"Single venture: {', '.join(VENTURES)}")
    p.add_argument("--edge", action="store_true", help="Grey edge tactics only")
    p.add_argument("--json", action="store_true", help="JSON output for agents")
    a = p.parse_args()

    vlist = VENTURES
    if a.venture:
        v = a.venture.upper()
        if v not in VENTURES: print(f"Unknown: {v}\nAvailable: {', '.join(VENTURES)}"); sys.exit(1)
        vlist = [v]

    result = generate_report(vlist, edge_only=a.edge, as_json=a.json)
    if a.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        REPORTS.mkdir(parents=True, exist_ok=True)
        out = safe_path(REPORTS / f"growth_strategy_{datetime.now():%Y%m%d}.md")
        out.write_text(result, encoding="utf-8")
        print(result)
        log(f"Saved: {out}")

if __name__ == "__main__":
    main()
