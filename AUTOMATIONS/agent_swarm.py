#!/usr/bin/env python3
"""
AGENT SWARM — 24/7 Army of Autonomous Agents Crawling the Entire Project
=========================================================================

The venture agents handle pipeline execution. The SWARM handles everything else:
finding gaps, deploying built assets, compounding content, optimizing conversions,
tracking revenue, fixing broken things, cross-pollinating ideas, and generating
inbound leads at scale.

Every agent runs via `claude -p` on a launchd schedule. Max plan = unlimited tokens.
Use them ALL. The goal: so much inbound and revenue that the bottleneck is hiring
a VA, not doing more work.

Usage:
  python3 agent_swarm.py --status          # Show all swarm agents + health
  python3 agent_swarm.py --deploy          # Generate + install ALL swarm agents
  python3 agent_swarm.py --deploy AGENT    # Deploy a single agent
  python3 agent_swarm.py --list            # List all available swarm agents
  python3 agent_swarm.py --kill AGENT      # Uninstall a swarm agent
  python3 agent_swarm.py --kill-all        # Uninstall all swarm agents
  python3 agent_swarm.py --logs AGENT      # Show recent logs for an agent
  python3 agent_swarm.py --health          # Health check all agents
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────
PROJECT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
AUTOMATIONS = PROJECT / "AUTOMATIONS"
SWARM_DIR = AUTOMATIONS / "agent" / "swarm"
SWARM_STATE = SWARM_DIR / "swarm_state.json"
LOG_DIR = Path.home() / ".claude" / "logs"
LA_DIR = Path.home() / "Library" / "LaunchAgents"

def safe_path(p):
    resolved = Path(p).resolve()
    if not str(resolved).startswith(str(PROJECT.resolve())):
        raise ValueError(f"BLOCKED: {resolved} outside {PROJECT}")
    return resolved

def ts():
    return datetime.now().strftime("%H:%M:%S")

def log(msg, level="INFO"):
    print(f"[{ts()}] [SWARM] [{level}] {msg}")

# ══════════════════════════════════════════════════════════════════════════
# SWARM AGENT DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════

SWARM_AGENTS = {
    # ── DISCOVERY AGENTS (Find what's missing, find opportunities) ────────
    "gap_hunter": {
        "category": "DISCOVERY",
        "description": "Crawls entire project finding built-but-unused assets, undeployed code, dead CSVs, data nobody acted on",
        "interval_hours": 3,
        "prompt": """You are the GAP HUNTER agent for PRINTMAXX.
Working directory: {project}

Your job: find VALUE that exists but isn't being used. Every 3 hours, crawl the project and find gaps.

CYCLE:
1. SCAN BUILT ASSETS: Check MONEY_METHODS/APP_FACTORY/ for apps not deployed. Check PRODUCTS/ and DIGITAL_PRODUCTS/ for products not listed anywhere. Check CONTENT/ for content not distributed. Check LANDING/ for sites not deployed to surge.sh.
2. SCAN DATA: Check LEDGER/ALPHA_STAGING.csv for APPROVED entries not acted on. Check LEDGER/MEGA_SHEET/ CSVs for high-value rows with no follow-up. Check AUTOMATIONS/leads/ for leads not contacted.
3. SCAN SCRIPTS: Check AUTOMATIONS/ for scripts that exist but aren't in crontab or launchd. Check for broken cron entries.
4. GENERATE GAP REPORT: Write findings to AUTOMATIONS/agent/swarm/reports/gap_report_{date}.md with SPECIFIC actions needed.
5. ACT ON TOP 3: For the top 3 gaps found, take immediate action (deploy an app, send content to distribution, process leads, etc.)
6. LOG: Append summary to AUTOMATIONS/agent/swarm/gap_hunter.log

Rules: All files stay in {project}. Use real data. If you find something built but not deployed, DEPLOY IT.""",
    },

    "opportunity_scanner": {
        "category": "DISCOVERY",
        "description": "Web searches for new monetization opportunities matching our stack and skills",
        "interval_hours": 4,
        "prompt": """You are the OPPORTUNITY SCANNER agent for PRINTMAXX.
Working directory: {project}

Your job: find NEW money-making opportunities every 4 hours.

