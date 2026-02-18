#!/usr/bin/env python3
"""
Daily Report Generator - Creates markdown reports from alpha scan results
Summarizes top findings, action items, and metrics.
Saves to OPS/reports/

Usage:
    generator = DailyReportGenerator()
    report_path = generator.generate_report(scan_results, output_dir)
"""

import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger('ReportGenerator')


class DailyReportGenerator:
    """Generates daily alpha research reports in markdown format."""

    def __init__(self):
        self.template = self._load_template()

    def _load_template(self) -> str:
        """Load report template."""
        return """# Alpha Research Report - {date}

## Scan Summary

| Metric | Value |
|--------|-------|
| Sources Scanned | {sources_scanned} |
| New Findings | {findings_count} |
| Errors | {errors_count} |
| Scan Duration | {duration} |
| Started | {started_at} |
| Completed | {completed_at} |

---

## Category Breakdown

{category_breakdown}

---

## Source Breakdown

{source_breakdown}

---

## Top Priority Findings

{top_findings}

---

## Findings by Signal Level

### HIGHEST Signal
{highest_signal}

### HIGH Signal
{high_signal}

### MEDIUM Signal
{medium_signal}

---

## ChatGPT Ads Update

{chatgpt_ads_update}

---

## Action Items

{action_items}

---

## Errors & Issues

{errors_section}

---

## Next Steps

1. Review ALPHA_STAGING.csv entries marked PENDING_REVIEW
2. Mark each as APPROVED or REJECTED
3. Run `/review-alpha` to integrate approved entries
4. Update ALPHA_WATCHLIST.csv with new tracking items

---

*Report generated: {generated_at}*
"""

    def generate_report(
        self,
        scan_results: dict,
        output_dir: Path,
        filename: Optional[str] = None
    ) -> Path:
        """
        Generate a markdown report from scan results.

        Args:
            scan_results: Dictionary containing scan results
            output_dir: Directory to save report
            filename: Optional custom filename

        Returns:
            Path to generated report
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        date_str = datetime.now().strftime('%Y-%m-%d')
        if filename:
            report_name = filename
        else:
            report_name = f"alpha_research_{date_str}.md"

        report_path = output_dir / report_name

        # Calculate metrics
        findings = scan_results.get('findings', [])
        errors = scan_results.get('errors', [])

        # Calculate duration
        started = scan_results.get('started_at', '')
        completed = scan_results.get('completed_at', '')
        duration = self._calculate_duration(started, completed)

        # Get category breakdown
        category_breakdown = self._format_category_breakdown(findings)

        # Get source breakdown
        source_breakdown = self._format_source_breakdown(findings)

        # Get top findings
        top_findings = self._format_top_findings(findings, limit=5)

        # Get findings by signal level
        highest = self._filter_by_signal(findings, 'HIGHEST')
        high = self._filter_by_signal(findings, 'HIGH')
        medium = self._filter_by_signal(findings, 'MEDIUM')

        # Check for ChatGPT ads mentions
        chatgpt_update = self._check_chatgpt_ads(findings)

        # Generate action items
        action_items = self._generate_action_items(findings)

        # Format errors
        errors_section = self._format_errors(errors)

        # Fill template
        report_content = self.template.format(
            date=date_str,
            sources_scanned=scan_results.get('sources_scanned', 0),
            findings_count=len(findings),
            errors_count=len(errors),
            duration=duration,
            started_at=started[:19] if started else 'N/A',
            completed_at=completed[:19] if completed else 'N/A',
            category_breakdown=category_breakdown,
            source_breakdown=source_breakdown,
            top_findings=top_findings,
            highest_signal=self._format_signal_findings(highest),
            high_signal=self._format_signal_findings(high),
            medium_signal=self._format_signal_findings(medium),
            chatgpt_ads_update=chatgpt_update,
            action_items=action_items,
            errors_section=errors_section,
            generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        # Write report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        logger.info(f"Report generated: {report_path}")
        return report_path

    def _calculate_duration(self, started: str, completed: str) -> str:
        """Calculate scan duration as human-readable string."""
        if not started or not completed:
            return 'N/A'

        try:
            start_dt = datetime.fromisoformat(started.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(completed.replace('Z', '+00:00'))
            delta = end_dt - start_dt

            minutes = delta.total_seconds() / 60
            if minutes < 1:
                return f"{int(delta.total_seconds())} seconds"
            elif minutes < 60:
                return f"{int(minutes)} minutes"
            else:
                hours = minutes / 60
                return f"{hours:.1f} hours"
        except Exception:
            return 'N/A'

    def _format_category_breakdown(self, findings: list) -> str:
        """Format category breakdown as markdown table."""
        if not findings:
            return "No findings to categorize."

        categories = {}
        for f in findings:
            cats = f.get('category', 'GENERAL').split('|')
            for cat in cats:
                categories[cat] = categories.get(cat, 0) + 1

        if not categories:
            return "No categories found."

        lines = ["| Category | Count |", "|----------|-------|"]
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            lines.append(f"| {cat} | {count} |")

        return '\n'.join(lines)

    def _format_source_breakdown(self, findings: list) -> str:
        """Format source breakdown as markdown table."""
        if not findings:
            return "No findings to analyze."

        sources = {}
        for f in findings:
            source = f.get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1

        if not sources:
            return "No sources found."

        lines = ["| Source | Count |", "|--------|-------|"]
        for source, count in sorted(sources.items(), key=lambda x: -x[1])[:15]:
            lines.append(f"| {source} | {count} |")

        return '\n'.join(lines)

    def _format_top_findings(self, findings: list, limit: int = 5) -> str:
        """Format top priority findings."""
        if not findings:
            return "No findings to display."

        # Sort by signal level priority
        signal_priority = {'HIGHEST': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        sorted_findings = sorted(
            findings,
            key=lambda x: signal_priority.get(x.get('roi_potential', 'LOW'), 0),
            reverse=True
        )

        lines = []
        for i, f in enumerate(sorted_findings[:limit], 1):
            title = f.get('title', 'Untitled')[:80]
            source = f.get('source', 'Unknown')
            signal = f.get('roi_potential', 'N/A')
            category = f.get('category', 'GENERAL').split('|')[0]

            lines.append(f"### {i}. [{signal}] {title}")
            lines.append(f"**Source:** {source} | **Category:** {category}")
            lines.append("")

            description = f.get('description', '')[:200]
            if description:
                lines.append(f"> {description}...")
                lines.append("")

            url = f.get('source_url', '')
            if url:
                lines.append(f"[View Source]({url})")
                lines.append("")

            lines.append("---")
            lines.append("")

        return '\n'.join(lines) if lines else "No priority findings."

    def _filter_by_signal(self, findings: list, signal: str) -> list:
        """Filter findings by signal level."""
        return [f for f in findings if f.get('roi_potential') == signal]

    def _format_signal_findings(self, findings: list) -> str:
        """Format findings for a signal level section."""
        if not findings:
            return "_No findings at this signal level._"

        lines = []
        for f in findings[:10]:  # Limit per section
            title = f.get('title', 'Untitled')[:60]
            source = f.get('source', 'Unknown')
            lines.append(f"- **{title}** ({source})")

        if len(findings) > 10:
            lines.append(f"- _...and {len(findings) - 10} more_")

        return '\n'.join(lines)

    def _check_chatgpt_ads(self, findings: list) -> str:
        """Check for ChatGPT ads related findings."""
        chatgpt_mentions = []

        for f in findings:
            content = (f.get('description', '') + f.get('title', '')).lower()
            if any(term in content for term in ['chatgpt ads', 'openai ads', 'chatgpt advertising']):
                chatgpt_mentions.append(f)

        if not chatgpt_mentions:
            return """**Status:** No new ChatGPT ads updates found this scan.

