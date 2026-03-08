#!/usr/bin/env python3
"""
PRINTMAXX Decision Engine — Closed-Loop Autonomous Business Agent

Replaces the old "scan → CSV → nothing" pattern with:
scan → analyze → decide → act → log → learn

Runs as a persistent daemon. Each cycle:
1. Reads all data sources (CSVs, logs, output dirs)
2. Scores opportunities using configurable thresholds
3. Takes action (generate listings, draft responses, create content, deploy)
4. Logs every decision with reasoning for audit trail
5. Updates progress trackers

Uses Claude Agent SDK when LLM judgment is needed.
Falls back to rule-based decisions for simple threshold checks.

Usage:
  python3 AUTOMATIONS/decision_engine.py --cycle          # Run one decision cycle
  python3 AUTOMATIONS/decision_engine.py --daemon         # Run continuously (every 30min)
  python3 AUTOMATIONS/decision_engine.py --status         # Show pipeline status
  python3 AUTOMATIONS/decision_engine.py --dry-run        # Show what would happen without acting
  python3 AUTOMATIONS/decision_engine.py --fix-broken     # Diagnose and fix broken cron jobs
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# === SAFETY ===
PROJECT_ROOT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
DECISION_LOG = PROJECT_ROOT / "AUTOMATIONS" / "logs" / "decision_engine.log"
DECISION_LEDGER = PROJECT_ROOT / "LEDGER" / "DECISIONS.csv"
OUTPUT_DIR = PROJECT_ROOT / "ralph" / "loops" / "spreadsheet_buildout" / "output"

def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root")
    return resolved

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    with open(DECISION_LOG, "a") as f:
        f.write(line + "\n")

def log_decision(source, action, reasoning, outcome="PENDING"):
    """Append to decisions ledger for full audit trail."""
    safe_path(DECISION_LEDGER)
    row = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "action": action,
        "reasoning": reasoning,
        "outcome": outcome,
    }
    exists = DECISION_LEDGER.exists()
    with open(DECISION_LEDGER, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=row.keys())
        if not exists:
            w.writeheader()
        w.writerow(row)


# === DATA READERS ===

def read_csv_tail(filepath, n=50):
    """Read last N rows of a CSV file."""
    p = safe_path(filepath)
    if not p.exists():
        return []
    rows = []
    with open(p, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            if len(rows) > n * 2:
                rows = rows[-n:]
    return rows[-n:]

def count_csv_rows(filepath):
    p = safe_path(filepath)
    if not p.exists():
        return 0
    with open(p, "r") as f:
        return sum(1 for _ in f) - 1  # minus header


# === DECISION MODULES ===

class FreelancePipeline:
    """Process freelance demand scan results into actionable responses."""

    SOURCE = PROJECT_ROOT / "LEDGER" / "FREELANCE_DEMAND_SCAN.csv"
    OUTPUT = PROJECT_ROOT / "CONTENT" / "freelance_responses"

    # Services we can deliver with Claude Max (mirrors auto_freelance_responder.py)
    SERVICES = {
        "website": {
            "name": "Website / Landing Page",
            "delivery": "24-48h",
            "price_floor": 99,
            "pitch": "i build modern, responsive sites. can share a quick sample mockup for your niche",
            "portfolio": ["dental-motion.surge.sh", "realtor-motion.surge.sh", "restaurant-motion.surge.sh"],
        },
        "automation": {
            "name": "Automation / Scripts / Bots",
            "delivery": "12-24h",
            "price_floor": 79,
            "pitch": "i build automation workflows (Python, APIs, data pipelines) and can ship a working script fast",
            "portfolio": [],
        },
        "data_entry": {
            "name": "Data Entry / Research / VA Work",
            "delivery": "same day",
            "price_floor": 15,
            "pitch": "i use AI-assisted workflows to move fast while keeping accuracy high. can do a small sample first",
            "portfolio": [],
        },
        "logo": {
            "name": "Logo / Graphic Design",
            "delivery": "24h",
            "price_floor": 50,
            "pitch": "i do logo design. 3-5 concepts in 24h, unlimited revisions included",
            "portfolio": [],
        },
        "social_media": {
            "name": "Social Media Management",
            "delivery": "ongoing",
            "price_floor": 200,
            "pitch": "i can set up a content pipeline and provide a 7-day plan with sample posts in your tone",
            "portfolio": [],
        },
        "scraper": {
            "name": "Web Scraper / Data Extraction",
            "delivery": "12-24h",
            "price_floor": 79,
            "pitch": "i build scrapers that run on a schedule. can deliver working code plus sample output quickly",
            "portfolio": ["sitescore-app.surge.sh"],
        },
        "video_editing": {
            "name": "Video Editing / Clipping",
            "delivery": "24-48h",
            "price_floor": 50,
            "pitch": "i do short-form edits and stream clips. fast turnaround with captions and hooks baked in",
            "portfolio": [],
        },
        "cold_email": {
            "name": "Cold Email / Outreach",
            "delivery": "24h",
            "price_floor": 50,
            "pitch": "i write cold email sequences that actually get replies. can share sample sequences and results",
            "portfolio": [],
        },
    }

    def analyze(self, dry_run=False):
        rows = read_csv_tail(self.SOURCE, 100)
        if not rows:
            log("Freelance: No data found")
            return []

        actions = []
        for row in rows:
            score = float(row.get("score", row.get("relevance_score", 0)) or 0)
            title = row.get("title", row.get("post_title", "unknown"))
            url = row.get("url", row.get("post_url", ""))
            subreddit = row.get("source", row.get("subreddit", "unknown"))
            processed = row.get("processed", row.get("response_generated", ""))
            budget = row.get("budget", "N/A")
            matched_services = row.get("matched_services", "")
            delivery_time = row.get("delivery_time", "")
            body_preview = row.get("body_preview", "")

            if score >= 60 and not processed:
                action = {
                    "type": "freelance_response",
                    "title": title,
                    "url": url,
                    "subreddit": subreddit,
                    "score": score,
                    "budget": budget,
                    "matched_services": matched_services,
                    "delivery_time": delivery_time,
                    "body_preview": body_preview,
                    "reasoning": f"Score {score} >= 60 threshold. Subreddit: {subreddit}",
                }
                actions.append(action)

        hot = [a for a in actions if a["score"] >= 80]
        warm = [a for a in actions if 60 <= a["score"] < 80]

        log(f"Freelance: {len(hot)} HOT, {len(warm)} WARM opportunities from last 100 rows")

        if not dry_run and (hot or warm):
            self._generate_responses(hot[:5] + warm[:3])

        return actions

    def _match_service(self, opp):
        """Match opportunity to best service based on title and matched_services field."""
        services_str = opp.get("matched_services", "")
        title = opp.get("title", "").lower()
        body = opp.get("body_preview", "").lower()
        combined = f"{title} {body} {services_str}"

        # Check each service for keyword match
        for svc_key in self.SERVICES:
            if svc_key in services_str:
                return svc_key
            svc_name_lower = self.SERVICES[svc_key]["name"].lower()
            if any(kw in combined for kw in svc_name_lower.split("/")):
                return svc_key

        # Keyword fallback
        keyword_map = {
            "website": ["website", "web dev", "landing page", "html", "css", "react", "next"],
            "logo": ["logo", "branding", "graphic design", "design", "label", "card"],
            "automation": ["automation", "bot", "script", "python", "engineer", "developer"],
            "scraper": ["scraper", "scraping", "data extraction", "crawl"],
            "social_media": ["social media", "tiktok", "instagram", "content creator", "faceless"],
            "video_editing": ["video edit", "clip", "editor", "short-form", "youtube"],
            "data_entry": ["data entry", "research", "va ", "virtual assistant", "typing"],
            "cold_email": ["cold email", "outreach", "lead gen", "email specialist"],
        }
        for svc_key, keywords in keyword_map.items():
            if any(kw in combined for kw in keywords):
                return svc_key

        return "website"  # default

    def _build_price_line(self, opp, svc):
        """Build a price/delivery line based on budget and service."""
        import re as _re
        budget_str = opp.get("budget", "N/A")
        delivery = svc["delivery"]
        price_floor = svc["price_floor"]

        if budget_str and budget_str != "N/A":
            try:
                budget_num = int(_re.sub(r'[^\d]', '', str(budget_str)))
                our_price = max(price_floor, int(budget_num * 0.85))
                return f"i can do this for ${our_price}. delivery in {delivery}."
            except (ValueError, TypeError):
                pass
        return f"delivery in {delivery}. pricing depends on scope, but starts at ${price_floor}."

    def _generate_responses(self, opportunities):
        """Generate personalized, copy-paste-ready responses for top opportunities."""
        self.OUTPUT.mkdir(parents=True, exist_ok=True)

        for opp in opportunities:
            slug = opp["title"][:50].replace(" ", "_").replace("/", "_")
            outfile = self.OUTPUT / f"response_{slug}_{datetime.now().strftime('%Y%m%d')}.md"
            if outfile.exists():
                continue

            svc_key = self._match_service(opp)
            svc = self.SERVICES[svc_key]
            price_line = self._build_price_line(opp, svc)

            # Build portfolio section
            portfolio_section = ""
            if svc["portfolio"]:
                links = "\n".join([f"  - https://{url}" for url in svc["portfolio"][:3]])
                portfolio_section = f"\n\nlive examples of my work:\n{links}"

            # Build the actual response (no placeholders, no chatbot artifacts)
            response_text = f"hey, {svc['pitch']}.{portfolio_section}\n\n{price_line}\n\ndm me if you want to see a quick sample before committing. i can put something together in a few hours so you know exactly what you're getting."

            # Quality self-check: reject if response still has placeholders or chatbot artifacts
            quality_problems = []
            if "[" in response_text and "]" in response_text:
                quality_problems.append("contains unfilled [placeholder] brackets")
            for artifact in ["Happy to help", "I hope this helps", "Let me know if you have questions",
                             "Happy to discuss scope and timeline", "I specialize in exactly"]:
                if artifact.lower() in response_text.lower():
                    quality_problems.append(f"contains chatbot artifact: '{artifact}'")
            if quality_problems:
                log(f"Freelance: QUALITY REJECT for '{opp['title'][:30]}': {'; '.join(quality_problems)}", "WARN")
                continue

            content = f"""# Freelance Response Draft
