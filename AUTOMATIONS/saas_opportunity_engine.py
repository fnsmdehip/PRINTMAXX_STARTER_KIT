#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX SaaS Opportunity Engine - SCRIPT-TO-SAAS ANALYZER

Scans all 210+ scripts in AUTOMATIONS/ and scores each for SaaS-ification potential.
Parses CLI interfaces, estimates market size, defensibility, recurring potential.
Generates landing page copy, pricing tiers, and feature comparisons for top candidates.

Output: OPS/SAAS_MANIFEST_V2.md

Usage:
    python3 saas_opportunity_engine.py --scan                    # Full scan all scripts
    python3 saas_opportunity_engine.py --deep-analyze 10         # Deep analysis of top N
    python3 saas_opportunity_engine.py --generate-landing APP    # Landing page copy
    python3 saas_opportunity_engine.py --pricing APP             # Pricing breakdown
    python3 saas_opportunity_engine.py --manifest                # Output full manifest
"""

import argparse
import ast
import json
import os
import re
import sys
import textwrap
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR = PROJECT_ROOT / "AUTOMATIONS"
OPS_DIR = PROJECT_ROOT / "OPS"
OUTPUT_MANIFEST = OPS_DIR / "SAAS_MANIFEST_V2.md"
LOG_FILE = AUTOMATIONS_DIR / "logs" / f"saas_engine_{datetime.now().strftime('%Y-%m-%d')}.log"

# ============================================================
# SCORING WEIGHTS
# ============================================================

SCORE_WEIGHTS = {
    'market_size': 0.30,
    'defensibility': 0.20,
    'recurring_potential': 0.30,
    'api_difficulty': 0.20,  # inverted: lower difficulty = higher score
}

# ============================================================
# MARKET SIZE INDICATORS (keyword -> estimated market score)
# ============================================================

MARKET_KEYWORDS = {
    # Large markets (score 70-100)
    'lead': 90, 'leads': 90, 'email': 85, 'cold_email': 85, 'outreach': 85,
    'seo': 80, 'content': 75, 'social': 75, 'video': 80, 'clip': 78,
    'ecom': 85, 'product': 70, 'ad': 80, 'ads': 80, 'marketing': 75,
    'sales': 85, 'crm': 80, 'analytics': 75, 'scraper': 70, 'scrape': 70,
    'monitor': 72, 'track': 68, 'automat': 75, 'pipeline': 78,
    'freelance': 72, 'invoice': 70, 'client': 75, 'prospect': 80,
    'competitor': 78, 'pricing': 75, 'arb': 65, 'arbitrage': 65,

    # Medium markets (score 40-69)
    'reddit': 55, 'twitter': 60, 'instagram': 58, 'tiktok': 62,
    'youtube': 65, 'podcast': 55, 'newsletter': 60, 'blog': 50,
    'keyword': 65, 'aso': 55, 'app': 60, 'clone': 45,
    'resume': 55, 'cover_letter': 50, 'portfolio': 48,
    'crypto': 50, 'meme_coin': 35, 'trading': 55,
    'backup': 40, 'deploy': 45, 'cron': 35,

    # Niche markets (score 10-39)
    'guardrail': 15, 'health': 30, 'compliance': 35, 'audit': 38,
    'memory': 20, 'brain': 18, 'subconscious': 10, 'overnight': 15,
    'venture': 30, 'alpha': 25, 'quant': 35,
}

# ============================================================
# EDGE TACTIC CLASSIFIERS
# ============================================================

EDGE_TACTICS = {
    'picks_and_shovels': {
        'description': 'Sell tools to gold rushers, not pan for gold yourself',
        'keywords': ['lead', 'scraper', 'monitor', 'track', 'analytics', 'report',
                     'scan', 'audit', 'check', 'validate', 'score'],
        'multiplier': 1.15,
    },
    'api_arbitrage': {
        'description': 'Wrap expensive APIs in simple UX, charge markup on convenience',
        'keywords': ['api', 'openai', 'gpt', 'claude', 'whisper', 'elevenlabs',
                     'replicate', 'anthropic', 'scrape', 'fetch', 'request'],
        'multiplier': 1.10,
    },
    'vertical_saas': {
        'description': 'Generic tool narrowed to specific vertical = 10x pricing power',
        'keywords': ['niche', 'specific', 'vertical', 'industry', 'sector',
                     'freelance', 'agency', 'ecom', 'creator', 'solopreneur'],
        'multiplier': 1.20,
    },
    'productized_service': {
        'description': 'Automate what agencies charge $5K/mo for, sell at $99/mo',
        'keywords': ['cold_email', 'outreach', 'content', 'seo', 'social',
                     'posting', 'scheduling', 'campaign', 'funnel', 'ad'],
        'multiplier': 1.12,
    },
    'data_moat': {
        'description': 'Accumulate proprietary data that compounds over time',
        'keywords': ['scrape', 'collect', 'aggregate', 'trend', 'signal',
                     'history', 'archive', 'database', 'index', 'crawl'],
        'multiplier': 1.18,
    },
}

# ============================================================
# PRICING TIERS
# ============================================================

PRICING_TIERS = {
    'starter': {
        'price': 9,
        'name': 'Starter',
        'limits': '100 runs/mo, 1 user, basic features',
        'target': 'side hustlers testing the waters',
    },
    'growth': {
        'price': 29,
        'name': 'Growth',
        'limits': '1,000 runs/mo, 3 users, all features, email support',
        'target': 'serious solopreneurs scaling up',
    },
    'scale': {
        'price': 99,
        'name': 'Scale',
        'limits': 'Unlimited runs, 10 users, API access, priority support, custom integrations',
        'target': 'agencies and teams printing money',
    },
}

# ============================================================
# SCRIPT PARSER
# ============================================================

class ScriptAnalyzer:
    """Parses a Python script to extract metadata for SaaS scoring."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.name = filepath.stem
        self.content = ''
        self.lines = []
        self.docstring = ''
        self.imports = []
        self.cli_args = []
        self.functions = []
        self.classes = []
        self.line_count = 0
        self.has_argparse = False
        self.has_cli = False
        self.has_output = False
        self.output_formats = []
        self.external_deps = []
        self.api_calls = []
        self.error_handling_score = 0
        self._parse()

    def _parse(self):
        """Parse the script file."""
        try:
            self.content = self.filepath.read_text(encoding='utf-8', errors='replace')
        except Exception:
            return

        self.lines = self.content.split('\n')
        self.line_count = len(self.lines)

        # Extract docstring
        self._extract_docstring()

        # Parse AST for structured info
        self._parse_ast()

        # Regex-based extraction for things AST misses
        self._extract_cli_args()
        self._extract_imports()
        self._detect_outputs()
        self._detect_api_calls()
        self._score_error_handling()

    def _extract_docstring(self):
        """Extract module-level docstring."""
        match = re.search(r'^"""(.*?)"""', self.content, re.DOTALL)
        if not match:
            match = re.search(r"^'''(.*?)'''", self.content, re.DOTALL)
        if match:
            self.docstring = match.group(1).strip()

    def _parse_ast(self):
        """Parse AST to extract functions, classes."""
        try:
            tree = ast.parse(self.content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.functions.append({
                    'name': node.name,
                    'args': [a.arg for a in node.args.args if a.arg != 'self'],
                    'lineno': node.lineno,
                    'has_docstring': (
                        isinstance(node.body[0], ast.Expr) and
                        isinstance(node.body[0].value, (ast.Constant, ast.Str))
                    ) if node.body else False,
                })
            elif isinstance(node, ast.ClassDef):
                self.classes.append({
                    'name': node.name,
                    'lineno': node.lineno,
                    'methods': [
                        n.name for n in node.body
                        if isinstance(n, ast.FunctionDef)
                    ],
                })

    def _extract_cli_args(self):
        """Extract argparse arguments."""
        # Check for argparse usage
        if 'argparse' in self.content:
            self.has_argparse = True
            self.has_cli = True

        # Extract add_argument calls
        arg_pattern = re.compile(
            r"add_argument\(\s*['\"](-{1,2}[\w-]+)['\"]"
            r"(?:.*?help\s*=\s*['\"]([^'\"]+)['\"])?"
            , re.DOTALL
        )
        for match in arg_pattern.finditer(self.content):
            self.cli_args.append({
                'flag': match.group(1),
                'help': match.group(2) or '',
            })

        # Check for sys.argv or click
        if 'sys.argv' in self.content:
            self.has_cli = True
        if 'import click' in self.content or 'from click' in self.content:
            self.has_cli = True

    def _extract_imports(self):
        """Extract external dependencies."""
        import_pattern = re.compile(r'^(?:import|from)\s+([\w.]+)', re.MULTILINE)
        stdlib_modules = {
            'os', 'sys', 'json', 'csv', 're', 'time', 'datetime', 'pathlib',
            'argparse', 'subprocess', 'shutil', 'hashlib', 'random', 'math',
            'collections', 'functools', 'itertools', 'typing', 'abc',
            'urllib', 'http', 'email', 'html', 'xml', 'sqlite3', 'socket',
            'threading', 'multiprocessing', 'logging', 'unittest', 'io',
            'tempfile', 'glob', 'fnmatch', 'struct', 'copy', 'pprint',
            'textwrap', 'string', 'types', 'ast', 'inspect', 'traceback',
            'base64', 'binascii', 'uuid', 'secrets', 'hmac', 'contextlib',
            'signal', 'platform', 'sched', 'queue', 'heapq', 'bisect',
            'array', 'enum', 'dataclasses', 'decimal', 'fractions',
            'statistics', 'operator', 'warnings', 'weakref',
        }

        for match in import_pattern.finditer(self.content):
            module = match.group(1).split('.')[0]
            if module not in stdlib_modules:
                self.external_deps.append(module)

        self.external_deps = list(set(self.external_deps))

    def _detect_outputs(self):
        """Detect what output formats the script produces."""
        if re.search(r'\.csv', self.content, re.IGNORECASE):
            self.output_formats.append('CSV')
            self.has_output = True
        if re.search(r'\.json', self.content, re.IGNORECASE):
            self.output_formats.append('JSON')
            self.has_output = True
        if re.search(r'\.md', self.content, re.IGNORECASE):
            self.output_formats.append('Markdown')
            self.has_output = True
        if re.search(r'\.html', self.content, re.IGNORECASE):
            self.output_formats.append('HTML')
            self.has_output = True
        if re.search(r'\.xlsx?', self.content, re.IGNORECASE):
            self.output_formats.append('Excel')
            self.has_output = True
        if re.search(r'print\(', self.content):
            self.output_formats.append('stdout')
            self.has_output = True

    def _detect_api_calls(self):
        """Detect external API calls."""
        api_patterns = [
            (r'requests\.(?:get|post|put|delete)', 'HTTP requests'),
            (r'urllib\.request', 'urllib'),
            (r'openai', 'OpenAI API'),
            (r'anthropic', 'Anthropic API'),
            (r'selenium|playwright', 'Browser automation'),
            (r'pytrends', 'Google Trends API'),
            (r'tweepy|twitter', 'Twitter API'),
            (r'google\.', 'Google API'),
            (r'stripe', 'Stripe API'),
            (r'sendgrid|mailgun|ses', 'Email API'),
            (r'BeautifulSoup|bs4|lxml', 'Web scraping'),
            (r'scrapy', 'Scrapy framework'),
        ]

        for pattern, name in api_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.api_calls.append(name)

    def _score_error_handling(self):
        """Score quality of error handling."""
        score = 0
        try_count = self.content.count('try:')
        except_count = self.content.count('except')

        if try_count > 0:
            score += 20
        if try_count >= 3:
            score += 15
        if except_count > try_count:
            # More specific except clauses
            score += 10
        if 'logging' in self.content or 'logger' in self.content:
            score += 15
        if 'raise' in self.content:
            score += 10
        if re.search(r'except\s+\w+Error', self.content):
            score += 15
        if 'finally:' in self.content:
            score += 10
        if 'retry' in self.content.lower():
            score += 5

        self.error_handling_score = min(score, 100)

    def summary(self) -> dict:
        """Return analysis summary."""
        return {
            'name': self.name,
            'path': str(self.filepath),
            'line_count': self.line_count,
            'docstring': self.docstring[:200] if self.docstring else '',
            'has_cli': self.has_cli,
            'cli_args': self.cli_args,
            'functions': len(self.functions),
            'classes': len(self.classes),
            'external_deps': self.external_deps,
            'output_formats': self.output_formats,
            'api_calls': self.api_calls,
            'error_handling': self.error_handling_score,
            'function_names': [f['name'] for f in self.functions],
        }


# ============================================================
# SAAS SCORER
# ============================================================

class SaaSScorer:
    """Scores a script's SaaS potential across multiple dimensions."""

    def __init__(self, analysis: dict):
        self.analysis = analysis
        self.name = analysis['name']
        self.scores = {}
        self.edge_tactics = []
        self.composite = 0.0

    def score_all(self) -> dict:
        """Run all scoring dimensions."""
        self.scores['market_size'] = self._score_market_size()
        self.scores['defensibility'] = self._score_defensibility()
        self.scores['recurring_potential'] = self._score_recurring()
        self.scores['api_difficulty'] = self._score_api_difficulty()
        self.edge_tactics = self._classify_edge_tactics()

        # Composite = weighted average
        raw_composite = sum(
            self.scores[dim] * SCORE_WEIGHTS[dim]
            for dim in SCORE_WEIGHTS
        )

        # Apply edge tactic multipliers
        multiplier = 1.0
        for tactic in self.edge_tactics:
            multiplier = max(multiplier, EDGE_TACTICS[tactic]['multiplier'])

        self.composite = min(round(raw_composite * multiplier, 1), 100)
        self.scores['composite'] = self.composite

        return {
            'name': self.name,
            'scores': self.scores,
            'edge_tactics': self.edge_tactics,
            'composite': self.composite,
        }

    def _score_market_size(self) -> int:
        """Score based on keyword matches to known market sizes."""
        name_lower = self.name.lower()
        doc_lower = (self.analysis.get('docstring', '') or '').lower()
        combined = name_lower + ' ' + doc_lower

        # Add function names for richer signal
        func_text = ' '.join(self.analysis.get('function_names', [])).lower()
        combined += ' ' + func_text

        best_score = 10  # baseline
        matching_keywords = []

        for keyword, score in MARKET_KEYWORDS.items():
            if keyword in combined:
                matching_keywords.append((keyword, score))
                if score > best_score:
                    best_score = score

        # Bonus for multiple market matches (intersection = bigger opportunity)
        if len(matching_keywords) >= 3:
            best_score = min(best_score + 10, 100)
        if len(matching_keywords) >= 5:
            best_score = min(best_score + 5, 100)

        # Penalty for very small scripts (< 50 lines = probably not substantial)
        if self.analysis['line_count'] < 50:
            best_score = max(best_score - 20, 5)

        return best_score

    def _score_defensibility(self) -> int:
        """Score how defensible this would be as a SaaS product."""
        score = 20  # baseline

        # Has CLI = designed for users, not just internal
        if self.analysis['has_cli']:
            score += 10

        # Multiple functions = more complex = harder to replicate
        func_count = self.analysis['functions']
        if func_count >= 10:
            score += 15
        elif func_count >= 5:
            score += 10

        # Classes = structured, potentially harder to replicate
        if self.analysis['classes']:
            score += 8

        # Large codebase = more invested effort
        lines = self.analysis['line_count']
        if lines >= 500:
            score += 15
        elif lines >= 200:
            score += 10
        elif lines >= 100:
            score += 5

        # External API integration = integration moat
        if len(self.analysis['api_calls']) >= 2:
            score += 12
        elif len(self.analysis['api_calls']) >= 1:
            score += 6

        # Good error handling = production-ready
        if self.analysis['error_handling'] >= 50:
            score += 10

        # Multiple output formats = more complete product
        if len(self.analysis['output_formats']) >= 2:
            score += 5

        return min(score, 100)

    def _score_recurring(self) -> int:
        """Score recurring revenue potential."""
        score = 20  # baseline
        name_lower = self.name.lower()
        doc_lower = (self.analysis.get('docstring', '') or '').lower()
        combined = name_lower + ' ' + doc_lower

        # Daily/recurring use patterns
        recurring_signals = [
            'daily', 'hourly', 'cron', 'monitor', 'scan', 'track', 'watch',
            'alert', 'report', 'digest', 'recurring', 'schedule', 'pipeline',
            'dashboard', 'continuous', 'stream', 'feed', 'sync',
        ]
        for signal in recurring_signals:
            if signal in combined:
                score += 8

        # CLI with multiple modes = users keep coming back
        if len(self.analysis['cli_args']) >= 3:
            score += 10
        elif len(self.analysis['cli_args']) >= 1:
            score += 5

        # Data accumulation = stickiness
        data_signals = ['csv', 'database', 'history', 'log', 'archive', 'cache']
        for signal in data_signals:
            if signal in combined:
                score += 5

        # Scraping/monitoring = needs to run regularly
        if 'scrape' in combined or 'fetch' in combined or 'request' in combined:
            score += 10

        # Multiple output formats = workflow integration
        if len(self.analysis['output_formats']) >= 2:
            score += 5

        return min(score, 100)

    def _score_api_difficulty(self) -> int:
        """Score how easy it is to wrap as an API. Higher = EASIER (inverted)."""
        score = 50  # baseline

        # Has argparse = already has clear input/output interface
        if self.analysis['has_cli']:
            score += 20

        # Has functions (not just a script blob)
        if self.analysis['functions'] >= 3:
            score += 10

        # Has classes = already modular
        if self.analysis['classes']:
            score += 10

        # Good error handling = less work to productize
        if self.analysis['error_handling'] >= 40:
            score += 10

        # Output to file = can easily return as API response
        if self.analysis['output_formats']:
            score += 5

        # Penalty: browser automation = hard to scale
        if 'Browser automation' in self.analysis.get('api_calls', []):
            score -= 25

        # Penalty: heavy external deps = more infrastructure
        if len(self.analysis['external_deps']) > 8:
            score -= 10
        elif len(self.analysis['external_deps']) > 5:
            score -= 5

        # Penalty: very large script = complex to maintain
        if self.analysis['line_count'] > 800:
            score -= 5

        return max(min(score, 100), 5)

    def _classify_edge_tactics(self) -> list:
        """Classify which edge tactics apply to this script."""
        name_lower = self.name.lower()
        doc_lower = (self.analysis.get('docstring', '') or '').lower()
        func_text = ' '.join(self.analysis.get('function_names', [])).lower()
        combined = name_lower + ' ' + doc_lower + ' ' + func_text

        matching_tactics = []

        for tactic_key, tactic_info in EDGE_TACTICS.items():
            matches = sum(1 for kw in tactic_info['keywords'] if kw in combined)
            if matches >= 2:
                matching_tactics.append(tactic_key)

        return matching_tactics


# ============================================================
# LANDING PAGE GENERATOR
# ============================================================

def generate_saas_name(script_name: str) -> str:
    """Generate a SaaS product name from script name."""
    # Map common patterns to product names
    name_map = {
        'lead': 'LeadMaxx', 'pipeline': 'PipeMaxx', 'clip': 'ClipMaxx',
        'content': 'ContentMaxx', 'seo': 'SEOMaxx', 'ad': 'AdMaxx',
        'email': 'MailMaxx', 'cold': 'ColdMaxx', 'scraper': 'ScrapeMaxx',
        'monitor': 'MonitorMaxx', 'arb': 'ArbMaxx', 'ecom': 'EcomMaxx',
        'social': 'SocialMaxx', 'video': 'VideoMaxx', 'trend': 'TrendMaxx',
        'competitor': 'CompeteMaxx', 'freelance': 'GigMaxx', 'app': 'AppMaxx',
        'clone': 'CloneMaxx', 'pricing': 'PriceMaxx', 'product': 'ProductMaxx',
        'keyword': 'KeywordMaxx', 'reddit': 'RedditMaxx', 'twitter': 'XMaxx',
        'rebalancer': 'MethodMaxx', 'quant': 'QuantMaxx', 'venture': 'VentureMaxx',
        'alpha': 'AlphaMaxx', 'auto': 'AutoMaxx', 'research': 'ResearchMaxx',
        'resume': 'ResumeMaxx', 'deploy': 'DeployMaxx', 'track': 'TrackMaxx',
    }

    name_lower = script_name.lower()
    for keyword, product_name in name_map.items():
        if keyword in name_lower:
            return product_name

    # Fallback: CamelCase + Maxx
    parts = script_name.replace('_', ' ').split()
    camel = ''.join(p.capitalize() for p in parts[:2])
    return f"{camel}Maxx"


def generate_landing_copy(scored_result: dict, analysis: dict) -> str:
    """Generate landing page copy in PRINTMAXXER voice."""
    name = generate_saas_name(analysis['name'])
    docstring = analysis.get('docstring', '') or 'Automated workflow engine'
    composite = scored_result['composite']
    tactics = scored_result.get('edge_tactics', [])
    cli_args = analysis.get('cli_args', [])

    # Extract core functionality from docstring
    first_line = docstring.split('\n')[0].strip() if docstring else 'Automates your workflow'

    # Feature list from CLI args
    features = []
    for arg in cli_args[:8]:
        flag = arg['flag'].lstrip('-').replace('-', ' ')
        help_text = arg.get('help', flag)
        features.append(f"  - {flag}: {help_text}" if help_text else f"  - {flag}")

    if not features:
        # Generate from function names
        for fn in analysis.get('function_names', [])[:8]:
            if not fn.startswith('_'):
                features.append(f"  - {fn.replace('_', ' ')}")

    features_block = '\n'.join(features) if features else '  - Full automation suite'

    # Edge tactic descriptions
    edge_lines = []
    for tactic in tactics:
        info = EDGE_TACTICS.get(tactic, {})
        edge_lines.append(f"  [{tactic.upper()}] {info.get('description', '')}")
    edge_block = '\n'.join(edge_lines) if edge_lines else '  [PICKS_AND_SHOVELS] You sell the tools, not do the digging'

    # Pricing block
    pricing_lines = []
    for tier_key, tier_info in PRICING_TIERS.items():
        pricing_lines.append(
            f"  ${tier_info['price']}/mo — {tier_info['name']}: {tier_info['limits']}"
        )
    pricing_block = '\n'.join(pricing_lines)

    copy = f"""
================================================================================
  {name} — LANDING PAGE COPY
  SaaS Score: {composite}/100
================================================================================

HEADLINE:
  "{first_line.rstrip('.')}. On autopilot."

SUBHEAD:
  stop doing this manually. {name} runs 24/7, finds the opportunities,
  and drops results in your inbox. you sleep, it works.

HERO SECTION:
  i built this because i was tired of running the same script 47 times a day.
  now it runs itself. checks everything. alerts me when there's money on the table.
  you can keep doing it by hand. or you can stop being a peasant about it.

FEATURES:
{features_block}

EDGE TACTICS:
{edge_block}

SOCIAL PROOF SECTION:
  "i was spending 4 hours/day on this manually. {name} does it in 12 minutes."
  "found 3 opportunities in the first scan that paid for 6 months of the tool."
  "borderline illegal how much intel this gives you."

PRICING:
{pricing_block}

CTA:
  "start your free trial. 7 days. no credit card. cancel anytime.
   or keep doing it manually like it's 2019. your call."

FAQ:
  Q: "do I need technical skills?"
  A: "if you can click a button, you can use {name}. we handle the rest."

  Q: "what if it doesn't work for my niche?"
  A: "7-day free trial. test it. if it's not printing money, cancel. we're not
     going to chase you with winback emails like a desperate ex."

  Q: "is this just a wrapper around free tools?"
  A: "it's an engine that combines 5+ data sources, scores everything, and
     tells you exactly what to do. could you build it yourself? sure. will you?
     no. that's why we exist."
================================================================================
"""
    return copy


# ============================================================
# PRICING ANALYZER
# ============================================================

def generate_pricing_breakdown(scored_result: dict, analysis: dict) -> str:
    """Generate detailed pricing analysis."""
    name = generate_saas_name(analysis['name'])
    composite = scored_result['composite']

    # Estimate API costs per run
    api_cost_per_run = 0.0
    if 'OpenAI API' in analysis.get('api_calls', []):
        api_cost_per_run += 0.02
    if 'Anthropic API' in analysis.get('api_calls', []):
        api_cost_per_run += 0.03
    if 'HTTP requests' in analysis.get('api_calls', []):
        api_cost_per_run += 0.005
    if 'Web scraping' in analysis.get('api_calls', []):
        api_cost_per_run += 0.01
    if 'Google Trends API' in analysis.get('api_calls', []):
        api_cost_per_run += 0.005
    if api_cost_per_run == 0:
        api_cost_per_run = 0.001  # minimal compute cost

    # Infrastructure cost estimates
    infra_monthly = 25.0  # baseline VPS
    if 'Browser automation' in analysis.get('api_calls', []):
        infra_monthly += 50.0  # headless browser infra

    breakdown = f"""
================================================================================
  {name} — PRICING BREAKDOWN
================================================================================

  TIER COMPARISON:

  {'Feature':<35} {'$9 Starter':<15} {'$29 Growth':<15} {'$99 Scale':<15}
  {'-'*35} {'-'*15} {'-'*15} {'-'*15}
  {'Runs per month':<35} {'100':<15} {'1,000':<15} {'Unlimited':<15}
  {'Users':<35} {'1':<15} {'3':<15} {'10':<15}
  {'Email alerts':<35} {'Daily':<15} {'Hourly':<15} {'Real-time':<15}
  {'CSV export':<35} {'Yes':<15} {'Yes':<15} {'Yes':<15}
  {'API access':<35} {'No':<15} {'No':<15} {'Yes':<15}
  {'Priority support':<35} {'No':<15} {'Email':<15} {'Slack + Call':<15}
  {'Custom integrations':<35} {'No':<15} {'No':<15} {'Yes':<15}
  {'Data retention':<35} {'30 days':<15} {'90 days':<15} {'1 year':<15}
  {'White-label':<35} {'No':<15} {'No':<15} {'Yes':<15}

  UNIT ECONOMICS:

  API cost per run:     ${api_cost_per_run:.4f}
  Infra (monthly):      ${infra_monthly:.2f}

  Starter ($9/mo, 100 runs):
    Revenue:            $9.00
    API costs:          ${api_cost_per_run * 100:.2f}
    Infra (allocated):  ${infra_monthly * 0.05:.2f}
    Gross margin:       ${9.00 - (api_cost_per_run * 100) - (infra_monthly * 0.05):.2f} ({max(0, (9.00 - (api_cost_per_run * 100) - (infra_monthly * 0.05)) / 9.00 * 100):.0f}%)

  Growth ($29/mo, 1000 runs):
    Revenue:            $29.00
    API costs:          ${api_cost_per_run * 1000:.2f}
    Infra (allocated):  ${infra_monthly * 0.15:.2f}
    Gross margin:       ${29.00 - (api_cost_per_run * 1000) - (infra_monthly * 0.15):.2f} ({max(0, (29.00 - (api_cost_per_run * 1000) - (infra_monthly * 0.15)) / 29.00 * 100):.0f}%)

  Scale ($99/mo, ~5000 runs est):
    Revenue:            $99.00
    API costs:          ${api_cost_per_run * 5000:.2f}
    Infra (allocated):  ${infra_monthly * 0.40:.2f}
    Gross margin:       ${99.00 - (api_cost_per_run * 5000) - (infra_monthly * 0.40):.2f} ({max(0, (99.00 - (api_cost_per_run * 5000) - (infra_monthly * 0.40)) / 99.00 * 100):.0f}%)

  BREAK-EVEN ANALYSIS:
    Monthly infra:      ${infra_monthly:.2f}
    Break-even (Starter only): {max(1, int(infra_monthly / 9) + 1)} customers
    Break-even (mixed):        {max(1, int(infra_monthly / 29) + 1)} customers
    Target MRR at 100 customers: ${9 * 50 + 29 * 35 + 99 * 15:,}

  RECOMMENDATION:
    SaaS score {composite}/100 — {'STRONG CANDIDATE. Ship it.' if composite >= 70 else 'VIABLE. Needs differentiation.' if composite >= 50 else 'WEAK. Consider bundling with other tools.'}
================================================================================
"""
    return breakdown


# ============================================================
# MANIFEST GENERATOR
# ============================================================

def generate_manifest(all_scored: list, all_analyses: dict) -> str:
    """Generate full SaaS manifest markdown."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    # Sort by composite score descending
    all_scored.sort(key=lambda x: x['composite'], reverse=True)

    lines = [
        f"# PRINTMAXX SaaS Product Manifest V2",
        f"*Generated: {timestamp}*",
        f"",
        f"**{len(all_scored)} scripts analyzed. Top candidates ranked below.**",
        f"",
        f"## Quick Stats",
        f"- Total scripts scanned: {len(all_scored)}",
        f"- Scripts with CLI interface: {sum(1 for s in all_scored if all_analyses[s['name']]['has_cli'])}",
        f"- Scripts scoring 70+: {sum(1 for s in all_scored if s['composite'] >= 70)}",
        f"- Scripts scoring 50+: {sum(1 for s in all_scored if s['composite'] >= 50)}",
        f"",
        f"## Priority Ranking (Top 30)",
        f"",
        f"| # | Score | Name | SaaS Name | Lines | CLI | Edge Tactics |",
        f"|---|-------|------|-----------|-------|-----|-------------|",
    ]

    for i, scored in enumerate(all_scored[:30], 1):
        analysis = all_analyses[scored['name']]
        saas_name = generate_saas_name(scored['name'])
        tactics_str = ', '.join(scored.get('edge_tactics', [])[:2]) or '-'
        cli_flag = 'Yes' if analysis['has_cli'] else 'No'
        lines.append(
            f"| {i} | {scored['composite']:.0f} | {scored['name']} | "
            f"**{saas_name}** | {analysis['line_count']} | {cli_flag} | {tactics_str} |"
        )

    lines.append("")
    lines.append("## Score Breakdown (Top 15)")
    lines.append("")

    for i, scored in enumerate(all_scored[:15], 1):
        analysis = all_analyses[scored['name']]
        saas_name = generate_saas_name(scored['name'])
        scores = scored['scores']

        lines.append(f"### {i}. {saas_name} (Score: {scored['composite']:.0f}/100)")
        lines.append(f"**Script:** `{scored['name']}.py` ({analysis['line_count']} lines)")

        if analysis.get('docstring'):
            doc_first = analysis['docstring'].split('\n')[0][:100]
            lines.append(f"**Purpose:** {doc_first}")

        lines.append(f"**Scores:** Market={scores['market_size']} | "
                     f"Defensibility={scores['defensibility']} | "
                     f"Recurring={scores['recurring_potential']} | "
                     f"API Ease={scores['api_difficulty']}")

        if scored.get('edge_tactics'):
            for tactic in scored['edge_tactics']:
                info = EDGE_TACTICS[tactic]
                lines.append(f"**Edge:** [{tactic.upper()}] {info['description']}")

        if analysis.get('cli_args'):
            args_str = ', '.join(a['flag'] for a in analysis['cli_args'][:6])
            lines.append(f"**CLI:** {args_str}")

        if analysis.get('api_calls'):
            lines.append(f"**APIs:** {', '.join(analysis['api_calls'])}")

        if analysis.get('external_deps'):
            lines.append(f"**Deps:** {', '.join(analysis['external_deps'][:8])}")

        lines.append(f"**Pricing:** $9/$29/$99 tiers")
        lines.append("")

    # Edge tactic distribution
    lines.append("## Edge Tactic Distribution")
    lines.append("")
    tactic_counts = defaultdict(int)
    for scored in all_scored:
        for tactic in scored.get('edge_tactics', []):
            tactic_counts[tactic] += 1

    for tactic, count in sorted(tactic_counts.items(), key=lambda x: x[1], reverse=True):
        info = EDGE_TACTICS[tactic]
        lines.append(f"- **{tactic.upper()}** ({count} scripts): {info['description']}")

    lines.append("")

    # Low-hanging fruit section
    lines.append("## Low-Hanging Fruit (Quick Wins)")
    lines.append("")
    lines.append("Scripts that score high AND are easy to wrap as API:")
    lines.append("")

    quick_wins = [
        s for s in all_scored
        if s['scores']['api_difficulty'] >= 60 and s['composite'] >= 50
    ][:10]

    for scored in quick_wins:
        analysis = all_analyses[scored['name']]
        saas_name = generate_saas_name(scored['name'])
        lines.append(f"- **{saas_name}** ({scored['name']}.py) - "
                     f"Score: {scored['composite']:.0f}, "
                     f"API ease: {scored['scores']['api_difficulty']}, "
                     f"{analysis['line_count']} lines")

    lines.append("")

    # Bundle opportunities
    lines.append("## Bundle Opportunities")
    lines.append("")
    lines.append("Scripts that could be combined into a single SaaS product:")
    lines.append("")

    # Group by common keywords
    keyword_groups = defaultdict(list)
    for scored in all_scored:
        name_lower = scored['name'].lower()
        for keyword in ['lead', 'content', 'ecom', 'social', 'seo', 'alpha',
                        'monitor', 'scraper', 'ad', 'freelance', 'competitor']:
            if keyword in name_lower:
                keyword_groups[keyword].append(scored['name'])

    for keyword, scripts in sorted(keyword_groups.items(), key=lambda x: len(x[1]), reverse=True):
        if len(scripts) >= 2:
            lines.append(f"- **{keyword.upper()} Suite** ({len(scripts)} scripts): "
                         f"{', '.join(scripts[:5])}")

    lines.append("")
    lines.append("---")
    lines.append(f"*Generated by saas_opportunity_engine.py on {timestamp}*")

    return '\n'.join(lines)


# ============================================================
# MAIN ENGINE
# ============================================================

def scan_all_scripts(quiet: bool = False) -> tuple:
    """Scan all Python scripts in AUTOMATIONS/."""
    scripts = sorted(AUTOMATIONS_DIR.glob('*.py'))

    if not quiet:
        print(f"\n{'='*60}")
        print(f"  PRINTMAXX SAAS OPPORTUNITY ENGINE")
        print(f"  Scanning {len(scripts)} scripts in AUTOMATIONS/")
        print(f"{'='*60}")

    all_analyses = {}
    all_scored = []
    skipped = 0

    for i, script_path in enumerate(scripts):
        if script_path.name.startswith('__') or script_path.name == 'saas_opportunity_engine.py':
            skipped += 1
            continue

        if not quiet and (i + 1) % 20 == 0:
            print(f"  [{i+1}/{len(scripts)}] Analyzing {script_path.name}...")

        # Analyze
        analyzer = ScriptAnalyzer(script_path)
        analysis = analyzer.summary()
        all_analyses[analysis['name']] = analysis

        # Score
        scorer = SaaSScorer(analysis)
        scored = scorer.score_all()
        all_scored.append(scored)

    # Sort by composite
    all_scored.sort(key=lambda x: x['composite'], reverse=True)

    if not quiet:
        print(f"\n  Analyzed: {len(all_scored)} scripts (skipped {skipped})")
        print(f"  Top SaaS candidates:\n")
        print(f"  {'#':<4} {'Score':<8} {'Script':<40} {'SaaS Name':<20} {'Edge Tactics'}")
        print(f"  {'-'*4} {'-'*8} {'-'*40} {'-'*20} {'-'*30}")

        for i, scored in enumerate(all_scored[:20], 1):
            analysis = all_analyses[scored['name']]
            saas_name = generate_saas_name(scored['name'])
            tactics = ', '.join(scored.get('edge_tactics', [])[:2]) or '-'
            score_color = '\033[92m' if scored['composite'] >= 70 else \
                          '\033[93m' if scored['composite'] >= 50 else '\033[91m'
            reset = '\033[0m'
            print(f"  {i:<4} {score_color}{scored['composite']:<8.0f}{reset} "
                  f"{scored['name']:<40} {saas_name:<20} {tactics}")

        print(f"\n  Scoring: market_size({SCORE_WEIGHTS['market_size']:.0%}) + "
              f"defensibility({SCORE_WEIGHTS['defensibility']:.0%}) + "
              f"recurring({SCORE_WEIGHTS['recurring_potential']:.0%}) + "
              f"api_ease({SCORE_WEIGHTS['api_difficulty']:.0%})")

    return all_scored, all_analyses


def deep_analyze(n: int, all_scored: list, all_analyses: dict, quiet: bool = False):
    """Deep analysis of top N candidates."""
    top_n = all_scored[:n]

    if not quiet:
        print(f"\n{'='*60}")
        print(f"  DEEP ANALYSIS — TOP {n} CANDIDATES")
        print(f"{'='*60}")

    for i, scored in enumerate(top_n, 1):
        analysis = all_analyses[scored['name']]
        saas_name = generate_saas_name(scored['name'])

        if not quiet:
            print(f"\n{'='*60}")
            print(f"  [{i}/{n}] {saas_name} ({scored['name']}.py)")
            print(f"{'='*60}")
            print(f"  Composite Score: {scored['composite']:.0f}/100")
            print(f"  Market Size:     {scored['scores']['market_size']}/100")
            print(f"  Defensibility:   {scored['scores']['defensibility']}/100")
            print(f"  Recurring:       {scored['scores']['recurring_potential']}/100")
            print(f"  API Ease:        {scored['scores']['api_difficulty']}/100")
            print(f"  Lines:           {analysis['line_count']}")
            print(f"  Functions:       {analysis['functions']}")
            print(f"  Classes:         {analysis['classes']}")
            print(f"  Error Handling:  {analysis['error_handling']}/100")
            print(f"  Output Formats:  {', '.join(analysis['output_formats']) or 'None'}")
            print(f"  External Deps:   {', '.join(analysis['external_deps'][:8]) or 'None'}")
            print(f"  API Calls:       {', '.join(analysis['api_calls']) or 'None'}")

            if scored.get('edge_tactics'):
                print(f"\n  Edge Tactics:")
                for tactic in scored['edge_tactics']:
                    info = EDGE_TACTICS[tactic]
                    print(f"    [{tactic.upper()}] {info['description']}")

            if analysis.get('cli_args'):
                print(f"\n  CLI Interface:")
                for arg in analysis['cli_args'][:10]:
                    print(f"    {arg['flag']:<25} {arg.get('help', '')}")

            if analysis.get('docstring'):
                print(f"\n  Docstring:")
                for line in analysis['docstring'].split('\n')[:5]:
                    print(f"    {line.strip()}")

            # Generate mini landing copy
            print(f"\n  --- LANDING PAGE PREVIEW ---")
            copy = generate_landing_copy(scored, analysis)
            # Print just the headline and subhead
            for line in copy.split('\n'):
                stripped = line.strip()
                if stripped.startswith('HEADLINE:') or stripped.startswith('SUBHEAD:') or \
                   (stripped.startswith('"') and len(stripped) < 100):
                    print(f"  {stripped}")

    return top_n


def find_script_by_name(name: str, all_scored: list, all_analyses: dict):
    """Find a script by partial name match."""
    name_lower = name.lower().replace('.py', '')

    # Exact match first
    for scored in all_scored:
        if scored['name'].lower() == name_lower:
            return scored, all_analyses[scored['name']]

    # Partial match
    for scored in all_scored:
        if name_lower in scored['name'].lower():
            return scored, all_analyses[scored['name']]

    # SaaS name match
    for scored in all_scored:
        saas_name = generate_saas_name(scored['name']).lower()
        if name_lower in saas_name.lower():
            return scored, all_analyses[scored['name']]

    return None, None


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='PRINTMAXX SaaS Opportunity Engine - Script-to-SaaS Analyzer'
    )
    parser.add_argument('--scan', action='store_true',
                        help='Full scan of all AUTOMATIONS/ scripts')
    parser.add_argument('--deep-analyze', type=int, metavar='N',
                        help='Deep analysis of top N candidates')
    parser.add_argument('--generate-landing', type=str, metavar='APP',
                        help='Generate landing page copy for APP')
    parser.add_argument('--pricing', type=str, metavar='APP',
                        help='Generate pricing breakdown for APP')
    parser.add_argument('--manifest', action='store_true',
                        help='Output full manifest to OPS/SAAS_MANIFEST_V2.md')
    parser.add_argument('--top', type=int, default=10,
                        help='Number of top results to show (default 10)')
    parser.add_argument('--quiet', action='store_true',
                        help='Quiet mode for automation')
    parser.add_argument('--json', action='store_true',
                        help='Output results as JSON')
    args = parser.parse_args()

    if not any([args.scan, args.deep_analyze, args.generate_landing,
                args.pricing, args.manifest]):
        parser.print_help()
        print("\n  example: python3 saas_opportunity_engine.py --scan")
        print("  example: python3 saas_opportunity_engine.py --scan --deep-analyze 10")
        print("  example: python3 saas_opportunity_engine.py --scan --generate-landing ecom_arb")
        return

    # Always scan first
    all_scored, all_analyses = scan_all_scripts(quiet=args.quiet)

    if args.json:
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_scripts': len(all_scored),
            'top_candidates': [
                {
                    'name': s['name'],
                    'saas_name': generate_saas_name(s['name']),
                    'composite': s['composite'],
                    'scores': s['scores'],
                    'edge_tactics': s.get('edge_tactics', []),
                    'line_count': all_analyses[s['name']]['line_count'],
                    'has_cli': all_analyses[s['name']]['has_cli'],
                }
                for s in all_scored[:args.top]
            ],
        }
        print(json.dumps(output, indent=2))
        return

    if args.deep_analyze:
        deep_analyze(args.deep_analyze, all_scored, all_analyses, quiet=args.quiet)

    if args.generate_landing:
        scored, analysis = find_script_by_name(args.generate_landing, all_scored, all_analyses)
        if scored and analysis:
            copy = generate_landing_copy(scored, analysis)
            print(copy)
        else:
            print(f"\n  Script not found: {args.generate_landing}")
            print(f"  Available scripts (top 10):")
            for s in all_scored[:10]:
                print(f"    {s['name']} ({generate_saas_name(s['name'])})")

    if args.pricing:
        scored, analysis = find_script_by_name(args.pricing, all_scored, all_analyses)
        if scored and analysis:
            breakdown = generate_pricing_breakdown(scored, analysis)
            print(breakdown)
        else:
            print(f"\n  Script not found: {args.pricing}")
            print(f"  Available scripts (top 10):")
            for s in all_scored[:10]:
                print(f"    {s['name']} ({generate_saas_name(s['name'])})")

    if args.manifest:
        manifest_content = generate_manifest(all_scored, all_analyses)
        OPS_DIR.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_MANIFEST, 'w') as f:
            f.write(manifest_content)
        if not args.quiet:
            print(f"\n  Manifest saved to: {OUTPUT_MANIFEST}")
            print(f"  {len(all_scored)} scripts analyzed, top 30 ranked.")

    # Log run
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        top_3 = [f"{s['name']}({s['composite']:.0f})" for s in all_scored[:3]]
        f.write(f"{datetime.now().isoformat()} | scanned: {len(all_scored)} | "
                f"top3: {', '.join(top_3)} | "
                f"70+: {sum(1 for s in all_scored if s['composite'] >= 70)}\n")


if __name__ == '__main__':
    main()
