# Alpha Processor

## Overview

A multi-tier pipeline that takes raw intelligence entries from multiple sources (scrapers, bookmarks, research), scores them for actionability, deduplicates, classifies by venture type, and routes to the correct destination. The processor transforms unstructured signal into scored, categorized, venture-assigned alpha ready for agents to act on. Handles 15,000+ entries with hash-based deduplication and multi-model processing tiers.

## Architecture

The processor operates as a staged pipeline with progressively deeper analysis at each tier.

```
Raw Sources                    Tier 1: Pre-Screen           Tier 2: Deep Analysis        Tier 3: Routing
┌─────────────┐               ┌─────────────────┐          ┌──────────────────┐          ┌─────────────────┐
│ Twitter      │──┐            │ Bulk filter      │          │ Full scoring     │          │ Route A: NEW    │
│ Scraper      │  │            │ - Dedup (MD5)    │          │ - Actionability  │          │   VENTURE       │
├─────────────┤  │            │ - Status check   │          │ - ROI potential  │          ├─────────────────┤
│ Reddit       │──┤            │ - Basic keyword  │          │ - Engagement     │          │ Route B: BOLSTER│
│ Scraper      │  ├──▶ CSV ──▶│   relevance      │──pass──▶│   authenticity   │──pass──▶│   EXISTING      │
├─────────────┤  │            │ - Format valid.  │          │ - Method extract │          ├─────────────────┤
│ Bookmarks    │──┤            └─────────────────┘          │ - Category match │          │ Route C: RESEARCH│
│ Import       │  │                    │                     │ - OPS index match│          │   TASK          │
├─────────────┤  │                 filtered                  └──────────────────┘          ├─────────────────┤
│ Research     │──┘                   out                            │                     │ Route D: HIGH   │
│ Feeds        │                                                   scored                  │   VALUE QUEUE   │
└─────────────┘                                                     │                     ├─────────────────┤
                                                                    │                     │ Route E: ARCHIVE│
                                                                    ▼                     └─────────────────┘
                                                          ALPHA_STAGING.csv
                                                          (scored, categorized,
                                                           routed)
```

**Pipeline stages:**

1. **Ingestion** -- raw entries arrive in ALPHA_STAGING.csv with status PENDING_REVIEW or NEW. Sources include Twitter scrapers (monitoring 133+ accounts), Reddit JSON API scrapers, bookmark imports, and manual research entries.

2. **Pre-screen (Tier 1)** -- bulk filter pass:
   - MD5 hash-based deduplication (text_hash on lowercase stripped content)
   - Status validation (only processes PENDING_REVIEW, NEW, or empty status)
   - Basic format validation
   - Skips entries already processed or archived

3. **Scoring (Tier 2)** -- multi-dimension analysis:
   - **Actionability score** -- does this entry contain specific steps, frameworks, or methods? Keywords: viral, trending, revenue, conversion, framework, etc.
   - **ROI potential** -- HIGHEST / HIGH / MEDIUM / LOW based on specificity of numbers, proof of results, replicability
   - **Engagement authenticity** -- checks for bot signals (engagement ratio, comment quality, account age vs follower count)
   - **Earnings claim verification** -- flags round numbers, text-only claims, selling-to-audience patterns
   - **Method extraction** -- identifies the core replicable tactic even when wrapped in hype

4. **Classification** -- maps scored entries to venture types using keyword matching and category inference:
   - APP_FACTORY, OUTBOUND, CONTENT, LOCAL_BIZ, MONETIZATION, RESEARCH, PRODUCT, SCRAPING
   - Also classifies by content type: APPROVED (real alpha), ENGAGEMENT_BAIT (good for content farming), REPURPOSE_ONLY (reference material), COMPLIANCE_RISK (needs FTC handling), EXAGGERATED_BUT_SIGNAL (strip hype, extract method)

5. **Routing (Tier 3)** -- directs classified entries to destinations:
   - Route A: NEW VENTURE -- creates a stub in OPS/ for novel opportunities
   - Route B: BOLSTER EXISTING -- appends to matching OPS/ or LEDGER/ file
   - Route C: RESEARCH TASK -- generates a cron entry for deeper investigation
   - Route D: HIGH VALUE QUEUE -- surfaces in a priority queue for immediate action
   - Route E: ARCHIVE -- marks entries that have been fully processed

## Required Inputs

