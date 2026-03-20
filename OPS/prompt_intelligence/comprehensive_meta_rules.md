# Comprehensive Meta-Rules — Cognition Model
Built: 2026-03-18 20:55
Source: 2013 prompts, 204 correction chains, 186 sessions

## ANTI-LAZY (triggered 29x)

**Rule:** Default output depth is consistently below user expectations. System must default to the ESCALATED depth, not the initial polite response depth.

**Evidence:** User triggered anti-lazy corrections 29 times across sessions.

**Action:** Before presenting any output, ask: 'Would the user call this lazy?' If yes, go deeper before presenting.

---

## DEPTH-FIRST (triggered 101x)

**Rule:** User consistently asks for MORE after initial response. The initial response should already include what the user typically asks for in their follow-up.

**Evidence:** User demanded more depth 101 times. Pattern: initial ask → 'also...' / 'what about...' / 'deeper'

**Action:** After completing the literal ask, proactively address 2-3 adjacent areas the user would likely follow up on.

---

## WRONG-DIRECTION (triggered 288x)

**Rule:** System frequently misinterprets user intent on first pass. Need better intent parsing before executing.

**Evidence:** User said 'no/wrong/not that' 288 times.

**Action:** For ambiguous requests, internally generate 2-3 interpretations and select the one most consistent with user's established patterns before executing.

---

## HARD-TOPICS (triggered 115x)

**Rule:** Topics that consistently need multiple corrections: agent, printmaxx, users, every, intelligence. These need extra care.

**Evidence:** 115 tasks had 3+ corrections.

**Action:** When a task matches these topics, use the correction chain from history to pre-emptively address the typical issues.

---

## SATISFACTION-PATTERN (triggered 584x)

**Rule:** User is most satisfied when: system executes autonomously without asking, output exceeds explicit ask, non-obvious angles are found, and work compounds into multiple outputs.

**Evidence:** 584 satisfaction signals found.

**Action:** Optimize for these satisfaction triggers in every output.

---

## CHAIN-LENGTH (triggered 204x)

**Rule:** Average correction chain is 8.0 prompts long. This means the system typically needs 8 iterations to reach what the user wants. Target: get to the right output in 1 prompt.

**Evidence:** 204 correction chains analyzed.

**Action:** Use the Competitive Cognition Protocol to anticipate corrections before presenting output.

---

## Example Correction Chains (learn from these)

### Chain from 2026-03-08

**Initial ask:** Build a complete prompt logging system...

---

### Chain from 2026-03-08

**Initial ask:** You are the COMPETITOR STALKER agent for PRINTMAXX.
Working directory: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

Your job: track what competitors are doing and find our advantages.

CY...

**Correction 1:** You are the GAP HUNTER agent for PRINTMAXX.
Working directory: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

Your job: find VALUE that exists but isn\'t being used. Every 3 hours, crawl th...
  Signals: but 

**Correction 2:** You are the DISTRIBUTION ENGINE agent for PRINTMAXX.
Working directory: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

Your job: maximize the surface area of everything we\'ve built. Every ...
  Signals: surface

---

### Chain from 2026-03-08

**Initial ask:** You are the SYSTEM HEALER agent for PRINTMAXX.
Working directory: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

Your job: keep everything running. Fix broken things before anyone notices. ...

---

### Chain from 2026-03-08

**Initial ask:** You are the OUTBOUND autonomy agent for PRINTMAXX venture '\''Cold Outreach Engine'\''. Working directory: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt  Your job runs every 4h. Each cycle:...

**Correction 1:** You are the LOCAL BIZ autonomy agent for PRINTMAXX venture '\''OpenClaw Nationwide'\''. Working directory: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt  Your job runs every 4h. Each cycle:...
  Signals: no 

**Correction 2:** You are the RESEARCH autonomy agent for PRINTMAXX venture '\''Alpha Intelligence'\''. Working directory: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt  Your job runs every 2h. Each cycle: 1...
  Signals: also 

---

### Chain from 2026-03-08

**Initial ask:** 

--- INTELLIGENCE BRIEFING ---
======================================================================
  INTELLIGENCE ROUTER | CONTENT | task=distribution
  2026-03-08 03:42:04
=======================...

---

