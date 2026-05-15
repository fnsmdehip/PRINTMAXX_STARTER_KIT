# Audit: Content + Media + Email
**Date**: 2026-05-15
**Scope**: 04_CONTENT/, CONTENT/, MEDIA/, EMAIL/, clips/

---

## Inventory

### Top-level directories
- `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/CONTENT/` — **AUTHORITATIVE.** Last touched Apr 6 2026. 38 entries at top level, ~99 subdirs under `social/`. Active write target for every scraper/generator/poster.
- `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/04_CONTENT/` — **LEGACY ARCHIVE.** Last touched Feb 19 2026. Never updated since. Numbered-prefix sibling of `CONTENT/` from an earlier filing scheme.
- `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MEDIA/` — image + video pipeline. ~340 PNGs in `generated_images/`, Playwright HTML templates in `image_templates/`, Remotion video project in `remotion/`. Active: April write timestamps on subdirs.
- `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/EMAIL/` — sequences, outreach templates, compliance footer. Most recent activity Apr 6 (`influencer_outreach/`, `telehealth_sequences/`). 15 entries.
- `/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/clips/` — empty. `clips_metadata.csv` is header-only (zero rows). `clips/`, `downloads/`, `metadata/`, `transcripts/` are all empty.

### CONTENT/ key surfaces
- `CONTENT/social/posting_queue/` — **1,638 files.** This is the central queue. 302 `twitter_PRINTMAXXER_*` files, plus engagement_bait, viral_repurpose, deployment_announcement, reddit/HN/linkedin variants.
- `CONTENT/social/CONTENT_QUEUE.csv` — 1,130 lines. Source pool, not approved.
- `CONTENT/social/auto_generated/` — 119 files. Daily `auto_content_YYYYMMDD_HHMMSS.csv` + `alpha_content_YYYY_MM_DD.md` outputs.
- `CONTENT/social/distribution/` — 237 files. Per-cycle multi-platform distribution maps.
- `CONTENT/social/deployment_announcements/` — 44 files. Most recent `2026-05-05_deployment_content.md`.
- `CONTENT/freelance_responses/` — 202 files. Each saved per-day per-job (responses regenerate daily — the same job ID has files dated Mar 5, 6, 7, …, May 15).
- `CONTENT/ecom_listings/` — 40 files. Same pattern (per-product per-day regeneration).
- `CONTENT/social/post_log.json` — central manifest. 173 queued, 0 posted, coverage to Apr 21. Pipeline bug flags called out (BUFFER_UPLOAD_MAR7 token parsing, reddit scraper schema mismatch).
- `CONTENT/social/post_schedule.json` — 1,295 lines. Schedule entries with warmup-phase override fields.

### MEDIA/ key surfaces
- `MEDIA/generated_images/` — ~340 PNGs (alpha cards, app promos, video thumbnails, twitter banner + PFP). Newest Mar 9 2026.
- `MEDIA/image_factory_batch.py`, `MEDIA/batch_image_generator.py`, `MEDIA/generate_batch_mar7.py`, `MEDIA/generate_batch_mar8.py` — Playwright HTML-to-PNG pipeline scripts.
- `MEDIA/image_templates/` — 13 HTML templates including `twitter_banner.html`, `twitter_pfp.html`, `og_image.html`, `thread_card.html`, `product_cover.html`, `niche_card.html`, `stat_highlight.html`, `comparison_og.html`.
- `MEDIA/remotion/` — React-based video factory with `render.py`, `catalog.json`, npm-installed.
- `MEDIA/og_temp/` — temp staging.

### EMAIL/ key surfaces
- `EMAIL/sequences/` — 4 generic sequences (welcome, launch, reengagement, local_biz_followup). All edited Mar 8.
- `EMAIL/triggering_events/` — 6 trigger-driven email templates (competitor_layoff, glassdoor_spike, job_removed, leadership_change, office_move, sec_filing_change). Fed by SEC EDGAR / Crunchbase scanners.
- `EMAIL/telehealth_sequences/` — 3 nurture sequences (glp1, peptide, trt) — 7-day each.
- `EMAIL/influencer_outreach/` — playbook + templates.
- `EMAIL/ecom_outreach/` — growth offer + tech stack templates.
- `EMAIL/COMPLIANCE_FOOTER.md` — CAN-SPAM / FTC boilerplate.

