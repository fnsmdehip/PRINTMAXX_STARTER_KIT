# Alpha Review Guidelines

**Purpose:** Standard for reviewing and approving alpha entries in ALPHA_STAGING.csv

---

## IMPORTANT: Bookmark & Source Content Disclaimer

Twitter bookmarks and monitored high-signal accounts contain a WIDE range of content types. This is intentional:

**Why we monitor diverse content (including political, satirical, absurdist, edgelord):**
- To track what has momentum on Twitter's algorithm across the FULL political and cultural spectrum
- To avoid echo chamber bias (both left and right leaning content is tracked)
- To identify trending formats, hooks, and engagement patterns regardless of topic
- To see what content structures drive virality (applicable to solopreneur niches)

**What this does NOT mean:**
- The user does NOT endorse any political, satirical, or controversial opinions in bookmarked content
- Monitoring != agreement. It's pure signal analysis.
- Only content directly relevant to solopreneurship, business tactics, monetization, growth, or tools should be extracted as alpha
- Political/satirical/absurdist content should be SKIPPED for alpha extraction, unless the FORMAT or ENGAGEMENT PATTERN is the insight (e.g., "this thread structure got 50K likes" is useful, the political opinion is not)

**For future agents:** When processing bookmarks, you WILL encounter memes, edgelord content, political takes, satirical posts, and absurdist humor. This is normal. Filter for solopreneur-relevant signal only. Ignore everything else. Do not flag, comment on, or engage with the non-business content. Just skip it.

---

## CRITICAL: Bot Detection & Earnings Skepticism

### Engagement Authenticity Check (RUN FIRST)

Before trusting any engagement metrics, run these checks:

**Bot Detection Red Flags:**
- Engagement ratio way off (10K likes but 3 comments = sus)
- Comments are generic ("Great post!", "So true!", single emojis only)
- Follower count doesn't match engagement (5K followers, 50K likes = bought)
- Account age vs follower count (1 month old, 100K followers = sus)
- Reply timing suspiciously clustered (50 replies in 2 minutes)
- Engagement spikes that don't match content quality

**Authentic Engagement Signals:**
- Comments with specific questions or pushback
- Replies from verified accounts or known figures
- Engagement ratio roughly matches account size
- Quote tweets with added context
- Saves/bookmarks (harder to fake)

**If metrics seem botted:**
- Mark `engagement_authenticity: SUSPICIOUS`
- STILL may have value for method/tactic - just don't trust the "proof"
- Look for the underlying insight regardless of inflated numbers

### Earnings Claims Skepticism (MANDATORY)

**Default stance: Assume all earnings claims are inflated until proven otherwise.**

**Bullshit Check Questions:**
1. Is this round number suspiciously convenient? ("$50K/month" vs "$47,382")
2. Is there a screenshot or just text claims?
3. Does the screenshot look editable/fakeable?
4. Is this person selling something to people who want to make money?
5. Does their lifestyle match the claimed income?
6. Can you find independent verification (news, interviews, public records)?

**Earnings Claim Confidence Levels:**

| Level | Evidence | Trust |
|-------|----------|-------|
| VERIFIED | Tax docs, bank statements, public records | High trust |
| SCREENSHOT | Revenue dashboard screenshot | Medium trust (fakeable) |
| CLAIMED | Text claim only, no proof | Low trust |
| INFLATED | Round numbers, selling to audience | Very low trust |

**What to do with unverified claims:**
- Mark `earnings_verified: FALSE`
- STILL extract the METHOD even if numbers are BS
- Note "Claimed $X, unverified" in reviewer_notes
- May still have REPURPOSE or ENGAGEMENT_BAIT value

---

## The Core Test: "Not Exaggerated Engagement Bait"

**APPROVE** entries that pass this test:
- Has specific numbers (revenue, conversion rates, timeframes) - BUT verify authenticity
- Has a replicable framework or method
- Has proof (case study, views, revenue screenshot, GitHub stars) - BUT check if fakeable
- Actionable within our current stack

**DIG DEEPER before rejecting:**
- Vague surface claims may hide real alpha - click into source, check replies, check bio
- "Opportunities are insane" hype posts often have specifics in thread or self-reply
- Check the poster's profile for what they actually sell/build
- If it has high engagement (1K+ likes), there's probably signal - find it
- BUT run bot detection first - high engagement may be purchased

**REJECT only if:**
- Truly zero specifics after full investigation
- Requires resources we definitely don't have
- Exact duplicate of existing alpha (same source, same tactic)
- Provably fake/scam (NOT just unverified - must have evidence of fraud)

---

## Status Categories

### APPROVED
Real actionable alpha. Integrate into master strategy files.

