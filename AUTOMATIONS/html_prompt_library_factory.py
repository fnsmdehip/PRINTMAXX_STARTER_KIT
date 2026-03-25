#!/usr/bin/env python3
"""
html_prompt_library_factory.py

PRINTMAXX automation: generates 150 niche-specific AI prompts via `claude -p`,
wraps them in a searchable/filterable single-file HTML app, and outputs a
ready-to-sell .html file for Gumroad at $17/product.

Runs weekly (via cron) to saturate niches: freelancers, solopreneurs,
marketers, devs, designers, coaches.

Usage:
    python html_prompt_library_factory.py --run --niche freelancers --roles copywriter strategist
    python html_prompt_library_factory.py --dry-run --niche devs --roles consultant
    python html_prompt_library_factory.py --status
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path):
        resolved = Path(path).resolve()
        if not str(resolved).startswith(str(PROJECT)):
            raise ValueError(f"Path {resolved} is outside PROJECT root {PROJECT}")
        return resolved

    def recall_skills_for_task(task):
        return []

    def capture_skill_from_result(result, task):
        pass

# --- Constants ---
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_FILE = AUTOMATIONS_DIR / "logs" / "html_prompt_library_factory.log"
OUTPUT_DIR = AUTOMATIONS_DIR / "output" / "prompt_libraries"
STATUS_FILE = AUTOMATIONS_DIR / "logs" / "html_prompt_library_factory_status.json"

PROMPTS_PER_CATEGORY = 15
NUM_CATEGORIES = 10
TOTAL_PROMPTS = PROMPTS_PER_CATEGORY * NUM_CATEGORIES  # 150


# --- Logging ---
def setup_logging():
    log_path = safe_path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(str(log_path), mode="a"),
            logging.StreamHandler(sys.stdout),
        ],
    )


# --- Claude CLI ---
def call_claude(prompt_text, dry_run=False):
    """Invoke `claude -p` and return stdout, or None on failure."""
    if dry_run:
        logging.info("[DRY RUN] claude -p call skipped: %s", prompt_text[:80])
        return "__DRY_RUN__"
    try:
        result = subprocess.run(
            ["claude", "-p", prompt_text],
            capture_output=True,
            text=True,
            timeout=180,
        )
        if result.returncode != 0:
            logging.error("claude -p exited %d: %s", result.returncode, result.stderr[:200])
            return None
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        logging.error("claude -p timed out after 180s")
        return None
    except FileNotFoundError:
        logging.error("'claude' not found in PATH — install Claude CLI first")
        return None
    except Exception as exc:
        logging.error("Unexpected subprocess error: %s", exc)
        return None


def _strip_code_fence(text):
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:]) if len(lines) > 1 else ""
        if text.endswith("```"):
            text = text[:-3].rstrip()
    return text


# --- Prompt Generation ---
def fetch_categories(niche, role, dry_run=False):
    """Ask Claude to return NUM_CATEGORIES category names as a JSON array."""
    prompt = (
        f"Generate exactly {NUM_CATEGORIES} distinct, practical prompt categories for an AI prompt library "
        f"targeting {niche} who work as {role}s.\n\n"
        "Cover varied aspects of their work (e.g. client communication, content creation, strategy, "
        "productivity, marketing, pricing, personal branding, analytics, outreach, mindset).\n\n"
        f"Return ONLY a JSON array of exactly {NUM_CATEGORIES} short category name strings. "
        "No extra text, no code fences."
    )
    logging.info("Fetching %d categories for niche='%s' role='%s'", NUM_CATEGORIES, niche, role)
    raw = call_claude(prompt, dry_run=dry_run)
    if raw is None:
        return None
    if raw == "__DRY_RUN__":
        return [
            "Content Creation", "Client Communication", "Marketing Strategy",
            "Productivity & Focus", "Email & Outreach", "Social Media",
            "Pricing & Proposals", "Business Development", "Personal Branding",
            "Analytics & Reporting",
        ]
    try:
        cats = json.loads(_strip_code_fence(raw))
        if isinstance(cats, list) and len(cats) >= NUM_CATEGORIES:
            return [str(c) for c in cats[:NUM_CATEGORIES]]
        logging.error("Categories response wrong shape: %s", raw[:200])
        return None
    except json.JSONDecodeError as exc:
        logging.error("JSON parse error for categories: %s\nRaw: %s", exc, raw[:300])
        return None


def fetch_prompts_for_category(niche, role, category, dry_run=False):
    """Ask Claude to return PROMPTS_PER_CATEGORY prompts as a JSON array."""
    prompt = (
        f"You are an expert prompt engineer creating a prompt library for {niche} who work as {role}s.\n\n"
        f"Generate exactly {PROMPTS_PER_CATEGORY} high-quality, immediately actionable AI prompts "
        f"for the category: '{category}'.\n\n"
        "Requirements:\n"
        f"- Tailor every prompt specifically to {niche} and {role} context\n"
        "- Each prompt must be ready to paste into ChatGPT/Claude and return useful output\n"
        "- Include clear placeholders like [YOUR_TOPIC], [TARGET_AUDIENCE], [YOUR_NICHE] where helpful\n"
        "- Vary difficulty across beginner / intermediate / advanced\n\n"
        'Return ONLY a JSON array of objects with fields: "title" (short string), '
        '"prompt" (full prompt text), "use_case" (one-line description), '
        '"difficulty" (beginner|intermediate|advanced). No extra text.'
    )
    logging.info("  Fetching %d prompts for category: '%s'", PROMPTS_PER_CATEGORY, category)
    raw = call_claude(prompt, dry_run=dry_run)
    if raw is None:
        return []
    if raw == "__DRY_RUN__":
        return [
            {
                "title": f"{category} Prompt {i + 1}",
                "prompt": (
                    f"Act as an expert {role} for {niche}. Help me with [YOUR_TOPIC] "
                    f"in the context of {category}. Provide step-by-step guidance, "
                    "specific examples, and actionable next steps tailored to [TARGET_AUDIENCE]."
                ),
                "use_case": f"Sample use case #{i + 1} for {category}",
                "difficulty": ("beginner", "intermediate", "advanced")[i % 3],
                "category": category,
            }
            for i in range(PROMPTS_PER_CATEGORY)
        ]
    try:
        items = json.loads(_strip_code_fence(raw))
        if not isinstance(items, list):
            logging.error("Expected list for '%s', got %s", category, type(items).__name__)
            return []
        for item in items:
            item["category"] = category
            item.setdefault("difficulty", "intermediate")
        return items
    except json.JSONDecodeError as exc:
        logging.error("JSON parse error for '%s': %s\nRaw: %s", category, exc, raw[:300])
        return []


def generate_all_prompts(niche, role, dry_run=False):
    """Orchestrate full generation: categories → prompts. Returns dict or None."""
    categories = fetch_categories(niche, role, dry_run=dry_run)
    if not categories:
        logging.error("Aborting: could not retrieve categories.")
        return None

    logging.info("Categories: %s", categories)
    all_prompts = []
    for idx, category in enumerate(categories, 1):
        logging.info("Category %d/%d: %s", idx, len(categories), category)
        prompts = fetch_prompts_for_category(niche, role, category, dry_run=dry_run)
        all_prompts.extend(prompts)
        logging.info("  +%d prompts (total: %d)", len(prompts), len(all_prompts))

    logging.info("Generation complete. Total prompts: %d", len(all_prompts))
    return {"categories": categories, "prompts": all_prompts}


# --- HTML Template ---
_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
:root{{--p:#6c63ff;--pd:#5a52d5;--bg:#f8f9fe;--cb:#fff;--tx:#2d2d3a;--mu:#6b7280;--bd:#e5e7eb;--tb:#ede9fe;--tt:#6c63ff;--ok:#10b981;--r:12px}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--tx);min-height:100vh}}
header{{background:linear-gradient(135deg,var(--p) 0%,#a78bfa 100%);color:#fff;padding:48px 24px 64px;text-align:center}}
header h1{{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;margin-bottom:12px}}
header p{{font-size:1.1rem;opacity:.9;max-width:620px;margin:0 auto}}
.badge{{display:inline-block;background:rgba(255,255,255,.2);padding:4px 14px;border-radius:999px;font-size:.85rem;font-weight:600;margin-bottom:16px;backdrop-filter:blur(4px)}}
.stats{{display:flex;justify-content:center;gap:32px;margin-top:24px;flex-wrap:wrap}}
.stat-num{{font-size:2rem;font-weight:800}}
.stat-label{{font-size:.8rem;opacity:.8;text-transform:uppercase;letter-spacing:.05em}}
.container{{max-width:1200px;margin:-32px auto 0;padding:0 16px 64px}}
.controls{{background:var(--cb);border-radius:var(--r);padding:20px;box-shadow:0 4px 24px rgba(0,0,0,.08);margin-bottom:24px;display:flex;flex-wrap:wrap;gap:12px;align-items:center}}
.sw{{flex:1;min-width:220px;position:relative}}
.sw svg{{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--mu)}}
input[type=search]{{width:100%;padding:12px 14px 12px 42px;border:2px solid var(--bd);border-radius:8px;font-size:1rem;outline:none;transition:border-color .2s}}
input[type=search]:focus{{border-color:var(--p)}}
select{{padding:12px 16px;border:2px solid var(--bd);border-radius:8px;font-size:.9rem;outline:none;cursor:pointer;background:#fff;transition:border-color .2s}}
select:focus{{border-color:var(--p)}}
.rc{{font-size:.9rem;color:var(--mu);font-weight:500;white-space:nowrap}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px}}
.card{{background:var(--cb);border-radius:var(--r);padding:20px;box-shadow:0 2px 12px rgba(0,0,0,.06);border:1px solid var(--bd);transition:transform .15s,box-shadow .15s;display:flex;flex-direction:column;gap:12px}}
.card:hover{{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.1)}}
.ch{{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}}
.ct{{font-size:1rem;font-weight:700;line-height:1.3}}
.dif{{font-size:.7rem;font-weight:700;padding:3px 10px;border-radius:999px;white-space:nowrap;text-transform:uppercase;letter-spacing:.05em}}
.db{{background:#d1fae5;color:#065f46}}
.di{{background:#fef3c7;color:#92400e}}
.da{{background:#fee2e2;color:#991b1b}}
.tag{{display:inline-flex;align-items:center;gap:4px;background:var(--tb);color:var(--tt);font-size:.78rem;font-weight:600;padding:4px 10px;border-radius:999px}}
.uc{{font-size:.85rem;color:var(--mu)}}
.pb{{background:#f9fafb;border:1px solid var(--bd);border-radius:8px;padding:14px;font-size:.88rem;line-height:1.6;white-space:pre-wrap;word-break:break-word;max-height:160px;overflow-y:auto;flex:1}}
.ca{{display:flex;gap:8px}}
.btn{{flex:1;padding:10px;border-radius:8px;font-size:.88rem;font-weight:600;cursor:pointer;border:none;transition:all .15s;display:flex;align-items:center;justify-content:center;gap:6px}}
.bc{{background:var(--p);color:#fff}}
.bc:hover{{background:var(--pd)}}
.bc.ok{{background:var(--ok)}}
.be{{background:var(--bg);color:var(--mu);border:1px solid var(--bd)}}
.be:hover{{background:var(--bd)}}
.nr{{text-align:center;padding:64px 16px;color:var(--mu);grid-column:1/-1}}
footer{{text-align:center;padding:32px;color:var(--mu);font-size:.85rem;border-top:1px solid var(--bd)}}
@media(max-width:600px){{.grid{{grid-template-columns:1fr}}header{{padding:32px 16px 48px}}}}
</style>
</head>
<body>
<header>
  <div class="badge">{niche_badge}</div>
  <h1>{title}</h1>
  <p>{subtitle}</p>
  <div class="stats">
    <div class="stat"><div class="stat-num">{total_count}</div><div class="stat-label">Prompts</div></div>
    <div class="stat"><div class="stat-num">{category_count}</div><div class="stat-label">Categories</div></div>
    <div class="stat"><div class="stat-num">$0</div><div class="stat-label">Extra tools needed</div></div>
  </div>
</header>
<div class="container">
  <div class="controls">
    <div class="sw">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      <input type="search" id="si" placeholder="Search prompts..." oninput="fp()">
    </div>
    <select id="cf" onchange="fp()"><option value="">All Categories</option>{category_options}</select>
    <select id="df" onchange="fp()">
      <option value="">All Levels</option>
      <option value="beginner">Beginner</option>
      <option value="intermediate">Intermediate</option>
      <option value="advanced">Advanced</option>
    </select>
    <div class="rc" id="rc"></div>
  </div>
  <div class="grid" id="pg"></div>
</div>
<footer><p>{footer_text}</p></footer>
<script>
const D={prompts_json};
function eh(s){{return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}}
function dc(d){{if(d==='beginner')return'db';if(d==='advanced')return'da';return'di'}}
function card(p,i){{
  return`<div class="card">
    <div class="ch"><div class="ct">${{eh(p.title)}}</div><span class="dif ${{dc(p.difficulty||'intermediate')}}">${{eh(p.difficulty||'intermediate')}}</span></div>
    <div><span class="tag"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4 6h16M4 12h16M4 18h7"/></svg>${{eh(p.category)}}</span></div>
    <div class="uc">${{eh(p.use_case||'')}}</div>
    <div class="pb" id="pb${{i}}">${{eh(p.prompt)}}</div>
    <div class="ca">
      <button class="btn bc" id="cb${{i}}" onclick="cp(${{i}})">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>Copy
      </button>
      <button class="btn be" onclick="xp(${{i}})">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
      </button>
    </div>
  </div>`;
}}
function cp(i){{
  navigator.clipboard.writeText(D[i].prompt).then(()=>{{
    const b=document.getElementById('cb'+i);
    b.classList.add('ok');
    b.innerHTML='<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>Copied!';
    setTimeout(()=>{{b.classList.remove('ok');b.innerHTML='<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>Copy';}},2000);
  }});
}}
function xp(i){{
  const b=document.getElementById('pb'+i);
  b.style.maxHeight=b.style.maxHeight==='none'?'160px':'none';
}}
function fp(){{
  const s=document.getElementById('si').value.toLowerCase();
  const c=document.getElementById('cf').value;
  const d=document.getElementById('df').value;
  let n=0,html='';
  D.forEach((p,i)=>{{
    const ms=!s||p.title.toLowerCase().includes(s)||p.prompt.toLowerCase().includes(s)||(p.use_case||'').toLowerCase().includes(s)||p.category.toLowerCase().includes(s);
    const mc=!c||p.category===c;
    const md=!d||(p.difficulty||'intermediate')===d;
    if(ms&&mc&&md){{n++;html+=card(p,i);}}
  }});
  document.getElementById('pg').innerHTML=n?html:'<div class="nr"><p>No prompts match your filters.</p></div>';
  document.getElementById('rc').textContent=n+' of '+D.length+' prompts';
}}
fp();
</script>
</body>
</html>"""


