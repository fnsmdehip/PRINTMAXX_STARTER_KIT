# Ralph Task: Automation Scripts Build

Build core automation scripts for content management.

---

## Context
- Read `ralph/guardrails.md` before starting
- Output to `AUTOMATIONS/scripts/`
- Python 3.11 compatible
- Standard library only (no pip installs)
- Include CLI interfaces

## Success Criteria

### Content Database (content_database.py)
1. [ ] SQLite database with content table
2. [ ] Fields: id, source, platform, text, media_url, likes, rts, views, scraped_at, posted_at, account_used
3. [ ] Index on source and scraped_at
4. [ ] create_db() function
5. [ ] add_content() function
6. [ ] get_pending() function
7. [ ] mark_posted() function
8. [ ] search() function
9. [ ] export_csv() function
10. [ ] CLI with argparse
11. [ ] Database file: LEDGER/content.db
12. [ ] CONTENT_DB_COMPLETE.md created when done

### Caption Modifier (caption_modifier.py)
13. [ ] Takes original caption as input
14. [ ] Generates 3-5 variations
15. [ ] modify(text, num_variants=3) function
16. [ ] clean_ai_tells(text) function removes banned words
17. [ ] check_length(text, max_chars=280) function
18. [ ] CLI interface with --variants flag
19. [ ] Removes em dashes automatically
20. [ ] CAPTION_MOD_COMPLETE.md created when done

## Constraints
- No external dependencies
- Include docstrings
- Error handling for file operations
- argparse for CLI

## After Completion
- Update `ralph/progress.md`
- Test scripts run without errors

---

test_command: "python AUTOMATIONS/scripts/content_database.py --help && python AUTOMATIONS/scripts/caption_modifier.py --help"
expected_output: "usage:"
