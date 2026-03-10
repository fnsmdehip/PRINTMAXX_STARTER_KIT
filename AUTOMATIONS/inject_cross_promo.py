#!/usr/bin/env python3
"""
inject_cross_promo.py - Injects a cross-promotion footer into all 8 PRINTMAXX PWAs.

Adds a "more free tools" section + email capture before </body>.
Idempotent: skips files that already have id="cross-promo".
Makes a .bak backup before modifying.
"""

import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")

# --------------------------------------------------------------------------- #
# PWA registry
# --------------------------------------------------------------------------- #

PWAS = [
    {
        "name": "TaskSmash",
        "url": "https://tasksmash.surge.sh",
        "desc": "ADHD task breaker. free goblin tools alternative.",
        "path": PROJECT_ROOT / "MONEY_METHODS/APP_FACTORY/builds/tasksmash-web/index.html",
    },
    {
        "name": "CoreDay",
        "url": "https://coreday.surge.sh",
        "desc": "3 non-negotiables. that's it. win your day.",
        "path": PROJECT_ROOT / "MONEY_METHODS/APP_FACTORY/coreday/index.html",
    },
    {
        "name": "FocusLock",
        "url": "https://focuslock-web.surge.sh",
        "desc": "pomodoro timer with stats. lock in.",
        "path": PROJECT_ROOT / "MONEY_METHODS/APP_FACTORY/builds/focuslock-web/index.html",
    },
    {
        "name": "HabitForge",
        "url": "https://habitforge-web.surge.sh",
        "desc": "build streaks. track habits. no BS.",
        "path": PROJECT_ROOT / "ralph/loops/app_factory/output/habitforge-web/index.html",
    },
    {
        "name": "MealMaxx",
        "url": "https://mealmaxx-web.surge.sh",
        "desc": "meal planning that doesn't suck.",
        "path": PROJECT_ROOT / "ralph/loops/app_factory/output/mealmaxx-web/index.html",
    },
    {
        "name": "SleepMaxx",
        "url": "https://sleepmaxx-web.surge.sh",
        "desc": "sleep tracking and optimization.",
        "path": PROJECT_ROOT / "MONEY_METHODS/APP_FACTORY/builds/sleepmaxx-web/index.html",
    },
    {
        "name": "WalkToUnlock",
        "url": "https://walktounlock-web.surge.sh",
        "desc": "walking incentive. earn your screen time.",
        "path": PROJECT_ROOT / "MONEY_METHODS/APP_FACTORY/builds/walktounlock-web/index.html",
    },
    {
        "name": "Hilal",
        "url": "https://ramadan-tracker.surge.sh",
        "desc": "ramadan companion. fasting, prayer, quran.",
        "path": PROJECT_ROOT / "ralph/loops/app_factory/output/ramadan-tracker/index.html",
    },
]

# --------------------------------------------------------------------------- #
# Path guard
# --------------------------------------------------------------------------- #

def safe_path(target: Path) -> Path:
    """Raise if path escapes project root."""
    resolved = target.resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


# --------------------------------------------------------------------------- #
# HTML generation
# --------------------------------------------------------------------------- #

def build_cross_promo_html(current_name: str) -> str:
    """Build the cross-promo footer HTML, excluding the current app."""
    others = [p for p in PWAS if p["name"] != current_name]

    cards_html = "\n".join(
        f'      <a href="{p["url"]}" target="_blank" rel="noopener" style="'
        f'display:block;padding:12px 14px;background:#111827;border:1px solid #1f2937;'
        f'border-radius:8px;text-decoration:none;transition:border-color 0.15s;"'
        f' onmouseover="this.style.borderColor=\'#3b82f6\'" onmouseout="this.style.borderColor=\'#1f2937\'">'
        f'<span style="font-size:13px;font-weight:600;color:#e5e5e5;display:block;margin-bottom:3px;">{p["name"]}</span>'
        f'<span style="font-size:12px;color:#9ca3af;">{p["desc"]}</span>'
        f"</a>"
        for p in others
    )

    return f"""
<!-- cross-promo: injected by inject_cross_promo.py -->
<div id="cross-promo" style="
  background:#0a0f1a;
  border-top:1px solid #1f2937;
  padding:32px 20px 40px;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  color:#e5e5e5;
  margin-top:48px;
">
  <p style="margin:0 0 18px;font-size:11px;font-weight:600;letter-spacing:0.08em;color:#6b7280;text-transform:uppercase;">more free tools</p>
  <div style="
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(160px,1fr));
    gap:10px;
    margin-bottom:32px;
  ">
{cards_html}
  </div>

  <!-- email capture -->
  <div style="border-top:1px solid #1f2937;padding-top:24px;max-width:400px;">
    <p style="margin:0 0 4px;font-size:14px;font-weight:600;color:#e5e5e5;">join 2,000+ solopreneurs</p>
    <p style="margin:0 0 14px;font-size:12px;color:#9ca3af;">free tools, no fluff. unsubscribe any time.</p>
    <!-- TODO: wire to beehiiv/convertkit -->
    <form action="#" method="POST" style="display:flex;gap:8px;flex-wrap:wrap;">
      <input
        type="email"
        name="email"
        placeholder="your@email.com"
        required
        style="
          flex:1;min-width:180px;
          padding:9px 12px;
          background:#111827;
          border:1px solid #374151;
          border-radius:6px;
          color:#e5e5e5;
          font-size:13px;
          outline:none;
        "
        onfocus="this.style.borderColor='#3b82f6'"
        onblur="this.style.borderColor='#374151'"
      />
      <button
        type="submit"
        style="
          padding:9px 16px;
          background:#3b82f6;
          border:none;
          border-radius:6px;
          color:#fff;
          font-size:13px;
          font-weight:600;
          cursor:pointer;
          white-space:nowrap;
        "
        onmouseover="this.style.background='#2563eb'"
        onmouseout="this.style.background='#3b82f6'"
      >get updates</button>
    </form>
  </div>
</div>
<!-- /cross-promo -->
"""


