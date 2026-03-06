#!/usr/bin/env python3
"""
AUTONOMOUS MONEY PRINTER v2 — 24/7 Master Orchestration Layer
═══════════════════════════════════════════════════════════════

This is the BRAIN that ties every PRINTMAXX system together into a single
autonomous loop. It doesn't just run scripts — it makes DECISIONS:

  1. What to prioritize based on current scores and data
  2. When to kill losing methods and double down on winners
  3. How to allocate effort across 30+ revenue methods
  4. When something is quality enough to ship vs needs more work
  5. What new opportunities to pursue vs ignore

Runs via cron every 2 hours. Each run:
  - Gathers system state from ALL sources
  - Scores all methods and opportunities
  - Identifies highest-ROI actions
  - Executes what it can autonomously
  - Queues what needs human input
  - Logs everything for continuous improvement

Usage:
  python3 AUTOMATIONS/autonomous_money_printer.py --cycle      # Full autonomous cycle
  python3 AUTOMATIONS/autonomous_money_printer.py --status     # System status
  python3 AUTOMATIONS/autonomous_money_printer.py --priorities # Top 20 priorities
  python3 AUTOMATIONS/autonomous_money_printer.py --execute    # Execute top priority
  python3 AUTOMATIONS/autonomous_money_printer.py --report     # Generate daily report
  python3 AUTOMATIONS/autonomous_money_printer.py --api-json   # JSON for webapp
"""

import json
import csv
import os
import sys
import subprocess
import hashlib
import time
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# ── paths ────────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent
AUTO = BASE / "AUTOMATIONS"
OPS  = BASE / "OPS"
LEDGER = BASE / "LEDGER"
LOGS = AUTO / "logs"
CONTENT = BASE / "CONTENT"
PRODUCTS = BASE / "PRODUCTS"
FINANCIALS = BASE / "FINANCIALS"

# Safety: verify we're in project root
def safe_path(p):
    resolved = Path(p).resolve()
    if not str(resolved).startswith(str(BASE)):
        raise ValueError(f"BLOCKED: {resolved} outside project root")
    return resolved

# ── system state gathering ───────────────────────────────────────────────────

def gather_system_state():
    """Gather comprehensive system state from ALL sources."""
    state = {
        "timestamp": datetime.now().isoformat(),
        "disk_usage_pct": _get_disk_usage(),
        "revenue": _get_revenue(),
        "accounts": _get_account_status(),
        "methods": _get_method_scores(),
        "leads": _get_lead_pipeline(),
        "content": _get_content_status(),
        "alpha": _get_alpha_status(),
        "apps": _get_app_status(),
        "cron": _get_cron_health(),
        "discovery": _get_discovery_opportunities(),
        "blockers": _get_blockers(),
        "recent_logs": _get_recent_log_entries(),
        "community_intel": _get_community_intel(),
        "products": _get_product_status(),
    }
    return state

def _get_disk_usage():
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        return round(used / total * 100, 1)
    except Exception:
        return 0

def _get_revenue():
    rev_file = FINANCIALS / "REVENUE_TRACKER.csv"
    total = 0.0
    transactions = []
    if rev_file.exists():
        try:
            with open(rev_file) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    amt = 0
                    for key in ["amount", "revenue", "total"]:
                        if key in row and row[key]:
                            try:
                                amt = float(row[key].replace("$", "").replace(",", ""))
                                break
                            except ValueError:
                                pass
                    total += amt
                    transactions.append(row)
        except Exception:
            pass
    return {"total": total, "transaction_count": len(transactions)}

def _get_account_status():
    accounts_file = LEDGER / "ACCOUNTS.csv"
    total = 0
    active = 0
    by_platform = defaultdict(int)
    if accounts_file.exists():
        try:
            with open(accounts_file) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total += 1
                    status = row.get("status", "").lower()
                    if status in ["active", "created", "live"]:
                        active += 1
                    platform = row.get("platform", "unknown")
                    by_platform[platform] += 1
        except Exception:
            pass
    return {"total": total, "active": active, "by_platform": dict(by_platform)}

def _get_method_scores():
    """Get scores from money_printer_engine."""
    try:
        sys.path.insert(0, str(AUTO))
        from money_printer_engine import rank_all_methods, METHODS_REGISTRY
        ranked = rank_all_methods()
        return {
            "total": len(METHODS_REGISTRY),
            "ranked": ranked[:10],
            "top_method": ranked[0] if ranked else None,
            "deployed": sum(1 for m in METHODS_REGISTRY.values() if m.get("status") == "DEPLOYED"),
            "ready": sum(1 for m in METHODS_REGISTRY.values() if m.get("status") == "READY"),
            "building": sum(1 for m in METHODS_REGISTRY.values() if m.get("status") == "BUILDING"),
        }
    except Exception as e:
        return {"error": str(e)}

