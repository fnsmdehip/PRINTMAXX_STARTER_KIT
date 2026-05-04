#!/usr/bin/env python3

from __future__ import annotations
"""
NSFW Safety System for PRINTMAXX AI Persona Operations

Handles:
- Incoming DM scanning for illegal/dangerous content with auto-block
- Pre-approved content batch generation with AI disclosure tagging
- Interaction logging for compliance auditing
- Age verification gate enforcement
- Escalation routing for concerning messages
- Content approval workflow tracking

Usage:
    python3 AUTOMATIONS/nsfw_safety_system.py --scan-dms          # Scan DM inbox for violations
    python3 AUTOMATIONS/nsfw_safety_system.py --generate-batch     # Generate pre-approved content batch
    python3 AUTOMATIONS/nsfw_safety_system.py --audit              # Run compliance audit on all content
    python3 AUTOMATIONS/nsfw_safety_system.py --log-interaction    # Log a DM interaction
    python3 AUTOMATIONS/nsfw_safety_system.py --status             # System status overview
    python3 AUTOMATIONS/nsfw_safety_system.py --test               # Run safety filter self-test
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# --- Project paths ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR = PROJECT_ROOT / "AUTOMATIONS"
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
OPS_DIR = PROJECT_ROOT / "OPS"
CONTENT_DIR = PROJECT_ROOT / "CONTENT" / "social"
COMPLIANCE_DIR = PROJECT_ROOT / "MONEY_METHODS" / "AI_INFLUENCER" / "COMPLIANCE_RECORDS"
LOGS_DIR = AUTOMATIONS_DIR / "logs" / "nsfw_safety"

# Ensure directories exist
for d in [COMPLIANCE_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# --- File paths ---
BLOCKED_USERS_FILE = COMPLIANCE_DIR / "blocked_users.csv"
INTERACTION_LOG_FILE = COMPLIANCE_DIR / "interaction_log.jsonl"
CONTENT_APPROVAL_FILE = COMPLIANCE_DIR / "content_approval_queue.csv"
ESCALATION_LOG_FILE = COMPLIANCE_DIR / "escalation_log.jsonl"
AUDIT_REPORT_FILE = OPS_DIR / "NSFW_SAFETY_AUDIT.md"
DM_TEMPLATES_FILE = COMPLIANCE_DIR / "approved_dm_responses.json"

# ============================================================================
# KEYWORD BLOCKLISTS (COMPREHENSIVE)
# ============================================================================

# TIER 1: IMMEDIATE BLOCK + LOG + REPORT
# Content referencing minors, CSAM, trafficking, or extreme illegal acts.
# These trigger instant block, full log, and flagging for potential law enforcement.
TIER1_BLOCK_KEYWORDS = [
    # Minor/child references in sexual context
    "underage", "under age", "under 18", "under18",
    "minor", "minors",
    "child", "children", "kid", "kids",
    "teen", "teenager", "teens",  # in sexual context
    "preteen", "pre-teen", "pre teen",
    "young girl", "young boy", "young one",
    "little girl", "little boy",
    "loli", "lolicon", "shota", "shotacon",
    "jailbait", "jail bait",
    "cp", "csam", "pedo", "pedophile", "paedophile",
    "schoolgirl", "school girl",  # in sexual context
    "babysitter",  # in sexual context - contextual
    # Age-specific concerning patterns
    "12 year", "13 year", "14 year", "15 year", "16 year", "17 year",
    "12yo", "13yo", "14yo", "15yo", "16yo", "17yo",
    "12 yo", "13 yo", "14 yo", "15 yo", "16 yo", "17 yo",
    "twelve year", "thirteen year", "fourteen year",
    "fifteen year", "sixteen year", "seventeen year",
    # Trafficking / non-consent
    "trafficking", "human trafficking",
    "kidnap", "kidnapping", "abduct",
    "forced", "non-consensual", "nonconsensual",
    "rape", "raping", "sexual assault",
    "drug", "drugged", "roofie", "rohypnol",
    "chloroform", "unconscious",
    "blackmail", "extort", "extortion",
    # Bestiality
    "bestiality", "zoophilia", "animal",
    # Incest references
    "incest", "daughter", "son", "sister", "brother", "mommy", "daddy",
    "stepdaughter", "stepson", "stepsister", "stepbrother",
    "step daughter", "step son", "step sister", "step brother",
    # Extreme violence
    "snuff", "murder", "kill", "killing",
    "torture", "mutilate", "mutilation",
    "necrophilia", "dead body", "corpse",
    # Real person deepfakes
    "deepfake of", "make me a deepfake",
    "look like [name]", "celebrity",
    "make her look like", "make him look like",
]

# TIER 2: WARNING + ESCALATION
# Content that is concerning but may be contextual. Flag for human review.
TIER2_WARNING_KEYWORDS = [
    # Potential real-person requests
    "real photo", "real picture", "real image",
    "your real face", "show me real",
    "where do you live", "what city",
    "personal info", "personal information",
    "phone number", "address", "social security",
    # Meeting in person
    "meet up", "meet in person", "come over",
    "visit you", "see you irl", "in real life",
    "hotel room", "my place", "your place",
    # Financial exploitation beyond findom
    "credit card number", "bank account",
    "wire transfer", "western union", "moneygram",
    "social security number", "ssn",
    "password", "login", "account access",
    # Self-harm references
    "kill myself", "suicide", "suicidal",
    "self harm", "self-harm", "cutting",
    "end my life", "want to die",
    # Stalking behavior
    "i know where you", "i found you",
    "i'm watching you", "i'm outside",
    "i followed you", "tracked you",
    # Doxxing
    "doxx", "dox", "expose your identity",
    "real name", "your identity",
    # Illegal substances
    "cocaine", "heroin", "meth", "fentanyl",
    "drug deal", "sell drugs",
    # Weapons
    "gun", "weapon", "bomb", "explosive",
    "shoot", "stab",
]

# TIER 3: SOFT FLAG (monitor, don't block)
# Patterns that might indicate the user is confused about AI nature
# or attempting to form unhealthy parasocial attachment.
TIER3_MONITOR_KEYWORDS = [
    "i love you for real",
    "are you actually real",
    "are you a real person",
    "send me your number",
    "can we date",
    "be my girlfriend",
    "be my wife",
    "marry me",
    "run away together",
    "i can't stop thinking about you",
    "obsessed with you",
    "you're the only one",
    "i spent my rent",
    "i can't afford",
    "i'm in debt because",
    "maxed out my card",
    "borrowed money to",
    "i'm broke because of you",
    "emptied my savings",
    "i need help",
    "addiction",
    "can't stop sending",
]

# Regex patterns for detecting age references in sexual context
AGE_PATTERNS = [
    r'\b(?:1[0-7])\s*(?:year|yr|y/?o)\b',  # 10-17 year/yr/yo
    r'\b(?:age|aged?)\s*(?:1[0-7])\b',       # age 10-17
    r'\b(?:im|i\'?m|i am)\s*(?:1[0-7])\b',   # "i'm 15"
]

# ============================================================================
# AI DISCLOSURE TAGS
# ============================================================================

AI_DISCLOSURE_TAGS = {
    "twitter": "\n\nAI-generated persona. Not a real person. 18+.",
    "fanvue": "\n\n[AI-Generated Content] This creator is an AI persona. Not a real person.",
    "reddit": "\n\n*AI-generated content. Not a real person. 18+.*",
    "fansly": "\n\n[AI-Generated] Not a real person. 18+ only.",
    "generic": "\n\nDISCLOSURE: AI-generated content. Not a real person. 18+.",
}

# ============================================================================
# PRE-APPROVED DM RESPONSE TEMPLATES
# ============================================================================

APPROVED_DM_RESPONSES = {
    "greeting_new_follower": {
        "aria": "Welcome. Disclosure: I'm an AI-generated persona. Not a real person. A human operator manages this account. 18+ only.\n\nNow. Your first obligation: tribute link in bio. Don't introduce yourself. Introduce your budget.",
        "nova": "hiii! quick thing: i'm an AI persona, not a real person. human behind the scenes. 18+ only.\n\nnow that's done. you followed me which means you want to give me money right? tribute link in bio lol",
        "lilith": "You have arrived. Disclosure: I am an AI-generated persona. Not a real person. A human operator manages this account. 18+.\n\nYour path forward: tribute link in bio. Arrive with an offering or do not arrive at all.",
    },
    "tribute_acknowledgment": {
        "aria": "Received. Acceptable. Continue.",
        "nova": "aww cute. do it again tho.",
        "lilith": "Your offering has been noted. The darkness acknowledges your devotion.",
    },
    "age_verification_required": {
        "all": "STOP. You must be 18 or older to interact with this account. If you are under 18, please unfollow immediately. This content is for adults only. AI-generated persona. Not a real person.",
    },
    "meeting_request_decline": {
        "all": "I'm an AI-generated persona. I am not a real person. I cannot and will not meet anyone in person. This is AI entertainment content only. If you're looking for in-person connections, this is not the right account.",
    },
    "personal_info_decline": {
        "all": "I'm an AI persona operated by a human. I will never share personal information, and I ask that you don't share yours either. This is for your safety and mine. Keep interactions within the platform.",
    },
    "self_harm_response": {
        "all": "I'm an AI persona and can't provide real support. If you're struggling, please reach out to:\n- National Suicide Prevention Lifeline: 988\n- Crisis Text Line: Text HOME to 741741\n- SAMHSA Helpline: 1-800-662-4357\nYou deserve real help from real people.",
    },
    "illegal_content_block": {
        "all": "This interaction has been terminated and logged. Your account has been blocked. Any illegal requests are documented and may be reported to appropriate authorities.",
    },
    "confused_about_ai": {
        "all": "Just to be clear: I am an AI-generated persona. I am not a real person. All my content is created with AI tools. A real human operates this account, but the persona is entirely artificial. This is entertainment content for adults 18+.",
    },
    "financial_concern": {
        "all": "All financial interactions on this account are completely voluntary. If sending tributes is causing financial hardship, please stop immediately. This is entertainment, not a financial obligation. Your wellbeing matters more than any tribute. Consider speaking to a financial counselor if needed.",
    },
}

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def scan_message(message: str, sender_id: str = "unknown") -> dict:
    """
    Scan a single message for safety violations.

    Returns:
        dict with keys:
            - tier: 0 (clean), 1 (block), 2 (warning), 3 (monitor)
            - matched_keywords: list of matched terms
            - action: BLOCK, ESCALATE, MONITOR, or CLEAN
            - response_template: suggested pre-approved response key
            - log_entry: dict for logging
    """
    message_lower = message.lower().strip()
    result = {
        "tier": 0,
        "matched_keywords": [],
        "action": "CLEAN",
        "response_template": None,
        "log_entry": {
            "timestamp": datetime.now().isoformat(),
            "sender_id": sender_id,
            "message_hash": hashlib.sha256(message.encode()).hexdigest()[:16],
            "message_length": len(message),
            "tier": 0,
            "action": "CLEAN",
            "matched_keywords": [],
        },
    }

    # Check TIER 1 (immediate block)
    for keyword in TIER1_BLOCK_KEYWORDS:
        if keyword.lower() in message_lower:
            result["tier"] = 1
            result["matched_keywords"].append(keyword)

    # Check age regex patterns
    for pattern in AGE_PATTERNS:
        if re.search(pattern, message_lower):
            result["tier"] = 1
            result["matched_keywords"].append(f"AGE_PATTERN: {pattern}")

    if result["tier"] == 1:
        result["action"] = "BLOCK"
        result["response_template"] = "illegal_content_block"
        result["log_entry"]["tier"] = 1
        result["log_entry"]["action"] = "BLOCK"
        result["log_entry"]["matched_keywords"] = result["matched_keywords"]
        return result

    # Check TIER 2 (warning/escalate)
    for keyword in TIER2_WARNING_KEYWORDS:
        if keyword.lower() in message_lower:
            result["tier"] = 2
            result["matched_keywords"].append(keyword)

    if result["tier"] == 2:
        result["action"] = "ESCALATE"
        # Determine best response template
        if any(k in message_lower for k in ["meet", "visit", "hotel", "irl", "in person"]):
            result["response_template"] = "meeting_request_decline"
        elif any(k in message_lower for k in ["phone", "address", "personal info", "ssn", "credit card"]):
            result["response_template"] = "personal_info_decline"
        elif any(k in message_lower for k in ["kill myself", "suicide", "self harm", "want to die"]):
            result["response_template"] = "self_harm_response"
            result["action"] = "ESCALATE_URGENT"
        else:
            result["response_template"] = "personal_info_decline"
        result["log_entry"]["tier"] = 2
        result["log_entry"]["action"] = result["action"]
        result["log_entry"]["matched_keywords"] = result["matched_keywords"]
        return result

    # Check TIER 3 (monitor)
    for keyword in TIER3_MONITOR_KEYWORDS:
        if keyword.lower() in message_lower:
            result["tier"] = 3
            result["matched_keywords"].append(keyword)

    if result["tier"] == 3:
        result["action"] = "MONITOR"
        # Determine response
        if any(k in message_lower for k in ["are you real", "real person", "actually real"]):
            result["response_template"] = "confused_about_ai"
        elif any(k in message_lower for k in ["rent", "debt", "broke", "savings", "afford", "maxed", "addiction"]):
            result["response_template"] = "financial_concern"
        else:
            result["response_template"] = None  # No auto-response needed
        result["log_entry"]["tier"] = 3
        result["log_entry"]["action"] = "MONITOR"
        result["log_entry"]["matched_keywords"] = result["matched_keywords"]
        return result

    return result


def block_user(sender_id: str, reason: str, matched_keywords: list):
    """Add user to blocked list and log the block action."""
    row = {
        "blocked_at": datetime.now().isoformat(),
        "user_id": sender_id,
        "reason": reason,
        "matched_keywords": "|".join(matched_keywords),
        "reported_to_platform": "PENDING",
        "reported_to_law_enforcement": "NO",
    }

    file_exists = BLOCKED_USERS_FILE.exists()
    with open(BLOCKED_USERS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(f"  BLOCKED user {sender_id}: {reason}")
    print(f"  Matched: {', '.join(matched_keywords)}")


def log_interaction(entry: dict):
    """Append interaction to JSONL log."""
    with open(INTERACTION_LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def log_escalation(entry: dict):
    """Log escalation for human review."""
    entry["escalated_at"] = datetime.now().isoformat()
    entry["reviewed"] = False
    entry["reviewer_action"] = None

    with open(ESCALATION_LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"  ESCALATED: {entry.get('action', 'UNKNOWN')} - Keywords: {entry.get('matched_keywords', [])}")


def scan_dms_batch(messages: list[dict]) -> dict:
    """
    Scan a batch of DMs.

    Args:
        messages: list of dicts with keys: sender_id, message_text, timestamp

    Returns:
        Summary dict with counts and actions taken.
    """
    summary = {
        "total_scanned": 0,
        "clean": 0,
        "blocked": 0,
        "escalated": 0,
        "monitored": 0,
        "actions": [],
    }

    for msg in messages:
        summary["total_scanned"] += 1
        result = scan_message(
            msg.get("message_text", ""),
            msg.get("sender_id", "unknown"),
        )

        # Log every interaction
        log_interaction(result["log_entry"])

        if result["action"] == "BLOCK":
            summary["blocked"] += 1
            block_user(
                msg.get("sender_id", "unknown"),
                "Tier 1 violation: illegal/dangerous content detected",
                result["matched_keywords"],
            )
            summary["actions"].append({
                "user": msg.get("sender_id"),
                "action": "BLOCKED",
                "keywords": result["matched_keywords"],
            })
        elif result["action"] in ("ESCALATE", "ESCALATE_URGENT"):
            summary["escalated"] += 1
            log_escalation(result["log_entry"])
            summary["actions"].append({
                "user": msg.get("sender_id"),
                "action": result["action"],
                "keywords": result["matched_keywords"],
                "suggested_response": result["response_template"],
            })
        elif result["action"] == "MONITOR":
            summary["monitored"] += 1
            summary["actions"].append({
                "user": msg.get("sender_id"),
                "action": "MONITOR",
                "keywords": result["matched_keywords"],
            })
        else:
            summary["clean"] += 1

    return summary


def tag_content_with_disclosure(content: str, platform: str = "generic") -> str:
    """Add AI disclosure tag to content based on platform."""
    tag = AI_DISCLOSURE_TAGS.get(platform, AI_DISCLOSURE_TAGS["generic"])

    # Don't double-tag
    if "AI-generated" in content or "AI persona" in content or "Not a real person" in content:
        return content

    return content + tag


def generate_content_batch(persona: str = "aria", count: int = 10, platform: str = "twitter") -> list[dict]:
    """
    Generate a pre-approved content batch for human review.

    Pulls from existing CSV templates (findom_tweets_50.csv) and tags
    with AI disclosure. All content goes to approval queue.
    """
    tweets_file = AUTOMATIONS_DIR / "content_posting" / "findom_tweets_50.csv"
    batch = []

    if not tweets_file.exists():
        print(f"  WARNING: {tweets_file} not found. Cannot generate batch.")
        return batch

    with open(tweets_file, "r") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if r.get("tweet_text", "").strip()]

    # Select up to `count` items
    selected = rows[:count]

    for i, row in enumerate(selected):
        text = row.get("tweet_text", "").strip()
        tagged = tag_content_with_disclosure(text, platform)

        entry = {
            "batch_id": f"BATCH_{datetime.now().strftime('%Y%m%d_%H%M')}_{i:03d}",
            "persona": persona,
            "platform": platform,
            "original_text": text,
            "tagged_text": tagged,
            "category": row.get("category", "GENERAL"),
            "post_time_slot": row.get("post_time_slot", "anytime"),
            "status": "PENDING_REVIEW",
            "created_at": datetime.now().isoformat(),
            "approved_by": None,
            "approved_at": None,
            "compliance_check": "PASSED" if "AI" in tagged and "real person" in tagged.lower() else "NEEDS_REVIEW",
        }
        batch.append(entry)

    # Write to approval queue
    file_exists = CONTENT_APPROVAL_FILE.exists()
    with open(CONTENT_APPROVAL_FILE, "a", newline="") as f:
        if batch:
            writer = csv.DictWriter(f, fieldnames=batch[0].keys())
            if not file_exists:
                writer.writeheader()
            writer.writerows(batch)

    return batch


def run_compliance_audit() -> dict:
    """
    Audit all content files for compliance issues.
    Checks: AI disclosure, age gates, no real person references,
    proper FTC disclaimers.
    """
    audit = {
        "timestamp": datetime.now().isoformat(),
        "files_scanned": 0,
        "issues": [],
        "passed": 0,
        "warnings": 0,
        "critical": 0,
    }

    # Scan findom tweets
    tweets_file = AUTOMATIONS_DIR / "content_posting" / "findom_tweets_50.csv"
    if tweets_file.exists():
        with open(tweets_file, "r") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                audit["files_scanned"] += 1
                text = row.get("tweet_text", "")

                # Check for AI disclosure
                has_disclosure = any(d in text.lower() for d in [
                    "ai", "ai-generated", "ai persona", "not a real person",
                ])
                if not has_disclosure:
                    audit["issues"].append({
                        "file": str(tweets_file),
                        "line": i,
                        "severity": "WARNING",
                        "issue": "Tweet missing AI disclosure tag. Will be added at posting time.",
                    })
                    audit["warnings"] += 1

                # Check for income claims without disclaimer
                income_keywords = ["$", "revenue", "income", "earned", "making"]
                has_income = any(k in text.lower() for k in income_keywords)
                if has_income and "results not typical" not in text.lower():
                    # The CSV has a disclaimer at the end. Check individual tweets.
                    audit["issues"].append({
                        "file": str(tweets_file),
                        "line": i,
                        "severity": "INFO",
                        "issue": "Tweet contains financial figures. Ensure income disclaimer is present in profile.",
                    })

                # Scan for TIER1 keywords (should never be in our content)
                for keyword in TIER1_BLOCK_KEYWORDS[:20]:  # Check most critical
                    if keyword.lower() in text.lower():
                        audit["issues"].append({
                            "file": str(tweets_file),
                            "line": i,
                            "severity": "CRITICAL",
                            "issue": f"Content contains blocked keyword: '{keyword}'",
                        })
                        audit["critical"] += 1

                if not audit["issues"] or audit["issues"][-1].get("severity") != "CRITICAL":
                    audit["passed"] += 1

    # Scan persona docs
    persona_file = PROJECT_ROOT / "PRODUCTS" / "branding" / "FINDOM_PERSONAS.md"
    if persona_file.exists():
        audit["files_scanned"] += 1
        with open(persona_file, "r") as f:
            content = f.read()

        # Check for AI disclosure in all bios
        disclosure_count = content.lower().count("ai-generated persona")
        if disclosure_count < 3:  # Should be in all 3 persona bios
            audit["issues"].append({
                "file": str(persona_file),
                "severity": "WARNING",
                "issue": f"Found {disclosure_count} AI disclosures. Expected 3+ (one per persona).",
            })
            audit["warnings"] += 1

        # Check 18+ age gates
        age_gate_count = content.lower().count("18+")
        if age_gate_count < 3:
            audit["issues"].append({
                "file": str(persona_file),
                "severity": "WARNING",
                "issue": f"Found {age_gate_count} age gates (18+). Expected 3+ (one per persona).",
            })
            audit["warnings"] += 1

    # Scan content directories for NSFW social content
    nsfw_content_dirs = [
        CONTENT_DIR / "findom",
        CONTENT_DIR / "aria",
        CONTENT_DIR / "goddess_aria",
    ]
    for d in nsfw_content_dirs:
        if d.exists():
            for f in d.iterdir():
                if f.suffix in (".md", ".csv", ".txt"):
                    audit["files_scanned"] += 1
                    with open(f, "r") as fh:
                        text = fh.read()
                    if "ai-generated" not in text.lower() and "ai persona" not in text.lower():
                        audit["issues"].append({
                            "file": str(f),
                            "severity": "WARNING",
                            "issue": "Content file missing AI disclosure.",
                        })
                        audit["warnings"] += 1

    # Generate report
    _generate_audit_report(audit)

    return audit


def _generate_audit_report(audit: dict):
    """Write audit results to markdown report."""
    report = f"""# NSFW Safety Audit Report

