#!/usr/bin/env python3
"""
DAILY TACTICAL ENGINE — Unified daily action plan across ALL ventures.

Reads intelligence_router.py, alpha_query.py, INTELLIGENCE_CATALOG.json,
state files (ceo/autonomy/swarm/warmup), DAILY_DIGEST.md, PERSISTENT_TASK_TRACKER.md,
and revenue blockers. Outputs OPS/DAILY_TACTICAL_PLAN.md.

Usage:
    python3 AUTOMATIONS/daily_tactical_engine.py              # Print plan
    python3 AUTOMATIONS/daily_tactical_engine.py --save       # Write to OPS/
    python3 AUTOMATIONS/daily_tactical_engine.py --json       # Structured JSON
    python3 AUTOMATIONS/daily_tactical_engine.py --dry-run    # Print only

Run at 7:15 AM after engagement planner.
"""

from __future__ import annotations

import argparse, json, subprocess, sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# === Master Ops xlsx bridge ===
try:
    from master_ops_bridge import MasterOpsBridge
    _BRIDGE_AVAILABLE = True
except ImportError:
    _BRIDGE_AVAILABLE = False

PROJECT = Path(__file__).resolve().parent.parent
AUTO = PROJECT / "AUTOMATIONS"
OPS = PROJECT / "OPS"
AGT = AUTO / "agent"
PYTHON = sys.executable
OUTPUT = OPS / "DAILY_TACTICAL_PLAN.md"

PATHS = {
    "ceo": AGT / "ceo_agent" / "ceo_state.json",
    "autonomy": AGT / "autonomy" / "autonomy_state.json",
    "swarm": AGT / "swarm" / "swarm_state.json",
    "warmup": AGT / "twitter_warmup_state.json",
    "catalog": OPS / "INTELLIGENCE_CATALOG.json",
    "digest": OPS / "DAILY_DIGEST.md",
    "tracker": OPS / "PERSISTENT_TASK_TRACKER.md",
}

VENTURES = ["CONTENT", "OUTBOUND", "APP_FACTORY", "LOCAL_BIZ",
            "MONETIZATION", "PRODUCT", "RESEARCH", "SCRAPING"]

VENTURE_NAMES = {
    "CONTENT": "Content Farm & Distribution", "OUTBOUND": "Cold Email & Outbound",
    "APP_FACTORY": "App Factory (PWAs & Mobile)", "LOCAL_BIZ": "Local Business Pipeline",
    "MONETIZATION": "Revenue & Monetization", "PRODUCT": "Digital Products",
    "RESEARCH": "Alpha Research & Intelligence", "SCRAPING": "Competitive Intel Scrapers",
}

BLOCKERS = [
    ("P0", "Authenticate Stripe MCP", "5 min", "Unlocks payments", "Settings > MCP > Stripe > paste API key"),
    ("P0", "Authenticate Gmail MCP", "5 min", "Unlocks cold email", "Settings > MCP > Gmail > OAuth flow"),
    ("P0", "Upload Twitter profile", "10 min", "@PRINTMAXXER has no pfp/banner/bio",
     "MEDIA/generated_images/twitter_banner.png + twitter_pfp.png + TWITTER_PROFILE_SPEC.md"),
    ("P0", "Gumroad: list 13 products", "30 min", "13 products built, $0 listed",
     "gumroad.com > sign up > upload from DIGITAL_PRODUCTS/"),
    ("P1", "TikTok account + first video", "30 min", "5 scripts ready",
     "tiktok.com > sign up > post from TIKTOK_LAUNCH_SCRIPTS.md"),
    ("P1", "Cloudflare signup", "5 min", "Replace surge.sh",
     "cloudflare.com > sign up > connect GitHub"),
]

# ─── Helpers ──────────────────────────────────────────────────────────

def _safe_path(p: str | Path) -> Path:
    r = Path(p).resolve()
    if not str(r).startswith(str(PROJECT)):
        raise ValueError(f"BLOCKED: {r} outside {PROJECT}")
    return r

def _json(path: str | Path) -> dict[str, Any]:
    try:
        if Path(path).exists():
            return json.loads(Path(path).read_text(encoding="utf-8", errors="replace"))
    except Exception: pass
    return {}

def _text(path: str | Path, n: int = 200) -> str:
    try:
        if Path(path).exists():
            return "\n".join(Path(path).read_text(encoding="utf-8", errors="replace").splitlines()[:n])
    except Exception: pass
    return ""

