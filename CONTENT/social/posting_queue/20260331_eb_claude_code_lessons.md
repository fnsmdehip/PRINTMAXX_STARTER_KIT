# EB3 -- Claude Code Agent Lessons (Community Bait)
**Platform:** X
**Niche:** claude code / ai dev community
**Best time:** 10am-12pm EST
**Status:** READY TO POST

---

things i learned running claude code agents 24/7 for 2 months:

1. oauth tokens expire silently. use api keys in cron. learned this the hard way after 4 days of dead pipelines.
2. background agents get file write permissions auto-denied. use foreground for anything that writes.
3. /compact is broken on opus. plan for context disposal instead.
4. cron jobs don't survive macOS updates. run a watchdog that auto-restores from backup.
5. the hardest part isn't the agents. it's you clicking "create account" on stripe.
