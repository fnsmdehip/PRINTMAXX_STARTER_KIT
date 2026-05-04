#!/usr/bin/env python3
"""
Targeted build+deploy for OpenClaw leads.
Builds HTML + deploys to surge for:
  1. F/D leads with email, not yet built or built locally only (priority)
  2. F/D leads without email, not yet built (secondary)
Capped at MAX_BUILDS per run to avoid runaway.
"""

import csv
import sys
import subprocess
import random
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "AUTOMATIONS"))

LEADS_CSV = PROJECT_ROOT / "AUTOMATIONS/leads/openclaw/openclaw_leads.csv"
BUILD_DIR  = PROJECT_ROOT / "AUTOMATIONS/leads/openclaw/_sites"
LOG_FILE   = PROJECT_ROOT / "AUTOMATIONS/leads/openclaw/openclaw.log"
MAX_BUILDS = int(sys.argv[1]) if len(sys.argv) > 1 else 60

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def slugify(text):
    import re
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text[:60]

def safe_path(p):
    resolved = Path(p).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} outside project root")
    return resolved

def get_npx():
    for candidate in ["/usr/local/bin/npx", "/opt/homebrew/bin/npx"]:
        if Path(candidate).exists():
            return candidate
    result = subprocess.run(["which", "npx"], capture_output=True, text=True)
    return result.stdout.strip() or "npx"

NPX = get_npx()

def build_html(row):
    biz = row.get("business_name", "Local Business")
    city = row.get("city", "")
    cat = row.get("category", "service")
    phone = row.get("phone", "")
    addr = row.get("address", "")
    colors = [
        ("2563EB", "1E40AF"), ("059669", "065F46"), ("DC2626", "991B1B"),
        ("7C3AED", "5B21B6"), ("D97706", "92400E"),
    ]
    accent, dark = random.choice(colors)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{biz} | {city}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#111}}
