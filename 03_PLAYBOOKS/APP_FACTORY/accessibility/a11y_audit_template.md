# Accessibility audit template

Use this template to audit each screen in your app.

---

## Audit information

| Field | Value |
|-------|-------|
| App name | |
| Version | |
| Auditor | |
| Date | |
| Platforms tested | iOS / Android |
| Devices | |
| Screen reader | VoiceOver / TalkBack |

---

## Screen audit

### Screen: [Screen name]

**Purpose:** [Brief description of what this screen does]

**URL/Route:** [Navigation path to reach this screen]

---

#### 1. Screen reader navigation

| Check | Pass | Fail | N/A | Notes |
|-------|------|------|-----|-------|
| Screen title announced on entry | | | | |
| All elements reachable via swipe | | | | |
| Reading order matches visual order | | | | |
| No duplicate announcements | | | | |
| All interactive elements focusable | | | | |

**Issues found:**
-

---

#### 2. Labels and descriptions

| Element | Has label | Label quality | Notes |
|---------|-----------|---------------|-------|
| [Button 1] | Yes/No | Good/Needs work | |
| [Button 2] | | | |
| [Image 1] | | | |
| [Input 1] | | | |
| [Icon 1] | | | |

**Label quality criteria:**
- Good: Clearly describes purpose/content
- Needs work: Vague, redundant, or missing context

**Issues found:**
-

---

#### 3. Touch targets

| Element | Size (points) | Meets 44x44 | Notes |
|---------|---------------|-------------|-------|
| [Button 1] | | Yes/No | |
| [Button 2] | | | |
| [Icon button] | | | |
| [Link] | | | |

**Issues found:**
-

---

#### 4. Color contrast

| Element | Foreground | Background | Ratio | Passes AA | Notes |
|---------|------------|------------|-------|-----------|-------|
| Body text | | | | Yes/No | |
| Heading | | | | | |
| Button text | | | | | |
| Link text | | | | | |
| Placeholder | | | | | |
| Error text | | | | | |

**Issues found:**
-

---

#### 5. State announcements

| Element | State | Announced | Notes |
|---------|-------|-----------|-------|
| [Toggle] | On/Off | Yes/No | |
| [Checkbox] | Checked | | |
| [Tab] | Selected | | |
| [Button] | Disabled | | |
| [Accordion] | Expanded | | |

**Issues found:**
-

---

#### 6. Dynamic content

| Update type | Live region | Announced | Notes |
|-------------|-------------|-----------|-------|
| Loading indicator | | Yes/No | |
| Error message | | | |
| Success message | | | |
| List update | | | |
| Counter change | | | |

**Issues found:**
-

---

#### 7. Forms (if applicable)

| Field | Label visible | Label linked | Error announced | Keyboard type | Autocomplete |
|-------|---------------|--------------|-----------------|---------------|--------------|
| [Email] | Yes/No | Yes/No | Yes/No | | |
| [Password] | | | | | |
| [Name] | | | | | |

**Form flow:**
- [ ] Can tab through all fields
- [ ] Can submit form
- [ ] Errors announced immediately
- [ ] Success feedback provided

**Issues found:**
-

---

#### 8. Motion and animations

| Animation | Respects reduce motion | Can be paused | Notes |
|-----------|------------------------|---------------|-------|
| Page transition | Yes/No | N/A | |
| Loading spinner | | | |
| Carousel | | | |
| Skeleton loader | | | |

**Issues found:**
-

---

#### 9. Media (if applicable)

| Media | Captions | Transcript | Controls accessible | Notes |
|-------|----------|------------|---------------------|-------|
| [Video 1] | Yes/No | Yes/No | Yes/No | |
| [Audio 1] | N/A | | | |

**Issues found:**
-

---

### Issues summary

#### Critical (blocks task completion)

| ID | Element | Issue | Recommendation |
|----|---------|-------|----------------|
| C1 | | | |
| C2 | | | |

#### Major (significant difficulty)

| ID | Element | Issue | Recommendation |
|----|---------|-------|----------------|
| M1 | | | |
| M2 | | | |

#### Minor (inconvenient but not blocking)

| ID | Element | Issue | Recommendation |
|----|---------|-------|----------------|
| m1 | | | |
| m2 | | | |

#### Enhancements

| ID | Element | Suggestion |
|----|---------|------------|
| E1 | | |
| E2 | | |

---

## Full app audit tracker

Track audit progress across all screens.

| Screen | Audited | Critical | Major | Minor | Status |
|--------|---------|----------|-------|-------|--------|
| Home | | | | | Not started / In progress / Complete |
| Login | | | | | |
| Register | | | | | |
| Profile | | | | | |
| Settings | | | | | |
| Product list | | | | | |
| Product detail | | | | | |
| Cart | | | | | |
| Checkout | | | | | |
| Order confirmation | | | | | |

---

## Remediation tracking

| Issue ID | Screen | Severity | Assignee | Status | PR/Commit |
|----------|--------|----------|----------|--------|-----------|
| C1 | | Critical | | Open / In progress / Resolved | |
| M1 | | Major | | | |
| m1 | | Minor | | | |

---

## Testing checklist (per release)

### Before QA

- [ ] All screens audited
- [ ] Critical issues resolved
- [ ] Major issues resolved or documented with workaround
- [ ] Automated accessibility tests passing

### QA testing

- [ ] VoiceOver end-to-end test (iOS)
- [ ] TalkBack end-to-end test (Android)
- [ ] Large font test (200% scale)
- [ ] Bold text test (iOS)
- [ ] Reduce motion test
- [ ] Dark mode test
- [ ] Color blindness simulation

### Sign-off

| Role | Name | Date | Approved |
|------|------|------|----------|
| Developer | | | Yes/No |
| QA | | | |
| Accessibility specialist | | | |
| Product owner | | | |

---

## Notes

[Any additional observations, recommendations, or context]

---

## Revision history

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | | | Initial audit |
| | | | |
