#!/usr/bin/env python3
"""trend_to_listing.py - Trend-to-Listing Automation Pipeline
Reads trend signals, ecom arb, and freelance demand -> auto-generates listings.
CLI: --scan | --hourly | --check-winners | --generate-ads | --status | --category POD|DIGITAL|ETSY|ALL
"""
import argparse, csv, hashlib, os, re, sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER = PROJECT_ROOT / "LEDGER"
OUT_BASE = PROJECT_ROOT / "AUTOMATIONS" / "output" / "auto_listings"
OUT_POD, OUT_GUMROAD, OUT_ETSY, OUT_SOCIAL = (OUT_BASE / d for d in ("pod", "gumroad", "etsy", "social"))
WINNERS_CSV = OUT_BASE / "WINNERS.csv"
TREND_CSV, ECOM_CSV, FREELANCE_CSV = (LEDGER / f for f in
    ("TREND_SIGNALS.csv", "ECOM_ARB_OPPORTUNITIES.csv", "FREELANCE_DEMAND_SCAN.csv"))
MIN_SCORE = 60
DIGITAL_MATCHES = {"digital_product", "service_opportunity", "content_opportunity", "productivity"}
POD_MATCHES = {"general", "fashion_accessories", "health_wellness", "pet", "home_organization",
               "tech_gadget", "beauty_skincare"}

def safe_path(p: Path) -> bool:
    try: p.resolve().relative_to(PROJECT_ROOT.resolve()); return True
    except ValueError: return False

def ensure_dirs():
    for d in [OUT_POD, OUT_GUMROAD, OUT_ETSY, OUT_SOCIAL]:
        if safe_path(d): d.mkdir(parents=True, exist_ok=True)

def read_csv_safe(path: Path) -> list:
    if not path.exists(): print(f"  [SKIP] {path.name} not found"); return []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))

def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower().strip())[:60].strip("_")

def trend_id(signal: str, source: str) -> str:
    return f"TL-{hashlib.md5(f'{signal}|{source}'.encode()).hexdigest()[:8]}"

def parse_ts(ts_str: str) -> datetime:
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try: return datetime.strptime(ts_str, fmt)
        except ValueError: pass
    return datetime.min

def extract_keywords(signal: str) -> list:
    stop = {"a","an","the","to","of","in","on","for","and","or","is","it","how","your","you",
            "that","this","with","from","about","cool","guide","what","if","are","be","was",
            "were","been","being","do","does","did","has","have","had","at","by","my","me",
            "we","us","our","its"}
    return [w.lower() for w in re.findall(r"[a-zA-Z]{3,}", signal) if w.lower() not in stop][:8]

def get_product_types(pm: str) -> set:
    return {m.strip() for m in pm.split(",") if m.strip()} if pm else set()

def now_str(): return datetime.now().strftime('%Y-%m-%d %H:%M')

def gen_pod_listing(tid, signal, score, source, kw, strength, url):
    kws, dkw = ", ".join(kw[:5]), " ".join(kw[:4])
    tb = " ".join(w.capitalize() for w in kw[:4])
    return f"""# POD Listing: {tid}
**Generated:** {now_str()} | **Score:** {score} | **Strength:** {strength} | **Source:** {source}
**Signal:** {signal[:120]}
**URL:** {url}

## T-Shirt
- **Title:** {tb} - Trending Design Tee
- **Desc:** {signal[:80]}. Premium cotton, unisex fit. S-3XL. Black/White/Navy.
- **Tags:** {kws}, trending, viral, gift idea
- **Price:** $24.99 (cost ~$12, margin ~$13)

## Mug
- **Title:** {tb} Coffee Mug | 11oz ceramic, dishwasher safe.
- **Tags:** {kws}, coffee mug, gift, trending | **Price:** $16.99 (cost ~$7)

## Sticker
- **Title:** {tb} Vinyl Sticker | 3" die-cut, waterproof, UV resistant.
- **Tags:** {kws}, sticker, vinyl, laptop | **Price:** $4.99 (cost ~$1.50)

## Design Prompt
```
minimalist vector illustration of {dkw}, clean lines, bold typography,
print on demand, high contrast, {kw[0] if kw else 'trending'} theme,
no background, PNG transparent, 4500x5400px 300dpi
```

## Platforms: Redbubble (free, 20%) | TeePublic (free) | Printful+Etsy (higher margin)
"""