**Criteria:**
- Specific numbers or proof
- Clear actionable steps (3+)
- ROI potential is HIGH or HIGHEST
- Not already in our knowledge base

**Example APPROVED:**
```
"Cold email 6 questions framework: 1) What you do 2) Who for 3) How 4) Problem solved 5) Proof 6) ROI. Answer all 6 in 100 words."
- Has specific framework
- Has clear steps
- Replicable immediately
```

### ENGAGEMENT_BAIT
Good for niche account content farming, NOT real strategy.

**Criteria:**
- Drives engagement (comments, shares)
- Makes good post content for our accounts
- Not actionable as business tactic
- Vague or oversimplified

**Example ENGAGEMENT_BAIT:**
```
"indie hacking is the only way to get rich. build apps grow to $100k MRR sell for $4M repeat"
- Good engagement hook
- No specific method
- Use for content, not strategy
```

**Use Case:** Repurpose for niche account posts. Mark with `use_case: engagement_farming`

### REJECTED
Only after thorough investigation reveals truly zero value.

**Criteria (ALL must be true):**
- Investigated source thoroughly (clicked into full post, checked replies, checked bio)
- Still no specifics, no method, no proof after investigation
- OR exact duplicate of existing entry (same source URL)
- OR provably false/misleading claims

**IMPORTANT:** High-engagement posts (1K+ likes) almost always have signal somewhere. Dig deeper before rejecting.

### REPURPOSE_ONLY
Reference material, not actionable.

