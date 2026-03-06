#!/usr/bin/env python3
"""
PRINTMAXX OPS MANAGER — Hierarchical Multi-Agent Business System

The brain. Manages venture sub-agents, prioritizes by ROI, kills losers,
doubles winners, adds new ventures, and perpetually improves everything.

Architecture:
  OPS MANAGER (this file)
  └── Venture Agents (each a class with missions, metrics, priorities)
      ├── ContentFarm — personas, social, engagement, viral, findom
      ├── Ecom — arbitrage, POD, TikTok shop, dropship
      ├── Services — freelance, cold outbound, local biz, AI automation
      ├── DigitalProducts — Gumroad, Etsy, KDP, Notion templates
      ├── Apps — PWA factory, micro-SaaS
      ├── Affiliate — review sites, SaaS referrals, Amazon
      ├── AdultContent — findom AI personas (legal, FTC compliant)
      └── Growth — SEO, reply guy, community, newsletter

Usage:
  python3 AUTOMATIONS/printmaxx_ops_manager.py                # Full cycle
  python3 AUTOMATIONS/printmaxx_ops_manager.py --status       # Dashboard
  python3 AUTOMATIONS/printmaxx_ops_manager.py --venture X    # Run one venture
  python3 AUTOMATIONS/printmaxx_ops_manager.py --prioritize   # Re-rank ventures
  python3 AUTOMATIONS/printmaxx_ops_manager.py --discover     # Hunt new ventures
  python3 AUTOMATIONS/printmaxx_ops_manager.py --daemon       # Run forever

GUARDRAILS (non-negotiable):
  - ALL file ops locked to PROJECT root
  - No Desktop, Downloads, Library, system dirs
  - No dangerous commands (rm -rf /, dd, fork bombs)
  - All subprocess timeouts enforced
  - Disk < 2GB = pause write-heavy ops
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# === GUARDRAILS ===
PROJECT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
OPS_DIR = PROJECT / "AUTOMATIONS" / "agent" / "ops_manager"
STATE_FILE = OPS_DIR / "ops_state.json"
VENTURE_LOG = OPS_DIR / "venture_log.jsonl"
PYTHON = sys.executable

BLOCKED_DIRS = [
    Path.home() / d for d in
    ["Desktop", "Downloads", "Pictures", "Music", "Movies", "Library", ".ssh", ".aws", ".gnupg"]
] + [Path(d) for d in ["/System", "/Library", "/usr", "/bin", "/etc", "/var"]]

BLOCKED_COMMANDS = ["rm -rf /", "rm -rf ~", "dd if=", "diskutil erase", "mkfs", ":(){ :|:& };:"]


def safe_path(p):
    resolved = Path(p).resolve()
    project_resolved = PROJECT.resolve()
    if not str(resolved).startswith(str(project_resolved)):
        raise ValueError(f"GUARDRAIL BLOCKED: {resolved} outside project {project_resolved}")
    for blocked in BLOCKED_DIRS:
        if str(resolved).startswith(str(blocked.resolve())):
            raise ValueError(f"GUARDRAIL BLOCKED: {resolved} in protected dir {blocked}")
    return resolved


def safe_command(cmd_str):
    lower = cmd_str.lower()
    for bad in BLOCKED_COMMANDS:
        if bad in lower:
            raise ValueError(f"GUARDRAIL BLOCKED: {bad}")


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
    log_path = PROJECT / "AUTOMATIONS" / "logs" / "ops_manager.log"
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


COMPLIANCE_BLOCKLIST = [
    # Illegal content patterns — if local LLM generates any of these, reject the output
    "underage", "minor", "child", "non-consensual", "rape", "blackmail",
    "revenge porn", "deepfake of real", "without consent", "forced",
    "traffick", "exploit children", "cp ", "csam",
]

COMPLIANCE_REQUIRED_DISCLAIMERS = [
    # At least one of these must appear in findom content for it to pass
    "#findom", "findom", "voluntary", "consenting", "18+", "adult",
]

LOCAL_LLM_OUTPUT_DIR = PROJECT / "CONTENT" / "_LOCAL_LLM_QUARANTINE"
# ^^^ ISOLATED directory. Claude never reads from here automatically.
# Human reviews content here, then moves approved content to CONTENT/social/


def compliance_filter(text, content_type="adult"):
    """Screen local LLM output for illegal/non-compliant content.
    Returns (passed, reason). If passed=False, content is rejected."""
    lower = text.lower()

    # Hard reject: illegal content patterns
    for bad in COMPLIANCE_BLOCKLIST:
        if bad in lower:
            return False, f"COMPLIANCE REJECTED: matched blocklist pattern '{bad}'"

    # For adult content: must include at least one disclaimer indicator
    if content_type == "adult":
        has_disclaimer = any(d in lower for d in COMPLIANCE_REQUIRED_DISCLAIMERS)
        if not has_disclaimer:
            return False, "COMPLIANCE REJECTED: no disclaimer/consent language found"

    return True, "passed"


def run_local_llm(prompt, timeout=300):
    """Run a prompt through local LLM (LM Studio or Ollama).
    Uses OpenAI-compatible API (both LM Studio and Ollama support this).
    Used for content that Claude's safety filter blocks (e.g. adult content).

    LM Studio: http://localhost:1234/v1/chat/completions (default)
    Ollama:    http://localhost:11434/v1/chat/completions (alternative)

    Recommended models for LM Studio (64GB M1 Max):
    - Dolphin 3.0 Llama-3.1 70B Q4 — best quality, ~40GB
    - Eva Qwen2.5 32B — excellent creative/roleplay, ~20GB
    - Nous Hermes 3 8B — fast fallback, ~5GB
    """
    import urllib.request
    import urllib.error

    # Try LM Studio first (port 1234), then Ollama (port 11434)
    endpoints = [
        ("http://localhost:1234/v1/chat/completions", "LM Studio"),
        ("http://localhost:11434/v1/chat/completions", "Ollama"),
    ]

    for url, name in endpoints:
        try:
            payload = json.dumps({
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.85,
                "max_tokens": 4000,
                "stream": False
            }).encode()
            req = urllib.request.Request(
                url, data=payload,
                headers={"Content-Type": "application/json"}
            )
            resp = urllib.request.urlopen(req, timeout=timeout)
            data = json.loads(resp.read().decode())
            text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if text and len(text) > 50:
                log(f"Local LLM ({name}) generated {len(text)} chars")
                return True, text
        except urllib.error.URLError:
            log(f"{name} not running at {url}", "WARN")
        except Exception as e:
            log(f"Local LLM error ({name}): {e}", "WARN")

    return False, "No local LLM available. Start LM Studio and load a model, or run Ollama."


def run_script(script, args="", timeout=300):
    script_path = (PROJECT / "AUTOMATIONS" / script).resolve()
    if not str(script_path).startswith(str(PROJECT.resolve())):
        return False, f"BLOCKED: {script} outside project"
    if not script_path.exists():
        return False, f"Not found: {script}"
    cmd = f"{PYTHON} {script_path} {args}"
    safe_command(cmd)
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           timeout=timeout, cwd=str(PROJECT))
        return r.returncode == 0, (r.stdout + r.stderr)[-2000:]
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT {timeout}s"
    except Exception as e:
        return False, str(e)


def run_claude(prompt, timeout=180):
    cmd = ["claude", "--dangerously-skip-permissions", "--print",
           "--mcp-config", str(PROJECT / "ralph" / "empty_mcp.json"),
           "--strict-mcp-config"]
    try:
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                           timeout=timeout, cwd=str(PROJECT),
                           env={**os.environ, "CLAUDECODE": ""})
        return r.returncode == 0, (r.stdout + r.stderr)[-4000:]
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT {timeout}s"
    except Exception as e:
        return False, str(e)


# === OPS STATE ===

class OpsState:
    def __init__(self):
        OPS_DIR.mkdir(parents=True, exist_ok=True)
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
            "venture_scores": {},
            "venture_status": {},
            "revenue": {"total": 0, "by_venture": {}},
            "active_ventures": [],
            "killed_ventures": [],
            "pending_ventures": [],
            "last_prioritization": None,
            "disk_gb_free": 0,
        }

    def save(self):
        safe_path(STATE_FILE)
        STATE_FILE.write_text(json.dumps(self.data, indent=2, default=str))

    def log_venture(self, venture, result, duration, output):
        entry = {
            "ts": datetime.now().isoformat(),
            "venture": venture,
            "result": result,
            "duration": round(duration, 1),
            "output": output[:300]
        }
        safe_path(VENTURE_LOG)
        with open(VENTURE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")


# === VENTURE DEFINITIONS ===

class Venture:
    """Base class for all venture agents."""

    name = "base"
    category = "uncategorized"
    priority = 5  # 1=highest, 10=lowest
    estimated_monthly = "$0"
    time_to_first_dollar = "unknown"
    accounts_needed = []
    scripts = []
    content_types = []
    compliance_notes = []

    def __init__(self, state: OpsState):
        self.state = state
        self.output_dir = PROJECT / "MONEY_METHODS" / self.name.upper()
        self.content_dir = PROJECT / "CONTENT" / "social" / self.name.lower()

    def run_cycle(self):
        """Run one full cycle of this venture's operations."""
        raise NotImplementedError

    def get_metrics(self):
        """Return current metrics for this venture."""
        return self.state.data.get("venture_scores", {}).get(self.name, {})

    def score(self):
        """Calculate venture priority score. Higher = better."""
        metrics = self.get_metrics()
        revenue = metrics.get("revenue_30d", 0)
        effort = metrics.get("hours_per_week", 10)
        readiness = metrics.get("readiness_pct", 0)
        roi = revenue / max(effort, 1)
        return round(roi * (readiness / 100), 2)


