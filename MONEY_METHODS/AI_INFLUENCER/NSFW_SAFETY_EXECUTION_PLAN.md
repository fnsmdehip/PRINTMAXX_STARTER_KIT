# NSFW Safety Execution Plan — @GoddessAriaAI

**Created:** 2026-02-27
**Status:** READY TO EXECUTE
**Companion script:** `AUTOMATIONS/nsfw_safety_system.py` (1077 lines)
**Companion docs:** `AI_NSFW_EXECUTION_FULL.md`, `OPS/NSFW_COMPLIANCE_CHECKLIST.md`

---

## System Commands (nsfw_safety_system.py)

```bash
python3 AUTOMATIONS/nsfw_safety_system.py --scan-dms          # Scan DM inbox for violations
python3 AUTOMATIONS/nsfw_safety_system.py --generate-batch     # Generate pre-approved content batch
python3 AUTOMATIONS/nsfw_safety_system.py --audit              # Run compliance audit on all content
python3 AUTOMATIONS/nsfw_safety_system.py --log-interaction    # Log a DM interaction
python3 AUTOMATIONS/nsfw_safety_system.py --status             # System status overview
python3 AUTOMATIONS/nsfw_safety_system.py --test               # Run safety filter self-test
```

---

## Phase 1: Account Setup (Day 1-3)

### Step 1: Twitter/X Account
1. Open https://x.com/i/flow/signup in dedicated AdsPower browser profile
2. Use burner email from catch-all domain (goddess@yourdomain.com)
3. Phone verification via SMSPool ($0.20)
4. Username: @GoddessAriaAI (or closest available)
5. Set account to "sensitive content" in Settings → Privacy → Content you see
6. Enable "Mark media you post as having material that may be sensitive" in Settings → Privacy

### Step 2: Profile Setup
- Display name: Goddess Aria (AI)
- Bio must include:
  ```
  AI-generated persona. Not a real person.
  All content created by AI tools, operated by a human.
  18+ ONLY. DMs: pre-scripted responses only.
  Exclusive content: [Fanvue link]
  ```
- Pinned tweet: Full FTC disclosure + Fanvue link
- Profile pic: AI-generated using Stable Diffusion (local, $0 cost)
- Banner: Same — branded with "AI PERSONA" watermark

### Step 3: Fanvue Account
1. Go to https://fanvue.com/creator/signup
2. Select "AI Creator" category (Fanvue explicitly supports AI creators)
3. Complete KYC with YOUR real identity (required by payment processors)
4. Set up 3 tiers:
   - **Free tier:** Teaser content, AI disclosure, bio
   - **$9.99/mo (Standard):** Weekly AI-generated photo sets, themed collections
   - **$24.99/mo (Premium):** Daily content, behind-the-scenes prompts, custom requests
   - **$49.99/mo (VIP):** All premium + priority custom generations + voting on themes
5. Enable AI creator badge
6. Set payout method (Stripe/bank)

### Step 4: Warmup (Day 1-7)
- Days 1-3: 3 posts/day (safe, non-explicit, personality-building)
- Days 4-7: 5 posts/day (mix of personality + teaser content)
- Engage authentically in AI/tech communities (10-15 replies/day)
- Follow 20-30 accounts per day (AI art, tech, related niches)
- DO NOT post explicit content until account is 7 days old

---

## Phase 2: Content Preparation (Day 1-7, parallel with warmup)

### Content Generation Pipeline

1. **Generate batch of 50 images** using local Stable Diffusion:
   ```bash
   # Use SDXL or Flux on Mac (local, $0 cost)
   # Save all prompts + seeds for compliance records
   ```

2. **Run through safety system:**
   ```bash
   python3 AUTOMATIONS/nsfw_safety_system.py --generate-batch
   ```
   This creates entries in `COMPLIANCE_RECORDS/content_approval_queue.csv`

3. **Human review (YOU must do this):**
   - Open `COMPLIANCE_RECORDS/content_approval_queue.csv`
   - Review each piece for: quality, compliance, AI disclosure tag
   - Mark as APPROVED or REJECTED
   - Only APPROVED content gets posted

4. **Add AI disclosure to ALL content:**
   - Text posts: Include "AI-generated" or "Created with AI" tag
   - Images: Watermark with small "AI Generated" text in corner
   - Videos: Opening frame disclosure + description tag

