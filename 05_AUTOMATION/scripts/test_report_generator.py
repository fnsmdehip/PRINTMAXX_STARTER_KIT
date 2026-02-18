#!/usr/bin/env python3
"""
Test Report Generator - Generate Comprehensive Test Reports
==========================================================
Generate HTML, JSON, and Markdown reports from test results.

Features:
- Multiple output formats (HTML, JSON, Markdown)
- Trend analysis over time
- Test history tracking
- Failure pattern detection
- Performance metrics
- Email-ready summaries
- Badge generation

Usage:
    from test_report_generator import TestReportGenerator

    generator = TestReportGenerator()
    generator.add_result(bulk_result)
    generator.generate_html("report.html")

CLI:
    python test_report_generator.py --input results.json --format html
    python test_report_generator.py --input results.json --format markdown --output report.md
    python test_report_generator.py --history --days 7
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import logging

# Configure logging
LOG_DIR = Path(__file__).parent.parent / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("test_report_generator")


@dataclass
class TestTrend:
    """Trend data for a test."""
    test_name: str
    total_runs: int
    pass_rate: float
    avg_duration: float
    recent_status: List[str] = field(default_factory=list)
    flaky: bool = False


@dataclass
class ReportData:
    """Data structure for report generation."""
    title: str = "Test Report"
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    summary: Dict[str, Any] = field(default_factory=dict)
    results: List[Dict[str, Any]] = field(default_factory=list)
    trends: List[TestTrend] = field(default_factory=list)
    failures: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class TestResultsStore:
    """Store and retrieve test results history."""

    def __init__(self, store_path: Path = None):
        self.store_path = store_path or (LOG_DIR / "test_history.json")
        self._history: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        """Load history from file."""
        if self.store_path.exists():
            try:
                with open(self.store_path, 'r') as f:
                    self._history = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load history: {e}")
                self._history = []

    def _save(self):
        """Save history to file."""
        with open(self.store_path, 'w') as f:
            json.dump(self._history, f, indent=2)

    def add_run(self, result: Dict[str, Any]):
        """Add a test run to history."""
        self._history.append({
            "timestamp": datetime.now().isoformat(),
            "data": result
        })
        # Keep last 100 runs
        self._history = self._history[-100:]
        self._save()

    def get_runs(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get runs from the last N days."""
        cutoff = datetime.now() - timedelta(days=days)
        return [
            run for run in self._history
            if datetime.fromisoformat(run["timestamp"]) > cutoff
        ]

    def get_test_history(self, test_name: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get history for a specific test."""
        history = []
        for run in reversed(self._history):
            for result in run.get("data", {}).get("results", []):
                if result.get("test_name") == test_name:
                    history.append({
                        "timestamp": run["timestamp"],
                        "status": result.get("status"),
                        "duration": result.get("duration_seconds")
                    })
                    if len(history) >= limit:
                        return history
        return history


class TestReportGenerator:
    """Generate test reports in multiple formats."""

    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.store = TestResultsStore()

    def add_result(self, result: Dict[str, Any]):
        """Add a test result to the report."""
        self.results.append(result)
        self.store.add_run(result)

    def load_from_file(self, file_path: str) -> Dict[str, Any]:
        """Load test results from JSON file."""
        with open(file_path, 'r') as f:
            result = json.load(f)
        self.results.append(result)
        return result

    def _build_report_data(self) -> ReportData:
        """Build report data from results."""
        if not self.results:
            return ReportData()

        # Use most recent result for main summary
        latest = self.results[-1]

        report = ReportData(
            title="PRINTMAXX Test Report",
            summary={
                "total": latest.get("total_tests", 0),
                "passed": latest.get("passed", 0),
                "failed": latest.get("failed", 0),
                "errors": latest.get("errors", 0),
                "skipped": latest.get("skipped", 0),
                "timeout": latest.get("timeout", 0),
                "duration": latest.get("duration_seconds", 0),
                "pass_rate": self._calculate_pass_rate(latest),
                "start_time": latest.get("start_time"),
                "end_time": latest.get("end_time"),
            },
            results=latest.get("results", []),
            metadata={
                "report_version": "1.0",
                "generator": "PRINTMAXX Test Report Generator",
            }
        )

        # Extract failures
        report.failures = [
            r for r in report.results
            if r.get("status") in ("failed", "error", "timeout")
        ]

        # Build trends
        report.trends = self._build_trends()

        return report

    def _calculate_pass_rate(self, result: Dict[str, Any]) -> float:
        """Calculate pass rate percentage."""
        total = result.get("total_tests", 0)
        passed = result.get("passed", 0)
        if total == 0:
            return 0.0
        return round((passed / total) * 100, 2)

    def _build_trends(self) -> List[TestTrend]:
        """Build trend data for tests."""
        # Aggregate by test name
        test_stats = defaultdict(lambda: {"runs": 0, "passed": 0, "durations": [], "statuses": []})

        for run in self.store.get_runs(days=7):
            for result in run.get("data", {}).get("results", []):
                name = result.get("test_name", "unknown")
                test_stats[name]["runs"] += 1
                if result.get("status") == "passed":
                    test_stats[name]["passed"] += 1
                test_stats[name]["durations"].append(result.get("duration_seconds", 0))
                test_stats[name]["statuses"].append(result.get("status", "unknown"))

        trends = []
        for name, stats in test_stats.items():
            pass_rate = (stats["passed"] / stats["runs"] * 100) if stats["runs"] > 0 else 0
            avg_duration = sum(stats["durations"]) / len(stats["durations"]) if stats["durations"] else 0

            # Detect flaky tests (fail sometimes but not always)
            flaky = 0 < stats["passed"] < stats["runs"] and stats["runs"] >= 3

            trends.append(TestTrend(
                test_name=name,
                total_runs=stats["runs"],
                pass_rate=round(pass_rate, 2),
                avg_duration=round(avg_duration, 2),
                recent_status=stats["statuses"][-10:],
                flaky=flaky
            ))

        return sorted(trends, key=lambda t: t.pass_rate)

    def generate_html(self, output_path: str = None) -> str:
        """
        Generate HTML report.

        Args:
            output_path: Optional path to save the report

        Returns:
            HTML content
        """
        report = self._build_report_data()

        # Determine status color
        if report.summary.get("pass_rate", 0) >= 90:
            status_color = "#28a745"  # green
            status_text = "HEALTHY"
        elif report.summary.get("pass_rate", 0) >= 70:
            status_color = "#ffc107"  # yellow
            status_text = "WARNING"
        else:
            status_color = "#dc3545"  # red
            status_text = "FAILING"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report.title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{
            background: #1a1a2e;
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        h1 {{ font-size: 2rem; margin-bottom: 10px; }}
        .status-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            background: {status_color};
            color: white;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-card .number {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #1a1a2e;
        }}
        .summary-card .label {{ color: #666; font-size: 0.9rem; }}
        .passed .number {{ color: #28a745; }}
        .failed .number {{ color: #dc3545; }}
        .section {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h2 {{ color: #1a1a2e; margin-bottom: 15px; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background: #f8f9fa; font-weight: 600; }}
        .status-passed {{ color: #28a745; }}
        .status-failed {{ color: #dc3545; }}
        .status-error {{ color: #dc3545; }}
        .status-skipped {{ color: #6c757d; }}
        .status-timeout {{ color: #fd7e14; }}
        .failure-detail {{
            background: #fff5f5;
            border-left: 4px solid #dc3545;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 0 4px 4px 0;
        }}
        .failure-detail h4 {{ color: #dc3545; margin-bottom: 5px; }}
        .failure-detail pre {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 0.85rem;
        }}
        .trend-indicator {{
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 2px;
        }}
        .trend-pass {{ background: #28a745; }}
        .trend-fail {{ background: #dc3545; }}
        .flaky-badge {{
            background: #ffc107;
            color: #000;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.75rem;
        }}
        footer {{
            text-align: center;
            color: #666;
            padding: 20px;
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{report.title}</h1>
            <p>Generated: {report.generated_at}</p>
            <span class="status-badge">{status_text}</span>
        </header>

        <div class="summary-grid">
            <div class="summary-card">
                <div class="number">{report.summary.get('total', 0)}</div>
                <div class="label">Total Tests</div>
            </div>
            <div class="summary-card passed">
                <div class="number">{report.summary.get('passed', 0)}</div>
                <div class="label">Passed</div>
            </div>
            <div class="summary-card failed">
                <div class="number">{report.summary.get('failed', 0)}</div>
                <div class="label">Failed</div>
            </div>
            <div class="summary-card">
                <div class="number">{report.summary.get('errors', 0)}</div>
                <div class="label">Errors</div>
            </div>
            <div class="summary-card">
                <div class="number">{report.summary.get('pass_rate', 0)}%</div>
                <div class="label">Pass Rate</div>
            </div>
            <div class="summary-card">
                <div class="number">{report.summary.get('duration', 0):.1f}s</div>
                <div class="label">Duration</div>
            </div>
        </div>
"""

        # Failures section
        if report.failures:
            html += """
        <div class="section">
            <h2>Failures</h2>
"""
            for failure in report.failures:
                error_msg = failure.get('error_message', 'No error message')
                # Escape HTML
                error_msg = error_msg.replace('<', '&lt;').replace('>', '&gt;')
                html += f"""
            <div class="failure-detail">
                <h4>{failure.get('test_name', 'Unknown')}</h4>
                <p><strong>Status:</strong> {failure.get('status', 'unknown')}</p>
                <p><strong>Duration:</strong> {failure.get('duration_seconds', 0):.2f}s</p>
                <pre>{error_msg}</pre>
            </div>
"""
            html += "        </div>\n"

        # All results table
        html += """
        <div class="section">
            <h2>All Test Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Attempt</th>
                    </tr>
                </thead>
                <tbody>
"""
        for result in report.results:
            status = result.get('status', 'unknown')
            html += f"""
                    <tr>
                        <td>{result.get('test_name', 'Unknown')}</td>
                        <td class="status-{status}">{status.upper()}</td>
                        <td>{result.get('duration_seconds', 0):.2f}s</td>
                        <td>{result.get('attempt', 1)}</td>
                    </tr>
"""
        html += """
                </tbody>
            </table>
        </div>
"""

        # Trends section
        if report.trends:
            html += """
        <div class="section">
            <h2>Test Trends (Last 7 Days)</h2>
            <table>
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Runs</th>
                        <th>Pass Rate</th>
                        <th>Avg Duration</th>
                        <th>Recent</th>
                    </tr>
                </thead>
                <tbody>
"""
            for trend in report.trends:
                recent_html = ""
                for status in trend.recent_status[-10:]:
                    css_class = "trend-pass" if status == "passed" else "trend-fail"
                    recent_html += f'<span class="trend-indicator {css_class}"></span>'

                flaky_html = '<span class="flaky-badge">FLAKY</span>' if trend.flaky else ""

                html += f"""
                    <tr>
                        <td>{trend.test_name} {flaky_html}</td>
                        <td>{trend.total_runs}</td>
                        <td>{trend.pass_rate}%</td>
                        <td>{trend.avg_duration:.2f}s</td>
                        <td>{recent_html}</td>
                    </tr>
"""
            html += """
                </tbody>
            </table>
        </div>
"""

        html += f"""
        <footer>
            <p>Generated by PRINTMAXX Test Report Generator</p>
            <p>Report Version: {report.metadata.get('report_version', '1.0')}</p>
        </footer>
    </div>
</body>
</html>
"""

        if output_path:
            with open(output_path, 'w') as f:
                f.write(html)
            logger.info(f"HTML report saved to: {output_path}")

        return html

    def generate_markdown(self, output_path: str = None) -> str:
        """
        Generate Markdown report.

        Args:
            output_path: Optional path to save the report

        Returns:
            Markdown content
        """
        report = self._build_report_data()

        # Status emoji
        if report.summary.get("pass_rate", 0) >= 90:
            status_emoji = "pass"
        elif report.summary.get("pass_rate", 0) >= 70:
            status_emoji = "warn"
        else:
            status_emoji = "fail"

        md = f"""# {report.title}

**Generated:** {report.generated_at}

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | {report.summary.get('total', 0)} |
| Passed | {report.summary.get('passed', 0)} |
| Failed | {report.summary.get('failed', 0)} |
| Errors | {report.summary.get('errors', 0)} |
| Skipped | {report.summary.get('skipped', 0)} |
| Pass Rate | {report.summary.get('pass_rate', 0)}% |
| Duration | {report.summary.get('duration', 0):.2f}s |

"""

        # Failures
        if report.failures:
            md += "## Failures\n\n"
            for failure in report.failures:
                md += f"""### {failure.get('test_name', 'Unknown')}

- **Status:** {failure.get('status', 'unknown')}
- **Duration:** {failure.get('duration_seconds', 0):.2f}s
- **Error:** {failure.get('error_message', 'No error message')}

"""

        # All results
        md += """## All Test Results

| Test | Status | Duration | Attempt |
|------|--------|----------|---------|
"""
        for result in report.results:
            status = result.get('status', 'unknown')
            md += f"| {result.get('test_name', 'Unknown')} | {status.upper()} | {result.get('duration_seconds', 0):.2f}s | {result.get('attempt', 1)} |\n"

        # Trends
        if report.trends:
            md += """
## Test Trends (Last 7 Days)

| Test | Runs | Pass Rate | Avg Duration | Flaky |
|------|------|-----------|--------------|-------|
"""
            for trend in report.trends:
                flaky = "Yes" if trend.flaky else "No"
                md += f"| {trend.test_name} | {trend.total_runs} | {trend.pass_rate}% | {trend.avg_duration:.2f}s | {flaky} |\n"

        md += f"""
---
*Generated by PRINTMAXX Test Report Generator*
"""

        if output_path:
            with open(output_path, 'w') as f:
                f.write(md)
            logger.info(f"Markdown report saved to: {output_path}")

        return md

    def generate_json(self, output_path: str = None) -> Dict[str, Any]:
        """
        Generate JSON report.

        Args:
            output_path: Optional path to save the report

        Returns:
            Report data as dict
        """
        report = self._build_report_data()

        data = {
            "title": report.title,
            "generated_at": report.generated_at,
            "summary": report.summary,
            "results": report.results,
            "failures": report.failures,
            "trends": [
                {
                    "test_name": t.test_name,
                    "total_runs": t.total_runs,
                    "pass_rate": t.pass_rate,
                    "avg_duration": t.avg_duration,
                    "flaky": t.flaky,
                    "recent_status": t.recent_status
                }
                for t in report.trends
            ],
            "metadata": report.metadata
        }

        if output_path:
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"JSON report saved to: {output_path}")

        return data

    def generate_badge(self, output_path: str = None) -> str:
        """
        Generate a shields.io compatible badge URL.

        Args:
            output_path: Optional path to save badge JSON

        Returns:
            Badge URL
        """
        report = self._build_report_data()
        pass_rate = report.summary.get("pass_rate", 0)

        if pass_rate >= 90:
            color = "brightgreen"
        elif pass_rate >= 70:
            color = "yellow"
        else:
            color = "red"

        badge_url = f"https://img.shields.io/badge/tests-{pass_rate}%25%20passing-{color}"

        # Also generate shields.io endpoint JSON
        badge_data = {
            "schemaVersion": 1,
            "label": "tests",
            "message": f"{pass_rate}% passing",
            "color": color
        }

        if output_path:
            with open(output_path, 'w') as f:
                json.dump(badge_data, f, indent=2)
            logger.info(f"Badge JSON saved to: {output_path}")

        return badge_url

    def generate_email_summary(self) -> str:
        """Generate a plain text summary suitable for email."""
        report = self._build_report_data()

        status = "PASSING" if report.summary.get("pass_rate", 0) >= 90 else "FAILING"

        summary = f"""PRINTMAXX Test Report - {status}
{'=' * 40}

Summary:
  Total:     {report.summary.get('total', 0)}
  Passed:    {report.summary.get('passed', 0)}
  Failed:    {report.summary.get('failed', 0)}
  Errors:    {report.summary.get('errors', 0)}
  Pass Rate: {report.summary.get('pass_rate', 0)}%
  Duration:  {report.summary.get('duration', 0):.2f}s

"""

        if report.failures:
            summary += "Failures:\n"
            for failure in report.failures:
                summary += f"  - {failure.get('test_name')}: {failure.get('error_message', 'No message')[:100]}\n"

        summary += f"\nGenerated: {report.generated_at}"

        return summary


