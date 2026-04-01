---
name: debug
description: Enter Debugger Mode - systematic 8-step debugging protocol from hyper-rat-engine. Reflects on 5-7 possible sources, distills to 1-2, adds diagnostic logs, checks console/network, produces comprehensive analysis. Use for any bug, failure, or unexpected behavior.
---

# Debugger Mode Activated

Follow this EXACT sequence. Do not skip steps. Do not guess fixes before completing diagnosis.

## Step 1: Reflect on 5-7 possible sources of the problem
List 5-7 different hypotheses for what could be causing the issue. Consider:
- Configuration/environment issues
- Logic errors in the code
- Data format mismatches
- Race conditions / timing issues
- Missing dependencies or imports
- API/external service failures
- Permission/access issues

## Step 2: Distill to 1-2 most likely sources
Rank the hypotheses by probability. Explain WHY these 2 are most likely based on the symptoms.

## Step 3: Add diagnostic logs
Add logging/console output to validate your top 2 hypotheses. Track the transformation of data throughout the control flow. Don't fix anything yet - just observe.

## Step 4: Check browser/client logs
Use available tools to check:
- Console logs (errors, warnings)
- Network requests (failed requests, unexpected responses)
- Any error boundaries or crash reports

## Step 5: Check server logs
If there's a server component, check server-side logs. If not accessible, ask the user to provide them.

## Step 6: Comprehensive analysis
Based on ALL collected evidence (not assumptions), produce a detailed analysis of:
- What is actually happening vs what should happen
- Where exactly the data/flow diverges from expected
- The root cause (not just the symptom)

## Step 7: Implement fix OR add more logs
If the root cause is clear: implement the fix.
If the source is still unclear: suggest additional targeted logs and repeat steps 4-6.

## Step 8: Cleanup
Once the fix is verified working, ask for approval to remove the diagnostic logs added in step 3.

---

**RULES:**
- Never guess fixes before step 6
- Always verify the fix actually works (run it, check output)
- If the fix doesn't work, go back to step 1 with new information
- Document what was wrong for future reference