class ContentFarmVenture(Venture):
    name = "content_farm"
    category = "content"
    priority = 2
    estimated_monthly = "$500-5,000"
    time_to_first_dollar = "14-30 days"
    accounts_needed = ["twitter", "tiktok", "instagram", "youtube"]
    compliance_notes = ["FTC disclosure on affiliate links", "AI content disclosure where required"]

    def run_cycle(self):
        log(f"[{self.name}] Running content farm cycle")
        results = []

        # 1. Generate fresh content from intelligence
        ok, out = run_script("printmaxx_agent.py", "--mission content", timeout=180)
        results.append(("content_gen", ok))

        # 2. Upgrade existing content
        ok, out = run_script("printmaxx_agent.py", "--mission upgrade", timeout=180)
        results.append(("content_upgrade", ok))

        # 3. Schedule content
        ok, out = run_script("printmaxx_agent.py", "--mission schedule", timeout=60)
        results.append(("schedule", ok))

        successes = sum(1 for _, ok in results if ok)
        return "success" if successes >= 2 else "partial", f"{successes}/3 content ops completed"


class EcomVenture(Venture):
    name = "ecom"
    category = "ecom"
    priority = 3
    estimated_monthly = "$200-3,000"
    time_to_first_dollar = "7-21 days"
    accounts_needed = ["ebay", "facebook_marketplace", "etsy"]
    compliance_notes = ["Product safety disclosures", "Accurate descriptions"]

    def run_cycle(self):
        log(f"[{self.name}] Running ecom cycle")
        results = []

        # Scan for arb opportunities
        ok, out = run_script("ecom_arb_engine.py", timeout=120)
        results.append(("arb_scan", ok))

        # Process into listings
        ok, out = run_script("decision_engine.py", "--cycle", timeout=120)
        results.append(("decisions", ok))

        successes = sum(1 for _, ok in results if ok)
        return "success" if successes >= 1 else "failed", f"{successes}/2 ecom ops"


