# Audit: Legal + Financials + Secrets
**Date**: 2026-05-15
**Scope**: 09_LEGAL/, LEGAL/, FINANCIALS/, SECRETS/, .env

## Inventory

### 09_LEGAL/ (24 template files, total ~225KB)
Five subdirectories. All files dated Jan 20, 2026. All are unfilled templates with `[BRACKET]` placeholders. None signed.

- `contracts/` (5 files): AFFILIATE_AGREEMENT, CLIENT_SERVICE_AGREEMENT, CONTENT_LICENSE, FREELANCER_AGREEMENT, NDA_TEMPLATE
- `email_compliance/` (4 files): B2B_VS_B2C_RULES, CAN_SPAM_CHECKLIST, GDPR_EMAIL_GUIDE, UNSUBSCRIBE_REQUIREMENTS
- `ftc_compliance/` (5 files): AFFILIATE_DISCLOSURE, AI_DISCLOSURE, INCOME_DISCLAIMER, SPONSORED_CONTENT_RULES, TESTIMONIAL_GUIDELINES
- `platform_compliance/` (5 files): GUMROAD_RULES, INSTAGRAM_RULES, TIKTOK_RULES, X_TWITTER_RULES, YOUTUBE_RULES
- `website_policies/` (5 files): COOKIE_POLICY_TEMPLATE, DISCLAIMER_TEMPLATE, PRIVACY_POLICY_TEMPLATE, REFUND_POLICY_TEMPLATE, TERMS_OF_SERVICE_TEMPLATE

### LEGAL/
**EMPTY directory.** Created Feb 2 — never populated. This appears to be the intended "live/signed" location. The duplicate `09_LEGAL/` vs `LEGAL/` is itself a structural smell (two homes for legal docs, only one used and both incomplete).

### MONEY_METHODS/EAS/legal/ (referenced in memory — present)
4 EAS-specific docs (dated Mar 16, ~70KB total): `MSA_TEMPLATE.md`, `SOW_TEMPLATE.md`, `RISK_DISCLOSURE.md`, `SUBCONTRACTOR_AGREEMENT.md`. All are templates with `[CLIENT_NAME]`, `[LLC_NAME]`, `[EAS_ADDRESS]` placeholders. Header on each: "Review with qualified legal counsel before use."

### FINANCIALS/ (9 files, ~43KB)
- `FINANCIAL_DASHBOARD.md` (Apr 2): Pre-Revenue Day 58 at $0. Lifetime expenses ~$524. Says Pipeline Value $5,500-7,000/mo if activated.
- `revenue_pipeline.json` (May 15 — most recent file): days_at_zero_revenue=101, total_revenue=0, 13 PDF products ready / 0 listed, 10 Fiverr gigs ready / 0 listed, 36 cold emails drafted / 0 sent.
- `REVENUE_TRACKER.csv`: only 2 entries, both **paper trades** (PAPER_TRADE_001/002), not real revenue.
- `EXPENSE_TRACKER.csv`: 3 entries — Apple Dev $99, Google Play $25, Python deps $0. Missing Claude Max ~$200/mo recurring.
- `INVESTMENT_PORTFOLIO.csv`: header only, **zero rows**.
- `TAX_DEDUCTIONS_2026.csv`: 2 entries — Apple/Google fees only.
- `MASTER_FINANCIAL_TRACKER.csv`, `P_AND_L_MONTHLY.csv`, `SWARM_PROJECTIONS_SUMMARY.csv`: exist but heavily projection-based.

### SECRETS/ (4 files)
- `CREDENTIALS.env` (11KB, 196 keys): the master credential vault
- `HOW_TO_FILL_CREDENTIALS.md` (5.5KB): instructions for where to obtain each key
- `created_accounts.json` (1.9KB): browser-automation account creation attempt log (most FAILED or CAPTCHA_BLOCKED)
- `PAYMENT_INFO.md` (2KB): personal-info template — ALL fields empty except PRIMARY_EMAIL

### .env (root, 1.2KB)
Tiny file — only 10 active key=value lines. The real credential mass lives in `SECRETS/CREDENTIALS.env`, not the root `.env`.

---

## .env key names (NAMES ONLY) — root `.env`

