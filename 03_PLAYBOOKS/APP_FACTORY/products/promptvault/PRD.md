# PromptVault - Product Requirements Document

**App Name:** PromptVault
**Niche:** AI Tools (Prompt Engineering)
**Method:** AFM007 - Free Tier Extraction
**Monetization:** Freemium - Free tier + $19/mo Pro

---

## Overview

PromptVault is a prompt library and management tool. Free tier gives access to curated prompts. Pro tier adds AI-enhanced features: prompt improvement, custom prompt generation, and organization tools.

Core insight: AI is powerful but most people suck at prompting. Curated prompts solve 80% of use cases. Premium AI features solve the remaining 20%.

---

## Problem Statement

AI users struggle with:
1. Writing effective prompts from scratch
2. Remembering prompts that worked well
3. Finding quality prompts in scattered places
4. Adapting generic prompts to specific needs
5. Organizing prompts across different use cases

---

## Solution

### Free Tier (Lead Magnet)
- Access to 500+ curated, categorized prompts
- Copy-to-clipboard functionality
- Basic search and filter
- Favorite prompts locally

### Pro Tier ($19/mo)
- AI prompt improver (paste your prompt, get better version)
- Custom prompt generator (describe need, get prompt)
- Unlimited prompt organization (folders, tags)
- Prompt history and versioning
- Export to Notion/Sheets
- Early access to new prompts
- No ads

---

## User Stories (MVP - Single Context Window Implementable)

### US001: Browse Prompts (Free)
**As a** free user
**I want to** browse categorized prompts
**So that** I can find prompts for my use case

**Acceptance Criteria:**
- Display prompts in category grid
- Categories: Writing, Coding, Marketing, Analysis, Creative, Business
- Show prompt title and preview
- Tap to see full prompt
- Copy button for each prompt

**Implementation Notes:**
- Static JSON file with prompts
- Category filter chips
- Simple list UI
- Clipboard API for copy

---

### US002: Search Prompts (Free)
**As a** user
**I want to** search for specific prompts
**So that** I can quickly find what I need

**Acceptance Criteria:**
- Search bar at top
- Search by title and tags
- Results update as user types
- Clear search button
- "No results" state

**Implementation Notes:**
- Client-side search (fast)
- Debounce input
- Fuse.js for fuzzy search

---

### US003: Copy Prompt (Free)
**As a** user
**I want to** copy a prompt to clipboard
**So that** I can paste it into ChatGPT/Claude

**Acceptance Criteria:**
- One-tap copy button
- Visual feedback on copy
- "Copied!" toast notification
- Works on all prompts

**Implementation Notes:**
- Clipboard.setString()
- Haptic feedback
- Toast component

---

### US004: Favorite Prompts (Free)
**As a** free user
**I want to** save my favorite prompts
**So that** I can access them quickly

**Acceptance Criteria:**
- Heart icon on each prompt
- Favorites tab in navigation
- Persist favorites locally
- Unfavorite option

**Implementation Notes:**
- AsyncStorage for persistence
- Simple array of prompt IDs
- Filter view for favorites

---

### US005: Prompt Improver (Pro)
**As a** pro user
**I want to** improve my existing prompts
**So that** I get better AI responses

**Acceptance Criteria:**
- Input field for user's prompt
- "Improve" button
- Loading state while processing
- Display improved prompt
- Option to copy or save

**Implementation Notes:**
- API call to OpenAI/Claude
- Prompt template for improvement
- Rate limiting per user
- Error handling for API failures

---

### US006: Prompt Generator (Pro)
**As a** pro user
**I want to** generate prompts from descriptions
**So that** I can create prompts without expertise

**Acceptance Criteria:**
- Input: "What do you want to do?"
- Output: Generated prompt
- Option to refine with follow-up
- Save to personal library

**Implementation Notes:**
- API call with generation template
- Max 3 refinements per generation
- Save to user's prompts collection

---

### US007: Organize Prompts (Pro)
**As a** pro user
**I want to** organize prompts into folders
**So that** I can manage my prompt collection

**Acceptance Criteria:**
- Create/edit/delete folders
- Add prompts to folders
- Tag prompts with labels
- Filter by folder/tag
- Drag and drop reordering

**Implementation Notes:**
- User-generated folders in local storage
- Sync to cloud for cross-device (future)
- Simple folder structure

---

### US008: Freemium Paywall
**As a** new user
**I want to** see what Pro offers
**So that** I can decide whether to upgrade

**Acceptance Criteria:**
- Pro features locked with paywall overlay
- Clear comparison of Free vs Pro
- Multiple price options (monthly, annual)
- Free trial available (7 days)
- Restore purchases

**Implementation Notes:**
- RevenueCat integration
- Soft paywall (see feature, then prompted)
- 7-day trial with full Pro access

---

### US009: Prompt History (Pro)
**As a** pro user
**I want to** see my prompt history
**So that** I can reuse past improvements

**Acceptance Criteria:**
- List of all improved/generated prompts
- Timestamp for each
- Filter by date/type
- Delete history option

**Implementation Notes:**
- Store in local DB
- Paginated list
- Cloud sync for premium (future)

---

## Future Features (Post-MVP)

- **Prompt chains:** Multi-step prompts for complex tasks
- **Community prompts:** User submissions with voting
- **API access:** Use PromptVault from your apps
- **Chrome extension:** Insert prompts directly into ChatGPT
- **Team features:** Shared prompt libraries
- **Analytics:** Track which prompts perform best
- **Version control:** Track prompt iterations
- **Integrations:** Notion, Obsidian, Raycast

