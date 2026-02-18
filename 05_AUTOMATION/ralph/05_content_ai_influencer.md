---
task_id: CONTENT-003
test_command: "python3 -c \"import os; total = sum(len(os.listdir(f'CONTENT/social/ai_influencer/{d}')) for d in os.listdir('CONTENT/social/ai_influencer/') if os.path.isdir(f'CONTENT/social/ai_influencer/{d}')); assert total >= 60, f'Only {total} files'\""
max_iterations: 25
completion_signal: "AI_INFLUENCER_BATCH_COMPLETE"
---

# Task: Generate AI influencer content for 3 personas

## Context
- Read .claude/rules/copy-style.md for voice
- Read .ralph/guardrails.md for constraints
- Check LEDGER/CROSS_POLLINATION_MATRIX.csv for synergy opportunities
- Output to CONTENT/social/ai_influencer/
- Create directories: `mkdir -p CONTENT/social/ai_influencer/{niche_expert,fitness_coach,tech_explainer}`

## Personas to Create

### 1. NICHE_EXPERT (AI001) - 20 posts
- **Voice:** Thoughtful, analytical, shares frameworks
- **Synergy:** Stack with MM002 (courses), CF007 (motivation)
- **Content types:**
  - 8 value threads (frameworks, insights)
  - 6 hot takes (contrarian but smart)
  - 4 story posts (case studies, results)
  - 2 engagement posts (polls, questions)

### 2. FITNESS_COACH (AI005) - 20 posts
- **Voice:** Encouraging, no-BS, results-focused
- **Synergy:** Stack with MM001 (fitness app), CF007 (motivation)
- **Content types:**
  - 8 tips posts (workout, nutrition, mindset)
  - 6 myth-busting posts
  - 4 transformation hooks
  - 2 product mentions (subtle, for app cross-promo)

### 3. TECH_EXPLAINER (CF009) - 20 posts
- **Voice:** Curious, simplifying complex topics
- **Synergy:** Stack with MM003 (affiliate), MM004 (SaaS)
- **Content types:**
  - 8 explainer threads
  - 6 tool recommendations
  - 4 trend analysis
  - 2 prediction/opinion posts

## Per-Persona Deliverables
Each persona folder needs:
1. `bio.md` - Profile bio (160 chars)
2. `pinned.md` - Pinned tweet/post
3. `post_001.md` through `post_020.md`

## Post File Format
```markdown
---
persona: niche_expert | fitness_coach | tech_explainer
post_type: thread | hot_take | story | engagement | tip | myth_bust | explainer | tool_rec
platform: x
synergy_methods: [list of method IDs this could promote]
generated_date: 2026-01-22
char_count: [number or "thread" for multi-part]
---

[Post content here]
```

## Quality Checks
- Does each persona have a distinct voice?
- Would followers believe this is a real person?
- Are the synergy hooks natural, not forced?
- No em dashes, no banned vocabulary
- Threads have clear 1/, 2/, 3/ markers

## Cross-Pollination Opportunities
Embed subtle hooks for synergistic methods:
- NICHE_EXPERT: "I'm building a course on this..." (MM002)
- FITNESS_COACH: "New app I've been testing..." (MM001)
- TECH_EXPLAINER: "Best tool for this: [affiliate link placeholder]" (MM003)

## Success Criteria
1. [ ] 60 total posts (20 per persona)
2. [ ] Bio and pinned post for each persona
3. [ ] Voice consistency within each persona
4. [ ] No em dashes or banned vocabulary
5. [ ] Synergy hooks embedded naturally
6. [ ] Files in correct directory structure

## When complete
After all 60 posts + 6 supporting files created:
Output: <promise>AI_INFLUENCER_BATCH_COMPLETE</promise>
