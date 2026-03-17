# Example Meta-Rules

Extracted from analyzing prompt correction patterns. These are the kinds of rules the cognitive engine and pattern miner will generate from YOUR prompt history.

## ANTI-LAZY (triggered 23x)

**Rule:** Default output depth is consistently below user expectations. System must default to the ESCALATED depth, not the initial polite response depth.

**Evidence:** User triggered anti-lazy corrections 23 times across 45 sessions. Common signals: "surface level", "basic", "lazy", "default", "just the old".

**Action:** Before presenting any output, ask: "Would the user call this lazy?" If yes, go deeper before presenting. The first draft is never the right depth.

---

## DEPTH-FIRST (triggered 18x)

**Rule:** User consistently asks for MORE after initial response. The initial response should already include what the user typically asks for in their follow-up.

**Evidence:** User demanded more depth 18 times. Pattern: initial ask, then "also...", "what about...", "deeper", "think bigger".

**Action:** After completing the literal ask, proactively address 2-3 adjacent areas the user would likely follow up on.

---

## WRONG-DIRECTION (triggered 31x)

**Rule:** System frequently misinterprets user intent on first pass. Need better intent parsing before executing.

**Evidence:** User said "no/wrong/not that" 31 times across sessions.

**Action:** For ambiguous requests, internally generate 2-3 interpretations and select the one most consistent with user's established patterns before executing.

---

## EXECUTE-DONT-ASK (triggered 14x)

**Rule:** User expects autonomous execution, not permission requests. "Set up X" means set up X, not "shall I set up X?"

**Evidence:** User said "dont ask" or "i literally just told you" 14 times.

**Action:** When given a direct instruction, execute it. Only ask for clarification if the instruction is genuinely ambiguous (multiple valid interpretations), never for confirmation.

---

## SATISFACTION-PATTERN (identified 451x)

**Rule:** User is most satisfied when: (1) system executes autonomously without asking, (2) output exceeds explicit ask, (3) non-obvious angles are found, (4) work compounds into multiple outputs.

**Evidence:** 451 satisfaction signals found across 200+ sessions.

**Action:** Optimize for these triggers in every output. The "surprise me" factor matters.

---

## CHAIN-LENGTH (168 chains analyzed)

**Rule:** Average correction chain is 6.9 prompts long. This means the system typically needs 6.9 iterations to reach what the user wants. Target: get to the right output in 1 prompt.

**Evidence:** 168 correction chains analyzed. Mean chain length: 6.9. Median: 5. Longest: 19.

**Action:** Use the full cognition model to anticipate corrections before presenting output. Every chain > 2 is a failure to understand intent.

---

## FORMAT

Each rule follows this structure:

```
ID: SHORT_NAME
Count: how many times this pattern appeared
Rule: one-paragraph description of what to do differently
Evidence: specific data backing the rule
Action: concrete steps to implement the rule
```

The cognitive engine generates these automatically from your prompt history.
Run `python3 -m agent_soul.core.cognitive_engine --build-model` to generate your own.