def _run(cmd: list[str], t: int = 30) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=t, cwd=str(PROJECT))
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception: return ""

# ─── Gatherers ────────────────────────────────────────────────────────

def gather_venture_intel() -> dict[str, str]:
    out: dict[str, str] = {}
    router = str(AUTO / "intelligence_router.py")
    for v in VENTURES:
        b = _run([PYTHON, router, "--venture", v, "--brief"], t=20)
        # Strip router banner lines
        clean = [ln.strip() for ln in (b or "").splitlines()
                 if ln.strip() and len(ln.strip()) > 15
                 and not ln.strip().startswith("=") and not ln.strip().startswith("---")
                 and not ln.strip().startswith("INTELLIGENCE ROUTER")
                 and not ln.strip().startswith("Venture:") and not ln.strip().startswith("Task:")
                 and not ln.strip().startswith("BRIEF:") and not ln.strip()[:5].replace("-","").isdigit()]
        out[v] = clean[0][:150] if clean else ""
    return out

def gather_top_alpha(n: int = 5) -> list[dict[str, Any]]:
    raw = _run([PYTHON, str(AUTO / "alpha_query.py"), "--top", str(n), "--json"], t=15)
    try: return json.loads(raw) if raw else []
    except Exception: return []

def gather_alpha_stats() -> str:
    return _run([PYTHON, str(AUTO / "alpha_query.py"), "--stats"], t=15) or ""

def gather_catalog() -> dict[str, list[dict[str, Any]]]:
    cat = _json(PATHS["catalog"])
    out = {}
    for vt, data in cat.get("ventures", {}).items():
        high = [d for d in data.get("docs", []) if d.get("value") in ("HIGH", "HIGHEST")][:2]
        if high: out[vt] = high
    return out

def gather_ceo() -> dict[str, Any]:
    s = _json(PATHS["ceo"])
    if not s: return {"cycles": 0, "decisions": 0, "top_ops": [], "last": "never"}
    ops = sorted(s.get("op_scores", {}).values(), key=lambda x: x.get("total_score", 0), reverse=True)
    return {
        "cycles": s.get("cycles_run", 0), "decisions": s.get("total_decisions", 0),
        "last": s.get("last_cycle", "never"),
        "top_ops": [{"id": o.get("op_id"), "name": o.get("name"), "score": o.get("total_score", 0),
                      "blocker": o.get("blocker", ""), "rev": o.get("revenue_range", "")} for o in ops[:5]],
    }

def gather_autonomy() -> list[dict[str, Any]]:
    s = _json(PATHS["autonomy"])
    out = []
    for vid, v in s.get("ventures", {}).items():
        stats = v.get("pipeline_stats", {})
        stuck = [st for st in v.get("pipeline", [])
                 if stats.get(st, {}).get("runs", 0) > 0 and stats.get(st, {}).get("successes", 0) == 0]
        out.append({"id": vid, "name": v.get("name", vid), "type": v.get("type", "?"),
                     "status": v.get("status", "?"), "cycles": v.get("cycles_run", 0),
                     "last_run": v.get("last_run") or "never", "stuck": stuck})
    return out

def gather_swarm() -> dict[str, int]:
    s = _json(PATHS["swarm"])
    agents = s.get("agents", {})
    return {"total": len(agents), "active": sum(1 for a in agents.values() if a.get("status") == "ACTIVE")}

def gather_warmup() -> dict[str, Any]:
    s = _json(PATHS["warmup"])
    day = s.get("current_day", 0)
    for name, lo, hi in [("LURK",1,3),("ENGAGE",4,7),("SOFT_POST",8,14),("RAMP",15,21),("FULL_OPS",22,999)]:
        if lo <= day <= hi: return {"day": day, "phase": name}
    return {"day": day, "phase": "NOT_STARTED"}

def gather_digest() -> str:
    t = _text(PATHS["digest"], 100)
    if not t: return ""
    return "\n".join(ln.strip() for ln in t.splitlines()
                     if ln.strip().startswith("- **") or ln.strip().startswith("### "))[:800]

def gather_tracker() -> str:
    t = _text(PATHS["tracker"], 150)
    if not t: return ""
    active = [ln.strip()[:120] for ln in t.splitlines()
              if "[ ]" in ln or "in progress" in ln.lower()][:5]
    blocked = [ln.strip()[:120] for ln in t.splitlines()
               if "blocked" in ln.lower() or "blocker" in ln.lower()][:5]
    parts = []
    if active: parts.append("Active: " + " | ".join(active))
    if blocked: parts.append("Blocked: " + " | ".join(blocked))
    return "\n".join(parts)

