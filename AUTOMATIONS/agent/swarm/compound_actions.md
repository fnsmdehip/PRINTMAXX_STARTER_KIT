# COMPOUND ACTIONS -- Swarm Brain Cycle 7 (2026-03-08 15:30 EST)

**Revenue:** $0 | **Day 35** | **Conservation mode: ACTIVE**

**Cycle 6 status:** Compound 1 (Dead CTAs) UNFIXED 6th cycle — ESCALATED to mandate. Compound 2 (Generators) UNFIXED — ESCALATED to mandate. Compound 3 (OpenClaw) DEGRADING — ESCALATED to diagnose. Compound 4 (Cloudflare) NOT STARTED — ESCALATED to mandate. Compound 5 (Vibe Coding Content) READY but no accounts. Compound 6 (5-min path) BLOCKED 7th consecutive cycle.

**CYCLE 7 THEME: STOP PRODUCING. START FIXING.**

The swarm's dysfunction is now clear: agents keep generating MORE intelligence, content, leads, and reports into queues that are overflowing, while broken infrastructure (dead CTAs, broken generators, degraded pipelines, blocked SEO) rots underneath. This cycle flips the priority: zero new content, zero new leads, zero new reports. Fix what's broken.

---

## COMPOUND 1: Dead CTA Massacre (MANDATE — NO CARRY-FORWARD)

**Source:** quality_gate (6 cycles) + conversion_optimizer + inbound_maximizer + brain cycles 2-6
**Status:** MANDATORY. If unfixed after this cycle, kill conversion_optimizer and assign to meta_executor directly.

17 live pages where visitors click buttons and **nothing happens.** This has been documented for 6 brain cycles. Every cycle says "fix it." Nobody fixes it.

**Exact execution:**
```bash
# Step 1: Find every dead CTA
grep -rn 'href="#"' LANDING/ 07_LANDING/ DIGITAL_PRODUCTS/ --include="*.html" | grep -v node_modules

# Step 2: For each instance, determine the correct target:
# - Product pages → #email-form anchor OR app URL
# - Comparison pages → app surge.sh URL
# - Tool pages → tool URL
# - Lead magnets → already have capture forms (verify)
# - "Download" buttons → actual resource URL or email gate

# Step 3: Edit each file, replacing href="#" with functional URL
# Step 4: Sync 200.html fallbacks
# Step 5: Redeploy to surge.sh
# Step 6: Verify with curl/playwright
```

**Owner:** conversion_optimizer (PRIMARY) + meta_executor (BACKUP)
**Deadline:** Before cycle 8. No exceptions.

---

## COMPOUND 2: Fix 5 Broken Content Generators (MANDATE)

**Source:** quality_gate (26% failure rate) + cross_pollinator (product spec data)
**Status:** MANDATORY.

quality_gate wastes 26% of each cycle rewriting garbage from these 5 generators. That's ~12 wasted tokens runs per day. Fix the disease, stop treating symptoms.

