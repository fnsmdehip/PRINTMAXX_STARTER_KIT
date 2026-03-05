#!/usr/bin/env python3
"""
PRINTMAXX Auto-Rebalancer
==========================
Kill losers. Double winners. Treat every method like a portfolio position.

Reads performance data from multiple sources, scores each method 0-100,
and auto-adjusts priorities. Works across ecom, content, freelance, leads,
apps — everything.

The "kill losers, reinvest winners" system that applies to all verticals:
  - SaaS marketing channels
  - Ecom ad spend
  - Content strategies
  - Lead gen sources
  - Product lines
  - Scraper effectiveness

Usage:
  python3 auto_rebalancer.py --check         # Score all, show report
  python3 auto_rebalancer.py --rebalance     # Auto-adjust (safe actions only)
  python3 auto_rebalancer.py --history       # Score trend over time
  python3 auto_rebalancer.py --kill METHOD   # Flag method for decommission
"""

import json
import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).resolve().parent.parent
AUTO = BASE / "AUTOMATIONS"
LEDGER = BASE / "LEDGER"
OPS = BASE / "OPS"
LOGS = AUTO / "logs"
HISTORY_FILE = LOGS / "rebalance_history.jsonl"
LATEST_FILE = LOGS / "rebalance_latest.json"
CHECKPOINTS = OPS / "checkpoints" / "pending"

CHECKPOINTS.mkdir(parents=True, exist_ok=True)


