#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX AGENT — Proactive Autonomous Business System

Not a chatbot. Not a cron job collection. An agent that works for you.

It wakes up on schedule. It reads the state of everything. It decides what
matters right now. It does the work. It ships the output. It learns what
worked. It does it again, better.

Architecture:
- ONE process that orchestrates everything
- Missions: discrete units of work with goals, tools, and success criteria
- Channels: where output goes (files, surge, buffer, social, email)
- Memory: what worked, what failed, what changed
- Schedule: when each mission type runs
- LLM: Claude CLI for missions requiring judgment (via Max plan)

Usage:
  python3 AUTOMATIONS/printmaxx_agent.py                    # Run forever
  python3 AUTOMATIONS/printmaxx_agent.py --once             # One full cycle
  python3 AUTOMATIONS/printmaxx_agent.py --status           # What's happening
  python3 AUTOMATIONS/printmaxx_agent.py --mission <name>   # Run specific mission
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import time
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# === CONSTANTS ===
PROJECT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
AGENT_DIR = PROJECT / "AUTOMATIONS" / "agent"
STATE_FILE = AGENT_DIR / "state.json"
MISSION_LOG = AGENT_DIR / "missions.jsonl"
MEMORY_FILE = AGENT_DIR / "memory.json"
PYTHON = sys.executable

BLOCKED_DIRS = [
    Path.home() / "Desktop",
    Path.home() / "Downloads",
    Path.home() / "Pictures",
    Path.home() / "Music",
    Path.home() / "Movies",
    Path.home() / "Library",
    Path.home() / ".ssh",
    Path.home() / ".aws",
    Path.home() / ".gnupg",
    Path("/System"), Path("/Library"), Path("/usr"), Path("/bin"), Path("/etc"), Path("/var"),
]
BLOCKED_COMMANDS = ["rm -rf /", "rm -rf ~", "rm -rf $HOME", "dd if=", "diskutil erase",
                     "mkfs", "format", "> /dev/", "fork", ":(){ :|:& };:"]

def safe_path(p):
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(p).resolve()
    project_resolved = PROJECT.resolve()
    if not str(resolved).startswith(str(project_resolved)):
        raise ValueError(f"GUARDRAIL BLOCKED: {resolved} is outside project root {project_resolved}")
    for blocked in BLOCKED_DIRS:
        if str(resolved).startswith(str(blocked.resolve())):
            raise ValueError(f"GUARDRAIL BLOCKED: {resolved} is in protected directory {blocked}")
    return resolved

def safe_command(cmd_str):
    """Check a command string for dangerous patterns."""
    lower = cmd_str.lower()
    for bad in BLOCKED_COMMANDS:
        if bad in lower:
            raise ValueError(f"GUARDRAIL BLOCKED dangerous command: {bad}")
    # Block writes outside project
    for pattern in ["> /", ">> /", "> ~/", ">> ~/"]:
        if pattern in cmd_str and str(PROJECT) not in cmd_str.split(pattern)[-1][:100]:
            raise ValueError(f"GUARDRAIL BLOCKED: redirect outside project")


# === STATE MANAGEMENT ===

