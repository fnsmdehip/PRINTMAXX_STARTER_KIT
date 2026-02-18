# Alpha Integration Playbooks -- Top 20 Orphaned Finding Integrations

**Generated:** 2026-02-18
**Source:** AUDIT/ALPHA_INTEGRATION_GAP_ANALYSIS.md Section 4 (Top 20 Integration Opportunities)
**Purpose:** Concrete, step-by-step playbooks to convert orphaned alpha findings into running automations and revenue

---

## How to Use This Document

Each playbook is self-contained. Pick any one, read it top to bottom, execute step by step. Playbooks are sorted into three priority tiers:

- **P0: NO BLOCKERS** -- Can be built and run RIGHT NOW with no human action, no accounts, no money
- **P1: MINOR BLOCKERS** -- Need small human action (email setup, domain config, one-time install)
- **P2: ACCOUNT-BLOCKED** -- Need human to create accounts first, then Claude can execute

Within each tier, playbooks are ordered by estimated impact descending.

---

## Quick Reference: Priority Matrix

| # | Playbook | Tier | Build Time | Monthly Value | Status |
|---|----------|------|------------|---------------|--------|
| 6 | Ralph Loop Fixer | P0 | 0 min (done) | Enables 20-40 alpha/night | ALREADY FIXED |
| 15 | MCP Tool Installer | P0 | 1 hr | $2,392/mo force multiplier | READY NOW |
| 2 | Alpha Review Automation | P0 | 3-4 hr | Clears 867 backlog | READY NOW |
| 3 | Niche Meta Detector Live Data | P0 | 1-2 hr | Real-time meta detection | READY NOW |
| 5 | Hashtag-to-Post Merger | P0 | 1 hr | 40-100% reach increase | READY NOW |
| 19 | Content QA Automation | P0 | 2-3 hr | Zero compliance violations | READY NOW |
| 8 | Cold Email Template Expander | P0 | 2 hr | 3x outreach coverage | READY NOW |
| 13 | Competitor Alert System | P0 | 3-4 hr | 24hr competitive response | READY NOW |
| 20 | Freshness Audit Automation | P0 | 2-3 hr | Fresh alpha database | READY NOW |
| 17 | Cross-Pollination Automator | P0 | 4-5 hr | Method stacking discovery | READY NOW |
| 9 | Legal Page Deployer | P1 | 1-2 hr | Unblocks 3 revenue streams | NEEDS LEGAL CONTENT |
| 4 | Email Follow-up Automation | P1 | 2-3 hr | 80% more closes | NEEDS EMAIL INFRA |
| 11 | Surge.sh to Vercel Migration | P1 | 3-4 hr | 601 pages indexed | NEEDS VERCEL LOGIN |
| 7 | Affiliate Link Auto-Inserter | P2 | 3-4 hr | $35-$5,500/mo | NEEDS AFFILIATE ACCOUNTS |
| 1 | Account Creation Automation | P2 | 2-3 hr | Unblocks everything | NEEDS HUMAN AT KEYBOARD |
| 10 | Gumroad Auto-Lister | P2 | 2-3 hr | 13 products live | NEEDS GUMROAD ACCOUNT |
| 14 | Unified Posting Automation | P2 | 4-6 hr | 13 accounts posting | NEEDS SOCIAL ACCOUNTS |
| 12 | Remotion Video Pipeline | P2 | 6-8 hr | 1-2 videos/day | NEEDS REMOTION + ACCOUNTS |
| 16 | Alpha-to-Product Pipeline | P2 | 6-8 hr | Auto micro-products | NEEDS GUMROAD ACCOUNT |
| 18 | Revenue Attribution Tracker | P2 | 3-4 hr | Revenue source intel | NEEDS REVENUE FLOWING |

---

# P0: NO BLOCKERS -- Build and Run RIGHT NOW

These playbooks require zero human action, zero accounts, zero money. Claude can pick up any of these and execute immediately.

---

## Playbook 6: Ralph Loop Fixer

### What it does
Removes the invalid `--max-tokens` flag from all ralph loop run.sh files, restoring autonomous overnight execution.

### Alpha source
- Gap Analysis 2.15: Overnight Ralph Sprint System
- Gap Analysis 1.13: Ralph Loops (12/13 originally BROKEN)

### Prerequisites
None.

### Implementation spec

**STATUS: ALREADY FIXED.** All 13 ralph loop `run.sh` files now use the correct syntax without `--max-tokens`. Verified 2026-02-18:

```bash
grep -rl "max-tokens" ralph/loops/*/run.sh
# Returns nothing -- all clean
```

Confirmed working syntax in all loops:
```bash
cat prompt.md | claude --print --dangerously-skip-permissions --model claude-opus-4-6
```

**To test a loop:**
```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
bash ralph/loops/comprehensive_alpha_research/run.sh
```

### Expected output
- 13 autonomous loops operational
- 5-8 iterations/night at $0.20-$0.50 per iteration
- 20-40 alpha entries produced per overnight session

### Revenue/impact estimate
Multiplier effect: 8+ hours/day of autonomous work. Alpha entries feed content, products, outreach.

### Build time estimate
0 min (already complete). Verification: 2 min.