**Action:** Continue monitoring @openai and tech news for announcements.

**Key Question:** Is there early mover advantage like TikTok ads 2019?"""

        lines = ["**New Updates Found:**", ""]
        for f in chatgpt_mentions:
            lines.append(f"- {f.get('title', 'Untitled')}")
            if f.get('source_url'):
                lines.append(f"  [Source]({f.get('source_url')})")
            lines.append("")

        return '\n'.join(lines)

    def _generate_action_items(self, findings: list) -> str:
        """Generate action items from findings."""
        if not findings:
            return "- [ ] Run another scan with expanded sources"

        # Find highest priority items
        highest = self._filter_by_signal(findings, 'HIGHEST')
        high = self._filter_by_signal(findings, 'HIGH')

        lines = []

        if highest:
            lines.append("### Immediate (HIGHEST Signal)")
            for f in highest[:3]:
                title = f.get('title', 'Untitled')[:50]
                lines.append(f"- [ ] Review: {title}")

        if high:
            lines.append("")
            lines.append("### This Week (HIGH Signal)")
            for f in high[:5]:
                title = f.get('title', 'Untitled')[:50]
                lines.append(f"- [ ] Evaluate: {title}")

        # Category-specific actions
        categories = {}
        for f in findings:
            for cat in f.get('category', '').split('|'):
                categories[cat] = categories.get(cat, 0) + 1

        if 'TOOL_ALPHA' in categories:
            lines.append("")
            lines.append("### Tools to Test")
            tool_findings = [f for f in findings if 'TOOL_ALPHA' in f.get('category', '')]
            for f in tool_findings[:3]:
                lines.append(f"- [ ] Test: {f.get('title', '')[:40]}")

        if 'COMPETITOR' in categories:
            lines.append("")
            lines.append("### Competitor Intel")
            lines.append("- [ ] Update competitive analysis")

        return '\n'.join(lines) if lines else "- [ ] Review all staged findings"

    def _format_errors(self, errors: list) -> str:
        """Format error section."""
        if not errors:
            return "_No errors during this scan._"

        lines = []
        for err in errors:
            source = err.get('source', 'Unknown')
            error_msg = err.get('error', 'Unknown error')
            lines.append(f"- **{source}:** {error_msg}")

        return '\n'.join(lines)

    def generate_summary_email(self, scan_results: dict) -> str:
        """Generate a short summary suitable for email/Slack."""
        findings = scan_results.get('findings', [])
        errors = scan_results.get('errors', [])

        highest = len(self._filter_by_signal(findings, 'HIGHEST'))
        high = len(self._filter_by_signal(findings, 'HIGH'))

        summary = f"""Alpha Research Summary - {datetime.now().strftime('%Y-%m-%d')}