# ─── Action Generation ───────────────────────────────────────────────

def gen_venture_actions(intel: dict[str, str], autonomy: list[dict[str, Any]], catalog: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    by_type = {}
    for v in autonomy:
        by_type.setdefault(v["type"], []).append(v)
    actions = []
    for vt in VENTURES:
        brief = intel.get(vt, "")
        autos = by_type.get(vt, [])
        cats = catalog.get(vt, [])
        acts = []
        for av in autos:
            if av["stuck"]:
                acts.append({"action": f"Fix stuck: {', '.join(av['stuck'])} in {av['name']}",
                             "why": f"{av['cycles']} cycles, stages failing",
                             "cmd": f"python3 AUTOMATIONS/venture_autonomy.py --run {av['id']}",
                             "expected": "Stuck stages complete"})
            elif av["cycles"] == 0 and av["status"] == "ACTIVE":
                acts.append({"action": f"First run: {av['name']}",
                             "why": "Created but never executed",
                             "cmd": f"python3 AUTOMATIONS/venture_autonomy.py --run {av['id']}",
                             "expected": "First full cycle completes"})
        if cats:
            d = cats[0]
            tac = (d.get("key_tactics") or [""])[0][:100]
            acts.append({"action": f"Execute: {d.get('path','')}",
                         "why": f"HIGH value: {d.get('summary','')[:80]}",
                         "cmd": f"cat {d.get('path','')} | head -50", "expected": tac})
        if brief:
            acts.append({"action": f"Intel: {brief[:120]}",
                         "why": f"Router brief for {vt}",
                         "cmd": f"python3 AUTOMATIONS/intelligence_router.py --venture {vt} --brief",
                         "expected": "Intelligence-informed action"})
        if acts:
            actions.append({"type": vt, "name": VENTURE_NAMES.get(vt, vt), "actions": acts})
    return actions

# ─── Master Ops Intelligence ─────────────────────────────────────────

def _get_master_ops_priorities() -> str:
    """Get priority actions from Master Ops xlsx for today's plan."""
    if not _BRIDGE_AVAILABLE:
        return ""
    try:
        bridge = MasterOpsBridge()

        sections = []

        # Priority launches that are READY
        priority = bridge.get_priority_launch()
        ready_ids = {op.get("OP_ID") for op in bridge.get_ready_ops()}
        actionable = [p for p in priority if p.get("OP_ID") in ready_ids]

        if actionable:
            sections.append("### PRIORITY LAUNCHES (READY NOW)")
            for p in actionable[:5]:
                sections.append(
                    f"- [{p.get('OP_ID')}] {p.get('OP_NAME')} "
                    f"— Revenue: {p.get('REVENUE_POTENTIAL')} "
                    f"— First $: {p.get('TIME_TO_FIRST_$')} "
                    f"— Step: {str(p.get('FIRST_STEP', ''))[:80]}"
                )

        # Top synergy opportunities
        synergies = bridge.get_top_synergies(3)
        if synergies:
            sections.append("\n### TOP SYNERGY STACKS")
            for s in synergies:
                sections.append(
                    f"- {s.get('NAME')} (score: {s.get('SYNERGY_SCORE')}, "
                    f"{s.get('REVENUE_MULTIPLIER')}x) — {s.get('METHODS_COMBINED')}"
                )

        # Current blockers to surface
        blockers = bridge.get_blocker_summary()
        if blockers:
            sections.append("\n### ACTIVE BLOCKERS (HUMAN ACTION NEEDED)")
            for b in blockers[:5]:
                sections.append(f"- {b.get('blocker')}: blocking {b.get('count')} ventures")

        # Ops with playbooks available
        ready_with_playbook = []
        for op in bridge.get_ready_ops()[:20]:
            playbook = bridge.get_playbook_for_op(op.get("OP_ID", ""))
            if playbook:
                ready_with_playbook.append(op)

        if ready_with_playbook:
            sections.append("\n### READY OPS WITH PLAYBOOKS")
            for op in ready_with_playbook[:5]:
                sections.append(
                    f"- [{op.get('OP_ID')}] {op.get('OP_NAME')} "
                    f"— {op.get('LANE')} — Auto score: {op.get('AUTOMATION_SCORE_100')}/100"
                )

        return "\n".join(sections)
    except Exception:
        return ""


# ─── Build Plan ───────────────────────────────────────────────────────

def build_plan() -> str:
    now = datetime.now()
    vi = gather_venture_intel()
    stats = gather_alpha_stats()
    top = gather_top_alpha(5)
    cat = gather_catalog()
    ceo = gather_ceo()
    aut = gather_autonomy()
    swm = gather_swarm()
    wrm = gather_warmup()
    dig = gather_digest()
    trk = gather_tracker()
    va = gen_venture_actions(vi, aut, cat)

    total_min = sum(int(b[2].split()[0]) for b in BLOCKERS)
    L = []  # output lines
    def w(*args): L.extend(args)

    w(f"# DAILY TACTICAL PLAN — {now.strftime('%B %d, %Y')}",
      f"# Auto-generated by daily_tactical_engine.py at {now.strftime('%H:%M')}", "",
      f"**System pulse:** CEO: {ceo['cycles']} cycles | Swarm: {swm['active']}/{swm['total']} | "
      f"Ventures: {len(aut)} | Warmup: Day {wrm['day']} ({wrm['phase']})", "", "---", "")

    # HUMAN ACTIONS
    w(f"## HUMAN ACTIONS (do these first, ~{total_min} min total)", "",
      "Only the human can do these. System is blocked until they happen.", "")
    for pri, act, tm, why, steps in BLOCKERS:
        if pri == "P0":
            w(f"### [{pri}] {act} ({tm})", f"- **WHY:** {why}", f"- **STEPS:** {steps}", "")
    p1 = [b for b in BLOCKERS if b[0] == "P1"]
    if p1:
        w("### P1 (after P0s)", "")
        for _, act, tm, why, steps in p1:
            w(f"- **{act}** ({tm}) — {why}", f"  Steps: {steps}", "")
    w("---", "")

    # VENTURE ACTIONS
    w("## VENTURE ACTIONS (system executes these)", "")
    for v in va:
        w(f"### {v['type']} — {v['name']}", "")
        for a in v["actions"]:
            w(f"- **ACTION:** {a['action']}", f"  - WHY: {a['why']}",
              f"  - COMMAND: `{a['cmd']}`", f"  - EXPECTED: {a['expected']}", "")
    if not va:
        w("No actions generated. Run: `python3 AUTOMATIONS/venture_autonomy.py --run-all`", "")
    w("---", "")

    # INTELLIGENCE HIGHLIGHTS
    w("## INTELLIGENCE HIGHLIGHTS (act on today)", "",
      "Top alpha by ROI not yet fully executed:", "")
    for i, e in enumerate(top[:5], 1):
        w(f"{i}. **[{e.get('alpha_id','?')}]** ({e.get('category','?')} | ROI:{e.get('roi_potential','?')} | "
          f"{e.get('status','?')} | score:{e.get('score',0)})",
          f"   {(e.get('tactic') or '')[:120]}", "")
    if not top:
        w("No alpha returned. Check: `python3 AUTOMATIONS/alpha_query.py --top 5 --json`", "")
    cat_total = sum(len(d) for d in cat.values())
    if cat_total:
        w(f"**Buried gold ({cat_total} HIGH-value docs):**", "")
        shown = 0
        for vt, docs in cat.items():
            if shown >= 5: break
            w(f"- [{vt}] `{docs[0].get('path','?')}` — {docs[0].get('summary','')[:90]}")
            shown += 1
        w("")
    w("---", "")

    # PIPELINE STATUS
    w("## PIPELINE STATUS", "")
    if ceo["top_ops"]:
        w("**Top ops by CEO score:**", "")
        for o in ceo["top_ops"]:
            blk = f" | BLOCKED: {o['blocker']}" if o.get("blocker") else ""
            w(f"- {o['id']}: {o['name']} (score:{o['score']:.0f}, rev:{o.get('rev','?')}{blk})")
        w("")
    stuck = [v for v in aut if v["stuck"]]
    never = [v for v in aut if v["cycles"] == 0 and v["status"] == "ACTIVE"]
    if stuck:
        w("**Stuck:**", "")
        for v in stuck: w(f"- {v['name']} ({v['type']}): {', '.join(v['stuck'])}")
        w("")
    if never:
        w("**Never ran:**", "")
        for v in never: w(f"- {v['name']} ({v['type']})")
        w("")
    if dig:
        w("**Overnight digest:**", "")
        for dl in dig.splitlines()[:8]: w(f"> {dl}")
        w("")
    if trk and "no actionable" not in trk.lower():
        w("**Tracker:**", "")
        for tl in trk.splitlines()[:4]: w(f"> {tl}")
        w("")
    w("---", "")

    # MASTER OPS INTELLIGENCE
    master_ops_section = _get_master_ops_priorities()
    if master_ops_section:
        w("## MASTER OPS INTELLIGENCE", "", master_ops_section, "", "---", "")

    # OVERNIGHT TARGETS
    w("## OVERNIGHT TARGETS", "", "```",
      "# Scrapers", "python3 AUTOMATIONS/twitter_alpha_scraper.py --all        # 6:00 AM",
      "python3 AUTOMATIONS/background_reddit_scraper.py --scrape # 6:15 AM",
      "python3 AUTOMATIONS/alpha_auto_processor.py --process-new # 6:30 AM", "",
      "# Planning", "python3 AUTOMATIONS/daily_digest.py --days 1 --save       # 6:45 AM",
      "python3 AUTOMATIONS/daily_engagement_planner.py --save    # 7:00 AM",
      "python3 AUTOMATIONS/daily_tactical_engine.py --save       # 7:15 AM", "",
      "# Agents", "python3 AUTOMATIONS/ceo_agent.py                          # every 1h",
      "python3 AUTOMATIONS/venture_autonomy.py --run-all         # every 2h",
      "python3 AUTOMATIONS/loop_closer.py --cycle                # every 2h",
      "```", "")

    if stats:
        w("---", "", "<details><summary>Alpha Stats</summary>", "", "```")
        for al in stats.splitlines()[:25]: w(al)
        w("```", "", "</details>", "")

    w("---", f"*Generated {now.strftime('%Y-%m-%d %H:%M:%S')} by daily_tactical_engine.py*")
    return "\n".join(L)


def build_json() -> dict[str, Any]:
    vi = gather_venture_intel()
    top = gather_top_alpha(5)
    cat = gather_catalog()
    ceo = gather_ceo()
    aut = gather_autonomy()
    swm = gather_swarm()
    wrm = gather_warmup()
    va = gen_venture_actions(vi, aut, cat)
    # Master Ops xlsx intelligence
    master_ops = {}
    if _BRIDGE_AVAILABLE:
        try:
            bridge = MasterOpsBridge()
            ready = bridge.get_ready_ops()
            priority = bridge.get_priority_launch()
            blocked_ops = bridge.get_blocked_ops()
            ready_ids = {op.get("OP_ID") for op in ready}
            actionable_priority = [p for p in priority if p.get("OP_ID") in ready_ids]
            master_ops = {
                "ready_count": len(ready),
                "priority_launches": len(priority),
                "actionable_priority": [
                    {"op_id": p.get("OP_ID"), "name": p.get("OP_NAME"),
                     "revenue": p.get("REVENUE_POTENTIAL")}
                    for p in actionable_priority[:5]
                ],
                "blocked_count": len(blocked_ops),
                "blocker_summary": bridge.get_blocker_summary()[:5],
                "top_synergies": bridge.get_top_synergies(3),
            }
        except Exception:
            pass

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "pulse": {"ceo": ceo["cycles"], "swarm": swm["active"], "ventures": len(aut),
                  "warmup_day": wrm["day"], "warmup_phase": wrm["phase"]},
        "human_actions": [{"pri": b[0], "action": b[1], "time": b[2], "why": b[3]} for b in BLOCKERS],
        "venture_actions": va, "top_alpha": top[:5],
        "pipeline": {"top_ops": ceo["top_ops"],
                     "stuck": [v for v in aut if v["stuck"]],
                     "never_ran": [v for v in aut if v["cycles"] == 0]},
        "master_ops": master_ops,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Daily tactical plan across all ventures")
    p.add_argument("--save", action="store_true", help="Write to OPS/DAILY_TACTICAL_PLAN.md")
    p.add_argument("--json", action="store_true", help="Output JSON")
    p.add_argument("--dry-run", action="store_true", help="Print only (default)")
    a = p.parse_args()
    if a.json:
        print(json.dumps(build_json(), indent=2, default=str)); return
    plan = build_plan()
    if a.save:
        validated = _safe_path(OUTPUT)
        OPS.mkdir(parents=True, exist_ok=True)
        validated.write_text(plan, encoding="utf-8")
        print(f"Saved to {validated}")
    else:
        print(plan)

if __name__ == "__main__":
    main()
