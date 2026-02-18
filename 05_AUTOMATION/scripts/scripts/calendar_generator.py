#!/usr/bin/env python3
"""
Content Calendar Generator
===========================
Generates calendar entries from existing content in CONTENT/social/.

Features:
- Scans content directories for available content
- Balances content types across days
- Avoids duplicate content too close together
- Rotates across niches and platforms
- Generates CSV for LEDGER/CONTENT_CALENDAR_2026.csv

Usage:
    python calendar_generator.py --days 30 --start 2026-01-21
    python calendar_generator.py --days 7 --preview
    python calendar_generator.py --append  # Add to existing calendar
"""

import os
import sys
import csv
import random
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict

# Configure paths
BASE_DIR = Path(__file__).parent.parent.parent
LEDGER_DIR = BASE_DIR / "LEDGER"
CONTENT_DIR = BASE_DIR / "CONTENT" / "social"
CALENDAR_PATH = LEDGER_DIR / "CONTENT_CALENDAR_2026.csv"
HASHTAG_LIBRARY_PATH = LEDGER_DIR / "HASHTAG_LIBRARY.csv"
ACCOUNTS_PATH = LEDGER_DIR / "ACCOUNTS.csv"


@dataclass
class ContentFile:
    """Represents a content file."""
    path: str  # Relative path from BASE_DIR
    niche: str
    content_type: str
    filename: str

    @property
    def full_path(self) -> Path:
        return BASE_DIR / self.path


@dataclass
class Account:
    """Represents a social media account."""
    niche: str
    platform: str
    handle: str


@dataclass
class CalendarConfig:
    """Configuration for calendar generation."""
    # Platform posting frequency per day
    platform_frequency: Dict[str, int] = field(default_factory=lambda: {
        "X": 1,  # 1 post per day per niche
        "Instagram": 0.5,  # Every other day per niche
    })

    # Content type rotation order
    content_rotation: Dict[str, List[str]] = field(default_factory=lambda: {
        "faith": ["devotional", "encouragement", "practical"],
        "fitness": ["motivation", "workout_tip", "nutrition_habit"],
        "ai": ["ai_tool_tip", "automation_win", "productivity_hack"],
    })

    # Minimum days between same content reuse
    min_content_gap: int = 14

    # Instagram repurpose delay from X (days)
    ig_repurpose_delay: int = 1


