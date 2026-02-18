#!/usr/bin/env python3
"""
A/B Test Analyzer

Pulls test data from RevenueCat/analytics, calculates statistical significance,
generates recommendations, and updates LEDGER/AB_TESTS_MASTER.csv.

Usage:
    python ab_test_analyzer.py --test-id APP-PAY-001
    python ab_test_analyzer.py --analyze-all
    python ab_test_analyzer.py --report weekly
"""

import argparse
import csv
import json
import math
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Configuration
BASE_DIR = Path(__file__).parent.parent
LEDGER_DIR = BASE_DIR / "LEDGER"
AB_TESTS_FILE = LEDGER_DIR / "AB_TESTS_MASTER.csv"
REPORTS_DIR = BASE_DIR / "OPS" / "logs" / "ab_reports"


@dataclass
class Variant:
    """Represents a single test variant."""
    name: str
    visitors: int
    conversions: int

    @property
    def conversion_rate(self) -> float:
        if self.visitors == 0:
            return 0.0
        return self.conversions / self.visitors

    @property
    def standard_error(self) -> float:
        p = self.conversion_rate
        if self.visitors == 0:
            return 0.0
        return math.sqrt(p * (1 - p) / self.visitors)


@dataclass
class TestResult:
    """Represents the result of analyzing an A/B test."""
    test_id: str
    variant_a: Variant
    variant_b: Variant
    variant_c: Optional[Variant]
    z_score: float
    p_value: float
    confidence: float
    relative_lift: float
    winner: Optional[str]
    recommendation: str
    sample_size_adequate: bool
    duration_adequate: bool


