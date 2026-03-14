#!/usr/bin/env python3
"""
T023 — Parallel Design Review (Challenger Agents)

Three challenger personas adversarially review major CEO decisions:
  1. Devil's Advocate — argues against the CEO recommendation with evidence
  2. Risk Assessor — identifies top 3 failure modes with probability estimates
  3. Market Reality Checker — validates decision against MARKET_SIGNALS.csv data

Trigger conditions (MAJOR decision):
  - PROMOTE: New venture promoted to paid ads (>$100 spend)
  - KILL: Venture killed after >30 days active
  - CREATE: New revenue lane created (>10h estimated build time)

Usage:
    python3 AUTOMATIONS/challenger_agents.py --review decision.json
    python3 AUTOMATIONS/challenger_agents.py --review-inline '{"type":"PROMOTE","venture":"CONTENT",...}'
    python3 AUTOMATIONS/challenger_agents.py --history
    python3 AUTOMATIONS/challenger_agents.py --stats
    python3 AUTOMATIONS/challenger_agents.py --dry-run decision.json

Stdlib only. No external dependencies.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Imports from shared utilities
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PROJECT, safe_path, log, ts, load_json

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REVIEW_LOG = safe_path(PROJECT / "LEDGER" / "DECISION_REVIEWS.jsonl")
PENDING_APPROVAL = safe_path(PROJECT / "OPS" / "PENDING_HUMAN_APPROVAL.jsonl")
MARKET_SIGNALS_CSV = safe_path(PROJECT / "LEDGER" / "MARKET_SIGNALS.csv")

# Ensure parent dirs exist
REVIEW_LOG.parent.mkdir(parents=True, exist_ok=True)
PENDING_APPROVAL.parent.mkdir(parents=True, exist_ok=True)

MAX_ROUNDS = 3


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------
class DecisionType(str, Enum):
    PROMOTE = "PROMOTE"
    KILL = "KILL"
    CREATE = "CREATE"


class Verdict(str, Enum):
    APPROVE = "APPROVE"
    OBJECT = "OBJECT"


class AggregateVerdict(str, Enum):
    APPROVED = "APPROVED"
    CHALLENGED = "CHALLENGED"
    ESCALATED = "ESCALATED"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class ChallengerVerdict:
    challenger_name: str
    verdict: Verdict
    evidence: str
    confidence: float  # 0.0 - 1.0
    analysis_time_ms: int = 0


@dataclass
class ChallengeResult:
    decision_id: str
    decision_type: str
    venture: str
    reasoning: str
    estimated_impact: str
    verdicts: list[ChallengerVerdict] = field(default_factory=list)
    aggregate_verdict: AggregateVerdict = AggregateVerdict.APPROVED
    round_number: int = 1
    timestamp: str = ""
    dry_run: bool = False

    def to_dict(self) -> dict:
        return {
            "decision_id": self.decision_id,
            "decision_type": self.decision_type,
            "venture": self.venture,
            "reasoning": self.reasoning,
            "estimated_impact": self.estimated_impact,
            "aggregate_verdict": self.aggregate_verdict.value,
            "round_number": self.round_number,
            "timestamp": self.timestamp,
            "dry_run": self.dry_run,
            "verdicts": [
                {
                    "challenger_name": v.challenger_name,
                    "verdict": v.verdict.value,
                    "evidence": v.evidence,
                    "confidence": v.confidence,
                    "analysis_time_ms": v.analysis_time_ms,
                }
                for v in self.verdicts
            ],
        }


# ---------------------------------------------------------------------------
# Market signals loader
# ---------------------------------------------------------------------------
def load_market_signals() -> list[dict]:
    """Load MARKET_SIGNALS.csv for the Market Reality Checker."""
    signals: list[dict] = []
    try:
        if not MARKET_SIGNALS_CSV.exists():
            log("MARKET_SIGNALS.csv not found — Market Reality Checker will use limited data",
                level="WARN", tag="CHALLENGER")
            return signals
        with open(MARKET_SIGNALS_CSV, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                signals.append(dict(row))
    except Exception as e:
        log(f"Error loading MARKET_SIGNALS.csv: {e}", level="WARN", tag="CHALLENGER")
    return signals


# ---------------------------------------------------------------------------
# Challenger implementations (placeholder logic)
#
# In production these would call Claude Opus via subprocess or the agent swarm
# pattern. For now they apply structured heuristic analysis and log what a
# full LLM challenger WOULD examine.
# ---------------------------------------------------------------------------

def _challenge_devils_advocate(decision: dict) -> ChallengerVerdict:
    """
    Devil's Advocate — argues against the CEO recommendation.

    In production: sends a structured prompt to Claude Opus asking it to
    argue AGAINST the decision with specific counter-evidence.

    Current implementation: heuristic analysis based on decision type.
    """
    t0 = time.monotonic_ns()
    dtype = decision.get("type", "UNKNOWN")
    venture = decision.get("venture", "UNKNOWN")
    reasoning = decision.get("reasoning", "")
    evidence = decision.get("evidence", "")
    estimated_impact = decision.get("estimated_impact", "")

    analysis_points: list[str] = []
    verdict = Verdict.APPROVE
    confidence = 0.5

    if dtype == "PROMOTE":
        analysis_points.append(
            f"COUNTER: Promoting {venture} to paid ads requires proven organic traction first. "
            f"Has {venture} demonstrated >2% organic conversion rate?"
        )
        analysis_points.append(
            "COUNTER: Paid ad spend >$100 without A/B tested creatives risks burning budget. "
            "Recommend split-testing 3 creatives organically before paid push."
        )
        if not evidence or len(evidence) < 20:
            analysis_points.append(
                "OBJECTION: Decision lacks concrete evidence (revenue data, conversion metrics). "
                "Promoting without quantified organic performance is premature."
            )
            verdict = Verdict.OBJECT
            confidence = 0.72

    elif dtype == "KILL":
        analysis_points.append(
            f"COUNTER: Killing {venture} after 30+ days ignores potential pivot opportunities. "
            f"Has the team explored adjacent use cases for existing assets?"
        )
        analysis_points.append(
            "COUNTER: Sunk cost analysis needed — what existing assets (content, code, leads) "
            "can be repurposed into other ventures before full kill?"
        )
        if "revenue" not in reasoning.lower() and "roi" not in reasoning.lower():
            analysis_points.append(
                "OBJECTION: Kill reasoning doesn't reference revenue metrics or ROI. "
                "Kill decisions must be data-driven, not sentiment-driven."
            )
            verdict = Verdict.OBJECT
            confidence = 0.65

    elif dtype == "CREATE":
        analysis_points.append(
            f"COUNTER: Creating a new revenue lane for {venture} (est. >10h build) diverts "
            f"resources from optimizing existing lanes that may have untapped potential."
        )
        analysis_points.append(
            "COUNTER: Opportunity cost — 10h of build time could instead be spent on "
            "distribution/marketing of existing products at $0 revenue."
        )
        if not estimated_impact or "revenue" not in estimated_impact.lower():
            analysis_points.append(
                "OBJECTION: No concrete revenue projection provided. "
                "New lane creation must include specific MRR targets and timeline."
            )
            verdict = Verdict.OBJECT
            confidence = 0.68

    elapsed_ms = int((time.monotonic_ns() - t0) / 1_000_000)
    return ChallengerVerdict(
        challenger_name="devils_advocate",
        verdict=verdict,
        evidence="\n".join(analysis_points),
        confidence=confidence,
        analysis_time_ms=elapsed_ms,
    )


def _challenge_risk_assessor(decision: dict) -> ChallengerVerdict:
    """
    Risk Assessor — identifies top 3 failure modes with probability estimates.

    In production: sends a structured prompt to Claude Opus requesting
    failure mode analysis with probability estimates per mode.

    Current implementation: heuristic failure mode identification.
    """
    t0 = time.monotonic_ns()
    dtype = decision.get("type", "UNKNOWN")
    venture = decision.get("venture", "UNKNOWN")
    reasoning = decision.get("reasoning", "")
    estimated_impact = decision.get("estimated_impact", "")

    failure_modes: list[str] = []
    verdict = Verdict.APPROVE
    confidence = 0.5
    total_risk = 0.0

    if dtype == "PROMOTE":
        modes = [
            ("Ad spend exhausted with <1% ROAS", 0.35,
             "Most first-time paid campaigns lose money. Without historical CPC data for "
             f"{venture}, budget burn probability is high."),
            ("Audience targeting misaligned with product-market fit", 0.25,
             "Organic audience != paid audience. Lookalike audiences require 1K+ converter "
             "seed list for accuracy."),
            ("Creative fatigue within 7 days, no replacement pipeline", 0.20,
             "Paid campaigns require 3-5 creative variants refreshed weekly. "
             "Is the content pipeline ready to sustain this?"),
        ]
        failure_modes = [f"RISK ({int(p*100)}% prob): {name} — {detail}" for name, p, detail in modes]
        total_risk = sum(p for _, p, _ in modes)

    elif dtype == "KILL":
        modes = [
            ("Killing a venture with recoverable assets destroys compound value", 0.30,
             f"{venture} may have content, code, leads, or brand equity that compounds "
             f"if pivoted rather than killed."),
            ("Team morale/pattern: repeated kill cycles signal strategic drift", 0.20,
             "If this is the 3rd+ kill, the issue may be strategy selection, "
             "not venture execution."),
            ("Competitor captures abandoned position within 30 days", 0.15,
             "Markets don't stay empty. Vacating a position you spent 30+ days "
             "building may hand advantage to a competitor."),
        ]
        failure_modes = [f"RISK ({int(p*100)}% prob): {name} — {detail}" for name, p, detail in modes]
        total_risk = sum(p for _, p, _ in modes)

    elif dtype == "CREATE":
        modes = [
            ("Build time exceeds estimate by 2-3x (scope creep)", 0.40,
             "Software projects systematically underestimate by 2-3x. "
             "A 10h estimate likely becomes 25-30h."),
            ("New lane cannibalizes existing revenue lanes", 0.20,
             f"New {venture} lane may compete for the same audience as existing "
             f"ventures, splitting attention without net revenue gain."),
            ("Integration complexity creates cascading failures", 0.15,
             "New systems require integration with existing agents, scrapers, "
             "and pipelines. Each integration point is a potential failure."),
        ]
        failure_modes = [f"RISK ({int(p*100)}% prob): {name} — {detail}" for name, p, detail in modes]
        total_risk = sum(p for _, p, _ in modes)

    # If combined failure probability > 60%, object
    if total_risk > 0.60:
        verdict = Verdict.OBJECT
        confidence = min(0.85, total_risk)
    else:
        confidence = 1.0 - total_risk

    failure_modes.append(f"\nCOMBINED FAILURE PROBABILITY: {total_risk:.0%}")

    elapsed_ms = int((time.monotonic_ns() - t0) / 1_000_000)
    return ChallengerVerdict(
        challenger_name="risk_assessor",
        verdict=verdict,
        evidence="\n".join(failure_modes),
        confidence=confidence,
        analysis_time_ms=elapsed_ms,
    )


def _challenge_market_reality(decision: dict) -> ChallengerVerdict:
    """
    Market Reality Checker — validates against MARKET_SIGNALS.csv data.

    In production: loads market signals, cross-references with the decision,
    and uses Claude Opus to identify contradictions between the decision
    and actual market data.

    Current implementation: loads CSV and performs keyword matching.
    """
    t0 = time.monotonic_ns()
    dtype = decision.get("type", "UNKNOWN")
    venture = decision.get("venture", "UNKNOWN").lower()
    reasoning = decision.get("reasoning", "").lower()

    signals = load_market_signals()
    analysis_points: list[str] = []
    verdict = Verdict.APPROVE
    confidence = 0.5

    # Search for relevant market signals
    relevant_signals: list[dict] = []
    venture_keywords = venture.replace("_", " ").split()

    for signal in signals:
        signal_text = " ".join(str(v).lower() for v in signal.values())
        # Match on venture name keywords
        if any(kw in signal_text for kw in venture_keywords):
            relevant_signals.append(signal)

    if not signals:
        analysis_points.append(
            "MARKET DATA: MARKET_SIGNALS.csv not available or empty. "
            "Cannot validate decision against market data. "
            "RECOMMENDATION: Collect market signals before major decisions."
        )
        verdict = Verdict.OBJECT
        confidence = 0.55
    elif not relevant_signals:
        analysis_points.append(
            f"MARKET DATA: No signals found matching venture '{venture}' "
            f"in MARKET_SIGNALS.csv ({len(signals)} total signals scanned). "
            f"Decision is being made without market data validation."
        )
        analysis_points.append(
            "RECOMMENDATION: Run market scanner for this venture before proceeding. "
            "Decisions without market data have 2-3x higher failure rate."
        )
        verdict = Verdict.OBJECT
        confidence = 0.60
    else:
        analysis_points.append(
            f"MARKET DATA: Found {len(relevant_signals)} relevant signal(s) "
            f"out of {len(signals)} total in MARKET_SIGNALS.csv."
        )

        # Summarize relevant signals
        for i, sig in enumerate(relevant_signals[:5]):  # cap at 5
            sig_summary = " | ".join(f"{k}: {v}" for k, v in sig.items() if v and len(str(v)) < 100)
            analysis_points.append(f"  Signal {i+1}: {sig_summary}")

        # Check for contradicting signals (bearish signals on PROMOTE, bullish on KILL)
        bearish_keywords = ["decline", "down", "drop", "shrink", "saturated", "oversupplied", "risk"]
        bullish_keywords = ["growth", "up", "rising", "expanding", "opportunity", "demand", "hot"]

        bearish_count = 0
        bullish_count = 0
        for sig in relevant_signals:
            sig_text = " ".join(str(v).lower() for v in sig.values())
            if any(kw in sig_text for kw in bearish_keywords):
                bearish_count += 1
            if any(kw in sig_text for kw in bullish_keywords):
                bullish_count += 1

        if dtype == "PROMOTE" and bearish_count > bullish_count:
            analysis_points.append(
                f"\nMARKET CONTRADICTION: {bearish_count} bearish signal(s) vs {bullish_count} bullish. "
                f"Promoting {venture} to paid ads runs against current market sentiment."
            )
            verdict = Verdict.OBJECT
            confidence = 0.70
        elif dtype == "KILL" and bullish_count > bearish_count:
            analysis_points.append(
                f"\nMARKET CONTRADICTION: {bullish_count} bullish signal(s) vs {bearish_count} bearish. "
                f"Killing {venture} when market signals are positive may be premature."
            )
            verdict = Verdict.OBJECT
            confidence = 0.65
        else:
            analysis_points.append(
                f"\nMARKET ALIGNMENT: Market signals are consistent with {dtype} decision "
                f"(bearish={bearish_count}, bullish={bullish_count})."
            )
            confidence = 0.75

    elapsed_ms = int((time.monotonic_ns() - t0) / 1_000_000)
    return ChallengerVerdict(
        challenger_name="market_reality_checker",
        verdict=verdict,
        evidence="\n".join(analysis_points),
        confidence=confidence,
        analysis_time_ms=elapsed_ms,
    )


# ---------------------------------------------------------------------------
# ChallengerManager
# ---------------------------------------------------------------------------
class ChallengerManager:
    """Orchestrates 3 challenger agents to adversarially review CEO decisions."""

    CHALLENGERS = [
        ("devils_advocate", _challenge_devils_advocate),
        ("risk_assessor", _challenge_risk_assessor),
        ("market_reality_checker", _challenge_market_reality),
    ]

    @staticmethod
    def _generate_id(decision: dict) -> str:
        """Generate a deterministic decision ID from content."""
        raw = json.dumps(decision, sort_keys=True)
        return "DEC_" + hashlib.sha256(raw.encode()).hexdigest()[:12].upper()

    @staticmethod
    def is_major_decision(decision: dict) -> bool:
        """Check if a decision meets MAJOR threshold for challenger review."""
        dtype = decision.get("type", "").upper()
        if dtype == "PROMOTE":
            # >$100 spend
            spend = decision.get("estimated_spend", 0)
            try:
                spend = float(str(spend).replace("$", "").replace(",", ""))
            except (ValueError, TypeError):
                spend = 0
            return spend > 100
        elif dtype == "KILL":
            # >30 days active
            days_active = decision.get("days_active", 0)
            try:
                days_active = int(days_active)
            except (ValueError, TypeError):
                days_active = 0
            return days_active > 30
        elif dtype == "CREATE":
            # >10h estimated build time
            build_hours = decision.get("estimated_build_hours", 0)
            try:
                build_hours = float(build_hours)
            except (ValueError, TypeError):
                build_hours = 0
            return build_hours > 10
        return False

    def review_decision(self, decision: dict, dry_run: bool = False) -> ChallengeResult:
        """
        Run all 3 challengers against a decision.

        Args:
            decision: dict with type, venture, reasoning, evidence, estimated_impact
            dry_run: if True, log analysis but don't write to PENDING_HUMAN_APPROVAL

        Returns:
            ChallengeResult with aggregate verdict
        """
        decision_id = self._generate_id(decision)
        result = ChallengeResult(
            decision_id=decision_id,
            decision_type=decision.get("type", "UNKNOWN"),
            venture=decision.get("venture", "UNKNOWN"),
            reasoning=decision.get("reasoning", ""),
            estimated_impact=decision.get("estimated_impact", ""),
            timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            dry_run=dry_run,
        )

        log(f"Starting challenger review for {decision_id} ({result.decision_type} / {result.venture})",
            tag="CHALLENGER")

        # Run all 3 challengers (sequentially — would be parallel with real LLM calls)
        for name, challenger_fn in self.CHALLENGERS:
            try:
                log(f"  Running {name}...", tag="CHALLENGER")
                verdict = challenger_fn(decision)
                result.verdicts.append(verdict)
                log(f"  {name}: {verdict.verdict.value} (confidence={verdict.confidence:.2f}, "
                    f"{verdict.analysis_time_ms}ms)", tag="CHALLENGER")
            except Exception as e:
                log(f"  {name} FAILED: {e}", level="ERROR", tag="CHALLENGER")
                # Record a cautious OBJECT on challenger failure
                result.verdicts.append(ChallengerVerdict(
                    challenger_name=name,
                    verdict=Verdict.OBJECT,
                    evidence=f"Challenger {name} failed with error: {e}. Defaulting to OBJECT for safety.",
                    confidence=0.5,
                ))

        # Aggregate: 2+ OBJECTIONs with evidence -> CHALLENGED
        objections = [v for v in result.verdicts if v.verdict == Verdict.OBJECT]
        objections_with_evidence = [v for v in objections if v.evidence and len(v.evidence) > 10]

        if len(objections_with_evidence) >= 2:
            result.aggregate_verdict = AggregateVerdict.CHALLENGED
            log(f"CHALLENGED: {len(objections_with_evidence)}/3 challengers objected with evidence",
                level="WARN", tag="CHALLENGER")
            if not dry_run:
                self._write_pending_approval(decision, result)
        elif result.round_number >= MAX_ROUNDS:
            result.aggregate_verdict = AggregateVerdict.ESCALATED
            log(f"ESCALATED: Max rounds ({MAX_ROUNDS}) reached, escalating to human",
                level="WARN", tag="CHALLENGER")
            if not dry_run:
                self._write_pending_approval(decision, result)
        else:
            result.aggregate_verdict = AggregateVerdict.APPROVED
            log(f"APPROVED: {len(objections)}/3 objections (need 2+ with evidence to challenge)",
                tag="CHALLENGER")

        # Always log to DECISION_REVIEWS.jsonl
        self._log_review(result)

        return result

    def _log_review(self, result: ChallengeResult) -> None:
        """Append review to DECISION_REVIEWS.jsonl."""
        try:
            with open(REVIEW_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(result.to_dict()) + "\n")
            log(f"Review logged to {REVIEW_LOG.name}", tag="CHALLENGER")
        except Exception as e:
            log(f"Failed to log review: {e}", level="ERROR", tag="CHALLENGER")

    def _write_pending_approval(self, decision: dict, result: ChallengeResult) -> None:
        """Write challenged decision to OPS/PENDING_HUMAN_APPROVAL.jsonl."""
        try:
            entry = {
                "decision_id": result.decision_id,
                "decision_type": result.decision_type,
                "venture": result.venture,
                "original_reasoning": result.reasoning,
                "aggregate_verdict": result.aggregate_verdict.value,
                "objection_count": sum(1 for v in result.verdicts if v.verdict == Verdict.OBJECT),
                "challenger_summaries": [
                    {
                        "name": v.challenger_name,
                        "verdict": v.verdict.value,
                        "confidence": v.confidence,
                        "evidence_preview": v.evidence[:200] + "..." if len(v.evidence) > 200 else v.evidence,
                    }
                    for v in result.verdicts
                ],
                "timestamp": result.timestamp,
                "status": "PENDING_HUMAN_REVIEW",
            }
            with open(PENDING_APPROVAL, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            log(f"Decision {result.decision_id} written to PENDING_HUMAN_APPROVAL.jsonl", tag="CHALLENGER")
        except Exception as e:
            log(f"Failed to write pending approval: {e}", level="ERROR", tag="CHALLENGER")

    # -- history / stats -----------------------------------------------------

    @staticmethod
    def load_history() -> list[dict]:
        """Load all reviews from DECISION_REVIEWS.jsonl."""
        reviews: list[dict] = []
        if not REVIEW_LOG.exists():
            return reviews
        try:
            with open(REVIEW_LOG, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            reviews.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except Exception:
            pass
        return reviews

    @staticmethod
    def compute_stats(reviews: list[dict]) -> dict:
        """Compute aggregate stats from review history."""
        if not reviews:
            return {"total_reviews": 0}

        stats: dict[str, Any] = {
            "total_reviews": len(reviews),
            "by_verdict": {},
            "by_type": {},
            "by_venture": {},
            "challenger_objection_rates": {},
            "avg_confidence_by_challenger": {},
        }

        verdict_counts: dict[str, int] = {}
        type_counts: dict[str, int] = {}
        venture_counts: dict[str, int] = {}
        challenger_objections: dict[str, int] = {}
        challenger_total: dict[str, int] = {}
        challenger_confidence_sum: dict[str, float] = {}

        for r in reviews:
            # By verdict
            v = r.get("aggregate_verdict", "UNKNOWN")
            verdict_counts[v] = verdict_counts.get(v, 0) + 1

            # By type
            dt = r.get("decision_type", "UNKNOWN")
            type_counts[dt] = type_counts.get(dt, 0) + 1

            # By venture
            ven = r.get("venture", "UNKNOWN")
            venture_counts[ven] = venture_counts.get(ven, 0) + 1

            # Per-challenger stats
            for cv in r.get("verdicts", []):
                name = cv.get("challenger_name", "unknown")
                challenger_total[name] = challenger_total.get(name, 0) + 1
                if cv.get("verdict") == "OBJECT":
                    challenger_objections[name] = challenger_objections.get(name, 0) + 1
                conf = cv.get("confidence", 0.5)
                challenger_confidence_sum[name] = challenger_confidence_sum.get(name, 0.0) + conf

        stats["by_verdict"] = verdict_counts
        stats["by_type"] = type_counts
        stats["by_venture"] = venture_counts

        for name in challenger_total:
            total = challenger_total[name]
            obj = challenger_objections.get(name, 0)
            stats["challenger_objection_rates"][name] = f"{obj}/{total} ({obj/total*100:.0f}%)" if total else "0/0"
            stats["avg_confidence_by_challenger"][name] = round(challenger_confidence_sum[name] / total, 2) if total else 0

        return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _load_decision(source: str) -> dict:
    """Load a decision from a file path or inline JSON string."""
    # Try as file first
    p = Path(source)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            log(f"Invalid JSON in file {source}: {e}", level="ERROR", tag="CHALLENGER")
            sys.exit(1)

    # Try as inline JSON
    try:
        return json.loads(source)
    except json.JSONDecodeError:
        # Try as project-relative path
        project_path = PROJECT / source
        if project_path.exists():
            try:
                return json.loads(project_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                log(f"Invalid JSON in file {project_path}: {e}", level="ERROR", tag="CHALLENGER")
                sys.exit(1)

    log(f"Cannot parse decision source: {source}", level="ERROR", tag="CHALLENGER")
    log("Provide a JSON file path or inline JSON string.", level="ERROR", tag="CHALLENGER")
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="T023 — Parallel Design Review (Challenger Agents)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Decision JSON format:
  {
    "type": "PROMOTE|KILL|CREATE",
    "venture": "CONTENT",
    "reasoning": "Why this decision was made",
    "evidence": "Data supporting the decision",
    "estimated_impact": "Expected outcome",
    "estimated_spend": 500,          // for PROMOTE
    "days_active": 45,               // for KILL
    "estimated_build_hours": 20      // for CREATE
  }

Examples:
  %(prog)s --review decision.json
  %(prog)s --review-inline '{"type":"PROMOTE","venture":"CONTENT","reasoning":"Strong organic growth","evidence":"2%% CTR","estimated_impact":"$500 MRR","estimated_spend":200}'
  %(prog)s --history
  %(prog)s --stats
  %(prog)s --dry-run decision.json
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--review", type=str, metavar="DECISION_JSON_FILE",
                       help="Review a decision from a JSON file")
    group.add_argument("--review-inline", type=str, metavar="JSON_STRING",
                       help="Review a decision from inline JSON")
    group.add_argument("--history", action="store_true", help="Show review history")
    group.add_argument("--stats", action="store_true", help="Show aggregate stats")
    group.add_argument("--dry-run", type=str, metavar="DECISION_JSON_FILE",
                       help="Dry-run review (no writes to PENDING_HUMAN_APPROVAL)")

    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--force", action="store_true",
                        help="Skip major-decision threshold check")

    args = parser.parse_args()
    manager = ChallengerManager()

    if args.review or args.review_inline or args.dry_run:
        source = args.review or args.review_inline or args.dry_run
        decision = _load_decision(source)
        dry_run = bool(args.dry_run)

        # Validate decision has required fields
        required_fields = ["type", "venture"]
        missing = [f for f in required_fields if f not in decision]
        if missing:
            log(f"Decision missing required fields: {missing}", level="ERROR", tag="CHALLENGER")
            sys.exit(1)

        # Check if this is a major decision (unless --force)
        if not args.force and not manager.is_major_decision(decision):
            log("Decision does not meet MAJOR threshold for challenger review.", level="WARN", tag="CHALLENGER")
            log("Thresholds: PROMOTE >$100 spend | KILL >30 days active | CREATE >10h build",
                level="WARN", tag="CHALLENGER")
            log("Use --force to override.", level="WARN", tag="CHALLENGER")
            sys.exit(0)

        result = manager.review_decision(decision, dry_run=dry_run)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"  CHALLENGER REVIEW: {result.decision_id}")
            print(f"  Type: {result.decision_type} | Venture: {result.venture}")
            print(f"  Aggregate: {result.aggregate_verdict.value}")
            print(f"{'='*60}")
            for v in result.verdicts:
                icon = "PASS" if v.verdict == Verdict.APPROVE else "FAIL"
                print(f"\n  [{icon}] {v.challenger_name} — {v.verdict.value} "
                      f"(confidence: {v.confidence:.2f}, {v.analysis_time_ms}ms)")
                for line in v.evidence.split("\n"):
                    if line.strip():
                        print(f"    {line}")
            print(f"\n{'='*60}")
            if result.aggregate_verdict == AggregateVerdict.CHALLENGED:
                print(f"  >> DECISION CHALLENGED — written to PENDING_HUMAN_APPROVAL.jsonl")
            elif result.aggregate_verdict == AggregateVerdict.ESCALATED:
                print(f"  >> DECISION ESCALATED — max rounds reached, human review required")
            else:
                print(f"  >> DECISION APPROVED — challengers did not block")
            if dry_run:
                print(f"  >> (DRY RUN — no writes to PENDING_HUMAN_APPROVAL)")
            print()

    elif args.history:
        reviews = manager.load_history()
        if not reviews:
            print("\n  No reviews found in DECISION_REVIEWS.jsonl\n")
        elif args.json:
            print(json.dumps(reviews, indent=2))
        else:
            print(f"\n  {len(reviews)} review(s) in history:")
            print(f"  {'='*55}")
            for r in reviews:
                dt = r.get("decision_type", "?")
                ven = r.get("venture", "?")
                agg = r.get("aggregate_verdict", "?")
                ts_val = r.get("timestamp", "?")
                did = r.get("decision_id", "?")
                obj_count = sum(1 for v in r.get("verdicts", []) if v.get("verdict") == "OBJECT")
                print(f"  {ts_val}  {did}  {dt:<8} {ven:<15} -> {agg} ({obj_count}/3 objections)")
            print()

    elif args.stats:
        reviews = manager.load_history()
        stats = manager.compute_stats(reviews)
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print(f"\n  CHALLENGER STATS")
            print(f"  {'='*50}")
            print(f"  Total reviews: {stats['total_reviews']}")
            if stats["total_reviews"] > 0:
                print(f"\n  By verdict:")
                for v, c in stats.get("by_verdict", {}).items():
                    print(f"    {v}: {c}")
                print(f"\n  By decision type:")
                for t, c in stats.get("by_type", {}).items():
                    print(f"    {t}: {c}")
                print(f"\n  By venture:")
                for ven, c in stats.get("by_venture", {}).items():
                    print(f"    {ven}: {c}")
                print(f"\n  Challenger objection rates:")
                for name, rate in stats.get("challenger_objection_rates", {}).items():
                    avg_conf = stats.get("avg_confidence_by_challenger", {}).get(name, 0)
                    print(f"    {name}: {rate} (avg confidence: {avg_conf})")
            print()


if __name__ == "__main__":
    main()
