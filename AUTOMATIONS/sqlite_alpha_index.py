#!/usr/bin/env python3
"""
SQLite FTS5 Alpha Index — Sub-second full-text search across 15K+ alpha entries.

Reads ALPHA_STAGING.csv, builds a SQLite FTS5 index at LEDGER/alpha_index.db,
and provides CLI search with ranked results, filters, and JSON output.

Usage:
    python3 AUTOMATIONS/sqlite_alpha_index.py --rebuild --stats
    python3 AUTOMATIONS/sqlite_alpha_index.py --search "cold email framework"
    python3 AUTOMATIONS/sqlite_alpha_index.py --search "pricing" --category MONETIZATION --top 10
    python3 AUTOMATIONS/sqlite_alpha_index.py --venture CONTENT --status APPROVED --json
    python3 AUTOMATIONS/sqlite_alpha_index.py --stats

Stdlib only. No external dependencies.
"""

import argparse
import csv
csv.field_size_limit(10 * 1024 * 1024)
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
DB_PATH = PROJECT_ROOT / "LEDGER" / "alpha_index.db"

# All columns in ALPHA_STAGING.csv (order matters for CSV reader)
ALL_COLUMNS = [
    "alpha_id", "source", "source_url", "category", "tactic",
    "roi_potential", "priority", "status", "applicable_methods",
    "applicable_niches", "synergy_score", "cross_sell_products",
    "implementation_priority", "engagement_authenticity", "earnings_verified",
    "extracted_method", "compliance_notes", "reviewer_notes",
    "created_at", "ops_generated", "quality_issues", "date_added",
]

# Columns indexed for full-text search
FTS_COLUMNS = [
    "tactic", "category", "extracted_method", "reviewer_notes",
    "applicable_methods", "applicable_niches",
]


def safe_path(target) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


# Validate both paths at import time
safe_path(CSV_PATH)
safe_path(DB_PATH)


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def _connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Open a connection with WAL mode for concurrent reads."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.row_factory = sqlite3.Row
    return conn


def _csv_meta() -> dict:
    """Return row count and mtime for the CSV file."""
    p = safe_path(CSV_PATH)
    if not p.exists():
        return {"row_count": 0, "mtime": 0.0}
    mtime = p.stat().st_mtime
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        count = sum(1 for _ in reader)
    return {"row_count": count, "mtime": mtime}


def _stored_meta(conn: sqlite3.Connection) -> dict:
    """Return metadata stored in the DB (or defaults)."""
    try:
        row = conn.execute(
            "SELECT row_count, csv_mtime, build_time FROM index_meta ORDER BY rowid DESC LIMIT 1"
        ).fetchone()
        if row:
            return {
                "row_count": row["row_count"],
                "mtime": row["csv_mtime"],
                "build_time": row["build_time"],
            }
    except sqlite3.OperationalError:
        pass
    return {"row_count": 0, "mtime": 0.0, "build_time": ""}


def _needs_rebuild(conn: sqlite3.Connection) -> bool:
    """True if CSV is newer or row count changed vs stored metadata."""
    csv_m = _csv_meta()
    db_m = _stored_meta(conn)
    if csv_m["row_count"] != db_m["row_count"]:
        return True
    if csv_m["mtime"] > db_m.get("mtime", 0):
        return True
    return False


# ---------------------------------------------------------------------------
# Build / rebuild
# ---------------------------------------------------------------------------