def build_html(niche, role, data):
    """Render the HTML template with prompt data and return (html_str, title)."""
    prompts = data["prompts"]
    categories = data["categories"]

    title = f"150 AI Prompts for {niche.title()} — {role.title()} Edition"
    niche_badge = f"{niche.title()} Edition"
    subtitle = (
        f"{len(prompts)} battle-tested AI prompts for {niche} working as {role}s. "
        "Copy, customize, and get results instantly — no extra tools needed."
    )
    category_options = "\n      ".join(
        f'<option value="{cat}">{cat}</option>' for cat in categories
    )
    footer_text = (
        f"Generated {datetime.now().strftime('%B %d, %Y')} &bull; "
        f"{len(prompts)} prompts across {len(categories)} categories &bull; "
        "Works with ChatGPT, Claude, Gemini, and any AI assistant"
    )
    prompts_json = json.dumps(prompts, ensure_ascii=False)

    html = _HTML.format(
        title=title,
        niche_badge=niche_badge,
        subtitle=subtitle,
        total_count=len(prompts),
        category_count=len(categories),
        category_options=category_options,
        footer_text=footer_text,
        prompts_json=prompts_json,
    )
    return html, title


# --- File I/O ---
def _slug(niche, role):
    return urllib.parse.quote_plus(
        f"{niche.lower().replace(' ', '-')}_{role.lower().replace(' ', '-')}"
    )