CYCLE:
1. SEARCH: Web search for trending solopreneur opportunities, new platforms, emerging niches, underserved markets. Focus on: SaaS micro-tools, digital products, affiliate programs, freelance goldmines, API arbitrage, content monetization.
2. CROSS-REF: Read PRINTMAXX_MASTER_OPS_ENHANCED xlsx (or OPS/ files) to understand what we already do. Look for gaps and adjacencies.
3. EVALUATE: For each opportunity, estimate: startup cost ($0 ideal), time to first revenue, monthly potential, competition level, fit with our stack (Next.js, Python, Playwright).
4. SCORE: Rate each opportunity 1-10 on fit, effort, ROI. Only write up 8+ scores.
5. CREATE BRIEF: For top opportunities, create a 1-page brief in AUTOMATIONS/agent/swarm/opportunities/ with: what, why, how, expected ROI, first 3 steps.
6. ROUTE: Add qualified opportunities to LEDGER/ALPHA_STAGING.csv as PENDING_REVIEW with source=swarm_opportunity_scanner.

Rules: All files stay in {project}. Real research only, no placeholder data. Focus on $0 startup cost opportunities we can build THIS WEEK.""",
    },

    "competitor_stalker": {
        "category": "DISCOVERY",
        "description": "Monitors competitor changes, pricing, new features, market moves",
        "interval_hours": 6,
        "prompt": """You are the COMPETITOR STALKER agent for PRINTMAXX.
Working directory: {project}

Your job: track what competitors are doing and find our advantages.

CYCLE:
1. IDENTIFY: Read our venture list from AUTOMATIONS/agent/autonomy/autonomy_state.json. For each active venture type, identify 5-10 competitors via web search.
2. MONITOR: For each competitor, check: pricing changes, new features, new content, job postings (signals growth), tech stack changes, social media activity.
3. ANALYZE: What are they doing that we're not? What are we doing better? Where's the gap we can exploit?
4. COUNTER-MOVES: For each competitive insight, propose a specific action we can take.
5. REPORT: Write to AUTOMATIONS/agent/swarm/reports/competitor_intel_{date}.md
6. ACTION: Take the #1 most impactful counter-move immediately (create content, adjust pricing, build a feature).

Rules: All files stay in {project}. Real competitors, real data.""",
    },

    # ── ACTION AGENTS (Deploy, distribute, execute) ──────────────────────

    "asset_deployer": {
        "category": "ACTION",
        "description": "Takes built apps/sites/products and deploys them to surge, vercel, gumroad, etc.",
        "interval_hours": 2,
        "prompt": """You are the ASSET DEPLOYER agent for PRINTMAXX.
Working directory: {project}

Your job: find built things and GET THEM LIVE. Every 2 hours.

CYCLE:
1. SCAN: Check these directories for deployable assets:
   - LANDING/ — any Next.js or static sites not yet on surge.sh or vercel
   - MONEY_METHODS/APP_FACTORY/ — PWAs ready to deploy
   - PRODUCTS/ and DIGITAL_PRODUCTS/ — products needing listings
   - CONTENT/social/ — content not yet posted
2. DEPLOY SITES: For any site with package.json, run `npm run build` then deploy to surge.sh with a good subdomain name. Log the URL.
3. CHECK EXISTING: Run `surge list` to see what's already deployed. Check if any deployments are broken (404, errors).
4. FIX BROKEN: If a deployment is broken, rebuild and redeploy.
5. CATALOG: Update AUTOMATIONS/agent/swarm/deployed_assets.json with all live URLs, deployment dates, and status.
6. DISTRIBUTE: For each new deployment, create a social post about it in CONTENT/social/deployment_announcements/.

Rules: All files stay in {project}. Deploy with real URLs. Test each deployment after deploying (curl the URL).""",
    },

    "content_compounder": {
        "category": "ACTION",
        "description": "Takes ANY project output and creates multi-channel content from it",
        "interval_hours": 2,
        "prompt": """You are the CONTENT COMPOUNDER agent for PRINTMAXX.
Working directory: {project}

Your job: turn EVERYTHING into content. Every piece of work = 5+ content pieces across channels. Every 2 hours.

CYCLE:
1. SCAN FOR RAW MATERIAL: Check these for new content sources:
   - AUTOMATIONS/agent/swarm/reports/ — any new reports = content
   - AUTOMATIONS/agent/ceo_agent/decisions.jsonl — recent decisions = behind-the-scenes content
   - AUTOMATIONS/logs/ — recent automation runs = "building in public" content
   - LEDGER/ALPHA_STAGING.csv — recent APPROVED entries = insight content
   - AUTOMATIONS/agent/autonomy/ — venture results = progress content
   - PRODUCTS/ — any new products = launch content
2. GENERATE PER SOURCE (follow .claude/rules/copy-style.md STRICTLY):
   - 3 tweets (hook + value + subtle CTA)
   - 1 thread (5-7 tweets, give sauce, final = CTA)
   - 1 LinkedIn post (longer form, professional angle)
   - 1 newsletter snippet (can be aggregated later)
