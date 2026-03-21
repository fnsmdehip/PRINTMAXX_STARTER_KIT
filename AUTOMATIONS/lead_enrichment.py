#!/usr/bin/env python3

from __future__ import annotations
"""Lead Enrichment Engine — PRINTMAXX
Reads HOT_LEADS_QUALIFIED.csv -> enriches with Google Maps, social, tech stack,
competitor count, personalization hooks -> outputs HOT_LEADS_ENRICHED.csv

CLI: --enrich [--top N] [--category X] [--force] | --status
"""
import argparse, csv, hashlib, json, os, random, re, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

try:
    import requests
except ImportError:
    sys.exit("ERROR: pip3 install requests")

BASE = os.path.dirname(os.path.abspath(__file__))
QUALIFIED_DIR = os.path.join(BASE, "leads", "qualified")
INPUT_CSV = os.path.join(QUALIFIED_DIR, "HOT_LEADS_QUALIFIED.csv")
OUTPUT_CSV = os.path.join(QUALIFIED_DIR, "HOT_LEADS_ENRICHED.csv")
CACHE_DIR = os.path.join(QUALIFIED_DIR, ".enrichment_cache")
TIMEOUT, MAX_WORKERS = 10, 5
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/122.0.0.0"}
ENRICH_COLS = [
    "google_rating", "google_review_count", "has_facebook", "has_instagram",
    "facebook_url", "instagram_url", "detected_tech_stack", "competitor_count",
    "personalization_hooks", "enrichment_timestamp", "enrichment_status",
]


def ensure_dirs():
    os.makedirs(CACHE_DIR, exist_ok=True)

def cache_path(domain): return os.path.join(CACHE_DIR, hashlib.md5(domain.encode()).hexdigest() + ".json")

def load_cache(domain):
    p = cache_path(domain)
    if os.path.exists(p):
        try:
            with open(p) as f: return json.load(f)
        except (json.JSONDecodeError, IOError): pass
    return None

def save_cache(domain, data):
    try:
        with open(cache_path(domain), "w") as f: json.dump(data, f, indent=2)
    except IOError: pass


def fetch_google_maps_data(name, city, state, category):
    """Scrape Google rating + review count from search results."""
    result = {"google_rating": "", "google_review_count": ""}
    url = f"https://www.google.com/search?q={requests.utils.quote(f'{name} {city} {state} {category}')}+reviews"
    try:
        text = requests.get(url, headers=UA, timeout=TIMEOUT).text
        for pat in [r'data-rating="([\d.]+)"', r'"ratingValue"\s*:\s*"?([\d.]+)"?', r'(\d\.\d)\s*star']:
            m = re.search(pat, text, re.IGNORECASE)
            if m: result["google_rating"] = m.group(1); break
        for pat in [r'"ratingCount"\s*:\s*"?(\d+)"?', r'([\d,]+)\s*(?:reviews?|Google reviews?)']:
            m = re.search(pat, text, re.IGNORECASE)
            if m: result["google_review_count"] = m.group(1).replace(",", ""); break
    except Exception: pass
    return result


def check_social_presence(domain):
    """Check homepage for Facebook/Instagram links."""
    result = {"has_facebook": "NO", "has_instagram": "NO", "facebook_url": "", "instagram_url": ""}
    try:
        html = requests.get(f"https://{domain}", headers=UA, timeout=TIMEOUT, allow_redirects=True).text
        fb = re.search(r'href=["\']?(https?://(?:www\.)?facebook\.com/[^"\'>\s]+)', html, re.I)
        if fb: result["has_facebook"], result["facebook_url"] = "YES", fb.group(1).split("?")[0]
        ig = re.search(r'href=["\']?(https?://(?:www\.)?instagram\.com/[^"\'>\s]+)', html, re.I)
        if ig: result["has_instagram"], result["instagram_url"] = "YES", ig.group(1).split("?")[0]
    except Exception: pass
    return result


def detect_tech_stack(domain, existing_tech):
    """Detect CMS/platform from headers + HTML signatures."""
    sigs = [existing_tech] if existing_tech else []
    try:
        resp = requests.get(f"https://{domain}", headers=UA, timeout=TIMEOUT, allow_redirects=True)
        html, hdrs = resp.text.lower(), {k.lower(): v.lower() for k, v in resp.headers.items()}
        checks = [
            ("wp-content" in html or "wp-includes" in html, "WordPress"),
            ("wix.com" in html or "x-wix" in str(hdrs), "Wix"),
            ("squarespace" in html or "sqsp" in html, "Squarespace"),
            ("weebly" in html, "Weebly"), ("shopify" in html, "Shopify"),
            ("webflow" in html, "Webflow"),
            ("__next" in html or "_next/static" in html, "Next.js"),
            ("jquery" in html, "jQuery"), ("bootstrap" in html, "Bootstrap"),
            ("nginx" in hdrs.get("server", ""), "Nginx"),
            ("apache" in hdrs.get("server", ""), "Apache"),
            ("cloudflare" in hdrs.get("server", ""), "Cloudflare"),
            ("php" in hdrs.get("x-powered-by", ""), "PHP"),
        ]
        for cond, name in checks:
            if cond: sigs.append(name)
        if not sigs: sigs.append("Custom/Unknown")
    except Exception:
        if not sigs: sigs.append("Unreachable")
    seen, unique = set(), []
    for s in sigs:
        sl = s.lower().strip()
        if sl and sl not in seen: seen.add(sl); unique.append(s.strip())
    return " | ".join(unique) or "Unknown"