### Priority tier
**P0** -- Already fixed.

---

## Playbook 15: MCP Tool Installer

### What it does
Installs MCP (Model Context Protocol) tools that give Claude direct access to browser automation, web scraping, and file management, unlocking $2,392/mo in automation value.

### Alpha source
- Gap Analysis 2.2: MCP Tools Window ($2,392/mo unrealized value, Batch 55)

### Prerequisites
- Node.js and npx available (confirmed present)
- Claude Code configured (confirmed)

### Implementation spec

**Step 1: Create installer script**

File: `AUTOMATIONS/install_mcp_tools.sh`

```bash
#!/bin/bash
set -e
echo "=== PRINTMAXX MCP Tool Installer ==="

# 1. Playwright MCP (browser automation from Claude context)
echo "[1/3] Installing Playwright MCP Server..."
npm install -g @anthropic/mcp-server-playwright 2>/dev/null || echo "  Try: npx -y @anthropic/mcp-server-playwright"

# 2. Filesystem MCP (direct file access)
echo "[2/3] Installing Filesystem MCP Server..."
npm install -g @anthropic/mcp-server-filesystem 2>/dev/null || echo "  Try: npx -y @anthropic/mcp-server-filesystem"

# 3. Fetch MCP (web fetching)
echo "[3/3] Installing Fetch MCP Server..."
npm install -g @anthropic/mcp-server-fetch 2>/dev/null || echo "  Try: npx -y @anthropic/mcp-server-fetch"

echo ""
echo "=== Installed. Configure in Claude Code MCP settings. ==="
echo "Future (after accounts): Google Sheets MCP, Buffer MCP"
```

**Step 2: Run it**
```bash
chmod +x AUTOMATIONS/install_mcp_tools.sh
bash AUTOMATIONS/install_mcp_tools.sh
```

**Step 3: Verify by checking MCP server list in Claude Code settings**

### Expected output
- Browser automation directly from Claude prompts
- Direct web fetching for real-time data
- File management via MCP

### Revenue/impact estimate
$2,392/mo estimated automation value. Playwright MCP alone automates account creation, product listing, content posting.

### Build time estimate
1 hour (install + verify + test)

### Priority tier
**P0** -- No blockers.

---

## Playbook 2: Alpha Review Automation (PENDING_REVIEW Crusher)

### What it does
Creates a Python script + cron job that auto-reviews PENDING_REVIEW alpha entries using heuristic scoring, batch-processing 50 entries per run.

### Alpha source
- Gap Analysis Section 1.10: Alpha Review Process (manual only)
- 867 PENDING_REVIEW entries in ALPHA_STAGING.csv

### Prerequisites
- `LEDGER/ALPHA_STAGING.csv` (confirmed)
- `.claude/rules/alpha-review.md` (confirmed)

### Implementation spec

**Step 1: Create `AUTOMATIONS/auto_alpha_reviewer.py`**

Core logic:
```python
# Auto-approval heuristics from alpha-review.md
NUMBER_PATTERN = re.compile(r'\$[\d,]+|\d+%|\d+x|\d+K|\d+k')
PROOF_KEYWORDS = ['screenshot', 'dashboard', 'revenue', 'github.com', 'stars', 'MRR']
BAIT_KEYWORDS = ['opportunities are insane', 'ship fast', 'the future is']

def score_entry(entry):
    content = entry.get('content', '') + ' ' + entry.get('source_content', '')
    has_numbers = bool(NUMBER_PATTERN.search(content))
    has_proof = any(kw in content.lower() for kw in PROOF_KEYWORDS)
    word_count = len(content.split())

    if has_numbers and has_proof and word_count > 30:
        return 'APPROVED', 'Auto: specific numbers + proof + substance'
    if has_numbers and word_count > 50:
        return 'APPROVED', 'Auto: specific numbers + detailed content'
    if not has_numbers and word_count < 20:
        return 'ENGAGEMENT_BAIT', 'Auto: too short, no specifics'
    return 'NEEDS_HUMAN_REVIEW', 'Ambiguous: needs human evaluation'
```

Full script reads ALPHA_STAGING.csv, processes `--batch N` PENDING_REVIEW entries, updates statuses in place, writes audit log to `AUTOMATIONS/logs/alpha_review_YYYY_MM_DD.log`.

**Step 2: Test**
```bash
python3 AUTOMATIONS/auto_alpha_reviewer.py 10
# Review first 10, check log output
```

**Step 3: Add to crontab**
```
0 6 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && /usr/bin/python3 AUTOMATIONS/auto_alpha_reviewer.py 50 >> AUTOMATIONS/logs/alpha_review_cron.log 2>&1
```

### Expected output
- 867 PENDING_REVIEW backlog cleared in ~18 runs (2-3 days at 50/run)
- Daily auto-processing of new entries from scraper pipeline
- NEEDS_HUMAN_REVIEW entries flagged for efficient batch review

### Revenue/impact estimate
Unblocks the entire alpha-to-action pipeline. Every approved entry feeds content, products, outreach.

### Build time estimate
3-4 hours

### Priority tier
**P0** -- No blockers. All input files exist.

---

## Playbook 3: Niche Meta Detector Live Data Connection