Scanned: {scan_results.get('sources_scanned', 0)} sources
New Findings: {len(findings)} total
  - HIGHEST: {highest}
  - HIGH: {high}
Errors: {len(errors)}

"""
        if findings:
            summary += "Top Finding:\n"
            top = sorted(
                findings,
                key=lambda x: {'HIGHEST': 4, 'HIGH': 3, 'MEDIUM': 2}.get(x.get('roi_potential', ''), 0),
                reverse=True
            )[0]
            summary += f"  {top.get('title', 'Untitled')[:60]}\n"
            summary += f"  Source: {top.get('source', 'Unknown')}\n"

        summary += "\nAction: Review ALPHA_STAGING.csv"

        return summary


# Standalone test
def _test():
    """Test the report generator."""
    generator = DailyReportGenerator()

    # Sample results
    results = {
        'sources_scanned': 15,
        'findings': [
            {
                'alpha_id': 'ALPHA_001',
                'source': '@levelsio',
                'source_url': 'https://x.com/levelsio/status/123',
                'category': 'APP_FACTORY|MONETIZATION',
                'title': 'Made $50k MRR with simple SaaS...',
                'description': 'Full breakdown of how I built and monetized a simple SaaS product.',
                'roi_potential': 'HIGHEST'
            },
            {
                'alpha_id': 'ALPHA_002',
                'source': 'r/SideProject',
                'source_url': 'https://reddit.com/r/SideProject/123',
                'category': 'GROWTH_HACK',
                'title': 'TikTok distribution strategy that worked...',
                'description': 'Got 10k downloads in a week using this TikTok strategy.',
                'roi_potential': 'HIGH'
            },
            {
                'alpha_id': 'ALPHA_003',
                'source': 'HackerNews',
                'source_url': 'https://news.ycombinator.com/item?id=456',
                'category': 'TOOL_ALPHA',
                'title': 'Show HN: New automation tool...',
                'description': 'Built a tool to automate content scheduling.',
                'roi_potential': 'MEDIUM'
            }
        ],
        'errors': [
            {'source': '@someAccount', 'error': 'Rate limited'}
        ],
        'started_at': '2026-01-21T09:00:00',
        'completed_at': '2026-01-21T09:15:30'
    }

    # Generate report
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        report_path = generator.generate_report(results, Path(tmpdir))
        print(f"Report generated: {report_path}")

        with open(report_path, 'r') as f:
            print("\n" + "=" * 60)
            print(f.read())

    # Generate email summary
    print("\n" + "=" * 60)
    print("EMAIL SUMMARY:")
    print(generator.generate_summary_email(results))


if __name__ == '__main__':
    _test()