class ABTestAnalyzer:
    """Main class for analyzing A/B tests."""

    def __init__(self):
        self.tests = self._load_tests()

    def _load_tests(self) -> list[dict]:
        """Load tests from CSV."""
        tests = []
        if AB_TESTS_FILE.exists():
            with open(AB_TESTS_FILE, 'r') as f:
                reader = csv.DictReader(f)
                tests = list(reader)
        return tests

    def _save_tests(self):
        """Save tests back to CSV."""
        if not self.tests:
            return

        fieldnames = self.tests[0].keys()
        with open(AB_TESTS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.tests)

    @staticmethod
    def calculate_z_score(variant_a: Variant, variant_b: Variant) -> float:
        """Calculate Z-score for two proportions."""
        p1 = variant_a.conversion_rate
        p2 = variant_b.conversion_rate
        n1 = variant_a.visitors
        n2 = variant_b.visitors

        if n1 == 0 or n2 == 0:
            return 0.0

        # Pooled proportion
        p_pooled = (variant_a.conversions + variant_b.conversions) / (n1 + n2)

        if p_pooled == 0 or p_pooled == 1:
            return 0.0

        # Standard error of difference
        se = math.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))

        if se == 0:
            return 0.0

        return (p2 - p1) / se

    @staticmethod
    def z_to_p_value(z: float) -> float:
        """Convert Z-score to two-tailed p-value using approximation."""
        # Using approximation for standard normal CDF
        # This is accurate to about 0.0001
        a1 = 0.254829592
        a2 = -0.284496736
        a3 = 1.421413741
        a4 = -1.453152027
        a5 = 1.061405429
        p = 0.3275911

        sign = 1 if z >= 0 else -1
        z = abs(z) / math.sqrt(2)

        t = 1.0 / (1.0 + p * z)
        y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-z * z)

        cdf = 0.5 * (1.0 + sign * y)

        # Two-tailed p-value
        return 2 * (1 - cdf) if cdf > 0.5 else 2 * cdf

    @staticmethod
    def calculate_sample_size(baseline_cr: float, mde: float,
                             alpha: float = 0.05, power: float = 0.8) -> int:
        """Calculate required sample size per variant."""
        # Z-scores for alpha and power
        z_alpha = 1.96  # 95% confidence
        z_beta = 0.84   # 80% power

        p1 = baseline_cr
        p2 = baseline_cr + mde

        # Sample size formula
        numerator = (z_alpha + z_beta) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2))
        denominator = (p2 - p1) ** 2

        if denominator == 0:
            return float('inf')

        return int(math.ceil(numerator / denominator))

    def analyze_test(self, test_id: str,
                     variant_a_data: tuple[int, int],
                     variant_b_data: tuple[int, int],
                     variant_c_data: Optional[tuple[int, int]] = None,
                     start_date: Optional[datetime] = None) -> TestResult:
        """
        Analyze a single A/B test.

        Args:
            test_id: Test identifier
            variant_a_data: (visitors, conversions) for variant A
            variant_b_data: (visitors, conversions) for variant B
            variant_c_data: Optional (visitors, conversions) for variant C
            start_date: When the test started

        Returns:
            TestResult with analysis
        """
        variant_a = Variant("A", variant_a_data[0], variant_a_data[1])
        variant_b = Variant("B", variant_b_data[0], variant_b_data[1])
        variant_c = None
        if variant_c_data:
            variant_c = Variant("C", variant_c_data[0], variant_c_data[1])

        # Calculate statistics for A vs B (primary comparison)
        z_score = self.calculate_z_score(variant_a, variant_b)
        p_value = self.z_to_p_value(z_score)
        confidence = (1 - p_value) * 100

        # Calculate lift
        if variant_a.conversion_rate > 0:
            relative_lift = ((variant_b.conversion_rate - variant_a.conversion_rate)
                           / variant_a.conversion_rate * 100)
        else:
            relative_lift = 0.0

        # Determine winner
        winner = None
        if confidence >= 95:
            if z_score > 0:
                winner = "variant_b"
            else:
                winner = "variant_a"

        # Check sample size adequacy (assuming 20% MDE target)
        baseline = max(variant_a.conversion_rate, 0.01)
        required_sample = self.calculate_sample_size(baseline, baseline * 0.2)
        sample_size_adequate = min(variant_a.visitors, variant_b.visitors) >= required_sample * 0.8

        # Check duration (minimum 7 days)
        duration_adequate = True
        if start_date:
            days_running = (datetime.now() - start_date).days
            duration_adequate = days_running >= 7

        # Generate recommendation
        recommendation = self._generate_recommendation(
            confidence, relative_lift, winner,
            sample_size_adequate, duration_adequate,
            variant_a, variant_b
        )

        return TestResult(
            test_id=test_id,
            variant_a=variant_a,
            variant_b=variant_b,
            variant_c=variant_c,
            z_score=z_score,
            p_value=p_value,
            confidence=confidence,
            relative_lift=relative_lift,
            winner=winner,
            recommendation=recommendation,
            sample_size_adequate=sample_size_adequate,
            duration_adequate=duration_adequate
        )

    def _generate_recommendation(self, confidence: float, lift: float,
                                winner: Optional[str],
                                sample_ok: bool, duration_ok: bool,
                                variant_a: Variant, variant_b: Variant) -> str:
        """Generate actionable recommendation."""

        if not sample_ok:
            return f"CONTINUE: Need more data. Current sample: {variant_a.visitors + variant_b.visitors}. Recommendation: Wait for adequate sample size."

        if not duration_ok:
            return "CONTINUE: Test has not run for minimum 7 days. Wait for duration requirement."

        if confidence < 90:
            return f"INCONCLUSIVE: {confidence:.1f}% confidence. No significant difference detected. Consider extending test or accepting null hypothesis."

        if confidence < 95:
            return f"DIRECTIONAL: {confidence:.1f}% confidence suggests {'B' if lift > 0 else 'A'} may be better ({abs(lift):.1f}% {'lift' if lift > 0 else 'drop'}). Consider extending for stronger signal."

        if winner:
            variant_name = "B" if winner == "variant_b" else "A"
            return f"WINNER: Variant {variant_name} wins with {confidence:.1f}% confidence, {abs(lift):.1f}% {'lift' if lift > 0 else 'drop'}. Implement winning variant."

        return "ERROR: Unable to generate recommendation."

    def update_test_result(self, test_id: str, result: TestResult):
        """Update test result in CSV."""
        for test in self.tests:
            if test['test_id'] == test_id:
                test['sample_size_actual'] = str(result.variant_a.visitors + result.variant_b.visitors)
                test['status'] = 'COMPLETED' if result.winner else 'IN_PROGRESS'
                test['result'] = result.winner.upper() if result.winner else 'PENDING'
                test['winner'] = result.winner if result.winner else ''
                test['lift_percent'] = f"{result.relative_lift:.1f}"
                test['confidence'] = f"{result.confidence:.1f}"
                test['notes'] = result.recommendation
                break

        self._save_tests()

    def generate_report(self, report_type: str = 'all') -> str:
        """Generate analysis report."""
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        report_lines = [
            "# A/B Test Analysis Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Summary",
            "",
        ]

        # Count tests by status
        statuses = {}
        for test in self.tests:
            status = test.get('status', 'NOT_STARTED')
            statuses[status] = statuses.get(status, 0) + 1

        report_lines.append("| Status | Count |")
        report_lines.append("|--------|-------|")
        for status, count in sorted(statuses.items()):
            report_lines.append(f"| {status} | {count} |")
        report_lines.append("")

        # List tests by category
        categories = {}
        for test in self.tests:
            test_type = test.get('test_type', 'unknown')
            if test_type not in categories:
                categories[test_type] = []
            categories[test_type].append(test)

        report_lines.append("## Tests by Category")
        report_lines.append("")

        for category, tests in sorted(categories.items()):
            report_lines.append(f"### {category.replace('_', ' ').title()}")
            report_lines.append("")
            report_lines.append("| Test ID | App | Hypothesis | Status | Winner | Lift |")
            report_lines.append("|---------|-----|------------|--------|--------|------|")

            for test in tests:
                test_id = test.get('test_id', '')
                app = test.get('app', '')
                hypothesis = test.get('hypothesis', '')[:40] + '...' if len(test.get('hypothesis', '')) > 40 else test.get('hypothesis', '')
                status = test.get('status', '')
                winner = test.get('winner', '-')
                lift = test.get('lift_percent', '-')

                report_lines.append(f"| {test_id} | {app} | {hypothesis} | {status} | {winner} | {lift}% |")

            report_lines.append("")

        # Save report
        report_content = '\n'.join(report_lines)
        report_file = REPORTS_DIR / f"ab_report_{datetime.now().strftime('%Y%m%d')}.md"
        report_file.write_text(report_content)

        return report_content


