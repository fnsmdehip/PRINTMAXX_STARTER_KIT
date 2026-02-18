#!/usr/bin/env python3
"""
PRINTMAXX Experiment Runner - A/B test management and statistical analysis.

Commands:
  list                          Show all experiments with status
  start <id>                    Mark experiment as RUNNING
  log <id> --variant --metric --value --n   Log a data point
  analyze <id>                  Statistical analysis of experiment data
  complete <id> --winner --notes  Complete experiment, record learning
  recommend                     Recommend top 3 experiments to start
"""

import argparse
import csv
import json
import math
import os
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = BASE_DIR / "LEDGER"
AB_TESTS_CSV = LEDGER_DIR / "AB_TESTS_MASTER.csv"
HYPOTHESES_JSON = LEDGER_DIR / "RBI_STRATEGIC" / "HYPOTHESES.json"
LEARNINGS_JSONL = LEDGER_DIR / "RBI_STRATEGIC" / "LEARNINGS.jsonl"
EXPERIMENT_DATA_DIR = LEDGER_DIR / "EXPERIMENT_DATA"


# ---------------------------------------------------------------------------
# Statistics (no scipy needed)
# ---------------------------------------------------------------------------

def normal_cdf(x):
    """Cumulative distribution function for standard normal."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def normal_ppf(p):
    """Inverse CDF (percent point function) for standard normal. Rational approximation."""
    if p <= 0:
        return -float("inf")
    if p >= 1:
        return float("inf")
    if p == 0.5:
        return 0.0
    if p < 0.5:
        return -normal_ppf(1 - p)
    # Rational approximation for 0.5 < p < 1
    t = math.sqrt(-2.0 * math.log(1.0 - p))
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    return t - (c0 + c1 * t + c2 * t * t) / (1.0 + d1 * t + d2 * t * t + d3 * t * t * t)


def chi2_cdf_1df(x):
    """CDF for chi-squared distribution with 1 degree of freedom."""
    if x <= 0:
        return 0.0
    return 2.0 * normal_cdf(math.sqrt(x)) - 1.0


def chi2_cdf(x, k):
    """CDF for chi-squared distribution with k degrees of freedom.
    Uses the regularized incomplete gamma function approximation.
    For small k (typical A/B tests), Wilson-Hilferty approximation works well."""
    if x <= 0:
        return 0.0
    if k == 1:
        return chi2_cdf_1df(x)
    if k == 2:
        return 1.0 - math.exp(-x / 2.0)
    # Wilson-Hilferty approximation
    z = ((x / k) ** (1.0 / 3.0) - (1.0 - 2.0 / (9.0 * k))) / math.sqrt(2.0 / (9.0 * k))
    return normal_cdf(z)


def t_cdf(t_val, df):
    """CDF for Student's t-distribution using incomplete beta approximation."""
    if df <= 0:
        return 0.5
    x = df / (df + t_val * t_val)
    # Use regularized incomplete beta function via continued fraction
    alpha = df / 2.0
    beta = 0.5
    ibeta = _regularized_incomplete_beta(x, alpha, beta)
    if t_val >= 0:
        return 1.0 - 0.5 * ibeta
    else:
        return 0.5 * ibeta


def _regularized_incomplete_beta(x, a, b, max_iter=200, tol=1e-12):
    """Regularized incomplete beta function I_x(a,b) via Lentz's continued fraction."""
    if x < 0 or x > 1:
        return 0.0
    if x == 0 or x == 1:
        return x
    # Use symmetry for better convergence
    if x > (a + 1) / (a + b + 2):
        return 1.0 - _regularized_incomplete_beta(1 - x, b, a, max_iter, tol)

    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(math.log(x) * a + math.log(1.0 - x) * b - lbeta) / a

    # Lentz's algorithm
    f = 1.0
    c = 1.0
    d = 1.0 - (a + b) * x / (a + 1.0)
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    f = d

    for m in range(1, max_iter + 1):
        # Even step
        numerator = m * (b - m) * x / ((a + 2 * m - 1) * (a + 2 * m))
        d = 1.0 + numerator * d
        if abs(d) < 1e-30:
            d = 1e-30
        d = 1.0 / d
        c = 1.0 + numerator / c
        if abs(c) < 1e-30:
            c = 1e-30
        f *= d * c

        # Odd step
        numerator = -(a + m) * (a + b + m) * x / ((a + 2 * m) * (a + 2 * m + 1))
        d = 1.0 + numerator * d
        if abs(d) < 1e-30:
            d = 1e-30
        d = 1.0 / d
        c = 1.0 + numerator / c
        if abs(c) < 1e-30:
            c = 1e-30
        delta = d * c
        f *= delta

        if abs(delta - 1.0) < tol:
            break

    return front * f


