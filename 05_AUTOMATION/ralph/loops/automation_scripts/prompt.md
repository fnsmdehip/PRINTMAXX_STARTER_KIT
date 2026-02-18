---
task: Build automation scripts for PRINTMAXX
test_command: "python3 /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/AUTOMATIONS/scripts/content_database.py --help"
---

# Task: Build Automation Scripts

You are a Ralph loop iteration. Read this prompt fresh each time.

## First: Read These Files
1. `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/ralph/guardrails.md`

## Current State
Check `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/ralph/loops/automation_scripts/state.md`

## Your Job This Iteration
1. Read state.md for what's complete
2. Pick FIRST incomplete task
3. Do ONLY that task
4. Mark it complete in state.md
5. Exit

## Tasks

### Task 1: Content Database Schema
Create `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/AUTOMATIONS/scripts/content_database.py`
- SQLite database
- Fields: id, source, platform, text, media_url, likes, rts, views, scraped_at, posted_at, account_used
- create_db(), add_content(), get_pending(), mark_posted(), search()
- CLI with argparse
- DB location: LEDGER/content.db

### Task 2: Caption Modifier
Create `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/AUTOMATIONS/scripts/caption_modifier.py`
- modify(text, num_variants=3) returns variations
- clean_ai_tells(text) removes banned words
- check_length(text, max_chars=280)
- CLI interface
- No external dependencies

### Task 3: Content Validator
Create `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/AUTOMATIONS/scripts/content_validator.py`
- validate_post(text) checks for em dashes, AI words, length
- batch_validate(folder) checks all .md files
- Returns pass/fail with reasons
- CLI: python content_validator.py CONTENT/social/faith/

### Task 4: Post Scheduler Queue
Create `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/AUTOMATIONS/scripts/post_queue.py`
- Queue management for posts
- add_to_queue(content_id, platform, scheduled_time)
- get_due_posts() returns posts ready to send
- mark_sent(content_id)
- Uses SQLite in LEDGER/queue.db

## Constraints
- Python 3.11 compatible
- Standard library only
- Include docstrings
- Error handling

## When All Done
If all 4 tasks complete in state.md, output: <promise>COMPLETE</promise>
