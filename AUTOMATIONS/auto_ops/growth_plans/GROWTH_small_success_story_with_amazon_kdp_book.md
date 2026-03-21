# Growth Plan: Small success story with Amazon KDP book (Non-fiction)

**Created:** 2026-03-21 12:40
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $150-600/mo per book at steady state, $1,500-6,000/mo at 10-book catalog (3-6 month build timeline)

---

## Tactics

1. Target niche sweet spot: 1K-10K monthly searches, <200 avg reviews on top 10 books — proven demand, beatable competition
2. Mine 1-star and 2-star reviews of top competitors to find gaps — make those gaps the book's USP
3. Cross-link entire catalog in back matter of every book — drives Amazon internal recommendation traffic
4. Disclose AI-assisted writing on KDP dashboard (required post-2024) — do not skip, account ban risk
5. Launch with 10-20 ARC readers via r/BetaReaders (free) and BookSirens free tier for social proof reviews
6. Use KDP Select free days (5 per 90-day enrollment) during launch week to spike rank and visibility
7. Add lead magnet link in book (free companion resource) — builds email list from readers for future launches

## Budget Tier Strategies

### FREE
ARC outreach via Reddit r/BetaReaders and Goodreads groups, Amazon A+ Content (free after first sale), KDP Select free days, cross-book linking, keyword research via free tier of Publisher Rocket alternatives (DS Amazon Quick View extension)

### LOW
$0-50/mo — Amazon AMS ads at $5/day on exact-match keywords per title ($35/wk budget), BookBub Featured Deal application (free to apply, $15-50/slot when accepted), Kindle Countdown Deals for backlist titles

### MID
$50-200/mo — 3-5 Amazon AMS campaigns at $10-15/day each, Fiverr cover designer ($30-50/book for premium covers vs AI-generated), Goodreads giveaways for social proof, BookBub Ads for retargeting warm readers

## Daily Actions

- [ ] 1. Create kdp_book_factory.py with 4-phase DAG: niche_scan → plan → generate → package
- [ ] 2. Playwright scraper: hit Amazon BSR /best-sellers/[category] for 20 non-fiction categories, extract top 100 per category with ASIN, title, review count, price, BSR rank
- [ ] 3. Niche scorer: filter to niches where avg top-10 review count <200 AND price $3.99-9.99 AND clear informational keyword (how-to, guide, system)
- [ ] 4. Review miner: for top 3 niches, scrape 1-2 star reviews of top 5 books — extract recurring complaints as content differentiation signals
- [ ] 5. Outline generator: claude -p with niche + review gap data → 10-chapter outline with 2000-word chapter targets
- [ ] 6. Chapter workers: 4 parallel subagents via claude -p, each assigned 2-3 chapters with outline context, write 2000-2500 words per chapter
- [ ] 7. Compiler: merge chapters, add intro/outro boilerplate, format to python-docx KDP spec
- [ ] 8. Metadata generator: claude -p → title/subtitle/description/7 keywords + Midjourney cover prompt
- [ ] 9. Output package to MONEY_METHODS/APP_FACTORY/builds/kdp-books/[niche-slug]/
- [ ] 10. KPI entry: add to KPI_DASHBOARD.md. HUMAN ACTION required: upload .docx + metadata to KDP dashboard, set price, enable KDP Select
- [ ] 11. Cron: 0 7 * * 1 (Monday 7am) — weekly niche scan + one full book pipeline run

## Tooling

```json
{
  "browser": "playwright (Amazon BSR scraping, competitor review mining)",
  "content": "claude -p parallel workers (chapter generation, metadata, cover briefs)",
  "formatting": "python-docx (KDP-spec .docx output: 1-inch margins, 11pt Garamond, section breaks)",
  "email": "none initially"
}
```
