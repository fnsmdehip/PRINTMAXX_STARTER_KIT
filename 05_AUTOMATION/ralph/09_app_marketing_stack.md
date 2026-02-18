# Ralph Task: App Marketing Stack

Create full marketing infrastructure for each app: social content, email, ads, affiliates.

---

## Context

Read these files before starting:
- `MONEY_METHODS/APP_FACTORY/APP_LAUNCH_FULL_STACK.md` - Launch checklist
- `MONEY_METHODS/APP_FACTORY/GREY_HAT_COMPLIANCE_PLAYBOOK.md` - Edge tactics
- `MONEY_METHODS/APP_FACTORY/AFFILIATE_SOURCES_MASTER.md` - Affiliate programs
- `CONTENT/social/` - Content templates by niche
- `CONTENT/email_sequences/` - Email templates

Output to:
- `MONEY_METHODS/APP_FACTORY/marketing/[app-name]/`
- `LEDGER/CONTENT_QUEUE.csv`

---

## Success Criteria

### Step 1: Social content batch

For each app, create:

**TikTok/Reels (30 pieces):**
1. [ ] 10 problem/solution hooks
2. [ ] 10 feature demos
3. [ ] 5 behind-the-scenes
4. [ ] 5 testimonial-style

**X/Twitter (50 posts):**
5. [ ] 20 tips related to app's problem
6. [ ] 15 engagement posts
7. [ ] 10 feature teasers
8. [ ] 5 launch posts

**Threads (10 pieces):**
9. [ ] 3 educational how-to threads
10. [ ] 3 problem deep-dives
11. [ ] 2 comparison threads
12. [ ] 2 story threads

### Step 2: Email sequences

13. [ ] Welcome sequence (7 emails)
14. [ ] Launch sequence (5 emails)
15. [ ] Nurture sequence (4 emails)
16. [ ] Win-back sequence (3 emails)

### Step 3: Ad creative

**TikTok Ads:**
17. [ ] 5 UGC-style scripts
18. [ ] 3 product demo scripts
19. [ ] 2 testimonial scripts

**Meta Ads:**
20. [ ] 5 static image concepts
21. [ ] 3 video ad scripts
22. [ ] 2 carousel concepts

**Apple Search Ads:**
23. [ ] 20 target keywords
24. [ ] 10 competitor keywords
25. [ ] Bid recommendations

### Step 4: Affiliate materials

26. [ ] Affiliate landing page copy
27. [ ] Commission structure recommendation
28. [ ] Marketing assets for affiliates:
    - [ ] Banner images (3 sizes)
    - [ ] Social post templates
    - [ ] Email swipe copy
29. [ ] List of affiliate programs to join (from AFFILIATE_SOURCES_MASTER.md)

### Step 5: Landing page

30. [ ] Hero section copy
31. [ ] Feature sections (3-5)
32. [ ] Social proof section
33. [ ] FAQ content (10 questions)
34. [ ] CTA copy variations

### Step 6: PR/outreach

35. [ ] Press release template
36. [ ] Podcast pitch template
37. [ ] Influencer outreach template
38. [ ] Partnership outreach template
39. [ ] List of 50 outreach targets

---

## Output Structure

```
MONEY_METHODS/APP_FACTORY/marketing/prayerlock/
├── social/
│   ├── tiktok/
│   │   ├── problem_solution_01.md
│   │   └── ...
│   ├── twitter/
│   │   ├── tips_01.md
│   │   └── ...
│   └── threads/
│       ├── educational_01.md
│       └── ...
├── email/
│   ├── welcome_sequence.md
│   ├── launch_sequence.md
│   ├── nurture_sequence.md
│   └── winback_sequence.md
├── ads/
│   ├── tiktok_scripts.md
│   ├── meta_concepts.md
│   └── aso_keywords.md
├── affiliate/
│   ├── landing_page.md
│   ├── commission_structure.md
│   ├── assets/
│   └── target_programs.md
├── landing/
│   ├── hero.md
│   ├── features.md
│   ├── social_proof.md
│   └── faq.md
└── outreach/
    ├── press_release.md
    ├── podcast_pitch.md
    ├── influencer_template.md
    └── targets_list.csv
```

---

## Content Calendar Template

```csv
day,platform,content_type,file_path,status
Mon,TikTok,tutorial,social/tiktok/tutorial_01.md,scheduled
Mon,Twitter,tip,social/twitter/tip_01.md,scheduled
Tue,TikTok,testimonial,social/tiktok/testimonial_01.md,draft
...
```

---

## Niche-specific content angles

### Faith apps (PrayerLock)

**Pain points:**
- Want to pray more but get distracted
- Feel guilty about phone time
- Morning routine disrupted by notifications

**Hooks:**
- "I couldn't pray for 5 minutes without checking my phone"
- "This app blocks everything until you pray"
- "My morning devotional streak is now 47 days"

**Testimonial angles:**
- Renewed relationship with God
- Finally consistent prayer habit
- Family noticed the change

### Fitness apps (WalkToUnlock)

**Pain points:**
- Sedentary lifestyle
- Phone addiction
- Can't stick to movement goals

**Hooks:**
- "I have to walk 1000 steps to unlock Instagram"
- "Lost 15 lbs because my phone made me walk"
- "Gamified getting off the couch"

**Testimonial angles:**
- Weight loss
- More energy
- Better sleep
- Phone time down

---

## Guardrails

### Content style
- Follow `.claude/rules/copy-style.md`
- No em dashes
- No banned AI vocabulary
- Specific numbers
- Direct voice

### Compliance
- FTC disclosure on sponsored content
- No unsubstantiated health claims
- No fake testimonials
- AI disclosure where required

### Grey hat limits
- Bio-only disclosure acceptable for affiliate
- Don't claim AI personas are human
- Don't make income claims without data

---

## Integration points

### Queue for posting
Add to `LEDGER/CONTENT_QUEUE.csv`:
```csv
id,app,platform,content_path,scheduled_date,status,account
1,prayerlock,tiktok,marketing/prayerlock/social/tiktok/hook_01.md,2026-01-25,queued,@prayerlock
```

### Integration with daily research
Check `LEDGER/ALPHA_STAGING.csv` for:
- New content formats performing well
- Platform algorithm changes
- Competitor tactics to adapt

---

## A/B testing framework

For each content type, create variations:

**Hook variations:**
- Question hook
- Statement hook
- Story hook
- Statistic hook

**CTA variations:**
- Soft CTA ("link in bio")
- Direct CTA ("download now")
- Social proof CTA ("join 10k users")
- Urgency CTA ("limited time")

Track performance and iterate.

---

## After Completion

1. Update `.ralph/progress.md`
2. Add content to `LEDGER/CONTENT_QUEUE.csv`
3. Create calendar in `marketing/[app]/content_calendar.csv`
4. Note any blockers

---

test_command: "ls MONEY_METHODS/APP_FACTORY/marketing/*/social/tiktok/*.md | wc -l"
