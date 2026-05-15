# Audit: Landing, Products, Apps, Factory
**Date**: 2026-05-15
**Scope**: 07_LANDING, LANDING, 08_PRODUCTS, PRODUCTS, DIGITAL_PRODUCTS, APPS, factory, builds, lie-detector-app, GUMROAD_INSTANT_UPLOAD, deploy scripts (deploy_apps.py, deploy_all_apps.sh, deploy_surge_quick.sh, ship.sh, Makefile)

---

## Inventory

### Top-level shippable subtrees

| Dir | Purpose | git-tracked files | Canonical? | Notes |
|---|---|---|---|---|
| `LANDING/` | **CANONICAL** production landing pages and surge-deployed sites | 370 | YES | builders-ledger, cnsnt, research-blog, affiliate-pages (61 subdirs), app-marketing-pages (30 subdirs), androx, dosewell, truthscope, cnsnt-downloads, printmaxx-local-demos, privacy, tos |
| `07_LANDING/` | Older / comparison-page layer + the Next.js Remotion video studio (`printmaxx-site`) | 38 | LEGACY + ACTIVE-MIXED | Mostly comparison HTML; `printmaxx-site/` is a Next.js 16 project with Remotion video promos. `before-you-fathers-day` and `before-you-mothers-day` are single-file holiday pages. |
| `PRODUCTS/` | **CANONICAL** digital products + storefront + Gumroad/Whop/Fiverr/Etsy upload kits | 263 | YES | Root has GUMROAD_INSTANT_UPLOAD with 48 entries + 13 PDFs ready, storefront/ with deploy.sh targeting printmaxx-store.surge.sh |
| `DIGITAL_PRODUCTS/` | Earlier parallel products layer | 143 | LEGACY-MIRROR | lead_magnets/ (35 HTML), ready_to_sell/ (37 listings), notion_templates/ (5 systems), listings/ (9 Gumroad ready), micro_products/ |
| `08_PRODUCTS/` | Older 3-product build-guide stubs | 6 | LEGACY | Only `gumroad_copy/` with 3 product copies; rest is uncommitted markdown |
| `GUMROAD_INSTANT_UPLOAD/` | **Empty stub** at root (only `LISTINGS_READY.md`, 1 tracked file) | 1 | DUPE / STUB | Real Gumroad upload kit is `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` |
| `APPS/` | **Empty** — only `specs/` (empty dir) | 0 | EMPTY | Not in git. Real apps live in `lie-detector-app/`, `MONEY_METHODS/APP_FACTORY/builds/`, and `ralph/loops/app_factory/output/` |
| `lie-detector-app/` | **Active** native iOS apps | 75 | YES | TruthScope (released), TruthScope-v2 (refactor) — both Expo/RN with babel, dist/, ios/, src/ |
| `factory/` | **DOES NOT EXIST** | n/a | MISSING | Mentioned in mission; not present |
| `builds/` | **CANONICAL** static-site builds | 641 | YES | 8 subprojects: comparison-pages, focuslock-vs-opal, prayerlock-vs-hallow, programmatic_seo (601-page SEO site), seo-analyzer-web, site-scorer, master_dashboard, portfolio |

### Deploy scripts at root
- `deploy_apps.py` (PWA deployer for 6 ralph/loops/app_factory/output PWAs: ramadan-tracker, focuslock-web, habitforge-web, mealmaxx-web, sleepmaxx-web, walktounlock-web — Vercel → Surge → Netlify fallback chain)
- `deploy_all_apps.sh` (same 6 PWAs, bash version, Vercel-first)
- `deploy_surge_quick.sh` (same 6 PWAs, surge-only, zero-auth path)
- `ship.sh` (wraps `python3 AUTOMATIONS/ship_captain.py --run --swarm --max-parallel 4`)
- `Makefile` (dev/build/lint targets pointing to `LANDING/printmaxx-site` — BROKEN, that path is `07_LANDING/printmaxx-site`; also has `apps`, `validate`, `content`, `status`, `deploy-check`)