class CalendarGenerator:
    """Generate content calendar from available content."""

    def __init__(self):
        """Initialize the generator."""
        self.content_files: Dict[str, Dict[str, List[ContentFile]]] = defaultdict(lambda: defaultdict(list))
        self.accounts: List[Account] = []
        self.hashtags: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
        self.config = CalendarConfig()

        # Track content usage to avoid duplicates
        self.content_usage: Dict[str, date] = {}  # path -> last used date

        self._scan_content()
        self._load_accounts()
        self._load_hashtags()

    def _scan_content(self) -> None:
        """Scan content directories for available files."""
        if not CONTENT_DIR.exists():
            print(f"Warning: Content directory not found: {CONTENT_DIR}")
            return

        for niche_dir in CONTENT_DIR.iterdir():
            if not niche_dir.is_dir():
                continue

            niche = niche_dir.name  # faith, fitness, ai

            for content_file in niche_dir.glob("*.md"):
                # Determine content type from filename
                # e.g., devotional_01.md -> devotional
                # e.g., ai_tool_tip_001.md -> ai_tool_tip
                filename = content_file.stem
                parts = filename.rsplit('_', 1)
                if len(parts) == 2 and parts[1].isdigit():
                    content_type = parts[0]
                else:
                    content_type = filename

                cf = ContentFile(
                    path=str(content_file.relative_to(BASE_DIR)),
                    niche=niche,
                    content_type=content_type,
                    filename=filename
                )
                self.content_files[niche][content_type].append(cf)

        # Log what was found
        for niche, types in self.content_files.items():
            for ctype, files in types.items():
                print(f"  Found {len(files)} {ctype} files in {niche}")

    def _load_accounts(self) -> None:
        """Load accounts from ACCOUNTS.csv."""
        if not ACCOUNTS_PATH.exists():
            print(f"Warning: Accounts file not found: {ACCOUNTS_PATH}")
            # Use defaults
            self.accounts = [
                Account("faith", "X", "@daily_anchor_faith"),
                Account("faith", "Instagram", "@dailyanchorfaith"),
                Account("fitness", "X", "@three_hour_physique"),
                Account("fitness", "Instagram", "@threehourphysique"),
                Account("ai", "X", "@ai_workflows_daily"),
                Account("ai", "Instagram", "@aiworkflowsdaily"),
            ]
            return

        try:
            with open(ACCOUNTS_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.accounts.append(Account(
                        niche=row.get("Niche", "").lower(),
                        platform=row.get("Platform", ""),
                        handle=row.get("Handle", "")
                    ))
        except Exception as e:
            print(f"Error loading accounts: {e}")

    def _load_hashtags(self) -> None:
        """Load hashtags from HASHTAG_LIBRARY.csv."""
        if not HASHTAG_LIBRARY_PATH.exists():
            return

        try:
            with open(HASHTAG_LIBRARY_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    platform = row.get("platform", "")
                    niche = row.get("niche", "")
                    hashtag = row.get("hashtag", "")
                    recommended = row.get("recommended", "").lower() == "true"

                    if recommended and hashtag:
                        self.hashtags[platform][niche].append(hashtag)
        except Exception as e:
            print(f"Error loading hashtags: {e}")

    def get_account(self, niche: str, platform: str) -> Optional[Account]:
        """Get account for a niche and platform."""
        for account in self.accounts:
            if account.niche.lower() == niche.lower() and account.platform.lower() == platform.lower():
                return account
        return None

    def get_hashtags_for_post(self, platform: str, niche: str, count: int = 4) -> str:
        """Get hashtags for a post."""
        available = self.hashtags.get(platform, {}).get(niche, [])

        if not available:
            # Fallback to defaults
            defaults = {
                "faith": ["#faith", "#christian", "#dailydevotion", "#blessed"],
                "fitness": ["#fitness", "#gym", "#workout", "#health"],
                "ai": ["#AI", "#productivity", "#automation", "#tech"],
            }
            available = defaults.get(niche, [])

        selected = random.sample(available, min(count, len(available)))
        return " ".join(selected)

    def get_next_content(
        self,
        niche: str,
        content_type: str,
        current_date: date
    ) -> Optional[ContentFile]:
        """
        Get next available content file for a niche/type.
        Avoids content used within min_content_gap days.
        """
        available = self.content_files.get(niche, {}).get(content_type, [])

        if not available:
            return None

        # Filter out recently used
        candidates = []
        for cf in available:
            last_used = self.content_usage.get(cf.path)
            if last_used is None:
                candidates.append(cf)
            elif (current_date - last_used).days >= self.config.min_content_gap:
                candidates.append(cf)

        if not candidates:
            # All content used recently, pick least recently used
            sorted_by_usage = sorted(
                available,
                key=lambda x: self.content_usage.get(x.path, date.min)
            )
            return sorted_by_usage[0]

        return random.choice(candidates)

    def generate_calendar(
        self,
        start_date: date,
        num_days: int,
        niches: List[str] = None
    ) -> List[Dict[str, str]]:
        """
        Generate calendar entries for specified period.

        Args:
            start_date: First day of calendar
            num_days: Number of days to generate
            niches: List of niches to include (default: all)

        Returns:
            List of calendar entry dictionaries
        """
        if niches is None:
            niches = list(self.content_files.keys())

        entries = []

        # Track rotation index per niche
        rotation_index: Dict[str, int] = {n: 0 for n in niches}

        # Track Instagram repurpose queue
        ig_repurpose_queue: Dict[str, List[tuple]] = {n: [] for n in niches}

        for day_offset in range(num_days):
            current_date = start_date + timedelta(days=day_offset)
            date_str = current_date.strftime("%Y-%m-%d")
            is_weekend = current_date.weekday() >= 5

            for niche in niches:
                rotation = self.config.content_rotation.get(niche, [])
                if not rotation:
                    continue

                # Get current content type in rotation
                content_type = rotation[rotation_index[niche] % len(rotation)]

                # Get X account
                x_account = self.get_account(niche, "X")
                if x_account:
                    # Get content
                    content_file = self.get_next_content(niche, content_type, current_date)

                    if content_file:
                        # Mark as used
                        self.content_usage[content_file.path] = current_date

                        entry = {
                            "date": date_str,
                            "platform": "X",
                            "account": x_account.handle,
                            "niche": niche,
                            "content_type": content_type,
                            "content_path": content_file.path,
                            "caption": "",  # Will be loaded from file
                            "hashtags": self.get_hashtags_for_post("X", niche),
                            "status": "pending",
                            "posted_url": "",
                            "notes": f"Day {day_offset + 1} rotation" + (" (weekend)" if is_weekend else "")
                        }
                        entries.append(entry)

                        # Add to Instagram repurpose queue
                        ig_repurpose_queue[niche].append((
                            current_date + timedelta(days=self.config.ig_repurpose_delay),
                            content_file,
                            content_type
                        ))

                # Process Instagram repurpose queue
                ig_account = self.get_account(niche, "Instagram")
                if ig_account:
                    # Check for content ready to repurpose
                    ready = [item for item in ig_repurpose_queue[niche] if item[0] <= current_date]

                    # Post 2-3 times per week on Instagram
                    if ready and current_date.weekday() in [1, 3, 6]:  # Tue, Thu, Sun
                        item = ready[0]
                        ig_repurpose_queue[niche].remove(item)

                        entry = {
                            "date": date_str,
                            "platform": "Instagram",
                            "account": ig_account.handle,
                            "niche": niche,
                            "content_type": item[2],
                            "content_path": item[1].path,
                            "caption": "",
                            "hashtags": self.get_hashtags_for_post("Instagram", niche, count=6),
                            "status": "pending",
                            "posted_url": "",
                            "notes": "IG repurpose"
                        }
                        entries.append(entry)

                # Advance rotation
                rotation_index[niche] += 1

        return entries

    def load_existing_calendar(self) -> List[Dict[str, str]]:
        """Load existing calendar entries."""
        entries = []

        if not CALENDAR_PATH.exists():
            return entries

        try:
            with open(CALENDAR_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    entries.append(dict(row))
        except Exception as e:
            print(f"Error loading existing calendar: {e}")

        return entries

    def save_calendar(self, entries: List[Dict[str, str]], append: bool = False) -> None:
        """Save calendar entries to CSV."""
        if append:
            existing = self.load_existing_calendar()
            entries = existing + entries

        fieldnames = [
            "date", "platform", "account", "niche", "content_type",
            "content_path", "caption", "hashtags", "status", "posted_url", "notes"
        ]

        with open(CALENDAR_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(entries)

        print(f"Saved {len(entries)} entries to {CALENDAR_PATH}")

    def preview_calendar(self, entries: List[Dict[str, str]]) -> None:
        """Print a preview of calendar entries."""
        print("\n" + "=" * 70)
        print("CALENDAR PREVIEW")
        print("=" * 70)

        by_date = defaultdict(list)
        for e in entries:
            by_date[e["date"]].append(e)

        for date_str in sorted(by_date.keys())[:14]:  # Show first 2 weeks
            print(f"\n{date_str}")
            print("-" * 40)
            for e in by_date[date_str]:
                print(f"  {e['platform']:10} | {e['account']:25} | {e['content_type']}")

        print("\n" + "=" * 70)
        print(f"Total entries: {len(entries)}")

        # Stats
        platforms = defaultdict(int)
        niches = defaultdict(int)
        for e in entries:
            platforms[e["platform"]] += 1
            niches[e["niche"]] += 1

        print("\nBy Platform:")
        for p, c in sorted(platforms.items()):
            print(f"  {p}: {c}")

        print("\nBy Niche:")
        for n, c in sorted(niches.items()):
            print(f"  {n}: {c}")

        print("=" * 70 + "\n")

    def analyze_balance(self, entries: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze content balance in calendar."""
        analysis = {
            "total": len(entries),
            "by_niche": defaultdict(int),
            "by_platform": defaultdict(int),
            "by_content_type": defaultdict(int),
            "by_day_of_week": defaultdict(int),
            "issues": []
        }

        content_dates = defaultdict(list)

        for e in entries:
            analysis["by_niche"][e["niche"]] += 1
            analysis["by_platform"][e["platform"]] += 1
            analysis["by_content_type"][e["content_type"]] += 1

            try:
                d = datetime.strptime(e["date"], "%Y-%m-%d")
                analysis["by_day_of_week"][d.strftime("%A")] += 1
            except:
                pass

            content_dates[e["content_path"]].append(e["date"])

        # Check for duplicate content too close together
        for path, dates in content_dates.items():
            if len(dates) > 1:
                sorted_dates = sorted(dates)
                for i in range(1, len(sorted_dates)):
                    d1 = datetime.strptime(sorted_dates[i-1], "%Y-%m-%d")
                    d2 = datetime.strptime(sorted_dates[i], "%Y-%m-%d")
                    gap = (d2 - d1).days
                    if gap < self.config.min_content_gap:
                        analysis["issues"].append(
                            f"Content used twice within {gap} days: {path}"
                        )

        return analysis


# CLI
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate content calendar")
    parser.add_argument("--days", type=int, default=30, help="Number of days to generate")
    parser.add_argument("--start", help="Start date (YYYY-MM-DD), default: today")
    parser.add_argument("--preview", action="store_true", help="Preview without saving")
    parser.add_argument("--append", action="store_true", help="Append to existing calendar")
    parser.add_argument("--niches", nargs="+", help="Specific niches to include")
    parser.add_argument("--analyze", action="store_true", help="Analyze existing calendar")

    args = parser.parse_args()

    generator = CalendarGenerator()

    if args.analyze:
        entries = generator.load_existing_calendar()
        analysis = generator.analyze_balance(entries)

        print("\n" + "=" * 50)
        print("CALENDAR ANALYSIS")
        print("=" * 50)
        print(f"\nTotal entries: {analysis['total']}")

        print("\nBy Niche:")
        for n, c in sorted(analysis["by_niche"].items()):
            print(f"  {n}: {c}")

        print("\nBy Platform:")
        for p, c in sorted(analysis["by_platform"].items()):
            print(f"  {p}: {c}")

        print("\nBy Content Type:")
        for t, c in sorted(analysis["by_content_type"].items()):
            print(f"  {t}: {c}")

        print("\nBy Day of Week:")
        for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            print(f"  {d}: {analysis['by_day_of_week'].get(d, 0)}")

        if analysis["issues"]:
            print("\nIssues Found:")
            for issue in analysis["issues"]:
                print(f"  - {issue}")
        else:
            print("\nNo issues found.")

        print("=" * 50 + "\n")

    else:
        # Determine start date
        if args.start:
            try:
                start_date = datetime.strptime(args.start, "%Y-%m-%d").date()
            except ValueError:
                print(f"Invalid date format: {args.start}. Use YYYY-MM-DD")
                sys.exit(1)
        else:
            start_date = date.today()

        print(f"\nGenerating calendar from {start_date} for {args.days} days...")

        entries = generator.generate_calendar(
            start_date=start_date,
            num_days=args.days,
            niches=args.niches
        )

        generator.preview_calendar(entries)

        if not args.preview:
            generator.save_calendar(entries, append=args.append)
            print("Calendar saved successfully.")
        else:
            print("Preview only - not saved. Remove --preview to save.")
