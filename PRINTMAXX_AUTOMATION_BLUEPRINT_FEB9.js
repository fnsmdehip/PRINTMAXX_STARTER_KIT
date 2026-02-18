const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, LevelFormat } = require('docx');

const PW = 12240, MG = 1440, CW = PW - 2*MG;
const C = { pri: "1B3A4B", acc: "3D8B37", warn: "C45A1C", crit: "B91C1C", mut: "6B7280", hBg: "1B3A4B", hTx: "FFFFFF", alt: "F3F4F6", grn: "DCFCE7", yel: "FEF9C3", red: "FEE2E2", blu: "DBEAFE", pur: "EDE9FE" };
const bd = { style: BorderStyle.SINGLE, size: 1, color: "D1D5DB" };
const bds = { top: bd, bottom: bd, left: bd, right: bd };

function hc(t, w) { return new TableCell({ borders: bds, width: { size: w, type: WidthType.DXA }, shading: { fill: C.hBg, type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 120, right: 120 }, children: [new Paragraph({ children: [new TextRun({ text: t, font: "Arial", size: 20, bold: true, color: C.hTx })] })] }); }
function tc(t, w, o={}) {
  const sm = { "ACTIVE": {bg:C.grn,c:"166534"}, "HIGH": {bg:C.grn,c:"166534"}, "HIGHEST": {bg:"BBF7D0",c:"14532D"}, "MEDIUM": {bg:C.yel,c:"854D0E"}, "LOW": {bg:C.blu,c:"1E40AF"}, "DAILY": {bg:C.grn,c:"166534"}, "WEEKLY": {bg:C.blu,c:"1E40AF"}, "MONTHLY": {bg:C.pur,c:"5B21B6"}, "P0": {bg:C.red,c:"991B1B"}, "P1": {bg:C.yel,c:"854D0E"}, "P2": {bg:C.blu,c:"1E40AF"} };
  const b = o.badge && sm[o.badge] ? sm[o.badge] : null;
  return new TableCell({ borders: bds, width: { size: w, type: WidthType.DXA }, shading: b ? { fill: b.bg, type: ShadingType.CLEAR } : o.bg ? { fill: o.bg, type: ShadingType.CLEAR } : o.alt ? { fill: C.alt, type: ShadingType.CLEAR } : undefined, margins: { top: 60, bottom: 60, left: 120, right: 120 }, children: [new Paragraph({ children: [new TextRun({ text: t, font: "Arial", size: o.sz||20, color: b?b.c:o.c||"374151", bold: o.b||false })] })] });
}
function mt(hdrs, rows, cw) {
  return new Table({ width: { size: cw.reduce((a,b)=>a+b,0), type: WidthType.DXA }, columnWidths: cw, rows: [
    new TableRow({ children: hdrs.map((h,i) => hc(h, cw[i])) }),
    ...rows.map((r,ri) => new TableRow({ children: r.map((c,ci) => typeof c==='object'&&c.t ? tc(c.t, cw[ci], c) : tc(String(c), cw[ci], { alt: ri%2===1 })) }))
  ]});
}
function h1(t) { return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 }, children: [new TextRun({ text: t, bold: true, font: "Arial", size: 36, color: C.pri })] }); }
function h2(t) { return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 }, children: [new TextRun({ text: t, bold: true, font: "Arial", size: 30, color: C.pri })] }); }
function h3(t) { return new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 200, after: 120 }, children: [new TextRun({ text: t, bold: true, font: "Arial", size: 26, color: C.pri })] }); }
function p(t,o={}) { return new Paragraph({ spacing: { after: 140 }, ...o, children: [new TextRun({ text: t, font: "Arial", size: 22, color: o.c||"374151" })] }); }
function bp(l,t) { return new Paragraph({ spacing: { after: 130 }, children: [new TextRun({ text: l, font: "Arial", size: 22, bold: true, color: C.pri }), new TextRun({ text: t, font: "Arial", size: 22, color: "374151" })] }); }
function sp(n=120) { return new Paragraph({ spacing: { before: n, after: n }, children: [] }); }
function bi(t,r="bul") { return new Paragraph({ numbering: { reference: r, level: 0 }, spacing: { after: 80 }, children: [new TextRun({ text: t, font: "Arial", size: 22, color: "374151" })] }); }
function ni(t,r="num1") { return new Paragraph({ numbering: { reference: r, level: 0 }, spacing: { after: 80 }, children: [new TextRun({ text: t, font: "Arial", size: 22, color: "374151" })] }); }
function box(title, body, color=C.acc) {
  return new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: [CW], rows: [new TableRow({ children: [new TableCell({
    borders: { top: { style: BorderStyle.SINGLE, size: 3, color }, bottom: { style: BorderStyle.SINGLE, size: 3, color }, left: { style: BorderStyle.SINGLE, size: 3, color }, right: { style: BorderStyle.SINGLE, size: 3, color } },
    width: { size: CW, type: WidthType.DXA }, shading: { fill: color===C.crit?"FEF2F2":color===C.warn?"FFFBEB":"F0FDF4", type: ShadingType.CLEAR },
    margins: { top: 180, bottom: 180, left: 280, right: 280 },
    children: [
      new Paragraph({ spacing: { after: 100 }, children: [new TextRun({ text: title, font: "Arial", size: 26, bold: true, color })] }),
      new Paragraph({ children: [new TextRun({ text: body, font: "Arial", size: 21, color: "374151" })] })
    ]
  })] })] });
}
function pb() { return new Paragraph({ children: [new PageBreak()] }); }

