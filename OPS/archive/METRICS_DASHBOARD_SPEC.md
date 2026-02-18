# PRINTMAXX Metrics Dashboard Specification

**Purpose:** Single source of truth for all business metrics across money methods.
**Primary Implementation:** Google Sheets (free, shareable, formula-driven)
**Update Frequency:** Daily for core metrics, weekly for aggregates

---

## Dashboard Architecture

```
MASTER_DASHBOARD (Sheet 1)
├── APP_FACTORY (Sheet 2)
├── CONTENT_FARM (Sheet 3)
├── LEAD_GEN (Sheet 4)
├── FINANCIALS (Sheet 5)
├── RAW_DATA (Sheet 6)
└── SETTINGS (Sheet 7)
```

---

## 1. Master Overview Dashboard

### Metrics

| Metric | Formula/Source | Update | Alert Threshold |
|--------|----------------|--------|-----------------|
| Total Revenue (MTD) | `=SUM(FINANCIALS!B:B)` | Daily | < $500 = yellow, < $100 = red |
| Total Revenue (YTD) | `=SUMIF(FINANCIALS!A:A,">="&DATE(YEAR(TODAY()),1,1),FINANCIALS!B:B)` | Daily | - |
| Total Followers | `=SUM(CONTENT_FARM!C:C)` | Weekly | - |
| Total Downloads | `=SUM(APP_FACTORY!D:D)` | Daily | - |
| Active Leads | `=COUNTIF(LEAD_GEN!E:E,"active")` | Daily | < 50 = yellow |
| MRR | `=APP_FACTORY!B2+CONTENT_FARM!B2` | Monthly | < $1000 = red |
| Runway (months) | `=FINANCIALS!B10/FINANCIALS!B11` | Monthly | < 3 = red |

### Card Layout (Top Row)

```
+-------------+-------------+-------------+-------------+
| Revenue MTD | MRR         | Downloads   | Followers   |
| $2,450      | $1,200      | 12,500      | 45,000      |
| +15%        | +8%         | +22%        | +12%        |
+-------------+-------------+-------------+-------------+
```

---

## 2. App Factory Dashboard

### Core Metrics

| Metric | Source | Formula | Frequency |
|--------|--------|---------|-----------|
| Total Downloads | App Store Connect | `=SUM(D3:D100)` | Daily |
| Downloads (7d) | Manual entry | `=SUMIF(A:A,">="&TODAY()-7,D:D)` | Daily |
| MRR | RevenueCat | `=SUM(E3:E100)` | Daily |
| ARR | Calculated | `=B2*12` | Monthly |
| Avg Rating | App Store | `=AVERAGE(F3:F100)` | Weekly |
| D1 Retention | Analytics | Manual entry | Weekly |
| D7 Retention | Analytics | Manual entry | Weekly |
| Paywall Conversion | RevenueCat | `=I2/H2` | Daily |
| Trial-to-Paid | RevenueCat | `=J2/I2` | Weekly |
| CAC | Ads spend / installs | `=L2/D2` | Weekly |
| LTV | RevenueCat | Manual or calculated | Monthly |
| LTV:CAC Ratio | Calculated | `=M2/N2` | Monthly |

### Per-App Tracking Table

| App Name | Status | Downloads | Revenue | Rating | D7 Retention | Paywall CVR |
|----------|--------|-----------|---------|--------|--------------|-------------|
| PrayerLock | Live | 5,200 | $890 | 4.7 | 32% | 8.5% |
| WalkToUnlock | Live | 3,100 | $450 | 4.5 | 28% | 6.2% |
| StudyLock | Dev | - | - | - | - | - |

### Alert Rules

```
=IF(F3<4.0, "RATING LOW", "")
=IF(J3<0.03, "PAYWALL CVR LOW", "")
=IF(H3<0.15, "D7 RETENTION LOW", "")
=IF(N3<3, "LTV:CAC UNHEALTHY", "")
```

---

## 3. Content Farm Dashboard

### Core Metrics

| Metric | Platforms | Formula | Frequency |
|--------|-----------|---------|-----------|
| Total Followers | All | `=SUM(C3:C50)` | Weekly |
| Followers (7d growth) | All | `=C2-OFFSET(C2,-7,0)` | Weekly |
| Total Views (MTD) | All | `=SUMIFS(D:D,A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))` | Daily |
| Engagement Rate | Calculated | `=(Likes+Comments+Shares)/Views` | Weekly |
| Revenue (MTD) | Creator funds + sponsorships | `=SUM(F3:F50)` | Monthly |
| CPM | Calculated | `=(Revenue/Views)*1000` | Monthly |

### Per-Platform Tracking

| Platform | Account | Followers | Views (7d) | Engagement | Revenue | Status |
|----------|---------|-----------|------------|------------|---------|--------|
| TikTok | @faithmaxx | 25,000 | 450,000 | 8.2% | $120 | Active |
| YouTube | FaithFocus | 12,000 | 85,000 | 4.5% | $340 | Active |
| Instagram | @prayerlock | 8,000 | 22,000 | 3.1% | $0 | Growing |
| X/Twitter | @printmaxxer | 2,500 | 15,000 | 2.8% | $0 | Active |

---

## 4. Lead Generation Dashboard

### Core Metrics