def _get_lead_pipeline():
    result = {"hot": 0, "warm": 0, "total_analyzed": 0, "emails_ready": 0}
    hot_file = AUTO / "leads" / "qualified" / "HOT_LEADS_QUALIFIED.csv"
    warm_file = AUTO / "leads" / "qualified" / "WARM_LEADS_QUALIFIED.csv"
    analyzed_file = AUTO / "leads" / "qualified" / "ANALYZED_LEADS.csv"
    email_file = AUTO / "outreach" / "HOT_BATCH_FEB13.csv"

    for fpath, key in [(hot_file, "hot"), (warm_file, "warm"), (analyzed_file, "total_analyzed")]:
        if fpath.exists():
            try:
                with open(fpath) as f:
                    result[key] = sum(1 for _ in f) - 1  # minus header
            except Exception:
                pass

    if email_file.exists():
        try:
            with open(email_file) as f:
                result["emails_ready"] = sum(1 for _ in f) - 1
        except Exception:
            pass

    return result

def _get_content_status():
    result = {"total_files": 0, "pending_review": 0, "by_niche": defaultdict(int)}
    social_dir = CONTENT / "social"
    if social_dir.exists():
        for f in social_dir.rglob("*"):
            if f.is_file() and f.suffix in [".md", ".csv"]:
                result["total_files"] += 1
                niche = f.parent.name
                result["by_niche"][niche] += 1

    qa_dir = OPS / "CONTENT_QA_QUEUE"
    if qa_dir.exists():
        result["pending_review"] = sum(1 for f in qa_dir.iterdir() if f.is_file())

    result["by_niche"] = dict(result["by_niche"])
    return result

def _get_alpha_status():
    alpha_file = LEDGER / "ALPHA_STAGING.csv"
    result = {"total": 0, "pending": 0, "approved": 0, "categories": defaultdict(int)}
    if alpha_file.exists():
        try:
            with open(alpha_file) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    result["total"] += 1
                    status = row.get("status", "").upper()
                    if "PENDING" in status:
                        result["pending"] += 1
                    elif "APPROVED" in status:
                        result["approved"] += 1
                    cat = row.get("category", "unknown")
                    result["categories"][cat] += 1
        except Exception:
            pass
    result["categories"] = dict(result["categories"])
    return result

def _get_app_status():
    apps = {}
    app_dirs = [
        BASE / "ralph" / "loops" / "app_factory" / "output",
        BASE / "MONEY_METHODS" / "APP_FACTORY" / "builds",
    ]
    for app_dir in app_dirs:
        if app_dir.exists():
            for d in app_dir.iterdir():
                if d.is_dir() and not d.name.startswith("."):
                    apps[d.name] = {
                        "path": str(d),
                        "has_index": (d / "index.html").exists(),
                        "has_package": (d / "package.json").exists(),
                        "file_count": sum(1 for _ in d.rglob("*") if _.is_file()),
                    }
    return apps

def _get_cron_health():
    cron_file = AUTO / "crontab_printmaxx_v2.txt"
    result = {"total_jobs": 0, "recent_logs": []}
    if cron_file.exists():
        try:
            text = cron_file.read_text()
            result["total_jobs"] = sum(1 for line in text.splitlines()
                                       if line.strip() and not line.strip().startswith("#")
                                       and "*" in line)
        except Exception:
            pass

    # Check recent log files
    if LOGS.exists():
        log_files = sorted(LOGS.glob("*.log"), key=lambda f: f.stat().st_mtime, reverse=True)
        for lf in log_files[:10]:
            try:
                mtime = datetime.fromtimestamp(lf.stat().st_mtime)
                size = lf.stat().st_size
                result["recent_logs"].append({
                    "name": lf.name,
                    "modified": mtime.isoformat(),
                    "size_kb": round(size / 1024, 1),
                    "age_hours": round((datetime.now() - mtime).total_seconds() / 3600, 1),
                })
            except Exception:
                pass

    return result