## Post: {opp['title']}
## URL: {opp['url']}
## Subreddit: {opp['subreddit']}
## Score: {opp['score']}
## Budget: {opp.get('budget', 'N/A')}
## Service Match: {svc['name']}
## Generated: {datetime.now().isoformat()}

---

### Response (copy-paste ready)

{response_text}

---

### Follow-Up DM

hey, i left a comment on your post about {svc_key.replace('_', ' ')}. wanted to follow up directly.

i can put together a quick sample based on your requirements. take a look and let me know if the direction works for you.

if you want to move forward, i can have the full deliverable ready in {svc['delivery']}.

---

### Notes for Human Review
- Add your actual portfolio URL before posting
- Check {opp['subreddit']} rules for self-promotion
- Verify budget is still available (post age matters)
- Status: PENDING_REVIEW
"""
            safe_path(outfile)
            outfile.write_text(content)
            log(f"Freelance: Generated response for '{opp['title'][:40]}...' (service: {svc_key})")
            log_decision("freelance_demand", f"draft_response:{slug}", opp["reasoning"])


class EcomArbPipeline:
    """Process ecom arbitrage opportunities into listing drafts."""

    SOURCE = PROJECT_ROOT / "LEDGER" / "ECOM_ARB_OPPORTUNITIES.csv"
    OUTPUT = PROJECT_ROOT / "CONTENT" / "ecom_listings"

    # Product knowledge database: real features, benefits, and copy for each product type.
    # Keyed by normalized product name (lowercase). Each entry has FB and eBay-specific copy.
    PRODUCT_DB = {
        "led face mask": {
            "category": "Beauty & Health",
            "fb_title": "LED Light Therapy Face Mask - 7 Color, Anti-Aging + Acne",
            "ebay_title": "LED Light Therapy Face Mask 7 Color Red Blue Anti-Aging Skin Rejuvenation",
            "features": [
                "7 color modes for different skin concerns (red for anti-aging, blue for acne)",
                "15-20 minute sessions, visible results in 4-6 weeks",
                "USB rechargeable, no batteries needed",
                "Covers full face evenly, not like handheld wands that miss spots",
            ],
            "fb_description": "Professional LED light therapy mask with 7 colors. Red light boosts collagen and reduces fine lines. Blue light kills acne bacteria. Use 15-20 minutes daily.\n\nDermatologists charge $150+ per session for the same technology. This pays for itself after one use vs clinic prices.\n\nUSB rechargeable. Fits any face shape with adjustable strap. Free shipping.",
            "ebay_description": "7-color LED light therapy mask for at-home skin treatment. Red (630nm) for anti-aging and collagen production. Blue (415nm) for acne treatment. Green for pigmentation.\n\n15-20 minute daily sessions. Visible improvement in 4-6 weeks. USB rechargeable. Adjustable fit strap. ABS plastic construction.\n\nFraction of the cost of dermatologist LED sessions ($150+ each).",
        },
        "yoga mat": {
            "category": "Sporting Goods",
            "fb_title": "Extra Thick Yoga Mat - Non-Slip, 72x24, Carrying Strap Included",
            "ebay_title": "Extra Thick Non-Slip Yoga Mat Exercise Fitness Pilates Gym Workout Pad 72x24",
            "features": [
                "10mm thick high-density NBR foam, protects knees and joints",
                "Non-slip surface on both sides",
                "72x24 inches, fits any height",
                "Includes carrying strap",
            ],
            "fb_description": "10mm thick yoga mat with non-slip surface on both sides. Most mats are 4-6mm and your knees feel the floor. This one actually cushions.\n\n72x24 inches. Works for yoga, pilates, stretching, and floor exercises. Includes carrying strap.\n\nEasy to clean with soap and water. Free shipping.",
            "ebay_description": "High-density NBR yoga mat, 10mm thick for real joint protection. Non-slip surface on both sides prevents sliding during poses.\n\n72x24 inches. Suitable for yoga, pilates, stretching, and floor exercises. Includes carrying strap. Lightweight and portable.\n\nEasy to clean. Durable construction lasts years of daily use.",
        },
        "posture corrector": {
            "category": "Health & Wellness",
            "fb_title": "Posture Corrector - Adjustable, Wearable Under Clothes",
            "ebay_title": "Posture Corrector Back Brace Adjustable Support Upper Spine Shoulder Strap",
            "features": [
                "Adjustable straps fit chest sizes 28-48 inches",
                "Thin enough to wear under a t-shirt",
                "Pulls shoulders back without restricting movement",
                "Padded straps, no chafing",
            ],
            "fb_description": "Adjustable posture corrector that pulls your shoulders back and trains your spine to sit straight. Wear it 30 min/day for the first week, then increase.\n\nThin enough to wear under a t-shirt at work. Nobody sees it. Padded straps so it won't dig in.\n\nFits chest sizes 28-48 inches. If you sit at a desk 8+ hours, your back will thank you.\n\nFree shipping.",
            "ebay_description": "Adjustable posture corrector brace for upper back and shoulder alignment. Padded straps for comfort during extended wear. Fits chest sizes 28-48 inches.\n\nWear under clothing at work or home. Start with 30 minutes daily and increase gradually. Trains muscles to maintain correct posture over time.\n\nLightweight, breathable mesh material.",
        },
        "gua sha tool": {
            "category": "Beauty & Health",
            "fb_title": "Gua Sha Facial Tool - Natural Rose Quartz, Sculpts + Depuffs",
            "ebay_title": "Gua Sha Rose Quartz Facial Sculpting Massage Tool Lymphatic Drainage",
            "features": [
                "Natural rose quartz stone, cool to the touch",
                "Reduces face puffiness in 5 minutes",
                "Promotes lymphatic drainage and blood circulation",
                "Multiple edges for jawline, cheekbones, and under-eye",
            ],
            "fb_description": "Rose quartz gua sha tool for facial sculpting and depuffing. Keep it in the fridge and use for 5 minutes in the morning. The puffiness difference is visible immediately.\n\nMultiple edges shaped for jawline sculpting, cheekbone lifting, and under-eye drainage. Use with any facial oil or serum.\n\nNatural stone, not plastic. Lasts forever. Free shipping.",
            "ebay_description": "Natural rose quartz gua sha facial tool for lymphatic drainage and facial sculpting. Multiple contoured edges for jawline, cheekbones, forehead, and under-eye.\n\nStore in refrigerator for cooling effect. Reduces morning puffiness in one 5-minute session. Use with facial oil for smooth glide.\n\nHandcrafted natural stone. Each piece has unique natural veining.",
        },
        "scalp massager": {
            "category": "Beauty & Health",
            "fb_title": "Scalp Massager Shampoo Brush - Silicone, Feels Like a Spa",
            "ebay_title": "Silicone Scalp Massager Shampoo Brush Head Scrubber Hair Growth Stimulator",
            "features": [
                "Soft silicone bristles, won't scratch",
                "Distributes shampoo evenly and removes buildup",
                "Stimulates blood flow to scalp",
                "Waterproof, use in the shower",
            ],
            "fb_description": "Silicone scalp massager you use in the shower while shampooing. Soft bristles massage the scalp and remove product buildup that regular washing misses.\n\nStimulates blood circulation to hair follicles. People report less hair shedding and faster growth after consistent use.\n\nWaterproof. Hangs in your shower. Feels like a $80 spa treatment for a fraction of the price.\n\nFree shipping.",
            "ebay_description": "Silicone scalp massager brush for use during shampooing. Soft flexible bristles clean deeply and stimulate blood circulation to scalp.\n\nRemoves product buildup, dead skin, and excess oil that regular washing leaves behind. Promotes healthier hair growth through improved circulation.\n\nWaterproof design. Ergonomic handle. Easy to clean.",
        },
        "wireless earbuds": {
            "category": "Electronics",
            "fb_title": "Wireless Earbuds - Bluetooth 5.3, 30hr Battery, Touch Control",
            "ebay_title": "Wireless Bluetooth 5.3 Earbuds Touch Control 30hr Battery Noise Cancelling",
            "features": [
                "Bluetooth 5.3 for stable connection",
                "30-hour total battery (6hr buds + 24hr case)",
                "Touch controls for play/pause/skip",
                "IPX5 water resistant",
            ],
            "fb_description": "Bluetooth 5.3 wireless earbuds with 30-hour total battery life. 6 hours per charge in the buds, plus 4 extra charges in the case.\n\nTouch controls on both earbuds. No need to pull out your phone to skip tracks or answer calls.\n\nIPX5 water resistant, fine for workouts and rain. USB-C charging. Works with iPhone and Android.\n\nFree shipping.",
            "ebay_description": "Bluetooth 5.3 wireless earbuds with 30-hour total battery life (6hr + 24hr charging case). Touch controls for play/pause, track skip, and calls.\n\nIPX5 water resistant for gym and outdoor use. USB-C fast charging. 10 minutes of charging gives 1 hour of playback.\n\nCompatible with all Bluetooth devices. Includes S/M/L ear tips for secure fit.",
        },
        "cat water fountain": {
            "category": "Pet Supplies",
            "fb_title": "Cat Water Fountain - 2L Automatic, Ultra Quiet, Triple Filter",
            "ebay_title": "Automatic Cat Water Fountain 2L Quiet Pump Triple Filtration Pet Drinking",
            "features": [
                "2-liter capacity, lasts 2-3 days for one cat",
                "Triple filtration (cotton, carbon, ion exchange)",
                "Ultra-quiet pump under 30dB",
                "BPA-free, dishwasher-safe parts",
            ],
            "fb_description": "2-liter automatic water fountain for cats. Running water encourages cats to drink more, which prevents kidney and urinary issues. Vets recommend fountains over stagnant bowls.\n\nTriple filtration system (cotton, carbon, ion exchange) keeps water clean for 2-3 weeks between filter changes. Replacement filters cost about $3 each.\n\nWhisper-quiet pump. You won't hear it from the next room. BPA-free plastic. Dishwasher-safe parts.\n\nFree shipping. Works for small dogs too.",
            "ebay_description": "Running water fountain that keeps cats hydrated. 2L capacity lasts 2-3 days for one cat. Triple filtration removes hair, debris, and chlorine taste.\n\nUltra-quiet pump (under 30dB). BPA-free. Dishwasher-safe bowl and cover. LED indicator shows water level.\n\nVets recommend flowing water over still bowls for cat kidney health.",
        },
        "jump rope weighted": {
            "category": "Sporting Goods",
            "fb_title": "Weighted Jump Rope - 1 lb, Burns 2x Calories vs Regular Rope",
            "ebay_title": "Weighted Jump Rope 1lb Adjustable Fitness Cardio Skipping Rope Ball Bearing",
            "features": [
                "1 lb weighted rope for extra calorie burn",
                "Ball bearing handles for smooth rotation",
                "Adjustable length, cut to fit any height",
                "Foam grip pads prevent blisters",
            ],
            "fb_description": "1 lb weighted jump rope for cardio and upper body conditioning. The added weight forces your arms, shoulders, and core to engage more than a standard speed rope.\n\n10 minutes of weighted jump rope burns roughly the same calories as 30 minutes of jogging. No gym required.\n\nAdjustable length fits any height (just cut the cable). Ball bearing handles for smooth rotation. Foam grip pads prevent blisters.\n\nFree shipping. Great for home workouts, boxing training, or CrossFit warm-ups.",
            "ebay_description": "1 lb weighted jump rope with ball bearing handles for smooth, tangle-free rotation. Adjustable cable length. Foam grip handles.\n\nBurns more calories per minute than running. Works arms, shoulders, and core simultaneously. Used by boxers, CrossFit athletes, and home gym owners.\n\nSuitable for beginners and advanced. Cut cable to your height and start.",
        },
        "lash serum": {
            "category": "Beauty & Health",
            "fb_title": "Lash Growth Serum - Fuller Lashes in 4-6 Weeks, No Irritation",
            "ebay_title": "Lash Growth Serum Peptide Eyelash Lengthening Enhancer 5ml 3-Month Supply",
            "features": [
                "Peptide-based formula, no prostaglandin",
                "Visible results in 3-4 weeks",
                "5ml tube lasts about 3 months",
                "Safe for sensitive eyes and contact lens wearers",
            ],
            "fb_description": "Peptide-based lash serum that strengthens and lengthens your natural lashes. Apply once at night along the lash line with the built-in micro brush. Takes 10 seconds.\n\nMost people see noticeable thickness in 3-4 weeks. Full results in 6-8 weeks.\n\nNo irritation. No prostaglandin (the ingredient that causes eye color changes in prescription serums). Safe for sensitive eyes and contact lens wearers.\n\n5ml tube lasts about 3 months. Free shipping.",
            "ebay_description": "Peptide lash serum that promotes natural lash growth. Apply nightly to clean lash line. Visible results in 3-4 weeks, full length in 6-8 weeks.\n\nNo prostaglandin. No eye color change risk. Hypoallergenic and safe for sensitive eyes. 5ml tube lasts approximately 3 months.\n\n1/5 the price of prescription lash serums with no doctor visit needed.",
        },
        "phone projector": {
            "category": "Electronics",
            "fb_title": "Mini Phone Projector - Movie Nights Without a TV, Portable",
            "ebay_title": "Mini Portable Phone Projector LED 1080p HDMI Wireless Home Theater",
            "features": [
                "Projects up to 100 inches on any white wall",
                "Connects via HDMI or wireless casting",
                "Built-in speaker, under 1 lb",
                "USB-C rechargeable or plug-in power",
            ],
            "fb_description": "Portable LED projector that connects to your phone via HDMI or wireless casting. Projects up to 100 inches on any white wall.\n\nPerfect for backyard movie nights, dorm rooms, or camping trips. Weighs under 1 lb. Fits in a backpack.\n\nBuilt-in speaker. 1080p supported input. 2-hour battery or plug into USB-C power bank for all-night use.\n\nFree shipping. Message for 2-unit bundle pricing.",
            "ebay_description": "Turn any wall into a movie screen. This mini projector connects to iPhone or Android via HDMI adapter or wireless screen mirror.\n\nProjects 40-100 inch image. Built-in speaker. Under 1 lb. USB-C rechargeable or plug-in power.\n\nGreat for apartments, camping, kids' rooms, backyard hangouts.",
        },
        "shower head filter": {
            "category": "Home & Garden",
            "fb_title": "Shower Head Filter - Removes Chlorine, Fixes Hard Water Hair",
            "ebay_title": "15-Stage Shower Head Filter Chlorine Hard Water Remover High Pressure",
            "features": [
                "15-stage filtration removes chlorine, heavy metals, sediment",
                "Installs in 2 minutes, no tools needed",
                "Filter lasts 6 months, replacements around $8",
                "Maintains full water pressure",
            ],
            "fb_description": "15-stage filtration shower head that removes chlorine, heavy metals, and sediment from your water. Installs in 2 minutes with no tools. Fits standard 1/2 inch shower arms.\n\nIf your hair feels dry and your skin itches after showers, it's the water. This fixes it.\n\nFilter lasts 6 months before replacement. Replacement cartridges run about $8.\n\nHigh-pressure spray even with the filter attached. You won't notice a flow difference.\n\nFree shipping.",
            "ebay_description": "Removes chlorine, fluoride, heavy metals, and sediment. 15 filtration stages. Installs on any standard shower arm in under 2 minutes, no plumber needed.\n\nReduces dry skin and brittle hair caused by hard water. Filter cartridge lasts 6 months.\n\nMaintains full water pressure. Chrome finish matches any bathroom.",
        },
        "resistance bands set": {
            "category": "Sporting Goods",
            "fb_title": "Resistance Bands Set - 5 Bands + Handles + Door Anchor + Bag",
            "ebay_title": "Resistance Bands Set 5 Pack Exercise Workout Bands Handles Home Gym Fitness",
            "features": [
                "5 resistance levels from 10-50 lbs",
                "Includes 2 handles, 2 ankle straps, door anchor, carrying bag",
                "Natural latex, snap-resistant",
                "Full body workout without a gym",
            ],
            "fb_description": "Complete resistance bands set with 5 different resistance levels (10-50 lbs). Includes 2 cushioned handles, 2 ankle straps, door anchor, and carrying bag.\n\nReplaces a gym membership for most exercises. Chest press, rows, curls, squats, leg extensions. Stack multiple bands for heavier resistance.\n\nNatural latex construction. Snap-resistant. Portable enough for hotel rooms and travel.\n\nFree shipping.",
            "ebay_description": "5-piece resistance bands set with handles, ankle straps, door anchor, and carrying bag. Bands range from 10 to 50 lbs resistance.\n\nFull body workout capability. Stack bands for heavier resistance. Natural latex, durable construction.\n\nPerfect for home gym, travel, physical therapy, and strength training.",
        },
        "ring light": {
            "category": "Electronics",
            "fb_title": "10\" Ring Light with Tripod + Phone Holder - TikTok/YouTube Ready",
            "ebay_title": "10 Inch LED Ring Light Tripod Stand Phone Holder Video TikTok YouTube Streaming",
            "features": [
                "10-inch LED ring, 3 color modes, 10 brightness levels",
                "Adjustable tripod stand included",
                "Phone holder built in",
                "USB powered, works with any power bank or laptop",
            ],
            "fb_description": "10-inch LED ring light with adjustable tripod stand and phone holder. 3 color modes (warm, cool, daylight) with 10 brightness levels each.\n\nMakes anyone look better on camera. Eliminates shadows and evens out skin tone. The difference in video call and content quality is immediate.\n\nUSB powered. Works with any laptop, power bank, or wall adapter. Perfect for TikTok, YouTube, Zoom calls, or selfies.\n\nFree shipping.",
            "ebay_description": "10-inch LED ring light with adjustable tripod and phone holder. 3 color temperatures (3200K-6500K) with 10 brightness levels.\n\nUSB powered. Compatible with all smartphones. Ideal for content creation, video calls, live streaming, and photography.\n\nAdjustable tripod height. Compact for travel and storage.",
        },
        "pull up bar": {
            "category": "Sporting Goods",
            "fb_title": "Doorway Pull Up Bar - No Screws, Fits Standard Doors, 300lb Max",
            "ebay_title": "Doorway Pull Up Bar No Screw Home Gym Chin Up Exercise Fitness Training Bar",
            "features": [
                "No drilling required, pressure-mount design",
                "Fits standard door frames 24-36 inches",
                "Supports up to 300 lbs",
                "Multiple grip positions (wide, narrow, neutral)",
            ],
            "fb_description": "Heavy-duty doorway pull up bar. No drilling, no screws. Pressure-mount design locks into any standard door frame (24-36 inches).\n\nSupports up to 300 lbs. Multiple grip positions for pull ups, chin ups, and hanging ab exercises. Padded foam grips for comfort.\n\nInstalls in 30 seconds. Remove it when you're done, zero damage to the door frame.\n\nFree shipping.",
            "ebay_description": "Doorway pull up bar with pressure-mount installation. No screws or drilling. Fits door frames 24-36 inches wide. Supports up to 300 lbs.\n\nMultiple grip positions: wide, narrow, and neutral. Foam-padded handles for comfort. Removable with no damage to door frame.\n\nIdeal for home gym. Pull ups, chin ups, hanging leg raises.",
        },
        "cable organizer": {
            "category": "Electronics / Home",
            "fb_title": "Cable Organizer Clips - Stick On, No More Desk Spaghetti",
            "ebay_title": "Cable Organizer Clips Adhesive Desk Cord Management Holder Set",
            "features": [
                "Self-adhesive backing, sticks to any surface",
                "Holds multiple cable sizes (USB-C, Lightning, HDMI)",
                "Keeps desk clean and cables accessible",
                "Reusable, won't damage surfaces",
            ],
            "fb_description": "Self-adhesive cable organizer clips for your desk. Stick them to the edge and slide your cables in. No more fishing for charging cables that fell behind the desk.\n\nHolds USB-C, Lightning, HDMI, and headphone cables. Strong adhesive but won't damage surfaces when removed.\n\nTakes 2 minutes to install. Makes your desk look 10x cleaner.\n\nFree shipping.",
            "ebay_description": "Adhesive cable management clips for desk, nightstand, or wall. Holds multiple cable sizes. Strong 3M adhesive backing.\n\nKeeps cables organized and within reach. No drilling required. Removable without surface damage.\n\nSet includes multiple clips for full desk organization.",
        },
        "ice roller face": {
            "category": "Beauty & Health",
            "fb_title": "Ice Roller for Face - Depuffs in 2 Minutes, Stainless Steel",
            "ebay_title": "Ice Roller Face Massager Stainless Steel Cold Therapy Depuffing Skincare",
            "features": [
                "Stainless steel roller stays cold without freezing",
                "Reduces face puffiness and under-eye bags",
                "Shrinks pores and calms redness",
                "No water, no mess, use anytime",
            ],
            "fb_description": "Stainless steel ice roller for face depuffing. Keep it in the fridge and roll for 2 minutes in the morning. The puffiness reduction is visible immediately.\n\nShrinks pores, calms redness, reduces under-eye bags. Use after skincare to help products absorb.\n\nNo water dripping like ice cubes. No mess. Lasts forever because it's solid steel.\n\nFree shipping.",
            "ebay_description": "Stainless steel facial ice roller for cold therapy. Reduces puffiness, shrinks pores, and calms skin redness. Store in refrigerator for cooling effect.\n\nUse morning and night for depuffing and skincare product absorption. No water, no mess.\n\nDurable stainless steel construction. Easy to clean.",
        },
        "neck stretcher": {
            "category": "Health & Wellness",
            "fb_title": "Neck Stretcher - Cervical Traction Device, Relieves Tension in 10 Min",
            "ebay_title": "Neck Stretcher Cervical Traction Device Pain Relief Spine Alignment Relaxer",
            "features": [
                "Decompresses cervical spine without a chiropractor",
                "10 minutes provides noticeable tension relief",
                "Ergonomic design supports natural neck curve",
                "No moving parts, nothing to inflate or pump",
            ],
            "fb_description": "Cervical traction neck stretcher that decompresses your spine. Lie on it for 10 minutes and feel the tension release in your neck and upper back.\n\nSame concept as chiropractic cervical traction but you do it at home, anytime. No appointments, no copays.\n\nErgonomic design restores the natural C-curve of your neck that gets flattened from desk work and phone use.\n\nFree shipping.",
            "ebay_description": "Cervical traction neck stretcher for pain relief and spine decompression. Restores natural neck curvature affected by desk work and phone use.\n\n10 minutes of use provides tension relief. No inflation, no moving parts. Ergonomic contoured design.\n\nLightweight and portable. Use at home or office.",
        },
        "dermaplaning tool": {
            "category": "Beauty & Health",
            "fb_title": "Dermaplaning Tool Set - Facial Exfoliation, Peach Fuzz Removal",
            "ebay_title": "Dermaplaning Tool Set Facial Exfoliation Peach Fuzz Hair Removal Eyebrow Razor",
            "features": [
                "Removes peach fuzz and dead skin cells",
                "Makeup applies smoother after use",
                "Stainless steel, precision blade",
                "Use once per week",
            ],
            "fb_description": "Dermaplaning tool for facial exfoliation and peach fuzz removal. One pass removes the fine hair and dead skin layer that makes makeup look textured.\n\nYour foundation and serums apply noticeably smoother after dermaplaning. Use once per week before your skincare routine.\n\nStainless steel precision blade. Safety guard prevents cuts. Each blade lasts about 3-4 sessions.\n\nFree shipping.",
            "ebay_description": "Facial dermaplaning tool for exfoliation and peach fuzz removal. Stainless steel blade with safety guard. Removes dead skin cells for smoother skincare absorption.\n\nUse weekly before skincare routine. Improves makeup application. Precision blade for eyebrow shaping.\n\nSet includes multiple replacement blades.",
        },
    }

    # Fallback copy generator for products not in the database
    CATEGORY_COPY_HINTS = {
        "beauty": {"angle": "Results you can see in the mirror", "trust": "salon/spa quality at home prices"},
        "health": {"angle": "Fixes a daily annoyance you've been living with", "trust": "used by professionals"},
        "fitness": {"angle": "Replaces a gym membership or class", "trust": "used by athletes and trainers"},
        "tech": {"angle": "Solves a specific tech annoyance", "trust": "works with all devices"},
        "pet": {"angle": "Your pet will actually use this one", "trust": "vet recommended"},
        "home": {"angle": "Makes your space look/work better immediately", "trust": "installs in minutes"},
        "kitchen": {"angle": "Saves time on something you do every day", "trust": "durable materials"},
    }

    def analyze(self, dry_run=False):
        rows = read_csv_tail(self.SOURCE, 100)
        if not rows:
            log("Ecom Arb: No data found")
            return []

        actions = []
        for row in rows:
            margin = float(row.get("margin_pct", row.get("margin", 0)) or 0)
            action_flag = row.get("action", row.get("recommendation", "")).upper()
            product = row.get("product", row.get("product_name", "unknown"))
            source_price = row.get("source_price", row.get("buy_price", "?"))
            sell_price = row.get("sell_price", row.get("target_price", "?"))
            category = row.get("category", "general")

            if margin >= 25 or "LIST" in action_flag:
                actions.append({
                    "type": "ecom_listing",
                    "product": product,
                    "margin": margin,
                    "source_price": source_price,
                    "sell_price": sell_price,
                    "category": category,
                    "reasoning": f"Margin {margin}% >= 25% threshold, action={action_flag}",
                })

        log(f"Ecom Arb: {len(actions)} listable products from last 100 rows")

        if not dry_run and actions:
            self._generate_listings(actions[:10])

        return actions

    def _get_product_data(self, prod):
        """Look up product in knowledge DB or generate fallback copy."""
        product_key = prod["product"].strip().lower()
        db_entry = self.PRODUCT_DB.get(product_key)
        if db_entry:
            return db_entry

        # Fallback: generate reasonable copy from product name and category
        product_name = prod["product"].strip()
        product_title = product_name.title()
        category = prod.get("category", "general").strip().lower()
        hints = self.CATEGORY_COPY_HINTS.get(category, {"angle": "Solves a real problem", "trust": "quality materials"})

        return {
            "category": category.title(),
            "fb_title": product_title,
            "ebay_title": f"{product_title} - Free Shipping",
            "features": [
                f"{hints['trust']}",
                "Ships within 1-2 business days",
            ],
            "fb_description": f"{product_title}. {hints['angle']}. {hints['trust']}.\n\nFree shipping.",
            "ebay_description": f"{product_title}. {hints['trust']}. Ships fast.",
            "_is_fallback": True,
        }

    def _generate_listings(self, products):
        """Generate marketplace listing drafts with real product-specific copy."""
        self.OUTPUT.mkdir(parents=True, exist_ok=True)

        for prod in products:
            slug = prod["product"][:40].replace(" ", "_").replace("/", "_")
            outfile = self.OUTPUT / f"listing_{slug}_{datetime.now().strftime('%Y%m%d')}.md"
            if outfile.exists():
                continue

            db = self._get_product_data(prod)
            is_fallback = db.get("_is_fallback", False)

            fb_desc = db["fb_description"]
            ebay_desc = db["ebay_description"]
            fb_title = db["fb_title"]
            ebay_title = db["ebay_title"]
            category = db["category"]

            # Quality self-check: reject skeleton output
            quality_problems = []
            skeleton_markers = ["Brand new, ships fast", "[Auto-detect]", "[placeholder]",
                                "Brand new, sealed", "Ships fast, free shipping"]
            for marker in skeleton_markers:
                if marker in fb_desc or marker in ebay_desc:
                    quality_problems.append(f"skeleton marker detected: '{marker}'")
            if len(fb_desc) < 80:
                quality_problems.append(f"FB description too short ({len(fb_desc)} chars, need 80+)")
            if len(ebay_desc) < 60:
                quality_problems.append(f"eBay description too short ({len(ebay_desc)} chars, need 60+)")

            if quality_problems:
                log(f"Ecom: QUALITY REJECT for '{prod['product']}': {'; '.join(quality_problems)}", "WARN")
                continue

            status = "PENDING_REVIEW" if is_fallback else "READY_TO_LIST"

            content = f"""# Ecom Listing Draft
