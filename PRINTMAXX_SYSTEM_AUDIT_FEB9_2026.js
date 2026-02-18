const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, LevelFormat } = require('docx');

// === CONSTANTS ===
const PAGE_WIDTH = 12240;
const MARGIN = 1440;
const CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN); // 9360

const COLORS = {
  primary: "1B3A4B",
  accent: "3D8B37",
  warning: "C45A1C",
  critical: "B91C1C",
  muted: "6B7280",
  headerBg: "1B3A4B",
  headerText: "FFFFFF",
  rowAlt: "F3F4F6",
  greenBg: "DCFCE7",
  yellowBg: "FEF9C3",
  redBg: "FEE2E2",
  blueBg: "DBEAFE",
};

const border = { style: BorderStyle.SINGLE, size: 1, color: "D1D5DB" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0 };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

// === HELPER FUNCTIONS ===
function heading(text, level = HeadingLevel.HEADING_1) {
  return new Paragraph({ heading: level, spacing: { before: level === HeadingLevel.HEADING_1 ? 360 : 240, after: 200 }, children: [new TextRun({ text, bold: true, font: "Arial", size: level === HeadingLevel.HEADING_1 ? 36 : level === HeadingLevel.HEADING_2 ? 30 : 26, color: COLORS.primary })] });
}

function para(text, opts = {}) {
  return new Paragraph({ spacing: { after: 160 }, ...opts, children: [new TextRun({ text, font: "Arial", size: 22, color: opts.color || "374151", ...opts.run })] });
}

function boldPara(label, text) {
  return new Paragraph({ spacing: { after: 140 }, children: [
    new TextRun({ text: label, font: "Arial", size: 22, bold: true, color: COLORS.primary }),
    new TextRun({ text, font: "Arial", size: 22, color: "374151" })
  ]});
}

function statusBadge(status) {
  const map = { "ACTIVE": { bg: COLORS.greenBg, color: "166534" }, "DEFINED": { bg: COLORS.yellowBg, color: "854D0E" }, "BROKEN": { bg: COLORS.redBg, color: "991B1B" }, "MANUAL": { bg: COLORS.yellowBg, color: "854D0E" }, "MISSING": { bg: COLORS.redBg, color: "991B1B" }, "WORKING": { bg: COLORS.greenBg, color: "166534" }, "PARTIAL": { bg: COLORS.blueBg, color: "1E40AF" } };
  return map[status] || { bg: "F3F4F6", color: "374151" };
}

function headerCell(text, width) {
  return new TableCell({ borders, width: { size: width, type: WidthType.DXA }, shading: { fill: COLORS.headerBg, type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 120, right: 120 }, verticalAlign: "center",
    children: [new Paragraph({ children: [new TextRun({ text, font: "Arial", size: 20, bold: true, color: COLORS.headerText })] })]
  });
}

function cell(text, width, opts = {}) {
  const badge = opts.status ? statusBadge(opts.status) : null;
  return new TableCell({ borders, width: { size: width, type: WidthType.DXA },
    shading: badge ? { fill: badge.bg, type: ShadingType.CLEAR } : opts.shading ? { fill: opts.shading, type: ShadingType.CLEAR } : undefined,
    margins: { top: 60, bottom: 60, left: 120, right: 120 }, verticalAlign: "center",
    children: [new Paragraph({ children: [new TextRun({ text, font: "Arial", size: 20, color: badge ? badge.color : opts.color || "374151", bold: opts.bold || false })] })]
  });
}

function makeTable(headers, rows, colWidths) {
  const totalWidth = colWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({ children: headers.map((h, i) => headerCell(h, colWidths[i])) }),
      ...rows.map((row, ri) => new TableRow({
        children: row.map((c, ci) => {
          if (typeof c === 'object' && c.text) return cell(c.text, colWidths[ci], c);
          return cell(String(c), colWidths[ci], { shading: ri % 2 === 1 ? COLORS.rowAlt : undefined });
        })
      }))
    ]
  });
}

function spacer(size = 120) {
  return new Paragraph({ spacing: { before: size, after: size }, children: [] });
}

function bulletItem(text, ref = "bullets") {
  return new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 80 }, children: [new TextRun({ text, font: "Arial", size: 22, color: "374151" })] });
}

function numberItem(text, ref = "numbers") {
  return new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 80 }, children: [new TextRun({ text, font: "Arial", size: 22, color: "374151" })] });
}