header{{background:#{accent};color:#fff;padding:1.5rem 1rem;text-align:center}}
header h1{{font-size:1.8rem;font-weight:700}}
header p{{margin-top:.4rem;opacity:.9}}
.hero{{background:#f8fafc;padding:2.5rem 1rem;text-align:center;border-bottom:3px solid #{accent}}}
.hero h2{{font-size:1.5rem;color:#{dark};margin-bottom:.8rem}}
.hero p{{max-width:560px;margin:0 auto;line-height:1.6;color:#444}}
.cta-btn{{display:inline-block;margin-top:1.2rem;background:#{accent};color:#fff;padding:.8rem 2rem;border-radius:.5rem;text-decoration:none;font-weight:600;font-size:1rem}}
.services{{padding:2rem 1rem;max-width:800px;margin:0 auto}}
.services h3{{text-align:center;font-size:1.3rem;color:#{dark};margin-bottom:1.2rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem}}
.card{{background:#fff;border:1px solid #e2e8f0;border-radius:.75rem;padding:1.2rem;box-shadow:0 1px 4px rgba(0,0,0,.07)}}
.card h4{{color:#{accent};margin-bottom:.4rem}}
.card p{{font-size:.9rem;color:#555;line-height:1.5}}
.contact{{background:#{accent};color:#fff;padding:2rem 1rem;text-align:center}}
.contact h3{{font-size:1.3rem;margin-bottom.8rem}}
.contact p{{margin-top:.5rem;font-size:1.1rem}}
.contact a{{color:#fff;text-decoration:underline}}
footer{{background:#1e293b;color:#94a3b8;text-align:center;padding:1rem;font-size:.85rem}}
.badge{{display:inline-block;background:rgba(255,255,255,.2);border-radius:2rem;padding:.2rem .8rem;font-size:.75rem;margin-top:.5rem}}
</style>
</head>
<body>
<header>
  <h1>{biz}</h1>
  <p>{city}{" · " + cat.title() if cat else ""}</p>
  <div class="badge">⚡ Free Preview — Built by PRINTMAXX</div>
</header>
<section class="hero">
  <h2>Professional {cat.title() if cat else "Services"} in {city}</h2>
  <p>Trusted, reliable, and ready to serve your community. We take pride in delivering quality results every time.</p>
  {"<a href='tel:" + phone + "' class='cta-btn'>📞 Call Now: " + phone + "</a>" if phone else "<a href='#contact' class='cta-btn'>📞 Get a Free Quote</a>"}
</section>
<section class="services">
  <h3>What We Offer</h3>
  <div class="grid">
    <div class="card"><h4>Fast Response</h4><p>Same-day or next-day availability for most requests.</p></div>
    <div class="card"><h4>Fair Pricing</h4><p>Transparent quotes with no hidden fees. Pay only what was agreed.</p></div>
    <div class="card"><h4>Local Experts</h4><p>Serving {city} and surrounding areas with pride.</p></div>
    <div class="card"><h4>Satisfaction Guaranteed</h4><p>We don't leave until the job is done right.</p></div>
  </div>
</section>
<section class="contact" id="contact">
  <h3>Get In Touch</h3>
  {"<p>📞 <a href='tel:" + phone + "'>" + phone + "</a></p>" if phone else ""}
  {"<p>📍 " + addr + "</p>" if addr else ""}
  <p style="margin-top:1rem;font-size:.9rem;opacity:.8">Available Mon–Sat · Fast callbacks guaranteed</p>
</section>
<footer>
  <p>© {datetime.now().year} {biz} · {city}</p>
  <p style="margin-top:.3rem;font-size:.75rem">Preview generated by PRINTMAXX Web Services · printmaxx.co</p>
</footer>
</body>
</html>"""

def deploy_surge(site_dir, domain_slug):
    import os
    env = os.environ.copy()
    for slug in [domain_slug, f"{domain_slug}-pmx", f"{domain_slug}-2"]:
        domain = f"{slug}.surge.sh"
        try:
            r = subprocess.run(
                [NPX, "surge", "--project", str(site_dir), "--domain", domain],
                capture_output=True, text=True, timeout=60,
                cwd=str(PROJECT_ROOT), stdin=subprocess.DEVNULL, env=env
            )
            combined = (r.stdout or "") + (r.stderr or "")
            if r.returncode == 0 and "Success" in combined:
                return f"https://{domain}", True
            if "do not have permission" in combined:
                # Verify via HTTP
                import urllib.request, ssl
                try:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    resp = urllib.request.urlopen(f"https://{domain}", timeout=8, context=ctx)
                    if resp.status == 200:
                        return f"https://{domain}", True
                except Exception:
                    pass
                continue
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            log(f"  surge error {slug}: {e}")
            return f"https://{domain_slug}.surge.sh", False
    return f"https://{domain_slug}.surge.sh", False

def main():
    rows = list(csv.DictReader(open(LEADS_CSV)))
    LEADS_HEADERS = list(rows[0].keys()) if rows else []

    # Classify leads
    needs_work = []
    for r in rows:
        if r.get("grade") not in ("D", "F"):
            continue
        purl = r.get("preview_url", "").strip()
        if purl.startswith("https://") and "surge.sh" in purl:
            continue  # already deployed
        priority = 1 if r.get("email") else 2
        needs_work.append((priority, r))

    needs_work.sort(key=lambda x: x[0])
    log(f"Needs work: {len(needs_work)} leads ({sum(1 for p,_ in needs_work if p==1)} with email)")

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    built = 0
    deployed = 0
    skipped = 0

    row_index = {r.get("website","") + r.get("business_name",""): i for i, r in enumerate(rows)}

    for priority, row in needs_work[:MAX_BUILDS]:
        biz_slug = slugify(row.get("business_name", f"biz-{built}"))
        city_slug = slugify(row.get("city", "local"))
        domain_slug = f"{biz_slug}-{city_slug}"

        site_dir = BUILD_DIR / domain_slug
        safe_path(site_dir)
        site_dir.mkdir(parents=True, exist_ok=True)

        html = build_html(row)
        index = site_dir / "index.html"
        index.write_text(html)

        label = f"[{'has-email' if priority==1 else 'no-email'}]"
        log(f"  Built {label}: {domain_slug}")

        url, ok = deploy_surge(site_dir, domain_slug)
        if ok:
            row["preview_url"] = url
            row["status"] = "site_built"
            log(f"  Deployed: {url}")
            deployed += 1
        else:
            row["preview_url"] = f"file://{index}"
            row["status"] = "site_built"
            log(f"  Local only (surge failed): {index}")

        # Update rows list
        key = row.get("website","") + row.get("business_name","")
        if key in row_index:
            rows[row_index[key]] = row
        built += 1

    # Rewrite CSV
    with open(LEADS_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEADS_HEADERS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    log(f"Done. Built: {built} | Deployed to surge: {deployed} | Skipped: {skipped}")

    # Show status
    rows2 = list(csv.DictReader(open(LEADS_CSV)))
    surge_count = sum(1 for r in rows2 if r.get("preview_url","").startswith("https://") and "surge.sh" in r.get("preview_url",""))
    print(f"\nTotal surge deployments: {surge_count}")

if __name__ == "__main__":
    main()
