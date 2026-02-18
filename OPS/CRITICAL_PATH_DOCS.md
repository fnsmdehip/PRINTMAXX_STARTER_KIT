# Critical Path Documents - OPS/ Navigation Guide

**Purpose:** Tell agents exactly which files to read and in what order. Prevents agents from wasting context on orphaned or superseded files.

**Rule:** If a file is not listed here, it is either a deep-reference doc or a candidate for archival. Agents should NOT speculatively read OPS/ files. Use this guide.

---

## TIER 1: MUST-READ (Every Session Start)

These files are required context for any session. Read them in this order.

| Order | File | Why | Tokens |
|-------|------|-----|--------|
| 1 | `OPS/SESSION_HANDOFF.md` | Current state, blockers, what to do next | ~2K |
| 2 | `.claude/CLAUDE.md` (Session Log section at bottom) | What was built recently, current priorities | ~5K (bottom section only) |
| 3 | `setup/HUMAN_INFRA_CHECKLIST.md` | What human setup is done/blocked | ~2K |

**Total: ~9K tokens. If these 3 files are current, agent has full context to start working.**

Note: SESSION_HANDOFF.md is stale (Jan 27). CLAUDE.md session logs are the actual handoff mechanism now. Consider deprecating SESSION_HANDOFF.md.

---

## TIER 2: READ WHEN RELEVANT (Task-Specific)

Only read these when working on the specific task.

### Building Apps
| File | When to Read |
|------|-------------|
| `MONEY_METHODS/APP_FACTORY/APP_MONETIZATION_STRATEGY.md` | Before any app work |
| `MONEY_METHODS/APP_FACTORY/APP_STORE_REJECTION_GUIDE.md` | Before app submission |
| `MONEY_METHODS/APP_FACTORY/PAYWALL_PSYCHOLOGY_AB_PLAYBOOK.md` | When implementing paywall |

### SEO/GEO/ASO Work
| File | When to Read |
|------|-------------|
| `OPS/ENTITY_SEO_AGENT_READINESS_PLAYBOOK.md` | **CANONICAL** for all SEO/GEO work |
| `OPS/growth/GTM_OPTIMIZATION_CHECKLIST.md` | Before launching anything |
| `OPS/growth/SEO_KEYWORD_RESEARCH_GUIDE.md` | When doing keyword research |

**DO NOT READ:** GEO_RESEARCH_2025.md, SEO_AGENT_READABILITY_GUIDE.md, growth/SEO_GEO_ASO_TACTICS_2026.md, growth/SEO_GEO_ASO_RESEARCH_SUMMARY_2026.md, growth/SEO_GEO_ASO_ACTION_PLAN_2026.md. These overlap with the canonical file.

### Content Creation
| File | When to Read |
|------|-------------|
| `.claude/rules/copy-style.md` | **ALWAYS** before writing any content |
| `OPS/COPY_PSYCHOLOGY_MASTER_REFERENCE.md` | For sales/engagement psychology |
| `OPS/content/NICHE_ACCOUNT_CONTENT_CALENDAR.md` | When scheduling content |
| `OPS/growth/NICHE_POSTING_STRATEGY.md` | When planning posts |

**DO NOT READ all 3 content repurposing files.** They say the same thing. If needed, read only `content/CONTENT_REPURPOSING_AUTOMATION.md` (most actionable).

### Social Media Growth
| File | When to Read |
|------|-------------|
| `OPS/growth/TWITTER_GROWTH_PLAYBOOK_2026.md` | **CANONICAL** for X/Twitter |
| `OPS/growth/LINKEDIN_GROWTH_PLAYBOOK_2026.md` | For LinkedIn |
| `OPS/growth/EDGE_GROWTH_TACTICS.md` | For grey-hat growth |
| `OPS/growth/PLATFORM_AUTOMATION_LIMITS_2026.md` | Before any automation |
| `OPS/growth/ENGAGEMENT_FARMING_TACTICS.md` | For engagement strategy |

**DO NOT READ:** X_ALGORITHM_OPTIMIZATION.md, X_TWITTER_ALGORITHM_RESEARCH_2025.md, TWITTER_META_JANUARY_2026.md (covered by TWITTER_GROWTH_PLAYBOOK_2026.md).

### Cold Outbound
| File | When to Read |
|------|-------------|
| `MONEY_METHODS/COLD_OUTBOUND/EMAIL_SEQUENCES.md` | Email copy |
| `MONEY_METHODS/COLD_OUTBOUND/LINKEDIN_TEMPLATES.md` | LinkedIn copy |
| `OPS/operations/EMAIL_DELIVERABILITY_GUIDE.md` | Technical email setup |

### Setup/Infrastructure (Human Tasks)
| File | When to Read |
|------|-------------|
| `setup/RETARDMAXX_MANUAL_TODO.md` | **CANONICAL** for human setup tasks |
| `setup/ULTIMATE_STACK_GUIDE.md` | Deep reference for tool selection |
| `CAPITAL_GENESIS_HUMAN_TASKS.md` | Revenue-lane-specific human tasks |

**DO NOT READ the other 12 setup files.** They are earlier versions of the same content.