def gen_gumroad_listing(tid, signal, score, source, kw, strength, url):
    tw = " ".join(w.capitalize() for w in kw[:5])
    return f"""# Gumroad Product: {tid}
**Generated:** {now_str()} | **Score:** {score} | **Strength:** {strength} | **Source:** {source}
**Signal:** {signal[:120]}
**URL:** {url}

- **Title:** The Complete {tw} Guide
- **Price:** $9 (or $0+ PWYW for lead magnet)
- **Format:** PDF 15-25 pages + bonus checklist
- **Tags:** {", ".join(kw[:5])}

## Description
People are searching for this RIGHT NOW. {signal[:100]}.
Covers: core framework, common mistakes, quick-start checklist, printable reference sheet.
No fluff. Specific steps. Actionable immediately.

## TOC
1. Why this matters now  2. Core method (step-by-step)  3. Tools + resources
4. Common mistakes  5. Quick-start checklist  6. Bonus one-pager

## Production: Claude (Opus) + Canva layout. 2-3 hours. Break-even: 1 sale. Target: 20+/week.
"""

def gen_etsy_listing(tid, signal, score, source, kw, strength, ptypes, url):
    is_dig = "digital_product" in ptypes
    tw = " ".join(w.capitalize() for w in kw[:6])
    raw = kw[:6] + ["trending", "viral", "gift idea", "bestseller", "popular", "2026",
                     "printable" if is_dig else "handmade"]
    tags = ", ".join(t[:20] for t in raw[:13])
    if is_dig:
        return f"""# Etsy Digital: {tid}
**Generated:** {now_str()} | **Score:** {score} | **Source:** {source}
**Signal:** {signal[:120]}

- **Title:** {tw} | Printable Guide | Digital Download | Instant PDF
- **Price:** $5.99 | **Category:** Digital Downloads > Printables
- **Tags (13):** {tags}

## Description
Trending topic, instant download. {signal[:80]}.
You get: high-res PDF (A4/Letter), quick reference checklist, clean minimal design.
DIGITAL DOWNLOAD. No physical item. Instant access after purchase.
SEO: primary "{kw[0] if kw else 'guide'}" | long-tail "{' '.join(kw[:3])} printable guide"
"""
    return f"""# Etsy POD: {tid}
**Generated:** {now_str()} | **Score:** {score} | **Source:** {source}
**Signal:** {signal[:120]}

- **Title:** {tw} | Trending Design | Unisex T-Shirt | Gift Idea 2026
- **Price:** $24.99 | **Category:** Clothing > Unisex > Tops & Tees
- **Tags (13):** {tags}
- **Shipping:** Printful/Printify (3-5 business days)

## Description
{signal[:80]}. Premium ringspun cotton, unisex relaxed fit, eco-friendly inks. S-3XL.
Ships from US. Exchanges within 30 days.
SEO: primary "{kw[0] if kw else 'trending'} shirt" | long-tail "{' '.join(kw[:3])} t-shirt"
"""

def gen_social_posts(tid, signal, score, source, kw, url):
    ss = signal[:80].rstrip(".")
    ht = " ".join(f"#{w}" for w in kw[:3])
    return f"""# Social: {tid}
**Generated:** {now_str()} | **Score:** {score} | **Source:** {source}

## Tweet
{ss}
turned this into a product. link in bio.
{ht}

## Tweet Alt (build-in-public)
spotted this trending: "{ss}"
made a listing in 20 min. if it sells 3 copies I'm putting $5/day ads behind it.
the playbook: find trend -> make product -> test -> scale winners.

## Reddit (r/SideProject)
**Title:** I turned a trending topic into a product listing in under an hour
Noticed "{ss}" getting traction ({source}). Made a quick product around it in 30 min.
My approach: 1) Spot trends via scanners 2) Generate listing copy + design prompts
3) List on 2-3 platforms 4) 3+ sales in 48h = paid ads 5) Kill non-converters
"""

