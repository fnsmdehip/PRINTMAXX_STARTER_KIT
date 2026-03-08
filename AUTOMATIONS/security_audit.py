#!/usr/bin/env python3
"""
PRINTMAXX Security Audit
Scans the entire project for secrets, injection vectors, prompt injection surface,
file permission issues, network exposure, and agent safety problems.

Usage:
    python3 AUTOMATIONS/security_audit.py              # full report
    python3 AUTOMATIONS/security_audit.py --quick      # summary only
    python3 AUTOMATIONS/security_audit.py --json       # JSON for agent consumption
    python3 AUTOMATIONS/security_audit.py --fix        # auto-fix trivial issues

Stdlib only. Report saved to OPS/SECURITY_AUDIT_REPORT.md by default.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import textwrap
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import IntEnum
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR: Path = PROJECT_ROOT / "AUTOMATIONS"
SECRETS_DIR: Path = PROJECT_ROOT / "SECRETS"
OPS_DIR: Path = PROJECT_ROOT / "OPS"
DEFAULT_REPORT: Path = OPS_DIR / "SECURITY_AUDIT_REPORT.md"

# File extensions to scan per category
CODE_EXTS = {".py", ".sh"}
DOC_EXTS = {".md", ".json", ".env", ".txt", ".csv", ".yaml", ".yml", ".toml"}
ALL_EXTS = CODE_EXTS | DOC_EXTS
PYTHON_ONLY = {".py"}

# Directories to skip entirely (performance + irrelevance)
SKIP_DIRS = {
    "__pycache__", ".git", "node_modules", ".next", ".expo",
    "venv", ".venv", "env", ".env.d", "dist", "build",
    ".mypy_cache", ".pytest_cache",
    # Bulk data dirs (too many files, no secrets expected in generated content)
    "twitter_scraper_output", "scraper_output", "generated_images",
    "generated_content", "posting_queue", "remotion", "image_templates",
    "printmaxx-site", "MEGA_SHEET", "backup",
    # Auto-generated bulk ops (tool evals, playbooks, email templates, cold emails)
    "auto_ops", "freelance_responses_auto", "CONTENT_QA_QUEUE",
    "cold_emails_txt_Austin_Miami_Phoenix", "cold_emails",
    ".uv-cache", ".venv-qwen3-tts", "longtail_pages",
    ".enrichment_cache", "outreach",
}

# Max file size to scan (5 MB) -- skip binaries / huge dumps
MAX_FILE_SIZE = 5 * 1024 * 1024


# ---------------------------------------------------------------------------
# Severity
# ---------------------------------------------------------------------------

class Severity(IntEnum):
    INFO = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    def label(self) -> str:
        return self.name


# ---------------------------------------------------------------------------
# Finding dataclass
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    category: str
    severity: Severity
    message: str
    file: str = ""
    line: int = 0
    snippet: str = ""
    fix_applied: bool = False

    def to_dict(self) -> dict:
        d = asdict(self)
        d["severity"] = self.severity.label()
        return d

    def oneliner(self) -> str:
        loc = f"{self.file}:{self.line}" if self.file else ""
        return f"[{self.severity.label()}] {self.category}: {self.message} {loc}".strip()


# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------

def safe_path(target: str | Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


# ---------------------------------------------------------------------------
# File walker
# ---------------------------------------------------------------------------

def walk_project(extensions: set[str] | None = None) -> list[Path]:
    """Yield project files matching *extensions*, skipping SKIP_DIRS and large files."""
    results: list[Path] = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if extensions and not any(fname.endswith(ext) for ext in extensions):
                continue
            fp = Path(root) / fname
            try:
                if fp.stat().st_size > MAX_FILE_SIZE:
                    continue
            except OSError:
                continue
            results.append(fp)
    return results


def read_lines(fp: Path) -> list[str]:
    """Read file lines, returning empty list on decode errors."""
    try:
        return fp.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []


# ---------------------------------------------------------------------------
# 1. SECRETS DETECTION
# ---------------------------------------------------------------------------

# Each tuple: (compiled regex, description, severity)
# The regex captures the key/token portion in group(1) where possible.
_SECRET_PATTERNS: list[tuple[re.Pattern, str, Severity]] = []

def _build_secret_patterns() -> list[tuple[re.Pattern, str, Severity]]:
    """Build and return the secret-detection regexes."""
    return [
        # API keys by prefix
        (re.compile(r'(?:"|\')?(' + r'sk-[a-zA-Z0-9]{20,}' + r')(?:"|\')?'),
         "OpenAI/Stripe secret key (sk-)", Severity.CRITICAL),
        (re.compile(r'(?:"|\')?(' + r'sk_live_[a-zA-Z0-9]{20,}' + r')(?:"|\')?'),
         "Stripe live secret key", Severity.CRITICAL),
        (re.compile(r'(?:"|\')?(' + r'pk_live_[a-zA-Z0-9]{20,}' + r')(?:"|\')?'),
         "Stripe live publishable key", Severity.HIGH),
        (re.compile(r'(?:"|\')?(' + r'pk_test_[a-zA-Z0-9]{20,}' + r')(?:"|\')?'),
         "Stripe test publishable key", Severity.MEDIUM),
        (re.compile(r'(?:"|\')?(' + r'sk_test_[a-zA-Z0-9]{20,}' + r')(?:"|\')?'),
         "Stripe test secret key", Severity.HIGH),
        (re.compile(r'(?:"|\')?(' + r'AKIA[0-9A-Z]{16}' + r')(?:"|\')?'),
         "AWS access key ID (AKIA)", Severity.CRITICAL),
        (re.compile(r'(?:"|\')?(' + r'ghp_[a-zA-Z0-9]{36,}' + r')(?:"|\')?'),
         "GitHub personal access token", Severity.CRITICAL),
        (re.compile(r'(?:"|\')?(' + r'gho_[a-zA-Z0-9]{36,}' + r')(?:"|\')?'),
         "GitHub OAuth token", Severity.CRITICAL),
        (re.compile(r'(?:"|\')?(' + r'glpat-[a-zA-Z0-9\-_]{20,}' + r')(?:"|\')?'),
         "GitLab personal access token", Severity.CRITICAL),
        (re.compile(r'(?:"|\')?(' + r'xoxb-[a-zA-Z0-9\-]+' + r')(?:"|\')?'),
         "Slack bot token", Severity.CRITICAL),
        (re.compile(r'(?:"|\')?(' + r'xoxp-[a-zA-Z0-9\-]+' + r')(?:"|\')?'),
         "Slack user token", Severity.CRITICAL),
        (re.compile(r'(?:"|\')?(' + r'SG\.[a-zA-Z0-9\-_]{22,}\.[a-zA-Z0-9\-_]{43,}' + r')(?:"|\')?'),
         "SendGrid API key", Severity.CRITICAL),
        # Bearer tokens in code
        (re.compile(r'(?:Authorization|Bearer)\s*[:=]\s*' + r"['\"]" + r'(Bearer\s+[a-zA-Z0-9\-_.]{20,})' + r"['\"]", re.IGNORECASE),
         "Hardcoded Bearer token", Severity.CRITICAL),
        # Generic password/token assignments
        (re.compile(r'(?:password|passwd|secret|token|api_key|apikey|auth_token)\s*=\s*["\']([^"\']{8,})["\']', re.IGNORECASE),
         "Hardcoded password/token assignment", Severity.HIGH),
        # Private keys
        (re.compile(r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----'),
         "Private key in source", Severity.CRITICAL),
    ]

# Build at import time
_SECRET_PATTERNS = _build_secret_patterns()

# Lines that are clearly comments, docstrings, examples, or regex patterns -- skip them
_SKIP_LINE_RE = re.compile(
    r'^\s*(?:#|//|/\*|\*|"""|\'\'\'|>>>)'
)

