#!/usr/bin/env python3
"""
Translation Export/Import Tool

Export JSON translation files to CSV for translators.
Import translated CSV files back to JSON.
Validate translations for completeness.

Usage:
    python translation_export.py export --source translations/en --output export.csv
    python translation_export.py import --input translated.csv --output translations/es
    python translation_export.py validate --base translations/en --target translations/es
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def flatten_dict(
    d: Dict[str, Any],
    parent_key: str = "",
    sep: str = ".",
) -> Dict[str, str]:
    """Flatten a nested dictionary into dot-notation keys."""
    items: List[Tuple[str, str]] = []

    for k, v in d.items():
        # Skip context keys
        if k.startswith("_"):
            continue

        new_key = f"{parent_key}{sep}{k}" if parent_key else k

        if isinstance(v, dict):
            # Check if it's a plural form object
            if set(v.keys()).issubset({"zero", "one", "two", "few", "many", "other"}):
                # Store plural forms as JSON string
                items.append((new_key, json.dumps(v, ensure_ascii=False)))
            else:
                items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, str(v)))

    return dict(items)


def unflatten_dict(d: Dict[str, str]) -> Dict[str, Any]:
    """Unflatten dot-notation keys back to nested dictionary."""
    result: Dict[str, Any] = {}

    for key, value in d.items():
        parts = key.split(".")
        current = result

        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]

        # Try to parse as JSON for plural forms
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                current[parts[-1]] = parsed
            else:
                current[parts[-1]] = value
        except (json.JSONDecodeError, TypeError):
            current[parts[-1]] = value

    return result


def load_json_translations(folder: Path) -> Dict[str, Dict[str, str]]:
    """Load all JSON files from a translations folder."""
    translations: Dict[str, Dict[str, str]] = {}

    if not folder.exists():
        print(f"Error: Folder not found: {folder}")
        sys.exit(1)

    for json_file in folder.glob("*.json"):
        namespace = json_file.stem
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            translations[namespace] = flatten_dict(data)
        except json.JSONDecodeError as e:
            print(f"Error parsing {json_file}: {e}")
            sys.exit(1)

    return translations


def export_to_csv(
    source_folder: Path,
    output_file: Path,
    namespaces: Optional[List[str]] = None,
    include_context: bool = True,
) -> None:
    """Export translation JSON files to CSV format."""
    translations = load_json_translations(source_folder)

    # Filter namespaces if specified
    if namespaces:
        translations = {k: v for k, v in translations.items() if k in namespaces}

    if not translations:
        print("No translations found to export.")
        sys.exit(1)

    # Load context if available
    context: Dict[str, str] = {}
    if include_context:
        for namespace, data in translations.items():
            context_file = source_folder / f"{namespace}_context.json"
            if context_file.exists():
                with open(context_file, "r", encoding="utf-8") as f:
                    ctx_data = json.load(f)
                for key, ctx in ctx_data.items():
                    context[f"{namespace}.{key}"] = ctx

    # Write CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header
        headers = ["Key", "English", "Context", "Translation", "Notes"]
        writer.writerow(headers)

        # Sort by namespace then key
        all_rows: List[Tuple[str, str, str, str, str]] = []

        for namespace in sorted(translations.keys()):
            for key in sorted(translations[namespace].keys()):
                full_key = f"{namespace}.{key}"
                value = translations[namespace][key]
                ctx = context.get(full_key, "")

                # Add row: key, english value, context, empty translation, notes
                all_rows.append((full_key, value, ctx, "", ""))

        writer.writerows(all_rows)

    print(f"Exported {len(all_rows)} strings to {output_file}")
    print(f"Namespaces: {', '.join(sorted(translations.keys()))}")


def import_from_csv(
    input_file: Path,
    output_folder: Path,
    language_code: str = "",
) -> None:
    """Import translations from CSV back to JSON files."""
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    # Create output folder if needed
    output_folder.mkdir(parents=True, exist_ok=True)

    # Read CSV
    translations_by_namespace: Dict[str, Dict[str, str]] = {}

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            key = row.get("Key", "")
            translation = row.get("Translation", "")

            # Skip empty translations (use English column as fallback)
            if not translation.strip():
                translation = row.get("English", "")

            if not key or not translation:
                continue

            # Split namespace from key
            parts = key.split(".", 1)
            if len(parts) != 2:
                print(f"Warning: Invalid key format: {key}")
                continue

            namespace, subkey = parts

            if namespace not in translations_by_namespace:
                translations_by_namespace[namespace] = {}

            translations_by_namespace[namespace][subkey] = translation

    # Write JSON files
    for namespace, flat_translations in translations_by_namespace.items():
        nested = unflatten_dict(flat_translations)

        output_file = output_folder / f"{namespace}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(nested, f, ensure_ascii=False, indent=2)

        print(f"Created {output_file} with {len(flat_translations)} strings")

    print(f"\nImported {sum(len(v) for v in translations_by_namespace.values())} total strings")


def validate_translations(
    base_folder: Path,
    target_folder: Path,
    show_missing_only: bool = True,
) -> bool:
    """Validate target translations against base (English) translations."""
    base_translations = load_json_translations(base_folder)
    target_translations = load_json_translations(target_folder)

    all_valid = True
    missing_keys: List[str] = []
    extra_keys: List[str] = []
    placeholder_issues: List[Tuple[str, str, str]] = []

    for namespace, base_strings in base_translations.items():
        if namespace not in target_translations:
            print(f"Missing namespace: {namespace}")
            missing_keys.extend([f"{namespace}.{k}" for k in base_strings.keys()])
            all_valid = False
            continue

        target_strings = target_translations[namespace]

        # Check for missing keys
        for key in base_strings:
            if key not in target_strings:
                missing_keys.append(f"{namespace}.{key}")
                all_valid = False

        # Check for extra keys (might be outdated)
        for key in target_strings:
            if key not in base_strings:
                extra_keys.append(f"{namespace}.{key}")

        # Check placeholder consistency
        for key, base_value in base_strings.items():
            if key in target_strings:
                base_placeholders = set(extract_placeholders(base_value))
                target_placeholders = set(extract_placeholders(target_strings[key]))

                if base_placeholders != target_placeholders:
                    placeholder_issues.append((
                        f"{namespace}.{key}",
                        str(base_placeholders),
                        str(target_placeholders)
                    ))
                    all_valid = False

    # Report results
    target_name = target_folder.name

    if missing_keys:
        print(f"\nMissing keys in {target_name} ({len(missing_keys)}):")
        for key in sorted(missing_keys):
            print(f"  - {key}")

    if extra_keys and not show_missing_only:
        print(f"\nExtra keys in {target_name} (may be outdated) ({len(extra_keys)}):")
        for key in sorted(extra_keys):
            print(f"  + {key}")

    if placeholder_issues:
        print(f"\nPlaceholder mismatches in {target_name} ({len(placeholder_issues)}):")
        for key, base, target in placeholder_issues:
            print(f"  ! {key}")
            print(f"    Base:   {base}")
            print(f"    Target: {target}")

    if all_valid:
        print(f"\nValidation passed for {target_name}")
    else:
        print(f"\nValidation failed for {target_name}")

    return all_valid


def extract_placeholders(text: str) -> List[str]:
    """Extract {{placeholder}} variables from text."""
    import re

    # Handle both plain strings and JSON (for plural forms)
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            # Plural form - check all variations
            placeholders = []
            for value in parsed.values():
                placeholders.extend(re.findall(r"\{\{(\w+)\}\}", value))
            return placeholders
    except (json.JSONDecodeError, TypeError):
        pass

    return re.findall(r"\{\{(\w+)\}\}", text)


def generate_stats(folder: Path) -> None:
    """Generate statistics about translations."""
    translations = load_json_translations(folder)

    total_strings = 0
    total_words = 0

    print(f"\nTranslation Statistics for {folder.name}")
    print("=" * 50)

    for namespace in sorted(translations.keys()):
        strings = translations[namespace]
        word_count = sum(
            len(v.split()) for v in strings.values()
            if not v.startswith("{")  # Skip JSON plural forms
        )

        print(f"{namespace}:")
        print(f"  Strings: {len(strings)}")
        print(f"  Words: ~{word_count}")

        total_strings += len(strings)
        total_words += word_count

    print("-" * 50)
    print(f"Total: {total_strings} strings, ~{total_words} words")

    # Estimate translation cost
    rate_low = 0.05
    rate_high = 0.12
    print(f"\nEstimated translation cost:")
    print(f"  Budget ($0.05/word): ${total_words * rate_low:.2f}")
    print(f"  Premium ($0.12/word): ${total_words * rate_high:.2f}")


def main():
    parser = argparse.ArgumentParser(
        description="Translation Export/Import Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Export English to CSV:
    python translation_export.py export --source translations/en --output export.csv

  Import Spanish translations:
    python translation_export.py import --input spanish.csv --output translations/es

  Validate Spanish against English:
    python translation_export.py validate --base translations/en --target translations/es

  Generate statistics:
    python translation_export.py stats --source translations/en
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export translations to CSV")
    export_parser.add_argument(
        "--source", "-s",
        type=Path,
        required=True,
        help="Source translation folder (e.g., translations/en)"
    )
    export_parser.add_argument(
        "--output", "-o",
        type=Path,
        required=True,
        help="Output CSV file"
    )
    export_parser.add_argument(
        "--namespace", "-n",
        type=str,
        help="Comma-separated namespaces to export (default: all)"
    )
    export_parser.add_argument(
        "--no-context",
        action="store_true",
        help="Exclude context column"
    )

    # Import command
    import_parser = subparsers.add_parser("import", help="Import translations from CSV")
    import_parser.add_argument(
        "--input", "-i",
        type=Path,
        required=True,
        help="Input CSV file"
    )
    import_parser.add_argument(
        "--output", "-o",
        type=Path,
        required=True,
        help="Output translation folder (e.g., translations/es)"
    )
    import_parser.add_argument(
        "--language", "-l",
        type=str,
        default="",
        help="Language code (for logging)"
    )

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate translations")
    validate_parser.add_argument(
        "--base", "-b",
        type=Path,
        required=True,
        help="Base translation folder (e.g., translations/en)"
    )
    validate_parser.add_argument(
        "--target", "-t",
        type=Path,
        required=True,
        help="Target translation folder to validate"
    )
    validate_parser.add_argument(
        "--show-extra",
        action="store_true",
        help="Show extra keys in target (potentially outdated)"
    )

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Generate translation statistics")
    stats_parser.add_argument(
        "--source", "-s",
        type=Path,
        required=True,
        help="Translation folder"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "export":
        namespaces = args.namespace.split(",") if args.namespace else None
        export_to_csv(
            args.source,
            args.output,
            namespaces=namespaces,
            include_context=not args.no_context,
        )

    elif args.command == "import":
        import_from_csv(args.input, args.output, args.language)

    elif args.command == "validate":
        is_valid = validate_translations(
            args.base,
            args.target,
            show_missing_only=not args.show_extra,
        )
        sys.exit(0 if is_valid else 1)

    elif args.command == "stats":
        generate_stats(args.source)


if __name__ == "__main__":
    main()
