## Key Workflows

### Generate Content
```bash
# For longtail pages (use Haiku for bulk)
python scripts/generate_longtail.py --count 25 --model haiku

# For truth pages (use Sonnet for quality)
python scripts/generate_truth_page.py --topic "X" --model sonnet
```

### Validate Changes
Ask the **validator subagent** to check:
- Code style and lint rules
- SEO requirements (meta tags, structured data)
- Security (no exposed credentials)
- Performance (bundle size, image optimization)

### Code Review
Ask the **reviewer subagent** before commits:
- Test coverage check
- Breaking changes identified
- Documentation updated
- LEDGER files synced

### Deployment
Ask the **deployer subagent** to:
- Run full test suite
- Check build output
- Verify environment variables
- Create deployment checklist

---

## File Organization

```
PRINTMAXX_STARTER_KIT/
├── .claude/
│   ├── CLAUDE.md              # This file
│   ├── agents/                # Specialized subagents
│   └── rules/                 # Modular guidelines
├── LANDING/printmaxx-site/    # Next.js application
├── CONTENT/
│   ├── truth_pages/           # 10 pillar content pieces
│   └── longtail_pages/        # SEO optimized pages
├── LEDGER/                    # Source of truth CSVs
│   ├── GEO_PROMPTS_200.csv
│   ├── GEO_TRUTH_PAGES_10.csv
│   ├── GEO_LONGTAIL_SLUGS_300.csv
│   ├── FUNNEL_METRICS.csv
│   ├── MASTER_TASKS.md        # Task tracking
│   └── leads.csv              # Lead captures
├── AUTOMATIONS/               # Playwright scripts
├── OPS/
│   ├── prompts/               # Reusable agent prompts
│   └── logs/                  # Session runlogs
└── MASTER_DOC/                # Full operating system doc
```

---

## Useful Commands

```bash
# Development
make dev              # Start dev server
make build            # Production build
make test             # Run tests

# Validation
make validate         # Check file structure
make lint             # Code quality

# Content Generation
make longtail N=25    # Generate N longtail pages
make truth TOPIC=X    # Generate truth page

# Utilities
make clean            # Clean build artifacts
make sync-sheets      # Sync LEDGER with Google Sheets
```

---

## Common Patterns

### Adding a New Truth Page
1. Research topic and competition
2. Draft outline in CONTENT/truth_pages/
3. Use Sonnet to write compelling copy
4. Add to LEDGER/GEO_TRUTH_PAGES_10.csv
5. Build and test locally
6. Get review, then publish

### Bulk Longtail Generation
1. Filter LEDGER/GEO_LONGTAIL_SLUGS_300.csv for unpublished
2. Use Haiku for rapid generation (cheap + fast)
3. Use Sonnet for quality gates (every 10th piece)
4. Update CSV with published=TRUE
5. Run SEO validator

### Lead Magnet Creation
1. Research what converts in niche
2. Build interactive tool or downloadable
3. Create landing page in /magnet/
4. Wire up lead capture → LEDGER/leads.csv
5. Test conversion flow
6. Deploy and track in FUNNEL_METRICS.csv

---

