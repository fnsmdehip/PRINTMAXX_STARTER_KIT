# FINANCIALS - Capital Genesis Tracking System

Track every dollar in, every dollar out, every dollar invested. The LEDGER is the source of truth.

---

## File index

| File | Purpose | Update frequency |
|------|---------|-----------------|
| `REVENUE_TRACKER.csv` | Every revenue transaction across all methods | Per transaction (daily) |
| `EXPENSE_TRACKER.csv` | Every expense and subscription | Per transaction (daily) |
| `P_AND_L_MONTHLY.csv` | Monthly profit/loss summary | Monthly (1st of month) |
| `INVESTMENT_PORTFOLIO.csv` | All capital genesis investments | Per trade + monthly valuation |
| `TAX_DEDUCTIONS_2026.csv` | Deductible expenses for tax filing | Per transaction (daily) |
| `FINANCIAL_DASHBOARD.md` | Human-readable summary of everything | Weekly |

### Existing planning docs

| Directory | Contents |
|-----------|----------|
| `budgets/` | Tool, marketing, contractor, emergency fund budgets |
| `metrics/` | KPI dashboard, benchmarks, warning signs |
| `projections/` | Month 1-3, 4-6, 7-12, Year 2 financial projections |
| `unit_economics/` | Per-method unit economics (affiliate, agency, content, info products, SaaS) |

---

## How to use each file

### REVENUE_TRACKER.csv

Log every dollar earned. Include platform fees so you know actual net.

**Fields:**
- `date` - Transaction date (YYYY-MM-DD)
- `method_id` - From MONEY_METHODS_TRACKER.csv (MM001, CF001, AI001, etc.)
- `method_name` - Human readable (APP_FACTORY, CONTENT_FARM, etc.)
- `source_platform` - Where the money came from (app_store_ios, gumroad, youtube, etc.)
- `transaction_type` - subscription, one_time, commission, ad_revenue, sponsorship, tip
- `amount` - Gross amount before fees
- `fees` - Platform fees (Apple 30%, Gumroad 10%, etc.)
- `net_amount` - What actually hits your account
- `recurring` - TRUE/FALSE for subscription revenue
- `product_name` - Specific product or service sold

**Platform fee reference:**
| Platform | Fee |
|----------|-----|
| App Store (iOS) | 30% (15% under Small Business Program if <$1M) |
| Google Play | 30% (15% for first $1M) |
| Gumroad | 10% |
| Stripe | 2.9% + $0.30 |
| YouTube AdSense | ~45% (Google keeps 45%) |
| TikTok Creator Fund | Varies (low CPM) |
| Amazon Associates | 1-10% depending on category |

### EXPENSE_TRACKER.csv

Log every business expense. Mark tax deductible items. Save receipts.

**Fields:**
- `category` - ai_tools, domain_hosting, developer_accounts, advertising, equipment, contractor_payments, education, software, travel, phone_internet, home_office
- `recurring` - TRUE/FALSE
- `frequency` - monthly, yearly, one_time, quarterly
- `method_id` - Which money method this supports (ALL if shared)
- `tax_deductible` - TRUE/FALSE

**Current monthly recurring expenses:**

| Vendor | Amount | Category |
|--------|--------|----------|
| Anthropic (Claude Max) | $100.00 | ai_tools |
| Leonardo.ai | $12.00 | ai_tools |
| ElevenLabs | $5.00 | ai_tools |
| D-ID | $5.90 | ai_tools |
| **Monthly total** | **$122.90** | |

**Annual expenses (amortized):**

| Vendor | Amount | Monthly equiv |
|--------|--------|---------------|
| Apple Developer | $99.00 | $8.25 |
| Domain registration | $12.00 | $1.00 |
| Google Play (one-time) | $25.00 | $2.08 (first year) |

### P_AND_L_MONTHLY.csv

Summarize at month end. Pull totals from REVENUE_TRACKER and EXPENSE_TRACKER.

**Fields:**
- `revenue_by_method` - Pipe-separated (MM001:500|MM006:200|MM009:100)
- `margin_pct` - (gross_profit / total_revenue) * 100
- `runway_months` - Cash on hand / monthly burn
- `reinvestment_amount` - What goes back into the business
- `investment_amount` - What goes into capital genesis investments

### INVESTMENT_PORTFOLIO.csv

Track the capital genesis strategy. Every investment from business profits.

**Asset classes:**
- `INDEX_FUND` - VOO, VTI, VXUS (long-term compounding)
- `INDIVIDUAL_STOCK` - Individual picks with thesis
- `CRYPTO` - BTC, ETH, SOL (max 10% of portfolio)
- `REIT` - Real estate exposure (VNQ, O)
- `COMMODITY` - Gold, silver (inflation hedge)
- `DOMAIN` - Brandable domains bought for resale
- `BUSINESS_ACQUISITION` - Buying profitable apps/sites
- `ANGEL_INVESTMENT` - Seed investments in startups
- `PRIVATE_EQUITY` - Any private deals

**Update current_value monthly. Calculate gain_loss_pct = ((current_value - total_value) / total_value) * 100**

### TAX_DEDUCTIONS_2026.csv

Track deductible expenses separately for tax time. Mirror of relevant EXPENSE_TRACKER entries but organized by IRS category.

**Deduction categories for solopreneurs:**