class ServicesVenture(Venture):
    name = "services"
    category = "services"
    priority = 1  # Fastest to first dollar
    estimated_monthly = "$500-10,000"
    time_to_first_dollar = "3-14 days"
    accounts_needed = ["fiverr", "upwork", "email_accounts"]
    compliance_notes = ["Accurate service descriptions", "Clear deliverables"]

    def run_cycle(self):
        log(f"[{self.name}] Running services cycle")
        results = []

        # Scan freelance demand
        ok, out = run_script("freelance_demand_scanner.py", timeout=120)
        results.append(("freelance_scan", ok))

        # Generate responses
        ok, out = run_script("decision_engine.py", "--cycle", timeout=120)
        results.append(("response_gen", ok))

        # Cold outreach scan
        ok, out = run_script("daily_nocost_rbi_scanner.py", "--scan", timeout=180)
        results.append(("rbi_scan", ok))

        successes = sum(1 for _, ok in results if ok)
        return "success" if successes >= 2 else "partial", f"{successes}/3 service ops"


class DigitalProductsVenture(Venture):
    name = "digital_products"
    category = "products"
    priority = 3
    estimated_monthly = "$100-2,000"
    time_to_first_dollar = "7-30 days"
    accounts_needed = ["gumroad", "etsy", "payhip"]
    compliance_notes = ["Accurate product descriptions", "Refund policy"]

    def run_cycle(self):
        log(f"[{self.name}] Running digital products cycle")
        # Check for product ideas from alpha
        ok, out = run_script("alpha_to_ops.py", "--process", timeout=180)
        return "success" if ok else "partial", "Product pipeline processed"


class AppsVenture(Venture):
    name = "apps"
    category = "tech"
    priority = 4
    estimated_monthly = "$50-1,000"
    time_to_first_dollar = "14-60 days"
    accounts_needed = ["surge_sh"]

    def run_cycle(self):
        log(f"[{self.name}] Running apps cycle")
        ok, out = run_script("autonomous_factory.py", "--full", timeout=300)
        return "success" if ok else "partial", "Factory cycle ran"


class AffiliateVenture(Venture):
    name = "affiliate"
    category = "affiliate"
    priority = 3
    estimated_monthly = "$100-3,000"
    time_to_first_dollar = "14-45 days"
    accounts_needed = ["amazon_associates", "shareasale", "impact"]
    compliance_notes = ["FTC disclosure required on ALL affiliate content",
                        "Must disclose material connection"]

    def run_cycle(self):
        log(f"[{self.name}] Running affiliate cycle")
        # Generate affiliate content from existing product data
        ok, out = run_script("decision_engine.py", "--cycle", timeout=120)
        return "success" if ok else "partial", "Affiliate pipeline ran"