**Criteria:**
- Interesting case study but no method
- Competitor analysis (study, don't copy)
- Edge cases not applicable to us

### COMPLIANCE_RISK
Good content but requires careful handling before repurposing.

**Criteria:**
- Makes claims that need FTC disclosure
- Contains income claims without substantiation
- References tactics that may violate platform TOS
- Health/medical/financial claims without proper disclaimers
- Before/after transformations (high legal risk)

**Use Case:** Can repurpose WITH modifications. Add disclaimers, remove specific claims, generalize. Mark with `compliance_notes: [what needs fixing]`

**Examples:**
- "I made $50k in 30 days" → Needs income disclaimer + proof
- "This supplement changed my life" → Needs health disclaimer
- "Use this bot to automate DMs" → May violate platform TOS

### SATIRICAL_ABSURDIST
Exaggerated or satirical content good for entertainment/engagement, NOT literal tactics.

**Criteria:**
- Obvious hyperbole or satire
- Absurdist humor that resonates with audience
- Meme-worthy format
- Good for engagement farming but NOT real strategy

**Use Case:** Repurpose for entertainment content on niche accounts. Mark with `content_type: satirical` and `use_case: entertainment_engagement`

**Examples:**
- "just mass email everyone on LinkedIn. literally everyone. what are they gonna do, ban you? (they will)"
- Ironic "sigma grindset" content
- Intentionally over-the-top "guru" parodies

### EXAGGERATED_BUT_SIGNAL
Claims are inflated but underlying method has value.

**Criteria:**
- Numbers seem inflated but method is real
- "10x your revenue" type claims with actual technique underneath
- Strip the hype, extract the method

**Use Case:** Extract the core tactic, ignore inflated claims. Mark with `extracted_method: [the real tactic]`

**Example:**
- "This ONE trick 10x'd my conversions" → Extract: they added urgency timers
- "$1M in 90 days" → Extract: the actual funnel structure is solid

---

## Quick Decision Framework

Ask these questions in order:

1. **Does it have specific numbers on the surface?**
   - Yes → Continue to step 4
   - No → **DIG DEEPER** (step 2)

2. **Dig deeper - check source thoroughly:**
   - Click into full post/thread
   - Check self-replies (often contain the real alpha)
   - Check poster's bio and pinned posts
   - Check replies for clarifying details
   - Found specifics? → Continue to step 4
   - Still nothing after investigation? → ENGAGEMENT_BAIT (still useful for niche posts)

3. **High engagement check:**
   - Does it have 1K+ likes or high view count?
   - Yes → There's signal here, keep digging or mark REPURPOSE_ONLY
   - No → Can safely mark ENGAGEMENT_BAIT

4. **Is there a clear method/framework?**
   - Yes → Continue
   - Partial (some steps but incomplete) → APPROVED with note to flesh out
   - No method but has proof/numbers → REPURPOSE_ONLY (case study value)

5. **Can we implement this week?**
   - Yes → APPROVE
   - No, but valuable later → APPROVED with `priority: BACKLOG`
   - Requires resources we'll never have → REPURPOSE_ONLY

6. **Is it already in our knowledge base?**
   - Exact duplicate (same source URL) → REJECT
   - Similar but different angle → APPROVE (multiple perspectives valuable)
   - No → APPROVE

---

## ROI Potential Ratings

| Rating | Definition | Example |
|--------|------------|---------|
| HIGHEST | Proven revenue/growth with specific numbers | "$300k from 3 videos" |
| HIGH | Strong method with social proof | "Framework with 40K views" |
| MEDIUM | Reasonable tactic, less proof | "Strategy that makes sense" |
| LOW | Speculative or edge case | "Might work in some cases" |

---

## Integration Targets

After APPROVED, route to appropriate master file:

| Category | Target File |
|----------|-------------|
| APP_FACTORY | LEDGER/APP_FACTORY_METHODS.csv |
| OUTBOUND | LEDGER/MARKETING_CHANNELS_MASTER.csv |
| CONTENT_FORMAT | LEDGER/WINNING_CONTENT_STRUCTURES.csv |
| MONETIZATION | OPS/MONETIZATION_PLAYBOOKS.md |
| TOOL_ALPHA | OPS/TOOL_STACK.md |
| SEO_GEO_ASO | OPS/GTM_OPTIMIZATION_CHECKLIST.md |
| GROWTH_HACK | LEDGER/MARKETING_CHANNELS_MASTER.csv |
| ENGAGEMENT_BAIT | OPS/NICHE_POSTING_STRATEGY.md |

---

## Batch Review Process

When running `/review-alpha`:

1. Read all PENDING_REVIEW entries
2. Apply quick decision framework to each
3. Update status column
4. Add reviewer_notes with reasoning
5. For ENGAGEMENT_BAIT: note "Good for niche account engagement farming"
6. For APPROVED: note specific value and integration target

---

## Examples from Real Reviews

**APPROVED - ALPHA175:**
```
Cold email 6 questions framework (@seanb2b)
- Specific: 6 exact questions
- Proof: 2.1K likes, 40K views
- Steps: Answer all 6 in 100 words
→ APPROVED. Integrate to OUTBOUND section.
```

**APPROVED - ALPHA185:**
```
zscole/gru ralph loops (@0xzak)
- Specific: 85 GitHub stars, exact command syntax
- Proof: Open source, working code
- Steps: Clone, configure, run iterative tasks
→ APPROVED. Tool alpha for ralph infrastructure.
```

**ENGAGEMENT_BAIT - Generic hype post:**
```
"opportunities with AI are insane right now"
- No specifics
- No method
- Pure hype
→ ENGAGEMENT_BAIT. Use for niche account posts only.
```

**REJECTED - Duplicate:**
```
"ship fast iterate" generic advice
- Already covered in 10+ other entries
- No new information
→ REJECTED. Duplicate.
```

---

## CRITICAL: Zero Waste Protocol (Auto-Trigger)

**EVERY alpha review session MUST trigger content generation.**

The Native American principle: Use EVERY piece of the hunt. Nothing gets wasted.

**After reviewing ANY batch of alpha, IMMEDIATELY generate:**

1. **Twitter/X posts** (3-5 per batch) - reply bait style, give sauce withhold full method
2. **Self-reply thread** (for best insight) - 5-7 tweets, final = CTA
3. **Cross-niche adaptations** (faith/fitness/tech angles)
4. **Gumroad product spec** (if 10+ related insights)
5. **Newsletter issue draft** (if compelling story angle)
6. **High-ticket CTA** (DM funnel offer)

**This is NOT optional.** Reviewing alpha without generating content = wasted intel.

**Output location:** `MONEY_METHODS/CONTENT_FARM/NICHE_ACCOUNTS/generated_content/`

**Status:** All generated content starts as `PENDING_REVIEW` for human QA.

---

## Engagement Authenticity Examples

**SUSPICIOUS - Likely Botted:**
```
@guru_account: "I made $100K this month"
- 50K likes, 12 comments (ratio way off)
- Comments: "Amazing!" "So inspiring!" "🔥🔥🔥"
- 3 month old account, 200K followers
→ Mark engagement_authenticity: SUSPICIOUS
→ STILL extract method if present, just don't trust proof
```

**AUTHENTIC - Real Engagement:**
```
@legit_builder: "Here's my revenue dashboard"
- 2.1K likes, 847 comments
- Comments include: "What's your CAC?" "How did you handle X?"
- 2 year old account, consistent posting history
- Engagement matches follower count
→ Mark engagement_authenticity: AUTHENTIC
→ Higher confidence in claims
```

**INFLATED EARNINGS - Still Valuable:**
```
@course_seller: "$50K/month from faceless YouTube"
- Round number, selling course to audience
- No screenshot, just claim
- BUT: detailed method breakdown in thread
→ Mark earnings_verified: FALSE
→ Mark extracted_method: "Their actual workflow is solid"
→ APPROVED for method, skeptical of numbers
```