def count_competitors(city, state, category, all_leads):
    """Count same city+category leads as competitor density proxy."""
    c, s, cat = city.lower().strip(), state.lower().strip(), category.lower().strip()
    return max(sum(1 for l in all_leads if l.get("city","").lower().strip() == c
                   and l.get("state","").lower().strip() == s
                   and l.get("category","").lower().strip() == cat) - 1, 0)


def generate_hooks(row, enriched):
    """Build personalization hooks for cold email from enriched data."""
    hooks = []
    rating = enriched.get("google_rating", "")
    if rating:
        try:
            r = float(rating)
            if r < 4.0: hooks.append(f"Your {r}-star Google rating has room to grow")
            elif r >= 4.5: hooks.append(f"Your {r}-star rating is strong but your website doesn't match")
        except ValueError: pass
    reviews = enriched.get("google_review_count", "")
    if reviews:
        try:
            rc = int(reviews)
            if rc < 20: hooks.append(f"Only {rc} Google reviews. More online visibility = more reviews")
            elif rc > 100: hooks.append(f"{rc} reviews is impressive. Your site should showcase that")
        except ValueError: pass
    if enriched.get("has_facebook") == "NO" and enriched.get("has_instagram") == "NO":
        hooks.append("No social media linked on your site. Missing credibility signals")
    tech = enriched.get("detected_tech_stack", "").lower()
    if "unreachable" in tech:
        hooks.append("Your website appears down. Searchers are finding competitors instead")
    elif any(x in tech for x in ["table_layout", "flash_content", "font_tags", "frames"]):
        hooks.append("Site uses outdated tech. A modern rebuild loads faster and ranks higher")
    if row.get("mobile_friendly", "").upper() == "NO":
        hooks.append("Site not mobile-friendly. 60%+ of local searches are on phones")
    if row.get("ssl_valid", "").upper() == "NO":
        hooks.append("No SSL. Chrome shows 'Not Secure' warning to every visitor")
    comp = enriched.get("competitor_count", 0)
    if isinstance(comp, int) and comp > 5:
        hooks.append(f"{comp}+ competitors in {row.get('city', 'your area')} fighting for the same clients")
    score = row.get("total_score", "")
    if score:
        try:
            if int(score) >= 85: hooks.append("Your online presence scored bottom tier. Easy wins available")
        except ValueError: pass
    return " || ".join(hooks[:4]) if hooks else "Custom outreach recommended"


def enrich_lead(row, all_leads, force):
    """Enrich a single lead. Returns enrichment dict."""
    domain = row.get("domain", "").strip()
    if not domain:
        return {c: "" for c in ENRICH_COLS} | {"enrichment_status": "SKIP_NO_DOMAIN"}
    if not force:
        cached = load_cache(domain)
        if cached: cached["enrichment_status"] = "CACHED"; return cached

    time.sleep(random.uniform(1.0, 3.0))  # rate limit
    enriched = {}
    enriched.update(fetch_google_maps_data(row.get("name",""), row.get("city",""), row.get("state",""), row.get("category","")))
    enriched.update(check_social_presence(domain))
    enriched["detected_tech_stack"] = detect_tech_stack(domain, row.get("tech_stack", ""))
    enriched["competitor_count"] = count_competitors(row.get("city",""), row.get("state",""), row.get("category",""), all_leads)
    enriched["personalization_hooks"] = generate_hooks(row, enriched)
    enriched["enrichment_timestamp"] = datetime.now().isoformat()
    enriched["enrichment_status"] = "ENRICHED"
    save_cache(domain, enriched)
    return enriched


def read_leads(category_filter=None):
    if not os.path.exists(INPUT_CSV): sys.exit(f"ERROR: Not found: {INPUT_CSV}")
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f)
                if not category_filter or r.get("category","").lower().strip() == category_filter.lower().strip()]


def write_enriched(rows, enrichments, fieldnames):
    out_fields = fieldnames + [c for c in ENRICH_COLS if c not in fieldnames]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({**row, **enrichments.get(row.get("domain","").strip(), {c: "" for c in ENRICH_COLS})})
    print(f"\nOutput: {OUTPUT_CSV} ({len(rows)} rows)")


