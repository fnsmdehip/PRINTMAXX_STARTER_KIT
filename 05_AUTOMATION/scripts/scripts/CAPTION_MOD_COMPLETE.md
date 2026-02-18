# Caption Modifier - Complete

**Script:** `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/AUTOMATIONS/scripts/caption_modifier.py`
**Created:** 2026-01-24
**Status:** Ready for use

---

## Features Implemented

### Core Functions

| Function | Description |
|----------|-------------|
| `modify(text, num_variants=3)` | Generate 3-5 caption variations |
| `clean_ai_tells(text)` | Remove banned AI vocabulary |
| `check_length(text, max_chars=280)` | Validate character count |
| `score_variation(original, variant)` | Calculate similarity percentage |

### AI Tell Removal

The script removes/replaces 60+ banned AI vocabulary words:
- leverage, utilize, delve, comprehensive, robust
- innovative, seamless, game-changer, unlock, empower
- cutting-edge, additionally, furthermore, moreover
- And 50+ more from copy-style.md

### Pattern Fixes

- Replaces em dashes (—) with commas
- Fixes "It's not just X, it's Y" constructions
- Removes filler phrases (in order to, due to the fact that, etc.)
- Strips hedge words (basically, essentially, honestly, etc.)

### Variation Strategies

1. **Synonym replacement** - Non-AI word substitutions
2. **Sentence restructuring** - Reorder for variety
3. **Filler removal** - Cut unnecessary words
4. **Question/statement conversion** - Change format
5. **Specificity injection** - Replace vague terms with numbers
6. **Twitter shortening** - Fit 280 char limit

---

## CLI Usage

```bash
# Basic usage
python caption_modifier.py "your caption here" --variants 5

# Clean AI tells only
python caption_modifier.py --clean "text with AI words"

# Twitter mode (280 char limit)
python caption_modifier.py "long caption" --twitter

# Custom char limit
python caption_modifier.py "text" --max-chars 150

# File processing
python caption_modifier.py --file input.txt --output output.txt

# Score similarity
python caption_modifier.py --score "original text" "variant text"
```

---

## Python API Usage

```python
from caption_modifier import modify, clean_ai_tells, check_length, score_variation

# Generate variants
variants = modify("Your caption here", num_variants=5, max_chars=280)
for v in variants:
    print(f"{v['text']} ({v['chars']} chars, {v['similarity']}% similar)")

# Clean AI vocabulary
cleaned = clean_ai_tells("Leverage cutting-edge tools to unlock productivity")
# Returns: "Use new tools to get productivity"

# Check length
is_valid, char_count = check_length("Your text", max_chars=280)

# Score similarity
similarity = score_variation("original", "variant")
# Returns: 75.0 (percentage)
```

---

## Output Format

```
Original: [original text]
(X chars)
---
Variant 1: [text] (chars: X, similarity: Y%)
Variant 2: [text] (chars: X, similarity: Y%)
Variant 3: [text] (chars: X, similarity: Y%)
```

---

## Dependencies

None - uses Python 3 standard library only:
- `argparse` - CLI parsing
- `random` - Variation generation
- `re` - Pattern matching
- `difflib` - Similarity scoring

---

## Test Results

**AI-heavy input:**
```
"leveraging cutting-edge automation tools to unlock unprecedented productivity"
```

**After cleaning:**
```
"using new automation tools to get unprecedented productivity"
```

**Similarity score:** 89%+

---

## Integration Points

- Works with `AUTOMATIONS/content_generation/` workflows
- Pairs with `OPS/NICHE_ACCOUNT_CONTENT_CALENDAR.md` for post generation
- Compatible with bulk processing for content farms
