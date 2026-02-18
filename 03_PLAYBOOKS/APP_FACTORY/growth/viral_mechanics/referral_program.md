# Referral program: structure and rewards

A referral program is a system that rewards users for bringing new users. Done right, it's your cheapest acquisition channel.

---

## Referral program anatomy

### Core components

1. **Referrer reward** - What the inviter gets
2. **Referee reward** - What the new user gets
3. **Trigger action** - When rewards unlock
4. **Distribution mechanism** - How invites spread
5. **Tracking system** - Attribution and fraud prevention

### The reward equation

Total reward = Referrer reward + Referee reward
This total must be less than your CAC from paid channels.

Example:
- Paid CAC: $5
- Referral reward budget: $4
- Split: $2 referrer + $2 referee
- Profit: $1 per referral vs paid

---

## Reward types

### Monetary rewards

| Type | Pros | Cons |
|------|------|------|
| Cash | High motivation | Attracts fraud |
| App credit | Lower fraud | Less exciting |
| Subscription time | High value, low cost | Only for paid apps |
| Gift cards | Flexible | Tax implications |

### In-app rewards

| Type | Pros | Cons |
|------|------|------|
| Premium features | High perceived value | May cannibalize revenue |
| Virtual currency | Scalable | Requires economy design |
| Exclusive content | Unique value | Content cost |
| Status/badges | Zero marginal cost | Lower motivation |

### Reward selection by app type

| App Type | Referrer Reward | Referee Reward |
|----------|-----------------|----------------|
| Subscription fitness | 1 month free | 7-day extended trial |
| Freemium meditation | Premium week | Premium week |
| Prayer app | Exclusive prayers | Welcome bundle |
| Habit tracker | Pro features unlock | Extended trial |

---

## Reward structures

### Single-sided (referrer only)

Referrer gets reward. Referee gets nothing extra.

Best for: Apps with strong organic value prop
Example: "Invite friends, get $5 credit"

### Double-sided (both rewarded)

Both parties benefit. Higher conversion, higher cost.

Best for: Apps needing conversion boost
Example: "Give $5, get $5"

### Tiered rewards

Rewards increase with more referrals.

| Referrals | Reward |
|-----------|--------|
| 1 | 1 week premium |
| 3 | 1 month premium |
| 10 | 1 year premium |
| 25 | Lifetime access |

Best for: Apps with power users
Caution: Can attract gaming/fraud

### Milestone-based

Reward unlocks when referee reaches milestone.

Example: "Get $10 when your friend completes 7 workouts"

Best for: High-LTV apps where early retention matters
Benefit: Ensures quality referrals

---

## Trigger actions

### When to credit rewards

| Trigger | Pros | Cons |
|---------|------|------|
| Install | Simple, fast | High fraud risk |
| Signup | Verified user | Still gameable |
| Activation | Quality signal | Delayed gratification |
| First purchase | Highest quality | Very delayed |
| Day 7 retention | Strong signal | Complex tracking |

### Recommended triggers by model

| Business Model | Trigger | Rationale |
|----------------|---------|-----------|
| Subscription | First payment | Ensures paying customer |
| Freemium | 7-day retention | Ensures engaged user |
| One-time purchase | Purchase | Direct revenue link |
| Ad-supported | Day 3 retention | Ensures ad revenue potential |

---

## Referral mechanics

### Code-based

User shares unique code. Referee enters at signup.

Pros: Simple to implement
Cons: Friction to enter code

Implementation:
```
Code: JOHN2024
"Enter friend's code for bonus"
```

### Link-based

User shares tracked URL. Attribution automatic.

Pros: Zero friction
Cons: Link can be shared publicly (fraud risk)

Implementation:
```
yourapp.com/invite/abc123
Opens app store with attribution
```

### Contact-based

User selects contacts. App sends invite.

Pros: Personal, higher conversion
Cons: Permission required, spam concerns

