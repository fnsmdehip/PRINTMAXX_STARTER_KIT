#!/usr/bin/env python3
"""PRINTMAXX Automation System — streak_app_morning_routine_dag.py

Multi-phase daily DAG pipeline for the Morning Routine niche:

  Phase 1: Vibe-code streak app MVP scaffold with RevenueCat IAP + AdMob stubs
  Phase 2: Scrape ~580k morning routine community (Reddit / Twitter / YouTube)
  Phase 3: Generate engagement content from community signals
  Phase 4: Cold-email influencers in the morning routine niche
  Phase 5: Track cohort retention and install attribution

Run modes:
  --run       Execute the full DAG
  --status    Print last-run status from the state file
  --dry-run   Walk the DAG without performing external I/O

Cron example (daily at 06:00):
  0 6 * * * /usr/bin/env python3 /path/to/streak_app_morning_routine_dag.py --run
"""

import argparse
import csv
import json
import logging
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: import from _common when available; inline fallbacks otherwise.
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(*parts: str) -> Path:
        """Return an absolute path validated to reside inside PROJECT."""
        target = PROJECT.joinpath(*parts).resolve()
        if not str(target).startswith(str(PROJECT) + os.sep) and target != PROJECT:
            raise ValueError(f"Path escape attempt blocked: {target}")
        return target

    def recall_skills_for_task(task_name: str) -> list:  # noqa: ARG001
        return []

    def capture_skill_from_result(task_name: str, result: object) -> None:  # noqa: ARG001
        pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCRIPT_NAME = "streak_app_morning_routine_dag"

LOG_DIR  = safe_path("AUTOMATIONS", "logs")
LOG_FILE = safe_path("AUTOMATIONS", "logs", f"{SCRIPT_NAME}.log")

DATA_DIR       = safe_path("AUTOMATIONS", "data", SCRIPT_NAME)
STATE_FILE     = safe_path("AUTOMATIONS", "data", SCRIPT_NAME, "state.json")
INFLUENCER_CSV = safe_path("AUTOMATIONS", "data", SCRIPT_NAME, "influencers.csv")
SCRAPE_OUTPUT  = safe_path("AUTOMATIONS", "data", SCRIPT_NAME, "scraped_posts.json")
CONTENT_OUTPUT = safe_path("AUTOMATIONS", "data", SCRIPT_NAME, "generated_content.json")
COHORT_CSV     = safe_path("AUTOMATIONS", "data", SCRIPT_NAME, "cohort_retention.csv")
APP_SCAFFOLD_DIR = safe_path("AUTOMATIONS", "data", SCRIPT_NAME, "streak_app_scaffold")

REDDIT_SUBREDDITS = [
    "morningRoutine",
    "getdisciplined",
    "productivity",
    "selfimprovement",
]

YOUTUBE_SEARCH_TERMS = [
    "morning routine 2024",
    "morning habits productivity",
    "5am morning routine",
]

CONTENT_TEMPLATES = [
    "Hot take: {title} — agree or disagree? 🧵",
    "Steal this: {title} (we tested it for 30 days) 🔥",
    "Nobody talks about this morning habit: {title}",
    "If you only do ONE thing tomorrow: {title}",
    "Day {day} of documenting: {title}",
]

SEED_INFLUENCERS = [
    {"handle": "@morningbrewofficial", "platform": "twitter",   "niche": "morning newsletter", "email": ""},
    {"handle": "@robinsharmaleader",   "platform": "twitter",   "niche": "morning habits",     "email": ""},
    {"handle": "Robin Sharma",         "platform": "youtube",   "niche": "5am club",           "email": ""},
    {"handle": "Hal Elrod",            "platform": "youtube",   "niche": "miracle morning",    "email": ""},
    {"handle": "@levelupwithmel",      "platform": "instagram", "niche": "productivity",       "email": ""},
]


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(SCRIPT_NAME)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%dT%H:%M:%SZ")
    fh = logging.FileHandler(str(LOG_FILE), mode="a", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"last_run": None, "phases": {}, "errors": []}


def save_state(state: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, default=str), encoding="utf-8")


def stamp_phase(state: dict, phase: str, status: str, detail: str = "") -> None:
    state["phases"][phase] = {
        "status": status,
        "ts":     datetime.now(timezone.utc).isoformat(),
        "detail": detail,
    }


# ---------------------------------------------------------------------------
# HTTP helper (stdlib only)
# ---------------------------------------------------------------------------

