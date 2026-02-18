# Compliance-First Growth Playbook (Edge Cases, Not Evasion)

This file is the compliance-first rewrite of the older "grey hat" playbook.
It exists as a *separate* document so you can make the executive call on what to apply without losing any prior notes.

**Non-negotiables:**
- No impersonation, fake identities, or “account farming” tactics.
- No fake testimonials, fake reviews, or simulated results presented as real.
- Disclose material connections clearly and in-content (not hidden in footers/bios).
- If content uses AI/virtual personas or synthetic media that could be mistaken for real, label it.

This playbook exists to help PRINTMAXX scale distribution **without** crossing into illegal or deceptive behavior.

---

## The Cluely case study (what to copy safely)

We treat Cluely as a *public disclosure pattern reference*, not as a basis for allegations.

**What is worth copying (compliance architecture):**
- A dedicated **Marketing Disclosure** page that explains:
  - What counts as official marketing vs third-party content
  - How endorsements/UGC/satire are labeled
  - How testimonials are treated
- Strong footer “Legal” hygiene (Privacy/Terms/etc. are easy to find).

**PRINTMAXX implementation:**
- Static builds get:
  - `marketing-disclosure.html`
  - `privacy.html`
  - `terms.html`
  - Footer links injected into entrypoints
- Generated/maintained by `AUTOMATIONS/cluely_compliance_pack.py`.

---

## Disclosure placement rules (operational)

**Affiliate/sponsored/paid partnerships:**
- Put disclosure **in the content** (caption, first lines, overlay, or spoken).
- Do not rely on “link in bio” or footer-only disclosure.

**AI / virtual personas / synthetic media:**
- If the audience could reasonably think it’s a real human or real footage:
  - Label it as AI/virtual/synthetic using the platform tool (when available)
  - Also label it in the content/bio in plain language

---

## What to avoid (high-risk)

- Any tactic that depends on deception about identity (fake “female account”, fake employee, fake customer).
- Buying aged accounts, proxy evasion, anti-detect browser “fingerprint laundering”.
- “Satire” as a shield for marketing claims (if it’s marketing, disclose it as marketing).

---

## Where the real templates live

- FTC affiliate disclosure template: `09_LEGAL/ftc_compliance/AFFILIATE_DISCLOSURE.md`
- Sponsored content rules: `09_LEGAL/ftc_compliance/SPONSORED_CONTENT_RULES.md`
- AI disclosure guidelines: `09_LEGAL/ftc_compliance/AI_DISCLOSURE.md`
- Testimonials guidelines: `09_LEGAL/ftc_compliance/TESTIMONIAL_GUIDELINES.md`
- Platform guides:
  - `09_LEGAL/platform_compliance/TIKTOK_RULES.md`
  - `09_LEGAL/platform_compliance/INSTAGRAM_RULES.md`
  - `09_LEGAL/platform_compliance/YOUTUBE_RULES.md`
  - `09_LEGAL/platform_compliance/X_TWITTER_RULES.md`

---

## Sources (reference only)

- FTC disclosures for social media (official FTC guidance)
- Platform official policies (TikTok/Meta/YouTube/X)
- Cluely public “Marketing Disclosure” page (pattern reference)