def chi_square_test(successes_a, n_a, successes_b, n_b):
    """2x2 chi-square test for two proportions. Returns (chi2_stat, p_value)."""
    fail_a = n_a - successes_a
    fail_b = n_b - successes_b
    total = n_a + n_b
    total_success = successes_a + successes_b
    total_fail = fail_a + fail_b

    if total == 0 or total_success == 0 or total_fail == 0:
        return 0.0, 1.0

    # Expected values
    e_sa = n_a * total_success / total
    e_fa = n_a * total_fail / total
    e_sb = n_b * total_success / total
    e_fb = n_b * total_fail / total

    chi2 = 0.0
    for obs, exp in [(successes_a, e_sa), (fail_a, e_fa), (successes_b, e_sb), (fail_b, e_fb)]:
        if exp > 0:
            chi2 += (obs - exp) ** 2 / exp

    p_value = 1.0 - chi2_cdf_1df(chi2)
    return chi2, p_value


def welch_t_test(mean_a, var_a, n_a, mean_b, var_b, n_b):
    """Welch's t-test for two independent samples. Returns (t_stat, df, p_value)."""
    if n_a < 2 or n_b < 2:
        return 0.0, 0, 1.0

    se = math.sqrt(var_a / n_a + var_b / n_b)
    if se == 0:
        return 0.0, max(n_a + n_b - 2, 1), 1.0

    t_stat = (mean_a - mean_b) / se

    # Welch-Satterthwaite degrees of freedom
    num = (var_a / n_a + var_b / n_b) ** 2
    denom = (var_a / n_a) ** 2 / (n_a - 1) + (var_b / n_b) ** 2 / (n_b - 1)
    if denom == 0:
        df = max(n_a + n_b - 2, 1)
    else:
        df = num / denom

    # Two-tailed p-value
    p_value = 2.0 * (1.0 - t_cdf(abs(t_stat), df))
    return t_stat, df, p_value


def min_sample_size(baseline_rate, mde_relative=0.2, alpha=0.05, power=0.80):
    """Minimum sample size per variant for detecting a relative change in conversion rate."""
    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde_relative)
    if p1 <= 0 or p1 >= 1 or p2 <= 0 or p2 >= 1:
        return 0
    z_alpha = normal_ppf(1 - alpha / 2)
    z_beta = normal_ppf(power)
    p_avg = (p1 + p2) / 2
    n = ((z_alpha * math.sqrt(2 * p_avg * (1 - p_avg)) +
          z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) / (p2 - p1)) ** 2
    return math.ceil(n)


def confidence_interval_proportion(successes, n, confidence=0.95):
    """Wilson score interval for a proportion."""
    if n == 0:
        return 0, 0, 0
    p_hat = successes / n
    z = normal_ppf(1 - (1 - confidence) / 2)
    denom = 1 + z * z / n
    center = (p_hat + z * z / (2 * n)) / denom
    margin = z * math.sqrt((p_hat * (1 - p_hat) + z * z / (4 * n)) / n) / denom
    return p_hat, max(0, center - margin), min(1, center + margin)