### What it does
Replaces hardcoded `SAMPLE_DATA` in `AUTOMATIONS/niche_meta_detector.py` with readers that pull from live CSVs.

### Alpha source
- Gap Analysis 2.11: Niche Meta Detector Using Sample Data

### Prerequisites
- `AUTOMATIONS/niche_meta_detector.py` (confirmed, 20KB)
- `LEDGER/ALPHA_STAGING.csv`, `LEDGER/TREND_SIGNALS.csv`, `LEDGER/ECOM_ARB_OPPORTUNITIES.csv` (all confirmed)

### Implementation spec

**Step 1: Add `load_live_data()` function after imports in niche_meta_detector.py**

```python
def load_live_data():
    """Load live data from production CSVs instead of hardcoded samples."""
    data_points = []
    # Read ALPHA_STAGING.csv (APPROVED + PENDING_REVIEW entries)
    alpha_file = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"
    if alpha_file.exists():
        with open(alpha_file, 'r') as f:
            for row in csv.DictReader(f):
                if row.get('status', '').strip() in ('APPROVED', 'PENDING_REVIEW'):
                    data_points.append({
                        'source': row.get('source', ''),
                        'content': row.get('content', '') + ' ' + row.get('source_content', ''),
                        'category': row.get('category', ''),
                        'date': row.get('date', ''),
                        'type': 'alpha'
                    })
    # Read TREND_SIGNALS.csv
    trend_file = BASE_DIR / "LEDGER" / "TREND_SIGNALS.csv"
    if trend_file.exists():
        with open(trend_file, 'r') as f:
            for row in csv.DictReader(f):
                data_points.append({
                    'source': 'trend_aggregator',
                    'content': row.get('keyword', '') + ' ' + row.get('description', ''),
                    'category': row.get('category', ''),
                    'date': row.get('date', ''),
                    'type': 'trend'
                })
    # Read ECOM_ARB_OPPORTUNITIES.csv
    ecom_file = BASE_DIR / "LEDGER" / "ECOM_ARB_OPPORTUNITIES.csv"
    if ecom_file.exists():
        with open(ecom_file, 'r') as f:
            for row in csv.DictReader(f):
                data_points.append({
                    'source': 'ecom_arb',
                    'content': row.get('product', '') + ' ' + row.get('description', ''),
                    'category': 'ECOM',
                    'date': row.get('date', ''),
                    'type': 'ecom'
                })
    return data_points
```

**Step 2: Replace all references to `SAMPLE_DATA` with `load_live_data()` calls**

**Step 3: Add `--live` CLI flag**
```python
if '--live' in sys.argv:
    data = load_live_data()
    print(f"Loaded {len(data)} live data points")
```

**Step 4: Test and add to cron**
```bash
python3 AUTOMATIONS/niche_meta_detector.py --live
```
```
0 7 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && /usr/bin/python3 AUTOMATIONS/niche_meta_detector.py --live >> AUTOMATIONS/logs/meta_detect.log 2>&1
```

### Expected output
- Pattern matching on 867+ alpha entries + 56 trend signals + 47 ecom opportunities
- Sample data found 8 meta trends. Live data should find 50+.

### Revenue/impact estimate
One correctly detected meta trend = potential $10K+ if acted on fast.

### Build time estimate
1-2 hours

### Priority tier
**P0** -- No blockers.

---

## Playbook 5: Hashtag-to-Post Merger

### What it does
Reads 210 hashtag sets, matches to 1,008 Buffer CSV posts by niche, appends platform-appropriate hashtags.

### Alpha source
- Gap Analysis 2.17: 210 Hashtag Sets Disconnected from 1,008 Posts

### Prerequisites
- `AUTOMATIONS/content_posting/` (confirmed: 11 CSVs)
- Hashtag data in `CONTENT/social/` directories

### Implementation spec

**Step 1: Create `AUTOMATIONS/hashtag_post_merger.py`**

Core logic:
- Niche-to-hashtag mapping (faith, fitness, tech, sleep, meme, finance, ecom, outbound, aesthetic, esoteric)
- Platform limits: X=3, IG=15, TikTok=5, LinkedIn=5, default=5
- Skip posts that already contain `#` (no double-tagging)
- Detect niche from content keywords, detect platform from filename

**Step 2: Dry run**
```bash
python3 AUTOMATIONS/hashtag_post_merger.py --dry-run
```

**Step 3: Execute**
```bash
python3 AUTOMATIONS/hashtag_post_merger.py
```

### Expected output
~1,008 posts enriched with niche-appropriate hashtags. Platform-specific limits enforced.

### Revenue/impact estimate
40-100% reach increase per post (documented in gap analysis).

### Build time estimate
1 hour

### Priority tier
**P0** -- No blockers.

---

## Playbook 19: Content QA Automation

### What it does
Wires `compliance_scanner.py` into content pipeline as a pre-publish gate. Auto-fixes missing disclosures. Blocks content with critical violations.

### Alpha source
- Gap Analysis Section 4 #19
- 285 CRITICAL compliance violations in existing content

### Prerequisites
- `AUTOMATIONS/compliance_scanner.py` (confirmed, ~400 lines, runs)

