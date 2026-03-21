#!/usr/bin/env python3

from __future__ import annotations
"""Email Domain Health Checker - Cold outreach readiness scoring.

Checks SPF, DKIM, DMARC, MX, blacklist status, and domain age.
Scores 0-100 with letter grade. Uses only macOS stdlib + dig/whois.

Usage:
    python3 email_domain_health.py --check gmail.com
    python3 email_domain_health.py --check-leads --top 10
    python3 email_domain_health.py --check gmail.com --report
    python3 email_domain_health.py --fix-guide
"""
import argparse, csv, json, os, re, subprocess, sys
from datetime import datetime
from pathlib import Path

# --- Colors ---
G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"; B = "\033[94m"; W = "\033[97m"; D = "\033[0m"
BOLD = "\033[1m"

SCRIPT_DIR = Path(__file__).resolve().parent
LEADS_CSV = SCRIPT_DIR / "leads" / "qualified" / "HOT_LEADS_QUALIFIED.csv"
OUTPUT_DIR = SCRIPT_DIR / "output"
DKIM_SELECTORS = ["google", "default", "k1", "selector1", "selector2", "dkim"]
BLACKLISTS = ["zen.spamhaus.org", "bl.spamcop.net", "b.barracudacentral.org", "dnsbl.sorbs.net"]


def run(cmd, timeout=8):
    """Run shell command, return stdout or empty string on failure."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""


def check_spf(domain):
    """Check SPF record. Returns (pass:bool, detail:str)."""
    out = run(["dig", "+short", "TXT", domain])
    for line in out.splitlines():
        if "v=spf1" in line.lower():
            clean = line.strip('" ')
            has_all = "-all" in clean or "~all" in clean
            return True, f"Found: {clean[:80]}" + ("" if has_all else f" {Y}(missing -all){D}")
    return False, "No SPF record found"


def check_dkim(domain):
    """Probe common DKIM selectors. Returns (pass:bool, detail:str)."""
    found = []
    for sel in DKIM_SELECTORS:
        out = run(["dig", "+short", "TXT", f"{sel}._domainkey.{domain}"])
        if out and "NXDOMAIN" not in out and out.strip('" '):
            found.append(sel)
    if found:
        return True, f"DKIM selectors responding: {', '.join(found)}"
    return False, f"No DKIM found (probed: {', '.join(DKIM_SELECTORS)})"


def check_dmarc(domain):
    """Check DMARC record. Returns (pass:bool, detail:str)."""
    out = run(["dig", "+short", "TXT", f"_dmarc.{domain}"])
    for line in out.splitlines():
        if "v=dmarc1" in line.lower():
            clean = line.strip('" ')
            policy = "none"
            m = re.search(r'p=(\w+)', clean)
            if m:
                policy = m.group(1)
            severity = {"reject": G + "reject" + D, "quarantine": Y + "quarantine" + D}
            ps = severity.get(policy, R + policy + D)
            return True, f"Policy: {ps} | {clean[:70]}"
    return False, "No DMARC record found"


def check_mx(domain):
    """Check MX records. Returns (pass:bool, detail:str)."""
    out = run(["dig", "+short", "MX", domain])
    records = [l.strip() for l in out.splitlines() if l.strip() and ";" not in l]
    if records:
        top = records[:3]
        return True, f"{len(records)} MX record(s): {', '.join(top)}"
    return False, "No MX records found"


def check_blacklists(domain):
    """Check domain against 4 DNSBLs via dig. Returns (pass:bool, detail:str)."""
    # Resolve domain to IP first
    ip_out = run(["dig", "+short", "A", domain])
    ip = None
    for line in ip_out.splitlines():
        line = line.strip()
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', line):
            ip = line
            break
    if not ip:
        return True, "Could not resolve IP (skipped blacklist check)"

    parts = ip.split(".")
    reversed_ip = ".".join(reversed(parts))
    listed = []
    for bl in BLACKLISTS:
        out = run(["dig", "+short", f"{reversed_ip}.{bl}"], timeout=5)
        if out and re.match(r'^\d+\.\d+\.\d+\.\d+', out.splitlines()[0].strip()):
            listed.append(bl)

    if listed:
        return False, f"LISTED on: {R}{', '.join(listed)}{D} (IP: {ip})"
    return True, f"Clean on all {len(BLACKLISTS)} DNSBLs (IP: {ip})"


def check_domain_age(domain):
    """Approximate domain age via whois. Returns (pass:bool, detail:str)."""
    out = run(["whois", domain], timeout=10)
    if not out:
        return False, "whois lookup failed"

    patterns = [
        r'Creation Date:\s*(.+)',
        r'Created On:\s*(.+)',
        r'Registration Date:\s*(.+)',
        r'created:\s*(.+)',
        r'Domain Name Commencement Date:\s*(.+)',
    ]
    for pat in patterns:
        m = re.search(pat, out, re.IGNORECASE)
        if m:
            raw = m.group(1).strip()
            for fmt in ["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d",
                        "%d-%b-%Y", "%Y/%m/%d", "%a %b %d %H:%M:%S %Z %Y"]:
                try:
                    dt = datetime.strptime(raw[:25].rstrip("Z "), fmt.replace("%z", "").rstrip())
                    age_days = (datetime.now() - dt).days
                    age_years = age_days / 365.25
                    if age_days > 365:
                        return True, f"~{age_years:.1f} years old (created {dt.strftime('%Y-%m-%d')})"
                    elif age_days > 90:
                        return True, f"{Y}~{age_days} days old{D} (created {dt.strftime('%Y-%m-%d')})"
                    else:
                        return False, f"{R}Only ~{age_days} days old{D} - too new for cold outreach"
                except ValueError:
                    continue
            return True, f"Created: {raw[:30]} (could not parse exact age)"
    return False, "Could not determine domain age"


def score_domain(results):
    """Score 0-100 from check results dict. Returns (score, grade)."""
    weights = {"spf": 25, "dkim": 20, "dmarc": 20, "mx": 15, "blacklist": 15, "age": 5}
    score = 0
    for key, (passed, _) in results.items():
        if passed:
            score += weights.get(key, 0)
    grade = "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 50 else "D" if score >= 30 else "F"
    return score, grade


def grade_color(grade):
    return {
        "A": G, "B": G, "C": Y, "D": R, "F": R
    }.get(grade, D)


def check_domain(domain, verbose=True):
    """Run all 6 checks on a domain. Returns (score, grade, results_dict)."""
    checks = [
        ("spf", "SPF Record", check_spf),
        ("dkim", "DKIM Selectors", check_dkim),
        ("dmarc", "DMARC Record", check_dmarc),
        ("mx", "MX Records", check_mx),
        ("blacklist", "Blacklist Check", check_blacklists),
        ("age", "Domain Age", check_domain_age),
    ]
    results = {}
    if verbose:
        print(f"\n{BOLD}{W}{'='*60}")
        print(f"  Email Domain Health: {B}{domain}{D}")
        print(f"{W}{'='*60}{D}\n")

    for key, label, fn in checks:
        passed, detail = fn(domain)
        results[key] = (passed, detail)
        if verbose:
            icon = f"{G}PASS{D}" if passed else f"{R}FAIL{D}"
            print(f"  [{icon}] {label:18s} {detail}")

    sc, gr = score_domain(results)
    gc = grade_color(gr)
    if verbose:
        print(f"\n{W}{'─'*60}{D}")
        bar_filled = int(sc / 2)
        bar = f"{gc}{'█' * bar_filled}{D}{'░' * (50 - bar_filled)}"
        print(f"  Score: {gc}{BOLD}{sc}/100{D}  Grade: {gc}{BOLD}{gr}{D}")
        print(f"  [{bar}]")
        readiness = f"{G}READY for cold outreach{D}" if sc >= 70 else \
                    f"{Y}NEEDS FIXES before outreach{D}" if sc >= 40 else \
                    f"{R}NOT READY - major DNS issues{D}"
        print(f"  Outreach Readiness: {readiness}\n")
    return sc, gr, results


def extract_email_domains(csv_path, top_n=None):
    """Extract unique email domains from leads CSV."""
    domains = set()
    if not csv_path.exists():
        print(f"{R}CSV not found: {csv_path}{D}")
        return []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row.get("email", "")
            if "@" in email:
                d = email.split("@")[1].strip().lower()
                if d and "." in d:
                    domains.add(d)
    result = sorted(domains)
    if top_n:
        result = result[:top_n]
    return result


def check_leads(top_n=None):
    """Check all unique email domains from HOT_LEADS_QUALIFIED.csv."""
    domains = extract_email_domains(LEADS_CSV, top_n)
    if not domains:
        print(f"{R}No email domains found in {LEADS_CSV}{D}")
        return []
    print(f"\n{BOLD}{W}Checking {len(domains)} unique email domains from leads...{D}\n")
    all_results = []
    for i, d in enumerate(domains, 1):
        print(f"{W}[{i}/{len(domains)}]{D} ", end="", flush=True)
        sc, gr, res = check_domain(d, verbose=False)
        gc = grade_color(gr)
        icon = f"{G}PASS" if sc >= 70 else f"{Y}WARN" if sc >= 40 else f"{R}FAIL"
        print(f"{icon}{D} {d:40s} {gc}{BOLD}{sc:3d}/100 ({gr}){D}")
        all_results.append({"domain": d, "score": sc, "grade": gr, "results": res})

    # Summary
    avg = sum(r["score"] for r in all_results) / len(all_results) if all_results else 0
    ready = sum(1 for r in all_results if r["score"] >= 70)
    print(f"\n{W}{'─'*60}{D}")
    print(f"  Domains checked: {len(all_results)}")
    print(f"  Average score:   {avg:.0f}/100")
    print(f"  Outreach ready:  {G}{ready}{D}/{len(all_results)}")
    print(f"  Needs fixes:     {Y}{len(all_results) - ready}{D}/{len(all_results)}\n")
    return all_results


def generate_report(results_list, output_path=None):
    """Generate markdown report from results."""
    if not output_path:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / "email_health_report.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Email Domain Health Report", f"**Generated:** {now}\n",
        f"| Domain | Score | Grade | SPF | DKIM | DMARC | MX | Blacklist | Age |",
        f"|--------|-------|-------|-----|------|-------|----|-----------|----|",
    ]
    for r in sorted(results_list, key=lambda x: x["score"], reverse=True):
        row_cells = [r["domain"], f"{r['score']}/100", r["grade"]]
        for key in ["spf", "dkim", "dmarc", "mx", "blacklist", "age"]:
            passed = r["results"][key][0]
            row_cells.append("PASS" if passed else "FAIL")
        lines.append("| " + " | ".join(row_cells) + " |")

    avg = sum(r["score"] for r in results_list) / len(results_list) if results_list else 0
    ready = sum(1 for r in results_list if r["score"] >= 70)
    lines += [
        f"\n## Summary", f"- **Domains checked:** {len(results_list)}",
        f"- **Average score:** {avg:.0f}/100",
        f"- **Outreach ready (70+):** {ready}/{len(results_list)}",
        f"- **Needs fixes (<70):** {len(results_list) - ready}/{len(results_list)}",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n")
    print(f"{G}Report saved: {output_path}{D}")


def print_fix_guide():
    """Print step-by-step DNS fix instructions for common failures."""
    print(f"""
{BOLD}{W}{'='*60}
  DNS Fix Guide for Cold Email Deliverability
{'='*60}{D}

{BOLD}1. SPF Record{D} (TXT record on root domain)
   Add a TXT record to your domain DNS:
   {G}v=spf1 include:_spf.google.com ~all{D}  (for Google Workspace)
   {G}v=spf1 include:amazonses.com ~all{D}    (for Amazon SES)
   Use {B}https://www.spfwizard.net{D} to generate yours.
   Change ~all to -all for strict enforcement.

{BOLD}2. DKIM{D} (TXT record, selector._domainkey.yourdomain.com)
   - Google Workspace: Admin > Apps > Google Workspace > Gmail > Authenticate email
   - Amazon SES: Verified identities > your domain > DKIM
   - Instantly/Smartlead: Settings > Email accounts > DKIM setup
   Each provider gives you a TXT record to add.

{BOLD}3. DMARC{D} (TXT record at _dmarc.yourdomain.com)
   Start with monitoring:
   {G}v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com{D}
   After 2 weeks of clean reports, upgrade:
   {G}v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com{D}
   Then after another 2 weeks:
   {G}v=DMARC1; p=reject; rua=mailto:dmarc@yourdomain.com{D}

{BOLD}4. MX Records{D} (MX record on root domain)
   Google Workspace:
   {G}1  ASPMX.L.GOOGLE.COM.{D}
   {G}5  ALT1.ASPMX.L.GOOGLE.COM.{D}
   {G}5  ALT2.ASPMX.L.GOOGLE.COM.{D}

{BOLD}5. Blacklist Removal{D}
   - Spamhaus:  {B}https://check.spamhaus.org{D}
   - SpamCop:   {B}https://www.spamcop.net/bl.shtml{D}
   - Barracuda:  {B}https://www.barracudacentral.org/lookups{D}
   - SORBS:     {B}http://www.sorbs.net/lookup.shtml{D}
   Submit delisting request. Fix the root cause first.

{BOLD}6. Domain Age{D}
   New domains (<90 days) have poor reputation by default.
   Warm up for 2-4 weeks: send 5-10 real emails/day, get replies.
   Use tools: Instantly, Smartlead, or Lemwarm for automated warmup.

{W}{'─'*60}{D}
{BOLD}Warmup Sequence (new cold email domain):{D}
  Week 1: 5 emails/day, personal replies only
  Week 2: 10 emails/day, mix of warm + cold
  Week 3: 20 emails/day, start cold sequences
  Week 4: 30-50 emails/day, full cold outreach
  {Y}Never exceed 50 cold emails/day per inbox.{D}
""")


def main():
    parser = argparse.ArgumentParser(description="Email Domain Health Checker")
    parser.add_argument("--check", metavar="DOMAIN", help="Check a single domain")
    parser.add_argument("--check-leads", action="store_true", help="Check domains from HOT_LEADS_QUALIFIED.csv")
    parser.add_argument("--top", type=int, default=None, help="Limit to top N domains (with --check-leads)")
    parser.add_argument("--report", action="store_true", help="Generate markdown report")
    parser.add_argument("--fix-guide", action="store_true", help="Print DNS fix instructions")
    args = parser.parse_args()

    if not any([args.check, args.check_leads, args.fix_guide]):
        parser.print_help()
        sys.exit(1)

    if args.fix_guide:
        print_fix_guide()
        if not args.check and not args.check_leads:
            return

    results_list = []
    if args.check:
        sc, gr, res = check_domain(args.check)
        results_list.append({"domain": args.check, "score": sc, "grade": gr, "results": res})

    if args.check_leads:
        results_list = check_leads(args.top)

    if args.report and results_list:
        generate_report(results_list)


if __name__ == "__main__":
    main()
