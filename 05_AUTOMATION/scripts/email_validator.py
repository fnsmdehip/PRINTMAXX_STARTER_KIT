#!/usr/bin/env python3
"""
email_validator.py - Validate email lists for cold outreach

Checks email addresses for format validity, disposable domains,
role-based addresses, and common typos. Outputs clean and risky lists.

Usage:
    python3 email_validator.py --file emails.csv --column email
    python3 email_validator.py --email test@example.com
    python3 email_validator.py --file LEDGER/leads.csv --column email --output clean.csv

Example:
    # Validate a single email
    python3 email_validator.py --email john@company.com

    # Validate an email list
    python3 email_validator.py --file leads.csv --column email

    # Output clean emails only
    python3 email_validator.py --file leads.csv --column email --output clean_leads.csv
"""

import argparse
import csv
import json
import logging
import re
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "email_validator.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Disposable email domains (common ones)
DISPOSABLE_DOMAINS = {
    "mailinator.com", "guerrillamail.com", "tempmail.com", "throwaway.email",
    "10minutemail.com", "trashmail.com", "yopmail.com", "fakeinbox.com",
    "sharklasers.com", "guerrillamailblock.com", "grr.la", "dispostable.com",
    "maildrop.cc", "temp-mail.org", "getnada.com", "emailondeck.com",
    "mohmal.com", "tempr.email", "discard.email", "mailnesia.com",
}

# Role-based prefixes (less likely to be real people)
ROLE_PREFIXES = {
    "admin", "info", "support", "help", "sales", "contact", "office",
    "billing", "service", "webmaster", "postmaster", "hostmaster",
    "abuse", "noreply", "no-reply", "marketing", "team", "hello",
    "general", "enquiries", "feedback", "hr", "jobs", "careers",
}

# Common typo domains
TYPO_FIXES = {
    "gmial.com": "gmail.com",
    "gamil.com": "gmail.com",
    "gmal.com": "gmail.com",
    "gnail.com": "gmail.com",
    "gmail.con": "gmail.com",
    "gmail.co": "gmail.com",
    "yaho.com": "yahoo.com",
    "yahooo.com": "yahoo.com",
    "yahoo.con": "yahoo.com",
    "hotmai.com": "hotmail.com",
    "hotmal.com": "hotmail.com",
    "hotmail.con": "hotmail.com",
    "outlok.com": "outlook.com",
    "outloo.com": "outlook.com",
}

# Email regex pattern
EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)


def validate_email(email):
    """Validate a single email address. Returns dict with results."""
    email = email.strip().lower()
    result = {
        "email": email,
        "valid": True,
        "issues": [],
        "risk_level": "LOW",
        "suggested_fix": None,
    }

    # Basic format check
    if not email:
        result["valid"] = False
        result["issues"].append("empty")
        result["risk_level"] = "INVALID"
        return result

    if not EMAIL_PATTERN.match(email):
        result["valid"] = False
        result["issues"].append("invalid_format")
        result["risk_level"] = "INVALID"
        return result

    local_part, domain = email.rsplit("@", 1)

    # Check for typo domains
    if domain in TYPO_FIXES:
        result["issues"].append(f"likely_typo: {domain}")
        result["suggested_fix"] = f"{local_part}@{TYPO_FIXES[domain]}"
        result["risk_level"] = "MEDIUM"

    # Check disposable domain
    if domain in DISPOSABLE_DOMAINS:
        result["issues"].append("disposable_domain")
        result["risk_level"] = "HIGH"

    # Check role-based prefix
    prefix = local_part.split(".")[0]
    if prefix in ROLE_PREFIXES:
        result["issues"].append(f"role_based: {prefix}")
        result["risk_level"] = "MEDIUM"

    # Check for too many dots/special chars
    if local_part.count(".") > 3:
        result["issues"].append("unusual_format")

    # Check domain TLD
    tld = domain.split(".")[-1]
    if len(tld) > 10:
        result["issues"].append("unusual_tld")
        result["risk_level"] = "MEDIUM"

    # Catch-all detection (basic heuristic)
    if local_part in ("test", "testing", "asdf", "abc", "123"):
        result["issues"].append("test_address")
        result["risk_level"] = "HIGH"

    if not result["issues"]:
        result["issues"].append("clean")

    return result