def gen_ad_spec(w):
    sig, tid = w.get("signal","?")[:80], w.get("tid","?")
    sales, rev = w.get("sales","?"), w.get("revenue","?")
    return f"""# Ad Spec: {tid}
**Generated:** {now_str()} | **Performance:** {sales} sales, ${rev} revenue

## Facebook Ad
**Hook:** "{sig}" - everyone is talking about this.
**Body:** We turned this into something you can use. Already {sales} people grabbed it.
**CTA:** Get yours before the trend dies.
**Targeting:** Interest-based keywords | Lookalike if pixel | Age 18-45 | Feed+Stories+Reels
**Budget:** $5/day x 3 days ($15 test). ROAS>2x -> $20/day. ROAS<1x -> kill.

## TikTok Ad
**Hook (1s):** "this is trending and I turned it into a product"
**Script (15s):** "saw this blowing up. made a product in 30 min. already {sales} sales."
**CTA:** "link in bio. grab it before the trend dies."
**Targeting:** Broad (let algo find buyers) | Age 18-34 | $5/day spark ads

## Scale: 3+ sales $0 ads -> $5/day | ROAS>2x -> $20/day | ROAS>3x -> $50/day | ROAS<1x 3d -> kill
"""

def load_winners():
    return read_csv_safe(WINNERS_CSV) if WINNERS_CSV.exists() else []

def init_winners_csv():
    if WINNERS_CSV.exists(): return
    if not safe_path(WINNERS_CSV): return
    with open(WINNERS_CSV, "w", newline="") as f:
        csv.writer(f).writerow(["tid","signal","score","platform","listed_date",
                                 "sales","revenue","ad_spend","status","notes"])

def write_if_safe(path: Path, content: str) -> bool:
    if safe_path(path): path.write_text(content); return True
    return False

