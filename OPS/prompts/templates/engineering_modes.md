# Engineering Modes for Claude

**Source:** Extracted from `hyper rat soft engin.rtf`
**Last Updated:** 2026-01-21
**Use Case:** Structured approaches for planning, debugging, and code review

---

## Planner Mode

When entering "Planner Mode", follow this sequence:

1. **Analyze the request** - Reflect on changes being asked
2. **Map existing code** - Understand current architecture and dependencies
3. **Ask clarifying questions** - 4-6 specific questions based on findings
4. **Draft plan** - Create comprehensive action plan after questions answered
5. **Get approval** - Wait for user approval before implementing
6. **Execute with updates** - After each phase, state what was completed and what's next

### Planner Mode Output Format

```markdown
## Analysis
[Brief summary of what's being requested]

## Current State
[Relevant files/architecture identified]

## Clarifying Questions
1. [Question about scope]
2. [Question about approach]
3. [Question about constraints]
4. [Question about edge cases]

## Proposed Plan (after questions answered)
### Phase 1: [Name]
- [ ] Step 1
- [ ] Step 2

### Phase 2: [Name]
- [ ] Step 1
- [ ] Step 2

## Risks & Mitigations
- Risk: [X] → Mitigation: [Y]
```

---

## Debugger Mode

When entering "Debugger Mode", follow this exact sequence:

1. **Hypothesize** - Reflect on 5-7 possible sources of the problem
2. **Narrow down** - Distill to 1-2 most likely sources
3. **Add logging** - Add logs to validate assumptions and track data flow
4. **Gather evidence** - Check console logs, errors, network logs
5. **Analyze** - Produce comprehensive analysis of the issue
6. **Iterate** - Suggest additional logs if source not clear
7. **Fix** - Implement fix once source confirmed
8. **Clean up** - Ask for approval to remove added logs

### Debugger Mode Output Format

```markdown
## Potential Sources (5-7)
1. [Hypothesis 1]
2. [Hypothesis 2]
3. [Hypothesis 3]
4. [Hypothesis 4]
5. [Hypothesis 5]

## Most Likely (1-2)
1. [Primary hypothesis] - because [evidence]
2. [Secondary hypothesis] - because [evidence]

## Logging Strategy
- Add log at [location] to check [assumption]
- Add log at [location] to track [data transformation]

## Analysis After Logs
[What the logs revealed]

## Fix
[Proposed fix with rationale]

## Cleanup
Ready to remove debug logs? [y/n]
```

---

## Security Review Checklist

Use when reviewing code for security issues:

### Configuration Security
- [ ] No secrets in code
- [ ] No secrets in version control
- [ ] No hardcoded credentials

### Authentication & Authorization
- [ ] Authentication checks present where needed
- [ ] Authorization patterns correct
- [ ] Principle of least privilege followed

### Data Protection
- [ ] Sensitive data encrypted
- [ ] Input validation present
- [ ] Output encoding (XSS prevention)
- [ ] Parameterized queries (SQL injection prevention)

### API Security
- [ ] Rate limiting implemented
- [ ] Error handling doesn't leak info
- [ ] Input validation on all endpoints

### Logging
- [ ] No sensitive info in logs
- [ ] Error logging present

### Dependencies
- [ ] No known vulnerabilities (`npm audit`)
- [ ] No unnecessary dependencies

### Resilience
- [ ] Error handling present
- [ ] Timeout configurations set
- [ ] No obvious DoS vectors

---

## PR Creation Workflow

When creating PRs via CLI:

```bash
# 1. Check status
git status

# 2. Stage changes (if needed)
git add .

# 3. Commit (if needed)
git commit -m "commit message"

# 4. Push (if needed)
git push

# 5. Check branch
git branch

# 6. Log changes vs main
git log main..$(git branch --show-current)

# 7. Check changed files
git diff --name-status main

# 8. Create PR
gh pr create --title "Title" --body "Description"
```

**Note:** PR body should be single line, no newlines.

---

## Code Quality Principles

### File Management
- When file > 300 lines, consider splitting
- When function > 50 lines, consider splitting
- One concern per file

### After Writing Code
Reflect on:
1. **Scalability** - Will this handle 10x load?
2. **Maintainability** - Can someone else understand this?
3. **Testability** - Can this be unit tested?

Produce 1-2 paragraph analysis and suggest improvements.

### PRD Handling
- Read PRD files for reference only
- Don't modify PRD files unless asked
- Use PRDs for structure examples

---

## When to Use Each Mode

| Situation | Mode |
|-----------|------|
| New feature implementation | Planner Mode |
| Bug report from user | Debugger Mode |
| Code review request | Security Review |
| PR creation | PR Workflow |
| Refactoring request | Planner Mode |
| Performance issue | Debugger Mode |

---

## Related Files

- `.claude/rules/security.md` - Full security guidelines
- `.claude/rules/code-style.md` - Code style rules
- `OPS/RALPH_LOOP_GUIDE.md` - Autonomous task execution
