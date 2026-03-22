---
alpha_id: ALPHA1773996268
source: r/ClaudeAI
priority: HIGH
route: INTELLIGENCE
url: https://www.reddit.com/r/ClaudeAI/comments/1rzyqqt/found_3_instructions_in_anthropics_docs_that/
score: 1524 upvotes
date_scraped: 2026-03-22
---

# Claude Hallucination Reduction Techniques

Source: Anthropic's official docs page — https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations

## The 3 Instructions

### 1. Allow Claude to say "I don't know"
Without this, Claude fills knowledge gaps with plausible fiction. With the instruction, it responds "I don't have enough information to answer that" instead of fabricating. The default behavior is to always give an answer, even when it shouldn't.

### 2. Verify with citations
Tell Claude every claim needs a source. If it can't find one, it should retract the claim. OP reported watching statements vanish from outputs when this was activated -- statements that previously sounded authoritative had no backing.

### 3. Use direct quotes for factual grounding
Force Claude to extract word-for-word quotes from documents before analyzing them. This prevents "paraphrase-drift" where the model subtly changes meaning while summarizing.

## Results

- All three together "fundamentally change the output quality"
- One commenter reported telling Claude to say "I don't know" and stick to a provided FAQ "almost completely fixed their customer support bot that was inventing answers"
- Another user estimated ~70% reduction in confidently wrong answers from instruction #1 alone
- Creativity tradeoff is real: arXiv 2307.02185 found ~15-20% drop in creative output with citation-heavy prompts
- OP's solution: toggle between "research mode" (all 3 active) and "default mode" (none active)

## Community Additions

**Toggle/slash command approach (multiple users):** Create a `/research` command that activates all 3 rules only when needed. Don't run them always.

**Label inferences explicitly (u/xkcd327, 4 upvotes):** Add "if you make an inference, label it explicitly as inference" to catch the middle ground between facts and guesses.

**Epistemic research prompt (u/Frosty-Tumbleweed648, 3 upvotes):** Full system prompt shared:
- "You are a research collaborator, not an authority"
- Flag confidence level, note where explanation is simplification vs precise
- Provide 2 analogies per concept, state what each hides/distorts
- For every theory, identify conditions under which it would fail
- Ask: "how would we design an experiment to test whether this explanation is a hallucination?"

**"Canonical" keyword (u/Isar3lite, 2 upvotes):** Using the word "canonical" in prompts helps Claude know data exists and to look for it before guessing.

**Context window degradation warning (u/fredjutsu, 10 upvotes):** These instructions lose effectiveness as context window fills up. Counter with hooks that re-inject the rules on every submission.

**Copyright constraint on quotes (u/YoghiThorn, 3 upvotes):** Claude may push back on direct quotes citing copyright constraints (one quote per source, under 15 words). This limits instruction #3 for general knowledge queries -- works best when Claude is analyzing YOUR documents.

**Step-wise approach (u/Frosty-Tumbleweed648):** Discussion first, then searching, then sourcing/quoting. Going step-wise produces better results than asking for everything at once.

## Application to PRINTMAXX

### 1. CLAUDE.md / Agent Prompts
Add a togglable research mode block to agent prompts that handle factual research (alpha processors, method discovery, competitive intel):

```
## Research Mode (activate for factual/intel tasks)
- If you lack sufficient information, say so explicitly. Do not fabricate.
- Every factual claim must cite a source. If no source exists, retract the claim.
- When analyzing documents, extract direct quotes before summarizing.
- If making an inference, label it explicitly as inference.
```

Do NOT apply to creative/content agents (engagement bait converter, content multiplier) -- the 15-20% creativity drop would hurt output quality.

### 2. Specific Scripts to Enhance
- `alpha_auto_processor.py` -- add research mode to the LLM prompt when classifying alpha entries. Reduces false-positive "real alpha" classifications.
- `method_discovery_crawler.py` -- when scoring methods, force citation of the source post/data. Prevents score inflation from hallucinated metrics.
- `autonomous_integrator.py` -- when analyzing methods for integration, require explicit "I don't know" for missing data rather than fabricating revenue estimates.
- `capital_genesis_ranker.py` -- add "label inferences" instruction so ranking explanations distinguish facts from estimates.

### 3. Hooks Integration
Per the community tip about context window degradation: use hooks to re-inject research mode instructions on every submission for research-critical agents, not just at session start.

### 4. The "Canonical" Trick
Already partially in use via our system map references. Extend: when agents need to reference existing state, use "check the canonical [X]" phrasing to reduce hallucination about system state.

### 5. Do NOT Apply Globally
The creativity-accuracy tradeoff is real. Keep the toggle approach:
- Research/intel agents: research mode ON
- Content/creative agents: research mode OFF
- Coding agents: selective (ON for architecture analysis, OFF for generation)