### 04_CONTENT/ legacy content
Read-only at this point. Holds:
- `04_CONTENT/longtail_pages/` — 142 SEO-driven markdown pages (jan 21 stamps).
- `04_CONTENT/truth_pages/` — 13 playbooks.
- `04_CONTENT/email_sequences/` — 24 sequences in older format (cold_*, launch_*, nurture_*, welcome_*).
- `04_CONTENT/email_templates/` — 12 HTML templates (welcome, nurture, launch, trial_expiring, winback, transactional, receipt).
- `04_CONTENT/social/{ai,faith,fitness,digital_minimalism}/` — pre-built niche content (129 + 119 + 119 + 10 files).
- `04_CONTENT/medium_articles/`, `substack_posts/`, `meme_library/`, `video_scripts/`, `threads/` — all populated Jan-Feb only.

---

## Live / Operational (what's auto-generating, what's publishing)

### Auto-generating (writes new files on cron)
- **Twitter alpha scraper** (6 AM) — feeds `LEDGER/ALPHA_STAGING.csv` → routes via `alpha_auto_processor` → drops into `CONTENT/social/auto_generated/`.
- **Reddit scraper** (6:15 AM) — same path, also lands `CONTENT/social/auto_generated/auto_content_YYYYMMDD_*.csv` daily.
- **Image factory** (`MEDIA/image_factory_batch.py`, `batch_image_generator.py`) — Playwright HTML→PNG. Last batch Mar 9 (`vid_thumb_*.png`, `app_promo_*.png`).
- **Daily engagement planner** (cron 7 AM) — writes `CONTENT/social/posting_queue/ENGAGEMENT_PLAN_YYYY-MM-DD.md`. Only one such file exists: `ENGAGEMENT_PLAN_2026-03-08.md` (warmup-aware, no posts allowed). **PLAN GENERATION HAS NOT RUN SINCE MAR 8.**
- **Daily digest** (cron 6:45 AM) — surfaces yesterday's activity.
- **Freelance scraper** — regenerates `CONTENT/freelance_responses/response_*.md` daily. Most recent May 15 (today). This loop IS running.
- **Ecom listing generator** — regenerates `CONTENT/ecom_listings/listing_*_YYYYMMDD.md` daily (last Mar 9).
- **Engagement_bait_converter / content_repurposer / content_multiplier / content_trend_pipeline / app_viral_content_engine / claude_code_market_intel_poster / clip_post_scheduler** — all referenced as live converters routing alpha into posts.
- **Twitter warmup poster** (`AUTOMATIONS/twitter_warmup_poster.py`) — reads from `CONTENT/social/APPROVED_POSTS_*.csv`, gated by `AUTOMATIONS/agent/twitter_warmup_state.json`.

### Publishing (writes go where)
- **NOTHING IS POSTING TO TWITTER.** `post_log.json` shows `"total_posted": 0` and every entry has `"posted_at": null`. `post_schedule.json` documents `"api_status": {"twitter": "no_api_keys", "linkedin": "no_api_keys", "reddit": "no_api_keys"}` and `"posting_method": "manual_buffer"`. No `POSTED_LOG.csv` exists on disk.
- **Buffer uploads were attempted** — `BUFFER_UPLOAD_MAR14.csv`, `BUFFER_UPLOAD_MAR7.csv`, `BUFFER_UPLOAD_MAR5.csv` exist but `BUFFER_UPLOAD_MAR7.csv` is flagged `DO_NOT_POST` (token parsing bug — tool names got truncated to "No", "mCP").
- **All posting is manual.** Human is expected to copy/paste from `posting_queue/` into Buffer or directly into X.
- **Freelance scraper outputs to local md only** — no DM-sender script wired. The user is expected to read and reply manually.

### Live loops verified
- Freelance response loop: timestamp on `response_*_20260515.md` files = today.
- Auto_generated CSVs: stopped at `auto_content_20260318_055055.csv`. **Pipeline has been dead for ~2 months on that surface.**
- Distribution cycles: stopped at cycle 47 dated `20260505_*`. Loop went silent ~10 days ago.