def http_get(url: str, headers: dict | None = None, timeout: int = 15) -> dict | list | None:
    req = urllib.request.Request(
        url,
        headers=headers or {"User-Agent": "PRINTMAXX-MorningStreak/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError):
        return None


# ---------------------------------------------------------------------------
# Phase 1 — Streak App MVP scaffold (Flutter + RevenueCat + AdMob)
# ---------------------------------------------------------------------------

def phase_01_vibe_code_streak_app(state: dict, dry_run: bool, log: logging.Logger) -> bool:
    """Generate Flutter streak app MVP scaffold with RevenueCat IAP + AdMob stubs."""
    log.info("Phase 1: Generating streak app MVP scaffold …")
    recall_skills_for_task("streak_app_scaffold")

    files = {
        "pubspec.yaml":                          _flutter_pubspec(),
        "lib/main.dart":                         _flutter_main(),
        "lib/services/revenue_cat_service.dart": _revenue_cat_service(),
        "lib/services/admob_service.dart":       _admob_service(),
        "lib/screens/streak_screen.dart":        _streak_screen(),
        "README.md":                             _app_readme(),
    }

    if dry_run:
        for fname in files:
            log.info(f"  [dry-run] Would write: streak_app_scaffold/{fname}")
        stamp_phase(state, "phase_01", "dry_run")
        return True

    try:
        for rel_path, content in files.items():
            dest = safe_path(
                "AUTOMATIONS", "data", SCRIPT_NAME,
                "streak_app_scaffold", *rel_path.split("/"),
            )
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8")
            log.info(f"  Wrote {dest.relative_to(PROJECT)}")

        result = subprocess.run(
            ["find", str(APP_SCAFFOLD_DIR), "-type", "f"],
            capture_output=True, text=True, check=False,
        )
        file_count = len(result.stdout.strip().splitlines()) if result.returncode == 0 else len(files)
        capture_skill_from_result("streak_app_scaffold", files)
        stamp_phase(state, "phase_01", "ok", f"{file_count} files written to {APP_SCAFFOLD_DIR.name}/")
        log.info("Phase 1 complete.")
        return True
    except (OSError, ValueError) as exc:
        log.error(f"Phase 1 error: {exc}")
        stamp_phase(state, "phase_01", "error", str(exc))
        return False


def _flutter_pubspec() -> str:
    return """\
name: streak_app
description: Morning Routine Streak Tracker — PRINTMAXX MVP
version: 1.0.0+1

environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter
  purchases_flutter: ^6.0.0
  google_mobile_ads: ^4.0.0
  shared_preferences: ^2.2.0

flutter:
  uses-material-design: true
"""


def _flutter_main() -> str:
    return """\
import 'package:flutter/material.dart';
import 'services/revenue_cat_service.dart';
import 'services/admob_service.dart';
import 'screens/streak_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await RevenueCatService.init();
  await AdMobService.init();
  runApp(const StreakApp());
}

class StreakApp extends StatelessWidget {
  const StreakApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'Morning Streak',
        theme: ThemeData(colorSchemeSeed: Colors.amber, useMaterial3: true),
        home: const StreakScreen(),
      );
}
"""


def _revenue_cat_service() -> str:
    return """\
import 'package:purchases_flutter/purchases_flutter.dart';

class RevenueCatService {
  static const _apiKey = 'YOUR_REVENUECAT_API_KEY';

  static Future<void> init() async {
    await Purchases.setLogLevel(LogLevel.debug);
    await Purchases.configure(PurchasesConfiguration(_apiKey));
  }

  static Future<bool> purchasePremium() async {
    try {
      final offerings = await Purchases.getOfferings();
      final pkg = offerings.current?.monthly;
      if (pkg == null) return false;
      await Purchases.purchasePackage(pkg);
      return true;
    } catch (_) {
      return false;
    }
  }

  static Future<bool> isSubscribed() async {
    final info = await Purchases.getCustomerInfo();
    return info.entitlements.active.isNotEmpty;
  }
}
"""


def _admob_service() -> str:
    return """\
import 'package:google_mobile_ads/google_mobile_ads.dart';

class AdMobService {
  static const _bannerAdUnitId = 'ca-app-pub-XXXXXXXXXXXXXXXX/XXXXXXXXXX';
  static BannerAd? _banner;

  static Future<void> init() async {
    await MobileAds.instance.initialize();
  }

  static BannerAd loadBanner() {
    _banner = BannerAd(
      adUnitId: _bannerAdUnitId,
      size: AdSize.banner,
      request: const AdRequest(),
      listener: const BannerAdListener(),
    )..load();
    return _banner!;
  }
}
"""


def _streak_screen() -> str:
    return """\
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/revenue_cat_service.dart';
import '../services/admob_service.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

class StreakScreen extends StatefulWidget {
  const StreakScreen({super.key});

  @override
  State<StreakScreen> createState() => _StreakScreenState();
}

class _StreakScreenState extends State<StreakScreen> {
  int _streak = 0;
  bool _isPremium = false;
  BannerAd? _bannerAd;

  @override
  void initState() {
    super.initState();
    _loadStreak();
    _checkPremium();
  }

  Future<void> _loadStreak() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() => _streak = prefs.getInt('streak') ?? 0);
  }

  Future<void> _checkPremium() async {
    final sub = await RevenueCatService.isSubscribed();
    setState(() {
      _isPremium = sub;
      if (!sub) _bannerAd = AdMobService.loadBanner();
    });
  }

  Future<void> _checkIn() async {
    final prefs = await SharedPreferences.getInstance();
    final newStreak = _streak + 1;
    await prefs.setInt('streak', newStreak);
    setState(() => _streak = newStreak);
  }

  Future<void> _upgrade() async {
    await RevenueCatService.purchasePremium();
    await _checkPremium();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Morning Streak'),
        actions: [
          if (!_isPremium)
            TextButton(onPressed: _upgrade, child: const Text('Go Premium')),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(r'$_streak 🔥',
                      style: Theme.of(context).textTheme.displayLarge),
                  const SizedBox(height: 8),
                  Text('day streak',
                      style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 32),
                  FilledButton.icon(
                    onPressed: _checkIn,
                    icon: const Icon(Icons.check_circle_outline),
                    label: const Text('Check In Today'),
                  ),
                ],
              ),
            ),
          ),
          if (!_isPremium && _bannerAd != null)
            SizedBox(
              height: _bannerAd!.size.height.toDouble(),
              child: AdWidget(ad: _bannerAd!),
            ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _bannerAd?.dispose();
    super.dispose();
  }
}
"""


def _app_readme() -> str:
    return """\
# Morning Streak App — PRINTMAXX MVP

## Quick Start
1. Replace `YOUR_REVENUECAT_API_KEY` in `lib/services/revenue_cat_service.dart`
2. Replace the AdMob unit ID in `lib/services/admob_service.dart`
3. `flutter pub get && flutter run`

## Revenue Model
| Tier    | Mechanism                                           |
|---------|-----------------------------------------------------|
| Free    | AdMob banner ad at bottom of streak screen          |
| Premium | RevenueCat monthly subscription — removes ads,      |
|         | unlocks detailed stats                              |

## Attribution
Integrate AppsFlyer or Firebase Analytics for install attribution.
Feed data into the PRINTMAXX cohort CSV via the DAG Phase 5.
"""


# ---------------------------------------------------------------------------
# Phase 2 — Scrape morning routine community
# ---------------------------------------------------------------------------

def phase_02_scrape_community(state: dict, dry_run: bool, log: logging.Logger) -> bool:
    """Scrape Reddit public JSON feeds for top morning routine posts."""
    log.info("Phase 2: Scraping morning routine community …")

    if dry_run:
        log.info("  [dry-run] Would scrape subreddits: " + ", ".join(REDDIT_SUBREDDITS))
        stamp_phase(state, "phase_02", "dry_run")
        return True

    posts: list[dict] = []
    try:
        for sub in REDDIT_SUBREDDITS:
            url = f"https://www.reddit.com/r/{sub}/top.json?limit=25&t=week"
            data = http_get(url)
            if not data:
                log.warning(f"  Could not fetch r/{sub} — skipping")
                continue
            children = data.get("data", {}).get("children", [])
            for child in children:
                p = child.get("data", {})
                posts.append({
                    "source":       f"reddit:r/{sub}",
                    "id":           p.get("id"),
                    "title":        p.get("title", ""),
                    "url":          p.get("url", ""),
                    "score":        p.get("score", 0),
                    "num_comments": p.get("num_comments", 0),
                    "created_utc":  p.get("created_utc"),
                    "selftext":     (p.get("selftext") or "")[:500],
                })
            log.info(f"  r/{sub}: {len(children)} posts fetched")
            time.sleep(1)  # polite crawl delay

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        SCRAPE_OUTPUT.write_text(
            json.dumps(posts, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        log.info(f"  Saved {len(posts)} posts → {SCRAPE_OUTPUT.relative_to(PROJECT)}")
        stamp_phase(state, "phase_02", "ok", f"{len(posts)} posts scraped")
        return True
    except (OSError, ValueError) as exc:
        log.error(f"Phase 2 error: {exc}")
        stamp_phase(state, "phase_02", "error", str(exc))
        return False


# ---------------------------------------------------------------------------
# Phase 3 — Generate engagement content
# ---------------------------------------------------------------------------

def phase_03_generate_content(state: dict, dry_run: bool, log: logging.Logger) -> bool:
    """Derive social content angles from the scraped community data."""
    log.info("Phase 3: Generating engagement content …")

    if dry_run:
        log.info("  [dry-run] Would generate content pieces from scraped posts")
        stamp_phase(state, "phase_03", "dry_run")
        return True

    try:
        if not SCRAPE_OUTPUT.exists():
            log.warning("  No scrape output found — run phase 2 first")
            stamp_phase(state, "phase_03", "skipped", "no scrape output")
            return True

        posts = json.loads(SCRAPE_OUTPUT.read_text(encoding="utf-8"))

        # Rank by engagement proxy: score + 3× comment weight
        scored = sorted(
            posts,
            key=lambda p: p.get("score", 0) + p.get("num_comments", 0) * 3,
            reverse=True,
        )
        top_posts = scored[:10]

        channels = ["twitter", "instagram_reels", "tiktok"]
        content_items: list[dict] = []
        for i, post in enumerate(top_posts):
            tpl = CONTENT_TEMPLATES[i % len(CONTENT_TEMPLATES)]
            hook = tpl.format(title=post["title"][:80], day=i + 1)
            content_items.append({
                "hook":         hook,
                "source_url":   post.get("url", ""),
                "source_score": post.get("score", 0),
                "channel":      channels[i % len(channels)],
                "cta":          "Download Morning Streak — link in bio 📱",
            })

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        CONTENT_OUTPUT.write_text(
            json.dumps(content_items, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        log.info(
            f"  Generated {len(content_items)} pieces → {CONTENT_OUTPUT.relative_to(PROJECT)}"
        )
        stamp_phase(state, "phase_03", "ok", f"{len(content_items)} content items")
        return True
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        log.error(f"Phase 3 error: {exc}")
        stamp_phase(state, "phase_03", "error", str(exc))
        return False


# ---------------------------------------------------------------------------
# Phase 4 — Cold email influencers
# ---------------------------------------------------------------------------

_OUTREACH_SUBJECT = "Collab opportunity: Morning Streak App × {handle} 🌅"

_OUTREACH_BODY = """\
Hi {handle},

I'm the founder of Morning Streak — a streak-tracking app built for the morning routine community.

Your content around {niche} is exactly what our users love. Here is what we could explore:

  • Sponsored story / reel  ($500–$2,000 flat)
  • Affiliate revenue share (20 % recurring on every subscriber you bring in)
  • Co-created 30-day morning challenge

App: https://morningstreak.app  |  One-page deck: reply and I will send it over.

Would a quick 15-min intro call work this week?

Best,
The PRINTMAXX / Morning Streak Team"""


def phase_04_cold_email_influencers(state: dict, dry_run: bool, log: logging.Logger) -> bool:
    """Build the influencer outreach queue and append email drafts to CSV."""
    log.info("Phase 4: Cold email influencer outreach …")

    if dry_run:
        log.info(f"  [dry-run] Would queue {len(SEED_INFLUENCERS)} outreach emails")
        stamp_phase(state, "phase_04", "dry_run")
        return True

    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        write_header = not INFLUENCER_CSV.exists()
        fieldnames = ["date", "handle", "platform", "niche", "email", "subject", "body", "status"]
        today = datetime.now(timezone.utc).date().isoformat()

        with open(str(INFLUENCER_CSV), "a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            for inf in SEED_INFLUENCERS:
                writer.writerow({
                    "date":     today,
                    "handle":   inf["handle"],
                    "platform": inf["platform"],
                    "niche":    inf["niche"],
                    "email":    inf["email"],
                    "subject":  _OUTREACH_SUBJECT.format(handle=inf["handle"]),
                    "body":     _OUTREACH_BODY.format(
                                    handle=inf["handle"], niche=inf["niche"]),
                    "status":   "queued",
                })

        log.info(
            f"  Appended {len(SEED_INFLUENCERS)} rows → {INFLUENCER_CSV.relative_to(PROJECT)}"
        )
        stamp_phase(state, "phase_04", "ok", f"{len(SEED_INFLUENCERS)} influencers queued")
        return True
    except (OSError, ValueError) as exc:
        log.error(f"Phase 4 error: {exc}")
        stamp_phase(state, "phase_04", "error", str(exc))
        return False


# ---------------------------------------------------------------------------
# Phase 5 — Cohort retention & install attribution
# ---------------------------------------------------------------------------

def phase_05_track_cohort_retention(state: dict, dry_run: bool, log: logging.Logger) -> bool:
    """Log a cohort retention snapshot row (wire to RevenueCat / AppsFlyer for actuals)."""
    log.info("Phase 5: Tracking cohort retention and install attribution …")

    if dry_run:
        log.info("  [dry-run] Would append cohort retention row to CSV")
        stamp_phase(state, "phase_05", "dry_run")
        return True

    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        today = datetime.now(timezone.utc).date().isoformat()
        write_header = not COHORT_CSV.exists()

        # In production: pull actuals via RevenueCat REST API + AppsFlyer / Firebase.
        # Schema is established here; replace zeros with real metric fetches.
        row = {
            "date":              today,
            "cohort":            today,
            "installs_d0":       0,
            "retained_d1":       0,
            "retained_d7":       0,
            "retained_d30":      0,
            "iap_conversions":   0,
            "ad_revenue_usd":    0.0,
            "attributed_source": "organic",
            "notes":             "placeholder — wire RevenueCat + AppsFlyer webhooks",
        }

        with open(str(COHORT_CSV), "a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(row.keys()))
            if write_header:
                writer.writeheader()
            writer.writerow(row)

        log.info(f"  Cohort row appended → {COHORT_CSV.relative_to(PROJECT)}")
        stamp_phase(state, "phase_05", "ok", "cohort row written")
        return True
    except (OSError, ValueError) as exc:
        log.error(f"Phase 5 error: {exc}")
        stamp_phase(state, "phase_05", "error", str(exc))
        return False


# ---------------------------------------------------------------------------
# DAG runner
# ---------------------------------------------------------------------------

PHASES = [
    ("phase_01", phase_01_vibe_code_streak_app),
    ("phase_02", phase_02_scrape_community),
    ("phase_03", phase_03_generate_content),
    ("phase_04", phase_04_cold_email_influencers),
    ("phase_05", phase_05_track_cohort_retention),
]


def run_dag(dry_run: bool, log: logging.Logger) -> int:
    state = load_state()
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    failures = 0
    for phase_key, fn in PHASES:
        try:
            ok = fn(state, dry_run, log)
        except Exception as exc:  # noqa: BLE001
            log.exception(f"Uncaught exception in {phase_key}: {exc}")
            stamp_phase(state, phase_key, "error", str(exc))
            ok = False
        if not ok:
            failures += 1
            log.warning(f"  {phase_key} reported failure — continuing DAG")
        save_state(state)
    return failures


def print_status(log: logging.Logger) -> None:
    state = load_state()
    log.info("=== PRINTMAXX DAG Status ===")
    log.info(f"Last run : {state.get('last_run', 'never')}")
    phases = state.get("phases", {})
    if not phases:
        log.info("  No phases recorded yet.")
        return
    for phase, info in phases.items():
        log.info(
            f"  {phase}: [{info.get('status', '?'):8}]"
            f"  @ {info.get('ts', '')}  {info.get('detail', '')}"
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description="PRINTMAXX — Morning Routine streak app daily DAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Cron:  0 6 * * *  python3 streak_app_morning_routine_dag.py --run",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run",     action="store_true", help="Execute the full DAG")
    group.add_argument("--status",  action="store_true", help="Print last-run status")
    group.add_argument("--dry-run", dest="dry_run", action="store_true",
                       help="Walk the DAG without external I/O")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    log = setup_logging()
    log.info(f"PRINTMAXX {SCRIPT_NAME} started — pid={os.getpid()}")

    try:
        if args.status:
            print_status(log)
            sys.exit(0)

        dry_run = getattr(args, "dry_run", False)
        if dry_run:
            log.info("Dry-run mode — no external I/O will occur")

        failures = run_dag(dry_run=dry_run, log=log)

        if failures:
            log.warning(f"DAG finished with {failures} phase failure(s).")
            sys.exit(1)
        else:
            log.info("DAG completed successfully.")
            sys.exit(0)

    except KeyboardInterrupt:
        log.info("Interrupted — exiting cleanly.")
        sys.exit(130)
    except Exception as exc:  # noqa: BLE001
        log.exception(f"Unhandled error in main: {exc}")
        sys.exit(2)


if __name__ == "__main__":
    main()