# CLI
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test Report Generator")
    parser.add_argument("--input", "-i", help="Input JSON results file")
    parser.add_argument("--format", "-f", choices=["html", "markdown", "json", "badge", "email"],
                        default="html", help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--history", action="store_true", help="Include historical trends")
    parser.add_argument("--days", type=int, default=7, help="Days of history for trends")

    args = parser.parse_args()

    generator = TestReportGenerator()

    if args.input:
        generator.load_from_file(args.input)
    else:
        # Try to load most recent results
        log_files = sorted(LOG_DIR.glob("bulk_test_results_*.json"), reverse=True)
        if log_files:
            generator.load_from_file(str(log_files[0]))
            print(f"Loaded: {log_files[0].name}")
        else:
            print("No test results found. Run tests first or specify --input")
            sys.exit(1)

    # Generate output
    if args.format == "html":
        output = args.output or str(LOG_DIR / "test_report.html")
        generator.generate_html(output)
        print(f"HTML report: {output}")

    elif args.format == "markdown":
        output = args.output or str(LOG_DIR / "test_report.md")
        generator.generate_markdown(output)
        print(f"Markdown report: {output}")

    elif args.format == "json":
        output = args.output or str(LOG_DIR / "test_report.json")
        generator.generate_json(output)
        print(f"JSON report: {output}")

    elif args.format == "badge":
        output = args.output or str(LOG_DIR / "badge.json")
        badge_url = generator.generate_badge(output)
        print(f"Badge URL: {badge_url}")
        print(f"Badge JSON: {output}")

    elif args.format == "email":
        summary = generator.generate_email_summary()
        if args.output:
            with open(args.output, 'w') as f:
                f.write(summary)
            print(f"Email summary: {args.output}")
        else:
            print(summary)