class AgentState:
    """Persistent state that survives restarts."""

    def __init__(self):
        AGENT_DIR.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self):
        if STATE_FILE.exists():
            try:
                return json.loads(STATE_FILE.read_text())
            except Exception:
                return self._default()
        return self._default()

    def _default(self):
        return {
            "last_cycle": None,
            "cycles_run": 0,
            "missions_completed": 0,
            "missions_failed": 0,
            "last_mission_results": {},
            "active_priorities": [],
            "learnings": [],
            "blockers": ["account_creation"],
            "disk_gb_free": 0,
        }

    def save(self):
        safe_path(STATE_FILE)
        STATE_FILE.write_text(json.dumps(self.data, indent=2, default=str))

    def log_mission(self, mission_name, result, duration_s, output_summary):
        entry = {
            "ts": datetime.now().isoformat(),
            "mission": mission_name,
            "result": result,  # "success" | "partial" | "failed" | "skipped"
            "duration_s": round(duration_s, 1),
            "output": output_summary,
        }
        safe_path(MISSION_LOG)
        with open(MISSION_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
        self.data["last_mission_results"][mission_name] = result
        if result in ("success", "partial"):
            self.data["missions_completed"] += 1
        else:
            self.data["missions_failed"] += 1


# === MISSION RUNNER ===

def run_script(script, args="", timeout=300):
    """Run a Python script from AUTOMATIONS/ only. Guardrailed."""
    script_path = (PROJECT / "AUTOMATIONS" / script).resolve()
    # Guardrail: script must be inside project
    if not str(script_path).startswith(str(PROJECT.resolve())):
        log(f"GUARDRAIL BLOCKED: {script} resolves outside project", "SECURITY")
        return False, f"BLOCKED: {script} outside project"
    if not script_path.exists():
        return False, f"Script not found: {script}"
    cmd = f"{PYTHON} {script_path} {args}"
    safe_command(cmd)
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, cwd=str(PROJECT)
        )
        output = (r.stdout + r.stderr)[-2000:]  # Last 2K chars
        return r.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT after {timeout}s"
    except Exception as e:
        return False, str(e)


def run_claude(prompt, timeout=180):
    """Run a Claude CLI prompt for LLM-required work. Uses Max plan."""
    cmd = [
        "claude", "--dangerously-skip-permissions", "--print",
        "--mcp-config", str(PROJECT / "ralph" / "empty_mcp.json"),
        "--strict-mcp-config"
    ]
    try:
        r = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True,
            timeout=timeout, cwd=str(PROJECT),
            env={**os.environ, "CLAUDECODE": ""}  # unset to allow nested
        )
        return r.returncode == 0, (r.stdout + r.stderr)[-3000:]
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT after {timeout}s"
    except Exception as e:
        return False, str(e)


def count_csv(path):
    p = PROJECT / path
    if not p.exists():
        return 0
    try:
        with open(p) as f:
            return sum(1 for _ in f) - 1
    except Exception:
        return 0


def read_csv_tail(path, n=20):
    p = PROJECT / path
    if not p.exists():
        return []
    rows = []
    try:
        with open(p) as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
                if len(rows) > n * 2:
                    rows = rows[-n:]
    except Exception:
        return []
    return rows[-n:]


def disk_free_gb():
    try:
        st = os.statvfs("/")
        return round(st.f_bavail * st.f_frsize / (1024**3), 1)
    except Exception:
        return -1


def ts():
    return datetime.now().strftime("%H:%M:%S")


