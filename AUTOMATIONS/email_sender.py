#!/usr/bin/env python3
"""
PRINTMAXX Cold Email Sender
Sends personalized emails to leads from CSV files via Gmail SMTP or Resend API.

Setup:
  1. Gmail: Create App Password at myaccount.google.com/apppasswords
     Add to SECRETS/PAYMENT_INFO.md:
       GMAIL_ADDRESS=your@gmail.com
       GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

  2. Resend (optional): Get API key at resend.com/api-keys
     Add to SECRETS/PAYMENT_INFO.md:
       RESEND_API_KEY=re_xxxxx

Usage:
  # Preview emails (dry run, no sending)
  python3 email_sender.py --preview --leads AUTOMATIONS/leads/dentist_phoenix_leads.csv --industry dental

  # Send from pre-drafted outreach CSVs
  python3 email_sender.py --outreach AUTOMATIONS/outreach/dental_austin_tx_leads_emails_step1.csv

  # Send to raw leads with auto-generated email
  python3 email_sender.py --leads AUTOMATIONS/leads/dentist_phoenix_leads.csv --industry dental

  # Send with custom template
  python3 email_sender.py --leads AUTOMATIONS/leads/dentist_phoenix_leads.csv --template my_template.txt

  # Limit sends per run
  python3 email_sender.py --outreach emails.csv --max-sends 20

  # Use Resend API instead of Gmail
  python3 email_sender.py --outreach emails.csv --provider resend

  # Stats on all lead files
  python3 email_sender.py --stats
"""

import argparse
import csv
import json
import os
import random
import re
import smtplib
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SECRETS_FILE = PROJECT_ROOT / "SECRETS" / "PAYMENT_INFO.md"
SEND_LOG = PROJECT_ROOT / "AUTOMATIONS" / "logs" / "email_sends.csv"
LEADS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "leads"
OUTREACH_DIR = PROJECT_ROOT / "AUTOMATIONS" / "outreach"

(PROJECT_ROOT / "AUTOMATIONS" / "logs").mkdir(parents=True, exist_ok=True)

# Demo site URLs matched to industry
DEMO_SITES = {
    "dental": {
        "basic": "https://dental-demo.surge.sh",
        "motion": "https://dental-motion.surge.sh",
    },
    "dentist": {
        "basic": "https://dental-demo.surge.sh",
        "motion": "https://dental-motion.surge.sh",
    },
    "restaurant": {
        "basic": "https://restaurant-site-demo.surge.sh",
        "motion": "https://restaurant-motion.surge.sh",
    },
    "plumber": {
        "basic": "https://plumber-demo.surge.sh",
        "motion": None,
    },
    "lawyer": {
        "basic": "https://legal-demo.surge.sh",
        "motion": None,
    },
    "legal": {
        "basic": "https://legal-demo.surge.sh",
        "motion": None,
    },
    "fitness": {
        "basic": "https://fitness-demo.surge.sh",
        "motion": None,
    },
    "realtor": {
        "basic": "https://realtor-demo.surge.sh",
        "motion": "https://realtor-motion.surge.sh",
    },
}