def _get_discovery_opportunities():
    discovery_dir = OPS / "discovery"
    result = {"total": 0, "files": []}
    if discovery_dir.exists():
        for f in sorted(discovery_dir.iterdir()):
            if f.is_file():
                result["total"] += 1
                result["files"].append(f.name)
    return result

def _get_blockers():
    blockers = []

    # Account blocker
    accounts = _get_account_status()
    if accounts["active"] == 0:
        blockers.append({
            "severity": "CRITICAL",
            "type": "ACCOUNTS",
            "description": f"0 active accounts. Total registered: {accounts['total']}. "
                          "Cannot generate revenue without platform accounts.",
            "fix": "Open OPS/ACCOUNT_CREATION_NOW.md and create Stripe→Gumroad→Fiverr in order."
        })

    # Email infra blocker
    rev = _get_revenue()
    leads = _get_lead_pipeline()
    if leads["hot"] > 100 and leads["emails_ready"] > 0 and rev["total"] == 0:
        blockers.append({
            "severity": "HIGH",
            "type": "EMAIL_INFRA",
            "description": f"{leads['hot']} hot leads, {leads['emails_ready']} emails ready, "
                          "$0 sent. Need email sending infrastructure.",
            "fix": "Set up Instantly.ai or Smartlead for cold email sending."
        })

    # Disk space
    disk = _get_disk_usage()
    if disk > 95:
        blockers.append({
            "severity": "HIGH",
            "type": "DISK_SPACE",
            "description": f"Disk at {disk}%. Risk of cron job failures.",
            "fix": "Clean AUTOMATIONS/logs/ old files and node_modules in unused projects."
        })

    # Content not posted
    content = _get_content_status()
    if content["total_files"] > 100:
        blockers.append({
            "severity": "MEDIUM",
            "type": "CONTENT_UNPOSTED",
            "description": f"{content['total_files']} content files, 0 posted. "
                          "Content sitting idle = wasted alpha.",
            "fix": "Create social accounts and start posting. Use Buffer/Publer for scheduling."
        })

    # Alpha backlog
    alpha = _get_alpha_status()
    if alpha["pending"] > 50:
        blockers.append({
            "severity": "MEDIUM",
            "type": "ALPHA_BACKLOG",
            "description": f"{alpha['pending']} alpha entries pending review. "
                          "Unprocessed alpha = missed opportunities.",
            "fix": "Run: python3 AUTOMATIONS/alpha_auto_processor.py --process-new"
        })

    return blockers

def _get_recent_log_entries():
    """Get the last significant log entries for context."""
    entries = []
    daily_dir = LOGS / "daily"
    if daily_dir.exists():
        logs = sorted(daily_dir.glob("*.md"), reverse=True)
        if logs:
            try:
                text = logs[0].read_text()
                lines = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]
                entries = lines[-10:]  # last 10 entries
            except Exception:
                pass
    return entries

def _get_community_intel():
    intel_file = LEDGER / "COMMUNITY_INTEL.csv"
    result = {"total_signals": 0, "high_score": 0, "recent": []}
    if intel_file.exists():
        try:
            with open(intel_file) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    result["total_signals"] += 1
                    score = int(row.get("score", 0))
                    if score >= 75:
                        result["high_score"] += 1
        except Exception:
            pass
    return result

def _get_product_status():
    result = {"gumroad_ready": 0, "fiverr_ready": 0, "etsy_ready": 0, "total_listings": 0}

    gumroad_dir = PRODUCTS / "GUMROAD_INSTANT_UPLOAD"
    if gumroad_dir.exists():
        result["gumroad_ready"] = sum(1 for f in gumroad_dir.iterdir() if f.is_file())

    fiverr_dir = PRODUCTS / "FIVERR_INSTANT_UPLOAD"
    if fiverr_dir.exists():
        result["fiverr_ready"] = sum(1 for f in fiverr_dir.iterdir() if f.is_file())

    for d in PRODUCTS.iterdir():
        if d.is_file() and d.suffix == ".md":
            result["total_listings"] += 1

    return result


# ── priority generation ──────────────────────────────────────────────────────

PRIORITY_RULES = [
    # (condition_func, priority_score, action_description, execution_cmd)
    # Higher score = more urgent
]