| Category | IRS Line | Notes |
|----------|----------|-------|
| home_office | Schedule C, Line 30 | Simplified: $5/sq ft, max 300 sq ft = $1,500 |
| software_subscriptions | Schedule C, Line 18 | All SaaS tools used for business |
| equipment | Schedule C, Line 13 | Computers, monitors, phones (Section 179) |
| domain_hosting | Schedule C, Line 18 | Domains, hosting, CDN |
| advertising | Schedule C, Line 8 | All ad spend |
| contractor_payments | Schedule C, Line 11 | 1099-NEC if $600+ to any contractor |
| education | Schedule C, Line 27a | Courses, books, conferences related to business |
| travel | Schedule C, Line 24a | Business travel (not commuting) |
| phone_internet | Schedule C, Line 25 | Business percentage of bills |

---

## Tax tips for solopreneurs

### Structure

1. **Start as sole proprietor** - No setup cost. File Schedule C with personal return.
2. **Get an EIN** - Free from IRS. Use instead of SSN on business forms.
3. **Open business bank account** - Separate personal and business. Makes tracking simple.
4. **Consider LLC at $50k+ revenue** - Asset protection. $50-500 depending on state.
5. **Consider S-Corp election at $40k+ profit** - Save on self-employment tax. Talk to CPA first.

### Quarterly estimated taxes

If you expect to owe $1,000+ in taxes, pay quarterly:
- Q1: April 15 (covers Jan-Mar)
- Q2: June 15 (covers Apr-May)
- Q3: September 15 (covers Jun-Aug)
- Q4: January 15 of next year (covers Sep-Dec)

**Safe harbor:** Pay 100% of prior year tax liability (110% if AGI > $150k) to avoid penalties.

### Self-employment tax

15.3% on net profit (12.4% Social Security + 2.9% Medicare). You can deduct half of SE tax.

### Key deductions to never miss

1. **Home office** - Simplified method: $5/sq ft, max $1,500
2. **Internet and phone** - Business use percentage
3. **Software subscriptions** - Every tool you pay for
4. **Equipment** - Section 179 lets you deduct full cost in year 1
5. **Health insurance premiums** - Self-employed health insurance deduction
6. **Retirement contributions** - SEP IRA (up to 25% of net earnings) or Solo 401(k)
7. **Mileage** - 67 cents/mile for 2026 (estimated, check IRS)
8. **Education** - Courses and books directly related to your business

### When to get a CPA

- **$0-$25k revenue:** Use TurboTax Self-Employed or FreeTaxUSA. Simple enough to DIY.
- **$25k-$50k revenue:** Consider a CPA for first year to set up correctly ($300-800).
- **$50k+ revenue:** Get a CPA. They will save you more than they cost. S-Corp election alone can save $5k+/year in SE tax.
- **Any time you're confused:** A one-hour CPA consultation ($150-300) beats a tax penalty.

---

## Workflow

### Daily

1. Revenue comes in? Add row to REVENUE_TRACKER.csv
2. Expense paid? Add row to EXPENSE_TRACKER.csv
3. Deductible expense? Also add to TAX_DEDUCTIONS_2026.csv

### Weekly

1. Update FINANCIAL_DASHBOARD.md with current numbers
2. Check subscription renewals coming up
3. Review any pending refunds or chargebacks

### Monthly (1st of each month)

1. Sum REVENUE_TRACKER.csv for prior month
2. Sum EXPENSE_TRACKER.csv for prior month
3. Calculate P&L and add row to P_AND_L_MONTHLY.csv
4. Update INVESTMENT_PORTFOLIO.csv current values
5. Review burn rate and runway
6. Adjust targets if needed

### Quarterly

1. Calculate estimated tax payment
2. Review all deductions in TAX_DEDUCTIONS_2026.csv
3. Audit subscriptions (cancel what you don't use)
4. Update financial projections in projections/

### Annually

1. Export all CSVs for tax filing
2. Reconcile against bank statements
3. File Schedule C (or hand to CPA)
4. Set new year targets
5. Create TAX_DEDUCTIONS_{NEXT_YEAR}.csv

---

## File relationships

```
REVENUE_TRACKER.csv ──────┐
                          ├──→ P_AND_L_MONTHLY.csv ──→ FINANCIAL_DASHBOARD.md
EXPENSE_TRACKER.csv ──────┘           │
         │                            │
         └──→ TAX_DEDUCTIONS_2026.csv │
                                      │
         INVESTMENT_PORTFOLIO.csv ────┘
```

Revenue and expenses feed into monthly P&L. P&L determines investment allocation. Deductible expenses tracked separately for tax time. Dashboard summarizes everything.

---

## Cross-reference with LEDGER

| FINANCIALS file | Related LEDGER file |
|-----------------|---------------------|
| REVENUE_TRACKER.csv | LEDGER/FUNNEL_METRICS.csv (conversion data) |
| REVENUE_TRACKER.csv | LEDGER/PRODUCTS.csv (product catalog) |
| EXPENSE_TRACKER.csv | LEDGER/MONEY_METHODS_TRACKER.csv (method costs) |
| P_AND_L_MONTHLY.csv | LEDGER/GTM_OPTIMIZATION_PRIORITIES.csv (ROI per method) |

**LEDGER is the operational source of truth. FINANCIALS is the money source of truth. Both must stay in sync.**