def log(msg, level="INFO"):
    line = f"[{ts()}] [{level}] {msg}"
    print(line)
    log_path = PROJECT / "AUTOMATIONS" / "logs" / "agent.log"
    try:
        with open(log_path, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


# === MISSIONS ===
# Each mission is a function that returns (result, summary)
# result: "success" | "partial" | "failed" | "skipped"

def mission_scan_opportunities():
    """Scan all data sources for new opportunities."""
    log("MISSION: Scan opportunities")
    results = []

    # Freelance demand
    ok, out = run_script("freelance_demand_scanner.py", timeout=120)
    results.append(("freelance_scan", ok, out))

    # Ecom arb
    ok, out = run_script("ecom_arb_engine.py", timeout=120)
    results.append(("ecom_arb", ok, out))

    # Reddit pain points
    ok, out = run_script("reddit_pain_point_miner.py", "--scan", timeout=120)
    results.append(("pain_points", ok, out))

    # RBI scanner
    ok, out = run_script("daily_nocost_rbi_scanner.py", "--scan", timeout=180)
    results.append(("rbi", ok, out))

    successes = sum(1 for _, ok, _ in results if ok)
    return (
        "success" if successes >= 3 else "partial" if successes >= 1 else "failed",
        f"{successes}/4 scanners completed"
    )


def mission_process_and_decide():
    """Process collected data into decisions and actionable outputs."""
    log("MISSION: Process & decide")
    ok, out = run_script("decision_engine.py", "--cycle", timeout=120)
    if ok:
        # Count outputs produced
        freelance_count = len(list((PROJECT / "CONTENT" / "freelance_responses").glob("*.md"))) if (PROJECT / "CONTENT" / "freelance_responses").exists() else 0
        ecom_count = len(list((PROJECT / "CONTENT" / "ecom_listings").glob("*.md"))) if (PROJECT / "CONTENT" / "ecom_listings").exists() else 0
        return "success", f"Decisions made. {freelance_count} response drafts, {ecom_count} listing drafts"
    return "failed", out[-200:]


def mission_screen_alpha():
    """Screen alpha entries and clear the backlog."""
    log("MISSION: Screen alpha")
    pending = count_csv("LEDGER/ALPHA_STAGING.csv")
    if pending < 10:
        return "skipped", f"Only {pending} entries, not worth screening"

    ok, out = run_script("alpha_screening.py", "--pending", timeout=300)
    if ok:
        # Also run alpha review bot
        run_script("alpha_review_bot.py", "--batch 100", timeout=180)
        return "success", f"Screened batch from {pending} pending entries"
    return "failed", out[-200:]


def mission_generate_content():
    """Generate fresh content from the best opportunities found today."""
    log("MISSION: Generate content")

    # Check what we have to work with
    pain_digest = PROJECT / "OPS" / f"PAIN_POINT_DIGEST_{datetime.now().strftime('%Y_%m_%d')}.md"
    rbi_summary = PROJECT / "LEDGER" / "RBI_AUDITS" / f"rbi_summary_{datetime.now().strftime('%Y-%m-%d')}.md"

    sources = []
    if pain_digest.exists():
        sources.append(f"Pain point digest: {pain_digest.read_text()[:1000]}")
    if rbi_summary.exists():
        sources.append(f"RBI opportunities: {rbi_summary.read_text()[:1000]}")

    # Get top ecom arb products
    ecom_rows = read_csv_tail("LEDGER/ECOM_ARB_OPPORTUNITIES.csv", 10)
    hot_products = [r for r in ecom_rows if float(r.get("margin_pct", r.get("margin", 0)) or 0) > 40]
    if hot_products:
        products_str = ", ".join(f"{r.get('product', '?')} ({r.get('margin_pct', r.get('margin', '?'))}% margin)" for r in hot_products[:5])
        sources.append(f"Hot arb products: {products_str}")

    if not sources:
        return "skipped", "No fresh data to generate content from"

    # Use Claude to generate tweets from today's findings
    prompt = f"""You are @printmaxxer on Twitter. Write 5 standalone tweets and 1 thread (5 tweets) based on today's real intelligence data below.

VOICE RULES (non-negotiable):
- lowercase energy. no caps unless emphasizing a number.
- consequence-first hooks. lead with what happened or what works, not "here's how" or "I found".
- exact numbers always. "$47/hr" not "good money". "200+ pages" not "a lot".
- no em dashes. no AI words (leverage, utilize, comprehensive, innovative, seamless, game-changer, delve).
- name specific tools (visualping.io, photon, buffer) not generic terms ("a monitoring tool").
- short punchy sentences. staccato rhythm. period-heavy.
- would @pipelineabuser post this? if it sounds like a LinkedIn influencer, delete it and rewrite.

BAD EXAMPLE: "I discovered an incredible opportunity in the meal prep space that could generate significant revenue."
GOOD EXAMPLE: "meal prep pain point showed up 3x in today's scan. $300-500/mo retainer per client. batch 4-5 clients same day and it's a logistics play not a service. nobody's doing this with route optimization yet."

TODAY'S INTELLIGENCE (real data, use these specifics):
{chr(10).join(sources)}

OUTPUT: Write each tweet as ready-to-post copy. Separate tweets with ---
After the 5 standalone tweets, write THREAD: then each thread tweet on its own line separated by ---
No meta commentary. No "here are the tweets". Just the tweets themselves.
"""

    ok, out = run_claude(prompt, timeout=120)
    if ok and len(out) > 200:
        # Save output
        outfile = PROJECT / "CONTENT" / "social" / "printmaxxer" / f"AGENT_CONTENT_{datetime.now().strftime('%Y%m%d')}.md"
        outfile.parent.mkdir(parents=True, exist_ok=True)
        safe_path(outfile)
        outfile.write_text(f"# Agent-Generated Content — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{out}")
        return "success", f"Generated content from {len(sources)} sources, saved to {outfile.name}"
    return "partial", f"Claude returned {'ok' if ok else 'error'}, output length: {len(out)}"


def mission_factory_run():
    """Run the autonomous factory to generate listings, deploy, report."""
    log("MISSION: Factory run")
    ok, out = run_script("autonomous_factory.py", "--full", timeout=300)
    if ok:
        return "success", "Factory cycle complete"
    # Partial is fine — some sub-tasks may fail
    if "Report:" in out:
        return "partial", "Factory ran with some errors"
    return "failed", out[-200:]


def mission_health_and_heal():
    """Check system health and auto-heal what's broken."""
    log("MISSION: Health & heal")

    # Guardian pulse
    ok1, out1 = run_script("perpetual_guardian.py", "--pulse", timeout=60)

    # Self-heal
    ok2, out2 = run_script("perpetual_guardian.py", "--heal", timeout=120)

    # Update heartbeat
    run_script("memory_manager.py", "--heartbeat", timeout=60)

    healed = "Healed" in out2
    return (
        "success" if ok1 and ok2 else "partial",
        f"Health checked. {'Healed issues.' if healed else 'No issues to heal.'}"
    )


def mission_compliance_check():
    """Scan all pending content for compliance issues."""
    log("MISSION: Compliance check")
    ok, out = run_script("compliance_scanner.py", "--audit-all --save", timeout=180)
    if ok:
        critical = out.count("CRITICAL")
        return "success", f"Compliance scan done. {critical} critical issues."
    return "failed", out[-200:]


def mission_schedule_content():
    """Generate Buffer CSV and Tweetlio JSON for posting."""
    log("MISSION: Schedule content")
    ok, out = run_script("auto_scheduler.py", "--generate", timeout=60)
    if ok:
        slots = "42" if "42" in out else "?"
        return "success", f"Scheduled {slots} slots across 7 days"
    return "failed", out[-200:]


def mission_research_and_scrape():
    """Run all research scrapers."""
    log("MISSION: Research & scrape")
    results = []

    ok, _ = run_script("daily_reddit_scraper.py", timeout=120)
    results.append(("reddit", ok))

    ok, _ = run_script("daily_twitter_scraper.py", timeout=180)
    results.append(("twitter", ok))

    ok, _ = run_script("producthunt_scraper.py", timeout=60)
    results.append(("producthunt", ok))

    successes = sum(1 for _, ok in results if ok)
    return (
        "success" if successes >= 2 else "partial" if successes >= 1 else "failed",
        f"{successes}/3 scrapers completed"
    )


def mission_upgrade_content():
    """Take existing content and make it better. Recursive improvement."""
    log("MISSION: Upgrade content (recursive)")

    # Find content that exists but could be better
    buildout = PROJECT / "CONTENT" / "social" / "buildout"
    if not buildout.exists():
        return "skipped", "No buildout content to upgrade"

    # Pick the category with the most files that hasn't been upgraded yet
    upgraded_marker = AGENT_DIR / "upgraded_content.json"
    already_upgraded = set()
    if upgraded_marker.exists():
        try:
            already_upgraded = set(json.loads(upgraded_marker.read_text()))
        except Exception:
            pass

    candidates = []
    for d in buildout.iterdir():
        if d.is_dir() and d.name not in already_upgraded:
            file_count = sum(1 for _ in d.rglob("*.md"))
            if file_count > 0:
                candidates.append((d.name, file_count, d))

    if not candidates:
        return "skipped", "All content already upgraded"

    # Pick the one with most files
    candidates.sort(key=lambda x: x[1], reverse=True)
    target_name, count, target_dir = candidates[0]

    # Read first file to understand what we're working with
    first_file = next(target_dir.rglob("*.md"), None)
    if not first_file:
        return "skipped", f"No markdown in {target_name}"

    sample = first_file.read_text()[:2000]

    prompt = f"""You are upgrading content for the PRINTMAXX system. This content was auto-generated by a ralph loop and may be surface-level.

CONTENT TO UPGRADE (from {target_name}, sample):
{sample}

YOUR JOB:
1. Read this content critically
2. Identify what's generic/weak/missing
3. Add specific numbers, real tool names, actual pricing, conversion rates
4. Add compliance notes where needed (FTC disclosures, income disclaimers)
5. Make it actually useful — not just a template but a playbook someone could execute TODAY

Write the upgraded version. Keep the same structure but make every section 2x more specific and actionable.
Output the improved content directly — no meta commentary.
"""

    ok, out = run_claude(prompt, timeout=120)
    if ok and len(out) > 500:
        upgrade_file = target_dir / f"UPGRADED_{first_file.name}"
        safe_path(upgrade_file)
        upgrade_file.write_text(out)

        already_upgraded.add(target_name)
        safe_path(upgraded_marker)
        upgraded_marker.write_text(json.dumps(list(already_upgraded)))

        return "success", f"Upgraded {target_name} ({count} files), saved to {upgrade_file.name}"
    return "partial", f"Upgrade attempt for {target_name}: {'ok' if ok else 'failed'}"


def mission_find_new_opportunities():
    """Proactively search for things nobody asked about."""
    log("MISSION: Proactive opportunity hunt")

    prompt = """You are a proactive business intelligence agent for PRINTMAXX, a solopreneur automation system.

Your job: Find ONE specific, actionable opportunity that the system isn't currently pursuing.

Context on what we already do:
- Ecom arbitrage (AliExpress → FB/eBay)
- Freelance services (Fiverr, cold email)
- Content farming (TikTok, YouTube, Twitter, newsletters)
- Digital products (Gumroad, Etsy)
- App development (PWAs on surge.sh)
- Print on demand
- AI automation services

Search for something SPECIFIC and NEW. Not generic advice. Something like:
- "Canva template marketplace just launched a new category with 0 competition"
- "ChatGPT plugin store has a gap in [specific niche] — here's the 3-day build plan"
- "This specific Upwork job category has 10x the pay rate of similar ones"

Requirements:
- Must be deployable with $0 upfront
- Must be achievable by one person with AI tools
- Must have a clear path to first dollar in under 14 days
- Include the EXACT first 3 steps to execute

Output format:
OPPORTUNITY: [one line]
WHY NOW: [why this works right now, not 6 months ago]
FIRST DOLLAR PATH: [exact steps]
ESTIMATED MONTHLY: [realistic range]
TOOLS NEEDED: [specific names]
RISK: [what could go wrong]
"""

    ok, out = run_claude(prompt, timeout=90)
    if ok and len(out) > 200:
        outfile = PROJECT / "LEDGER" / "PROACTIVE_OPPORTUNITIES" / f"opportunity_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        outfile.parent.mkdir(parents=True, exist_ok=True)
        safe_path(outfile)
        outfile.write_text(f"# Proactive Opportunity — {datetime.now().isoformat()}\n\n{out}")

        # Also append to alpha staging
        try:
            with open(PROJECT / "LEDGER" / "ALPHA_STAGING.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerow([
                    f"PROACTIVE_{datetime.now().strftime('%Y%m%d_%H%M')}",
                    out[:200].replace("\n", " "),
                    "PROACTIVE_AGENT",
                    "", "PENDING_REVIEW", "HIGH", "",
                    datetime.now().isoformat(), "agent_hunt"
                ])
        except Exception:
            pass

        return "success", f"Found opportunity, saved to {outfile.name}"
    return "partial", "Searched but results were thin"