# --- Main pipeline ---
def run_scan(hourly=False, category="ALL"):
    ensure_dirs(); init_winners_csv()
    now = datetime.now()
    cutoff = now - timedelta(hours=2) if hourly else datetime.min
    mode = "HOURLY (last 2h)" if hourly else "FULL SCAN"
    print(f"\n{'='*60}\n  TREND-TO-LISTING PIPELINE\n  Mode: {mode}\n  "
          f"Category: {category} | Min Score: {MIN_SCORE}\n  {now.strftime('%Y-%m-%d %H:%M:%S')}\n{'='*60}\n")

    print("[1/4] Loading data sources...")
    trends, ecom, freelance = read_csv_safe(TREND_CSV), read_csv_safe(ECOM_CSV), read_csv_safe(FREELANCE_CSV)
    print(f"  Trends: {len(trends)} | Ecom Arb: {len(ecom)} | Freelance: {len(freelance)}")

    print(f"\n[2/4] Filtering trends (score >= {MIN_SCORE})...")
    qualified, seen = [], set()

    for row in trends:
        try: score = int(float(row.get("score", 0)))
        except (ValueError, TypeError): continue
        if score < MIN_SCORE: continue
        ts = parse_ts(row.get("timestamp", ""))
        if hourly and ts < cutoff: continue
        signal = row.get("signal", "").strip()
        if not signal: continue
        sk = signal[:60].lower()
        if sk in seen: continue
        seen.add(sk)
        qualified.append({"signal": signal, "score": score, "source": row.get("source", "unknown"),
            "strength": int(float(row.get("strength", 0))) if row.get("strength") else 0,
            "product_matches": row.get("product_matches", ""), "url": row.get("url", "")})

    for row in ecom:
        if row.get("action") != "LIST": continue
        try: margin, comp = float(row.get("margin_pct", 0)), float(row.get("composite_score", 0))
        except (ValueError, TypeError): continue
        if comp < MIN_SCORE: continue
        prod = row.get("product", "")
        if prod.lower() in seen: continue
        seen.add(prod.lower())
        qualified.append({"signal": f"Ecom arb: {prod} (margin {margin:.0f}%, ${row.get('net_profit','?')} profit)",
            "score": int(comp), "source": f"ecom_arb/{row.get('category','general')}",
            "strength": int(float(row.get("sell_price", 0))) if row.get("sell_price") else 0,
            "product_matches": row.get("category", "general"), "url": ""})

    for row in freelance:
        try: score = int(float(row.get("score", 0)))
        except (ValueError, TypeError): continue
        if score < MIN_SCORE: continue
        title = row.get("title", "").strip()
        sk = title[:60].lower()
        if sk in seen: continue
        seen.add(sk)
        budget = row.get("budget", "?")
        qualified.append({"signal": f"Freelance demand: {title} (budget ${budget})", "score": score,
            "source": row.get("source", "r/forhire"),
            "strength": int(float(budget)) if budget and budget != "?" else 0,
            "product_matches": "digital_product,service_opportunity", "url": row.get("url", "")})

    qualified.sort(key=lambda x: x["score"], reverse=True)
    print(f"  Qualified trends: {len(qualified)} (after dedup + score filter)")

    print(f"\n[3/4] Generating listings...")
    c = {"pod": 0, "gumroad": 0, "etsy": 0, "social": 0}
    for item in qualified:
        tid = trend_id(item["signal"], item["source"])
        kw = extract_keywords(item["signal"])
        pt = get_product_types(item["product_matches"])
        s, sc, src, st, url = item["signal"], item["score"], item["source"], item["strength"], item["url"]
        fn = slug(item["signal"][:50])

        if category in ("ALL","POD") and pt & POD_MATCHES:
            if write_if_safe(OUT_POD / f"{fn}_{tid}.md", gen_pod_listing(tid,s,sc,src,kw,st,url)): c["pod"] += 1
        if category in ("ALL","DIGITAL") and pt & DIGITAL_MATCHES:
            if write_if_safe(OUT_GUMROAD / f"{fn}_{tid}.md", gen_gumroad_listing(tid,s,sc,src,kw,st,url)): c["gumroad"] += 1
        if category in ("ALL","ETSY"):
            if write_if_safe(OUT_ETSY / f"{fn}_{tid}.md", gen_etsy_listing(tid,s,sc,src,kw,st,pt,url)): c["etsy"] += 1
        if write_if_safe(OUT_SOCIAL / f"{fn}_{tid}.md", gen_social_posts(tid,s,sc,src,kw,url)): c["social"] += 1

    total = sum(c.values())
    print(f"\n[4/4] RESULTS\n{'='*60}")
    print(f"  Trends processed:   {len(qualified)}\n  POD listings:       {c['pod']}")
    print(f"  Gumroad products:   {c['gumroad']}\n  Etsy listings:      {c['etsy']}")
    print(f"  Social posts:       {c['social']}\n  TOTAL FILES:        {total}")
    print(f"{'='*60}\n  Output: {OUT_BASE}/")
    if qualified:
        print(f"\n  TOP 5 TRENDS:")
        for i, item in enumerate(qualified[:5], 1):
            print(f"    {i}. [{item['score']}] {item['signal'][:70]}")
    return c