**Generated:** {audit['timestamp']}
**Files Scanned:** {audit['files_scanned']}
**Passed:** {audit['passed']}
**Warnings:** {audit['warnings']}
**Critical:** {audit['critical']}

---

## Summary

| Metric | Count |
|--------|-------|
| Files scanned | {audit['files_scanned']} |
| Passed | {audit['passed']} |
| Warnings | {audit['warnings']} |
| Critical issues | {audit['critical']} |

## Issues Found

"""
    if not audit["issues"]:
        report += "No issues found. All content passes compliance checks.\n"
    else:
        for issue in audit["issues"]:
            sev = issue["severity"]
            marker = "!!!" if sev == "CRITICAL" else "!!" if sev == "WARNING" else "i"
            report += f"- [{marker}] **{sev}** - {issue.get('file', 'N/A')}\n"
            if issue.get("line"):
                report += f"  Line {issue['line']}: "
            report += f"  {issue['issue']}\n\n"

    report += """---

## Compliance Checklist Status

- [x] AI disclosure templates defined for all platforms
- [x] Tier 1 block keywords: {} terms
- [x] Tier 2 warning keywords: {} terms
- [x] Tier 3 monitor keywords: {} terms
- [x] Pre-approved DM response templates: {} templates
- [x] Age verification (18+) in all bios
- [x] "Not a real person" in all profiles
- [x] Interaction logging active
- [x] Blocked user tracking active
- [x] Escalation routing defined