def cmd_enrich(args):
    ensure_dirs()
    leads = read_leads(args.category)
    if not leads: print("No leads found."); return
    if args.top and args.top > 0: leads = leads[:args.top]
    print(f"Enriching {len(leads)} leads (workers={MAX_WORKERS}, force={args.force})")
    if args.category: print(f"Category: {args.category}")
    all_leads = read_leads(None)
    with open(INPUT_CSV, newline="", encoding="utf-8") as f: fieldnames = csv.DictReader(f).fieldnames or []

    enrichments, completed, errors, cached, total = {}, 0, 0, 0, len(leads)
    def worker(row): return row.get("domain","").strip(), enrich_lead(row, all_leads, args.force)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futs = {ex.submit(worker, r): r for r in leads}
        for fut in as_completed(futs):
            try:
                domain, result = fut.result()
                enrichments[domain] = result; completed += 1
                st = result.get("enrichment_status", "")
                if st == "CACHED": cached += 1
                elif st.startswith("SKIP"): errors += 1
                pct = completed / total * 100
                filled = int(30 * completed / total)
                sys.stdout.write(f"\r[{'=' * filled}{'-' * (30 - filled)}] {pct:5.1f}% "
                                 f"({completed}/{total}) new={completed-cached-errors} cached={cached}")
                sys.stdout.flush()
            except Exception as e:
                errors += 1; completed += 1; print(f"\nError: {e}")

    print()
    write_enriched(leads, enrichments, fieldnames)
    print(f"Done. Enriched={completed-cached-errors}, Cached={cached}, Skipped={errors}")


def cmd_status(args):
    ensure_dirs()
    leads = read_leads(None)
    total = len(leads)
    cache_files = [f for f in os.listdir(CACHE_DIR) if f.endswith(".json")] if os.path.exists(CACHE_DIR) else []
    cached_count = len(cache_files)

    # Output stats
    enr_count, with_rating, with_social = 0, 0, 0
    out_cats = {}
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                enr_count += 1; cat = row.get("category", "?")
                out_cats.setdefault(cat, {"enriched": 0, "rating": 0, "social": 0})
                if row.get("enrichment_status") == "ENRICHED": out_cats[cat]["enriched"] += 1
                if row.get("google_rating", ""): with_rating += 1; out_cats[cat]["rating"] += 1
                if row.get("has_facebook") == "YES" or row.get("has_instagram") == "YES":
                    with_social += 1; out_cats[cat]["social"] += 1

    # Cache timestamps
    cache_oldest = cache_newest = None
    if cache_files:
        ts = [os.path.getmtime(os.path.join(CACHE_DIR, f)) for f in cache_files]
        cache_oldest = datetime.fromtimestamp(min(ts)).strftime("%Y-%m-%d %H:%M")
        cache_newest = datetime.fromtimestamp(max(ts)).strftime("%Y-%m-%d %H:%M")

    # Input category counts
    in_cats = {}
    for l in leads: in_cats[l.get("category","?")] = in_cats.get(l.get("category","?"), 0) + 1

    pct = (cached_count / total * 100) if total else 0
    filled = int(30 * cached_count / total) if total else 0
    remaining = total - cached_count
    est = (remaining * 2.0) / MAX_WORKERS / 60

    print("=" * 65)
    print("  LEAD ENRICHMENT ENGINE - Status Report")
    print("=" * 65)
    print(f"\n  Input:  {INPUT_CSV}")
    print(f"  Output: {OUTPUT_CSV}")
    print(f"  Cache:  {CACHE_DIR}")
    print(f"\n  Total leads:  {total:,}")
    print(f"  Cached:       {cached_count:,} ({pct:.1f}%)")
    print(f"  Enriched CSV: {enr_count:,} rows")
    print(f"\n  Progress: [{'=' * filled}{'-' * (30 - filled)}] {pct:.1f}%")
    print(f"  Remaining: {remaining:,} leads (~{est:.0f} min to enrich)")
    if enr_count:
        print(f"\n  With rating: {with_rating:,} ({with_rating/enr_count*100:.1f}%)")
        print(f"  With social: {with_social:,} ({with_social/enr_count*100:.1f}%)")
    if cache_oldest:
        print(f"\n  Cache oldest: {cache_oldest}  newest: {cache_newest}")
    print(f"\n  {'Category':<28} {'Input':>7} {'Enriched':>9}")
    print(f"  {'-'*28} {'-'*7} {'-'*9}")
    for cat in sorted(in_cats, key=lambda x: -in_cats[x]):
        e = out_cats.get(cat, {}).get("enriched", 0)
        print(f"  {cat:<28} {in_cats[cat]:>7,} {e:>9,}")
    if not os.path.exists(OUTPUT_CSV):
        print(f"\n  Run: python3 {sys.argv[0]} --enrich")
    print()


def main():
    p = argparse.ArgumentParser(description="Lead Enrichment Engine")
    p.add_argument("--enrich", action="store_true", help="Run enrichment")
    p.add_argument("--status", action="store_true", help="Show progress")
    p.add_argument("--top", type=int, default=0, help="Limit to top N")
    p.add_argument("--force", action="store_true", help="Re-enrich cached")
    p.add_argument("--category", type=str, default=None, help="Filter category")
    a = p.parse_args()
    if not a.enrich and not a.status: p.print_help(); return
    if a.status: cmd_status(a)
    if a.enrich: cmd_enrich(a)

if __name__ == "__main__":
    main()
