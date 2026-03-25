#!/usr/bin/env python3
"""
PRINTMAXX Automation: app_aesthetic_theme_injector.py

Retro/nostalgic aesthetic theme injector for App Factory builds.
When a new app is scaffolded, auto-suggests and applies Game Boy, Nokia,
Windows 95, or CRT-style CSS themes to increase social shareability and
r/SideProject virality. Aesthetic differentiation = free acquisition on launch.

Workflow type: ACQUISITION
Method context: Built a group trip planner with a Game Boy aesthetic.

Usage:
    python3 app_aesthetic_theme_injector.py --run
    python3 app_aesthetic_theme_injector.py --status
    python3 app_aesthetic_theme_injector.py --dry-run
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path: Path) -> Path:
        resolved = Path(path).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(f"Path escape attempt blocked: {resolved} is outside {PROJECT}")
        return resolved

    def recall_skills_for_task(task_name: str) -> list:
        return []

    def capture_skill_from_result(skill_name: str, result: dict) -> None:
        pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_PATH = AUTOMATIONS_DIR / "logs" / "app_aesthetic_theme_injector.log"
STATE_PATH = AUTOMATIONS_DIR / "state" / "app_aesthetic_theme_injector.json"
APPS_MANIFEST_PATH = AUTOMATIONS_DIR / "data" / "app_factory_manifest.json"
THEME_CATALOG_PATH = AUTOMATIONS_DIR / "data" / "retro_theme_catalog.json"
INJECTION_LOG_PATH = AUTOMATIONS_DIR / "logs" / "theme_injections.csv"

RETRO_THEMES = {
    "gameboy": {
        "name": "Game Boy",
        "description": "Classic green-on-dark palette from Nintendo's 1989 handheld",
        "virality_score": 9.4,
        "platforms": ["web", "mobile"],
        "css_vars": {
            "--bg-primary": "#0f380f",
            "--bg-secondary": "#306230",
            "--bg-tertiary": "#8bac0f",
            "--bg-lightest": "#9bbc0f",
            "--text-primary": "#9bbc0f",
            "--text-secondary": "#8bac0f",
            "--accent": "#0f380f",
            "--border": "#306230",
            "--font-family": "'Press Start 2P', 'Courier New', monospace",
            "--border-radius": "2px",
            "--pixel-border": "4px solid #306230",
            "--shadow": "4px 4px 0px #0f380f",
        },
        "google_font": "Press+Start+2P",
        "body_classes": ["gameboy-theme", "pixel-font"],
        "recommended_for": ["games", "retro", "portfolio", "fun-tools"],
    },
    "nokia": {
        "name": "Nokia 3310",
        "description": "Blue-on-teal monochrome reminiscent of the indestructible brick phone",
        "virality_score": 8.7,
        "platforms": ["web", "mobile"],
        "css_vars": {
            "--bg-primary": "#3a4a3a",
            "--bg-secondary": "#4a5e4a",
            "--bg-tertiary": "#6b7c6b",
            "--bg-lightest": "#c8d8c8",
            "--text-primary": "#c8d8c8",
            "--text-secondary": "#9aaa9a",
            "--accent": "#7aaa7a",
            "--border": "#4a5e4a",
            "--font-family": "'VT323', 'Courier New', monospace",
            "--border-radius": "0px",
            "--pixel-border": "2px solid #6b7c6b",
            "--shadow": "2px 2px 0px #3a4a3a",
        },
        "google_font": "VT323",
        "body_classes": ["nokia-theme", "monochrome-display"],
        "recommended_for": ["utilities", "productivity", "minimalist", "todo-apps"],
    },
    "windows95": {
        "name": "Windows 95",
        "description": "Classic Microsoft desktop OS with beveled borders and teal taskbar",
        "virality_score": 9.1,
        "platforms": ["web", "desktop"],
        "css_vars": {
            "--bg-primary": "#008080",
            "--bg-secondary": "#c0c0c0",
            "--bg-tertiary": "#ffffff",
            "--bg-lightest": "#dfdfdf",
            "--text-primary": "#000000",
            "--text-secondary": "#444444",
            "--accent": "#000080",
            "--border-light": "#ffffff",
            "--border-dark": "#808080",
            "--font-family": "'MS Sans Serif', 'Arial', sans-serif",
            "--border-radius": "0px",
            "--win95-border": "2px solid",
            "--win95-bevel": "inset -2px -2px #808080, inset 2px 2px #ffffff",
            "--shadow": "2px 2px 4px rgba(0,0,0,0.5)",
            "--titlebar-bg": "#000080",
            "--titlebar-text": "#ffffff",
        },
        "google_font": None,
        "body_classes": ["win95-theme", "beveled-ui"],
        "recommended_for": ["productivity", "dashboards", "admin-panels", "saas"],
    },
    "crt": {
        "name": "CRT Terminal",
        "description": "Phosphor green CRT monitor aesthetic with scanlines and glow",
        "virality_score": 8.9,
        "platforms": ["web"],
        "css_vars": {
            "--bg-primary": "#0a0a0a",
            "--bg-secondary": "#001a00",
            "--bg-tertiary": "#003300",
            "--bg-lightest": "#004d00",
            "--text-primary": "#00ff41",
            "--text-secondary": "#00cc33",
            "--text-dim": "#008f11",
            "--accent": "#00ff41",
            "--border": "#00ff41",
            "--font-family": "'Share Tech Mono', 'Courier New', monospace",
            "--border-radius": "0px",
            "--glow": "0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 40px #00ff41",
            "--scanline-opacity": "0.05",
            "--flicker": "crt-flicker 0.15s infinite",
            "--shadow": "0 0 8px #00ff41",
        },
        "google_font": "Share+Tech+Mono",
        "body_classes": ["crt-theme", "phosphor-glow", "scanlines"],
        "recommended_for": ["dev-tools", "hacker-aesthetic", "terminal", "data-viz"],
    },
    "commodore64": {
        "name": "Commodore 64",
        "description": "Blue-on-light-blue BASIC prompt aesthetic from the 1982 home computer",
        "virality_score": 8.5,
        "platforms": ["web"],
        "css_vars": {
            "--bg-primary": "#4040e8",
            "--bg-secondary": "#4040e8",
            "--bg-tertiary": "#5050f8",
            "--bg-lightest": "#7070ff",
            "--text-primary": "#7878f8",
            "--text-secondary": "#5858e8",
            "--accent": "#a0a0ff",
            "--border": "#7878f8",
            "--font-family": "'Pixelify Sans', 'Courier New', monospace",
            "--border-radius": "0px",
            "--pixel-border": "2px solid #7878f8",
            "--shadow": "none",
            "--cursor-blink": "c64-blink 1s step-end infinite",
        },
        "google_font": "Pixelify+Sans",
        "body_classes": ["c64-theme", "basic-prompt"],
        "recommended_for": ["coding-tools", "education", "retro-games", "nostalgia"],
    },
}

CSS_TEMPLATE = """/* PRINTMAXX Retro Theme: {theme_name} */
/* Auto-injected by app_aesthetic_theme_injector.py on {date} */
/* Virality score: {virality_score}/10 — {description} */

