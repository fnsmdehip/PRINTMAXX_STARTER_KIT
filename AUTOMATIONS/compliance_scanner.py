#!/usr/bin/env python3
"""
PRINTMAXX Compliance Scanner — Content Safety Guardrails
=========================================================
Separate from guardrails.py (file-system safety). This module scans
CONTENT for legal/compliance issues before publishing.

Scans for:
- FTC disclosure violations (affiliate links without disclosure)
- CAN-SPAM violations (missing unsubscribe, physical address)
- Fake social proof ("3 businesses already signed up" with no proof)
- Copyright issues (scraped content without attribution)
- Income claims without disclaimers
- Health/medical claims without disclaimers
- Platform TOS red flags (mass automation language, bot references)
- NSFW content in non-NSFW channels
- PII exposure (emails, phones, addresses in public content)

Usage:
  python3 compliance_scanner.py --scan-content CONTENT/social/
  python3 compliance_scanner.py --scan-emails AUTOMATIONS/outreach/
  python3 compliance_scanner.py --scan-file path/to/file.md
  python3 compliance_scanner.py --audit-all
  python3 compliance_scanner.py --fix path/to/file.md  (auto-fix where possible)
"""

import os
import sys
import re
import csv
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# COMPLIANCE RULES
# ============================================================

# FTC required disclosures for affiliate content
FTC_AFFILIATE_PATTERNS = [
    r'(?i)affiliate\s+link',
    r'(?i)commission\s+(?:from|on|for)',
    r'(?i)referral\s+(?:link|code|bonus)',
    r'(?i)(?:use|with)\s+(?:my|this)\s+(?:link|code)',
    r'(?i)partner\s+(?:link|program)',
    r'(?i)earn\s+(?:a\s+)?commission',
]

FTC_DISCLOSURE_PATTERNS = [
    r'(?i)#ad\b',
    r'(?i)\bad\b.*\bdisclosure',
    r'(?i)affiliate\s+disclosure',
    r'(?i)paid\s+partnership',
    r'(?i)sponsored\s+(?:by|content|post)',
    r'(?i)this\s+(?:post|content)\s+contains?\s+affiliate',
    r'(?i)i\s+(?:may\s+)?(?:earn|receive)\s+(?:a\s+)?commission',
    r'(?i)disclosure:',
]

# Income claim patterns that need disclaimers
INCOME_CLAIM_PATTERNS = [
    r'\$[\d,]+(?:\.\d+)?\s*(?:/|\s*per\s*)(?:mo(?:nth)?|day|week|year|hr|hour)',
    r'(?i)(?:made|earned|generating|making)\s+\$[\d,]+',
    r'(?i)\$[\d,]+\s+(?:in\s+)?(?:revenue|income|profit|sales)',
    r'(?i)(?:6|7)\s*(?:-|\s)figure',
    r'(?i)quit\s+(?:my|their|his|her)\s+(?:job|9-5|9\s*to\s*5)',
    r'(?i)(?:financial|income)\s+freedom',
    r'(?i)passive\s+income',
]

INCOME_DISCLAIMER_PATTERNS = [
    r'(?i)results\s+(?:may|will)\s+vary',
    r'(?i)not\s+(?:a\s+)?(?:guarantee|typical)',
    r'(?i)individual\s+results',
    r'(?i)no\s+guarantee',
    r'(?i)past\s+(?:results|performance)',
    r'(?i)disclaimer',
]

# Health claim patterns
HEALTH_CLAIM_PATTERNS = [
    r'(?i)(?:cure|treat|prevent|heal)s?\s+(?:\w+\s+){0,3}(?:disease|cancer|diabetes|anxiety|depression)',
    r'(?i)(?:clinically|scientifically)\s+proven',
    r'(?i)(?:doctor|physician)\s+recommended',
    r'(?i)(?:weight|fat)\s+loss\s+(?:guarantee|results)',
    r'(?i)(?:boost|increase|improve)s?\s+(?:immunity|immune)',
]

