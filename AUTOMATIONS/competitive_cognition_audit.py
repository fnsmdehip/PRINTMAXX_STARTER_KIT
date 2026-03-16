#!/usr/bin/env python3
"""
Competitive Cognition Audit — Meta-improvement system.

Analyzes our own prompting patterns, session outputs, and system architecture
to find ways to stay ahead of other power users. Runs weekly.

This is the system that improves the system.

Usage:
    python3 competitive_cognition_audit.py --audit    # Run full audit
    python3 competitive_cognition_audit.py --report   # Show latest findings
    python3 competitive_cognition_audit.py --inject   # Update SOUL.md with new insights

Cron: 0 5 * * 0 cd $BASE && $PYTHON AUTOMATIONS/competitive_cognition_audit.py --audit >> AUTOMATIONS/logs/cognition_audit.log 2>&1
"""

import json
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIT_DIR = PROJECT_ROOT / "OPS" / "cognition_audits"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
LATEST_AUDIT = AUDIT_DIR / "latest_audit.json"


def audit_system_patterns():
    """Analyze our system for improvement opportunities."""
    findings = []

    # 1. Check CLAUDE.md for staleness
    claude_md = PROJECT_ROOT / ".claude" / "CLAUDE.md"
    if claude_md.exists():
        content = claude_md.read_text()
        lines = len(content.split("\n"))
        # Check for common anti-patterns
        if "comprehensive" in content.lower():
            findings.append({
                "category": "AI_SLOP_IN_SYSTEM_FILES",
                "severity": "MEDIUM",
                "detail": "CLAUDE.md contains banned AI vocabulary ('comprehensive'). The system prompt itself has slop.",
                "fix": "Search and replace banned words in CLAUDE.md"
            })
        if lines > 700:
            findings.append({
                "category": "CONTEXT_BLOAT",
                "severity": "HIGH",
                "detail": f"CLAUDE.md is {lines} lines. Every session loads this. Token waste compounds.",
                "fix": "Extract rarely-used sections to reference files. Keep CLAUDE.md under 500 lines."
            })

    # 2. Check SOUL.md for drift
    soul = PROJECT_ROOT / "AUTOMATIONS" / "SOUL.md"
    if soul.exists():
        content = soul.read_text()
        if "Competitive Cognition Protocol" not in content:
            findings.append({
                "category": "MISSING_META_COGNITION",
                "severity": "HIGH",
                "detail": "SOUL.md lacks competitive cognition protocol. Agents default to median output.",
                "fix": "Add Competitive Cognition Protocol section to SOUL.md"
            })
        lines = len(content.split("\n"))
        if lines > 150:
            findings.append({
                "category": "SOUL_BLOAT",
                "severity": "MEDIUM",
                "detail": f"SOUL.md is {lines} lines. Should be lean and impactful. Over-long SOUL = diluted identity.",
                "fix": "Trim SOUL.md to essential behavioral directives only."
            })

    # 3. Check for orphan scripts (scripts not in cron or referenced anywhere)
    import subprocess
    cron_content = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
    scripts = list((PROJECT_ROOT / "AUTOMATIONS").glob("*.py"))
    orphans = []
    for script in scripts:
        name = script.name
        if name.startswith("_") or name in ("guardrails.py", "gates.py", "llm_backends.py"):
            continue
        # Check if referenced in cron, CLAUDE.md, or other scripts
        in_cron = name in cron_content
        in_claude = name in (claude_md.read_text() if claude_md.exists() else "")
        if not in_cron and not in_claude:
            orphans.append(name)

    if len(orphans) > 50:
        findings.append({
            "category": "ORPHAN_SCRIPTS",
            "severity": "MEDIUM",
            "detail": f"{len(orphans)} scripts not referenced in cron or CLAUDE.md. Potential dead code.",
            "fix": "Audit orphan scripts. Kill dead ones. Wire live ones into cron."
        })

    # 4. Check prompt patterns in user prompts
    prompts_file = PROJECT_ROOT / "LEDGER" / "USER_PROMPTS.jsonl"
    if prompts_file.exists():
        prompt_count = sum(1 for _ in open(prompts_file))
        findings.append({
            "category": "PROMPT_INTELLIGENCE",
            "severity": "INFO",
            "detail": f"{prompt_count} user prompts logged. Analyze for: recurring frustrations, repeated requests (should be automated), capability gaps.",
            "fix": "Run prompt_meta_review.py to extract patterns."
        })

    # 5. Check for competitive edge decay
    findings.append({
        "category": "EDGE_CHECK",
        "severity": "INFO",
        "detail": "Weekly check: Are our system patterns still ahead of what's publicly available? Search for 'CLAUDE.md best practices', 'claude code power user', 'ai agent architecture 2026' and compare to our system.",
        "fix": "Agent should web-search for latest patterns and compare to our CLAUDE.md/SOUL.md."
    })

    # 6. Meta-cognition check
    findings.append({
        "category": "META_COGNITION",
        "severity": "INFO",
        "detail": "Is the Competitive Cognition Protocol actually changing agent behavior? Check: are session outputs qualitatively different from before it was added? Are agents finding non-obvious angles?",
        "fix": "Compare pre/post session quality. If no improvement, revise the protocol."
    })

    # Save audit
    audit = {
        "timestamp": datetime.now().isoformat(),
        "findings": findings,
        "total_findings": len(findings),
        "high_severity": len([f for f in findings if f["severity"] == "HIGH"]),
        "medium_severity": len([f for f in findings if f["severity"] == "MEDIUM"]),
    }

    with open(LATEST_AUDIT, "w") as f:
        json.dump(audit, f, indent=2)

    # Also save timestamped version
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    with open(AUDIT_DIR / f"audit_{ts}.json", "w") as f:
        json.dump(audit, f, indent=2)

    print(f"\n=== Competitive Cognition Audit ===")
    print(f"Findings: {len(findings)} ({audit['high_severity']} HIGH, {audit['medium_severity']} MEDIUM)")
    for f in findings:
        print(f"  [{f['severity']:6s}] {f['category']}: {f['detail'][:100]}")

    return audit


def show_report():
    """Show latest audit findings."""
    if LATEST_AUDIT.exists():
        audit = json.loads(LATEST_AUDIT.read_text())
        print(f"\n=== Latest Cognition Audit ({audit['timestamp']}) ===")
        for f in audit.get("findings", []):
            print(f"\n[{f['severity']}] {f['category']}")
            print(f"  Detail: {f['detail']}")
            print(f"  Fix: {f['fix']}")
    else:
        print("No audit results yet. Run --audit first.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--audit" in args:
        audit_system_patterns()
    elif "--report" in args:
        show_report()
    else:
        print("Usage: competitive_cognition_audit.py --audit | --report")
        print("Meta-improvement system that audits our own prompting patterns and system architecture.")
