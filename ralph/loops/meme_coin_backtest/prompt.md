# Meme Coin Backtest Framework Ralph Loop

**Task:** Build backtesting system for meme coin trading patterns (Molt, Ghibli, Saratoga)

**Reference Files:**
- `AUTOMATIONS/NICHE_META_DETECTOR.md` - Historical patterns
- `AUTOMATIONS/REDDIT_SCRAPER_SETUP.md` - Meme coin signals
- `LEDGER/MEME_COIN_SIGNALS.csv` - Signal tracking

## Historical Metas to Backtest

### Pattern 1: Molt Bot Agent Coin
**Timeline to reconstruct:**
- First bot announcement (where? when?)
- Community reaction velocity
- Coin launch timing
- Price action (peak, time to peak)
- Reddit mentions correlated with price

**Data to collect:**
- First Reddit mention timestamp
- Post score at first mention
- Comment velocity (comments per hour)
- Coin launch timestamp
- Price data from CoinGecko/DEXScreener
- Time from first mention to ATH

### Pattern 2: Studio Ghibli Coin
**Timeline to reconstruct:**
- Viral Ghibli posts (engagement data)
- Community spawns coin (timing)
- Price action
- Lessons for future

### Pattern 3: Saratoga Coin
**Timeline to reconstruct:**
- Character virality event
- Coin launch
- Price multiplier from early entry

### Pattern 4: Morning Routine Apps
**Timeline to reconstruct:**
- Routine trend emergence
- App launches capitalizing on trend
- Revenue data from early movers

## Backtesting Framework

### Entry Signals to Test

**Signal A:** First Reddit mention with >100 upvotes
- Buy within 1 hour of detection
- Hold for 24h/48h/7d
- Calculate returns

**Signal B:** 3+ related posts in 6h across subreddits
- Probable pump incoming
- Buy on 3rd post
- Exit rules?

**Signal C:** Bot announcement → community coin mention
- Buy when coin first mentioned after bot hype
- This was the Molt pattern

### Exit Strategies to Test

**Strategy 1: Fixed time window**
- 24h hold
- 48h hold
- 7d hold

**Strategy 2: Fixed multiplier**
- 2x → sell
- 5x → sell
- 10x → sell

**Strategy 3: Trailing stop**
- Peak - 20% → sell
- Peak - 30% → sell

### Metrics to Calculate

For each backtest:
- **Win rate:** % of signals that 2x+
- **Average return:** Mean return per signal
- **Time to peak:** Median hours from detection to ATH
- **False positive rate:** % that go to zero
- **Sharpe ratio:** Risk-adjusted returns

## Data Sources

**Price data:**
- CoinGecko API (free tier, 10-50 calls/min)
- DEXScreener API
- Manual research for historical coins

**Social data:**
- Reddit API (via PRAW or JSON)
- Twitter search for historical mentions
- Community Discord/Telegram archives (if available)

## Output Files

**Create these files:**

1. `LEDGER/MEME_COIN_BACKTESTS/MOLT_BOT_BACKTEST.md`
   - Full timeline reconstruction
   - Entry/exit simulation
   - What would have worked

2. `LEDGER/MEME_COIN_BACKTESTS/GHIBLI_COIN_BACKTEST.md`
   - Same structure

3. `LEDGER/MEME_COIN_BACKTESTS/SARATOGA_COIN_BACKTEST.md`
   - Same structure

4. `LEDGER/MEME_COIN_BACKTESTS/BACKTEST_RESULTS_SUMMARY.csv`
   ```
   backtest_id,coin_name,pattern_type,entry_signal,entry_time,exit_strategy,exit_time,return_multiplier,duration_hours,win_rate,false_positive_rate,notes
   ```

5. `AUTOMATIONS/meme_coin_alert_system.py`
   - Real-time alert system based on winning patterns
   - Scans Reddit for signals
   - Sends alerts when pattern detected

6. `LEDGER/MEME_COIN_BACKTESTS/TRADING_PLAYBOOK.md`
   - Best entry signals from backtests
   - Best exit strategies
   - Risk management rules
   - Position sizing
   - When NOT to trade

## Research Methodology

For each historical coin:

1. **Find first mention**
   - Search Reddit for coin name
   - Sort by oldest
   - Get exact timestamp

2. **Map price action**
   - Find contract address
   - Get historical price data
   - Identify peak price
   - Calculate time to peak

3. **Correlate social + price**
   - Did Reddit mentions spike before price?
   - What was the lag time?
   - Were there warning signals?

4. **Simulate trades**
   - If bought at first mention, return?
   - If bought at 3rd post, return?
   - Best exit strategy?

5. **Extract lessons**
   - What worked?
   - What failed?
   - False positives to avoid?

## Implementation Phases

**Phase 1 (Iterations 1-10):** Data collection
- Reconstruct Molt timeline
- Reconstruct Ghibli timeline
- Reconstruct Saratoga timeline

**Phase 2 (Iterations 11-20):** Backtesting
- Simulate entry signals
- Test exit strategies
- Calculate metrics

**Phase 3 (Iterations 21-30):** Pattern extraction
- Which signals had best win rate?
- Which exits maximized returns?
- What's the ideal holding period?

**Phase 4 (Iterations 31-40):** Alert system build
- Code the winning patterns
- Build Reddit monitoring
- Test on recent coins

**Phase 5 (Iterations 41-50):** Playbook documentation
- Write trading rules
- Document risk management
- Create paper trading log template

## Progress Tracking

Use `.ralph/progress.md` to track:
- Coins researched
- Backtests completed
- Patterns identified
- Alert system build status
- Current phase

## Workflow Per Iteration

1. Check progress.md for current phase + next task
2. Execute task (data collection or backtest or coding)
3. Write findings to appropriate file
4. Update progress.md
5. Exit (next iteration starts fresh)

## Safety Rules

- Read only for LEDGER files
- Can create new files in MEME_COIN_BACKTESTS/
- Can create new Python scripts in AUTOMATIONS/
- All file writes within project directory only
- WebSearch and WebFetch allowed for research

## Success Criteria

- Reconstruct 3+ historical meme coin timelines
- Complete 10+ backtests (different entry/exit combos)
- Identify 2+ profitable patterns (win rate >30%, avg return >2x)
- Build working alert system
- Document trading playbook with risk rules