---

## 04_CONTENT vs CONTENT — which is canonical?

**`CONTENT/` is canonical and active.** `04_CONTENT/` is a frozen legacy snapshot.

Evidence:
- `CONTENT/` mod time: Apr 6 2026. `04_CONTENT/` mod time: Feb 19 2026.
- `CONTENT/social/` referenced explicitly in `.claude/rules/file-locations.md`, `auto-integration.md`, `app-factory-pipeline.md`, `agent-infrastructure.md`, `commands-reference.md`, and project memory (`MEMORY.md`).
- Every active automation script writes to `CONTENT/...` paths — `posting_queue/`, `auto_generated/`, `distribution/`, `freelance_responses/`, `ecom_listings/`.
- `04_CONTENT/` has zero writes since Feb 19. All files Jan/Feb-stamped.
- The only "newer" thing under `04_CONTENT/` per `find -newer` is `.DS_Store` and some files matching by inode/mtime quirks, not actual content edits.

**04_CONTENT/ still contains useful frozen assets** that the active system doesn't seem to know about (the rules don't index it):
- 142 longtail SEO pages
- 13 truth/playbook pages
- 24 mature email sequences (more variety than `EMAIL/sequences/`)
- 129+119+119 niche-content posts (ai, faith, fitness)

**Recommendation: treat `04_CONTENT/` as a read-only library to mine, not a parallel queue.** Wire its assets into the manifest if reused. Do not let agents write there.

---

## Queue state

### Twitter (@PRINTMAXXER)
- **Warmup state**: `AUTOMATIONS/agent/twitter_warmup_state.json` says **Day 22, phase FULL_OPS**, phase_override active (reason: "RESTRUCTURE_V2 T019/T022 — distribution active > all architecture improvements", set 2026-03-13).
- **Project memory still says Day 2 LURK** — memory is stale. The actual code-tracked phase is FULL_OPS.
- **last_post_date in warmup state**: 2026-03-13. **total_posted: 0.** So the warmup state has advanced the calendar but never recorded a successful post.
- **post_schedule.json `warmup_override`** disagrees with the state file — it says `"current_phase": "LURK", "current_day": 2`. That object was last edited 2026-03-08 and is stale; the canonical state is the JSON in `AUTOMATIONS/agent/`.
- **Queue depth**: 302 `twitter_PRINTMAXXER_*` queue files; 173 entries scheduled in `post_log.json` (161 twitter, 3 linkedin, 0 reddit); 0 posted.
- **Coverage**: schedule entries run Mar 7 → Apr 21 2026. After Apr 21, no scheduled slots until ad-hoc files dated May 5 reappear in the queue.
- **Newest queue entries** (mtime): `linkedin_overengineering_professional_20260505.md`, `reply_bait_ai_agents_amplify_patterns_20260505.md`, `inbound_tweets_20260505.md`, `QUEUE_20260505.csv` (May 5 — 10 days ago).
- **QUEUE_20260505.csv** has 13 rows scheduled May 6–12, status `READY`. No status flip to POSTED on any.
- Next scheduled tweet according to post_log.json that has a date past today: the file is silent past Apr 21 — system has not regenerated forward schedule since Mar 8.

### LinkedIn
- 4 queued (`linkedin_PRINTMAXXER_mar12_0900.txt`, `mar12_1400`, `mar13_0900`, `apr21_0900`). Plus the May 5 batch. None posted.

### Reddit / HN
- ~50+ `reddit_*` and `hn_*` posts in `posting_queue/` and `distribution/`. Some flagged as PENDING_REVIEW.

### Email
- Sequences exist (`welcome_sequence.md`, `launch_sequence.md`, `reengagement_sequence.md`, `local_biz_followup_sequence.md`). 7-day nurture sequences for telehealth (glp1, peptide, trt). NO ESP wired. `post_schedule.json` notes `Beehiiv/ConvertKit account needed to send`.
- **Triggering-events templates are armed** for SEC EDGAR / Crunchbase scanners but no outbound email API is wired.

