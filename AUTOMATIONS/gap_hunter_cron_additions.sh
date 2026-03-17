#!/bin/bash
# GAP HUNTER CRON ADDITIONS — 2026-03-16 19:35
# Run: bash AUTOMATIONS/gap_hunter_cron_additions.sh
# These 7 scripts exist but were never scheduled in cron

BASE=/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

crontab -l > /tmp/cron_backup_gaphunter.txt

cat >> /tmp/cron_backup_gaphunter.txt <<'NEWCRON'

# =============================================================================
# GAP HUNTER ADDITIONS — 2026-03-16 19:35
# =============================================================================

# 6:10 AM - Twitter alpha deep scrape (bookmarks + high-signal accounts)
10 6 * * * cd $BASE && $PYTHON AUTOMATIONS/twitter_alpha_scraper.py --all >> AUTOMATIONS/logs/twitter_alpha_scraper.log 2>&1

# 6:25 AM - Reddit deep scrape (all 41 subreddits via JSON API)
25 6 * * * cd $BASE && $PYTHON AUTOMATIONS/reddit_deep_scraper.py --full >> AUTOMATIONS/logs/reddit_deep_scraper.log 2>&1

# Every 4h - Alpha auto-approver
0 */4 * * * cd $BASE && $PYTHON AUTOMATIONS/alpha_auto_approver.py --approve >> AUTOMATIONS/logs/alpha_auto_approver.log 2>&1

# Every 4h (offset 10min) - Alpha-to-ops converter
10 */4 * * * cd $BASE && $PYTHON AUTOMATIONS/alpha_to_ops.py --generate >> AUTOMATIONS/logs/alpha_to_ops.log 2>&1

# 8:00 AM - Content multiplier (1 piece to 20+ variants)
0 8 * * * cd $BASE && $PYTHON AUTOMATIONS/content_multiplier.py --batch >> AUTOMATIONS/logs/content_multiplier.log 2>&1

# 8:30 AM - Auto-respond to freelance opportunities
30 8 * * * cd $BASE && $PYTHON AUTOMATIONS/auto_freelance_responder.py >> AUTOMATIONS/logs/auto_freelance_responder.log 2>&1

# 9:00 AM - Monetization engine daily run
0 9 * * * cd $BASE && $PYTHON AUTOMATIONS/monetization_engine.py >> AUTOMATIONS/logs/monetization_engine.log 2>&1

# === END GAP HUNTER ADDITIONS 2026-03-16 ===
NEWCRON

crontab /tmp/cron_backup_gaphunter.txt
echo "Cron updated: $(crontab -l | wc -l) lines"