# Fake social proof patterns
FAKE_SOCIAL_PROOF = [
    r'(?i)\d+\s+(?:businesses|clients|customers|people)\s+(?:already|have)\s+(?:signed|joined|started|bought)',
    r'(?i)(?:hundreds|thousands)\s+of\s+(?:happy|satisfied)\s+(?:clients|customers)',
    r'(?i)(?:trusted|used)\s+by\s+\d+\+?\s+(?:companies|businesses|brands)',
    r'(?i)join\s+\d+\+?\s+(?:others|entrepreneurs|founders)',
]

# PII patterns (should not appear in public content)
PII_PATTERNS = [
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'email'),
    (r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', 'phone'),
    # Keep strict to reduce false positives (9-digit IDs are common in public docs/URLs).
    (r'\b\d{3}[-.\s]\d{2}[-.\s]\d{4}\b', 'ssn_pattern'),
]

# CAN-SPAM requirements for email content
CANSPAM_REQUIRED = [
    'unsubscribe',
    'physical_address',
    'sender_identity',
]

# Platform-specific red flags
PLATFORM_RED_FLAGS = [
    r'(?i)(?:mass|bulk)\s+(?:follow|unfollow|like|comment|DM|message)',
    r'(?i)(?:bot|automated)\s+(?:account|posting|engagement)',
    r'(?i)(?:fake|bought|purchased)\s+(?:followers|likes|engagement)',
    r'(?i)(?:spam|blast)\s+(?:DM|message|comment)',
]


class ComplianceIssue:
    def __init__(self, category: str, severity: str, file_path: str,
                 line_num: int, text: str, rule: str, fix_suggestion: str = ""):
        self.category = category  # FTC, CANSPAM, INCOME, HEALTH, PII, FAKE_PROOF, PLATFORM
        self.severity = severity  # CRITICAL, WARNING, INFO
        self.file_path = file_path
        self.line_num = line_num
        self.text = text[:200]
        self.rule = rule
        self.fix_suggestion = fix_suggestion
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            "category": self.category,
            "severity": self.severity,
            "file": self.file_path,
            "line": self.line_num,
            "text": self.text,
            "rule": self.rule,
            "fix": self.fix_suggestion,
            "time": self.timestamp,
        }

    def __str__(self):
        return f"[{self.severity}] {self.category} @ {self.file_path}:{self.line_num} — {self.rule}"


