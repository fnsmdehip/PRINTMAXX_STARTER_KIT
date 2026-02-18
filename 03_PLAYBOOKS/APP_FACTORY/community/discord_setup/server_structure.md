# Discord server structure

Channel architecture, role hierarchy, and permissions setup.

---

## Channel architecture

### Minimal viable server (start here)

```
INFORMATION
├── #welcome (read-only, rules + intro)
├── #announcements (read-only)
└── #start-here (read-only, getting started guide)

COMMUNITY
├── #introductions (new member posts)
├── #general (main chat)
├── #wins (celebration channel)
└── #questions (help requests)

VOICE
└── #hangout (voice chat)
```

**Total: 7 channels.** Start here. Add more only when these overflow.

### Scaled server (500+ members)

```
INFORMATION
├── #welcome
├── #announcements
├── #rules
├── #start-here
└── #resources (links, guides)

COMMUNITY
├── #introductions
├── #general
├── #wins
├── #questions
├── #off-topic
└── #memes

FOCUS AREAS (niche-specific)
├── #beginners
├── #intermediate
├── #advanced
└── #accountability-groups

CHALLENGES
├── #current-challenge
├── #challenge-check-ins
└── #leaderboard

VOICE
├── #coworking
├── #hangout
└── #events

SUPPORT
├── #app-support
├── #feedback
└── #bug-reports

PREMIUM (role-gated)
├── #inner-circle
├── #exclusive-content
└── #direct-access
```

---

## Role hierarchy

### Basic structure

```
@Admin (you + trusted ops)
    |
@Moderator (community managers)
    |
@Ambassador (top contributors)
    |
@Premium (paid tier)
    |
@Verified (completed onboarding)
    |
@Member (joined, not verified)
```

### Role setup in Discord

1. **Server Settings > Roles**
2. Create roles in order (highest = most permissions)
3. Assign colors for visibility

### Recommended colors

| Role | Color hex | Visual |
|------|-----------|--------|
| Admin | #E74C3C | Red |
| Moderator | #9B59B6 | Purple |
| Ambassador | #F1C40F | Gold |
| Premium | #3498DB | Blue |
| Verified | #2ECC71 | Green |
| Member | #95A5A6 | Gray |

---

## Permissions matrix

### Channel permissions by role

| Channel | Member | Verified | Premium | Ambassador | Mod | Admin |
|---------|--------|----------|---------|------------|-----|-------|
| #welcome | View | View | View | View | View + Edit | All |
| #announcements | View | View | View | View | View + Post | All |
| #general | No | Post | Post | Post | Post + Manage | All |
| #introductions | No | Post | Post | Post | Manage | All |
| #wins | No | Post | Post | Post | Manage | All |
| #questions | No | Post | Post | Post | Manage | All |
| #premium-chat | No | No | Post | Post | Manage | All |
| #mod-chat | No | No | No | No | Post | All |

### Key permission settings

**@everyone (default role):**
- View Channels: No (lock by default)
- Send Messages: No
- Add Reactions: Yes
- Read Message History: Yes

**@Member:**
- View public channels: Yes
- Send Messages: No (until verified)

**@Verified:**
- Send Messages: Yes
- Attach Files: Yes
- Use External Emojis: Yes
- Create Threads: Yes

**@Moderator:**
- Manage Messages: Yes
- Kick Members: Yes
- Mute Members: Yes
- Manage Threads: Yes
- View Audit Log: Yes

**@Admin:**
- Administrator: Yes (full control)

---

## Verification system

### Option 1: Reaction role (simple)

1. In #welcome, post verification message
2. Users react with specific emoji
3. Bot assigns @Verified role

**Setup with Carl-bot:**
```
!reactionrole make
[Then follow prompts]
```

### Option 2: Introduction required (recommended)

1. New member joins with @Member role (can only see #welcome, #rules, #introductions)
2. They post introduction in #introductions
3. Mod/bot verifies and adds @Verified role

**Bot command (MEE6):**
Set up auto-mod to ping mods when new intro posted.

### Option 3: Agreement required

1. #rules channel with detailed rules
2. User must react to agree
3. Reaction triggers @Verified role

---

## Category setup

### How to create categories

1. Right-click channel list > Create Category
2. Name it (e.g., "COMMUNITY")
3. Drag channels into category
4. Set category permissions (channels inherit)

### Permission inheritance

Set permissions at category level. Channels inherit unless overridden.

Example: Make entire "PREMIUM" category only visible to @Premium role:
1. Edit category permissions
2. @everyone: View Channel = No
3. @Premium: View Channel = Yes

---

## Thread strategy

### When to use threads

- Long discussions that would clutter main channel
- Topic-specific Q&A
- Challenge check-ins
- Event discussions

### Thread settings

- Auto-archive: 1 week (keeps server clean)
- Thread permissions: Match parent channel
- Naming convention: [Topic] - Brief description

---

## Slow mode settings

| Channel type | Slow mode | Why |
|--------------|-----------|-----|
| #general | None | Conversation flow |
| #introductions | 30 min | Prevent spam |
| #wins | 1 hour | Quality over quantity |
| #questions | 5 min | Allow follow-ups |
| #off-topic | None | Let it flow |

---

## Channel descriptions

Write clear descriptions. Example:

**#wins**
> Share your victories, big or small. Completed a challenge? Hit a milestone? Post it here. We celebrate everything.

**#questions**
> Stuck on something? Ask here. No question too basic. Tag @Helper for faster response.

**#general**
> Main hangout. Chat about anything related to [topic]. Keep it friendly.

---

## Pinned messages

Every active channel needs:
1. **Purpose** - What this channel is for
2. **Rules** - Channel-specific guidelines
3. **Resources** - Helpful links

Example for #questions:
```
PIN 1: How to ask great questions
- Search first (use Discord search)
- Be specific (what you tried, what happened)
- Share context (screenshots help)

PIN 2: Frequently asked questions
[Link to FAQ or use Discord's FAQ feature]

PIN 3: Can't find help? Tag @Moderator
```

---

## Forum channels (Discord's built-in forums)

### When to use forums vs chat

**Use forums for:**
- Questions (searchable, organized)
- Feedback (threaded responses)
- Showcase (portfolio posts)
- Challenges (individual threads per participant)

**Use chat for:**
- Real-time discussion
- Quick questions
- Casual conversation

### Forum setup

1. Create channel > Select "Forum"
2. Add tags (e.g., "Question", "Solved", "Discussion")
3. Set guidelines post
4. Configure sort order (Latest Activity recommended)

---

## Server template

Save your setup as template for future servers:

1. Server Settings > Server Template
2. Create template
3. Share template link

**Warning:** Templates don't include:
- Messages
- Members
- Bots
- Webhooks

---

## Launch checklist

- [ ] Categories created
- [ ] Essential channels created (7 minimum)
- [ ] Roles created with correct hierarchy
- [ ] Permissions set at category level
- [ ] Verification system active
- [ ] #welcome message posted
- [ ] #rules posted
- [ ] Channel descriptions written
- [ ] Key channels have pinned messages
- [ ] Server icon and banner uploaded
- [ ] Vanity URL claimed (if eligible)
