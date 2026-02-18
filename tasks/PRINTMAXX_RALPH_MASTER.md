# PRINTMAXX Ralph Master Guide

This document guides ralph agents on how to find and use all the alpha/stack knowledge in the PRINTMAXX codebase.

## Quick Reference: Where Everything Lives

### Alpha & Research
| What | Location | Purpose |
|------|----------|---------|
| New findings | `LEDGER/ALPHA_STAGING.csv` | All new alpha, PENDING_REVIEW status |
| Approved alpha | Various `LEDGER/*.csv` files | Integrated into workflows |
| High-signal sources | `LEDGER/HIGH_SIGNAL_SOURCES.csv` | 66+ X accounts to scan |
| App opportunities | `LEDGER/APP_CLONE_OPPORTUNITIES.csv` | Apps to clone |
| App playbooks | `LEDGER/APP_FACTORY_METHODS.csv` | Proven building methods |
| Watchlist | `LEDGER/ALPHA_WATCHLIST.csv` | Emerging tools to monitor |

### App Factory
| What | Location | Purpose |
|------|----------|---------|
| App builds | `MONEY_METHODS/APP_FACTORY/builds/` | All app source code |
| SDK 54 apps | `builds/*-sdk54/` | Latest Expo 54 versions |
| Monetization | `APP_FACTORY/APP_MONETIZATION_STRATEGY.md` | IAP, subscriptions, affiliates |
| Assets guide | `APP_FACTORY/ASSET_GENERATION_GUIDE.md` | Icons, images, Gemini prompts |
| App Store guide | `APP_FACTORY/APP_STORE_REJECTION_GUIDE.md` | Avoid rejection |
| Discovery process | `APP_FACTORY/APP_DISCOVERY_PROCESS.md` | Find trending apps |
| QA Report | `builds/SDK54_QA_REPORT.md` | Current app status |

### Content & Video
| What | Location | Purpose |
|------|----------|---------|
| Remotion prompts | `OPS/prompts/remotion/REMOTION_MASTER_PROMPT.md` | Video templates |
| Remotion project | `LANDING/printmaxx-site/src/remotion/` | Video compositions |
| Video outputs | `LANDING/printmaxx-site/out/` | Rendered videos |
| Copy style | `.claude/rules/copy-style.md` | Human-first writing |
| Truth pages | `CONTENT/truth_pages/` | SEO pillar content |

### Automation
| What | Location | Purpose |
|------|----------|---------|
| X bookmarks | `AUTOMATIONS/x_bookmarks/` | Twitter scraping scripts |
| Ralph tasks | `ralph_tasks/` | Legacy task definitions |
| Ralph system | `scripts/ralph/` | Snarktank ralph installation |
| PRDs | `tasks/` | Product requirement docs |
| Skills | `~/.claude/skills/` | Claude Code skills |

### Configuration
| What | Location | Purpose |
|------|----------|---------|
| Main instructions | `.claude/CLAUDE.md` | Master operating guide |
| Code style | `.claude/rules/code-style.md` | TypeScript patterns |
| Security | `.claude/rules/security.md` | Security requirements |
| Performance | `.claude/rules/performance.md` | Optimization targets |

## How to Use Alpha Stack

### Before Starting Any Task

1. **Read relevant CLAUDE.md sections** - Find the section matching your task
2. **Check LEDGER files** - See what alpha exists for your domain
3. **Review existing code** - Look at working examples (prayerlock-sdk54, biomaxx-sdk54)
4. **Check for PRDs** - See if there's a detailed plan in `tasks/`

### Alpha Integration Pattern

When you discover something useful:
```
1. Add to LEDGER/ALPHA_STAGING.csv with PENDING_REVIEW status
2. Include actionable_steps (numbered list of how to implement)
3. Set appropriate category: APP_FACTORY, CONTENT_FORMAT, OUTBOUND, GROWTH_HACK, TOOL_ALPHA, MONETIZATION
4. Human reviews and either APPROVES or REJECTS
5. If APPROVED, integrate into relevant master file
```

### Finding Best Practices

**For app building:**
1. Check `LEDGER/APP_FACTORY_METHODS.csv` for proven patterns
2. Read `APP_MONETIZATION_STRATEGY.md` for revenue tactics
3. Review working SDK 54 apps for code patterns
4. Check `ALPHA_STAGING.csv` for latest tactics (filter by APPROVED)

**For content:**
1. Read `.claude/rules/copy-style.md` for writing guidelines
2. Check `LEDGER/WINNING_CONTENT_STRUCTURES.csv` for formats
3. Review `OPS/prompts/remotion/` for video templates
4. Look at `CONTENT/truth_pages/` for SEO examples

**For outbound:**
1. Check `LEDGER/ALPHA_STAGING.csv` category=OUTBOUND
2. Read `MONEY_METHODS/COLD_OUTBOUND/` for sequences
3. Review email infrastructure docs

## Ralph Execution

### Available PRDs

1. `tasks/prd-app-icon-generation.md` - Generate 3D app icons
2. `tasks/prd-remotion-video-regeneration.md` - Remake marketing videos
3. `tasks/prd-sdk54-app-fixes.md` - Fix broken SDK 54 apps
4. `tasks/prd-twitter-bookmark-extraction.md` - Deep bookmark analysis

### Running Ralph

```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT

# Convert PRD to prd.json
# (Use ralph skill or manually create)

# Run ralph loop
./scripts/ralph/ralph.sh --tool claude 10
```

### Creating New PRDs

Use the PRD skill or follow this pattern:
1. Define clear user stories (small, one-iteration scope)
2. Reference relevant alpha/docs from this guide
3. Include acceptance criteria with "Typecheck passes"
4. Save to `tasks/prd-[feature-name].md`
5. Convert to `prd.json` for ralph execution

## Key Principles

1. **Alpha stacks** - Always build on existing alpha, don't reinvent
2. **Reference files** - Point to specific files, not vague concepts
3. **Small iterations** - Each ralph story = one context window
4. **Human greenlight** - PENDING_REVIEW for anything publishable
5. **Progress logging** - Update progress.txt and BOOKMARK_EXTRACTION_LOG.md
6. **Pattern consolidation** - Add reusable patterns to CLAUDE.md files

## Emergency References

**If stuck on app building:** Read `APP_FACTORY/APP_LAUNCH_FULL_STACK.md`
**If stuck on content:** Read `.claude/rules/copy-style.md`
**If stuck on alpha:** Read `.claude/CLAUDE.md` → DAILY RESEARCH SYSTEM
**If ralph fails:** Check `scripts/ralph/progress.txt` for learnings
