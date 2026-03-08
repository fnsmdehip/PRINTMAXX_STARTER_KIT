# PRINTMAXX CODEBASE GRAMMAR
# Generated: 2026-03-08T01:33:51.475922
# 20 scripts | Instant system understanding

## EXECUTION HIERARCHY
  level_0_orchestrator: ceo_agent.py
  level_1_engines: venture_autonomy.py, agent_swarm.py, decision_engine.py
  level_2_intelligence: intelligence_router.py, alpha_query.py, daily_digest.py
  level_3_execution: twitter_warmup_poster.py, daily_engagement_planner.py, alpha_auto_processor.py, daily_research_orchestrator.py
  level_4_collection: twitter_alpha_scraper.py, background_reddit_scraper.py
  level_5_quality: quality_gate.py, compliance_scanner.py, system_health_monitor.py
  level_6_maintenance: loop_closer.py, memory_manager.py, wire_missed_intelligence.py, build_codebase_grammar.py

## STATE FILES
  ceo_state: AUTOMATIONS/agent/ceo_agent/ceo_state.json
  swarm_state: AUTOMATIONS/agent/swarm/swarm_state.json
  autonomy_state: AUTOMATIONS/agent/autonomy/autonomy_state.json
  warmup_state: AUTOMATIONS/agent/twitter_warmup_state.json
  alpha_staging: LEDGER/ALPHA_STAGING.csv
  intelligence_catalog: OPS/INTELLIGENCE_CATALOG.json
  decisions_log: AUTOMATIONS/agent/ceo_agent/decisions.jsonl
  missions_log: AUTOMATIONS/agent/missions.jsonl
  message_bus: AUTOMATIONS/agent/message_bus.jsonl

## CRON SCHEDULE
  6:00 AM: twitter_alpha_scraper (133 accounts)
  6:15 AM: background_reddit_scraper
  6:30 AM: alpha_auto_processor --process-new
  6:45 AM: daily_digest --days 1 --save
  7:00 AM: daily_engagement_planner --save
  midnight: twitter_warmup_poster --advance
  every 2h: ceo_agent cycle, loop_closer --cycle
  every 4h: agent_swarm swarm_brain cycle

## SCRIPTS

### ceo_agent.py (2023L) — 24/7 orchestrator — scores ops, makes PROMOTE/ENHANCE/CREATE/KILL/DISCOVER decisions, delegates to ventures
  class GitGuard: [__init__(), snapshot(label), rollback(), post_change_commit(summary)]
  class XlsxIntel: [__init__(), _find_xlsx(), _load(), get_all_ops(), get_auto_status(), get_priority_launch(), get_synergy_stacks(), get_venture_map(), get_expansion_queue(), get_op_by_id(op_id)]
  class CEOState: [__init__(), _load(), _default(), save(), log_decision(decision), log_audit(audit_entry), is_protected(op_id), protect_op(op_id), get_score_trend(op_id, periods)]
  class VentureScorer: [__init__(xlsx, state), score_all(), _score_op(op, auto_status, venture_info, synergies), _parse_revenue_score(rev_str)]
  class CEOBrain: [__init__(scorer, xlsx, state), _get_strategic_intelligence(), analyze_and_decide(dry_run)]
  class VentureRunner: [__init__(state, xlsx), execute_decisions(decisions), _execute_promote(decision), _execute_enhance(decision), _execute_create(decision), _execute_kill(decision), _execute_discover(decision), run_dynamic_ventures(), _try_auto_fix(op_id, blocker), run_existing_ventures()]
  class AuditTrail: [__init__(state), capture_baseline(), check_regression(results)]
  class LockGuard: [__init__(), acquire(), release()]
  fn: safe_path(p) | safe_command(cmd_str) | disk_free_gb() | ts() | log(msg, level) | run_script(script_path, args, timeout_sec, label) — Run a PRINTMAXX script with guardrails. Returns (success, output). | _hours_since(iso_ts) — Return hours elapsed since an ISO timestamp string. Returns float('inf') if None | run_ceo_cycle(dry_run) — Run one full CEO cycle: score → decide → snapshot → execute → audit. | show_status() — Show full CEO agent status dashboard. | run_daemon() — Run the CEO agent 24/7. | main()
  cli: --status --daemon --score --decide --run --protect --rollback --alpha --research --content --health --decision-engine --ventures --cron-list --cron-add