### Strategic Planning
| File | When to Read |
|------|-------------|
| `CAPITAL_GENESIS_UNIFIED_PLAN.md` | Master strategy |
| `CAPITAL_GENESIS_REPRIORITIZED_EXECUTION.md` | **CANONICAL** execution plan |
| `CAPITAL_GENESIS_DASHBOARD.md` | Current lane status |
| `CAPITAL_GENESIS_FASTEST_PATH.md` | Speed-ranked methods |

**DO NOT READ:** SURGICAL_EXECUTION_PLAN.md (superseded by REPRIORITIZED).

### Research/Alpha
| File | When to Read |
|------|-------------|
| `.claude/rules/alpha-review.md` | Before reviewing alpha |
| `LEDGER/ALPHA_STAGING.csv` | Current pending entries |
| `OPS/DIRECTIONAL_SIGNALS_2026.md` | Market direction intel |
| `OPS/HEDGE_FUND_INTELLIGENCE_REPORT.md` | Deep strategic intel |
| `OPS/NOVEL_OPPORTUNITIES_REPORT.md` | New method discovery |

### Quant Infrastructure
| File | When to Read |
|------|-------------|
| `OPS/QUANT_QUICK_START.md` | Quick commands |
| `OPS/QUANT_INFRASTRUCTURE_GUIDE.md` | Full usage guide |

### Compliance/Legal
| File | When to Read |
|------|-------------|
| `OPS/RISK_RADAR_FEBRUARY_2026.md` | Current risk landscape |
| `OPS/GREY_HAT_LEGAL_PLAYBOOK_2026.md` | Legal boundaries |
| `OPS/operations/LEGAL_COMPLIANCE_GUIDE.md` | FTC compliance |

### Browser Automation
| File | When to Read |
|------|-------------|
| `OPS/BROWSER_CONTROL/BROWSER_AGENT_GUIDE.md` | Fallback chain |

### Ralph Loops
| File | When to Read |
|------|-------------|
| `ralph/loops/mega/prompt.md` | Mega loop behavior |
| `ralph/loops/mega/.ralph/progress.md` | Current progress |
| `ralph/loops/mega/checkpoints/` | Human review items |

---

## TIER 3: DEEP REFERENCE (Rarely Read)

These files exist as reference material. Only read when explicitly needed for a specific question.

| File | Purpose | When |
|------|---------|------|
| `setup/ULTIMATE_STACK_GUIDE.md` (45KB) | Full tool/service catalog | Comparing tools |
| `setup/COMPREHENSIVE_STACK_COMPARISON.md` (25KB) | 200+ tool matrix | Tool selection |
| `METHOD_STACKING_PLAYBOOK.md` (37KB) | Revenue multiplier stacks | Method stacking decisions |
| `ULTRATHINK_CAPITAL_STACKS.md` (16KB) | Non-obvious strategies | Strategic brainstorming |
| `COHERENCE_AUDIT_2026-01-28.md` (33KB) | Stress test of plan | Validity checking |
| `content/ALL_33_NICHES_CONTENT_STRATEGY.md` (65KB) | Per-niche content | Building for specific niche |
| `content/CONTENT_CALENDAR_ALL_33_NICHES.md` (37KB) | Per-niche calendar | Scheduling for specific niche |
| `ULTIMATE_ACCOUNT_WARMUP_GUIDE.md` (20KB) | Warmup protocols | Setting up new accounts |
| `VA_HIRING_SYSTEM.md` (17KB) | VA hiring | When hiring VAs |
| `TELEGRAM_COMMUNITY_GUIDE.md` (17KB) | Telegram communities | When building Telegram |

---

## TIER 4: DO NOT READ (Archive Candidates)

These files should NOT be read by agents. They are either:
- Superseded by newer files
- Premature (for systems that don't exist yet)
- Orphaned (not referenced anywhere)

See `OPS/DEPRECATED_FILES.txt` for the complete list.

**Key files to NEVER read:**
- Any file in `setup/` except RETARDMAXX_MANUAL_TODO.md, HUMAN_INFRA_CHECKLIST.md, ULTIMATE_STACK_GUIDE.md, COMPREHENSIVE_STACK_COMPARISON.md
- FRESH_CHAT_PROMPT.md (old paths)
- MODEL_ROUTING_POLICY.md (irrelevant with Max plan)
- TOKEN_COST_CHECKPOINTS.md (irrelevant with Max plan)
- SURGICAL_EXECUTION_PLAN.md (superseded)
- GEO_RESEARCH_2025.md (outdated)
- YOUTUBE_SHORTS_RESEARCH_2025.md (outdated)
- AI_VOICE_TOOLS_COMPARISON_2025.md (outdated)
- CUSTOMER_SUPPORT_GUIDE.md (premature)
- CRISIS_RESPONSE_PLAYBOOK.md (premature)
- DISCORD_COMMUNITIES_ALL_NICHES.md (premature, 105KB)
- TELEGRAM_COMMUNITIES_ALL_NICHES.md (premature, 94KB)

---

## Context Budget Quick Math

| Scenario | Without Guide | With Guide | Savings |
|----------|--------------|-----------|---------|
| Session start | 30-50K tokens (reads multiple files) | 9K tokens (reads 3 files) | 70-80% |
| SEO task | 40-60K (reads 8 SEO files) | 12K (reads canonical + checklist) | 70-80% |
| Setup context | 25-40K (reads 5+ setup files) | 5K (reads canonical) | 80-87% |
| Content creation | 20-30K (reads 3 repurposing files) | 8K (reads 1 file) | 60-73% |