---

## MVP Feature Set

| Feature | Priority | Effort | Free | Pro |
|---------|----------|--------|------|-----|
| Browse prompts | P0 | Low | Yes | Yes |
| Search prompts | P0 | Low | Yes | Yes |
| Copy prompt | P0 | Low | Yes | Yes |
| Favorite prompts | P1 | Low | Yes | Yes |
| Prompt improver | P0 | Medium | No | Yes |
| Prompt generator | P0 | Medium | No | Yes |
| Organize prompts | P1 | Medium | No | Yes |
| Paywall | P0 | Low | - | - |
| Prompt history | P2 | Low | No | Yes |

---

## Monetization Structure

### Pricing
- **Free:** Core library access, basic features
- **Pro Monthly:** $19/mo
- **Pro Annual:** $99/yr (save 56%)

### Why Freemium
Unlike screen blockers (hard paywall works), prompt tools benefit from:
1. Free users spread word of mouth
2. AI/prompt market is crowded, need free entry point
3. Power users will pay for productivity gains
4. Free library is SEO traffic magnet

### Conversion Strategy
1. Free users discover value in library
2. Hit limitation (want to improve/generate)
3. Soft paywall shows Pro features
4. 7-day trial removes friction
5. Convert after trial shows value

### Target Metrics
- Free to trial: 15%
- Trial to paid: 25%
- Overall free to paid: ~4%

---

## Prompt Library Strategy

### Initial Library (500 prompts)

**Categories:**
| Category | Count | Examples |
|----------|-------|----------|
| Writing | 100 | Blog posts, emails, social media |
| Coding | 80 | Debug, explain, refactor |
| Marketing | 70 | Copy, ads, SEO |
| Analysis | 60 | Data, research, summaries |
| Creative | 50 | Stories, brainstorm, ideas |
| Business | 50 | Strategy, planning, proposals |
| Productivity | 40 | Tasks, notes, organization |
| Learning | 30 | Explain, teach, quiz |
| Career | 20 | Resume, interview, negotiation |

### Prompt Quality Criteria
- Tested with ChatGPT and Claude
- Clear instructions
- Includes context/constraints
- Produces consistent results
- Fills real use case

### Update Cadence
- 10 new prompts weekly
- Monthly category refresh
- User-requested prompts prioritized
- Seasonal/trending prompts added

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Daily Active Users (Free) | 1,000 | Analytics |
| Free to Trial | >15% | RevenueCat |
| Trial to Paid | >25% | RevenueCat |
| MRR | $5,000 (Month 3) | RevenueCat |
| Prompts copied/day | 500 | Analytics |
| Pro feature usage | 10+ uses/user/week | Analytics |
| App Store Rating | >4.5 | Reviews |
| Churn Rate | <10% monthly | RevenueCat |

---

## Launch Checklist

### Pre-Launch
- [ ] 500 prompts curated and organized
- [ ] AI improvement/generation working
- [ ] RevenueCat integration tested
- [ ] App Store screenshots
- [ ] Privacy policy
- [ ] TestFlight beta
- [ ] Landing page with waitlist

### Launch
- [ ] Submit to App Store
- [ ] Submit to Google Play
- [ ] Launch on Product Hunt
- [ ] Post on X/Twitter
- [ ] Reddit posts (r/ChatGPT, r/ClaudeAI)
- [ ] Email waitlist
- [ ] Influencer outreach

### Post-Launch (Week 1-4)
- [ ] Monitor reviews
- [ ] Respond to feedback
- [ ] Add requested prompts
- [ ] Optimize conversion
- [ ] Build Chrome extension
- [ ] Reach 1,000 free users

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Market saturation (many prompt apps) | High | High | Better curation, AI features differentiate |
| OpenAI API costs | Medium | Medium | Rate limiting, caching, efficient prompts |
| Users don't convert | Medium | High | Improve free->pro funnel, add more pro value |
| Prompts become outdated | Medium | Low | Regular updates, user feedback loop |
| AI providers change APIs | Low | Medium | Abstract AI layer, support multiple providers |

---

## Technical Requirements Summary

- **Platform:** Web (primary), iOS, Android
- **Framework:** Next.js (web), React Native (mobile)
- **Backend:** Supabase (auth, database)
- **AI API:** OpenAI GPT-4o-mini (cost-effective)
- **Payments:** Stripe (web), RevenueCat (mobile)
- **Analytics:** Mixpanel
- **Search:** Fuse.js (client-side)

---

## Appendix: Prompt Improvement System Prompt

```
You are a prompt engineering expert. Your task is to improve the user's prompt to get better results from AI assistants.

Analyze the given prompt and improve it by:
1. Adding clear context and constraints
2. Specifying the desired output format
3. Including relevant examples if helpful
4. Breaking complex requests into steps
5. Removing ambiguity

Keep the improved prompt concise but complete.

User's original prompt:
{user_prompt}

Improved prompt:
```

---

## Appendix: Prompt Generation System Prompt

```
You are a prompt engineering expert. Create an effective prompt based on the user's description of what they want to accomplish.

The prompt should:
1. Be specific and actionable
2. Include context and constraints
3. Specify desired output format
4. Be ready to copy-paste into ChatGPT or Claude

User's description:
{user_description}

Generated prompt:
```