### agent_swarm.py (1415L) — 22 operational agents — generates launchd plists, manages health, AGENT_VENTURE_MAP for intelligence injection
  class SwarmState: [__init__(), save(), update_agent(agent_id, updates)]
  fn: safe_path(p) | ts() | log(msg, level) | get_agent_intelligence(agent_id) — Query intelligence router for this agent's venture context. | generate_plist(agent_id, agent_def) — Generate a launchd plist for a swarm agent. | install_agent(agent_id) — Generate plist and install via launchctl. | uninstall_agent(agent_id) — Unload and remove a swarm agent. | list_installed() — List all installed swarm agents. | show_status() | deploy_all() | kill_all() | show_logs(agent_id) | health_check() | main()
  cli: --status --deploy --list --kill --kill-all --logs --health --run

### venture_autonomy.py (1634L) — 8 venture types — universal execution engine, self-managing schedules, SelfManager auto-adjusts
  class AutonomyState: [__init__(), _load(), save(), get_venture(venture_id), add_venture(venture_id, venture_def), update_venture(venture_id, updates), get_active_ventures()]
  class VentureAutonomyEngine: [__init__(state), create_venture(venture_type, name, config), run_venture(venture_id), run_all_active(), _get_venture_intelligence(venture_type, step), _run_with_claude(venture_id, venture, step, vtype), _save_step_result(venture_id, step, success, output), _generate_schedule_configs(venture_id, venture_def), _generate_llm_launchd_plist(venture_id, venture_def, vtype, interval_hours), _generate_script_launchd_plist(venture_id, venture_def, interval_hours)]
  class SchedulerManager: [install_launchd(venture_id, mode), uninstall_launchd(venture_id), install_all_llm(), install_cron(venture_id), list_installed()]
  class SelfManager: [__init__(state, engine), run_self_management_cycle(), _ensure_all_scheduled(), _fix_broken_schedules(), _adjust_intervals(), _create_from_opportunities(), _prune_dead_ventures()]
  fn: _sig(s, f) | safe_path(p) | ts() | log(msg, level) | run_cmd(cmd, timeout_sec, label) — Run a command with guardrails. Returns (success, output). | run_script(script_name, args, timeout_sec, label) — Run a PRINTMAXX automation script. | _hours_since(iso_ts) | log_mission(mission_name, result, duration_s, output) — Log to the shared agent mission log (same format as monitor.py expects). | send_bus_message(body, to_agent) — Send a message on the shared inter-agent bus. | show_status() | list_types() | run_daemon() — Run the autonomy engine forever, cycling all active ventures. | main()
  cli: --status --run --run-all --create --list-types --schedule --install-launchd --install-script-launchd --install-cron --install-all --import-ceo --daemon --pause --resume-venture --bootstrap --self-manage

### intelligence_router.py (1609L) — central intelligence hub — 484 docs, 14,799 alpha, 16 CSVs across 9 ventures
  fn: safe_path(p) — Verify path is within project root. Raises ValueError if not. | ts() | load_catalog() — Load INTELLIGENCE_CATALOG.json if it exists, merge with hardcoded map. | query_alpha(venture_type, top) — Query alpha_query.py for top alpha entries relevant to a venture. | find_existing_docs(venture_type) — Return list of (path, description, exists) for a venture's docs. | find_existing_dirs(venture_type) — Return list of (dir_path, description, file_count, files) for directories. | find_existing_csvs(venture_type) — Return list of (path, description, exists, row_count) for LEDGER CSVs. | find_swarm_reports(venture_type, max_reports) — Find the most recent swarm reports relevant to a venture type. | find_task_docs(venture_type, task_type) — Get the most relevant docs for a specific task within a venture. | extract_doc_summary(doc_path, max_lines) — Extract key sections from a doc (headers + first few lines under each). | get_intelligence(venture_type, task_type, include_summaries, alpha_count) | compute_stats() — Compute coverage statistics across all venture types. | format_human_output(intel, mode) — Format intelligence for human-readable CLI output. | format_stats_output(stats) — Format stats for human-readable output. | format_catalog_output() — Show the full document-to-venture mapping.
  cli: --venture --task --json --brief --full --stats --catalog --list-ventures --alpha-count