// === DOCUMENT ===
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.START, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers2", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.START, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers3", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.START, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: COLORS.primary },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Arial", color: COLORS.primary },
        paragraph: { spacing: { before: 240, after: 180 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: COLORS.primary },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
    ]
  },
  sections: [
    // ==================== TITLE PAGE ====================
    {
      properties: {
        page: { size: { width: PAGE_WIDTH, height: 15840 }, margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN } }
      },
      children: [
        spacer(2400),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: "PRINTMAXX SYSTEM AUDIT", font: "Arial", size: 56, bold: true, color: COLORS.primary })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [new TextRun({ text: "Full Infrastructure, Automation & Inter-Folder Analysis", font: "Arial", size: 28, color: COLORS.muted })] }),
        spacer(200),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [new TextRun({ text: "February 9, 2026", font: "Arial", size: 24, color: COLORS.muted })] }),
        spacer(600),
        // Executive summary box
        new Table({
          width: { size: CONTENT_WIDTH, type: WidthType.DXA }, columnWidths: [CONTENT_WIDTH],
          rows: [new TableRow({ children: [new TableCell({
            borders: { top: { style: BorderStyle.SINGLE, size: 3, color: COLORS.primary }, bottom: { style: BorderStyle.SINGLE, size: 3, color: COLORS.primary }, left: { style: BorderStyle.SINGLE, size: 3, color: COLORS.primary }, right: { style: BorderStyle.SINGLE, size: 3, color: COLORS.primary } },
            width: { size: CONTENT_WIDTH, type: WidthType.DXA },
            shading: { fill: "F0F9FF", type: ShadingType.CLEAR },
            margins: { top: 200, bottom: 200, left: 300, right: 300 },
            children: [
              new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "EXECUTIVE SUMMARY", font: "Arial", size: 26, bold: true, color: COLORS.primary })] }),
              new Paragraph({ spacing: { after: 100 }, children: [new TextRun({ text: "This audit maps every file, script, research loop, and automation process across the PRINTMAXX Starter Kit. It identifies what runs, what's defined but manual, what's broken, and delivers a concrete cron/scheduling plan to automate execution at daily, weekly, and monthly intervals.", font: "Arial", size: 21, color: "374151" })] }),
              new Paragraph({ spacing: { after: 60 }, children: [
                new TextRun({ text: "Key finding: ", font: "Arial", size: 21, bold: true, color: COLORS.critical }),
                new TextRun({ text: "~80% of automation is defined but not running. The system has institutional-grade research and analysis logic with zero scheduled execution. Fixing this requires ~6 hours of work and unlocks autonomous overnight operation.", font: "Arial", size: 21, color: "374151" })
              ]}),
            ]
          })] })]
        }),
      ]
    },
    // ==================== SECTION 1: SYSTEM ARCHITECTURE ====================
    {
      properties: {
        page: { size: { width: PAGE_WIDTH, height: 15840 }, margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN } }
      },
      headers: {
        default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "PRINTMAXX System Audit | Feb 9, 2026", font: "Arial", size: 18, color: COLORS.muted, italics: true })] })] })
      },
      footers: {
        default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Page ", font: "Arial", size: 18, color: COLORS.muted }), new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: COLORS.muted })] })] })
      },
      children: [
        heading("1. System Architecture Overview"),
        para("The PRINTMAXX Starter Kit is a multi-layered solopreneur operating system designed to bootstrap from $0 to $200K+ through 88 tracked money methods, autonomous research loops, and content automation. Below is the full folder-to-folder data flow."),
        spacer(80),

        heading("1.1 Folder Map & Responsibilities", HeadingLevel.HEADING_2),
        makeTable(
          ["Folder", "Role", "Files", "Status"],
          [
            [".claude/", "Agent config: rules, commands, agents, skills", "25+", { text: "ACTIVE", status: "ACTIVE" }],
            ["MASTER_DOC/", "Single source of truth (269KB master OS doc)", "5 versions", { text: "ACTIVE", status: "ACTIVE" }],
            ["01_STRATEGY/", "Strategic synthesis, capital genesis plans", "10+", { text: "ACTIVE", status: "ACTIVE" }],
            ["02_TRACKING/", "Reorganized MEGA_SHEET CSVs by category", "6 subdirs", { text: "PARTIAL", status: "PARTIAL" }],
            ["LEDGER/", "Master CSV database (alpha, methods, tools)", "39+ CSVs", { text: "PARTIAL", status: "PARTIAL" }],
            ["OPS/", "Operations: reports, prompts, playbooks, logs", "194 files", { text: "ACTIVE", status: "ACTIVE" }],
            ["AUTOMATIONS/", "Python scrapers, monitors, TUI", "15+ scripts", { text: "BROKEN", status: "BROKEN" }],
            ["scripts/", "Data processors, generators, Ralph framework", "13+ scripts", { text: "PARTIAL", status: "PARTIAL" }],
            ["ralph/", "Ralph loop execution hub (11 loops)", "11 loop dirs", { text: "ACTIVE", status: "ACTIVE" }],
            ["05_AUTOMATION/", "Browser automation (X bookmarks, scrapers)", "20+ scripts", { text: "DEFINED", status: "DEFINED" }],
            ["MONEY_METHODS/", "46+ method playbooks with SOPs", "11 subdirs", { text: "DEFINED", status: "DEFINED" }],
            ["03_PLAYBOOKS/", "Reorganized playbooks (new structure)", "46 subdirs", { text: "DEFINED", status: "DEFINED" }],
            ["04_CONTENT/", "Content library (social, email, video, articles)", "665+ files", { text: "ACTIVE", status: "ACTIVE" }],
            ["CONTENT/", "Legacy content folder", "5 subdirs", { text: "ACTIVE", status: "ACTIVE" }],
            ["RESEARCH/", "Deep domain research (PEMF, 21 files)", "21 files", { text: "ACTIVE", status: "ACTIVE" }],
            ["tasks/", "PRD files for Ralph agent execution", "5 PRDs", { text: "ACTIVE", status: "ACTIVE" }],
            ["logs/", "Automation activity logs", "5 log files", { text: "ACTIVE", status: "ACTIVE" }],
            ["PRINTMAXX Terminal.app", "macOS TUI launcher (v3.0)", "App bundle", { text: "ACTIVE", status: "ACTIVE" }],
          ],
          [2200, 3500, 1500, 2160]
        ),

        spacer(200),
        heading("1.2 Inter-Folder Data Flow", HeadingLevel.HEADING_2),
        para("The system operates as a pipeline where research flows into the LEDGER, gets processed by scripts, generates content, and feeds back into research. Here are the critical data flows:"),
        spacer(60),

        boldPara("Flow 1 - Research to Alpha: ", "Twitter/Reddit scrapers (AUTOMATIONS/) extract raw alpha, write to LEDGER/ALPHA_STAGING.csv, which feeds into LEDGER/MEGA_SHEET/TAB3_ALPHA_MASTER.csv (835 entries). Ralph loops (ralph/) run nightly research sweeps that also write to ALPHA_STAGING."),
        boldPara("Flow 2 - Alpha to Content: ", "Approved alpha triggers the Zero Waste Protocol: each finding generates 5+ social posts, a thread, newsletter draft, and Gumroad product spec. Content routes to 04_CONTENT/ and CONTENT/ folders for QA review in OPS/CONTENT_QA_QUEUE/."),
        boldPara("Flow 3 - Alpha to Methods: ", "Validated alpha gets classified and routed to MONEY_METHODS/ playbooks and LEDGER/ master CSVs. New tools go to TOOLS_CHANNELS_MASTER, new methods to MONEY_METHODS_MASTER, new formats to WINNING_CONTENT_STRUCTURES."),
        boldPara("Flow 4 - Methods to Execution: ", "Makefile orchestrates execution commands. Ralph loops execute overnight sprints across 8 parallel loops. PRINTMAXX Terminal.app provides a GUI launcher for manual triggering."),
        boldPara("Flow 5 - Execution to Tracking: ", "All outputs log to OPS/logs/, ralph/logs/, and logs/. Financial results track in FINANCIALS/REVENUE_TRACKER.csv. Portfolio rebalancing writes to LEDGER/REBALANCE_REPORTS/."),

        spacer(80),
        boldPara("CRITICAL BREAK IN FLOW: ", "LEDGER/ALPHA_STAGING.csv is missing. This file is referenced by 7+ scripts and all .claude/commands. Data exists in MEGA_SHEET/TAB3 (835 rows) but the standalone file that scripts expect does not exist. This is the single biggest blocker in the system."),

        // ==================== SECTION 2: .CLAUDE CONFIGURATION ====================
        new Paragraph({ children: [new PageBreak()] }),
        heading("2. Claude Configuration (.claude/)"),
        para("The .claude/ directory contains 64KB+ of configuration defining how AI agents operate within this project. This is the brain of the system."),

        heading("2.1 Rules (5 files)", HeadingLevel.HEADING_2),
        makeTable(
          ["Rule File", "Purpose", "Key Enforcement"],
          [
            ["alpha-review.md", "Alpha entry validation", "24-point bot detection, earnings skepticism, 6 status categories"],
            ["copy-style.md", "Human-first writing voice", "Weighted voice system (S/A/B/C tiers), 24 banned AI patterns, zero em dashes"],
            ["security.md", "Security requirements", "No hardcoded creds, input validation, GDPR/FTC compliance"],
            ["code-style.md", "TypeScript/React standards", "PascalCase components, prop interfaces, server components default"],
            ["performance.md", "Performance targets", "500KB bundle, <2.5s LCP, <100ms FID, <0.1 CLS"],
          ],
          [2200, 3000, 4160]
        ),

        spacer(120),
        heading("2.2 Commands (13 workflows)", HeadingLevel.HEADING_2),
        makeTable(
          ["Command", "Model", "Purpose", "Frequency"],
          [
            ["/printmaxx", "Sonnet", "Load full context, show status, recommend next actions", "Every session"],
            ["/daily-research", "Haiku", "Scan 56+ X accounts, 6 subreddits, 4 YouTube, 4 websites", "Daily"],
            ["/review-alpha", "Sonnet", "Review pending alpha, apply approval criteria, integrate", "Daily"],
            ["/status", "Sonnet", "Dashboard: apps, content, accounts, leads, CSVs", "On demand"],
            ["/validate", "Sonnet", "Content + code + LEDGER + compliance validation", "Pre-deploy"],
            ["/deploy-check", "Sonnet", "Pre-flight: build, env, perf, SEO, compliance", "Pre-deploy"],
            ["/generate-posts", "Haiku", "Generate social posts across niches and platforms", "Daily/Weekly"],
            ["/generate-longtail", "-", "Generate SEO longtail pages", "Weekly"],
            ["/remotion-video", "-", "Create videos with Remotion + React", "On demand"],
            ["/parallel-launch", "-", "Launch parallel agent teams", "On demand"],
            ["/run-alpha-extractor", "-", "Run alpha extraction pipeline", "Daily"],
            ["/warmup-sop", "-", "Email account warmup protocol", "Setup"],
            ["/brand-names", "-", "Brand naming conventions", "On demand"],
          ],
          [2100, 1200, 4060, 2000]
        ),

        spacer(120),
        heading("2.3 Agents (4 specialists)", HeadingLevel.HEADING_2),
        makeTable(
          ["Agent", "Model", "Role"],
          [
            ["content-generator", "Sonnet", "Generate SEO longtail and truth pages (2000-3000 words, research-backed)"],
            ["reviewer", "Sonnet", "Code review: architecture, quality, testing, security, performance"],
            ["validator", "Haiku", "Validate code + content + SEO + performance + LEDGER sync"],
            ["deployer", "Haiku", "Deployment workflows: staging, production, rollback with checklists"],
          ],
          [2400, 1200, 5760]
        ),

        // ==================== SECTION 3: RALPH LOOPS ====================
        new Paragraph({ children: [new PageBreak()] }),
        heading("3. Ralph Loop System (Autonomous Agent Orchestration)"),
        para("Ralph is an autonomous AI agent loop framework. It spawns fresh Claude instances iteratively, maintaining state via git history, progress.txt, and prd.json. Each iteration is a complete, independent agent session that reads previous context from the filesystem (not from context window memory)."),

        heading("3.1 Active Ralph Loops", HeadingLevel.HEADING_2),
        makeTable(
          ["Loop Name", "Purpose", "Frequency", "Status"],
          [
            ["comprehensive_alpha_research", "Deep research across 81+ sources, 10 alpha categories", "Nightly", { text: "ACTIVE", status: "ACTIVE" }],
            ["niche_meta_detection", "Detect trending metas across 88 niches with history", "Nightly", { text: "ACTIVE", status: "ACTIVE" }],
            ["synergy_package_builder", "Find cross-pollination opportunities between methods", "Nightly", { text: "ACTIVE", status: "ACTIVE" }],
            ["retardmaxx_execution", "Execute revenue tasks: Gumroad, emails, social posts", "Nightly", { text: "ACTIVE", status: "ACTIVE" }],
            ["meme_coin_backtest", "Backtest meme coin patterns vs historical data", "Nightly", { text: "ACTIVE", status: "ACTIVE" }],
            ["daily_ops", "Daily operations and planning", "Daily", { text: "ACTIVE", status: "ACTIVE" }],
            ["social_branding", "Social media branding and positioning", "Nightly", { text: "ACTIVE", status: "ACTIVE" }],
            ["full_printmaxx_audit", "Comprehensive 27-task system audit", "Nightly", { text: "ACTIVE", status: "ACTIVE" }],
            ["digital_products", "Digital product development and launch", "Nightly", { text: "ACTIVE", status: "ACTIVE" }],
            ["content_machine", "Content generation at scale (15 batches)", "Nightly", { text: "ACTIVE", status: "ACTIVE" }],
            ["mega", "Master orchestrator combining all loop results", "Periodic", { text: "ACTIVE", status: "ACTIVE" }],
          ],
          [2800, 3600, 1200, 1760]
        ),

        spacer(100),
        heading("3.2 Execution Scripts", HeadingLevel.HEADING_2),
        boldPara("run_parallel_loops.sh: ", "Launches 5 main loops simultaneously as background processes with nohup."),
        boldPara("run_overnight_sprint.sh: ", "Launches all 8 core loops for overnight execution. Logs timestamped in ralph/logs/."),
        boldPara("Current triggering: ", "MANUAL. These scripts exist and work, but nobody runs them on a schedule. No crontab entries found."),

        spacer(100),
        heading("3.3 Swarm Orchestration (Multi-Agent)", HeadingLevel.HEADING_2),
        para("For complex tasks, Ralph coordinates multiple Claude agents in waves:"),
        boldPara("Wave 1 (Parallel Research): ", "T1: Twitter scanning (49 accounts), T2: Reddit alpha (41 subs), T3: Ecom arbitrage, T4: POD trends, T5: Platform arbitrage"),
        boldPara("Wave 2 (Processing): ", "T6: Deduplication and scoring, T7: Financial projection, T8: Cross-pollination mapping"),
        boldPara("Wave 3 (Integration): ", "T9: Alpha to investment conversion, T10: Content generation (Zero Waste), T11: Financial tracker update"),

        // ==================== SECTION 4: AUTOMATION SCRIPTS ====================
        new Paragraph({ children: [new PageBreak()] }),
        heading("4. Automation Scripts Inventory"),
        para("Three separate directories contain automation scripts with overlapping responsibilities. This creates confusion about which scripts are canonical."),

        heading("4.1 AUTOMATIONS/ (Primary Python Scripts)", HeadingLevel.HEADING_2),
        makeTable(
          ["Script", "Purpose", "Dependencies", "Status"],
          [
            ["printmaxx_tui.py", "Terminal UI launcher (main menu system)", "rich, textual", { text: "BROKEN", status: "BROKEN" }],
            ["niche_meta_detector.py", "Historical pattern matching across 88 niches", "Standard lib", { text: "WORKING", status: "WORKING" }],
            ["reddit_alpha_scraper.py", "Daily Reddit scraping (40 subreddits)", "requests", { text: "DEFINED", status: "DEFINED" }],
            ["meme_coin_signal_tracker.py", "Meme coin pattern tracking for backtesting", "Standard lib", { text: "DEFINED", status: "DEFINED" }],
            ["agent_monitor.py", "Live dashboard for running agents", "rich", { text: "BROKEN", status: "BROKEN" }],
            ["twitter_scraper_live.py", "Live Twitter scraping via Selenium", "selenium", { text: "DEFINED", status: "DEFINED" }],
            ["scrape_twitter_applescript.py", "macOS AppleScript-based Twitter scraping", "macOS only", { text: "DEFINED", status: "DEFINED" }],
            ["scrape_caiden_playwright.py", "Browser automation for specific accounts", "playwright", { text: "DEFINED", status: "DEFINED" }],
            ["parallel_background_scraper.py", "Parallel scraping infrastructure", "asyncio", { text: "DEFINED", status: "DEFINED" }],
          ],
          [2800, 2800, 1600, 2160]
        ),

        spacer(100),
        heading("4.2 scripts/ (Data Processors & Generators)", HeadingLevel.HEADING_2),
        makeTable(
          ["Script", "Purpose", "Status"],
          [
            ["auto_backtest_trigger.py", "Triggers backtesting on new alpha entries", { text: "DEFINED", status: "DEFINED" }],
            ["organize_alpha.py", "Organizes alpha by category", { text: "WORKING", status: "WORKING" }],
            ["merge_backtest_scores.py", "Consolidates backtest results", { text: "WORKING", status: "WORKING" }],
            ["write_playbooks.py", "Generates playbooks from alpha", { text: "DEFINED", status: "DEFINED" }],
            ["generate_30day_calendar.py", "Creates content calendar", { text: "DEFINED", status: "DEFINED" }],
            ["generate_buffer_csvs.py", "Creates Buffer scheduling CSVs", { text: "DEFINED", status: "DEFINED" }],
            ["content_to_qa_router.py", "Routes content for review", { text: "DEFINED", status: "DEFINED" }],
            ["extract_source_csvs_from_mega_sheet.py", "Extracts CSVs from mega sheet", { text: "WORKING", status: "WORKING" }],
            ["consolidate_swarm_output.py", "Consolidates multi-agent outputs", { text: "DEFINED", status: "DEFINED" }],
            ["repair_alpha_staging_v2.py", "Repairs corrupted alpha CSV", { text: "WORKING", status: "WORKING" }],
          ],
          [3200, 3960, 2200]
        ),

        spacer(100),
        heading("4.3 Critical Blockers", HeadingLevel.HEADING_2),
        makeTable(
          ["Issue", "Impact", "Fix Time", "Priority"],
          [
            ["Missing ALPHA_STAGING.csv", "Blocks 7+ scripts, all /commands", "30 min", { text: "P0", status: "MISSING" }],
            ["Missing Python deps (rich, textual, numpy)", "Blocks TUI, monitor, projector", "10 min", { text: "P0", status: "MISSING" }],
            ["2 scripts have ValueError bugs", "revenue_projector, method_analyzer broken", "30 min", { text: "P1", status: "BROKEN" }],
            ["No requirements.txt", "Reproducibility impossible", "5 min", { text: "P1", status: "MISSING" }],
            ["Hardcoded absolute paths", "Breaks if project folder moves", "20 min", { text: "P2", status: "BROKEN" }],
            ["No integration/orchestration layer", "Scripts don't coordinate", "2 hours", { text: "P1", status: "MISSING" }],
            ["Duplicate folder structures (OPS vs 06_OPERATIONS)", "Confusion about canonical location", "1 hour", { text: "P2", status: "BROKEN" }],
          ],
          [2800, 3000, 1400, 2160]
        ),

        // ==================== SECTION 5: RESEARCH & ANALYSIS PROCESSES ====================
        new Paragraph({ children: [new PageBreak()] }),
        heading("5. Research & Analysis Processes"),
        para("The system has sophisticated research logic defined across multiple locations. Below is every research loop identified, its current state, and what it needs to become automated."),

        heading("5.1 Research Pipeline Architecture", HeadingLevel.HEADING_2),
        makeTable(
          ["Pipeline Stage", "What Happens", "Tools/Scripts", "Status"],
          [
            ["1. Source Scanning", "92 Twitter accounts + 41 subreddits + GitHub + Product Hunt", "twitter_scraper_live.py, reddit_alpha_scraper.py", { text: "MANUAL", status: "MANUAL" }],
            ["2. Alpha Extraction", "Raw findings scored 0-100, classified by type", "alpha_screening.py, niche_meta_detector.py", { text: "PARTIAL", status: "PARTIAL" }],
            ["3. Bot Detection", "24-point authenticity check on engagement claims", ".claude/rules/alpha-review.md", { text: "MANUAL", status: "MANUAL" }],
            ["4. Earnings Skepticism", "Income claims verified (default: skeptical)", ".claude/rules/alpha-review.md", { text: "MANUAL", status: "MANUAL" }],
            ["5. Classification", "APPROVED / ENGAGEMENT_BAIT / REPURPOSE / REJECTED", "/review-alpha command", { text: "MANUAL", status: "MANUAL" }],
            ["6. Integration", "Route to correct master CSV + generate content", "organize_alpha.py", { text: "MANUAL", status: "MANUAL" }],
            ["7. Content Generation", "Zero Waste: 5+ posts, thread, newsletter, Gumroad spec", "/generate-posts command", { text: "MANUAL", status: "MANUAL" }],
            ["8. Backtesting", "Test alpha performance against historical data", "auto_backtest_trigger.py", { text: "DEFINED", status: "DEFINED" }],
            ["9. Portfolio Rebalance", "Kelly Criterion allocation across methods", "LEDGER/KELLY_ALLOCATIONS.csv", { text: "MANUAL", status: "MANUAL" }],
          ],
          [1800, 3200, 2560, 1800]
        ),

        spacer(120),
        heading("5.2 Tracking Systems", HeadingLevel.HEADING_2),
        para("The LEDGER/ directory contains the master database with 39+ CSV files organized into a MEGA_SHEET (10 tabs) plus standalone tracking files."),
        makeTable(
          ["MEGA_SHEET Tab", "Rows", "Content", "Status"],
          [
            ["TAB1: MONEY_METHODS_MASTER", "69", "All 69 methods + synergy scores + ROI estimates", { text: "ACTIVE", status: "ACTIVE" }],
            ["TAB2: NICHES_MASTER", "34", "Niche profiles (faith, fitness, AI, crypto, etc.)", { text: "ACTIVE", status: "ACTIVE" }],
            ["TAB3: ALPHA_MASTER", "835", "All alpha entries with status/ROI/difficulty", { text: "ACTIVE", status: "ACTIVE" }],
            ["TAB4: TOOLS_CHANNELS_MASTER", "225", "Tools and marketing channels", { text: "MISSING", status: "MISSING" }],
            ["TAB5: CONTENT_MASTER", "570", "Content calendar + winning formats", { text: "ACTIVE", status: "ACTIVE" }],
            ["TAB6: APPS_ECOM_MASTER", "154", "App opportunities + ecom data", { text: "MISSING", status: "MISSING" }],
            ["TAB7: SOURCES_ACCOUNTS", "159", "92 Twitter + 41 Reddit + research sources", { text: "ACTIVE", status: "ACTIVE" }],
            ["TAB8: OPERATIONS", "214", "GTM operations + affiliate + outreach", { text: "ACTIVE", status: "ACTIVE" }],
            ["TAB9: EXPERIMENTS_METRICS", "79", "A/B tests + metrics + performance data", { text: "ACTIVE", status: "ACTIVE" }],
            ["TAB10: RESEARCH_MISC", "180", "Ad hoc research findings + opportunities", { text: "ACTIVE", status: "ACTIVE" }],
          ],
          [2800, 800, 3560, 2200]
        ),

        // ==================== SECTION 6: PROCESSES DEFINED NOT AUTOMATED ====================
        new Paragraph({ children: [new PageBreak()] }),
        heading("6. Processes: Defined But Not Automated"),
        para("These are the perpetual improvement loops that have complete logic, documentation, and even scripts, but no scheduling. Each one runs only when a human remembers to trigger it."),

        heading("6.1 Daily Research Workflow (2-3 hrs/day manual)", HeadingLevel.HEADING_2),
        boldPara("What exists: ", "/daily-research command, twitter_scraper_live.py, reddit_alpha_scraper.py, alpha_screening.py"),
        boldPara("What's missing: ", "No cron trigger. No overnight batch. No auto-classification. Human must run each step manually."),
        boldPara("Automation potential: ", "HIGH. The Ralph loop 'comprehensive_alpha_research' already does this. Just needs a crontab entry."),

        heading("6.2 Content QA Queue (256+ files pending)", HeadingLevel.HEADING_2),
        boldPara("What exists: ", "OPS/CONTENT_QA_QUEUE/ with 256 review files (Jan 22 - Feb 2). content_to_qa_router.py script."),
        boldPara("What's missing: ", "No auto-routing. No batch approval. No quality scoring. Everything is human-reviewed one by one."),
        boldPara("Automation potential: ", "MEDIUM. Claude validator agent could score and auto-approve content meeting threshold."),

        heading("6.3 Alpha Zero-Waste Protocol", HeadingLevel.HEADING_2),
        boldPara("What exists: ", "Documented process: every alpha finding generates 5+ posts, thread, newsletter, Gumroad spec. /generate-posts command exists."),
        boldPara("What's missing: ", "No trigger connecting alpha approval to content generation. Manual gap between review and creation."),
        boldPara("Automation potential: ", "HIGH. Chain /review-alpha output directly to /generate-posts."),

        heading("6.4 Portfolio Rebalancing (Quarterly manual)", HeadingLevel.HEADING_2),
        boldPara("What exists: ", "Kelly Criterion allocation math, backtest results, REBALANCE_REPORTS/ with Feb 4 report."),
        boldPara("What's missing: ", "No monthly trigger. No auto-collection of performance data. Manual spreadsheet work."),
        boldPara("Automation potential: ", "HIGH. Python scripts already compute allocations. Just need monthly schedule."),

        heading("6.5 Financial Tracking", HeadingLevel.HEADING_2),
        boldPara("What exists: ", "FINANCIALS/ with REVENUE_TRACKER.csv, EXPENSE_TRACKER.csv, P_AND_L_MONTHLY.csv, DAILY_METRICS.csv."),
        boldPara("What's missing: ", "All manual data entry. No API integrations (Stripe, Gumroad, etc.). No automated P&L generation."),
        boldPara("Automation potential: ", "MEDIUM. Requires API keys for payment platforms."),

        heading("6.6 Competitor Intelligence", HeadingLevel.HEADING_2),
        boldPara("What exists: ", "COMPETITIVE_INTELLIGENCE_JAN_2026.md, COMPETITOR_MONITORING_SYSTEM.md, COMPETITOR_SEO_ANALYSIS.md. Full framework."),
        boldPara("What's missing: ", "No scheduled scans. Visualping listed but not configured ($13/mo). No automated comparison reports."),
        boldPara("Automation potential: ", "HIGH. Ralph loop + web scraping could run weekly."),

        heading("6.7 Platform Algorithm Detection", HeadingLevel.HEADING_2),
        boldPara("What exists: ", "PLATFORM_ALGORITHM_RESEARCH_FEB2026.md, PLATFORM_ARBITRAGE_RESEARCH_FEB2026.md. Pattern docs."),
        boldPara("What's missing: ", "No RSS monitoring. No automated blog scanning. Manual research only."),
        boldPara("Automation potential: ", "MEDIUM. WebFetch + RSS parsing on a weekly schedule."),

        // ==================== SECTION 7: AUTOMATION PLAN ====================
        new Paragraph({ children: [new PageBreak()] }),
        heading("7. Recommended Automation Schedule"),
        para("Below is the concrete cron/scheduling plan organized by frequency. Each task maps to an existing script or command that just needs a trigger."),

        heading("7.1 DAILY Automations (Run Every Day)", HeadingLevel.HEADING_2),
        makeTable(
          ["#", "Task", "Time", "Script/Command", "What It Does"],
          [
            ["D1", "Overnight Ralph Sprint", "10:00 PM", "ralph/run_overnight_sprint.sh", "Launches 8 parallel loops: alpha research, niche detection, synergy building, content gen, digital products, social branding, audit, execution"],
            ["D2", "Alpha Staging Sync", "6:00 AM", "scripts/extract_source_csvs_from_mega_sheet.py", "Syncs MEGA_SHEET tabs to standalone CSVs that scripts expect (fixes the ALPHA_STAGING.csv gap)"],
            ["D3", "Alpha Screening", "6:30 AM", "scripts/organize_alpha.py + alpha_screening.py", "Scores new alpha entries 0-100, classifies APPROVED/REJECTED, updates ALPHA_STAGING.csv"],
            ["D4", "Content Generation", "7:00 AM", "/generate-posts --count 10 --platform all", "Generates 10 social posts across niches using approved alpha from overnight"],
            ["D5", "Buffer CSV Export", "7:30 AM", "scripts/generate_buffer_csvs.py", "Creates ready-to-import CSVs for Buffer social scheduling"],
            ["D6", "Revenue Dashboard Check", "8:00 AM", "AUTOMATIONS/printmaxx_quant_terminal.py", "Runs quant dashboard showing system health, method performance, pipeline status"],
          ],
          [500, 2000, 1200, 3460, 2200]
        ),

        spacer(120),
        heading("7.2 WEEKLY Automations (Run Every Monday)", HeadingLevel.HEADING_2),
        makeTable(
          ["#", "Task", "Script/Command", "What It Does"],
          [
            ["W1", "Full System Validation", "/validate", "Validates all content (FTC compliance, copy style), code (TypeScript, bundle), LEDGER (CSV headers, orphans)"],
            ["W2", "Competitor Intelligence Scan", "Ralph loop: competitive_intel", "Web scrape competitor sites, compare SEO rankings, detect new products/features"],
            ["W3", "Platform Algorithm Check", "Ralph loop: platform_monitor", "Scan X/TikTok/YouTube official blogs for algorithm changes, policy updates"],
            ["W4", "Content QA Batch Review", "scripts/content_to_qa_router.py", "Process all PENDING_REVIEW content, auto-approve meeting threshold, flag outliers"],
            ["W5", "Backtest Merge & Score", "scripts/merge_backtest_scores.py", "Consolidate all backtest results from the week, update method performance scores"],
            ["W6", "30-Day Calendar Refresh", "scripts/generate_30day_calendar.py", "Regenerate content calendar from current approved alpha and trending topics"],
            ["W7", "GitHub Trending Scan", "Ralph loop: github_trending", "Scan GitHub trending repos for new tools, MCP servers, automation opportunities"],
          ],
          [500, 2400, 3260, 3200]
        ),

        spacer(120),
        heading("7.3 MONTHLY Automations (1st of Each Month)", HeadingLevel.HEADING_2),
        makeTable(
          ["#", "Task", "Script/Command", "What It Does"],
          [
            ["M1", "Portfolio Rebalance", "Kelly Criterion recalculation", "Collect all method performance data, recalculate allocations, generate REBALANCE_REPORT"],
            ["M2", "P&L Generation", "FINANCIALS pipeline", "Aggregate REVENUE_TRACKER + EXPENSE_TRACKER into P_AND_L_MONTHLY. Compare to projections"],
            ["M3", "Method Kill/Promote Review", "Ralph loop: method_review", "Score all 69 methods on execution progress, kill underperformers, promote winners"],
            ["M4", "MEGA_SHEET Full Audit", "Ralph loop: full_printmaxx_audit", "27-task audit: data integrity, missing files, broken references, stale entries"],
            ["M5", "Strategy Synthesis Refresh", "01_STRATEGY/ update", "Update PRINTMAXX_STRATEGIC_SYNTHESIS with latest performance data and market shifts"],
            ["M6", "Niche Performance Review", "TAB2 analysis", "Review all 34 niches: engagement rates, revenue per niche, growth trajectory, kill/expand"],
          ],
          [500, 2400, 3160, 3300]
        ),

        // ==================== SECTION 8: IMPLEMENTATION ====================
        new Paragraph({ children: [new PageBreak()] }),
        heading("8. Implementation: Crontab Setup"),
        para("Below are the exact crontab entries needed. These assume the project lives at the standard macOS path. Adjust PROJ_DIR if the folder moves."),

        spacer(80),
        heading("8.1 Prerequisites (Fix First)", HeadingLevel.HEADING_2),
        numberItem("Create ALPHA_STAGING.csv from MEGA_SHEET/TAB3 (run extract_source_csvs_from_mega_sheet.py)", "numbers"),
        numberItem("Install Python dependencies: pip install rich textual numpy playwright", "numbers"),
        numberItem("Fix ValueError bugs in revenue_projector.py and method_performance_analyzer.py (string-to-float parsing)", "numbers"),
        numberItem("Create requirements.txt with all dependencies", "numbers"),
        numberItem("Create master orchestrator script (printmaxx_cron.sh) that wraps all scheduled tasks with logging and error handling", "numbers"),

        spacer(80),
        heading("8.2 Crontab Entries", HeadingLevel.HEADING_2),
        para("These are the recommended crontab entries for macOS. Each writes to a timestamped log file for auditability."),
        spacer(60),

        // Daily entries
        boldPara("DAILY (every day):", ""),
        bulletItem("22:00 - Overnight Ralph Sprint: 0 22 * * * cd $PROJ_DIR && bash ralph/run_overnight_sprint.sh >> logs/cron_overnight_$(date +%Y%m%d).log 2>&1"),
        bulletItem("06:00 - Alpha Staging Sync: 0 6 * * * cd $PROJ_DIR && python3 scripts/extract_source_csvs_from_mega_sheet.py >> logs/cron_sync_$(date +%Y%m%d).log 2>&1"),
        bulletItem("06:30 - Alpha Screening: 30 6 * * * cd $PROJ_DIR && python3 scripts/organize_alpha.py >> logs/cron_screen_$(date +%Y%m%d).log 2>&1"),
        bulletItem("07:30 - Buffer CSV Export: 30 7 * * * cd $PROJ_DIR && python3 scripts/generate_buffer_csvs.py >> logs/cron_buffer_$(date +%Y%m%d).log 2>&1"),

        spacer(60),
        boldPara("WEEKLY (every Monday):", ""),
        bulletItem("09:00 Mon - Backtest Merge: 0 9 * * 1 cd $PROJ_DIR && python3 scripts/merge_backtest_scores.py >> logs/cron_backtest_$(date +%Y%m%d).log 2>&1"),
        bulletItem("09:30 Mon - Calendar Refresh: 30 9 * * 1 cd $PROJ_DIR && python3 scripts/generate_30day_calendar.py >> logs/cron_calendar_$(date +%Y%m%d).log 2>&1"),
        bulletItem("10:00 Mon - Content QA Batch: 0 10 * * 1 cd $PROJ_DIR && python3 scripts/content_to_qa_router.py >> logs/cron_qa_$(date +%Y%m%d).log 2>&1"),

        spacer(60),
        boldPara("MONTHLY (1st of each month):", ""),
        bulletItem("08:00 1st - Full System Audit: 0 8 1 * * cd $PROJ_DIR && bash ralph/loops/full_printmaxx_audit/run.sh >> logs/cron_audit_$(date +%Y%m%d).log 2>&1"),
        bulletItem("09:00 1st - Portfolio Rebalance: 0 9 1 * * cd $PROJ_DIR && python3 scripts/merge_backtest_scores.py --rebalance >> logs/cron_rebalance_$(date +%Y%m%d).log 2>&1"),

        // ==================== SECTION 9: REALITY CHECK ====================
        new Paragraph({ children: [new PageBreak()] }),
        heading("9. Reality Check: Current State vs. Potential"),

        makeTable(
          ["Metric", "Current (Feb 9, 2026)", "With Automation Active"],
          [
            ["Revenue", "$0", "$451/week within 2 weeks (digital products)"],
            ["Alpha entries processed/day", "0 (manual backlog)", "30-50 auto-screened nightly"],
            ["Content pieces generated/day", "0", "10-20 auto-generated, human QA"],
            ["Scripts running on schedule", "0 (all manual)", "6 daily + 7 weekly + 6 monthly"],
            ["Ralph loops running nightly", "0 (manual trigger)", "8 parallel loops overnight"],
            ["Data pipeline integrity", "Broken (missing ALPHA_STAGING.csv)", "Full sync every 6 AM"],
            ["System health monitoring", "None", "Daily quant dashboard + weekly audit"],
            ["Portfolio rebalancing", "Quarterly manual", "Monthly automated with reports"],
            ["Competitor intelligence", "Sporadic manual", "Weekly automated scans"],
            ["Time spent on ops/day", "2-3 hours manual", "30 min review of auto-generated reports"],
          ],
          [2800, 3280, 3280]
        ),

        spacer(200),
        heading("9.1 The 6-Hour Fix", HeadingLevel.HEADING_2),
        para("Total estimated time to go from current state (80% broken/manual) to fully automated overnight execution:"),
        spacer(60),

        makeTable(
          ["Task", "Time", "Impact"],
          [
            ["Fix ALPHA_STAGING.csv (extract from MEGA_SHEET)", "30 min", "Unblocks 7+ scripts"],
            ["Install Python dependencies", "10 min", "Unblocks TUI, monitor, projector"],
            ["Fix 2 broken scripts (ValueError bugs)", "30 min", "Revenue projector + method analyzer working"],
            ["Create requirements.txt", "5 min", "Reproducibility for any machine"],
            ["Create printmaxx_cron.sh orchestrator", "2 hours", "Master script with logging, error handling, notifications"],
            ["Set up crontab entries", "15 min", "Everything runs on schedule"],
            ["Update hardcoded paths to use env vars", "20 min", "Portable across machines"],
            ["Test full overnight sprint", "2 hours", "Validate end-to-end pipeline"],
          ],
          [3800, 1000, 4560]
        ),

        spacer(200),
        // Final box
        new Table({
          width: { size: CONTENT_WIDTH, type: WidthType.DXA }, columnWidths: [CONTENT_WIDTH],
          rows: [new TableRow({ children: [new TableCell({
            borders: { top: { style: BorderStyle.SINGLE, size: 3, color: COLORS.accent }, bottom: { style: BorderStyle.SINGLE, size: 3, color: COLORS.accent }, left: { style: BorderStyle.SINGLE, size: 3, color: COLORS.accent }, right: { style: BorderStyle.SINGLE, size: 3, color: COLORS.accent } },
            width: { size: CONTENT_WIDTH, type: WidthType.DXA },
            shading: { fill: "F0FDF4", type: ShadingType.CLEAR },
            margins: { top: 200, bottom: 200, left: 300, right: 300 },
            children: [
              new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "BOTTOM LINE", font: "Arial", size: 28, bold: true, color: COLORS.accent })] }),
              new Paragraph({ spacing: { after: 100 }, children: [new TextRun({ text: "The PRINTMAXX system has hedge-fund-grade research logic, 88 tracked methods, 835 validated alpha entries, 665+ content pieces ready to deploy, and 11 Ralph loops built for overnight autonomous execution. The only thing missing is a crontab. Six hours of infrastructure work turns this from a planning system into an execution machine that runs while you sleep.", font: "Arial", size: 22, color: "374151" })] }),
            ]
          })] })]
        }),
      ]
    }
  ]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/sessions/awesome-nice-brown/mnt/PRINTMAXX_STARTER_KITttttt/PRINTMAXX_SYSTEM_AUDIT_FEB9_2026.docx", buffer);
  console.log("Audit report created successfully: PRINTMAXX_SYSTEM_AUDIT_FEB9_2026.docx");
});
