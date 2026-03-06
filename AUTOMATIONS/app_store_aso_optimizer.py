#!/usr/bin/env python3
"""
App Store ASO Optimizer - Keyword optimization, localization, tracking.

Reads competitor data from MONEY_METHODS/APP_FACTORY/COMPETITOR_REAL_DATA.md,
generates optimized ASO keywords, localizes metadata, tracks rankings.

Usage:
    python3 AUTOMATIONS/app_store_aso_optimizer.py --optimize focuslock
    python3 AUTOMATIONS/app_store_aso_optimizer.py --keywords sleepmaxx
    python3 AUTOMATIONS/app_store_aso_optimizer.py --localize hilal
    python3 AUTOMATIONS/app_store_aso_optimizer.py --track focuslock
    python3 AUTOMATIONS/app_store_aso_optimizer.py --all-apps
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
COMPETITOR_DATA_PATH = PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY" / "COMPETITOR_REAL_DATA.md"
ASO_DATA_DIR = PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY" / "aso_data"
TRACKING_FILE = ASO_DATA_DIR / "keyword_rankings.json"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT.resolve())):
        raise ValueError(f"BLOCKED: {resolved} is outside project root")
    return resolved


# ---------------------------------------------------------------------------
# App keyword profiles - curated per app based on competitor analysis
# ---------------------------------------------------------------------------
APP_KEYWORD_PROFILES = {
    "focuslock": {
        "display_name": "FocusLock",
        "category": "Productivity",
        "primary_keywords": [
            "focus", "timer", "pomodoro", "block", "distraction",
            "productivity", "study", "screen time", "app blocker", "work",
        ],
        "secondary_keywords": [
            "concentrate", "deep work", "lock phone", "study timer",
            "white noise", "ambient", "forest", "do not disturb",
            "time management", "exam", "adhd", "school",
        ],
        "competitor_names": ["Forest", "Opal", "Flora", "Freedom", "Structured"],
        "competitor_keywords": [
            "focus timer", "app blocker", "screen time limit", "study aid",
            "pomodoro technique", "digital wellbeing", "phone addiction",
        ],
        "avoid_keywords": ["game", "social", "chat", "video"],
    },
    "habitforge": {
        "display_name": "HabitForge",
        "category": "Health & Fitness",
        "primary_keywords": [
            "habit", "tracker", "streak", "routine", "daily",
            "goals", "discipline", "morning", "consistency", "heatmap",
        ],
        "secondary_keywords": [
            "habit builder", "self improvement", "daily planner",
            "routine tracker", "goal setting", "accountability",
            "new year resolution", "wellness", "lifestyle", "mindset",
        ],
        "competitor_names": ["Streaks", "Habitify", "Finch", "Habitica", "Done"],
        "competitor_keywords": [
            "habit tracking", "daily habits", "streak counter",
            "self care", "routine planner", "habit loop",
        ],
        "avoid_keywords": ["pet", "game", "social media"],
    },
    "mealmaxx": {
        "display_name": "MealMaxx",
        "category": "Food & Drink",
        "primary_keywords": [
            "meal", "prep", "plan", "grocery", "list",
            "macros", "calories", "recipe", "diet", "nutrition",
        ],
        "secondary_keywords": [
            "meal planner", "grocery list", "macro tracker",
            "keto", "vegan", "halal", "weight loss",
            "food log", "cooking", "healthy eating",
        ],
        "competitor_names": ["MyFitnessPal", "Yummly", "Mealime", "Eat This Much", "MacroFactor"],
        "competitor_keywords": [
            "calorie counter", "food diary", "meal planning",
            "recipe finder", "diet plan", "nutrition tracker",
        ],
        "avoid_keywords": ["restaurant", "delivery", "takeout"],
    },
    "hilal": {
        "display_name": "Hilal",
        "category": "Lifestyle",
        "primary_keywords": [
            "ramadan", "prayer", "times", "fasting", "islam",
            "quran", "dua", "iftar", "suhoor", "muslim",
        ],
        "secondary_keywords": [
            "salah", "adhan", "qibla", "taraweeh", "eid",
            "islamic", "hajj", "dhikr", "mosque", "halal",
        ],
        "competitor_names": ["Muslim Pro", "Athan", "Quran Majeed", "IslamicFinder", "Pillars"],
        "competitor_keywords": [
            "prayer times", "azan", "quran reader", "ramadan calendar",
            "islamic prayer", "fasting tracker", "qibla compass",
        ],
        "avoid_keywords": ["game", "dating"],
    },
    "sleepmaxx": {
        "display_name": "SleepMaxx",
        "category": "Health & Fitness",
        "primary_keywords": [
            "sleep", "tracker", "insomnia", "bedtime", "routine",
            "sounds", "alarm", "rest", "night", "quality",
        ],
        "secondary_keywords": [
            "sleep aid", "white noise", "brown noise", "rain sounds",
            "sleep score", "circadian", "melatonin", "snore",
            "sleep diary", "wind down", "relaxation", "nap",
        ],
        "competitor_names": ["Sleep Cycle", "Rise", "ShutEye", "Calm", "Pillow"],
        "competitor_keywords": [
            "sleep tracker", "sleep sounds", "smart alarm",
            "sleep analysis", "bedtime reminder", "sleep quality",
        ],
        "avoid_keywords": ["dating", "social"],
    },
    "walktounlock": {
        "display_name": "WalkToUnlock",
        "category": "Health & Fitness",
        "primary_keywords": [
            "walk", "steps", "pedometer", "fitness", "walking",
            "health", "exercise", "motivation", "streak", "rewards",
        ],
        "secondary_keywords": [
            "step counter", "daily steps", "walking tracker",
            "10000 steps", "step goal", "activity", "outdoor",
            "weight loss", "cardio", "move", "challenge", "miles",
        ],
        "competitor_names": ["StepBet", "Sweatcoin", "WeWalk", "Pacer", "StepsApp"],
        "competitor_keywords": [
            "step tracker", "walking app", "fitness tracker",
            "step counter pedometer", "daily walk", "walk rewards",
        ],
        "avoid_keywords": ["running", "gym", "cycling"],
    },
}

# ---------------------------------------------------------------------------
# Localization templates
# ---------------------------------------------------------------------------
LOCALES = {
    "en-US": {
        "name": "English (US)",
        "code": "en-US",
    },
    "es-ES": {
        "name": "Spanish (Spain)",
        "code": "es-ES",
    },
    "ar-SA": {
        "name": "Arabic (Saudi Arabia)",
        "code": "ar-SA",
    },
    "pt-BR": {
        "name": "Portuguese (Brazil)",
        "code": "pt-BR",
    },
    "hi-IN": {
        "name": "Hindi (India)",
        "code": "hi-IN",
    },
}

# Localized keyword sets per locale (manually curated for quality)
LOCALE_KEYWORD_OVERRIDES = {
    "focuslock": {
        "es-ES": "enfoque,temporizador,pomodoro,bloquear,distracciones,productividad,estudiar,trabajo,concentrar,tiempo",
        "ar-SA": "تركيز,مؤقت,بومودورو,حظر,تشتت,إنتاجية,دراسة,عمل,وقت,شاشة",
        "pt-BR": "foco,temporizador,pomodoro,bloquear,distração,produtividade,estudar,trabalho,concentrar,tempo",
        "hi-IN": "फोकस,टाइमर,पोमोडोरो,ब्लॉक,ध्यान,उत्पादकता,पढ़ाई,काम,एकाग्रता,समय",
    },
    "habitforge": {
        "es-ES": "hábito,rastreador,racha,rutina,diario,metas,disciplina,mañana,consistencia,progreso",
        "ar-SA": "عادة,متتبع,سلسلة,روتين,يومي,أهداف,انضباط,صباح,ثبات,تقدم",
        "pt-BR": "hábito,rastreador,sequência,rotina,diário,metas,disciplina,manhã,consistência,progresso",
        "hi-IN": "आदत,ट्रैकर,स्ट्रीक,दिनचर्या,दैनिक,लक्ष्य,अनुशासन,सुबह,निरंतरता,प्रगति",
    },
    "mealmaxx": {
        "es-ES": "comida,preparar,planificar,compras,lista,macros,calorías,receta,dieta,nutrición",
        "ar-SA": "وجبة,تحضير,خطة,بقالة,قائمة,ماكرو,سعرات,وصفة,حمية,تغذية",
        "pt-BR": "refeição,preparo,planejar,compras,lista,macros,calorias,receita,dieta,nutrição",
        "hi-IN": "भोजन,तैयारी,योजना,किराना,सूची,मैक्रो,कैलोरी,रेसिपी,आहार,पोषण",
    },
    "hilal": {
        "es-ES": "ramadán,oración,horarios,ayuno,islam,corán,dua,iftar,suhoor,musulmán",
        "ar-SA": "رمضان,صلاة,أوقات,صيام,إسلام,قرآن,دعاء,إفطار,سحور,مسلم",
        "pt-BR": "ramadã,oração,horários,jejum,islã,alcorão,dua,iftar,suhoor,muçulmano",
        "hi-IN": "रमज़ान,नमाज़,समय,रोज़ा,इस्लाम,कुरान,दुआ,इफ्तार,सहरी,मुस्लिम",
    },
    "sleepmaxx": {
        "es-ES": "sueño,rastreador,insomnio,dormir,rutina,sonidos,alarma,descanso,noche,calidad",
        "ar-SA": "نوم,متتبع,أرق,نوم,روتين,أصوات,منبه,راحة,ليل,جودة",
        "pt-BR": "sono,rastreador,insônia,dormir,rotina,sons,alarme,descanso,noite,qualidade",
        "hi-IN": "नींद,ट्रैकर,अनिद्रा,सोना,दिनचर्या,ध्वनि,अलार्म,आराम,रात,गुणवत्ता",
    },
    "walktounlock": {
        "es-ES": "caminar,pasos,podómetro,fitness,caminata,salud,ejercicio,motivación,racha,recompensas",
        "ar-SA": "مشي,خطوات,عداد,لياقة,المشي,صحة,تمرين,تحفيز,سلسلة,مكافآت",
        "pt-BR": "caminhar,passos,pedômetro,fitness,caminhada,saúde,exercício,motivação,sequência,recompensas",
        "hi-IN": "चलना,कदम,पेडोमीटर,फिटनेस,पैदल,स्वास्थ्य,व्यायाम,प्रेरणा,स्ट्रीक,पुरस्कार",
    },
}

# Localized subtitles
LOCALE_SUBTITLES = {
    "focuslock": {
        "es-ES": "Bloquea Distracciones, Enfócate",
        "ar-SA": "حظر التشتت، حافظ على التركيز",
        "pt-BR": "Bloqueie Distrações, Foque",
        "hi-IN": "ध्यान भटकाव रोकें, फोकस बनाएं",
    },
    "habitforge": {
        "es-ES": "Crea Hábitos Que Realmente Duran",
        "ar-SA": "ابنِ عادات تدوم فعلاً",
        "pt-BR": "Crie Hábitos Que Realmente Ficam",
        "hi-IN": "ऐसी आदतें बनाएं जो टिकें",
    },
    "mealmaxx": {
        "es-ES": "Preparación de Comidas Simplificada",
        "ar-SA": "تحضير الوجبات بسهولة",
        "pt-BR": "Preparação de Refeições Simplificada",
        "hi-IN": "भोजन तैयारी आसान बनाएं",
    },
    "hilal": {
        "es-ES": "Rastreador de Ramadán y Oraciones",
        "ar-SA": "متتبع رمضان وأوقات الصلاة",
        "pt-BR": "Rastreador de Ramadã e Orações",
        "hi-IN": "रमज़ान ट्रैकर और नमाज़ का समय",
    },
    "sleepmaxx": {
        "es-ES": "Mejor Sueño Empieza Esta Noche",
        "ar-SA": "نوم أفضل يبدأ الليلة",
        "pt-BR": "Sono Melhor Começa Hoje à Noite",
        "hi-IN": "बेहतर नींद आज रात से शुरू",
    },
    "walktounlock": {
        "es-ES": "Camina Más. Gana Recompensas.",
        "ar-SA": "امشِ أكثر. اكسب مكافآت.",
        "pt-BR": "Caminhe Mais. Ganhe Recompensas.",
        "hi-IN": "ज़्यादा चलें। इनाम पाएं।",
    },
}


# ---------------------------------------------------------------------------
# Competitor data parser
# ---------------------------------------------------------------------------

def parse_competitor_data() -> dict:
    """Parse COMPETITOR_REAL_DATA.md into structured data."""
    if not COMPETITOR_DATA_PATH.exists():
        print(f"  [!] Competitor data not found: {COMPETITOR_DATA_PATH}")
        return {}

    content = COMPETITOR_DATA_PATH.read_text()
    competitors = {}
    current_category = None
    current_app = None

    for line in content.split("\n"):
        # Detect category headers
        cat_match = re.match(r"^## (\w[\w\s/]+) CATEGORY", line)
        if cat_match:
            current_category = cat_match.group(1).strip()
            continue

        # Detect app headers
        app_match = re.match(r"^### \d+\.\s+(.+)$", line)
        if app_match:
            current_app = app_match.group(1).strip()
            competitors[current_app] = {
                "category": current_category,
                "pricing": None,
                "rating": None,
                "revenue": None,
                "downloads": None,
                "complaints": [],
            }
            continue

        if not current_app or current_app not in competitors:
            continue

        # Parse table rows
        if "| **Current Price**" in line:
            price_match = re.search(r"\|\s*(.+?)\s*\|", line.split("**Current Price**")[1])
            if price_match:
                competitors[current_app]["pricing"] = price_match.group(1).strip()

        if "| **App Store Rating**" in line:
            rating_match = re.search(r"(\d+\.?\d*)\s*stars", line)
            if rating_match:
                competitors[current_app]["rating"] = float(rating_match.group(1))

        if "| **Monthly Revenue**" in line or "| **Revenue Est**" in line:
            rev_match = re.search(r"\$[\d,.]+[KMB]?(?:/\w+)?", line)
            if rev_match:
                competitors[current_app]["revenue"] = rev_match.group(0)

        if "| **Monthly Downloads**" in line:
            dl_match = re.search(r"([\d,.]+[KM]?)/month", line)
            if dl_match:
                competitors[current_app]["downloads"] = dl_match.group(0)

        # Parse complaints
        if line.strip().startswith("- ") and current_app and "complaint" not in line.lower():
            complaint = line.strip().lstrip("- ").strip('"').strip("'")
            if len(complaint) > 10 and "edge" not in complaint.lower():
                competitors[current_app]["complaints"].append(complaint)

    return competitors


# ---------------------------------------------------------------------------
# Keyword optimization engine
# ---------------------------------------------------------------------------

def optimize_keywords(app_key: str, competitor_data: dict) -> dict:
    """Generate optimized 100-char keyword field for Apple App Store."""
    if app_key not in APP_KEYWORD_PROFILES:
        print(f"  [-] Unknown app: {app_key}")
        return {}

    profile = APP_KEYWORD_PROFILES[app_key]

    # Score keywords based on relevance, competition, and uniqueness
    keyword_scores = {}

    # Primary keywords get highest base score
    for kw in profile["primary_keywords"]:
        keyword_scores[kw.lower()] = 10.0

    # Secondary keywords
    for kw in profile["secondary_keywords"]:
        keyword_scores[kw.lower()] = 6.0

    # Competitor keywords that aren't in primary -- opportunity gap
    for kw in profile["competitor_keywords"]:
        kw_lower = kw.lower()
        if kw_lower not in keyword_scores:
            keyword_scores[kw_lower] = 4.0
        else:
            keyword_scores[kw_lower] += 2.0  # Boost if we already had it

    # Penalize keywords that are in competitor app names (hard to rank for)
    for comp_name in profile["competitor_names"]:
        comp_lower = comp_name.lower()
        if comp_lower in keyword_scores:
            keyword_scores[comp_lower] *= 0.3  # Heavy penalty

    # Remove avoid keywords
    for kw in profile["avoid_keywords"]:
        keyword_scores.pop(kw.lower(), None)

    # Remove the app's own name (Apple already indexes it)
    display_lower = profile["display_name"].lower()
    keyword_scores.pop(display_lower, None)

    # Remove single-character keywords
    keyword_scores = {k: v for k, v in keyword_scores.items() if len(k) > 1}

    # Sort by score descending
    sorted_keywords = sorted(keyword_scores.items(), key=lambda x: -x[1])

    # Build the 100-char keyword string (comma-separated, no spaces after commas)
    # Apple strips spaces around commas anyway, but we keep it tight
    selected = []
    current_length = 0

    for kw, score in sorted_keywords:
        # Calculate length: keyword + comma separator
        add_length = len(kw) + (1 if selected else 0)  # +1 for comma
        if current_length + add_length <= 100:
            selected.append(kw)
            current_length += add_length
        else:
            # Try shorter keywords from remaining
            continue

    keyword_string = ",".join(selected)

    result = {
        "app_key": app_key,
        "display_name": profile["display_name"],
        "keyword_string": keyword_string,
        "keyword_count": len(selected),
        "char_count": len(keyword_string),
        "chars_remaining": 100 - len(keyword_string),
        "all_scored_keywords": [
            {"keyword": kw, "score": round(score, 1)}
            for kw, score in sorted_keywords
        ],
        "selected_keywords": selected,
        "excluded_keywords": [
            kw for kw, _ in sorted_keywords if kw not in selected
        ],
        "generated_at": datetime.now().isoformat(),
    }

    return result


def generate_localized_metadata(app_key: str) -> dict:
    """Generate localized metadata for all supported locales."""
    if app_key not in APP_KEYWORD_PROFILES:
        print(f"  [-] Unknown app: {app_key}")
        return {}

    profile = APP_KEYWORD_PROFILES[app_key]
    localized = {}

    for locale_code, locale_info in LOCALES.items():
        entry = {
            "locale": locale_code,
            "locale_name": locale_info["name"],
            "name": profile["display_name"],  # App name stays English (brand)
        }

        if locale_code == "en-US":
            # English uses the base keywords from profile
            try:
                sys.path.insert(0, str(PROJECT_ROOT / "AUTOMATIONS"))
                from ios_release_pipeline import APP_REGISTRY as FULL_REGISTRY
                if app_key in FULL_REGISTRY:
                    reg = FULL_REGISTRY[app_key]
                    entry["subtitle"] = reg.get("subtitle", profile["display_name"])
                    entry["keywords"] = reg.get("keywords", ",".join(profile["primary_keywords"][:10]))
                    entry["description"] = reg.get("description", "")
                    entry["promotional_text"] = reg.get("promotional_text", "")
                else:
                    entry["subtitle"] = profile["display_name"]
                    entry["keywords"] = ",".join(profile["primary_keywords"][:10])
            except ImportError:
                entry["subtitle"] = profile["display_name"]
                entry["keywords"] = ",".join(profile["primary_keywords"][:10])
        else:
            # Use localized overrides
            subtitles = LOCALE_SUBTITLES.get(app_key, {})
            entry["subtitle"] = subtitles.get(locale_code, profile["display_name"])

            kw_overrides = LOCALE_KEYWORD_OVERRIDES.get(app_key, {})
            entry["keywords"] = kw_overrides.get(locale_code, "")

            entry["description"] = f"[Translate from en-US for {locale_code}]"
            entry["promotional_text"] = f"[Translate from en-US for {locale_code}]"

        localized[locale_code] = entry

    return localized


# ---------------------------------------------------------------------------
# Keyword tracking
# ---------------------------------------------------------------------------

def load_tracking_data() -> dict:
    if TRACKING_FILE.exists():
        return json.loads(TRACKING_FILE.read_text())
    return {"apps": {}, "snapshots": []}


def save_tracking_data(data: dict) -> None:
    safe_path(TRACKING_FILE)
    TRACKING_FILE.parent.mkdir(parents=True, exist_ok=True)
    TRACKING_FILE.write_text(json.dumps(data, indent=2, default=str))


def track_keywords(app_key: str) -> None:
    """Record a keyword tracking snapshot for an app."""
    profile = APP_KEYWORD_PROFILES.get(app_key)
    if not profile:
        print(f"  [-] Unknown app: {app_key}")
        return

    tracking = load_tracking_data()

    if app_key not in tracking["apps"]:
        tracking["apps"][app_key] = {"snapshots": []}

    # Generate current optimized keywords
    competitor_data = parse_competitor_data()
    optimized = optimize_keywords(app_key, competitor_data)

    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "keyword_string": optimized.get("keyword_string", ""),
        "keyword_count": optimized.get("keyword_count", 0),
        "char_count": optimized.get("char_count", 0),
        "selected_keywords": optimized.get("selected_keywords", []),
    }

    tracking["apps"][app_key]["snapshots"].append(snapshot)

    # Keep last 50 snapshots per app
    if len(tracking["apps"][app_key]["snapshots"]) > 50:
        tracking["apps"][app_key]["snapshots"] = tracking["apps"][app_key]["snapshots"][-50:]

    save_tracking_data(tracking)

    # Show tracking history
    snapshots = tracking["apps"][app_key]["snapshots"]
    print(f"\n  Keyword tracking for {profile['display_name']}:")
    print(f"  Total snapshots: {len(snapshots)}")

    if len(snapshots) >= 2:
        prev = set(snapshots[-2]["selected_keywords"])
        curr = set(snapshots[-1]["selected_keywords"])
        added = curr - prev
        removed = prev - curr
        if added:
            print(f"  Added:   {', '.join(added)}")
        if removed:
            print(f"  Removed: {', '.join(removed)}")
        if not added and not removed:
            print("  No changes from previous snapshot.")
    else:
        print("  First snapshot recorded.")

    print(f"  Current: {snapshot['keyword_string']}")
    print(f"  ({snapshot['char_count']}/100 chars, {snapshot['keyword_count']} keywords)")


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_optimization_report(result: dict) -> None:
    """Print a formatted optimization report."""
    print(f"\n{'='*60}")
    print(f"  ASO KEYWORD OPTIMIZATION: {result['display_name']}")
    print(f"{'='*60}")
    print(f"\n  Keyword field ({result['char_count']}/100 chars, {result['chars_remaining']} remaining):")
    print(f"  {result['keyword_string']}")
    print(f"\n  Selected keywords ({result['keyword_count']}):")
    for i, kw in enumerate(result["selected_keywords"], 1):
        score = next((s["score"] for s in result["all_scored_keywords"] if s["keyword"] == kw), 0)
        print(f"    {i:2d}. {kw:25s} (score: {score})")

    if result["excluded_keywords"]:
        print(f"\n  Excluded (would not fit / low score):")
        for kw in result["excluded_keywords"][:10]:
            score = next((s["score"] for s in result["all_scored_keywords"] if s["keyword"] == kw), 0)
            print(f"      {kw:25s} (score: {score})")

    print(f"\n{'='*60}\n")


def print_localization_report(app_key: str, localized: dict) -> None:
    """Print a formatted localization report."""
    profile = APP_KEYWORD_PROFILES.get(app_key, {})
    print(f"\n{'='*60}")
    print(f"  ASO LOCALIZATION: {profile.get('display_name', app_key)}")
    print(f"{'='*60}")

    for locale_code, entry in localized.items():
        print(f"\n  [{locale_code}] {entry['locale_name']}")
        print(f"    Subtitle:  {entry.get('subtitle', 'N/A')}")
        kw = entry.get("keywords", "")
        print(f"    Keywords:  {kw[:70]}{'...' if len(kw) > 70 else ''}")
        print(f"    Chars:     {len(kw)}/100")

    print(f"\n{'='*60}\n")


def print_competitor_report(competitor_data: dict) -> None:
    """Print parsed competitor data summary."""
    print(f"\n{'='*60}")
    print("  COMPETITOR DATA SUMMARY")
    print(f"{'='*60}\n")

    for name, data in competitor_data.items():
        cat = data.get("category", "Unknown")
        price = data.get("pricing", "N/A")
        rating = data.get("rating", "N/A")
        rev = data.get("revenue", "N/A")
        complaints = len(data.get("complaints", []))
        print(f"  {name:20s} | {cat:20s} | {str(price):25s} | Rating: {rating} | Rev: {rev} | {complaints} complaints")

    print(f"\n{'='*60}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def resolve_app_key(name: str) -> Optional[str]:
    """Fuzzy-match an app key."""
    clean = name.lower().replace("-", "").replace("_", "").replace(" ", "")
    for key in APP_KEYWORD_PROFILES:
        if key == clean or key.startswith(clean) or clean in key:
            return key
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="App Store ASO Optimizer - keyword optimization, localization, tracking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s --optimize focuslock          Optimize keywords for FocusLock
  %(prog)s --keywords sleepmaxx          Show current keyword string
  %(prog)s --localize hilal              Generate localized metadata
  %(prog)s --track focuslock             Record keyword tracking snapshot
  %(prog)s --all-apps                    Optimize all apps
  %(prog)s --competitors                 Show competitor data summary
""",
    )

    parser.add_argument("--optimize", metavar="APP", help="Optimize ASO keywords for APP")
    parser.add_argument("--keywords", metavar="APP", help="Show optimized keyword string for APP")
    parser.add_argument("--localize", metavar="APP", help="Generate localized metadata for APP")
    parser.add_argument("--track", metavar="APP", help="Record keyword tracking snapshot for APP")
    parser.add_argument("--all-apps", action="store_true", help="Run optimization for all apps")
    parser.add_argument("--competitors", action="store_true", help="Show competitor data summary")
    parser.add_argument("--export", action="store_true", help="Export results to JSON files")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    competitor_data = parse_competitor_data()

    if args.competitors:
        print_competitor_report(competitor_data)
        return

    if args.all_apps:
        ASO_DATA_DIR.mkdir(parents=True, exist_ok=True)
        for app_key in APP_KEYWORD_PROFILES:
            result = optimize_keywords(app_key, competitor_data)
            print_optimization_report(result)
            if args.export:
                out_file = safe_path(ASO_DATA_DIR / f"{app_key}_aso.json")
                out_file.write_text(json.dumps(result, indent=2))
                print(f"  Exported: {out_file}")
        return

    if args.optimize:
        app_key = resolve_app_key(args.optimize)
        if not app_key:
            print(f"Unknown app: {args.optimize}")
            print(f"Available: {', '.join(APP_KEYWORD_PROFILES.keys())}")
            sys.exit(1)
        result = optimize_keywords(app_key, competitor_data)
        print_optimization_report(result)
        if args.export:
            ASO_DATA_DIR.mkdir(parents=True, exist_ok=True)
            out_file = safe_path(ASO_DATA_DIR / f"{app_key}_aso.json")
            out_file.write_text(json.dumps(result, indent=2))
            print(f"  Exported: {out_file}")

    if args.keywords:
        app_key = resolve_app_key(args.keywords)
        if not app_key:
            print(f"Unknown app: {args.keywords}")
            sys.exit(1)
        result = optimize_keywords(app_key, competitor_data)
        profile = APP_KEYWORD_PROFILES[app_key]
        print(f"\n  {profile['display_name']} keywords ({result['char_count']}/100 chars):")
        print(f"  {result['keyword_string']}\n")

    if args.localize:
        app_key = resolve_app_key(args.localize)
        if not app_key:
            print(f"Unknown app: {args.localize}")
            sys.exit(1)
        localized = generate_localized_metadata(app_key)
        print_localization_report(app_key, localized)
        if args.export:
            ASO_DATA_DIR.mkdir(parents=True, exist_ok=True)
            out_file = safe_path(ASO_DATA_DIR / f"{app_key}_localized.json")
            out_file.write_text(json.dumps(localized, indent=2, ensure_ascii=False))
            print(f"  Exported: {out_file}")

    if args.track:
        app_key = resolve_app_key(args.track)
        if not app_key:
            print(f"Unknown app: {args.track}")
            sys.exit(1)
        track_keywords(app_key)


if __name__ == "__main__":
    main()