def read_csv_rows(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def read_jsonl(path):
    entries = []
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    except Exception:
        pass
    return entries


def safe_float(v, default=0.0):
    try:
        return float(v)
    except (ValueError, TypeError):
        return default


# ---------------------------------------------------------------------------
# Data collectors — each returns a dict of {method_name: {metric: value}}
# ---------------------------------------------------------------------------

def collect_venture_scores():
    """Read venture_performance_tracker output."""
    path = LEDGER / "VENTURE_PERFORMANCE.csv"
    if not path.exists():
        # Try running the tracker
        import subprocess
        try:
            subprocess.run(
                [sys.executable, str(AUTO / "venture_performance_tracker.py"), "--csv"],
                capture_output=True, timeout=30, cwd=str(BASE)
            )
        except Exception:
            pass

    rows = read_csv_rows(path)
    scores = {}
    for r in rows:
        name = r.get("method", r.get("venture", r.get("name", "")))
        if not name:
            continue
        scores[name] = {
            "venture_score": safe_float(r.get("score", r.get("total_score", 50))),
            "recommendation": r.get("recommendation", r.get("action", "MAINTAIN")),
        }
    return scores


def collect_overnight_health():
    """Score each script by success rate over last 7 days."""
    scores = defaultdict(lambda: {"runs": 0, "success": 0, "fail": 0, "timeout": 0})

    for i in range(7):
        dt = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        sf = LOGS / f"overnight_status_{dt}.json"
        if not sf.exists():
            continue
        try:
            content = sf.read_text().strip()
            # Try proper JSON array first, fall back to JSONL
            parsed = []
            try:
                parsed = json.loads(content)
                if not isinstance(parsed, list):
                    parsed = [parsed]
            except json.JSONDecodeError:
                # JSONL fallback: one JSON object per line
                for line in content.split("\n"):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        parsed.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

            for entry in parsed:
                if not isinstance(entry, dict):
                    continue
                name = entry.get("script", "")
                status = entry.get("status", "")
                scores[name]["runs"] += 1
                if status == "SUCCESS":
                    scores[name]["success"] += 1
                elif status == "FAILED":
                    scores[name]["fail"] += 1
                elif status == "TIMEOUT":
                    scores[name]["timeout"] += 1
        except Exception:
            continue

    result = {}
    for name, data in scores.items():
        if data["runs"] > 0:
            rate = data["success"] / data["runs"] * 100
        else:
            rate = 0
        result[name] = {
            "success_rate": round(rate, 1),
            "runs_7d": data["runs"],
            "fails_7d": data["fail"],
            "timeouts_7d": data["timeout"],
        }
    return result


def collect_lead_source_scores():
    """Score lead gen sources by volume and quality."""
    sources = defaultdict(lambda: {"count": 0, "hot": 0, "warm": 0})

    for csv_name in ["HOT_LEADS_QUALIFIED.csv", "WARM_LEADS_QUALIFIED.csv"]:
        rows = read_csv_rows(AUTO / "leads" / "qualified" / csv_name)
        is_hot = "HOT" in csv_name
        for r in rows:
            src = r.get("source", r.get("lead_source", "unknown"))
            sources[src]["count"] += 1
            if is_hot:
                sources[src]["hot"] += 1
            else:
                sources[src]["warm"] += 1

    result = {}
    for src, data in sources.items():
        total = data["count"]
        hot_pct = (data["hot"] / total * 100) if total > 0 else 0
        # Score: volume * quality
        score = min(100, int(total / 10 + hot_pct))
        result[src] = {
            "lead_count": total,
            "hot_count": data["hot"],
            "hot_pct": round(hot_pct, 1),
            "lead_score": score,
        }
    return result


def collect_pipeline_metrics():
    """Read pipeline_metrics.jsonl for recent performance."""
    path = AUTO / "leads" / "qualified" / "pipeline_metrics.jsonl"
    entries = read_jsonl(path)
    if not entries:
        return {}

    # Last 7 entries
    recent = entries[-7:]
    total_analyzed = sum(safe_float(e.get("analyzed", 0)) for e in recent)
    total_hot = sum(safe_float(e.get("hot", 0)) for e in recent)
    avg_rate = (total_hot / total_analyzed * 100) if total_analyzed > 0 else 0

    return {
        "pipeline": {
            "analyzed_7d": int(total_analyzed),
            "hot_7d": int(total_hot),
            "hot_rate": round(avg_rate, 2),
            "cycles_7d": len(recent),
        }
    }


# ---------------------------------------------------------------------------
# Trend computation
# ---------------------------------------------------------------------------

def compute_trends():
    """Read rebalance_history.jsonl, compute 7-day score trend per method.

    Returns dict of {method: trend_value} where trend ranges roughly -50 to +50.
    Positive = improving, negative = declining.
    """
    entries = read_jsonl(HISTORY_FILE)
    if len(entries) < 2:
        return {}

    # Only use last 14 entries (roughly 2 weeks at 1/day)
    entries = entries[-14:]

    # Split into older half and recent half
    mid = len(entries) // 2
    older = entries[:mid]
    recent = entries[mid:]

    # Average scores per method for each half
    def avg_scores(subset):
        totals = defaultdict(list)
        for e in subset:
            for method, score in e.get("scores", {}).items():
                totals[method].append(safe_float(score, 50))
        return {m: sum(vals) / len(vals) for m, vals in totals.items()}

    old_avg = avg_scores(older)
    new_avg = avg_scores(recent)

    trends = {}
    all_methods = set(old_avg.keys()) | set(new_avg.keys())
    for method in all_methods:
        old_val = old_avg.get(method, 50)
        new_val = new_avg.get(method, 50)
        # Clamp to -50..+50
        trends[method] = max(-50, min(50, new_val - old_val))

    return trends


# ---------------------------------------------------------------------------
# Scoring engine
# ---------------------------------------------------------------------------

def score_all():
    """Aggregate all data sources into unified method scores."""
    ventures = collect_venture_scores()
    overnight = collect_overnight_health()
    leads = collect_lead_source_scores()
    pipeline = collect_pipeline_metrics()
    trends = compute_trends()

    # Merge into unified method list
    all_methods = set()
    all_methods.update(ventures.keys())
    all_methods.update(overnight.keys())

    results = []
    for method in sorted(all_methods):
        v = ventures.get(method, {})
        o = overnight.get(method, {})

        # Composite score: venture (40%) + overnight health (30%) + trend (30%)
        v_score = v.get("venture_score", 50)
        o_rate = o.get("success_rate", 100)  # default 100 if not in overnight runner
        # Trend from history: positive if improving, negative if declining
        trend = trends.get(method, 0)

        composite = int(v_score * 0.4 + o_rate * 0.3 + (50 + trend) * 0.3)
        composite = max(0, min(100, composite))

        # Action recommendation
        if composite >= 70:
            action = "DOUBLE_DOWN"
        elif composite >= 40:
            action = "MAINTAIN"
        elif composite >= 20:
            action = "REDUCE"
        else:
            action = "KILL"

        results.append({
            "method": method,
            "score": composite,
            "action": action,
            "venture_score": v.get("venture_score", "-"),
            "success_rate": o.get("success_rate", "-"),
            "runs_7d": o.get("runs_7d", 0),
            "fails_7d": o.get("fails_7d", 0),
            "recommendation": v.get("recommendation", "-"),
        })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_check():
    results = score_all()
    now = datetime.now()

    print("=" * 70)
    print(f"PRINTMAXX REBALANCER — {now.strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    print()
    print(f"{'METHOD':<35} {'SCORE':>5} {'ACTION':<12} {'SUCCESS%':>8} {'7D RUNS':>7}")
    print("-" * 70)

    kill_count = 0
    double_count = 0
    for r in results:
        score = r["score"]
        action = r["action"]
        sr = r["success_rate"]
        sr_str = f"{sr}%" if sr != "-" else "-"

        # Color hint
        tag = ""
        if action == "KILL":
            tag = " !!!"
            kill_count += 1
        elif action == "DOUBLE_DOWN":
            tag = " +++"
            double_count += 1

        print(f"{r['method']:<35} {score:>5} {action:<12} {sr_str:>8} {r['runs_7d']:>7}{tag}")

    print("-" * 70)
    print(f"TOTAL: {len(results)} methods | {double_count} DOUBLE_DOWN | {kill_count} KILL")
    print()

    # Save latest
    try:
        LATEST_FILE.write_text(json.dumps(results, indent=2, default=str))
    except Exception:
        pass

    # Append to history
    entry = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "methods": len(results),
        "kills": kill_count,
        "doubles": double_count,
        "scores": {r["method"]: r["score"] for r in results},
    }
    try:
        with open(HISTORY_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass

    return results


def cmd_rebalance():
    results = cmd_check()
    print()
    print("REBALANCE ACTIONS:")
    print()

    actions_taken = 0
    for r in results:
        if r["action"] == "KILL" and r["runs_7d"] >= 5 and r["fails_7d"] >= 4:
            # Auto-disable: script failed 80%+ over a week
            print(f"  AUTO-DISABLE: {r['method']} (failed {r['fails_7d']}/{r['runs_7d']} last 7d)")
            # Write checkpoint for human review
            cp = CHECKPOINTS / f"KILL_{r['method'].replace(' ', '_')}.md"
            content = (
                f"# Kill Method: {r['method']}\n\n"
                f"Score: {r['score']}/100\n"
                f"Success rate: {r['success_rate']}%\n"
                f"Runs last 7 days: {r['runs_7d']}\n"
                f"Failures: {r['fails_7d']}\n\n"
                f"**Recommendation:** Disable in overnight_master_runner.sh\n"
                f"**Reason:** Consistently failing, wasting runtime\n\n"
                f"Approve by moving this file to OPS/checkpoints/approved/\n"
            )
            try:
                cp.write_text(content)
                actions_taken += 1
            except Exception:
                pass

        elif r["action"] == "DOUBLE_DOWN" and r["score"] >= 80:
            print(f"  PRIORITY UP: {r['method']} (score {r['score']})")
            actions_taken += 1

    if actions_taken == 0:
        print("  No automated actions needed. System balanced.")


def cmd_history():
    entries = read_jsonl(HISTORY_FILE)
    if not entries:
        print("No rebalance history yet. Run --check first.")
        return

    print(f"REBALANCE HISTORY ({len(entries)} entries)")
    print()
    print(f"{'DATE':<12} {'METHODS':>7} {'DOUBLES':>7} {'KILLS':>5}")
    print("-" * 35)
    for e in entries[-14:]:  # Last 2 weeks
        print(f"{e['date']:<12} {e['methods']:>7} {e['doubles']:>7} {e['kills']:>5}")


def cmd_kill(method):
    cp = CHECKPOINTS / f"KILL_{method.replace(' ', '_')}.md"
    content = (
        f"# Kill Method: {method}\n\n"
        f"Manually flagged for decommission at {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"Approve by moving this file to OPS/checkpoints/approved/\n"
    )
    cp.write_text(content)
    print(f"Checkpoint created: {cp}")
    print("Human must approve by moving to OPS/checkpoints/approved/")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="PRINTMAXX Auto-Rebalancer")
    p.add_argument("--check", action="store_true", help="Score all methods")
    p.add_argument("--rebalance", action="store_true", help="Auto-adjust")
    p.add_argument("--history", action="store_true", help="Show score trend")
    p.add_argument("--kill", metavar="METHOD", help="Flag method for kill")
    args = p.parse_args()

    if args.check:
        cmd_check()
    elif args.rebalance:
        cmd_rebalance()
    elif args.history:
        cmd_history()
    elif args.kill:
        cmd_kill(args.kill)
    else:
        cmd_check()