# Short prefix fragments that are just pattern examples, not real keys
_MIN_KEY_LEN = 12  # real keys are long


def _is_false_positive_secret(line: str, match_text: str) -> bool:
    """Return True if the match is almost certainly a false positive."""
    # Skip comment lines and pattern definitions
    if _SKIP_LINE_RE.search(line):
        return True
    # Skip very short matches (just a prefix fragment)
    if len(match_text) < _MIN_KEY_LEN:
        return True
    # Skip if it looks like a regex pattern string or our own scanner code
    if "re.compile" in line or "Pattern" in line:
        return True
    if "Severity." in line:
        return True
    # Skip lines referencing env vars (os.environ, os.getenv) -- those are safe
    if "os.environ" in line or "os.getenv" in line or "getenv" in line:
        return True
    # Skip placeholder/example values
    lower_match = match_text.lower()
    if any(placeholder in lower_match for placeholder in
           ("example", "your_", "placeholder", "xxx", "test_key", "changeme", "fixme")):
        return True
    return False


def scan_secrets(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for fp in files:
        rel = str(fp.relative_to(PROJECT_ROOT))
        lines = read_lines(fp)
        for i, line in enumerate(lines, 1):
            for pat, desc, sev in _SECRET_PATTERNS:
                m = pat.search(line)
                if m:
                    matched_text = m.group(1) if m.lastindex else m.group(0)
                    if _is_false_positive_secret(line, matched_text):
                        continue
                    # Redact the actual secret in output
                    if len(matched_text) > 14:
                        redacted = matched_text[:6] + "..." + matched_text[-4:]
                    else:
                        redacted = matched_text[:4] + "..."
                    findings.append(Finding(
                        category="SECRETS",
                        severity=sev,
                        message=f"{desc}: {redacted}",
                        file=rel,
                        line=i,
                        snippet=line.strip()[:120],
                    ))
    return findings


def scan_env_files() -> list[Finding]:
    """Check for .env files outside SECRETS/ and credential files in wrong places."""
    findings: list[Finding] = []
    for fp in walk_project({".env"}):
        rel = str(fp.relative_to(PROJECT_ROOT))
        in_secrets = str(fp).startswith(str(SECRETS_DIR))
        if not in_secrets:
            findings.append(Finding(
                category="SECRETS",
                severity=Severity.HIGH,
                message=".env file outside SECRETS/ directory",
                file=rel,
            ))
    # Check for credentials files outside SECRETS/
    for fp in walk_project(None):
        name = fp.name.lower()
        if name in ("credentials.json", "credentials.env", "service_account.json", ".netrc"):
            rel = str(fp.relative_to(PROJECT_ROOT))
            if not str(fp).startswith(str(SECRETS_DIR)):
                findings.append(Finding(
                    category="SECRETS",
                    severity=Severity.HIGH,
                    message=f"Credential file outside SECRETS/: {fp.name}",
                    file=rel,
                ))
    return findings


# ---------------------------------------------------------------------------
# 2. INJECTION VECTORS
# ---------------------------------------------------------------------------

# Regex patterns for dangerous function calls
_OS_SYSTEM_STR = r'os\.system\s*\('
_OS_SYSTEM_RE = re.compile(_OS_SYSTEM_STR)

_SUBPROCESS_CMDS = r'subprocess\.(?:run|call|Popen|check_output|check_call)'

_SUBPROCESS_FSTR = re.compile(_SUBPROCESS_CMDS + r"""\s*\(\s*f['"]""")
_SUBPROCESS_FORMAT = re.compile(_SUBPROCESS_CMDS + r"""\s*\(.*\.format\(""")
_SUBPROCESS_PERCENT = re.compile(_SUBPROCESS_CMDS + r"""\s*\(.*%\s*(?:\(|[a-zA-Z])""")
_SUBPROCESS_SHELL = re.compile(_SUBPROCESS_CMDS + r"""\s*\(.*shell\s*=\s*True""")

_EVAL_RE = re.compile(r'\beval\s*\(')
_EXEC_RE = re.compile(r'\bexec\s*\(')
_COMPILE_RE = re.compile(r'\bcompile\s*\(')

_SQL_CONCAT = re.compile(
    r'(?:execute|cursor\.execute|query)\s*\(\s*(?:f["\']|.*\.format\(|.*%\s*\().*(?:SELECT|INSERT|UPDATE|DELETE|DROP)',
    re.IGNORECASE,
)
_SQL_FSTR = re.compile(
    r'(?:execute|cursor\.execute)\s*\(\s*f["\'].*(?:SELECT|INSERT|UPDATE|DELETE)',
    re.IGNORECASE,
)


def scan_injection(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for fp in files:
        if fp.suffix != ".py":
            continue
        rel = str(fp.relative_to(PROJECT_ROOT))
        lines = read_lines(fp)
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Skip comments
            if stripped.startswith("#"):
                continue

            # Detect os.system() usage
            if _OS_SYSTEM_RE.search(line):
                findings.append(Finding(
                    category="INJECTION",
                    severity=Severity.HIGH,
                    message="Detected os.system() call -- use subprocess with list args instead",
                    file=rel, line=i,
                    snippet=stripped[:120],
                ))

            # subprocess with f-string / .format / % interpolation
            checks = [
                (_SUBPROCESS_FSTR, "subprocess with f-string interpolation (injection risk)"),
                (_SUBPROCESS_FORMAT, "subprocess with .format() interpolation (injection risk)"),
                (_SUBPROCESS_PERCENT, "subprocess with % interpolation (injection risk)"),
            ]
            for pat, desc in checks:
                if pat.search(line):
                    findings.append(Finding(
                        category="INJECTION",
                        severity=Severity.HIGH,
                        message=desc,
                        file=rel, line=i,
                        snippet=stripped[:120],
                    ))

            # subprocess shell=True
            if _SUBPROCESS_SHELL.search(line):
                findings.append(Finding(
                    category="INJECTION",
                    severity=Severity.MEDIUM,
                    message="subprocess with shell=True -- prefer list args",
                    file=rel, line=i,
                    snippet=stripped[:120],
                ))

            # eval/exec/compile
            dangerous_calls = [(_EVAL_RE, "eval"), (_EXEC_RE, "exec"), (_COMPILE_RE, "compile")]
            for pat, name in dangerous_calls:
                if pat.search(line):
                    # Skip safe usages
                    if "literal_eval" in line or "json." in line:
                        continue
                    if name == "compile" and ("re.compile" in line or "py_compile" in line):
                        continue
                    sev = Severity.HIGH if name != "compile" else Severity.MEDIUM
                    findings.append(Finding(
                        category="INJECTION",
                        severity=sev,
                        message=f"{name}() call -- potential code injection if input is external",
                        file=rel, line=i,
                        snippet=stripped[:120],
                    ))

            # SQL injection patterns
            if _SQL_CONCAT.search(line) or _SQL_FSTR.search(line):
                findings.append(Finding(
                    category="INJECTION",
                    severity=Severity.CRITICAL,
                    message="Possible SQL injection -- use parameterized queries",
                    file=rel, line=i,
                    snippet=stripped[:120],
                ))

    return findings


# ---------------------------------------------------------------------------
# 3. PROMPT INJECTION SURFACE
# ---------------------------------------------------------------------------

_CLAUDE_PROMPT_RE = re.compile(r'claude\s+-p|claude\s+--print')
_SANITIZE_IMPORT_RE = re.compile(r'from\s+agent_resilience\s+import.*sanitize_for_prompt|sanitize_for_prompt')

_EXTERNAL_CONTENT_VARS = re.compile(
    r'(?:scraped|external|raw|tweet|post|comment|content|reply|body|text|html|response_text)'
    r'(?:_data|_content|_text|_body|_raw)?',
    re.IGNORECASE,
)


def scan_prompt_injection(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for fp in files:
        if fp.suffix != ".py":
            continue
        rel = str(fp.relative_to(PROJECT_ROOT))
        lines = read_lines(fp)
        full_text = "\n".join(lines)

        has_sanitize = bool(_SANITIZE_IMPORT_RE.search(full_text))
        has_claude_call = bool(_CLAUDE_PROMPT_RE.search(full_text))

        if not has_claude_call:
            continue

        # Find lines where claude -p is invoked
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue

            if _CLAUDE_PROMPT_RE.search(line):
                # Check if this line or surrounding context uses external vars
                start = max(0, i - 10)
                end = min(len(lines), i + 5)
                context_window = "\n".join(lines[start:end])
                if _EXTERNAL_CONTENT_VARS.search(context_window) and not has_sanitize:
                    findings.append(Finding(
                        category="PROMPT_INJECTION",
                        severity=Severity.HIGH,
                        message="claude -p invoked near external content without sanitize_for_prompt()",
                        file=rel, line=i,
                        snippet=stripped[:120],
                    ))
                elif not has_sanitize:
                    findings.append(Finding(
                        category="PROMPT_INJECTION",
                        severity=Severity.MEDIUM,
                        message="File uses claude -p but does not import sanitize_for_prompt",
                        file=rel, line=i,
                        snippet=stripped[:120],
                    ))

        # Check for raw external content in prompt-building functions
        in_prompt_builder = False
        for i, line in enumerate(lines, 1):
            if "prompt" in line.lower() and ("def " in line or "= f" in line or "+=" in line):
                in_prompt_builder = True
            if in_prompt_builder and _EXTERNAL_CONTENT_VARS.search(line):
                if "sanitize" not in line.lower():
                    findings.append(Finding(
                        category="PROMPT_INJECTION",
                        severity=Severity.MEDIUM,
                        message="External content variable in prompt-building context without sanitization",
                        file=rel, line=i,
                        snippet=line.strip()[:120],
                    ))
            if in_prompt_builder and (line.strip() == "" or line.strip().startswith("def ")):
                in_prompt_builder = False

    return findings


# ---------------------------------------------------------------------------
# 4. FILE PERMISSION ISSUES
# ---------------------------------------------------------------------------

def scan_file_permissions(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for fp in files:
        if fp.suffix not in {".py", ".sh"}:
            continue
        rel = str(fp.relative_to(PROJECT_ROOT))
        try:
            mode = fp.stat().st_mode
        except OSError:
            continue

        # World-writable
        if mode & stat.S_IWOTH:
            findings.append(Finding(
                category="FILE_PERMS",
                severity=Severity.HIGH,
                message=f"World-writable script (mode {oct(mode)})",
                file=rel,
            ))

        # Group-writable
        if mode & stat.S_IWGRP:
            findings.append(Finding(
                category="FILE_PERMS",
                severity=Severity.LOW,
                message=f"Group-writable script (mode {oct(mode)})",
                file=rel,
            ))

    # Check for stale lock files (older than 6 hours)
    locks_dir = AUTOMATIONS_DIR / "locks"
    if locks_dir.exists():
        now = datetime.now().timestamp()
        for lf in locks_dir.glob("*.lock"):
            try:
                age_hours = (now - lf.stat().st_mtime) / 3600
                if age_hours > 6:
                    findings.append(Finding(
                        category="FILE_PERMS",
                        severity=Severity.LOW,
                        message=f"Stale lock file ({age_hours:.1f}h old): {lf.name}",
                        file=str(lf.relative_to(PROJECT_ROOT)),
                    ))
            except OSError:
                pass

    # Check for temp files written outside project
    _tmp_write_re = re.compile(r"""(?:open|write|Path)\s*\(.*['"]/tmp/""")
    for fp in files:
        if fp.suffix != ".py":
            continue
        rel = str(fp.relative_to(PROJECT_ROOT))
        lines = read_lines(fp)
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if _tmp_write_re.search(line):
                findings.append(Finding(
                    category="FILE_PERMS",
                    severity=Severity.MEDIUM,
                    message="Writing to /tmp/ -- use project-local temp directory instead",
                    file=rel, line=i,
                    snippet=stripped[:120],
                ))

    return findings


# ---------------------------------------------------------------------------
# 5. NETWORK EXPOSURE
# ---------------------------------------------------------------------------

_BIND_ALL = re.compile(r"""(?:host|bind)\s*=\s*["']0\.0\.0\.0["']""")
_HTTP_URL = re.compile(r"""["']http://(?!localhost|127\.0\.0\.1|0\.0\.0\.0)[\w.-]+""")
_OUTBOUND_POST = re.compile(
    r"""requests\.(?:post|put|patch|delete)\s*\(\s*(?:f?["']https?://(?!localhost|127\.0\.0\.1))"""
)


def scan_network(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for fp in files:
        if fp.suffix not in {".py", ".sh"}:
            continue
        rel = str(fp.relative_to(PROJECT_ROOT))
        lines = read_lines(fp)
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue

            # Binding to 0.0.0.0
            if _BIND_ALL.search(line):
                findings.append(Finding(
                    category="NETWORK",
                    severity=Severity.HIGH,
                    message="Binding to 0.0.0.0 -- use 127.0.0.1 for local-only services",
                    file=rel, line=i,
                    snippet=stripped[:120],
                ))

            # Unencrypted HTTP (non-localhost)
            if _HTTP_URL.search(line):
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    continue
                findings.append(Finding(
                    category="NETWORK",
                    severity=Severity.MEDIUM,
                    message="Unencrypted HTTP URL (should be HTTPS)",
                    file=rel, line=i,
                    snippet=stripped[:120],
                ))

            # Outbound data transmission
            if _OUTBOUND_POST.search(line):
                findings.append(Finding(
                    category="NETWORK",
                    severity=Severity.INFO,
                    message="Outbound POST to external URL -- verify this is expected",
                    file=rel, line=i,
                    snippet=stripped[:120],
                ))

    return findings


# ---------------------------------------------------------------------------
# 6. AGENT SAFETY
# ---------------------------------------------------------------------------

_WHILE_TRUE_RE = re.compile(r'while\s+True\s*:')
_BARE_EXCEPT_PASS_RE = re.compile(r'except\s*:')
_SAFE_PATH_PRESENT_RE = re.compile(r'(?:from\s+\S+\s+import.*safe_path|def\s+safe_path)')


def scan_agent_safety(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []

    # 6a. Check cron entries point to AUTOMATIONS/
    crontab_files = list(AUTOMATIONS_DIR.glob("crontab*.txt"))
    for ctf in crontab_files:
        rel = str(ctf.relative_to(PROJECT_ROOT))
        lines = read_lines(ctf)
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if re.match(r'^[A-Z_]+=', stripped):
                continue
            parts = stripped.split(None, 5)
            if len(parts) < 6:
                continue
            command = parts[5]
            script_match = re.search(r'(?:python3?|bash|sh)\s+(?:["\']?)(\S+\.(?:py|sh))', command)
            if script_match:
                script_path = script_match.group(1)
                if not (script_path.startswith("AUTOMATIONS/") or
                        script_path.startswith("$PROJECT") or
                        script_path.startswith(str(PROJECT_ROOT))):
                    findings.append(Finding(
                        category="AGENT_SAFETY",
                        severity=Severity.HIGH,
                        message=f"Cron entry runs script outside AUTOMATIONS/: {script_path}",
                        file=rel, line=i,
                        snippet=stripped[:120],
                    ))

    # 6b-6d. Scan Python files
    for fp in files:
        if fp.suffix != ".py":
            continue
        rel = str(fp.relative_to(PROJECT_ROOT))
        lines = read_lines(fp)
        full_text = "\n".join(lines)

        has_safe_path = bool(_SAFE_PATH_PRESENT_RE.search(full_text))
        does_file_write = bool(re.search(r'(?:open\s*\(|\.write\s*\(|\.write_text\s*\()', full_text))

        # 6b. Infinite loop without break/timeout
        for i, line in enumerate(lines, 1):
            if _WHILE_TRUE_RE.search(line):
                end_idx = min(len(lines), i + 50)
                window = "\n".join(lines[i:end_idx])
                has_break = "break" in window
                has_timeout = bool(re.search(r'timeout|max_iter|max_cycle|MAX_CYCLES|signal\.alarm', window))
                if not has_break and not has_timeout:
                    findings.append(Finding(
                        category="AGENT_SAFETY",
                        severity=Severity.MEDIUM,
                        message="while True without visible break/timeout in next 50 lines",
                        file=rel, line=i,
                        snippet=line.strip()[:120],
                    ))

        # 6c. Scripts that write files should use safe_path()
        if does_file_write and not has_safe_path:
            if str(fp).startswith(str(AUTOMATIONS_DIR)):
                findings.append(Finding(
                    category="AGENT_SAFETY",
                    severity=Severity.MEDIUM,
                    message="Script writes files but does not define/import safe_path()",
                    file=rel,
                ))

        # 6d. Bare except: pass (silent failure)
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if _BARE_EXCEPT_PASS_RE.search(stripped):
                for j in range(i, min(len(lines), i + 3)):
                    next_stripped = lines[j].strip()
                    if next_stripped in ("pass", "continue", "pass  # noqa"):
                        findings.append(Finding(
                            category="AGENT_SAFETY",
                            severity=Severity.LOW,
                            message="Bare 'except: pass' silently swallows all errors",
                            file=rel, line=i,
                            snippet=f"{stripped} ... {next_stripped}",
                        ))
                        break

    return findings


# ---------------------------------------------------------------------------
# Auto-fix engine
# ---------------------------------------------------------------------------

def apply_fixes(findings: list[Finding]) -> list[Finding]:
    """Apply trivial fixes. Returns list of fixed findings."""
    fixed: list[Finding] = []

    for f in findings:
        fp = PROJECT_ROOT / f.file if f.file else None

        # Fix: replace 0.0.0.0 with 127.0.0.1
        if (f.category == "NETWORK" and "0.0.0.0" in f.message and fp and fp.exists()):
            try:
                content = fp.read_text(encoding="utf-8")
                new_content = content.replace('"0.0.0.0"', '"127.0.0.1"').replace("'0.0.0.0'", "'127.0.0.1'")
                if new_content != content:
                    safe_path(fp)
                    fp.write_text(new_content, encoding="utf-8")
                    f.fix_applied = True
                    f.message += " [FIXED -> 127.0.0.1]"
                    fixed.append(f)
            except Exception:
                pass

        # Fix: add safe_path import for AUTOMATIONS scripts missing it
        if (f.category == "AGENT_SAFETY" and "safe_path" in f.message and fp and fp.exists()):
            try:
                content = fp.read_text(encoding="utf-8")
                if "safe_path" not in content:
                    import_line = "\nfrom _common import safe_path  # security audit auto-fix\n"
                    last_import = 0
                    for idx, ln in enumerate(content.splitlines()):
                        if ln.startswith("import ") or ln.startswith("from "):
                            last_import = idx
                    if last_import > 0:
                        lines_list = content.splitlines(True)
                        lines_list.insert(last_import + 1, import_line)
                        new_content = "".join(lines_list)
                        safe_path(fp)
                        fp.write_text(new_content, encoding="utf-8")
                        f.fix_applied = True
                        f.message += " [FIXED: added safe_path import]"
                        fixed.append(f)
            except Exception:
                pass

    return fixed


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def categorize(findings: list[Finding]) -> dict[str, list[Finding]]:
    cats: dict[str, list[Finding]] = {}
    for f in findings:
        cats.setdefault(f.category, []).append(f)
    return cats


def severity_counts(findings: list[Finding]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for f in findings:
        label = f.severity.label()
        counts[label] = counts.get(label, 0) + 1
    return counts


def overall_grade(findings: list[Finding]) -> str:
    """Compute letter grade from findings."""
    score = 100
    for f in findings:
        if f.fix_applied:
            continue
        if f.severity == Severity.CRITICAL:
            score -= 15
        elif f.severity == Severity.HIGH:
            score -= 8
        elif f.severity == Severity.MEDIUM:
            score -= 3
        elif f.severity == Severity.LOW:
            score -= 1
    score = max(0, score)
    if score >= 90:
        return f"A ({score}/100)"
    if score >= 80:
        return f"B ({score}/100)"
    if score >= 70:
        return f"C ({score}/100)"
    if score >= 60:
        return f"D ({score}/100)"
    return f"F ({score}/100)"


CATEGORY_DISPLAY = {
    "SECRETS": "Secrets Detection",
    "INJECTION": "Injection Vectors",
    "PROMPT_INJECTION": "Prompt Injection Surface",
    "FILE_PERMS": "File Permission Issues",
    "NETWORK": "Network Exposure",
    "AGENT_SAFETY": "Agent Safety",
}


def render_quick(findings: list[Finding]) -> str:
    """Quick summary: PASS/FAIL per category + count."""
    cats = categorize(findings)
    lines = [
        "PRINTMAXX SECURITY AUDIT -- QUICK SUMMARY",
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Grade: {overall_grade(findings)}",
        "",
    ]
    all_cats = ["SECRETS", "INJECTION", "PROMPT_INJECTION", "FILE_PERMS", "NETWORK", "AGENT_SAFETY"]
    for cat in all_cats:
        cat_findings = cats.get(cat, [])
        has_crit = any(f.severity >= Severity.HIGH for f in cat_findings)
        status = "FAIL" if has_crit else ("WARN" if cat_findings else "PASS")
        count = len(cat_findings)
        display = CATEGORY_DISPLAY.get(cat, cat)
        sev = severity_counts(cat_findings)
        sev_str = ", ".join(f"{k}:{v}" for k, v in sorted(sev.items())) if sev else "clean"
        lines.append(f"  [{status:4s}] {display:<30s}  {count:3d} findings  ({sev_str})")

    total = len(findings)
    unfixed = sum(1 for f in findings if not f.fix_applied)
    lines.append("")
    lines.append(f"Total findings: {total}  |  Unfixed: {unfixed}  |  Auto-fixed: {total - unfixed}")
    return "\n".join(lines)


def render_full(findings: list[Finding]) -> str:
    """Full report with file:line references."""
    cats = categorize(findings)
    lines = [
        "# PRINTMAXX Security Audit Report",
        "",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Grade:** {overall_grade(findings)}",
        f"**Total findings:** {len(findings)}",
        "",
        "---",
        "",
    ]

    all_cats = ["SECRETS", "INJECTION", "PROMPT_INJECTION", "FILE_PERMS", "NETWORK", "AGENT_SAFETY"]
    for cat in all_cats:
        cat_findings = cats.get(cat, [])
        display = CATEGORY_DISPLAY.get(cat, cat)
        has_crit = any(f.severity >= Severity.HIGH for f in cat_findings)
        status = "FAIL" if has_crit else ("WARN" if cat_findings else "PASS")
        lines.append(f"## {display} [{status}] ({len(cat_findings)} findings)")
        lines.append("")

        if not cat_findings:
            lines.append("No issues found.")
            lines.append("")
            continue

        sorted_findings = sorted(cat_findings, key=lambda x: x.severity, reverse=True)
        for f in sorted_findings:
            loc = f"{f.file}:{f.line}" if f.line else f.file
            fixed_tag = " [FIXED]" if f.fix_applied else ""
            lines.append(f"- **{f.severity.label()}**{fixed_tag}: {f.message}")
            if loc:
                lines.append(f"  - Location: `{loc}`")
            if f.snippet:
                lines.append(f"  - Snippet: `{f.snippet}`")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def render_json(findings: list[Finding]) -> str:
    """JSON output for agent consumption."""
    return json.dumps({
        "date": datetime.now().isoformat(),
        "grade": overall_grade(findings),
        "total": len(findings),
        "severity_counts": severity_counts(findings),
        "categories": {
            cat: {
                "count": len(cat_findings),
                "status": "FAIL" if any(f.severity >= Severity.HIGH for f in cat_findings)
                          else ("WARN" if cat_findings else "PASS"),
                "findings": [f.to_dict() for f in cat_findings],
            }
            for cat, cat_findings in categorize(findings).items()
        },
    }, indent=2, default=str)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_audit(do_fix: bool = False) -> list[Finding]:
    """Run all audit checks and return consolidated findings."""
    all_files = walk_project(ALL_EXTS)
    py_files = [f for f in all_files if f.suffix == ".py"]

    findings: list[Finding] = []
    findings.extend(scan_secrets(all_files))
    findings.extend(scan_env_files())
    findings.extend(scan_injection(py_files))
    findings.extend(scan_prompt_injection(py_files))
    findings.extend(scan_file_permissions(all_files))
    findings.extend(scan_network(all_files))
    findings.extend(scan_agent_safety(all_files))

    if do_fix:
        apply_fixes(findings)

    return findings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Security Audit -- scan project for security issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python3 AUTOMATIONS/security_audit.py              # full report
              python3 AUTOMATIONS/security_audit.py --quick      # summary only
              python3 AUTOMATIONS/security_audit.py --json       # JSON for agents
              python3 AUTOMATIONS/security_audit.py --fix        # auto-fix trivials
              python3 AUTOMATIONS/security_audit.py --fix --quick
        """),
    )
    parser.add_argument("--quick", action="store_true", help="Summary only (PASS/FAIL per category)")
    parser.add_argument("--json", action="store_true", help="JSON output for agent consumption")
    parser.add_argument("--fix", action="store_true", help="Auto-fix trivial issues")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help=f"Output file (default: {DEFAULT_REPORT.relative_to(PROJECT_ROOT)})")
    parser.add_argument("--no-save", action="store_true", help="Don't save report to file")
    args = parser.parse_args()

    findings = run_audit(do_fix=args.fix)

    # Render
    if args.json:
        output = render_json(findings)
    elif args.quick:
        output = render_quick(findings)
    else:
        output = render_full(findings)

    print(output)

    # Save report
    if not args.no_save:
        out_path = Path(args.output) if args.output else DEFAULT_REPORT
        try:
            out_path = safe_path(out_path)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(output, encoding="utf-8")
            print(f"\nReport saved to: {out_path.relative_to(PROJECT_ROOT)}")
        except Exception as e:
            print(f"\n[WARN] Could not save report: {e}", file=sys.stderr)

    # Exit code: 1 if any CRITICAL or HIGH findings unfixed
    unfixed_serious = [f for f in findings if f.severity >= Severity.HIGH and not f.fix_applied]
    sys.exit(1 if unfixed_serious else 0)


if __name__ == "__main__":
    main()
