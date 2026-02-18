#!/usr/bin/env python3
"""
Email Validator - Validate email lists before sending campaigns
Uses DNS MX lookup, syntax validation, and optional Hunter/NeverBounce API

Usage:
    python email_validator.py emails.csv                  # Validate CSV file
    python email_validator.py emails.csv --column email   # Specify email column
    python email_validator.py emails.csv --api hunter     # Use Hunter.io API
    python email_validator.py emails.csv --api neverbounce  # Use NeverBounce API
    python email_validator.py --email test@example.com    # Validate single email

Environment Variables:
    HUNTER_API_KEY: Hunter.io API key (optional)
    NEVERBOUNCE_API_KEY: NeverBounce API key (optional)

Output:
    Validated CSV with status column: emails_validated.csv
    Summary report printed to console
"""

import argparse
import csv
import dns.resolver
import os
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    exit(1)


# Validation patterns
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

# Known disposable email domains (subset)
DISPOSABLE_DOMAINS = {
    'tempmail.com', 'throwaway.email', 'guerrillamail.com', 'mailinator.com',
    'temp-mail.org', '10minutemail.com', 'fakeinbox.com', 'getnada.com',
    'maildrop.cc', 'yopmail.com', 'trashmail.com', 'sharklasers.com'
}

# Role-based prefixes to flag
ROLE_BASED_PREFIXES = {
    'info', 'admin', 'support', 'sales', 'contact', 'hello', 'help',
    'noreply', 'no-reply', 'postmaster', 'webmaster', 'abuse', 'feedback'
}


def validate_syntax(email: str) -> tuple[bool, str]:
    """Check email syntax"""
    if not email:
        return False, "Empty email"

    email = email.strip().lower()

    if not EMAIL_REGEX.match(email):
        return False, "Invalid syntax"

    if len(email) > 254:
        return False, "Too long"

    local_part = email.split('@')[0]
    if len(local_part) > 64:
        return False, "Local part too long"

    return True, "Valid syntax"


def check_disposable(domain: str) -> bool:
    """Check if domain is a disposable email service"""
    return domain.lower() in DISPOSABLE_DOMAINS


def check_role_based(email: str) -> bool:
    """Check if email is role-based (info@, admin@, etc.)"""
    local_part = email.split('@')[0].lower()
    return local_part in ROLE_BASED_PREFIXES


def check_mx_record(domain: str) -> tuple[bool, str]:
    """Check if domain has MX records"""
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if mx_records:
            return True, f"MX found: {mx_records[0].exchange}"
        return False, "No MX records"
    except dns.resolver.NXDOMAIN:
        return False, "Domain does not exist"
    except dns.resolver.NoAnswer:
        return False, "No MX records"
    except dns.resolver.Timeout:
        return False, "DNS timeout"
    except Exception as e:
        return False, f"DNS error: {str(e)}"


def verify_with_smtp(email: str, domain: str, timeout: int = 10) -> tuple[bool, str]:
    """
    Basic SMTP verification (check if mailbox exists)
    Note: Many servers don't support this or give false positives
    """
    try:
        # Get MX record
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = str(mx_records[0].exchange).rstrip('.')

        # Connect to SMTP server
        with socket.create_connection((mx_host, 25), timeout=timeout) as sock:
            sock.recv(1024)  # Get greeting

            sock.send(b'HELO check.local\r\n')
            sock.recv(1024)

            sock.send(f'MAIL FROM:<check@check.local>\r\n'.encode())
            sock.recv(1024)

            sock.send(f'RCPT TO:<{email}>\r\n'.encode())
            response = sock.recv(1024).decode()

            sock.send(b'QUIT\r\n')

            if response.startswith('250'):
                return True, "SMTP verified"
            elif response.startswith('550'):
                return False, "Mailbox does not exist"
            else:
                return None, f"SMTP response: {response[:50]}"

    except socket.timeout:
        return None, "SMTP timeout"
    except socket.error as e:
        return None, f"SMTP connection error: {str(e)}"
    except Exception as e:
        return None, f"SMTP error: {str(e)}"


