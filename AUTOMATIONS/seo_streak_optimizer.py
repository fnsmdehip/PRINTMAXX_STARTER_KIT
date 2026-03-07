#!/usr/bin/env python3
"""Batch SEO optimizer for streak landing pages — injects missing OG/Twitter/canonical/JSON-LD tags."""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

STREAK_CONFIGS = [
    {
        "dir": "quran-streak-landing",
        "url": "https://quran-streak-app.surge.sh/",
        "name": "Quran Streak",
        "keywords": "quran reading streak, daily quran habit tracker, quran streak app, islamic habit tracker, muslim habit builder, daily quran app, quran reading consistency",
        "category": "LifestyleApplication",
        "twitter_desc": "track your daily Quran reading. streak keeps you consistent when dua alone can't.",
    },
    {
        "dir": "coding-streak-landing",
        "url": "https://coding-streak-app.surge.sh/",
        "name": "Coding Streak",
        "keywords": "daily coding streak app, code every day challenge, coding habit tracker, developer habit app, 100 days of code tracker, programming streak app, daily coding habit",
        "category": "ProductivityApplication",
        "twitter_desc": "30 minutes of code a day compounds hard. streak tracker keeps the pressure on.",
    },
    {
        "dir": "fitness-streak-landing",
        "url": "https://fitness-streak-app.surge.sh/",
        "name": "Fitness Streak",
        "keywords": "fitness streak app, daily workout tracker, gym habit app, exercise streak tracker, workout consistency app, daily fitness habit, workout habit tracker",
        "category": "HealthApplication",
        "twitter_desc": "miss a workout? start over. streak tracker that makes skipping feel worse than going.",
    },
    {
        "dir": "meditation-streak-landing",
        "url": "https://meditation-streak-app.surge.sh/",
        "name": "Meditation Streak",
        "keywords": "meditation streak app, daily meditation tracker, mindfulness habit app, meditation consistency app, daily mindfulness tracker, meditation habit builder, wellness streak tracker",
        "category": "HealthApplication",
        "twitter_desc": "5 minutes of meditation daily. streak tracking makes showing up non-negotiable.",
    },
    {
        "dir": "reading-streak-landing",
        "url": "https://reading-streak-app.surge.sh/",
        "name": "Reading Streak",
        "keywords": "reading streak app, daily reading habit tracker, read every day app, book reading tracker, reading consistency app, daily reading challenge, reading habit builder",
        "category": "EducationApplication",
        "twitter_desc": "10 pages a day = 18 books a year. streak tracker makes it non-negotiable.",
    },
    {
        "dir": "journal-streak-landing",
        "url": "https://journal-streak-app.surge.sh/",
        "name": "Journal Streak",
        "keywords": "journaling streak app, daily journal habit tracker, journaling habit app, journal every day, daily writing streak, journaling consistency app, habit journal app",
        "category": "LifestyleApplication",
        "twitter_desc": "5 minutes of journaling daily. streak tracking makes you actually do it.",
    },
    {
        "dir": "language-streak-landing",
        "url": "https://language-streak-app.surge.sh/",
        "name": "Language Streak",
        "keywords": "language learning streak app, daily language habit tracker, duolingo streak alternative, language study tracker, daily language practice app, foreign language habit, learn language daily app",
        "category": "EducationApplication",
        "twitter_desc": "pairs with Duolingo, Anki, anything. adds streak pressure on top of your existing routine.",
    },
    {
        "dir": "art-streak-landing",
        "url": "https://art-streak-app.surge.sh/",
        "name": "Art Streak",
        "keywords": "daily art practice streak, drawing streak app, creative habit tracker, art every day app, daily drawing habit, artist habit tracker, creative consistency app",
        "category": "LifestyleApplication",
        "twitter_desc": "daily art practice tracker. miss a day, start over. simple streak accountability.",
    },
    {
        "dir": "buddhist-streak-landing",
        "url": "https://sutra-streak-app.surge.sh/",
        "name": "Sutra Streak",
        "keywords": "buddhist sutra streak app, daily sutra reading tracker, buddhist habit app, dharma daily practice, sutra study app, buddhist practice tracker, daily meditation sutra",
        "category": "LifestyleApplication",
        "twitter_desc": "daily sutra practice tracker. streak keeps the consistency a sitting alone can't.",
    },
    {
        "dir": "torah-streak-landing",
        "url": "https://torah-streak-app.surge.sh/",
        "name": "Torah Streak",
        "keywords": "daily torah learning app, torah streak tracker, jewish study habit app, parsha tracker, daily torah study, torah learning consistency, jewish habit tracker, daf yomi app",
        "category": "LifestyleApplication",
        "twitter_desc": "daily Torah learning + parsha progress tracking. scholarship compounds over years.",
    },
    {
        "dir": "sikh-streak-landing",
        "url": "https://guru-streak-app.surge.sh/",
        "name": "Guru Streak",
        "keywords": "nitnem streak app, sikh daily prayer tracker, gurbani streak app, sikh habit tracker, daily nitnem reminder, gurbani reading app, sikh prayer consistency app",
        "category": "LifestyleApplication",
        "twitter_desc": "nitnem streak tracker. daily reminders to keep your practice consistent.",
    },
    {
        "dir": "mormon-streak-landing",
        "url": "https://scripture-streak-lds.surge.sh/",
        "name": "Scripture Streak",
        "keywords": "lds scripture reading app, book of mormon streak, daily scripture study app, lds habit tracker, scripture study consistency, latter day saints app, come follow me tracker",
        "category": "LifestyleApplication",
        "twitter_desc": "daily scripture study streak for LDS members. consistent study changes how you see your day.",
    },
    {
        "dir": "gita-streak-landing",
        "url": "https://gita-streak-app.surge.sh/",
        "name": "Gita Streak",
        "keywords": "bhagavad gita daily reading app, gita streak tracker, hindu habit app, daily gita verse app, bhagavad gita study tracker, gita reading consistency, hindu scripture habit app",
        "category": "LifestyleApplication",
        "twitter_desc": "one Gita verse per day with reflection. clarity most people never find.",
    },
]

