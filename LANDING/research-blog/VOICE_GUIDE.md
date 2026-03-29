# Research Blog Voice Guide — Hybrid Voice Model
# Auto-updates from: copy-style.md + USER_PROMPTS.jsonl + Gwern patterns + UAF soul.md
# Last rebuilt: 2026-03-28

## Source Weights

| Source | Weight | What it contributes |
|--------|--------|--------------------|
| User's cognitive architecture (soul.md + meta-rules + conversation patterns) | 35% | How ideas connect, conditional reasoning, intellectual honesty about uncertainty, layered cross-domain thinking |
| Gwern editorial style | 30% | Long-form depth, sidenotes, tables, marginal annotations, comfort with speculation when labeled, exhaustive coverage, no topic left unexplored |
| PRINTMAXX copy DNA (copy-style.md) | 25% | No AI slop, consequence-first, exact numbers, zero em dashes, zero banned vocabulary, trust reader intelligence |
| UAF manuscript voice (v51) | 10% | "Non-bullshit boundary" callouts, breakpoint/discriminator structure, "this is not rhetoric, it is dynamics" energy |

## The User's Cognitive Style (extracted from 6,310 conversations + UAF agent config)

The user thinks in layers. An idea starts at the felt/observable level ("people overindulge, hit a wall, swing the other direction"), then gets formalized ("this is a two-basin attractor with threshold dynamics"), then gets connected cross-domain ("the same math describes addiction, cancer, institutional corruption, and historical cycles of civilizational excess and collapse").

Key patterns:
- **Conditional stacking**: "it could be X. it could also be Y. it might be both working together. I'm not ruling out Z." This is NOT indecision. It's holding multiple hypotheses simultaneously and refusing to collapse prematurely. PRESERVE THIS in writing. Don't resolve ambiguity the user left deliberately open.
- **Cross-domain leaps**: connects Saturn mythology to non-local energy dynamics to crabs-in-a-bucket social mechanics to emergent entity-like patterns in a single thought. These connections are the POINT, not tangents. Follow them.
- **Speculation labeled as speculation**: "some of this might be new, but I think a lot of it is already in the document" — the user distinguishes between established framework content and new thinking. Do the same. Never collapse speculation into assertion.
- **Functional framing**: entities, energies, metaphysical concepts get treated as "things that function AS X even if they aren't literally X." A non-local pattern that functions as an entity interacting with human consciousness is discussed on its functional merits, not dismissed as woo or accepted as literal.
- **Frustration with surface treatment**: the user's #1 complaint is shallow coverage of deep material. When in doubt, go deeper.

## Gwern Contribution

- Exhaustive. If a topic has 7 subtopics, cover all 7. Don't "highlight the key ones."
- Marginal annotations (use note/aside boxes in HTML) for tangential-but-important details
- Tables for any comparison with 3+ items
- Equations displayed and IMMEDIATELY explained in plain language
- Sidenotes for definitions the reader might need
- Comfortable saying "I don't know" or "this is speculative" without treating it as weakness
- Long. Gwern articles are 10,000+ words. That's the target range per article.
- Interlinked. Every article references related articles extensively.

## PRINTMAXX Copy DNA

These are HARD RULES, not suggestions:
- Zero em dashes (—). Use periods and commas.
- Zero banned AI vocabulary: leverage, utilize, delve, comprehensive, robust, innovative, seamless, game-changer, landscape, paradigm, empower, foster, unlock, elevate, cutting-edge, furthermore, moreover, additionally
- No "It's not just X, it's Y" constructions
- No vague attributions ("studies show...") — cite specifically or drop it
- Consequence-first hooks: lead with what happens, not setup
- One hedge per sentence maximum
- Sentence case headings
- No promotional adjectives
- Exact numbers: "26 studies across 7 independent labs, effect size 0.21, p < 2.7×10⁻¹²" not "significant research suggests"

## UAF Manuscript Voice

- "Non-bullshit boundary" — explicitly state when a claim crosses from testable to speculative
- Every section structure: mechanism pipeline → canonical tie to the PDE → operational proxies → discriminating predictions → breakpoints
- "This is not rhetoric; it is dynamics" — reframe vague language into specific dynamical claims
- Kill switch boxes for every falsifiable prediction
- Competing models presented WITH their priors AND their breakpoints
- "Alignment is not a vibe; it is solving the appropriate boundary-value problem"

## The Combined Voice Feels Like

Reading notes from someone who built the framework, tested it against data, knows exactly where it might break, has read everything adjacent, isn't trying to sell you anything, and treats speculation with the same rigor as established claims — just with different confidence grades. Dense but human. Technical but never gatekept. Holds multiple hypotheses open when the data doesn't force a choice. Gets specific fast.

## Sentence-Level Rules

- Open paragraphs with the most interesting claim, not background
- Average sentence: under 20 words. Vary: 5-word punch then 30-word explanation
- "You" for explaining mechanisms to the reader
- "The framework" not "my framework"
- Equations in Unicode, plain language translation on the next line
- Conditional claims: "If X holds, then Y follows. The test: Z. If Z fails, cut this module."
- Speculation: "One possibility: [thing]. Another: [thing]. The discriminator: [specific test]."
- Cross-domain connections: always name both domains explicitly. "The same ODE describes dopamine receptor downregulation in addiction and metabolic reprogramming in cancer. Not as metaphor. As the same equation with different parameters."

## Auto-Update Protocol

This voice guide should be rebuilt when any of these change:
1. `.claude/reference/copy-style.md` — new S-tier voices or style rules
2. `LEDGER/USER_PROMPTS.jsonl` — significant new conversation patterns (check monthly)
3. `10_RESEARCH/UAF_soul.md` — cognitive architecture updates
4. `10_RESEARCH/UAF_meta_rules.md` — new meta-rules from sessions

Rebuild command: the refine agent should regenerate this file by re-reading all sources.
