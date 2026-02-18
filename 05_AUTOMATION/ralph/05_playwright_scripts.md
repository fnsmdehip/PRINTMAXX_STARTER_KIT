# Ralph Task: Playwright Automation Scripts

Build social posting automation scripts.

---

## Context
- Read `AUTOMATIONS/SOCIAL_AUTOMATION_STRATEGY.md` for approach
- Read `AUTOMATIONS/SOAX_MOBILE_PROXIES.md` for proxy setup
- Read `AUTOMATIONS/ACCOUNT_WARMING_SOP.md` for limits
- Output to `AUTOMATIONS/scripts/`
- Language: Python with playwright

## Success Criteria

### X/Twitter Poster
1. [ ] `x_poster.py` created
2. [ ] Supports proxy configuration
3. [ ] Uses session persistence
4. [ ] Human-like typing delays
5. [ ] Human-like mouse movement
6. [ ] Logs success/failure
7. [ ] Handles rate limits gracefully

### Instagram Poster
8. [ ] `ig_poster.py` created
9. [ ] Mobile viewport emulation
10. [ ] Mobile user agent
11. [ ] Supports mobile proxy (Soax)
12. [ ] Image upload support
13. [ ] Caption with hashtags
14. [ ] Story posting support

### Multi-Account Manager
15. [ ] `account_manager.py` created
16. [ ] Loads accounts from JSON config
17. [ ] Assigns proxies per account
18. [ ] Tracks last post time
19. [ ] Prevents over-posting

### Content Queue Processor
20. [ ] `queue_processor.py` created
21. [ ] Reads from `LEDGER/content_queue.csv`
22. [ ] Updates status after posting
23. [ ] Logs to `LEDGER/post_log.csv`

### Utility Scripts
24. [ ] `session_manager.py` - Save/load browser sessions
25. [ ] `proxy_tester.py` - Test proxy connectivity
26. [ ] `health_checker.py` - Check account status

## Code Requirements
```python
# All scripts must have:
# 1. Proxy support
# 2. Session persistence
# 3. Human-like delays
# 4. Error handling
# 5. Logging
# 6. Config from environment/file
```

## Example Structure
```python
# x_poster.py

from playwright.sync_api import sync_playwright
import time
import random
import json
from pathlib import Path

class XPoster:
    def __init__(self, account_config: dict):
        self.config = account_config
        self.proxy = account_config.get('proxy')
        self.session_path = account_config.get('session_path')

    def human_delay(self, min_sec=1, max_sec=3):
        time.sleep(random.uniform(min_sec, max_sec))

    def human_type(self, page, text):
        for char in text:
            page.keyboard.type(char)
            time.sleep(random.gauss(0.1, 0.03))

    def post(self, content: str) -> bool:
        # Implementation
        pass
```

## Constraints
- No hardcoded credentials
- All config via JSON/env
- Extensive error handling
- Rate limit respect
- Logging to files

## After Completion
- Update `.ralph/progress.md`
- Log any errors to `.ralph/errors.log`
- Add new guardrails if patterns discovered

---

test_command: "ls AUTOMATIONS/scripts/*.py | wc -l"
expected_output: "7"
