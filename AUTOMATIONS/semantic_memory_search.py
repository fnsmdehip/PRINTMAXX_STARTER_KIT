#!/usr/bin/env python3
"""
PRINTMAXX Semantic Memory Search
==================================
Zero-dependency TF-IDF search across all system logs, learnings, signals,
orchestrator history, and operational data.

Usage:
  python3 semantic_memory_search.py "what methods are failing"
  python3 semantic_memory_search.py --query "lead pipeline performance" --top 10
  python3 semantic_memory_search.py --index               # Rebuild index
  python3 semantic_memory_search.py --stats               # Index statistics
  python3 semantic_memory_search.py --category learnings   # Search within category
  python3 semantic_memory_search.py --recent 7 "rebalancer" # Last 7 days only
  python3 semantic_memory_search.py --export results.json  # Export results as JSON

Categories: learnings, orchestrator, signals, pipeline, brain, prompts,
            alerts, scraper, rebalancer, tasks, cold_email, checkpoints
"""

import csv
import json
import math
import os
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
INDEX_DIR = BASE / "AUTOMATIONS" / "logs" / ".search_index"
INDEX_FILE = INDEX_DIR / "tfidf_index.json"
DOCS_FILE = INDEX_DIR / "documents.json"

# All searchable data sources
SOURCES = {
    "learnings": BASE / "LEDGER" / "RBI_STRATEGIC" / "LEARNINGS.jsonl",
    "orchestrator": BASE / "LEDGER" / "OPS_ORCHESTRATOR_LOG.jsonl",
    "signals": BASE / "LEDGER" / "SIGNAL_HISTORY.jsonl",
    "pipeline": BASE / "AUTOMATIONS" / "leads" / "qualified" / "pipeline_metrics.jsonl",
    "brain": BASE / "LEDGER" / "BRAIN_LOG.jsonl",
    "prompts": BASE / "LEDGER" / "PROMPT_LOG.jsonl",
    "alerts": BASE / "AUTOMATIONS" / "logs" / "alerts.jsonl",
    "scraper": BASE / "AUTOMATIONS" / "logs" / "scraper_daily.jsonl",
    "rebalancer": BASE / "AUTOMATIONS" / "logs" / "rebalance_history.jsonl",
    "tasks": BASE / "OPS" / "AUTONOMOUS_TASK_QUEUE.jsonl",
    "cold_email": BASE / "AUTOMATIONS" / "logs" / "cold_email_generator.jsonl",
}

# Additional markdown sources (high-signal operational docs)
MD_SOURCES = {
    "heartbeat": BASE / "OPS" / "HEARTBEAT.md",
    "active_tasks": BASE / "OPS" / "active-tasks.md",
    "overnight_log": BASE / "OPS" / "logs" / "OVERNIGHT_SESSION_LOG.md",
}

# Checkpoint files
CHECKPOINT_DIR = BASE / "OPS" / "checkpoints" / "pending"

# Stop words for TF-IDF (common English words that add noise)
STOP_WORDS = frozenset([
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "dare", "ought",
    "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "as", "into", "through", "during", "before", "after", "above", "below",
    "between", "out", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "each",
    "every", "both", "few", "more", "most", "other", "some", "such", "no",
    "nor", "not", "only", "own", "same", "so", "than", "too", "very",
    "just", "because", "but", "and", "or", "if", "while", "that", "this",
    "these", "those", "it", "its", "i", "me", "my", "we", "our", "you",
    "your", "he", "him", "his", "she", "her", "they", "them", "their",
    "what", "which", "who", "whom", "up", "about", "also", "any",
])


def tokenize(text):
    """Split text into lowercase tokens, strip punctuation."""
    text = text.lower()
    # Replace common separators with spaces
    text = re.sub(r'[_\-/\\.:,;!?\[\]{}()"\'`~#@&*+=<>|]', " ", text)
    tokens = text.split()
    return [t for t in tokens if len(t) > 1 and t not in STOP_WORDS]


def extract_text_from_json(obj):
    """Recursively extract all string values from a JSON object."""
    parts = []
    if isinstance(obj, str):
        parts.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            parts.extend(extract_text_from_json(v))
    elif isinstance(obj, list):
        for item in obj:
            parts.extend(extract_text_from_json(item))
    return parts


