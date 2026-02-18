# Revenue Tracker Automation

Aggregates revenue from Gumroad, App Store Connect, and Google Play Console into FINANCIALS/REVENUE_TRACKER.csv. Generates daily summaries.

## Setup

```bash
# Gumroad (get token from Settings > Advanced > Application)
export GUMROAD_ACCESS_TOKEN="your_token"

# App Store Connect (create API key in App Store Connect > Users and Access)
export ASC_KEY_ID="your_key_id"
export ASC_ISSUER_ID="your_issuer_id"
export ASC_PRIVATE_KEY_PATH="/path/to/AuthKey.p8"

# Google Play Console (create service account)
export GOOGLE_PLAY_JSON_KEY="/path/to/service_account.json"
```

## Usage

```bash
# Pull from all configured sources
python3 track_revenue.py

# Pull from specific source
python3 track_revenue.py --source gumroad

# Import from CSV export (Gumroad, App Store, Google Play exports)
python3 track_revenue.py --import-csv gumroad_sales.csv --import-source gumroad

# Generate summary only (no API calls)
python3 track_revenue.py --summary

# Summary for last 30 days
python3 track_revenue.py --summary --days 30

# Only fetch sales after a date
python3 track_revenue.py --after 2026-01-01
```

## CSV Import

For platforms without API access yet, export CSVs from dashboards and import:

```bash
# Gumroad: Settings > Sales > Export
python3 track_revenue.py --import-csv gumroad_export.csv --import-source gumroad

# App Store: App Store Connect > Sales and Trends > Export
python3 track_revenue.py --import-csv appstore_export.csv --import-source app_store_ios

# Google Play: Play Console > Financial reports > Download
python3 track_revenue.py --import-csv play_export.csv --import-source google_play
```

## Output

- Updates `FINANCIALS/REVENUE_TRACKER.csv` with new entries
- Generates summary in `summaries/revenue_summary_YYYYMMDD.md`
- Deduplicates against existing entries (date + platform + product)

## Revenue Summary Example

```
Gross Revenue: $1,234.00
Platform Fees: $123.40
Net Revenue: $1,110.60
Transactions: 47

By Method:
- INFO_PRODUCTS: $800.00
- APP_FACTORY: $310.60

By Platform:
- gumroad: $800.00
- app_store_ios: $310.60
```

## Dependencies

None (stdlib only).
