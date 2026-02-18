#!/usr/bin/env python3
"""
PRINTMAXX — Cluely-Style Compliance Pack
=======================================

Goal: replicate the *compliant elements* (clear disclosure pages + clear footer
link placement) that show up in modern "AI avatar" / influencer-led marketing.

This script:
- Generates lightweight site policy pages (HTML) into known static build roots.
- Injects footer links to those pages into build entrypoints (idempotent).

It does NOT:
- Create accounts
- Post content
- Send emails
- Automate anything that would be a platform/identity deception risk
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, Tuple


BASE_DIR = Path(__file__).resolve().parent.parent
SECRETS_FILE = BASE_DIR / "SECRETS" / "PAYMENT_INFO.md"
STATE_DIR = BASE_DIR / "OPS" / "_state"
STATE_FILE = STATE_DIR / "cluely_compliance_pack.json"

MARKER = "<!-- PRINTMAXX LEGAL LINKS -->"


@dataclass(frozen=True)
class BuildTarget:
    name: str
    root: Path
    site_name: str
    entrypoints: Tuple[str, ...] = ("index.html",)


TARGETS: Tuple[BuildTarget, ...] = (
    BuildTarget("site-scorer", BASE_DIR / "builds" / "site-scorer", "SiteScore", ("index.html",)),
    BuildTarget("seo-analyzer-web", BASE_DIR / "builds" / "seo-analyzer-web", "SiteScore Pro", ("index.html",)),
    BuildTarget("programmatic_seo", BASE_DIR / "builds" / "programmatic_seo", "PRINTMAXX", ("index.html", "apps.html")),
    BuildTarget("master_dashboard", BASE_DIR / "builds" / "master_dashboard", "PRINTMAXX", ("index.html",)),
    BuildTarget("portfolio-landing", BASE_DIR / "builds" / "portfolio" / "landing-page", "Flowstack", ("index.html",)),
    BuildTarget("portfolio-dashboard", BASE_DIR / "builds" / "portfolio" / "dashboard", "ShopMetrics", ("index.html",)),
)


def _read_kv_md(path: Path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if not path.exists():
        return out
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip()
        if k:
            out[k] = v
    return out


def _load_or_init_state() -> Dict[str, str]:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if STATE_FILE.exists():
        try:
            payload = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                return {str(k): str(v) for k, v in payload.items()}
        except Exception:
            pass
    payload = {"generated_on": date.today().isoformat()}
    STATE_FILE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def _write_if_changed(path: Path, content: str) -> bool:
    if path.exists():
        try:
            current = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            current = ""
        if current == content:
            return False
    path.write_text(content, encoding="utf-8")
    return True


def _min_css() -> str:
    return """
    :root { color-scheme: light; }
    body { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 0; padding: 0; color: #111; background: #fff; }
    .wrap { max-width: 860px; margin: 0 auto; padding: 28px 18px 44px; }
    h1 { font-size: 28px; letter-spacing: -0.02em; margin: 0 0 8px; }
    h2 { font-size: 18px; margin: 22px 0 8px; }
    p, li { line-height: 1.55; }
    .meta { color: #555; font-size: 13px; margin-bottom: 18px; }
    .box { background: #f6f7fb; border: 1px solid #e6e8f2; border-radius: 10px; padding: 14px 14px; }
    code { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.95em; }
    a { color: #0b57d0; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .footer { margin-top: 26px; padding-top: 16px; border-top: 1px solid #eee; color: #666; font-size: 13px; }
    """


def _html_page(title: str, body_html: str, *, site_name: str, generated_on: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_escape_html(title)} | { _escape_html(site_name) }</title>
  <style>{_min_css()}</style>
</head>
<body>
  <main class="wrap">
    <h1>{_escape_html(title)}</h1>
    <div class="meta">Last updated: <strong>{_escape_html(generated_on)}</strong></div>
    {body_html}
    <div class="footer">
      <div>{_escape_html(site_name)} · <a href="marketing-disclosure.html">Marketing Disclosure</a> · <a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></div>
    </div>
  </main>
</body>
</html>
"""


def _escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def marketing_disclosure_html(*, site_name: str, contact_email: str, generated_on: str) -> str:
    body = f"""
    <div class="box">
      <p><strong>Summary:</strong> We disclose material connections (sponsorships, affiliates, paid partnerships) and we label content that could reasonably be misunderstood as coming from a real person when it is generated by or features AI/virtual characters.</p>
    </div>

    <h2>1) Official vs UGC vs Satire/Fiction</h2>
    <ul>
      <li><strong>Official content</strong>: content published by { _escape_html(site_name) } or its owned accounts.</li>
      <li><strong>UGC (user-generated content)</strong>: content created by third parties. If there is a material connection (paid, free product, affiliate), it should be disclosed clearly in the content itself.</li>
      <li><strong>Satire/fiction</strong>: if we publish content intended as satire or fictionalized storytelling, we label it as such where it appears.</li>
    </ul>

    <h2>2) Affiliate Links and Sponsored Content</h2>
    <p>Some pages/posts/emails may include affiliate links or sponsored placements. When that happens:</p>
    <ul>
      <li>We include an in-content disclosure such as <code>#ad</code>, <code>Paid partnership</code>, or <code>I may earn a commission</code> (format varies by platform).</li>
      <li>Disclosures should be <strong>clear and conspicuous</strong>, not hidden in a bio, footer, or after long blocks of hashtags.</li>
    </ul>

    <h2>3) AI / Virtual Personas and Synthetic Media</h2>
    <p>{ _escape_html(site_name) } may use AI tools to create or assist with text, images, audio, video, or to operate virtual characters. If content features a virtual/AI character that could be mistaken for a real person:</p>
    <ul>
      <li>We label the account and/or post as <strong>AI / virtual</strong>.</li>
      <li>We do not impersonate real individuals or use someone’s likeness without permission.</li>
      <li>We avoid “personal experience” claims that imply a real human lived the story when it is not true.</li>
    </ul>

    <h2>4) Testimonials and Results</h2>
    <ul>
      <li>Testimonials are presented as real customer opinions unless explicitly labeled as simulated/illustrative.</li>
      <li>Results depend on many factors; <strong>results may vary</strong>.</li>
    </ul>

    <h2>5) Questions or Corrections</h2>
    <p>If you believe a disclosure is missing or unclear, contact us: <a href="mailto:{_escape_html(contact_email)}">{_escape_html(contact_email)}</a>.</p>
    """
    return _html_page("Marketing Disclosure", body, site_name=site_name, generated_on=generated_on)


def privacy_html(*, site_name: str, contact_email: str, generated_on: str) -> str:
    body = f"""
    <div class="box">
      <p><strong>Minimal policy:</strong> This site may collect basic analytics and form submissions. We do not sell personal information. Contact: <a href="mailto:{_escape_html(contact_email)}">{_escape_html(contact_email)}</a>.</p>
    </div>
    <h2>What we collect</h2>
    <ul>
      <li>Information you submit via forms (if enabled)</li>
      <li>Basic technical data (device, browser, approximate location) via analytics (if enabled)</li>
    </ul>
    <h2>How we use it</h2>
    <ul>
      <li>To operate and improve the product</li>
      <li>To respond to requests</li>
      <li>To prevent abuse</li>
    </ul>
    <h2>Contact</h2>
    <p>Email: <a href="mailto:{_escape_html(contact_email)}">{_escape_html(contact_email)}</a></p>
    """
    return _html_page("Privacy Policy", body, site_name=site_name, generated_on=generated_on)


def terms_html(*, site_name: str, contact_email: str, generated_on: str) -> str:
    body = f"""
    <div class="box">
      <p><strong>Disclaimer:</strong> This site is provided “as is” for informational purposes and may change at any time. If something looks wrong, contact: <a href="mailto:{_escape_html(contact_email)}">{_escape_html(contact_email)}</a>.</p>
    </div>
    <h2>Use of the site</h2>
    <ul>
      <li>Do not misuse or attempt to disrupt the service.</li>
      <li>Do not rely on outputs for legal/medical/financial decisions without independent verification.</li>
    </ul>
    <h2>Limitation of liability</h2>
    <p>To the maximum extent permitted by law, { _escape_html(site_name) } is not liable for indirect or consequential damages arising from use of this site.</p>
    <h2>Contact</h2>
    <p>Email: <a href="mailto:{_escape_html(contact_email)}">{_escape_html(contact_email)}</a></p>
    """
    return _html_page("Terms of Service", body, site_name=site_name, generated_on=generated_on)


def cookies_html(*, site_name: str, generated_on: str) -> str:
    body = """
    <div class="box">
      <p><strong>Minimal notice:</strong> This site may use cookies or local storage for basic functionality and analytics (if enabled). You can clear cookies in your browser settings.</p>
    </div>
    """
    return _html_page("Cookie Notice", body, site_name=site_name, generated_on=generated_on)


def _legal_snippet() -> str:
    # Inline styles so we don't depend on each build's CSS.
    return f"""{MARKER}
<div style="margin-top:12px; font-size:12px; opacity:0.85; text-align:center;">
  <a href="marketing-disclosure.html">Marketing Disclosure</a>
  <span style="opacity:0.6;"> · </span>
  <a href="privacy.html">Privacy</a>
  <span style="opacity:0.6;"> · </span>
  <a href="terms.html">Terms</a>
</div>
"""


def _repair_backref_artifacts(html: str) -> str:
    # Bug from an earlier implementation: a literal "\1" was written where a closing
    # tag should have been. Repair idempotently.
    if "\\1" not in html:
        return html

    out = html
    while "\\1" in out:
        idx = out.find("\\1")
        if idx < 0:
            break
        after = out[idx + 2 :].lower()
        replacement = "</footer>" if "</body" in after else "</body>"
        out = out[:idx] + replacement + out[idx + 2 :]
    return out


def _inject_into_html(html: str) -> str:
    html = _repair_backref_artifacts(html)

    if MARKER in html:
        return html

    snippet = _legal_snippet()

    # Prefer injecting into an existing footer.
    m = re.search(r"</footer>", html, flags=re.IGNORECASE)
    if m:
        return html[: m.start()] + snippet + "\n" + html[m.start() :]

    # Otherwise add a minimal footer before </body>.
    m = re.search(r"</body>", html, flags=re.IGNORECASE)
    if m:
        footer = (
            "\n<footer style=\"padding:18px 12px; border-top:1px solid rgba(0,0,0,0.08);\">"
            + snippet
            + "</footer>\n"
        )
        return html[: m.start()] + footer + html[m.start() :]

    # Fallback: append.
    return html + "\n" + snippet


def apply_pack() -> int:
    secrets = _read_kv_md(SECRETS_FILE)
    state = _load_or_init_state()

    contact_email = (secrets.get("EMAIL") or "contact@example.com").strip()
    generated_on = (state.get("generated_on") or date.today().isoformat()).strip()

    changed_any = False
    injected_any = False

    for t in TARGETS:
        if not t.root.exists():
            continue

        page_map = {
            "marketing-disclosure.html": marketing_disclosure_html(
                site_name=t.site_name, contact_email=contact_email, generated_on=generated_on
            ),
            "privacy.html": privacy_html(site_name=t.site_name, contact_email=contact_email, generated_on=generated_on),
            "terms.html": terms_html(site_name=t.site_name, contact_email=contact_email, generated_on=generated_on),
            "cookies.html": cookies_html(site_name=t.site_name, generated_on=generated_on),
        }

        for filename, content in page_map.items():
            changed_any = _write_if_changed(t.root / filename, content) or changed_any

        for ep in t.entrypoints:
            p = t.root / ep
            if not p.exists():
                continue
            html = p.read_text(encoding="utf-8", errors="replace")
            patched = _inject_into_html(html)
            if patched != html:
                p.write_text(patched, encoding="utf-8")
                injected_any = True

    print("cluely_compliance_pack: ok")
    print("- legal pages written: 4")
    print(f"- changed_any: {changed_any}")
    print(f"- injected_any: {injected_any}")
    return 0


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Write pages + inject footer links (idempotent).")
    args = ap.parse_args()

    if args.apply:
        return apply_pack()
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
