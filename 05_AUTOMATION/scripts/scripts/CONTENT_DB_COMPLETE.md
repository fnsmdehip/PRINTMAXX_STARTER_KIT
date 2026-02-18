# Content Database System - Complete

**Script:** `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/AUTOMATIONS/scripts/content_database.py`
**Database:** `/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LEDGER/content.db`
**Created:** 2026-01-24

---

## Features Implemented

| Feature | Status | Description |
|---------|--------|-------------|
| `create_db()` | Done | Initializes SQLite database with content table and indexes |
| `add_content()` | Done | Adds content with source, platform, text, media, metrics |
| `get_pending()` | Done | Returns all content not yet posted |
| `mark_posted()` | Done | Marks content as posted with account name |
| `get_by_source()` | Done | Filters content by source (partial match) |
| `search()` | Done | Full text search on content text |
| `export_csv()` | Done | Exports all content to CSV |
| `import_csv()` | Done | Imports content from CSV |
| `dedupe()` | Done | Removes duplicate content by text |
| `stats()` | Done | Shows counts by source, platform, account |

---

## Database Schema

```sql
CREATE TABLE content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    platform TEXT NOT NULL,
    text TEXT NOT NULL,
    media_url TEXT,
    likes INTEGER DEFAULT 0,
    rts INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    scraped_at TEXT NOT NULL,
    posted_at TEXT,
    account_used TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)

-- Indexes
CREATE INDEX idx_source ON content(source)
CREATE INDEX idx_scraped_at ON content(scraped_at)
CREATE INDEX idx_platform ON content(platform)
CREATE INDEX idx_posted_at ON content(posted_at)
```

---

## CLI Usage

```bash
# Initialize database
python content_database.py init

# Add content
python content_database.py add "@levelsio" "twitter" "shipped 12 products"
python content_database.py add "@source" "platform" "text" --media "url" --likes 500 --rts 50 --views 10000

# View pending content
python content_database.py pending
python content_database.py pending -v  # verbose
python content_database.py pending -n 10  # limit to 10

# Mark as posted
python content_database.py posted 123 "account_name"

# Search
python content_database.py search "cold email"

# Filter by source
python content_database.py source "@levelsio"

# Get by ID
python content_database.py get 123

# Delete
python content_database.py delete 123

# Statistics
python content_database.py stats

# Export/Import
python content_database.py export backup.csv
python content_database.py import data.csv

# Remove duplicates
python content_database.py dedupe
```

---

## Python API Usage

```python
from content_database import (
    create_db,
    add_content,
    get_pending,
    mark_posted,
    get_by_source,
    search,
    export_csv,
    import_csv,
    dedupe,
    stats
)

# Add content
content_id = add_content(
    source="@levelsio",
    platform="twitter",
    text="shipped 12 products this year",
    media_url="https://example.com/image.jpg",
    metrics={"likes": 4500, "rts": 320, "views": 180000}
)

# Get pending content
pending = get_pending()
for item in pending:
    print(f"{item['id']}: {item['text'][:50]}")

# Mark as posted
mark_posted(content_id, "niche_account_1")

# Search
results = search("automation")

# Stats
s = stats()
print(f"Total: {s['total']}, Pending: {s['pending']}, Posted: {s['posted']}")
```

---

## Tests Passed

- [x] Database initialization
- [x] Add content with all fields
- [x] Add content with partial fields
- [x] Get pending content
- [x] Mark content as posted
- [x] Search functionality
- [x] Filter by source
- [x] Export to CSV
- [x] Dedupe removes duplicates
- [x] Stats calculation
- [x] CLI help output
- [x] Get by ID
- [x] Verbose output mode

---

## Integration Points

Use with other PRINTMAXX scripts:

```python
# In daily_alpha_scanner.py
from content_database import add_content
add_content("@source", "twitter", tweet_text, metrics={"likes": likes})

# In queue_processor.py
from content_database import get_pending, mark_posted
for item in get_pending():
    if post_to_platform(item):
        mark_posted(item["id"], account_name)

# In daily_report_generator.py
from content_database import stats
s = stats()
report.add(f"Content posted today: {s['posted']}")
```

---

## No External Dependencies

Uses only Python standard library:
- sqlite3
- csv
- argparse
- datetime
- pathlib
- typing
