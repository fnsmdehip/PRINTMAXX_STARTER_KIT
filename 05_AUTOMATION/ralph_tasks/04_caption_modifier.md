---
task_id: CAPTION-001
test_command: "python3 AUTOMATIONS/scripts/caption_modifier.py --test"
max_iterations: 15
completion_signal: "CAPTION_MOD_COMPLETE"
---

# Task: Build caption variation generator

## Context
- Read .claude/rules/copy-style.md for voice rules
- Output to AUTOMATIONS/scripts/caption_modifier.py
- Purpose: Take repurposed content captions and generate variations

## Requirements

### Core Functionality
1. Takes original caption as input
2. Generates 3-5 variations
3. Maintains meaning, changes phrasing
4. Removes AI tells (banned vocabulary)
5. Ensures < 280 chars for X

### CLI Interface
```bash
# Single caption
python caption_modifier.py --text "Original caption here"

# From file
python caption_modifier.py --file captions.txt --output variations.csv

# With count
python caption_modifier.py --text "Caption" --count 5

# Test mode
python caption_modifier.py --test
```

### Variation Strategies

1. **Tone shift** - Casual to slightly formal, or vice versa
2. **Perspective change** - First person to third, or vice versa
3. **Length adjust** - Shorter/punchier or add context
4. **Question flip** - Statement to question or vice versa
5. **Emphasis shift** - Highlight different aspect

### Examples

Original: "This is the craziest thing I've seen today"
Variations:
- "bruh what did I just witness"
- "how is no one talking about this"
- "I can't believe this is real"
- "okay this actually broke my brain"
- "when you see it you won't believe it"

### Banned Patterns to Remove
- Em dashes (—) → commas or periods
- "leverage", "utilize" → "use"
- "comprehensive" → (remove or simplify)
- "innovative" → "new" or (remove)
- "It's not just X, it's Y" → rewrite entirely

## Success Criteria
1. [ ] Script runs without errors
2. [ ] Generates 3-5 variations per input
3. [ ] All variations < 280 chars
4. [ ] No banned vocabulary in output
5. [ ] No em dashes in output
6. [ ] --test flag validates functionality
7. [ ] Variations feel genuinely different

## Technical Implementation

```python
#!/usr/bin/env python3
"""
Caption Variation Generator
Creates unique variations of captions for repurposed content.
"""

import argparse
import re

BANNED_WORDS = [
    'leverage', 'utilize', 'delve', 'comprehensive', 'robust',
    'innovative', 'seamless', 'game-changer', 'unlock', 'empower',
    'cutting-edge', 'additionally', 'furthermore'
]

def clean_caption(text):
    """Remove AI tells and banned patterns."""
    # Replace em dashes
    text = text.replace('—', ', ')
    text = text.replace('–', ', ')

    # Remove banned words
    for word in BANNED_WORDS:
        text = re.sub(rf'\b{word}\b', '', text, flags=re.IGNORECASE)

    return text.strip()

def generate_variations(original, count=3):
    """Generate caption variations."""
    # Implementation here
    pass

# ... rest of implementation ...
```

## When complete
Run test: `python3 AUTOMATIONS/scripts/caption_modifier.py --test`
If passes: <promise>CAPTION_MOD_COMPLETE</promise>
