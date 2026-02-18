#!/usr/bin/env python3
"""
Content Validator

Validates content against PRINTMAXX copy style rules.
Checks for em dashes, AI vocabulary, length limits, and other quality issues.
"""

import argparse
import re
from pathlib import Path
from typing import List, Dict, Tuple


# Banned AI vocabulary from copy-style.md
BANNED_WORDS = [
    "additionally", "moreover", "furthermore",
    "testament", "landscape", "paradigm",
    "leverage", "utilize",
    "delve", "dive into", "unpack",
    "comprehensive", "robust", "streamlined",
    "game-changer", "unlock", "elevate",
    "cutting-edge", "innovative", "revolutionary",
    "empower", "enable", "foster",
    "seamless", "frictionless"
]

# Banned phrases
BANNED_PHRASES = [
    r"it's not just .+, it's .+",
    r"experts? (say|believe|agree)",
    r"studies show",
    r"in today's .+ landscape",
    r"in order to",
    r"due to the fact that",
    r"at this point in time",
    r"it's important to note that",
    r"it goes without saying"
]


def validate_post(text: str, max_chars: int = 280) -> Tuple[bool, List[str]]:
    """
    Validate a single post against copy style rules.

    Args:
        text: Post text to validate
        max_chars: Maximum character limit (default 280 for X/Twitter)

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    # Check for em dashes
    if "—" in text:
        issues.append("Contains em dash (—). Use comma or period instead.")

    # Check for banned words
    text_lower = text.lower()
    for word in BANNED_WORDS:
        if re.search(r'\b' + word.lower() + r'\b', text_lower):
            issues.append(f"Contains banned AI word: '{word}'")

    # Check for banned phrases
    for pattern in BANNED_PHRASES:
        if re.search(pattern, text_lower):
            issues.append(f"Contains banned phrase pattern: {pattern}")

    # Check length
    if len(text) > max_chars:
        issues.append(f"Too long: {len(text)} chars (max {max_chars})")

    # Check for excessive hedging
    hedge_words = ["might", "possibly", "perhaps", "somewhat", "maybe", "could"]
    hedge_count = sum(1 for word in hedge_words if re.search(r'\b' + word + r'\b', text_lower))
    if hedge_count > 1:
        issues.append(f"Excessive hedging: {hedge_count} hedge words (max 1 per sentence)")

    # Check for promotional adjectives
    promo_words = ["breathtaking", "revolutionary", "groundbreaking", "incredible", "amazing"]
    for word in promo_words:
        if re.search(r'\b' + word.lower() + r'\b', text_lower):
            issues.append(f"Contains promotional adjective: '{word}'")

    # Check for vague attributions without specifics
    if re.search(r'\b(experts?|studies|research(ers)?)\b', text_lower):
        if not re.search(r'(https?://|@\w+)', text):
            issues.append("Vague attribution without link or citation")

    is_valid = len(issues) == 0
    return is_valid, issues


def clean_ai_tells(text: str) -> str:
    """
    Remove AI tells from text.

    Args:
        text: Input text

    Returns:
        Cleaned text
    """
    cleaned = text

    # Remove em dashes (replace with commas)
    cleaned = cleaned.replace("—", ",")

    # Replace banned words with simpler alternatives
    replacements = {
        "utilize": "use",
        "leverage": "use",
        "additionally": "also",
        "furthermore": "also",
        "moreover": "also",
        "in order to": "to",
        "due to the fact that": "because",
        "at this point in time": "now"
    }

    for old, new in replacements.items():
        cleaned = re.sub(r'\b' + old + r'\b', new, cleaned, flags=re.IGNORECASE)

    return cleaned


def check_length(text: str, max_chars: int = 280) -> Dict[str, any]:
    """
    Check text length and provide stats.

    Args:
        text: Text to check
        max_chars: Maximum allowed characters

    Returns:
        Dictionary with length stats
    """
    char_count = len(text)
    word_count = len(text.split())
    over_limit = char_count > max_chars

    return {
        "char_count": char_count,
        "word_count": word_count,
        "max_chars": max_chars,
        "over_limit": over_limit,
        "remaining": max_chars - char_count if not over_limit else 0
    }


def validate_file(filepath: Path, max_chars: int = 280) -> Tuple[bool, List[str]]:
    """
    Validate a single markdown file.

    Args:
        filepath: Path to markdown file
        max_chars: Maximum character limit

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    try:
        content = filepath.read_text(encoding='utf-8')

        # Skip frontmatter if present
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2].strip()

        return validate_post(content, max_chars)

    except Exception as e:
        return False, [f"Error reading file: {str(e)}"]