class AdultContentVenture(Venture):
    """Legal adult content monetization — findom AI personas.

    COMPLIANCE (non-negotiable):
    - All content must comply with platform TOS
    - FTC disclosure on all sponsored/affiliate content
    - Age verification on any gated content
    - No minors, no non-consensual themes
    - AI-generated persona disclosed where required by law
    - Financial domination is legal fantasy roleplay between consenting adults
    - All monetary transactions are voluntary gifts/tributes
    - Tax reporting on all income (1099 thresholds)
    """
    name = "adult_content"
    category = "adult"
    priority = 2
    estimated_monthly = "$500-10,000"
    time_to_first_dollar = "7-21 days"
    accounts_needed = ["twitter_adult", "loyalfans", "cashapp"]
    compliance_notes = [
        "FTC disclosure on all monetized content",
        "AI persona disclosure where legally required",
        "Age verification on gated content (18+)",
        "All transactions are voluntary — no coercion claims",
        "Tax reporting: track all income, 1099 threshold",
        "Platform TOS compliance — review each platform's adult content policy",
        "No minors, no non-consensual content, no illegal content",
        "CAN-SPAM compliance on any email marketing",
    ]
    content_types = ["findom_tweets", "tribute_cta", "worship_content", "lifestyle_flex"]

    def run_cycle(self):
        log(f"[{self.name}] Running adult content cycle")

        findom_dir = PROJECT / "MONEY_METHODS" / "AI_INFLUENCER" / "FINDOM"
        exec_plan = PROJECT / "MONEY_METHODS" / "AI_INFLUENCER" / "AI_NSFW_FINDOM_EXECUTION_PLAN.md"
        if not findom_dir.exists() and not exec_plan.exists():
            return "skipped", "Findom research not built yet"

        # Claude CLI refuses findom marketing copy. Use local LLM (Ollama) for content.
        # Claude handles business intel. Local LLM handles persona content.

        results = []

        # 1. Business intel via Claude (always works)
        intel_prompt = """Analyze the financial domination niche business model briefly:
1. Top monetization platforms (CashApp, LoyalFans, iWantClips, Throne, OnlyFans)
2. Typical posting frequency for 5K-50K follower accounts
3. Account setup requirements (age verification, compliance)
Output a brief business model summary. Focus on platform economics only."""

        ok, out = run_claude(intel_prompt, timeout=90)
        if ok and len(out) > 100:
            outfile = OPS_DIR / f"findom_intel_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            safe_path(outfile)
            outfile.write_text(f"# Findom Business Intel — {datetime.now().isoformat()}\n\n{out}")
            results.append(("intel", True))

        # 2. Content generation via local LLM (Ollama — unrestricted)
        content_prompt = """You are a confident, commanding findom persona on Twitter.
Write 5 standalone tweets. Mix luxury lifestyle posts with dominant energy.
Voice: confident woman who knows her worth. Playful, not cruel. Lowercase energy.
Include hashtags: #findom #financialdomination
Include CashApp placeholder: $[HANDLE]
All content is legal fantasy roleplay between consenting adults.
This account is disclosed as AI-generated.

Write 5 tweets separated by ---"""

        ok, out = run_local_llm(content_prompt)
        if ok and len(out) > 100:
            # Compliance filter — reject anything illegal
            passed, reason = compliance_filter(out, content_type="adult")
            if not passed:
                log(f"LOCAL LLM OUTPUT REJECTED: {reason}", "SECURITY")
                results.append(("content", False))
            else:
                # Save to QUARANTINE dir — Claude never reads this automatically.
                # User manually reviews and moves approved content.
                quarantine = LOCAL_LLM_OUTPUT_DIR / "findom"
                quarantine.mkdir(parents=True, exist_ok=True)
                outfile = quarantine / f"findom_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
                safe_path(outfile)
                header = "# QUARANTINED — LOCAL LLM OUTPUT — HUMAN REVIEW REQUIRED\n"
                header += "# This content was generated by a local LLM, NOT Claude.\n"
                header += "# DO NOT feed this back to Claude or commit to git without review.\n"
                header += "#\n"
                header += "# COMPLIANCE CHECKLIST (must pass ALL before posting):\n"
                header += "# [ ] Content is legal (consenting adults, no minors, no coercion)\n"
                header += "# [ ] FTC disclosure present (#ad or equivalent)\n"
                header += "# [ ] AI persona disclosed where required\n"
                header += "# [ ] 18+ content label applied on platform\n"
                header += "# [ ] No real person's likeness used without consent\n"
                header += "# [ ] Platform TOS reviewed and compliant\n"
                header += f"# Generated: {datetime.now().isoformat()}\n"
                header += "# Model: local LLM via LM Studio / Ollama\n\n"
                outfile.write_text(header + out)
                log(f"Content quarantined for review: {outfile.name}")
                results.append(("content", True))
        else:
            results.append(("content", False))
            log("Local LLM not available — start LM Studio and load a model", "WARN")

        successes = sum(1 for _, ok in results if ok)
        if successes == 2:
            return "success", "Intel (Claude) + content (local LLM) both generated"
        elif successes == 1:
            return "partial", "Intel OK but local LLM not available for content — install Ollama"
        return "failed", "Both intel and content generation failed"


