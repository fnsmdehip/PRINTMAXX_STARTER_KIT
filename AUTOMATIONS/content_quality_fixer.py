#!/usr/bin/env python3
"""Auto-fix content quality issues: em dashes, AI slop, weak hooks."""
import re, os, sys
from pathlib import Path
from itertools import chain

SLOP_WORDS = {
    "leverage": "use",
    "unlock": "get",
    "comprehensive": "complete",
    "innovative": "novel",
    "paradigm": "model",
    "journey": "path",
    "delve": "dig",
    "robust": "strong",
    "utilize": "use",
    "moreover": "also",
    "furthermore": "and",
    "additionally": "also",
}

def fix_em_dashes(text):
    """Replace em dashes with commas."""
    return text.replace(" — ", ", ").replace("—", "-")

def fix_slop(text):
    """Remove AI slop vocabulary."""
    for word, replacement in SLOP_WORDS.items():
        text = re.sub(r'\b' + word + r'\b', replacement, text, flags=re.IGNORECASE)
    return text

def process_file(fpath):
    """Fix a single content file."""
    try:
        with open(fpath, 'r') as f:
            content = f.read()
        
        original = content
        content = fix_em_dashes(content)
        content = fix_slop(content)
        
        if content != original:
            with open(fpath, 'w') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        return None

# Find all content files
content_dir = Path("CONTENT/social")
if not content_dir.exists():
    print("No CONTENT/social directory")
    sys.exit(1)

fixed = 0
for ext in ["*.md", "*.txt"]:
    for fpath in content_dir.rglob(ext):
        result = process_file(fpath)
        if result is True:
            fixed += 1

print(f"Fixed {fixed} files (em dashes, AI slop)")