| Metric | Source | Formula | Frequency |
|--------|--------|---------|-----------|
| Total Leads | LEDGER/leads.csv | `=COUNTA(A:A)-1` | Daily |
| Leads (7d) | Filtered | `=COUNTIF(B:B,">="&TODAY()-7)` | Daily |
| Email List Size | Email provider | Manual | Weekly |
| Open Rate | Email provider | Manual | Per campaign |
| Click Rate | Email provider | Manual | Per campaign |
| Lead-to-Customer | Calculated | `=Customers/Leads` | Monthly |
| Cost per Lead | Ads/leads | `=AdSpend/Leads` | Weekly |

### Lead Source Breakdown

| Source | Leads | % of Total | CPL | LTV |
|--------|-------|------------|-----|-----|
| Organic Search | 380 | 35% | $0 | $45 |
| TikTok | 290 | 27% | $0.50 | $38 |
| Cold Email | 180 | 17% | $2.10 | $62 |
| Paid Ads | 120 | 11% | $8.50 | $55 |
| Referral | 110 | 10% | $0 | $78 |

---

## 5. Financial Dashboard

### Revenue by Method

| Method | Revenue MTD | Revenue YTD | % of Total | MoM Change |
|--------|-------------|-------------|------------|------------|
| App Factory | $1,340 | $12,500 | 45% | +12% |
| Content Farm | $890 | $8,200 | 30% | +8% |
| Affiliate | $420 | $3,800 | 14% | +15% |
| Services | $300 | $2,500 | 9% | -5% |
| Other | $50 | $500 | 2% | +2% |

### Expense Tracking

| Category | Amount MTD | Amount YTD | Budget | Variance |
|----------|------------|------------|--------|----------|
| Hosting/Infra | $120 | $1,200 | $150 | -$30 |
| Tools/SaaS | $85 | $850 | $100 | -$15 |
| Ads/Marketing | $200 | $1,800 | $300 | -$100 |
| Contractors | $0 | $500 | $200 | -$200 |
| App Store Fees | $135 | $1,250 | - | - |
| Payment Fees | $45 | $420 | - | - |
| Total Expenses | $585 | $6,020 | $750 | -$165 |

### Cash Flow

| Metric | Value |
|--------|-------|
| Starting Balance | $5,200 |
| + Revenue | $3,000 |
| - Expenses | $585 |
| - Taxes Reserved (25%) | $750 |
| = Ending Balance | $6,865 |
| Runway (months) | 11.7 |

---

## 6. Implementation Options

### Option A: Google Sheets (Recommended)

**Pros:**
- Free
- Shareable
- Formula-driven automation
- API integrations available

**Setup Time:** 2-3 hours

### Option B: Notion

**Pros:**
- Visual databases
- Relation linking
- Team collaboration

**Cons:**
- Limited formulas
- No real-time charts

**Setup Time:** 3-4 hours

### Option C: Airtable

**Pros:**
- Powerful relational databases
- Native automations
- API access

**Cons:**
- Row limits on free plan (1,000)

**Setup Time:** 2-3 hours

**Recommendation:** Start with Google Sheets. Migrate to custom dashboard when hitting $10k MRR.

---

## 7. Data Collection Workflow

### Daily (5 min)

1. Check RevenueCat dashboard, update APP_FACTORY revenue
2. Check App Store Connect, update downloads
3. Check email provider, update leads count

### Weekly (15 min)

1. Export platform analytics, update CONTENT_FARM
2. Review all platform followers
3. Calculate engagement rates
4. Review alert flags

### Monthly (30 min)

1. Full revenue reconciliation
2. Expense categorization
3. Update retention metrics
4. Calculate LTV/CAC
5. Update financial projections

---

## 8. Alert Configuration

### Critical Alerts (Immediate Action)

| Condition | Alert | Action |
|-----------|-------|--------|
| MRR drops >20% MoM | REVENUE CRASH | Investigate churn |
| Runway <3 months | CASH CRITICAL | Cut expenses |
| App rating <4.0 | RATING CRISIS | Address reviews |
| Paywall CVR <2% | PAYWALL BROKEN | A/B test |

### Warning Alerts (Review Within 48h)

| Condition | Alert | Action |
|-----------|-------|--------|
| Lead flow <10/week | LOW LEADS | Check funnels |
| Email open rate <20% | DELIVERABILITY | Warm up |
| D7 retention <15% | RETENTION LOW | Improve onboarding |
| Engagement <2% | LOW ENGAGEMENT | Test content |

---

## 9. LEDGER Files Integration

| LEDGER File | Dashboard Tab | Key Columns |
|-------------|---------------|-------------|
| leads.csv | LEAD_GEN | email, source, date, status |
| FUNNEL_METRICS.csv | MASTER | metric, value, date |
| APP_LAUNCH_TRACKER.csv | APP_FACTORY | app, downloads, revenue |
| MONEY_METHODS_TRACKER.csv | FINANCIALS | method, revenue, status |

---

## Quick Start

1. Copy Google Sheets template structure
2. Set up 5 tabs: MASTER, APP_FACTORY, CONTENT_FARM, LEAD_GEN, FINANCIALS
3. Add formulas for core metrics
4. Configure conditional formatting for alerts
5. Spend 5 min daily updating

The goal is clarity, not complexity. A simple dashboard you update beats a sophisticated one you ignore.

---

Last updated: 2026-01-23