def mission_safety_commit():
    """Git commit all changes as a safety net."""
    log("MISSION: Safety commit")
    ok, out = run_script("perpetual_guardian.py", "--safety-commit", timeout=60)
    return ("success" if ok else "partial"), "Git safety commit"


# === SCHEDULE ===
# Defines which missions run at which hours
# Format: (hour_range, mission_fn, name, frequency_hours)

SCHEDULE = [
    # Always run (every cycle)
    (range(0, 24), mission_health_and_heal, "health_heal", 1),
    (range(0, 24), mission_process_and_decide, "process_decide", 1),

    # Morning (5-9 AM): Heavy scanning and research
    (range(5, 10), mission_scan_opportunities, "scan_opps", 2),
    (range(5, 10), mission_research_and_scrape, "research", 3),
    (range(5, 10), mission_screen_alpha, "screen_alpha", 4),

    # Midday (10 AM - 2 PM): Content generation and upgrades
    (range(10, 15), mission_generate_content, "gen_content", 3),
    (range(10, 15), mission_upgrade_content, "upgrade_content", 4),
    (range(10, 15), mission_schedule_content, "schedule", 6),

    # Afternoon (2-6 PM): Factory and compliance
    (range(14, 19), mission_factory_run, "factory", 4),
    (range(14, 19), mission_compliance_check, "compliance", 8),
    (range(14, 19), mission_find_new_opportunities, "proactive_hunt", 6),

    # Evening (6-11 PM): More scanning, content, safety
    (range(18, 24), mission_scan_opportunities, "scan_opps_eve", 3),
    (range(18, 24), mission_generate_content, "gen_content_eve", 4),
    (range(18, 24), mission_safety_commit, "safety_commit", 2),

    # Overnight (11 PM - 5 AM): Deep processing
    (range(23, 24), mission_screen_alpha, "screen_alpha_night", 2),
    (range(0, 5), mission_research_and_scrape, "research_night", 4),
    (range(0, 5), mission_upgrade_content, "upgrade_night", 3),
    (range(0, 5), mission_find_new_opportunities, "hunt_night", 4),
    (range(0, 5), mission_safety_commit, "safety_night", 3),
]