@import url('https://fonts.googleapis.com/css2?family={google_font}:wght@400;700&display=swap');

:root {{
{css_vars}
}}

body.{main_class} {{
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: var(--font-family);
    min-height: 100vh;
}}

{extra_styles}
"""

CRT_EXTRA_STYLES = """
body.crt-theme::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 0, 0, var(--scanline-opacity)) 2px,
        rgba(0, 0, 0, var(--scanline-opacity)) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

@keyframes crt-flicker {
    0% { opacity: 0.97; }
    100% { opacity: 1; }
}

body.crt-theme {
    animation: crt-flicker 0.15s infinite;
    text-shadow: var(--glow);
}
"""

WIN95_EXTRA_STYLES = """
.win95-window {
    background: var(--bg-secondary);
    box-shadow: var(--win95-bevel);
    padding: 2px;
}

.win95-titlebar {
    background: var(--titlebar-bg);
    color: var(--titlebar-text);
    padding: 3px 6px;
    font-weight: bold;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
}

.win95-button {
    background: var(--bg-secondary);
    box-shadow: var(--win95-bevel);
    border: none;
    padding: 4px 12px;
    cursor: pointer;
    font-family: var(--font-family);
}

.win95-button:active {
    box-shadow: inset 2px 2px #808080, inset -2px -2px #ffffff;
}
"""

EXTRA_STYLES_MAP = {
    "crt": CRT_EXTRA_STYLES,
    "windows95": WIN95_EXTRA_STYLES,
}

SHARE_COPY_TEMPLATES = {
    "gameboy": [
        "Built {app_name} with a Game Boy aesthetic — hit r/SideProject and blew up overnight",
        "Why does my {app_name} look like a 1989 Nintendo handheld? Because virality.",
        "Launched {app_name} with a Game Boy UI. The nostalgia hook works every time.",
    ],
    "nokia": [
        "{app_name} now looks like a Nokia 3310 and I'm not sorry",
        "Gave {app_name} a monochrome Nokia display aesthetic. r/nostalgia incoming.",
        "Indestructible UI for {app_name}: Nokia 3310 edition just shipped.",
    ],
    "windows95": [
        "{app_name} runs in your browser but looks like Windows 95. The engagement metrics are unreal.",
        "Built {app_name} with a Win95 UI. The bevel borders hit different.",
        "It's {current_year} and {app_name} looks like Windows 95. You're welcome, r/SideProject.",
    ],
    "crt": [
        "{app_name} with CRT scanlines and phosphor glow — hacker aesthetic goes viral every time",
        "Gave {app_name} a green-screen CRT terminal look. Zero marketing budget, maximum shareability.",
        "The {app_name} CRT edition just dropped. Your terminal fantasies are valid.",
    ],
    "commodore64": [
        "{app_name} now boots like a Commodore 64 BASIC prompt. The internet loves it.",
        "10 PRINT 'LAUNCHED {APP_NAME}' — gave it a C64 aesthetic and r/SideProject exploded",
        "{app_name} in Commodore 64 blue. Because 1982 had the best UX.",
    ],
}


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    log_dir = safe_path(LOG_PATH.parent)
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("app_aesthetic_theme_injector")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.FileHandler(safe_path(LOG_PATH), mode="a", encoding="utf-8")
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))
        logger.addHandler(handler)
    return logger


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def load_state() -> dict:
    try:
        p = safe_path(STATE_PATH)
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    except (ValueError, json.JSONDecodeError, OSError):
        pass
    return {
        "last_run": None,
        "total_themes_injected": 0,
        "apps_processed": [],
        "injection_history": [],
    }


def save_state(state: dict, logger: logging.Logger) -> None:
    try:
        p = safe_path(STATE_PATH)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except (ValueError, OSError) as e:
        logger.error(f"Failed to save state: {e}")


# ---------------------------------------------------------------------------
# App discovery
# ---------------------------------------------------------------------------

def discover_apps(logger: logging.Logger) -> list[dict]:
    apps = []

    if APPS_MANIFEST_PATH.exists():
        try:
            with open(safe_path(APPS_MANIFEST_PATH), "r", encoding="utf-8") as f:
                manifest = json.load(f)
            apps = manifest.get("apps", [])
            logger.info(f"Loaded {len(apps)} apps from manifest")
            return apps
        except (ValueError, json.JSONDecodeError, OSError) as e:
            logger.warning(f"Could not load manifest: {e}, falling back to directory scan")

    app_dirs = []
    for candidate_dir in ["apps", "src/apps", "projects", "builds"]:
        scan_path = PROJECT / candidate_dir
        if scan_path.exists() and scan_path.is_dir():
            for child in scan_path.iterdir():
                if child.is_dir() and not child.name.startswith("."):
                    app_dirs.append(child)

    for app_dir in app_dirs:
        app_info = {
            "name": app_dir.name,
            "path": str(app_dir.relative_to(PROJECT)),
            "theme": None,
            "scaffolded_at": None,
        }
        pkg_json = app_dir / "package.json"
        if pkg_json.exists():
            try:
                with open(pkg_json, "r", encoding="utf-8") as f:
                    pkg = json.load(f)
                app_info["name"] = pkg.get("name", app_dir.name)
                app_info["description"] = pkg.get("description", "")
                app_info["framework"] = _detect_framework(pkg)
            except (json.JSONDecodeError, OSError):
                pass
        apps.append(app_info)

    logger.info(f"Discovered {len(apps)} apps via directory scan")
    return apps


def _detect_framework(package_json: dict) -> str:
    deps = {**package_json.get("dependencies", {}), **package_json.get("devDependencies", {})}
    if "next" in deps:
        return "nextjs"
    if "react" in deps:
        return "react"
    if "vue" in deps:
        return "vue"
    if "svelte" in deps:
        return "svelte"
    if "@angular/core" in deps:
        return "angular"
    return "unknown"


# ---------------------------------------------------------------------------
# Theme recommendation engine
# ---------------------------------------------------------------------------

def recommend_theme(app: dict, logger: logging.Logger) -> str:
    name = (app.get("name") or "").lower()
    desc = (app.get("description") or "").lower()
    combined = f"{name} {desc}"

    scores: dict[str, float] = {}
    for theme_key, theme_data in RETRO_THEMES.items():
        score = theme_data["virality_score"]
        for keyword in theme_data.get("recommended_for", []):
            if keyword in combined:
                score += 1.5
        scores[theme_key] = score

    best = max(scores, key=lambda k: scores[k])
    logger.debug(f"Theme scores for '{app.get('name')}': {scores} — selected: {best}")
    return best


# ---------------------------------------------------------------------------
# CSS generation
# ---------------------------------------------------------------------------

def build_css_vars_block(css_vars: dict) -> str:
    lines = []
    for var, value in css_vars.items():
        lines.append(f"    {var}: {value};")
    return "\n".join(lines)


def generate_theme_css(theme_key: str, app_name: str) -> str:
    theme = RETRO_THEMES[theme_key]
    google_font = theme.get("google_font") or "monospace"
    css_vars_block = build_css_vars_block(theme["css_vars"])
    extra = EXTRA_STYLES_MAP.get(theme_key, "")
    main_class = (theme.get("body_classes") or [theme_key])[0]

    return CSS_TEMPLATE.format(
        theme_name=theme["name"],
        date=datetime.now().strftime("%Y-%m-%d"),
        virality_score=theme["virality_score"],
        description=theme["description"],
        google_font=google_font,
        css_vars=css_vars_block,
        main_class=main_class,
        extra_styles=extra,
    )


# ---------------------------------------------------------------------------
# Share copy generation
# ---------------------------------------------------------------------------

def generate_share_copy(theme_key: str, app_name: str) -> list[str]:
    templates = SHARE_COPY_TEMPLATES.get(theme_key, [
        f"Launched {app_name} with a retro aesthetic. r/SideProject approved."
    ])
    year = datetime.now().year
    result = []
    for t in templates:
        copy = t.replace("{app_name}", app_name)
        copy = copy.replace("{APP_NAME}", app_name.upper())
        copy = copy.replace("{current_year}", str(year))
        result.append(copy)
    return result


# ---------------------------------------------------------------------------
# Injection logic
# ---------------------------------------------------------------------------

def inject_theme(app: dict, theme_key: str, dry_run: bool, logger: logging.Logger) -> dict:
    app_name = app.get("name", "unknown-app")
    app_rel_path = app.get("path", "")
    app_path = PROJECT / app_rel_path if app_rel_path else None

    theme = RETRO_THEMES[theme_key]
    css_content = generate_theme_css(theme_key, app_name)
    share_copy = generate_share_copy(theme_key, app_name)

    result = {
        "app": app_name,
        "theme_key": theme_key,
        "theme_name": theme["name"],
        "virality_score": theme["virality_score"],
        "timestamp": datetime.now().isoformat(),
        "dry_run": dry_run,
        "css_written": False,
        "share_copy": share_copy,
        "errors": [],
    }

    if app_path and app_path.exists():
        css_candidates = [
            app_path / "src" / "styles" / f"theme-{theme_key}.css",
            app_path / "styles" / f"theme-{theme_key}.css",
            app_path / "public" / "css" / f"theme-{theme_key}.css",
            app_path / f"theme-{theme_key}.css",
        ]
        target_css = css_candidates[0]
        for candidate in css_candidates:
            if candidate.parent.exists():
                target_css = candidate
                break

        if not dry_run:
            try:
                safe_target = safe_path(target_css)
                safe_target.parent.mkdir(parents=True, exist_ok=True)
                with open(safe_target, "w", encoding="utf-8") as f:
                    f.write(css_content)
                result["css_written"] = True
                result["css_path"] = str(safe_target.relative_to(PROJECT))
                logger.info(f"Wrote {theme['name']} CSS to {safe_target.relative_to(PROJECT)}")
            except (ValueError, OSError) as e:
                err = f"CSS write failed for {app_name}: {e}"
                result["errors"].append(err)
                logger.error(err)
        else:
            result["css_path_preview"] = str(target_css.relative_to(PROJECT))
            logger.info(f"[DRY-RUN] Would write {theme['name']} CSS to {target_css.relative_to(PROJECT)}")

        if not dry_run:
            _write_theme_config(app_path, theme_key, theme, result, logger)
    else:
        result["errors"].append(f"App directory not found: {app_rel_path}")
        logger.warning(f"App directory not found for '{app_name}': {app_rel_path}")
        if not dry_run:
            _write_standalone_output(app_name, theme_key, css_content, result, logger)

    logger.info(
        f"Theme injection {'(dry-run) ' if dry_run else ''}— "
        f"app='{app_name}' theme='{theme['name']}' virality={theme['virality_score']}"
    )
    return result


def _write_theme_config(
    app_path: Path,
    theme_key: str,
    theme: dict,
    result: dict,
    logger: logging.Logger,
) -> None:
    config = {
        "theme_key": theme_key,
        "theme_name": theme["name"],
        "body_classes": theme.get("body_classes", []),
        "google_font": theme.get("google_font"),
        "virality_score": theme["virality_score"],
        "injected_at": result["timestamp"],
        "share_copy": result["share_copy"],
    }
    config_candidates = [
        app_path / ".printmaxx" / "theme.json",
        app_path / "src" / ".printmaxx-theme.json",
        app_path / ".theme.json",
    ]
    target = config_candidates[0]
    for c in config_candidates:
        if c.parent.exists():
            target = c
            break
    try:
        safe_t = safe_path(target)
        safe_t.parent.mkdir(parents=True, exist_ok=True)
        with open(safe_t, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        result["config_path"] = str(safe_t.relative_to(PROJECT))
        logger.info(f"Wrote theme config to {safe_t.relative_to(PROJECT)}")
    except (ValueError, OSError) as e:
        logger.warning(f"Could not write theme config: {e}")


def _write_standalone_output(
    app_name: str,
    theme_key: str,
    css_content: str,
    result: dict,
    logger: logging.Logger,
) -> None:
    output_dir = AUTOMATIONS_DIR / "output" / "theme_injector" / app_name
    try:
        safe_dir = safe_path(output_dir)
        safe_dir.mkdir(parents=True, exist_ok=True)

        css_out = safe_path(safe_dir / f"theme-{theme_key}.css")
        with open(css_out, "w", encoding="utf-8") as f:
            f.write(css_content)
        result["css_written"] = True
        result["css_path"] = str(css_out.relative_to(PROJECT))

        payload = {
            "app_name": app_name,
            "theme_key": theme_key,
            "theme_name": RETRO_THEMES[theme_key]["name"],
            "virality_score": RETRO_THEMES[theme_key]["virality_score"],
            "share_copy": result["share_copy"],
            "css_vars": RETRO_THEMES[theme_key]["css_vars"],
            "body_classes": RETRO_THEMES[theme_key].get("body_classes", []),
            "google_font": RETRO_THEMES[theme_key].get("google_font"),
            "generated_at": result["timestamp"],
        }
        json_out = safe_path(safe_dir / "theme_payload.json")
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        result["payload_path"] = str(json_out.relative_to(PROJECT))

        logger.info(f"Standalone output written to {safe_dir.relative_to(PROJECT)}")
    except (ValueError, OSError) as e:
        err = f"Standalone output write failed: {e}"
        result["errors"].append(err)
        logger.error(err)


# ---------------------------------------------------------------------------
# Injection log (CSV)
# ---------------------------------------------------------------------------

def append_injection_log(result: dict, logger: logging.Logger) -> None:
    if result.get("dry_run"):
        return
    try:
        p = safe_path(INJECTION_LOG_PATH)
        p.parent.mkdir(parents=True, exist_ok=True)
        write_header = not p.exists()
        with open(p, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow([
                    "timestamp", "app", "theme_key", "theme_name",
                    "virality_score", "css_written", "errors",
                ])
            writer.writerow([
                result.get("timestamp", ""),
                result.get("app", ""),
                result.get("theme_key", ""),
                result.get("theme_name", ""),
                result.get("virality_score", ""),
                result.get("css_written", False),
                "; ".join(result.get("errors", [])),
            ])
    except (ValueError, OSError) as e:
        logger.warning(f"Could not append injection log: {e}")


# ---------------------------------------------------------------------------
# Theme catalog persistence
# ---------------------------------------------------------------------------

def save_theme_catalog(logger: logging.Logger) -> None:
    try:
        p = safe_path(THEME_CATALOG_PATH)
        p.parent.mkdir(parents=True, exist_ok=True)
        catalog = {
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "themes": {
                k: {
                    "name": v["name"],
                    "description": v["description"],
                    "virality_score": v["virality_score"],
                    "platforms": v["platforms"],
                    "recommended_for": v.get("recommended_for", []),
                    "body_classes": v.get("body_classes", []),
                    "google_font": v.get("google_font"),
                }
                for k, v in RETRO_THEMES.items()
            },
        }
        with open(p, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2)
        logger.info(f"Theme catalog saved to {p.relative_to(PROJECT)}")
    except (ValueError, OSError) as e:
        logger.warning(f"Could not save theme catalog: {e}")


# ---------------------------------------------------------------------------
# Status report
# ---------------------------------------------------------------------------

def print_status(state: dict, logger: logging.Logger) -> None:
    print("\n=== PRINTMAXX: App Aesthetic Theme Injector — Status ===\n")
    print(f"  Last run:              {state.get('last_run') or 'Never'}")
    print(f"  Themes injected:       {state.get('total_themes_injected', 0)}")
    apps = state.get("apps_processed", [])
    print(f"  Apps processed:        {len(apps)}")

    history = state.get("injection_history", [])
    if history:
        print(f"\n  Recent injections ({min(5, len(history))} of {len(history)}):")
        for entry in history[-5:]:
            status = "OK" if not entry.get("errors") else f"ERRORS: {entry['errors']}"
            dry = " [dry-run]" if entry.get("dry_run") else ""
            print(
                f"    {entry.get('timestamp', '')[:19]}{dry}  "
                f"{entry.get('app', '?'):25s}  "
                f"{entry.get('theme_name', '?'):15s}  "
                f"virality={entry.get('virality_score', '?')}  {status}"
            )

    print(f"\n  Available themes:")
    for key, theme in RETRO_THEMES.items():
        print(f"    [{key:12s}]  {theme['name']:20s}  virality={theme['virality_score']}")

    if INJECTION_LOG_PATH.exists():
        print(f"\n  CSV log: {INJECTION_LOG_PATH.relative_to(PROJECT)}")
    print()
    logger.info("Status report displayed")


# ---------------------------------------------------------------------------
# Core run logic
# ---------------------------------------------------------------------------

def run(dry_run: bool, logger: logging.Logger) -> int:
    mode = "DRY-RUN" if dry_run else "LIVE"
    logger.info(f"--- Starting theme injection run [{mode}] ---")

    state = load_state()
    skills = recall_skills_for_task("aesthetic_theme_injection")
    if skills:
        logger.info(f"Recalled {len(skills)} skills for task")

    save_theme_catalog(logger)

    apps = discover_apps(logger)
    if not apps:
        logger.warning("No apps discovered — nothing to inject")
        print("No apps discovered. Check AUTOMATIONS/data/app_factory_manifest.json or app directories.")
        return 0

    results = []
    for app in apps:
        app_name = app.get("name", "unknown")
        already_processed = app_name in state.get("apps_processed", [])
        if already_processed and not dry_run:
            logger.debug(f"Skipping already-processed app: {app_name}")
            continue

        try:
            theme_key = app.get("theme") or recommend_theme(app, logger)
            result = inject_theme(app, theme_key, dry_run, logger)
            results.append(result)
            append_injection_log(result, logger)

            if not dry_run and not result.get("errors"):
                if app_name not in state["apps_processed"]:
                    state["apps_processed"].append(app_name)
                state["total_themes_injected"] += 1
                state["injection_history"].append(result)
                state["injection_history"] = state["injection_history"][-100:]

            if result.get("share_copy"):
                logger.info(f"Share copy for '{app_name}': {result['share_copy'][0]}")

        except Exception as e:
            logger.error(f"Unexpected error processing app '{app_name}': {e}", exc_info=True)
            results.append({"app": app_name, "errors": [str(e)], "dry_run": dry_run})

    state["last_run"] = datetime.now().isoformat()
    if not dry_run:
        save_state(state, logger)

    success_count = sum(1 for r in results if not r.get("errors"))
    error_count = sum(1 for r in results if r.get("errors"))

    summary = {
        "run_at": state["last_run"],
        "mode": mode,
        "total_apps": len(apps),
        "processed": len(results),
        "success": success_count,
        "errors": error_count,
        "results": results,
    }

    capture_skill_from_result("aesthetic_theme_injection", summary)

    logger.info(
        f"Run complete [{mode}]: {success_count} injected, {error_count} errors "
        f"out of {len(results)} apps"
    )
    print(
        f"[{mode}] Theme injection complete: {success_count} succeeded, "
        f"{error_count} errors, {len(results)} apps processed."
    )

    if dry_run:
        print("\nDry-run preview:")
        for r in results:
            css_preview = r.get("css_path_preview", r.get("css_path", "N/A"))
            print(f"  {r.get('app', '?'):25s}  {r.get('theme_name', '?'):15s}  -> {css_preview}")
            if r.get("share_copy"):
                print(f"    Share: {r['share_copy'][0]}")

    return 0 if error_count == 0 else 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: Retro aesthetic theme injector for App Factory builds",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --run         Inject themes into all discovered apps\n"
            "  %(prog)s --dry-run     Preview theme injections without writing files\n"
            "  %(prog)s --status      Show injection history and available themes\n"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", action="store_true", help="Run theme injection")
    group.add_argument("--status", action="store_true", help="Show status and history")
    group.add_argument("--dry-run", action="store_true", dest="dry_run",
                       help="Preview injections without writing files")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = setup_logging()

    try:
        if args.status:
            state = load_state()
            print_status(state, logger)
            sys.exit(0)
        elif args.dry_run:
            exit_code = run(dry_run=True, logger=logger)
            sys.exit(exit_code)
        elif args.run:
            exit_code = run(dry_run=False, logger=logger)
            sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        try:
            logger.critical(f"Fatal error: {e}", exc_info=True)
        except Exception:
            pass
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()