---

## Live (deployed, with URL) — per cron + DEPLOYMENT_URLS.md

### Weekly auto-deployed (Sunday 5:00 AM cron, 6 sites)

| Name | URL | Path | Last-deployed |
|---|---|---|---|
| builders-ledger | https://builders-ledger.surge.sh | `LANDING/builders-ledger/` | May 5 (index.html mtime); next auto Sun 5:00 |
| devprint-portfolio | https://devprint-portfolio.surge.sh | `/Users/macbookpro/Documents/devprint/portfolio_site/build` (OUTSIDE project) | next auto Sun 5:02 |
| sovrun-agent-os | https://sovrun-agent-os.surge.sh | `OPEN_SOURCE/agent-soul/site/` | next auto Sun 5:04 |
| eas-preview | https://eas-preview.surge.sh | **BROKEN** — cron entry has no `cd`, so deploys from `$HOME` | next auto Sun 5:06 (likely failing) |
| before-you-ancestry | https://before-you-ancestry.surge.sh | `/Users/macbookpro/Documents/ancestry-research/website/dist` (OUTSIDE project) | next auto Sun 5:08 |
| fnsmdehip-research | https://fnsmdehip-research.surge.sh | `LANDING/research-blog/` | May 5 (index.html mtime); next auto Sun 5:10 |

### Previously deployed (in `OPS/DEPLOYMENT_URLS.md`, last updated May 5)

40+ surge sites listed as LIVE, including:
- App PWAs: ramadan-tracker, focuslock-web, habitforge-web, mealmaxx-web, sleepmaxx-web, walktounlock-web, tasksmash, coreday, deskbreak-web, prayerlock-web
- Standalone tools: coldmaxx, invoiceforge, pagescorer, pitchdeck, pdfmaxx, prospectmaxx, roicalc, stackmaxx, content-calendar, invoice-tracker, website-audit, mcp-marketplace
- Mobile app landing: truthscope, androx-trt, dosewell, pocket-alexandria
- Streak apps (15+): adhd-streak, art-streak-landing, buddhist-streak-landing, beat-making-streak, music-theory-streak, outfit-design-streak, photography-streak, cultural-etiquette-streak, geography-mastery-streak, world-history-streak, all denominational streak apps (catholic, baptist, lutheran, methodist, etc.)

These have no current cron — they were one-shot deploys by `gap-hunter` and cycle scripts. No re-deploy schedule. Cannot verify they're still up without HTTP probe (out of scope read-only).

### Storefront with self-contained deploy script
- `PRODUCTS/storefront/deploy.sh` → printmaxx-store.surge.sh (manual run only, not in cron)

---

## Built but not deployed (no live URL or no cron, ready to ship)

