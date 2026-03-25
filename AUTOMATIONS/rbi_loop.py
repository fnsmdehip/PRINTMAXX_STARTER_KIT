#!/usr/bin/env python3
"""RBI LOOP -- Research, Backtest, Implement pipeline.

Real 3-phase loop reading live project state.  Validates methods against
actual system capabilities and routes PASS methods into execution.

CLI:
    python3 AUTOMATIONS/rbi_loop.py --full          # All 3 phases
    python3 AUTOMATIONS/rbi_loop.py --research       # Research only
    python3 AUTOMATIONS/rbi_loop.py --backtest       # Backtest top N
    python3 AUTOMATIONS/rbi_loop.py --implement      # Implement validated
    python3 AUTOMATIONS/rbi_loop.py --status         # Pipeline status
    python3 AUTOMATIONS/rbi_loop.py --top N          # Top N at each stage

Stdlib only.  No claude -p calls.
"""
from __future__ import annotations
import argparse, csv, json, logging, sys, time
from datetime import datetime, timezone
from pathlib import Path

csv.field_size_limit(10 * 1024 * 1024)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent_resilience import safe_path, TrajectoryLogger, PROJECT_ROOT

# -- Paths ------------------------------------------------------------------
PROJECT = PROJECT_ROOT
AUTO = PROJECT / "AUTOMATIONS"
LEDGER, OPS = PROJECT / "LEDGER", PROJECT / "OPS"
STATE_FILE = AUTO / "agent" / "rbi_state.json"
LOG_FILE = AUTO / "logs" / "rbi_loop.log"
RANKINGS_CSV = LEDGER / "CAPITAL_GENESIS_RANKINGS.csv"
PRIORITY_MD = OPS / "CAPITAL_GENESIS_PRIORITY_STACK.md"
ACCOUNTS_CSV = LEDGER / "ACCOUNTS.csv"
MANIFEST = OPS / "RESOURCE_MANIFEST.md"
ALPHA_DB = LEDGER / "alpha_index.db"
AQ = OPS / "ACTIONABLE_QUEUE.md"
MEGA_CSV = LEDGER / "MEGA_SHEET" / "TAB1_MONEY_METHODS_MASTER.csv"

_traj = TrajectoryLogger("rbi_loop")
AUTO.joinpath("logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO,
    format="[%(asctime)s] [RBI] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(str(LOG_FILE), encoding="utf-8"),
              logging.StreamHandler(sys.stderr)])
log = logging.getLogger("rbi_loop")

# -- Helpers ----------------------------------------------------------------
def _now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _sf(v, d=5.0):
    try: return float(str(v).replace("*","").strip())
    except (ValueError,TypeError): return d

def _read_csv(p):
    if not p.exists(): return []
    try:
        with open(p,"r",newline="",errors="replace") as f:
            return list(csv.DictReader(f))
    except Exception as e:
        log.warning("CSV read fail %s: %s", p.name, e); return []

def _load_state():
    if STATE_FILE.exists():
        try: return json.loads(STATE_FILE.read_text())
        except Exception: pass
    return {"researched":[],"backtested":[],"implemented":[],"last_run":None}

def _save_state(s):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    safe_path(STATE_FILE)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(s, indent=2, default=str)); tmp.rename(STATE_FILE)

def _fts(query, limit=20):
    if not ALPHA_DB.exists(): return []
    try:
        import sqlite3
        c = sqlite3.connect(str(ALPHA_DB)); c.row_factory = sqlite3.Row
        rows = c.execute("SELECT alpha_id,category,tactic,roi_potential,status "
            "FROM alpha_fts WHERE alpha_fts MATCH ? ORDER BY rank LIMIT ?",
            (query, limit)).fetchall()
        c.close(); return [dict(r) for r in rows]
    except Exception: return []

def _accounts():
    return {row.get("Platform",row.get("platform","")).strip().lower()
            for row in _read_csv(ACCOUNTS_CSV) if row.get("Platform",row.get("platform","")).strip()}

def _automations():
    return {f.stem.lower() for f in AUTO.iterdir() if f.suffix==".py" and f.is_file()} if AUTO.exists() else set()

# -- PHASE 1: RESEARCH -----------------------------------------------------
PLATFORM_KW = {"tiktok":"tiktok","twitter":"x","instagram":"instagram",
    "youtube":"youtube","gumroad":"gumroad","stripe":"stripe","linkedin":"linkedin",
    "facebook":"facebook","reddit":"reddit","shopify":"shopify","whop":"whop","beehiiv":"beehiiv"}