class RevenueCatClient:
    """Client for pulling data from RevenueCat API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('REVENUECAT_API_KEY')
        self.base_url = "https://api.revenuecat.com/v1"

    def get_experiment_data(self, experiment_id: str) -> dict:
        """
        Pull experiment data from RevenueCat.

        Note: This is a placeholder. Actual implementation requires:
        1. Valid RevenueCat API key
        2. Experiment ID from RevenueCat dashboard

        Returns mock data for demonstration.
        """
        # TODO: Implement actual API call when API key is available
        # import requests
        # headers = {"Authorization": f"Bearer {self.api_key}"}
        # response = requests.get(f"{self.base_url}/experiments/{experiment_id}", headers=headers)
        # return response.json()

        print(f"[Mock] Fetching experiment data for {experiment_id}")
        return {
            "experiment_id": experiment_id,
            "status": "running",
            "variants": {
                "control": {"users": 1000, "conversions": 50},
                "treatment": {"users": 1000, "conversions": 65}
            }
        }

    def list_experiments(self) -> list[dict]:
        """List all active experiments."""
        # TODO: Implement actual API call
        print("[Mock] Listing experiments")
        return []


class FirebaseClient:
    """Client for pulling data from Firebase Analytics."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get('FIREBASE_PROJECT_ID')

    def get_ab_test_data(self, test_name: str) -> dict:
        """
        Pull A/B test data from Firebase.

        Note: This is a placeholder. Actual implementation requires:
        1. Firebase service account credentials
        2. BigQuery access for analytics data

        Returns mock data for demonstration.
        """
        # TODO: Implement actual Firebase/BigQuery query
        print(f"[Mock] Fetching Firebase data for {test_name}")
        return {
            "test_name": test_name,
            "variants": {
                "control": {"users": 500, "events": {"purchase": 25}},
                "variant_1": {"users": 500, "events": {"purchase": 35}}
            }
        }