## Product: {prod['product']}
## Source Price: {prod['source_price']}
## Sell Price: {prod['sell_price']}
## Margin: {prod['margin']}%
## Generated: {datetime.now().isoformat()}

---

### FB Marketplace Listing

**Title:** {fb_title}
**Price:** ${prod['sell_price']}
**Category:** {category}
**Condition:** New
**Description:**
{fb_desc}

### eBay Listing

**Title:** {ebay_title}
**Price:** ${prod['sell_price']}
**Shipping:** Free (built into price)
**Description:**
{ebay_desc}

---

### Action Required
- Status: {status}
- Need: Platform accounts (FB Marketplace, eBay)
- Blocker: Account creation (see OPS/ACCOUNT_CREATION_NOW.md)
"""
            safe_path(outfile)
            outfile.write_text(content)
            log(f"Ecom: Generated listing for '{prod['product'][:30]}...' ({prod['margin']}% margin, status={status})")
            log_decision("ecom_arb", f"listing_draft:{slug}", prod["reasoning"])


class AlphaPipeline:
    """Process alpha staging entries into actionable content or strategy updates."""

    SOURCE = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
    BACKTEST = PROJECT_ROOT / "LEDGER" / "BACKTESTS" / "BACKTEST_RESULTS.csv"
    OUTPUT = PROJECT_ROOT / "CONTENT" / "alpha_actions"

    def analyze(self, dry_run=False):
        # Check backtest results for SCALE verdicts
        bt_rows = read_csv_tail(self.BACKTEST, 200)
        scale = [r for r in bt_rows if r.get("verdict", "").upper() == "SCALE"]
        paper = [r for r in bt_rows if r.get("verdict", "").upper() == "PAPER_TRADE"]

        log(f"Alpha: {len(scale)} SCALE, {len(paper)} PAPER_TRADE from backtest results")

        if not dry_run and scale:
            self._escalate_scale_items(scale)

        return {"scale": len(scale), "paper_trade": len(paper)}

    def _escalate_scale_items(self, items):
        """Create action items for SCALE-worthy alpha."""
        self.OUTPUT.mkdir(parents=True, exist_ok=True)

        for item in items[:5]:
            method = item.get("method", item.get("alpha_id", "unknown"))
            outfile = self.OUTPUT / f"scale_{method}_{datetime.now().strftime('%Y%m%d')}.md"
            if outfile.exists():
                continue

            content = f"""# SCALE ALERT — {method}