### Video
- `clips/` is empty (zero rows in `clips_metadata.csv`).
- `CONTENT/social/TIKTOK_LAUNCH_SCRIPTS.md` and `TIKTOK_VIRAL_STRATEGY_2026.md` exist (5 scripts ready).
- Remotion factory present in `MEDIA/remotion/` but `out/` was not inspected — no evidence of rendered videos in flight.
- No TikTok account exists per project memory (revenue blocker P1).

---

## Dead / Orphan / Abandoned

1. **`clips/`** — entire subtree is empty. The pipeline never wired the YouTube-to-clip transcription path. Either kill the dir or wire ClipVault/yt-dlp + ffmpeg.
2. **`04_CONTENT/`** — frozen legacy. 142 longtail pages, 24 email sequences, 13 truth playbooks orphaned because no current automation reads from there. The Resource Manifest doesn't index it.
3. **`BUFFER_UPLOAD_MAR7.csv`** — flagged `DO_NOT_POST` due to tweet_drafter token parsing bug. Bug never fixed.
4. **`CONTENT/social/auto_generated/`** — last file `auto_content_20260318_055055.csv`. The daily auto-content loop went silent ~2 months ago. The scraper still runs but its content-emission step is dead.
5. **`alpha_review_mar7_tweet1-5.txt`** — listed in `post_log.json` as `pending_review_not_queued`. Stuck for 2+ months.
6. **`ENGAGEMENT_PLAN_*.md`** — only one was ever generated (Mar 8). Cron 7 AM either isn't firing or isn't writing.
7. **All `compound_engagement_bait_*.txt`, `engagement_bait_2026030*.txt`** — generated but never posted, never converted, never re-purposed.
8. **`MEDIA/generated_images/`** — image generation stopped Mar 9. No images for Mar-May content cycles. Visual asset pipeline is dead.
9. **Distribution cycles 1-47** — sit in `CONTENT/social/distribution/` as plan docs. There's no consumer that reads them and posts.
10. **CONTENT_QUEUE.csv (1,130 rows)** — flagged `PENDING_REVIEW` and `source pool, not approved`. Never made it to posting.
11. **`POSTED_LOG.csv`** — referenced in code but doesn't exist on disk. The "manual_buffer" posting method never had a feedback loop to mark anything posted.
12. **Freelance responses** — regenerate daily on the same set of jobs, but no DM/email sender consumes them. They're orphan reports.

---

## Top 3 Risks

1. **Generation outpaces distribution by 1000x and there is no posting path wired.** 302 queue files for one Twitter account, 0 ever posted, no API keys, no Buffer integration that works (token bug), no human review loop. The factory is producing content into a black hole. This is the single biggest dollar leak in the project — every cron tick adds to a pile that goes nowhere.
2. **Warmup state file is split-brain with project memory and post_schedule.json.** State file says FULL_OPS Day 22 (Mar 13 override). `post_schedule.json.warmup_override` says LURK Day 2. Project memory says LURK Day 2. If `/goal` reads the wrong source it will either over-post (triggering account suspension) or under-post (continuing the 2-month silence). The phase_override note ("distribution active > all architecture improvements") implies someone intended to override but never connected a poster to it.
3. **Auto-gen pipeline silently died around Mar 18–20.** `auto_generated/` last write Mar 18. `MEDIA/generated_images/` last write Mar 9. `posting_queue` newest scheduled date is Apr 21. The system kept *some* loops alive (freelance scraper through May 15) but most of the content scaffolding has been dead for two months without alerting. The user thinks they have an active system; they have a partial corpse.

---

## Top 3 Opportunities

1. **Wire the existing 302 PRINTMAXXER queue files into Twitter API or a working Buffer push.** Content is approved, voice-checked, dated, even paired with images. Unblocking distribution is one credential and a 50-line poster script. This converts the entire backlog from sunk cost to immediate output.
2. **Resurface `04_CONTENT/` assets into the live system.** 142 longtail SEO pages + 13 playbook truth pages + 129 ai-niche posts already exist and aren't being mined. Run them through `engagement_bait_converter` and `content_repurposer` to multiply current output without generating new ground-truth.
3. **Standardize the queue schema and add a `POSTED_LOG.csv` writer.** Today's queue is JSON + CSV + free-form .txt + .md across `posting_queue/`, `distribution/`, `auto_generated/`, `deployment_announcements/`. One schema (date, platform, account, file, status, posted_at) writable to a single CSV means `/goal` can both pull next post AND mark it posted. Closes the feedback loop the warmup poster expects.

