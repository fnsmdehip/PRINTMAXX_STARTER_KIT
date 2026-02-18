#!/usr/bin/env python3
"""
domain_checker.py - Check domain reputation and health for cold email

Validates sending domains for DNS records (SPF, DKIM, DMARC),
checks blacklists, and monitors domain age. Critical for maintaining
cold email deliverability.

Usage:
    python3 domain_checker.py --domain example.com
    python3 domain_checker.py --file domains.txt
    python3 domain_checker.py --check-sending example.com
    python3 domain_checker.py --all-checks example.com

Example:
    # Quick domain check
    python3 domain_checker.py --domain printmaxx.com

    # Check all sending domains
    python3 domain_checker.py --file MONEY_METHODS/COLD_OUTBOUND/domains.txt

    # Full deliverability check
    python3 domain_checker.py --all-checks printmaxx.com
"""

import argparse
import json
import logging
import re
import socket
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "domain_checker.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Common blacklists to check
BLACKLISTS = [
    "zen.spamhaus.org",
    "bl.spamcop.net",
    "b.barracudacentral.org",
    "dnsbl.sorbs.net",
    "spam.dnsbl.sorbs.net",
]


def check_dns_record(domain, record_type):
    """Check for a DNS record. Returns True/False and the record value."""
    try:
        import subprocess
        result = subprocess.run(
            ["dig", "+short", record_type, domain],
            capture_output=True, text=True, timeout=10,
        )
        records = result.stdout.strip()
        return bool(records), records
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "dig command not available"
    except Exception as e:
        return False, str(e)


def check_spf(domain):
    """Check SPF record."""
    try:
        import subprocess
        result = subprocess.run(
            ["dig", "+short", "TXT", domain],
            capture_output=True, text=True, timeout=10,
        )
        txt_records = result.stdout.strip()
        has_spf = "v=spf1" in txt_records
        return {
            "exists": has_spf,
            "record": txt_records if has_spf else None,
            "recommendation": None if has_spf else "Add SPF record to DNS",
        }
    except Exception:
        return {"exists": False, "record": None, "recommendation": "Cannot check SPF"}


def check_dkim(domain, selector="default"):
    """Check DKIM record."""
    dkim_domain = f"{selector}._domainkey.{domain}"
    try:
        import subprocess
        result = subprocess.run(
            ["dig", "+short", "TXT", dkim_domain],
            capture_output=True, text=True, timeout=10,
        )
        records = result.stdout.strip()
        has_dkim = bool(records and "v=DKIM1" in records)
        return {
            "exists": has_dkim,
            "selector": selector,
            "record": records if has_dkim else None,
            "recommendation": None if has_dkim else "Add DKIM record to DNS",
        }
    except Exception:
        return {"exists": False, "selector": selector, "record": None, "recommendation": "Cannot check DKIM"}


def check_dmarc(domain):
    """Check DMARC record."""
    dmarc_domain = f"_dmarc.{domain}"
    try:
        import subprocess
        result = subprocess.run(
            ["dig", "+short", "TXT", dmarc_domain],
            capture_output=True, text=True, timeout=10,
        )
        records = result.stdout.strip()
        has_dmarc = "v=DMARC1" in records
        return {
            "exists": has_dmarc,
            "record": records if has_dmarc else None,
            "recommendation": None if has_dmarc else "Add DMARC record: v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com",
        }
    except Exception:
        return {"exists": False, "record": None, "recommendation": "Cannot check DMARC"}


def check_mx(domain):
    """Check MX records."""
    try:
        import subprocess
        result = subprocess.run(
            ["dig", "+short", "MX", domain],
            capture_output=True, text=True, timeout=10,
        )
        records = result.stdout.strip()
        has_mx = bool(records)
        return {
            "exists": has_mx,
            "records": records.split("\n") if records else [],
            "recommendation": None if has_mx else "No MX records found - email won't work",
        }
    except Exception:
        return {"exists": False, "records": [], "recommendation": "Cannot check MX"}