### Implementation spec

**Step 1: Create `AUTOMATIONS/content_compliance_gate.py`**

Core logic:
- Scan all `.md` files in `OPS/CONTENT_QA_QUEUE/`
- Run compliance_scanner.py on each
- Auto-fix: append FTC disclosure for affiliate mentions, income disclaimer for revenue claims
- Block: PII exposure, fake social proof
- Log results to `AUTOMATIONS/logs/compliance_gate_YYYY_MM_DD.log`

**Step 2: Add to cron**
```
0 8 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && /usr/bin/python3 AUTOMATIONS/content_compliance_gate.py >> AUTOMATIONS/logs/compliance_gate_cron.log 2>&1
```

### Expected output
Zero CRITICAL compliance violations in posted content. Auto-fixed disclosures. Daily audit trail.

### Revenue/impact estimate
Prevents FTC violations ($16K-$50K penalties per violation). Prevents CAN-SPAM violations ($51K per violation).

### Build time estimate
2-3 hours

### Priority tier
**P0** -- No blockers.

---

## Playbook 8: Cold Email Template Expander

### What it does
Updates `generate_cold_emails.py` to load templates from a directory instead of 6 hardcoded ones, auto-matching to lead industry.

### Alpha source
- Gap Analysis 2.6: 18 Outreach Templates Not Integrated

### Prerequisites
- `AUTOMATIONS/generate_cold_emails.py` (confirmed, 610 lines)
- Template files in `MONEY_METHODS/LOCAL_BIZ/templates/` (confirmed: dental, restaurant, fitness, legal, plumber, realtor)

### Implementation spec

**Step 1: Create `AUTOMATIONS/email_templates/` directory**

**Step 2: Extract templates from existing sources into individual `.md` files**
- One file per vertical: `dental.md`, `restaurant.md`, `fitness.md`, `legal.md`, `plumber.md`, `realtor.md`, plus 12 more from OPS/ and MONEY_METHODS/
- Each file has YAML frontmatter: `industry`, `demo_url`, `subject_line`

**Step 3: Add `load_templates()` function to generate_cold_emails.py**
```python
def load_templates(template_dir=None):
    if template_dir is None:
        template_dir = Path(__file__).parent / "email_templates"
    templates = {}
    for f in template_dir.glob('*.md'):
        templates[f.stem] = f.read_text()
    return templates
```

**Step 4: Replace hardcoded template selection with fuzzy industry matching**

**Step 5: Test**
```bash
python3 AUTOMATIONS/generate_cold_emails.py --dry-run --industry dental
python3 AUTOMATIONS/generate_cold_emails.py --dry-run --industry plumber
```

### Expected output
18+ vertical-specific templates loaded dynamically. Adding a new vertical = adding one `.md` file.

### Revenue/impact estimate
3x more targeted cold email variants. At 14% reply rate: more targeted = more replies = more $2.5K deals.

### Build time estimate
2 hours

### Priority tier
**P0** -- No blockers.

---

## Playbook 13: Competitor Alert System

### What it does
Adds price-change and launch-detection alerts to seo_competitor_analyzer.py. Triggers alerts when competitors make significant moves.

### Alpha source
- Gap Analysis 2.18: Competitor Monitoring (data collected, no alerts)

### Prerequisites
- `AUTOMATIONS/seo_competitor_analyzer.py` (confirmed, 737 lines)
- Competitor data in LEDGER/

### Implementation spec

**Step 1: Create `AUTOMATIONS/competitor_alerts.py`**

Core logic:
- Load previous competitor snapshots from `LEDGER/COMPETITOR_SNAPSHOTS.json`
- For each tracked competitor: hash current data, compare to previous hash
- Alert triggers: score change >10%, new products detected, homepage redesign
- Write alerts to `LEDGER/COMPETITOR_ALERTS.csv` with recommended response
- Save new snapshots

**Step 2: Add to cron**
```
0 10 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && /usr/bin/python3 AUTOMATIONS/competitor_alerts.py >> AUTOMATIONS/logs/competitor_alerts_cron.log 2>&1
```

### Expected output
`LEDGER/COMPETITOR_ALERTS.csv` with timestamped alerts and recommended responses.

### Revenue/impact estimate
Know within 24h when competitors make moves. Proactive instead of reactive.

### Build time estimate
3-4 hours

### Priority tier
**P0** -- No blockers.

---

## Playbook 20: Freshness Audit Automation

### What it does
Cron job that scans ALPHA_STAGING.csv for entries >30 days old, marks stale ones as NEEDS_REVALIDATION.

### Alpha source
- Gap Analysis Section 4 #20
- Max Squeeze Protocol: freshness audit cadence

### Prerequisites
- `LEDGER/ALPHA_STAGING.csv` (confirmed)

### Implementation spec

**Step 1: Create `AUTOMATIONS/alpha_freshness_auditor.py`**

Core logic:
- Parse dates in multiple formats
- Mark entries older than 30 days as `NEEDS_REVALIDATION`
- Add `freshness_status` and `last_validated` columns if missing
- Skip entries already flagged
- Weekly log to `AUTOMATIONS/logs/freshness_audit_YYYY_MM_DD.log`