def load_jsonl_docs(filepath, category):
    """Load a JSONL file into searchable documents."""
    docs = []
    if not filepath.exists():
        return docs
    try:
        with open(filepath, "r") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Extract timestamp
                ts = obj.get("timestamp", obj.get("date", ""))

                # Extract all text content
                text_parts = extract_text_from_json(obj)
                full_text = " ".join(text_parts)

                # Build a readable snippet
                snippet = _build_snippet(obj, category)

                docs.append({
                    "id": f"{category}:{i}",
                    "category": category,
                    "source": str(filepath.relative_to(BASE)),
                    "timestamp": str(ts),
                    "text": full_text,
                    "snippet": snippet,
                    "raw": obj,
                })
    except Exception as e:
        print(f"  Warning: Error reading {filepath}: {e}", file=sys.stderr)
    return docs


def _build_snippet(obj, category):
    """Build a human-readable snippet from a JSON object."""
    if category == "learnings":
        learning = obj.get("learning", obj.get("finding", ""))
        outcome = obj.get("outcome", "")
        return f"{learning} {outcome}".strip()[:200]
    elif category == "orchestrator":
        event = obj.get("event", "")
        learning = obj.get("learning", "")
        return f"[{event}] {learning}".strip()[:200]
    elif category == "signals":
        top5 = obj.get("top_5", [])
        titles = [s.get("title", "")[:60] for s in top5[:3]]
        return f"Signals: {obj.get('total_signals', '?')} total. Top: {'; '.join(titles)}"[:200]
    elif category == "pipeline":
        step = obj.get("step", "")
        if step == "qualify":
            return (f"Pipeline qualify: batch={obj.get('batch_size')}, "
                    f"+{obj.get('new_hot', 0)} hot, +{obj.get('new_warm', 0)} warm, "
                    f"total_hot={obj.get('total_hot')}, total_warm={obj.get('total_warm')}")
        elif step == "email_gen":
            return (f"Pipeline email_gen: {obj.get('total_emails_generated', '?')} emails, "
                    f"{obj.get('email_files', '?')} files from {obj.get('hot_leads_input', '?')} hot leads")
        elif step == "pipeline_update":
            return (f"Pipeline update: +{obj.get('new_entries', 0)} entries, "
                    f"total={obj.get('total_pipeline', '?')}")
        else:
            analyzed = obj.get("analyzed", obj.get("total_analyzed", "?"))
            hot = obj.get("hot", obj.get("hot_count", "?"))
            return f"Pipeline [{step}]: {analyzed} analyzed, {hot} hot leads"
    elif category == "brain":
        decision = obj.get("decision", obj.get("event", ""))
        detail = obj.get("detail", obj.get("message", ""))
        return f"[Brain] {decision}: {detail}"[:200]
    elif category == "rebalancer":
        scores = obj.get("scores", {})
        if isinstance(scores, dict):
            total = obj.get("methods", len(scores))
            kills = obj.get("kills", 0)
            doubles = obj.get("doubles", 0)
            # Show a few method scores
            sample = list(scores.items())[:3]
            parts = [f"{m}={s}" for m, s in sample]
            return f"Rebalance: {total} methods, {kills} kills, {doubles} doubles. Sample: {', '.join(parts)}"
        methods = obj.get("methods", [])
        if isinstance(methods, list) and methods:
            top = methods[:3]
            parts = [f"{m.get('method','?')}={m.get('score','?')}" for m in top]
            return f"Rebalance: {len(methods)} methods. Top: {', '.join(parts)}"
        return json.dumps(obj)[:200]
    elif category == "tasks":
        task = obj.get("task", obj.get("description", ""))
        status = obj.get("status", "")
        return f"[{status}] {task}"[:200]
    else:
        # Generic: take first 200 chars of all values
        parts = extract_text_from_json(obj)
        return " ".join(parts)[:200]