def validate_file(filepath, email_column="email"):
    """Validate all emails in a CSV file."""
    path = Path(filepath)
    if not path.is_absolute():
        path = PROJECT_DIR / filepath

    if not path.exists():
        logger.error(f"File not found: {path}")
        return []

    results = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if email_column not in (reader.fieldnames or []):
            logger.error(f"Column '{email_column}' not found. Available: {reader.fieldnames}")
            return []

        for row in reader:
            email = row.get(email_column, "")
            if email:
                result = validate_email(email)
                result["row_data"] = row
                results.append(result)

    return results


def print_results(results):
    """Print validation results."""
    print("\n" + "=" * 70)
    print("  EMAIL VALIDATION RESULTS")
    print("=" * 70)

    valid = [r for r in results if r["valid"]]
    invalid = [r for r in results if not r["valid"]]
    high_risk = [r for r in results if r["risk_level"] == "HIGH"]
    med_risk = [r for r in results if r["risk_level"] == "MEDIUM"]
    fixable = [r for r in results if r["suggested_fix"]]

    print(f"\n  Total: {len(results)}")
    print(f"  Valid: {len(valid)}")
    print(f"  Invalid: {len(invalid)}")
    print(f"  High Risk: {len(high_risk)}")
    print(f"  Medium Risk: {len(med_risk)}")
    print(f"  Fixable Typos: {len(fixable)}")

    if invalid:
        print(f"\n  --- INVALID EMAILS ---")
        for r in invalid[:10]:
            print(f"    {r['email']}: {', '.join(r['issues'])}")

    if high_risk:
        print(f"\n  --- HIGH RISK ---")
        for r in high_risk[:10]:
            print(f"    {r['email']}: {', '.join(r['issues'])}")

    if fixable:
        print(f"\n  --- SUGGESTED FIXES ---")
        for r in fixable[:10]:
            print(f"    {r['email']} -> {r['suggested_fix']}")

    print("=" * 70)


def write_clean_output(results, output_path, include_medium=False):
    """Write clean emails to output file."""
    clean = [
        r for r in results
        if r["valid"] and r["risk_level"] in (["LOW"] + (["MEDIUM"] if include_medium else []))
    ]

    if not clean:
        logger.warning("No clean emails to write")
        return

    # Get fieldnames from first result's row data
    sample_row = clean[0].get("row_data", {})
    fieldnames = list(sample_row.keys())

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in clean:
            writer.writerow(r["row_data"])

    logger.info(f"Wrote {len(clean)} clean emails to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate email addresses for cold outreach quality"
    )
    parser.add_argument("--email", type=str, default=None, help="Validate a single email")
    parser.add_argument("--file", type=str, default=None, help="CSV file with emails")
    parser.add_argument("--column", type=str, default="email", help="Email column name")
    parser.add_argument("--output", type=str, default=None, help="Output clean list to file")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.email:
        result = validate_email(args.email)
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"\n  Email: {result['email']}")
            print(f"  Valid: {result['valid']}")
            print(f"  Risk: {result['risk_level']}")
            print(f"  Issues: {', '.join(result['issues'])}")
            if result["suggested_fix"]:
                print(f"  Suggested: {result['suggested_fix']}")
    elif args.file:
        results = validate_file(args.file, args.column)
        if results:
            if args.output:
                write_clean_output(results, args.output)
            if args.format == "json":
                print(json.dumps([{k: v for k, v in r.items() if k != "row_data"} for r in results], indent=2))
            else:
                print_results(results)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