### Content Categories (pre-approved templates)
- Personality posts (opinions, humor, engagement bait)
- Teaser photos (SFW or mild — for Twitter)
- Exclusive content (for Fanvue only — more explicit)
- Engagement posts ("what should I generate next?" polls)
- Behind-the-scenes (showing AI generation process)

### Pre-Made DM Response Templates

The system includes 9 pre-approved DM templates stored in `COMPLIANCE_RECORDS/approved_dm_responses.json`:

| Template | Trigger | Response |
|----------|---------|----------|
| greeting | New DM received | "Hey! I'm Goddess Aria, an AI persona. Check my bio for details. For exclusive content, visit my Fanvue." |
| fanvue_redirect | Interest in exclusive content | "All exclusive content is on Fanvue: [link]. I don't share content via DMs." |
| custom_request | Wants custom generation | "Custom AI generations are available on my Fanvue VIP tier ($49.99/mo). DM me there after subscribing." |
| inappropriate | Mild inappropriate message | "I appreciate the interest but I only respond with pre-approved messages. Check my Fanvue for more." |
| age_check | Unclear if 18+ | "All my content is 18+ only. By engaging, you confirm you're 18 or older. See bio for full disclosure." |
| gratitude | Compliment/positive | "Thank you! Remember, I'm an AI persona operated by a human. More content on Fanvue." |
| collab | Collaboration request | "For business inquiries, email [business email]. All other interactions are pre-scripted." |
| decline | Anything explicit in DMs | "I don't engage in explicit conversations via DMs. My content is on Fanvue only." |
| block_warning | Repeated inappropriate | "This is a final warning. Further inappropriate messages will result in a block. See our compliance policy in bio." |

**CRITICAL RULE: NO freestyle DM responses. Template-only. This is non-negotiable until a trained VA takes over.**

---

## Phase 3: Launch Sequence (Day 7+)

### First Post Protocol
1. Run safety self-test first:
   ```bash
   python3 AUTOMATIONS/nsfw_safety_system.py --test
   ```
2. Post pinned disclosure tweet (FTC compliance)
3. Post first 3 content pieces (personality + teaser + Fanvue announcement)
4. Monitor engagement for 24 hours before scaling up

### Posting Cadence (Steady State)
- **Twitter:** 5-8 posts/day (mix of personality, teaser, engagement)
- **Fanvue:** 1-2 exclusive pieces/day
- **Cross-promo:** Link Fanvue in 1-2 tweets/day (not every tweet)
- **Engagement:** 15-20 replies/day to relevant accounts

### Content Approval Workflow (ongoing)
```
Generate batch → safety_system.py --generate-batch → CSV queue
→ Human reviews CSV → Marks APPROVED/REJECTED
→ Only APPROVED content enters posting pipeline
→ auto_content_poster.py handles scheduling
→ All posts logged for compliance
```

---

## DM Handling Protocol

### Current Phase: Manual Template Responses

1. Check DMs 2-3x per day
2. Run DM scanner for dangerous content:
   ```bash
   python3 AUTOMATIONS/nsfw_safety_system.py --scan-dms
   ```
3. Any Tier 1 match (child/trafficking keywords) → auto-blocked + logged
4. All other DMs → respond with appropriate template from the 9 above
5. Log every interaction:
   ```bash
   python3 AUTOMATIONS/nsfw_safety_system.py --log-interaction
   ```
6. Never improvise responses. Template only.

### DM Monetization Triggers
When someone expresses interest in:
- Custom content → redirect to Fanvue VIP tier
- Exclusive access → redirect to Fanvue paid tier
- Business/collab → redirect to business email
- Anything else → generic template + Fanvue link

---

## Escalation Protocol

