#!/usr/bin/env python3
"""
App Rebuild Opportunity Monitor
Based on Greg Isenberg's App Rebuild Flips Strategy

Monitors app stores for rebuild opportunities using the criteria:
- Keyword Pop > 20
- Keyword Diff < 50
- Low ratings (< 99)
- Recent releases (< 2 years)
- ≥2 apps matching criteria
- Category MRR potential ~$10k+

Author: PRINTMAXX App Factory Team
Date: 2026-01-19
"""

import csv
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time

# Note: These imports would need to be installed
# pip install requests beautifulsoup4 playwright pandas
try:
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
except ImportError:
    print("⚠️  Missing dependencies. Install with:")
    print("pip install requests beautifulsoup4 pandas")
    exit(1)


class AppOpportunityMonitor:
    """Monitor app stores for rebuild opportunities"""

    def __init__(self, csv_path: str = "APP_OPPORTUNITIES.csv"):
        self.csv_path = csv_path
        self.opportunities = []
        self.load_existing_opportunities()

    def load_existing_opportunities(self):
        """Load existing opportunities from CSV"""
        if os.path.exists(self.csv_path):
            df = pd.read_csv(self.csv_path)
            self.opportunities = df.to_dict('records')
            print(f"✅ Loaded {len(self.opportunities)} existing opportunities")
        else:
            print("⚠️  No existing CSV found. Will create new one.")
            self.opportunities = []

    def save_opportunities(self):
        """Save opportunities to CSV"""
        if not self.opportunities:
            print("⚠️  No opportunities to save")
            return

        df = pd.DataFrame(self.opportunities)
        df.to_csv(self.csv_path, index=False)
        print(f"✅ Saved {len(self.opportunities)} opportunities to {self.csv_path}")

    def search_google_play(self, category: str, keyword: str) -> List[Dict]:
        """
        Search Google Play Store for apps matching criteria

        Note: This is a simplified version. In production, you'd want to:
        1. Use the Google Play Store API (unofficial)
        2. Or use a service like AppTweak, App Annie, or 42matters API
        3. Or use Playwright for headless browser scraping

        For now, this demonstrates the logic structure.
        """
        print(f"🔍 Searching Google Play: {category} - {keyword}")

        # Placeholder for API call or scraping
        # In production, you'd actually fetch from Play Store here

        # Example structure of what you'd return:
        results = []

        # Simulated result (replace with actual API/scraping)
        # This would come from AppTweak, data.ai, or custom scraper

        return results

    def search_app_store(self, category: str, keyword: str) -> List[Dict]:
        """
        Search Apple App Store for apps matching criteria

        Similar to Google Play, this would use:
        1. App Store Connect API (limited)
        2. Third-party service APIs (AppTweak, Sensor Tower)
        3. Scraping with Playwright
        """
        print(f"🔍 Searching App Store: {category} - {keyword}")

        # Placeholder
        results = []

        return results

    def manual_entry_mode(self):
        """Interactive mode to manually add opportunities"""
        print("\n" + "="*60)
        print("📝 MANUAL ENTRY MODE")
        print("="*60)
        print("Enter app details (or 'quit' to finish):\n")

        while True:
            app_name = input("App Name (or 'quit'): ").strip()
            if app_name.lower() == 'quit':
                break

            category = input("Category: ").strip()
            keyword_pop = input("Keyword Pop (>20): ").strip()
            keyword_diff = input("Keyword Diff (<50): ").strip()
            ratings_count = input("Ratings Count (<99): ").strip()
            release_date = input("Release Date (YYYY-MM-DD): ").strip()
            est_mrr = input("Estimated MRR (e.g., $10,000): ").strip()
            rebuild_notes = input("Rebuild Notes: ").strip()
            status = input("Status (RESEARCH/VALIDATED/WATCHLIST): ").strip().upper()

            opportunity = {
                'App_Name': app_name,
                'Category': category,
                'Keyword_Pop': keyword_pop,
                'Keyword_Diff': keyword_diff,
                'Ratings_Count': ratings_count,
                'Release_Date': release_date,
                'Est_MRR': est_mrr,
                'Rebuild_Notes': rebuild_notes,
                'Status': status if status else 'RESEARCH',
            }

            self.opportunities.append(opportunity)
            print(f"✅ Added: {app_name}\n")

        self.save_opportunities()

    def analyze_opportunity(self, app: Dict) -> Dict:
        """
        Analyze an app opportunity and score it

        Scoring criteria:
        - Keyword Pop (higher is better)
        - Keyword Diff (lower is better)
        - Ratings Count (lower is better, shows weakness)
        - Recency (newer is better, less established)
        - Est MRR (higher is better, shows market size)
        """
        score = 0
        reasons = []

        # Keyword Pop score (max 30 points)
        try:
            pop = int(app.get('Keyword_Pop', 0))
            if pop > 40:
                score += 30
                reasons.append(f"Excellent keyword pop: {pop}")
            elif pop > 30:
                score += 20
                reasons.append(f"Good keyword pop: {pop}")
            elif pop > 20:
                score += 10
                reasons.append(f"Decent keyword pop: {pop}")
        except (ValueError, TypeError):
            pass

        # Keyword Diff score (max 25 points)
        try:
            diff = int(app.get('Keyword_Diff', 100))
            if diff < 30:
                score += 25
                reasons.append(f"Very low competition: {diff}")
            elif diff < 40:
                score += 15
                reasons.append(f"Low competition: {diff}")
            elif diff < 50:
                score += 5
                reasons.append(f"Moderate competition: {diff}")
        except (ValueError, TypeError):
            pass

        # Ratings Count score (max 25 points)
        try:
            ratings = int(app.get('Ratings_Count', 1000))
            if ratings < 50:
                score += 25
                reasons.append(f"Very few ratings: {ratings}")
            elif ratings < 75:
                score += 15
                reasons.append(f"Few ratings: {ratings}")
            elif ratings < 99:
                score += 5
                reasons.append(f"Low ratings: {ratings}")
        except (ValueError, TypeError):
            pass

        # Recency score (max 20 points)
        try:
            release_date = datetime.strptime(app.get('Release_Date', '2020-01-01'), '%Y-%m-%d')
            age_days = (datetime.now() - release_date).days
            if age_days < 180:  # < 6 months
                score += 20
                reasons.append(f"Very recent: {age_days} days old")
            elif age_days < 365:  # < 1 year
                score += 15
                reasons.append(f"Recent: {age_days} days old")
            elif age_days < 730:  # < 2 years
                score += 10
                reasons.append(f"Recent enough: {age_days} days old")
        except (ValueError, TypeError):
            pass

        return {
            'score': score,
            'reasons': reasons,
            'grade': self._score_to_grade(score)
        }

    def _score_to_grade(self, score: int) -> str:
        """Convert score to letter grade"""
        if score >= 80:
            return "A - EXCELLENT OPPORTUNITY"
        elif score >= 60:
            return "B - GOOD OPPORTUNITY"
        elif score >= 40:
            return "C - MODERATE OPPORTUNITY"
        else:
            return "D - WEAK OPPORTUNITY"

    def generate_report(self):
        """Generate analysis report of all opportunities"""
        if not self.opportunities:
            print("⚠️  No opportunities to analyze")
            return

        print("\n" + "="*80)
        print("📊 APP REBUILD OPPORTUNITY REPORT")
        print("="*80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Opportunities: {len(self.opportunities)}\n")

        # Analyze each opportunity
        analyzed = []
        for opp in self.opportunities:
            analysis = self.analyze_opportunity(opp)
            analyzed.append({**opp, **analysis})

        # Sort by score
        analyzed.sort(key=lambda x: x['score'], reverse=True)

        # Print top opportunities
        print("🏆 TOP OPPORTUNITIES:\n")
        for i, opp in enumerate(analyzed[:5], 1):
            print(f"{i}. {opp['App_Name']} - {opp['Category']}")
            print(f"   Score: {opp['score']}/100 - {opp['grade']}")
            print(f"   Status: {opp.get('Status', 'UNKNOWN')}")
            print(f"   Est. MRR: {opp.get('Est_MRR', 'Unknown')}")
            print(f"   Reasons:")
            for reason in opp['reasons']:
                print(f"     • {reason}")
            print(f"   Notes: {opp.get('Rebuild_Notes', 'None')}\n")

        # Category summary
        print("\n📈 CATEGORY BREAKDOWN:\n")
        categories = {}
        for opp in analyzed:
            cat = opp.get('Category', 'Unknown')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(opp)

        for cat, opps in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
            avg_score = sum(o['score'] for o in opps) / len(opps)
            print(f"  {cat}: {len(opps)} opportunities (Avg Score: {avg_score:.1f})")

        # Status summary
        print("\n📋 STATUS BREAKDOWN:\n")
        statuses = {}
        for opp in analyzed:
            status = opp.get('Status', 'UNKNOWN')
            statuses[status] = statuses.get(status, 0) + 1

        for status, count in sorted(statuses.items()):
            print(f"  {status}: {count}")

        print("\n" + "="*80)

    def check_filters(self, app: Dict) -> tuple[bool, List[str]]:
        """
        Check if app meets Greg Isenberg's filters

        Returns: (passes, reasons)
        """
        passes = True
        reasons = []

        # Filter 1: Keyword Pop > 20
        try:
            pop = int(app.get('Keyword_Pop', 0))
            if pop <= 20:
                passes = False
                reasons.append(f"❌ Keyword Pop too low: {pop} (need >20)")
            else:
                reasons.append(f"✅ Keyword Pop good: {pop}")
        except (ValueError, TypeError):
            passes = False
            reasons.append("❌ Invalid Keyword Pop value")

        # Filter 2: Keyword Diff < 50
        try:
            diff = int(app.get('Keyword_Diff', 100))
            if diff >= 50:
                passes = False
                reasons.append(f"❌ Keyword Diff too high: {diff} (need <50)")
            else:
                reasons.append(f"✅ Keyword Diff good: {diff}")
        except (ValueError, TypeError):
            passes = False
            reasons.append("❌ Invalid Keyword Diff value")

        # Filter 3: Low ratings (< 99)
        try:
            ratings = int(app.get('Ratings_Count', 1000))
            if ratings >= 99:
                passes = False
                reasons.append(f"❌ Too many ratings: {ratings} (need <99)")
            else:
                reasons.append(f"✅ Low ratings: {ratings}")
        except (ValueError, TypeError):
            passes = False
            reasons.append("❌ Invalid Ratings Count value")

        # Filter 4: Recent release (< 2 years)
        try:
            release_date = datetime.strptime(app.get('Release_Date', '2020-01-01'), '%Y-%m-%d')
            age_days = (datetime.now() - release_date).days
            if age_days > 730:  # 2 years
                passes = False
                reasons.append(f"❌ Too old: {age_days} days (need <730)")
            else:
                reasons.append(f"✅ Recent: {age_days} days old")
        except (ValueError, TypeError):
            passes = False
            reasons.append("❌ Invalid Release Date")

        return passes, reasons

    def validate_opportunities(self):
        """Run all opportunities through Greg's filters"""
        print("\n" + "="*80)
        print("🔍 VALIDATING OPPORTUNITIES AGAINST GREG'S FILTERS")
        print("="*80 + "\n")

        if not self.opportunities:
            print("⚠️  No opportunities to validate")
            return

        valid = []
        invalid = []

        for opp in self.opportunities:
            passes, reasons = self.check_filters(opp)
            if passes:
                valid.append((opp, reasons))
            else:
                invalid.append((opp, reasons))

        print(f"✅ Valid Opportunities: {len(valid)}")
        print(f"❌ Invalid Opportunities: {len(invalid)}\n")

        if valid:
            print("VALID OPPORTUNITIES:\n")
            for opp, reasons in valid:
                print(f"  {opp['App_Name']} ({opp['Category']})")
                for reason in reasons:
                    print(f"    {reason}")
                print()

        if invalid:
            print("\nINVALID OPPORTUNITIES (Don't meet criteria):\n")
            for opp, reasons in invalid:
                print(f"  {opp['App_Name']} ({opp['Category']})")
                for reason in reasons:
                    print(f"    {reason}")
                print()


def main():
    """Main entry point"""
    print("="*80)
    print("  APP REBUILD OPPORTUNITY MONITOR")
    print("  Based on Greg Isenberg's App Rebuild Flips Strategy")
    print("="*80 + "\n")

    csv_path = os.path.join(os.path.dirname(__file__), "APP_OPPORTUNITIES.csv")
    monitor = AppOpportunityMonitor(csv_path)

    while True:
        print("\nWhat would you like to do?\n")
        print("1. Add opportunities manually")
        print("2. Generate analysis report")
        print("3. Validate against Greg's filters")
        print("4. Export to JSON")
        print("5. Quit")

        choice = input("\nChoice (1-5): ").strip()

        if choice == "1":
            monitor.manual_entry_mode()
        elif choice == "2":
            monitor.generate_report()
        elif choice == "3":
            monitor.validate_opportunities()
        elif choice == "4":
            json_path = csv_path.replace('.csv', '.json')
            with open(json_path, 'w') as f:
                json.dump(monitor.opportunities, f, indent=2)
            print(f"✅ Exported to {json_path}")
        elif choice == "5":
            print("\n👋 Goodbye! Happy app building!")
            break
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