def build_index(force: bool = False) -> dict:
    """Read ALPHA_STAGING.csv and (re)build the SQLite FTS5 index.

    Returns a dict with build stats.
    """
    csv_path = safe_path(CSV_PATH)
    db_path = safe_path(DB_PATH)

    if not csv_path.exists():
        return {"error": f"CSV not found: {csv_path}"}

    conn = _connect(db_path)

    if not force and not _needs_rebuild(conn):
        meta = _stored_meta(conn)
        conn.close()
        return {
            "status": "up_to_date",
            "row_count": meta["row_count"],
            "build_time": meta["build_time"],
        }

    t0 = time.time()

    # Drop existing tables for clean rebuild
    conn.execute("DROP TABLE IF EXISTS alpha_fts")
    conn.execute("DROP TABLE IF EXISTS alpha")
    conn.execute("DROP TABLE IF EXISTS index_meta")

    # Regular table with all columns
    col_defs = ", ".join(f'"{c}" TEXT' for c in ALL_COLUMNS)
    conn.execute(f'CREATE TABLE alpha (rowid INTEGER PRIMARY KEY AUTOINCREMENT, {col_defs})')

    # Indexes for common filter columns
    conn.execute('CREATE INDEX idx_alpha_category ON alpha(category)')
    conn.execute('CREATE INDEX idx_alpha_status ON alpha(status)')
    conn.execute('CREATE INDEX idx_alpha_roi ON alpha(roi_potential)')
    conn.execute('CREATE INDEX idx_alpha_id ON alpha(alpha_id)')

    # FTS5 virtual table (content synced with alpha table)
    fts_cols = ", ".join(FTS_COLUMNS)
    conn.execute(
        f"CREATE VIRTUAL TABLE alpha_fts USING fts5({fts_cols}, content='alpha', content_rowid='rowid')"
    )

    # Metadata table
    conn.execute(
        "CREATE TABLE index_meta (row_count INTEGER, csv_mtime REAL, build_time TEXT, elapsed_s REAL)"
    )

    # Read CSV
    rows_inserted = 0
    placeholders = ", ".join(["?"] * len(ALL_COLUMNS))
    col_names = ", ".join(f'"{c}"' for c in ALL_COLUMNS)
    insert_sql = f"INSERT INTO alpha ({col_names}) VALUES ({placeholders})"

    fts_placeholders = ", ".join(["?"] * len(FTS_COLUMNS))
    fts_insert_sql = f"INSERT INTO alpha_fts(rowid, {fts_cols}) VALUES (?, {fts_placeholders})"

    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        batch_alpha = []
        batch_fts = []
        rowid = 0

        for raw_row in reader:
            # Build a values tuple aligned to ALL_COLUMNS
            values = []
            for col in ALL_COLUMNS:
                val = raw_row.get(col, "")
                if val is None:
                    val = ""
                values.append(str(val).strip())

            rowid += 1
            batch_alpha.append(tuple(values))

            # FTS values
            fts_values = [rowid]
            for col in FTS_COLUMNS:
                val = raw_row.get(col, "")
                if val is None:
                    val = ""
                fts_values.append(str(val).strip())
            batch_fts.append(tuple(fts_values))
            rows_inserted += 1

            # Batch insert every 1000 rows
            if len(batch_alpha) >= 1000:
                conn.executemany(insert_sql, batch_alpha)
                conn.executemany(fts_insert_sql, batch_fts)
                batch_alpha.clear()
                batch_fts.clear()

        # Insert remaining rows
        if batch_alpha:
            conn.executemany(insert_sql, batch_alpha)
            conn.executemany(fts_insert_sql, batch_fts)

    elapsed = time.time() - t0
    build_time = time.strftime("%Y-%m-%d %H:%M:%S")
    csv_m = _csv_meta()

    conn.execute(
        "INSERT INTO index_meta (row_count, csv_mtime, build_time, elapsed_s) VALUES (?, ?, ?, ?)",
        (rows_inserted, csv_m["mtime"], build_time, round(elapsed, 3)),
    )
    conn.commit()
    conn.close()

    return {
        "status": "rebuilt",
        "row_count": rows_inserted,
        "build_time": build_time,
        "elapsed_s": round(elapsed, 3),
    }


# ---------------------------------------------------------------------------
# Search / query
# ---------------------------------------------------------------------------