def generate_priorities(state):
    """Generate ranked priority list based on current system state."""
    priorities = []

    # 1. CRITICAL: Account creation (blocks ALL revenue)
    if state["accounts"]["active"] == 0:
        priorities.append({
            "score": 100,
            "category": "ACCOUNTS",
            "action": "Create platform accounts: Stripe → Gumroad → Fiverr → Upwork",
            "type": "HUMAN_REQUIRED",
            "impact": "Unblocks ALL revenue streams. Currently $0 because 0 accounts.",
            "time_estimate": "30 min per account",
        })

    # 2. HIGH: List products on existing platforms
    products = state["products"]
    if products["gumroad_ready"] > 0:
        priorities.append({
            "score": 95,
            "category": "PRODUCTS",
            "action": f"Upload {products['gumroad_ready']} products to Gumroad",
            "type": "HUMAN_REQUIRED",
            "impact": f"{products['gumroad_ready']} products ready to list. Each could generate $10-500/mo.",
            "time_estimate": "5 min per product",
        })

    # 3. HIGH: Process alpha backlog
    if state["alpha"]["pending"] > 20:
        priorities.append({
            "score": 88,
            "category": "ALPHA",
            "action": f"Process {state['alpha']['pending']} pending alpha entries",
            "type": "AUTOMATED",
            "cmd": "python3 AUTOMATIONS/alpha_auto_processor.py --process-new",
            "impact": "Each approved alpha could unlock new revenue path.",
        })

    # 4. HIGH: Send cold emails
    leads = state["leads"]
    if leads["emails_ready"] > 0 and leads["hot"] > 50:
        priorities.append({
            "score": 85,
            "category": "OUTREACH",
            "action": f"Send {leads['emails_ready']} cold emails to {leads['hot']} hot leads",
            "type": "NEEDS_INFRA",
            "impact": "At 3% reply rate = potential $2-5K/mo in service revenue.",
        })

    # 5. MEDIUM: Post content to social
    content = state["content"]
    if content["total_files"] > 50:
        priorities.append({
            "score": 75,
            "category": "CONTENT",
            "action": f"Post content from {content['total_files']} files across social accounts",
            "type": "NEEDS_ACCOUNTS",
            "impact": "Content sitting idle = 0 distribution. Each post compounds.",
        })

    # 6. MEDIUM: Deploy apps to stores
    apps = state["apps"]
    deployable = [name for name, info in apps.items() if info.get("has_index")]
    if deployable:
        priorities.append({
            "score": 72,
            "category": "APPS",
            "action": f"Submit {len(deployable)} apps to App Store/directories",
            "type": "NEEDS_ACCOUNTS",
            "impact": "Each app on App Store = passive revenue potential.",
        })

    # 7. MEDIUM: Run discovery scan
    priorities.append({
        "score": 65,
        "category": "DISCOVERY",
        "action": "Run full discovery scan for new revenue opportunities",
        "type": "AUTOMATED",
        "cmd": "python3 AUTOMATIONS/agentic_discovery.py --discover",
        "impact": "Identifies cross-pollination, seasonal, underserved market opportunities.",
    })

    # 8. Run community intel scan
    priorities.append({
        "score": 62,
        "category": "INTEL",
        "action": "Scan communities for latest tactics and platform changes",
        "type": "AUTOMATED",
        "cmd": "python3 AUTOMATIONS/community_intel_scanner.py --scan",
        "impact": "Surfaces real-time intel from 25+ communities.",
    })

    # 9. Run quality gate
    priorities.append({
        "score": 58,
        "category": "QUALITY",
        "action": "Score all outputs and block sub-par content from shipping",
        "type": "AUTOMATED",
        "cmd": "python3 AUTOMATIONS/quality_gate.py --score-all",
        "impact": "Prevents AI slop from reaching audience. Protects brand.",
    })

    # 10. Edge growth squeeze
    priorities.append({
        "score": 55,
        "category": "GROWTH",
        "action": "Run edge growth analysis to find missed revenue in existing content",
        "type": "AUTOMATED",
        "cmd": "python3 AUTOMATIONS/edge_growth_engine.py --squeeze",
        "impact": "Finds affiliate gaps, content multiplication opportunities.",
    })

    # 11. Run money printer cycle
    methods = state.get("methods", {})
    if isinstance(methods, dict) and "total" in methods:
        priorities.append({
            "score": 70,
            "category": "MONEY_PRINTER",
            "action": f"Run money printer cycle across {methods.get('total', 21)} methods",
            "type": "AUTOMATED",
            "cmd": "python3 AUTOMATIONS/money_printer_engine.py --cycle",
            "impact": "Scores, ranks, and optimizes all revenue methods.",
        })

    # 12. Market scanner
    priorities.append({
        "score": 50,
        "category": "MARKETS",
        "action": "Scan prediction markets, crypto, and options for opportunities",
        "type": "AUTOMATED",
        "cmd": "python3 AUTOMATIONS/market_scanner.py --scan-polymarket --scan-crypto",
        "impact": "Identifies trading/prediction market edge opportunities.",
    })

    # 13. Monetization optimization
    priorities.append({
        "score": 60,
        "category": "MONETIZATION",
        "action": "Optimize monetization across all apps",
        "type": "AUTOMATED",
        "cmd": "python3 AUTOMATIONS/monetization_engine.py --all",
        "impact": "Ensures optimal pricing, paywall, and affiliate integration.",
    })

    # 14. iOS pre-screening
    if apps:
        priorities.append({
            "score": 55,
            "category": "IOS",
            "action": "Screen all apps for iOS rejection risks",
            "type": "AUTOMATED",
            "cmd": f"python3 AUTOMATIONS/ios_rejection_screener.py --check {next(iter(apps.values()), {}).get('path', '.')}",
            "impact": "Prevents costly App Store rejections.",
        })

    # 15. Algo ban prevention check
    priorities.append({
        "score": 52,
        "category": "SAFETY",
        "action": "Check all accounts for algo ban risk",
        "type": "AUTOMATED",
        "cmd": "python3 AUTOMATIONS/algo_ban_prevention.py --health",
        "impact": "Prevents shadowbans and account restrictions.",
    })

    # 16. Freelance demand scan
    priorities.append({
        "score": 68,
        "category": "FREELANCE",
        "action": "Scan Reddit for active hiring posts matching our services",
        "type": "AUTOMATED",
        "cmd": "python3 AUTOMATIONS/freelance_demand_scanner.py --scan",
        "impact": "Find $100-5000 freelance gigs we can fulfill with AI.",
    })

    # 17. Ecom arb scan
    priorities.append({
        "score": 63,
        "category": "ECOM",
        "action": "Scan for ecom arbitrage opportunities",
        "type": "AUTOMATED",
        "cmd": "python3 AUTOMATIONS/ecom_arb_engine.py --scan --top 10",
        "impact": "Find products to flip for 30-60% margins.",
    })

    # 18. Creative sourcing refresh
    priorities.append({
        "score": 48,
        "category": "CREATIVE",
        "action": "Refresh creative sourcing database (hooks, sounds, ad formats)",
        "type": "AUTOMATED",
        "cmd": "python3 AUTOMATIONS/creative_sourcer.py --all-niches --swipe-file",
        "impact": "Keeps content fresh with latest trending formats.",
    })

    # 19. Compliance scan
    priorities.append({
        "score": 57,
        "category": "COMPLIANCE",
        "action": "Scan all content for compliance issues",
        "type": "AUTOMATED",
        "cmd": "python3 AUTOMATIONS/compliance_scanner.py --audit-all",
        "impact": "Prevents FTC fines, CAN-SPAM violations, income claim issues.",
    })

    # 20. Trend aggregation
    priorities.append({
        "score": 53,
        "category": "TRENDS",
        "action": "Aggregate trends across Google, Reddit, Product Hunt",
        "type": "AUTOMATED",
        "cmd": "python3 AUTOMATIONS/trend_aggregator.py --scan",
        "impact": "Catch trending products/topics for content and listings.",
    })

    # Sort by score descending
    priorities.sort(key=lambda x: x["score"], reverse=True)
    return priorities


