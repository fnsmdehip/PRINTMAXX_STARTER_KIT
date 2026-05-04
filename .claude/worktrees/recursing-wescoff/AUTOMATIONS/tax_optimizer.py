#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Tax Optimizer
========================
Tax efficiency for solopreneurs. Schedule C categorization, deduction
identification, quarterly estimates, and tax reports.

Usage:
    python3 AUTOMATIONS/tax_optimizer.py --categorize
    python3 AUTOMATIONS/tax_optimizer.py --deductions
    python3 AUTOMATIONS/tax_optimizer.py --quarterly-estimate
    python3 AUTOMATIONS/tax_optimizer.py --report Q1
"""

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime, date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FINANCIALS = BASE_DIR / "FINANCIALS"
REVENUE_CSV = FINANCIALS / "REVENUE_TRACKER.csv"
EXPENSE_CSV = FINANCIALS / "EXPENSE_TRACKER.csv"

W = 76

# ---------------------------------------------------------------------------
# Schedule C expense categories (IRS lines)
# ---------------------------------------------------------------------------

SCHEDULE_C_CATEGORIES = {
    "advertising": {
        "line": 8,
        "description": "Advertising & marketing",
        "keywords": ["ad", "ads", "marketing", "advertising", "promo", "sponsor",
                      "facebook ads", "google ads", "tiktok ads", "instagram"],
    },
    "car_and_truck": {
        "line": 9,
        "description": "Car and truck expenses",
        "keywords": ["gas", "fuel", "mileage", "car", "uber", "lyft", "parking",
                      "toll", "vehicle", "auto"],
    },
    "commissions": {
        "line": 10,
        "description": "Commissions and fees",
        "keywords": ["commission", "referral fee", "affiliate payout", "finder fee"],
    },
    "contract_labor": {
        "line": 11,
        "description": "Contract labor",
        "keywords": ["contractor", "freelancer", "va ", "virtual assistant",
                      "fiverr", "upwork", "subcontractor"],
    },
    "depreciation": {
        "line": 13,
        "description": "Depreciation (Section 179)",
        "keywords": ["computer", "laptop", "macbook", "monitor", "desk",
                      "chair", "camera", "microphone", "equipment"],
    },
    "insurance": {
        "line": 15,
        "description": "Insurance",
        "keywords": ["insurance", "liability", "e&o", "health insurance"],
    },
    "interest_mortgage": {
        "line": 16,
        "description": "Interest on business debt",
        "keywords": ["interest", "loan payment", "business credit"],
    },
    "legal_professional": {
        "line": 17,
        "description": "Legal and professional services",
        "keywords": ["lawyer", "attorney", "legal", "accountant", "cpa",
                      "tax prep", "bookkeeper"],
    },
    "office_expense": {
        "line": 18,
        "description": "Office expenses",
        "keywords": ["office", "supplies", "printer", "paper", "ink",
                      "stationery", "postage", "shipping"],
    },
    "rent_lease": {
        "line": 20,
        "description": "Rent or lease (business property)",
        "keywords": ["rent", "lease", "coworking", "wework", "office space"],
    },
    "repairs": {
        "line": 21,
        "description": "Repairs and maintenance",
        "keywords": ["repair", "maintenance", "fix"],
    },
    "supplies": {
        "line": 22,
        "description": "Supplies",
        "keywords": ["supplies", "materials"],
    },
    "taxes_licenses": {
        "line": 23,
        "description": "Taxes and licenses",
        "keywords": ["license", "permit", "business license", "llc fee",
                      "state fee", "annual report"],
    },
    "travel": {
        "line": 24,
        "description": "Travel",
        "keywords": ["flight", "hotel", "airbnb", "travel", "conference",
                      "lodging", "train"],
    },
    "meals": {
        "line": 24,
        "description": "Meals (50% deductible)",
        "keywords": ["meal", "lunch", "dinner", "restaurant", "food",
                      "coffee meeting", "client dinner"],
        "deductible_pct": 50,
    },
    "utilities": {
        "line": 25,
        "description": "Utilities",
        "keywords": ["electric", "gas bill", "water", "internet", "phone",
                      "wifi", "cellular"],
    },
    "software_subscriptions": {
        "line": 27,
        "description": "Other expenses - Software & subscriptions",
        "keywords": ["software", "saas", "subscription", "tool", "api",
                      "hosting", "domain", "cloud", "aws", "vercel", "heroku",
                      "github", "notion", "slack", "zoom", "chatgpt", "openai",
                      "anthropic", "claude", "cursor", "figma", "canva",
                      "ahrefs", "semrush", "mailchimp", "convertkit",
                      "stripe fee", "gumroad fee", "platform fee",
                      "apple developer", "google play", "app store"],
    },
    "education": {
        "line": 27,
        "description": "Other expenses - Education & training",
        "keywords": ["course", "book", "training", "workshop", "seminar",
                      "udemy", "skillshare", "masterclass", "coaching"],
    },
    "home_office": {
        "line": 30,
        "description": "Home office deduction (Form 8829)",
        "keywords": ["home office"],
        "note": "Simplified method: $5/sqft up to 300 sqft = $1,500 max",
    },
}

# Map raw expense categories to Schedule C
CATEGORY_MAP = {
    "INFRASTRUCTURE": "software_subscriptions",
    "TOOLS": "software_subscriptions",
    "SOFTWARE": "software_subscriptions",
    "HOSTING": "software_subscriptions",
    "MARKETING": "advertising",
    "ADS": "advertising",
    "EQUIPMENT": "depreciation",
    "HARDWARE": "depreciation",
    "TRAVEL": "travel",
    "MEALS": "meals",
    "EDUCATION": "education",
    "LEGAL": "legal_professional",
    "INSURANCE": "insurance",
    "OFFICE": "office_expense",
    "SUPPLIES": "supplies",
    "CONTRACT": "contract_labor",
    "FREELANCER": "contract_labor",
}

# Quarters
QUARTERS = {
    "Q1": (1, 3),  # Jan-Mar
    "Q2": (4, 6),  # Apr-Jun
    "Q3": (7, 9),  # Jul-Sep
    "Q4": (10, 12),  # Oct-Dec
}

# 2025/2026 estimated tax brackets (single filer, approximate)
TAX_BRACKETS = [
    (11600, 0.10),
    (47150, 0.12),
    (100525, 0.22),
    (191950, 0.24),
    (243725, 0.32),
    (609350, 0.35),
    (float("inf"), 0.37),
]

SE_TAX_RATE = 0.153  # 15.3% self-employment tax
SE_DEDUCTION_RATE = 0.5  # deduct half of SE tax
QBI_DEDUCTION_RATE = 0.20  # 20% QBI deduction for pass-through


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def safe_float(val, default=0.0):
    if val is None:
        return default
    s = str(val).strip().replace("$", "").replace(",", "")
    if not s:
        return default
    try:
        return float(s)
    except (ValueError, TypeError):
        return default


def load_expenses():
    if not EXPENSE_CSV.exists():
        return []
    rows = []
    try:
        with open(EXPENSE_CSV, "r", newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    d = datetime.strptime(row.get("date", ""), "%Y-%m-%d").date()
                except (ValueError, KeyError):
                    continue
                rows.append({
                    "date": d,
                    "category": row.get("category", "UNCATEGORIZED"),
                    "item": row.get("item", ""),
                    "amount": safe_float(row.get("amount")),
                    "recurring": row.get("recurring", "FALSE").upper() == "TRUE",
                    "frequency": row.get("frequency", "one-time"),
                    "method_id": row.get("method_id", ""),
                    "notes": row.get("notes", ""),
                })
    except Exception:
        pass
    return rows


def load_revenue():
    if not REVENUE_CSV.exists():
        return []
    rows = []
    try:
        with open(REVENUE_CSV, "r", newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    d = datetime.strptime(row.get("date", ""), "%Y-%m-%d").date()
                except (ValueError, KeyError):
                    continue
                rows.append({
                    "date": d,
                    "revenue": safe_float(row.get("revenue")),
                    "expenses": safe_float(row.get("expenses")),
                    "profit": safe_float(row.get("profit")),
                    "method_id": row.get("method_id", ""),
                    "source": row.get("source", ""),
                })
    except Exception:
        pass
    return rows


# ---------------------------------------------------------------------------
# Categorization engine
# ---------------------------------------------------------------------------

def categorize_expense(expense):
    """Map an expense to a Schedule C category."""
    raw_cat = expense["category"].upper().strip()
    item = expense["item"].lower()
    notes = expense.get("notes", "").lower()
    combined = f"{item} {notes} {raw_cat.lower()}"

    # Direct category map
    if raw_cat in CATEGORY_MAP:
        return CATEGORY_MAP[raw_cat]

    # Keyword matching
    best_match = None
    best_score = 0
    for sched_cat, info in SCHEDULE_C_CATEGORIES.items():
        score = 0
        for kw in info["keywords"]:
            if kw.lower() in combined:
                # Longer keyword matches are more specific
                score += len(kw)
        if score > best_score:
            best_score = score
            best_match = sched_cat

    return best_match or "software_subscriptions"  # default for tech solopreneur


def categorize_all(expenses):
    """Categorize all expenses and return grouped results."""
    categorized = defaultdict(lambda: {"items": [], "total": 0.0})

    for exp in expenses:
        cat = categorize_expense(exp)
        deductible_pct = SCHEDULE_C_CATEGORIES.get(cat, {}).get("deductible_pct", 100)
        deductible_amount = exp["amount"] * deductible_pct / 100

        categorized[cat]["items"].append({
            **exp,
            "schedule_c_category": cat,
            "deductible_pct": deductible_pct,
            "deductible_amount": deductible_amount,
        })
        categorized[cat]["total"] += deductible_amount

    return categorized


# ---------------------------------------------------------------------------
# Deduction identification
# ---------------------------------------------------------------------------

COMMON_DEDUCTIONS = [
    {
        "name": "Home Office Deduction",
        "description": "Simplified: $5/sqft, up to 300 sqft = $1,500 max",
        "max_amount": 1500,
        "category": "home_office",
        "check": lambda exps: not any("home office" in e["item"].lower() for e in exps),
    },
    {
        "name": "Internet (Business %)",
        "description": "50-100% of internet bill if work from home",
        "estimated_annual": 720,  # $60/mo avg
        "category": "utilities",
        "check": lambda exps: not any("internet" in e["item"].lower() or "wifi" in e["item"].lower() for e in exps),
    },
    {
        "name": "Phone (Business %)",
        "description": "Business percentage of phone bill",
        "estimated_annual": 480,  # $40/mo avg
        "category": "utilities",
        "check": lambda exps: not any("phone" in e["item"].lower() or "cellular" in e["item"].lower() for e in exps),
    },
    {
        "name": "Health Insurance Premium",
        "description": "Self-employed health insurance deduction (above-the-line)",
        "estimated_annual": 6000,
        "category": "insurance",
        "check": lambda exps: not any("health" in e["item"].lower() and "insurance" in e["item"].lower() for e in exps),
    },
    {
        "name": "SEP IRA / Solo 401k Contribution",
        "description": "Up to 25% of net SE income, max $69,000 (2024)",
        "estimated_annual": None,  # Depends on income
        "category": "retirement",
        "check": lambda exps: True,  # Always suggest
    },
    {
        "name": "Software Subscriptions",
        "description": "All business software: IDE, design, hosting, APIs",
        "estimated_annual": 2400,  # $200/mo avg
        "category": "software_subscriptions",
        "check": lambda exps: sum(e["amount"] for e in exps if "software" in categorize_expense(e)) < 500,
    },
    {
        "name": "Professional Development",
        "description": "Books, courses, conferences related to business",
        "estimated_annual": 1000,
        "category": "education",
        "check": lambda exps: not any("course" in e["item"].lower() or "book" in e["item"].lower() for e in exps),
    },
    {
        "name": "Business Banking Fees",
        "description": "Bank fees, payment processor fees (Stripe, PayPal)",
        "estimated_annual": 360,
        "category": "commissions",
        "check": lambda exps: not any("fee" in e["item"].lower() or "stripe" in e["item"].lower() for e in exps),
    },
    {
        "name": "Equipment (Section 179)",
        "description": "Computer, monitor, desk, chair - deduct full cost in year 1",
        "estimated_annual": 2000,
        "category": "depreciation",
        "check": lambda exps: not any("computer" in e["item"].lower() or "laptop" in e["item"].lower() for e in exps),
    },
    {
        "name": "Mileage Deduction",
        "description": "67 cents/mile (2024) for business driving",
        "estimated_annual": 2000,  # ~3000 miles
        "category": "car_and_truck",
        "check": lambda exps: not any("mileage" in e["item"].lower() or "gas" in e["item"].lower() for e in exps),
    },
    {
        "name": "Domain Names & Hosting",
        "description": "All domain registrations and web hosting",
        "estimated_annual": 300,
        "category": "software_subscriptions",
        "check": lambda exps: not any("domain" in e["item"].lower() or "hosting" in e["item"].lower() for e in exps),
    },
]


def find_missing_deductions(expenses):
    """Identify deductions that are not being tracked."""
    missing = []
    for deduction in COMMON_DEDUCTIONS:
        if deduction["check"](expenses):
            missing.append(deduction)
    return missing


# ---------------------------------------------------------------------------
# Tax calculation
# ---------------------------------------------------------------------------

def calculate_income_tax(taxable_income):
    """Calculate federal income tax using brackets."""
    tax = 0.0
    prev_limit = 0
    for limit, rate in TAX_BRACKETS:
        if taxable_income <= prev_limit:
            break
        bracket_income = min(taxable_income, limit) - prev_limit
        if bracket_income > 0:
            tax += bracket_income * rate
        prev_limit = limit
    return tax


def calculate_quarterly_estimate(annual_revenue, annual_expenses, quarter=None):
    """Calculate quarterly estimated tax payment.

    Accounts for:
    - Self-employment tax (15.3%)
    - SE tax deduction (half of SE tax)
    - QBI deduction (20% of qualified business income)
    - Federal income tax brackets
    """
    net_profit = annual_revenue - annual_expenses
    if net_profit <= 0:
        return {
            "net_profit": net_profit,
            "se_tax": 0,
            "income_tax": 0,
            "total_tax": 0,
            "quarterly_payment": 0,
            "effective_rate": 0,
        }

    # Self-employment tax
    se_taxable = net_profit * 0.9235  # 92.35% of net profit
    se_tax = se_taxable * SE_TAX_RATE
    se_tax = min(se_tax, 168600 * 0.124 + se_taxable * 0.029)  # SS cap + Medicare

    # Deductions
    se_deduction = se_tax * SE_DEDUCTION_RATE
    qbi_deduction = net_profit * QBI_DEDUCTION_RATE

    # Standard deduction (single filer 2025 estimate)
    standard_deduction = 15000

    # Taxable income
    taxable_income = net_profit - se_deduction - qbi_deduction - standard_deduction
    taxable_income = max(0, taxable_income)

    # Income tax
    income_tax = calculate_income_tax(taxable_income)

    # Total
    total_tax = se_tax + income_tax
    quarterly = total_tax / 4
    effective_rate = (total_tax / net_profit * 100) if net_profit > 0 else 0

    result = {
        "gross_revenue": round(annual_revenue, 2),
        "total_expenses": round(annual_expenses, 2),
        "net_profit": round(net_profit, 2),
        "se_taxable_income": round(se_taxable, 2),
        "se_tax": round(se_tax, 2),
        "se_deduction": round(se_deduction, 2),
        "qbi_deduction": round(qbi_deduction, 2),
        "standard_deduction": standard_deduction,
        "taxable_income": round(taxable_income, 2),
        "income_tax": round(income_tax, 2),
        "total_annual_tax": round(total_tax, 2),
        "quarterly_payment": round(quarterly, 2),
        "effective_rate": round(effective_rate, 1),
    }

    if quarter:
        # Adjust for specific quarter (prorate based on YTD)
        q_start, q_end = QUARTERS.get(quarter, (1, 3))
        q_number = list(QUARTERS.keys()).index(quarter) + 1 if quarter in QUARTERS else 1
        result["quarter"] = quarter
        result["quarterly_due_date"] = {
            "Q1": "April 15",
            "Q2": "June 15",
            "Q3": "September 15",
            "Q4": "January 15 (next year)",
        }.get(quarter, "Unknown")

    return result


# ---------------------------------------------------------------------------
# Display functions
# ---------------------------------------------------------------------------

def hr(char="="):
    return char * W


def print_header(title):
    print(hr())
    print(f"  {title}".center(W))
    print(hr())
    print()


def print_section(title):
    print(f"  {title}")
    print(f"  {'-' * (W - 4)}")


def cmd_categorize():
    """Categorize all expenses for Schedule C."""
    expenses = load_expenses()

    print_header("SCHEDULE C EXPENSE CATEGORIZATION")

    if not expenses:
        print("  No expenses found in EXPENSE_TRACKER.csv")
        print("  Add expenses to get started.")
        print(hr())
        return

    categorized = categorize_all(expenses)
    total_deductible = 0.0
    total_raw = 0.0

    # Sort by Schedule C line number
    sorted_cats = sorted(
        categorized.items(),
        key=lambda x: SCHEDULE_C_CATEGORIES.get(x[0], {}).get("line", 99)
    )

    for cat, data in sorted_cats:
        info = SCHEDULE_C_CATEGORIES.get(cat, {})
        line = info.get("line", "?")
        desc = info.get("description", cat)
        deduct_pct = info.get("deductible_pct", 100)

        cat_total = sum(item["amount"] for item in data["items"])
        deductible = data["total"]
        total_raw += cat_total
        total_deductible += deductible

        pct_note = f" ({deduct_pct}% deductible)" if deduct_pct < 100 else ""
        print(f"\n  LINE {line}: {desc}{pct_note}")
        print(f"  {'.' * (W - 4)}")
        for item in sorted(data["items"], key=lambda x: x["amount"], reverse=True):
            deduct_str = ""
            if deduct_pct < 100:
                deduct_str = f"  (deductible: ${item['deductible_amount']:.2f})"
            print(f"    {item['date']}  ${item['amount']:>8,.2f}  {item['item'][:35]}{deduct_str}")
        print(f"    {'SUBTOTAL:':>48} ${deductible:>10,.2f}")

    print(f"\n  {'=' * (W - 4)}")
    print(f"  TOTAL EXPENSES:          ${total_raw:>12,.2f}")
    print(f"  TOTAL DEDUCTIBLE:        ${total_deductible:>12,.2f}")
    if total_raw != total_deductible:
        print(f"  NON-DEDUCTIBLE PORTION:  ${total_raw - total_deductible:>12,.2f}")

    print()
    print(hr())


def cmd_deductions():
    """Identify missing deductions."""
    expenses = load_expenses()

    print_header("MISSING DEDUCTION FINDER")

    # Current deductions
    categorized = categorize_all(expenses)
    current_total = sum(data["total"] for data in categorized.values())

    print_section("CURRENT DEDUCTIONS TRACKED")
    print(f"  Total Tracked:  ${current_total:>10,.2f}")
    print(f"  Categories:     {len(categorized)}")
    print()

    # Missing deductions
    missing = find_missing_deductions(expenses)

    if not missing:
        print_section("DEDUCTION STATUS: COMPLETE")
        print("  All common deductions appear to be tracked.")
    else:
        print_section(f"MISSING DEDUCTIONS IDENTIFIED: {len(missing)}")
        total_missing = 0.0
        for d in missing:
            est = d.get("estimated_annual") or d.get("max_amount", 0)
            total_missing += est or 0
            est_str = f"${est:,.0f}/yr est." if est else "varies"
            print(f"\n  {d['name']}")
            print(f"    {d['description']}")
            print(f"    Estimated Value: {est_str}")
            print(f"    Schedule C Category: {d['category']}")

        print(f"\n  ESTIMATED UNCLAIMED DEDUCTIONS: ${total_missing:>10,.2f}")

        # Tax savings estimate
        # Assume 22% marginal bracket + 15.3% SE tax
        marginal_rate = 0.22 + 0.153
        savings = total_missing * marginal_rate
        print(f"  ESTIMATED TAX SAVINGS:         ${savings:>10,.2f}")
        print(f"  (At marginal rate of {marginal_rate*100:.1f}%: "
              f"22% income + 15.3% SE)")

    # Action items
    print()
    print_section("ACTION ITEMS")
    print("  1. Add missing deductions to FINANCIALS/EXPENSE_TRACKER.csv")
    print("  2. Keep ALL receipts (digital photo or email forward)")
    print("  3. Track mileage with an app (Stride, MileIQ)")
    print("  4. Measure home office square footage (take photo)")
    print("  5. Document business purpose for meals/travel")
    print("  6. Consider SEP IRA contribution before tax deadline")

    print()
    print(hr())


def cmd_quarterly_estimate():
    """Calculate quarterly estimated tax payment."""
    revenue_rows = load_revenue()
    expenses = load_expenses()

    print_header("QUARTERLY ESTIMATED TAX CALCULATION")

    today = date.today()
    current_year = today.year

    # YTD revenue
    ytd_revenue = sum(r["revenue"] for r in revenue_rows if r["date"].year == current_year)
    ytd_expenses_rev = sum(r["expenses"] for r in revenue_rows if r["date"].year == current_year)
    ytd_expenses_exp = sum(e["amount"] for e in expenses if e["date"].year == current_year)
    ytd_total_expenses = ytd_expenses_rev + ytd_expenses_exp

    # Annualize
    days_elapsed = (today - date(current_year, 1, 1)).days + 1
    days_in_year = 365
    annualization_factor = days_in_year / days_elapsed if days_elapsed > 0 else 1

    annualized_revenue = ytd_revenue * annualization_factor
    annualized_expenses = ytd_total_expenses * annualization_factor

    print_section("YEAR-TO-DATE ACTUALS")
    print(f"  Period:             Jan 1 - {today.strftime('%b %d, %Y')} ({days_elapsed} days)")
    print(f"  YTD Revenue:        ${ytd_revenue:>12,.2f}")
    print(f"  YTD Expenses:       ${ytd_total_expenses:>12,.2f}")
    print(f"  YTD Net Profit:     ${ytd_revenue - ytd_total_expenses:>12,.2f}")
    print()

    print_section("ANNUALIZED PROJECTION")
    print(f"  Annualized Revenue: ${annualized_revenue:>12,.2f}")
    print(f"  Annualized Expenses:${annualized_expenses:>12,.2f}")
    print(f"  Projected Net:      ${annualized_revenue - annualized_expenses:>12,.2f}")
    print()

    # Calculate for each scenario
    scenarios = [
        ("ACTUAL YTD (Annualized)", annualized_revenue, annualized_expenses),
        ("Conservative (50% of projected)", annualized_revenue * 0.5, annualized_expenses * 0.7),
        ("Aggressive (150% of projected)", annualized_revenue * 1.5, annualized_expenses * 1.2),
    ]

    for label, rev, exp in scenarios:
        calc = calculate_quarterly_estimate(rev, exp)
        print_section(f"SCENARIO: {label}")
        print(f"  Net Profit:         ${calc['net_profit']:>12,.2f}")
        print(f"  Self-Employment Tax:${calc['se_tax']:>12,.2f}")
        print(f"  SE Tax Deduction:   ${calc['se_deduction']:>12,.2f}")
        print(f"  QBI Deduction:      ${calc['qbi_deduction']:>12,.2f}")
        print(f"  Standard Deduction: ${calc['standard_deduction']:>12,.2f}")
        print(f"  Taxable Income:     ${calc['taxable_income']:>12,.2f}")
        print(f"  Income Tax:         ${calc['income_tax']:>12,.2f}")
        print(f"  Total Annual Tax:   ${calc['total_annual_tax']:>12,.2f}")
        print(f"  Quarterly Payment:  ${calc['quarterly_payment']:>12,.2f}")
        print(f"  Effective Rate:     {calc['effective_rate']:>12.1f}%")
        print()

    # Due dates
    print_section("QUARTERLY DUE DATES")
    print("  Q1 (Jan-Mar):  April 15")
    print("  Q2 (Apr-Jun):  June 15")
    print("  Q3 (Jul-Sep):  September 15")
    print("  Q4 (Oct-Dec):  January 15 (next year)")
    print()

    # Current quarter
    current_month = today.month
    for q, (start, end) in QUARTERS.items():
        if start <= current_month <= end:
            print(f"  CURRENT QUARTER: {q} ({today.strftime('%B %Y')})")
            break

    print()
    print(hr())


def cmd_report(quarter):
    """Generate quarterly tax report."""
    quarter = quarter.upper()
    if quarter not in QUARTERS:
        print(f"ERROR: Invalid quarter '{quarter}'. Use Q1, Q2, Q3, or Q4.")
        sys.exit(1)

    revenue_rows = load_revenue()
    expenses = load_expenses()

    q_start_month, q_end_month = QUARTERS[quarter]
    current_year = date.today().year

    print_header(f"QUARTERLY TAX REPORT: {quarter} {current_year}")

    # Filter to quarter
    q_revenue = [r for r in revenue_rows
                 if r["date"].year == current_year
                 and q_start_month <= r["date"].month <= q_end_month]

    q_expenses = [e for e in expenses
                  if e["date"].year == current_year
                  and q_start_month <= e["date"].month <= q_end_month]

    q_rev_total = sum(r["revenue"] for r in q_revenue)
    q_rev_expenses = sum(r["expenses"] for r in q_revenue)
    q_exp_total = sum(e["amount"] for e in q_expenses)
    q_total_expenses = q_rev_expenses + q_exp_total
    q_net = q_rev_total - q_total_expenses

    # Quarter dates
    month_names = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                   7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    start_name = month_names[q_start_month]
    end_name = month_names[q_end_month]

    print_section(f"INCOME SUMMARY ({start_name} - {end_name} {current_year})")
    print(f"  Gross Revenue:      ${q_rev_total:>12,.2f}  ({len(q_revenue)} transactions)")
    print(f"  Direct Costs:       ${q_rev_expenses:>12,.2f}")
    print(f"  Overhead Expenses:  ${q_exp_total:>12,.2f}  ({len(q_expenses)} items)")
    print(f"  Net Profit:         ${q_net:>12,.2f}")
    margin = (q_net / q_rev_total * 100) if q_rev_total > 0 else 0
    print(f"  Profit Margin:      {margin:>12.1f}%")
    print()

    # Revenue by source
    if q_revenue:
        print_section("REVENUE BY SOURCE")
        by_source = defaultdict(float)
        for r in q_revenue:
            by_source[r.get("source", "DIRECT") or "DIRECT"] += r["revenue"]
        for src, amt in sorted(by_source.items(), key=lambda x: x[1], reverse=True):
            pct = (amt / q_rev_total * 100) if q_rev_total > 0 else 0
            print(f"    {src:<30} ${amt:>10,.2f}  ({pct:.1f}%)")
        print()

    # Categorized expenses
    if q_expenses:
        categorized = categorize_all(q_expenses)
        print_section("EXPENSES BY SCHEDULE C CATEGORY")
        for cat, data in sorted(categorized.items(),
                                key=lambda x: SCHEDULE_C_CATEGORIES.get(x[0], {}).get("line", 99)):
            info = SCHEDULE_C_CATEGORIES.get(cat, {})
            line = info.get("line", "?")
            desc = info.get("description", cat)
            print(f"    Line {line}: {desc:<40} ${data['total']:>10,.2f}")
        print()

    # Tax estimate for this quarter
    annualized_rev = q_rev_total * 4
    annualized_exp = q_total_expenses * 4
    calc = calculate_quarterly_estimate(annualized_rev, annualized_exp, quarter)

    print_section(f"TAX ESTIMATE FOR {quarter}")
    print(f"  Annualized Revenue: ${annualized_rev:>12,.2f}")
    print(f"  Annualized Profit:  ${calc['net_profit']:>12,.2f}")
    print(f"  Est. Annual Tax:    ${calc['total_annual_tax']:>12,.2f}")
    print(f"  Quarterly Payment:  ${calc['quarterly_payment']:>12,.2f}")
    print(f"  Effective Rate:     {calc['effective_rate']:>12.1f}%")
    print()

    # Deductible vs non-deductible
    if q_expenses:
        categorized = categorize_all(q_expenses)
        deductible = sum(data["total"] for data in categorized.values())
        non_deductible = q_exp_total - deductible
        print_section("DEDUCTIBILITY SUMMARY")
        print(f"  Fully Deductible:   ${deductible:>12,.2f}")
        if non_deductible > 0:
            print(f"  Non-Deductible:     ${non_deductible:>12,.2f}")
        print(f"  Total Expenses:     ${q_exp_total:>12,.2f}")
        print()

    # Monthly breakdown
    print_section("MONTHLY BREAKDOWN")
    print(f"  {'MONTH':<12} {'REVENUE':>10} {'EXPENSES':>10} {'NET':>10}")
    for m in range(q_start_month, q_end_month + 1):
        m_rev = sum(r["revenue"] for r in q_revenue if r["date"].month == m)
        m_exp_r = sum(r["expenses"] for r in q_revenue if r["date"].month == m)
        m_exp_e = sum(e["amount"] for e in q_expenses if e["date"].month == m)
        m_total_exp = m_exp_r + m_exp_e
        m_net = m_rev - m_total_exp
        print(f"  {month_names[m]} {current_year:<8} ${m_rev:>9,.2f} ${m_total_exp:>9,.2f} ${m_net:>9,.2f}")
    print()

    # Filing reminders
    due_date = {
        "Q1": "April 15",
        "Q2": "June 15",
        "Q3": "September 15",
        "Q4": "January 15 (next year)",
    }[quarter]

    print_section("FILING REMINDERS")
    print(f"  Estimated Payment Due: {due_date}")
    print(f"  Payment Method: IRS Direct Pay (irs.gov/directpay)")
    print(f"  Form: 1040-ES")
    print(f"  Keep all receipts for 7 years minimum")
    print()

    # YTD context
    ytd_rev = sum(r["revenue"] for r in revenue_rows if r["date"].year == current_year)
    ytd_exp_r = sum(r["expenses"] for r in revenue_rows if r["date"].year == current_year)
    ytd_exp_e = sum(e["amount"] for e in expenses if e["date"].year == current_year)
    ytd_net = ytd_rev - ytd_exp_r - ytd_exp_e

    print_section("YEAR-TO-DATE CONTEXT")
    print(f"  YTD Revenue:    ${ytd_rev:>12,.2f}")
    print(f"  YTD Expenses:   ${ytd_exp_r + ytd_exp_e:>12,.2f}")
    print(f"  YTD Net Profit: ${ytd_net:>12,.2f}")

    print()
    print(hr())
    print(f"  Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  DISCLAIMER: This is an estimate. Consult a CPA for actual filing.")
    print(hr())


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Tax Optimizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 AUTOMATIONS/tax_optimizer.py --categorize
  python3 AUTOMATIONS/tax_optimizer.py --deductions
  python3 AUTOMATIONS/tax_optimizer.py --quarterly-estimate
  python3 AUTOMATIONS/tax_optimizer.py --report Q1
        """,
    )
    parser.add_argument("--categorize", action="store_true",
                        help="Categorize expenses for Schedule C")
    parser.add_argument("--deductions", action="store_true",
                        help="Identify missing deductions")
    parser.add_argument("--quarterly-estimate", action="store_true",
                        help="Calculate quarterly estimated tax payment")
    parser.add_argument("--report", metavar="Q1|Q2|Q3|Q4",
                        help="Generate quarterly tax report")

    args = parser.parse_args()

    if args.categorize:
        cmd_categorize()
    elif args.deductions:
        cmd_deductions()
    elif args.quarterly_estimate:
        cmd_quarterly_estimate()
    elif args.report:
        cmd_report(args.report)
    else:
        # Default: show all
        cmd_deductions()


if __name__ == "__main__":
    main()