**Step 2: Add to cron (weekly)**
```
30 5 * * 1 cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && /usr/bin/python3 AUTOMATIONS/alpha_freshness_auditor.py >> AUTOMATIONS/logs/freshness_cron.log 2>&1
```

### Expected output
Stale entries flagged weekly. Prevents building on dead tactics.

### Revenue/impact estimate
30 seconds of freshness check saves 6 hours of building the wrong thing.

### Build time estimate
2-3 hours

### Priority tier
**P0** -- No blockers.

---

## Playbook 17: Cross-Pollination Automator

### What it does
Reads CROSS_POLLINATION_MATRIX.csv, finds high-synergy method pairs (score >85), generates integration playbooks.

### Alpha source
- Gap Analysis Section 4 #17

### Prerequisites
- `LEDGER/CROSS_POLLINATION_MATRIX.csv` (confirmed)
- Method directories in `MONEY_METHODS/` (confirmed)

### Implementation spec

**Step 1: Create `AUTOMATIONS/cross_pollination_automator.py`**

Core logic:
- Load matrix CSV, filter pairs with synergy_score >= 85
- For each pair: generate integration playbook markdown
- Include: connection description, integration steps, implementation priority, files to connect
- Output to `OPS/cross_pollination_playbooks/`

**Step 2: Run**
```bash
python3 AUTOMATIONS/cross_pollination_automator.py
```

### Expected output
Integration playbooks for all high-synergy method pairs in `OPS/cross_pollination_playbooks/`.

### Revenue/impact estimate
Method stacking is the primary scaling lever (2x-5x individual method returns).

### Build time estimate
4-5 hours

### Priority tier
**P0** -- No blockers.

---

# P1: MINOR BLOCKERS -- Need Small Human Action

---

## Playbook 9: Legal Page Deployer

### What it does
Deploys privacy policy, terms of service, and affiliate disclosures as static pages. Unblocks App Store, email campaigns, and affiliate content simultaneously.

### Alpha source
- Gap Analysis 2.8: Legal Templates Blocking 3 Revenue Streams (1,159 lines exist)

### Prerequisites
- Legal template content (needs compilation from existing docs)
- **HUMAN ACTION:** None if using surge.sh (already have account). Vercel needs `vercel login`.

### Implementation spec

**Step 1: Create `builds/legal-pages/` with 4 HTML files**
- `privacy-policy.html` -- from existing LEGAL/ templates
- `terms-of-service.html` -- from existing LEGAL/ templates
- `affiliate-disclosure.html` -- FTC-compliant disclosure
- `income-disclaimer.html` -- earnings disclaimer

**Step 2: Deploy to surge.sh**
```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/builds/legal-pages/
npx surge . printmaxx-legal.surge.sh
```

**Step 3: Generate platform-specific snippets in `LEGAL/PLATFORM_SNIPPETS.md`**
- App Store privacy URL: `https://printmaxx-legal.surge.sh/privacy-policy.html`
- CAN-SPAM email footer block
- Social post affiliate disclosure one-liner

**Step 4: Update all PWA configs with legal URLs**

### Expected output
Legal pages live. Three revenue streams unblocked: App Store (6 apps), email (2,908 leads), affiliates (42 programs).

### Revenue/impact estimate
- App Store: 6 subscription revenue streams
- Cold email: 2,908 leads can receive emails legally
- Affiliates: 42 programs can be promoted with proper disclosure

### Build time estimate
1-2 hours

### Priority tier
**P1** -- Minor blocker: needs legal content compiled from existing docs.

---

## Playbook 4: Email Follow-up Automation

### What it does
Adds cron-triggered follow-up logic to response_tracker.py. Checks leads past Day 3/7/14 without response, queues next email.

### Alpha source
- Gap Analysis 2.9: Follow-up Timing Tables Not Programmed

### Prerequisites
- `AUTOMATIONS/response_tracker.py` (confirmed, 392 lines)
- `AUTOMATIONS/email_sender.py` (confirmed, 606 lines)
- `AUTOMATIONS/outreach/PIPELINE_TRACKER.csv` (confirmed)
- **BLOCKER:** Email infrastructure ($46/mo for DeliverOn/EmailBison)
- **HUMAN ACTION:** Purchase email warmup service, set up 3 domains

### Implementation spec

**Step 1: Create `AUTOMATIONS/auto_followup.py`**

Core logic:
- Read PIPELINE_TRACKER.csv for leads with status SENT
- Follow-up schedule: Day 3 (first), Day 7 (second), Day 14 (final)
- Templates per follow-up number (shorter each time, reference original)
- Maximum 3 follow-ups per lead
- Log to `AUTOMATIONS/logs/followup_YYYY_MM_DD.log`

**Step 2: Add to cron (activate after email infra)**
```
30 9 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && /usr/bin/python3 AUTOMATIONS/auto_followup.py >> AUTOMATIONS/logs/followup_cron.log 2>&1
```

### Expected output
Automated follow-up on 2,908 leads at optimal timing windows.

### Revenue/impact estimate
80% of sales happen on follow-up #2-5. At $2.5K average deal: even 5 more closes = $12.5K.