def _ensure_index() -> sqlite3.Connection:
    """Return a connection, auto-rebuilding if CSV is newer than DB."""
    db_path = safe_path(DB_PATH)
    if not db_path.exists():
        result = build_index(force=True)
        if "error" in result:
            print(f"ERROR: {result['error']}", file=sys.stderr)
            sys.exit(1)
    conn = _connect(db_path)
    if _needs_rebuild(conn):
        conn.close()
        build_index(force=True)
        conn = _connect(db_path)
    return conn


def search(
    query: str = "",
    venture: str = "",
    category: str = "",
    status: str = "",
    roi: str = "",
    top: int = 20,
    as_json: bool = False,
) -> list:
    """Search the alpha index. Returns list of dicts."""
    conn = _ensure_index()

    if query:
        # FTS5 search — get matching rowids ranked by relevance
        # Sanitize query for FTS5: escape double quotes, wrap terms
        safe_q = query.replace('"', '""')
        # Split into terms and join with AND for better matching
        terms = safe_q.split()
        if len(terms) > 1:
            fts_query = " AND ".join(f'"{t}"' for t in terms)
        else:
            fts_query = f'"{safe_q}"'

        # Try exact match first, fall back to OR match, then prefix match
        try:
            fts_sql = (
                "SELECT rowid, rank FROM alpha_fts WHERE alpha_fts MATCH ? ORDER BY rank LIMIT ?"
            )
            fts_rows = conn.execute(fts_sql, (fts_query, top * 5)).fetchall()
        except sqlite3.OperationalError:
            fts_rows = []

        # If AND match returns nothing, try OR match
        if not fts_rows and len(terms) > 1:
            fts_query_or = " OR ".join(f'"{t}"' for t in terms)
            try:
                fts_rows = conn.execute(fts_sql, (fts_query_or, top * 5)).fetchall()
            except sqlite3.OperationalError:
                fts_rows = []

        # If still nothing, try prefix match
        if not fts_rows:
            fts_query_prefix = " OR ".join(f'{t}*' for t in terms)
            try:
                fts_rows = conn.execute(fts_sql, (fts_query_prefix, top * 5)).fetchall()
            except sqlite3.OperationalError:
                fts_rows = []

        if not fts_rows:
            conn.close()
            return []

        rowids = [r["rowid"] for r in fts_rows]
        rank_map = {r["rowid"]: r["rank"] for r in fts_rows}

        # Fetch full rows from alpha table
        placeholders = ",".join(["?"] * len(rowids))
        sql = f"SELECT rowid, * FROM alpha WHERE rowid IN ({placeholders})"
        rows = conn.execute(sql, rowids).fetchall()
    else:
        # No FTS query — filter-only mode
        sql = "SELECT rowid, * FROM alpha WHERE 1=1"
        params = []
        rank_map = {}
        rows = None  # will be fetched below

    # Apply filters
    conditions = []
    params = []

    if venture:
        conditions.append('("applicable_methods" LIKE ? OR "category" LIKE ?)')
        params.extend([f"%{venture.upper()}%", f"%{venture.upper()}%"])

    if category:
        conditions.append('"category" = ?')
        params.append(category.upper())

    if status:
        conditions.append('"status" = ?')
        params.append(status.upper())

    if roi:
        conditions.append('"roi_potential" = ?')
        params.append(roi.upper())

    if query:
        # Filter already-fetched FTS rows
        results = []
        for row in rows:
            row_dict = dict(row)
            # Remove internal rowid from output
            rid = row_dict.pop("rowid", None)

            # Apply additional filters
            skip = False
            if venture:
                v = venture.upper()
                am = (row_dict.get("applicable_methods") or "").upper()
                cat = (row_dict.get("category") or "").upper()
                if v not in am and v not in cat:
                    skip = True
            if category and (row_dict.get("category") or "").upper() != category.upper():
                skip = True
            if status and (row_dict.get("status") or "").upper() != status.upper():
                skip = True
            if roi and (row_dict.get("roi_potential") or "").upper() != roi.upper():
                skip = True

            if not skip:
                row_dict["_rank"] = rank_map.get(rid, 0)
                results.append(row_dict)

        # Sort by FTS rank (lower = better match)
        results.sort(key=lambda x: x.get("_rank", 0))
        results = results[:top]
    else:
        # Pure filter query
        where = " AND ".join(conditions) if conditions else "1=1"
        sql = f"SELECT * FROM alpha WHERE {where} ORDER BY rowid DESC LIMIT ?"
        params.append(top)
        rows = conn.execute(sql, params).fetchall()
        results = [dict(r) for r in rows]

    conn.close()
    return results


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