# Email templates per industry (copy-style.md compliant: no em dashes, no AI slop, specific numbers, consequence-first)
TEMPLATES = {
    "dental": {
        "subject": "quick website demo for {business_name} ({city})",
        "body": """Hi {first_name},

I was looking at dental practices in {city} and found {business_name}.

I put together a quick demo site concept for a practice like yours. here it is:

{demo_url}

it's mobile-first with a clear call to action (call / directions / booking link).

if you want something like this for {business_name}, I can have it live in 48 hours. $500 flat, no monthly fees.

if not, no worries. the demo is yours to look at either way.

best,
PM""",
    },
    "restaurant": {
        "subject": "quick restaurant website demo ({city})",
        "body": """Hi {first_name},

found {business_name} while looking at restaurants in {city}.

I put together a sample site for a place like yours:

{demo_url}

mobile-first with your menu and a clear reservation / call button.

if you want one customized for {business_name}, it's $500 flat. live in 48 hours. no monthly fees, you own it.

take a look, let me know what you think.

PM""",
    },
    "plumber": {
        "subject": "quick plumbing website demo ({city})",
        "body": """Hi {first_name},

looked at plumbing companies in {city} and found {business_name}.

I built a demo site that might be useful:

{demo_url}

it's mobile-first with a click-to-call button and clear services section.

$500 flat to customize it for {business_name}. live in 48 hours. no contracts, no monthly fees.

PM""",
    },
    "lawyer": {
        "subject": "quick law firm website demo ({city})",
        "body": """Hi {first_name},

found {business_name} while looking at law firms in {city}.

put together a demo site:

{demo_url}

clean design with a clear consultation call to action.

if you want one for {business_name}, $500 flat. 48 hours to go live. you own it, no monthly fees.

PM""",
    },
    "fitness": {
        "subject": "quick fitness studio website demo ({city})",
        "body": """Hi {first_name},

found {business_name} while looking at fitness studios in {city}.

built a demo site for a studio like yours:

{demo_url}

mobile-first with a clear schedule/booking call to action.

$500 flat to make it yours. 48 hours. no monthly fees.

PM""",
    },
    "realtor": {
        "subject": "quick real estate website demo ({city})",
        "body": """Hi {first_name},

found {business_name} while looking at agents in {city}.

put together a demo:

{demo_url}

mobile-first with a clear contact call to action.

$500 flat to customize for {business_name}. 48 hours. no monthly fees, you own it.

PM""",
    },
}

# Fallback for unknown industries
TEMPLATES["default"] = {
    "subject": "quick website demo for {business_name} ({city})",
    "body": """Hi {first_name},

found {business_name} while looking at businesses in {city}.

I put together a demo site:

{demo_url}

mobile-first with a clear contact call to action.

$500 flat to customize it for {business_name}. live in 48 hours. no monthly fees.

PM""",
}


def load_template_file(filepath):
    """Load email template from .txt file.

    Format:
        Subject: your subject line with {placeholders}
        ---
        Hi {first_name},

        body text with {placeholders}...

    Supported placeholders: {first_name}, {business_name}, {city}, {industry}, {demo_url}
    """
    text = Path(filepath).read_text().strip()
    if "---" not in text:
        raise ValueError(f"Template {filepath} missing --- separator between subject and body")

    subject_part, body = text.split("---", 1)
    subject = subject_part.strip()
    if subject.lower().startswith("subject:"):
        subject = subject[len("subject:"):].strip()

    body = body.strip()
    return {"subject": subject, "body": body}


def log(msg, level="INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [{level}] {msg}")


def load_secrets():
    """Load credentials from SECRETS/PAYMENT_INFO.md."""
    secrets = {}
    if not SECRETS_FILE.exists():
        return secrets
    for line in SECRETS_FILE.read_text().splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            if val:
                secrets[key] = val
    return secrets


def ensure_can_spam_footer(body: str, physical_address: str) -> str:
    """Ensure a minimal CAN-SPAM footer exists on outbound emails."""
    physical_address = (physical_address or "").strip()
    if not physical_address:
        # Caller should validate before sending.
        return body or ""

    body_s = body or ""
    low = body_s.lower()
    has_unsub = "unsubscribe" in low
    has_addr = physical_address in body_s
    if has_unsub and has_addr:
        return body_s

    footer = "\n\n---\nIf you'd prefer I don't email again, reply \"unsubscribe\".\n" + physical_address + "\n"
    return body_s.rstrip() + footer


def log_send(recipient, subject, status, provider, notes=""):
    """Log each send attempt to CSV."""
    is_new = not SEND_LOG.exists()
    with open(SEND_LOG, "a", newline="") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["timestamp", "recipient", "subject", "status", "provider", "notes"])
        w.writerow([
            datetime.now().isoformat(),
            recipient,
            subject,
            status,
            provider,
            notes,
        ])


def get_already_sent():
    """Get set of emails already sent to (avoid duplicates)."""
    sent = set()
    if SEND_LOG.exists():
        with open(SEND_LOG) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("status") == "SENT":
                    sent.add(row.get("recipient", "").lower())
    return sent


def send_gmail(from_email, app_password, to_email, subject, body):
    """Send email via Gmail SMTP."""
    msg = MIMEMultipart("alternative")
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # Plain text version
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_email, app_password)
        server.send_message(msg)

    return True