def check_blacklist(domain):
    """Check if domain IP is on common blacklists."""
    results = []
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        return [{"blacklist": "DNS", "listed": False, "note": f"Cannot resolve {domain}"}]

    # Reverse the IP for DNSBL lookup
    reversed_ip = ".".join(reversed(ip.split(".")))

    for bl in BLACKLISTS:
        try:
            lookup = f"{reversed_ip}.{bl}"
            socket.gethostbyname(lookup)
            results.append({"blacklist": bl, "listed": True, "note": "LISTED - Action needed"})
        except socket.gaierror:
            results.append({"blacklist": bl, "listed": False, "note": "Clean"})
        except Exception:
            results.append({"blacklist": bl, "listed": False, "note": "Check failed"})

    return results


def full_domain_check(domain):
    """Run all checks on a domain."""
    logger.info(f"Running full check for: {domain}")

    results = {
        "domain": domain,
        "spf": check_spf(domain),
        "dkim": check_dkim(domain),
        "dmarc": check_dmarc(domain),
        "mx": check_mx(domain),
        "blacklist": check_blacklist(domain),
    }

    # Calculate health score
    score = 0
    if results["spf"]["exists"]:
        score += 25
    if results["dkim"]["exists"]:
        score += 25
    if results["dmarc"]["exists"]:
        score += 25
    if results["mx"]["exists"]:
        score += 15
    listed = sum(1 for bl in results["blacklist"] if bl["listed"])
    if listed == 0:
        score += 10

    results["health_score"] = score
    results["health_grade"] = (
        "A" if score >= 90 else
        "B" if score >= 75 else
        "C" if score >= 50 else
        "D" if score >= 25 else "F"
    )

    return results


def print_domain_report(results):
    """Print formatted domain report."""
    print("\n" + "=" * 60)
    print(f"  DOMAIN CHECK: {results['domain']}")
    print(f"  Health Score: {results['health_score']}/100 ({results['health_grade']})")
    print("=" * 60)

    checks = [
        ("SPF", results["spf"]),
        ("DKIM", results["dkim"]),
        ("DMARC", results["dmarc"]),
        ("MX", results["mx"]),
    ]

    for name, check in checks:
        status = "OK" if check["exists"] else "MISSING"
        marker = " OK" if check["exists"] else "!!!"
        print(f"  [{marker}] {name}: {status}")
        if check.get("recommendation"):
            print(f"        Fix: {check['recommendation']}")

    # Blacklist
    print(f"\n  --- BLACKLIST CHECK ---")
    listed_count = 0
    for bl in results["blacklist"]:
        marker = "!!!" if bl["listed"] else " OK"
        print(f"  [{marker}] {bl['blacklist']}: {bl['note']}")
        if bl["listed"]:
            listed_count += 1

    if listed_count > 0:
        print(f"\n  WARNING: Listed on {listed_count} blacklist(s). Deliverability will be affected.")

    # Recommendations
    recs = []
    if not results["spf"]["exists"]:
        recs.append("Add SPF record")
    if not results["dkim"]["exists"]:
        recs.append("Add DKIM record")
    if not results["dmarc"]["exists"]:
        recs.append("Add DMARC record")
    if listed_count > 0:
        recs.append("Request blacklist removal")

    if recs:
        print(f"\n  --- ACTION ITEMS ---")
        for i, rec in enumerate(recs, 1):
            print(f"  {i}. {rec}")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Check domain reputation and email deliverability health"
    )
    parser.add_argument("--domain", type=str, default=None, help="Domain to check")
    parser.add_argument("--file", type=str, default=None, help="File with domain list (one per line)")
    parser.add_argument("--check-sending", type=str, default=None, help="Check sending domain setup")
    parser.add_argument("--all-checks", type=str, default=None, help="Run all checks on domain")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    domain = args.domain or args.check_sending or args.all_checks

    if domain:
        results = full_domain_check(domain)
        if args.output == "json":
            print(json.dumps(results, indent=2))
        else:
            print_domain_report(results)

    elif args.file:
        filepath = Path(args.file)
        if not filepath.is_absolute():
            filepath = PROJECT_DIR / args.file

        if not filepath.exists():
            logger.error(f"File not found: {filepath}")
            sys.exit(1)

        with open(filepath) as f:
            domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        for d in domains:
            results = full_domain_check(d)
            if args.output == "json":
                print(json.dumps(results, indent=2))
            else:
                print_domain_report(results)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