| Path | Type | Status |
|---|---|---|
| `LANDING/cnsnt/` | iOS app landing | HTML built, og.png exists, sitemap May 5 — **NOT in weekly cron** |
| `LANDING/cnsnt-downloads/` | Mac download page | HTML built with cnsnt-mac.dmg artifact, sitemap May 5 — NOT in cron |
| `LANDING/androx/` | TRT clinic site | 6 HTML pages + style.css + CNAME — NOT in cron |
| `LANDING/dosewell/` | dosing/telehealth site | 6 HTML pages + style.css — NOT in cron |
| `LANDING/truthscope/` | app landing | 3 files — NOT in cron |
| `LANDING/printmaxx-local-demos/` | local biz demo index | single page — NOT in cron |
| `LANDING/affiliate-pages/` | **61 affiliate/SEO comparison subdirs**, each with index.html + robots.txt + sitemap.xml | All BUILT, none in cron. Target audience: men 50+ supplements, TRT, GLP1, telehealth, CPAP, hearing aids, cold email tools, AI tools |
| `LANDING/app-marketing-pages/` | **30 app marketing landing pages** including denominational streak apps, focuslock, coldmaxx, mealmaxx, prayerlock, sleepmaxx, walktounlock, hilal, scripture-streak, comparison pages | All BUILT, none in cron |
| `LANDING/affiliate-pages/seo-articles/` | 22 long-form SEO articles + `generate_articles.py` | All built, none deployed |
| `LANDING/privacy/` + `LANDING/tos/` | legal pages | static, no cron |
| `07_LANDING/printmaxx-site/out/` | Next.js export of 7-app store + apps index | Built (`out/index.html`, `out/apps/*`), never wired to deploy |
| `07_LANDING/coldmaxx-vs-instantly/`, `cursor-vs-claudecode/`, `instantly-vs-lemlist/`, `pagescorer-vs-gtmetrix/`, `sleepmaxx-vs-sleepcycle/`, `best-newsletter-platforms/` | 6 comparison pages with 200.html + index.html + robots + sitemap | All BUILT, none in cron |
| `07_LANDING/before-you-fathers-day/`, `before-you-mothers-day/` | single-page holiday lead magnets | BUILT, never deployed |
| `builds/programmatic_seo/` | 601-page programmatic SEO site (12 categories × 50 cities) | BUILT, deployed to printmaxx-seo.surge.sh per `OPS/DEPLOY_LOG.md` Feb 12, **no re-deploy cron** |
| `builds/comparison-pages/`, `focuslock-vs-opal/`, `prayerlock-vs-hallow/` | static comparisons | BUILT, no cron |
| `builds/seo-analyzer-web/`, `site-scorer/`, `master_dashboard/` | static webapps with privacy/terms/cookies/disclosure | BUILT, no cron — `master_dashboard` has `generate_dashboard.py` (regenerator) |
| `builds/portfolio/` | 5 subprojects (chrome-ext, dashboard, discord-bot, landing-page, scraper) | scaffolds, status uncertain |
| `lie-detector-app/TruthScope/dist/` + `TruthScope-v2/dist/` | iOS apps with Expo dist bundles | BUILT, App Store status: APP_STORE_LISTING.md exists, simulator tested per CLAUDE.md |
| `PRODUCTS/storefront/` | central storefront page | HAS deploy.sh → printmaxx-store.surge.sh, NOT in cron |

---

## In-progress

| Path | Evidence |
|---|---|
| `lie-detector-app/TruthScope-v2/` | parallel v2 refactor of TruthScope, both kept, suggesting active iteration |
| `07_LANDING/printmaxx-site/` | progress.txt last updated 2026-01-22 documents BioMaxxPromoV2 Remotion video template; "Next Steps" lists 4 more app promos pending (PrayerLockPromoV2, StepUnlockPromoV2, PelvicProPromoV2, GlowMaxxPromoV2). Site has `out/` with 7 app pages exported. |
| `LANDING/research-blog/` | `build.py` is a generator pointing to `/Users/macbookpro/Documents/research-blog` (OUTSIDE project root — risky); 30+ UAF/PEMF/WiFi-sensing pages built, AUDIT_REPORT.md present. Cron-deployed. |
| `LANDING/builders-ledger/archive/` | weekly archive snapshots (`index_2026-W14.html`, `index_2026-W15.html`) suggest weekly regeneration loop |
| `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` | 22 product slugs (`01_*.md` through `22-*`), PDFs only for 1-13, products 14-22 (Claude Code series, Before You workbook, Reddit Money Machine, Prompt Vault) have markdown only, no PDFs yet |

---

## Abandoned