### daily_engagement_planner.py (602L) — warmup-aware daily action plan — posts, replies, likes, follows with timing
  fn: load_warmup_state() | get_phase(day) | get_system_metrics() — Pull real metrics from the system for use in reply templates. | get_todays_posts(phase_config, state) — Get warmup-safe posts for today from posting queue. | get_intelligence_brief(venture, task) — Pull intelligence brief for the plan. | populate_reply_template(hook_key, metrics) — Fill a reply hook template with real metrics. | generate_plan(day_override, save) — Generate the daily engagement plan. | show_metrics() — Show current system metrics that would be used in replies. | main()
  cli: --save --tomorrow --metrics

### twitter_warmup_poster.py (365L) — 21-day warmup poster — 5 phases (LURK/ENGAGE/SOFT_POST/RAMP/FULL_OPS)
  fn: load_state() | save_state(state) | get_phase(day) | load_approved_posts() — Load all approved posts from CSV files, newest first. | filter_for_warmup(posts, phase_config, state) — Filter posts based on warmup phase rules. | pick_posts(filtered, max_count) — Pick posts to send, with some randomization for natural feel. | show_status(state) | do_post(state, dry_run) | log_post(text, post_meta) — Log posted content to POSTED_LOG.csv | main()
  cli: --status --post --dry-run --set-day --advance

### daily_digest.py (254L) — human-readable system activity summary — alpha, content, agents, changes
  fn: get_date_range(days) | alpha_summary(dates) | content_summary(dates) | agent_summary(dates) | blocker_summary() | improvements_summary(dates) | main()
  cli: --days --save

### alpha_query.py (375L) — venture-based alpha queries with ROI normalization — search/filter 14,799 entries
  fn: normalize_roi(val) — Fix corrupted ROI values from CSV misalignment. | load_alpha() — Load all alpha entries from CSV, fixing known data quality issues. | score_entry(entry, venture_config) — Score how relevant an alpha entry is to a venture type. | query_venture(entries, venture_type, status_filter, limit) — Query alpha entries relevant to a venture type. | keyword_search(entries, query, limit) — Full-text keyword search across all alpha fields. | query_by_category(entries, category, limit) — Query by exact category match. | top_alpha(entries, limit) — Get top alpha entries by ROI potential. | show_stats(entries) — Show alpha distribution stats. | format_result(score, entry, verbose) — Format a single result for display. | main()
  cli: --venture --category --search --top --status --stats --untagged --json --verbose

### loop_closer.py (886L) — closes open loops — decision execution, feedback tracking, pipeline advancement
  fn: log(msg, level) | log_action(action_type, target, result, details) | load_state() | save_state(state) | run_cmd(cmd, timeout, label) | adjust_interval(agent_id, params, dry_run) | kill_agent(agent_id, dry_run) | deploy_agent(agent_id, dry_run) | create_venture(venture_type, params, dry_run) | boost_agent(agent_id, dry_run) | throttle_agent(agent_id, dry_run) | run_script_action(script, params, dry_run) | process_alpha(dry_run) | execute_weekly_target(target_key, params, dry_run) — Execute an agent-owned weekly target by triggering the relevant swarm agent. | generate_content(target, params, dry_run)
  cli: --cycle --decisions --feedback --pipeline --status --dry-run

### decision_engine.py (673L) — closed-loop decision processing — pending data → actions
  class FreelancePipeline: [analyze(dry_run), _generate_responses(opportunities)]
  class EcomArbPipeline: [analyze(dry_run), _generate_listings(products)]
  class AlphaPipeline: [analyze(dry_run), _escalate_scale_items(items)]
  class ContentIntegrationPipeline: [analyze(dry_run), _integrate_outputs(dirs, marker_file, already_done)]
  class BrokenCronFixer: [diagnose(), fix(dry_run)]
  class CronOptimizer: [__init__(), _read_crontab(), analyze()]
  fn: safe_path(target) | log(msg, level) | log_decision(source, action, reasoning, outcome) — Append to decisions ledger for full audit trail. | read_csv_tail(filepath, n) — Read last N rows of a CSV file. | count_csv_rows(filepath) | run_cycle(dry_run) — Run one full decision cycle across all pipelines. | run_daemon() — Run continuously, one cycle every 30 minutes. | show_status() — Show current pipeline status. | main()
  cli: --cycle --daemon --status --dry-run --fix-broken

