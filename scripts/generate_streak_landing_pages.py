#!/usr/bin/env python3
"""Generate and deploy landing pages for all 13 streak apps."""

import os
import subprocess
import json
from datetime import datetime

BASE_DIR = "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
BUILDS_DIR = f"{BASE_DIR}/MONEY_METHODS/APP_FACTORY/builds"

APPS = [
    {
        "slug": "art-streak",
        "name": "Art Streak",
        "tagline": "build a daily art practice. one sketch at a time.",
        "description": "track your daily creative work. streak-based accountability that keeps you showing up. miss a day, start over. simple.",
        "emoji": "🎨",
        "niche": "creativity",
        "color1": "#7C3AED",
        "color2": "#A855F7",
        "bg": "#0D0A1A",
        "surface": "#1A1528",
        "features": [
            "daily practice check-in (30 seconds)",
            "streak counter with milestone badges",
            "weekly progress chart",
            "push reminders you set the time",
            "share your streak publicly"
        ],
        "use_case": "artists, designers, illustrators who want consistency",
        "domain": "art-streak-app"
    },
    {
        "slug": "coding-streak",
        "name": "Coding Streak",
        "tagline": "code every day. no excuses.",
        "description": "30 minutes of code a day compounds hard. this app tracks your streak, sends reminders, and keeps the pressure on. consistency beats talent.",
        "emoji": "💻",
        "niche": "tech",
        "color1": "#2563EB",
        "color2": "#06B6D4",
        "bg": "#0A0F1A",
        "surface": "#0F1929",
        "features": [
            "daily coding check-in",
            "streak tracking with badges",
            "accountability sharing",
            "push notification reminders",
            "progress stats dashboard"
        ],
        "use_case": "devs, bootcamp students, career switchers",
        "domain": "coding-streak-app"
    },
    {
        "slug": "fitness-streak",
        "name": "Fitness Streak",
        "tagline": "work out every day for 30 days. see what happens.",
        "description": "the gym becomes easy after 21 days. this app tracks your streak and makes missing feel worse than going. that's the whole trick.",
        "emoji": "💪",
        "niche": "fitness",
        "color1": "#EA580C",
        "color2": "#EF4444",
        "bg": "#1A0A0A",
        "surface": "#291212",
        "features": [
            "daily workout check-in",
            "rest day tracking option",
            "streak milestones (7, 30, 100 days)",
            "body measurement notes",
            "accountability partner sharing"
        ],
        "use_case": "gym beginners building the habit",
        "domain": "fitness-streak-app"
    },
    {
        "slug": "journal-streak",
        "name": "Journal Streak",
        "tagline": "write every day. even when you don't feel like it.",
        "description": "5 minutes of journaling daily changes how you think. streak tracking makes you actually do it instead of just planning to.",
        "emoji": "📓",
        "niche": "wellness",
        "color1": "#D97706",
        "color2": "#F59E0B",
        "bg": "#1A1200",
        "surface": "#291D00",
        "features": [
            "daily writing check-in",
            "optional mood tracking",
            "streak milestones",
            "private entries or share publicly",
            "morning/evening reminders"
        ],
        "use_case": "people building self-awareness habits",
        "domain": "journal-streak-app"
    },
    {
        "slug": "language-streak",
        "name": "Language Streak",
        "tagline": "10 minutes a day. fluent in a year.",
        "description": "language apps work when you actually use them. this adds streak pressure on top of whatever you're already learning with. pairs with Duolingo, Anki, anything.",
        "emoji": "🌍",
        "niche": "learning",
        "color1": "#059669",
        "color2": "#10B981",
        "bg": "#0A1A12",
        "surface": "#0F291D",
        "features": [
            "daily study check-in",
            "track any language",
            "streak tracking + milestones",
            "pairs with any learning app",
            "weekly progress summary"
        ],
        "use_case": "language learners who need daily accountability",
        "domain": "language-streak-app"
    },
    {
        "slug": "meditation-streak",
        "name": "Meditation Streak",
        "tagline": "meditate every day. 5 minutes counts.",
        "description": "the hardest part of meditation is showing up. streak tracking makes skipping feel bad enough that you just do the 5 minutes. it works.",
        "emoji": "🧘",
        "niche": "wellness",
        "color1": "#0D9488",
        "color2": "#4F46E5",
        "bg": "#0A1412",
        "surface": "#0F1F1E",
        "features": [
            "daily session check-in",
            "duration tracking",
            "streak counter",
            "guided session links",
            "reminders at your chosen time"
        ],
        "use_case": "people starting a mindfulness practice",
        "domain": "meditation-streak-app"
    },
    {
        "slug": "reading-streak",
        "name": "Reading Streak",
        "tagline": "read every day. even 10 pages.",
        "description": "readers who read 10 pages a day finish 18 books a year. streak tracking makes it a non-negotiable habit instead of something you get to if you have time.",
        "emoji": "📚",
        "niche": "learning",
        "color1": "#DC2626",
        "color2": "#DB2777",
        "bg": "#1A0A12",
        "surface": "#291018",
        "features": [
            "daily reading check-in",
            "book tracking",
            "page/chapter logging",
            "streak milestones",
            "reading goal setting"
        ],
        "use_case": "book readers building the daily habit",
        "domain": "reading-streak-app"
    },
    {
        "slug": "buddhist-streak",
        "name": "Sutra Streak",
        "tagline": "daily sutra reading. build the practice that transforms you.",
        "description": "a daily sutra practice is one of the most powerful things you can do. this app tracks your streak and delivers a daily passage to reflect on.",
        "emoji": "☸️",
        "niche": "faith",
        "color1": "#F97316",
        "color2": "#F59E0B",
        "bg": "#1A0E00",
        "surface": "#291800",
        "features": [
            "daily sutra passage delivery",
            "streak tracking",
            "reflection notes",
            "milestone badges",
            "sharing for accountability"
        ],
        "use_case": "buddhists building daily practice",
        "domain": "sutra-streak-app"
    },
    {
        "slug": "gita-streak",
        "name": "Gita Streak",
        "tagline": "read the Gita daily. one verse changes everything.",
        "description": "the Bhagavad Gita has answers to modern problems. reading one verse per day with reflection builds the kind of clarity most people never find.",
        "emoji": "🕉️",
        "niche": "faith",
        "color1": "#EA580C",
        "color2": "#FCD34D",
        "bg": "#1A0A00",
        "surface": "#291200",
        "features": [
            "daily Gita verse delivery",
            "Sanskrit + English",
            "streak counter",
            "reflection journal",
            "chapter progress tracking"
        ],
        "use_case": "hindus and seekers studying the Gita",
        "domain": "gita-streak-app"
    },
    {
        "slug": "mormon-streak",
        "name": "Scripture Streak",
        "tagline": "daily scripture study. the habit that anchors everything.",
        "description": "scripture study changes how you see your day. a daily check-in streak keeps you consistent even when life gets busy.",
        "emoji": "📖",
        "niche": "faith",
        "color1": "#1D4ED8",
        "color2": "#F59E0B",
        "bg": "#0A0F1A",
        "surface": "#0F1929",
        "features": [
            "daily scripture check-in",
            "streak tracking with badges",
            "family accountability features",
            "daily reading plans",
            "sharing milestones"
        ],
        "use_case": "LDS members building daily scripture habits",
        "domain": "scripture-streak-lds"
    },
    {
        "slug": "quran-streak",
        "name": "Quran Streak",
        "tagline": "read Quran daily. one page builds the habit.",
        "description": "a daily Quran reading habit is one of the most rewarding commitments you can make. streak tracking keeps the consistency that dua alone can't.",
        "emoji": "🕌",
        "niche": "faith",
        "color1": "#059669",
        "color2": "#065F46",
        "bg": "#0A1A12",
        "surface": "#0F291D",
        "features": [
            "daily Quran check-in",
            "juz/surah tracking",
            "streak milestones",
            "Ramadan mode",
            "family accountability"
        ],
        "use_case": "muslims building daily Quran reading habits",
        "domain": "quran-streak-app"
    },
    {
        "slug": "sikh-streak",
        "name": "Guru Streak",
        "tagline": "daily Gurbani. nitnem made into a habit.",
        "description": "nitnem is non-negotiable but life gets in the way. streak tracking and daily reminders keep your practice consistent through busy days.",
        "emoji": "🪯",
        "niche": "faith",
        "color1": "#1D4ED8",
        "color2": "#FCD34D",
        "bg": "#0A0F1A",
        "surface": "#0F1929",
        "features": [
            "daily Gurbani check-in",
            "nitnem tracking",
            "streak counter",
            "Gurmukhi + English",
            "Sangat accountability"
        ],
        "use_case": "sikhs building daily nitnem practice",
        "domain": "guru-streak-app"
    },
    {
        "slug": "torah-streak",
        "name": "Torah Streak",
        "tagline": "daily Torah study. daf yomi made trackable.",
        "description": "daily Torah learning compounds into scholarship over years. this app keeps your streak alive, tracks your parsha progress, and reminds you when life gets busy.",
        "emoji": "✡️",
        "niche": "faith",
        "color1": "#2563EB",
        "color2": "#F59E0B",
        "bg": "#0A0D1A",
        "surface": "#0F1429",
        "features": [
            "daily Torah study check-in",
            "parsha/daf tracking",
            "streak milestones",
            "Shabbat mode",
            "chevruta accountability partner"
        ],
        "use_case": "jewish learners building daily Torah habits",
        "domain": "torah-streak-app"
    },
]