# --------------------------------------------------------------------------- #
# Injection logic
# --------------------------------------------------------------------------- #

def process_pwa(pwa: dict) -> str:
    """
    Process one PWA. Returns one of:
      'modified' | 'skipped_already_present' | 'skipped_no_body' | 'error:<msg>' | 'skipped_missing'
    """
    path: Path = pwa["path"]

    # guard
    try:
        safe_path(path)
    except ValueError as e:
        return f"error:{e}"

    if not path.exists():
        return "skipped_missing"

    content = path.read_text(encoding="utf-8")

    # dedup check
    if 'id="cross-promo"' in content or "cross-promo" in content or "more-tools" in content:
        return "skipped_already_present"

    # find injection point
    close_body = content.rfind("</body>")
    if close_body == -1:
        return "skipped_no_body"

    # backup
    bak_path = path.with_suffix(".html.bak")
    try:
        safe_path(bak_path)
    except ValueError as e:
        return f"error:{e}"
    shutil.copy2(path, bak_path)

    # inject
    injection = build_cross_promo_html(pwa["name"])
    new_content = content[:close_body] + injection + content[close_body:]

    path.write_text(new_content, encoding="utf-8")
    return "modified"


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main() -> None:
    results = {"modified": [], "skipped_already_present": [], "skipped_missing": [], "other": []}

    for pwa in PWAS:
        status = process_pwa(pwa)
        name = pwa["name"]
        path = pwa["path"]

        if status == "modified":
            results["modified"].append((name, path))
        elif status == "skipped_already_present":
            results["skipped_already_present"].append((name, path))
        elif status == "skipped_missing":
            results["skipped_missing"].append((name, path))
        else:
            results["other"].append((name, path, status))

    # ---------- summary ----------
    print("\n" + "=" * 60)
    print("cross-promo injection summary")
    print("=" * 60)

    if results["modified"]:
        print(f"\n  modified ({len(results['modified'])}):")
        for name, path in results["modified"]:
            print(f"    + {name}")
            print(f"      {path}")

    if results["skipped_already_present"]:
        print(f"\n  skipped - cross-promo already present ({len(results['skipped_already_present'])}):")
        for name, path in results["skipped_already_present"]:
            print(f"    - {name}  ({path.name})")

    if results["skipped_missing"]:
        print(f"\n  skipped - file not found ({len(results['skipped_missing'])}):")
        for name, path in results["skipped_missing"]:
            print(f"    ! {name}")
            print(f"      expected: {path}")

    if results["other"]:
        print(f"\n  other / errors ({len(results['other'])}):")
        for name, path, status in results["other"]:
            print(f"    ? {name}: {status}")

    total = len(PWAS)
    mod = len(results["modified"])
    skip = len(results["skipped_already_present"])
    miss = len(results["skipped_missing"])
    print(f"\n  total: {total}  |  injected: {mod}  |  already done: {skip}  |  missing: {miss}")
    print("=" * 60 + "\n")

    if results["modified"]:
        print("backups saved as index.html.bak in each app directory.")
        print("email form action='#' — wire to beehiiv/convertkit when ready.\n")

    sys.exit(0 if not results["other"] else 1)


if __name__ == "__main__":
    main()