def verify_with_hunter(email: str, api_key: str) -> tuple[str, dict]:
    """Verify email using Hunter.io API"""
    try:
        response = requests.get(
            'https://api.hunter.io/v2/email-verifier',
            params={'email': email, 'api_key': api_key},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json().get('data', {})
            status = data.get('status', 'unknown')
            return status, {
                'score': data.get('score'),
                'gibberish': data.get('gibberish'),
                'disposable': data.get('disposable'),
                'webmail': data.get('webmail'),
                'mx_records': data.get('mx_records'),
                'smtp_server': data.get('smtp_server'),
                'smtp_check': data.get('smtp_check'),
                'accept_all': data.get('accept_all')
            }
        elif response.status_code == 429:
            return 'rate_limited', {}
        else:
            return 'api_error', {'error': response.text}

    except requests.Timeout:
        return 'timeout', {}
    except Exception as e:
        return 'error', {'error': str(e)}


def verify_with_neverbounce(email: str, api_key: str) -> tuple[str, dict]:
    """Verify email using NeverBounce API"""
    try:
        response = requests.post(
            'https://api.neverbounce.com/v4/single/check',
            data={
                'key': api_key,
                'email': email
            },
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            result = data.get('result', 'unknown')

            # Map NeverBounce results
            status_map = {
                'valid': 'valid',
                'invalid': 'invalid',
                'disposable': 'disposable',
                'catchall': 'accept_all',
                'unknown': 'unknown'
            }

            return status_map.get(result, result), {
                'flags': data.get('flags', []),
                'suggested_correction': data.get('suggested_correction'),
                'execution_time': data.get('execution_time')
            }
        else:
            return 'api_error', {'error': response.text}

    except requests.Timeout:
        return 'timeout', {}
    except Exception as e:
        return 'error', {'error': str(e)}


def validate_email(
    email: str,
    use_api: Optional[str] = None,
    api_key: Optional[str] = None,
    check_smtp: bool = False
) -> dict:
    """Full email validation"""
    result = {
        'email': email,
        'valid': False,
        'status': 'unknown',
        'reason': '',
        'domain': '',
        'is_disposable': False,
        'is_role_based': False,
        'mx_valid': False,
        'api_score': None
    }

    # Basic syntax check
    is_valid, reason = validate_syntax(email)
    if not is_valid:
        result['status'] = 'invalid'
        result['reason'] = reason
        return result

    email = email.strip().lower()
    domain = email.split('@')[1]
    result['email'] = email
    result['domain'] = domain

    # Check disposable
    result['is_disposable'] = check_disposable(domain)
    if result['is_disposable']:
        result['status'] = 'disposable'
        result['reason'] = 'Disposable email domain'
        return result

    # Check role-based
    result['is_role_based'] = check_role_based(email)

    # Check MX records
    mx_valid, mx_reason = check_mx_record(domain)
    result['mx_valid'] = mx_valid
    if not mx_valid:
        result['status'] = 'invalid'
        result['reason'] = mx_reason
        return result

    # Use API if specified
    if use_api and api_key:
        if use_api == 'hunter':
            api_status, api_data = verify_with_hunter(email, api_key)
        elif use_api == 'neverbounce':
            api_status, api_data = verify_with_neverbounce(email, api_key)
        else:
            api_status, api_data = 'unknown', {}

        result['status'] = api_status
        result['api_score'] = api_data.get('score')
        result['valid'] = api_status == 'valid'
        result['reason'] = f"API: {api_status}"
        return result

    # Optional SMTP check (can be unreliable)
    if check_smtp:
        smtp_valid, smtp_reason = verify_with_smtp(email, domain)
        if smtp_valid is not None:
            result['valid'] = smtp_valid
            result['status'] = 'valid' if smtp_valid else 'invalid'
            result['reason'] = smtp_reason
            return result

    # If we got here, syntax and MX are valid
    result['valid'] = True
    result['status'] = 'valid_syntax'
    result['reason'] = 'Passed syntax and MX checks (API recommended for full verification)'

    return result


def validate_csv(
    input_file: Path,
    output_file: Path,
    email_column: str = 'email',
    use_api: Optional[str] = None,
    api_key: Optional[str] = None,
    check_smtp: bool = False,
    max_workers: int = 5
) -> dict:
    """Validate all emails in a CSV file"""
    results = {
        'total': 0,
        'valid': 0,
        'invalid': 0,
        'disposable': 0,
        'role_based': 0,
        'unknown': 0,
        'errors': []
    }

    # Read input CSV
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if email_column not in fieldnames:
            print(f"ERROR: Column '{email_column}' not found in CSV")
            print(f"Available columns: {', '.join(fieldnames)}")
            return results
        rows = list(reader)

    results['total'] = len(rows)
    print(f"Validating {len(rows)} emails...")

    # Validate emails
    validated_rows = []

    def process_row(row):
        email = row.get(email_column, '').strip()
        validation = validate_email(email, use_api, api_key, check_smtp)
        row['validation_status'] = validation['status']
        row['validation_reason'] = validation['reason']
        row['is_disposable'] = validation['is_disposable']
        row['is_role_based'] = validation['is_role_based']
        row['mx_valid'] = validation['mx_valid']
        if validation.get('api_score'):
            row['api_score'] = validation['api_score']
        return row, validation

    # Process with thread pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_row, row): row for row in rows}

        for i, future in enumerate(as_completed(futures)):
            try:
                row, validation = future.result()
                validated_rows.append(row)

                # Update stats
                status = validation['status']
                if status == 'valid' or status == 'valid_syntax':
                    results['valid'] += 1
                elif status == 'disposable':
                    results['disposable'] += 1
                elif status in ['invalid', 'unknown']:
                    results['invalid'] += 1
                else:
                    results['unknown'] += 1

                if validation['is_role_based']:
                    results['role_based'] += 1

                # Progress
                if (i + 1) % 50 == 0:
                    print(f"  Processed {i + 1}/{len(rows)}...")

            except Exception as e:
                results['errors'].append(str(e))

            # Rate limiting for API calls
            if use_api:
                time.sleep(0.5)

    # Write output CSV
    output_fieldnames = list(fieldnames) + [
        'validation_status', 'validation_reason', 'is_disposable',
        'is_role_based', 'mx_valid'
    ]
    if use_api:
        output_fieldnames.append('api_score')

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=output_fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(validated_rows)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Validate email lists before sending"
    )
    parser.add_argument(
        'input_file',
        type=Path,
        nargs='?',
        help="Input CSV file with emails"
    )
    parser.add_argument(
        '--email',
        type=str,
        help="Validate a single email address"
    )
    parser.add_argument(
        '--column',
        type=str,
        default='email',
        help="Column name containing emails (default: email)"
    )
    parser.add_argument(
        '--output',
        type=Path,
        help="Output CSV file (default: input_validated.csv)"
    )
    parser.add_argument(
        '--api',
        choices=['hunter', 'neverbounce'],
        help="Use API for verification"
    )
    parser.add_argument(
        '--smtp',
        action='store_true',
        help="Perform SMTP verification (can be unreliable)"
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=5,
        help="Number of parallel workers (default: 5)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("EMAIL VALIDATOR")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Get API key if using API
    api_key = None
    if args.api:
        if args.api == 'hunter':
            api_key = os.getenv('HUNTER_API_KEY')
        elif args.api == 'neverbounce':
            api_key = os.getenv('NEVERBOUNCE_API_KEY')

        if not api_key:
            print(f"WARNING: {args.api.upper()}_API_KEY not set, falling back to basic validation")
            args.api = None

    # Single email validation
    if args.email:
        print(f"\nValidating: {args.email}")
        result = validate_email(args.email, args.api, api_key, args.smtp)

        print(f"\n{'=' * 40}")
        print(f"Email: {result['email']}")
        print(f"Status: {result['status']}")
        print(f"Valid: {result['valid']}")
        print(f"Reason: {result['reason']}")
        print(f"Domain: {result['domain']}")
        print(f"MX Valid: {result['mx_valid']}")
        print(f"Disposable: {result['is_disposable']}")
        print(f"Role-based: {result['is_role_based']}")
        if result.get('api_score'):
            print(f"API Score: {result['api_score']}")
        return

    # CSV validation
    if not args.input_file:
        parser.print_help()
        return

    if not args.input_file.exists():
        print(f"ERROR: File not found: {args.input_file}")
        return

    output_file = args.output or args.input_file.with_stem(f"{args.input_file.stem}_validated")

    print(f"\nInput: {args.input_file}")
    print(f"Output: {output_file}")
    print(f"Email column: {args.column}")
    if args.api:
        print(f"API: {args.api}")
    if args.smtp:
        print("SMTP check: enabled")
    print()

    results = validate_csv(
        input_file=args.input_file,
        output_file=output_file,
        email_column=args.column,
        use_api=args.api,
        api_key=api_key,
        check_smtp=args.smtp,
        max_workers=args.workers
    )

    # Print summary
    print(f"\n{'=' * 60}")
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total emails: {results['total']}")
    print(f"Valid: {results['valid']} ({results['valid']/max(results['total'],1)*100:.1f}%)")
    print(f"Invalid: {results['invalid']} ({results['invalid']/max(results['total'],1)*100:.1f}%)")
    print(f"Disposable: {results['disposable']}")
    print(f"Role-based: {results['role_based']}")
    print(f"Unknown: {results['unknown']}")
    if results['errors']:
        print(f"Errors: {len(results['errors'])}")

    print(f"\nOutput saved to: {output_file}")
    print(f"\n{'=' * 60}")
    print("COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
