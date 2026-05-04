#!/usr/bin/env python3
"""PRINTMAXX Clawdbot-Style RBI Growth Engine.

Purpose:
  - Convert distributed alpha into executable growth queues across channels.
  - Keep outputs safe-by-default: draft queues only, no auto-posting/submitting.
  - Compound learning by rewriting a local project skill file each run.

Inputs (best effort):
  - LEDGER/ALPHA_STAGING.csv
  - LEDGER/LAUNCH_DIRECTORIES_MASTER.csv
  - LEDGER/TELEGRAM_SIGNALS.csv
  - LEDGER/TRIGGERING_EVENTS.csv (optional)
  - AUTOMATIONS/alpha_monitor_output/reddit_scan_*.json
  - output/apps/manifest.json
  - output/native_apps/manifest.json
  - OPS/COPY_STYLE_HANDLES.txt

Outputs:
  - output/clawdbot/intents/reply_queue.csv
  - output/clawdbot/syndication/syndication_wave.csv
  - output/clawdbot/directories/submission_wave.csv
  - output/clawdbot/jobs/job_sniper_queue.csv
  - output/clawdbot/seo/keyword_gap_queue.csv
  - output/clawdbot/community/community_signal_queue.csv
  - output/clawdbot/latest.md
  - output/clawdbot/latest.html
  - output/clawdbot/manifest.json
  - OPS/skills/CLAWDBOT_RBI_SKILL.md
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, deque
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Deque, Dict, Iterable, List, Tuple


BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "LEDGER"
OPS = BASE / "OPS"
OUTPUT = BASE / "output" / "clawdbot"

ALPHA_CSV = LEDGER / "ALPHA_STAGING.csv"
LAUNCH_DIR_CSV = LEDGER / "LAUNCH_DIRECTORIES_MASTER.csv"
TELEGRAM_CSV = LEDGER / "TELEGRAM_SIGNALS.csv"
TRIGGER_CSV = LEDGER / "TRIGGERING_EVENTS.csv"
COPY_STYLE_HANDLES = OPS / "COPY_STYLE_HANDLES.txt"

APPS_MANIFEST = BASE / "output" / "apps" / "manifest.json"
NATIVE_APPS_MANIFEST = BASE / "output" / "native_apps" / "manifest.json"

REDDIT_SCAN_DIR = BASE / "AUTOMATIONS" / "alpha_monitor_output"

INTENTS_DIR = OUTPUT / "intents"
SYNDICATION_DIR = OUTPUT / "syndication"
DIRECTORIES_DIR = OUTPUT / "directories"
JOBS_DIR = OUTPUT / "jobs"
SEO_DIR = OUTPUT / "seo"
COMMUNITY_DIR = OUTPUT / "community"

INTENTS_CSV = INTENTS_DIR / "reply_queue.csv"
SYNDICATION_CSV = SYNDICATION_DIR / "syndication_wave.csv"
DIRECTORY_CSV = DIRECTORIES_DIR / "submission_wave.csv"
JOBS_CSV = JOBS_DIR / "job_sniper_queue.csv"
KEYWORD_CSV = SEO_DIR / "keyword_gap_queue.csv"
COMMUNITY_CSV = COMMUNITY_DIR / "community_signal_queue.csv"

LATEST_MD = OUTPUT / "latest.md"
LATEST_HTML = OUTPUT / "latest.html"
MANIFEST = OUTPUT / "manifest.json"
SKILL_FILE = OPS / "skills" / "CLAWDBOT_RBI_SKILL.md"

INTENT_PATTERNS = [
    r"\bneed(?:ing)?\b",
    r"\blooking for\b",
    r"\balternative to\b",
    r"\bbest tool\b",
    r"\bhow do i\b",
    r"\bany recommendation\b",
    r"\bstruggl(?:e|ing)\b",
    r"\bwhat should i use\b",
]

HIRING_PATTERNS = [
    r"\bhiring\b",
    r"\blooking for (?:a|an)\b",
    r"\bjob opening\b",
    r"\bheadcount\b",
    r"\bopen role\b",
]

SEO_PATTERNS = [
    r"\bseo\b",
    r"\bkeyword\b",
    r"\bserp\b",
    r"\brank(?:ing)?\b",
    r"\bgoogle\b",
    r"\bsearch\b",
    r"\baso\b",
]

HIGH_RISK_TERMS = [
    "fake account",
    "catfish",
    "ban evasion",
    "bypass platform",
    "evade detection",
    "exploit",
    "findom",
    "nsfw",
    "money laundering",
    "wire fraud",
    "identity theft",
]

PLATFORM_STYLES = {
    "linkedin": "operator insight, concise bullets",
    "medium": "long-form breakdown with examples",
    "substack": "founder newsletter voice",
    "quora": "answer-first with practical steps",
    "reddit": "value-first no hard sell",
    "dev.to": "technical implementation angle",
    "hashnode": "developer tutorial with code snippets",
    "indiehackers": "build-in-public metrics framing",
    "github": "readme/changelog style summary",
    "slideshare": "slide-outline concise framing",
    "x_thread": "hook + short punchy proofs",
    "tumblr": "casual narrative + visual cues",
    "wordpress": "evergreen SEO article structure",
    "flipboard": "curation summary + CTA",
    "scribd": "document summary with key takeaways",
}

PRIORITY_ORDER = {"HIGHEST": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_int(v: object, default: int = 0) -> int:
    try:
        return int(float(str(v).strip()))
    except Exception:
        return default


def read_csv_rows(path: Path, max_rows: int = 200000) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    rows: List[Dict[str, str]] = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                rows.append({k: (v or "").strip() for k, v in row.items()})
    except Exception:
        return []
    return rows


def tail_csv_rows(path: Path, max_rows: int) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    keep: Deque[Dict[str, str]] = deque(maxlen=max_rows)
    try:
        with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                keep.append({k: (v or "").strip() for k, v in row.items()})
    except Exception:
        return []
    return list(keep)


def write_csv_rows(path: Path, fieldnames: Iterable[str], rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in writer.fieldnames})


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def load_copy_style_handles() -> List[str]:
    if not COPY_STYLE_HANDLES.exists():
        return []
    handles: List[str] = []
    seen: set[str] = set()
    for raw in COPY_STYLE_HANDLES.read_text(encoding="utf-8", errors="replace").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        h = "@" + s.lstrip("@")
        key = h.lower()
        if key in seen:
            continue
        seen.add(key)
        handles.append(h)
    return handles


def normalize_text(text: str, max_len: int = 500) -> str:
    s = re.sub(r"\s+", " ", (text or "").strip())
    if len(s) <= max_len:
        return s
    return s[: max_len - 3].rstrip() + "..."


def text_from_alpha_row(row: Dict[str, str]) -> str:
    parts = [
        row.get("tactic", ""),
        row.get("extracted_method", ""),
        row.get("reviewer_notes", ""),
        row.get("compliance_notes", ""),
        row.get("source", ""),
    ]
    joined = " ".join([p for p in parts if p]).strip()
    return normalize_text(joined, 700)


def matches_any(text: str, patterns: List[str]) -> bool:
    s = (text or "").lower()
    for p in patterns:
        if re.search(p, s):
            return True
    return False


def risk_level_for_text(text: str) -> str:
    s = (text or "").lower()
    for term in HIGH_RISK_TERMS:
        if term in s:
            return "HIGH"
    if any(t in s for t in ["income claim", "guaranteed", "cease-and-desist"]):
        return "MEDIUM"
    return "LOW"


def is_recent_date(date_text: str, max_age_days: int = 180) -> bool:
    s = (date_text or "").strip()
    if not s:
        return True
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            d = datetime.strptime(s, fmt)
            return d >= (datetime.now() - timedelta(days=max_age_days))
        except Exception:
            continue
    return True


def choose_compare_set(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["seo", "keyword", "serp", "rank"]):
        return "Ahrefs|Semrush|GSC"
    if any(k in t for k in ["email", "outreach", "cold"]):
        return "Instantly|Smartlead|Apollo"
    if any(k in t for k in ["ecom", "shop", "listing", "etsy", "amazon"]):
        return "Etsy|eBay|Amazon"
    if any(k in t for k in ["saas", "app", "tool"]):
        return "Web app|iOS app|Chrome extension"
    return "Option A|Option B|PRINTMAXX"


def intent_reply_draft(pain: str, compare: str) -> str:
    return (
        f"Short answer: start with the smallest test that removes '{pain}'. "
        f"Compare {compare} on speed-to-value, cost, and integration overhead. "
        "If helpful, I can share a concrete setup checklist."
    )


def build_intent_queue(alpha_rows: List[Dict[str, str]], reddit_rows: List[Dict[str, Any]], max_items: int) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    seen: set[str] = set()
    ts = now_iso()

    for row in alpha_rows:
        text = text_from_alpha_row(row)
        if not text or not matches_any(text, INTENT_PATTERNS):
            continue
        source_url = row.get("source_url", "")
        dedupe_key = (source_url or text[:120]).lower()
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        pain = normalize_text(text, 140)
        risk = risk_level_for_text(text)
        if risk == "HIGH":
            continue
        compare = choose_compare_set(text)
        out.append(
            {
                "generated_at": ts,
                "intent_id": row.get("alpha_id", ""),
                "source": row.get("source", "alpha"),
                "source_url": source_url,
                "channel": "alpha",
                "signal_text": pain,
                "compare_set": compare,
                "draft_reply": intent_reply_draft(pain, compare),
                "disclosure_line": "Disclosure: affiliated with PRINTMAXX.",
                "risk_level": risk,
                "status": "DRAFT_ONLY",
            }
        )
        if len(out) >= max_items:
            return out

    for item in reddit_rows:
        title = normalize_text(str(item.get("title", "")), 180)
        body = normalize_text(str(item.get("selftext", "")), 350)
        text = f"{title} {body}".strip()
        if not text or not matches_any(text, INTENT_PATTERNS):
            continue
        source_url = str(item.get("url", "")).strip()
        dedupe_key = (source_url or text[:120]).lower()
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        compare = choose_compare_set(text)
        risk = risk_level_for_text(text)
        if risk == "HIGH":
            continue
        out.append(
            {
                "generated_at": ts,
                "intent_id": "",
                "source": f"r/{item.get('subreddit', '')}",
                "source_url": source_url,
                "channel": "reddit",
                "signal_text": title,
                "compare_set": compare,
                "draft_reply": intent_reply_draft(title, compare),
                "disclosure_line": "Disclosure: affiliated with PRINTMAXX.",
                "risk_level": risk,
                "status": "DRAFT_ONLY",
            }
        )
        if len(out) >= max_items:
            break

    return out


def load_reddit_scan_rows(max_files: int = 4, max_rows: int = 600) -> List[Dict[str, Any]]:
    files = sorted(REDDIT_SCAN_DIR.glob("reddit_scan_*.json"))
    if not files:
        return []
    selected = files[-max_files:]
    rows: List[Dict[str, Any]] = []
    for p in selected:
        try:
            payload = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        if not isinstance(payload, list):
            continue
        for item in payload:
            if not isinstance(item, dict):
                continue
            rows.append(item)
            if len(rows) >= max_rows:
                return rows
    return rows


def topic_from_signal(text: str) -> str:
    s = (text or "").strip().lower()
    s = re.sub(r"https?://\S+", "", s)
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    if not s:
        return "growth automation system"
    words = [w for w in s.split() if len(w) > 2][:8]
    return " ".join(words) if words else "growth automation system"


def build_syndication_wave(intent_rows: List[Dict[str, Any]], max_rows: int) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    seen_topics: set[str] = set()
    topics: List[str] = []
    for item in intent_rows:
        topic = topic_from_signal(str(item.get("signal_text", "")))
        if topic in seen_topics:
            continue
        seen_topics.add(topic)
        topics.append(topic)
        if len(topics) >= 60:
            break

    if not topics:
        topics = [
            "cold outreach conversion systems",
            "zero budget marketplace launch process",
            "micro saas validation with distribution first",
            "job posting intent based b2b prospecting",
        ]

    day_offset = 0
    idx = 1
    for topic in topics:
        for platform, style in PLATFORM_STYLES.items():
            out.append(
                {
                    "generated_at": now_iso(),
                    "wave_id": f"WAVE{idx:04d}",
                    "topic": topic,
                    "platform": platform,
                    "style_profile": style,
                    "backlink_target": "PRINTMAXX core hub page",
                    "day_offset": day_offset % 21,
                    "status": "DRAFT_ONLY",
                }
            )
            idx += 1
            day_offset += 1
            if len(out) >= max_rows:
                return out
    return out


def load_launch_products() -> List[Dict[str, str]]:
    products: List[Dict[str, str]] = []
    apps = load_json(APPS_MANIFEST)
    a_items = apps.get("items") if isinstance(apps.get("items"), list) else []
    for it in a_items:
        if not isinstance(it, dict):
            continue
        app_id = str(it.get("app_id", "")).strip()
        if not app_id:
            continue
        products.append(
            {
                "product_id": app_id,
                "product_name": str(it.get("title") or app_id).strip() or app_id,
                "product_type": "web_app",
            }
        )

    native = load_json(NATIVE_APPS_MANIFEST)
    n_items = native.get("items") if isinstance(native.get("items"), list) else []
    for it in n_items:
        if not isinstance(it, dict):
            continue
        app_id = str(it.get("app_id", "")).strip()
        if not app_id:
            continue
        products.append(
            {
                "product_id": f"native-{app_id}",
                "product_name": app_id,
                "product_type": "native_app",
            }
        )

    if not products:
        products.append(
            {
                "product_id": "printmaxx-digital-bundle",
                "product_name": "PRINTMAXX Digital Bundle",
                "product_type": "digital_product",
            }
        )
    return products


def build_directory_wave(max_rows: int) -> List[Dict[str, Any]]:
    dirs = read_csv_rows(LAUNCH_DIR_CSV, max_rows=2000)
    active = [d for d in dirs if (d.get("status", "").upper() == "ACTIVE")]
    active.sort(key=lambda d: (PRIORITY_ORDER.get((d.get("priority") or "").upper(), 9), d.get("directory_name", "")))

    products = load_launch_products()
    rows: List[Dict[str, Any]] = []
    i = 1
    for p in products:
        for d in active:
            rows.append(
                {
                    "generated_at": now_iso(),
                    "submission_id": f"SUB{i:05d}",
                    "product_id": p.get("product_id", ""),
                    "product_name": p.get("product_name", ""),
                    "product_type": p.get("product_type", ""),
                    "directory_id": d.get("directory_id", ""),
                    "directory_name": d.get("directory_name", ""),
                    "directory_url": d.get("url", ""),
                    "priority": (d.get("priority") or "").upper(),
                    "day_offset": (i - 1) % 21,
                    "status": "PENDING_SUBMISSION",
                    "next_action": "human submit with payload variant",
                }
            )
            i += 1
            if len(rows) >= max_rows:
                return rows
    return rows


def extract_company(text: str) -> str:
    s = text.strip()
    m = re.search(r"\b(?:at|for)\s+([A-Z][A-Za-z0-9&.\- ]{2,50})", s)
    if m:
        return m.group(1).strip()
    m2 = re.search(r"\b([A-Z][A-Za-z0-9&.\-]{2,})\b", s)
    if m2:
        return m2.group(1).strip()
    return "Unknown"


def build_job_sniper_queue(alpha_rows: List[Dict[str, str]], max_rows: int) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    ts = now_iso()
    i = 1

    trigger_rows = read_csv_rows(TRIGGER_CSV, max_rows=5000)
    for row in trigger_rows:
        detail = normalize_text(row.get("detail", ""), 220)
        company = row.get("company", "") or extract_company(detail)
        out.append(
            {
                "generated_at": ts,
                "signal_id": f"JOB{i:05d}",
                "company": company,
                "signal_source": row.get("event_type", "trigger"),
                "signal_detail": detail,
                "source_url": row.get("url", ""),
                "pitch_draft": (
                    f"Saw a hiring signal at {company}. "
                    "Before adding fixed headcount, we can pilot an AI-assisted workflow in 7 days."
                ),
                "status": "DRAFT_ONLY",
            }
        )
        i += 1
        if len(out) >= max_rows:
            return out

    for row in alpha_rows:
        text = text_from_alpha_row(row)
        if not matches_any(text, HIRING_PATTERNS):
            continue
        company = extract_company(text)
        out.append(
            {
                "generated_at": ts,
                "signal_id": f"JOB{i:05d}",
                "company": company,
                "signal_source": row.get("source", "alpha"),
                "signal_detail": normalize_text(text, 220),
                "source_url": row.get("source_url", ""),
                "pitch_draft": (
                    f"Saw your team is hiring for workflow-heavy roles. "
                    f"{company} can test a lower-risk automation pilot before full hiring."
                ),
                "status": "DRAFT_ONLY",
            }
        )
        i += 1
        if len(out) >= max_rows:
            break
    return out


def extract_keyword_candidates(alpha_rows: List[Dict[str, str]]) -> List[str]:
    kws: List[str] = []
    for row in alpha_rows:
        text = text_from_alpha_row(row)
        category = (row.get("category") or "").upper()
        if category != "SEO_GEO_ASO" and not matches_any(text, SEO_PATTERNS):
            continue

        for m in re.finditer(r"['\"]([a-zA-Z0-9][a-zA-Z0-9 \-]{3,50})['\"]", text):
            candidate = re.sub(r"\s+", " ", m.group(1)).strip().lower()
            if 3 <= len(candidate) <= 60:
                kws.append(candidate)
        for m in re.finditer(r"\b(?:keyword|query|term)\s*[:\-]\s*([a-zA-Z0-9][a-zA-Z0-9 \-]{3,50})", text, re.IGNORECASE):
            candidate = re.sub(r"\s+", " ", m.group(1)).strip().lower()
            if 3 <= len(candidate) <= 60:
                kws.append(candidate)
    return kws


def build_keyword_gap_queue(alpha_rows: List[Dict[str, str]], max_rows: int) -> List[Dict[str, Any]]:
    seed_niches = [
        "cold email automation",
        "website redesign service",
        "freelance proposal automation",
        "product listing automation",
        "micro saas launch",
        "ai content distribution",
        "sam gov opportunity monitor",
    ]
    modifiers = [
        "best",
        "for small business",
        "template",
        "pricing",
        "alternative",
        "checklist",
        "workflow",
    ]
    out: List[Dict[str, Any]] = []
    seen: set[str] = set()
    idx = 1

    extracted = extract_keyword_candidates(alpha_rows)
    queue = extracted[:]
    for niche in seed_niches:
        for m in modifiers:
            queue.append(f"{niche} {m}")

    for kw in queue:
        keyword = re.sub(r"\s+", " ", kw).strip().lower()
        if not keyword or keyword in seen:
            continue
        seen.add(keyword)
        intent_stage = "BOFU" if any(x in keyword for x in ["pricing", "alternative", "best"]) else "MOFU"
        out.append(
            {
                "generated_at": now_iso(),
                "keyword_id": f"KW{idx:05d}",
                "keyword": keyword,
                "intent_stage": intent_stage,
                "suggested_asset": "comparison page" if intent_stage == "BOFU" else "how-to article",
                "distribution_target": "site + medium + dev community mirrors",
                "status": "DRAFT_ONLY",
            }
        )
        idx += 1
        if len(out) >= max_rows:
            break

    return out


def build_community_signal_queue(telegram_rows: List[Dict[str, str]], reddit_rows: List[Dict[str, Any]], max_rows: int) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    ts = now_iso()
    idx = 1

    # Telegram signals first (if reasonably scored)
    for row in telegram_rows:
        if not is_recent_date(row.get("date", ""), max_age_days=180):
            continue
        score = safe_int(row.get("score"), 0)
        if score < 60:
            continue
        text = normalize_text(row.get("text", ""), 220)
        if not text:
            continue
        risk = risk_level_for_text(text)
        if risk == "HIGH":
            continue
        out.append(
            {
                "generated_at": ts,
                "signal_id": f"COM{idx:05d}",
                "source": row.get("channel", ""),
                "community": row.get("niche", ""),
                "signal_text": text,
                "suggested_response": (
                    "Useful context. If helpful, I can share the exact implementation steps and trade-offs."
                ),
                "disclosure_line": "Disclosure: affiliated with PRINTMAXX.",
                "risk_level": risk,
                "status": "DRAFT_ONLY",
            }
        )
        idx += 1
        if len(out) >= max_rows:
            return out

    # Then Reddit question-style posts
    for item in reddit_rows:
        title = normalize_text(str(item.get("title", "")), 180)
        body = normalize_text(str(item.get("selftext", "")), 220)
        if "?" not in title and not matches_any(title + " " + body, INTENT_PATTERNS):
            continue
        risk = risk_level_for_text(title + " " + body)
        if risk == "HIGH":
            continue
        out.append(
            {
                "generated_at": ts,
                "signal_id": f"COM{idx:05d}",
                "source": str(item.get("url", "")),
                "community": f"r/{item.get('subreddit', '')}",
                "signal_text": title,
                "suggested_response": (
                    "If you want, I can break this into a simple playbook with cost, setup time, and expected outcomes."
                ),
                "disclosure_line": "Disclosure: affiliated with PRINTMAXX.",
                "risk_level": risk,
                "status": "DRAFT_ONLY",
            }
        )
        idx += 1
        if len(out) >= max_rows:
            break
    return out


def write_skill_file(intent_rows: List[Dict[str, Any]], handles: List[str]) -> None:
    SKILL_FILE.parent.mkdir(parents=True, exist_ok=True)
    top_signals = [normalize_text(str(r.get("signal_text", "")), 120) for r in intent_rows[:12]]
    top_signals = [t for t in top_signals if t]
    lines: List[str] = []
    lines.append("# CLAWDBOT RBI Skill (Project Local)")
    lines.append("")
    lines.append(f"Updated: {now_iso()}")
    lines.append("")
    lines.append("## Mission")
    lines.append("- Convert high-intent market signals into compliant, execution-ready queue items.")
    lines.append("- Keep everything draft-first until explicit account/payment/compliance approval gates are open.")
    lines.append("")
    lines.append("## Non-Negotiables")
    lines.append("- No auto posting, no auto form submission, no auto DMs in this workflow.")
    lines.append("- Always include disclosure line in outreach/reply drafts.")
    lines.append("- Favor value-first language over hype claims.")
    lines.append("")
    lines.append("## Copy-Style Inputs")
    if handles:
        for h in handles:
            lines.append(f"- {h}")
    else:
        lines.append("- none configured")
    lines.append("")
    lines.append("## Current High-Signal Prompts")
    if top_signals:
        for t in top_signals:
            lines.append(f"- {t}")
    else:
        lines.append("- No high-signal prompts captured this run.")
    lines.append("")
    lines.append("## Reply Formula")
    lines.append("- Acknowledge context in one sentence.")
    lines.append("- Offer 2-3 comparison options.")
    lines.append("- Give one practical next step.")
    lines.append("- Include disclosure.")
    lines.append("")
    lines.append("## Iteration Rule")
    lines.append("- Move items from DRAFT_ONLY to approved lanes only after explicit queue clearance.")
    lines.append("")
    SKILL_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_latest_md(
    intent_rows: List[Dict[str, Any]],
    syndication_rows: List[Dict[str, Any]],
    directory_rows: List[Dict[str, Any]],
    job_rows: List[Dict[str, Any]],
    keyword_rows: List[Dict[str, Any]],
    community_rows: List[Dict[str, Any]],
) -> str:
    by_channel = Counter((r.get("channel") or "unknown") for r in intent_rows)
    lines: List[str] = []
    lines.append("# PRINTMAXX Clawdbot-Style RBI Engine")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append("## Queue Counts")
    lines.append(f"- Intent replies: {len(intent_rows)}")
    lines.append(f"- Syndication wave rows: {len(syndication_rows)}")
    lines.append(f"- Directory submission rows: {len(directory_rows)}")
    lines.append(f"- Job-sniper rows: {len(job_rows)}")
    lines.append(f"- Keyword-gap rows: {len(keyword_rows)}")
    lines.append(f"- Community signal rows: {len(community_rows)}")
    lines.append("")
    lines.append("## Intent Sources")
    for ch, c in sorted(by_channel.items()):
        lines.append(f"- {ch}: {c}")
    if not by_channel:
        lines.append("- none")
    lines.append("")
    lines.append("## Output Files")
    lines.append(f"- {INTENTS_CSV}")
    lines.append(f"- {SYNDICATION_CSV}")
    lines.append(f"- {DIRECTORY_CSV}")
    lines.append(f"- {JOBS_CSV}")
    lines.append(f"- {KEYWORD_CSV}")
    lines.append(f"- {COMMUNITY_CSV}")
    lines.append(f"- {SKILL_FILE}")
    lines.append("")
    lines.append("## Guardrails")
    lines.append("- Draft queues only. No auto posting/submitting from this engine.")
    lines.append("- Human approvals still gate live sends, listings, deploys, and payment actions.")
    lines.append("")
    lines.append("## Top Intent Signals")
    for row in intent_rows[:12]:
        lines.append(f"- {row.get('signal_text', '')}")
    if not intent_rows:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_latest_html(md_text: str) -> None:
    esc = md_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>PRINTMAXX Clawdbot RBI</title>
  <style>
    body {{ margin: 0; background: #0b0b0b; color: #eaeaea; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }}
    .wrap {{ max-width: 1120px; margin: 0 auto; padding: 20px; }}
    pre {{ white-space: pre-wrap; line-height: 1.45; font-size: 13px; }}
  </style>
</head>
<body>
  <div class="wrap"><pre>{esc}</pre></div>
</body>
</html>
"""
    LATEST_HTML.write_text(html, encoding="utf-8")