const doc = new Document({
  numbering: { config: [
    { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "num1", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.START, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "num2", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.START, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "num3", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.START, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
  ]},
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 36, bold: true, font: "Arial", color: C.pri }, paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 30, bold: true, font: "Arial", color: C.pri }, paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, font: "Arial", color: C.pri }, paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
    ]
  },
  sections: [
    // ===== TITLE PAGE =====
    {
      properties: { page: { size: { width: PW, height: 15840 }, margin: { top: MG, right: MG, bottom: MG, left: MG } } },
      children: [
        sp(2000),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: "PRINTMAXX AUTOMATION BLUEPRINT", font: "Arial", size: 52, bold: true, color: C.pri })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [new TextRun({ text: "Alpha-to-Ops Pipeline | Interactive HQ Terminal | Perpetual Improvement Loops", font: "Arial", size: 26, color: C.mut })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [new TextRun({ text: "February 9, 2026", font: "Arial", size: 22, color: C.mut })] }),
        sp(400),
        box("WHAT THIS DOCUMENT DOES",
          "Maps 137 automatable alpha entries to daily/weekly/monthly execution pipelines. Designs the PRINTMAXX Terminal as an interactive HQ that triggers tasks, shows checklists, and monitors everything. Defines backup/safety gates so no major overhaul happens without human approval. Leverages your M1 Max 64GB + Claude Max $200/mo for maximum parallel automation.",
          C.pri),
        sp(200),
        mt(["Your Hardware", "Capability", "What It Enables"], [
          ["M1 Max 64GB RAM", "10-core CPU, 32-core GPU, unified memory", "8+ parallel Claude agents, browser automation, video rendering simultaneously"],
          ["Claude Max $200/mo", "Unlimited messages, extended context, agent mode", "Overnight Ralph sprints, daily research loops, content generation at scale"],
          ["Claude Cowork", "Task scheduling, file access, browser control", "Automated daily/weekly/monthly tasks without cron, GUI monitoring"],
          ["Macbook Pro", "Always-on capability (lid closed = sleep)", "Scheduled wake for overnight sprints, pmset schedule wake"],
        ], [2200, 3200, 3960]),
      ]
    },
    // ===== SECTION 1: ALPHA TO OPS =====
    {
      properties: { page: { size: { width: PW, height: 15840 }, margin: { top: MG, right: MG, bottom: MG, left: MG } } },
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "PRINTMAXX Automation Blueprint | Feb 9, 2026", font: "Arial", size: 18, color: C.mut, italics: true })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Page ", font: "Arial", size: 18, color: C.mut }), new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: C.mut })] })] }) },
      children: [
        h1("1. Alpha Inventory: 137 Automatable Ops"),
        p("Your MEGA_SHEET TAB3 has 835 alpha entries. Of those, 137 map directly to operations that can be partially or fully automated. 61 are rated HIGHEST ROI. Here's how they break down by category and what can run daily."),
        sp(60),

        h2("1.1 Alpha by Category (Automatable Only)"),
        mt(["Category", "Count", "Top Auto Ops", "Daily Potential"],
          [
            [{t:"OUTBOUND",b:true}, "56", "Cold email sequences, Crunchbase scraping, LinkedIn DMs, voice note outreach", {t:"HIGH",badge:"HIGH"}],
            [{t:"MONETIZATION",b:true}, "29", "Digital product launches, pricing optimization, Gumroad listings, closing scripts", {t:"MEDIUM",badge:"MEDIUM"}],
            [{t:"TOOL_ALPHA",b:true}, "18", "Browser automation tools, MCP servers, n8n workflows, API wrappers", {t:"HIGH",badge:"HIGH"}],
            [{t:"APP_FACTORY",b:true}, "12", "Vibe-coded SaaS, app submissions, app store optimization", {t:"MEDIUM",badge:"MEDIUM"}],
            [{t:"GROWTH_HACK",b:true}, "8", "Organic viral launches, SaaS distribution, Reddit/HN tactics", {t:"HIGH",badge:"HIGH"}],
            [{t:"CONTENT_FORMAT",b:true}, "6", "Thread pipelines, atomic essays, Reddit AMAs to content", {t:"HIGH",badge:"HIGH"}],
            [{t:"PROGRAMMATIC_SEO",b:true}, "4", "Longtail page generation, internal linking, volume requirements", {t:"HIGH",badge:"HIGH"}],
            [{t:"OTHER (4 cats)",b:true}, "4", "Info products, automation, paid ads, local service", {t:"LOW",badge:"LOW"}],
          ],
          [2000, 800, 4360, 2200]),

        sp(120),
        h2("1.2 The 10 Highest-ROI Automatable Pipelines"),
        p("These are the specific alpha entries that map to daily automated execution. Each one can run as a Ralph loop or Cowork scheduled task."),
        sp(60),

        mt(["#", "Pipeline", "Alpha Source", "Daily Actions", "Revenue Path"],
          [
            ["1", "Crunchbase Funded Co. Outreach", "ALPHA059, ALPHA115, ALPHA175", "Scrape newly funded companies, enrich contacts via Apollo, generate personalized cold emails, send via Instantly", "$2-12K/deal, 2-5% close rate"],
            ["2", "Content-to-Product Pipeline", "ALPHA337299, ALPHA36DCFA", "Take approved alpha, generate 5 social posts + 1 thread + 1 newsletter + 1 Gumroad product spec per entry", "$20-200/product, 10+ products/week"],
            ["3", "Programmatic SEO Farm", "ALPHA109, ALPHA110", "Generate 10-20 longtail pages/day from alpha + niche data, auto-interlink, submit to Google", "$0.50-5/page/mo in ad revenue at scale"],
            ["4", "AI Automation Agency Outreach", "ALPHA762E85, ALPHA191", "Identify businesses spending $50K+ on manual processes, cold email automation ROI pitch", "$5-20K/deal, 1-2 deals/month"],
            ["5", "Voice Note DM Blitz", "ALPHA206, ALPHA091", "Generate AI voice notes for top 20 prospects/day, send via LinkedIn + Twitter DMs", "40%+ reply rate, $1-5K/converted lead"],
            ["6", "Digital Product Launch Cycle", "ALPHA3405F7, ALPHA075", "Create 1 Notion template or ebook/week from alpha, list on Gumroad, auto-promote", "$500-5K/mo passive per product"],
            ["7", "Newsletter Growth Engine", "ALPHA244, ALPHA063", "Daily alpha digest, weekly deep-dive, serialized content strategy", "$5-50/subscriber/year, scales to $10K+/mo"],
            ["8", "App Factory Sprint", "ALPHA086, ALPHA182", "Vibe-code 1 micro-SaaS/week using NextJS+Supabase+Clerk+Stripe stack", "$500-5K MRR per app at $5-20/mo"],
            ["9", "Platform Arbitrage Monitor", "ALPHA070, ALPHA116", "Daily scan for pricing gaps, API changes, new platform features to exploit", "Variable, $1-50K/opportunity"],
            ["10", "LinkedIn + Loom Prospecting", "ALPHA082, ALPHA210", "Auto-generate Loom scripts, record batch videos, send with LinkedIn connection requests", "$10K+ deals, 5-10% conversion"],
          ],
          [400, 2000, 1800, 3160, 2000]),

        // ===== SECTION 2: AUTOMATION ARCHITECTURE =====
        pb(),
        h1("2. Automation Architecture"),
        p("Three automation layers work together. Each has different strengths and the system needs all three to cover daily ops, overnight processing, and interactive monitoring."),
        sp(60),

        h2("2.1 The Three Automation Layers"),
        mt(["Layer", "Tool", "Strengths", "Best For", "Limitations"],
          [
            ["1. Ralph Loops", "Claude Code + bash scripts", "Deep multi-step agent work, git-backed state, fresh context each iteration", "Overnight research sprints, content generation, system audits", "Requires Terminal, manual trigger currently"],
            ["2. Cowork Shortcuts", "Claude Cowork + create-shortcut skill", "Scheduled tasks (daily/weekly/monthly), file access, browser control, no cron needed", "Daily checklists, file sync, report generation, monitoring", "Single task at a time, no parallel agents"],
            ["3. PRINTMAXX Terminal", "Textual TUI (Python)", "Interactive dashboard, drill-down views, real-time monitoring, task launching", "HQ command center, health monitoring, manual task triggers", "Requires Terminal window, Python deps"],
          ],
          [1600, 2000, 2200, 1960, 1600]),

        sp(120),
        h2("2.2 How They Wire Together"),
        p("The three layers form a feedback loop. Ralph runs overnight and produces outputs. Cowork shortcuts run at scheduled intervals to process those outputs. The Terminal displays everything and lets you trigger ad-hoc tasks."),
        sp(60),
        bp("10:00 PM - Ralph Overnight Sprint: ", "8 parallel loops launch via run_overnight_sprint.sh. Research, content gen, meta detection, backtesting all run simultaneously. Your M1 Max with 64GB can handle 8 Claude agents + browser automation without breaking a sweat."),
        bp("6:00 AM - Cowork Morning Sync: ", "Scheduled shortcut runs extract_source_csvs, syncs ALPHA_STAGING.csv, scores new entries, generates Buffer CSVs for the day's social posts."),
        bp("8:00 AM - You Open Terminal HQ: ", "Dashboard shows overnight results: new alpha found, content generated, methods scored, any alerts. Interactive checklists show what needs human review. Click to approve/reject."),
        bp("Throughout Day - Cowork Background Tasks: ", "Outreach sequences send on schedule. Content QA auto-processes. Backtest results merge. All logged."),
        bp("6:00 PM - Cowork Evening Digest: ", "Scheduled shortcut generates daily summary: what ran, what earned, what needs attention tomorrow."),

        // ===== SECTION 3: COWORK SCHEDULED TASKS =====
        pb(),
        h1("3. Cowork Scheduled Tasks (Replace Cron)"),
        p("Claude Cowork has a create-shortcut skill that can schedule recurring tasks. This replaces crontab entirely and is more reliable on macOS (which can miss cron jobs during sleep). Each shortcut is a self-contained automation that runs at the specified interval."),
        sp(60),

        box("WHY COWORK SHORTCUTS > CRON",
          "macOS cron jobs don't fire when the laptop is asleep. launchd agents are better but complex to configure. Cowork shortcuts are the simplest path: they run in the Cowork environment with full file access, can trigger shell commands, and have built-in scheduling. Plus they show in the Cowork UI so you can monitor them.",
          C.pri),

        sp(100),
        h2("3.1 DAILY Shortcuts"),
        mt(["Shortcut Name", "Time", "What It Does", "Files Touched"],
          [
            ["morning-alpha-sync", "6:00 AM", "Run extract_source_csvs_from_mega_sheet.py to sync ALPHA_STAGING.csv from MEGA_SHEET. Run organize_alpha.py to score/classify new entries.", "LEDGER/ALPHA_STAGING.csv, MEGA_SHEET/*.csv"],
            ["morning-content-gen", "6:30 AM", "Generate 10 social posts from top approved alpha using /generate-posts logic. Create Buffer-ready CSVs.", "04_CONTENT/social/, LEDGER/buffer_imports/"],
            ["outreach-queue", "9:00 AM", "Process cold email queue: check which sequences are due, prepare personalized first lines, stage for sending", "MONEY_METHODS/COLD_OUTBOUND/, EMAIL/sequences/"],
            ["evening-digest", "6:00 PM", "Generate daily summary: alpha processed, content created, revenue tracked, alerts", "OPS/reports/daily_digest_YYYYMMDD.md"],
            ["nightly-backup", "9:00 PM", "Git commit all changes with timestamp, push to remote if configured", "Entire project (git)"],
            ["overnight-sprint-trigger", "10:00 PM", "Launch ralph/run_overnight_sprint.sh in background", "ralph/logs/overnight_*.log"],
          ],
          [2200, 1000, 4160, 2000]),

        sp(100),
        h2("3.2 WEEKLY Shortcuts (Mondays)"),
        mt(["Shortcut Name", "What It Does", "Files Touched"],
          [
            ["weekly-system-validate", "Run full validation: CSV integrity, content compliance, code quality, broken references", "OPS/reports/weekly_validation.md"],
            ["weekly-backtest-merge", "Consolidate all backtest results from the week, update method performance scores", "LEDGER/BACKTESTS/, scripts/merge_backtest_scores.py"],
            ["weekly-calendar-refresh", "Regenerate 30-day content calendar from current alpha + trending topics", "04_CONTENT/generated/content_calendar.csv"],
            ["weekly-content-qa", "Batch-process all PENDING_REVIEW content, auto-approve meeting quality threshold", "OPS/CONTENT_QA_QUEUE/"],
            ["weekly-competitor-scan", "Ralph loop: scan competitor sites, SEO rankings, new products/features", "10_RESEARCH/competitors/"],
            ["weekly-platform-monitor", "Check X/TikTok/YouTube official blogs for algorithm changes, policy updates", "06_OPERATIONS/trend_intel/"],
          ],
          [2600, 4560, 2200]),

        sp(100),
        h2("3.3 MONTHLY Shortcuts (1st of Month)"),
        mt(["Shortcut Name", "What It Does", "Files Touched"],
          [
            ["monthly-portfolio-rebalance", "Kelly Criterion recalculation across all 69 methods based on actual performance data", "LEDGER/REBALANCE_REPORTS/, LEDGER/KELLY_ALLOCATIONS.csv"],
            ["monthly-pnl", "Aggregate REVENUE_TRACKER + EXPENSE_TRACKER into P&L. Compare to projections", "FINANCIALS/P_AND_L_MONTHLY.csv"],
            ["monthly-method-review", "Score all methods, kill underperformers (<20 health), promote winners (>80 health)", "LEDGER/MEGA_SHEET/TAB1_MONEY_METHODS_MASTER.csv"],
            ["monthly-mega-audit", "27-task system audit: data integrity, missing files, broken references, stale entries", "OPS/reports/monthly_audit_YYYYMM.md"],
            ["monthly-niche-review", "Review all 34 niches: engagement rates, revenue per niche, growth trajectory", "LEDGER/MEGA_SHEET/TAB2_NICHES_MASTER.csv"],
            ["monthly-full-backup", "Full project backup: git bundle + zip archive to external location", "Backup to ~/Documents/PRINTMAXX_BACKUPS/"],
          ],
          [2600, 4560, 2200]),

        // ===== SECTION 4: TERMINAL HQ UPGRADE =====
        pb(),
        h1("4. PRINTMAXX Terminal HQ Upgrade"),
        p("The existing Textual TUI is powerful but read-only. Here's the design for making it an interactive command center where you can trigger tasks, approve alpha, and manage checklists without jumping between Claude Code instances."),
        sp(60),

        h2("4.1 New Interactive Features"),
        mt(["Feature", "What It Does", "Implementation"],
          [
            ["Daily Checklist Tab", "Shows today's tasks with checkboxes. Auto-populated from morning-alpha-sync results + manual items.", "New TabPane with DataTable + Toggle widgets. Persists to OPS/checklists/daily_YYYYMMDD.json"],
            ["Task Launcher", "Click a button to trigger any automation (Ralph loop, script, Cowork shortcut)", "Button grid in new 'Launch' tab. Each button runs subprocess.Popen() with the target script"],
            ["Alpha Review Queue", "Shows PENDING alpha entries. Click to APPROVE/REJECT/FLAG with inline notes", "Modified Alpha tab with action buttons. Writes back to ALPHA_STAGING.csv"],
            ["Overnight Results Panel", "Shows results from last night's Ralph sprint: new alpha found, content generated, errors", "Reads ralph/logs/overnight_*.log, parses for key metrics"],
            ["Backup Status", "Shows last backup time, git status, uncommitted changes count", "Reads git log/status, shows in footer or dedicated panel"],
            ["Automation Monitor", "Live view of running processes (Ralph loops, scrapers, Cowork tasks)", "subprocess check + psutil for process monitoring"],
            ["Revenue Dashboard", "Daily/weekly/monthly revenue with sparklines, method breakdown", "Enhanced existing financial panel with charting"],
            ["Quick Actions Bar", "Keyboard shortcuts: R=run research, C=generate content, B=backup, A=approve alpha", "Textual key bindings mapped to functions"],
          ],
          [2200, 3560, 3600]),

        sp(100),
        h2("4.2 Terminal Architecture"),
        p("The upgraded terminal stays as a single Python file (printmaxx_tui.py) but gains a task execution engine and a checklist persistence layer. All task triggers use subprocess so the TUI never blocks."),
        sp(60),
        bp("Task Execution Engine: ", "A TaskRunner class that wraps subprocess.Popen. Each task gets a unique ID, log file, start time, and status (RUNNING/COMPLETED/FAILED). The Monitor tab shows all active tasks."),
        bp("Checklist Persistence: ", "Daily checklists save to OPS/checklists/daily_YYYYMMDD.json. When you check an item, it writes immediately. Next morning, a new checklist auto-generates from the template + overnight results."),
        bp("Alpha Review Integration: ", "The review queue reads ALPHA_STAGING.csv, filters for status=PENDING_REVIEW, and lets you approve/reject inline. Approved entries trigger the Zero Waste Protocol (content generation)."),
        bp("Wiring to Quant Terminal: ", "The risk engine (printmaxx_quant_terminal.py) is imported as a module. Portfolio risk metrics display in the main TUI's Risk tab, no separate launch needed."),

        // ===== SECTION 5: SAFETY & BACKUP =====
        pb(),
        h1("5. Safety Gates & Backup Protocol"),
        p("Every automation has guardrails. No major changes happen without a backup. No structural overhaul without human approval. Here's the full safety framework."),
        sp(60),

        box("CORE SAFETY PRINCIPLE",
          "Every automated action that modifies data must: (1) create a backup first, (2) log what it changed, (3) be reversible. Any action that would restructure folders, delete files, or change more than 50 CSV rows requires human approval via the Terminal's approval queue.",
          C.crit),

        sp(100),
        h2("5.1 Backup Strategy"),
        mt(["Backup Type", "Frequency", "What", "Where", "Retention"],
          [
            ["Git Auto-Commit", "Daily 9 PM", "All changed files (git add -A, commit with timestamp)", "Local .git + GitHub remote", "Full history (infinite)"],
            ["Git Bundle", "Monthly 1st", "Complete repo as single .bundle file", "~/Documents/PRINTMAXX_BACKUPS/", "Last 6 months"],
            ["CSV Snapshot", "Before any batch operation", "Copy of all LEDGER/*.csv files", "LEDGER/.snapshots/YYYYMMDD_HHMMSS/", "Last 30 snapshots"],
            ["Pre-Overhaul Backup", "Before any structural change", "Full project zip", "~/Documents/PRINTMAXX_BACKUPS/pre_overhaul/", "Keep all"],
          ],
          [2000, 1400, 3160, 2200, 1600]),

        sp(100),
        h2("5.2 Human-in-the-Loop Gates"),
        mt(["Action", "Requires Approval?", "How"],
          [
            ["Add new alpha entries to ALPHA_STAGING", "No (auto)", "Auto-scored, auto-classified. Shows in review queue for optional human override"],
            ["Approve/reject alpha entries", "YES", "Must be clicked in Terminal HQ or explicitly approved in Cowork"],
            ["Generate social content from approved alpha", "No (auto)", "Runs on approved entries only. Content goes to QA queue"],
            ["Post content to social platforms", "YES", "Buffer CSVs generated automatically, but actual posting requires human upload to Buffer"],
            ["Send cold emails", "YES (first send)", "Sequences are staged. First send of any new sequence requires human approval. Follow-ups auto-send"],
            ["Restructure folders", "YES (always)", "Pre-overhaul backup + approval prompt in Terminal. Never auto-restructure"],
            ["Delete files", "YES (always)", "No automated deletion ever. Archive instead. Human deletes manually if needed"],
            ["Change method scores/allocations", "No (auto) with override", "Monthly rebalance runs automatically but shows diff for review. Human can override"],
            ["Major research pivot", "YES", "If overnight research suggests a fundamental strategy change, it goes to approval queue with full context"],
            ["Install new tools/dependencies", "YES", "Never auto-install. Recommendation goes to checklist"],
          ],
          [3000, 2000, 4360]),

        sp(100),
        h2("5.3 The Perpetual Improvement Loop"),
        p("This is the core feedback cycle that runs continuously and gets smarter over time:"),
        sp(60),
        ni("RESEARCH: Overnight Ralph loops scan 92 Twitter accounts, 41 subreddits, GitHub trending, Product Hunt, Crunchbase. New alpha extracted and scored.", "num1"),
        ni("CLASSIFY: Morning sync scores alpha 0-100, classifies as APPROVED/REJECTED/REPURPOSE. Bot detection and earnings skepticism applied automatically.", "num1"),
        ni("GENERATE: Approved alpha triggers Zero Waste Protocol. 5+ social posts, 1 thread, 1 newsletter draft, 1 product spec per entry. All go to QA queue.", "num1"),
        ni("DISTRIBUTE: QA-approved content gets Buffer CSVs generated. Cold email sequences staged. Newsletter drafts queued. Human reviews and sends.", "num1"),
        ni("MEASURE: Revenue, engagement, conversion tracked in FINANCIALS/ and LEDGER/. Method health scores update daily.", "num1"),
        ni("OPTIMIZE: Weekly backtest merge scores method performance. Monthly rebalance shifts allocation to winners. Quarterly strategy review.", "num1"),
        ni("LEARN: Every Ralph loop iteration writes to progress.txt. Patterns, failures, and discoveries accumulate. Next iteration reads these and improves.", "num1"),
        sp(60),
        p("This loop never stops. It only gets smarter. Every cycle adds data, refines scoring, and improves content quality. The M1 Max runs it overnight while you sleep."),

        // ===== SECTION 6: IMPLEMENTATION PLAN =====
        pb(),
        h1("6. Implementation Plan (Priority Order)"),
        p("Here's exactly what to do, in order, with time estimates. Total: ~8 hours spread across 2-3 sessions."),
        sp(60),

        h2("Phase 1: Fix Foundation (2 hours)"),
        mt(["#", "Task", "Time", "Priority"],
          [
            ["1.1", "Create ALPHA_STAGING.csv by running extract_source_csvs_from_mega_sheet.py", "15 min", {t:"P0",badge:"P0"}],
            ["1.2", "Install Python deps: pip install rich textual numpy", "10 min", {t:"P0",badge:"P0"}],
            ["1.3", "Fix ValueError bugs in revenue_projector.py and method_performance_analyzer.py", "30 min", {t:"P0",badge:"P0"}],
            ["1.4", "Create requirements.txt with all dependencies", "5 min", {t:"P1",badge:"P1"}],
            ["1.5", "Set up GitHub remote for backup (git remote add origin + first push)", "15 min", {t:"P0",badge:"P0"}],
            ["1.6", "Test printmaxx_tui.py launches successfully", "15 min", {t:"P0",badge:"P0"}],
            ["1.7", "Test printmaxx_quant_terminal.py launches successfully", "15 min", {t:"P0",badge:"P0"}],
          ],
          [500, 5360, 1200, 2300]),

        sp(100),
        h2("Phase 2: Set Up Cowork Shortcuts (2 hours)"),
        mt(["#", "Task", "Time", "Priority"],
          [
            ["2.1", "Create morning-alpha-sync shortcut (daily 6 AM)", "15 min", {t:"P0",badge:"P0"}],
            ["2.2", "Create nightly-backup shortcut (daily 9 PM, git commit + push)", "15 min", {t:"P0",badge:"P0"}],
            ["2.3", "Create overnight-sprint-trigger shortcut (daily 10 PM)", "15 min", {t:"P0",badge:"P0"}],
            ["2.4", "Create morning-content-gen shortcut (daily 6:30 AM)", "15 min", {t:"P1",badge:"P1"}],
            ["2.5", "Create evening-digest shortcut (daily 6 PM)", "15 min", {t:"P1",badge:"P1"}],
            ["2.6", "Create all weekly shortcuts (5 shortcuts)", "30 min", {t:"P1",badge:"P1"}],
            ["2.7", "Create all monthly shortcuts (6 shortcuts)", "30 min", {t:"P2",badge:"P2"}],
          ],
          [500, 5360, 1200, 2300]),

        sp(100),
        h2("Phase 3: Upgrade Terminal HQ (3 hours)"),
        mt(["#", "Task", "Time", "Priority"],
          [
            ["3.1", "Add TaskRunner class to printmaxx_tui.py for subprocess management", "30 min", {t:"P1",badge:"P1"}],
            ["3.2", "Add Daily Checklist tab with persistence to JSON", "30 min", {t:"P1",badge:"P1"}],
            ["3.3", "Add Task Launcher tab with button grid for all automations", "30 min", {t:"P1",badge:"P1"}],
            ["3.4", "Add Alpha Review Queue with APPROVE/REJECT actions", "30 min", {t:"P1",badge:"P1"}],
            ["3.5", "Add Overnight Results panel parsing Ralph logs", "20 min", {t:"P2",badge:"P2"}],
            ["3.6", "Wire quant terminal risk engine as importable module", "20 min", {t:"P2",badge:"P2"}],
            ["3.7", "Add keyboard shortcuts (R/C/B/A quick actions)", "15 min", {t:"P2",badge:"P2"}],
          ],
          [500, 5360, 1200, 2300]),

        sp(100),
        h2("Phase 4: Wire Outreach Pipeline (1 hour)"),
        mt(["#", "Task", "Time", "Priority"],
          [
            ["4.1", "Set up Tier 1 infra: 3 cold email domains on Porkbun + Google Workspace", "Human task", {t:"P1",badge:"P1"}],
            ["4.2", "Create cold email sequence templates from ALPHA059, ALPHA175 frameworks", "20 min", {t:"P1",badge:"P1"}],
            ["4.3", "Create outreach-queue shortcut that stages daily sends", "15 min", {t:"P1",badge:"P1"}],
            ["4.4", "Create lead enrichment script using Apollo free tier", "20 min", {t:"P2",badge:"P2"}],
          ],
          [500, 5360, 1200, 2300]),

        sp(200),
        box("WHAT YOU GET WHEN THIS IS DONE",
          "A system where you wake up to: overnight research results scored and classified, 10+ social posts ready for review, cold email sequences staged for approval, a daily checklist auto-generated in your Terminal HQ, all backed up to git. You review for 30 minutes, approve what looks good, and the machine keeps running. The M1 Max handles the compute, Claude Max handles the intelligence, and you handle the decisions that matter.",
          C.acc),

        sp(200),
        box("NEXT STEP",
          "Say 'start phase 1' and I'll begin fixing the foundation: create ALPHA_STAGING.csv, install deps, fix broken scripts, set up git remote, and verify both terminals launch. Or say 'create the shortcuts' to jump straight to Phase 2 if foundation is already solid.",
          C.pri),
      ]
    }
  ]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/sessions/awesome-nice-brown/mnt/PRINTMAXX_STARTER_KITttttt/PRINTMAXX_AUTOMATION_BLUEPRINT_FEB9.docx", buf);
  console.log("Blueprint created: PRINTMAXX_AUTOMATION_BLUEPRINT_FEB9.docx");
});
