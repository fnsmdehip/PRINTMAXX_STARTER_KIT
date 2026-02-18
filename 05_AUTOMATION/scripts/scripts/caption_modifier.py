#!/usr/bin/env python3
"""
Caption Variation Generator

Generates multiple variations of captions while removing AI tells
and maintaining human-first writing style per PRINTMAXX guidelines.

Usage:
    python caption_modifier.py "your caption here" --variants 5
    python caption_modifier.py --file input.txt --output output.txt
    python caption_modifier.py --clean "text with AI words"
"""

import argparse
import random
import re
import sys
from difflib import SequenceMatcher
from typing import List, Tuple, Optional


# Banned AI vocabulary (from copy-style.md)
AI_TELLS = {
    # Single word replacements
    "leverage": "use",
    "leveraging": "using",
    "leveraged": "used",
    "utilize": "use",
    "utilizing": "using",
    "utilized": "used",
    "utilization": "use",
    "delve": "look at",
    "delving": "looking at",
    "delved": "looked at",
    "comprehensive": "",
    "robust": "solid",
    "innovative": "",
    "seamless": "smooth",
    "seamlessly": "smoothly",
    "game-changer": "useful",
    "game changer": "useful",
    "gamechanger": "useful",
    "unlock": "get",
    "unlocking": "getting",
    "unlocked": "got",
    "empower": "help",
    "empowering": "helping",
    "empowered": "helped",
    "cutting-edge": "new",
    "cutting edge": "new",
    "additionally": "also",
    "furthermore": "also",
    "moreover": "also",
    "streamlined": "simple",
    "streamline": "simplify",
    "paradigm": "approach",
    "paradigm shift": "change",
    "landscape": "space",
    "ecosystem": "system",
    "synergy": "combination",
    "synergies": "combinations",
    "optimize": "improve",
    "optimizing": "improving",
    "optimized": "improved",
    "optimization": "improvement",
    "revolutionize": "change",
    "revolutionary": "new",
    "transform": "change",
    "transformative": "useful",
    "elevate": "improve",
    "elevating": "improving",
    "elevated": "improved",
    "frictionless": "easy",
    "holistic": "complete",
    "impactful": "effective",
    "proactive": "early",
    "proactively": "early",
    "scalable": "growable",
    "actionable": "useful",
    "deep dive": "look",
    "unpack": "explain",
    "unpacking": "explaining",
    "journey": "process",
    "foster": "build",
    "fostering": "building",
    "fostered": "built",
    "enable": "let",
    "enabling": "letting",
    "enabled": "let",
    "testament": "proof",
}

# Filler phrases to remove
FILLER_PHRASES = [
    "in order to",
    "due to the fact that",
    "at this point in time",
    "in terms of",
    "it's important to note that",
    "it goes without saying",
    "needless to say",
    "as a matter of fact",
    "for all intents and purposes",
    "at the end of the day",
    "when all is said and done",
    "the fact of the matter is",
    "in the final analysis",
    "as we all know",
    "it should be noted that",
    "it is worth mentioning that",
    "basically",
    "essentially",
    "fundamentally",
    "literally",
    "actually",
    "honestly",
    "obviously",
    "clearly",
]

# Replacements for filler phrases
FILLER_REPLACEMENTS = {
    "in order to": "to",
    "due to the fact that": "because",
    "at this point in time": "now",
    "in terms of": "",
    "it's important to note that": "",
    "it goes without saying": "",
    "needless to say": "",
    "as a matter of fact": "",
    "for all intents and purposes": "",
    "at the end of the day": "",
    "when all is said and done": "",
    "the fact of the matter is": "",
    "in the final analysis": "",
    "as we all know": "",
    "it should be noted that": "",
    "it is worth mentioning that": "",
}

# Synonym groups for variation (non-AI words)
SYNONYM_GROUPS = {
    "great": ["solid", "good", "strong", "effective"],
    "good": ["solid", "decent", "useful", "helpful"],
    "best": ["top", "leading", "strongest", "most effective"],
    "important": ["key", "critical", "essential", "vital"],
    "new": ["fresh", "recent", "latest", "updated"],
    "fast": ["quick", "rapid", "speedy", "instant"],
    "easy": ["simple", "straightforward", "direct", "clear"],
    "hard": ["tough", "difficult", "challenging", "demanding"],
    "big": ["large", "major", "significant", "substantial"],
    "small": ["minor", "slight", "modest", "limited"],
    "start": ["begin", "launch", "kick off", "initiate"],
    "stop": ["end", "halt", "finish", "conclude"],
    "make": ["create", "build", "produce", "generate"],
    "get": ["grab", "obtain", "acquire", "secure"],
    "show": ["display", "reveal", "demonstrate", "present"],
    "help": ["assist", "support", "aid", "guide"],
    "think": ["believe", "consider", "reckon", "figure"],
    "know": ["understand", "realize", "recognize", "see"],
    "need": ["require", "must have", "want", "demand"],
    "want": ["desire", "wish for", "seek", "aim for"],
    "use": ["apply", "employ", "work with", "run"],
    "try": ["attempt", "test", "experiment with", "give a shot"],
    "find": ["discover", "locate", "spot", "uncover"],
    "see": ["notice", "observe", "witness", "view"],
}