| Path | Evidence |
|---|---|
| `APPS/` | empty except for empty `specs/`, zero git-tracked files |
| `factory/` | does not exist (despite mission referencing it) |
| `08_PRODUCTS/` | only 3 build-guide markdowns + `gumroad_copy/` (3 files), 6 tracked files total, predates `DIGITAL_PRODUCTS/` and `PRODUCTS/` |
| `GUMROAD_INSTANT_UPLOAD/` (root) | only 1 file (`LISTINGS_READY.md`) — superseded by `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` |
| `DIGITAL_PRODUCTS/` (relative to `PRODUCTS/`) | mostly mirrored / older; `PRODUCTS/` is the active layer though both have content — DEDUP NEEDED |
| `07_LANDING/printmaxx-site/progress.txt` | last touched Jan 22, 2026 — 4 pending video renders never completed |
| `LANDING/affiliate-pages/seo-articles/generate_articles.py` | generator exists but no cron, articles last modified March/April |
| `OPS/STATIC_DEPLOYMENT_URLS.md` | last updated 2026-02-15, only 6 sites listed; superseded by `OPS/DEPLOYMENT_URLS.md` (May 5, 40+ sites) |

---

## 07_LANDING vs LANDING / 08_PRODUCTS vs PRODUCTS — canonical answer

### LANDING is canonical. 07_LANDING is legacy-mixed.
- `LANDING/` has 370 git-tracked files including all production sites (builders-ledger, cnsnt, research-blog, all affiliate pages, app marketing pages, legal pages, downloads).
- All 6 weekly surge cron deploys with paths inside this project reference `LANDING/`, not `07_LANDING/`. 
- `07_LANDING/` has only 38 tracked files — it's a hybrid: the comparison pages (coldmaxx-vs-instantly etc.) are legacy versions duplicated/superseded by `LANDING/app-marketing-pages/coldmaxx/` and `LANDING/affiliate-pages/best-cold-email-tools/`. The exception is `07_LANDING/printmaxx-site/` (the Next.js + Remotion video studio), which is genuinely a different artifact — but its `progress.txt` is stale (Jan 22).
- **Recommendation**: keep `LANDING/` as canonical. Treat `07_LANDING/` as archive except for `printmaxx-site/` which should be moved to `LANDING/printmaxx-site/` (note: Makefile already points there but the path is wrong — needs fix).