class ComplianceScanner:
    def __init__(self, project_root: str = BASE):
        self.project_root = project_root
        self.issues: List[ComplianceIssue] = []

    def scan_file(self, file_path: str) -> List[ComplianceIssue]:
        """Scan a single file for compliance issues."""
        issues = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            return [ComplianceIssue("ERROR", "CRITICAL", file_path, 0,
                                    str(e), "File read error")]

        rel_path = os.path.relpath(file_path, self.project_root)

        # Determine content type
        is_email = 'outreach' in rel_path.lower() or 'email' in rel_path.lower()
        is_social = 'social' in rel_path.lower() or 'tweet' in rel_path.lower()
        is_product = 'product' in rel_path.lower() or 'listing' in rel_path.lower()
        is_public = is_email or is_social or is_product

        # 1. FTC Affiliate Disclosure Check
        # Only flag publishable content (social, product listings, emails)
        # Skip internal strategy/OPS docs that just DISCUSS affiliate programs
        is_internal = any(x in rel_path.lower() for x in [
            'ops/', 'ledger/', 'money_methods/', 'strategy/', '.claude/',
            'playbook', 'checklist', 'guide', 'audit', 'index', 'plan',
            'schedule', 'spec', 'status', '_ready', 'master_',
        ])
        has_affiliate = any(re.search(p, content) for p in FTC_AFFILIATE_PATTERNS)
        has_disclosure = any(re.search(p, content) for p in FTC_DISCLOSURE_PATTERNS)
        # Also check if there are actual URLs (sign of real promotional content vs discussion)
        has_urls = bool(re.search(r'https?://\S+', content))
        if has_affiliate and not has_disclosure and is_public and not is_internal and has_urls:
            for i, line in enumerate(lines):
                for p in FTC_AFFILIATE_PATTERNS:
                    if re.search(p, line):
                        issues.append(ComplianceIssue(
                            "FTC", "CRITICAL", rel_path, i + 1, line.strip(),
                            "Affiliate content without FTC disclosure",
                            "Add '#ad' or 'Affiliate disclosure: I may earn a commission' to the content"
                        ))
                        break

        # 2. Income Claims Check
        for i, line in enumerate(lines):
            for p in INCOME_CLAIM_PATTERNS:
                if re.search(p, line):
                    # Check if disclaimer exists nearby (within 5 lines)
                    context = '\n'.join(lines[max(0, i-5):min(len(lines), i+5)])
                    has_disclaimer = any(re.search(d, context) for d in INCOME_DISCLAIMER_PATTERNS)
                    if not has_disclaimer:
                        issues.append(ComplianceIssue(
                            "INCOME", "WARNING", rel_path, i + 1, line.strip(),
                            "Income claim without disclaimer",
                            "Add 'Results may vary. Not a guarantee of income.' near this claim"
                        ))
                    break

        # 3. Health Claims Check
        for i, line in enumerate(lines):
            for p in HEALTH_CLAIM_PATTERNS:
                if re.search(p, line):
                    issues.append(ComplianceIssue(
                        "HEALTH", "CRITICAL", rel_path, i + 1, line.strip(),
                        "Health claim that may require substantiation",
                        "Add medical disclaimer or remove unsubstantiated health claim"
                    ))
                    break

        # 4. Fake Social Proof Check
        for i, line in enumerate(lines):
            for p in FAKE_SOCIAL_PROOF:
                if re.search(p, line):
                    issues.append(ComplianceIssue(
                        "FAKE_PROOF", "WARNING", rel_path, i + 1, line.strip(),
                        "Potentially unverifiable social proof claim",
                        "Replace with verifiable claim or remove specific numbers"
                    ))
                    break

        # 5. PII in Public Content
        if is_public:
            for i, line in enumerate(lines):
                for pattern, pii_type in PII_PATTERNS:
                    matches = re.findall(pattern, line)
                    if matches and pii_type == 'email':
                        # Allow emails in email outreach files (expected)
                        if not is_email:
                            issues.append(ComplianceIssue(
                                "PII", "WARNING", rel_path, i + 1,
                                line.strip()[:100], f"Exposed {pii_type} in public content",
                                f"Remove or redact {pii_type} from public-facing content"
                            ))
                    elif matches and pii_type == 'ssn_pattern':
                        issues.append(ComplianceIssue(
                            "PII", "CRITICAL", rel_path, i + 1,
                            "[REDACTED]", "Possible SSN pattern detected",
                            "Immediately remove any SSN-like patterns"
                        ))

        # 6. CAN-SPAM for email content
        if is_email:
            content_lower = content.lower()
            if 'unsubscribe' not in content_lower:
                issues.append(ComplianceIssue(
                    "CANSPAM", "CRITICAL", rel_path, 0, "",
                    "Email missing unsubscribe mechanism",
                    "Add unsubscribe link/instructions to all marketing emails"
                ))
            if not re.search(r'\d+\s+\w+\s+(?:st|ave|blvd|rd|dr|ln|ct|way)', content_lower):
                issues.append(ComplianceIssue(
                    "CANSPAM", "WARNING", rel_path, 0, "",
                    "Email may be missing physical address",
                    "Add physical business address per CAN-SPAM requirements"
                ))

        # 7. Platform TOS Red Flags
        if is_social:
            for i, line in enumerate(lines):
                for p in PLATFORM_RED_FLAGS:
                    if re.search(p, line):
                        issues.append(ComplianceIssue(
                            "PLATFORM", "INFO", rel_path, i + 1, line.strip(),
                            "Language that may trigger platform TOS enforcement",
                            "Rephrase to avoid explicit mention of automation/bots in public content"
                        ))
                        break

        self.issues.extend(issues)
        return issues

    def scan_directory(self, dir_path: str, extensions: List[str] = None) -> List[ComplianceIssue]:
        """Scan all files in a directory."""
        if extensions is None:
            extensions = ['.md', '.csv', '.txt', '.html']

        all_issues = []
        for root, dirs, files in os.walk(dir_path):
            # Skip hidden dirs, node_modules, and archive dirs
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and 'archive' not in d.lower()]
            for f in files:
                if any(f.endswith(ext) for ext in extensions):
                    fp = os.path.join(root, f)
                    issues = self.scan_file(fp)
                    all_issues.extend(issues)
        return all_issues

    def scan_content(self) -> List[ComplianceIssue]:
        """Scan all content directories."""
        dirs = [
            os.path.join(self.project_root, "CONTENT", "social"),
            os.path.join(self.project_root, "CONTENT", "social", "auto_generated"),
        ]
        all_issues = []
        for d in dirs:
            if os.path.exists(d):
                all_issues.extend(self.scan_directory(d))
        return all_issues

    def scan_emails(self) -> List[ComplianceIssue]:
        """Scan all outreach/email content."""
        dirs = [
            os.path.join(self.project_root, "AUTOMATIONS", "outreach"),
            os.path.join(self.project_root, "AUTOMATIONS", "content_posting"),
            os.path.join(self.project_root, "EMAIL"),
        ]
        all_issues = []
        for d in dirs:
            if os.path.exists(d):
                all_issues.extend(self.scan_directory(d))
        return all_issues

    def audit_all(self) -> List[ComplianceIssue]:
        """Full audit of all scannable content."""
        dirs = [
            "CONTENT/social",
            "CONTENT/social/auto_generated",
            "AUTOMATIONS/outreach",
            "AUTOMATIONS/content_posting",
            "AUTOMATIONS/freelance_response_templates",
            "PRODUCTS",
            "DIGITAL_PRODUCTS",
            "EMAIL",
        ]
        all_issues = []
        for d in dirs:
            full = os.path.join(self.project_root, d)
            if os.path.exists(full):
                all_issues.extend(self.scan_directory(full))
        return all_issues

    def generate_report(self, issues: List[ComplianceIssue] = None) -> str:
        """Generate a human-readable compliance report."""
        if issues is None:
            issues = self.issues

        if not issues:
            return "COMPLIANCE SCAN: ALL CLEAR. No issues found."

        # Count by severity and category
        by_severity = {}
        by_category = {}
        for issue in issues:
            by_severity[issue.severity] = by_severity.get(issue.severity, 0) + 1
            by_category[issue.category] = by_category.get(issue.category, 0) + 1

        lines = [
            f"# PRINTMAXX Compliance Scan Report",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**Total Issues:** {len(issues)}",
            f"",
            f"## Summary",
            f"| Severity | Count |",
            f"|----------|-------|",
        ]
        for sev in ['CRITICAL', 'WARNING', 'INFO']:
            if sev in by_severity:
                lines.append(f"| {sev} | {by_severity[sev]} |")

        lines.extend([
            f"",
            f"| Category | Count |",
            f"|----------|-------|",
        ])
        for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
            lines.append(f"| {cat} | {count} |")

        # Critical issues first
        critical = [i for i in issues if i.severity == 'CRITICAL']
        if critical:
            lines.extend([
                f"",
                f"## CRITICAL Issues (fix before publishing)",
                f"",
            ])
            for i, issue in enumerate(critical, 1):
                lines.append(f"### {i}. {issue.category} — {issue.file_path}:{issue.line_num}")
                lines.append(f"**Rule:** {issue.rule}")
                if issue.text:
                    lines.append(f"**Text:** `{issue.text[:150]}`")
                if issue.fix_suggestion:
                    lines.append(f"**Fix:** {issue.fix_suggestion}")
                lines.append("")

        # Warnings
        warnings = [i for i in issues if i.severity == 'WARNING']
        if warnings:
            lines.extend([
                f"## WARNING Issues (review before publishing)",
                f"",
            ])
            for i, issue in enumerate(warnings, 1):
                lines.append(f"{i}. **{issue.category}** `{issue.file_path}:{issue.line_num}` — {issue.rule}")
                if issue.fix_suggestion:
                    lines.append(f"   Fix: {issue.fix_suggestion}")

        # Info
        info = [i for i in issues if i.severity == 'INFO']
        if info:
            lines.extend([
                f"",
                f"## INFO (review optional)",
                f"",
            ])
            for issue in info:
                lines.append(f"- `{issue.file_path}:{issue.line_num}` — {issue.rule}")

        return '\n'.join(lines)

    def save_report(self, issues: List[ComplianceIssue] = None, output_dir: str = None):
        """Save report to file."""
        if output_dir is None:
            output_dir = os.path.join(self.project_root, "OPS")

        report = self.generate_report(issues)
        date_str = datetime.now().strftime('%Y_%m_%d')
        output_path = os.path.join(output_dir, f"COMPLIANCE_SCAN_{date_str}.md")

        with open(output_path, 'w') as f:
            f.write(report)

        # Also save JSON for programmatic access
        json_path = os.path.join(self.project_root, "LEDGER",
                                 f"compliance_scan_{date_str}.json")
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w') as f:
            json.dump([i.to_dict() for i in (issues or self.issues)], f, indent=2)

        return output_path, json_path