### Build time estimate
2-3 hours (build now, activate when email infra exists)

### Priority tier
**P1** -- Blocked on email infrastructure ($46/mo).

---

## Playbook 11: Surge.sh to Vercel Migration

### What it does
Migrates 20+ surge.sh sites to Vercel free tier, fixing robots.txt that blocks 601 SEO pages from Google.

### Alpha source
- Gap Analysis 2.14: 601 Programmatic SEO Pages Deployed, 0 Indexed

### Prerequisites
- 20+ live surge.sh sites (confirmed)
- `builds/programmatic_seo/` (confirmed, 601 pages)
- **HUMAN ACTION:** Run `vercel login` once (30-second OAuth flow in browser)

### Implementation spec

**Step 1: Human runs `vercel login`**

**Step 2: Create `AUTOMATIONS/migrate_to_vercel.sh`**

For each site:
- Generate `vercel.json` with proper `robots.txt` route and `X-Robots-Tag: index, follow` headers
- Create `robots.txt` with `Allow: /` and sitemap URL
- Run `vercel deploy --prod --yes`
- Priority: programmatic SEO site first (601 pages), then PWAs

**Step 3: Run migration**
```bash
bash AUTOMATIONS/migrate_to_vercel.sh
```

**Step 4: Verify and submit to Google Search Console**
```bash
curl -s https://printmaxx-seo.vercel.app/robots.txt
# Should show "Allow: /"
```

### Expected output
601 SEO pages indexable by Google. All PWAs on edge CDN.

### Revenue/impact estimate
601 long-tail pages for "[service] in [city]" keywords. Estimated 100-500 organic visitors/mo within 60 days. Each visitor = potential $500-$3K deal lead.

### Build time estimate
3-4 hours (after `vercel login`)

### Priority tier
**P1** -- Blocked on `vercel login` (30 seconds of human action).

---

# P2: ACCOUNT-BLOCKED -- Need Human Account Creation First

---

## Playbook 1: Account Creation Automation

### What it does
Tests and fixes `auto_account_creator.py` to open signup pages for priority accounts, pre-fill fields, pause at CAPTCHAs.

### Alpha source
- Gap Analysis Appendix B: 84% of orphaned alpha blocked by 0/49 accounts

### Prerequisites
- `AUTOMATIONS/auto_account_creator.py` (confirmed, 518 lines)
- `LEDGER/ACCOUNTS.csv` (confirmed, 49 rows)
- **HUMAN ACTION:** Must be at keyboard for CAPTCHA + email verification

### Implementation spec

**Step 1: Test with dry run**
```bash
python3 AUTOMATIONS/auto_account_creator.py --dry-run
```

**Step 2: Fix broken selectors, add error handling**

**Step 3: Run for top 10 accounts in priority order:**
1. Gumroad (13 products waiting, 5 min)
2. Buffer (1,278 posts waiting, 3 min)
3. Fiverr (11 gigs waiting, 5 min)
4. Upwork (5 profiles waiting, 10 min)
5. Email service -- SendGrid/Resend (cold email waiting, $0-$46/mo)
6. Amazon Associates (affiliate revenue, 5 min)
7. Beehiiv (4 newsletter sequences, 3 min)
8. Etsy (20 listings, 10 min)
9. Apple Developer (6 iOS apps, $99/yr)
10. Stripe (payment processing, 10 min)

**Step 4: After each account, immediately deploy waiting assets**

### Expected output
15-20 accounts created. Revenue pipeline unblocked.

### Revenue/impact estimate
- Week 1: Gumroad + Fiverr + Buffer = first $100-$500
- Month 1: + affiliates + cold email + Etsy = $1,000-$3,000
- Highest ROI action in the entire project

### Build time estimate
2-3 hr script fixes + 2-3 hr human account creation session

### Priority tier
**P2** -- Needs human at keyboard.

---

## Playbook 7: Affiliate Link Auto-Inserter

### What it does
Maps affiliate program data to content, auto-inserts appropriate links into Buffer CSVs and templates.

### Alpha source
- Gap Analysis 2.4: 200+ Affiliate Programs, 0 Applied To

### Prerequisites
- `OPS/AFFILIATE_LAUNCH_CHECKLIST.md` (confirmed, 42 programs)
- **BLOCKER:** Must sign up and get approved for programs first

### Implementation spec

**Step 1: Create `LEDGER/AFFILIATE_LINKS.csv`** with program, niche, URL, commission rate

**Step 2: Create `AUTOMATIONS/affiliate_link_inserter.py`**
- Load affiliate links from CSV
- For each Buffer CSV, detect product/tool mentions
- Insert contextually relevant affiliate link + FTC disclosure
- Skip posts already containing affiliate URLs

**Step 3: Run after accounts approved**
```bash
python3 AUTOMATIONS/affiliate_link_inserter.py --dry-run
python3 AUTOMATIONS/affiliate_link_inserter.py
```

### Expected output
Affiliate links in 50%+ of content mentioning products. FTC disclosure on every link.

### Revenue/impact estimate
$35-$5,500/mo depending on programs and traffic.

### Build time estimate
3-4 hours (after program approvals)

### Priority tier
**P2** -- Needs affiliate account approvals.

---