AUTO_KW = {"content":["content_","engagement_bait","content_repurpose"],
    "scraping":["scraper","scrape","crawl"],"outbound":["outbound","cold_email","lead_"],
    "affiliate":["affiliate","commission"],"app":["app_factory","app_autopilot"],
    "ecom":["ecom_","arb_","listing"]}

VENTURE_MAP = {"CONTENT_FARM":"CONTENT","CONTENT_FORMAT":"CONTENT","AI_INFLUENCER":"CONTENT",
    "NEWSLETTER":"CONTENT","APP_FACTORY":"APP_FACTORY","CHROME_EXT":"APP_FACTORY",
    "MCP_SERVER":"APP_FACTORY","SAAS":"APP_FACTORY","DIRECTORY":"APP_FACTORY",
    "OUTBOUND":"OUTBOUND","COLD_OUTBOUND":"OUTBOUND","AGENCY":"OUTBOUND","LOCAL_BIZ":"LOCAL_BIZ",
    "MONETIZATION":"MONETIZE","ECOM":"MONETIZE","ECOM_ARB":"MONETIZE",
    "DIGITAL_PRODUCTS":"PRODUCT","INFO_PRODUCTS":"PRODUCT","AFFILIATE":"CONTENT",
    "COMMUNITY":"CONTENT","FREELANCE":"OUTBOUND","BROKERING":"OUTBOUND",
    "SCRAPING":"SCRAPING","RESEARCH":"RESEARCH"}

def phase_research(top_n=30):
    log.info("=== RESEARCH PHASE ===")
    rankings = _read_csv(RANKINGS_CSV)
    if not rankings:
        return _research_md(top_n)
    rankings.sort(key=lambda r: _sf(r.get("composite",0),0), reverse=True)
    out = []
    for r in rankings[:top_n]:
        m = {"method_id":r.get("method_id",""), "name":r.get("method_name","")[:120],
             "composite":_sf(r.get("composite",0),0), "priority":r.get("priority","P2"),
             "category":r.get("category","GENERAL"),
             "revenue_potential":_sf(r.get("revenue_potential",5)),
             "speed":_sf(r.get("speed_to_revenue",5)),
             "automation":_sf(r.get("automation_potential",5)),
             "risk":_sf(r.get("downside_risk",5)), "cost_raw":r.get("estimated_cost","$0"),
             "source_type":r.get("source_type",""), "status":r.get("status",""),
             "action":r.get("recommended_action",""), "rbi_stage":"RESEARCHED"}
        kw = m["name"].split()[:3]
        m["alpha_signals"] = len(_fts(" ".join(kw), 3)) if kw else 0
        out.append(m)
    log.info("Researched %d candidates (top %d from %d ranked)", len(out), top_n, len(rankings))
    _traj.log_attempt("research_complete", candidates=len(out))
    return out

def _research_md(top_n):
    if not PRIORITY_MD.exists(): log.error("No priority stack"); return []
    text = PRIORITY_MD.read_text(errors="replace"); out = []
    for line in text.split("\n"):
        if not line.startswith("|") or "Rank" in line or "---" in line: continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 8: continue
        try: sc = float(cells[2].replace("*","").strip())
        except (ValueError,IndexError): continue
        out.append({"method_id":f"STACK_{len(out)}","name":cells[1][:120],"composite":sc,
            "priority":"P0" if sc>=7.5 else "P1" if sc>=6.0 else "P2",
            "category":cells[-1] if len(cells)>7 else "GENERAL",
            "revenue_potential":_sf(cells[4]) if len(cells)>4 else 5,
            "speed":_sf(cells[5]) if len(cells)>5 else 5,"automation":5,"risk":5,
            "cost_raw":"$0","source_type":"priority_stack","status":"","action":"",
            "alpha_signals":0,"rbi_stage":"RESEARCHED"})
        if len(out)>=top_n: break
    log.info("Parsed %d from priority stack markdown", len(out)); return out

# -- PHASE 2: BACKTEST ------------------------------------------------------
def phase_backtest(candidates, top_n=15):
    log.info("=== BACKTEST PHASE ===")
    manifest = (MANIFEST.read_text(errors="replace").lower() if MANIFEST.exists() else "")
    accts, autos = _accounts(), _automations()
    mega = _read_csv(MEGA_CSV)
    mega_ids = {r.get("method_id","").lower() for r in mega if r.get("method_id")}
    results = [_bt_one(m, manifest, accts, autos, mega_ids, mega) for m in candidates[:top_n]]
    p = sum(1 for r in results if r["backtest_verdict"]=="PASS")
    c = sum(1 for r in results if r["backtest_verdict"]=="CONDITIONAL")
    f = sum(1 for r in results if r["backtest_verdict"]=="FAIL")
    log.info("Backtested %d: PASS=%d, CONDITIONAL=%d, FAIL=%d", len(results), p, c, f)
    _traj.log_attempt("backtest_complete", total=len(results), passed=p, conditional=c, failed=f)
    return results