def load_md_docs(filepath, category):
    """Load a markdown file as a single searchable document."""
    docs = []
    if not filepath.exists():
        return docs
    try:
        content = filepath.read_text(errors="replace")
        docs.append({
            "id": f"{category}:0",
            "category": category,
            "source": str(filepath.relative_to(BASE)),
            "timestamp": datetime.fromtimestamp(filepath.stat().st_mtime).isoformat(),
            "text": content,
            "snippet": content[:300].replace("\n", " "),
            "raw": {"content": content[:500]},
        })
    except Exception as e:
        print(f"  Warning: Error reading {filepath}: {e}", file=sys.stderr)
    return docs


def load_checkpoint_docs():
    """Load pending checkpoint files."""
    docs = []
    if not CHECKPOINT_DIR.exists():
        return docs
    for f in CHECKPOINT_DIR.glob("*.json"):
        try:
            obj = json.loads(f.read_text())
            text_parts = extract_text_from_json(obj)
            docs.append({
                "id": f"checkpoints:{f.stem}",
                "category": "checkpoints",
                "source": str(f.relative_to(BASE)),
                "timestamp": obj.get("timestamp", ""),
                "text": " ".join(text_parts),
                "snippet": f"Checkpoint: {obj.get('type', '?')} - {obj.get('description', f.stem)}"[:200],
                "raw": obj,
            })
        except Exception:
            pass
    return docs


def build_index():
    """Load all sources, build TF-IDF index, save to disk."""
    print("Building semantic memory index...")
    all_docs = []

    # JSONL sources
    for cat, path in SOURCES.items():
        docs = load_jsonl_docs(path, cat)
        print(f"  {cat}: {len(docs)} documents from {path.name}")
        all_docs.extend(docs)

    # Markdown sources
    for cat, path in MD_SOURCES.items():
        docs = load_md_docs(path, cat)
        if docs:
            print(f"  {cat}: 1 document from {path.name}")
        all_docs.extend(docs)

    # Checkpoints
    cp_docs = load_checkpoint_docs()
    if cp_docs:
        print(f"  checkpoints: {len(cp_docs)} pending")
    all_docs.extend(cp_docs)

    print(f"\nTotal: {len(all_docs)} documents")

    # Build TF-IDF
    print("Computing TF-IDF scores...")
    doc_count = len(all_docs)
    if doc_count == 0:
        print("No documents to index.")
        return [], {}

    # Tokenize all docs
    doc_tokens = []
    for doc in all_docs:
        tokens = tokenize(doc["text"])
        doc_tokens.append(tokens)

    # Document frequency (how many docs contain each term)
    df = Counter()
    for tokens in doc_tokens:
        unique = set(tokens)
        for t in unique:
            df[t] += 1

    # IDF = log(N / df)
    idf = {}
    for term, freq in df.items():
        idf[term] = math.log(doc_count / freq)

    # TF-IDF per document (stored as sparse dict)
    index = {}  # term -> [(doc_idx, tfidf_score), ...]
    for idx, tokens in enumerate(doc_tokens):
        tf = Counter(tokens)
        doc_len = len(tokens) if tokens else 1
        for term, count in tf.items():
            # Normalized TF * IDF
            tfidf = (count / doc_len) * idf.get(term, 0)
            if tfidf > 0:
                if term not in index:
                    index[term] = []
                index[term].append((idx, round(tfidf, 6)))

    # Save index
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    # Save documents (without full text to save space, keep snippet + metadata)
    saved_docs = []
    for doc in all_docs:
        saved_docs.append({
            "id": doc["id"],
            "category": doc["category"],
            "source": doc["source"],
            "timestamp": doc["timestamp"],
            "snippet": doc["snippet"],
        })

    with open(DOCS_FILE, "w") as f:
        json.dump(saved_docs, f)

    with open(INDEX_FILE, "w") as f:
        json.dump(index, f)

    vocab_size = len(index)
    print(f"Index built: {vocab_size} unique terms, {doc_count} documents")
    print(f"Saved to: {INDEX_DIR}/")

    return all_docs, index


def load_index():
    """Load saved index from disk."""
    if not INDEX_FILE.exists() or not DOCS_FILE.exists():
        return None, None
    with open(DOCS_FILE, "r") as f:
        docs = json.load(f)
    with open(INDEX_FILE, "r") as f:
        index = json.load(f)
    return docs, index