## Verdict: SCALE (backtest passed)
## Generated: {datetime.now().isoformat()}

---

### What This Means
The alpha screening system backtested this method and it passed the SCALE threshold.
This means it should be actively deployed, not just tracked.

### Source Data
{json.dumps(item, indent=2, default=str)}

### Next Actions
1. Review the method details above
2. Check if required accounts/tools exist
3. Deploy if ready, or add to OPS/PERSISTENT_TASK_TRACKER.md
4. Status: PENDING_REVIEW
"""
            safe_path(outfile)
            outfile.write_text(content)
            log(f"Alpha: Escalated SCALE item '{method}'")
            log_decision("alpha_screening", f"scale_escalation:{method}",
                        f"Backtest verdict=SCALE, auto-escalated for review")


class ContentIntegrationPipeline:
    """Move ralph loop output into proper content directories and deployment pipeline."""

    def analyze(self, dry_run=False):
        if not OUTPUT_DIR.exists():
            log("Content Integration: No spreadsheet buildout output found")
            return {}

        dirs = [d for d in OUTPUT_DIR.iterdir() if d.is_dir()]
        total_files = sum(1 for d in dirs for _ in d.rglob("*") if _.is_file())

        # Check what's already been integrated
        integrated_marker = OUTPUT_DIR / ".integrated"
        already_done = set()
        if integrated_marker.exists():
            already_done = set(integrated_marker.read_text().strip().split("\n"))

        new_dirs = [d for d in dirs if d.name not in already_done]

        log(f"Content Integration: {len(dirs)} output dirs, {len(new_dirs)} not yet integrated, {total_files} total files")

        if not dry_run and new_dirs:
            self._integrate_outputs(new_dirs, integrated_marker, already_done)

        return {"total_dirs": len(dirs), "new": len(new_dirs), "files": total_files}

    def _integrate_outputs(self, dirs, marker_file, already_done):
        """Copy relevant outputs to proper content directories."""
        content_base = PROJECT_ROOT / "CONTENT"

        mapping = {
            "C": "social",        # Content ops → social content
            "E": "ecom",          # Ecom → ecom content
            "D": "digital",       # Digital products
            "S": "services",      # Services
            "A": "apps",          # Apps
            "P": "personas",      # Personas
            "I": "invest",        # Investment
            "M": "community",     # Community
            "F": "affiliate",     # Affiliate
            "G": "growth",        # Growth
            "N": "growth",        # N-series → growth
        }

        integrated = list(already_done)

        for d in dirs:
            # Determine category from dir name prefix
            prefix = d.name[0].upper()
            category = mapping.get(prefix, "misc")
            target = content_base / category / "buildout" / d.name

            if target.exists():
                integrated.append(d.name)
                continue

            target.mkdir(parents=True, exist_ok=True)

            # Copy files (not move — keep originals)
            import shutil
            for f in d.rglob("*"):
                if f.is_file():
                    dest = target / f.relative_to(d)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    safe_path(dest)
                    shutil.copy2(f, dest)

            log(f"Content Integration: Integrated {d.name} → CONTENT/{category}/buildout/{d.name}")
            log_decision("content_integration", f"integrated:{d.name}",
                        f"Moved {sum(1 for _ in d.rglob('*') if _.is_file())} files to content pipeline")
            integrated.append(d.name)

        safe_path(marker_file)
        marker_file.write_text("\n".join(integrated))


class BrokenCronFixer:
    """Diagnose and fix broken cron jobs."""

    KNOWN_ISSUES = {
        "sam_gov_monitor.py": {
            "symptom": "Historically returned HTTP 404 on legacy SAM endpoint",
            "fix": "Patched 2026-03-06 to use sam.gov public search API endpoint",
            "severity": "LOW",
        },
        "hashtag_audio_tracking.py": {
            "symptom": "Historically had brotli decode errors and subreddit 404s",
            "fix": "Patched 2026-03-06 with gzip/identity encoding, retries, and valid subreddit list",
            "severity": "MEDIUM",
        },
        "trend_aggregator.py": {
            "symptom": "Historically produced 0 signals when run with no mode flags",
            "fix": "Patched 2026-03-06 so no-flag and --hourly runs default to full scan",
            "severity": "MEDIUM",
        },
        "platform_algo_detection.py": {
            "symptom": "Historically had Brave brotli decode failures and stale subreddit targets",
            "fix": "Patched 2026-03-06 with gzip/identity encoding, retries, and updated subreddit list",
            "severity": "LOW",
        },
    }

    def diagnose(self):
        log("=== BROKEN CRON DIAGNOSIS ===")
        fixes = []

        for script, info in self.KNOWN_ISSUES.items():
            log(f"  {script}: {info['symptom']}")
            log(f"    Fix: {info['fix']}")
            log(f"    Severity: {info['severity']}")
            fixes.append(info)

        return fixes

    def fix(self, dry_run=False):
        fixes_applied = []

        # Fix 1: Install brotli
        if not dry_run:
            try:
                import brotli
                log("brotli already installed")
            except ImportError:
                log("Installing brotli for Brave search fix...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "brotli"],
                    capture_output=True, text=True, timeout=60
                )
                if result.returncode == 0:
                    log("brotli installed successfully")
                    fixes_applied.append("brotli_install")
                else:
                    log(f"brotli install failed: {result.stderr[:200]}", "ERROR")

        return fixes_applied


class CronOptimizer:
    """Analyze and optimize cron schedule."""

    def __init__(self):
        self.last_check_error = None
        self.last_check_performed = False

    def _read_crontab(self):
        """Read active crontab text safely (may be unavailable in restricted envs)."""
        try:
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        except (PermissionError, FileNotFoundError, OSError) as e:
            self.last_check_error = str(e)
            return None

        if result.returncode != 0:
            stderr = (result.stderr or "").strip()
            self.last_check_error = stderr or "crontab unavailable"
            return None

        return result.stdout

    def analyze(self):
        """Check which action scripts exist but aren't in cron."""
        missing_from_cron = []
        self.last_check_error = None
        self.last_check_performed = False

        action_scripts = [
            ("auto_freelance_responder.py", "Responds to hot freelance posts", "*/3"),
            ("arb_listing_generator.py", "Generates listings from arb opportunities", "*/4"),
            ("trend_to_listing.py", "Converts trends to product listings", "*/6"),
            ("ecom_autopilot.py", "Auto-manages ecom pipeline", "*/4"),
        ]

        crontab_text = self._read_crontab()
        if crontab_text is None:
            log(f"Cron check skipped: {self.last_check_error}", "WARN")
            return missing_from_cron

        self.last_check_performed = True

        for script, desc, freq in action_scripts:
            path = PROJECT_ROOT / "AUTOMATIONS" / script
            if path.exists():
                if script not in crontab_text:
                    missing_from_cron.append({
                        "script": script,
                        "description": desc,
                        "suggested_frequency": freq,
                        "exists": True,
                    })
                    log(f"Cron gap: {script} exists but NOT in crontab ({desc})")

        return missing_from_cron