BUILDS_DIR = PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY" / "builds"

def safe_path(p: Path) -> Path:
    resolved = p.resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} outside project root")
    return resolved

def build_seo_block(cfg: dict) -> str:
    url = cfg["url"]
    name = cfg["name"]
    keywords = cfg["keywords"]
    category = cfg["category"]
    twitter_desc = cfg["twitter_desc"]
    # Read og:description from the existing file to reuse it
    return f"""<meta name="keywords" content="{keywords}">
<meta name="robots" content="index, follow">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{name}">
<meta property="og:image" content="{url}og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@printmaxxer">
<meta name="twitter:title" content="{name}">
<meta name="twitter:description" content="{twitter_desc}">
<meta name="twitter:image" content="{url}og-image.png">
<link rel="canonical" href="{url}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"MobileApplication","name":"{name}","url":"{url}","applicationCategory":"{category}","operatingSystem":"iOS, Android","offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}
</script>"""

def process_file(cfg: dict) -> bool:
    filepath = safe_path(BUILDS_DIR / cfg["dir"] / "index.html")
    if not filepath.exists():
        print(f"  SKIP (not found): {cfg['dir']}")
        return False

    content = filepath.read_text(encoding="utf-8")

    # Check if already fully upgraded
    if 'twitter:card' in content and 'canonical' in content:
        print(f"  ALREADY DONE: {cfg['dir']}")
        return False

    anchor = '<meta property="og:type" content="website">'
    if anchor not in content:
        print(f"  WARN: anchor not found in {cfg['dir']}")
        return False

    seo_block = build_seo_block(cfg)
    new_content = content.replace(anchor, anchor + "\n" + seo_block, 1)
    filepath.write_text(new_content, encoding="utf-8")
    print(f"  DONE: {cfg['dir']}")
    return True

if __name__ == "__main__":
    updated = 0
    for cfg in STREAK_CONFIGS:
        if process_file(cfg):
            updated += 1
    print(f"\nUpdated {updated}/{len(STREAK_CONFIGS)} streak landing pages.")