def write_manifest(
    intent_rows: List[Dict[str, Any]],
    syndication_rows: List[Dict[str, Any]],
    directory_rows: List[Dict[str, Any]],
    job_rows: List[Dict[str, Any]],
    keyword_rows: List[Dict[str, Any]],
    community_rows: List[Dict[str, Any]],
    handles: List[str],
) -> None:
    payload = {
        "generated_at": now_iso(),
        "counts": {
            "intent_rows": len(intent_rows),
            "syndication_rows": len(syndication_rows),
            "directory_rows": len(directory_rows),
            "job_rows": len(job_rows),
            "keyword_rows": len(keyword_rows),
            "community_rows": len(community_rows),
        },
        "sources": {
            "alpha_csv": str(ALPHA_CSV),
            "launch_directories_csv": str(LAUNCH_DIR_CSV),
            "telegram_csv": str(TELEGRAM_CSV),
            "trigger_csv": str(TRIGGER_CSV),
        },
        "outputs": {
            "intent_queue_csv": str(INTENTS_CSV),
            "syndication_wave_csv": str(SYNDICATION_CSV),
            "directory_wave_csv": str(DIRECTORY_CSV),
            "job_sniper_csv": str(JOBS_CSV),
            "keyword_gap_csv": str(KEYWORD_CSV),
            "community_queue_csv": str(COMMUNITY_CSV),
            "latest_md": str(LATEST_MD),
            "latest_html": str(LATEST_HTML),
            "skill_file": str(SKILL_FILE),
        },
        "copy_style_handles": handles,
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def run_tick(
    *,
    max_intents: int,
    max_syndication: int,
    max_directories: int,
    max_jobs: int,
    max_keywords: int,
    max_community: int,
) -> Dict[str, Any]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    INTENTS_DIR.mkdir(parents=True, exist_ok=True)
    SYNDICATION_DIR.mkdir(parents=True, exist_ok=True)
    DIRECTORIES_DIR.mkdir(parents=True, exist_ok=True)
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    SEO_DIR.mkdir(parents=True, exist_ok=True)
    COMMUNITY_DIR.mkdir(parents=True, exist_ok=True)

    alpha_rows = tail_csv_rows(ALPHA_CSV, max_rows=18000)
    telegram_rows = tail_csv_rows(TELEGRAM_CSV, max_rows=5000)
    reddit_rows = load_reddit_scan_rows(max_files=4, max_rows=800)
    handles = load_copy_style_handles()

    intent_rows = build_intent_queue(alpha_rows, reddit_rows, max_items=max_intents)
    syndication_rows = build_syndication_wave(intent_rows, max_rows=max_syndication)
    directory_rows = build_directory_wave(max_rows=max_directories)
    job_rows = build_job_sniper_queue(alpha_rows, max_rows=max_jobs)
    keyword_rows = build_keyword_gap_queue(alpha_rows, max_rows=max_keywords)
    community_rows = build_community_signal_queue(telegram_rows, reddit_rows, max_rows=max_community)

    write_csv_rows(
        INTENTS_CSV,
        [
            "generated_at",
            "intent_id",
            "source",
            "source_url",
            "channel",
            "signal_text",
            "compare_set",
            "draft_reply",
            "disclosure_line",
            "risk_level",
            "status",
        ],
        intent_rows,
    )
    write_csv_rows(
        SYNDICATION_CSV,
        [
            "generated_at",
            "wave_id",
            "topic",
            "platform",
            "style_profile",
            "backlink_target",
            "day_offset",
            "status",
        ],
        syndication_rows,
    )
    write_csv_rows(
        DIRECTORY_CSV,
        [
            "generated_at",
            "submission_id",
            "product_id",
            "product_name",
            "product_type",
            "directory_id",
            "directory_name",
            "directory_url",
            "priority",
            "day_offset",
            "status",
            "next_action",
        ],
        directory_rows,
    )
    write_csv_rows(
        JOBS_CSV,
        [
            "generated_at",
            "signal_id",
            "company",
            "signal_source",
            "signal_detail",
            "source_url",
            "pitch_draft",
            "status",
        ],
        job_rows,
    )
    write_csv_rows(
        KEYWORD_CSV,
        [
            "generated_at",
            "keyword_id",
            "keyword",
            "intent_stage",
            "suggested_asset",
            "distribution_target",
            "status",
        ],
        keyword_rows,
    )
    write_csv_rows(
        COMMUNITY_CSV,
        [
            "generated_at",
            "signal_id",
            "source",
            "community",
            "signal_text",
            "suggested_response",
            "disclosure_line",
            "risk_level",
            "status",
        ],
        community_rows,
    )

    write_skill_file(intent_rows, handles)
    md = render_latest_md(intent_rows, syndication_rows, directory_rows, job_rows, keyword_rows, community_rows)
    LATEST_MD.write_text(md, encoding="utf-8")
    write_latest_html(md)
    write_manifest(intent_rows, syndication_rows, directory_rows, job_rows, keyword_rows, community_rows, handles)

    return {
        "intent_rows": len(intent_rows),
        "syndication_rows": len(syndication_rows),
        "directory_rows": len(directory_rows),
        "job_rows": len(job_rows),
        "keyword_rows": len(keyword_rows),
        "community_rows": len(community_rows),
        "manifest": str(MANIFEST),
    }


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="PRINTMAXX clawdbot-style RBI growth engine (safe draft mode)")
    ap.add_argument("--tick", action="store_true", help="Run one generation tick")
    ap.add_argument("--max-intents", type=int, default=180, help="Max rows in intent queue")
    ap.add_argument("--max-syndication", type=int, default=420, help="Max rows in syndication wave")
    ap.add_argument("--max-directories", type=int, default=900, help="Max rows in directory submission wave")
    ap.add_argument("--max-jobs", type=int, default=200, help="Max rows in job sniper queue")
    ap.add_argument("--max-keywords", type=int, default=260, help="Max rows in keyword gap queue")
    ap.add_argument("--max-community", type=int, default=180, help="Max rows in community queue")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    if not args.tick:
        print("Use --tick to run one safe generation cycle.")
        return 2

    result = run_tick(
        max_intents=max(1, int(args.max_intents)),
        max_syndication=max(1, int(args.max_syndication)),
        max_directories=max(1, int(args.max_directories)),
        max_jobs=max(1, int(args.max_jobs)),
        max_keywords=max(1, int(args.max_keywords)),
        max_community=max(1, int(args.max_community)),
    )
    print(
        "clawdbot_rbi_engine: "
        + f"intent={result['intent_rows']} "
        + f"syndication={result['syndication_rows']} "
        + f"directories={result['directory_rows']} "
        + f"jobs={result['job_rows']} "
        + f"keywords={result['keyword_rows']} "
        + f"community={result['community_rows']} "
        + f"manifest={result['manifest']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
