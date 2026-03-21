You are the PRINTMAXX worker node. Execute the daily autonomous cycle:

1. Read OPS/PRINTMAXX_SYSTEM_MAP.md and OPS/CAPITAL_GENESIS_PRIORITY_STACK.md
2. Check what ran last: read output/worker_session_log.md and LEDGER/VENTURE_MAP_EXEC_STATE.json
3. Run the capital genesis ranker if stale: python3 AUTOMATIONS/capital_genesis_ranker.py
4. Execute the top 3 highest-priority tasks from the priority stack
5. Run venture map executor: python3 AUTOMATIONS/venture_map_executor.py --apply
6. Run loop closer: python3 AUTOMATIONS/loop_closer.py
7. Check Before You status: verify https://before-you-landing.surge.sh is live, check if generator needs updates
8. Write session results to output/worker_session_log.md

Focus on revenue-generating actions. Skip documentation-only tasks. Log errors but do not stop on non-critical failures.