# Question to statement templates
QUESTION_PATTERNS = [
    (r"^Do you want to (.+)\?$", "You can {0}."),
    (r"^Are you looking for (.+)\?$", "Here's {0}."),
    (r"^Want to (.+)\?$", "Here's how to {0}."),
    (r"^Need (.+)\?$", "Get {0}."),
    (r"^Struggling with (.+)\?$", "Fix {0} now."),
    (r"^Tired of (.+)\?$", "Stop {0}."),
]

# Statement to question templates
STATEMENT_PATTERNS = [
    (r"^Here's how to (.+)\.$", "Want to {0}?"),
    (r"^You can (.+)\.$", "Ready to {0}?"),
    (r"^This helps you (.+)\.$", "Need to {0}?"),
]


def clean_ai_tells(text: str) -> str:
    """Remove AI vocabulary and replace with human alternatives."""
    result = text

    # Replace AI vocabulary (case-insensitive)
    for ai_word, replacement in AI_TELLS.items():
        # Create pattern that matches word boundaries
        pattern = re.compile(r'\b' + re.escape(ai_word) + r'\b', re.IGNORECASE)
        if replacement:
            # Preserve original case for first letter if replacing
            def replace_with_case(match):
                matched = match.group(0)
                if matched[0].isupper():
                    return replacement.capitalize()
                return replacement
            result = pattern.sub(replace_with_case, result)
        else:
            # Remove the word and clean up extra spaces
            result = pattern.sub('', result)

    # Replace filler phrases
    for filler, replacement in FILLER_REPLACEMENTS.items():
        pattern = re.compile(re.escape(filler), re.IGNORECASE)
        result = pattern.sub(replacement, result)

    # Remove standalone filler words
    for filler in ["basically", "essentially", "fundamentally", "literally",
                   "actually", "honestly", "obviously", "clearly"]:
        # Only remove when followed by comma or at start
        pattern = re.compile(r'\b' + filler + r',?\s*', re.IGNORECASE)
        result = pattern.sub('', result)

    # Replace em dashes with commas or periods
    result = result.replace('—', ', ')
    result = result.replace(' - ', ', ')  # Spaced dashes

    # Fix "It's not just X, it's Y" pattern
    pattern = re.compile(r"[Ii]t'?s not just (.+?),?\s*it'?s (.+?)([.\!]|$)")
    result = pattern.sub(r"It's \2.", result)

    # Clean up multiple spaces
    result = re.sub(r'\s+', ' ', result)

    # Clean up punctuation issues
    result = re.sub(r'\s+([,\.\!\?])', r'\1', result)
    result = re.sub(r'([,\.\!\?])\s*\1+', r'\1', result)
    result = re.sub(r',\s*\.', '.', result)

    return result.strip()


def check_length(text: str, max_chars: int = 280) -> Tuple[bool, int]:
    """Check if text is under character limit. Returns (is_valid, char_count)."""
    char_count = len(text)
    return char_count <= max_chars, char_count


def score_variation(original: str, variant: str) -> float:
    """Calculate similarity score between original and variant (0-100%)."""
    matcher = SequenceMatcher(None, original.lower(), variant.lower())
    return round(matcher.ratio() * 100, 1)


def _apply_synonym_replacement(text: str, intensity: float = 0.3) -> str:
    """Replace some words with synonyms based on intensity (0-1)."""
    words = text.split()
    result = []

    for word in words:
        clean_word = word.lower().strip('.,!?":;')
        if clean_word in SYNONYM_GROUPS and random.random() < intensity:
            # Pick a random synonym
            synonyms = SYNONYM_GROUPS[clean_word]
            new_word = random.choice(synonyms)
            # Preserve punctuation
            if word[-1] in '.,!?":;':
                new_word += word[-1]
            if word[0].isupper():
                new_word = new_word.capitalize()
            result.append(new_word)
        else:
            result.append(word)

    return ' '.join(result)