def write_html(html_content, niche, role, dry_run=False):
    """Write the HTML product file; returns its path."""
    slug = _slug(niche, role)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = safe_path(OUTPUT_DIR / slug)
    out_dir.mkdir(parents=True, exist_ok=True)

    html_path = safe_path(out_dir / f"prompt_library_{slug}_{timestamp}.html")
    if dry_run:
        logging.info("[DRY RUN] Would write HTML → %s", html_path)
        return html_path

    html_path.write_text(html_content, encoding="utf-8")
    logging.info("HTML written → %s", html_path)
    return html_path


def write_artifacts(data, niche, role, dry_run=False):
    """Save raw JSON + CSV alongside the HTML for record-keeping."""
    slug = _slug(niche, role)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = safe_path(OUTPUT_DIR / slug)
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = safe_path(out_dir / f"prompts_{slug}_{timestamp}.json")
    csv_path = safe_path(out_dir / f"prompts_{slug}_{timestamp}.csv")

    if dry_run:
        logging.info("[DRY RUN] Would write JSON → %s", json_path)
        logging.info("[DRY RUN] Would write CSV  → %s", csv_path)
        return

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    logging.info("JSON written → %s", json_path)

    prompts = data.get("prompts", [])
    if prompts:
        fields = ["category", "title", "use_case", "difficulty", "prompt"]
        with open(str(csv_path), "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(prompts)
        logging.info("CSV  written → %s", csv_path)


# --- Status ---
def _load_status():
    path = safe_path(STATUS_FILE)
    if not path.exists():
        return {"runs": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"runs": []}


def _save_status(status):
    path = safe_path(STATUS_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(status, indent=2), encoding="utf-8")


def record_run(niche, role, html_path, prompt_count, success):
    status = _load_status()
    status.setdefault("runs", []).append(
        {
            "timestamp": datetime.now().isoformat(),
            "niche": niche,
            "role": role,
            "output": str(html_path),
            "prompt_count": prompt_count,
            "success": success,
        }
    )
    status["runs"] = status["runs"][-100:]
    _save_status(status)


def show_status():
    status = _load_status()
    runs = status.get("runs", [])
    if not runs:
        print("No runs recorded yet.")
        return
    print(f"Last {min(10, len(runs))} runs (of {len(runs)} total):\n")
    for r in runs[-10:]:
        tag = "[OK  ]" if r.get("success") else "[FAIL]"
        ts = r.get("timestamp", "")[:16]
        print(
            f"  {tag} {ts} | {r.get('niche','?'):15s} / {r.get('role','?'):15s} | "
            f"{r.get('prompt_count', 0):3d} prompts | {r.get('output', '')}"
        )


# --- CLI ---
def parse_args():
    parser = argparse.ArgumentParser(
        prog="html_prompt_library_factory.py",
        description="PRINTMAXX: Generate a 150-prompt HTML library ready for Gumroad ($17).",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", action="store_true", help="Generate prompts and write HTML product")
    group.add_argument("--status", action="store_true", help="Show recent run history")
    group.add_argument("--dry-run", action="store_true", help="Simulate without calling Claude or writing files")

    parser.add_argument("--niche", default="freelancers", help="Target niche (default: freelancers)")
    parser.add_argument(
        "--roles",
        nargs="+",
        default=["copywriter"],
        help="One or more roles to generate for (default: copywriter)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging()

    if args.status:
        show_status()
        sys.exit(0)

    dry_run = args.dry_run
    niche = args.niche
    roles = args.roles

    recall_skills_for_task("generate AI prompt library as digital product for Gumroad")

    overall_ok = True

    for role in roles:
        logging.info("=== START niche='%s' role='%s' dry_run=%s ===", niche, role, dry_run)
        try:
            data = generate_all_prompts(niche, role, dry_run=dry_run)
            if not data or not data.get("prompts"):
                logging.error("No prompts generated for %s/%s — skipping.", niche, role)
                record_run(niche, role, "N/A", 0, False)
                overall_ok = False
                continue

            html_content, title = build_html(niche, role, data)
            html_path = write_html(html_content, niche, role, dry_run=dry_run)
            write_artifacts(data, niche, role, dry_run=dry_run)

            count = len(data["prompts"])
            record_run(niche, role, html_path, count, True)

            capture_skill_from_result(
                {"niche": niche, "role": role, "prompt_count": count, "path": str(html_path)},
                "prompt library generation",
            )

            logging.info("=== DONE %d prompts → %s ===", count, html_path)
            print(f"\n{'='*60}")
            print(f"  Product ready:   {html_path}")
            print(f"  Title:           {title}")
            print(f"  Prompts:         {count} across {len(data['categories'])} categories")
            print(f"  Suggested price: $17 on Gumroad")
            print(f"{'='*60}\n")

        except Exception as exc:
            logging.error("Unhandled error for %s/%s: %s", niche, role, exc, exc_info=True)
            record_run(niche, role, "ERROR", 0, False)
            overall_ok = False

    sys.exit(0 if overall_ok else 1)


if __name__ == "__main__":
    main()