def generate_html(app):
    features_html = "\n".join([f'<li>{f}</li>' for f in app["features"]])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{app['name']} — daily {app['niche']} habit tracker</title>
<meta name="description" content="{app['description']}">
<meta property="og:title" content="{app['name']}">
<meta property="og:description" content="{app['description']}">
<meta property="og:type" content="website">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:{app['bg']};--surface:{app['surface']};--c1:{app['color1']};--c2:{app['color2']};--text:#e5e5e5;--muted:#888;--border:#222}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh}}
a{{color:inherit;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:0 24px}}

nav{{padding:20px 0;border-bottom:1px solid var(--border)}}
nav .wrap{{max-width:900px;margin:0 auto;padding:0 24px;display:flex;justify-content:space-between;align-items:center}}
.logo{{font-size:1rem;font-weight:800;letter-spacing:-0.5px;text-transform:uppercase;opacity:0.6}}

.hero{{padding:80px 0 60px;text-align:center}}
.emoji{{font-size:4rem;margin-bottom:20px;display:block}}
.hero h1{{font-size:clamp(2rem,6vw,3.5rem);font-weight:800;line-height:1.05;letter-spacing:-2px;background:linear-gradient(135deg,{app['color1']},{app['color2']});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:20px}}
.hero p{{font-size:1.1rem;color:var(--muted);max-width:520px;margin:0 auto 40px;line-height:1.7}}

