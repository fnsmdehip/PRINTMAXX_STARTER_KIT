# Share prompts: when and how to trigger sharing

Share prompts fail when they interrupt. They succeed when they amplify emotion.

---

## The share prompt framework

### Timing: when to prompt

**High-emotion moments (best)**
- Achievement unlocked
- Streak milestone hit
- Personal record broken
- Goal completed
- Challenge won

**Value-received moments (good)**
- Insight delivered
- Problem solved
- Session completed
- Progress shown

**Random/interruptive moments (avoid)**
- App open
- Mid-session
- After error
- During onboarding

### Emotion mapping

| Emotion | Trigger | Share Format |
|---------|---------|--------------|
| Pride | Achievement | "I just hit 30 days of meditation" |
| Excitement | Milestone | "100 workouts completed" |
| Gratitude | Help received | "This app helped me..." |
| Competition | Leaderboard | "Can you beat my score?" |
| Connection | Shared activity | "Join me in this challenge" |

---

## Share prompt copy that works

### Formula 1: Achievement + invitation

Bad: "Share your progress with friends!"
Good: "You just completed 7 days. Challenge a friend to beat you."

### Formula 2: Benefit + curiosity

Bad: "Tell others about this app"
Good: "Send your workout to your gym buddy" (they'll ask what app)

### Formula 3: Social proof + FOMO

Bad: "Invite friends to join"
Good: "1,247 people joined this challenge today. Add a friend before it closes."

### Copy templates by app type

**Fitness app**
- "You crushed it. Show your gym partner what 30 days looks like."
- "New PR: [weight] lb deadlift. Who can beat it?"
- "Challenge sent. They have 24 hours to accept."

**Meditation app**
- "7-day streak. Invite someone to start theirs."
- "You've meditated 10 hours total. Share your journey."
- "Start a meditation circle with friends."

**Prayer app**
- "Your prayer was supported by 12 people. Invite more."
- "Share this prayer request with your small group."
- "Start a prayer chain for [cause]."

**Habit tracker**
- "21-day streak. You've built a habit. Inspire someone else."
- "Accountability partner wanted: share this habit."
- "You completed [habit] 100 times. Post your win."

---

## Share prompt UX patterns

### Pattern 1: Inline share (non-blocking)

```
[Achievement card]
"30-day streak!"
[Continue] [Share]
```

User can dismiss without friction. Share is secondary action.

### Pattern 2: Celebration modal (blocking but earned)

```
[Full-screen celebration]
"You did it! 100 workouts completed."
[Image of badge/certificate]
[Share to Instagram] [Share to Stories] [Copy link]
[Maybe later]
```

Only use for major milestones. Always have dismiss option.

### Pattern 3: Embedded sharing (best)

Share is part of the feature, not a prompt.

- Workout complete: auto-generates shareable card
- Challenge: requires sharing to start
- Leaderboard: tap name to share comparison

### Pattern 4: Post-session summary

```
Session complete
- Duration: 15 min
- Calories: 180
- Streak: 12 days

[Share summary] [Done]
```

Share is natural next step after reviewing stats.

---

## Share content formats

### What to include in share content

| Element | Purpose | Example |
|---------|---------|---------|
| Metric | Proof | "30 days" |
| Visual | Attention | Badge/chart image |
| Personal touch | Authenticity | User's name or avatar |
| CTA | Conversion | "Join me" |
| App branding | Attribution | Small logo, no domination |

### Platform-specific formats

**Instagram Stories**
- Vertical (9:16)
- Bold metric as hero
- Minimal text
- Sticker-style graphics
- "Add yours" prompt

**Twitter/X**
- Horizontal or square
- Metric + one-liner
- No hashtag spam (1-2 max)
- Thread-friendly for longer achievements

**iMessage/WhatsApp**
- Link preview optimized
- Personal message template
- Deep link to specific content

**TikTok**
- Video format preferred
- Before/after if applicable
- Sound-on design

---

## Share prompt frequency rules

### Limits

- Max 1 share prompt per session
- Max 3 share prompts per week
- Never prompt on first session
- Never prompt after failed action

### Escalation

| User Behavior | Prompt Level |
|---------------|--------------|
| First milestone | Subtle inline |
| Repeated engagement | Modal with value |
| High streak | Premium share content |
| Referred others before | Priority prompt |

---

## Measuring share prompt performance

### Metrics to track

1. **Prompt display rate** - How often prompts show
2. **Share tap rate** - % who tap share button
3. **Share complete rate** - % who actually share
4. **Referral conversion** - % of shares that convert
5. **Viral coefficient** - Shares x conversion rate

### Benchmarks

| Metric | Poor | Average | Good |
|--------|------|---------|------|
| Share tap rate | <2% | 5% | 10%+ |
| Share complete rate | <20% | 40% | 60%+ |
| Referral conversion | <1% | 3% | 8%+ |

### A/B test priorities

1. Timing (which moment)
2. Copy (what words)
3. Visual (what image)
4. CTA (what button)
5. Frequency (how often)

---

## Anti-patterns to avoid

1. **Share-gating** - Don't block features behind sharing
2. **Fake urgency** - "Share now or lose progress"
3. **Spam requests** - Multiple prompts per session
4. **Generic content** - "I'm using this app"
5. **No value for receiver** - Share must benefit both parties
6. **Ignoring platform norms** - Each platform has different expectations

---

## Implementation checklist

- [ ] Identify top 3 emotional moments in your app
- [ ] Create share-worthy content for each moment
- [ ] Design platform-specific share formats
- [ ] Implement share tracking (prompt > tap > complete > convert)
- [ ] Set frequency caps
- [ ] A/B test copy and timing
- [ ] Track viral coefficient weekly