def _restructure_sentence(text: str) -> str:
    """Restructure sentences for variety."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) < 2:
        return text

    # Try different restructuring strategies
    strategy = random.choice(['reverse', 'front_load', 'combine'])

    if strategy == 'reverse' and len(sentences) >= 2:
        # Put last sentence first (if it's short and punchy)
        if len(sentences[-1]) < 60:
            return sentences[-1] + ' ' + ' '.join(sentences[:-1])

    elif strategy == 'front_load':
        # Find sentence with numbers and put it first
        for i, sent in enumerate(sentences):
            if re.search(r'\d+', sent) and i > 0:
                return sent + ' ' + ' '.join(sentences[:i] + sentences[i+1:])

    elif strategy == 'combine' and len(sentences) >= 3:
        # Combine two short sentences
        for i in range(len(sentences) - 1):
            if len(sentences[i]) < 40 and len(sentences[i+1]) < 40:
                combined = sentences[i].rstrip('.!?') + ' and ' + sentences[i+1][0].lower() + sentences[i+1][1:]
                return ' '.join(sentences[:i] + [combined] + sentences[i+2:])

    return text


def _remove_filler_words(text: str) -> str:
    """Remove additional filler and hedge words."""
    fillers = [
        r'\bvery\b',
        r'\breally\b',
        r'\bjust\b',
        r'\bquite\b',
        r'\brather\b',
        r'\bsomewhat\b',
        r'\bperhaps\b',
        r'\bmaybe\b',
        r'\bprobably\b',
        r'\bpossibly\b',
        r'\bmight\b',
        r'\bcould\b',
    ]

    result = text
    # Only remove some fillers to avoid over-processing
    for filler in random.sample(fillers, min(3, len(fillers))):
        result = re.sub(filler + r'\s+', '', result, flags=re.IGNORECASE)

    return re.sub(r'\s+', ' ', result).strip()


def _convert_question_statement(text: str) -> str:
    """Convert questions to statements or vice versa."""
    # Try question to statement
    for pattern, template in QUESTION_PATTERNS:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            return template.format(*match.groups())

    # Try statement to question
    for pattern, template in STATEMENT_PATTERNS:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            return template.format(*match.groups())

    return text


def _add_specificity(text: str) -> str:
    """Replace vague terms with more specific alternatives."""
    replacements = {
        r'\bmany\b': lambda: f"{random.randint(10, 50)}+",
        r'\bseveral\b': lambda: f"{random.randint(3, 7)}",
        r'\ba lot of\b': lambda: f"{random.randint(20, 100)}+",
        r'\btons of\b': lambda: f"{random.randint(50, 200)}+",
        r'\bquickly\b': lambda: f"in {random.choice(['30 seconds', '2 minutes', '5 minutes'])}",
        r'\bsoon\b': lambda: f"in {random.choice(['24 hours', '48 hours', 'a week'])}",
        r'\brecently\b': lambda: random.choice(['last week', 'yesterday', '3 days ago']),
    }

    result = text
    # Only apply one replacement to avoid over-stuffing
    for pattern, replacement_fn in random.sample(list(replacements.items()), 1):
        if re.search(pattern, result, re.IGNORECASE):
            result = re.sub(pattern, replacement_fn(), result, count=1, flags=re.IGNORECASE)
            break

    return result


def _shorten_for_twitter(text: str, max_chars: int = 280) -> str:
    """Shorten text to fit Twitter limit while preserving meaning."""
    if len(text) <= max_chars:
        return text

    result = text

    # Step 1: Remove filler words aggressively
    fillers = ['very', 'really', 'just', 'quite', 'rather', 'somewhat',
               'actually', 'basically', 'honestly', 'literally']
    for filler in fillers:
        result = re.sub(r'\b' + filler + r'\b\s*', '', result, flags=re.IGNORECASE)

    if len(result) <= max_chars:
        return result.strip()

    # Step 2: Shorten phrases
    shortenings = {
        'in order to': 'to',
        'due to': 'because',
        'a lot of': 'many',
        'as well as': 'and',
        'in addition to': 'plus',
        'for example': 'e.g.',
        'such as': 'like',
        'in the future': 'later',
        'at this time': 'now',
        'right now': 'now',
    }
    for long_form, short_form in shortenings.items():
        result = re.sub(re.escape(long_form), short_form, result, flags=re.IGNORECASE)

    if len(result) <= max_chars:
        return result.strip()

    # Step 3: Truncate sentences from end
    sentences = re.split(r'(?<=[.!?])\s+', result)
    while len(' '.join(sentences)) > max_chars and len(sentences) > 1:
        sentences.pop()

    result = ' '.join(sentences)

    # Step 4: Hard truncate if still too long
    if len(result) > max_chars:
        result = result[:max_chars-3].rsplit(' ', 1)[0] + '...'

    return result.strip()


def modify(text: str, num_variants: int = 3, max_chars: Optional[int] = None) -> List[dict]:
    """
    Generate multiple variations of a caption.

    Args:
        text: Original caption text
        num_variants: Number of variants to generate (3-5)
        max_chars: Optional max character limit (e.g., 280 for Twitter)

    Returns:
        List of dicts with 'text', 'chars', and 'similarity' keys
    """
    num_variants = max(3, min(5, num_variants))

    # First, clean the original
    cleaned = clean_ai_tells(text)

    variants = []
    seen_texts = {cleaned.lower()}

    # Strategy functions
    strategies = [
        lambda t: _apply_synonym_replacement(t, 0.2),
        lambda t: _apply_synonym_replacement(t, 0.4),
        lambda t: _restructure_sentence(t),
        lambda t: _remove_filler_words(t),
        lambda t: _convert_question_statement(t),
        lambda t: _add_specificity(t),
    ]

    attempts = 0
    max_attempts = num_variants * 5

    while len(variants) < num_variants and attempts < max_attempts:
        attempts += 1

        # Start with cleaned version
        variant = cleaned

        # Apply 1-3 random strategies
        num_strategies = random.randint(1, 3)
        selected_strategies = random.sample(strategies, min(num_strategies, len(strategies)))

        for strategy in selected_strategies:
            variant = strategy(variant)

        # Clean again to catch any AI tells introduced
        variant = clean_ai_tells(variant)

        # Apply length constraint if specified
        if max_chars:
            variant = _shorten_for_twitter(variant, max_chars)

        # Check for uniqueness
        if variant.lower() not in seen_texts and variant != text:
            seen_texts.add(variant.lower())
            is_valid, char_count = check_length(variant, max_chars or 280)
            similarity = score_variation(text, variant)

            variants.append({
                'text': variant,
                'chars': char_count,
                'similarity': similarity,
                'valid_length': is_valid if max_chars else True
            })

    # If we couldn't generate enough variants, add the cleaned version
    if len(variants) < num_variants:
        if cleaned.lower() not in seen_texts:
            is_valid, char_count = check_length(cleaned, max_chars or 280)
            variants.append({
                'text': cleaned if not max_chars else _shorten_for_twitter(cleaned, max_chars),
                'chars': char_count,
                'similarity': score_variation(text, cleaned),
                'valid_length': is_valid
            })

    # Sort by similarity (descending) to show most similar first
    variants.sort(key=lambda x: x['similarity'], reverse=True)

    return variants[:num_variants]


def format_output(original: str, variants: List[dict]) -> str:
    """Format output for display."""
    lines = [
        f"Original: {original}",
        f"({len(original)} chars)",
        "---"
    ]

    for i, variant in enumerate(variants, 1):
        lines.append(
            f"Variant {i}: {variant['text']} "
            f"(chars: {variant['chars']}, similarity: {variant['similarity']}%)"
        )

    return '\n'.join(lines)


def process_file(input_path: str, output_path: Optional[str] = None,
                 num_variants: int = 3, max_chars: Optional[int] = None) -> str:
    """Process captions from a file."""
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    results = []
    for line in lines:
        variants = modify(line, num_variants, max_chars)
        results.append(format_output(line, variants))
        results.append('\n' + '=' * 50 + '\n')

    output = '\n'.join(results)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        return f"Processed {len(lines)} captions. Output saved to {output_path}"

    return output


def main():
    parser = argparse.ArgumentParser(
        description='Generate caption variations while removing AI tells.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python caption_modifier.py "your caption here" --variants 5
  python caption_modifier.py --file input.txt --output output.txt
  python caption_modifier.py --clean "text with AI words"
  python caption_modifier.py "long caption" --twitter  # Enforce 280 char limit
        """
    )

    parser.add_argument('text', nargs='?', help='Caption text to modify')
    parser.add_argument('--variants', '-v', type=int, default=3,
                        help='Number of variants to generate (3-5)')
    parser.add_argument('--file', '-f', help='Input file with captions (one per line)')
    parser.add_argument('--output', '-o', help='Output file for results')
    parser.add_argument('--clean', '-c', help='Just clean AI tells from text')
    parser.add_argument('--twitter', '-t', action='store_true',
                        help='Enforce 280 character limit for Twitter')
    parser.add_argument('--max-chars', '-m', type=int,
                        help='Custom max character limit')
    parser.add_argument('--score', '-s', nargs=2, metavar=('ORIGINAL', 'VARIANT'),
                        help='Score similarity between two texts')

    args = parser.parse_args()

    # Determine max chars
    max_chars = None
    if args.twitter:
        max_chars = 280
    elif args.max_chars:
        max_chars = args.max_chars

    # Handle different modes
    if args.clean:
        print(clean_ai_tells(args.clean))

    elif args.score:
        similarity = score_variation(args.score[0], args.score[1])
        print(f"Similarity: {similarity}%")

    elif args.file:
        result = process_file(args.file, args.output, args.variants, max_chars)
        print(result)

    elif args.text:
        variants = modify(args.text, args.variants, max_chars)
        print(format_output(args.text, variants))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