## Playbook 10: Gumroad Auto-Lister

### What it does
Lists all 13 products from PRODUCTS/GUMROAD_INSTANT_UPLOAD/ on Gumroad via Playwright.

### Alpha source
- Gap Analysis 2.12: 13 Gumroad Products Ready, 0 Listed

### Prerequisites
- `AUTOMATIONS/auto_list_products.py` (confirmed, Playwright-based)
- `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` (confirmed, 13 listings)
- `DIGITAL_PRODUCTS/ready_to_sell/pdfs/` (confirmed, 5 PDFs)
- **BLOCKER:** Gumroad account must exist

### Implementation spec

**Step 1: Human creates Gumroad account** (gumroad.com, 5 min)

**Step 2: Test auto-lister with first product**
```bash
python3 AUTOMATIONS/auto_list_products.py --platform gumroad --dry-run
```

**Step 3: Fix selector issues, then list all 13**
```bash
python3 AUTOMATIONS/auto_list_products.py --platform gumroad --start
```

### Expected output
13 digital products live on Gumroad. Each with title, description, pricing, PDF attachment.

### Revenue/impact estimate
13 products at $5-$19 each. Digital products = 95%+ margin. Cross-promoted in 1,278 posts.

### Build time estimate
2-3 hours (after account creation)

### Priority tier
**P2** -- Needs Gumroad account.

---

## Playbook 14: Unified Posting Automation

### What it does
Posts approved content to all platforms via Buffer API or direct platform APIs.

### Alpha source
- Gap Analysis 2.3: 15,352 Lines of Content, 0 Published
- Gap Analysis 2.16: 1,278 Posts in Buffer CSVs

### Prerequisites
- 13 content packages in `CONTENT/social/` (confirmed)
- 11 Buffer CSVs (confirmed)
- **BLOCKER:** 0/49 social accounts created

### Implementation spec

**Step 1: Human creates minimum viable accounts** (X @PRINTMAXXER + 2 niche accounts + Buffer)

**Step 2: Upload Buffer CSVs** via Buffer dashboard import

**Step 3: Create `AUTOMATIONS/social_poster.py`** for non-Buffer platforms (direct API posting)

**Step 4: Schedule posting cadence**: X 3-4/day, TikTok 1-2/day, IG 1/day, LinkedIn 1/day

### Expected output
13 accounts posting 2-3x/day. 1,278 posts scheduled across 30+ days.

### Revenue/impact estimate
Content is top-of-funnel for every revenue stream. Even 100 followers per account = 1,300 total.

### Build time estimate
4-6 hours (after account creation)

### Priority tier
**P2** -- Needs social accounts.

---

## Playbook 12: Remotion Video Rendering Pipeline

### What it does
Creates a pipeline that renders videos from `.claude/remotion-skills/` specs, one per niche per day.

### Alpha source
- Gap Analysis 2.1: Remotion Video System ($0 cost, 0 videos produced, 2,474 lines of specs)

### Prerequisites
- `.claude/remotion-skills/rules/` (confirmed)
- `OPS/prompts/remotion/` (confirmed)
- **BLOCKER:** Remotion needs to be installed, social accounts needed to post

### Implementation spec

**Step 1: Set up Remotion project**
```bash
mkdir -p builds/remotion-videos && cd builds/remotion-videos
npx create-video@latest . --template blank
```

**Step 2: Create `AUTOMATIONS/render_videos.py`**
- Read niche-specific specs from `.claude/remotion-skills/rules/`
- Render via `npx remotion render` for each niche
- Output to `CONTENT/video/{niche}/`

**Step 3: Add to cron**
```
0 2 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && /usr/bin/python3 AUTOMATIONS/render_videos.py >> AUTOMATIONS/logs/video_render.log 2>&1
```

### Expected output
1-2 videos/day across 5 niches. Format: 1080x1920 vertical for TikTok/Reels/Shorts.

### Revenue/impact estimate
Video content has 3-5x engagement vs text. 150 videos/month across 5 niches.

### Build time estimate
6-8 hours

### Priority tier
**P2** -- Needs Remotion installation + social accounts.

---

## Playbook 16: Alpha-to-Product Pipeline

### What it does
Converts clusters of APPROVED alpha entries into $5-$19 Gumroad micro-products via a 5-prompt production sequence.

### Alpha source
- Gap Analysis 2.10: 5-Prompt Product Pipeline (never run)

### Prerequisites
- `LEDGER/ALPHA_STAGING.csv` with APPROVED entries (confirmed)
- `DIGITAL_PRODUCTS/MICRO_PRODUCT_SPECS.md` (confirmed)
- **BLOCKER:** Gumroad account needed to list output

### Implementation spec

**Step 1: Create `AUTOMATIONS/alpha_to_product.py`**
- Read APPROVED alpha, cluster by category (min 10 per cluster)
- Run 5-prompt sequence: ideation, outline, content, packaging, listing copy
- Output PDF + listing copy to `PRODUCTS/GUMROAD_INSTANT_UPLOAD/auto_generated/`
- Product pricing by cluster size: 10-15 entries=$5, 16-25=$9, 26+=$19