---

## For the /goal long-run command

### Should /goal generate content? Post content? Just stage?

**`/goal` should NOT generate net-new content by default.** The backlog is already 200+ posts deep on the @PRINTMAXXER queue alone, plus the entire `04_CONTENT/` library and the multi-platform `distribution/` cycles. Generation is not the bottleneck — distribution is.

**`/goal` should:**
1. **Reconcile warmup state first.** Read `AUTOMATIONS/agent/twitter_warmup_state.json` as source of truth. Update `post_schedule.json.warmup_override` and project memory to match. Phase = FULL_OPS Day 22+.
2. **Stage the next post.** Pull next-scheduled file from `CONTENT/social/posting_queue/twitter_PRINTMAXXER_*.txt` based on `post_log.json` + `post_schedule.json`, surface the actual text + image path to the user.
3. **Post if creds available, else surface as human-blocker.** If `TWITTER_API_KEY` is in env, post via `twitter_warmup_poster.py`. If not, drop the post body into clipboard / a "post this now" surface and require the human to confirm.
4. **Write back posted_at.** Update `post_log.json` and (create) `POSTED_LOG.csv` once posted. Close the loop the warmup poster expects.
5. **Generate content only when queue runs dry past 3 days out.** Trigger `engagement_bait_converter` / `content_repurposer` / `content_multiplier` only when forward coverage drops below 3 days. Otherwise, drain the existing pile.
6. **Resurrect dead loops.** Run `daily_engagement_planner.py` if no `ENGAGEMENT_PLAN_$(today).md` exists. Run the image factory if any queued tweet references an image path that doesn't exist on disk.

### Which generators/posters to invoke

**Posters (canonical):**
- `AUTOMATIONS/twitter_warmup_poster.py --post` — reads queue, gated by warmup state, posts to X. (Needs API key.)
- `AUTOMATIONS/auto_content_poster.py` — found in AUTOMATIONS, check before using.
- `AUTOMATIONS/clip_post_scheduler.py` — for video clips when those resurrect.

**Generators (drain mode, only when queue thin):**
- `AUTOMATIONS/engagement_bait_converter.py` — single-shot EB → 3+ posts.
- `AUTOMATIONS/content_repurposer.py` — cross-platform multiplier.
- `AUTOMATIONS/content_multiplier.py` — bulk gen.
- `AUTOMATIONS/content_trend_pipeline.py` — trend-aware.
- `AUTOMATIONS/app_viral_content_engine.py` — app-promo content.
- `AUTOMATIONS/claude_code_market_intel_poster.py` — Claude Code niche.

**Image factory:**
- `MEDIA/image_factory_batch.py` — Playwright HTML→PNG. Templates in `MEDIA/image_templates/`. Cron this back to life.

**Email (currently inert, no ESP):**
- `EMAIL/sequences/welcome_sequence.md`, `launch_sequence.md`, `reengagement_sequence.md`, `local_biz_followup_sequence.md` — ready to send the moment Beehiiv/ConvertKit are wired.
- `EMAIL/triggering_events/*` — wire to SEC EDGAR / Crunchbase scanners only after ESP is live.

**Plans/Schedules `/goal` must read every run:**
- `AUTOMATIONS/agent/twitter_warmup_state.json` — phase/day source of truth
- `CONTENT/social/post_log.json` — entry-level ledger
- `CONTENT/social/post_schedule.json` — per-account schedule (treat `warmup_override` block as stale)
- `CONTENT/social/posting_queue/QUEUE_20260505.csv` — most recent attempt at a unified schedule

**Plans/Schedules `/goal` must write every run:**
- `CONTENT/social/post_log.json` — flip `status: "queued"` → `"posted"`, set `posted_at`.
- `CONTENT/social/POSTED_LOG.csv` (create) — append every successful post for the warmup poster's feedback loop.
- `CONTENT/social/posting_queue/ENGAGEMENT_PLAN_$(today).md` — write today's plan if missing.