def batch_validate(folder: str, max_chars: int = 280) -> Dict[str, any]:
    """
    Validate all .md files in a folder.

    Args:
        folder: Path to folder
        max_chars: Maximum character limit

    Returns:
        Dictionary with validation results
    """
    folder_path = Path(folder)

    if not folder_path.exists():
        return {
            "error": f"Folder not found: {folder}",
            "total": 0,
            "passed": 0,
            "failed": 0,
            "files": []
        }

    md_files = list(folder_path.glob("**/*.md"))

    results = []
    passed = 0
    failed = 0

    for filepath in md_files:
        is_valid, issues = validate_file(filepath, max_chars)

        if is_valid:
            passed += 1
        else:
            failed += 1

        results.append({
            "file": str(filepath.relative_to(folder_path)),
            "valid": is_valid,
            "issues": issues
        })

    return {
        "total": len(md_files),
        "passed": passed,
        "failed": failed,
        "files": results
    }


def main():
    """CLI interface."""
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Content Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python content_validator.py --text "This is a test post"
    python content_validator.py --file post.md
    python content_validator.py --folder CONTENT/social/faith/
    python content_validator.py --clean "I will utilize this tool"
    python content_validator.py --length "This is my post text"
        """
    )

    parser.add_argument("--text", help="Validate a single text string")
    parser.add_argument("--file", help="Validate a single markdown file")
    parser.add_argument("--folder", help="Validate all .md files in folder")
    parser.add_argument("--clean", help="Clean AI tells from text")
    parser.add_argument("--length", help="Check text length")
    parser.add_argument("--max-chars", type=int, default=280, help="Max character limit (default: 280)")

    args = parser.parse_args()

    if args.text:
        is_valid, issues = validate_post(args.text, args.max_chars)
        print(f"\nValidation: {'PASS' if is_valid else 'FAIL'}")
        if issues:
            print("\nIssues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("No issues found.")

        stats = check_length(args.text, args.max_chars)
        print(f"\nLength: {stats['char_count']}/{stats['max_chars']} chars, {stats['word_count']} words")

    elif args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"File not found: {args.file}")
            return

        is_valid, issues = validate_file(filepath, args.max_chars)
        print(f"\nFile: {args.file}")
        print(f"Validation: {'PASS' if is_valid else 'FAIL'}")
        if issues:
            print("\nIssues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("No issues found.")

    elif args.folder:
        results = batch_validate(args.folder, args.max_chars)

        if "error" in results:
            print(results["error"])
            return

        print(f"\nValidation Results for: {args.folder}")
        print(f"Total files: {results['total']}")
        print(f"Passed: {results['passed']}")
        print(f"Failed: {results['failed']}")

        if results['failed'] > 0:
            print("\nFiles with issues:")
            for file_result in results['files']:
                if not file_result['valid']:
                    print(f"\n{file_result['file']}:")
                    for issue in file_result['issues']:
                        print(f"  - {issue}")

    elif args.clean:
        cleaned = clean_ai_tells(args.clean)
        print(f"Original: {args.clean}")
        print(f"Cleaned:  {cleaned}")

    elif args.length:
        stats = check_length(args.length, args.max_chars)
        print(f"Characters: {stats['char_count']}/{stats['max_chars']}")
        print(f"Words: {stats['word_count']}")
        print(f"Status: {'OVER LIMIT' if stats['over_limit'] else 'OK'}")
        if not stats['over_limit']:
            print(f"Remaining: {stats['remaining']} chars")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
