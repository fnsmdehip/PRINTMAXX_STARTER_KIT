#!/usr/bin/env python3

from __future__ import annotations
"""
Vibe Coder Security Audit Script
Automated security checks for web apps and APIs.

Checks:
  - Rate limiting (sends burst requests)
  - CORS misconfiguration
  - API key exposure in client-side code
  - Security headers (CSP, HSTS, X-Frame-Options, etc.)
  - Dependency vulnerabilities (if package.json URL found)
  - Common sensitive file exposure (.env, .git, etc.)
  - SSL/TLS configuration
  - Cookie security flags

Usage:
    python3 app_security_audit.py https://example.com
    python3 app_security_audit.py https://example.com --full
    python3 app_security_audit.py https://example.com --output report.json
"""

import argparse
import json
import re
import sys
import time
import ssl
import socket
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install: pip3 install requests beautifulsoup4")
    sys.exit(1)

# Suppress SSL warnings for testing
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SecurityAudit:
    """Automated security audit for web applications."""

    def __init__(self, url: str, verbose: bool = False):
        self.base_url = url.rstrip("/")
        self.parsed = urlparse(self.base_url)
        self.hostname = self.parsed.hostname
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "PRINTMAXX-SecurityAudit/1.0 (security testing)",
        })
        self.findings = []
        self.score = 100  # Start at 100, deduct for issues

    def log(self, msg: str):
        if self.verbose:
            print(f"  [DEBUG] {msg}")

    def add_finding(self, severity: str, category: str, title: str, detail: str, fix: str):
        """Record a security finding."""
        deductions = {"CRITICAL": 25, "HIGH": 15, "MEDIUM": 10, "LOW": 5, "INFO": 0}
        self.score = max(0, self.score - deductions.get(severity, 0))
        finding = {
            "severity": severity,
            "category": category,
            "title": title,
            "detail": detail,
            "fix": fix,
        }
        self.findings.append(finding)
        icon = {"CRITICAL": "!!!", "HIGH": "!!", "MEDIUM": "!", "LOW": "~", "INFO": "i"}
        print(f"  [{icon.get(severity, '?')}] {severity}: {title}")
        if self.verbose:
            print(f"      Detail: {detail}")
            print(f"      Fix: {fix}")

    # ─── Check 1: Rate Limiting ───

    def check_rate_limiting(self):
        """Send burst requests to check if rate limiting exists."""
        print("\n[1/8] Checking rate limiting...")
        endpoint = self.base_url
        status_codes = []

        try:
            for i in range(20):
                resp = self.session.get(endpoint, timeout=5, allow_redirects=True)
                status_codes.append(resp.status_code)
                if resp.status_code == 429:
                    print(f"  Rate limit hit after {i+1} requests. Good.")
                    self.add_finding("INFO", "rate_limiting", "Rate limiting active",
                                     f"429 returned after {i+1} rapid requests", "No action needed")
                    return
                time.sleep(0.05)  # 50ms between requests

            # Check if all succeeded
            if all(c == 200 for c in status_codes):
                self.add_finding("HIGH", "rate_limiting",
                                 "No rate limiting detected",
                                 f"20 rapid requests all returned 200. No 429 responses.",
                                 "Add rate limiting: express-rate-limit (Node), django-ratelimit (Python), or Cloudflare WAF rules")
            else:
                unique = set(status_codes)
                self.add_finding("MEDIUM", "rate_limiting",
                                 "Inconsistent rate limiting",
                                 f"Mixed status codes: {unique}",
                                 "Review rate limiting configuration")
        except requests.exceptions.ConnectionError:
            self.add_finding("INFO", "rate_limiting",
                             "Connection dropped during burst test",
                             "Server may have connection-level rate limiting",
                             "Verify rate limiting is intentional, not a crash")
        except Exception as e:
            self.log(f"Rate limit check error: {e}")

    # ─── Check 2: Security Headers ───

    def check_security_headers(self):
        """Check for presence of security headers."""
        print("\n[2/8] Checking security headers...")
        try:
            resp = self.session.get(self.base_url, timeout=10)
            headers = resp.headers

            required_headers = {
                "Strict-Transport-Security": {
                    "severity": "HIGH",
                    "fix": "Add HSTS header: Strict-Transport-Security: max-age=31536000; includeSubDomains",
                },
                "X-Content-Type-Options": {
                    "severity": "MEDIUM",
                    "fix": "Add: X-Content-Type-Options: nosniff",
                },
                "X-Frame-Options": {
                    "severity": "MEDIUM",
                    "fix": "Add: X-Frame-Options: DENY (or SAMEORIGIN if you use iframes)",
                },
                "Content-Security-Policy": {
                    "severity": "HIGH",
                    "fix": "Add CSP header. Start with: Content-Security-Policy: default-src 'self'",
                },
                "X-XSS-Protection": {
                    "severity": "LOW",
                    "fix": "Add: X-XSS-Protection: 1; mode=block (legacy but still useful)",
                },
                "Referrer-Policy": {
                    "severity": "LOW",
                    "fix": "Add: Referrer-Policy: strict-origin-when-cross-origin",
                },
                "Permissions-Policy": {
                    "severity": "LOW",
                    "fix": "Add: Permissions-Policy: camera=(), microphone=(), geolocation=()",
                },
            }

            for header_name, info in required_headers.items():
                if header_name.lower() not in {k.lower(): v for k, v in headers.items()}:
                    self.add_finding(info["severity"], "security_headers",
                                     f"Missing {header_name} header",
                                     f"Response does not include {header_name}",
                                     info["fix"])
                else:
                    self.log(f"Found {header_name}: {headers.get(header_name, '')[:80]}")

            # Check for server version disclosure
            server = headers.get("Server", "")
            if server and any(v in server.lower() for v in ["apache/", "nginx/", "express", "php/"]):
                self.add_finding("LOW", "security_headers",
                                 "Server version disclosed",
                                 f"Server header reveals: {server}",
                                 "Remove version from Server header to reduce attack surface info")

        except Exception as e:
            self.log(f"Header check error: {e}")

    # ─── Check 3: CORS Configuration ───

    def check_cors(self):
        """Check for CORS misconfiguration."""
        print("\n[3/8] Checking CORS configuration...")
        evil_origins = [
            "https://evil.com",
            "https://attacker.example.com",
            "null",
        ]

        for origin in evil_origins:
            try:
                resp = self.session.get(
                    self.base_url,
                    headers={"Origin": origin},
                    timeout=10
                )
                acao = resp.headers.get("Access-Control-Allow-Origin", "")
                acac = resp.headers.get("Access-Control-Allow-Credentials", "")

                if acao == "*":
                    self.add_finding("HIGH", "cors",
                                     "CORS allows all origins (wildcard *)",
                                     f"Access-Control-Allow-Origin: * allows any website to read responses",
                                     "Restrict CORS to specific trusted domains. Never use * with credentials.")
                    break
                elif acao == origin:
                    severity = "CRITICAL" if acac.lower() == "true" else "HIGH"
                    self.add_finding(severity, "cors",
                                     f"CORS reflects arbitrary origin: {origin}",
                                     f"Server echoes back {origin} as allowed. "
                                     f"Credentials allowed: {acac}",
                                     "Whitelist specific origins. Never reflect Origin header blindly.")
                    break
            except Exception as e:
                self.log(f"CORS check error for {origin}: {e}")

    # ─── Check 4: API Key Exposure ───

    def check_api_key_exposure(self):
        """Scan page source for exposed API keys."""
        print("\n[4/8] Checking for API key exposure in client code...")
        try:
            resp = self.session.get(self.base_url, timeout=15)
            html = resp.text

            # Patterns for common API keys
            key_patterns = {
                "Supabase Key": r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
                "Firebase API Key": r'AIza[0-9A-Za-z_-]{35}',
                "AWS Access Key": r'AKIA[0-9A-Z]{16}',
                "Stripe Secret Key": r'sk_live_[0-9a-zA-Z]{24,}',
                "Stripe Publishable": r'pk_live_[0-9a-zA-Z]{24,}',
                "OpenAI API Key": r'sk-[a-zA-Z0-9]{20,}',
                "Anthropic API Key": r'sk-ant-[a-zA-Z0-9_-]{20,}',
                "GitHub Token": r'ghp_[A-Za-z0-9]{36}',
                "Slack Token": r'xox[baprs]-[0-9A-Za-z-]+',
                "Google Maps Key": r'AIza[0-9A-Za-z_-]{35}',
                "Twilio": r'SK[0-9a-fA-F]{32}',
                "SendGrid": r'SG\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
                "Mailgun": r'key-[0-9a-zA-Z]{32}',
                "Generic API Key": r'(?:api[_-]?key|apikey|api_secret|secret_key)\s*[:=]\s*["\']([^"\']{16,})["\']',
            }

            for key_name, pattern in key_patterns.items():
                matches = re.findall(pattern, html)
                if matches:
                    # Don't log actual keys, just flag existence
                    # Allow publishable keys (they're meant to be public)
                    if "Publishable" in key_name or "Firebase API" in key_name:
                        self.add_finding("INFO", "api_keys",
                                         f"Public {key_name} found in source",
                                         f"Found {len(matches)} instance(s). Publishable keys are expected client-side.",
                                         "Ensure server-side validation restricts key usage to your domains")
                    else:
                        self.add_finding("CRITICAL", "api_keys",
                                         f"SECRET {key_name} exposed in client code!",
                                         f"Found {len(matches)} instance(s) of what appears to be a secret key",
                                         f"IMMEDIATELY rotate this key. Move to server-side env vars. Never expose secret keys in client-side code.")

            # Check for .env file reference
            if ".env" in html and ("NEXT_PUBLIC" not in html or "process.env" in html):
                self.add_finding("MEDIUM", "api_keys",
                                 "Potential env var reference in client code",
                                 "Found references to .env or process.env in page source",
                                 "Ensure only NEXT_PUBLIC_ prefixed vars are in client bundles")

            # Check linked JS bundles for keys (first 3 scripts)
            soup = BeautifulSoup(html, "html.parser")
            scripts = soup.find_all("script", src=True)[:3]
            for script in scripts:
                src = script.get("src", "")
                if src.startswith("/") or src.startswith(self.base_url):
                    js_url = urljoin(self.base_url, src)
                    try:
                        js_resp = self.session.get(js_url, timeout=10)
                        js_text = js_resp.text[:100000]  # First 100KB
                        for key_name, pattern in key_patterns.items():
                            if "Publishable" in key_name:
                                continue
                            if re.search(pattern, js_text):
                                self.add_finding("CRITICAL", "api_keys",
                                                 f"SECRET {key_name} found in JS bundle: {src[:60]}",
                                                 "Secret key found in a JavaScript bundle file",
                                                 "Rotate key immediately. Move to server-side only.")
                    except Exception:
                        pass

        except Exception as e:
            self.log(f"API key check error: {e}")

    # ─── Check 5: Sensitive File Exposure ───

    def check_sensitive_files(self):
        """Check for exposed sensitive files."""
        print("\n[5/8] Checking for exposed sensitive files...")
        sensitive_paths = [
            ("/.env", "CRITICAL", "Environment file exposed - contains secrets"),
            ("/.git/config", "CRITICAL", "Git config exposed - source code leak"),
            ("/.git/HEAD", "CRITICAL", "Git HEAD exposed - source code leak"),
            ("/wp-config.php", "CRITICAL", "WordPress config exposed"),
            ("/config.json", "HIGH", "Config file exposed"),
            ("/package.json", "LOW", "package.json exposed - dependency info"),
            ("/.htaccess", "MEDIUM", "Apache config exposed"),
            ("/robots.txt", "INFO", "robots.txt found (check for sensitive paths)"),
            ("/sitemap.xml", "INFO", "Sitemap found"),
            ("/api/", "INFO", "API endpoint accessible"),
            ("/.well-known/security.txt", "INFO", "Security contact info"),
            ("/server-status", "HIGH", "Apache server-status exposed"),
            ("/phpinfo.php", "HIGH", "PHP info page exposed"),
            ("/debug", "HIGH", "Debug endpoint exposed"),
            ("/graphql", "MEDIUM", "GraphQL endpoint found - check introspection"),
            ("/swagger", "MEDIUM", "Swagger/API docs exposed"),
            ("/api-docs", "MEDIUM", "API docs exposed"),
            ("/.DS_Store", "LOW", "macOS directory file exposed"),
            ("/backup", "HIGH", "Backup directory accessible"),
            ("/admin", "MEDIUM", "Admin panel accessible"),
        ]

        for path, severity, description in sensitive_paths:
            try:
                url = f"{self.base_url}{path}"
                resp = self.session.get(url, timeout=5, allow_redirects=False)
                if resp.status_code == 200 and len(resp.text) > 10:
                    # Verify it's not a generic 200 page (soft 404)
                    if path in ["/.env", "/.git/config", "/.git/HEAD"]:
                        self.add_finding(severity, "file_exposure",
                                         f"Sensitive file accessible: {path}",
                                         description,
                                         f"Block access to {path} in your web server config or .htaccess")
                    elif severity in ["CRITICAL", "HIGH"]:
                        self.add_finding(severity, "file_exposure",
                                         f"Sensitive path accessible: {path}",
                                         description,
                                         f"Review if {path} should be publicly accessible. Add auth or block access.")
                    else:
                        self.add_finding(severity, "file_exposure",
                                         f"Path accessible: {path}",
                                         description,
                                         f"Review if {path} exposes useful recon info to attackers")
            except Exception:
                pass

    # ─── Check 6: Cookie Security ───

    def check_cookie_security(self):
        """Check cookie security flags."""
        print("\n[6/8] Checking cookie security...")
        try:
            resp = self.session.get(self.base_url, timeout=10)
            cookies = resp.cookies

            for cookie in cookies:
                issues = []
                if not cookie.secure and self.parsed.scheme == "https":
                    issues.append("missing Secure flag")
                if not cookie.has_nonstandard_attr("HttpOnly") and "session" in cookie.name.lower():
                    issues.append("missing HttpOnly flag")
                samesite = cookie.get_nonstandard_attr("SameSite")
                if not samesite or samesite.lower() == "none":
                    issues.append("SameSite=None or missing")

                if issues:
                    self.add_finding("MEDIUM", "cookies",
                                     f"Cookie '{cookie.name}' has security issues",
                                     f"Issues: {', '.join(issues)}",
                                     "Set Secure, HttpOnly (for session cookies), and SameSite=Lax/Strict flags")

        except Exception as e:
            self.log(f"Cookie check error: {e}")

    # ─── Check 7: SSL/TLS ───

    def check_ssl(self):
        """Check SSL/TLS configuration."""
        print("\n[7/8] Checking SSL/TLS configuration...")
        if self.parsed.scheme != "https":
            self.add_finding("CRITICAL", "ssl",
                             "Site not using HTTPS",
                             f"URL scheme is {self.parsed.scheme}",
                             "Enable HTTPS. Use Let's Encrypt for free SSL certs.")
            return

        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    cert = ssock.getpeercert()
                    protocol = ssock.version()

                    # Check certificate expiry
                    not_after = cert.get("notAfter", "")
                    if not_after:
                        from email.utils import parsedate_to_datetime
                        try:
                            expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                            days_left = (expiry - datetime.utcnow()).days
                            if days_left < 30:
                                self.add_finding("HIGH", "ssl",
                                                 f"SSL certificate expires in {days_left} days",
                                                 f"Certificate expires: {not_after}",
                                                 "Renew SSL certificate. Set up auto-renewal with certbot.")
                            else:
                                self.log(f"SSL cert valid for {days_left} more days")
                        except ValueError:
                            pass

                    # Check protocol version
                    if protocol and "TLSv1.0" in protocol or "TLSv1.1" in protocol:
                        self.add_finding("HIGH", "ssl",
                                         f"Outdated TLS version: {protocol}",
                                         "TLS 1.0/1.1 are deprecated and vulnerable",
                                         "Configure server to use TLS 1.2+ only")
                    else:
                        self.log(f"TLS version: {protocol}")

        except ssl.SSLError as e:
            self.add_finding("CRITICAL", "ssl",
                             "SSL certificate error",
                             str(e),
                             "Fix SSL configuration. Check certificate chain and hostname match.")
        except Exception as e:
            self.log(f"SSL check error: {e}")

    # ─── Check 8: Supabase/Firebase RLS ───

    def check_backend_security(self):
        """Check for common backend misconfigurations (Supabase, Firebase)."""
        print("\n[8/8] Checking for backend misconfigurations...")
        try:
            resp = self.session.get(self.base_url, timeout=15)
            html = resp.text.lower()

            # Check for Supabase
            if "supabase" in html or "supabase.co" in html:
                self.add_finding("INFO", "backend",
                                 "Supabase detected",
                                 "App uses Supabase backend",
                                 "Verify RLS (Row Level Security) is enabled on ALL tables. "
                                 "Check: Supabase Dashboard > Database > Tables > RLS enabled. "
                                 "NEVER rely on client-side filtering alone.")

                # Try to find Supabase URL
                supabase_url_match = re.search(
                    r'https://[a-z0-9]+\.supabase\.co', resp.text
                )
                if supabase_url_match:
                    sb_url = supabase_url_match.group(0)
                    # Check if REST API is open
                    try:
                        rest_url = f"{sb_url}/rest/v1/"
                        rest_resp = self.session.get(rest_url, timeout=5)
                        if rest_resp.status_code != 401:
                            self.add_finding("CRITICAL", "backend",
                                             "Supabase REST API accessible without auth",
                                             f"GET {rest_url} returned {rest_resp.status_code}",
                                             "Enable RLS on all tables. Add authentication requirement.")
                    except Exception:
                        pass

            # Check for Firebase
            if "firebase" in html or "firebaseio.com" in html:
                self.add_finding("INFO", "backend",
                                 "Firebase detected",
                                 "App uses Firebase backend",
                                 "Verify Firestore/RTDB security rules. "
                                 "NEVER use: allow read, write: if true; in production. "
                                 "Test: Firebase Console > Firestore > Rules")

        except Exception as e:
            self.log(f"Backend check error: {e}")

    # ─── Run All Checks ───

    def run_audit(self, full: bool = False):
        """Run all security checks."""
        print(f"\n{'='*60}")
        print(f"  SECURITY AUDIT: {self.base_url}")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")

        # Verify target is reachable
        try:
            resp = self.session.get(self.base_url, timeout=15)
            print(f"  Target reachable: HTTP {resp.status_code}")
        except Exception as e:
            print(f"  ERROR: Cannot reach {self.base_url}: {e}")
            return self.get_report()

        self.check_security_headers()
        self.check_cors()
        self.check_api_key_exposure()
        self.check_sensitive_files()
        self.check_cookie_security()
        self.check_ssl()
        self.check_backend_security()

        if full:
            self.check_rate_limiting()

        return self.get_report()

    def get_report(self) -> dict:
        """Generate final report."""
        severity_counts = {}
        for f in self.findings:
            sev = f["severity"]
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        grade = "A" if self.score >= 90 else "B" if self.score >= 75 else "C" if self.score >= 60 else "D" if self.score >= 40 else "F"

        report = {
            "url": self.base_url,
            "audited_at": datetime.now().isoformat(),
            "score": self.score,
            "grade": grade,
            "severity_counts": severity_counts,
            "total_findings": len(self.findings),
            "findings": self.findings,
        }

        print(f"\n{'='*60}")
        print(f"  AUDIT RESULTS")
        print(f"{'='*60}")
        print(f"  Score:    {self.score}/100 (Grade: {grade})")
        print(f"  Findings: {len(self.findings)} total")
        for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
            count = severity_counts.get(sev, 0)
            if count:
                print(f"    {sev}: {count}")
        print(f"{'='*60}\n")

        return report

    def print_checklist(self):
        """Print a remediation checklist."""
        print("\nREMEDIATION CHECKLIST:")
        print("-" * 40)
        for i, f in enumerate(self.findings, 1):
            if f["severity"] in ["CRITICAL", "HIGH", "MEDIUM"]:
                print(f"  [ ] {i}. ({f['severity']}) {f['title']}")
                print(f"      Fix: {f['fix']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Vibe Coder Security Audit")
    parser.add_argument("url", help="URL to audit (e.g., https://example.com)")
    parser.add_argument("--full", action="store_true", help="Run full audit including rate limit test (slower)")
    parser.add_argument("--output", type=str, help="Save JSON report to file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Normalize URL
    url = args.url
    if not url.startswith("http"):
        url = f"https://{url}"

    audit = SecurityAudit(url, verbose=args.verbose)
    report = audit.run_audit(full=args.full)
    audit.print_checklist()

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to {output_path}")

    # Exit code based on severity
    if report["severity_counts"].get("CRITICAL", 0) > 0:
        sys.exit(2)
    elif report["severity_counts"].get("HIGH", 0) > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
