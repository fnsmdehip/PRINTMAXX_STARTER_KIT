# Niche Meta Detection Ralph Loop

**Task:** Detect meta opportunities across ALL 88+ niches with historical pattern matching

**Reference Files (read these):**
- `AUTOMATIONS/NICHE_META_DETECTOR.md` - Historical patterns, detection methodology
- `LEDGER/MONEY_METHODS_TRACKER.csv` - All 88 methods
- `LEDGER/RESEARCH_SUBREDDITS.csv` - 40 subreddits to scan
- `LEDGER/HIGH_SIGNAL_SOURCES.csv` - Twitter accounts to monitor

## Historical Meta Patterns to Detect

### Pattern 1: Character/Brand Virality → Coin Launch
**Examples:** Ghibli coin, Saratoga coin, Molt bot coin

**Indicators:**
- Viral posts about specific character/brand (10K+ engagement in 24h)
- Community spawns unofficial coin within 48h
- Opportunity window: First Reddit mention → 10-50x in 18-48h

**Detection signals:**
- Character name trending across Reddit + Twitter
- Fan art/memes spike (3+ posts in 6h)
- "Someone should make a [character] coin" comments
- Community Discord/Telegram forms

### Pattern 2: Routine/Lifestyle Trend → Product/Service
**Examples:** Morning routine apps, 75 Hard trackers, Cold plunge products

**Indicators:**
- "My [routine] changed my life" posts (5+ in week)
- Before/after content spike
- Subreddit formation
- Opportunity: Build app/info product for routine tracking

### Pattern 3: Tool/Platform Arbitrage → Quick Money Method
**Examples:** Notion templates, Canva templates, ChatGPT GPTs

**Indicators:**
- New platform feature announced
- Community asks "How do I use this for [use case]?"
- Early adopters making $X (posted with proof)
- Opportunity window: 2-8 weeks before saturation

### Pattern 4: Controversy/Drama → Engagement Farming
**Indicators:**
- Rapid comment velocity (500+ comments in 2h)
- Polarizing topic (upvote ratio 60-75%)
- Quote tweets > retweets

## For Each Niche (N001-N088+), Detect:

1. **Trending subtopics** - What's hot THIS week in the niche
2. **Pain point spikes** - Sudden increase in "How do I..." posts
3. **Tool opportunities** - Community asking for specific tools
4. **Coin/token potential** - Character/brand virality
5. **Content angles** - What's getting 10K+ engagement

## Cross-Platform Velocity Check

**Trending = mentions across 3+ platforms in 24h:**
- Reddit (3+ posts in different subreddits)
- Twitter (trending topic or 100+ mentions)
- TikTok (hashtag with 1M+ views)
- Product Hunt (featured or 500+ upvotes)

## Scoring System

For each detected meta:
- **Coin potential:** 0-10 (based on community size + brand affinity)
- **Product potential:** 0-10 (based on pain point clarity + willingness to pay)
- **Content potential:** 0-10 (based on engagement velocity)
- **Time window:** Days/Weeks/Months before saturation

## Output Files

**Create/update these files as you discover metas:**

1. `LEDGER/META_TRACKER.csv` - All detected metas
   ```
   meta_id,meta_name,category,detected_date,velocity_score,coin_potential,product_potential,content_potential,time_window,applicable_niches,historical_pattern_match,status
   ```

2. `LEDGER/MEME_COIN_SIGNALS.csv` - Coin-specific signals
   ```
   signal_id,coin_name,character_brand,first_mention_timestamp,reddit_score,twitter_mentions,community_size,pattern_match,entry_window,status
   ```

3. `LEDGER/NICHE_META_OPPORTUNITIES.csv` - Per-niche opportunities
   ```
   opportunity_id,niche_id,niche_name,meta_detected,opportunity_type,evidence,applicable_methods,priority,created_date
   ```

## Progress Tracking

Use `.ralph/progress.md` to track:
- Which niches you've scanned (N001-N088+)
- Metas detected per niche
- Patterns matched
- Cross-platform confirmations

## Workflow Per Iteration

1. Pick next unscanned niche from progress.md
2. Search Twitter + Reddit + TikTok for niche keywords
3. Check for pattern matches against 4 historical patterns
4. Score coin/product/content potential
5. Cross-reference with existing LEDGER files
6. Write findings to output CSVs
7. Update progress.md
8. Exit (next iteration starts fresh)

## Safety Rules

- Read only, no bash commands
- Append to CSVs, don't overwrite
- Check for duplicates before adding
- All file writes within project directory only
- WebSearch and WebFetch allowed

## Success Criteria

- Scan all 88+ niches
- Detect 20+ metas with cross-platform velocity
- Match 10+ to historical patterns
- Flag 5+ coin opportunities
- Flag 10+ product opportunities