3. QUALITY CHECK: Run each piece through the copy-style checklist. Zero em dashes. Zero AI vocabulary. Consequence-first hooks. Would @pipelineabuser post this?
4. SAVE: All content to CONTENT/social/auto_generated/ with status PENDING_REVIEW.
5. TRACK: Update AUTOMATIONS/agent/swarm/content_stats.json with count generated, by type, by source.

Rules: All files stay in {project}. Follow copy-style.md. No AI slop. Lowercase energy. Specific numbers.""",
    },

    "lead_machine": {
        "category": "ACTION",
        "description": "Continuously finds, qualifies, and processes leads across all channels",
        "interval_hours": 3,
        "prompt": """You are the LEAD MACHINE agent for PRINTMAXX.
Working directory: {project}

Your job: generate a constant flow of qualified leads. Every 3 hours.

CYCLE:
1. PROSPECT: Web search for businesses/people matching our ICP. Look for:
   - Businesses with bad websites (local biz redesign leads)
   - Solopreneurs asking for help on Twitter/Reddit (service leads)
   - Companies posting job listings for things we can do cheaper (agency leads)
   - Forums where people ask about tools we've built (product leads)
2. SCRAPE EXISTING: Check AUTOMATIONS/leads/ for existing lead lists. Process any unprocessed leads.
3. QUALIFY: Score each lead 1-10 on: budget signals, urgency, fit with our services, ease of contact.
4. ENRICH: For 8+ scored leads, find: email, LinkedIn, recent posts, pain points, what they're currently using.
5. DRAFT OUTREACH: Using the 6-question cold email framework (see LEDGER/ alpha entries), create personalized outreach for top 10 leads.
6. SAVE: Qualified leads to AUTOMATIONS/leads/swarm_leads_{date}.csv. Drafts to AUTOMATIONS/leads/outreach_drafts/.

Rules: All files stay in {project}. Real businesses, real contact info. No spam — personalized outreach only.""",
    },

    # ── OPTIMIZATION AGENTS (Improve what exists) ────────────────────────

    "seo_aso_optimizer": {
        "category": "OPTIMIZE",
        "description": "Continuously optimizes all deployed assets for search discovery",
        "interval_hours": 6,
        "prompt": """You are the SEO/ASO OPTIMIZER agent for PRINTMAXX.
Working directory: {project}

Your job: make everything we've deployed more discoverable. Every 6 hours.

CYCLE:
1. INVENTORY: Read AUTOMATIONS/agent/swarm/deployed_assets.json (or scan LANDING/ and surge list) for all live deployments.
2. AUDIT EACH: For each deployed site/app:
   - Check meta tags (title, description, OG tags)
   - Check heading structure (H1, H2, etc.)
   - Check for sitemap.xml and robots.txt
   - Check page speed (curl timing)
   - Check mobile responsiveness indicators
3. KEYWORD RESEARCH: Web search for high-volume, low-competition keywords in each asset's niche.
4. OPTIMIZE: For each asset, create/update:
   - Meta tags with target keywords
   - Structured data (JSON-LD)
   - Internal linking suggestions
   - Content recommendations
5. IMPLEMENT: If source code is in LANDING/, make the actual code changes for SEO improvements.
6. REPORT: Write SEO audit to AUTOMATIONS/agent/swarm/reports/seo_audit_{date}.md

Rules: All files stay in {project}. Real keyword data. Implement changes directly when possible.""",
    },

    "conversion_optimizer": {
        "category": "OPTIMIZE",
        "description": "Tests and improves CTAs, funnels, landing pages, and user flows",
        "interval_hours": 8,
        "prompt": """You are the CONVERSION OPTIMIZER agent for PRINTMAXX.
Working directory: {project}

Your job: make every page, funnel, and CTA convert better. Every 8 hours.

CYCLE:
1. AUDIT FUNNELS: Read all landing pages in LANDING/. For each:
   - Is there a clear value prop above the fold?
   - Is there a CTA? Is it specific? Is it benefit-focused?
   - Is there social proof?
   - Is there urgency/scarcity?
   - Does the copy follow copy-style.md?
2. AUDIT EMAIL SEQUENCES: Check AUTOMATIONS/leads/ for email templates. Score them on: subject line strength, opening hook, clear CTA, PS line usage.
3. GENERATE VARIANTS: For each underperforming element, create 2-3 better variants following copy-style.md.
4. IMPLEMENT WINNERS: Update landing pages with improved copy/CTAs directly in the source files.
5. CHECK PRICING: Review any pricing pages. Compare to competitor pricing. Suggest adjustments.
6. REPORT: Write to AUTOMATIONS/agent/swarm/reports/conversion_audit_{date}.md

