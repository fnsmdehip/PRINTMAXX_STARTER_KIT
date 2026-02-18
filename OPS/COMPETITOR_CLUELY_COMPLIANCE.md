# Cluely Compliance Patterns (Observed) → PRINTMAXX Replication

Purpose: capture *what’s worth copying safely* from Cluely-style marketing pages: disclosure architecture + placement that reduces FTC/platform risk while keeping conversion high.

This is a pattern memo, not legal advice and not allegations about any company.

---

## 1) Disclosure Placement (What Stands Out)

- Strong footer “Legal” hygiene (Privacy/Terms/etc. are easy to find on landing pages).
- A dedicated **Marketing Disclosure** page exists and is written in plain language.
- Their marketing disclosure is framed as applying to specific marketing content that is linked/annotated with it (not necessarily a blanket statement for every piece of content).

---

## 2) How They Frame UGC, Satire, and Testimonials

- Marketing is categorized into buckets (official content vs third-party/UGC vs satirical content).
- UGC and satire are presented as labeled when applicable.
- Testimonials are described as authentic unless explicitly labeled otherwise.

Practical takeaway: you can run high-volume creator distribution *without* hiding the ball by writing a clear policy and mirroring that clarity in-content.

---

## 3) AI Avatar / Virtual Persona Framing (Safe Replication)

PRINTMAXX posture:
- If a persona could be mistaken for a real person, label it as **AI / virtual** in bio and, when appropriate, in-content.
- Never impersonate real individuals.
- Avoid “personal experience” claims when it’s a virtual persona (use “users report…” / “in our testing…” framing).

Canonical templates:
- `09_LEGAL/ftc_compliance/AI_DISCLOSURE.md`
- `09_LEGAL/ftc_compliance/TESTIMONIAL_GUIDELINES.md`
- `09_LEGAL/ftc_compliance/AFFILIATE_DISCLOSURE.md`

---

## 4) Replication Implemented in PRINTMAXX

Automation:
- `AUTOMATIONS/cluely_compliance_pack.py` writes disclosure/policy HTML pages into static build roots and injects footer links (idempotent).
- Wired into the 24/7 loop via `AUTOMATIONS/ship_captain.py` as auto step `cluely_pack`.

Pages generated into each build root:
- `marketing-disclosure.html`
- `privacy.html`
- `terms.html`
- `cookies.html`

Build entrypoints patched to link these in the footer:
- `builds/site-scorer/index.html`
- `builds/seo-analyzer-web/index.html`
- `builds/programmatic_seo/index.html`
- `builds/programmatic_seo/apps.html`
- `builds/master_dashboard/index.html`
- `builds/portfolio/landing-page/index.html`
- `builds/portfolio/dashboard/index.html`