def send_resend(api_key, from_email, to_email, subject, body):
    """Send email via Resend API."""
    import urllib.request

    data = json.dumps({
        "from": from_email,
        "to": [to_email],
        "subject": subject,
        "text": body,
    }).encode()

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        log(f"Resend API error: {e.code} {error_body}", "ERROR")
        return False


def detect_industry(filename):
    """Detect industry from filename."""
    name = filename.lower()
    for industry in ["dental", "dentist", "restaurant", "plumber", "lawyer", "legal", "fitness", "realtor"]:
        if industry in name:
            return industry
    return "default"


def detect_city(filename):
    """Extract city from filename like dentist_phoenix_leads.csv."""
    name = Path(filename).stem.lower()
    # Remove common prefixes/suffixes
    name = name.replace("_leads", "").replace("_emails", "")
    for prefix in ["dentist_", "dental_", "restaurant_", "plumber_", "lawyer_", "legal_", "fitness_", "realtor_"]:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    # Clean up
    city = name.replace("_", " ").replace("-", " ").title().strip()
    # Remove state abbreviations like "tx" "az" at end
    city = re.sub(r'\s+(Tx|Az|Ca|Ny|Fl|Ga|Il|Co|Wa)\s*$', '', city, flags=re.IGNORECASE)
    return city if city else "your area"


def extract_first_name(business_name):
    """Try to get a usable first name or fallback to 'there'."""
    if not business_name:
        return "there"
    # If it looks like a person's name (2-3 words, no business words)
    biz_words = ["inc", "llc", "corp", "group", "associates", "dental", "law", "plumbing",
                 "restaurant", "fitness", "realty", "clinic", "office", "studio", "center"]
    words = business_name.strip().split()
    if len(words) <= 3 and not any(w.lower().strip(".,") in biz_words for w in words):
        return words[0]
    return "there"


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def extract_recipients(raw_value):
    """Parse one or many recipients from a CSV cell."""
    if not raw_value:
        return []

    recipients = []
    seen = set()
    for token in re.split(r"[;,\s]+", str(raw_value).strip()):
        email = token.strip().strip("<>()[]{}")
        lower = email.lower()
        if not email:
            continue
        if lower in seen:
            continue
        if "@" not in lower:
            continue
        if "your@email.com" in lower or "example.com" in lower:
            continue
        if not EMAIL_RE.match(email):
            continue
        seen.add(lower)
        recipients.append(email)
    return recipients


def load_outreach_csv(filepath):
    """Load pre-drafted outreach CSV.

    Supports both simple format:
      email,subject,body
    and sequence format:
      email,step1_subject,step1_body,...
    """
    emails = []
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipients = extract_recipients(row.get("email", ""))
            if not recipients:
                continue

            subject = (
                (row.get("subject") or "").strip()
                or (row.get("step1_subject") or "").strip()
                or (row.get("step_1_subject") or "").strip()
            )
            body = (
                (row.get("body") or "").strip()
                or (row.get("step1_body") or "").strip()
                or (row.get("step_1_body") or "").strip()
            )

            if not subject or not body:
                continue

            first_name = (row.get("first_name") or "there").strip() or "there"
            company = (
                (row.get("company_name") or "").strip()
                or (row.get("company") or "").strip()
                or (row.get("business_name") or "").strip()
            )

            for email in recipients:
                emails.append({
                    "email": email,
                    "subject": subject,
                    "body": body,
                    "first_name": first_name,
                    "company": company,
                })
    return emails


def load_raw_leads(filepath, industry=None, template_file=None):
    """Load raw leads CSV and generate emails from templates."""
    if not industry:
        industry = detect_industry(str(filepath))
    city = detect_city(str(filepath))

    if template_file:
        template = load_template_file(template_file)
    else:
        template = TEMPLATES.get(industry, TEMPLATES["default"])
    demo_info = DEMO_SITES.get(industry, DEMO_SITES.get("dental"))
    demo_url = demo_info["basic"] if demo_info else "https://dental-demo.surge.sh"

    emails = []
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Try multiple column names for email
            email = (row.get("email_if_found") or row.get("email") or "").strip()
            if not email or "@" not in email:
                continue

            business_name = (row.get("business_name") or row.get("company_name") or row.get("name") or "your business").strip()
            first_name = extract_first_name(business_name)

            fmt = dict(
                city=city,
                business_name=business_name,
                first_name=first_name,
                demo_url=demo_url,
                industry=industry if industry != "default" else "local",
            )
            subject = template["subject"].format(**fmt)
            body = template["body"].format(**fmt)

            emails.append({
                "email": email,
                "subject": subject,
                "body": body,
                "first_name": first_name,
                "company": business_name,
            })
    return emails