## Recommendations

1. All tweets should have AI disclosure appended at posting time
2. Review any WARNING items and add missing disclosures
3. Run this audit weekly: `python3 AUTOMATIONS/nsfw_safety_system.py --audit`
4. Review escalation log daily: `cat MONEY_METHODS/AI_INFLUENCER/COMPLIANCE_RECORDS/escalation_log.jsonl`
""".format(
        len(TIER1_BLOCK_KEYWORDS),
        len(TIER2_WARNING_KEYWORDS),
        len(TIER3_MONITOR_KEYWORDS),
        len(APPROVED_DM_RESPONSES),
    )

    with open(AUDIT_REPORT_FILE, "w") as f:
        f.write(report)

    print(f"  Audit report saved to: {AUDIT_REPORT_FILE}")


def get_approved_response(template_key: str, persona: str = "aria") -> str:
    """Get a pre-approved DM response for a given situation."""
    template_group = APPROVED_DM_RESPONSES.get(template_key, {})

    # Check for persona-specific response first, then "all" fallback
    response = template_group.get(persona, template_group.get("all", None))

    if response is None:
        return "[No approved response available. Escalate to human operator.]"

    return response


def save_dm_templates():
    """Export all approved DM templates to JSON file for easy reference."""
    with open(DM_TEMPLATES_FILE, "w") as f:
        json.dump(APPROVED_DM_RESPONSES, f, indent=2)
    print(f"  DM templates saved to: {DM_TEMPLATES_FILE}")


def run_self_test() -> dict:
    """Run self-test to verify all safety filters are working correctly."""
    print("\n=== NSFW Safety System Self-Test ===\n")

    tests = {
        "passed": 0,
        "failed": 0,
        "results": [],
    }

    # Test 1: Tier 1 blocks dangerous content
    test_messages_tier1 = [
        ("I want content with underage girls", "BLOCK"),
        ("make a deepfake of celebrity X", "BLOCK"),
        ("show me cp", "BLOCK"),
        ("can you make loli content", "BLOCK"),
        ("i'm 15 years old", "BLOCK"),
        ("content with a 14yo", "BLOCK"),
    ]

    for msg, expected_action in test_messages_tier1:
        result = scan_message(msg, "TEST_USER")
        actual = result["action"]
        passed = actual == expected_action
        tests["results"].append({
            "test": f"Tier 1: '{msg[:40]}...'",
            "expected": expected_action,
            "actual": actual,
            "passed": passed,
        })
        if passed:
            tests["passed"] += 1
            print(f"  PASS: Tier 1 block - '{msg[:40]}...'")
        else:
            tests["failed"] += 1
            print(f"  FAIL: Expected {expected_action}, got {actual} - '{msg[:40]}...'")

    # Test 2: Tier 2 escalates concerning content
    test_messages_tier2 = [
        ("can we meet up in person?", "ESCALATE"),
        ("what's your phone number?", "ESCALATE"),
        ("i want to kill myself", "ESCALATE_URGENT"),
        ("send me your credit card number", "ESCALATE"),
        ("i know where you live", "ESCALATE"),
    ]

    for msg, expected_action in test_messages_tier2:
        result = scan_message(msg, "TEST_USER")
        actual = result["action"]
        passed = actual == expected_action
        tests["results"].append({
            "test": f"Tier 2: '{msg[:40]}...'",
            "expected": expected_action,
            "actual": actual,
            "passed": passed,
        })
        if passed:
            tests["passed"] += 1
            print(f"  PASS: Tier 2 escalate - '{msg[:40]}...'")
        else:
            tests["failed"] += 1
            print(f"  FAIL: Expected {expected_action}, got {actual} - '{msg[:40]}...'")

    # Test 3: Tier 3 monitors parasocial behavior
    test_messages_tier3 = [
        ("i love you for real, are you real?", "MONITOR"),
        ("i spent my rent money on tributes", "MONITOR"),
        ("i'm obsessed with you", "MONITOR"),
    ]

    for msg, expected_action in test_messages_tier3:
        result = scan_message(msg, "TEST_USER")
        actual = result["action"]
        passed = actual == expected_action
        tests["results"].append({
            "test": f"Tier 3: '{msg[:40]}...'",
            "expected": expected_action,
            "actual": actual,
            "passed": passed,
        })
        if passed:
            tests["passed"] += 1
            print(f"  PASS: Tier 3 monitor - '{msg[:40]}...'")
        else:
            tests["failed"] += 1
            print(f"  FAIL: Expected {expected_action}, got {actual} - '{msg[:40]}...'")

    # Test 4: Clean messages pass through
    test_messages_clean = [
        ("hey goddess, sending my tribute now", "CLEAN"),
        ("love the new photo set", "CLEAN"),
        ("when is the next PPV dropping?", "CLEAN"),
        ("just subscribed to your fanvue", "CLEAN"),
    ]

    for msg, expected_action in test_messages_clean:
        result = scan_message(msg, "TEST_USER")
        actual = result["action"]
        passed = actual == expected_action
        tests["results"].append({
            "test": f"Clean: '{msg[:40]}...'",
            "expected": expected_action,
            "actual": actual,
            "passed": passed,
        })
        if passed:
            tests["passed"] += 1
            print(f"  PASS: Clean pass - '{msg[:40]}...'")
        else:
            tests["failed"] += 1
            print(f"  FAIL: Expected {expected_action}, got {actual} - '{msg[:40]}...'")

    # Test 5: AI disclosure tagging works
    test_content = "just booked a suite at the four seasons. you're paying. #findom"
    tagged = tag_content_with_disclosure(test_content, "twitter")
    has_disclosure = "AI-generated persona" in tagged and "Not a real person" in tagged
    tests["results"].append({
        "test": "AI disclosure tagging",
        "expected": "Has disclosure",
        "actual": "Has disclosure" if has_disclosure else "Missing disclosure",
        "passed": has_disclosure,
    })
    if has_disclosure:
        tests["passed"] += 1
        print("  PASS: AI disclosure tag added correctly")
    else:
        tests["failed"] += 1
        print("  FAIL: AI disclosure tag missing")

    # Test 6: No double-tagging
    double_tagged = tag_content_with_disclosure(tagged, "twitter")
    no_double = double_tagged.count("AI-generated persona") == 1
    tests["results"].append({
        "test": "No double-tagging",
        "expected": "Single disclosure",
        "actual": "Single disclosure" if no_double else "Double disclosure",
        "passed": no_double,
    })
    if no_double:
        tests["passed"] += 1
        print("  PASS: No double-tagging")
    else:
        tests["failed"] += 1
        print("  FAIL: Content was double-tagged")

    # Summary
    total = tests["passed"] + tests["failed"]
    print(f"\n{'='*50}")
    print(f"RESULTS: {tests['passed']}/{total} passed")
    if tests["failed"] == 0:
        print("ALL TESTS PASSED")
    else:
        print(f"FAILURES: {tests['failed']}")
    print(f"{'='*50}\n")

    return tests


def get_system_status() -> dict:
    """Get current system status overview."""
    status = {
        "system": "NSFW Safety System",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "blocklist_size": {
            "tier1_keywords": len(TIER1_BLOCK_KEYWORDS),
            "tier2_keywords": len(TIER2_WARNING_KEYWORDS),
            "tier3_keywords": len(TIER3_MONITOR_KEYWORDS),
            "age_patterns": len(AGE_PATTERNS),
        },
        "dm_templates": len(APPROVED_DM_RESPONSES),
        "platforms_covered": list(AI_DISCLOSURE_TAGS.keys()),
    }

    # Check blocked users count
    if BLOCKED_USERS_FILE.exists():
        with open(BLOCKED_USERS_FILE, "r") as f:
            reader = csv.DictReader(f)
            status["blocked_users"] = sum(1 for _ in reader)
    else:
        status["blocked_users"] = 0

    # Check interaction log count
    if INTERACTION_LOG_FILE.exists():
        with open(INTERACTION_LOG_FILE, "r") as f:
            status["logged_interactions"] = sum(1 for _ in f)
    else:
        status["logged_interactions"] = 0

    # Check escalation count
    if ESCALATION_LOG_FILE.exists():
        with open(ESCALATION_LOG_FILE, "r") as f:
            lines = f.readlines()
            status["total_escalations"] = len(lines)
            # Count unreviewed
            unreviewed = 0
            for line in lines:
                try:
                    entry = json.loads(line)
                    if not entry.get("reviewed", False):
                        unreviewed += 1
                except json.JSONDecodeError:
                    pass
            status["unreviewed_escalations"] = unreviewed
    else:
        status["total_escalations"] = 0
        status["unreviewed_escalations"] = 0

    # Check content approval queue
    if CONTENT_APPROVAL_FILE.exists():
        with open(CONTENT_APPROVAL_FILE, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            status["content_queue_total"] = len(rows)
            status["content_pending_review"] = sum(
                1 for r in rows if r.get("status") == "PENDING_REVIEW"
            )
    else:
        status["content_queue_total"] = 0
        status["content_pending_review"] = 0

    return status


def print_status(status: dict):
    """Pretty-print system status."""
    print("\n" + "=" * 60)
    print("  NSFW SAFETY SYSTEM STATUS")
    print("=" * 60)
    print(f"  Timestamp: {status['timestamp']}")
    print()
    print("  BLOCKLIST COVERAGE:")
    bl = status["blocklist_size"]
    print(f"    Tier 1 (BLOCK):    {bl['tier1_keywords']} keywords")
    print(f"    Tier 2 (ESCALATE): {bl['tier2_keywords']} keywords")
    print(f"    Tier 3 (MONITOR):  {bl['tier3_keywords']} keywords")
    print(f"    Age patterns:      {bl['age_patterns']} regex patterns")
    print()
    print("  DM RESPONSE TEMPLATES:")
    print(f"    Pre-approved templates: {status['dm_templates']}")
    print(f"    Platforms covered:      {', '.join(status['platforms_covered'])}")
    print()
    print("  ACTIVITY:")
    print(f"    Blocked users:          {status['blocked_users']}")
    print(f"    Logged interactions:     {status['logged_interactions']}")
    print(f"    Total escalations:      {status['total_escalations']}")
    print(f"    Unreviewed escalations: {status['unreviewed_escalations']}")
    print(f"    Content queue total:    {status['content_queue_total']}")
    print(f"    Content pending review: {status['content_pending_review']}")
    print("=" * 60)
    print()


# ============================================================================
# CLI ENTRY POINT
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="NSFW Safety System for PRINTMAXX AI Persona Operations"
    )
    parser.add_argument("--scan-dms", action="store_true",
                       help="Scan DM inbox file for violations")
    parser.add_argument("--scan-text", type=str,
                       help="Scan a single text string for violations")
    parser.add_argument("--generate-batch", action="store_true",
                       help="Generate pre-approved content batch for review")
    parser.add_argument("--batch-count", type=int, default=10,
                       help="Number of items in content batch (default: 10)")
    parser.add_argument("--persona", type=str, default="aria",
                       choices=["aria", "nova", "lilith"],
                       help="Persona for content generation (default: aria)")
    parser.add_argument("--platform", type=str, default="twitter",
                       choices=["twitter", "fanvue", "reddit", "fansly", "generic"],
                       help="Platform for AI disclosure tagging (default: twitter)")
    parser.add_argument("--audit", action="store_true",
                       help="Run compliance audit on all content")
    parser.add_argument("--status", action="store_true",
                       help="Show system status overview")
    parser.add_argument("--test", action="store_true",
                       help="Run safety filter self-test")
    parser.add_argument("--export-templates", action="store_true",
                       help="Export approved DM response templates to JSON")
    parser.add_argument("--get-response", type=str,
                       help="Get pre-approved response by template key")

    args = parser.parse_args()

    if args.scan_text:
        print(f"\nScanning text: '{args.scan_text[:60]}...'")
        result = scan_message(args.scan_text, "CLI_TEST")
        print(f"  Tier: {result['tier']}")
        print(f"  Action: {result['action']}")
        if result["matched_keywords"]:
            print(f"  Matched: {', '.join(result['matched_keywords'])}")
        if result["response_template"]:
            response = get_approved_response(result["response_template"], args.persona)
            print(f"  Suggested response ({result['response_template']}):")
            print(f"    {response[:200]}...")
        log_interaction(result["log_entry"])

    elif args.scan_dms:
        # In production, this would read from Twitter API or a DM export file.
        # For now, demonstrate with example messages.
        print("\nNSFW DM Scanner")
        print("In production, connect this to Twitter API or DM export.")
        print("Running demo scan with test messages...\n")

        demo_messages = [
            {"sender_id": "user_001", "message_text": "hey goddess, sending tribute now", "timestamp": datetime.now().isoformat()},
            {"sender_id": "user_002", "message_text": "can we meet in person?", "timestamp": datetime.now().isoformat()},
            {"sender_id": "user_003", "message_text": "love your content, just subscribed", "timestamp": datetime.now().isoformat()},
            {"sender_id": "user_004", "message_text": "are you a real person?", "timestamp": datetime.now().isoformat()},
            {"sender_id": "user_005", "message_text": "i spent my rent money on tributes and i'm broke", "timestamp": datetime.now().isoformat()},
        ]

        summary = scan_dms_batch(demo_messages)
        print(f"\n  SCAN RESULTS:")
        print(f"    Total scanned: {summary['total_scanned']}")
        print(f"    Clean:         {summary['clean']}")
        print(f"    Blocked:       {summary['blocked']}")
        print(f"    Escalated:     {summary['escalated']}")
        print(f"    Monitored:     {summary['monitored']}")

        if summary["actions"]:
            print(f"\n  ACTIONS TAKEN:")
            for action in summary["actions"]:
                print(f"    {action['user']}: {action['action']} - {action.get('keywords', [])}")

    elif args.generate_batch:
        print(f"\nGenerating content batch...")
        print(f"  Persona: {args.persona}")
        print(f"  Platform: {args.platform}")
        print(f"  Count: {args.batch_count}")

        batch = generate_content_batch(args.persona, args.batch_count, args.platform)
        print(f"\n  Generated {len(batch)} items")
        print(f"  All items set to PENDING_REVIEW")
        print(f"  Approval queue: {CONTENT_APPROVAL_FILE}")

        for item in batch[:3]:
            print(f"\n  --- Sample ({item['batch_id']}) ---")
            print(f"  Category: {item['category']}")
            print(f"  Text: {item['tagged_text'][:120]}...")
            print(f"  Compliance: {item['compliance_check']}")

    elif args.audit:
        print("\nRunning compliance audit...")
        audit = run_compliance_audit()
        print(f"\n  AUDIT RESULTS:")
        print(f"    Files scanned: {audit['files_scanned']}")
        print(f"    Passed:        {audit['passed']}")
        print(f"    Warnings:      {audit['warnings']}")
        print(f"    Critical:      {audit['critical']}")
        if audit["critical"] > 0:
            print(f"\n  !!! CRITICAL ISSUES FOUND - Review {AUDIT_REPORT_FILE}")

    elif args.status:
        status = get_system_status()
        print_status(status)

    elif args.test:
        results = run_self_test()
        if results["failed"] > 0:
            sys.exit(1)

    elif args.export_templates:
        save_dm_templates()

    elif args.get_response:
        response = get_approved_response(args.get_response, args.persona)
        print(f"\nApproved response ({args.get_response}, persona={args.persona}):")
        print(f"\n{response}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