### PRODUCTS is canonical. 08_PRODUCTS and root GUMROAD_INSTANT_UPLOAD are stubs. DIGITAL_PRODUCTS overlaps.
- `PRODUCTS/` has 263 tracked files including the active 48-entry `GUMROAD_INSTANT_UPLOAD/` (with 13 PDFs ready, 22 product slugs, listings for Whop/Fiverr/Etsy/KDP/Redbubble), `storefront/`, `gov_contract_samples/`, `community/`, `branding/`, and the master `PRODUCTS_CENTRAL_INDEX.md` (32KB index).
- `DIGITAL_PRODUCTS/` has 143 tracked files with parallel content: `lead_magnets/` (35 HTML files including the calculators, scorecards, quizzes), `ready_to_sell/` (37 listings including Claude Code series 14-17, AEO Starter Kit #24, Before You workbook #18), `notion_templates/` (5 systems), 9 listings — these are mostly NOT duplicated in PRODUCTS/.
- `08_PRODUCTS/` has 6 tracked files (3 build guides + 3 gumroad copies for AI Clarity Stack, Daily Anchor System, Three Hour Physique).
- `GUMROAD_INSTANT_UPLOAD/` at root has 1 file.
- **Recommendation**: `PRODUCTS/` is the primary, but `DIGITAL_PRODUCTS/lead_magnets/` (35 HTML calculators/quizzes) is real distinct work that should be referenced or merged. `08_PRODUCTS/` and root `GUMROAD_INSTANT_UPLOAD/` should be archived. Real sellable digital inventory lives in `PRODUCTS/GUMROAD_INSTANT_UPLOAD/` (22 products, 13 with PDFs).

---

## GUMROAD_INSTANT_UPLOAD readiness (memory says 13, verify)

**Memory is partially correct.** The original 13 products (`01_local_biz_client_system.md` through `13_local_biz_cold_email_pack.md`) all have PDFs in `PRODUCTS/GUMROAD_INSTANT_UPLOAD/pdfs/`. They are READY to upload. `LISTING_METADATA.md` has copy-paste-ready Gumroad form fields for each.

**But there's more — actually 22 products now:**
- Products 1-13 (original): READY. Files + PDFs + listing metadata + bundle definitions ($7 funnel teardown → $97 flagship + 3 bundles).
- Products 14-17: Claude Code series (Agent Bible, For Solopreneurs, For Nontechnical Founders, For Content Creators) — markdown ready, no PDFs.
- Product 18: Before You Family Story Workbook — markdown ready, no PDF.
- Products 19-22: Reddit Money Machine, Claude Code Mastery, Cold Email System, Prompt Vault — markdown ready, no PDFs.
- Also: standalone product subdirs (`ai-automation-kit/`, `cold-email-playbook/`, `lead-machine/`, `pwa-blueprint/`, `financial-dashboard/`) — likely interactive bundles.

**Blocker**: Per memory, P0 revenue blocker is "Gumroad account + list 13 products (30 min)." That's still pending. The system has everything ready for instant upload. 9 additional products (14-22) need PDF conversion via `PRODUCTS/GUMROAD_INSTANT_UPLOAD/convert_to_pdf.sh`.

---

## Top 3 Risks

1. **eas-preview cron is broken** — cron entry 6 (Sun 5:06) has no `cd` directive, so npx surge runs from `$HOME`. It either fails silently or deploys whatever happens to be in `$HOME`. Log path is set, so this is silently logging failures every Sunday since the cron was added. **Action**: fix cron entry to include the actual eas-preview source path (`MONEY_METHODS/EAS/preview/` if it exists, or whichever path holds the EAS marketing site).
2. **research-blog `build.py` writes OUTSIDE project root** to `/Users/macbookpro/Documents/research-blog` — violates Rule 6/guardrails (file ops must stay within PRINTMAXX root). The deploy is from `LANDING/research-blog/` so that part is safe, but a regeneration via `build.py` would touch an external dir. **Action**: change `BASE` in `research-blog/build.py` to `LANDING/research-blog/`. Currently a latent guardrail violation.
3. **40+ surge sites listed LIVE in DEPLOYMENT_URLS.md have no re-deploy cron**. They were one-shot deploys by `gap-hunter` and cycle scripts. Surge.sh sites don't expire, but any content updates require manual redeploy. If any of these get DMCA'd, account suspended, or domain conflicts, there's no automated recovery. Only 6 sites get weekly cron refresh. **Action**: either prune the list to "what we actually want live" or add a weekly cron to re-deploy them all (surge is idempotent — re-deploying the same content is a no-op).

---

## Top 3 Opportunities

1. **Two-line cron change unblocks 80+ landing pages weekly**. `LANDING/affiliate-pages/` (61 subdirs) + `LANDING/app-marketing-pages/` (30 subdirs) + 6 `07_LANDING/*-vs-*/` comparison pages are all BUILT static HTML. A single cron loop (`for dir in LANDING/affiliate-pages/*/; do npx surge "$dir" "$(basename $dir).surge.sh"; done`) would push them all live every Sunday. Current state: built, sitting on disk, never deployed.
2. **PRODUCTS/storefront/ has a deploy.sh that nobody runs**. It targets `printmaxx-store.surge.sh` and is a single-page Gumroad-product showcase. Adding it to the Sun 5:00 cron block adds central buyer landing. Even just a one-shot `bash PRODUCTS/storefront/deploy.sh` would put the storefront live. **Action**: add to cron OR run once from `/goal`.
3. **The 22-product Gumroad lineup is 100% upload-ready for products 1-13** but the human blocker (account creation) hasn't been cleared. Memory says 80-min total to unblock all revenue channels. `/goal` cannot create the account, but it CAN: (a) regenerate fresh PDFs via `convert_to_pdf.sh` to ensure files match latest markdown, (b) verify `LISTING_METADATA.md` matches current pricing, (c) generate cover images for products 14-22 that don't have them yet.

---

## For the `/goal` long-run command

### Should /goal deploy? Build? Just check freshness?

**Recommendation: all three, with explicit phase ordering.**

The system has 6 sites on weekly cron, ~40 sites previously live without cron refresh, and ~100+ sites BUILT-but-never-deployed. Most of the work is already done — the bottleneck is execution, not creation.

`/goal` should:

**Phase 1: Check freshness (cheap, fast)**
- HTTP-probe the 6 cron-deployed sites: returns 200? content matches expected?
- Diff `OPS/DEPLOYMENT_URLS.md` against `crontab -l` — find LIVE sites with no cron refresh.
- Check git diff for changes in `LANDING/` since last `surge_deploy.log` entry — find sites that need redeploy.
- Verify `eas-preview` cron is fixed (currently broken).

**Phase 2: Deploy what exists (idempotent, safe)**
- Run `bash PRODUCTS/storefront/deploy.sh` (central buyer page, not in cron).
- Loop-deploy `LANDING/affiliate-pages/*/` (61 subdirs → 61 surge URLs) — surge is idempotent so this is safe to re-run.
- Loop-deploy `LANDING/app-marketing-pages/*/` (30 subdirs → 30 surge URLs).
- Loop-deploy `07_LANDING/*-vs-*/` and `07_LANDING/before-you-*-day/` comparison/holiday pages.
- Deploy `LANDING/cnsnt/`, `LANDING/cnsnt-downloads/`, `LANDING/androx/`, `LANDING/dosewell/`, `LANDING/truthscope/`, `LANDING/printmaxx-local-demos/`.
- Re-deploy `builds/programmatic_seo/` to printmaxx-seo.surge.sh (last deployed Feb 12, may be stale).
- Re-run `build.py` for `LANDING/research-blog/` if any UAF/PEMF MD content changed (after fixing BASE path).

**Phase 3: Build the gap (token-intensive, scoped)**
- Generate PDFs for Gumroad products 14-22 via `bash PRODUCTS/GUMROAD_INSTANT_UPLOAD/convert_to_pdf.sh`.
- Render the 4 pending Remotion app promos listed in `07_LANDING/printmaxx-site/progress.txt` (PrayerLockPromoV2, StepUnlockPromoV2, PelvicProPromoV2, GlowMaxxPromoV2).
- Regenerate `builds/master_dashboard/index.html` via its `generate_dashboard.py`.
- Regenerate weekly `LANDING/builders-ledger/index.html` if `builders-ledger/archive/` is missing this week's snapshot.

**Phase 4: Surface human blockers (no execution needed)**
- Print exact 80-minute revenue checklist: Gumroad account → upload 13 products → Stripe MCP auth → list TruthScope on App Store.
- Print which cron entries are broken (eas-preview).
- Print which routine cron deploys failed in last `surge_deploy.log`.

### What /goal should NOT do
- Don't deploy `LANDING/research-blog/build.py` until BASE path is fixed (external-dir guardrail violation).
- Don't re-run `deploy_apps.py` / `deploy_all_apps.sh` / `deploy_surge_quick.sh` unless the 6 PWAs in `ralph/loops/app_factory/output/` have actually changed — these scripts target `ralph/loops/app_factory/output` which is outside this audit's scope; defer to audit 05 (app factory).
- Don't touch `APPS/`, `08_PRODUCTS/`, root `GUMROAD_INSTANT_UPLOAD/` — these are legacy stubs.
- Don't iterate the Next.js `07_LANDING/printmaxx-site/` build unless content actually changed (heavy install if `node_modules/` is stale).
- Don't redeploy abandoned sites listed in `OPS/STATIC_DEPLOYMENT_URLS.md` without first probing — some may have content drift the user doesn't want re-published.

### Decision tree summary
- 6 cron sites → /goal just verifies and reports.
- ~100 built-but-undeployed sites → /goal deploys (idempotent, safe).
- 22 Gumroad products → /goal builds missing PDFs/covers; human uploads.
- 1 broken cron (eas-preview) → /goal fixes if path is discoverable, else surfaces as human blocker.
- 40+ historic LIVE URLs → /goal probes; if any 404, decides per-site whether to redeploy or prune.