def get_stats() -> dict:
    """Return index health stats."""
    db_path = safe_path(DB_PATH)
    if not db_path.exists():
        return {"error": "No index built yet. Run with --rebuild first."}

    conn = _connect(db_path)
    meta = _stored_meta(conn)

    stats = {
        "index_db": str(db_path),
        "csv_source": str(CSV_PATH),
        "total_rows": meta.get("row_count", 0),
        "last_build": meta.get("build_time", "never"),
        "db_size_mb": round(db_path.stat().st_size / (1024 * 1024), 2),
    }

    # Category breakdown
    try:
        rows = conn.execute(
            'SELECT category, COUNT(*) as cnt FROM alpha GROUP BY category ORDER BY cnt DESC'
        ).fetchall()
        stats["categories"] = {r["category"]: r["cnt"] for r in rows}
    except sqlite3.OperationalError:
        stats["categories"] = {}

    # Status breakdown
    try:
        rows = conn.execute(
            'SELECT status, COUNT(*) as cnt FROM alpha GROUP BY status ORDER BY cnt DESC'
        ).fetchall()
        stats["statuses"] = {r["status"]: r["cnt"] for r in rows}
    except sqlite3.OperationalError:
        stats["statuses"] = {}

    # ROI breakdown
    try:
        rows = conn.execute(
            'SELECT roi_potential, COUNT(*) as cnt FROM alpha GROUP BY roi_potential ORDER BY cnt DESC'
        ).fetchall()
        stats["roi_breakdown"] = {r["roi_potential"]: r["cnt"] for r in rows}
    except sqlite3.OperationalError:
        stats["roi_breakdown"] = {}

    # Needs rebuild?
    stats["needs_rebuild"] = _needs_rebuild(conn)

    conn.close()
    return stats


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def _truncate(s: str, length: int = 80) -> str:
    """Truncate string to length, adding ellipsis if needed."""
    if not s:
        return ""
    s = s.replace("\n", " ").strip()
    if len(s) <= length:
        return s
    return s[: length - 3] + "..."


def print_results(results: list, as_json: bool = False):
    """Print search results as table or JSON."""
    if as_json:
        # Remove internal _rank from JSON output
        clean = []
        for r in results:
            row = {k: v for k, v in r.items() if not k.startswith("_")}
            clean.append(row)
        print(json.dumps(clean, indent=2))
        return

    if not results:
        print("No results found.")
        return

    # Table header
    print(f"\n{'='*120}")
    print(f"  {'ALPHA_ID':<25} {'CATEGORY':<20} {'ROI':<10} {'STATUS':<18} {'TACTIC/METHOD'}")
    print(f"{'='*120}")

    for r in results:
        alpha_id = _truncate(r.get("alpha_id", ""), 24)
        category = _truncate(r.get("category", ""), 19)
        roi = _truncate(r.get("roi_potential", ""), 9)
        status = _truncate(r.get("status", ""), 17)
        # Show tactic first, fall back to extracted_method, then reviewer_notes
        detail = r.get("tactic", "") or r.get("extracted_method", "") or r.get("reviewer_notes", "")
        detail = _truncate(detail, 60)
        print(f"  {alpha_id:<25} {category:<20} {roi:<10} {status:<18} {detail}")

    print(f"{'='*120}")
    print(f"  {len(results)} result(s)\n")