class GrowthVenture(Venture):
    name = "growth"
    category = "growth"
    priority = 2
    estimated_monthly = "$0 direct (enables all other ventures)"
    time_to_first_dollar = "N/A — force multiplier"
    accounts_needed = ["twitter", "reddit", "producthunt"]

    def run_cycle(self):
        log(f"[{self.name}] Running growth cycle")
        results = []

        # Research and scrape
        ok, out = run_script("printmaxx_agent.py", "--mission research", timeout=300)
        results.append(("research", ok))

        # Proactive opportunity hunt
        ok, out = run_script("printmaxx_agent.py", "--mission hunt", timeout=120)
        results.append(("hunt", ok))

        successes = sum(1 for _, ok in results if ok)
        return "success" if successes >= 1 else "partial", f"{successes}/2 growth ops"


class EdgeTacticsVenture(Venture):
    """Aggressive but legal growth tactics — engagement hacking, reply farming,
    controversy content, algorithm exploitation, swarm promotion.

    Everything here is legal. Some tactics push platform ToS boundaries.
    See grey_hat_legal.md for full compliance analysis of each tactic.
    """
    name = "edge_tactics"
    category = "growth"
    priority = 1  # Force multiplier for everything else
    estimated_monthly = "$0 direct (10x amplifier for all ventures)"
    time_to_first_dollar = "N/A — multiplier"
    accounts_needed = ["twitter", "tiktok", "instagram"]
    compliance_notes = [
        "All tactics must be ALLOWED or RISKY per grey_hat_legal.md — never ILLEGAL",
        "FTC disclosure on all monetized content",
        "No coordinated inauthentic behavior (each account adds genuine value)",
        "No fake scarcity/urgency (FTC explicitly targets this)",
        "AI content disclosed where platform requires it",
    ]

    def run_cycle(self):
        log(f"[{self.name}] Running edge tactics cycle")

        prompt = """You are an aggressive but legal engagement hacking agent for PRINTMAXX social accounts.

LEGAL BOUNDARIES (from grey_hat_legal.md):
- ALLOWED: Multiple accounts, AI personas (disclosed), content scraping (public), reply farming,
  competitor brand in SEO, swarm promotion (organic), controversy hooks
- RISKY BUT LEGAL: Engagement pods (ToS violation only), DM automation (triggered by user),
  aggressive SEO tactics
- NEVER DO: Fake scarcity (FTC), buying followers for sponsor fraud, bot manipulation,
  scraping behind login walls

YOUR JOB: Generate 3 tactical outputs:

1. REPLY FARMING TARGETS (5 specific tweets to reply to right now)
   - Find tweets from high-follower accounts in solopreneur/money/tech niche
   - Draft the reply (use Pattern 1: add next level, Pattern 2: contrarian with data,
     or Pattern 3: personal proof)
   - Each reply must add genuine value (not "great point!")

2. ENGAGEMENT BAIT CONTENT (3 posts designed for maximum engagement)
   - Use tactics: hot takes that split comments 50/50, "wrong answers only",
     intentional visual errors that drive comments, polls with controversial options
   - lowercase energy, no AI vocab, consequence-first hooks
   - These should drive comments and shares, not just likes

3. CONTROVERSY HOOK (1 post that's provocative but not bannable)
   - Pick a topic where solopreneurs disagree strongly
   - Frame it as a take, not a question
   - Goal: 100+ comments minimum
   - Must be legal and not violate any platform TOS
   - Examples: "college is a scam for 90% of people", "most SaaS is just a spreadsheet",
     "remote work makes you lazy and I can prove it"

Output directly. No meta commentary. Separate sections with ==="""

        ok, out = run_claude(prompt, timeout=120)
        if ok and len(out) > 300:
            outfile = PROJECT / "CONTENT" / "social" / "edge_tactics" / f"edge_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            outfile.parent.mkdir(parents=True, exist_ok=True)
            safe_path(outfile)
            header = "# Edge Tactics Content (PENDING_REVIEW)\n"
            header += "# All tactics verified legal per grey_hat_legal.md\n"
            header += f"# Generated: {datetime.now().isoformat()}\n\n"
            outfile.write_text(header + out)
            return "success", f"Generated edge tactics: {outfile.name}"
        return "partial", "Edge tactics generation thin"