# === MAIN ENGINE ===

def run_cycle(dry_run=False):
    """Run one full decision cycle across all pipelines."""
    log("=" * 60)
    log(f"DECISION ENGINE CYCLE START {'(DRY RUN)' if dry_run else ''}")
    log("=" * 60)

    results = {}

    # Run all pipelines
    pipelines = [
        ("freelance", FreelancePipeline()),
        ("ecom_arb", EcomArbPipeline()),
        ("alpha", AlphaPipeline()),
        ("content_integration", ContentIntegrationPipeline()),
    ]

    for name, pipeline in pipelines:
        try:
            results[name] = pipeline.analyze(dry_run=dry_run)
        except Exception as e:
            log(f"{name}: ERROR — {e}", "ERROR")
            results[name] = {"error": str(e)}

    # Summary
    log("=" * 60)
    log("CYCLE COMPLETE — SUMMARY")
    for name, result in results.items():
        log(f"  {name}: {result}")
    log("=" * 60)

    return results


def run_daemon():
    """Run continuously, one cycle every 30 minutes."""
    log("DECISION ENGINE DAEMON STARTING — Ctrl+C to stop")
    log("Cycle interval: 30 minutes")

    while True:
        try:
            run_cycle(dry_run=False)
            log("Sleeping 30 minutes until next cycle...")
            time.sleep(1800)
        except KeyboardInterrupt:
            log("DAEMON STOPPED by user")
            break
        except Exception as e:
            log(f"CYCLE FAILED: {e} — retrying in 5 minutes", "ERROR")
            time.sleep(300)


