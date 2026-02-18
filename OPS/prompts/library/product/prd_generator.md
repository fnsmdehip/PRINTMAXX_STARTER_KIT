# PRD Generator

Generate product requirements documents for features and products. Outputs structured, actionable specs.

---

## System prompt

```
You are a product manager creating PRDs for solopreneur products. You write clear, actionable specs that a developer (or you building it yourself) can implement.

Approach:
- Start with the problem and user value
- Be specific about requirements
- Include acceptance criteria
- Keep scope minimal for V1
- Separate must-haves from nice-to-haves

Output format:
- Clear section headers
- Bullet points for requirements
- User stories in standard format
- Edge cases documented
- Out of scope explicitly stated
```

---

## User prompt template

```
Generate a PRD for [FEATURE/PRODUCT].

Product context:
- Product: [PRODUCT]
- Target user: [USER]
- Business goal: [GOAL]

Feature details:
- Feature name: [NAME]
- Problem it solves: [PROBLEM]
- Proposed solution: [SOLUTION - high level]

Constraints:
- Timeline: [TIMELINE]
- Resources: [RESOURCES - solo dev, small team]
- Tech stack: [STACK]

What to include:
- [ ] User stories
- [ ] Acceptance criteria
- [ ] Edge cases
- [ ] Out of scope
- [ ] Technical considerations
- [ ] Success metrics
```

---

## Example output

**Input:**
```
Generate a PRD for a lead capture form.

Product context:
- Product: PRINTMAXX landing site
- Target user: Solopreneurs interested in content automation
- Business goal: Capture email leads for nurture sequence

Feature details:
- Feature name: Lead capture form with lead magnet
- Problem it solves: Visitors leave without way to contact them
- Proposed solution: Email form that delivers free resource

Constraints:
- Timeline: 1 week
- Resources: Solo developer
- Tech stack: Next.js, CSV storage (no database)

What to include:
- [x] User stories
- [x] Acceptance criteria
- [x] Edge cases
- [x] Out of scope
- [x] Technical considerations
- [x] Success metrics
```

**Output:**

```
# PRD: Lead capture form with lead magnet

## Overview

### Problem statement
Visitors land on PRINTMAXX site, get value from content, but leave without any way for us to follow up. We lose potential customers because we can't nurture them over time.

### Solution summary
A simple email capture form that:
1. Collects visitor email
2. Delivers a free resource (lead magnet)
3. Saves contact to our lead list

### Success criteria
- Form loads on all truth pages
- Submissions save to LEDGER/leads.csv
- User receives lead magnet link immediately
- Form converts at 3%+ of page visitors

---

## User stories

### Primary user story
**As a** visitor who found value in the content,
**I want to** get a free resource in exchange for my email,
**So that** I can learn more about automating my content.

### Secondary user stories

**US-01:** As a visitor, I want confirmation my signup worked so I know the resource is coming.

**US-02:** As a visitor, I want to know what I'm signing up for before submitting my email.

**US-03:** As the site owner, I want leads saved to a central file so I can follow up later.

**US-04:** As the site owner, I want to see when each lead signed up and from which page.

---

## Requirements

### Functional requirements

**FR-01: Email input**
- Single email field
- Standard email validation (contains @, valid format)
- Placeholder text: "Enter your email"
- Required field

**FR-02: Submit button**
- Clear CTA text (e.g., "Get free guide")
- Loading state while processing
- Disabled while submitting

**FR-03: Lead magnet description**
- Brief description of what they'll receive
- Located above or beside the form
- No more than 2 sentences

**FR-04: Success state**
- Clear confirmation message
- Link to lead magnet (or promise it's in their inbox)
- Option to share on social (optional V2)

**FR-05: Data storage**
- Save to LEDGER/leads.csv
- Fields: email, timestamp, source_page, utm_source (if present)
- Append to existing file, don't overwrite

**FR-06: Page integration**
- Form appears on all truth pages
- Consistent placement (end of content or sidebar)
- Responsive design

### Non-functional requirements

**NFR-01: Performance**
- Form renders in under 100ms
- Submission completes in under 2 seconds

**NFR-02: Accessibility**
- Form fields have proper labels
- Error messages are screen-reader friendly
- Keyboard navigable

**NFR-03: Security**
- Basic spam protection (honeypot field)
- Rate limiting (max 10 submissions per IP per hour)
- No sensitive data stored

---

## Acceptance criteria

### AC-01: Successful submission
- Given a visitor on a truth page
- When they enter a valid email and click submit
- Then their email is saved to leads.csv with timestamp and page source
- And they see a success message with lead magnet access

### AC-02: Invalid email handling
- Given a visitor enters an invalid email format
- When they click submit
- Then they see an error message: "Please enter a valid email"
- And the form is not submitted

### AC-03: Duplicate handling
- Given a visitor submits an email already in leads.csv
- When the form processes
- Then the submission is accepted (still save timestamp for re-engagement)
- And they see the normal success message

### AC-04: Empty submission
- Given a visitor clicks submit without entering email
- When the form validates
- Then they see error: "Email is required"
- And the form is not submitted

### AC-05: CSV format
- Given a new lead submission
- When saved to leads.csv
- Then the row contains: email,timestamp,source_page,utm_source
- And timestamp is ISO 8601 format

---

## Edge cases

| Scenario | Handling |
|----------|----------|
| User submits twice rapidly | Dedupe within 5 seconds, accept only first |
| CSV file doesn't exist | Create with headers on first submission |
| CSV is locked/busy | Retry once after 100ms, then fail gracefully |
| Very long email (>254 chars) | Reject with validation error |
| Email with plus sign (user+tag@example.com) | Accept as valid |
| JavaScript disabled | Show fallback message with manual contact option |
| Bot submission | Honeypot catches most, rate limit handles rest |

---

## Out of scope (V1)

- Email verification/double opt-in
- CRM integration
- Automated email sending
- A/B testing different forms
- Pop-up or exit-intent triggers
- Multi-step forms
- Additional fields (name, company, etc.)

These can be added in V2 after validating the basic form works.

---

## Technical considerations

### Implementation approach
```
1. Create form component in components/forms/LeadCaptureForm.tsx
2. API route at app/api/leads/route.ts for processing
3. CSV helper in lib/leads.ts for file operations
4. Styling with existing design system
```

### Data flow
```
User submits form
  → Client validates email format
  → POST to /api/leads
  → Server validates email
  → Append to LEDGER/leads.csv
  → Return success response
  → Client shows confirmation