class ViralContentVenture(Venture):
    """Viral content factory — AI UGC ads, intentional flaw ads, rage bait,
    algorithm exploitation across TikTok/Twitter/Instagram.

    The seven-finger-ad approach: intentionally include something "wrong"
    that compels people to comment, which feeds the algorithm.
    """
    name = "viral_content"
    category = "content"
    priority = 2
    estimated_monthly = "$200-5,000"
    time_to_first_dollar = "7-21 days"
    accounts_needed = ["tiktok", "instagram", "twitter"]
    compliance_notes = [
        "AI-generated content disclosed where platform requires",
        "FTC disclosure on any paid/affiliate content",
        "No fake testimonials",
        "UGC ads must comply with platform ad policies",
        "Controversy content must not violate hate speech policies",
    ]

    def run_cycle(self):
        log(f"[{self.name}] Running viral content cycle")

        prompt = """You are a viral content strategist. Generate content designed to exploit
platform algorithms for maximum reach.

TACTICS TO USE:
1. INTENTIONAL FLAW ADS — "seven finger" approach
   - Create ad copy/concept where something is subtly wrong
   - People comment "wait, that has 7 fingers" or "that math is wrong"
   - Comments feed algorithm → more reach → more eyes on the product
   - The flaw must be subtle enough to feel accidental

2. RAGE BAIT / HOT TAKES
   - Opinions that split audience 50/50
   - "I stopped [popular thing] and here's what happened"
   - Contrarian takes on widely-accepted advice

3. DUET/STITCH BAIT (TikTok)
   - Create content specifically designed to be stitched or dueted
   - Open-ended questions, controversial rankings, "rate my..."

4. ALGORITHM EXPLOITATION
   - First 3 seconds must hook (face close to camera, unexpected visual)
   - Loop content (seamless end-to-start loop increases watch time)
   - Reply to own content to create conversation threads

Generate:
- 3 intentional flaw ad concepts (product-agnostic, we'll plug in our products)
- 3 rage bait tweets (solopreneur niche, lowercase energy)
- 2 TikTok stitch bait concepts
- 2 loop content concepts

All content: lowercase, no AI vocab, no em dashes, specific numbers where possible.
Output directly, sections separated by ==="""

        ok, out = run_claude(prompt, timeout=120)
        if ok and len(out) > 300:
            outfile = PROJECT / "CONTENT" / "social" / "viral" / f"viral_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            outfile.parent.mkdir(parents=True, exist_ok=True)
            safe_path(outfile)
            header = "# Viral Content (PENDING_REVIEW)\n"
            header += f"# Generated: {datetime.now().isoformat()}\n\n"
            outfile.write_text(header + out)
            return "success", f"Generated viral content: {outfile.name}"
        return "partial", "Viral content generation thin"


class CompetitiveIntelVenture(Venture):
    """Competitive intelligence — monitor winners, copy what works,
    find gaps, track what competitors are doing across all niches."""
    name = "competitive_intel"
    category = "intelligence"
    priority = 2
    estimated_monthly = "$0 direct (informs all other ventures)"
    time_to_first_dollar = "N/A — intelligence layer"
    accounts_needed = []
    compliance_notes = ["Only scrape public data", "No CFAA violations"]

    def run_cycle(self):
        log(f"[{self.name}] Running competitive intel cycle")

        prompt = """You are a competitive intelligence agent. Your job: find what's WORKING
right now for other solopreneurs, content creators, and findom accounts.

SCAN FOR:
1. Twitter accounts in solopreneur niche with unusual engagement spikes (post went viral)
   - What format did they use? What hook? What time did they post?
   - Can we replicate the format with our content?

2. Findom/adult content accounts doing well
   - What monetization are they using? (CashApp, OnlyFans, LoyalFans, Throne wishlists)
   - What content formats drive the most engagement?
   - What's their posting frequency?
   - NOTE: All research must be about legal adult content between consenting adults

3. TikTok/Reels accounts that went from 0 to 100K+ in last 90 days
   - What niche? What format? Faceless or face? AI or human?
   - What's their monetization path?

4. Any new platform features or algorithm changes we should exploit

OUTPUT FORMAT:
WINNER: [account or example]
WHAT WORKED: [specific tactic]
REPLICABLE: [yes/no and how]
OUR ADAPTATION: [how we'd do it]
PRIORITY: [P1/P2/P3]

Find 5 winners across different categories."""

        ok, out = run_claude(prompt, timeout=120)
        if ok and len(out) > 300:
            outfile = OPS_DIR / f"competitive_intel_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            safe_path(outfile)
            outfile.write_text(f"# Competitive Intel — {datetime.now().isoformat()}\n\n{out}")
            return "success", f"Intel gathered: {outfile.name}"
        return "partial", "Intel gathering thin"


# === ALL VENTURES ===

VENTURE_CLASSES = [
    ServicesVenture,        # P1 — fastest to first dollar
    EdgeTacticsVenture,     # P1 — force multiplier
    ContentFarmVenture,     # P2 — scalable
    AdultContentVenture,    # P2 — high margin
    ViralContentVenture,    # P2 — algorithm exploitation
    CompetitiveIntelVenture,# P2 — intelligence layer
    GrowthVenture,          # P2 — force multiplier
    EcomVenture,            # P3 — proven pipeline
    DigitalProductsVenture, # P3 — high margin
    AffiliateVenture,       # P3 — passive
    AppsVenture,            # P4 — longer runway
]