def _bt_one(m, manifest, accts, autos, mega_ids, mega):
    blockers, signals, score = [], [], 0
    nl, cl, ml = m.get("name","").lower(), m.get("category","").lower(), m.get("method_id","").lower()
    # 1. Dedup
    if ml in mega_ids: signals.append("EXISTS_IN_MEGA_SHEET"); score -= 10
    words = [w for w in nl.split() if len(w)>3][:4]
    if sum(1 for w in words if w in manifest) >= 2:
        signals.append("PLAYBOOK_EXISTS"); score += 15
    # 2. Account check
    for kw, plat in PLATFORM_KW.items():
        if kw in nl or kw in cl:
            if plat in accts: signals.append(f"ACCT_OK:{plat}"); score += 10
            else: blockers.append(f"NEED_ACCOUNT:{plat}")
    # 3. Automation check
    for dom, stems in AUTO_KW.items():
        if dom in nl or dom in cl:
            if any(s in a for a in autos for s in stems):
                signals.append(f"AUTO_EXISTS:{dom}"); score += 10
            break
    # 4. Alpha signals
    ac = m.get("alpha_signals", 0)
    if ac >= 3: signals.append(f"STRONG_ALPHA:{ac}"); score += 15
    elif ac >= 1: signals.append(f"SOME_ALPHA:{ac}"); score += 5
    # 5. Revenue estimate
    cat = m.get("category","").upper()
    comps = [r for r in mega if cat in str(r.get("category","")).upper()] or mega[:10]
    lows = [float(r.get("monthly_potential_low",0) or 0) for r in comps
            if float(r.get("monthly_potential_low",0) or 0) > 0]
    highs = [float(r.get("monthly_potential_high",0) or 0) for r in comps
             if float(r.get("monthly_potential_high",0) or 0) > 0]
    rp = int(m.get("revenue_potential",5))
    bl = {10:500,8:200,5:50,2:10}.get(rp, 50)
    bh = bl * 5
    if lows: bl = max(bl, int(sum(lows)/len(lows)))
    if highs: bh = max(bh, int(sum(highs)/len(highs)))
    m["revenue_estimate"] = {"monthly_low":bl,"monthly_high":bh,"comparables":len(comps)}
    # 6. Composite
    score += int(m.get("composite",0)*8) + int(m.get("speed",5)*2)
    score = max(0, min(100, score))
    m["backtest_score"] = score
    # Verdict
    if blockers and all("NEED_ACCOUNT" in b for b in blockers):
        m["backtest_verdict"] = "CONDITIONAL"
    elif score >= 50 and not blockers:
        m["backtest_verdict"] = "PASS"
    elif score >= 35:
        m["backtest_verdict"] = "CONDITIONAL"
    else:
        m["backtest_verdict"] = "FAIL"
    m["backtest_blockers"] = blockers
    m["backtest_signals"] = signals
    m["rbi_stage"] = "BACKTESTED"
    return m

# -- PHASE 3: IMPLEMENT -----------------------------------------------------
def phase_implement(backtested):
    log.info("=== IMPLEMENT PHASE ===")
    impl, queued, archived = [], [], []
    for m in backtested:
        v = m.get("backtest_verdict")
        if v == "PASS":
            tgt = VENTURE_MAP.get(m.get("category","").upper(), "CONTENT")
            impl.append({"method_id":m["method_id"],"name":m["name"][:100],
                "target_venture":tgt,"category":m.get("category",""),
                "composite":m.get("composite",0),"revenue_estimate":m.get("revenue_estimate",{}),
                "routed_at":_now(),"signals":m.get("backtest_signals",[])})
            m["rbi_stage"] = "IMPLEMENTED"
            log.info("IMPLEMENT: %s -> %s (%.1f)", m["method_id"], tgt, m.get("composite",0))
        elif v == "CONDITIONAL":
            queued.append({"method_id":m["method_id"],"name":m["name"],
                "blockers":m.get("backtest_blockers",[]),"priority":m.get("priority","P2")})
        else:
            archived.append({"method_id":m["method_id"],"name":m["name"],
                "reason":m.get("backtest_blockers",["FAILED"]),"score":m.get("backtest_score",0)})
    if queued:
        safe_path(AQ)
        lines = [f"\n\n## RBI Conditional Methods\n*Updated: {_now()}*\n"]
        for q in queued:
            lines.append(f"- **{q['priority']}** | {q['name'][:80]} | Blockers: {', '.join(q['blockers'])}")
        try:
            with open(AQ, "a", encoding="utf-8") as f: f.write("\n".join(lines)+"\n")
            log.info("Appended %d items to ACTIONABLE_QUEUE.md", len(queued))
        except Exception as e: log.warning("Queue write fail: %s", e)
    summary = {"implemented":len(impl),"queued":len(queued),"archived":len(archived),
               "details":{"implemented":impl,"queued":queued,"archived":archived}}
    log.info("Implemented %d, queued %d, archived %d", len(impl), len(queued), len(archived))
    _traj.log_attempt("implement_complete", implemented=len(impl),queued=len(queued),archived=len(archived))
    return summary