# ── autonomous execution ─────────────────────────────────────────────────────

def execute_automated_priorities(state, max_tasks=5, dry_run=False):
    """Execute top automated priorities."""
    priorities = generate_priorities(state)
    automated = [p for p in priorities if p.get("type") == "AUTOMATED" and p.get("cmd")]

    results = []
    executed = 0

    for priority in automated[:max_tasks]:
        cmd = priority["cmd"]
        category = priority["category"]

        if dry_run:
            results.append({
                "category": category,
                "cmd": cmd,
                "status": "DRY_RUN",
                "action": priority["action"],
            })
            continue

        print(f"\n  [{category}] Executing: {priority['action']}")
        print(f"  CMD: {cmd}")

        try:
            proc = subprocess.run(
                cmd.split(),
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(BASE),
            )

            output = proc.stdout[-500:] if proc.stdout else ""
            error = proc.stderr[-200:] if proc.stderr else ""
            success = proc.returncode == 0

            results.append({
                "category": category,
                "cmd": cmd,
                "status": "SUCCESS" if success else "FAILED",
                "output_tail": output,
                "error_tail": error if not success else "",
                "action": priority["action"],
            })

            if success:
                executed += 1
                print(f"  ✓ Success")
            else:
                print(f"  ✗ Failed: {error[:100]}")

        except subprocess.TimeoutExpired:
            results.append({
                "category": category,
                "cmd": cmd,
                "status": "TIMEOUT",
                "action": priority["action"],
            })
            print(f"  ⏱ Timeout (300s)")
        except Exception as e:
            results.append({
                "category": category,
                "cmd": cmd,
                "status": "ERROR",
                "error": str(e),
                "action": priority["action"],
            })
            print(f"  ✗ Error: {e}")

    return {"executed": executed, "total_attempted": len(results), "results": results}