- **Alpha staging CSV** -- the central inbox. Minimum columns: `alpha_id`, `source`, `content`, `category`, `status`, `roi_potential`, `reviewer_notes`, `engagement_authenticity`, `earnings_verified`, `venture_tag`, `timestamp`
- **OPS index** -- the processor builds an index of existing OPS/*.md files (filename stem -> first meaningful line) to match alpha entries to existing operations
- **Scraper outputs** -- Twitter, Reddit, and other scrapers deposit entries into the alpha CSV. The processor reads entries with PENDING_REVIEW or NEW status.

## Outputs

- **Scored alpha CSV** -- the same ALPHA_STAGING.csv with updated columns: `status` (APPROVED/ENGAGEMENT_BAIT/REJECTED/etc.), `roi_potential` (HIGHEST/HIGH/MEDIUM/LOW), `reviewer_notes`, `venture_tag`, `engagement_authenticity`, `earnings_verified`
- **High-value queue** -- a markdown file listing the highest-scored entries that need immediate action
- **Auto-generated cron entries** -- for research tasks that need periodic re-checking
- **OPS file updates** -- entries routed to existing ops are appended to the matching file
- **Processing log** -- detailed log of every entry processed, score assigned, route taken
- **Stats output** -- distribution of entries by status, category, venture, and ROI potential

## Setup

1. **Create the alpha staging CSV** with required columns:
   ```csv
   alpha_id,source,content,category,status,roi_potential,reviewer_notes
   ALPHA001,twitter_scraper,"Cold email framework...",OUTBOUND,PENDING_REVIEW,
   ```

2. **Configure scrapers** to deposit entries into the alpha CSV. Each scraper should:
   - Generate a unique alpha_id
   - Set status to PENDING_REVIEW or NEW
   - Include the source URL and raw content

3. **Set up the OPS directory** with existing operation files. The processor matches alpha entries to these files for Route B (bolster existing) routing.

4. **Schedule processing** via cron:
   ```bash
   # Process new entries every 6 hours
   0 */6 * * * python3 AUTOMATIONS/alpha_auto_processor.py --process-new
   ```

5. **Optional: configure the app factory command center** to refresh priority queues after processing.

## Example Usage

Preview what would be processed without making changes:
```bash
python3 alpha_auto_processor.py --dry-run
```

Process all new entries since last run:
```bash
python3 alpha_auto_processor.py --process-new
```

Process the full backlog:
```bash
python3 alpha_auto_processor.py --process-all
```

Process with a custom batch size:
```bash
python3 alpha_auto_processor.py --batch-size 50
```

View processing stats:
```bash
python3 alpha_auto_processor.py --status
```

Query processed alpha by venture type:
```bash
python3 alpha_query.py --venture APP_FACTORY --status APPROVED --top 10
```

Search across all alpha by keyword:
```bash
python3 alpha_query.py --search "cold email framework" --json
```

## Key Patterns

- **Multi-model pipeline design** -- the architecture supports tiered model usage. Cheap/fast models handle bulk pre-screening (dedup, format validation). Expensive/powerful models handle deep analysis (method extraction, ROI scoring). This keeps costs manageable at 15,000+ entries.
- **Hash-based deduplication** -- MD5 hash on lowercased, stripped content catches exact and near-exact duplicates. This runs before any scoring to avoid wasting compute on duplicates.
- **ROI normalization** -- all entries are scored on the same HIGHEST/HIGH/MEDIUM/LOW scale regardless of source. A Twitter alpha and a Reddit alpha are compared apples-to-apples.
- **Engagement authenticity checking** -- before trusting engagement metrics as proof of value, the processor checks for bot signals: engagement ratio anomalies, generic comments, account age vs follower count mismatches, suspicious reply clustering.
- **Earnings claim skepticism** -- default stance is that all earnings claims are inflated. Round numbers, text-only claims, and selling-to-audience patterns reduce confidence. The method is still extracted even when numbers are suspect.
- **OPS index matching** -- the processor builds a live index of OPS/ files and matches alpha entries to existing operations by stem name and content similarity. This enables automatic bolstering of existing ops rather than creating orphan documents.
- **Venture-based routing** -- each alpha entry is tagged with the most relevant venture type using a keyword map. Venture types map to specific method CSVs and strategy documents in the system.
- **Zero-waste content generation** -- the system mandates that every alpha review session triggers content generation (tweets, threads, cross-niche adaptations). Alpha that is merely logged to a CSV without generating downstream value is considered a pipeline failure.

## Limitations

- **Scoring is keyword-based, not semantic.** The processor uses keyword lists to estimate actionability and ROI. Entries with novel vocabulary or unusual framing may be under-scored.
- **Single CSV bottleneck.** All alpha flows through one CSV file. At very high volumes (50,000+ entries), file-locking contention and read performance may become issues. A SQLite FTS index exists as a mitigation but is a separate component.
- **Category inference is heuristic.** Venture type assignment uses keyword matching, not understanding. An entry about "app pricing strategies for dentists" could be tagged APP_FACTORY or LOCAL_BIZ depending on which keywords match first.
- **No automatic source credibility scoring.** The processor does not maintain a reputation database for sources. A consistently low-value source gets the same initial treatment as a consistently high-value one.
- **Route A (new venture creation) only creates stubs.** The processor does not fully build out new operations -- it creates a minimal file in OPS/ and relies on the CEO agent or human to develop it.
- **Batch processing, not streaming.** The processor runs on a schedule (cron) or manual trigger, not on every new entry. There is latency between an entry arriving and being processed.