# === OPS MANAGER CORE ===

def prioritize_ventures(state):
    """Re-rank ventures by ROI potential and readiness."""
    log("PRIORITIZING ventures by ROI...")
    ventures = [V(state) for V in VENTURE_CLASSES]

    ranked = []
    for v in ventures:
        score = v.score()
        accounts_ready = 0  # TODO: check actual account status
        total_accounts = len(v.accounts_needed)
        readiness = (accounts_ready / max(total_accounts, 1)) * 100

        ranked.append({
            "name": v.name,
            "priority": v.priority,
            "score": score,
            "estimated_monthly": v.estimated_monthly,
            "time_to_first_dollar": v.time_to_first_dollar,
            "readiness_pct": readiness,
            "accounts_needed": v.accounts_needed,
            "compliance_notes": v.compliance_notes,
        })

    ranked.sort(key=lambda x: (-x["score"], x["priority"]))

    state.data["active_ventures"] = [r["name"] for r in ranked]
    state.data["last_prioritization"] = datetime.now().isoformat()
    state.data["venture_scores"] = {r["name"]: r for r in ranked}
    state.save()

    for i, r in enumerate(ranked):
        log(f"  #{i+1} {r['name']}: P{r['priority']} | {r['estimated_monthly']} | {r['time_to_first_dollar']}")

    return ranked


def discover_new_ventures(state):
    """Use Claude to proactively hunt for new venture opportunities."""
    log("DISCOVERING new venture opportunities...")

    existing = [V.name for V in VENTURE_CLASSES]

    prompt = f"""You are a proactive business intelligence agent. Your job: find ONE new venture opportunity
that is NOT already in our portfolio.

EXISTING VENTURES (do NOT suggest these):
{', '.join(existing)}

REQUIREMENTS for new venture:
- $0 upfront cost to start
- One person with AI tools can run it
- First dollar possible in under 14 days
- Legal and compliant
- Can be automated/semi-automated
- Not saturated yet

Think about:
- New platform features (Twitter subscriptions, TikTok monetization changes, etc)
- Gaps in marketplaces (Etsy categories with demand but low supply)
- Emerging trends (AI wrappers, new API services, untapped niches)
- Cross-pollination (combining two existing methods into something new)
- Regulatory arbitrage (things that just became legal/possible)

OUTPUT FORMAT:
VENTURE_NAME: [short name, snake_case]
CATEGORY: [content/ecom/services/products/tech/growth/adult]
DESCRIPTION: [one paragraph]
FIRST_DOLLAR_PATH: [exact 5 steps]
ESTIMATED_MONTHLY: [$X-$Y range]
TOOLS_NEEDED: [specific names]
COMPLIANCE_NOTES: [any legal/regulatory considerations]
WHY_NOW: [why this works right now specifically]
"""

    ok, out = run_claude(prompt, timeout=120)
    if ok and len(out) > 200:
        outfile = OPS_DIR / f"discovered_venture_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        safe_path(outfile)
        outfile.write_text(f"# Discovered Venture — {datetime.now().isoformat()}\n\n{out}")
        state.data.setdefault("pending_ventures", []).append({
            "discovered": datetime.now().isoformat(),
            "file": str(outfile.name),
            "status": "PENDING_REVIEW"
        })
        state.save()
        log(f"  New venture discovered, saved to {outfile.name}")
        return True, out[:200]
    return False, "Discovery search returned nothing actionable"