# ── full cycle ───────────────────────────────────────────────────────────────

def run_full_cycle(max_tasks=5, dry_run=False):
    """Run a full autonomous money printer cycle."""
    print("=" * 70)
    print("  AUTONOMOUS MONEY PRINTER — FULL CYCLE")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')} | Max tasks: {max_tasks}")
    print("=" * 70)

    # Phase 1: Gather state
    print("\n  PHASE 1: Gathering system state...")
    state = gather_system_state()

    print(f"  Revenue: ${state['revenue']['total']:.2f}")
    print(f"  Accounts: {state['accounts']['active']} active / {state['accounts']['total']} total")
    print(f"  Leads: {state['leads']['hot']} hot, {state['leads']['warm']} warm")
    print(f"  Alpha: {state['alpha']['total']} total, {state['alpha']['pending']} pending")
    print(f"  Methods: {state['methods'].get('total', '?')} tracked")
    print(f"  Disk: {state['disk_usage_pct']}%")
    print(f"  Blockers: {len(state['blockers'])}")

    # Phase 2: Generate priorities
    print("\n  PHASE 2: Generating priorities...")
    priorities = generate_priorities(state)

    print(f"  Top 5 priorities:")
    for i, p in enumerate(priorities[:5], 1):
        status_icon = "🤖" if p["type"] == "AUTOMATED" else "👤"
        print(f"    {i}. [{p['score']}] {p['category']}: {p['action'][:60]} {status_icon}")

    # Phase 3: Execute automated tasks
    print(f"\n  PHASE 3: Executing top {max_tasks} automated tasks...")
    exec_result = execute_automated_priorities(state, max_tasks=max_tasks, dry_run=dry_run)

    print(f"\n  Executed: {exec_result['executed']}/{exec_result['total_attempted']}")

    # Phase 4: Log results
    print("\n  PHASE 4: Logging results...")
    log_cycle_results(state, priorities, exec_result)

    # Phase 5: Generate human action items
    human_items = [p for p in priorities if p["type"] in ["HUMAN_REQUIRED", "NEEDS_ACCOUNTS", "NEEDS_INFRA"]]
    if human_items:
        print(f"\n  HUMAN ACTIONS NEEDED ({len(human_items)}):")
        for item in human_items[:5]:
            print(f"    [{item['score']}] {item['action'][:70]}")

    print("\n" + "=" * 70)
    return {
        "state": state,
        "priorities": priorities,
        "execution": exec_result,
        "human_items": human_items,
    }


def log_cycle_results(state, priorities, exec_result):
    """Log cycle results for continuous improvement."""
    log_dir = LOGS / "money_printer"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"cycle_{datetime.now().strftime('%Y%m%d_%H%M')}.json"

    # Simplify state for JSON serialization
    serializable_state = {
        "timestamp": state["timestamp"],
        "disk_usage_pct": state["disk_usage_pct"],
        "revenue_total": state["revenue"]["total"],
        "accounts_active": state["accounts"]["active"],
        "leads_hot": state["leads"]["hot"],
        "alpha_pending": state["alpha"]["pending"],
        "blockers_count": len(state["blockers"]),
    }

    log_data = {
        "state_summary": serializable_state,
        "top_5_priorities": [
            {"score": p["score"], "category": p["category"], "action": p["action"]}
            for p in priorities[:5]
        ],
        "execution_summary": {
            "executed": exec_result["executed"],
            "attempted": exec_result["total_attempted"],
        },
    }

    try:
        safe_path(log_file)
        log_file.write_text(json.dumps(log_data, indent=2))
    except Exception as e:
        print(f"  Warning: Could not save log: {e}")

    # Also append to JSONL for trend analysis
    jsonl_file = LOGS / "money_printer_cycles.jsonl"
    try:
        safe_path(jsonl_file)
        with open(jsonl_file, "a") as f:
            f.write(json.dumps(log_data) + "\n")
    except Exception:
        pass