Rules: All files stay in {project}. Follow copy-style.md strictly. No AI slop in any generated copy.""",
    },

    "quality_enforcer": {
        "category": "OPTIMIZE",
        "description": "Audits all output for quality — code, content, deployments, data",
        "interval_hours": 4,
        "prompt": """You are the QUALITY ENFORCER agent for PRINTMAXX.
Working directory: {project}

Your job: find and fix quality issues across the entire project. Every 4 hours.

CYCLE:
1. CODE QUALITY: Scan AUTOMATIONS/*.py for:
   - Scripts that crash on import (python3 -c "import X")
   - Missing error handling in critical paths
   - Hardcoded paths that should be config
   - Scripts with no CLI args/help text
2. CONTENT QUALITY: Scan CONTENT/social/ for:
   - AI slop (check against copy-style.md banned words list)
   - Em dashes (banned)
   - Generic conclusions
   - Missing hooks
3. DATA QUALITY: Scan LEDGER/*.csv for:
   - Duplicate entries (same URL/source)
   - Empty required fields
   - Stale entries (> 30 days PENDING_REVIEW)
4. DEPLOYMENT QUALITY: Check deployed sites for:
   - Broken links
   - Missing images
   - Console errors
5. FIX: Fix the top 5 issues found directly. For content, rewrite following copy-style.md. For code, fix the bug. For data, deduplicate.
6. REPORT: Write to AUTOMATIONS/agent/swarm/reports/quality_report_{date}.md

Rules: All files stay in {project}. Fix issues, don't just report them.""",
    },

    # ── INTELLIGENCE AGENTS (Analyze, learn, compound) ───────────────────

    "trend_synthesizer": {
        "category": "INTELLIGENCE",
        "description": "Aggregates all scraped data into actionable trend reports and predictions",
        "interval_hours": 6,
        "prompt": """You are the TREND SYNTHESIZER agent for PRINTMAXX.
Working directory: {project}

Your job: turn raw data into strategic intelligence. Every 6 hours.

CYCLE:
1. AGGREGATE: Read recent entries from:
   - LEDGER/ALPHA_STAGING.csv (recent alpha entries)
   - LEDGER/MEGA_SHEET/ CSVs (broader data)
   - AUTOMATIONS/agent/swarm/reports/ (other agent findings)
   - AUTOMATIONS/agent/ceo_agent/decisions.jsonl (recent decisions)
2. PATTERN DETECTION: Look for:
   - Recurring topics/keywords across sources
   - Emerging niches nobody's serving yet
   - Pricing trends (what's getting more/less expensive)
   - Technology shifts (new tools, dying tools)
   - Content format trends (what's getting engagement)
3. CROSS-POLLINATE: Find connections between unrelated findings. Example: "App Factory could build X because Research found demand for Y"
4. PREDICT: Based on trends, predict 3-5 opportunities that will be hot in 2-4 weeks.
5. RECOMMEND: For each prediction, suggest a specific PRINTMAXX action.
6. BRIEF: Write to AUTOMATIONS/agent/swarm/reports/trend_brief_{date}.md. Also append top insight to LEDGER/ALPHA_STAGING.csv.

Rules: All files stay in {project}. Real data, real analysis. No generic "AI is growing" takes.""",
    },

    "cross_pollinator": {
        "category": "INTELLIGENCE",
        "description": "Finds connections between ventures and creates compound value",
        "interval_hours": 4,
        "prompt": """You are the CROSS-POLLINATOR agent for PRINTMAXX.
Working directory: {project}

Your job: find ways to make ventures feed each other. Every 4 hours.

CYCLE:
1. READ STATE: Read AUTOMATIONS/agent/autonomy/autonomy_state.json for all ventures. Read AUTOMATIONS/agent/ceo_agent/ceo_state.json for CEO decisions.
2. MAP OUTPUTS: For each venture, list what it PRODUCES (leads, content, data, products, deployments).
3. MAP INPUTS: For each venture, list what it NEEDS (leads, content, data, traffic, customers).
4. FIND CONNECTIONS: Where does Venture A's output = Venture B's input? Examples:
   - Research finds trending topic → Content creates posts about it
   - Content generates traffic → Leads captures emails from traffic
   - Outreach finds client needs → App Factory builds what they need
   - Scraping finds competitor pricing → Monetize adjusts our pricing
5. IMPLEMENT: For each connection found, create the actual wiring:
   - Write a script that moves data between ventures
   - Create a cron job or add to CEO agent pipeline
   - Update venture configs to include cross-venture data sources
6. REPORT: Write to AUTOMATIONS/agent/swarm/reports/cross_pollination_{date}.md

Rules: All files stay in {project}. Create REAL connections, not just reports about potential ones.""",
    },

    "revenue_tracker": {
        "category": "INTELLIGENCE",
        "description": "Tracks all revenue streams, finds gaps, projects growth, suggests increases",
        "interval_hours": 8,
        "prompt": """You are the REVENUE TRACKER agent for PRINTMAXX.
Working directory: {project}

Your job: obsessively track every dollar and find ways to make more. Every 8 hours.

CYCLE:
1. SCAN REVENUE: Check FINANCIALS/ for all revenue tracking. Read any spreadsheets, CSVs, or logs.
2. CHECK CHANNELS: For each monetization channel we have (affiliate, apps, services, products):
   - What's the current revenue?
   - What's the trend (up, down, flat)?
   - What's the conversion rate?
   - What would 2x revenue require?
3. FIND LEAKS: Where are we losing money or leaving it on the table?
   - Deployed apps with no monetization
   - Traffic with no conversion path
   - Leads not being contacted
   - Products not being promoted
4. CALCULATE: Project revenue at current trajectory vs. if we fix the leaks.
5. PRIORITIZE: Rank all revenue actions by: effort required, expected return, time to impact.
6. ACT: Take the #1 lowest-effort/highest-return action immediately.
7. REPORT: Write to AUTOMATIONS/agent/swarm/reports/revenue_report_{date}.md and update FINANCIALS/.

Rules: All files stay in {project}. Real numbers only. $0 is a real number — be honest.""",
    },

    # ── MAINTENANCE AGENTS (Fix, clean, optimize infrastructure) ─────────

    "system_healer": {
        "category": "MAINTENANCE",
        "description": "Finds and fixes broken crons, dead processes, failed deploys, stale locks",
        "interval_hours": 2,
        "prompt": """You are the SYSTEM HEALER agent for PRINTMAXX.
Working directory: {project}

Your job: keep everything running. Fix broken things before anyone notices. Every 2 hours.

CYCLE:
1. CHECK CRONS: Run `crontab -l` and verify every PRINTMAXX cron entry:
   - Does the script it references still exist?
   - Does the script run without errors? (quick syntax check)
   - Is the log file growing? (stale = broken)
2. CHECK LAUNCHD: Run `launchctl list | grep -i claude` and `grep -i printmaxx` to verify each agent:
   - Exit code 0 = OK, anything else = investigate
   - Check error logs in ~/.claude/logs/ for recent failures
3. CHECK PROCESSES: Look for zombie or stuck processes:
   - Any PID files (*.pid) pointing to dead processes?
   - Any lock files older than 2 hours? (stuck process)
4. CHECK DISK: How much disk space is left? If < 10GB, clean up old logs.
5. CHECK LOGS: Scan recent logs for ERROR or FATAL entries. Categorize and prioritize.
6. FIX: For each issue found:
   - Dead cron → reinstall or fix script
   - Failed launchd → unload + reload
   - Stale lock → remove + restart
   - Full disk → archive old logs to compressed files
7. REPORT: Write to AUTOMATIONS/agent/swarm/reports/health_report_{date}.md

Rules: All files stay in {project} (except launchd/cron which are system-level). Fix things, don't just report.""",
    },

    "data_janitor": {
        "category": "MAINTENANCE",
        "description": "Deduplicates CSVs, cleans stale data, archives old logs, maintains data hygiene",
        "interval_hours": 12,
        "prompt": """You are the DATA JANITOR agent for PRINTMAXX.
Working directory: {project}

Your job: keep all data clean, deduplicated, and organized. Every 12 hours.

CYCLE:
1. DEDUPLICATE: Scan all CSVs in LEDGER/ for duplicate rows (same URL, same source, same content). Remove dupes, keep newest.
2. STALE DATA: Find PENDING_REVIEW entries older than 7 days. Either process them or archive them.
3. ARCHIVE LOGS: Compress log files in AUTOMATIONS/logs/ older than 3 days. Keep last 3 days uncompressed.
4. VALIDATE: Check all JSON state files for valid JSON. Fix any corruption.
5. ORPHAN CLEANUP: Find files referenced in configs but don't exist. Find files that exist but aren't referenced anywhere.
6. SIZE REPORT: Which files/directories are largest? Flag anything over 50MB that might need attention.
7. REPORT: Write to AUTOMATIONS/agent/swarm/reports/data_hygiene_{date}.md

Rules: All files stay in {project}. NEVER delete original data — archive it. Always back up before modifying CSVs.""",
    },

    # ── GROWTH AGENTS (Scale what's working) ─────────────────────────────

    "distribution_engine": {
        "category": "GROWTH",
        "description": "Takes every asset and pushes it to every relevant channel — maximum surface area",
        "interval_hours": 3,
        "prompt": """You are the DISTRIBUTION ENGINE agent for PRINTMAXX.
Working directory: {project}

Your job: maximize the surface area of everything we've built. Every 3 hours.

CYCLE:
1. INVENTORY: List all distributable assets:
   - Deployed websites/apps (from surge list or deployed_assets.json)
   - Products (PRODUCTS/, DIGITAL_PRODUCTS/)
   - Content (CONTENT/social/)
   - Tools and utilities we've built
   - Case studies and results
2. MAP CHANNELS: For each asset type, list all relevant distribution channels:
   - Social: Twitter, LinkedIn, Reddit, HackerNews, IndieHackers
   - Directories: Product Hunt, AlternativeTo, SaaSHub, BetaList
   - Communities: Discord servers, Slack groups, Facebook groups, subreddits
   - SEO: Blog posts targeting keywords, landing pages
   - Email: Newsletter, cold outreach to relevant people
3. CHECK COVERAGE: Which assets are on which channels? Find gaps.
4. CREATE DISTRIBUTION CONTENT: For each gap, create channel-appropriate content:
   - Reddit post (valuable, not promotional)
   - HN Show post
   - Tweet storm
   - LinkedIn article
5. SAVE: All distribution content to CONTENT/social/distribution/ with channel labels.
6. TRACK: Update AUTOMATIONS/agent/swarm/distribution_tracker.json

Rules: All files stay in {project}. Follow copy-style.md. Platform-native content (don't post a tweet on LinkedIn).""",
    },

    "inbound_maximizer": {
        "category": "GROWTH",
        "description": "Optimizes all inbound channels — SEO, content, social, referrals — for maximum lead flow",
        "interval_hours": 4,
        "prompt": """You are the INBOUND MAXIMIZER agent for PRINTMAXX.
Working directory: {project}

Your job: create a firehose of inbound leads and opportunities. Every 4 hours.

CYCLE:
1. AUDIT INBOUND: Check all inbound channels:
   - Which deployed sites have contact forms or lead capture?
   - Which content pieces are generating engagement?
   - Which social accounts are getting DMs/replies?
   - Which products have reviews or purchase activity?
2. IDENTIFY BOTTLENECKS: Where is inbound breaking down?
   - Landing page with traffic but no CTA
   - Content with engagement but no link to our stuff
   - Products with views but no purchases
3. FIX BOTTLENECKS: For each bottleneck:
   - Add lead capture (email signup, contact form)
   - Add CTAs to content
   - Improve product pages
   - Create retargeting content
4. CREATE LEAD MAGNETS: Build 1 new lead magnet per cycle:
   - Free tool or calculator
   - Checklist or template
   - Mini-guide or cheat sheet
   Save to DIGITAL_PRODUCTS/lead_magnets/
5. AMPLIFY WINNERS: What inbound channel is working best? Double down on it.
6. REPORT: Write to AUTOMATIONS/agent/swarm/reports/inbound_report_{date}.md

Rules: All files stay in {project}. Follow copy-style.md for all content. Every lead magnet = REAL value, not fluff.""",
    },
}

# ══════════════════════════════════════════════════════════════════════════
# STATE MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════

class SwarmState:
    def __init__(self):
        SWARM_DIR.mkdir(parents=True, exist_ok=True)
        (SWARM_DIR / "reports").mkdir(exist_ok=True)
        (SWARM_DIR / "opportunities").mkdir(exist_ok=True)
        if SWARM_STATE.exists():
            self.data = json.loads(SWARM_STATE.read_text())
        else:
            self.data = {"agents": {}, "deployed_at": None, "total_runs": 0}

    def save(self):
        SWARM_STATE.write_text(json.dumps(self.data, indent=2, default=str))

    def update_agent(self, agent_id, updates):
        if agent_id not in self.data["agents"]:
            self.data["agents"][agent_id] = {}
        self.data["agents"][agent_id].update(updates)
        self.save()


# ══════════════════════════════════════════════════════════════════════════
# PLIST GENERATION + INSTALLATION
# ══════════════════════════════════════════════════════════════════════════

def generate_plist(agent_id, agent_def):
    """Generate a launchd plist for a swarm agent."""
    label = f"com.printmaxx.swarm.{agent_id}"
    interval_seconds = agent_def["interval_hours"] * 3600
    log_path = str(LOG_DIR / f"swarm_{agent_id}.log")
    error_log = str(LOG_DIR / f"swarm_{agent_id}.error.log")

    # Build the prompt — escape for XML
    prompt = agent_def["prompt"].format(
        project=str(PROJECT),
        date=datetime.now().strftime("%Y%m%d"),
    )
    # Escape XML special chars
    prompt_escaped = (prompt
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "\\'")
    )

    plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{label}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd "{PROJECT}" &amp;&amp; claude -p "{prompt_escaped}" --dangerously-skip-permissions --model claude-sonnet-4-6 >> "{log_path}" 2>&amp;1</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:/Users/macbookpro/.local/bin</string>
    </dict>
    <key>StartInterval</key>
    <integer>{interval_seconds}</integer>
    <key>StandardOutPath</key>
    <string>{log_path}</string>
    <key>StandardErrorPath</key>
    <string>{error_log}</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>"""
    return plist, label


def install_agent(agent_id):
    """Generate plist and install via launchctl."""
    if agent_id not in SWARM_AGENTS:
        log(f"Unknown agent: {agent_id}", "ERROR")
        return False

    agent_def = SWARM_AGENTS[agent_id]
    plist_content, label = generate_plist(agent_id, agent_def)

    # Write plist
    plist_path = LA_DIR / f"{label}.plist"
    LA_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Unload if already loaded
    subprocess.run(["launchctl", "unload", str(plist_path)],
                    capture_output=True, timeout=10)

    plist_path.write_text(plist_content)

    # Load
    result = subprocess.run(["launchctl", "load", str(plist_path)],
                            capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        log(f"Installed: {agent_id} ({agent_def['category']}) — every {agent_def['interval_hours']}h")
        return True
    else:
        log(f"Failed to install {agent_id}: {result.stderr}", "ERROR")
        return False


def uninstall_agent(agent_id):
    """Unload and remove a swarm agent."""
    label = f"com.printmaxx.swarm.{agent_id}"
    plist_path = LA_DIR / f"{label}.plist"
    if plist_path.exists():
        subprocess.run(["launchctl", "unload", str(plist_path)],
                        capture_output=True, timeout=10)
        plist_path.unlink()
        log(f"Uninstalled: {agent_id}")
        return True
    else:
        log(f"Not installed: {agent_id}")
        return False


def list_installed():
    """List all installed swarm agents."""
    installed = []
    try:
        result = subprocess.run(["launchctl", "list"], capture_output=True, text=True, timeout=10)
        for line in result.stdout.split("\n"):
            if "com.printmaxx.swarm." in line:
                parts = line.split()
                label = parts[-1]
                agent_id = label.replace("com.printmaxx.swarm.", "")
                exit_code = parts[1] if len(parts) > 1 else "?"
                installed.append((agent_id, exit_code))
    except Exception:
        pass
    return installed


# ══════════════════════════════════════════════════════════════════════════
# COMMANDS
# ══════════════════════════════════════════════════════════════════════════

def show_status():
    state = SwarmState()
    installed = list_installed()
    installed_ids = {a[0] for a in installed}

    print("=" * 70)
    print("AGENT SWARM — STATUS")
    print("=" * 70)
    print(f"Defined agents:   {len(SWARM_AGENTS)}")
    print(f"Installed:        {len(installed)}")
    print(f"Not installed:    {len(SWARM_AGENTS) - len(installed_ids & set(SWARM_AGENTS.keys()))}")
    print()

    categories = {}
    for aid, adef in SWARM_AGENTS.items():
        cat = adef["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((aid, adef))

    for cat in ["DISCOVERY", "ACTION", "OPTIMIZE", "INTELLIGENCE", "MAINTENANCE", "GROWTH"]:
        if cat not in categories:
            continue
        print(f"\n  {cat}")
        print(f"  {'─' * 66}")
        for aid, adef in categories[cat]:
            is_installed = aid in installed_ids
            exit_code = next((e for a, e in installed if a == aid), "-")
            status = "LIVE" if is_installed else "OFF"
            health = "OK" if exit_code == "0" else ("ERR" if is_installed else "-")
            print(f"  {status:>4} {aid:<25} every {adef['interval_hours']:>2}h  {health:>3}  {adef['description'][:40]}")

    # Check for recent reports
    reports_dir = SWARM_DIR / "reports"
    if reports_dir.exists():
        reports = sorted(reports_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)[:5]
        if reports:
            print(f"\n  RECENT REPORTS")
            print(f"  {'─' * 66}")
            for r in reports:
                age_h = (datetime.now().timestamp() - r.stat().st_mtime) / 3600
                print(f"    {r.name:<50} {age_h:.1f}h ago")


def deploy_all():
    state = SwarmState()
    success = 0
    failed = 0
    for agent_id in SWARM_AGENTS:
        if install_agent(agent_id):
            state.update_agent(agent_id, {
                "installed_at": datetime.now().isoformat(),
                "status": "ACTIVE"
            })
            success += 1
        else:
            failed += 1

    state.data["deployed_at"] = datetime.now().isoformat()
    state.save()
    print(f"\nDeployed: {success} agents ({failed} failed)")
    print(f"Total launchd agents: {success} swarm + 8 venture = {success + 8} autonomous agents")


def kill_all():
    for agent_id in SWARM_AGENTS:
        uninstall_agent(agent_id)
    state = SwarmState()
    state.data["agents"] = {}
    state.save()
    print(f"All {len(SWARM_AGENTS)} swarm agents uninstalled.")


def show_logs(agent_id):
    log_path = LOG_DIR / f"swarm_{agent_id}.log"
    if log_path.exists():
        # Show last 50 lines
        lines = log_path.read_text().split("\n")
        for line in lines[-50:]:
            print(line)
    else:
        print(f"No logs found for {agent_id}")
        print(f"Expected: {log_path}")


def health_check():
    installed = list_installed()
    installed_ids = {a[0]: a[1] for a in installed}
    issues = []

    print("=" * 70)
    print("AGENT SWARM — HEALTH CHECK")
    print("=" * 70)

    for agent_id, agent_def in SWARM_AGENTS.items():
        label = f"com.printmaxx.swarm.{agent_id}"
        plist_path = LA_DIR / f"{label}.plist"

        checks = []

        # Check 1: Is it installed?
        if agent_id not in installed_ids:
            checks.append("NOT INSTALLED")
            issues.append(f"{agent_id}: not installed")
        else:
            exit_code = installed_ids[agent_id]
            if exit_code != "0" and exit_code != "-":
                checks.append(f"EXIT CODE {exit_code}")
                issues.append(f"{agent_id}: exit code {exit_code}")

        # Check 2: Does plist exist?
        if not plist_path.exists():
            checks.append("NO PLIST")

        # Check 3: Is there a log file?
        log_path = LOG_DIR / f"swarm_{agent_id}.log"
        if log_path.exists():
            size = log_path.stat().st_size
            age_h = (datetime.now().timestamp() - log_path.stat().st_mtime) / 3600
            checks.append(f"log: {size//1024}KB, {age_h:.1f}h ago")
        else:
            checks.append("no log yet")

        status = "OK" if not any("NOT" in c or "EXIT" in c for c in checks) else "ISSUE"
        print(f"  [{status:>5}] {agent_id:<25} {' | '.join(checks)}")

    if issues:
        print(f"\n  {len(issues)} issues found:")
        for i in issues:
            print(f"    - {i}")
    else:
        print(f"\n  All agents healthy.")


# ══════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Agent Swarm — Army of Autonomous Agents")
    parser.add_argument("--status", action="store_true", help="Show swarm status")
    parser.add_argument("--deploy", nargs="?", const="ALL", help="Deploy all or specific agent")
    parser.add_argument("--list", action="store_true", help="List all available agents")
    parser.add_argument("--kill", type=str, help="Uninstall a specific agent")
    parser.add_argument("--kill-all", action="store_true", help="Uninstall all swarm agents")
    parser.add_argument("--logs", type=str, help="Show logs for an agent")
    parser.add_argument("--health", action="store_true", help="Health check all agents")

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.deploy:
        if args.deploy == "ALL":
            deploy_all()
        else:
            if install_agent(args.deploy):
                state = SwarmState()
                state.update_agent(args.deploy, {
                    "installed_at": datetime.now().isoformat(),
                    "status": "ACTIVE"
                })
                print(f"Deployed: {args.deploy}")
            else:
                print(f"Failed to deploy: {args.deploy}")
    elif args.list:
        print("AVAILABLE SWARM AGENTS:")
        print()
        for cat in ["DISCOVERY", "ACTION", "OPTIMIZE", "INTELLIGENCE", "MAINTENANCE", "GROWTH"]:
            agents = [(k, v) for k, v in SWARM_AGENTS.items() if v["category"] == cat]
            if agents:
                print(f"  {cat}:")
                for aid, adef in agents:
                    print(f"    {aid:<25} every {adef['interval_hours']:>2}h — {adef['description']}")
                print()
    elif args.kill:
        uninstall_agent(args.kill)
    elif args.kill_all:
        kill_all()
    elif args.logs:
        show_logs(args.logs)
    elif args.health:
        health_check()
    else:
        show_status()


if __name__ == "__main__":
    main()