### alpha_auto_processor.py (796L) — auto-processes ALPHA_STAGING.csv — routes to ventures/OPS/cron/archive
  fn: now_iso() | log(msg) — Append to log file and print to stderr. | safe_path(target) — Verify path is within project root. | text_hash(text) — Short hash for dedup. | build_ops_index() | _kw_score(text, keywords, max_pts) — Count how many keyword patterns match, scale to max_pts. | score_alpha(row) | check_redundancy(row, seen_hashes, ops_index) | find_ops_match(row, ops_index) | detect_timeframe(text) | route_alpha(row, score, ops_index) | create_venture_stub(row, score, dry_run) — Create a stub OPS file for a new venture opportunity. | bolster_existing(row, target_path, score, dry_run) — Append alpha intelligence to an existing OPS file. | add_cron_entry(row, cron_schedule, dry_run) — Append a cron entry specification. | add_to_high_value_queue(row, score, dry_run) — Add entry to the high-value queue for human review.

### system_health_monitor.py (858L) — health checks — agents, cron, disk, processes
  fn: _now() | _file_age_h(p) — Hours since file was last modified. Returns inf if missing. | _newest_in_dir(directory, pattern) — Age in hours of newest file matching pattern in directory. inf if none. | _newest_matching(base_dir, pattern) — Age of newest file matching glob pattern under base_dir. | _csv_rows(p) — Count data rows in CSV (excludes header). 0 if missing. | _http_status(url, timeout) — HTTP status code for url. 0 on failure. Uses curl, then urllib fallback. | _crontab_text() — Return current crontab contents as string, empty on error. | _sev(age_h, amber, red) — Map age to severity: GREEN / AMBER / RED. | _status_word(sev) | _fmt_age(h) | check_01_cron_jobs() — Cron job freshness: entries installed + key logs producing output. | check_02_pipeline_freshness() — Pipeline freshness: ANALYZED_LEADS, HOT_LEADS_QUALIFIED, progress.json. | check_03_live_sites() — Live site uptime: check all 16 surge.sh sites return 200. | check_04_memory_system() — Memory system: HEARTBEAT.md + active-tasks.md freshness. | check_05_lead_growth() — Lead pipeline growth: row counts across lead files.
  cli: --check --quick --json --skip-sites

### daily_research_orchestrator.py (1054L) — research pipeline — scrapers, alpha review, content generation
  fn: acquire_lock() | release_lock() | fetch_json(url, timeout) — Fetch JSON from URL with rate limiting and error handling. | fetch_text(url, timeout) — Fetch raw text/HTML from URL. | content_hash(text) — MD5 hash of normalized text for deduplication. | load_existing_hashes() — Load content hashes from existing ALPHA_STAGING entries to avoid duplicates. | is_duplicate(text, url) — Check if content already exists in ALPHA_STAGING. | mark_seen(text, url) — Mark content as seen for this run. | get_next_alpha_id() — Get the next alpha_id number from ALPHA_STAGING.csv. | append_alpha_entries(entries, dry_run) — Append entries to ALPHA_STAGING.csv. Returns count appended. | categorize_finding(text) — Categorize a finding based on keyword matching. | score_finding(text, upvotes, comments) — Score a finding 0-100 for relevance and quality. | score_to_status(score) — Convert score to alpha status. | score_to_roi(score) — Convert score to ROI potential. | run_existing_scrapers() — Run existing scraper scripts via subprocess. Returns run results.
  cli: --full --gaps-only --dry-run --status