```

### CSV structure
```
email,timestamp,source_page,utm_source
user@example.com,2024-01-15T10:30:00Z,/truth/automation-myth,twitter
```

### Spam protection
- Honeypot field (hidden, if filled = bot)
- Rate limit by IP
- Basic email format validation

### Error handling
- Network error: "Something went wrong. Try again."
- Validation error: Specific field error
- Server error: Log error, show generic message

---

## Success metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Conversion rate | 3%+ | Submissions / page views |
| Form completion time | <10 seconds | Analytics timing |
| Error rate | <1% | Failed submissions / total attempts |
| Lead quality | TBD | Open rate of follow-up emails |

### Tracking implementation
- Page view: existing analytics
- Form impression: track when form enters viewport
- Form submission: success event with source page

---

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Design | 1 day | Form mockup and copy |
| Build | 2 days | Working form component |
| Test | 1 day | Edge cases and mobile |
| Deploy | 0.5 days | Push to production |
| Monitor | Ongoing | Check conversion and errors |

Total: 4-5 days

---

## Open questions

1. What is the lead magnet? (Need specific resource to link to)
2. Should we send an email or just show a download link?
3. Do we want utm tracking for attribution?

**Decision needed before build:** Lead magnet asset must be ready.
```

---

## Variations

### Feature PRD (within existing product)
```
Generate a PRD for [FEATURE] in [EXISTING PRODUCT].

Focus on:
- How it integrates with existing functionality
- Impact on current user flows
- Technical dependencies
- Migration or rollout considerations
```

### MVP PRD (new product)
```
Generate an MVP PRD for [NEW PRODUCT].

Focus on:
- Core value proposition
- Minimum feature set to validate
- What NOT to build yet
- Launch criteria
```

### Technical spec PRD
```
Generate a technical PRD for [FEATURE].

Include:
- Architecture decisions
- Data models
- API contracts
- Integration points
- Performance requirements
```

---

## Quality checklist

- [ ] Problem clearly stated
- [ ] User stories cover main scenarios
- [ ] Acceptance criteria are testable
- [ ] Edge cases documented
- [ ] Out of scope explicitly listed
- [ ] Technical approach outlined
- [ ] Success metrics defined
- [ ] Timeline realistic
- [ ] Open questions identified
- [ ] Would a developer know what to build?