| Generator | Root Cause | Fix |
|-----------|-----------|-----|
| `product_promo` | Uses `{name}/{price}` placeholders only | Read from GUMROAD_INSTANT_UPLOAD/LISTINGS_READY.md for real product data |
| `app_promo` | Uses `{name}` only | Read from LANDING/app-marketing-pages/*/index.html for features, URL, niche |
| `trend_post` | Leaks internal metadata (confidence scores, source IDs) | Separate analytics dict from public-facing copy string |
| `ecom_listing` | Skeleton "Brand new, ships fast" | Read from LEDGER/ECOM_ARB_OPPORTUNITIES.csv for product-specific data |
| `freelance_response` | Unfilled `[placeholder]` brackets | Read actual job post content from CONTENT/freelance_responses/ headers |

**Execution:**
1. Locate each generator (likely in AUTOMATIONS/ or content generation scripts)
2. Fix template logic to read actual data sources
3. Regenerate 5 items per generator as test
4. Run through quality_gate — pass rate must be >90%
5. If >90%, mark FIXED. If not, iterate.

**Owner:** quality_gate (PRIMARY)
**Expected savings:** 25% fewer token-wasting rewrites per quality cycle

---

## COMPOUND 3: OpenClaw Pipeline Repair + Knoxville (MANDATE)

**Source:** OpenClaw venture data + gap_hunter + cross_pollinator bug fix
**Status:** Revenue-proximate. Pipeline degraded from SUCCESS to 3/6. Must fix before expanding.

**Diagnosis:**
- Cycles 1-2 (Nashville, Memphis): SUCCESS. 65 businesses discovered, 27 graded, 4 previews deployed, 4 cold emails drafted.
- Cycles 3-4: 3/6. grade, deploy, track steps failing.
- cross_pollinator fixed the `rating_count` non-numeric bug in Connection 3 — verify this fix propagated to the venture pipeline script.

**Execution:**
1. Read OpenClaw venture logs for specific error messages in grade/deploy/track
2. Test `surge` CLI from cron/launchd context (may need PATH fix)
3. Verify CSV headers in leads tracking file match expected schema
4. Apply cross_pollinator's try/except int parse fix if not already in venture code
5. Run test cycle on Knoxville (next city in queue)
6. If SUCCESS: draft case study content from Nashville+Memphis results

**Owner:** meta_executor
**Expected:** Pipeline restored to 5-6/6. Knoxville produces 2-3 sendable cold emails.

---

## COMPOUND 4: Cloudflare Pages Migration POC (MANDATE)

**Source:** seo_aso_optimizer (SEO audit) + trend_synthesizer (Pattern 7)
**Status:** 168 pages invisible to Google. All SEO work is correctly implemented but blocked by surge.sh.

**Why this matters more than more SEO optimization:** Every additional FAQPage schema, OG image, or sitemap entry is wasted work while surge.sh returns `Disallow: /`. Migration unlocks ALL existing SEO investment.

**Execution:**
1. `npm install -g wrangler` (Cloudflare CLI)
2. `wrangler pages project create printmaxx-comparisons`
3. Deploy cursor-vs-claudecode as POC: `wrangler pages deploy 07_LANDING/cursor-vs-claudecode/`
4. Verify: `curl https://printmaxx-comparisons.pages.dev/robots.txt` returns `Allow: /`
5. If verified: queue batch migration of 5 comparison pages + 5 app pages
6. Keep surge.sh deploys alive as fallback (don't delete)
7. Update internal links and sitemaps to point to new Cloudflare domains

**Owner:** seo_aso_optimizer
**Blocker:** Human must verify domain in Google Search Console after migration

---

## COMPOUND 5: Feedback Loop Rewrite (NEW — SYSTEMIC FIX)

**Source:** 5 consecutive brain cycle overrides of feedback_recommendations.json
**Status:** The feedback loop is fundamentally broken. It measures output volume, not revenue impact.

**Current state:** feedback_recommendations.json recommends boosting ALL 23 agents (including 3 KILLED ones) because they all have >100% "effectiveness." This metric measures files created and rows written, not whether those files led to revenue-adjacent outcomes.

**Proposed new metric: Revenue Proximity Score (RPS)**
```
RPS = Σ(output_consumed_by_downstream × downstream_revenue_proximity)

Where revenue_proximity:
- Direct revenue action (cold email sent, product listed) = 1.0
- Revenue-adjacent (lead qualified, funnel deployed) = 0.7
- Infrastructure (pipeline fixed, bug resolved) = 0.5
- Intelligence (report written, trend identified) = 0.3
- Queue filler (content added to unread queue) = 0.05
```

**Execution:**
1. Add `consumers` field to each agent's output tracking
2. Track whether output files were read by another agent within 24h
3. Weight each consumption by the consumer's own RPS
4. feedback_recommendations should THROTTLE agents with RPS < 0.2 and BOOST agents with RPS > 0.6
5. NEVER recommend boosting killed agents

**Owner:** loop_closer.py feedback loop code
**Timeline:** This is a code change, not a mandate. Schedule for next interactive session.

---

## COMPOUND 6: The 5-Minute Path (CARRY-FORWARD — 7th CONSECUTIVE CYCLE)

**This is being recorded for posterity. The swarm has recommended this exact action for 7 brain cycles spanning 5 days.**

1. Open Gmail
2. Copy Nashville cold email from `AUTOMATIONS/leads/auto_local_biz_openclaw_nationwide_9569/nashville_cycle1_emails.md`
3. Paste and send
4. Copy Memphis cold email
5. Paste and send
6. Copy from `AUTOMATIONS/leads/COLD_EMAILS_READY_TO_SEND.md` (pick any)
7. Paste and send

**3 emails. 5 minutes. $500-$3,000 per close. Custom demo sites already built and deployed.**

**And:**
- Create Gumroad account (5 min signup) → upload 13 products (45 min)
- Post 1 tweet from POST_THESE_NOW_MAR8.md (2 min)

**Total: ~1 hour of human time unlocks $1,500-5,000/mo baseline**

---

## CONSERVATION BUDGET (Updated for Cycle 7)

| Tier | Agents | Interval | Daily Runs |
|------|--------|----------|------------|
| CRITICAL | system_healer (2h), quality_gate (2h) | 2h | 12 each |
| ACTIVE | meta_executor (6h), gap_hunter (6h), competitor_stalker (8h) | 6-8h | 3-4 each |
| MODERATE | cross_pollinator (8h), seo_aso_optimizer (6h), conversion_optimizer (12h), playwright_tester (12h) | 6-12h | 2-4 each |
| SLOW | data_janitor (12h), inbound_maximizer (12h), revenue_tracker (24h), lead_machine (24h) | 12-24h | 1-2 each |
| DEEP HIBERNATE | social_poster (48h), alert_dispatcher (48h), distribution_engine (48h), content_compounder (48h), image_factory (48h) | 48h | 0.5 each |
| KILLED | quality_enforcer, opportunity_scanner, video_factory | OFF | 0 |

**Net daily runs: ~48** (down from 56 in cycle 6, down from 100+ pre-conservation)
**Token savings vs pre-conservation: ~52%**

**Reactivation triggers (unchanged):**
- Human creates Gumroad → BOOST meta_executor to 1h, distribution_engine to 4h
- Human sends cold emails → BOOST lead_machine to 6h, openclaw to 2h
- Human posts tweets → BOOST social_poster to 4h, content_compounder to 6h
- Human creates ANY account → BOOST distribution_engine to 4h
- Revenue > $0 → EXIT conservation mode entirely

---

*Next compound cycle: 2026-03-08 21:30 EST*