def print_stats(stats: dict, as_json: bool = False):
    """Print stats as table or JSON."""
    if as_json:
        print(json.dumps(stats, indent=2))
        return

    if "error" in stats:
        print(f"ERROR: {stats['error']}")
        return

    print(f"\n{'='*60}")
    print(f"  ALPHA INDEX HEALTH")
    print(f"{'='*60}")
    print(f"  Total rows indexed:  {stats['total_rows']:,}")
    print(f"  Last build:          {stats['last_build']}")
    print(f"  DB size:             {stats['db_size_mb']} MB")
    print(f"  Needs rebuild:       {'YES' if stats['needs_rebuild'] else 'no'}")
    print(f"  DB path:             {stats['index_db']}")
    print(f"  CSV source:          {stats['csv_source']}")

    if stats.get("categories"):
        print(f"\n  {'CATEGORY':<30} {'COUNT':>8}")
        print(f"  {'-'*40}")
        for cat, cnt in stats["categories"].items():
            label = cat if cat else "(empty)"
            print(f"  {label:<30} {cnt:>8}")

    if stats.get("statuses"):
        print(f"\n  {'STATUS':<30} {'COUNT':>8}")
        print(f"  {'-'*40}")
        for st, cnt in stats["statuses"].items():
            label = st if st else "(empty)"
            print(f"  {label:<30} {cnt:>8}")

    if stats.get("roi_breakdown"):
        print(f"\n  {'ROI POTENTIAL':<30} {'COUNT':>8}")
        print(f"  {'-'*40}")
        for roi, cnt in stats["roi_breakdown"].items():
            label = roi if roi else "(empty)"
            print(f"  {label:<30} {cnt:>8}")

    print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="SQLite FTS5 Alpha Index — sub-second search across 15K+ alpha entries"
    )
    parser.add_argument("--search", "-s", type=str, default="", help="Full-text search query")
    parser.add_argument("--venture", "-v", type=str, default="", help="Filter by venture/applicable_methods (e.g. OUTBOUND, CONTENT)")
    parser.add_argument("--category", "-c", type=str, default="", help="Exact category filter (e.g. MONETIZATION)")
    parser.add_argument("--status", type=str, default="", help="Status filter (e.g. APPROVED, PENDING_REVIEW)")
    parser.add_argument("--roi", type=str, default="", help="ROI potential filter (e.g. HIGH, HIGHEST)")
    parser.add_argument("--top", "-t", type=int, default=20, help="Max results (default 20)")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output for agent consumption")
    parser.add_argument("--rebuild", action="store_true", help="Force full index rebuild")
    parser.add_argument("--stats", action="store_true", help="Show index health stats")

    args = parser.parse_args()

    # Rebuild if requested
    if args.rebuild:
        print("Rebuilding alpha index...", file=sys.stderr)
        result = build_index(force=True)
        if "error" in result:
            print(f"ERROR: {result['error']}", file=sys.stderr)
            sys.exit(1)
        print(
            f"Index built: {result['row_count']:,} rows in {result.get('elapsed_s', '?')}s",
            file=sys.stderr,
        )

    # Stats
    if args.stats:
        stats = get_stats()
        print_stats(stats, as_json=args.json)
        if not args.search and not args.venture and not args.category:
            return

    # Search / filter
    if args.search or args.venture or args.category or args.status or args.roi:
        t0 = time.time()
        results = search(
            query=args.search,
            venture=args.venture,
            category=args.category,
            status=args.status,
            roi=args.roi,
            top=args.top,
            as_json=args.json,
        )
        elapsed_ms = (time.time() - t0) * 1000
        print_results(results, as_json=args.json)
        if not args.json:
            print(f"  Search completed in {elapsed_ms:.1f}ms\n")
    elif not args.rebuild and not args.stats:
        parser.print_help()


if __name__ == "__main__":
    main()