# ── reporting ────────────────────────────────────────────────────────────────

def generate_daily_report():
    """Generate comprehensive daily report."""
    state = gather_system_state()
    priorities = generate_priorities(state)

    report = []
    report.append("# AUTONOMOUS MONEY PRINTER — DAILY REPORT")
    report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")

    # Revenue
    report.append("## Revenue")
    report.append(f"- Total: ${state['revenue']['total']:.2f}")
    report.append(f"- Transactions: {state['revenue']['transaction_count']}")
    report.append("")

    # System health
    report.append("## System Health")
    report.append(f"- Disk: {state['disk_usage_pct']}%")
    report.append(f"- Cron jobs: {state['cron']['total_jobs']} active")
    report.append(f"- Accounts: {state['accounts']['active']}/{state['accounts']['total']}")
    report.append("")

    # Pipeline
    report.append("## Lead Pipeline")
    leads = state["leads"]
    report.append(f"- Hot leads: {leads['hot']}")
    report.append(f"- Warm leads: {leads['warm']}")
    report.append(f"- Total analyzed: {leads['total_analyzed']}")
    report.append(f"- Emails ready: {leads['emails_ready']}")
    report.append("")

    # Methods
    methods = state["methods"]
    if isinstance(methods, dict) and "ranked" in methods:
        report.append("## Top Revenue Methods")
        for m in methods["ranked"][:5]:
            if isinstance(m, dict):
                report.append(f"- [{m.get('score', 0):.0f}] {m.get('name', 'unknown')} — {m.get('status', '?')}")
            elif isinstance(m, (list, tuple)) and len(m) >= 3:
                report.append(f"- [{m[1]:.0f}] {m[0]} — {m[2]}")
        report.append("")

    # Blockers
    report.append("## Blockers")
    for b in state["blockers"]:
        report.append(f"- **[{b['severity']}]** {b['description'][:80]}")
        report.append(f"  Fix: {b['fix'][:80]}")
    report.append("")

    # Top priorities
    report.append("## Top 10 Priorities")
    for i, p in enumerate(priorities[:10], 1):
        type_emoji = {"AUTOMATED": "🤖", "HUMAN_REQUIRED": "👤", "NEEDS_ACCOUNTS": "🔑", "NEEDS_INFRA": "🔧"}.get(p["type"], "?")
        report.append(f"{i}. [{p['score']}] {type_emoji} **{p['category']}**: {p['action']}")
    report.append("")

    # Alpha intel
    alpha = state["alpha"]
    report.append("## Alpha Intelligence")
    report.append(f"- Total entries: {alpha['total']}")
    report.append(f"- Pending review: {alpha['pending']}")
    report.append(f"- Approved: {alpha['approved']}")
    if alpha["categories"]:
        report.append("- Top categories:")
        sorted_cats = sorted(alpha["categories"].items(), key=lambda x: x[1], reverse=True)
        for cat, count in sorted_cats[:5]:
            report.append(f"  - {cat}: {count}")
    report.append("")

    # Discovery
    discovery = state["discovery"]
    report.append("## Discovery")
    report.append(f"- Total opportunities found: {discovery['total']}")
    report.append("")

    # Content
    content = state["content"]
    report.append("## Content")
    report.append(f"- Total files: {content['total_files']}")
    report.append(f"- Pending review: {content['pending_review']}")
    if content["by_niche"]:
        report.append("- By niche:")
        for niche, count in sorted(content["by_niche"].items(), key=lambda x: x[1], reverse=True)[:5]:
            report.append(f"  - {niche}: {count}")
    report.append("")

    # Recent cycle history
    jsonl_file = LOGS / "money_printer_cycles.jsonl"
    if jsonl_file.exists():
        try:
            lines = jsonl_file.read_text().strip().splitlines()
            recent = lines[-5:]
            report.append("## Recent Cycle History")
            for line in recent:
                data = json.loads(line)
                ts = data.get("state_summary", {}).get("timestamp", "?")
                executed = data.get("execution_summary", {}).get("executed", 0)
                report.append(f"- {ts}: {executed} tasks executed")
            report.append("")
        except Exception:
            pass

    report_text = "\n".join(report)

    # Save report
    report_dir = OPS / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"MONEY_PRINTER_REPORT_{datetime.now().strftime('%Y_%m_%d')}.md"
    try:
        safe_path(report_file)
        report_file.write_text(report_text)
        print(f"  Report saved: {report_file}")
    except Exception as e:
        print(f"  Warning: Could not save report: {e}")

    return report_text