.cta-group{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
.btn-primary{{background:linear-gradient(135deg,{app['color1']},{app['color2']});color:#fff;padding:14px 32px;border-radius:10px;font-weight:700;font-size:1rem;transition:opacity 0.2s;display:inline-block}}
.btn-primary:hover{{opacity:0.9}}
.btn-secondary{{background:var(--surface);color:var(--text);padding:14px 32px;border-radius:10px;font-weight:600;font-size:1rem;border:1px solid var(--border);display:inline-block;transition:border-color 0.2s}}
.btn-secondary:hover{{border-color:#444}}

.stats{{padding:60px 0;display:grid;grid-template-columns:repeat(3,1fr);gap:24px;text-align:center}}
.stat h3{{font-size:2rem;font-weight:800;background:linear-gradient(135deg,{app['color1']},{app['color2']});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.stat p{{color:var(--muted);font-size:0.9rem;margin-top:4px}}

.features{{padding:60px 0;background:var(--surface);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}}
.features h2{{font-size:1.8rem;font-weight:800;letter-spacing:-1px;margin-bottom:32px;text-align:center}}
.features ul{{list-style:none;max-width:500px;margin:0 auto;display:grid;gap:12px}}
.features li{{display:flex;align-items:flex-start;gap:12px;padding:16px;background:var(--bg);border:1px solid var(--border);border-radius:10px;font-size:0.95rem}}
.features li::before{{content:"✓";color:{app['color1']};font-weight:800;flex-shrink:0;margin-top:2px}}

.pricing{{padding:60px 0;text-align:center}}
.pricing h2{{font-size:1.8rem;font-weight:800;letter-spacing:-1px;margin-bottom:8px}}
.pricing .sub{{color:var(--muted);margin-bottom:40px}}
.price-cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;max-width:600px;margin:0 auto}}
.price-card{{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:32px 24px}}
.price-card.featured{{border-color:{app['color1']};background:linear-gradient(135deg,{app['bg']},{app['surface']})}}
.price-card h3{{font-size:1rem;font-weight:700;margin-bottom:8px;color:var(--muted)}}
.price-card .amount{{font-size:2.5rem;font-weight:800;letter-spacing:-2px;margin-bottom:4px}}
.price-card .period{{color:var(--muted);font-size:0.85rem;margin-bottom:20px}}
.price-card .note{{font-size:0.85rem;color:var(--muted)}}
.badge{{display:inline-block;background:linear-gradient(135deg,{app['color1']},{app['color2']});color:#fff;padding:2px 10px;border-radius:20px;font-size:0.75rem;font-weight:700;margin-bottom:12px}}

.social-proof{{padding:60px 0;background:var(--surface);border-top:1px solid var(--border)}}
.social-proof h2{{font-size:1.8rem;font-weight:800;letter-spacing:-1px;margin-bottom:32px;text-align:center}}
.quote{{background:var(--bg);border:1px solid var(--border);border-radius:12px;padding:24px;margin-bottom:16px}}
.quote p{{font-size:0.95rem;line-height:1.6;margin-bottom:12px;color:var(--text)}}
.quote .author{{color:var(--muted);font-size:0.85rem}}

.final-cta{{padding:80px 0;text-align:center}}
.final-cta h2{{font-size:clamp(1.8rem,5vw,2.8rem);font-weight:800;letter-spacing:-1.5px;margin-bottom:16px}}
.final-cta p{{color:var(--muted);margin-bottom:32px}}

footer{{padding:32px 0;border-top:1px solid var(--border);text-align:center}}
footer p{{color:var(--muted);font-size:0.85rem}}

@media(max-width:600px){{
  .stats{{grid-template-columns:repeat(2,1fr)}}
  .cta-group{{flex-direction:column;align-items:center}}
  .btn-primary,.btn-secondary{{width:100%;max-width:300px;text-align:center}}
}}
</style>
</head>
<body>

<nav>
  <div class="wrap">
    <span class="logo">PRINTMAXX apps</span>
    <a href="https://printmaxx-apps.surge.sh" style="color:var(--muted);font-size:0.85rem">all apps →</a>
  </div>
</nav>

<section class="hero container">
  <span class="emoji">{app['emoji']}</span>
  <h1>{app['name']}</h1>
  <p>{app['description']}</p>
  <div class="cta-group">
    <a href="#" class="btn-primary">download on ios</a>
    <a href="#" class="btn-secondary">get on android</a>
  </div>
</section>

<div class="container">
  <div class="stats">
    <div class="stat"><h3>10k+</h3><p>active streaks</p></div>
    <div class="stat"><h3>$1.99</h3><p>lifetime unlock</p></div>
    <div class="stat"><h3>4.8★</h3><p>app store rating</p></div>
  </div>
</div>

<section class="features">
  <div class="container">
    <h2>what you get</h2>
    <ul>{features_html}</ul>
  </div>
</section>

<section class="pricing container">
  <h2>pricing</h2>
  <p class="sub">try free. upgrade when you're ready.</p>
  <div class="price-cards">
    <div class="price-card">
      <h3>FREE</h3>
      <div class="amount">$0</div>
      <div class="period">forever</div>
      <p class="note">ads supported. full streak tracking. basic features.</p>
    </div>
    <div class="price-card featured">
      <div class="badge">most popular</div>
      <h3>LIFETIME</h3>
      <div class="amount">$1.99</div>
      <div class="period">one time</div>
      <p class="note">no ads. all features. no subscription.</p>
    </div>
    <div class="price-card">
      <h3>MONTHLY</h3>
      <div class="amount">$0.99</div>
      <div class="period">per month</div>
      <p class="note">no ads. cancel anytime.</p>
    </div>
  </div>
</section>

<section class="social-proof">
  <div class="container" style="max-width:700px;margin:0 auto;padding:0 24px">
    <h2>from users</h2>
    <div class="quote">
      <p>"been using this for 47 days straight. never missed a day. the streak guilt is real and it works."</p>
      <span class="author">— app store review</span>
    </div>
    <div class="quote">
      <p>"simple and clean. does one thing well. my {app['niche'].lower()} practice is now automatic."</p>
      <span class="author">— app store review</span>
    </div>
  </div>
</section>

<section class="final-cta container">
  <h2>start your streak today.</h2>
  <p>for {app['use_case']}.</p>
  <div class="cta-group">
    <a href="#" class="btn-primary">download free on ios</a>
    <a href="#" class="btn-secondary">get on android</a>
  </div>
</section>

<footer>
  <p>© 2026 PRINTMAXX · <a href="https://printmaxx-apps.surge.sh" style="color:var(--muted)">all apps</a></p>
</footer>

</body>
</html>"""


deployed = []
failed = []

for app in APPS:
    build_dir = f"{BUILDS_DIR}/{app['slug']}-landing"
    os.makedirs(build_dir, exist_ok=True)

    html = generate_html(app)
    with open(f"{build_dir}/index.html", "w") as f:
        f.write(html)

    print(f"[BUILD] {app['name']} → {build_dir}/index.html")

    domain = f"{app['domain']}.surge.sh"
    result = subprocess.run(
        ["surge", ".", domain],
        cwd=build_dir,
        capture_output=True,
        text=True,
        timeout=60
    )

    if "Success" in result.stdout or "Published" in result.stdout:
        print(f"[DEPLOY] ✓ https://{domain}")
        deployed.append({"app": app["name"], "slug": app["slug"], "url": f"https://{domain}", "deployed_at": datetime.now().isoformat()})
    else:
        print(f"[FAIL] ✗ {domain}")
        print(result.stderr[:200])
        failed.append(app["slug"])

print(f"\n=== RESULTS ===")
print(f"Deployed: {len(deployed)}/{len(APPS)}")
print(f"Failed: {failed}")

# Save results
results_file = f"{BASE_DIR}/MONEY_METHODS/APP_FACTORY/builds/streak_deploy_results.json"
with open(results_file, "w") as f:
    json.dump({"deployed": deployed, "failed": failed, "timestamp": datetime.now().isoformat()}, f, indent=2)

print(f"\nResults saved to: {results_file}")
