# Alpha Extraction Processor

Processes raw Twitter bookmark/tweet JSON dumps into formatted ALPHA_STAGING.csv entries. Filters for business content, deduplicates, classifies by category, and estimates ROI potential.

## Usage

```bash
# Process a JSON dump of bookmarks
python3 extract_alpha.py bookmarks.json

# Append directly to ALPHA_STAGING.csv
python3 extract_alpha.py bookmarks.json --append

# Output as CSV file
python3 extract_alpha.py bookmarks.json --format csv

# Process folder of JSON files
python3 extract_alpha.py json_folder/ --batch

# Read from stdin (pipe from another tool)
cat bookmarks.json | python3 extract_alpha.py --stdin --append
```

## Input JSON Formats

Accepts multiple Twitter JSON structures:
- Standard Twitter API v1.1 format
- Twitter API v2 format
- Twitter archive/export format
- Array of tweet objects
- Wrapper objects with `data`, `tweets`, or `bookmarks` keys

## What It Does

1. Parses raw JSON into normalized tweet data
2. Filters for business content using 50+ keyword patterns
3. Deduplicates against existing ALPHA_STAGING.csv entries (by URL)
4. Classifies into categories: APP_FACTORY, CONTENT_FORMAT, OUTBOUND, GROWTH_HACK, TOOL_ALPHA, MONETIZATION, SEO_GEO_ASO, ECOM
5. Estimates ROI potential based on revenue numbers and specificity
6. Extracts actionable steps from structured content
7. Outputs ALPHA_STAGING.csv-compatible rows

## Categories

| Category | Detected By |
|----------|------------|
| APP_FACTORY | app, mobile, ios, android, react native, aso |
| CONTENT_FORMAT | content, tiktok, youtube, viral, hook |
| OUTBOUND | cold email, deliverability, warmup, linkedin |
| GROWTH_HACK | growth, automation, scraping, engagement |
| TOOL_ALPHA | tool, api, mcp, plugin, github, open source |
| MONETIZATION | revenue, mrr, pricing, paywall, subscription |
| SEO_GEO_ASO | seo, geo, aso, rank, keyword, backlink |
| ECOM | ecom, dropship, tiktok shop, amazon, etsy |

## Noise Filtering

Automatically skips:
- Giveaway posts
- "Drop your" engagement bait
- Retweet/follow contests
- Generic "DM me" spam

## Dependencies

None (stdlib only).