| Key | Seems set? |
|-----|-----------|
| GEMINI_API_KEY | y |
| N8N_API_KEY | y |
| STRIPE_SECRET_KEY | y |
| STRIPE_PUBLISHABLE_KEY | y |
| REVENUECAT_API_KEY | y |
| REVENUECAT_SECRET | y |
| ADMOB_APP_ID | y |
| ADMOB_BANNER_AD_UNIT | n (placeholder/empty) |
| ADMOB_INTERSTITIAL_AD_UNIT | n (placeholder/empty) |
| ADMOB_REWARDED_AD_UNIT | n (placeholder/empty) |

## SECRETS/CREDENTIALS.env summary (NAMES ONLY)
**196 total keys. 184 EMPTY (no value after `=`). 12 set with values.**

The 12 set keys are roughly: Stripe live key, RevenueCat keys, AdMob app ID, GoLogin plan, Cold-email domain registrar, Apple bits, and a few platform tokens (Buffer, Resend pattern). Everything platform-specific (Twitter for 13 accounts, Instagram for 9, TikTok for 9, YouTube for 7) and the entire ANTI-DETECT/PROXY stack (SOAX, GoLogin) is EMPTY.

Notable EMPTY keys for revenue-critical blockers from memory:
- `GUMROAD_EMAIL`, `GUMROAD_PASSWORD`, `GUMROAD_ACCESS_TOKEN` — EMPTY
- `STRIPE_EMAIL`, `STRIPE_PASSWORD`, `STRIPE_API_KEY_TEST` — EMPTY (only LIVE key set)
- `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ZONE_ID` — EMPTY
- `GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD` — EMPTY
- `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` — EMPTY (rules require `--api-key` flag when ANTHROPIC_API_KEY is set; if it isn't, Rule 18 OAuth fallback is the actual auth path)
- `TWITTER_PRINTMAXXER_*` (the primary account) — EMPTY

---

## Legal docs status (signed vs draft vs missing)

| Doc | Location | Status |
|-----|----------|--------|
| Affiliate Agreement | 09_LEGAL/contracts/ | TEMPLATE (unsigned, has `[BRACKETS]`) |
| Client Service Agreement | 09_LEGAL/contracts/ | TEMPLATE |
| Content License | 09_LEGAL/contracts/ | TEMPLATE |
| Freelancer Agreement | 09_LEGAL/contracts/ | TEMPLATE |
| NDA | 09_LEGAL/contracts/ | TEMPLATE |
| EAS MSA | MONEY_METHODS/EAS/legal/ | TEMPLATE — needs `[LLC_NAME]`, `[EAS_ADDRESS]` filled |
| EAS SOW | MONEY_METHODS/EAS/legal/ | TEMPLATE |
| EAS Risk Disclosure | MONEY_METHODS/EAS/legal/ | TEMPLATE |
| EAS Subcontractor Agreement | MONEY_METHODS/EAS/legal/ | TEMPLATE |
| Privacy Policy | 09_LEGAL/website_policies/ | TEMPLATE — not published to any of 202 surge sites |
| Terms of Service | 09_LEGAL/website_policies/ | TEMPLATE |
| Cookie Policy | 09_LEGAL/website_policies/ | TEMPLATE |
| Refund Policy | 09_LEGAL/website_policies/ | TEMPLATE |
| Disclaimer | 09_LEGAL/website_policies/ | TEMPLATE |
| FTC Affiliate Disclosure | 09_LEGAL/ftc_compliance/ | TEMPLATE — not embedded in 5 affiliate pages |
| AI Disclosure | 09_LEGAL/ftc_compliance/ | TEMPLATE |
| Income Disclaimer | 09_LEGAL/ftc_compliance/ | TEMPLATE |
| CAN-SPAM Checklist | 09_LEGAL/email_compliance/ | REFERENCE GUIDE (not actionable doc) |
| GDPR Email Guide | 09_LEGAL/email_compliance/ | REFERENCE GUIDE |
| LLC formation docs | NONE FOUND | **MISSING** |
| Tax filings (Schedule C, 1099s, EIN letter) | NONE FOUND | **MISSING** |
| Business bank account docs | NONE FOUND | **MISSING** |
| Operating Agreement | NONE FOUND | **MISSING** |
| Signed engagement contracts | NONE FOUND | **N/A — no clients yet** |

The memory says "DBA under existing Wyoming LLC" for EAS but no LLC formation paperwork is on disk in any of these locations.

---

## Financial records (high level)

- **Revenue:** $0 lifetime. The only `REVENUE_TRACKER.csv` rows are 2 paper-trade simulations from Feb 4. The system has been at $0 for 101+ days per `revenue_pipeline.json`.
- **Expenses:** Tracker only logs $124 (Apple + Google dev fees). Dashboard mentions Claude Max ~$200/mo but it's not in the CSV — actual spend likely $600-800+ over 5 months.
- **Banking:** No bank statement, account number, reconciliation, or accounting software output anywhere.
- **Taxes:** `TAX_DEDUCTIONS_2026.csv` has 2 rows. No quarterly estimates filed (visible). No EIN reference. No 1099 receipts.
- **Investments:** `INVESTMENT_PORTFOLIO.csv` is empty (header only).
- **Accounting state:** Manual CSVs. No QuickBooks, Wave, Xero, or Bench integration. No bookkeeper. No reconciliation cadence.

---

## Secrets inventory (file types only)

| File | Type | Status |
|------|------|--------|
| `SECRETS/CREDENTIALS.env` | .env (196 keys) | 12/196 filled = 6% complete |
| `SECRETS/HOW_TO_FILL_CREDENTIALS.md` | docs | Complete reference |
| `SECRETS/created_accounts.json` | json log | Mostly FAILED/CAPTCHA_BLOCKED rows from Feb 12 — stale |
| `SECRETS/PAYMENT_INFO.md` | template | All fields empty |
| `.env` (root) | .env (10 keys) | 7/10 set, 3 placeholder |
| LLC docs / EIN letter / W-9 | — | **NOT PRESENT** |
| SSH/PGP keys, .pem, .p12 | — | **NOT PRESENT** in this tree |
| Apple App Store Connect .p8 key | — | **NOT PRESENT** (path referenced in PAYMENT_INFO but file absent) |

The `created_accounts.json` log is also a soft secret leak — it contains actual plaintext passwords for FAILED/CAPTCHA_BLOCKED attempts (e.g., Gumroad, Buffer). That file should not exist in this form.

---

## Gaps / Missing items

1. **No LLC paperwork on disk.** Memory says Wyoming LLC + EAS DBA. No Articles of Organization, no Operating Agreement, no EIN letter, no registered-agent confirmation.
2. **No client-signed contracts.** EAS is a 4-package productized service ($1,500 - $4,500), but no signed MSA, no SOW, no Risk Disclosure has client signatures.
3. **No published legal pages.** 202 live surge.sh sites, but none link to a real Privacy Policy/Terms/Disclaimer. FTC affiliate disclosure NOT embedded in the 5 supplement affiliate pages (memory flags this explicitly).
4. **Stripe live key set, but no business setup audit.** No reconciliation file. No record of payouts/refunds. No 1099-K tracking.
5. **LEGAL/ directory empty.** Either delete it or move signed/active docs into it. Pick one home (`09_LEGAL/` for templates, `LEGAL/` for executed) and use it.
6. **No tax artifacts** for ANY tax year — no Schedule C draft, no quarterly estimated payment record, no mileage log.
7. **CREDENTIALS.env is 94% empty** — 184/196 keys unfilled. Revenue blockers (Gumroad, Cloudflare, Gmail App Pwd, Stripe email/test key) all empty.
8. **`created_accounts.json` contains plaintext passwords** for failed signup attempts. Should be deleted or rotated.
9. **No `.gitignore` verification** for `.env` and `SECRETS/` shown in this audit — assumed safe per Rule 15 of CLAUDE.md, but worth a one-line check.
10. **No DPA (Data Processing Agreement) template** despite collecting emails on multiple sites. GDPR exposure.
11. **No audit trail** for who/what touches Stripe keys, RevenueCat keys (Rule 23 — VERIFY REAL).

---

## Top 3 Risks

1. **Compliance — FTC + Apple Review violation risk.** Memory states 5 supplement affiliate pages live with `REPLACE_CB_ID` / `REPLACE_AMZN_TAG` placeholders AND no affiliate disclosure embedded. The moment those IDs get filled and a sale happens, the site is operating an undisclosed affiliate relationship — FTC `16 CFR Part 255` violation. Apps about to submit to App Store also need a working privacy policy URL (Rule 24 mentions this) — the URL points nowhere currently.
2. **Secret-exposure — plaintext passwords in `created_accounts.json` + 94% empty credentials vault.** The JSON file logs raw passwords from failed/blocked account creation attempts (Gumroad, Buffer). If those passwords were reused or weren't single-use, they're now sitting unencrypted on disk in a known-path JSON. Combined with the fact that the vault is mostly EMPTY, anyone with disk access doesn't even gain much — but anyone with disk access who finds reused credentials definitely does.
3. **Operational/Legal — LLC + tax invisibility.** Memory claims a Wyoming LLC and an EAS DBA, but ZERO supporting documents are on disk. If the IRS, a client, or a counterparty asks for a W-9 or Certificate of Good Standing, there is nothing to send. EAS is selling $1,500-$4,500 packages under an entity whose paperwork lives outside this project — risk if the user is gone or the system is being audited by anyone.

---

## Top 3 Opportunities

1. **One-script template-instantiation:** All 24 legal templates and 4 EAS docs use the same `[BRACKET]` placeholder pattern. A 50-line Python script driven by a single `OPS/LEGAL_ENTITY_PROFILE.json` (LLC_NAME, EAS_ADDRESS, OWNER_NAME, EIN, etc.) could materialize fully-filled versions of all 28 docs in `LEGAL/` in seconds. Removes the "still a template" excuse forever.
2. **Auto-embed FTC disclosure + Privacy Policy on all 202 surge sites.** A single deploy-time post-processor (or a single `_include` snippet) could fix the most acute compliance risk in a few hours. This is also the gating dependency for shipping any affiliate page that earns money — a 1-hour fix unlocks the 5 supplement pages.
3. **Consolidate to one secrets store.** The `.env` at root (10 keys) and `SECRETS/CREDENTIALS.env` (196 keys) duplicate intent. Move everything into one canonical file, source it once, delete the other, delete `created_accounts.json`, and rotate any passwords that ever appeared there. Cuts the credential surface area from 2 files to 1, eliminates plaintext-password log file, and makes the "is X credential present?" check a single grep.

---

## For the /goal long-run command

**Should /goal touch this area at all? No, but it MUST treat it as a precondition checker.**

`/goal` is for long-run autonomous execution. Legal/financial/secrets are the **gating layer**, not part of the loop. Specifically:

- `/goal` should NOT modify legal templates, financial CSVs, or any file under `SECRETS/`.
- `/goal` MUST run a one-shot **secret-completeness precondition check** at startup and again before any revenue-action phase. Recommended preconditions to gate by goal type:
  - Goal involves Gumroad upload? → require `GUMROAD_ACCESS_TOKEN` set. If empty, mark goal `human_blocked` and exit (per Rule 17 anti-entropy and the `venture_autonomy.py` `human_blocked` pattern).
  - Goal involves Stripe? → require `STRIPE_SECRET_KEY` set AND a published privacy policy URL exists. If either missing, `human_blocked`.
  - Goal involves Twitter posting from `@PRINTMAXXER`? → require `TWITTER_PRINTMAXXER_*` keys set OR confirmed Publer/Typefully token. Currently all empty.
  - Goal involves affiliate revenue activation? → require FTC disclosure HTML snippet present on target page (grep check). Currently missing across all 5 supplement pages.
  - Goal involves App Store submission? → require Privacy Policy URL resolves (HTTP 200) and `APP_STORE_CONNECT_API_KEY_PATH` references an existing file (currently doesn't).
- `/goal` should surface these preconditions to the user in plain English at top of run: "BLOCKED: missing 4 credentials, 1 missing legal doc. Fix here, then re-run." Match the existing pattern from `OPS/ACTIONABLE_QUEUE.md` and the human-blocker list in CEO agent.
- `/goal` should never PRINT credential values — only existence checks. The precondition checker can return a boolean + a "missing keys" name list, never the values. This is consistent with this audit's constraint and Rule 22 (zero fakes — don't pretend a goal is unblocked when a key is empty).

In short: `/goal` reads from this area, never writes. The audit's mission gap (94% empty credentials, 100% template-state legal docs, $0 revenue, no LLC paperwork) IS the blocker pile that `/goal` should refuse to run past silently.