def confidence_interval_mean(values, confidence=0.95):
    """Confidence interval for a mean using t-distribution approximation."""
    n = len(values)
    if n < 2:
        m = values[0] if values else 0
        return m, m, m
    m = statistics.mean(values)
    s = statistics.stdev(values)
    z = normal_ppf(1 - (1 - confidence) / 2)
    margin = z * s / math.sqrt(n)
    return m, m - margin, m + margin


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def load_ab_tests():
    """Load AB_TESTS_MASTER.csv as list of dicts."""
    if not AB_TESTS_CSV.exists():
        return []
    with open(AB_TESTS_CSV, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_ab_tests(rows):
    """Write AB_TESTS_MASTER.csv from list of dicts."""
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(AB_TESTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_hypotheses():
    """Load HYPOTHESES.json as list of dicts."""
    if not HYPOTHESES_JSON.exists():
        return []
    with open(HYPOTHESES_JSON, "r") as f:
        return json.load(f)


def save_hypotheses(data):
    """Write HYPOTHESES.json."""
    with open(HYPOTHESES_JSON, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def append_learning(entry):
    """Append a JSON line to LEARNINGS.jsonl."""
    LEARNINGS_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(LEARNINGS_JSONL, "a") as f:
        f.write(json.dumps(entry) + "\n")


def load_experiment_data(exp_id):
    """Load experiment data CSV for a given experiment ID."""
    path = EXPERIMENT_DATA_DIR / f"{exp_id}.csv"
    if not path.exists():
        return []
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def append_experiment_data(exp_id, row):
    """Append a data row to the experiment's CSV file."""
    EXPERIMENT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = EXPERIMENT_DATA_DIR / f"{exp_id}.csv"
    file_exists = path.exists()
    fieldnames = ["timestamp", "variant", "metric", "value", "n"]
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def find_experiment(exp_id):
    """Find experiment in AB tests CSV or hypotheses JSON. Returns (source, record) or (None, None)."""
    for row in load_ab_tests():
        if row.get("test_id", "").strip() == exp_id:
            return "ab_tests", row
    for h in load_hypotheses():
        if h.get("id", "").strip() == exp_id:
            return "hypotheses", h
    return None, None


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_list(args):
    """Show all experiments with status."""
    ab_tests = load_ab_tests()
    hypotheses = load_hypotheses()

    # Count data points per experiment
    data_counts = {}
    if EXPERIMENT_DATA_DIR.exists():
        for f in EXPERIMENT_DATA_DIR.iterdir():
            if f.suffix == ".csv":
                eid = f.stem
                rows = load_experiment_data(eid)
                data_counts[eid] = len(rows)

    print("=" * 90)
    print("PRINTMAXX EXPERIMENT RUNNER - All Experiments")
    print("=" * 90)

    # AB Tests
    if ab_tests:
        print(f"\n--- AB_TESTS_MASTER.csv ({len(ab_tests)} tests) ---\n")
        print(f"{'ID':<16} {'App':<12} {'Status':<14} {'Metric':<20} {'Data Pts':<10} Hypothesis")
        print("-" * 90)
        for row in ab_tests:
            tid = row.get("test_id", "?")
            app = row.get("app", "?")
            status = row.get("status", "?")
            metric = row.get("metric", "?")
            dp = data_counts.get(tid, 0)
            hyp = row.get("hypothesis", "")[:40]
            print(f"{tid:<16} {app:<12} {status:<14} {metric:<20} {dp:<10} {hyp}")

    # Hypotheses
    if hypotheses:
        print(f"\n--- HYPOTHESES.json ({len(hypotheses)} hypotheses) ---\n")
        print(f"{'ID':<8} {'Status':<14} {'Effort':<12} {'Data Pts':<10} Hypothesis")
        print("-" * 90)
        for h in hypotheses:
            hid = h.get("id", "?")
            status = h.get("status", "NOT STARTED")
            effort = h.get("effort", "?")
            dp = data_counts.get(hid, 0)
            hyp = h.get("hypothesis", "")[:55]
            print(f"{hid:<8} {status:<14} {effort:<12} {dp:<10} {hyp}")

    # Summary
    total = len(ab_tests) + len(hypotheses)
    running = sum(1 for r in ab_tests if r.get("status") == "RUNNING")
    running += sum(1 for h in hypotheses if h.get("status") == "RUNNING")
    completed = sum(1 for r in ab_tests if r.get("status") == "COMPLETED")
    completed += sum(1 for h in hypotheses if h.get("status") == "COMPLETED")
    print(f"\nTotal: {total} | Running: {running} | Completed: {completed} | "
          f"Not started: {total - running - completed}")


def cmd_start(args):
    """Mark an experiment as RUNNING with start_date."""
    exp_id = args.id
    today = datetime.now().strftime("%Y-%m-%d")

    # Check AB tests
    ab_tests = load_ab_tests()
    found = False
    for row in ab_tests:
        if row.get("test_id", "").strip() == exp_id:
            row["status"] = "RUNNING"
            row["start_date"] = today
            found = True
            break
    if found:
        save_ab_tests(ab_tests)
        print(f"[STARTED] {exp_id} marked as RUNNING (start_date: {today})")
        return

    # Check hypotheses
    hypotheses = load_hypotheses()
    for h in hypotheses:
        if h.get("id", "").strip() == exp_id:
            h["status"] = "RUNNING"
            h["start_date"] = today
            found = True
            break
    if found:
        save_hypotheses(hypotheses)
        print(f"[STARTED] {exp_id} marked as RUNNING (start_date: {today})")
        return

    print(f"[ERROR] Experiment '{exp_id}' not found in AB_TESTS_MASTER.csv or HYPOTHESES.json")
    sys.exit(1)


def cmd_log(args):
    """Log a data point for an experiment."""
    exp_id = args.id
    source, record = find_experiment(exp_id)
    if source is None:
        print(f"[ERROR] Experiment '{exp_id}' not found")
        sys.exit(1)

    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "variant": args.variant,
        "metric": args.metric,
        "value": str(args.value),
        "n": str(args.n),
    }
    append_experiment_data(exp_id, row)
    print(f"[LOGGED] {exp_id} | variant={args.variant} metric={args.metric} "
          f"value={args.value} n={args.n}")

    # Show running totals
    data = load_experiment_data(exp_id)
    variants = {}
    for d in data:
        v = d["variant"]
        if v not in variants:
            variants[v] = {"count": 0, "total_n": 0}
        variants[v]["count"] += 1
        variants[v]["total_n"] += int(d.get("n", 0))
    print("  Running totals:")
    for v, info in sorted(variants.items()):
        print(f"    Variant {v}: {info['count']} data points, total n={info['total_n']}")


def cmd_analyze(args):
    """Statistical analysis of an experiment."""
    exp_id = args.id
    data = load_experiment_data(exp_id)
    if not data:
        print(f"[ERROR] No data found for experiment '{exp_id}'")
        print(f"  Expected file: {EXPERIMENT_DATA_DIR / f'{exp_id}.csv'}")
        sys.exit(1)

    # Group by variant
    variants = {}
    for row in data:
        v = row["variant"]
        if v not in variants:
            variants[v] = []
        variants[v].append(row)

    if len(variants) < 2:
        print(f"[ERROR] Need at least 2 variants for analysis. Found: {list(variants.keys())}")
        sys.exit(1)

    # Determine metric type from first row
    metric_name = data[0].get("metric", "unknown")
    is_rate = "rate" in metric_name.lower() or "conversion" in metric_name.lower() or "ctr" in metric_name.lower()

    print("=" * 80)
    print(f"EXPERIMENT ANALYSIS: {exp_id}")
    print(f"Metric: {metric_name} | Type: {'Proportion/Rate' if is_rate else 'Continuous'}")
    print("=" * 80)

    variant_names = sorted(variants.keys())

    if is_rate:
        _analyze_proportions(exp_id, variants, variant_names, metric_name)
    else:
        _analyze_continuous(exp_id, variants, variant_names, metric_name)


def _analyze_proportions(exp_id, variants, variant_names, metric_name):
    """Analyze proportion/rate metrics using chi-square test."""
    # For rate metrics, value = rate, n = sample size
    # Compute successes = rate * n for each data point, then aggregate
    variant_stats = {}
    for v in variant_names:
        total_n = 0
        total_successes = 0.0
        for row in variants[v]:
            n = int(row.get("n", 0))
            val = float(row.get("value", 0))
            # If value is between 0 and 1, treat as rate; if > 1, treat as count
            if val <= 1.0:
                successes = round(val * n)
            else:
                successes = int(val)
            total_n += n
            total_successes += successes
        rate = total_successes / total_n if total_n > 0 else 0
        p_hat, ci_low, ci_high = confidence_interval_proportion(int(total_successes), total_n)
        variant_stats[v] = {
            "n": total_n,
            "successes": int(total_successes),
            "rate": rate,
            "ci_low": ci_low,
            "ci_high": ci_high,
        }

    # Print variant summary
    print(f"\n{'Variant':<10} {'N':<10} {'Successes':<12} {'Rate':<12} {'95% CI':<20}")
    print("-" * 64)
    for v in variant_names:
        s = variant_stats[v]
        ci_str = f"[{s['ci_low']:.4f}, {s['ci_high']:.4f}]"
        print(f"{v:<10} {s['n']:<10} {s['successes']:<12} {s['rate']:<12.4f} {ci_str:<20}")

    # Pairwise comparisons
    print("\n--- Pairwise Comparisons (Chi-Square Test) ---\n")
    best_variant = None
    best_rate = -1

    for i, v1 in enumerate(variant_names):
        for v2 in variant_names[i + 1:]:
            s1 = variant_stats[v1]
            s2 = variant_stats[v2]
            chi2, p_val = chi_square_test(s1["successes"], s1["n"], s2["successes"], s2["n"])
            lift = ((s1["rate"] - s2["rate"]) / s2["rate"] * 100) if s2["rate"] > 0 else 0
            sig = "YES" if p_val < 0.05 else "NO"

            print(f"  {v1} vs {v2}:")
            print(f"    Chi-square statistic: {chi2:.4f}")
            print(f"    p-value: {p_val:.6f}")
            print(f"    Significant (p<0.05): {sig}")
            print(f"    Lift ({v1} over {v2}): {lift:+.1f}%")
            if p_val < 0.05:
                winner = v1 if s1["rate"] > s2["rate"] else v2
                print(f"    Winner: {winner}")
            print()

    for v in variant_names:
        if variant_stats[v]["rate"] > best_rate:
            best_rate = variant_stats[v]["rate"]
            best_variant = v

    # Sample size recommendation
    if best_rate > 0 and best_rate < 1:
        needed = min_sample_size(best_rate, mde_relative=0.2)
        current_min = min(variant_stats[v]["n"] for v in variant_names)
        print(f"--- Sample Size Analysis ---")
        print(f"  To detect 20% relative change from {best_rate:.4f} baseline:")
        print(f"    Minimum per variant: {needed}")
        print(f"    Current minimum: {current_min}")
        if current_min < needed:
            print(f"    NEED {needed - current_min} MORE per variant for reliable results")
        else:
            print(f"    SUFFICIENT sample size")
    print()

    # Overall verdict
    print("=" * 60)
    print(f"  CURRENT LEADER: Variant {best_variant} ({best_rate:.4f})")
    any_sig = False
    for i, v1 in enumerate(variant_names):
        for v2 in variant_names[i + 1:]:
            s1 = variant_stats[v1]
            s2 = variant_stats[v2]
            _, p_val = chi_square_test(s1["successes"], s1["n"], s2["successes"], s2["n"])
            if p_val < 0.05:
                any_sig = True
    if any_sig:
        print(f"  STATUS: Statistically significant differences found")
    else:
        print(f"  STATUS: No statistically significant differences yet")
    print("=" * 60)


def _analyze_continuous(exp_id, variants, variant_names, metric_name):
    """Analyze continuous metrics using Welch's t-test."""
    variant_stats = {}
    for v in variant_names:
        values = []
        total_n = 0
        for row in variants[v]:
            val = float(row.get("value", 0))
            n = int(row.get("n", 1))
            total_n += n
            values.extend([val] * n)
        if not values:
            variant_stats[v] = {"n": 0, "mean": 0, "std": 0, "var": 0, "ci_low": 0, "ci_high": 0, "values": []}
            continue
        m = statistics.mean(values)
        s = statistics.stdev(values) if len(values) > 1 else 0
        v_val = s * s
        _, ci_low, ci_high = confidence_interval_mean(values)
        variant_stats[v] = {
            "n": len(values),
            "mean": m,
            "std": s,
            "var": v_val,
            "ci_low": ci_low,
            "ci_high": ci_high,
            "values": values,
        }

    # Print variant summary
    print(f"\n{'Variant':<10} {'N':<10} {'Mean':<12} {'Std Dev':<12} {'95% CI':<24}")
    print("-" * 68)
    for v in variant_names:
        s = variant_stats[v]
        ci_str = f"[{s['ci_low']:.4f}, {s['ci_high']:.4f}]"
        print(f"{v:<10} {s['n']:<10} {s['mean']:<12.4f} {s['std']:<12.4f} {ci_str:<24}")

    # Pairwise comparisons
    print("\n--- Pairwise Comparisons (Welch's t-test) ---\n")
    best_variant = None
    best_mean = -float("inf")

    for i, v1 in enumerate(variant_names):
        for v2 in variant_names[i + 1:]:
            s1 = variant_stats[v1]
            s2 = variant_stats[v2]
            t_stat, df, p_val = welch_t_test(s1["mean"], s1["var"], s1["n"],
                                             s2["mean"], s2["var"], s2["n"])
            diff = s1["mean"] - s2["mean"]
            pct_diff = (diff / s2["mean"] * 100) if s2["mean"] != 0 else 0
            sig = "YES" if p_val < 0.05 else "NO"

            print(f"  {v1} vs {v2}:")
            print(f"    t-statistic: {t_stat:.4f}")
            print(f"    Degrees of freedom: {df:.1f}")
            print(f"    p-value: {p_val:.6f}")
            print(f"    Significant (p<0.05): {sig}")
            print(f"    Difference: {diff:+.4f} ({pct_diff:+.1f}%)")
            if p_val < 0.05:
                winner = v1 if s1["mean"] > s2["mean"] else v2
                print(f"    Winner: {winner}")
            print()

    for v in variant_names:
        if variant_stats[v]["mean"] > best_mean:
            best_mean = variant_stats[v]["mean"]
            best_variant = v

    print("=" * 60)
    print(f"  CURRENT LEADER: Variant {best_variant} (mean={best_mean:.4f})")
    any_sig = False
    for i, v1 in enumerate(variant_names):
        for v2 in variant_names[i + 1:]:
            s1 = variant_stats[v1]
            s2 = variant_stats[v2]
            _, _, p_val = welch_t_test(s1["mean"], s1["var"], s1["n"],
                                       s2["mean"], s2["var"], s2["n"])
            if p_val < 0.05:
                any_sig = True
    if any_sig:
        print(f"  STATUS: Statistically significant differences found")
    else:
        print(f"  STATUS: No statistically significant differences yet")
    print("=" * 60)


def cmd_complete(args):
    """Complete an experiment, record the learning."""
    exp_id = args.id
    winner = args.winner
    notes = args.notes or ""
    today = datetime.now().strftime("%Y-%m-%d")

    # Update AB tests
    ab_tests = load_ab_tests()
    found = False
    for row in ab_tests:
        if row.get("test_id", "").strip() == exp_id:
            row["status"] = "COMPLETED"
            row["result"] = "WINNER_FOUND" if winner else "NO_WINNER"
            row["winner"] = winner
            row["notes"] = notes
            found = True
            break
    if found:
        save_ab_tests(ab_tests)

    # Update hypotheses
    hypotheses = load_hypotheses()
    hyp_record = None
    for h in hypotheses:
        if h.get("id", "").strip() == exp_id:
            h["status"] = "COMPLETED"
            h["winner"] = winner
            h["completed_date"] = today
            h["notes"] = notes
            hyp_record = h
            found = True
            break
    if hyp_record:
        save_hypotheses(hypotheses)

    if not found:
        print(f"[ERROR] Experiment '{exp_id}' not found")
        sys.exit(1)

    # Append learning to LEARNINGS.jsonl
    learning = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "category": "experiment_result",
        "experiment_id": exp_id,
        "winner": winner,
        "finding": notes,
        "action": f"Apply variant {winner} as default. Update playbooks.",
        "evidence": f"A/B test {exp_id} completed {today}",
    }
    append_learning(learning)

    print(f"[COMPLETED] {exp_id}")
    print(f"  Winner: {winner}")
    print(f"  Notes: {notes}")
    print(f"  Learning appended to {LEARNINGS_JSONL}")


def cmd_recommend(args):
    """Recommend top 3 experiments to start based on effort vs impact."""
    ab_tests = load_ab_tests()
    hypotheses = load_hypotheses()

    candidates = []

    # Score AB tests
    for row in ab_tests:
        if row.get("status", "").strip() not in ("NOT_STARTED", "PENDING"):
            continue
        # Impact proxy: lower sample size target = faster result
        try:
            sample_target = int(row.get("sample_size_target", 1000))
        except (ValueError, TypeError):
            sample_target = 1000
        # Paywall and pricing tests are highest impact
        test_type = row.get("test_type", "")
        impact = 5
        if "paywall" in test_type or "pricing" in test_type:
            impact = 9
        elif "cta" in test_type:
            impact = 7
        elif "onboarding" in test_type:
            impact = 6
        elif "email" in test_type or "ad" in test_type:
            impact = 7
        elif "landing" in test_type:
            impact = 8
        # Effort is inverse of sample size (smaller = easier)
        effort = 10 - min(sample_target / 200, 9)
        score = impact * 0.6 + effort * 0.4
        candidates.append({
            "id": row.get("test_id", "?"),
            "source": "AB_TESTS",
            "hypothesis": row.get("hypothesis", "")[:60],
            "impact": impact,
            "effort_score": effort,
            "score": score,
            "metric": row.get("metric", "?"),
        })

    # Score hypotheses
    effort_map = {"LOW": 8, "MEDIUM": 5, "HIGH": 3}
    for h in hypotheses:
        if h.get("status", "").strip() not in ("NOT STARTED", "NOT_STARTED", "PENDING"):
            continue
        effort_str = h.get("effort", "MEDIUM").upper()
        effort_score = 5
        for key, val in effort_map.items():
            if key in effort_str:
                effort_score = val
                break
        # All hypotheses have explicit targets, so impact is high
        impact = 8
        score = impact * 0.6 + effort_score * 0.4
        candidates.append({
            "id": h.get("id", "?"),
            "source": "HYPOTHESES",
            "hypothesis": h.get("hypothesis", "")[:60],
            "impact": impact,
            "effort_score": effort_score,
            "score": score,
            "metric": h.get("metric", "?"),
        })

    candidates.sort(key=lambda x: x["score"], reverse=True)

    print("=" * 80)
    print("TOP EXPERIMENT RECOMMENDATIONS (effort-adjusted impact)")
    print("=" * 80)

    for i, c in enumerate(candidates[:3], 1):
        print(f"\n  #{i}  {c['id']} (score: {c['score']:.1f})")
        print(f"      Source: {c['source']}")
        print(f"      Hypothesis: {c['hypothesis']}")
        print(f"      Metric: {c['metric']}")
        print(f"      Impact: {c['impact']}/10 | Effort: {c['effort_score']:.0f}/10 (higher=easier)")
        print(f"      Start: python3 scripts/experiment_runner.py start {c['id']}")

    remaining = len(candidates) - 3
    if remaining > 0:
        print(f"\n  ... and {remaining} more candidates")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Experiment Runner - A/B test management and statistical analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/experiment_runner.py list
  python3 scripts/experiment_runner.py start H001
  python3 scripts/experiment_runner.py log H001 --variant A --metric conversion_rate --value 0.045 --n 100
  python3 scripts/experiment_runner.py analyze H001
  python3 scripts/experiment_runner.py complete H001 --winner A --notes "Animated paywall 2.3x better"
  python3 scripts/experiment_runner.py recommend
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # list
    subparsers.add_parser("list", help="Show all experiments with status")

    # start
    p_start = subparsers.add_parser("start", help="Mark experiment as RUNNING")
    p_start.add_argument("id", help="Experiment ID (e.g. H001, APP-PAY-001)")

    # log
    p_log = subparsers.add_parser("log", help="Log a data point")
    p_log.add_argument("id", help="Experiment ID")
    p_log.add_argument("--variant", required=True, help="Variant name (e.g. A, B, C)")
    p_log.add_argument("--metric", required=True, help="Metric name")
    p_log.add_argument("--value", required=True, type=float, help="Metric value")
    p_log.add_argument("--n", required=True, type=int, help="Sample size")

    # analyze
    p_analyze = subparsers.add_parser("analyze", help="Statistical analysis")
    p_analyze.add_argument("id", help="Experiment ID")

    # complete
    p_complete = subparsers.add_parser("complete", help="Complete experiment")
    p_complete.add_argument("id", help="Experiment ID")
    p_complete.add_argument("--winner", required=True, help="Winning variant")
    p_complete.add_argument("--notes", default="", help="Result notes/learnings")

    # recommend
    subparsers.add_parser("recommend", help="Recommend top 3 experiments to start")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "list": cmd_list,
        "start": cmd_start,
        "log": cmd_log,
        "analyze": cmd_analyze,
        "complete": cmd_complete,
        "recommend": cmd_recommend,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