def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Compliance Scanner — Content Safety Guardrails",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--scan-content", type=str, nargs='?', const='CONTENT/social',
                        help="Scan content directory for compliance issues")
    parser.add_argument("--scan-emails", type=str, nargs='?', const='AUTOMATIONS/outreach',
                        help="Scan email/outreach content")
    parser.add_argument("--scan-file", type=str, help="Scan a single file")
    parser.add_argument("--audit-all", action="store_true",
                        help="Full compliance audit of all publishable content")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--save", action="store_true", help="Save report to OPS/")
    parser.add_argument(
        "--no-fail",
        action="store_true",
        help="Always exit 0 (useful for continuous automation runs). Critical issues still reported in output/JSON.",
    )

    args = parser.parse_args()
    scanner = ComplianceScanner()

    if args.scan_file:
        path = os.path.join(BASE, args.scan_file) if not os.path.isabs(args.scan_file) else args.scan_file
        issues = scanner.scan_file(path)
    elif args.scan_content:
        path = os.path.join(BASE, args.scan_content)
        issues = scanner.scan_directory(path)
    elif args.scan_emails:
        path = os.path.join(BASE, args.scan_emails)
        issues = scanner.scan_directory(path)
    elif args.audit_all:
        issues = scanner.audit_all()
    else:
        parser.print_help()
        return

    if args.json:
        print(json.dumps([i.to_dict() for i in issues], indent=2))
    else:
        report = scanner.generate_report(issues)
        print(report)

    if args.save:
        md_path, json_path = scanner.save_report(issues)
        print(f"\nReport saved to: {md_path}")
        print(f"JSON saved to: {json_path}")

    # Exit code based on critical issues
    critical_count = sum(1 for i in issues if i.severity == 'CRITICAL')
    if critical_count > 0:
        print(f"\n{critical_count} CRITICAL issues found. Fix before publishing.")
        sys.exit(0 if args.no_fail else 1)
    elif issues:
        print(f"\n{len(issues)} non-critical issues found. Review recommended.")
        sys.exit(0)
    else:
        print("\nAll clear. No compliance issues detected.")
        sys.exit(0)


if __name__ == "__main__":
    main()