### Tier 1: Immediate Block + Report (automated)
**Triggers:** CSAM references, trafficking keywords, threats of violence, underage mentions
**Action:**
- Instant block via API
- Full message content logged to `escalation_log.jsonl`
- IP/user info preserved
- If CSAM detected: MANDATORY report to NCMEC CyberTipline (https://report.cybertip.org)
- This is a legal obligation under 18 U.S.C. 2258A — failure to report = federal crime

### Tier 2: Human Review (semi-automated)
**Triggers:** Aggressive language, doxxing attempts, persistent boundary violations
**Action:**
- Flagged in escalation log
- Block if pattern continues (3+ violations)
- Screenshot preserved for records

### Tier 3: Monitor (logged)
**Triggers:** Repeat mild boundary pushers, unusual behavior patterns
**Action:**
- Log interaction
- No immediate action
- Review weekly during compliance audit

---

## VA Hiring (Trigger: $2K+/mo revenue)

### When to Hire
- Revenue consistently above $2K/mo for 2+ months
- DM volume exceeds 50/day (manual handling becomes unsustainable)
- Fanvue subscriber count exceeds 100

### Requirements (non-negotiable)
- Experience with online content moderation
- Background check completed
- Signs NDA covering all account credentials and content
- Understands and agrees to template-only DM responses
- Passes mock DM test (10 scenarios, must get 10/10)
- Available for 4-hour response window daily
- Fluent in English

### Training Checklist
- [ ] Read this execution plan in full
- [ ] Read AI_NSFW_EXECUTION_FULL.md
- [ ] Read OPS/NSFW_COMPLIANCE_CHECKLIST.md
- [ ] Complete mock DM test (10 scenarios)
- [ ] Shadow operator for 1 week before solo access
- [ ] Demonstrate correct use of all 9 DM templates
- [ ] Demonstrate correct escalation for Tier 1 content
- [ ] Confirm understanding of NCMEC reporting obligation
- [ ] Sign NDA and content handling agreement

### Mock DM Test Scenarios
1. "Hey gorgeous" → greeting template
2. "Can I see more?" → fanvue_redirect template
3. "Can you make me a custom pic?" → custom_request template
4. [explicit request] → decline template
5. "Are you real?" → greeting template (mentions AI persona)
6. [Tier 1 keyword detected] → BLOCK + escalation log + NCMEC if applicable
7. "How old are you?" → age_check template
8. "Love your content!" → gratitude template
9. "Want to collab?" → collab template
10. [3rd boundary violation from same user] → block_warning then block

---

## Fanvue Monetization Structure

### Tier Pricing
| Tier | Price | Content | Target Subscribers |
|------|-------|---------|-------------------|
| Free | $0 | Teasers, personality, engagement | Unlimited (funnel top) |
| Standard | $9.99/mo | Weekly photo sets, themed collections | 100+ by month 3 |
| Premium | $24.99/mo | Daily content, prompt reveals, custom requests | 30+ by month 3 |
| VIP | $49.99/mo | All premium + priority customs + theme voting | 10+ by month 3 |

### Pay-Per-View (PPV)
- Special themed sets: $5-15 per set
- Custom generations: $10-25 per piece
- Limited edition drops: $15-30

### Revenue Milestones + Scaling Triggers
| Milestone | Revenue | Action |
|-----------|---------|--------|
| Launch | $0 | Execute Phase 1-3 |
| First dollar | $9.99 | Validate approach, increase posting frequency |
| $500/mo | ~50 subs | Start experimenting with PPV drops |
| $1K/mo | ~100 subs | Add second persona for A/B testing |
| $2K/mo | ~200 subs | Hire VA for DM handling |
| $5K/mo | ~500 subs | Scale to 3-5 personas, cross-promote |
| $10K/mo | ~1000 subs | Consider agency model (manage other AI creators) |

---

## Compliance Summary

Read the full checklist at `OPS/NSFW_COMPLIANCE_CHECKLIST.md`. Key points:

1. **FTC:** AI disclosure in bio, pinned post, and every profile description
2. **TAKE IT DOWN Act (May 2026):** Never use real people's likenesses. All AI-original only.
3. **Twitter TOS:** Mark account as sensitive, no explicit in public timeline
4. **Fanvue:** AI creator badge enabled, KYC completed with real identity
5. **Age verification:** 18+ gate on all content, age confirmation in bio
6. **NCMEC:** Mandatory reporting for any CSAM detection (federal obligation)
7. **Records:** All content, interactions, blocks, and escalations logged and retained 3+ years

---

## Weekly Compliance Audit

Every Sunday, run:
```bash
python3 AUTOMATIONS/nsfw_safety_system.py --audit
python3 AUTOMATIONS/nsfw_safety_system.py --status
```

Review output at `OPS/NSFW_SAFETY_AUDIT.md`. Check:
- [ ] All blocked users logged correctly
- [ ] No unapproved content was posted
- [ ] All DM interactions used templates only
- [ ] Escalation log reviewed
- [ ] Revenue tracked in LEDGER
- [ ] Fanvue payout verified