def main():
    parser = argparse.ArgumentParser(description='A/B Test Analyzer')
    parser.add_argument('--test-id', help='Analyze specific test by ID')
    parser.add_argument('--analyze-all', action='store_true', help='Analyze all active tests')
    parser.add_argument('--report', choices=['daily', 'weekly', 'all'], help='Generate report')
    parser.add_argument('--manual', action='store_true', help='Enter data manually')

    args = parser.parse_args()

    analyzer = ABTestAnalyzer()

    if args.test_id and args.manual:
        # Manual data entry mode
        print(f"\nManual data entry for test: {args.test_id}")
        print("-" * 40)

        print("\nVariant A (Control):")
        a_visitors = int(input("  Visitors: "))
        a_conversions = int(input("  Conversions: "))

        print("\nVariant B (Treatment):")
        b_visitors = int(input("  Visitors: "))
        b_conversions = int(input("  Conversions: "))

        has_c = input("\nDo you have Variant C? (y/n): ").lower() == 'y'
        c_data = None
        if has_c:
            print("\nVariant C:")
            c_visitors = int(input("  Visitors: "))
            c_conversions = int(input("  Conversions: "))
            c_data = (c_visitors, c_conversions)

        result = analyzer.analyze_test(
            args.test_id,
            (a_visitors, a_conversions),
            (b_visitors, b_conversions),
            c_data
        )

        print("\n" + "=" * 50)
        print("ANALYSIS RESULTS")
        print("=" * 50)
        print(f"\nTest ID: {result.test_id}")
        print(f"\nVariant A: {result.variant_a.conversion_rate*100:.2f}% ({result.variant_a.conversions}/{result.variant_a.visitors})")
        print(f"Variant B: {result.variant_b.conversion_rate*100:.2f}% ({result.variant_b.conversions}/{result.variant_b.visitors})")
        if result.variant_c:
            print(f"Variant C: {result.variant_c.conversion_rate*100:.2f}% ({result.variant_c.conversions}/{result.variant_c.visitors})")
        print(f"\nZ-Score: {result.z_score:.3f}")
        print(f"P-Value: {result.p_value:.4f}")
        print(f"Confidence: {result.confidence:.1f}%")
        print(f"Relative Lift (A vs B): {result.relative_lift:+.1f}%")
        print(f"\nWinner: {result.winner or 'None yet'}")
        print(f"\nRECOMMENDATION: {result.recommendation}")

        update = input("\nUpdate LEDGER with these results? (y/n): ").lower() == 'y'
        if update:
            analyzer.update_test_result(args.test_id, result)
            print("LEDGER updated successfully.")

    elif args.test_id:
        # Fetch from APIs (mock mode)
        rc_client = RevenueCatClient()
        data = rc_client.get_experiment_data(args.test_id)
        print(f"Fetched data: {json.dumps(data, indent=2)}")

    elif args.analyze_all:
        print("Analyzing all active tests...")
        active_tests = [t for t in analyzer.tests if t.get('status') == 'IN_PROGRESS']
        print(f"Found {len(active_tests)} active tests")

        for test in active_tests:
            print(f"\n  - {test['test_id']}: {test['hypothesis'][:50]}...")

    elif args.report:
        print(f"Generating {args.report} report...")
        report = analyzer.generate_report(args.report)
        print("\nReport generated. Summary:")
        print(report[:500] + "..." if len(report) > 500 else report)

    else:
        # Interactive mode
        print("\nA/B Test Analyzer - Interactive Mode")
        print("=" * 40)
        print("\nOptions:")
        print("1. Analyze test with manual data entry")
        print("2. Generate report")
        print("3. List all tests")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ")

        if choice == '1':
            test_id = input("Enter test ID: ")
            # Recursively call with manual flag
            import sys
            sys.argv = ['ab_test_analyzer.py', '--test-id', test_id, '--manual']
            main()

        elif choice == '2':
            report = analyzer.generate_report('all')
            print("\n" + report)

        elif choice == '3':
            print("\nAll Tests:")
            print("-" * 80)
            for test in analyzer.tests:
                status = test.get('status', 'NOT_STARTED')
                print(f"{test['test_id']}: {test['app']} - {test['test_type']} [{status}]")

        else:
            print("Goodbye!")


if __name__ == '__main__':
    main()