### quality_gate.py (1445L) — hard quality gate — blocks slop before deployment, rewrites bad content
  class AppQualityScorer: [__init__(), score_all(), _score_app(name, files), _aggregate_fixes(items)]
  class ContentQualityScorer: [__init__(), score_all(), _score_content_file(path), _aggregate_fixes(items)]
  class EmailQualityScorer: [__init__(), score_all(), _score_email_file(path), _extract_emails(content, path), _score_single_email(email_text), _fix_for_dimension(dim, score, content), _aggregate_fixes(items)]
  class ListingQualityScorer: [__init__(), score_all(), _score_listing(path), _aggregate_fixes(items)]
  class ScriptQualityScorer: [__init__(), score_all(), _score_script(path), _aggregate_fixes(items)]
  class QualityGate: [__init__(), score_dimension(dim), score_all(), gate_check(), overall_score(), print_summary(), _score_bar(score, width), generate_report(), to_json()]
  fn: rating(score) | rating_symbol(score) | collect_files(dirs, extensions, recursive) — Collect files from multiple directories, handling missing dirs gracefully. | safe_read(path, max_bytes) — Read file content safely, handling encoding errors. | count_pattern(text, pattern, case_insensitive) | find_slop_words(text) — Find banned AI slop words in text. Returns (word, count) pairs. | find_spam_words(text) — Find spam trigger words in text. | count_em_dashes(text) | main()
  cli: --score-all --score-apps --score-content --score-emails --score-listings --score-scripts --gate --report --api-json

### twitter_alpha_scraper.py (1014L) — scrapes 133 Twitter accounts via Brave cookies + Playwright
  class TwitterScraper: [__init__(deep, download_media, meme_mode, days), _load_alpha_fieldnames(), _load_copy_style_handles(), _parse_ts(ts), _load_existing_urls(), _get_next_alpha_id(), _is_signal_content(text), _categorize(text), _estimate_roi(tweet), save_to_csv(tweets, source_type)]
  fn: extract_brave_cookies(domain_filter) — Extract and decrypt cookies from Brave's cookie database.
  cli: --bookmarks --accounts --handles --all --meme --deep --download-media --limit --days --max-scrolls --visible

### background_reddit_scraper.py (278L) — Reddit JSON API scraper — no auth needed
  fn: load_subreddits(limit) — Load subreddits marked for auto-monitoring | get_next_alpha_id() — Get next available ALPHA ID | load_existing_urls() — Load existing URLs to avoid duplicates | estimate_roi(text, upvotes) — Estimate ROI potential | has_signal(title) — Check if title has business/alpha signal | scrape_subreddits(subreddits) — Scrape subreddits using Reddit JSON API - runs in background | main()
  cli: --scrape --full --limit

### compliance_scanner.py (511L) — FTC/platform compliance auditing
  class ComplianceIssue: [__init__(category, severity, file_path, line_num, text, rule, fix_suggestion), to_dict(), __str__()]
  class ComplianceScanner: [__init__(project_root), scan_file(file_path), scan_directory(dir_path, extensions), scan_content(), scan_emails(), audit_all(), generate_report(issues), save_report(issues, output_dir)]
  fn: main()
  cli: --scan-content --scan-emails --scan-file --audit-all --json --save

### memory_manager.py (464L) — filesystem-based memory management
  fn: count_csv(path) | count_files(pattern) | read_json(path) | file_age_hours(path) | safe_read_csv_column(path, col) | update_heartbeat() — Generate HEARTBEAT.md — the system pulse check. | update_active_tasks() — Refresh active-tasks.md with current system state. | log_to_daily(message) — Append a message to today's daily log. | generate_daily_summary() — Generate end-of-day summary from daily log entries. | check_venture_health() — Quick health check across all ventures. | main()
  cli: --heartbeat --active-tasks --daily-summary --log --health --full
  reads: ETSY_LISTINGS_COMPLETE.md, progress.json, ACCOUNTS.csv, REVENUE_TRACKER.csv

### wire_missed_intelligence.py (258L) — parses MISSED_INTELLIGENCE_SCAN.md → updates catalog
  fn: classify_path(path) — Classify a file path into a venture type. | parse_scan_file(scan_path) — Parse MISSED_INTELLIGENCE_SCAN.md and extract all file entries. | get_existing_paths(catalog) — Get all paths already in the catalog across all ventures. | main()

### build_codebase_grammar.py (342L) — LLM-optimized codebase representation — AST parsing, 100x+ compression
  fn: extract_script_grammar(script_path, description) — Extract a compact grammar representation of a Python script. | build_grammar() — Build the full codebase grammar. | render_markdown(grammar) — Render grammar as compact markdown for LLM consumption. | main()
  cli: --json --stats