def show_status():
    """Show current pipeline status."""
    print("=" * 60)
    print("PRINTMAXX DECISION ENGINE STATUS")
    print("=" * 60)

    # Data source sizes
    sources = {
        "Freelance Demand": PROJECT_ROOT / "LEDGER" / "FREELANCE_DEMAND_SCAN.csv",
        "Ecom Arb": PROJECT_ROOT / "LEDGER" / "ECOM_ARB_OPPORTUNITIES.csv",
        "Alpha Staging": PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv",
        "Backtest Results": PROJECT_ROOT / "LEDGER" / "BACKTESTS" / "BACKTEST_RESULTS.csv",
        "Decisions Log": DECISION_LEDGER,
    }

    print("\nDATA SOURCES:")
    for name, path in sources.items():
        count = count_csv_rows(path) if path.exists() else 0
        age = ""
        if path.exists():
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            age = f" (updated {mtime.strftime('%Y-%m-%d %H:%M')})"
        print(f"  {name}: {count:,} rows{age}")

    # Output integration status
    if OUTPUT_DIR.exists():
        dirs = [d for d in OUTPUT_DIR.iterdir() if d.is_dir()]
        marker = OUTPUT_DIR / ".integrated"
        integrated = set()
        if marker.exists():
            integrated = set(marker.read_text().strip().split("\n"))
        print(f"\nBUILDOUT OUTPUT: {len(dirs)} dirs, {len(integrated)} integrated")

    # Action outputs
    action_dirs = [
        ("Freelance Responses", PROJECT_ROOT / "CONTENT" / "freelance_responses"),
        ("Ecom Listings", PROJECT_ROOT / "CONTENT" / "ecom_listings"),
        ("Alpha Actions", PROJECT_ROOT / "CONTENT" / "alpha_actions"),
    ]

    print("\nACTION OUTPUTS:")
    for name, path in action_dirs:
        count = len(list(path.glob("*.md"))) if path.exists() else 0
        print(f"  {name}: {count} drafts")

    # Decision log
    if DECISION_LEDGER.exists():
        decisions = count_csv_rows(DECISION_LEDGER)
        print(f"\nDECISIONS LOGGED: {decisions}")

    # Cron watchlist
    print("\nCRON WATCHLIST (historical issues + patch notes):")
    fixer = BrokenCronFixer()
    for script, info in fixer.KNOWN_ISSUES.items():
        print(f"  {script}: {info['symptom']} [{info['severity']}]")
        print(f"    {info['fix']}")

    # Missing action scripts in cron
    print("\nMISSING FROM CRON (exist but not scheduled):")
    optimizer = CronOptimizer()
    missing = optimizer.analyze()
    if optimizer.last_check_error:
        print(f"  Skipped cron check: {optimizer.last_check_error}")
    elif not missing:
        print("  All action scripts are in cron")
    else:
        for item in missing:
            print(f"  {item['script']} ({item['suggested_frequency']}): {item['description']}")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Decision Engine")
    parser.add_argument("--cycle", action="store_true", help="Run one decision cycle")
    parser.add_argument("--daemon", action="store_true", help="Run continuously")
    parser.add_argument("--status", action="store_true", help="Show pipeline status")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without executing")
    parser.add_argument("--fix-broken", action="store_true", help="Fix broken cron jobs")

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.fix_broken:
        fixer = BrokenCronFixer()
        fixer.diagnose()
        fixer.fix(dry_run=False)
    elif args.daemon:
        run_daemon()
    elif args.cycle or args.dry_run:
        run_cycle(dry_run=args.dry_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