Implementation:
```
"Select friends to invite"
[Contact picker]
Sends personalized SMS/email
```

### In-app invite

Referee must join specific feature (challenge, group).

Pros: Context-rich, natural
Cons: Limits use cases

Implementation:
```
"Add partner to challenge"
[Share link or pick contact]
```

---

## Referral flow design

### Optimal flow for referrer

1. Complete high-emotion action (workout, milestone)
2. See referral prompt with clear value
3. One-tap share to preferred platform
4. Track pending referrals in-app
5. Get notified when reward unlocks

### Optimal flow for referee

1. Receive personal invite (not mass blast)
2. Clear value prop: what they get
3. Frictionless signup (social login)
4. See friend connection in app
5. Reward delivered immediately

---

## Fraud prevention

### Common fraud patterns

1. **Self-referral** - Creating fake accounts
2. **Referral rings** - Groups gaming system
3. **Incentivized installs** - Paying for fake signups
4. **Device farms** - Mass fake device creation

### Prevention tactics

| Tactic | Prevents |
|--------|----------|
| Device fingerprinting | Self-referral, farms |
| Phone verification | Fake accounts |
| Delayed rewards | Incentivized installs |
| Behavioral scoring | All fraud types |
| Reward caps | Abuse scaling |

### Recommended limits

- Max 10 referrals rewarded per month
- Max 50 referrals rewarded lifetime
- 7-day delay for cash rewards
- Phone verification for cash-out

---

## Referral program metrics

### Key metrics

1. **Participation rate** - % of users who refer
2. **Invites per referrer** - Sharing activity
3. **Conversion rate** - Invites to signups
4. **Viral coefficient** - Referrals per user
5. **Referral CAC** - Total cost per acquired user

### Benchmarks

| Metric | Poor | Average | Good |
|--------|------|---------|------|
| Participation rate | <1% | 3% | 8%+ |
| Invites per referrer | <2 | 4 | 8+ |
| Conversion rate | <5% | 15% | 30%+ |
| Viral coefficient | <0.1 | 0.25 | 0.5+ |

### Tracking setup

Track these events:
- `referral_prompt_shown`
- `referral_share_tapped`
- `referral_share_completed`
- `referral_link_clicked`
- `referral_signup_completed`
- `referral_activated` (trigger met)
- `referral_reward_given`

---

## Referral program examples

### Dropbox (classic)

- Referrer: 500MB storage
- Referee: 500MB storage
- Trigger: Signup
- Result: 3900% growth in 15 months

Why it worked: Storage was expensive, free space was valuable.

### Uber

- Referrer: $20 credit
- Referee: $20 off first ride
- Trigger: First ride completed

Why it worked: High LTV justified high reward.

### Robinhood

- Referrer: Free stock
- Referee: Free stock
- Trigger: Account funded

Why it worked: Gamified with mystery stock value.

---

## Launch checklist

### Pre-launch

- [ ] Define reward structure (type, amount, trigger)
- [ ] Build tracking infrastructure
- [ ] Implement fraud prevention
- [ ] Create referral dashboard
- [ ] Design share assets (images, copy)
- [ ] Set up attribution

### Launch

- [ ] Soft launch to power users
- [ ] Monitor for fraud signals
- [ ] Gather feedback on flow
- [ ] Optimize share copy based on data
- [ ] Scale to full user base

### Ongoing

- [ ] Weekly metrics review
- [ ] Monthly fraud audit
- [ ] Quarterly reward optimization
- [ ] A/B test continuously

---

## Common mistakes

1. **Reward too small** - Not worth the social capital
2. **Reward too big** - Attracts fraud, unsustainable
3. **Delayed reward** - Referrer forgets and churns
4. **Hidden program** - Users don't know it exists
5. **No referee benefit** - Converts poorly
6. **No fraud prevention** - Bankrupts the program
7. **One-time push** - Needs ongoing promotion