# -- ORCHESTRATION -----------------------------------------------------------
def run_full(top_n=20):
    state = _load_state(); t0 = time.time()
    researched = phase_research(top_n=top_n*2)
    state["researched"] = [r["method_id"] for r in researched]
    backtested = phase_backtest(researched, top_n=top_n)
    state["backtested"] = [{"id":r["method_id"],"verdict":r.get("backtest_verdict","?")} for r in backtested]
    impl = phase_implement(backtested)
    state["implemented"] = impl.get("details",{}).get("implemented",[])
    state["last_run"] = _now()
    state["duration_s"] = round(time.time()-t0, 2)
    state["summary"] = {"researched":len(researched),"backtested":len(backtested),
        "passed":sum(1 for r in backtested if r.get("backtest_verdict")=="PASS"),
        "conditional":sum(1 for r in backtested if r.get("backtest_verdict")=="CONDITIONAL"),
        "failed":sum(1 for r in backtested if r.get("backtest_verdict")=="FAIL"),
        "implemented":impl["implemented"]}
    _save_state(state); return state

def show_status():
    s = _load_state()
    if not s.get("last_run"):
        print("RBI pipeline not yet run.\nRun: python3 AUTOMATIONS/rbi_loop.py --full"); return
    sm = s.get("summary",{})
    print(f"=== RBI Pipeline Status ===\nLast run: {s['last_run']}\n"
          f"Researched:    {sm.get('researched',0)}\nBacktested:    {sm.get('backtested',0)}\n"
          f"  PASS:        {sm.get('passed',0)}\n  CONDITIONAL: {sm.get('conditional',0)}\n"
          f"  FAIL:        {sm.get('failed',0)}\nImplemented:   {sm.get('implemented',0)}\n"
          f"Duration:      {s.get('duration_s',0)}s\nState file:    {STATE_FILE}")

def show_top(n):
    bt = phase_backtest(phase_research(top_n=n*2), top_n=n)
    bt.sort(key=lambda m: m.get("backtest_score",0), reverse=True)
    print(f"\n{'='*90}\n  TOP {n} RBI CANDIDATES\n{'='*90}")
    fmt = "{:<5} {:<40} {:>5} {:>4} {:>11} {:<6} {}"
    print(fmt.format("RANK","METHOD","COMP","BT","VERDICT","PRI","BLOCKERS"))
    print("-"*90)
    for i, m in enumerate(bt[:n], 1):
        print(fmt.format(i, m.get("name","?")[:40], f"{m.get('composite',0):.1f}",
            m.get("backtest_score",0), m.get("backtest_verdict","?"),
            m.get("priority","?"), ",".join(m.get("backtest_blockers",[]))[:25]))
    print()

# -- CLI ---------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="RBI Loop: Research, Backtest, Implement")
    ap.add_argument("--full", action="store_true", help="Run all 3 phases")
    ap.add_argument("--research", action="store_true", help="Research phase only")
    ap.add_argument("--backtest", action="store_true", help="Backtest phase only")
    ap.add_argument("--implement", action="store_true", help="Implement validated")
    ap.add_argument("--status", action="store_true", help="Show pipeline status")
    ap.add_argument("--top", type=int, default=0, metavar="N", help="Top N methods")
    a = ap.parse_args()
    if a.status: show_status()
    elif a.top: show_top(a.top)
    elif a.full: print(json.dumps(run_full().get("summary",{}), indent=2))
    elif a.research:
        res = phase_research()
        for r in res[:10]:
            print(f"  [{r.get('priority','?')}] {r.get('composite',0):.1f} | {r.get('name','?')[:60]}")
        print(f"\nTotal researched: {len(res)}")
    elif a.backtest:
        bt = phase_backtest(phase_research())
        for r in bt:
            print(f"  [{r['backtest_verdict']:11}] BT={r.get('backtest_score',0):3d} | {r.get('name','?')[:60]}")
    elif a.implement:
        print(json.dumps(phase_implement(phase_backtest(phase_research())), indent=2, default=str))
    else: show_status()

if __name__ == "__main__":
    main()