def search(query, docs=None, index=None, top_k=10, category=None,
           recent_days=None):
    """Search the index with a natural language query."""
    if docs is None or index is None:
        docs, index = load_index()
        if docs is None:
            print("No index found. Building now...")
            all_docs, index = build_index()
            docs, _ = load_index()
            if docs is None:
                print("Failed to build index.")
                return []

    query_tokens = tokenize(query)
    if not query_tokens:
        print("No searchable terms in query.")
        return []

    # Score each document
    scores = defaultdict(float)
    matched_terms = defaultdict(set)

    for token in query_tokens:
        if token in index:
            for doc_idx, tfidf in index[token]:
                scores[doc_idx] += tfidf
                matched_terms[doc_idx].add(token)

    # Filter by category
    if category:
        scores = {
            idx: s for idx, s in scores.items()
            if docs[idx]["category"] == category
        }

    # Filter by recency
    if recent_days:
        cutoff = (datetime.now() - timedelta(days=recent_days)).isoformat()
        scores = {
            idx: s for idx, s in scores.items()
            if docs[idx].get("timestamp", "") >= cutoff
        }

    # Boost score by number of matched query terms (breadth bonus)
    for idx in scores:
        term_coverage = len(matched_terms[idx]) / len(query_tokens)
        scores[idx] *= (1 + term_coverage)

    # Rank
    ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_k]

    results = []
    for idx, score in ranked:
        doc = docs[idx]
        results.append({
            "score": round(score, 4),
            "matched_terms": sorted(matched_terms[idx]),
            **doc,
        })

    return results