def check_winners():
    print(f"\n{'='*60}\n  WINNER CHECK\n{'='*60}\n")
    winners = load_winners()
    if not winners:
        print(f"  No entries in WINNERS.csv yet.\n  File: {WINNERS_CSV}"); return
    hot = [w for w in winners if int(float(w.get("sales", 0))) >= 3]
    print(f"  Total tracked: {len(winners)}\n  Winners (3+ sales): {len(hot)}")
    if hot:
        print(f"\n  PUT ADS BEHIND THESE:")
        for w in hot:
            print(f"    [{w.get('tid','?')}] {w.get('signal','?')[:50]} | {w.get('sales','?')} sales"
                  f" | ${w.get('revenue','?')} | {w.get('platform','?')}")
    else: print("  No winners yet. Keep listing and tracking sales.")

def generate_ads():
    ensure_dirs()
    print(f"\n{'='*60}\n  AD CREATIVE GENERATOR\n{'='*60}\n")
    winners = load_winners()
    hot = [w for w in winners if int(float(w.get("sales", 0))) >= 3]
    if not hot: print("  No winners with 3+ sales found."); return
    ad_dir = OUT_BASE / "ads"
    if safe_path(ad_dir): ad_dir.mkdir(parents=True, exist_ok=True)
    for w in hot:
        out = ad_dir / f"ad_{w.get('tid','unknown')}.md"
        if write_if_safe(out, gen_ad_spec(w)): print(f"  Generated: {out.name}")
    print(f"\n  {len(hot)} ad specs -> {ad_dir}/")

def show_status():
    print(f"\n{'='*60}\n  TREND-TO-LISTING STATUS\n  {now_str()}\n{'='*60}\n")
    trends = read_csv_safe(TREND_CSV) if TREND_CSV.exists() else []
    ecom = read_csv_safe(ECOM_CSV) if ECOM_CSV.exists() else []
    freelance = read_csv_safe(FREELANCE_CSV) if FREELANCE_CSV.exists() else []
    hi = sum(1 for t in trends if int(float(t.get("score", 0))) >= MIN_SCORE)
    print(f"  DATA SOURCES:\n    Trends: {len(trends)} total, {hi} high-score (>={MIN_SCORE})")
    print(f"    Ecom arb: {len(ecom)} | Freelance: {len(freelance)}")
    cf = lambda d: len(list(d.glob("*.md"))) if d.exists() else 0
    pc, gc, ec, sc = cf(OUT_POD), cf(OUT_GUMROAD), cf(OUT_ETSY), cf(OUT_SOCIAL)
    print(f"\n  LISTINGS: POD {pc} | Gumroad {gc} | Etsy {ec} | Social {sc} | TOTAL {pc+gc+ec+sc}")
    winners = load_winners()
    hot = [w for w in winners if int(float(w.get("sales", 0))) >= 3]
    print(f"\n  WINNERS: {len(winners)} tracked, {len(hot)} hot (3+ sales)")
    if hot:
        for w in hot:
            print(f"    [{w.get('tid')}] {w.get('signal','?')[:40]} | {w.get('sales')} sales")
    ac = cf(OUT_BASE / "ads") if (OUT_BASE / "ads").exists() else 0
    print(f"  AD SPECS: {ac}")

def main():
    p = argparse.ArgumentParser(description="Trend-to-Listing Pipeline")
    p.add_argument("--scan", action="store_true", help="Full pipeline scan")
    p.add_argument("--hourly", action="store_true", help="Cron: last 2 hours only")
    p.add_argument("--check-winners", action="store_true", help="Review winners")
    p.add_argument("--generate-ads", action="store_true", help="Ad specs for winners")
    p.add_argument("--status", action="store_true", help="Pipeline status")
    p.add_argument("--category", choices=["POD","DIGITAL","ETSY","ALL"], default="ALL")
    args = p.parse_args()
    if not any([args.scan, args.hourly, args.check_winners, args.generate_ads, args.status]):
        p.print_help(); print("\nQuick start: python3 trend_to_listing.py --scan"); sys.exit(0)
    if args.status: show_status()
    if args.scan: run_scan(hourly=False, category=args.category)
    if args.hourly: run_scan(hourly=True, category=args.category)
    if args.check_winners: check_winners()
    if args.generate_ads: generate_ads()

if __name__ == "__main__": main()
