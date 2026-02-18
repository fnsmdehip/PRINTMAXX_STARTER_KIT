# Ralph Guardrails

Learned constraints. Each iteration reads this first.

---

## Content Rules (Always Apply)

### Sign: No em dashes in any content
- Trigger: Writing any text content
- Instruction: Use commas or periods, never —
- Source: copy-style.md

### Sign: No banned AI vocabulary
- Trigger: Writing any content
- Instruction: Never use: leverage, utilize, delve, comprehensive, robust, innovative, seamless, game-changer, unlock, empower, cutting-edge, additionally, furthermore
- Source: copy-style.md

### Sign: Specific numbers over vague claims
- Trigger: Making any claim
- Instruction: Use real numbers ("saved 5 hours") not vague ("saved time")
- Source: copy-style.md

### Sign: Start with conclusion
- Trigger: Writing paragraphs
- Instruction: Lead with the point, details follow
- Source: copy-style.md

### Sign: Posts must be < 280 chars for X
- Trigger: Writing X/Twitter posts
- Instruction: Check character count, rewrite if over
- Source: Platform limit

---

## File Operation Rules

### Sign: Verify file exists before editing
- Trigger: Using Edit tool
- Instruction: Read file first, or use Write for new files
- Added after: Common error pattern

### Sign: Use absolute paths
- Trigger: Any file operation
- Instruction: Always use /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/...
- Added after: Path resolution errors

### Sign: Create directories before writing
- Trigger: Writing to new location
- Instruction: mkdir -p the parent directory first
- Added after: Directory not found errors

---

## Output Rules

### Sign: Save to correct location
- Trigger: Generating content
- Instruction: Check task spec for exact output path
- Source: Task requirements

### Sign: Use individual files for batches
- Trigger: Generating multiple pieces
- Instruction: One file per piece, numbered (001.md, 002.md...)
- Source: Review workflow

### Sign: Include metadata in content files
- Trigger: Creating content files
- Instruction: Add frontmatter with type, target_platform, generated_date
- Source: Tracking requirements

---

## API/Automation Rules

### Sign: Random delays between actions
- Trigger: Writing automation code
- Instruction: Add random.uniform(30, 180) between API calls
- Source: Anti-ban strategy

### Sign: One proxy per account
- Trigger: Writing proxy configuration
- Instruction: Never share proxies between accounts
- Source: PROXY_COMPARISON.md

### Sign: Rate limits
- Trigger: Writing posting scripts
- Instruction: X: 10-15 posts/day, TikTok: 3-5/day, IG: 1-3/day
- Source: MASTER_AUTOMATION_PLAN.md

---

## Quality Gates

### Sign: Test before commit
- Trigger: Writing code
- Instruction: Run test_command from task spec before marking complete
- Source: Ralph methodology

### Sign: Validate content batch
- Trigger: Completing content generation
- Instruction: Run validation script on all outputs
- Source: Quality control

---

## Add New Guardrails Below

When a pattern causes repeated failures, add here:

---

Last updated: 2026-01-22