def cmd_search(query, top_k=10, category=None, recent_days=None,
               export_path=None):
    """Execute a search and display results."""
    results = search(query, top_k=top_k, category=category,
                     recent_days=recent_days)

    if not results:
        print(f"No results for: {query}")
        return

    cat_filter = f" [{category}]" if category else ""
    time_filter = f" [last {recent_days}d]" if recent_days else ""
    print(f"\nSearch: \"{query}\"{cat_filter}{time_filter}")
    print(f"Found: {len(results)} results")
    print("=" * 70)

    for i, r in enumerate(results, 1):
        ts = r.get("timestamp", "")[:19]
        cat = r["category"]
        score = r["score"]
        matched = ", ".join(r["matched_terms"])
        snippet = r["snippet"]

        print(f"\n{i}. [{cat}] score={score:.3f}  ({ts})")
        print(f"   Source: {r['source']}")
        print(f"   Match: {matched}")
        print(f"   {snippet}")

    print()

    if export_path:
        with open(export_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results exported to: {export_path}")


def cmd_stats():
    """Show index statistics."""
    docs, index = load_index()
    if docs is None:
        print("No index found. Run --index first.")
        return

    print("SEMANTIC MEMORY INDEX STATISTICS")
    print("=" * 50)
    print(f"Total documents: {len(docs)}")
    print(f"Vocabulary size: {len(index)}")
    print()

    # Category breakdown
    cat_counts = Counter(d["category"] for d in docs)
    print("Documents by category:")
    for cat, count in cat_counts.most_common():
        print(f"  {cat:<20} {count:>5}")

    # Index freshness
    if INDEX_FILE.exists():
        age = time.time() - INDEX_FILE.stat().st_mtime
        if age < 3600:
            freshness = f"{int(age)}s ago"
        elif age < 86400:
            freshness = f"{age / 3600:.1f}h ago"
        else:
            freshness = f"{age / 86400:.1f}d ago"
        print(f"\nIndex built: {freshness}")
        print(f"Index size: {INDEX_FILE.stat().st_size / 1024:.1f} KB")

    # Top terms by document frequency
    term_counts = {term: len(postings) for term, postings in index.items()}
    top_terms = sorted(term_counts.items(), key=lambda x: -x[1])[:20]
    print(f"\nTop 20 terms (by document frequency):")
    for term, count in top_terms:
        print(f"  {term:<25} appears in {count} docs")

    # Timestamp range
    timestamps = [d["timestamp"] for d in docs if d.get("timestamp")]
    if timestamps:
        timestamps_clean = [t for t in timestamps if len(t) > 10]
        if timestamps_clean:
            print(f"\nData range: {min(timestamps_clean)[:10]} to "
                  f"{max(timestamps_clean)[:10]}")


def cmd_live_search(query, top_k=10, category=None, recent_days=None):
    """Search directly from source files without building index.
    Slower but always fresh data."""
    all_docs = []
    for cat, path in SOURCES.items():
        all_docs.extend(load_jsonl_docs(path, cat))
    for cat, path in MD_SOURCES.items():
        all_docs.extend(load_md_docs(path, cat))
    all_docs.extend(load_checkpoint_docs())

    if not all_docs:
        print("No documents found.")
        return

    # Build temporary in-memory index
    doc_count = len(all_docs)
    doc_tokens_list = [tokenize(d["text"]) for d in all_docs]

    df = Counter()
    for tokens in doc_tokens_list:
        for t in set(tokens):
            df[t] += 1

    idf = {t: math.log(doc_count / freq) for t, freq in df.items()}

    temp_index = {}
    for idx, tokens in enumerate(doc_tokens_list):
        tf = Counter(tokens)
        doc_len = len(tokens) if tokens else 1
        for term, count in tf.items():
            tfidf = (count / doc_len) * idf.get(term, 0)
            if tfidf > 0:
                if term not in temp_index:
                    temp_index[term] = []
                temp_index[term].append((idx, round(tfidf, 6)))

    # Convert docs to saved format
    saved_docs = [{
        "id": d["id"], "category": d["category"], "source": d["source"],
        "timestamp": d["timestamp"], "snippet": d["snippet"],
    } for d in all_docs]

    results = search(query, docs=saved_docs, index=temp_index,
                     top_k=top_k, category=category,
                     recent_days=recent_days)

    if not results:
        print(f"No results for: {query}")
        return

    cat_filter = f" [{category}]" if category else ""
    time_filter = f" [last {recent_days}d]" if recent_days else ""
    print(f"\nLive Search: \"{query}\"{cat_filter}{time_filter}")
    print(f"Scanned: {len(all_docs)} documents")
    print(f"Found: {len(results)} results")
    print("=" * 70)

    for i, r in enumerate(results, 1):
        ts = r.get("timestamp", "")[:19]
        print(f"\n{i}. [{r['category']}] score={r['score']:.3f}  ({ts})")
        print(f"   Source: {r['source']}")
        print(f"   Match: {', '.join(r['matched_terms'])}")
        print(f"   {r['snippet']}")
    print()


def api_search(query, top_k=5, category=None, recent_days=None):
    """Programmatic API for other scripts to call.
    Returns list of result dicts."""
    return search(query, top_k=top_k, category=category,
                  recent_days=recent_days)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(
        description="PRINTMAXX Semantic Memory Search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 semantic_memory_search.py "what methods are failing"
  python3 semantic_memory_search.py --query "lead pipeline" --top 5
  python3 semantic_memory_search.py --category learnings "rebalancer scores"
  python3 semantic_memory_search.py --recent 7 "overnight session"
  python3 semantic_memory_search.py --live "cold email performance"
  python3 semantic_memory_search.py --index
  python3 semantic_memory_search.py --stats
        """)
    p.add_argument("query", nargs="?", help="Search query")
    p.add_argument("--query", "-q", dest="query_flag",
                   help="Search query (alternative)")
    p.add_argument("--index", action="store_true",
                   help="Rebuild the search index")
    p.add_argument("--stats", action="store_true",
                   help="Show index statistics")
    p.add_argument("--top", "-k", type=int, default=10,
                   help="Number of results (default: 10)")
    p.add_argument("--category", "-c",
                   help="Filter by category")
    p.add_argument("--recent", type=int, metavar="DAYS",
                   help="Only search last N days")
    p.add_argument("--live", action="store_true",
                   help="Search directly from files (slower, always fresh)")
    p.add_argument("--export", metavar="FILE",
                   help="Export results as JSON")

    args = p.parse_args()
    q = args.query or args.query_flag

    if args.index:
        build_index()
    elif args.stats:
        cmd_stats()
    elif q:
        if args.live:
            cmd_live_search(q, top_k=args.top, category=args.category,
                            recent_days=args.recent)
        else:
            cmd_search(q, top_k=args.top, category=args.category,
                       recent_days=args.recent, export_path=args.export)
    else:
        p.print_help()