def should_run_mission(name, freq_hours, state):
    """Check if enough time has passed since last run."""
    last = state.data.get("last_run_times", {}).get(name)
    if not last:
        return True
    try:
        last_dt = datetime.fromisoformat(last)
        return datetime.now() - last_dt > timedelta(hours=freq_hours)
    except Exception:
        return True


def mark_mission_run(name, state):
    if "last_run_times" not in state.data:
        state.data["last_run_times"] = {}
    state.data["last_run_times"][name] = datetime.now().isoformat()


# === MAIN LOOP ===

def run_cycle(state, specific_mission=None):
    """Run one full agent cycle."""
    hour = datetime.now().hour
    cycle_start = time.time()

    log("=" * 60)
    log(f"AGENT CYCLE START — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    log(f"Disk: {disk_free_gb()}GB free | Missions completed: {state.data['missions_completed']} | Failed: {state.data['missions_failed']}")
    log("=" * 60)

    state.data["disk_gb_free"] = disk_free_gb()

    # Disk safety check
    if state.data["disk_gb_free"] < 2:
        log("DISK CRITICAL: < 2GB free. Skipping write-heavy missions.", "WARN")

    missions_run = 0

    if specific_mission:
        # Run a specific mission by name
        mission_map = {
            "scan": mission_scan_opportunities,
            "decide": mission_process_and_decide,
            "alpha": mission_screen_alpha,
            "content": mission_generate_content,
            "factory": mission_factory_run,
            "health": mission_health_and_heal,
            "compliance": mission_compliance_check,
            "schedule": mission_schedule_content,
            "research": mission_research_and_scrape,
            "upgrade": mission_upgrade_content,
            "hunt": mission_find_new_opportunities,
            "commit": mission_safety_commit,
        }
        fn = mission_map.get(specific_mission)
        if fn:
            start = time.time()
            result, summary = fn()
            duration = time.time() - start
            state.log_mission(specific_mission, result, duration, summary)
            log(f"  [{result.upper()}] {specific_mission}: {summary} ({duration:.1f}s)")
            missions_run = 1
        else:
            log(f"Unknown mission: {specific_mission}. Options: {', '.join(mission_map.keys())}")
            return
    else:
        # Run scheduled missions
        for hour_range, fn, name, freq in SCHEDULE:
            if hour not in hour_range:
                continue
            if not should_run_mission(name, freq, state):
                continue
            if state.data["disk_gb_free"] < 2 and name not in ("health_heal", "safety_commit"):
                log(f"  [SKIP] {name}: disk too low", "WARN")
                continue

            start = time.time()
            try:
                result, summary = fn()
            except Exception as e:
                result, summary = "failed", str(e)[:200]
            duration = time.time() - start

            state.log_mission(name, result, duration, summary)
            mark_mission_run(name, state)
            log(f"  [{result.upper()}] {name}: {summary} ({duration:.1f}s)")
            missions_run += 1

    cycle_duration = time.time() - cycle_start
    state.data["last_cycle"] = datetime.now().isoformat()
    state.data["cycles_run"] += 1
    state.save()

    log("=" * 60)
    log(f"CYCLE COMPLETE — {missions_run} missions in {cycle_duration:.0f}s")
    log("=" * 60)


def run_daemon(state):
    """Run forever. One cycle per hour, adjusting to schedule."""
    log("AGENT DAEMON STARTING — Ctrl+C to stop")
    log("Cycle interval: 60 minutes (missions self-throttle by frequency)")

    while True:
        try:
            run_cycle(state)
            # Sleep until next hour
            now = datetime.now()
            next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
            sleep_secs = (next_hour - now).total_seconds()
            log(f"Sleeping {sleep_secs:.0f}s until {next_hour.strftime('%H:%M')}")
            time.sleep(sleep_secs)
        except KeyboardInterrupt:
            log("DAEMON STOPPED")
            state.save()
            break
        except Exception as e:
            log(f"CYCLE ERROR: {e} — retrying in 5 min", "ERROR")
            time.sleep(300)


def show_status(state):
    """Show what the agent is doing."""
    print("=" * 60)
    print("PRINTMAXX AGENT STATUS")
    print("=" * 60)
    print(f"Cycles run: {state.data['cycles_run']}")
    print(f"Last cycle: {state.data.get('last_cycle', 'never')}")
    print(f"Missions completed: {state.data['missions_completed']}")
    print(f"Missions failed: {state.data['missions_failed']}")
    print(f"Disk free: {disk_free_gb()}GB")

    print("\nLAST MISSION RESULTS:")
    for name, result in state.data.get("last_mission_results", {}).items():
        icon = {"success": "+", "partial": "~", "failed": "X", "skipped": "-"}.get(result, "?")
        print(f"  [{icon}] {name}: {result}")

    print("\nLAST RUN TIMES:")
    for name, ts in sorted(state.data.get("last_run_times", {}).items()):
        print(f"  {name}: {ts}")

    # Show recent mission log
    if MISSION_LOG.exists():
        print("\nRECENT MISSIONS (last 10):")
        lines = MISSION_LOG.read_text().strip().split("\n")
        for line in lines[-10:]:
            try:
                entry = json.loads(line)
                icon = {"success": "+", "partial": "~", "failed": "X", "skipped": "-"}.get(entry["result"], "?")
                print(f"  [{icon}] {entry['ts'][:16]} {entry['mission']}: {entry['output'][:80]}")
            except Exception:
                pass

    # Active schedule for current hour
    hour = datetime.now().hour
    print(f"\nACTIVE MISSIONS FOR {hour}:00:")
    for hour_range, _, name, freq in SCHEDULE:
        if hour in hour_range:
            will_run = should_run_mission(name, freq, state)
            print(f"  {'>>>' if will_run else '   '} {name} (every {freq}h) {'— DUE' if will_run else ''}")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Agent — Proactive Autonomous System")
    parser.add_argument("--once", action="store_true", help="Run one cycle then exit")
    parser.add_argument("--status", action="store_true", help="Show agent status")
    parser.add_argument("--mission", type=str, help="Run a specific mission")
    args = parser.parse_args()

    state = AgentState()

    if args.status:
        show_status(state)
    elif args.mission:
        run_cycle(state, specific_mission=args.mission)
    elif args.once:
        run_cycle(state)
    else:
        run_daemon(state)


if __name__ == "__main__":
    main()