**Step 2: Test with one cluster**
```bash
python3 AUTOMATIONS/alpha_to_product.py --topic "cold email" --dry-run
```

### Expected output
Auto-generated micro-products from alpha data. Each has PDF + listing + cover spec.

### Revenue/impact estimate
Digital products at 95%+ margin. Each targets validated pain points.

### Build time estimate
6-8 hours

### Priority tier
**P2** -- Needs Gumroad account.

---

## Playbook 18: Revenue Attribution Tracker

### What it does
Maps revenue to the alpha findings that inspired each product/service. Identifies highest-ROI alpha sources.

### Alpha source
- Gap Analysis Section 4 #18

### Prerequisites
- `FINANCIALS/REVENUE_TRACKER.csv` (confirmed)
- `LEDGER/ALPHA_STAGING.csv` (confirmed)
- **BLOCKER:** No revenue yet to attribute

### Implementation spec

**Step 1: Create `AUTOMATIONS/revenue_attribution.py`**
- Read revenue entries, match to alpha sources by category/method
- Write `LEDGER/REVENUE_ATTRIBUTION.csv` with revenue-to-alpha mappings
- Generate top 10 revenue-producing alpha sources report
- Feed back into scraper prioritization

**Step 2: Add weekly cron**
```
0 20 * * 0 cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && /usr/bin/python3 AUTOMATIONS/revenue_attribution.py >> AUTOMATIONS/logs/attribution.log 2>&1
```

### Expected output
Revenue entries linked to alpha sources. Top performers identified for doubling down.

### Revenue/impact estimate
Attribution intelligence drives resource allocation to highest-ROI activities.

### Build time estimate
3-4 hours

### Priority tier
**P2** -- Needs revenue flowing first.

---

# Execution Order Summary

## Immediate (Today, P0)

| Order | Playbook | Time | Cumulative |
|-------|----------|------|------------|
| 1 | #6 Ralph Loop Fixer | 0 min (done) | 0 min |
| 2 | #15 MCP Tool Installer | 1 hr | 1 hr |
| 3 | #5 Hashtag-to-Post Merger | 1 hr | 2 hr |
| 4 | #3 Niche Meta Detector Live Data | 1-2 hr | 4 hr |
| 5 | #2 Alpha Review Automation | 3-4 hr | 8 hr |

## This Week (Remaining P0)

| Order | Playbook | Time | Cumulative |
|-------|----------|------|------------|
| 6 | #19 Content QA Gate | 2-3 hr | 11 hr |
| 7 | #8 Cold Email Template Expander | 2 hr | 13 hr |
| 8 | #13 Competitor Alert System | 3-4 hr | 17 hr |
| 9 | #20 Freshness Auditor | 2-3 hr | 20 hr |
| 10 | #17 Cross-Pollination Automator | 4-5 hr | 25 hr |

## When Human Available (P1)

| Order | Playbook | Time | Blocker |
|-------|----------|------|---------|
| 11 | #9 Legal Page Deployer | 1-2 hr | Compile legal content |
| 12 | #11 Vercel Migration | 3-4 hr | `vercel login` (30 sec) |
| 13 | #4 Email Follow-up | 2-3 hr | Email infra ($46/mo) |

## After Account Creation (P2)

| Order | Playbook | Time | Blocker |
|-------|----------|------|---------|
| 14 | #1 Account Creation | 2-3 hr + human time | Human at keyboard |
| 15 | #10 Gumroad Auto-Lister | 2-3 hr | Gumroad account |
| 16 | #14 Unified Posting | 4-6 hr | Social accounts |
| 17 | #7 Affiliate Inserter | 3-4 hr | Affiliate approvals |
| 18 | #16 Alpha-to-Product | 6-8 hr | Gumroad account |
| 19 | #12 Remotion Video | 6-8 hr | Remotion + accounts |
| 20 | #18 Revenue Attribution | 3-4 hr | Revenue flowing |

## Totals

| Tier | Playbooks | Build Hours | What It Unlocks |
|------|-----------|-------------|-----------------|
| P0 | 10 | ~22-30 hr | Internal optimization, 867 alpha cleared, live meta detection |
| P1 | 3 | ~7-10 hr | 601 SEO pages indexed, 3 revenue streams, email follow-ups |
| P2 | 7 | ~25-38 hr | All external revenue: products, posting, affiliates, video |
| **Total** | **20** | **~54-78 hr** | **Full system operational** |

## Dependencies Graph

```
Playbook 1 (Accounts) ──┬── #10 (Gumroad)
                         ├── #14 (Auto Poster)
                         ├── #7 (Affiliates)
                         ├── #12 (Video)
                         └── #16 (Alpha-to-Product)

Playbook 2 (Alpha Review) ──┬── #16 (Alpha-to-Product)
                             └── #17 (Cross-Pollination)

Playbook 19 (Content QA) ──── #14 (Auto Poster)

Playbook 4 (Follow-ups) ──── needs email infra ($46/mo)

All P0 playbooks: INDEPENDENT -- can be built in parallel.
```

---

*Generated from AUDIT/ALPHA_INTEGRATION_GAP_ANALYSIS.md. Each playbook is designed to be picked up and executed in a single focused session by either a human or Claude agent.*