# ── API JSON ─────────────────────────────────────────────────────────────────

def get_api_json():
    """Get full system state as JSON for webapp."""
    state = gather_system_state()
    priorities = generate_priorities(state)

    return {
        "timestamp": state["timestamp"],
        "revenue": state["revenue"],
        "accounts": state["accounts"],
        "methods": state["methods"] if not isinstance(state["methods"], dict) or "error" not in state["methods"] else {"error": state["methods"]["error"]},
        "leads": state["leads"],
        "content": state["content"],
        "alpha": state["alpha"],
        "blockers": state["blockers"],
        "discovery": state["discovery"],
        "products": state["products"],
        "priorities": [
            {
                "score": p["score"],
                "category": p["category"],
                "action": p["action"],
                "type": p["type"],
            }
            for p in priorities[:20]
        ],
        "disk_usage_pct": state["disk_usage_pct"],
        "cron_jobs": state["cron"]["total_jobs"],
    }


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Autonomous Money Printer v2")
    parser.add_argument("--cycle", action="store_true", help="Run full autonomous cycle")
    parser.add_argument("--status", action="store_true", help="System status overview")
    parser.add_argument("--priorities", action="store_true", help="Show top 20 priorities")
    parser.add_argument("--execute", action="store_true", help="Execute top automated priorities")
    parser.add_argument("--report", action="store_true", help="Generate daily report")
    parser.add_argument("--api-json", action="store_true", help="JSON for webapp")
    parser.add_argument("--dry-run", action="store_true", help="Don't actually execute tasks")
    parser.add_argument("--max-tasks", type=int, default=5, help="Max tasks to execute per cycle")

    args = parser.parse_args()

    if args.api_json:
        print(json.dumps(get_api_json(), indent=2, default=str))
    elif args.cycle:
        run_full_cycle(max_tasks=args.max_tasks, dry_run=args.dry_run)
    elif args.status:
        state = gather_system_state()
        print("=" * 70)
        print("  AUTONOMOUS MONEY PRINTER — STATUS")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("=" * 70)
        print(f"\n  Revenue: ${state['revenue']['total']:.2f} ({state['revenue']['transaction_count']} transactions)")
        print(f"  Accounts: {state['accounts']['active']} active / {state['accounts']['total']} total")
        print(f"  Disk: {state['disk_usage_pct']}%")
        print(f"  Cron: {state['cron']['total_jobs']} active jobs")
        print(f"  Leads: {state['leads']['hot']} hot | {state['leads']['warm']} warm | {state['leads']['emails_ready']} emails ready")
        print(f"  Alpha: {state['alpha']['total']} total | {state['alpha']['pending']} pending | {state['alpha']['approved']} approved")
        print(f"  Content: {state['content']['total_files']} files | {state['content']['pending_review']} pending review")
        print(f"  Apps: {len(state['apps'])} in pipeline")
        print(f"  Discovery: {state['discovery']['total']} opportunities")
        print(f"  Products: {state['products']['gumroad_ready']} Gumroad | {state['products']['fiverr_ready']} Fiverr ready")

        print(f"\n  BLOCKERS ({len(state['blockers'])}):")
        for b in state["blockers"]:
            print(f"    [{b['severity']}] {b['type']}: {b['description'][:70]}")

    elif args.priorities:
        state = gather_system_state()
        priorities = generate_priorities(state)
        print("=" * 70)
        print("  AUTONOMOUS MONEY PRINTER — TOP 20 PRIORITIES")
        print("=" * 70)
        for i, p in enumerate(priorities[:20], 1):
            type_icon = {"AUTOMATED": "AUTO", "HUMAN_REQUIRED": "HUMAN", "NEEDS_ACCOUNTS": "ACCTS", "NEEDS_INFRA": "INFRA"}.get(p["type"], "?")
            print(f"\n  {i:2d}. [{p['score']:3d}] {p['category']} ({type_icon})")
            print(f"      {p['action']}")
            if p.get("impact"):
                print(f"      Impact: {p['impact'][:70]}")
    elif args.execute:
        state = gather_system_state()
        execute_automated_priorities(state, max_tasks=args.max_tasks, dry_run=args.dry_run)
    elif args.report:
        report = generate_daily_report()
        print(report)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