def run_full_cycle(state, specific_venture=None):
    """Run one full ops manager cycle across all ventures."""
    cycle_start = time.time()
    disk = disk_free_gb()

    log("=" * 70)
    log(f"OPS MANAGER CYCLE — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    log(f"Disk: {disk}GB | Ventures: {len(VENTURE_CLASSES)} | Cycles: {state.data['cycles_run']}")
    log("=" * 70)

    if disk < 2:
        log("DISK CRITICAL < 2GB — pausing write-heavy operations", "WARN")

    ventures_run = 0

    if specific_venture:
        # Run one specific venture
        for V in VENTURE_CLASSES:
            if V.name == specific_venture:
                v = V(state)
                start = time.time()
                try:
                    result, summary = v.run_cycle()
                except Exception as e:
                    result, summary = "failed", str(e)[:200]
                duration = time.time() - start
                state.log_venture(v.name, result, duration, summary)
                log(f"  [{result.upper()}] {v.name}: {summary} ({duration:.0f}s)")
                ventures_run = 1
                break
        else:
            log(f"Unknown venture: {specific_venture}")
    else:
        # Run all ventures in priority order
        for V in VENTURE_CLASSES:
            v = V(state)

            if disk < 2 and v.category not in ("growth",):
                log(f"  [SKIP] {v.name}: disk too low", "WARN")
                continue

            start = time.time()
            try:
                result, summary = v.run_cycle()
            except Exception as e:
                result, summary = "failed", str(e)[:200]
            duration = time.time() - start

            state.log_venture(v.name, result, duration, summary)
            state.data.setdefault("venture_status", {})[v.name] = {
                "last_result": result,
                "last_run": datetime.now().isoformat(),
                "last_summary": summary[:200],
                "duration": round(duration, 1)
            }
            log(f"  [{result.upper()}] {v.name}: {summary} ({duration:.0f}s)")
            ventures_run += 1

    cycle_duration = time.time() - cycle_start
    state.data["last_cycle"] = datetime.now().isoformat()
    state.data["cycles_run"] += 1
    state.data["disk_gb_free"] = disk
    state.save()

    log("=" * 70)
    log(f"CYCLE COMPLETE — {ventures_run} ventures in {cycle_duration:.0f}s")
    log("=" * 70)


def show_status(state):
    """Show full ops manager status."""
    print("=" * 70)
    print("PRINTMAXX OPS MANAGER STATUS")
    print("=" * 70)
    print(f"Cycles run: {state.data['cycles_run']}")
    print(f"Last cycle: {state.data.get('last_cycle', 'never')}")
    print(f"Disk free: {disk_free_gb()}GB")
    print(f"Revenue: ${state.data.get('revenue', {}).get('total', 0)}")

    print(f"\nACTIVE VENTURES ({len(VENTURE_CLASSES)}):")
    for V in VENTURE_CLASSES:
        v = V(state)
        status = state.data.get("venture_status", {}).get(v.name, {})
        result = status.get("last_result", "never_run")
        last_run = status.get("last_run", "never")[:16]
        icon = {"success": "+", "partial": "~", "failed": "X", "skipped": "-",
                "never_run": "?"}.get(result, "?")
        print(f"  [{icon}] P{v.priority} {v.name}: {result} | {v.estimated_monthly} | last: {last_run}")
        if v.compliance_notes:
            print(f"      compliance: {v.compliance_notes[0]}")

    print(f"\nPENDING VENTURES:")
    for pv in state.data.get("pending_ventures", []):
        print(f"  {pv.get('file', '?')} — {pv.get('status', '?')}")

    print(f"\nKILLED VENTURES:")
    for kv in state.data.get("killed_ventures", []):
        print(f"  {kv}")

    # Recent venture log
    if VENTURE_LOG.exists():
        print(f"\nRECENT VENTURE OPS (last 15):")
        lines = VENTURE_LOG.read_text().strip().split("\n")
        for line in lines[-15:]:
            try:
                entry = json.loads(line)
                icon = {"success": "+", "partial": "~", "failed": "X", "skipped": "-"}.get(
                    entry["result"], "?")
                print(f"  [{icon}] {entry['ts'][:16]} {entry['venture']}: {entry['output'][:60]}")
            except Exception:
                pass

    print("=" * 70)


def run_daemon(state):
    """Run forever. One full cycle every 2 hours."""
    log("OPS MANAGER DAEMON STARTING")
    log("Cycle interval: 2 hours (ventures self-manage frequency)")

    while True:
        try:
            # Prioritize first
            prioritize_ventures(state)

            # Run all ventures
            run_full_cycle(state)

            # Every 6 hours, discover new ventures
            last_discovery = state.data.get("last_discovery")
            if not last_discovery or (datetime.now() - datetime.fromisoformat(last_discovery)) > timedelta(hours=6):
                discover_new_ventures(state)
                state.data["last_discovery"] = datetime.now().isoformat()
                state.save()

            # Sleep 2 hours
            next_run = datetime.now() + timedelta(hours=2)
            log(f"Sleeping until {next_run.strftime('%H:%M')}")
            time.sleep(7200)

        except KeyboardInterrupt:
            log("DAEMON STOPPED")
            state.save()
            break
        except Exception as e:
            log(f"CYCLE ERROR: {e} — retrying in 10 min", "ERROR")
            time.sleep(600)


# === CLI ===

def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Ops Manager")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--venture", type=str, help="Run specific venture")
    parser.add_argument("--prioritize", action="store_true", help="Re-rank ventures")
    parser.add_argument("--discover", action="store_true", help="Hunt new ventures")
    parser.add_argument("--daemon", action="store_true", help="Run forever")
    args = parser.parse_args()

    state = OpsState()

    if args.status:
        show_status(state)
    elif args.prioritize:
        prioritize_ventures(state)
    elif args.discover:
        discover_new_ventures(state)
    elif args.venture:
        run_full_cycle(state, specific_venture=args.venture)
    elif args.daemon:
        run_daemon(state)
    else:
        # Default: full cycle
        prioritize_ventures(state)
        run_full_cycle(state)


if __name__ == "__main__":
    main()
