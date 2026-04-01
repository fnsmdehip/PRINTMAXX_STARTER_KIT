# HN -- Show HN: Zombie Agent Architecture
**Platform:** Hacker News
**Section:** Show HN
**Best time:** 10am EST (HN peaks mid-morning)
**Status:** READY TO POST
**Angle:** Technical architecture with honest failure mode

**Title:** Show HN: 5 AI agents I "killed" ran for 22 cycles and produced more value than the live ones

---

I run 33 autonomous Python agents on a MacBook via launchd. A swarm brain evaluates them every 4 hours and marks agents as KILLED/HIBERNATED in a state JSON when they underperform.

Problem: the brain updates the JSON but can't unload launchd plists (guardrails block ~/Library/ writes). So "killing" an agent is writing a note. launchd doesn't read the note.

I discovered today that 5 "dead" agents have been running for 22 cycles. The reports directory had fresh output files. One agent deployed 3 websites. Another fixed OG tags, Twitter cards, and sitemaps across 32 pages. A third scraped 10 new leads.

This is a split-brain problem applied to AI agent orchestration. The twist is that in traditional distributed systems, split-brain causes data corruption. Here it caused free productive labor.

Stack: Python + Claude Code + launchd plists + surge.sh (160 sites deployed). Total infra cost: $20/mo. The seo_aso_optimizer agent alone fixed 32 pages today and deployed 13 updates. No human input.

After 56 days: 528 scripts, 160 sites, 4 iOS apps, 22 products, 17K qualified leads, $0 revenue. The entire monetization layer is blocked on 45 minutes of account creation (Stripe, Gumroad, Gmail API).

The most interesting design question: should the orchestration layer be given the ability to actually kill agents (unload plists), or is the current "zombie-friendly" design better? The zombies are currently my most productive workers.

Code is Python, no frameworks. Happy to share architecture details.