def show_stats():
    """Show stats on all lead and outreach files."""
    print("\n=== LEAD FILES ===")
    total_leads = 0
    total_with_email = 0
    if LEADS_DIR.exists():
        for f in sorted(LEADS_DIR.glob("*.csv")):
            leads = 0
            emails_found = 0
            with open(f, newline="", encoding="utf-8-sig") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    leads += 1
                    email = (row.get("email_if_found") or row.get("email") or "").strip()
                    if email and "@" in email:
                        emails_found += 1
            total_leads += leads
            total_with_email += emails_found
            if emails_found > 0:
                print(f"  {f.name:45s}  {leads:4d} leads  {emails_found:4d} with email")
        print(f"\n  TOTAL: {total_leads} leads, {total_with_email} with email")

    print("\n=== OUTREACH FILES (pre-drafted emails) ===")
    total_outreach = 0
    if OUTREACH_DIR.exists():
        for f in sorted(OUTREACH_DIR.glob("*.csv")):
            count = 0
            with open(f, newline="", encoding="utf-8-sig") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    email = (row.get("email") or "").strip()
                    if email and "@" in email:
                        count += 1
            total_outreach += count
            if count > 0:
                print(f"  {f.name:55s}  {count:4d} emails")
        print(f"\n  TOTAL: {total_outreach} pre-drafted emails ready to send")

    print("\n=== SEND LOG ===")
    sent = get_already_sent()
    print(f"  Already sent: {len(sent)} unique recipients")

    print(f"\n=== DEMO SITES (live, attach to emails) ===")
    for industry, urls in DEMO_SITES.items():
        if urls.get("basic"):
            print(f"  {industry:12s}  basic: {urls['basic']}")
        if urls.get("motion"):
            print(f"  {industry:12s}  motion: {urls['motion']}")


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Cold Email Sender")
    parser.add_argument("--outreach", help="Path to pre-drafted outreach CSV (has email, subject, body columns)")
    parser.add_argument("--leads", help="Path to raw leads CSV (auto-generates email from template)")
    parser.add_argument("--industry", help="Industry for template selection (dental, restaurant, plumber, lawyer, fitness, realtor)")
    parser.add_argument("--template", help="Path to custom email template .txt file")
    parser.add_argument("--max-sends", type=int, default=50, help="Max emails per run (default: 50)")
    parser.add_argument("--delay-min", type=int, default=30, help="Min seconds between sends (default: 30)")
    parser.add_argument("--delay-max", type=int, default=90, help="Max seconds between sends (default: 90)")
    parser.add_argument("--preview", "--dry-run", action="store_true", help="Preview emails without sending (dry run)")
    parser.add_argument("--provider", choices=["gmail", "resend"], default="gmail", help="Email provider (default: gmail)")
    parser.add_argument("--stats", action="store_true", help="Show stats on all lead files")
    parser.add_argument("--from-email", help="Override sender email")
    args = parser.parse_args()

    if args.stats:
        show_stats()
        return

    if not args.outreach and not args.leads:
        parser.print_help()
        print("\nQuick start:")
        print("  python3 email_sender.py --stats")
        print("  python3 email_sender.py --preview --outreach AUTOMATIONS/outreach/dental_austin_tx_leads_emails_step1.csv")
        print("  python3 email_sender.py --preview --leads AUTOMATIONS/leads/dentist_phoenix_leads.csv --industry dental")
        return

    # Load emails
    if args.outreach:
        emails = load_outreach_csv(args.outreach)
        log(f"Loaded {len(emails)} pre-drafted emails from {args.outreach}")
    else:
        emails = load_raw_leads(args.leads, args.industry, template_file=args.template)
        if args.template:
            log(f"Generated {len(emails)} emails from {args.leads} using template {args.template}")
        else:
            log(f"Generated {len(emails)} emails from {args.leads}")

    if not emails:
        log("No valid emails found. check that the CSV has email addresses.", "ERROR")
        return

    # Filter already-sent
    already_sent = get_already_sent()
    emails = [e for e in emails if e["email"].lower() not in already_sent]
    log(f"After dedup: {len(emails)} new recipients ({len(already_sent)} already sent)")

    if not emails:
        log("All recipients already contacted. nothing to send.")
        return

    # Cap at max sends
    if len(emails) > args.max_sends:
        emails = emails[:args.max_sends]
        log(f"Capped at {args.max_sends} emails for this run")

    # Preview mode
    if args.preview:
        print(f"\n{'='*60}")
        print(f"PREVIEW MODE - {len(emails)} emails would be sent")
        print(f"{'='*60}")
        for i, e in enumerate(emails[:5]):
            print(f"\n--- Email {i+1}/{len(emails)} ---")
            print(f"To:      {e['email']}")
            print(f"Subject: {e['subject']}")
            print(f"Body:\n{e['body'][:300]}...")
            print()
        if len(emails) > 5:
            print(f"... and {len(emails) - 5} more")
        print(f"\nTo send for real: remove --preview flag")
        return

    # Load credentials
    secrets = load_secrets()
    physical_address = secrets.get("PHYSICAL_ADDRESS", "").strip()
    if not physical_address:
        log("PHYSICAL_ADDRESS missing. add PHYSICAL_ADDRESS to SECRETS/PAYMENT_INFO.md before live sends.", "ERROR")
        return

    if args.provider == "gmail":
        gmail_addr = args.from_email or secrets.get("GMAIL_ADDRESS")
        gmail_pw = secrets.get("GMAIL_APP_PASSWORD")
        if not gmail_addr or not gmail_pw:
            log("Gmail credentials missing. add GMAIL_ADDRESS and GMAIL_APP_PASSWORD to SECRETS/PAYMENT_INFO.md", "ERROR")
            log("Get app password: myaccount.google.com/apppasswords", "ERROR")
            return
        from_email = gmail_addr
        log(f"Using Gmail SMTP: {from_email}")
    elif args.provider == "resend":
        resend_key = secrets.get("RESEND_API_KEY")
        if not resend_key:
            log("Resend API key missing. add RESEND_API_KEY to SECRETS/PAYMENT_INFO.md", "ERROR")
            return
        from_email = args.from_email or secrets.get("RESEND_FROM_EMAIL", "onboarding@resend.dev")
        log(f"Using Resend API: {from_email}")

    # Send loop
    sent_count = 0
    fail_count = 0

    for i, e in enumerate(emails):
        log(f"[{i+1}/{len(emails)}] Sending to {e['email']}...")

        try:
            e_body = ensure_can_spam_footer(e["body"], physical_address)
            if args.provider == "gmail":
                send_gmail(from_email, gmail_pw, e["email"], e["subject"], e_body)
            elif args.provider == "resend":
                success = send_resend(resend_key, from_email, e["email"], e["subject"], e_body)
                if not success:
                    raise Exception("Resend API failed")

            sent_count += 1
            log_send(e["email"], e["subject"], "SENT", args.provider, e.get("company", ""))
            log(f"  sent to {e['email']}")

        except Exception as ex:
            fail_count += 1
            log_send(e["email"], e["subject"], "FAILED", args.provider, str(ex))
            log(f"  FAILED: {ex}", "ERROR")

            # If 3 consecutive failures, stop (likely auth issue)
            if fail_count >= 3 and sent_count == 0:
                log("3 consecutive failures with 0 successes. check credentials.", "ERROR")
                break

        # Delay between sends (human-like)
        if i < len(emails) - 1:
            delay = random.randint(args.delay_min, args.delay_max)
            log(f"  waiting {delay}s before next send...")
            time.sleep(delay)

    # Summary
    print(f"\n{'='*60}")
    print(f"SEND COMPLETE")
    print(f"{'='*60}")
    print(f"  Sent:   {sent_count}")
    print(f"  Failed: {fail_count}")
    print(f"  Log:    {SEND_LOG}")
    print(f"  Total sent all-time: {len(get_already_sent())}")


if __name__ == "__main__":
    main()
