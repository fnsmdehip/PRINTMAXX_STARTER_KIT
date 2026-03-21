# META ADS AUTONOMOUS SYSTEM

Fully autonomous Meta (Facebook/Instagram) ad management pipeline. Zero daily human input after setup. Agent monitors, kills bleeders, scales winners, writes new copy from what converts, and uploads creative directly to your ad account.

## CONCEPT

Replace the daily Ads Manager ritual (the same 5 questions every morning for 20 years) with an agent loop that runs autonomously: health check, fatigue detection, auto-pause, budget shift, copy generation, creative upload, morning brief.

## TOOLING

| Tool | Role | Cost |
|------|------|------|
| OpenClaw (or equivalent agent framework) | Orchestration layer, skill execution | $0/mo (open source) |
| social-cli (@vishalojha_me) | Wraps Meta Marketing API: token refresh, pagination, rate limits | $0 (open source) |
| Meta Marketing API | Read/write access to ad accounts | $0 (Meta charges for ads, not API) |
| Claude API (via PRINTMAXX Claude Max) | Copy generation, pattern analysis | Included in $200/mo Max plan |
| Telegram/Slack bot | Delivery channel for briefs and approvals | $0 |

Total incremental cost: $0/mo on top of existing PRINTMAXX infrastructure.

## 6-STEP AUTONOMOUS LOOP

### Step 1: Daily Health Check
- Agent queries Meta Marketing API via social-cli
- Five questions answered automatically:
  1. Am I on track against target CPA?
  2. What campaigns are running?
  3. Which ads are winning (lowest CPA, highest ROAS)?
  4. Which ads are bleeding (CPA > target)?
  5. Any creative fatigue signals?
- Output: structured health report (JSON) + human readable brief

### Step 2: Fatigue Detection
- Pull daily frequency by ad via Marketing API
- **Signal**: frequency > 3.5 = audience is cooked, CTR drop imminent
- This single metric saves more ad spend than any dashboard
- Log all fatigue events to `fatigue_log.csv` for trend analysis
- Cross reference with CTR decline to validate the 3.5 threshold per account

### Step 3: Auto-Pause Bleeders + Budget Shift
- **Kill rule**: CPA > 2.5x target for 48hrs = auto-pause, no hesitation
- Rank every active campaign by efficiency (CPA, ROAS, CTR composite score)
- Recommend (or auto-execute) budget shift from bottom performers to top
- Example outcome: "Paused an $87 CPA campaign at 3am and scaled best performer 30%"
- All actions logged to `actions_log.csv` with timestamp, campaign ID, reason, amount

### Step 4: Write New Ad Copy from Winners
- Agent analyzes top performing ads: hooks, angles, CTAs, emotional triggers
- Generates variations using Claude, modeled on patterns in YOUR winning ads
- Not generic copy; trained on what already converts in your specific account
- Output: 3-5 copy variants per winning angle, stored in `copy_queue.json`
- Human can review or auto-approve based on confidence threshold

### Step 5: Upload Ads Directly
- New creative + copy assembled into ad format
- Published directly to Meta Ads Manager via Marketing API
- No manual downloading, formatting, clicking through upload flow
- Agent handles the entire publish cycle: ad set targeting, placement, budget allocation
- Confirmation logged, new ad IDs tracked

### Step 6: Morning Brief + Content Concepts
- Spots patterns across winners: what themes, hooks, visuals are trending
- Suggests what to test next based on diminishing returns analysis
- Delivers everything to Telegram, Slack, or wherever configured
- **Human interaction**: 90 seconds to read, reply "approved", done

## IMPLEMENTATION PATH

### Phase 1: Read-Only Monitor (Week 1)
- Set up social-cli with Meta Marketing API credentials
- Build health check + fatigue detection skills
- Deliver daily brief to Telegram
- **No write actions yet**, just monitoring

### Phase 2: Auto-Pause + Budget Recs (Week 2)
- Enable auto-pause for confirmed bleeders (CPA > 2.5x for 48hrs)
- Budget shift recommendations (human approved via Telegram reply)
- Track savings from auto-paused campaigns

### Phase 3: Copy Generation + Upload (Week 3-4)
- Analyze winning ad patterns
- Generate copy variants via Claude
- Auto-upload with human approval gate (reply "approved" to publish)
- Remove approval gate once confidence is established

## PRINTMAXX CROSS-POLLINATION

| From | To | How |
|------|----|-----|
| Meta Ads | Before You | Run ads for ancestry narrative product ($19.99/$39.99 tiers) |
| Meta Ads | App Factory | Paid acquisition for PWAs once organic validates product-market fit |
| Meta Ads | EAS | Case study: "we built an autonomous ad manager, we can build yours" |
| Content Farm | Meta Ads | Organic content winners become ad creative candidates |
| Meta Ads | Newsletter | Retarget newsletter subscribers, use newsletter engagement as lookalike seed |
| Meta Ads | Digital Products | Paid traffic to Gumroad products once unit economics proven |

## KEY METRICS

- **CPA**: cost per acquisition vs target (primary)
- **ROAS**: return on ad spend (secondary)
- **Frequency**: fatigue signal, threshold 3.5
- **CTR**: click-through rate, early warning for creative decay
- **Spend saved**: $ from auto-paused bleeders (track weekly)
- **Time saved**: hours of manual Ads Manager eliminated (track weekly)

## KILL / DOUBLE TRIGGERS

- **Kill**: Ad spend > $500 with 0 conversions after 14 days across all campaigns
- **Double**: ROAS > 3x sustained for 7 days on any campaign = increase budget 50%

## FILES

```
META_ADS_AUTONOMOUS/
  META_ADS_PLAYBOOK.md          # This file
  config/
    targets.json                # CPA targets, frequency thresholds, budget rules per venture
    credentials.env             # Meta API tokens (gitignored)
  logs/
    health_reports/             # Daily health check JSONs
    fatigue_log.csv             # Frequency tracking
    actions_log.csv             # Auto-pause, budget shift actions
    copy_queue.json             # Generated copy awaiting approval/upload
  scripts/
    health_check.py             # Step 1: daily health check
    fatigue_detector.py         # Step 2: frequency monitoring
    auto_pauser.py              # Step 3: kill bleeders
    budget_optimizer.py         # Step 3: shift budget to winners
    copy_generator.py           # Step 4: Claude-powered copy from winners
    ad_uploader.py              # Step 5: publish to Meta
    morning_brief.py            # Step 6: compile + deliver brief
    orchestrator.py             # Runs full loop, cron-scheduled
```

## SOURCE / CREDIT

Concept adapted from an OpenClaw Meta Ads Kit demo. Core insight: the same 5 questions asked of Ads Manager every morning for 20 years can be answered by an agent in seconds, and the single most valuable signal (frequency > 3.5) is one that dashboards bury.
